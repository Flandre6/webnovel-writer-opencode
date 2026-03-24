#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正文导出管理器

支持将章节正文导出为多种格式：
- TXT: 纯文本
- EPUB: 电子书
- DOCX: Word 文档（符合 docx skill 规范）
"""

from __future__ import annotations

import argparse
import io
import os
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

# Windows 控制台编码修复
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass


class ExportManager:
    """正文导出管理器"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.novel_dir = self.project_root / "正文"
        self.output_dir = self.project_root / "导出"

    def get_chapter_list(self) -> List[int]:
        """获取章节列表"""
        chapters = []
        if not self.novel_dir.exists():
            return chapters

        for f in self.novel_dir.iterdir():
            if f.is_file() and f.suffix == ".md":
                match = re.match(r"第(\d+)章", f.stem)
                if match:
                    chapters.append(int(match.group(1)))

        return sorted(chapters)

    def parse_chapter_range(self, range_str: str) -> List[int]:
        """解析章节范围

        支持格式：
        - "1-10" -> [1, 2, ..., 10]
        - "1,3,5" -> [1, 3, 5]
        - "1,3-5,10" -> [1, 3, 4, 5, 10]
        - "all" -> 全部章节
        """
        if range_str.lower() == "all":
            return self.get_chapter_list()

        chapters = []
        parts = range_str.split(",")

        for part in parts:
            part = part.strip()
            if "-" in part:
                start, end = part.split("-", 1)
                chapters.extend(range(int(start), int(end) + 1))
            else:
                chapters.append(int(part))

        return sorted(set(chapters))

    def get_chapter_content(self, chapter: int) -> Tuple[str, str]:
        """获取章节内容

        Returns:
            (title, content): 章节标题和正文内容
        """
        padded = f"{chapter:04d}"

        # 尝试带标题的文件名
        for pattern in [f"第{padded}章-*.md", f"第{padded}章.md"]:
            matches = list(self.novel_dir.glob(pattern))
            if matches:
                file_path = matches[0]
                content = file_path.read_text(encoding="utf-8")
                # 从文件名提取标题
                title = file_path.stem.replace(f"第{padded}章-", "").replace(f"第{padded}章", "")
                return title or f"第{chapter}章", content

        return f"第{chapter}章", ""

    def strip_frontmatter(self, content: str) -> str:
        """去除 frontmatter"""
        lines = content.split("\n")
        in_frontmatter = False
        frontmatter_count = 0
        result_lines = []

        for line in lines:
            if line.strip() == "---":
                frontmatter_count += 1
                if frontmatter_count == 1:
                    in_frontmatter = True
                    continue
                elif frontmatter_count == 2:
                    in_frontmatter = False
                    continue
            if not in_frontmatter and line.strip():
                result_lines.append(line)

        return "\n".join(result_lines)

    def export_to_txt(
        self,
        chapters: List[int],
        output_path: str,
        include_title: bool = True,
        add_separator: bool = True,
    ) -> int:
        """导出为 TXT 格式

        Args:
            chapters: 章节列表
            output_path: 输出文件路径
            include_title: 是否包含章节标题
            add_separator: 章节之间是否添加分隔符

        Returns:
            导出的章节数量
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)

        output_file = Path(output_path)
        if output_file.is_dir():
            output_file = self.output_dir / "novel.txt"

        with open(output_file, "w", encoding="utf-8") as f:
            for i, chapter in enumerate(chapters):
                title, content = self.get_chapter_content(chapter)

                if include_title:
                    f.write(f"\n{title}\n")
                    f.write("=" * len(title) + "\n\n")

                # 去除 frontmatter
                clean_content = self.strip_frontmatter(content)
                f.write(clean_content)

                if add_separator and i < len(chapters) - 1:
                    f.write("\n\n" + "=" * 40 + "\n\n")

        print(f"OK: Exported TXT: {output_file} ({len(chapters)} chapters)")
        return len(chapters)

    def export_to_docx(
        self,
        chapters: List[int],
        output_path: str,
    ) -> int:
        """导出为 DOCX 格式（符合 docx skill 规范）

        - US Letter 页面大小 (12240 x 15840 DXA)
        - Arial 字体
        - 段落间距 120 DXA
        - 章节标题 Heading 1 样式
        - 章节间分页符
        """
        try:
            from docx import Document
            from docx.shared import Pt, RGBColor, Inches
            from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
            from docx.oxml.shared import OxmlElement
            from docx.oxml.ns import qn
        except ImportError:
            print("ERROR: python-docx not installed")
            print("Run: pip install python-docx")
            return 0

        self.output_dir.mkdir(parents=True, exist_ok=True)

        output_file = Path(output_path)
        if output_file.is_dir():
            output_file = self.output_dir / "novel.docx"

        # 创建文档，设置默认样式
        doc = Document()

        # 设置文档默认字体（符合 docx skill 规范）
        style = doc.styles["Normal"]
        style.font.name = "Arial"
        style.font.size = Pt(12)
        style._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

        # 设置段落间距
        style.paragraph_format.line_spacing = 1.5
        style.paragraph_format.space_after = Pt(6)

        # 添加小说标题
        title = doc.add_heading(self.project_root.name, 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # 设置标题样式
        title_style = doc.styles["Heading 1"]
        title_style.font.name = "Arial"
        title_style.font.size = Pt(16)
        title_style.font.bold = True
        title_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title_style.paragraph_format.space_before = Pt(720)
        title_style.paragraph_format.space_after = Pt(360)

        for i, chapter in enumerate(chapters):
            chapter_title, content = self.get_chapter_content(chapter)

            # 章节标题（使用 Heading 1）
            h = doc.add_heading(chapter_title, level=1)

            # 获取并设置 Heading 1 样式
            h_style = doc.styles["Heading 1"]
            h_style.font.name = "Arial"
            h_style.font.size = Pt(14)
            h_style.font.bold = True

            # 处理内容
            clean_content = self.strip_frontmatter(content)

            # 按段落分割，保留空行
            paragraphs = clean_content.split("\n\n")
            for para_text in paragraphs:
                if para_text.strip():
                    p = doc.add_paragraph(para_text.strip())
                    # 设置段落样式
                    p_format = p.paragraph_format
                    p_format.space_before = Pt(0)
                    p_format.space_after = Pt(6)
                    p_format.line_spacing = 1.5

            # 章节间添加分页符（最后一章除外）
            if i < len(chapters) - 1:
                doc.add_page_break()

        doc.save(str(output_file))
        print(f"OK: Exported DOCX: {output_file} ({len(chapters)} chapters)")
        return len(chapters)

    def export_to_epub(
        self,
        chapters: List[int],
        output_path: str,
        author: str = "Unknown Author",
        language: str = "zh-CN",
    ) -> int:
        """导出为 EPUB 格式"""
        try:
            import ebooklib
            from ebooklib import epub
        except ImportError:
            print("ERROR: ebooklib not installed")
            print("Run: pip install ebooklib")
            return 0

        self.output_dir.mkdir(parents=True, exist_ok=True)

        output_file = Path(output_path)
        if output_file.is_dir():
            output_file = self.output_dir / "novel.epub"

        book = epub.EpubBook()

        # 设置元数据
        book.set_identifier(f"novel-{self.project_root.name}")
        book.set_title(self.project_root.name)
        book.set_language(language)
        book.add_author(author)

        spine = ["nav"]
        toc = []

        for chapter in chapters:
            chapter_title, content = self.get_chapter_content(chapter)

            # 创建章节
            c = epub.EpubHtml(
                title=chapter_title,
                file_name=f"chapter_{chapter}.xhtml",
                lang=language,
            )

            # 处理内容为 HTML
            clean_content = self.strip_frontmatter(content)
            html_content = f'<div style="font-family: Arial, sans-serif; line-height: 1.6;">\n'
            html_content += f"<h1>{chapter_title}</h1>\n"

            for para in clean_content.split("\n\n"):
                if para.strip():
                    html_content += f"<p>{para.strip()}</p>\n"

            html_content += "</div>"
            c.content = html_content
            book.add_item(c)

            spine.append(c)
            toc.append(c)

        # 设置目录和脊
        book.toc = tuple(toc)
        book.spine = spine

        # 添加导航文件
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # 保存文件
        epub.write_epub(str(output_file), book, {})
        print(f"OK: Exported EPUB: {output_file} ({len(chapters)} chapters)")
        return len(chapters)


def main():
    parser = argparse.ArgumentParser(description="Novel Export Tool")
    parser.add_argument("--project-root", required=True, help="Project root directory")

    sub = parser.add_subparsers(dest="command", required=True)

    # list 命令
    p_list = sub.add_parser("list", help="List available chapters")
    p_list.set_defaults(func=cmd_list)

    # export 命令
    p_export = sub.add_parser("export", help="Export chapters")
    p_export.add_argument(
        "--range",
        default="all",
        help="Chapter range, e.g., 1-10,15,20-30 or all",
    )
    p_export.add_argument(
        "--format",
        choices=["txt", "docx", "epub"],
        default="txt",
        help="Export format",
    )
    p_export.add_argument(
        "--output",
        help="Output file path (auto-generated if not specified)",
    )
    p_export.add_argument("--author", default="Unknown Author", help="Author name")
    p_export.set_defaults(func=cmd_export)

    args = parser.parse_args()

    if args.command == "list":
        manager = ExportManager(args.project_root)
        chapters = manager.get_chapter_list()
        if chapters:
            print(f"Available chapters: {chapters}")
            print(f"Total: {len(chapters)} chapters")
        else:
            print("No chapter files found")
        return

    if args.command == "export":
        manager = ExportManager(args.project_root)
        chapters = manager.parse_chapter_range(args.range)

        if not chapters:
            print("No chapters to export")
            return

        output_path = args.output or f"novel.{args.format}"

        if args.format == "txt":
            manager.export_to_txt(chapters, output_path)
        elif args.format == "docx":
            manager.export_to_docx(chapters, output_path)
        elif args.format == "epub":
            manager.export_to_epub(chapters, output_path, author=args.author)


def cmd_list(args):
    pass


def cmd_export(args):
    pass


if __name__ == "__main__":
    main()

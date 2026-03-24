#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
正文导出管理器

支持将章节正文导出为多种格式：
- TXT: 纯文本
- EPUB: 电子书
- Markdown: Markdown 格式
"""

from __future__ import annotations

import argparse
import io
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

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

    def get_volumes(self) -> List[int]:
        """获取卷号列表"""
        volumes: Set[int] = set()
        if not self.novel_dir.exists():
            return []

        for root, dirs, files in os.walk(self.novel_dir):
            for d in dirs:
                match = re.search(r"第([0-9]+)卷", d)
                if match:
                    volumes.add(int(match.group(1)))

        return sorted(volumes)

    def get_volume_chapters(self, volume: int) -> List[int]:
        """获取指定卷的章节列表"""
        chapters: List[int] = []
        volume_dir = self.novel_dir / f"第{volume}卷"

        if not volume_dir.exists():
            for root, dirs, files in os.walk(self.novel_dir):
                for d in dirs:
                    if d == f"第{volume}卷":
                        volume_dir = self.novel_dir / d
                        break

        if not volume_dir.exists():
            return []

        for root, dirs, files in os.walk(volume_dir):
            for f in files:
                if f.endswith(".md"):
                    match = re.search(r"第(\d+)章", f)
                    if match:
                        chapters.append(int(match.group(1)))

        return sorted(chapters)

    def get_chapter_list(self) -> List[int]:
        """获取章节列表（递归搜索所有子目录）"""
        chapters: List[int] = []
        if not self.novel_dir.exists():
            return chapters

        for root, dirs, files in os.walk(self.novel_dir):
            for f in files:
                if f.endswith(".md"):
                    match = re.search(r"第(\d+)章", f)
                    if match:
                        chapters.append(int(match.group(1)))

        return sorted(set(chapters))

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

        chapters: List[int] = []
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
        """获取章节内容（递归搜索所有子目录）

        Returns:
            (title, content): 章节标题和正文内容
        """
        padded = f"{chapter:04d}"

        for root, dirs, files in os.walk(self.novel_dir):
            for f in files:
                if f.endswith(".md") and f"第{padded}章" in f:
                    file_path = os.path.join(root, f)
                    content = Path(file_path).read_text(encoding="utf-8")
                    title = f.replace(".md", "").replace(f"第{padded}章-", "").replace(f"第{padded}章", "")
                    return title or f"第{chapter}章", content

        return f"第{chapter}章", ""

    def strip_frontmatter(self, content: str) -> str:
        """去除 frontmatter"""
        lines = content.split("\n")
        in_frontmatter = False
        frontmatter_count = 0
        result_lines: List[str] = []

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

    def export_to_markdown(
        self,
        chapters: List[int],
        output_path: str,
        add_separator: bool = True,
    ) -> int:
        """导出为 Markdown 格式

        Args:
            chapters: 章节列表
            output_path: 输出文件路径
            add_separator: 章节之间是否添加分隔符

        Returns:
            导出的章节数量
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)

        output_file = Path(output_path)
        if output_file.is_dir():
            output_file = self.output_dir / "novel.md"

        with open(output_file, "w", encoding="utf-8") as f:
            for i, chapter in enumerate(chapters):
                title, content = self.get_chapter_content(chapter)

                f.write(f"# {title}\n\n")

                clean_content = self.strip_frontmatter(content)
                f.write(clean_content)

                if add_separator and i < len(chapters) - 1:
                    f.write("\n\n---\n\n")

        print(f"OK: Exported Markdown: {output_file} ({len(chapters)} chapters)")
        return len(chapters)

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

                clean_content = self.strip_frontmatter(content)
                f.write(clean_content)

                if add_separator and i < len(chapters) - 1:
                    f.write("\n\n" + "=" * 40 + "\n\n")

        print(f"OK: Exported TXT: {output_file} ({len(chapters)} chapters)")
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

        book.set_identifier(f"novel-{self.project_root.name}")
        book.set_title(self.project_root.name)
        book.set_language(language)
        book.add_author(author)

        spine = ["nav"]
        toc = []

        for chapter in chapters:
            chapter_title, content = self.get_chapter_content(chapter)

            c = epub.EpubHtml(
                title=chapter_title,
                file_name=f"chapter_{chapter}.xhtml",
                lang=language,
            )

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

        book.toc = tuple(toc)
        book.spine = spine

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        epub.write_epub(str(output_file), book, {})
        print(f"OK: Exported EPUB: {output_file} ({len(chapters)} chapters)")
        return len(chapters)


def main():
    parser = argparse.ArgumentParser(description="Novel Export Tool")
    parser.add_argument("--project-root", required=True, help="Project root directory")

    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List available chapters")
    p_list.add_argument("--volume", type=int, help="List chapters in specific volume")
    p_list.set_defaults(func=cmd_list)

    p_export = sub.add_parser("export", help="Export chapters")
    p_export.add_argument(
        "--range",
        default="all",
        help="Chapter range, e.g., 1-10,15,20-30 or all",
    )
    p_export.add_argument(
        "--volume",
        type=int,
        help="Export specific volume",
    )
    p_export.add_argument(
        "--format",
        choices=["markdown", "txt", "epub"],
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

    manager = ExportManager(args.project_root)

    if args.command == "list":
        if args.volume:
            chapters = manager.get_volume_chapters(args.volume)
            if chapters:
                print(f"Chapters in Volume {args.volume}: {chapters}")
                print(f"Total: {len(chapters)} chapters")
            else:
                print(f"No chapters found in Volume {args.volume}")
        else:
            chapters = manager.get_chapter_list()
            if chapters:
                print(f"Available chapters: {chapters}")
                print(f"Total: {len(chapters)} chapters")
            else:
                print("No chapter files found")

            volumes = manager.get_volumes()
            if volumes:
                print(f"\nAvailable volumes: {volumes}")
        return

    if args.command == "export":
        if args.volume:
            chapters = manager.get_volume_chapters(args.volume)
            if not chapters:
                print(f"No chapters found in Volume {args.volume}")
                return
        else:
            chapters = manager.parse_chapter_range(args.range)

        if not chapters:
            print("No chapters to export")
            return

        default_output = manager.output_dir / f"novel.{args.format}"
        output_path = args.output if args.output else default_output

        if args.format == "markdown":
            manager.export_to_markdown(chapters, output_path)
        elif args.format == "txt":
            manager.export_to_txt(chapters, output_path)
        elif args.format == "epub":
            manager.export_to_epub(chapters, output_path, author=args.author)


def cmd_list(args):
    pass


def cmd_export(args):
    pass


if __name__ == "__main__":
    main()

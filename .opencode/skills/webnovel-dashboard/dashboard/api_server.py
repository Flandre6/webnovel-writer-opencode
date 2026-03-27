#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
看板 API 服务器 - 提供数据接口供前端调用
"""

import http.server
import socketserver
import json
import sqlite3
import urllib.parse
from pathlib import Path

PORT = 8086
PROJECT_ROOT = None


class APIHandler(http.server.SimpleHTTPRequestHandler):
    """API 请求处理器"""

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        params = urllib.parse.parse_qs(parsed.query)

        try:
            if path == '/api/files/tree':
                self.handle_file_tree()
            elif path == '/api/files/read':
                self.handle_file_read(params)
            elif path == '/api/entities':
                self.handle_entities(params)
            elif path == '/api/state-changes':
                self.handle_state_changes(params)
            elif path == '/api/reading-power':
                self.handle_reading_power(params)
            elif path == '/api/chapters':
                self.handle_chapters()
            elif path == '/api/scenes':
                self.handle_scenes(params)
            elif path == '/api/relationships':
                self.handle_relationships(params)
            elif path == '/api/review-metrics':
                self.handle_review_metrics(params)
            else:
                self.send_error(404, 'Not Found')
        except Exception as e:
            self.send_json({'error': str(e)}, 500)

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def handle_file_tree(self):
        result = {}
        for folder_name in ['正文', '大纲', '设定集']:
            folder = PROJECT_ROOT / folder_name
            if folder.is_dir():
                result[folder_name] = self._walk_tree(folder)
            else:
                result[folder_name] = []
        self.send_json(result)

    def _walk_tree(self, folder):
        items = []
        try:
            for child in sorted(folder.iterdir()):
                if child.name.startswith('.'):
                    continue
                if child.is_dir():
                    items.append({
                        'name': child.name,
                        'type': 'dir',
                        'path': str(child.relative_to(PROJECT_ROOT)).replace('\\', '/'),
                        'children': self._walk_tree(child)
                    })
                else:
                    items.append({
                        'name': child.name,
                        'type': 'file',
                        'path': str(child.relative_to(PROJECT_ROOT)).replace('\\', '/'),
                        'size': child.stat().st_size
                    })
        except Exception:
            pass
        return items

    def handle_file_read(self, params):
        path = params.get('path', [''])[0]
        if not path:
            self.send_json({'error': '缺少 path 参数'}, 400)
            return

        full_path = (PROJECT_ROOT / path).resolve()
        if not str(full_path).startswith(str(PROJECT_ROOT.resolve())):
            self.send_json({'error': '非法路径'}, 403)
            return

        allowed = ['正文', '大纲', '设定集']
        rel = full_path.relative_to(PROJECT_ROOT)
        if rel.parts[0] not in allowed:
            self.send_json({'error': '仅允许访问正文/大纲/设定集'}, 403)
            return

        if not full_path.is_file():
            self.send_json({'error': '文件不存在'}, 404)
            return

        try:
            content = full_path.read_text(encoding='utf-8')
            self.send_json({'path': path, 'content': content})
        except UnicodeDecodeError:
            self.send_json({'error': '二进制文件，无法预览'}, 400)

    def get_db(self):
        db_path = PROJECT_ROOT / '.webnovel' / 'index.db'
        if not db_path.is_file():
            return None
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def handle_entities(self, params):
        conn = self.get_db()
        if not conn:
            self.send_json([])
            return

        entity_type = params.get('type', [''])[0]
        try:
            if entity_type:
                rows = conn.execute(
                    'SELECT * FROM entities WHERE type = ? ORDER BY last_appearance DESC',
                    (entity_type,)
                ).fetchall()
            else:
                rows = conn.execute(
                    'SELECT * FROM entities ORDER BY last_appearance DESC'
                ).fetchall()
            self.send_json([dict(r) for r in rows])
        except sqlite3.OperationalError:
            self.send_json([])
        finally:
            conn.close()

    def handle_state_changes(self, params):
        conn = self.get_db()
        if not conn:
            self.send_json([])
            return

        entity = params.get('entity', [''])[0]
        limit = int(params.get('limit', ['100'])[0])
        try:
            if entity:
                rows = conn.execute(
                    'SELECT * FROM state_changes WHERE entity_id = ? ORDER BY chapter DESC LIMIT ?',
                    (entity, limit)
                ).fetchall()
            else:
                rows = conn.execute(
                    'SELECT * FROM state_changes ORDER BY chapter DESC LIMIT ?',
                    (limit,)
                ).fetchall()
            self.send_json([dict(r) for r in rows])
        except sqlite3.OperationalError:
            self.send_json([])
        finally:
            conn.close()

    def handle_reading_power(self, params):
        conn = self.get_db()
        if not conn:
            self.send_json([])
            return

        limit = int(params.get('limit', ['50'])[0])
        try:
            rows = conn.execute(
                'SELECT * FROM chapter_reading_power ORDER BY chapter DESC LIMIT ?',
                (limit,)
            ).fetchall()
            self.send_json([dict(r) for r in rows])
        except sqlite3.OperationalError:
            self.send_json([])
        finally:
            conn.close()

    def handle_chapters(self):
        conn = self.get_db()
        if not conn:
            self.send_json([])
            return

        try:
            rows = conn.execute(
                'SELECT * FROM chapters ORDER BY chapter ASC'
            ).fetchall()
            self.send_json([dict(r) for r in rows])
        except sqlite3.OperationalError:
            self.send_json([])
        finally:
            conn.close()

    def handle_scenes(self, params):
        conn = self.get_db()
        if not conn:
            self.send_json([])
            return

        chapter = params.get('chapter', [''])[0]
        limit = int(params.get('limit', ['200'])[0])
        try:
            if chapter:
                rows = conn.execute(
                    'SELECT * FROM scenes WHERE chapter = ? ORDER BY scene_index ASC',
                    (int(chapter),)
                ).fetchall()
            else:
                rows = conn.execute(
                    'SELECT * FROM scenes ORDER BY chapter ASC, scene_index ASC LIMIT ?',
                    (limit,)
                ).fetchall()
            self.send_json([dict(r) for r in rows])
        except sqlite3.OperationalError:
            self.send_json([])
        finally:
            conn.close()

    def handle_relationships(self, params):
        conn = self.get_db()
        if not conn:
            self.send_json([])
            return

        limit = int(params.get('limit', ['300'])[0])
        try:
            rows = conn.execute(
                'SELECT * FROM relationships ORDER BY chapter DESC LIMIT ?',
                (limit,)
            ).fetchall()
            self.send_json([dict(r) for r in rows])
        except sqlite3.OperationalError:
            self.send_json([])
        finally:
            conn.close()

    def handle_review_metrics(self, params):
        conn = self.get_db()
        if not conn:
            self.send_json([])
            return

        limit = int(params.get('limit', ['20'])[0])
        try:
            rows = conn.execute(
                'SELECT * FROM review_metrics ORDER BY end_chapter DESC LIMIT ?',
                (limit,)
            ).fetchall()
            self.send_json([dict(r) for r in rows])
        except sqlite3.OperationalError:
            self.send_json([])
        finally:
            conn.close()

    def log_message(self, format, *args):
        if '/api/' in str(args):
            print(f"[API] {args[0]}")


def main():
    global PROJECT_ROOT, PORT

    import sys
    args = sys.argv[1:]

    if '--help' in args or '-h' in args:
        print(f"用法: python {sys.argv[0]} [项目根目录] [--port PORT]")
        print(f"默认端口: {PORT}")
        return

    for i, arg in enumerate(args):
        if not arg.startswith('--') and arg != '--port':
            if i > 0 and args[i-1] == '--port':
                continue
            PROJECT_ROOT = Path(arg).resolve()
            break

    if not PROJECT_ROOT:
        PROJECT_ROOT = Path.cwd().resolve()

    if '--port' in args:
        idx = args.index('--port')
        if idx + 1 < len(args):
            PORT = int(args[idx + 1])

    print(f"项目根目录: {PROJECT_ROOT}")
    print(f"API 服务器启动在: http://localhost:{PORT}")

    with socketserver.TCPServer(("", PORT), APIHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")


if __name__ == "__main__":
    main()

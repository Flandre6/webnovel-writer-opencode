#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说看板 - 本地服务器启动脚本
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8085

# 全局变量
PROJECT_ROOT = None
DASHBOARD_DIR = None


class DualHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = path.lstrip('/')
        
        # 优先从 dashboard 目录查找
        dashboard_path = os.path.join(DASHBOARD_DIR, path)
        if os.path.isfile(dashboard_path):
            return dashboard_path
        
        # 从项目根目录查找数据文件
        if path.startswith('.webnovel/') or path.startswith('大纲/') or path.startswith('正文/'):
            project_path = os.path.join(PROJECT_ROOT, path)
            if os.path.isfile(project_path):
                return project_path
        
        # 尝试向上查找项目根目录
        if '.webnovel/' in path or '大纲/' in path or '正文/' in path:
            for parent_dir in [DASHBOARD_DIR] + self._get_parent_dirs(DASHBOARD_DIR):
                potential_root = os.path.dirname(parent_dir)
                for _ in range(5):
                    if os.path.exists(os.path.join(potential_root, '.webnovel')):
                        project_path = os.path.join(potential_root, path)
                        if os.path.isfile(project_path):
                            return project_path
                    potential_root = os.path.dirname(potential_root)
        
        return os.path.join(DASHBOARD_DIR, path)
    
    def _get_parent_dirs(self, path):
        parents = []
        current = path
        for _ in range(10):
            parent = os.path.dirname(current)
            if parent == current:
                break
            parents.append(parent)
            current = parent
        return parents
    
    def log_message(self, format, *args):
        pass


def main():
    global PROJECT_ROOT, DASHBOARD_DIR
    
    # dashboard 目录
    DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # 项目根目录
    PROJECT_ROOT = os.path.dirname(DASHBOARD_DIR)
    
    # 查找实际项目根目录
    markers = ['.webnovel', 'novel.txt', '大纲', '正文']
    for m in markers:
        if os.path.exists(os.path.join(PROJECT_ROOT, m)):
            break
    else:
        # 向上查找
        current = PROJECT_ROOT
        while current:
            if any(os.path.exists(os.path.join(current, m)) for m in markers):
                PROJECT_ROOT = current
                break
            parent = os.path.dirname(current)
            if parent == current:
                break
            current = parent
    
    # state.json 相对路径
    state_rel_path = '.webnovel/state.json'
    
    print("=" * 50)
    print("  Novel Dashboard - Local Server")
    print("=" * 50)
    print()
    print(f"Project: {PROJECT_ROOT}")
    print(f"Dashboard: {DASHBOARD_DIR}")
    print(f"Data: {state_rel_path}")
    print()
    print(f"Server running at: http://localhost:{PORT}")
    print("Press Ctrl+C to stop server")
    print()
    
    # 写入配置文件
    config_path = os.path.join(DASHBOARD_DIR, 'config.js')
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(f"window.DASHBOARD_CONFIG = {{\n")
        f.write(f"    projectRoot: '{PROJECT_ROOT.replace(chr(92), '/')}',\n")
        f.write(f"    stateJsonPath: '{state_rel_path}'\n")
        f.write(f"}};\n")
    
    # 切换到 dashboard 目录
    os.chdir(DASHBOARD_DIR)
    
    # 自动打开浏览器
    try:
        webbrowser.open(f"http://localhost:{PORT}")
    except:
        pass
    
    with socketserver.TCPServer(("", PORT), DualHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            if os.path.exists(config_path):
                os.remove(config_path)


if __name__ == "__main__":
    main()

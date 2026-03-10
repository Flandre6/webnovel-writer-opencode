#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
webnovel 统一入口脚本（无须 `cd`）

用法示例：
  python -m scripts.webnovel where
  python -m scripts.webnovel index stats

说明：
- 该脚本转发到 `data_modules.webnovel`。
- 适配 OpenCode Skills 调用。
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add scripts directory to path for internal imports
_scripts_dir = Path(__file__).resolve().parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

from runtime_compat import enable_windows_utf8_stdio


def main() -> None:
    """Main entry point."""
    # Import and run the data_modules main
    from data_modules.webnovel import main as _main
    _main()


if __name__ == "__main__":
    enable_windows_utf8_stdio(skip_in_pytest=True)
    main()


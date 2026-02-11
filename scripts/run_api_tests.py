#!/usr/bin/env python3
"""
统一的 API 测试运行入口。

默认行为：
- 禁用第三方 pytest 插件自动加载（减少环境噪音与启动抖动）
- 执行 `pytest api_tests -v`

示例：
  python scripts/run_api_tests.py
  python scripts/run_api_tests.py api_tests/admin -v
  python scripts/run_api_tests.py api_tests -v --no-tapd-report
  python scripts/run_api_tests.py --with-third-party-plugins api_tests -v
"""

import argparse
import os
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Run API tests with stable defaults")
    parser.add_argument(
        "--with-third-party-plugins",
        action="store_true",
        help="Enable pytest third-party plugin autoload (disabled by default)",
    )
    args, pytest_args = parser.parse_known_args()

    if not pytest_args:
        pytest_args = ["api_tests", "-v"]

    env = os.environ.copy()
    if not args.with_third_party_plugins:
        env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"

    cmd = [sys.executable, "-m", "pytest", *pytest_args]
    print("[RUN]", " ".join(cmd))
    if not args.with_third_party_plugins:
        print("[INFO] PYTEST_DISABLE_PLUGIN_AUTOLOAD=1")

    return subprocess.run(cmd, env=env).returncode


if __name__ == "__main__":
    raise SystemExit(main())

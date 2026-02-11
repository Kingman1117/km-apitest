#!/usr/bin/env python3
"""
统一的 API 测试运行入口。

默认行为：
- 禁用第三方 pytest 插件自动加载（减少环境噪音与启动抖动）
- 执行 `pytest api_tests -v`

示例：
  python scripts/run_api_tests.py
  python scripts/run_api_tests.py api_tests/admin -v
  python scripts/run_api_tests.py --junit                    # 生成 JUnit XML
  python scripts/run_api_tests.py --html                     # 生成 HTML 报告
  python scripts/run_api_tests.py --junit --html             # 同时生成两种报告
  python scripts/run_api_tests.py --with-third-party-plugins # 启用第三方插件
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run API tests with stable defaults",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--with-third-party-plugins",
        action="store_true",
        help="Enable pytest third-party plugin autoload (disabled by default)",
    )
    parser.add_argument(
        "--junit",
        action="store_true",
        help="Generate JUnit XML report (saved to reports/junit.xml)",
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Generate HTML report (saved to reports/report-<timestamp>.html)",
    )
    args, pytest_args = parser.parse_known_args()

    if not pytest_args:
        pytest_args = ["api_tests", "-v"]

    # 创建 reports 目录
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    # 添加报告参数
    if args.junit:
        pytest_args.extend(["--junit-xml", "reports/junit.xml"])
        print("[INFO] JUnit XML 报告将保存到: reports/junit.xml")

    if args.html:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_report = f"reports/report-{timestamp}.html"
        pytest_args.extend(["--html", html_report, "--self-contained-html"])
        print(f"[INFO] HTML 报告将保存到: {html_report}")

    env = os.environ.copy()
    if not args.with_third-party-plugins:
        env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"

    cmd = [sys.executable, "-m", "pytest", *pytest_args]
    print("[RUN]", " ".join(cmd))
    if not args.with_third_party_plugins:
        print("[INFO] PYTEST_DISABLE_PLUGIN_AUTOLOAD=1")

    return subprocess.run(cmd, env=env).returncode


if __name__ == "__main__":
    raise SystemExit(main())

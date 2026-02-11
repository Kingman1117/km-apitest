#!/usr/bin/env python3
"""
自动化测试执行脚本（带TAPD回填）

使用方式:
    # 使用配置文件中的测试计划
    python scripts/run_test_with_tapd.py
    
    # 指定测试计划ID
    python scripts/run_test_with_tapd.py --plan-id 1150695810001001509
    
    # 指定测试计划ID和名称
    python scripts/run_test_with_tapd.py --plan-id 1150695810001001509 --plan-name "第7期验收"
    
    # 禁用TAPD回填
    python scripts/run_test_with_tapd.py --no-tapd

    # 启用第三方pytest插件自动加载
    python scripts/run_test_with_tapd.py --with-third-party-plugins
"""

import argparse
import subprocess
import json
import sys
import os
from pathlib import Path
from datetime import datetime


def update_tapd_config(plan_id, plan_name=None):
    """更新TAPD配置文件中的测试计划ID"""
    config_path = Path("config/tapd_config.json")
    
    if not config_path.exists():
        print(f"错误: 配置文件不存在: {config_path}")
        return False
    
    try:
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)
        
        if "current_test_plan" not in config:
            config["current_test_plan"] = {}
        
        config["current_test_plan"]["id"] = plan_id
        if plan_name:
            config["current_test_plan"]["name"] = plan_name
        config["current_test_plan"]["updated_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print(f"[OK] 已更新测试计划ID: {plan_id}")
        if plan_name:
            print(f"[OK] 测试计划名称: {plan_name}")
        return True
    
    except Exception as e:
        print(f"错误: 更新配置文件失败: {e}")
        return False


def run_pytest(extra_args=None, with_third_party_plugins=False):
    """执行pytest测试"""
    print("\n" + "="*60)
    print("开始执行自动化测试...")
    print("="*60 + "\n")

    cmd = [sys.executable, "scripts/run_api_tests.py", "api_tests/", "-v", "--tb=short"]
    if with_third_party_plugins:
        cmd.insert(2, "--with-third-party-plugins")
    if extra_args:
        cmd.extend(extra_args)

    env = os.environ.copy()
    result = subprocess.run(cmd, capture_output=False, env=env)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="执行自动化测试并回填TAPD",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/run_test_with_tapd.py
  python scripts/run_test_with_tapd.py --plan-id 1150695810001001509
  python scripts/run_test_with_tapd.py --plan-id 1150695810001001509 --plan-name "第7期验收"
  python scripts/run_test_with_tapd.py --no-tapd
        """
    )
    
    parser.add_argument(
        "--plan-id",
        help="TAPD测试计划ID（如: 1150695810001001509）"
    )
    parser.add_argument(
        "--plan-name",
        help="测试计划名称（可选）"
    )
    parser.add_argument(
        "--no-update-config",
        action="store_true",
        help="不更新配置文件，仅通过命令行传递"
    )
    parser.add_argument(
        "--no-tapd",
        action="store_true",
        help="禁用TAPD回填"
    )
    parser.add_argument(
        "--with-third-party-plugins",
        action="store_true",
        help="启用 pytest 第三方插件自动加载（默认禁用）",
    )
    
    args = parser.parse_args()
    
    # 更新配置文件
    if args.plan_id and not args.no_update_config:
        if not update_tapd_config(args.plan_id, args.plan_name):
            return 1
    
    # 构建pytest额外参数
    extra_args = []
    if args.plan_id and args.no_update_config:
        extra_args.append(f"--tapd-plan={args.plan_id}")
    if args.no_tapd:
        extra_args.append("--no-tapd-report")
    
    # 执行测试
    exit_code = run_pytest(extra_args, with_third_party_plugins=args.with_third_party_plugins)
    
    print("\n" + "="*60)
    if exit_code == 0:
        print("[OK] 所有测试通过，TAPD回填完成")
    else:
        print(f"[失败] 测试失败，退出码: {exit_code}")
    print("="*60 + "\n")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())

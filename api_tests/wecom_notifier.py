"""
企业微信通知封装。
"""
import logging
import time
from datetime import datetime
from typing import Dict, List

import requests


logger = logging.getLogger(__name__)


class WecomResultCollector:
    """测试结果收集器。"""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.start_time = None
        self.failed_cases: List[str] = []

    def start(self):
        self.start_time = time.time()
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.failed_cases = []

    def record(self, report):
        if report.when != "call":
            return
        if report.passed:
            self.passed += 1
        elif report.failed:
            self.failed += 1
            self.failed_cases.append(report.nodeid.split("::")[-1])
        elif report.skipped:
            self.skipped += 1

    def send(self, tapd_config: Dict) -> None:
        if not tapd_config.get("wecom_enabled", False):
            return
        webhook_url = tapd_config.get("wecom_webhook")
        if not webhook_url:
            return

        total = self.passed + self.failed + self.skipped
        if total == 0:
            return

        if self.failed == 0 and not tapd_config.get("wecom_notify_on_success", True):
            return
        if self.failed > 0 and not tapd_config.get("wecom_notify_on_failure", True):
            return

        duration = time.time() - self.start_time if self.start_time else 0
        pass_rate = self.passed / total * 100 if total else 0
        status = "全部通过" if self.failed == 0 else f"失败 {self.failed} 个"
        color = "info" if self.failed == 0 else "warning"

        plan_info = tapd_config.get("current_test_plan", {})
        plan_url = plan_info.get("url", "")
        plan_name = plan_info.get("name", "验收测试")

        content = f"""## API自动化测试报告
> **{plan_name}**
> 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**执行结果**: <font color="{color}">{status}</font>

| 指标 | 数值 |
|------|------|
| 总用例 | {total} |
| 通过 | <font color="info">{self.passed}</font> |
| 失败 | <font color="warning">{self.failed}</font> |
| 跳过 | {self.skipped} |
| 通过率 | {pass_rate:.1f}% |
| 耗时 | {duration:.1f}秒 |"""

        if self.failed_cases:
            top_failed = self.failed_cases[:5]
            content += "\n\n**失败用例**:\n" + "\n".join(f"- {name}" for name in top_failed)
            if len(self.failed_cases) > 5:
                content += f"\n- ...等共 {len(self.failed_cases)} 个"

        if plan_url:
            content += f"\n\n[查看TAPD测试计划]({plan_url})"

        message = {"msgtype": "markdown", "markdown": {"content": content}}
        try:
            resp = requests.post(webhook_url, json=message, timeout=10)
            result = resp.json()
            if result.get("errcode") == 0:
                logger.info("企业微信通知发送成功")
            else:
                logger.warning("企业微信通知发送失败: %s", result)
        except Exception as exc:
            logger.warning("企业微信通知发送异常: %s", exc)

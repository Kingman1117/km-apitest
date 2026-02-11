"""
TAPD 回填能力封装。
"""
import logging
import os
import re
import time
from typing import Any, Dict, Optional

import requests


logger = logging.getLogger(__name__)
_LAST_TAPD_POST_TS = 0.0


def extract_tapd_case_id(item) -> Optional[str]:
    """从模块或函数 docstring 中提取 19 位 TAPD 用例 ID。"""
    doc_candidates = []
    if hasattr(item, "module") and item.module and item.module.__doc__:
        doc_candidates.append(item.module.__doc__)
    if item.function and item.function.__doc__:
        doc_candidates.append(item.function.__doc__)

    patterns = [r"用例\s*(?:ID\s*:\s*)?(\d{19})", r"\((\d{19})\)"]
    for doc in doc_candidates:
        for pattern in patterns:
            match = re.search(pattern, doc)
            if match:
                return match.group(1)
    return None


class TAPDClient:
    """TAPD API 客户端。"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.auth = (config.get("api_user"), config.get("api_password"))
        self.base_url = config.get("base_url", "https://api.tapd.cn")
        self.workspace_id = config.get("workspace_id")

    def _build_notes(self, error_msg: Optional[str]) -> str:
        if not error_msg:
            return "自动化测试通过"

        lines = [line.strip() for line in str(error_msg).split("\n") if line.strip()]
        concise = "未知错误"
        for line in reversed(lines):
            if ("Error:" in line) or ("Exception:" in line) or ("AssertionError" in line) or ("assert " in line):
                concise = line
                break
            if len(line) > 8:
                concise = line
        return concise[:240]

    def create_test_result(self, test_plan_id: str, case_id: str, result: str, error_msg=None):
        url = f"{self.base_url}/tcase_instance/execute"
        result_status = "pass" if result == "passed" else "no_pass"
        data = {
            "workspace_id": self.workspace_id,
            "test_plan_id": test_plan_id,
            "tcase_id": case_id,
            "result_status": result_status,
            "last_executor": self.config.get("tester", "自动化测试"),
            "result_remark": self._build_notes(error_msg),
        }
        try:
            global _LAST_TAPD_POST_TS
            min_interval = float(os.getenv("TAPD_REPORT_INTERVAL_SECONDS", "0.3"))
            now = time.time()
            elapsed = now - _LAST_TAPD_POST_TS
            if min_interval > 0 and elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            response = requests.post(url, auth=self.auth, data=data, timeout=15)
            _LAST_TAPD_POST_TS = time.time()
            response.raise_for_status()
            try:
                result_data = response.json()
                if result_data.get("status") == 1:
                    return True, result_data
                return False, result_data.get("info", "未知错误")
            except Exception:
                return True, {"message": "执行成功"}
        except requests.exceptions.RequestException as exc:
            return False, str(exc)


def report_case_result(item, report, tapd_config: Dict[str, Any]) -> None:
    """执行单条用例结果回填。"""
    if report.when != "call" or not tapd_config.get("enabled"):
        return

    case_id = extract_tapd_case_id(item)
    if not case_id:
        logger.info("跳过 TAPD 回填，未找到用例 ID: %s", item.nodeid)
        return

    test_plan_id = tapd_config.get("current_test_plan", {}).get("id")
    if not test_plan_id:
        logger.warning("未配置当前测试计划 ID，跳过回填")
        return

    client = TAPDClient(tapd_config)
    status = report.outcome
    error_msg = str(report.longrepr) if report.failed else None
    success, response = client.create_test_result(test_plan_id, case_id, status, error_msg)
    if success:
        logger.info("TAPD 回填成功: case=%s status=%s", case_id, status.upper())
    else:
        logger.warning("TAPD 回填失败: case=%s reason=%s", case_id, response)

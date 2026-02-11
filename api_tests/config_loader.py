"""
配置加载工具。

职责：
- 读取 JSON 配置
- 支持环境变量覆盖
"""
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional


logger = logging.getLogger(__name__)

ROOT = Path(__file__).parent.parent
TEST_PLAN_CONFIG_PATH = ROOT / "config" / "test_plan_config.json"
TAPD_CONFIG_PATH = ROOT / "config" / "tapd_config.json"


def load_json(path: Path, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if not path.exists():
        logger.warning("配置文件不存在: %s", path)
        return default or {}
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        logger.error("配置文件加载失败 %s: %s", path, exc)
        return default or {}


def env_or_value(env_name: str, value: Any, cast=str):
    env_val = os.getenv(env_name)
    if env_val is None or env_val == "":
        return value
    if cast is bool:
        return env_val.lower() in ("1", "true", "yes", "on")
    return cast(env_val)


def load_test_plan_config() -> Dict[str, Any]:
    """加载测试配置并支持环境变量覆盖。"""
    cfg = load_json(TEST_PLAN_CONFIG_PATH, default={"credentials": {}})
    creds = cfg.setdefault("credentials", {})
    admin = creds.setdefault("admin", {})
    student = creds.setdefault("student", {})

    admin["username"] = env_or_value("KMSK_ADMIN_USERNAME", admin.get("username"))
    admin["password"] = env_or_value("KMSK_ADMIN_PASSWORD", admin.get("password"))
    student["username"] = env_or_value("KMSK_STUDENT_USERNAME", student.get("username", "km7"))
    student["password"] = env_or_value("KMSK_STUDENT_PASSWORD", student.get("password", "123456"))
    return cfg


def load_tapd_config() -> Dict[str, Any]:
    """加载 TAPD 配置并支持环境变量覆盖。"""
    cfg = load_json(TAPD_CONFIG_PATH, default={"enabled": False})
    plan = cfg.setdefault("current_test_plan", {})

    cfg["enabled"] = env_or_value("TAPD_ENABLED", cfg.get("enabled", False), cast=bool)
    cfg["workspace_id"] = env_or_value("TAPD_WORKSPACE_ID", cfg.get("workspace_id"))
    cfg["api_user"] = env_or_value("TAPD_API_USER", cfg.get("api_user"))
    cfg["api_password"] = env_or_value("TAPD_API_PASSWORD", cfg.get("api_password"))
    cfg["base_url"] = env_or_value("TAPD_BASE_URL", cfg.get("base_url", "https://api.tapd.cn"))
    cfg["tester"] = env_or_value("TAPD_TESTER", cfg.get("tester", "自动化测试"))

    plan["id"] = env_or_value("TAPD_TEST_PLAN_ID", plan.get("id"))
    plan["name"] = env_or_value("TAPD_TEST_PLAN_NAME", plan.get("name"))

    cfg["wecom_webhook"] = env_or_value("WECOM_WEBHOOK", cfg.get("wecom_webhook", ""))
    cfg["wecom_enabled"] = env_or_value("WECOM_ENABLED", cfg.get("wecom_enabled", False), cast=bool)
    cfg["wecom_notify_on_success"] = env_or_value(
        "WECOM_NOTIFY_ON_SUCCESS", cfg.get("wecom_notify_on_success", True), cast=bool
    )
    cfg["wecom_notify_on_failure"] = env_or_value(
        "WECOM_NOTIFY_ON_FAILURE", cfg.get("wecom_notify_on_failure", True), cast=bool
    )
    return cfg

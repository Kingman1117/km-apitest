"""
共享 fixtures：
- 客户端登录
- TAPD 结果回填
- 企业微信通知
"""
import logging
import os
import time

import pytest

# 全局日志配置（仅在入口处配置一次）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

from config_loader import load_tapd_config, load_test_plan_config
from tapd_reporter import report_case_result
from wecom_notifier import WecomResultCollector


logger = logging.getLogger(__name__)
TAPD_CONFIG = load_tapd_config()
WECOM_RESULTS = WecomResultCollector()


@pytest.fixture(scope="session")
def config():
    """加载测试账号配置。"""
    return load_test_plan_config()


@pytest.fixture(scope="session")
def admin_client(config):
    """登录后的管理后台客户端（session 复用）。"""
    from clients.admin_client import AdminClient

    cred = config["credentials"]["admin"]
    client = AdminClient(cred["username"], cred["password"])
    client.login()
    return client


@pytest.fixture(scope="session")
def edupc_client(config):
    """登录后的 EduPC 客户端（session 复用）。"""
    from clients.edupc_client import EduPCClient

    cred = config["credentials"]["student"]
    client = EduPCClient(cred["username"], cred["password"])
    client.login()
    return client


@pytest.fixture(scope="session")
def h5_client(config):
    """登录后的 H5 客户端（session 复用）。"""
    from clients.h5_client import H5Client

    cred = config["credentials"]["student"]
    client = H5Client(cred["username"], cred["password"])
    client.login()
    return client


@pytest.fixture
def timestamp():
    """当前时间戳后 6 位（用于唯一命名）。"""
    return str(int(time.time()))[-6:]


@pytest.fixture(autouse=True)
def rate_limit_delay():
    """每条用例后延时，避免接口限频。"""
    yield
    delay_str = os.getenv("API_RATE_LIMIT_SECONDS", "2")
    try:
        delay_seconds = float(delay_str)
    except ValueError:
        delay_seconds = 2.0
        logger.warning("API_RATE_LIMIT_SECONDS 非法，回退到默认 2 秒: %s", delay_str)
    if delay_seconds > 0:
        time.sleep(delay_seconds)


def pytest_addoption(parser):
    parser.addoption("--tapd-plan", action="store", help="指定 TAPD 测试计划 ID（覆盖配置）")
    parser.addoption("--no-tapd-report", action="store_true", help="禁用 TAPD 自动回填")


@pytest.fixture(scope="session", autouse=True)
def configure_tapd_plan(request):
    if request.config.getoption("--no-tapd-report"):
        TAPD_CONFIG["enabled"] = False
        logger.info("TAPD 自动回填已禁用")
        return

    plan_id = request.config.getoption("--tapd-plan")
    if plan_id:
        TAPD_CONFIG.setdefault("current_test_plan", {})["id"] = plan_id
        logger.info("使用命令行指定 TAPD 测试计划: %s", plan_id)

    if TAPD_CONFIG.get("enabled"):
        plan_info = TAPD_CONFIG.get("current_test_plan", {})
        logger.info("TAPD 回填目标: id=%s name=%s", plan_info.get("id"), plan_info.get("name", ""))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report_case_result(item, report, TAPD_CONFIG)


def pytest_sessionstart(session):
    WECOM_RESULTS.start()


def pytest_runtest_logreport(report):
    WECOM_RESULTS.record(report)


def pytest_sessionfinish(session, exitstatus):
    WECOM_RESULTS.send(TAPD_CONFIG)

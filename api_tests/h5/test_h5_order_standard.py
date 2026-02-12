"""
H5 端标准订单（下单→查单→退款）参数化用例。

覆盖 8 种商品类型，每种商品类型对应一条 TAPD 用例 ID。
复杂 itemList 结构的商品（实物商品、课外服务、线下课）保留独立用例文件。
"""
import pytest
from actions.order_actions import OrderActions
from actions.refund_actions import RefundActions
from test_data_manager import TestDataManager


# (service_key, TAPD 用例 ID, 中文描述)
_H5_ORDER_CASES = [
    ("audio",         "1150695810001062378", "音频"),
    ("video",         "1150695810001062379", "视频"),
    ("news",          "1150695810001062377", "图文"),
    ("column",        "1150695810001062376", "系列课"),
    ("ebook",         "1150695810001062380", "电子书"),
    ("checkpoint",    "1150695810001062386", "关卡"),
    ("evaluation",    "1150695810001062384", "测评"),
    ("question_bank", "1150695810001062385", "题库"),
]


@pytest.mark.parametrize(
    "service_key, tapd_id, label",
    _H5_ORDER_CASES,
    ids=[c[0] for c in _H5_ORDER_CASES],
)
def test_h5_order_and_refund(h5_client, admin_client, service_key, tapd_id, label):
    """
    H5端{label}订单 - 下单→查单→退款完整流程
    用例 ID: {tapd_id}
    接口: POST /api/guestAuth/order/v2/commitOrder
    """
    # Arrange
    test_data = TestDataManager.get_service_data(service_key, "h5")

    # Act: 下单
    order_no = OrderActions.commit_h5_order(
        h5_client,
        service_type=test_data["service_type"],
        service_id=test_data["service_id"],
        amount=test_data["amount"],
    )

    # Act: 查单
    order_detail = OrderActions.get_order_detail(admin_client, order_no)

    # Act: 退款
    RefundActions.refund_order(
        admin_client,
        order_no=order_no,
        order_item_id=order_detail["order_item_id"],
        stu_id=str(h5_client.stu_id),
        amount=test_data["amount"],
    )

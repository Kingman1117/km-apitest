"""
用例 ID: 1150695810001062408
用例名称: EduPC端正常访问系列课，提交系列课订单并管理后台退款
接口: POST /api/guestAuth/pcOrder/v2/commitOrder

流程：
1. EduPC端提交系列课订单
2. 管理后台查询订单详情
3. 管理后台退款
"""
from actions.order_actions import OrderActions
from actions.refund_actions import RefundActions
from test_data_manager import TestDataManager


def test_edupc_order_column_and_refund(edupc_client, admin_client):
    """EduPC端系列课订单 - 下单→查单→退款完整流程"""

    # Arrange: 获取测试数据
    test_data = TestDataManager.get_service_data("column", "edupc")

    # Act: EduPC端提交订单
    order_no = OrderActions.commit_edupc_order(
        edupc_client,
        service_type=test_data["service_type"],
        service_id=test_data["service_id"],
        amount=test_data["amount"]
    )

    # Act: 管理后台查询订单详情
    order_detail = OrderActions.get_order_detail(admin_client, order_no)

    # Act: 管理后台退款
    RefundActions.refund_order(
        admin_client,
        order_no=order_no,
        order_item_id=order_detail["order_item_id"],
        stu_id=str(edupc_client.stu_id),
        amount=test_data["amount"]
    )

    # Assert: 各步骤成功断言与关键字段校验在 OrderActions 中统一完成

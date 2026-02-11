"""
用例 ID: 1150695810001062383
用例名称: H5端正常提交实物商品订单并管理后台退款
接口: POST /api/guestAuth/order/v2/commitOrder

流程：
1. H5端提交实物商品订单
2. 管理后台查询订单详情
3. 管理后台退款
"""
import json
import logging
from actions.order_actions import OrderActions
from actions.refund_actions import RefundActions
from data_factory import DataFactory
from test_data_manager import TestDataManager


logger = logging.getLogger(__name__)


def test_h5_order_product_and_refund(h5_client, admin_client):
    """H5端实物商品订单 - 下单→查单→退款完整流程（复杂itemList）"""

    # Arrange: 获取测试数据
    stu_id = DataFactory.resolve_stu_id(h5_client.stu_id)
    union_user_id = DataFactory.resolve_union_user_id(h5_client.union_user_id)
    item_list = TestDataManager.get_order_item_template("h5_product")
    item_list[0]["stuId"] = int(stu_id)

    # Act: H5端提交实物商品订单（特殊itemList结构）
    order_result = h5_client.post(
        "/api/guestAuth/order/v2/commitOrder",
        data={
            "aid": h5_client.aid,
            "wxappId": h5_client.wxapp_id,
            "wxappAid": h5_client.wxapp_aid,
            "isOem": "false",
            "from": "3",
            "isModel": "false",
            "unionUserId": union_user_id,
            "TOKEN": h5_client._token,
            "edu_aid": h5_client.edu_aid,
            "stuId": stu_id,
            "wxappAppId": "wx88cf35a9fa55948a",
            "amount": "1000",
            "giftAmount": "0",
            "payType": "5",
            "payPrice": "0",
            "itemList": json.dumps(item_list, ensure_ascii=False),
            "integralMall": "false",
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    
    h5_client.assert_success(order_result, "提交实物商品订单失败")
    order_no = order_result.get("data", {}).get("orderNo")
    assert order_no, f"订单号为空: {order_result}"
    logger.info("H5 实物商品订单提交成功: orderNo=%s", order_no)
    
    # Act: 管理后台查询订单详情
    order_detail = OrderActions.get_order_detail(admin_client, order_no)
    order_item_id = order_detail["order_item_id"]

    # Act: 管理后台退款
    RefundActions.refund_order(
        admin_client,
        order_no=order_no,
        order_item_id=order_item_id,
        stu_id=stu_id,
        amount=1000
    )

    # Assert: 下单与退款关键断言已在 client/actions 层完成

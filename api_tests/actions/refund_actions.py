"""
退款相关业务动作
"""
import logging
from data_factory import DataFactory


logger = logging.getLogger(__name__)


class RefundActions:
    """退款业务动作"""

    @staticmethod
    def refund_order(admin_client, order_no: str, order_item_id: str, stu_id: str, amount: int):
        """
        管理后台退款
        
        Args:
            admin_client: 管理后台客户端
            order_no: 订单号
            order_item_id: 订单项ID
            stu_id: 学员ID
            amount: 退款金额（分）
        """
        result = admin_client.post(
            "/api/manage/refund/refundOrder",
            data=DataFactory.build_refund_data(
                order_no=order_no,
                order_item_id=order_item_id,
                stu_id=stu_id,
                amount=amount,
            ),
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
            },
        )
        
        # 验证退款成功
        admin_client.assert_success(result, f"退款失败: orderNo={order_no}")
        
        logger.info("退款成功: order_no=%s, amount=%s", order_no, amount)

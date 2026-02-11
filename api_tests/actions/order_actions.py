"""
订单相关业务动作

封装订单提交、查询、退款等可复用业务动作
"""
import logging
from typing import Dict, Any

from data_factory import DataFactory


logger = logging.getLogger(__name__)


class OrderActions:
    """订单业务动作"""
    
    @staticmethod
    def commit_edupc_order(edupc_client, service_type: int, service_id: int, amount: int) -> str:
        """
        EduPC端提交订单
        
        Args:
            edupc_client: EduPC客户端
            service_type: 服务类型（5=系列课, 6=图文, 7=视频, 8=音频等）
            service_id: 服务ID
            amount: 订单金额（分）
            
        Returns:
            order_no: 订单号
        """
        result = edupc_client.post(
            "/api/guestAuth/pcOrder/v2/commitOrder",
            data=DataFactory.build_edupc_commit_order_data(
                edupc_client=edupc_client,
                service_type=service_type,
                service_id=service_id,
                amount=amount,
            ),
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
            },
        )
        
        # 验证订单提交成功
        edupc_client.assert_success(result, "EduPC订单提交失败")
        
        # 提取订单号
        order_no = result.get("data", {}).get("orderNo")
        assert order_no, f"订单号为空: {result}"
        
        logger.info(
            "EduPC订单提交成功: order_no=%s, service_id=%s, amount=%s",
            order_no,
            service_id,
            amount,
        )
        return order_no
    
    @staticmethod
    def commit_h5_order(h5_client, service_type: int, service_id: int, amount: int) -> str:
        """
        H5端提交订单
        
        Args:
            h5_client: H5客户端
            service_type: 服务类型
            service_id: 服务ID
            amount: 订单金额（分）
            
        Returns:
            order_no: 订单号
        """
        result = h5_client.post(
            "/api/guestAuth/order/v2/commitOrder",
            data=DataFactory.build_h5_commit_order_data(
                h5_client=h5_client,
                service_type=service_type,
                service_id=service_id,
                amount=amount,
            ),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        
        # 验证订单提交成功
        h5_client.assert_success(result, "H5订单提交失败")
        
        # 提取订单号
        order_no = result.get("data", {}).get("orderNo")
        assert order_no, f"订单号为空: {result}"
        
        logger.info(
            "H5订单提交成功: order_no=%s, service_id=%s, amount=%s",
            order_no,
            service_id,
            amount,
        )
        return order_no
    
    @staticmethod
    def get_order_detail(admin_client, order_no: str) -> Dict[str, Any]:
        """
        管理后台查询订单详情
        
        Args:
            admin_client: 管理后台客户端
            order_no: 订单号
            
        Returns:
            订单详情字典，包含：
            - order_info: 订单信息
            - order_item_id: 第一个订单项ID（用于退款）
        """
        result = admin_client.get(
            "/api/manage/order/v2/getOrderDetails",
            params={"orderNo": order_no},
        )
        
        # 验证查询成功
        admin_client.assert_success(result, f"查询订单详情失败: orderNo={order_no}")
        
        # 提取订单信息
        detail_data = result.get("data", {})
        order_info = detail_data.get("orderInfo", {})
        order_items = order_info.get("itemList", [])
        
        # 如果orderInfo下没有，尝试从顶层获取
        if not order_items:
            order_items = detail_data.get("itemList", []) or detail_data.get("orderItems", [])
        
        assert len(order_items) > 0, f"订单详情中无商品明细: {result}"
        
        # 提取orderItemId
        order_item_id = order_items[0].get("orderItemId") or order_items[0].get("id")
        assert order_item_id, f"订单明细ID为空: {result}"
        
        logger.info("订单详情查询成功: order_no=%s, order_item_id=%s", order_no, order_item_id)
        
        return {
            "order_info": order_info,
            "order_item_id": order_item_id,
            "order_items": order_items,
        }
    
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

"""
测试数据工厂（轻量版）。

目标：
- 收敛默认值来源，避免业务代码里散落魔法值
- 统一订单与退款入参构造，减少重复
"""
import json
from typing import Any, Dict, Optional

from test_data_manager import TestDataManager


class DataFactory:
    """构建常用业务请求数据。"""

    @staticmethod
    def resolve_stu_id(client_stu_id: Optional[Any]) -> str:
        """优先使用登录态中的 stu_id，不存在时回退到配置默认值。"""
        if client_stu_id:
            return str(client_stu_id)
        return str(TestDataManager.get_default("stu_id", "57711"))

    @staticmethod
    def resolve_union_user_id(client_union_user_id: Optional[Any]) -> str:
        """优先使用登录态中的 union_user_id，不存在时回退到配置默认值。"""
        if client_union_user_id:
            return str(client_union_user_id)
        return str(TestDataManager.get_default("union_user_id", "57655"))

    @classmethod
    def build_edupc_commit_order_data(
        cls,
        edupc_client,
        service_type: int,
        service_id: int,
        amount: int,
    ) -> Dict[str, Any]:
        stu_id = cls.resolve_stu_id(edupc_client.stu_id)
        union_user_id = cls.resolve_union_user_id(edupc_client.union_user_id)
        return {
            "aid": edupc_client.aid,
            "wxappAid": edupc_client.wxapp_aid,
            "wxappId": edupc_client.wxapp_id,
            "isOem": "false",
            "from": "4",
            "payType": "5",
            "unionUserId": union_user_id,
            "openId": "",
            "payPrice": "0",
            "amount": str(amount),
            "giftAmount": "0",
            "itemList": (
                f'[{{"payPrice":{amount},"serviceType":{service_type},'
                f'"serviceId":{service_id},"stuId":{stu_id}}}]'
            ),
        }

    @classmethod
    def build_h5_commit_order_data(
        cls,
        h5_client,
        service_type: int,
        service_id: int,
        amount: int,
    ) -> Dict[str, Any]:
        stu_id = cls.resolve_stu_id(h5_client.stu_id)
        union_user_id = cls.resolve_union_user_id(h5_client.union_user_id)
        return {
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
            "payPrice": "0",
            "amount": str(amount),
            "giftAmount": "0",
            "payType": "5",
            "itemList": (
                f'[{{"payPrice":0,"serviceType":{service_type},"serviceId":{service_id},'
                f'"quantity":1,"stuId":{stu_id}}}]'
            ),
            "integralMall": "false",
        }

    @staticmethod
    def build_refund_data(order_no: str, order_item_id: str, stu_id: str, amount: int) -> Dict[str, Any]:
        refund_list = [
            {
                "num": 1,
                "orderNo": order_no,
                "orderItemId": order_item_id,
                "refundPrice": 0,
                "amount": amount,
                "giftAmount": 0,
            }
        ]
        return {
            "reason": "自动化测试退款",
            "refundList": json.dumps(refund_list, ensure_ascii=False),
            "refundType": "1",
            "stuId": stu_id,
            "unionUserId": "0",
            "refundMethod": "1",
        }

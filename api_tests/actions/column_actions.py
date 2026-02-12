"""
系列课相关业务动作
"""
import json
import logging

from content_settings_loader import ContentSettingsLoader
from utils.date_utils import future_date


logger = logging.getLogger(__name__)


class ColumnActions:
    """系列课业务动作"""

    @staticmethod
    def create_column(admin_client, name: str, summary: str = "", **extra_data) -> str:
        """
        创建系列课
        
        Args:
            admin_client: 管理后台客户端
            name: 系列课名称
            summary: 摘要
            **extra_data: 额外参数
            
        Returns:
            column_id: 系列课ID
        """
        validity_date = future_date()
        setting = ContentSettingsLoader.get_column_setting(validity_date)
        
        data = {
            "wxappId": admin_client.wxapp_id,
            "name": name,
            "summary": summary,
            "picIdList": '["AJQBCAAQAhgAIKWqgMwGKObW7pcGMLgIOLgI"]',
            "payModel": "1",
            "price": "0.01",
            "status": "0",
            "introduce": "",
            "setting": json.dumps(setting, ensure_ascii=False),
            "isBigColumn": "false",
            "openPresent": "false",
            "classifyIdList": "[]",
            "courseType": "0",
            "startType": "0",
            "fixedStartTime": "",
            "isSignUpEndTime": "false",
            "signUpEndTime": "",
            "isCusAgreement": "false",
            "isOpenAgreement": "false",
            "agreementId": "0",
            "agreementName": "",
            **extra_data,
        }
        result = admin_client.post(
            "/ajax/wxAppColumn_h.jsp",
            params={"cmd": "addColumn"},
            data=data,
            schema="admin.content.column.create",
        )
        admin_client.assert_success(result, "创建系列课失败")
        column_id = admin_client.extract_id(result, id_field="id", data_path=None)
        logger.info("系列课创建成功: id=%s name=%s", column_id, name)
        return column_id

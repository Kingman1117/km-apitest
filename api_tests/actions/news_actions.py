"""
图文相关业务动作
"""
import json
import logging
import time
from content_settings_loader import ContentSettingsLoader


logger = logging.getLogger(__name__)


class NewsActions:
    """图文业务动作"""

    @staticmethod
    def create_news(admin_client, name: str, summary: str = "", **extra_data) -> str:
        """
        创建图文内容
        
        Args:
            admin_client: 管理后台客户端
            name: 图文标题
            summary: 摘要
            **extra_data: 额外参数
            
        Returns:
            news_id: 图文ID
        """
        setting = ContentSettingsLoader.get_news_setting()
        
        data = {
            "title": name,
            "autoSummary": "true",
            "summary": summary,
            "views": "0",
            "content": "<p>自动化接口测试图文内容</p>",
            "picId": "",
            "publicTime": time.strftime("%Y-%m-%d %H:%M"),
            "top": "false",
            "isCusPic": "false",
            "tdk": '{"t":"","d":"","k":""}',
            "setting": json.dumps(setting, ensure_ascii=False),
            "homeworkId": "0",
            "isRelevancyColumn": "false",
            "classifyIdList": "[]",
            "isCusAgreement": "false",
            "isOpenAgreement": "false",
            "agreementId": "0",
            "agreementName": "",
            **extra_data,
        }
        result = admin_client.post("/ajax/wxAppNews_h.jsp", params={"cmd": "addNews"}, data=data)
        admin_client.assert_success(result, "创建图文失败")
        news_id = admin_client.extract_id(result, id_field="id", data_path="data")
        logger.info("图文创建成功: id=%s name=%s", news_id, name)
        return news_id

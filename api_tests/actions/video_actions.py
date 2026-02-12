"""
视频相关业务动作
"""
import json
import logging

from content_settings_loader import ContentSettingsLoader
from utils.date_utils import future_date


logger = logging.getLogger(__name__)


class VideoActions:
    """视频业务动作"""

    @staticmethod
    def create_video(admin_client, name: str, file_id: str, summary: str = "", **extra_data) -> str:
        """
        创建视频课程
        
        Args:
            admin_client: 管理后台客户端
            name: 视频名称
            file_id: 视频文件ID
            summary: 摘要
            **extra_data: 额外参数
            
        Returns:
            video_id: 视频ID
        """
        validity_date = future_date()
        setting = ContentSettingsLoader.get_video_setting(validity_date)
        
        data = {
            "wxappId": admin_client.wxapp_id,
            "id": "0",
            "name": name,
            "summary": summary,
            "type": "0",
            "vid": "",
            "file": file_id,
            "postFile": "",
            "classifyIdList": "[]",
            "content": "",
            "offSale": "false",
            "setting": json.dumps(setting, ensure_ascii=False),
            "subscriptionsNum": "0",
            "homeworkId": "0",
            "columnItemId": "0",
            "isRelevancyColumn": "false",
            "relevancyColumnId": "0",
            "coverType": "2",
            "isCusAgreement": "false",
            "isOpenAgreement": "false",
            "agreementId": "0",
            "agreementName": "",
            **extra_data,
        }
        result = admin_client.post(
            "/ajax/video_h.jsp",
            params={"cmd": "addVideo"},
            data=data,
            schema="admin.content.video.create",
        )
        admin_client.assert_success(result, "创建视频失败")
        video_id = admin_client.extract_id(result, id_field="id", data_path="video")
        logger.info("视频创建成功: id=%s name=%s", video_id, name)
        return video_id

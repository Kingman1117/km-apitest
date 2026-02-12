"""
音频相关业务动作
"""
import json
import logging

from content_settings_loader import ContentSettingsLoader
from utils.date_utils import future_date


logger = logging.getLogger(__name__)


class AudioActions:
    """音频业务动作"""

    @staticmethod
    def create_audio(admin_client, name: str, file_id: str, summary: str = "", **extra_data) -> str:
        """
        创建音频课程
        
        Args:
            admin_client: 管理后台客户端
            name: 音频名称
            file_id: 音频文件ID
            summary: 摘要
            **extra_data: 额外参数
            
        Returns:
            audio_id: 音频ID
        """
        validity_date = future_date()
        setting = ContentSettingsLoader.get_audio_setting(validity_date)
        
        data = {
            "wxappId": admin_client.wxapp_id,
            "name": name,
            "summary": summary,
            "content": "",
            "fileId": file_id,
            "picIdList": "[]",
            "classifyIdList": "[]",
            "tdk": '{"t":"","d":"","k":""}',
            "setting": json.dumps(setting, ensure_ascii=False),
            "subscriptionsNum": "0",
            "homeworkId": "0",
            "columnItemId": "0",
            "isRelevancyColumn": "false",
            "relevancyColumnId": "0",
            "coverType": "0",
            "isCusAgreement": "false",
            "isOpenAgreement": "false",
            "agreementId": "0",
            "agreementName": "",
            **extra_data,
        }
        result = admin_client.post(
            "/ajax/wxAppAudio_h.jsp",
            params={"cmd": "add"},
            data=data,
            schema="admin.content.audio.create",
        )
        admin_client.assert_success(result, "创建音频失败")
        audio_id = admin_client.extract_id(result, id_field="id", data_path=None)
        logger.info("音频创建成功: id=%s name=%s", audio_id, name)
        return audio_id

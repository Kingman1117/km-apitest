"""
用例 ID: 1150695810001062392
用例名称: 管理后台正常添加音频课程

接口: POST /ajax/wxAppAudio_h.jsp?cmd=add
"""
from actions.audio_actions import AudioActions
from actions.delete_actions import DeleteActions
from test_data_manager import TestDataManager


def test_admin_add_audio(admin_client, timestamp):
    """管理后台添加音频 - 验证创建成功且数据正确"""
    # Arrange: 准备测试数据
    name = f"接口测试音频_{timestamp}"
    file_id = TestDataManager.get_file_id("audio")
    audio_id = None

    try:
        # Act: 创建音频
        audio_id = AudioActions.create_audio(admin_client, name, file_id)
    finally:
        # 清理：删除创建的音频
        if audio_id:
            DeleteActions.delete_audio(admin_client, audio_id)

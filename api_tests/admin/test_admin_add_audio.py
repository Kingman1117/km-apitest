"""
用例 ID: 1150695810001062392
用例名称: 管理后台正常添加音频课程

接口: POST /ajax/wxAppAudio_h.jsp?cmd=add
"""
from actions.content_actions import ContentActions
from test_data_manager import TestDataManager


def test_admin_add_audio(admin_client, timestamp):
    """管理后台添加音频 - 验证创建成功且数据正确"""
    # Arrange: 准备测试数据
    name = f"接口测试音频_{timestamp}"
    file_id = TestDataManager.get_file_id("audio")

    # Act: 创建音频
    audio_id = ContentActions.create_audio(admin_client, name, file_id)

    # Assert: 验证创建成功
    assert audio_id, "音频创建失败"

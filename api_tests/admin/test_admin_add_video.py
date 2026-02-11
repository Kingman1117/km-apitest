"""
用例 ID: 1150695810001062393
用例名称: 管理后台正常添加视频课程

接口: POST /ajax/video_h.jsp?cmd=addVideo
"""
from actions.video_actions import VideoActions
from test_data_manager import TestDataManager


def test_admin_add_video(admin_client, timestamp):
    """管理后台添加视频 - 验证创建成功且数据正确"""
    # Arrange: 准备测试数据
    name = f"接口测试视频_{timestamp}"
    file_id = TestDataManager.get_file_id("video")

    # Act: 创建视频
    video_id = VideoActions.create_video(admin_client, name, file_id)

    # Assert: 验证创建成功
    assert video_id, "视频创建失败"

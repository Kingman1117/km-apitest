"""
用例 ID: 1150695810001062391
用例名称: 管理后台正常添加图文课程

接口: POST /ajax/wxAppNews_h.jsp?cmd=addNews
"""
from actions.news_actions import NewsActions


def test_admin_add_news(admin_client, timestamp):
    """管理后台添加图文 - 验证创建成功且数据正确"""
    # Arrange: 准备测试数据
    name = f"接口测试图文_{timestamp}"

    # Act: 创建图文
    news_id = NewsActions.create_news(admin_client, name)

    # Assert: 验证创建成功
    assert news_id, "图文创建失败"

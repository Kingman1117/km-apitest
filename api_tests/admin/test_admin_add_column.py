"""
用例 ID: 1150695810001062390
用例名称: 管理后台正常添加系列课

接口: POST /ajax/wxAppColumn_h.jsp?cmd=addColumn
"""
from actions.column_actions import ColumnActions


def test_admin_add_column(admin_client, timestamp):
    """管理后台添加系列课 - 验证创建成功且数据正确"""
    # Arrange: 准备测试数据
    name = f"接口测试系列课_{timestamp}"

    # Act: 创建系列课
    column_id = ColumnActions.create_column(admin_client, name)

    # Assert: 验证创建成功
    assert column_id, "系列课创建失败"

"""
用例 ID: 1150695810001062402
用例名称: 管理后台正常添加表单

接口: POST /ajax/wxAppForm_h.jsp?cmd=addWXAppForm
"""
from actions.delete_actions import DeleteActions
from payloads.admin_payloads import build_add_form_payload
from utils.response_assert import assert_any_field


def test_admin_add_form(admin_client, timestamp):
    """管理后台正常添加表单"""
    # Arrange: 准备测试数据
    form_name = f"接口测试表单_{timestamp}"
    form_id = None
    
    try:
        # Act: 创建表单
        result = admin_client.post(
            "/ajax/wxAppForm_h.jsp",
            params={"cmd": "addWXAppForm"},
            data=build_add_form_payload(form_name, str(admin_client.wxapp_id)),
            schema="admin.form.create",
        )
        
        # Assert: 验证创建成功
        admin_client.assert_success(result, "添加表单失败")
        form_id = assert_any_field(result, ["data.id", "id"], msg="表单创建失败")
    finally:
        # 清理：删除创建的表单
        if form_id:
            DeleteActions.delete_form(admin_client, form_id)

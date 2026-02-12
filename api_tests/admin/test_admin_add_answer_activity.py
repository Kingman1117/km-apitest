"""
用例 ID: 1150695810001062398
用例名称: 管理后台正常添加答题活动

接口: POST /ajax/wxAppAnswer_h.jsp?cmd=addAnswerActivity
"""
from payloads.admin_payloads import build_add_answer_activity_payload
from utils.response_assert import assert_any_field


def test_admin_add_answer_activity(admin_client, timestamp):
    """管理后台正常添加答题活动"""
    # Arrange: 准备测试数据
    activity_name = f"接口测试答题_{timestamp}"
    
    # Act: 创建答题活动（questionList 使用简化版）
    result = admin_client.post(
        "/ajax/wxAppAnswer_h.jsp",
        params={"cmd": "addAnswerActivity"},
        data=build_add_answer_activity_payload(activity_name, str(admin_client.wxapp_id)),
        schema="admin.answer_activity.create",
    )
    
    # Assert: 验证创建成功
    admin_client.assert_success(result, "添加答题活动失败")
    assert_any_field(result, ["data.id", "id"], msg="答题活动创建失败")

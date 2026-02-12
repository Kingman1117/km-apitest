"""
用例 ID: 1150695810001062389
用例名称: 管理后台正常创建线下课程

接口: POST /ajax/eduCourse_h.jsp?cmd=addCourse
"""
from actions.delete_actions import DeleteActions
from payloads.admin_payloads import build_add_offline_course_payload
from utils.response_assert import assert_any_field


def test_admin_add_offline_course(admin_client, timestamp):
    """管理后台创建线下课程 - 验证创建成功"""
    # Arrange: 准备测试数据
    course_name = f"接口测试线下课_{timestamp}"
    course_id = None

    try:
        # Act: 创建线下课程
        result = admin_client.post(
            "/ajax/eduCourse_h.jsp",
            params={"cmd": "addCourse"},
            data=build_add_offline_course_payload(course_name, str(admin_client.wxapp_id)),
            schema="admin.offline_course.create",
        )

        # Assert: 验证创建成功
        admin_client.assert_success(result, "创建线下课程失败")
        course_id = assert_any_field(result, ["data.id", "id"], msg="线下课程创建失败")
    finally:
        # 清理：删除创建的线下课程
        if course_id:
            DeleteActions.delete_offline_course(admin_client, course_id)

"""
用例 ID: 1150695810001062397
用例名称: 管理后台正常添加超级题库

接口: POST /api/manage/superQuestionBank/addSuperQuestionBank
"""
from actions.delete_actions import DeleteActions
from payloads.admin_payloads import build_add_question_bank_payload
from utils.response_assert import assert_any_field


def test_admin_add_question_bank(admin_client, timestamp):
    """管理后台正常添加超级题库"""
    # Arrange: 准备测试数据
    bank_name = f"接口测试题库_{timestamp}"
    bank_id = None

    try:
        # Act: 创建超级题库
        result = admin_client.post(
            "/api/manage/superQuestionBank/addSuperQuestionBank",
            params={},  # _TOKEN 会自动添加
            data=build_add_question_bank_payload(bank_name),
            schema="admin.question_bank.create",
        )
        
        # Assert: 验证创建成功
        admin_client.assert_success(result, "添加超级题库失败")
        bank_id = assert_any_field(result, ["data.id", "id"], msg="超级题库创建失败")
    finally:
        # 清理：删除创建的题库
        if bank_id:
            DeleteActions.delete_question_bank(admin_client, bank_id)

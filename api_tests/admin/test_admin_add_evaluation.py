"""
用例 ID: 1150695810001062401
用例名称: 管理后台正常添加测评活动

接口: POST /api/manage/evaluation/addEvaluation
注意：测评活动比较特殊，暂不清理测试数据
"""
from payloads.admin_payloads import build_add_evaluation_payload


def test_admin_add_evaluation(admin_client, timestamp):
    """管理后台正常添加测评活动"""
    # Arrange: 准备测试数据
    evaluation_name = f"接口测试测评_{timestamp}"

    # Act: 创建测评活动
    result = admin_client.post(
        "/api/manage/evaluation/addEvaluation",
        params={},  # _TOKEN 会自动添加
        data=build_add_evaluation_payload(evaluation_name),
        schema="admin.evaluation.create",
    )
    
    # Assert: 验证创建成功
    admin_client.assert_success(result, "添加测评活动失败")

"""
用例 ID: 1150695810001062397
用例名称: 管理后台正常添加超级题库

接口: POST /api/manage/superQuestionBank/addSuperQuestionBank
"""
from actions.delete_actions import DeleteActions


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
            data={
                "id": "0",
                "name": bank_name,
                "summary": "",
                "pic": "",
                "picUrl": "",
                "classifyIdList": "[]",
                "classifyList": "[]",
                "introduce": "",
                "payType": "3",
                "price": "0.01",
                "setting": '{"bp":0,"bml":1,"btype":0,"bmtgs":[],"memoryMode":1,"menuTypes":[1,2,3,4,5],"pfk":{"lp":0.01,"slp":0,"duration":0,"validityType":0,"asp":0,"sst":0,"vsu":0,"bpam":1}}',
                "isCusAgreement": "false",
                "isOpenAgreement": "false",
                "agreementId": "0",
                "agreementName": "",
                "globalAgreement": '{"open":false,"id":0,"name":""}',
            },
        )
        
        # Assert: 验证创建成功
        admin_client.assert_success(result, "添加超级题库失败")
        bank_id = result.get("data", {}).get("id") or result.get("id")
        assert bank_id, "超级题库创建失败"
    finally:
        # 清理：删除创建的题库
        if bank_id:
            DeleteActions.delete_question_bank(admin_client, bank_id)

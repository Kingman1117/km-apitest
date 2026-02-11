"""
用例 ID: 1150695810001062401
用例名称: 管理后台正常添加测评活动

接口: POST /api/manage/evaluation/addEvaluation
"""


def test_admin_add_evaluation(admin_client, timestamp):
    """管理后台正常添加测评活动"""
    # Arrange: 准备测试数据
    evaluation_name = f"接口测试测评_{timestamp}"

    # Act: 创建测评活动
    result = admin_client.post(
        "/api/manage/evaluation/addEvaluation",
        params={},  # _TOKEN 会自动添加
        data={
            "name": evaluation_name,
            "pic": "",
            "picUrl": "",
            "summary": "",
            "payType": "3",
            "payOpportunity": "0",
            "price": "0.01",
            "introduce": "",
            "classifyIdList": "[]",
            "setting": '{"bp":0,"btype":0,"bmtgs":[],"bml":1,"pfk":{"asp":0,"duration":0,"validityType":0,"validityDate":"","otc":0,"stct":1,"lp":0.01,"slp":0},"joinType":0,"joinNum":1,"resultType":0,"resultNum":1,"dimensionType":0,"evaluationType":0,"chartType":0,"showScore":1,"showChart":0,"wxType":0,"wxDesc":"","wxList":[{"open":0,"qrCode":"","text":"","qrCodeUrl":""},{"open":0,"qrCode":"","text":"","qrCodeUrl":""}]}',
            "questionSort": "[-10000001]",
            "isCusAgreement": "false",
            "isOpenAgreement": "false",
            "agreementId": "0",
            "agreementName": "",
            "globalAgreement": '{"open":false,"id":0,"name":""}',
            "addDimensionList": "[]",
            "addQuestionList": '[{"id":-10000001,"stem":"111","type":0,"optionContent":{"options":[{"id":1,"value":"22","score":1},{"id":2,"value":"33","score":1}]}}]',
            "addResultList": '[{"id":-1,"name":"其他结果","section":[],"result":"无法评估，请重新测试","analysis":"","recommend":[],"isOtherResult":true,"setting":{"rulesType":0,"cl":[],"so":0,"sofs":[1],"sd":1,"sdfs":[1],"sda":1}}]',
            "addDimensionGroupList": "[]",
            "addOverallIndicatorList": '[{"id":-9999,"name":"测评总分","isSys":true,"formula":"#测评总分#","isTotalScore":true,"degree":{"dl":[]}},{"id":-10000,"name":"测评平均分","isSys":true,"formula":"#测评平均分#","isAverageScore":true,"degree":{"dl":[]}}]',
            "addDimensionIndicatorList": '[{"id":-1,"name":"平均分","degree":{"dl":[]},"dimensionDegreeList":[]}]',
        },
    )
    
    # Assert: 验证创建成功
    admin_client.assert_success(result, "添加测评活动失败")

"""
用例 ID: 1150695810001062398
用例名称: 管理后台正常添加答题活动

接口: POST /ajax/wxAppAnswer_h.jsp?cmd=addAnswerActivity
"""


def test_admin_add_answer_activity(admin_client, timestamp):
    """管理后台正常添加答题活动"""
    # Arrange: 准备测试数据
    activity_name = f"接口测试答题_{timestamp}"
    
    # Act: 创建答题活动（questionList 使用简化版）
    result = admin_client.post(
        "/ajax/wxAppAnswer_h.jsp",
        params={"cmd": "addAnswerActivity"},
        data={
            "isRelevancyColumn": "false",
            "relevancyColumnId": "0",
            "wxappId": admin_client.wxapp_id,
            "isUnLimitTime": "true",
            "name": activity_name,
            "mode": "0",
            "startTime": "",
            "endTime": "",
            "questionBuildAction": "0",
            "payType": "0",
            "price": "0.01",
            "setting": '{"at":{"t":1,"v":60},"ac":{"t":1,"v":1,"dailyLimitCount":1},"pa":{"t":0,"v":""},"bml":1,"bp":0,"btype":0,"bmtgs":[],"wp":0,"ar":0,"rqna":false,"wqna":false,"qooo":0,"memoryMode":0,"preCheat":{"cutScreenOpen":false,"cutScreenCount":3,"cutScreenTime":3,"screenshotOpen":false,"screenshotCount":2,"banPasteOpen":false,"noOpsSubOpen":false,"noOpsSubTime":120,"entriesLimitOpen":false,"entriesCount":3,"entriesTipsOpen":false,"entriesTxtType":0,"triggerTipsOpen":false,"triggerType":0,"triggerTxtType":0}}',
            "questionOther": '{"st":{"scs":1,"cscs":1,"mcs":1,"cmcs":1,"fibs":1,"cfibs":1,"tofs":1,"ctofs":1,"sas":1,"csas":1,"ls":1,"cls":1},"questionScoreList":[],"customTypeScoreList":[]}',
            "classifyIdList": "[]",
            "isCusAgreement": "false",
            "isOpenAgreement": "false",
            "agreementId": "0",
            "agreementName": "",
            "version": "V2",
            "pic": "",
            "questionList": '[{"id":77615,"stem":"<p style=\\"line-height:1.5em;\\">123</p>","type":0,"content":{"t":-1,"ol":[{"id":1,"v":"<p style=\\"line-height:1.5em;\\">12</p>","r":true,"picUrl":""},{"id":2,"v":"<p style=\\"line-height:1.5em;\\">434</p>","r":false,"picUrl":""}]},"answerAnalysis":"","groupIdList":[0],"createTime":1767777575000,"updateTime":1767777575000,"status":0,"oldId":77615,"examSiteIdList":[],"difficulty":3,"customTypeId":0,"flag":0,"customTypeName":"单选题","snapshot":false,"examSiteInfo":[],"groupInfo":[{"id":0,"name":"默认分类"}],"title":"123","key":"77615"},{"id":77614,"stem":"<p style=\\"line-height:1.5em;\\">11</p>","type":4,"content":{"p":false},"answerAnalysis":"<p style=\\"line-height:1.5em;\\">11</p>","groupIdList":[0],"createTime":1767777567000,"updateTime":1767777567000,"status":0,"oldId":77614,"examSiteIdList":[],"difficulty":3,"customTypeId":4,"flag":0,"customTypeName":"简答题","snapshot":false,"examSiteInfo":[],"groupInfo":[{"id":0,"name":"默认分类"}],"title":"11","key":"77614"}]',
        },
    )
    
    # Assert: 验证创建成功
    admin_client.assert_success(result, "添加答题活动失败")
    activity_id = result.get("data", {}).get("id") or result.get("id")
    assert activity_id, "答题活动创建失败"

"""
用例 ID: 1150695810001062404
用例名称: 管理后台正常添加兑换码

接口: POST /ajax/eduCouponCode_h.jsp?cmd=addWafCk_saveOrUpdateCoupon
注意：兑换码比较特殊，暂不清理测试数据
"""


def test_admin_add_redemption_code(admin_client, timestamp):
    """管理后台正常添加兑换码"""
    # Arrange: 准备测试数据
    code_name = f"接口测试兑换码_{timestamp}"

    # Act: 创建兑换码
    result = admin_client.post(
        "/ajax/eduCouponCode_h.jsp",
        params={"cmd": "addWafCk_saveOrUpdateCoupon"},
        data={
            "name": code_name,
            "channels": "[]",
            "remark": "",
            "universalCode": "",
            "type": "1",
            "codeType": "1",
            "generateType": "0",
            "startTime": "1770181200000",
            "endTime": "1803657599000",
            "stockNum": "1000",
            "useCount": "1",
            "noCountLimit": "true",
            "rightsType": "1",
            "noTimeLimit": "true",
            "couponType": "0",
            "savePrice": "9.99",
            "saveDiscount": "0.1",
            "useStartTime": "",
            "useEndTime": "",
            "ruleTxt": "说说说",
            "pricePageInfo": '{"showPrice":0,"useNotice":""}',
            "isAllCourse": "true",
            "serviceList": "[]",
            "serviceInfo": "{}",
            "status": "0",
        },
    )
    
    # Assert: 验证创建成功
    admin_client.assert_success(result, "添加兑换码失败")

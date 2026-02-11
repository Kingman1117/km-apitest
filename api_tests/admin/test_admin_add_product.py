"""
用例 ID: 1150695810001062396
用例名称: 管理后台正常添加实物商品

接口: POST /ajax/eduProduct_h.jsp?cmd=addProduct
"""


def test_admin_add_product(admin_client, timestamp):
    """管理后台添加实物商品 - 验证创建成功"""
    # Arrange: 准备测试数据
    product_name = f"接口测试实物_{timestamp}"

    # Act: 创建实物商品
    result = admin_client.post(
        "/ajax/eduProduct_h.jsp",
        params={"cmd": "addProduct"},
        data={
            "name": product_name,
            "remark": "",
            "keepProp2": "",
            "hasWeight": "false",
            "imgList": '["AJQBCAAQAhgAIKWqgMwGKObW7pcGMLgIOLgI"]',
            "imgPathList": '["//3444128.s148i.faieduusr.com.faidev.cc/2/110/AJQBCAAQAhgAIKWqgMwGKObW7pcGMLgIOLgI.jpg"]',
            "distributeList": "[0,1]",
            "shippingTmpId": "-1",
            "specList": '[{"name":"尺码","sort":1,"inPdScValList":[{"fi":"","n":"s","path":"","c":true},{"fi":"","n":"m","path":"","c":true},{"fi":"","n":"l","path":"","c":true}]}]',
            "specInfoList": '[{"count":1000,"nameList":["s"],"originPrice":"1500.00","price":"100.00","weight":"0.00","sort":1},{"count":1000,"nameList":["m"],"originPrice":"257.00","price":"17.00","weight":"0.00","sort":2},{"count":2000,"nameList":["l"],"originPrice":"59.00","price":"14.77","weight":"0.00","sort":3}]',
            "setting": '{"bp":0,"bml":1,"btype":0,"bmtgs":[]}',
            "openPresent": "false",
            "productOtherSub": "0",
            "classifyIdList": "[]",
            "addPresentList": "[]",
            "isCusAgreement": "false",
            "isOpenAgreement": "false",
            "agreementId": "0",
            "agreementName": "",
            "independentOrderProp": "false",
            "addPropList": "[]",
            "updatePropList": "[]",
            "delPropIdList": "[]",
        },
    )
    
    # Assert: 验证创建成功
    admin_client.assert_success(result, "添加实物商品失败")
    product_id = result.get("data", {}).get("id") or result.get("id")
    assert product_id, "实物商品创建失败"

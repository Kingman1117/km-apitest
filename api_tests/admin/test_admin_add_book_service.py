"""
用例 ID: 1150695810001062395
用例名称: 管理后台正常添加课外服务

接口: POST /api/manage/book/addBookService
"""
from actions.delete_actions import DeleteActions
from utils.response_assert import assert_field


def test_admin_add_book_service(admin_client, timestamp):
    """管理后台正常添加课外服务"""
    # Arrange: 准备测试数据
    service_name = f"接口测试课外服务_{timestamp}"
    service_id = None

    try:
        # Act: 创建课外服务
        result = admin_client.post(
            "/api/manage/book/addBookService",
            params={},  # _TOKEN 会自动添加到 query params
            data={
                "serviceName": service_name,
                "summary": "",
                "price": "0",
                "promotionPrice": "0",
                "picList": '[{"id":"AJQBCAAQAhgAIKWqgMwGKObW7pcGMLgIOLgI"}]',
                "classifyIdList": "[]",
                "content": "",
                "type": "0",
                "addSpecificationList": "[]",
                "isLimit": "false",
                "addMappingList": "[]",
                "limitCount": "0",
                "setting": '{"bp":0,"bml":1,"btype":0,"bmtgs":[],"pu":{"t":0,"v":""},"pl":{"t":0,"k":0,"v":0,"ti":""},"fdl":{"s":0,"ip":0,"fil":[],"viewType":0},"cs":{"p":"13919161913","po":true,"prov":"广州市","addr":"天河路250号","ao":false,"lat":0,"lng":0,"blat":0,"blng":0,"bts":{"odl":[1,2,3,4,5,6,0],"og":{"t":0,"gd":7},"a":1,"ot":{"t":1,"ut":[0,1,2,3,4,5,6,23],"ti":0,"ut30":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,45,46,47],"ut15":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,89,90,91,92,93,94,95]},"od":{"t":0,"ud":[],"od":[]},"lc":{"c":1,"l":true}},"bto":false},"cso":false,"obsd":0,"oasd":0,"bsdd":{"qrCodeUrl":"","qrCode":"","eg":"添加老师微信，获取更多服务","wt":"微信二维码","wd":"长按二维码添加微信","apuw":false,"ep":0,"bt":"进群"},"asdd":{"qrCodeUrl":"","qrCode":"","eg":"添加班主任安排课程","bt":"扫码","wt":"微信二维码","wd":"长按二维码添加微信","apuw":true},"ss":{"pt":0,"lt":0,"ct":0,"so":[]}}',
                "isCusAgreement": "false",
                "isOpenAgreement": "false",
                "agreementId": "0",
                "agreementName": "",
                "independentOrderProp": "false",
            },
        )
        
        # Assert: 验证创建成功
        admin_client.assert_success(result, "添加课外服务失败")
        service_id = assert_field(result, "data", msg="课外服务创建失败")
    finally:
        # 清理：删除创建的课外服务
        if service_id:
            DeleteActions.delete_book_service(admin_client, service_id)

"""
用例 ID: 1150695810001062389
用例名称: 管理后台正常创建线下课程

接口: POST /ajax/eduCourse_h.jsp?cmd=addCourse
"""
from actions.delete_actions import DeleteActions
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
            data={
                "courseType": "0",
                "courseName": course_name,
                "tollMethod": "0",
                "purchaseLimit": "false",
                "content": "",
                "summary": "",
                "setting": '{"bp":0,"bml":0,"fdl":{"s":0,"ip":0,"fil":[],"viewType":0},"btype":0,"bmtgs":[],"vc":{"cm":0,"dd":"","du":0,"et":0,"vst":"","vet":""},"pageSetting":{"promptValue":3,"promptText":"可在【我的】页面，点击【我的课程】查看已购课程","jumpValue":3,"jumpCustomValue":[2,3],"customerValue":3,"guideText":"如有疑惑，可通过以下方式，与我们联系","openPhone":false,"phone":"","openQrCode":false,"qrCode":"","qrCodeUrl":"","qrText":"添加客服微信，第一时间解决您的疑问","openOfficialCode":false,"officialCode":"","officialCodeUrl":"","officialText":"关注公众号，获取最新课程信息&联系客服"},"obsd":0,"oasd":0,"bsdd":{"qrCodeUrl":"","qrCode":"","eg":"添加老师微信，获取更多服务","wt":"微信二维码","wd":"长按二维码添加微信","apuw":false,"ep":0,"bt":"进群"},"asdd":{"qrCodeUrl":"","qrCode":"","eg":"添加班主任安排课程","wt":"微信二维码","wd":"长按二维码添加微信","apuw":true,"bt":"扫码","ep":0},"independentOrderProp":false}',
                "classifyIdList": "[]",
                "picList": '[{"id":"AJQBCAAQAhgAILqSoMkGKOnJ_o4GMLgIOLgI","url":"//3444128.s148i.faieduusr.com.faidev.cc/2/110/AJQBCAAQAhgAILqSoMkGKOnJ_o4GMLgIOLgI.jpg"}]',
                "addSpecificationList": '[{"name":"100课时","num":100,"price":100,"promotionPrice":50,"total":1000,"type":0,"isEdited":true}]',
                "headerImgList[0][id]": "AJQBCAAQAhgAILqSoMkGKOnJ_o4GMLgIOLgI",
                "headerImgList[0][url]": "//3444128.s148i.faieduusr.com.faidev.cc/2/110/AJQBCAAQAhgAILqSoMkGKOnJ_o4GMLgIOLgI.jpg",
                "pl": '{"k":0,"ln":1}',
                "openPresent": "false",
                "teachCourseIdList": "[]",
                "isCusAgreement": "false",
                "isOpenAgreement": "false",
                "agreementId": "0",
                "agreementName": "",
                "globalAgreement[open]": "false",
                "globalAgreement[id]": "162",
                "globalAgreement[name]": "购课须知",
                "wxappId": admin_client.wxapp_id,
                "independentOrderProp": "false",
            },
        )

        # Assert: 验证创建成功
        admin_client.assert_success(result, "创建线下课程失败")
        course_id = assert_any_field(result, ["data.id", "id"], msg="线下课程创建失败")
    finally:
        # 清理：删除创建的线下课程
        if course_id:
            DeleteActions.delete_offline_course(admin_client, course_id)

"""
用例 ID: 1150695810001062404
用例名称: 管理后台正常添加兑换码

接口: POST /ajax/eduCouponCode_h.jsp?cmd=addWafCk_saveOrUpdateCoupon
注意：兑换码比较特殊，暂不清理测试数据
"""
from payloads.admin_payloads import build_add_redemption_code_payload


def test_admin_add_redemption_code(admin_client, timestamp):
    """管理后台正常添加兑换码"""
    # Arrange: 准备测试数据
    code_name = f"接口测试兑换码_{timestamp}"

    # Act: 创建兑换码
    result = admin_client.post(
        "/ajax/eduCouponCode_h.jsp",
        params={"cmd": "addWafCk_saveOrUpdateCoupon"},
        data=build_add_redemption_code_payload(code_name),
        schema="admin.redemption_code.create",
    )
    
    # Assert: 验证创建成功
    admin_client.assert_success(result, "添加兑换码失败")

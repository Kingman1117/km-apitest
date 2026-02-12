"""
用例 ID: 1150695810001062403
用例名称: 管理后台正常添加优惠券

接口: POST /ajax/coupon_h.jsp?cmd=addCoupon
"""
from actions.delete_actions import DeleteActions
from payloads.admin_payloads import build_add_coupon_payload
from utils.response_assert import assert_any_field


def test_admin_add_coupon(admin_client, timestamp):
    """管理后台正常添加优惠券"""
    # Arrange: 准备测试数据
    # 优惠券名称不能超过10字符（3+6=9）
    coupon_name = f"券{timestamp}"
    coupon_id = None
    
    try:
        # Act: 创建优惠券
        result = admin_client.post(
            "/ajax/coupon_h.jsp",
            params={"cmd": "addCoupon"},
            data=build_add_coupon_payload(coupon_name, str(admin_client.wxapp_id)),
            schema="admin.coupon.create",
        )
        
        # Assert: 验证创建成功
        admin_client.assert_success(result, "添加优惠券失败")
        coupon_id = assert_any_field(result, ["coupon.id", "id"], msg="优惠券创建失败")
    finally:
        # 清理：删除创建的优惠券
        if coupon_id:
            DeleteActions.delete_coupon(admin_client, coupon_id)

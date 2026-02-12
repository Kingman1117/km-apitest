"""
用例 ID: 1150695810001062396
用例名称: 管理后台正常添加实物商品

接口: POST /ajax/eduProduct_h.jsp?cmd=addProduct
"""
from actions.delete_actions import DeleteActions
from payloads.admin_payloads import build_add_product_payload
from utils.response_assert import assert_any_field


def test_admin_add_product(admin_client, timestamp):
    """管理后台添加实物商品 - 验证创建成功"""
    # Arrange: 准备测试数据
    product_name = f"接口测试实物_{timestamp}"
    product_id = None

    try:
        # Act: 创建实物商品
        result = admin_client.post(
            "/ajax/eduProduct_h.jsp",
            params={"cmd": "addProduct"},
            data=build_add_product_payload(product_name),
            schema="admin.product.create",
        )
        
        # Assert: 验证创建成功
        admin_client.assert_success(result, "添加实物商品失败")
        product_id = assert_any_field(result, ["data.id", "id"], msg="实物商品创建失败")
    finally:
        # 清理：删除创建的实物商品
        if product_id:
            DeleteActions.delete_product(admin_client, product_id)

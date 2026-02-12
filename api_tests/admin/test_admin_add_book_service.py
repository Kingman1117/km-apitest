"""
用例 ID: 1150695810001062395
用例名称: 管理后台正常添加课外服务

接口: POST /api/manage/book/addBookService
"""
from actions.delete_actions import DeleteActions
from payloads.admin_payloads import build_add_book_service_payload
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
            data=build_add_book_service_payload(service_name),
            schema="admin.book_service.create",
        )
        
        # Assert: 验证创建成功
        admin_client.assert_success(result, "添加课外服务失败")
        service_id = assert_field(result, "data", msg="课外服务创建失败")
    finally:
        # 清理：删除创建的课外服务
        if service_id:
            DeleteActions.delete_book_service(admin_client, service_id)

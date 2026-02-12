"""
用例 ID: 1150695810001062394
用例名称: 管理后台正常添加电子书

接口: POST /api/manage/electronicBook/addElectronicBook
"""
from actions.delete_actions import DeleteActions
from payloads.admin_payloads import build_add_ebook_payload
from test_data_manager import TestDataManager
from utils.response_assert import assert_any_field


def test_admin_add_ebook(admin_client, timestamp):
    """管理后台添加电子书 - 验证创建成功"""
    # Arrange: 准备测试数据
    ebook_name = f"接口测试电子书_{timestamp}"
    file_id = TestDataManager.get_file_id("ebook")
    ebook_id = None
    
    try:
        # Act: 创建电子书
        result = admin_client.post(
            "/api/manage/electronicBook/addElectronicBook",
            params={},
            data=build_add_ebook_payload(ebook_name, str(file_id)),
            schema="admin.ebook.create",
        )
        
        # Assert: 验证创建成功
        admin_client.assert_success(result, "添加电子书失败")
        ebook_id = assert_any_field(result, ["data.id", "id"], msg="电子书创建失败")
    finally:
        # 清理：删除创建的电子书
        if ebook_id:
            DeleteActions.delete_ebook(admin_client, ebook_id)

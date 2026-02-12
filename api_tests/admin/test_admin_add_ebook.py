"""
用例 ID: 1150695810001062394
用例名称: 管理后台正常添加电子书

接口: POST /api/manage/electronicBook/addElectronicBook
"""
import json
from actions.delete_actions import DeleteActions
from test_data_manager import TestDataManager


def test_admin_add_ebook(admin_client, timestamp):
    """管理后台添加电子书 - 验证创建成功"""
    # Arrange: 准备测试数据
    ebook_name = f"接口测试电子书_{timestamp}"
    file_id = TestDataManager.get_file_id("ebook")
    ebook_id = None
    
    info = {
        "name": ebook_name,
        "pic": "",
        "picUrl": "",
        "author": "",
        "summary": "",
        "fileId": file_id,
        "content": "",
        "setting": {
            "bp": 0,
            "bml": 1,
            "btype": 0,
            "bmtgs": [],
            "ds": 0,
            "pfk": {
                "ss": True,
                "pm": 0,
                "pa": 0.01,
                "duration": 0,
                "asp": 1
            }
        },
        "fileName": "final_optimized_text_version.pdf",
        "fileTypeStr": "pdf",
        "relevancyColumnId": 0,
        "isRelevancyColumn": False,
        "isCusAgreement": False,
        "isOpenAgreement": False,
        "agreementId": 0,
        "agreementName": "",
        "globalAgreement": {
            "open": False,
            "id": 163,
            "name": "购课须知"
        }
    }
    
    try:
        # Act: 创建电子书
        result = admin_client.post(
            "/api/manage/electronicBook/addElectronicBook",
            params={},
            data={
                "info": json.dumps(info, ensure_ascii=False),
                "isCusAgreement": "false",
                "isOpenAgreement": "false",
                "agreementId": "0",
                "agreementName": "",
            },
        )
        
        # Assert: 验证创建成功
        admin_client.assert_success(result, "添加电子书失败")
        ebook_id = result.get("data", {}).get("id") or result.get("id")
        assert ebook_id, "电子书创建失败"
    finally:
        # 清理：删除创建的电子书
        if ebook_id:
            DeleteActions.delete_ebook(admin_client, ebook_id)

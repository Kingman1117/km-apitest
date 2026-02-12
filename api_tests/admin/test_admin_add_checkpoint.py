"""
用例 ID: 1150695810001062400
用例名称: 管理后台正常添加打卡活动

接口: POST /ajax/checkpoint_h.jsp?cmd=addCheckpoint
注意：这个接口和作业是同一个接口，通过其他参数区分（如 auditType、taskList 等）
"""
import json
from actions.delete_actions import DeleteActions
from payloads.admin_payloads import build_default_task_list
from utils.response_assert import assert_any_field


def test_admin_add_checkpoint(admin_client, timestamp):
    """管理后台正常添加打卡活动"""
    # Arrange: 准备测试数据
    checkpoint_name = f"接口测试打卡_{timestamp}"
    checkpoint_id = None
    
    task_list = build_default_task_list()
    
    try:
        # Act: 创建打卡活动
        result = admin_client.post(
            "/ajax/checkpoint_h.jsp",
            params={"cmd": "addCheckpoint"},
            data={
                "name": checkpoint_name,
                "picIdList": '["AJQBCAAQAhgAIKWqgMwGKObW7pcGMLgIOLgI"]',
                "rule": "",
                "payType": "0",
                "dailyCount": "1",
                "auditType": "0",
                "taskCount": "3",
                "price": "0.1",
                "noticeTime": "",
                "isCusAgreement": "false",
                "isOpenAgreement": "false",
                "agreementId": "0",
                "agreementName": "",
                "taskList": json.dumps(task_list, ensure_ascii=False),
            },
            schema="admin.checkpoint.create",
        )
        
        # Assert: 验证创建成功
        admin_client.assert_success(result, "添加打卡活动失败")
        checkpoint_id = assert_any_field(result, ["checkpoint.id", "id", "data.id"], msg="打卡活动创建失败")
    finally:
        # 清理：删除创建的打卡活动
        if checkpoint_id:
            DeleteActions.delete_checkpoint(admin_client, checkpoint_id)

"""
用例 ID: 1150695810001062399
用例名称: 管理后台正常新建作业

接口: POST /ajax/checkpoint_h.jsp?cmd=addCheckpoint
注意：这个接口和打卡活动是同一个接口，但 cmd 参数相同，可能需要其他参数区分
"""
import json
from actions.delete_actions import DeleteActions


def test_admin_add_homework(admin_client, timestamp):
    """管理后台正常新建作业"""
    # Arrange: 准备测试数据
    homework_name = f"接口测试作业_{timestamp}"
    homework_id = None
    
    # taskList: 作业任务列表
    task_list = [
        {
            "id": 1,
            "name": "1",
            "rule": '<p style="line-height:1.5em;">1</p>',
            "sequence": "01",
            "dailyCount": 0,
            "requirement": {
                "t": {"c": False, "mc": 1},
                "i": {"c": False, "mc": 1},
                "audio": {"c": False, "mc": 1},
                "video": {"c": False, "mc": 1},
                "completeQuestion": {"c": False, "mc": 1},
                "linkQuestion": {"link": [], "isOpen": False}
            },
            "passCount": 0,
            "taskCount": 0,
            "isNewAdd": True
        },
        {
            "id": 2,
            "name": "2",
            "rule": '<p style="line-height:1.5em;">2</p>',
            "sequence": "02",
            "dailyCount": 0,
            "requirement": {
                "t": {"c": False, "mc": 1},
                "i": {"c": False, "mc": 1},
                "audio": {"c": False, "mc": 1},
                "video": {"c": False, "mc": 1},
                "completeQuestion": {"c": False, "mc": 1},
                "linkQuestion": {"link": [], "isOpen": False}
            },
            "passCount": 0,
            "taskCount": 0,
            "isNewAdd": True
        },
        {
            "id": 3,
            "name": "3",
            "rule": '<p style="line-height:1.5em;">3</p>',
            "sequence": "03",
            "dailyCount": 0,
            "requirement": {
                "t": {"c": False, "mc": 1},
                "i": {"c": False, "mc": 1},
                "audio": {"c": False, "mc": 1},
                "video": {"c": False, "mc": 1},
                "completeQuestion": {"c": False, "mc": 1},
                "linkQuestion": {"link": [], "isOpen": False}
            },
            "passCount": 0,
            "taskCount": 0,
            "isNewAdd": True
        }
    ]
    
    try:
        # Act: 创建作业
        result = admin_client.post(
            "/ajax/checkpoint_h.jsp",
            params={"cmd": "addCheckpoint"},
            data={
                "name": homework_name,
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
        )
        
        # Assert: 验证创建成功
        admin_client.assert_success(result, "新建作业失败")
        homework_id = result.get("checkpoint", {}).get("id")
        assert homework_id, "作业创建失败"
    finally:
        # 清理：删除创建的作业
        if homework_id:
            DeleteActions.delete_homework(admin_client, homework_id)

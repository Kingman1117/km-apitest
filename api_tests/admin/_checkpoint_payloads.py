"""
管理后台作业/打卡通用 payload 片段。
"""
from typing import Any, Dict, List


def build_default_task_list() -> List[Dict[str, Any]]:
    """生成默认 3 个任务配置，供作业/打卡用例复用。"""
    return [
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
                "linkQuestion": {"link": [], "isOpen": False},
            },
            "passCount": 0,
            "taskCount": 0,
            "isNewAdd": True,
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
                "linkQuestion": {"link": [], "isOpen": False},
            },
            "passCount": 0,
            "taskCount": 0,
            "isNewAdd": True,
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
                "linkQuestion": {"link": [], "isOpen": False},
            },
            "passCount": 0,
            "taskCount": 0,
            "isNewAdd": True,
        },
    ]

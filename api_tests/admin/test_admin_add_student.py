"""
用例 ID: 1150695810001062388
用例名称: 管理后台正常创建学员

接口: POST /ajax/eduStudent_h.jsp?cmd=addEduStudentAndAcct
"""
import json
from security_utils import md5


def test_admin_add_student(admin_client, timestamp):
    """管理后台创建学员 - 验证创建成功"""
    # Arrange: 准备测试数据
    acct = f"ht{timestamp}"
    name = f"后台添加{timestamp}"
    pwd_md5 = md5("123456")

    prop_list = json.dumps([
        {"v": name, "p": 2},
        {"v": "", "p": 10},
        {"v": "", "p": 3},
        {"v": "", "p": 10002},
        {"v": "", "p": 10001},
        {"v": "", "p": 5},
        {"v": "0", "p": 4},
        {"v": "", "p": 9},
        {"v": "", "p": 500},
        {"v": "", "p": 6},
        {"v": "", "p": 10003},
        {"v": "", "p": 10004},
    ], ensure_ascii=False)

    # Act: 创建学员
    result = admin_client.post(
        "/ajax/eduStudent_h.jsp",
        params={"cmd": "addEduStudentAndAcct"},
        data={
            "propList": prop_list,
            "photoImg": "",
            "schoolManagerTeacherIdList": "[]",
            "acct": acct,
            "pwd": pwd_md5,
            "pwdCheck": pwd_md5,
        },
    )

    # Assert: 验证创建成功
    admin_client.assert_success(result, "创建学员失败")
    assert result["data"]["name"] == name, f"学员名称不匹配"
    student_id = result["data"]["id"]
    assert student_id, "学员创建失败"

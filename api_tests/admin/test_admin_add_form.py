"""
用例 ID: 1150695810001062402
用例名称: 管理后台正常添加表单

接口: POST /ajax/wxAppForm_h.jsp?cmd=addWXAppForm
"""
import json
from actions.delete_actions import DeleteActions


def test_admin_add_form(admin_client, timestamp):
    """管理后台正常添加表单"""
    # Arrange: 准备测试数据
    form_name = f"接口测试表单_{timestamp}"
    form_id = None
    
    # contentList: 表单字段列表
    content_list = [
        {"name": "单行文本", "type": 0, "placeholder": "111", "input": "", "must": False},
        {"name": "单选按钮", "type": 1, "placeholder": "", "input": "选项一\n选项二\n选项三", "must": False},
        {"name": "多选按钮", "type": 2, "placeholder": "", "input": "选项一\n选项二\n选项三", "must": False},
        {"name": "多行文本", "type": 3, "placeholder": "", "input": "", "must": False},
        {"name": "文件上传", "type": 4, "placeholder": "", "input": "", "fileSetting": {"fs": 100, "ia": 0, "dftl": "", "ft": 0}, "must": False},
        {"name": "日期时间", "type": 5, "placeholder": "", "input": "", "dateSetting": {"a": 0, "ot": {"t": 0, "ti": 0, "ut": [0, 1, 2, 3, 4, 5, 6, 23], "ut15": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 89, 90, 91, 92, 93, 94, 95], "ut30": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 45, 46, 47]}, "od": {"t": 0, "ud": [], "od": []}, "ba": False, "bh": True, "bpd": True}, "must": False},
        {"name": "下拉选项", "type": 7, "placeholder": "", "input": "选项一\n选项二\n选项三", "must": False},
        {"name": "多级下拉", "type": 20, "placeholder": "", "input": "", "multiLevelDropdownSetting": {"data": ["大区/省份/城市/区县", "华南地区/广东省/广州市/天河区", "华南地区/广东省/广州市/越秀区", "华南地区/广东省/广州市/海珠区", "华南地区/广东省/深圳市/南山区", "华南地区/广东省/深圳市/罗湖区", "华南地区/广东省/深圳市/龙华区", "华南地区/湖南省/株洲市/芦淞区", "华南地区/湖南省/长沙市/天心区", "华东地区/上海市/静安区", "华东地区/上海市/闵行区", "华东地区/浙江省/杭州市/拱墅区", "华东地区/浙江省/杭州市/余杭区", "华北地区/山东省/济南市/历下区", "华北地区/山东省/济南市/章丘区", "华北地区/山东省/青岛市/黄岛区", "华北地区/山东省/青岛市/崂山区"]}, "must": False},
        {"name": "省市区县", "type": 8, "placeholder": "", "input": "", "addrSetting": {"p": "440000", "ph": False, "c": "440100", "ch": False, "d": "440104", "dh": False, "a": "请输入详细地址11", "ah": False}, "must": False},
        {"name": "邮箱地址", "type": 10, "placeholder": "", "input": "", "must": False},
        {"name": "身份证号", "type": 11, "placeholder": "", "input": "", "must": False},
        {"name": "手机号码", "type": 6, "placeholder": "", "input": "", "phoneSetting": {"ov": False}, "must": False}
    ]

    try:
        # Act: 创建表单
        result = admin_client.post(
            "/ajax/wxAppForm_h.jsp",
            params={"cmd": "addWXAppForm"},
            data={
                "name": form_name,
                "contentList": json.dumps(content_list, ensure_ascii=False),
                "wxappId": admin_client.wxapp_id,
                "submitCount": "0",
                "privacyStatus": "true",
            },
        )
        
        # Assert: 验证创建成功
        admin_client.assert_success(result, "添加表单失败")
        form_id = result.get("data", {}).get("id") or result.get("id")
        assert form_id, "表单创建失败"
    finally:
        # 清理：删除创建的表单
        if form_id:
            DeleteActions.delete_form(admin_client, form_id)

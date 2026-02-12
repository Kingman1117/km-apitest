"""
用例 ID: 1150695810001062420
用例名称: 移动端设计器正常添加各个课程模块
接口: POST /api/manage/designerSave/handle

流程：
1. 新增移动端自定义页面（addColInfo）
2. 获取页面详情（getColInfo）
3. 调用 designerSave/handle 保存课程模块配置
4. 再次获取页面详情，确认模块已保存
5. 删除自定义页面（清理数据）
"""
import json
import pytest
from pathlib import Path

from actions.mobile_designer_actions import MobileDesignerActions
from utils.response_assert import assert_field, get_field


@pytest.mark.write
@pytest.mark.rate_limited
def test_mobile_designer_course(admin_client):
    """移动端设计器：新增页面并添加课程模块。"""
    col_id = MobileDesignerActions.add_mobile_custom_page(admin_client)

    try:
        first_info = MobileDesignerActions.get_mobile_col_info(admin_client, col_id=col_id)
        page_data = assert_field(first_info, "pageData", dict, msg="pageData 类型异常")

        # 从 HAR 提取的课程模块完整配置
        course_payload_path = Path(__file__).parent.parent.parent / "config/designer_payloads/mobile_course_modules.json"
        with open(course_payload_path, encoding="utf-8") as f:
            har_payload = json.load(f)

        add_module_info_list = har_payload["addModuleInfoList"]
        module_id_list = har_payload["moduleIdList"]

        set_col_info = {
            "id": int(col_id),
            "type": 1,
            "name": f"课程{col_id[-4:]}",
            "oriName": "自定义",
            "tdk": {"t": "", "k": "", "d": ""},
            "pattern": get_field(page_data, "pattern", default={}),
            "setting": get_field(page_data, "setting", default={}),
            "moduleIdList": module_id_list,
            "addModuleInfoList": add_module_info_list,
            "delModuleIdList": [],
        }

        MobileDesignerActions.mobile_designer_handle_save(admin_client, set_col_info_list=[set_col_info])

        second_info = MobileDesignerActions.get_mobile_col_info(admin_client, col_id=col_id)
        success = assert_field(second_info, "success", bool, msg="保存后读取页面失败")
        assert success is True, f"保存后读取页面失败: {second_info}"
        saved_page_data = assert_field(second_info, "pageData", dict, msg="保存后 pageData 缺失")
        saved_modules = get_field(saved_page_data, "moduleList", default=[])
        assert len(saved_modules) > 0, f"保存后 moduleList 为空: {saved_page_data}"
    finally:
        # 清理：删除自定义页面
        if col_id:
            MobileDesignerActions.delete_mobile_custom_page(admin_client, col_id=col_id)

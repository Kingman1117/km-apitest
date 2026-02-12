"""
用例 ID: 1150695810001062416
用例名称: edupc设计器正常添加自定义栏目以及课程模块，访客态正常预览
接口: POST /ajax/site_h.jsp?cmd=setWafCk_set

流程：
1. EduPC设计器新增栏目（获取 col_id）
2. 添加课程模块（视频、音频、图文、系列课）
3. 校验模块资源列表可获取到目标资源
4. 简化保存（仅保存本次新增模块）
5. 访客态预览并校验新增模块可读
6. 删除刚新增栏目（清理）
"""
import pytest

from actions.designer_common_actions import DesignerCommonActions
from actions.edupc_designer_actions import EdupcDesignerActions
from actions.mobile_designer_actions import MobileDesignerActions


@pytest.mark.write
@pytest.mark.rate_limited
def test_edupc_designer_add_course_modules_preview(edupc_designer_client, edupc_client):
    """EduPC 设计器课程类模块新增并访客预览。"""
    col_id = None
    try:
        column_name = DesignerCommonActions.build_unique_column_name(prefix="课模")
        col_id = EdupcDesignerActions.add_column(edupc_designer_client, column_name=column_name)

        module_templates = [
            {"name": "视频", "style": 35, "type": 1, "id": 201},
            {"name": "音频", "style": 34, "type": 1, "id": 202},
            {"name": "图文", "style": 36, "type": 1, "id": 203},
            {"name": "系列课", "style": 37, "type": 1, "id": 204},
        ]

        saved_modules = []
        module_ids = []
        for module in module_templates:
            module_id = EdupcDesignerActions.add_module(
                edupc_designer_client,
                col_id=col_id,
                module_info=module,
            )
            module_ids.append(module_id)
            saved_modules.append(
                {"id": int(module_id), "type": 1, "style": module["style"], "name": module["name"]}
            )

        EdupcDesignerActions.check_resource_list(
            edupc_designer_client=edupc_designer_client,
            col_id=col_id,
            path="/ajax/video_h.jsp",
            params={"cmd": "getWafNotCk_getList"},
            data={"useGroup": "false", "idList": "[124]", "getSingle": "true", "libId": "-1"},
            expected_id=124,
        )
        EdupcDesignerActions.check_resource_list(
            edupc_designer_client=edupc_designer_client,
            col_id=col_id,
            path="/ajax/audio_h.jsp",
            params={"cmd": "getWafNotCk_getList"},
            data={"useGroup": "false", "idList": "[1161]", "getSingle": "true", "libId": "-1"},
            expected_id=1161,
        )
        EdupcDesignerActions.check_resource_list(
            edupc_designer_client=edupc_designer_client,
            col_id=col_id,
            path="/ajax/news_h.jsp",
            params={"cmd": "getWafNotCk_getList"},
            data={"useGroup": "false", "idList": "[115]", "getSingle": "true"},
            expected_id=115,
        )
        EdupcDesignerActions.check_resource_list(
            edupc_designer_client=edupc_designer_client,
            col_id=col_id,
            path="/ajax/column_h.jsp",
            params={"cmd": "getWafNotCk_getList"},
            data={"idList": "[3345]", "getSingle": "true"},
            expected_id=3345,
        )

        row_ids = [51 + idx for idx in range(len(saved_modules))]
        EdupcDesignerActions.save_added_module_configs_only(
            edupc_designer_client=edupc_designer_client,
            col_id=col_id,
            column_name=column_name,
            module_configs=saved_modules,
            row_ids=row_ids,
        )

        preview_result = EdupcDesignerActions.preview_modules_on_edupc(
            edupc_client,
            col_id=col_id,
            module_ids=module_ids,
        )
        assert "module" in str(preview_result).lower(), f"预览结果中未识别到模块数据: {preview_result}"
    finally:
        if col_id:
            EdupcDesignerActions.delete_column(edupc_designer_client, col_id=col_id)

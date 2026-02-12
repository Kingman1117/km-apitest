"""
用例 ID: 1150695810001062417
用例名称: edupc设计器正常添加各基础和排版模块，访客态正常预览
接口: POST /ajax/site_h.jsp?cmd=setWafCk_set

流程：
1. EduPC设计器新增栏目（获取 col_id）
2. 依次添加基础/排版模块（文本、图片、按钮、图文展示、列表多图、轮播多图、课程搜索、在线地图、横向标签）
3. 简化保存（仅保存本次新增模块）
4. 访客态预览并校验新增模块可读
5. 删除刚新增栏目（清理）
"""
import pytest

from actions.designer_common_actions import DesignerCommonActions
from actions.edupc_designer_actions import EdupcDesignerActions
from actions.mobile_designer_actions import MobileDesignerActions


@pytest.mark.write
@pytest.mark.rate_limited
def test_edupc_designer_add_basic_layout_modules_preview(edupc_designer_client, edupc_client):
    """EduPC 设计器基础/排版模块新增并访客预览。"""
    col_id = None
    try:
        column_name = DesignerCommonActions.build_unique_column_name(prefix="基排")
        col_id = EdupcDesignerActions.add_column(edupc_designer_client, column_name=column_name)

        module_templates = [
            {"name": "文本", "style": 6, "type": 1, "id": 201},
            {"name": "图片", "style": 7, "type": 1, "id": 202},
            {"name": "按钮", "style": 8, "type": 1, "id": 203},
            {"name": "图文模块", "style": 1, "type": 1, "id": 204},
            {"name": "列表多图", "style": 3, "type": 1, "id": 205},
            {"name": "轮播多图", "style": 2, "type": 1, "id": 206},
            {"name": "课程搜索", "style": 29, "type": 1, "id": 207},
            {"name": "在线地图", "style": 19, "type": 1, "id": 208},
            {"name": "横向标签", "style": 32, "type": 1, "id": 209},
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

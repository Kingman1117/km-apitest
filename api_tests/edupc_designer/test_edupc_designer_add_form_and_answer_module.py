"""
用例 ID: 1150695810001062418
用例名称: edupc设计器正常添加表单和答题模块，访客态正常预览
接口: POST /ajax/site_h.jsp?cmd=setWafCk_set

流程：
1. EduPC设计器新增栏目（获取 col_id）
2. 添加表单模块
3. 绑定具体表单（form_row_id）
4. 添加答题模块
5. 选择具体答题活动
6. 简化保存（仅保存本次新增模块）
7. 访客态预览并校验新增模块可读
8. 删除刚新增栏目（清理）
"""
import pytest

from actions.designer_common_actions import DesignerCommonActions
from actions.edupc_designer_actions import EdupcDesignerActions
from test_data_manager import TestDataManager


@pytest.mark.write
@pytest.mark.rate_limited
def test_edupc_designer_add_form_and_answer_module_preview(edupc_designer_client, edupc_client):
    """EduPC 设计器完整链路：新增栏目 -> 模块配置 -> C端预览。"""
    designer_data = TestDataManager.get_designer_data("edupc")

    col_id = None
    try:
        # 1) 新增栏目
        column_name = DesignerCommonActions.build_unique_column_name()
        col_id = EdupcDesignerActions.add_column(edupc_designer_client, column_name=column_name)

        # 2) 添加表单模块
        form_module_id = EdupcDesignerActions.add_module(
            edupc_designer_client,
            col_id=col_id,
            module_info={"name": "表单", "style": 44, "type": 1, "id": 201},
        )

        # 3) 选择具体表单（绑定 form_row_id）
        EdupcDesignerActions.bind_form_to_module(
            edupc_designer_client,
            col_id=col_id,
            form_row_id=int(designer_data["form_row_id"]),
        )

        # 4) 添加答题模块
        answer_module_id = EdupcDesignerActions.add_module(
            edupc_designer_client,
            col_id=col_id,
            module_info={"name": "答题", "style": 45, "type": 1, "id": 202},
        )

        # 5) 选择具体答题活动（校验活动可获取）
        EdupcDesignerActions.select_answer_activity(
            edupc_designer_client,
            col_id=col_id,
            activity_id=int(designer_data["answer_activity_id"]),
        )

        # 6) 简化保存（仅保存新增的表单/答题模块）
        EdupcDesignerActions.save_added_modules_only(
            edupc_designer_client,
            col_id=col_id,
            column_name=column_name,
            form_row_id=int(designer_data["form_row_id"]),
            answer_row_id=int(designer_data.get("answer_row_id", 52)),
            form_module_id=form_module_id,
            answer_module_id=answer_module_id,
            answer_activity_id=int(designer_data["answer_activity_id"]),
        )

        # 7) C端预览（读取刚新增的两个模块）
        preview_result = EdupcDesignerActions.preview_modules_on_edupc(
            edupc_client,
            col_id=col_id,
            module_ids=[form_module_id, answer_module_id],
        )

        # 基础断言：确保返回体包含模块数据
        payload_str = str(preview_result)
        assert "module" in payload_str.lower(), f"预览结果中未识别到模块数据: {preview_result}"
    finally:
        # 8) 删除刚新增栏目（清理）
        if col_id:
            EdupcDesignerActions.delete_column(edupc_designer_client, col_id=col_id)

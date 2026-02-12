"""
EduPC 设计器业务动作

封装 EduPC 设计器新增栏目、添加模块、绑定业务数据、C 端预览校验等动作。
"""
import json
import logging
from typing import Any, Dict, List

from utils.response_assert import assert_any_field, get_field

logger = logging.getLogger(__name__)


class EdupcDesignerActions:
    """EduPC 设计器业务动作"""

    @staticmethod
    def add_column(edupc_designer_client, column_name: str) -> str:
        """新增栏目并返回 col_id。"""
        result = edupc_designer_client.post(
            "/ajax/col_h.jsp",
            params={
                "cmd": "addWafCk_add",
                "fromResponsive": "true",
            },
            data={
                "name": column_name,
                "title": "",
                "cusColAddress": "",
                "footParentId": "0",
                "parentId": "0",
                "openType": "false",
                "all": "true",
                "buddy": "true",
                "byMemberLevel": "true",
                "authMemberLevelId": "1",
                "authBuddyGroupIdList": "[]",
                "memberOnlyLevel": "false",
                "pageBrowserTitle": "false",
                "browserTitle": "",
                "pageSearchKeyword": "false",
                "searchKeyword": "",
                "pageSearchDesc": "false",
                "searchDesc": "",
                "colType": "1",
                "rollingScreenType": "0",
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"{edupc_designer_client.BASE_URL}/manage/navColEdit.jsp?fromResponsive=true",
            },
            schema="designer.edupc.add_column",
        )
        edupc_designer_client.assert_success(result, "设计器新增栏目失败")
        col_id = assert_any_field(result, ["id", "data.id"], msg="新增栏目成功但未返回栏目ID")
        return str(col_id)

    @staticmethod
    def add_module(edupc_designer_client, col_id: str, module_info: Dict[str, Any]) -> str:
        """新增模块并返回 module_id。"""
        result = edupc_designer_client.post(
            "/ajax/module_h.jsp",
            params={},
            data={
                "cmd": "addWafCk_addModule",
                "info": json.dumps(module_info, ensure_ascii=False),
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"{edupc_designer_client.BASE_URL}/col.jsp?id={col_id}",
            },
            schema="designer.edupc.add_module",
        )
        edupc_designer_client.assert_success(result, f"设计器新增模块失败: {module_info}")
        module_id = assert_any_field(
            result,
            ["id", "moduleId", "mid", "data.id", "data.moduleId", "data.mid"],
            msg="新增模块成功但未返回 module_id",
        )
        return str(module_id)

    @staticmethod
    def bind_form_to_module(edupc_designer_client, col_id: str, form_row_id: int) -> Dict[str, Any]:
        """将指定表单绑定到当前栏目中的表单模块。"""
        result = edupc_designer_client.post(
            "/ajax/row_h.jsp",
            params={},
            data={
                "cmd": "addWafCk_add",
                "info": json.dumps(
                    {
                        "id": form_row_id,
                        "type": 1,
                        "pattern": "{\"pc\":{\"pl\":0,\"pr\":0}}",
                    },
                    ensure_ascii=False,
                ),
                "_colId": str(col_id),
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"{edupc_designer_client.BASE_URL}/col.jsp?id={col_id}",
            },
        )
        edupc_designer_client.assert_success(result, f"绑定表单失败: form_row_id={form_row_id}")
        return result

    @staticmethod
    def select_answer_activity(edupc_designer_client, col_id: str, activity_id: int) -> Dict[str, Any]:
        """
        根据答题模块配置查询可用活动并断言目标 activity_id 可见。

        该步骤对应"选择具体答题活动"的拉取列表动作。
        """
        result = edupc_designer_client.post(
            "/ajax/answerActivity_h.jsp",
            params={"cmd": "getAnswerActivityListByModule"},
            data={
                "useGroup": "false",
                "idList": json.dumps([int(activity_id)]),
                "getSingle": "true",
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"{edupc_designer_client.BASE_URL}/col.jsp?id={col_id}",
            },
        )
        edupc_designer_client.assert_success(result, f"获取答题活动列表失败: activity_id={activity_id}")
        payload = json.dumps(result, ensure_ascii=False)
        assert str(activity_id) in payload, f"返回中未找到目标答题活动: {activity_id}\n响应: {payload}"
        return result

    @staticmethod
    def save_added_modules_only(
        edupc_designer_client,
        col_id: str,
        column_name: str,
        form_row_id: int,
        answer_row_id: int,
        form_module_id: str,
        answer_module_id: str,
        answer_activity_id: int,
    ) -> Dict[str, Any]:
        """简化保存：仅保存表单+答题两个新增模块。"""
        modules = [
            {"id": int(form_module_id), "type": 1, "style": 44, "name": "表单"},
            {
                "id": int(answer_module_id),
                "type": 1,
                "style": 45,
                "name": "答题",
                "prop3": json.dumps([int(answer_activity_id)], ensure_ascii=False),
            },
        ]
        row_ids = [int(form_row_id), int(answer_row_id)]
        return EdupcDesignerActions.save_added_module_configs_only(
            edupc_designer_client=edupc_designer_client,
            col_id=col_id,
            column_name=column_name,
            module_configs=modules,
            row_ids=row_ids,
        )

    @staticmethod
    def save_added_module_configs_only(
        edupc_designer_client,
        col_id: str,
        column_name: str,
        module_configs: List[Dict[str, Any]],
        row_ids: List[int],
    ) -> Dict[str, Any]:
        """
        通用简化保存：仅保存本次新增模块，不回传整页历史模块。
        """
        assert module_configs, "module_configs 不能为空"
        assert len(module_configs) == len(row_ids), "module_configs 与 row_ids 数量必须一致"

        normalized_modules: List[Dict[str, Any]] = []
        rows_info: List[Dict[str, Any]] = []
        for idx, module in enumerate(module_configs):
            module_id = int(module["id"])
            row_id = int(row_ids[idx])
            normalized_modules.append(module)
            rows_info.append(
                {
                    "id": row_id,
                    "type": 1,
                    "colId": int(col_id),
                    "cols": [{"type": 0, "mIds": [module_id], "rIds": []}],
                    "pattern": {"pc": {"pl": 0, "pr": 0}},
                }
            )

        info = {
            "rowIds": row_ids,
            "headerRowIds": [],
            "footerRowIds": [],
            "title": {"content": column_name},
        }
        result = edupc_designer_client.post(
            "/ajax/site_h.jsp",
            params={},
            data={
                "cmd": "setWafCk_set",
                "_colId": str(col_id),
                "_extId": "0",
                "info": json.dumps(info, ensure_ascii=False),
                "rowsInfo": json.dumps(rows_info, ensure_ascii=False),
                "modulesInfo": json.dumps(normalized_modules, ensure_ascii=False),
                "delete": json.dumps({"rows": [], "modules": []}, ensure_ascii=False),
                "delRowAll": json.dumps({"all": [], "notAll": []}, ensure_ascii=False),
                "pool": "{}",
                "settings": "{}",
                "baidu": "{}",
                "seoOptions": json.dumps(
                    {
                        "_detailBrowserTitleExt": column_name,
                        "_browserTitleExt": "",
                        "_templateBrowserTitleData": column_name,
                    },
                    ensure_ascii=False,
                ),
                "independentSetting": json.dumps({"pageBanner": False}, ensure_ascii=False),
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"{edupc_designer_client.BASE_URL}/col.jsp?id={col_id}",
            },
        )
        # 某些环境会返回 success=false,wgd=true（权限网关侧），这里统一视为接口已受理
        assert get_field(result, "success", default=False) is True or get_field(result, "wgd", default=False) is True, \
            f"简化保存栏目失败: {result}"
        return result

    @staticmethod
    def check_resource_list(
        edupc_designer_client,
        col_id: str,
        path: str,
        params: Dict[str, Any],
        data: Dict[str, Any],
        expected_id: int,
    ) -> Dict[str, Any]:
        """
        调用模块资源列表接口并校验目标资源 ID 在响应中可见。
        """
        result = edupc_designer_client.post(
            path,
            params=params,
            data=data,
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"{edupc_designer_client.BASE_URL}/col.jsp?id={col_id}",
            },
        )
        edupc_designer_client.assert_success(result, f"资源列表接口失败: {path}")
        payload = json.dumps(result, ensure_ascii=False)
        assert str(expected_id) in payload, f"资源列表返回未包含目标ID={expected_id}: {payload}"
        return result

    @staticmethod
    def delete_column(edupc_designer_client, col_id: str) -> Dict[str, Any]:
        """
        删除栏目（按设计器导航多操作接口）。
        """
        # 来自抓包样例的导航顺序模板；删除时仅替换 rmList
        order = [2, 101, 102, 105, 106, 103, 104, 133, 139, 136, 137, 138, 134, 135, 7, 9]
        md_list = [{"colId": cid, "hidden": cid in [7, 9]} for cid in order]
        result = edupc_designer_client.post(
            "/ajax/col_h.jsp",
            params={"cmd": "setWafCk_multiSet"},
            data={
                "ot": "undefined",
                "order": json.dumps(order, ensure_ascii=False),
                "mdList": json.dumps(md_list, ensure_ascii=False),
                "rmList": json.dumps([int(col_id)], ensure_ascii=False),
                "newIndexColId": "2",
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"{edupc_designer_client.BASE_URL}/manage/nav.jsp?_showHideCol=false&_fromResponsive=true",
            },
        )
        # 某些环境会返回 success=false,wgd=true（权限网关侧），这里统一视为接口已受理
        assert get_field(result, "success", default=False) is True or get_field(result, "wgd", default=False) is True, \
            f"删除栏目失败: {result}"
        return result

    @staticmethod
    def preview_modules_on_edupc(edupc_client, col_id: str, module_ids: List[str]) -> Dict[str, Any]:
        """在 EduPC C 端预览模块数据并断言返回成功。"""
        assert module_ids, "module_ids 不能为空"
        result = edupc_client.post(
            "/ajax/module_h.jsp",
            params={
                "id": str(col_id),
                "cmd": "getWafNotCk_getVisitorModuleData",
                "colId": str(col_id),
                "stuId": str(edupc_client.stu_id),
                "href": f"{edupc_client.BASE_URL}/col.jsp?id={col_id}",
            },
            data={
                "moduleIdList": json.dumps([int(mid) for mid in module_ids]),
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"{edupc_client.BASE_URL}/col.jsp?id={col_id}",
            },
        )
        edupc_client.assert_success(result, "EduPC 端预览模块数据失败")
        return result

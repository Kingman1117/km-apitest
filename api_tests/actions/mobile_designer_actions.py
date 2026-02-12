"""
移动端设计器业务动作

封装移动端设计器新增自定义页面、保存页面数据、删除页面等动作。
"""
import json
import logging
from typing import Any, Dict, List

from utils.response_assert import assert_any_field

logger = logging.getLogger(__name__)


class MobileDesignerActions:
    """移动端设计器业务动作"""

    @staticmethod
    def add_mobile_custom_page(admin_client) -> str:
        """
        移动端设计器：新增自定义页面，返回 col_id。
        接口：/ajax/wxAppCol_h.jsp?cmd=addColInfo
        """
        result = admin_client.post(
            "/ajax/wxAppCol_h.jsp",
            params={
                "cmd": "addColInfo",
                "_wxappId": str(admin_client.wxapp_id),
                "_wxappAid": str(admin_client.wxapp_aid),
            },
            data={},
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"{admin_client.BASE_URL}/editorNew.jsp?_wxappId={admin_client.wxapp_id}&__aacct={admin_client.username}",
            },
            schema="designer.mobile.add_page",
        )
        admin_client.assert_success(result, "移动端设计器新增自定义页面失败")
        col_id = assert_any_field(result, ["colId", "id", "data.colId", "data.id"], msg="新增页面成功但未返回 col_id")
        return str(col_id)

    @staticmethod
    def get_mobile_col_info(admin_client, col_id: str) -> Dict[str, Any]:
        """
        移动端设计器：获取页面详情。
        接口：/ajax/wxAppCol_h.jsp?cmd=getColInfo
        """
        result = admin_client.get(
            "/ajax/wxAppCol_h.jsp",
            params={
                "cmd": "getColInfo",
                "_wxappId": str(admin_client.wxapp_id),
                "_wxappAid": str(admin_client.wxapp_aid),
                "_colId": str(col_id),
            },
            headers={
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"{admin_client.BASE_URL}/editorNew.jsp?_wxappId={admin_client.wxapp_id}&__aacct={admin_client.username}",
            },
        )
        admin_client.assert_success(result, f"获取移动端设计器页面信息失败: col_id={col_id}")
        return result

    @staticmethod
    def save_mobile_col_page_data(admin_client, col_id: str, page_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        移动端设计器：保存页面数据。
        接口：/ajax/wxAppCol_h.jsp?cmd=savePageData
        """
        result = admin_client.post(
            "/ajax/wxAppCol_h.jsp",
            params={
                "cmd": "savePageData",
                "_wxappId": str(admin_client.wxapp_id),
                "_wxappAid": str(admin_client.wxapp_aid),
                "_colId": str(col_id),
            },
            data={
                "_colId": str(col_id),
                "pageData": json.dumps(page_data, ensure_ascii=False),
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"{admin_client.BASE_URL}/editorNew.jsp?_wxappId={admin_client.wxapp_id}&__aacct={admin_client.username}",
            },
        )
        admin_client.assert_success(result, f"保存移动端设计器页面失败: col_id={col_id}")
        return result

    @staticmethod
    def mobile_designer_handle_save(admin_client, set_col_info_list: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        移动端设计器保存聚合接口。
        接口：/api/manage/designerSave/handle
        """
        payload = set_col_info_list if set_col_info_list is not None else []
        result = admin_client.post(
            "/api/manage/designerSave/handle",
            params={
                "wxappAid": str(admin_client.wxapp_aid),
                "wxappId": str(admin_client.wxapp_id),
            },
            data={"setColInfoList": json.dumps(payload, ensure_ascii=False)},
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"{admin_client.BASE_URL}/editorNew.jsp?_wxappId={admin_client.wxapp_id}&__aacct={admin_client.username}",
            },
        )
        admin_client.assert_success(result, "移动端设计器聚合保存接口失败")
        return result

    @staticmethod
    def delete_mobile_custom_page(admin_client, col_id: str) -> Dict[str, Any]:
        """
        删除移动端自定义页面。
        接口：/ajax/wxAppCol_h.jsp?cmd=delColInfo
        """
        result = admin_client.post(
            "/ajax/wxAppCol_h.jsp",
            params={
                "cmd": "delColInfo",
                "_wxappId": str(admin_client.wxapp_id),
                "_wxappAid": str(admin_client.wxapp_aid),
            },
            data={"_colId": str(col_id)},
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"{admin_client.BASE_URL}/editorNew.jsp?_wxappId={admin_client.wxapp_id}&__aacct={admin_client.username}",
            },
        )
        admin_client.assert_success(result, f"删除移动端自定义页面失败: col_id={col_id}")
        return result

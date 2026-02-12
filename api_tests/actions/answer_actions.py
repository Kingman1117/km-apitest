"""
答题相关业务动作

封装答题提交、批阅等可复用业务逻辑
"""
import json
import logging
from typing import Dict, Any, List

from utils.response_assert import assert_any_field, assert_field, get_field

logger = logging.getLogger(__name__)


class AnswerActions:
    """答题业务动作"""

    @staticmethod
    def _warmup_answer_session(edupc_client, activity_id: int, stu_id: str, union_user_id: str) -> None:
        """
        按 HAR 预热答题会话上下文，避免 addRecord 直接调用被服务端拦截。
        """
        base_headers = {
            "Referer": f"{edupc_client.BASE_URL}/exm.jsp?id={activity_id}",
            "X-Requested-With": "XMLHttpRequest",
        }
        post_headers = {
            **base_headers,
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }

        # 1) 登录后任务埋点（HAR 中紧随登录后调用）
        edupc_client.post(
            "/ajax/integral_h.jsp",
            params={"cmd": "doTaskByLogin"},
            data={
                "wxappAid": str(edupc_client.wxapp_aid),
                "wxappId": str(edupc_client.wxapp_id),
            },
            headers=post_headers,
        )

        # 2) 拉取学员列表，确认 unionUserId 与 stuId 归属关系
        student_list_resp = edupc_client.post(
            "/ajax/eduStudent_h.jsp",
            params={},
            data={
                "cmd": "getEduStudentList",
                "wxappId": str(edupc_client.wxapp_id),
                "wxappAid": str(edupc_client.wxapp_aid),
                "unionUserId": union_user_id,
            },
            headers=post_headers,
        )
        edupc_client.assert_success(student_list_resp, "获取学员列表失败")

        # 3) 登录信息补全（HAR 中 window.onload 后调用）
        login_info_resp = edupc_client.post(
            "/ajax/login_h.jsp",
            params={},
            data={"cmd": "wafNotCk_loginInfo"},
            headers=post_headers,
        )
        edupc_client.assert_success(login_info_resp, "获取登录信息失败")

        # 4) token 更新（HAR 中存在，部分环境返回 success=false 但不影响后续）
        edupc_client.get(
            "/ajax/login_h.jsp",
            params={"cmd": "updateToken"},
            headers=base_headers,
        )

        # 5) 站点/模块预热请求（与 HAR 对齐，建立页面上下文）
        edupc_client.get("/api/guest/setting/getContentSetting", params={}, headers=base_headers)
        edupc_client.get(
            "/ajax/module_h.jsp",
            params={
                "id": str(activity_id),
                "cmd": "getWafNotCk_getVisitorModuleData",
                "colId": "12",
                "stuId": stu_id,
                "href": f"{edupc_client.BASE_URL}/exm.jsp?id={activity_id}",
            },
            headers=base_headers,
        )
        edupc_client.get("/api/guest/adPopup/getEduAdPopupList", params={}, headers=base_headers)
        edupc_client.get("/ajax/wxAppConnectionVisitor.jsp", params={}, headers=base_headers)
        edupc_client.get("/ajax/wxAppConnectionVisitor.jsp", params={}, headers=base_headers)
    
    @staticmethod
    def create_answer_record(
        edupc_client,
        activity_id: int,
        column_item_id: int = 0,
        big_column_item_id: int = 0
    ) -> str:
        """
        EduPC端创建答题记录（开始答题）
        
        Args:
            edupc_client: EduPC客户端
            activity_id: 答题活动ID
            column_item_id: 系列课项ID（默认0）
            big_column_item_id: 大系列课项ID（默认0）
        
        Returns:
            record_id: 答题记录ID（用于后续保存、提交、批阅）
        """
        from data_factory import DataFactory
        
        stu_id = DataFactory.resolve_stu_id(edupc_client.stu_id)
        union_user_id = DataFactory.resolve_union_user_id(edupc_client.union_user_id)
        
        logger.info(
            "创建答题记录: activity_id=%s, stu_id=%s (from client: %s), union_user_id=%s (from client: %s)",
            activity_id, stu_id, edupc_client.stu_id, union_user_id, edupc_client.union_user_id
        )

        # 对齐真实链路：addRecord 前先做会话预热
        AnswerActions._warmup_answer_session(edupc_client, activity_id, stu_id, union_user_id)

        # 对齐真实链路：addRecord 前先拉取活动信息
        precheck = edupc_client.get(
            "/ajax/answer_h.jsp",
            params={
                "cmd": "getAnswerActivityInfo",
                "activityId": str(activity_id),
            },
            headers={
                "Referer": f"{edupc_client.BASE_URL}/exm.jsp?id={activity_id}",
                "X-Requested-With": "XMLHttpRequest",
            },
        )
        edupc_client.assert_success(precheck, f"获取答题活动信息失败 (activity_id={activity_id})")
        
        params = {
            "cmd": "addRecord",
            "unionUserId": union_user_id,
            "stuId": stu_id,
            "activityId": str(activity_id),
            "columnItemId": str(column_item_id),
            "bigColumnItemId": str(big_column_item_id),
        }
        
        # EduPC 需要在 URL 参数中传递 _TOKEN
        if edupc_client._token:
            params["_TOKEN"] = edupc_client._token
        
        result = edupc_client.get(
            "/ajax/answer_h.jsp",
            params=params,
            headers={
                "Referer": f"{edupc_client.BASE_URL}/exm.jsp?id={activity_id}",
                "X-Requested-With": "XMLHttpRequest",
            }
        )
        
        edupc_client.assert_success(result, f"创建答题记录失败 (activity_id={activity_id}, stu_id={stu_id})")
        
        # 提取 recordId（兼容 id 在顶层或 data 层）
        record_id = assert_any_field(
            result,
            ["id", "data.id"],
            msg="未获取到答题记录ID",
        )
        
        record_id = str(record_id)
        logger.info("答题记录创建成功: record_id=%s, activity_id=%s", record_id, activity_id)
        return record_id
    
    @staticmethod
    def save_answer(
        edupc_client,
        record_id: str,
        activity_id: int,
        answer_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        EduPC端保存答题（答题过程中）
        
        Args:
            edupc_client: EduPC客户端
            record_id: 答题记录ID（需要提前获取或从页面获取）
            activity_id: 答题活动ID
            answer_list: 答案列表，格式如：
                [
                    {"qid": 77614, "v": "答案文本"},  # 填空题/简答题
                    {"qid": 77615, "o": [1, 2], "v": 1}  # 选择题
                ]
        
        Returns:
            保存结果
        """
        from data_factory import DataFactory
        
        stu_id = DataFactory.resolve_stu_id(edupc_client.stu_id)
        union_user_id = DataFactory.resolve_union_user_id(edupc_client.union_user_id)
        
        params = {"cmd": "saveAnswer"}
        if edupc_client._token:
            params["_TOKEN"] = edupc_client._token
        
        result = edupc_client.post(
            "/ajax/answer_h.jsp",
            params=params,
            data={
                "unionUserId": union_user_id,
                "recordId": record_id,
                "stuId": stu_id,
                "answerList": json.dumps(answer_list, ensure_ascii=False),
                "activityId": str(activity_id),
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
            }
        )
        
        edupc_client.assert_success(result, "保存答题失败")
        logger.info("答题保存成功: record_id=%s, activity_id=%s", record_id, activity_id)
        return result
    
    @staticmethod
    def commit_answer(
        edupc_client,
        record_id: str,
        activity_id: int
    ) -> Dict[str, Any]:
        """
        EduPC端提交答题（最终提交）
        
        Args:
            edupc_client: EduPC客户端
            record_id: 答题记录ID
            activity_id: 答题活动ID
        
        Returns:
            提交结果
        """
        from data_factory import DataFactory
        
        stu_id = DataFactory.resolve_stu_id(edupc_client.stu_id)
        union_user_id = DataFactory.resolve_union_user_id(edupc_client.union_user_id)
        
        params = {"cmd": "commitAnswer"}
        if edupc_client._token:
            params["_TOKEN"] = edupc_client._token
        
        result = edupc_client.post(
            "/ajax/answer_h.jsp",
            params=params,
            data={
                "unionUserId": union_user_id,
                "stuId": stu_id,
                "recordId": record_id,
                "activityId": str(activity_id),
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
            }
        )
        
        edupc_client.assert_success(result, "提交答题失败")
        logger.info("答题提交成功: record_id=%s, activity_id=%s", record_id, activity_id)
        return result
    
    @staticmethod
    def get_answer_record_detail(
        admin_client,
        record_id: str
    ) -> Dict[str, Any]:
        """
        Admin端查看答题记录详情（用于批阅）
        
        Args:
            admin_client: Admin客户端
            record_id: 答题记录ID
        
        Returns:
            答题记录详情，包含学员答案、题目信息等
        """
        result = admin_client.get(
            "/ajax/wxAppAnswer_h.jsp",
            params={
                "cmd": "getAnswerRecordViewInfo",
                "recordId": record_id,
                "wxappAid": admin_client.wxapp_aid,
                "wxappId": admin_client.wxapp_id,
            }
        )
        
        admin_client.assert_success(result, f"查询答题记录详情失败: recordId={record_id}")
        logger.info("答题记录查询成功: record_id=%s", record_id)

        # 兼容两种结构：
        # 1) {"success": true, "data": {...}}
        # 2) {"success": true, "record": {...}, "activity": {...}}
        detail = get_field(result, "data", default=None)
        if isinstance(detail, dict):
            return detail
        return result
    
    @staticmethod
    def review_answer(
        admin_client,
        record_id: str,
        answer_list: List[Dict[str, Any]],
        score: int,
        comment: str = ""
    ) -> Dict[str, Any]:
        """
        Admin端批阅答题（给分+评语）
        
        Args:
            admin_client: Admin客户端
            record_id: 答题记录ID
            answer_list: 答题列表（来自提交流程）
            score: 分数
            comment: 批阅评语
        
        Returns:
            批阅结果
        """
        # 对齐你提供的后台批阅 cURL：POST /ajax/wxAppAnswer_h.jsp（query 仅公共参数）
        # data: cmd=saveAnswerList&recordId=...&answerList=...
        review_answer_list: List[Dict[str, Any]] = []
        per_question_score = 1.0 if score > 1 else float(score)
        for item in answer_list:
            review_item = dict(item)
            # 简答/填空题在后台批阅接口中需要带上评分相关字段
            if "o" not in review_item:
                review_item.setdefault("ns", True)
                review_item.setdefault("s", per_question_score)
                review_item.setdefault(
                    "r",
                    f"<p style=\"line-height:1.5em;\">{comment or '自动化批阅'}<br /></p>",
                )
            review_answer_list.append(review_item)

        result = admin_client.post(
            "/ajax/wxAppAnswer_h.jsp",
            params={},
            data={
                "cmd": "saveAnswerList",
                "recordId": record_id,
                "answerList": json.dumps(review_answer_list, ensure_ascii=False),
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
            }
        )

        admin_client.assert_success(result, f"批阅答题失败: recordId={record_id}")
        logger.info("答题批阅成功: record_id=%s, score=%s", record_id, score)
        return result

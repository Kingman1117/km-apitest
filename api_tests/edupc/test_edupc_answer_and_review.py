"""
用例 ID: 1150695810001062405
用例名称: edupc正常提交答题，B端正常完成批阅
接口: POST /ajax/answer_h.jsp?cmd=commitAnswer

流程：
1. EduPC端创建答题记录（获取recordId）
2. EduPC端保存答题
3. EduPC端提交答题
4. 管理后台查看答题详情
5. 管理后台批阅答题
"""
from actions.answer_actions import AnswerActions
from test_data_manager import TestDataManager


def test_edupc_answer_and_review(edupc_client, admin_client):
    """EduPC端提交答题 -> 管理后台批阅完整流程"""

    # Arrange: 获取测试数据
    answer_data = TestDataManager.get_answer_activity_data("test_activity")
    activity_id = answer_data["activity_id"]
    answer_list = answer_data["answer_list"]

    # Act: EduPC端创建答题记录
    record_id = AnswerActions.create_answer_record(
        edupc_client,
        activity_id=activity_id
    )

    # Act: EduPC端保存答题
    AnswerActions.save_answer(
        edupc_client,
        record_id=record_id,
        activity_id=activity_id,
        answer_list=answer_list
    )

    # Act: EduPC端提交答题
    AnswerActions.commit_answer(
        edupc_client,
        record_id=record_id,
        activity_id=activity_id
    )

    # Act: 管理后台查看答题详情
    answer_detail = AnswerActions.get_answer_record_detail(
        admin_client,
        record_id=record_id
    )

    # Act: 管理后台批阅答题
    AnswerActions.review_answer(
        admin_client,
        record_id=record_id,
        answer_list=answer_list,
        score=85,
        comment="自动化测试批阅"
    )

    # Assert: 各步骤成功断言在 AnswerActions 中统一完成

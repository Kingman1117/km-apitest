"""
删除资源的统一 Actions
避免在各个 Actions 文件中重复删除逻辑
"""
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class DeleteActions:
    """统一的删除操作 Actions"""

    @staticmethod
    def delete_offline_course(admin_client, course_id: int) -> Dict[str, Any]:
        """
        删除线下课程
        接口：/ajax/eduCourse_h.jsp?cmd=delCourse
        """
        result = admin_client.get(
            "/ajax/eduCourse_h.jsp",
            params={"cmd": "delCourse", "id": str(course_id)},
        )
        admin_client.assert_success(result, f"删除线下课程失败: course_id={course_id}")
        return result

    @staticmethod
    def delete_column(admin_client, column_id: int) -> Dict[str, Any]:
        """
        删除系列课
        接口：/ajax/wxAppColumn_h.jsp?cmd=delColumn
        """
        import json
        result = admin_client.post(
            "/ajax/wxAppColumn_h.jsp",
            data={
                "cmd": "delColumn",
                "wxappId": str(admin_client.wxapp_id),
                "idList": json.dumps([column_id]),
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        admin_client.assert_success(result, f"删除系列课失败: column_id={column_id}")
        return result

    @staticmethod
    def delete_news(admin_client, news_id: int) -> Dict[str, Any]:
        """
        删除图文课程
        接口：/ajax/wxAppNews_h.jsp?cmd=delNews
        """
        result = admin_client.post(
            "/ajax/wxAppNews_h.jsp",
            params={"cmd": "delNews"},
            data={"id": str(news_id)},
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
            },
        )
        admin_client.assert_success(result, f"删除图文课程失败: news_id={news_id}")
        return result

    @staticmethod
    def delete_audio(admin_client, audio_id: int) -> Dict[str, Any]:
        """
        删除音频课程
        接口：/ajax/wxAppAudio_h.jsp?cmd=del
        """
        result = admin_client.post(
            "/ajax/wxAppAudio_h.jsp",
            data={
                "id": str(audio_id),
                "wxappId": str(admin_client.wxapp_id),
                "cmd": "del",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        admin_client.assert_success(result, f"删除音频课程失败: audio_id={audio_id}")
        return result

    @staticmethod
    def delete_video(admin_client, video_id: int) -> Dict[str, Any]:
        """
        删除视频课程
        接口：/ajax/video_h.jsp?cmd=delVideo
        """
        result = admin_client.post(
            "/ajax/video_h.jsp",
            data={
                "id": str(video_id),
                "wxappId": str(admin_client.wxapp_id),
                "cmd": "delVideo",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        admin_client.assert_success(result, f"删除视频课程失败: video_id={video_id}")
        return result

    @staticmethod
    def delete_ebook(admin_client, ebook_id: int) -> Dict[str, Any]:
        """
        删除电子书
        接口：/api/manage/electronicBook/delElectronicBook
        """
        result = admin_client.post(
            "/api/manage/electronicBook/delElectronicBook",
            data={"id": str(ebook_id)},
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
            },
        )
        admin_client.assert_success(result, f"删除电子书失败: ebook_id={ebook_id}")
        return result

    @staticmethod
    def delete_book_service(admin_client, service_id: int) -> Dict[str, Any]:
        """
        删除课外服务
        接口：/api/manage/book/delBookService
        """
        result = admin_client.post(
            "/api/manage/book/delBookService",
            data={"id": str(service_id)},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        admin_client.assert_success(result, f"删除课外服务失败: service_id={service_id}")
        return result

    @staticmethod
    def delete_product(admin_client, product_id: int) -> Dict[str, Any]:
        """
        删除实物商品
        接口：/ajax/eduProduct_h.jsp?cmd=delProduct
        """
        import json
        result = admin_client.get(
            "/ajax/eduProduct_h.jsp",
            params={
                "cmd": "delProduct",
                "idList": json.dumps([product_id]),
            },
        )
        admin_client.assert_success(result, f"删除实物商品失败: product_id={product_id}")
        return result

    @staticmethod
    def delete_question_bank(admin_client, bank_id: int) -> Dict[str, Any]:
        """
        删除题库
        接口：/api/manage/batchOpt/del (serviceType=25)
        """
        import json
        result = admin_client.post(
            "/api/manage/batchOpt/del",
            data={
                "serviceType": "25",
                "serviceIdList": json.dumps([bank_id]),
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
            },
        )
        admin_client.assert_success(result, f"删除题库失败: bank_id={bank_id}")
        return result

    @staticmethod
    def delete_homework(admin_client, homework_id: int) -> Dict[str, Any]:
        """
        删除作业
        接口：/ajax/eduHomework_h.jsp?cmd=delHomework
        """
        import json
        result = admin_client.get(
            "/ajax/eduHomework_h.jsp",
            params={
                "cmd": "delHomework",
                "eduId": str(admin_client.wxapp_id),
                "idListStr": json.dumps([homework_id]),
            },
        )
        admin_client.assert_success(result, f"删除作业失败: homework_id={homework_id}")
        return result

    @staticmethod
    def delete_checkpoint(admin_client, checkpoint_id: int) -> Dict[str, Any]:
        """
        删除打卡活动
        接口：/ajax/checkpoint_h.jsp?cmd=delCheckpoint
        """
        import json
        result = admin_client.get(
            "/ajax/checkpoint_h.jsp",
            params={
                "cmd": "delCheckpoint",
                "idList": json.dumps([checkpoint_id]),
            },
        )
        admin_client.assert_success(result, f"删除打卡活动失败: checkpoint_id={checkpoint_id}")
        return result

    @staticmethod
    def delete_evaluation(admin_client, evaluation_id: int) -> Dict[str, Any]:
        """
        删除测评
        接口：/api/manage/batchOpt/del (serviceType=24)
        """
        import json
        result = admin_client.post(
            "/api/manage/batchOpt/del",
            data={
                "serviceType": "24",
                "serviceIdList": json.dumps([evaluation_id]),
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
            },
        )
        admin_client.assert_success(result, f"删除测评失败: evaluation_id={evaluation_id}")
        return result

    @staticmethod
    def delete_form(admin_client, form_id: int) -> Dict[str, Any]:
        """
        删除表单
        接口：/ajax/wxAppForm_h.jsp?cmd=delWXAppForm
        """
        import json
        result = admin_client.post(
            "/ajax/wxAppForm_h.jsp",
            params={"cmd": "delWXAppForm"},
            data={
                "delIdList": json.dumps([form_id]),
                "wxappId": str(admin_client.wxapp_id),
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        admin_client.assert_success(result, f"删除表单失败: form_id={form_id}")
        return result

    @staticmethod
    def delete_coupon(admin_client, coupon_id: int) -> Dict[str, Any]:
        """
        删除优惠券
        接口：/ajax/coupon_h.jsp?cmd=delCoupon
        """
        import json
        result = admin_client.get(
            "/ajax/coupon_h.jsp",
            params={
                "cmd": "delCoupon",
                "idList": json.dumps([coupon_id]),
            },
        )
        admin_client.assert_success(result, f"删除优惠券失败: coupon_id={coupon_id}")
        return result

    @staticmethod
    def delete_redemption_code(admin_client, code_id: int) -> Dict[str, Any]:
        """
        删除兑换码（需先失效再删除）
        接口：
        1. /ajax/eduCouponCode_h.jsp?cmd=setWafCk_invalidCoupon (失效)
        2. /ajax/eduCouponCode_h.jsp?cmd=delWafCk_deleteCoupon (删除)
        """
        import json
        
        # 先失效
        invalid_result = admin_client.get(
            "/ajax/eduCouponCode_h.jsp",
            params={
                "cmd": "setWafCk_invalidCoupon",
                "couponIds": json.dumps([code_id]),
            },
        )
        admin_client.assert_success(invalid_result, f"失效兑换码失败: code_id={code_id}")
        
        # 再删除
        delete_result = admin_client.get(
            "/ajax/eduCouponCode_h.jsp",
            params={
                "cmd": "delWafCk_deleteCoupon",
                "couponIds": json.dumps([code_id]),
            },
        )
        admin_client.assert_success(delete_result, f"删除兑换码失败: code_id={code_id}")
        return delete_result

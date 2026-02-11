"""
内容创建相关业务动作（当前仅保留在用能力）。
"""
import logging
import time
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


def _future_date(days: int = 365) -> str:
    """生成未来日期字符串（默认1年后），格式 YYYY-MM-DD"""
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")


class ContentActions:
    """管理后台内容创建动作。"""

    @staticmethod
    def create_audio(admin_client, name: str, file_id: str, summary: str = "", **extra_data) -> str:
        validity_date = _future_date()
        data = {
            "wxappId": admin_client.wxapp_id,
            "name": name,
            "summary": summary,
            "content": "",
            "fileId": file_id,
            "picIdList": "[]",
            "classifyIdList": "[]",
            "tdk": '{"t":"","d":"","k":""}',
            "setting": f'{{"bp":0,"bml":1,"btype":0,"bmtgs":[],"pageStyle":1,"pfk":{{"ss":false,"pm":0,"pa":0.01,"sst":0,"vsu":0,"atm":0,"duration":0,"asp":0,"lp":0.01,"slp":0,"validityType":0,"validityDate":"{validity_date}"}},"fdl":{{"s":0,"ip":0,"fil":[],"viewType":0}}}}',
            "subscriptionsNum": "0",
            "homeworkId": "0",
            "columnItemId": "0",
            "isRelevancyColumn": "false",
            "relevancyColumnId": "0",
            "coverType": "0",
            "isCusAgreement": "false",
            "isOpenAgreement": "false",
            "agreementId": "0",
            "agreementName": "",
            **extra_data,
        }
        result = admin_client.post("/ajax/wxAppAudio_h.jsp", params={"cmd": "add"}, data=data)
        admin_client.assert_success(result, "创建音频失败")
        audio_id = admin_client.extract_id(result, id_field="id", data_path=None)
        logger.info("音频创建成功: id=%s name=%s", audio_id, name)
        return audio_id

    @staticmethod
    def create_video(admin_client, name: str, file_id: str, summary: str = "", **extra_data) -> str:
        validity_date = _future_date()
        data = {
            "wxappId": admin_client.wxapp_id,
            "id": "0",
            "name": name,
            "summary": summary,
            "type": "0",
            "vid": "",
            "file": file_id,
            "postFile": "",
            "classifyIdList": "[]",
            "content": "",
            "offSale": "false",
            "setting": f'{{"bp":0,"bml":1,"btype":0,"bmtgs":[],"pfk":{{"ss":false,"pm":0,"pa":0.01,"sst":0,"vsu":0,"atm":0,"duration":0,"asp":0,"lp":0.01,"slp":0,"validityType":0,"validityDate":"{validity_date}"}},"fdl":{{"s":0,"ip":0,"fil":[],"viewType":0}}}}',
            "subscriptionsNum": "0",
            "homeworkId": "0",
            "columnItemId": "0",
            "isRelevancyColumn": "false",
            "relevancyColumnId": "0",
            "coverType": "2",
            "isCusAgreement": "false",
            "isOpenAgreement": "false",
            "agreementId": "0",
            "agreementName": "",
            **extra_data,
        }
        result = admin_client.post("/ajax/video_h.jsp", params={"cmd": "addVideo"}, data=data)
        admin_client.assert_success(result, "创建视频失败")
        video_id = admin_client.extract_id(result, id_field="id", data_path="video")
        logger.info("视频创建成功: id=%s name=%s", video_id, name)
        return video_id

    @staticmethod
    def create_news(admin_client, name: str, summary: str = "", **extra_data) -> str:
        data = {
            "title": name,
            "autoSummary": "true",
            "summary": summary,
            "views": "0",
            "content": "<p>自动化接口测试图文内容</p>",
            "picId": "",
            "publicTime": time.strftime("%Y-%m-%d %H:%M"),
            "top": "false",
            "isCusPic": "false",
            "tdk": '{"t":"","d":"","k":""}',
            "setting": '{"sd":0,"bp":0,"bml":1,"btype":0,"bmtgs":[],"pfk":{"ss":false,"pm":0,"pa":0.01,"sst":0,"vsu":0,"duration":0,"asp":0,"svct":0,"ovc":0,"lp":0.01,"slp":0,"validityType":0,"validityDate":""},"fdl":{"s":0,"ip":0,"fil":[],"viewType":0}}',
            "homeworkId": "0",
            "isRelevancyColumn": "false",
            "classifyIdList": "[]",
            "isCusAgreement": "false",
            "isOpenAgreement": "false",
            "agreementId": "0",
            "agreementName": "",
            **extra_data,
        }
        result = admin_client.post("/ajax/wxAppNews_h.jsp", params={"cmd": "addNews"}, data=data)
        admin_client.assert_success(result, "创建图文失败")
        news_id = admin_client.extract_id(result, id_field="id", data_path="data")
        logger.info("图文创建成功: id=%s name=%s", news_id, name)
        return news_id

    @staticmethod
    def create_column(admin_client, name: str, summary: str = "", **extra_data) -> str:
        validity_date = _future_date()
        data = {
            "wxappId": admin_client.wxapp_id,
            "name": name,
            "summary": summary,
            "picIdList": '["AJQBCAAQAhgAIKWqgMwGKObW7pcGMLgIOLgI"]',
            "payModel": "1",
            "price": "0.01",
            "status": "0",
            "introduce": "",
            "setting": f'{{"so":0,"vo":0,"bp":0,"bml":1,"sm":0,"ds":0,"btype":0,"bmtgs":[],"snt":1,"vct":1,"utt":2,"duration":0,"asp":0,"lp":0.01,"slp":0,"obsd":0,"oasd":0,"hd":0,"bsdd":{{"qrCodeUrl":"","qrCode":"","eg":"添加老师微信，获取更多服务","wt":"微信二维码","wd":"长按二维码添加微信","apuw":false}},"asdd":{{"qrCodeUrl":"","qrCode":"","eg":"添加老师微信，获取更多服务","wt":"微信二维码","wd":"长按二维码添加微信","apuw":false}},"stmo":0,"apl":{{"painlt":0,"esinlt":0}},"dds":0,"dateModeDetail":{{"type":1,"day":1,"time":"08:00","num":1,"itemType":3}},"columnDirectoryStyle":1,"validityType":0,"validityDate":"{validity_date}","fdl":{{"s":0,"ip":0,"fil":[],"viewType":0,"showTime":0}}}}',
            "isBigColumn": "false",
            "openPresent": "false",
            "classifyIdList": "[]",
            "courseType": "0",
            "startType": "0",
            "fixedStartTime": "",
            "isSignUpEndTime": "false",
            "signUpEndTime": "",
            "isCusAgreement": "false",
            "isOpenAgreement": "false",
            "agreementId": "0",
            "agreementName": "",
            **extra_data,
        }
        result = admin_client.post("/ajax/wxAppColumn_h.jsp", params={"cmd": "addColumn"}, data=data)
        admin_client.assert_success(result, "创建系列课失败")
        column_id = admin_client.extract_id(result, id_field="id", data_path=None)
        logger.info("系列课创建成功: id=%s name=%s", column_id, name)
        return column_id

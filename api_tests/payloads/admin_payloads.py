"""
Admin 相关测试 payload 模板。
"""
import json
from typing import Any, Dict, List


def build_add_form_payload(form_name: str, wxapp_id: str) -> Dict[str, Any]:
    content_list = [
        {"name": "单行文本", "type": 0, "placeholder": "111", "input": "", "must": False},
        {"name": "单选按钮", "type": 1, "placeholder": "", "input": "选项一\n选项二\n选项三", "must": False},
        {"name": "多选按钮", "type": 2, "placeholder": "", "input": "选项一\n选项二\n选项三", "must": False},
        {"name": "多行文本", "type": 3, "placeholder": "", "input": "", "must": False},
        {"name": "文件上传", "type": 4, "placeholder": "", "input": "", "fileSetting": {"fs": 100, "ia": 0, "dftl": "", "ft": 0}, "must": False},
        {"name": "日期时间", "type": 5, "placeholder": "", "input": "", "dateSetting": {"a": 0, "ot": {"t": 0, "ti": 0, "ut": [0, 1, 2, 3, 4, 5, 6, 23], "ut15": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 89, 90, 91, 92, 93, 94, 95], "ut30": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 45, 46, 47]}, "od": {"t": 0, "ud": [], "od": []}, "ba": False, "bh": True, "bpd": True}, "must": False},
        {"name": "下拉选项", "type": 7, "placeholder": "", "input": "选项一\n选项二\n选项三", "must": False},
        {"name": "多级下拉", "type": 20, "placeholder": "", "input": "", "multiLevelDropdownSetting": {"data": ["大区/省份/城市/区县", "华南地区/广东省/广州市/天河区", "华南地区/广东省/广州市/越秀区", "华南地区/广东省/广州市/海珠区", "华南地区/广东省/深圳市/南山区", "华南地区/广东省/深圳市/罗湖区", "华南地区/广东省/深圳市/龙华区", "华南地区/湖南省/株洲市/芦淞区", "华南地区/湖南省/长沙市/天心区", "华东地区/上海市/静安区", "华东地区/上海市/闵行区", "华东地区/浙江省/杭州市/拱墅区", "华东地区/浙江省/杭州市/余杭区", "华北地区/山东省/济南市/历下区", "华北地区/山东省/济南市/章丘区", "华北地区/山东省/青岛市/黄岛区", "华北地区/山东省/青岛市/崂山区"]}, "must": False},
        {"name": "省市区县", "type": 8, "placeholder": "", "input": "", "addrSetting": {"p": "440000", "ph": False, "c": "440100", "ch": False, "d": "440104", "dh": False, "a": "请输入详细地址11", "ah": False}, "must": False},
        {"name": "邮箱地址", "type": 10, "placeholder": "", "input": "", "must": False},
        {"name": "身份证号", "type": 11, "placeholder": "", "input": "", "must": False},
        {"name": "手机号码", "type": 6, "placeholder": "", "input": "", "phoneSetting": {"ov": False}, "must": False},
    ]
    return {
        "name": form_name,
        "contentList": json.dumps(content_list, ensure_ascii=False),
        "wxappId": wxapp_id,
        "submitCount": "0",
        "privacyStatus": "true",
    }


def build_add_offline_course_payload(course_name: str, wxapp_id: str) -> Dict[str, Any]:
    return {
        "courseType": "0",
        "courseName": course_name,
        "tollMethod": "0",
        "purchaseLimit": "false",
        "content": "",
        "summary": "",
        "setting": '{"bp":0,"bml":0,"fdl":{"s":0,"ip":0,"fil":[],"viewType":0},"btype":0,"bmtgs":[],"vc":{"cm":0,"dd":"","du":0,"et":0,"vst":"","vet":""},"pageSetting":{"promptValue":3,"promptText":"可在【我的】页面，点击【我的课程】查看已购课程","jumpValue":3,"jumpCustomValue":[2,3],"customerValue":3,"guideText":"如有疑惑，可通过以下方式，与我们联系","openPhone":false,"phone":"","openQrCode":false,"qrCode":"","qrCodeUrl":"","qrText":"添加客服微信，第一时间解决您的疑问","openOfficialCode":false,"officialCode":"","officialCodeUrl":"","officialText":"关注公众号，获取最新课程信息&联系客服"},"obsd":0,"oasd":0,"bsdd":{"qrCodeUrl":"","qrCode":"","eg":"添加老师微信，获取更多服务","wt":"微信二维码","wd":"长按二维码添加微信","apuw":false,"ep":0,"bt":"进群"},"asdd":{"qrCodeUrl":"","qrCode":"","eg":"添加班主任安排课程","wt":"微信二维码","wd":"长按二维码添加微信","apuw":true,"bt":"扫码","ep":0},"independentOrderProp":false}',
        "classifyIdList": "[]",
        "picList": '[{"id":"AJQBCAAQAhgAILqSoMkGKOnJ_o4GMLgIOLgI","url":"//3444128.s148i.faieduusr.com.faidev.cc/2/110/AJQBCAAQAhgAILqSoMkGKOnJ_o4GMLgIOLgI.jpg"}]',
        "addSpecificationList": '[{"name":"100课时","num":100,"price":100,"promotionPrice":50,"total":1000,"type":0,"isEdited":true}]',
        "headerImgList[0][id]": "AJQBCAAQAhgAILqSoMkGKOnJ_o4GMLgIOLgI",
        "headerImgList[0][url]": "//3444128.s148i.faieduusr.com.faidev.cc/2/110/AJQBCAAQAhgAILqSoMkGKOnJ_o4GMLgIOLgI.jpg",
        "pl": '{"k":0,"ln":1}',
        "openPresent": "false",
        "teachCourseIdList": "[]",
        "isCusAgreement": "false",
        "isOpenAgreement": "false",
        "agreementId": "0",
        "agreementName": "",
        "globalAgreement[open]": "false",
        "globalAgreement[id]": "162",
        "globalAgreement[name]": "购课须知",
        "wxappId": wxapp_id,
        "independentOrderProp": "false",
    }


def build_add_evaluation_payload(evaluation_name: str) -> Dict[str, Any]:
    return {
        "name": evaluation_name,
        "pic": "",
        "picUrl": "",
        "summary": "",
        "payType": "3",
        "payOpportunity": "0",
        "price": "0.01",
        "introduce": "",
        "classifyIdList": "[]",
        "setting": '{"bp":0,"btype":0,"bmtgs":[],"bml":1,"pfk":{"asp":0,"duration":0,"validityType":0,"validityDate":"","otc":0,"stct":1,"lp":0.01,"slp":0},"joinType":0,"joinNum":1,"resultType":0,"resultNum":1,"dimensionType":0,"evaluationType":0,"chartType":0,"showScore":1,"showChart":0,"wxType":0,"wxDesc":"","wxList":[{"open":0,"qrCode":"","text":"","qrCodeUrl":""},{"open":0,"qrCode":"","text":"","qrCodeUrl":""}]}',
        "questionSort": "[-10000001]",
        "isCusAgreement": "false",
        "isOpenAgreement": "false",
        "agreementId": "0",
        "agreementName": "",
        "globalAgreement": '{"open":false,"id":0,"name":""}',
        "addDimensionList": "[]",
        "addQuestionList": '[{"id":-10000001,"stem":"111","type":0,"optionContent":{"options":[{"id":1,"value":"22","score":1},{"id":2,"value":"33","score":1}]}}]',
        "addResultList": '[{"id":-1,"name":"其他结果","section":[],"result":"无法评估，请重新测试","analysis":"","recommend":[],"isOtherResult":true,"setting":{"rulesType":0,"cl":[],"so":0,"sofs":[1],"sd":1,"sdfs":[1],"sda":1}}]',
        "addDimensionGroupList": "[]",
        "addOverallIndicatorList": '[{"id":-9999,"name":"测评总分","isSys":true,"formula":"#测评总分#","isTotalScore":true,"degree":{"dl":[]}},{"id":-10000,"name":"测评平均分","isSys":true,"formula":"#测评平均分#","isAverageScore":true,"degree":{"dl":[]}}]',
        "addDimensionIndicatorList": '[{"id":-1,"name":"平均分","degree":{"dl":[]},"dimensionDegreeList":[]}]',
    }


def build_add_redemption_code_payload(code_name: str) -> Dict[str, Any]:
    return {
        "name": code_name,
        "channels": "[]",
        "remark": "",
        "universalCode": "",
        "type": "1",
        "codeType": "1",
        "generateType": "0",
        "startTime": "1770181200000",
        "endTime": "1803657599000",
        "stockNum": "1000",
        "useCount": "1",
        "noCountLimit": "true",
        "rightsType": "1",
        "noTimeLimit": "true",
        "couponType": "0",
        "savePrice": "9.99",
        "saveDiscount": "0.1",
        "useStartTime": "",
        "useEndTime": "",
        "ruleTxt": "说说说",
        "pricePageInfo": '{"showPrice":0,"useNotice":""}',
        "isAllCourse": "true",
        "serviceList": "[]",
        "serviceInfo": "{}",
        "status": "0",
    }


def build_add_book_service_payload(service_name: str) -> Dict[str, Any]:
    return {
        "serviceName": service_name,
        "summary": "",
        "price": "0",
        "promotionPrice": "0",
        "picList": '[{"id":"AJQBCAAQAhgAIKWqgMwGKObW7pcGMLgIOLgI"}]',
        "classifyIdList": "[]",
        "content": "",
        "type": "0",
        "addSpecificationList": "[]",
        "isLimit": "false",
        "addMappingList": "[]",
        "limitCount": "0",
        "setting": '{"bp":0,"bml":1,"btype":0,"bmtgs":[],"pu":{"t":0,"v":""},"pl":{"t":0,"k":0,"v":0,"ti":""},"fdl":{"s":0,"ip":0,"fil":[],"viewType":0},"cs":{"p":"13919161913","po":true,"prov":"广州市","addr":"天河路250号","ao":false,"lat":0,"lng":0,"blat":0,"blng":0,"bts":{"odl":[1,2,3,4,5,6,0],"og":{"t":0,"gd":7},"a":1,"ot":{"t":1,"ut":[0,1,2,3,4,5,6,23],"ti":0,"ut30":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,45,46,47],"ut15":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,89,90,91,92,93,94,95]},"od":{"t":0,"ud":[],"od":[]},"lc":{"c":1,"l":true}},"bto":false},"cso":false,"obsd":0,"oasd":0,"bsdd":{"qrCodeUrl":"","qrCode":"","eg":"添加老师微信，获取更多服务","wt":"微信二维码","wd":"长按二维码添加微信","apuw":false,"ep":0,"bt":"进群"},"asdd":{"qrCodeUrl":"","qrCode":"","eg":"添加班主任安排课程","bt":"扫码","wt":"微信二维码","wd":"长按二维码添加微信","apuw":true},"ss":{"pt":0,"lt":0,"ct":0,"so":[]}}',
        "isCusAgreement": "false",
        "isOpenAgreement": "false",
        "agreementId": "0",
        "agreementName": "",
        "independentOrderProp": "false",
    }


def build_add_coupon_payload(coupon_name: str, wxapp_id: str) -> Dict[str, Any]:
    entries = [
        {"type": 5, "selected": True, "name": "系列课", "suitableTarget": {"suitableType": 0, "category": 0, "selectedIdList": [], "selectedClassifyIdList": []}},
        {"type": 2, "selected": True, "name": "音频", "suitableTarget": {"suitableType": 0, "category": 0, "selectedIdList": [], "selectedClassifyIdList": []}},
        {"type": 4, "selected": True, "name": "视频", "suitableTarget": {"suitableType": 0, "category": 0, "selectedIdList": [], "selectedClassifyIdList": []}},
        {"type": 1, "selected": True, "name": "图文", "suitableTarget": {"suitableType": 0, "category": 0, "selectedIdList": [], "selectedClassifyIdList": []}},
        {"type": 0, "selected": True, "name": "线下课程", "suitableTarget": {"suitableType": 0, "category": 0, "selectedIdList": [], "selectedClassifyIdList": []}},
        {"type": 14, "selected": True, "name": "商品", "suitableTarget": {"suitableType": 0, "category": 0, "selectedIdList": [], "selectedClassifyIdList": []}},
        {"type": 9, "selected": True, "name": "会员卡", "suitableTarget": {"suitableType": 0, "category": 0, "selectedIdList": [], "selectedClassifyIdList": []}},
        {"type": 7, "selected": True, "name": "答题", "suitableTarget": {"suitableType": 0, "category": 0, "selectedIdList": [], "selectedClassifyIdList": []}},
        {"type": 24, "selected": True, "name": "测评", "suitableTarget": {"suitableType": 0, "category": 0, "selectedIdList": [], "selectedClassifyIdList": []}},
        {"type": 25, "selected": True, "name": "题库", "suitableTarget": {"suitableType": 0, "category": 0, "selectedIdList": [], "selectedClassifyIdList": []}},
        {"type": 15, "selected": True, "name": "课外服务", "suitableTarget": {"suitableType": 0, "category": 0, "selectedIdList": [], "selectedClassifyIdList": []}},
    ]
    return {
        "wxappId": wxapp_id,
        "id": "-1",
        "name": coupon_name,
        "type": "0",
        "discountPrice": "100",
        "discount": "9.8",
        "timeType": "1",
        "startTime": "",
        "endTime": "",
        "day": "1000",
        "remainType": "1",
        "remainCount": "1",
        "entries": json.dumps(entries, ensure_ascii=False),
        "rule": "",
        "isIntegralMall": "false",
        "targetUser": '{"bp":0,"btype":0,"bmtgs":[],"bml":1}',
        "isNewClassify": "true",
    }


def build_add_product_payload(product_name: str) -> Dict[str, Any]:
    return {
        "name": product_name,
        "remark": "",
        "keepProp2": "",
        "hasWeight": "false",
        "imgList": '["AJQBCAAQAhgAIKWqgMwGKObW7pcGMLgIOLgI"]',
        "imgPathList": '["//3444128.s148i.faieduusr.com.faidev.cc/2/110/AJQBCAAQAhgAIKWqgMwGKObW7pcGMLgIOLgI.jpg"]',
        "distributeList": "[0,1]",
        "shippingTmpId": "-1",
        "specList": '[{"name":"尺码","sort":1,"inPdScValList":[{"fi":"","n":"s","path":"","c":true},{"fi":"","n":"m","path":"","c":true},{"fi":"","n":"l","path":"","c":true}]}]',
        "specInfoList": '[{"count":1000,"nameList":["s"],"originPrice":"1500.00","price":"100.00","weight":"0.00","sort":1},{"count":1000,"nameList":["m"],"originPrice":"257.00","price":"17.00","weight":"0.00","sort":2},{"count":2000,"nameList":["l"],"originPrice":"59.00","price":"14.77","weight":"0.00","sort":3}]',
        "setting": '{"bp":0,"bml":1,"btype":0,"bmtgs":[]}',
        "openPresent": "false",
        "productOtherSub": "0",
        "classifyIdList": "[]",
        "addPresentList": "[]",
        "isCusAgreement": "false",
        "isOpenAgreement": "false",
        "agreementId": "0",
        "agreementName": "",
        "independentOrderProp": "false",
        "addPropList": "[]",
        "updatePropList": "[]",
        "delPropIdList": "[]",
    }


def build_add_question_bank_payload(bank_name: str) -> Dict[str, Any]:
    return {
        "id": "0",
        "name": bank_name,
        "summary": "",
        "pic": "",
        "picUrl": "",
        "classifyIdList": "[]",
        "classifyList": "[]",
        "introduce": "",
        "payType": "3",
        "price": "0.01",
        "setting": '{"bp":0,"bml":1,"btype":0,"bmtgs":[],"memoryMode":1,"menuTypes":[1,2,3,4,5],"pfk":{"lp":0.01,"slp":0,"duration":0,"validityType":0,"asp":0,"sst":0,"vsu":0,"bpam":1}}',
        "isCusAgreement": "false",
        "isOpenAgreement": "false",
        "agreementId": "0",
        "agreementName": "",
        "globalAgreement": '{"open":false,"id":0,"name":""}',
    }


def build_add_ebook_payload(ebook_name: str, file_id: str) -> Dict[str, Any]:
    info = {
        "name": ebook_name,
        "pic": "",
        "picUrl": "",
        "author": "",
        "summary": "",
        "fileId": file_id,
        "content": "",
        "setting": {
            "bp": 0,
            "bml": 1,
            "btype": 0,
            "bmtgs": [],
            "ds": 0,
            "pfk": {"ss": True, "pm": 0, "pa": 0.01, "duration": 0, "asp": 1},
        },
        "fileName": "final_optimized_text_version.pdf",
        "fileTypeStr": "pdf",
        "relevancyColumnId": 0,
        "isRelevancyColumn": False,
        "isCusAgreement": False,
        "isOpenAgreement": False,
        "agreementId": 0,
        "agreementName": "",
        "globalAgreement": {"open": False, "id": 163, "name": "购课须知"},
    }
    return {
        "info": json.dumps(info, ensure_ascii=False),
        "isCusAgreement": "false",
        "isOpenAgreement": "false",
        "agreementId": "0",
        "agreementName": "",
    }


def build_add_answer_activity_payload(activity_name: str, wxapp_id: str) -> Dict[str, Any]:
    return {
        "isRelevancyColumn": "false",
        "relevancyColumnId": "0",
        "wxappId": wxapp_id,
        "isUnLimitTime": "true",
        "name": activity_name,
        "mode": "0",
        "startTime": "",
        "endTime": "",
        "questionBuildAction": "0",
        "payType": "0",
        "price": "0.01",
        "setting": '{"at":{"t":1,"v":60},"ac":{"t":1,"v":1,"dailyLimitCount":1},"pa":{"t":0,"v":""},"bml":1,"bp":0,"btype":0,"bmtgs":[],"wp":0,"ar":0,"rqna":false,"wqna":false,"qooo":0,"memoryMode":0,"preCheat":{"cutScreenOpen":false,"cutScreenCount":3,"cutScreenTime":3,"screenshotOpen":false,"screenshotCount":2,"banPasteOpen":false,"noOpsSubOpen":false,"noOpsSubTime":120,"entriesLimitOpen":false,"entriesCount":3,"entriesTipsOpen":false,"entriesTxtType":0,"triggerTipsOpen":false,"triggerType":0,"triggerTxtType":0}}',
        "questionOther": '{"st":{"scs":1,"cscs":1,"mcs":1,"cmcs":1,"fibs":1,"cfibs":1,"tofs":1,"ctofs":1,"sas":1,"csas":1,"ls":1,"cls":1},"questionScoreList":[],"customTypeScoreList":[]}',
        "classifyIdList": "[]",
        "isCusAgreement": "false",
        "isOpenAgreement": "false",
        "agreementId": "0",
        "agreementName": "",
        "version": "V2",
        "pic": "",
        "questionList": '[{"id":77615,"stem":"<p style=\\"line-height:1.5em;\\">123</p>","type":0,"content":{"t":-1,"ol":[{"id":1,"v":"<p style=\\"line-height:1.5em;\\">12</p>","r":true,"picUrl":""},{"id":2,"v":"<p style=\\"line-height:1.5em;\\">434</p>","r":false,"picUrl":""}]},"answerAnalysis":"","groupIdList":[0],"createTime":1767777575000,"updateTime":1767777575000,"status":0,"oldId":77615,"examSiteIdList":[],"difficulty":3,"customTypeId":0,"flag":0,"customTypeName":"单选题","snapshot":false,"examSiteInfo":[],"groupInfo":[{"id":0,"name":"默认分类"}],"title":"123","key":"77615"},{"id":77614,"stem":"<p style=\\"line-height:1.5em;\\">11</p>","type":4,"content":{"p":false},"answerAnalysis":"<p style=\\"line-height:1.5em;\\">11</p>","groupIdList":[0],"createTime":1767777567000,"updateTime":1767777567000,"status":0,"oldId":77614,"examSiteIdList":[],"difficulty":3,"customTypeId":4,"flag":0,"customTypeName":"简答题","snapshot":false,"examSiteInfo":[],"groupInfo":[{"id":0,"name":"默认分类"}],"title":"11","key":"77614"}]',
    }


def build_add_audio_payload(audio_name: str, summary: str, file_id: str, wxapp_id: str) -> Dict[str, Any]:
    return {
        "wxappId": wxapp_id,
        "name": audio_name,
        "summary": summary,
        "content": "<p>音频内容描述</p>",
        "fileId": file_id,
        "picIdList": "[]",
        "classifyIdList": "[]",
        "tdk": '{"t":"","d":"","k":""}',
        "setting": '{"bp":0,"bml":1,"btype":0,"bmtgs":[],"pageStyle":1,"pfk":{"ss":false,"pm":0,"pa":0.01,"sst":0,"vsu":0,"atm":0,"duration":0,"asp":0,"lp":0.01,"slp":0,"validityType":0,"validityDate":""},"fdl":{"s":0,"ip":0,"fil":[],"viewType":0}}',
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
    }


def build_default_task_list() -> List[Dict[str, Any]]:
    """生成默认 3 个任务配置，供作业/打卡用例复用。"""
    _requirement = {
        "t": {"c": False, "mc": 1},
        "i": {"c": False, "mc": 1},
        "audio": {"c": False, "mc": 1},
        "video": {"c": False, "mc": 1},
        "completeQuestion": {"c": False, "mc": 1},
        "linkQuestion": {"link": [], "isOpen": False},
    }
    return [
        {"id": i, "name": str(i), "rule": f'<p style="line-height:1.5em;">{i}</p>',
         "sequence": f"{i:02d}", "dailyCount": 0, "requirement": {**_requirement},
         "passCount": 0, "taskCount": 0, "isNewAdd": True}
        for i in range(1, 4)
    ]

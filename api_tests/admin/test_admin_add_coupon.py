"""
用例 ID: 1150695810001062403
用例名称: 管理后台正常添加优惠券

接口: POST /ajax/coupon_h.jsp?cmd=addCoupon
"""
import json
import time


def test_admin_add_coupon(admin_client, timestamp):
    """管理后台正常添加优惠券"""
    # Arrange: 准备测试数据
    # 优惠券名称不能超过10字符（3+6=9）
    coupon_name = f"券{timestamp}"
    
    # 计算时间戳（开始时间和结束时间）
    start_time = int(time.time() * 1000)
    end_time = start_time + (365 * 24 * 60 * 60 * 1000)  # 1年后
    
    # entries: 适用范围配置
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
        {"type": 15, "selected": True, "name": "课外服务", "suitableTarget": {"suitableType": 0, "category": 0, "selectedIdList": [], "selectedClassifyIdList": []}}
    ]
    
    # Act: 创建优惠券
    result = admin_client.post(
        "/ajax/coupon_h.jsp",
        params={"cmd": "addCoupon"},
        data={
            "wxappId": admin_client.wxapp_id,
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
        },
    )
    
    # Assert: 验证创建成功
    admin_client.assert_success(result, "添加优惠券失败")
    coupon_id = result.get("coupon", {}).get("id") or result.get("id")
    assert coupon_id, "优惠券创建失败"

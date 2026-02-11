"""
业务常量和枚举定义

统一管理项目中的常量，避免魔法值散落在代码中
"""
from enum import IntEnum


# ===================================
# 服务类型枚举
# ===================================

class ServiceType(IntEnum):
    """服务类型枚举"""
    COLUMN = 5          # 系列课
    NEWS = 6            # 图文
    VIDEO = 7           # 视频
    AUDIO = 8           # 音频
    EBOOK = 9           # 电子书
    EVALUATION = 10     # 测评
    CHECKPOINT = 11     # 打卡
    QUESTION_BANK = 12  # 超级题库
    OFFLINE_COURSE = 13 # 线下课
    BOOK_SERVICE = 14   # 课外服务
    PRODUCT = 15        # 实物商品
    FORM = 16           # 表单
    COUPON = 17         # 优惠券
    REDEMPTION_CODE = 18 # 兑换码
    HOMEWORK = 19       # 作业
    ANSWER_ACTIVITY = 20 # 答题活动


# ===================================
# 支付类型枚举
# ===================================

class PayType(IntEnum):
    """支付类型枚举"""
    WECHAT = 1          # 微信支付
    ALIPAY = 2          # 支付宝
    BALANCE = 3         # 余额支付
    OFFLINE = 4         # 线下支付
    FREE = 5            # 免费（0元购）


# ===================================
# 客户端来源枚举
# ===================================

class ClientFrom(IntEnum):
    """客户端来源枚举"""
    ADMIN = 1           # 管理后台
    PC = 2              # PC端
    H5 = 3              # H5端
    EDUPC = 4           # EduPC端
    MINIPROGRAM = 5     # 小程序


# ===================================
# 订单状态枚举
# ===================================

class OrderStatus(IntEnum):
    """订单状态枚举"""
    PENDING = 0         # 待支付
    PAID = 1            # 已支付
    CANCELLED = 2       # 已取消
    REFUNDED = 3        # 已退款
    PARTIAL_REFUND = 4  # 部分退款


# ===================================
# 退款类型枚举
# ===================================

class RefundType(IntEnum):
    """退款类型枚举"""
    FULL = 1            # 全额退款
    PARTIAL = 2         # 部分退款


# ===================================
# 退款方式枚举
# ===================================

class RefundMethod(IntEnum):
    """退款方式枚举"""
    ORIGINAL = 1        # 原路退回
    BALANCE = 2         # 退到余额
    OFFLINE = 3         # 线下退款


# ===================================
# HTTP 请求头常量
# ===================================

class HttpHeaders:
    """HTTP 请求头常量"""
    CONTENT_TYPE_FORM = "application/x-www-form-urlencoded; charset=UTF-8"
    CONTENT_TYPE_JSON = "application/json; charset=UTF-8"
    X_REQUESTED_WITH = "XMLHttpRequest"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


# ===================================
# API 路径常量
# ===================================

class ApiPath:
    """API 路径常量"""
    
    # 管理后台
    ADMIN_LOGIN = "/ajax/login_h.jsp"
    ADMIN_ADD_AUDIO = "/ajax/wxAppAudio_h.jsp"
    ADMIN_ADD_VIDEO = "/ajax/video_h.jsp"
    ADMIN_ADD_NEWS = "/ajax/wxAppNews_h.jsp"
    ADMIN_ADD_COLUMN = "/ajax/wxAppColumn_h.jsp"
    ADMIN_GET_ORDER_DETAIL = "/api/manage/order/v2/getOrderDetails"
    ADMIN_REFUND_ORDER = "/api/manage/refund/refundOrder"
    
    # EduPC端
    EDUPC_LOGIN = "/ajax/login_h.jsp"
    EDUPC_COMMIT_ORDER = "/api/guestAuth/pcOrder/v2/commitOrder"
    
    # H5端
    H5_LOGIN = "/ajax/login_h.jsp"
    H5_COMMIT_ORDER = "/api/guestAuth/order/v2/commitOrder"


# ===================================
# 默认值常量
# ===================================

class DefaultValues:
    """默认值常量"""
    
    # 超时时间
    DEFAULT_TIMEOUT = 30  # 秒
    
    # 延时配置
    DEFAULT_RATE_LIMIT_SECONDS = 2  # 秒
    
    # TAPD 配置
    TAPD_REPORT_INTERVAL = 0.3  # 秒
    
    # 学员信息
    DEFAULT_STU_ID = "57711"
    DEFAULT_UNION_USER_ID = "57655"
    
    # 应用信息
    DEFAULT_WXAPP_AID = "3444128"
    DEFAULT_WXAPP_ID = "110"
    DEFAULT_AID = "31687084"
    
    # 价格
    MIN_PRICE = 0.01  # 最小价格（元）
    
    # 有效期
    DEFAULT_VALIDITY_DAYS = 365  # 天


# ===================================
# 业务规则常量
# ===================================

class BusinessRules:
    """业务规则常量"""
    
    # 需要退款的服务类型
    NEED_REFUND_SERVICES = [
        ServiceType.COLUMN,
        ServiceType.NEWS,
        ServiceType.AUDIO,
        ServiceType.VIDEO,
        ServiceType.EBOOK,
        ServiceType.EVALUATION,
        ServiceType.QUESTION_BANK,
        ServiceType.CHECKPOINT,
    ]
    
    # 需要核销的服务类型
    NEED_WRITE_OFF_SERVICES = [
        ServiceType.PRODUCT,
    ]
    
    # 不需要清理的服务类型
    NO_CLEANUP_SERVICES = [
        ServiceType.OFFLINE_COURSE,
        ServiceType.BOOK_SERVICE,
    ]


# ===================================
# 测试标记常量
# ===================================

class TestMarks:
    """pytest 测试标记常量"""
    WRITE = "write"                 # 写操作（需要延时）
    RATE_LIMITED = "rate_limited"   # 限频操作（需要延时）
    SMOKE = "smoke"                 # 冒烟测试
    SLOW = "slow"                   # 慢速测试
    SKIP = "skip"                   # 跳过测试

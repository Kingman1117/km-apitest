"""
Actions层 - 业务动作复用

负责：
- 封装可复用的业务动作
- 统一业务断言和数据提取
- 隐藏接口细节
- 提供简洁的业务API供Test层调用
"""
from .order_actions import OrderActions
from .refund_actions import RefundActions
from .audio_actions import AudioActions
from .video_actions import VideoActions
from .news_actions import NewsActions
from .column_actions import ColumnActions

__all__ = [
    'OrderActions',
    'RefundActions',
    'AudioActions',
    'VideoActions',
    'NewsActions',
    'ColumnActions',
]

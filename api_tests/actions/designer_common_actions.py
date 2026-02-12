"""
设计器通用业务动作

封装 EduPC 设计器和移动端设计器的共用逻辑。
"""
import time


class DesignerCommonActions:
    """设计器通用业务动作"""

    @staticmethod
    def build_unique_column_name(prefix: str = "设测") -> str:
        """
        生成不超过 8 个字符的栏目名。
        默认格式: 设测 + 6位时间尾号
        """
        suffix = f"{int(time.time()) % 1000000:06d}"
        name = f"{prefix}{suffix}"
        return name[:8]

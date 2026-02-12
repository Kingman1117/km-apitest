"""日期工具函数"""
from datetime import datetime, timedelta


def future_date(days: int = 365) -> str:
    """
    生成未来日期字符串（默认1年后），格式 YYYY-MM-DD
    
    Args:
        days: 未来天数，默认365天（1年）
        
    Returns:
        日期字符串，格式: YYYY-MM-DD
        
    Examples:
        >>> future_date()  # 1年后
        '2027-02-12'
        >>> future_date(30)  # 30天后
        '2026-03-14'
    """
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

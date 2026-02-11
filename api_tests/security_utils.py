"""
安全相关通用工具。
"""
import hashlib


def md5(text: str) -> str:
    """返回字符串的 MD5 十六进制摘要。"""
    return hashlib.md5(text.encode()).hexdigest()

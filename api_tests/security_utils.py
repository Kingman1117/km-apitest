"""
安全相关通用工具。
"""
import hashlib


def md5(text: str) -> str:
    """返回字符串的 MD5 十六进制摘要（用于登录密码加密等场景）。"""
    return hashlib.md5(text.encode()).hexdigest()

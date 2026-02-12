"""
日志脱敏与体积治理工具。

企业级敏感信息保护：
- 按 key 名匹配脱敏（token、password 等）
- 按 value 正则匹配脱敏（手机号、身份证、银行卡等）
- 嵌套 JSON 字符串自动解析脱敏
- 可配置的日志体积控制
"""
import json
import os
import re
from typing import Any, Dict, List, Optional, Set, Tuple

# ============================================================
# 配置项（可通过环境变量覆盖）
# ============================================================

# 日志片段长度上限（字符数）
LOG_SNIPPET_LIMIT = int(os.getenv("LOG_SNIPPET_LIMIT", "500"))

# 单个字段值长度上限
LOG_FIELD_VALUE_LIMIT = int(os.getenv("LOG_FIELD_VALUE_LIMIT", "200"))

# 列表元素最大展示数
LOG_LIST_MAX_ITEMS = int(os.getenv("LOG_LIST_MAX_ITEMS", "3"))

# 是否启用 value 正则脱敏（性能敏感场景可关闭）
ENABLE_VALUE_PATTERN_MASK = os.getenv("LOG_VALUE_PATTERN_MASK", "1") == "1"

# 脱敏占位符
MASK_PLACEHOLDER = "***"

# ============================================================
# 敏感 key 名（大小写不敏感）
# ============================================================

SENSITIVE_KEYS: Set[str] = {
    # 认证相关
    "token", "_token", "access_token", "refresh_token", "id_token",
    "authorization", "auth", "bearer",
    "password", "pwd", "passwd", "secret", "api_key", "apikey",
    "cookie", "session", "sessionid", "jsessionid",
    # 个人隐私
    "phone", "mobile", "tel", "telephone", "cellphone",
    "email", "mail",
    "idcard", "id_card", "idno", "id_no", "sfz", "sfzh",
    "bankcard", "bank_card", "cardno", "card_no",
    "realname", "real_name", "truename", "true_name",
    "address", "addr",
    # 支付相关
    "cvv", "cvv2", "cvc", "securitycode",
    "expiry", "expire", "validdate",
    # 其他
    "credential", "credentials",
    "private", "privatekey", "private_key",
}

# ============================================================
# 敏感 value 正则模式（用于检测未按敏感 key 命名的字段）
# ============================================================

_PHONE_PATTERN = re.compile(r"1[3-9]\d{9}")
_IDCARD_PATTERN = re.compile(r"\d{17}[\dXx]")
_BANKCARD_PATTERN = re.compile(r"\d{16,19}")
_EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

# (pattern, mask_func) - mask_func 接收 match 对象，返回脱敏后的字符串
_VALUE_PATTERNS: List[Tuple[re.Pattern, Any]] = [
    # 手机号：保留前3后4
    (_PHONE_PATTERN, lambda m: m.group()[:3] + "****" + m.group()[-4:]),
    # 身份证：保留前4后4
    (_IDCARD_PATTERN, lambda m: m.group()[:4] + "**********" + m.group()[-4:]),
    # 银行卡：保留前4后4
    (_BANKCARD_PATTERN, lambda m: m.group()[:4] + "****" + m.group()[-4:]),
    # 邮箱：保留首字母和@后域名
    (_EMAIL_PATTERN, lambda m: m.group()[0] + "***@" + m.group().split("@")[-1]),
]


def _is_sensitive_key(key: str) -> bool:
    """检查 key 是否为敏感字段（大小写不敏感）。"""
    key_lower = key.lower().replace("-", "").replace("_", "")
    for sensitive in SENSITIVE_KEYS:
        if sensitive.replace("_", "") in key_lower:
            return True
    return False


def _mask_value_patterns(value: str) -> str:
    """对 value 中的敏感模式进行脱敏。"""
    if not ENABLE_VALUE_PATTERN_MASK:
        return value
    result = value
    for pattern, mask_fn in _VALUE_PATTERNS:
        result = pattern.sub(mask_fn, result)
    return result


def _try_parse_json_string(value: str) -> Optional[Any]:
    """尝试将字符串解析为 JSON（用于处理嵌套 JSON 字符串如 itemList）。"""
    if not value or len(value) < 2:
        return None
    stripped = value.strip()
    if not (stripped.startswith("{") or stripped.startswith("[")):
        return None
    try:
        return json.loads(stripped)
    except (json.JSONDecodeError, ValueError):
        return None


def sanitize(value: Any, depth: int = 0) -> Any:
    """
    递归脱敏处理。
    
    Args:
        value: 任意值
        depth: 当前递归深度（防止无限递归）
        
    Returns:
        脱敏后的值
    """
    if depth > 10:
        return "[max_depth_exceeded]"
    
    if value is None:
        return None
    
    if isinstance(value, dict):
        result = {}
        for k, v in value.items():
            key_str = str(k)
            if _is_sensitive_key(key_str):
                result[k] = MASK_PLACEHOLDER
            else:
                result[k] = sanitize(v, depth + 1)
        return result
    
    if isinstance(value, (list, tuple)):
        items = list(value)
        sanitized_items = [sanitize(item, depth + 1) for item in items[:LOG_LIST_MAX_ITEMS]]
        if len(items) > LOG_LIST_MAX_ITEMS:
            sanitized_items.append(f"...+{len(items) - LOG_LIST_MAX_ITEMS} more")
        return sanitized_items if isinstance(value, list) else tuple(sanitized_items)
    
    if isinstance(value, str):
        # 尝试解析嵌套 JSON 字符串
        parsed = _try_parse_json_string(value)
        if parsed is not None:
            sanitized_nested = sanitize(parsed, depth + 1)
            # 返回脱敏后的 JSON 字符串
            try:
                return json.dumps(sanitized_nested, ensure_ascii=False)
            except Exception:
                pass
        
        # 普通字符串：value 正则脱敏 + 截断
        masked = _mask_value_patterns(value)
        if len(masked) > LOG_FIELD_VALUE_LIMIT:
            return masked[:LOG_FIELD_VALUE_LIMIT] + "...(truncated)"
        return masked
    
    if isinstance(value, (int, float, bool)):
        return value
    
    # 其他类型转字符串处理
    str_value = str(value)
    if len(str_value) > LOG_FIELD_VALUE_LIMIT:
        return str_value[:LOG_FIELD_VALUE_LIMIT] + "...(truncated)"
    return str_value


def build_snippet(text: str, limit: Optional[int] = None) -> str:
    """
    构建响应片段（用于日志展示）。
    
    Args:
        text: 原始响应文本
        limit: 截断长度，默认使用 LOG_SNIPPET_LIMIT
        
    Returns:
        截断后的文本
    """
    if not text:
        return "[empty]"
    
    max_len = limit or LOG_SNIPPET_LIMIT
    compact = text.strip()
    
    if len(compact) <= max_len:
        return compact
    
    return compact[:max_len] + f"...(truncated, total={len(compact)})"


def sanitize_response_text(text: str) -> str:
    """
    对响应体文本进行脱敏。
    
    Args:
        text: 原始响应文本
        
    Returns:
        脱敏后的文本片段
    """
    if not text:
        return "[empty]"
    
    # 尝试解析为 JSON 进行结构化脱敏
    parsed = _try_parse_json_string(text)
    if parsed is not None:
        sanitized = sanitize(parsed)
        try:
            result = json.dumps(sanitized, ensure_ascii=False)
            return build_snippet(result)
        except Exception:
            pass
    
    # 非 JSON：直接 value 正则脱敏 + 截断
    masked = _mask_value_patterns(text)
    return build_snippet(masked)


# ============================================================
# 日志体积控制：采样与聚合
# ============================================================

class LogRateLimiter:
    """
    日志速率限制器，防止高频重复日志。
    
    用法：
        limiter = LogRateLimiter(window_seconds=60, max_count=10)
        if limiter.should_log("endpoint:/api/order/commit"):
            logger.info(...)
    """
    
    def __init__(self, window_seconds: int = 60, max_count: int = 10):
        self.window_seconds = window_seconds
        self.max_count = max_count
        self._counters: Dict[str, List[float]] = {}
    
    def should_log(self, key: str) -> bool:
        """判断是否应该记录此日志。"""
        import time
        now = time.time()
        
        if key not in self._counters:
            self._counters[key] = []
        
        # 清理过期记录
        window_start = now - self.window_seconds
        self._counters[key] = [t for t in self._counters[key] if t > window_start]
        
        # 检查是否超限
        if len(self._counters[key]) >= self.max_count:
            return False
        
        self._counters[key].append(now)
        return True
    
    def get_suppressed_count(self, key: str) -> int:
        """获取被抑制的日志数量（用于定期汇总输出）。"""
        # 简化实现：返回窗口内超出 max_count 的数量
        if key not in self._counters:
            return 0
        return max(0, len(self._counters[key]) - self.max_count)


# 全局速率限制器实例
_default_limiter = LogRateLimiter(window_seconds=60, max_count=20)


def should_log_request(endpoint: str) -> bool:
    """判断是否应该记录此请求日志（用于高频接口采样）。"""
    return _default_limiter.should_log(f"req:{endpoint}")

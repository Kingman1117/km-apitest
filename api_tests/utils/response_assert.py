"""
响应访问与断言工具。

目标：
- 统一 data.xxx 这类字段访问
- 统一字段存在性/类型断言
- 提供更可读、可复用的断言失败信息
"""
import json
from typing import Any, Iterable, Optional, Tuple, Union


_MISSING = object()
_TypeLike = Union[type, Tuple[type, ...]]


def _format_response(response: Any) -> str:
    try:
        return json.dumps(response, ensure_ascii=False, indent=2)
    except Exception:
        return str(response)


def _walk_path(payload: Any, path: str) -> Any:
    """
    按点路径访问字段，支持 list 下标：
    - data.orderInfo.itemList.0.orderItemId
    """
    current = payload
    for part in path.split("."):
        if isinstance(current, dict):
            if part not in current:
                return _MISSING
            current = current[part]
            continue

        if isinstance(current, list):
            if not part.isdigit():
                return _MISSING
            idx = int(part)
            if idx < 0 or idx >= len(current):
                return _MISSING
            current = current[idx]
            continue

        return _MISSING
    return current


def get_field(response: Any, path: str, default: Any = None) -> Any:
    """安全读取字段，字段不存在时返回 default。"""
    value = _walk_path(response, path)
    return default if value is _MISSING else value


def assert_field(
    response: Any,
    path: str,
    expected_type: Optional[_TypeLike] = None,
    msg: str = "",
) -> Any:
    """
    断言字段存在，且可选地断言字段类型。
    返回字段值，便于链式使用。
    """
    value = _walk_path(response, path)
    if value is _MISSING:
        base_msg = msg or f"字段不存在: {path}"
        raise AssertionError(f"{base_msg}\n响应: {_format_response(response)}")

    if expected_type and not isinstance(value, expected_type):
        base_msg = msg or f"字段类型错误: {path}"
        raise AssertionError(
            f"{base_msg}\n期望类型: {expected_type}\n实际类型: {type(value)}\n响应: {_format_response(response)}"
        )

    return value


def assert_any_field(
    response: Any,
    paths: Iterable[str],
    expected_type: Optional[_TypeLike] = None,
    msg: str = "",
) -> Any:
    """
    断言多个候选路径中至少一个存在（并可选校验类型）。
    常用于兼容多种响应结构。
    """
    for path in paths:
        value = _walk_path(response, path)
        if value is _MISSING:
            continue
        if expected_type and not isinstance(value, expected_type):
            continue
        return value

    joined = ", ".join(paths)
    base_msg = msg or f"候选字段均不存在或类型不匹配: [{joined}]"
    raise AssertionError(f"{base_msg}\n响应: {_format_response(response)}")

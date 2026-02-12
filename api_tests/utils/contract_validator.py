"""
响应契约校验工具。

用于在 BaseClient 中对响应做可选 JSON Schema 校验。
"""
import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union


class ContractValidationError(AssertionError):
    """响应契约校验失败。"""


def _format_path(path_items) -> str:
    parts = []
    for item in list(path_items):
        if isinstance(item, int):
            if not parts:
                parts.append(f"[{item}]")
            else:
                parts[-1] = f"{parts[-1]}[{item}]"
        else:
            parts.append(str(item))
    return ".".join(parts) if parts else "$"


def _short_repr(value: Any, limit: int = 180) -> str:
    try:
        raw = json.dumps(value, ensure_ascii=False, default=str)
    except Exception:
        raw = repr(value)
    if len(raw) <= limit:
        return raw
    return raw[:limit] + "...(truncated)"


@lru_cache(maxsize=128)
def _load_schema_file(path: str) -> Dict[str, Any]:
    text = Path(path).read_text(encoding="utf-8")
    return json.loads(text)


def _resolve_schema(schema: Union[str, Dict[str, Any]]) -> Tuple[str, Dict[str, Any]]:
    if isinstance(schema, dict):
        return "<inline>", schema

    if not isinstance(schema, str) or not schema.strip():
        raise ValueError("schema 必须是非空字符串或 dict")

    schema_name = schema.strip()

    direct_path = Path(schema_name)
    if direct_path.exists():
        return direct_path.name, _load_schema_file(str(direct_path.resolve()))

    from schemas.registry import get_schema_path  # 延迟导入，避免循环依赖

    schema_path = get_schema_path(schema_name)
    return schema_name, _load_schema_file(schema_path)


def validate_contract(
    response_data: Dict[str, Any],
    schema: Optional[Union[str, Dict[str, Any]]] = None,
) -> None:
    """
    校验响应契约。schema 为空时直接跳过。

    Args:
        response_data: 响应 JSON（dict）
        schema: schema 名称（注册表 key / 文件路径）或 schema dict

    Raises:
        ContractValidationError: 校验失败
    """
    if schema is None:
        return

    schema_name, schema_obj = _resolve_schema(schema)

    try:
        from jsonschema import Draft7Validator
    except Exception as exc:
        raise ContractValidationError(
            "未安装 jsonschema 依赖，无法执行契约校验。"
            "请安装: pip install jsonschema"
        ) from exc

    validator = Draft7Validator(schema_obj)
    errors = sorted(validator.iter_errors(response_data), key=lambda e: list(e.path))
    if not errors:
        return

    first = errors[0]
    field_path = _format_path(first.path)
    expected = f"{first.validator}={first.validator_value}"
    actual_type = type(first.instance).__name__
    actual_value = _short_repr(first.instance)

    raise ContractValidationError(
        f"响应契约校验失败(schema={schema_name})\n"
        f"字段路径: {field_path}\n"
        f"规则: {first.message}\n"
        f"期望: {expected}\n"
        f"实际: type={actual_type}, value={actual_value}"
    )

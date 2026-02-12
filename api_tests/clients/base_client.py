"""
BaseClient - HTTP请求基类

提供统一的HTTP请求处理、Session管理、日志记录、重试策略
"""
import json
import logging
import os
import time
import uuid
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional, Dict, Any, Union

from utils.contract_validator import ContractValidationError, validate_contract
from utils.log_sanitizer import (
    sanitize,
    sanitize_response_text,
    build_snippet,
    should_log_request,
    LOG_SNIPPET_LIMIT,
)


logger = logging.getLogger(__name__)

# 日志级别控制（环境变量可覆盖）
# DEBUG: 完整请求/响应日志
# INFO: 仅关键节点日志
# WARNING: 仅异常日志
LOG_HTTP_LEVEL = os.getenv("LOG_HTTP_LEVEL", "INFO").upper()


class BaseClient:
    """HTTP客户端基类"""
    
    BASE_URL = ""  # 子类需要覆盖
    DEFAULT_TIMEOUT = 30  # 默认超时时间（秒）
    ENABLE_RETRY = True  # 是否启用重试（子类可覆盖）
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        self.timeout = self.DEFAULT_TIMEOUT
        
        # 配置重试策略（仅对幂等请求和特定错误码重试）
        if self.ENABLE_RETRY:
            retry_strategy = Retry(
                total=2,  # 最多重试2次
                backoff_factor=0.5,  # 重试间隔：0.5s, 1s
                status_forcelist=[502, 503, 504],  # 仅对网关错误重试
                allowed_methods=["GET", "HEAD"],  # 仅对幂等请求重试
                raise_on_status=False,  # 不自动抛异常，由我们的代码处理
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            self.session.mount("http://", adapter)
            self.session.mount("https://", adapter)
    
    @property
    def common_params(self) -> Dict[str, Any]:
        """公共参数，子类可覆盖"""
        return {}
    
    def get(
        self,
        path: str,
        params: Optional[Dict] = None,
        schema: Optional[Union[str, Dict[str, Any]]] = None,
        **kwargs
    ) -> Dict:
        """
        GET请求
        
        Args:
            path: 接口路径
            params: URL参数
            **kwargs: requests额外参数（可覆盖 timeout）
            
        Returns:
            响应字典
        """
        url = f"{self.BASE_URL}{path}"
        query = {**self.common_params, **(params or {})}
        
        # 设置默认超时，允许 kwargs 覆盖
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout

        client_request_id = self._ensure_client_request_id(kwargs)
        
        self._log_http_event(
            level="info",
            event="http.request",
            payload={
                "method": "GET",
                "url": url,
                "client_request_id": client_request_id,
                "params": self._sanitize_for_log(query),
            },
        )
        
        start_time = time.time()
        resp = self.session.get(url, params=query, **kwargs)
        elapsed_ms = int((time.time() - start_time) * 1000)
        
        return self._parse_response(
            resp,
            method="GET",
            url=url,
            params=query,
            elapsed_ms=elapsed_ms,
            schema=schema,
            client_request_id=client_request_id,
        )
    
    def post(
        self,
        path: str,
        data=None,
        params: Optional[Dict] = None,
        schema: Optional[Union[str, Dict[str, Any]]] = None,
        **kwargs
    ) -> Dict:
        """
        POST请求
        
        Args:
            path: 接口路径
            data: POST数据（dict或str）
            params: URL参数
            **kwargs: requests额外参数（可覆盖 timeout）
            
        Returns:
            响应字典
        """
        url = f"{self.BASE_URL}{path}"
        query = {**self.common_params, **(params or {})}
        
        # 设置默认超时，允许 kwargs 覆盖
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout

        client_request_id = self._ensure_client_request_id(kwargs)
        
        self._log_http_event(
            level="info",
            event="http.request",
            payload={
                "method": "POST",
                "url": url,
                "client_request_id": client_request_id,
                "params": self._sanitize_for_log(query),
                "data": self._sanitize_for_log(data),
            },
        )
        
        start_time = time.time()
        resp = self.session.post(url, data=data, params=query, **kwargs)
        elapsed_ms = int((time.time() - start_time) * 1000)
        
        return self._parse_response(
            resp,
            method="POST",
            url=url,
            params=query,
            data=data,
            elapsed_ms=elapsed_ms,
            schema=schema,
            client_request_id=client_request_id,
        )
    
    def _parse_response(
        self, 
        resp: requests.Response, 
        method: str = "UNKNOWN",
        url: str = "",
        params: Optional[Dict] = None,
        data: Any = None,
        elapsed_ms: int = 0,
        schema: Optional[Union[str, Dict[str, Any]]] = None,
        client_request_id: str = "",
    ) -> Dict:
        """
        解析响应（带HTTP状态码硬断言和结构化错误信息）
        
        Args:
            resp: requests响应对象
            method: HTTP方法（用于日志）
            url: 请求URL（用于日志）
            params: 请求参数（用于日志）
            data: 请求数据（用于日志）
            elapsed_ms: 请求耗时（毫秒）
            
        Returns:
            响应字典
            
        Raises:
            requests.HTTPError: 当HTTP状态码非2xx时
        """
        status_code = resp.status_code
        text = resp.text.strip()
        
        trace_id = self._extract_trace_id(resp)
        server_request_id = (
            resp.headers.get("X-Request-Id")
            or resp.headers.get("x-request-id")
            or ""
        )
        request_id = server_request_id or client_request_id or trace_id or ""
        request_context = {
            "method": method,
            "url": url,
            "params": self._sanitize_for_log(params),
            "data": self._sanitize_for_log(data),
            "client_request_id": client_request_id or "N/A",
        }
        
        # P0-1: HTTP状态码硬断言 - 非2xx直接抛出结构化错误
        if not resp.ok:  # status_code < 200 or >= 300
            self._log_http_event(
                level="error",
                event="http.response.error",
                payload={
                    "trace_id": trace_id or "N/A",
                    "request_id": request_id or "N/A",
                    "client_request_id": client_request_id or "N/A",
                    "server_request_id": server_request_id or "N/A",
                    "status_code": status_code,
                    "elapsed_ms": elapsed_ms,
                    "request": request_context,
                    "response_snippet": self._build_response_snippet(text),
                },
            )
            
            # 抛出包含完整诊断信息的异常
            error_msg = (
                f"HTTP {status_code} Error\n"
                f"Method: {method}\n"
                f"URL: {url}\n"
                f"Elapsed: {elapsed_ms}ms\n"
                f"TraceId: {trace_id or 'N/A'}\n"
                f"Response: {self._build_response_snippet(text)}"
            )
            raise requests.HTTPError(error_msg, response=resp)
        
        # 处理空响应（某些删除接口可能返回空）
        if not text:
            logger.info(
                "HTTP请求成功（空响应）[%s %s] status=%d elapsed=%dms",
                method, url, status_code, elapsed_ms
            )
            return {"success": True}
        
        # 解析JSON
        try:
            result = json.loads(text)
            
            if not trace_id:
                trace_id = self._extract_trace_id(resp, result)
            if not server_request_id:
                server_request_id = self._extract_request_id(resp, result)
            request_id = server_request_id or client_request_id or trace_id or ""

            should_validate_schema = not (
                isinstance(result, dict) and result.get("success") is False
            )

            if schema is not None and should_validate_schema:
                try:
                    validate_contract(result, schema=schema)
                except ContractValidationError:
                    self._log_http_event(
                        level="error",
                        event="http.contract.error",
                        payload={
                            "trace_id": trace_id or "N/A",
                            "request_id": request_id or "N/A",
                            "client_request_id": client_request_id or "N/A",
                            "server_request_id": server_request_id or "N/A",
                            "status_code": status_code,
                            "elapsed_ms": elapsed_ms,
                            "schema": schema if isinstance(schema, str) else "<inline>",
                            "request": request_context,
                            "response_snippet": self._build_response_snippet(text),
                        },
                    )
                    raise

            self._log_http_event(
                level="info",
                event="http.response",
                payload={
                    "trace_id": trace_id or "N/A",
                    "request_id": request_id or "N/A",
                    "client_request_id": client_request_id or "N/A",
                    "server_request_id": server_request_id or "N/A",
                    "status_code": status_code,
                    "elapsed_ms": elapsed_ms,
                    "request": request_context,
                    "response_snippet": self._build_response_snippet(text),
                    "success": result.get("success", "unknown"),
                    "schema": schema if isinstance(schema, str) else None,
                },
            )
            
            return result
            
        except json.JSONDecodeError as e:
            self._log_http_event(
                level="error",
                event="http.response.json_decode_error",
                payload={
                    "trace_id": trace_id or "N/A",
                    "request_id": request_id or "N/A",
                    "client_request_id": client_request_id or "N/A",
                    "server_request_id": server_request_id or "N/A",
                    "status_code": status_code,
                    "elapsed_ms": elapsed_ms,
                    "error": str(e),
                    "request": request_context,
                    "response_snippet": self._build_response_snippet(text),
                },
            )
            
            # 返回结构化错误而不是直接抛异常（保持向后兼容）
            return {
                "success": False,
                "error": f"JSON解析失败: {str(e)}",
                "response_preview": text[:500],
                "status_code": status_code,
            }

    def _extract_trace_id(
        self,
        resp: requests.Response,
        response_json: Optional[Dict[str, Any]] = None,
    ) -> str:
        candidates = [
            "X-Trace-Id",
            "x-trace-id",
            "X-Request-Id",
            "x-request-id",
            "Trace-Id",
            "trace-id",
        ]
        for key in candidates:
            value = resp.headers.get(key)
            if value:
                return str(value)

        if isinstance(response_json, dict):
            for key in ("traceId", "trace_id", "requestId", "request_id"):
                value = response_json.get(key)
                if value:
                    return str(value)
            data = response_json.get("data")
            if isinstance(data, dict):
                for key in ("traceId", "trace_id", "requestId", "request_id"):
                    value = data.get(key)
                    if value:
                        return str(value)

        return ""

    def _extract_request_id(
        self,
        resp: requests.Response,
        response_json: Optional[Dict[str, Any]] = None,
    ) -> str:
        candidates = [
            "X-Request-Id",
            "x-request-id",
            "Request-Id",
            "request-id",
        ]
        for key in candidates:
            value = resp.headers.get(key)
            if value:
                return str(value)

        if isinstance(response_json, dict):
            for key in ("requestId", "request_id"):
                value = response_json.get(key)
                if value:
                    return str(value)
            data = response_json.get("data")
            if isinstance(data, dict):
                for key in ("requestId", "request_id"):
                    value = data.get(key)
                    if value:
                        return str(value)

        return ""

    def _ensure_client_request_id(self, request_kwargs: Dict[str, Any]) -> str:
        headers = request_kwargs.get("headers")
        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        client_request_id = headers.get("X-Client-Request-Id")
        if not client_request_id:
            client_request_id = uuid.uuid4().hex
            headers["X-Client-Request-Id"] = client_request_id

        request_kwargs["headers"] = headers
        return str(client_request_id)

    def _build_response_snippet(self, text: str) -> str:
        """构建响应片段（带脱敏）。"""
        return sanitize_response_text(text)

    def _sanitize_for_log(self, value: Any) -> Any:
        """递归脱敏日志数据（委托给 log_sanitizer）。"""
        return sanitize(value)

    def _log_http_event(self, level: str, event: str, payload: Dict[str, Any]) -> None:
        """
        记录 HTTP 事件日志（带体积控制）。
        
        - LOG_HTTP_LEVEL=WARNING 时，仅输出 error 级别日志
        - LOG_HTTP_LEVEL=INFO 时，输出 info 及以上日志
        - LOG_HTTP_LEVEL=DEBUG 时，输出所有日志
        - 高频请求自动采样（60秒内同一 endpoint 最多 20 条）
        """
        # 日志级别过滤
        level_priority = {"debug": 0, "info": 1, "warning": 2, "error": 3}
        config_priority = level_priority.get(LOG_HTTP_LEVEL.lower(), 1)
        event_priority = level_priority.get(level.lower(), 1)
        
        if event_priority < config_priority:
            return
        
        # 高频请求采样（仅对成功响应进行采样，错误始终记录）
        if level.lower() == "info" and event == "http.response":
            url = payload.get("request", {}).get("url", "")
            if url and not should_log_request(url):
                return
        
        message = json.dumps(
            {"event": event, **payload},
            ensure_ascii=False,
            default=str,
        )
        log_fn = getattr(logger, level, logger.info)
        log_fn(message)
    
    def assert_success(self, response: Dict, error_msg: str = "API调用失败") -> Dict:
        """
        统一的成功断言
        
        Args:
            response: API响应
            error_msg: 失败时的错误消息
            
        Returns:
            原响应（支持链式调用）
        """
        assert response.get("success") is True, \
            f"{error_msg}\n响应: {json.dumps(response, ensure_ascii=False, indent=2)}"
        return response
    
    def extract_id(self, response: Dict, id_field: str = "id", data_path: Optional[str] = None) -> Any:
        """
        提取ID字段
        
        Args:
            response: API响应
            id_field: ID字段名
            data_path: data字段路径，如"data"或None（直接从响应提取）
            
        Returns:
            ID值
        """
        if data_path:
            data = response.get(data_path, {})
        else:
            data = response
        
        if isinstance(data, dict):
            resource_id = data.get(id_field)
        else:
            resource_id = response.get(id_field)
        
        assert resource_id, \
            f"未找到{id_field}字段\n响应: {json.dumps(response, ensure_ascii=False, indent=2)}"
        
        return resource_id

"""
BaseClient - HTTP请求基类

提供统一的HTTP请求处理、Session管理、日志记录、重试策略
"""
import json
import logging
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional, Dict, Any


logger = logging.getLogger(__name__)


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
    
    def get(self, path: str, params: Optional[Dict] = None, **kwargs) -> Dict:
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
        
        logger.debug("GET %s", url)
        logger.debug("Params: %s", query)
        
        start_time = time.time()
        resp = self.session.get(url, params=query, **kwargs)
        elapsed_ms = int((time.time() - start_time) * 1000)
        
        return self._parse_response(resp, method="GET", url=url, params=query, elapsed_ms=elapsed_ms)
    
    def post(self, path: str, data=None, params: Optional[Dict] = None, **kwargs) -> Dict:
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
        
        logger.debug("POST %s", url)
        logger.debug("Params: %s", query)
        logger.debug("Data: %s", data if not isinstance(data, str) else "[string data]")
        
        start_time = time.time()
        resp = self.session.post(url, data=data, params=query, **kwargs)
        elapsed_ms = int((time.time() - start_time) * 1000)
        
        return self._parse_response(resp, method="POST", url=url, params=query, data=data, elapsed_ms=elapsed_ms)
    
    def _parse_response(
        self, 
        resp: requests.Response, 
        method: str = "UNKNOWN",
        url: str = "",
        params: Optional[Dict] = None,
        data: Any = None,
        elapsed_ms: int = 0
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
        
        # 提取 traceId/requestId（如果存在）
        trace_id = resp.headers.get("X-Trace-Id") or resp.headers.get("X-Request-Id", "")
        
        # P0-1: HTTP状态码硬断言 - 非2xx直接抛出结构化错误
        if not resp.ok:  # status_code < 200 or >= 300
            error_context = {
                "method": method,
                "url": url,
                "status_code": status_code,
                "elapsed_ms": elapsed_ms,
                "trace_id": trace_id,
                "response_preview": text[:500] if text else "[empty response]",
                "params": params,
            }
            
            # P0-3: 失败时使用 ERROR 级别日志
            logger.error(
                "HTTP请求失败 [%s %s] status=%d elapsed=%dms trace_id=%s\n"
                "响应预览: %s\n"
                "请求参数: %s",
                method, url, status_code, elapsed_ms, trace_id or "N/A",
                text[:500] if text else "[empty]",
                json.dumps(params, ensure_ascii=False) if params else "N/A"
            )
            
            # 抛出包含完整诊断信息的异常
            error_msg = (
                f"HTTP {status_code} Error\n"
                f"Method: {method}\n"
                f"URL: {url}\n"
                f"Elapsed: {elapsed_ms}ms\n"
                f"TraceId: {trace_id or 'N/A'}\n"
                f"Response: {text[:500] if text else '[empty]'}"
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
            
            # P0-3: 成功时使用 INFO 级别记录关键信息
            logger.info(
                "HTTP请求成功 [%s %s] status=%d elapsed=%dms trace_id=%s success=%s",
                method, url, status_code, elapsed_ms, trace_id or "N/A",
                result.get("success", "unknown")
            )
            
            return result
            
        except json.JSONDecodeError as e:
            # P0-3: JSON解析失败时使用 ERROR 级别
            logger.error(
                "JSON解析失败 [%s %s] status=%d elapsed=%dms\n"
                "错误: %s\n"
                "响应内容: %s",
                method, url, status_code, elapsed_ms, str(e), text[:500]
            )
            
            # 返回结构化错误而不是直接抛异常（保持向后兼容）
            return {
                "success": False,
                "error": f"JSON解析失败: {str(e)}",
                "response_preview": text[:500],
                "status_code": status_code,
            }
    
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

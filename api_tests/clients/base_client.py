"""
BaseClient - HTTP请求基类

提供统一的HTTP请求处理、Session管理、日志记录
"""
import json
import logging
import requests
from typing import Optional, Dict, Any


logger = logging.getLogger(__name__)


class BaseClient:
    """HTTP客户端基类"""
    
    BASE_URL = ""  # 子类需要覆盖
    DEFAULT_TIMEOUT = 30  # 默认超时时间（秒）
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        self.timeout = self.DEFAULT_TIMEOUT
    
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
        
        resp = self.session.get(url, params=query, **kwargs)
        return self._parse_response(resp)
    
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
        
        resp = self.session.post(url, data=data, params=query, **kwargs)
        return self._parse_response(resp)
    
    @staticmethod
    def _parse_response(resp: requests.Response) -> Dict:
        """
        解析响应
        
        Args:
            resp: requests响应对象
            
        Returns:
            响应字典
        """
        text = resp.text.strip()
        
        # 处理空响应（某些删除接口可能返回空）
        if not text:
            # 如果HTTP状态码是200，认为成功
            if resp.status_code == 200:
                return {"success": True}
            else:
                return {"success": False, "error": f"HTTP {resp.status_code}"}
        
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            logger.error("JSON解析失败: %s", e)
            logger.error("响应内容: %s", text[:500])
            raise
    
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

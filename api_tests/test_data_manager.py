"""
测试数据管理器

统一管理测试数据，避免硬编码
"""
import json
import logging
import copy
from pathlib import Path
from typing import Dict, Any, Optional


logger = logging.getLogger(__name__)


class TestDataManager:
    """测试数据管理器"""
    
    __test__ = False  # 告诉pytest这不是测试类
    
    _instance = None
    _data = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._data is None:
            self._load_data()
    
    def _load_data(self):
        """加载测试数据配置"""
        config_path = Path(__file__).parent.parent / "config" / "test_data.json"
        try:
            with open(config_path, encoding="utf-8") as f:
                self._data = json.load(f)
            logger.info("测试数据配置加载成功: %s", config_path)
        except Exception as e:
            logger.error(f"加载测试数据配置失败: {e}")
            self._data = {}
    
    @classmethod
    def get_service_data(cls, service_name: str, client_type: str) -> Dict[str, Any]:
        """
        获取服务测试数据
        
        Args:
            service_name: 服务名称（column/news/video/audio等）
            client_type: 客户端类型（edupc/h5）
            
        Returns:
            包含service_type、service_id、amount的字典
        """
        instance = cls()
        service_config = instance._data.get("services", {}).get(service_name, {})
        
        if not service_config:
            raise ValueError(f"未找到服务配置: {service_name}")
        
        client_config = service_config.get(client_type, {})
        if not client_config:
            raise ValueError(f"未找到客户端配置: {service_name}.{client_type}")
        
        return {
            "service_type": service_config.get("service_type"),
            "service_id": client_config.get("service_id"),
            "amount": client_config.get("amount")
        }
    
    @classmethod
    def get_file_id(cls, file_type: str) -> str:
        """
        获取文件ID
        
        Args:
            file_type: 文件类型（audio/video/ebook/image）
            
        Returns:
            文件ID字符串
        """
        instance = cls()
        file_id = instance._data.get("files", {}).get(file_type)
        
        if not file_id:
            raise ValueError(f"未找到文件ID配置: {file_type}")
        
        return file_id
    
    @classmethod
    def get_default(cls, key: str, fallback: Optional[str] = None) -> str:
        """
        获取默认值
        
        Args:
            key: 配置键（stu_id/union_user_id等）
            fallback: 回退值
            
        Returns:
            配置值或回退值
        """
        instance = cls()
        value = instance._data.get("defaults", {}).get(key)
        
        if value is None and fallback is None:
            raise ValueError(f"未找到默认值配置: {key}")
        
        return value or fallback

    @classmethod
    def get_order_item_template(cls, template_name: str) -> Any:
        """
        获取订单 itemList 模板（返回深拷贝，避免运行时污染配置）。

        Args:
            template_name: 模板名称（h5_book_service/h5_offline_course/h5_product）
        """
        instance = cls()
        template = instance._data.get("order_item_templates", {}).get(template_name)
        if template is None:
            raise ValueError(f"未找到订单模板配置: {template_name}")
        return copy.deepcopy(template)
    
    @classmethod
    def get_all_services(cls) -> Dict[str, Any]:
        """获取所有服务配置"""
        instance = cls()
        return instance._data.get("services", {})
    
    @classmethod
    def get_all_files(cls) -> Dict[str, str]:
        """获取所有文件ID配置"""
        instance = cls()
        return instance._data.get("files", {})
    
    @classmethod
    def get_all_defaults(cls) -> Dict[str, str]:
        """获取所有默认值配置"""
        instance = cls()
        return instance._data.get("defaults", {})

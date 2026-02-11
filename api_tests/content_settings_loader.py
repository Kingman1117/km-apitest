"""
内容配置加载器

统一加载和管理内容创建的 setting 配置
"""
import json
import logging
from pathlib import Path
from typing import Dict, Any
import copy


logger = logging.getLogger(__name__)


class ContentSettingsLoader:
    """内容配置加载器"""
    
    _instance = None
    _settings = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._settings is None:
            self._load_settings()
    
    def _load_settings(self):
        """加载内容配置"""
        config_path = Path(__file__).parent.parent / "config" / "content_settings.json"
        try:
            with open(config_path, encoding="utf-8") as f:
                self._settings = json.load(f)
            logger.debug("内容配置加载成功: %s", config_path)
        except Exception as e:
            logger.error(f"加载内容配置失败: {e}")
            self._settings = {}
    
    @classmethod
    def get_audio_setting(cls, validity_date: str = "") -> Dict[str, Any]:
        """
        获取音频默认配置（深拷贝）
        
        Args:
            validity_date: 有效期日期（YYYY-MM-DD）
            
        Returns:
            音频配置字典
        """
        instance = cls()
        setting = copy.deepcopy(instance._settings.get("audio_default_setting", {}))
        if validity_date:
            setting["pfk"]["validityDate"] = validity_date
        return setting
    
    @classmethod
    def get_video_setting(cls, validity_date: str = "") -> Dict[str, Any]:
        """
        获取视频默认配置（深拷贝）
        
        Args:
            validity_date: 有效期日期（YYYY-MM-DD）
            
        Returns:
            视频配置字典
        """
        instance = cls()
        setting = copy.deepcopy(instance._settings.get("video_default_setting", {}))
        if validity_date:
            setting["pfk"]["validityDate"] = validity_date
        return setting
    
    @classmethod
    def get_news_setting(cls) -> Dict[str, Any]:
        """
        获取图文默认配置（深拷贝）
        
        Returns:
            图文配置字典
        """
        instance = cls()
        return copy.deepcopy(instance._settings.get("news_default_setting", {}))
    
    @classmethod
    def get_column_setting(cls, validity_date: str = "") -> Dict[str, Any]:
        """
        获取系列课默认配置（深拷贝）
        
        Args:
            validity_date: 有效期日期（YYYY-MM-DD）
            
        Returns:
            系列课配置字典
        """
        instance = cls()
        setting = copy.deepcopy(instance._settings.get("column_default_setting", {}))
        if validity_date:
            setting["validityDate"] = validity_date
        return setting

"""
EduPCClient - EduPC端API客户端
"""
import logging
import os
import pickle
import time
from pathlib import Path

from .base_client import BaseClient
from security_utils import md5
from test_data_manager import TestDataManager
from constants import DefaultValues

logger = logging.getLogger(__name__)


class EduPCClient(BaseClient):
    """EduPC端API客户端"""
    
    BASE_URL = os.getenv("EDUPC_BASE_URL", "http://huaedu1-110.365hjy.com.faidev.cc")
    LOGIN_URL = f"{BASE_URL}/ajax/login_h.jsp?cmd=wafNotCk_loginAcct"
    SESSION_CACHE = Path(__file__).parent.parent / ".edupc_session_cache.pkl"
    
    def __init__(self, username: str, password: str):
        super().__init__()
        self.username = username
        self.password = password
        self._token = None
        self.stu_id = None
        self.union_user_id = None
        # 从配置读取默认值
        defaults = TestDataManager.get_all_defaults()
        self.wxapp_aid = defaults.get("wxapp_aid", DefaultValues.DEFAULT_WXAPP_AID)
        self.wxapp_id = defaults.get("wxapp_id", DefaultValues.DEFAULT_WXAPP_ID)
        self.aid = defaults.get("aid", DefaultValues.DEFAULT_AID)
    
    @property
    def common_params(self):
        """EduPC公共参数"""
        return {"_TOKEN": self._token} if self._token else {}
    
    def login(self):
        """登录EduPC端"""
        # 尝试从缓存加载
        if self._load_session_cache():
            logger.info("EduPC session 缓存加载成功: user=%s", self.username)
            return self
        
        logger.info("EduPC 开始登录: user=%s", self.username)
        pwd_md5 = md5(self.password)
        
        resp = self.session.post(
            self.LOGIN_URL,
            data={"pwd": pwd_md5, "acct": self.username},
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": f"{self.BASE_URL}/login.jsp",
            },
        )
        
        result = self._parse_response(resp)
        self.assert_success(result, "EduPC 登录失败")
        
        # 提取关键信息
        self._extract_session_info(result)
        
        # 保存缓存
        self._save_session_cache()
        logger.info("EduPC 登录成功: user=%s stuId=%s", self.username, self.stu_id)
        
        return self
    
    def _extract_session_info(self, result):
        """从登录响应中提取_TOKEN, stuId等"""
        # 从响应data中提取
        if "data" in result and isinstance(result["data"], dict):
            token_value = result["data"].get("tokenValue") or result["data"].get("_token")
            if token_value:
                self._token = token_value
            self.stu_id = result["data"].get("stuId")
        
        # 从cookies中提取
        cookies = self.session.cookies.get_dict()
        if not self._token:
            self._token = cookies.get("_USERTOKEN")
        if not self.stu_id:
            self.stu_id = cookies.get("_STUID")
        
        # 如果没有stuId，使用默认值
        if not self.stu_id:
            self.stu_id = DefaultValues.DEFAULT_STU_ID
            logger.info("EduPC 使用默认 stuId: %s", self.stu_id)
    
    def _save_session_cache(self):
        """保存session到缓存"""
        cache_data = {
            "username": self.username,  # 新增：记录用户名
            "cookies": self.session.cookies,
            "_token": self._token,
            "stu_id": self.stu_id,
            "union_user_id": self.union_user_id,
            "timestamp": time.time(),
        }
        with open(self.SESSION_CACHE, "wb") as f:
            pickle.dump(cache_data, f)
        logger.info("EduPC session 已缓存")
    
    def _load_session_cache(self):
        """从缓存加载session"""
        if not self.SESSION_CACHE.exists():
            return False
        
        try:
            with open(self.SESSION_CACHE, "rb") as f:
                cache_data = pickle.load(f)
            
            # 新增：检查用户名是否匹配
            cached_username = cache_data.get("username")
            if cached_username and cached_username != self.username:
                logger.info("EduPC session 缓存用户不匹配（缓存: %s, 当前: %s），清除缓存",
                           cached_username, self.username)
                self.SESSION_CACHE.unlink()
                return False
            
            # 检查缓存是否过期（30分钟）
            age = time.time() - cache_data["timestamp"]
            if age > 1800:
                logger.info("EduPC session 缓存已过期（%.0f 秒）", age)
                self.SESSION_CACHE.unlink()
                return False
            
            # 恢复session
            self.session.cookies.update(cache_data["cookies"])
            self._token = cache_data["_token"]
            self.stu_id = cache_data["stu_id"]
            self.union_user_id = cache_data.get("union_user_id")
            
            return True
        except Exception as e:
            logger.warning("EduPC 加载缓存失败: %s", e)
            if self.SESSION_CACHE.exists():
                self.SESSION_CACHE.unlink()
            return False

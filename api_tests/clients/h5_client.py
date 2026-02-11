"""
H5Client - H5端API客户端
"""
import logging
import os
import pickle
import time
from pathlib import Path

from .base_client import BaseClient
from security_utils import md5
from test_data_manager import TestDataManager
from constants import DefaultValues, ClientFrom

logger = logging.getLogger(__name__)


class H5Client(BaseClient):
    """H5端API客户端"""
    
    BASE_URL = os.getenv("H5_BASE_URL", "http://huaedu1-110.m.365hjy.com.faidev.cc")
    LOGIN_URL = f"{BASE_URL}/api/guest/login/login"
    SESSION_CACHE = Path(__file__).parent.parent / ".h5_session_cache.pkl"
    
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
        self.edu_aid = defaults.get("aid", DefaultValues.DEFAULT_AID)
    
    @property
    def common_params(self):
        """H5公共参数"""
        return {"edu_aid": self.edu_aid}
    
    def login(self):
        """登录H5端"""
        # 尝试从缓存加载
        if self._load_session_cache():
            logger.info("H5 session 缓存加载成功: user=%s", self.username)
            return self
        
        logger.info("H5 开始登录: user=%s", self.username)
        pwd_md5 = md5(self.password)
        
        resp = self.session.post(
            self.LOGIN_URL,
            params={"edu_aid": self.edu_aid},
            data={
                "aid": self.aid,
                "wxappId": self.wxapp_id,
                "wxappAid": self.wxapp_aid,
                "isOem": "false",
                "from": "3",
                "isModel": "false",
                "unionUserId": "0",
                "TOKEN": "",
                "edu_aid": self.edu_aid,
                "wxappAppId": "wx88cf35a9fa55948a",
                "acct": self.username,
                "pwd": pwd_md5,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": f"{self.BASE_URL}/webIndex.jsp?isRedirect=true",
            },
        )
        
        result = self._parse_response(resp)
        self.assert_success(result, "H5 登录失败")
        
        # 提取关键信息
        self._extract_session_info(result)
        
        # 保存缓存
        self._save_session_cache()
        
        token_preview = self._token[:20] if self._token else "None"
        logger.info("H5 登录成功: user=%s stuId=%s token=%s...", self.username, self.stu_id, token_preview)
        
        return self
    
    def _extract_session_info(self, result):
        """从登录响应中提取TOKEN, stuId等"""
        # H5登录后，TOKEN在data.tokenValue中
        if "data" in result and isinstance(result["data"], dict):
            self._token = result["data"].get("tokenValue") or result["data"].get("TOKEN") or result["data"].get("token")
            self.stu_id = result["data"].get("stuId")
            self.union_user_id = result["data"].get("unionUserId")
        
        # 也可能在cookies中
        cookies = self.session.cookies.get_dict()
        if not self._token:
            self._token = cookies.get("TOKEN") or cookies.get("_USERTOKEN")
        
        # stuId可能在cookies中
        if not self.stu_id:
            self.stu_id = cookies.get("_STUID")
        
        # 如果没有stuId，使用默认值
        if not self.stu_id:
            self.stu_id = DefaultValues.DEFAULT_STU_ID
            logger.info("H5 使用默认 stuId: %s", self.stu_id)
    
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
        logger.info("H5 session 已缓存")
    
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
                logger.info("H5 session 缓存用户不匹配（缓存: %s, 当前: %s），清除缓存",
                           cached_username, self.username)
                self.SESSION_CACHE.unlink()
                return False
            
            # 检查缓存是否过期（30分钟）
            age = time.time() - cache_data["timestamp"]
            if age > 1800:
                logger.info("H5 session 缓存已过期（%.0f 秒）", age)
                self.SESSION_CACHE.unlink()
                return False
            
            # 恢复session
            self.session.cookies.update(cache_data["cookies"])
            self._token = cache_data["_token"]
            self.stu_id = cache_data["stu_id"]
            self.union_user_id = cache_data.get("union_user_id")
            
            return True
        except Exception as e:
            logger.warning("H5 加载缓存失败: %s", e)
            if self.SESSION_CACHE.exists():
                self.SESSION_CACHE.unlink()
            return False

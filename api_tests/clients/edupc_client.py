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
        self.edupc_user_token = os.getenv("EDUPC_USER_TOKEN") or defaults.get("edupc_user_token")
        self.edupc_jsession_id = os.getenv("EDUPC_JSESSIONID") or defaults.get("edupc_jsession_id")
    
    @property
    def common_params(self):
        """EduPC公共参数"""
        return {"_TOKEN": self._token} if self._token else {}
    
    def login(self):
        """登录EduPC端"""
        # 尝试从缓存加载
        if self._load_session_cache():
            self._ensure_browser_answer_cookies()
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
        self._ensure_browser_answer_cookies()
        
        # 保存缓存
        self._save_session_cache()
        logger.info("EduPC 登录成功: user=%s stuId=%s", self.username, self.stu_id)
        
        return self
    
    def _extract_session_info(self, result):
        """从登录响应中提取_TOKEN, stuId, unionUserId等"""
        # 从响应data中提取
        if "data" in result and isinstance(result["data"], dict):
            token_value = (
                result["data"].get("tokenValue")
                or result["data"].get("TOKEN")
                or result["data"].get("token")
                or result["data"].get("_token")
            )
            if token_value:
                self._token = token_value
            self.stu_id = result["data"].get("stuId")
            self.union_user_id = result["data"].get("unionUserId")

        # 兜底：部分接口会把 token 放在顶层字段
        if not self._token:
            self._token = (
                result.get("tokenValue")
                or result.get("TOKEN")
                or result.get("token")
                or result.get("_TOKEN")
            )
        
        # 从cookies中提取
        cookies = self.session.cookies.get_dict()
        if not self._token:
            self._token = cookies.get("TOKEN") or cookies.get("_USERTOKEN")
        if not self.stu_id:
            self.stu_id = cookies.get("_STUID")
        
        # 如果没有stuId，使用默认值
        if not self.stu_id:
            self.stu_id = DefaultValues.DEFAULT_STU_ID
            logger.info("EduPC 使用默认 stuId: %s", self.stu_id)
        
        # 如果没有unionUserId，使用默认值
        if not self.union_user_id:
            self.union_user_id = DefaultValues.DEFAULT_UNION_USER_ID
            logger.info("EduPC 使用默认 unionUserId: %s", self.union_user_id)
    
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

    def _ensure_browser_answer_cookies(self):
        """
        补齐答题链路依赖的浏览器态 Cookie。
        addRecord / updateToken 在服务端会校验 _STUID / _USERTOKEN / JSESSIONID。
        """
        domain = self.BASE_URL.replace("http://", "").replace("https://", "")

        if self.stu_id:
            self.session.cookies.set("_STUID", str(self.stu_id), domain=domain, path="/")
        self.session.cookies.set("_checkRespLvBrowser", "true", domain=domain, path="/")

        # _USERTOKEN 优先使用配置中的浏览器值，其次回退登录 token
        user_token = self.edupc_user_token or self._token
        if user_token:
            self.session.cookies.set("_USERTOKEN", str(user_token), domain=domain, path="/")

        # JSESSIONID 无法从当前接口链稳定获取，允许从配置注入
        if self.edupc_jsession_id:
            self.session.cookies.set("JSESSIONID", str(self.edupc_jsession_id), domain=domain, path="/")
    
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
            
            # 如果缓存中没有 union_user_id，使用默认值
            if not self.union_user_id:
                self.union_user_id = DefaultValues.DEFAULT_UNION_USER_ID
                logger.info("EduPC 缓存中无 unionUserId，使用默认值: %s", self.union_user_id)
            
            return True
        except Exception as e:
            logger.warning("EduPC 加载缓存失败: %s", e)
            if self.SESSION_CACHE.exists():
                self.SESSION_CACHE.unlink()
            return False

"""
AdminClient - 管理后台API客户端
"""
import logging
import pickle
import re
import time
from pathlib import Path
from urllib.parse import quote

from .base_client import BaseClient
from security_utils import md5

logger = logging.getLogger(__name__)

class AdminClient(BaseClient):
    """管理后台API客户端"""
    
    BASE_URL = "http://i.edu.fkw.com.faidev.cc"
    LOGIN_URL = "http://i.fkw.com.faidev.cc/ajax/login_h.jsp?dogSrc=3"
    SESSION_CACHE = Path(__file__).parent.parent / ".session_cache.pkl"
    
    def __init__(self, username: str, password: str):
        super().__init__()
        self.username = username
        self.password = password
        self._token = None
        self.wxapp_aid = None
        self.wxapp_id = None
    
    @property
    def common_params(self):
        """管理后台公共参数"""
        return {
            "_TOKEN": self._token,
            "wxappAid": self.wxapp_aid,
            "wxappId": self.wxapp_id,
        }
    
    def login(self):
        """登录管理后台"""
        # 尝试从缓存加载
        if self._load_session_cache():
            logger.info("使用缓存的 admin session")
            return self
        
        logger.info("admin session 缓存无效，执行登录")
        
        # 先访问登录页获取初始cookie
        self.session.get("http://i.fkw.com.faidev.cc/")
        
        # 登录
        params_str = (
            f"cacct={quote(self.username)}"
            f"&sacct=boss"
            f"&pwd={md5(self.password)}"
            f"&autoLogin=false"
            f"&staffLogin=false"
            f"&bizType=5"
            f"&dogId=0"
            f"&fromsite=false"
            f"&cmd=loginCorpNews"
            f"&validateCode="
        )
        
        resp = self.session.post(
            self.LOGIN_URL,
            data=params_str,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "http://i.fkw.com.faidev.cc/",
            },
        )
        
        result = self._parse_response(resp)
        
        if not result.get("success") and result.get("needValidateCode"):
            logger.warning("登录触发图形验证码保护，请稍后重试或清理 session 缓存")
            raise AssertionError(f"Login failed (need CAPTCHA): {result}")
        
        self.assert_success(result, "Admin 登录失败")
        logger.info("admin 登录成功: user=%s aid=%s", self.username, result.get("aid"))
        
        # 提取token
        self._extract_token()
        
        # 保存缓存
        self._save_session_cache()
        
        return self
    
    def _extract_token(self):
        """从管理后台页面提取_TOKEN和wxappAid/wxappId"""
        resp = self.session.get(
            f"{self.BASE_URL}/?__aacct={self.username}",
            allow_redirects=True,
        )
        html = resp.text
        
        # 提取_TOKEN
        token_match = re.search(r"TOKEN['\"]?\s*(?:value=|[:=])\s*['\"]([a-f0-9]{32})['\"]", html)
        if token_match:
            self._token = token_match.group(1)
        
        # 提取wxappAid/wxappId
        aid_match = re.search(r'wxappAid["\']?\s*[:=]\s*["\']?(\d+)', html)
        wid_match = re.search(r'wxappId["\']?\s*[:=]\s*["\']?(\d+)', html)
        self.wxapp_aid = aid_match.group(1) if aid_match else "3444128"
        self.wxapp_id = wid_match.group(1) if wid_match else "110"
        
        logger.info("提取 admin token 和站点参数成功")
    
    def _save_session_cache(self):
        """保存session到缓存"""
        try:
            cache_data = {
                'cookies': self.session.cookies,
                '_token': self._token,
                'wxapp_aid': self.wxapp_aid,
                'wxapp_id': self.wxapp_id,
                'timestamp': time.time(),
            }
            with open(self.SESSION_CACHE, 'wb') as f:
                pickle.dump(cache_data, f)
            logger.info("admin session 已缓存")
        except Exception as e:
            logger.warning("保存 admin session 缓存失败: %s", e)
    
    def _load_session_cache(self):
        """从缓存加载session（有效期30分钟）"""
        if not self.SESSION_CACHE.exists():
            return False
        
        try:
            with open(self.SESSION_CACHE, 'rb') as f:
                cache_data = pickle.load(f)
            
            # 检查缓存是否过期
            cache_age = time.time() - cache_data['timestamp']
            if cache_age > 1800:  # 30分钟
                logger.info("admin session 缓存已过期（%.1f 分钟）", cache_age / 60)
                self.SESSION_CACHE.unlink()
                return False
            
            # 恢复session
            self.session.cookies.update(cache_data['cookies'])
            self._token = cache_data['_token']
            self.wxapp_aid = cache_data['wxapp_aid']
            self.wxapp_id = cache_data['wxapp_id']
            
            logger.info("加载 admin 缓存 session 成功（%.1f 分钟前）", cache_age / 60)
            return True
            
        except Exception as e:
            logger.warning("加载 admin session 缓存失败: %s", e)
            if self.SESSION_CACHE.exists():
                self.SESSION_CACHE.unlink()
            return False

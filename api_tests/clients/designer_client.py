"""
DesignerClient - 设计器端API客户端
"""
import logging
import os
from pathlib import Path
import re

from .admin_client import AdminClient

logger = logging.getLogger(__name__)


class BaseDesignerClient(AdminClient):
    """设计器端API客户端（与管理后台共用登录）"""

    BASE_URL = ""
    LOGIN_URL = os.getenv("ADMIN_LOGIN_URL", "http://i.fkw.com.faidev.cc/ajax/login_h.jsp?dogSrc=3")
    SESSION_CACHE = Path(__file__).parent.parent / ".designer_session_cache.pkl"

    @property
    def common_params(self):
        """设计器公共参数（仅_TOKEN）"""
        return {"_TOKEN": self._token} if self._token else {}

    def _extract_token(self):
        """从设计器页面提取_TOKEN"""
        resp = self.session.get(
            f"{self.BASE_URL}/?__aacct={self.username}",
            allow_redirects=True,
        )
        html = resp.text
        token_match = re.search(r"TOKEN['\"]?\s*(?:value=|[:=])\s*['\"]([a-f0-9]{32})['\"]", html)
        if token_match:
            self._token = token_match.group(1)
        logger.info("提取设计器 token 成功")


class EdupcDesignerClient(BaseDesignerClient):
    """EduPC设计器端客户端"""

    BASE_URL = os.getenv("EDUPC_DESIGNER_BASE_URL", "http://huaedu1-110.edu.fkw.com.faidev.cc")
    SESSION_CACHE = Path(__file__).parent.parent / ".edupc_designer_session_cache.pkl"


class MobileDesignerClient(BaseDesignerClient):
    """移动端设计器客户端"""

    BASE_URL = os.getenv("MOBILE_DESIGNER_BASE_URL", "http://m.edu.fkw.com.faidev.cc")
    SESSION_CACHE = Path(__file__).parent.parent / ".mobile_designer_session_cache.pkl"

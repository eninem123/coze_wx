import requests
import json
import time
from typing import Optional
from config import Config

class FeishuMessenger:
    def __init__(self):
        self.app_id = Config.FEISHU_APP_ID
        self.app_secret = Config.FEISHU_APP_SECRET
        self.tenant_access_token = None
        self.token_expire_time = 0
    
    def get_tenant_access_token(self) -> str:
        current_time = time.time()
        
        if self.tenant_access_token and current_time < self.token_expire_time:
            return self.tenant_access_token
        
        url = f"{Config.FEISHU_API_BASE}/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") == 0:
                self.tenant_access_token = result.get("tenant_access_token")
                self.token_expire_time = current_time + result.get("expire", 7200) - 300
                return self.tenant_access_token
            else:
                raise Exception(f"获取token失败: {result.get('msg')}")
                
        except Exception as e:
            raise Exception(f"获取飞书token失败: {str(e)}")
    
    def send_message(self, receive_id: str, content: str, msg_type: str = "text") -> bool:
        try:
            token = self.get_tenant_access_token()
            url = f"{Config.FEISHU_API_BASE}/im/v1/messages?receive_id_type=open_id"
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "receive_id": receive_id,
                "msg_type": msg_type,
                "content": json.dumps({"text": content})
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") == 0:
                return True
            else:
                print(f"发送消息失败: {result.get('msg')}")
                return False
                
        except Exception as e:
            print(f"发送消息异常: {str(e)}")
            return False
    
    def send_rich_text(self, receive_id: str, title: str, content: str) -> bool:
        try:
            token = self.get_tenant_access_token()
            url = f"{Config.FEISHU_API_BASE}/im/v1/messages?receive_id_type=open_id"
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            rich_content = [
                {
                    "tag": "text",
                    "text": f"{title}\n\n{content}"
                }
            ]
            
            data = {
                "receive_id": receive_id,
                "msg_type": "text",
                "content": json.dumps({"text": f"{title}\n\n{content}"})
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            return result.get("code") == 0
            
        except Exception as e:
            print(f"发送富文本消息异常: {str(e)}")
            return False
    
    def send_card_message(self, receive_id: str, title: str, content: str) -> bool:
        try:
            token = self.get_tenant_access_token()
            url = f"{Config.FEISHU_API_BASE}/im/v1/messages?receive_id_type=open_id"
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            card_content = {
                "config": {
                    "wide_screen_mode": True
                },
                "header": {
                    "title": {
                        "content": title,
                        "tag": "plain_text"
                    }
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "content": content,
                            "tag": "lark_md"
                        }
                    }
                ]
            }
            
            data = {
                "receive_id": receive_id,
                "msg_type": "interactive",
                "content": json.dumps(card_content)
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            return result.get("code") == 0
            
        except Exception as e:
            print(f"发送卡片消息异常: {str(e)}")
            return False

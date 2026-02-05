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
    
    def upload_image(self, image_path: str, image_type: str = "message") -> Optional[str]:
        """
        上传图片到飞书
        :param image_path: 图片本地路径
        :param image_type: 图片用途，message或avatar
        :return: 上传成功返回image_key，失败返回None
        """
        try:
            token = self.get_tenant_access_token()
            url = f"{Config.FEISHU_API_BASE}/im/v1/images"
            
            headers = {
                "Authorization": f"Bearer {token}"
            }
            
            files = {
                "image": open(image_path, 'rb')
            }
            
            data = {
                "image_type": image_type
            }
            
            response = requests.post(url, files=files, data=data, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") == 0:
                image_key = result.get("data", {}).get("image_key")
                if image_key:
                    return image_key
                else:
                    print(f"上传图片成功但未返回image_key: {result}")
                    return None
            else:
                print(f"上传图片失败: {result.get('msg')}")
                return None
                
        except Exception as e:
            print(f"上传图片异常: {str(e)}")
            return None
    
    def send_image_message(self, receive_id: str, image_key: str) -> bool:
        """
        发送图片消息
        :param receive_id: 接收者open_id
        :param image_key: 图片的image_key
        :return: 发送成功返回True，失败返回False
        """
        try:
            token = self.get_tenant_access_token()
            url = f"{Config.FEISHU_API_BASE}/im/v1/messages?receive_id_type=open_id"
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "receive_id": receive_id,
                "msg_type": "image",
                "content": json.dumps({"image_key": image_key})
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            return result.get("code") == 0
            
        except Exception as e:
            print(f"发送图片消息异常: {str(e)}")
            return False
    
    def upload_image_to_drive(self, image_path: str, file_name: str, parent_type: str = "ccm_import_open", parent_node: str = "") -> Optional[str]:
        """
        上传图片到飞书云文档
        :param image_path: 图片本地路径
        :param file_name: 素材名称（需带扩展名，如 demo.png）
        :param parent_type: 挂载类型，如 bitable_file（多维表格）、ccm_import_open（云空间）
        :param parent_node: 父节点 token（如多维表格 app_token 或文件夹 token）
        :return: 上传成功返回file_token，失败返回None
        """
        try:
            token = self.get_tenant_access_token()
            url = f"{Config.FEISHU_API_BASE}/drive/v1/medias/upload_all"
            
            headers = {
                "Authorization": f"Bearer {token}"
            }
            
            # 读取文件内容
            with open(image_path, 'rb') as f:
                file_content = f.read()
            
            files = {
                "file": (file_name, file_content)
            }
            
            data = {
                "parent_type": parent_type,
                "file_name": file_name,
                "size": len(file_content)
            }
            
            if parent_node:
                data["parent_node"] = parent_node
            
            response = requests.post(url, files=files, data=data, headers=headers, timeout=60)
            
            # 打印详细的响应信息用于调试
            print(f"云文档上传响应状态码: {response.status_code}")
            print(f"云文档上传响应内容: {response.text}")
            
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") == 0:
                file_token = result.get("data", {}).get("file_token")
                if file_token:
                    return file_token
                else:
                    print(f"上传图片到云文档成功但未返回file_token: {result}")
                    return None
            else:
                print(f"上传图片到云文档失败: {result.get('msg')}")
                return None
                
        except Exception as e:
            print(f"上传图片到云文档异常: {str(e)}")
            return None

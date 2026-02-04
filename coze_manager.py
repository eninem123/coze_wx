import requests
import json
import time
import logging
from typing import List, Dict, Optional
from config import Config

logger = logging.getLogger(__name__)

class CozeContextManager:
    def __init__(self):
        self.sessions: Dict[str, List[Dict]] = {}
        self.default_session_id = "Sv2ke0dSddwKotcns0j1c"
    
    def get_or_create_session(self, user_id: str) -> str:
        if user_id not in self.sessions:
            self.sessions[user_id] = []
        return self.default_session_id
    
    def add_message(self, user_id: str, role: str, content: str):
        if user_id not in self.sessions:
            self.sessions[user_id] = []
        
        self.sessions[user_id].append({
            "role": role,
            "content": content,
            "timestamp": time.time()
        })
        
        if len(self.sessions[user_id]) > 20:
            self.sessions[user_id] = self.sessions[user_id][-20:]
    
    def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        if user_id not in self.sessions:
            return []
        return self.sessions[user_id][-limit:]
    
    def call_coze_with_context(self, user_id: str, question: str) -> str:
        logger.info(f"[Coze] 用户 {user_id} 提问: {question}")
        session_id = self.get_or_create_session(user_id)
        
        self.add_message(user_id, "user", question)
        
        headers = {
            "Authorization": f"Bearer {Config.COZE_BEARER_TOKEN}",
            "Content-Type": "application/json"
        }
        
        conversation_history = self.get_conversation_history(user_id)
        logger.info(f"[Coze] 对话历史记录数: {len(conversation_history)}")
        
        prompt_messages = []
        for msg in conversation_history:
            if msg["role"] == "user":
                prompt_messages.append({
                    "type": "text",
                    "content": {
                        "text": msg["content"]
                    }
                })
        
        data = {
            "content": {
                "query": {
                    "prompt": prompt_messages
                }
            },
            "type": "query",
            "session_id": session_id,
            "project_id": Config.COZE_PROJECT_ID
        }
        
        logger.info(f"[Coze] 请求数据: {json.dumps(data, ensure_ascii=False)[:200]}...")
        
        try:
            logger.info(f"[Coze] 正在调用API: {Config.COZE_API_URL}")
            response = requests.post(
                Config.COZE_API_URL,
                json=data,
                headers=headers,
                timeout=60,
                stream=True
            )
            logger.info(f"[Coze] API响应状态码: {response.status_code}")
            response.raise_for_status()
            
            full_answer = ""
            line_count = 0
            for line in response.iter_lines():
                if line:
                    line_count += 1
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]
                        try:
                            data_json = json.loads(data_str)
                            if data_json.get('type') == 'answer':
                                answer = data_json.get('content', {}).get('answer', '')
                                full_answer += answer
                                logger.debug(f"[Coze] 收到回答片段: {answer}")
                        except json.JSONDecodeError as json_err:
                            logger.debug(f"[Coze] JSON解析错误: {json_err}")
            
            logger.info(f"[Coze] 处理了 {line_count} 行响应")
            logger.info(f"[Coze] 完整回答: {full_answer[:100]}...")
            
            if full_answer:
                self.add_message(user_id, "assistant", full_answer)
                logger.info(f"[Coze] 成功获取智能体回复，长度: {len(full_answer)}")
                return full_answer
            else:
                logger.warning("[Coze] 未获取到智能体回复")
                return "未获取到智能体回复"
                
        except Exception as e:
            error_msg = f"调用Coze智能体失败：{str(e)}"
            logger.error(f"[Coze] API调用失败: {str(e)}")
            self.add_message(user_id, "system", error_msg)
            return error_msg
    
    def clear_session(self, user_id: str):
        if user_id in self.sessions:
            self.sessions[user_id] = []

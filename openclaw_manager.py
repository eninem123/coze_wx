#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw上下文管理器

用于管理OpenClaw智能体的对话上下文和API调用
"""

import requests
import json
import time
import logging
from typing import Optional, Dict, List
from config import Config

logger = logging.getLogger(__name__)

class OpenClawContextManager:
    def __init__(self):
        self.sessions: Dict[str, List[Dict]] = {}
        self.default_session_id = "openclaw-default"
        self.max_history_length = 20
    
    def get_or_create_session(self, user_id: str) -> str:
        """获取或创建用户会话"""
        if user_id not in self.sessions:
            self.sessions[user_id] = []
            logger.info(f"[OpenClaw] 为用户 {user_id} 创建新会话")
        return self.default_session_id
    
    def add_message(self, user_id: str, role: str, content: str):
        """添加消息到会话历史"""
        if user_id not in self.sessions:
            self.sessions[user_id] = []
        
        self.sessions[user_id].append({
            "role": role,
            "content": content,
            "timestamp": time.time()
        })
        
        if len(self.sessions[user_id]) > self.max_history_length:
            self.sessions[user_id] = self.sessions[user_id][-self.max_history_length:]
            logger.info(f"[OpenClaw] 用户 {user_id} 会话历史已截断到 {self.max_history_length} 条")
    
    def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """获取对话历史"""
        if user_id not in self.sessions:
            return []
        return self.sessions[user_id][-limit:]
    
    def clear_session(self, user_id: str):
        """清空用户会话"""
        if user_id in self.sessions:
            self.sessions[user_id] = []
            logger.info(f"[OpenClaw] 已清空用户 {user_id} 的对话历史")
            return True
        return False
    
    def call_openclaw_with_context(self, user_id: str, question: str) -> str:
        """
        调用OpenClaw智能体并维护上下文
        
        Args:
            user_id: 用户ID
            question: 用户问题
            
        Returns:
            智能体回答
        """
        logger.info(f"[OpenClaw] 用户 {user_id} 提问: {question}")
        
        session_id = self.get_or_create_session(user_id)
        self.add_message(user_id, "user", question)
        
        headers = {
            "Authorization": f"Bearer {Config.OPENCLAW_TOKEN}",
            "Content-Type": "application/json"
        }
        
        conversation_history = self.get_conversation_history(user_id)
        logger.info(f"[OpenClaw] 对话历史记录数: {len(conversation_history)}")
        
        messages = []
        for msg in conversation_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        data = {
            "messages": messages,
            "model": "openclaw-default",
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        logger.info(f"[OpenClaw] 请求数据: {json.dumps(data, ensure_ascii=False)[:200]}...")
        
        try:
            logger.info(f"[OpenClaw] 正在调用API: {Config.OPENCLAW_API_URL}")
            response = requests.post(
                Config.OPENCLAW_API_URL,
                json=data,
                headers=headers,
                timeout=60
            )
            logger.info(f"[OpenClaw] API响应状态码: {response.status_code}")
            response.raise_for_status()
            
            response_json = response.json()
            logger.info(f"[OpenClaw] API响应: {json.dumps(response_json, ensure_ascii=False)[:200]}...")
            
            if isinstance(response_json, dict):
                if "content" in response_json:
                    full_answer = response_json["content"]
                elif "choices" in response_json and len(response_json["choices"]) > 0:
                    full_answer = response_json["choices"][0].get("message", {}).get("content", "")
                else:
                    full_answer = str(response_json)
            else:
                full_answer = str(response_json)
            
            logger.info(f"[OpenClaw] 完整回答: {full_answer[:100]}...")
            
            if full_answer:
                self.add_message(user_id, "assistant", full_answer)
                logger.info(f"[OpenClaw] 成功获取智能体回复，长度: {len(full_answer)}")
                return full_answer
            else:
                logger.warning("[OpenClaw] 未获取到智能体回复")
                return "未获取到智能体回复"
                
        except requests.exceptions.HTTPError as e:
            error_msg = f"调用OpenClaw智能体失败（HTTP错误）：{str(e)}"
            logger.error(f"[OpenClaw] HTTP错误: {str(e)}")
            if e.response is not None:
                logger.error(f"[OpenClaw] 响应内容: {e.response.text}")
            self.add_message(user_id, "system", error_msg)
            return error_msg
        except requests.exceptions.Timeout:
            error_msg = "调用OpenClaw智能体超时，请稍后重试"
            logger.error(f"[OpenClaw] 请求超时")
            self.add_message(user_id, "system", error_msg)
            return error_msg
        except requests.exceptions.RequestException as e:
            error_msg = f"调用OpenClaw智能体失败（网络错误）：{str(e)}"
            logger.error(f"[OpenClaw] 网络错误: {str(e)}")
            self.add_message(user_id, "system", error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"调用OpenClaw智能体失败：{str(e)}"
            logger.error(f"[OpenClaw] 未知错误: {str(e)}")
            import traceback
            logger.error(f"[OpenClaw] 错误堆栈: {traceback.format_exc()}")
            self.add_message(user_id, "system", error_msg)
            return error_msg
    
    def get_session_info(self, user_id: str) -> Dict:
        """获取会话信息"""
        if user_id not in self.sessions:
            return {
                "user_id": user_id,
                "message_count": 0,
                "last_message_time": None
            }
        
        messages = self.sessions[user_id]
        last_message_time = messages[-1].get("timestamp") if messages else None
        
        return {
            "user_id": user_id,
            "message_count": len(messages),
            "last_message_time": last_message_time
        }
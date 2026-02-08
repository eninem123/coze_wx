#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw模拟器

由于OpenClaw API接口暂时无法访问，提供一个模拟器来测试飞书集成
"""

import time
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

class OpenClawSimulator:
    def __init__(self):
        self.sessions: Dict[str, List[Dict]] = {}
        self.default_session_id = "openclaw-default"
        self.max_history_length = 20
        
        # 模拟的智能体回复
        self.responses = {
            "你是谁": "我是OpenClaw智能体，很高兴为您服务！",
            "你好": "你好！我是OpenClaw，有什么可以帮助您的吗？",
            "帮助": "我是OpenClaw智能体，可以回答各种问题。请告诉我您需要什么帮助。",
            "股票": "关于股票分析，我可以为您提供市场趋势、个股分析等建议。请告诉我您关注的股票。",
            "天气": "我是OpenClaw智能体，主要专注于通用对话和问题解答。天气查询建议使用专门的天气服务。",
            "时间": "当前时间是：{}".format(time.strftime('%Y-%m-%d %H:%M:%S'))
        }
    
    def get_or_create_session(self, user_id: str) -> str:
        """获取或创建用户会话"""
        if user_id not in self.sessions:
            self.sessions[user_id] = []
            logger.info(f"[OpenClaw模拟器] 为用户 {user_id} 创建新会话")
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
            logger.info(f"[OpenClaw模拟器] 用户 {user_id} 会话历史已截断到 {self.max_history_length} 条")
    
    def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """获取对话历史"""
        if user_id not in self.sessions:
            return []
        return self.sessions[user_id][-limit:]
    
    def clear_session(self, user_id: str):
        """清空用户会话"""
        if user_id in self.sessions:
            self.sessions[user_id] = []
            logger.info(f"[OpenClaw模拟器] 已清空用户 {user_id} 的对话历史")
            return True
        return False
    
    def call_openclaw_with_context(self, user_id: str, question: str) -> str:
        """
        模拟调用OpenClaw智能体并维护上下文
        
        Args:
            user_id: 用户ID
            question: 用户问题
            
        Returns:
            智能体回答
        """
        logger.info(f"[OpenClaw模拟器] 用户 {user_id} 提问: {question}")
        
        session_id = self.get_or_create_session(user_id)
        self.add_message(user_id, "user", question)
        
        conversation_history = self.get_conversation_history(user_id)
        logger.info(f"[OpenClaw模拟器] 对话历史记录数: {len(conversation_history)}")
        
        # 模拟API调用延迟
        time.sleep(1)
        
        # 生成智能回复
        if question in self.responses:
            answer = self.responses[question]
        else:
            # 基于问题内容生成回复
            if any(word in question.lower() for word in ['股票', '投资', '股市', '涨跌']):
                answer = f"关于'{question}'，作为OpenClaw智能体，我可以为您提供股票市场分析。但请注意，投资有风险，建议您结合专业分析师的建议进行决策。"
            elif any(word in question.lower() for word in ['天气', '温度', '下雨']):
                answer = f"关于'{question}'，我是OpenClaw智能体，主要专注于通用对话。天气查询建议使用专门的天气服务应用。"
            elif any(word in question.lower() for word in ['时间', '日期', '几点']):
                answer = f"当前时间是：{time.strftime('%Y-%m-%d %H:%M:%S')}"
            else:
                answer = f"感谢您的提问：'{question}'。作为OpenClaw智能体，我会尽力为您提供有用的信息。如果您有具体的问题或需要特定领域的帮助，请告诉我。"
        
        logger.info(f"[OpenClaw模拟器] 生成回答: {answer[:100]}...")
        
        if answer:
            self.add_message(user_id, "assistant", answer)
            logger.info(f"[OpenClaw模拟器] 成功生成智能体回复，长度: {len(answer)}")
            return answer
        else:
            logger.warning("[OpenClaw模拟器] 未生成智能体回复")
            return "抱歉，我暂时无法回答这个问题。"
    
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

# 测试函数
def test_simulator():
    """测试模拟器功能"""
    simulator = OpenClawSimulator()
    user_id = "test-user"
    
    questions = ["你好", "你是谁", "今天天气怎么样", "帮我分析股票", "现在几点了"]
    
    for question in questions:
        print(f"用户: {question}")
        answer = simulator.call_openclaw_with_context(user_id, question)
        print(f"OpenClaw: {answer}")
        print("---")

if __name__ == "__main__":
    test_simulator()
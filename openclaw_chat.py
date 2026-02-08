#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw对话脚本

这个脚本用于：
1. 与阿里云服务器上的OpenClaw智能体进行对话
2. 在服务器上部署polymarket
3. 提供命令行交互界面
"""

import requests
import json
import time
import logging
import argparse
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class OpenClawChat:
    def __init__(self):
        self.sessions = {}
        self.default_session_id = "openclaw-default"
    
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
    
    def get_conversation_history(self, user_id: str, limit: int = 10) -> list:
        if user_id not in self.sessions:
            return []
        return self.sessions[user_id][-limit:]
    
    def chat_with_openclaw(self, user_id: str, question: str) -> str:
        """与OpenClaw智能体对话"""
        logger.info(f"[OpenClaw] 用户 {user_id} 提问: {question}")
        session_id = self.get_or_create_session(user_id)
        
        self.add_message(user_id, "user", question)
        
        headers = {
            "Authorization": f"Bearer {Config.OPENCLAW_TOKEN}",
            "Content-Type": "application/json"
        }
        
        conversation_history = self.get_conversation_history(user_id)
        logger.info(f"[OpenClaw] 对话历史记录数: {len(conversation_history)}")
        
        # 构建对话历史
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
            
            # 解析OpenClaw的响应
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
                
        except Exception as e:
            error_msg = f"调用OpenClaw智能体失败：{str(e)}"
            logger.error(f"[OpenClaw] API调用失败: {str(e)}")
            self.add_message(user_id, "system", error_msg)
            return error_msg
    
    def clear_session(self, user_id: str):
        """清空对话历史"""
        if user_id in self.sessions:
            self.sessions[user_id] = []
            logger.info(f"[OpenClaw] 已清空用户 {user_id} 的对话历史")
            return "对话历史已清空"
        return "对话历史为空"
    
    def deploy_polymarket(self, server_ip: str, username: str, password: str) -> str:
        """在服务器上部署polymarket"""
        logger.info(f"[OpenClaw] 正在部署polymarket到服务器: {server_ip}")
        
        # 这里应该实现部署polymarket的逻辑
        # 由于我们没有SSH访问权限，这里只返回一个模拟的部署结果
        
        try:
            # 模拟部署过程
            # logger.info("[OpenClaw] 正在连接服务器...")
            # time.sleep(1)
            # logger.info("[OpenClaw] 正在更新系统包...")
            # time.sleep(1)
            # logger.info("[OpenClaw] 正在安装依赖...")
            # time.sleep(1)
            # logger.info("[OpenClaw] 正在克隆polymarket代码...")
            # time.sleep(1)
            # logger.info("[OpenClaw] 正在配置polymarket...")
            # time.sleep(1)
            # logger.info("[OpenClaw] 正在启动polymarket服务...")
            # time.sleep(1)
            logger.info("[OpenClaw] 模拟polymarket部署完成！")
            
            return "模拟polymarket已成功部署到服务器"
            
        except Exception as e:
            error_msg = f"部署polymarket失败：{str(e)}"
            logger.error(f"[OpenClaw] 部署失败: {str(e)}")
            return error_msg

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="OpenClaw对话工具")
    parser.add_argument("--deploy", action="store_true", help="部署polymarket到服务器")
    parser.add_argument("--server", type=str, default="8.218.129.40", help="服务器IP地址")
    parser.add_argument("--username", type=str, default="admin", help="服务器用户名")
    parser.add_argument("--password", type=str, default="", help="服务器密码")
    
    args = parser.parse_args()
    
    chatbot = OpenClawChat()
    user_id = "local-user"
    
    if args.deploy:
        # 部署polymarket
        result = chatbot.deploy_polymarket(args.server, args.username, args.password)
        print(f"部署结果: {result}")
        return
    
    # 交互式对话
    print("=" * 60)
    print("🤖 OpenClaw 对话工具")
    print("=" * 60)
    print("输入您的问题，与OpenClaw智能体对话")
    print("输入 'clear' 清空对话历史")
    print("输入 'exit' 退出程序")
    print("=" * 60)
    
    while True:
        try:
            question = input("\n您: ")
            
            if question.lower() == "exit":
                print("再见！")
                break
            
            if question.lower() == "clear":
                result = chatbot.clear_session(user_id)
                print(f"🤖 {result}")
                continue
            
            # 与OpenClaw对话
            answer = chatbot.chat_with_openclaw(user_id, question)
            print(f"🤖 {answer}")
            
        except KeyboardInterrupt:
            print("\n再见！")
            break
        except Exception as e:
            print(f"错误: {str(e)}")
            continue

if __name__ == "__main__":
    main()

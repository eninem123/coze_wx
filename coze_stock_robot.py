import requests
import time
import os
import json
from dotenv import load_dotenv

# 加载环境变量（避免密钥硬编码，安全）
load_dotenv()

# ====================== 配置区（只改这里！）======================
# 1. Coze API 核心参数（从Coze智能体API调用页复制）
def _get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default

COZE_API_KEY = os.getenv("COZE_KEY")
COZE_BOT_ID = os.getenv("COZE_BOT_ID_CG")
COZE_USER_ID = os.getenv("COZE_USER_ID")
COZE_CG_BER = os.getenv("COZE_CG_BEARER_TOKEN") or os.getenv("COZE_BEARER_TOKEN")
STOCK_QUESTION = "帮我分析今天A股的整体走势，北向资金流向，以及半导体板块的投资机会，给出简洁的分析和建议"
PUSH_TYPE = "wechat"
COZE_API_URL = "https://8mbn769hk8.coze.site/stream_run"
COZE_SESSION_ID = os.getenv("COZE_SESSION_ID", "Sv2ke0dSddwKotcns0j1c")
COZE_PROJECT_ID = _get_int_env("COZE_PROJECT_ID", 7598933258117611561)

def call_coze_bot(question):
    headers = {
        "Authorization": f"Bearer {COZE_CG_BER}",
        "Content-Type": "application/json"
    }
    data = {
        "content": {
            "query": {
                "prompt": [
                    {
                        "type": "text",
                        "content": {
                            "text": question
                        }
                    }
                ]
            }
        },
        "type": "query",
        "session_id": COZE_SESSION_ID,
        "project_id": COZE_PROJECT_ID
    }
    try:
        response = requests.post(COZE_API_URL, json=data, headers=headers, timeout=60, stream=True)
        response.raise_for_status()
        
        full_answer = ""
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data_str = line_str[6:]
                    try:
                        data_json = json.loads(data_str)
                        if data_json.get('type') == 'answer':
                            answer = data_json.get('content', {}).get('answer', '')
                            full_answer += answer
                    except json.JSONDecodeError:
                        pass
        
        if full_answer:
            return f"【{time.strftime('%Y-%m-%d %H:%M:%S')} 炒股智能体分析】\n{full_answer}"
        else:
            return "未获取到智能体回复"
    except Exception as e:
        return f"调用Coze智能体失败：{str(e)}"

def push_message(content):
    """推送结果到指定渠道，选一个用即可"""
    if PUSH_TYPE == "wechat":
        # 微信推送：用「Server酱」，最方便的个人微信推送（免费版足够用）
        SCKEY = os.getenv("SERVERCHAN_SCKEY", "")
        if not SCKEY:
            return "微信推送未配置SCKEY"
        url = f"https://sctapi.ftqq.com/{SCKEY}.send"
        data = {"title": "炒股智能体分析结果", "desp": content}
        requests.post(url, data=data, timeout=30)
        return "微信推送成功"
    elif PUSH_TYPE == "qywx":
        # 企业微信推送：适合有企业微信的场景，无广告
        QYWX_WEBHOOK = os.getenv("PUSH_QYWX_WEBHOOK")  # 企业微信机器人webhook
        if not QYWX_WEBHOOK:
            return "企业微信推送未配置webhook"
        data = {"msgtype": "text", "text": {"content": content}}
        requests.post(QYWX_WEBHOOK, json=data, timeout=30)
        return "企业微信推送成功"
    elif PUSH_TYPE == "qq":
        # QQ推送：用「酷Q/NoneBot」简易机器人，或第三方QQ推送接口（按需选）
        # 这里给个第三方免费接口示例，替换成自己的即可
        QQ_PUSH_URL = os.getenv("PUSH_QQ_URL")
        QQ_NUM = os.getenv("PUSH_QQ_NUM")
        if not QQ_PUSH_URL or not QQ_NUM:
            return "QQ推送未配置参数"
        data = {"qq": QQ_NUM, "msg": content}
        requests.post(QQ_PUSH_URL, json=data, timeout=30)
        return "QQ推送成功"
    else:
        return "未选择有效推送渠道"

if __name__ == "__main__":
    # 主逻辑：调用Coze提问 → 获取结果 → 推送
    print("开始调用Coze炒股智能体...")
    analysis_result = call_coze_bot(STOCK_QUESTION)
    print(f"智能体返回结果：\n{analysis_result}")
    push_status = push_message(analysis_result)
    print(f"推送状态：{push_status}")
    # 可选：保存历史分析结果到本地（方便回溯）
    # with open("stock_analysis_history.txt", "a", encoding="utf-8") as f:
    #     f.write(f"{analysis_result}\n{'='*50}\n")

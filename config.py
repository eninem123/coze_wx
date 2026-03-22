import os
from dotenv import load_dotenv

load_dotenv()

def _get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default

class Config:
    # Coze配置（备用）
    COZE_API_URL = os.getenv("COZE_API_URL", "https://8mbn769hk8.coze.site/stream_run")
    COZE_BEARER_TOKEN = os.getenv("COZE_BEARER_TOKEN", "")
    COZE_PROJECT_ID = _get_int_env("COZE_PROJECT_ID", 7598933258117611561)
    
    
    DOUB_KEY = os.getenv("DOUB_KEY", "")
    DOUB_API_URL = os.getenv("DOUB_API_URL", "https://ark.cn-beijing.volces.com/api/v3/responses")
    DOUB_MODEL = os.getenv("DOUB_MODEL", "doubao-seed-1-6-251015")
    
    FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
    FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
    FEISHU_VERIFICATION_TOKEN = os.getenv("FEISHU_VERIFICATION_TOKEN", "")
    FEISHU_ENCRYPT_KEY = os.getenv("FEISHU_ENCRYPT_KEY", "")
    
    FEISHU_API_BASE = "https://open.feishu.cn/open-apis"
    
    DEFAULT_STOCK_QUESTION = "今天如果买入，可以短期14天能高概率涨10%的股票有哪些，给出简洁的分析和建议"
    
    SCHEDULE_TIMES = ["09:00", "15:00", "20:00"]
    
    LOG_FILE = "feishu_bot.log"

    OPENCLAW_API_URL = os.getenv("OPENCLAW_API_URL", "http://localhost:18789/v1/chat/completions")
    OPENCLAW_TOKEN = os.getenv("OPENCLAW_TOKEN", "")
    OPENCLAW_SESSION_KEY = os.getenv("OPENCLAW_SESSION_KEY", "")

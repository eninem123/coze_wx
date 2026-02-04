import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    COZE_API_URL = "https://8mbn769hk8.coze.site/stream_run"
    COZE_BEARER_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImUxNWJiODBmLTAyODAtNDM4My1iZDAwLTY3OThiY2M5ZmI3ZSJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIldUM1FJb0xzWXNvY0QxM0xaSmRGRHBzWllQWmQ0cnJXIl0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzcwMjE1ODM5LCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NTk4OTQwOTA3NDg3ODg3NDAyIiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjAzMDE5MTM4MDcxNTI3NDU5In0.Ecp_aZcL95ughEMVLSNL2ZNN-M9orPAc4w8tEr6xaa8xOV4gqkfUPh1ZoyOs3DWKcgT3jHDGWWyb6HCN1Ssh5bqKjdxa4cMAOIIjeSuKi7HfAiIhg3QxLD7G52FIJDvB1fuR3eFixJyRBODXmEgolHgGqbfgBtT8sVLP23RlBmz3e2f3iaZPK6iK9g0gR2XtOx7H5-pj9zNZyagGrRhkkD_nfnSn8ak8nclQtPPRNpMbjFNCwmgKqZdPikPD2FdQvmBE67dc-MKZd_zPp0k2ToDyTc0DcYxnvsmYs34myTto964bp1SKoUOveT_S_clhiWMajNrkpKhc0oAcqUz39Q"
    COZE_PROJECT_ID = 7598933258117611561
    
    DOUB_KEY = os.getenv("DOUB_KEY", "")
    DOUB_API_URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    DOUB_MODEL = "ep-20260204233249-7q4r9"
    
    FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
    FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
    FEISHU_VERIFICATION_TOKEN = os.getenv("FEISHU_VERIFICATION_TOKEN", "")
    FEISHU_ENCRYPT_KEY = os.getenv("FEISHU_ENCRYPT_KEY", "")
    
    FEISHU_API_BASE = "https://open.feishu.cn/open-apis"
    
    DEFAULT_STOCK_QUESTION = "今天如果买入，可以短期14天能高概率涨10%的股票有哪些，给出简洁的分析和建议"
    
    SCHEDULE_TIMES = ["09:00", "15:00", "20:00"]
    
    LOG_FILE = "feishu_bot.log"
    
    # 豆包图像分析配置
    DOUB_KEY = "cf7ec1a8-8f65-4559-bdfc-e8438dc489c2"
    DOUB_API_URL = "https://ark.cn-beijing.volces.com/api/v3/responses"
    DOUB_MODEL = "doubao-seed-1-6-251015"

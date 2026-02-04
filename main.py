import signal
import sys
import time
import logging
from config import Config
from coze_manager import CozeContextManager
from feishu_messenger import FeishuMessenger
from stock_scheduler import StockScheduler
from feishu_websocket import FeishuWebSocketServer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class FeishuStockBot:
    def __init__(self):
        self.coze_manager = CozeContextManager()
        self.feishu_messenger = FeishuMessenger()
        self.scheduler = StockScheduler(self.coze_manager, self.feishu_messenger)
        self.websocket_server = FeishuWebSocketServer(self.coze_manager, self.scheduler)
        self.running = False
    
    def start(self):
        logger.info("=" * 50)
        logger.info("飞书股票智能机器人启动中...")
        logger.info("=" * 50)
        
        try:
            self.scheduler.start()
            logger.info("✅ 定时任务调度器已启动")
            
            self.websocket_server.start()
            logger.info("✅ 飞书WebSocket服务器已启动")
            
            self.running = True
            logger.info("=" * 50)
            logger.info("🚀 飞书股票智能机器人已成功启动！")
            logger.info("=" * 50)
            logger.info("📋 可用命令：")
            logger.info("  • 订阅 - 订阅股票分析推送")
            logger.info("  • 取消订阅 - 取消订阅")
            logger.info("  • 立即分析 - 立即获取股票分析")
            logger.info("  • 清空上下文 - 清空对话历史")
            logger.info("  • 帮助 - 显示帮助信息")
            logger.info("  • 其他问题 - 直接与智能体对话")
            logger.info("=" * 50)
            logger.info(f"⏰ 定时推送时间: {', '.join(Config.SCHEDULE_TIMES)}")
            logger.info("=" * 50)
            
            self.keep_running()
            
        except Exception as e:
            logger.error(f"启动失败: {str(e)}")
            self.stop()
            sys.exit(1)
    
    def keep_running(self):
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("收到中断信号，正在停止...")
            self.stop()
    
    def stop(self):
        logger.info("正在停止飞书股票智能机器人...")
        self.running = False
        
        self.websocket_server.stop()
        self.scheduler.stop()
        
        logger.info("✅ 飞书股票智能机器人已停止")

def signal_handler(signum, frame):
    logger.info(f"收到信号 {signum}，正在停止...")
    if hasattr(signal_handler, 'bot'):
        signal_handler.bot.stop()
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    bot = FeishuStockBot()
    signal_handler.bot = bot
    
    try:
        bot.start()
    except Exception as e:
        logger.error(f"程序异常: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

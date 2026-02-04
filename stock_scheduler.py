import threading
import time
import schedule
from datetime import datetime
from typing import List, Callable
from config import Config
from coze_manager import CozeContextManager
from feishu_messenger import FeishuMessenger

class StockScheduler:
    def __init__(self, coze_manager: CozeContextManager, feishu_messenger: FeishuMessenger):
        self.coze_manager = coze_manager
        self.feishu_messenger = feishu_messenger
        self.subscribers: List[str] = []
        self.scheduler_thread = None
        self.running = False
    
    def add_subscriber(self, user_id: str):
        if user_id not in self.subscribers:
            self.subscribers.append(user_id)
            print(f"添加订阅用户: {user_id}")
    
    def remove_subscriber(self, user_id: str):
        if user_id in self.subscribers:
            self.subscribers.remove(user_id)
            print(f"移除订阅用户: {user_id}")
    
    def send_stock_analysis(self):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始发送股票分析...")
        
        if not self.subscribers:
            print("没有订阅用户，跳过发送")
            return
        
        question = Config.DEFAULT_STOCK_QUESTION
        
        for user_id in self.subscribers:
            try:
                print(f"正在为用户 {user_id} 分析股票...")
                answer = self.coze_manager.call_coze_with_context(user_id, question)
                
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                title = f"【{timestamp} 股票智能分析】"
                
                success = self.feishu_messenger.send_card_message(user_id, title, answer)
                
                if success:
                    print(f"✅ 成功发送给用户 {user_id}")
                else:
                    print(f"❌ 发送给用户 {user_id} 失败")
                    
            except Exception as e:
                print(f"❌ 为用户 {user_id} 发送股票分析失败: {str(e)}")
    
    def schedule_tasks(self):
        for schedule_time in Config.SCHEDULE_TIMES:
            schedule.every().day.at(schedule_time).do(self.send_stock_analysis)
            print(f"已设置定时任务: 每天 {schedule_time} 发送股票分析")
    
    def run_scheduler(self):
        self.running = True
        self.schedule_tasks()
        
        while self.running:
            schedule.run_pending()
            time.sleep(60)
    
    def start(self):
        if not self.running:
            self.scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
            self.scheduler_thread.start()
            print("定时任务调度器已启动")
    
    def stop(self):
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        print("定时任务调度器已停止")
    
    def send_immediate_analysis(self, user_id: str, question: str = None):
        try:
            if question is None:
                question = Config.DEFAULT_STOCK_QUESTION
            
            print(f"立即为用户 {user_id} 发送股票分析...")
            answer = self.coze_manager.call_coze_with_context(user_id, question)
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            title = f"【{timestamp} 股票智能分析】"
            
            success = self.feishu_messenger.send_card_message(user_id, title, answer)
            
            if success:
                return "✅ 股票分析已发送"
            else:
                return "❌ 发送失败"
                
        except Exception as e:
            return f"❌ 发送失败: {str(e)}"

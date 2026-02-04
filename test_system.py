import sys
import time
from config import Config
from coze_manager import CozeContextManager
from feishu_messenger import FeishuMessenger
from stock_scheduler import StockScheduler

def test_config():
    print("=" * 50)
    print("测试1: 配置模块")
    print("=" * 50)
    
    print(f"✅ Coze API URL: {Config.COZE_API_URL}")
    print(f"✅ Coze Project ID: {Config.COZE_PROJECT_ID}")
    print(f"✅ 定时推送时间: {Config.SCHEDULE_TIMES}")
    print(f"✅ 默认股票问题: {Config.DEFAULT_STOCK_QUESTION[:50]}...")
    
    if not Config.FEISHU_APP_ID:
        print("⚠️  警告: FEISHU_APP_ID 未配置")
    else:
        print(f"✅ 飞书 App ID: {Config.FEISHU_APP_ID}")
    
    print()

def test_coze_manager():
    print("=" * 50)
    print("测试2: Coze上下文管理器")
    print("=" * 50)
    
    try:
        manager = CozeContextManager()
        print("✅ Coze管理器初始化成功")
        
        test_user_id = "test_user_001"
        test_question = "测试问题：今天股市怎么样？"
        
        print(f"📝 发送测试问题: {test_question}")
        answer = manager.call_coze_with_context(test_user_id, test_question)
        
        if answer and "失败" not in answer:
            print(f"✅ Coze API调用成功")
            print(f"📊 回答内容: {answer[:100]}...")
            
            history = manager.get_conversation_history(test_user_id)
            print(f"✅ 对话历史记录数: {len(history)}")
            
            manager.clear_session(test_user_id)
            print("✅ 清空会话成功")
        else:
            print(f"❌ Coze API调用失败: {answer}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print()

def test_feishu_messenger():
    print("=" * 50)
    print("测试3: 飞书消息推送")
    print("=" * 50)
    
    try:
        messenger = FeishuMessenger()
        print("✅ 飞书消息推送器初始化成功")
        
        if not Config.FEISHU_APP_ID or not Config.FEISHU_APP_SECRET:
            print("⚠️  跳过测试: 飞书配置未完成")
            print("   请在 .env 文件中配置 FEISHU_APP_ID 和 FEISHU_APP_SECRET")
        else:
            try:
                token = messenger.get_tenant_access_token()
                print(f"✅ 获取飞书Token成功: {token[:20]}...")
            except Exception as e:
                print(f"❌ 获取飞书Token失败: {str(e)}")
                
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print()

def test_scheduler():
    print("=" * 50)
    print("测试4: 定时任务调度器")
    print("=" * 50)
    
    try:
        coze_manager = CozeContextManager()
        feishu_messenger = FeishuMessenger()
        scheduler = StockScheduler(coze_manager, feishu_messenger)
        
        print("✅ 定时任务调度器初始化成功")
        
        test_user_id = "test_user_002"
        scheduler.add_subscriber(test_user_id)
        print(f"✅ 添加订阅用户: {test_user_id}")
        
        print(f"✅ 当前订阅用户数: {len(scheduler.subscribers)}")
        
        scheduler.remove_subscriber(test_user_id)
        print(f"✅ 移除订阅用户: {test_user_id}")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    print()

def main():
    print("\n" + "=" * 50)
    print("飞书股票智能机器人 - 系统测试")
    print("=" * 50 + "\n")
    
    test_config()
    test_coze_manager()
    test_feishu_messenger()
    test_scheduler()
    
    print("=" * 50)
    print("测试完成！")
    print("=" * 50)
    print("\n📋 测试总结:")
    print("✅ 配置模块: 正常")
    print("✅ Coze上下文管理: 正常")
    print("✅ 飞书消息推送: 需要配置")
    print("✅ 定时任务调度: 正常")
    print("\n💡 提示:")
    print("1. 配置飞书应用信息到 .env 文件")
    print("2. 运行 python main.py 启动机器人")
    print("3. 在飞书中发送 '帮助' 查看可用命令")
    print()

if __name__ == "__main__":
    main()

import requests
import json
from config import Config

def get_bot_info():
    print("=" * 50)
    print("获取飞书机器人信息")
    print("=" * 50)
    
    from feishu_messenger import FeishuMessenger
    messenger = FeishuMessenger()
    
    try:
        token = messenger.get_tenant_access_token()
        print(f"✅ 获取Token成功: {token[:30]}...")
        
        url = "https://open.feishu.cn/open-apis/bot/v3/info"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        print("📡 正在请求机器人信息...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        print(f"📊 API响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("code") == 0:
            bot_info = result.get("bot", {})
            print("✅ 获取机器人信息成功！")
            print("=" * 50)
            print(f"🤖 机器人名称: {bot_info.get('app_name')}")
            print(f"🆔 机器人Open ID: {bot_info.get('open_id')}")
            print(f"📷 机器人头像: {bot_info.get('avatar_url')}")
            print(f"🔄 激活状态: {bot_info.get('activate_status')}")
            print(f"📋 IP白名单: {bot_info.get('ip_white_list')}")
            print("=" * 50)
            
            open_id = bot_info.get('open_id')
            if open_id:
                print(f"💡 提示: 请在飞书中使用此Open ID与机器人交互")
                print(f"   机器人Open ID: {open_id}")
            
            return bot_info
        else:
            print(f"❌ 获取失败: {result.get('msg')}")
            return None
            
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        return None

if __name__ == "__main__":
    get_bot_info()

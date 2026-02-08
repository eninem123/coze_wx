import lark_oapi as lark
import logging
import json
from config import Config
from coze_manager import CozeContextManager
from stock_scheduler import StockScheduler
from image_analyzer import DoubaoImageAnalyzer
from feishu_messenger import FeishuMessenger
from openclaw_simulator import OpenClawSimulator

logger = logging.getLogger(__name__)

class FeishuWebSocketServer:
    def __init__(self, coze_manager: CozeContextManager, scheduler: StockScheduler):
        self.coze_manager = coze_manager
        self.openclaw_manager = OpenClawSimulator()
        self.scheduler = scheduler
        self.client = None
        self.image_analyzer = DoubaoImageAnalyzer()
        self.feishu_messenger = FeishuMessenger()
        self.user_ai_preference = {}
    
    def handle_message(self, data):
        try:
            logger.info(f"收到消息，数据类型: {type(data)}")
            
            try:
                # 方式1: 如果是 lark_oapi 对象
                message = data.event.message
                sender = data.event.sender
                open_id = sender.sender_id.open_id
                message_type = message.message_type
                content = message.content
                
                logger.info(f"收到消息，用户: {open_id}, 消息类型: {message_type}")
                
            except AttributeError:
                # 方式2: 如果是字典
                event = data.get('event', {})
                message = event.get('message', {})
                sender = event.get('sender', {})
                sender_id = sender.get('sender_id', {})
                open_id = sender_id.get('open_id', '')
                message_type = message.get('message_type', '')
                content = message.get('content', '')
                
                logger.info(f"收到消息(字典格式)，用户: {open_id}, 消息类型: {message_type}")
            
            if message_type == "text" and content:
                try:
                    text_content = json.loads(content).get("text", "").strip()
                    if text_content:
                        logger.info(f"用户 {open_id} 发送消息: {text_content}")
                        self.process_user_message(open_id, text_content)
                except json.JSONDecodeError:
                    logger.error(f"解析消息内容失败: {content}")
                    self.feishu_messenger.send_message(open_id, "❌ 消息格式错误")
            
            elif message_type == "image" and content:
                try:
                    image_data = json.loads(content)
                    image_key = image_data.get('image_key', '')
                    image_url = image_data.get('image_url', '') or image_data.get('url', '')
                    
                    logger.info(f"用户 {open_id} 发送图片: {image_key}")
                    logger.info(f"图片信息: {image_data}")
                    
                    if image_url:
                        logger.info(f"直接使用消息中的图片URL: {image_url}")
                        self.handle_image_message(open_id, image_key, image_url)
                    elif image_key:
                        logger.info(f"使用图片key: {image_key}")
                        self.handle_image_message(open_id, image_key)
                    else:
                        logger.error(f"图片信息中未找到image_key或URL: {image_data}")
                        self.feishu_messenger.send_message(open_id, "❌ 图片信息不完整")
                except json.JSONDecodeError:
                    logger.error(f"解析图片内容失败: {content}")
                    self.feishu_messenger.send_message(open_id, "❌ 图片格式错误")
            
        except Exception as e:
            logger.error(f"处理消息失败: {str(e)}")
            import traceback
            logger.error(f"错误堆栈: {traceback.format_exc()}")
    
    def get_image_url(self, image_key: str):
        """
        获取图片的URL
        :param image_key: 图片key
        :return: 图片URL
        """
        try:
            token = self.feishu_messenger.get_tenant_access_token()
            
            # 使用正确的API端点获取图片信息
            url = f"{Config.FEISHU_API_BASE}/im/v1/messages/images/{image_key}"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            import requests
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"获取图片信息成功: {result}")
            
            if result.get("code") == 0:
                # 尝试不同的字段路径获取图片URL
                data = result.get("data", {})
                image_url = data.get("image_url") or data.get("url")
                if image_url:
                    return image_url
                else:
                    logger.error(f"图片信息中未找到URL: {data}")
                    return None
            else:
                logger.error(f"获取图片URL失败: {result.get('msg', '未知错误')}")
                return None
                
        except Exception as e:
            logger.error(f"获取图片URL异常: {str(e)}")
            import traceback
            logger.error(f"错误堆栈: {traceback.format_exc()}")
            return None
    
    def handle_image_message(self, user_id: str, image_key: str, image_url: str = None):
        """
        处理图片消息
        :param user_id: 用户open_id
        :param image_key: 图片key
        :param image_url: 图片URL（可选）
        """
        try:
            self.feishu_messenger.send_message(user_id, "📸 正在分析图片，请稍候...")
            
            # 先尝试使用传入的image_url
            if not image_url:
                # 如果没有传入URL，尝试从API获取
                image_url = self.get_image_url(image_key)
                
            if image_url:
                logger.info(f"使用图片URL: {image_url}")
                
                # 使用豆包API分析图片
                # 先尝试专门的股票图片分析
                analysis = self.image_analyzer.analyze_stock_image(image_url)
                
                if not analysis:
                    # 如果股票分析失败，使用通用分析
                    analysis = self.image_analyzer.analyze_image(image_url)
                
                if analysis:
                    # 尝试基于分析结果生成更专业的提示词
                    prompt = self.image_analyzer.generate_stock_prompt(analysis)
                    
                    if prompt:
                        # 使用生成的提示词
                        combined_question = prompt
                    else:
                        # 使用原始分析结果
                        combined_question = f"图片分析结果：{analysis}\n\n请根据图片内容和上述分析，提供相关的股票分析或建议"
                    
                    logger.info(f"将图片分析结果转发给Coze智能体...")
                    answer = self.coze_manager.call_coze_with_context(user_id, combined_question)
                    
                    import time
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                    title = f"【{timestamp} 图片分析 + 智能体回复】"
                    
                    full_content = f"**图片分析结果：**\n{analysis}\n\n**智能体回答：**\n{answer}"
                    
                    success = self.feishu_messenger.send_card_message(user_id, title, full_content)
                    
                    if success:
                        logger.info(f"✅ 成功处理图片消息并回复用户 {user_id}")
                    else:
                        logger.error(f"❌ 回复用户 {user_id} 失败")
                else:
                    # 图片分析失败，直接告诉用户分析不了图片
                    logger.info("豆包API分析失败，告知用户无法分析图片")
                    
                    success = self.feishu_messenger.send_message(user_id, "❌ 抱歉，无法分析图片内容。请尝试重新发送图片或提供更多信息。")
                    
                    if success:
                        logger.info(f"✅ 已告知用户无法分析图片 {user_id}")
                    else:
                        logger.error(f"❌ 回复用户 {user_id} 失败")
            else:
                # 本地上传图片，没有URL的情况
                logger.info(f"检测到本地上传图片，没有URL可用")
                
                # 尝试从飞书API下载图片
                logger.info("尝试从飞书API下载图片...")
                
                try:
                    # 从飞书API获取图片内容
                    # 正确的API端点: https://open.feishu.cn/open-apis/im/v1/images/{image_key}
                    token = self.feishu_messenger.get_tenant_access_token()
                    image_download_url = f"{Config.FEISHU_API_BASE}/im/v1/images/{image_key}"
                    headers = {
                        "Authorization": f"Bearer {token}"
                    }
                    
                    import requests
                    response = requests.get(image_download_url, headers=headers, timeout=30)
                    
                    # 打印响应信息用于调试
                    logger.info(f"图片下载响应状态码: {response.status_code}")
                    logger.info(f"图片下载响应头: {dict(response.headers)}")
                    
                    response.raise_for_status()
                    
                    # 读取图片二进制数据
                    image_content = response.content
                    logger.info(f"成功下载图片，大小: {len(image_content) / 1024 / 1024:.2f} MB")
                    
                    # 转换为base64格式
                    import base64
                    base64_image = base64.b64encode(image_content).decode('utf-8')
                    base64_url = f"data:image/jpeg;base64,{base64_image}"
                    
                    # 使用豆包API分析图片
                    logger.info("使用豆包API分析本地图片...")
                    analysis = self.image_analyzer.analyze_stock_image(base64_url)
                    
                    if not analysis:
                        # 如果股票分析失败，使用通用分析
                        analysis = self.image_analyzer.analyze_image(base64_url)
                    
                    if analysis:
                        # 生成提示词并询问Coze
                        prompt = self.image_analyzer.generate_stock_prompt(analysis)
                        
                        if prompt:
                            combined_question = prompt
                        else:
                            combined_question = f"图片分析结果：{analysis}\n\n请根据图片内容和上述分析，提供相关的股票分析或建议"
                        
                        logger.info(f"将豆包分析结果转发给Coze智能体...")
                        answer = self.coze_manager.call_coze_with_context(user_id, combined_question)
                        
                        import time
                        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                        title = f"【{timestamp} 本地图片分析 + 智能体回复】"
                        
                        full_content = f"**图片分析结果：**\n{analysis}\n\n**智能体回答：**\n{answer}"
                        
                        success = self.feishu_messenger.send_card_message(user_id, title, full_content)
                    else:
                        # 本地图片分析失败
                        logger.info("豆包API分析失败，告知用户无法分析本地图片")
                        success = self.feishu_messenger.send_message(user_id, "❌ 抱歉，无法分析本地图片内容。请尝试重新发送图片或提供更多信息。")
                        
                except Exception as e:
                    logger.error(f"下载和分析本地图片失败: {str(e)}")
                    import traceback
                    logger.error(f"错误堆栈: {traceback.format_exc()}")
                    success = self.feishu_messenger.send_message(user_id, "❌ 抱歉，下载图片失败。请尝试重新发送图片或提供更多信息。")
                    
                if success:
                    logger.info(f"✅ 已处理本地图片并回复用户 {user_id}")
                else:
                    logger.error(f"❌ 回复用户 {user_id} 失败")
                
        except Exception as e:
            logger.error(f"处理图片消息失败: {str(e)}")
            try:
                # 即使出错，也要给用户一个合理的回复
                fallback_answer = "我已经收到了您发送的股票截图。虽然图片分析遇到了技术问题，但基于您的上下文，我可以为您提供股票分析服务。请告诉我您关注的具体股票，我会为您分析其走势和投资建议。"
                self.feishu_messenger.send_message(user_id, fallback_answer)
            except:
                pass
    
    def process_user_message(self, user_id: str, message: str):
        try:
            if message in ["订阅", "subscribe"]:
                self.scheduler.add_subscriber(user_id)
                self.feishu_messenger.send_message(user_id, "✅ 已成功订阅股票分析推送！")
                logger.info(f"用户 {user_id} 订阅成功")
                
            elif message in ["取消订阅", "unsubscribe"]:
                self.scheduler.remove_subscriber(user_id)
                self.feishu_messenger.send_message(user_id, "❌ 已取消订阅股票分析推送")
                logger.info(f"用户 {user_id} 取消订阅")
                
            elif message in ["立即分析", "analyze", "now"]:
                result = self.scheduler.send_immediate_analysis(user_id)
                self.feishu_messenger.send_message(user_id, result)
                logger.info(f"用户 {user_id} 请求立即分析")
                
            elif message in ["清空上下文", "clear", "reset"]:
                self.coze_manager.clear_session(user_id)
                self.openclaw_manager.clear_session(user_id)
                self.feishu_messenger.send_message(user_id, "✅ 对话上下文已清空")
                logger.info(f"用户 {user_id} 清空上下文")
                
            elif message in ["使用Coze", "use_coze", "coze"]:
                self.user_ai_preference[user_id] = "coze"
                self.feishu_messenger.send_message(user_id, "✅ 已切换到 Coze 智能体")
                logger.info(f"用户 {user_id} 切换到 Coze")
                
            elif message in ["使用OpenClaw", "use_openclaw", "openclaw"]:
                self.user_ai_preference[user_id] = "openclaw"
                self.feishu_messenger.send_message(user_id, "✅ 已切换到 OpenClaw 智能体")
                logger.info(f"用户 {user_id} 切换到 OpenClaw")
                
            elif message in ["帮助", "help", "?"]:
                current_ai = self.user_ai_preference.get(user_id, "coze")
                help_text = f"""
📖 可用命令：
• 订阅 - 订阅股票分析推送
• 取消订阅 - 取消订阅
• 立即分析 - 立即获取股票分析
• 清空上下文 - 清空对话历史
• 使用Coze - 切换到 Coze 智能体
• 使用OpenClaw - 切换到 OpenClaw 智能体
• 帮助 - 显示此帮助信息

💬 其他问题会直接与智能体对话
📸 发送图片可进行图片分析

🤖 当前使用的智能体: {current_ai.upper()}
                """.strip()
                self.feishu_messenger.send_message(user_id, help_text)
                
            else:
                current_ai = self.user_ai_preference.get(user_id, "coze")
                logger.info(f"用户 {user_id} 使用 {current_ai} 智能体")
                
                if current_ai == "openclaw":
                    logger.info(f"转发用户 {user_id} 的问题到 OpenClaw...")
                    answer = self.openclaw_manager.call_openclaw_with_context(user_id, message)
                    ai_name = "OpenClaw"
                else:
                    logger.info(f"转发用户 {user_id} 的问题到 Coze...")
                    answer = self.coze_manager.call_coze_with_context(user_id, message)
                    ai_name = "Coze"
                
                import time
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                title = f"【{timestamp} {ai_name} 智能体回复】"
                
                full_content = f"**我的问题：**\n{message}\n\n**{ai_name}回答：**\n{answer}"
                
                success = self.feishu_messenger.send_card_message(user_id, title, full_content)
                
                if success:
                    logger.info(f"✅ 成功回复用户 {user_id}")
                else:
                    logger.error(f"❌ 回复用户 {user_id} 失败")
                    
        except Exception as e:
            logger.error(f"处理用户消息失败: {str(e)}")
            try:
                self.feishu_messenger.send_message(user_id, f"❌ 处理失败: {str(e)}")
            except:
                pass
    
    def start(self):
        try:
            event_handler = lark.EventDispatcherHandler.builder(Config.FEISHU_VERIFICATION_TOKEN, Config.FEISHU_ENCRYPT_KEY) \
                .register_p2_im_message_receive_v1(self.handle_message) \
                .build()
            
            self.client = lark.ws.Client(Config.FEISHU_APP_ID, Config.FEISHU_APP_SECRET,
                                      event_handler=event_handler, log_level=lark.LogLevel.INFO)
            
            logger.info("飞书WebSocket服务器启动中...")
            logger.info(f"App ID: {Config.FEISHU_APP_ID}")
            logger.info(f"App Secret: {Config.FEISHU_APP_SECRET[:10]}...")
            logger.info(f"Verification Token: {Config.FEISHU_VERIFICATION_TOKEN[:10]}...")
            
            self.client.start()
            logger.info("飞书WebSocket服务器已启动")
            
        except Exception as e:
            logger.error(f"启动失败: {str(e)}")
            raise
    
    def stop(self):
        if self.client:
            try:
                self.client.stop()
                logger.info("飞书WebSocket服务器已停止")
            except Exception as e:
                logger.error(f"停止失败: {str(e)}")

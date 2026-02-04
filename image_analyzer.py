import requests
import base64
import json
from typing import Optional
from config import Config

class DoubaoImageAnalyzer:
    def __init__(self):
        self.api_key = Config.DOUB_KEY
        self.api_url = Config.DOUB_API_URL
        self.model = Config.DOUB_MODEL
    
    def analyze_image(self, image_url: str) -> Optional[str]:
        """
        使用豆包API分析图像内容
        :param image_url: 图像URL
        :return: 图像分析结果
        """
        if not self.api_key:
            print("⚠️  DOUB_KEY 未配置")
            return None
        
        try:
            print(f"📸 正在分析图像: {image_url}")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "请详细分析这张图片的内容，描述图片中包含的所有重要信息"
                        },
                        {
                            "type": "image",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ]
            
            data = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            response = requests.post(
                self.api_url,
                json=data,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                analysis = result["choices"][0]["message"]["content"]
                print(f"✅ 图像分析完成: {analysis[:100]}...")
                return analysis
            else:
                print(f"❌ 图像分析失败: {result}")
                return None
                
        except Exception as e:
            print(f"❌ 图像分析异常: {str(e)}")
            return None
    
    def analyze_image_from_content(self, image_content: bytes) -> Optional[str]:
        """
        分析二进制图像内容
        :param image_content: 图像二进制数据
        :return: 图像分析结果
        """
        try:
            base64_image = base64.b64encode(image_content).decode('utf-8')
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "请详细分析这张图片的内容"
                        },
                        {
                            "type": "image",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
            
            data = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            response = requests.post(
                self.api_url,
                json=data,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                analysis = result["choices"][0]["message"]["content"]
                return analysis
            else:
                return None
                
        except Exception as e:
            print(f"❌ 二进制图像分析失败: {str(e)}")
            return None
    
    def analyze_stock_image(self, image_path: str) -> Optional[str]:
        """
        专门分析股票相关图片并生成提示词
        :param image_path: 图像路径或URL
        :return: 股票图片分析结果和提示词
        """
        if not self.api_key:
            print("⚠️  DOUB_KEY 未配置")
            return None
        
        try:
            print(f"📈 正在分析股票图像: {image_path}")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 准备图片数据
            image_data = None
            if image_path.startswith('http'):
                # 是URL
                image_url = image_path
            else:
                # 是本地文件，需要读取并转换为base64
                try:
                    with open(image_path, 'rb') as f:
                        image_bytes = f.read()
                    import base64
                    image_data = base64.b64encode(image_bytes).decode('utf-8')
                    image_url = f"data:image/jpeg;base64,{image_data}"
                except Exception as file_error:
                    print(f"❌ 读取本地文件失败: {file_error}")
                    return None
            
            # 使用豆包API的正确格式
            data = {
                "model": self.model,
                "input": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_image",
                                "image_url": image_url
                            },
                            {
                                "type": "input_text",
                                "text": "请详细分析这张股票相关图片，包括但不限于：\n1. 图片类型（K线图、分时图、成交量图等）\n2. 股票名称和代码（如果可见）\n3. 当前价格和涨跌幅\n4. 技术指标状态（MACD、KDJ、RSI等）\n5. 成交量情况\n6. 价格走势形态\n7. 支撑位和阻力位\n8. 其他重要信息\n\n请以结构化的方式输出分析结果，最后基于分析结果生成一个适合股票分析的提示词。"
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(
                self.api_url,
                json=data,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            
            if "output" in result:
                analysis = result["output"]["text"]
                print(f"✅ 股票图像分析完成: {analysis[:100]}...")
                return analysis
            else:
                print(f"❌ 股票图像分析失败: {result}")
                return None
                
        except Exception as e:
            print(f"❌ 股票图像分析异常: {str(e)}")
            return None
    
    def generate_stock_prompt(self, analysis: str) -> Optional[str]:
        """
        基于图片分析结果生成股票分析提示词
        :param analysis: 图片分析结果
        :return: 股票分析提示词
        """
        if not analysis:
            return None
        
        try:
            print("📝 正在生成股票分析提示词...")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 使用豆包API的正确格式
            data = {
                "model": self.model,
                "input": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": f"基于以下股票图片分析结果，生成一个专业的股票分析提示词，用于请求更深入的股票分析：\n\n{analysis}\n\n提示词应该包含：\n1. 股票的关键信息\n2. 需要分析的技术指标\n3. 关注的价格走势\n4. 资金流向分析需求\n5. 投资建议请求\n\n请生成一个结构清晰、信息完整的提示词。"
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(
                self.api_url,
                json=data,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            
            if "output" in result:
                prompt = result["output"]["text"]
                print(f"✅ 股票分析提示词生成完成: {prompt[:100]}...")
                return prompt
            else:
                print(f"❌ 提示词生成失败: {result}")
                return None
                
        except Exception as e:
            print(f"❌ 提示词生成异常: {str(e)}")
            return None

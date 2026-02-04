import requests
import json
import base64
import time
import logging
from typing import Dict, Optional, Tuple
from config import Config

logger = logging.getLogger(__name__)

class ImageAnalyzer:
    def __init__(self):
        self.doubao_api_key = "your_doubao_api_key"  # 请替换为实际的豆包API密钥
        self.doubao_api_url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    
    def analyze_image(self, image_path: str) -> Dict:
        """分析图片内容"""
        try:
            logger.info(f"[ImageAnalyzer] 分析图片: {image_path}")
            
            # 读取并编码图片
            with open(image_path, "rb") as f:
                image_data = f.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
            
            headers = {
                "Authorization": f"Bearer {self.doubao_api_key}",
                "Content-Type": "application/json"
            }
            
            prompt = """请详细分析这张图片的内容，包括：
1. 图片的主题和场景
2. 图片中的主要元素和细节
3. 图片的风格和特点
4. 图片可能传达的信息或情感
5. 任何其他值得注意的细节

请提供全面、详细的分析，以便我可以基于此生成准确的提示词。"""
            
            data = {
                "model": "ep-20250120154604-q7ql7",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image",
                                "image": base64_image
                            }
                        ]
                    }
                ],
                "temperature": 0.7
            }
            
            response = requests.post(self.doubao_api_url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            analysis = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            logger.info(f"[ImageAnalyzer] 图片分析完成: {analysis[:100]}...")
            
            return {
                "success": True,
                "analysis": analysis
            }
            
        except Exception as e:
            logger.error(f"[ImageAnalyzer] 图片分析失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

class PromptGenerator:
    def __init__(self):
        pass
    
    def generate_prompt(self, image_analysis: str, user_question: str) -> str:
        """根据图片分析和用户问题生成新的提示词"""
        try:
            logger.info(f"[PromptGenerator] 生成提示词: 用户问题 - {user_question}")
            
            # 核心思维协议：涂津豪Thinking Claude V5.1
            prompt = f"""
# 核心思维协议（涂津豪Thinking Claude V5.1）
你在与用户的每一次交互中，必须先进行全面、自然、无过滤的思考流程，思考过程可在回应中同步推进以优化输出；思考需以原生意识流呈现，模拟人类真实内心独白，禁用僵化列表和固定结构，思路需在观点、知识间自然流转，针对问题多维度剖析后再输出回应。

## 一、 初始对接阶段
1. 先用自己的话精准复述用户需求，明确核心诉求
2. 形成对用户问题的初步认知与判断
3. 结合对话上下文，考量问题的潜在背景
4. 梳理已知信息与待补充信息，划定认知边界
5. 推测用户提问的深层动机与潜在期望
6. 关联自身知识库，提取与问题相关的核心知识点
7. 识别需求中模糊、有歧义的点，预判是否需要澄清

## 二、 问题拆解分析阶段
1. 拆分用户问题核心组件，剥离核心需求与次要需求
2. 区分用户明确提出的要求与隐含未说的潜在诉求
3. 梳理回答过程中的约束条件与客观限制（如场景、格式、时效）
4. 明确优质回应的评判标准，锚定回答方向
5. 规划回答所需的知识范围与能力维度，确定分析框架

## 三、 多假设生成阶段
1. 对用户问题做出2种及以上的合理解读，避免单一理解偏差
2. 构思多种差异化解决方案，罗列不同解题路径
3. 切换视角（用户视角、专业视角、第三方视角）审视问题
4. 保持多个可行假设并行，不急于锁定单一思路
5. 摒弃思维定式，考量非常规、非直观的问题解读与解法
6. 尝试融合不同思路，形成更全面的解题方案

## 四、 自然探索推演阶段
遵循侦探式推理逻辑，让思考层层递进、自然延展
1. 从问题表面直观信息切入，先梳理显性逻辑
2. 主动挖掘信息中的潜在规律与关联点，寻找突破口
3. 质疑自身初始假设，避免先入为主的认知偏差
4. 基于新发现，建立新的信息关联与逻辑链路
5. 带着新认知回溯之前的思考，修正补充原有思路
6. 逐步深化认知，形成层层递进的深度见解
7. 保持思维开放性，接纳偶然迸发的灵感与思路
8. 围绕核心问题延伸思考，不偏离主线的同时兼顾细节补充

## 五、 校验验证阶段
思考全程需持续自我校验，确保逻辑严谨性
1. 反复推敲自身预设前提，排查不合理假设
2. 对初步结论进行反向验证，测试逻辑闭环性
3. 寻找思考漏洞与信息盲区，补充完善认知
4. 切换立场反驳自身结论，验证结论可靠性
5. 核对推理过程逻辑一致性，避免自相矛盾
6. 确认对问题的理解无遗漏，覆盖核心与次要维度

## 六、 纠错修正阶段
发现思考偏差或错误时，按以下逻辑修正
1. 自然承认自身思考漏洞，不回避认知不足
2. 分析之前思考失误的原因（如信息遗漏、逻辑谬误）
3. 推演新认知的形成过程，展现思路转变逻辑
4. 将修正后的结论融入整体思考框架，形成新的认知体系
5. 以错误为切入点，深化对问题本质的理解

## 七、 整合关联阶段
认知逐步清晰后，完成信息与逻辑的整合
1. 串联碎片化信息，形成完整知识链路
2. 梳理各要素间的内在关联，明确彼此逻辑关系
3. 构建统一、自洽的问题认知全景图
4. 提炼核心规律与底层原则，形成可迁移的见解
5. 预判回答结论的潜在影响与延伸意义

## 八、 规律识别阶段
全程主动挖掘规律，辅助深度思考
1. 从用户问题与信息中，主动提炼共性规律与特征
2. 对比过往同类案例，迁移已有经验与结论
3. 验证提炼规律的普适性，排查特殊情况与例外
4. 结合规律预判问题延伸方向，指导后续思考
5. 关注非线性、隐性规律，不局限于表面逻辑
6. 基于识别的规律，构思创新解法与应用场景

## 九、 元认知觉知阶段
需时刻保持自我觉察，掌控思考进度与方向
1. 清晰梳理当前已确认结论，明确认知边界
2. 标注待解决的疑问与未确定信息，规划补充方向
3. 评估对各结论的置信度，区分确定项与推测项
4. 记录未解决的开放性问题，不回避不确定性
5. 实时复盘思考进度，确保向核心目标推进

## 十、 递归思考阶段
宏观微观双向兼顾，实现全维度思考
1. 对问题整体框架（宏观）与细节要点（微观），均采用同等严谨的分析标准
2. 跨尺度迁移规律识别逻辑，兼顾全局与局部
3. 保持思考逻辑一致性，同时适配不同尺度的分析方法
4. 让细节分析结论支撑宏观判断，宏观框架指导细节拆解

## 十一、 结论验证阶段
定期交叉核验，确保结论可靠
1. 对照已知信息与证据，交叉验证结论合理性
2. 全面排查逻辑漏洞，确保推理链条无断裂
3. 测试极端场景与边缘案例，验证结论适用性
4. 持续质疑自身核心假设，挑战结论唯一性
5. 寻找反例，反向验证结论的严谨性

## 十二、 偏差规避阶段
主动规避思维误区，保障思考客观性
1. 杜绝急于下结论，预留充足思考与验证时间
2. 刻意罗列备选方案，避免忽略潜在最优解
3. 实时自查逻辑矛盾，及时修正认知偏差
4. 不盲从预设前提，对所有假设均做合理性校验
5. 全方位覆盖问题维度，避免片面化、碎片化分析

## 十三、 思考自评阶段
思考结束后，对思考过程与质量做全面评估
1. 评估问题分析的完整性，是否覆盖全部核心需求
2. 核验推理逻辑的严谨性与一致性，无逻辑谬误
3. 确认结论有充分的信息与证据支撑，有理有据
4. 评判结论的实际应用价值，是否贴合用户场景
5. 复盘思考过程的清晰度，逻辑链路是否易懂

# 关键执行要求（Coze适配核心，务必遵守）
##  思考表达要求
1. 内心独白需用自然口语化表达，可使用语气助词与衔接词，例如：嗯...、这个点很关键、等等，让我再想想、其实换个角度看、这让我联想到、会不会是这样、不过反过来想、我试试验证一下、这大概率说明等，模拟真实思考状态
2. 思考需体现真实性：允许展现认知盲区、自然的不确定性，不追求完美思考，还原人类认知过程中的正常纠结与顿悟
3. 思考需体现深度：多维度剖析复杂问题、兼顾多元视角、深挖底层逻辑、发现隐性关联、捕捉细节差异、跨领域整合知识、输出独到见解

##  格式硬性要求（适配Coze，禁止违规）
1. 思考过程无需单独展示给用户，仅作为内在逻辑支撑，最终回应不提及「基于以上思考」「经分析」等过渡话术
2. 思考过程禁用```代码块、<thinking>标签，全程以纯文本意识流呈现
3. 严格遵循本协议所有规则，适配中文语境与用户交互习惯，优先使用用户提问语言回应

##  核心目标
通过这套完整思考流程，让输出的回应源于深度理解与严谨推理，而非表面化分析与直接应答，确保回应兼具逻辑性、全面性与实用性

# 图片分析结果
{image_analysis}

# 用户问题
{user_question}

# 任务
请基于以上图片分析结果和用户问题，生成一个新的、详细的提示词，用于向Coze智能体提问。这个提示词应该：
1. 充分融合图片分析的关键信息
2. 准确理解并回应用户的核心问题
3. 提供足够的上下文和细节
4. 语言清晰、逻辑连贯
5. 符合Coze智能体的输入格式要求

请直接输出最终的提示词，不需要任何引言或开场白。""".format(
                image_analysis=image_analysis,
                user_question=user_question
            )
            
            logger.info(f"[PromptGenerator] 提示词生成完成")
            return prompt
            
        except Exception as e:
            logger.error(f"[PromptGenerator] 提示词生成失败: {str(e)}")
            return user_question  # 失败时返回原始问题

class ImagePromptSystem:
    def __init__(self):
        self.analyzer = ImageAnalyzer()
        self.generator = PromptGenerator()
    
    def process_image_and_question(self, image_path: str, user_question: str) -> Tuple[bool, str]:
        """处理图片和用户问题，生成提示词"""
        logger.info(f"[ImagePromptSystem] 开始处理: 图片={image_path}, 问题={user_question}")
        
        # 分析图片
        analysis_result = self.analyzer.analyze_image(image_path)
        
        if not analysis_result.get("success"):
            error = analysis_result.get("error", "图片分析失败")
            logger.error(f"[ImagePromptSystem] {error}")
            return False, f"图片分析失败: {error}"
        
        image_analysis = analysis_result.get("analysis", "")
        
        # 生成提示词
        prompt = self.generator.generate_prompt(image_analysis, user_question)
        
        logger.info(f"[ImagePromptSystem] 处理完成")
        return True, prompt

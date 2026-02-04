# 飞书股票智能机器人

一个基于飞书企业自建应用的智能股票分析机器人，支持双向问答、定时推送和上下文连贯对话。

## 功能特性

✅ **双向问答**
- 发送消息到飞书机器人，自动转发到Coze智能体
- 智能体回复后，通过飞书推送回您

✅ **定时自动推送**
- 每天定时自动询问股票问题
- 自动推送分析结果到飞书

✅ **上下文连贯**
- 维持对话历史，支持连续对话
- 每个用户独立的对话上下文

✅ **本地WebSocket长连接**
- 无需公网服务器
- Windows后台挂起运行

## 系统架构

```
飞书机器人 ←→ WebSocket服务器 ←→ Coze上下文管理器 ←→ Coze API
    ↓                                              ↑
定时任务调度器 ←→ 飞书消息推送 ←───────────────────┘
```

## 文件结构

```
coze_wx/
├── config.py              # 配置管理
├── coze_manager.py        # Coze上下文管理
├── feishu_messenger.py    # 飞书消息推送
├── stock_scheduler.py     # 定时任务调度
├── feishu_websocket.py    # 飞书WebSocket服务器
├── main.py                # 主程序入口
├── requirements.txt       # 依赖包
├── .env.example          # 环境变量示例
└── README.md             # 说明文档
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置飞书应用

#### 2.1 创建飞书企业自建应用

1. 登录[飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取以下信息：
   - App ID
   - App Secret

#### 2.2 配置机器人权限

在飞书开放平台配置以下权限：

- `im:message` - 发送消息
- `im:message:group_at_msg` - 群组@消息
- `im:resource` - 获取资源信息

#### 2.3 启用事件订阅

1. 在飞书开放平台启用事件订阅
2. 订阅以下事件：
   - `im.message.receive_v1` - 接收消息事件

#### 2.4 获取验证信息

- Verification Token
- Encrypt Key

### 3. 配置环境变量

复制 `.env.example` 为 `.env`，并填入配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
FEISHU_APP_ID=your_feishu_app_id
FEISHU_APP_SECRET=your_feishu_app_secret
FEISHU_VERIFICATION_TOKEN=your_verification_token
FEISHU_ENCRYPT_KEY=your_encrypt_key
```

### 4. 启动机器人

```bash
python main.py
```

## 使用说明

### 可用命令

发送以下命令到飞书机器人：

- **订阅** - 订阅股票分析推送
- **取消订阅** - 取消订阅
- **立即分析** - 立即获取股票分析
- **清空上下文** - 清空对话历史
- **帮助** - 显示帮助信息

### 自由对话

发送任何其他问题，机器人会：
1. 转发到Coze智能体
2. 维持对话上下文
3. 推送智能体回复

### 图片分析

发送图片到机器人，会自动：
1. 使用豆包API分析图片内容
2. 将分析结果转发到Coze智能体
3. 智能体结合图片内容给出股票分析
4. 推送完整分析结果

### 定时推送

默认在以下时间自动推送股票分析：
- 09:00 - 早盘分析
- 15:00 - 收盘分析
- 20:00 - 晚间分析

可在 `config.py` 中修改 `SCHEDULE_TIMES` 调整推送时间。

## 配置说明

### config.py 配置项

```python
# Coze API配置
COZE_API_URL = "https://8mbn769hk8.coze.site/stream_run"
COZE_BEARER_TOKEN = "your_token"
COZE_PROJECT_ID = 7598933258117611561

# 飞书API配置
FEISHU_APP_ID = ""
FEISHU_APP_SECRET = ""
FEISHU_VERIFICATION_TOKEN = ""
FEISHU_ENCRYPT_KEY = ""

# 定时推送时间
SCHEDULE_TIMES = ["09:00", "15:00", "20:00"]

# 默认股票问题
DEFAULT_STOCK_QUESTION = "帮我分析今天A股的整体走势..."
```

## 运行模式

### 前台运行

```bash
python main.py
```

### 后台运行（Windows）

使用 `start` 命令：

```bash
start /B python main.py
```

或使用 `pythonw`：

```bash
pythonw main.py
```

### 使用服务管理（推荐）

使用 NSSM 将其注册为Windows服务：

```bash
nssm install FeishuStockBot "C:\Python39\python.exe" "E:\coze_wx\main.py"
nssm start FeishuStockBot
```

## 日志查看

日志文件：`feishu_bot.log`

```bash
# 实时查看日志
tail -f feishu_bot.log

# Windows PowerShell
Get-Content feishu_bot.log -Wait
```

## 故障排查

### 问题1：无法连接飞书WebSocket

**解决方案：**
1. 检查网络连接
2. 确认飞书应用权限已正确配置
3. 检查 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET` 是否正确

### 问题2：Coze API调用失败

**解决方案：**
1. 检查 `COZE_BEARER_TOKEN` 是否有效
2. 确认 `COZE_PROJECT_ID` 正确
3. 查看日志中的详细错误信息

### 问题3：定时任务不执行

**解决方案：**
1. 检查系统时间是否正确
2. 确认 `SCHEDULE_TIMES` 格式正确（HH:MM）
3. 查看日志确认调度器是否正常启动

### 问题4：消息推送失败

**解决方案：**
1. 确认用户已订阅
2. 检查飞书消息推送权限
3. 查看日志中的错误信息

## 安全建议

1. **不要将 `.env` 文件提交到版本控制**
2. **定期更换 API Token**
3. **限制飞书应用的使用范围**
4. **监控日志文件大小**

## 扩展功能

### 添加新的定时任务

在 `stock_scheduler.py` 中添加：

```python
def custom_task(self):
    pass

# 在 schedule_tasks() 中注册
schedule.every().day.at("12:00").do(self.custom_task)
```

### 添加新的命令

在 `feishu_websocket.py` 的 `process_user_message()` 中添加：

```python
elif message == "新命令":
    self.feishu_messenger.send_message(user_id, "回复内容")
```

### 自定义股票问题

修改 `config.py` 中的 `DEFAULT_STOCK_QUESTION`。

## 技术栈

- **Python 3.7+**
- **飞书开放平台 API**
- **Coze 智能体 API**
- **WebSocket**
- **多线程**
- **定时任务调度**

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题，请提交 Issue。

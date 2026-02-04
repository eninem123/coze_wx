# 飞书股票智能机器人 - 快速使用指南

## 🎯 系统功能

### ✅ 核心功能

1. **双向问答**
   - 发送消息到飞书机器人
   - 自动转发到Coze智能体
   - 智能体回复后推送回飞书

2. **定时自动推送**
   - 每天 09:00、15:00、20:00 自动推送股票分析
   - 支持多用户订阅
   - 可自定义推送时间和问题

3. **上下文连贯**
   - 维持对话历史
   - 支持连续对话
   - 每个用户独立上下文

4. **本地运行**
   - 无需公网服务器
   - WebSocket长连接
   - Windows后台挂起

## 📁 文件结构

```
coze_wx/
├── config.py              # 配置管理
├── coze_manager.py        # Coze上下文管理
├── feishu_messenger.py    # 飞书消息推送
├── stock_scheduler.py     # 定时任务调度
├── feishu_websocket.py    # 飞书WebSocket服务器
├── main.py                # 主程序入口
├── test_system.py         # 系统测试脚本
├── start.bat              # Windows启动脚本
├── requirements.txt       # Python依赖
├── .env                   # 环境变量配置
└── README.md              # 详细文档
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置飞书应用

已配置的飞书应用信息：
- **App ID**: `cli_a909df14e7f85bc0`
- **App Secret**: `GMw20dEYICen1AWS7NC02ZgqcQHkLaBV`

### 3. 启动机器人

**方式一：使用启动脚本（推荐）**
```bash
start.bat
```

**方式二：直接运行**
```bash
python main.py
```

**方式三：后台运行**
```bash
start /B python main.py
```

## 💬 使用说明

### 可用命令

在飞书中发送以下命令：

| 命令 | 功能 |
|------|------|
| `订阅` | 订阅股票分析推送 |
| `取消订阅` | 取消订阅 |
| `立即分析` | 立即获取股票分析 |
| `清空上下文` | 清空对话历史 |
| `帮助` | 显示帮助信息 |

### 自由对话

发送任何其他问题，机器人会：
1. 转发到Coze智能体
2. 维持对话上下文
3. 推送智能体回复

### 示例对话

```
用户: 帮我分析今天A股走势
机器人: [智能体回复A股分析]

用户: 半导体板块怎么样？
机器人: [智能体回复半导体分析，基于上下文]

用户: 订阅
机器人: ✅ 已成功订阅股票分析推送！

用户: 立即分析
机器人: ✅ 股票分析已发送
```

## ⚙️ 配置说明

### 修改定时推送时间

编辑 `config.py`：

```python
SCHEDULE_TIMES = ["09:00", "15:00", "20:00"]
```

### 修改默认股票问题

编辑 `config.py`：

```python
DEFAULT_STOCK_QUESTION = "帮我分析今天A股的整体走势..."
```

### 修改Coze配置

编辑 `config.py`：

```python
COZE_API_URL = "https://8mbn769hk8.coze.site/stream_run"
COZE_BEARER_TOKEN = "your_token"
COZE_PROJECT_ID = 7598933258117611561
```

## 🔍 系统测试

运行测试脚本：

```bash
python test_system.py
```

测试内容：
- ✅ 配置模块
- ✅ Coze上下文管理
- ✅ 飞书消息推送
- ✅ 定时任务调度

## 📊 日志查看

日志文件：`feishu_bot.log`

**实时查看日志（PowerShell）：**
```powershell
Get-Content feishu_bot.log -Wait
```

**查看最近100行：**
```powershell
Get-Content feishu_bot.log -Tail 100
```

## 🛠️ 故障排查

### 问题1：无法连接飞书WebSocket

**检查项：**
- 网络连接是否正常
- 飞书应用权限是否配置
- `.env` 文件中的 App ID 和 Secret 是否正确

**解决方案：**
```bash
# 测试飞书API连接
python -c "from feishu_messenger import FeishuMessenger; m = FeishuMessenger(); print(m.get_tenant_access_token())"
```

### 问题2：Coze API调用失败

**检查项：**
- `COZE_BEARER_TOKEN` 是否有效
- `COZE_PROJECT_ID` 是否正确
- 网络连接是否正常

**解决方案：**
```bash
# 测试Coze API连接
python -c "from coze_manager import CozeContextManager; m = CozeContextManager(); print(m.call_coze_with_context('test', '测试'))"
```

### 问题3：定时任务不执行

**检查项：**
- 系统时间是否正确
- `SCHEDULE_TIMES` 格式是否正确（HH:MM）
- 调度器是否正常启动

**解决方案：**
```bash
# 查看日志确认调度器状态
Get-Content feishu_bot.log | Select-String "定时任务"
```

## 🔐 安全建议

1. **不要将 `.env` 文件提交到版本控制**
2. **定期更换 API Token**
3. **限制飞书应用的使用范围**
4. **监控日志文件大小**

## 📈 性能优化

### 减少日志输出

编辑 `config.py`：

```python
logging.basicConfig(level=logging.WARNING)
```

### 限制对话历史长度

编辑 `coze_manager.py`：

```python
if len(self.sessions[user_id]) > 10:  # 改为10条
    self.sessions[user_id] = self.sessions[user_id][-10:]
```

### 调整WebSocket重连间隔

编辑 `feishu_websocket.py`：

```python
self.reconnect_interval = 10  # 改为10秒
```

## 🎓 高级用法

### 添加新的定时任务

编辑 `stock_scheduler.py`：

```python
def custom_task(self):
    pass

# 在 schedule_tasks() 中注册
schedule.every().day.at("12:00").do(self.custom_task)
```

### 添加新的命令

编辑 `feishu_websocket.py` 的 `process_user_message()`：

```python
elif message == "新命令":
    self.feishu_messenger.send_message(user_id, "回复内容")
```

### 自定义股票问题

修改 `config.py` 中的 `DEFAULT_STOCK_QUESTION`。

## 📞 技术支持

遇到问题？
1. 查看 `feishu_bot.log` 日志文件
2. 运行 `python test_system.py` 进行系统测试
3. 查看 `README.md` 详细文档

## 🎉 开始使用

```bash
# 1. 启动机器人
start.bat

# 2. 在飞书中发送
帮助

# 3. 开始对话
帮我分析今天A股走势

# 4. 订阅推送
订阅
```

---

**祝您使用愉快！** 🚀

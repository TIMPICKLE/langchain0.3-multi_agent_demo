# LangChain 0.3 多Agent协作演示项目

## 项目简介

这个项目展示了如何使用 LangChain 0.3 创建多个智能代理（Agent）协作完成复杂任务的完整流程。该演示专为初学者设计，通过一个实际的任务场景来展示多Agent系统的工作原理。

## 项目特点

- 🤖 **多Agent协作**: 演示4个不同角色的Agent如何协作
- 📚 **完整教学**: 详细的代码注释和分步教程
- 🏠 **本地部署**: 使用公司内部LLM，无需依赖外部服务
- 🔧 **易于理解**: 清晰的代码结构和丰富的示例
- 📖 **详细文档**: 包含原理解释和最佳实践

## Agent角色说明

### 1. 研究员Agent (Researcher)
- **职责**: 收集和分析相关信息
- **技能**: 信息检索、数据分析、知识整理
- **输出**: 结构化的研究报告

### 2. 规划师Agent (Planner)
- **职责**: 制定详细的执行计划
- **技能**: 任务分解、时间规划、资源分配
- **输出**: 可执行的行动计划

### 3. 执行者Agent (Executor)
- **职责**: 根据计划执行具体任务
- **技能**: 任务执行、问题解决、进度跟踪
- **输出**: 执行结果和状态报告

### 4. 审查员Agent (Reviewer)
- **职责**: 质量检查和结果评估
- **技能**: 质量评估、错误检测、改进建议
- **输出**: 评估报告和改进建议

## 项目结构

```
multi_agent_demo/
├── README.md                    # 项目说明文档
├── requirements.txt             # 依赖包列表
├── config/
│   ├── __init__.py
│   └── llm_config.py           # LLM配置文件
├── agents/
│   ├── __init__.py
│   ├── base_agent.py           # 基础Agent类
│   ├── researcher_agent.py     # 研究员Agent
│   ├── planner_agent.py        # 规划师Agent
│   ├── executor_agent.py       # 执行者Agent
│   └── reviewer_agent.py       # 审查员Agent
├── workflows/
│   ├── __init__.py
│   ├── multi_agent_workflow.py # 多Agent工作流
│   └── task_coordinator.py     # 任务协调器
├── examples/
│   ├── __init__.py
│   ├── simple_demo.py          # 简单演示
│   ├── complex_demo.py         # 复杂场景演示
│   └── interactive_demo.py     # 交互式演示
├── docs/
│   ├── tutorial.md             # 详细教程
│   ├── concepts.md             # 核心概念解释
│   └── best_practices.md       # 最佳实践指南
└── tests/
    ├── __init__.py
    ├── test_agents.py          # Agent测试
    └── test_workflows.py       # 工作流测试
```

## 快速开始

### 1. 环境准备

```bash
# 克隆或下载项目
cd multi_agent_demo

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置LLM

编辑 `config/llm_config.py` 文件，配置您的LLM服务地址：

```python
LLM_BASE_URL = "http://10.6.12.215:6091/v1"
LLM_MODEL_NAME = "DeepSeek-V3-0324-HSW"
```

### 3. 运行演示

```bash
# 运行简单演示
python examples/simple_demo.py

# 运行交互式演示
python examples/interactive_demo.py
```

## 学习路径

1. **阅读概念文档**: 先了解多Agent系统的基本概念 ([docs/concepts.md](docs/concepts.md))
2. **查看简单示例**: 运行 `simple_demo.py` 了解基本流程
3. **深入学习**: 阅读详细教程 ([docs/tutorial.md](docs/tutorial.md))
4. **实践应用**: 修改和扩展示例代码
5. **最佳实践**: 学习生产环境的最佳实践 ([docs/best_practices.md](docs/best_practices.md))

## 核心特性

### Agent通信机制
- 使用LangChain的内置消息传递系统
- 支持同步和异步通信
- 完整的状态管理和错误处理

### 工作流编排
- 灵活的任务分配和调度
- 支持并行和串行执行
- 智能的依赖关系管理

### 可扩展性
- 模块化设计，易于添加新的Agent
- 标准化的接口和协议
- 丰富的配置选项

## 示例场景

### 场景1: 技术文档撰写
多个Agent协作完成一篇技术文档的撰写：
- 研究员收集技术资料
- 规划师制定文档结构
- 执行者撰写具体内容
- 审查员检查质量和一致性

### 场景2: 项目规划
协作制定软件项目开发计划：
- 研究员分析需求和技术栈
- 规划师制定开发计划和里程碑
- 执行者细化任务和时间估算
- 审查员评估可行性和风险

## 技术栈

- **LangChain 0.3**: 核心框架
- **Python 3.8+**: 编程语言
- **内部LLM**: DeepSeek-V3-0324-HSW
- **异步编程**: asyncio支持
- **类型提示**: 完整的类型注解

## 故障排除

### 常见问题

#### 1. 超时错误 (Timeout Error)
```
HTTPConnectionPool(host='10.6.12.215', port=6091): Read timed out. (read timeout=60)
```

**解决方案**:
```bash
# 运行自动修复脚本
python fix_timeout_issues.py

# 或手动测试连接
python test_llm_performance.py
```

**已优化设置**:
- 超时时间增加到120秒
- 降低max_tokens提高响应速度
- 优化Agent参数配置

#### 2. 连接失败
```
ConnectionError: Failed to connect to LLM service
```

**检查步骤**:
1. 确认LLM服务正在运行
2. 检查网络连接
3. 验证服务地址配置
4. 检查防火墙设置

#### 3. 所有任务失败

**快速诊断**:
```bash
# 基本连接测试
python -c "from config.llm_config import test_llm_connection; print('连接状态:', test_llm_connection())"

# 性能测试
python test_llm_performance.py

# 最小化修复
python fix_timeout_issues.py
```

### 性能优化

1. **降低复杂度**: 使用较小的max_tokens和简化的任务描述
2. **网络优化**: 确保稳定的网络连接
3. **服务器负载**: 避免在服务器高负载时运行
4. **参数调优**: 根据具体需求调整Agent参数

### 调试工具

- `test_llm_performance.py`: LLM性能测试
- `fix_timeout_issues.py`: 超时问题修复
- 日志文件: 查看详细错误信息

## 贡献指南

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

MIT License

# 快速开始指南

## 目录

1. [环境准备](#环境准备)
2. [安装依赖](#安装依赖)
3. [配置LLM服务](#配置llm服务)
4. [运行第一个示例](#运行第一个示例)
5. [理解示例代码](#理解示例代码)
6. [自定义工作流](#自定义工作流)
7. [常见问题](#常见问题)

## 环境准备

### 系统要求

- **操作系统**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python版本**: 3.8 或更高版本
- **内存**: 最少 4GB RAM，推荐 8GB+
- **存储**: 至少 1GB 可用空间

### 检查Python版本

打开命令行（Windows用户使用PowerShell），运行：

```bash
python --version
```

如果显示 `Python 3.8.x` 或更高版本，则可以继续。否则请先安装或升级Python。

### 下载项目

如果您还没有下载项目代码，可以通过以下方式获取：

1. **直接下载**：下载项目压缩包并解压到您选择的目录
2. **Git克隆**（如果您有Git）：
   ```bash
   git clone <repository-url>
   cd multi_agent_demo
   ```

## 安装依赖

### 1. 创建虚拟环境（推荐）

虚拟环境可以避免包冲突：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

激活后，您的命令行提示符前面会显示 `(venv)`。

### 2. 安装依赖包

```bash
pip install -r requirements.txt
```

安装完成后，您应该看到类似以下的输出：
```
Successfully installed langchain-0.3.1 requests-2.31.0 pydantic-2.5.0 ...
```

### 3. 验证安装

运行以下命令验证安装：

```bash
python -c "import langchain; print('LangChain版本:', langchain.__version__)"
```

应该显示类似：`LangChain版本: 0.3.1`

## 配置LLM服务

### 1. 检查现有配置

查看项目中的 `test_api.py` 文件，确认LLM服务配置：

```bash
# Windows PowerShell:
Get-Content APIs/test_api.py | Select-Object -First 20

# macOS/Linux:
head -20 APIs/test_api.py
```

### 2. 测试LLM连接

运行测试脚本确认LLM服务可用：

```bash
cd APIs
python test_api.py
```

如果看到成功的响应，说明LLM服务配置正确。

### 3. 修改配置（如果需要）

如果需要修改LLM服务地址或参数，编辑 `config/llm_config.py` 文件：

```python
# 修改基础URL（如果不同）
self.base_url = "http://your-llm-server:port/v1"

# 修改模型名称（如果不同）
self.model_name = "your-model-name"
```

## 运行第一个示例

### 1. 简单文档生成示例

这个示例将展示4个Agent协作创建一份技术文档：

```bash
cd examples
python simple_demo.py
```

您将看到类似以下的输出：

```
=== LangChain 0.3 多Agent协作演示 ===

正在初始化Agent系统...
✓ 研究员Agent已就绪
✓ 规划师Agent已就绪  
✓ 执行者Agent已就绪
✓ 审查员Agent已就绪

开始执行文档创建工作流...

[研究员] 正在研究主题: Python异步编程...
[研究员] ✓ 研究完成，发现了5个关键点

[规划师] 正在制定文档大纲...
[规划师] ✓ 大纲制定完成，包含6个章节

[执行者] 正在撰写文档内容...
[执行者] ✓ 文档撰写完成，共2500字

[审查员] 正在进行质量审查...
[审查员] ✓ 审查完成，质量评分: 88/100

=== 工作流执行完成 ===
执行时间: 45.2秒
任务成功率: 100%
```

### 2. 查看生成的结果

程序会显示每个Agent的详细输出，包括：
- 研究结果和关键发现
- 文档结构和大纲
- 完整的文档内容
- 质量评估和改进建议

### 3. 查看执行统计

在输出的最后，您会看到详细的执行统计：

```
=== 执行统计 ===
总执行时间: 45.2秒
任务完成数: 4
平均任务时间: 11.3秒
最慢任务: 执行者 (18.5秒)
Agent性能:
  - 研究员: 3次调用, 平均8.2秒
  - 规划师: 2次调用, 平均7.1秒  
  - 执行者: 3次调用, 平均12.8秒
  - 审查员: 2次调用, 平均6.5秒
```

## 理解示例代码

### 1. 工作流结构

简单示例使用了预定义的"文档创建"工作流：

```
研究主题 → 制定大纲 → 撰写内容 → 质量审查
    ↓         ↓          ↓         ↓
 研究员     规划师      执行者     审查员
```

### 2. 关键代码解析

让我们看看 `simple_demo.py` 的关键部分：

```python
# 1. 创建工作流管理器
workflow_manager = MultiAgentWorkflow()

# 2. 执行预定义模板
result = await workflow_manager.execute_template_workflow(
    "document_creation",  # 模板名称
    {
        "topic": "Python异步编程",
        "target_audience": "中级开发者",
        "document_type": "技术指南"
    }
)
```

### 3. Agent交互过程

每个Agent处理任务时：
1. 接收前一个Agent的输出作为输入
2. 调用LLM进行处理
3. 将结果传递给下一个Agent
4. 记录执行统计信息

## 自定义工作流

### 1. 创建简单的自定义工作流

创建一个新文件 `my_first_workflow.py`：

```python
import asyncio
from workflows.multi_agent_workflow import MultiAgentWorkflow

async def my_workflow():
    workflow_manager = MultiAgentWorkflow()
    
    # 自定义工作流数据
    workflow_data = {
        "name": "我的第一个工作流",
        "description": "学习如何创建自定义工作流",
        "tasks": [
            {
                "task_id": "research",
                "task_type": "research_topic",
                "agent_id": "researcher_001",
                "data": {
                    "topic": "人工智能在教育中的应用",
                    "scope": "focused",
                    "depth": "intermediate"
                },
                "dependencies": [],
                "priority": 1
            },
            {
                "task_id": "planning",
                "task_type": "create_project_plan",
                "agent_id": "planner_001", 
                "data": {
                    "project_name": "AI教育项目",
                    "objectives": ["提高学习效率", "个性化学习"],
                    "constraints": {
                        "timeline": "3个月",
                        "budget": "中等",
                        "resources": "小团队"
                    }
                },
                "dependencies": ["research"],  # 依赖研究任务
                "priority": 1
            }
        ]
    }
    
    # 执行自定义工作流
    result = await workflow_manager.create_custom_workflow(workflow_data)
    
    print("=== 自定义工作流执行完成 ===")
    print(f"工作流ID: {result.workflow_id}")
    print(f"状态: {result.status}")
    
    # 显示任务结果
    for task in result.tasks:
        if task.result:
            print(f"\n[{task.task_id}] 执行结果:")
            print(f"状态: {task.result.status}")
            print(f"执行时间: {task.result.execution_time:.1f}秒")

if __name__ == "__main__":
    asyncio.run(my_workflow())
```

运行自定义工作流：

```bash
python my_first_workflow.py
```

### 2. 理解任务依赖

在上面的例子中，`planning` 任务依赖于 `research` 任务：

```python
"dependencies": ["research"]  # 必须等research完成后才能开始
```

系统会自动处理依赖关系，确保任务按正确顺序执行。

### 3. 添加并行任务

修改工作流以包含并行任务：

```python
"tasks": [
    {
        "task_id": "research_tech",
        "task_type": "research_topic",
        "agent_id": "researcher_001",
        "data": {"topic": "AI技术趋势"},
        "dependencies": [],
        "priority": 1
    },
    {
        "task_id": "research_market", 
        "task_type": "research_topic",
        "agent_id": "researcher_001",
        "data": {"topic": "教育市场分析"},
        "dependencies": [],  # 与tech研究并行
        "priority": 1
    },
    {
        "task_id": "综合分析",
        "task_type": "analyze_data",
        "agent_id": "researcher_001",
        "data": {"analysis_type": "综合"},
        "dependencies": ["research_tech", "research_market"],  # 依赖两个并行任务
        "priority": 2
    }
]
```

## 常见问题

### Q1: 程序运行时出现连接错误

**错误信息**: `ConnectionError: Failed to connect to LLM service`

**解决方案**:
1. 确认LLM服务正在运行：
   ```bash
   # 测试连接
   curl http://10.6.12.215:6091/v1/models
   ```
2. 检查网络连接和防火墙设置
3. 确认配置文件中的URL正确

### Q2: Python包导入错误

**错误信息**: `ModuleNotFoundError: No module named 'langchain'`

**解决方案**:
1. 确认虚拟环境已激活
2. 重新安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 检查Python路径：
   ```bash
   python -c "import sys; print(sys.path)"
   ```

### Q3: Agent响应时间过长

**现象**: Agent执行任务时间超过30秒

**解决方案**:
1. 检查LLM服务负载
2. 调整超时设置：
   ```python
   task.timeout = 60  # 增加到60秒
   ```
3. 简化任务复杂度
4. 检查网络延迟

### Q4: 工作流执行失败

**错误信息**: `RuntimeError: Workflow execution failed`

**解决方案**:
1. 检查任务依赖是否正确
2. 验证输入数据格式：
   ```python
   from workflows.multi_agent_workflow import validate_workflow_data
   is_valid = validate_workflow_data(workflow_data)
   ```
3. 查看详细错误日志
4. 逐个测试Agent功能

### Q5: 内存使用过高

**现象**: 程序运行时内存占用持续增长

**解决方案**:
1. 启用消息历史清理：
   ```python
   # 在workflow_manager初始化后
   workflow_manager.enable_memory_cleanup(max_messages=50)
   ```
2. 定期重启长时间运行的程序
3. 监控内存使用：
   ```python
   import psutil
   print(f"内存使用: {psutil.virtual_memory().percent}%")
   ```

### Q6: 如何调试Agent行为

**调试技巧**:

1. **启用详细日志**：
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **查看Agent消息历史**：
   ```python
   for agent in workflow_manager.coordinator.agents.values():
       print(f"{agent.name} 消息历史:")
       for msg in agent.message_history[-5:]:  # 最近5条
           print(f"  {msg.sender} -> {msg.receiver}: {msg.content[:100]}")
   ```

3. **单独测试Agent**：
   ```python
   from agents.researcher_agent import ResearcherAgent
   
   agent = ResearcherAgent()
   result = await agent.process_task({
       "type": "research_topic",
       "data": {"topic": "测试主题"}
   })
   print(result)
   ```

### Q7: 如何提高执行效率

**优化建议**:

1. **调整并发数**：
   ```python
   # 在coordinator中设置
   coordinator.max_concurrent_tasks = 5  # 根据系统性能调整
   ```

2. **优化LLM参数**：
   ```python
   # 减少max_tokens以提高速度
   agent_params = {
       "temperature": 0.3,
       "max_tokens": 1000,  # 从2000减少到1000
   }
   ```

3. **使用缓存**：
   ```python
   # 启用响应缓存
   llm_config.enable_cache = True
   llm_config.cache_size = 100
   ```

## 下一步

恭喜！您已经成功运行了第一个多Agent工作流。接下来您可以：

1. **尝试其他示例**：
   ```bash
   python complex_demo.py      # 复杂演示
   python interactive_demo.py  # 交互式演示
   ```

2. **阅读详细文档**：
   - [详细教程](docs/tutorial.md) - 深入理解系统架构
   - [API参考](docs/api_reference.md) - 完整的API文档

3. **创建自己的Agent**：
   - 参考 `agents/` 目录中的示例
   - 实现自己的业务逻辑

4. **扩展工作流模板**：
   - 添加新的工作流模板
   - 集成到现有系统中

5. **加入社区**：
   - 分享您的使用经验
   - 贡献代码和想法

## 获取帮助

如果您遇到其他问题：

1. **查看日志文件**：检查 `multi_agent_YYYYMMDD.log` 文件
2. **运行诊断脚本**：
   ```bash
   python -c "from config.llm_config import LLMConfig; print('连接测试:', LLMConfig().test_connection())"
   ```
3. **查看系统状态**：
   ```bash
   python -c "from workflows.multi_agent_workflow import MultiAgentWorkflow; maw = MultiAgentWorkflow(); print('系统状态:', maw.get_system_status())"
   ```

祝您使用愉快！🚀


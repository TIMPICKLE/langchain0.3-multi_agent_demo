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
LLM_BASE_URL = "http://127.0.0.1:6000/v1"
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

## 联系方式

如有问题，请提交Issue或联系项目维护者。

# API 参考文档

## 目录

1. [核心类](#核心类)
2. [Agent接口](#agent接口)
3. [工作流管理](#工作流管理)
4. [配置管理](#配置管理)
5. [数据模型](#数据模型)
6. [工具函数](#工具函数)

## 核心类

### BaseAgent

所有Agent的基础类，提供通用功能。

```python
class BaseAgent(ABC):
    def __init__(self, agent_id: str, name: str, description: str)
```

#### 参数
- `agent_id` (str): Agent的唯一标识符
- `name` (str): Agent的显示名称
- `description` (str): Agent的功能描述

#### 属性
- `agent_id`: Agent唯一标识
- `name`: Agent名称
- `description`: Agent描述
- `message_history`: 消息历史记录
- `task_history`: 任务执行历史
- `stats`: 性能统计信息

#### 方法

##### `get_system_prompt() -> str`
获取Agent的系统提示词。

**返回值**: 系统提示词字符串

**注意**: 这是一个抽象方法，子类必须实现。

##### `process_task(task: Dict[str, Any]) -> TaskResult`
处理指定的任务。

**参数**:
- `task`: 包含任务信息的字典

**返回值**: TaskResult对象

**注意**: 这是一个抽象方法，子类必须实现。

##### `call_llm(messages: List[Dict[str, str]], **kwargs) -> str`
调用LLM服务。

**参数**:
- `messages`: 消息列表，格式为[{"role": "user", "content": "..."}]
- `**kwargs`: 额外的LLM参数

**返回值**: LLM的响应文本

**异常**:
- `ConnectionError`: 连接LLM服务失败
- `TimeoutError`: 请求超时
- `ValueError`: 参数无效

##### `get_conversation_context(max_messages: int = 5) -> List[Dict[str, str]]`
获取会话上下文。

**参数**:
- `max_messages`: 最大消息数量，默认5

**返回值**: 格式化的消息列表

##### `update_stats(execution_time: float, status: str)`
更新性能统计。

**参数**:
- `execution_time`: 执行时间（秒）
- `status`: 执行状态（"success"/"failed"）

## Agent接口

### ResearcherAgent

专门用于信息研究和分析的Agent。

```python
class ResearcherAgent(BaseAgent):
    def __init__(self, agent_id: str = "researcher_001")
```

#### 支持的任务类型

##### `research_topic`
进行主题研究。

**输入数据格式**:
```python
{
    "topic": "研究主题",
    "scope": "broad|focused|comprehensive",  # 可选
    "depth": "basic|intermediate|advanced", # 可选
    "focus_areas": ["领域1", "领域2"]        # 可选
}
```

**输出格式**:
```python
{
    "summary": "研究摘要",
    "key_findings": ["发现1", "发现2"],
    "sources": ["来源1", "来源2"],
    "recommendations": ["建议1", "建议2"]
}
```

##### `analyze_data`
分析提供的数据。

**输入数据格式**:
```python
{
    "data": "待分析的数据",
    "analysis_type": "descriptive|diagnostic|predictive",
    "focus": "重点分析领域"
}
```

##### `literature_review`
进行文献综述。

**输入数据格式**:
```python
{
    "domain": "研究领域",
    "time_range": "时间范围",
    "key_concepts": ["概念1", "概念2"]
}
```

##### `fact_check`
进行事实核查。

**输入数据格式**:
```python
{
    "claims": ["声明1", "声明2"],
    "sources": ["来源1", "来源2"]  # 可选
}
```

### PlannerAgent

专门用于制定计划和策略的Agent。

```python
class PlannerAgent(BaseAgent):
    def __init__(self, agent_id: str = "planner_001")
```

#### 支持的任务类型

##### `create_project_plan`
创建项目计划。

**输入数据格式**:
```python
{
    "project_name": "项目名称",
    "objectives": ["目标1", "目标2"],
    "constraints": {
        "timeline": "时间限制",
        "budget": "预算限制",
        "resources": "资源限制"
    },
    "requirements": ["需求1", "需求2"]
}
```

**输出格式**:
```python
{
    "project_overview": "项目概述",
    "phases": [
        {
            "name": "阶段名称",
            "duration": "持续时间",
            "tasks": ["任务1", "任务2"],
            "deliverables": ["交付物1", "交付物2"]
        }
    ],
    "milestones": ["里程碑1", "里程碑2"],
    "resource_allocation": {"角色": "资源分配"}
}
```

##### `break_down_task`
分解复杂任务。

**输入数据格式**:
```python
{
    "main_task": "主要任务描述",
    "complexity_level": "simple|moderate|complex",
    "constraints": ["约束条件"],
    "success_criteria": ["成功标准"]
}
```

##### `resource_planning`
进行资源规划。

**输入数据格式**:
```python
{
    "project_scope": "项目范围",
    "required_skills": ["技能1", "技能2"],
    "timeline": "时间线",
    "budget_range": "预算范围"
}
```

##### `risk_assessment`
进行风险评估。

**输入数据格式**:
```python
{
    "project_context": "项目背景",
    "risk_categories": ["技术风险", "时间风险", "资源风险"],
    "mitigation_strategies": true  # 是否需要缓解策略
}
```

### ExecutorAgent

专门用于执行任务和解决问题的Agent。

```python
class ExecutorAgent(BaseAgent):
    def __init__(self, agent_id: str = "executor_001")
```

#### 支持的任务类型

##### `execute_plan`
执行制定的计划。

**输入数据格式**:
```python
{
    "plan": "执行计划详情",
    "current_phase": "当前阶段",  # 可选
    "resources_available": ["可用资源"],
    "constraints": ["执行约束"]
}
```

##### `solve_problem`
解决特定问题。

**输入数据格式**:
```python
{
    "problem_description": "问题描述",
    "context": "问题背景",
    "constraints": ["解决约束"],
    "preferred_approach": "preferred_method"  # 可选
}
```

##### `monitor_progress`
监控进度。

**输入数据格式**:
```python
{
    "project_status": "项目当前状态",
    "milestones": ["里程碑列表"],
    "completion_criteria": ["完成标准"]
}
```

##### `quality_check`
进行质量检查。

**输入数据格式**:
```python
{
    "deliverable": "交付物内容",
    "quality_standards": ["质量标准"],
    "check_type": "functional|performance|compliance"
}
```

### ReviewerAgent

专门用于审查和评估的Agent。

```python
class ReviewerAgent(BaseAgent):
    def __init__(self, agent_id: str = "reviewer_001")
```

#### 支持的任务类型

##### `quality_review`
进行质量审查。

**输入数据格式**:
```python
{
    "content": "待审查内容",
    "review_criteria": ["审查标准"],
    "content_type": "document|code|plan|analysis"
}
```

**输出格式**:
```python
{
    "overall_score": 85,  # 0-100分
    "detailed_feedback": {
        "strengths": ["优点1", "优点2"],
        "weaknesses": ["不足1", "不足2"],
        "suggestions": ["建议1", "建议2"]
    },
    "compliance_status": "compliant|non_compliant|partial",
    "recommendation": "approve|revise|reject"
}
```

##### `content_review`
进行内容审查。

**输入数据格式**:
```python
{
    "content": "内容文本",
    "target_audience": "目标受众",
    "review_aspects": ["准确性", "清晰度", "完整性"],
    "style_guide": "风格指南"  # 可选
}
```

##### `compliance_check`
进行合规检查。

**输入数据格式**:
```python
{
    "content": "待检查内容",
    "compliance_rules": ["规则1", "规则2"],
    "severity_level": "strict|moderate|lenient"
}
```

##### `final_assessment`
进行最终评估。

**输入数据格式**:
```python
{
    "project_deliverables": ["交付物1", "交付物2"],
    "success_criteria": ["成功标准"],
    "stakeholder_requirements": ["利益相关者需求"]
}
```

## 工作流管理

### TaskCoordinator

多Agent任务协调器。

```python
class TaskCoordinator:
    def __init__(self)
```

#### 方法

##### `register_agent(agent: BaseAgent)`
注册Agent到协调器。

**参数**:
- `agent`: 要注册的Agent实例

##### `create_workflow(workflow_id: str, name: str, description: str) -> Workflow`
创建新的工作流。

**参数**:
- `workflow_id`: 工作流唯一标识
- `name`: 工作流名称
- `description`: 工作流描述

**返回值**: Workflow对象

##### `add_task_to_workflow(workflow_id: str, task: WorkflowTask)`
向工作流添加任务。

**参数**:
- `workflow_id`: 工作流ID
- `task`: 要添加的任务

**异常**:
- `ValueError`: 工作流不存在

##### `execute_workflow(workflow_id: str) -> Workflow`
执行工作流。

**参数**:
- `workflow_id`: 要执行的工作流ID

**返回值**: 包含执行结果的Workflow对象

**异常**:
- `ValueError`: 工作流不存在
- `RuntimeError`: 执行过程中出现错误

##### `get_workflow_status(workflow_id: str) -> Dict[str, Any]`
获取工作流状态。

**参数**:
- `workflow_id`: 工作流ID

**返回值**: 包含状态信息的字典

##### `send_message(sender: str, receiver: str, content: str, message_type: str = "text")`
发送Agent间消息。

**参数**:
- `sender`: 发送者Agent ID
- `receiver`: 接收者Agent ID
- `content`: 消息内容
- `message_type`: 消息类型

### MultiAgentWorkflow

高级工作流管理器。

```python
class MultiAgentWorkflow:
    def __init__(self)
```

#### 方法

##### `execute_template_workflow(template_name: str, input_data: Dict[str, Any]) -> Workflow`
执行预定义的模板工作流。

**参数**:
- `template_name`: 模板名称
- `input_data`: 输入数据

**返回值**: 执行完成的Workflow对象

**支持的模板**:
- `document_creation`: 文档创建工作流
- `project_planning`: 项目规划工作流
- `problem_solving`: 问题解决工作流
- `quality_improvement`: 质量改进工作流
- `research_analysis`: 研究分析工作流

##### `create_custom_workflow(workflow_data: Dict[str, Any]) -> Workflow`
创建自定义工作流。

**参数**:
- `workflow_data`: 工作流定义数据

**工作流数据格式**:
```python
{
    "name": "工作流名称",
    "description": "工作流描述",
    "tasks": [
        {
            "task_id": "task_1",
            "task_type": "research_topic",
            "agent_id": "researcher_001",
            "data": {"topic": "AI技术"},
            "dependencies": [],
            "priority": 1
        }
    ]
}
```

##### `get_available_templates() -> List[str]`
获取可用的工作流模板列表。

**返回值**: 模板名称列表

## 配置管理

### LLMConfig

LLM服务配置类。

```python
class LLMConfig:
    def __init__(self)
```

#### 属性
- `base_url`: LLM服务基础URL
- `model_name`: 模型名称
- `api_key`: API密钥（如果需要）
- `timeout`: 请求超时时间
- `max_retries`: 最大重试次数

#### 方法

##### `call_llm(messages: List[Dict[str, str]], **kwargs) -> str`
调用LLM服务。

**参数**:
- `messages`: 消息列表
- `**kwargs`: 额外参数（temperature, max_tokens等）

**返回值**: LLM响应文本

##### `test_connection() -> bool`
测试LLM服务连接。

**返回值**: 连接是否成功

##### `get_params_for_agent(agent_type: str) -> Dict[str, Any]`
获取特定Agent类型的参数。

**参数**:
- `agent_type`: Agent类型（"researcher", "planner", "executor", "reviewer"）

**返回值**: 参数字典

## 数据模型

### Message

Agent间消息的数据模型。

```python
@dataclass
class Message:
    sender: str
    receiver: str
    content: str
    message_type: str = "text"
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
```

#### 字段说明
- `sender`: 发送者Agent ID
- `receiver`: 接收者Agent ID
- `content`: 消息内容
- `message_type`: 消息类型（"text", "data", "result"等）
- `timestamp`: 消息时间戳
- `metadata`: 额外的元数据

### TaskResult

任务执行结果的数据模型。

```python
@dataclass
class TaskResult:
    agent_id: str
    task_id: str
    status: str
    result: Dict[str, Any]
    execution_time: float = 0.0
    error_message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
```

#### 字段说明
- `agent_id`: 执行任务的Agent ID
- `task_id`: 任务唯一标识
- `status`: 执行状态（"success", "failed", "pending", "running"）
- `result`: 任务执行结果
- `execution_time`: 执行时间（秒）
- `error_message`: 错误信息（如果失败）
- `metadata`: 额外的元数据

### WorkflowTask

工作流任务的数据模型。

```python
@dataclass
class WorkflowTask:
    task_id: str
    task_type: str
    agent_id: str
    data: Dict[str, Any]
    dependencies: List[str] = field(default_factory=list)
    priority: int = 1
    timeout: int = 300
    retry_count: int = 0
    max_retries: int = 3
    status: str = "pending"
    result: Optional[TaskResult] = None
```

#### 字段说明
- `task_id`: 任务唯一标识
- `task_type`: 任务类型
- `agent_id`: 负责执行的Agent ID
- `data`: 任务输入数据
- `dependencies`: 依赖的任务ID列表
- `priority`: 任务优先级（1-10，数字越大优先级越高）
- `timeout`: 超时时间（秒）
- `retry_count`: 当前重试次数
- `max_retries`: 最大重试次数
- `status`: 任务状态
- `result`: 任务执行结果

### Workflow

工作流的数据模型。

```python
@dataclass
class Workflow:
    workflow_id: str
    name: str
    description: str
    tasks: List[WorkflowTask] = field(default_factory=list)
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
```

#### 字段说明
- `workflow_id`: 工作流唯一标识
- `name`: 工作流名称
- `description`: 工作流描述
- `tasks`: 任务列表
- `status`: 工作流状态（"pending", "running", "completed", "failed"）
- `created_at`: 创建时间
- `completed_at`: 完成时间
- `metadata`: 额外的元数据

## 工具函数

### 实用工具函数

#### `create_agent_by_type(agent_type: str, agent_id: str = None) -> BaseAgent`
根据类型创建Agent实例。

**参数**:
- `agent_type`: Agent类型（"researcher", "planner", "executor", "reviewer"）
- `agent_id`: Agent ID（可选，如果不提供会自动生成）

**返回值**: Agent实例

**异常**:
- `ValueError`: 不支持的Agent类型

#### `validate_workflow_data(workflow_data: Dict[str, Any]) -> bool`
验证工作流数据格式。

**参数**:
- `workflow_data`: 工作流数据

**返回值**: 验证是否通过

**异常**:
- `ValueError`: 数据格式无效

#### `calculate_workflow_metrics(workflow: Workflow) -> Dict[str, Any]`
计算工作流性能指标。

**参数**:
- `workflow`: 工作流对象

**返回值**: 包含各种指标的字典
```python
{
    "total_execution_time": 120.5,
    "task_count": 5,
    "success_rate": 0.8,
    "avg_task_time": 24.1,
    "bottleneck_tasks": ["task_3"],
    "concurrency_utilization": 0.6
}
```

#### `export_workflow_results(workflow: Workflow, format: str = "json") -> str`
导出工作流结果。

**参数**:
- `workflow`: 工作流对象
- `format`: 导出格式（"json", "yaml", "csv"）

**返回值**: 格式化的结果字符串

#### `import_workflow_from_file(file_path: str) -> Dict[str, Any]`
从文件导入工作流定义。

**参数**:
- `file_path`: 文件路径

**返回值**: 工作流定义数据

**支持的文件格式**: JSON, YAML

### 调试和监控

#### `enable_debug_logging(level: str = "INFO")`
启用调试日志。

**参数**:
- `level`: 日志级别（"DEBUG", "INFO", "WARNING", "ERROR"）

#### `get_system_stats() -> Dict[str, Any]`
获取系统统计信息。

**返回值**: 系统统计数据
```python
{
    "active_agents": 4,
    "running_workflows": 2,
    "total_tasks_executed": 150,
    "avg_response_time": 3.2,
    "memory_usage": "45.2MB",
    "uptime": "2h 30m"
}
```

#### `monitor_agent_performance(agent_id: str) -> Dict[str, Any]`
监控Agent性能。

**参数**:
- `agent_id`: Agent ID

**返回值**: 性能数据
```python
{
    "tasks_completed": 25,
    "avg_execution_time": 12.3,
    "success_rate": 0.92,
    "last_activity": "2024-01-15T10:30:00",
    "current_status": "idle"
}
```

## 错误代码参考

### 通用错误代码

- `AGENT_001`: Agent未找到
- `AGENT_002`: Agent初始化失败
- `AGENT_003`: Agent执行超时

### 工作流错误代码

- `WORKFLOW_001`: 工作流未找到
- `WORKFLOW_002`: 工作流配置无效
- `WORKFLOW_003`: 任务依赖循环
- `WORKFLOW_004`: 工作流执行失败

### LLM错误代码

- `LLM_001`: LLM服务连接失败
- `LLM_002`: LLM响应格式错误
- `LLM_003`: LLM服务超时
- `LLM_004`: LLM API配额不足

### 任务错误代码

- `TASK_001`: 任务数据格式错误
- `TASK_002`: 任务执行超时
- `TASK_003`: 任务依赖未满足
- `TASK_004`: 任务重试次数超限

## 版本兼容性

### LangChain版本支持

- **支持版本**: LangChain 0.3.x
- **最低要求**: LangChain 0.3.0
- **推荐版本**: LangChain 0.3.1+

### Python版本支持

- **支持版本**: Python 3.8+
- **推荐版本**: Python 3.9+
- **测试环境**: Python 3.8, 3.9, 3.10, 3.11

### 依赖包版本

```
langchain>=0.3.0
requests>=2.25.0
pydantic>=2.0.0
asyncio>=3.4.3
typing-extensions>=4.0.0
```

## 许可证

本项目采用MIT许可证。详见LICENSE文件。

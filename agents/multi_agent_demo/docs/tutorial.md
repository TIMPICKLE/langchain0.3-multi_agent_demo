# LangChain 0.3 多Agent协作系统 - 详细教程

## 目录

1. [系统架构概览](#1-系统架构概览)
2. [核心组件详解](#2-核心组件详解)
3. [Agent设计原理](#3-agent设计原理)
4. [工作流设计模式](#4-工作流设计模式)
5. [LLM集成机制](#5-llm集成机制)
6. [实战案例解析](#6-实战案例解析)
7. [扩展开发指南](#7-扩展开发指南)
8. [性能优化技巧](#8-性能优化技巧)
9. [故障排除指南](#9-故障排除指南)
10. [进阶应用场景](#10-进阶应用场景)

## 1. 系统架构概览

### 1.1 整体架构

LangChain 0.3 多Agent协作系统采用分层架构设计：

```
┌─────────────────────────────────────┐
│           应用层 (Examples)          │
│  simple_demo.py | complex_demo.py   │
│       interactive_demo.py           │
├─────────────────────────────────────┤
│          工作流层 (Workflows)        │
│  MultiAgentWorkflow | TaskCoordinator│
├─────────────────────────────────────┤
│           Agent层 (Agents)          │
│ Researcher | Planner | Executor     │
│              Reviewer               │
├─────────────────────────────────────┤
│          配置层 (Config)            │
│         LLM Configuration           │
├─────────────────────────────────────┤
│          基础设施层                 │
│      LangChain 0.3 | Python        │
└─────────────────────────────────────┘
```

### 1.2 核心设计原则

1. **模块化设计**：每个组件职责单一，便于维护和扩展
2. **异步优先**：全面采用异步编程，提高并发性能
3. **类型安全**：完整的类型注解，提高代码质量
4. **配置驱动**：通过配置文件管理系统参数
5. **容错设计**：完善的错误处理和恢复机制

## 2. 核心组件详解

### 2.1 BaseAgent 基础类

BaseAgent是所有Agent的基础类，提供了通用功能：

```python
class BaseAgent(ABC):
    def __init__(self, agent_id: str, name: str, description: str):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        # ... 其他初始化
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """获取系统提示词 - 子类必须实现"""
        pass
    
    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> TaskResult:
        """处理任务 - 子类必须实现"""
        pass
```

#### 关键特性：

- **LLM调用管理**：统一的LLM调用接口和错误处理
- **消息传递**：Agent间的消息通信机制
- **性能监控**：自动收集执行统计信息
- **状态管理**：Agent的工作状态追踪

### 2.2 TaskCoordinator 任务协调器

TaskCoordinator负责管理多Agent系统的任务分发和协调：

```python
class TaskCoordinator:
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.workflows: Dict[str, Workflow] = {}
        self.message_queue: List[Message] = []
        # ... 其他初始化
    
    async def execute_workflow(self, workflow_id: str) -> Workflow:
        """执行工作流的核心方法"""
        # 依赖解析
        # 任务调度
        # 并发控制
        # 结果收集
```

#### 核心功能：

1. **依赖解析**：自动处理任务间的依赖关系
2. **并发控制**：控制同时执行的任务数量
3. **消息路由**：Agent间消息的路由和传递
4. **错误恢复**：任务失败时的重试和恢复机制

### 2.3 工作流定义

工作流使用数据类定义，支持复杂的执行逻辑：

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
```

## 3. Agent设计原理

### 3.1 专业化分工

每个Agent都有明确的职责分工：

#### 研究员Agent (ResearcherAgent)
- **核心能力**：信息收集、数据分析、知识整理
- **支持任务**：主题研究、数据分析、文献综述、事实核查
- **设计特点**：注重准确性和客观性

```python
class ResearcherAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return """你是一名专业的研究员，主要职责是：
        1. 信息收集与整理
        2. 分析与评估
        3. 报告生成
        ..."""
```

#### 规划师Agent (PlannerAgent)
- **核心能力**：任务分解、计划制定、资源配置
- **支持任务**：项目计划、任务分解、资源规划、风险评估
- **设计特点**：系统性思考和逻辑规划

#### 执行者Agent (ExecutorAgent)
- **核心能力**：任务执行、问题解决、结果交付
- **支持任务**：计划执行、方案实施、进度监控、质量检查
- **设计特点**：高效执行和实时反馈

#### 审查员Agent (ReviewerAgent)
- **核心能力**：质量评估、错误检测、改进建议
- **支持任务**：质量审查、内容评估、合规检查、最终评估
- **设计特点**：严格标准和客观评价

### 3.2 Agent通信机制

Agent间通过消息传递进行通信：

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

#### 通信模式：

1. **点对点通信**：Agent间直接消息传递
2. **广播通信**：向所有Agent发送消息
3. **任务结果传递**：通过任务依赖传递执行结果
4. **状态同步**：协调器统一管理Agent状态

### 3.3 LLM参数优化

不同Agent采用不同的LLM参数配置：

```python
AGENT_SPECIFIC_PARAMS = {
    "researcher": {
        "temperature": 0.3,  # 需要准确信息
        "max_tokens": 1500,
    },
    "planner": {
        "temperature": 0.5,  # 平衡创造性和逻辑性
        "max_tokens": 2000,
    },
    "executor": {
        "temperature": 0.4,  # 精确执行
        "max_tokens": 1800,
    },
    "reviewer": {
        "temperature": 0.2,  # 严格准确
        "max_tokens": 1200,
    }
}
```

## 4. 工作流设计模式

### 4.1 串行工作流

任务按顺序依次执行，适合有明确步骤依赖的场景：

```
研究 → 规划 → 执行 → 审查
```

#### 实现示例：

```python
# 1. 研究任务
research_task = coordinator.create_task(
    task_id="research",
    task_type="research_topic",
    agent_id="researcher_001",
    data={"topic": "AI技术"}
)

# 2. 规划任务（依赖研究结果）
planning_task = coordinator.create_task(
    task_id="planning",
    task_type="create_project_plan",
    agent_id="planner_001",
    data={"project_name": "AI项目"},
    dependencies=["research"]  # 依赖研究任务
)
```

### 4.2 并行工作流

多个任务同时执行，适合独立性强的场景：

```
    ┌─ 需求分析 ─┐
    │            │
开始├─ 技术调研 ─┤─ 综合评估
    │            │
    └─ 风险评估 ─┘
```

#### 实现示例：

```python
# 三个并行任务，都不依赖其他任务
parallel_tasks = [
    coordinator.create_task("requirements", "analyze_data", "researcher_001", data1),
    coordinator.create_task("tech_research", "research_topic", "researcher_001", data2),
    coordinator.create_task("risk_assessment", "risk_assessment", "planner_001", data3)
]

# 综合评估任务依赖所有并行任务
final_task = coordinator.create_task(
    "evaluation", "final_assessment", "reviewer_001", data4,
    dependencies=["requirements", "tech_research", "risk_assessment"]
)
```

### 4.3 混合工作流

结合串行和并行模式，适合复杂的业务场景：

```
初始研究 → ┌─ 深度分析 ─┐ → 最终报告
          │            │
          └─ 竞品分析 ─┘
```

### 4.4 动态工作流

根据执行结果动态调整工作流结构：

```python
async def dynamic_workflow_example():
    # 执行初始任务
    initial_result = await execute_task(initial_task)
    
    # 根据结果决定后续任务
    if should_deep_analysis(initial_result):
        # 动态添加深度分析任务
        deep_analysis_task = create_deep_analysis_task(initial_result)
        workflow.add_task(deep_analysis_task)
    
    if should_comparative_study(initial_result):
        # 动态添加对比研究任务
        comparative_task = create_comparative_task(initial_result)
        workflow.add_task(comparative_task)
```

## 5. LLM集成机制

### 5.1 统一接口设计

系统提供统一的LLM调用接口：

```python
class LLMConfig:
    def call_llm(self, messages: List[Dict[str, str]], **kwargs) -> str:
        # 构建请求
        request_data = self.build_request_data(messages, **kwargs)
        
        # 发送请求
        response = requests.post(
            self.get_chat_url(),
            headers=self.get_headers(),
            json=request_data,
            timeout=60
        )
        
        # 处理响应
        return self.parse_response(response)
```

### 5.2 请求构建

根据Agent类型和任务要求构建请求：

```python
def build_request_data(self, messages: list, agent_type: str = None) -> Dict[str, Any]:
    # 获取Agent专用参数
    params = self.get_params_for_agent(agent_type)
    
    return {
        "model": self.model_name,
        "messages": messages,
        "temperature": params.get("temperature", 0.7),
        "max_tokens": params.get("max_tokens", 2000),
        "top_p": params.get("top_p", 0.9)
    }
```

### 5.3 上下文管理

管理Agent的会话上下文：

```python
def get_conversation_context(self, max_messages: int = 5) -> List[Dict[str, str]]:
    # 系统提示词
    context = [{"role": "system", "content": self.get_system_prompt()}]
    
    # 添加历史消息
    recent_messages = self.message_history[-max_messages:]
    for msg in recent_messages:
        if msg.receiver == self.agent_id:
            context.append({"role": "user", "content": msg.content})
        elif msg.sender == self.agent_id:
            context.append({"role": "assistant", "content": msg.content})
    
    return context
```

### 5.4 错误处理和重试

实现健壮的错误处理机制：

```python
async def call_llm_with_retry(self, messages: List[Dict[str, str]], max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            result = self.call_llm(messages)
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            
            # 指数退避
            wait_time = 2 ** attempt
            await asyncio.sleep(wait_time)
```

## 6. 实战案例解析

### 6.1 技术文档撰写案例

#### 场景描述
使用多Agent协作撰写"LangChain入门指南"技术文档。

#### 工作流设计
```
研究员收集资料 → 规划师制定大纲 → 执行者撰写内容 → 审查员质量检查
```

#### 详细实现

**第一步：信息研究**
```python
research_task = {
    "task_id": "langchain_research",
    "task_type": "research_topic",
    "agent_id": "researcher_001",
    "data": {
        "topic": "LangChain框架入门",
        "scope": "全面",
        "depth": "初学者友好",
        "focus_areas": ["基本概念", "核心组件", "使用方法", "最佳实践"]
    }
}
```

**第二步：大纲规划**
```python
planning_task = {
    "task_id": "document_planning",
    "task_type": "break_down_task", 
    "agent_id": "planner_001",
    "data": {
        "main_task": "撰写LangChain入门指南",
        "requirements": ["结构清晰", "循序渐进", "示例丰富"],
        "target_audience": "初学者"
    },
    "dependencies": ["langchain_research"]
}
```

**第三步：内容撰写**
```python
writing_task = {
    "task_id": "content_writing",
    "task_type": "execute_plan",
    "agent_id": "executor_001", 
    "data": {
        "plan": "基于研究结果和大纲撰写文档",
        "quality_requirements": ["准确性", "可读性", "实用性"]
    },
    "dependencies": ["document_planning"]
}
```

**第四步：质量审查**
```python
review_task = {
    "task_id": "quality_review",
    "task_type": "content_review",
    "agent_id": "reviewer_001",
    "data": {
        "content_type": "技术文档",
        "review_criteria": ["技术准确性", "逻辑完整性", "表达清晰度"],
        "target_audience": "技术初学者"
    },
    "dependencies": ["content_writing"]
}
```

#### 执行结果分析

1. **研究阶段**：收集了LangChain的核心概念、组件架构、使用场景等信息
2. **规划阶段**：制定了包含概述、安装、基础用法、进阶功能、最佳实践的文档结构
3. **执行阶段**：按照大纲撰写了详细的技术文档内容
4. **审查阶段**：检查并优化了文档的技术准确性和可读性

### 6.2 项目规划案例

#### 场景描述
为"智能客服系统"项目制定完整的开发计划。

#### 工作流设计
```
需求研究 → 技术调研 → 项目规划 → 风险评估 → 计划审查
```

#### 关键实现细节

**需求研究**：分析业务需求、用户场景、功能要求
**技术调研**：评估技术方案、架构设计、技术选型
**项目规划**：制定开发计划、资源分配、时间安排
**风险评估**：识别项目风险、制定应对策略
**计划审查**：验证计划可行性、优化资源配置

#### 输出成果

1. **需求分析报告**：详细的功能需求和非功能需求
2. **技术方案文档**：架构设计和技术选型建议
3. **项目计划书**：包含WBS、时间线、里程碑
4. **风险管理计划**：风险清单和应对措施
5. **最终评估报告**：项目可行性和成功概率评估

## 7. 扩展开发指南

### 7.1 创建新的Agent

#### 步骤1：继承BaseAgent
```python
class CustomAgent(BaseAgent):
    def __init__(self, agent_id: str = "custom_001"):
        super().__init__(
            agent_id=agent_id,
            name="自定义Agent",
            description="专门处理特定业务逻辑的Agent"
        )
```

#### 步骤2：实现必需方法
```python
def get_system_prompt(self) -> str:
    return """你是一个专门的自定义Agent，负责：
    1. 特定任务处理
    2. 业务逻辑执行
    3. 结果输出"""

async def process_task(self, task: Dict[str, Any]) -> TaskResult:
    task_type = task.get("type", "default")
    
    if task_type == "custom_task_type":
        return await self._handle_custom_task(task.get("data", {}))
    else:
        return await self._handle_general_task(task.get("data", {}))
```

#### 步骤3：实现具体业务逻辑
```python
async def _handle_custom_task(self, data: Dict[str, Any]) -> TaskResult:
    # 实现具体的业务逻辑
    prompt = self._build_custom_prompt(data)
    
    context = self.get_conversation_context()
    context.append({"role": "user", "content": prompt})
    
    result = self.call_llm(context)
    
    return TaskResult(
        agent_id=self.agent_id,
        task_id=data.get("task_id", "unknown"),
        status="success",
        result={"content": result, "type": "custom_output"}
    )
```

### 7.2 创建新的工作流模板

#### 步骤1：定义工作流逻辑
```python
def _create_custom_workflow_template(self, input_data: Dict[str, Any]) -> Workflow:
    workflow_id = f"custom_workflow_{int(time.time())}"
    
    workflow = self.coordinator.create_workflow(
        workflow_id=workflow_id,
        name="自定义工作流",
        description="处理特定业务场景的工作流"
    )
    
    # 定义任务序列
    tasks = self._define_custom_tasks(workflow_id, input_data)
    
    for task in tasks:
        self.coordinator.add_task_to_workflow(workflow_id, task)
    
    return workflow
```

#### 步骤2：注册到模板系统
```python
def _register_workflow_templates(self):
    self.workflow_templates = {
        # 现有模板...
        "custom_workflow": self._create_custom_workflow_template,
    }
```

### 7.3 扩展LLM支持

#### 添加新的LLM提供商
```python
class CustomLLMConfig(LLMConfig):
    def __init__(self, provider: str = "custom"):
        self.provider = provider
        if provider == "custom":
            self.base_url = "https://api.custom-llm.com/v1"
            self.model_name = "custom-model-v1"
        
    def build_request_data(self, messages: list, agent_type: str = None):
        if self.provider == "custom":
            return self._build_custom_request(messages, agent_type)
        else:
            return super().build_request_data(messages, agent_type)
```

## 8. 性能优化技巧

### 8.1 并发控制优化

#### 动态并发数调整
```python
class AdaptiveConcurrencyController:
    def __init__(self):
        self.base_concurrency = 3
        self.max_concurrency = 10
        self.current_concurrency = self.base_concurrency
        self.performance_history = []
    
    def adjust_concurrency(self, success_rate: float, avg_response_time: float):
        if success_rate > 0.95 and avg_response_time < 5.0:
            # 性能良好，可以增加并发
            self.current_concurrency = min(
                self.current_concurrency + 1, 
                self.max_concurrency
            )
        elif success_rate < 0.8 or avg_response_time > 10.0:
            # 性能下降，减少并发
            self.current_concurrency = max(
                self.current_concurrency - 1,
                1
            )
```

### 8.2 缓存机制

#### LLM响应缓存
```python
import hashlib
import json
from typing import Optional

class LLMResponseCache:
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
        self.access_order = []
    
    def _generate_key(self, messages: List[Dict], params: Dict) -> str:
        content = json.dumps({"messages": messages, "params": params}, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()
    
    def get(self, messages: List[Dict], params: Dict) -> Optional[str]:
        key = self._generate_key(messages, params)
        if key in self.cache:
            # 更新访问顺序
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None
    
    def set(self, messages: List[Dict], params: Dict, response: str):
        key = self._generate_key(messages, params)
        
        # 缓存满时删除最少使用的
        if len(self.cache) >= self.max_size:
            oldest_key = self.access_order.pop(0)
            del self.cache[oldest_key]
        
        self.cache[key] = response
        self.access_order.append(key)
```

### 8.3 任务优先级调度

#### 智能优先级调度器
```python
class SmartPriorityScheduler:
    def __init__(self):
        self.priority_weights = {
            "deadline": 0.4,    # 截止时间权重
            "importance": 0.3,  # 重要性权重
            "dependency": 0.2,  # 依赖关系权重
            "resource": 0.1     # 资源可用性权重
        }
    
    def calculate_priority_score(self, task: WorkflowTask) -> float:
        score = 0.0
        
        # 基础优先级
        score += task.priority * self.priority_weights["importance"]
        
        # 截止时间压力
        if hasattr(task, 'deadline'):
            time_pressure = self._calculate_time_pressure(task.deadline)
            score += time_pressure * self.priority_weights["deadline"]
        
        # 依赖关系影响
        dependency_impact = len(task.dependencies) * 0.1
        score += dependency_impact * self.priority_weights["dependency"]
        
        return score
```

### 8.4 内存管理

#### 消息历史清理
```python
class MessageHistoryManager:
    def __init__(self, max_messages: int = 100):
        self.max_messages = max_messages
    
    def cleanup_agent_history(self, agent: BaseAgent):
        if len(agent.message_history) > self.max_messages:
            # 保留最近的消息
            agent.message_history = agent.message_history[-self.max_messages:]
        
        # 清理任务历史中的大型结果
        for task_result in agent.task_history:
            if hasattr(task_result.result, 'content'):
                content = task_result.result.get('content', '')
                if len(content) > 10000:  # 大于10KB的内容
                    # 保留摘要
                    task_result.result['content'] = content[:500] + "...[truncated]"
```

## 9. 故障排除指南

### 9.1 常见问题诊断

#### LLM连接问题
```python
def diagnose_llm_connection():
    """诊断LLM连接问题"""
    issues = []
    
    # 检查网络连接
    try:
        response = requests.get(LLM_BASE_URL, timeout=10)
        if response.status_code != 200:
            issues.append(f"LLM服务响应异常: {response.status_code}")
    except requests.exceptions.ConnectTimeout:
        issues.append("连接超时：网络连接问题或服务不可用")
    except requests.exceptions.ConnectionError:
        issues.append("连接错误：无法连接到LLM服务")
    
    # 检查认证配置
    if not test_llm_authentication():
        issues.append("认证失败：检查API密钥或认证配置")
    
    # 检查模型可用性
    if not test_model_availability():
        issues.append("模型不可用：检查模型名称配置")
    
    return issues
```

#### 任务执行失败分析
```python
def analyze_task_failure(task_result: TaskResult):
    """分析任务执行失败原因"""
    if task_result.status != "failed":
        return "任务未失败"
    
    error_msg = task_result.error_message
    
    if "timeout" in error_msg.lower():
        return {
            "type": "timeout",
            "cause": "任务执行超时",
            "solution": "增加超时时间或优化任务复杂度"
        }
    elif "connection" in error_msg.lower():
        return {
            "type": "connection",
            "cause": "网络连接问题", 
            "solution": "检查网络连接和LLM服务状态"
        }
    elif "rate limit" in error_msg.lower():
        return {
            "type": "rate_limit",
            "cause": "API调用频率限制",
            "solution": "降低并发数或增加请求间隔"
        }
    else:
        return {
            "type": "unknown",
            "cause": "未知错误",
            "solution": "检查详细错误日志"
        }
```

### 9.2 性能问题调试

#### 性能瓶颈识别
```python
class PerformanceProfiler:
    def __init__(self):
        self.metrics = {
            "llm_call_times": [],
            "task_execution_times": [],
            "queue_wait_times": [],
            "memory_usage": []
        }
    
    def profile_workflow_execution(self, workflow_id: str):
        """分析工作流执行性能"""
        workflow = self.get_workflow(workflow_id)
        
        bottlenecks = []
        
        # 分析任务执行时间
        for task in workflow.tasks:
            if task.result and task.result.execution_time > 30:  # 超过30秒
                bottlenecks.append({
                    "type": "slow_task",
                    "task_id": task.task_id,
                    "execution_time": task.result.execution_time,
                    "recommendation": "优化任务复杂度或增加超时时间"
                })
        
        # 分析并发利用率
        concurrent_tasks = self._analyze_concurrency(workflow)
        if concurrent_tasks < 0.5:  # 并发利用率低于50%
            bottlenecks.append({
                "type": "low_concurrency",
                "utilization": concurrent_tasks,
                "recommendation": "增加任务并行度或优化依赖关系"
            })
        
        return bottlenecks
```

### 9.3 日志和监控

#### 综合日志系统
```python
import logging
from datetime import datetime

class MultiAgentLogger:
    def __init__(self):
        self.logger = logging.getLogger("multi_agent_system")
        self.setup_logging()
    
    def setup_logging(self):
        handler = logging.FileHandler(f"multi_agent_{datetime.now().strftime('%Y%m%d')}.log")
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_agent_action(self, agent_id: str, action: str, details: Dict[str, Any]):
        self.logger.info(f"Agent[{agent_id}] {action}: {json.dumps(details)}")
    
    def log_workflow_event(self, workflow_id: str, event: str, metadata: Dict[str, Any]):
        self.logger.info(f"Workflow[{workflow_id}] {event}: {json.dumps(metadata)}")
    
    def log_error(self, component: str, error: Exception, context: Dict[str, Any]):
        self.logger.error(f"Error in {component}: {str(error)}, Context: {json.dumps(context)}")
```

## 10. 进阶应用场景

### 10.1 企业级应用集成

#### 与现有系统集成
```python
class EnterpriseIntegration:
    def __init__(self):
        self.erp_connector = ERPConnector()
        self.crm_connector = CRMConnector()
        self.workflow_manager = MultiAgentWorkflow()
    
    async def process_business_request(self, request_type: str, request_data: Dict):
        """处理企业业务请求"""
        if request_type == "customer_analysis":
            # 从CRM获取客户数据
            customer_data = await self.crm_connector.get_customer_data(request_data['customer_id'])
            
            # 使用多Agent分析
            analysis_result = await self.workflow_manager.execute_template_workflow(
                "research_analysis",
                {"topic": "客户行为分析", "data": customer_data}
            )
            
            # 将结果写回CRM
            await self.crm_connector.update_customer_insights(
                request_data['customer_id'], 
                analysis_result
            )
```

### 10.2 实时协作系统

#### WebSocket集成
```python
import websockets
import json

class RealTimeCollaboration:
    def __init__(self, workflow_manager: MultiAgentWorkflow):
        self.workflow_manager = workflow_manager
        self.connected_clients = set()
    
    async def handle_client_connection(self, websocket, path):
        """处理客户端连接"""
        self.connected_clients.add(websocket)
        try:
            async for message in websocket:
                await self.process_client_message(websocket, json.loads(message))
        finally:
            self.connected_clients.remove(websocket)
    
    async def process_client_message(self, websocket, message):
        """处理客户端消息"""
        if message['type'] == 'start_workflow':
            workflow_id = await self.start_workflow(message['data'])
            await self.broadcast_workflow_started(workflow_id)
        
        elif message['type'] == 'get_workflow_status':
            status = self.get_workflow_status(message['workflow_id'])
            await websocket.send(json.dumps(status))
    
    async def broadcast_workflow_started(self, workflow_id: str):
        """广播工作流启动事件"""
        message = {
            "type": "workflow_started",
            "workflow_id": workflow_id,
            "timestamp": datetime.now().isoformat()
        }
        
        for client in self.connected_clients:
            await client.send(json.dumps(message))
```

### 10.3 多租户支持

#### 租户隔离
```python
class MultiTenantWorkflow:
    def __init__(self):
        self.tenant_workflows = {}
        self.tenant_configs = {}
    
    def create_tenant_workspace(self, tenant_id: str, config: Dict[str, Any]):
        """为租户创建独立的工作空间"""
        # 创建租户专用的Agent实例
        tenant_agents = self._create_tenant_agents(tenant_id, config)
        
        # 创建租户专用的协调器
        tenant_coordinator = TaskCoordinator()
        for agent in tenant_agents:
            tenant_coordinator.register_agent(agent)
        
        # 创建租户专用的工作流管理器
        tenant_workflow_manager = MultiAgentWorkflow()
        tenant_workflow_manager.coordinator = tenant_coordinator
        
        self.tenant_workflows[tenant_id] = tenant_workflow_manager
        self.tenant_configs[tenant_id] = config
    
    async def execute_tenant_workflow(self, tenant_id: str, template_name: str, input_data: Dict):
        """执行租户的工作流"""
        if tenant_id not in self.tenant_workflows:
            raise ValueError(f"租户 {tenant_id} 不存在")
        
        workflow_manager = self.tenant_workflows[tenant_id]
        return await workflow_manager.execute_template_workflow(template_name, input_data)
```

### 10.4 AI驱动的工作流优化

#### 智能工作流推荐
```python
class WorkflowOptimizer:
    def __init__(self):
        self.execution_history = []
        self.optimization_models = {}
    
    def analyze_workflow_performance(self, workflow_results: List[Dict]):
        """分析工作流性能"""
        performance_metrics = {
            "avg_execution_time": 0,
            "success_rate": 0,
            "bottleneck_tasks": [],
            "optimization_opportunities": []
        }
        
        # 分析执行时间
        execution_times = [r['execution_time'] for r in workflow_results]
        performance_metrics["avg_execution_time"] = sum(execution_times) / len(execution_times)
        
        # 分析成功率
        successful_workflows = sum(1 for r in workflow_results if r['status'] == 'completed')
        performance_metrics["success_rate"] = successful_workflows / len(workflow_results)
        
        # 识别瓶颈任务
        task_performance = {}
        for result in workflow_results:
            for task in result['task_results']:
                task_type = task['task_type']
                if task_type not in task_performance:
                    task_performance[task_type] = []
                task_performance[task_type].append(task['execution_time'])
        
        # 找出执行时间最长的任务类型
        for task_type, times in task_performance.items():
            avg_time = sum(times) / len(times)
            if avg_time > 30:  # 超过30秒认为是瓶颈
                performance_metrics["bottleneck_tasks"].append({
                    "task_type": task_type,
                    "avg_execution_time": avg_time
                })
        
        return performance_metrics
    
    def recommend_optimizations(self, performance_metrics: Dict) -> List[Dict]:
        """推荐优化建议"""
        recommendations = []
        
        if performance_metrics["success_rate"] < 0.9:
            recommendations.append({
                "type": "reliability",
                "description": "增加错误处理和重试机制",
                "priority": "high"
            })
        
        if performance_metrics["avg_execution_time"] > 60:
            recommendations.append({
                "type": "performance", 
                "description": "考虑增加任务并行度或优化LLM参数",
                "priority": "medium"
            })
        
        for bottleneck in performance_metrics["bottleneck_tasks"]:
            recommendations.append({
                "type": "bottleneck",
                "description": f"优化 {bottleneck['task_type']} 任务的执行效率",
                "priority": "high",
                "task_type": bottleneck['task_type']
            })
        
        return recommendations
```

## 总结

LangChain 0.3 多Agent协作系统是一个功能完整、易于扩展的多智能体框架。通过本教程，您应该已经掌握了：

1. **系统架构**：理解了分层架构和各组件的职责
2. **Agent设计**：学会了如何设计专业化的Agent
3. **工作流管理**：掌握了多种工作流模式的实现
4. **LLM集成**：了解了如何高效地集成和管理LLM调用
5. **性能优化**：学会了多种性能优化技巧
6. **故障排除**：具备了基本的问题诊断和解决能力
7. **扩展开发**：能够根据业务需求扩展系统功能

### 下一步学习建议

1. **深入实践**：通过实际项目应用所学知识
2. **源码研究**：深入研究LangChain 0.3的源码实现
3. **社区参与**：参与开源社区，贡献代码和想法
4. **持续学习**：关注AI和多Agent系统的最新发展

### 相关资源

- [LangChain官方文档](https://docs.langchain.com/)
- [多Agent系统研究论文](https://arxiv.org/search/cs?query=multi-agent+systems)
- [AI协作系统最佳实践](https://github.com/langchain-ai/langchain)

希望这个教程能够帮助您构建出色的多Agent协作系统！

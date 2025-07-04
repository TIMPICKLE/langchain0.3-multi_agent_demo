"""
任务协调器

负责管理多个Agent之间的任务分配、协调和同步。
主要功能：
1. 任务分发和调度
2. Agent之间的消息传递
3. 工作流状态管理
4. 结果收集和整合
5. 异常处理和恢复
"""
import asyncio
import json
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

from agents import BaseAgent, Message, TaskResult

class WorkflowStatus(Enum):
    """工作流状态枚举"""
    IDLE = "idle"
    RUNNING = "running" 
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class WorkflowTask:
    """工作流任务定义"""
    task_id: str
    task_type: str
    agent_id: str
    data: Dict[str, Any]
    dependencies: List[str] = field(default_factory=list)
    priority: int = 1  # 1-10, 数字越大优先级越高
    timeout: int = 300  # 超时时间（秒）
    retry_count: int = 0
    max_retries: int = 3
    status: str = "pending"  # pending, running, completed, failed
    result: Optional[TaskResult] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

@dataclass 
class Workflow:
    """工作流定义"""
    workflow_id: str
    name: str
    description: str
    tasks: List[WorkflowTask] = field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.IDLE
    progress: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

class TaskCoordinator:
    """
    任务协调器
    
    负责管理多Agent系统中的任务分发、调度和协调工作。
    提供完整的工作流管理能力，包括任务依赖处理、并发控制、
    错误恢复等功能。
    """
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.workflows: Dict[str, Workflow] = {}
        self.message_queue: List[Message] = []
        self.task_history: List[TaskResult] = []
        
        # 配置参数
        self.max_concurrent_tasks = 5
        self.default_timeout = 300
        self.message_batch_size = 10
        
        # 运行状态
        self.is_running = False
        self.current_tasks: Dict[str, asyncio.Task] = {}
        
        print("🎛️ 任务协调器初始化完成")
    
    def register_agent(self, agent: BaseAgent):
        """
        注册Agent到协调器
        
        Args:
            agent: 要注册的Agent实例
        """
        self.agents[agent.agent_id] = agent
        print(f"📝 注册Agent: {agent.name} ({agent.agent_id})")
    
    def unregister_agent(self, agent_id: str):
        """
        注销Agent
        
        Args:
            agent_id: Agent ID
        """
        if agent_id in self.agents:
            agent_name = self.agents[agent_id].name
            del self.agents[agent_id]
            print(f"📝 注销Agent: {agent_name} ({agent_id})")
    
    def create_workflow(self, workflow_id: str, name: str, 
                       description: str = "") -> Workflow:
        """
        创建新的工作流
        
        Args:
            workflow_id: 工作流ID
            name: 工作流名称
            description: 工作流描述
            
        Returns:
            创建的工作流对象
        """
        workflow = Workflow(
            workflow_id=workflow_id,
            name=name,
            description=description
        )
        self.workflows[workflow_id] = workflow
        print(f"📋 创建工作流: {name} ({workflow_id})")
        return workflow
    
    def add_task_to_workflow(self, workflow_id: str, task: WorkflowTask):
        """
        向工作流添加任务
        
        Args:
            workflow_id: 工作流ID
            task: 要添加的任务
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"工作流不存在: {workflow_id}")
        
        workflow = self.workflows[workflow_id]
        workflow.tasks.append(task)
        print(f"➕ 向工作流 {workflow.name} 添加任务: {task.task_id}")
    
    def create_task(self, task_id: str, task_type: str, agent_id: str,
                   data: Dict[str, Any], dependencies: List[str] = None,
                   priority: int = 1, timeout: int = None) -> WorkflowTask:
        """
        创建工作流任务
        
        Args:
            task_id: 任务ID
            task_type: 任务类型
            agent_id: 负责执行的Agent ID
            data: 任务数据
            dependencies: 依赖的任务ID列表
            priority: 任务优先级
            timeout: 超时时间
            
        Returns:
            创建的任务对象
        """
        if agent_id not in self.agents:
            raise ValueError(f"Agent不存在: {agent_id}")
        
        task = WorkflowTask(
            task_id=task_id,
            task_type=task_type,
            agent_id=agent_id,
            data=data,
            dependencies=dependencies or [],
            priority=priority,
            timeout=timeout or self.default_timeout
        )
        
        print(f"🎯 创建任务: {task_id} -> {agent_id}")
        return task
    
    async def execute_workflow(self, workflow_id: str) -> Workflow:
        """
        执行工作流
        
        Args:
            workflow_id: 工作流ID
            
        Returns:
            执行完成的工作流对象
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"工作流不存在: {workflow_id}")
        
        workflow = self.workflows[workflow_id]
        print(f"🚀 开始执行工作流: {workflow.name}")
        
        workflow.status = WorkflowStatus.RUNNING
        workflow.started_at = datetime.now()
        
        try:
            await self._execute_workflow_tasks(workflow)
            
            workflow.status = WorkflowStatus.COMPLETED
            workflow.completed_at = datetime.now()
            workflow.progress = 100.0
            
            print(f"✅ 工作流执行完成: {workflow.name}")
            
        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            workflow.error_message = str(e)
            workflow.completed_at = datetime.now()
            
            print(f"❌ 工作流执行失败: {workflow.name} - {str(e)}")
            raise e
        
        return workflow
    
    async def _execute_workflow_tasks(self, workflow: Workflow):
        """
        执行工作流中的所有任务
        
        Args:
            workflow: 工作流对象
        """
        completed_tasks = set()
        running_tasks = {}
        
        while len(completed_tasks) < len(workflow.tasks):
            # 查找可以执行的任务
            ready_tasks = self._get_ready_tasks(workflow, completed_tasks, running_tasks)
            
            # 控制并发数量
            available_slots = self.max_concurrent_tasks - len(running_tasks)
            tasks_to_start = ready_tasks[:available_slots]
            
            # 启动新任务
            for task in tasks_to_start:
                print(f"⚡ 启动任务: {task.task_id}")
                task.status = "running"
                task.started_at = datetime.now()
                
                # 创建异步任务
                coroutine = self._execute_single_task(task)
                async_task = asyncio.create_task(coroutine)
                running_tasks[task.task_id] = async_task
            
            # 等待至少一个任务完成
            if running_tasks:
                done, pending = await asyncio.wait(
                    running_tasks.values(),
                    return_when=asyncio.FIRST_COMPLETED
                )
                
                # 处理完成的任务
                for async_task in done:
                    task_id = None
                    for tid, atask in running_tasks.items():
                        if atask == async_task:
                            task_id = tid
                            break
                    
                    if task_id:
                        del running_tasks[task_id]
                        completed_tasks.add(task_id)
                        
                        # 更新进度
                        workflow.progress = len(completed_tasks) / len(workflow.tasks) * 100
                        print(f"📊 工作流进度: {workflow.progress:.1f}%")
            
            # 避免无限循环
            if not ready_tasks and not running_tasks:
                remaining_tasks = [t for t in workflow.tasks if t.task_id not in completed_tasks]
                if remaining_tasks:
                    unresolved_deps = []
                    for task in remaining_tasks:
                        for dep in task.dependencies:
                            if dep not in completed_tasks:
                                unresolved_deps.append(f"{task.task_id} -> {dep}")
                    
                    raise Exception(f"任务依赖无法解决: {unresolved_deps}")
                break
    
    def _get_ready_tasks(self, workflow: Workflow, completed_tasks: set, 
                        running_tasks: dict) -> List[WorkflowTask]:
        """
        获取可以执行的任务列表
        
        Args:
            workflow: 工作流对象
            completed_tasks: 已完成的任务ID集合
            running_tasks: 正在运行的任务字典
            
        Returns:
            可以执行的任务列表
        """
        ready_tasks = []
        
        for task in workflow.tasks:
            # 跳过已完成或正在运行的任务
            if (task.task_id in completed_tasks or 
                task.task_id in running_tasks or
                task.status in ["completed", "running"]):
                continue
            
            # 检查依赖是否满足
            dependencies_met = all(dep in completed_tasks for dep in task.dependencies)
            
            if dependencies_met:
                ready_tasks.append(task)
        
        # 按优先级排序
        ready_tasks.sort(key=lambda t: t.priority, reverse=True)
        return ready_tasks
    
    async def _execute_single_task(self, task: WorkflowTask) -> TaskResult:
        """
        执行单个任务
        
        Args:
            task: 要执行的任务
            
        Returns:
            任务执行结果
        """
        agent = self.agents[task.agent_id]
        
        try:
            # 准备任务数据
            task_data = {
                "id": task.task_id,
                "type": task.task_type,
                "data": task.data
            }
            
            # 执行任务（带超时控制）
            result = await asyncio.wait_for(
                agent.execute_task(task_data),
                timeout=task.timeout
            )
            
            task.result = result
            task.status = "completed"
            task.completed_at = datetime.now()
            
            # 记录到历史
            self.task_history.append(result)
            
            print(f"✅ 任务完成: {task.task_id}")
            return result
            
        except asyncio.TimeoutError:
            error_msg = f"任务超时: {task.task_id} (超时时间: {task.timeout}s)"
            result = TaskResult(
                agent_id=task.agent_id,
                task_id=task.task_id,
                status="failed",
                result=None,
                error_message=error_msg
            )
            
            task.result = result
            task.status = "failed"
            task.completed_at = datetime.now()
            
            print(f"⏰ {error_msg}")
            
            # 是否重试
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = "pending"
                print(f"🔄 任务重试: {task.task_id} (第{task.retry_count}次)")
                return await self._execute_single_task(task)
            
            raise Exception(error_msg)
            
        except Exception as e:
            error_msg = f"任务执行失败: {task.task_id} - {str(e)}"
            result = TaskResult(
                agent_id=task.agent_id,
                task_id=task.task_id,
                status="failed",
                result=None,
                error_message=error_msg
            )
            
            task.result = result
            task.status = "failed"
            task.completed_at = datetime.now()
            
            print(f"❌ {error_msg}")
            
            # 是否重试
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = "pending"
                print(f"🔄 任务重试: {task.task_id} (第{task.retry_count}次)")
                return await self._execute_single_task(task)
            
            raise e
    
    def send_message(self, sender_id: str, receiver_id: str, 
                    content: str, message_type: str = "text",
                    metadata: Dict[str, Any] = None):
        """
        发送消息给指定Agent
        
        Args:
            sender_id: 发送者ID
            receiver_id: 接收者ID
            content: 消息内容
            message_type: 消息类型
            metadata: 元数据
        """
        if receiver_id not in self.agents:
            raise ValueError(f"接收者Agent不存在: {receiver_id}")
        
        message = Message(
            sender=sender_id,
            receiver=receiver_id,
            content=content,
            message_type=message_type,
            metadata=metadata or {}
        )
        
        # 添加到消息队列
        self.message_queue.append(message)
        
        # 直接发送给接收者
        receiver_agent = self.agents[receiver_id]
        receiver_agent.add_message(message)
        
        print(f"📨 消息发送: {sender_id} -> {receiver_id}")
    
    def broadcast_message(self, sender_id: str, content: str,
                         message_type: str = "broadcast",
                         exclude_agents: List[str] = None):
        """
        广播消息给所有Agent
        
        Args:
            sender_id: 发送者ID
            content: 消息内容
            message_type: 消息类型
            exclude_agents: 排除的Agent ID列表
        """
        exclude_agents = exclude_agents or []
        
        for agent_id in self.agents:
            if agent_id != sender_id and agent_id not in exclude_agents:
                self.send_message(sender_id, agent_id, content, message_type)
        
        print(f"📢 广播消息: {sender_id} -> 所有Agent")
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """
        获取工作流状态
        
        Args:
            workflow_id: 工作流ID
            
        Returns:
            工作流状态信息
        """
        if workflow_id not in self.workflows:
            raise ValueError(f"工作流不存在: {workflow_id}")
        
        workflow = self.workflows[workflow_id]
        
        task_stats = {
            "total": len(workflow.tasks),
            "pending": len([t for t in workflow.tasks if t.status == "pending"]),
            "running": len([t for t in workflow.tasks if t.status == "running"]),
            "completed": len([t for t in workflow.tasks if t.status == "completed"]),
            "failed": len([t for t in workflow.tasks if t.status == "failed"])
        }
        
        return {
            "workflow_id": workflow.workflow_id,
            "name": workflow.name,
            "status": workflow.status.value,
            "progress": workflow.progress,
            "task_stats": task_stats,
            "created_at": workflow.created_at.isoformat(),
            "started_at": workflow.started_at.isoformat() if workflow.started_at else None,
            "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None,
            "error_message": workflow.error_message
        }
    
    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """
        获取Agent状态
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Agent状态信息
        """
        if agent_id not in self.agents:
            raise ValueError(f"Agent不存在: {agent_id}")
        
        agent = self.agents[agent_id]
        return agent.get_performance_stats()
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        获取整个系统状态
        
        Returns:
            系统状态信息
        """
        workflow_stats = {}
        for status in WorkflowStatus:
            workflow_stats[status.value] = len([
                w for w in self.workflows.values() 
                if w.status == status
            ])
        
        agent_stats = {
            "total": len(self.agents),
            "idle": len([a for a in self.agents.values() if a.status == "idle"]),
            "working": len([a for a in self.agents.values() if a.status == "working"]),
            "error": len([a for a in self.agents.values() if a.status == "error"])
        }
        
        return {
            "coordinator_status": "running" if self.is_running else "idle",
            "workflows": {
                "total": len(self.workflows),
                "stats": workflow_stats
            },
            "agents": agent_stats,
            "tasks": {
                "total_executed": len(self.task_history),
                "success_rate": (
                    len([t for t in self.task_history if t.status == "success"]) / 
                    len(self.task_history) * 100
                ) if self.task_history else 0
            },
            "messages": {
                "total": len(self.message_queue)
            }
        }
    
    def clear_history(self):
        """清除历史记录"""
        self.message_queue.clear()
        self.task_history.clear()
        print("🧹 历史记录已清除")
    
    def reset_system(self):
        """重置整个系统"""
        # 重置所有Agent
        for agent in self.agents.values():
            agent.reset()
        
        # 清除工作流
        self.workflows.clear()
        
        # 清除历史
        self.clear_history()
        
        print("🔄 系统已重置")

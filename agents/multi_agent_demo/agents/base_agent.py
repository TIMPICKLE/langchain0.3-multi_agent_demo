"""
基础Agent类

这个模块定义了所有Agent的基础类，包含了Agent的通用功能和接口。
"""
import asyncio
import json
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import requests

from config.llm_config import get_llm_config

@dataclass
class Message:
    """消息类，用于Agent之间的通信"""
    sender: str
    receiver: str
    content: str
    message_type: str = "text"
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "content": self.content,
            "message_type": self.message_type,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }

@dataclass
class TaskResult:
    """任务结果类"""
    agent_id: str
    task_id: str
    status: str  # "success", "failed", "in_progress"
    result: Any
    error_message: Optional[str] = None
    execution_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "agent_id": self.agent_id,
            "task_id": self.task_id,
            "status": self.status,
            "result": self.result,
            "error_message": self.error_message,
            "execution_time": self.execution_time,
            "timestamp": self.timestamp.isoformat()
        }

class BaseAgent(ABC):
    """
    基础Agent类
    
    所有具体的Agent都应该继承这个基础类，并实现必要的抽象方法。
    这个类提供了Agent的基本功能，包括：
    - LLM调用
    - 消息处理
    - 任务执行
    - 状态管理
    """
    
    def __init__(self, agent_id: str, name: str, description: str):
        """
        初始化Agent
        
        Args:
            agent_id: Agent的唯一标识符
            name: Agent的名称
            description: Agent的描述
        """
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.llm_config = get_llm_config()
        
        # 状态管理
        self.status = "idle"  # "idle", "working", "error"
        self.current_task = None
        self.message_history: List[Message] = []
        self.task_history: List[TaskResult] = []
        
        # 性能统计
        self.total_requests = 0
        self.total_execution_time = 0.0
        self.success_count = 0
        self.error_count = 0
        
        print(f"🤖 Agent初始化完成: {self.name} ({self.agent_id})")
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        获取系统提示词
        
        每个具体的Agent都需要实现这个方法，定义自己的角色和职责
        """
        pass
    
    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> TaskResult:
        """
        处理任务
        
        每个具体的Agent都需要实现这个方法，定义如何处理分配给它的任务
        """
        pass
    
    def call_llm(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        调用LLM获取响应
        
        Args:
            messages: 消息列表，符合OpenAI API格式
            **kwargs: 额外的LLM参数
            
        Returns:
            LLM的响应文本
        """
        start_time = time.time()
        self.total_requests += 1
        
        try:
            # 构建请求数据
            request_data = self.llm_config.build_request_data(
                messages=messages, 
                agent_type=self.get_agent_type()
            )
            
            # 应用额外参数
            request_data.update(kwargs)
            
            # 发送请求
            response = requests.post(
                self.llm_config.get_chat_url(),
                headers=self.llm_config.get_headers(),
                json=request_data,
                timeout=120  # 增加到120秒，与LLMConfig保持一致
            )
            
            execution_time = time.time() - start_time
            self.total_execution_time += execution_time
            
            if response.status_code == 200:
                response_data = response.json()
                content = response_data['choices'][0]['message']['content']
                self.success_count += 1
                
                print(f"📡 {self.name} LLM调用成功 (耗时: {execution_time:.2f}s)")
                return content
            else:
                self.error_count += 1
                error_msg = f"LLM API错误: {response.status_code} - {response.text}"
                print(f"❌ {self.name} LLM调用失败: {error_msg}")
                raise Exception(error_msg)
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.total_execution_time += execution_time
            self.error_count += 1
            print(f"❌ {self.name} LLM调用异常: {str(e)}")
            raise e
    
    def get_agent_type(self) -> str:
        """
        获取Agent类型，用于LLM参数配置
        
        默认返回类名的小写形式，子类可以重写
        """
        return self.__class__.__name__.lower().replace("agent", "")
    
    def add_message(self, message: Message):
        """添加消息到历史记录"""
        self.message_history.append(message)
        print(f"📨 {self.name} 收到消息: {message.sender} -> {message.content[:50]}...")
    
    def send_message(self, receiver: str, content: str, message_type: str = "text", 
                     metadata: Dict[str, Any] = None) -> Message:
        """
        发送消息
        
        Args:
            receiver: 接收者ID
            content: 消息内容
            message_type: 消息类型
            metadata: 元数据
            
        Returns:
            创建的消息对象
        """
        message = Message(
            sender=self.agent_id,
            receiver=receiver,
            content=content,
            message_type=message_type,
            metadata=metadata or {}
        )
        
        print(f"📤 {self.name} 发送消息给 {receiver}: {content[:50]}...")
        return message
    
    async def execute_task(self, task: Dict[str, Any]) -> TaskResult:
        """
        执行任务的主入口
        
        这个方法包含了任务执行的通用逻辑，包括状态管理、错误处理等
        """
        task_id = task.get("id", f"task_{int(time.time())}")
        start_time = time.time()
        
        print(f"🎯 {self.name} 开始执行任务: {task_id}")
        
        self.status = "working"
        self.current_task = task
        
        try:
            # 调用具体的任务处理逻辑
            result = await self.process_task(task)
            result.execution_time = time.time() - start_time
            
            self.status = "idle"
            self.current_task = None
            self.task_history.append(result)
            
            print(f"✅ {self.name} 任务完成: {task_id} (耗时: {result.execution_time:.2f}s)")
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_result = TaskResult(
                agent_id=self.agent_id,
                task_id=task_id,
                status="failed",
                result=None,
                error_message=str(e),
                execution_time=execution_time
            )
            
            self.status = "error"
            self.current_task = None
            self.task_history.append(error_result)
            
            print(f"❌ {self.name} 任务失败: {task_id} - {str(e)}")
            return error_result
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """获取性能统计信息"""
        avg_execution_time = (self.total_execution_time / self.total_requests 
                             if self.total_requests > 0 else 0)
        success_rate = (self.success_count / self.total_requests 
                       if self.total_requests > 0 else 0)
        
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "status": self.status,
            "total_requests": self.total_requests,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "success_rate": f"{success_rate * 100:.1f}%",
            "total_execution_time": f"{self.total_execution_time:.2f}s",
            "avg_execution_time": f"{avg_execution_time:.2f}s",
            "tasks_completed": len([t for t in self.task_history if t.status == "success"]),
            "tasks_failed": len([t for t in self.task_history if t.status == "failed"])
        }
    
    def get_conversation_context(self, max_messages: int = 5) -> List[Dict[str, str]]:
        """
        获取会话上下文，用于LLM调用
        
        Args:
            max_messages: 最大消息数量
            
        Returns:
            格式化的消息列表
        """
        # 系统提示词
        context = [{"role": "system", "content": self.get_system_prompt()}]
        
        # 添加最近的消息历史
        recent_messages = self.message_history[-max_messages:] if self.message_history else []
        
        for msg in recent_messages:
            if msg.receiver == self.agent_id:  # 收到的消息
                context.append({"role": "user", "content": msg.content})
            elif msg.sender == self.agent_id:  # 发送的消息
                context.append({"role": "assistant", "content": msg.content})
        
        return context
    
    def reset(self):
        """重置Agent状态"""
        self.status = "idle"
        self.current_task = None
        self.message_history.clear()
        self.task_history.clear()
        
        # 保留性能统计
        print(f"🔄 {self.name} 状态已重置")
    
    def __str__(self) -> str:
        return f"Agent({self.name}, {self.agent_id}, {self.status})"
    
    def __repr__(self) -> str:
        return self.__str__()

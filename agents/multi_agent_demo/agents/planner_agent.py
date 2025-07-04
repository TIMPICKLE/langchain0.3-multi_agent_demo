"""
规划师Agent

专门负责制定计划、策略分析和资源调配的智能代理。
规划师Agent的主要职责：
1. 任务分解和优先级排序
2. 制定详细的执行计划
3. 资源需求分析和分配
4. 风险评估和应对策略
5. 时间线规划和里程碑设定
"""
import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime, timedelta

from .base_agent import BaseAgent, TaskResult

class PlannerAgent(BaseAgent):
    """
    规划师Agent
    
    这个Agent专门负责规划和策略制定工作。它具有以下特点：
    - 系统性的任务分解能力
    - 科学的优先级排序
    - 合理的资源分配
    - 全面的风险评估
    - 可执行的计划制定
    """
    
    def __init__(self, agent_id: str = "planner_001"):
        super().__init__(
            agent_id=agent_id,
            name="规划师小P",
            description="专业的项目规划和策略制定专家，擅长任务分解、计划制定和资源优化"
        )
        
        # 规划师专用配置
        self.planning_methods = [
            "SMART目标设定", "关键路径法", "甘特图", "风险矩阵", "资源平衡"
        ]
        self.priority_frameworks = [
            "紧急重要矩阵", "价值影响矩阵", "MoSCoW法", "Kano模型"
        ]
        self.risk_categories = [
            "技术风险", "资源风险", "时间风险", "质量风险", "外部风险"
        ]
    
    def get_system_prompt(self) -> str:
        """获取规划师的系统提示词"""
        return """你是一名专业的规划师，名叫小P。你的主要职责是：

1. 任务分解与规划：
   - 将复杂任务分解为可执行的子任务
   - 确定任务之间的依赖关系
   - 设定合理的时间估算和里程碑

2. 优先级排序：
   - 基于重要性和紧急性排序
   - 考虑资源限制和依赖关系
   - 确保关键路径的优先执行

3. 资源分配：
   - 分析所需资源类型和数量
   - 优化资源配置和利用率
   - 识别资源瓶颈和解决方案

4. 风险管理：
   - 识别潜在风险和挑战
   - 评估风险概率和影响
   - 制定风险应对和缓解策略

5. 计划制定：
   - 生成详细的执行计划
   - 设定检查点和评估标准
   - 确保计划的可行性和灵活性

工作原则：
- 目标导向，注重实际可执行性
- 系统性思考，考虑全局优化
- 平衡效率与质量
- 预见性规划，主动风险防控

输出格式要求：
- 使用结构化的计划格式
- 明确的时间线和里程碑
- 清晰的责任分工和资源需求
- 详细的风险评估和应对措施"""
    
    async def process_task(self, task: Dict[str, Any]) -> TaskResult:
        """
        处理规划任务
        
        支持的任务类型：
        - create_project_plan: 创建项目计划
        - break_down_task: 任务分解
        - resource_planning: 资源规划
        - risk_assessment: 风险评估
        - schedule_optimization: 时间表优化
        """
        task_id = task.get("id", f"plan_{int(asyncio.get_event_loop().time())}")
        task_type = task.get("type", "create_project_plan")
        task_data = task.get("data", {})
        
        try:
            if task_type == "create_project_plan":
                result = await self._create_project_plan(task_data)
            elif task_type == "break_down_task":
                result = await self._break_down_task(task_data)
            elif task_type == "resource_planning":
                result = await self._resource_planning(task_data)
            elif task_type == "risk_assessment":
                result = await self._risk_assessment(task_data)
            elif task_type == "schedule_optimization":
                result = await self._schedule_optimization(task_data)
            else:
                result = await self._general_planning(task_data)
            
            return TaskResult(
                agent_id=self.agent_id,
                task_id=task_id,
                status="success",
                result=result
            )
            
        except Exception as e:
            return TaskResult(
                agent_id=self.agent_id,
                task_id=task_id,
                status="failed",
                result=None,
                error_message=str(e)
            )
    
    async def _create_project_plan(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建项目计划
        
        Args:
            data: 包含项目信息的数据
            
        Returns:
            项目计划
        """
        project_name = data.get("project_name", "")
        objectives = data.get("objectives", [])
        constraints = data.get("constraints", {})
        timeline = data.get("timeline", "")
        resources = data.get("resources", {})
        
        print(f"📋 {self.name} 正在制定项目计划: {project_name}")
        
        planning_prompt = f"""
请为以下项目制定详细的执行计划：

项目名称：{project_name}

项目目标：
{json.dumps(objectives, ensure_ascii=False, indent=2)}

约束条件：
{json.dumps(constraints, ensure_ascii=False, indent=2)}

时间要求：{timeline}

可用资源：
{json.dumps(resources, ensure_ascii=False, indent=2)}

请提供以下内容的详细计划：

1. 项目概览
   - 项目范围和边界
   - 主要可交付成果
   - 成功标准定义

2. 任务分解结构(WBS)
   - 主要阶段划分
   - 详细任务列表
   - 任务依赖关系

3. 时间安排
   - 详细时间线
   - 关键里程碑
   - 缓冲时间设置

4. 资源配置
   - 人力资源需求
   - 技术资源配置
   - 预算分配建议

5. 风险管理
   - 主要风险识别
   - 风险评估矩阵
   - 应对策略制定

6. 质量保证
   - 质量标准定义
   - 检查点设置
   - 评估方法确定

7. 沟通计划
   - 汇报机制
   - 沟通频率
   - 利益相关者管理

请确保计划具体可行，时间安排合理。
"""
        
        context = self.get_conversation_context()
        context.append({"role": "user", "content": planning_prompt})
        
        plan_result = self.call_llm(context)
        
        result = {
            "type": "project_plan",
            "project_name": project_name,
            "objectives": objectives,
            "constraints": constraints,
            "timeline": timeline,
            "content": plan_result,
            "metadata": {
                "planning_framework": "标准项目管理",
                "complexity_level": "中等",
                "feasibility": "高",
                "created_at": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成项目计划制定: {project_name}")
        return result
    
    async def _break_down_task(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        任务分解
        """
        main_task = data.get("main_task", "")
        complexity_level = data.get("complexity", "中等")
        available_time = data.get("available_time", "")
        team_size = data.get("team_size", 1)
        
        print(f"🔄 {self.name} 正在进行任务分解")
        
        breakdown_prompt = f"""
请对以下主任务进行详细分解：

主任务：{main_task}
复杂度：{complexity_level}
可用时间：{available_time}
团队规模：{team_size}人

请提供以下分解结果：

1. 任务分析
   - 任务目标明确化
   - 核心要求识别
   - 成功标准定义

2. 分解结构
   - 主要阶段划分
   - 具体子任务列表
   - 任务粒度说明

3. 依赖关系
   - 串行任务识别
   - 并行任务机会
   - 关键路径分析

4. 工作量估算
   - 各子任务时间估计
   - 难度系数评估
   - 工作量分布

5. 分工建议
   - 角色和责任分配
   - 技能要求匹配
   - 协作方式设计

6. 检查点设置
   - 关键验收点
   - 进度监控机制
   - 质量检查标准

请确保分解合理，任务可独立执行。
"""
        
        context = self.get_conversation_context()
        context.append({"role": "user", "content": breakdown_prompt})
        
        breakdown_result = self.call_llm(context)
        
        result = {
            "type": "task_breakdown",
            "main_task": main_task,
            "complexity": complexity_level,
            "team_size": team_size,
            "content": breakdown_result,
            "metadata": {
                "breakdown_method": "WBS工作分解结构",
                "granularity": "详细",
                "executability": "高",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成任务分解")
        return result
    
    async def _resource_planning(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        资源规划
        """
        project_scope = data.get("project_scope", "")
        resource_constraints = data.get("constraints", {})
        priority_requirements = data.get("priorities", [])
        
        print(f"📊 {self.name} 正在进行资源规划")
        
        resource_prompt = f"""
请为以下项目进行资源规划：

项目范围：{project_scope}

资源约束：
{json.dumps(resource_constraints, ensure_ascii=False, indent=2)}

优先级要求：
{json.dumps(priority_requirements, ensure_ascii=False, indent=2)}

请提供详细的资源规划：

1. 资源需求分析
   - 人力资源需求
   - 技术资源需求
   - 物理资源需求
   - 财务资源需求

2. 资源获取计划
   - 内部资源调配
   - 外部资源采购
   - 资源获取时间表
   - 备选方案设计

3. 资源配置优化
   - 资源利用率最大化
   - 瓶颈资源识别
   - 负载均衡策略
   - 灵活性保障

4. 成本效益分析
   - 资源成本估算
   - 效益预期分析
   - ROI计算
   - 成本控制措施

5. 风险应对
   - 资源风险识别
   - 应急预案制定
   - 替代方案准备
   - 监控机制建立

请确保资源配置合理高效。
"""
        
        context = self.get_conversation_context()
        context.append({"role": "user", "content": resource_prompt})
        
        resource_result = self.call_llm(context)
        
        result = {
            "type": "resource_planning",
            "project_scope": project_scope,
            "constraints": resource_constraints,
            "priorities": priority_requirements,
            "content": resource_result,
            "metadata": {
                "planning_approach": "综合优化",
                "efficiency_focus": "高",
                "flexibility": "中等",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成资源规划")
        return result
    
    async def _risk_assessment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        风险评估
        """
        project_context = data.get("project_context", "")
        risk_categories = data.get("categories", self.risk_categories)
        assessment_depth = data.get("depth", "详细")
        
        print(f"⚠️ {self.name} 正在进行风险评估")
        
        risk_prompt = f"""
请对以下项目进行{assessment_depth}的风险评估：

项目背景：{project_context}

风险类别：
{json.dumps(risk_categories, ensure_ascii=False, indent=2)}

请提供全面的风险评估报告：

1. 风险识别
   - 各类别风险清单
   - 风险根本原因分析
   - 风险相互关系

2. 风险评估
   - 发生概率评估
   - 影响程度评估
   - 风险优先级排序
   - 风险矩阵图

3. 风险应对策略
   - 规避策略
   - 缓解措施
   - 转移方案
   - 接受策略

4. 监控计划
   - 风险指标定义
   - 监控频率设定
   - 预警机制建立
   - 响应流程设计

5. 应急预案
   - 关键风险应急方案
   - 资源调配预案
   - 沟通升级机制
   - 恢复计划制定

6. 风险管理建议
   - 组织建议
   - 流程改进
   - 能力建设
   - 文化培养

请确保评估全面准确，策略可操作。
"""
        
        context = self.get_conversation_context()
        context.append({"role": "user", "content": risk_prompt})
        
        risk_result = self.call_llm(context)
        
        result = {
            "type": "risk_assessment",
            "project_context": project_context,
            "categories": risk_categories,
            "depth": assessment_depth,
            "content": risk_result,
            "metadata": {
                "assessment_framework": "全面风险管理",
                "completeness": "高",
                "actionability": "强",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成风险评估")
        return result
    
    async def _schedule_optimization(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        时间表优化
        """
        current_schedule = data.get("schedule", {})
        constraints = data.get("constraints", {})
        optimization_goals = data.get("goals", ["缩短总时间", "平衡工作负载"])
        
        print(f"⏰ {self.name} 正在优化时间表")
        
        schedule_prompt = f"""
请对以下时间表进行优化：

当前时间表：
{json.dumps(current_schedule, ensure_ascii=False, indent=2)}

约束条件：
{json.dumps(constraints, ensure_ascii=False, indent=2)}

优化目标：
{json.dumps(optimization_goals, ensure_ascii=False, indent=2)}

请提供优化方案：

1. 现状分析
   - 当前时间表评估
   - 瓶颈和问题识别
   - 改进空间分析

2. 优化策略
   - 并行化机会
   - 关键路径优化
   - 资源重新分配
   - 依赖关系调整

3. 优化结果
   - 新的时间安排
   - 时间节省分析
   - 效率提升说明
   - 风险变化评估

4. 实施建议
   - 变更管理
   - 团队沟通
   - 监控调整
   - 持续优化

请确保优化方案可行有效。
"""
        
        context = self.get_conversation_context()
        context.append({"role": "user", "content": schedule_prompt})
        
        schedule_result = self.call_llm(context)
        
        result = {
            "type": "schedule_optimization",
            "current_schedule": current_schedule,
            "constraints": constraints,
            "goals": optimization_goals,
            "content": schedule_result,
            "metadata": {
                "optimization_method": "关键路径法+资源平衡",
                "improvement_potential": "高",
                "implementation_difficulty": "中等",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成时间表优化")
        return result
    
    async def _general_planning(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        通用规划任务
        """
        planning_request = data.get("request", "")
        context_info = data.get("context", {})
        
        print(f"📋 {self.name} 正在进行通用规划")
        
        general_prompt = f"""
规划请求：{planning_request}

背景信息：
{json.dumps(context_info, ensure_ascii=False, indent=2)}

请提供详细的规划方案，包括：

1. 目标分析
2. 现状评估
3. 方案设计
4. 实施计划
5. 资源需求
6. 风险控制
7. 成功标准

请确保规划科学合理，具有可操作性。
"""
        
        context = self.get_conversation_context()
        context.append({"role": "user", "content": general_prompt})
        
        planning_result = self.call_llm(context)
        
        result = {
            "type": "general_planning",
            "request": planning_request,
            "context": context_info,
            "content": planning_result,
            "metadata": {
                "approach": "系统性规划",
                "completeness": "全面",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成通用规划")
        return result
    
    def get_planning_capabilities(self) -> Dict[str, Any]:
        """获取规划能力描述"""
        return {
            "supported_tasks": [
                "create_project_plan",
                "break_down_task",
                "resource_planning",
                "risk_assessment", 
                "schedule_optimization",
                "general_planning"
            ],
            "planning_methods": self.planning_methods,
            "priority_frameworks": self.priority_frameworks,
            "risk_categories": self.risk_categories,
            "output_formats": ["项目计划", "任务分解", "资源方案", "风险报告"],
            "quality_standards": ["可行性", "完整性", "系统性", "可操作性"]
        }

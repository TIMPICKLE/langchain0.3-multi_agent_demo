"""
多Agent工作流

定义了常用的多Agent协作工作流模板和执行逻辑。
包含多种工作流模式：
1. 串行工作流 - 任务按顺序执行
2. 并行工作流 - 任务并行执行
3. 协作工作流 - Agent协作完成复杂任务
4. 评审工作流 - 包含评审和反馈环节
"""
import asyncio
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

from agents import ResearcherAgent, PlannerAgent, ExecutorAgent, ReviewerAgent
from .task_coordinator import TaskCoordinator, WorkflowTask, Workflow

class MultiAgentWorkflow:
    """
    多Agent工作流管理器
    
    提供预定义的工作流模板和自定义工作流创建功能。
    支持多种协作模式和工作流模式。
    """
    
    def __init__(self):
        self.coordinator = TaskCoordinator()
        self.workflow_templates = {}
        
        # 初始化Agent
        self._initialize_agents()
        
        # 注册工作流模板
        self._register_workflow_templates()
        
        print("🔄 多Agent工作流管理器初始化完成")
    
    def _initialize_agents(self):
        """初始化所有Agent"""
        # 创建Agent实例
        self.researcher = ResearcherAgent("researcher_001")
        self.planner = PlannerAgent("planner_001") 
        self.executor = ExecutorAgent("executor_001")
        self.reviewer = ReviewerAgent("reviewer_001")
        
        # 注册到协调器
        self.coordinator.register_agent(self.researcher)
        self.coordinator.register_agent(self.planner)
        self.coordinator.register_agent(self.executor)
        self.coordinator.register_agent(self.reviewer)
        
        print("🤖 所有Agent初始化完成")
    
    def _register_workflow_templates(self):
        """注册工作流模板"""
        self.workflow_templates = {
            "document_creation": self._create_document_creation_workflow,
            "project_planning": self._create_project_planning_workflow,
            "problem_solving": self._create_problem_solving_workflow,
            "quality_improvement": self._create_quality_improvement_workflow,
            "research_analysis": self._create_research_analysis_workflow
        }
        
        print(f"📋 注册了 {len(self.workflow_templates)} 个工作流模板")
    
    async def execute_template_workflow(self, template_name: str, input_data: Dict[str, Any]) -> Workflow:
        """
        执行模板工作流
        
        Args:
            template_name: 模板名称
            input_data: 输入数据
            
        Returns:
            执行完成的工作流
        """
        if template_name not in self.workflow_templates:
            available_templates = list(self.workflow_templates.keys())
            raise ValueError(f"工作流模板不存在: {template_name}。可用模板: {available_templates}")
        
        print(f"🚀 开始执行模板工作流: {template_name}")
        
        # 创建工作流
        workflow_creator = self.workflow_templates[template_name]
        workflow = workflow_creator(input_data)
        
        # 执行工作流
        result_workflow = await self.coordinator.execute_workflow(workflow.workflow_id)
        
        print(f"✅ 模板工作流执行完成: {template_name}")
        return result_workflow
    
    def _create_document_creation_workflow(self, input_data: Dict[str, Any]) -> Workflow:
        """
        创建文档撰写工作流
        
        流程：研究 -> 规划 -> 执行 -> 审查
        
        Args:
            input_data: 输入数据，包含topic, requirements等
            
        Returns:
            文档创建工作流
        """
        workflow_id = f"doc_creation_{int(datetime.now().timestamp())}"
        topic = input_data.get("topic", "未指定主题")
        requirements = input_data.get("requirements", [])
        
        # 创建工作流
        workflow = self.coordinator.create_workflow(
            workflow_id=workflow_id,
            name=f"文档撰写: {topic}",
            description="多Agent协作完成文档撰写任务"
        )
        
        # 1. 研究阶段
        research_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_research",
            task_type="research_topic",
            agent_id="researcher_001",
            data={
                "topic": topic,
                "scope": "全面",
                "depth": "详细"
            },
            priority=8
        )
        self.coordinator.add_task_to_workflow(workflow_id, research_task)
        
        # 2. 规划阶段
        planning_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_planning",
            task_type="create_project_plan",
            agent_id="planner_001",
            data={
                "project_name": f"文档撰写: {topic}",
                "objectives": [f"撰写关于{topic}的高质量文档"],
                "requirements": requirements,
                "timeline": "1-2天"
            },
            dependencies=[f"{workflow_id}_research"],
            priority=7
        )
        self.coordinator.add_task_to_workflow(workflow_id, planning_task)
        
        # 3. 执行阶段
        execution_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_execution",
            task_type="execute_plan",
            agent_id="executor_001",
            data={
                "plan": "基于研究结果和规划方案撰写文档",
                "priority": "高",
                "deadline": "按计划完成"
            },
            dependencies=[f"{workflow_id}_planning"],
            priority=6
        )
        self.coordinator.add_task_to_workflow(workflow_id, execution_task)
        
        # 4. 审查阶段
        review_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_review",
            task_type="quality_review",
            agent_id="reviewer_001",
            data={
                "content": "执行阶段的输出文档",
                "standards": ["准确性", "完整性", "可读性", "逻辑性"],
                "scope": "全面审查"
            },
            dependencies=[f"{workflow_id}_execution"],
            priority=5
        )
        self.coordinator.add_task_to_workflow(workflow_id, review_task)
        
        print(f"📝 创建文档撰写工作流: {topic}")
        return workflow
    
    def _create_project_planning_workflow(self, input_data: Dict[str, Any]) -> Workflow:
        """
        创建项目规划工作流
        
        流程：研究 -> 规划 -> 评估 -> 优化
        """
        workflow_id = f"project_planning_{int(datetime.now().timestamp())}"
        project_name = input_data.get("project_name", "未命名项目")
        objectives = input_data.get("objectives", [])
        constraints = input_data.get("constraints", {})
        
        workflow = self.coordinator.create_workflow(
            workflow_id=workflow_id,
            name=f"项目规划: {project_name}",
            description="多Agent协作完成项目规划"
        )
        
        # 1. 需求研究
        research_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_research",
            task_type="analyze_data",
            agent_id="researcher_001",
            data={
                "dataset": json.dumps(input_data, ensure_ascii=False),
                "analysis_type": "需求分析",
                "objectives": ["理解项目需求", "分析约束条件", "识别关键因素"]
            },
            priority=9
        )
        self.coordinator.add_task_to_workflow(workflow_id, research_task)
        
        # 2. 制定计划
        planning_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_planning",
            task_type="create_project_plan",
            agent_id="planner_001",
            data={
                "project_name": project_name,
                "objectives": objectives,
                "constraints": constraints,
                "timeline": input_data.get("timeline", "待定")
            },
            dependencies=[f"{workflow_id}_research"],
            priority=8
        )
        self.coordinator.add_task_to_workflow(workflow_id, planning_task)
        
        # 3. 风险评估
        risk_assessment_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_risk_assessment",
            task_type="risk_assessment",
            agent_id="planner_001",
            data={
                "project_context": f"项目: {project_name}",
                "categories": ["技术风险", "资源风险", "时间风险", "质量风险"],
                "depth": "详细"
            },
            dependencies=[f"{workflow_id}_planning"],
            priority=7
        )
        self.coordinator.add_task_to_workflow(workflow_id, risk_assessment_task)
        
        # 4. 计划审查
        review_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_review",
            task_type="process_review",
            agent_id="reviewer_001",
            data={
                "process": "项目计划和风险评估结果",
                "standards": ["可行性", "完整性", "合理性"],
                "efficiency": {"time": "合理", "resource": "优化"}
            },
            dependencies=[f"{workflow_id}_risk_assessment"],
            priority=6
        )
        self.coordinator.add_task_to_workflow(workflow_id, review_task)
        
        print(f"📊 创建项目规划工作流: {project_name}")
        return workflow
    
    def _create_problem_solving_workflow(self, input_data: Dict[str, Any]) -> Workflow:
        """
        创建问题解决工作流
        
        流程：分析 -> 规划 -> 实施 -> 验证
        """
        workflow_id = f"problem_solving_{int(datetime.now().timestamp())}"
        problem = input_data.get("problem", "未描述的问题")
        context = input_data.get("context", {})
        
        workflow = self.coordinator.create_workflow(
            workflow_id=workflow_id,
            name=f"问题解决: {problem[:30]}...",
            description="多Agent协作解决问题"
        )
        
        # 1. 问题分析
        analysis_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_analysis",
            task_type="fact_checking",
            agent_id="researcher_001",
            data={
                "statements": [problem],
                "sources": [context]
            },
            priority=9
        )
        self.coordinator.add_task_to_workflow(workflow_id, analysis_task)
        
        # 2. 解决方案规划
        solution_planning_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_solution_planning",
            task_type="general_planning",
            agent_id="planner_001",
            data={
                "request": f"为以下问题制定解决方案: {problem}",
                "context": context
            },
            dependencies=[f"{workflow_id}_analysis"],
            priority=8
        )
        self.coordinator.add_task_to_workflow(workflow_id, solution_planning_task)
        
        # 3. 方案实施
        implementation_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_implementation",
            task_type="implement_solution",
            agent_id="executor_001",
            data={
                "solution": "基于规划阶段的解决方案",
                "context": context,
                "criteria": ["有效性", "可行性", "持续性"]
            },
            dependencies=[f"{workflow_id}_solution_planning"],
            priority=7
        )
        self.coordinator.add_task_to_workflow(workflow_id, implementation_task)
        
        # 4. 效果验证
        validation_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_validation",
            task_type="quality_check",
            agent_id="reviewer_001",
            data={
                "deliverable": "问题解决方案及实施结果",
                "standards": ["问题解决程度", "方案可行性", "实施质量"],
                "scope": "全面检查"
            },
            dependencies=[f"{workflow_id}_implementation"],
            priority=6
        )
        self.coordinator.add_task_to_workflow(workflow_id, validation_task)
        
        print(f"🔧 创建问题解决工作流")
        return workflow
    
    def _create_quality_improvement_workflow(self, input_data: Dict[str, Any]) -> Workflow:
        """
        创建质量改进工作流
        
        流程：评估 -> 分析 -> 改进计划 -> 实施 -> 验证
        """
        workflow_id = f"quality_improvement_{int(datetime.now().timestamp())}"
        target = input_data.get("target", "未指定目标")
        current_state = input_data.get("current_state", {})
        
        workflow = self.coordinator.create_workflow(
            workflow_id=workflow_id,
            name=f"质量改进: {target}",
            description="多Agent协作进行质量改进"
        )
        
        # 1. 现状评估
        assessment_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_assessment",
            task_type="quality_review",
            agent_id="reviewer_001",
            data={
                "content": json.dumps(current_state, ensure_ascii=False),
                "standards": ["效率", "质量", "可靠性", "用户满意度"],
                "scope": "深度评估"
            },
            priority=9
        )
        self.coordinator.add_task_to_workflow(workflow_id, assessment_task)
        
        # 2. 问题根因分析
        analysis_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_analysis",
            task_type="analyze_data",
            agent_id="researcher_001",
            data={
                "dataset": "质量评估结果",
                "analysis_type": "根因分析",
                "objectives": ["识别问题根源", "分析影响因素", "找出改进机会"]
            },
            dependencies=[f"{workflow_id}_assessment"],
            priority=8
        )
        self.coordinator.add_task_to_workflow(workflow_id, analysis_task)
        
        # 3. 改进计划制定
        improvement_planning_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_improvement_planning",
            task_type="general_planning",
            agent_id="planner_001",
            data={
                "request": f"制定{target}的质量改进计划",
                "context": {"current_state": current_state, "analysis_results": "根因分析结果"}
            },
            dependencies=[f"{workflow_id}_analysis"],
            priority=7
        )
        self.coordinator.add_task_to_workflow(workflow_id, improvement_planning_task)
        
        # 4. 改进措施实施
        implementation_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_implementation",
            task_type="execute_plan",
            agent_id="executor_001",
            data={
                "plan": "质量改进计划",
                "priority": "高",
                "deadline": "按计划执行"
            },
            dependencies=[f"{workflow_id}_improvement_planning"],
            priority=6
        )
        self.coordinator.add_task_to_workflow(workflow_id, implementation_task)
        
        # 5. 改进效果验证
        validation_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_validation",
            task_type="final_assessment",
            agent_id="reviewer_001",
            data={
                "deliverables": ["改进措施", "实施结果", "效果评估"],
                "criteria": ["改进效果", "目标达成度", "可持续性"],
                "requirements": {"improvement": "显著提升", "sustainability": "长期有效"}
            },
            dependencies=[f"{workflow_id}_implementation"],
            priority=5
        )
        self.coordinator.add_task_to_workflow(workflow_id, validation_task)
        
        print(f"📈 创建质量改进工作流: {target}")
        return workflow
    
    def _create_research_analysis_workflow(self, input_data: Dict[str, Any]) -> Workflow:
        """
        创建研究分析工作流
        
        流程：数据收集 -> 深度分析 -> 报告撰写 -> 同行评议
        """
        workflow_id = f"research_analysis_{int(datetime.now().timestamp())}"
        research_topic = input_data.get("topic", "未指定研究主题")
        research_scope = input_data.get("scope", "标准")
        
        workflow = self.coordinator.create_workflow(
            workflow_id=workflow_id,
            name=f"研究分析: {research_topic}",
            description="多Agent协作进行研究分析"
        )
        
        # 1. 数据收集和初步研究
        data_collection_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_data_collection",
            task_type="research_topic",
            agent_id="researcher_001",
            data={
                "topic": research_topic,
                "scope": research_scope,
                "depth": "深入"
            },
            priority=9
        )
        self.coordinator.add_task_to_workflow(workflow_id, data_collection_task)
        
        # 2. 文献综述
        literature_review_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_literature_review",
            task_type="literature_review",
            agent_id="researcher_001",
            data={
                "topic": research_topic,
                "timeframe": "近5年",
                "focus_areas": input_data.get("focus_areas", [])
            },
            dependencies=[f"{workflow_id}_data_collection"],
            priority=8
        )
        self.coordinator.add_task_to_workflow(workflow_id, literature_review_task)
        
        # 3. 分析报告撰写计划
        report_planning_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_report_planning",
            task_type="break_down_task",
            agent_id="planner_001",
            data={
                "main_task": f"撰写{research_topic}的研究分析报告",
                "complexity": "高",
                "available_time": "3-5天",
                "team_size": 1
            },
            dependencies=[f"{workflow_id}_literature_review"],
            priority=7
        )
        self.coordinator.add_task_to_workflow(workflow_id, report_planning_task)
        
        # 4. 报告撰写
        report_writing_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_report_writing",
            task_type="general_execution",
            agent_id="executor_001",
            data={
                "description": f"基于研究结果撰写{research_topic}的分析报告",
                "requirements": [
                    "结构清晰",
                    "论证充分", 
                    "数据可靠",
                    "结论明确"
                ],
                "context": {"research_data": "前期研究结果", "literature": "文献综述"}
            },
            dependencies=[f"{workflow_id}_report_planning"],
            priority=6
        )
        self.coordinator.add_task_to_workflow(workflow_id, report_writing_task)
        
        # 5. 同行评议
        peer_review_task = self.coordinator.create_task(
            task_id=f"{workflow_id}_peer_review",
            task_type="content_review",
            agent_id="reviewer_001",
            data={
                "content": "研究分析报告",
                "type": "学术报告",
                "audience": "专业研究人员",
                "focus": ["学术严谨性", "论证逻辑", "创新性", "实用价值"]
            },
            dependencies=[f"{workflow_id}_report_writing"],
            priority=5
        )
        self.coordinator.add_task_to_workflow(workflow_id, peer_review_task)
        
        print(f"🔬 创建研究分析工作流: {research_topic}")
        return workflow
    
    async def create_custom_workflow(self, workflow_name: str, tasks: List[Dict[str, Any]]) -> Workflow:
        """
        创建自定义工作流
        
        Args:
            workflow_name: 工作流名称
            tasks: 任务定义列表
            
        Returns:
            创建的工作流
        """
        workflow_id = f"custom_{int(datetime.now().timestamp())}"
        
        workflow = self.coordinator.create_workflow(
            workflow_id=workflow_id,
            name=workflow_name,
            description="自定义多Agent工作流"
        )
        
        for task_def in tasks:
            task = self.coordinator.create_task(
                task_id=task_def.get("id", f"{workflow_id}_{len(workflow.tasks)}"),
                task_type=task_def["type"],
                agent_id=task_def["agent_id"],
                data=task_def["data"],
                dependencies=task_def.get("dependencies", []),
                priority=task_def.get("priority", 5),
                timeout=task_def.get("timeout", 300)
            )
            self.coordinator.add_task_to_workflow(workflow_id, task)
        
        print(f"🎯 创建自定义工作流: {workflow_name}")
        return workflow
    
    def get_available_templates(self) -> List[str]:
        """获取可用的工作流模板列表"""
        return list(self.workflow_templates.keys())
    
    def get_template_description(self, template_name: str) -> Dict[str, Any]:
        """
        获取模板描述
        
        Args:
            template_name: 模板名称
            
        Returns:
            模板描述信息
        """
        descriptions = {
            "document_creation": {
                "name": "文档撰写工作流",
                "description": "多Agent协作完成文档撰写，包括研究、规划、执行、审查四个阶段",
                "agents": ["研究员", "规划师", "执行者", "审查员"],
                "stages": ["主题研究", "撰写规划", "文档执行", "质量审查"],
                "input_required": ["topic", "requirements"],
                "output": "高质量的文档内容及评审报告"
            },
            "project_planning": {
                "name": "项目规划工作流", 
                "description": "全面的项目规划流程，包括需求分析、计划制定、风险评估和审查",
                "agents": ["研究员", "规划师", "审查员"],
                "stages": ["需求研究", "计划制定", "风险评估", "计划审查"],
                "input_required": ["project_name", "objectives", "constraints"],
                "output": "完整的项目计划和风险评估报告"
            },
            "problem_solving": {
                "name": "问题解决工作流",
                "description": "系统性的问题解决流程，从分析到实施再到验证",
                "agents": ["研究员", "规划师", "执行者", "审查员"],
                "stages": ["问题分析", "方案规划", "方案实施", "效果验证"],
                "input_required": ["problem", "context"],
                "output": "问题解决方案及实施验证报告"
            },
            "quality_improvement": {
                "name": "质量改进工作流",
                "description": "全面的质量改进流程，包括评估、分析、改进和验证",
                "agents": ["审查员", "研究员", "规划师", "执行者"],
                "stages": ["现状评估", "根因分析", "改进规划", "措施实施", "效果验证"],
                "input_required": ["target", "current_state"],
                "output": "质量改进方案及效果评估报告"
            },
            "research_analysis": {
                "name": "研究分析工作流",
                "description": "学术研究和分析流程，包括数据收集、分析、报告撰写和评议",
                "agents": ["研究员", "规划师", "执行者", "审查员"],
                "stages": ["数据收集", "文献综述", "报告规划", "报告撰写", "同行评议"],
                "input_required": ["topic", "scope"],
                "output": "研究分析报告及同行评议结果"
            }
        }
        
        return descriptions.get(template_name, {"error": "模板不存在"})
    
    def get_workflow_results(self, workflow_id: str) -> Dict[str, Any]:
        """
        获取工作流执行结果
        
        Args:
            workflow_id: 工作流ID
            
        Returns:
            工作流结果汇总
        """
        if workflow_id not in self.coordinator.workflows:
            raise ValueError(f"工作流不存在: {workflow_id}")
        
        workflow = self.coordinator.workflows[workflow_id]
        
        # 收集所有任务结果
        task_results = []
        for task in workflow.tasks:
            if task.result:
                task_results.append({
                    "task_id": task.task_id,
                    "agent_id": task.agent_id,
                    "status": task.result.status,
                    "result": task.result.result,
                    "execution_time": task.result.execution_time,
                    "error_message": task.result.error_message
                })
        
        return {
            "workflow_id": workflow_id,
            "workflow_name": workflow.name,
            "status": workflow.status.value,
            "progress": workflow.progress,
            "task_results": task_results,
            "total_tasks": len(workflow.tasks),
            "successful_tasks": len([t for t in workflow.tasks if t.status == "completed"]),
            "failed_tasks": len([t for t in workflow.tasks if t.status == "failed"]),
            "execution_summary": {
                "started_at": workflow.started_at.isoformat() if workflow.started_at else None,
                "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None,
                "total_time": (
                    (workflow.completed_at - workflow.started_at).total_seconds()
                    if workflow.started_at and workflow.completed_at else None
                )
            }
        }
    
    def get_system_overview(self) -> Dict[str, Any]:
        """获取系统总览"""
        return {
            "coordinator_status": self.coordinator.get_system_status(),
            "available_agents": {
                agent_id: {
                    "name": agent.name,
                    "description": agent.description,
                    "status": agent.status,
                    "performance": agent.get_performance_stats()
                }
                for agent_id, agent in self.coordinator.agents.items()
            },
            "workflow_templates": {
                name: self.get_template_description(name)
                for name in self.workflow_templates.keys()
            }
        }

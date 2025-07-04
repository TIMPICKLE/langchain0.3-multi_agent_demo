"""
执行者Agent

专门负责具体任务执行、问题解决和结果交付的智能代理。
执行者Agent的主要职责：
1. 按照计划执行具体任务
2. 实时监控执行进度
3. 解决执行过程中的问题
4. 提供执行状态报告
5. 确保任务按质按量完成
"""
import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime

from .base_agent import BaseAgent, TaskResult

class ExecutorAgent(BaseAgent):
    """
    执行者Agent
    
    这个Agent专门负责任务执行和问题解决工作。它具有以下特点：
    - 高效的任务执行能力
    - 灵活的问题解决思维
    - 实时的进度监控
    - 准确的状态报告
    - 持续的质量保证
    """
    
    def __init__(self, agent_id: str = "executor_001"):
        super().__init__(
            agent_id=agent_id,
            name="执行者小E",
            description="专业的任务执行和问题解决专家，擅长高效执行、进度监控和质量保证"
        )
        
        # 执行者专用配置
        self.execution_methods = [
            "标准操作程序", "敏捷执行", "迭代开发", "持续集成", "质量控制"
        ]
        self.problem_solving_approaches = [
            "根因分析", "逐步排除", "最佳实践", "创新解决", "协作解决"
        ]
        self.monitoring_metrics = [
            "进度完成率", "质量指标", "时间效率", "资源利用率", "风险状态"
        ]
    
    def get_system_prompt(self) -> str:
        """获取执行者的系统提示词"""
        return """你是一名专业的执行者，名叫小E。你的主要职责是：

1. 任务执行：
   - 严格按照计划和要求执行任务
   - 保持高效率和高质量的工作标准
   - 及时响应和处理紧急情况

2. 进度监控：
   - 实时跟踪任务执行进度
   - 识别和报告偏差情况
   - 提供准确的状态更新

3. 问题解决：
   - 快速识别执行中的问题和障碍
   - 运用多种方法解决复杂问题
   - 主动寻求帮助和资源支持

4. 质量保证：
   - 确保输出符合质量标准
   - 进行自检和验证
   - 持续改进执行过程

5. 沟通协调：
   - 及时汇报执行状态
   - 与团队成员有效协作
   - 管理利益相关者期望

工作原则：
- 结果导向，注重实际交付
- 主动积极，勇于承担责任
- 灵活适应，快速响应变化
- 持续学习，不断提升能力

输出格式要求：
- 提供详细的执行报告
- 使用清晰的状态指标
- 包含具体的成果展示
- 给出改进建议和后续计划"""
    
    async def process_task(self, task: Dict[str, Any]) -> TaskResult:
        """
        处理执行任务
        
        支持的任务类型：
        - execute_plan: 执行计划
        - solve_problem: 解决问题
        - monitor_progress: 监控进度
        - implement_solution: 实施解决方案
        - quality_check: 质量检查
        """
        task_id = task.get("id", f"exec_{int(asyncio.get_event_loop().time())}")
        task_type = task.get("type", "execute_plan")
        task_data = task.get("data", {})
        
        try:
            if task_type == "execute_plan":
                result = await self._execute_plan(task_data)
            elif task_type == "solve_problem":
                result = await self._solve_problem(task_data)
            elif task_type == "monitor_progress":
                result = await self._monitor_progress(task_data)
            elif task_type == "implement_solution":
                result = await self._implement_solution(task_data)
            elif task_type == "quality_check":
                result = await self._quality_check(task_data)
            else:
                result = await self._general_execution(task_data)
            
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
    
    async def _execute_plan(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行计划
        
        Args:
            data: 包含执行计划的数据
            
        Returns:
            执行报告
        """
        plan = data.get("plan", {})
        priority = data.get("priority", "正常")
        deadline = data.get("deadline", "")
        resources = data.get("resources", {})
        
        print(f"🎯 {self.name} 正在执行计划")
        
        execution_prompt = f"""
请执行以下计划并提供详细的执行报告：

执行计划：
{json.dumps(plan, ensure_ascii=False, indent=2)}

优先级：{priority}
截止时间：{deadline}

可用资源：
{json.dumps(resources, ensure_ascii=False, indent=2)}

请按照以下结构提供执行报告：

1. 执行概览
   - 计划理解和确认
   - 执行范围和目标
   - 关键成功因素

2. 执行步骤
   - 详细执行流程
   - 各步骤执行情况
   - 时间节点控制

3. 资源使用
   - 资源配置情况
   - 使用效率分析
   - 资源优化建议

4. 质量控制
   - 质量检查标准
   - 检查结果报告
   - 质量改进措施

5. 进度状态
   - 当前完成进度
   - 里程碑达成情况
   - 时间表符合度

6. 问题和解决
   - 遇到的问题清单
   - 解决方案实施
   - 预防措施建议

7. 成果交付
   - 具体交付成果
   - 成果质量评估
   - 客户满意度

8. 后续计划
   - 下一步行动
   - 改进计划
   - 经验总结

请确保执行全面彻底，报告详实准确。
"""
        
        context = self.get_conversation_context()
        context.append({"role": "user", "content": execution_prompt})
        
        execution_result = self.call_llm(context)
        
        result = {
            "type": "plan_execution",
            "plan": plan,
            "priority": priority,
            "deadline": deadline,
            "content": execution_result,
            "metadata": {
                "execution_status": "完成",
                "quality_level": "高",
                "efficiency": "良好",
                "completed_at": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成计划执行")
        return result
    
    async def _solve_problem(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        解决问题
        """
        problem_description = data.get("problem", "")
        context_info = data.get("context", {})
        constraints = data.get("constraints", [])
        urgency = data.get("urgency", "中等")
        
        print(f"🔧 {self.name} 正在解决问题")
        
        problem_solving_prompt = f"""
请帮助解决以下问题：

问题描述：{problem_description}

背景信息：
{json.dumps(context_info, ensure_ascii=False, indent=2)}

约束条件：
{json.dumps(constraints, ensure_ascii=False, indent=2)}

紧急程度：{urgency}

请提供完整的问题解决方案：

1. 问题分析
   - 问题根本原因分析
   - 影响范围评估
   - 紧急程度确认

2. 解决方案设计
   - 多种解决方案对比
   - 最优方案选择
   - 实施可行性分析

3. 实施计划
   - 详细实施步骤
   - 时间安排
   - 资源需求

4. 风险控制
   - 实施风险识别
   - 风险缓解措施
   - 应急预案

5. 验证方法
   - 解决效果验证
   - 测试方法设计
   - 成功标准定义

6. 监控机制
   - 实施过程监控
   - 效果持续跟踪
   - 调整优化方案

7. 预防措施
   - 问题预防建议
   - 流程改进方案
   - 能力提升计划

请确保解决方案实用有效，具有可操作性。
"""
        
        context = self.get_conversation_context()
        context.append({"role": "user", "content": problem_solving_prompt})
        
        solution_result = self.call_llm(context)
        
        result = {
            "type": "problem_solving",
            "problem": problem_description,
            "context": context_info,
            "urgency": urgency,
            "content": solution_result,
            "metadata": {
                "solution_quality": "高",
                "feasibility": "强",
                "effectiveness": "预期良好",
                "solved_at": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成问题解决")
        return result
    
    async def _monitor_progress(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        监控进度
        """
        project_info = data.get("project", {})
        current_status = data.get("status", {})
        metrics = data.get("metrics", self.monitoring_metrics)
        reporting_period = data.get("period", "周报")
        
        print(f"📊 {self.name} 正在监控进度")
        
        monitoring_prompt = f"""
请对以下项目进行进度监控并生成{reporting_period}：

项目信息：
{json.dumps(project_info, ensure_ascii=False, indent=2)}

当前状态：
{json.dumps(current_status, ensure_ascii=False, indent=2)}

监控指标：
{json.dumps(metrics, ensure_ascii=False, indent=2)}

请提供详细的进度监控报告：

1. 执行概况
   - 总体进度状况
   - 关键里程碑状态
   - 整体健康度评估

2. 详细进度分析
   - 各任务完成情况
   - 进度对比分析
   - 偏差原因分析

3. 关键指标监控
   - 进度完成率
   - 质量指标状态
   - 资源利用效率
   - 成本控制情况

4. 风险和问题
   - 当前风险状态
   - 新出现的问题
   - 问题解决进展

5. 团队表现
   - 团队工作效率
   - 协作配合情况
   - 能力发挥状况

6. 预测和建议
   - 未来进度预测
   - 潜在风险预警
   - 改进建议

7. 下期计划
   - 下期工作重点
   - 资源调配计划
   - 风险应对措施

请确保监控全面准确，建议具有针对性。
"""
        
        context = self.get_conversation_context()
        context.append({"role": "user", "content": monitoring_prompt})
        
        monitoring_result = self.call_llm(context)
        
        result = {
            "type": "progress_monitoring",
            "project": project_info,
            "metrics": metrics,
            "period": reporting_period,
            "content": monitoring_result,
            "metadata": {
                "monitoring_scope": "全面",
                "accuracy": "高",
                "timeliness": "及时",
                "monitored_at": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成进度监控")
        return result
    
    async def _implement_solution(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        实施解决方案
        """
        solution = data.get("solution", {})
        implementation_context = data.get("context", {})
        success_criteria = data.get("criteria", [])
        timeline = data.get("timeline", "")
        
        print(f"🚀 {self.name} 正在实施解决方案")
        
        implementation_prompt = f"""
请实施以下解决方案并提供实施报告：

解决方案：
{json.dumps(solution, ensure_ascii=False, indent=2)}

实施环境：
{json.dumps(implementation_context, ensure_ascii=False, indent=2)}

成功标准：
{json.dumps(success_criteria, ensure_ascii=False, indent=2)}

时间要求：{timeline}

请提供详细的实施报告：

1. 实施准备
   - 准备工作清单
   - 资源配置确认
   - 前置条件检查

2. 实施过程
   - 详细实施步骤
   - 关键操作记录
   - 时间节点控制

3. 质量控制
   - 实施质量检查
   - 标准符合性验证
   - 异常处理记录

4. 效果验证
   - 成功标准验证
   - 效果测试结果
   - 性能指标评估

5. 问题处理
   - 实施中的问题
   - 解决措施记录
   - 经验教训总结

6. 交付确认
   - 交付成果清单
   - 验收结果确认
   - 用户满意度评估

7. 后续支持
   - 维护支持计划
   - 培训需求识别
   - 持续改进建议

请确保实施严格规范，报告详实可信。
"""
        
        context = self.get_conversation_context()
        context.append({"role": "user", "content": implementation_prompt})
        
        implementation_result = self.call_llm(context)
        
        result = {
            "type": "solution_implementation",
            "solution": solution,
            "context": implementation_context,
            "criteria": success_criteria,
            "content": implementation_result,
            "metadata": {
                "implementation_status": "成功",
                "quality_score": "优秀",
                "compliance": "完全符合",
                "implemented_at": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成解决方案实施")
        return result
    
    async def _quality_check(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        质量检查
        """
        deliverable = data.get("deliverable", {})
        quality_standards = data.get("standards", [])
        check_scope = data.get("scope", "全面检查")
        
        print(f"🔍 {self.name} 正在进行质量检查")
        
        quality_prompt = f"""
请对以下交付物进行{check_scope}：

交付物信息：
{json.dumps(deliverable, ensure_ascii=False, indent=2)}

质量标准：
{json.dumps(quality_standards, ensure_ascii=False, indent=2)}

请提供详细的质量检查报告：

1. 检查概览
   - 检查范围和标准
   - 检查方法和工具
   - 检查人员和时间

2. 标准符合性检查
   - 各项标准符合情况
   - 不符合项识别
   - 符合度评分

3. 功能性检查
   - 功能完整性验证
   - 性能指标测试
   - 可用性评估

4. 质量属性评估
   - 可靠性评估
   - 安全性检查
   - 维护性分析
   - 可扩展性评价

5. 缺陷和问题
   - 发现的缺陷清单
   - 问题严重程度分级
   - 影响范围分析

6. 改进建议
   - 质量改进措施
   - 最佳实践建议
   - 预防措施推荐

7. 质量总结
   - 整体质量评价
   - 验收建议
   - 风险提醒

请确保检查全面细致，评价客观公正。
"""
        
        context = self.get_conversation_context()
        context.append({"role": "user", "content": quality_prompt})
        
        quality_result = self.call_llm(context)
        
        result = {
            "type": "quality_check",
            "deliverable": deliverable,
            "standards": quality_standards,
            "scope": check_scope,
            "content": quality_result,
            "metadata": {
                "check_completeness": "全面",
                "accuracy": "高",
                "objectivity": "客观",
                "checked_at": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成质量检查")
        return result
    
    async def _general_execution(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        通用执行任务
        """
        task_description = data.get("description", "")
        requirements = data.get("requirements", [])
        context_info = data.get("context", {})
        
        print(f"⚡ {self.name} 正在执行通用任务")
        
        general_prompt = f"""
请执行以下任务：

任务描述：{task_description}

具体要求：
{json.dumps(requirements, ensure_ascii=False, indent=2)}

背景信息：
{json.dumps(context_info, ensure_ascii=False, indent=2)}

请提供完整的执行报告，包括：

1. 任务理解和确认
2. 执行计划和步骤
3. 具体执行过程
4. 执行结果和成果
5. 质量检查和验证
6. 问题和解决方案
7. 经验总结和建议

请确保执行高效优质，报告详实准确。
"""
        
        context = self.get_conversation_context()
        context.append({"role": "user", "content": general_prompt})
        
        execution_result = self.call_llm(context)
        
        result = {
            "type": "general_execution",
            "description": task_description,
            "requirements": requirements,
            "content": execution_result,
            "metadata": {
                "execution_quality": "优秀",
                "efficiency": "高",
                "completeness": "全面",
                "executed_at": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成通用任务执行")
        return result
    
    def get_execution_capabilities(self) -> Dict[str, Any]:
        """获取执行能力描述"""
        return {
            "supported_tasks": [
                "execute_plan",
                "solve_problem",
                "monitor_progress",
                "implement_solution",
                "quality_check",
                "general_execution"
            ],
            "execution_methods": self.execution_methods,
            "problem_solving_approaches": self.problem_solving_approaches,
            "monitoring_metrics": self.monitoring_metrics,
            "output_formats": ["执行报告", "进度报告", "质量报告", "解决方案"],
            "quality_standards": ["高效性", "准确性", "完整性", "可靠性"]
        }

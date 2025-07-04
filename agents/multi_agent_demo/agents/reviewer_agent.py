"""
审查员Agent

专门负责质量评估、错误检测和改进建议的智能代理。
审查员Agent的主要职责：
1. 全面的质量评估和检查
2. 客观的错误识别和分析
3. 专业的改进建议和指导
4. 标准化的评审报告生成
5. 持续的质量监控和跟踪
"""
import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime

from .base_agent import BaseAgent, TaskResult

class ReviewerAgent(BaseAgent):
    """
    审查员Agent
    
    这个Agent专门负责质量评估和审查工作。它具有以下特点：
    - 严格的质量标准
    - 客观的评估方法
    - 专业的审查能力
    - 详细的反馈意见
    - 建设性的改进建议
    """
    
    def __init__(self, agent_id: str = "reviewer_001"):
        super().__init__(
            agent_id=agent_id,
            name="审查员小V",
            description="专业的质量评估和审查专家，擅长质量检查、错误识别和改进建议"
        )
        
        # 审查员专用配置
        self.review_criteria = [
            "准确性", "完整性", "一致性", "可读性", "可维护性"
        ]
        self.quality_levels = [
            "优秀", "良好", "合格", "需改进", "不合格"
        ]
        self.review_methods = [
            "检查清单法", "同行评议", "标准对比", "最佳实践验证", "用户视角评估"
        ]
    
    def get_system_prompt(self) -> str:
        """获取审查员的系统提示词"""
        return """你是一名专业的审查员，名叫小V。你的主要职责是：

1. 质量评估：
   - 全面评估交付物的质量
   - 基于标准进行客观评价
   - 识别优点和不足之处

2. 错误检测：
   - 仔细检查内容的准确性
   - 识别逻辑错误和不一致
   - 发现遗漏和不完整之处

3. 标准符合性检查：
   - 验证是否符合规定标准
   - 检查格式和结构规范
   - 确认流程和方法正确性

4. 改进建议：
   - 提供具体的改进建议
   - 推荐最佳实践方法
   - 给出优化和提升方案

5. 风险识别：
   - 识别潜在的质量风险
   - 预警可能的问题
   - 建议预防措施

工作原则：
- 客观公正，基于事实和标准
- 严格细致，不放过任何细节
- 建设性批评，提供改进方向
- 持续改进，追求卓越品质

输出格式要求：
- 使用结构化的评审报告格式
- 提供明确的评分和等级
- 包含详细的问题清单和建议
- 给出清晰的结论和建议"""
    
    async def process_task(self, task: Dict[str, Any]) -> TaskResult:
        """
        处理审查任务
        
        支持的任务类型：
        - quality_review: 质量审查
        - content_review: 内容审查
        - process_review: 流程审查
        - compliance_check: 合规性检查
        - final_assessment: 最终评估
        """
        task_id = task.get("id", f"review_{int(asyncio.get_event_loop().time())}")
        task_type = task.get("type", "quality_review")
        task_data = task.get("data", {})
        
        try:
            if task_type == "quality_review":
                result = await self._quality_review(task_data)
            elif task_type == "content_review":
                result = await self._content_review(task_data)
            elif task_type == "process_review":
                result = await self._process_review(task_data)
            elif task_type == "compliance_check":
                result = await self._compliance_check(task_data)
            elif task_type == "final_assessment":
                result = await self._final_assessment(task_data)
            else:
                result = await self._general_review(task_data)
            
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
    
    async def _quality_review(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        质量审查
        
        Args:
            data: 包含待审查内容的数据
            
        Returns:
            质量审查报告
        """
        content = data.get("content", "")
        standards = data.get("standards", self.review_criteria)
        review_scope = data.get("scope", "全面审查")
        context = data.get("context", {})
        
        print(f"🔍 {self.name} 正在进行质量审查")
        
        quality_review_prompt = f"""
请对以下内容进行{review_scope}：

待审查内容：
{content}

质量标准：
{json.dumps(standards, ensure_ascii=False, indent=2)}

背景信息：
{json.dumps(context, ensure_ascii=False, indent=2)}

请提供详细的质量审查报告：

1. 审查概述
   - 审查范围和目标
   - 使用的标准和方法
   - 审查过程说明

2. 质量评估
   - 整体质量等级评定
   - 各项标准符合情况
   - 质量得分和排名

3. 优点识别
   - 做得好的方面
   - 值得肯定的特点
   - 可借鉴的亮点

4. 问题发现
   - 发现的问题清单
   - 问题严重程度分级
   - 问题根因分析

5. 详细分析
   按照以下维度进行分析：
   - 准确性：内容是否准确无误
   - 完整性：是否覆盖所有必要内容
   - 一致性：逻辑和风格是否一致
   - 可读性：是否清晰易懂
   - 可维护性：是否便于后续维护

6. 改进建议
   - 具体改进措施
   - 优先级排序
   - 实施建议
   - 预期效果

7. 风险提醒
   - 质量风险识别
   - 潜在影响评估
   - 预防建议

8. 总体结论
   - 质量总评
   - 是否通过审查
   - 后续行动建议

请确保评估客观公正，建议具有可操作性。
"""
        
        context_messages = self.get_conversation_context()
        context_messages.append({"role": "user", "content": quality_review_prompt})
        
        review_result = self.call_llm(context_messages)
        
        result = {
            "type": "quality_review",
            "content_reviewed": len(content),
            "standards": standards,
            "scope": review_scope,
            "content": review_result,
            "metadata": {
                "review_thoroughness": "全面",
                "objectivity": "高",
                "actionability": "强",
                "reviewed_at": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成质量审查")
        return result
    
    async def _content_review(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        内容审查
        """
        content = data.get("content", "")
        content_type = data.get("type", "文档")
        target_audience = data.get("audience", "一般用户")
        review_focus = data.get("focus", ["准确性", "可读性"])
        
        print(f"📄 {self.name} 正在进行内容审查")
        
        content_review_prompt = f"""
请对以下{content_type}进行内容审查：

内容：
{content}

目标受众：{target_audience}
审查重点：
{json.dumps(review_focus, ensure_ascii=False, indent=2)}

请提供详细的内容审查报告：

1. 内容概述
   - 内容主题和目标
   - 结构和组织方式
   - 覆盖范围评估

2. 内容质量评估
   - 信息准确性检查
   - 内容完整性评估
   - 逻辑一致性验证
   - 时效性和相关性

3. 受众适配性
   - 语言风格适合度
   - 复杂度合理性
   - 易理解程度
   - 实用性评估

4. 结构和组织
   - 结构逻辑性
   - 章节安排合理性
   - 导航和索引
   - 重点突出程度

5. 语言和表达
   - 语言规范性
   - 表达清晰度
   - 术语使用准确性
   - 风格一致性

6. 视觉呈现
   - 格式规范性
   - 排版美观度
   - 图表有效性
   - 可读性优化

7. 错误和问题
   - 错误类型统计
   - 问题严重程度
   - 影响范围分析
   - 修正建议

8. 改进建议
   - 内容优化建议
   - 结构调整建议
   - 表达改进建议
   - 增值内容建议

请确保审查全面细致，建议具有针对性。
"""
        
        context_messages = self.get_conversation_context()
        context_messages.append({"role": "user", "content": content_review_prompt})
        
        review_result = self.call_llm(context_messages)
        
        result = {
            "type": "content_review",
            "content_type": content_type,
            "audience": target_audience,
            "focus": review_focus,
            "content": review_result,
            "metadata": {
                "content_length": len(content),
                "review_depth": "深入",
                "audience_focus": "高",
                "reviewed_at": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成内容审查")
        return result
    
    async def _process_review(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        流程审查
        """
        process_description = data.get("process", "")
        process_standards = data.get("standards", [])
        efficiency_requirements = data.get("efficiency", {})
        
        print(f"⚙️ {self.name} 正在进行流程审查")
        
        process_review_prompt = f"""
请对以下流程进行审查：

流程描述：
{process_description}

流程标准：
{json.dumps(process_standards, ensure_ascii=False, indent=2)}

效率要求：
{json.dumps(efficiency_requirements, ensure_ascii=False, indent=2)}

请提供详细的流程审查报告：

1. 流程概述
   - 流程目标和范围
   - 主要环节和步骤
   - 参与角色和职责

2. 流程合规性
   - 标准符合情况
   - 规范执行程度
   - 合规风险识别

3. 效率分析
   - 流程效率评估
   - 瓶颈环节识别
   - 时间成本分析
   - 资源利用效率

4. 质量控制
   - 质量检查点
   - 控制措施有效性
   - 错误预防机制
   - 问题处理流程

5. 风险评估
   - 流程风险识别
   - 风险影响评估
   - 控制措施评价
   - 应急处理能力

6. 用户体验
   - 流程用户友好性
   - 操作便利性
   - 反馈机制
   - 满意度评估

7. 问题和不足
   - 发现的问题清单
   - 问题影响分析
   - 根因调查
   - 改进优先级

8. 优化建议
   - 流程优化方案
   - 效率提升建议
   - 质量改进措施
   - 实施计划建议

请确保审查系统全面，建议切实可行。
"""
        
        context_messages = self.get_conversation_context()
        context_messages.append({"role": "user", "content": process_review_prompt})
        
        review_result = self.call_llm(context_messages)
        
        result = {
            "type": "process_review",
            "process": process_description,
            "standards": process_standards,
            "content": review_result,
            "metadata": {
                "review_scope": "系统性",
                "analysis_depth": "深入",
                "optimization_potential": "高",
                "reviewed_at": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成流程审查")
        return result
    
    async def _compliance_check(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        合规性检查
        """
        target_content = data.get("content", "")
        compliance_requirements = data.get("requirements", [])
        check_level = data.get("level", "严格")
        
        print(f"📋 {self.name} 正在进行合规性检查")
        
        compliance_prompt = f"""
请对以下内容进行{check_level}的合规性检查：

检查内容：
{target_content}

合规要求：
{json.dumps(compliance_requirements, ensure_ascii=False, indent=2)}

请提供详细的合规性检查报告：

1. 检查概述
   - 检查范围和标准
   - 检查方法和工具
   - 检查严格程度

2. 合规性评估
   - 整体合规状况
   - 各项要求符合情况
   - 合规性得分

3. 详细检查结果
   按要求逐项检查：
   - 符合情况说明
   - 证据和依据
   - 不符合项识别
   - 风险等级评估

4. 违规问题分析
   - 违规项目清单
   - 违规严重程度
   - 违规原因分析
   - 影响范围评估

5. 风险评估
   - 合规风险识别
   - 法律法规风险
   - 业务影响风险
   - 声誉风险评估

6. 整改建议
   - 紧急整改事项
   - 短期改进措施
   - 长期完善计划
   - 预防机制建议

7. 监控建议
   - 持续监控机制
   - 定期检查安排
   - 预警指标设置
   - 报告机制建立

8. 合规结论
   - 总体合规评价
   - 是否达到要求
   - 改进时间建议
   - 复查安排

请确保检查严格准确，建议具有可操作性。
"""
        
        context_messages = self.get_conversation_context()
        context_messages.append({"role": "user", "content": compliance_prompt})
        
        compliance_result = self.call_llm(context_messages)
        
        result = {
            "type": "compliance_check",
            "requirements": compliance_requirements,
            "check_level": check_level,
            "content": compliance_result,
            "metadata": {
                "check_rigor": "严格",
                "coverage": "全面",
                "reliability": "高",
                "checked_at": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成合规性检查")
        return result
    
    async def _final_assessment(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        最终评估
        """
        project_deliverables = data.get("deliverables", [])
        assessment_criteria = data.get("criteria", self.review_criteria)
        stakeholder_requirements = data.get("requirements", {})
        
        print(f"🎯 {self.name} 正在进行最终评估")
        
        assessment_prompt = f"""
请对项目交付物进行最终评估：

项目交付物：
{json.dumps(project_deliverables, ensure_ascii=False, indent=2)}

评估标准：
{json.dumps(assessment_criteria, ensure_ascii=False, indent=2)}

利益相关者要求：
{json.dumps(stakeholder_requirements, ensure_ascii=False, indent=2)}

请提供综合的最终评估报告：

1. 评估概述
   - 评估范围和目标
   - 评估标准和方法
   - 评估团队和时间

2. 交付物评估
   对每个交付物进行评估：
   - 质量水平评定
   - 标准符合度
   - 完成度评估
   - 用户满意度

3. 综合质量分析
   - 整体质量水平
   - 各维度表现
   - 质量一致性
   - 质量稳定性

4. 目标达成度
   - 项目目标实现情况
   - 关键指标达成度
   - 用户需求满足度
   - 预期效果实现度

5. 优势和亮点
   - 突出表现方面
   - 创新点和特色
   - 超预期表现
   - 可复制经验

6. 问题和不足
   - 主要问题汇总
   - 影响和风险评估
   - 根本原因分析
   - 改进紧迫性

7. 价值评估
   - 商业价值实现
   - 技术价值体现
   - 社会价值贡献
   - 投资回报评估

8. 最终结论
   - 综合评价等级
   - 验收建议
   - 后续行动建议
   - 经验总结

请确保评估客观全面，结论可信可靠。
"""
        
        context_messages = self.get_conversation_context()
        context_messages.append({"role": "user", "content": assessment_prompt})
        
        assessment_result = self.call_llm(context_messages)
        
        result = {
            "type": "final_assessment",
            "deliverables": project_deliverables,
            "criteria": assessment_criteria,
            "content": assessment_result,
            "metadata": {
                "assessment_scope": "全面",
                "objectivity": "高",
                "reliability": "强",
                "assessed_at": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成最终评估")
        return result
    
    async def _general_review(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        通用审查任务
        """
        review_request = data.get("request", "")
        review_context = data.get("context", {})
        
        print(f"📝 {self.name} 正在进行通用审查")
        
        general_prompt = f"""
审查请求：{review_request}

背景信息：
{json.dumps(review_context, ensure_ascii=False, indent=2)}

请提供详细的审查报告，包括：

1. 审查理解和确认
2. 审查方法和标准
3. 详细审查结果
4. 问题和建议
5. 质量评估
6. 改进方案
7. 总结和结论

请确保审查全面客观，建议具有建设性。
"""
        
        context_messages = self.get_conversation_context()
        context_messages.append({"role": "user", "content": general_prompt})
        
        review_result = self.call_llm(context_messages)
        
        result = {
            "type": "general_review",
            "request": review_request,
            "context": review_context,
            "content": review_result,
            "metadata": {
                "review_type": "通用",
                "completeness": "全面",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成通用审查")
        return result
    
    def get_review_capabilities(self) -> Dict[str, Any]:
        """获取审查能力描述"""
        return {
            "supported_tasks": [
                "quality_review",
                "content_review",
                "process_review",
                "compliance_check",
                "final_assessment",
                "general_review"
            ],
            "review_criteria": self.review_criteria,
            "quality_levels": self.quality_levels,
            "review_methods": self.review_methods,
            "output_formats": ["审查报告", "质量评估", "改进建议", "合规检查"],
            "quality_standards": ["客观性", "全面性", "准确性", "建设性"]
        }

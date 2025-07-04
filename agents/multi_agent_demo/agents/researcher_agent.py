"""
研究员Agent

专门负责信息收集、分析和整理的智能代理。
研究员Agent的主要职责：
1. 收集相关主题的信息和资料
2. 分析信息的可靠性和相关性
3. 整理并结构化信息
4. 生成研究报告
"""
import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime

from .base_agent import BaseAgent, TaskResult

class ResearcherAgent(BaseAgent):
    """
    研究员Agent
    
    这个Agent专门负责信息研究和分析工作。它具有以下特点：
    - 系统性的信息收集能力
    - 客观的分析和评估
    - 结构化的信息整理
    - 可靠的研究报告生成
    """
    
    def __init__(self, agent_id: str = "researcher_001"):
        super().__init__(
            agent_id=agent_id,
            name="研究员小R",
            description="专业的信息研究和分析专家，擅长收集、整理和分析各种信息资料"
        )
        
        # 研究员专用配置
        self.research_methods = [
            "文献调研", "数据分析", "案例研究", "对比分析", "趋势分析"
        ]
        self.knowledge_domains = [
            "技术", "商业", "教育", "科学", "社会", "文化"
        ]
    
    def get_system_prompt(self) -> str:
        """获取研究员的系统提示词"""
        return """你是一名专业的研究员，名叫小R。你的主要职责是：

1. 信息收集与整理：
   - 系统性地收集相关主题的信息
   - 识别可靠和权威的信息源
   - 整理信息并去除重复和冗余内容

2. 分析与评估：
   - 客观分析信息的准确性和相关性
   - 识别信息之间的关联和模式
   - 评估信息的重要性和优先级

3. 报告生成：
   - 生成结构化的研究报告
   - 使用清晰的逻辑结构
   - 提供具体的数据和事实支撑

工作原则：
- 保持客观和中立的态度
- 注重事实和数据
- 使用系统化的研究方法
- 确保信息的准确性和可靠性

输出格式要求：
- 使用结构化的格式（标题、列表、表格等）
- 明确标注信息来源和可靠性
- 提供关键发现的总结
- 包含进一步研究的建议"""
    
    async def process_task(self, task: Dict[str, Any]) -> TaskResult:
        """
        处理研究任务
        
        支持的任务类型：
        - research_topic: 主题研究
        - analyze_data: 数据分析
        - literature_review: 文献综述
        - fact_checking: 事实核查
        """
        task_id = task.get("id", f"research_{int(asyncio.get_event_loop().time())}")
        task_type = task.get("type", "research_topic")
        task_data = task.get("data", {})
        
        try:
            if task_type == "research_topic":
                result = await self._research_topic(task_data)
            elif task_type == "analyze_data":
                result = await self._analyze_data(task_data)
            elif task_type == "literature_review":
                result = await self._literature_review(task_data)
            elif task_type == "fact_checking":
                result = await self._fact_checking(task_data)
            else:
                result = await self._general_research(task_data)
            
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
    
    async def _research_topic(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行主题研究
        
        Args:
            data: 包含研究主题和要求的数据
            
        Returns:
            研究报告
        """
        topic = data.get("topic", "")
        scope = data.get("scope", "全面")
        depth = data.get("depth", "中等")
        
        print(f"🔍 {self.name} 正在研究主题: {topic}")
        
        # 构建研究提示词
        research_prompt = f"""
请对以下主题进行{scope}的研究分析：

研究主题：{topic}
研究深度：{depth}
研究范围：{scope}

请提供以下内容：

1. 主题概述
   - 定义和基本概念
   - 主要特点和特征
   - 发展历程和现状

2. 关键要点分析
   - 核心概念和原理
   - 重要组成部分
   - 关键技术或方法

3. 相关案例和应用
   - 典型应用场景
   - 成功案例分析
   - 实际应用效果

4. 优势与挑战
   - 主要优势和价值
   - 面临的挑战和问题
   - 解决方案和改进方向

5. 发展趋势
   - 未来发展方向
   - 新兴技术和方法
   - 市场前景分析

6. 研究总结
   - 关键发现
   - 重要结论
   - 进一步研究建议

请确保信息准确、结构清晰、分析深入。
"""
        
        # 调用LLM进行研究
        context = self.get_conversation_context()
        context.append({"role": "user", "content": research_prompt})
        
        research_result = self.call_llm(context)
        
        # 构建结构化结果
        result = {
            "type": "topic_research",
            "topic": topic,
            "scope": scope,
            "depth": depth,
            "content": research_result,
            "metadata": {
                "research_methods": ["文献调研", "信息整理", "分析总结"],
                "confidence_level": "高",
                "completeness": "完整",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成主题研究: {topic}")
        return result
    
    async def _analyze_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行数据分析
        
        Args:
            data: 包含待分析数据的字典
            
        Returns:
            数据分析报告
        """
        dataset = data.get("dataset", "")
        analysis_type = data.get("analysis_type", "描述性分析")
        objectives = data.get("objectives", [])
        
        print(f"📊 {self.name} 正在进行数据分析")
        
        analysis_prompt = f"""
请对以下数据进行{analysis_type}：

数据内容：
{dataset}

分析目标：
{', '.join(objectives) if objectives else '全面分析数据特征和模式'}

请提供以下分析内容：

1. 数据概览
   - 数据规模和结构
   - 数据质量评估
   - 主要字段说明

2. 描述性统计
   - 基本统计信息
   - 数据分布特征
   - 异常值识别

3. 模式发现
   - 数据趋势分析
   - 关联关系识别
   - 聚类和分组

4. 关键洞察
   - 重要发现总结
   - 业务意义解释
   - 异常情况说明

5. 结论和建议
   - 主要结论
   - 行动建议
   - 进一步分析方向

请确保分析客观准确，结论有理有据。
"""
        
        context = self.get_conversation_context()
        context.append({"role": "user", "content": analysis_prompt})
        
        analysis_result = self.call_llm(context)
        
        result = {
            "type": "data_analysis",
            "analysis_type": analysis_type,
            "objectives": objectives,
            "content": analysis_result,
            "metadata": {
                "analysis_methods": ["描述性统计", "模式识别", "趋势分析"],
                "data_quality": "良好",
                "confidence_level": "高",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成数据分析")
        return result
    
    async def _literature_review(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行文献综述
        """
        topic = data.get("topic", "")
        timeframe = data.get("timeframe", "近5年")
        focus_areas = data.get("focus_areas", [])
        
        print(f"📚 {self.name} 正在进行文献综述: {topic}")
        
        review_prompt = f"""
请对以下主题进行文献综述：

综述主题：{topic}
时间范围：{timeframe}
重点领域：{', '.join(focus_areas) if focus_areas else '全面综述'}

请提供以下内容：

1. 研究背景
   - 研究问题的重要性
   - 研究领域的发展历程
   - 当前研究现状

2. 主要研究方向
   - 核心研究主题分类
   - 各方向的研究重点
   - 代表性研究成果

3. 研究方法演进
   - 主要研究方法
   - 方法论发展趋势
   - 新兴研究工具

4. 关键发现汇总
   - 重要研究结论
   - 一致性发现
   - 争议性问题

5. 研究空白识别
   - 尚未解决的问题
   - 研究空白领域
   - 未来研究方向

6. 综述总结
   - 整体发展趋势
   - 主要贡献总结
   - 未来研究建议

请确保覆盖全面，分析客观。
"""
        
        context = self.get_conversation_context()
        context.append({"role": "user", "content": review_prompt})
        
        review_result = self.call_llm(context)
        
        result = {
            "type": "literature_review",
            "topic": topic,
            "timeframe": timeframe,
            "focus_areas": focus_areas,
            "content": review_result,
            "metadata": {
                "review_scope": "综合性",
                "coverage": "全面",
                "quality": "高",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成文献综述")
        return result
    
    async def _fact_checking(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行事实核查
        """
        statements = data.get("statements", [])
        sources = data.get("sources", [])
        
        print(f"🔍 {self.name} 正在进行事实核查")
        
        checking_prompt = f"""
请对以下陈述进行事实核查：

待核查陈述：
{json.dumps(statements, ensure_ascii=False, indent=2)}

参考来源：
{json.dumps(sources, ensure_ascii=False, indent=2) if sources else '请基于常识和逻辑进行判断'}

请对每个陈述提供：

1. 事实核查结果
   - 真实性评估（真实/部分真实/虚假/无法确定）
   - 准确性程度
   - 可信度评级

2. 支撑证据
   - 相关事实和数据
   - 可靠信息来源
   - 权威机构观点

3. 问题分析
   - 错误或争议之处
   - 可能的误解原因
   - 需要澄清的概念

4. 修正建议
   - 准确的表述方式
   - 补充信息
   - 注意事项

请保持客观中立，基于事实进行判断。
"""
        
        context = self.get_conversation_context()
        context.append({"role": "user", "content": checking_prompt})
        
        checking_result = self.call_llm(context)
        
        result = {
            "type": "fact_checking",
            "statements": statements,
            "sources": sources,
            "content": checking_result,
            "metadata": {
                "checking_criteria": ["准确性", "可靠性", "完整性"],
                "verification_level": "严格",
                "confidence": "高",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成事实核查")
        return result
    
    async def _general_research(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行通用研究任务
        """
        query = data.get("query", "")
        requirements = data.get("requirements", [])
        
        print(f"🔍 {self.name} 正在进行通用研究")
        
        general_prompt = f"""
研究请求：{query}

特殊要求：
{json.dumps(requirements, ensure_ascii=False, indent=2) if requirements else '标准研究流程'}

请提供全面的研究报告，包括：

1. 主题分析
2. 关键信息收集
3. 相关案例研究
4. 问题和挑战
5. 解决方案建议
6. 总结和结论

请确保信息准确、分析深入、结构清晰。
"""
        
        context = self.get_conversation_context()
        context.append({"role": "user", "content": general_prompt})
        
        research_result = self.call_llm(context)
        
        result = {
            "type": "general_research",
            "query": query,
            "requirements": requirements,
            "content": research_result,
            "metadata": {
                "research_approach": "综合性",
                "completeness": "全面",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        print(f"✅ {self.name} 完成通用研究")
        return result
    
    def get_research_capabilities(self) -> Dict[str, Any]:
        """获取研究能力描述"""
        return {
            "supported_tasks": [
                "research_topic",
                "analyze_data", 
                "literature_review",
                "fact_checking",
                "general_research"
            ],
            "research_methods": self.research_methods,
            "knowledge_domains": self.knowledge_domains,
            "output_formats": ["报告", "分析", "综述", "核查结果"],
            "quality_standards": ["准确性", "客观性", "完整性", "可读性"]
        }

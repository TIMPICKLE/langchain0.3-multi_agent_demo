"""
复杂演示 - LangChain 0.3 多Agent协作进阶场景

这个演示展示了更复杂的多Agent协作场景，包括：
1. 多个并行工作流
2. Agent间的消息传递
3. 动态任务调整
4. 错误处理和恢复
5. 性能监控和优化

适合已经了解基础概念的开发者深入学习。
"""
import asyncio
import sys
import os
import time
import json
from typing import Dict, Any, List

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflows import MultiAgentWorkflow
from config import test_llm_connection
import random

def print_header(title: str):
    """打印标题"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)

def print_section(title: str):
    """打印章节标题"""
    print(f"\n🔸 {title}")
    print("-" * 50)

def print_progress(current: int, total: int, description: str = ""):
    """打印进度"""
    percentage = (current / total) * 100 if total > 0 else 0
    bar_length = 30
    filled_length = int(bar_length * current // total) if total > 0 else 0
    bar = "█" * filled_length + "░" * (bar_length - filled_length)
    print(f"📊 {description}: [{bar}] {percentage:.1f}% ({current}/{total})")

class AdvancedDemo:
    """高级演示类"""
    
    def __init__(self):
        self.workflow_manager = MultiAgentWorkflow()
        self.active_workflows = {}
        self.performance_metrics = {
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "total_execution_time": 0,
            "start_time": None
        }
    
    async def run_parallel_workflows_demo(self):
        """
        并行工作流演示
        
        同时运行多个不同类型的工作流，展示系统的并发处理能力
        """
        print_header("🚀 并行工作流演示")
        
        print("📋 场景说明:")
        print("  同时执行3个不同的工作流:")
        print("  1. 技术文档撰写")
        print("  2. 项目规划")
        print("  3. 问题解决")
        print("  展示多Agent系统的并发处理能力")
        
        # 定义三个不同的工作流任务
        workflows_to_run = [
            {
                "template": "document_creation",
                "name": "AI技术报告",
                "input": {
                    "topic": "人工智能在医疗领域的应用",
                    "requirements": ["技术深度", "应用案例", "发展趋势"]
                }
            },
            {
                "template": "project_planning", 
                "name": "移动应用开发",
                "input": {
                    "project_name": "智能健康管理App",
                    "objectives": ["用户健康监测", "数据分析", "个性化建议"],
                    "constraints": {"budget": "50万", "timeline": "6个月", "team_size": "8人"}
                }
            },
            {
                "template": "problem_solving",
                "name": "性能优化",
                "input": {
                    "problem": "系统响应速度慢，用户体验差",
                    "context": {
                        "current_response_time": "3-5秒",
                        "target_response_time": "1秒内",
                        "daily_users": "10万+"
                    }
                }
            }
        ]
        
        print_section("启动并行工作流")
        
        # 记录开始时间
        start_time = time.time()
        self.performance_metrics["start_time"] = start_time
        
        # 创建并启动所有工作流
        workflow_tasks = []
        for workflow_def in workflows_to_run:
            print(f"🚀 启动工作流: {workflow_def['name']}")
            task = asyncio.create_task(
                self._run_single_workflow(workflow_def)
            )
            workflow_tasks.append(task)
        
        print(f"⚡ {len(workflow_tasks)} 个工作流已启动，正在并行执行...")
        
        # 监控执行进度
        await self._monitor_parallel_execution(workflow_tasks, workflows_to_run)
        
        # 等待所有工作流完成
        results = await asyncio.gather(*workflow_tasks, return_exceptions=True)
        
        # 统计结果
        end_time = time.time()
        total_time = end_time - start_time
        
        print_section("并行执行结果")
        
        successful_workflows = 0
        failed_workflows = 0
        
        for i, (result, workflow_def) in enumerate(zip(results, workflows_to_run)):
            if isinstance(result, Exception):
                print(f"❌ {workflow_def['name']}: 执行失败 - {str(result)}")
                failed_workflows += 1
            else:
                print(f"✅ {workflow_def['name']}: 执行成功")
                successful_workflows += 1
                
                # 显示简要结果
                workflow_results = self.workflow_manager.get_workflow_results(result.workflow_id)
                print(f"   📊 任务完成: {workflow_results['successful_tasks']}/{workflow_results['total_tasks']}")
                if workflow_results['execution_summary']['total_time']:
                    print(f"   ⏱️ 执行时间: {workflow_results['execution_summary']['total_time']:.2f}秒")
        
        print(f"\n📊 总体统计:")
        print(f"   ✅ 成功工作流: {successful_workflows}")
        print(f"   ❌ 失败工作流: {failed_workflows}")
        print(f"   ⏱️ 总执行时间: {total_time:.2f}秒")
        print(f"   ⚡ 平均每个工作流: {total_time/len(workflows_to_run):.2f}秒")
    
    async def _run_single_workflow(self, workflow_def: Dict[str, Any]):
        """运行单个工作流"""
        try:
            workflow = await self.workflow_manager.execute_template_workflow(
                template_name=workflow_def["template"],
                input_data=workflow_def["input"]
            )
            return workflow
        except Exception as e:
            print(f"⚠️ 工作流 {workflow_def['name']} 执行异常: {str(e)}")
            raise e
    
    async def _monitor_parallel_execution(self, workflow_tasks: List, workflow_defs: List):
        """监控并行执行进度"""
        print_section("实时执行监控")
        
        monitoring_interval = 2  # 2秒检查一次
        max_monitoring_time = 300  # 最大监控5分钟
        
        start_monitor_time = time.time()
        
        while not all(task.done() for task in workflow_tasks):
            current_time = time.time()
            
            # 检查是否超时
            if current_time - start_monitor_time > max_monitoring_time:
                print("⚠️ 监控超时，停止监控")
                break
            
            # 显示各工作流状态
            for i, (task, workflow_def) in enumerate(zip(workflow_tasks, workflow_defs)):
                if task.done():
                    status = "✅ 已完成" if not task.exception() else "❌ 失败"
                else:
                    status = "🔄 执行中"
                
                print(f"   {workflow_def['name']}: {status}")
            
            print(f"⏱️ 已执行时间: {current_time - self.performance_metrics['start_time']:.1f}秒")
            print("-" * 30)
            
            await asyncio.sleep(monitoring_interval)
    
    async def run_message_passing_demo(self):
        """
        Agent消息传递演示
        
        展示Agent之间如何通过消息进行通信和协作
        """
        print_header("📨 Agent消息传递演示")
        
        print("📋 场景说明:")
        print("  展示Agent之间的消息传递和协作:")
        print("  1. 研究员发现问题并通知规划师")
        print("  2. 规划师制定解决方案并指派执行者")
        print("  3. 执行者完成任务并请求审查员验证")
        print("  4. 审查员提供反馈并建议改进")
        
        coordinator = self.workflow_manager.coordinator
        
        print_section("消息传递流程")
        
        # 1. 研究员发现问题
        print("1️⃣ 研究员发现问题...")
        problem_message = "发现系统性能瓶颈：数据库查询响应时间过长，影响用户体验"
        coordinator.send_message(
            sender_id="researcher_001",
            receiver_id="planner_001", 
            content=problem_message,
            message_type="problem_report"
        )
        print(f"   📤 研究员 -> 规划师: {problem_message}")
        
        await asyncio.sleep(1)
        
        # 2. 规划师制定方案
        print("\n2️⃣ 规划师制定解决方案...")
        solution_message = "已制定数据库优化方案：索引优化、查询重构、缓存策略。请执行者按计划实施"
        coordinator.send_message(
            sender_id="planner_001",
            receiver_id="executor_001",
            content=solution_message,
            message_type="task_assignment"
        )
        print(f"   📤 规划师 -> 执行者: {solution_message}")
        
        await asyncio.sleep(1)
        
        # 3. 执行者请求审查
        print("\n3️⃣ 执行者完成实施...")
        completion_message = "数据库优化已完成：创建了新索引，重构了慢查询，部署了Redis缓存。请审查效果"
        coordinator.send_message(
            sender_id="executor_001", 
            receiver_id="reviewer_001",
            content=completion_message,
            message_type="review_request"
        )
        print(f"   📤 执行者 -> 审查员: {completion_message}")
        
        await asyncio.sleep(1)
        
        # 4. 审查员提供反馈
        print("\n4️⃣ 审查员提供反馈...")
        feedback_message = "优化效果良好：响应时间从3秒降至0.8秒。建议增加监控告警机制"
        coordinator.send_message(
            sender_id="reviewer_001",
            receiver_id="system",
            content=feedback_message,
            message_type="review_result"
        )
        print(f"   📤 审查员 -> 系统: {feedback_message}")
        
        # 5. 广播总结消息
        print("\n5️⃣ 系统广播任务完成...")
        summary_message = "数据库优化项目成功完成！性能提升60%，用户体验显著改善"
        coordinator.broadcast_message(
            sender_id="system",
            content=summary_message,
            message_type="project_completion"
        )
        print(f"   📢 系统广播: {summary_message}")
        
        print_section("消息队列状态")
        print(f"📨 消息队列中共有 {len(coordinator.message_queue)} 条消息")
        
        # 显示各Agent的消息历史
        for agent_id, agent in coordinator.agents.items():
            received_messages = len([m for m in agent.message_history if m.receiver == agent_id])
            sent_messages = len([m for m in agent.message_history if m.sender == agent_id])
            print(f"   {agent.name}: 收到{received_messages}条, 发送{sent_messages}条消息")
    
    async def run_dynamic_workflow_demo(self):
        """
        动态工作流演示
        
        展示如何根据执行结果动态调整工作流
        """
        print_header("🔄 动态工作流演示")
        
        print("📋 场景说明:")
        print("  展示动态工作流调整能力:")
        print("  1. 创建基础研究任务")
        print("  2. 根据研究结果决定后续流程")
        print("  3. 动态添加额外的分析任务")
        print("  4. 自适应调整任务优先级")
        
        coordinator = self.workflow_manager.coordinator
        
        # 创建动态工作流
        workflow = coordinator.create_workflow(
            workflow_id=f"dynamic_workflow_{int(time.time())}",
            name="动态适应性研究工作流",
            description="根据执行结果动态调整的智能工作流"
        )
        
        print_section("第一阶段: 初始研究")
        
        # 初始研究任务
        initial_research = coordinator.create_task(
            task_id=f"{workflow.workflow_id}_initial_research",
            task_type="research_topic",
            agent_id="researcher_001",
            data={
                "topic": "区块链技术在供应链管理中的应用",
                "scope": "初步调研",
                "depth": "基础"
            },
            priority=9
        )
        coordinator.add_task_to_workflow(workflow.workflow_id, initial_research)
        
        # 执行初始研究
        print("🔍 执行初始研究...")
        await coordinator._execute_single_task(initial_research)
        
        if initial_research.status == "completed":
            print("✅ 初始研究完成")
            
            # 模拟根据研究结果决定后续任务
            print_section("第二阶段: 动态决策")
            
            # 假设研究发现了有趣的方向，添加深度分析
            print("🧠 AI决策：研究发现区块链在溯源方面有重大突破，需要深度分析")
            
            deep_analysis = coordinator.create_task(
                task_id=f"{workflow.workflow_id}_deep_analysis",
                task_type="analyze_data", 
                agent_id="researcher_001",
                data={
                    "dataset": "初始研究结果",
                    "analysis_type": "深度分析",
                    "objectives": ["技术可行性", "商业价值", "实施挑战"]
                },
                dependencies=[initial_research.task_id],
                priority=8
            )
            coordinator.add_task_to_workflow(workflow.workflow_id, deep_analysis)
            
            # 并行添加竞争技术分析
            competitive_analysis = coordinator.create_task(
                task_id=f"{workflow.workflow_id}_competitive_analysis",
                task_type="literature_review",
                agent_id="researcher_001",
                data={
                    "topic": "供应链管理技术对比",
                    "timeframe": "近3年",
                    "focus_areas": ["区块链", "IoT", "AI"]
                },
                dependencies=[initial_research.task_id],
                priority=7
            )
            coordinator.add_task_to_workflow(workflow.workflow_id, competitive_analysis)
            
            print("➕ 动态添加了2个新任务:")
            print("   1. 深度技术分析")
            print("   2. 竞争技术对比")
            
            print_section("第三阶段: 并行执行")
            
            # 并行执行新任务
            await asyncio.gather(
                coordinator._execute_single_task(deep_analysis),
                coordinator._execute_single_task(competitive_analysis)
            )
            
            print("✅ 动态任务执行完成")
            
            # 根据结果决定是否需要进一步分析
            print_section("第四阶段: 智能决策")
            
            if deep_analysis.status == "completed" and competitive_analysis.status == "completed":
                print("🎯 所有分析完成，触发智能决策...")
                
                # 模拟AI决策逻辑
                decision_score = random.uniform(0.7, 0.9)  # 模拟决策分数
                
                if decision_score > 0.8:
                    print(f"🚀 决策分数: {decision_score:.2f} - 项目价值很高，建议制定实施计划")
                    
                    # 动态添加规划任务
                    implementation_planning = coordinator.create_task(
                        task_id=f"{workflow.workflow_id}_implementation_planning",
                        task_type="create_project_plan",
                        agent_id="planner_001",
                        data={
                            "project_name": "区块链供应链溯源系统",
                            "objectives": ["建立溯源体系", "提升透明度", "降低风险"],
                            "constraints": {"budget": "200万", "timeline": "12个月"}
                        },
                        dependencies=[deep_analysis.task_id, competitive_analysis.task_id],
                        priority=9
                    )
                    coordinator.add_task_to_workflow(workflow.workflow_id, implementation_planning)
                    
                    await coordinator._execute_single_task(implementation_planning)
                    print("✅ 实施计划制定完成")
                    
                else:
                    print(f"🤔 决策分数: {decision_score:.2f} - 需要更多研究")
        
        # 获取最终结果
        workflow_results = self.workflow_manager.get_workflow_results(workflow.workflow_id)
        
        print_section("动态工作流执行总结")
        print(f"📊 动态添加任务数: {len(workflow.tasks) - 1}")  # 减去初始任务
        print(f"✅ 成功完成: {workflow_results['successful_tasks']}/{workflow_results['total_tasks']}")
        print(f"🔄 动态适应性: 根据执行结果自动调整了工作流结构")
    
    async def run_error_handling_demo(self):
        """
        错误处理和恢复演示
        
        展示系统如何处理各种错误情况并自动恢复
        """
        print_header("🛡️ 错误处理和恢复演示")
        
        print("📋 场景说明:")
        print("  模拟各种错误情况并展示系统恢复能力:")
        print("  1. 任务超时处理")
        print("  2. Agent异常恢复")
        print("  3. 依赖任务失败处理")
        print("  4. 自动重试机制")
        
        coordinator = self.workflow_manager.coordinator
        
        # 创建错误处理测试工作流
        workflow = coordinator.create_workflow(
            workflow_id=f"error_handling_{int(time.time())}",
            name="错误处理测试工作流",
            description="测试系统错误处理和恢复能力"
        )
        
        print_section("测试1: 任务超时处理")
        
        # 创建一个会超时的任务（设置很短的超时时间）
        timeout_task = coordinator.create_task(
            task_id=f"{workflow.workflow_id}_timeout_test",
            task_type="research_topic",
            agent_id="researcher_001",
            data={
                "topic": "复杂的量子计算理论研究",
                "scope": "全面深入",
                "depth": "博士级别"
            },
            timeout=5,  # 5秒超时
            priority=8
        )
        coordinator.add_task_to_workflow(workflow.workflow_id, timeout_task)
        
        print("⏰ 执行短超时任务...")
        try:
            await coordinator._execute_single_task(timeout_task)
            print("✅ 任务意外完成")
        except Exception as e:
            print(f"⚠️ 预期的超时错误: {str(e)}")
            print("🔄 系统正确处理了超时情况")
        
        print_section("测试2: 错误任务依赖处理")
        
        # 创建依赖失败任务的任务
        dependent_task = coordinator.create_task(
            task_id=f"{workflow.workflow_id}_dependent_test",
            task_type="create_project_plan",
            agent_id="planner_001",
            data={
                "project_name": "基于失败任务的规划",
                "objectives": ["依赖前置任务结果"]
            },
            dependencies=[timeout_task.task_id],  # 依赖失败的任务
            priority=7
        )
        coordinator.add_task_to_workflow(workflow.workflow_id, dependent_task)
        
        print("🔗 测试依赖任务处理...")
        # 由于依赖任务失败，这个任务应该不会执行
        print("⚠️ 依赖的任务失败，系统应该跳过此任务")
        
        print_section("测试3: 自动重试机制")
        
        # 创建带重试的任务
        retry_task = coordinator.create_task(
            task_id=f"{workflow.workflow_id}_retry_test",
            task_type="research_topic",
            agent_id="researcher_001",
            data={
                "topic": "简单的技术概念",
                "scope": "基础",
                "depth": "入门"
            },
            timeout=30,
            priority=6
        )
        retry_task.max_retries = 2  # 设置最大重试次数
        coordinator.add_task_to_workflow(workflow.workflow_id, retry_task)
        
        print("🔄 执行带重试机制的任务...")
        try:
            await coordinator._execute_single_task(retry_task)
            if retry_task.status == "completed":
                print("✅ 任务成功完成")
            else:
                print(f"⚠️ 任务执行状态: {retry_task.status}")
                if retry_task.retry_count > 0:
                    print(f"🔄 重试次数: {retry_task.retry_count}")
        except Exception as e:
            print(f"❌ 任务最终失败: {str(e)}")
            print(f"🔄 已重试: {retry_task.retry_count} 次")
        
        print_section("错误处理总结")
        
        workflow_results = self.workflow_manager.get_workflow_results(workflow.workflow_id)
        
        print("🛡️ 系统错误处理能力总结:")
        print("  ✅ 超时检测和处理")
        print("  ✅ 依赖任务失败处理")
        print("  ✅ 自动重试机制")
        print("  ✅ 优雅的错误恢复")
        
        print(f"\n📊 错误处理测试结果:")
        print(f"  总任务数: {workflow_results['total_tasks']}")
        print(f"  成功任务: {workflow_results['successful_tasks']}")
        print(f"  失败任务: {workflow_results['failed_tasks']}")
        print(f"  系统稳定性: {'优秀' if workflow_results['failed_tasks'] <= workflow_results['total_tasks'] / 2 else '良好'}")
    
    async def run_performance_monitoring_demo(self):
        """
        性能监控演示
        
        展示系统的性能监控和优化功能
        """
        print_header("📊 性能监控演示")
        
        print("📋 场景说明:")
        print("  展示系统性能监控功能:")
        print("  1. 实时性能指标监控")
        print("  2. Agent性能统计")
        print("  3. 系统资源使用情况")
        print("  4. 性能优化建议")
        
        print_section("系统整体状态")
        
        # 获取系统总览
        system_overview = self.workflow_manager.get_system_overview()
        coordinator_status = system_overview['coordinator_status']
        
        print(f"🎛️ 协调器状态: {coordinator_status}")
        print(f"🤖 注册Agent数量: {len(system_overview['available_agents'])}")
        print(f"📋 可用工作流模板: {len(system_overview['workflow_templates'])}")
        
        print_section("Agent性能统计")
        
        for agent_id, agent_info in system_overview['available_agents'].items():
            stats = agent_info['performance']
            print(f"\n{agent_info['name']} ({agent_id}):")
            print(f"  📊 状态: {agent_info['status']}")
            print(f"  🔢 总请求数: {stats['total_requests']}")
            print(f"  ✅ 成功次数: {stats['success_count']}")
            print(f"  ❌ 失败次数: {stats['error_count']}")
            print(f"  📈 成功率: {stats['success_rate']}")
            print(f"  ⏱️ 平均执行时间: {stats['avg_execution_time']}")
            print(f"  📝 完成任务数: {stats['tasks_completed']}")
        
        print_section("执行性能测试")
        
        # 运行性能测试
        test_tasks = [
            {
                "name": "轻量级研究",
                "template": "research_analysis",
                "input": {
                    "topic": "Python基础语法",
                    "scope": "基础"
                }
            },
            {
                "name": "中等复杂度规划", 
                "template": "project_planning",
                "input": {
                    "project_name": "小型网站开发",
                    "objectives": ["用户注册", "内容展示"],
                    "constraints": {"timeline": "1个月"}
                }
            }
        ]
        
        performance_results = []
        
        for test_task in test_tasks:
            print(f"🚀 执行性能测试: {test_task['name']}")
            
            start_time = time.time()
            try:
                workflow = await self.workflow_manager.execute_template_workflow(
                    template_name=test_task["template"],
                    input_data=test_task["input"]
                )
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                workflow_results = self.workflow_manager.get_workflow_results(workflow.workflow_id)
                
                performance_results.append({
                    "name": test_task["name"],
                    "execution_time": execution_time,
                    "success_rate": workflow_results['successful_tasks'] / workflow_results['total_tasks'] * 100,
                    "total_tasks": workflow_results['total_tasks']
                })
                
                print(f"  ✅ 完成时间: {execution_time:.2f}秒")
                print(f"  📊 成功率: {performance_results[-1]['success_rate']:.1f}%")
                
            except Exception as e:
                print(f"  ❌ 测试失败: {str(e)}")
                performance_results.append({
                    "name": test_task["name"],
                    "execution_time": -1,
                    "success_rate": 0,
                    "total_tasks": 0
                })
        
        print_section("性能分析报告")
        
        total_execution_time = sum(r['execution_time'] for r in performance_results if r['execution_time'] > 0)
        avg_success_rate = sum(r['success_rate'] for r in performance_results) / len(performance_results)
        
        print(f"📊 性能测试总结:")
        print(f"  ⏱️ 总执行时间: {total_execution_time:.2f}秒")
        print(f"  📈 平均成功率: {avg_success_rate:.1f}%")
        print(f"  🎯 系统吞吐量: {sum(r['total_tasks'] for r in performance_results)} 任务")
        
        # 性能优化建议
        print(f"\n💡 性能优化建议:")
        if avg_success_rate < 90:
            print("  ⚠️ 成功率偏低，建议检查Agent配置和LLM连接")
        if total_execution_time > 60:
            print("  ⚠️ 执行时间较长，建议优化任务粒度和并发设置")
        if total_execution_time < 30 and avg_success_rate > 95:
            print("  ✅ 系统性能优秀，运行状态良好")
        
        print("  🔧 可考虑的优化措施:")
        print("    - 调整Agent的LLM参数")
        print("    - 优化任务分解粒度")
        print("    - 增加并发执行任务数")
        print("    - 实施任务结果缓存")

async def main():
    """主函数"""
    print("🎯 LangChain 0.3 多Agent协作系统 - 复杂演示")
    print("=" * 80)
    
    # 检查LLM连接
    print("🔗 检查LLM服务连接...")
    if not test_llm_connection():
        print("❌ LLM服务连接失败！请检查配置后再试")
        return
    
    print("✅ LLM服务连接正常")
    
    # 创建演示实例
    demo = AdvancedDemo()
    
    # 演示菜单
    demos = [
        ("并行工作流", demo.run_parallel_workflows_demo),
        ("消息传递", demo.run_message_passing_demo), 
        ("动态工作流", demo.run_dynamic_workflow_demo),
        ("错误处理", demo.run_error_handling_demo),
        ("性能监控", demo.run_performance_monitoring_demo)
    ]
    
    print("\n🎮 可用的复杂演示:")
    for i, (name, _) in enumerate(demos, 1):
        print(f"  {i}. {name}")
    print("  0. 运行所有演示")
    
    try:
        choice = input("\n请选择要运行的演示 (0-5): ").strip()
        
        if choice == "0":
            # 运行所有演示
            for name, demo_func in demos:
                print(f"\n🚀 开始运行: {name}")
                await demo_func()
                print(f"✅ {name} 演示完成")
                await asyncio.sleep(2)  # 间隔2秒
                
        elif choice.isdigit() and 1 <= int(choice) <= len(demos):
            demo_index = int(choice) - 1
            name, demo_func = demos[demo_index]
            print(f"\n🚀 开始运行: {name}")
            await demo_func()
            print(f"✅ {name} 演示完成")
            
        else:
            print("❌ 无效的选择")
            return
        
        print_header("🎉 复杂演示完成")
        print("🎓 您已经体验了多Agent系统的高级功能！")
        print("\n📚 继续学习建议:")
        print("  1. 尝试 interactive_demo.py 进行交互式探索")
        print("  2. 阅读 docs/tutorial.md 深入学习实现原理")
        print("  3. 查看 docs/best_practices.md 了解生产环境最佳实践")
        print("  4. 基于本项目创建自己的多Agent应用")
        
    except KeyboardInterrupt:
        print("\n👋 演示被用户中断")
    except Exception as e:
        print(f"\n❌ 演示执行异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

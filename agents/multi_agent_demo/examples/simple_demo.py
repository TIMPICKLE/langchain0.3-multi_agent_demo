"""
简单演示 - LangChain 0.3 多Agent协作

这个演示展示了最基本的多Agent协作流程，通过一个简单的
文档撰写任务来演示Agent之间是如何协作的。

适合初学者理解多Agent系统的基本概念和工作原理。
"""
import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflows import MultiAgentWorkflow
from config import test_llm_connection
import json

def print_separator(title: str = ""):
    """打印分隔线"""
    print("\n" + "="*60)
    if title:
        print(f"  {title}")
        print("="*60)
    print()

def print_task_result(task_result: dict):
    """打印任务结果"""
    print(f"🎯 任务ID: {task_result['task_id']}")
    print(f"📋 执行Agent: {task_result['agent_id']}")
    print(f"✅ 状态: {task_result['status']}")
    print(f"⏱️ 执行时间: {task_result['execution_time']:.2f}秒")
    
    if task_result['status'] == 'success' and task_result['result']:
        result_content = task_result['result'].get('content', '')
        if result_content:
            # 截取前200个字符作为预览
            preview = result_content[:200] + "..." if len(result_content) > 200 else result_content
            print(f"📄 结果预览: {preview}")
    
    if task_result.get('error_message'):
        print(f"❌ 错误信息: {task_result['error_message']}")
    
    print("-" * 40)

async def simple_document_creation_demo():
    """
    简单文档创建演示
    
    演示4个Agent协作完成一个技术文档的撰写：
    1. 研究员收集LangChain相关信息
    2. 规划师制定文档撰写计划
    3. 执行者撰写文档内容
    4. 审查员检查文档质量
    """
    print_separator("🚀 LangChain 0.3 多Agent协作演示")
    
    print("📋 演示场景: 协作撰写 'LangChain 入门指南' 技术文档")
    print("🤖 参与Agent: 研究员小R、规划师小P、执行者小E、审查员小V")
    print("🔄 工作流程: 研究 → 规划 → 执行 → 审查")
    
    # 初始化多Agent工作流
    print("\n🔧 正在初始化多Agent工作流...")
    workflow_manager = MultiAgentWorkflow()
    
    # 定义任务输入 - 简化版本以减少处理时间
    task_input = {
        "topic": "LangChain 快速入门",
        "requirements": [
            "简洁明了",
            "包含核心概念",
            "提供基本示例"
        ],
        "length": "简短",  # 添加长度限制
        "complexity": "basic"  # 添加复杂度控制
    }
    
    print(f"📝 文档主题: {task_input['topic']}")
    print(f"📋 文档要求: {', '.join(task_input['requirements'])}")
    print(f"📏 文档长度: {task_input['length']}")
    
    try:
        print_separator("开始执行工作流")
        
        # 显示预估时间
        print("⏱️  预估执行时间: 2-5分钟")
        print("🔄 正在执行，请耐心等待...")
        
        # 执行文档创建工作流
        workflow = await workflow_manager.execute_template_workflow(
            template_name="document_creation",
            input_data=task_input
        )
        
        print_separator("工作流执行完成")
        
        # 获取执行结果
        results = workflow_manager.get_workflow_results(workflow.workflow_id)
        
        print(f"📊 工作流状态: {results['status']}")
        print(f"📈 完成进度: {results['progress']:.1f}%")
        print(f"✅ 成功任务: {results['successful_tasks']}/{results['total_tasks']}")
        
        if results['failed_tasks'] > 0:
            print(f"❌ 失败任务: {results['failed_tasks']}")
            print("\n🔧 失败原因分析:")
            for task_result in results['task_results']:
                if task_result['status'] == 'failed':
                    error_msg = task_result.get('error_message', '')
                    if 'timeout' in error_msg.lower():
                        print(f"  ⏱️  {task_result['task_id']}: 响应超时")
                    elif 'connection' in error_msg.lower():
                        print(f"  🔗 {task_result['task_id']}: 连接问题")
                    else:
                        print(f"  ❓ {task_result['task_id']}: {error_msg[:100]}")
        
        # 显示执行时间
        if results['execution_summary']['total_time']:
            print(f"⏱️ 总执行时间: {results['execution_summary']['total_time']:.2f}秒")
        
        print_separator("详细任务结果")
        
        # 显示每个任务的结果
        for i, task_result in enumerate(results['task_results'], 1):
            print(f"\n第{i}步:")
            print_task_result(task_result)
        
        # 只有在有成功任务时才显示内容
        successful_tasks = [t for t in results['task_results'] if t['status'] == 'success']
        
        if successful_tasks:
            print_separator("成功任务内容")
            
            for task_result in successful_tasks:
                if task_result['result'] and task_result['result'].get('content'):
                    task_name = task_result['task_id'].split('_')[-1]  # 获取任务类型
                    print(f"\n📝 {task_name.upper()} 结果:")
                    print("-" * 40)
                    content = task_result['result']['content']
                    # 限制显示长度
                    if len(content) > 1000:
                        print(content[:1000] + "\n... (内容截断)")
                    else:
                        print(content)
                    print("-" * 40)
        
        print_separator("演示总结")
        
        if results['successful_tasks'] > 0:
            print("🎉 部分或全部任务执行成功！")
            print("\n📚 本演示展示了以下关键概念:")
            print("  1. Agent角色分工 - 每个Agent都有特定的职责")
            print("  2. 任务依赖关系 - 后续任务依赖前面任务的结果")
            print("  3. 异步执行 - 多个任务可以并行或串行执行")
            print("  4. 结果传递 - Agent之间可以传递和共享信息")
            print("  5. 质量控制 - 通过审查确保输出质量")
            
            print("\n🔧 系统统计信息:")
            system_overview = workflow_manager.get_system_overview()
            for agent_id, agent_info in system_overview['available_agents'].items():
                stats = agent_info['performance']
                print(f"  {agent_info['name']}: {stats['success_count']}次成功调用, "
                      f"平均{stats['avg_execution_time']}耗时")
        else:
            print("⚠️  所有任务都失败了，这可能是由于:")
            print("  1. LLM服务响应时间过长")
            print("  2. 网络连接不稳定")
            print("  3. 服务器负载过高")
            print("\n💡 建议尝试:")
            print("  1. 运行 python test_llm_performance.py 测试连接")
            print("  2. 检查LLM服务状态")
            print("  3. 稍后重试")
        
        return results['successful_tasks'] > 0
        
    except Exception as e:
        print(f"❌ 演示执行失败: {str(e)}")
        print("\n🔧 可能的原因:")
        print("  1. LLM服务连接问题")
        print("  2. 配置文件设置错误")
        print("  3. 网络连接问题")
        print("  4. 服务器响应超时")
        print("\n💡 建议检查:")
        print("  - config/llm_config.py中的LLM服务配置")
        print("  - 运行 python test_llm_performance.py 进行诊断")
        return False

async def test_agent_capabilities():
    """
    测试Agent能力演示
    
    展示每个Agent的独特能力和特点
    """
    print_separator("🧪 Agent能力测试")
    
    workflow_manager = MultiAgentWorkflow()
    
    # 测试研究员
    print("🔍 测试研究员Agent...")
    research_input = {
        "topic": "人工智能的发展历程",
        "scope": "简要",
        "depth": "基础"
    }
    
    try:
        research_workflow = await workflow_manager.coordinator.execute_workflow(
            workflow_manager.coordinator.create_workflow(
                "research_test", "研究员能力测试", "测试研究员的基本能力"
            ).workflow_id
        )
        print("✅ 研究员测试成功")
    except Exception as e:
        print(f"❌ 研究员测试失败: {e}")
    
    print("📋 各Agent能力说明:")
    agents = workflow_manager.coordinator.agents
    for agent_id, agent in agents.items():
        print(f"  {agent.name}: {agent.description}")

def main():
    """主函数"""
    print("🎯 LangChain 0.3 多Agent协作系统 - 简单演示")
    print("=" * 60)
    
    # 检查LLM连接
    print("🔗 检查LLM服务连接...")
    if not test_llm_connection():
        print("❌ LLM服务连接失败！")
        print("💡 请检查config/llm_config.py中的配置是否正确")
        print("📋 确保以下信息正确:")
        print(f"   - LLM服务地址: http://127.0.0.1:6000/v1")
        print(f"   - 模型名称: DeepSeek-V3-0324-HSW")
        print("\n🧪 建议运行性能测试:")
        print("   python test_llm_performance.py")
        return
    
    print("✅ LLM服务连接正常")
    
    # 提示用户关于性能
    print("\n⚠️  性能提示:")
    print("  - 首次运行可能需要2-5分钟")
    print("  - 如果超时，已优化参数减少token使用")
    print("  - 可运行 test_llm_performance.py 测试服务性能")
    
    # 运行演示
    try:
        # 运行文档创建演示
        success = asyncio.run(simple_document_creation_demo())
        
        if success:
            print("\n🎓 下一步学习建议:")
            print("  1. 查看 complex_demo.py 了解更复杂的场景")
            print("  2. 尝试 interactive_demo.py 进行交互式探索")
            print("  3. 阅读 docs/tutorial.md 深入学习")
            print("  4. 查看 docs/api_reference.md 了解API详情")
            print("  5. 运行 test_llm_performance.py 测试性能")
        else:
            print("\n🔧 故障排除建议:")
            print("  1. 运行 python test_llm_performance.py")
            print("  2. 检查LLM服务状态和负载")
            print("  3. 确认网络连接稳定")
            print("  4. 查看错误日志寻找详细信息")
        
    except KeyboardInterrupt:
        print("\n👋 演示被用户中断")
    except Exception as e:
        print(f"\n❌ 演示执行异常: {str(e)}")
        print("🔧 建议:")
        print("  1. 运行 python test_llm_performance.py 诊断问题")
        print("  2. 检查config/llm_config.py配置")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

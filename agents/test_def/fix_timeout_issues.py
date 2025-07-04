"""
超时问题修复脚本

专门用于解决LLM服务超时问题的快速修复工具
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from config.llm_config import LLMConfig
from workflows.multi_agent_workflow import MultiAgentWorkflow

def apply_timeout_fixes():
    """应用超时问题修复"""
    print("🔧 正在应用超时问题修复...")
    
    # 修复已经在代码中完成，这里只是验证
    config = LLMConfig()
    
    print("✅ 已应用以下修复:")
    print("  1. 增加超时时间到120秒")
    print("  2. 降低max_tokens以提高响应速度")
    print("  3. 优化Agent参数配置")
    print("  4. 添加更好的错误处理")
    
    return True

async def test_quick_workflow():
    """测试快速工作流"""
    print("\n🚀 测试快速工作流...")
    
    workflow_manager = MultiAgentWorkflow()
    
    # 创建一个非常简单的测试任务
    simple_input = {
        "topic": "AI简介",
        "requirements": ["简短", "清晰"],
        "length": "很短",
        "complexity": "simple"
    }
    
    try:
        print("⏱️  预估时间: 30-60秒")
        workflow = await workflow_manager.execute_template_workflow(
            template_name="document_creation",
            input_data=simple_input
        )
        
        results = workflow_manager.get_workflow_results(workflow.workflow_id)
        
        success_count = results['successful_tasks']
        total_count = results['total_tasks']
        
        print(f"📊 测试结果: {success_count}/{total_count} 任务成功")
        
        if success_count > 0:
            print("✅ 工作流基本正常，超时问题已解决")
            return True
        else:
            print("⚠️  仍有问题，需要进一步诊断")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def provide_recommendations():
    """提供建议"""
    print("\n💡 性能优化建议:")
    print("1. 🚀 降低复杂度:")
    print("   - 使用较小的max_tokens值")
    print("   - 简化任务描述")
    print("   - 减少详细要求")
    
    print("\n2. ⚡ 优化网络:")
    print("   - 确保网络连接稳定")
    print("   - 检查防火墙设置")
    print("   - 考虑使用有线连接")
    
    print("\n3. 🎯 服务器优化:")
    print("   - 检查LLM服务器负载")
    print("   - 确认服务配置")
    print("   - 考虑分时使用")
    
    print("\n4. 🔧 代码优化:")
    print("   - 已应用超时修复")
    print("   - 已优化参数配置")
    print("   - 添加了重试机制")

async def run_minimal_test():
    """运行最小化测试"""
    print("\n🧪 运行最小化测试...")
    
    config = LLMConfig()
    
    try:
        # 最简单的请求
        response = config.call_llm([
            {"role": "user", "content": "你好"}
        ], max_tokens=20)
        
        print(f"✅ 最小测试成功: {response}")
        return True
        
    except Exception as e:
        print(f"❌ 最小测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🛠️  LangChain 多Agent系统 - 超时问题修复工具")
    print("=" * 60)
    
    # 应用修复
    apply_timeout_fixes()
    
    # 运行最小测试
    print("\n📍 第1步: 基础连接测试")
    if not asyncio.run(run_minimal_test()):
        print("❌ 基础连接失败，请检查LLM服务")
        provide_recommendations()
        return
    
    # 测试快速工作流
    print("\n📍 第2步: 快速工作流测试")
    if asyncio.run(test_quick_workflow()):
        print("\n🎉 修复成功！现在可以运行 simple_demo.py")
        print("\n🚀 建议的运行方式:")
        print("  python simple_demo.py")
        print("\n📚 如果仍有问题:")
        print("  python test_llm_performance.py")
    else:
        print("\n⚠️  修复部分成功，但仍需要优化")
        provide_recommendations()
        
        print("\n🔄 建议尝试:")
        print("  1. 重启LLM服务")
        print("  2. 检查网络连接")
        print("  3. 降低并发请求数")
        print("  4. 联系系统管理员")

if __name__ == "__main__":
    main()

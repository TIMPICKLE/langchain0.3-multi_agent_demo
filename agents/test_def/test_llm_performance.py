"""
LLM连接和性能测试脚本

这个脚本用于测试LLM服务的连接性能，并帮助优化参数设置
"""
import sys
import os
import time
import requests

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.llm_config import LLMConfig

def test_basic_connection():
    """测试基本连接"""
    print("🔗 测试基本连接...")
    
    config = LLMConfig()
    
    try:
        start_time = time.time()
        success = config.test_connection()
        end_time = time.time()
        
        if success:
            print(f"✅ 连接成功 (耗时: {end_time - start_time:.2f}秒)")
            return True
        else:
            print("❌ 连接失败")
            return False
    except Exception as e:
        print(f"❌ 连接异常: {e}")
        return False

def test_simple_request():
    """测试简单请求"""
    print("\n🧪 测试简单请求...")
    
    config = LLMConfig()
    
    try:
        start_time = time.time()
        
        # 构建一个简单的请求
        messages = [
            {"role": "user", "content": "请简短回答：你好"}
        ]
        
        response = config.call_llm(messages, max_tokens=50)
        end_time = time.time()
        
        print(f"✅ 请求成功 (耗时: {end_time - start_time:.2f}秒)")
        print(f"📝 响应内容: {response}")
        return True
        
    except Exception as e:
        end_time = time.time()
        print(f"❌ 请求失败 (耗时: {end_time - start_time:.2f}秒)")
        print(f"错误信息: {e}")
        return False

def test_different_token_limits():
    """测试不同token限制下的性能"""
    print("\n🚀 测试不同token限制下的性能...")
    
    config = LLMConfig()
    token_limits = [50, 100, 200, 400, 800]
    
    test_message = [
        {"role": "user", "content": "请介绍一下Python编程语言的特点"}
    ]
    
    for max_tokens in token_limits:
        try:
            print(f"\n📊 测试 max_tokens={max_tokens}...")
            start_time = time.time()
            
            response = config.call_llm(test_message, max_tokens=max_tokens)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            print(f"✅ 成功 (耗时: {execution_time:.2f}秒)")
            print(f"📝 响应长度: {len(response)}字符")
            
            if execution_time > 30:
                print(f"⚠️  响应时间较长: {execution_time:.2f}秒")
            
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"❌ 失败 (耗时: {execution_time:.2f}秒): {e}")

def test_agent_specific_params():
    """测试Agent专用参数"""
    print("\n🤖 测试Agent专用参数...")
    
    config = LLMConfig()
    agent_types = ["researcher", "planner", "executor", "reviewer"]
    
    test_message = [
        {"role": "user", "content": "请简要说明你的作用"}
    ]
    
    for agent_type in agent_types:
        try:
            print(f"\n🔧 测试 {agent_type} 参数...")
            start_time = time.time()
            
            response = config.call_llm(test_message, agent_type=agent_type)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            print(f"✅ 成功 (耗时: {execution_time:.2f}秒)")
            print(f"📝 响应预览: {response[:100]}...")
            
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"❌ 失败 (耗时: {execution_time:.2f}秒): {e}")

def test_concurrent_requests():
    """测试并发请求"""
    print("\n⚡ 测试并发请求性能...")
    
    import asyncio
    import aiohttp
    
    async def make_request(session, config, request_id):
        """发送单个异步请求"""
        try:
            messages = [
                {"role": "user", "content": f"请简短回答问题{request_id}: 1+1等于多少？"}
            ]
            
            request_data = config.build_request_data(messages, "researcher")
            
            start_time = time.time()
            async with session.post(
                config.get_chat_url(),
                headers=config.get_headers(),
                json=request_data,
                timeout=aiohttp.ClientTimeout(total=60)
            ) as response:
                result = await response.json()
                end_time = time.time()
                
                if response.status == 200:
                    content = result['choices'][0]['message']['content']
                    return {
                        "id": request_id,
                        "success": True,
                        "time": end_time - start_time,
                        "content": content[:50]
                    }
                else:
                    return {
                        "id": request_id,
                        "success": False,
                        "time": end_time - start_time,
                        "error": f"HTTP {response.status}"
                    }
        except Exception as e:
            return {
                "id": request_id,
                "success": False,
                "time": time.time() - start_time,
                "error": str(e)
            }
    
    async def run_concurrent_test():
        config = LLMConfig()
        
        async with aiohttp.ClientSession() as session:
            # 并发3个请求
            tasks = [make_request(session, config, i) for i in range(3)]
            
            start_time = time.time()
            results = await asyncio.gather(*tasks)
            end_time = time.time()
            
            print(f"🏁 并发测试完成 (总耗时: {end_time - start_time:.2f}秒)")
            
            success_count = sum(1 for r in results if r["success"])
            print(f"📊 成功率: {success_count}/{len(results)}")
            
            for result in results:
                status = "✅" if result["success"] else "❌"
                print(f"{status} 请求{result['id']}: {result['time']:.2f}秒")
                if result["success"]:
                    print(f"   响应: {result['content']}...")
                else:
                    print(f"   错误: {result['error']}")
    
    try:
        asyncio.run(run_concurrent_test())
    except Exception as e:
        print(f"❌ 并发测试失败: {e}")

def main():
    """主测试函数"""
    print("🧪 LLM连接和性能测试")
    print("=" * 50)
    
    # 基本连接测试
    if not test_basic_connection():
        print("❌ 基本连接失败，跳过后续测试")
        return
    
    # 简单请求测试
    if not test_simple_request():
        print("❌ 简单请求失败，建议检查服务状态")
        return
    
    # 性能测试
    test_different_token_limits()
    
    # Agent参数测试
    test_agent_specific_params()
    
    # 并发测试（可选）
    try:
        import aiohttp
        test_concurrent_requests()
    except ImportError:
        print("\n⚠️  跳过并发测试 (需要安装 aiohttp: pip install aiohttp)")
    
    print("\n" + "=" * 50)
    print("🎯 测试建议:")
    print("1. 如果所有测试都通过，LLM服务工作正常")
    print("2. 如果响应时间超过30秒，考虑降低max_tokens")
    print("3. 如果经常超时，检查网络连接和服务负载")
    print("4. 建议使用较小的max_tokens值以提高响应速度")

if __name__ == "__main__":
    main()

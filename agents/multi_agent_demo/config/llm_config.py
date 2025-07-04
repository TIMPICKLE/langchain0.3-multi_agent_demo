"""
LLM配置模块

这个模块包含了与大语言模型相关的所有配置信息，
包括API端点、模型参数等。基于test_api.py的配置。
"""
from typing import Dict, Any
import requests
import json

# LLM服务配置 - 基于您的test_api.py文件
LLM_BASE_URL = "http://127.0.0.1:6000/v1"
LLM_MODEL_NAME = "DeepSeek-V3-0324-HSW"

# 默认请求参数
DEFAULT_LLM_PARAMS = {
    "temperature": 0.7,
    "max_tokens": 2000,
    "top_p": 0.9,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
}

# 不同Agent角色的专用参数 - 优化后降低复杂度
AGENT_SPECIFIC_PARAMS = {
    "researcher": {
        "temperature": 0.3,  # 研究员需要更准确的信息
        "max_tokens": 800,   # 降低token数以提高响应速度
    },
    "planner": {
        "temperature": 0.5,  # 规划师需要平衡创造性和逻辑性
        "max_tokens": 1000,  # 降低token数以提高响应速度
    },
    "executor": {
        "temperature": 0.4,  # 执行者需要精确的执行指令
        "max_tokens": 1200,  # 降低token数以提高响应速度
    },
    "reviewer": {
        "temperature": 0.2,  # 审查员需要严格和准确
        "max_tokens": 600,   # 降低token数以提高响应速度
    }
}

class LLMConfig:
    """LLM配置类，用于管理所有LLM相关的配置"""
    
    def __init__(self):
        self.base_url = LLM_BASE_URL
        self.model_name = LLM_MODEL_NAME
        self.default_params = DEFAULT_LLM_PARAMS.copy()
        
    def get_chat_url(self) -> str:
        """获取聊天API的完整URL"""
        return f"{self.base_url}/chat/completions"
    
    def get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Content-Type": "application/json"
        }
    
    def get_params_for_agent(self, agent_type: str) -> Dict[str, Any]:
        """
        根据Agent类型获取专用参数
        
        Args:
            agent_type: Agent类型 ('researcher', 'planner', 'executor', 'reviewer')
            
        Returns:
            包含该Agent专用参数的字典
        """
        params = self.default_params.copy()
        if agent_type in AGENT_SPECIFIC_PARAMS:
            params.update(AGENT_SPECIFIC_PARAMS[agent_type])
        return params
    
    def build_request_data(self, messages: list, agent_type: str = None) -> Dict[str, Any]:
        """
        构建API请求数据
        
        Args:
            messages: 消息列表
            agent_type: Agent类型，用于获取专用参数
            
        Returns:
            完整的请求数据字典
        """
        params = self.get_params_for_agent(agent_type) if agent_type else self.default_params
        
        return {
            "model": self.model_name,
            "messages": messages,
            **params
        }
    
    def test_connection(self) -> bool:
        """
        测试LLM连接是否正常
        
        Returns:
            连接成功返回True，否则返回False
        """
        try:
            test_data = self.build_request_data([
                {"role": "user", "content": "Hello, this is a connection test."}
            ])
            
            response = requests.post(
                self.get_chat_url(),
                headers=self.get_headers(),
                json=test_data,
                timeout=120  # 增加到120秒超时
            )
            
            return response.status_code == 200
        except Exception as e:
            print(f"连接测试失败: {e}")
            return False
    
    def call_llm(self, messages: list, agent_type: str = None, **kwargs) -> str:
        """
        调用LLM服务
        
        Args:
            messages: 消息列表
            agent_type: Agent类型
            **kwargs: 额外参数
            
        Returns:
            LLM的响应文本
        """
        try:
            request_data = self.build_request_data(messages, agent_type)
            
            # 合并额外参数
            request_data.update(kwargs)
            
            response = requests.post(
                self.get_chat_url(),
                headers=self.get_headers(),
                json=request_data,
                timeout=120  # 统一设置为120秒超时
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                raise Exception(f"LLM服务响应错误: {response.status_code}, {response.text}")
                
        except requests.exceptions.Timeout:
            raise Exception("LLM服务响应超时，请稍后重试")
        except requests.exceptions.ConnectionError:
            raise Exception("无法连接到LLM服务，请检查网络和服务状态")
        except Exception as e:
            raise Exception(f"LLM调用失败: {str(e)}")

# 全局配置实例
llm_config = LLMConfig()

# 便捷函数
def get_llm_config() -> LLMConfig:
    """获取全局LLM配置实例"""
    return llm_config

def test_llm_connection() -> bool:
    """测试LLM连接"""
    return llm_config.test_connection()

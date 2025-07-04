"""
配置模块初始化文件
"""
from .llm_config import llm_config, get_llm_config, test_llm_connection

__all__ = ['llm_config', 'get_llm_config', 'test_llm_connection']

"""
交互式演示 - LangChain 0.3 多Agent协作

这个演示提供了一个交互式的命令行界面，让用户可以：
1. 自由选择工作流模板
2. 自定义输入参数
3. 实时查看执行过程
4. 探索Agent能力
5. 自定义工作流

适合希望深度探索系统功能的开发者。
"""
import asyncio
import sys
import os
import json
import time
from typing import Dict, Any, List, Optional

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflows import MultiAgentWorkflow
from config import test_llm_connection

class InteractiveDemo:
    """交互式演示类"""
    
    def __init__(self):
        self.workflow_manager = None
        self.running = True
        self.current_workflows = {}
        
    async def initialize(self):
        """初始化系统"""
        print("🔧 正在初始化多Agent工作流系统...")
        self.workflow_manager = MultiAgentWorkflow()
        print("✅ 系统初始化完成")
    
    def print_header(self, title: str):
        """打印标题"""
        print("\n" + "="*60)
        print(f"  {title}")
        print("="*60)
    
    def print_menu(self, title: str, options: List[str]):
        """打印菜单"""
        print(f"\n📋 {title}")
        print("-" * 40)
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        print("  0. 返回上级菜单")
    
    def get_user_input(self, prompt: str, input_type: type = str, default: Any = None):
        """获取用户输入"""
        while True:
            try:
                user_input = input(f"{prompt}").strip()
                
                if not user_input and default is not None:
                    return default
                
                if input_type == int:
                    return int(user_input)
                elif input_type == float:
                    return float(user_input)
                elif input_type == bool:
                    return user_input.lower() in ['y', 'yes', 'true', '1']
                else:
                    return user_input
                    
            except ValueError:
                print(f"❌ 请输入有效的{input_type.__name__}类型值")
            except KeyboardInterrupt:
                print("\n👋 操作被用户取消")
                return None
    
    async def main_menu(self):
        """主菜单"""
        while self.running:
            self.print_header("🎯 LangChain 0.3 多Agent协作系统 - 交互式演示")
            
            options = [
                "运行预定义工作流",
                "创建自定义工作流", 
                "探索Agent能力",
                "查看系统状态",
                "管理工作流",
                "性能测试",
                "帮助和文档",
                "退出系统"
            ]
            
            self.print_menu("主菜单", options)
            
            choice = self.get_user_input("请选择操作 (0-8): ", int)
            
            if choice is None:  # 用户取消
                break
            elif choice == 0:
                print("👋 感谢使用多Agent协作系统！")
                self.running = False
            elif choice == 1:
                await self.run_predefined_workflow_menu()
            elif choice == 2:
                await self.create_custom_workflow_menu()
            elif choice == 3:
                await self.explore_agent_capabilities_menu()
            elif choice == 4:
                await self.view_system_status()
            elif choice == 5:
                await self.manage_workflows_menu()
            elif choice == 6:
                await self.performance_test_menu()
            elif choice == 7:
                self.show_help_and_docs()
            elif choice == 8:
                print("👋 感谢使用多Agent协作系统！")
                self.running = False
            else:
                print("❌ 无效的选择，请重新输入")
    
    async def run_predefined_workflow_menu(self):
        """预定义工作流菜单"""
        self.print_header("📋 预定义工作流")
        
        # 获取可用模板
        templates = self.workflow_manager.get_available_templates()
        template_descriptions = {
            name: self.workflow_manager.get_template_description(name)
            for name in templates
        }
        
        # 显示模板选项
        print("🎯 可用的工作流模板:")
        for i, template_name in enumerate(templates, 1):
            desc = template_descriptions[template_name]
            print(f"\n{i}. {desc['name']}")
            print(f"   📝 {desc['description']}")
            print(f"   🤖 参与Agent: {', '.join(desc['agents'])}")
            print(f"   🔄 执行阶段: {' → '.join(desc['stages'])}")
        
        choice = self.get_user_input(f"\n请选择工作流模板 (1-{len(templates)}): ", int)
        
        if choice and 1 <= choice <= len(templates):
            template_name = templates[choice - 1]
            await self.run_selected_template(template_name, template_descriptions[template_name])
    
    async def run_selected_template(self, template_name: str, template_info: Dict[str, Any]):
        """运行选中的模板"""
        self.print_header(f"🚀 {template_info['name']}")
        
        print(f"📝 描述: {template_info['description']}")
        print(f"📋 必需输入: {', '.join(template_info['input_required'])}")
        
        # 收集输入参数
        input_data = {}
        
        if "topic" in template_info['input_required']:
            topic = self.get_user_input("请输入主题: ")
            if topic:
                input_data["topic"] = topic
            else:
                print("❌ 主题是必需的")
                return
        
        if "project_name" in template_info['input_required']:
            project_name = self.get_user_input("请输入项目名称: ")
            if project_name:
                input_data["project_name"] = project_name
            else:
                print("❌ 项目名称是必需的")
                return
        
        if "objectives" in template_info['input_required']:
            print("请输入项目目标 (每行一个，空行结束):")
            objectives = []
            while True:
                objective = self.get_user_input("目标: ")
                if not objective:
                    break
                objectives.append(objective)
            input_data["objectives"] = objectives
        
        if "problem" in template_info['input_required']:
            problem = self.get_user_input("请描述要解决的问题: ")
            if problem:
                input_data["problem"] = problem
            else:
                print("❌ 问题描述是必需的")
                return
        
        if "requirements" in template_info['input_required']:
            print("请输入需求 (每行一个，空行结束):")
            requirements = []
            while True:
                requirement = self.get_user_input("需求: ")
                if not requirement:
                    break
                requirements.append(requirement)
            input_data["requirements"] = requirements
        
        # 其他可选输入
        more_params = self.get_user_input("是否要设置更多参数? (y/n): ", bool, False)
        if more_params:
            input_data.update(await self.collect_additional_params(template_name))
        
        # 确认执行
        print(f"\n📊 即将执行工作流:")
        print(f"   模板: {template_info['name']}")
        print(f"   输入参数: {json.dumps(input_data, ensure_ascii=False, indent=2)}")
        
        confirm = self.get_user_input("确认执行? (y/n): ", bool, True)
        if not confirm:
            print("❌ 执行已取消")
            return
        
        # 执行工作流
        print(f"\n🚀 开始执行工作流: {template_info['name']}")
        start_time = time.time()
        
        try:
            workflow = await self.workflow_manager.execute_template_workflow(
                template_name=template_name,
                input_data=input_data
            )
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # 保存到当前工作流
            self.current_workflows[workflow.workflow_id] = {
                "workflow": workflow,
                "template_name": template_name,
                "execution_time": execution_time
            }
            
            print(f"✅ 工作流执行完成！耗时: {execution_time:.2f}秒")
            
            # 显示结果
            await self.show_workflow_results(workflow.workflow_id)
            
        except Exception as e:
            print(f"❌ 工作流执行失败: {str(e)}")
    
    async def collect_additional_params(self, template_name: str) -> Dict[str, Any]:
        """收集额外参数"""
        params = {}
        
        if template_name in ["project_planning", "quality_improvement"]:
            constraints = {}
            print("项目约束条件:")
            
            budget = self.get_user_input("预算 (可选): ")
            if budget:
                constraints["budget"] = budget
            
            timeline = self.get_user_input("时间线 (可选): ")
            if timeline:
                constraints["timeline"] = timeline
            
            team_size = self.get_user_input("团队规模 (可选): ")
            if team_size:
                constraints["team_size"] = team_size
            
            if constraints:
                params["constraints"] = constraints
        
        if template_name == "research_analysis":
            scope = self.get_user_input("研究范围 (基础/标准/深入): ", default="标准")
            params["scope"] = scope
            
            print("重点领域 (每行一个，空行结束):")
            focus_areas = []
            while True:
                area = self.get_user_input("领域: ")
                if not area:
                    break
                focus_areas.append(area)
            if focus_areas:
                params["focus_areas"] = focus_areas
        
        return params
    
    async def create_custom_workflow_menu(self):
        """创建自定义工作流菜单"""
        self.print_header("🛠️ 创建自定义工作流")
        
        workflow_name = self.get_user_input("请输入自定义工作流名称: ")
        if not workflow_name:
            print("❌ 工作流名称是必需的")
            return
        
        print(f"\n🎯 创建工作流: {workflow_name}")
        print("现在请定义工作流中的任务...")
        
        # 获取可用Agent
        agents = list(self.workflow_manager.coordinator.agents.keys())
        agent_info = {
            agent_id: self.workflow_manager.coordinator.agents[agent_id]
            for agent_id in agents
        }
        
        print(f"\n🤖 可用的Agent:")
        for i, agent_id in enumerate(agents, 1):
            agent = agent_info[agent_id]
            print(f"   {i}. {agent.name} ({agent_id}) - {agent.description}")
        
        tasks = []
        task_counter = 1
        
        while True:
            print(f"\n--- 定义第 {task_counter} 个任务 ---")
            
            # 任务基本信息
            task_id = self.get_user_input(f"任务ID (默认: task_{task_counter}): ", default=f"task_{task_counter}")
            
            # 选择Agent
            agent_choice = self.get_user_input(f"选择执行Agent (1-{len(agents)}): ", int)
            if not agent_choice or not (1 <= agent_choice <= len(agents)):
                print("❌ 无效的Agent选择")
                continue
            
            agent_id = agents[agent_choice - 1]
            agent = agent_info[agent_id]
            
            # 获取Agent支持的任务类型
            if hasattr(agent, 'get_research_capabilities'):
                capabilities = agent.get_research_capabilities()
            elif hasattr(agent, 'get_planning_capabilities'):
                capabilities = agent.get_planning_capabilities()
            elif hasattr(agent, 'get_execution_capabilities'):
                capabilities = agent.get_execution_capabilities()
            elif hasattr(agent, 'get_review_capabilities'):
                capabilities = agent.get_review_capabilities()
            else:
                capabilities = {"supported_tasks": ["general_task"]}
            
            supported_tasks = capabilities.get('supported_tasks', ['general_task'])
            
            print(f"\n📋 {agent.name} 支持的任务类型:")
            for i, task_type in enumerate(supported_tasks, 1):
                print(f"   {i}. {task_type}")
            
            task_type_choice = self.get_user_input(f"选择任务类型 (1-{len(supported_tasks)}): ", int)
            if not task_type_choice or not (1 <= task_type_choice <= len(supported_tasks)):
                print("❌ 无效的任务类型选择")
                continue
            
            task_type = supported_tasks[task_type_choice - 1]
            
            # 任务数据
            print("\n请输入任务数据 (JSON格式, 或按回车跳过):")
            task_data_str = self.get_user_input("任务数据: ", default="{}")
            try:
                task_data = json.loads(task_data_str)
            except json.JSONDecodeError:
                print("❌ 无效的JSON格式，使用空数据")
                task_data = {}
            
            # 依赖关系
            if tasks:
                print(f"\n已定义的任务: {', '.join([t['id'] for t in tasks])}")
                dependencies_str = self.get_user_input("依赖的任务ID (逗号分隔, 可选): ", default="")
                dependencies = [dep.strip() for dep in dependencies_str.split(",") if dep.strip()]
            else:
                dependencies = []
            
            # 优先级
            priority = self.get_user_input("任务优先级 (1-10, 默认5): ", int, 5)
            
            # 创建任务定义
            task_def = {
                "id": task_id,
                "type": task_type,
                "agent_id": agent_id,
                "data": task_data,
                "dependencies": dependencies,
                "priority": priority
            }
            
            tasks.append(task_def)
            
            print(f"✅ 任务 {task_id} 已添加")
            
            # 继续添加任务
            continue_adding = self.get_user_input("继续添加任务? (y/n): ", bool, False)
            if not continue_adding:
                break
            
            task_counter += 1
        
        if not tasks:
            print("❌ 没有定义任务，无法创建工作流")
            return
        
        # 显示工作流总结
        print(f"\n📊 自定义工作流总结:")
        print(f"   名称: {workflow_name}")
        print(f"   任务数: {len(tasks)}")
        
        for task in tasks:
            agent_name = agent_info[task['agent_id']].name
            deps_str = f" (依赖: {', '.join(task['dependencies'])})" if task['dependencies'] else ""
            print(f"   - {task['id']}: {task['type']} -> {agent_name}{deps_str}")
        
        # 确认创建
        confirm = self.get_user_input("确认创建并执行工作流? (y/n): ", bool, True)
        if not confirm:
            print("❌ 工作流创建已取消")
            return
        
        # 创建并执行工作流
        try:
            workflow = await self.workflow_manager.create_custom_workflow(workflow_name, tasks)
            
            print(f"✅ 自定义工作流已创建: {workflow_name}")
            print("🚀 开始执行...")
            
            start_time = time.time()
            result_workflow = await self.workflow_manager.coordinator.execute_workflow(workflow.workflow_id)
            end_time = time.time()
            
            execution_time = end_time - start_time
            
            # 保存结果
            self.current_workflows[workflow.workflow_id] = {
                "workflow": result_workflow,
                "template_name": "custom",
                "execution_time": execution_time
            }
            
            print(f"✅ 自定义工作流执行完成！耗时: {execution_time:.2f}秒")
            
            # 显示结果
            await self.show_workflow_results(workflow.workflow_id)
            
        except Exception as e:
            print(f"❌ 自定义工作流执行失败: {str(e)}")
    
    async def explore_agent_capabilities_menu(self):
        """探索Agent能力菜单"""
        self.print_header("🤖 探索Agent能力")
        
        agents = list(self.workflow_manager.coordinator.agents.keys())
        agent_info = {
            agent_id: self.workflow_manager.coordinator.agents[agent_id]
            for agent_id in agents
        }
        
        print("🤖 可用的Agent:")
        for i, agent_id in enumerate(agents, 1):
            agent = agent_info[agent_id]
            print(f"   {i}. {agent.name} ({agent_id})")
            print(f"      📝 {agent.description}")
            print(f"      📊 状态: {agent.status}")
        
        choice = self.get_user_input(f"\n选择要探索的Agent (1-{len(agents)}): ", int)
        
        if choice and 1 <= choice <= len(agents):
            agent_id = agents[choice - 1]
            await self.explore_single_agent(agent_id, agent_info[agent_id])
    
    async def explore_single_agent(self, agent_id: str, agent):
        """探索单个Agent的能力"""
        self.print_header(f"🔍 探索 {agent.name}")
        
        print(f"📝 描述: {agent.description}")
        print(f"📊 当前状态: {agent.status}")
        
        # 获取能力信息
        if hasattr(agent, 'get_research_capabilities'):
            capabilities = agent.get_research_capabilities()
        elif hasattr(agent, 'get_planning_capabilities'):
            capabilities = agent.get_planning_capabilities()
        elif hasattr(agent, 'get_execution_capabilities'):
            capabilities = agent.get_execution_capabilities()
        elif hasattr(agent, 'get_review_capabilities'):
            capabilities = agent.get_review_capabilities()
        else:
            capabilities = {"supported_tasks": ["general_task"]}
        
        print(f"\n🎯 支持的任务类型:")
        for task_type in capabilities.get('supported_tasks', []):
            print(f"   - {task_type}")
        
        if 'output_formats' in capabilities:
            print(f"\n📄 输出格式:")
            for format_type in capabilities['output_formats']:
                print(f"   - {format_type}")
        
        if 'quality_standards' in capabilities:
            print(f"\n⭐ 质量标准:")
            for standard in capabilities['quality_standards']:
                print(f"   - {standard}")
        
        # 性能统计
        stats = agent.get_performance_stats()
        print(f"\n📊 性能统计:")
        print(f"   总请求数: {stats['total_requests']}")
        print(f"   成功率: {stats['success_rate']}")
        print(f"   平均执行时间: {stats['avg_execution_time']}")
        print(f"   完成任务数: {stats['tasks_completed']}")
        
        # 测试Agent能力
        test_agent = self.get_user_input("\n是否要测试这个Agent? (y/n): ", bool, False)
        if test_agent:
            await self.test_agent_capability(agent_id, agent, capabilities)
    
    async def test_agent_capability(self, agent_id: str, agent, capabilities: Dict[str, Any]):
        """测试Agent能力"""
        print(f"\n🧪 测试 {agent.name} 的能力")
        
        supported_tasks = capabilities.get('supported_tasks', [])
        
        print("选择要测试的任务类型:")
        for i, task_type in enumerate(supported_tasks, 1):
            print(f"   {i}. {task_type}")
        
        choice = self.get_user_input(f"选择任务类型 (1-{len(supported_tasks)}): ", int)
        
        if not choice or not (1 <= choice <= len(supported_tasks)):
            print("❌ 无效的选择")
            return
        
        task_type = supported_tasks[choice - 1]
        
        # 根据任务类型准备测试数据
        test_data = await self.prepare_test_data(task_type)
        
        if not test_data:
            print("❌ 测试数据准备失败")
            return
        
        # 执行测试
        print(f"🚀 执行测试任务: {task_type}")
        
        try:
            start_time = time.time()
            
            task_def = {
                "id": f"test_{task_type}_{int(time.time())}",
                "type": task_type,
                "data": test_data
            }
            
            result = await agent.execute_task(task_def)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            print(f"✅ 测试完成！耗时: {execution_time:.2f}秒")
            print(f"📊 结果状态: {result.status}")
            
            if result.status == "success" and result.result:
                content = result.result.get('content', '')
                if content:
                    preview = content[:300] + "..." if len(content) > 300 else content
                    print(f"📄 结果预览:\n{preview}")
            
            if result.error_message:
                print(f"❌ 错误信息: {result.error_message}")
                
        except Exception as e:
            print(f"❌ 测试执行失败: {str(e)}")
    
    async def prepare_test_data(self, task_type: str) -> Optional[Dict[str, Any]]:
        """准备测试数据"""
        if task_type == "research_topic":
            topic = self.get_user_input("请输入研究主题: ", default="人工智能的发展趋势")
            return {
                "topic": topic,
                "scope": "基础",
                "depth": "入门"
            }
        
        elif task_type == "create_project_plan":
            project_name = self.get_user_input("请输入项目名称: ", default="测试项目")
            return {
                "project_name": project_name,
                "objectives": ["目标1", "目标2"],
                "constraints": {"timeline": "1个月"}
            }
        
        elif task_type == "execute_plan":
            return {
                "plan": "执行测试计划",
                "priority": "正常",
                "deadline": "尽快完成"
            }
        
        elif task_type == "quality_review":
            content = self.get_user_input("请输入要审查的内容: ", default="这是一个测试文档内容")
            return {
                "content": content,
                "standards": ["准确性", "完整性"],
                "scope": "基础审查"
            }
        
        else:
            # 通用测试数据
            description = self.get_user_input(f"请输入{task_type}的测试描述: ", default=f"测试{task_type}功能")
            return {
                "description": description,
                "requirements": ["基本功能测试"],
                "context": {"test": True}
            }
    
    async def view_system_status(self):
        """查看系统状态"""
        self.print_header("📊 系统状态")
        
        # 获取系统总览
        system_overview = self.workflow_manager.get_system_overview()
        coordinator_status = system_overview['coordinator_status']
        
        print(f"🎛️ 协调器状态:")
        print(f"   状态: {coordinator_status['coordinator_status']}")
        print(f"   工作流总数: {coordinator_status['workflows']['total']}")
        print(f"   Agent总数: {coordinator_status['agents']['total']}")
        print(f"   任务成功率: {coordinator_status['tasks']['success_rate']:.1f}%")
        
        print(f"\n🤖 Agent状态:")
        for agent_id, agent_info in system_overview['available_agents'].items():
            stats = agent_info['performance']
            print(f"   {agent_info['name']} ({agent_id}):")
            print(f"     状态: {agent_info['status']}")
            print(f"     成功率: {stats['success_rate']}")
            print(f"     平均执行时间: {stats['avg_execution_time']}")
            print(f"     完成任务: {stats['tasks_completed']}")
        
        print(f"\n📋 工作流模板:")
        for template_name, template_info in system_overview['workflow_templates'].items():
            if 'error' not in template_info:
                print(f"   {template_info['name']}")
                print(f"     描述: {template_info['description']}")
        
        # 当前运行的工作流
        if self.current_workflows:
            print(f"\n🔄 当前会话中的工作流:")
            for workflow_id, workflow_info in self.current_workflows.items():
                workflow = workflow_info['workflow']
                print(f"   {workflow.name} ({workflow_id})")
                print(f"     状态: {workflow.status.value}")
                print(f"     执行时间: {workflow_info['execution_time']:.2f}秒")
    
    async def manage_workflows_menu(self):
        """管理工作流菜单"""
        self.print_header("📋 工作流管理")
        
        if not self.current_workflows:
            print("📝 当前会话中没有工作流")
            return
        
        print("🔄 当前会话中的工作流:")
        workflow_list = list(self.current_workflows.items())
        
        for i, (workflow_id, workflow_info) in enumerate(workflow_list, 1):
            workflow = workflow_info['workflow']
            print(f"   {i}. {workflow.name}")
            print(f"      ID: {workflow_id}")
            print(f"      状态: {workflow.status.value}")
            print(f"      执行时间: {workflow_info['execution_time']:.2f}秒")
        
        choice = self.get_user_input(f"\n选择要查看的工作流 (1-{len(workflow_list)}): ", int)
        
        if choice and 1 <= choice <= len(workflow_list):
            workflow_id, _ = workflow_list[choice - 1]
            await self.show_workflow_results(workflow_id)
    
    async def show_workflow_results(self, workflow_id: str):
        """显示工作流结果"""
        results = self.workflow_manager.get_workflow_results(workflow_id)
        
        self.print_header(f"📊 工作流结果: {results['workflow_name']}")
        
        print(f"📈 执行总结:")
        print(f"   状态: {results['status']}")
        print(f"   进度: {results['progress']:.1f}%")
        print(f"   成功任务: {results['successful_tasks']}/{results['total_tasks']}")
        
        if results['execution_summary']['total_time']:
            print(f"   总执行时间: {results['execution_summary']['total_time']:.2f}秒")
        
        print(f"\n📋 任务详情:")
        for i, task_result in enumerate(results['task_results'], 1):
            print(f"\n{i}. 任务: {task_result['task_id']}")
            print(f"   Agent: {task_result['agent_id']}")
            print(f"   状态: {task_result['status']}")
            print(f"   执行时间: {task_result['execution_time']:.2f}秒")
            
            if task_result['status'] == 'success' and task_result['result']:
                content = task_result['result'].get('content', '')
                if content:
                    preview = content[:200] + "..." if len(content) > 200 else content
                    print(f"   结果预览: {preview}")
            
            if task_result.get('error_message'):
                print(f"   错误: {task_result['error_message']}")
        
        # 选项菜单
        print(f"\n🎯 操作选项:")
        print("   1. 查看完整结果")
        print("   2. 导出结果到文件")
        print("   3. 返回")
        
        option = self.get_user_input("选择操作 (1-3): ", int)
        
        if option == 1:
            await self.show_full_results(results)
        elif option == 2:
            await self.export_results(results)
    
    async def show_full_results(self, results: Dict[str, Any]):
        """显示完整结果"""
        self.print_header("📄 完整结果")
        
        for i, task_result in enumerate(results['task_results'], 1):
            print(f"\n{'='*50}")
            print(f"任务 {i}: {task_result['task_id']}")
            print(f"执行Agent: {task_result['agent_id']}")
            print(f"{'='*50}")
            
            if task_result['status'] == 'success' and task_result['result']:
                content = task_result['result'].get('content', '')
                if content:
                    print(content)
                else:
                    print("(无内容)")
            else:
                print(f"任务状态: {task_result['status']}")
                if task_result.get('error_message'):
                    print(f"错误信息: {task_result['error_message']}")
    
    async def export_results(self, results: Dict[str, Any]):
        """导出结果到文件"""
        filename = self.get_user_input("请输入文件名 (默认: workflow_results.json): ", default="workflow_results.json")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 结果已导出到: {filename}")
            
        except Exception as e:
            print(f"❌ 导出失败: {str(e)}")
    
    async def performance_test_menu(self):
        """性能测试菜单"""
        self.print_header("⚡ 性能测试")
        
        print("🎯 可用的性能测试:")
        print("   1. 单Agent性能测试")
        print("   2. 工作流并发测试")
        print("   3. 系统压力测试")
        
        choice = self.get_user_input("选择测试类型 (1-3): ", int)
        
        if choice == 1:
            await self.single_agent_performance_test()
        elif choice == 2:
            await self.workflow_concurrent_test()
        elif choice == 3:
            await self.system_stress_test()
    
    async def single_agent_performance_test(self):
        """单Agent性能测试"""
        print("\n🔍 单Agent性能测试")
        
        # 选择Agent
        agents = list(self.workflow_manager.coordinator.agents.keys())
        print("选择要测试的Agent:")
        for i, agent_id in enumerate(agents, 1):
            agent = self.workflow_manager.coordinator.agents[agent_id]
            print(f"   {i}. {agent.name}")
        
        choice = self.get_user_input(f"选择Agent (1-{len(agents)}): ", int)
        if not choice or not (1 <= choice <= len(agents)):
            print("❌ 无效选择")
            return
        
        agent_id = agents[choice - 1]
        agent = self.workflow_manager.coordinator.agents[agent_id]
        
        # 测试参数
        test_count = self.get_user_input("测试次数 (默认5): ", int, 5)
        
        print(f"\n🚀 开始测试 {agent.name}，执行 {test_count} 次任务...")
        
        # 执行测试
        results = []
        for i in range(test_count):
            print(f"执行第 {i+1} 次测试...")
            
            start_time = time.time()
            try:
                task_def = {
                    "id": f"perf_test_{i+1}",
                    "type": "research_topic",
                    "data": {
                        "topic": f"测试主题 {i+1}",
                        "scope": "基础",
                        "depth": "入门"
                    }
                }
                
                result = await agent.execute_task(task_def)
                end_time = time.time()
                
                results.append({
                    "success": result.status == "success",
                    "time": end_time - start_time
                })
                
            except Exception as e:
                end_time = time.time()
                results.append({
                    "success": False,
                    "time": end_time - start_time,
                    "error": str(e)
                })
        
        # 统计结果
        successful_tests = sum(1 for r in results if r["success"])
        total_time = sum(r["time"] for r in results)
        avg_time = total_time / len(results)
        
        print(f"\n📊 性能测试结果:")
        print(f"   总测试次数: {test_count}")
        print(f"   成功次数: {successful_tests}")
        print(f"   成功率: {successful_tests/test_count*100:.1f}%")
        print(f"   总耗时: {total_time:.2f}秒")
        print(f"   平均耗时: {avg_time:.2f}秒/次")
        print(f"   最快: {min(r['time'] for r in results):.2f}秒")
        print(f"   最慢: {max(r['time'] for r in results):.2f}秒")
    
    async def workflow_concurrent_test(self):
        """工作流并发测试"""
        print("\n🔄 工作流并发测试")
        
        concurrent_count = self.get_user_input("并发工作流数量 (默认3): ", int, 3)
        
        print(f"🚀 启动 {concurrent_count} 个并发工作流...")
        
        # 创建并发任务
        tasks = []
        for i in range(concurrent_count):
            task_input = {
                "topic": f"并发测试主题 {i+1}",
                "requirements": ["快速完成", "基础质量"]
            }
            
            task = asyncio.create_task(
                self.workflow_manager.execute_template_workflow(
                    "document_creation", task_input
                )
            )
            tasks.append(task)
        
        start_time = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = time.time()
        
        total_time = end_time - start_time
        successful_workflows = sum(1 for r in results if not isinstance(r, Exception))
        
        print(f"\n📊 并发测试结果:")
        print(f"   并发数量: {concurrent_count}")
        print(f"   成功数量: {successful_workflows}")
        print(f"   成功率: {successful_workflows/concurrent_count*100:.1f}%")
        print(f"   总耗时: {total_time:.2f}秒")
        print(f"   平均每个工作流: {total_time/concurrent_count:.2f}秒")
    
    async def system_stress_test(self):
        """系统压力测试"""
        print("\n💪 系统压力测试")
        
        print("⚠️ 警告: 压力测试会产生大量LLM调用，请确认是否继续")
        confirm = self.get_user_input("确认执行压力测试? (y/n): ", bool, False)
        
        if not confirm:
            print("❌ 压力测试已取消")
            return
        
        stress_duration = self.get_user_input("测试持续时间(秒, 默认30): ", int, 30)
        
        print(f"🚀 开始压力测试，持续 {stress_duration} 秒...")
        
        start_time = time.time()
        task_counter = 0
        successful_tasks = 0
        
        while time.time() - start_time < stress_duration:
            try:
                task_counter += 1
                
                # 随机选择Agent和任务类型
                agent_id = "researcher_001"  # 使用研究员进行压力测试
                agent = self.workflow_manager.coordinator.agents[agent_id]
                
                task_def = {
                    "id": f"stress_test_{task_counter}",
                    "type": "research_topic",
                    "data": {
                        "topic": f"压力测试主题 {task_counter}",
                        "scope": "基础",
                        "depth": "入门"
                    }
                }
                
                result = await agent.execute_task(task_def)
                
                if result.status == "success":
                    successful_tasks += 1
                
                print(f"完成任务 {task_counter}, 成功率: {successful_tasks/task_counter*100:.1f}%")
                
            except Exception as e:
                print(f"任务 {task_counter} 失败: {str(e)}")
            
            # 短暂休息避免过载
            await asyncio.sleep(0.1)
        
        end_time = time.time()
        actual_duration = end_time - start_time
        
        print(f"\n📊 压力测试结果:")
        print(f"   测试时长: {actual_duration:.2f}秒")
        print(f"   总任务数: {task_counter}")
        print(f"   成功任务数: {successful_tasks}")
        print(f"   成功率: {successful_tasks/task_counter*100:.1f}%")
        print(f"   任务吞吐量: {task_counter/actual_duration:.2f} 任务/秒")
        print(f"   平均响应时间: {actual_duration/task_counter:.2f}秒/任务")
    
    def show_help_and_docs(self):
        """显示帮助和文档"""
        self.print_header("📚 帮助和文档")
        
        print("🎯 LangChain 0.3 多Agent协作系统使用指南")
        print()
        print("📖 核心概念:")
        print("   • Agent: 智能代理，具有特定的职责和能力")
        print("   • Workflow: 工作流，定义多个Agent的协作流程")
        print("   • Task: 任务，Agent执行的具体工作单元")
        print("   • Coordinator: 协调器，管理Agent和工作流的执行")
        print()
        print("🤖 可用的Agent:")
        print("   • 研究员 (Researcher): 信息收集、分析和整理")
        print("   • 规划师 (Planner): 计划制定、任务分解和资源配置")
        print("   • 执行者 (Executor): 任务执行、问题解决和结果交付")
        print("   • 审查员 (Reviewer): 质量评估、错误检测和改进建议")
        print()
        print("📋 预定义工作流:")
        print("   • 文档撰写: 研究 → 规划 → 执行 → 审查")
        print("   • 项目规划: 需求分析 → 计划制定 → 风险评估 → 审查")
        print("   • 问题解决: 问题分析 → 方案规划 → 实施 → 验证")
        print("   • 质量改进: 现状评估 → 根因分析 → 改进规划 → 实施 → 验证")
        print("   • 研究分析: 数据收集 → 文献综述 → 报告规划 → 撰写 → 评议")
        print()
        print("🔧 系统配置:")
        print("   • LLM服务: DeepSeek-V3-0324-HSW")
        print("   • 服务地址: http://127.0.0.1:6000/v1")
        print("   • 配置文件: config/llm_config.py")
        print()
        print("📁 项目结构:")
        print("   • agents/: Agent实现")
        print("   • workflows/: 工作流管理")
        print("   • config/: 配置文件")
        print("   • examples/: 示例程序")
        print("   • docs/: 详细文档")
        print()
        print("💡 使用建议:")
        print("   1. 从简单的预定义工作流开始")
        print("   2. 理解每个Agent的能力和特点")
        print("   3. 尝试创建自定义工作流")
        print("   4. 利用性能测试优化系统")
        print("   5. 阅读详细文档深入学习")
        print()
        print("🔗 相关文档:")
        print("   • docs/tutorial.md - 详细教程")
        print("   • docs/concepts.md - 核心概念")
        print("   • docs/best_practices.md - 最佳实践")
        print("   • README.md - 项目说明")

async def main():
    """主函数"""
    # 检查LLM连接
    print("🔗 检查LLM服务连接...")
    if not test_llm_connection():
        print("❌ LLM服务连接失败！")
        print("💡 请检查config/llm_config.py中的配置")
        return
    
    print("✅ LLM服务连接正常")
    
    # 创建交互式演示
    demo = InteractiveDemo()
    
    try:
        await demo.initialize()
        await demo.main_menu()
        
    except KeyboardInterrupt:
        print("\n👋 感谢使用LangChain 0.3 多Agent协作系统！")
    except Exception as e:
        print(f"\n❌ 系统错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

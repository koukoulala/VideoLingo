"""
VideoLingo Copilot 运行指南和测试脚本
=====================================

本脚本帮助您：
1. 验证 Copilot 集成是否正常工作
2. 测试翻译功能
3. 确认正在使用 Copilot LLM
4. 提供运行指南
"""

import os
import sys
import logging
from pathlib import Path

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_environment():
    """检查运行环境"""
    print("🔍 检查运行环境...")
    
    # 检查 Python 版本
    python_version = sys.version_info
    print(f"  Python 版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # 检查必要的包
    required_packages = ['requests', 'ruamel.yaml', 'json_repair']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (缺失)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 请安装缺失的包:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_copilot_setup():
    """检查 Copilot 设置"""
    print("\n🔍 检查 Copilot 设置...")
    
    # 检查 token 文件
    if not os.path.exists('access_token.txt'):
        print("  ❌ access_token.txt 文件不存在")
        return False
    
    with open('access_token.txt', 'r') as f:
        token = f.read().strip()
    
    if not token or token == 'your-github-access-token-here':
        print("  ❌ 请在 access_token.txt 中设置您的 GitHub access token")
        return False
    
    if not token.startswith('ghu_') and not token.startswith('ghp_'):
        print("  ❌ GitHub token 格式不正确 (应该以 ghp_ 或 ghu_ 开头)")
        return False
    
    print(f"  ✅ GitHub token: {token[:8]}...")
    return True

def test_copilot_api():
    """测试 Copilot API"""
    print("\n🧪 测试 Copilot API...")
    
    try:
        from core.utils.copilot_api import CopilotAPIClient
        
        # 初始化客户端
        client = CopilotAPIClient()
        print(f"  ✅ Copilot 客户端初始化成功")
        
        # 测试连接
        if client.test_connection():
            print("  ✅ Copilot API 连接测试成功")
            return True, client
        else:
            print("  ❌ Copilot API 连接测试失败")
            return False, None
    
    except Exception as e:
        print(f"  ❌ Copilot API 错误: {e}")
        return False, None

def test_translation():
    """测试翻译功能"""
    print("\n🌍 测试翻译功能...")
    
    try:
        from core.utils.ask_gpt import ask_gpt
        
        # 测试简单翻译
        test_prompt = "请将以下英文翻译成中文：'Hello, how are you today?'"
        print(f"  📝 测试提示: {test_prompt}")
        
        result = ask_gpt(test_prompt, log_title="copilot_test")
        
        if result:
            print(f"  ✅ 翻译结果: {result}")
            return True
        else:
            print("  ❌ 翻译失败")
            return False
    
    except Exception as e:
        print(f"  ❌ 翻译错误: {e}")
        return False

def test_json_mode():
    """测试 JSON 模式"""
    print("\n📋 测试 JSON 响应模式...")
    
    try:
        from core.utils.ask_gpt import ask_gpt
        
        json_prompt = '''请用 JSON 格式回复，包含以下字段：
{
    "original": "Hello world",
    "translation": "中文翻译",
    "model": "使用的模型名称"
}'''
        
        result = ask_gpt(json_prompt, resp_type="json", log_title="json_test")
        
        if isinstance(result, dict) and "translation" in result:
            print(f"  ✅ JSON 模式测试成功: {result}")
            return True
        else:
            print(f"  ❌ JSON 模式失败: {result}")
            return False
    
    except Exception as e:
        print(f"  ❌ JSON 模式错误: {e}")
        return False

def show_usage_guide():
    """显示使用指南"""
    print("\n" + "="*60)
    print("🚀 VideoLingo Copilot 使用指南")
    print("="*60)
    
    print("\n1. 📱 启动 Web 界面 (推荐):")
    print("   python st.py")
    print("   然后在浏览器中打开 http://localhost:8501")
    
    print("\n2. 💻 命令行使用:")
    print("   python main.py")
    
    print("\n3. 🔍 如何确认使用 Copilot LLM:")
    print("   - 检查 config.yaml 中 api.model 是否为 'gpt-4o'")
    print("   - 检查 config.yaml 中 api.base_url 是否为 'https://api.githubcopilot.com'")
    print("   - 运行翻译时，查看日志输出")
    print("   - 检查 output/gpt_log/ 目录下的日志文件")
    
    print("\n4. 📊 监控 Copilot 使用:")
    print("   - 日志文件: output/gpt_log/")
    print("   - 模型信息会显示在翻译过程中")
    print("   - 可以通过 GitHub Copilot 使用统计查看 API 调用")
    
    print("\n5. 🔧 故障排除:")
    print("   - 如果 Copilot 不可用，系统会自动回退到 OpenAI API")
    print("   - 确保 GitHub token 有 Copilot 访问权限")
    print("   - 检查网络连接")

def check_log_files():
    """检查日志文件以确认模型使用"""
    print("\n📁 检查日志文件...")
    
    log_dir = Path('output/gpt_log')
    if log_dir.exists():
        log_files = list(log_dir.glob('*.json'))
        if log_files:
            print(f"  ✅ 找到 {len(log_files)} 个日志文件")
            latest_log = max(log_files, key=os.path.getctime)
            print(f"  📄 最新日志: {latest_log.name}")
            
            # 读取最新日志的前几行
            try:
                import json
                with open(latest_log, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                
                if logs:
                    latest_entry = logs[-1]
                    model = latest_entry.get('model', 'unknown')
                    print(f"  🤖 最后使用的模型: {model}")
                    
                    if model == 'gpt-4o':
                        print("  ✅ 确认正在使用 GPT-4o (Copilot)")
                    else:
                        print(f"  ⚠️  使用的模型: {model} (可能不是 Copilot)")
            except Exception as e:
                print(f"  ❌ 读取日志错误: {e}")
        else:
            print("  ℹ️  尚未有日志文件 (需要先运行翻译)")
    else:
        print("  ℹ️  日志目录不存在 (需要先运行翻译)")

def main():
    """主函数"""
    print("🎯 VideoLingo Copilot 集成测试和运行指南")
    print("="*60)
    
    # 检查是否在正确的目录
    if not os.path.exists('config.yaml'):
        print("❌ 请在 VideoLingo 根目录运行此脚本")
        return
    
    # 运行所有检查
    checks = [
        ("环境检查", check_environment),
        ("Copilot 设置", check_copilot_setup),
        ("API 测试", lambda: test_copilot_api()[0]),
        ("翻译测试", test_translation),
        ("JSON 模式测试", test_json_mode)
    ]
    
    passed = 0
    for name, check_func in checks:
        try:
            if check_func():
                passed += 1
            else:
                break  # 如果基础检查失败，停止后续测试
        except Exception as e:
            print(f"  ❌ {name}失败: {e}")
            break
    
    # 检查日志文件
    check_log_files()
    
    # 显示结果
    print(f"\n📊 测试结果: {passed}/{len(checks)} 项通过")
    
    if passed == len(checks):
        print("🎉 所有测试通过！Copilot 集成工作正常。")
        show_usage_guide()
    elif passed >= 2:
        print("⚠️  基本功能正常，但有些问题需要解决。")
        show_usage_guide()
    else:
        print("❌ 集成有问题，请检查设置。")
        print("\n🔧 建议:")
        print("1. 确保在 access_token.txt 中设置了有效的 GitHub token")
        print("2. 确保 token 有 Copilot 访问权限")
        print("3. 运行: pip install requests ruamel.yaml json-repair")

if __name__ == '__main__':
    main()

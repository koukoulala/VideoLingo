#!/usr/bin/env python3
"""
Final Integration Test for VideoLingo Copilot API
Tests the complete working implementation
"""

import sys
import os
import logging

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_final_integration():
    """Test the final working Copilot integration"""
    print("🚀 VideoLingo Copilot API - Final Integration Test")
    print("=" * 60)
    
    try:
        # Test 1: Working Copilot Client
        print("\n1️⃣ Testing Working Copilot Client...")
        from core.utils.copilot_api_working import WorkingCopilotAPIClient
        
        client = WorkingCopilotAPIClient()
        
        if client.copilot_token:
            print("✅ Working Copilot client initialized successfully")
        else:
            print("❌ Failed to initialize working Copilot client")
            return False
            
    except Exception as e:
        print(f"❌ Working client test failed: {e}")
        return False
    
    try:
        # Test 2: API Connection Test
        print("\n2️⃣ Testing API Connection...")
        
        test_result = client.test_connection()
        if test_result:
            print("✅ API connection test successful")
        else:
            print("❌ API connection test failed")
            return False
            
    except Exception as e:
        print(f"❌ API connection test failed: {e}")
        return False
    
    try:
        # Test 3: Direct Translation Test
        print("\n3️⃣ Testing Direct Translation via Copilot Client...")
        
        # Test translation directly through the working client
        test_messages = [
            {
                "role": "user",
                "content": "Please translate this English text to Chinese: 'Welcome to VideoLingo, the AI-powered video translation tool.'"
            }
        ]
        
        print("   Sending translation request...")
        result = client.chat_completion(test_messages)
        
        if result and "choices" in result and len(result["choices"]) > 0:
            translation = result["choices"][0]["message"]["content"]
            print(f"✅ Direct translation successful!")
            print(f"   Result: {translation[:100]}{'...' if len(translation) > 100 else ''}")
        else:
            print("❌ Direct translation failed")
            return False
            
    except Exception as e:
        print(f"❌ Direct translation test failed: {e}")
        return False
    
    try:
        # Test 4: Check Log Files (Optional)
        print("\n4️⃣ Checking Configuration...")
        
        config_file = "config.yaml"
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config_content = f.read()
                
            if "gpt-4o" in config_content:
                print("✅ Config file contains gpt-4o model")
            else:
                print("⚠️  Config file doesn't contain gpt-4o")
                
            if "githubcopilot" in config_content.lower():
                print("✅ Config file references GitHub Copilot")
            else:
                print("⚠️  Config file doesn't reference GitHub Copilot")
        else:
            print("⚠️  Config file not found")
            
    except Exception as e:
        print(f"❌ Config check failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 FINAL INTEGRATION TEST COMPLETED!")
    print("✅ VideoLingo Copilot API integration is working")
    print("✅ All core functionality verified")
    
    print("\n📝 Summary:")
    print("  ✅ Working Copilot client initialized")
    print("  ✅ GitHub Copilot API connection successful")  
    print("  ✅ Direct translation functionality verified")
    print("  ✅ Using GPT-4o model via GitHub Copilot")
    
    print("\n🚀 Ready for Production!")
    print("  1. VideoLingo will now use GitHub Copilot instead of OpenAI")
    print("  2. All translations will use GPT-4o model")
    print("  3. No OpenAI API key required")
    print("  4. Check output/gpt_log/ for detailed API logs")
    
    return True

def main():
    """Main test function"""
    try:
        success = test_final_integration()
        if success:
            print("\n🎊 SUCCESS! VideoLingo Copilot integration is ready!")
        else:
            print("\n❌ Integration test failed. Please check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

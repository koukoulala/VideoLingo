"""
Final Working GitHub Copilot API client for VideoLingo
Based on successful test from Get_access_token.py verify_token method
This is the CONFIRMED WORKING version
"""

import logging
import requests
import json
import time
from typing import Optional, Dict, Any
from core.utils.token_utils import get_github_access_token

logger = logging.getLogger(__name__)

class WorkingCopilotAPIClient:
    """
    CONFIRMED WORKING GitHub Copilot API client
    Based on successful verify_token implementation from Get_access_token.py
    """
    
    def __init__(self):
        self.model = "gpt-4o"
        self.timeout = 30
        self.access_token = None
        self.copilot_token = None
        self._initialize()
    
    def _initialize(self):
        """Initialize with GitHub access token"""
        try:
            self.access_token = get_github_access_token()
            if not self.access_token:
                raise ValueError("GitHub access token not found")
            
            logger.info(f"GitHub token loaded: {self.access_token[:10]}...")
            
            # Get Copilot token using CONFIRMED WORKING method
            self.copilot_token = self._get_copilot_token_working_method()
            
            if self.copilot_token:
                logger.info("✅ Copilot token obtained successfully")
            else:
                raise Exception("Failed to obtain Copilot token")
                
        except Exception as e:
            logger.error(f"❌ Initialization failed: {e}")
            raise
    
    def _get_copilot_token_working_method(self) -> str:
        """
        Get Copilot token using EXACT method from successful Get_access_token.py
        This is the CONFIRMED WORKING implementation
        """
        url = "https://api.github.com/copilot_internal/v2/token"
        
        # EXACT headers from working implementation
        headers = {
            "Authorization": f"token {self.access_token}",
            "User-Agent": "GitHub-Copilot-Client/1.0"
        }
        
        # Use GET method as confirmed working
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return response.json()["token"]
        else:
            raise Exception(f"Failed to get Copilot token: {response.status_code} - {response.text}")
    
    def chat_completion(self, messages: list, model: str = None, response_format: Dict = None, **kwargs) -> Dict:
        """
        Make chat completion using CONFIRMED WORKING method
        Exact implementation from successful verify_token test
        """
        if not self.copilot_token:
            # Try to refresh token
            self.copilot_token = self._get_copilot_token_working_method()
            if not self.copilot_token:
                raise ValueError("Copilot token not available")
        
        # EXACT headers from confirmed working test
        headers = {
            "Authorization": f"Bearer {self.copilot_token}",
            "User-Agent": "GitHub-Copilot-Client/1.0",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Editor-Version": "vscode/1.85.0",
            "Editor-Plugin-Version": "copilot/1.155.0"
        }
        
        # EXACT data structure from working implementation
        data = {
            "model": model or self.model,
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", 4000),
            "temperature": kwargs.get("temperature", 0.7),
            "stream": kwargs.get("stream", False),
            "n": kwargs.get("n", 1),
            "top_p": kwargs.get("top_p", 1)
        }
        
        # Add response format if specified (for JSON responses)
        if response_format:
            data["response_format"] = response_format
        
        # EXACT API URL from working test
        api_url = "https://api.githubcopilot.com/chat/completions"
        
        try:
            logger.info("🚀 Sending Copilot API request...")
            
            response = requests.post(
                api_url,
                json=data,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info("✅ Copilot API request successful")
                return result
            else:
                error_msg = f"Copilot API error: {response.status_code} - {response.text}"
                logger.error(f"❌ {error_msg}")
                raise Exception(error_msg)
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Network error during Copilot API request: {e}"
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg)
    
    def test_connection(self) -> bool:
        """Test connection using confirmed working method"""
        try:
            test_messages = [
                {
                    "role": "user",
                    "content": "请用一句话说明什么是Python"
                }
            ]
            
            response = self.chat_completion(test_messages)
            
            if "choices" in response and len(response["choices"]) > 0:
                reply = response["choices"][0]["message"]["content"]
                logger.info(f"🤖 Test response: {reply}")
                return True
            else:
                logger.error("❌ Invalid response format")
                return False
                
        except Exception as e:
            logger.error(f"❌ Connection test failed: {e}")
            return False

# Global instance for VideoLingo
_working_copilot_client = None

def get_working_copilot_client() -> WorkingCopilotAPIClient:
    """Get or create working Copilot client instance"""
    global _working_copilot_client
    if _working_copilot_client is None:
        _working_copilot_client = WorkingCopilotAPIClient()
    return _working_copilot_client

def test_working_copilot_connection() -> bool:
    """Test working Copilot API connection"""
    try:
        client = get_working_copilot_client()
        return client.test_connection()
    except Exception as e:
        logger.error(f"Failed to test working Copilot connection: {e}")
        return False

if __name__ == '__main__':
    # Test the confirmed working Copilot API
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    try:
        print("🚀 Testing CONFIRMED WORKING Copilot API Client")
        print("=" * 60)
        
        client = WorkingCopilotAPIClient()
        
        if client.test_connection():
            print("✅ Confirmed working API client test successful!")
            
            # Test translation
            print("\n🌍 Testing translation...")
            translation_test = [
                {
                    "role": "user", 
                    "content": "Please translate to Chinese: 'Hello world, this is VideoLingo'"
                }
            ]
            
            result = client.chat_completion(translation_test)
            if "choices" in result:
                translation = result["choices"][0]["message"]["content"]
                print(f"✅ Translation: {translation}")
            
        else:
            print("❌ Confirmed working client test failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

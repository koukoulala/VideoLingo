"""
Access token utilities for VideoLingo
"""

import os
from pathlib import Path

def get_github_access_token():
    """
    Get GitHub access token from various sources
    
    Returns:
        GitHub access token or None
    """
    # Try to get token from VideoLingo config first
    token_file_paths = [
        "access_token.txt",
        "core/access_token.txt", 
        "../ai-localization-demo/AudioTranslation/tokens/access_token.txt",
        "../ai-localization-demo/ai-localization-demo-backend/test/access_token.txt"
    ]
    
    for token_path in token_file_paths:
        if os.path.exists(token_path):
            try:
                with open(token_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    # Skip comments and empty lines
                    for line in content.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('#') and (line.startswith('ghp_') or line.startswith('ghu_')):
                            return line
            except Exception as e:
                print(f"Warning: Failed to read token from {token_path}: {e}")
    
    # Try environment variable
    token = os.getenv('GITHUB_ACCESS_TOKEN')
    if token and (token.startswith('ghp_') or token.startswith('ghu_')):
        return token
    
    print("GitHub access token not found. Please:")
    print("1. Set GITHUB_ACCESS_TOKEN environment variable, or")
    print("2. Create access_token.txt file in VideoLingo root directory with your GitHub token")
    return None

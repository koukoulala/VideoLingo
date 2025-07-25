import os
import json
from threading import Lock
import json_repair
from core.utils.config_utils import load_key
from core.utils.copilot_api_working import get_working_copilot_client
from rich import print as rprint
from core.utils.decorator import except_handler

# ------------
# cache gpt response
# ------------

LOCK = Lock()
GPT_LOG_FOLDER = 'output/gpt_log'

def _save_cache(model, prompt, resp_content, resp_type, resp, message=None, log_title="default"):
    with LOCK:
        logs = []
        file = os.path.join(GPT_LOG_FOLDER, f"{log_title}.json")
        os.makedirs(os.path.dirname(file), exist_ok=True)
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        logs.append({"model": model, "prompt": prompt, "resp_content": resp_content, "resp_type": resp_type, "resp": resp, "message": message})
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)

def _load_cache(prompt, resp_type, log_title):
    with LOCK:
        file = os.path.join(GPT_LOG_FOLDER, f"{log_title}.json")
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                for item in json.load(f):
                    if item["prompt"] == prompt and item["resp_type"] == resp_type:
                        return item["resp"]
        return False

# ------------
# ask gpt once
# ------------

@except_handler("GPT request failed", retry=5)
def ask_gpt(prompt, resp_type=None, valid_def=None, log_title="default"):
    # Check if we have Copilot access token, fallback to original OpenAI if not
    try:
        copilot_client = get_working_copilot_client()
        use_copilot = True
    except Exception as e:
        rprint(f"[yellow]Warning: Failed to initialize Copilot client: {e}[/yellow]")
        rprint("[yellow]Falling back to OpenAI API[/yellow]")
        use_copilot = False
    
    # check cache
    cached = _load_cache(prompt, resp_type, log_title)
    if cached:
        rprint("use cache response")
        return cached

    if use_copilot:
        # Use Copilot API
        model = "gpt-4o"  # Force use GPT-4o for Copilot
        
        messages = [{"role": "user", "content": prompt}]
        response_format = {"type": "json_object"} if resp_type == "json" else None

        params = dict(
            messages=messages,
            model=model,
            response_format=response_format,
            temperature=0.7,
            timeout=300
        )
        
        resp_raw = copilot_client.chat_completion(**params)
    else:
        # Fallback to original OpenAI API
        if not load_key("api.key"):
            raise ValueError("API key is not set")
            
        from openai import OpenAI
        
        model = load_key("api.model")
        base_url = load_key("api.base_url")
        if 'ark' in base_url:
            base_url = "https://ark.cn-beijing.volces.com/api/v3" # huoshan base url
        elif 'v1' not in base_url:
            base_url = base_url.strip('/') + '/v1'
        client = OpenAI(api_key=load_key("api.key"), base_url=base_url)
        response_format = {"type": "json_object"} if resp_type == "json" and load_key("api.llm_support_json") else None

        messages = [{"role": "user", "content": prompt}]

        params = dict(
            model=model,
            messages=messages,
            response_format=response_format,
            timeout=300
        )
        resp_raw = client.chat.completions.create(**params)

    # process and return full result
    # Handle different response formats (OpenAI vs Copilot API)
    if hasattr(resp_raw, 'choices') and resp_raw.choices:
        # Standard OpenAI API response format
        resp_content = resp_raw.choices[0].message.content
    elif isinstance(resp_raw, dict) and 'choices' in resp_raw:
        # Dict format (from Copilot API or other APIs)
        resp_content = resp_raw['choices'][0]['message']['content']
    else:
        # Fallback for unexpected response format
        rprint(f"[red]Unexpected response format: {type(resp_raw)}, content: {resp_raw}[/red]")
        raise ValueError(f"Unexpected API response format: {type(resp_raw)}")
    
    if resp_type == "json":
        resp = json_repair.loads(resp_content)
    else:
        resp = resp_content
    
    # check if the response format is valid
    if valid_def:
        valid_resp = valid_def(resp)
        if valid_resp['status'] != 'success':
            _save_cache(model, prompt, resp_content, resp_type, resp, log_title="error", message=valid_resp['message'])
            raise ValueError(f"❎ API response error: {valid_resp['message']}")

    _save_cache(model, prompt, resp_content, resp_type, resp, log_title=log_title)
    return resp


if __name__ == '__main__':
    from rich import print as rprint
    
    result = ask_gpt("""test respond ```json\n{\"code\": 200, \"message\": \"success\"}\n```""", resp_type="json")
    rprint(f"Test json output result: {result}")

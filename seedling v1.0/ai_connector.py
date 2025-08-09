# MIT License - Copyright (c) 2025 Viktor Kirschner
import os
from openai import OpenAI  # This is Moonshot's client
import httpx

# The client will be initialized by the main script.
client = None

def initialize_client(api_key: str):
    """
    Initializes the Moonshot client with a provided API key, verifies it,
    and automatically handles system proxy settings.
    Returns True on success, False on failure.
    """
    global client
    if not api_key or not api_key.strip():
        print("\n[ERROR] API key is missing. Cannot initialize Moonshot client.")
        client = None
        return False

    try:
        # Check for system proxy settings
        proxy_url = os.environ.get('https_proxy') or os.environ.get('HTTPS_PROXY')

        # Create an httpx client. If a proxy is found, configure the client to use it.
        if proxy_url:
            print(f"[INFO] Proxy detected at {proxy_url}. Attempting to connect through it.")
            http_client = httpx.Client(proxies=proxy_url)
        else:
            http_client = httpx.Client()

        # Initialize the Moonshot client using base_url
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.moonshot.ai/v1",
            http_client=http_client
        )

        # Sanity check: list models (Moonshot supports it)
        client.models.list()

        print("[SUCCESS] Moonshot client initialized and key verified.")
        return True

    except Exception as e:
        print(f"\n[ERROR] Failed to initialize Moonshot client: {e}")
        client = None
        return False

def get_ai_response_with_history(system_prompt: str, history: list, model_name: str = "kimi-k2-turbo-preview") -> str:
    """
    Sends the full conversation history to the Moonshot model and gets a response.
    """
    if not client:
        return "[CMD_START]append_log \"[ERROR] Moonshot client not initialized. Cannot get AI response.\"[CMD_END]"

    messages = [{"role": "system", "content": system_prompt}] + history

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.7,
            max_tokens=8192
        )
        ai_response_text = response.choices[0].message.content
        return ai_response_text

    except Exception as e:
        error_message = f"[ERROR] An unexpected error occurred during API call: {e}"
        print(error_message)
        return f"An unexpected error occurred. I will log it. [CMD_START]append_log \"{error_message}\"[CMD_END]"

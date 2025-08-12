# ai_connector.py
# MIT License
#
# OpenAI connector for Seedling/CLI agent
# - GPT-5 / GPT-4.1 param handling
# - Extended timeout for long generations (300s)
# - Auto-retry on timeout or rate-limit
# - Graceful empty-response handling
# - Detailed logging

import os
import re
import time
import httpx
from typing import List, Dict, Any, Optional
from openai import OpenAI

client: Optional[OpenAI] = None


def _make_httpx_client(timeout_seconds=300):
    """Create httpx.Client with proxy support and extended timeout."""
    proxy = (
        os.environ.get("https_proxy")
        or os.environ.get("HTTPS_PROXY")
        or os.environ.get("http_proxy")
        or os.environ.get("HTTP_PROXY")
    )
    if proxy:
        print(f"[INFO] Proxy detected: {proxy}")
        return httpx.Client(proxies=proxy, timeout=timeout_seconds)
    return httpx.Client(timeout=timeout_seconds)


def initialize_client(api_key: str) -> bool:
    """Initialize OpenAI client with provided key."""
    global client

    if not api_key.strip():
        print("[ERROR] API key is missing.")
        return False

    try:
        http_client = _make_httpx_client()
        base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

        client = OpenAI(api_key=api_key, base_url=base_url, http_client=http_client)
        client.models.list()  # Sanity check
        print("[SUCCESS] OpenAI client initialized and key verified.")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to initialize OpenAI client: {e}")
        client = None
        return False


def _is_strict_model(model: str) -> bool:
    """Detect GPT-5 / GPT-4.1 style models."""
    return model.startswith(("gpt-5", "gpt-4.1"))


def _sanitize_history(history: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Ensure history is in a valid format."""
    allowed = {"user", "assistant", "system"}
    sanitized = []
    for m in history:
        role = str(m.get("role", "user")).lower()
        content = m.get("content", "")
        if role not in allowed:
            continue
        sanitized.append({"role": role, "content": str(content or "")})
    return sanitized


def get_ai_response_with_history(system_prompt: str, history: list, model_name: str = None) -> str:
    """Send conversation to OpenAI and return the assistant's reply."""
    if not client:
        return "[ERROR] OpenAI client not initialized."

    model = model_name or os.environ.get("OPENAI_CHAT_MODEL", "gpt-5")
    messages = [{"role": "system", "content": system_prompt}]
    messages += _sanitize_history(history)

    params: Dict[str, Any] = {"model": model, "messages": messages}

    if _is_strict_model(model):
        params["max_completion_tokens"] = 8192
    else:
        params["max_tokens"] = 8192
        try:
            params["temperature"] = float(os.environ.get("OPENAI_TEMPERATURE", "0.7"))
        except ValueError:
            params["temperature"] = 0.7

    def _try_request(p: Dict[str, Any], retry_on_timeout=True, retry_on_rate=True):
        try:
            return client.chat.completions.create(**p)
        except httpx.ReadTimeout:
            if retry_on_timeout:
                print("[WARN] Request timed out, retrying once...")
                return _try_request(p, retry_on_timeout=False, retry_on_rate=retry_on_rate)
            print("[ERROR] Request timed out.")
            return None
        except Exception as e:
            msg = str(e)

            # --- Handle rate limits ---
            if "rate_limit_exceeded" in msg:
                if retry_on_rate:
                    wait_time = 10  # default
                    m = re.search(r"try again in ([0-9.]+)s", msg)
                    if m:
                        wait_time = float(m.group(1)) + 0.5
                    print(f"[WARN] Rate limit hit, waiting {wait_time:.1f}s before retry...")
                    time.sleep(wait_time)
                    return _try_request(p, retry_on_timeout=retry_on_timeout, retry_on_rate=False)
                print("[ERROR] Rate limit hit again, aborting.")
                return None

            # --- Param auto-fix ---
            if "max_tokens" in msg and "Unsupported" in msg:
                p.pop("max_tokens", None)
                p["max_completion_tokens"] = 8192
                print("[WARN] Switched to max_completion_tokens.")
                return _try_request(p, retry_on_timeout, retry_on_rate)
            if "max_completion_tokens" in msg and "Unsupported" in msg:
                p.pop("max_completion_tokens", None)
                p["max_tokens"] = 8192
                print("[WARN] Switched to max_tokens.")
                return _try_request(p, retry_on_timeout, retry_on_rate)
            if "temperature" in msg and "Unsupported" in msg:
                p.pop("temperature", None)
                print("[WARN] Removed temperature param.")
                return _try_request(p, retry_on_timeout, retry_on_rate)

            print(f"[ERROR] API call failed: {msg}")
            return None

    resp = _try_request(params)
    if not resp:
        return "[ERROR] API call failed."

    try:
        content = resp.choices[0].message.content
    except Exception:
        return "[ERROR] Empty or malformed response from model."

    if not content or not content.strip():
        return "[ERROR] Empty response from model."

    return content.strip()

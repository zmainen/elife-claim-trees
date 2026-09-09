"""Multi-provider LLM support via litellm.

Wraps litellm to provide a unified interface that the extraction and
review pipelines can use. Supports Anthropic, OpenAI, Google, OpenRouter,
and Vertex (via direct SDK for authenticated sessions).

The key insight: litellm uses provider-prefixed model names:
  anthropic/claude-sonnet-4-6
  openai/gpt-4o
  gemini/gemini-2.5-pro
  openrouter/anthropic/claude-sonnet-4

We store the provider prefix in the config and prepend it to model names.
"""

from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

# Provider → model catalog (what shows up in the dropdown)
PROVIDER_MODELS = {
    "anthropic": [
        {"id": "claude-sonnet-4-6", "name": "Claude Sonnet 4.6 (balanced)", "tier": "fast"},
        {"id": "claude-opus-4-8", "name": "Claude Opus 4.8 (best)", "tier": "best"},
        {"id": "claude-haiku-4-5", "name": "Claude Haiku 4.5 (fast/cheap)", "tier": "cheap"},
    ],
    "openai": [
        {"id": "gpt-4o", "name": "GPT-4o", "tier": "fast"},
        {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "tier": "cheap"},
        {"id": "o3", "name": "o3", "tier": "best"},
    ],
    "google": [
        {"id": "gemini-2.5-pro", "name": "Gemini 2.5 Pro (best)", "tier": "best"},
        {"id": "gemini-2.5-flash", "name": "Gemini 2.5 Flash (fast)", "tier": "fast"},
    ],
    "openrouter": [
        {"id": "anthropic/claude-sonnet-4", "name": "Claude Sonnet 4 (via OpenRouter)", "tier": "fast"},
        {"id": "openai/gpt-4o", "name": "GPT-4o (via OpenRouter)", "tier": "fast"},
        {"id": "google/gemini-2.5-pro", "name": "Gemini 2.5 Pro (via OpenRouter)", "tier": "best"},
    ],
    # Hosted demo path (server-paid Vertex). cr-mainen pins opus at 4-6 —
    # 4-7/4-8 time out on that region. Requires a demo token / passkey auth.
    "vertex": [
        {"id": "gemini-2.5-flash", "name": "Gemini 2.5 Flash (fastest)", "tier": "fast"},
        {"id": "gemini-2.5-pro", "name": "Gemini 2.5 Pro", "tier": "best"},
        {"id": "claude-sonnet-4-6", "name": "Claude Sonnet 4.6 (Vertex)", "tier": "fast"},
        {"id": "claude-opus-4-6", "name": "Claude Opus 4.6 (Vertex)", "tier": "best"},
    ],
}


def litellm_model_name(provider: str, model_id: str) -> str:
    """Convert provider + model_id to litellm's prefixed format."""
    if provider == "vertex":
        return f"vertex_ai/{model_id}"
    if provider == "openrouter":
        return f"openrouter/{model_id}"
    if provider == "google":
        return f"gemini/{model_id}"
    if provider == "openai":
        return f"openai/{model_id}"
    if provider == "anthropic":
        return f"anthropic/{model_id}"
    return model_id


def call_llm(
    *,
    provider: str,
    api_key: str,
    model: str,
    system: str,
    user_message: str,
    max_tokens: int = 32768,
) -> str:
    """Call an LLM via litellm. Returns the response text."""
    import litellm

    litellm_model = litellm_model_name(provider, model)

    # Set the API key for this call
    env_key = {
        "anthropic": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY",
        "google": "GEMINI_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
    }.get(provider)

    kwargs = {
        "model": litellm_model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user_message},
        ],
        "max_tokens": max_tokens,
    }

    if provider == "vertex":
        kwargs["vertex_project"] = os.environ.get("VERTEX_PROJECT_ID", "cr-mainen")
        kwargs["vertex_location"] = os.environ.get("VERTEX_REGION", "europe-west1")
    elif api_key and env_key:
        kwargs["api_key"] = api_key

    logger.info("litellm call: provider=%s model=%s", provider, litellm_model)

    response = litellm.completion(**kwargs)
    return response.choices[0].message.content


def stream_llm(
    *,
    provider: str,
    api_key: str,
    model: str,
    system: str,
    messages: list[dict],
    max_tokens: int = 4096,
):
    """Stream an LLM response via litellm. Yields text chunks."""
    import litellm

    litellm_model = litellm_model_name(provider, model)

    kwargs = {
        "model": litellm_model,
        "messages": [{"role": "system", "content": system}] + messages,
        "max_tokens": max_tokens,
        "stream": True,
    }

    if provider == "vertex":
        kwargs["vertex_project"] = os.environ.get("VERTEX_PROJECT_ID", "cr-mainen")
        kwargs["vertex_location"] = os.environ.get("VERTEX_REGION", "europe-west1")
    elif api_key:
        env_key = {
            "anthropic": "ANTHROPIC_API_KEY",
            "openai": "OPENAI_API_KEY",
            "google": "GEMINI_API_KEY",
            "openrouter": "OPENROUTER_API_KEY",
        }.get(provider)
        kwargs["api_key"] = api_key

    for chunk in litellm.completion(**kwargs):
        delta = chunk.choices[0].delta
        if delta and delta.content:
            yield delta.content

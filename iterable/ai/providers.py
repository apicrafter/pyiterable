"""
LLM provider abstraction layer.

Provides unified interface for different LLM providers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):
    """Base class for LLM providers."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> str:
        """
        Generate text using the LLM provider.

        Args:
            prompt: Input prompt
            model: Model name (provider-specific)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Provider-specific options

        Returns:
            Generated text
        """
        pass

    @abstractmethod
    def get_usage_info(self) -> dict[str, Any] | None:
        """
        Get token usage information if available.

        Returns:
            Dictionary with usage info (tokens, cost, etc.) or None
        """
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI provider implementation."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "OpenAI is required. Install with: pip install openai"
            )

        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self._usage_info: dict[str, Any] | None = None

    def generate(
        self,
        prompt: str,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> str:
        model = model or "gpt-4o-mini"
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )
        self._usage_info = {
            "prompt_tokens": response.usage.prompt_tokens if response.usage else None,
            "completion_tokens": response.usage.completion_tokens if response.usage else None,
            "total_tokens": response.usage.total_tokens if response.usage else None,
        }
        return response.choices[0].message.content

    def get_usage_info(self) -> dict[str, Any] | None:
        return self._usage_info


class OpenRouterProvider(LLMProvider):
    """OpenRouter provider implementation."""

    def __init__(self, api_key: str | None = None):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "OpenAI client is required for OpenRouter. Install with: pip install openai"
            )

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )
        self._usage_info: dict[str, Any] | None = None

    def generate(
        self,
        prompt: str,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> str:
        model = model or "openai/gpt-4o-mini"
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )
        self._usage_info = {
            "prompt_tokens": response.usage.prompt_tokens if response.usage else None,
            "completion_tokens": response.usage.completion_tokens if response.usage else None,
            "total_tokens": response.usage.total_tokens if response.usage else None,
        }
        return response.choices[0].message.content

    def get_usage_info(self) -> dict[str, Any] | None:
        return self._usage_info


class OllamaProvider(LLMProvider):
    """Ollama provider implementation (local)."""

    def __init__(self, base_url: str = "http://localhost:11434"):
        try:
            import requests
        except ImportError:
            raise ImportError(
                "requests is required for Ollama. Install with: pip install requests"
            )

        self.base_url = base_url
        self._usage_info: dict[str, Any] | None = None

    def generate(
        self,
        prompt: str,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> str:
        import requests

        model = model or "llama2"
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                },
                **kwargs,
            },
            timeout=300,
        )
        response.raise_for_status()
        result = response.json()
        self._usage_info = {
            "prompt_tokens": result.get("prompt_eval_count"),
            "completion_tokens": result.get("eval_count"),
            "total_tokens": result.get("prompt_eval_count", 0) + result.get("eval_count", 0),
        }
        return result.get("response", "")

    def get_usage_info(self) -> dict[str, Any] | None:
        return self._usage_info


class LMStudioProvider(LLMProvider):
    """LMStudio provider implementation (local)."""

    def __init__(self, base_url: str = "http://localhost:1234/v1"):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "OpenAI client is required for LMStudio. Install with: pip install openai"
            )

        self.client = OpenAI(base_url=base_url, api_key="not-needed")
        self._usage_info: dict[str, Any] | None = None

    def generate(
        self,
        prompt: str,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> str:
        # LMStudio uses OpenAI-compatible API
        response = self.client.chat.completions.create(
            model=model or "local-model",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )
        self._usage_info = {
            "prompt_tokens": response.usage.prompt_tokens if response.usage else None,
            "completion_tokens": response.usage.completion_tokens if response.usage else None,
            "total_tokens": response.usage.total_tokens if response.usage else None,
        }
        return response.choices[0].message.content

    def get_usage_info(self) -> dict[str, Any] | None:
        return self._usage_info


class PerplexityProvider(LLMProvider):
    """Perplexity provider implementation."""

    def __init__(self, api_key: str | None = None):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError(
                "OpenAI client is required for Perplexity. Install with: pip install openai"
            )

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai",
        )
        self._usage_info: dict[str, Any] | None = None

    def generate(
        self,
        prompt: str,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
        **kwargs: Any,
    ) -> str:
        model = model or "llama-3.1-sonar-small-128k-online"
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )
        self._usage_info = {
            "prompt_tokens": response.usage.prompt_tokens if response.usage else None,
            "completion_tokens": response.usage.completion_tokens if response.usage else None,
            "total_tokens": response.usage.total_tokens if response.usage else None,
        }
        return response.choices[0].message.content

    def get_usage_info(self) -> dict[str, Any] | None:
        return self._usage_info


def get_provider(
    provider: str,
    api_key: str | None = None,
    base_url: str | None = None,
) -> LLMProvider:
    """
    Get LLM provider instance.

    Args:
        provider: Provider name - "openai", "openrouter", "ollama", "lmstudio", "perplexity"
        api_key: API key (if required)
        base_url: Base URL (for local providers)

    Returns:
        LLMProvider instance
    """
    if provider == "openai":
        return OpenAIProvider(api_key=api_key, base_url=base_url)
    elif provider == "openrouter":
        return OpenRouterProvider(api_key=api_key)
    elif provider == "ollama":
        return OllamaProvider(base_url=base_url or "http://localhost:11434")
    elif provider == "lmstudio":
        return LMStudioProvider(base_url=base_url or "http://localhost:1234/v1")
    elif provider == "perplexity":
        return PerplexityProvider(api_key=api_key)
    else:
        raise ValueError(f"Unknown provider: {provider}")

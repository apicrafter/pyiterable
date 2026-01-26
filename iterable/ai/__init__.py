"""
AI-powered documentation generation.

Provides functions for generating dataset documentation using various LLM providers.
"""

from . import doc
from .doc import generate

__all__ = ["doc", "generate"]

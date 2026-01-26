"""
AI-powered documentation generation.

Generates dataset documentation using LLM providers.
"""

from __future__ import annotations

import collections.abc
import json
from typing import Any

from ..helpers.detect import open_iterable
from ..ops import schema
from ..types import Row
from .providers import get_provider


def generate(
    iterable: collections.abc.Iterable[Row] | str,
    provider: str = "openai",
    model: str | None = None,
    format: str = "markdown",
    api_key: str | None = None,
    base_url: str | None = None,
    include_schema: bool = True,
    include_samples: bool = True,
    sample_size: int = 5,
    temperature: float = 0.7,
    max_tokens: int | None = None,
    **kwargs: Any,
) -> str | dict[str, Any]:
    """
    Generate AI-powered documentation for a dataset.

    Args:
        iterable: An iterable of row dictionaries, or a file path/stream
        provider: LLM provider - "openai", "openrouter", "ollama", "lmstudio", "perplexity" (default: "openai")
        model: Model name (provider-specific, uses default if None)
        format: Output format - "markdown", "json", "html" (default: "markdown")
        api_key: API key for the provider (uses environment variable if None)
        base_url: Base URL for local providers (Ollama, LMStudio)
        include_schema: Whether to include schema information (default: True)
        include_samples: Whether to include sample data (default: True)
        sample_size: Number of sample rows to include (default: 5)
        temperature: Sampling temperature (default: 0.7)
        max_tokens: Maximum tokens to generate
        **kwargs: Additional provider-specific options

    Returns:
        Generated documentation as string (markdown/html) or dict (json)

    Example:
        >>> from iterable.ai import doc
        >>> documentation = doc.generate(
        ...     "data.csv",
        ...     provider="openai",
        ...     model="gpt-4o-mini",
        ...     format="markdown"
        ... )
        >>> print(documentation)
    """
    # Open iterable if file path
    if isinstance(iterable, str):
        iterable_obj = open_iterable(iterable)
    else:
        iterable_obj = iterable

    # Collect context information
    context: dict[str, Any] = {}

    # Get schema if requested
    if include_schema:
        try:
            schema_info = schema.infer(iterable_obj, detect_constraints=True)
            context["schema"] = schema_info
        except Exception:
            # If schema inference fails, continue without it
            pass

    # Get sample data if requested
    if include_samples:
        samples: list[Row] = []
        try:
            # Reset if possible
            if hasattr(iterable_obj, "reset"):
                iterable_obj.reset()
            elif isinstance(iterable, str):
                iterable_obj = open_iterable(iterable)

            for i, row in enumerate(iterable_obj):
                if i >= sample_size:
                    break
                samples.append(row)
            context["samples"] = samples
        except Exception:
            # If sampling fails, continue without it
            pass

    # Build prompt
    prompt = _build_documentation_prompt(context)

    # Get provider and generate
    try:
        llm_provider = get_provider(provider, api_key=api_key, base_url=base_url)
        generated_text = llm_provider.generate(
            prompt=prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )
    except ImportError as e:
        raise ImportError(
            f"Provider '{provider}' requires additional dependencies. "
            f"Install with: pip install openai (or provider-specific package)"
        ) from e

    # Format output
    if format == "json":
        return _format_as_json(generated_text, context, llm_provider.get_usage_info())
    elif format == "html":
        return _format_as_html(generated_text)
    else:  # markdown
        return generated_text


def _build_documentation_prompt(context: dict[str, Any]) -> str:
    """Build prompt for documentation generation."""
    prompt_parts = [
        "Generate comprehensive documentation for a dataset. Include:",
        "- Dataset overview and purpose",
        "- Field descriptions with types and constraints",
        "- Data quality notes",
        "- Usage examples",
        "",
    ]

    if "schema" in context:
        schema_info = context["schema"]
        prompt_parts.append("## Schema Information:")
        prompt_parts.append(json.dumps(schema_info, indent=2, default=str))
        prompt_parts.append("")

    if "samples" in context:
        samples = context["samples"]
        prompt_parts.append("## Sample Data:")
        prompt_parts.append(json.dumps(samples, indent=2, default=str))
        prompt_parts.append("")

    prompt_parts.append(
        "Generate well-formatted markdown documentation that describes this dataset comprehensively."
    )

    return "\n".join(prompt_parts)


def _format_as_json(
    generated_text: str,
    context: dict[str, Any],
    usage_info: dict[str, Any] | None,
) -> dict[str, Any]:
    """Format documentation as JSON."""
    return {
        "documentation": generated_text,
        "schema": context.get("schema"),
        "samples": context.get("samples"),
        "usage": usage_info,
    }


def _format_as_html(markdown_text: str) -> str:
    """Format markdown documentation as HTML."""
    try:
        import markdown
    except ImportError:
        # Fallback: simple HTML wrapper
        html_content = markdown_text.replace("\n", "<br>\n")
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Dataset Documentation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        h1, h2, h3 {{ color: #333; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""

    html = markdown.markdown(markdown_text, extensions=["fenced_code", "tables"])
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Dataset Documentation</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        h1, h2, h3 {{ color: #333; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
{html}
</body>
</html>"""

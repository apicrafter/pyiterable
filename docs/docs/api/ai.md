---
sidebar_position: 15
title: AI-Powered Documentation
description: Generate dataset documentation using LLM providers
---

# AI-Powered Documentation

The `iterable.ai` module provides functions for generating AI-powered documentation for datasets using various LLM providers.

## Overview

AI documentation generation helps you:
- **Automatically document datasets** using AI analysis
- **Support multiple LLM providers** (OpenAI, OpenRouter, Ollama, LMStudio, Perplexity)
- **Generate multiple formats** (Markdown, JSON, HTML)
- **Integrate with schema inference** for accurate field descriptions
- **Include sample data** for better context

## Functions

### `doc.generate()`

Generate AI-powered documentation for a dataset.

```python
from iterable.ai import doc

# Basic usage with OpenAI
documentation = doc.generate(
    "data.csv",
    provider="openai",
    model="gpt-4o-mini",
    format="markdown"
)
print(documentation)
```

**Parameters:**
- `iterable`: An iterable of row dictionaries, or a file path/stream
- `provider`: LLM provider - "openai", "openrouter", "ollama", "lmstudio", "perplexity" (default: "openai")
- `model`: Model name (provider-specific, uses default if None)
- `format`: Output format - "markdown", "json", "html" (default: "markdown")
- `api_key`: API key for the provider (uses environment variable if None)
- `base_url`: Base URL for local providers (Ollama, LMStudio)
- `include_schema`: Whether to include schema information (default: True)
- `include_samples`: Whether to include sample data (default: True)
- `sample_size`: Number of sample rows to include (default: 5)
- `temperature`: Sampling temperature (default: 0.7)
- `max_tokens`: Maximum tokens to generate
- `**kwargs`: Additional provider-specific options

**Returns:**
- String for markdown/html formats
- Dictionary for JSON format (includes documentation, schema, samples, usage)

## Examples

### Basic Documentation Generation

```python
from iterable.ai import doc

# Generate markdown documentation
documentation = doc.generate(
    "users.csv",
    provider="openai",
    model="gpt-4o-mini"
)

# Save to file
with open("users_docs.md", "w") as f:
    f.write(documentation)
```

### Using Different Providers

```python
from iterable.ai import doc

# OpenAI
docs = doc.generate("data.csv", provider="openai", api_key="sk-...")

# OpenRouter
docs = doc.generate("data.csv", provider="openrouter", api_key="sk-...")

# Ollama (local)
docs = doc.generate("data.csv", provider="ollama", base_url="http://localhost:11434")

# LMStudio (local)
docs = doc.generate("data.csv", provider="lmstudio", base_url="http://localhost:1234/v1")

# Perplexity
docs = doc.generate("data.csv", provider="perplexity", api_key="pplx-...")
```

### JSON Format

```python
from iterable.ai import doc
import json

# Generate JSON documentation
result = doc.generate(
    "data.csv",
    provider="openai",
    format="json"
)

# Access components
print(result["documentation"])  # Generated markdown
print(result["schema"])          # Schema information
print(result["samples"])         # Sample data
print(result["usage"])           # Token usage info
```

### HTML Format

```python
from iterable.ai import doc

# Generate HTML documentation
html_docs = doc.generate(
    "data.csv",
    provider="openai",
    format="html"
)

# Save to file
with open("docs.html", "w") as f:
    f.write(html_docs)
```

### Customizing Documentation

```python
from iterable.ai import doc

# Generate without schema (faster, less accurate)
docs = doc.generate(
    "data.csv",
    provider="openai",
    include_schema=False
)

# Generate with more samples
docs = doc.generate(
    "data.csv",
    provider="openai",
    sample_size=10
)

# Generate with custom temperature
docs = doc.generate(
    "data.csv",
    provider="openai",
    temperature=0.3  # More deterministic
)
```

### Combining with Schema Inference

```python
from iterable.ai import doc
from iterable.ops import schema

# Infer schema first
sch = schema.infer("data.csv", detect_constraints=True)

# Generate documentation (will use inferred schema)
docs = doc.generate(
    "data.csv",
    provider="openai",
    include_schema=True  # Uses schema.infer() internally
)
```

### Using Environment Variables

```python
import os
from iterable.ai import doc

# Set API key via environment variable
os.environ["OPENAI_API_KEY"] = "sk-..."

# Use without explicit API key
docs = doc.generate("data.csv", provider="openai")
```

## Supported Providers

### OpenAI

- **Provider name**: `"openai"`
- **Default model**: `"gpt-4o-mini"`
- **Requirements**: `pip install openai`
- **API Key**: Set `OPENAI_API_KEY` environment variable or pass `api_key` parameter
- **Models**: Any OpenAI model (gpt-4o, gpt-4o-mini, gpt-3.5-turbo, etc.)

### OpenRouter

- **Provider name**: `"openrouter"`
- **Default model**: `"openai/gpt-4o-mini"`
- **Requirements**: `pip install openai`
- **API Key**: Set `OPENROUTER_API_KEY` environment variable or pass `api_key` parameter
- **Models**: Any model available on OpenRouter

### Ollama (Local)

- **Provider name**: `"ollama"`
- **Default model**: `"llama2"`
- **Requirements**: `pip install requests` and running Ollama locally
- **Base URL**: Defaults to `"http://localhost:11434"`, can be customized
- **Models**: Any model installed in Ollama (llama2, mistral, codellama, etc.)

### LMStudio (Local)

- **Provider name**: `"lmstudio"`
- **Default model**: `"local-model"`
- **Requirements**: `pip install openai` and running LMStudio locally
- **Base URL**: Defaults to `"http://localhost:1234/v1"`, can be customized
- **Models**: Any model loaded in LMStudio

### Perplexity

- **Provider name**: `"perplexity"`
- **Default model**: `"llama-3.1-sonar-small-128k-online"`
- **Requirements**: `pip install openai`
- **API Key**: Set `PERPLEXITY_API_KEY` environment variable or pass `api_key` parameter
- **Models**: Perplexity-specific models

## Output Formats

### Markdown

Default format, returns a markdown string:

```markdown
# Dataset Documentation

## Overview
This dataset contains user information...

## Fields

### id
- Type: integer
- Description: Unique user identifier
- Constraints: Required, non-null

### name
- Type: string
- Description: User's full name
...
```

### JSON

Returns a dictionary with structured information:

```json
{
  "documentation": "# Dataset Documentation\n\n...",
  "schema": {
    "fields": {...},
    "constraints": {...}
  },
  "samples": [
    {"id": 1, "name": "John"},
    ...
  ],
  "usage": {
    "prompt_tokens": 500,
    "completion_tokens": 200,
    "total_tokens": 700
  }
}
```

### HTML

Returns a complete HTML document with embedded styles:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Dataset Documentation</title>
    <style>...</style>
</head>
<body>
    <!-- Generated documentation -->
</body>
</html>
```

## Error Handling

```python
from iterable.ai import doc

try:
    docs = doc.generate("data.csv", provider="openai")
except ImportError as e:
    print(f"Missing dependencies: {e}")
    # Install with: pip install openai
except ValueError as e:
    print(f"Invalid provider: {e}")
except Exception as e:
    print(f"API error: {e}")
```

## Performance and Cost

### Token Usage

Token usage information is available in JSON format:

```python
result = doc.generate("data.csv", provider="openai", format="json")
usage = result["usage"]
print(f"Tokens used: {usage['total_tokens']}")
```

### Cost Optimization

1. **Use smaller models** for cost savings (e.g., `gpt-4o-mini` instead of `gpt-4o`)
2. **Disable schema/samples** if not needed (`include_schema=False`, `include_samples=False`)
3. **Use local providers** (Ollama, LMStudio) for free generation
4. **Limit sample size** to reduce prompt size

### Local Providers

For cost-free generation, use local providers:

```python
# Ollama (free, local)
docs = doc.generate(
    "data.csv",
    provider="ollama",
    model="llama2"
)

# LMStudio (free, local)
docs = doc.generate(
    "data.csv",
    provider="lmstudio",
    model="local-model"
)
```

## Integration with Other Operations

```python
from iterable.ai import doc
from iterable.ops import schema, stats, inspect

# Analyze dataset first
analysis = inspect.analyze("data.csv")
schema_info = schema.infer("data.csv", detect_constraints=True)
stats_info = stats.compute("data.csv")

# Generate comprehensive documentation
docs = doc.generate(
    "data.csv",
    provider="openai",
    include_schema=True,
    sample_size=10
)
```

## Installation

AI documentation requires optional dependencies:

```bash
# OpenAI/OpenRouter/Perplexity
pip install openai

# Ollama (local)
pip install requests

# All AI dependencies
pip install iterabledata[ai]
```

## Best Practices

1. **Use schema inference** for accurate field descriptions
2. **Include samples** for better context (but limit size for cost)
3. **Choose appropriate models** based on quality vs. cost needs
4. **Use local providers** for sensitive data or cost-free generation
5. **Cache results** for repeated documentation generation
6. **Review generated docs** - AI may make mistakes, always verify

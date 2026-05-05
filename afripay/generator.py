"""OpenAI-backed scaffold generation engine."""

import json
from pathlib import Path
from typing import Any

import yaml
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]


def _load_provider(provider_name: str) -> dict[str, Any]:
    provider_path = ROOT / "providers" / f"{provider_name}.json"
    return json.loads(provider_path.read_text())


def _load_security_rules(provider_name: str) -> dict[str, Any]:
    rules_path = ROOT / "security" / "rules.yaml"
    rules = yaml.safe_load(rules_path.read_text())
    return rules[provider_name]


def _build_prompt(provider: dict[str, Any], rules: dict[str, Any], framework: str) -> str:
    provider_context = json.dumps(provider, indent=2)
    rules_context = json.dumps(rules, indent=2)
    verification_method = rules.get("verification_method", "none")

    return f"""
Generate a production-ready Python {framework} integration module.

Provider spec:
{provider_context}

Security rules:
{rules_context}

Requirements:
- Include a security decision comment block explaining each security choice.
- Implement authentication handling using the provider spec.
- Implement the primary endpoint call from the provider spec.
- Implement a webhook handler when the provider has webhook rules.
- Include webhook signature verification using verification_method "{verification_method}" from rules.yaml.
- Include idempotency handling based on the security rules.
- Include structured error handling for provider and network failures.
- Return only Python code, with no markdown fences or commentary.
""".strip()


def generate_scaffold(provider_name: str, framework: str) -> str:
    """Generate scaffold code for a provider and framework."""
    provider = _load_provider(provider_name)
    rules = _load_security_rules(provider_name)
    prompt = _build_prompt(provider, rules, framework)
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You generate secure, idiomatic Python integration modules.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    content = response.choices[0].message.content
    return content.strip() if content else ""


def generate_tests(provider_name: str, framework: str, scaffold_code: str) -> str:
    """Generate pytest tests for scaffold code."""
    prompt = f"""
Generate a pytest test file for a Python {framework} integration module.

Provider name:
{provider_name}

Scaffold code:
{scaffold_code}

Requirements:
- Import the generated module as integration.
- Test the primary successful provider flow.
- Test provider or network error handling where possible.
- Test webhook signature verification behavior when a webhook handler exists.
- Test idempotency behavior when the scaffold includes idempotency handling.
- Return only Python test code, with no markdown fences or commentary.
""".strip()
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You generate focused pytest files for secure Python integrations.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    content = response.choices[0].message.content
    return content.strip() if content else ""


def generate_readme(
    provider_name: str,
    framework: str,
    scaffold_code: str,
    security_rules: dict[str, Any],
) -> str:
    """Generate a README explaining scaffold security decisions."""
    rules_context = json.dumps(security_rules, indent=2)
    prompt = f"""
Generate a concise README.md section for a Python {framework} integration scaffold.

Provider name:
{provider_name}

Security rules:
{rules_context}

Scaffold code:
{scaffold_code}

Requirements:
- Explain in plain English what the scaffold does.
- Explain why webhook signature verification is implemented the way it is for this provider.
- Use the security rules as the source of truth for verification behavior.
- List the environment variables developers must set before using the scaffold.
- Include provider-specific gotchas from the rules, such as when a provider has no HMAC.
- Keep the README concise and practical.
- Return only Markdown content, with no markdown fences or commentary.
""".strip()
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You generate concise security-focused README documentation.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    content = response.choices[0].message.content
    return content.strip() if content else ""

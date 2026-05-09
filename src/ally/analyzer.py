"""OpenAI-backed report analysis engine."""

import json
from pathlib import Path
from typing import Any

import yaml
from openai import OpenAI

ROOT = Path(__file__).resolve().parents[2]


def _load_framework(framework_name: str) -> dict[str, Any]:
    framework_path = ROOT / "frameworks" / f"{framework_name}.json"
    return json.loads(framework_path.read_text())


def _load_analysis_rules(framework_name: str) -> dict[str, Any]:
    rules_path = ROOT / "analysis" / "rules.yaml"
    rules = yaml.safe_load(rules_path.read_text())
    return rules[framework_name]


def _build_prompt(report_text: str, framework: dict[str, Any], rules: dict[str, Any]) -> str:
    framework_context = json.dumps(framework, indent=2)
    rules_context = json.dumps(rules, indent=2)

    return f"""
Generate a concise Ally accountability analysis.

Report:
{report_text}

Framework:
{framework_context}

Analysis rules:
{rules_context}

Requirements:
- Summarize the accountability concern.
- Identify relevant rights or accountability categories.
- Explain the analysis in plain English.
- Return only Markdown content, with no markdown fences or commentary.
""".strip()


def generate_analysis(report_text: str, framework_name: str) -> str:
    """Generate analysis for a report and rights framework."""
    framework = _load_framework(framework_name)
    rules = _load_analysis_rules(framework_name)
    prompt = _build_prompt(report_text, framework, rules)
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You generate careful community accountability analysis.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    content = response.choices[0].message.content
    return content.strip() if content else ""


def generate_analysis_tests(report_text: str, framework_name: str, analysis_text: str) -> str:
    """Generate pytest tests for analysis behavior."""
    prompt = f"""
Generate a pytest test file for an Ally analysis module.

Framework name:
{framework_name}

Report:
{report_text}

Analysis:
{analysis_text}

Requirements:
- Test the primary successful report analysis flow.
- Test that relevant accountability categories are represented where possible.
- Return only Python test code, with no markdown fences or commentary.
""".strip()
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You generate focused pytest files for Ally analysis.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    content = response.choices[0].message.content
    return content.strip() if content else ""


def generate_report_readme(
    report_text: str,
    framework_name: str,
    analysis_text: str,
    analysis_rules: dict[str, Any],
) -> str:
    """Generate a README explaining analysis decisions."""
    rules_context = json.dumps(analysis_rules, indent=2)
    prompt = f"""
Generate a concise README.md section for an Ally accountability analysis.

Framework name:
{framework_name}

Analysis rules:
{rules_context}

Report:
{report_text}

Analysis:
{analysis_text}

Requirements:
- Explain in plain English what the analysis does.
- Use the analysis rules as the source of truth.
- Keep the README concise and practical.
- Return only Markdown content, with no markdown fences or commentary.
""".strip()
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You generate concise accountability-focused README documentation.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    content = response.choices[0].message.content
    return content.strip() if content else ""

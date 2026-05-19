#!/usr/bin/env python3
"""
Generate Hermes cron job config from natural language.

Usage:
    python generate_cron.py "every day at 9am" --prompt "Check logs"
    python generate_cron.py "every 2 hours" --prompt "Monitor API" --name "api-monitor" --output yaml
"""

import argparse
import json
import sys

# Allow running from both the scripts dir and the skill root
try:
    from parse import parse_natural_language
except ImportError:
    from scripts.parse import parse_natural_language


def generate_cron_config(schedule_text: str, prompt: str, name: str = None) -> dict:
    """
    Generate a Hermes cronjob config dict from natural language.

    Args:
        schedule_text: Natural language schedule (e.g., "every day at 9am")
        prompt: Task prompt for the cron job
        name: Job name (auto-generated if not provided)

    Returns:
        Dict ready to pass to cronjob(action='create', **config)
    """
    cron_expr = parse_natural_language(schedule_text)

    if not name:
        safe_text = schedule_text.replace(" ", "-").replace(":", "").lower()
        name = f"auto-{safe_text}"

    config = {
        "name": name,
        "schedule": cron_expr,
        "prompt": prompt,
        "deliver": "origin",
        "enabled_toolsets": ["terminal", "file", "cronjob"],
    }

    return config


def main():
    parser = argparse.ArgumentParser(
        description="Generate Hermes cron job config from natural language"
    )
    parser.add_argument("schedule", help="Natural language schedule, e.g., 'every day at 9am'")
    parser.add_argument("--prompt", required=True, help="Task prompt for the cron job")
    parser.add_argument("--name", help="Job name (auto-generated if not provided)")
    parser.add_argument(
        "--output",
        choices=["json", "yaml"],
        default="json",
        help="Output format (default: json)",
    )

    args = parser.parse_args()

    try:
        config = generate_cron_config(args.schedule, args.prompt, args.name)

        if args.output == "json":
            print(json.dumps(config, indent=2))
        else:
            # Simple YAML-like output
            for key, value in config.items():
                if isinstance(value, list):
                    print(f"{key}:")
                    for item in value:
                        print(f"  - {item}")
                elif isinstance(value, dict):
                    print(f"{key}:")
                    for k, v in value.items():
                        print(f"  {k}: {v}")
                else:
                    print(f"{key}: {value}")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

---
name: cron-from-natural-language
description: "Generate Hermes cron jobs from natural language descriptions"
version: 1.0.0
author: Peepo
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [automation, cron, scheduling, nlp]
    related_skills: [hermes-agent]
---

# Cron from Natural Language

## Overview

Convert natural language scheduling descriptions into Hermes cron jobs.

Examples:
- "every day at 9am" → `0 9 * * *`
- "every 2 hours" → `0 */2 * * *`
- "weekdays at 3pm" → `0 15 * * 1-5`

## Quick Start

1. Install the skill:
```bash
hermes skill install cron-from-natural-language
```

2. Use in your Hermes session:
```python
# Load the skill
from scripts.generate_cron import generate_cron_config

config = generate_cron_config(
    schedule_text="every day at 9am",
    prompt="Check system logs and send summary",
    name="daily-log-check"
)

cronjob(action='create', **config)
```

3. Or use CLI directly:
```bash
python scripts/generate_cron.py "every 2 hours" --prompt "Monitor API health" --name "api-health-check"
```

## Supported Phrases

- "every day at [time]" (e.g., "every day at 9am", "every day at 2:30pm")
- "every [N] hours" (e.g., "every 2 hours", "every 6 hours")
- "weekdays at [time]" (e.g., "weekdays at 3pm")
- "every [N] minutes" (e.g., "every 5 minutes", "every 30 minutes")

## Examples

### Daily backup reminder
```bash
python scripts/generate_cron.py "every day at 11pm" \
  --prompt "Check if daily backups completed successfully. If not, alert via Telegram." \
  --name "backup-check"
```

### Weekly report
```bash
python scripts/generate_cron.py "weekdays at 8am" \
  --prompt "Generate daily team status report from Jira and GitHub activity." \
  --name "daily-status"
```

### Real-time monitoring
```bash
python scripts/generate_cron.py "every 5 minutes" \
  --prompt "Check server CPU and memory usage. Alert if >80%." \
  --name "server-monitor"
```

## Integration with Hermes Skills

### With `hermes-agent` skill
```python
# Auto-setup cron jobs for new Hermes deployments
from scripts.generate_cron import generate_cron_config

jobs = [
    ("every day at 9am", "Daily system health check"),
    ("every 2 hours", "API endpoint monitoring"),
    ("weekdays at 5pm", "End-of-day summary report"),
]

for schedule, prompt in jobs:
    config = generate_cron_config(schedule, prompt)
    cronjob(action='create', **config)
```

## Contributing

1. Fork the repository
2. Add new parsing patterns in `scripts/parse.py`
3. Submit a pull request

## License

MIT

"""
Natural Language to Cron Expression Parser.

Converts phrases like "every day at 9am" into cron expressions like "0 9 * * *".
"""

import re


def parse_natural_language(text: str) -> str:
    """
    Convert natural language scheduling text to cron expression.

    Args:
        text: Natural language schedule description.
              Examples: "every day at 9am", "every 2 hours", "weekdays at 3pm"

    Returns:
        Cron expression string.

    Raises:
        ValueError: If text cannot be parsed.
    """
    text = text.lower().strip()

    # Pattern: every day at HH:MM or HHam/pm
    match = re.match(r'every day at (\d{1,2})(?::(\d{2}))?\s*(am|pm)?', text)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2) or 0)
        ampm = match.group(3)

        if ampm:
            if ampm == 'pm' and hour < 12:
                hour += 12
            elif ampm == 'am' and hour == 12:
                hour = 0

        return f"{minute} {hour} * * *"

    # Pattern: every N hours
    match = re.match(r'every (\d+)\s*hours?', text)
    if match:
        hours = int(match.group(1))
        if hours < 1:
            raise ValueError("Hours must be >= 1")
        return f"0 */{hours} * * *"

    # Pattern: weekdays at HH:MM
    match = re.match(r'weekdays?\s*at\s*(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', text)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2) or 0)
        ampm = match.group(3)

        if ampm:
            if ampm == 'pm' and hour < 12:
                hour += 12
            elif ampm == 'am' and hour == 12:
                hour = 0

        return f"{minute} {hour} * * 1-5"

    # Pattern: weekends at HH:MM
    match = re.match(r'weekends?\s*at\s*(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', text)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2) or 0)
        ampm = match.group(3)

        if ampm:
            if ampm == 'pm' and hour < 12:
                hour += 12
            elif ampm == 'am' and hour == 12:
                hour = 0

        return f"{minute} {hour} * * 0,6"

    # Pattern: every N minutes
    match = re.match(r'every (\d+)\s*minutes?', text)
    if match:
        minutes = int(match.group(1))
        if minutes < 1:
            raise ValueError("Minutes must be >= 1")
        return f"*/{minutes} * * * *"

    raise ValueError(
        f"Could not parse schedule: '{text}'. "
        "Supported formats: 'every day at 9am', 'every 2 hours', "
        "'weekdays at 3pm', 'weekends at 10am', 'every 5 minutes'"
    )


if __name__ == "__main__":
    test_cases = [
        "every day at 9am",
        "every day at 2:30pm",
        "every day at 12pm",
        "every day at 12am",
        "every 2 hours",
        "every 6 hours",
        "weekdays at 3pm",
        "weekdays at 8:30am",
        "weekends at 10am",
        "every 5 minutes",
        "every 30 minutes",
    ]

    print(f"{'Input':25} → {'Cron Expression':15}")
    print("-" * 42)
    for test in test_cases:
        try:
            cron = parse_natural_language(test)
            print(f"{test:25} → {cron:15}")
        except ValueError as e:
            print(f"{test:25} → ERROR: {e}")

from __future__ import annotations

import calendar

cron_presets: dict[str, str] = {
    "@hourly": "0 * * * *",
    "@daily": "0 0 * * *",
    "@weekly": "0 0 * * 0",
    "@monthly": "0 0 1 * *",
    "@quarterly": "0 0 1 */3 *",
    "@yearly": "0 0 1 1 *",
}


def datetime_to_nano(datetime) -> int | None:
    """Convert datetime to nanoseconds."""
    if datetime:
        if datetime.tzinfo is None:
            # There is no timezone info, handle it the same as UTC.
            timestamp = calendar.timegm(datetime.timetuple()) + datetime.microsecond / 1e6
        else:
            # The datetime is timezone-aware. Use timestamp directly.
            timestamp = datetime.timestamp()
        return int(timestamp * 1e9)
    return None

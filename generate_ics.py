import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def esc(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def fold(line: str, limit: int = 73) -> list[str]:
    data = line.encode("utf-8")
    chunks = []
    while len(data) > limit:
        cut = limit
        while cut > 0 and (data[cut] & 0xC0) == 0x80:
            cut -= 1
        chunks.append(data[:cut].decode("utf-8"))
        data = data[cut:]
    chunks.append(data.decode("utf-8"))
    return [chunks[0], *[" " + x for x in chunks[1:]]]


events = json.loads((ROOT / "events.json").read_text(encoding="utf-8"))
now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
lines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//Desolatepuppy//Market Events Calendar//ZH-CN",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    "X-WR-CALNAME:Investment 4.0 市场与投资事件",
    "X-WR-CALDESC:资本、席位、研究精力与投资纪律复盘",
    "X-WR-TIMEZONE:America/Los_Angeles",
    "REFRESH-INTERVAL;VALUE=DURATION:PT6H",
    "X-PUBLISHED-TTL:PT6H",
]

for event in events:
    raw = [
        "BEGIN:VEVENT",
        f"UID:{event['uid']}@desolatepuppy.github.io",
        f"DTSTAMP:{now}",
    ]

    if event.get("date"):
        start_day = date.fromisoformat(event["date"])
        end_day = start_day + timedelta(days=1)
        raw.extend(
            [
                f"DTSTART;VALUE=DATE:{start_day.strftime('%Y%m%d')}",
                f"DTEND;VALUE=DATE:{end_day.strftime('%Y%m%d')}",
            ]
        )
    else:
        start = datetime.fromisoformat(event["start_utc"].replace("Z", "+00:00"))
        end = start + timedelta(minutes=int(event["duration_minutes"]))
        raw.extend(
            [
                f"DTSTART:{start.strftime('%Y%m%dT%H%M%SZ')}",
                f"DTEND:{end.strftime('%Y%m%dT%H%M%SZ')}",
            ]
        )

    raw.extend(
        [
            f"SUMMARY:{esc(event['summary'])}",
            f"DESCRIPTION:{esc(event['description'])}",
            f"CATEGORIES:{esc(event['category'])}",
        ]
    )
    if event.get("url"):
        raw.append(f"URL:{event['url']}")
    if event.get("rrule"):
        raw.append(f"RRULE:{event['rrule']}")
    raw.extend(
        [
            f"STATUS:{event.get('status', 'CONFIRMED')}",
            "TRANSP:TRANSPARENT",
        ]
    )

    alarms = event.get("alarms")
    if alarms is None:
        alarms = [event.get("alarm", "-P1D" if event.get("date") else "-PT30M")]
    for alarm in alarms:
        raw.extend(
            [
                "BEGIN:VALARM",
                f"TRIGGER:{alarm}",
                "ACTION:DISPLAY",
                f"DESCRIPTION:{esc(event.get('alarm_text', '投资日历事件提醒'))}",
                "END:VALARM",
            ]
        )
    raw.append("END:VEVENT")
    for line in raw:
        lines.extend(fold(line))

lines.append("END:VCALENDAR")
payload = ("\r\n".join(lines) + "\r\n").encode("utf-8")
(ROOT / "investment3_portfolio_watch_pdt.ics").write_bytes(payload)
(ROOT / "calendar.ics").write_bytes(payload)
print(f"Generated {len(events)} events")

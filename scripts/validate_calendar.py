import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "events.json"
CANONICAL = ROOT / "investment3_portfolio_watch_pdt.ics"
ALIAS = ROOT / "calendar.ics"


def fail(message: str) -> None:
    raise SystemExit(f"ERROR: {message}")


events = json.loads(EVENTS.read_text(encoding="utf-8"))
uids = [event["uid"] for event in events]
duplicate_uids = [uid for uid, count in Counter(uids).items() if count > 1]
if duplicate_uids:
    fail(f"duplicate UIDs: {duplicate_uids}")

date_title = []
for event in events:
    start_key = event.get("date") or event.get("start_utc", "")[:10]
    date_title.append((start_key, event["summary"]))
duplicate_slots = [item for item, count in Counter(date_title).items() if count > 1]
if duplicate_slots:
    fail(f"duplicate date+summary pairs: {duplicate_slots}")

for event in events:
    if "date" not in event and "start_utc" not in event:
        fail(f"event has no date: {event['uid']}")
    if event.get("alarms") is not None:
        alarms = event["alarms"]
        if not isinstance(alarms, list) or not alarms:
            fail(f"alarms must be a non-empty list: {event['uid']}")
        if len(alarms) != len(set(alarms)):
            fail(f"duplicate alarms: {event['uid']}")
    if event.get("status") == "TENTATIVE":
        marker_text = event["summary"] + event["description"]
        if not any(marker in marker_text for marker in ("预约", "预计", "研究检查", "待公告", "未确认")):
            fail(f"tentative event lacks a visible uncertainty label: {event['uid']}")

for path in (CANONICAL, ALIAS):
    if not path.exists():
        fail(f"missing generated feed: {path.name}")

canonical = CANONICAL.read_bytes()
alias = ALIAS.read_bytes()
if canonical != alias:
    fail("canonical feed and compatibility alias differ")

text = canonical.decode("utf-8")
if not text.startswith("BEGIN:VCALENDAR\r\n") or not text.endswith("END:VCALENDAR\r\n"):
    fail("invalid VCALENDAR envelope")
if text.count("BEGIN:VEVENT") != len(events):
    fail("VEVENT count does not match events.json")

for line in text.split("\r\n"):
    if len(line.encode("utf-8")) > 75:
        fail(f"ICS line exceeds 75 octets: {line[:40]!r}")

print(
    json.dumps(
        {
            "events": len(events),
            "unique_uids": len(set(uids)),
            "rrules": sum(bool(event.get("rrule")) for event in events),
            "tentative": sum(event.get("status") == "TENTATIVE" for event in events),
            "canonical_bytes": len(canonical),
        },
        ensure_ascii=False,
        indent=2,
    )
)

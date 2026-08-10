# Calendar maintenance rules

- `events.json` is the only editable event source.
- Run `python generate_ics.py` after every event edit.
- The canonical public feed is `investment3_portfolio_watch_pdt.ics`; never rename it.
- Keep `calendar.ics` as an identical compatibility alias.
- Run `python scripts/validate_calendar.py` before publishing.
- Every event must have a stable, unique UID. Editing an event must not change its UID.
- Do not add portfolio quantities, costs, account values, private notes, credentials, or personal identifiers.
- Use primary sources when available. Label exchange appointment dates as `[预约披露]` and unconfirmed research windows as `[预计窗口]` or `[研究检查]`.
- Do not add airline, dividend bookkeeping, weekly oil inventory, or generic supply-chain placeholder events unless the portfolio thesis changes and the event becomes decision-relevant.
- Prefer one decision-rich recurring review over several low-value reminders.

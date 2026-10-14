---
title: "Support days"
labels: [enhancement]
---
## Problem

Durations longer than a day print as hours — `format_duration(90000)` is `"25h"` — and
`parse("1d")` is refused. Anything measured in days is awkward to read and impossible to type.

## Acceptance criteria

- [ ] `d` is a unit of 86400 seconds, larger than `h`: `parse("1d 2h") == 93600`.
- [ ] `format_duration(90000)` returns `"1d 1h"`.
- [ ] `format_duration(86400)` returns `"1d"`.
- [ ] `UNITS` lists `d` first, and the README's unit list names it.
- [ ] Every value in the existing round-trip test still round-trips.

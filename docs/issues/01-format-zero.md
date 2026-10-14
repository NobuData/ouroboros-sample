---
title: "format_duration(0) returns an empty string"
labels: [bug, good first issue]
---
## Problem

`format_duration(0)` returns `""`, because every component is zero and zero components are
left out. An empty string is not a duration: `python -m durations --format 0` prints a blank
line, and `parse(format_duration(0))` raises `ValueError`.

## Acceptance criteria

- [ ] `format_duration(0)` returns `"0s"`.
- [ ] `python -m durations --format 0` prints `0s`.
- [ ] `parse(format_duration(0)) == 0`, with a test.

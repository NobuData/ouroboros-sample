---
title: "Accept upper-case unit suffixes"
labels: [good first issue]
---
## Problem

`parse("1H 30M")` raises `ValueError`. People type durations the way they write them, and
upper-case suffixes are common in pasted text.

## Acceptance criteria

- [ ] `parse` accepts `H`, `M` and `S` as well as `h`, `m` and `s`, in any mix: `parse("1H 30m") == 5400`.
- [ ] `format_duration` still prints lower-case suffixes.
- [ ] The tests cover an all-upper-case and a mixed-case input.

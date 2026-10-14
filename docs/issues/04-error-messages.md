---
title: "Name the offending part of a bad duration in the error"
labels: [bug]
---
## Problem

`parse("1h 2x")` raises `ValueError: invalid duration: '1h 2x'`. The whole input is repeated
and the reader has to find the mistake themselves. On a long input the message says nothing
useful.

## Acceptance criteria

- [ ] The message names the first part that could not be read: `parse("1h 2x")` raises `ValueError` whose message contains `'2x'`.
- [ ] A number with no unit is named the same way: `parse("1h 2")` mentions `'2'`.
- [ ] A unit given twice still says so, naming the unit.
- [ ] `python -m durations` prints the new message and exits with status 2, as now.

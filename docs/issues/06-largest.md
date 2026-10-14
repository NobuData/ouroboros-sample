---
title: "Round format_duration to its largest units"
labels: [enhancement]
---
## Problem

`format_duration(7322)` is `"2h 2m 2s"`. A dashboard wants `"2h 2m"`: the two largest units,
rounded. Today a caller has to round the seconds themselves and gets it wrong at the edges.

## Acceptance criteria

- [ ] `format_duration(seconds, largest=n)` prints at most `n` units, starting from the largest non-zero one; `largest` defaults to all units, so existing calls are unchanged.
- [ ] The result is rounded to the smallest unit printed, halves rounding up: `format_duration(7322, largest=2) == "2h 2m"` and `format_duration(5430, largest=1) == "2h"`.
- [ ] Rounding carries into the next unit: `format_duration(3599, largest=1) == "1h"`, not `"60m"`; `format_duration(3570, largest=2) == "1h"`, not `"59m 60s"`.
- [ ] Zero components produced by rounding are left out: `format_duration(3601, largest=2) == "1h"`.
- [ ] `largest` below 1 raises `ValueError`.

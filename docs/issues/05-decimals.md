---
title: "Accept decimal amounts such as 1.5h"
labels: [enhancement]
---
## Problem

`parse("1.5h")` is refused, although "one and a half hours" is the most natural way to write
it. Durations are whole seconds, so a decimal amount has to be rounded somewhere.

## Acceptance criteria

- [ ] An amount may have a decimal part: `parse("1.5h") == 5400` and `parse("0.25m") == 15`.
- [ ] The total is rounded to the nearest whole second, **halves rounding up**: `parse("0.5s") == 1` and `parse("2.5s") == 3`.
- [ ] Rounding happens once, on the total: `parse("0.5s 0.5s")` is still refused as a repeated unit, and `parse("1.0004m 0.5s") == 61`.
- [ ] `parse(".5h")`, `parse("1.h")` and `parse("1..5h")` are refused.
- [ ] `format_duration` is unchanged.

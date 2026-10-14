---
title: "Total durations read from standard input"
labels: [enhancement]
---
## Problem

Adding up a column of durations from a log means a shell loop around the command line. The
command could read them itself.

## Acceptance criteria

- [ ] `python -m durations --sum` reads one duration per line from standard input and prints the total, formatted: `printf '1h\n30m\n' | python -m durations --sum` prints `1h 30m`.
- [ ] Blank lines are skipped.
- [ ] A line that cannot be read is reported on standard error with its line number, and the command exits with status 2 without printing a total.
- [ ] `--sum` and `--format` together are refused with a usage error.

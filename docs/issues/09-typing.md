---
title: "Ship type information"
labels: [chore]
---
## Problem

The package has type hints, but a type checker in a project that installs it treats every
name as `Any`, because the package does not say it is typed.

## Acceptance criteria

- [ ] The package includes a `py.typed` marker, and the built wheel contains it.
- [ ] A test asserts the marker is in the package directory.

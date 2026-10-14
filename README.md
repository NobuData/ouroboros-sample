# ouroboros-sample

The reference demonstration repository for [Ouroboros](https://ouroboros.build): a small, real
project with a build, a test suite and ten issues, kept public so that a run of the loop on it
can be checked by anybody. *That is the issue, that is the pull request the loop opened, that is
the build that judged it.*

It is a demonstration fixture, not a product. The code is deliberately small; the issues are
deliberately written the way Ouroboros reads issues.

## The project

`durations` parses and formats human-readable durations:

```python
>>> from durations import parse, format_duration
>>> parse("1h 30m")
5400
>>> format_duration(5400)
'1h 30m'
```

```
$ python -m durations 1h 30m
5400
$ python -m durations --format 5400
1h 30m
```

The units are `h`, `m` and `s`. It uses only the Python standard library; the tests use pytest.

### Build and test

```
make check
```

That is what a build runner runs. It needs `python3` (3.10 or later) and `make`; the first run
creates `.venv/` and installs pytest into it, and nothing outside this directory changes. From
a clean checkout it takes a few seconds.

| Target | Does |
| --- | --- |
| `make build` | byte-compiles the package and builds a wheel into `dist/` |
| `make test` | runs the test suite |
| `make check` | both |
| `make clean` | removes everything the others made |

## The issues

Ten issues, filed from [`docs/issues/`](docs/issues) by
[`scripts/file-issues.sh`](scripts/file-issues.sh). Each has a problem statement and an
**Acceptance criteria** section that Ouroboros imports as the pull request's checklist.

| # | Issue | Intended size | What it exercises |
| --- | --- | --- | --- |
| 1 | `format_duration(0)` returns an empty string | XS | a one-line fix with a test |
| 2 | Accept upper-case unit suffixes | XS | a small parser change |
| 3 | Support days | S | a new unit through parser, formatter and docs |
| 4 | Name the offending part of a bad duration in the error | S | error handling and the command line's exit status |
| 5 | Accept decimal amounts such as 1.5h | M | **a correction round** — Python's `round()` rounds halves to even, and the criteria ask for halves up |
| 6 | Round `format_duration` to its largest units | M | **a correction round** — rounding has to carry (`3599` is `1h`, not `60m`) |
| 7 | Add ISO 8601 output | S | a new public function |
| 8 | Total durations read from standard input | M | the command line, standard input and error reporting |
| 9 | Ship type information | XS | packaging |
| 10 | Make the output friendlier for international users | — | **should be declined**: it names no language, no wording and nothing checkable |

*Intended size* is the size of the work. Ouroboros's own estimate is separate and can differ: the
rule-based estimator (`heuristic-v0`) takes the largest of its signals, so an issue labelled
`enhancement` sizes as L whatever its length.

## Running the demonstration

What it takes to get from nothing to a state where a run can start. You need an Ouroboros
deployment you can sign in to as an Owner or Maintainer, a GitHub account, and a machine to use
as a build runner.

1. **Your own copy.** Use this repository as a template (**Use this template → Create a new
   repository**) or fork it, so the loop can push branches and open pull requests. In a
   template copy, file the issues: `scripts/file-issues.sh YOUR-ACCOUNT/YOUR-REPO` (needs `gh`).
   A fork does not copy issues either — run the same script against the fork.
2. **Tag the starting point**, so the repository can be reset later:
   `git tag demo-start && git push origin demo-start`.
3. **Connect GitHub** in Ouroboros (**Get Started**, step 1, or **Settings → Sources**) with a
   token that can read and write this repository, and enable the repository.
4. **Set the backlog token** under **Settings → Sources → Backlog token**, so the issues are
   mirrored and sized.
5. **Enrol a runner** in a pool named `pool-a` (**Build Farm → Enroll a runner**) on a machine
   with `python3` and `make`. Check it can build: on that machine, `make check` in a clone of
   your copy passes.
6. **Load the workflow** from [`.ouroboros/live-slice.loop.ts`](.ouroboros/live-slice.loop.ts) —
   see [`.ouroboros/README.md`](.ouroboros/README.md) — and publish it.
7. **Protect** `LICENSE` and `.ouroboros/**` (**Settings → Policies → Protected paths**).
8. **Route** the `plan` and `implement` tasks to a model alias with a working provider key
   (**Models**).

The issues should now be listed on the **Issues** page with their sizes, and queueing one starts
a `live-slice` run.

## Resetting

[`scripts/reset.sh`](scripts/reset.sh) returns the repository to where a run starts:

```
scripts/reset.sh YOUR-ACCOUNT/YOUR-REPO                  # close run PRs, delete run branches, reopen issues
scripts/reset.sh --restore-main YOUR-ACCOUNT/YOUR-REPO   # …and move main back to demo-start (asks first)
```

Run branches are those starting `ouro/run-` (set `OURO_RUN_BRANCH_PREFIX` to change it).
Comments a run left on issues stay, as the record of what happened.

## What is not here

No agent configuration: nothing under `.claude/`, no `AGENTS.md`, no editor settings that
steer a model. A run on this repository reflects Ouroboros, not instructions left for it.

## Licence

MIT — see [LICENSE](LICENSE).

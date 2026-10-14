# `.ouroboros/`

What Ouroboros needs to run the reference demonstration on this repository. Nothing here
changes how the code builds or tests.

## `live-slice.loop.ts`

The `live-slice` workflow, in Ouroboros's workflow code language: plan → implement → build →
gate → open a pull request. The build stage runs `make check` on a runner in the pool
`pool-a`; a failed build returns to implement once.

**Provisional.** The published `live-slice` workflow is built by
[DI.5 (#1314)](https://github.com/NobuData/ouroboros/issues/1314). This file was written from
that issue's specification and checked against Ouroboros's own parser and validator (it reads,
validates and prints back unchanged), but two parts of the specification are not yet in the
language and are approximated:

- **Implement** is an `llm` stage that may push to the run branch, not a harness session with
  file tools.
- **Open pull request** is the language's `openPr`, which arms auto-merge; the specification
  asks for a draft. Leave the repository's required checks in place so nothing merges unseen.

When DI.5 publishes `live-slice`, this file is replaced by its export.

To load it: in Ouroboros, open **Workflows**, create a workflow named `live-slice`, switch to the
**Code** view, paste this file, then **Validate** and **Publish**.

## Protected path

The demonstration protects `LICENSE` and `.ouroboros/**`: a run that touches either stops and
asks a person. Add both patterns under **Settings → Policies → Protected paths**, or on the
repository's detection card in **Get Started**.

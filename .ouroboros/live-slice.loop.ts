import { defineLoop, route, trigger, llm, infra, gate, openPr } from "@ouroboros/sdk";

export default defineLoop("live-slice", {
  dsl: "1.0",
  trigger: {
    on: "issue.queued",
  },
  stages: [
    trigger("issue-queued", {
      title: "Issue queued",
      description: "Runs when an issue of this repository reaches the queue.",
      next: "plan",
    }),
    llm("plan", {
      title: "Plan the change",
      description: "One call: reads the issue and names the files the change touches.",
      model: route.task("plan"),
      retries: 1,
      tokenBudget: 50_000,
      permissions: { pushFixup: false, touchCi: false },
      prompt: `Plan the change for this issue.

Issue: {{issue.title}}
Body:  {{issue.body}}

Name every file under src/ and tests/ the change touches, and the test you will add.`,
      next: "implement",
    }),
    llm("implement", {
      title: "Implement",
      description: "Writes the change and its test onto the run branch.",
      model: route.task("implement"),
      retries: 1,
      tokenBudget: 400_000,
      permissions: { pushFixup: true, touchCi: false },
      prompt: `Implement the plan.

Issue: {{issue.title}}
Plan:  {{plan}}

Change only what the plan names. Every acceptance criterion needs a test.`,
      next: "build",
    }),
    infra("build", {
      title: "Build and test",
      description: "Builds the wheel and runs the test suite on a farm runner.",
      farm: "pool-a",
      cmd: "make check",
      next: "gate",
    }),
    gate("gate", {
      title: "Build green?",
      description: "Opens the pull request when the build passed; a failure returns to implement.",
      require: ["build"],
      branches: [
        { to: "open-pr", when: (i) => i.checks.allPassed() },
      ],
      onFail: "implement",
    }), // the loop bites its tail
    openPr("open-pr", {
      title: "Open pull request",
      description: "Opens the pull request for a person to review.",
      merge: "squash",
      deleteBranch: true,
    }),
  ],
});

// Round-trips with the visual canvas: every node on the graph is one
// stage call above, and `onFail` is the declared back-edge that
// closes the loop. Publishing writes the next version for both editors.

// @ouroboros/layout v1 — generated; the canvas owns these lines
// node issue-queued 0 0
// node plan 240 0
// node implement 480 0
// node build 720 0
// node gate 960 0
// node open-pr 1200 0
// edge issue-queued plan
// edge plan implement
// edge implement build
// edge build gate
// edge gate open-pr
// edge gate implement "fail ↺"

const { RunGovernor } = require("./runGovernor")

const gov = new RunGovernor({
  maxSteps: 12,
  maxToolCalls: 10,
  maxLlmCalls: 8,
  maxCostUsd: 0.5,
  maxWallClockSeconds: 120,
  maxRetriesPerStep: 2,
  loopSignatureWindow: 5,
  loopThreshold: 3
})

gov.recordStep("search", "start search step")
gov.recordTool(
  "search",
  { query: "openclaw run governor" },
  0.01,
  "search",
  "search query executed"
)

gov.recordStep("summarize", "summarize results")
gov.recordLlmCall(
  "gpt-4o-mini",
  500,
  0.005,
  "summarize",
  "summary generated"
)

console.log(gov.summary())
console.log(gov.exportTrace())
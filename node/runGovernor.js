const crypto = require("crypto")

function stableStringify(value) {
  if (value === null || typeof value !== "object") {
    return JSON.stringify(value)
  }

  if (Array.isArray(value)) {
    return `[${value.map(stableStringify).join(",")}]`
  }

  const keys = Object.keys(value).sort()
  const items = keys.map((key) => `${JSON.stringify(key)}:${stableStringify(value[key])}`)
  return `{${items.join(",")}}`
}

class RunGovernor {
  constructor({
    maxSteps = 50,
    maxToolCalls = 25,
    maxLlmCalls = 25,
    maxCostUsd = 1.0,
    maxWallClockSeconds = 300,
    maxRetriesPerStep = 2,
    loopSignatureWindow = 5,
    loopThreshold = 3,
    runId = null
  } = {}) {
    this.runId = runId || crypto.randomUUID()

    this.maxSteps = maxSteps
    this.maxToolCalls = maxToolCalls
    this.maxLlmCalls = maxLlmCalls
    this.maxCostUsd = maxCostUsd
    this.maxWallClockSeconds = maxWallClockSeconds
    this.maxRetriesPerStep = maxRetriesPerStep
    this.loopSignatureWindow = loopSignatureWindow
    this.loopThreshold = loopThreshold

    this.stepCount = 0
    this.toolCalls = 0
    this.llmCalls = 0
    this.costUsd = 0
    this.startedAt = Date.now()
    this.retriesByStep = {}
    this.recentToolSignatures = []
    this.trace = []
  }

  now() {
    return Date.now() / 1000
  }

  checkTimeout() {
    const elapsedSeconds = this.now() - (this.startedAt / 1000)
    if (elapsedSeconds > this.maxWallClockSeconds) {
      throw new Error("wall clock time limit exceeded")
    }
  }

  checkBudget() {
    if (this.costUsd > this.maxCostUsd) {
      throw new Error("cost limit exceeded")
    }
  }

  makeToolSignature(toolName, args = {}) {
    const raw = `${toolName}:${stableStringify(args)}`
    return crypto.createHash("sha256").update(raw).digest("hex")
  }

  checkLoopGuard(signature) {
    this.recentToolSignatures.push(signature)
    this.recentToolSignatures = this.recentToolSignatures.slice(-this.loopSignatureWindow)

    const repeats = this.recentToolSignatures.filter((s) => s === signature).length
    if (repeats >= this.loopThreshold) {
      throw new Error("loop guard triggered")
    }
  }

  appendTrace(event) {
    this.trace.push({
      run_id: this.runId,
      ...event
    })
  }

  recordStep(stepName = "default_step", summary = "") {
    this.checkTimeout()
    this.stepCount += 1

    if (this.stepCount > this.maxSteps) {
      throw new Error("step limit exceeded")
    }

    this.appendTrace({
      event_type: "step",
      step_index: this.stepCount,
      step_name: stepName,
      timestamp: this.now(),
      status: "ok",
      summary
    })
  }

  recordTool(toolName, args = {}, costUsd = 0, stepName = "default_step", summary = "") {
    this.checkTimeout()
    this.toolCalls += 1

    if (this.toolCalls > this.maxToolCalls) {
      throw new Error("tool call limit exceeded")
    }

    this.costUsd += costUsd
    this.checkBudget()

    const signature = this.makeToolSignature(toolName, args)
    this.checkLoopGuard(signature)

    this.appendTrace({
      event_type: "tool_call",
      step_index: this.stepCount,
      step_name: stepName,
      tool: toolName,
      arguments: args,
      tool_signature_hash: signature,
      cost_usd: costUsd,
      timestamp: this.now(),
      status: "ok",
      summary
    })

    return signature
  }

  recordLlmCall(model, tokens = 0, costUsd = 0, stepName = "default_step", summary = "") {
    this.checkTimeout()
    this.llmCalls += 1

    if (this.llmCalls > this.maxLlmCalls) {
      throw new Error("llm call limit exceeded")
    }

    this.costUsd += costUsd
    this.checkBudget()

    this.appendTrace({
      event_type: "llm_call",
      step_index: this.stepCount,
      step_name: stepName,
      model,
      tokens,
      cost_usd: costUsd,
      timestamp: this.now(),
      status: "ok",
      summary
    })
  }

  recordRetry(stepName, summary = "") {
    this.retriesByStep[stepName] = (this.retriesByStep[stepName] || 0) + 1

    if (this.retriesByStep[stepName] > this.maxRetriesPerStep) {
      throw new Error(`retry limit exceeded for step: ${stepName}`)
    }

    this.appendTrace({
      event_type: "retry",
      step_index: this.stepCount,
      step_name: stepName,
      retry_count: this.retriesByStep[stepName],
      timestamp: this.now(),
      status: "ok",
      summary
    })
  }

  summary() {
    return {
      run_id: this.runId,
      step_count: this.stepCount,
      tool_calls: this.toolCalls,
      llm_calls: this.llmCalls,
      cost_usd: Number(this.costUsd.toFixed(6)),
      elapsed_seconds: Number((this.now() - (this.startedAt / 1000)).toFixed(3))
    }
  }

  exportTrace() {
    return this.trace
  }
}

module.exports = { RunGovernor }
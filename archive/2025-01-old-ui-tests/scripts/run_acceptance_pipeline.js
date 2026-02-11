#!/usr/bin/env node
/* eslint-disable no-console */
const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const ROOT = path.resolve(__dirname, "..");
const DEFAULT_CONFIG = path.join(ROOT, "config", "acceptance_pipeline.json");

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf-8"));
}

function ensureDirForFile(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function runCommand(commandText, cwd = ROOT) {
  const started = Date.now();
  const result = spawnSync(commandText, {
    cwd,
    shell: true,
    encoding: "utf-8",
    env: { ...process.env, PYTHONIOENCODING: "utf-8" }
  });
  return {
    commandText,
    exitCode: result.status === null ? 1 : result.status,
    durationMs: Date.now() - started,
    stdout: result.stdout || "",
    stderr: result.stderr || ""
  };
}

function parsePytest(stdout) {
  const text = stdout || "";
  const summary = { passed: 0, failed: 0, skipped: 0, errors: 0 };
  const matched = text.match(/(\d+)\s+passed/);
  if (matched) summary.passed = Number(matched[1]);
  const failed = text.match(/(\d+)\s+failed/);
  if (failed) summary.failed = Number(failed[1]);
  const skipped = text.match(/(\d+)\s+skipped/);
  if (skipped) summary.skipped = Number(skipped[1]);
  const errors = text.match(/(\d+)\s+error/);
  if (errors) summary.errors = Number(errors[1]);
  return summary;
}

function parsePytestCaseLines(stdout) {
  const lines = (stdout || "").split(/\r?\n/);
  const results = [];
  for (const line of lines) {
    const m = line.match(/(api_tests\/[^\s]+::[^\s]+)\s+(PASSED|FAILED|ERROR|SKIPPED)/);
    if (!m) continue;
    const statusMap = {
      PASSED: "passed",
      FAILED: "failed",
      ERROR: "blocked",
      SKIPPED: "blocked"
    };
    results.push({
      id: m[1],
      name: m[1],
      stage: "api_core",
      status: statusMap[m[2]] || "blocked",
      note: null
    });
  }
  return results;
}

function normalizeStatusCounts(items) {
  const out = { passed: 0, failed: 0, blocked: 0 };
  for (const item of items) {
    if (item.status === "passed") out.passed += 1;
    else if (item.status === "failed") out.failed += 1;
    else out.blocked += 1;
  }
  return out;
}

function runApiStage(cfg) {
  const stage = {
    enabled: cfg.apiCore.enabled,
    attempted: false,
    command: null,
    exitCode: null,
    durationMs: 0,
    summary: null,
    rawLog: null
  };
  if (!cfg.apiCore.enabled) return stage;

  const baseArgs = cfg.apiCore.command.join(" ");
  for (const py of cfg.apiCore.pythonCandidates || []) {
    const cmd = `${py} ${baseArgs}`.trim();
    const res = runCommand(cmd);
    stage.attempted = true;
    stage.command = cmd;
    stage.exitCode = res.exitCode;
    stage.durationMs = res.durationMs;
    stage.rawLog = `STDOUT:\n${res.stdout}\n\nSTDERR:\n${res.stderr}`;
    stage.summary = parsePytest(res.stdout);
    stage.caseResults = parsePytestCaseLines(res.stdout);
    if (res.exitCode !== 127) {
      return stage;
    }
  }
  return stage;
}

function runUiStage(cfg) {
  const stage = {
    enabled: cfg.uiSmoke.enabled,
    attempted: false,
    command: null,
    exitCode: null,
    durationMs: 0,
    summary: null,
    reportFile: null
  };
  if (!cfg.uiSmoke.enabled) return stage;

  const cmd = cfg.uiSmoke.command.join(" ");
  const res = runCommand(cmd);
  stage.attempted = true;
  stage.command = cmd;
  stage.exitCode = res.exitCode;
  stage.durationMs = res.durationMs;

  const uiPlan = readJson(path.join(ROOT, cfg.uiSmoke.planFile));
  const uiReportFile = path.join(ROOT, uiPlan.runner?.resultFile || "test-results/ui-smoke-results.json");
  stage.reportFile = path.relative(ROOT, uiReportFile).replace(/\\/g, "/");
  if (fs.existsSync(uiReportFile)) {
    stage.summary = readJson(uiReportFile).summary;
    stage.caseResults = (readJson(uiReportFile).results || []).map((r) => ({
      id: r.caseId,
      name: r.name,
      stage: "ui_smoke",
      status: r.status,
      note: r.reason || null
    }));
  } else {
    stage.summary = { total: 0, passed: 0, blocked: 0, failed: 0 };
    stage.caseResults = [];
  }
  stage.rawLog = `STDOUT:\n${res.stdout}\n\nSTDERR:\n${res.stderr}`;
  return stage;
}

function buildSummary(apiStage, uiStage, startedAt) {
  const all = [...(apiStage.caseResults || []), ...(uiStage.caseResults || [])];
  const counts = normalizeStatusCounts(all);
  return {
    total: all.length,
    passed: counts.passed,
    failed: counts.failed,
    blocked: counts.blocked,
    executed: all.length,
    pending: 0,
    startedAt,
    endedAt: new Date().toISOString()
  };
}

function writeMarkdownReport(cfg, result) {
  const lines = [
    "# 验收流程执行报告",
    "",
    `- 计划ID: ${cfg.planId}`,
    `- 计划URL: ${cfg.planUrl}`,
    `- 执行时间: ${result.executedAt}`,
    `- 策略: API优先 + UI冒烟`,
    "",
    "## 汇总",
    "",
    `- 总执行项: ${result.summary.total}`,
    `- 通过: ${result.summary.passed}`,
    `- 失败: ${result.summary.failed}`,
    `- 阻塞: ${result.summary.blocked}`,
    "",
    "## 分阶段",
    "",
    `- API核心: exit=${result.stages.apiCore.exitCode}, passed=${result.stages.apiCore.summary?.passed ?? 0}, failed=${result.stages.apiCore.summary?.failed ?? 0}`,
    `- UI冒烟: exit=${result.stages.uiSmoke.exitCode}, passed=${result.stages.uiSmoke.summary?.passed ?? 0}, blocked=${result.stages.uiSmoke.summary?.blocked ?? 0}`,
    "",
    "## 结果明细",
    ""
  ];
  for (const item of result.results) {
    lines.push(`- [${item.stage}] ${item.id} - ${item.status}${item.note ? ` (${item.note})` : ""}`);
  }
  const out = path.join(ROOT, cfg.outputs.summaryMarkdownFile);
  ensureDirForFile(out);
  fs.writeFileSync(out, `${lines.join("\n")}\n`, "utf-8");
}

function main() {
  const configArg = process.argv.find((x) => x.startsWith("--config="));
  const cfgPath = configArg ? path.resolve(ROOT, configArg.split("=")[1]) : DEFAULT_CONFIG;
  const cfg = readJson(cfgPath);
  const startedAt = new Date().toISOString();

  console.log(`[PIPELINE] start ${startedAt}`);
  const apiStage = runApiStage(cfg);
  console.log(`[PIPELINE] api stage done, exit=${apiStage.exitCode}`);

  let uiStage = {
    enabled: false,
    attempted: false,
    command: null,
    exitCode: null,
    durationMs: 0,
    summary: { total: 0, passed: 0, failed: 0, blocked: 0 },
    caseResults: []
  };

  const shouldRunUi = cfg.executionPolicy.includeUiSmoke && (
    !cfg.executionPolicy.stopOnApiFailure || apiStage.exitCode === 0
  );

  if (shouldRunUi) {
    uiStage = runUiStage(cfg);
    console.log(`[PIPELINE] ui stage done, exit=${uiStage.exitCode}`);
  } else {
    console.log("[PIPELINE] skip ui stage due to policy");
  }

  const result = {
    planId: cfg.planId,
    planUrl: cfg.planUrl,
    strategy: "api-first-with-ui-smoke",
    executedAt: startedAt,
    updatedAt: new Date().toISOString(),
    syncToTapdDone: false,
    stages: {
      apiCore: apiStage,
      uiSmoke: uiStage
    },
    results: [...(apiStage.caseResults || []), ...(uiStage.caseResults || [])],
    summary: buildSummary(apiStage, uiStage, startedAt)
  };

  const outMain = path.join(ROOT, cfg.outputs.pipelineResultFile);
  ensureDirForFile(outMain);
  fs.writeFileSync(outMain, JSON.stringify(result, null, 2), "utf-8");

  const outJson = path.join(ROOT, cfg.outputs.summaryJsonFile);
  ensureDirForFile(outJson);
  fs.writeFileSync(outJson, JSON.stringify(result, null, 2), "utf-8");

  writeMarkdownReport(cfg, result);
  console.log(`[PIPELINE] report written to ${cfg.outputs.pipelineResultFile}`);

  if ((apiStage.exitCode && apiStage.exitCode !== 0) || (uiStage.exitCode && uiStage.exitCode !== 0)) {
    process.exitCode = 1;
  }
}

main();

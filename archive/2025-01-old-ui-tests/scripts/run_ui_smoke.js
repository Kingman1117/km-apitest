#!/usr/bin/env node
/* eslint-disable no-console */
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const DEFAULT_PLAN_PATH = path.join(ROOT, "config", "ui_smoke_plan.json");
const CASE_INDEX_PATH = path.join(ROOT, "case_scripts", "index.json");

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf-8"));
}

function ensureDirForFile(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function isoWeek(date = new Date()) {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  const dayNum = d.getUTCDay() || 7;
  d.setUTCDate(d.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
}

function selectRotationCases(pool, count) {
  if (!Array.isArray(pool) || pool.length === 0 || count <= 0) return [];
  const week = isoWeek();
  const start = week % pool.length;
  const selected = [];
  for (let i = 0; i < Math.min(count, pool.length); i += 1) {
    selected.push(pool[(start + i) % pool.length]);
  }
  return selected;
}

function buildCaseScriptPath(group, caseId) {
  return path.join(ROOT, "case_scripts", group, `${caseId}.json`);
}

async function clickWithFallbacks(page, step, timeout) {
  const selectors = [step.selector, ...(step.fallbacks || [])].filter(Boolean);
  let lastErr = null;
  for (const selector of selectors) {
    try {
      const loc = page.locator(selector).first();
      await loc.waitFor({ state: "visible", timeout });
      await loc.click({ force: Boolean(step.force) });
      return selector;
    } catch (err) {
      lastErr = err;
    }
  }
  throw new Error(`click failed, selectors=${selectors.join(" | ")}, err=${lastErr ? lastErr.message : "unknown"}`);
}

async function fillWithFallbacks(page, step, timeout) {
  const selectors = [step.selector, ...(step.fallbacks || [])].filter(Boolean);
  let lastErr = null;
  const value = String(step.value || "").replace("{timestamp}", String(Date.now()).slice(-8));
  for (const selector of selectors) {
    try {
      const loc = page.locator(selector).first();
      await loc.waitFor({ state: "visible", timeout });
      await loc.fill(value);
      return { selector, value };
    } catch (err) {
      lastErr = err;
    }
  }
  throw new Error(`fill failed, selectors=${selectors.join(" | ")}, err=${lastErr ? lastErr.message : "unknown"}`);
}

async function runStep(page, step, timeout) {
  switch (step.action) {
    case "goto":
      await page.goto(step.url, { waitUntil: "domcontentloaded", timeout: 30000 });
      return `goto ${step.url}`;
    case "wait":
      await page.waitForTimeout(Number(step.ms || 500));
      return `wait ${step.ms || 500}ms`;
    case "click": {
      const used = await clickWithFallbacks(page, step, timeout);
      return `click ${used}`;
    }
    case "fill": {
      const used = await fillWithFallbacks(page, step, timeout);
      return `fill ${used.selector}`;
    }
    case "evaluate":
      await page.evaluate(step.script);
      return "evaluate script";
    case "verify": {
      const text = await page.locator("body").innerText().catch(() => "");
      const re = new RegExp(step.expect || "", "i");
      if (!re.test(text)) {
        throw new Error(`verify failed, regex=${step.expect}`);
      }
      return `verify ${step.expect}`;
    }
    default:
      throw new Error(`unsupported action: ${step.action}`);
  }
}

async function runCase(page, entry, runnerConfig) {
  const startedAt = new Date().toISOString();
  const casePath = buildCaseScriptPath(entry.group, entry.caseId);
  const result = {
    caseId: entry.caseId,
    group: entry.group,
    name: entry.name,
    path: path.relative(ROOT, casePath).replace(/\\/g, "/"),
    startedAt,
    endedAt: null,
    status: "blocked",
    reason: null,
    steps: []
  };

  try {
    const script = readJson(casePath);
    for (const step of script.steps || []) {
      const desc = await runStep(page, step, runnerConfig.defaultTimeoutMs || 15000);
      result.steps.push({ action: step.action, ok: true, detail: desc });
    }
    result.status = "passed";
  } catch (err) {
    result.reason = err.message;
    if (runnerConfig.snapshotOnFailureOnly) {
      const name = `${entry.caseId}-${Date.now()}-failed.png`;
      const out = path.join(ROOT, "test-results", "ui-smoke-screenshots", name);
      fs.mkdirSync(path.dirname(out), { recursive: true });
      await page.screenshot({ path: out, fullPage: true }).catch(() => {});
      result.screenshot = path.relative(ROOT, out).replace(/\\/g, "/");
    }
  } finally {
    result.endedAt = new Date().toISOString();
  }

  return result;
}

function summarize(results) {
  const summary = { total: results.length, passed: 0, blocked: 0, failed: 0 };
  for (const r of results) {
    if (r.status === "passed") summary.passed += 1;
    else if (r.status === "failed") summary.failed += 1;
    else summary.blocked += 1;
  }
  return summary;
}

async function main() {
  const planArg = process.argv.find((x) => x.startsWith("--plan="));
  const planPath = planArg ? path.resolve(ROOT, planArg.split("=")[1]) : DEFAULT_PLAN_PATH;
  const smokePlan = readJson(planPath);
  const caseIndex = readJson(CASE_INDEX_PATH);

  const fixedCases = smokePlan.fixedCases || [];
  const rotateCases = selectRotationCases(
    smokePlan.rotation?.pool || [],
    Number(smokePlan.rotation?.weeklyCount || 0)
  );
  const allCases = [...fixedCases, ...rotateCases];

  const caseIdsInPlan = new Set();
  for (const group of caseIndex.groups || []) {
    for (const caseId of group.caseIds || []) {
      caseIdsInPlan.add(caseId);
    }
  }
  const executableCases = allCases.filter((c) => caseIdsInPlan.has(c.caseId));

  const browser = await chromium.launch({ headless: Boolean(smokePlan.runner?.headless ?? true) });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 }
  });
  context.setDefaultTimeout(Number(smokePlan.runner?.defaultTimeoutMs || 15000));
  context.setDefaultNavigationTimeout(Number(smokePlan.runner?.navigationTimeoutMs || 30000));

  const page = await context.newPage();
  const results = [];
  for (const item of executableCases) {
    console.log(`[UI-SMOKE] Running ${item.caseId} ${item.name}`);
    const caseResult = await runCase(page, item, smokePlan.runner || {});
    results.push(caseResult);
    console.log(`[UI-SMOKE] ${item.caseId} => ${caseResult.status}`);
  }

  await context.close();
  await browser.close();

  const report = {
    profile: "fixed-plus-rotation",
    generatedAt: new Date().toISOString(),
    fixedCount: fixedCases.length,
    rotatedCount: rotateCases.length,
    selectedCases: executableCases.map((c) => c.caseId),
    summary: summarize(results),
    results
  };

  const reportFile = path.join(ROOT, smokePlan.runner?.resultFile || "test-results/ui-smoke-results.json");
  ensureDirForFile(reportFile);
  fs.writeFileSync(reportFile, JSON.stringify(report, null, 2), "utf-8");
  console.log(`[UI-SMOKE] report written: ${path.relative(ROOT, reportFile)}`);

  if (report.summary.blocked > 0 || report.summary.failed > 0) {
    process.exitCode = 1;
  }
}

main().catch((err) => {
  console.error("[UI-SMOKE] fatal error", err);
  process.exit(1);
});

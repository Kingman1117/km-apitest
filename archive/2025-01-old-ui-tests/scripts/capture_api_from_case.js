#!/usr/bin/env node
/* eslint-disable no-console */
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");

const ROOT = path.resolve(__dirname, "..");
const CASE_INDEX_PATH = path.join(ROOT, "case_scripts", "index.json");

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf-8"));
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function parseArgs() {
  const args = {};
  for (const raw of process.argv.slice(2)) {
    if (raw.startsWith("--")) {
      const [k, v = ""] = raw.slice(2).split("=");
      args[k] = v || true;
    }
  }
  return args;
}

function maskUrl(url) {
  return url
    .replace(/([?&])_TOKEN=[^&]+/i, "$1_TOKEN={token}")
    .replace(/([?&])wxappAid=[^&]+/i, "$1wxappAid={wxappAid}")
    .replace(/([?&])wxappId=[^&]+/i, "$1wxappId={wxappId}");
}

function maskValue(value) {
  if (typeof value !== "string") return value;
  // Replace long digit sequences with {timestamp}
  return value.replace(/\d{6,}/g, "{timestamp}");
}

function maskObject(obj) {
  if (Array.isArray(obj)) return obj.map(maskObject);
  if (obj && typeof obj === "object") {
    const out = {};
    for (const [k, v] of Object.entries(obj)) {
      out[k] = maskObject(v);
    }
    return out;
  }
  return maskValue(obj);
}

function parseRequestBody(postData, headers) {
  if (!postData) return null;
  const contentType = (headers["content-type"] || headers["Content-Type"] || "").toLowerCase();
  if (contentType.includes("application/json")) {
    try {
      return JSON.parse(postData);
    } catch {
      return postData;
    }
  }
  if (contentType.includes("application/x-www-form-urlencoded")) {
    const params = new URLSearchParams(postData);
    const out = {};
    for (const [k, v] of params.entries()) {
      out[k] = v;
    }
    return out;
  }
  return postData;
}

function findGroupByCaseId(caseId) {
  const index = readJson(CASE_INDEX_PATH);
  for (const group of index.groups || []) {
    if ((group.caseIds || []).includes(caseId)) {
      return group.dir;
    }
  }
  return null;
}

function buildCaseScriptPath(group, caseId) {
  return path.join(ROOT, "case_scripts", group, `${caseId}.json`);
}

async function runStep(page, step, timeout) {
  switch (step.action) {
    case "goto":
      await page.goto(step.url, { waitUntil: "domcontentloaded", timeout: 30000 });
      return;
    case "wait":
      await page.waitForTimeout(Number(step.ms || 500));
      return;
    case "click": {
      const selectors = [step.selector, ...(step.fallbacks || [])].filter(Boolean);
      for (const selector of selectors) {
        try {
          const loc = page.locator(selector).first();
          await loc.waitFor({ state: "visible", timeout });
          await loc.click({ force: Boolean(step.force) });
          return;
        } catch {
          continue;
        }
      }
      throw new Error(`click failed: ${selectors.join(" | ")}`);
    }
    case "fill": {
      const selectors = [step.selector, ...(step.fallbacks || [])].filter(Boolean);
      const value = String(step.value || "").replace("{timestamp}", String(Date.now()).slice(-8));
      for (const selector of selectors) {
        try {
          const loc = page.locator(selector).first();
          await loc.waitFor({ state: "visible", timeout });
          await loc.fill(value);
          return;
        } catch {
          continue;
        }
      }
      throw new Error(`fill failed: ${selectors.join(" | ")}`);
    }
    case "evaluate":
      await page.evaluate(step.script);
      return;
    case "verify":
      return;
    default:
      throw new Error(`unsupported action: ${step.action}`);
  }
}

async function capture(caseId, group, options) {
  const casePath = buildCaseScriptPath(group, caseId);
  const script = readJson(casePath);
  const captureList = [];

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1280, height: 720 } });
  context.setDefaultTimeout(15000);
  context.setDefaultNavigationTimeout(30000);
  const page = await context.newPage();

  page.on("response", async (response) => {
    try {
      const req = response.request();
      const url = response.url();
      if (!url.includes("/ajax/")) return;
      const method = req.method();
      const reqHeaders = req.headers();
      const reqBodyRaw = parseRequestBody(req.postData(), reqHeaders);
      let respBody = null;
      try {
        respBody = await response.json();
      } catch {
        respBody = null;
      }
      captureList.push({
        method,
        url: maskUrl(url),
        headers: reqHeaders,
        requestBody: maskObject(reqBodyRaw),
        responseStatus: response.status(),
        responseBody: respBody
      });
    } catch {
      // ignore capture errors
    }
  });

  try {
    for (const step of script.steps || []) {
      await runStep(page, step, 15000);
    }
  } finally {
    await context.close();
    await browser.close();
  }

  const keyApi =
    captureList.find((c) => c.method === "POST" && c.responseBody && c.responseBody.success === true) ||
    captureList.find((c) => c.method === "POST") ||
    captureList[0] ||
    null;

  const verifyApi =
    captureList.find((c) => c.method === "GET" && c.responseBody && c.responseBody.success === true) ||
    null;

  const output = {
    caseId,
    caseName: script.name,
    captureTime: new Date().toISOString(),
    keyApi,
    verifyApi,
    allApis: captureList
  };

  const outDir = path.join(ROOT, "api_captures");
  ensureDir(outDir);
  const outPath = path.join(outDir, `${caseId}.json`);
  fs.writeFileSync(outPath, JSON.stringify(output, null, 2), "utf-8");
  return outPath;
}

async function main() {
  const args = parseArgs();
  const caseId = args.caseId || args.case || "";
  let group = args.group || "";
  if (!caseId) {
    console.error("Usage: node scripts/capture_api_from_case.js --caseId=xxxx [--group=admin]");
    process.exit(1);
  }
  if (!group) {
    group = findGroupByCaseId(caseId);
  }
  if (!group) {
    console.error(`Cannot find group for caseId ${caseId}`);
    process.exit(1);
  }
  const outPath = await capture(caseId, group, args);
  console.log(`[CAPTURE] saved: ${path.relative(ROOT, outPath)}`);
}

main().catch((err) => {
  console.error("[CAPTURE] fatal error", err);
  process.exit(1);
});

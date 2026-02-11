#!/usr/bin/env node
/* eslint-disable no-console */
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const CACHE_PATH = path.join(ROOT, "case_details_cache.json");
const INDEX_PATH = path.join(ROOT, "case_scripts", "index.json");
const MAPPING_PATH = path.join(ROOT, "config", "case_api_mapping.json");
const CAPTURE_DIR = path.join(ROOT, "api_captures");

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf-8"));
}

function ensureDirForFile(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function findGroupByCaseId(caseId, indexData) {
  for (const group of indexData.groups || []) {
    if ((group.caseIds || []).includes(caseId)) return group.dir;
  }
  return null;
}

function hasCapture(caseId) {
  return fs.existsSync(path.join(CAPTURE_DIR, `${caseId}.json`));
}

function main() {
  const cache = readJson(CACHE_PATH);
  const indexData = readJson(INDEX_PATH);
  const existing = fs.existsSync(MAPPING_PATH) ? readJson(MAPPING_PATH) : { version: "1.0", cases: [] };
  const byId = new Map(existing.cases.map((c) => [c.caseId, c]));

  const merged = [];
  for (const item of cache) {
    const caseId = item.id;
    const existingItem = byId.get(caseId) || {};
    const group = existingItem.group || findGroupByCaseId(caseId, indexData) || "unknown";
    const captured = hasCapture(caseId);
    const status = captured ? "ready" : (existingItem.status || "planned");

    merged.push({
      caseId,
      name: item.name,
      group,
      status,
      apiTestFile: status === "ready" ? "api_tests/test_api_capture_replay.py" : (existingItem.apiTestFile || null),
      actionApi: existingItem.actionApi || null,
      verifyApi: existingItem.verifyApi || null
    });
  }

  const out = {
    version: existing.version || "1.0",
    description: "Case-to-API mapping for core acceptance. status=ready means capture exists and replay is enabled.",
    cases: merged
  };

  ensureDirForFile(MAPPING_PATH);
  fs.writeFileSync(MAPPING_PATH, JSON.stringify(out, null, 2), "utf-8");
  console.log(`[SYNC] mapping updated: ${path.relative(ROOT, MAPPING_PATH)}`);
}

main();

#!/usr/bin/env node
/* eslint-disable no-console */
const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const ROOT = path.resolve(__dirname, "..");
const INDEX_PATH = path.join(ROOT, "case_scripts", "index.json");

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf-8"));
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

function runCapture(caseId, group) {
  const cmd = `node scripts/capture_api_from_case.js --caseId=${caseId} --group=${group}`;
  const res = spawnSync(cmd, { cwd: ROOT, shell: true, stdio: "inherit" });
  return res.status === 0;
}

function main() {
  const args = parseArgs();
  const groupsArg = args.group || args.groups || "";
  if (!groupsArg) {
    console.error("Usage: node scripts/capture_api_from_group.js --group=admin[,h5]");
    process.exit(1);
  }

  const targetGroups = groupsArg.split(",").map((g) => g.trim()).filter(Boolean);
  const index = readJson(INDEX_PATH);

  for (const group of index.groups || []) {
    if (!targetGroups.includes(group.dir) && !targetGroups.includes(group.name)) continue;
    console.log(`[CAPTURE] group ${group.dir}`);
    for (const caseId of group.caseIds || []) {
      console.log(`[CAPTURE] case ${caseId}`);
      const ok = runCapture(caseId, group.dir);
      if (!ok) {
        console.error(`[CAPTURE] failed case ${caseId}, continue`);
      }
    }
  }
}

main();

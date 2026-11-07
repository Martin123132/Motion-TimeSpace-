"use strict";
const fs = require("node:fs");
const crypto = require("node:crypto");
const path = require("node:path");
const data = JSON.parse(fs.readFileSync(0, "utf8").replace(/^\uFEFF/, ""));
const result = require("./wave.cjs").run(data.profiles, data.massEV);
result.inputs = data.inputs;
result.sha256 = data.sha256;
result.code = Object.fromEntries(["wave.cjs", "inputs.ps1", "PROTOCOL.md"].map(name =>
  [name, crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname, name))).digest("hex")]));
process.stdout.write(JSON.stringify(result, null, 2) + "\n");

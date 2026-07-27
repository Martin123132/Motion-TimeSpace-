from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3896"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3896-Y5-R2FR-memory-suppression-runner-and-first-local-bound-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3896_SOURCE_REGISTER.csv",
    "schema": SRC / "P8_Y5_R2FR_3896_MEMORY_SUPPRESSION_INPUT_SCHEMA.csv",
    "inputs": SRC / "P8_Y5_R2FR_3896_MEMORY_SUPPRESSION_INPUT_ROWS_NONCLAIM.csv",
    "bounds": SRC / "P8_Y5_R2FR_3896_LOCAL_BOUND_ANCHOR_ROWS.csv",
    "runner": SRC / "P8_Y5_R2FR_3896_MEMORY_SUPPRESSION_RUNNER_DRYRUN.csv",
    "gate": SRC / "P8_Y5_R2FR_3896_LOCAL_GR_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3896_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3896_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3896_VALIDATION.csv",
}

BOUND_SOURCE = SRC / "P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_FINITE_RESIDUAL_BOUND_PACK.csv"
MEMORY_BOUND = "X_static_bound=(J_open_plus_B_lift)/(a_min*C_P_over_L_D2+m_min2)"
HISTORY_BOUND = "X_dynamic_bound=exp(-gamma_mem_Delta_t)*X_initial+(1-exp(-gamma_mem_Delta_t))*X_static_bound"
ARENA_BOUND = "DeltaO_i_bound=K_i*X_dynamic_bound+K_i_grad*gradX_bound"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    return str(path.relative_to(PCW)) if path.is_relative_to(PCW) else str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.startswith("MISSING") or text in {"NA", "None"}:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3896_00_next", SRC / "P8_Y5_R2FR_3895_NEXT_TARGET.csv", "NEXT3895_0", "3895 selected executable suppression runner"),
        ("SRC3896_01_law", SRC / "P8_Y5_R2FR_3895_MEMORY_SUPPRESSION_LAW.csv", "LAW3895_2_static_amplitude", "3895 static memory suppression law"),
        ("SRC3896_02_numeric", SRC / "P8_Y5_R2FR_3895_FIRST_NUMERIC_MEMORY_ROW_INTERFACE.csv", "NUM3895_0_a_min", "3895 numeric row interface"),
        ("SRC3896_03_gate", SRC / "P8_Y5_R2FR_3895_LOCAL_GR_DECISION_GATE.csv", "LGG3895_4_local_GR", "3895 no-claim local-GR gate"),
        ("SRC3896_04_validation", SRC / "P8_Y5_BRR545_3895_VALIDATION.csv", "VAL3895_15_next_target", "3895 validation"),
        ("SRC3896_05_bound_pack", BOUND_SOURCE, "417 pressure anchors only", "existing local pressure-bound anchor row"),
        ("SRC3896_06_status", SRC / "P8_Y5_R2FR_3895_STATUS.csv", "PASS_MEMORY_ZERO_PARTIAL_SUPPRESSION_LAW_DERIVED", "3895 status"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        found = exists and needle in read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": found,
                "role": role,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def schema_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"field": "a_min", "role": "principal-symbol lower bound", "units": "dimensionless after normalization", "required": True, "claim_gate": "must be parent-signed positive", "timestamp_utc": timestamp},
        {"field": "C_P_over_L_D2", "role": "Poincare/domain eigenvalue lower bound", "units": "1/length^2", "required": True, "claim_gate": "must be sourced by local matching domain", "timestamp_utc": timestamp},
        {"field": "m_min2", "role": "memory mass/gap lower bound", "units": "1/length^2", "required": True, "claim_gate": "must be parent-derived or zero-mode removed", "timestamp_utc": timestamp},
        {"field": "J_open_plus_B_lift", "role": "remaining wall/boundary/history source norm", "units": "operator-normalized source", "required": True, "claim_gate": "must sum real component norms with no cancellation credit", "timestamp_utc": timestamp},
        {"field": "gamma_mem_Delta_t", "role": "history suppression exponent", "units": "dimensionless", "required": True, "claim_gate": "must come from retarded kernel/local matching interval", "timestamp_utc": timestamp},
        {"field": "X_initial", "role": "incoming memory amplitude", "units": "X units", "required": True, "claim_gate": "zero only if no-incoming-memory clause is signed", "timestamp_utc": timestamp},
        {"field": "gradX_bound", "role": "gradient memory bound", "units": "X/length", "required": False, "claim_gate": "needed for gradient-sensitive arenas", "timestamp_utc": timestamp},
        {"field": "K_i", "role": "observable derivative with respect to X_mem", "units": "arena units per X", "required": True, "claim_gate": "must be differentiated from readout map", "timestamp_utc": timestamp},
        {"field": "K_i_grad", "role": "observable derivative with respect to grad X_mem", "units": "arena units per X/length", "required": False, "claim_gate": "must be differentiated from readout map", "timestamp_utc": timestamp},
    ]


def input_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "LIVE3896_placeholder",
            "case_type": "live_candidate",
            "arena": "all",
            "a_min": "MISSING_PARENT_SIGN",
            "C_P_over_L_D2": "MISSING_DOMAIN_SCALE",
            "m_min2": "MISSING_MEMORY_GAP",
            "J_open_plus_B_lift": "MISSING_SOURCE_NORM",
            "gamma_mem_Delta_t": "MISSING_HISTORY_KERNEL",
            "X_initial": "MISSING_INCOMING_MEMORY",
            "gradX_bound": "MISSING_GRAD_BOUND",
            "K_i": "MISSING_ARENA_DERIVATIVE",
            "K_i_grad": "MISSING_GRAD_ARENA_DERIVATIVE",
            "bound_to_compare": "MISSING_BOUND_SELECTION",
            "is_real_mts_input": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "DRY3896_unit_pass",
            "case_type": "artificial_arithmetic_check",
            "arena": "alpha3",
            "a_min": 1.0,
            "C_P_over_L_D2": 1.0,
            "m_min2": 0.0,
            "J_open_plus_B_lift": 1.0e-25,
            "gamma_mem_Delta_t": 5.0,
            "X_initial": 0.0,
            "gradX_bound": 0.0,
            "K_i": 1.0,
            "K_i_grad": 0.0,
            "bound_to_compare": 4.0e-20,
            "is_real_mts_input": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "DRY3896_gap_fail",
            "case_type": "artificial_failure_check",
            "arena": "alpha3",
            "a_min": 0.0,
            "C_P_over_L_D2": 0.0,
            "m_min2": 0.0,
            "J_open_plus_B_lift": 1.0e-25,
            "gamma_mem_Delta_t": 1.0,
            "X_initial": 0.0,
            "gradX_bound": 0.0,
            "K_i": 1.0,
            "K_i_grad": 0.0,
            "bound_to_compare": 4.0e-20,
            "is_real_mts_input": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_anchor_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"bound_id": "BND3896_0_alpha3", "arena": "PPN/preferred-frame", "observable": "alpha3", "bound_value": 4.0e-20, "units": "dimensionless", "comparison": "abs(predicted_alpha3) <= bound_value", "source_path": rel(BOUND_SOURCE), "source_basis": "2627 finite residual pack / 417 pressure anchor", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"bound_id": "BND3896_1_Gdot", "arena": "clock/orbital/local-G drift", "observable": "abs(Gdot/G)", "bound_value": 9.6e-15, "units": "yr^-1", "comparison": "abs(predicted_Gdot_over_G) <= bound_value", "source_path": rel(BOUND_SOURCE), "source_basis": "2627 finite residual pack / 417 pressure anchor", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"bound_id": "BND3896_2_alpha2", "arena": "PPN/preferred-frame", "observable": "alpha2", "bound_value": 2.0e-9, "units": "dimensionless", "comparison": "abs(predicted_alpha2) <= bound_value", "source_path": rel(BOUND_SOURCE), "source_basis": "2627 finite residual pack / 417 pressure anchor", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"bound_id": "BND3896_3_xi", "arena": "PPN/preferred-location", "observable": "xi", "bound_value": 4.0e-9, "units": "dimensionless", "comparison": "abs(predicted_xi) <= bound_value", "source_path": rel(BOUND_SOURCE), "source_basis": "2627 finite residual pack / 417 pressure anchor", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"bound_id": "BND3896_4_gamma", "arena": "PPN/R10 gamma-scale", "observable": "abs(gamma-1)", "bound_value": 2.3e-5, "units": "dimensionless", "comparison": "abs(predicted_gamma_minus_one) <= bound_value", "source_path": rel(BOUND_SOURCE), "source_basis": "2627 finite residual pack / 417 pressure anchor", "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def evaluate_case(row: dict[str, Any], timestamp: str) -> dict[str, Any]:
    required = ["a_min", "C_P_over_L_D2", "m_min2", "J_open_plus_B_lift", "gamma_mem_Delta_t", "X_initial", "K_i", "bound_to_compare"]
    missing = [field for field in required if as_float(row.get(field)) is None]
    if missing:
        return {
            "case_id": row["case_id"],
            "arena": row["arena"],
            "lambda_gap": "",
            "X_static_bound": "",
            "X_dynamic_bound": "",
            "DeltaO_bound": "",
            "bound_to_compare": row.get("bound_to_compare", ""),
            "runner_status": "BLOCKED_MISSING_INPUTS",
            "failure_reason": ";".join(missing),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }

    a_min = as_float(row["a_min"]) or 0.0
    domain = as_float(row["C_P_over_L_D2"]) or 0.0
    m_min2 = as_float(row["m_min2"]) or 0.0
    source = as_float(row["J_open_plus_B_lift"]) or 0.0
    gamma_delta = as_float(row["gamma_mem_Delta_t"]) or 0.0
    x_initial = as_float(row["X_initial"]) or 0.0
    grad_bound = as_float(row.get("gradX_bound")) or 0.0
    k_i = as_float(row["K_i"]) or 0.0
    k_i_grad = as_float(row.get("K_i_grad")) or 0.0
    compare = as_float(row["bound_to_compare"]) or 0.0
    lambda_gap = a_min * domain + m_min2
    if lambda_gap <= 0:
        return {
            "case_id": row["case_id"],
            "arena": row["arena"],
            "lambda_gap": lambda_gap,
            "X_static_bound": "",
            "X_dynamic_bound": "",
            "DeltaO_bound": "",
            "bound_to_compare": compare,
            "runner_status": "FAIL_NONPOSITIVE_GAP",
            "failure_reason": "lambda_gap<=0",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    x_static = source / lambda_gap
    decay = math.exp(-gamma_delta)
    x_dynamic = decay * abs(x_initial) + (1.0 - decay) * x_static
    delta_o = abs(k_i) * x_dynamic + abs(k_i_grad) * grad_bound
    artificial = not bool(row.get("is_real_mts_input"))
    status = "PASS_DRYRUN_ARITHMETIC_ONLY" if delta_o <= compare and artificial else "FAIL_DRYRUN_ARITHMETIC_ONLY"
    if not artificial and delta_o <= compare:
        status = "PASS_NUMERIC_NONCLAIM_UNTIL_SOURCES_AUDITED"
    return {
        "case_id": row["case_id"],
        "arena": row["arena"],
        "lambda_gap": lambda_gap,
        "X_static_bound": x_static,
        "X_dynamic_bound": x_dynamic,
        "DeltaO_bound": delta_o,
        "bound_to_compare": compare,
        "runner_status": status,
        "failure_reason": "" if "PASS" in status else "DeltaO_bound>bound",
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
    }


def runner_rows(inputs: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    return [evaluate_case(row, timestamp) for row in inputs]


def gate_rows(runner: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    return [
        {"gate_id": "LGG3896_0_schema", "gate": "memory suppression schema", "result": "all required fields are explicit", "status": "PASS_EXECUTABLE_SCHEMA", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3896_1_bounds", "gate": "first local bound anchors", "result": "alpha3/Gdot/alpha2/xi/gamma anchors carried as comparison bounds only", "status": "PASS_BOUNDS_NONCLAIM", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3896_2_live", "gate": "live MTS memory row", "result": "live candidate row remains blocked by missing parent numeric inputs", "status": "BLOCKED_MISSING_PARENT_NUMBERS", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3896_3_arithmetic", "gate": "runner arithmetic", "result": "dry-run pass and nonpositive-gap failure are both detected", "status": "PASS_DRYRUN_ONLY", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3896_4_local_GR", "gate": "local-GR promotion", "result": "no claim until live sourced MTS inputs beat local bounds", "status": "BLOCKED_NO_CLAIM_EXECUTABLE_ROUTE_OPEN", "claim_allowed": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3896_0",
            "target_checkpoint": "3897-Y5-R2FR-derive-memory-Ki-projection-or-fill-first-physical-row.md",
            "script": "scripts/Y5_R2FR_3897_derive_memory_Ki_projection_or_fill_first_physical_row.py",
            "objective": "derive the observable projection derivatives K_alpha3, K_Gdot, K_gamma, K_R10, K_clock, K_orbital from the readout map; if derivation fails, keep the runner live but mark physical rows blocked",
            "why_next": "3896 made the suppression bound executable, so the next non-circular move is deriving the arena K_i maps rather than creating more missing-input ledgers",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_EXECUTABLE_MEMORY_SUPPRESSION_RUNNER_NONCLAIM",
            "claim": "NO_LOCAL_GR_CLAIM",
            "summary": "memory suppression law now has a runnable schema, dry-run arithmetic, failure-mode guard, and local bound anchors; live MTS row remains blocked until physical coefficients are derived",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    timestamp: str,
) -> None:
    doc = f"""# 3896 - Memory Suppression Runner and First Local Bound Row

Generated: `{timestamp}`

## Result

3896 turns the 3895 suppression formula into an executable non-claim runner.

Runner equations:

- `{MEMORY_BOUND}`
- `{HISTORY_BOUND}`
- `{ARENA_BOUND}`

The live MTS row is intentionally blocked because the parent-owned numbers are still not filled. The runner also includes two artificial dry-runs: one checks arithmetic can pass a bound, and one proves the runner rejects a non-positive gap. This is not a physics claim; it is the machinery needed before a physics claim can even be evaluated.

## Input Schema

{markdown_table(schema, ["field", "role", "units", "required", "claim_gate"])}

## Local Bound Anchors

{markdown_table(bounds, ["bound_id", "arena", "observable", "bound_value", "units", "comparison", "source_path"])}

## Runner Inputs

{markdown_table(inputs, ["case_id", "case_type", "arena", "a_min", "C_P_over_L_D2", "m_min2", "J_open_plus_B_lift", "gamma_mem_Delta_t", "K_i", "bound_to_compare", "valid_for_claim"])}

## Runner Output

{markdown_table(runner, ["case_id", "arena", "lambda_gap", "X_static_bound", "X_dynamic_bound", "DeltaO_bound", "bound_to_compare", "runner_status", "failure_reason"])}

## Local-GR Decision Gate

{markdown_table(gate, ["gate_id", "gate", "result", "status", "claim_allowed"])}

## Source Register

Resolved `{sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This checkpoint gives us a working scoreboard for the memory branch. The next hard leap is no longer "find what is missing"; it is deriving the projection coefficients `K_i` from the readout map so a physical memory row can be run against the local bounds.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3896 MEMORY SUPPRESSION RUNNER -->
## 3896 Memory Suppression Runner and First Local Bound Row

Timestamp: `{timestamp}`

Result: `PASS_EXECUTABLE_MEMORY_SUPPRESSION_RUNNER_NONCLAIM`.

Executable equations:
- `{MEMORY_BOUND}`
- `{HISTORY_BOUND}`
- `{ARENA_BOUND}`

First local comparison anchors are carried as nonclaim rows: alpha3 `4e-20`, Gdot/G `9.6e-15 yr^-1`, alpha2 `2e-9`, xi `4e-9`, and gamma-scale `2.3e-5`.

Decision: no local-GR claim. The live row is blocked by missing parent numeric inputs, but the memory residual is now scoreable as soon as `a_min`, `C_P/L_D^2`, `m_min^2`, `J_open+B_lift`, `gamma_mem Delta t`, and arena `K_i` are derived.

Next gate: `3897`, derive memory observable projection coefficients `K_i`.
<!-- END 3896 MEMORY SUPPRESSION RUNNER -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3896 MEMORY SUPPRESSION RUNNER -->"
    end = "<!-- END 3896 MEMORY SUPPRESSION RUNNER -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = [row for row in sources if row["exists"] and row["needle_found"]]
    checks.append(("VAL3896_0_sources", "all source paths and needles resolve", len(resolved) == len(sources), f"{len(resolved)}/{len(sources)} sources resolved"))
    required_schema = {"a_min", "C_P_over_L_D2", "m_min2", "J_open_plus_B_lift", "gamma_mem_Delta_t", "X_initial", "K_i"}
    checks.append(("VAL3896_1_schema", "required runner fields are explicit", required_schema.issubset({str(row["field"]) for row in schema}), f"{len(schema)} schema rows"))
    checks.append(("VAL3896_2_bounds", "first local bounds exist", {"alpha3", "abs(Gdot/G)", "alpha2", "xi", "abs(gamma-1)"}.issubset({str(row["observable"]) for row in bounds}), f"{len(bounds)} bounds"))
    checks.append(("VAL3896_3_live_blocked", "live MTS row is blocked by missing inputs", any(row["case_id"] == "LIVE3896_placeholder" and row["runner_status"] == "BLOCKED_MISSING_INPUTS" for row in runner), "LIVE3896_placeholder"))
    checks.append(("VAL3896_4_dry_pass", "dry-run arithmetic pass exists", any(row["case_id"] == "DRY3896_unit_pass" and row["runner_status"] == "PASS_DRYRUN_ARITHMETIC_ONLY" for row in runner), "DRY3896_unit_pass"))
    checks.append(("VAL3896_5_gap_fail", "nonpositive gap failure is caught", any(row["case_id"] == "DRY3896_gap_fail" and row["runner_status"] == "FAIL_NONPOSITIVE_GAP" for row in runner), "DRY3896_gap_fail"))
    checks.append(("VAL3896_6_no_claim", "local GR remains blocked", any(row["gate_id"] == "LGG3896_4_local_GR" and "BLOCKED" in str(row["status"]) for row in gate), "LGG3896_4"))
    checks.append(("VAL3896_7_all_nonclaim", "all generated rows are nonclaim", all(str(row.get("valid_for_claim", row.get("claim_allowed", False))) == "False" for collection in [inputs, bounds, runner, gate] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3896_8_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "working scoreboard" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3896_9_spine", "spine updated with 3896 block", SPINE_PATH.exists() and "BEGIN 3896 MEMORY SUPPRESSION RUNNER" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3896_10_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3896*")
            if path.is_file() and ("3896-Y5" in path.name or "P8_Y5_R2FR_3896" in path.name or "P8_Y5_BRR545_3896" in path.name)
        ]
    checks.append(("VAL3896_11_formalization_untouched", "no generated 3896 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3896_12_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3896_13_next_target", "next target derives K_i projections", any("derive-memory-Ki-projection" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3897 K_i"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    schema = schema_rows(timestamp)
    inputs = input_rows(timestamp)
    bounds = bound_anchor_rows(timestamp)
    runner = runner_rows(inputs, timestamp)
    gate = gate_rows(runner, timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["schema"], schema)
    write_csv(OUTPUTS["inputs"], inputs)
    write_csv(OUTPUTS["bounds"], bounds)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, schema, inputs, bounds, runner, gate, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, schema, inputs, bounds, runner, gate, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_EXECUTABLE_MEMORY_SUPPRESSION_RUNNER_NONCLAIM")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

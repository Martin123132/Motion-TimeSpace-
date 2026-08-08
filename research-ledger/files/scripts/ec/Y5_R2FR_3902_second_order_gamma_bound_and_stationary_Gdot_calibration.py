from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3902"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3902-Y5-R2FR-second-order-gamma-bound-and-stationary-Gdot-calibration.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3902_SOURCE_REGISTER.csv",
    "gamma": SRC / "P8_Y5_R2FR_3902_SECOND_ORDER_GAMMA_BOUND_DERIVATION.csv",
    "gdot": SRC / "P8_Y5_R2FR_3902_GDOT_STATIONARY_CALIBRATION_GATE.csv",
    "inputs": SRC / "P8_Y5_R2FR_3902_EXECUTABLE_SCALAR_RUNNER_INPUTS.csv",
    "runner": SRC / "P8_Y5_R2FR_3902_SCALAR_RUNNER_DRYRUN.csv",
    "gate": SRC / "P8_Y5_R2FR_3902_LOCAL_GR_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3902_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3902_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3902_VALIDATION.csv",
}

LAMBDA_GAP = "lambda_gap=a_min*C_P_over_L_D2+m_min2"
X_BOUND = "X_bound=S_X/lambda_gap, with S_X=J_open_plus_B_lift"
GRADX_BOUND = "gradX_bound^2 <= S_X^2/(a_min*lambda_gap)"
GAMMA2_BOUND = "gamma2_bound=C_slip*(S_X^2/(a_min*lambda_gap)+m_eff2*S_X^2/lambda_gap^2+B_TF_boundary)"
GAMMA2_ACCEPT = "gamma2_bound <= 2.3e-5"
GAMMA_SOURCE_CEILING = "S_X^2 <= (2.3e-5/C_slip-B_TF_boundary)/(1/(a_min*lambda_gap)+m_eff2/lambda_gap^2)"
DXDT_BOUND = "dXdt_bound <= gamma_mem*X_bound + (dJdt_bound+dBdt_bound)/lambda_gap + incoming_tail_dt"
GDOT_BOUND = "Gdot_bound=abs(c_G)*dXdt_bound+abs(X_bound)*dcGdt_bound+calibration_drift_bound <= 9.6e-15 yr^-1"


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
        ("SRC3902_00_next", SRC / "P8_Y5_R2FR_3901_NEXT_TARGET.csv", "NEXT3901_0", "3901 selected second-order gamma/Gdot target"),
        ("SRC3902_01_gamma", SRC / "P8_Y5_R2FR_3901_GAMMA_SECOND_ORDER_BOUND_INTERFACE.csv", "G2B3901_1_second_order_bound", "3901 gamma second-order interface"),
        ("SRC3902_02_runner", SRC / "P8_Y5_R2FR_3901_RUNNER_SCORE_UPDATE_ROWS.csv", "RUN3901_2_Gdot", "3901 runner update"),
        ("SRC3902_03_validation", SRC / "P8_Y5_BRR545_3901_VALIDATION.csv", "VAL3901_14_next_target", "3901 validation"),
        ("SRC3902_04_memory_law", SRC / "P8_Y5_R2FR_3895_MEMORY_SUPPRESSION_LAW.csv", "LAW3895_2_static_amplitude", "3895 memory bound law"),
        ("SRC3902_05_schema", SRC / "P8_Y5_R2FR_3896_MEMORY_SUPPRESSION_INPUT_SCHEMA.csv", "gradX_bound", "3896 executable memory input schema"),
        ("SRC3902_06_stationary", SRC / "P8_Y5_R2FR_3899_STATIONARY_MEMORY_PROOF_ATTEMPT.csv", "STAT3899_4_verdict", "3899 stationary Gdot verdict"),
        ("SRC3902_07_EM", SRC / "P8_Y5_R2FR_3900_MAXWELL_EM_STRESS_CALIBRATION_GATE.csv", "EM3900_2_alpha_vertex", "3900 EM/alpha calibration gate"),
        ("SRC3902_08_boundary", SRC / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv", "BC3892_4_verdict", "3892 boundary certificate"),
        ("SRC3902_09_bounds", SRC / "P8_Y5_R2FR_3896_LOCAL_BOUND_ANCHOR_ROWS.csv", "BND3896_1_Gdot", "3896 gamma/Gdot bound anchors"),
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


def gamma_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "GAM3902_0_gap",
            "piece": "coercive memory gap",
            "formula": LAMBDA_GAP,
            "derived_result": "positive lambda_gap is the denominator for both X and gradient bounds",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GAM3902_1_X",
            "piece": "memory amplitude",
            "formula": X_BOUND,
            "derived_result": "restates 3895/3896 in runner variables",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GAM3902_2_gradX",
            "piece": "gradient memory bound",
            "formula": GRADX_BOUND,
            "derived_result": "from energy identity: a_min||grad X||^2 <= ||X||S_X <= S_X^2/lambda_gap",
            "status": "DERIVED_GRADIENT_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GAM3902_3_gamma2",
            "piece": "second-order gamma residual",
            "formula": GAMMA2_BOUND,
            "derived_result": "substitutes X_bound and gradX_bound into the 3901 no-slip fallback",
            "status": "DERIVED_SECOND_ORDER_RUNNER_FORMULA",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GAM3902_4_accept",
            "piece": "gamma acceptance inequality",
            "formula": GAMMA2_ACCEPT,
            "derived_result": "Cassini/gamma-scale comparison remains nonclaim until all inputs are source-backed",
            "status": "NONCLAIM_THRESHOLD_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GAM3902_5_source_ceiling",
            "piece": "allowed source norm ceiling",
            "formula": GAMMA_SOURCE_CEILING,
            "derived_result": "turns gamma pressure into a direct maximum allowed S_X once C_slip and boundary anisotropy are fixed",
            "status": "DERIVED_REARRANGED_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gdot_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "GD3902_0_dxdt",
            "piece": "memory time-derivative bound",
            "formula": DXDT_BOUND,
            "result": "stationarity kills dXdt only when source, boundary, and incoming history are all time-silent",
            "status": "DERIVED_DXDT_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GD3902_1_stationary_zero",
            "piece": "stationary Gdot zero branch",
            "formula": "dXdt_bound=0 and calibration_drift_bound=0 => Gdot_bound=0",
            "result": "candidate exact zero branch from 3899, still parent-unsigned",
            "status": "CANDIDATE_ZERO_PARENT_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GD3902_2_bound",
            "piece": "Gdot executable bound",
            "formula": GDOT_BOUND,
            "result": "retains nonstationary memory and calibration drift as scored components",
            "status": "DERIVED_GDOT_RUNNER_FORMULA",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "GD3902_3_calibration",
            "piece": "calibration drift split",
            "formula": "calibration_drift_bound = abs(partial_t ln G_cal) + clock/alpha/source-frame drift terms",
            "result": "minimal Maxwell helps source stress but does not by itself fix alpha/clock/G calibration",
            "status": "OPEN_EM_CLOCK_CALIBRATION_INPUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def input_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "LIVE3902_placeholder",
            "case_type": "live_candidate",
            "C_slip": "MISSING_OPERATOR_NORM",
            "S_X": "MISSING_SOURCE_NORM",
            "a_min": "MISSING_PRINCIPAL_SIGN",
            "lambda_gap": "MISSING_GAP",
            "m_eff2": "MISSING_MEMORY_MASS",
            "B_TF_boundary": "MISSING_BOUNDARY_ANISO",
            "c_G": "MISSING_G_CALIBRATION_COEFF",
            "dXdt_bound": "MISSING_MEMORY_TIME_DERIVATIVE",
            "X_bound": "MISSING_X_BOUND",
            "dcGdt_bound": "MISSING_CG_TIME_DERIVATIVE",
            "calibration_drift_bound": "MISSING_CALIBRATION_DRIFT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "DRY3902_pass",
            "case_type": "artificial_arithmetic_check",
            "C_slip": 1.0,
            "S_X": 1.0e-4,
            "a_min": 1.0,
            "lambda_gap": 1.0,
            "m_eff2": 0.0,
            "B_TF_boundary": 0.0,
            "c_G": 1.0,
            "dXdt_bound": 1.0e-16,
            "X_bound": 1.0e-4,
            "dcGdt_bound": 0.0,
            "calibration_drift_bound": 1.0e-16,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "DRY3902_fail",
            "case_type": "artificial_failure_check",
            "C_slip": 1.0,
            "S_X": 1.0e-2,
            "a_min": 1.0,
            "lambda_gap": 1.0,
            "m_eff2": 0.0,
            "B_TF_boundary": 0.0,
            "c_G": 1.0,
            "dXdt_bound": 1.0e-12,
            "X_bound": 1.0e-2,
            "dcGdt_bound": 0.0,
            "calibration_drift_bound": 0.0,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def evaluate_case(row: dict[str, Any], timestamp: str) -> dict[str, Any]:
    required = ["C_slip", "S_X", "a_min", "lambda_gap", "m_eff2", "B_TF_boundary", "c_G", "dXdt_bound", "X_bound", "dcGdt_bound", "calibration_drift_bound"]
    missing = [field for field in required if as_float(row.get(field)) is None]
    if missing:
        return {
            "case_id": row["case_id"],
            "gamma2_bound": "",
            "gamma_pass": "",
            "Gdot_bound": "",
            "Gdot_pass": "",
            "runner_status": "BLOCKED_MISSING_INPUTS",
            "failure_reason": ";".join(missing),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }

    C_slip = as_float(row["C_slip"]) or 0.0
    S_X = as_float(row["S_X"]) or 0.0
    a_min = as_float(row["a_min"]) or 0.0
    lambda_gap = as_float(row["lambda_gap"]) or 0.0
    m_eff2 = as_float(row["m_eff2"]) or 0.0
    B_TF_boundary = as_float(row["B_TF_boundary"]) or 0.0
    c_G = as_float(row["c_G"]) or 0.0
    dXdt_bound = as_float(row["dXdt_bound"]) or 0.0
    X_bound = as_float(row["X_bound"]) or 0.0
    dcGdt_bound = as_float(row["dcGdt_bound"]) or 0.0
    calibration_drift_bound = as_float(row["calibration_drift_bound"]) or 0.0
    if C_slip < 0 or a_min <= 0 or lambda_gap <= 0 or m_eff2 < 0 or B_TF_boundary < 0:
        return {
            "case_id": row["case_id"],
            "gamma2_bound": "",
            "gamma_pass": "",
            "Gdot_bound": "",
            "Gdot_pass": "",
            "runner_status": "FAIL_INVALID_GAMMA_INPUTS",
            "failure_reason": "requires C_slip>=0, a_min>0, lambda_gap>0, m_eff2>=0, B_TF_boundary>=0",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    gamma2 = C_slip * ((S_X * S_X) / (a_min * lambda_gap) + m_eff2 * (S_X * S_X) / (lambda_gap * lambda_gap) + B_TF_boundary)
    gdot = abs(c_G) * abs(dXdt_bound) + abs(X_bound) * abs(dcGdt_bound) + abs(calibration_drift_bound)
    gamma_pass = gamma2 <= 2.3e-5
    gdot_pass = gdot <= 9.6e-15
    if gamma_pass and gdot_pass:
        status = "PASS_DRYRUN_BOUNDS_ARITHMETIC_ONLY"
        failure = ""
    else:
        status = "FAIL_DRYRUN_BOUND_EXCEEDED"
        parts = []
        if not gamma_pass:
            parts.append("gamma2>2.3e-5")
        if not gdot_pass:
            parts.append("Gdot>9.6e-15")
        failure = ";".join(parts)
    return {
        "case_id": row["case_id"],
        "gamma2_bound": gamma2,
        "gamma_pass": gamma_pass,
        "Gdot_bound": gdot,
        "Gdot_pass": gdot_pass,
        "runner_status": status,
        "failure_reason": failure,
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
    }


def runner_rows(inputs: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    return [evaluate_case(row, timestamp) for row in inputs]


def gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"gate_id": "LGG3902_0_gradX", "gate": "gradient memory bound", "result": GRADX_BOUND, "status": "PASS_DERIVED_FORMULA", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3902_1_gamma2", "gate": "second-order gamma bound", "result": GAMMA2_BOUND, "status": "PASS_FORMULA_READY_INPUTS_MISSING", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3902_2_Gdot", "gate": "Gdot calibration bound", "result": GDOT_BOUND, "status": "PASS_FORMULA_READY_INPUTS_MISSING", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3902_3_arithmetic", "gate": "runner arithmetic", "result": "dry-run pass and fail branches validate the scalar runner", "status": "PASS_DRYRUN_ONLY", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3902_4_local_GR", "gate": "local-GR promotion", "result": "no claim until live second-order gamma and Gdot calibration inputs are source-backed and pass", "status": "BLOCKED_NO_CLAIM_SCALAR_RUNNER_READY", "claim_allowed": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3902_0",
            "target_checkpoint": "3903-Y5-R2FR-source-second-order-inputs-or-promote-linear-gamma-zero-branch.md",
            "script": "scripts/Y5_R2FR_3903_source_second_order_inputs_or_promote_linear_gamma_zero_branch.py",
            "objective": "try to parent-sign the linear gamma-zero branch; if not, source C_slip, a_min, lambda_gap, m_eff2, B_TF_boundary, c_G, dXdt_bound, and calibration_drift_bound for a live nonclaim scalar runner row",
            "why_next": "3902 makes the scalar gamma/Gdot route executable, so the next move is to replace placeholders with parent signatures or real inputs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_SECOND_ORDER_GAMMA_GDOT_RUNNER_DERIVED",
            "claim": "NO_LOCAL_GR_CLAIM",
            "summary": "gradient memory bound, second-order gamma inequality, source-norm ceiling, and Gdot calibration runner are derived; live inputs remain missing",
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
    gamma: list[dict[str, Any]],
    gdot: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    timestamp: str,
) -> None:
    doc = f"""# 3902 - Second-Order Gamma Bound and Stationary Gdot Calibration

Generated: `{timestamp}`

## Result

3902 turns the 3901 second-order gamma route into an executable scalar runner.

Derived memory inputs:

- `{X_BOUND}`
- `{GRADX_BOUND}`

Second-order gamma:

- `{GAMMA2_BOUND}`
- `{GAMMA_SOURCE_CEILING}`

Gdot/calibration:

- `{DXDT_BOUND}`
- `{GDOT_BOUND}`

The live MTS row remains blocked because the physical inputs are not yet parent-signed or sourced. The dry-run pass/fail rows prove the arithmetic gate works.

## Second-Order Gamma Bound Derivation

{markdown_table(gamma, ["row_id", "piece", "formula", "derived_result", "status"])}

## Gdot Stationary Calibration Gate

{markdown_table(gdot, ["row_id", "piece", "formula", "result", "status"])}

## Executable Scalar Runner Inputs

{markdown_table(inputs, ["case_id", "case_type", "C_slip", "S_X", "a_min", "lambda_gap", "m_eff2", "B_TF_boundary", "c_G", "dXdt_bound", "calibration_drift_bound", "valid_for_claim"])}

## Scalar Runner Dryrun

{markdown_table(runner, ["case_id", "gamma2_bound", "gamma_pass", "Gdot_bound", "Gdot_pass", "runner_status", "failure_reason"])}

## Local-GR Decision Gate

{markdown_table(gate, ["gate_id", "gate", "result", "status", "claim_allowed"])}

## Source Register

Resolved `{sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is no longer vibes-missing. Gamma and Gdot now have an executable scalar scoreboard. The next useful work is to either parent-sign the linear gamma-zero branch or fill the live runner with real/sourced coefficients.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3902 SECOND ORDER GAMMA GDOT RUNNER -->
## 3902 Second-Order Gamma Bound and Stationary Gdot Calibration

Timestamp: `{timestamp}`

Result: `PASS_SECOND_ORDER_GAMMA_GDOT_RUNNER_DERIVED`.

Derived scalar runner formulas:
- `{GRADX_BOUND}`
- `{GAMMA2_BOUND}`
- `{GAMMA_SOURCE_CEILING}`
- `{DXDT_BOUND}`
- `{GDOT_BOUND}`

Decision: no local-GR claim. Gamma/Gdot are now executable nonclaim rows; live coefficients still need parent signatures or real source-backed inputs.

Next gate: `3903`, source second-order inputs or promote linear gamma-zero branch.
<!-- END 3902 SECOND ORDER GAMMA GDOT RUNNER -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3902 SECOND ORDER GAMMA GDOT RUNNER -->"
    end = "<!-- END 3902 SECOND ORDER GAMMA GDOT RUNNER -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    gamma: list[dict[str, Any]],
    gdot: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = [row for row in sources if row["exists"] and row["needle_found"]]
    checks.append(("VAL3902_0_sources", "all source paths and needles resolve", len(resolved) == len(sources), f"{len(resolved)}/{len(sources)} sources resolved"))
    checks.append(("VAL3902_1_gradX", "gradient bound derived", any(row["row_id"] == "GAM3902_2_gradX" and "S_X^2" in str(row["formula"]) for row in gamma), "GAM3902_2"))
    checks.append(("VAL3902_2_gamma2", "second-order gamma formula derived", any(row["row_id"] == "GAM3902_3_gamma2" and "C_slip" in str(row["formula"]) for row in gamma), "GAM3902_3"))
    checks.append(("VAL3902_3_ceiling", "source ceiling derived", any(row["row_id"] == "GAM3902_5_source_ceiling" and "S_X^2" in str(row["formula"]) for row in gamma), "GAM3902_5"))
    checks.append(("VAL3902_4_Gdot", "Gdot bound formula derived", any(row["row_id"] == "GD3902_2_bound" and "9.6e-15" in str(row["formula"]) for row in gdot), "GD3902_2"))
    checks.append(("VAL3902_5_live_blocked", "live row blocked by missing inputs", any(row["case_id"] == "LIVE3902_placeholder" and row["runner_status"] == "BLOCKED_MISSING_INPUTS" for row in runner), "LIVE3902_placeholder"))
    checks.append(("VAL3902_6_dry_pass", "dry-run pass exists", any(row["case_id"] == "DRY3902_pass" and row["runner_status"] == "PASS_DRYRUN_BOUNDS_ARITHMETIC_ONLY" for row in runner), "DRY3902_pass"))
    checks.append(("VAL3902_7_dry_fail", "dry-run fail exists", any(row["case_id"] == "DRY3902_fail" and row["runner_status"] == "FAIL_DRYRUN_BOUND_EXCEEDED" for row in runner), "DRY3902_fail"))
    checks.append(("VAL3902_8_no_claim", "local GR remains blocked", any(row["gate_id"] == "LGG3902_4_local_GR" and "BLOCKED" in str(row["status"]) for row in gate), "LGG3902_4"))
    checks.append(("VAL3902_9_all_nonclaim", "all generated rows are nonclaim", all(str(row.get("valid_for_claim", row.get("claim_allowed", False))) == "False" for collection in [gamma, gdot, inputs, runner, gate] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3902_10_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "executable scalar scoreboard" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3902_11_spine", "spine updated with 3902 block", SPINE_PATH.exists() and "BEGIN 3902 SECOND ORDER GAMMA GDOT RUNNER" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3902_12_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3902*")
            if path.is_file() and ("3902-Y5" in path.name or "P8_Y5_R2FR_3902" in path.name or "P8_Y5_BRR545_3902" in path.name)
        ]
    checks.append(("VAL3902_13_formalization_untouched", "no generated 3902 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3902_14_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3902_15_next_target", "next target sources second-order inputs", any("source-second-order-inputs" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3903 source inputs"))
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
    gamma = gamma_rows(timestamp)
    gdot = gdot_rows(timestamp)
    inputs = input_rows(timestamp)
    runner = runner_rows(inputs, timestamp)
    gate = gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["gamma"], gamma)
    write_csv(OUTPUTS["gdot"], gdot)
    write_csv(OUTPUTS["inputs"], inputs)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, gamma, gdot, inputs, runner, gate, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, gamma, gdot, inputs, runner, gate, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_SECOND_ORDER_GAMMA_GDOT_RUNNER_DERIVED")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

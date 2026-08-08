from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3899"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3899-Y5-R2FR-conformal-readout-stationary-memory-proof-or-scalar-bound-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3899_SOURCE_REGISTER.csv",
    "conformal": SRC / "P8_Y5_R2FR_3899_CONFORMAL_READOUT_PROOF_ATTEMPT.csv",
    "stationary": SRC / "P8_Y5_R2FR_3899_STATIONARY_MEMORY_PROOF_ATTEMPT.csv",
    "bounds": SRC / "P8_Y5_R2FR_3899_SCALAR_GAMMA_GDOT_BOUND_ROWS.csv",
    "gate": SRC / "P8_Y5_R2FR_3899_LOCAL_GR_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3899_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3899_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3899_VALIDATION.csv",
}

GAMMA_PROJECTION = "gamma_eff=(1+b_X X)/(1+a_X X)=1+(b_X-a_X)X+O(X^2)"
CONFORMAL_LOCK = "single observed coframe e_obs=Omega(X) e_GR gives a_X=b_X and therefore gamma_eff-1=O(X^2) at first PPN order after common measured-GM calibration"
STATIONARY_LOCK = "partial_t X_mem=0 follows only from a stationary/Killing local collar plus source-free memory equation, zero incoming history, and time-independent boundary data"
GDOT_PROJECTION = "partial_t ln G_eff = c_G partial_t X_mem + X_mem partial_t c_G + calibration_source_drift"


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


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3899_00_next", SRC / "P8_Y5_R2FR_3898_NEXT_TARGET.csv", "NEXT3898_0", "3898 selected conformal/stationary scalar target"),
        ("SRC3899_01_coeff", SRC / "P8_Y5_R2FR_3898_PARENT_READOUT_COEFFICIENT_ZERO_ATTEMPT.csv", "COEFF3898_2_c_gamma", "3898 scalar coefficient split"),
        ("SRC3899_02_fill", SRC / "P8_Y5_R2FR_3898_GAMMA_GDOT_FILL_FORMULAS.csv", "FILL3898_3_Gdot", "3898 gamma/Gdot fill formulas"),
        ("SRC3899_03_validation", SRC / "P8_Y5_BRR545_3898_VALIDATION.csv", "VAL3898_14_next_target", "3898 validation"),
        ("SRC3899_04_gamma_projection", SRC / "P8_Y5_R10_931_GAMMA_PROJECTION_DERIVATION.csv", "GAM931_2_gamma_projection", "older gamma projection derivation"),
        ("SRC3899_05_gamma_zero", SRC / "P8_Y5_R10_932_GAMMA_ZERO_THEOREM_ATTEMPT.csv", "GZ932_3_equal_response", "older gamma equal-response theorem attempt"),
        ("SRC3899_06_stationary_clock", SRC / "P8_Y5_HILBERT_CURRENT_2467_CLOCK_COMPATIBILITY_GATE.csv", "CLK2467_0_stationary_gate", "stationary/Killing local collar gate"),
        ("SRC3899_07_stationary_obstruction", SRC / "P8_Y5_BOUNDARY_CLOCK_TAU_2599_CLAIM_GATES.csv", "CG2599_3_stationarity_axiom", "stationarity treated as rejected shortcut in prior work"),
        ("SRC3899_08_memory_constant", SRC / "P8_Y5_MEMORY_OWNER_GATE_2626_COUNTERMODEL_LEDGER.csv", "CM2626_2_constant_mode", "constant-mode memory exception"),
        ("SRC3899_09_runner_bounds", SRC / "P8_Y5_R2FR_3896_LOCAL_BOUND_ANCHOR_ROWS.csv", "BND3896_1_Gdot", "3896 local bound anchors"),
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


def conformal_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CONF3899_0_projection",
            "clause": "weak-field gamma projection",
            "math": GAMMA_PROJECTION,
            "result": "gamma is controlled by the mismatch b_X-a_X, matching the older 931/932 route",
            "status": "DERIVED_PROJECTION_ALGEBRA",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CONF3899_1_single_coframe",
            "clause": "single observed coframe",
            "math": "e_obs^a=Omega(X) e_GR^a; g_obs=Omega(X)^2 g_GR",
            "result": "the lapse and spatial sectors receive the same scalar multiplier",
            "status": "PASS_IF_PARENT_SINGLE_COFRAME_SIGNED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CONF3899_2_equal_response",
            "clause": "no gravitational slip from memory",
            "math": CONFORMAL_LOCK,
            "result": "c_space-c_lapse=0 at first order if no disformal/lapse-only/spatial-only term exists",
            "status": "CANDIDATE_GAMMA_ZERO_PARENT_UNSIGNED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CONF3899_3_escape",
            "clause": "disformal/lapse-space escape",
            "math": "Delta g_obs may contain A(X)dt^2+B(X)delta_ij dx^i dx^j with A' != B'",
            "result": "scalarity alone does not force conformality; parent grammar must ban independent lapse/spatial coefficients",
            "status": "OPEN_ESCAPE_RETAINED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CONF3899_4_verdict",
            "clause": "gamma zero verdict",
            "math": "|gamma-1| <= |c_space-c_lapse| X_bound, with c_space-c_lapse=0 only on the conformal branch",
            "result": "gamma can be zero by single-coframe/no-slip proof, otherwise it remains a scalar bound row",
            "status": "PARTIAL_PROOF_BOUND_FALLBACK",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def stationary_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "STAT3899_0_equation",
            "clause": "local memory evolution",
            "math": "partial_t X_mem = -gamma_mem X_mem + lambda_gap^{-1}J_open(t) + boundary_history(t) in the reduced local branch",
            "result": "time variation is controlled by damping, open source, boundary, and incoming history",
            "status": "DERIVED_SYMBOLIC_EVOLUTION",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "STAT3899_1_stationary_collar",
            "clause": "stationary/Killing collar",
            "math": "L_tau g_obs=0, partial_t J_open=0, partial_t boundary=0, and no incoming memory tail",
            "result": "sufficient for partial_t X_mem=0 on the exact local branch",
            "status": "PASS_IF_PARENT_STATIONARY_COLLAR_SIGNED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "STAT3899_2_prior_obstruction",
            "clause": "stationarity is not free",
            "math": "prior 2599 gate rejected local stationarity as a shortcut when not parent-derived",
            "result": "cannot assert partial_t X_mem=0 globally from convenience",
            "status": "FAIL_AS_UNSIGNED_AXIOM",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "STAT3899_3_constant_mode",
            "clause": "constant memory mode",
            "math": "partial_t X_mem=0 but X_mem != 0 is harmless only if universal, source-independent, and absorbed into calibration",
            "result": "constant mode does not produce Gdot but may still affect gamma/R10/clock unless calibration is quotient-owned",
            "status": "CONSTANT_MODE_GUARD",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "STAT3899_4_verdict",
            "clause": "Gdot zero verdict",
            "math": GDOT_PROJECTION,
            "result": "Gdot is zero only if partial_t X_mem=0 and calibration drift is zero; otherwise bound it",
            "status": "PARTIAL_PROOF_BOUND_FALLBACK",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def scalar_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "SGB3899_0_gamma_zero_branch",
            "observable": "gamma-1",
            "branch": "single_coframe_conformal",
            "formula": "c_space-c_lapse=0 => gamma-1=O(X_mem^2) at first PPN order; runner may set K_gamma=0 only if parent signs conformal readout",
            "required_inputs": "parent single observed coframe; no disformal/lapse-space split; same measured-GM calibration",
            "bound_anchor": "2.3e-5",
            "row_status": "CANDIDATE_ZERO_PARENT_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "SGB3899_1_gamma_bound_branch",
            "observable": "gamma-1",
            "branch": "nonconformal_scalar",
            "formula": "|gamma-1| <= |c_space-c_lapse| X_bound <= 2.3e-5",
            "required_inputs": "numeric/source-backed c_space-c_lapse and X_bound from 3896 runner",
            "bound_anchor": "2.3e-5",
            "row_status": "FORMULA_READY_NUMERIC_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "SGB3899_2_Gdot_zero_branch",
            "observable": "Gdot/G",
            "branch": "stationary_memory",
            "formula": "partial_t X_mem=0 and calibration_source_drift=0 => Gdot/G=0",
            "required_inputs": "parent stationary/Killing collar; no incoming memory tail; time-independent boundary/source; quotient-owned calibration",
            "bound_anchor": "9.6e-15 yr^-1",
            "row_status": "CANDIDATE_ZERO_PARENT_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "SGB3899_3_Gdot_bound_branch",
            "observable": "Gdot/G",
            "branch": "nonstationary_memory",
            "formula": "|Gdot/G| <= |c_G| |partial_t X_mem| + |X_mem partial_t c_G| + |calibration_source_drift| <= 9.6e-15 yr^-1",
            "required_inputs": "c_G, partial_t X_mem bound, partial_t c_G or zero, calibration drift bound",
            "bound_anchor": "9.6e-15 yr^-1",
            "row_status": "FORMULA_READY_NUMERIC_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"gate_id": "LGG3899_0_gamma_projection", "gate": "gamma projection algebra", "result": "gamma residual is b_X-a_X at first order", "status": "PASS_DERIVED", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3899_1_conformal", "gate": "conformal readout proof", "result": "single observed coframe would set c_space=c_lapse, but parent no-disformal clause is unsigned", "status": "CANDIDATE_PASS_PARENT_UNSIGNED", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3899_2_stationary", "gate": "stationary memory proof", "result": "stationary collar would set partial_t X=0, but stationarity remains a parent/matching clause not a free axiom", "status": "CANDIDATE_PASS_PARENT_UNSIGNED", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3899_3_scalar_bounds", "gate": "gamma/Gdot fallback bounds", "result": "bound rows are formula-ready but require coefficients and X/partial_tX inputs", "status": "PASS_BOUND_ROWS_NONCLAIM", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3899_4_local_GR", "gate": "local-GR promotion", "result": "no claim until conformal/stationary clauses are parent-signed or scalar bound rows are numerically scored", "status": "BLOCKED_NO_CLAIM_SCALAR_GATE_SHARPENED", "claim_allowed": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3899_0",
            "target_checkpoint": "3900-Y5-R2FR-single-coframe-Maxwell-calibration-lock-or-scalar-runner-fill.md",
            "script": "scripts/Y5_R2FR_3900_single_coframe_Maxwell_calibration_lock_or_scalar_runner_fill.py",
            "objective": "try to sign the single observed coframe/no-disformal clause using the matter/EM/clock descent grammar; if not, push the gamma/Gdot scalar bound rows into the executable runner",
            "why_next": "3899 shows conformal readout and stationary memory are sufficient but unsigned; tying the single coframe to Maxwell/EM stress and calibrated clocks is the most direct way to connect local GR, Newtonian source calibration, and EM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_CONFORMAL_STATIONARY_SCALAR_GATE_SHARPENED",
            "claim": "NO_LOCAL_GR_CLAIM",
            "summary": "gamma zero follows from single-coframe conformal readout if parent-signed; Gdot zero follows from stationary memory plus zero calibration drift if parent-signed; fallback scalar bound rows emitted",
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
    conformal: list[dict[str, Any]],
    stationary: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    timestamp: str,
) -> None:
    doc = f"""# 3899 - Conformal Readout, Stationary Memory, or Scalar Bound Fill

Generated: `{timestamp}`

## Result

3899 sharpens the two scalar channels that survived 3898.

Gamma channel:

`{GAMMA_PROJECTION}`

`{CONFORMAL_LOCK}`

Gdot channel:

`{GDOT_PROJECTION}`

`{STATIONARY_LOCK}`

Verdict: conformal readout and stationary memory are sufficient routes, but not yet parent-signed. Therefore gamma and Gdot remain nonclaim scalar bound rows unless `3900` can lock the single observed coframe/Maxwell/clock calibration.

## Conformal Readout Proof Attempt

{markdown_table(conformal, ["row_id", "clause", "math", "result", "status"])}

## Stationary Memory Proof Attempt

{markdown_table(stationary, ["row_id", "clause", "math", "result", "status"])}

## Scalar Gamma/Gdot Bound Rows

{markdown_table(bounds, ["bound_id", "observable", "branch", "formula", "required_inputs", "bound_anchor", "row_status"])}

## Local-GR Decision Gate

{markdown_table(gate, ["gate_id", "gate", "result", "status", "claim_allowed"])}

## Source Register

Resolved `{sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is closer to a real local-GR route. The preferred-frame channels are symmetry-controlled, gamma is killed by single-coframe/no-slip readout, and Gdot is killed by stationary memory plus fixed calibration. The missing step is now explicit: prove those clauses from the parent coframe/Maxwell/clock structure, or score the scalar bounds.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3899 CONFORMAL STATIONARY SCALAR GATE -->
## 3899 Conformal Readout, Stationary Memory, or Scalar Bounds

Timestamp: `{timestamp}`

Result: `PASS_CONFORMAL_STATIONARY_SCALAR_GATE_SHARPENED`.

Gamma projection:
`{GAMMA_PROJECTION}`

Conformal lock:
`{CONFORMAL_LOCK}`

Gdot projection:
`{GDOT_PROJECTION}`

Stationary lock:
`{STATIONARY_LOCK}`

Decision: no local-GR claim. The sufficient routes are now explicit but parent-unsigned; fallback gamma/Gdot bound rows are formula-ready.

Next gate: `3900`, single coframe / Maxwell calibration lock or scalar runner fill.
<!-- END 3899 CONFORMAL STATIONARY SCALAR GATE -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3899 CONFORMAL STATIONARY SCALAR GATE -->"
    end = "<!-- END 3899 CONFORMAL STATIONARY SCALAR GATE -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    conformal: list[dict[str, Any]],
    stationary: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = [row for row in sources if row["exists"] and row["needle_found"]]
    checks.append(("VAL3899_0_sources", "all source paths and needles resolve", len(resolved) == len(sources), f"{len(resolved)}/{len(sources)} sources resolved"))
    checks.append(("VAL3899_1_gamma_projection", "gamma projection algebra included", any(row["row_id"] == "CONF3899_0_projection" and "b_X-a_X" in str(row["result"]) for row in conformal), "CONF3899_0"))
    checks.append(("VAL3899_2_conformal_lock", "conformal lock candidate exists", any(row["row_id"] == "CONF3899_2_equal_response" and "CANDIDATE_GAMMA_ZERO" in str(row["status"]) for row in conformal), "CONF3899_2"))
    checks.append(("VAL3899_3_escape_retained", "nonconformal escape retained", any(row["row_id"] == "CONF3899_3_escape" and "OPEN_ESCAPE" in str(row["status"]) for row in conformal), "CONF3899_3"))
    checks.append(("VAL3899_4_stationary", "stationary memory sufficient condition exists", any(row["row_id"] == "STAT3899_1_stationary_collar" and "PASS_IF_PARENT" in str(row["status"]) for row in stationary), "STAT3899_1"))
    checks.append(("VAL3899_5_stationary_not_axiom", "stationarity shortcut rejected", any(row["row_id"] == "STAT3899_2_prior_obstruction" and "FAIL_AS_UNSIGNED_AXIOM" in str(row["status"]) for row in stationary), "STAT3899_2"))
    checks.append(("VAL3899_6_bound_rows", "gamma/Gdot zero and bound rows exist", {"SGB3899_0_gamma_zero_branch", "SGB3899_1_gamma_bound_branch", "SGB3899_2_Gdot_zero_branch", "SGB3899_3_Gdot_bound_branch"}.issubset({str(row["bound_id"]) for row in bounds}), f"{len(bounds)} rows"))
    checks.append(("VAL3899_7_no_claim", "local GR remains blocked", any(row["gate_id"] == "LGG3899_4_local_GR" and "BLOCKED" in str(row["status"]) for row in gate), "LGG3899_4"))
    checks.append(("VAL3899_8_all_nonclaim", "all generated rows are nonclaim", all(str(row.get("valid_for_claim", row.get("claim_allowed", False))) == "False" for collection in [conformal, stationary, bounds, gate] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3899_9_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "parent coframe/Maxwell/clock" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3899_10_spine", "spine updated with 3899 block", SPINE_PATH.exists() and "BEGIN 3899 CONFORMAL STATIONARY SCALAR GATE" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3899_11_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3899*")
            if path.is_file() and ("3899-Y5" in path.name or "P8_Y5_R2FR_3899" in path.name or "P8_Y5_BRR545_3899" in path.name)
        ]
    checks.append(("VAL3899_12_formalization_untouched", "no generated 3899 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3899_13_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3899_14_next_target", "next target attacks single coframe Maxwell calibration", any("single-coframe-Maxwell" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3900 single coframe Maxwell"))
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
    conformal = conformal_rows(timestamp)
    stationary = stationary_rows(timestamp)
    bounds = scalar_bound_rows(timestamp)
    gate = gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["conformal"], conformal)
    write_csv(OUTPUTS["stationary"], stationary)
    write_csv(OUTPUTS["bounds"], bounds)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, conformal, stationary, bounds, gate, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, conformal, stationary, bounds, gate, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_CONFORMAL_STATIONARY_SCALAR_GATE_SHARPENED")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

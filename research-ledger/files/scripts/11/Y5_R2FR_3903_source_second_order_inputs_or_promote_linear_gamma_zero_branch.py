from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3903"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3903-Y5-R2FR-source-second-order-inputs-or-promote-linear-gamma-zero-branch.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3903_SOURCE_REGISTER.csv",
    "promotion": SRC / "P8_Y5_R2FR_3903_LINEAR_GAMMA_ZERO_BRANCH_PROMOTION.csv",
    "inputs": SRC / "P8_Y5_R2FR_3903_LIVE_SCALAR_INPUT_FILL_QUEUE.csv",
    "runner": SRC / "P8_Y5_R2FR_3903_RUNNER_BRANCH_UPDATE.csv",
    "gate": SRC / "P8_Y5_R2FR_3903_LOCAL_GR_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3903_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3903_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3903_VALIDATION.csv",
}

CHAIN_RULE = "D_X e_obs = D ebar_obs[Dq(X_mem)] = 0 if X_mem in ker(Dq_parent) and e_obs=ebar_obs(q(Phi))"
LINEAR_ZERO_CONTRACT = "K_gamma_linear=0 iff Dq[X_mem]=0, no direct hidden/disformal readout, quadratic memory stress, finite Sigma-R11, and no linear boundary/projector anisotropy"
LIVE_GAMMA2 = "gamma2_bound=C_slip*(S_X^2/(a_min*lambda_gap)+m_eff2*S_X^2/lambda_gap^2+B_TF_boundary)"
LIVE_GDOT = "Gdot_bound=abs(c_G)*dXdt_bound+abs(X_bound)*dcGdt_bound+calibration_drift_bound"


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
        ("SRC3903_00_next", SRC / "P8_Y5_R2FR_3902_NEXT_TARGET.csv", "NEXT3902_0", "3902 selected source/promote target"),
        ("SRC3903_01_gamma2", SRC / "P8_Y5_R2FR_3902_SECOND_ORDER_GAMMA_BOUND_DERIVATION.csv", "GAM3902_5_source_ceiling", "3902 second-order gamma bound"),
        ("SRC3903_02_runner", SRC / "P8_Y5_R2FR_3902_SCALAR_RUNNER_DRYRUN.csv", "LIVE3902_placeholder", "3902 executable scalar runner"),
        ("SRC3903_03_validation", SRC / "P8_Y5_BRR545_3902_VALIDATION.csv", "VAL3902_15_next_target", "3902 validation"),
        ("SRC3903_04_chain", SRC / "P8_Y5_R2FR_3888_QUOTIENT_NO_LINEAR_SOURCE_DERIVATION.csv", "NLS3888_2_chain_rule", "quotient chain rule"),
        ("SRC3903_05_action", SRC / "P8_Y5_R2FR_3890_PARENT_ACTION_GRAMMAR_INSERTION.csv", "INS3890_3_variation", "candidate action vertical variation"),
        ("SRC3903_06_memory", SRC / "P8_Y5_R2FR_3894_MEMORY_PARENT_OWNER_INSERTION.csv", "OWN3894_0_owner", "memory parent owner candidate"),
        ("SRC3903_07_response", SRC / "P8_Y5_R2FR_3901_NO_DISFORMAL_RESPONSE_EQUATION.csv", "RESP3901_5_verdict", "linear gamma zero candidate"),
        ("SRC3903_08_dq", SRC / "P8_Y5_FIELD_QUOTIENT_2570_DQ_VERTICAL_GENERATOR_LEDGER.csv", "DQ2570_4_memory_frame", "memory-frame verticality obstruction"),
        ("SRC3903_09_qmap", SRC / "P8_EM_actual_q_map_vertical_basis_candidate.csv", "QMAP3517_0_public_geometry", "public geometry q-map candidate"),
        ("SRC3903_10_boundary", SRC / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv", "BC3892_4_verdict", "boundary anisotropy certificate context"),
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


def promotion_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "LGZ3903_0_chain_rule",
            "clause": "q-basic observed coframe chain rule",
            "statement": CHAIN_RULE,
            "status": "EXACT_IF_DQ_ZERO_AND_QBASIC",
            "remaining_failure": "must prove X_mem is actually in ker(Dq_parent) for the same q used by e_obs/tau/clocks",
            "candidate_zero": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "LGZ3903_1_Xmem_vertical",
            "clause": "memory verticality",
            "statement": "X_mem is a Y_loc parent auxiliary, but Dq[X_mem]=0 is an admission condition, not yet globally proved",
            "status": "FAIL_TO_PROMOTE_PARENT_UNSIGNED",
            "remaining_failure": "2570 memory-frame row keeps tau/coframe residuals live until Dq and DObs_e vanish",
            "candidate_zero": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "LGZ3903_2_direct_disformal",
            "clause": "direct disformal readout",
            "statement": "If LGZ3903_0 and LGZ3903_1 pass, direct A(X)tau_tau+B(X)h_ij readout is ill-typed/zero because e_obs has no X derivative",
            "status": "PASS_IF_MEMORY_VERTICALITY_SIGNED",
            "remaining_failure": "direct disformal coefficient remains a fallback input if Dq[X_mem] is nonzero",
            "candidate_zero": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "LGZ3903_3_stress",
            "clause": "linear anisotropic stress",
            "statement": "3894 quadratic memory stress plus 3893 Sigma-R11 factorization remove linear stress terms on the candidate local branch",
            "status": "PASS_CANDIDATE_BRANCH",
            "remaining_failure": "boundary/projector anisotropy and source closure still must be zero or bounded",
            "candidate_zero": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "LGZ3903_4_contract",
            "clause": "linear gamma-zero contract",
            "statement": LINEAR_ZERO_CONTRACT,
            "status": "CONTRACT_READY_NOT_PROMOTED",
            "remaining_failure": "Dq[X_mem], boundary/projector anisotropy, and live scalar inputs remain unsourced",
            "candidate_zero": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def input_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"input_id": "IN3903_0_Dq_Xmem", "input": "Dq[X_mem]", "route": "derive from parent quotient map and Y_loc/memory owner", "current_status": "MISSING_VERTICALITY_PROOF", "runner_use": "if zero, direct disformal K_gamma_linear row closes", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"input_id": "IN3903_1_C_slip", "input": "C_slip", "route": "operator norm of inverse EH traceless spatial equation on selected local domain/gauge", "current_status": "MISSING_OPERATOR_NORM", "runner_use": LIVE_GAMMA2, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"input_id": "IN3903_2_a_min", "input": "a_min", "route": "positive principal-symbol lower bound for memory action", "current_status": "MISSING_PARENT_SIGN_CERTIFICATE", "runner_use": LIVE_GAMMA2, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"input_id": "IN3903_3_lambda_gap", "input": "lambda_gap", "route": "lambda_gap=a_min*C_P/L_D^2+m_min2 from local domain and memory mass", "current_status": "MISSING_DOMAIN_AND_GAP_NUMBERS", "runner_use": LIVE_GAMMA2, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"input_id": "IN3903_4_m_eff2", "input": "m_eff2", "route": "memory mass/gap or zero-mode removal theorem", "current_status": "MISSING_MEMORY_MASS_OR_ZERO_MODE", "runner_use": LIVE_GAMMA2, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"input_id": "IN3903_5_B_TF_boundary", "input": "B_TF_boundary", "route": "3892 topological/no-flux certificate or numeric traceless boundary stress norm", "current_status": "MISSING_BOUNDARY_ANISOTROPY_ZERO_OR_BOUND", "runner_use": LIVE_GAMMA2, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"input_id": "IN3903_6_c_G", "input": "c_G", "route": "differentiate Newton/G calibration with respect to X_mem on same coframe/source branch", "current_status": "MISSING_G_CALIBRATION_COEFFICIENT", "runner_use": LIVE_GDOT, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"input_id": "IN3903_7_dXdt", "input": "dXdt_bound", "route": "stationary-memory proof or dynamic memory equation bound", "current_status": "MISSING_STATIONARY_OR_DYNAMIC_INPUT", "runner_use": LIVE_GDOT, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"input_id": "IN3903_8_calibration", "input": "calibration_drift_bound", "route": "quotient-owned Maxwell/clock/G constants or clock/alpha drift bound", "current_status": "MISSING_EM_CLOCK_CALIBRATION_LOCK", "runner_use": LIVE_GDOT, "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "update_id": "RUN3903_0_branch_split",
            "runner_field": "gamma_branch",
            "rule": "if Dq[X_mem]=0 and boundary/projector anisotropy is zero, use linear-zero branch; otherwise evaluate second-order/live-input branch",
            "status": "BRANCH_LOGIC_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "RUN3903_1_live_inputs",
            "runner_field": "LIVE3902_placeholder",
            "rule": "replace placeholder with IN3903_1..8 only after source paths/units/parent signatures exist",
            "status": "LIVE_ROW_STILL_BLOCKED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "RUN3903_2_no_shortcut",
            "runner_field": "claim_guard",
            "rule": "linear gamma zero is not claimable from q-basic language unless the memory direction itself passes Dq and DObs_e tests",
            "status": "NO_SHORTCUT_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"gate_id": "LGG3903_0_chain", "gate": "q-basic coframe chain rule", "result": "exact zero if Dq[X_mem]=0", "status": "PASS_CONDITIONAL_EXACT", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3903_1_verticality", "gate": "memory verticality", "result": "not parent-signed; 2570 memory-frame obstruction remains", "status": "FAIL_PARENT_UNSIGNED", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3903_2_linear_gamma", "gate": "linear gamma-zero promotion", "result": "contract ready but not promoted to claim", "status": "BLOCKED_DQ_MEMORY_BOUNDARY_INPUTS", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3903_3_live_runner", "gate": "live scalar runner row", "result": "input fill queue emitted, but no physical live row is claimable yet", "status": "BLOCKED_INPUTS_MISSING", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3903_4_local_GR", "gate": "local-GR promotion", "result": "no claim until Dq[X_mem] or live scalar inputs close", "status": "BLOCKED_NO_CLAIM_DQ_GATE_IDENTIFIED", "claim_allowed": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3903_0",
            "target_checkpoint": "3904-Y5-R2FR-Dq-memory-verticality-proof-or-live-scalar-input-fill.md",
            "script": "scripts/Y5_R2FR_3904_Dq_memory_verticality_proof_or_live_scalar_input_fill.py",
            "objective": "prove or reject Dq[X_mem]=0 and DObs_e[X_mem]=0 for the memory direction; if rejected, fill direct disformal/scalar live runner coefficients instead",
            "why_next": "3903 shows the linear gamma-zero branch hinges primarily on memory verticality, not on another vague coupling audit",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_LINEAR_GAMMA_ZERO_CONTRACT_DQ_GATE_IDENTIFIED",
            "claim": "NO_LOCAL_GR_CLAIM",
            "summary": "linear gamma-zero branch is reduced to an exact Dq/e_obs verticality condition plus boundary/projector inputs; live scalar fill queue emitted",
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
    promotion: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    timestamp: str,
) -> None:
    doc = f"""# 3903 - Source Second-Order Inputs or Promote Linear Gamma-Zero Branch

Generated: `{timestamp}`

## Result

3903 tries to promote the linear gamma-zero branch and finds the exact hinge.

Exact chain rule:

`{CHAIN_RULE}`

Linear gamma-zero contract:

`{LINEAR_ZERO_CONTRACT}`

Verdict: the branch is not claim-promoted because `Dq[X_mem]=0`/`DObs_e[X_mem]=0` for the memory direction is still unsigned. But this is progress: the blocker is now a concrete verticality equation, not an atmospheric "coupling issue".

## Linear Gamma-Zero Branch Promotion

{markdown_table(promotion, ["row_id", "clause", "statement", "status", "remaining_failure"])}

## Live Scalar Input Fill Queue

{markdown_table(inputs, ["input_id", "input", "route", "current_status", "runner_use"])}

## Runner Branch Update

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Local-GR Decision Gate

{markdown_table(gate, ["gate_id", "gate", "result", "status", "claim_allowed"])}

## Source Register

Resolved `{sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This checkpoint makes the next target brutally clear: prove the memory direction is truly quotient-vertical for the observed coframe, or stop trying to use the linear gamma-zero branch and fill the scalar runner coefficients.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3903 LINEAR GAMMA DQ GATE -->
## 3903 Linear Gamma-Zero Contract and Dq Gate

Timestamp: `{timestamp}`

Result: `PASS_LINEAR_GAMMA_ZERO_CONTRACT_DQ_GATE_IDENTIFIED`.

Exact chain rule:
`{CHAIN_RULE}`

Linear gamma-zero contract:
`{LINEAR_ZERO_CONTRACT}`

Decision: no local-GR claim. The branch now hinges on proving `Dq[X_mem]=0` and `DObs_e[X_mem]=0`; otherwise the scalar runner needs live physical coefficients.

Next gate: `3904`, Dq memory verticality proof or live scalar input fill.
<!-- END 3903 LINEAR GAMMA DQ GATE -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3903 LINEAR GAMMA DQ GATE -->"
    end = "<!-- END 3903 LINEAR GAMMA DQ GATE -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = [row for row in sources if row["exists"] and row["needle_found"]]
    checks.append(("VAL3903_0_sources", "all source paths and needles resolve", len(resolved) == len(sources), f"{len(resolved)}/{len(sources)} sources resolved"))
    checks.append(("VAL3903_1_chain", "exact Dq chain rule row exists", any(row["row_id"] == "LGZ3903_0_chain_rule" and "Dq" in str(row["statement"]) for row in promotion), "LGZ3903_0"))
    checks.append(("VAL3903_2_verticality_block", "memory verticality remains unsigned", any(row["row_id"] == "LGZ3903_1_Xmem_vertical" and "FAIL" in str(row["status"]) for row in promotion), "LGZ3903_1"))
    checks.append(("VAL3903_3_contract", "linear gamma-zero contract emitted", any(row["row_id"] == "LGZ3903_4_contract" and "CONTRACT_READY" in str(row["status"]) for row in promotion), "LGZ3903_4"))
    required_inputs = {"Dq[X_mem]", "C_slip", "a_min", "lambda_gap", "m_eff2", "B_TF_boundary", "c_G", "dXdt_bound", "calibration_drift_bound"}
    checks.append(("VAL3903_4_inputs", "live scalar input queue complete", required_inputs.issubset({str(row["input"]) for row in inputs}), f"{len(inputs)} inputs"))
    checks.append(("VAL3903_5_runner", "runner branch update guards shortcut", any(row["update_id"] == "RUN3903_2_no_shortcut" for row in runner), "RUN3903_2"))
    checks.append(("VAL3903_6_no_claim", "local GR remains blocked", any(row["gate_id"] == "LGG3903_4_local_GR" and "BLOCKED" in str(row["status"]) for row in gate), "LGG3903_4"))
    checks.append(("VAL3903_7_all_nonclaim", "all generated rows are nonclaim", all(str(row.get("valid_for_claim", row.get("claim_allowed", False))) == "False" for collection in [promotion, inputs, runner, gate] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3903_8_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "quotient-vertical" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3903_9_spine", "spine updated with 3903 block", SPINE_PATH.exists() and "BEGIN 3903 LINEAR GAMMA DQ GATE" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3903_10_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3903*")
            if path.is_file() and ("3903-Y5" in path.name or "P8_Y5_R2FR_3903" in path.name or "P8_Y5_BRR545_3903" in path.name)
        ]
    checks.append(("VAL3903_11_formalization_untouched", "no generated 3903 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3903_12_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3903_13_next_target", "next target attacks Dq memory verticality", any("Dq-memory-verticality" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3904 Dq memory"))
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
    promotion = promotion_rows(timestamp)
    inputs = input_rows(timestamp)
    runner = runner_rows(timestamp)
    gate = gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["inputs"], inputs)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, promotion, inputs, runner, gate, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, promotion, inputs, runner, gate, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_LINEAR_GAMMA_ZERO_CONTRACT_DQ_GATE_IDENTIFIED")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

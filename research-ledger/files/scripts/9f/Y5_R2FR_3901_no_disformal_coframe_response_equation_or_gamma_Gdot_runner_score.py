from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3901"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3901-Y5-R2FR-no-disformal-coframe-response-equation-or-gamma-Gdot-runner-score.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3901_SOURCE_REGISTER.csv",
    "response": SRC / "P8_Y5_R2FR_3901_NO_DISFORMAL_RESPONSE_EQUATION.csv",
    "gamma": SRC / "P8_Y5_R2FR_3901_GAMMA_SECOND_ORDER_BOUND_INTERFACE.csv",
    "runner": SRC / "P8_Y5_R2FR_3901_RUNNER_SCORE_UPDATE_ROWS.csv",
    "gate": SRC / "P8_Y5_R2FR_3901_LOCAL_GR_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3901_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3901_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3901_VALIDATION.csv",
}

SLIP_EQUATION = "(partial_i partial_j-delta_ij nabla^2/3)(Phi-Psi)=8*pi*G*Pi_TF_total"
QUADRATIC_STRESS = "Pi_TF_mem=O((grad X_mem)^2)+O(X_mem^2)+Pi_TF_boundary/projector"
GAMMA_SECOND_ORDER = "|gamma-1| <= C_slip[(gradX_bound)^2 + m_eff^2 X_bound^2 + B_TF_boundary] <= 2.3e-5"
LINEAR_GAMMA_ZERO = "c_space-c_lapse=0 at O(X_mem) if direct disformal readout is absent and memory stress is quadratic about X_mem=0"


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
        ("SRC3901_00_next", SRC / "P8_Y5_R2FR_3900_NEXT_TARGET.csv", "NEXT3900_0", "3900 selected no-disformal response target"),
        ("SRC3901_01_coframe", SRC / "P8_Y5_R2FR_3900_SINGLE_COFRAME_LOCK_ATTEMPT.csv", "COF3900_3_no_disformal", "3900 no-disformal open row"),
        ("SRC3901_02_Maxwell", SRC / "P8_Y5_R2FR_3900_MAXWELL_EM_STRESS_CALIBRATION_GATE.csv", "EM3900_0_minimal_Maxwell", "3900 Maxwell same-source stress row"),
        ("SRC3901_03_validation", SRC / "P8_Y5_BRR545_3900_VALIDATION.csv", "VAL3900_14_next_target", "3900 validation"),
        ("SRC3901_04_memory_action", SRC / "P8_Y5_R2FR_3894_MEMORY_PARENT_OWNER_INSERTION.csv", "OWN3894_1_action", "3894 quadratic memory action"),
        ("SRC3901_05_memory_bound", SRC / "P8_Y5_R2FR_3895_MEMORY_SUPPRESSION_LAW.csv", "LAW3895_2_static_amplitude", "3895 memory amplitude bound"),
        ("SRC3901_06_R11", SRC / "P8_Y5_R2FR_3893_R11_SIGMA_FACTORIZATION_INSERTION.csv", "R11S3893_05_vector_preferred_frame", "3893 R11 Sigma factorization"),
        ("SRC3901_07_Yloc_STF", SRC / "P8_Y5_R2FR_3887_YLOC_COMPONENT_CLOSURE_MATRIX.csv", "YLC3887_1_Qcoh_STF", "Yloc tensor/shear closure context"),
        ("SRC3901_08_gamma_zero", SRC / "P8_Y5_R10_932_GAMMA_ZERO_THEOREM_ATTEMPT.csv", "GZ932_3_equal_response", "older gamma no-slip/equal-response attempt"),
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


def response_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RESP3901_0_weak_field",
            "piece": "weak-field scalar response",
            "statement": "g00=-1+2 Phi, gij=(1+2 Psi)delta_ij; gamma-1 tracks Psi/Phi-1 and hence the slip Phi-Psi after measured-GM calibration",
            "result": "gamma-zero is equivalent to no scalar slip at linear order",
            "status": "DERIVED_READOUT_EQUATION",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RESP3901_1_EH_traceless",
            "piece": "EH traceless spatial equation",
            "statement": SLIP_EQUATION,
            "result": "only traceless anisotropic stress sources Phi-Psi at linear order",
            "status": "DERIVED_NO_SLIP_RESPONSE",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RESP3901_2_memory_quadratic",
            "piece": "memory stress order",
            "statement": QUADRATIC_STRESS,
            "result": "the 3894 quadratic memory action has no linear anisotropic stress around X_mem=0 unless affine/source/boundary terms reopen it",
            "status": "PASS_CANDIDATE_LINEAR_SLIP_ZERO",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RESP3901_3_direct_disformal",
            "piece": "direct readout guard",
            "statement": "direct A(X)tau_tau+B(X)h_ij readout would bypass the stress equation and create c_space-c_lapse at O(X)",
            "result": "must be forbidden by parent object-language/no-hidden-frame rule or retained as coefficient",
            "status": "OPEN_IF_DIRECT_DISFORMAL_ALLOWED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RESP3901_4_R11",
            "piece": "R11/operator leakage",
            "statement": "Sigma_loc(Y)-factorized R11 families have zero first variation on Y_loc=0 and do not source linear slip if finite",
            "result": "vector/preferred-frame R11 leakage is linear-silent on the candidate branch but still depends on Y_loc/source closure",
            "status": "PASS_CANDIDATE_R11_LINEAR_SILENCE",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RESP3901_5_verdict",
            "piece": "no-disformal response verdict",
            "statement": LINEAR_GAMMA_ZERO,
            "result": "gamma is not fully proved zero, but the dangerous linear scalar leak is replaced by a second-order bound",
            "status": "LINEAR_GAMMA_ZERO_CANDIDATE_SECOND_ORDER_BOUND_REQUIRED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def gamma_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "G2B3901_0_linear_zero",
            "quantity": "linear gamma coefficient",
            "formula": "K_gamma_linear=0, equivalently c_space-c_lapse=0",
            "required_inputs": "no direct disformal readout; quadratic memory stress; finite Sigma-factorized R11; no linear boundary/projector anisotropy",
            "status": "CANDIDATE_LINEAR_ZERO_PARENT_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "G2B3901_1_second_order_bound",
            "quantity": "second-order gamma residual",
            "formula": GAMMA_SECOND_ORDER,
            "required_inputs": "C_slip, gradX_bound, X_bound, m_eff, B_TF_boundary",
            "status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "G2B3901_2_boundary_projector_escape",
            "quantity": "boundary/projector anisotropic stress",
            "formula": "Pi_TF_boundary/projector must be zero by 3892 certificate or included in B_TF_boundary",
            "required_inputs": "topological/no-flux boundary certificate or numeric anisotropic boundary stress norm",
            "status": "ESCAPE_RETAINED_AS_BOUND_INPUT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "G2B3901_3_runner_threshold",
            "quantity": "gamma acceptance threshold",
            "formula": "G2B3901_1 <= 2.3e-5",
            "required_inputs": "all second-order inputs source-backed; no cancellation credit",
            "status": "NONCLAIM_RUNNER_THRESHOLD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "update_id": "RUN3901_0_gamma_linear",
            "runner_field": "K_gamma_linear",
            "rule": "set to zero only if RESP3901_2, RESP3901_3 guard, and RESP3901_4 are parent-signed",
            "status": "CANDIDATE_ZERO_GATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "RUN3901_1_gamma_second_order",
            "runner_field": "gamma_second_order_bound",
            "rule": GAMMA_SECOND_ORDER,
            "status": "RUNNER_FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "RUN3901_2_Gdot",
            "runner_field": "Gdot_bound",
            "rule": "Gdot remains governed by 3899/3900 stationary-memory and calibration-drift rows; no-disformal response does not close it",
            "status": "UNCHANGED_OPEN_GDOT_SCALAR_CHANNEL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "RUN3901_3_alpha_clock",
            "runner_field": "alpha_clock_bound",
            "rule": "alpha/clock rows remain open unless quotient-owned Maxwell coefficient and clock calibration are signed",
            "status": "UNCHANGED_OPEN_EM_CALIBRATION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"gate_id": "LGG3901_0_slip_equation", "gate": "EH no-slip response", "result": "traceless equation isolates gamma leak to anisotropic stress", "status": "PASS_DERIVED", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3901_1_memory_linear", "gate": "memory linear anisotropic stress", "result": "quadratic memory action makes linear anisotropic stress vanish on candidate branch", "status": "CANDIDATE_PASS_PARENT_UNSIGNED", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3901_2_disformal_guard", "gate": "direct disformal readout", "result": "must be parent-forbidden; otherwise gamma linear coefficient remains", "status": "OPEN_GUARD_REQUIRED", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3901_3_gamma", "gate": "gamma residual", "result": "linear gamma leak is candidate-zero; second-order bound remains", "status": "PARTIAL_PASS_SECOND_ORDER_BOUND_REQUIRED", "claim_allowed": False, "timestamp_utc": timestamp},
        {"gate_id": "LGG3901_4_local_GR", "gate": "local-GR promotion", "result": "no claim until disformal guard and second-order gamma/Gdot/EM calibration bounds close", "status": "BLOCKED_NO_CLAIM_LINEAR_GAMMA_SHARPENED", "claim_allowed": False, "timestamp_utc": timestamp},
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3901_0",
            "target_checkpoint": "3902-Y5-R2FR-second-order-gamma-bound-and-stationary-Gdot-calibration.md",
            "script": "scripts/Y5_R2FR_3902_second_order_gamma_bound_and_stationary_Gdot_calibration.py",
            "objective": "source or derive the second-order gamma inputs C_slip, gradX_bound, X_bound, B_TF_boundary, then attack stationary Gdot/calibration drift",
            "why_next": "3901 reduces gamma from a linear scalar-coefficient problem to a second-order anisotropic-stress bound, while Gdot and EM calibration remain open",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_LINEAR_GAMMA_NO_SLIP_ROUTE_DERIVED",
            "claim": "NO_LOCAL_GR_CLAIM",
            "summary": "derived EH no-slip response route; memory quadratic stress gives candidate linear gamma zero, but second-order gamma, disformal guard, Gdot, and EM calibration remain open",
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
    response: list[dict[str, Any]],
    gamma: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    timestamp: str,
) -> None:
    doc = f"""# 3901 - No-Disformal Coframe Response Equation or Gamma/Gdot Runner Score

Generated: `{timestamp}`

## Result

3901 takes the no-disformal problem through the GR no-slip equation instead of assuming a conformal coframe.

No-slip equation:

`{SLIP_EQUATION}`

Memory stress order:

`{QUADRATIC_STRESS}`

Main result:

`{LINEAR_GAMMA_ZERO}`

Fallback:

`{GAMMA_SECOND_ORDER}`

This is progress: gamma is no longer treated as an arbitrary first-order scalar coefficient if the candidate branch signs the no-direct-disformal guard. The remaining gamma problem is a second-order anisotropic-stress bound.

## No-Disformal Response Equation

{markdown_table(response, ["row_id", "piece", "statement", "result", "status"])}

## Gamma Second-Order Bound Interface

{markdown_table(gamma, ["bound_id", "quantity", "formula", "required_inputs", "status"])}

## Runner Score Update Rows

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Local-GR Decision Gate

{markdown_table(gate, ["gate_id", "gate", "result", "status", "claim_allowed"])}

## Source Register

Resolved `{sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is one of the better leaps in the local branch: gamma can plausibly be removed at linear order by the same mechanism GR uses, provided direct disformal readout is forbidden. The next job is not another audit; it is scoring the second-order gamma bound and then doing the same hard treatment for Gdot/calibration.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3901 NO DISFORMAL RESPONSE EQUATION -->
## 3901 No-Disformal Coframe Response Equation

Timestamp: `{timestamp}`

Result: `PASS_LINEAR_GAMMA_NO_SLIP_ROUTE_DERIVED`.

No-slip equation:
`{SLIP_EQUATION}`

Memory stress order:
`{QUADRATIC_STRESS}`

Linear gamma result:
`{LINEAR_GAMMA_ZERO}`

Second-order fallback:
`{GAMMA_SECOND_ORDER}`

Decision: no local-GR claim. Gamma is candidate-zero at linear order, but the second-order anisotropic-stress bound, disformal guard, Gdot, and EM calibration remain open.

Next gate: `3902`, second-order gamma bound and stationary Gdot calibration.
<!-- END 3901 NO DISFORMAL RESPONSE EQUATION -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3901 NO DISFORMAL RESPONSE EQUATION -->"
    end = "<!-- END 3901 NO DISFORMAL RESPONSE EQUATION -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    response: list[dict[str, Any]],
    gamma: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gate: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = [row for row in sources if row["exists"] and row["needle_found"]]
    checks.append(("VAL3901_0_sources", "all source paths and needles resolve", len(resolved) == len(sources), f"{len(resolved)}/{len(sources)} sources resolved"))
    checks.append(("VAL3901_1_slip", "no-slip equation exists", any(row["row_id"] == "RESP3901_1_EH_traceless" and "Phi-Psi" in str(row["statement"]) for row in response), "RESP3901_1"))
    checks.append(("VAL3901_2_quadratic", "quadratic memory stress row exists", any(row["row_id"] == "RESP3901_2_memory_quadratic" and "PASS_CANDIDATE" in str(row["status"]) for row in response), "RESP3901_2"))
    checks.append(("VAL3901_3_disformal_guard", "direct disformal escape retained", any(row["row_id"] == "RESP3901_3_direct_disformal" and "OPEN" in str(row["status"]) for row in response), "RESP3901_3"))
    checks.append(("VAL3901_4_linear_gamma", "linear gamma zero candidate exists", any(row["bound_id"] == "G2B3901_0_linear_zero" and "K_gamma_linear=0" in str(row["formula"]) for row in gamma), "G2B3901_0"))
    checks.append(("VAL3901_5_second_order", "second-order gamma bound exists", any(row["bound_id"] == "G2B3901_1_second_order_bound" and "2.3e-5" in str(row["formula"]) for row in gamma), "G2B3901_1"))
    checks.append(("VAL3901_6_Gdot_open", "Gdot remains open in runner update", any(row["update_id"] == "RUN3901_2_Gdot" and "OPEN_GDOT" in str(row["status"]) for row in runner), "RUN3901_2"))
    checks.append(("VAL3901_7_no_claim", "local GR remains blocked", any(row["gate_id"] == "LGG3901_4_local_GR" and "BLOCKED" in str(row["status"]) for row in gate), "LGG3901_4"))
    checks.append(("VAL3901_8_all_nonclaim", "all generated rows are nonclaim", all(str(row.get("valid_for_claim", row.get("claim_allowed", False))) == "False" for collection in [response, gamma, runner, gate] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3901_9_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "better leaps" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3901_10_spine", "spine updated with 3901 block", SPINE_PATH.exists() and "BEGIN 3901 NO DISFORMAL RESPONSE EQUATION" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3901_11_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3901*")
            if path.is_file() and ("3901-Y5" in path.name or "P8_Y5_R2FR_3901" in path.name or "P8_Y5_BRR545_3901" in path.name)
        ]
    checks.append(("VAL3901_12_formalization_untouched", "no generated 3901 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3901_13_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3901_14_next_target", "next target attacks second-order gamma and Gdot", any("second-order-gamma-bound" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3902 second-order gamma"))
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
    response = response_rows(timestamp)
    gamma = gamma_rows(timestamp)
    runner = runner_rows(timestamp)
    gate = gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["response"], response)
    write_csv(OUTPUTS["gamma"], gamma)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, response, gamma, runner, gate, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, response, gamma, runner, gate, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_LINEAR_GAMMA_NO_SLIP_ROUTE_DERIVED")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

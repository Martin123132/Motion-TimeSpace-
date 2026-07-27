from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4722"
CLAIM_ID = "L-564"
MARKER = "PPC4161_PARENT_TWO_DERIVATIVE_SIGNATURE_OR_R2_ALPHA_LAMBDA_RUNNER_4722"
PACKET_MARKER = "PPC4161_PACKET_PARENT_TWO_DERIVATIVE_SIGNATURE_OR_R2_ALPHA_LAMBDA_RUNNER_4722"
DECISION = "PARENT_EH_SIGNATURE_INSERTED_UNSIGNED_R2_ALPHA_LAMBDA_RUNNER_FAILS_CLOSED_NONCLAIM"
NEXT_TARGET = "4723-Y5-R2FR-parent-EH-signature-evidence-hunt-or-R2-mR-alpha-first-source-row.md"

DOC_PATH = POST / "4722-Y5-R2FR-parent-two-derivative-signature-insertion-or-R2-alpha-lambda-runner.md"
FORMAL_PATH = FORMAL / "738-PPC4161-parent-two-derivative-signature-insertion-or-R2-alpha-lambda-runner.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4722_SOURCE_REGISTER.csv"
SIGNATURE_INSERTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4722_PARENT_EH_SIGNATURE_INSERTION_AUDIT.csv"
R2_RUNNER_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4722_R2_ALPHA_LAMBDA_RUNNER_INPUT.csv"
R2_RUNNER_RESULTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4722_R2_ALPHA_LAMBDA_RUNNER_RESULTS.csv"
BOUND_CURVE_JOIN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4722_R2_R10_BOUND_CURVE_JOIN_STATUS.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4722_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4722_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4722_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4722_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4722_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4722_VALIDATION.csv"

CURVE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4635_R10_EOTWASH2020_VECTOR_DIGITIZED_CURVE.csv"


SOURCE_SPECS = [
    ("SRC4722_0", "P8_Y5_R2FR_4721_TWO_DERIVATIVE_EH_SELECTOR_PROOF_ROWS.csv", "TDEH4721_1_two_derivative_count", "4721 conditional two-derivative selector proof."),
    ("SRC4722_1", "P8_Y5_R2FR_4721_R2_SCALAR_RANGE_BOUND_ROW.csv", "R2F4721_0_scalaron_contract", "4721 R2/f(R) fallback scalar row."),
    ("SRC4722_2", "P8_Y5_R2FR_4721_R2_GAMMA_BETA_R10_PROJECTION_ROWS.csv", "R2P4721_0_R10_curve", "4721 R10 projection contract."),
    ("SRC4722_3", "P8_Y5_R2FR_4635_R10_EOTWASH2020_VECTOR_DIGITIZED_CURVE.csv", "R10_EOTWASH2020_ABS_ALPHA_VECTOR_FROM_FIG5B1", "Existing full vector-digitized R10 curve, nonclaim QA required."),
    ("SRC4722_4", "P8_Y5_R2FR_4635_R10_CURVE_STATUS_ROWS.csv", "FULL_VECTOR_CURVE_EXTRACTED_FROM_FIG5B1_NONCLAIM", "Curve status: usable for smoke but not claim-grade."),
    ("SRC4722_5", "P8_Y5_R2FR_4635_R10_SOURCE_ACQUISITION_LEDGER.csv", "VECTOR_DIGITIZED_FULL_CURVE_NONCLAIM_QA_REQUIRED", "Curve acquisition provenance."),
    ("SRC4722_6", "P8_Y5_R10_ALPHA_LAMBDA_PLACEHOLDER_REJECTION.csv", "PR558_0_missing_MTS_alpha", "Existing placeholder rejection rules."),
    ("SRC4722_7", "P8_Y5_R2FR_4720_PARENT_EH_SIGNATURE_CLAUSES.csv", "EHSC4720_2_two_derivative_IR", "Parent signature clauses from 4720."),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    separator = "\n\n" if existing and not existing.endswith("\n\n") else ""
    path.write_text(existing + separator + block.rstrip() + "\n", encoding="utf-8", newline="\n")


def source_register(ts: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, rel_path, needle, role in SOURCE_SPECS:
        path = SOURCE_DIR / rel_path
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": ts,
            }
        )
    return rows


def signature_insertion_rows(ts: str) -> list[dict[str, Any]]:
    rows = [
        ("SIG4722_0_geometry_domain", "Parent geometry domain contains one visible metric/coframe and compatible connection before readout.", "candidate_inserted", "needs parent source path or action clause"),
        ("SIG4722_1_two_derivative_IR", "Bulk principal local order is restricted to two derivatives.", "candidate_inserted", "R2/f(R), Ricci2 and Weyl2 remain unless parent signs exclusion"),
        ("SIG4722_2_no_extra_slots", "No scalar/vector/disformal/memory/source coefficient target exists in local collar.", "candidate_inserted", "must audit parent grammar for hidden coefficient targets"),
        ("SIG4722_3_torsion_resolution", "Torsion/nonmetricity are algebraic and vanish in compact spinless branch or are retained as coefficients.", "candidate_inserted", "not parent-signed globally"),
        ("SIG4722_4_boundary_topological", "Boundary/topological terms are fixed/source-blind and do not add bulk source charge.", "candidate_inserted", "needs boundary action/source-blind proof"),
        ("SIG4722_5_common_normalization", "M_EH and lambda_D are common normalizations, not relative source prefactors.", "candidate_inserted", "needs link to 4717/4718 parent signature"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "signature_id": signature_id,
            "clause": clause,
            "insertion_status": status,
            "remaining_evidence": remaining,
            "parent_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for signature_id, clause, status, remaining in rows
    ]


def selected_curve_points(limit: int = 5) -> list[dict[str, str]]:
    if not CURVE_CSV.exists():
        return []
    with CURVE_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [r for r in csv.DictReader(handle) if r.get("component_id") == "PURPLE_COMPONENT_0"]
    if not rows:
        return []
    indexes = sorted(set([0, len(rows) // 4, len(rows) // 2, (3 * len(rows)) // 4, len(rows) - 1]))[:limit]
    return [rows[i] for i in indexes]


def r2_runner_input_rows(ts: str) -> list[dict[str, Any]]:
    points = selected_curve_points()
    rows: list[dict[str, Any]] = []
    if not points:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "runner_row_id": "R2RUN4722_NO_CURVE",
                "branch": "R2_fR_scalar_fallback",
                "lambda_m": "MISSING_R10_CURVE",
                "alpha_predicted": "MISSING_PARENT_ALPHA_R",
                "alpha_bound": "MISSING_ALPHA_BOUND",
                "m_R_source": "MISSING_PARENT_MASS",
                "alpha_R_source": "MISSING_PARENT_COUPLING",
                "derivation_status": "blocked_missing_curve",
                "valid_for_claim": False,
                "timestamp_utc": ts,
            }
        )
        return rows
    for idx, point in enumerate(points):
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "runner_row_id": f"R2RUN4722_{idx}_pure_fR_missing_lambda",
                "branch": "R2_fR_scalar_fallback",
                "lambda_m": point["lambda_m"],
                "alpha_predicted": "MISSING_PARENT_ALPHA_R_OR_THEOREM_ZERO",
                "alpha_bound": point["alpha_bound_abs"],
                "m_R_source": "MISSING_PARENT_MASS_OR_a_R2",
                "alpha_R_source": "MISSING_PARENT_SCALAR_CHARGE_OR_SELECTOR_ZERO",
                "derivation_status": "curve_bound_present_MTS_R2_inputs_missing",
                "valid_for_claim": False,
                "timestamp_utc": ts,
            }
        )
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "runner_row_id": "R2RUN4722_SELECTOR_ZERO_UNSIGNED",
            "branch": "two_derivative_EH_selector_zero",
            "lambda_m": "all",
            "alpha_predicted": "0_CONDITIONAL_IF_PARENT_SELECTOR_SIGNED",
            "alpha_bound": "not_needed_if_exact_zero",
            "m_R_source": "selector_excludes_R2",
            "alpha_R_source": "selector_excludes_scalaron",
            "derivation_status": "conditional_theorem_zero_parent_unsigned",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    )
    return rows


def runner_result_rows(ts: str, input_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for row in input_rows:
        alpha = str(row["alpha_predicted"])
        if alpha.startswith("0_CONDITIONAL"):
            verdict = "BLOCKED_SELECTOR_UNSIGNED"
            passes = False
        elif "MISSING" in alpha:
            verdict = "BLOCKED_MISSING_PARENT_ALPHA_OR_MASS"
            passes = False
        else:
            try:
                passes = abs(float(alpha)) <= float(row["alpha_bound"])
                verdict = "PASS_NUMERIC_NONCLAIM" if passes else "FAIL_NUMERIC_NONCLAIM"
            except Exception:
                passes = False
                verdict = "BLOCKED_NONNUMERIC_INPUT"
        results.append(
            {
                "checkpoint": CHECKPOINT,
                "runner_row_id": row["runner_row_id"],
                "verdict": verdict,
                "passes_bound": passes,
                "claim_allowed": False,
                "valid_for_claim": False,
                "reason": "parent selector unsigned or R2 m_R/alpha_R inputs missing; curve is smoke-grade nonclaim",
                "timestamp_utc": ts,
            }
        )
    return results


def curve_join_rows(ts: str, input_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    numeric_bound_rows = [r for r in input_rows if str(r["alpha_bound"]).replace(".", "", 1).replace("e", "", 1).replace("-", "", 1).replace("+", "", 1).isdigit()]
    return [
        {
            "checkpoint": CHECKPOINT,
            "join_id": "CURVEJOIN4722_0_bound_side",
            "status": "bound_curve_joined_for_smoke" if numeric_bound_rows else "bound_curve_missing",
            "row_count": len(numeric_bound_rows),
            "source_curve": str(CURVE_CSV),
            "claim_grade": "nonclaim_vector_digitized_QA_required",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "join_id": "CURVEJOIN4722_1_MTS_side",
            "status": "MTS_R2_alpha_lambda_inputs_missing",
            "row_count": len(input_rows),
            "source_curve": str(R2_RUNNER_INPUT_CSV),
            "claim_grade": "blocked_until_mR_alphaR_or_selector_zero_parent_signed",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def gate_rows(ts: str) -> list[dict[str, Any]]:
    rows = [
        ("GATE4722_0_parent_signature_signed", "Parent EH/two-derivative signature is source-backed and adopted.", "PARENT_SIGNATURE_UNSIGNED"),
        ("GATE4722_1_R2_inputs_numeric", "m_R or a_R2 and alpha_R/zeta_R are numeric or theorem-zero with source paths.", "R2_PARENT_INPUTS_MISSING"),
        ("GATE4722_2_curve_claim_grade", "R10 curve is official or manually QA-promoted claim-grade.", "CURVE_QA_NONCLAIM"),
        ("GATE4722_3_runner_numeric_pass", "Every numeric alpha(lambda) row passes its bound without placeholders.", "RUNNER_BLOCKED_FAIL_CLOSED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "requirement": req,
            "passed": False,
            "blocker": blocker,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for gate_id, req, blocker in rows
    ]


def firewall_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4722_0_no_curve_only_pass",
            "rule": "A digitized bound curve alone is not an MTS prediction.",
            "reason": "MTS must supply m_R/lambda_R and alpha_R or a parent theorem-zero.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": "FW4722_1_no_conditional_zero_claim",
            "rule": "The selector-zero row is not a claim until the parent signature is signed.",
            "reason": "4721 proved sufficiency, not parent adoption.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def decision_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4722_0",
            "decision": DECISION,
            "meaning": "The parent EH signature has been inserted as a concrete audit but remains unsigned. The R2 alpha(lambda) smoke runner can join the existing bound curve, but it fails closed because the MTS-side m_R/alpha_R or theorem-zero certificate is missing.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4722_0",
            "status": "private_nonclaim_signature_inserted_runner_blocked",
            "summary": "Parent EH signature insertion audit created; R2 alpha(lambda) runner input/results created; bound curve side exists for smoke but MTS R2 inputs are missing.",
            "claim_allowed": False,
            "timestamp_utc": ts,
        }
    ]


def next_target_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4722_0",
            "next_target": NEXT_TARGET,
            "why": "The split is now exact: either find parent evidence that signs the EH selector, or source the first R2 scalar mass/coupling row.",
            "derive_first": "hunt parent files for explicit two-derivative/no-extra-slot EH signature evidence",
            "fallback": "source or derive m_R/a_R2 and alpha_R/zeta_R for the R2 scalar row, then rerun alpha(lambda)",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def write_docs(ts: str, sources: list[dict[str, Any]], signature: list[dict[str, Any]], inputs: list[dict[str, Any]], results: list[dict[str, Any]], joins: list[dict[str, Any]], gates: list[dict[str, Any]]) -> None:
    source_lines = "\n".join(f"- `{r['source_id']}`: `{r['source_path']}`; exists={r['exists']}; needle_found={r['needle_found']}; role={r['role']}" for r in sources)
    signature_lines = "\n".join(f"- `{r['signature_id']}`: {r['clause']} Status: `{r['insertion_status']}`; remaining: {r['remaining_evidence']}." for r in signature)
    input_lines = "\n".join(f"- `{r['runner_row_id']}`: lambda=`{r['lambda_m']}`, alpha=`{r['alpha_predicted']}`, bound=`{r['alpha_bound']}`." for r in inputs[:8])
    result_lines = "\n".join(f"- `{r['runner_row_id']}`: `{r['verdict']}`." for r in results[:8])
    join_lines = "\n".join(f"- `{r['join_id']}`: `{r['status']}`; rows={r['row_count']}; grade=`{r['claim_grade']}`." for r in joins)
    gate_lines = "\n".join(f"- `{r['gate_id']}`: passed={r['passed']}; blocker=`{r['blocker']}`." for r in gates)

    write_text(
        DOC_PATH,
        f"""# 4722 - Parent Two-Derivative Signature Insertion or R2 Alpha-Lambda Runner

Generated: `{ts}`

## Purpose

4721 proved the conditional two-derivative EH selector and staged the `R2/f(R)` scalar fallback. 4722 makes that fork executable:

- insert the parent EH selector signature as an audit target;
- create a fail-closed `R2` `alpha(lambda)` smoke runner input;
- join the existing Eot-Wash 2020 vector-digitized curve only as nonclaim smoke evidence.

## Parent Signature Insertion Audit

{signature_lines}

## R2 Alpha-Lambda Runner Input

{input_lines}

## Runner Results

{result_lines}

## Curve Join Status

{join_lines}

## Gates

{gate_lines}

## Source Register

{source_lines}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
""",
    )

    write_text(
        FORMAL_PATH,
        f"""# PPC4161 4722 - Parent EH Signature / R2 Alpha-Lambda Runner

Generated: `{ts}`

## Result

The parent EH selector signature is now an explicit insertion audit, but it remains unsigned.

The `R2/f(R)` fallback runner joins a smoke-grade R10 bound curve and fails closed because MTS has not supplied:

- `m_R` or `a_R2`;
- `alpha_R` or `zeta_R`;
- a parent theorem-zero excluding the scalaron.

## Nonclaim Boundary

Bound data existing on the experimental side does not make an MTS prediction. The MTS side must provide numeric/theorem-zero `R2` inputs before any local/R10 statement can be scored.

## Decision

`{DECISION}`

## Next

`{NEXT_TARGET}`
""",
    )


def update_claims(ts: str) -> None:
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    if CLAIM_ID in {row.get("claim_id", "") for row in rows}:
        return
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4722 inserts the parent two-derivative EH signature audit and builds a fail-closed R2 alpha(lambda) runner input/results pair using the existing nonclaim R10 curve.",
        "current_evidence": "Generated source register, signature insertion audit, R2 runner input/results, curve join status, gates, firewalls, decision, status, next target and validation.",
        "status": "EH_signature_unsigned_R2_runner_blocked_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Mistaking a bound curve or conditional selector-zero row for an MTS prediction before m_R/alpha_R or parent selector evidence exists.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "",
        "title": "Parent two-derivative signature insertion or R2 alpha-lambda runner",
        "notes": f"{MARKER}; {DECISION}; generated {ts}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.DictWriter(handle, fieldnames=fieldnames).writerow(new_row)


def update_resume(ts: str) -> None:
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Updated: `{ts}`

## Latest completed checkpoint

`4722-Y5-R2FR-parent-two-derivative-signature-insertion-or-R2-alpha-lambda-runner.md`

## Decision

`{DECISION}`

## What moved forward

- Parent EH selector signature is now an explicit audit target.
- R2 alpha(lambda) smoke runner input and fail-closed results exist.
- The bound-curve side exists for smoke via the 4635 vector-digitized curve, but it is not claim-grade.
- The MTS side is blocked until `m_R/a_R2`, `alpha_R/zeta_R`, or a parent selector-zero certificate is sourced.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
""",
    )


def validation_rows(ts: str, sources: list[dict[str, Any]], signature: list[dict[str, Any]], inputs: list[dict[str, Any]], results: list[dict[str, Any]], joins: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4722_sources_exist", all(r["exists"] for r in sources), "all cited local source paths exist"),
        ("VAL4722_needles_found", all(r["needle_found"] for r in sources), "all cited source needles found"),
        ("VAL4722_signature_inserted", len(signature) >= 6 and any(r["signature_id"] == "SIG4722_1_two_derivative_IR" for r in signature), "signature insertion audit rows present"),
        ("VAL4722_runner_input", len(inputs) >= 2 and any("MISSING" in str(r["alpha_predicted"]) for r in inputs), "R2 runner input rows present and fail-closed"),
        ("VAL4722_runner_results_block", len(results) == len(inputs) and all(not bool(r["passes_bound"]) for r in results), "runner results block all rows"),
        ("VAL4722_curve_join", any(r["join_id"] == "CURVEJOIN4722_0_bound_side" and int(r["row_count"]) > 0 for r in joins), "bound curve joined for smoke"),
        ("VAL4722_gates_not_passing", not all(bool(r["passed"]) for r in gates), "promotion gates not all passing"),
        ("VAL4722_no_claim_allowed", all(not bool(r.get("valid_for_claim")) for r in sources + signature + inputs + results + joins + gates), "no row allows a claim"),
        ("VAL4722_doc_written", DOC_PATH.exists() and DOC_PATH.stat().st_size > 1000, "checkpoint document written"),
        ("VAL4722_formal_written", FORMAL_PATH.exists() and FORMAL_PATH.stat().st_size > 500, "formal packet document written"),
        ("VAL4722_no_pycache", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": check_id,
            "passed": passed,
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4722_OVERALL",
            "passed": overall,
            "detail": "4722 artifacts validate as private nonclaim parent-signature/R2-runner checkpoint",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    )
    return rows


def main() -> None:
    ts = now()
    sources = source_register(ts)
    signature = signature_insertion_rows(ts)
    inputs = r2_runner_input_rows(ts)
    results = runner_result_rows(ts, inputs)
    joins = curve_join_rows(ts, inputs)
    gates = gate_rows(ts)
    firewalls = firewall_rows(ts)
    decisions = decision_rows(ts)
    statuses = status_rows(ts)
    next_targets = next_target_rows(ts)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(SIGNATURE_INSERTION_CSV, signature)
    write_csv(R2_RUNNER_INPUT_CSV, inputs)
    write_csv(R2_RUNNER_RESULTS_CSV, results)
    write_csv(BOUND_CURVE_JOIN_CSV, joins)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)

    write_docs(ts, sources, signature, inputs, results, joins, gates)
    update_claims(ts)
    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Derivation gain: parent EH selector signature is an explicit audit target; R2 alpha(lambda) runner fails closed with existing nonclaim curve data and missing MTS-side mass/coupling inputs.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: connects the two-derivative EH selector fork to a fail-closed R2/f(R) R10 smoke runner input/results pair.
- Validation: `{VALIDATION_CSV}`.
""",
    )
    update_resume(ts)

    shutil.rmtree(POST / "scripts" / "__pycache__", ignore_errors=True)
    write_csv(VALIDATION_CSV, validation_rows(ts, sources, signature, inputs, results, joins, gates))


if __name__ == "__main__":
    main()

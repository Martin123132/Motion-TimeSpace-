from __future__ import annotations

import csv
import math
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1004-Y5-R10-Bref-range-independence-theorem-or-Delta-ref-lambda-profile-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "S1004_0_handoff_doc",
            "path": "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
            "role": "1003 handoff selecting range/lambda derivative target",
            "needle": "1004-Y5-R10-Bref-range-independence-theorem-or-Delta-ref-lambda-profile-row.md",
        },
        {
            "source_id": "S1004_1_next_target",
            "path": "source-intake/mts_residuals/P8_Y5_R10_1003_NEXT_TARGET.csv",
            "role": "machine-readable 1004 target",
            "needle": "partial_lambda Delta_ref",
        },
        {
            "source_id": "S1004_2_derivative_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_997_DERIVATIVE_COMPONENT_AUDIT.csv",
            "role": "lambda/range derivative blocker from 997",
            "needle": "DVC997_4_lambda",
        },
        {
            "source_id": "S1004_3_range_gate",
            "path": "source-intake/mts_residuals/P8_Y5_R10_746_R10_RANGE_GATE.csv",
            "role": "R10 finite-range gate",
            "needle": "R10Q746_1_no_range_zero",
        },
        {
            "source_id": "S1004_4_cokernel_theorem",
            "path": "source-intake/mts_residuals/P8_Y5_R10_831_RANGE_COKERNEL_THEOREM.csv",
            "role": "range/cokernel theorem attempt",
            "needle": "RT831_2_exact_zero",
        },
        {
            "source_id": "S1004_5_cokernel_template",
            "path": "source-intake/mts_residuals/P8_Y5_R10_831_RANGE_RUNNER_INPUT_TEMPLATE.csv",
            "role": "range runner missing-input template",
            "needle": "template_missing_range_inputs",
        },
        {
            "source_id": "S1004_6_cokernel_runner",
            "path": "source-intake/mts_residuals/P8_Y5_R10_831_RANGE_RUNNER_OUTPUT.csv",
            "role": "range runner blocked output",
            "needle": "blocked_missing_inputs",
        },
        {
            "source_id": "S1004_7_range_demotion",
            "path": "source-intake/mts_residuals/P8_Y5_R10_616_RANGE_CLOSURE_DEMOTION_GATE.csv",
            "role": "range-closure demotion gate",
            "needle": "DG616_5_no_R10_promotion",
        },
        {
            "source_id": "S1004_8_lambda_windows",
            "path": "source-intake/mts_residuals/P8_Y5_R10_611_ALLOWED_LAMBDA_WINDOWS.csv",
            "role": "review-candidate lambda windows",
            "needle": "review_candidate_nonclaim_pressure",
        },
        {
            "source_id": "S1004_9_lambda_ceiling",
            "path": "source-intake/mts_residuals/P8_Y5_R10_612_LAMBDA_CX_CEILING_TABLE.csv",
            "role": "review-candidate lambda/C_X ceilings",
            "needle": "pressure_verdict",
        },
        {
            "source_id": "S1004_10_curve_contract",
            "path": "437-R10-alpha-lambda-executable-curve-contract.md",
            "role": "R10 alpha(lambda) executable curve contract",
            "needle": "R10_alpha_lambda_executable_curve_contract_written_theorem_zero_or_curve_required_no_R10_pass_no_local_GR_pass",
        },
        {
            "source_id": "S1004_11_no_cancellation",
            "path": "source-intake/mts_residuals/P8_Y5_R10_994_DELTAH_NO_CANCELLATION_ENVELOPE.csv",
            "role": "absolute residual envelope",
            "needle": "DHE994_1_no_cancellation",
        },
        {
            "source_id": "S1004_12_prior_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_1003_VALIDATION.csv",
            "role": "1003 validation pass",
            "needle": "V1003_SUMMARY",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        path = source_path(spec["path"])
        text = read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(path.exists()),
                "needle_found": flag(spec["needle"] in text),
                "valid_for_claim": "false",
            }
        )
    return rows


def range_independence_theorem_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "RIA1004_0_quantity",
            "object": "partial_lambda Delta_ref",
            "needed_for_zero": "B_ref and H_ref must not depend on R10 range, memory, domain, or sector-scale parameters",
            "current_evidence": "997 flags MISSING_RANGE_INDEPENDENCE_RULE",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "RIA1004_1_predeclared_reference",
            "object": "B_ref lambda-independence",
            "needed_for_zero": "reference branch is fixed before any alpha(lambda), R10 bound, or lambda-window comparison",
            "current_evidence": "MISSING_PARENT_BREF_RANGE_INDEPENDENCE_CERTIFICATE",
            "status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "RIA1004_2_no_range_kernel",
            "object": "finite-range source kernel",
            "needed_for_zero": "q_loc has no local compact finite-range source kernel in the GR branch",
            "current_evidence": "746 marks c_q_alpha(lambda)=0 as not derived",
            "status": "fail_current_claim",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "RIA1004_3_cokernel_obstruction",
            "object": "range/cokernel residual",
            "needed_for_zero": "P_coker(D_T)G=0 with no boundary or regularizer obstruction",
            "current_evidence": "831 reduces the problem to a theorem, but the runner output is blocked by missing inputs",
            "status": "conditional_only",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "RIA1004_4_memory_domain_sector_scales",
            "object": "memory/domain/sector scale dependence",
            "needed_for_zero": "lambda, memory scale, domain selector scale, and sector scale are not hidden arguments of B_ref/H_ref",
            "current_evidence": "MISSING_SCALE_SEPARATION_AND_DOMAIN_SELECTOR_CERTIFICATE",
            "status": "unsigned",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "RIA1004_5_review_windows_nonclaim",
            "object": "lambda windows and C_X ceilings",
            "needed_for_zero": "empirical windows may pressure a branch but cannot derive range independence",
            "current_evidence": "611/612 are review-candidate nonclaim pressure rows",
            "status": "evidence_mapping_only",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "RIA1004_6_theorem_verdict",
            "object": "partial_lambda Delta_ref = 0",
            "needed_for_zero": "predeclared B_ref/H_ref, no-range-kernel, cokernel-zero, boundary silence, regularizer silence, and scale-separation clauses parent-signed",
            "current_evidence": "not enough parent range/domain-scale geometry to promote zero",
            "status": "fail_current_claim",
            "valid_for_claim": "false",
        },
    ]


def lambda_profile_schema_rows() -> list[dict[str, str]]:
    return [
        {
            "schema_id": "LPS1004_0_profile_formula",
            "target": "Delta_ref_lambda_profile_over_MH",
            "formula": "abs(partial_lambda_Delta_ref * Delta_lambda_profile)/M_H_ref",
            "required_columns": "system_id;lambda_parameter;lambda_units;Delta_lambda_profile;partial_lambda_Delta_ref;Delta_ref_units;M_H_ref;M_H_ref_units;B_ref_range_independence_certificate;H_ref_range_independence_certificate;scale_separation_certificate;range_kernel_certificate;cokernel_certificate;boundary_certificate;source_path;equation_ref;valid_for_claim",
            "acceptance_rule": "finite same-frame ratio or theorem_zero=true with parent-signed range-independence theorem; no MISSING markers",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "LPS1004_1_range_zero_switch",
            "target": "partial_lambda_Delta_ref_zero",
            "formula": "theorem_zero=true iff lambda_zero_authority=PARENT_SIGNED_RANGE_INDEPENDENCE_TRUE",
            "required_columns": "B_ref_range_independence_certificate;H_ref_range_independence_certificate;no_range_kernel_certificate;cokernel_zero_certificate;boundary_silence_certificate;regularizer_silence_certificate;scale_separation_certificate;source_path;equation_ref",
            "acceptance_rule": "range independence by notation, fitted lambda choice, and review-window survival are rejected",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "LPS1004_2_range_cokernel_fallback",
            "target": "epsilon_range_lambda_to_lambda_profile_bridge",
            "formula": "Delta_ref_lambda_profile_over_MH <= C_lambda*(q_cokernel_bound+q_boundary_bound+q_regularizer_bound+epsilon_range_kernel) when every term is sourced",
            "required_columns": "G_norm;cokernel_fraction;boundary_obstruction_norm;regularizer_norm;coercivity_inverse;kappa_K;epsilon_range_kernel;C_lambda;M_H_ref;units;source_path;equation_ref",
            "acceptance_rule": "fallback is nonclaim until all range/cokernel/boundary/regularizer components are numeric, sourced, same-frame, and absolute-summed",
            "valid_for_claim": "false",
        },
        {
            "schema_id": "LPS1004_3_no_cancellation",
            "target": "lambda contribution to residual envelope",
            "formula": "absolute values only",
            "required_columns": "no_cancellation_guard=ABS_PRODUCT_NO_SIGN_CANCELLATION",
            "acceptance_rule": "no sign cancellation, fitted lambda cancellation, or range-window cherry-picking",
            "valid_for_claim": "false",
        },
    ]


def candidate_lambda_profile_rows() -> list[dict[str, str]]:
    base = {
        "system_id": "R10_local_reference_branch",
        "lambda_parameter": "MISSING_LAMBDA_PARAMETER",
        "lambda_units": "MISSING_LAMBDA_UNITS",
        "Delta_lambda_profile": "MISSING_DELTA_LAMBDA_PROFILE",
        "Delta_lambda_units": "MISSING_DELTA_LAMBDA_UNITS",
        "partial_lambda_Delta_ref": "MISSING_PARTIAL_LAMBDA_DELTA_REF",
        "partial_lambda_units": "MISSING_PARTIAL_LAMBDA_UNITS",
        "Delta_ref_units": "MISSING_DELTA_REF_UNITS",
        "M_H_ref": "MISSING_M_H_REF",
        "M_H_ref_units": "MISSING_M_H_REF_UNITS",
        "B_ref_range_independence_certificate": "MISSING_B_REF_RANGE_INDEPENDENCE_CERTIFICATE",
        "H_ref_range_independence_certificate": "MISSING_H_REF_RANGE_INDEPENDENCE_CERTIFICATE",
        "scale_separation_certificate": "MISSING_SCALE_SEPARATION_CERTIFICATE",
        "range_kernel_certificate": "MISSING_RANGE_KERNEL_CERTIFICATE",
        "cokernel_certificate": "MISSING_COKERNEL_CERTIFICATE",
        "boundary_certificate": "MISSING_BOUNDARY_CERTIFICATE",
        "regularizer_certificate": "MISSING_REGULARIZER_CERTIFICATE",
        "source_path": "MISSING_SOURCE_FILE",
        "equation_ref": "MISSING_EQUATION_REF",
        "theorem_zero": "false",
        "lambda_zero_authority": "MISSING_PARENT_RANGE_SIGNATURE",
        "G_norm": "MISSING_G_NORM",
        "cokernel_fraction": "MISSING_COKERNEL_FRACTION",
        "boundary_obstruction_norm": "MISSING_BOUNDARY_OBSTRUCTION_NORM",
        "regularizer_norm": "MISSING_REGULARIZER_NORM",
        "coercivity_inverse": "MISSING_COERCIVITY_INVERSE",
        "kappa_K": "MISSING_KAPPA_K",
        "epsilon_range_kernel": "MISSING_EPSILON_RANGE_KERNEL",
        "C_lambda": "MISSING_C_LAMBDA",
        "observable_response_norm": "MISSING_OBSERVABLE_RESPONSE_NORM",
        "observable_limit": "MISSING_OBSERVABLE_LIMIT",
        "no_cancellation_guard": "MISSING_ABSOLUTE_PRODUCT_GUARD",
        "valid_for_claim": "false",
    }
    variants = [
        ("LPT1004_0_missing_range_independence", "B_ref/H_ref range-independence certificate is absent"),
        ("LPT1004_1_missing_lambda_derivative", "partial_lambda Delta_ref is not finite or theorem-zero"),
        ("LPT1004_2_missing_lambda_profile", "Delta_lambda profile is not sourced"),
        ("LPT1004_3_missing_MHref", "positive same-frame M_H_ref denominator is missing"),
        ("LPT1004_4_zero_switch_unsigned", "theorem-zero switch is requested without parent-signed range independence"),
        ("LPT1004_5_missing_cokernel_boundary_regularizer", "range/cokernel/boundary/regularizer fallback components are not sourced"),
        ("LPT1004_6_missing_observable_projection", "lambda-profile row has no arena projection or empirical limit"),
        ("LPT1004_7_all_missing_live_placeholder", "live lambda row is schema-only and cannot be scored"),
    ]
    rows: list[dict[str, str]] = []
    for row_id, purpose in variants:
        row = {**base, "candidate_id": row_id, "target": "Delta_ref_lambda_profile_over_MH", "purpose": purpose}
        if row_id == "LPT1004_4_zero_switch_unsigned":
            row["theorem_zero"] = "true"
            row["lambda_zero_authority"] = "MISSING_PARENT_RANGE_SIGNATURE"
        rows.append(row)
    return rows


def is_missing(value: str) -> bool:
    stripped = str(value).strip()
    return not stripped or stripped.upper().startswith("MISSING") or stripped.upper().startswith("SCHEMA_ONLY")


def finite_float(value: str) -> tuple[bool, float | None]:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False, None
    return math.isfinite(number), number


def path_exists(value: str) -> bool:
    if is_missing(value):
        return False
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / value
    return path.exists()


def evaluate_lambda_profile(row: dict[str, str]) -> dict[str, str]:
    reasons: list[str] = []
    derivative_ok, derivative = finite_float(row.get("partial_lambda_Delta_ref", ""))
    theorem_zero = row.get("theorem_zero", "").strip().lower() == "true"
    parent_signed_lambda_zero = theorem_zero and row.get("lambda_zero_authority") == "PARENT_SIGNED_RANGE_INDEPENDENCE_TRUE"
    if not derivative_ok and not parent_signed_lambda_zero:
        reasons.append("MISSING_PARTIAL_LAMBDA_DELTA_REF_OR_PARENT_SIGNED_RANGE_ZERO")
    if theorem_zero and not parent_signed_lambda_zero:
        reasons.append("THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNED_RANGE_INDEPENDENCE")
    delta_lambda_ok, delta_lambda = finite_float(row.get("Delta_lambda_profile", ""))
    if not delta_lambda_ok or delta_lambda is None or delta_lambda <= 0:
        reasons.append("MISSING_POSITIVE_DELTA_LAMBDA_PROFILE")
    mh_ok, mh = finite_float(row.get("M_H_ref", ""))
    if not mh_ok or mh is None or mh <= 0:
        reasons.append("MISSING_POSITIVE_SAME_FRAME_M_H_REF")
    for field in [
        "system_id",
        "lambda_parameter",
        "lambda_units",
        "Delta_lambda_units",
        "partial_lambda_units",
        "Delta_ref_units",
        "M_H_ref_units",
        "B_ref_range_independence_certificate",
        "H_ref_range_independence_certificate",
        "scale_separation_certificate",
        "range_kernel_certificate",
        "cokernel_certificate",
        "boundary_certificate",
        "regularizer_certificate",
        "equation_ref",
    ]:
        if is_missing(row.get(field, "")):
            reasons.append(f"MISSING_{field.upper()}")
    component_fields = [
        "G_norm",
        "cokernel_fraction",
        "boundary_obstruction_norm",
        "regularizer_norm",
        "coercivity_inverse",
        "kappa_K",
        "epsilon_range_kernel",
        "C_lambda",
        "observable_response_norm",
        "observable_limit",
    ]
    components_ok = True
    for field in component_fields:
        ok, value = finite_float(row.get(field, ""))
        if not ok or value is None:
            components_ok = False
            reasons.append(f"MISSING_RANGE_COMPONENT_{field.upper()}")
        elif value < 0:
            components_ok = False
            reasons.append(f"NEGATIVE_RANGE_COMPONENT_{field.upper()}")
    if not parent_signed_lambda_zero and not components_ok:
        reasons.append("MISSING_RANGE_COKERNEL_FALLBACK_BOUND")
    if not path_exists(row.get("source_path", "")):
        reasons.append("MISSING_EXISTING_SOURCE_PATH")
    if row.get("no_cancellation_guard") != "ABS_PRODUCT_NO_SIGN_CANCELLATION":
        reasons.append("MISSING_NO_CANCELLATION_GUARD")
    if row.get("valid_for_claim") != "true":
        reasons.append("VALID_FOR_CLAIM_FALSE")
    numeric_ratio = "NOT_SCORED"
    if not reasons and derivative is not None and delta_lambda is not None and mh is not None:
        numeric_ratio = f"{abs(derivative * delta_lambda) / mh:.16e}"
    verdict = "ACCEPT_NUMERIC_OR_PARENT_SIGNED_RANGE_ZERO" if not reasons else "REFUSED_MISSING_RANGE_INDEPENDENCE_PROVENANCE"
    return {
        "runner_id": row["candidate_id"].replace("LPT", "LPR"),
        "candidate_id": row["candidate_id"],
        "target": row["target"],
        "verdict": verdict,
        "score_ready": flag(not reasons),
        "claim_allowed": "false",
        "valid_for_claim": "false",
        "computed_abs_ratio": numeric_ratio,
        "failure_reasons": ";".join(reasons) if reasons else "none",
        "generated_utc": stamp(),
    }


def lambda_profile_runner_rows(candidates: list[dict[str, str]]) -> list[dict[str, str]]:
    return [evaluate_lambda_profile(row) for row in candidates]


def refusal_ledger_rows(runner: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "refusal_id": row["runner_id"].replace("LPR", "LRF"),
            "candidate_id": row["candidate_id"],
            "refusal": row["verdict"],
            "why": row["failure_reasons"],
            "required_exit": "parent-signed range-independence theorem or finite lambda-profile coefficient with range/cokernel fallback, units, source, and equation path",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        }
        for row in runner
    ]


def claim_gate_rows(runner: list[dict[str, str]], theorem: list[dict[str, str]]) -> list[dict[str, str]]:
    runner_refuses = all(row["verdict"] == "REFUSED_MISSING_RANGE_INDEPENDENCE_PROVENANCE" for row in runner)
    theorem_fails = any(row["audit_id"] == "RIA1004_6_theorem_verdict" and row["status"] == "fail_current_claim" for row in theorem)
    return [
        {
            "gate_id": "CG1004_0_partial_lambda_Delta_ref_zero",
            "claim": "partial_lambda Delta_ref = 0",
            "gate_pass": "false",
            "reason": "B_ref/H_ref range independence, no-range-kernel, cokernel-zero, boundary silence, regularizer silence, and scale separation are unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1004_1_Delta_ref_lambda_profile_bound",
            "claim": "Delta_ref_lambda_profile_over_MH is bounded",
            "gate_pass": "false",
            "reason": "lambda derivative/profile/M_H_ref/range-cokernel inputs are placeholder-only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1004_2_range_cokernel_bound",
            "claim": "range/cokernel fallback supplies a valid local bound",
            "gate_pass": "false",
            "reason": "831 defines the reduction but missing-input runner blocks quantitative claim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1004_3_derivative_vector",
            "claim": "all five Delta_ref derivative components are zero or source-bounded",
            "gate_pass": "false",
            "reason": "source/radius/time/frame/lambda components are now guarded but none are parent-zero or numerically source-bounded",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1004_4_RC994_0",
            "claim": "RC994_0 residual current passes",
            "gate_pass": "false",
            "reason": "Delta_ref derivative vector and M_H_ref denominator remain nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1004_5_local_GR_branch",
            "claim": "local-GR branch passes",
            "gate_pass": "false",
            "reason": "R10 residual vector is fully scaffolded but not zero or source-bounded",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "CG1004_6_guardrail",
            "claim": "range/lambda guardrail is installed",
            "gate_pass": flag(runner_refuses and theorem_fails),
            "reason": "theorem is not promoted and all placeholder rows are refused",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1004_0_theorem_not_closed",
            "decision": "do not claim partial_lambda Delta_ref = 0",
            "reason": "range independence is still a parent-action/cokernel theorem target, not a signed result",
            "effect": "lambda derivative remains a nonclaim closure or source-bound input",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1004_1_lambda_profile_staged",
            "decision": "stage Delta_ref_lambda_profile_over_MH as the fallback row",
            "reason": "if range independence cannot be closed, retained lambda/range components must be source-backed and absolute-summed",
            "effect": "future proof/data can fill the row without weakening the gate",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1004_2_next_vector_target",
            "decision": "aggregate the five derivative components into a strict vector-norm gate",
            "reason": "1000-1004 now guard source, radius, time, frame, and lambda components",
            "effect": "1005 should compute/refuse ||D_ref Delta_ref||_1/M_H_ref and keep RC994_0/local-GR blocked unless every component is parent-zero or source-bounded",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1005-Y5-R10-Delta-ref-derivative-vector-norm-gate.md",
            "objective": "aggregate source, radius, time, frame, and lambda Delta_ref components into a strict ||D_ref Delta_ref||_1/M_H_ref gate",
            "include": "component CSVs from 1000-1004, M_H_ref, absolute-value sum, per-component theorem-zero/source-bound flags, RC994_0 and local-GR claim gates",
            "exclude": "component cancellation, closure-only zeros, missing M_H_ref, RC994_0 pass, FB554_0 pass, local-GR claim, GitHub action",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_timestamp = SCRIPT_START_UTC.timestamp()
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                if path.stat().st_mtime > start_timestamp:
                    count += 1
            except OSError:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    schema: list[dict[str, str]],
    candidates: list[dict[str, str]],
    runner: list[dict[str, str]],
    refusals: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    theorem_ok = any(row["audit_id"] == "RIA1004_6_theorem_verdict" and row["status"] == "fail_current_claim" for row in theorem) and all(row["valid_for_claim"] == "false" for row in theorem)
    schema_ok = any(row["target"] == "Delta_ref_lambda_profile_over_MH" for row in schema) and any("PARENT_SIGNED_RANGE_INDEPENDENCE_TRUE" in row["formula"] for row in schema)
    candidates_ok = len(candidates) >= 8 and all(row["valid_for_claim"] == "false" for row in candidates)
    runner_ok = all(row["verdict"] == "REFUSED_MISSING_RANGE_INDEPENDENCE_PROVENANCE" and row["score_ready"] == "false" for row in runner)
    zero_switch_ok = any(
        row["candidate_id"] == "LPT1004_4_zero_switch_unsigned"
        and "THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNED_RANGE_INDEPENDENCE" in row["failure_reasons"]
        for row in runner
    )
    fallback_ok = any("MISSING_RANGE_COKERNEL_FALLBACK_BOUND" in row["failure_reasons"] for row in runner)
    components_ok = any("MISSING_RANGE_COMPONENT_G_NORM" in row["failure_reasons"] for row in runner)
    refusals_ok = len(refusals) == len(runner) and all(row["claim_allowed"] == "false" for row in refusals)
    claims_ok = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claims)
    vector_gate_ok = any(row["gate_id"] == "CG1004_3_derivative_vector" and row["gate_pass"] == "false" for row in claims)
    decisions_ok = any(row["decision_id"] == "DEC1004_2_next_vector_target" for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V1004_0_sources_exist", "result": "pass" if sources_ok else "fail", "detail": "all source paths exist and needles are present"},
        {"check_id": "V1004_1_theorem_audit_nonclaim", "result": "pass" if theorem_ok else "fail", "detail": "range/lambda zero theorem remains blocked rather than promoted"},
        {"check_id": "V1004_2_schema_ready", "result": "pass" if schema_ok else "fail", "detail": "lambda profile and range-independence theorem-zero schema rows are present"},
        {"check_id": "V1004_3_candidate_rows_nonclaim", "result": "pass" if candidates_ok else "fail", "detail": "candidate rows remain valid_for_claim=false"},
        {"check_id": "V1004_4_runner_refuses_placeholders", "result": "pass" if runner_ok else "fail", "detail": "runner refuses every current lambda placeholder row"},
        {"check_id": "V1004_5_range_zero_guard", "result": "pass" if zero_switch_ok else "fail", "detail": "theorem_zero=true is refused without PARENT_SIGNED_RANGE_INDEPENDENCE_TRUE"},
        {"check_id": "V1004_6_range_cokernel_fallback_guard", "result": "pass" if fallback_ok else "fail", "detail": "range/cokernel fallback is demanded when the parent theorem is absent"},
        {"check_id": "V1004_7_component_guard", "result": "pass" if components_ok else "fail", "detail": "retained range components such as G_norm are demanded explicitly"},
        {"check_id": "V1004_8_refusal_ledger_nonclaim", "result": "pass" if refusals_ok else "fail", "detail": "refusal ledger mirrors runner and keeps claims false"},
        {"check_id": "V1004_9_claim_gates_blocked", "result": "pass" if claims_ok else "fail", "detail": "lambda, range-cokernel, RC994_0, and local-GR claims stay blocked"},
        {"check_id": "V1004_10_vector_gate_written", "result": "pass" if vector_gate_ok else "fail", "detail": "derivative-vector aggregate gate is present and blocked"},
        {"check_id": "V1004_11_decision_written", "result": "pass" if decisions_ok else "fail", "detail": "derivative-vector aggregate target decision is written"},
        {"check_id": "V1004_12_next_target_written", "result": "pass" if next_ok else "fail", "detail": "1005 target row is present and nonclaim"},
        {"check_id": "V1004_13_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    checks.append(
        {
            "check_id": "V1004_SUMMARY",
            "result": "pass" if ready else "fail",
            "detail": "1004 range-independence theorem and lambda-profile-row validation summary",
            "generated_utc": stamp(),
        }
    )
    for row in checks:
        row.setdefault("generated_utc", stamp())
    return checks


def write_doc(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    schema: list[dict[str, str]],
    candidates: list[dict[str, str]],
    runner: list[dict[str, str]],
    refusals: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 1004 Y5 R10 B-ref Range Independence Theorem Or Delta-ref Lambda Profile Row",
        "",
        "**Status:** range/lambda zero theorem attempted, not closed; fallback lambda-profile row staged as nonclaim.",
        "",
        "**Claim ceiling:** this checkpoint does not claim partial_lambda Delta_ref=0, range/cokernel bound, derivative-vector pass, RC994_0, FB554_0, R10, PPN, WEP, clock, orbital, or local-GR pass.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "path", "role", "needle", "exists", "needle_found", "valid_for_claim"]),
        "",
        "## Range Independence Theorem Audit",
        "",
        md_table(theorem, ["audit_id", "object", "needed_for_zero", "current_evidence", "status", "valid_for_claim"]),
        "",
        "## Lambda Profile Schema",
        "",
        md_table(schema, ["schema_id", "target", "formula", "required_columns", "acceptance_rule", "valid_for_claim"]),
        "",
        "## Candidate Lambda Profile Template",
        "",
        md_table(candidates, ["candidate_id", "purpose", "target", "partial_lambda_Delta_ref", "Delta_lambda_profile", "M_H_ref", "B_ref_range_independence_certificate", "theorem_zero", "lambda_zero_authority", "G_norm", "no_cancellation_guard", "valid_for_claim"]),
        "",
        "## Lambda Profile Runner",
        "",
        md_table(runner, ["runner_id", "candidate_id", "verdict", "score_ready", "claim_allowed", "computed_abs_ratio", "failure_reasons", "generated_utc"]),
        "",
        "## Refusal Ledger",
        "",
        md_table(refusals, ["refusal_id", "candidate_id", "refusal", "why", "required_exit", "claim_allowed", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(claims, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
        "",
        "## Next Target",
        "",
        md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    theorem = range_independence_theorem_audit_rows()
    schema = lambda_profile_schema_rows()
    candidates = candidate_lambda_profile_rows()
    runner = lambda_profile_runner_rows(candidates)
    refusals = refusal_ledger_rows(runner)
    claims = claim_gate_rows(runner, theorem)
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, theorem, schema, candidates, runner, refusals, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1004_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1004_RANGE_INDEPENDENCE_THEOREM_AUDIT.csv", theorem)
    write_csv(OUT / "P8_Y5_R10_1004_LAMBDA_PROFILE_SCHEMA.csv", schema)
    write_csv(OUT / "P8_Y5_R10_1004_CANDIDATE_LAMBDA_PROFILE_TEMPLATE.csv", candidates)
    write_csv(OUT / "P8_Y5_R10_1004_LAMBDA_PROFILE_RUNNER.csv", runner)
    write_csv(OUT / "P8_Y5_R10_1004_REFUSAL_LEDGER.csv", refusals)
    write_csv(OUT / "P8_Y5_R10_1004_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_1004_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1004_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1004_VALIDATION.csv", validation)
    write_doc(sources, theorem, schema, candidates, runner, refusals, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()

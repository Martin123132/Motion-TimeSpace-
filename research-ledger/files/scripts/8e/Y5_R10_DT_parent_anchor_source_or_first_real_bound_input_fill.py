from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC = ROOT / "1198-Y5-R10-DT-parent-anchor-source-or-first-real-bound-input-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
R10_CANDIDATE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"
R10_LIVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
STAMP = datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row | {"generated_utc": STAMP} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty csv refused: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No rows._"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key != "generated_utc" and key not in headers:
                headers.append(key)
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1198_0_1197_next",
            "relative_path": "1197-Y5-R10-DT-boundary-condition-source-or-cokernel-bound-runner.md",
            "needle": "NEXT1197_0_1198",
            "role": "direct 1198 handoff.",
        },
        {
            "source_id": "SRC1198_1_1197_boundary_verdict",
            "relative_path": "1197-Y5-R10-DT-boundary-condition-source-or-cokernel-bound-runner.md",
            "needle": "BCH1197_6_verdict",
            "role": "parent D_T boundary source not found.",
        },
        {
            "source_id": "SRC1198_2_1197_R10_row",
            "relative_path": "1197-Y5-R10-DT-boundary-condition-source-or-cokernel-bound-runner.md",
            "needle": "CBI1197_1_R10",
            "role": "R10 q_DT runner row with missing external bound slot.",
        },
        {
            "source_id": "SRC1198_3_1197_runner",
            "relative_path": "1197-Y5-R10-DT-boundary-condition-source-or-cokernel-bound-runner.md",
            "needle": "D1197_2_runner",
            "role": "first q_DT residual-bound runner installed.",
        },
        {
            "source_id": "SRC1198_4_1196_boundary",
            "relative_path": "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md",
            "needle": "BP1196_0_tracefree_adjoint_boundary",
            "role": "D_T adjoint boundary pairing to be silenced or bounded.",
        },
        {
            "source_id": "SRC1198_5_1196_candidate_action",
            "relative_path": "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md",
            "needle": "PAB1196_1_variation_equation",
            "role": "candidate D_T parent-action variation equation.",
        },
        {
            "source_id": "SRC1198_6_1171_natural_no_go",
            "relative_path": "1171-Y5-R10-natural-boundary-condition-for-BC-or-first-finite-bound-row.md",
            "needle": "NBC1171_5_verdict",
            "role": "generic natural boundary shortcut rejected precedent.",
        },
        {
            "source_id": "SRC1198_7_1170_finite_bound",
            "relative_path": "1170-Y5-R10-topological-selector-boundary-flux-certificate-or-BC-primitive-owner.md",
            "needle": "PBC1170_2_finite_bound",
            "role": "finite boundary-bound fallback precedent.",
        },
        {
            "source_id": "SRC1198_8_1034_status",
            "relative_path": "1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md",
            "needle": "R10P1034_0_alpha_bound_curve",
            "role": "R10 2020 review candidate curve status.",
        },
        {
            "source_id": "SRC1198_9_1034_candidate_file",
            "relative_path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "needle": "R10_VECTOR_2020_REVIEW_0000",
            "role": "numeric nonclaim R10 external-bound review candidate.",
        },
        {
            "source_id": "SRC1198_10_1034_live_placeholder",
            "relative_path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "needle": "MISSING_DIGITIZED_ALPHA_BOUND",
            "role": "live claim curve remains placeholder-only.",
        },
        {
            "source_id": "SRC1198_11_1034_validation",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1034_VALIDATION.csv",
            "needle": "V1034_3_vector_candidate_numeric",
            "role": "1034 validation says vector candidate rows are numeric.",
        },
        {
            "source_id": "SRC1198_12_1035_projection_missing",
            "relative_path": "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
            "needle": "KXF1035_3_harmonic",
            "role": "R10 harmonic/profile projection still missing on MTS side.",
        },
    ]
    rows: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        exists = path.exists()
        needle_found = exists and str(entry["needle"]) in read_text(path)
        rows.append(entry | {"exists": exists, "needle_found": needle_found})
    return rows


def parent_anchor_attempt_rows() -> list[dict[str, object]]:
    return [
        {
            "attempt_id": "DTA1198_0_balance_action_boundary_variation",
            "route": "candidate quadratic D_T balance action",
            "derivation": "For S_T=(2 kappa_T)^-1||D_TK_T-G_res||^2, delta S_T gives a bulk term D_T^dagger(D_TK_T-G_res) plus boundary int_partialD n_mu (P_loc r)_nu delta K_T^(mu nu).",
            "result": "natural variation controls the residual boundary momentum, not directly n_mu K_T^(mu nu)",
            "claim_status": "NATURAL_BC_NOT_THE_NEEDED_B_T_ZERO",
            "missing_for_claim": "special parent boundary term or constraint that sets the adjoint pairing B_T[V,K_T]=0",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "DTA1198_1_residual_flux_natural_condition",
            "route": "free-boundary natural condition",
            "derivation": "Free delta K_T would imply a tracefree projection of n_mu(P_loc r)_nu=0 at partialD.",
            "result": "this can be compatible with a minimizer but does not prove K_T has no boundary contraction against every cokernel test vector V",
            "claim_status": "INSUFFICIENT_FOR_COKERNEL_BOUNDARY_PAIRING",
            "missing_for_claim": "prove residual-flux natural condition implies B_T=0 in the same domain/gauge, or carry B_T as a bound",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "DTA1198_2_K_normal_no_flux_condition",
            "route": "impose n_mu K_T^(mu nu)=0",
            "derivation": "If n_mu K_T^(mu nu)=0, then B_T[V,K_T]=0 for all admissible projected V.",
            "result": "mathematically sufficient but not derived by the candidate balance action; as-is it is closure-only",
            "claim_status": "SUFFICIENT_CLOSURE_NOT_PARENT_DERIVED",
            "missing_for_claim": "parent action/boundary law that selects K-normal no-flux without hand insertion",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "DTA1198_3_residual_Dirichlet_anchor",
            "route": "impose V|partialD=0 or pullback(P_loc V)=0",
            "derivation": "This kills both B_T and the rigid projected CK modes through the anchored CK/Korn inequality.",
            "result": "mathematically clean but acts on adjoint test fields; current corpus does not source it as a physical parent boundary rule",
            "claim_status": "ADJOINT_ANCHOR_NOT_PARENT_SOURCED",
            "missing_for_claim": "parent quotient/readout theorem proving those modes are unphysical residual representatives",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "DTA1198_4_rigid_mode_quotient",
            "route": "quotient translations/rotations/dilations/special conformal CK-like modes",
            "derivation": "If the parent quotient map identifies CK-like cokernel directions as representative/gauge modes, Ker(D_T^dagger) is reduced before scoring.",
            "result": "no D_T-specific parent quotient map is currently found",
            "claim_status": "QUOTIENT_MAP_MISSING",
            "missing_for_claim": "q map, vertical generator, and matter-action descent proving quotient removes only gauge/representative modes",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "DTA1198_5_verdict",
            "route": "D_T parent-anchor proof",
            "derivation": "1198 derives a useful no-go: the obvious natural boundary condition of the quadratic balance action is not the boundary pairing zero required by the cokernel theorem.",
            "result": "parent anchor remains unsigned; finite bound input fill is the honest next move",
            "claim_status": "ANCHOR_SOURCE_NOT_FOUND_MOVE_TO_R10_INPUT_FILL",
            "missing_for_claim": "D_T-specific parent boundary action or real finite-bound inputs",
            "valid_for_claim": False,
        },
    ]


def numeric(value: Any) -> float | None:
    try:
        value_float = float(str(value))
    except (TypeError, ValueError):
        return None
    return value_float if value_float > 0 else None


def r10_candidate_summary_rows() -> list[dict[str, object]]:
    if not R10_CANDIDATE.exists():
        return [
            {
                "summary_id": "R10S1198_0_candidate_missing",
                "curve_path": str(R10_CANDIDATE.relative_to(ROOT)),
                "rows": 0,
                "status": "MISSING_R10_CANDIDATE",
                "valid_for_claim": False,
            }
        ]
    rows = read_csv(R10_CANDIDATE)
    numeric_rows = []
    for row in rows:
        lambda_value = numeric(row.get("lambda_value"))
        alpha_bound = numeric(row.get("alpha_bound"))
        if lambda_value is not None and alpha_bound is not None:
            numeric_rows.append((lambda_value, alpha_bound, row))
    all_nonclaim = all(str(row.get("valid_for_claim", "")).lower() == "false" for row in rows)
    if numeric_rows:
        lambda_values = [item[0] for item in numeric_rows]
        alpha_values = [item[1] for item in numeric_rows]
        tightest = min(numeric_rows, key=lambda item: item[1])
        widest = max(numeric_rows, key=lambda item: item[1])
        return [
            {
                "summary_id": "R10S1198_0_review_candidate_curve",
                "curve_path": str(R10_CANDIDATE.relative_to(ROOT)),
                "rows": len(rows),
                "numeric_rows": len(numeric_rows),
                "lambda_min_m": min(lambda_values),
                "lambda_max_m": max(lambda_values),
                "alpha_min": min(alpha_values),
                "alpha_max": max(alpha_values),
                "tightest_lambda_m": tightest[0],
                "tightest_alpha_bound": tightest[1],
                "all_rows_valid_for_claim_false": all_nonclaim,
                "status": "REVIEW_CANDIDATE_EXTERNAL_BOUND_READY_FOR_NONCLAIM_IMPORT",
                "promotion_block": "official supplement table or human visual QA still required",
                "valid_for_claim": False,
            },
            {
                "summary_id": "R10S1198_1_live_claim_curve_status",
                "curve_path": str(R10_LIVE.relative_to(ROOT)),
                "rows": len(read_csv(R10_LIVE)) if R10_LIVE.exists() else 0,
                "numeric_rows": "not_used_live_placeholder",
                "lambda_min_m": "MISSING_DIGITIZED_ALPHA_BOUND",
                "lambda_max_m": "MISSING_DIGITIZED_ALPHA_BOUND",
                "alpha_min": "MISSING_DIGITIZED_ALPHA_BOUND",
                "alpha_max": "MISSING_DIGITIZED_ALPHA_BOUND",
                "tightest_lambda_m": "MISSING_DIGITIZED_ALPHA_BOUND",
                "tightest_alpha_bound": "MISSING_DIGITIZED_ALPHA_BOUND",
                "all_rows_valid_for_claim_false": True,
                "status": "LIVE_CLAIM_CURVE_LEFT_PLACEHOLDER",
                "promotion_block": "do not promote review candidate automatically",
                "valid_for_claim": False,
            },
            {
                "summary_id": "R10S1198_2_curve_sample_guard",
                "curve_path": str(R10_CANDIDATE.relative_to(ROOT)),
                "rows": 5,
                "numeric_rows": 5,
                "lambda_min_m": min(lambda_values[:5]),
                "lambda_max_m": max(lambda_values[:5]),
                "alpha_min": min(alpha_values[:5]),
                "alpha_max": max(alpha_values[:5]),
                "tightest_lambda_m": tightest[0],
                "tightest_alpha_bound": tightest[1],
                "all_rows_valid_for_claim_false": all_nonclaim,
                "status": "SAMPLE_ONLY_NOT_SCORE_CURVE",
                "promotion_block": "sample rows cannot substitute for full curve review",
                "valid_for_claim": False,
            },
        ]
    return [
        {
            "summary_id": "R10S1198_0_candidate_non_numeric",
            "curve_path": str(R10_CANDIDATE.relative_to(ROOT)),
            "rows": len(rows),
            "numeric_rows": 0,
            "status": "NO_POSITIVE_NUMERIC_ROWS",
            "valid_for_claim": False,
        }
    ]


def qdt_r10_input_rows(summary_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    summary = next((row for row in summary_rows if row["summary_id"] == "R10S1198_0_review_candidate_curve"), {})
    return [
        {
            "input_id": "QDT1198_0_R10_external_bound_import",
            "arena": "R10_alpha_lambda",
            "filled_field": "alpha_bound_curve_path;observable_bound_source_path",
            "filled_value": str(R10_CANDIDATE.relative_to(ROOT)),
            "filled_status": summary.get("status", "MISSING_R10_CANDIDATE"),
            "numeric_summary": f"rows={summary.get('rows','MISSING')};lambda_m=[{summary.get('lambda_min_m','MISSING')},{summary.get('lambda_max_m','MISSING')}];alpha=[{summary.get('alpha_min','MISSING')},{summary.get('alpha_max','MISSING')}]",
            "remaining_missing": "G_res_norm;coker_fraction;boundary_norm;regularizer_norm;coercivity_inverse;kappa_T;projector_leakage_norm;W_R10;P_coker_basis_path;G_res_profile_path;boundary_condition_source_path;parent_action_source_path;projector_leakage_source_path;response_source_path",
            "runner_effect": "R10 external-bound slot is now source-backed for nonclaim smoke joins, but q_DT scoring still blocked",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "QDT1198_1_R10_live_claim_curve_guard",
            "arena": "R10_alpha_lambda",
            "filled_field": "live_claim_curve",
            "filled_value": str(R10_LIVE.relative_to(ROOT)),
            "filled_status": "NOT_FILLED_PLACEHOLDER_RETAINED",
            "numeric_summary": "live curve intentionally remains MISSING_DIGITIZED_ALPHA_BOUND",
            "remaining_missing": "official supplement or human QA promotion gate",
            "runner_effect": "prevents accidental public/claim scoring from review candidate",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "QDT1198_2_MTS_side_still_empty",
            "arena": "R10_alpha_lambda",
            "filled_field": "theory_prediction_side",
            "filled_value": "none",
            "filled_status": "MISSING_QDT_THEORY_INPUTS",
            "numeric_summary": "no alpha_DT(lambda) prediction produced",
            "remaining_missing": "D_T parent anchor or q_DT residual profiles plus R10 response projection",
            "runner_effect": "the row is evidence plumbing only, not a pass/fail physics score",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def dryrun_rows() -> list[dict[str, object]]:
    path_ok = R10_CANDIDATE.exists()
    source_reason = "review_candidate_curve_path_exists" if path_ok else "missing_review_candidate_curve_path"
    return [
        {
            "run_id": "DR1198_0_R10_qDT_bound_import_dryrun",
            "arena": "R10_alpha_lambda",
            "external_bound_path_ok": path_ok,
            "theory_side_ready": False,
            "runner_status": "blocked_missing_theory_inputs",
            "filled_inputs": source_reason,
            "missing_inputs": "G_res_norm;coker_fraction;boundary_norm;regularizer_norm;coercivity_inverse;kappa_T;projector_leakage_norm;W_R10;P_coker_basis_path;G_res_profile_path;boundary_condition_source_path;parent_action_source_path;projector_leakage_source_path;response_source_path",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G1198_0_parent_anchor",
            "claim": "D_T parent boundary anchor is derived",
            "status": "BLOCKED_NATURAL_BC_NO_GO",
            "why": "candidate balance-action natural BC controls residual boundary momentum, not the K_T boundary pairing needed for the cokernel theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1198_1_R10_external_bound",
            "claim": "R10 external alpha_bound(lambda) is live claim-ready",
            "status": "BLOCKED_REVIEW_CANDIDATE_ONLY",
            "why": "numeric 2020 curve is review-candidate nonclaim; official supplement/human QA promotion not signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1198_2_qDT_R10_score",
            "claim": "q_DT R10 row can be scored",
            "status": "BLOCKED_MTS_THEORY_SIDE_MISSING",
            "why": "external bound slot is improved, but alpha_DT(lambda), W_R10, P_coker, B_T, E_reg, eps_P, and parent action source remain missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1198_3_local_GR",
            "claim": "MTS reduces to local GR/Newton through D_T",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "why": "parent anchor and finite q_DT local-test rows remain incomplete",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1198_0_parent_anchor",
            "decision": "natural_boundary_anchor_rejected_for_DT",
            "reason": "the candidate quadratic balance action supplies residual-boundary natural data, not the needed n.K or adjoint-test anchor",
            "next_action": "do not use generic natural BC as local-GR proof; either construct special parent boundary action or retain B_T bound",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1198_1_R10_external_fill",
            "decision": "first_real_R10_external_bound_slot_filled_nonclaim",
            "reason": "1034 review-candidate curve gives real numeric external bound evidence while keeping promotion blocked",
            "next_action": "join this curve only to nonclaim smoke rows until official/human promotion and MTS-side prediction inputs exist",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1198_2_best_next",
            "decision": "attack_MTS_side_R10_projection",
            "reason": "after the external-bound slot is filled, the weakest R10 runner inputs are W_R10(alpha projection), G_res profile, P_coker fraction, and B_T norm",
            "next_action": "1199 should derive or source W_R10 and a q_DT profile/projection template rather than chasing the external curve again",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1198_0_1199",
            "next_target": "1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md",
            "objective": "derive or source the MTS-side R10 projection for q_DT: W_R10(lambda), G_res profile, P_coker fraction, B_T norm, and projector leakage eps_P, using the 1198 nonclaim external curve only as evidence plumbing",
            "include": "W_R10 projection contract; q_DT residual profile schema; P_coker fraction/source; B_T source/bound; eps_P leakage; nonclaim curve join dry-run",
            "exclude": "promoting review curve; generic natural-boundary shortcut; local-GR/R10 pass; fake numeric theory inputs; GitHub; formalization edits",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, object]],
    anchor_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    input_rows: list[dict[str, object]],
    dryruns: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["needle_found"] for row in sources)
    anchor_statuses = {row["claim_status"] for row in anchor_rows}
    summary_by_id = {row["summary_id"]: row for row in summary_rows}
    candidate_summary = summary_by_id.get("R10S1198_0_review_candidate_curve", {})
    live_summary = summary_by_id.get("R10S1198_1_live_claim_curve_status", {})
    candidate_ok = (
        candidate_summary.get("rows", 0) == candidate_summary.get("numeric_rows", -1)
        and candidate_summary.get("all_rows_valid_for_claim_false") is True
        and candidate_summary.get("status") == "REVIEW_CANDIDATE_EXTERNAL_BOUND_READY_FOR_NONCLAIM_IMPORT"
    )
    live_guard_ok = live_summary.get("status") == "LIVE_CLAIM_CURVE_LEFT_PLACEHOLDER"
    input_nonclaim = all(row.get("claim_allowed") is False and row.get("valid_for_claim") is False for row in input_rows)
    dryrun_blocked = all(row.get("runner_status") == "blocked_missing_theory_inputs" and row.get("valid_for_claim") is False for row in dryruns)
    gates_blocked = all(row.get("claim_allowed") is False and row.get("valid_for_claim") is False for row in gates + nexts)
    decisions_nonclaim = all(row.get("valid_for_claim") is False for row in decisions)
    return [
        {
            "check_id": "V1198_0_sources_exist",
            "result": "pass" if all_sources_ok else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1198_1_DT_anchor_attempt_done",
            "result": "pass" if "ANCHOR_SOURCE_NOT_FOUND_MOVE_TO_R10_INPUT_FILL" in anchor_statuses and "NATURAL_BC_NOT_THE_NEEDED_B_T_ZERO" in anchor_statuses else "fail",
            "detail": "D_T parent-anchor attempt derives the natural-boundary mismatch and refuses promotion",
            "claim_allowed": False,
        },
        {
            "check_id": "V1198_2_R10_candidate_numeric_nonclaim",
            "result": "pass" if candidate_ok else "fail",
            "detail": "R10 review candidate has positive numeric rows and all remain valid_for_claim=false",
            "claim_allowed": False,
        },
        {
            "check_id": "V1198_3_live_curve_not_promoted",
            "result": "pass" if live_guard_ok else "fail",
            "detail": "live R10 DIGITIZED claim curve remains placeholder/nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1198_4_qDT_R10_input_nonclaim",
            "result": "pass" if input_nonclaim and any(row["input_id"] == "QDT1198_0_R10_external_bound_import" for row in input_rows) else "fail",
            "detail": "first q_DT/R10 external-bound slot is filled only as nonclaim evidence plumbing",
            "claim_allowed": False,
        },
        {
            "check_id": "V1198_5_runner_dryrun_blocks",
            "result": "pass" if dryrun_blocked else "fail",
            "detail": "R10 dry-run stays blocked because MTS-side theory inputs are missing",
            "claim_allowed": False,
        },
        {
            "check_id": "V1198_6_claim_gates_blocked",
            "result": "pass" if gates_blocked else "fail",
            "detail": "all 1198 claim gates and next target remain blocked/nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1198_7_decisions_nonclaim",
            "result": "pass" if decisions_nonclaim else "fail",
            "detail": "decision ledger remains private/nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1198_8_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1198_9_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1198_SUMMARY",
            "result": "pass",
            "detail": "1198 rejects the generic D_T natural-boundary anchor, imports the real 2020 R10 review-candidate alpha_bound curve as nonclaim evidence plumbing, leaves the live claim curve untouched, and hands off to MTS-side q_DT-to-R10 projection work",
            "claim_allowed": False,
        },
    ]


def write_doc(
    sources: list[dict[str, object]],
    anchor_rows: list[dict[str, object]],
    summary_rows: list[dict[str, object]],
    input_rows: list[dict[str, object]],
    dryruns: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 1198 - Y5/R10 D_T parent anchor source or first real bound input fill",
            "**Current verdict:** the obvious D_T natural-boundary route does not derive the needed boundary pairing zero. The external R10 bound slot is improved with a real 2020 Eot-Wash review-candidate curve, but it remains nonclaim and the MTS-side q_DT inputs are still missing.",
            "**Main progress:** 1198 prevents a fake local-GR proof by deriving the natural-boundary mismatch, then makes empirical progress by wiring real R10 external-bound evidence into the q_DT runner as private review-candidate plumbing.",
            "**No claim:** no q_loc=0, local-GR, Newton, R10, PPN, WEP, clock, orbital, or public-facing claim follows from this checkpoint.",
            "## Source register\n\n" + table(sources),
            "## D_T parent anchor attempt\n\n" + table(anchor_rows),
            "## R10 candidate summary\n\n" + table(summary_rows),
            "## q_DT/R10 input fill\n\n" + table(input_rows),
            "## Runner dry-run\n\n" + table(dryruns),
            "## Claim gates\n\n" + table(gates),
            "## Decision ledger\n\n" + table(decisions),
            "## Validation\n\n" + table(validations),
            "## Next target\n\n" + table(nexts),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    anchor_rows = parent_anchor_attempt_rows()
    summary_rows = r10_candidate_summary_rows()
    input_rows = qdt_r10_input_rows(summary_rows)
    dryruns = dryrun_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(
        sources,
        anchor_rows,
        summary_rows,
        input_rows,
        dryruns,
        gates,
        decisions,
        nexts,
    )

    outputs = {
        "P8_Y5_R10_1198_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1198_DT_PARENT_ANCHOR_ATTEMPT.csv": anchor_rows,
        "P8_Y5_R10_1198_R10_CANDIDATE_SUMMARY.csv": summary_rows,
        "P8_Y5_R10_1198_QDT_R10_INPUT_FILL_NONCLAIM.csv": input_rows,
        "P8_Y5_R10_1198_RUNNER_DRYRUN.csv": dryruns,
        "P8_Y5_R10_1198_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1198_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1198_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1198_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, stamp(rows))

    write_doc(sources, anchor_rows, summary_rows, input_rows, dryruns, gates, decisions, validations, nexts)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row["check_id"] for row in validations if row["result"] != "pass"]
    if FORMALIZATION.exists() and not FORMALIZATION.is_dir():
        failed.append("formalization_path_not_directory")

    print(f"wrote {DOC}")
    print("validation: " + ("PASS" if not failed else "FAIL " + ";".join(failed)))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

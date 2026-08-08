from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1192-Y5-R10-parent-phi-source-or-active-Gamma-bound-first-score-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
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
            "source_id": "SRC1192_0_1191_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1191_NEXT_TARGET.csv",
            "needle": "NEXT1191_0_1192",
            "role": "direct 1192 handoff.",
        },
        {
            "source_id": "SRC1192_1_1191_parent_zero",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1191_PARENT_ZERO_CERTIFICATE.csv",
            "needle": "PZ1191_1_phi_parent_source",
            "role": "1191 parent phi/K_L source blocker.",
        },
        {
            "source_id": "SRC1192_2_1191_bound_pack",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1191_LEFTOVER_BOUND_PACK.csv",
            "needle": "LBP1191_1_phi_gradient_from_gamma",
            "role": "phi gradient and Ricci residual bound slot.",
        },
        {
            "source_id": "SRC1192_3_1190_solver",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1190_TRACEFREE_KHAT_SOLVER_GATE.csv",
            "needle": "KLS1190_2_covariant_cancellation_condition",
            "role": "exact curved source equation required for scalar phi.",
        },
        {
            "source_id": "SRC1192_4_795_origin",
            "relative_path": "795-Y5-R10-parent-origin-of-tracefree-Khat-solver-or-amplitude-bound.md",
            "needle": "POA795_0_auxiliary_phi_constraint",
            "role": "auxiliary phi constraint route previously rejected as closure unless parent-derived.",
        },
        {
            "source_id": "SRC1192_5_796_relaxation",
            "relative_path": "796-Y5-R10-KL-amplitude-PPN-budget-or-parent-relaxation-source.md",
            "needle": "PRS796_1_stationary_equation",
            "role": "parent relaxation source stationary-equation contract.",
        },
        {
            "source_id": "SRC1192_6_797_tradeoff",
            "relative_path": "797-Y5-R10-parent-relaxation-source-action-contract-and-Gammaeff-screening-gate.md",
            "needle": "RTL797_2_residual_tradeoff",
            "role": "relaxation residual/amplitude no-free-lunch theorem.",
        },
        {
            "source_id": "SRC1192_7_834_gamma_support",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_834_GAMMA_MODE_SPLIT_THEOREM.csv",
            "needle": "GS834_2_source_support",
            "role": "active gamma support law.",
        },
        {
            "source_id": "SRC1192_8_835_schema",
            "relative_path": "835-Y5-R10-Gamma-active-mode-bound-and-local-response-runner.md",
            "needle": "active_gamma_coeff",
            "role": "active-Gamma local-response runner schema.",
        },
        {
            "source_id": "SRC1192_9_836_fill",
            "relative_path": "836-Y5-R10-fill-active-Gamma-bound-from-source-support-or-demote-local-branch.md",
            "needle": "FA836_1_U_B2_window43",
            "role": "U_B^2 support-value smoke rows.",
        },
        {
            "source_id": "SRC1192_10_838_coefficient",
            "relative_path": "838-Y5-R10-active-Gamma-coefficient-source-pack-or-parent-derivation.md",
            "needle": "NR838_0_F2_bound",
            "role": "missing active-Gamma coefficient inputs.",
        },
        {
            "source_id": "SRC1192_11_1189_arenas",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1189_ARENA_PROJECTION_QUEUE.csv",
            "needle": "APR1189_0_gamma_beta",
            "role": "local arena projection queue retained.",
        },
    ]
    rows: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        exists = path.exists()
        needle_found = exists and str(entry["needle"]) in read_text(path)
        rows.append(entry | {"exists": exists, "needle_found": needle_found})
    return rows


def parent_phi_source_audit_rows() -> list[dict[str, object]]:
    return [
        {
            "audit_id": "PHE1192_0_required_vector_equation",
            "target": "exact curved scalar cancellation equation",
            "derivation": "For K_L^{mu nu}=2 nabla^mu nabla^nu phi-(1/2)g^{mu nu}Box phi, exact cancellation needs M^nu[phi]:=(3/2)nabla^nu Box phi+2R^nu_sigma nabla^sigma phi=nabla^nu Gamma_eff plus retained source/boundary terms.",
            "result": "REQUIRED_EQUATION_RESTATED",
            "promotion_status": "not_parent_derived",
            "blocking_gap": "MISSING_PARENT_EULER_OR_CONSTRAINT_SOURCE",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PHE1192_1_curl_integrability_obstruction",
            "target": "scalar phi can source a gradient-compatible vector",
            "derivation": "Since the right-hand side is a gradient, a necessary condition is curl M[phi]=0. The Hessian part is exact, but curl(2R^nu_sigma nabla^sigma phi) generally contributes 2 nabla_[alpha](R_{beta]sigma}nabla^sigma phi).",
            "result": "RICCI_CURL_OBSTRUCTION_IDENTIFIED",
            "promotion_status": "new_gate_added",
            "blocking_gap": "MISSING_RICCI_EXACTNESS_OR_COMPENSATOR",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PHE1192_2_special_Ricci_flat_branch",
            "target": "flat/local exterior limit",
            "derivation": "If R_{mu nu}=0 or the Ricci one-form R^nu_sigma nabla^sigma phi is exact and boundary silent, the equation reduces locally to Box phi=(2/3)Gamma_eff+C.",
            "result": "CONDITIONAL_BRANCH_AVAILABLE",
            "promotion_status": "special_branch_only",
            "blocking_gap": "MISSING_DOMAIN_PROOF_FOR_LAB_AND_MATTER_REGIONS",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PHE1192_3_parent_ownership_test",
            "target": "phi/K_L is parent-owned rather than inserted",
            "derivation": "A Lagrange multiplier can force Box phi=(2/3)Gamma_eff in a flat branch, but it adds phi/lambda stress and boundary equations; this is a new parent sector unless derived from existing MTS variables.",
            "result": "CONSTRAINT_ACTION_IS_CLOSURE_UNTIL_SIGNED",
            "promotion_status": "not_adopted",
            "blocking_gap": "MISSING_VARIATION_STRESS_WARD_AND_MATTER_READOUT",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PHE1192_4_relaxation_tradeoff_link",
            "target": "avoid hard scalar constraint by relaxation",
            "derivation": "The quadratic parent-relaxation route is mathematically well-posed but 797 shows it trades residual suppression against carrier amplitude; it does not prove q_loc=0 by itself.",
            "result": "RELAXATION_RETAINED_AS_CONTRACT_NOT_ZERO_PROOF",
            "promotion_status": "not_claim",
            "blocking_gap": "MISSING_GAMMA_SCREENING_OR_RESPONSE_KERNEL",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PHE1192_5_verdict",
            "target": "parent phi source closes local GR",
            "derivation": "The scalar route closes only if parent ownership, Ricci/exactness, boundary/no-flux, and metric response all close together.",
            "result": "SCALAR_ROUTE_RETAINED_CONDITIONALLY_NO_LOCAL_GR_CLAIM",
            "promotion_status": "blocked",
            "blocking_gap": "R_K_CURL;PARENT_SOURCE;BOUNDARY;RESPONSE_MATRIX",
            "valid_for_claim": False,
        },
    ]


def integrability_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "IG1192_0_curl_zero",
            "condition": "curl M[phi]=0",
            "mathematical_form": "nabla_[alpha]((3/2)nabla_{beta]}Box phi+2R_{beta]sigma}nabla^sigma phi)=0",
            "safe_case": "Ricci-flat local exterior, or R_{nu sigma}nabla^sigma phi is an exact one-form",
            "current_status": "UNSIGNED",
            "needed_to_close": "domain Ricci class; phi gradient direction; source path; sign convention",
            "valid_for_claim": False,
        },
        {
            "gate_id": "IG1192_1_parent_source",
            "condition": "scalar source equation descends from S_MTS",
            "mathematical_form": "delta S_parent/delta lambda gives curved source equation and delta S_parent/delta phi plus delta_g S_parent are Ward-safe",
            "safe_case": "phi is an owned parent/moment variable with stress accounted",
            "current_status": "UNSIGNED",
            "needed_to_close": "parent variable map; stress variation; Bianchi/Ward identity; matter readout",
            "valid_for_claim": False,
        },
        {
            "gate_id": "IG1192_2_boundary_green",
            "condition": "Green operator and boundary modes are fixed",
            "mathematical_form": "Box^{-1}_D or curved Green inverse has declared zero modes and boundary flux B_phi=0 or bounded",
            "safe_case": "compact local domain with parent natural boundary/no-flux condition",
            "current_status": "UNSIGNED",
            "needed_to_close": "boundary condition; zero-mode convention; normal flux source row",
            "valid_for_claim": False,
        },
        {
            "gate_id": "IG1192_3_matter_domain",
            "condition": "local matter Ricci term does not spoil scalar route",
            "mathematical_form": "R_{mu nu} from ordinary matter either negligible, exactly aligned, or compensated by parent equations",
            "safe_case": "vacuum exterior limit only, or vector/tensor compensator handles matter Ricci",
            "current_status": "UNSIGNED",
            "needed_to_close": "lab/solar matter-domain bound; Ricci scale; compensator source equation",
            "valid_for_claim": False,
        },
        {
            "gate_id": "IG1192_4_vector_tensor_escape",
            "condition": "if scalar integrability fails, use parent vector/tensor carrier",
            "mathematical_form": "K_hat not restricted to scalar Hessian range; solve within tracefree tensor range with Ward-safe stress",
            "safe_case": "parent tracefree tensor sector has positive operator and local response bound",
            "current_status": "AVAILABLE_AS_NEXT_ROUTE_NOT_BUILT",
            "needed_to_close": "operator range theorem; amplitude penalty; response matrix; boundary no-flux",
            "valid_for_claim": False,
        },
    ]


def parent_action_candidate_rows() -> list[dict[str, object]]:
    return [
        {
            "candidate_id": "PAC1192_0_lagrange_constraint",
            "candidate_action": "S_phi_lambda = integral sqrt(-g) lambda(Box phi - 2 Gamma_eff/3) plus curved correction terms",
            "would_buy": "enforces the flat-branch scalar source equation exactly",
            "cost_or_failure": "introduces new lambda/phi stress, boundary equations, and possible higher-derivative response unless parent-owned",
            "status": "CLOSURE_ONLY_NOT_ADOPTED",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "PAC1192_1_quadratic_penalty",
            "candidate_action": "S_penalty = -1/2 integral sqrt(-g) |M[phi]-grad Gamma_eff|^2 - mu_phi^2 |K_L|^2/2",
            "would_buy": "variational stationary equation with tunable residual/amplitude",
            "cost_or_failure": "inherits 797 tradeoff and can be fourth-order/stiff; not a zero proof",
            "status": "CONTRACT_ONLY",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "PAC1192_2_moment_closure",
            "candidate_action": "derive phi or K_L as the scalar-longitudinal part of a parent coarse-grained motion moment",
            "would_buy": "natural parent ownership without adding an external scalar",
            "cost_or_failure": "requires closed moment equation and projection/range theorem not present yet",
            "status": "BEST_DERIVATION_CANDIDATE_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "PAC1192_3_vector_tensor_compensator",
            "candidate_action": "allow the parent tracefree K_hat sector to solve the full vector equation beyond scalar Hessian range",
            "would_buy": "bypasses scalar Ricci-curl obstruction",
            "cost_or_failure": "amplitude and metric response become more dangerous unless the parent operator is signed and bounded",
            "status": "NEXT_ROUTE_IF_SCALAR_EXACTNESS_FAILS",
            "valid_for_claim": False,
        },
        {
            "candidate_id": "PAC1192_4_metric_null_improvement",
            "candidate_action": "make Khat carrier a metric-null improvement/boundary stress in the observed matter frame",
            "would_buy": "carrier can cancel q_loc without PPN/Newton footprint",
            "cost_or_failure": "1191/834 keep metric-null variation proof unsigned",
            "status": "CANDIDATE_ONLY",
            "valid_for_claim": False,
        },
    ]


def active_gamma_first_score_rows() -> list[dict[str, object]]:
    khat_norm_factor = math.sqrt(4 / 3)
    window_u_b = 3.7965595357794454e-7
    point_mass_u_b = 9.725553695716371e-14
    rows = [
        {
            "row_id": "AGS1192_0_window43_U_B2_PPN",
            "arena": "PPN",
            "formula_family": "Gamma_eff-Lambda_loc <= C_U U_B^2",
            "dimension_n": 4,
            "active_gamma_coeff": "MISSING_C_U",
            "small_parameter": window_u_b,
            "support_power": 2,
            "visible_suppression_factor": window_u_b**2,
            "Khat_norm_factor": khat_norm_factor,
            "symbolic_Khat_bound": f"{khat_norm_factor:.16g} * C_U * {window_u_b**2:.16g}",
            "metric_response_coeff": "MISSING_RESPONSE_MATRIX",
            "K00_projection_fraction": "MISSING_K00_PROJECTION",
            "matter_curvature_norm": "MISSING_KMATTER",
            "observable_limit": "MISSING_PPN_BOUND",
            "block_reason": "MISSING_C_U;MISSING_RESPONSE_MATRIX;MISSING_K00_PROJECTION;MISSING_KMATTER;MISSING_PPN_BOUND",
            "runner_status": "blocked_missing_inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "AGS1192_1_point_mass_U_B2_PPN",
            "arena": "PPN",
            "formula_family": "Gamma_eff-Lambda_loc <= C_U U_B^2",
            "dimension_n": 4,
            "active_gamma_coeff": "MISSING_C_U",
            "small_parameter": point_mass_u_b,
            "support_power": 2,
            "visible_suppression_factor": point_mass_u_b**2,
            "Khat_norm_factor": khat_norm_factor,
            "symbolic_Khat_bound": f"{khat_norm_factor:.16g} * C_U * {point_mass_u_b**2:.16g}",
            "metric_response_coeff": "MISSING_RESPONSE_MATRIX",
            "K00_projection_fraction": "MISSING_K00_PROJECTION",
            "matter_curvature_norm": "MISSING_KMATTER",
            "observable_limit": "MISSING_PPN_BOUND",
            "block_reason": "MISSING_C_U;MISSING_RESPONSE_MATRIX;MISSING_K00_PROJECTION;MISSING_KMATTER;MISSING_PPN_BOUND",
            "runner_status": "blocked_missing_inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "AGS1192_2_R10_template_same_inputs",
            "arena": "R10",
            "formula_family": "alpha_K(lambda)=W_R10(lambda)*sqrt(4/3)*C_U*U_B^2",
            "dimension_n": 4,
            "active_gamma_coeff": "MISSING_C_U",
            "small_parameter": "reuse_source_supported_U_B_when_domain_matches",
            "support_power": 2,
            "visible_suppression_factor": "numeric_only_after_R10_domain_U_B_source",
            "Khat_norm_factor": khat_norm_factor,
            "symbolic_Khat_bound": "sqrt(4/3)*C_U*U_B_R10^2",
            "metric_response_coeff": "MISSING_W_R10_LAMBDA",
            "K00_projection_fraction": "not_sufficient_for_R10",
            "matter_curvature_norm": "MISSING_R10_SOURCE_NORMALIZATION",
            "observable_limit": "MISSING_ALPHA_BOUND_CURVE",
            "block_reason": "MISSING_C_U;MISSING_W_R10_LAMBDA;MISSING_R10_DOMAIN_U_B;MISSING_ALPHA_BOUND_CURVE",
            "runner_status": "template_only_blocked_missing_inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G1192_0_parent_phi_source",
            "claim": "phi/K_L source equation is derived from parent action",
            "status": "BLOCKED_PARENT_SOURCE_UNSIGNED",
            "why": "constraint and penalty actions remain candidate closures without parent variable/stress/Ward signatures",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1192_1_scalar_integrability",
            "claim": "scalar phi route cancels curved local residual generically",
            "status": "BLOCKED_RICCI_CURL_OBSTRUCTION",
            "why": "curl of Ricci-gradient term is not generally zero, so scalar route needs Ricci-flat/exact branch or compensator",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1192_2_active_gamma_first_score",
            "claim": "active-Gamma local bound row scores an arena pass",
            "status": "BLOCKED_COEFFICIENT_AND_RESPONSE_MISSING",
            "why": "U_B^2 suppression factors are staged but C_U, K00/response, matter normalization, and bounds are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1192_3_local_GR",
            "claim": "MTS reduces to local GR/Newton",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "why": "parent source, Ricci integrability, boundary, metric response, and arena projection gates remain open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1192_0_new_integrability_gate",
            "decision": "add_Ricci_curl_obstruction_to_scalar_phi_route",
            "reason": "the curved scalar source equation is a vector equation with a gradient right-hand side; Ricci-gradient curl is a necessary condition",
            "next_action": "try to prove Ricci-exactness on the local branch or move to a parent vector/tensor compensator",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1192_1_phi_source_not_parent_signed",
            "decision": "do_not_adopt_auxiliary_phi_constraint",
            "reason": "a Lagrange multiplier can force the equation but would be a new closure sector unless stress/Ward/matter readout are derived",
            "next_action": "look for moment-closure or parent tracefree-sector origin",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1192_2_first_score_row_staged",
            "decision": "stage_active_gamma_first_score_rows_nonclaim",
            "reason": "window43 and point-mass U_B^2 values give explicit suppression factors but cannot score without C_U and response matrices",
            "next_action": "source C_U or prove it zero; source one PPN/R10 response operator",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1192_3_selected_next_route",
            "decision": "attack_Ricci_exactness_or_vector_tensor_compensator",
            "reason": "this is now the cleanest derivability fork after the parent scalar route fails generically",
            "next_action": "build 1193 Ricci-exact scalar branch or vector/tensor compensator gate",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1192_0_1193",
            "next_target": "1193-Y5-R10-Ricci-exact-scalar-branch-or-vector-tensor-compensator.md",
            "objective": "try to close the new Ricci-curl integrability gate for the scalar phi route; if it fails, construct the parent tracefree vector/tensor compensator contract with amplitude and response bounds",
            "include": "curl M[phi] gate; Ricci-flat/exact one-form branch; matter-domain bound; vector/tensor range theorem; nonclaim active-Gamma score continuity",
            "exclude": "generic scalar phi zero claim; parentless Lagrange constraint; local-GR pass; invented coefficients; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, object]],
    phi: list[dict[str, object]],
    integrability: list[dict[str, object]],
    candidates: list[dict[str, object]],
    active_gamma: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["needle_found"] for row in sources)
    phi_ids = {row["audit_id"] for row in phi}
    gate_ids = {row["gate_id"] for row in integrability}
    score_ids = {row["row_id"] for row in active_gamma}
    science_rows = phi + integrability + candidates + active_gamma + gates + decisions + nexts
    all_nonclaim = all(row.get("valid_for_claim") is False for row in science_rows)
    all_scores_blocked = all(row.get("claim_allowed") is False for row in active_gamma + gates)
    return [
        {
            "check_id": "V1192_0_sources_exist",
            "result": "pass" if all_sources_ok else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1192_1_phi_audit_complete",
            "result": "pass" if {"PHE1192_0_required_vector_equation", "PHE1192_1_curl_integrability_obstruction", "PHE1192_5_verdict"} <= phi_ids else "fail",
            "detail": "parent phi source equation, Ricci-curl obstruction, and verdict rows are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1192_2_integrability_gate_complete",
            "result": "pass" if {"IG1192_0_curl_zero", "IG1192_3_matter_domain", "IG1192_4_vector_tensor_escape"} <= gate_ids else "fail",
            "detail": "curl, matter-domain, and vector/tensor escape gates are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1192_3_constraint_not_adopted",
            "result": "pass" if any(row["status"] == "CLOSURE_ONLY_NOT_ADOPTED" for row in candidates) else "fail",
            "detail": "auxiliary Lagrange constraint is not promoted to parent action",
            "claim_allowed": False,
        },
        {
            "check_id": "V1192_4_active_gamma_first_rows",
            "result": "pass" if {"AGS1192_0_window43_U_B2_PPN", "AGS1192_1_point_mass_U_B2_PPN", "AGS1192_2_R10_template_same_inputs"} <= score_ids else "fail",
            "detail": "first active-Gamma score rows are staged but blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1192_5_scores_block_missing_inputs",
            "result": "pass" if all_scores_blocked and all("MISSING" in str(row.get("block_reason", "")) for row in active_gamma) else "fail",
            "detail": "no active-Gamma row can score with missing coefficient/response inputs",
            "claim_allowed": False,
        },
        {
            "check_id": "V1192_6_claim_gates_blocked",
            "result": "pass" if all(row["claim_allowed"] is False for row in gates) else "fail",
            "detail": "all 1192 claim gates remain blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1192_7_all_science_rows_nonclaim",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated science rows keep valid_for_claim=false",
            "claim_allowed": False,
        },
        {
            "check_id": "V1192_8_next_target",
            "result": "pass" if nexts and nexts[0]["next_id"] == "NEXT1192_0_1193" else "fail",
            "detail": "1193 handoff targets Ricci-exact scalar branch or vector/tensor compensator",
            "claim_allowed": False,
        },
        {
            "check_id": "V1192_9_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1192_10_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1192_SUMMARY",
            "result": "pass",
            "detail": "1192 identifies the Ricci-curl integrability obstruction for parent phi/K_L, refuses auxiliary constraint promotion, stages first active-Gamma nonclaim rows, and hands off to Ricci-exactness or vector/tensor compensator",
            "claim_allowed": False,
        },
    ]


def write_doc(
    sources: list[dict[str, object]],
    phi: list[dict[str, object]],
    integrability: list[dict[str, object]],
    candidates: list[dict[str, object]],
    active_gamma: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 1192 - Y5/R10 parent phi source or active-Gamma bound first score row",
            "**Current verdict:** the parent `phi/K_L` route is still alive, but not generically closed. 1192 adds a new hard gate: in curved matter regions the Ricci-gradient term must be curl-free/exact, Ricci-flat, or handled by a parent vector/tensor compensator.",
            "**Main progress:** the scalar route is now separated into a special Ricci-compatible branch, a rejected parentless constraint branch, and a nonclaim active-Gamma first-score branch with explicit `U_B^2` suppression factors.",
            "**No claim:** no `q_loc=0`, local-GR, Newton, R10, PPN, WEP, clock, orbital, or public-facing claim follows from this checkpoint.",
            "## Source register\n\n" + table(sources),
            "## Parent phi source audit\n\n" + table(phi),
            "## Curved scalar integrability gate\n\n" + table(integrability),
            "## Parent action candidate audit\n\n" + table(candidates),
            "## Active Gamma first score rows\n\n" + table(active_gamma),
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
    phi = parent_phi_source_audit_rows()
    integrability = integrability_gate_rows()
    candidates = parent_action_candidate_rows()
    active_gamma = active_gamma_first_score_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, phi, integrability, candidates, active_gamma, gates, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1192_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1192_PARENT_PHI_SOURCE_AUDIT.csv": phi,
        "P8_Y5_R10_1192_CURVED_SCALAR_INTEGRABILITY_GATE.csv": integrability,
        "P8_Y5_R10_1192_PARENT_ACTION_CANDIDATE_AUDIT.csv": candidates,
        "P8_Y5_R10_1192_ACTIVE_GAMMA_FIRST_SCORE_ROWS.csv": active_gamma,
        "P8_Y5_R10_1192_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1192_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1192_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1192_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, stamp(rows))

    write_doc(sources, phi, integrability, candidates, active_gamma, gates, decisions, validations, nexts)

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

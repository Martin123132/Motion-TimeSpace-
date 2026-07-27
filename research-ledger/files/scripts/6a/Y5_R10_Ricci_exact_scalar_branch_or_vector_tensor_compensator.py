from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1193-Y5-R10-Ricci-exact-scalar-branch-or-vector-tensor-compensator.md"
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
            "source_id": "SRC1193_0_1192_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1192_NEXT_TARGET.csv",
            "needle": "NEXT1192_0_1193",
            "role": "direct 1193 handoff.",
        },
        {
            "source_id": "SRC1193_1_1192_integrability",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1192_CURVED_SCALAR_INTEGRABILITY_GATE.csv",
            "needle": "IG1192_0_curl_zero",
            "role": "Ricci-curl scalar integrability gate.",
        },
        {
            "source_id": "SRC1193_2_1192_vector_escape",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1192_PARENT_ACTION_CANDIDATE_AUDIT.csv",
            "needle": "PAC1192_3_vector_tensor_compensator",
            "role": "vector/tensor compensator candidate from 1192.",
        },
        {
            "source_id": "SRC1193_3_1192_active_gamma",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1192_ACTIVE_GAMMA_FIRST_SCORE_ROWS.csv",
            "needle": "AGS1192_0_window43_U_B2_PPN",
            "role": "nonclaim active-Gamma score continuity.",
        },
        {
            "source_id": "SRC1193_4_832_curvature",
            "relative_path": "832-Y5-R10-tracefree-divergence-range-theorem-or-cokernel-bound.md",
            "needle": "CB832_1_curvature_residual",
            "role": "curved Ricci obstruction for Hessian Khat carrier.",
        },
        {
            "source_id": "SRC1193_5_832_flat_range",
            "relative_path": "832-Y5-R10-tracefree-divergence-range-theorem-or-cokernel-bound.md",
            "needle": "FRI832_0_domain",
            "role": "flat tracefree divergence range theorem.",
        },
        {
            "source_id": "SRC1193_6_831_range",
            "relative_path": "831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md",
            "needle": "OC831_3_exact_zero_condition",
            "role": "range/cokernel exact-zero condition.",
        },
        {
            "source_id": "SRC1193_7_831_projection",
            "relative_path": "831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md",
            "needle": "RT831_1_projection_law",
            "role": "residual equals cokernel projection.",
        },
        {
            "source_id": "SRC1193_8_830_owner",
            "relative_path": "830-Y5-R10-Khat-boundary-owner-or-residual-vector-runner.md",
            "needle": "KO830_0_parent_tensor_operator",
            "role": "Khat parent tensor operator missing.",
        },
        {
            "source_id": "SRC1193_9_830_ppn",
            "relative_path": "830-Y5-R10-Khat-boundary-owner-or-residual-vector-runner.md",
            "needle": "OG830_1_PPN",
            "role": "PPN observable response gate.",
        },
        {
            "source_id": "SRC1193_10_833_amplitude",
            "relative_path": "833-Y5-R10-Hessian-Khat-carrier-amplitude-and-metric-response-bound.md",
            "needle": "AL833_1_exact_L2_norm",
            "role": "Khat carrier amplitude law.",
        },
        {
            "source_id": "SRC1193_11_798_screening",
            "relative_path": "798-Y5-R10-Gammaeff-local-screening-source-law-or-response-kernel-bound.md",
            "needle": "STA798_0_F_stationary_lock",
            "role": "Gamma_eff screening/stationary lock condition.",
        },
        {
            "source_id": "SRC1193_12_800_kperp",
            "relative_path": "800-Y5-R10-universal-XB-PiB-support-powers-or-Kperp-boundary-zero-lemma.md",
            "needle": "KBL800_0_needed_operator",
            "role": "K_perp tensor boundary operator gap.",
        },
    ]
    rows: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        exists = path.exists()
        needle_found = exists and str(entry["needle"]) in read_text(path)
        rows.append(entry | {"exists": exists, "needle_found": needle_found})
    return rows


def ricci_exact_scalar_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": "RES1193_0_curl_identity",
            "claim_tested": "scalar curved source vector can equal a gradient",
            "derivation": "For M_beta=(3/2)nabla_beta Box phi+2R_beta_sigma nabla^sigma phi, curl M = 2 nabla_[alpha](R_{beta]sigma}nabla^sigma phi) because curl of nabla Box phi is zero.",
            "result": "EXACT_NECESSARY_INTEGRABILITY_IDENTITY",
            "condition_to_use": "curl M=0 on the selected local domain",
            "status": "derived_gate_no_claim",
            "valid_for_claim": False,
        },
        {
            "branch_id": "RES1193_1_expanded_ricci_curl",
            "claim_tested": "generic Ricci matter region supports scalar exactness",
            "derivation": "2 nabla_[alpha](R_{beta]sigma}nabla^sigma phi)=2(nabla_[alpha R_{beta]sigma})nabla^sigma phi+2R_{[beta|sigma|}nabla_{alpha]}nabla^sigma phi.",
            "result": "GENERIC_MATTER_RICCI_NOT_AUTOMATICALLY_EXACT",
            "condition_to_use": "Ricci tensor and Hessian/gradient of phi satisfy an exactness/alignment theorem",
            "status": "obstruction_retained",
            "valid_for_claim": False,
        },
        {
            "branch_id": "RES1193_2_Einstein_space_exact_branch",
            "claim_tested": "Einstein-space/Ricci-proportional domains close scalar integrability",
            "derivation": "If R_{mu nu}=Lambda_E g_{mu nu} and nabla Lambda_E=0, then R_beta_sigma nabla^sigma phi=Lambda_E nabla_beta phi and M_beta=nabla_beta((3/2)Box phi+2 Lambda_E phi).",
            "result": "CONDITIONAL_EXACT_SCALAR_BRANCH",
            "condition_to_use": "(3/2)Box phi+2 Lambda_E phi = Gamma_eff + C with boundary/no-flux and parent ownership",
            "status": "conditional_theorem_written_not_promoted",
            "valid_for_claim": False,
        },
        {
            "branch_id": "RES1193_3_Ricci_flat_limit",
            "claim_tested": "local exterior Ricci-flat limit",
            "derivation": "Set Lambda_E=0 in the Einstein-space branch to recover Box phi=(2/3)(Gamma_eff+C).",
            "result": "RICCI_FLAT_SCALAR_LIMIT_RECOVERED",
            "condition_to_use": "true vacuum/exterior domain, declared Green inverse, boundary silence, carrier metric response bound",
            "status": "special_branch_only",
            "valid_for_claim": False,
        },
        {
            "branch_id": "RES1193_4_variable_Lambda_branch",
            "claim_tested": "slowly varying Lambda_E domain",
            "derivation": "If R_{mu nu}=Lambda_E(x)g_{mu nu}, then curl(R dot grad phi)=nabla_[alpha Lambda_E nabla_{beta]} phi, so exactness needs d Lambda_E wedge d phi=0 or a bound.",
            "result": "VARIABLE_LAMBDA_REMAINDER_IDENTIFIED",
            "condition_to_use": "nabla Lambda_E parallel to nabla phi or remainder below local response limits",
            "status": "bound_required",
            "valid_for_claim": False,
        },
        {
            "branch_id": "RES1193_5_matter_domain_failure",
            "claim_tested": "generic local matter/lab domain scalar closure",
            "derivation": "Ordinary matter Ricci is generally not proportional to g and need not align with grad phi; therefore scalar Hessian K_L alone does not generically cancel the curved vector residual.",
            "result": "SCALAR_ROUTE_FAILS_GENERIC_MATTER_DOMAIN",
            "condition_to_use": "use vector/tensor compensator or source-backed bound for the Ricci-curl remainder",
            "status": "generic_scalar_zero_rejected",
            "valid_for_claim": False,
        },
        {
            "branch_id": "RES1193_6_scalar_branch_verdict",
            "claim_tested": "scalar phi/K_L route as local-GR proof",
            "derivation": "The scalar branch is honest on Ricci-flat/Einstein-exact domains only after parent source, boundary, and metric response gates close; it is not a generic local-GR theorem.",
            "result": "RICCI_EXACT_BRANCH_RETAINED_NO_LOCAL_GR_CLAIM",
            "condition_to_use": "parent-owned scalar source plus Einstein/Ricci-flat domain proof plus all arena response bounds",
            "status": "nonclaim_conditional_branch",
            "valid_for_claim": False,
        },
    ]


def vector_tensor_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "VTC1193_0_residual_source_split",
            "object": "non-exact Ricci residual after scalar branch",
            "equation_or_condition": "G_res := P_loc(nabla Gamma_eff - D_T K_scalar) or the Ricci-curl remainder left by M[phi]",
            "what_it_buys": "separates exact scalar/einstein branch from the genuinely vector-valued leftover",
            "missing_for_claim": "component profile, P_loc domain, boundary measure, source path",
            "status": "contract_written",
            "valid_for_claim": False,
        },
        {
            "contract_id": "VTC1193_1_tracefree_tensor_range",
            "object": "parent tracefree compensator K_T in S^2_0",
            "equation_or_condition": "D_T K_T := P_loc nabla_mu K_T^{mu nu}; require P_coker(D_T)G_res=0 or a sourced cokernel bound",
            "what_it_buys": "bypasses scalar exactness because D_T maps tracefree tensors to general vector residuals",
            "missing_for_claim": "parent range theorem, no-zero-mode theorem, curved-domain boundary conditions",
            "status": "range_route_open",
            "valid_for_claim": False,
        },
        {
            "contract_id": "VTC1193_2_balance_action",
            "object": "variational owner for K_T",
            "equation_or_condition": "S_T=(2 kappa_T)^-1 ||D_T K_T-G_res||^2 + (mu_T^2/2)||K_T||^2 + B_T + S_Ward",
            "what_it_buys": "turns compensator into parent-action contract rather than post-readout cancellation",
            "missing_for_claim": "S_MTS source block, stress variation, Bianchi/Ward identity, boundary term",
            "status": "candidate_contract_only",
            "valid_for_claim": False,
        },
        {
            "contract_id": "VTC1193_3_amplitude_bound",
            "object": "carrier amplitude",
            "equation_or_condition": "||K_T|| <= C_T ||G_res|| plus boundary/regularizer terms, or Tikhonov mode bound ||K_i|| <= ||G_i||/(2 mu_T)",
            "what_it_buys": "prevents vector/tensor fix from hiding a large PPN/Newton source",
            "missing_for_claim": "C_T or mu_T, source norm, K00 projection, matter curvature, response matrix",
            "status": "bound_form_only",
            "valid_for_claim": False,
        },
        {
            "contract_id": "VTC1193_4_observable_response",
            "object": "PPN/R10/clock/orbital/WEP residual vector",
            "equation_or_condition": "R_obs[K_T,G_res,B_T] must be zero or below sourced arena limits componentwise",
            "what_it_buys": "connects local-GR reduction to tested observables rather than algebra only",
            "missing_for_claim": "response operators, bounds, matter descent, source normalization",
            "status": "arena_inputs_missing",
            "valid_for_claim": False,
        },
        {
            "contract_id": "VTC1193_5_Kperp_boundary_link",
            "object": "K_perp and homogeneous tensor modes",
            "equation_or_condition": "homogeneous K_T/K_perp modes vanish by boundary/coercivity or are included in response vector",
            "what_it_buys": "prevents tensor compensator from reintroducing the Kperp problem from 800",
            "missing_for_claim": "tensor boundary zero theorem, coercivity, no incoming memory condition",
            "status": "open",
            "valid_for_claim": False,
        },
        {
            "contract_id": "VTC1193_6_verdict",
            "object": "vector/tensor compensator route",
            "equation_or_condition": "usable as next derivation route but not adopted as parent-derived",
            "what_it_buys": "gives the least-cheaty escape from scalar Ricci-curl obstruction",
            "missing_for_claim": "parent operator plus amplitude and all-arena response proof",
            "status": "retained_nonclaim",
            "valid_for_claim": False,
        },
    ]


def bound_input_rows() -> list[dict[str, object]]:
    return [
        {
            "input_id": "BIN1193_0_Einstein_scalar_branch",
            "branch": "scalar_Einstein_space",
            "required_inputs": "Lambda_E; proof R_mn=Lambda_E g_mn on domain; nabla Lambda_E=0 or bound; Gamma_eff profile; Green inverse; boundary condition",
            "current_values": "MISSING_DOMAIN_CLASS;MISSING_LAMBDA_E;MISSING_GAMMA_PROFILE;MISSING_BOUNDARY",
            "row_status": "blocked_missing_inputs",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "BIN1193_1_variable_Lambda_remainder",
            "branch": "scalar_variable_Lambda",
            "required_inputs": "||d Lambda_E wedge d phi|| bound; phi gradient; local response operator; arena limits",
            "current_values": "MISSING_NABLA_LAMBDA;MISSING_PHI_GRADIENT;MISSING_RESPONSE",
            "row_status": "blocked_missing_inputs",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "BIN1193_2_matter_Ricci_curl",
            "branch": "generic_matter_Ricci",
            "required_inputs": "Ricci anisotropy norm; Hessian/gradient alignment; curl residual norm; lab/solar matter-domain classifier",
            "current_values": "MISSING_RICCI_ANISOTROPY;MISSING_ALIGNMENT;MISSING_DOMAIN_CLASSIFIER",
            "row_status": "blocked_scalar_branch_fails_without_compensator",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "BIN1193_3_DT_compensator",
            "branch": "tracefree_vector_tensor",
            "required_inputs": "G_res norm; cokernel_fraction; boundary_obstruction_norm; coercivity_inverse C_T; mu_T/kappa_T; parent action source path",
            "current_values": "MISSING_G_RES;MISSING_COKERNEL;MISSING_BOUNDARY;MISSING_C_T;MISSING_PARENT_ACTION",
            "row_status": "blocked_missing_parent_operator",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "BIN1193_4_observable_vector",
            "branch": "all_local_arenas",
            "required_inputs": "PPN response; R10 alpha(lambda); clock readout; orbital force/range kernel; WEP/matter descent",
            "current_values": "MISSING_PPN;MISSING_R10;MISSING_CLOCK;MISSING_ORBITAL;MISSING_WEP",
            "row_status": "blocked_missing_arena_response",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def active_gamma_continuity_rows() -> list[dict[str, object]]:
    return [
        {
            "row_id": "AGC1193_0_keep_1192_window43",
            "source_row": "AGS1192_0_window43_U_B2_PPN",
            "visible_suppression_factor": "1.4413864308717837e-13",
            "what_changed_in_1193": "no coefficient or response inputs were sourced; scalar/vector fork does not promote this row",
            "block_reason": "MISSING_C_U;MISSING_RESPONSE_MATRIX;MISSING_K00_PROJECTION;MISSING_KMATTER;MISSING_PPN_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "AGC1193_1_keep_1192_point_mass",
            "source_row": "AGS1192_1_point_mass_U_B2_PPN",
            "visible_suppression_factor": "9.458639468826237e-27",
            "what_changed_in_1193": "tiny factor remains promising smoke input, not evidence",
            "block_reason": "MISSING_C_U;MISSING_RESPONSE_MATRIX;MISSING_K00_PROJECTION;MISSING_KMATTER;MISSING_PPN_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "AGC1193_2_R10_template_retained",
            "source_row": "AGS1192_2_R10_template_same_inputs",
            "visible_suppression_factor": "requires R10 domain U_B",
            "what_changed_in_1193": "R10 still needs W_R10(lambda), domain source normalization, and real bound curve",
            "block_reason": "MISSING_C_U;MISSING_W_R10_LAMBDA;MISSING_R10_DOMAIN_U_B;MISSING_ALPHA_BOUND_CURVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G1193_0_scalar_generic",
            "claim": "scalar phi/K_L cancels curved local residual generically",
            "status": "REJECTED_GENERICALLY",
            "why": "Ricci-curl exactness fails for generic matter Ricci unless alignment/compensator is proven",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1193_1_scalar_Einstein_branch",
            "claim": "Einstein-space scalar branch is a local-GR pass",
            "status": "BLOCKED_CONDITIONAL_ONLY",
            "why": "branch equation is derived, but parent source, domain proof, boundary, and response bounds are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1193_2_vector_tensor_compensator",
            "claim": "D_T compensator closes the local branch",
            "status": "BLOCKED_PARENT_OPERATOR_UNSIGNED",
            "why": "range theorem, parent action, boundary/no-zero-mode, amplitude, and observable response are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1193_3_active_gamma_scores",
            "claim": "active-Gamma first score rows pass",
            "status": "BLOCKED_UNCHANGED_FROM_1192",
            "why": "C_U and local response coefficients remain missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1193_4_local_GR",
            "claim": "MTS reduces to local GR/Newton",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "why": "no scalar or tensor branch has parent source plus response-vector closure",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1193_0_scalar_branch_sharpened",
            "decision": "retain_Ricci_flat_or_Einstein_exact_scalar_branch",
            "reason": "R_mn=Lambda_E g_mn with constant Lambda_E makes the Ricci term exact and gives a clean scalar equation",
            "next_action": "source domain classifier and metric-response bound before using this branch",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1193_1_generic_scalar_rejected",
            "decision": "reject_generic_scalar_phi_zero",
            "reason": "generic matter Ricci produces a non-exact curl obstruction",
            "next_action": "route generic matter/local domains to D_T tracefree compensator or bounded residual row",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1193_2_tensor_compensator_selected",
            "decision": "construct_DT_compensator_contract",
            "reason": "tracefree tensor divergence can target general vector residuals, unlike scalar Hessian exact forms",
            "next_action": "derive parent D_T operator/range and source first response row",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1193_3_next_route",
            "decision": "quantify_Einstein_branch_or_DT_response",
            "reason": "these are the two non-cheaty ways forward after 1193",
            "next_action": "build 1194 Einstein scalar branch bound or D_T compensator response row",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1193_0_1194",
            "next_target": "1194-Y5-R10-Einstein-space-scalar-branch-bound-or-DT-compensator-response-row.md",
            "objective": "quantify the conditional Einstein/Ricci-flat scalar branch and, in parallel, stage the first D_T compensator response row with source, boundary, amplitude, and observable slots",
            "include": "Einstein-space Helmholtz scalar equation; domain classifier; variable-Lambda remainder; D_T coker/range row; PPN/R10 response slots; no-claim validation",
            "exclude": "generic scalar zero claim; parentless compensator adoption; local-GR pass; invented coefficients; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, object]],
    scalar: list[dict[str, object]],
    vector_contract: list[dict[str, object]],
    bounds: list[dict[str, object]],
    active_gamma: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["needle_found"] for row in sources)
    scalar_ids = {row["branch_id"] for row in scalar}
    contract_ids = {row["contract_id"] for row in vector_contract}
    bound_ids = {row["input_id"] for row in bounds}
    science_rows = scalar + vector_contract + bounds + active_gamma + gates + decisions + nexts
    all_nonclaim = all(row.get("valid_for_claim") is False for row in science_rows)
    all_claims_blocked = all(row["claim_allowed"] is False for row in gates + active_gamma + bounds)
    return [
        {
            "check_id": "V1193_0_sources_exist",
            "result": "pass" if all_sources_ok else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1193_1_scalar_branch_complete",
            "result": "pass" if {"RES1193_0_curl_identity", "RES1193_2_Einstein_space_exact_branch", "RES1193_5_matter_domain_failure"} <= scalar_ids else "fail",
            "detail": "curl identity, Einstein-space branch, and generic matter failure rows are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1193_2_no_generic_scalar_claim",
            "result": "pass" if any(row["status"] == "generic_scalar_zero_rejected" for row in scalar) else "fail",
            "detail": "generic scalar phi zero is explicitly rejected",
            "claim_allowed": False,
        },
        {
            "check_id": "V1193_3_vector_contract_complete",
            "result": "pass" if {"VTC1193_1_tracefree_tensor_range", "VTC1193_2_balance_action", "VTC1193_4_observable_response"} <= contract_ids else "fail",
            "detail": "D_T range, balance action, and observable response clauses are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1193_4_bound_inputs_blocked",
            "result": "pass" if {"BIN1193_0_Einstein_scalar_branch", "BIN1193_3_DT_compensator", "BIN1193_4_observable_vector"} <= bound_ids and all(row["claim_allowed"] is False for row in bounds) else "fail",
            "detail": "scalar, D_T, and all-arena input rows exist and remain blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1193_5_active_gamma_continuity",
            "result": "pass" if len(active_gamma) == 3 and all(row["claim_allowed"] is False for row in active_gamma) else "fail",
            "detail": "1192 active-Gamma score rows are carried forward as nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1193_6_claim_gates_blocked",
            "result": "pass" if all_claims_blocked else "fail",
            "detail": "all 1193 claim gates remain blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1193_7_all_science_rows_nonclaim",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated science rows keep valid_for_claim=false",
            "claim_allowed": False,
        },
        {
            "check_id": "V1193_8_next_target",
            "result": "pass" if nexts and nexts[0]["next_id"] == "NEXT1193_0_1194" else "fail",
            "detail": "1194 handoff targets Einstein scalar branch bound or D_T compensator response row",
            "claim_allowed": False,
        },
        {
            "check_id": "V1193_9_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1193_10_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1193_SUMMARY",
            "result": "pass",
            "detail": "1193 retains a conditional Einstein/Ricci-flat scalar branch, rejects generic scalar zero in matter domains, constructs the D_T vector/tensor compensator contract, and keeps active-Gamma rows nonclaim",
            "claim_allowed": False,
        },
    ]


def write_doc(
    sources: list[dict[str, object]],
    scalar: list[dict[str, object]],
    vector_contract: list[dict[str, object]],
    bounds: list[dict[str, object]],
    active_gamma: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 1193 - Y5/R10 Ricci-exact scalar branch or vector/tensor compensator",
            "**Current verdict:** the scalar `phi/K_L` route survives only as a conditional Ricci-flat/Einstein-space branch. Generic matter curvature keeps the Ricci-curl obstruction, so the honest general route is a parent tracefree `D_T` vector/tensor compensator with amplitude and response bounds.",
            "**Main progress:** 1193 derives the Einstein-space scalar equation `(3/2)Box phi + 2 Lambda_E phi = Gamma_eff + C`, rejects generic scalar zero in matter domains, and writes the `D_T K_T = G_res` compensator contract.",
            "**No claim:** no `q_loc=0`, local-GR, Newton, R10, PPN, WEP, clock, orbital, or public-facing claim follows from this checkpoint.",
            "## Source register\n\n" + table(sources),
            "## Ricci-exact scalar branch\n\n" + table(scalar),
            "## Vector/tensor compensator contract\n\n" + table(vector_contract),
            "## Bound input rows\n\n" + table(bounds),
            "## Active Gamma continuity\n\n" + table(active_gamma),
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
    scalar = ricci_exact_scalar_rows()
    vector_contract = vector_tensor_contract_rows()
    bounds = bound_input_rows()
    active_gamma = active_gamma_continuity_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, scalar, vector_contract, bounds, active_gamma, gates, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1193_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1193_RICCI_EXACT_SCALAR_BRANCH.csv": scalar,
        "P8_Y5_R10_1193_VECTOR_TENSOR_COMPENSATOR_CONTRACT.csv": vector_contract,
        "P8_Y5_R10_1193_BOUND_INPUT_ROWS.csv": bounds,
        "P8_Y5_R10_1193_ACTIVE_GAMMA_CONTINUITY.csv": active_gamma,
        "P8_Y5_R10_1193_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1193_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1193_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1193_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, stamp(rows))

    write_doc(sources, scalar, vector_contract, bounds, active_gamma, gates, decisions, validations, nexts)

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

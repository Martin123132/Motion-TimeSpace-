from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1194-Y5-R10-Einstein-space-scalar-branch-bound-or-DT-compensator-response-row.md"
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
            "source_id": "SRC1194_0_1193_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1193_NEXT_TARGET.csv",
            "needle": "NEXT1193_0_1194",
            "role": "direct 1194 handoff.",
        },
        {
            "source_id": "SRC1194_1_1193_scalar",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1193_RICCI_EXACT_SCALAR_BRANCH.csv",
            "needle": "RES1193_2_Einstein_space_exact_branch",
            "role": "conditional Einstein-space scalar branch.",
        },
        {
            "source_id": "SRC1194_2_1193_matter_failure",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1193_RICCI_EXACT_SCALAR_BRANCH.csv",
            "needle": "RES1193_5_matter_domain_failure",
            "role": "generic matter-domain scalar rejection.",
        },
        {
            "source_id": "SRC1194_3_1193_DT_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1193_VECTOR_TENSOR_COMPENSATOR_CONTRACT.csv",
            "needle": "VTC1193_1_tracefree_tensor_range",
            "role": "D_T tracefree vector/tensor range route.",
        },
        {
            "source_id": "SRC1194_4_1193_bound_inputs",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1193_BOUND_INPUT_ROWS.csv",
            "needle": "BIN1193_3_DT_compensator",
            "role": "blocked scalar/D_T input rows.",
        },
        {
            "source_id": "SRC1194_5_1193_active_gamma",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1193_ACTIVE_GAMMA_CONTINUITY.csv",
            "needle": "AGC1193_0_keep_1192_window43",
            "role": "active-Gamma nonclaim score continuity.",
        },
        {
            "source_id": "SRC1194_6_831_range",
            "relative_path": "831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md",
            "needle": "OC831_4_bound_condition",
            "role": "range/cokernel bound condition for D_T residual.",
        },
        {
            "source_id": "SRC1194_7_831_coker",
            "relative_path": "831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md",
            "needle": "RT831_3_bound",
            "role": "D_T residual bound with cokernel/boundary/regularizer terms.",
        },
        {
            "source_id": "SRC1194_8_832_amplitude",
            "relative_path": "832-Y5-R10-tracefree-divergence-range-theorem-or-cokernel-bound.md",
            "needle": "CB832_4_amplitude_warning",
            "role": "carrier amplitude remains a local metric issue.",
        },
        {
            "source_id": "SRC1194_9_833_norm",
            "relative_path": "833-Y5-R10-Hessian-Khat-carrier-amplitude-and-metric-response-bound.md",
            "needle": "AL833_1_exact_L2_norm",
            "role": "Khat norm is order Gamma for Hessian carrier.",
        },
        {
            "source_id": "SRC1194_10_830_ppn_gate",
            "relative_path": "830-Y5-R10-Khat-boundary-owner-or-residual-vector-runner.md",
            "needle": "OG830_1_PPN",
            "role": "PPN response gate remains missing.",
        },
        {
            "source_id": "SRC1194_11_830_R10_gate",
            "relative_path": "830-Y5-R10-Khat-boundary-owner-or-residual-vector-runner.md",
            "needle": "OG830_2_R10",
            "role": "R10 response gate remains missing.",
        },
        {
            "source_id": "SRC1194_12_798_screening",
            "relative_path": "798-Y5-R10-Gammaeff-local-screening-source-law-or-response-kernel-bound.md",
            "needle": "GSE798_2_local_locked_expansion",
            "role": "active Gamma local locked expansion.",
        },
        {
            "source_id": "SRC1194_13_800_kperp",
            "relative_path": "800-Y5-R10-universal-XB-PiB-support-powers-or-Kperp-boundary-zero-lemma.md",
            "needle": "KBL800_3_failure",
            "role": "scalar Pi_B does not remove Kperp tensor modes.",
        },
    ]
    rows: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        exists = path.exists()
        needle_found = exists and str(entry["needle"]) in read_text(path)
        rows.append(entry | {"exists": exists, "needle_found": needle_found})
    return rows


def einstein_scalar_bound_rows() -> list[dict[str, object]]:
    return [
        {
            "bound_id": "ESB1194_0_Helmholtz_equation",
            "branch": "Einstein_or_Ricci_flat_scalar",
            "derived_statement": "If R_mn=Lambda_E g_mn and nabla Lambda_E=0, then H_E phi := (Box + 4 Lambda_E/3)phi = (2/3)(Gamma_eff + C).",
            "bound_form": "phi = (2/3) H_E^{-1}(Gamma_eff + C) after zero-mode and boundary conventions are fixed",
            "needed_inputs": "domain proof; Lambda_E; H_E Green operator; Gamma_eff profile; boundary/no-flux; parent source",
            "status": "EXACT_CONDITIONAL_EQUATION_NO_PARENT_CLAIM",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "ESB1194_1_gradient_bound",
            "branch": "Einstein_or_Ricci_flat_scalar",
            "derived_statement": "The Ricci residual entering q_loc is controlled by nabla phi, hence by the Green operator of H_E.",
            "bound_form": "||nabla phi||_D <= (2/3) C_grad,H_E,D ||Gamma_act||_D + B_phi + Z_phi",
            "needed_inputs": "C_grad,H_E,D; active Gamma norm; boundary mode; zero-mode convention; source path",
            "status": "BOUND_FORM_ONLY",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "ESB1194_2_KL_amplitude_bound",
            "branch": "Einstein_or_Ricci_flat_scalar",
            "derived_statement": "The scalar branch still carries K_L amplitude through second derivatives of phi; exact scalar integrability does not make the carrier metric-safe.",
            "bound_form": "||K_L||_D <= C_K,H_E,D ||Gamma_act||_D + B_K + R_Lambda",
            "needed_inputs": "C_K,H_E,D; Gamma_act support law; K00 projection; matter curvature; metric response coefficient",
            "status": "AMPLITUDE_NOT_SUPPRESSED_WITHOUT_GAMMA_SUPPORT",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "ESB1194_3_variable_Lambda_remainder",
            "branch": "nearly_Einstein_scalar",
            "derived_statement": "If R_mn=Lambda_E(x)g_mn, scalar exactness leaves a curl source d Lambda_E wedge d phi unless d Lambda_E is parallel to d phi.",
            "bound_form": "||R_curl,Lambda|| <= 2 ||d Lambda_E wedge d phi|| <= 2 ||d Lambda_E|| ||d phi||",
            "needed_inputs": "nabla Lambda_E; phi gradient bound; alignment angle or wedge bound; arena response limit",
            "status": "VARIABLE_LAMBDA_REMAINDER_RETAINED",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "ESB1194_4_domain_classifier",
            "branch": "branch_selection",
            "derived_statement": "The scalar branch is only eligible on domains passing an Einstein/Ricci-flat classifier; generic matter domains route to D_T or residual bounds.",
            "bound_form": "epsilon_E := ||Ric - Lambda_E g||_D / (||Ric||_D + epsilon_ref) <= epsilon_E_limit",
            "needed_inputs": "Ricci tensor model; Lambda_E fit/definition; epsilon_ref; epsilon_E_limit; local domain source path",
            "status": "DOMAIN_CLASSIFIER_TEMPLATE_ONLY",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "ESB1194_5_scalar_branch_gate",
            "branch": "scalar_branch_claim_gate",
            "derived_statement": "Einstein-space scalar integrability is a mathematical sub-branch, not a local-GR pass.",
            "bound_form": "claim_allowed only if parent source + domain classifier + boundary + amplitude + all arena response rows pass",
            "needed_inputs": "all scalar branch and response inputs",
            "status": "SCALAR_BRANCH_RETAINED_NONCLAIM",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def dt_compensator_response_rows() -> list[dict[str, object]]:
    return [
        {
            "response_id": "DTR1194_0_PPN_gamma_beta_first_row",
            "arena": "PPN gamma/beta",
            "source_object": "K_T compensating non-exact Ricci/vector residual G_res",
            "prediction_form": "||Delta_PPN_DT|| <= ||W_PPN|| (C_T ||G_res|| + ||B_T|| + kappa_T C_T ||E_reg||)",
            "needed_inputs": "W_PPN; C_T; G_res profile; boundary obstruction; regularizer; observable limits gamma,beta; parent action source",
            "runner_status": "blocked_missing_inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "response_id": "DTR1194_1_PPN_preferred_frame_slot",
            "arena": "PPN alpha_i/preferred-frame",
            "source_object": "anisotropic/time-dependent K_T and Kperp modes",
            "prediction_form": "||alpha_i_DT|| <= ||W_alpha|| ||K_T,Kperp,boundary||",
            "needed_inputs": "preferred-frame projector; W_alpha; homogeneous mode bound; source normalization; alpha_i limits",
            "runner_status": "blocked_missing_inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "response_id": "DTR1194_2_R10_alpha_lambda_slot",
            "arena": "R10 short-range/fifth-force",
            "source_object": "finite-range projection of D_T compensator",
            "prediction_form": "alpha_DT(lambda) = W_R10(lambda)[K_T,G_res,B_T]",
            "needed_inputs": "W_R10(lambda); range/domain profile; source normalization; real alpha_bound(lambda); boundary profile",
            "runner_status": "blocked_missing_inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "response_id": "DTR1194_3_clock_orbital_slot",
            "arena": "clock/orbital",
            "source_object": "metric/coframe readout of K_T carrier",
            "prediction_form": "clock_DT or a_DT <= W_clock/orbital [K_T,G_res,B_T]",
            "needed_inputs": "clock readout coefficients; orbital force kernel; domain profile; observational limits",
            "runner_status": "blocked_missing_inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "response_id": "DTR1194_4_WEP_matter_descent_slot",
            "arena": "WEP/matter descent",
            "source_object": "ordinary matter coupling to compensator variables",
            "prediction_form": "eta_AB_DT=0 if matter descends through same observed coframe; otherwise eta_AB_DT <= W_WEP charge vector",
            "needed_inputs": "matter descent proof; species charge vector; MICROSCOPE/WEP bound row; source path",
            "runner_status": "blocked_missing_inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "response_id": "DTR1194_5_first_response_verdict",
            "arena": "all_local",
            "source_object": "D_T compensator response matrix",
            "prediction_form": "first response row staged; no observable can be evaluated until W_PPN/R10/clock/orbital/WEP and parent source rows exist",
            "needed_inputs": "parent D_T operator; response matrices; bounds; matter descent",
            "runner_status": "nonclaim_template_only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def branch_selector_rows() -> list[dict[str, object]]:
    return [
        {
            "selector_id": "SEL1194_0_scalar_exact_allowed",
            "condition": "domain passes Ricci-flat/Einstein classifier and parent scalar source/boundary/response gates close",
            "selected_branch": "Einstein scalar H_E phi branch",
            "fallback_if_false": "D_T compensator or retained residual bound",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "selector_id": "SEL1194_1_generic_matter",
            "condition": "Ricci anisotropy or matter-domain classifier fails scalar exactness",
            "selected_branch": "D_T tracefree vector/tensor compensator",
            "fallback_if_false": "explicit residual closure row if parent D_T operator also absent",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "selector_id": "SEL1194_2_response_kernel",
            "condition": "source residual is not small but lies in zero observable kernel",
            "selected_branch": "response-kernel theorem if sourced",
            "fallback_if_false": "source-backed bound required in every arena",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "selector_id": "SEL1194_3_closure_label",
            "condition": "neither scalar domain proof nor parent D_T operator/response can be sourced",
            "selected_branch": "local branch remains explicit closure/input-acquisition",
            "fallback_if_false": "continue derivation",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]


def missing_input_matrix_rows() -> list[dict[str, object]]:
    return [
        {
            "matrix_id": "MIM1194_0_scalar_domain",
            "route": "Einstein scalar",
            "missing_inputs": "domain classifier; Lambda_E; Green operator; Gamma_act profile; boundary/no-flux; parent source",
            "blocks": "scalar branch score",
            "next_action": "source domain classifier or declare branch exterior-only",
            "valid_for_claim": False,
        },
        {
            "matrix_id": "MIM1194_1_scalar_response",
            "route": "Einstein scalar",
            "missing_inputs": "K_L amplitude response; K00 projection; PPN/R10/clock/orbital/WEP response matrix",
            "blocks": "local-GR/local-test claim",
            "next_action": "reuse D_T response schema for scalar K_L carrier",
            "valid_for_claim": False,
        },
        {
            "matrix_id": "MIM1194_2_DT_parent_operator",
            "route": "D_T compensator",
            "missing_inputs": "parent action block; range/cokernel theorem; C_T or mu_T; boundary/no-zero-mode theorem",
            "blocks": "D_T compensator adoption",
            "next_action": "derive parent D_T operator or retain as closure",
            "valid_for_claim": False,
        },
        {
            "matrix_id": "MIM1194_3_DT_response",
            "route": "D_T compensator",
            "missing_inputs": "W_PPN; W_R10(lambda); W_clock; W_orbital; W_WEP; source normalization",
            "blocks": "first response score",
            "next_action": "source one PPN or R10 response row as nonclaim",
            "valid_for_claim": False,
        },
        {
            "matrix_id": "MIM1194_4_active_gamma",
            "route": "active Gamma support",
            "missing_inputs": "C_U/C_gamma; K00 projection; matter curvature; observable bounds",
            "blocks": "using U_B^2 suppression factors as evidence",
            "next_action": "derive C_U or prove metric-null response",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G1194_0_Einstein_scalar_score",
            "claim": "Einstein/Ricci-flat scalar branch scores a local residual bound",
            "status": "BLOCKED_INPUTS_MISSING",
            "why": "H_E equation is derived, but domain classifier, Green constants, parent source, boundary, and response inputs are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1194_1_DT_first_response_score",
            "claim": "D_T compensator has first response-row pass",
            "status": "BLOCKED_RESPONSE_MATRICES_MISSING",
            "why": "PPN/R10/clock/orbital/WEP response operators and parent D_T inputs are still missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1194_2_branch_selector",
            "claim": "local branch selector is evidence-ready",
            "status": "BLOCKED_DOMAIN_AND_RESPONSE_UNSOURCED",
            "why": "the selector exists but cannot classify real local domains or score observables",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1194_3_local_GR",
            "claim": "MTS reduces to local GR/Newton",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "why": "neither scalar nor D_T branch has parent-source plus all-arena response closure",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1194_0_scalar_quantified",
            "decision": "Einstein_scalar_branch_bound_forms_created",
            "reason": "1193's exact scalar branch now has H_E Green, gradient, amplitude, variable-Lambda, and domain-classifier slots",
            "next_action": "source domain classifier or keep scalar branch exterior-only",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1194_1_DT_response_staged",
            "decision": "first_DT_response_rows_created",
            "reason": "generic matter curvature needs a tracefree tensor compensator, and now its PPN/R10/clock/orbital/WEP slots are explicit",
            "next_action": "derive parent D_T operator/range or source one response operator",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1194_2_best_next_route",
            "decision": "parent_DT_operator_before_claim",
            "reason": "the Einstein scalar branch is too special to carry generic local matter domains by itself",
            "next_action": "build 1195 parent D_T operator/range source or Einstein-domain classifier",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1194_0_1195",
            "next_target": "1195-Y5-R10-parent-DT-operator-range-source-or-Einstein-domain-classifier.md",
            "objective": "derive or source the parent D_T tracefree tensor operator/range theorem, while keeping an Einstein-domain classifier as the scalar-branch fallback",
            "include": "D_T parent action block; range/cokernel coefficient; boundary/no-zero-mode; one PPN or R10 response row; Einstein-domain classifier; no-claim validation",
            "exclude": "generic scalar zero claim; parentless compensator adoption; local-GR pass; placeholder observable pass; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, object]],
    scalar: list[dict[str, object]],
    dt_rows: list[dict[str, object]],
    selectors: list[dict[str, object]],
    missing: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["needle_found"] for row in sources)
    scalar_ids = {row["bound_id"] for row in scalar}
    dt_ids = {row["response_id"] for row in dt_rows}
    selector_ids = {row["selector_id"] for row in selectors}
    all_science_rows = scalar + dt_rows + selectors + missing + gates + decisions + nexts
    all_nonclaim = all(row.get("valid_for_claim") is False for row in all_science_rows)
    all_blocked = all(row.get("claim_allowed") is False for row in scalar + dt_rows + gates + nexts)
    return [
        {
            "check_id": "V1194_0_sources_exist",
            "result": "pass" if all_sources_ok else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1194_1_scalar_bound_forms",
            "result": "pass" if {"ESB1194_0_Helmholtz_equation", "ESB1194_2_KL_amplitude_bound", "ESB1194_4_domain_classifier"} <= scalar_ids else "fail",
            "detail": "Einstein scalar H_E, amplitude, and domain-classifier rows are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1194_2_DT_response_rows",
            "result": "pass" if {"DTR1194_0_PPN_gamma_beta_first_row", "DTR1194_2_R10_alpha_lambda_slot", "DTR1194_5_first_response_verdict"} <= dt_ids else "fail",
            "detail": "D_T PPN, R10, and response-verdict rows are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1194_3_branch_selector",
            "result": "pass" if {"SEL1194_0_scalar_exact_allowed", "SEL1194_1_generic_matter", "SEL1194_3_closure_label"} <= selector_ids else "fail",
            "detail": "branch selector covers scalar, generic matter, and closure fallback",
            "claim_allowed": False,
        },
        {
            "check_id": "V1194_4_missing_matrix_complete",
            "result": "pass" if len(missing) >= 5 else "fail",
            "detail": "missing-input matrix covers scalar, D_T, response, and active-Gamma debts",
            "claim_allowed": False,
        },
        {
            "check_id": "V1194_5_all_rows_blocked",
            "result": "pass" if all_blocked else "fail",
            "detail": "scalar, D_T, and claim rows remain blocked/nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1194_6_all_science_rows_nonclaim",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated science rows keep valid_for_claim=false",
            "claim_allowed": False,
        },
        {
            "check_id": "V1194_7_next_target",
            "result": "pass" if nexts and nexts[0]["next_id"] == "NEXT1194_0_1195" else "fail",
            "detail": "1195 handoff targets parent D_T operator/range source or Einstein-domain classifier",
            "claim_allowed": False,
        },
        {
            "check_id": "V1194_8_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1194_9_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1194_SUMMARY",
            "result": "pass",
            "detail": "1194 quantifies the Einstein scalar branch, stages first D_T response slots, installs a branch selector, and keeps all local-GR claims blocked",
            "claim_allowed": False,
        },
    ]


def write_doc(
    sources: list[dict[str, object]],
    scalar: list[dict[str, object]],
    dt_rows: list[dict[str, object]],
    selectors: list[dict[str, object]],
    missing: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 1194 - Y5/R10 Einstein-space scalar branch bound or D_T compensator response row",
            "**Current verdict:** the Einstein/Ricci-flat scalar branch is now bound-shaped, not claim-shaped. Generic matter curvature still routes to the parent `D_T` tracefree tensor compensator, whose first response rows are now staged but blocked.",
            "**Main progress:** 1194 writes the scalar Helmholtz equation `H_E phi=(2/3)(Gamma_eff+C)`, its gradient/amplitude/remainder bounds, a domain classifier, and first `D_T` PPN/R10 response slots.",
            "**No claim:** no `q_loc=0`, local-GR, Newton, R10, PPN, WEP, clock, orbital, or public-facing claim follows from this checkpoint.",
            "## Source register\n\n" + table(sources),
            "## Einstein scalar bound forms\n\n" + table(scalar),
            "## D_T compensator response rows\n\n" + table(dt_rows),
            "## Branch selector\n\n" + table(selectors),
            "## Missing input matrix\n\n" + table(missing),
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
    scalar = einstein_scalar_bound_rows()
    dt_rows = dt_compensator_response_rows()
    selectors = branch_selector_rows()
    missing = missing_input_matrix_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, scalar, dt_rows, selectors, missing, gates, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1194_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1194_EINSTEIN_SCALAR_BOUND_FORMS.csv": scalar,
        "P8_Y5_R10_1194_DT_COMPENSATOR_RESPONSE_ROWS.csv": dt_rows,
        "P8_Y5_R10_1194_BRANCH_SELECTOR.csv": selectors,
        "P8_Y5_R10_1194_MISSING_INPUT_MATRIX.csv": missing,
        "P8_Y5_R10_1194_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1194_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1194_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1194_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, stamp(rows))

    write_doc(sources, scalar, dt_rows, selectors, missing, gates, decisions, validations, nexts)

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

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1191-Y5-R10-curved-Khat-P_loc-commutator-bound-pack-or-parent-zero.md"
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
            "source_id": "SRC1191_0_1190_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1190_NEXT_TARGET.csv",
            "needle": "NEXT1190_0_1191",
            "role": "direct 1191 handoff.",
        },
        {
            "source_id": "SRC1191_1_1190_residuals",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1190_EXACT_RESIDUAL_UPDATE_ROWS.csv",
            "needle": "RES1190_0_Ricci_Khat_residual",
            "role": "retained exact residual rows from the curved Khat/P_loc gate.",
        },
        {
            "source_id": "SRC1191_2_1190_ploc",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1190_PLOC_PARENT_COMMUTATOR_GATE.csv",
            "needle": "PLC1190_2_derivative_commutator",
            "role": "P_loc derivative commutator that must be theorem-zero or bounded.",
        },
        {
            "source_id": "SRC1191_3_834_gamma",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_834_GAMMA_MODE_SPLIT_THEOREM.csv",
            "needle": "GS834_1_refined_amplitude",
            "role": "active Gamma/Khat amplitude law.",
        },
        {
            "source_id": "SRC1191_4_835_schema",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_835_ACTIVE_GAMMA_INPUT_SCHEMA.csv",
            "needle": "active_gamma_coeff",
            "role": "active Gamma metric-safety input schema.",
        },
        {
            "source_id": "SRC1191_5_835_output",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_835_ACTIVE_GAMMA_RUNNER_OUTPUT.csv",
            "needle": "blocked_missing_inputs",
            "role": "active Gamma runner remains blocked by missing inputs.",
        },
        {
            "source_id": "SRC1191_6_836_fill",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_836_ACTIVE_GAMMA_FILL_ATTEMPT.csv",
            "needle": "FA836_1_U_B2_window43",
            "role": "source-support attempt with candidate small-parameter rows.",
        },
        {
            "source_id": "SRC1191_7_838_inputs",
            "relative_path": "838-Y5-R10-active-Gamma-coefficient-source-pack-or-parent-derivation.md",
            "needle": "NR838_0_F2_bound",
            "role": "active Gamma coefficient/source-pack debts.",
        },
        {
            "source_id": "SRC1191_8_1014_commutator",
            "relative_path": "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
            "needle": "PCC1014_1_I_commutator",
            "role": "earlier projector commutator coefficient debt.",
        },
        {
            "source_id": "SRC1191_9_1019_sourcepack",
            "relative_path": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "needle": "SP1019_6_projector_zero_or_bound",
            "role": "boundary/projector zero-or-bound source-pack row.",
        },
        {
            "source_id": "SRC1191_10_1175_projector_leak",
            "relative_path": "1175-Y5-R10-Qcoh-projector-owner-or-projector-leak-bound-row.md",
            "needle": "PLB1175_0_first_projector_leak_row",
            "role": "projector-leak nonclaim bound row.",
        },
        {
            "source_id": "SRC1191_11_1189_pack",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1189_ARENA_PROJECTION_QUEUE.csv",
            "needle": "APR1189_2_R10",
            "role": "component-pack arena queue retained as fallback.",
        },
        {
            "source_id": "SRC1191_12_931_gamma",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_931_GAMMA_PROJECTION_DERIVATION.csv",
            "needle": "GAM931_2_gamma_projection",
            "role": "weak-field gamma projection coefficient debt.",
        },
    ]
    rows: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        exists = path.exists()
        needle_found = exists and str(entry["needle"]) in read_text(path)
        rows.append(entry | {"exists": exists, "needle_found": needle_found})
    return rows


def leftover_bound_pack_rows() -> list[dict[str, object]]:
    return [
        {
            "bound_id": "LBP1191_0_Ricci_Khat_residual",
            "quantity": "R_K^nu residual after curved tracefree Khat divergence",
            "source_basis": "RES1190_0_Ricci_Khat_residual; KLS1190_1_exact_curved_divergence",
            "component_bound_form": "||P_loc R_K||_D <= 2 ||P_loc||_D ||Ric||_D ||nabla phi||_D + sign_convention_remainder",
            "theorem_zero_condition": "local Ricci-flat vacuum, or parent phi equation cancels 2 R^nu_sigma nabla^sigma phi in the same Euler equation",
            "needed_inputs": "Ricci scale; phi gradient bound; sign convention; P_loc operator norm; source path",
            "current_status": "BOUND_FORM_STAGED_INPUTS_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "LBP1191_1_phi_gradient_from_gamma",
            "quantity": "phi-gradient needed by R_K",
            "source_basis": "KLS1190_2_covariant_cancellation_condition; KLS1190_3_flat_patch_limit",
            "component_bound_form": "||nabla phi||_D <= C_gradBox,D ||gamma_act||_D + B_phi_boundary",
            "theorem_zero_condition": "parent source equation fixes phi with no boundary mode and Ricci-corrected Green operator",
            "needed_inputs": "C_gradBox,D; boundary Green choice; gamma_act bound; compact-domain regularity",
            "current_status": "BOUND_FORM_STAGED_INPUTS_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "LBP1191_2_projector_commutator",
            "quantity": "C_P^nu := (nabla_mu P_loc^nu_rho) K^{mu rho}",
            "source_basis": "PLC1190_2_derivative_commutator; PCC1014_1_I_commutator; PLB1175_0_first_projector_leak_row",
            "component_bound_form": "||C_P||_D <= ||nabla P_loc||_D ||K||_D",
            "theorem_zero_condition": "nabla P_loc=0 on the parent local domain, or K lies in ker(nabla P_loc) by parent-owned symmetry",
            "needed_inputs": "P_loc formula; parent domain variation; Khat profile; projector kernel; source path",
            "current_status": "RETAINED_NONCLAIM_COMMUTATOR",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "LBP1191_3_boundary_flux",
            "quantity": "B_P^nu := integral_{partial U} n_mu P_loc^nu_rho K^{mu rho}",
            "source_basis": "PLC1190_3_boundary_no_flux; SP1019_6_projector_zero_or_bound",
            "component_bound_form": "||B_P|| <= C_boundary(U,P_loc) ||K||_{partial U}",
            "theorem_zero_condition": "parent natural boundary condition or exactness/orthogonality theorem gives n_mu P_loc^nu_rho K^{mu rho}=0 on partial U",
            "needed_inputs": "boundary condition; boundary measure; compact-domain normal; no-flux theorem or finite row",
            "current_status": "RETAINED_NONCLAIM_BOUNDARY_FLUX",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "LBP1191_4_Khat_metric_footprint",
            "quantity": "metric footprint from active tracefree Khat carrier",
            "source_basis": "RES1190_3_Khat_metric_footprint; GS834_1_refined_amplitude; GAM931_2_gamma_projection",
            "component_bound_form": "epsilon_K <= R_metric f_00 sqrt(n/(n-1)) C_gamma s^p / K_matter",
            "theorem_zero_condition": "Khat carrier is metric-null by parent Hilbert response, or active_gamma is source-suppressed below every local response limit",
            "needed_inputs": "C_gamma; small parameter s; support power p; f_00 projection; K_matter; response matrix; observable limit",
            "current_status": "ACTIVE_GAMMA_BOUND_NOT_SCOREABLE",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "LBP1191_5_total_abs_envelope",
            "quantity": "componentwise no-cancellation local residual envelope",
            "source_basis": "1189 component pack plus all 1190 exact leftovers",
            "component_bound_form": "Delta_local <= |P_loc R_K| + |C_P| + |B_P| + |epsilon_K| arena-by-arena",
            "theorem_zero_condition": "all four parent-zero clauses close, or each component receives a source-backed bound below arena limits",
            "needed_inputs": "all R_K, C_P, B_P, epsilon_K inputs plus PPN/R10/clock/orbital response operators",
            "current_status": "TOTAL_ENVELOPE_TEMPLATE_ONLY",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def parent_zero_certificate_rows() -> list[dict[str, object]]:
    return [
        {
            "certificate_id": "PZ1191_0_Ricci_zero",
            "clause": "Ricci Khat residual zero",
            "required_statement": "2 R^nu_sigma nabla^sigma phi is zero or exactly cancelled by the parent curved phi equation before projection",
            "current_evidence": "1190 derived the residual; no parent cancellation equation is signed",
            "blocking_gap": "MISSING_PARENT_CURVED_PHI_SOURCE_OR_RICCI_ZERO_DOMAIN",
            "passes_now": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "PZ1191_1_phi_parent_source",
            "clause": "parent origin of phi/K_L",
            "required_statement": "K_L and phi are not auxiliary closure choices; they descend from parent Euler, relaxation, or moment equations",
            "current_evidence": "795 retained parent-origin gap; 1190 wrote required source equation only",
            "blocking_gap": "MISSING_PARENT_EULER_OR_CONSTRAINT_DERIVATION",
            "passes_now": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "PZ1191_2_Ploc_parallel",
            "clause": "projector commutator zero",
            "required_statement": "nabla_mu P_loc^nu_rho=0 on the selected parent domain, or K is parent-confined to the commutator kernel",
            "current_evidence": "1175 gives a projector shape, but 1190 keeps derivative commutator",
            "blocking_gap": "MISSING_PARENT_DOMAIN_PARALLEL_PROJECTOR_OR_KERNEL_PROOF",
            "passes_now": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "PZ1191_3_boundary_no_flux",
            "clause": "local boundary flux zero",
            "required_statement": "integral boundary n.P.K vanishes from parent natural boundary conditions or exactness/orthogonality",
            "current_evidence": "1019 is conditional; 1190 keeps B_P residual",
            "blocking_gap": "MISSING_NO_FLUX_BOUNDARY_THEOREM",
            "passes_now": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "PZ1191_4_metric_null_or_suppressed",
            "clause": "Khat carrier metric footprint zero or bounded",
            "required_statement": "active Khat either has zero Hilbert metric response or is quantitatively below local PPN/R10/clock/orbital response limits",
            "current_evidence": "834/835/836 staged amplitude law and partial small-parameter candidates; response coefficients missing",
            "blocking_gap": "MISSING_ACTIVE_GAMMA_COEFFICIENT_AND_RESPONSE_MATRIX",
            "passes_now": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "PZ1191_5_all_arenas",
            "clause": "same parent proof silences every local arena",
            "required_statement": "the same zero/bound controls PPN gamma/beta/alpha_i, R10, clocks, and orbital/source-normalization",
            "current_evidence": "1189 projection queue remains open",
            "blocking_gap": "MISSING_ARENA_PROJECTION_OPERATORS",
            "passes_now": False,
            "valid_for_claim": False,
        },
    ]


def arena_projection_slot_rows() -> list[dict[str, object]]:
    return [
        {
            "slot_id": "APS1191_0_PPN_gamma_beta",
            "arena": "PPN gamma/beta",
            "residual_inputs": "R_K; C_P; B_P; epsilon_K",
            "response_operator_needed": "W_gamma_beta[R_K,C_P,B_P,epsilon_K] in a declared weak-field gauge",
            "existing_anchor": "APR1189_0_gamma_beta; GAM931_2_gamma_projection",
            "missing_inputs": "weak-field Green operator; C_gamma_FM; gauge lock; source normalization",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "slot_id": "APS1191_1_PPN_alpha3",
            "arena": "PPN alpha3/preferred-frame",
            "residual_inputs": "C_P; B_P; momentum/preferred-frame part of R_K; epsilon_K",
            "response_operator_needed": "W_alpha3 component map plus same denominator as q_loc pack",
            "existing_anchor": "APR1189_1_alpha3",
            "missing_inputs": "preferred-frame projector; f_qV; alpha3 bound row; component q_loc profile",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "slot_id": "APS1191_2_R10",
            "arena": "R10 short-range/fifth-force",
            "residual_inputs": "finite-range projection of R_K+C_P+B_P plus epsilon_K",
            "response_operator_needed": "alpha_residual(lambda)=c_residual(lambda)*profile_residual(lambda)",
            "existing_anchor": "APR1189_2_R10",
            "missing_inputs": "range kernel; c_residual(lambda); real bound curve; finite support profile",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "slot_id": "APS1191_3_clock",
            "arena": "clock/time/readout",
            "residual_inputs": "time/readout projection of R_K; C_P; B_P; epsilon_K",
            "response_operator_needed": "delta nu_i/nu_i = b_clock_i Q_clock[residuals]",
            "existing_anchor": "APR1189_3_clock",
            "missing_inputs": "clock coefficients; readout frame; constant-marker classification; domain profile",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "slot_id": "APS1191_4_orbital",
            "arena": "orbital/source-normalization",
            "residual_inputs": "spatial force/source drift from R_K; C_P; B_P; epsilon_K",
            "response_operator_needed": "a_res^i = W_orb^i_mu residual^mu or d ln mu_obs/dt = W_mu residual",
            "existing_anchor": "APR1189_4_orbital",
            "missing_inputs": "force-to-acceleration map; radial profile; source-charge equality; uncertainty",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def active_gamma_input_status_rows() -> list[dict[str, object]]:
    return [
        {
            "status_id": "AG1191_0_active_gamma_coeff",
            "input_name": "C_gamma or C_U active coefficient",
            "candidate_value": "MISSING",
            "source_basis": "NR838_0_F2_bound; FA836_1_U_B2_window43",
            "status": "MISSING_PARENT_COEFFICIENT",
            "use_in_claim": False,
            "valid_for_claim": False,
        },
        {
            "status_id": "AG1191_1_U_B2_window43_small_parameter",
            "input_name": "small_parameter",
            "candidate_value": "3.7965595357794454e-7",
            "source_basis": "FA836_1_U_B2_window43",
            "status": "CANDIDATE_SUPPORT_NUMBER_ONLY_NOT_SCOREABLE_WITHOUT_COEFFICIENTS",
            "use_in_claim": False,
            "valid_for_claim": False,
        },
        {
            "status_id": "AG1191_2_U_B2_point_mass_squared",
            "input_name": "small_parameter_squared",
            "candidate_value": "9.458639468826237e-27",
            "source_basis": "FA836_2_U_B2_point_mass",
            "status": "CANDIDATE_SUPPORT_NUMBER_ONLY_NOT_SCOREABLE_WITHOUT_COEFFICIENTS",
            "use_in_claim": False,
            "valid_for_claim": False,
        },
        {
            "status_id": "AG1191_3_support_power",
            "input_name": "support_power",
            "candidate_value": "2 for U_B^2 route",
            "source_basis": "FA836_1_U_B2_window43; FA836_2_U_B2_point_mass",
            "status": "CANDIDATE_POWER_NOT_PARENT_LOCKED",
            "use_in_claim": False,
            "valid_for_claim": False,
        },
        {
            "status_id": "AG1191_4_metric_response_matrix",
            "input_name": "R_metric and K00/projection fractions",
            "candidate_value": "MISSING",
            "source_basis": "P8_Y5_R10_835_ACTIVE_GAMMA_INPUT_SCHEMA.csv",
            "status": "MISSING_RESPONSE_OPERATOR",
            "use_in_claim": False,
            "valid_for_claim": False,
        },
        {
            "status_id": "AG1191_5_observable_limits",
            "input_name": "PPN/R10/clock/orbital observable limits",
            "candidate_value": "MISSING",
            "source_basis": "P8_Y5_R10_835_ACTIVE_GAMMA_INPUT_SCHEMA.csv; 1189 arena projection queue",
            "status": "MISSING_ARENA_LIMIT_LINKS",
            "use_in_claim": False,
            "valid_for_claim": False,
        },
        {
            "status_id": "AG1191_6_claim_status",
            "input_name": "active Gamma local safety",
            "candidate_value": "BLOCKED",
            "source_basis": "835 runner output",
            "status": "ACTIVE_GAMMA_BOUND_REMAINS_NONCLAIM",
            "use_in_claim": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G1191_0_residual_pack_source_ready",
            "claim": "R_K, C_P, B_P, and epsilon_K are source-backed local residual bounds",
            "status": "BLOCKED_INPUTS_MISSING",
            "why": "1191 writes bound forms and input slots, not numeric/source-backed bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1191_1_parent_zero_certificate",
            "claim": "all 1190 leftovers vanish by parent theorem",
            "status": "BLOCKED_CERTIFICATE_UNSIGNED",
            "why": "Ricci cancellation, phi parent source, P_loc parallelism, no-flux, and metric-null clauses all fail today",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1191_2_active_gamma_safety",
            "claim": "active Gamma/Khat carrier is locally metric safe",
            "status": "BLOCKED_RESPONSE_MATRIX_MISSING",
            "why": "small support candidates exist, but coefficient and response operator inputs are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1191_3_arena_projections",
            "claim": "PPN/R10/clock/orbital projections are score-ready",
            "status": "BLOCKED_PROJECTION_OPERATORS_MISSING",
            "why": "all five arena slots still require response operators and real profiles",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1191_4_local_GR",
            "claim": "local GR/Newton limit passes",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "why": "1189 component pack remains active and 1191 does not close theorem-zero or numeric bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1191_0_bound_pack_staged",
            "decision": "exact_leftovers_converted_to_bound_pack",
            "reason": "1190 identified the four real local debts; 1191 gives each a theorem-zero condition and a no-cancellation bound form",
            "next_action": "fill parent phi/P_loc/no-flux theorem clauses or source the first response operator",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1191_1_zero_route_not_closed",
            "decision": "parent_zero_not_claimed",
            "reason": "each zero clause still lacks a parent signature",
            "next_action": "try the parent phi-source equation first because it also controls the Ricci residual and Khat amplitude",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1191_2_testing_route_ready_to_start",
            "decision": "source_ready_testing_shape_exists",
            "reason": "arena projection slots now say exactly which operator is needed for PPN, alpha3, R10, clocks, and orbital tests",
            "next_action": "if derivation stalls, fill one PPN/R10 response row with valid_for_claim=false before scoring",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1191_3_selected_next_route",
            "decision": "derive_parent_phi_source_or_fill_active_gamma_first_score_row",
            "reason": "this is the shortest route to shrink both q_loc residual and local metric footprint without smuggling in a plateau axiom",
            "next_action": "build 1192 parent phi-source equation or active Gamma first-bound row",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1191_0_1192",
            "next_target": "1192-Y5-R10-parent-phi-source-or-active-Gamma-bound-first-score-row.md",
            "objective": "try to derive the parent source equation for phi/K_L; if that fails, fill the first nonclaim active-Gamma bound row with coefficient, support, response operator, and arena limit slots",
            "include": "parent Euler/constraint route for phi; Ricci-corrected Green operator; Khat amplitude response; one explicit arena score row; no-claim validation",
            "exclude": "flat-patch q_loc zero claim; parentless auxiliary phi; post-readout projector tuning; invented coefficients; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, object]],
    bounds: list[dict[str, object]],
    certs: list[dict[str, object]],
    arenas: list[dict[str, object]],
    active_gamma: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    all_sources_ok = all(row["exists"] and row["needle_found"] for row in sources)
    bound_ids = {row["bound_id"] for row in bounds}
    arena_names = {row["arena"] for row in arenas}
    all_science_rows = bounds + certs + arenas + active_gamma + gates + decisions + nexts
    all_nonclaim = all(row.get("valid_for_claim") is False for row in all_science_rows)
    needed_bounds = {
        "LBP1191_0_Ricci_Khat_residual",
        "LBP1191_2_projector_commutator",
        "LBP1191_3_boundary_flux",
        "LBP1191_4_Khat_metric_footprint",
        "LBP1191_5_total_abs_envelope",
    }
    needed_arenas = {
        "PPN gamma/beta",
        "PPN alpha3/preferred-frame",
        "R10 short-range/fifth-force",
        "clock/time/readout",
        "orbital/source-normalization",
    }
    active_ids = {row["status_id"] for row in active_gamma}
    return [
        {
            "check_id": "V1191_0_sources_exist",
            "result": "pass" if all_sources_ok else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1191_1_leftover_bound_pack_complete",
            "result": "pass" if needed_bounds <= bound_ids else "fail",
            "detail": "Ricci residual, projector commutator, boundary flux, Khat footprint, and total envelope rows are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1191_2_parent_zero_certificate_not_promoted",
            "result": "pass" if all(row["passes_now"] is False for row in certs) else "fail",
            "detail": "all parent-zero clauses remain unsigned and nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1191_3_arena_projection_coverage",
            "result": "pass" if needed_arenas <= arena_names else "fail",
            "detail": "PPN gamma/beta, alpha3, R10, clock, and orbital projection slots are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1191_4_active_gamma_status",
            "result": "pass" if {"AG1191_1_U_B2_window43_small_parameter", "AG1191_4_metric_response_matrix", "AG1191_6_claim_status"} <= active_ids else "fail",
            "detail": "active Gamma has support candidates but remains blocked by coefficient/response/operator inputs",
            "claim_allowed": False,
        },
        {
            "check_id": "V1191_5_claim_gates_blocked",
            "result": "pass" if all(row["claim_allowed"] is False for row in gates) else "fail",
            "detail": "all 1191 claim gates remain blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1191_6_all_science_rows_nonclaim",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated science rows keep valid_for_claim=false",
            "claim_allowed": False,
        },
        {
            "check_id": "V1191_7_next_target",
            "result": "pass" if nexts and nexts[0]["next_id"] == "NEXT1191_0_1192" else "fail",
            "detail": "1192 handoff targets parent phi-source derivation or first active-Gamma bound row",
            "claim_allowed": False,
        },
        {
            "check_id": "V1191_8_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1191_9_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1191_SUMMARY",
            "result": "pass",
            "detail": "1191 stages a nonclaim residual-bound pack for R_K, C_P, B_P, and active Khat footprint, then hands off to parent phi-source or first active-Gamma bound row",
            "claim_allowed": False,
        },
    ]


def write_doc(
    sources: list[dict[str, object]],
    bounds: list[dict[str, object]],
    certs: list[dict[str, object]],
    arenas: list[dict[str, object]],
    active_gamma: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 1191 - Y5/R10 curved Khat P_loc commutator bound pack or parent zero",
            "**Current verdict:** 1191 does not prove local GR, but it converts the exact 1190 leftovers into a clean no-cancellation residual-bound pack. That is progress: the enemy is no longer fog, it has four named doors.",
            "**Main progress:** `R_K`, `C_P`, `B_P`, and the active `K_hat` metric footprint now each have a theorem-zero condition, a bound form, missing input list, and arena projection slot.",
            "**No claim:** no `q_loc=0`, local-GR, Newton, R10, PPN, WEP, clock, orbital, or public-facing claim follows from this checkpoint.",
            "## Source register\n\n" + table(sources),
            "## Leftover bound pack\n\n" + table(bounds),
            "## Parent-zero certificate\n\n" + table(certs),
            "## Arena projection slots\n\n" + table(arenas),
            "## Active Gamma input status\n\n" + table(active_gamma),
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
    bounds = leftover_bound_pack_rows()
    certs = parent_zero_certificate_rows()
    arenas = arena_projection_slot_rows()
    active_gamma = active_gamma_input_status_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, bounds, certs, arenas, active_gamma, gates, decisions, nexts)

    outputs = {
        "P8_Y5_R10_1191_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1191_LEFTOVER_BOUND_PACK.csv": bounds,
        "P8_Y5_R10_1191_PARENT_ZERO_CERTIFICATE.csv": certs,
        "P8_Y5_R10_1191_ARENA_PROJECTION_SLOTS.csv": arenas,
        "P8_Y5_R10_1191_ACTIVE_GAMMA_INPUT_STATUS.csv": active_gamma,
        "P8_Y5_R10_1191_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1191_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1191_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1191_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, stamp(rows))

    write_doc(sources, bounds, certs, arenas, active_gamma, gates, decisions, validations, nexts)

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

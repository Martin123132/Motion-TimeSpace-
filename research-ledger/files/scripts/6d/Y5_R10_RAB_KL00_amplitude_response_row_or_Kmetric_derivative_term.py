from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1288"
TITLE = "1288-Y5-R10-RAB-KL00-amplitude-response-row-or-Kmetric-derivative-term"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
KL00_AMPLITUDE_PATH = OUT_DIR / f"{PACK_ID}_KL00_AMPLITUDE_RESPONSE_ROW_NONCLAIM.csv"
RESPONSE_REQUIREMENTS_PATH = OUT_DIR / f"{PACK_ID}_RESPONSE_MATRIX_REQUIREMENTS.csv"
KMETRIC_BLOCKER_PATH = OUT_DIR / f"{PACK_ID}_KMETRIC_DERIVATIVE_TERM_BLOCKER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1288_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        KL00_AMPLITUDE_PATH,
        RESPONSE_REQUIREMENTS_PATH,
        KMETRIC_BLOCKER_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1288_0_1287_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1287_NEXT_TARGET.csv",
            "needle": "NEXT1287_0_1288",
            "role": "handoff into KL00 amplitude/response row or Kmetric derivative term",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1288_1_1287_KL00",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1287_FIRST_KHAT_COMPONENT_ROW_NONCLAIM.csv",
            "needle": "KTC1287_0_flat_Ricci_scalar_KL00",
            "role": "filled formal K_L^{00} component row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1288_2_1287_Kmetric_volume",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1287_FIRST_KMETRIC_VOLUME_ROW_NONCLAIM.csv",
            "needle": "KMC1287_0_volume_metric_response",
            "role": "existing Kmetric volume subpiece",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1288_3_1287_DeltaK_status",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1287_DELTAK_COMPONENT_STATUS_LEDGER.csv",
            "needle": "DKS1287_2_component_comparison",
            "role": "Delta_K^{00} still not computable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1288_4_796_amplitude_budget",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_796_KL_AMPLITUDE_PPN_BUDGET.csv",
            "needle": "KLB796_2_Newton_source_fraction",
            "role": "Newton source fraction epsilon_K formula",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1288_5_1194_KL_bound",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1194_EINSTEIN_SCALAR_BOUND_FORMS.csv",
            "needle": "ESB1194_2_KL_amplitude_bound",
            "role": "Einstein/Ricci-flat scalar branch K_L amplitude bound form",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1288_6_835_active_gamma_inputs",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_835_ACTIVE_GAMMA_INPUT_SCHEMA.csv",
            "needle": "K00_projection_fraction",
            "role": "missing projection, matter scale, response, and observable-limit inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1288_7_794_PPN_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_794_PPN_BOUND_REQUIREMENTS.csv",
            "needle": "PBR794_0_PPN_metric",
            "role": "PPN/Newton/orbital/clock/R10 bound requirements",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1288_8_1194_DT_response_slots",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1194_DT_COMPENSATOR_RESPONSE_ROWS.csv",
            "needle": "DTR1194_5_first_response_verdict",
            "role": "local response slots showing analogous missing response matrices",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    kl00_amplitude = [
        {
            "row_id": "KAR1288_0_KL00_Newton_source_fraction",
            "residual_component": "epsilon_K00",
            "source_component": "K_L^{00}",
            "amplitude_proxy": "Kbar_L,loc,00",
            "newton_budget_formula": "epsilon_K00=abs(c^2 Kbar_L,loc,00)/abs(4 pi G rho)",
            "bound_form": "||K_L||_D <= C_K,H_E,D ||Gamma_act||_D + B_K + R_Lambda",
            "units": "dimensionless_if_Kbar_L_loc_00_and_4piG_rho_cminus2_share_Lminus2_units",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_796_KL_AMPLITUDE_PPN_BUDGET.csv;source-intake/mts_residuals/P8_Y5_R10_1194_EINSTEIN_SCALAR_BOUND_FORMS.csv",
            "source_anchor": "KLB796_2_Newton_source_fraction;ESB1194_2_KL_amplitude_bound",
            "needed_values": "MISSING_KBAR_L_LOC_00;MISSING_RHO_MODEL;MISSING_C_K_HE_D;MISSING_GAMMA_ACT_NORM;MISSING_BOUNDARY_MODE;MISSING_RESPONSE_LIMIT",
            "current_status": "SYMBOLIC_AMPLITUDE_ROW_NOT_SCOREABLE",
            "maps_to_tests": "Newton;PPN;orbital;clock;R10;WEP_readout",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "KAR1288_1_KL_norm_Einstein_scalar_bound",
            "residual_component": "||K_L||_D",
            "source_component": "tracefree_longitudinal_scalar_branch",
            "amplitude_proxy": "C_K,H_E,D ||Gamma_act||_D + B_K + R_Lambda",
            "newton_budget_formula": "epsilon_K00 <= abs(c^2 K00_projection_fraction ||K_L||_D)/abs(4 pi G rho)",
            "bound_form": "requires K00_projection_fraction and matter_curvature_norm from active-gamma schema",
            "units": "L^-2_for_KL_norm_if_Gamma_act_L^-2",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1194_EINSTEIN_SCALAR_BOUND_FORMS.csv;source-intake/mts_residuals/P8_Y5_R10_835_ACTIVE_GAMMA_INPUT_SCHEMA.csv",
            "source_anchor": "ESB1194_2_KL_amplitude_bound;K00_projection_fraction;matter_curvature_norm",
            "needed_values": "MISSING_K00_PROJECTION_FRACTION;MISSING_MATTER_CURVATURE_NORM;MISSING_GAMMA_SUPPORT_LAW;MISSING_BOUNDARY_REMAINDER",
            "current_status": "BOUND_FORM_ONLY_NONCLAIM",
            "maps_to_tests": "Newton;PPN;clock;orbital",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "KAR1288_2_no_free_lunch_guard",
            "residual_component": "q_loc_cancellation_not_metric_silence",
            "source_component": "partial_mu K_L^{mu nu}=partial^nu Gamma_eff branch",
            "amplitude_proxy": "K_L~Gamma_eff up to boundary and curvature constants",
            "newton_budget_formula": "no numeric epsilon_K00 until amplitude and response rows exist",
            "bound_form": "K_L must be theorem-zero, metric-invisible, or below local residual tolerances",
            "units": "logic_guard",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_796_KL_AMPLITUDE_PPN_BUDGET.csv",
            "source_anchor": "KLB796_0_divergence_zero_not_metric_zero;KLB796_1_elliptic_scale_estimate;KLB796_5_acceptance_condition",
            "needed_values": "MISSING_METRIC_INVISIBILITY_THEOREM;MISSING_RESPONSE_BOUNDS;MISSING_KPERP_BOUNDARY_GUARD",
            "current_status": "NO_FREE_LUNCH_RETAINED",
            "maps_to_tests": "local_GR;PPN;Newton;R10",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    response_requirements = [
        {
            "req_id": "RMR1288_0_Newton_source",
            "arena": "Newton/source normalization",
            "observable_vector": "epsilon_K00",
            "source_object": "K_L^{00}",
            "required_coefficient_or_operator": "K00_projection_fraction plus matter_curvature_norm",
            "prediction_form": "epsilon_K00=abs(c^2 Kbar_L,loc,00)/abs(4 pi G rho)",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_796_KL_AMPLITUDE_PPN_BUDGET.csv;source-intake/mts_residuals/P8_Y5_R10_835_ACTIVE_GAMMA_INPUT_SCHEMA.csv",
            "source_anchor": "KLB796_2_Newton_source_fraction;K00_projection_fraction;matter_curvature_norm",
            "current_status": "MISSING_KBAR_L_LOC_00_AND_SOURCE_MODEL",
            "missing_inputs": "MISSING_KBAR_L_LOC_00;MISSING_RHO_MODEL;MISSING_MEASURED_GM_CALIBRATION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "req_id": "RMR1288_1_PPN_gamma_beta",
            "arena": "PPN gamma/beta",
            "observable_vector": "delta_gamma_K,delta_beta_K",
            "source_object": "weak-field metric response to K_L",
            "required_coefficient_or_operator": "R_PPN_gamma_beta[K_L]",
            "prediction_form": "Delta_PPN_K <= R_PPN_gamma_beta[K_L] ||K_L||_D",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_796_KL_AMPLITUDE_PPN_BUDGET.csv;source-intake/mts_residuals/P8_Y5_R10_794_PPN_BOUND_REQUIREMENTS.csv",
            "source_anchor": "KLB796_3_PPN_response_matrix;PBR794_0_PPN_metric",
            "current_status": "MISSING_RESPONSE_MATRIX",
            "missing_inputs": "MISSING_R_PPN_GAMMA;MISSING_R_PPN_BETA;MISSING_LIMIT_ROWS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "req_id": "RMR1288_2_PPN_preferred_frame",
            "arena": "PPN preferred-frame/preferred-location",
            "observable_vector": "alpha_i_K,xi_K",
            "source_object": "anisotropic/time-dependent K_L,Kperp,boundary modes",
            "required_coefficient_or_operator": "R_alpha_xi[K_L,Kperp,boundary]",
            "prediction_form": "alpha_i_K,xi_K <= R_alpha_xi ||K_L,Kperp,boundary||",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_796_KL_AMPLITUDE_PPN_BUDGET.csv;source-intake/mts_residuals/P8_Y5_R10_794_PPN_BOUND_REQUIREMENTS.csv",
            "source_anchor": "KLB796_3_PPN_response_matrix;PBR794_0_PPN_metric",
            "current_status": "MISSING_PREFERRED_FRAME_RESPONSE",
            "missing_inputs": "MISSING_ALPHA_I_PROJECTOR;MISSING_XI_PROJECTOR;MISSING_BOUNDARY_MODE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "req_id": "RMR1288_3_clock_readout",
            "arena": "clock/redshift",
            "observable_vector": "delta_clock_K",
            "source_object": "coframe/metric readout of K_L carrier",
            "required_coefficient_or_operator": "R_clock[K_L]",
            "prediction_form": "delta_clock_K <= R_clock ||K_L||_D",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_794_PPN_BOUND_REQUIREMENTS.csv;source-intake/mts_residuals/P8_Y5_R10_1194_DT_COMPENSATOR_RESPONSE_ROWS.csv",
            "source_anchor": "PBR794_3_clock_R10;DTR1194_3_clock_orbital_slot",
            "current_status": "MISSING_CLOCK_READOUT_COEFFICIENTS",
            "missing_inputs": "MISSING_R_CLOCK;MISSING_CLOCK_LIMIT_ROW;MISSING_DOMAIN_PROFILE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "req_id": "RMR1288_4_orbital_projection",
            "arena": "orbital dynamics",
            "observable_vector": "a_extra_K",
            "source_object": "extra acceleration sourced by K_L or Kperp",
            "required_coefficient_or_operator": "R_orbital[K_L,Kperp]",
            "prediction_form": "a_extra_K <= R_orbital ||K_L,Kperp||_D",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_794_PPN_BOUND_REQUIREMENTS.csv;source-intake/mts_residuals/P8_Y5_R10_1194_DT_COMPENSATOR_RESPONSE_ROWS.csv",
            "source_anchor": "PBR794_2_orbital;DTR1194_3_clock_orbital_slot",
            "current_status": "MISSING_ORBITAL_FORCE_KERNEL",
            "missing_inputs": "MISSING_R_ORBITAL;MISSING_PLANETARY_LUNAR_BINARY_LIMITS;MISSING_SOURCE_NORMALIZATION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "req_id": "RMR1288_5_R10_short_range",
            "arena": "R10 short-range/fifth-force",
            "observable_vector": "alpha_K(lambda)",
            "source_object": "finite-range projection of K_L carrier",
            "required_coefficient_or_operator": "R_R10(lambda)[K_L]",
            "prediction_form": "alpha_K(lambda)=R_R10(lambda) ||K_L||_D compared with real alpha_bound(lambda)",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_794_PPN_BOUND_REQUIREMENTS.csv;source-intake/mts_residuals/P8_Y5_R10_1194_DT_COMPENSATOR_RESPONSE_ROWS.csv",
            "source_anchor": "PBR794_3_clock_R10;DTR1194_2_R10_alpha_lambda_slot",
            "current_status": "MISSING_R10_PROJECTION",
            "missing_inputs": "MISSING_R_R10_LAMBDA;MISSING_RANGE_PROFILE;MISSING_REAL_ALPHA_BOUND_CURVE;MISSING_SOURCE_NORMALIZATION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "req_id": "RMR1288_6_WEP_readout",
            "arena": "WEP/matter descent",
            "observable_vector": "eta_AB_K",
            "source_object": "matter coupling/readout of K_L or compensator variables",
            "required_coefficient_or_operator": "R_WEP species-charge vector or descent theorem",
            "prediction_form": "eta_AB_K=0 if matter descends through same observed coframe, otherwise eta_AB_K <= R_WEP charge_vector",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1194_DT_COMPENSATOR_RESPONSE_ROWS.csv",
            "source_anchor": "DTR1194_4_WEP_matter_descent_slot",
            "current_status": "MISSING_MATTER_DESCENT_PROOF",
            "missing_inputs": "MISSING_SPECIES_CHARGE_VECTOR;MISSING_MICROSCOPE_BOUND_ROW;MISSING_COFAME_DESCENT_THEOREM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "req_id": "RMR1288_7_response_verdict",
            "arena": "all_local",
            "observable_vector": "Newton,PPN,clock,orbital,R10,WEP",
            "source_object": "K_L^{00} amplitude-response branch",
            "required_coefficient_or_operator": "full local response matrix",
            "prediction_form": "no arena is scoreable until response operators and observable limits are sourced",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_796_KL_AMPLITUDE_PPN_BUDGET.csv",
            "source_anchor": "KLB796_5_acceptance_condition",
            "current_status": "NONCLAIM_TEMPLATE_ONLY",
            "missing_inputs": "MISSING_FULL_RESPONSE_MATRIX;MISSING_LOCAL_BOUND_ROWS;MISSING_KPERP_BOUNDARY_GUARD",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    kmetric_blockers = [
        {
            "blocker_id": "KMR1288_0_volume_piece_available",
            "target": "Kmetric_volume^{mu nu}",
            "needed_term": "metric-proportional volume response",
            "formula_or_requirement": "delta sqrt(-g) Gamma_eff supplies Gamma_eff g^{mu nu} up to sign/convention",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1287_FIRST_KMETRIC_VOLUME_ROW_NONCLAIM.csv",
            "source_anchor": "KMC1287_0_volume_metric_response",
            "current_status": "SUBPIECE_EXISTS_NONCLAIM",
            "why_not_enough": "full Kmetric needs derivative, metric-dependence, boundary/reference, and current-Khat comparison terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "KMR1288_1_Gamma_metric_dependence",
            "target": "delta Gamma_eff / delta g_{mu nu}",
            "needed_term": "metric dependence of Gamma_eff=L_cg^-2 F(m)",
            "formula_or_requirement": "delta Gamma_eff = L_cg^-2 F'(m) delta m - 2 L_cg^-3 F(m) delta L_cg plus connection/domain terms",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1286_FIRST_RESPONSE_FIELD_COMPONENT_ROW_NONCLAIM.csv",
            "source_anchor": "RFR1286_0_Gamma_memory_scalar_projection",
            "current_status": "MISSING_METRIC_VARIATION_OF_m_AND_L_cg",
            "why_not_enough": "m, L_cg, and F do not yet have parent-signed metric-variation laws",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "KMR1288_2_derivative_terms",
            "target": "Kmetric_derivative^{00}",
            "needed_term": "connection and derivative variation terms after integration by parts",
            "formula_or_requirement": "compute all derivative terms in delta(S_Gamma)/delta g_{00} beyond the volume piece",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1287_FIRST_KMETRIC_VOLUME_ROW_NONCLAIM.csv",
            "source_anchor": "KMC1287_0_volume_metric_response",
            "current_status": "MISSING_DERIVATIVE_TERMS",
            "why_not_enough": "the source only gives the volume subpiece, not the derivative expansion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "KMR1288_3_boundary_reference_terms",
            "target": "Kmetric_boundary^{00}",
            "needed_term": "boundary/no-flux/reference terms",
            "formula_or_requirement": "fix boundary conditions and reference subtraction before turning Kmetric into a local observable component",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1287_DELTAK_COMPONENT_STATUS_LEDGER.csv",
            "source_anchor": "DKS1287_1_Kmetric_subpiece_exists",
            "current_status": "MISSING_BOUNDARY_REFERENCE_TERMS",
            "why_not_enough": "Kmetric volume-only comparison would be gauge/domain incomplete",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "KMR1288_4_GAB_doublet_metric",
            "target": "response-doublet metric dependence",
            "needed_term": "G_AB or equivalent response metric if the doublet route is used",
            "formula_or_requirement": "derive whether G_AB contributes to Kmetric or is fixed/background in the branch",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_835_ACTIVE_GAMMA_INPUT_SCHEMA.csv",
            "source_anchor": "metric_response_coeff",
            "current_status": "MISSING_G_AB_OR_RESPONSE_METRIC_DEPENDENCE",
            "why_not_enough": "without this, Kmetric is not the metric variation of the actual active response object",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "KMR1288_5_current_Khat_match",
            "target": "Delta_K^{00}=K_hat^{00}-Kmetric^{00}",
            "needed_term": "current-MTS Khat match to K_L^{00}",
            "formula_or_requirement": "prove K_hat^{00}=K_L^{00} in the parent/current branch or record a separate compensator current",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1287_DELTAK_COMPONENT_STATUS_LEDGER.csv",
            "source_anchor": "DKS1287_2_component_comparison",
            "current_status": "MISSING_CURRENT_KHAT_MATCH",
            "why_not_enough": "formal K_L candidate is not yet the sourced current-MTS K_hat",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "blocker_id": "KMR1288_6_full_Kmetric_verdict",
            "target": "Kmetric^{00}",
            "needed_term": "full component computation",
            "formula_or_requirement": "volume + metric-dependence + derivative + boundary/reference + readout conventions",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1287_FIRST_KMETRIC_VOLUME_ROW_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_1287_DELTAK_COMPONENT_STATUS_LEDGER.csv",
            "source_anchor": "KMC1287_0_volume_metric_response;DKS1287_2_component_comparison",
            "current_status": "FULL_KMETRIC_00_NOT_COMPUTABLE_YET",
            "why_not_enough": "Delta_K^{00} and local-GR claims stay blocked until every Kmetric term and current-Khat comparison is filled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1288_0_sources_exist",
            "claim": "internal source provenance",
            "current_status": "SATISFIED_FOR_PRIVATE_CHECKPOINT",
            "reason": "all registered source paths and anchors are checked before validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1288_1_KL00_numeric_amplitude",
            "claim": "KL00 Newton amplitude can be scored",
            "current_status": "BLOCKED_MISSING_NUMERIC_AMPLITUDE",
            "reason": "Kbar_L,loc,00, rho model, CK bound, Gamma norm, and boundary mode are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1288_2_response_matrix",
            "claim": "PPN/clock/orbital/R10/WEP response can be scored",
            "current_status": "BLOCKED_MISSING_RESPONSE_MATRIX",
            "reason": "no sourced R_PPN, R_clock, R_orbital, R_R10, or WEP readout coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1288_3_full_Kmetric",
            "claim": "Kmetric^{00} computed",
            "current_status": "BLOCKED_VOLUME_SUBPIECE_ONLY",
            "reason": "derivative, metric-dependence, boundary/reference, and response-metric terms remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1288_4_DeltaK_component",
            "claim": "Delta_K^{00} computable",
            "current_status": "BLOCKED_MISSING_KHAT_KMETRIC_COMPARISON",
            "reason": "current-MTS Khat match and full Kmetric^{00} are still unavailable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1288_5_local_GR_PPN",
            "claim": "local GR or PPN pass",
            "current_status": "BLOCKED_NONCLAIM",
            "reason": "q_loc cancellation and a symbolic amplitude row do not prove metric silence or observational safety",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1288_0_first_amplitude_row",
            "decision": "stage the first KL00 amplitude-response row",
            "because": "1287 supplied K_L^{00}; 796 and 1194 supply the Newton fraction and amplitude-bound forms",
            "next_action": "source or derive the first response coefficient instead of claiming local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1288_1_no_local_claim",
            "decision": "keep local recovery blocked",
            "because": "the amplitude row contains MISSING inputs and the response matrix is absent",
            "next_action": "fill R_PPN/R_Newton/R_clock/R_orbital/R_R10 or expand Kmetric derivatives",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1288_2_Kmetric_route",
            "decision": "retain Kmetric derivative expansion as the parallel route",
            "because": "the volume term exists but derivative/domain/boundary terms still control Delta_K^{00}",
            "next_action": "derive delta Gamma_eff / delta g_{00} for Gamma_eff=L_cg^-2 F(m)",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1288_3_status_plain_english",
            "decision": "tensor side now has a component and a budget row but not a score",
            "because": "K_L^{00} is formal and source-backed, but amplitude and readout coefficients are not numeric",
            "next_action": "next checkpoint should obtain a response matrix source or compute a Kmetric derivative term",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1288_0_1289",
            "target_file": "1289-Y5-R10-RAB-KL00-response-matrix-source-or-Kmetric-derivative-expansion.md",
            "target_script": "scripts/Y5_R10_RAB_KL00_response_matrix_source_or_Kmetric_derivative_expansion.py",
            "task": "source the first local response coefficient for K_L^{00}, or expand the first Kmetric derivative term for Gamma_eff=L_cg^-2 F(m)",
            "success_condition": "one response-matrix row becomes source-backed and still nonclaim, or a concrete Kmetric derivative/domain term is written with blockers separated",
            "do_not": "do not promote q_loc cancellation, KL00 amplitude templates, or volume-only Kmetric rows into local GR/PPN claims",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(KL00_AMPLITUDE_PATH, kl00_amplitude)
    write_csv(RESPONSE_REQUIREMENTS_PATH, response_requirements)
    write_csv(KMETRIC_BLOCKER_PATH, kmetric_blockers)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1288_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    amplitude_row = next(row for row in kl00_amplitude if row["row_id"] == "KAR1288_0_KL00_Newton_source_fraction")
    validations.append(
        validation_row(
            "VAL1288_1_KL00_amplitude_row_nonclaim",
            "KL00 Newton amplitude row exists, contains MISSING markers, and remains nonclaim",
            "MISSING_" in amplitude_row["needed_values"]
            and amplitude_row["current_status"] == "SYMBOLIC_AMPLITUDE_ROW_NOT_SCOREABLE"
            and is_false(amplitude_row["valid_for_claim"])
            and is_false(amplitude_row["claim_allowed"]),
            "KAR1288_0_KL00_Newton_source_fraction",
        )
    )
    validations.append(
        validation_row(
            "VAL1288_2_response_matrix_requirements_blocked",
            "all response matrix rows are blocked/nonclaim",
            all(is_false(row["valid_for_claim"]) and is_false(row["claim_allowed"]) for row in response_requirements)
            and any("MISSING" in row["current_status"] for row in response_requirements),
            f"response_requirement_rows={len(response_requirements)}",
        )
    )
    kmetric_verdict = next(row for row in kmetric_blockers if row["blocker_id"] == "KMR1288_6_full_Kmetric_verdict")
    validations.append(
        validation_row(
            "VAL1288_3_Kmetric_derivative_blocked",
            "Kmetric derivative/full component route is explicitly blocked",
            kmetric_verdict["current_status"] == "FULL_KMETRIC_00_NOT_COMPUTABLE_YET"
            and is_false(kmetric_verdict["claim_allowed"]),
            "KMR1288_6_full_Kmetric_verdict",
        )
    )
    validations.append(
        validation_row(
            "VAL1288_4_claim_gates_blocked",
            "claim gates prevent local GR/PPN promotion",
            all(is_false(row["claim_allowed"]) for row in claim_gates)
            and any("BLOCKED" in row["current_status"] for row in claim_gates),
            f"claim_gate_rows={len(claim_gates)}",
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        KL00_AMPLITUDE_PATH,
        RESPONSE_REQUIREMENTS_PATH,
        KMETRIC_BLOCKER_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    parse_ok = True
    parse_details: list[str] = []
    for table_path in generated_tables:
        try:
            parse_details.append(f"{table_path.name}:{len(read_csv(table_path))}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{table_path.name}:ERROR:{exc}")
    validations.append(validation_row("VAL1288_5_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1288_6_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1288_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, kl00_amplitude, response_requirements, kmetric_blockers, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1288_8_next_target_1289",
            "next target routes to response matrix source or Kmetric derivative expansion",
            next_target[0]["next_id"] == "NEXT1288_0_1289" and "response" in next_target[0]["task"],
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1288_9_overall",
            "overall 1288 validation",
            overall_pass,
            "1288 stages a source-backed nonclaim KL00 amplitude-response row, blocks response-matrix and Kmetric-derivative claims, and routes to 1289",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1288 Y5 R10 RAB KL00 amplitude-response row or Kmetric derivative term

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1288 stages the first source-backed **nonclaim** `K_L^{{00}}` amplitude-response row. The useful Newton budget is now explicit as `epsilon_K00=abs(c^2 Kbar_L,loc,00)/abs(4 pi G rho)`, but it is not scoreable because the actual local amplitude, matter model, response coefficients, and observable limits are still missing.

**Main progress:** the branch has moved from “tensor component exists” to “tensor component has a local budget row.” This is the right engineering move: `q_loc` cancellation is no longer allowed to hide the metric-amplitude problem. The row makes the missing inputs visible instead of pretending the cancellation is local GR.

**Next derivation target:** source the first response coefficient for `K_L^{{00}}`, or expand the first real derivative/domain/boundary term in `Kmetric[Gamma_eff]` for `Gamma_eff=L_cg^-2 F(m)`.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## KL00 Amplitude Response Rows

{markdown_table(kl00_amplitude, ["row_id", "residual_component", "source_component", "amplitude_proxy", "newton_budget_formula", "bound_form", "units", "source_path", "source_anchor", "needed_values", "current_status", "maps_to_tests", "valid_for_claim", "claim_allowed"])}

## Response Matrix Requirements

{markdown_table(response_requirements, ["req_id", "arena", "observable_vector", "source_object", "required_coefficient_or_operator", "prediction_form", "source_path", "source_anchor", "current_status", "missing_inputs", "valid_for_claim", "claim_allowed"])}

## Kmetric Derivative Term Blockers

{markdown_table(kmetric_blockers, ["blocker_id", "target", "needed_term", "formula_or_requirement", "source_path", "source_anchor", "current_status", "why_not_enough", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "claim", "current_status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()

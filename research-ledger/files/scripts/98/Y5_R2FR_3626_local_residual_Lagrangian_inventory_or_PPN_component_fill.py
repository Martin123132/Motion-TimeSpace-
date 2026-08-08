from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3626"
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_RESIDUAL_LAGRANGIAN_INVENTORY_OR_PPN_COMPONENT_FILL_3626"
DOC = ROOT / "3626-Y5-R2FR-local-residual-Lagrangian-inventory-or-PPN-component-fill.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8", errors="replace")


def output_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3626_SOURCE_REGISTER.csv",
        "inventory": RESIDUALS / "P8_Y5_R2FR_3626_LOCAL_RESIDUAL_LAGRANGIAN_INVENTORY.csv",
        "euler_map": RESIDUALS / "P8_Y5_R2FR_3626_EULER_VARIATION_CLOSURE_MAP.csv",
        "component_rows": RESIDUALS / "P8_Y5_R2FR_3626_PPN_COMPONENT_FILL_ROWS.csv",
        "scorecard": RESIDUALS / "P8_Y5_R2FR_3626_OWNERSHIP_SCORECARD.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3626_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3626_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3626_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_local_residual_Lagrangian_inventory_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3626_VALIDATION.csv",
    }


def source_map() -> list[dict[str, str]]:
    return [
        {
            "source_id": "handoff_3625",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3625_NEXT_TARGET.csv"),
            "needle": "local-residual-Lagrangian-inventory",
            "role": "3625 selected local residual Lagrangian inventory or component fill.",
        },
        {
            "source_id": "closure_audit_3625",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3625_RESIDUAL_CLOSURE_AUDIT.csv"),
            "needle": "RCA3625_6_Delta_PPN_abs",
            "role": "residual closure audit to inventory.",
        },
        {
            "source_id": "ppn_schema_3625",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3625_PPN_NEWTON_ENVELOPE_SCHEMA.csv"),
            "needle": "ENV3625_6_total",
            "role": "PPN/Newton fallback envelope schema.",
        },
        {
            "source_id": "residual_vector_3624",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3624_EXPLICIT_MTS_RESIDUAL_VECTOR.csv"),
            "needle": "RV3624_6_PPN_total",
            "role": "canonical live residual vector.",
        },
        {
            "source_id": "min_parent_action_511",
            "path": str(RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv"),
            "needle": "A511_6_metric_readout",
            "role": "minimum local-GR parent action blocks.",
        },
        {
            "source_id": "min_parent_residual_511",
            "path": str(RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_RESIDUAL_VECTOR.csv"),
            "needle": "AR511_8_transition_switching",
            "role": "prior residual vector and repair list.",
        },
        {
            "source_id": "gk_first_variation",
            "path": str(RESIDUALS / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv"),
            "needle": "GK513_0_action_existence",
            "role": "Gamma/Khat/q_loc action-existence and Helmholtz contract.",
        },
        {
            "source_id": "gk_action_candidates",
            "path": str(RESIDUALS / "P8_GK_STRESS_ACTION_CANDIDATES.csv"),
            "needle": "GK514_A_metric_response_scalar_density",
            "role": "candidate S_GK action families.",
        },
        {
            "source_id": "response_doublet",
            "path": str(RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"),
            "needle": "RD516_5_PPN_lock",
            "role": "response-doublet repair route for q_loc/local leakage.",
        },
        {
            "source_id": "pim_projector",
            "path": str(RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv"),
            "needle": "PM8_retained_residual_fallback",
            "role": "Pi_M projector/source-measure algebra and fallback.",
        },
        {
            "source_id": "source_current",
            "path": str(RESIDUALS / "P8_source_current_Ward_universality_CONTRACT.csv"),
            "needle": "SC8_second_order_source_stability",
            "role": "ordinary matter/source Hilbert current owner contract.",
        },
        {
            "source_id": "domain_selector",
            "path": str(RESIDUALS / "P8_DOMAIN_SELECTOR_PARENT_ACTION_CLAUSE.csv"),
            "needle": "C5_R11_silence",
            "role": "domain/projector parent action clause.",
        },
        {
            "source_id": "ellJ_law",
            "path": str(RESIDUALS / "P8_EM_ellJ_source_current_owner_residual_law.csv"),
            "needle": "EJR3513_0_total",
            "role": "source-current normalization residual decomposition.",
        },
        {
            "source_id": "pim_htau_law",
            "path": str(RESIDUALS / "P8_EM_PiM_Htau_commutator_residual_law.csv"),
            "needle": "PHCR3514_0_total",
            "role": "Pi_M/H_tau commutator denominator obstruction.",
        },
        {
            "source_id": "em_poynting",
            "path": str(RESIDUALS / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv"),
            "needle": "EMF3502_0_minimal_bound_field_stress",
            "role": "EM stress/Poynting/source residual components.",
        },
        {
            "source_id": "r11_source_minimum",
            "path": str(RESIDUALS / "P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv"),
            "needle": "R11SN_0_radial_Meff_hair",
            "role": "minimum source-normalization component rows.",
        },
        {
            "source_id": "source_measure_flux",
            "path": str(RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv"),
            "needle": "T509_2_no_extra_mass_channel",
            "role": "source-measure/mass-flux theorem and no-cheat clause.",
        },
    ]


def source_register_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    rows: list[dict[str, object]] = []
    for item in source_map():
        path = Path(item["path"])
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                **item,
                "exists": path.exists(),
                "needle_found": path.exists() and contains(path, item["needle"]),
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def inventory_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "inventory_id": "INV3626_0_DeltaE",
            "rv3624_id": "RV3624_0_DeltaE",
            "residual_symbol": "DeltaE_MTS_mn",
            "candidate_owner": "S_EH plus retained S_GK, S_selector, S_boundary, S_readout variations",
            "candidate_lagrangian_or_clause": "S_local=(2*kappa)^-1 int sqrt(-g)R + S_GK[g,Phi] + S_selector + S_boundary",
            "euler_owner": "metric Euler equation plus extra-field Euler equations",
            "metric_variation_owner": "delta_g S_GK + delta_g S_selector + delta_g S_boundary",
            "current_status": "OWNER_DECOMPOSITION_AVAILABLE_NOT_SIGNED",
            "blocks": "EH dominance and retained residual coefficient map missing",
            "source_path": str(RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "inventory_id": "INV3626_1_source_weight",
            "rv3624_id": "RV3624_1_source_weight",
            "residual_symbol": "DeltaT_source; w_EM; kappa_J; delta_ellJ",
            "candidate_owner": "S_matter[e_obs,psi] + S_EM[g_obs,A,J] with same Hilbert/Noether source current",
            "candidate_lagrangian_or_clause": "T_H = -2/sqrt(-g) delta(S_matter+S_EM)/delta g; J_Q=delta S_matter/delta A_Q",
            "euler_owner": "matter/EM Ward identities and source-current descent",
            "metric_variation_owner": "Hilbert stress from same observed coframe/Hodge",
            "current_status": "CONDITIONAL_CURRENT_OWNER_NOT_SIGNED",
            "blocks": "Pi_M/H_tau denominator, source-only multipliers, and same-frame readout still unsigned",
            "source_path": str(RESIDUALS / "P8_source_current_Ward_universality_CONTRACT.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "inventory_id": "INV3626_2_coupling_drift",
            "rv3624_id": "RV3624_2_coupling_drift",
            "residual_symbol": "delta_kappa; b_alpha; lambda_F2",
            "candidate_owner": "topological kappa sector plus parent EM level/fibre metric and unique F_Q^2 domain",
            "candidate_lagrangian_or_clause": "S_kappa_top=int kappa_eff dA_3; S_EM=-Z_Q/4 int F_Q wedge *F_Q",
            "euler_owner": "d kappa_eff=0 and fixed Z_Q/Q_* or calibrated alpha with drift bounds",
            "metric_variation_owner": "constant coupling factors only; no local source-gradient term",
            "current_status": "PARTIAL_KAPPA_CANDIDATE_ALPHA_LEVEL_UNSIGNED",
            "blocks": "parent EM level/Q_* certificate missing; drift rows remain live",
            "source_path": str(RESIDUALS / "P8_Y5_R2FR_3623_COUPLING_SCALING_NO_GO.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "inventory_id": "INV3626_3_q_loc",
            "rv3624_id": "RV3624_3_q_loc",
            "residual_symbol": "q_loc^nu",
            "candidate_owner": "S_GK[g,Phi] or response-doublet action whose Ward identity yields q_loc",
            "candidate_lagrangian_or_clause": "S_GK=-int sqrt(-g) Gamma_eff or S_GK=int sqrt(-g)[-1/2 G_AB grad Phi^A grad Phi^B - V(Phi)]",
            "euler_owner": "nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A; q_loc=0 on compact vacuum if E_A=0 and boundary flux=0",
            "metric_variation_owner": "T_GK=-2/sqrt(-g) delta S_GK/delta g",
            "current_status": "ACTION_EXISTENCE_AND_HELMHOLTZ_NOT_PROVED",
            "blocks": "Gamma/Khat stress may be non-variational bookkeeping; PPN projection coefficients missing",
            "source_path": str(RESIDUALS / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "inventory_id": "INV3626_4_GK_stress",
            "rv3624_id": "RV3624_4_GK_stress",
            "residual_symbol": "T_GK_mn; T_tau/P_mn",
            "candidate_owner": "positive auxiliary/response-doublet sector or topological exact sector",
            "candidate_lagrangian_or_clause": "L_GK=-1/2 G_AB(Phi) grad Phi^A grad Phi^B - V(Phi) with Phi0 fixed point and positive Hessian",
            "euler_owner": "L_AB delta Phi^B=0 with source-free compact exterior and no boundary flux",
            "metric_variation_owner": "stress zero if Phi=Phi0, dV(Phi0)=0, C(Phi0)=dC(Phi0)=0, and first variation vanishes",
            "current_status": "CANDIDATE_NOT_MATCHED_TO_EXISTING_MTS_SYMBOLS",
            "blocks": "positive operator/no-hair and physical residual lock not derived",
            "source_path": str(RESIDUALS / "P8_GK_STRESS_ACTION_CANDIDATES.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "inventory_id": "INV3626_5_PiM_boundary",
            "rv3624_id": "RV3624_5_PiM_boundary",
            "residual_symbol": "delta_PiM; Phi_EM_boundary; Q_boundary",
            "candidate_owner": "parent boundary symplectic metric, fixed Pi_M, Hamiltonian H_tau, and fixed reference/boundary terms",
            "candidate_lagrangian_or_clause": "S_boundary=S_GHY+S_ref+S_exact/topological; delta(Pi_M J_H)=Pi_M delta J_H+(delta Pi_M)J_H",
            "euler_owner": "d(Pi_M J_H)=0 from Ward/Euler/topology plus no radiative/boundary flux",
            "metric_variation_owner": "projector/boundary variation included or proved fixed/topological",
            "current_status": "PROJECTOR_VARIATION_AND_DENOMINATOR_NOT_PARENT_DERIVED",
            "blocks": "source mass can still be laundered through Pi_M/H_tau/reference",
            "source_path": str(RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "inventory_id": "INV3626_6_PPN_total",
            "rv3624_id": "RV3624_6_PPN_total",
            "residual_symbol": "Delta_PPN_abs",
            "candidate_owner": "derived weak-field/readout solution from the full owned local action",
            "candidate_lagrangian_or_clause": "Delta_PPN_abs=sum_abs(gamma,beta,preferred-frame,conservation,source/readout projections)",
            "euler_owner": "all sector Euler equations plus second-order weak-field solution",
            "metric_variation_owner": "PPN projection of all retained metric/source residuals",
            "current_status": "AGGREGATE_SCHEMA_READY_COMPONENT_VALUES_MISSING",
            "blocks": "beta, preferred-frame, source, boundary, and q_loc projection coefficients missing",
            "source_path": str(RESIDUALS / "P8_Y5_R2FR_3625_PPN_NEWTON_ENVELOPE_SCHEMA.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def euler_map_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "map_id": "EVM3626_0_DeltaE_metric",
            "inventory_id": "INV3626_0_DeltaE",
            "variation_test": "delta_g S_parent produces EH plus named residual stresses",
            "needed_identity": "DeltaE_MTS_mn = -2/sqrt(-g) delta(S_GK+S_selector+S_boundary+S_readout)/delta g_mn",
            "current_result": "DECOMPOSITION_WRITTEN_NOT_SIGNED",
            "fallback_component": "ENV3625_0_gamma; ENV3625_1_beta; ENV3625_4_Newton_Poisson",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "map_id": "EVM3626_1_source_Ward",
            "inventory_id": "INV3626_1_source_weight",
            "variation_test": "matter/EM diffeomorphism and gauge Ward identities use one observed source current",
            "needed_identity": "nabla_m(T_matter+T_EM+DeltaT_source)^{mn}=0 and J_readout=J_Noether",
            "current_result": "WARD_STANDARD_CONDITIONAL_DENOMINATOR_UNSIGNED",
            "fallback_component": "ENV3625_4_Newton_Poisson; ENV3625_5_EM_source",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "map_id": "EVM3626_2_GK_Helmholtz",
            "inventory_id": "INV3626_3_q_loc",
            "variation_test": "candidate T_GK satisfies variational Helmholtz symmetry and Euler closure",
            "needed_identity": "delta(sqrt(-g)T_GK^{mn})/delta g_ab symmetric as second variation plus boundary",
            "current_result": "NOT_CHECKED_CURRENT_MTS",
            "fallback_component": "ENV3625_2_preferred_frame; ENV3625_3_conservation; ENV3625_0_gamma",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "map_id": "EVM3626_3_double_zero",
            "inventory_id": "INV3626_4_GK_stress",
            "variation_test": "local fixed point kills value and first variation of extra stress/source",
            "needed_identity": "T_GK(Phi0)=0; partial_A T_GK(Phi0)=0; Hessian positive after constraints",
            "current_result": "CANDIDATE_ONLY_SYMBOL_MATCH_MISSING",
            "fallback_component": "ENV3625_0_gamma; ENV3625_1_beta; ENV3625_2_preferred_frame",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "map_id": "EVM3626_4_PiM_boundary",
            "inventory_id": "INV3626_5_PiM_boundary",
            "variation_test": "Pi_M and boundary/reference variations are owned before measured-GM readout",
            "needed_identity": "d(Pi_M J_H)=0 and delta Pi_M stress/reference flux are zero, fixed, or explicit residuals",
            "current_result": "PROJECTOR_VARIATION_NOT_PARENT_DERIVED",
            "fallback_component": "ENV3625_4_Newton_Poisson; ENV3625_3_conservation; ENV3625_5_EM_source",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "map_id": "EVM3626_5_PPN_projection",
            "inventory_id": "INV3626_6_PPN_total",
            "variation_test": "owned action is solved to weak-field second order and projected into PPN/Newton components",
            "needed_identity": "Delta_PPN_abs=sum_abs(component projections) with every term zero-owned or source-bounded",
            "current_result": "SCHEMA_READY_VALUES_MISSING",
            "fallback_component": "ENV3625_6_total",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def ppn_component_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "component_id": "PCF3626_0_gamma",
            "envelope_id": "ENV3625_0_gamma",
            "inventory_owner": "INV3626_0_DeltaE;INV3626_3_q_loc;INV3626_4_GK_stress",
            "observable_component": "gamma_minus_1",
            "component_value": "MISSING_WEAK_FIELD_PROJECTION",
            "component_units": "dimensionless",
            "bound_value": "MISSING_SOURCE_BACKED_GAMMA_BOUND",
            "bound_source_path": "MISSING_SOURCE_PATH",
            "no_cancellation_rule": "abs(component) checked independently",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "component_id": "PCF3626_1_beta",
            "envelope_id": "ENV3625_1_beta",
            "inventory_owner": "INV3626_0_DeltaE;INV3626_1_source_weight;INV3626_6_PPN_total",
            "observable_component": "beta_minus_1",
            "component_value": "MISSING_SECOND_ORDER_FIELD_SOLUTION",
            "component_units": "dimensionless",
            "bound_value": "MISSING_SOURCE_BACKED_BETA_BOUND",
            "bound_source_path": "MISSING_SOURCE_PATH",
            "no_cancellation_rule": "source/operator/readout beta pieces absolute-summed",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "component_id": "PCF3626_2_preferred_frame",
            "envelope_id": "ENV3625_2_preferred_frame",
            "inventory_owner": "INV3626_3_q_loc;INV3626_4_GK_stress;INV3626_5_PiM_boundary",
            "observable_component": "alpha_i;xi",
            "component_value": "MISSING_QLOC_OR_COFRAME_PROJECTION",
            "component_units": "dimensionless_vector",
            "bound_value": "MISSING_SOURCE_BACKED_PREFERRED_FRAME_BOUNDS",
            "bound_source_path": "MISSING_SOURCE_PATH",
            "no_cancellation_rule": "alpha1, alpha2, alpha3, xi independently bounded",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "component_id": "PCF3626_3_conservation",
            "envelope_id": "ENV3625_3_conservation",
            "inventory_owner": "INV3626_0_DeltaE;INV3626_1_source_weight;INV3626_5_PiM_boundary",
            "observable_component": "C_B^nu;zeta_i",
            "component_value": "MISSING_C_B_PROJECTION",
            "component_units": "divergence_or_dimensionless_projection",
            "bound_value": "MISSING_SOURCE_BACKED_CONSERVATION_BOUND",
            "bound_source_path": "MISSING_SOURCE_PATH",
            "no_cancellation_rule": "C_B cannot be cancelled against unowned source terms",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "component_id": "PCF3626_4_Newton_source",
            "envelope_id": "ENV3625_4_Newton_Poisson",
            "inventory_owner": "INV3626_1_source_weight;INV3626_2_coupling_drift;INV3626_5_PiM_boundary",
            "observable_component": "delta_Newton_MTS",
            "component_value": "MISSING_SOURCE_MASS_CLOSURE",
            "component_units": "dimensionless_or_acceleration_profile",
            "bound_value": "MISSING_SOURCE_BACKED_NEWTON_GM_BOUND",
            "bound_source_path": "MISSING_SOURCE_PATH",
            "no_cancellation_rule": "measured GM cannot define the source mass it is meant to test",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "component_id": "PCF3626_5_EM_source",
            "envelope_id": "ENV3625_5_EM_source",
            "inventory_owner": "INV3626_1_source_weight;INV3626_5_PiM_boundary",
            "observable_component": "w_EM;Phi_EM_boundary",
            "component_value": "MISSING_EM_FRACTION_OR_FLUX_NORMALIZATION",
            "component_units": "dimensionless_or_flux_over_MH",
            "bound_value": "MISSING_SOURCE_BACKED_EM_SOURCE_BOUND",
            "bound_source_path": "MISSING_SOURCE_PATH",
            "no_cancellation_rule": "bound-field Hilbert stress and radiative flux are separated",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "component_id": "PCF3626_6_total",
            "envelope_id": "ENV3625_6_total",
            "inventory_owner": "INV3626_0..INV3626_6",
            "observable_component": "Delta_local_GR_total_abs",
            "component_value": "MISSING_COMPONENT_COMPLETE_VECTOR",
            "component_units": "declared_by_components",
            "bound_value": "MISSING_ALL_COMPONENT_BOUNDS",
            "bound_source_path": "MISSING_SOURCE_PATH",
            "no_cancellation_rule": "pass only if every component has theorem-zero or independent numeric bound pass",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def scorecard_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "score_id": "OSC3626_0_EH_matter_EM",
            "sector": "EH/matter/visible EM",
            "ownership_level": "CONDITIONAL_STANDARD_OWNER",
            "why": "standard variational forms exist once observed metric/coframe/Hodge are admitted",
            "main_gap": "parent descent of observed fields and source current/readout closure",
            "next_priority": "medium",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "score_id": "OSC3626_1_GK_q_loc",
            "sector": "Gamma/Khat/q_loc/GK stress",
            "ownership_level": "HARD_ORPHAN",
            "why": "candidate actions exist but Helmholtz/action-existence, Euler closure, and double-zero are not proved",
            "main_gap": "S_GK variational owner or response-doublet physical lock",
            "next_priority": "highest",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "score_id": "OSC3626_2_PiM_source_denominator",
            "sector": "Pi_M/H_tau/source mass boundary denominator",
            "ownership_level": "HARD_ORPHAN",
            "why": "projector algebra exists but projector variation, source denominator, and boundary/reference flux are not parent-owned",
            "main_gap": "M_H_ref / Pi_M J_H / H_tau reference lock",
            "next_priority": "highest_parallel",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "score_id": "OSC3626_3_PPN_component_vector",
            "sector": "PPN/Newton component rows",
            "ownership_level": "RUNNER_SCHEMA_ONLY",
            "why": "component rows exist but values, official bound rows, units, and projection matrices are missing",
            "main_gap": "weak-field projection from action-owned residuals",
            "next_priority": "after_owner_attempt_or_parallel_data_fill",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_gate_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3626_0_inventory_result",
            "decision": "Every RV3624 residual now has a candidate local action/current/boundary owner, but none of the hard residual owners are parent-signed.",
            "status": "INVENTORY_COMPLETE_NONCLAIM",
            "next_action": "attack the highest-leverage orphan rather than circling the whole residual vector",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3626_1_root_orphan",
            "decision": "The cleanest derivation target is S_GK/action-existence: it controls q_loc, T_GK, DeltaE, Bianchi closure, and PPN projections at once.",
            "status": "GK_HELMHOLTZ_ROUTE_SELECTED",
            "next_action": "try Helmholtz/metric-response proof for S_GK; if it fails, demote q_loc/T_GK to coefficient-bound rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3626_2_parallel_orphan",
            "decision": "Pi_M/H_tau/source denominator remains equally dangerous for Newton, but it needs a charge/reference lock rather than a metric-response Helmholtz test.",
            "status": "PARALLEL_PRESSURE_POINT_RETAINED",
            "next_action": "keep source-denominator rows explicit; do not define source mass from measured GM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3626_3_component_rows",
            "decision": "PPN/Newton rows are now component-addressed but remain blocked because no source-backed values/bounds/projection matrices are present.",
            "status": "COMPONENT_ROWS_STAGED_NOT_SCORED",
            "next_action": "only score after owner theorem or real component coefficients exist",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3626_4_next_target",
            "decision": "Next checkpoint should try the Gamma/Khat response action Helmholtz proof or fill q_loc/T_GK PPN coefficient bounds if the proof fails.",
            "status": "NEXT_TARGET_SELECTED",
            "next_action": "3627-Y5-R2FR-Gamma-Khat-response-action-Helmholtz-or-qloc-TGK-bound.md",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS3626_0",
            "result": "LOCAL_RESIDUAL_LAGRANGIAN_INVENTORY_COMPLETE_NONCLAIM",
            "summary": "3626 attaches every explicit local residual to a candidate action/current/boundary owner and stages component-level PPN/Newton rows; the hard unsolved owners are S_GK/q_loc/T_GK and Pi_M/H_tau/source denominator.",
            "all_RV3624_residuals_covered": True,
            "component_rows_staged": True,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3626_0",
            "target_doc": "3627-Y5-R2FR-Gamma-Khat-response-action-Helmholtz-or-qloc-TGK-bound.md",
            "target_script": "scripts/Y5_R2FR_3627_Gamma_Khat_response_action_Helmholtz_or_qloc_TGK_bound.py",
            "objective": "test whether Gamma_eff/K_hat/q_loc/T_GK are generated by a legitimate variational S_GK via Helmholtz/metric-response/Euler/double-zero clauses; if not, fill q_loc/T_GK PPN/Newton component-bound rows as nonclaim",
            "success_gate": "either S_GK passes action-existence, Euler closure, double-zero, and boundary no-flux gates, or q_loc/T_GK receive component-level nonclaim coefficient rows with value/unit/bound/source placeholders made explicit",
            "reason": "S_GK is the highest-leverage orphan: closing it would reduce DeltaE, q_loc, T_GK, Bianchi, and PPN pressure together.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "inventory_status": "RV3624_ALL_RESIDUALS_CANDIDATE_OWNER_MAPPED",
            "hardest_orphan": "S_GK_q_loc_T_GK_ACTION_EXISTENCE",
            "parallel_orphan": "PiM_Htau_source_denominator",
            "PPN_component_status": "STAGED_NOT_SCORED",
            "local_GR_claim": "NO_CLAIM",
            "next_pressure_point": "Gamma_Khat_response_action_Helmholtz_or_qloc_TGK_bound",
            "valid_for_claim": False,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def write_markdown() -> None:
    sources = source_register_rows()
    inventory = inventory_rows()
    euler_map = euler_map_rows()
    components = ppn_component_rows()
    scorecard = scorecard_rows()
    decisions = decision_gate_rows()
    status = status_rows()
    next_target = next_target_rows()
    content = f"""# 3626 Y5 R2FR local residual Lagrangian inventory or PPN component fill

**Status:** {status[0]["summary"]}

**Claim ceiling:** no local-GR, Newton, PPN, Maxwell-source, source-normalization, or q_loc/T_GK pass is claimed from 3626.

## Core result

3626 turns the residual vector into an ownership map. The project now knows which live residuals have conditional standard owners and which remain true orphans:

- `EH/matter/visible EM`: conditional variational owners exist once the observed metric/coframe/Hodge/source current are parent-selected.
- `S_GK/q_loc/T_GK`: hard orphan; candidate actions exist, but Helmholtz/action-existence, Euler closure, double-zero, and boundary no-flux are not proven.
- `Pi_M/H_tau/source denominator`: hard parallel orphan; projector algebra exists, but source mass/reference/variation ownership is not parent-derived.
- `PPN/Newton rows`: component-addressed but not score-ready.

## Source register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Local residual Lagrangian inventory

{markdown_table(inventory, ["inventory_id", "rv3624_id", "residual_symbol", "candidate_owner", "current_status", "blocks"])}

## Euler / variation closure map

{markdown_table(euler_map, ["map_id", "inventory_id", "variation_test", "needed_identity", "current_result"])}

## PPN / Newton component fill rows

{markdown_table(components, ["component_id", "envelope_id", "inventory_owner", "observable_component", "component_value", "bound_value", "score_ready"])}

## Ownership scorecard

{markdown_table(scorecard, ["score_id", "sector", "ownership_level", "main_gap", "next_priority"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "status", "next_action"])}

## Next target

{markdown_table(next_target, ["target_doc", "target_script", "objective", "success_gate"])}
"""
    DOC.write_text(content, encoding="utf-8")


def validate() -> list[dict[str, object]]:
    timestamp = utc_now()
    paths = output_paths()
    pre_validation = {key: path for key, path in paths.items() if key != "validation"}
    sources = source_register_rows()
    inventory = inventory_rows()
    euler_map = euler_map_rows()
    components = ppn_component_rows()
    scorecard = scorecard_rows()
    decisions = decision_gate_rows()
    status = status_rows()
    next_target = next_target_rows()

    results: list[tuple[str, bool, str]] = []
    missing_sources = [row["path"] for row in sources if not row["exists"]]
    results.append(("VAL3626_0_sources_exist", not missing_sources, "all sources exist" if not missing_sources else "; ".join(missing_sources)))
    missing_needles = [row["source_id"] for row in sources if not row["needle_found"]]
    results.append(("VAL3626_1_needles_found", not missing_needles, "all source anchors found" if not missing_needles else "; ".join(missing_needles)))
    missing_outputs = [key for key, path in pre_validation.items() if not path.exists()]
    results.append(("VAL3626_2_outputs_exist", not missing_outputs, "all pre-validation outputs written" if not missing_outputs else "; ".join(missing_outputs)))

    parse_ok = True
    parse_details: list[str] = []
    for key, path in pre_validation.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            rows = read_csv(path)
            parse_details.append(f"{key}:{len(rows)}")
            if not rows:
                parse_ok = False
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{key}:{exc}")
    results.append(("VAL3626_3_csv_parse", parse_ok, "; ".join(parse_details)))

    expected_rv = {f"RV3624_{index}_{suffix}" for index, suffix in enumerate(["DeltaE", "source_weight", "coupling_drift", "q_loc", "GK_stress", "PiM_boundary", "PPN_total"])}
    observed_rv = {row["rv3624_id"] for row in inventory}
    results.append(("VAL3626_4_all_RV3624_covered", expected_rv == observed_rv, "all RV3624 residuals mapped to owners"))
    gk_present = any(row["inventory_id"] == "INV3626_3_q_loc" and "S_GK" in row["candidate_owner"] for row in inventory)
    results.append(("VAL3626_5_GK_owner_mapped", gk_present, "S_GK/q_loc owner row written"))
    pim_present = any(row["inventory_id"] == "INV3626_5_PiM_boundary" and "Pi_M" in row["candidate_owner"] for row in inventory)
    results.append(("VAL3626_6_PiM_boundary_mapped", pim_present, "Pi_M/boundary owner row written"))
    component_count_ok = len(components) == 7 and all(row["score_ready"] is False for row in components)
    results.append(("VAL3626_7_component_rows_nonclaim", component_count_ok, "seven PPN/Newton component rows staged and non-scored"))
    scorecard_ok = any(row["ownership_level"] == "HARD_ORPHAN" and row["sector"] == "Gamma/Khat/q_loc/GK stress" for row in scorecard)
    results.append(("VAL3626_8_hard_orphan_identified", scorecard_ok, "hard GK/q_loc orphan identified"))
    all_nonclaim = all(row.get("claim_allowed") is False and row.get("valid_for_claim") is False for collection in [inventory, euler_map, components, scorecard, decisions, status, next_target] for row in collection)
    results.append(("VAL3626_9_all_outputs_nonclaim", all_nonclaim, "all outputs remain nonclaim"))

    if FORMALIZATION.exists():
        leaked_paths = list(FORMALIZATION.rglob("*3626*"))
        formalization_clean = len(leaked_paths) == 0
        detail = "no 3626 files in formalization-workbench" if formalization_clean else "; ".join(str(path) for path in leaked_paths[:5])
    else:
        formalization_clean = True
        detail = "formalization-workbench not present"
    results.append(("VAL3626_10_no_formalization_leak", formalization_clean, detail))

    next_ok = next_target[0]["target_doc"] == "3627-Y5-R2FR-Gamma-Khat-response-action-Helmholtz-or-qloc-TGK-bound.md"
    results.append(("VAL3626_11_next_target_written", next_ok, "3627 Gamma/Khat Helmholtz target selected"))

    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in results
    ]


def main() -> None:
    paths = output_paths()
    write_csv(paths["source_register"], source_register_rows())
    write_csv(paths["inventory"], inventory_rows())
    write_csv(paths["euler_map"], euler_map_rows())
    write_csv(paths["component_rows"], ppn_component_rows())
    write_csv(paths["scorecard"], scorecard_rows())
    write_csv(paths["decision_gates"], decision_gate_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_csv(paths["canonical_status"], canonical_status_rows())
    write_markdown()
    write_csv(paths["validation"], validate())

    failed = [row for row in read_csv(paths["validation"]) if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3626 validation failed: {failed}")
    print(f"wrote 3626 checkpoint with {len(read_csv(paths['validation']))} validation checks")


if __name__ == "__main__":
    main()

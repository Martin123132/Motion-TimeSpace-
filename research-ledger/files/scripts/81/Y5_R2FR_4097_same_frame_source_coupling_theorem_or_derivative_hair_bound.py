from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4097-Y5-R2FR-same-frame-source-coupling-theorem-or-derivative-hair-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
DECISION = "SAME_FRAME_SOURCE_COUPLING_THEOREM_ASSEMBLED_FIRST_ORDER_NEWTON_DERIVED_CONDITIONALLY_DERIVATIVE_HAIR_VECTOR_RETAINED_NONCLAIM"

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4097_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4096_NEXT_TARGET.csv",
        "4097-Y5-R2FR-same-frame-source-coupling-theorem-or-derivative-hair-bound.md",
        "4096 selects same-frame source-coupling theorem or derivative-hair bound.",
    ),
    "SRC4097_01_source_law": (
        SOURCE_DIR / "P8_Y5_R2FR_4096_SOURCE_NORMALIZATION_LAW.csv",
        "SNL4096_0_observed_EH_source",
        "4096 source-normalization law: observed EH source and calibrated G_ref.",
    ),
    "SRC4097_02_g_calibration": (
        SOURCE_DIR / "P8_Y5_R2FR_4096_CONSTANT_G_CALIBRATION.csv",
        "G4096_1_success_condition",
        "4096 clarification that success is one universal source coefficient, not numeric G derivation.",
    ),
    "SRC4097_03_bound_queue": (
        SOURCE_DIR / "P8_Y5_R2FR_4096_RETAINED_BOUND_QUEUE.csv",
        "RB4096_0_source_derivative_hair",
        "4096 retained queue for source derivative hair.",
    ),
    "SRC4097_04_weak_field": (
        SOURCE_DIR / "P8_Y5_R2FR_3377_WEAK_FIELD_SOURCE_NORMALIZATION_THEOREM.csv",
        "WFS3377_6_normalization_verdict",
        "3377 weak-field source-normalization theorem stack.",
    ),
    "SRC4097_05_newton_chain": (
        SOURCE_DIR / "P8_Y5_R2FR_3382_NEWTON_SOURCE_NORMALIZATION_CHAIN.csv",
        "NEW3382_2_poisson",
        "3382 source-normalized Newton/Poisson chain.",
    ),
    "SRC4097_06_gm_guards": (
        SOURCE_DIR / "P8_Y5_R2FR_3818_SOURCE_NORMALIZATION_GM_GUARDS.csv",
        "SNG3818_3_no_orbital_GM_import",
        "3818 anti-circular measured-GM guard.",
    ),
    "SRC4097_07_ppn_map": (
        SOURCE_DIR / "P8_Y5_R2FR_3954_PPN_SOURCE_NORMALIZATION_RESIDUAL_MAP.csv",
        "PPN3954_8_total_source_norm",
        "3954 residual map for source-normalization leakage.",
    ),
    "SRC4097_08_theorem_stack": (
        SOURCE_DIR / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
        "S5_Newton_gate",
        "Source-normalization theorem stack and Newton gate.",
    ),
    "SRC4097_09_derivative_nohair": (
        SOURCE_DIR / "P8_Y5_R2FR_3557_DERIVATIVE_HAIR_NOHAIR_THEOREM.csv",
        "NH3557_6_no_cancellation_rule",
        "3557 derivative-hair no-hair theorem and no-cancellation guard.",
    ),
    "SRC4097_10_derivative_residuals": (
        SOURCE_DIR / "P8_Y5_R2FR_3599_DERIVATIVE_HAIR_RESIDUALS.csv",
        "DHR3599_0_total",
        "3599 derivative-hair residual identities.",
    ),
    "SRC4097_11_derivative_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_3599_DERIVATIVE_HAIR_BOUND_ROWS.csv",
        "DHB3599_0_dln_Geff_dt",
        "3599 derivative-hair bound rows.",
    ),
    "SRC4097_12_hilbert_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3558_HILBERT_CURRENT_CLOSURE_THEOREM.csv",
        "HC3558_2_closure_sufficient_conditions",
        "3558 same-frame Hilbert current closure theorem.",
    ),
    "SRC4097_13_hilbert_obstructions": (
        SOURCE_DIR / "P8_Y5_R2FR_3558_OBSTRUCTION_RESIDUAL_MAP.csv",
        "OB3558_0_projected_extra_current",
        "3558 source-current obstruction residual map.",
    ),
    "SRC4097_14_closure_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_3558_CLOSURE_CLAUSE_AUDIT.csv",
        "CL3558_2_PiM_chainmap",
        "3558 closure clause audit; Pi_M chainmap and source support gaps.",
    ),
    "SRC4097_15_same_source": (
        SOURCE_DIR / "P8_Y5_R2FR_3883_SAME_HILBERT_SOURCE_LOCK.csv",
        "HSL3883_4_conservation",
        "3883 same-Hilbert-source lock including matter+EM total conservation.",
    ),
    "SRC4097_16_bridge": (
        SOURCE_DIR / "P8_Y5_R2FR_3906_HILBERT_SOURCE_COUPLING_BRIDGE.csv",
        "SRCBR3906_2_Poisson",
        "3906 same-frame Hilbert source coupling bridge.",
    ),
    "SRC4097_17_denominator": (
        SOURCE_DIR / "P8_Y5_R2FR_3964_HILBERT_SOURCE_DENOMINATOR_IDENTITY.csv",
        "HDI3964_2_flux",
        "3964 Hilbert source denominator identity and flux obstruction.",
    ),
}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_string(value: bool) -> str:
    return "True" if value else "False"


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_checkpoint_csv",
                "path_or_url": str(path),
                "needle": needle,
                "role": role,
                "exists": bool_string(path.exists()),
                "valid_for_claim": "False",
                "timestamp_utc": TIMESTAMP,
            }
        )
    rows.append(
        {
            "source_id": "SRC4097_18_script",
            "source_type": "generator_script",
            "path_or_url": str(SCRIPT_PATH),
            "needle": SCRIPT_PATH.name,
            "role": "Reproducible generator for 4097 same-frame source-coupling gate.",
            "exists": bool_string(SCRIPT_PATH.exists()),
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def same_frame_source_coupling_theorem_rows() -> List[dict]:
    return [
        {
            "theorem_id": "SFC4097_0_parent_action_frame",
            "claim_piece": "same-frame parent action",
            "statement": "The local branch uses one observed metric/coframe for EH curvature, ordinary matter, EM stress, clocks and source variation.",
            "formula": "S_loc=(c^4/(16*pi*G_ref)) int sqrt(-g_obs) R[g_obs] + S_matter[psi,A,g_obs] + S_silent",
            "if_signed": "no source normalization is hidden in a frame/readout mismatch",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "SFC4097_1_single_kappa",
            "claim_piece": "single calibrated coupling",
            "statement": "The EH coefficient is the only local source coupling in the scored branch.",
            "formula": "kappa_ref=8*pi*G_ref/c^4 with D_X kappa_ref=0",
            "if_signed": "constant calibrated G_ref plays the same role as GR's G",
            "current_status": "CONDITIONAL_COMMON_MODE_ALLOWED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "SFC4097_2_Hilbert_source",
            "claim_piece": "Hilbert source owner",
            "statement": "The field-equation source is the Hilbert stress/current from the same matter action, before orbital or arena readout.",
            "formula": "T_H^{mu nu}=-(2/sqrt(-g_obs)) delta S_matter/delta g_obs_{mu nu}; J_H[tau]=T_H^{mu nu} tau_nu dSigma_mu",
            "if_signed": "rho_H is the same source in field equations, Hamiltonian charge and Newtonian limit",
            "current_status": "EXACT_CONDITIONAL_FROM_VARIATION",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "SFC4097_3_projected_flux_closure",
            "claim_piece": "closed projected Hilbert mass current",
            "statement": "The projected source mass is surface/support independent only when the Hilbert current obstruction vanishes.",
            "formula": "d(Pi_M J_H)= -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent = 0",
            "if_signed": "M_H is a parent source charge rather than post-fitted orbital GM",
            "current_status": "MAIN_UNSIGNED_GATE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "SFC4097_4_weak_field_poisson",
            "claim_piece": "Poisson/Newton coefficient",
            "statement": "Once the same source and kappa are fixed, the first-order weak-field equation gives the Newtonian Poisson law.",
            "formula": "G_00^(1)=2 nabla^2 Phi_N/c^2; T_00=rho_H c^2; kappa_ref=8*pi*G_ref/c^4 => nabla^2 Phi_N=4*pi*G_ref rho_H",
            "if_signed": "first-order Newton force follows with U=G_ref M_H/r and a=-grad U",
            "current_status": "EXACT_CONDITIONAL_ALGEBRA",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "SFC4097_5_derivative_hair_silence",
            "claim_piece": "no derivative source hair",
            "statement": "The chain promotes only if all independent time/range/radial/species/readout derivatives vanish by theorem, not cancellation.",
            "formula": "D_X ln mu_obs = D_X ln(G_ref w_common ell_J R_frame) + D_X ln M_H + D_X ln(1+epsilon_mu) = 0",
            "if_signed": "no hidden Gdot, WEP source charge, fifth-force range hair, radial mass drift or frame split remains",
            "current_status": "NOT_SIGNED_BOUND_VECTOR_ACTIVE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def newton_chain_gate_rows() -> List[dict]:
    return [
        {
            "gate_id": "NCG4097_0_same_frame",
            "requirement": "same frame gate: EH, matter, EM, clocks and source measure descend through the same g_obs/e_obs branch.",
            "evidence_status": "candidate_from_3883_3906",
            "failure_residual": "delta_frame_source",
            "observable_if_fail": "clock/WEP/source readout mismatch",
            "promotion_status": "NOT_PUBLIC",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "NCG4097_1_single_kappa",
            "requirement": "one derivative-free kappa_ref controls EH variation and Hilbert source response.",
            "evidence_status": "conditional_from_3377_3382",
            "failure_residual": "D_X ln(G_ref w_common ell_J R_frame)",
            "observable_if_fail": "Gdot; clock/source coupling drift; range-dependent G_eff",
            "promotion_status": "NOT_PUBLIC",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "NCG4097_2_Hilbert_current",
            "requirement": "J_H[tau] is the source current obtained by functional variation before readout.",
            "evidence_status": "exact_conditional_definition",
            "failure_residual": "J_direct; J_measure; eta_source_AB",
            "observable_if_fail": "WEP source charge; R10 composition dependence",
            "promotion_status": "NOT_PUBLIC",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "NCG4097_3_PiM_flux",
            "requirement": "Pi_M J_H is closed across the compact exterior annulus and independent of linking surface.",
            "evidence_status": "obstruction_identity_known_not_zeroed",
            "failure_residual": "Pi_M dJ_extra; [d,Pi_M]J_H; A_parent",
            "observable_if_fail": "radial source hair; source normalization drift; projector stress",
            "promotion_status": "MAIN_BLOCKER",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "NCG4097_4_Gauss_Hamiltonian",
            "requirement": "Hamiltonian boundary charge and projected Hilbert mass are the same object.",
            "evidence_status": "target_identity_from_3964",
            "failure_residual": "Delta_cal; C_ref; C_units; boundary symplectic flux",
            "observable_if_fail": "orbital GM backfill risk; inverse-square calibration drift",
            "promotion_status": "NOT_PUBLIC",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "NCG4097_5_Poisson",
            "requirement": "weak-field 00 equation reduces to Poisson with the same rho_H and G_ref.",
            "evidence_status": "exact_conditional_algebra",
            "failure_residual": "extra local K_MTS_IR_00; nonEH_operator_potential",
            "observable_if_fail": "gamma/beta/source R11 residuals",
            "promotion_status": "ALGEBRA_READY_INPUTS_UNSIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "gate_id": "NCG4097_6_no_orbital_backfill",
            "requirement": "measured orbital GM is not imported to define the source before Poisson/Gauss closure.",
            "evidence_status": "guardrail_pass_nonclaim",
            "failure_residual": "circular GM calibration",
            "observable_if_fail": "fake Newton derivation",
            "promotion_status": "GUARDRAIL_ACTIVE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def obstruction_to_bound_rows() -> List[dict]:
    return [
        {
            "obstruction_id": "OB4097_0_extra_mass_projection",
            "source_identity_piece": "Pi_M dJ_extra",
            "meaning": "boundary, bulk, domain, memory, connection, nonminimal EM or q_loc currents project into the mass channel",
            "zero_condition": "Pi_M dJ_extra=0 by parent silence/topology or explicit component theorem",
            "bound_if_open": "epsilon_mu; alpha(lambda); boundary/domain flux products",
            "current_status": "OPEN_BOUND_REQUIRED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "obstruction_id": "OB4097_1_PiM_commutator",
            "source_identity_piece": "[d,Pi_M]J_H",
            "meaning": "mass projector or support varies across source/readout/domain data",
            "zero_condition": "Pi_M is identity/inclusion on Hilbert mass current or fixed parent chain map",
            "bound_if_open": "Delta_PiM; C_M; C_shape; projector stress",
            "current_status": "MAIN_STRUCTURAL_BLOCKER",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "obstruction_id": "OB4097_2_parent_anomaly",
            "source_identity_piece": "A_parent",
            "meaning": "unowned multiplier/readout mask/source anomaly modifies the source identity",
            "zero_condition": "first-class/gauge/topological owner or no multiplier in local branch",
            "bound_if_open": "closure anomaly residual",
            "current_status": "OPEN_BOUND_REQUIRED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "obstruction_id": "OB4097_3_boundary_symplectic",
            "source_identity_piece": "Delta_symp",
            "meaning": "Hamiltonian/non-EH symplectic boundary flux shifts the source charge",
            "zero_condition": "integrable H_tau and exact/zero local boundary flux",
            "bound_if_open": "epsilon_boundary; alpha3; zeta/beta boundary rows",
            "current_status": "OPEN_BOUND_REQUIRED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "obstruction_id": "OB4097_4_worldtube_reference",
            "source_identity_piece": "C_domain+C_ref+C_units",
            "meaning": "worldtube/support/reference/units selected after readout launders mass normalization",
            "zero_condition": "support, reference and denominator are parent-owned before readout",
            "bound_if_open": "radial profile; reference drift; unit/readout drift",
            "current_status": "OPEN_BOUND_REQUIRED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "obstruction_id": "OB4097_5_frame_species",
            "source_identity_piece": "Delta_frame + eta_source_AB",
            "meaning": "source variation and matter/clock/orbit readout are not the same branch, or carry species labels",
            "zero_condition": "same-frame selector-blind source action",
            "bound_if_open": "delta_frame_source; eta_source_AB",
            "current_status": "OPEN_BOUND_REQUIRED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "obstruction_id": "OB4097_6_PPN_source_stability",
            "source_identity_piece": "Delta_PPN",
            "meaning": "first-order Newton closure does not automatically close gamma/beta/zeta",
            "zero_condition": "second-order source-normalized weak-field calculation",
            "bound_if_open": "delta_beta_source; gamma_minus_1; zeta_i",
            "current_status": "OPEN_NEXT_ORDER_REQUIRED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def derivative_hair_bound_vector_rows() -> List[dict]:
    return [
        {
            "bound_id": "DHB4097_0_coupling_time_drift",
            "hair_channel": "global/effective coupling drift",
            "symbol": "dln_Geff_dt",
            "formula": "d ln(G_ref w_common ell_J R_frame)/dt",
            "observable": "Gdot_over_G; clock/source drift",
            "zero_route": "G_ref, w_common, ell_J and R_frame are parent-fixed constants",
            "bound_route": "fill time-drift coefficient and compare to Gdot bounds",
            "current_value": "MISSING_GLOBAL_COUPLING_SUPERSELECTION_OR_DRIFT_BOUND",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "DHB4097_1_projected_mass_time_flux",
            "hair_channel": "projected Hilbert mass time drift",
            "symbol": "dln_MH_dt",
            "formula": "d ln M_H/dt from d(Pi_M J_H)",
            "observable": "Gdot-like source drift; nonstationary source normalization",
            "zero_route": "stationary compact exterior and no timelike boundary/source flux",
            "bound_route": "fill stationary flux coefficient or source-history profile",
            "current_value": "MISSING_STATIONARY_PROJECTED_SOURCE_FLUX_CLOSURE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "DHB4097_2_radial_coupling_hair",
            "hair_channel": "radial/range coupling hair",
            "symbol": "partial_r_ln_Geff",
            "formula": "partial_r ln G_eff or finite-range alpha(lambda)",
            "observable": "inverse-square law; R10 alpha(lambda); radial acceleration residual",
            "zero_route": "no finite-range pole/running coupling in source channel",
            "bound_route": "R10 alpha(lambda) and radial profile rows",
            "current_value": "MISSING_RANGE_RADIAL_COUPLING_SUPERSELECTION",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "DHB4097_3_projected_mass_radial_hair",
            "hair_channel": "radial projected source leakage",
            "symbol": "partial_r_ln_MH",
            "formula": "partial_r ln M_H = radial flux leakage of Pi_M J_H",
            "observable": "radial source hair; inverse-square failure",
            "zero_route": "closed Pi_M Hilbert flux over exterior annuli",
            "bound_route": "radial source profile coefficient",
            "current_value": "MISSING_RADIAL_PROJECTED_FLUX_CLOSURE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "DHB4097_4_species_source_charge",
            "hair_channel": "species/source composition dependence",
            "symbol": "eta_source_AB",
            "formula": "Delta source response between material labels A,B",
            "observable": "WEP source charge; R10 composition dependence",
            "zero_route": "selector-blind source action through one observed coframe",
            "bound_route": "species charge vector and WEP/R10 comparison",
            "current_value": "MISSING_SELECTOR_BLIND_THEOREM_OR_ETA_SOURCE_BOUND",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "DHB4097_5_frame_source_split",
            "hair_channel": "source/readout frame mismatch",
            "symbol": "delta_frame_source",
            "formula": "Delta between source variation frame and clock/orbit/photon readout frame",
            "observable": "clock redshift; WEP; local GR frame consistency",
            "zero_route": "same parent frame controls source, matter motion, clocks, photons and orbital readout",
            "bound_route": "frame calibration split residual",
            "current_value": "MISSING_SAME_FRAME_SOURCE_THEOREM_OR_FRAME_BOUND",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "DHB4097_6_extra_monopole",
            "hair_channel": "extra non-Hilbert monopole/source normalization",
            "symbol": "epsilon_mu",
            "formula": "mu_extra/(G_ref M_H)",
            "observable": "Newton source coupling; gamma/beta/zeta; R11 source normalization",
            "zero_route": "all non-Hilbert mass-channel currents vanish/topological/common constant",
            "bound_route": "component coefficient vector for boundary, bulk, domain, memory, connection, EM and q_loc",
            "current_value": "MISSING_ZERO_EXTRA_MONOPOLE_OR_UNIVERSAL_CONSTANT",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "DHB4097_7_PPN_source_tail",
            "hair_channel": "second-order source-normalization tail",
            "symbol": "delta_beta_source; gamma_minus_1; zeta_i",
            "formula": "Pi_PPN[source residuals] after first-order Poisson closure",
            "observable": "gamma; beta; zeta_i; local GR",
            "zero_route": "second-order weak-field source calculation closes with no R11/nonEH tail",
            "bound_route": "PPN source residual vector",
            "current_value": "MISSING_SECOND_ORDER_SOURCE_PPN_MAP",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def newton_ppn_decision_rows() -> List[dict]:
    return [
        {
            "decision_id": "NPD4097_0_first_order_algebra",
            "question": "Does the same-frame theorem give Newton/Poisson if its clauses are signed?",
            "answer": "yes_conditionally",
            "formula": "same frame + kappa_ref + T_H + d(Pi_M J_H)=0 => nabla^2 Phi_N=4*pi*G_ref rho_H",
            "status": "EXACT_CONDITIONAL_FIRST_ORDER_DERIVATION",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "NPD4097_1_current_claim",
            "question": "Can current MTS claim source-normalized Newtonian mechanics?",
            "answer": "not_yet",
            "formula": "Pi_M closure, Hamiltonian/Gauss equality, worldtube support, extra-current silence and derivative-hair nohair are unsigned",
            "status": "PUBLIC_NEWTON_SOURCE_CLAIM_FALSE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "NPD4097_2_PPN",
            "question": "Does first-order source closure prove local GR/PPN?",
            "answer": "no",
            "formula": "gamma,beta,zeta need second-order source/readout/R11 residual calculation",
            "status": "PPN_REMAINS_NEXT_ORDER_GATE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "NPD4097_3_G",
            "question": "Must MTS derive the numerical value of G_ref?",
            "answer": "no_for_GR_reduction",
            "formula": "G_ref is calibrated like GR's G; the derived target is one universal role with D_X G_ref=0",
            "status": "CALIBRATED_CONSTANT_ALLOWED_NO_HAIR_ALLOWED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def claim_gate_rows() -> List[dict]:
    return [
        {
            "claim_id": "CLAIM4097_0_conditional_derivation",
            "claim": "same-frame source-coupling clauses are sufficient for first-order Newton/Poisson",
            "allowed": "True",
            "reason": "variation plus weak-field 00 algebra gives Poisson with one G_ref if Hilbert source and flux closure are signed",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4097_1_Newton_public",
            "claim": "MTS has publicly derived source-normalized Newtonian mechanics",
            "allowed": "False",
            "reason": "Pi_M closure, Gauss/Hamiltonian equality, worldtube support and derivative-hair silence remain unsigned",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4097_2_G_numeric",
            "claim": "MTS derives the numeric value of Newton's constant",
            "allowed": "False",
            "reason": "not derived and not required for GR reduction; G_ref is a calibrated universal constant",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4097_3_no_derivative_hair",
            "claim": "all derivative source hair is theorem-zero",
            "allowed": "False",
            "reason": "bound vector rows remain missing parent coefficients or no-hair certificates",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4097_4_local_GR_PPN",
            "claim": "local GR/PPN is derived",
            "allowed": "False",
            "reason": "first-order source coupling does not close gamma, beta, zeta, R11 or EM/Poynting same-frame gate",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def decision_gate_rows() -> List[dict]:
    return [
        {
            "decision_id": "DEC4097_0_theorem",
            "decision": "assemble same-frame source-coupling theorem as the Newton branch target",
            "meaning": "This gives the exact contract a parent action must satisfy to reduce to Newton without importing orbital GM.",
            "result": "first-order Newton is conditionally derived from action/source clauses",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4097_1_bound",
            "decision": "retain derivative-hair vector for every unsigned leakage route",
            "meaning": "If a clause fails, the failure becomes Gdot/WEP/R10/radial/PPN source rows, not closure prose.",
            "result": "derivative-hair bound vector active",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4097_2_next",
            "decision": "attack Pi_M/Hamiltonian/Gauss identity next",
            "meaning": "The biggest remaining non-circular obstacle is proving the projected Hilbert mass is the same object as the geometric boundary/Gauss mass.",
            "result": "4098 source-mass identity target selected before EM gate",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            "target_id": "NEXT4097_0",
            "next_target": "4098-Y5-R2FR-PiM-Hamiltonian-Gauss-source-mass-identity-or-radial-hair-bound.md",
            "script": "scripts/Y5_R2FR_4098_PiM_Hamiltonian_Gauss_source_mass_identity_or_radial_hair_bound.py",
            "why": "4097 shows first-order Newton follows if the projected Hilbert mass is the same closed mass object as the Hamiltonian/Gauss charge. This is the sharpest remaining source-coupling obstruction.",
            "priority": "P0",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "target_id": "NEXT4097_1",
            "next_target": "4099-Y5-R2FR-EM-Maxwell-Hilbert-Poynting-same-frame-gate.md",
            "script": "defer_until_source_mass_identity",
            "why": "EM/Poynting should be tested once the source mass denominator is stable, because EM stress is part of the same Hilbert source.",
            "priority": "P1",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            "checkpoint": "4097",
            "decision": DECISION,
            "first_order_Newton_conditional": "True",
            "Newton_source_public": "False",
            "local_GR_public": "False",
            "derivative_hair_bound_vector": "active",
            "main_unsigned_gate": "Pi_M_Hamiltonian_Gauss_source_mass_identity",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    ]


def write_doc() -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 4097 - Same-Frame Source Coupling Theorem Or Derivative-Hair Bound",
                "",
                "## Purpose",
                "",
                "4096 reduced `Y5_source_normalization` to a concrete source-coupling problem. 4097 assembles the exact first-order Newton contract: one observed frame, one calibrated `G_ref/kappa_ref`, one Hilbert source, and one closed projected mass current.",
                "",
                f"- Decision: `{DECISION}`",
                "- Public Newton/source-coupling claim: `false`",
                "- Public local-GR/PPN claim: `false`",
                "",
                "## Conditional Derivation",
                "",
                "If the parent action signs",
                "",
                "```text",
                "S_loc = (c^4/(16 pi G_ref)) int sqrt(-g_obs) R[g_obs] + S_matter[psi,A,g_obs] + S_silent",
                "T_H^{mu nu} = -(2/sqrt(-g_obs)) delta S_matter / delta g_obs_{mu nu}",
                "d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent = 0",
                "kappa_ref = 8 pi G_ref / c^4",
                "```",
                "",
                "then the weak-field `00` equation gives",
                "",
                "```text",
                "G_00^(1)=2 nabla^2 Phi_N/c^2,   T_00=rho_H c^2",
                "=> nabla^2 Phi_N = 4 pi G_ref rho_H",
                "=> U = G_ref M_H/r,   a = -grad U",
                "```",
                "",
                "That is the right GR-style target: the numerical value of `G_ref` is calibrated, but its universal role is derived.",
                "",
                "## What Still Blocks A Claim",
                "",
                "- `Pi_M J_H` closure is not parent-signed.",
                "- the Hamiltonian/Gauss boundary charge is not yet proved to be the same object as the projected Hilbert mass.",
                "- worldtube/support/reference data are not yet locked before readout.",
                "- derivative hair (`Gdot`, radial/range hair, species source charge, frame split, extra monopoles) remains active.",
                "- first-order Newton does not by itself close `gamma`, `beta`, `zeta`, R11, or EM/Poynting stress ownership.",
                "",
                "## Bound Route",
                "",
                "Every failure mode has a retained row: `dln_Geff_dt`, `dln_MH_dt`, `partial_r_ln_Geff`, `partial_r_ln_MH`, `eta_source_AB`, `delta_frame_source`, `epsilon_mu`, and second-order PPN source tails.",
                "",
                "## Next Target",
                "",
                "`4098-Y5-R2FR-PiM-Hamiltonian-Gauss-source-mass-identity-or-radial-hair-bound.md` should attack the sharpest remaining source-coupling obstruction: proving the projected Hilbert mass is the same closed source object as the Hamiltonian/Gauss mass.",
                "",
                "## Outputs",
                "",
                "- `P8_Y5_R2FR_4097_SOURCE_REGISTER.csv`",
                "- `P8_Y5_R2FR_4097_SAME_FRAME_SOURCE_COUPLING_THEOREM.csv`",
                "- `P8_Y5_R2FR_4097_NEWTON_CHAIN_GATE.csv`",
                "- `P8_Y5_R2FR_4097_OBSTRUCTION_TO_BOUND.csv`",
                "- `P8_Y5_R2FR_4097_DERIVATIVE_HAIR_BOUND_VECTOR.csv`",
                "- `P8_Y5_R2FR_4097_NEWTON_PPN_DECISION.csv`",
                "- `P8_Y5_R2FR_4097_DECISION_GATE.csv`",
                "- `P8_Y5_R2FR_4097_CLAIM_GATE.csv`",
                "- `P8_Y5_R2FR_4097_NEXT_TARGET.csv`",
                "- `P8_Y5_R2FR_4097_STATUS.csv`",
                "- `P8_Y5_BRR545_4097_VALIDATION.csv`",
                "",
            ]
        ),
        encoding="utf-8",
    )


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4097_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4097_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4097_SAME_FRAME_SOURCE_COUPLING_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4097_SAME_FRAME_SOURCE_COUPLING_THEOREM.csv",
        "P8_Y5_R2FR_4097_NEWTON_CHAIN_GATE": SOURCE_DIR / "P8_Y5_R2FR_4097_NEWTON_CHAIN_GATE.csv",
        "P8_Y5_R2FR_4097_OBSTRUCTION_TO_BOUND": SOURCE_DIR / "P8_Y5_R2FR_4097_OBSTRUCTION_TO_BOUND.csv",
        "P8_Y5_R2FR_4097_DERIVATIVE_HAIR_BOUND_VECTOR": SOURCE_DIR / "P8_Y5_R2FR_4097_DERIVATIVE_HAIR_BOUND_VECTOR.csv",
        "P8_Y5_R2FR_4097_NEWTON_PPN_DECISION": SOURCE_DIR / "P8_Y5_R2FR_4097_NEWTON_PPN_DECISION.csv",
        "P8_Y5_R2FR_4097_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4097_DECISION_GATE.csv",
        "P8_Y5_R2FR_4097_CLAIM_GATE": SOURCE_DIR / "P8_Y5_R2FR_4097_CLAIM_GATE.csv",
        "P8_Y5_R2FR_4097_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4097_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4097_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4097_STATUS.csv",
    }


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4097_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4097_SAME_FRAME_SOURCE_COUPLING_THEOREM"], same_frame_source_coupling_theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4097_NEWTON_CHAIN_GATE"], newton_chain_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4097_OBSTRUCTION_TO_BOUND"], obstruction_to_bound_rows())
    write_csv(outputs["P8_Y5_R2FR_4097_DERIVATIVE_HAIR_BOUND_VECTOR"], derivative_hair_bound_vector_rows())
    write_csv(outputs["P8_Y5_R2FR_4097_NEWTON_PPN_DECISION"], newton_ppn_decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4097_DECISION_GATE"], decision_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4097_CLAIM_GATE"], claim_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4097_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4097_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        contains = exists and needle in read_text(path)
        rows.append(
            {
                "check_id": f"VAL4097_SRC_{source_id}",
                "check": "local source exists and contains needle",
                "passed": bool_string(contains),
                "detail": f"{path} | needle={needle} | role={role}",
                "timestamp_utc": TIMESTAMP,
            }
        )

    for name, path in outputs.items():
        try:
            parsed = parse_csv(path)
            ok = len(parsed) > 0
            detail = f"{path} rows={len(parsed)}"
        except Exception as exc:
            ok = False
            detail = f"{path} parse_error={exc}"
        rows.append(
            {
                "check_id": f"VAL4097_CSV_{name}",
                "check": "generated CSV parses and is non-empty",
                "passed": bool_string(ok),
                "detail": detail,
                "timestamp_utc": TIMESTAMP,
            }
        )

    theorem = parse_csv(outputs["P8_Y5_R2FR_4097_SAME_FRAME_SOURCE_COUPLING_THEOREM"])
    theorem_text = "\n".join(str(row) for row in theorem)
    theorem_ok = all(
        needle in theorem_text
        for needle in ["S_loc", "kappa_ref", "T_H", "d(Pi_M J_H)", "nabla^2 Phi_N=4*pi*G_ref rho_H", "D_X ln mu_obs"]
    )
    rows.append(
        {
            "check_id": "VAL4097_THEOREM_CORE",
            "check": "source-coupling theorem contains action, kappa, Hilbert source, flux closure, Poisson and derivative-hair identity",
            "passed": bool_string(theorem_ok),
            "detail": "requires first-order Newton derivation and no-hair identity",
            "timestamp_utc": TIMESTAMP,
        }
    )

    chain = parse_csv(outputs["P8_Y5_R2FR_4097_NEWTON_CHAIN_GATE"])
    chain_text = "\n".join(str(row) for row in chain)
    chain_ok = all(needle in chain_text for needle in ["same frame", "Pi_M", "Hamiltonian", "Poisson", "orbital GM"])
    rows.append(
        {
            "check_id": "VAL4097_CHAIN_GATES",
            "check": "Newton chain gates include same-frame, PiM, Hamiltonian, Poisson and no-orbital-backfill guard",
            "passed": bool_string(chain_ok),
            "detail": f"gate_rows={len(chain)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    obstructions = parse_csv(outputs["P8_Y5_R2FR_4097_OBSTRUCTION_TO_BOUND"])
    obstruction_text = "\n".join(str(row) for row in obstructions)
    obstruction_ok = all(
        needle in obstruction_text
        for needle in ["Pi_M dJ_extra", "[d,Pi_M]J_H", "A_parent", "Delta_symp", "Delta_frame", "Delta_PPN"]
    )
    rows.append(
        {
            "check_id": "VAL4097_OBSTRUCTION_MAP",
            "check": "obstruction map covers exact source-current failure modes",
            "passed": bool_string(obstruction_ok),
            "detail": f"obstruction_rows={len(obstructions)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    bounds = parse_csv(outputs["P8_Y5_R2FR_4097_DERIVATIVE_HAIR_BOUND_VECTOR"])
    bound_text = "\n".join(str(row) for row in bounds)
    bound_ok = all(
        needle in bound_text
        for needle in [
            "dln_Geff_dt",
            "dln_MH_dt",
            "partial_r_ln_Geff",
            "partial_r_ln_MH",
            "eta_source_AB",
            "delta_frame_source",
            "epsilon_mu",
            "delta_beta_source",
        ]
    )
    rows.append(
        {
            "check_id": "VAL4097_DERIVATIVE_BOUND_VECTOR",
            "check": "derivative-hair bound vector covers time, radial, species, frame, monopole and PPN tails",
            "passed": bool_string(bound_ok),
            "detail": f"bound_rows={len(bounds)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    decisions = parse_csv(outputs["P8_Y5_R2FR_4097_NEWTON_PPN_DECISION"])
    decision_text = "\n".join(str(row) for row in decisions)
    decision_ok = all(needle in decision_text for needle in ["yes_conditionally", "PUBLIC_NEWTON_SOURCE_CLAIM_FALSE", "PPN_REMAINS_NEXT_ORDER_GATE", "no_for_GR_reduction"])
    rows.append(
        {
            "check_id": "VAL4097_NEWTON_PPN_DECISION",
            "check": "decision separates conditional first-order Newton derivation from public claim and PPN closure",
            "passed": bool_string(decision_ok),
            "detail": "requires conditional derivation, false public claim, PPN next-order gate and calibrated-G clarification",
            "timestamp_utc": TIMESTAMP,
        }
    )

    claims = parse_csv(outputs["P8_Y5_R2FR_4097_CLAIM_GATE"])
    no_public = all(row.get("public_claim") == "False" and row.get("valid_for_claim") == "False" for row in claims)
    rows.append(
        {
            "check_id": "VAL4097_NO_PUBLIC_CLAIM",
            "check": "4097 does not promote Newton, numeric G, derivative-hair silence or local-GR/PPN claims",
            "passed": bool_string(no_public),
            "detail": "all claim rows remain private/nonclaim",
            "timestamp_utc": TIMESTAMP,
        }
    )

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4097_NEXT_TARGET"])
    next_text = "\n".join(str(row) for row in next_rows)
    next_ok = "4098-Y5-R2FR-PiM-Hamiltonian-Gauss-source-mass-identity-or-radial-hair-bound.md" in next_text
    rows.append(
        {
            "check_id": "VAL4097_NEXT_TARGET",
            "check": "next target attacks PiM/Hamiltonian/Gauss mass identity",
            "passed": bool_string(next_ok),
            "detail": "requires 4098 source-mass identity next target",
            "timestamp_utc": TIMESTAMP,
        }
    )

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_touched = any(is_under(path, FORMALIZATION) for path in output_paths)
    rows.append(
        {
            "check_id": "VAL4097_SCOPE",
            "check": "outputs stay in post-checkpoint-work and not formalization-workbench",
            "passed": bool_string(in_scope and not formalization_touched),
            "detail": f"doc={DOC_PATH}; csv_count={len(outputs)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
        compile_detail = "py_compile passed"
    except Exception as exc:
        compile_ok = False
        compile_detail = f"py_compile failed: {exc}"
    rows.append(
        {
            "check_id": "VAL4097_SCRIPT_COMPILES",
            "check": "generator script compiles",
            "passed": bool_string(compile_ok),
            "detail": compile_detail,
            "timestamp_utc": TIMESTAMP,
        }
    )

    return rows


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4097_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)

    print(f"4097 complete: {DECISION}")
    print(f"doc: {DOC_PATH}")
    print(f"csv_dir: {SOURCE_DIR}")
    print(f"validation: {validation_path}")


if __name__ == "__main__":
    main()

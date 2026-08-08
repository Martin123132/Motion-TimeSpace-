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
DOC_PATH = ROOT / "4098-Y5-R2FR-PiM-Hamiltonian-Gauss-source-mass-identity-or-radial-hair-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
DECISION = "PIMH_OPERATOR_IDENTITY_ADOPTED_HAMILTONIAN_GAUSS_MASS_IDENTITY_CONTRACT_BUILT_RADIAL_SOURCE_HAIR_BOUND_VECTOR_RETAINED"

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4098_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4097_NEXT_TARGET.csv",
        "4098-Y5-R2FR-PiM-Hamiltonian-Gauss-source-mass-identity-or-radial-hair-bound.md",
        "4097 selects PiM/Hamiltonian/Gauss source-mass identity.",
    ),
    "SRC4098_01_chain_gate": (
        SOURCE_DIR / "P8_Y5_R2FR_4097_NEWTON_CHAIN_GATE.csv",
        "NCG4097_4_Gauss_Hamiltonian",
        "4097 Newton chain gate identifies Hamiltonian/Gauss equality as an unsigned gate.",
    ),
    "SRC4098_02_obstructions": (
        SOURCE_DIR / "P8_Y5_R2FR_4097_OBSTRUCTION_TO_BOUND.csv",
        "OB4097_1_PiM_commutator",
        "4097 obstruction map preserves PiM/support/Hamiltonian/source failures.",
    ),
    "SRC4098_03_derivative_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4097_DERIVATIVE_HAIR_BOUND_VECTOR.csv",
        "DHB4097_3_projected_mass_radial_hair",
        "4097 derivative hair bound vector includes radial projected source hair.",
    ),
    "SRC4098_04_hilbert_denominator": (
        SOURCE_DIR / "P8_Y5_R2FR_3964_HILBERT_SOURCE_DENOMINATOR_IDENTITY.csv",
        "HDI3964_1_Hamiltonian",
        "3964 denominator identity: Hamiltonian equality target and Hilbert source denominator.",
    ),
    "SRC4098_05_flux_identity": (
        SOURCE_DIR / "P8_Y5_R2FR_3964_HILBERT_SOURCE_DENOMINATOR_IDENTITY.csv",
        "HDI3964_2_flux",
        "3964 flux identity: radial/time drift equals projected Hilbert flux failure.",
    ),
    "SRC4098_06_pim_adoption": (
        SOURCE_DIR / "P8_Y5_R2FR_3559_HILBERT_IDENTITY_PIM_ADOPTION_THEOREM.csv",
        "PIA3559_1_identity_chainmap_zero",
        "3559 adopts Pi_M^H as identity/inclusion on typed Hilbert mass-current complex.",
    ),
    "SRC4098_07_pim_clauses": (
        SOURCE_DIR / "P8_Y5_R2FR_3559_ADOPTION_CLAUSE_AUDIT.csv",
        "CLA3559_1_PiMH_identity",
        "3559 clause audit marks independent PiM operator commutator zero on preferred branch.",
    ),
    "SRC4098_08_pim_support": (
        SOURCE_DIR / "P8_Y5_R2FR_3559_SOURCE_SUPPORT_OBSTRUCTION_MAP.csv",
        "OBS3559_1_Delta_support",
        "3559 moves live obstruction from PiM operator to source support drift.",
    ),
    "SRC4098_09_support_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3560_SOURCE_SUPPORT_QBASIC_THEOREM.csv",
        "SWT3560_5_local_closure_consequence",
        "3560 proves support descent conditionally from q-basic density and regular support.",
    ),
    "SRC4098_10_support_residuals": (
        SOURCE_DIR / "P8_Y5_R2FR_3560_SUPPORT_RESIDUAL_DECOMPOSITION.csv",
        "SRD3560_7_Delta_support_total",
        "3560 support residual decomposition.",
    ),
    "SRC4098_11_density_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_3561_HILBERT_DENSITY_QBASIC_THEOREM.csv",
        "HDQ3561_1_pullback_density_theorem",
        "3561 q-basic Hilbert density theorem and source-only countermodel.",
    ),
    "SRC4098_12_density_bound": (
        SOURCE_DIR / "P8_Y5_R2FR_3561_BOUND_VECTOR.csv",
        "BD3561_1_delta_w_species",
        "3561 bound rows for source-only weights and density q-basic failure.",
    ),
    "SRC4098_13_gm_guards": (
        SOURCE_DIR / "P8_Y5_R2FR_3818_SOURCE_NORMALIZATION_GM_GUARDS.csv",
        "SNG3818_3_no_orbital_GM_import",
        "3818 anti-circular orbital GM import guard.",
    ),
    "SRC4098_14_newton_chain": (
        SOURCE_DIR / "P8_Y5_R2FR_3382_NEWTON_SOURCE_NORMALIZATION_CHAIN.csv",
        "NEW3382_3_gauss_charge",
        "3382 Gauss/charge consistency row.",
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
            "source_id": "SRC4098_15_script",
            "source_type": "generator_script",
            "path_or_url": str(SCRIPT_PATH),
            "needle": SCRIPT_PATH.name,
            "role": "Reproducible generator for 4098 source-mass identity gate.",
            "exists": bool_string(SCRIPT_PATH.exists()),
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    )
    return rows


def source_mass_identity_theorem_rows() -> List[dict]:
    return [
        {
            "theorem_id": "SMI4098_0_pimh_adoption",
            "claim_piece": "preferred mass-current projector",
            "statement": "Use Pi_M^H as identity/inclusion on the typed Hilbert mass-current complex C_H^M(W,e_obs,tau), not a free Hodge/topological/readout projector.",
            "formula": "Pi_M^H=id/inclusion on C_H^M => [d,Pi_M^H]J_H^M=0",
            "if_signed": "the independent PiM operator commutator is removed from the live obstruction list",
            "current_status": "ADOPTED_PRIVATE_BRANCH_EXACT_OPERATOR_ZERO",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "SMI4098_1_hilbert_mass_definition",
            "claim_piece": "projected Hilbert mass denominator",
            "statement": "Define source mass before readout by integrating the same Hilbert current over a fixed source-linking surface.",
            "formula": "M_H[S] := N_G int_S Pi_M^H J_H[tau]",
            "if_signed": "mass denominator is not imported from orbital GM",
            "current_status": "DEFINITION_CONDITIONAL_NONCLAIM",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "SMI4098_2_surface_independence",
            "claim_piece": "closed Hilbert source flux",
            "statement": "Two linking surfaces define the same source mass only if projected Hilbert flux has no exterior leakage.",
            "formula": "M_H(S2)-M_H(S1)=N_G int_A d(Pi_M^H J_H)",
            "if_signed": "radial source hair partial_r ln M_H vanishes",
            "current_status": "FLUX_IDENTITY_EXACT_ZERO_CONDITIONS_UNSIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "SMI4098_3_hamiltonian_equality",
            "claim_piece": "Hamiltonian boundary mass equals Hilbert mass",
            "statement": "The geometric Hamiltonian charge and the projected Hilbert source mass must be the same variational object with the same reference subtraction.",
            "formula": "B_tau/G_ref = M_H[Pi_M^H J_H] and delta B_tau = delta int_S Pi_M^H J_H",
            "if_signed": "Gauss mass, source mass and Hamiltonian mass share one denominator",
            "current_status": "TARGET_IDENTITY_NOT_PARENT_DERIVED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "SMI4098_4_gauss_newton_consequence",
            "claim_piece": "Gauss/Newton source mass",
            "statement": "If surface independence and Hamiltonian equality hold, the exterior weak-field potential uses the same source mass.",
            "formula": "Phi_N=-G_ref M_H/r; a_r=-G_ref M_H/r^2",
            "if_signed": "Newton inverse-square source denominator closes at first order",
            "current_status": "CONDITIONAL_CONSEQUENCE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "theorem_id": "SMI4098_5_failure_identity",
            "claim_piece": "radial/source-hair failure identity",
            "statement": "If the identity fails, the failure is radial/source hair rather than a harmless calibration.",
            "formula": "Delta_Gauss:=B_tau/G_ref-M_H; partial_r ln M_H ~ [N_G int_A d(Pi_M^H J_H)]/M_H",
            "if_signed": "not_applicable",
            "current_status": "BOUND_VECTOR_REQUIRED_IF_UNSIGNED",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def identity_clause_audit_rows() -> List[dict]:
    return [
        {
            "clause_id": "CLA4098_0_PiMH_identity",
            "required_clause": "Pi_M^H is identity/inclusion on fixed C_H^M after source branch selection.",
            "current_status": "PRIVATE_BRANCH_ADOPTED",
            "effect": "kills [d,Pi_M^H]J_H^M as independent operator obstruction",
            "residual_if_missing": "Delta_PiM_operator reopens",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "clause_id": "CLA4098_1_density_qbasic",
            "required_clause": "rho_H dV_H is q-basic from one descended matter+EM Hilbert source action with no source-only weights.",
            "current_status": "THEOREM_CLEAN_BUT_UNSIGNED",
            "effect": "allows source support and M_H integrand to descend through q",
            "residual_if_missing": "E_rho_qbasic; delta_w_species; hidden_marker_source",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "clause_id": "CLA4098_2_regular_support",
            "required_clause": "source support boundary is compact/regular with no vertical birth, death, shell, or readout mask.",
            "current_status": "UNSIGNED_REGULARITY_PREMISE",
            "effect": "turns q-basic density into q-basic W_source and shape moments",
            "residual_if_missing": "E_boundary_birth; Delta_mask; radial/source-shell hair",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "clause_id": "CLA4098_3_MHref_qbasic",
            "required_clause": "M_H_ref=H_tau-H_ref descends through q with source-blind reference subtraction.",
            "current_status": "CONDITIONAL_UNSIGNED",
            "effect": "kills source mass coordinate curvature C_M",
            "residual_if_missing": "D_X H_ref; C_ref; C_units",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "clause_id": "CLA4098_4_Hamiltonian_integrability",
            "required_clause": "H_tau/B_tau is integrable on the same boundary/source-linking class and uses the EH symplectic normalization.",
            "current_status": "TARGET_NOT_DERIVED",
            "effect": "makes B_tau/G_ref a real mass charge rather than a fitted calibration",
            "residual_if_missing": "Delta_symp; C_curl; epsilon_boundary",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "clause_id": "CLA4098_5_Gauss_readout",
            "required_clause": "the closed Hamiltonian/Hilbert charge is the inverse-square Gauss mass in the weak-field exterior.",
            "current_status": "CONDITIONAL_UNSIGNED",
            "effect": "connects source mass to orbital acceleration without circular GM import",
            "residual_if_missing": "Delta_cal; radial_profile; fake Newton derivation risk",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "clause_id": "CLA4098_6_extra_mass_silence",
            "required_clause": "Pi_M^H dJ_extra=0 or every extra mass-channel current is explicitly bounded.",
            "current_status": "LIVE_UNSIGNED",
            "effect": "prevents boundary/bulk/domain/memory/EM/q_loc channels from changing source mass",
            "residual_if_missing": "epsilon_mu; alpha(lambda); R11 source normalization",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def radial_hair_decomposition_rows() -> List[dict]:
    return [
        {
            "residual_id": "RHD4098_0_Delta_Gauss",
            "symbol": "Delta_Gauss",
            "formula": "B_tau/G_ref - M_H[Pi_M^H J_H]",
            "meaning": "Hamiltonian boundary charge and Hilbert source mass are not the same object",
            "zero_route": "delta B_tau = delta int_S Pi_M^H J_H with fixed H_ref and same EH symplectic normalization",
            "bound_route": "Delta_cal; radial_profile; boundary symplectic coefficient",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "residual_id": "RHD4098_1_radial_MH_flux",
            "symbol": "partial_r_ln_MH",
            "formula": "partial_r ln M_H = [N_G int_A d(Pi_M^H J_H)]/M_H",
            "meaning": "projected Hilbert mass changes between exterior linking surfaces",
            "zero_route": "d(Pi_M^H J_H)=0 from density q-basicness, regular support, no extra current and no side flux",
            "bound_route": "radial source-hair profile",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "residual_id": "RHD4098_2_support_drift",
            "symbol": "Delta_support",
            "formula": "D_X W_source + D_X sigma^a + C_domain + C_shape",
            "meaning": "support/shape/source collar drifts after Pi_M^H operator identity is fixed",
            "zero_route": "rho_H dV_H q-basic + regular support + q-basic M_H_ref + Dq(v_X)=0",
            "bound_route": "E_rho_qbasic; E_boundary_birth; E_Dq_source; Delta_mask",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "residual_id": "RHD4098_3_source_density_weight",
            "symbol": "delta_w_species",
            "formula": "S_src=sum_A(1+epsilon_A(X))S_A or T_source=sum_A kappa_A(X)T_A",
            "meaning": "source-only active weights break q-basic density even when field equations look respectable",
            "zero_route": "no-source-only Hom theorem: active source prefactor is empty or one common derivative-free constant",
            "bound_route": "species/source charge and R10/WEP bound rows",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "residual_id": "RHD4098_4_extra_mass_projection",
            "symbol": "Pi_M^H dJ_extra; epsilon_mu",
            "formula": "mu_extra/(G_ref M_H)",
            "meaning": "non-Hilbert boundary/bulk/domain/memory/connection/EM/q_loc currents project into source mass",
            "zero_route": "all extra mass channels vanish/topological/common constant in compact exterior",
            "bound_route": "epsilon_mu; alpha(lambda); gamma/beta/zeta/R11 source rows",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "residual_id": "RHD4098_5_EM_flux_leak",
            "symbol": "Phi_EM_rad; epsilon_EM_extra",
            "formula": "nonstationary/nonminimal Poynting flux outside stationary Hilbert source support",
            "meaning": "EM energy may leave the mass channel if Maxwell stress is not stationary/q-basic/same-frame",
            "zero_route": "stationary minimal q-basic Maxwell stress included in T_H",
            "bound_route": "EM flux/source exchange residual vector",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def gauss_newton_consequence_rows() -> List[dict]:
    return [
        {
            "row_id": "GNC4098_0_if_all_identity_gates_close",
            "condition": "Pi_M^H identity + q-basic density/support + M_H_ref q-basic + Hamiltonian equality + no extra mass current",
            "consequence": "M_H is surface independent and equals the Hamiltonian/Gauss mass.",
            "newton_result": "Phi_N=-G_ref M_H/r and a_r=-G_ref M_H/r^2",
            "status": "CONDITIONAL_FIRST_ORDER_SOURCE_DENOMINATOR_CLOSE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "GNC4098_1_current_state",
            "condition": "Pi_M^H operator identity adopted, but density/support/Hamiltonian equality not parent-signed",
            "consequence": "independent PiM commutator is removed, but source-mass identity is not public.",
            "newton_result": "first-order Newton remains conditional, not claimable",
            "status": "PUBLIC_NEWTON_CLAIM_FALSE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "row_id": "GNC4098_2_if_identity_fails",
            "condition": "Delta_Gauss or partial_r_ln_MH nonzero",
            "consequence": "the failure is observable source/radial hair, not a harmless choice of units.",
            "newton_result": "must bound inverse-square/radial source profile and source-normalization drift",
            "status": "RADIAL_HAIR_BOUND_ROUTE",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def bound_vector_rows() -> List[dict]:
    return [
        {
            "bound_id": "B4098_0_Delta_Gauss",
            "channel": "Hamiltonian/Gauss mass mismatch",
            "symbol": "Delta_Gauss",
            "definition": "B_tau/G_ref - M_H[Pi_M^H J_H]",
            "needed_input": "Hamiltonian equality theorem or numeric/source-ready boundary charge mismatch coefficient",
            "observable_links": "Newton denominator; orbital GM; inverse-square law",
            "current_value": "MISSING_HAMILTONIAN_GAUSS_EQUALITY_OR_DELTA_CAL_BOUND",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "B4098_1_radial_MH",
            "channel": "projected source mass radial hair",
            "symbol": "partial_r_ln_MH",
            "definition": "radial derivative of projected Hilbert mass between linking surfaces",
            "needed_input": "closed Pi_M^H J_H flux theorem or radial profile data/coefficient",
            "observable_links": "inverse-square law; R10; radial acceleration residual",
            "current_value": "MISSING_RADIAL_FLUX_CLOSURE_OR_PROFILE_BOUND",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "B4098_2_density_qbasic",
            "channel": "Hilbert density q-basic failure",
            "symbol": "E_rho_qbasic",
            "definition": "vertical derivative of rho_H dV_H",
            "needed_input": "single descended source action theorem or density-weight bound",
            "observable_links": "WEP source charge; R10 composition; PPN source",
            "current_value": "MISSING_SOURCE_DENSITY_QBASIC_OWNER_OR_BOUND",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "B4098_3_source_weight",
            "channel": "source-only active prefactor",
            "symbol": "delta_w_species",
            "definition": "species/material/source-only weighting of active source density",
            "needed_input": "no-source-only Hom theorem or numeric epsilon_A vector",
            "observable_links": "WEP; R10; source charge",
            "current_value": "MISSING_NO_SOURCE_ONLY_WEIGHT_THEOREM_OR_NUMERIC_EPSILON_A",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "B4098_4_support_boundary",
            "channel": "support regularity failure",
            "symbol": "E_boundary_birth; Delta_mask",
            "definition": "support shell/birth/death/readout-mask term",
            "needed_input": "regular support certificate/no readout mask theorem or boundary coefficient",
            "observable_links": "Gdot; radial hair; orbital source denominator",
            "current_value": "MISSING_REGULAR_SUPPORT_OR_BOUNDARY_SOURCE_BOUND",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "B4098_5_extra_mass_projection",
            "channel": "extra mass projection",
            "symbol": "epsilon_mu; Pi_M^H dJ_extra",
            "definition": "non-Hilbert mass-channel projection after Pi_M^H adoption",
            "needed_input": "zero extra mass theorem or channel coefficient vector",
            "observable_links": "Newton source coupling; gamma/beta/zeta; R11 source normalization; R10 alpha(lambda)",
            "current_value": "MISSING_ZERO_EXTRA_MONOPOLE_OR_CHANNEL_VECTOR_VALUES",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "bound_id": "B4098_6_EM_flux",
            "channel": "EM/Poynting source leakage",
            "symbol": "Phi_EM_rad; epsilon_EM_extra",
            "definition": "radiative/nonminimal EM stress not included in stationary q-basic Hilbert source",
            "needed_input": "stationary minimal EM zero theorem or flux bound",
            "observable_links": "EM stress; clocks; local source coupling; PPN",
            "current_value": "MISSING_STATIONARY_MINIMAL_EM_ZERO_OR_FLUX_BOUND",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def decision_gate_rows() -> List[dict]:
    return [
        {
            "decision_id": "DEC4098_0_PiM",
            "decision": "adopt Pi_M^H identity/inclusion on the typed Hilbert mass-current complex",
            "meaning": "The independent projector commutator is no longer the preferred obstruction.",
            "result": "source-mass identity reduces to support, density, Hamiltonian/Gauss, and extra-current gates",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4098_1_identity",
            "decision": "write Hamiltonian/Gauss equality as the source-mass identity contract",
            "meaning": "Newton source closure requires B_tau/G_ref and M_H[Pi_M^H J_H] to be the same parent object.",
            "result": "Delta_Gauss is the named failure variable",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4098_2_bounds",
            "decision": "retain radial/source-hair bound vector for every unsigned identity clause",
            "meaning": "If the identity fails, it is empirical source hair, not a cosmetic convention.",
            "result": "radial profile, density weight, source support, extra mass and EM flux rows active",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "decision_id": "DEC4098_3_next",
            "decision": "attack no-source-only active prefactor/Hom theorem next",
            "meaning": "The density q-basic theorem is the cleanest upstream gate for support descent and mass identity.",
            "result": "4099 target selected",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def claim_gate_rows() -> List[dict]:
    return [
        {
            "claim_id": "CLAIM4098_0_PiMH",
            "claim": "Pi_M^H identity/inclusion is the preferred private branch and removes the independent operator commutator",
            "allowed": "True",
            "reason": "3559 fixed Pi_M^H on C_H^M; 4098 imports that result into the current 4097 chain.",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4098_1_Hamiltonian_Gauss",
            "claim": "Hamiltonian/Gauss mass equals projected Hilbert source mass",
            "allowed": "False",
            "reason": "B_tau/G_ref = M_H and delta B_tau = delta int Pi_M^H J_H are target identities, not parent-derived.",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4098_2_Newton",
            "claim": "source-normalized Newtonian mechanics is publicly derived",
            "allowed": "False",
            "reason": "density q-basicness, regular support, Hamiltonian equality and extra-mass silence remain unsigned.",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4098_3_no_radial_hair",
            "claim": "radial/source hair is theorem-zero",
            "allowed": "False",
            "reason": "Delta_Gauss, partial_r_ln_MH and density/support residual rows are active until theorem or numeric bounds exist.",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "claim_id": "CLAIM4098_4_local_GR",
            "claim": "local GR/PPN is derived",
            "allowed": "False",
            "reason": "4098 is first-order source denominator work; PPN/R11/EM gates remain downstream.",
            "public_claim": "False",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def next_target_rows() -> List[dict]:
    return [
        {
            "target_id": "NEXT4098_0",
            "next_target": "4099-Y5-R2FR-Hilbert-density-no-source-only-Hom-theorem-or-prefactor-bound.md",
            "script": "scripts/Y5_R2FR_4099_Hilbert_density_no_source_only_Hom_theorem_or_prefactor_bound.py",
            "why": "4098 reduces the mass identity to q-basic Hilbert density/support and Hamiltonian equality. 3561 shows the dangerous countermodel is source-only active prefactors, so the next theorem must forbid or bound them.",
            "priority": "P0",
            "timestamp_utc": TIMESTAMP,
        },
        {
            "target_id": "NEXT4098_1",
            "next_target": "4100-Y5-R2FR-EM-Maxwell-Hilbert-Poynting-same-frame-gate.md",
            "script": "defer_until_density_prefactor_gate",
            "why": "EM/Poynting should be handled once active-source density ownership is stable; otherwise EM stress can be double counted or hidden as flux hair.",
            "priority": "P1",
            "timestamp_utc": TIMESTAMP,
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            "checkpoint": "4098",
            "decision": DECISION,
            "PiMH_operator_identity": "adopted_private_branch",
            "Hamiltonian_Gauss_identity_public": "False",
            "Newton_source_public": "False",
            "radial_source_hair_bound_vector": "active",
            "main_next_gate": "Hilbert_density_no_source_only_Hom_theorem",
            "valid_for_claim": "False",
            "timestamp_utc": TIMESTAMP,
        }
    ]


def write_doc() -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 4098 - PiM/Hamiltonian/Gauss Source-Mass Identity Or Radial-Hair Bound",
                "",
                "## Purpose",
                "",
                "4097 showed first-order Newton follows if the same-frame Hilbert source mass is the same closed object as the Hamiltonian/Gauss mass. 4098 sharpens that identity.",
                "",
                f"- Decision: `{DECISION}`",
                "- Public Newton/source-mass claim: `false`",
                "- Public local-GR/PPN claim: `false`",
                "",
                "## Forward Move",
                "",
                "Adopt the clean 3559 branch:",
                "",
                "```text",
                "Pi_M^H = id/inclusion on C_H^M(W,e_obs,tau)",
                "[d,Pi_M^H] J_H^M = 0",
                "```",
                "",
                "So the live obstruction is no longer a vague projector problem. It is the source-mass identity:",
                "",
                "```text",
                "M_H[S] := N_G int_S Pi_M^H J_H[tau]",
                "B_tau/G_ref = M_H[Pi_M^H J_H]",
                "delta B_tau = delta int_S Pi_M^H J_H",
                "M_H(S2)-M_H(S1)=N_G int_A d(Pi_M^H J_H)",
                "```",
                "",
                "If this closes, `Phi_N=-G_ref M_H/r` and `a_r=-G_ref M_H/r^2` use the same mass denominator as the parent Hilbert source.",
                "",
                "## What Still Blocks A Claim",
                "",
                "- `rho_H dV_H` q-basicness is not parent-signed.",
                "- source support regularity and no readout mask are unsigned.",
                "- `M_H_ref=H_tau-H_ref` is not proved q-basic/source-blind.",
                "- Hamiltonian boundary integrability/equality is a target identity, not yet derived.",
                "- extra mass-channel currents `Pi_M^H dJ_extra` remain live.",
                "",
                "## Bound Route",
                "",
                "If the identity fails, the failure is observable radial/source hair: `Delta_Gauss`, `partial_r_ln_MH`, `E_rho_qbasic`, `delta_w_species`, `E_boundary_birth`, `epsilon_mu`, and EM/Poynting flux leakage.",
                "",
                "## Next Target",
                "",
                "`4099-Y5-R2FR-Hilbert-density-no-source-only-Hom-theorem-or-prefactor-bound.md` should attack the active-source-prefactor countermodel: forbid source-only weights or bound them.",
                "",
                "## Outputs",
                "",
                "- `P8_Y5_R2FR_4098_SOURCE_REGISTER.csv`",
                "- `P8_Y5_R2FR_4098_SOURCE_MASS_IDENTITY_THEOREM.csv`",
                "- `P8_Y5_R2FR_4098_IDENTITY_CLAUSE_AUDIT.csv`",
                "- `P8_Y5_R2FR_4098_RADIAL_HAIR_DECOMPOSITION.csv`",
                "- `P8_Y5_R2FR_4098_GAUSS_NEWTON_CONSEQUENCE.csv`",
                "- `P8_Y5_R2FR_4098_BOUND_VECTOR.csv`",
                "- `P8_Y5_R2FR_4098_DECISION_GATE.csv`",
                "- `P8_Y5_R2FR_4098_CLAIM_GATE.csv`",
                "- `P8_Y5_R2FR_4098_NEXT_TARGET.csv`",
                "- `P8_Y5_R2FR_4098_STATUS.csv`",
                "- `P8_Y5_BRR545_4098_VALIDATION.csv`",
                "",
            ]
        ),
        encoding="utf-8",
    )


def generated_outputs() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4098_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4098_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4098_SOURCE_MASS_IDENTITY_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4098_SOURCE_MASS_IDENTITY_THEOREM.csv",
        "P8_Y5_R2FR_4098_IDENTITY_CLAUSE_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4098_IDENTITY_CLAUSE_AUDIT.csv",
        "P8_Y5_R2FR_4098_RADIAL_HAIR_DECOMPOSITION": SOURCE_DIR / "P8_Y5_R2FR_4098_RADIAL_HAIR_DECOMPOSITION.csv",
        "P8_Y5_R2FR_4098_GAUSS_NEWTON_CONSEQUENCE": SOURCE_DIR / "P8_Y5_R2FR_4098_GAUSS_NEWTON_CONSEQUENCE.csv",
        "P8_Y5_R2FR_4098_BOUND_VECTOR": SOURCE_DIR / "P8_Y5_R2FR_4098_BOUND_VECTOR.csv",
        "P8_Y5_R2FR_4098_DECISION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4098_DECISION_GATE.csv",
        "P8_Y5_R2FR_4098_CLAIM_GATE": SOURCE_DIR / "P8_Y5_R2FR_4098_CLAIM_GATE.csv",
        "P8_Y5_R2FR_4098_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4098_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4098_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4098_STATUS.csv",
    }


def write_outputs() -> Dict[str, Path]:
    outputs = generated_outputs()
    write_csv(outputs["P8_Y5_R2FR_4098_SOURCE_REGISTER"], source_register_rows())
    write_csv(outputs["P8_Y5_R2FR_4098_SOURCE_MASS_IDENTITY_THEOREM"], source_mass_identity_theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4098_IDENTITY_CLAUSE_AUDIT"], identity_clause_audit_rows())
    write_csv(outputs["P8_Y5_R2FR_4098_RADIAL_HAIR_DECOMPOSITION"], radial_hair_decomposition_rows())
    write_csv(outputs["P8_Y5_R2FR_4098_GAUSS_NEWTON_CONSEQUENCE"], gauss_newton_consequence_rows())
    write_csv(outputs["P8_Y5_R2FR_4098_BOUND_VECTOR"], bound_vector_rows())
    write_csv(outputs["P8_Y5_R2FR_4098_DECISION_GATE"], decision_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4098_CLAIM_GATE"], claim_gate_rows())
    write_csv(outputs["P8_Y5_R2FR_4098_NEXT_TARGET"], next_target_rows())
    write_csv(outputs["P8_Y5_R2FR_4098_STATUS"], status_rows())
    write_doc()
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        contains = exists and needle in read_text(path)
        rows.append(
            {
                "check_id": f"VAL4098_SRC_{source_id}",
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
                "check_id": f"VAL4098_CSV_{name}",
                "check": "generated CSV parses and is non-empty",
                "passed": bool_string(ok),
                "detail": detail,
                "timestamp_utc": TIMESTAMP,
            }
        )

    theorem = parse_csv(outputs["P8_Y5_R2FR_4098_SOURCE_MASS_IDENTITY_THEOREM"])
    theorem_text = "\n".join(str(row) for row in theorem)
    theorem_ok = all(
        needle in theorem_text
        for needle in ["Pi_M^H", "[d,Pi_M^H]J_H^M=0", "M_H[S]", "B_tau/G_ref", "Phi_N=-G_ref M_H/r", "Delta_Gauss"]
    )
    rows.append(
        {
            "check_id": "VAL4098_IDENTITY_THEOREM",
            "check": "source-mass identity theorem includes PiMH, Hilbert mass, Hamiltonian/Gauss equality, Newton consequence and failure variable",
            "passed": bool_string(theorem_ok),
            "detail": "requires PiMH, M_H, B_tau, Phi_N and Delta_Gauss",
            "timestamp_utc": TIMESTAMP,
        }
    )

    clauses = parse_csv(outputs["P8_Y5_R2FR_4098_IDENTITY_CLAUSE_AUDIT"])
    clause_text = "\n".join(str(row) for row in clauses)
    clause_ok = all(
        needle in clause_text
        for needle in ["Pi_M^H", "rho_H dV_H", "regular", "M_H_ref", "Hamiltonian", "Gauss", "Pi_M^H dJ_extra"]
    )
    rows.append(
        {
            "check_id": "VAL4098_CLAUSE_AUDIT",
            "check": "clause audit covers PiMH, density, support, MHref, Hamiltonian, Gauss and extra current gates",
            "passed": bool_string(clause_ok),
            "detail": f"clause_rows={len(clauses)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    radial = parse_csv(outputs["P8_Y5_R2FR_4098_RADIAL_HAIR_DECOMPOSITION"])
    radial_text = "\n".join(str(row) for row in radial)
    radial_ok = all(
        needle in radial_text
        for needle in ["Delta_Gauss", "partial_r ln M_H", "Delta_support", "delta_w_species", "epsilon_mu", "Phi_EM_rad"]
    )
    rows.append(
        {
            "check_id": "VAL4098_RADIAL_DECOMPOSITION",
            "check": "radial hair decomposition covers Gauss mismatch, mass flux, support drift, source weights, extra mass and EM flux",
            "passed": bool_string(radial_ok),
            "detail": f"radial_rows={len(radial)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    bounds = parse_csv(outputs["P8_Y5_R2FR_4098_BOUND_VECTOR"])
    bound_text = "\n".join(str(row) for row in bounds)
    bound_ok = all(
        needle in bound_text
        for needle in ["Delta_Gauss", "partial_r_ln_MH", "E_rho_qbasic", "delta_w_species", "E_boundary_birth", "epsilon_mu", "epsilon_EM_extra"]
    )
    rows.append(
        {
            "check_id": "VAL4098_BOUND_VECTOR",
            "check": "bound vector covers Gauss, radial mass, density, source weight, support boundary, extra mass and EM flux rows",
            "passed": bool_string(bound_ok),
            "detail": f"bound_rows={len(bounds)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    consequence = parse_csv(outputs["P8_Y5_R2FR_4098_GAUSS_NEWTON_CONSEQUENCE"])
    consequence_text = "\n".join(str(row) for row in consequence)
    consequence_ok = all(needle in consequence_text for needle in ["Phi_N=-G_ref M_H/r", "PUBLIC_NEWTON_CLAIM_FALSE", "RADIAL_HAIR_BOUND_ROUTE"])
    rows.append(
        {
            "check_id": "VAL4098_GAUSS_NEWTON_CONSEQUENCE",
            "check": "Gauss/Newton consequence separates conditional closure, current false claim and radial-hair fallback",
            "passed": bool_string(consequence_ok),
            "detail": f"consequence_rows={len(consequence)}",
            "timestamp_utc": TIMESTAMP,
        }
    )

    claims = parse_csv(outputs["P8_Y5_R2FR_4098_CLAIM_GATE"])
    no_public = all(row.get("public_claim") == "False" and row.get("valid_for_claim") == "False" for row in claims)
    rows.append(
        {
            "check_id": "VAL4098_NO_PUBLIC_CLAIM",
            "check": "4098 does not promote Hamiltonian/Gauss, Newton, no-radial-hair or local-GR claims",
            "passed": bool_string(no_public),
            "detail": "all claim rows remain private/nonclaim",
            "timestamp_utc": TIMESTAMP,
        }
    )

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4098_NEXT_TARGET"])
    next_text = "\n".join(str(row) for row in next_rows)
    next_ok = "4099-Y5-R2FR-Hilbert-density-no-source-only-Hom-theorem-or-prefactor-bound.md" in next_text
    rows.append(
        {
            "check_id": "VAL4098_NEXT_TARGET",
            "check": "next target attacks Hilbert density no-source-only Hom/prefactor theorem",
            "passed": bool_string(next_ok),
            "detail": "requires 4099 density prefactor target",
            "timestamp_utc": TIMESTAMP,
        }
    )

    output_paths = list(outputs.values()) + [DOC_PATH, SCRIPT_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths)
    formalization_touched = any(is_under(path, FORMALIZATION) for path in output_paths)
    rows.append(
        {
            "check_id": "VAL4098_SCOPE",
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
            "check_id": "VAL4098_SCRIPT_COMPILES",
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
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4098_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)

    print(f"4098 complete: {DECISION}")
    print(f"doc: {DOC_PATH}")
    print(f"csv_dir: {SOURCE_DIR}")
    print(f"validation: {validation_path}")


if __name__ == "__main__":
    main()

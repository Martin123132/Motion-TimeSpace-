from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from mass_flux_gm_common_mode_or_source_profile_gate import (  # noqa: E402
    evaluate_bound_rows,
    evaluate_closure_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4418"
CLAIM_ID = "L-259"
MARKER = "PPC4161_TRANSITION_MASS_FLUX_GM_COMMON_MODE_CLOSURE_OR_SOURCE_PROFILE_BOUND_4418"
PACKET_MARKER = "PPC4161_PACKET_MASS_FLUX_GM_COMMON_MODE_CLOSURE_OR_SOURCE_PROFILE_BOUND_4418"
DECISION = "POISSON_GAUSS_NEWTON_CHAIN_CONDITIONAL_FLUX_AND_COMMON_MODE_SOURCE_GATES_OPEN_NONCLAIM"
NEXT_TARGET = "4419-Y5-R2FR-transition-NoSourceOnlySpeciesSlot-or-topological-mass-current-origin.md"

FORMAL_PATH = FORMAL / "434-PPC4161-transition-mass-flux-GM-common-mode-closure-or-source-profile-bound.md"
DOC_PATH = POST / "4418-Y5-R2FR-transition-mass-flux-GM-common-mode-closure-or-source-profile-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4418_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4418_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4418_DERIVATION_ROWS.csv"
CLOSURE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4418_MASS_FLUX_GM_CLOSURE_INPUT.csv"
CLOSURE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4418_MASS_FLUX_GM_CLOSURE_OUTPUT.csv"
BOUND_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4418_SOURCE_PROFILE_GM_BOUND_INPUT.csv"
BOUND_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4418_SOURCE_PROFILE_GM_BOUND_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4418_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4418_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4418_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4418_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "mass_flux_gm_common_mode_or_source_profile_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4418_transition_mass_flux_GM_common_mode_closure_or_source_profile_bound.py"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4417 = SOURCE_DIR / "P8_Y5_R2FR_4417_NEXT_TARGET.csv"
FORMAL_433 = FORMAL / "433-PPC4161-transition-readout-projector-commutator-zero-or-Kprojective-values.md"
FORMAL_187 = FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md"
POST_3573 = POST / "3573-Y5-R2FR-PiM-flux-closure-Ward-Euler-or-Meff-drift-bound.md"
POST_3499 = POST / "3499-Y5-R2FR-Hamiltonian-source-charge-to-Poisson-Newton-gate-or-GM-transfer-bound.md"
POST_2125 = POST / "2125-Y5-R2FR-GM-common-mode-source-descent-or-Earth-profile-bound-row.md"
POST_2124 = POST / "2124-Y5-R2FR-source-feedback-kernel-normal-form-or-first-bounded-row.md"
POST_3108 = POST / "3108-Y5-R2FR-source-charge-Gauss-bridge-or-GM-calibration-residual-under-AX1090.md"
CSV_3591 = SOURCE_DIR / "P8_Y5_R2FR_3591_GM_TRANSFER_CONTRACT.csv"
CSV_3365 = SOURCE_DIR / "P8_Y5_R2FR_3365_DELTAGM_SPLIT_THEOREM.csv"
CSV_3998 = SOURCE_DIR / "P8_Y5_R2FR_3998_GM_ANTI_BACKFILL_CONTRACT.csv"
CSV_3109 = SOURCE_DIR / "P8_Y5_R2FR_3109_SOURCE_MASS_LOCK_DELTA_GM_ROWS.csv"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4418_00_4417_next": (
        NEXT_4417,
        "4418-Y5-R2FR-transition-mass-flux-GM-common-mode-closure-or-source-profile-bound.md",
        "4417 handoff to mass-flux and GM common-mode closure.",
    ),
    "SRC4418_01_433_formal": (
        FORMAL_433,
        "mass-flux closure `d(Pi_M J_H)=0`",
        "current-chain target after projector Gamma commutator closure.",
    ),
    "SRC4418_02_3573_flux": (
        POST_3573,
        "M_eff(S2)-M_eff(S1)=int_annulus d(Pi_M J_H)",
        "PiM flux closure fork and residual rows.",
    ),
    "SRC4418_03_3499_poisson": (
        POST_3499,
        "EH weak field plus the same Hamiltonian/Hilbert source charge gives Poisson",
        "conditional Poisson/Gauss/Newton theorem chain.",
    ),
    "SRC4418_04_2125_common_mode": (
        POST_2125,
        "NoSourceOnlySpeciesSlot",
        "GM common-mode descent theorem target.",
    ),
    "SRC4418_05_187_formal_newton": (
        FORMAL_187,
        "No observed orbital `GM`",
        "private Poisson/Gauss/Newton readout packet and anti-circularity.",
    ),
    "SRC4418_06_3591_transfer_contract": (
        CSV_3591,
        "GMT3591_8_theorem_result_if_all_close",
        "GM transfer contract rows.",
    ),
    "SRC4418_07_3365_split": (
        CSV_3365,
        "DGM3365_4_promotion_condition",
        "observed GM split and no-absorption promotion condition.",
    ),
    "SRC4418_08_3998_antibackfill": (
        CSV_3998,
        "GMC3998_0_split_law",
        "GM anti-backfill contract.",
    ),
    "SRC4418_09_3109_mass_lock": (
        CSV_3109,
        "SML3109_0",
        "source mass lock and DeltaGM residual rows.",
    ),
    "SRC4418_10_2124_protocol": (
        POST_2124,
        "protocol leakage",
        "source-feedback protocol leakage normal form.",
    ),
    "SRC4418_11_3108_gauss": (
        POST_3108,
        "Gauss/Poisson Bridge",
        "source-charge/Gauss bridge derivation.",
    ),
    "SRC4418_12_gate": (
        GATE_PATH,
        "def evaluate_closure_row",
        "new mass-flux/GM common-mode closure gate.",
    ),
}


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def locate(path: Path, needle: str) -> Tuple[bool, int]:
    body = text(path)
    if not body or needle not in body:
        return False, -1
    return True, body[: body.index(needle)].count("\n") + 1


def bool_true(value: object) -> bool:
    return str(value).strip().lower() == "true"


def rows_from(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        found, line = locate(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": found,
                "line_number": line,
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "FGM4418_0_poisson_gauss_chain",
            "claim": "The weak-field EH plus Hamiltonian/Hilbert source route gives a conditional Poisson/Gauss/Newton chain.",
            "derivation": "If the local exterior operator is EH-only, T_00=rho_H c^2, and the source charge M_H is fixed before orbital readout, then nabla^2 Phi_N=4*pi*G_ref*rho_H, Gauss gives Phi_N=-G_ref M_H/r plus residual multipoles, and the slow geodesic limit gives a_r=-G_ref M_H/r^2.",
            "consequence": "Newton is a real conditional derivation route, not a fitted-GM premise.",
            "status": "POISSON_GAUSS_NEWTON_CHAIN_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "FGM4418_1_flux_closure_law",
            "claim": "Projected source mass is surface-independent iff the PiM flux vanishes.",
            "derivation": "M_eff(S2)-M_eff(S1)=int_annulus d(Pi_M J_H). Thus d(Pi_M J_H)=0 is the exact flux closure; if it fails, dln_Meff_dt, partial_r_ln_mu_obs and Delta_flux become observable residuals.",
            "consequence": "Ward conservation alone is insufficient unless the Hamiltonian mass generator/current is the same projected source current on the same support.",
            "status": "FLUX_IDENTITY_DERIVED_CLOSURE_OPEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "FGM4418_2_common_mode_source_descent",
            "claim": "Measured GM may absorb one universal common mode but not relative source weights.",
            "derivation": "If the parent ordinary matter language has one descended source current and NoSourceOnlySpeciesSlot, all source weights collapse into a calibrated common mode. Without that clause, S_m=sum_A(1+epsilon_A)S_A is a live countermodel.",
            "consequence": "The clean theorem target is NoSourceOnlySpeciesSlot; otherwise source-profile/material/readout vectors must be bounded.",
            "status": "COMMON_MODE_CONDITIONAL_NOSOURCE_SLOT_OPEN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "FGM4418_3_anti_backfill",
            "claim": "Orbital GM cannot be used to define the source mass and then claimed as predicted.",
            "derivation": "The allowed calibration is a universal derivative-silent factor in G_ref M_H. Time, range, species, frame, boundary, non-EH, PPN or profile-dependent residuals are observable and must stay in Delta_Newton_source.",
            "consequence": "This blocks the fake path: M_H := GM_orb/G_ref.",
            "status": "ANTI_BACKFILL_GUARD_ACTIVE",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "FGM4418_4_bound_fallback",
            "claim": "If flux/common-mode closure fails, the fallback is a source/GM residual vector rather than a scalar fudge.",
            "derivation": "The retained vector is Delta_flux, Delta_cal, epsilon_mu, dln_Geff_dt, dln_Meff_dt, partial_r ln mu_obs and non-common source-profile/material response components, evaluated with an absolute/no-cancellation envelope.",
            "consequence": "The next step is a theorem proof of NoSourceOnlySpeciesSlot/topological mass current, or source-profile bound inputs.",
            "status": "SOURCE_GM_BOUND_VECTOR_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
    ]


def closure_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "closure_id": "FGC4418_0_private_poisson_gauss_chain",
            "branch": "private_EH_Hamiltonian_source_Newton_readout",
            "same_projected_source_current": True,
            "stationary_time_generator": False,
            "ward_conservation_signed": False,
            "topological_current_equals_PiJ": False,
            "euler_constraint_origin_signed": False,
            "no_boundary_flux": False,
            "Href_MH_lock": True,
            "same_frame_source_orbit": True,
            "Gref_constant_universal": False,
            "NoSourceOnlySpeciesSlot": False,
            "no_measured_GM_backfill": True,
            "EH_Poisson_operator_ready": True,
            "source_profile_claim_grade": False,
            "parent_policy_signed": False,
            "source_path": str(FORMAL_187),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Poisson/Gauss/Newton readout is conditionally derived in the private branch; flux/common-mode/source-profile gates are still open.",
        },
        {
            "closure_id": "FGC4418_1_flux_identity_fork",
            "branch": "PiM_flux_closure_or_Meff_drift",
            "same_projected_source_current": True,
            "stationary_time_generator": False,
            "ward_conservation_signed": False,
            "topological_current_equals_PiJ": False,
            "euler_constraint_origin_signed": False,
            "no_boundary_flux": False,
            "Href_MH_lock": False,
            "same_frame_source_orbit": True,
            "Gref_constant_universal": False,
            "NoSourceOnlySpeciesSlot": False,
            "no_measured_GM_backfill": True,
            "EH_Poisson_operator_ready": True,
            "source_profile_claim_grade": False,
            "parent_policy_signed": False,
            "source_path": str(POST_3573),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Stokes/annulus identity is derived; Ward/topological/Euler route remains unsigned.",
        },
        {
            "closure_id": "FGC4418_2_common_mode_source_theorem_target",
            "branch": "NoSourceOnlySpeciesSlot_common_mode",
            "same_projected_source_current": True,
            "stationary_time_generator": False,
            "ward_conservation_signed": False,
            "topological_current_equals_PiJ": False,
            "euler_constraint_origin_signed": False,
            "no_boundary_flux": False,
            "Href_MH_lock": False,
            "same_frame_source_orbit": True,
            "Gref_constant_universal": True,
            "NoSourceOnlySpeciesSlot": False,
            "no_measured_GM_backfill": True,
            "EH_Poisson_operator_ready": True,
            "source_profile_claim_grade": False,
            "parent_policy_signed": False,
            "source_path": str(POST_2125),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Common-mode descent theorem is exact conditional but NoSourceOnlySpeciesSlot is not parent-signed.",
        },
        {
            "closure_id": "FGC4418_3_future_public_contract",
            "branch": "future_flux_common_mode_public_Newton_contract",
            "same_projected_source_current": True,
            "stationary_time_generator": True,
            "ward_conservation_signed": True,
            "topological_current_equals_PiJ": True,
            "euler_constraint_origin_signed": True,
            "no_boundary_flux": True,
            "Href_MH_lock": True,
            "same_frame_source_orbit": True,
            "Gref_constant_universal": True,
            "NoSourceOnlySpeciesSlot": True,
            "no_measured_GM_backfill": True,
            "EH_Poisson_operator_ready": True,
            "source_profile_claim_grade": True,
            "parent_policy_signed": True,
            "source_path": str(POST_3499),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Full first-order Newton transfer contract; nonclaim because current corpus has not signed it as a parent theorem.",
        },
    ]


def bound_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "FGB4418_0_Delta_Newton_source_vector",
            "residual": "Delta_Newton_source",
            "arena": "NEWTON_R10_WEP_PPN_ORBIT",
            "normal_form": "Delta_Newton_source=(1+dKC)(1+epsilon_M)(1+dkappa)(1+dellJ)(1+Delta_flux)(1+epsilon_mu)(1+Delta_cal)-1",
            "dln_Meff_dt": "SCHEMA_DLN_MEFF_DT_REQUIRED",
            "partial_r_ln_mu_obs": "SCHEMA_PARTIAL_R_LN_MU_OBS_REQUIRED",
            "Delta_flux": "SCHEMA_DELTA_FLUX_REQUIRED",
            "Delta_cal": "SCHEMA_DELTA_CAL_REQUIRED",
            "epsilon_mu": "SCHEMA_EPSILON_MU_REQUIRED",
            "Gref_derivative": "SCHEMA_D_LN_GREF_REQUIRED",
            "source_profile_value": "SCHEMA_SOURCE_PROFILE_VECTOR_REQUIRED",
            "material_response": "SCHEMA_MATERIAL_READOUT_RESPONSE_REQUIRED",
            "comparator_bound": "SCHEMA_ARENA_BOUNDS_REQUIRED",
            "source_path": str(POST_3499),
            "no_cancellation_guard": True,
            "official_numeric_source": False,
            "parent_coefficient_source": False,
            "input_valid": False,
            "valid_for_claim": False,
            "issues": "Residual vector is executable symbolically; none of the component values are sourced as claim-grade inputs.",
        },
        {
            "bound_id": "FGB4418_1_flux_drift_radial_rows",
            "residual": "dln_Meff_dt;partial_r_ln_mu_obs;Delta_flux",
            "arena": "GDOT_RADIAL_R10_SOURCE_HAIR",
            "normal_form": "D_X ln mu_obs = D_X ln G_eff + D_X ln M_eff + D_X ln(1+epsilon_mu)",
            "dln_Meff_dt": "SCHEMA_DLN_MEFF_DT_REQUIRED",
            "partial_r_ln_mu_obs": "SCHEMA_PARTIAL_R_LN_MU_OBS_REQUIRED",
            "Delta_flux": "SCHEMA_ANNULUS_FLUX_INTEGRAL_REQUIRED",
            "Delta_cal": "SCHEMA_GAUSS_CAL_REQUIRED",
            "epsilon_mu": "SCHEMA_MU_EXTRA_REQUIRED",
            "Gref_derivative": "SCHEMA_D_LN_GEFF_REQUIRED",
            "source_profile_value": "SCHEMA_SOURCE_SUPPORT_REQUIRED",
            "material_response": "SCHEMA_NOT_PRIMARY_FOR_FLUX",
            "comparator_bound": "SCHEMA_GDOT_RADIAL_R10_BOUNDS_REQUIRED",
            "source_path": str(POST_3573),
            "no_cancellation_guard": True,
            "official_numeric_source": False,
            "parent_coefficient_source": False,
            "input_valid": False,
            "valid_for_claim": False,
            "issues": "Flux/drift rows are ready as identities; no theorem-zero or numeric bounds are supplied.",
        },
        {
            "bound_id": "FGB4418_2_source_profile_common_mode",
            "residual": "epsilon_sigma_source_GM",
            "arena": "SOURCE_PROFILE_WEP_R10_PPN",
            "normal_form": "source residual zero iff NoSourceOnlySpeciesSlot plus one descended matter current; else bound non-common profile vector times material/readout response",
            "dln_Meff_dt": "SCHEMA_NOT_PRIMARY_FOR_PROFILE",
            "partial_r_ln_mu_obs": "SCHEMA_PROFILE_RADIAL_WEIGHTING_REQUIRED",
            "Delta_flux": "SCHEMA_SOURCE_SUPPORT_FLUX_REQUIRED",
            "Delta_cal": "SCHEMA_COMMON_MODE_CALIBRATION_REQUIRED",
            "epsilon_mu": "SCHEMA_NONCOMMON_SOURCE_VECTOR_REQUIRED",
            "Gref_derivative": "SCHEMA_CONSTANT_GREF_GUARD_REQUIRED",
            "source_profile_value": "SCHEMA_PROFILE_WEIGHTED_EARTH_VECTOR_REQUIRED",
            "material_response": "SCHEMA_TEST_BODY_MATERIAL_RESPONSE_REQUIRED",
            "comparator_bound": "SCHEMA_WEP_R10_PPN_BOUNDS_REQUIRED",
            "source_path": str(POST_2125),
            "no_cancellation_guard": True,
            "official_numeric_source": False,
            "parent_coefficient_source": False,
            "input_valid": False,
            "valid_for_claim": False,
            "issues": "Bulk Earth DD context is available but not profile/worldtube weighted; parent basis map and material response are missing.",
        },
        {
            "bound_id": "FGB4418_3_anti_backfill_guard",
            "residual": "epsilon_GM_backfill_forbidden",
            "arena": "ORBITAL_GM_CALIBRATION_POLICY",
            "normal_form": "mu_obs=G0 M_H_ref(1+delta_cal+delta_range+delta_frame+delta_PPN+delta_boundary+delta_nonEH)",
            "dln_Meff_dt": "SCHEMA_COMPONENT_VECTOR_REQUIRED",
            "partial_r_ln_mu_obs": "SCHEMA_COMPONENT_VECTOR_REQUIRED",
            "Delta_flux": "SCHEMA_COMPONENT_VECTOR_REQUIRED",
            "Delta_cal": "SCHEMA_COMPONENT_VECTOR_REQUIRED",
            "epsilon_mu": "SCHEMA_COMPONENT_VECTOR_REQUIRED",
            "Gref_derivative": "SCHEMA_COMPONENT_VECTOR_REQUIRED",
            "source_profile_value": "SCHEMA_COMPONENT_VECTOR_REQUIRED",
            "material_response": "SCHEMA_COMPONENT_VECTOR_REQUIRED",
            "comparator_bound": "SCHEMA_PER_ARENA_BOUNDS_REQUIRED",
            "source_path": str(CSV_3998),
            "no_cancellation_guard": True,
            "official_numeric_source": False,
            "parent_coefficient_source": False,
            "input_valid": False,
            "valid_for_claim": False,
            "issues": "Guard blocks using orbital GM as source definition; not a numeric pass row.",
        },
    ]


def claim_gate_rows(
    closure_output: List[Mapping[str, str]],
    bound_output: List[Mapping[str, str]],
) -> List[Dict[str, object]]:
    closures = {row["closure_id"]: row for row in closure_output}
    bounds = {row["bound_id"]: row for row in bound_output}
    no_claims = not any(bool_true(row.get("valid_for_claim")) for row in closure_output + bound_output)
    return [
        {
            "gate_id": "CG4418_0_poisson_gauss_chain",
            "claim": "conditional Poisson/Gauss/Newton chain is written",
            "passed": closures["FGC4418_0_private_poisson_gauss_chain"].get("poisson_chain_ready") == "True",
            "valid_for_claim": False,
            "detail": "EH 00 + same source charge gives conditional Newton readout.",
        },
        {
            "gate_id": "CG4418_1_flux_closure",
            "claim": "d(Pi_M J_H)=0 is parent-derived",
            "passed": False,
            "valid_for_claim": False,
            "detail": "Ward/topological/Euler routes are written but unsigned.",
        },
        {
            "gate_id": "CG4418_2_common_mode_source",
            "claim": "NoSourceOnlySpeciesSlot and common-mode source descent are parent-signed",
            "passed": False,
            "valid_for_claim": False,
            "detail": "relative source-weight countermodel remains live.",
        },
        {
            "gate_id": "CG4418_3_anti_backfill_guard",
            "claim": "orbital GM backfill is forbidden",
            "passed": closures["FGC4418_0_private_poisson_gauss_chain"].get("no_measured_GM_backfill") == "True",
            "valid_for_claim": False,
            "detail": "measured GM cannot define M_H and then be claimed as predicted.",
        },
        {
            "gate_id": "CG4418_4_bound_vector_schema",
            "claim": "source/GM residual vector schema is ready",
            "passed": bounds["FGB4418_0_Delta_Newton_source_vector"].get("current_status")
            == "SOURCE_GM_BOUND_SCHEMA_READY_VALUES_MISSING_NONCLAIM",
            "valid_for_claim": False,
            "detail": "Delta_Newton_source vector is ready, but component values are missing.",
        },
        {
            "gate_id": "CG4418_5_Newton_local_GR_claim",
            "claim": "Newton/local-GR source bridge is public",
            "passed": False,
            "valid_for_claim": False,
            "detail": "flux, common-mode source, Href/MH, residual vector and second-order PPN are still open.",
        },
        {
            "gate_id": "CG4418_6_no_claim_outputs",
            "claim": "no generated row is claim-ready",
            "passed": no_claims,
            "valid_for_claim": False,
            "detail": "4418 is a disciplined conditional theorem/fallback checkpoint.",
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4418_0",
            "decision": DECISION,
            "summary": "4418 fuses the current projector branch with the older Poisson/Gauss/Newton and GM-source ledgers. The first-order Newton readout is a real conditional theorem: EH weak field plus the same Hamiltonian/Hilbert source charge gives Poisson, Gauss and inverse-square readout without using orbital GM as input. It is not claimable because d(Pi_M J_H)=0, NoSourceOnlySpeciesSlot/common-mode source descent, H_ref/M_H, constant G_ref and the Delta_Newton residual vector remain unsigned or unfilled.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "claim_id": CLAIM_ID,
            "marker": MARKER,
            "decision": DECISION,
            "best_result": "conditional_Poisson_Gauss_Newton_chain_imported_and_anti_backfill_guard_active",
            "still_missing": "d_PiM_JH_flux_closure; NoSourceOnlySpeciesSlot; topological_mass_current_origin; Href_MH_lock; constant_Gref; source_profile_material_response_values; Delta_Newton_component_bounds",
            "valid_for_claim": False,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4418_0",
            "target": NEXT_TARGET,
            "objective": "Try the two clean theorem routes together: prove NoSourceOnlySpeciesSlot in the parent object language and construct a parent-owned closed topological mass current equal to Pi_M J_H on shell.",
            "derive_first": "show ordinary matter admits only one descended source current and that the projected Hamiltonian mass current is closed by parent topology/Ward/Euler structure on the same support.",
            "fallback": "turn NoSourceOnlySpeciesSlot into an explicit closure clause and fill source-profile/material/GM residual rows with claim-grade sources.",
            "avoid": "using orbital GM as source input; using bulk Earth composition as profile vector; counting Ward conservation alone as flux closure; hiding relative source weights in fitted G.",
            "valid_for_claim": False,
        }
    ]


def markdown_table(rows: Iterable[Mapping[str, object]]) -> str:
    materialized = [dict(row) for row in rows]
    if not materialized:
        return ""
    headers: List[str] = []
    for row in materialized:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in materialized:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    source_register: List[Dict[str, object]],
    closure_output: List[Dict[str, str]],
    bound_output: List[Dict[str, str]],
    claim_gates: List[Dict[str, object]],
) -> str:
    return f"""# 434 PPC4161 transition: mass-flux GM common-mode closure or source-profile bound

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4418 banks the good news without smuggling the missing source physics:

- The first-order Poisson/Gauss/Newton readout is a real conditional theorem inside the private EH/Hamiltonian source branch.
- Orbital `GM` is not used as a source definition; the anti-backfill guard is active.
- The flux closure `d(Pi_M J_H)=0` is still not parent-derived; Ward/topological/Euler routes are named but unsigned.
- The GM common-mode theorem is reduced to `NoSourceOnlySpeciesSlot`; without it, relative source-weight countermodels remain live.
- The fallback is the explicit `Delta_Newton_source` / source-profile residual vector, not a scalar fudge.

## Source Register

{markdown_table(source_register)}

## Derivation Rows

{markdown_table(rows_from(DERIVATION_ROWS))}

## Flux / GM Closure Gate

{markdown_table(closure_output)}

## Source Profile / GM Bound Gate

{markdown_table(bound_output)}

## Claim Gates

{markdown_table(claim_gates)}

## Decision

{markdown_table(decision_rows())}

## Next Target

{markdown_table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4418 - Y5/R2FR transition mass-flux GM common-mode closure or source-profile bound

Private checkpoint for the local Newton/local-GR route.

Main result: the Poisson/Gauss/Newton bridge is conditionally real and anti-circular: no observed orbital `GM` is used to define the source charge. But Newton is not claimed. The live gates are `d(Pi_M J_H)=0`, `NoSourceOnlySpeciesSlot`, H_ref/M_H, constant G_ref and source-profile/material response values.

- Formal mirror: `{FORMAL_PATH}`
- Gate: `{GATE_PATH}`
- Generator: `{GENERATOR_PATH}`
- Validation: `{VALIDATION_PATH}`
- Next: `{NEXT_TARGET}`
"""


def upsert_marked_section(path: Path, marker: str, section: str) -> None:
    start = f"<!-- {marker}_START -->"
    end = f"<!-- {marker}_END -->"
    body = text(path)
    block = f"\n{start}\n{section.rstrip()}\n{end}\n"
    if start in body and end in body:
        prefix = body[: body.index(start)]
        suffix = body[body.index(end) + len(end) :]
        write_text(path, prefix.rstrip() + block + suffix.lstrip("\n"))
    else:
        write_text(path, body.rstrip() + "\n" + block)


def update_claims_register() -> None:
    fieldnames = ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk"]
    rows: List[Dict[str, str]] = []
    if CLAIMS_PATH.exists():
        with CLAIMS_PATH.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames:
                fieldnames = reader.fieldnames
            rows = [row for row in reader if row.get("claim_id") != CLAIM_ID]
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "sector": "local_gr",
        "claim": "4418 imports the conditional Poisson/Gauss/Newton source bridge into the current PPC4161 chain. EH weak field plus the same Hamiltonian/Hilbert source charge gives a non-circular first-order Newton readout if flux closure, common-mode source descent, H_ref/M_H, constant G_ref and residual silence close. Orbital GM backfill is explicitly forbidden. The branch remains nonclaim because d(Pi_M J_H)=0, NoSourceOnlySpeciesSlot/topological mass-current origin, source-profile/material response and Delta_Newton residual values are open.",
        "current_evidence": "4418 source register, derivation rows, flux/GM closure output, source-profile/GM bound output, claim gates, decision, status, next target and validation CSV.",
        "evidence": "4418 source register, derivation rows, flux/GM closure output, source-profile/GM bound output, claim gates, decision, status, next target and validation CSV.",
        "status": "conditional_Poisson_Newton_chain_imported_flux_common_mode_source_open_nonclaim",
        "next_test": "Prove NoSourceOnlySpeciesSlot and a topological/Ward/Euler closed mass current equal to Pi_M J_H, or fill source-profile/GM residual rows.",
        "next_action": "Prove NoSourceOnlySpeciesSlot and a topological/Ward/Euler closed mass current equal to Pi_M J_H, or fill source-profile/GM residual rows.",
        "key_risk": "Using orbital GM as source input, counting Ward conservation alone as mass-flux closure, or hiding relative source weights in fitted G.",
        "risk": "Using orbital GM as source input, counting Ward conservation alone as mass-flux closure, or hiding relative source weights in fitted G.",
    }
    for key in claim_row:
        if key not in fieldnames:
            fieldnames.append(key)
    rows.append({key: claim_row.get(key, "") for key in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = """## 4418 local spine update: Newton bridge is conditional, not fitted

4418 imports the Poisson/Gauss/Newton source bridge into the current PPC4161 chain. The good result is real: EH weak-field source normalization plus the same Hamiltonian/Hilbert source charge gives the first-order inverse-square readout without using observed orbital `GM` as an input. The claim still does not fire because `d(Pi_M J_H)=0`, `NoSourceOnlySpeciesSlot`, H_ref/M_H, constant G_ref, source-profile/material response and the `Delta_Newton_source` residual vector are open."""
    packet_section = """## 4418 packet update: no GM backfill

The Newton route is now anti-circular: measured orbital `GM` is a downstream test, not a source definition. Next clean shot: prove both source common-mode (`NoSourceOnlySpeciesSlot`) and a closed projected mass current equal to `Pi_M J_H`; otherwise fill source-profile/GM residual rows."""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    source_register = rows_from(SOURCE_REGISTER)
    closure_output = rows_from(CLOSURE_OUTPUT)
    bound_output = rows_from(BOUND_OUTPUT)
    claim_gates = rows_from(CLAIM_GATES)
    closures = {row["closure_id"]: row for row in closure_output}
    bounds = {row["bound_id"]: row["current_status"] for row in bound_output}
    no_claims = not any(bool_true(row.get("valid_for_claim")) for row in closure_output + bound_output + claim_gates)
    checks = [
        ("VAL4418_0_sources_exist", all(row["path_exists"] == "True" for row in source_register), "every cited source path exists"),
        ("VAL4418_1_source_needles_found", all(row["needle_found"] == "True" for row in source_register), "every cited source needle was found"),
        (
            "VAL4418_2_poisson_chain_ready",
            closures["FGC4418_0_private_poisson_gauss_chain"].get("poisson_chain_ready") == "True",
            "conditional Poisson/Gauss/Newton chain is ready",
        ),
        (
            "VAL4418_3_flux_closure_open",
            closures["FGC4418_1_flux_identity_fork"].get("flux_closure_ready") == "False",
            "flux closure remains open, not smuggled from Ward",
        ),
        (
            "VAL4418_4_common_mode_open",
            closures["FGC4418_2_common_mode_source_theorem_target"].get("common_mode_ready") == "False",
            "NoSourceOnlySpeciesSlot/common-mode source descent remains open",
        ),
        (
            "VAL4418_5_future_contract_nonclaim",
            closures["FGC4418_3_future_public_contract"].get("current_status")
            == "MASS_FLUX_GM_CONTRACT_READY_NONCLAIM",
            "future full contract remains nonclaim",
        ),
        (
            "VAL4418_6_delta_newton_schema",
            bounds.get("FGB4418_0_Delta_Newton_source_vector")
            == "SOURCE_GM_BOUND_SCHEMA_READY_VALUES_MISSING_NONCLAIM",
            "Delta_Newton source vector schema ready but values missing",
        ),
        (
            "VAL4418_7_profile_schema",
            bounds.get("FGB4418_2_source_profile_common_mode")
            == "SOURCE_GM_BOUND_SCHEMA_READY_VALUES_MISSING_NONCLAIM",
            "source profile/common-mode bound schema ready but values missing",
        ),
        ("VAL4418_8_no_claim_outputs", no_claims, "no generated gate row is valid for claim"),
        ("VAL4418_9_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-259"),
        ("VAL4418_10_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4418_11_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4418_12_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4418_13_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4418_14_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4418_15_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "passed": bool(passed),
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(CLOSURE_INPUT, closure_input_rows())
    write_csv(BOUND_INPUT, bound_input_rows())
    write_csv(CLOSURE_OUTPUT, evaluate_closure_rows(CLOSURE_INPUT))
    write_csv(BOUND_OUTPUT, evaluate_bound_rows(BOUND_INPUT))
    closure_output = rows_from(CLOSURE_OUTPUT)
    bound_output = rows_from(BOUND_OUTPUT)
    claim_gates = claim_gate_rows(closure_output, bound_output)
    write_csv(CLAIM_GATES, claim_gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    source_register = rows_from(SOURCE_REGISTER)
    write_text(FORMAL_PATH, build_doc(source_register, closure_output, bound_output, claim_gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(
        VALIDATION_PATH,
        validation_rows(
            {
                "formal": FORMAL_PATH,
                "post": DOC_PATH,
                "next": NEXT_CSV,
            }
        ),
    )


if __name__ == "__main__":
    main()

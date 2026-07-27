from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4126-Y5-R2FR-parent-source-normalization-ward-identity-or-beta-common-bound-fill.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_PARENT_SOURCE_NORMALIZATION_WARD_OR_BETA_COMMON_BOUND_FILL_4126"
CHECKPOINT_ID = "4126"
DECISION = "WARD_OBSTRUCTION_DERIVED_PARENT_ZERO_UNSIGNED_BETA_COMMON_BOUNDS_FILLED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4126_00_4125_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4125_NEXT_TARGET.csv",
        "4126-Y5-R2FR-parent-source-normalization-ward-identity-or-beta-common-bound-fill.md",
        "4125 selected this Ward/source-normalization fork.",
    ),
    "SRC4126_01_4125_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4125_STATUS.csv",
        "COMMON_BETA_ZERO_UNSIGNED_SOURCE_NORMALIZATION_RUNNER_FILLED",
        "Current-chain common beta remains live but mapped to arenas.",
    ),
    "SRC4126_02_4125_identity": (
        SOURCE_DIR / "P8_Y5_R2FR_4125_COMMON_BETA_IDENTITY.csv",
        "EM_common_beta",
        "4125 includes EM common-mode coupling in beta_common maps.",
    ),
    "SRC4126_03_4125_runner": (
        SOURCE_DIR / "P8_Y5_R2FR_4125_SOURCE_NORMALIZATION_RUNNER_ROWS.csv",
        "NO_TUNED_CANCELLATION_ALLOWED",
        "Current no-cancellation and WEP-null guard.",
    ),
    "SRC4126_04_3640_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3640_STATUS.csv",
        "WARD_FORM_DERIVED_PARENT_ZERO_UNSIGNED_BETA_COMMON_BOUNDS_FILLED",
        "Older Ward scaffold to upgrade onto current chain.",
    ),
    "SRC4126_05_source_law_4096": (
        SOURCE_DIR / "P8_Y5_R2FR_4096_SOURCE_NORMALIZATION_LAW.csv",
        "SNL4096_1_constant_G_ref",
        "Clarifies that G_ref is calibrated/universal, not numerically derived here.",
    ),
    "SRC4126_06_em_interface_4096": (
        SOURCE_DIR / "P8_Y5_R2FR_4096_EM_POYNTING_INTERFACE.csv",
        "EM4096_1_Poynting_exchange",
        "EM/Poynting source accounting guard.",
    ),
    "SRC4126_07_source_spine_4106": (
        SOURCE_DIR / "P8_Y5_R2FR_4106_SOURCE_COUPLING_SPINE.csv",
        "SCS4106_6_EM_Poynting_once",
        "Source-coupling spine includes EM/Poynting once-only theorem.",
    ),
    "SRC4126_08_em_spine_4112": (
        SOURCE_DIR / "P8_Y5_R2FR_4112_EM_POYNTING_HODGE_SCREEN_SPINE.csv",
        "EMS4112_5_source_owner_packet",
        "EM Hodge/source owner packet and coupling throat.",
    ),
    "SRC4126_09_mass_identity_4098": (
        SOURCE_DIR / "P8_Y5_R2FR_4098_SOURCE_MASS_IDENTITY_THEOREM.csv",
        "SMI4098_3_hamiltonian_equality",
        "Hamiltonian boundary mass/Hilbert mass identity target.",
    ),
    "SRC4126_10_source_descent_4121": (
        SOURCE_DIR / "P8_Y5_R2FR_4121_SOURCE_READOUT_DESCENT_THEOREM.csv",
        "SDT4121_2_point_particle_source",
        "Point-source action exposes mass/readout/EM source derivative.",
    ),
    "SRC4126_11_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4126_parent_source_normalization_ward_identity_or_beta_common_bound_fill.py",
        "Reproducible generator for this 4126 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        row = row_base()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(contains(path, needle)),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def ward_identity_rows() -> List[dict]:
    data = [
        (
            "WID4126_0_observed_source_scalar",
            "mu_obs_common",
            "mu_obs_common := G_ref M_H^dress (1+epsilon_mu)",
            "G_ref is the single calibrated GR/Newton coupling constant; MTS need not derive its numeric value, but must derive that it is universal and derivative-free in the local branch.",
            "definition locks Newton/GR source normalization to one object before orbital fitting",
            "DEFINITION_LOCK",
        ),
        (
            "WID4126_1_hilbert_mass_charge",
            "M_H^dress",
            "M_H^dress[S,tau,e_obs] := N_G int_S Pi_M^H J_H_total[tau,e_obs]",
            "J_H_total = J_matter + J_EM + J_Poynting + J_binding + exact improvements, counted once in the same observed coframe.",
            "Poynting/EM is inside the source charge, not an optional later patch",
            "DRESSED_SOURCE_CHARGE_FORM",
        ),
        (
            "WID4126_2_variation_identity",
            "beta_common_A",
            "beta_common_A := A_N ln mu_obs_common = A_N ln G_ref + A_N ln M_H^dress + A_N ln(1+epsilon_mu)",
            "A_N is X_N or Z_N. This is exact by logarithmic differentiation and is the clean coupling residual.",
            "turns coupling into a computable Ward derivative rather than a free coefficient",
            "EXACT_LOG_DERIVATIVE",
        ),
        (
            "WID4126_3_surface_variation",
            "A_N ln M_H^dress",
            "A_N ln M_H^dress = A_N ln N_G + (int_S A_N(Pi_M^H J_H_total)+int_{A_N S} Pi_M^H J_H_total)/int_S Pi_M^H J_H_total",
            "The numerator splits into projector, Hilbert-current, coframe/connection, EM/Poynting, boundary, and support/homology terms.",
            "gives the actual obstruction vector that must vanish or be bounded",
            "WARD_OBSTRUCTION_EXTRACTED",
        ),
        (
            "WID4126_4_parent_ward_zero",
            "beta_common_A = 0",
            "If A_N is a parent gauge/vertical generator of q and every object in mu_obs_common is q-owned or pure calibration gauge, then A_N ln mu_obs_common = 0.",
            "This is not an axiom: it follows only when G_ref, N_G, Pi_M^H, J_H_total, e_obs, tau, boundary/reference data, and epsilon_mu all descend through q or are Ward-gauge invariant.",
            "sufficient route to local Newton/GR source silence",
            "CONDITIONAL_PARENT_WARD_ZERO",
        ),
        (
            "WID4126_5_newton_gr_consequence",
            "local source limit",
            "beta_common_A=0 plus partial_t ln mu_obs=0 and partial_r ln mu_obs=0 gives mu_obs=G_ref M_H^dress with no finite-range/source hair; Poisson/Gauss then yields Phi_N=-G_ref M_H^dress/r.",
            "The numerical value of G_ref remains empirical exactly as in GR; the derivation target is universality, source ownership, and absence of local derivative hair.",
            "connects the source-coupling problem directly to Newton/GR reduction",
            "LOCAL_NEWTON_GR_CONSEQUENCE_CONDITIONAL",
        ),
    ]
    rows: List[dict] = []
    for identity_id, symbol, equation, derivation, consequence, status in data:
        row = row_base()
        row.update(
            {
                "identity_id": identity_id,
                "symbol": symbol,
                "equation": equation,
                "derivation": derivation,
                "consequence": consequence,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def residual_decomposition_rows() -> List[dict]:
    data = [
        (
            "WR4126_0_beta_G",
            "beta_G",
            "A_N ln G_ref",
            "global coupling superselection / constant calibrated GR coupling",
            "zero if G_ref is a fixed parent constant or pure unit calibration with no local derivative",
            "Gdot, PPN source normalization, clock common drift",
        ),
        (
            "WR4126_1_beta_NG",
            "beta_NG",
            "A_N ln N_G",
            "normalization convention for Hilbert source mass",
            "zero if N_G is fixed by the same calibration as G_ref and not a field/readout",
            "absolute mass normalization and source calibration",
        ),
        (
            "WR4126_2_beta_measure",
            "beta_measure",
            "A_N ln sqrt(sigma_S) or equivalent surface/source measure",
            "surface measure and homology class of the source-linking charge",
            "zero if source surface/support is fixed or descends as q-owned homology data",
            "radial/orbital source hair",
        ),
        (
            "WR4126_3_beta_coframe",
            "beta_coframe",
            "A_N e_obs acting inside J_H_total[tau,e_obs]",
            "rods, clocks, matter stress, and orbit readout use one observed coframe",
            "zero if e_obs=e_bar(q(Phi)) and A_N is vertical to q",
            "PPN preferred-frame, clock, orbital readout",
        ),
        (
            "WR4126_4_beta_connection",
            "beta_connection",
            "A_N nabla_obs and connection terms in stress/charge conservation",
            "Levi-Civita/covariant derivative ownership of the same observed geometry",
            "zero if connection is the q-owned LC connection of e_obs/g_obs with no independent representative channel",
            "PPN, conservation, source current closure",
        ),
        (
            "WR4126_5_beta_boundary",
            "beta_boundary",
            "A_N Q_boundary - i_{A_N} theta_boundary",
            "Hamiltonian/reference subtraction and boundary symplectic flux",
            "zero if boundary/reference data are fixed or Ward-invariant",
            "Gauss/Newton bridge, H_tau/M_H equality",
        ),
        (
            "WR4126_6_beta_source_matter",
            "beta_source_matter",
            "int_S Pi_M^H A_N J_matter",
            "ordinary matter source current",
            "zero if matter action descends through q and no source-mass representative dependence remains",
            "R10/R11 source coupling, WEP-null common mode",
        ),
        (
            "WR4126_7_beta_source_EM",
            "beta_source_EM",
            "int_S Pi_M^H A_N(J_EM + J_Poynting)",
            "Maxwell/Hodge/current/Poynting source contribution",
            "zero if EM action, Hodge star, current, orientation, and Poynting readout share the same q-owned frame and are counted once",
            "EM common mode, Maxwell stress, fine-structure/source calibration",
        ),
        (
            "WR4126_8_beta_projection",
            "beta_projection",
            "int_S [A_N,Pi_M^H] J_H_total",
            "projector/readout derivative",
            "zero if Pi_M^H is identity/inclusion on the typed Hilbert mass-current complex or is q-owned",
            "radial/source-hair and R10/R11 projection",
        ),
        (
            "WR4126_9_beta_calibration",
            "beta_calibration",
            "A_N ln(1+epsilon_mu)",
            "unit/readout calibration residual",
            "zero if calibration is pure gauge and has no time/range/species/EM derivative",
            "absolute G, clock common mode, finite-range source calibration",
        ),
    ]
    rows: List[dict] = []
    for residual_id, symbol, formula, meaning, zero_rule, observable_link in data:
        row = row_base()
        row.update(
            {
                "residual_id": residual_id,
                "symbol": symbol,
                "formula": formula,
                "meaning": meaning,
                "zero_rule": zero_rule,
                "master_sum": "beta_common_A = beta_G + beta_NG + beta_measure + beta_coframe + beta_connection + beta_boundary + beta_source_matter + beta_source_EM + beta_projection + beta_calibration",
                "observable_link": observable_link,
                "status": "ZERO_REQUIRED_OR_BOUND",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def parent_zero_signature_rows() -> List[dict]:
    data = [
        (
            "PZS4126_0_vertical_generator",
            "A_N in ker(Dq) for A in {X,Z}",
            "4120/4121 give conditional chain-rule route; current 4125 keeps beta_common live",
            "required",
            "NOT_PARENT_SIGNED_CURRENTLY",
        ),
        (
            "PZS4126_1_same_frame_source",
            "g_obs, e_obs, tau, rods, clocks, orbit readout, and matter stress all descend through the same q-owned observed frame",
            "4097/4106/4121 make this the non-cheat branch",
            "required",
            "PARTIAL_CONTRACT_NOT_FINAL_ZERO",
        ),
        (
            "PZS4126_2_hilbert_charge_owner",
            "M_H^dress is the source charge before orbital readout and is not imported from fitted GM",
            "4098 defines the charge and target equality but does not parent-sign the Hamiltonian equality",
            "required",
            "TARGET_IDENTITY_UNSIGNED",
        ),
        (
            "PZS4126_3_em_poynting_once",
            "J_EM and Poynting flux enter J_H_total exactly once in the same observed Hodge/coframe",
            "4096/4106/4112 identify the route and guard against optional EM bookkeeping",
            "required",
            "CONDITIONAL_ONCE_ONLY_UNSIGNED",
        ),
        (
            "PZS4126_4_boundary_reference_silence",
            "boundary charge, reference subtraction, and symplectic flux are fixed or Ward-invariant",
            "3640 and 4098 expose this as the Hamiltonian/Hilbert equality pressure point",
            "required",
            "NOT_PARENT_SIGNED_CURRENTLY",
        ),
        (
            "PZS4126_5_no_tuned_cancellation",
            "the ten beta residuals vanish by termwise descent or a single Noether/Ward identity, not by fitted cancellation",
            "4125 locks the no-cancellation guard",
            "required",
            "GUARD_ACTIVE",
        ),
        (
            "PZS4126_6_zero_verdict",
            "beta_common_X=beta_common_Z=0",
            "would follow if all clauses above are parent-signed simultaneously",
            "sufficient",
            "SIGNED_IF_ALL_CLAUSES_TRUE_BUT_UNSIGNED_CURRENTLY",
        ),
    ]
    rows: List[dict] = []
    for clause_id, clause, evidence, role, status in data:
        row = row_base()
        row.update(
            {
                "clause_id": clause_id,
                "clause": clause,
                "evidence": evidence,
                "role": role,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def bound_rows() -> List[dict]:
    data = [
        (
            "BB4126_0_R10_short_range",
            "R10_short_range",
            "alpha_common(lambda)",
            "alpha_common(lambda)=K_X tau_R10(lambda) beta_common_S beta_common_T / M_X^2",
            "|beta_common| <= sqrt(alpha_bound(lambda) M_X^2 / |K_X tau_R10(lambda)|) for common source/test beta",
            "dimensionless beta; lambda in length units; alpha dimensionless",
            "alpha_bound(lambda);K_X;M_X^2;tau_R10(lambda);source/test normalization",
        ),
        (
            "BB4126_1_PPN_local_GR",
            "PPN_local_GR",
            "Delta_PPN_common",
            "Delta_PPN_common=C_1 beta_common^2 + C_2 partial_i beta_common + C_3 beta_connection + C_4 beta_boundary",
            "requires every term below PPN bounds; common beta is not erased by WEP",
            "dimensionless PPN residuals",
            "C_i coefficients; local derivative map; gauge projection; solar-system bound source",
        ),
        (
            "BB4126_2_Gdot_clock",
            "Gdot_clock",
            "d ln mu_obs/dt",
            "d ln mu_obs/dt = beta_common_A dot(A_N) + beta_G_time + beta_cal_time + beta_source_time",
            "|beta_common_A| <= (limit - residual_budget)/|dot(A_N)| when dot(A_N) is sourced",
            "time^-1 for drift; beta dimensionless",
            "clock/ephemeris drift bound; dot(A_N); residual budget; units",
        ),
        (
            "BB4126_3_orbital_radial",
            "orbital_radial",
            "partial_r ln mu_obs",
            "partial_r ln mu_obs = beta_common_A partial_r A_N + beta_measure_r + beta_boundary_r + beta_projection_r",
            "|beta_common_A| <= (radial source-hair limit - residual_budget)/|partial_r A_N|",
            "length^-1 for radial derivative; beta dimensionless",
            "range residual bound; partial_r A_N; source surface convention; calibration radius",
        ),
        (
            "BB4126_4_clock_common_mode",
            "clock_common_mode",
            "common clock drift",
            "Delta nu/nu = S_mu beta_common_A delta A_N + S_alpha beta_EM_common delta A_N + calibration terms",
            "bound beta_common jointly with EM common mode after sensitivity matrix is specified",
            "dimensionless frequency ratio or time^-1 drift",
            "clock sensitivity coefficients; A_N profile; EM/source calibration split",
        ),
        (
            "BB4126_5_EM_common_mode",
            "EM_common_mode",
            "Maxwell/Poynting source calibration residual",
            "Delta_EM_common = C_Hodge beta_coframe + C_ZQ A_N ln Z_Q + C_J A_N ln J_Q + C_Poynt beta_source_EM",
            "requires observed-Hodge/same-current zero theorem or separate EM bound",
            "dimensionless EM constitutive/source residual",
            "Hodge coefficients; Z_Q/current derivative; Poynting readout coefficient; source path",
        ),
        (
            "BB4126_6_Newton_Gauss",
            "Newton_Gauss",
            "Poisson/Gauss source equality",
            "Phi_N=-G_ref M_H^dress/r only if Delta_Gauss:=B_tau/G_ref-M_H^dress=0 and partial_r ln M_H^dress=0",
            "source coupling passes Newton only when Hamiltonian boundary mass equals dressed Hilbert mass",
            "potential units and source-mass units fixed by G_ref",
            "B_tau;M_H^dress;surface independence;Hamiltonian/Hilbert equality certificate",
        ),
    ]
    rows: List[dict] = []
    for bound_id, arena, observable, prediction, bound_rule, units, required_inputs in data:
        row = row_base()
        row.update(
            {
                "bound_id": bound_id,
                "arena": arena,
                "observable": observable,
                "prediction": prediction,
                "bound_rule": bound_rule,
                "units": units,
                "required_inputs": required_inputs,
                "source_status": "FORMULA_FILLED_PARENT_OR_NUMERIC_INPUTS_REQUIRED",
                "status": "NONCLAIM_BOUND_ROW",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def em_poynting_rows() -> List[dict]:
    data = [
        (
            "EMP4126_0_same_hodge_owner",
            "observed Maxwell action",
            "S_EM=-1/4 int sqrt(-g_obs) Z_Q F_Q^2 + int A_Q j_Q",
            "if A_Q,F_Q,Z_Q,j_Q and star_obs are q-owned, A_N S_EM has no independent source-normalization current",
            "OBSERVED_HODGE_ZERO_ROUTE_CONDITIONAL",
        ),
        (
            "EMP4126_1_poynting_once",
            "Poynting source flux",
            "S_EM_vector=Z_Q E x B and u_EM=Z_Q(E^2+B^2)/2 enter J_H_total once",
            "including Poynting once prevents both undercounting EM source stress and double-counting it as extra MTS residual",
            "POYNTING_ONCE_GUARD",
        ),
        (
            "EMP4126_2_em_residual",
            "EM common residual",
            "beta_source_EM = A_N ln Z_Q + A_N ln star_obs + A_N ln j_Q + A_N ln readout_Poynting + orientation/support terms",
            "this is the precise EM coupling throat if same-frame Hodge/current ownership is not signed",
            "EM_COMMON_RESIDUAL_EXTRACTED",
        ),
        (
            "EMP4126_3_maxwell_limit",
            "Maxwell/local GR compatibility",
            "same-frame EM Hilbert stress contributes to T_total in Einstein/Newton source equation; residual EM beta must be zero or bounded",
            "the EM route helps the theory only if it strengthens source ownership rather than adding an unconstrained fifth source",
            "MAXWELL_LIMIT_GATE",
        ),
    ]
    rows: List[dict] = []
    for em_id, object_name, formula, consequence, status in data:
        row = row_base()
        row.update(
            {
                "em_id": em_id,
                "object": object_name,
                "formula": formula,
                "consequence": consequence,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        (
            "DG4126_0_derivation_advance",
            "The coupling is no longer a single missing knob: beta_common is the Ward derivative of G_ref M_H^dress(1+epsilon_mu).",
            "WARD_OBSTRUCTION_DERIVED",
            "use the ten residual terms as the exact checklist for local GR/Newton closure",
        ),
        (
            "DG4126_1_zero_not_claimed",
            "Do not claim beta_common_X/Z=0 yet because the full parent Ward signature is not signed.",
            "PARENT_ZERO_UNSIGNED",
            "either sign all parent clauses or keep beta_common as a bound vector",
        ),
        (
            "DG4126_2_gr_constant_clarification",
            "MTS does not have to derive the numerical value of Newton's constant to reduce to GR; it must derive one universal derivative-free G_ref coupling to the same Hilbert source.",
            "G_NUMERIC_VALUE_EMPIRICAL_ROLE_DERIVED_TARGET",
            "focus on universality, same-frame source ownership, and derivative-hair absence",
        ),
        (
            "DG4126_3_em_poynting_integrated",
            "EM/Poynting is now inside the source Ward identity rather than an external afterthought.",
            "EM_POYNTING_SOURCE_INCLUDED_ONCE",
            "next work can test whether EM source owner packet closes beta_source_EM",
        ),
        (
            "DG4126_4_next",
            "Next target is to attack the shortest parent-signature clause: same-frame Hilbert/source mass equality or EM/Poynting source-owner zero.",
            "NEXT_SIGNATURE_HUNT_SELECTED",
            "build 4127 to choose and test the easiest clause to actually sign, not just list",
        ),
    ]
    rows: List[dict] = []
    for decision_id, decision, status, next_action in data:
        row = row_base()
        row.update(
            {
                "decision_id": decision_id,
                "decision": decision,
                "status": status,
                "next_action": next_action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4126_0",
            "result": DECISION,
            "summary": (
                "4126 derives the current-chain source-normalization Ward obstruction: beta_common_A is the derivative "
                "of mu_obs_common=G_ref M_H^dress(1+epsilon_mu), with M_H^dress built from the same Hilbert source charge "
                "including EM/Poynting once. The zero theorem is still unsigned, but the residual is now a ten-term "
                "computable vector with R10, PPN, Gdot, radial/orbital, clock, EM, and Newton/Gauss bound rows."
            ),
            "ward_zero_signed": "False",
            "obstruction_vector_filled": "True",
            "em_poynting_included": "True",
            "score_ready": "False",
            "claim_state": "no local_GR, Newton, PPN, R10, Gdot, clock, EM, Maxwell, or source-normalization pass",
            "next_target": "4127 shortest parent-signature clause attack",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4126_0",
            "target_doc": "4127-Y5-R2FR-shortest-source-signature-clause-attack.md",
            "target_script": "scripts/Y5_R2FR_4127_shortest_source_signature_clause_attack.py",
            "objective": (
                "choose the shortest clause in the 4126 Ward obstruction that might actually be parent-signed next, "
                "prefer same-frame Hilbert/source mass equality or EM/Poynting source-owner zero; attempt the proof first, "
                "then stage the needed bound coefficient rows if it fails"
            ),
            "success_gate": (
                "at least one beta residual term is parent-signed zero, or a precise nonclaim coefficient row with source path, units, "
                "arena projection, and bound-input requirements is filled"
            ),
            "reason": "4126 turns coupling into a ten-term Ward obstruction; progress now means killing one term, not circling the whole coupling again.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4126_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4126_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4126_WARD_IDENTITY_DERIVATION": SOURCE_DIR / "P8_Y5_R2FR_4126_WARD_IDENTITY_DERIVATION.csv",
        "P8_Y5_R2FR_4126_WARD_RESIDUAL_DECOMPOSITION": SOURCE_DIR / "P8_Y5_R2FR_4126_WARD_RESIDUAL_DECOMPOSITION.csv",
        "P8_Y5_R2FR_4126_PARENT_ZERO_SIGNATURE_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4126_PARENT_ZERO_SIGNATURE_AUDIT.csv",
        "P8_Y5_R2FR_4126_BETA_COMMON_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4126_BETA_COMMON_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4126_EM_POYNTING_COUPLING_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4126_EM_POYNTING_COUPLING_ROWS.csv",
        "P8_Y5_R2FR_4126_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4126_DECISION_GATES.csv",
        "P8_Y5_R2FR_4126_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4126_STATUS.csv",
        "P8_Y5_R2FR_4126_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4126_NEXT_TARGET.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    status = status_rows()[0]
    sections = [
        "# 4126 - Parent Source-Normalization Ward Identity or Beta Common Bound Fill",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- Real advance: `beta_common_A` is now derived as a Ward derivative of `mu_obs_common=G_ref M_H^dress(1+epsilon_mu)`.",
        "- The source mass is explicitly the same-frame dressed Hilbert charge, with EM/Poynting counted once.",
        "- The parent zero is still not claimed; the ten-term obstruction vector is the next proof checklist.",
        "- GR/Newton matching does not require deriving the numerical value of `G_ref`; it requires deriving one universal, derivative-free source coupling.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(["", "## Ward Identity", "", "| identity_id | symbol | status |", "|---|---|---|"])
    for row in ward_identity_rows():
        sections.append(f"| {row['identity_id']} | {row['symbol']} | {row['status']} |")
    sections.extend(["", "## Residual Decomposition", "", "| residual_id | symbol | observable_link |", "|---|---|---|"])
    for row in residual_decomposition_rows():
        sections.append(f"| {row['residual_id']} | {row['symbol']} | {row['observable_link']} |")
    sections.extend(["", "## EM And Poynting", "", "| em_id | status | consequence |", "|---|---|---|"])
    for row in em_poynting_rows():
        sections.append(f"| {row['em_id']} | {row['status']} | {row['consequence']} |")
    sections.extend(["", "## Bound Rows", "", "| arena | observable | status |", "|---|---|---|"])
    for row in bound_rows():
        sections.append(f"| {row['arena']} | {row['observable']} | {row['status']} |")
    sections.extend(
        [
            "",
            "## Claim Ceiling",
            "",
            f"- {status['claim_state']}.",
            "- No local-GR/Newton pass is claimed until the parent zero clauses are signed or all residual terms are bounded.",
            "",
            "## Next Target",
            "",
            "- `4127-Y5-R2FR-shortest-source-signature-clause-attack.md`",
            "- Attack one obstruction term directly instead of looping over the whole coupling problem.",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4126_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4126_WARD_IDENTITY_DERIVATION": ward_identity_rows,
        "P8_Y5_R2FR_4126_WARD_RESIDUAL_DECOMPOSITION": residual_decomposition_rows,
        "P8_Y5_R2FR_4126_PARENT_ZERO_SIGNATURE_AUDIT": parent_zero_signature_rows,
        "P8_Y5_R2FR_4126_BETA_COMMON_BOUND_ROWS": bound_rows,
        "P8_Y5_R2FR_4126_EM_POYNTING_COUPLING_ROWS": em_poynting_rows,
        "P8_Y5_R2FR_4126_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4126_STATUS": status_rows,
        "P8_Y5_R2FR_4126_NEXT_TARGET": next_target_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4126_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add("VAL4126_1_doc", "checkpoint markdown exists and names decision", DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"), str(DOC_PATH))

    parse_ok = True
    parse_counts: Dict[str, object] = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4126_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    ward_text = flatten_rows([outputs["P8_Y5_R2FR_4126_WARD_IDENTITY_DERIVATION"]])
    ward_ok = all(token in ward_text for token in ["A_N ln mu_obs_common", "Pi_M^H J_H_total", "J_Poynting", "Phi_N=-G_ref M_H^dress/r"])
    add("VAL4126_3_ward_identity", "Ward identity includes source scalar, Hilbert charge, Poynting, and Newton consequence", ward_ok, "ward tokens checked")

    residual_text = flatten_rows([outputs["P8_Y5_R2FR_4126_WARD_RESIDUAL_DECOMPOSITION"]])
    residual_tokens = ["beta_G", "beta_NG", "beta_measure", "beta_coframe", "beta_connection", "beta_boundary", "beta_source_matter", "beta_source_EM", "beta_projection", "beta_calibration"]
    add("VAL4126_4_residual_vector", "ten-term Ward residual vector is present", all(token in residual_text for token in residual_tokens), "residual tokens checked")

    audit_text = flatten_rows([outputs["P8_Y5_R2FR_4126_PARENT_ZERO_SIGNATURE_AUDIT"]])
    audit_ok = all(token in audit_text for token in ["NOT_PARENT_SIGNED_CURRENTLY", "SIGNED_IF_ALL_CLAUSES_TRUE", "PZS4126_3_em_poynting_once", "PZS4126_5_no_tuned_cancellation"])
    add("VAL4126_5_parent_zero_audit", "audit keeps zero conditional and includes EM/Poynting and no-tuning clauses", audit_ok, "audit tokens checked")

    bound_text = flatten_rows([outputs["P8_Y5_R2FR_4126_BETA_COMMON_BOUND_ROWS"]])
    bound_ok = all(token in bound_text for token in ["R10_short_range", "PPN_local_GR", "Gdot_clock", "orbital_radial", "clock_common_mode", "EM_common_mode", "Newton_Gauss"])
    add("VAL4126_6_bound_rows", "bound rows cover R10, PPN, Gdot, radial, clock, EM, and Newton/Gauss", bound_ok, "bound tokens checked")

    em_text = flatten_rows([outputs["P8_Y5_R2FR_4126_EM_POYNTING_COUPLING_ROWS"]])
    em_ok = all(token in em_text for token in ["POYNTING_ONCE_GUARD", "EM_COMMON_RESIDUAL_EXTRACTED", "OBSERVED_HODGE_ZERO_ROUTE_CONDITIONAL", "MAXWELL_LIMIT_GATE"])
    add("VAL4126_7_em_poynting", "EM/Poynting coupling route is explicit and not double counted", em_ok, "EM tokens checked")

    decision_text = flatten_rows([outputs["P8_Y5_R2FR_4126_DECISION_GATES"]])
    decision_ok = all(token in decision_text for token in ["WARD_OBSTRUCTION_DERIVED", "PARENT_ZERO_UNSIGNED", "G_NUMERIC_VALUE_EMPIRICAL_ROLE_DERIVED_TARGET", "NEXT_SIGNATURE_HUNT_SELECTED"])
    add("VAL4126_8_decisions", "decision gates record derivation advance, no-claim state, G clarification, and next hunt", decision_ok, "decision tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4126_STATUS"])
    status_ok = bool(status) and status[0].get("result") == DECISION and "no local_GR" in status[0].get("claim_state", "") and status[0].get("em_poynting_included") == "True"
    add("VAL4126_9_status", "status records obstruction derived and no-claim state", status_ok, "status row checked")

    nxt = parse_csv(outputs["P8_Y5_R2FR_4126_NEXT_TARGET"])
    next_ok = len(nxt) == 1 and nxt[0].get("target_doc") == "4127-Y5-R2FR-shortest-source-signature-clause-attack.md"
    add("VAL4126_10_next_target", "next target attacks one source-signature clause", next_ok, str(nxt))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4126_11_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4126*")) or any(FORMALIZATION.rglob("4126-Y5-R2FR*"))
    add("VAL4126_12_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4126_13_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4126_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()

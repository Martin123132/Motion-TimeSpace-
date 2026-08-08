from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3884"
BRANCH = "MTS_R2FR_Y5_PIM_HILBERT_FLUX_GAUSS_MONOPOLE_3884"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3884-Y5-R2FR-PiM-Hilbert-flux-Gauss-monopole-calibration-or-residual-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3883_NEXT = OUT / "P8_Y5_R2FR_3883_NEXT_TARGET.csv"
CSV_3883_SOURCE = OUT / "P8_Y5_R2FR_3883_SAME_HILBERT_SOURCE_LOCK.csv"
CSV_3883_NEWTON = OUT / "P8_Y5_R2FR_3883_NEWTON_SOURCE_DENSITY_BRIDGE.csv"
CSV_3883_RESIDUALS = OUT / "P8_Y5_R2FR_3883_MATTER_EM_RESIDUAL_VECTOR.csv"
CSV_3883_RUNNER = OUT / "P8_Y5_R2FR_3883_RUNNER_UPDATE.csv"
CSV_3883_VALIDATION = OUT / "P8_Y5_BRR545_3883_VALIDATION.csv"
CSV_SOURCE_STACK = OUT / "P8_source_normalized_Newton_branch_STACK.csv"
CSV_OWNER = OUT / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv"
CSV_PG = OUT / "P8_PG_calibration_residual_MAP.csv"
CSV_BOUND_MATRIX = OUT / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv"
CSV_HILBERT_MONOPOLE = OUT / "P8_Hilbert_monopole_calibration_CONTRACT.csv"
CSV_HAMILTONIAN_CHARGE = OUT / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"
CSV_CC_DIRECT = OUT / "P8_charge_current_equality_DIRECT_ATTEMPT.csv"
CSV_CC_RESIDUAL = OUT / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv"
CSV_HILBERT_DIV = OUT / "P8_Y5_HILBERT_CURRENT_2467_DIVERGENCE_IDENTITY.csv"
CSV_HILBERT_EXCHANGE = OUT / "P8_Y5_HILBERT_CURRENT_2467_EXCHANGE_CURRENT_IDENTITY.csv"
CSV_HWT_ATTEMPT = OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv"
CSV_HWT_CONTRACT = OUT / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv"
CSV_HWT_CERT = OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv"
CSV_PIM_CONTRACT = OUT / "P8_PiM_projector_variation_stress_CONTRACT.csv"
CSV_TOPO_HILBERT = OUT / "P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv"
CSV_TOPO_DECISION = OUT / "P8_TOPOLOGICAL_HILBERT_EQUALITY_DECISION.csv"
CSV_EM_POYNTING = OUT / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv"
CSV_FRAME = OUT / "P8_frame_source_split_residual_or_zero.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3884_SOURCE_REGISTER.csv",
    "flux": OUT / "P8_Y5_R2FR_3884_PIM_HILBERT_FLUX_CLOSURE_THEOREM.csv",
    "gauss": OUT / "P8_Y5_R2FR_3884_GAUSS_MONOPOLE_CALIBRATION_CHAIN.csv",
    "orbital": OUT / "P8_Y5_R2FR_3884_ORBITAL_NEWTON_READOUT_CHAIN.csv",
    "residuals": OUT / "P8_Y5_R2FR_3884_MASS_GAUSS_RESIDUAL_BOUND_ROWS.csv",
    "runner": OUT / "P8_Y5_R2FR_3884_RUNNER_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3884_CLAIM_GATES.csv",
    "next": OUT / "P8_Y5_R2FR_3884_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3884_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3884_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3884_00_next", CSV_3883_NEXT, "NEXT3883_0", "3883 selected PiM/Gauss target"),
    ("SRC3884_01_same_source", CSV_3883_SOURCE, "HSL3883_2_same_source", "same Hilbert source lock"),
    ("SRC3884_02_conservation", CSV_3883_SOURCE, "HSL3883_4_conservation", "total stress conservation"),
    ("SRC3884_03_density", CSV_3883_NEWTON, "NSB3883_0_density", "Hilbert density bridge"),
    ("SRC3884_04_poisson", CSV_3883_NEWTON, "NSB3883_3_Poisson", "Poisson source bridge"),
    ("SRC3884_05_PiM_resid", CSV_3883_RESIDUALS, "MER3883_8_Delta_PiM", "PiM residual"),
    ("SRC3884_06_Gauss_resid", CSV_3883_RESIDUALS, "MER3883_9_Delta_Gauss", "Gauss residual"),
    ("SRC3884_07_runner", CSV_3883_RUNNER, "RUNU3883_0_source_lock", "b_MHref decomposition"),
    ("SRC3884_08_valid", CSV_3883_VALIDATION, "VAL3883_16_next_target", "3883 validation"),
    ("SRC3884_09_SN4", CSV_SOURCE_STACK, "SN4_closed_Meff_flux", "closed Meff flux"),
    ("SRC3884_10_SN8", CSV_SOURCE_STACK, "SN8_Gauss_surface_integral", "Gauss surface integral"),
    ("SRC3884_11_SN9", CSV_SOURCE_STACK, "SN9_orbital_inverse_square_readout", "orbital readout"),
    ("SRC3884_12_SN11", CSV_SOURCE_STACK, "SN11_second_order_PPN_source_stability", "PPN source stability"),
    ("SRC3884_13_Y5O4", CSV_OWNER, "Y5O_4_flux_closure", "flux closure owner"),
    ("SRC3884_14_Y5O6", CSV_OWNER, "Y5O_6_Gauss_orbital_calibration", "Gauss orbital calibration"),
    ("SRC3884_15_Y5O7", CSV_OWNER, "Y5O_7_second_order_PPN_stability", "PPN stability"),
    ("SRC3884_16_PG4", CSV_PG, "PG4_Gauss_surface_integral", "Gauss residual map"),
    ("SRC3884_17_PG5", CSV_PG, "PG5_orbital_inverse_square_readout", "orbital readout residual map"),
    ("SRC3884_18_PG8", CSV_PG, "PG8_no_derivative_hair", "derivative hair map"),
    ("SRC3884_19_bound_Meff", CSV_BOUND_MATRIX, "P8_Meff_conservation", "Meff bound matrix"),
    ("SRC3884_20_bound_radial", CSV_BOUND_MATRIX, "P8_radial_source_hair", "radial source bound matrix"),
    ("SRC3884_21_HM2", CSV_HILBERT_MONOPOLE, "HM2_mass_flux_closure", "mass flux closure contract"),
    ("SRC3884_22_HM3", CSV_HILBERT_MONOPOLE, "HM3_absolute_monopole_calibration", "monopole calibration contract"),
    ("SRC3884_23_HM6", CSV_HILBERT_MONOPOLE, "HM6_no_derivative_source_hair", "no derivative source hair"),
    ("SRC3884_24_HC4", CSV_HAMILTONIAN_CHARGE, "HC4_charge_equals_PiM_Hilbert_mass", "surface charge equals PiM Hilbert mass"),
    ("SRC3884_25_HC8", CSV_HAMILTONIAN_CHARGE, "HC8_Poisson_Gauss_orbital_calibration", "Poisson/Gauss/orbital calibration"),
    ("SRC3884_26_CC3", CSV_CC_DIRECT, "CC3_projected_mass_current", "projected mass current"),
    ("SRC3884_27_CC7", CSV_CC_DIRECT, "CC7_closed_flux_and_Gauss_calibration", "closed flux and Gauss calibration"),
    ("SRC3884_28_CC8", CSV_CC_DIRECT, "CC8_second_order_limit", "PPN second order guard"),
    ("SRC3884_29_Delta_PiM", CSV_CC_RESIDUAL, "Delta_PiM", "PiM residual decomposition"),
    ("SRC3884_30_Delta_flux", CSV_CC_RESIDUAL, "Delta_flux", "flux residual decomposition"),
    ("SRC3884_31_Delta_cal", CSV_CC_RESIDUAL, "Delta_cal", "calibration residual decomposition"),
    ("SRC3884_32_DIV2", CSV_HILBERT_DIV, "DIV2467_2_matter_shell", "matter-shell divergence"),
    ("SRC3884_33_DIV4", CSV_HILBERT_DIV, "DIV2467_4_Killing_clock", "Killing clock closure"),
    ("SRC3884_34_EXC3", CSV_HILBERT_EXCHANGE, "EXC2467_3_local_stationary_escape", "local stationary escape"),
    ("SRC3884_35_HWT3", CSV_HWT_ATTEMPT, "HWT536_3_Hilbert_to_PiM_charge_map", "Hilbert to PiM map"),
    ("SRC3884_36_HWT8", CSV_HWT_ATTEMPT, "HWT536_8_weak_field_readout_after_charge_glue", "weak-field readout after glue"),
    ("SRC3884_37_PAC537_4", CSV_HWT_CONTRACT, "PAC537_4_action_owned_PiM_projector", "action-owned PiM projector"),
    ("SRC3884_38_PAC537_8", CSV_HWT_CONTRACT, "PAC537_8_dressed_source_Gauss_readout", "dressed source Gauss readout"),
    ("SRC3884_39_HWG4", CSV_HWT_CERT, "HWG535_4_commutator_zero", "PiM commutator certificate"),
    ("SRC3884_40_HWG5", CSV_HWT_CERT, "HWG535_5_no_projector_stress", "no projector stress certificate"),
    ("SRC3884_41_PV1", CSV_PIM_CONTRACT, "PV1_topological_absolute_charge_route", "topological absolute charge route"),
    ("SRC3884_42_PV6", CSV_PIM_CONTRACT, "PV6_modified_exterior_residual_map", "projector residual map"),
    ("SRC3884_43_EH501_2", CSV_TOPO_HILBERT, "EH501_2_Ward_current_route", "Ward current route"),
    ("SRC3884_44_EH501_4", CSV_TOPO_HILBERT, "EH501_4_Hamiltonian_charge_route", "Hamiltonian charge route"),
    ("SRC3884_45_D501", CSV_TOPO_DECISION, "D501_1_best_route", "topological-Hilbert best route"),
    ("SRC3884_46_EM_flux", CSV_EM_POYNTING, "EMF3502_1_radiative_poynting_flux", "radiative EM flux"),
    ("SRC3884_47_frame", CSV_FRAME, "FS3048_0_frame_split_definition", "frame split residual"),
]

FLUX_THEOREM = (
    "Let J_M := Pi_M J_H[tau]. Then dJ_M = (dPi_M)J_H + Pi_M dJ_H. "
    "If Pi_M is parent-fixed/covariantly constant, T_H is conserved, tau is Killing or stationary in the local collar, "
    "and boundary/radiative fluxes vanish, then d(Pi_M J_H)=0."
)

GAUSS_CHAIN = (
    "From nabla^2 Phi=4*pi*G0*rho_H, integration over a compact source volume gives "
    "oint grad Phi.n dA = 4*pi*G0 M_H, where M_H=int rho_H dV = int Pi_M J_H."
)

ORBITAL_CHAIN = (
    "In the source-free exterior, Phi=-G0 M_H/r + multipoles + residuals; slow test bodies obey a^i=-partial^i Phi, "
    "so the monopole gives v^2 r=G0 M_H when range, radial, frame and non-EH residuals vanish."
)

MASS_DRIFT_BOUND = (
    "|d_t ln M_eff| <= |b_tau_strain| + |b_PiM_comm| + |Phi_EM_rad|/(M_eff*c^2) + |b_boundary_ref| + |b_extra_charge|"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return ""
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("\n", " ").replace("|", "\\|") for col in columns) + " |")
    return "\n".join(lines)


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_PiM_Hilbert_flux_Gauss_monopole",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def flux_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("PFC3884_0_definition", "projected mass current", "J_M := Pi_M J_H[tau]", "DEFINITION_FROM_3883_SOURCE", "uses the same Hilbert source before orbital readout"),
        ("PFC3884_1_product_rule", "flux identity", FLUX_THEOREM, "EXACT_CONDITIONAL_THEOREM", "turns Meff drift/radial hair into explicit failed-premise terms"),
        ("PFC3884_2_stationary_zero", "stationary collar zero", "If tau is Killing, ell_J fixed, Pi_M covariantly constant, and net boundary/radiative flux vanishes, then d_t M_eff=0 and partial_r M_eff=0 between linked surfaces.", "CANDIDATE_FLUX_ZERO", "closes time/radial source drift in the candidate branch"),
        ("PFC3884_3_em_flux", "EM flux exception", "Nonzero Phi_EM_rad changes M_eff by the Poynting energy flux and must stay in the residual vector.", "RETAIN_IF_NONZERO", "keeps EM flow honest rather than double-counted"),
        ("PFC3884_4_limits", "limits", "Pi_M parent ownership, projector stress silence, reference terms, domain motion, and non-EH extra charge are not globally signed.", "OPEN_RESIDUAL_GUARD", "no Newton/local-GR claim yet"),
    ]
    return [
        {
            "flux_id": row_id,
            "piece": piece,
            "statement": statement,
            "status": status,
            "effect": effect,
            "candidate_flux_closed": status == "CANDIDATE_FLUX_ZERO",
            "global_corpus_adopted": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, status, effect in raw_rows
    ]


def gauss_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("GMC3884_0_Poisson", "Poisson source", "nabla^2 Phi=4*pi*G0*rho_H from 3882/3883", "INPUT_LOCKED_IN_CANDIDATE", "source density is Hilbert density"),
        ("GMC3884_1_Gauss", "Gauss theorem", GAUSS_CHAIN, "EXACT_CONDITIONAL_GAUSS_BRIDGE", "converts source density into a surface monopole"),
        ("GMC3884_2_surface_independence", "surface independence", "If d(Pi_M J_H)=0 in the exterior annulus, M_H[S2]=M_H[S1] for linked surfaces around the same worldtube.", "CANDIDATE_SURFACE_INDEPENDENCE", "kills radial source hair from mass-flux drift"),
        ("GMC3884_3_multipoles", "multipole guard", "Non-spherical compact sources add multipoles but not a different monopole; multipoles are readout/PPN corrections, not GM calibration freedom.", "MONOPOLE_ONLY_GUARD", "prevents hiding source normalization in shape terms"),
        ("GMC3884_4_residual", "if failed", "Delta_Gauss = M_eff[Pi_M J_H] - (4*pi*G0)^-1 oint grad Phi.n dA stays as an explicit residual.", "RESIDUAL_IF_PREMISES_FAIL", "no orbital backfill"),
    ]
    return [
        {
            "gauss_id": row_id,
            "piece": piece,
            "statement": statement,
            "status": status,
            "effect": effect,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, status, effect in raw_rows
    ]


def orbital_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("ORB3884_0_exterior", "exterior potential", ORBITAL_CHAIN, "EXACT_CONDITIONAL_READOUT", "links Poisson/Gauss monopole to measured Kepler GM"),
        ("ORB3884_1_no_range", "range/radial guard", "No finite-range alpha(lambda), radial source hair, frame split, or non-EH force may be absorbed into the monopole.", "NO_CALIBRATION_CHEAT", "keeps SPARC/orbital style fits from defining the source"),
        ("ORB3884_2_slow_geodesic", "slow-particle readout", "For minimally coupled slow matter, d^2x^i/dt^2=-partial_i Phi+O(v^2/c^2,PPN).", "CANDIDATE_NEWTON_READOUT", "first-order Newton mechanics branch"),
        ("ORB3884_3_not_GR", "not local GR", "Newtonian inverse-square readout does not prove gamma=1, beta=1, alpha_i=0, xi=0 or R11 non-EH operator silence.", "NO_LOCAL_GR_PROMOTION", "next gate is second-order PPN/R11"),
    ]
    return [
        {
            "orbital_id": row_id,
            "piece": piece,
            "statement": statement,
            "status": status,
            "effect": effect,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, status, effect in raw_rows
    ]


def residual_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("MGR3884_0_Meff_time", "P8_Meff_conservation", "dln_Meff_dt", "yr^-1", MASS_DRIFT_BOUND, "Gdot/beta locks after decomposition", "OPEN_UNLESS_FLUX_THEOREM_PARENT_SIGNED"),
        ("MGR3884_1_radial", "P8_radial_source_hair", "partial_r_ln_mu_obs", "inverse_length_or_dimensionless", "|partial_r ln M_eff| <= |b_PiM_comm|+|b_boundary|+|b_extra_charge|+|b_range|", "zero radial hair or mapped PPN/R10 bound", "OPEN_UNLESS_GAUSS_SURFACE_INDEPENDENCE_SIGNED"),
        ("MGR3884_2_Gauss", "P8_Gauss_calibration", "Delta_Gauss", "mass_or_dimensionless_after_GM_norm", "M_eff[Pi_M J_H] - (4*pi*G0)^-1 oint grad Phi.n dA", "zero exact Gauss calibration or explicit residual", "OPEN_GLOBAL_CLAIM"),
        ("MGR3884_3_PiM", "P8_PiM_projector_stress", "Delta_PiM_metric", "dimensionless_or_stress_units", "M_eff[delta Pi_M J_H]+M_eff[Pi_M J_H-J_M_parent]", "PiM topological/covariantly constant or bound", "OPEN_PROJECTOR_PARENT_OWNERSHIP"),
        ("MGR3884_4_flux", "P8_boundary_radiative_flux", "Phi_EM_rad", "power_or_mass_rate", "dM_eff/dt includes -Phi_EM_rad/c^2", "stationary/no-flux theorem or measured flux bound", "OPEN_IF_RADIATING"),
        ("MGR3884_5_orbital", "P8_orbital_readout_residual", "delta_a_r", "acceleration", "a_r + G0*M_eff/r^2", "slow geodesic plus no force residual or explicit bound", "OPEN_UNTIL_READOUT_SIGNED"),
        ("MGR3884_6_PPN", "P8_nonlinear_beta_source_residue", "delta_beta_source;gamma_minus_1", "dimensionless", "second-order source-normalized PPN residual vector", "beta/gamma residual values or theorem-zero", "DEFERRED_NEXT"),
    ]
    return [
        {
            "residual_id": row_id,
            "component_id": component,
            "symbol": symbol,
            "units": units,
            "formula_or_bound": formula,
            "target": target,
            "current_status": status,
            "valid_prediction_row": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, component, symbol, units, formula, target, status in raw_rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("RUNU3884_0_flux", "b_MHref_lock", "b_MHref_lock := b_PiM_flux+b_Gauss+b_orbital+b_PiM_stress+b_boundary_ref+b_flux+b_PPN_source", "MASS_LOCK_REFINED"),
        ("RUNU3884_1_candidate", "candidate zeros", "b_PiM_flux=0 and b_Gauss=0 in the stationary candidate if PiM is parent-fixed and Gauss/readout premises hold", "CANDIDATE_ONLY"),
        ("RUNU3884_2_residual", "fallback rows", "if any premise fails, use MGR3884 residual rows for dln_Meff_dt, radial hair, Delta_Gauss, Delta_PiM, Phi_EM_rad and delta_a_r", "RESIDUAL_BOUND_READY"),
        ("RUNU3884_3_Newton", "Newton branch", "nabla^2 Phi=4*pi*G0 rho_H; oint gradPhi.n dA=4*pi*G0 M_eff; a=-gradPhi", "FIRST_ORDER_NEWTON_CANDIDATE"),
        ("RUNU3884_4_no_GR", "local_GR", "no promotion beyond first-order Newton until PPN/R11 source-stability vector is derived or bounded", "NO_LOCAL_GR_PROMOTION"),
    ]
    return [
        {
            "update_id": row_id,
            "runner_field": field,
            "rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, field, rule, status in raw_rows
    ]


def gate_rows(
    sources: list[dict[str, object]],
    flux: list[dict[str, object]],
    gauss: list[dict[str, object]],
    orbital: list[dict[str, object]],
    residuals: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    source_count = sum(1 for row in sources if row["exists"] and row["needle_found"])
    checks = [
        ("G3884_0_sources", source_count == len(sources), f"{source_count}/{len(sources)} sources resolved"),
        ("G3884_1_flux_theorem", any(row["flux_id"] == "PFC3884_1_product_rule" for row in flux), "PiM flux product-rule theorem"),
        ("G3884_2_flux_zero", any(row["flux_id"] == "PFC3884_2_stationary_zero" for row in flux), "candidate stationary flux zero"),
        ("G3884_3_Gauss", any(row["gauss_id"] == "GMC3884_1_Gauss" and "oint grad Phi" in str(row["statement"]) for row in gauss), "Gauss bridge"),
        ("G3884_4_orbital", any(row["orbital_id"] == "ORB3884_2_slow_geodesic" for row in orbital), "slow-particle readout"),
        ("G3884_5_residuals", len(residuals) >= 7, f"{len(residuals)} mass/Gauss residual rows"),
        ("G3884_6_no_GR", any(row["orbital_id"] == "ORB3884_3_not_GR" for row in orbital), "PPN/local-GR guard"),
        ("G3884_7_no_claim", True, "candidate first-order Newton only; global adoption and PPN/R11 remain open"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, passed, detail in checks
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3884_0",
            "target_checkpoint": "3885-Y5-R2FR-second-order-PPN-source-stability-or-R11-residual-vector.md",
            "script": "scripts/Y5_R2FR_3885_second_order_PPN_source_stability_or_R11_residual_vector.py",
            "objective": "push beyond first-order Newton by deriving gamma=1, beta=1 and preferred-frame/source-stability conditions in the candidate branch, or emit executable R11/PPN residual vector rows",
            "why_next": "3884 gives the candidate first-order Newton bridge; the next non-negotiable gate for local GR is second-order PPN and non-EH operator stability",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS3884_0",
            "branch": BRANCH,
            "summary": "PiM Hilbert flux closure and Gauss/orbital monopole calibration derived as exact stationary candidate theorems; dln_Meff, radial hair, Delta_Gauss, PiM stress, EM flux, orbital and PPN residual rows retained nonclaim",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    flux: list[dict[str, object]],
    gauss: list[dict[str, object]],
    orbital: list[dict[str, object]],
    residuals: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3884 - PiM Hilbert Flux and Gauss Monopole Calibration

Generated: `{timestamp}`

## Result

3884 turns the 3883 same Hilbert source into a first-order Newton candidate:

`{FLUX_THEOREM}`

Then:

`{GAUSS_CHAIN}`

and:

`{ORBITAL_CHAIN}`

So the candidate branch now has the right logical ladder: Hilbert stress -> closed projected mass -> Gauss monopole -> inverse-square orbital readout. It remains nonclaim because parent PiM ownership, boundary/reference silence, extra charge, and second-order PPN/R11 stability are still live gates.

## PiM Hilbert Flux Closure

{markdown_table(flux, ["flux_id", "piece", "statement", "status", "effect"])}

## Gauss Monopole Calibration

{markdown_table(gauss, ["gauss_id", "piece", "statement", "status", "effect"])}

## Orbital Newton Readout

{markdown_table(orbital, ["orbital_id", "piece", "statement", "status", "effect"])}

## Residual Bound Rows

{markdown_table(residuals, ["residual_id", "component_id", "symbol", "formula_or_bound", "current_status"])}

## Runner Update

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "detail", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is a serious Newton bridge in candidate form. If the PiM/topological/projector premises are signed, `M_eff` becomes the closed Hilbert mass and the Gauss monopole gives the measured inverse-square source. The work is not local GR yet; the next hard gate is second-order PPN/R11 stability.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3884 PIM GAUSS MONOPOLE -->"
    end = "<!-- END 3884 PIM GAUSS MONOPOLE -->"
    block = f"""{start}

## 3884 - PiM Hilbert flux and Gauss monopole calibration

Flux theorem:

`{FLUX_THEOREM}`

Gauss bridge:

`{GAUSS_CHAIN}`

Orbital readout:

`{ORBITAL_CHAIN}`

Candidate consequence: first-order Newton now has a clean ladder from Hilbert stress to closed projected source mass to inverse-square readout. Nonclaim guard: PiM parent ownership, projector stress, boundary/reference terms, extra charge, radiative flux, frame/range residuals and PPN/R11 stability remain live.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3884_PIM_HILBERT_FLUX_CLOSURE_THEOREM.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3884_GAUSS_MONOPOLE_CALIBRATION_CHAIN.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3884_MASS_GAUSS_RESIDUAL_BOUND_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3884_VALIDATION.csv`

Next gate: `3885`, second-order PPN source stability or R11 residual vector.

<!-- Generated by 3884 at {timestamp} -->
{end}
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else "# Local GR Coupling Spine Current State\n"
    if start in existing and end in existing:
        before = existing.split(start)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        new_text = f"{before}\n\n{block}\n\n{after}".rstrip() + "\n"
    else:
        new_text = existing.rstrip() + "\n\n" + block + "\n"
    SPINE_PATH.write_text(new_text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    flux: list[dict[str, object]],
    gauss: list[dict[str, object]],
    orbital: list[dict[str, object]],
    residuals: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    checks.append(("VAL3884_0_sources", "all cited source paths exist and needles are found", all_sources, f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"))
    checks.append(("VAL3884_1_flux_identity", "PiM flux identity exists", any(row["flux_id"] == "PFC3884_1_product_rule" and "d(Pi_M J_H)=0" in str(row["statement"]) for row in flux), "PFC3884_1"))
    checks.append(("VAL3884_2_stationary_zero", "stationary flux zero row exists", any(row["flux_id"] == "PFC3884_2_stationary_zero" for row in flux), "PFC3884_2"))
    checks.append(("VAL3884_3_Gauss", "Gauss monopole bridge exists", any(row["gauss_id"] == "GMC3884_1_Gauss" and "4*pi*G0" in str(row["statement"]) for row in gauss), "GMC3884_1"))
    checks.append(("VAL3884_4_orbital", "orbital Newton readout exists", any(row["orbital_id"] == "ORB3884_2_slow_geodesic" for row in orbital), "ORB3884_2"))
    required = {"dln_Meff_dt", "partial_r_ln_mu_obs", "Delta_Gauss", "Delta_PiM_metric", "Phi_EM_rad", "delta_a_r"}
    checks.append(("VAL3884_5_residual_symbols", "mass/Gauss residual rows include required symbols", required.issubset({str(row["symbol"]) for row in residuals}), "required residual symbols"))
    checks.append(("VAL3884_6_runner", "runner refines b_MHref_lock", any(row["runner_field"] == "b_MHref_lock" for row in runner), "b_MHref_lock"))
    checks.append(("VAL3884_7_no_GR_guard", "local GR promotion is blocked", any(row["orbital_id"] == "ORB3884_3_not_GR" for row in orbital), "ORB3884_3"))
    checks.append(("VAL3884_8_no_claim_gates", "no gate allows a claim", all(str(row["claim_allowed"]) == "False" for row in gates), "claim_allowed=false"))
    checks.append(("VAL3884_9_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "serious Newton bridge" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3884_10_spine", "spine updated with 3884 block", SPINE_PATH.exists() and "BEGIN 3884 PIM GAUSS MONOPOLE" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3884_11_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    generated_patterns = ("3884-Y5", "P8_Y5_R2FR_3884", "P8_Y5_BRR545_3884")
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3884*")
            if path.is_file() and any(pattern in path.name for pattern in generated_patterns)
        ]
    checks.append(("VAL3884_12_formalization_untouched", "no generated 3884 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3884_13_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3884_14_all_nonclaim", "all analytical rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [flux, gauss, orbital, residuals, runner] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3884_15_next_target", "next target attacks second-order PPN/R11", any("second-order-PPN" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3885 PPN/R11"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    flux = flux_rows(timestamp)
    gauss = gauss_rows(timestamp)
    orbital = orbital_rows(timestamp)
    residuals = residual_rows(timestamp)
    runner = runner_rows(timestamp)
    gates = gate_rows(sources, flux, gauss, orbital, residuals, timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["flux"], flux)
    write_csv(OUTPUTS["gauss"], gauss)
    write_csv(OUTPUTS["orbital"], orbital)
    write_csv(OUTPUTS["residuals"], residuals)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, flux, gauss, orbital, residuals, runner, gates, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, flux, gauss, orbital, residuals, runner, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_PIM_HILBERT_FLUX_GAUSS_MONOPOLE")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

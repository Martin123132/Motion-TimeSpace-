from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3135_CLOCK_READOUT_INPUTS.csv"
LEMMA = OUT / "P8_Y5_R2FR_3135_READOUT_CHAIN_LEMMA.csv"
LIMITS = OUT / "P8_Y5_R2FR_3135_SR_GR_LIMIT_EXPANSION.csv"
RESIDUALS = OUT / "P8_Y5_R2FR_3135_TIME_SIGN_RESIDUAL_VECTOR.csv"
GATE = OUT / "P8_Y5_R2FR_3135_GATE.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3135_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path_text


def parse_float(value: str) -> float | None:
    try:
        if value is None or str(value).strip() == "":
            return None
        return float(str(value).strip())
    except ValueError:
        return None


def source_inputs() -> list[dict[str, Any]]:
    return [
        {
            "source_id": "SRC3135_0",
            "role": "3134_parent_quotient_reduction",
            "source_file": "3134-Y5-R2FR-parent-quotient-map-and-matter-pullback-reduction-under-AX1090.md",
            "required": "true",
            "evidence_use": "q/readout and matter-pullback premises remain conditional",
            "valid_for_claim": "false",
        },
        {
            "source_id": "SRC3135_1",
            "role": "3134_proof_reduction_matrix",
            "source_file": "source-intake\\mts_residuals\\P8_Y5_R2FR_3134_PROOF_REDUCTION_MATRIX.csv",
            "required": "true",
            "evidence_use": "formal chain-rule pass and parent-signature failures",
            "valid_for_claim": "false",
        },
        {
            "source_id": "SRC3135_2",
            "role": "3134_leakage_carry_forward",
            "source_file": "source-intake\\mts_residuals\\P8_Y5_R2FR_3134_FINITE_LEAKAGE_CARRY_FORWARD.csv",
            "required": "true",
            "evidence_use": "C_Obs_e, C_shadow_abs, and DqZ/J_A leakage heads",
            "valid_for_claim": "false",
        },
        {
            "source_id": "SRC3135_3",
            "role": "private_time_flow_fork_heuristic",
            "source_file": "3134A-private-fork-heuristics-time-flow.md",
            "required": "true",
            "evidence_use": "heuristic only: separate internal flow variable from observable clock readout",
            "valid_for_claim": "false",
        },
        {
            "source_id": "SRC3135_4",
            "role": "auxiliary_clock_cell_route",
            "source_file": "79-auxiliary-clock-cell-variation-attempt.md",
            "required": "true",
            "evidence_use": "reference clocks/cells are allowed only if stressless or pure constraint",
            "valid_for_claim": "false",
        },
        {
            "source_id": "SRC3135_5",
            "role": "tau_generator_contract",
            "source_file": "source-intake\\mts_residuals\\P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
            "required": "true",
            "evidence_use": "one tau for source, charge, clock, boundary, and orbit is not signed",
            "valid_for_claim": "false",
        },
        {
            "source_id": "SRC3135_6",
            "role": "killing_clock_gate",
            "source_file": "source-intake\\mts_residuals\\P8_Y5_R10_685_KILLING_CLOCK_GATE.csv",
            "required": "true",
            "evidence_use": "stationary/Killing and clock normalization gates fail for claim",
            "valid_for_claim": "false",
        },
        {
            "source_id": "SRC3135_7",
            "role": "symgrad_tau_decomposition",
            "source_file": "source-intake\\mts_residuals\\P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv",
            "required": "true",
            "evidence_use": "nonstationary tau decomposes into trace, shear, lapse, shift, boundary, and role mismatch",
            "valid_for_claim": "false",
        },
        {
            "source_id": "SRC3135_8",
            "role": "tau_clock_map",
            "source_file": "source-intake\\mts_residuals\\P8_Y5_R10_647_TAU_CLOCK_MAP.csv",
            "required": "true",
            "evidence_use": "clock product map separates chi_X/time drift from Hamiltonian tau",
            "valid_for_claim": "false",
        },
        {
            "source_id": "SRC3135_9",
            "role": "clock_product_bounds",
            "source_file": "source-intake\\mts_residuals\\P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv",
            "required": "true",
            "evidence_use": "source-backed clock product bounds for alpha drift",
            "valid_for_claim": "false",
        },
        {
            "source_id": "SRC3135_10",
            "role": "clock_alpha_source_lock",
            "source_file": "source-intake\\mts_residuals\\P8_Y5_R10_766_CLOCK_ALPHA_SOURCE_LOCK.csv",
            "required": "true",
            "evidence_use": "Galileo redshift row is not an alpha_EM row; prevents source mixing",
            "valid_for_claim": "false",
        },
        {
            "source_id": "SRC3135_11",
            "role": "local_empirical_bounds",
            "source_file": "source-intake\\local_bounds\\local_bound_claims.csv",
            "required": "true",
            "evidence_use": "redshift, Gdot, PPN, WEP, and R10 bound anchors",
            "valid_for_claim": "false",
        },
    ]


def annotate_inputs(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    annotated: list[dict[str, Any]] = []
    for row in rows:
        path = source_path(str(row["source_file"]))
        annotated_row = dict(row)
        annotated_row["resolved_path"] = str(path)
        annotated_row["exists"] = str(path.exists()).lower()
        if path.suffix.lower() == ".csv" and path.exists():
            annotated_row["row_count"] = len(read_csv(path))
        else:
            annotated_row["row_count"] = ""
        annotated.append(annotated_row)
    return annotated


def strongest_clock_bound() -> dict[str, Any]:
    rows = read_csv(ROOT / "source-intake" / "mts_residuals" / "P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv")
    best: dict[str, Any] = {
        "clock_pair": "MISSING_CLOCK_BOUND",
        "bound_1sigma_yr_inv": "",
        "bound_2sigma_yr_inv": "",
        "source_row": "",
    }
    best_value: float | None = None
    for row in rows:
        value = parse_float(row.get("conservative_abs_product_bound_1sigma_yr_inv", ""))
        if value is None:
            continue
        if best_value is None or value < best_value:
            best_value = value
            best = {
                "clock_pair": row.get("clock_pair", ""),
                "bound_1sigma_yr_inv": row.get("conservative_abs_product_bound_1sigma_yr_inv", ""),
                "bound_2sigma_yr_inv": row.get("conservative_abs_product_bound_2sigma_yr_inv", ""),
                "source_row": row.get("bound_id", ""),
            }
    return best


def local_bound(row_id: str) -> dict[str, str]:
    rows = read_csv(ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv")
    for row in rows:
        if row.get("row_id") == row_id:
            return row
    return {}


def build_lemma(clock_bound: dict[str, Any]) -> list[dict[str, Any]]:
    now = stamp()
    return [
        {
            "lemma_id": "CRL3135_0_variable_separation",
            "claim": "internal flow time is not automatically observed clock time",
            "formal_statement": "tau_clk[path] = R_clock(q(Phi), path, clock_species); tau_flow is observable only through q or an explicit clock coupling",
            "proof_status": "conditional_lemma_valid",
            "what_is_proven": "A sign flip or monotonic inversion in an internal flow variable is not by itself a falsifier.",
            "what_is_not_proven": "That current MTS parent-signs q, R_clock, matter functor, and no direct tau_flow clock coupling.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "lemma_id": "CRL3135_1_SR_clock_limit",
            "claim": "SR clock dilation is recovered if R_clock is the observed metric/coframe proper-time functional",
            "formal_statement": "in a local inertial observed frame, d tau_clk / d t_obs = sqrt(1 - v_obs^2/c^2) + epsilon_SR_readout",
            "proof_status": "formal_pass_conditional",
            "what_is_proven": "The SR sign is fixed by the observable coframe metric, not by the internal flow parameter.",
            "what_is_not_proven": "epsilon_SR_readout=0 for MTS; this needs parent-owned coframe/readout and matter descent.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "lemma_id": "CRL3135_2_GR_redshift_limit",
            "claim": "GR weak-field redshift is recovered if the observed metric has the standard g00 potential coefficient",
            "formal_statement": "for g00_obs = -(1 + 2 Phi/c^2) + O(c^-4), Delta nu/nu = (Phi_A - Phi_B)/c^2 + epsilon_GR_redshift",
            "proof_status": "formal_pass_conditional",
            "what_is_proven": "The redshift sign is a readout-metric coefficient question.",
            "what_is_not_proven": "MTS derives the g00 coefficient, tau normalization, and zero residuals.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "lemma_id": "CRL3135_3_null_clock_clarifier",
            "claim": "photons carry zero proper time because the observed null condition gives ds_obs^2=0",
            "formal_statement": "for EM/geometric-optics rays, g_obs(k,k)=0 -> d tau_clk=0; this need not mean tau_flow literally stops",
            "proof_status": "formal_pass_conditional",
            "what_is_proven": "Massless no-proper-time behaviour can be read as an observed-geometry null condition.",
            "what_is_not_proven": "That the MTS EM sector inherits the observed null cone without flow/background leakage.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "lemma_id": "CRL3135_4_direct_flow_leak",
            "claim": "if internal flow couples directly to constants, matter phase, or EM stress, it is a bounded residual",
            "formal_statement": "epsilon_clock_flow <= |kappa_alpha tau_clock_time| + epsilon_tau_role + epsilon_CObs + epsilon_shadow + epsilon_EM_flow",
            "proof_status": "residual_vector_defined",
            "what_is_proven": f"source-backed clock product cap is loaded; strongest current row {clock_bound['source_row']} gives {clock_bound['bound_1sigma_yr_inv']} yr^-1 at 1sigma bookkeeping",
            "what_is_not_proven": "the MTS-side product or theorem-zero input is not supplied.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "lemma_id": "CRL3135_5_tau_generator_boundary",
            "claim": "clock readout and Hamiltonian/source tau must not be silently identified",
            "formal_statement": "tau_clock = tau_charge = tau_source = tau_orbit = tau_boundary is a separate parent-signature gate",
            "proof_status": "blocked_by_existing_tau_gate",
            "what_is_proven": "3135 may quarantine clock-sign issues but cannot define M_H_ref, Newton GM, or local GR from tau.",
            "what_is_not_proven": "one parent-selected tau controls all roles.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def build_limits() -> list[dict[str, Any]]:
    now = stamp()
    redshift = local_bound("R2_clock_redshift")
    gdot = local_bound("R9_Gdot")
    gamma = local_bound("R3_gamma")
    return [
        {
            "limit_id": "LIM3135_0_SR_timelike_clock",
            "arena": "local inertial clocks",
            "required_readout": "tau_clk[path]=integral sqrt(-g_obs(dx,dx))/c",
            "standard_limit": "d tau_clk/dt_obs = sqrt(1-v_obs^2/c^2)",
            "mts_residual": "epsilon_SR_readout = epsilon_q_parent + epsilon_factorization + epsilon_CObs + epsilon_matter_descent",
            "current_status": "conditional_not_claim_ready",
            "empirical_bound_loaded": "not_applicable_source_limit_is_standard_kinematic_identity",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "limit_id": "LIM3135_1_GR_redshift_clock",
            "arena": "redshift/clocks",
            "required_readout": "g00_obs = -(1+2 Phi/c^2)+O(c^-4) with tau normalized to the observed clock at reference",
            "standard_limit": "Delta nu/nu = (Phi_A-Phi_B)/c^2",
            "mts_residual": "epsilon_GR_redshift",
            "current_status": "source_bound_loaded_mts_prediction_missing",
            "empirical_bound_loaded": redshift.get("upper_bound", "MISSING_R2_BOUND"),
            "bound_units": redshift.get("units", ""),
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "limit_id": "LIM3135_2_Newton_slow_motion",
            "arena": "Newtonian mechanics",
            "required_readout": "same g00_obs potential controls slow-motion geodesic acceleration and the source-normalized Poisson equation",
            "standard_limit": "d2x/dt_obs^2 = -grad Phi plus Poisson/Gauss source normalization",
            "mts_residual": "epsilon_Newton = epsilon_g00 + epsilon_source_norm + epsilon_tau_orbit_charge",
            "current_status": "conditional_plus_source_normalization_blocked",
            "empirical_bound_loaded": gdot.get("upper_bound", "MISSING_R9_BOUND"),
            "bound_units": gdot.get("units", ""),
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "limit_id": "LIM3135_3_PPN_gamma_readout",
            "arena": "PPN/light propagation",
            "required_readout": "gij_obs and g00_obs weak-field coefficients have GR values after quotient/readout",
            "standard_limit": "gamma-1=0 for GR",
            "mts_residual": "epsilon_PPN_gamma_readout",
            "current_status": "source_bound_loaded_mts_prediction_missing",
            "empirical_bound_loaded": gamma.get("upper_bound", "MISSING_R3_BOUND"),
            "bound_units": gamma.get("units", ""),
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "limit_id": "LIM3135_4_null_EM_geometric_optics",
            "arena": "photons/EM rays",
            "required_readout": "EM high-frequency rays use the observed cone g_obs(k,k)=0",
            "standard_limit": "d tau_clk=0 on null rays; light bending/Shapiro read from g_obs",
            "mts_residual": "epsilon_EM_cone + epsilon_Poynting_flow",
            "current_status": "conditional_EM_block_not_parent_signed_here",
            "empirical_bound_loaded": "Cassini gamma row also constrains light propagation if mapped",
            "bound_units": gamma.get("units", ""),
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "limit_id": "LIM3135_5_Poynting_stress_channel",
            "arena": "Maxwell/EM stress and Poynting vector",
            "required_readout": "S_EM=-1/4 integral sqrt(-g_obs) F^2 and T_EM/Poynting flux are computed in the observed coframe",
            "standard_limit": "nabla_mu T_EM^{mu nu}=0 in free field, or =-F^{nu lambda}j_lambda with current",
            "mts_residual": "epsilon_EM_flow = direct background-flow energy flux not represented by observed Maxwell stress",
            "current_status": "residual_channel_defined_no_claim",
            "empirical_bound_loaded": "not_loaded_in_3135",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def build_residuals(clock_bound: dict[str, Any]) -> list[dict[str, Any]]:
    now = stamp()
    redshift = local_bound("R2_clock_redshift")
    gdot = local_bound("R9_Gdot")
    gamma = local_bound("R3_gamma")
    return [
        {
            "residual_id": "TSR3135_0_clock_product_alpha",
            "symbol": "epsilon_clock_alpha_product",
            "definition": "|kappa_alpha tau_clock_time| entering alpha-sensitive clock ratios",
            "current_bound_or_input": clock_bound["bound_1sigma_yr_inv"],
            "units": "yr^-1",
            "source_status": "source_bound_loaded_mts_product_missing",
            "next_action": "derive kappa_alpha*tau_clock_time=0 or provide source-backed MTS product",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_paths": str(ROOT / "source-intake" / "mts_residuals" / "P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv"),
            "generated_utc": now,
        },
        {
            "residual_id": "TSR3135_1_clock_redshift",
            "symbol": "epsilon_GR_redshift",
            "definition": "observable redshift deviation after readout",
            "current_bound_or_input": redshift.get("upper_bound", "MISSING_R2_BOUND"),
            "units": redshift.get("units", "dimensionless"),
            "source_status": "source_bound_loaded_mts_prediction_missing",
            "next_action": "derive observed g00 coefficient and clock normalization",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_paths": str(ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"),
            "generated_utc": now,
        },
        {
            "residual_id": "TSR3135_2_tau_role_mismatch",
            "symbol": "epsilon_tau_role",
            "definition": "mismatch between tau_clock, tau_charge, tau_source, tau_orbit, and tau_boundary",
            "current_bound_or_input": "MISSING_SAME_TAU_NORMALIZATION_THEOREM",
            "units": "dimensionless_or_contextual",
            "source_status": "blocked_by_685_688",
            "next_action": "prove one parent-selected tau or retain mismatch as finite residual",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_paths": str(ROOT / "source-intake" / "mts_residuals" / "P8_Y5_R10_685_KILLING_CLOCK_GATE.csv") + ";" + str(ROOT / "source-intake" / "mts_residuals" / "P8_Y5_R10_688_SYMGRAD_TAU_DECOMPOSITION.csv"),
            "generated_utc": now,
        },
        {
            "residual_id": "TSR3135_3_readout_direct",
            "symbol": "epsilon_clock_readout_direct",
            "definition": "direct internal-flow or representative-shadow contribution to observed clock/coframe readout",
            "current_bound_or_input": "MISSING_C_Obs_e_AND_C_shadow_abs_ZERO_OR_BOUND",
            "units": "dimensionless",
            "source_status": "3134_leakage_head_carried_forward",
            "next_action": "prove C_Obs_e/C_shadow_abs vanish for clocks or fill finite bounds",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_paths": str(ROOT / "source-intake" / "mts_residuals" / "P8_Y5_R2FR_3134_FINITE_LEAKAGE_CARRY_FORWARD.csv"),
            "generated_utc": now,
        },
        {
            "residual_id": "TSR3135_4_Newton_Gdot_or_mass_time_drift",
            "symbol": "epsilon_Gdot_source_time",
            "definition": "time-flow induced drift in source normalization, G, or mass scale",
            "current_bound_or_input": gdot.get("upper_bound", "MISSING_R9_BOUND"),
            "units": gdot.get("units", "yr^-1"),
            "source_status": "source_bound_loaded_mts_projection_missing",
            "next_action": "derive no source normalization drift or map MTS source drift to R9",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_paths": str(ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"),
            "generated_utc": now,
        },
        {
            "residual_id": "TSR3135_5_PPN_gamma_readout",
            "symbol": "epsilon_PPN_gamma_readout",
            "definition": "readout mismatch in spatial curvature/light propagation coefficient gamma",
            "current_bound_or_input": gamma.get("upper_bound", "MISSING_R3_BOUND"),
            "units": gamma.get("units", "dimensionless"),
            "source_status": "source_bound_loaded_mts_prediction_missing",
            "next_action": "derive observed weak-field metric coefficients or keep PPN residual vector",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_paths": str(ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"),
            "generated_utc": now,
        },
        {
            "residual_id": "TSR3135_6_EM_Poynting_flow",
            "symbol": "epsilon_EM_flow",
            "definition": "background-flow energy flux entering EM/Poynting stress outside observed Maxwell stress",
            "current_bound_or_input": "MISSING_EM_PARENT_MAXWELL_INHERITANCE_OR_BOUND",
            "units": "stress_flux_normalized",
            "source_status": "new_residual_channel_defined_nonclaim",
            "next_action": "derive Maxwell block from observed coframe or create EM stress-flow bound rows",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_paths": str(ROOT / "3134-Y5-R2FR-parent-quotient-map-and-matter-pullback-reduction-under-AX1090.md"),
            "generated_utc": now,
        },
    ]


def build_gate(lemma_rows: list[dict[str, Any]], limit_rows: list[dict[str, Any]], residual_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    formal_rows = sum(1 for row in lemma_rows if "formal_pass" in row.get("proof_status", "") or "conditional_lemma_valid" in row.get("proof_status", ""))
    missing_rows = sum(1 for row in residual_rows if "MISSING" in str(row.get("current_bound_or_input", "")))
    now = stamp()
    return [
        {
            "gate_id": "CRG3135_0_sign_quarantine",
            "gate": "internal_flow_sign_not_direct_observable",
            "status": "formal_pass_conditional",
            "claim_allowed": "false",
            "reason": "observable clock time is read through R_clock(q(Phi), path), so internal-flow sign is quarantined unless it leaks into q, constants, matter phase, or EM stress",
            "next_action": "parent-sign R_clock/q or bound leak residuals",
            "generated_utc": now,
        },
        {
            "gate_id": "CRG3135_1_SR_GR_limit",
            "gate": "SR_GR_limits_after_readout",
            "status": "conditional_not_parent_signed",
            "claim_allowed": "false",
            "reason": f"{formal_rows} conditional readout lemmas are written, but MTS-side epsilon terms are not zeroed or bounded",
            "next_action": "derive observed coframe metric coefficients and matter geodesic/clock action",
            "generated_utc": now,
        },
        {
            "gate_id": "CRG3135_2_clock_bounds",
            "gate": "real_clock_bounds_loaded",
            "status": "source_bounds_loaded_no_MTS_product",
            "claim_allowed": "false",
            "reason": "clock product rows give numeric caps, but no kappa_alpha*tau_clock_time prediction or theorem-zero is present",
            "next_action": "target constant-superselection/no-marker theorem or source-backed product input",
            "generated_utc": now,
        },
        {
            "gate_id": "CRG3135_3_tau_generator",
            "gate": "same_tau_for_charge_clock_source_orbit_boundary",
            "status": "fail_for_claim",
            "claim_allowed": "false",
            "reason": "685/688 still block parent-selected tau, Killing stationarity, clock normalization, and role matching",
            "next_action": "do not use clock-product tau as Hamiltonian/GM tau",
            "generated_utc": now,
        },
        {
            "gate_id": "CRG3135_4_EM_Poynting",
            "gate": "EM_stress_Poynting_readout_channel",
            "status": "new_residual_channel_defined_no_claim",
            "claim_allowed": "false",
            "reason": "Poynting vector must be observed-coframe Maxwell stress or finite epsilon_EM_flow; not assumed zero",
            "next_action": "derive Maxwell block inheritance or fill EM flow residual rows",
            "generated_utc": now,
        },
        {
            "gate_id": "CRG3135_5_total",
            "gate": "local_GR_Newton_Maxwell_claim",
            "status": "not_claim_ready",
            "claim_allowed": "false",
            "reason": f"sign issue is structurally quarantined, but {missing_rows} residual channels still carry missing theorem-zero/source-bound inputs",
            "next_action": "3136 should attack observed coframe clock functional ownership or the EM/Maxwell inheritance residual",
            "generated_utc": now,
        },
    ]


def validate(inputs: list[dict[str, Any]], lemma_rows: list[dict[str, Any]], limit_rows: list[dict[str, Any]], residual_rows: list[dict[str, Any]], gate_rows: list[dict[str, Any]], clock_bound: dict[str, Any]) -> list[dict[str, Any]]:
    now = stamp()
    all_sources_exist = all(row.get("exists") == "true" for row in inputs if row.get("required") == "true")
    no_claim_leak = all(str(row.get("claim_allowed", "")).lower() == "false" and str(row.get("valid_for_claim", "false")).lower() == "false" for row in lemma_rows + limit_rows + residual_rows)
    gates_no_claim = all(str(row.get("claim_allowed", "")).lower() == "false" for row in gate_rows)
    required_limits = {"LIM3135_0_SR_timelike_clock", "LIM3135_1_GR_redshift_clock", "LIM3135_2_Newton_slow_motion", "LIM3135_4_null_EM_geometric_optics", "LIM3135_5_Poynting_stress_channel"}
    present_limits = {row.get("limit_id", "") for row in limit_rows}
    missing_residual_markers = sum(1 for row in residual_rows if "MISSING" in str(row.get("current_bound_or_input", "")))
    return [
        {
            "check_id": "VAL3135_0_sources_exist",
            "status": "pass" if all_sources_exist else "fail",
            "details": json.dumps({row["source_id"]: {"exists": row["exists"], "path": row["resolved_path"]} for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3135_1_readout_lemma_written",
            "status": "pass" if len(lemma_rows) >= 6 and any(row.get("lemma_id") == "CRL3135_0_variable_separation" for row in lemma_rows) else "fail",
            "details": f"lemma_rows={len(lemma_rows)}",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3135_2_SR_GR_Newton_null_EM_limits_present",
            "status": "pass" if required_limits.issubset(present_limits) else "fail",
            "details": json.dumps(sorted(present_limits), ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3135_3_clock_bound_loaded_numeric",
            "status": "pass" if parse_float(str(clock_bound.get("bound_1sigma_yr_inv", ""))) is not None else "fail",
            "details": json.dumps(clock_bound, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3135_4_residuals_retained",
            "status": "pass" if missing_residual_markers >= 3 else "fail",
            "details": f"missing_residual_markers={missing_residual_markers}; residual_rows={len(residual_rows)}",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3135_5_no_claim_leak",
            "status": "pass" if no_claim_leak and gates_no_claim else "fail",
            "details": "",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = annotate_inputs(source_inputs())
    clock_bound = strongest_clock_bound()
    lemma_rows = build_lemma(clock_bound)
    limit_rows = build_limits()
    residual_rows = build_residuals(clock_bound)
    gate_rows = build_gate(lemma_rows, limit_rows, residual_rows)
    validation_rows = validate(inputs, lemma_rows, limit_rows, residual_rows, gate_rows, clock_bound)

    write_csv(INPUTS, inputs)
    write_csv(LEMMA, lemma_rows)
    write_csv(LIMITS, limit_rows)
    write_csv(RESIDUALS, residual_rows)
    write_csv(GATE, gate_rows)
    write_csv(VALIDATION, validation_rows)


if __name__ == "__main__":
    main()


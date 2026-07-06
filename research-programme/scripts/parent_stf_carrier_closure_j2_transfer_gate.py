from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Iterable, List


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    row_list = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not row_list:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row_list[0].keys()))
        writer.writeheader()
        writer.writerows(row_list)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def closure_clause_rows() -> List[Dict[str, object]]:
    return [
        {
            "clause_id": "PAC4482_0_scalar_exhaustion",
            "carrier_route": "scalar_marker_only",
            "closure_theorem": "If the local marker/support alphabet before variation contains only SO(3)-scalar amplitudes and h_ij, then Q_M_TF^{ij}=0 by the 4480 representation theorem.",
            "current_evidence": "core scalar psi action plus 4480 theorem",
            "missing_signature": "exhaustive parent alphabet certificate: no hidden vector, flux, boundary, source, phase, or integrated-out orientation variables",
            "closure_status": "PARTIAL_NOT_EXHAUSTIVE",
            "Z_orientation_signed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "PAC4482_1_wave_flux_firewall",
            "carrier_route": "wave_EM_Poynting_flux",
            "closure_theorem": "Wave/EM/Poynting carriers are harmless only if they enter after variation as readout/ordinary Hilbert stress, are quotient-vertical, or are isotropically averaged before local projection.",
            "current_evidence": "4480/4481 keep Poynting and wave flux as live STF carriers; formal claims include private EM side-channel work but not a global parent alphabet closure",
            "missing_signature": "parent proof that S^i, k^i, polarization e_TF^{ij}, and radiation stress do not enter marker support as independent l=2 carriers",
            "closure_status": "LIVE_COUNTERROUTE_UNSIGNED",
            "Z_orientation_signed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "PAC4482_2_tidal_hessian_firewall",
            "carrier_route": "tidal_Hessian_STF",
            "closure_theorem": "Tracefree Hessian/tidal carriers close only if B_eff=0, Sigma_H=0, or the tracefree response is quotient-vertical/common-mode under the observed metric map.",
            "current_evidence": "1950/1951 isolate B_eff and 3182 shows tracefree Hessian carrier enters metric slip under identity readout",
            "missing_signature": "parent-signed B_eff=0 or Sigma_H=0 theorem; otherwise finite STF response bound",
            "closure_status": "LIVE_STF_RESPONSE_UNSIGNED",
            "Z_orientation_signed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "PAC4482_3_boundary_orientation_firewall",
            "carrier_route": "boundary_normal_flux",
            "closure_theorem": "Boundary normal l=2 closes only if boundary data are fixed/topological/no-flux, symplectic l=2 flux vanishes, or the extra branch has no independent l=2 boundary degree of freedom.",
            "current_evidence": "867 boundary orientation warning; 1955 no-extra-boundary clause",
            "missing_signature": "parent boundary term and symplectic-flux certificate",
            "closure_status": "LIVE_BOUNDARY_UNSIGNED",
            "Z_orientation_signed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "PAC4482_4_source_worldtube_firewall",
            "carrier_route": "source_worldtube_l2",
            "closure_theorem": "Ordinary source multipoles are GR baseline only if the local parent action has the same EH matter source map; extra source-map residual l=2 must vanish or be bounded.",
            "current_evidence": "1954 baseline subtraction and 1955 EH same-source map contract",
            "missing_signature": "universal metric coupling, normalization, extra-sector source silence, and source-domain transfer",
            "closure_status": "LIVE_SAME_SOURCE_UNSIGNED",
            "Z_orientation_signed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "PAC4482_5_phase_carrier_measure",
            "carrier_route": "phase_carrier_weights",
            "closure_theorem": "Phase/carrier ensembles close the l=2 route only if their direction distribution is isotropic or their anisotropic weights are bounded by the finite scorer.",
            "current_evidence": "2275 carrier inventory represents q tangent algebraically but leaves parent multimode permission and smoothing unsigned",
            "missing_signature": "parent phase ensemble measure, isotropic averaging, cone guards, and smoothing theorem",
            "closure_status": "LIVE_CARRIER_MEASURE_UNSIGNED",
            "Z_orientation_signed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "PAC4482_6_verdict",
            "carrier_route": "all_STF_carriers",
            "closure_theorem": "Z_orientation=True only if PAC4482_0 through PAC4482_5 close together.",
            "current_evidence": "4481 sweep shows scalar branch and non-scalar carrier routes both present/live in the corpus",
            "missing_signature": "global parent STF carrier alphabet closure",
            "closure_status": "ZERO_ROUTE_NOT_SIGNED_USE_TRANSFER_SCORER",
            "Z_orientation_signed": False,
            "valid_for_claim": False,
        },
    ]


def corrected_j2_transfer_rows() -> List[Dict[str, object]]:
    return [
        {
            "transfer_id": "J2T4482_0_metric_normalization",
            "object": "public exterior J2 metric amplitude",
            "formula": "A_metric(r)=2*epsilon_sun_surface*J2*rho^-3, rho=r/R_sun",
            "derivation": "From Phi_J2=(GM/r) J2 (R_s/r)^2 P2 and g00=-(1+2 Phi/c^2), the dimensionless public metric P2 amplitude carries 2 GM/(c^2 r).",
            "numeric_surface_factor": "2*epsilon_sun_surface=4.245005140290714e-6",
            "status": "DERIVED_BY_3170_IMPORTED",
            "valid_for_claim": False,
        },
        {
            "transfer_id": "J2T4482_1_Upsilon_definition",
            "object": "Upsilon_J2",
            "formula": "A_metric_solar_surface = Upsilon_J2*K2*C_K2_unit",
            "derivation": "3171 proves current artifacts do not identify K2*C_K2_unit with the solar exterior public metric amplitude; Upsilon_J2 is the missing transfer kernel.",
            "numeric_surface_factor": "C_K2_unit=3.593766357482964e-24",
            "status": "TRANSFER_KERNEL_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "transfer_id": "J2T4482_2_corrected_J2eff",
            "object": "J2_eff",
            "formula": "J2_eff = Upsilon_J2*K2*C_K2_unit*rho^3/(2*epsilon_sun_surface)",
            "derivation": "Equate Upsilon_J2*K2*C_K2_unit to A_metric(r)=2 epsilon J2 rho^-3.",
            "numeric_surface_factor": "J2_eff(K2=1,rho=1,Upsilon=1)=8.465870449421527e-19",
            "status": "DERIVED_SYMBOLIC_TRANSFER",
            "valid_for_claim": False,
        },
        {
            "transfer_id": "J2T4482_3_K2_bound_scaling",
            "object": "K2_bound",
            "formula": "K2 <= [2*epsilon_sun_surface*J2_bound*rho^-3]/[abs(Upsilon_J2)*C_K2_unit]",
            "derivation": "Invert the corrected J2_eff map. At rho=1, 3170 half-range proxy gives K2 <= 3.898004369090586e10/|Upsilon_J2|.",
            "numeric_surface_factor": "ZK scale:2.362426890357931e11/|Upsilon|; half-range:3.898004369090586e10/|Upsilon|",
            "status": "DERIVED_CONDITIONAL_PRESSURE_ROW",
            "valid_for_claim": False,
        },
        {
            "transfer_id": "J2T4482_4_nonidentifiability",
            "object": "current_K2_to_J2_score",
            "formula": "Upsilon_J2 is free in current artifacts; Upsilon=0 and Upsilon=1 both preserve existing K2 bookkeeping",
            "derivation": "3171 counterfamily shows K2 can fail to source solar J2 or can source the corrected profile; current parent equations do not choose.",
            "numeric_surface_factor": "not_scoreable_until_Upsilon_J2_is_derived_or_bounded",
            "status": "NONIDENTIFIABILITY_IMPORTED",
            "valid_for_claim": False,
        },
    ]


def finite_l2_scorer_rows() -> List[Dict[str, object]]:
    return [
        {
            "scorer_id": "FLS4482_0_marker_amplitude_to_J2",
            "quantity": "A_marker_surface",
            "formula": "J2_eff_marker = A_marker_surface/(2*epsilon_sun_surface) at rho=1",
            "needed_inputs": "A_marker_surface from lambda_M*zeta_Q*Q_M_TF*H_TF/(2N), metric readout normalization, source-domain frame",
            "current_value": "MISSING_MARKER_TO_PUBLIC_METRIC_AMPLITUDE",
            "status": "SCORER_BRIDGE_DERIVED_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "scorer_id": "FLS4482_1_compact_support_envelope",
            "quantity": "A_marker_bound",
            "formula": "A_marker <= |lambda_M||zeta_Q| mu0_abs ell_sup^2/(2|N|L_loc^2)",
            "needed_inputs": "lambda_M, zeta_Q, mu0_abs, ell_sup, N, L_loc, public metric projection",
            "current_value": "MISSING_FINITE_MARKER_COEFFICIENTS",
            "status": "4480_BOUND_IMPORTED_NOT_NUMERIC",
            "valid_for_claim": False,
        },
        {
            "scorer_id": "FLS4482_2_J2_pressure_gate",
            "quantity": "J2_pressure",
            "formula": "A_marker_surface <= 2*epsilon_sun_surface*J2_bound",
            "needed_inputs": "choose bound row: solar total scale, half-range proxy, or formal covariance; source-domain convention",
            "current_value": "CONDITIONAL_J2_PRESSURE_AVAILABLE",
            "status": "NUMERIC_PRESSURE_EXISTS_TRANSFER_BLOCKED",
            "valid_for_claim": False,
        },
        {
            "scorer_id": "FLS4482_3_residual_l2_after_GR_baseline",
            "quantity": "S_TF_extra",
            "formula": "abs(S_TF_extra)<=||W_STF||_1(||K2|| ||DeltaJ2|| + ||K2X|| ||P2R_extra|| + ||H2|| ||Deltah2||)",
            "needed_inputs": "W_STF, DeltaJ2, P2R_extra, Deltah2 from 1955 or zero theorems",
            "current_value": "MISSING_RESIDUAL_L2_ENVELOPES",
            "status": "FAIR_GR_BASELINE_SCORER_STAGED",
            "valid_for_claim": False,
        },
        {
            "scorer_id": "FLS4482_4_no_cancellation_rule",
            "quantity": "finite_l2_claim_gate",
            "formula": "pass only if each arena l2 residual is separately zero or below its own sourced bound",
            "needed_inputs": "J2/Shapiro, PPN_STF, clock_Q, orbital_Q and residual-l2 rows",
            "current_value": "NOT_CLAIM_READY",
            "status": "NO_CANCELLATION_ENVELOPE",
            "valid_for_claim": False,
        },
    ]


def owner_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "input_id": "OI4482_0_Upsilon_J2",
            "symbol": "Upsilon_J2",
            "definition": "transfer from K2*C_K2_unit to solar-surface exterior public metric P2 amplitude",
            "current_value": "MISSING_PARENT_PROFILE_AND_METRIC_PROJECTION",
            "needed_for": "J2_eff scoring",
            "source_ref": "P8_Y5_R2FR_3171_UPSILON_J2_TRANSFER_CONTRACT.csv",
            "valid_for_claim": False,
        },
        {
            "input_id": "OI4482_1_Pi_J2_metric",
            "symbol": "Pi_J2_metric",
            "definition": "public metric injection kernel mapping finite MTS l=2 residual into exterior metric amplitude",
            "current_value": "MISSING_PUBLIC_METRIC_PROJECTION_KERNEL",
            "needed_for": "Upsilon_J2 or marker amplitude scorer",
            "source_ref": "P8_Y5_R2FR_3171_PROFILE_OWNER_AUDIT.csv",
            "valid_for_claim": False,
        },
        {
            "input_id": "OI4482_2_Green_profile",
            "symbol": "G_l2(r,r')",
            "definition": "exterior l=2 radial Green/profile owner; standard J2 requires r^-3",
            "current_value": "MISSING_EXTERIOR_R_MINUS_3_OWNER",
            "needed_for": "rho scaling and solar-domain transfer",
            "source_ref": "3171 profile owner audit",
            "valid_for_claim": False,
        },
        {
            "input_id": "OI4482_3_source_domain_transfer",
            "symbol": "T_source",
            "definition": "Earth/internal K2 source-domain lane to solar exterior l=2 lane, or direct solar K2 construction",
            "current_value": "MISSING_PARENT_SOURCE_DOMAIN_UNIVERSALITY",
            "needed_for": "using solar J2 bounds on K2",
            "source_ref": "P8_Y5_R2FR_3169_SOLAR_J2_EQUIVALENT_TRANSFER.csv",
            "valid_for_claim": False,
        },
        {
            "input_id": "OI4482_4_residual_l2_envelopes",
            "symbol": "DeltaJ2, P2R_extra, Deltah2, W_STF",
            "definition": "fair residual-l2 bound factors after GR baseline subtraction",
            "current_value": "MISSING_RESIDUAL_ENVELOPES_AND_READOUT_NORM",
            "needed_for": "finite scorer if zero route fails",
            "source_ref": "P8_Y5_PARENT_QLOC_1955_RESIDUAL_L2_BOUND_LEDGER.csv",
            "valid_for_claim": False,
        },
    ]


def decision_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4482_0_zero_route",
            "finding": "parent STF carrier alphabet closure cannot be signed from current evidence",
            "reason": "wave/flux, tidal/STF, boundary, source-worldtube and phase-carrier routes each need a parent firewall",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4482_1_transfer_route",
            "finding": "corrected J2eff transfer is derived symbolically with Upsilon_J2",
            "reason": "3170 supplies the metric normalization; 3171 supplies the non-identifiability proof and Upsilon_J2 contract",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4482_2_best_next",
            "finding": "the next decisive derivation is Pi_J2_metric/exterior r^-3 Green owner or a finite residual-l2 scorer",
            "reason": "more external J2 data cannot score the model until the parent metric/radial/source transfer exists",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    source_rows: List[Dict[str, object]],
    closure_rows: List[Dict[str, object]],
    transfer_rows: List[Dict[str, object]],
    scorer_rows: List[Dict[str, object]],
    input_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    sources_ok = all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in source_rows)
    zero_signed = any(row.get("clause_id") == "PAC4482_6_verdict" and row.get("Z_orientation_signed") is True for row in closure_rows)
    transfer_written = any(row.get("transfer_id") == "J2T4482_2_corrected_J2eff" for row in transfer_rows)
    scorer_written = any(row.get("scorer_id") == "FLS4482_3_residual_l2_after_GR_baseline" for row in scorer_rows)
    inputs_ready = all(
        "MISSING" not in str(row.get("current_value", "")) and row.get("valid_for_claim") is True
        for row in input_rows
    )
    return [
        {
            "gate_id": "CG4482_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": sources_ok,
            "claim_allowed": False,
            "detail": "4481, 3170, 3171, 1955 and 3169 transfer rows are cited",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4482_1_parent_alphabet_closed",
            "claim": "parent signs absence/routing of all STF carrier routes",
            "gate_pass": zero_signed,
            "claim_allowed": False,
            "detail": "carrier firewalls remain unsigned; Z_orientation not promoted",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4482_2_corrected_J2_transfer_written",
            "claim": "corrected Upsilon_J2 transfer formula is written",
            "gate_pass": transfer_written,
            "claim_allowed": False,
            "detail": "J2_eff = Upsilon_J2*K2*C_K2_unit*rho^3/(2 epsilon_sun_surface)",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4482_3_finite_l2_scorer_written",
            "claim": "finite l2 scorer bridge is written",
            "gate_pass": scorer_written,
            "claim_allowed": False,
            "detail": "marker amplitude, residual-l2 after GR baseline, and no-cancellation gates are staged",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4482_4_numeric_claim_ready",
            "claim": "J2/l2 scorer has claim-grade parent/source inputs",
            "gate_pass": inputs_ready,
            "claim_allowed": False,
            "detail": "Upsilon_J2, Pi_J2_metric, Green profile, source transfer and residual envelopes remain missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4482_5_no_generated_claim_rows",
            "claim": "no generated row is promoted to local-GR evidence",
            "gate_pass": all(
                str(row.get("valid_for_claim")).lower() == "false"
                for group in [source_rows, closure_rows, transfer_rows, scorer_rows, input_rows]
                for row in group
            ),
            "claim_allowed": False,
            "detail": "4482 is a transfer/scorer derivation checkpoint, not a pass",
            "valid_for_claim": False,
        },
    ]

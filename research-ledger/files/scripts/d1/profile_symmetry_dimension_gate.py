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


def local_spatial_symmetry_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "LSS4479_0_spatial_worldtube_branch",
            "clause": "local tests use a spatial profile after Hamiltonian/worldtube split",
            "formal_statement": "F_M(t,x) -> F_M^Sigma(x) on Sigma_t for static/adiabatic local tests, with time as the evolution parameter rather than a support coordinate",
            "derivation": "PPN, R10, clock-redshift and orbital local limits are read from fields on local spatial slices after source charges are defined. If no finite temporal marker kernel is retained, the profile moment expansion is spatial.",
            "zero_or_bound_result": "d_eff=3 and the gradient coefficient is mu2_M/(6 L_loc^2)",
            "current_status": "CONDITIONAL_LOCAL_SPATIAL_BRANCH",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "LSS4479_1_temporal_smearing_counterroute",
            "clause": "covariant time-smearing is a finite residual, not a free d_eff choice",
            "formal_statement": "F_M(tau,x)=K_M(tau) f_M(x) gives eta0 O + eta1 dt O + 1/2 eta2 dt^2 O + ...",
            "derivation": "If the marker has temporal support, the expansion includes time derivatives. These feed clock, Lorentz, locality, Gdot and orbital phase residuals, so d_eff=4 cannot be used as harmless covariance dressing.",
            "zero_or_bound_result": "temporal residuals vanish only if eta1_M=eta2_M=0 or tau_M/T_loc is bounded",
            "current_status": "TEMPORAL_SMEARING_BOUND_REQUIRED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "LSS4479_2_centering_theorem",
            "clause": "positive compact profiles can be centred exactly",
            "formal_statement": "x_M = (int x f_M)/(int f_M) gives D_M^i=int (x-x_M)^i F_M=0 for positive nonzero mu0_M",
            "derivation": "The dipole term is a coordinate-centre artefact for positive profiles. Choosing the centroid removes it exactly. Signed profiles require an absolute-centre guard or a finite signed dipole row.",
            "zero_or_bound_result": "D_M^i=0 on positive centred branch; abs(D_M)<=ell_sup mu0_abs for signed fallback",
            "current_status": "CENTERING_DERIVED_SIGNED_FALLBACK_LIVE",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "LSS4479_3_isotropy_no_orientation_carrier",
            "clause": "isotropy follows only if no orientation/nematic/tidal marker carrier exists",
            "formal_statement": "Q_M_TF^{ij}=0 iff the finite marker support has SO(3) little-group symmetry or the parent action has no orientation carrier that can select a tracefree tensor",
            "derivation": "A scalar support amplitude does not by itself carry a preferred direction. But an anisotropic body, nematic marker, tidal alignment, spin axis or boundary orientation can generate a tracefree second moment.",
            "zero_or_bound_result": "Q_M_TF=0 on the no-orientation branch; otherwise a quadrupole residual is mandatory",
            "current_status": "ISOTROPY_PARENT_UNSIGNED_ORIENTATION_COUNTERROUTE_LIVE",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "LSS4479_4_quadrupole_bound",
            "clause": "tracefree quadrupole has a compact-support bound",
            "formal_statement": "mu2_M^{ij}=(mu2_M/3)h^{ij}+Q_M_TF^{ij}; ||Q_M_TF|| <= mu2_abs <= ell_sup^2 mu0_abs on the spatial branch",
            "derivation": "The tracefree part cannot exceed the absolute second moment. Compact support bounds the absolute second moment by the support radius squared times total absolute profile weight.",
            "zero_or_bound_result": "abs(R_quad) <= abs(lambda_M)*abs(zeta_Q)*ell_sup^2*mu0_abs/(2 abs(N_a) L_loc^2)",
            "current_status": "DERIVED_QUADRUPOLE_BOUND",
            "parent_signed": True,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "LSS4479_5_dipole_bound",
            "clause": "unremoved dipole has a compact-support bound",
            "formal_statement": "D_M^i=int y^i F_M and ||D_M|| <= ell_sup mu0_abs",
            "derivation": "If profile centering is unavailable or the signed profile has cancellations, the first moment is still bounded by support radius times absolute profile weight.",
            "zero_or_bound_result": "abs(R_dip) <= abs(lambda_M)*abs(zeta_dip)*ell_sup*mu0_abs/(abs(N_a) L_loc)",
            "current_status": "DERIVED_DIPOLE_BOUND",
            "parent_signed": True,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "LSS4479_6_verdict",
            "clause": "local d_eff=3 plus centering/isotropy is conditional, but finite anisotropy is bound-ready",
            "formal_statement": "local clean branch requires no temporal smearing, centroid-valid profile and no orientation carrier; otherwise temporal, dipole and quadrupole residual rows are used",
            "derivation": "4479 proves the shape assumptions as conditional branches and derives componentwise fallback bounds. Current MTS has not parent-signed no-time-smearing or no-orientation carrier.",
            "zero_or_bound_result": "no local-GR/R10 claim; anisotropic residual rows staged",
            "current_status": "SPATIAL_SYMMETRY_BRANCH_PARENT_UNSIGNED_ANISOTROPY_BOUNDS_DERIVED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def anisotropy_bound_rows() -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "AB4479_0_temporal_kernel",
            "quantity": "tau_M, eta1_M, eta2_M",
            "residual_formula": "R_time <= abs(lambda_M)*(abs(zeta_t1)*abs(eta1_M)/T_loc + abs(zeta_t2)*abs(eta2_M)/(2 T_loc^2))/abs(N_a)",
            "zero_condition": "no finite temporal marker support, or K_M is instantaneous/even with eta1=eta2=0 at local-test order",
            "needed_inputs": "temporal kernel; tau_M; local timescale T_loc; clock/Lorentz projection",
            "target_arenas": "clock;Lorentz;Gdot;orbital_phase",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "bound_id": "AB4479_1_dipole",
            "quantity": "D_M^i",
            "residual_formula": "R_dip <= abs(lambda_M)*abs(zeta_dip)*ell_sup*mu0_abs/(abs(N_a)*L_loc)",
            "zero_condition": "positive profile centred at x_M, or signed-profile dipole source proves D_M^i=0",
            "needed_inputs": "centering proof; ell_sup; mu0_abs; zeta_dip; N_a; L_loc",
            "target_arenas": "PPN_preferred_location;clock_gradient;orbital_anisotropy",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "bound_id": "AB4479_2_quadrupole",
            "quantity": "Q_M_TF^{ij}",
            "residual_formula": "R_quad <= abs(lambda_M)*abs(zeta_Q)*ell_sup^2*mu0_abs/(2*abs(N_a)*L_loc^2)",
            "zero_condition": "SO(3)-isotropic support or no orientation/nematic/tidal carrier in parent action",
            "needed_inputs": "orientation-carrier zero proof or Q_M_TF bound; ell_sup; mu0_abs; zeta_Q; N_a; L_loc",
            "target_arenas": "PPN_xi_alpha;clock_anisotropy;orbital_precession",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "bound_id": "AB4479_3_dimension_branch",
            "quantity": "d_eff",
            "residual_formula": "d_eff=3 gives mu2/(6 L_loc^2); d_eff=4 gives mu2/(8 L_loc^2) plus temporal residual R_time",
            "zero_condition": "Hamiltonian local spatial branch with no time-smearing marker",
            "needed_inputs": "support branch; temporal kernel absence; local-test slicing convention",
            "target_arenas": "R10;PPN;clock;orbital",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "bound_id": "AB4479_4_component_envelope",
            "quantity": "R_shape_abs",
            "residual_formula": "R_shape_abs = abs(R_time)+abs(R_dip)+abs(R_quad)",
            "zero_condition": "R_time=R_dip=R_quad=0 individually",
            "needed_inputs": "all temporal, dipole and quadrupole values or separate zero certificates",
            "target_arenas": "claim_gate_guard",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
    ]


def shape_branch_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "SBI4479_0_spatial_branch_certificate",
            "quantity": "Z_spatial",
            "definition": "certificate that local marker support is spatial on Sigma_t and not temporally smeared",
            "formula_or_test": "Z_spatial=True iff d_eff=3 branch signs and temporal kernel residuals vanish",
            "needed_inputs": "Hamiltonian/worldtube split; no temporal marker kernel; local-test readout convention",
            "current_value": "MISSING_SPATIAL_BRANCH_CERTIFICATE",
            "units": "boolean_certificate",
            "target": "d_eff=3;R_time=0",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "SBI4479_1_tau_M",
            "quantity": "tau_M",
            "definition": "temporal support width if covariant time-smearing survives",
            "formula_or_test": "tau_M^2=eta2_abs/eta0_abs or declared temporal kernel width",
            "needed_inputs": "K_M(tau); eta0_abs; eta2_abs; local clock/orbital timescale",
            "current_value": "MISSING_TEMPORAL_SUPPORT_WIDTH",
            "units": "s",
            "target": "clock;Lorentz;orbital_phase",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "SBI4479_2_centering_certificate",
            "quantity": "Z_center",
            "definition": "certificate that the marker dipole vanishes",
            "formula_or_test": "Z_center=True iff profile is positive and centred, or signed dipole D_M^i is independently zero",
            "needed_inputs": "profile sign branch; centroid definition; D_M^i value or proof",
            "current_value": "MISSING_CENTERING_CERTIFICATE",
            "units": "boolean_certificate",
            "target": "D_M^i=0;R_dip=0",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "SBI4479_3_orientation_carrier",
            "quantity": "Z_orientation",
            "definition": "certificate that no orientation/nematic/tidal marker carrier exists",
            "formula_or_test": "Z_orientation=True iff parent action/support has no vector, spin-axis, tidal, boundary-normal or nematic carrier that can source Q_M_TF",
            "needed_inputs": "parent support alphabet; body/orientation averaging; boundary orientation routing",
            "current_value": "MISSING_ORIENTATION_CARRIER_ZERO_CERTIFICATE",
            "units": "boolean_certificate",
            "target": "Q_M_TF=0;R_quad=0",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "SBI4479_4_D_M_bound",
            "quantity": "D_M_abs",
            "definition": "absolute dipole bound",
            "formula_or_test": "D_M_abs <= ell_sup mu0_abs",
            "needed_inputs": "ell_sup; mu0_abs; signed-profile guard",
            "current_value": "MISSING_DIPOLE_BOUND_INPUTS",
            "units": "m_times_profile_units",
            "target": "R_dip",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "SBI4479_5_Q_TF_bound",
            "quantity": "Q_M_TF_abs",
            "definition": "absolute tracefree quadrupole bound",
            "formula_or_test": "||Q_M_TF|| <= mu2_abs <= ell_sup^2 mu0_abs",
            "needed_inputs": "ell_sup; mu0_abs; tensor norm convention",
            "current_value": "MISSING_QUADRUPOLE_BOUND_INPUTS",
            "units": "m^2_times_profile_units",
            "target": "R_quad",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
    ]


def decision_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4479_0_spatial_branch",
            "finding": "d_eff=3 is justified only on the Hamiltonian local spatial branch with no temporal marker kernel",
            "consequence": "time-smearing is retained as an explicit clock/Lorentz/orbital residual",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4479_1_symmetry_branch",
            "finding": "centering and isotropy are derived as branch conditions, not assumed",
            "consequence": "dipole and tracefree quadrupole residuals are bounded if centering/isotropy do not sign",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4479_2_next_target",
            "finding": "the next sharp target is the orientation-carrier zero proof; if that fails, score the quadrupole residual",
            "consequence": "attack Z_orientation before trying numeric local scoring",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    source_rows: List[Dict[str, object]],
    theorem_rows: List[Dict[str, object]],
    bound_rows: List[Dict[str, object]],
    input_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    sources_ok = all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in source_rows)
    theorem_written = any(row.get("theorem_id") == "LSS4479_6_verdict" for row in theorem_rows)
    clean_branch_signed = any(row.get("theorem_id") == "LSS4479_6_verdict" and row.get("parent_signed") is True for row in theorem_rows)
    bounds_written = all(
        any(row.get("bound_id") == bound_id for row in bound_rows)
        for bound_id in ["AB4479_0_temporal_kernel", "AB4479_1_dipole", "AB4479_2_quadrupole", "AB4479_4_component_envelope"]
    )
    inputs_ready = all(
        "MISSING" not in str(row.get("current_value")) and row.get("status") != "BLOCKED_SOURCE_READY"
        for row in input_rows
    )
    no_claims = all(
        str(row.get("valid_for_claim")).lower() == "false"
        for group in [source_rows, theorem_rows, bound_rows, input_rows]
        for row in group
    )
    return [
        {
            "gate_id": "CG4479_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": sources_ok,
            "claim_allowed": False,
            "detail": "source register validates 4478 dimension/symmetry handoff",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4479_1_spatial_symmetry_theorem_written",
            "claim": "local d_eff/centering/isotropy branch theorem is explicit",
            "gate_pass": theorem_written,
            "claim_allowed": False,
            "detail": "spatial branch, time-smearing counterroute, centering, isotropy and bounds are written",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4479_2_clean_branch_parent_signed",
            "claim": "MTS parent signs d_eff=3, centering and isotropy",
            "gate_pass": clean_branch_signed,
            "claim_allowed": False,
            "detail": "no-time-smearing and no-orientation carrier remain unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4479_3_anisotropy_bounds_written",
            "claim": "temporal, dipole and quadrupole bounds are written",
            "gate_pass": bounds_written,
            "claim_allowed": False,
            "detail": "fallback residual bounds are componentwise and no-cancellation",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4479_4_bound_inputs_ready",
            "claim": "anisotropy bound inputs are numeric/source ready",
            "gate_pass": inputs_ready,
            "claim_allowed": False,
            "detail": "input rows still need spatial branch, temporal width, centering, orientation, dipole and quadrupole values",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4479_5_no_generated_claim_rows",
            "claim": "no generated row is promoted to public/local-GR evidence",
            "gate_pass": no_claims,
            "claim_allowed": False,
            "detail": "4479 is a branch theorem plus anisotropy bound pack",
            "valid_for_claim": False,
        },
    ]

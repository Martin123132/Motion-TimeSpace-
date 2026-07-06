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


def support_zero_certificate_rows() -> List[Dict[str, object]]:
    return [
        {
            "certificate_id": "SZC4478_0_support_carrier_absence",
            "clause": "no marker support carrier exists in the parent bulk alphabet",
            "formal_test": "F_M, support set Sigma_M, density rho_M, indicator 1_M, worldtube marker W_M, and boundary marker B_M are absent from S_bulk field variables and backgrounds",
            "derivation": "A profile is not a number; it requires a carrier. If the parent bulk alphabet has no carrier for marker support, then the functional F_M cannot be formed inside S_bulk.",
            "if_signed": "F_M is absent and mu0_M=mu2_M=lambda_M*mu0_M=lambda_M*mu2_M=0",
            "current_status": "SUPPORT_CARRIER_ABSENCE_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "SZC4478_1_external_readout_not_support",
            "clause": "external readout coordinates do not define physical support",
            "formal_test": "R_obs only labels O_read or J=0 diagnostic insertion; it does not define a body, density, support set, or material marker in S_bulk",
            "derivation": "Readout can choose where an observation is reported, but it cannot create a support density that enters the variational problem.",
            "if_signed": "readout branch has no F_M and no marker moments",
            "current_status": "CONDITIONAL_READOUT_SUPPORT_ZERO",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "SZC4478_2_worldtube_support_firewall",
            "clause": "source worldtube support is not automatically marker support",
            "formal_test": "Hilbert matter/EM worldtube W_H may exist, but no extra marker profile F_M multiplies local operators unless declared as a new material/source field",
            "derivation": "Ordinary source support belongs to T_H or T_EM. It becomes a marker support only if a separate profile couples through lambda_M F_M O_a.",
            "if_signed": "do not double-count ordinary matter support as marker support",
            "current_status": "WORLDLINE_WORLDTUBE_SEPARATION_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "SZC4478_3_boundary_support_separation",
            "clause": "boundary/reference support is fixed, topological, no-flux, or Hamiltonian-routed",
            "formal_test": "Pi_loc(delta S_boundary/delta support_marker)=0, otherwise boundary_marker is a separate finite support row",
            "derivation": "Boundary support can feed local matching even when no bulk profile exists. It must be routed or bounded separately.",
            "if_signed": "boundary support does not induce mu0_M or mu2_M in the bulk branch",
            "current_status": "BOUNDARY_SUPPORT_SEPARATION_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "SZC4478_4_finite_support_fallback",
            "clause": "if support survives, canonical moment inputs are mandatory",
            "formal_test": "F_M = Q_M f_M with int f_M=1 for positive profiles, or absolute/signed split for signed profiles; declare support dimension, centre, second moment and support radius",
            "derivation": "A finite profile can be normalized without loss of generality by moving its amplitude into Q_M or lambda_M; the shape then has moments that feed the 4477 projection law.",
            "if_signed": "finite branch becomes moment-scoreable rather than verbal",
            "current_status": "DERIVED_FALLBACK_LAW",
            "parent_signed": True,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "SZC4478_5_verdict",
            "clause": "profile/support zero is exact but parent-conditional",
            "formal_test": "SZC4478_0 through SZC4478_3 sign together, or SZC4478_4 finite support branch is used",
            "derivation": "4478 shows what would make F_M absent. Current MTS has not signed support-carrier absence or boundary separation, so first moment input rows remain live.",
            "if_signed": "marker moments vanish and lambda_M projection vector closes on the zero branch",
            "current_status": "SUPPORT_ZERO_PARENT_UNSIGNED_FIRST_MOMENT_INPUTS_STAGED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def first_moment_input_law_rows() -> List[Dict[str, object]]:
    return [
        {
            "law_id": "MIL4478_0_canonical_normalization",
            "branch": "positive finite profile",
            "derivation": "Write F_M(y)=Q_M f_M(y), with int d^d y f_M(y)=1 and f_M>=0. Then mu0_M=Q_M and mu2_M=Q_M ell_rms^2.",
            "derived_inputs": "Q_M; f_M; ell_rms^2=int r^2 f_M",
            "projection_use": "C_a^M=lambda_M Q_M*(zeta_a + zeta_grad_a ell_rms^2/(2 d_eff L_loc^2))/N_a",
            "current_status": "DERIVED_CANONICAL_PROFILE_LAW",
            "valid_for_claim": False,
        },
        {
            "law_id": "MIL4478_1_signed_profile_guard",
            "branch": "signed or oscillatory profile",
            "derivation": "Use mu0_M=int F_M, mu0_abs=int |F_M|, mu2_abs=int r^2 |F_M|. No claim may use cancellation in mu0_M unless mu0_abs and componentwise residuals are also bounded.",
            "derived_inputs": "mu0_M; mu0_abs; mu2_abs",
            "projection_use": "abs(C_a^M) <= abs(lambda_M)*(abs(zeta_a)*mu0_abs + abs(zeta_grad_a)*mu2_abs/(2 d_eff L_loc^2))/abs(N_a)",
            "current_status": "DERIVED_NO_CANCELLATION_PROFILE_GUARD",
            "valid_for_claim": False,
        },
        {
            "law_id": "MIL4478_2_support_dimension_branch",
            "branch": "local static tests",
            "derivation": "For local PPN/R10/clock/orbital tests after Hamiltonian/worldtube split, the marker profile is a spatial profile on Sigma_t, so d_eff=3 if no time-smearing marker is retained.",
            "derived_inputs": "d_eff=3 conditional branch",
            "projection_use": "gradient coefficient becomes mu2_M/(6 L_loc^2)",
            "current_status": "CONDITIONAL_LOCAL_SPATIAL_BRANCH",
            "valid_for_claim": False,
        },
        {
            "law_id": "MIL4478_3_covariant_smearing_branch",
            "branch": "covariant spacetime support",
            "derivation": "If the marker is a spacetime smearing profile, d_eff=4 may be used, but finite temporal support is then a clock/Lorentz/locality residual that must be bounded separately.",
            "derived_inputs": "d_eff=4 fallback plus temporal-support residual",
            "projection_use": "gradient coefficient becomes mu2_M/(8 L_loc^2) only after temporal support is physically justified",
            "current_status": "COVARIANT_BRANCH_REQUIRES_EXTRA_BOUND",
            "valid_for_claim": False,
        },
        {
            "law_id": "MIL4478_4_centering_choice",
            "branch": "finite support with chosen centre",
            "derivation": "Choose x_M by the profile centroid when mu0_M is nonzero: int y^i F_M=0. For signed profiles use absolute-centre or keep the dipole row D_M^i=int y^i F_M.",
            "derived_inputs": "centred=True, or D_M^i finite dipole row",
            "projection_use": "if centred, the first derivative term vanishes; if not, lambda_M zeta_dip D_M^i partial_i O_a/N_a is a new residual",
            "current_status": "DERIVED_CENTERING_OR_DIPOLE_FALLBACK",
            "valid_for_claim": False,
        },
        {
            "law_id": "MIL4478_5_isotropy_or_quadrupole",
            "branch": "second moment tensor",
            "derivation": "Decompose mu2_M^{ij}=(mu2_M/d_eff) h^{ij}+Q_M^{ij,TF}. Isotropy is Q_M^{ij,TF}=0; otherwise the tracefree quadrupole is a finite anisotropic local residual.",
            "derived_inputs": "mu2_M trace; Q_M_TF anisotropy row",
            "projection_use": "isotropic branch gives Laplacian correction; anisotropic branch adds lambda_M Q_M_TF^{ij} partial_i partial_j O_a/(2 N_a)",
            "current_status": "DERIVED_ISOTROPY_OR_QUADRUPOLE_FALLBACK",
            "valid_for_claim": False,
        },
        {
            "law_id": "MIL4478_6_support_radius_bound",
            "branch": "compact support",
            "derivation": "If supp(f_M) lies inside radius ell_sup, then ell_rms^2<=ell_sup^2 and mu2_abs<=ell_sup^2 mu0_abs.",
            "derived_inputs": "ell_sup; ell_rms bound; mu2_abs bound",
            "projection_use": "abs(gradient leakage) <= abs(lambda_M)*abs(zeta_grad_a)*mu0_abs*ell_sup^2/(2 d_eff abs(N_a) L_loc^2)",
            "current_status": "DERIVED_SUPPORT_BOUND",
            "valid_for_claim": False,
        },
    ]


def first_moment_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "FMI4478_0_support_zero_certificate",
            "quantity": "Z_support",
            "definition": "certificate that no physical marker profile/support exists",
            "formula_or_test": "Z_support=True iff no support carrier, no readout-as-support, no marker worldtube double count and no boundary support residue",
            "needed_inputs": "parent support carrier inventory; readout/support split; worldtube separation; boundary support routing",
            "current_value": "MISSING_SUPPORT_ZERO_CERTIFICATE",
            "units": "boolean_certificate",
            "target": "F_M_absent;mu0_M_zero;mu2_M_zero",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "FMI4478_1_Q_M",
            "quantity": "Q_M",
            "definition": "profile amplitude after canonical normalization F_M=Q_M f_M",
            "formula_or_test": "Q_M=mu0_M for positive normalized profiles; use mu0_abs guard for signed profiles",
            "needed_inputs": "profile normalization; sign branch; parent source path",
            "current_value": "MISSING_MARKER_PROFILE_AMPLITUDE",
            "units": "profile_integral_units",
            "target": "mu0_M;C_a^M",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "FMI4478_2_d_eff",
            "quantity": "d_eff",
            "definition": "effective support dimension in the moment expansion",
            "formula_or_test": "d_eff=3 for local spatial worldtube branch; d_eff=4 for covariant spacetime smearing with clock/Lorentz residual",
            "needed_inputs": "support branch; Hamiltonian split; temporal smearing status",
            "current_value": "MISSING_SUPPORT_DIMENSION_SELECTION",
            "units": "dimensionless",
            "target": "mu2_gradient_coefficient",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "FMI4478_3_ell_rms",
            "quantity": "ell_rms",
            "definition": "root-mean-square marker support radius",
            "formula_or_test": "ell_rms^2=mu2_M/mu0_M for positive profiles; absolute version for signed profiles",
            "needed_inputs": "mu0_M;mu2_M;sign branch",
            "current_value": "MISSING_MARKER_RMS_SUPPORT_RADIUS",
            "units": "m",
            "target": "mu2_M;gradient_leakage",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "FMI4478_4_ell_sup",
            "quantity": "ell_sup",
            "definition": "upper radius of marker support",
            "formula_or_test": "supp(f_M) subset B_h(x_M,ell_sup), giving ell_rms<=ell_sup",
            "needed_inputs": "parent support law or worldtube geometry; non-circular source; uncertainty",
            "current_value": "MISSING_NONCIRCULAR_SUPPORT_RADIUS",
            "units": "m",
            "target": "bounded_projection_envelope",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "FMI4478_5_dipole_or_centering",
            "quantity": "D_M^i",
            "definition": "first moment/dipole if profile is not centred",
            "formula_or_test": "D_M^i=int y^i F_M; centred branch requires D_M^i=0",
            "needed_inputs": "centroid choice; profile symmetry; signed-profile guard",
            "current_value": "MISSING_CENTERING_OR_DIPOLE_VALUE",
            "units": "m_times_profile_units",
            "target": "first_derivative_marker_residual",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "FMI4478_6_quadrupole_TF",
            "quantity": "Q_M_TF^{ij}",
            "definition": "tracefree second-moment anisotropy",
            "formula_or_test": "mu2_M^{ij}=(mu2_M/d_eff)h^{ij}+Q_M_TF^{ij}; isotropy requires Q_M_TF=0",
            "needed_inputs": "profile tensor moment; isotropy proof or bound",
            "current_value": "MISSING_ISOTROPY_OR_QUADRUPOLE_BOUND",
            "units": "m^2_times_profile_units",
            "target": "anisotropic_PPN_clock_orbital_residual",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
    ]


def decision_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4478_0_support_zero_attempt",
            "finding": "profile/support zero reduces to absence of a support carrier plus readout/worldtube/boundary separation",
            "consequence": "the clean branch is precise but not parent-signed yet",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4478_1_first_moment_inputs",
            "finding": "finite support branch now has canonical inputs Q_M, d_eff, ell_rms, ell_sup, dipole and quadrupole anisotropy",
            "consequence": "finite profile scoring can proceed without pretending symmetry or support radius is known",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4478_2_next_target",
            "finding": "the next sharp target is profile symmetry/dimension branch, especially d_eff=3 local support versus covariant time-smearing and quadrupole leakage",
            "consequence": "next work should prove the local spatial branch and isotropy, or bound dipole/quadrupole residuals",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    source_rows: List[Dict[str, object]],
    certificate_rows: List[Dict[str, object]],
    law_rows: List[Dict[str, object]],
    input_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    sources_ok = all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in source_rows)
    support_zero_written = any(row.get("certificate_id") == "SZC4478_5_verdict" for row in certificate_rows)
    support_zero_signed = any(row.get("certificate_id") == "SZC4478_5_verdict" and row.get("parent_signed") is True for row in certificate_rows)
    input_law_written = all(
        any(row.get("law_id") == law_id for row in law_rows)
        for law_id in [
            "MIL4478_0_canonical_normalization",
            "MIL4478_2_support_dimension_branch",
            "MIL4478_4_centering_choice",
            "MIL4478_5_isotropy_or_quadrupole",
            "MIL4478_6_support_radius_bound",
        ]
    )
    inputs_ready = all(
        "MISSING" not in str(row.get("current_value")) and row.get("status") != "BLOCKED_SOURCE_READY"
        for row in input_rows
    )
    no_claims = all(
        str(row.get("valid_for_claim")).lower() == "false"
        for group in [source_rows, certificate_rows, law_rows, input_rows]
        for row in group
    )
    return [
        {
            "gate_id": "CG4478_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": sources_ok,
            "claim_allowed": False,
            "detail": "source register validates 4477 handoff and moment/support rows",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4478_1_support_zero_written",
            "claim": "marker support zero certificate is explicit",
            "gate_pass": support_zero_written,
            "claim_allowed": False,
            "detail": "support carrier, readout, worldtube and boundary separation clauses are written",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4478_2_support_zero_parent_signed",
            "claim": "MTS parent proves no marker support/profile exists",
            "gate_pass": support_zero_signed,
            "claim_allowed": False,
            "detail": "support-carrier absence and separation firewalls remain unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4478_3_first_input_laws_written",
            "claim": "first moment input laws are derived",
            "gate_pass": input_law_written,
            "claim_allowed": False,
            "detail": "canonical normalization, dimension branch, centering, isotropy/quadrupole and support bound are written",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4478_4_first_inputs_ready",
            "claim": "first moment inputs are numeric/source ready",
            "gate_pass": inputs_ready,
            "claim_allowed": False,
            "detail": "input rows still need support zero, Q_M, d_eff, support radius, centering and quadrupole values",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4478_5_no_generated_claim_rows",
            "claim": "no generated row is promoted to public/local-GR evidence",
            "gate_pass": no_claims,
            "claim_allowed": False,
            "detail": "4478 is a support-zero certificate attempt plus first moment input law",
            "valid_for_claim": False,
        },
    ]

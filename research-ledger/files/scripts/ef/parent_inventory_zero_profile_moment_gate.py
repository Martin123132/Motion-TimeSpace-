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


def inventory_zero_proof_rows() -> List[Dict[str, object]]:
    return [
        {
            "proof_id": "PIZ4477_0_quotient_action_factorization",
            "clause": "bulk action factors through the physical quotient before variation",
            "formal_statement": "q:Conf_parent->Q_bulk and S_bulk[Phi]=Sbar_bulk[q(Phi)], with Q_bulk coordinates excluding I_M=<M_cell,R_obs_as_bulk,P_active,J_finite,labelled_species,M_aux>",
            "derivation": "If the action is a pullback from Q_bulk and the marker ideal is not in Q_bulk, every derivative of S_bulk with respect to an I_M generator vanishes by the chain rule.",
            "zero_result": "Pi_{I_M}(S_bulk)=0 and Z_inventory=True",
            "current_status": "EXACT_CONDITIONAL_ZERO_THEOREM",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "PIZ4477_1_external_readout_separation",
            "clause": "readout variables are outside the bulk variational algebra",
            "formal_statement": "R_obs appears only in O_read[Phi;R_obs] or int J O_read with J=0 before local variation",
            "derivation": "This is the 4474 readout lemma recast as inventory grammar. External readout can select recorded coordinates but cannot create a bulk action monomial.",
            "zero_result": "R_obs_as_bulk not in I(S_bulk); no lambda_M from readout",
            "current_status": "CONDITIONAL_READOUT_ZERO_THEOREM",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "PIZ4477_2_no_active_label_or_species",
            "clause": "active-cell labels are quotient labels, not material species",
            "formal_statement": "P_active and labelled species do not occur as fixed backgrounds, source charges, material sectors, or surviving gauge-fixed labels",
            "derivation": "A labelled species vector can obey the same covariance as a quotient label while still carrying physical source data. The zero proof requires quotient-label status before variation.",
            "zero_result": "no active-label marker monomial enters S_bulk",
            "current_status": "SPECIES_AND_LABEL_EXCLUSION_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "PIZ4477_3_no_hidden_marker_auxiliary",
            "clause": "integrated-out variables do not regenerate the marker ideal",
            "formal_statement": "no M_aux with Delta S_aux = 1/2 M_aux L_M M_aux + M_aux B_M[Phi,I_M] whose elimination gives B_M^T L_M^-1 B_M in I_M",
            "derivation": "Even a quotient-looking visible action can hide marker dependence in an eliminated sector. The inventory proof must include the auxiliary completion, not only the written low-energy action.",
            "zero_result": "c_marker_aux=lambda_M_aux=0 only if the auxiliary marker ideal is empty",
            "current_status": "AUXILIARY_COMPLETION_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "PIZ4477_4_boundary_separation",
            "clause": "boundary/reference marker is fixed, topological, no-flux, or Hamiltonian-routed",
            "formal_statement": "Pi_loc(delta S_boundary/delta I_M)=0 under compact local variations",
            "derivation": "The bulk inventory proof cannot erase an interface marker. Boundary silence is a separate condition that must be signed or bounded.",
            "zero_result": "boundary_marker=0 only under a signed boundary routing theorem",
            "current_status": "BOUNDARY_SEPARATION_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "PIZ4477_5_verdict",
            "clause": "inventory zero proof exists as an exact conditional theorem but is not parent-signed",
            "formal_statement": "Z_inventory=True iff PIZ4477_0 through PIZ4477_4 sign together",
            "derivation": "4477 proves what would close the marker ideal. Current MTS still lacks a parent-signed quotient action alphabet, auxiliary completion, and boundary separation certificate.",
            "zero_result": "keep local-GR/R10 blocked; use marker moment fallback if finite branch survives",
            "current_status": "ZERO_THEOREM_PARENT_UNSIGNED_MOMENT_FALLBACK_REQUIRED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def marker_profile_moment_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "MPM4477_0_distribution_expansion",
            "assumption": "finite marker profile F_M has compact local support and O_a varies slowly over that support",
            "derivation": "int d^d y F_M(y) O_a(x+y) = mu0_M O_a(x) + mu1_M^i partial_i O_a(x) + 1/2 mu2_M^{ij} partial_i partial_j O_a(x) + O(mu3/L_loc^3)",
            "result": "mu0_M=int F_M, mu1_M^i=int y^i F_M, mu2_M^{ij}=int y^i y^j F_M",
            "use_in_projection": "turns finite lambda_M profile into local operator and derivative residuals",
            "derived_status": "DERIVED_MOMENT_EXPANSION",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "MPM4477_1_centered_isotropic_profile",
            "assumption": "local profile is centred and isotropic in d_eff dimensions",
            "derivation": "mu1_M^i=0 and mu2_M^{ij}=(mu2_M/d_eff) h^{ij}; hence the first correction is (mu2_M/(2 d_eff)) Delta_h O_a",
            "result": "int F_M O_a = mu0_M O_a + (mu2_M/(2 d_eff)) Delta_h O_a + O(mu4_M/L_loc^4)",
            "use_in_projection": "replaces the ad hoc gradient term in 4476 with a standard coefficient 1/(2 d_eff)",
            "derived_status": "DERIVED_CENTERED_ISOTROPIC_LAW",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "MPM4477_2_effective_marker_length",
            "assumption": "mu0_M is nonzero and the absolute profile moment is finite",
            "derivation": "ell_M^2 = abs(mu2_M/mu0_M), or ell_M,abs^2=mu2_abs/mu0_abs for signed profiles",
            "result": "mu2_M = sigma_M ell_M^2 mu0_M with sign/absolute guard sigma_M declared",
            "use_in_projection": "connects marker support to R10/PPN range without importing measured G",
            "derived_status": "DERIVED_LENGTH_MOMENT_LAW",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "MPM4477_3_compact_support_bound",
            "assumption": "profile support radius is bounded by ell_sup and absolute density is used for signed profiles",
            "derivation": "mu2_abs = int r^2 |F_M| <= ell_sup^2 int |F_M| = ell_sup^2 mu0_abs",
            "result": "abs(gradient leakage) <= abs(lambda_M)*abs(zeta_grad_a)*mu0_abs*ell_sup^2/(2 d_eff N_a L_loc^2)",
            "use_in_projection": "gives a clean upper bound even when profile sign is not trusted",
            "derived_status": "DERIVED_COMPACT_SUPPORT_BOUND",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "MPM4477_4_external_readout_zero_moments",
            "assumption": "inventory zero branch signs and F_M is not a bulk profile",
            "derivation": "if Pi_{I_M}(S_bulk)=0, there is no F_M in the physical action; the moment functional is absent rather than small",
            "result": "lambda_M mu0_M = lambda_M mu2_M = 0 on the signed inventory branch",
            "use_in_projection": "prevents treating unknown moments as evidence against the zero branch",
            "derived_status": "CONDITIONAL_ZERO_MOMENT_THEOREM",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "MPM4477_5_projection_vector_update",
            "assumption": "finite marker branch survives and moments/projectors/normalizations are declared",
            "derivation": "C_a^M=lambda_M*(zeta_a mu0_M + zeta_grad_a mu2_M/(2 d_eff L_loc^2)+O(mu4/L_loc^4))/N_a",
            "result": "Pi_local(lambda_M)=(c_R2_marker,C_marker,T_marker_projection,q_marker,boundary_marker) with componentwise absolute envelope",
            "use_in_projection": "upgrades 4476 projection map into a moment-expanded local residual vector",
            "derived_status": "DERIVED_MOMENT_PROJECTION_VECTOR",
            "valid_for_claim": False,
        },
    ]


def moment_intake_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "MIR4477_0_Z_inventory",
            "quantity": "Z_inventory",
            "definition": "signed parent inventory zero certificate",
            "formula_or_test": "Z_inventory=True iff q-action factorization, readout separation, no label/species, no auxiliary marker and boundary separation sign together",
            "needed_inputs": "parent action alphabet; quotient map; auxiliary completion; boundary routing certificate",
            "current_value": "MISSING_PARENT_INVENTORY_ZERO_CERTIFICATE",
            "units": "boolean_certificate",
            "target": "lambda_M_zero_branch",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MIR4477_1_d_eff",
            "quantity": "d_eff",
            "definition": "effective dimension of the local marker support used in the moment expansion",
            "formula_or_test": "d_eff=3 for spatial local-body support; d_eff=4 for covariant spacetime support; declare branch",
            "needed_inputs": "support convention; foliation/worldtube choice; covariance guard",
            "current_value": "MISSING_SUPPORT_DIMENSION_BRANCH",
            "units": "dimensionless",
            "target": "mu2_gradient_coefficient",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MIR4477_2_mu0_M",
            "quantity": "mu0_M",
            "definition": "zeroth marker profile moment",
            "formula_or_test": "mu0_M=int d^d y F_M(y), or zero if inventory branch signs",
            "needed_inputs": "F_M profile; support; normalization; sign convention",
            "current_value": "MISSING_MARKER_PROFILE_ZEROTH_MOMENT",
            "units": "profile_integral_units",
            "target": "all_marker_projection_channels",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MIR4477_3_mu2_M",
            "quantity": "mu2_M",
            "definition": "second marker profile moment",
            "formula_or_test": "mu2_M=int d^d y r^2 F_M(y); centred isotropic correction is mu2_M/(2 d_eff)",
            "needed_inputs": "profile; support radius; centred/isotropic status; signed or absolute moment",
            "current_value": "MISSING_MARKER_PROFILE_SECOND_MOMENT",
            "units": "m^2_times_profile_units",
            "target": "gradient_leakage;c_R2_marker;boundary_marker",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MIR4477_4_ell_sup",
            "quantity": "ell_sup",
            "definition": "upper support radius for compact-support moment bound",
            "formula_or_test": "mu2_abs <= ell_sup^2 mu0_abs",
            "needed_inputs": "parent geometry/support law; not fitted R10 range or measured G",
            "current_value": "MISSING_NONCIRCULAR_MARKER_SUPPORT_RADIUS",
            "units": "m",
            "target": "bounded_projection_envelope",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MIR4477_5_profile_symmetry",
            "quantity": "profile_symmetry",
            "definition": "whether first moment vanishes and second moment is isotropic",
            "formula_or_test": "centred=True gives mu1=0; isotropic=True gives mu2^{ij}=mu2 h^{ij}/d_eff",
            "needed_inputs": "profile centre; symmetry proof; body/worldtube convention",
            "current_value": "MISSING_PROFILE_CENTERING_AND_ISOTROPY_CERTIFICATE",
            "units": "boolean_pair",
            "target": "moment_expansion_validity",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MIR4477_6_component_values",
            "quantity": "Pi_local(lambda_M)_moment",
            "definition": "moment-expanded finite marker residual vector",
            "formula_or_test": "C_a^M=lambda_M*(zeta_a mu0_M + zeta_grad_a mu2_M/(2 d_eff L_loc^2))/N_a",
            "needed_inputs": "lambda_M; mu0_M; mu2_M; d_eff; zeta_a; zeta_grad_a; L_loc; N_a",
            "current_value": "MISSING_MOMENT_PROJECTION_VALUES",
            "units": "mixed_declared_components",
            "target": "R10;WEP;PPN;clock;orbital",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
    ]


def decision_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4477_0_zero_theorem_attempt",
            "finding": "Z_inventory has an exact quotient-action zero proof if the parent action alphabet excludes the marker ideal before variation",
            "consequence": "the proof route is real but remains unsigned by the current parent corpus",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4477_1_moment_law_derived",
            "finding": "finite marker profiles now have a Taylor/moment expansion with the gradient coefficient mu2_M/(2 d_eff)",
            "consequence": "mu0_M and mu2_M are no longer vague placeholders; they are profile moments with support bounds",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4477_2_next_target",
            "finding": "the sharpest next target is the support/profile law: either prove no bulk profile exists, or derive ell_sup/profile symmetry from parent geometry",
            "consequence": "next work should attempt a non-circular support-radius/profile-zero certificate before any numeric scoring",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    source_rows: List[Dict[str, object]],
    proof_rows: List[Dict[str, object]],
    moment_rows: List[Dict[str, object]],
    intake_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    sources_ok = all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in source_rows)
    zero_theorem_written = any(row.get("proof_id") == "PIZ4477_5_verdict" for row in proof_rows)
    zero_theorem_signed = any(row.get("proof_id") == "PIZ4477_5_verdict" and row.get("parent_signed") is True for row in proof_rows)
    moment_law_written = all(
        any(row.get("derivation_id") == derivation_id for row in moment_rows)
        for derivation_id in [
            "MPM4477_0_distribution_expansion",
            "MPM4477_1_centered_isotropic_profile",
            "MPM4477_3_compact_support_bound",
            "MPM4477_5_projection_vector_update",
        ]
    )
    intake_ready = all(
        "MISSING" not in str(row.get("current_value")) and row.get("status") != "BLOCKED_SOURCE_READY"
        for row in intake_rows
    )
    no_claims = all(
        str(row.get("valid_for_claim")).lower() == "false"
        for group in [source_rows, proof_rows, moment_rows, intake_rows]
        for row in group
    )
    return [
        {
            "gate_id": "CG4477_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": sources_ok,
            "claim_allowed": False,
            "detail": "source register validates 4476 handoff and moment/projection rows",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4477_1_zero_theorem_written",
            "claim": "parent inventory zero theorem is explicit",
            "gate_pass": zero_theorem_written,
            "claim_allowed": False,
            "detail": "quotient action factorization plus escape-route firewalls are written",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4477_2_zero_theorem_parent_signed",
            "claim": "MTS parent signs Z_inventory=True",
            "gate_pass": zero_theorem_signed,
            "claim_allowed": False,
            "detail": "parent action alphabet, auxiliary completion and boundary separation remain unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4477_3_moment_law_written",
            "claim": "finite marker profile moment law is derived",
            "gate_pass": moment_law_written,
            "claim_allowed": False,
            "detail": "Taylor expansion, centred/isotropic law, compact support bound and projection-vector update are written",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4477_4_moment_values_ready",
            "claim": "moment inputs are numeric/source ready",
            "gate_pass": intake_ready,
            "claim_allowed": False,
            "detail": "moment intake rows still need support dimension, profile moments, support radius and symmetry certificate",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4477_5_no_generated_claim_rows",
            "claim": "no generated row is promoted to public/local-GR evidence",
            "gate_pass": no_claims,
            "claim_allowed": False,
            "detail": "4477 is a zero-theorem attempt plus finite-profile moment derivation",
            "valid_for_claim": False,
        },
    ]

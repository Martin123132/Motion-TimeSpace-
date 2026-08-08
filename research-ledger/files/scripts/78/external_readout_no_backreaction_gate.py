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


def external_readout_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "ERN4474_0_action_split",
            "clause": "external readout is not a parent bulk field",
            "formal_statement": "S_total[Phi;R_obs,J]=S_bulk[Phi]+S_boundary[Phi]+S_J[Phi;R_obs,J], with either S_J absent from the variational problem or J set to zero before local equations are taken",
            "derivation": "For compact-support local variations, delta S_total|J=0 = delta S_bulk + delta S_boundary; no Euler-Lagrange term proportional to R_obs is present.",
            "zero_result": "R_obs contributes no local equation of motion when it appears only as a post-solution readout or source-at-zero insertion.",
            "current_status": "CONDITIONAL_THEOREM_DERIVED_PARENT_ROLE_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ERN4474_1_bulk_Robs_variation",
            "clause": "no bulk action dependence on R_obs",
            "formal_statement": "partial S_bulk/partial R_obs = 0 and delta S_bulk/delta R_obs = 0",
            "derivation": "If R_obs is absent from S_bulk as a field, background, spurion, label or material marker, functional differentiation of S_bulk has no R_obs slot.",
            "zero_result": "no marker equation, no hidden local source, and no primitive grain normalization from R_obs",
            "current_status": "DERIVED_IF_ABSENCE_CLAUSE_SIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ERN4474_2_hilbert_stress_zero",
            "clause": "external readout has no Hilbert stress tensor",
            "formal_statement": "T_R^{mu nu}=(-2/sqrt(-g)) delta S_bulk/delta g_{mu nu}|R_obs = 0",
            "derivation": "Metric variation only sees action terms. A readout functional O_read[Phi;R_obs] evaluated after solving can change recorded coordinates, not the stress-energy sourcing the metric.",
            "zero_result": "no Newton source, no PPN stress leakage, no EM/Poynting stress double count from R_obs",
            "current_status": "CONDITIONAL_STRESS_ZERO_THEOREM",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ERN4474_3_coframe_connection_scalar_zero",
            "clause": "external readout has no coframe, connection, or scalar source",
            "formal_statement": "delta S_bulk/delta e^A_mu|R_obs = 0, delta S_bulk/delta omega^{AB}_mu|R_obs = 0, delta S_bulk/delta chi|R_obs = 0",
            "derivation": "If R_obs is not a coframe, connection, scalar, matter-frame multiplier, or source charge in the action, every local variational derivative with respect to those fields is unchanged.",
            "zero_result": "no torsion/current channel, no scalar fifth-force source, no source-measure leak",
            "current_status": "CONDITIONAL_VARIATIONAL_SOURCE_ZERO_THEOREM",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ERN4474_4_source_at_zero_lemma",
            "clause": "source-at-zero readout is harmless only at zero source",
            "formal_statement": "S_J=int J O_read[Phi;R_obs]; local equations use delta S_total/delta Phi|J=0 = delta S_bulk/delta Phi",
            "derivation": "The source can generate readout derivatives after the solution, but if J is zero in the physical equations, the term J delta O_read/delta Phi drops out exactly.",
            "zero_result": "source-at-zero is a valid bookkeeping readout, not a physical marker, only if J is never kept finite in the local equations",
            "current_status": "DERIVED_WITH_FINITE_SOURCE_FIREWALL",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ERN4474_5_curvature_vertex_zero",
            "clause": "external readout has no curvature-linear vertex",
            "formal_statement": "delta^2 S_bulk/(delta R_obs delta Riemann)=0 and delta^2 S_bulk/(delta R_obs delta R)=0",
            "derivation": "A post-solution readout cannot generate a curvature-square coefficient. Such a coefficient appears only if the marker is in S_bulk, S_boundary, or an integrated-out physical sector.",
            "zero_result": "c_R2_marker=0 on the external-readout branch",
            "current_status": "CONDITIONAL_CR2_ZERO_THEOREM",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ERN4474_6_boundary_firewall",
            "clause": "boundary/reference readout is safe only if fixed, topological, no-flux, or Hamiltonian-routed",
            "formal_statement": "delta S_boundary|R_obs = 0 for local compact support, or boundary charge is routed outside local PPN/R10 response",
            "derivation": "Local bulk silence does not automatically silence boundary data. A moving or material boundary marker can feed a finite local residual through matching or source normalization.",
            "zero_result": "boundary_marker=0 only under a signed no-flux/fixed-charge theorem",
            "current_status": "BOUNDARY_EXCEPTION_RETAINED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ERN4474_7_verdict",
            "clause": "the no-backreaction proof is exact but conditional",
            "formal_statement": "If R_obs appears only in O_read or a J=0 source insertion, all local variational source components vanish; otherwise the marker coupling branch must be filled.",
            "derivation": "This proves the clean external-readout route, but it does not prove that the current MTS parent uses only that route.",
            "zero_result": "local-GR credit remains blocked until parent field inventory and source-at-zero/readout role are signed",
            "current_status": "EXACT_CONDITIONAL_THEOREM_PARENT_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def variational_source_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "VSA4474_0_bulk_absence",
            "variation_slot": "R_obs in S_bulk",
            "zero_condition": "R_obs not a bulk field, spurion, material marker, active label, or background datum",
            "derived_result": "delta S_bulk/delta R_obs = 0",
            "fallback_if_failed": "declare M_cell and fill lambda_M/bulk support rows",
            "current_status": "PARENT_INVENTORY_UNSIGNED",
            "arena_map": "local_GR;R10;PPN;clock;orbital",
            "valid_for_claim": False,
        },
        {
            "audit_id": "VSA4474_1_metric_stress",
            "variation_slot": "metric/Hilbert source",
            "zero_condition": "no R_obs-dependent term in sqrt(-g)L_bulk or source measure",
            "derived_result": "T_R^{mu nu}=0",
            "fallback_if_failed": "fill T_marker^{mu nu} and Newton/PPN source projection",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "arena_map": "Newton_source;PPN;orbital",
            "valid_for_claim": False,
        },
        {
            "audit_id": "VSA4474_2_coframe_connection",
            "variation_slot": "coframe/connection current",
            "zero_condition": "R_obs not in e^A_mu, omega^{AB}_mu, torsion/current sector, or matching map",
            "derived_result": "tau_R=0 and J_omega,R=0",
            "fallback_if_failed": "fill torsion/current marker residual",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "arena_map": "PPN;clock;spin_orbital",
            "valid_for_claim": False,
        },
        {
            "audit_id": "VSA4474_3_scalar_source",
            "variation_slot": "chi/Gamma/source-measure scalar",
            "zero_condition": "R_obs not in A(chi), Z_H, Gamma_eff, kappa_eff or source-label normalization",
            "derived_result": "J_chi,R=0 and C_marker=0",
            "fallback_if_failed": "fill C_marker and R10/common-mode scalar projection",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "arena_map": "R10;WEP;PPN;clock",
            "valid_for_claim": False,
        },
        {
            "audit_id": "VSA4474_4_curvature_vertex",
            "variation_slot": "curvature-linear/quadratic coefficient",
            "zero_condition": "no R_obs coupling to R, Ricci^2, Weyl^2, Riemann^2 or integrated-out marker mass matrix",
            "derived_result": "c_R2_marker=0",
            "fallback_if_failed": "fill c_R2_marker components and alpha(lambda) projection",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "arena_map": "R10_alpha_lambda;PPN_gamma_beta",
            "valid_for_claim": False,
        },
        {
            "audit_id": "VSA4474_5_boundary_flux",
            "variation_slot": "boundary/interface/reference readout",
            "zero_condition": "fixed/topological/no-flux/Hamiltonian-routed boundary reference under compact local variations",
            "derived_result": "boundary_marker=0 in local response",
            "fallback_if_failed": "fill boundary_marker and transition-current projection",
            "current_status": "BOUNDARY_SILENCE_UNSIGNED",
            "arena_map": "local_GR;clock;orbital;R10",
            "valid_for_claim": False,
        },
        {
            "audit_id": "VSA4474_6_source_at_zero",
            "variation_slot": "external source J",
            "zero_condition": "J is a diagnostic source set to zero before physical equations and never used as a fitted material field",
            "derived_result": "J delta O_read/delta Phi vanishes exactly at J=0",
            "fallback_if_failed": "finite J is a source extension and must be bounded",
            "current_status": "DERIVED_FIREWALL_PARENT_USAGE_UNSIGNED",
            "arena_map": "all_local_arenas",
            "valid_for_claim": False,
        },
    ]


def marker_coupling_fill_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "MCF4474_0_M_cell_role",
            "quantity": "M_cell",
            "definition": "marker/readout variable if R_obs is not purely external",
            "formula_or_test": "M_cell in Phi_parent or S_boundary, or finite J retained in equations",
            "needed_inputs": "parent field inventory; readout/action split; support classification",
            "current_value": "MISSING_PARENT_FIELD_INVENTORY_AND_READOUT_SPLIT",
            "units": "field_role_certificate",
            "arena_map": "all_local_arenas",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MCF4474_1_lambda_M",
            "quantity": "lambda_M",
            "definition": "marker bulk coupling to curvature/source/grain operator",
            "formula_or_test": "Delta S_M = int sqrt(-g) lambda_M F_M(M_cell) O_marker",
            "needed_inputs": "O_marker; normalization; sign; parent source path; no-cancellation guard",
            "current_value": "MISSING_MARKER_BULK_COUPLING",
            "units": "operator_dimension_dependent",
            "arena_map": "c_R2_eff;C_total;R10;PPN",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MCF4474_2_ell_marker",
            "quantity": "ell_marker",
            "definition": "physical marker range/grain scale if marker survives",
            "formula_or_test": "ell_marker must come from parent geometry or source support, not measured G or fitted R10 range",
            "needed_inputs": "non-circular scale law; units; uncertainty; support",
            "current_value": "MISSING_NONCIRCULAR_MARKER_LENGTH",
            "units": "m",
            "arena_map": "R10_lambda;PPN_range;orbital",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MCF4474_3_zeta_M",
            "quantity": "zeta_M",
            "definition": "projection from marker operator to canonical curvature-square basis",
            "formula_or_test": "O_marker -> zeta_M R^2/Ricci^2/Weyl^2 channel after local expansion",
            "needed_inputs": "basis map; expansion convention; channel sign",
            "current_value": "MISSING_MARKER_BASIS_PROJECTION",
            "units": "dimensionless_or_declared",
            "arena_map": "R10_alpha_lambda;PPN",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MCF4474_4_marker_auxiliary_elimination",
            "quantity": "B_M,L_M,c_marker_bare",
            "definition": "hidden auxiliary/bare marker contribution to curvature-square coefficient",
            "formula_or_test": "c_marker_aux = c_marker_bare + 0.5*B_M^T*L_M^-1*B_M",
            "needed_inputs": "auxiliary mass matrix; source vector; bare term; positive/negative signature",
            "current_value": "MISSING_MARKER_AUXILIARY_COMPONENTS",
            "units": "length_squared_after_EH_normalization",
            "arena_map": "R10;PPN",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MCF4474_5_c_R2_marker",
            "quantity": "c_R2_marker",
            "definition": "total marker-induced curvature-square coefficient",
            "formula_or_test": "c_R2_marker = zeta_M*lambda_M*ell_marker^2/N_EH + c_marker_bare + 0.5*B_M^T*L_M^-1*B_M",
            "needed_inputs": "lambda_M; ell_marker; zeta_M; N_EH; B_M; L_M; c_marker_bare",
            "current_value": "MISSING_MARKER_CR2_COMPONENTS",
            "units": "m^2_after_normalization",
            "arena_map": "R10_alpha_lambda;PPN_gamma_beta",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MCF4474_6_C_marker",
            "quantity": "C_marker",
            "definition": "marker contribution to common-mode scalar/source coupling",
            "formula_or_test": "C_total = C_explicit_Achi + C_metric_pole + C_hidden_source + C_marker",
            "needed_inputs": "matter-frame/source charge normalization; material dependence; screening branch",
            "current_value": "MISSING_MARKER_SOURCE_COUPLING",
            "units": "dimensionless",
            "arena_map": "R10;WEP;PPN;clock;orbital",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MCF4474_7_T_marker_J_marker",
            "quantity": "T_marker_or_J_marker",
            "definition": "stress/source current generated by marker variation",
            "formula_or_test": "T_marker^{mu nu}=(-2/sqrt(-g)) delta S_marker/delta g_{mu nu}; J_marker=delta S_marker/delta M_cell",
            "needed_inputs": "S_marker; variation convention; support; boundary routing; source path",
            "current_value": "MISSING_MARKER_VARIATIONAL_SOURCE",
            "units": "stress_or_current_units",
            "arena_map": "Newton_source;EM_stress;PPN;clock",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MCF4474_8_boundary_marker",
            "quantity": "boundary_marker",
            "definition": "local residue from marker/reference boundary variation or matching",
            "formula_or_test": "boundary_marker = Pi_loc(delta S_boundary/delta R_obs) unless fixed/topological/no-flux/Hamiltonian-routed",
            "needed_inputs": "boundary condition; charge routing; support-separation proof; units",
            "current_value": "MISSING_BOUNDARY_MARKER_SILENCE_OR_VALUE",
            "units": "declared_by_projection",
            "arena_map": "local_GR;R10;clock;orbital",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
        {
            "row_id": "MCF4474_9_no_cancellation_guard",
            "quantity": "R_marker_abs",
            "definition": "absolute marker residual envelope, forbidding hidden sign cancellation",
            "formula_or_test": "R_marker_abs = abs(c_R2_marker)+abs(C_marker)+abs(T_marker_projection)+abs(boundary_marker)",
            "needed_inputs": "all marker components individually zero or source-bounded",
            "current_value": "MISSING_MARKER_COMPONENT_VALUES",
            "units": "mixed_component_envelope",
            "arena_map": "claim_gate_guard",
            "status": "BLOCKED_SOURCE_READY",
            "valid_for_claim": False,
        },
    ]


def decision_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4474_0_exact_conditional_proof",
            "finding": "external readout/source-at-zero has been proved no-backreacting under an explicit action split",
            "consequence": "this is a real local theorem, but only for readout variables outside the physical variational problem",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4474_1_parent_usage_unsigned",
            "finding": "current MTS has not yet signed that its relational marker is only O_read or J=0 source dressing",
            "consequence": "local-GR and R10 claims remain blocked until the parent field inventory/readout split is signed",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4474_2_finite_branch_prepared",
            "finding": "if readout is material, the first finite component is lambda_M, followed by ell_marker, zeta_M, c_R2_marker, C_marker and T_marker/J_marker",
            "consequence": "next work should attack lambda_M: prove it is zero by parent grammar or source it as a finite coupling",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    source_rows: List[Dict[str, object]],
    theorem_rows: List[Dict[str, object]],
    audit_rows: List[Dict[str, object]],
    coupling_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    sources_ok = all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in source_rows)
    theorem_written = any(row.get("theorem_id") == "ERN4474_7_verdict" for row in theorem_rows)
    conditional_zero_derived = all(
        any(row.get("theorem_id") == theorem_id for row in theorem_rows)
        for theorem_id in ["ERN4474_1_bulk_Robs_variation", "ERN4474_2_hilbert_stress_zero", "ERN4474_3_coframe_connection_scalar_zero", "ERN4474_4_source_at_zero_lemma", "ERN4474_5_curvature_vertex_zero"]
    )
    parent_signed = any(row.get("theorem_id") == "ERN4474_7_verdict" and row.get("parent_signed") is True for row in theorem_rows)
    marker_rows_ready = all(
        "MISSING" not in str(row.get("current_value")) and row.get("status") != "BLOCKED_SOURCE_READY"
        for row in coupling_rows
    )
    audit_blocks = any("UNSIGNED" in str(row.get("current_status")) for row in audit_rows)
    no_claims = all(
        str(row.get("valid_for_claim")).lower() == "false"
        for group in [source_rows, theorem_rows, audit_rows, coupling_rows]
        for row in group
    )
    return [
        {
            "gate_id": "CG4474_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": sources_ok,
            "claim_allowed": False,
            "detail": "source register validates 4473, 340/341 source-at-zero/readout forks, and 4474 scripts",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4474_1_conditional_theorem_written",
            "claim": "external-readout no-backreaction theorem is explicit",
            "gate_pass": theorem_written and conditional_zero_derived,
            "claim_allowed": False,
            "detail": "bulk, Hilbert, coframe/connection/scalar, source-at-zero and curvature-vertex zeros are derived conditionally",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4474_2_parent_readout_role_signed",
            "claim": "MTS parent proves R_obs is only external readout/source-at-zero",
            "gate_pass": parent_signed,
            "claim_allowed": False,
            "detail": "parent field-inventory and readout/action split remain unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4474_3_variational_audit_blocks_claim",
            "claim": "no local variational source slots remain open",
            "gate_pass": not audit_blocks,
            "claim_allowed": False,
            "detail": "audit deliberately keeps parent-unsigned and boundary-silence clauses live",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4474_4_marker_couplings_claim_ready",
            "claim": "finite marker branch is numerically/source ready",
            "gate_pass": marker_rows_ready,
            "claim_allowed": False,
            "detail": "marker coupling rows are named but still contain missing source values",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4474_5_no_generated_claim_rows",
            "claim": "no generated row is promoted to public/local-GR evidence",
            "gate_pass": no_claims,
            "claim_allowed": False,
            "detail": "4474 is a derived conditional theorem plus nonclaim coupling intake",
            "valid_for_claim": False,
        },
    ]

from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Dict, Iterable, List


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def refinement_factor(order: int, subdivisions: int) -> float:
    if order < 1:
        raise ValueError("order must be >= 1")
    if subdivisions < 1:
        raise ValueError("subdivisions must be >= 1")
    return subdivisions ** (1 - order)


def phi_refinement_scan_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for order in [1, 2, 3, 4]:
        rows.append(
            {
                "term_id": f"PHI4459_{order}",
                "phi_term": f"a_{order} delta^{order}",
                "refined_sum_for_n_subcells": f"a_{order} delta^{order} n^(1-{order})",
                "factor_n2": refinement_factor(order, 2),
                "factor_n10": refinement_factor(order, 10),
                "refinement_invariant": order == 1,
                "zero_if_parent_refinement_signed": order > 1,
                "continuum_interpretation": "curvature_first_moment_EH_channel"
                if order == 1
                else "separate_higher_response_or_density_squared_channel",
                "valid_for_claim": False,
            }
        )
    return rows


def theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "RFL4459_0_target",
            "claim_piece": "primitive deficit refinement linearity",
            "statement": "If a primitive local action depends only on the oriented total deficit delta of a physical hinge/cell and arbitrary subdivision of that same physical flux is action-equivalent, then the response Phi(delta) is linear near delta=0.",
            "derivation": "For n equal subcells, S_n(delta)=n Phi(delta/n). If S_n(delta)=S_1(delta) for all n and Phi is smooth, then each Taylor coefficient a_m with m>=2 obeys a_m n^(1-m)=a_m for all n, hence a_m=0.",
            "result": "Phi''(0)=0 and all higher same-channel derivatives vanish under the refinement premise.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RFL4459_1_c2_rejection",
            "claim_piece": "visible c2 under refinement",
            "statement": "A visible deficit-squared cost A_h c2 delta_h^2 is not invariant under splitting the same total deficit into sub-deficits.",
            "derivation": "n c2 (delta/n)^2 = c2 delta^2/n, so the action changes by a factor 1/n unless c2=0 or subdivision is not an equivalence.",
            "result": "c2_visible is killed only by parent-signed refinement equivalence; otherwise it is a real coefficient owner.",
            "status": "C2_PRESSURE_DERIVED_NOT_ZEROED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RFL4459_2_EH_bridge",
            "claim_piece": "linear first moment bridge",
            "statement": "The surviving refinement-invariant first moment A_h k1 delta_h has the Regge/EH bridge shape.",
            "derivation": "The 1823 scaling row gives A_h delta_h ~ R ell^4 and the sum over cells gives integral sqrt(-g) R up to normalization and boundary/continuum assumptions.",
            "result": "This is the clean local-GR route if MTS derives the refinement/first-moment premise.",
            "status": "BRIDGE_SHARPENED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RFL4459_3_counterroute",
            "claim_piece": "R2 density counterroute",
            "statement": "A continuum R^2 density is not the same object as a first-moment deficit measure and remains legal unless the parent action forbids second response channels.",
            "derivation": "The refinement theorem kills nonlinear functions of the same integrated deficit measure, but a parent can still introduce a density-squared invariant, hidden scalar, marker prefactor, or renormalized tower.",
            "result": "No c_R2/c_Ric/c_W zero claim follows without no-second-channel and no-hidden-tower signatures.",
            "status": "COUNTERROUTE_RETAINED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "RFL4459_4_verdict",
            "claim_piece": "4459 theorem status",
            "statement": "4459 proves the exact mathematical law needed to kill Phi''(0) by refinement invariance, but current sources do not yet prove that MTS parent cells obey this law.",
            "derivation": "The theorem is stronger than preference for linearity and weaker than a parent-owned local-GR reduction.",
            "result": "Next target is parent refinement-gauge signature or a finite c2/c_Ric/c_W coefficient owner row.",
            "status": "THEOREM_CONDITIONAL_PARENT_SIGNATURE_MISSING",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def selector_signature_rows() -> List[Dict[str, object]]:
    return [
        {
            "signature_id": "SIG4459_0_oriented_flux",
            "required_parent_signature": "primitive gravitational response uses oriented curvature/holonomy flux delta as a first-moment measure",
            "why_needed": "distinguishes EH-like signed holonomy cost from strain-energy/variance/squared-mismatch cost",
            "current_status": "MOTIVATED_NOT_PARENT_SIGNED",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "signature_id": "SIG4459_1_refinement_equivalence",
            "required_parent_signature": "subdivision of one physical hinge/cell into n subcells with the same total deficit is gauge/refinement-equivalent",
            "why_needed": "activates S_n(delta)=n Phi(delta/n)=Phi(delta) and forces Phi linear",
            "current_status": "NOT_PARENT_SIGNED",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "signature_id": "SIG4459_2_no_second_channel",
            "required_parent_signature": "no independent curvature-density-squared, hidden scalar, marker-prefactor, or memory tower channel regenerates c_R2/c_Ric/c_W",
            "why_needed": "prevents the R2 density counterroute after the first-moment theorem",
            "current_status": "OPEN_COUNTERROUTES_FROM_964_1823_4458",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "signature_id": "SIG4459_3_boundary_measure",
            "required_parent_signature": "boundary and Gauss-Bonnet/topological terms are fixed/exact/silent on the same local collar",
            "why_needed": "prevents topological or boundary residues masquerading as bulk zero",
            "current_status": "GUARD_ACTIVE_NOT_CLOSED",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "signature_id": "SIG4459_4_readout_source_lock",
            "required_parent_signature": "same observed metric/coframe and Hilbert source are used for rods, clocks, EM, orbits, and pole diagonalization",
            "why_needed": "keeps zero theorem tied to the actual local tests rather than an unobserved representative",
            "current_status": "CONDITIONAL_FROM_PRIOR_PACKET_NOT_PARENT_SIGNED_HERE",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
    ]


def coefficient_owner_template_rows() -> List[Dict[str, object]]:
    return [
        {
            "owner_id": "OWN4459_0_refinement_zero_owner",
            "quantity": "Phi_double_prime_0; c_R2;c_Ric;c_W",
            "candidate_owner": "parent refinement-gauge first-moment theorem",
            "formula_or_value": "0 only if SIG4459_0..SIG4459_4 close in one branch",
            "required_inputs": "oriented flux measure; refinement equivalence; no second channel; boundary silence; readout/source lock",
            "current_status": "ZERO_OWNER_CONDITIONAL_UNSIGNED",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "owner_id": "OWN4459_1_visible_c2",
            "quantity": "c2_visible = 1/2 Phi''(0)",
            "candidate_owner": "primitive deficit response function Phi(delta)",
            "formula_or_value": "MISSING_PARENT_PHI_DOUBLE_PRIME_0",
            "required_inputs": "Phi(delta) from parent action; sign; normalization; source path; cell scale; shape factor",
            "current_status": "MISSING_PARENT_INPUT",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "owner_id": "OWN4459_2_basis_coefficients",
            "quantity": "c_R2,c_Ric,c_W,c_Riem",
            "candidate_owner": "4458 MTS basis coefficient row",
            "formula_or_value": "MISSING_PARENT_BASIS_COEFFICIENTS",
            "required_inputs": "numeric/symbolic coefficients in the 4458 basis; units m^2; source path; zero/topological flags",
            "current_status": "MISSING_PARENT_INPUT",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "owner_id": "OWN4459_3_hidden_tower",
            "quantity": "c_R2_eff hidden or renormalized",
            "candidate_owner": "integrated-out scalar/auxiliary/marker/memory tower",
            "formula_or_value": "MISSING_BETA_MASS_MARKER_KERNEL",
            "required_inputs": "beta; M; kernel; source coupling; readout metric; screening; source path",
            "current_status": "COUNTERROUTE_LIVE_UNSOURCED",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(parent_signature_signed: bool = False) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4459_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "source validation is performed by the generator.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4459_1_refinement_theorem",
            "claim": "refinement invariance forces Phi''(0)=0",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "exact conditional theorem written; parent premise still unsigned.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4459_2_parent_signature",
            "claim": "MTS parent signs oriented refinement-equivalent first-moment action",
            "gate_pass": parent_signature_signed,
            "claim_allowed": False,
            "detail": "no current source signs the refinement-gauge premise.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4459_3_no_second_channel",
            "claim": "no R2/Ricci2/Weyl2 hidden or density-squared channel remains",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "964/1823/4458 counterroutes remain live.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4459_4_coefficient_owner",
            "claim": "first finite coefficient owner value is source-backed",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "visible c2 and 4458 basis coefficients remain missing.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4459_5_local_GR",
            "claim": "local GR/Newton reduction follows from this branch",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "operator zero selector is improved but not parent-signed; broader local bridge gates remain open.",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4459_6_next_target",
            "claim": "next hinge is selected",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "4460-Y5-R2FR-parent-refinement-gauge-signature-or-visible-c2-finite-row.md",
            "valid_for_claim": False,
        },
    ]


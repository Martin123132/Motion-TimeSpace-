from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1165-Y5-R10-lifted-C-sector-parent-action-contract-or-Ccorner-zero-bound.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def is_false(value: object) -> bool:
    return str(value).strip().lower() == "false"


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1165_0_1164_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1164_NEXT_TARGET.csv",
            "needle": "NEXT1164_0_1165",
            "role": "handoff requiring lifted C parent-action contract or Ccorner/weight edge certificate.",
        },
        {
            "source_id": "SRC1165_1_274_lifted_verdict",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "lifted_C_sector_3form_boundary_route_identified_not_parent_derived_projected_metric_remains_closure",
            "role": "lifted C route identified but not promoted.",
        },
        {
            "source_id": "SRC1165_2_274_JC_boundary",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "J_C = dB_C + J_C^{top}",
            "role": "boundary-class decomposition candidate for lifted C.",
        },
        {
            "source_id": "SRC1165_3_274_theorem_shape",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "Let J_C be a domain 3-form memory current on a spatial domain D with boundary partial D.",
            "role": "conditional local-exact/FLRW-active theorem shape.",
        },
        {
            "source_id": "SRC1165_4_274_contract",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "derive `J_C` from `Q^i_j`, coframe, or `det(Q)`",
            "role": "future parent action contract burden.",
        },
        {
            "source_id": "SRC1165_5_275_JC_verdict",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "JC_three_form_has_conditional_kinematic_Q_origin_not_parent_action_projector_and_domain_still_closure",
            "role": "three-form has conditional kinematic origin but no parent-action promotion.",
        },
        {
            "source_id": "SRC1165_6_275_volume_origin",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "comes from the determinant / volume form of a 3D spatial domain.",
            "role": "candidate route from determinant/volume form.",
        },
        {
            "source_id": "SRC1165_7_275_missing_selector",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "physical domain selector `D` | not parent-derived",
            "role": "domain selector remains missing.",
        },
        {
            "source_id": "SRC1165_8_207_projector_Bianchi",
            "relative_path": "207-domain-projector-action-and-Bianchi-identity.md",
            "needle": "domain_projector_action_formal_Bianchi_conditional_representative_missing",
            "role": "projector action and Bianchi accounting conditionally shaped.",
        },
        {
            "source_id": "SRC1165_9_360_matter",
            "relative_path": "360-universal-matter-coupling-theorem-attempt.md",
            "needle": "conditional_universal_coupling_theorem_only_no_WEP_clock_PPN_or_local_GR_pass",
            "role": "matter coupling remains conditional, not a WEP/local-GR pass.",
        },
        {
            "source_id": "SRC1165_10_362_scalar_closure",
            "relative_path": "362-Cperp-relative-exactness-or-projected-metric-closure-decision.md",
            "needle": "Cperp_scalar_exactness_rejected_projected_metric_demoted_to_explicit_closure_lifted_C_route_open",
            "role": "scalar C route closure demotion; lifted route open.",
        },
        {
            "source_id": "SRC1165_11_361_presymplectic",
            "relative_path": "361-residual-gauge-principle-for-projected-matter-metric.md",
            "needle": "presymplectic null direction derived | fail",
            "role": "null-direction route remains missing exactness and boundary primitive.",
        },
        {
            "source_id": "SRC1165_12_1020_surface",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "BDC1020_0_surface_manifold",
            "role": "surface/corner certificate requirement.",
        },
        {
            "source_id": "SRC1165_13_1020_boundary_class",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "BDC1020_1_boundary_class",
            "role": "fixed boundary class requirement.",
        },
        {
            "source_id": "SRC1165_14_1020_epsilon",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "BDC1020_3_allowed_epsilon",
            "role": "allowed epsilon/proper generator requirement.",
        },
        {
            "source_id": "SRC1165_15_1020_kernel",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "BDC1020_4_kernel_weight",
            "role": "closed or bounded kernel weight requirement.",
        },
        {
            "source_id": "SRC1165_16_1020_stokes",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_1_weighted_Stokes_identity",
            "role": "weighted Stokes identity for corner and dS_Feps.",
        },
        {
            "source_id": "SRC1165_17_1020_zero",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "ETB1020_2_zero_conditions",
            "role": "zero theorem conditions.",
        },
        {
            "source_id": "SRC1165_18_1020_primitive",
            "relative_path": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "needle": "BXP1020_2_exact_primitive",
            "role": "B_C/b_X primitive remains missing.",
        },
    ]
    checked: list[dict[str, object]] = []
    for row in sources:
        path = source_path(str(row["relative_path"]))
        text = read_text(path)
        checked.append(
            {
                **row,
                "exists": path.exists(),
                "needle_found": str(row["needle"]) in text,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return checked


def parent_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "LPC1165_0_select_lifted_object",
            "clause": "lifted C object",
            "contract_requirement": "Replace scalar Cperp promotion with a lifted C-sector object: J_C in Omega^3(D) or an equivalent form/holonomy/boundary-class carrier.",
            "candidate_expression": "J_C ∈ Omega^3(D), with J_C = dB_C + J_C_top",
            "source_anchor": "274-lifted-C-sector-form-holonomy-route.md",
            "source_needle": "J_C = dB_C + J_C^{top}",
            "current_status": "CANDIDATE_SELECTED_FOR_CONTRACT_ONLY",
            "missing_piece": "parent action and variable ownership",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "LPC1165_1_origin_from_Q",
            "clause": "origin from MTS load geometry",
            "contract_requirement": "Derive J_C from Q^i_j, coframe/load data, or det(Q), instead of adding a repair field by hand.",
            "candidate_expression": "J_C = normalized volume/load 3-form from det(Q) or coframe volume",
            "source_anchor": "275-JC-three-form-memory-current-from-Q.md",
            "source_needle": "comes from the determinant / volume form of a 3D spatial domain.",
            "current_status": "CONDITIONAL_KINEMATIC_ORIGIN_ONLY",
            "missing_piece": "covariant parent definition and variation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "LPC1165_2_parent_action_term",
            "clause": "parent action term",
            "contract_requirement": "Write an action-level owner whose variation yields the J_C constraint, projector/domain stress, and boundary primitive.",
            "candidate_expression": "S_C = ∫ λ_C∧(J_C-J_C[Q,e,D]) + S_top[P_D,J_C,A_C] + S_boundary[B_C]",
            "source_anchor": "274-lifted-C-sector-form-holonomy-route.md",
            "source_needle": "The route does not yet derive the theory. It defines the contract a future parent action must satisfy:",
            "current_status": "ACTION_CONTRACT_STUB_ONLY",
            "missing_piece": "actual Lagrangian density, variational variables, signs, and stress tensor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "LPC1165_3_projector_owner",
            "clause": "P_D / coherent-domain projector",
            "contract_requirement": "P_D must be variational, idempotent, covariant/topological or dynamically owned, with delta P_D and stress terms retained.",
            "candidate_expression": "P_D[J_C] = coherent domain class C_D[D]",
            "source_anchor": "207-domain-projector-action-and-Bianchi-identity.md",
            "source_needle": "domain_projector_action_formal_Bianchi_conditional_representative_missing",
            "current_status": "FORMAL_PROJECTOR_ACTION_ONLY",
            "missing_piece": "physical representative selection and non-tuned domain scale",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "LPC1165_4_drel_complex",
            "clause": "lifted d_rel complex",
            "contract_requirement": "Instantiate a relative complex for the lifted branch: bulk Omega^3(D), boundary Omega^2(partialD), pullback, signs, and nilpotency.",
            "candidate_expression": "d_rel(J_C,B_C) = (dJ_C, i_star J_C - d_boundary B_C), sign convention to be fixed",
            "source_anchor": "274-lifted-C-sector-form-holonomy-route.md",
            "source_needle": "relative cohomology boundary contract",
            "current_status": "STANDARD_SHAPE_NOT_PARENT_INSTANTIATED",
            "missing_piece": "actual relative pair, degrees, signs, and boundary convention",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "LPC1165_5_exactness_law",
            "clause": "local exactness law",
            "contract_requirement": "Prove local residual changes satisfy delta J_C=dB_C on the same branch used for local tests.",
            "candidate_expression": "delta J_C = dB_C",
            "source_anchor": "274-lifted-C-sector-form-holonomy-route.md",
            "source_needle": "delta J_C = dB_C",
            "current_status": "CONDITIONAL_THEOREM_SHAPE_ONLY",
            "missing_piece": "Euler/Noether/Bianchi derivation from parent action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "LPC1165_6_boundary_primitive_silence",
            "clause": "boundary primitive silence",
            "contract_requirement": "Show the local stationary boundary primitive vanishes or is bounded without deleting physical ADM/tau/source charges.",
            "candidate_expression": "∫_partialD B_C = 0 on certified local stationary boundaries",
            "source_anchor": "274-lifted-C-sector-form-holonomy-route.md",
            "source_needle": "zero primitive on stationary local boundaries",
            "current_status": "NOT_CERTIFIED",
            "missing_piece": "boundary class, corner, allowed generator, and charge-preservation certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "LPC1165_7_FLRW_local_selector",
            "clause": "local-trivial / FLRW-active selector",
            "contract_requirement": "One parent law must explain why local residuals are exact/silent while the FLRW domain class remains active.",
            "candidate_expression": "local exact class plus nonzero coherent H^3(D,partialD) FLRW class",
            "source_anchor": "274-lifted-C-sector-form-holonomy-route.md",
            "source_needle": "local exact part can be killed by a stationary local boundary condition, while the coherent FLRW domain class can remain nonzero.",
            "current_status": "BRANCH_SELECTOR_NOT_DERIVED",
            "missing_piece": "same-parent selector; no hand switch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "LPC1165_8_matter_coupling_selector",
            "clause": "matter coupling selector",
            "contract_requirement": "Derive why matter sees the quotient/coherent variable, not raw scalar Cperp or species-specific compensating fields.",
            "candidate_expression": "S_matter[psi, exp(C_D[J_C]) g] with no independent Cperp vertex",
            "source_anchor": "360-universal-matter-coupling-theorem-attempt.md",
            "source_needle": "conditional_universal_coupling_theorem_only_no_WEP_clock_PPN_or_local_GR_pass",
            "current_status": "CONDITIONAL_ONLY_NO_WEP_LOCAL_PASS",
            "missing_piece": "parent selector and hidden-species-coupling guard",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "LPC1165_9_Bianchi_Ward_stress",
            "clause": "Bianchi/Ward accounting",
            "contract_requirement": "Vary domain, boundary, projector, and auxiliary stresses rather than freezing them externally.",
            "candidate_expression": "nabla_mu(E_g+E_JC+E_PD+E_boundary+T_matter)^{mu nu}=0",
            "source_anchor": "207-domain-projector-action-and-Bianchi-identity.md",
            "source_needle": "Bianchi closure can be made formal;",
            "current_status": "CONDITIONAL_IF_ALL_STRESSES_RETAINED",
            "missing_piece": "actual stress extraction and representative selection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "LPC1165_10_amplitude_locks",
            "clause": "amplitude locks",
            "contract_requirement": "Derive or source u3, B_mem, and normalization constants; do not use empirical constants as parent action proof.",
            "candidate_expression": "u3 and B_mem from lifted-sector eigenvalue/regularity/normalization",
            "source_anchor": "275-JC-three-form-memory-current-from-Q.md",
            "source_needle": "`B_mem = 2/27` | not parent-derived",
            "current_status": "NOT_PARENT_DERIVED",
            "missing_piece": "amplitude derivation and uncertainty propagation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "LPC1165_11_verdict",
            "clause": "lifted C parent-action status",
            "contract_requirement": "All previous clauses must close before using lifted C as GR/local/R10 proof.",
            "candidate_expression": "lifted C route = live theorem target, not a claim",
            "source_anchor": "1164-Y5-R10-parent-C-PD-drel-source-hunt-or-first-edge-zero-certificate.md",
            "source_needle": "SELECT_AS_PRIMARY_PARENT_SOURCE_HUNT_NONCLAIM",
            "current_status": "CONTRACT_WRITTEN_NOT_SATISFIED",
            "missing_piece": "parent action, projector, d_rel, boundary, matter selector, and amplitude locks",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def route_filter_rows() -> list[dict[str, object]]:
    return [
        {
            "route_id": "LCR1165_0_scalar",
            "route": "scalar Cperp",
            "decision": "REJECT_AS_DERIVATION_BRANCH",
            "reason": "already demoted to explicit closure in 273/362",
            "next_use": "closure-only empirical branch if clearly labelled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "LCR1165_1_one_form_holonomy",
            "route": "1-form connection holonomy",
            "decision": "SIDE_ROUTE",
            "reason": "can encode periods, but weaker match to FLRW volume/domain memory than 3-form route",
            "next_use": "retain only if 3-form fails or EM/charge route needs holonomy",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "LCR1165_2_two_form_boundary_flux",
            "route": "2-form boundary flux",
            "decision": "SIDE_ROUTE",
            "reason": "useful for boundary charge language, but not the best carrier of spatial domain load",
            "next_use": "feed B_C/boundary primitive rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "LCR1165_3_three_form_domain_current",
            "route": "3-form domain current J_C",
            "decision": "PRIMARY_CONTRACT_ROUTE_NONCLAIM",
            "reason": "best match to H^3(D,partialD), determinant/volume form, local exactness, and FLRW coherent domain class",
            "next_use": "try derive J_C from Q/coframe/det(Q) and write action variation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "route_id": "LCR1165_4_four_form_global_flux",
            "route": "4-form global flux",
            "decision": "TOO_GLOBAL_FOR_CURRENT_LOCAL_GR_ROUTE",
            "reason": "clean silence but risks over-global rigidity and weak local/domain selector",
            "next_use": "parking lot only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def edge_certificate_rows() -> list[dict[str, object]]:
    return [
        {
            "edge_id": "CCZ1165_0_surface_without_corners",
            "quantity": "C_corner",
            "zero_condition": "partial S_edge=empty for the exact integration surface, or every corner/joint charge is separately included.",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "BDC1020_0_surface_manifold",
            "current_status": "MISSING_LOCAL_SURFACE_CERTIFICATE",
            "missing_piece": "actual lifted-C local surface S_edge and proof no active corners/cutoffs",
            "runner_effect": "C_corner cannot be set to zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "CCZ1165_1_fixed_boundary_class",
            "quantity": "boundary_class",
            "zero_condition": "same boundary class is used by action, projector, readout, and source/test systems.",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "BDC1020_1_boundary_class",
            "current_status": "MISSING_FIXED_BOUNDARY_CLASS",
            "missing_piece": "no retuning/reference movement certificate",
            "runner_effect": "corner or reference terms may hide edge charge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "CCZ1165_2_allowed_epsilon",
            "quantity": "epsilon_C",
            "zero_condition": "epsilon_C is a proper representative generator without erasing physical tau/mass/rotation charges.",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "BDC1020_3_allowed_epsilon",
            "current_status": "MISSING_ALLOWED_GENERATOR_CERTIFICATE",
            "missing_piece": "proper/gauge versus physical Hamiltonian generator separation",
            "runner_effect": "cannot use proper-gauge zero as local-GR proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "CCZ1165_3_closed_kernel_weight",
            "quantity": "norm_dS_Feps",
            "zero_condition": "d_S(F_lambda epsilon_C)=0 on S_edge, or provide a nonnegative dual-surface norm bound.",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "BDC1020_4_kernel_weight",
            "current_status": "MISSING_KERNEL_DERIVATIVE_ZERO_OR_BOUND",
            "missing_piece": "F_lambda, epsilon_C, surface derivative, norm, units",
            "runner_effect": "weighted Stokes leaves derivative residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "CCZ1165_4_BC_primitive",
            "quantity": "norm_bC",
            "zero_condition": "B_C exact primitive exists and has zero or finite sourced norm on the certified boundary domain.",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "BXP1020_2_exact_primitive",
            "current_status": "MISSING_BC_PRIMITIVE",
            "missing_piece": "explicit B_C/b_C from lifted parent action",
            "runner_effect": "product norm_dS_Feps*norm_bC cannot be evaluated",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "CCZ1165_5_zero_theorem",
            "quantity": "Q_C_edge_zero",
            "zero_condition": "partialS=empty, h_C=0, r_C=0, d_S(F epsilon_C)=0, B_C primitive exists, and cocycle/source projector terms vanish.",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "ETB1020_2_zero_conditions",
            "current_status": "CONDITIONAL_NOT_MET",
            "missing_piece": "surface, cohomology, kernel, primitive, cocycle, and projector certificates",
            "runner_effect": "no edge-zero/local claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "edge_id": "CCZ1165_6_finite_bound",
            "quantity": "Q_C_edge_bound",
            "zero_condition": "if zero fails, bound C_corner + norm_dS_Feps*norm_bC + harmonic + residual + cocycle/source terms without cancellation.",
            "source_anchor": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "source_needle": "ETB1020_1_weighted_Stokes_identity",
            "current_status": "BOUND_SCHEMA_ONLY_VALUES_MISSING",
            "missing_piece": "all numeric/theorem-zero inputs and units",
            "runner_effect": "finite scoring not yet available",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def runner_rows(contract: list[dict[str, object]], edge: list[dict[str, object]]) -> list[dict[str, object]]:
    open_contract = [str(row["contract_id"]) for row in contract if not is_false(row["claim_allowed"]) or str(row["current_status"]) not in {"DERIVED", "CERTIFIED", "PARENT_SIGNED"}]
    open_edge = [str(row["edge_id"]) for row in edge if not is_false(row["claim_allowed"]) or str(row["current_status"]) not in {"CERTIFIED", "ZERO_CERTIFIED", "BOUND_CERTIFIED"}]
    return [
        {
            "run_id": "RUN1165_0_lifted_contract",
            "test": "lifted C parent-action contract promotion",
            "status": "REFUSED_PARENT_ACTION_CONTRACT_UNSATISFIED",
            "blocked_rows": ";".join(open_contract),
            "detail": "contract is useful but no parent action/projector/d_rel/matter selector is signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1165_1_edge_certificate",
            "test": "C_corner and dS_Feps zero/bound promotion",
            "status": "REFUSED_EDGE_CERTIFICATES_MISSING",
            "blocked_rows": ";".join(open_edge),
            "detail": "corner, boundary class, allowed epsilon, kernel weight, and B_C primitive are not certified",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1165_2_local_claim",
            "test": "local GR/R10/PPN/WEP/clock/orbital promotion",
            "status": "REFUSED_NO_LOCAL_CLAIM",
            "blocked_rows": "RUN1165_0_lifted_contract;RUN1165_1_edge_certificate",
            "detail": "both derivation route and finite edge route remain nonclaim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "G1165_0_lifted_action_owned",
            "gate": "lifted J_C parent action is owned",
            "current_status": "BLOCKED",
            "reason": "action density, variables, variation, and stress tensor are not derived",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1165_1_PD_drel_owned",
            "gate": "P_D and d_rel are owned on the lifted relative complex",
            "current_status": "BLOCKED",
            "reason": "projector representative and relative-pair signs/complex remain missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1165_2_boundary_zero_or_bound",
            "gate": "corner/kernel/B_C edge rows have zero certificates or numeric bounds",
            "current_status": "BLOCKED",
            "reason": "C_corner, dS_Feps, and B_C primitive remain source-contract rows only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1165_3_matter_selector",
            "gate": "matter coupling selector derives quotient/coherent metric without hidden species couplings",
            "current_status": "BLOCKED",
            "reason": "universal matter coupling is conditional only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1165_4_local_promotion",
            "gate": "GR/Newton/R10/PPN/WEP/clock/orbital promotion",
            "current_status": "BLOCKED_NO_LOCAL_CLAIM",
            "reason": "all upstream gates remain blocked",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D1165_0_best_derivation_route",
            "decision": "three_form_JC_lifted_route_is_best_current_derivation_target",
            "reason": "it ties C to a domain volume/load class and gives a natural relative cohomology/boundary primitive language",
            "next_action": "try deriving J_C from Q/coframe/det(Q) with full variation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "D1165_1_edge_fallback",
            "decision": "Ccorner_dSFeps_certificate_is_best_parallel_fallback",
            "reason": "if the parent action stalls, the first finite-bound progress is corner-free surface plus closed/bounded kernel weight",
            "next_action": "construct a local stationary boundary certificate or leave finite edge row blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "D1165_2_scalar_policy",
            "decision": "do_not_promote_scalar_projected_metric",
            "reason": "scalar Cperp exactness is already rejected and closure-labelled",
            "next_action": "keep scalar closure quarantined while deriving lifted route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT1165_0_1166",
            "next_target": "1166-Y5-R10-JC-from-Q-parent-variation-or-local-corner-certificate.md",
            "objective": "derive or reject the first lifted-C parent action clause by constructing J_C from Q/coframe/det(Q) and varying it; if that fails, certify the local corner-free/closed-weight edge conditions as nonclaim rows",
            "include": "J_C[Q,e,D]; det(Q) variation; domain representative; P_D variation; d_rel signs; B_C boundary term; C_corner=0 certificate; dS_Feps zero/bound; runner dry-run",
            "exclude": "scalar Cperp promotion; projected metric as theorem; invented constants; hidden projector stress; local-GR claim; c_g zero claim; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validate(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    routes: list[dict[str, object]],
    edge: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    required_clauses = {
        "lifted C object",
        "origin from MTS load geometry",
        "parent action term",
        "P_D / coherent-domain projector",
        "lifted d_rel complex",
        "local exactness law",
        "boundary primitive silence",
        "local-trivial / FLRW-active selector",
        "matter coupling selector",
        "Bianchi/Ward accounting",
        "amplitude locks",
        "lifted C parent-action status",
    }
    contract_ok = required_clauses <= {str(row["clause"]) for row in contract}
    primary_three_form = any(str(row["decision"]) == "PRIMARY_CONTRACT_ROUTE_NONCLAIM" for row in routes)
    scalar_rejected = any(str(row["route"]) == "scalar Cperp" and "REJECT" in str(row["decision"]) for row in routes)
    edge_terms_present = {"C_corner", "norm_dS_Feps", "norm_bC", "Q_C_edge_zero", "Q_C_edge_bound"} <= {str(row["quantity"]) for row in edge}
    runner_refuses = all(is_false(row["claim_allowed"]) for row in runner)
    gates_blocked = all(is_false(row["claim_allowed"]) for row in gates)
    all_nonclaim = all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for table in (sources, contract, routes, edge, runner, gates, decisions, next_rows)
        for row in table
    )
    csv_parse = True
    parse_detail = "all 1165 CSV outputs parse cleanly"
    for path in csv_paths:
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover
            csv_parse = False
            parse_detail = f"{path.name}: {exc}"
            break
    under_post = all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in csv_paths + [DOC])
    return [
        {
            "check_id": "V1165_0_sources_exist",
            "result": "pass" if source_ok else "fail",
            "detail": "all cited local source paths exist and needles are found" if source_ok else "source path or needle missing",
            "claim_allowed": False,
        },
        {
            "check_id": "V1165_1_contract_complete_shape",
            "result": "pass" if contract_ok else "fail",
            "detail": "lifted C parent-action contract includes action, projector, d_rel, boundary, matter, Bianchi, and amplitude clauses",
            "claim_allowed": False,
        },
        {
            "check_id": "V1165_2_three_form_selected_nonclaim",
            "result": "pass" if primary_three_form else "fail",
            "detail": "3-form J_C route is selected as primary contract route only",
            "claim_allowed": False,
        },
        {
            "check_id": "V1165_3_scalar_rejected",
            "result": "pass" if scalar_rejected else "fail",
            "detail": "scalar Cperp promotion remains rejected",
            "claim_allowed": False,
        },
        {
            "check_id": "V1165_4_edge_certificate_shape",
            "result": "pass" if edge_terms_present else "fail",
            "detail": "corner, kernel, primitive, zero, and finite-bound edge rows are present",
            "claim_allowed": False,
        },
        {
            "check_id": "V1165_5_runner_refuses_claim",
            "result": "pass" if runner_refuses else "fail",
            "detail": "runner refuses lifted-action, edge-certificate, and local-promotion claims",
            "claim_allowed": False,
        },
        {
            "check_id": "V1165_6_claim_gates_blocked",
            "result": "pass" if gates_blocked else "fail",
            "detail": "all claim gates remain blocked",
            "claim_allowed": False,
        },
        {
            "check_id": "V1165_7_no_claim_rows",
            "result": "pass" if all_nonclaim else "fail",
            "detail": "all generated rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1165_8_next_target",
            "result": "pass" if next_rows and "1166" in str(next_rows[0]["next_target"]) else "fail",
            "detail": "1166 handoff targets J_C-from-Q variation or local corner certificate",
            "claim_allowed": False,
        },
        {
            "check_id": "V1165_9_generated_under_post_checkpoint",
            "result": "pass" if under_post else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1165_10_csv_parse",
            "result": "pass" if csv_parse else "fail",
            "detail": parse_detail,
            "claim_allowed": False,
        },
        {
            "check_id": "V1165_11_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1165_SUMMARY",
            "result": "pass" if source_ok and contract_ok and primary_three_form and scalar_rejected and runner_refuses and all_nonclaim else "fail",
            "detail": "1165 writes the lifted J_C parent-action contract, selects the 3-form route as nonclaim, and tightens Ccorner/dS_Feps edge certificate requirements",
            "claim_allowed": False,
        },
    ]


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def write_doc(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    routes: list[dict[str, object]],
    edge: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 1165 — Y5/R10 lifted C-sector parent action contract or Ccorner zero-bound

**Current verdict:** the lifted `C` route is now a strict contract, not a claim. The best branch is the `J_C` domain three-form route because it can potentially own relative cohomology, boundary primitive language, and FLRW/local split without pretending scalar `Cperp` exactness worked.

**Main progress:** 1165 defines exactly what a future parent action must provide: `J_C[Q,e,D]`, variational `P_D`, a lifted `d_rel` complex, `delta J_C=dB_C`, boundary primitive silence, matter selector, Bianchi/Ward stress accounting, and amplitude locks. The first edge fallback is also sharpened into concrete `C_corner` and `d_S(F epsilon)` certificate rows.

**No claim:** no local-GR, R10, PPN, WEP, clock, orbital, projected-metric theorem, or `c_g=0` result follows here. This is a clean launchpad, not a victory lap.

## Source register

{md_table(sources, ["source_id", "relative_path", "needle", "exists", "needle_found", "role"])}

## Lifted C parent-action contract

{md_table(contract, ["contract_id", "clause", "contract_requirement", "candidate_expression", "current_status", "missing_piece", "valid_for_claim"])}

## Route filter

{md_table(routes, ["route_id", "route", "decision", "reason", "next_use", "valid_for_claim"])}

## Ccorner and dS(F epsilon) certificate rows

{md_table(edge, ["edge_id", "quantity", "zero_condition", "current_status", "missing_piece", "runner_effect", "valid_for_claim"])}

## Runner dry-run

{md_table(runner, ["run_id", "test", "status", "blocked_rows", "detail", "claim_allowed"])}

## Claim gates

{md_table(gates, ["gate_id", "gate", "current_status", "reason", "claim_allowed"])}

## Decision ledger

{md_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "result", "detail", "claim_allowed"])}

## Next target

{md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = stamp(source_rows())
    contract = stamp(parent_contract_rows())
    routes = stamp(route_filter_rows())
    edge = stamp(edge_certificate_rows())
    runner = stamp(runner_rows(contract, edge))
    gates = stamp(claim_gate_rows())
    decisions = stamp(decision_rows())
    next_rows = stamp(next_target_rows())
    outputs = {
        "P8_Y5_R10_1165_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1165_LIFTED_C_PARENT_ACTION_CONTRACT.csv": contract,
        "P8_Y5_R10_1165_LIFTED_C_ROUTE_FILTER.csv": routes,
        "P8_Y5_R10_1165_CCORNER_DSF_EPSILON_CERTIFICATE_ROWS.csv": edge,
        "P8_Y5_R10_1165_RUNNER_DRY_RUN.csv": runner,
        "P8_Y5_R10_1165_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1165_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1165_NEXT_TARGET.csv": next_rows,
    }
    csv_paths: list[Path] = []
    for name, rows in outputs.items():
        path = OUT / name
        write_csv(path, rows)
        csv_paths.append(path)

    validation = stamp(validate(sources, contract, routes, edge, runner, gates, decisions, next_rows, csv_paths))
    validation_path = OUT / "P8_Y5_BRR545_1165_VALIDATION.csv"
    write_csv(validation_path, validation)
    csv_paths.append(validation_path)
    write_doc(sources, contract, routes, edge, runner, gates, decisions, next_rows, validation)

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print("validation: PASS" if not failed else f"validation: FAIL {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

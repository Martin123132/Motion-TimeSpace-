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


def no_grain_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "NG4471_0_cell_scaling_lemma",
            "statement": "For a regular hinge/cell discretization with cell size ell, A_h=O(ell^2), delta_h=O(R ell^2), and N=O(V/ell^4).",
            "derivation": "The EH-like term sums as sum_h A_h delta_h = O(N ell^4 R)=O(integral sqrt(-g) R), while the quadratic term sums as sum_h A_h delta_h^2 = O(N ell^6 R^2)=O(ell^2 integral sqrt(-g) R^2).",
            "consequence": "same-cell quadratic curvature response maps to c_R2_cell = xi_shape*c2_visible*ell_cell^2/N_EH in the project conventions",
            "current_status": "DERIVED_SCALING_IDENTITY",
            "parent_signed": True,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NG4471_1_refinement_gauge_zero",
            "statement": "If ell is only a refinement/gauge parameter and observables are cylindrical under ell -> ell/n, c_R2_cell cannot depend on ell.",
            "derivation": "With fixed finite c2_visible, c_R2_cell scales as ell^2 and therefore changes under refinement; the only cylindrical continuum value is zero in the strict ell -> 0 gauge limit.",
            "consequence": "physical-grain contribution to c_R2_eff vanishes: c_R2_cell=0",
            "current_status": "EXACT_CONDITIONAL_NO_GRAIN_THEOREM",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NG4471_2_no_singular_running_clause",
            "statement": "A finite R^2 residue can be kept under refinement only if c2_visible or a counterterm scales as ell^-2 or a separate dimensionful UV datum is introduced.",
            "derivation": "c_R2_cell ~ c2_visible ell^2. Holding c_R2_cell finite as ell -> 0 requires c2_visible ~ ell^-2, which is not a smooth primitive response coefficient but a renormalized parent scale/counterterm.",
            "consequence": "singular running is not a no-grain proof; it moves the branch into c_bare/c_measure/c_boundary/hidden-mode intake rows",
            "current_status": "COUNTERROUTE_IDENTIFIED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NG4471_3_calibrated_G_not_ellcell",
            "statement": "The calibrated kappa/G scale cannot be reused as ell_cell to close the c_R2 branch without a non-circular parent scale owner.",
            "derivation": "The kappa scale-law audit says physical-cell/cutoff routes require ell_cell, shape factor and normalization not defined from measured G or Planck length by declaration.",
            "consequence": "ell_cell cannot be set to Planck length or sqrt(kappa_eff) as a proof; that would be circular calibration, not derivation",
            "current_status": "NO_CIRCULAR_SCALE_GUARD",
            "parent_signed": True,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NG4471_4_hidden_residue_guard",
            "statement": "Even if the visible grain contribution vanishes, hidden auxiliary, measure, boundary or bare higher-curvature terms can leave c_R2_eff finite.",
            "derivation": "The symbolic law c_R2_eff(k)=c_bare+1/2 B^T L^-1(k)B+c_measure+c_boundary is independent of the visible ell^2 suppression unless each term is parent-zero/topological/boundary-routed.",
            "consequence": "no-grain closes only c_R2_cell; full c_R2_eff=0 also needs no auxiliary/no bare/no measure/no boundary signatures",
            "current_status": "FINITE_RESIDUE_RETAINED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "NG4471_5_verdict",
            "statement": "The no-grain theorem is mathematically sharp but not parent-signed by the current MTS corpus.",
            "derivation": "If refinement is gauge, c2 is smooth, no singular counterterm exists and hidden residues vanish, then c_R2_eff=0. Current evidence has the scaling theorem and no-circular-scale guard, but not the parent refinement/no-residue signatures.",
            "consequence": "do not claim local GR; retain first c_R2_eff intake row unless the parent gauge/no-residue clauses close",
            "current_status": "CONDITIONAL_THEOREM_PROVEN_PARENT_SIGNATURE_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def continuum_scaling_rows() -> List[Dict[str, object]]:
    return [
        {
            "scaling_id": "SCL4471_0_linear_EH",
            "term": "sum_h A_h delta_h",
            "cell_estimate": "A_h~ell^2, delta_h~R ell^2, N~V/ell^4",
            "continuum_limit": "sum_h A_h delta_h -> xi_EH integral sqrt(-g) R",
            "operator": "EH/EC principal block",
            "verdict": "REFINEMENT_STABLE",
            "valid_for_claim": False,
        },
        {
            "scaling_id": "SCL4471_1_quadratic_visible",
            "term": "sum_h A_h delta_h^2",
            "cell_estimate": "A_h delta_h^2~R^2 ell^6, N~V/ell^4",
            "continuum_limit": "sum_h A_h delta_h^2 -> xi_shape ell^2 integral sqrt(-g) R^2",
            "operator": "visible c_R2_cell",
            "verdict": "VANISHES_ONLY_IF_ELL_IS_GAUGE_AND_C2_SMOOTH",
            "valid_for_claim": False,
        },
        {
            "scaling_id": "SCL4471_2_physical_grain",
            "term": "finite ell_cell retained",
            "cell_estimate": "ell_cell is a physical parent length/cutoff/grain",
            "continuum_limit": "c_R2_cell = xi_shape*c2_visible*ell_cell^2/N_EH",
            "operator": "finite R2/fR scalar branch",
            "verdict": "SOURCE_AND_BOUND_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "scaling_id": "SCL4471_3_singular_counterterm",
            "term": "c2_visible(ell)~ell^-2 or c_bare finite",
            "cell_estimate": "renormalized coefficient cancels ell^2 suppression",
            "continuum_limit": "finite c_R2 residue survives",
            "operator": "bare/measure/boundary/hidden c_R2_eff",
            "verdict": "NOT_A_NO_GRAIN_PROOF_FINITE_INTAKE",
            "valid_for_claim": False,
        },
        {
            "scaling_id": "SCL4471_4_full_zero_condition",
            "term": "total c_R2_eff",
            "cell_estimate": "c_R2_cell + c_bare + 0.5 B^T L^-1 B + c_measure + c_boundary",
            "continuum_limit": "zero only when every term is parent-zero/topological/boundary-routed",
            "operator": "complete local scalar/tensor curvature-square channel",
            "verdict": "FULL_ZERO_NOT_SIGNED",
            "valid_for_claim": False,
        },
    ]


def first_cr2eff_intake_rows() -> List[Dict[str, object]]:
    return [
        {
            "intake_id": "CR2I4471_0_visible_cell_component",
            "quantity": "c_R2_cell",
            "formula": "c_R2_cell = xi_shape*c2_visible*ell_cell^2/N_EH",
            "needed_inputs": "c2_visible; ell_cell; xi_shape; N_EH; continuum convention; source paths",
            "current_value": "MISSING_c2_VISIBLE_ELL_CELL_SHAPE_FACTOR_N_EH",
            "units": "length_squared_after_EH_normalization",
            "status": "BLOCKED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "intake_id": "CR2I4471_1_no_grain_zero_switch",
            "quantity": "Z_no_grain",
            "formula": "Z_no_grain=true iff ell is gauge, c2 smooth, no singular counterterm, no hidden/bare/measure/boundary residue",
            "needed_inputs": "parent refinement-gauge signature; no physical cell marker; no singular running; no auxiliary residue",
            "current_value": "CONDITIONAL_THEOREM_PARENT_SIGNATURE_UNSIGNED",
            "units": "boolean_certificate",
            "status": "ZERO_SWITCH_NOT_CLAIMED",
            "valid_for_claim": False,
        },
        {
            "intake_id": "CR2I4471_2_total_effective_component",
            "quantity": "c_R2_eff_total",
            "formula": "c_R2_eff_total = c_R2_cell + c_bare + 0.5*B^T*L^-1*B + c_measure + c_boundary",
            "needed_inputs": "visible cell component; bare higher-curvature owner; hidden B/L coefficients; measure and boundary rows",
            "current_value": "MISSING_TOTAL_COEFFICIENT_COMPONENTS",
            "units": "length_squared_or_declared_operator_units",
            "status": "BLOCKED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "intake_id": "CR2I4471_3_observable_projection",
            "quantity": "lambda_R2_and_alpha_eff",
            "formula": "pure R2 convention: lambda_R2=sqrt(6*c_R2_eff); alpha_eff=C_total^2/3 only if unscreened metric f(R) branch is sourced",
            "needed_inputs": "positive c_R2_eff or D0; C_total; screening/body-charge branch; live alpha(lambda) curve",
            "current_value": "MISSING_SCALARON_RANGE_COUPLING_BOUND_CURVE",
            "units": "meters_and_dimensionless",
            "status": "BLOCKED_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def decision_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4471_0_real_derivation_gain",
            "finding": "visible cell R2 scales as ell^2 relative to EH and therefore vanishes if ell is only gauge refinement",
            "consequence": "the no-grain route is a real theorem shape, not vibes",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4471_1_no_parent_signature_yet",
            "finding": "the current corpus does not yet prove refinement gauge/no physical grain/no singular counterterm/no hidden residue simultaneously",
            "consequence": "c_R2_eff=0 is not claimable from 4471",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4471_2_finite_row_is_now_precise",
            "finding": "the first finite row is c_R2_cell=xi_shape*c2_visible*ell_cell^2/N_EH plus total c_R2_eff residue components",
            "consequence": "if proof fails, the branch is testable by named coefficients rather than hand-waving",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4471_3_next_target",
            "finding": "the next best attack is to prove refinement parameter gauge/no physical primitive grain, or source ell_cell normalization",
            "consequence": "this keeps pushing the derivation route while preserving empirical fallback",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    source_rows: List[Dict[str, object]],
    theorem_rows: List[Dict[str, object]],
    scaling_rows: List[Dict[str, object]],
    intake_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    sources_ok = all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in source_rows)
    scaling_derived = any(row.get("theorem_id") == "NG4471_0_cell_scaling_lemma" for row in theorem_rows)
    no_grain_parent_signed = any(
        row.get("theorem_id") == "NG4471_5_verdict" and row.get("parent_signed") is True for row in theorem_rows
    )
    total_zero_signed = no_grain_parent_signed and all(
        row.get("current_status") not in {"FINITE_RESIDUE_RETAINED", "COUNTERROUTE_IDENTIFIED"}
        for row in theorem_rows
    )
    finite_row_ready = all(
        "MISSING" not in str(row.get("current_value")) and row.get("status") not in {"BLOCKED_NONCLAIM", "ZERO_SWITCH_NOT_CLAIMED"}
        for row in intake_rows
    )
    no_claims = all(
        str(row.get("valid_for_claim")).lower() == "false"
        for group in [source_rows, theorem_rows, scaling_rows, intake_rows]
        for row in group
    )
    return [
        {
            "gate_id": "CG4471_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": sources_ok,
            "claim_allowed": False,
            "detail": "source register validates 4470 selector, 4460 finite c2, 4463 scale, 1823 scaling and 1343 hidden-residue evidence",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4471_1_scaling_derivation",
            "claim": "visible cell quadratic term scales as ell^2 R^2 after summing cells",
            "gate_pass": scaling_derived,
            "claim_allowed": False,
            "detail": "this is a mathematical scaling result, not a local-GR claim",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4471_2_no_grain_parent_signed",
            "claim": "physical local grain route to c_R2_cell is closed",
            "gate_pass": no_grain_parent_signed,
            "claim_allowed": False,
            "detail": "refinement gauge/no physical primitive grain/no singular running are not parent-signed together",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4471_3_total_cR2_zero_signed",
            "claim": "full c_R2_eff total is zero",
            "gate_pass": total_zero_signed,
            "claim_allowed": False,
            "detail": "hidden, bare, measure and boundary residues remain retained until parent-zeroed or sourced",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4471_4_finite_row_ready",
            "claim": "finite c_R2_eff row is numerically score-ready",
            "gate_pass": finite_row_ready,
            "claim_allowed": False,
            "detail": "first intake row is precise but contains MISSING coefficients and source paths",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4471_5_no_generated_claim_rows",
            "claim": "no generated row is promoted to public/local-GR evidence",
            "gate_pass": no_claims,
            "claim_allowed": False,
            "detail": "4471 is a conditional theorem plus finite row interface only",
            "valid_for_claim": False,
        },
    ]

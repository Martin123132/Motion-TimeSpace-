from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1772"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1772_0_1771_handoff",
        "source_key": "1771_pim_next",
        "source_path": ROOT / "1771-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md",
        "needles": ["PIM_COMMUTATOR_PROJECTOR_VARIATION_ZERO_OR_BOUND_IS_NEXT", "NEXT1771_0_primary"],
    },
    {
        "source_id": "SRC1772_1_1771_validation",
        "source_key": "1771_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1771_VALIDATION.csv",
        "needles": ["VAL1771_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1772_2_1771_bounds",
        "source_key": "1771_operator_bounds",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1771_OPERATOR_BOUND_INPUT_PACK.csv",
        "needles": ["OBI1771_2_projector", "MISSING_PIM_COMMUTATOR_PROJECTOR_STRESS"],
    },
    {
        "source_id": "SRC1772_3_1013_product",
        "source_key": "1013_product_rule_obstruction",
        "source_path": ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
        "needles": ["PFC1013_2_product_rule", "OBS1013_1_PiM_commutator"],
    },
    {
        "source_id": "SRC1772_4_1013_decision",
        "source_key": "1013_commutator_decision",
        "source_path": ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
        "needles": ["DEC1013_2_next_commutator", "projector-stress coefficients"],
    },
    {
        "source_id": "SRC1772_5_1014_prior",
        "source_key": "1014_prior_commutator_checkpoint",
        "source_path": ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
        "needles": ["PCT1014_2_commutator_zero", "PCT1014_7_verdict"],
    },
    {
        "source_id": "SRC1772_6_pim_algebra",
        "source_key": "PiM_algebra_contract",
        "source_path": RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        "needles": ["PM5_projector_variation_owned", "PM6_flux_closure_requires_Ward_or_Euler"],
    },
    {
        "source_id": "SRC1772_7_pim_stress",
        "source_key": "PiM_projector_variation_stress",
        "source_path": RESIDUALS / "P8_PiM_projector_variation_stress_CONTRACT.csv",
        "needles": ["PV1_topological_absolute_charge_route", "PV6_modified_exterior_residual_map"],
    },
    {
        "source_id": "SRC1772_8_commutator_gate",
        "source_key": "PiM_commutator_gate",
        "source_path": RESIDUALS / "P8_Y5_PIM_COMMUTATOR_GATE.csv",
        "needles": ["PC521_0_product_rule", "PC521_2_topological_zero_commutator"],
    },
    {
        "source_id": "SRC1772_9_bound_template",
        "source_key": "PiM_bound_input_template",
        "source_path": RESIDUALS / "P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv",
        "needles": ["PIF537_1_I_commutator", "PIF537_3_projector_stress_beta_equiv"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1772_SOURCE_REGISTER.csv",
    "commutator_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1772_PIM_COMMUTATOR_ZERO_ATTEMPT.csv",
    "route_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1772_PIM_ROUTE_AUDIT.csv",
    "projector_stress": RESIDUALS / "P8_Y5_PARENT_QLOC_1772_PROJECTOR_STRESS_AUDIT.csv",
    "coefficient_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1772_PIM_COEFFICIENT_BOUND_PACK.csv",
    "impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1772_GR_NEWTON_IMPACT_LEDGER.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1772_COUNTERMODEL_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1772_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1772_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1772_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1772_VALIDATION.csv",
}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": all(needle in text for needle in needles),
                "needles": ";".join(needles),
                "role": "Pi_M commutator/projector variation zero or coefficient bound",
                "valid_for_claim": False,
            }
        )
    return rows


def commutator_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PCZ1772_0_product_rule",
            "claim_piece": "full projected-current product rule",
            "mathematical_form": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H",
            "status": "EXACT_OBSTRUCTION_ACTIVE",
            "proof_result": "commutator term must be zero, parent-owned, or bounded",
            "remaining_gap": "current MTS has not proved Pi_M is covariantly fixed on the Hilbert current domain",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PCZ1772_1_topological_zero",
            "claim_piece": "topological Pi_M kills commutator",
            "mathematical_form": "Pi_M J = ell_M(J) omega_M_top, d omega_M_top=0, delta_g Pi_M=0 => [d,Pi_M]J=0",
            "status": "CONDITIONAL_THEOREM_CLEAN",
            "proof_result": "if Pi_M is fixed absolute topological charge data, the commutator/projector-stress route closes",
            "remaining_gap": "must prove Pi_M J_H equals the observed Hilbert projected current, not merely a closed topological current",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PCZ1772_2_hilbert_equality_blocker",
            "claim_piece": "topological-Hilbert equality",
            "mathematical_form": "Pi_M J_H = J_M_top + dB_zero with integral_boundary dB_zero=0",
            "status": "KEY_BLOCKER_NOT_DERIVED",
            "proof_result": "closed topological charge can still be the wrong conserved object",
            "remaining_gap": "R_eq_integral or parent Hilbert/worldtube equality theorem required",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PCZ1772_3_Hodge_route",
            "claim_piece": "Hodge/DeWitt/domain projector implementation",
            "mathematical_form": "Pi_H(g,domain) gives delta_g Pi_H, delta chi_D, delta n_mu, delta G_B",
            "status": "RETAINED_IF_USED",
            "proof_result": "metric/domain-dependent projectors carry projector stress unless varied and zeroed",
            "remaining_gap": "T_PiM / projector_stress_beta_equiv map missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PCZ1772_4_current_verdict",
            "claim_piece": "current MTS Pi_M commutator zero",
            "mathematical_form": "[d,Pi_M]J_H=0 and delta Pi_M stress=0",
            "status": "FAIL_CURRENT_PARENT_PROOF",
            "proof_result": "zero route is exact only after topological-Hilbert equality and no-extra-projection certificates",
            "remaining_gap": "I_commutator, R_eq, B_zero_flux, and T_PiM remain nonclaim coefficient rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def route_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "PRA1772_0_topological_metric_independent",
            "route": "fixed topological absolute charge map",
            "condition": "Pi_M is fixed before readout, metric independent, and built from a closed S2 charge representative",
            "current_status": "CONDITIONAL_COMMUTATOR_ZERO",
            "risk": "topological current may not equal Pi_M J_H",
            "required_next": "topological-Hilbert equality theorem or R_eq bound",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "PRA1772_1_Hilbert_worldtube_equality",
            "route": "same Hilbert compact-source worldtube",
            "condition": "Pi_M J_H = J_M_top + dB_zero and M_source[W]=int_S Q_M[tau] before orbital fitting",
            "current_status": "FAIL_OPEN",
            "risk": "conserved wrong object gives false Newton/source-normalization pass",
            "required_next": "R_eq_integral and worldtube equality closure",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "PRA1772_2_Hodge_domain",
            "route": "Hodge/DeWitt/domain projector",
            "condition": "Pi_M depends on boundary metric, Green operator, normal, domain selector, or homology representative",
            "current_status": "RETAINED_STRESS_ROUTE",
            "risk": "delta_g Pi_M induces PPN/source-normalization stress",
            "required_next": "T_PiM and projector_stress_beta_equiv bound map",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "PRA1772_3_readout_mask",
            "route": "post-readout mass mask",
            "condition": "Pi_M chosen after orbit/readout or adjusted to measured GM",
            "current_status": "FORBIDDEN_AS_DERIVATION",
            "risk": "GM laundering",
            "required_next": "closure-only label if used; no derivation credit",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "PRA1772_4_verdict",
            "route": "Pi_M zero proof for current branch",
            "condition": "topological route + Hilbert equality + no extra projection + boundary silence",
            "current_status": "NOT_PARENT_SIGNED",
            "risk": "Newton/local-GR gates remain blocked",
            "required_next": "1773 topological-Hilbert equality or R_eq bound",
            "valid_for_claim": False,
        },
    ]


def projector_stress_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "stress_id": "PSA1772_0_delta_PiM",
            "quantity": "Delta_PiM",
            "mathematical_form": "delta(Pi_M J_H)=Pi_M delta J_H + (delta Pi_M)J_H",
            "status": "MISSING_DELTA_PIM_THEOREM_OR_BOUND",
            "impact": "hidden projector-source stress if omitted",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "stress_id": "PSA1772_1_T_PiM",
            "quantity": "T_PiM_munu",
            "mathematical_form": "T_PiM_munu := -2/sqrt(-g) delta S_PiM/delta g_munu",
            "status": "MISSING_PROJECTOR_STRESS_MAP",
            "impact": "PPN gamma/beta/preferred-frame and local-GR residual",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "stress_id": "PSA1772_2_boundary_domain",
            "quantity": "domain/boundary variation",
            "mathematical_form": "delta Sigma_ext, delta chi_D, delta n_mu, delta G_B",
            "status": "MISSING_DOMAIN_HOMOLOGY_VARIATION_SILENCE",
            "impact": "preferred-location/radial/source-normalization residual",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "stress_id": "PSA1772_3_topological_no_stress",
            "quantity": "topological no-stress branch",
            "mathematical_form": "delta_g Pi_M=0 if Pi_M is fixed absolute cohomology data",
            "status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "impact": "would close projector-stress if Hilbert equality also closes",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "stress_id": "PSA1772_4_verdict",
            "quantity": "projector stress for current MTS",
            "mathematical_form": "T_PiM=0",
            "status": "NOT_DERIVED_RETAIN_BOUND_ROWS",
            "impact": "local-GR/Newton gates remain closed",
            "valid_for_claim": False,
        },
    ]


def coefficient_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCB1772_0_R_eq_integral",
            "quantity": "R_eq_integral",
            "definition": "finite-shell integral of Pi_M J_H - J_M_top - dB_zero",
            "units": "dimensionless_after_MHref_normalization",
            "status": "MISSING_R_EQ_INTEGRAL",
            "maps_to": "wrong conserved object; source normalization; radial source hair",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCB1772_1_I_commutator",
            "quantity": "I_commutator",
            "definition": "finite-annulus integral of [d,Pi_M]J_H",
            "units": "GM_flux_or_dimensionless_after_Meff_normalization",
            "status": "MISSING_I_COMMUTATOR",
            "maps_to": "epsilon_radial_Meff; measured GM; R10/R11",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCB1772_2_B_zero_flux",
            "quantity": "B_zero_flux",
            "definition": "boundary/reference improvement flux through compact linked boundary",
            "units": "GM_flux_or_dimensionless",
            "status": "MISSING_B_ZERO_FLUX",
            "maps_to": "boundary/reference charge closure",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCB1772_3_projector_stress_beta_equiv",
            "quantity": "projector_stress_beta_equiv",
            "definition": "weak-field/PPN equivalent of metric stress generated by projector variation",
            "units": "PPN_or_operator_units",
            "status": "MISSING_PROJECTOR_STRESS_MAP",
            "maps_to": "gamma,beta,alpha_i,R11,local-GR",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCB1772_4_Delta_PiM",
            "quantity": "Delta_PiM",
            "definition": "projector-ownership/variation residual in measured source flux",
            "units": "GM_flux_or_dimensionless",
            "status": "MISSING_DELTA_PIM",
            "maps_to": "radial source hair, source normalization",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCB1772_5_epsilon_radial_Meff",
            "quantity": "epsilon_radial_Meff",
            "definition": "M_eff_ref^-1 int_A[-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent]",
            "units": "dimensionless",
            "status": "MISSING_EPSILON_RADIAL_MEFF",
            "maps_to": "R10/R11/orbital radial bounds",
            "valid_for_claim": False,
        },
    ]


def impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1772_0_EH_dominance",
            "bridge_piece": "EH dominance",
            "impact": "nonzero projector stress contributes to DeltaE_munu",
            "current_status": "BLOCKED_BY_T_PIM",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1772_1_Newton_source",
            "bridge_piece": "Poisson/Gauss measured source",
            "impact": "nonzero I_commutator means d(Pi_M J_H) is not closed in the compact exterior",
            "current_status": "BLOCKED_BY_I_COMMUTATOR",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1772_2_wrong_object",
            "bridge_piece": "topological conserved charge",
            "impact": "closed J_M_top is insufficient unless equal to Pi_M J_H plus silent boundary",
            "current_status": "BLOCKED_BY_R_EQ",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1772_3_local_GR",
            "bridge_piece": "local GR/Newton claim",
            "impact": "all local gates remain false until commutator/stress/equality rows close",
            "current_status": "NOT_CLAIMABLE",
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1772_0_closed_wrong_charge",
            "countermodel": "a closed topological current is conserved but not equal to the observed Hilbert source",
            "mathematical_form": "dJ_M_top=0 but Pi_M J_H - J_M_top - dB_zero != 0",
            "survives_current_constraints": True,
            "why_survives": "R_eq equality is not parent-derived",
            "what_kills_it": "topological-Hilbert equality theorem or source-backed R_eq bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1772_1_metric_projector_stress",
            "countermodel": "Hodge/domain projector has nonzero metric variation stress",
            "mathematical_form": "delta_g Pi_H(g) -> T_PiM_munu != 0",
            "survives_current_constraints": True,
            "why_survives": "Hodge route is retained if used and projector stress map is missing",
            "what_kills_it": "topological no-stress route or T_PiM bound below local locks",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1772_2_post_readout_mask",
            "countermodel": "Pi_M is chosen after orbit/readout",
            "mathematical_form": "Pi_M := Pi_M(GM_obs)",
            "survives_current_constraints": True,
            "why_survives": "can fit measured GM but has no derivation credit",
            "what_kills_it": "fixed-before-readout parent charge map",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1772_3_verdict",
            "countermodel": "Pi_M commutator/projector residual retained",
            "mathematical_form": "I_commutator, R_eq, B_zero, T_PiM retained",
            "survives_current_constraints": True,
            "why_survives": "1772 proves only conditional routes, not parent equality/silence",
            "what_kills_it": "1773 topological-Hilbert equality or R_eq/I_commutator bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1772_0_commutator_route",
            "decision": "TOPOLOGICAL_PIM_CAN_KILL_COMMUTATOR_ONLY_CONDITIONALLY",
            "reason": "metric-independent closed charge data gives [d,Pi_M]J=0, but only for the current it actually projects",
            "next_action": "prove equality to Pi_M J_H or keep R_eq/I_commutator rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1772_1_Hodge_route",
            "decision": "HODGE_DOMAIN_PROJECTOR_ROUTE_RETAINS_STRESS",
            "reason": "metric/domain dependence makes delta Pi_M a real weak-field/PPN/source residual",
            "next_action": "do not use Hodge Pi_M for local-GR unless T_PiM is zeroed or bounded",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1772_2_no_claim",
            "decision": "NEWTON_LOCAL_GR_GATES_REMAIN_BLOCKED",
            "reason": "commutator, Hilbert equality, boundary flux, and projector stress rows remain unfilled",
            "next_action": "keep all claim gates false",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1772_3_best_next",
            "decision": "TOPOLOGICAL_HILBERT_EQUALITY_OR_R_EQ_BOUND_IS_NEXT",
            "reason": "after conditional commutator zero, the remaining sharp blocker is whether the closed mass current is the Hilbert source current",
            "next_action": "build 1773 topological-Hilbert equality theorem or R_eq/I_commutator bound pack",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1772_0_commutator_zero",
            "claim": "[d,Pi_M]J_H=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_TOPOLOGICAL_HILBERT_EQUALITY_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1772_1_projector_stress_zero",
            "claim": "projector variation stress is zero",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_TOPOLOGICAL_NO_STRESS_OR_TPIM_BOUND_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1772_2_wrong_object",
            "claim": "topological current equals observed Hilbert projected source",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_R_EQ_INTEGRAL_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1772_3_coefficient_bounds",
            "claim": "Pi_M commutator/projector coefficients are source-backed",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_I_COMMUTATOR_TPIM_BZERO_BOUNDS_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1772_4_Newton_local_GR",
            "claim": "Newton/local-GR gates can reopen",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PIM_COMMUTATOR_PROJECTOR_RESIDUALS_RETAINED",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1772_0_primary",
            "next_target": "1773-Y5-R2FR-topological-Hilbert-equality-or-R-eq-bound.md",
            "script": "scripts/Y5_R2FR_topological_Hilbert_equality_or_R_eq_bound.py",
            "objective": "derive Pi_M J_H = J_M_top + dB_zero from the same compact-source worldtube, or fill R_eq/I_commutator/B_zero source-backed bound rows",
            "selection_status": "selected",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1772_1_fallback",
            "next_target": "1773b-Y5-R2FR-projector-stress-PPN-bound-pack.md",
            "script": "scripts/Y5_R2FR_projector_stress_PPN_bound_pack.py",
            "objective": "map T_PiM/projector_stress_beta_equiv into PPN/R10/orbital bound rows if topological route fails",
            "selection_status": "held_fallback",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "commutator_attempt": commutator_attempt_rows(),
        "route_audit": route_audit_rows(),
        "projector_stress": projector_stress_rows(),
        "coefficient_pack": coefficient_pack_rows(),
        "impact": impact_rows(),
        "countermodel": countermodel_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv_ok(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1772_SOURCE_REGISTER.csv")
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1772_{key.upper()}.csv")


def claim_like_field(key: str) -> bool:
    return key.lower() in {
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "prediction_allowed",
        "score_allowed",
        "claim_pass",
        "selected",
    }


def boolish_claim_true(key: str, value: Any) -> bool:
    if key.lower() == "selected":
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if claim_like_field(key) and boolish_claim_true(key, value):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    status_keys = {"current_status", "status", "remaining_gap"}
    for rows in rows_map.values():
        for row in rows:
            combined_status = " ".join(str(row.get(key, "")) for key in status_keys)
            if "MISSING_" in combined_status:
                for key, value in row.items():
                    if claim_like_field(key) and boolish_claim_true(key, value):
                        return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1772_SOURCE_REGISTER.csv").exists():
        return False
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1772_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched_for_1772() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1772*"))


def csv_parse_all() -> bool:
    return all(parse_csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def commutator_conditional_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "PCZ1772_1_topological_zero"
        and row["status"] == "CONDITIONAL_THEOREM_CLEAN"
        and row["valid_for_claim"] is False
        for row in rows_map["commutator_attempt"]
    )


def not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "PCZ1772_4_current_verdict"
        and row["status"] == "FAIL_CURRENT_PARENT_PROOF"
        and row["claim_allowed"] is False
        for row in rows_map["commutator_attempt"]
    )


def route_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["route_id"] == "PRA1772_4_verdict"
        and row["current_status"] == "NOT_PARENT_SIGNED"
        for row in rows_map["route_audit"]
    )


def stress_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["stress_id"] == "PSA1772_4_verdict"
        and row["status"] == "NOT_DERIVED_RETAIN_BOUND_ROWS"
        for row in rows_map["projector_stress"]
    )


def coefficient_pack_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["coefficient_pack"]
    return any(row["row_id"] == "PCB1772_1_I_commutator" for row in rows) and all(
        row["valid_for_claim"] is False for row in rows
    )


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["countermodel_id"] == "CM1772_3_verdict"
        and row["survives_current_constraints"] is True
        and row["valid_for_claim"] is False
        for row in rows_map["countermodel"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["route_id"] == "NEXT1772_0_primary" and row["selection_status"] == "selected"
        for row in rows_map["next_target"]
    )


def check_row(check_id: str, condition: bool, pass_detail: str, fail_detail: str) -> dict[str, str]:
    return {
        "branch_id": BRANCH_ID,
        "check_id": check_id,
        "result": "PASS" if condition else "FAIL",
        "detail": pass_detail if condition else fail_detail,
    }


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    sources = rows_map["source_register"]
    claim_gates = rows_map["claim_gate"]
    checks = [
        check_row("VAL1772_0_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check_row("VAL1772_1_needles_present", all(row["needles_present"] for row in sources), "required source needles are present", "one or more source needles missing"),
        check_row("VAL1772_2_conditional_commutator", commutator_conditional_recorded(rows_map), "conditional topological commutator theorem recorded", "conditional commutator theorem missing"),
        check_row("VAL1772_3_not_promoted", not_promoted(rows_map), "current commutator zero remains unpromoted", "commutator zero was promoted"),
        check_row("VAL1772_4_route_retained", route_retained(rows_map), "route verdict remains parent-unsigned", "route verdict missing or promoted"),
        check_row("VAL1772_5_stress_retained", stress_retained(rows_map), "projector stress remains retained", "projector stress missing or promoted"),
        check_row("VAL1772_6_coefficient_pack_nonclaim", coefficient_pack_nonclaim(rows_map), "Pi_M coefficient rows remain nonclaim", "coefficient pack missing or promoted"),
        check_row("VAL1772_7_countermodel_retained", countermodel_retained(rows_map), "Pi_M countermodel remains retained", "countermodel missing or promoted"),
        check_row(
            "VAL1772_8_claim_gates_safe",
            all(row["gate_pass"] is False and row["status"] == "BLOCKED" for row in claim_gates),
            "all claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check_row("VAL1772_9_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL1772_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row(
            "VAL1772_11_decision_next",
            any(row["decision_id"] == "DEC1772_3_best_next" and row["decision"] == "TOPOLOGICAL_HILBERT_EQUALITY_OR_R_EQ_BOUND_IS_NEXT" for row in rows_map["decision"]),
            "decision selects topological-Hilbert equality/R_eq route",
            "best-next decision missing",
        ),
        check_row("VAL1772_12_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL1772_13_csv_parse", csv_parse_all(), "all generated 1772 CSVs parse", "one or more generated 1772 CSVs fail to parse"),
        check_row("VAL1772_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "branch copies missing"),
        check_row("VAL1772_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check_row("VAL1772_16_formalization_untouched", formalization_untouched_for_1772(), "no 1772 outputs found under formalization-workbench", "1772 outputs found under formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in checks)
    checks.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1772_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1772 Pi_M commutator/projector variation zero or coefficient bound",
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    sections = [
        "# 1772 - Pi_M Commutator Projector Variation Zero Or Coefficient Bound",
        "",
        "## Verdict",
        "- 1772 proves the useful conditional theorem: a fixed, metric-independent topological `Pi_M` kills `[d,Pi_M]J` and avoids projector stress.",
        "- That does not yet prove the MTS source branch. The closed topological current must still be the same object as the observed Hilbert projected source: `Pi_M J_H = J_M_top + dB_zero`.",
        "- If the route is Hodge/DeWitt/domain-dependent instead, projector stress is retained and must be mapped into PPN/source-normalization bounds.",
        "- Therefore `[d,Pi_M]J_H=0`, `T_PiM=0`, measured-GM closure, Newton, and local-GR remain nonclaim.",
        "- The next sharp target is topological-Hilbert equality or an `R_eq/I_commutator/B_zero` bound pack.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Pi_M Commutator Zero Attempt",
        markdown_table(rows_map["commutator_attempt"], ["attempt_id", "claim_piece", "mathematical_form", "status", "proof_result", "remaining_gap"]),
        "",
        "## Pi_M Route Audit",
        markdown_table(rows_map["route_audit"], ["route_id", "route", "condition", "current_status", "risk", "required_next"]),
        "",
        "## Projector Stress Audit",
        markdown_table(rows_map["projector_stress"], ["stress_id", "quantity", "mathematical_form", "status", "impact"]),
        "",
        "## Pi_M Coefficient Bound Pack",
        markdown_table(rows_map["coefficient_pack"], ["row_id", "quantity", "definition", "units", "status", "maps_to"]),
        "",
        "## GR Newton Impact Ledger",
        markdown_table(rows_map["impact"], ["impact_id", "bridge_piece", "impact", "current_status"]),
        "",
        "## Countermodel Ledger",
        markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "mathematical_form", "survives_current_constraints", "why_survives", "what_kills_it"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "This checkpoint narrows the obstruction again. The commutator can be killed cleanly by a fixed topological projector, but that victory is hollow unless the topological charge equals the Hilbert source current that actually appears in the field equation. So the next fight is not abstract projector algebra; it is equality of conserved objects.",
        "",
    ]
    return "\n".join(sections)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1772-Y5-R2FR-PiM-commutator-projector-variation-zero-or-coefficient-bound.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1772 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()

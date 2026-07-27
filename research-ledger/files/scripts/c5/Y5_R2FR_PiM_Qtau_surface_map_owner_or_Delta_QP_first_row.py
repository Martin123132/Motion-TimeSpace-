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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1776"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1776_0_1775_handoff",
        "source_key": "1775_handoff",
        "source_path": ROOT / "1775-Y5-R2FR-Qtau-period-map-current-descent-or-Delta-period-source-pack.md",
        "needles": ["NEXT1775_0_primary", "QPM1775_3_PiM_surface_map", "DPS1775_0_Delta_QP_surface_map"],
    },
    {
        "source_id": "SRC1776_1_1775_validation",
        "source_key": "1775_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1775_VALIDATION.csv",
        "needles": ["VAL1775_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1776_2_1775_map_theorem",
        "source_key": "1775_map_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1775_QTAU_PERIOD_MAP_THEOREM.csv",
        "needles": ["QPM1775_3_PiM_surface_map", "QPM1775_5_verdict"],
    },
    {
        "source_id": "SRC1776_3_1775_source_pack",
        "source_key": "1775_source_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1775_DELTA_PERIOD_SOURCE_PACK.csv",
        "needles": ["DPS1775_0_Delta_QP_surface_map", "DPS1775_6_epsilon_QP_period_abs"],
    },
    {
        "source_id": "SRC1776_4_539_hamiltonian_pim",
        "source_key": "539_hamiltonian_pim",
        "source_path": ROOT / "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
        "needles": ["PH539_2_DAT537_4_repair_scope", "HG539_3_old_PiM_equivalence", "D539_0_Hamiltonian_PiM_candidate"],
    },
    {
        "source_id": "SRC1776_5_1769_gr_newton",
        "source_key": "1769_gr_newton_bridge",
        "source_path": ROOT / "1769-Y5-R2FR-GR-left-hand-Einstein-Newton-limit-or-operator-residual-pack.md",
        "needles": ["NWF1769_1_poisson_conditional", "ORP1769_5_source_normalization", "GATE1769_3_newton_orbit"],
    },
    {
        "source_id": "SRC1776_6_1771_operator_bounds",
        "source_key": "1771_operator_bounds",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1771_OPERATOR_BOUND_INPUT_PACK.csv",
        "needles": ["OBI1771_2_projector", "OBI1771_6_source_normalization"],
    },
    {
        "source_id": "SRC1776_7_hwt_attempt",
        "source_key": "hilbert_worldtube_attempt",
        "source_path": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
        "needles": ["HWT536_3_Hilbert_to_PiM_charge_map", "HWT536_5_exact_and_reference_terms_zero"],
    },
    {
        "source_id": "SRC1776_8_1733_current_owner",
        "source_key": "1733_current_owner",
        "source_path": ROOT / "1733-Y5-R2FR-parent-theta-Qtau-current-owner-or-Htau-first-row.md",
        "needles": ["COA1733_7_owner_verdict", "TQC1733_2_projector_PiM", "CG1733_0_current_owner"],
    },
    {
        "source_id": "SRC1776_9_1772_PiM",
        "source_key": "1772_PiM_equality",
        "source_path": ROOT / "1772-Y5-R2FR-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
        "needles": ["PCZ1772_2_hilbert_equality_blocker", "PCB1772_0_R_eq_integral"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1776_SOURCE_REGISTER.csv",
    "surface_map": RESIDUALS / "P8_Y5_PARENT_QLOC_1776_PIM_QTAU_SURFACE_MAP_ATTEMPT.csv",
    "gauss_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1776_GAUSS_CONSTRAINT_AUDIT.csv",
    "delta_qp_schema": RESIDUALS / "P8_Y5_PARENT_QLOC_1776_DELTA_QP_FIRST_ROW_SCHEMA.csv",
    "repair_routes": RESIDUALS / "P8_Y5_PARENT_QLOC_1776_REPAIR_ROUTE_LEDGER.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1776_COUNTERMODEL_LEDGER.csv",
    "impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1776_GR_NEWTON_IMPACT_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1776_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1776_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1776_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1776_VALIDATION.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(needles),
                "needles_present": exists and all(needle in text for needle in needles),
                "role": "1776 PiM/Q_tau surface-map owner or Delta_QP first-row evidence",
            }
        )
    return rows


def surface_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SMT1776_0_target",
            "claim_piece": "Pi_M/Q_tau surface map",
            "mathematical_form": "(4*pi*G_ref)^-1 integral_L Pi_M J_H = H_tau[S]-H_ref",
            "status": "TARGET_EXACT",
            "derivation_result": "this is the noncircular mass-source bridge needed by 1775",
            "remaining_gap": "must be derived from parent constraint/current map, not definition after readout",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SMT1776_1_GR_reference",
            "claim_piece": "EH/GR Gauss-law reference pattern",
            "mathematical_form": "Hamiltonian constraint + boundary Noether charge links surface mass to Hilbert source in GR",
            "status": "REFERENCE_TEMPLATE_ONLY",
            "derivation_result": "shows the route is mathematically natural",
            "remaining_gap": "MTS cannot import EH Gauss law until EH dominance and residual silence are parent-signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SMT1776_2_Hamiltonian_PiM_branch",
            "claim_piece": "define Pi_M^H from parent Hamiltonian charge",
            "mathematical_form": "Pi_M^H J_H := 4*pi*G_ref (H_tau[S]-H_ref) omega_M^H with integral_L omega_M^H=1",
            "status": "CANDIDATE_REPAIR_NOT_ADOPTED",
            "derivation_result": "removes wrong-conserved-object risk at charge level if adopted before readout",
            "remaining_gap": "integrability, source-measure glue, old-PiM equivalence, and PPN readout remain open",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SMT1776_3_old_PiM_equivalence",
            "claim_piece": "old/topological Pi_M equals Hamiltonian Pi_M^H",
            "mathematical_form": "Pi_M^top J_H = Pi_M^H J_H + dB_zero + R_PiH",
            "status": "KEY_BLOCKER_NOT_DERIVED",
            "derivation_result": "without this, old Pi_M remains a closure/topological branch only",
            "remaining_gap": "R_PiH/Delta_QP and B_zero_flux are not zeroed or bounded",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SMT1776_4_parent_constraint_map",
            "claim_piece": "parent constraint maps Hilbert source to surface charge",
            "mathematical_form": "C_tau^MTS = C_tau^EH[T_H] + C_tau^res and integral_W C_tau = integral_S Q_tau",
            "status": "NOT_PARENT_SIGNED",
            "derivation_result": "would make the source-side Gauss bridge a theorem",
            "remaining_gap": "Theta/Q_tau owner, EH dominance, residual silence, and source normalization remain missing",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SMT1776_5_current_verdict",
            "claim_piece": "current MTS derives Pi_M/Q_tau surface map",
            "mathematical_form": "SMT1776_1 through SMT1776_4 close with no circular denominator",
            "status": "FAIL_CURRENT_PARENT_PROOF",
            "derivation_result": "Delta_QP first-row path remains active",
            "remaining_gap": "Pi_M^H adoption/equivalence, parent constraint map, H_tau integrability, and boundary/source rows",
            "valid_for_claim": False,
        },
    ]


def gauss_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "GCA1776_0_parent_constraint",
            "clause": "parent Hamiltonian/Gauss constraint exists",
            "required_identity": "variation along tau gives a first-class constraint whose integral equals a surface charge",
            "current_status": "MISSING_PARENT_CONSTRAINT_MAP",
            "if_missing": "Delta_constraint_Gauss",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "GCA1776_1_EH_dominance",
            "clause": "local EH dominance is signed",
            "required_identity": "E_LHS=G+Lambda g plus zero/bounded residuals in the local branch",
            "current_status": "EH_REFERENCE_ONLY",
            "if_missing": "DeltaE_munu / operator coefficient vector",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "GCA1776_2_source_measure",
            "clause": "same Hilbert source measure enters the constraint",
            "required_identity": "T_H/J_H in the constraint is the observed source-frame matter current",
            "current_status": "MISSING_SOURCE_MEASURE_GLUE",
            "if_missing": "Delta_source_measure",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "GCA1776_3_PiM_owner",
            "clause": "Pi_M is the Hamiltonian source projector or equivalent to it",
            "required_identity": "Pi_M^top = Pi_M^H plus exact zero-flux/residual-bounded terms",
            "current_status": "MISSING_PIM_H_EQUIVALENCE",
            "if_missing": "R_PiH / Delta_QP",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "GCA1776_4_boundary_reference",
            "clause": "boundary/reference terms do not shift the charge",
            "required_identity": "B_zero_flux=Delta_symp=H_ref_shift=0 or source-backed finite rows",
            "current_status": "MISSING_BOUNDARY_REFERENCE_INPUT",
            "if_missing": "B_zero_flux;Delta_symp;H_ref_shift",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "GCA1776_5_no_orbital_backfill",
            "clause": "measured orbital GM is not used as denominator input",
            "required_identity": "H_tau-H_ref is derived/source-backed before orbital fit or local acceleration readout",
            "current_status": "GUARDRAIL_ACTIVE_SOURCE_ROW_MISSING",
            "if_missing": "M_H_ref remains unavailable",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "GCA1776_6_verdict",
            "clause": "surface-map Gauss bridge accepted",
            "required_identity": "GCA1776_0 through GCA1776_5 all pass",
            "current_status": "NOT_PARENT_SIGNED",
            "if_missing": "epsilon_surface_map_abs",
            "valid_for_claim": False,
        },
    ]


def delta_qp_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQP1776_0_Delta_QP",
            "quantity": "Delta_QP_surface_map",
            "definition": "(4*pi*G_ref)^-1 integral_L Pi_M J_H - (H_tau[S]-H_ref)",
            "required_fields": "system_id;surface_id;linked_cycle_id;PiM_definition;PiM_JH_period;H_tau;H_ref;G_ref;M_H_ref;units;source_path;equation_ref",
            "status": "MISSING_QTAU_PERIOD_MAP",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQP1776_1_R_PiH",
            "quantity": "R_PiH_equivalence",
            "definition": "old/topological Pi_M current minus Hamiltonian Pi_M^H current after exact improvement",
            "required_fields": "PiM_top_definition;PiM_H_definition;B_zero;linked_periods;M_H_ref;source_path",
            "status": "MISSING_PIM_H_EQUIVALENCE",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQP1776_2_Delta_constraint_Gauss",
            "quantity": "Delta_constraint_Gauss",
            "definition": "parent constraint/Gauss-law residual between volume Hilbert source and surface Q_tau",
            "required_fields": "constraint_density;volume_source;surface_Qtau;boundary_terms;units;source_path",
            "status": "MISSING_PARENT_CONSTRAINT_MAP",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQP1776_3_DeltaE_source",
            "quantity": "DeltaE_source_projection",
            "definition": "EH-dominance/source-side residual that shifts the Hamiltonian source map",
            "required_fields": "DeltaE_00;source_projection;operator_coefficients;local_scale;units;source_path",
            "status": "MISSING_EH_DOMINANCE_OR_OPERATOR_BOUND",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQP1776_4_boundary_reference",
            "quantity": "B_zero_flux;Delta_symp;H_ref_shift",
            "definition": "charge offset from boundary, symplectic, or reference terms",
            "required_fields": "surface_pair;boundary_rule;B_zero_flux;Delta_symp;H_ref_shift;M_H_ref;units;source_path",
            "status": "MISSING_BOUNDARY_REFERENCE_INPUT",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQP1776_5_epsilon_surface_map_abs",
            "quantity": "epsilon_surface_map_abs",
            "definition": "absolute no-cancellation envelope of Delta_QP, R_PiH, Gauss residual, EH/source residual, and boundary/reference residuals",
            "required_fields": "component_abs_sum;M_H_ref;common_units;component_source_paths;no_cancellation_guard",
            "status": "MISSING_COMPONENT_INPUTS",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def repair_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "RPR1776_0_adopt_Hamiltonian_PiM",
            "route": "adopt Pi_M^H as the parent-defined Hamiltonian source projector",
            "benefit": "removes the wrong-conserved-object risk at charge level",
            "current_status": "CANDIDATE_ONLY",
            "remaining_debt": "integrability, source-measure glue, old-PiM demotion/equivalence, PPN readout",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RPR1776_1_old_PiM_equivalence",
            "route": "prove old/topological Pi_M equals Pi_M^H",
            "benefit": "keeps older topological route as a representation of the Hamiltonian charge",
            "current_status": "NOT_DERIVED",
            "remaining_debt": "R_PiH and B_zero_flux zero/bound",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RPR1776_2_bound_Delta_QP",
            "route": "do not prove equality; bound Delta_QP as a local residual",
            "benefit": "makes failure empirical and testable",
            "current_status": "SOURCE_SCHEMA_ONLY",
            "remaining_debt": "numeric/theorem-zero rows and M_H_ref denominator",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RPR1776_3_demote_old_PiM",
            "route": "demote old/topological Pi_M to closure-only until equivalent to Pi_M^H",
            "benefit": "prevents two mass channels from being used interchangeably",
            "current_status": "RECOMMENDED_GUARDRAIL",
            "remaining_debt": "write adoption/demotion contract in the next checkpoint",
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1776_0_two_mass_channels",
            "countermodel": "old Pi_M period and Hamiltonian H_tau charge are different but both called mass",
            "survives_current_constraints": True,
            "why_survives": "Pi_M^top = Pi_M^H is not derived",
            "what_kills_it": "Hamiltonian PiM adoption plus old-PiM equivalence or demotion",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1776_1_EH_Gauss_import",
            "countermodel": "EH Gauss law is imported as MTS source map",
            "survives_current_constraints": True,
            "why_survives": "EH dominance/residual silence is not signed",
            "what_kills_it": "parent constraint map plus operator residual bounds",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1776_2_boundary_charge_shift",
            "countermodel": "surface equality is shifted by boundary/reference terms",
            "survives_current_constraints": True,
            "why_survives": "B_zero/Delta_symp/H_ref rows are missing",
            "what_kills_it": "boundary/reference zero theorem or finite source-backed row",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1776_3_orbital_calibration_loop",
            "countermodel": "Pi_M/Q_tau equality is normalized using measured orbital GM",
            "survives_current_constraints": True,
            "why_survives": "M_H_ref remains unavailable",
            "what_kills_it": "noncircular H_tau-H_ref source row",
        },
    ]


def impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "IMP1776_0_GR_source",
            "bridge_piece": "GR source side",
            "impact": "source charge cannot be used in Einstein/Newton bridge until Pi_M source period equals Hamiltonian charge",
            "current_status": "BLOCKED_BY_SURFACE_MAP",
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "IMP1776_1_Newton",
            "bridge_piece": "Newtonian GM",
            "impact": "inverse-square mass remains nonderived if Delta_QP is nonzero or unknown",
            "current_status": "BLOCKED_NO_GM_BACKFILL",
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "IMP1776_2_PPN_R10",
            "bridge_piece": "PPN/R10 local residuals",
            "impact": "Delta_QP, R_PiH, and constraint residuals become upstream local-test coefficients",
            "current_status": "NONCLAIM_SOURCE_ROWS_STAGED",
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "IMP1776_3_framework",
            "bridge_piece": "theory architecture",
            "impact": "cleanest route is to make Pi_M a Hamiltonian charge representative, not an independent topological selector",
            "current_status": "CANDIDATE_NOT_ADOPTED",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1776_0_surface_map_status",
            "decision": "PIM_QTAU_SURFACE_MAP_NOT_DERIVED",
            "reason": "old Pi_M, Hamiltonian Pi_M^H, and parent Gauss constraint are not yet the same object",
            "next_action": "keep Delta_QP nonclaim and do not reopen Newton/local-GR",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1776_1_best_repair",
            "decision": "HAMILTONIAN_PIM_BRANCH_IS_LOWEST_SCRUTINY_ROUTE",
            "reason": "GR-like mass is naturally a Hamiltonian/Noether charge, while independent topological Pi_M risks wrong-object conservation",
            "next_action": "try a formal adoption/demotion contract next",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1776_2_residual_path",
            "decision": "DELTA_QP_FIRST_ROW_IS_THE_FALLBACK",
            "reason": "if the map cannot be derived, the mismatch must be explicitly bounded rather than hidden",
            "next_action": "carry Delta_QP/R_PiH/Gauss residual schemas forward",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1776_3_best_next",
            "decision": "HAMILTONIAN_PIM_ADOPTION_CONTRACT_OR_RPIH_BOUND_IS_NEXT",
            "reason": "we must either define Pi_M by the parent Hamiltonian charge and demote old Pi_M, or prove/bound their difference",
            "next_action": "build 1777 Hamiltonian-PiM adoption/equivalence contract",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1776_0_surface_map",
            "claim": "Pi_M/Q_tau surface map is derived",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "MISSING_HAMILTONIAN_PIM_ADOPTION_OR_EQUIVALENCE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1776_1_Delta_QP_score",
            "claim": "Delta_QP row can be scored",
            "gate_pass": False,
            "status": "REFUSED",
            "blocker": "MISSING_NUMERIC_OR_THEOREM_ZERO_INPUTS_AND_MHREF",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1776_2_Newton_GR",
            "claim": "Newton/local-GR bridge can reopen",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "SURFACE_MAP_AND_EH_GAUSS_COUNTERMODELS_RETAINED",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1776_0_primary",
            "next_target": "1777-Y5-R2FR-Hamiltonian-PiM-adoption-contract-or-RPiH-bound.md",
            "script": "scripts/Y5_R2FR_Hamiltonian_PiM_adoption_contract_or_RPiH_bound.py",
            "objective": "attempt to adopt Pi_M^H as the parent charge-map representative and demote old Pi_M unless Pi_M^top=Pi_M^H+dB+R_PiH is proved or bounded",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1776_1_parallel",
            "next_target": "1777b-Y5-R2FR-Delta-QP-first-finite-source-row.md",
            "script": "scripts/Y5_R2FR_Delta_QP_first_finite_source_row.py",
            "objective": "create the first strict source row for Delta_QP_surface_map if adoption/equivalence does not close",
            "selection_status": "parallel_fallback",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "surface_map": surface_map_rows(),
        "gauss_audit": gauss_audit_rows(),
        "delta_qp_schema": delta_qp_schema_rows(),
        "repair_routes": repair_route_rows(),
        "countermodel": countermodel_rows(),
        "impact": impact_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1776_{key.upper()}.csv")


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def boolish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def sources_ok(rows_map: dict[str, list[dict[str, Any]]]) -> tuple[bool, bool]:
    rows = rows_map["source_register"]
    return all(boolish(row["exists"]) for row in rows), all(boolish(row["needles_present"]) for row in rows)


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            for flag in ("valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring"):
                if flag in row and boolish(row[flag]):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in text:
                if any(boolish(row.get(flag, False)) for flag in ("valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring")):
                    return False
    return True


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1776_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    return not any(FORMALIZATION.rglob("*1776*")) if FORMALIZATION.exists() else True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1776_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1776_1_needles_present", needles_ok, "required source needles are present"),
        (
            "VAL1776_2_surface_map_attempt",
            any(row["attempt_id"] == "SMT1776_0_target" and row["status"] == "TARGET_EXACT" for row in rows_map["surface_map"]),
            "surface map target is exact",
        ),
        (
            "VAL1776_3_current_map_not_promoted",
            any(row["attempt_id"] == "SMT1776_5_current_verdict" and row["status"] == "FAIL_CURRENT_PARENT_PROOF" for row in rows_map["surface_map"]),
            "current surface map remains unpromoted",
        ),
        (
            "VAL1776_4_gauss_audit_blocks",
            any(row["audit_id"] == "GCA1776_6_verdict" and row["current_status"] == "NOT_PARENT_SIGNED" for row in rows_map["gauss_audit"]),
            "Gauss/source-map audit blocks promotion",
        ),
        (
            "VAL1776_5_delta_qp_schema_nonclaim",
            all(not boolish(row["valid_for_claim"]) and not boolish(row["score_ready"]) for row in rows_map["delta_qp_schema"]),
            "Delta_QP schema rows remain nonclaim",
        ),
        (
            "VAL1776_6_repair_routes_nonclaim",
            all(not boolish(row["valid_for_claim"]) for row in rows_map["repair_routes"]),
            "repair routes remain candidate/nonclaim",
        ),
        (
            "VAL1776_7_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel"]),
            "surface-map countermodels remain live",
        ),
        (
            "VAL1776_8_claim_gates_blocked",
            all(not boolish(row["valid_for_claim"]) and row["status"] in {"BLOCKED", "REFUSED"} for row in rows_map["claim_gate"]),
            "claim gates are blocked or refused",
        ),
        ("VAL1776_9_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1776_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1776_11_decision_next",
            any(row["decision_id"] == "DEC1776_3_best_next" and "HAMILTONIAN_PIM_ADOPTION" in row["decision"] for row in rows_map["decision"]),
            "decision selects Hamiltonian-PiM adoption/equivalence next",
        ),
        (
            "VAL1776_12_next_selected",
            any(row["route_id"] == "NEXT1776_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1776_13_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1776 CSVs parse"),
        ("VAL1776_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1776_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1776_16_formalization_untouched", formalization_untouched(), "no 1776 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1776_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1776 PiM/Q_tau surface map owner or Delta_QP first row checkpoint",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# 1776 - Y5/R2FR PiM Q_tau Surface Map Owner or Delta_QP First Row",
            "",
            "## Verdict",
            "",
            "The surface-map proof does not close for current MTS. The cleanest route is now explicit: define/adopt `Pi_M^H` as the parent Hamiltonian charge representative, then either prove the old/topological `Pi_M` equals `Pi_M^H` up to exact zero-flux terms, or demote old `Pi_M` to a closure-only/residual branch. Until that is done, `Delta_QP` remains the honest source-normalization residual.",
            "",
            "**Claim ceiling:** no `Pi_M/Q_tau` surface map, legal `M_H_ref`, source-normalized Newton limit, GR reduction, R10/R11 pass, PPN pass, clock/orbital pass, or local-GR claim is allowed from 1776.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Surface Map Attempt",
            markdown_table(rows_map["surface_map"], ["attempt_id", "claim_piece", "mathematical_form", "status", "derivation_result", "remaining_gap", "valid_for_claim"]),
            "",
            "## Gauss Constraint Audit",
            markdown_table(rows_map["gauss_audit"], ["audit_id", "clause", "required_identity", "current_status", "if_missing", "valid_for_claim"]),
            "",
            "## Delta_QP First Row Schema",
            markdown_table(rows_map["delta_qp_schema"], ["row_id", "quantity", "definition", "required_fields", "status", "score_ready", "claim_allowed", "valid_for_claim"]),
            "",
            "## Repair Route Ledger",
            markdown_table(rows_map["repair_routes"], ["route_id", "route", "benefit", "current_status", "remaining_debt", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
            "",
            "## GR/Newton Impact Ledger",
            markdown_table(rows_map["impact"], ["impact_id", "bridge_piece", "impact", "current_status"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker", "valid_for_claim"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This checkpoint is a useful fork. If MTS wants the low-scrutiny GR/Newton route, `Pi_M` should be a Hamiltonian charge representative, not a second independent mass selector. If that adoption/equivalence cannot be made parent-clean, the theory can still remain testable by carrying `Delta_QP` as an explicit residual.",
            "",
        ]
    )


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1776-Y5-R2FR-PiM-Q_tau-surface-map-owner-or-Delta-QP-first-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1776 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()

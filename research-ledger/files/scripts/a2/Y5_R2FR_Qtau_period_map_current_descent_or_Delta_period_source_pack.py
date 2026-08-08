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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1775"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1775_0_1774_handoff",
        "source_key": "1774_handoff",
        "source_path": ROOT / "1774-Y5-R2FR-period-charge-lock-or-MHref-first-row.md",
        "needles": ["NEXT1774_0_primary", "PCT1774_5_verdict", "FR1774_1_Delta_period"],
    },
    {
        "source_id": "SRC1775_1_1774_validation",
        "source_key": "1774_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1774_VALIDATION.csv",
        "needles": ["VAL1774_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1775_2_1774_lock_theorem",
        "source_key": "1774_lock_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1774_PERIOD_CHARGE_LOCK_THEOREM.csv",
        "needles": ["PCT1774_0_statement", "PCT1774_1_current_descent", "PCT1774_5_verdict"],
    },
    {
        "source_id": "SRC1775_3_1774_first_rows",
        "source_key": "1774_first_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1774_PERIOD_MHREF_FIRST_ROWS.csv",
        "needles": ["FR1774_0_M_H_ref", "FR1774_1_Delta_period", "FR1774_2_deltaH_curl"],
    },
    {
        "source_id": "SRC1775_4_1733_current_owner",
        "source_key": "1733_current_owner",
        "source_path": ROOT / "1733-Y5-R2FR-parent-theta-Qtau-current-owner-or-Htau-first-row.md",
        "needles": ["COA1733_7_owner_verdict", "HFR1733_2_total_deltaH", "CG1733_3_MHref"],
    },
    {
        "source_id": "SRC1775_5_1734_projectability",
        "source_key": "1734_projectability",
        "source_path": ROOT / "1734-Y5-R2FR-current-descent-lemma-Dq-tau-projectability-or-theta-leak-row.md",
        "needles": ["DTP1734_6_verdict", "TLR1734_0_Dq_tau_commutator", "VAL1734_OVERALL"],
    },
    {
        "source_id": "SRC1775_6_1735_leak_pack",
        "source_key": "1735_leak_pack",
        "source_path": ROOT / "1735-Y5-R2FR-Dq-tau-theta-leak-source-pack-units-and-arena-projections.md",
        "needles": ["E_Dq_tau_commutator_norm", "epsilon_theta_Qtau_projectability_abs", "VAL1735_OVERALL"],
    },
    {
        "source_id": "SRC1775_7_1645_Htau",
        "source_key": "1645_Htau_integrability",
        "source_path": ROOT / "1645-Y5-R2FR-Htau-MHref-integrability-reference-lock-or-Mstar-source-row.md",
        "needles": ["H_tau exists on the branch iff d_field alpha_tau = 0", "CG1645_0_Htau_integrability"],
    },
    {
        "source_id": "SRC1775_8_1652_MHref",
        "source_key": "1652_MHref_guard",
        "source_path": ROOT / "1652-Y5-R2FR-MHref-denominator-first-row-and-source-measure-flux-contract.md",
        "needles": ["CG1652_0_MHref", "DEC1652_0_MHref", "NO_ORBITAL_GM_IMPORT"],
    },
    {
        "source_id": "SRC1775_9_worldtube_attempt",
        "source_key": "hilbert_worldtube_attempt",
        "source_path": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
        "needles": ["HWT536_3_Hilbert_to_PiM_charge_map", "HWT536_5_exact_and_reference_terms_zero"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1775_SOURCE_REGISTER.csv",
    "map_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1775_QTAU_PERIOD_MAP_THEOREM.csv",
    "descent_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1775_CURRENT_DESCENT_AUDIT.csv",
    "source_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1775_DELTA_PERIOD_SOURCE_PACK.csv",
    "runner": RESIDUALS / "P8_Y5_PARENT_QLOC_1775_LOCK_REFUSAL_RUNNER.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1775_COUNTERMODEL_LEDGER.csv",
    "impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1775_GR_NEWTON_IMPACT_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1775_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1775_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1775_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1775_VALIDATION.csv",
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
                "role": "1775 Q_tau-period map / Delta_period source-pack evidence",
            }
        )
    return rows


def map_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "QPM1775_0_contract",
            "claim": "parent Q_tau to Pi_M period map",
            "mathematical_form": "Delta_QP[S,L] := (4*pi*G_ref)^-1 integral_L Pi_M J_H - (H_tau[S]-H_ref); require Delta_QP=0 for the same linked source pair.",
            "status": "CONDITIONAL_MAP_CONTRACT",
            "would_close": "Pi_M linked period becomes the same Hamiltonian source charge used by M_H_ref",
            "current_blocker": "Q_tau^MTS owner, H_tau integrability, tau projectability, and Hilbert-to-PiM surface map are not signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "QPM1775_1_covariant_phase_space",
            "claim": "H_tau is generated by the parent covariant phase-space current",
            "mathematical_form": "delta H_tau = integral_S(delta Q_tau^MTS - i_tau Theta_total)",
            "status": "FORMAL_ROUTE_ONLY",
            "would_close": "H_tau can be integrated once the one-form is closed",
            "current_blocker": "Theta_total and Q_tau^MTS retained-sector pieces are not extracted",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "QPM1775_2_current_descent",
            "claim": "Q_tau descends through q to the observed reduced current",
            "mathematical_form": "q^*Q_tau^red = Q_tau^MTS + dC_tau + vertical/exact terms",
            "status": "NOT_PARENT_SIGNED",
            "would_close": "prevents importing EH current while hiding retained-sector charge",
            "current_blocker": "q/Dq map, tau projectability, vertical symplectic silence, and matter descent are missing",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "QPM1775_3_PiM_surface_map",
            "claim": "projected Hilbert current surface period equals Q_tau charge",
            "mathematical_form": "(4*pi*G_ref)^-1 integral_L Pi_M J_H = integral_S Q_tau^MTS - H_ref + boundary/exact terms",
            "status": "KEY_BLOCKER_NOT_DERIVED",
            "would_close": "turns topological/Hilbert source period into Hamiltonian mass",
            "current_blocker": "HWT536_3 remains not derived and projector current owner is missing",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "QPM1775_4_residual_identity",
            "claim": "Delta_period decomposes into explicit nonclaim residuals",
            "mathematical_form": "Delta_period/M_H_ref <= |Delta_QP| + |delta_H_tau_nonintegrable|/M_H_ref + |B_zero_flux|/M_H_ref + |E_Dq_tau| + |projector_current_leak| + |PD_norm_error|",
            "status": "RESIDUAL_IDENTITY_STAGED",
            "would_close": "failed proof becomes a measurable no-cancellation envelope",
            "current_blocker": "all numerator terms and M_H_ref are missing or unsigned",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "QPM1775_5_verdict",
            "claim": "current MTS proves Q_tau-period map",
            "mathematical_form": "QPM1775_1 through QPM1775_4 all pass in one parent action and linked source domain",
            "status": "FAIL_CURRENT_PARENT_PROOF",
            "would_close": "period-charge lock, M_H_ref denominator, and R_eq scoring could be re-audited",
            "current_blocker": "Delta_QP, H_tau curl, Dq/tau leak, boundary/reference, and M_H_ref rows remain missing",
            "valid_for_claim": False,
        },
    ]


def descent_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CDA1775_0_Qtau_owner",
            "clause": "Theta_total/Q_tau^MTS owner",
            "required_identity": "all retained-sector Theta_X, Q_X, projector, boundary and reference pieces are extracted from one parent variation",
            "current_status": "OWNER_NOT_SIGNED",
            "residual_if_missing": "Delta_Qtau_owner",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CDA1775_1_Dq_tau",
            "clause": "q/Dq/tau projectable current descent",
            "required_identity": "Dq(L_tau Phi)=L_tau_red q(Phi) and Dq([L_tau,v])=0 for vertical v",
            "current_status": "PROJECTABILITY_NOT_SIGNED",
            "residual_if_missing": "E_Dq_tau_commutator_norm",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CDA1775_2_Htau_integrability",
            "clause": "Hamiltonian one-form is integrable",
            "required_identity": "d_field alpha_tau=0 with alpha_tau=integral_S(delta Q_tau^MTS-i_tau Theta_total)-delta H_ref",
            "current_status": "MISSING_HTAU_CURL_COMPONENTS",
            "residual_if_missing": "delta_H_tau_nonintegrable_over_MH",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CDA1775_3_PiM_period",
            "clause": "Pi_M Hilbert source period equals the Hamiltonian charge period",
            "required_identity": "(4*pi*G_ref)^-1 integral_L Pi_M J_H = H_tau[S]-H_ref",
            "current_status": "MISSING_PIM_QTAU_SURFACE_MAP",
            "residual_if_missing": "Delta_QP_surface_map",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CDA1775_4_boundary_reference",
            "clause": "boundary, exact, and reference shifts are fixed",
            "required_identity": "B_zero_flux=0, Delta_symp=0, and H_ref is fixed once on the linked source class",
            "current_status": "MISSING_BOUNDARY_REFERENCE_INPUT",
            "residual_if_missing": "B_zero_flux;Delta_symp;H_ref_shift",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CDA1775_5_verdict",
            "clause": "Q_tau-period current descent accepted",
            "required_identity": "CDA1775_0 through CDA1775_4 all pass without circular source normalization",
            "current_status": "NOT_PARENT_SIGNED",
            "residual_if_missing": "epsilon_QP_period_abs",
            "valid_for_claim": False,
        },
    ]


def source_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DPS1775_0_Delta_QP_surface_map",
            "quantity": "Delta_QP_surface_map",
            "definition": "(4*pi*G_ref)^-1 integral_L Pi_M J_H - (H_tau[S]-H_ref)",
            "required_fields": "system_id;linked_cycle_id;surface_id;PiM_JH_period;H_tau;H_ref;G_ref;M_H_ref;units;source_path;equation_ref",
            "status": "MISSING_QTAU_PERIOD_MAP",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DPS1775_1_Delta_period",
            "quantity": "Delta_period",
            "definition": "max linked-surface mismatch integral_L(Pi_M J_H - J_M_top)",
            "required_fields": "system_id;linked_cycle_basis;PiM_JH_periods;JM_top_periods;PD_normalization;M_H_ref;source_path",
            "status": "MISSING_PERIOD_MISMATCH_BOUND",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DPS1775_2_Htau_curl",
            "quantity": "delta_H_tau_nonintegrable_over_MH",
            "definition": "field-space curl obstruction of alpha_tau normalized by M_H_ref",
            "required_fields": "I_EH;I_X;I_projector;I_boundary;I_ref;I_tau;I_surface;I_Dq;M_H_ref;units;source_paths",
            "status": "MISSING_HTAU_CURL_COMPONENTS",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DPS1775_3_E_Dq_tau",
            "quantity": "E_Dq_tau_commutator_norm",
            "definition": "Dq/tau projectability commutator norm",
            "required_fields": "q_map;Dq;vertical_basis;L_tau_on_parent;L_tau_red;norm;local_time_scale;source_path",
            "status": "MISSING_DQ_TAU_COMMUTATOR",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DPS1775_4_M_H_ref",
            "quantity": "M_H_ref",
            "definition": "positive same-frame H_tau[S_outer]-H_ref denominator",
            "required_fields": "system_id;e_obs_id;tau_id;S_outer;H_tau;H_ref;Q_tau_source;Theta_source;units;source_path;no_orbital_GM_import",
            "status": "MISSING_M_H_REF",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DPS1775_5_boundary_reference",
            "quantity": "B_zero_flux;Delta_symp;H_ref_shift",
            "definition": "boundary/reference/symplectic offset in Q_tau-to-period equality",
            "required_fields": "surface_pair;boundary_rule;B_zero_flux;Delta_symp;H_ref_shift;M_H_ref;units;source_path",
            "status": "MISSING_BOUNDARY_REFERENCE_INPUT",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DPS1775_6_epsilon_QP_period_abs",
            "quantity": "epsilon_QP_period_abs",
            "definition": "absolute no-cancellation envelope of Delta_QP, Delta_period, H_tau curl, Dq/tau leak, and boundary/reference residuals",
            "required_fields": "component_abs_sum;M_H_ref;common_units;component_source_paths;no_cancellation_guard",
            "status": "MISSING_COMPONENT_INPUTS",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def runner_rows(source_pack: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for idx, row in enumerate(source_pack):
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "run_id": f"RUN1775_{idx}_{row['quantity']}",
                "input_row": row["row_id"],
                "runner_decision": "REFUSE_SCORING",
                "refusal_reasons": f"{row['status']};VALID_FOR_CLAIM_FALSE;MISSING_SOURCE_PATH_OR_THEOREM_ZERO;NO_ORBITAL_GM_IMPORT;NO_CANCELLATION_CREDIT",
                "accepted_for_scoring": False,
                "claim_allowed": False,
            }
        )
    return rows


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1775_0_Qtau_not_PiM",
            "countermodel": "Q_tau charge exists but does not equal the Pi_M Hilbert period",
            "survives_current_constraints": True,
            "why_survives": "Delta_QP_surface_map is not zeroed or bounded",
            "what_kills_it": "parent Q_tau-to-PiM surface map theorem or source-backed small Delta_QP",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1775_1_integrable_wrong_charge",
            "countermodel": "H_tau is integrable for a charge that is not the measured Hilbert source mass",
            "survives_current_constraints": True,
            "why_survives": "Hilbert-to-Q_tau/Pi_M map remains missing",
            "what_kills_it": "HWT536_3-style source equality with no hidden sector charge",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1775_2_projectability_leak",
            "countermodel": "tau flow does not preserve quotient vertical directions",
            "survives_current_constraints": True,
            "why_survives": "E_Dq_tau_commutator_norm remains unfilled",
            "what_kills_it": "Dq/tau commutator zero theorem or finite arena bound",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1775_3_boundary_shift",
            "countermodel": "Q_tau-to-period equality is shifted by B_zero, Delta_symp, or H_ref",
            "survives_current_constraints": True,
            "why_survives": "boundary/reference lock remains missing",
            "what_kills_it": "fixed reference plus boundary/symplectic zero or source-backed finite rows",
        },
    ]


def impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "IMP1775_0_source_mass",
            "bridge_piece": "measured source mass",
            "impact": "without Delta_QP control, the topological/Hilbert period may not be the Hamiltonian source charge",
            "current_status": "BLOCKED_BY_QTAU_PERIOD_MAP",
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "IMP1775_1_Newton",
            "bridge_piece": "Newton/Poisson coefficient",
            "impact": "the inverse-square coefficient still cannot be derived without using measured orbital GM as an input",
            "current_status": "BLOCKED_NO_CIRCULAR_DENOMINATOR",
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "IMP1775_2_GR",
            "bridge_piece": "GR charge reduction",
            "impact": "EH charge logic remains a reference pattern until MTS Q_tau and Pi_M period are mapped",
            "current_status": "REFERENCE_ONLY",
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "IMP1775_3_tests",
            "bridge_piece": "R10/PPN/WEP/clock/orbit",
            "impact": "Delta_QP and E_Dq_tau become common upstream residuals feeding local test rows",
            "current_status": "SOURCE_PACK_STAGED_NONCLAIM",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1775_0_map_contract",
            "decision": "QTAU_PERIOD_MAP_IS_THE_EXACT_BRIDGE",
            "reason": "period-charge lock reduces to the difference between Pi_M linked Hilbert period and H_tau-H_ref",
            "next_action": "attack Delta_QP rather than adding another mass definition",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1775_1_current_status",
            "decision": "CURRENT_MTS_MAP_NOT_SIGNED",
            "reason": "current owner, projectability, H_tau curl, boundary reference, and Pi_M surface map remain missing",
            "next_action": "keep Delta_QP and Delta_period source rows nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1775_2_source_pack",
            "decision": "DELTA_QP_SOURCE_PACK_IS_NOW_THE_FALLBACK",
            "reason": "failed proof components have units/source requirements and can be made empirical later",
            "next_action": "do not score until rows are numeric or theorem-zeroed with sources",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1775_3_best_next",
            "decision": "PIM_QTAU_SURFACE_MAP_OR_DELTA_QP_FIRST_ROW_IS_NEXT",
            "reason": "the tightest remaining theorem is the surface equality (4piG)^-1 int Pi_M J_H = H_tau-H_ref",
            "next_action": "build 1776 Pi_M/Q_tau surface-map owner or first finite Delta_QP row",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1775_0_Qtau_period_map",
            "claim": "Q_tau/H_tau maps to Pi_M linked period",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "MISSING_DELTA_QP_ZERO_OR_BOUND",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1775_1_MHref",
            "claim": "M_H_ref denominator is legal",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "MISSING_HTAU_INTEGRABILITY_AND_QTAU_OWNER",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1775_2_Delta_period_score",
            "claim": "Delta_period/R_eq rows can be scored",
            "gate_pass": False,
            "status": "REFUSED",
            "blocker": "MISSING_DELTA_QP_MHREF_BOUNDARY_SOURCE_INPUTS",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1775_3_Newton_local_GR",
            "claim": "Newton/local-GR bridge can reopen",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "QTAU_PERIOD_COUNTERMODELS_RETAINED",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1775_0_primary",
            "next_target": "1776-Y5-R2FR-PiM-Q_tau-surface-map-owner-or-Delta-QP-first-row.md",
            "script": "scripts/Y5_R2FR_PiM_Qtau_surface_map_owner_or_Delta_QP_first_row.py",
            "objective": "derive the surface equality between Pi_M Hilbert period and H_tau-H_ref, or stage the first finite nonclaim Delta_QP row with units and source paths",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1775_1_parallel",
            "next_target": "1776b-Y5-R2FR-Dq-tau-commutator-bound-row-reentry.md",
            "script": "scripts/Y5_R2FR_Dq_tau_commutator_bound_row_reentry.py",
            "objective": "re-enter the exact E_Dq_tau obstruction if the surface-map route stalls",
            "selection_status": "parallel_fallback",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    source_pack = source_pack_rows()
    return {
        "source_register": source_register_rows(),
        "map_theorem": map_theorem_rows(),
        "descent_audit": descent_audit_rows(),
        "source_pack": source_pack,
        "runner": runner_rows(source_pack),
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
        shutil.copy2(path, RAB_QUEUE / f"JR1775_{key.upper()}.csv")


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
        if not (RAB_QUEUE / f"JR1775_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    return not any(FORMALIZATION.rglob("*1775*")) if FORMALIZATION.exists() else True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1775_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1775_1_needles_present", needles_ok, "required source needles are present"),
        (
            "VAL1775_2_map_contract_recorded",
            any(row["theorem_id"] == "QPM1775_0_contract" and row["status"] == "CONDITIONAL_MAP_CONTRACT" for row in rows_map["map_theorem"]),
            "Q_tau-period map contract is recorded",
        ),
        (
            "VAL1775_3_current_map_not_promoted",
            any(row["theorem_id"] == "QPM1775_5_verdict" and row["status"] == "FAIL_CURRENT_PARENT_PROOF" for row in rows_map["map_theorem"]),
            "current Q_tau-period map remains unpromoted",
        ),
        (
            "VAL1775_4_descent_audit_blocks",
            any(row["audit_id"] == "CDA1775_5_verdict" and row["current_status"] == "NOT_PARENT_SIGNED" for row in rows_map["descent_audit"]),
            "current descent audit remains blocked",
        ),
        (
            "VAL1775_5_source_pack_nonclaim",
            all(not boolish(row["valid_for_claim"]) and not boolish(row["score_ready"]) for row in rows_map["source_pack"]),
            "Delta_QP/period source rows remain nonclaim",
        ),
        (
            "VAL1775_6_runner_refuses",
            all(row["runner_decision"] == "REFUSE_SCORING" and not boolish(row["claim_allowed"]) for row in rows_map["runner"]),
            "runner refuses current scoring lanes",
        ),
        (
            "VAL1775_7_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel"]),
            "Q_tau/period countermodels remain live",
        ),
        (
            "VAL1775_8_claim_gates_blocked",
            all(not boolish(row["valid_for_claim"]) and row["status"] in {"BLOCKED", "REFUSED"} for row in rows_map["claim_gate"]),
            "claim gates are blocked or refused",
        ),
        ("VAL1775_9_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1775_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1775_11_decision_next",
            any(row["decision_id"] == "DEC1775_3_best_next" and "PIM_QTAU_SURFACE_MAP" in row["decision"] for row in rows_map["decision"]),
            "decision selects Pi_M/Q_tau surface map next",
        ),
        (
            "VAL1775_12_next_selected",
            any(row["route_id"] == "NEXT1775_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1775_13_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1775 CSVs parse"),
        ("VAL1775_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1775_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1775_16_formalization_untouched", formalization_untouched(), "no 1775 outputs found under formalization-workbench"),
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
            "check_id": "VAL1775_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1775 Q_tau-period map or Delta_period source-pack checkpoint",
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
            "# 1775 - Y5/R2FR Q_tau Period Map Current Descent or Delta_period Source Pack",
            "",
            "## Verdict",
            "",
            "This checkpoint names the exact bridge: `Delta_QP`, the gap between the parent Hamiltonian/Noether source charge and the `Pi_M` Hilbert linked period. If `Delta_QP=0`, with integrable `H_tau` and fixed boundary/reference data, the topological period can become the actual measured source charge. Current MTS does not yet prove this, so the map remains a conditional contract and the fallback source rows stay nonclaim.",
            "",
            "**Claim ceiling:** no `Q_tau`-period map, legal `M_H_ref`, `Delta_period` score, `R_eq` score, Newton/GR reduction, R10/R11 pass, PPN pass, clock/orbital pass, or local-GR claim is allowed from 1775.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Q_tau Period Map Theorem",
            markdown_table(rows_map["map_theorem"], ["theorem_id", "claim", "mathematical_form", "status", "would_close", "current_blocker", "valid_for_claim"]),
            "",
            "## Current Descent Audit",
            markdown_table(rows_map["descent_audit"], ["audit_id", "clause", "required_identity", "current_status", "residual_if_missing", "valid_for_claim"]),
            "",
            "## Delta Period Source Pack",
            markdown_table(rows_map["source_pack"], ["row_id", "quantity", "definition", "required_fields", "status", "score_ready", "claim_allowed", "valid_for_claim"]),
            "",
            "## Refusal Runner",
            markdown_table(rows_map["runner"], ["run_id", "input_row", "runner_decision", "refusal_reasons", "accepted_for_scoring", "claim_allowed"]),
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
            "This is progress because the problem is no longer 'how do we get mass?' in the abstract. The next door is concrete: prove the surface equality between `Pi_M J_H` and `H_tau-H_ref`, or fill `Delta_QP` as a real residual. That is the honest GR/Newton bridge pressure point.",
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
    doc_path = ROOT / "1775-Y5-R2FR-Qtau-period-map-current-descent-or-Delta-period-source-pack.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1775 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()

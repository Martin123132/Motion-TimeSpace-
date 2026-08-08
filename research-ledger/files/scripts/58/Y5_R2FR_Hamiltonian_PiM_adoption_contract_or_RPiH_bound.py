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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1777"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1777_0_1776_handoff",
        "source_key": "1776_handoff",
        "source_path": ROOT / "1776-Y5-R2FR-PiM-Q_tau-surface-map-owner-or-Delta-QP-first-row.md",
        "needles": ["NEXT1776_0_primary", "SMT1776_2_Hamiltonian_PiM_branch", "RPR1776_0_adopt_Hamiltonian_PiM"],
    },
    {
        "source_id": "SRC1777_1_1776_validation",
        "source_key": "1776_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1776_VALIDATION.csv",
        "needles": ["VAL1776_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1777_2_1776_delta_qp",
        "source_key": "1776_delta_qp_schema",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1776_DELTA_QP_FIRST_ROW_SCHEMA.csv",
        "needles": ["DQP1776_0_Delta_QP", "DQP1776_1_R_PiH"],
    },
    {
        "source_id": "SRC1777_3_539_candidate",
        "source_key": "539_hamiltonian_candidate",
        "source_path": ROOT / "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
        "needles": ["PH539_1_charge_representative", "PH539_3_no_independent_topological_credit", "HG539_3_old_PiM_equivalence"],
    },
    {
        "source_id": "SRC1777_4_540_readout",
        "source_key": "540_source_ppn_readout",
        "source_path": ROOT / "540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md",
        "needles": ["SMT540_0_branch_adoption", "SMT540_5_old_topological_equivalence_optional", "GPT540_5_full_PPN_vector"],
    },
    {
        "source_id": "SRC1777_5_541_scorecard",
        "source_key": "541_source_measure_scorecard",
        "source_path": ROOT / "541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md",
        "needles": ["HSM541_0_adopt_Hamiltonian_PiM", "HSS541_0_Hamiltonian_PiM_branch", "HSI541_6_PPN_vector"],
    },
    {
        "source_id": "SRC1777_6_539_branch_csv",
        "source_key": "539_branch_definition_csv",
        "source_path": RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_BRANCH_DEFINITION.csv",
        "needles": ["PH539_1_charge_representative", "PH539_3_no_independent_topological_credit"],
    },
    {
        "source_id": "SRC1777_7_539_gate_csv",
        "source_key": "539_gate_results_csv",
        "source_path": RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_GATE_RESULTS.csv",
        "needles": ["HG539_3_old_PiM_equivalence", "HG539_6_Gauss_PPN_readout"],
    },
    {
        "source_id": "SRC1777_8_topological_demotion_csv",
        "source_key": "topological_demotion_csv",
        "source_path": RESIDUALS / "P8_Y5_TOPOLOGICAL_PIM_DEMOTION_LEDGER.csv",
        "needles": ["demoted_unless_equivalent_to_PiM_H", "late equality multiplier"],
    },
    {
        "source_id": "SRC1777_9_repair_clause_csv",
        "source_key": "553_repair_clause_csv",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_REPAIR_CLAUSE_TEST.csv",
        "needles": ["HPT553_4_projector_variation_removed", "HPT553_6_denominator_and_Gauss_readout"],
    },
    {
        "source_id": "SRC1777_10_repair_residual_csv",
        "source_key": "553_repair_residual_csv",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_REPAIR_RESIDUAL_DECOMPOSITION.csv",
        "needles": ["HPRD553_3_old_PiM_equivalence", "HPRD553_6_total_no_cancellation"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1777_SOURCE_REGISTER.csv",
    "adoption_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1777_HAMILTONIAN_PIM_ADOPTION_CONTRACT.csv",
    "equivalence_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1777_OLD_PIM_EQUIVALENCE_AUDIT.csv",
    "demotion_policy": RESIDUALS / "P8_Y5_PARENT_QLOC_1777_OLD_PIM_DEMOTION_POLICY.csv",
    "r_pih_bound_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1777_RPIH_BOUND_PACK.csv",
    "downstream_debt": RESIDUALS / "P8_Y5_PARENT_QLOC_1777_DOWNSTREAM_DEBT_LEDGER.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1777_COUNTERMODEL_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1777_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1777_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1777_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1777_VALIDATION.csv",
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
                "role": "1777 Hamiltonian-PiM adoption/equivalence contract evidence",
            }
        )
    return rows


def adoption_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "HPA1777_0_declare_branch",
            "contract_clause": "declare whether the active local mass projector is Hamiltonian Pi_M^H",
            "mathematical_form": "Pi_M := Pi_M^H or Pi_M^top remains separately labelled Pi_M^top",
            "status": "CONTRACT_READY_NOT_ADOPTED",
            "why_needed": "prevents one symbol from hiding two mass channels",
            "missing_for_claim": "explicit parent-branch adoption plus symbol table update in main framework",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "HPA1777_1_charge_functional",
            "contract_clause": "define the mass functional from the parent Hamiltonian charge",
            "mathematical_form": "ell_H[J_H;tau,S] := 4*pi*G_ref int_S Q_tau^MTS[J_H]",
            "status": "FORMAL_CANDIDATE_ONLY",
            "why_needed": "mass must be a parent Noether/Hamiltonian charge, not a readout-selected mask",
            "missing_for_claim": "Theta_total/Q_tau owner and integrability/reference lock",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "HPA1777_2_representative",
            "contract_clause": "represent the Hamiltonian charge as a fixed mass cohomology representative",
            "mathematical_form": "Pi_M^H J_H := ell_H[J_H;tau,S] omega_M^H with integral_L omega_M^H=1",
            "status": "CANDIDATE_REPRESENTATIVE_ONLY",
            "why_needed": "lets Pi_M be a surface-charge representative while keeping the source object parent-owned",
            "missing_for_claim": "omega_M^H parent normalization and no-readout certificate",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "HPA1777_3_old_symbol_rule",
            "contract_clause": "old/topological Pi_M cannot be used as Pi_M unless equivalent to Pi_M^H",
            "mathematical_form": "Pi_M^top J_H = Pi_M^H J_H + dB_H + R_PiH",
            "status": "EQUIVALENCE_NOT_DERIVED",
            "why_needed": "keeps the old topological route from claiming measured mass by name",
            "missing_for_claim": "R_PiH theorem-zero or source-backed bound plus B_H flux rule",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "HPA1777_4_downstream_debt",
            "contract_clause": "Hamiltonian-PiM adoption does not itself prove Newton/GR",
            "mathematical_form": "adoption + integrability + source-measure glue + Gauss/Poisson + PPN vector all required",
            "status": "DEBT_RETAINED",
            "why_needed": "prevents notation from becoming a fake local-GR proof",
            "missing_for_claim": "HSM541_1 through HSM541_7 remain open",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "HPA1777_5_verdict",
            "contract_clause": "current MTS adopts Hamiltonian Pi_M as a claim-grade object",
            "mathematical_form": "HPA1777_0 through HPA1777_4 pass in one parent action with no circular source normalization",
            "status": "FAIL_CURRENT_PARENT_PROOF",
            "why_needed": "adoption/equivalence is the current source-normalization hinge",
            "missing_for_claim": "contract is staged but not signed; R_PiH and downstream rows remain missing",
            "valid_for_claim": False,
        },
    ]


def equivalence_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OPE1777_0_old_object",
            "object": "Pi_M^top",
            "test": "is the old/topological projector independently parent-owned?",
            "current_status": "DEMOTED_UNLESS_EQUIVALENT",
            "if_fail": "old PiM receives no measured-mass proof credit",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OPE1777_1_equivalence",
            "object": "R_PiH",
            "test": "Pi_M^top J_H - Pi_M^H J_H - dB_H = 0 or bounded",
            "current_status": "MISSING_RPIH_ZERO_OR_BOUND",
            "if_fail": "two mass channels survive",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OPE1777_2_boundary",
            "object": "B_H flux",
            "test": "int_boundary dB_H=0 under fixed reference/surface convention",
            "current_status": "MISSING_BOUNDARY_FLUX_RULE",
            "if_fail": "old-new equality can shift by boundary bookkeeping",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OPE1777_3_projector_stress",
            "object": "projector variation stress",
            "test": "old/projector variation stress is absent after adoption or mapped below PPN/local locks",
            "current_status": "MISSING_PROJECTOR_STRESS_MAP",
            "if_fail": "Hamiltonian adoption still leaves hidden fifth-force/PPN source",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OPE1777_4_verdict",
            "object": "old PiM status",
            "test": "old PiM is either equivalent to Pi_M^H or explicitly demoted",
            "current_status": "DEMOTION_POLICY_REQUIRED",
            "if_fail": "framework remains ambiguous about which mass charge is used",
            "valid_for_claim": False,
        },
    ]


def demotion_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "policy_id": "DPO1777_0_symbol_policy",
            "policy": "reserve Pi_M for Hamiltonian representative if adopted",
            "allowed_use": "Pi_M means Pi_M^H only after adoption contract is signed",
            "forbidden_use": "using Pi_M^top and Pi_M^H interchangeably",
            "status": "POLICY_STAGED_NOT_MAINLINE_ADOPTED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "policy_id": "DPO1777_1_old_topological",
            "policy": "label old/topological projector as Pi_M^top",
            "allowed_use": "closure/topological candidate or residual source term",
            "forbidden_use": "measured-GM/Newton evidence unless R_PiH=0/bounded",
            "status": "DEMOTED_GUARDRAIL",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "policy_id": "DPO1777_2_multiplier",
            "policy": "late equality multiplier is not a derivation",
            "allowed_use": "closure-only model ingredient if independently sourced with stress ledger",
            "forbidden_use": "imposing Pi_M^top=Pi_M^H to pass local GR",
            "status": "REJECTED_AS_PROOF",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "policy_id": "DPO1777_3_public_claim",
            "policy": "do not public-claim local GR/Newton from adoption notation",
            "allowed_use": "private derivation contract and source-row scaffold",
            "forbidden_use": "claiming source-normalized Newton before source-measure/Gauss/PPN gates",
            "status": "NONCLAIM_LOCK",
            "valid_for_claim": False,
        },
    ]


def r_pih_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "RPH1777_0_R_PiH",
            "quantity": "R_PiH_equivalence",
            "definition": "old/topological Pi_M current minus Hamiltonian Pi_M^H current after exact improvement",
            "required_fields": "system_id;PiM_top_definition;PiM_H_definition;J_H_source;B_H_flux;linked_periods;M_H_ref;units;source_path;equation_ref",
            "status": "MISSING_PIM_H_EQUIVALENCE",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RPH1777_1_B_H_flux",
            "quantity": "B_H_flux",
            "definition": "exact/boundary improvement flux in Pi_M^top to Pi_M^H equality",
            "required_fields": "surface_pair;boundary_rule;B_H_definition;B_H_flux;M_H_ref;units;source_path",
            "status": "MISSING_BOUNDARY_FLUX_RULE",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RPH1777_2_projector_stress",
            "quantity": "projector_stress_beta_equiv",
            "definition": "weak-field/PPN equivalent of any remaining projector variation stress after adoption/demotion",
            "required_fields": "delta_PiM;stress_map;weak_field_projection;PPN_lock;source_path",
            "status": "MISSING_PROJECTOR_STRESS_MAP",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RPH1777_3_Delta_QP",
            "quantity": "Delta_QP_surface_map",
            "definition": "(4*pi*G_ref)^-1 integral_L Pi_M^H J_H - (H_tau[S]-H_ref) after adoption",
            "required_fields": "system_id;surface_id;linked_cycle_id;PiM_H_period;H_tau;H_ref;G_ref;M_H_ref;units;source_path",
            "status": "MISSING_QTAU_PERIOD_MAP",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "RPH1777_4_total_abs",
            "quantity": "epsilon_HPiM_adoption_abs",
            "definition": "absolute no-cancellation envelope of adoption/equivalence residuals",
            "required_fields": "abs(R_PiH)+abs(B_H_flux)+abs(projector_stress)+abs(Delta_QP);M_H_ref;component_source_paths",
            "status": "MISSING_COMPONENT_INPUTS",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def downstream_debt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "debt_id": "DSD1777_0_integrability",
            "open_gate": "HSM541_1_integrable_charge",
            "why_still_open": "adoption does not prove Q_tau/H_tau integrability",
            "residual_if_open": "epsilon_HPiM_integrability_abs",
            "priority": "highest",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "debt_id": "DSD1777_1_source_measure",
            "open_gate": "HSM541_2_observed_worldtube_source",
            "why_still_open": "Hamiltonian charge must still equal observed Hilbert worldtube source before readout",
            "residual_if_open": "epsilon_HPiM_source_equality_abs",
            "priority": "highest",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "debt_id": "DSD1777_2_radial_gauss",
            "open_gate": "HSM541_3/HSM541_5 radial closure and Gauss readout",
            "why_still_open": "source-normalized Newton requires radial closure and Poisson/Gauss calibration",
            "residual_if_open": "epsilon_HPiM_radial_closure_abs;Delta_cal;alpha_lambda",
            "priority": "highest_after_adoption",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "debt_id": "DSD1777_3_PPN",
            "open_gate": "HSM541_7_PPN_followthrough",
            "why_still_open": "local GR requires gamma/beta/preferred-frame vector after first-order Newton",
            "residual_if_open": "delta_beta_source;gamma_minus_one;alpha_i;zeta_i;xi",
            "priority": "after_Newton",
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1777_0_symbol_collision",
            "countermodel": "Pi_M symbol silently refers to different projectors in different derivation steps",
            "survives_current_constraints": True,
            "why_survives": "main framework has not adopted a single Pi_M symbol policy",
            "what_kills_it": "Hamiltonian-PiM adoption contract plus old-PiM demotion/equivalence",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1777_1_candidate_not_charge",
            "countermodel": "Pi_M^H is defined but Q_tau is nonintegrable or reference-shifted",
            "survives_current_constraints": True,
            "why_survives": "H_tau integrability/reference lock remains open",
            "what_kills_it": "H_tau integrability theorem or source-backed curl/reference row",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1777_2_old_topological_wrong_object",
            "countermodel": "old/topological Pi_M stays closed but measures a different charge",
            "survives_current_constraints": True,
            "why_survives": "R_PiH is not zeroed or bounded",
            "what_kills_it": "R_PiH=0 theorem, small sourced bound, or explicit demotion from claims",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1777_3_notation_becomes_claim",
            "countermodel": "adoption notation is treated as source-normalized Newton",
            "survives_current_constraints": True,
            "why_survives": "source-measure/Gauss/PPN gates still fail or are not reached",
            "what_kills_it": "HSM541 scorecard gates become theorem-zero/source-backed and pass",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1777_0_adoption_status",
            "decision": "HAMILTONIAN_PIM_ADOPTION_CONTRACT_STAGED_NOT_SIGNED",
            "reason": "Pi_M^H is the lowest-scrutiny mass representative but requires parent current/integrability/source-measure proof",
            "next_action": "do not relabel main framework yet; keep adoption as private contract",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1777_1_old_PiM",
            "decision": "OLD_TOPOLOGICAL_PIM_DEMOTED_UNLESS_EQUIVALENT",
            "reason": "closed topology alone can conserve the wrong object",
            "next_action": "carry R_PiH and B_H_flux rows forward",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1777_2_no_promotion",
            "decision": "NO_NEWTON_LOCAL_GR_PROMOTION_FROM_NOTATION",
            "reason": "source-measure, radial closure, Gauss/orbital readout, universal G, and PPN followthrough remain open",
            "next_action": "keep all claim gates false",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1777_3_best_next",
            "decision": "ADOPTED_PIM_SOURCE_MEASURE_GLUE_OR_RPIH_FIRST_ROW_IS_NEXT",
            "reason": "after symbol policy, the next real theorem is whether Pi_M^H reads the observed source worldtube and old PiM mismatch is bounded",
            "next_action": "build 1778 adopted-PiM source-measure glue or first R_PiH row",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1777_0_adoption",
            "claim": "Hamiltonian Pi_M is adopted as parent-signed mass projector",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "CONTRACT_STAGED_NOT_MAINLINE_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1777_1_old_equivalence",
            "claim": "old/topological Pi_M equals Pi_M^H up to zero-flux terms",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "MISSING_RPIH_ZERO_OR_BOUND",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1777_2_RPiH_score",
            "claim": "R_PiH bound row can be scored",
            "gate_pass": False,
            "status": "REFUSED",
            "blocker": "MISSING_NUMERIC_OR_THEOREM_ZERO_INPUTS_AND_MHREF",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1777_3_Newton_local_GR",
            "claim": "source-normalized Newton/local GR can reopen",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "SOURCE_MEASURE_GAUSS_PPN_DEBT_RETAINED",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1777_0_primary",
            "next_target": "1778-Y5-R2FR-adopted-PiM-source-measure-glue-or-RPiH-first-row.md",
            "script": "scripts/Y5_R2FR_adopted_PiM_source_measure_glue_or_RPiH_first_row.py",
            "objective": "try to prove Pi_M^H reads the observed Hilbert worldtube source before readout; if not, stage the first strict R_PiH/B_H_flux source row",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1777_1_parallel",
            "next_target": "1778b-Y5-R2FR-Hamiltonian-PiM-symbol-policy-mainline-patch-plan.md",
            "script": "scripts/Y5_R2FR_Hamiltonian_PiM_symbol_policy_mainline_patch_plan.py",
            "objective": "prepare a later mainline patch plan that reserves Pi_M for Pi_M^H and relabels old topological Pi_M as Pi_M^top without making claims",
            "selection_status": "held_parallel",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "adoption_contract": adoption_contract_rows(),
        "equivalence_audit": equivalence_audit_rows(),
        "demotion_policy": demotion_policy_rows(),
        "r_pih_bound_pack": r_pih_bound_rows(),
        "downstream_debt": downstream_debt_rows(),
        "countermodel": countermodel_rows(),
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
        shutil.copy2(path, RAB_QUEUE / f"JR1777_{key.upper()}.csv")


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
        if not (RAB_QUEUE / f"JR1777_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    return not any(FORMALIZATION.rglob("*1777*")) if FORMALIZATION.exists() else True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1777_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1777_1_needles_present", needles_ok, "required source needles are present"),
        (
            "VAL1777_2_adoption_contract_staged",
            any(row["clause_id"] == "HPA1777_0_declare_branch" and row["status"] == "CONTRACT_READY_NOT_ADOPTED" for row in rows_map["adoption_contract"]),
            "Hamiltonian-PiM adoption contract is staged",
        ),
        (
            "VAL1777_3_current_adoption_not_promoted",
            any(row["clause_id"] == "HPA1777_5_verdict" and row["status"] == "FAIL_CURRENT_PARENT_PROOF" for row in rows_map["adoption_contract"]),
            "current adoption remains unpromoted",
        ),
        (
            "VAL1777_4_old_pim_demoted",
            any(row["policy_id"] == "DPO1777_1_old_topological" and row["status"] == "DEMOTED_GUARDRAIL" for row in rows_map["demotion_policy"]),
            "old/topological PiM demotion guardrail is written",
        ),
        (
            "VAL1777_5_RPiH_rows_nonclaim",
            all(not boolish(row["valid_for_claim"]) and not boolish(row["score_ready"]) for row in rows_map["r_pih_bound_pack"]),
            "R_PiH bound rows remain nonclaim",
        ),
        (
            "VAL1777_6_downstream_debt_retained",
            all(not boolish(row["valid_for_claim"]) for row in rows_map["downstream_debt"]),
            "source-measure/Gauss/PPN debt remains retained",
        ),
        (
            "VAL1777_7_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel"]),
            "Hamiltonian-PiM countermodels remain live",
        ),
        (
            "VAL1777_8_claim_gates_blocked",
            all(not boolish(row["valid_for_claim"]) and row["status"] in {"BLOCKED", "REFUSED"} for row in rows_map["claim_gate"]),
            "claim gates are blocked or refused",
        ),
        ("VAL1777_9_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1777_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1777_11_decision_next",
            any(row["decision_id"] == "DEC1777_3_best_next" and "ADOPTED_PIM_SOURCE_MEASURE" in row["decision"] for row in rows_map["decision"]),
            "decision selects adopted-PiM source-measure glue next",
        ),
        (
            "VAL1777_12_next_selected",
            any(row["route_id"] == "NEXT1777_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1777_13_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1777 CSVs parse"),
        ("VAL1777_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1777_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1777_16_formalization_untouched", formalization_untouched(), "no 1777 outputs found under formalization-workbench"),
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
            "check_id": "VAL1777_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1777 Hamiltonian-PiM adoption contract or R_PiH bound checkpoint",
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
            "# 1777 - Y5/R2FR Hamiltonian-PiM Adoption Contract or RPiH Bound",
            "",
            "## Verdict",
            "",
            "The adoption contract is now explicit, but it is not yet signed for current MTS. The clean route is to reserve `Pi_M` for the Hamiltonian charge representative `Pi_M^H`; old/topological `Pi_M` must be relabelled `Pi_M^top` and earns no measured-mass credit unless `R_PiH=0` or is source-bounded. This removes the symbol collision, but it does not by itself prove source-measure glue, Newton, PPN, or local GR.",
            "",
            "**Claim ceiling:** no Hamiltonian-`Pi_M` adoption, old-`Pi_M` equivalence, `R_PiH` score, source-normalized Newton, GR reduction, R10/R11 pass, PPN pass, clock/orbital pass, or local-GR claim is allowed from 1777.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Adoption Contract",
            markdown_table(rows_map["adoption_contract"], ["clause_id", "contract_clause", "mathematical_form", "status", "why_needed", "missing_for_claim", "valid_for_claim"]),
            "",
            "## Old-PiM Equivalence Audit",
            markdown_table(rows_map["equivalence_audit"], ["audit_id", "object", "test", "current_status", "if_fail", "valid_for_claim"]),
            "",
            "## Demotion Policy",
            markdown_table(rows_map["demotion_policy"], ["policy_id", "policy", "allowed_use", "forbidden_use", "status", "valid_for_claim"]),
            "",
            "## R_PiH Bound Pack",
            markdown_table(rows_map["r_pih_bound_pack"], ["row_id", "quantity", "definition", "required_fields", "status", "score_ready", "claim_allowed", "valid_for_claim"]),
            "",
            "## Downstream Debt Ledger",
            markdown_table(rows_map["downstream_debt"], ["debt_id", "open_gate", "why_still_open", "residual_if_open", "priority", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
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
            "This is a strong architecture cleanup. It does not prove local GR, but it prevents the framework from quietly switching mass definitions mid-proof. The next honest target is source-measure glue for the adopted Hamiltonian representative, or the first real `R_PiH` residual row.",
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
    doc_path = ROOT / "1777-Y5-R2FR-Hamiltonian-PiM-adoption-contract-or-RPiH-bound.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1777 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()

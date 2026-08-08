from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1721"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1721 - Source Prefactor Exclusion Or wA Current Row"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1721_0_1720_doc",
        "source_key": "1720_doc",
        "source_path": ROOT / "1720-Y5-R2FR-observed-Hilbert-current-norm-source-row-or-matter-functor-signature.md",
        "needles": ["NEXT1720_0_primary", "source-only prefactor"],
    },
    {
        "source_id": "SRC1721_1_1720_validation",
        "source_key": "1720_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1720_VALIDATION.csv",
        "needles": ["VAL1720_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1721_2_1720_matter_audit",
        "source_key": "1720_matter_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "needles": ["MFS1720_6_no_shadow_or_source_prefactor", "SOURCE_PREFACTOR_COUNTERMODEL_SURVIVES"],
    },
    {
        "source_id": "SRC1721_3_1720_jh_theorem",
        "source_key": "1720_jh_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_CURRENT_DEFINITION_THEOREM.csv",
        "needles": ["JHT1720_3_source_prefactor_countermodel", "COUNTERMODEL_SURVIVES"],
    },
    {
        "source_id": "SRC1721_4_1488_doc",
        "source_key": "1488_doc",
        "source_path": ROOT / "1488-Y5-R10-RAB-ordinary-matter-subaction-current-chain-owner-or-explicit-wA-residual-lock.md",
        "needles": ["WA1488_7_lock_verdict", "NONCLAIM_LOCK"],
    },
    {
        "source_id": "SRC1721_5_1488_lock",
        "source_key": "1488_lock",
        "source_path": RESIDUALS / "P8_Y5_R10_1488_WA_DELTAW_RESIDUAL_LOCK.csv",
        "needles": ["WA1488_7_lock_verdict", "NONCLAIM_LOCK"],
    },
    {
        "source_id": "SRC1721_6_1479_typing",
        "source_key": "1479_typing",
        "source_path": RESIDUALS / "P8_Y5_R10_1479_NO_SOURCE_ONLY_ACTION_PREFACTOR_TYPING_THEOREM_ATTEMPT.csv",
        "needles": ["NST1479_4_verdict", "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED"],
    },
    {
        "source_id": "SRC1721_7_1479_hom",
        "source_key": "1479_hom",
        "source_path": RESIDUALS / "P8_Y5_R10_1479_HOM_SPECIES_TO_SOURCE_PREFACTOR_AUDIT.csv",
        "needles": ["HOM1479_1_species_to_prefactor", "FORBIDDEN_BY_CONTRACT_NOT_PARENT_DERIVED"],
    },
    {
        "source_id": "SRC1721_8_1479_countermodel",
        "source_key": "1479_countermodel",
        "source_path": RESIDUALS / "P8_Y5_R10_1479_SOURCE_ONLY_PREFACTOR_COUNTERMODEL_LEDGER.csv",
        "needles": ["CM1479_0_wA_action", "S_matter=sum_A w_A S_A"],
    },
    {
        "source_id": "SRC1721_9_1604_no_wA",
        "source_key": "1604_no_wA",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1604_NO_WA_THEOREM_ATTEMPT.csv",
        "needles": ["NWA1604_7_verdict", "NO_WA_NOT_DERIVED"],
    },
    {
        "source_id": "SRC1721_10_1604_countermodel",
        "source_key": "1604_countermodel",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1604_WA_COUNTERMODEL_AUDIT.csv",
        "needles": ["WAC1604_0_direct_sum_weight", "LIVE_COUNTERMODEL"],
    },
    {
        "source_id": "SRC1721_11_1605_action_owner",
        "source_key": "1605_action_owner",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1605_ACTION_DENSITY_OWNER_THEOREM_ATTEMPT.csv",
        "needles": ["ADO1605_6_verdict", "ACTION_DENSITY_OWNER_NOT_PARENT_SIGNED"],
    },
    {
        "source_id": "SRC1721_12_1606_component_pack",
        "source_key": "1606_component_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1606_DELTA_W_COMPONENT_BOUND_PACK.csv",
        "needles": ["DWB1606_1_delta_w_e", "PROXY_UNIT_KERNEL_ONLY"],
    },
    {
        "source_id": "SRC1721_13_1607_material_tensor",
        "source_key": "1607_material_tensor",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1607_MATERIAL_TENSOR_CONTEXT_AUDIT.csv",
        "needles": ["MTA1607_5_full_tensor", "MISSING_FULL_PARENT_MATERIAL_TENSOR"],
    },
    {
        "source_id": "SRC1721_14_1608_tau",
        "source_key": "1608_tau",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1608_TAU_WEP_READOUT_CONTRACT.csv",
        "needles": ["TAU1608_4_verdict", "TAU_WEP_NOT_EVALUATED"],
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(col, "")).replace("\n", " ") for col in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        needles_present = exists and all(needle in text for needle in source["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(exists),
                "needles_present": yesno(needles_present),
                "required_needles": ";".join(source["needles"]),
                "generated_utc": UTC,
            }
        )
    return rows


def sources_for(keys: set[str]) -> str:
    return ";".join(str(item["source_path"]) for item in SOURCES if item["source_key"] in keys)


NO_SOURCE_PREFACTOR_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "theorem_id": "NSP1721_0_target",
        "claim_piece": "no source-only prefactor slot",
        "formal_statement": "Hom_parent(species_label, hidden_marker, readout_label -> R_+ active-source-prefactor) is absent or common-constant only before variation",
        "proof_status": "TARGET_EXACT",
        "mathematical_effect_if_signed": "S_ord cannot contain independent w_A S_A slots, so the observed Hilbert current is unique up to one universal calibration",
        "blocking_gap": "the object-language restriction is still a contract, not derived from deeper MTS primitives",
        "theorem_closed": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "theorem_id": "NSP1721_1_conditional_typing",
        "claim_piece": "typed parent-action domain",
        "formal_statement": "Allowed source coefficients depend only on q-owned observed geometry, dynamical fields, fixed representation data, and universal constants",
        "proof_status": "EXACT_CONDITIONAL_META_THEOREM",
        "mathematical_effect_if_signed": "relative delta_w_A is ill-typed rather than tuned small",
        "blocking_gap": "hidden invariant, marker, current-label, and readout-label maps remain legal unless parent-signature excludes them",
        "theorem_closed": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "theorem_id": "NSP1721_2_same_action_no_go",
        "claim_piece": "same-action Hilbert current is insufficient",
        "formal_statement": "S_ord=sum_A w_A S_A still gives T_source=sum_A w_A T_A under the same coframe variation",
        "proof_status": "NO_GO_GUARD",
        "mathematical_effect_if_signed": "prevents false proof by covariance, additivity, or isolated matter EOM scaling",
        "blocking_gap": "no exception; this remains a retained guardrail",
        "theorem_closed": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "theorem_id": "NSP1721_3_action_density_graph_route",
        "claim_piece": "parent-owned connected action-density graph",
        "formal_statement": "if every ordinary sector lies on one parent-owned L_action graph with nonzero morphisms, naturality forces w_A=w_*",
        "proof_status": "EXACT_CONDITIONAL_LEMMA_NOT_PARENT_SIGNED",
        "mathematical_effect_if_signed": "component delta_w vector collapses to a derivative-silent common calibration",
        "blocking_gap": "1605/1606 show physical connectedness exists only as template; parent-owned edges are missing",
        "theorem_closed": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "theorem_id": "NSP1721_4_verdict",
        "claim_piece": "no-w_A source-prefactor proof status",
        "formal_statement": "No-w_A is a clean conditional theorem, but current MTS does not parent-sign the no-Hom/action-density owner clauses",
        "proof_status": "NO_SOURCE_PREFACTOR_NOT_DERIVED",
        "mathematical_effect_if_signed": "would unblock the J_H norm source-owner route upstream of N_domain",
        "blocking_gap": "retain w_A/delta_w_A current rows as finite nonclaim coupling debt",
        "theorem_closed": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


WA_CURRENT_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "row_id": "WAC1721_0_weighted_Hilbert_current_identity",
        "quantity": "J_H_weighted",
        "definition": "observed Hilbert current when pre-variation ordinary-matter source/action weights survive",
        "formula": "J_H^w[tau] = star(sum_A w_A T_A_obs(tau,.))",
        "common_mode": "w_A = w_star(1+delta_w_A)",
        "residual_formula": "Delta J_w[tau] = star(sum_A delta_w_A T_A_obs(tau,.)) after one common w_star calibration",
        "current_value": "FORMAL_IDENTITY_ONLY",
        "units": "same_as_Hilbert_current_norm_after_norm_convention",
        "source_path": sources_for({"1720_jh_theorem", "1479_countermodel", "1488_lock", "1604_countermodel"}),
        "source_anchor": "JHT1720_3;CM1479_0;WA1488_1..7;WAC1604_0",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "row_id": "WAC1721_1_weighted_current_norm_candidate",
        "quantity": "C_wH",
        "definition": "finite contribution of surviving delta_w_A to the J_H norm on A_ext",
        "formula": "C_wH := ||star(sum_A delta_w_A T_A_obs(tau,.))||_{A_ext,norm}",
        "required_fields": "A_ext;norm_type;tau_obs;component_basis;T_A_component_decomposition;delta_w_vector;covariance;units;source_path;valid_for_claim",
        "current_value": "MISSING_NORM_TYPE;MISSING_A_EXT;MISSING_COMPONENT_TENSOR;MISSING_DELTA_W_VECTOR;MISSING_TAU_LOCK",
        "units": "MISSING_CURRENT_NORM_UNITS",
        "source_path": sources_for({"1606_component_pack", "1607_material_tensor", "1608_tau", "1720_jh_theorem"}),
        "source_anchor": "1606 DWB1606_*;1607 MTA1607_5;1608 TAU1608_4;1720 JHT1720_2",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "row_id": "WAC1721_2_no_Hom_zero_route",
        "quantity": "C_wH_zero_route",
        "definition": "theorem-zero route for weighted-current residual",
        "formula": "C_wH=0 if no source-only Hom exists and only derivative-silent common w_star remains",
        "required_fields": "parent_action_density_owner;typed_domain_no_Hom;common_measure_owner;parent_owned_graph;readout_no_reentry;nonHilbert_silence",
        "current_value": "NO_SOURCE_PREFACTOR_NOT_DERIVED",
        "units": "not_applicable_if_zero_theorem_signed",
        "source_path": sources_for({"1479_typing", "1604_no_wA", "1605_action_owner"}),
        "source_anchor": "NST1479_4;NWA1604_7;ADO1605_6",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "row_id": "WAC1721_3_verdict",
        "quantity": "w_A_JH_current_gate",
        "definition": "claim status of source-prefactor correction to the J_H norm",
        "formula": "J_H usable for N_domain only after C_wH=0 theorem or source-backed finite C_wH bound",
        "required_fields": "zero theorem or finite weighted-current norm pack",
        "current_value": "RETAINED_NONCLAIM_COUPLING_DEBT",
        "units": "declared by future C_wH row",
        "source_path": sources_for({"1720_doc", "1606_component_pack", "1607_material_tensor", "1608_tau"}),
        "source_anchor": "1720 DEC1720_1;1606 READY1606_5;1607 READY1607_5;1608 TLS1608_6",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


EXISTING_BRANCH_BRIDGE_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "bridge_id": "BR1721_0_existing_delta_w_lock",
        "source_artifact": "P8_Y5_R10_1488_WA_DELTAW_RESIDUAL_LOCK.csv",
        "status_imported": "NONCLAIM_LOCK",
        "use_in_1721": "w_A/delta_w_A residuals are already explicit and must feed J_H current rows",
        "missing_for_claim": "parent no-Hom theorem or finite source-backed coefficient values",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "bridge_id": "BR1721_1_existing_no_wA_contract",
        "source_artifact": "P8_Y5_PARENT_QLOC_1604_NO_WA_THEOREM_ATTEMPT.csv",
        "status_imported": "NO_WA_NOT_DERIVED",
        "use_in_1721": "do not repeat false zero proof; retain exact conditional theorem only",
        "missing_for_claim": "action-density owner, common measure, typed domain, current owner and readout no-reentry",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "bridge_id": "BR1721_2_existing_graph_route",
        "source_artifact": "P8_Y5_PARENT_QLOC_1606_DELTA_W_COMPONENT_BOUND_PACK.csv",
        "status_imported": "COMPONENT_PACK_SOURCE_READY_NOT_SCORE_READY",
        "use_in_1721": "finite branch supplies component names for C_wH but not a claim-grade value",
        "missing_for_claim": "full component vector, material tensor, tau/readout basis and covariance",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "bridge_id": "BR1721_3_existing_material_tau_route",
        "source_artifact": "1607/1608 material tensor and tau contracts",
        "status_imported": "MATERIAL_TENSOR_AND_TAU_NOT_READY",
        "use_in_1721": "prevents converting WEP/product anchors into delta_w or C_wH values",
        "missing_for_claim": "full parent material-response tensor and positive tau/nondegeneracy result",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


RUNNER_REFUSAL_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1721_0_no_source_prefactor",
        "quantity": "no-w_A theorem-zero",
        "runner_decision": "REJECT_THEOREM_ZERO",
        "refusal_reasons": "NO_HOM_CONTRACT_NOT_PARENT_SIGNED;ACTION_DENSITY_OWNER_UNSIGNED;PARENT_GRAPH_EDGES_MISSING;READOUT_REENTRY_OPEN",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1721_1_C_wH_finite_bound",
        "quantity": "weighted-current norm bound",
        "runner_decision": "REFUSE_SCORING",
        "refusal_reasons": "MISSING_COMPONENT_VECTOR;MISSING_MATERIAL_TENSOR;MISSING_TAU_LOCK;MISSING_NORM_TYPE;MISSING_A_EXT;VALID_FOR_CLAIM_FALSE",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1721_2_JH_norm",
        "quantity": "observed Hilbert current norm including source-prefactor guard",
        "runner_decision": "BLOCKED_NO_CLAIM",
        "refusal_reasons": "C_wH_NOT_ZERO_OR_BOUNDED;JH_NORM_ROW_STILL_TEMPLATE;NONHILBERT_AND_TAU_GATES_OPEN",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1721_3_Newton_GR",
        "quantity": "Newton/local-GR source-normalization reopening",
        "runner_decision": "BLOCKED_NO_CLAIM",
        "refusal_reasons": "SOURCE_PREFACTOR_SURVIVES;JH_NORM_UNBOUNDED;M_H_REF_AND_PPN_VECTOR_OPEN",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


DECISION_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "decision_id": "DEC1721_0_theorem_status",
        "decision": "do not promote no-w_A theorem-zero",
        "because": "no-Hom/source-prefactor exclusion is exact only as a parent grammar contract",
        "next_action": "either source parent-owned action-density/graph edges or keep C_wH as finite nonclaim current norm debt",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "decision_id": "DEC1721_1_JH_norm_status",
        "decision": "J_H norm cannot ignore w_A",
        "because": "pre-variation weights enter the same Hilbert variation and therefore alter the active source current",
        "next_action": "add C_wH to the J_H norm input stack before any N_domain/Newton/GR reopening",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "decision_id": "DEC1721_2_next",
        "decision": "target parent-owned action-density edge or C_wH norm bound",
        "because": "the theory route and finite route now meet at one object: weighted-current norm contribution",
        "next_action": "1722 should try to sign a parent action-density owner edge; if not, build a C_wH norm-bound source row with component/tau/material dependencies",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


NEXT_TARGET_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "route_id": "NEXT1721_0_primary",
        "next_target": "1722-Y5-R2FR-parent-action-density-edge-or-CwH-current-norm-bound.md",
        "script": "scripts/Y5_R2FR_parent_action_density_edge_or_CwH_current_norm_bound.py",
        "objective": "try to parent-sign an action-density owner/no-Hom edge that kills w_A; if not, build the finite C_wH weighted-current norm-bound source row",
        "selection_status": "selected",
        "success_condition": "C_wH is theorem-zero from parent action syntax, or a source-backed finite row has norm, units, tau, component tensor, covariance and no shortcut provenance",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "route_id": "NEXT1721_1_parallel_JH_norm",
        "next_target": "1722b-Y5-R2FR-JH-norm-stack-with-source-prefactor-guard.md",
        "script": "scripts/Y5_R2FR_JH_norm_stack_with_source_prefactor_guard.py",
        "objective": "merge JHN1720 and WAC1721 into one guarded J_H norm input schema for N_domain",
        "selection_status": "held_parallel",
        "success_condition": "J_H norm row refuses scoring unless source-prefactor, tau, annulus and non-Hilbert-current gates are all resolved",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


CLAIM_GATE_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1721_0_no_wA",
        "claim": "source-only action/source prefactor is theorem-zero",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "no-Hom typing theorem is exact only as unsigned parent grammar contract",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1721_1_C_wH",
        "claim": "weighted-current contribution C_wH is zero or finite bounded",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "C_wH row lacks component vector, material tensor, tau/source lock, norm type, annulus and units",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1721_2_JH_norm",
        "claim": "observed Hilbert current norm is source-backed",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "J_H norm cannot be scored while source-prefactor current contribution is unresolved",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1721_3_Newton_local_GR",
        "claim": "Newton/local-GR source-normalization gate can reopen",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "source-prefactor, J_H norm, M_H_ref, R_eq and PPN vector remain open",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1721_SOURCE_REGISTER.csv",
    "no_source_prefactor": RESIDUALS / "P8_Y5_PARENT_QLOC_1721_NO_SOURCE_PREFACTOR_THEOREM_AUDIT.csv",
    "wa_current": RESIDUALS / "P8_Y5_PARENT_QLOC_1721_WA_CURRENT_NORM_SOURCE_ROWS.csv",
    "bridge": RESIDUALS / "P8_Y5_PARENT_QLOC_1721_EXISTING_BRANCH_BRIDGE.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1721_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1721_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1721_NEXT_TARGET.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1721_CLAIM_GATE.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1721_VALIDATION.csv",
}


COPY_MAP = {
    "no_source_prefactor": "R2FR_no_source_prefactor_theorem_audit_1721.csv",
    "wa_current": "R2FR_wA_current_norm_source_rows_1721.csv",
    "bridge": "R2FR_existing_branch_bridge_1721.csv",
    "runner_refusal": "R2FR_runner_refusal_1721.csv",
    "decision": "R2FR_decision_ledger_1721.csv",
    "next_target": "R2FR_next_target_1721.csv",
    "claim_gate": "R2FR_claim_gate_1721.csv",
}


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register(),
        "no_source_prefactor": NO_SOURCE_PREFACTOR_ROWS,
        "wa_current": WA_CURRENT_ROWS,
        "bridge": EXISTING_BRANCH_BRIDGE_ROWS,
        "runner_refusal": RUNNER_REFUSAL_ROWS,
        "decision": DECISION_ROWS,
        "next_target": NEXT_TARGET_ROWS,
        "claim_gate": CLAIM_GATE_ROWS,
    }


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1721_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1721_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "accepted_for_scoring",
        "theorem_closed",
    }
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def wa_source_paths_exist() -> bool:
    for row in WA_CURRENT_ROWS:
        paths = [Path(item) for item in row["source_path"].split(";") if item]
        if not paths or any(not path.exists() for path in paths):
            return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1721_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1721_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1721*"):
        text = str(path)
        if "\\.venv\\" in text or "\\__pycache__\\" in text:
            continue
        if path.is_file():
            return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    source_rows = rows_map["source_register"]
    theorem_rows = rows_map["no_source_prefactor"]
    current_rows = rows_map["wa_current"]
    bridge_rows = rows_map["bridge"]
    runner_rows = rows_map["runner_refusal"]
    decision_rows = rows_map["decision"]
    next_rows = rows_map["next_target"]
    claim_rows = rows_map["claim_gate"]
    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    validation = [
        check("VAL1721_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1721_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "required source needles are present", "one or more required source needles missing"),
        check(
            "VAL1721_2_1720_handoff_preserved",
            any(row["source_key"] == "1720_doc" and row["needles_present"] == "True" for row in source_rows),
            "1720 selected source-prefactor route",
            "1720 handoff missing",
        ),
        check(
            "VAL1721_3_no_prefactor_not_derived",
            any(row["theorem_id"] == "NSP1721_4_verdict" and row["proof_status"] == "NO_SOURCE_PREFACTOR_NOT_DERIVED" for row in theorem_rows),
            "no-source-prefactor theorem remains unproved",
            "no-source-prefactor verdict missing or promoted",
        ),
        check(
            "VAL1721_4_same_action_guard_retained",
            any(row["theorem_id"] == "NSP1721_2_same_action_no_go" and row["proof_status"] == "NO_GO_GUARD" for row in theorem_rows),
            "same-action Hilbert-current shortcut is blocked",
            "same-action guard missing",
        ),
        check(
            "VAL1721_5_wa_current_rows_nonclaim",
            len(current_rows) == 4 and all(row["valid_for_claim"] == "False" and row["score_ready"] == "False" for row in current_rows),
            "w_A weighted-current rows exist and remain nonclaim",
            "w_A weighted-current rows missing or claim-enabled",
        ),
        check(
            "VAL1721_6_wa_source_paths_exist",
            wa_source_paths_exist(),
            "all source paths listed in w_A current rows exist",
            "one or more w_A source paths missing",
        ),
        check(
            "VAL1721_7_existing_branch_bridge",
            len(bridge_rows) == 4 and all(row["valid_for_claim"] == "False" for row in bridge_rows),
            "existing delta_w/material/tau branch is bridged as nonclaim",
            "existing branch bridge missing or claim-enabled",
        ),
        check(
            "VAL1721_8_runner_refuses_shortcuts",
            all(row["accepted_for_scoring"] == "False" and row["claim_allowed"] == "False" for row in runner_rows),
            "runner refuses no-w_A, C_wH, J_H norm and Newton/GR shortcuts",
            "runner allowed scoring or claim shortcut",
        ),
        check(
            "VAL1721_9_decision_selects_CwH_route",
            any(row["decision_id"] == "DEC1721_2_next" and "C_wH" in row["next_action"] for row in decision_rows),
            "decision ledger selects parent edge or C_wH bound route",
            "decision ledger does not select C_wH route",
        ),
        check(
            "VAL1721_10_next_selected",
            any(row["route_id"] == "NEXT1721_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "next target selects parent action-density edge or C_wH current norm bound",
            "next target missing selected primary route",
        ),
        check(
            "VAL1721_11_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check("VAL1721_12_csv_parse", parsed_ok, "all generated 1721 CSVs parse", "one or more generated 1721 CSVs failed to parse"),
        check("VAL1721_13_no_claim_flags", no_claim_flags(rows_map), "all generated scoring and claim flags remain false", "one or more generated flags enabled a claim"),
        check("VAL1721_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1721_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1721_16_formalization_untouched", formalization_untouched(), "no 1721 outputs found under formalization-workbench", "1721 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1721_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1721 source-prefactor exclusion and w_A current-row validation" if overall else "one or more 1721 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1721 attacks the coupling slot identified by 1720: independent pre-variation `w_A S_A` source/action weights.",
        "- The exact theorem is still clean: if the parent object language has no source-only `Hom(... -> active-source-prefactor)` slot, and ordinary matter sits on one parent action-density owner, then relative `w_A` dies modulo one derivative-silent common calibration.",
        "- That theorem is not parent-signed in the current corpus. Same-action Hilbert variation is not enough, because `S_ord=sum_A w_A S_A` varies to `T_source=sum_A w_A T_A`.",
        "- The honest output is a new guarded current row: `C_wH := ||star(sum_A delta_w_A T_A_obs(tau,.))||_{A_ext,norm}`. This is the source-prefactor contribution that must be zero-proved or bounded before `J_H` can feed `N_domain` or Newton/GR gates.",
        "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, source-normalization, `J_H`-norm, or public claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## No-Source-Prefactor Theorem Audit",
        markdown_table(rows_map["no_source_prefactor"], ["theorem_id", "claim_piece", "proof_status", "mathematical_effect_if_signed", "blocking_gap", "theorem_closed"]),
        "",
        "## w_A Weighted-Current Rows",
        markdown_table(rows_map["wa_current"], ["row_id", "quantity", "formula", "current_value", "source_anchor", "score_ready", "valid_for_claim"]),
        "",
        "## Existing Branch Bridge",
        markdown_table(rows_map["bridge"], ["bridge_id", "source_artifact", "status_imported", "use_in_1721", "missing_for_claim"]),
        "",
        "## Runner Refusal",
        markdown_table(rows_map["runner_refusal"], ["run_id", "quantity", "runner_decision", "refusal_reasons", "accepted_for_scoring", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "1721 is the punchline of the coupling hunt so far: the problem is not whether a Hilbert current can be written, but whether the parent action forbids weighting the ordinary sectors before that current is varied. Until the no-Hom/action-density owner theorem is signed, the finite `C_wH` weighted-current norm must travel with the `J_H` norm stack. This keeps the GR/Newton route honest: no hidden source universality, but also no abandonment of the derivation path.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1721-Y5-R2FR-source-prefactor-exclusion-or-wA-current-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1721_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1721 validation FAIL")
    print("1721 validation PASS")


if __name__ == "__main__":
    main()

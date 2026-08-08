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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1723"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1723 - Guarded JH Norm Stack Or CwH Input Source"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1723_0_1722_doc",
        "source_key": "1722_doc",
        "source_path": ROOT / "1722-Y5-R2FR-parent-action-density-edge-or-CwH-current-norm-bound.md",
        "needles": ["NEXT1722_0_primary", "guarded J_H norm stack"],
    },
    {
        "source_id": "SRC1723_1_1722_validation",
        "source_key": "1722_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1722_VALIDATION.csv",
        "needles": ["VAL1722_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1723_2_1722_bound_law",
        "source_key": "1722_bound_law",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1722_CWH_BOUND_LAW.csv",
        "needles": ["CWHL1722_1_operator_bound", "EXACT_NORM_BOUND_FORM"],
    },
    {
        "source_id": "SRC1723_3_1722_cwh_rows",
        "source_key": "1722_cwh_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1722_CWH_CURRENT_NORM_BOUND_ROWS.csv",
        "needles": ["CWH1722_0_CwH_current_norm_bound_candidate", "MISSING_OPERATOR_NORM"],
    },
    {
        "source_id": "SRC1723_4_1720_jh_row",
        "source_key": "1720_jh_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_NORM_FIRST_SOURCE_ROW.csv",
        "needles": ["JHN1720_0_observed_Hilbert_current_norm_candidate", "MISSING_PARENT_SIGNED_TAU_OBS"],
    },
    {
        "source_id": "SRC1723_5_1720_jh_theorem",
        "source_key": "1720_jh_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_CURRENT_DEFINITION_THEOREM.csv",
        "needles": ["JHT1720_4_verdict", "CONDITIONAL_THEOREM_ONLY_NORM_NOT_SOURCED"],
    },
    {
        "source_id": "SRC1723_6_1719_factor_bound",
        "source_key": "1719_factor_bound",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1719_NDOMAIN_FACTOR_BOUND_CONTRACT.csv",
        "needles": ["NF1719_0_factorized_bound", "MISSING_SOURCE_CURRENT_NORM"],
    },
    {
        "source_id": "SRC1723_7_1719_dpim",
        "source_key": "1719_dpim",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1719_DPIM_DOMAIN_OPERATOR_AUDIT.csv",
        "needles": ["DPO1719_4_verdict", "DPIM_DOMAIN_OPERATOR_NOT_SOURCED"],
    },
    {
        "source_id": "SRC1723_8_1719_ingredients",
        "source_key": "1719_ingredients",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1719_NUMERATOR_INGREDIENT_SOURCE_ROWS.csv",
        "needles": ["ING1719_0_JH_norm_candidate", "MISSING_SOURCE_CURRENT_NORM"],
    },
    {
        "source_id": "SRC1723_9_1608_tau",
        "source_key": "1608_tau",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1608_TAU_WEP_READOUT_CONTRACT.csv",
        "needles": ["TAU1608_4_verdict", "TAU_WEP_NOT_EVALUATED"],
    },
    {
        "source_id": "SRC1723_10_943_frame_residual",
        "source_key": "943_frame_residual",
        "source_path": RESIDUALS / "P8_Y5_R10_943_FRAME_RESIDUAL_SOURCE_PACK.csv",
        "needles": ["FRS943_6_nonHilbert_current_projection", "MISSING_NONHILBERT_CURRENT_SILENCE"],
    },
    {
        "source_id": "SRC1723_11_449_ward_contract",
        "source_key": "449_ward_contract",
        "source_path": RESIDUALS / "P8_source_current_Ward_universality_CONTRACT.csv",
        "needles": ["SC4_no_nonHilbert_source_current", "not_parent_derived"],
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
        "| " + " | ".join(str(row.get(col, "")).replace("\n", " ") for col in columns)
        + " |"
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


GUARD_REQUIREMENT_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "guard_id": "GJH1723_0_base_Hilbert_current",
        "stack_component": "base_J_H",
        "required_for_scoring": "parent-owned observed Hilbert current with norm, units, tau, annulus and source value/theorem",
        "current_status": "MISSING_PARENT_SIGNED_SOURCE_CURRENT_NORM",
        "source_anchor": "JHN1720_0;JHT1720_4",
        "if_missing": "J_H norm cannot feed N_domain",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "guard_id": "GJH1723_1_source_prefactor",
        "stack_component": "C_wH",
        "required_for_scoring": "source-prefactor correction is theorem-zero or source-backed finite bounded",
        "current_status": "CWH_BOUND_FORM_DERIVED_INPUTS_MISSING",
        "source_anchor": "CWHL1722_4;CWH1722_0",
        "if_missing": "weighted source current can change active gravitational source",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "guard_id": "GJH1723_2_tau_annulus_norm",
        "stack_component": "tau_A_norm",
        "required_for_scoring": "parent-signed tau/source-normal lock, compact exterior annulus, volume form, norm type and units",
        "current_status": "TAU_ANNULUS_NORM_MISSING",
        "source_anchor": "TAU1608_4;JHN1720_0",
        "if_missing": "neither base J_H nor C_wH has a common measurement space",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "guard_id": "GJH1723_3_nonHilbert_current",
        "stack_component": "q_nonH",
        "required_for_scoring": "non-Hilbert/current/boundary/readout source currents absent, exact zero-flux, projected silent, or finite bounded",
        "current_status": "NONHILBERT_CURRENT_SILENCE_NOT_PARENT_SIGNED",
        "source_anchor": "FRS943_6;SC4_no_nonHilbert_source_current",
        "if_missing": "ordinary Hilbert current may not be the full active source",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "guard_id": "GJH1723_4_dPiM_domain",
        "stack_component": "dPiM_domain",
        "required_for_scoring": "domain derivative operator norm C_DPiM and domain variation ||delta_D|| are theorem-zero or source-backed",
        "current_status": "DPIM_DOMAIN_OPERATOR_NOT_SOURCED",
        "source_anchor": "DPO1719_4;NF1719_0",
        "if_missing": "even a good J_H norm cannot produce a finite N_domain bound",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "guard_id": "GJH1723_5_mHref_R_eq_PPN",
        "stack_component": "downstream_GR_Newton",
        "required_for_scoring": "M_H_ref, R_eq, measured-GM calibration and PPN residual vector are resolved after J_H/N_domain",
        "current_status": "DOWNSTREAM_LOCAL_GR_DEBTS_OPEN",
        "source_anchor": "1719 claim gates; 1722 runner refusal",
        "if_missing": "no Newton/local-GR source-normalization promotion",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


JH_STACK_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "stack_id": "STACK1723_0_total_guarded_norm",
        "quantity": "J_H_total_norm_guarded",
        "formula": "||J_H_total||_A <= ||J_H||_A + C_wH + C_nonH",
        "base_JH": "MISSING_SOURCE_CURRENT_NORM",
        "C_wH": "MISSING_OPERATOR_NORM_OR_ZERO_THEOREM",
        "C_nonH": "MISSING_NONHILBERT_CURRENT_SILENCE_OR_BOUND",
        "tau_annulus_norm": "MISSING_TAU_AEXT_NORM_UNITS",
        "score_rule": "score only if every additive/source-current component is theorem-zero or source-backed finite with common norm/units",
        "current_status": "GUARDED_STACK_BLOCKED",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "stack_id": "STACK1723_1_Ndomain_guarded_bound",
        "quantity": "N_domain_guarded",
        "formula": "abs(N_domain) <= C_DPiM * ||delta_D|| * (||J_H||_A + C_wH + C_nonH)",
        "base_JH": "MISSING_SOURCE_CURRENT_NORM",
        "C_wH": "MISSING_CWH_BOUND",
        "C_nonH": "MISSING_NONHILBERT_BOUND",
        "tau_annulus_norm": "MISSING_SHARED_NORM_SPACE",
        "score_rule": "score only after C_DPiM, delta_D and all J_H_total pieces are sourced",
        "current_status": "NDOMAIN_GUARDED_BOUND_FORM_ONLY",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "stack_id": "STACK1723_2_zero_route",
        "quantity": "J_H_total_zero_corrections",
        "formula": "C_wH=C_nonH=0 and J_H norm finite if parent matter functor, no-Hom, current silence, tau/annulus and norm owners are signed",
        "base_JH": "CONDITIONAL_ONLY",
        "C_wH": "ZERO_ROUTE_NOT_PARENT_SIGNED",
        "C_nonH": "ZERO_ROUTE_NOT_PARENT_SIGNED",
        "tau_annulus_norm": "NOT_PARENT_SIGNED",
        "score_rule": "zero route cannot be used until every premise is parent-signed",
        "current_status": "ZERO_ROUTE_CONDITIONAL_ONLY",
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


SCORE_REFUSAL_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1723_0_base_JH_norm",
        "quantity": "base observed Hilbert current norm",
        "runner_decision": "REFUSE_SCORING",
        "refusal_reasons": "MISSING_NORM_TYPE;MISSING_A_EXT;MISSING_TAU_LOCK;MISSING_SOURCE_CURRENT_VALUE_OR_THEOREM;MISSING_UNITS",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1723_1_CwH",
        "quantity": "source-prefactor weighted-current correction",
        "runner_decision": "REFUSE_SCORING",
        "refusal_reasons": "MISSING_C_TW;MISSING_DELTA_W_NORM;MISSING_COMPONENT_STRESS_TENSOR;MISSING_TAU;MISSING_ANNULUS",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1723_2_nonHilbert",
        "quantity": "non-Hilbert/current/readout source correction",
        "runner_decision": "REFUSE_SCORING",
        "refusal_reasons": "MISSING_NONHILBERT_CURRENT_SILENCE;MISSING_Q_NONH_BOUND;MISSING_ZERO_FLUX_PROJECTION",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1723_3_Ndomain",
        "quantity": "N_domain guarded bound",
        "runner_decision": "BLOCKED_NO_CLAIM",
        "refusal_reasons": "JH_TOTAL_NORM_NOT_READY;DPIM_OPERATOR_NORM_MISSING;DELTA_D_MISSING;ANNULUS_MISSING",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "run_id": "RUN1723_4_Newton_GR",
        "quantity": "Newton/local-GR reopening",
        "runner_decision": "BLOCKED_NO_CLAIM",
        "refusal_reasons": "JH_NDOMAIN_CHAIN_BLOCKED;M_H_REF_MISSING;R_EQ_MISSING;PPN_VECTOR_OPEN",
        "accepted_for_scoring": no(),
        "score_ready": no(),
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


INPUT_PRIORITY_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "priority_id": "PRI1723_0_shared_norm_space",
        "target_input": "A_ext + norm_type + volume form + units",
        "why_first": "base J_H, C_wH, C_nonH and N_domain all need a common norm space",
        "current_status": "MISSING",
        "next_action": "derive or declare compact exterior annulus/norm owner as nonclaim; no scoring yet",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "priority_id": "PRI1723_1_tau_lock",
        "target_input": "tau_obs/source-normal lock",
        "why_first": "every source current is contracted with tau and compared through the same observed frame",
        "current_status": "TAU_WEP_NOT_EVALUATED",
        "next_action": "source parent tau lock or keep tau as explicit missing input",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "priority_id": "PRI1723_2_CwH_operator",
        "target_input": "C_Tw operator norm",
        "why_first": "source-prefactor correction cannot be bounded without the component-current projection operator",
        "current_status": "MISSING_OPERATOR_NORM",
        "next_action": "build C_Tw row only after norm space and component basis exist",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "priority_id": "PRI1723_3_nonHilbert",
        "target_input": "q_nonH zero/bound",
        "why_first": "Hilbert current may not exhaust active source current",
        "current_status": "MISSING_NONHILBERT_CURRENT_SILENCE",
        "next_action": "derive current silence or create q_nonH finite source row",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


RUNNER_CONTRACT_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "contract_id": "RC1723_0_no_partial_score",
        "rule": "do not score J_H_total if any additive source-current component is missing",
        "enforced_by": "RUN1723_0 through RUN1723_4",
        "status": "ACTIVE",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "contract_id": "RC1723_1_no_norm_mismatch",
        "rule": "do not combine base J_H, C_wH, C_nonH or N_domain unless the same A_ext, tau, volume form, norm type and units are declared",
        "enforced_by": "GJH1723_2_tau_annulus_norm",
        "status": "ACTIVE",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "contract_id": "RC1723_2_no_local_GR_shortcut",
        "rule": "do not reopen Newton/local-GR until J_H_total, dPiM/domain, M_H_ref, R_eq and PPN vector are closed",
        "enforced_by": "RUN1723_4_Newton_GR",
        "status": "ACTIVE",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


DECISION_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "decision_id": "DEC1723_0_guarded_stack",
        "decision": "J_H_total stack built as refusal schema",
        "because": "base J_H, source-prefactor, non-Hilbert, tau/annulus and dPiM dependencies are all open",
        "next_action": "do not score; fill shared norm/tau/annulus owner or first finite source-current input",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "decision_id": "DEC1723_1_best_next",
        "decision": "target common annulus/norm/tau owner first",
        "because": "the same missing norm space blocks base J_H, C_wH, q_nonH and N_domain",
        "next_action": "1724 should derive the compact exterior annulus/norm/tau owner, or write the first source-ready nonclaim row",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


NEXT_TARGET_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "route_id": "NEXT1723_0_primary",
        "next_target": "1724-Y5-R2FR-compact-annulus-norm-tau-owner-or-first-source-row.md",
        "script": "scripts/Y5_R2FR_compact_annulus_norm_tau_owner_or_first_source_row.py",
        "objective": "derive the common A_ext/norm/tau owner used by base J_H, C_wH, C_nonH and N_domain; if not, create the first source-ready nonclaim row",
        "selection_status": "selected",
        "success_condition": "common norm space is parent-owned or a complete nonclaim schema exists with A_ext, norm, tau, volume form, units and source paths",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "route_id": "NEXT1723_1_parallel_nonHilbert",
        "next_target": "1724b-Y5-R2FR-nonHilbert-current-silence-or-qnonH-source-row.md",
        "script": "scripts/Y5_R2FR_nonHilbert_current_silence_or_qnonH_source_row.py",
        "objective": "derive non-Hilbert current silence or add q_nonH finite source row",
        "selection_status": "held_parallel",
        "success_condition": "q_nonH is theorem-zero or bounded in the same norm stack",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


CLAIM_GATE_ROWS = [
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1723_0_JH_total",
        "claim": "guarded J_H_total norm is score-ready",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "base J_H, C_wH, C_nonH, tau/annulus/norm and units remain missing",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1723_1_Ndomain",
        "claim": "N_domain guarded bound is finite",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "J_H_total, C_DPiM, delta_D and annulus are not sourced",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
    {
        "branch_id": BRANCH_ID,
        "claim_id": "CG1723_2_Newton_local_GR",
        "claim": "Newton/local-GR source-normalization gate can reopen",
        "status": "BLOCKED_NO_CLAIM",
        "reason": "J_H/N_domain chain plus M_H_ref, R_eq and PPN vector remain open",
        "valid_for_claim": no(),
        "claim_allowed": no(),
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1723_SOURCE_REGISTER.csv",
    "guard_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1723_GUARD_REQUIREMENT_MATRIX.csv",
    "jh_stack": RESIDUALS / "P8_Y5_PARENT_QLOC_1723_GUARDED_JH_NORM_STACK.csv",
    "score_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1723_SCORE_REFUSAL.csv",
    "input_priority": RESIDUALS / "P8_Y5_PARENT_QLOC_1723_INPUT_PRIORITY_LEDGER.csv",
    "runner_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1723_RUNNER_CONTRACT.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1723_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1723_NEXT_TARGET.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1723_CLAIM_GATE.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1723_VALIDATION.csv",
}


COPY_MAP = {
    "guard_matrix": "R2FR_guard_requirement_matrix_1723.csv",
    "jh_stack": "R2FR_guarded_JH_norm_stack_1723.csv",
    "score_refusal": "R2FR_score_refusal_1723.csv",
    "input_priority": "R2FR_input_priority_ledger_1723.csv",
    "runner_contract": "R2FR_runner_contract_1723.csv",
    "decision": "R2FR_decision_ledger_1723.csv",
    "next_target": "R2FR_next_target_1723.csv",
    "claim_gate": "R2FR_claim_gate_1723.csv",
}


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register(),
        "guard_matrix": GUARD_REQUIREMENT_ROWS,
        "jh_stack": JH_STACK_ROWS,
        "score_refusal": SCORE_REFUSAL_ROWS,
        "input_priority": INPUT_PRIORITY_ROWS,
        "runner_contract": RUNNER_CONTRACT_ROWS,
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1723_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1723_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {"valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring"}
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1723_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1723_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1723*"):
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
    guard_rows = rows_map["guard_matrix"]
    stack_rows = rows_map["jh_stack"]
    score_rows = rows_map["score_refusal"]
    priority_rows = rows_map["input_priority"]
    contract_rows = rows_map["runner_contract"]
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
        check("VAL1723_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1723_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "required source needles are present", "one or more required source needles missing"),
        check(
            "VAL1723_2_1722_handoff_preserved",
            any(row["source_key"] == "1722_doc" and row["needles_present"] == "True" for row in source_rows),
            "1722 selected guarded J_H norm stack route",
            "1722 handoff missing",
        ),
        check(
            "VAL1723_3_guard_components_present",
            {row["stack_component"] for row in guard_rows} >= {"base_J_H", "C_wH", "tau_A_norm", "q_nonH", "dPiM_domain"},
            "guard matrix includes base J_H, C_wH, tau/norm, non-Hilbert and dPiM components",
            "guard matrix missing required component",
        ),
        check(
            "VAL1723_4_stack_bound_present",
            any(row["stack_id"] == "STACK1723_1_Ndomain_guarded_bound" and "C_DPiM" in row["formula"] for row in stack_rows),
            "guarded N_domain bound is present",
            "guarded N_domain bound missing",
        ),
        check(
            "VAL1723_5_stack_blocked",
            all(row["score_ready"] == "False" and row["valid_for_claim"] == "False" for row in stack_rows),
            "guarded stack rows remain blocked/nonclaim",
            "one or more guarded stack rows became score-ready",
        ),
        check(
            "VAL1723_6_score_refusals",
            len(score_rows) == 5 and all(row["accepted_for_scoring"] == "False" for row in score_rows),
            "score refusals cover base J_H, C_wH, non-Hilbert, N_domain and Newton/GR",
            "score refusals incomplete or scoring allowed",
        ),
        check(
            "VAL1723_7_priority_norm_first",
            any(row["priority_id"] == "PRI1723_0_shared_norm_space" for row in priority_rows),
            "shared norm/tau/annulus priority is recorded",
            "shared norm priority missing",
        ),
        check(
            "VAL1723_8_runner_contract_active",
            len(contract_rows) == 3 and all(row["status"] == "ACTIVE" for row in contract_rows),
            "runner contracts are active",
            "runner contracts missing or inactive",
        ),
        check(
            "VAL1723_9_decision_next",
            any(row["decision_id"] == "DEC1723_1_best_next" and "annulus" in row["next_action"] for row in decision_rows),
            "decision selects compact annulus/norm/tau owner next",
            "decision does not select shared norm/tau/annulus route",
        ),
        check(
            "VAL1723_10_next_selected",
            any(row["route_id"] == "NEXT1723_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "next target selects compact annulus/norm/tau owner",
            "next target missing selected primary route",
        ),
        check(
            "VAL1723_11_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check("VAL1723_12_csv_parse", parsed_ok, "all generated 1723 CSVs parse", "one or more generated 1723 CSVs failed to parse"),
        check("VAL1723_13_no_claim_flags", no_claim_flags(rows_map), "all generated scoring and claim flags remain false", "one or more generated flags enabled a claim"),
        check("VAL1723_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1723_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1723_16_formalization_untouched", formalization_untouched(), "no 1723 outputs found under formalization-workbench", "1723 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1723_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1723 guarded JH norm stack validation" if overall else "one or more 1723 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1723 builds the guarded `J_H_total` norm stack that 1722 selected.",
        "- The stack is deliberately a refusal schema: `||J_H_total||_A <= ||J_H||_A + C_wH + C_nonH`, and `abs(N_domain) <= C_DPiM ||delta_D|| (||J_H||_A + C_wH + C_nonH)`.",
        "- Nothing scores until the base Hilbert current, source-prefactor correction, non-Hilbert current, tau/annulus/norm/units, and dPiM/domain factors are theorem-zero or source-backed finite.",
        "- This is a guardrail improvement: it prevents the GR/Newton route from silently using a clean Hilbert current while `w_A`, non-Hilbert current, tau, annulus or dPiM debts remain open.",
        "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, source-normalization, `J_H`-norm, `N_domain`, or public claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Guard Requirement Matrix",
        markdown_table(rows_map["guard_matrix"], ["guard_id", "stack_component", "required_for_scoring", "current_status", "if_missing", "score_ready"]),
        "",
        "## Guarded JH Norm Stack",
        markdown_table(rows_map["jh_stack"], ["stack_id", "quantity", "formula", "current_status", "score_ready", "valid_for_claim"]),
        "",
        "## Score Refusal",
        markdown_table(rows_map["score_refusal"], ["run_id", "quantity", "runner_decision", "refusal_reasons", "accepted_for_scoring", "claim_allowed"]),
        "",
        "## Input Priority Ledger",
        markdown_table(rows_map["input_priority"], ["priority_id", "target_input", "why_first", "current_status", "next_action"]),
        "",
        "## Runner Contract",
        markdown_table(rows_map["runner_contract"], ["contract_id", "rule", "enforced_by", "status"]),
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
        "1723 does not derive local GR, but it makes the path to local GR much less slippery. The active source norm now has to carry every relevant source-current debt explicitly: the ordinary Hilbert piece, the source-prefactor piece, and the non-Hilbert/readout piece, all in one common norm space. The next high-leverage derivation target is therefore the shared compact exterior annulus/norm/tau owner, because that one missing object blocks almost every finite and theorem-zero route at once.",
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
    doc_path = ROOT / "1723-Y5-R2FR-guarded-JH-norm-stack-or-CwH-input-source.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1723_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1723 validation FAIL")
    print("1723 validation PASS")


if __name__ == "__main__":
    main()

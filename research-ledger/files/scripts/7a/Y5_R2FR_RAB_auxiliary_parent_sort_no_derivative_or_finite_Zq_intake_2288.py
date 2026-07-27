from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_RAB_AUXILIARY_PARENT_SORT_NO_DERIVATIVE_OR_FINITE_ZQ_INTAKE_2288"
START_TS = datetime.now(timezone.utc).timestamp()
DOC = ROOT / "2288-Y5-R2FR-RAB-auxiliary-parent-sort-no-derivative-or-finite-Zq-intake.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2288_00_2287_doc",
        "source_key": "2287_selector_handoff",
        "source_path": ROOT / "2287-Y5-R2FR-q-sector-parent-coefficient-extraction-or-selector-fork.md",
        "needles": ["AUXILIARY_COMPATIBILITY_IS_BEST_ZERO_ROUTE_BUT_UNSIGNED", "FINITE_BRANCH_RETAINED", "2288-Y5-R2FR"],
        "role": "current q-sector selector handoff into auxiliary/no-derivative hinge",
    },
    {
        "source_id": "SRC2288_01_2287_validation",
        "source_key": "2287_validation",
        "source_path": OUT / "P8_Y5_BRR545_2287_VALIDATION.csv",
        "needles": ["VAL2287_OVERALL", "PASS"],
        "role": "confirms 2287 passed before 2288",
    },
    {
        "source_id": "SRC2288_02_2287_next",
        "source_key": "2287_next",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2287_NEXT_TARGET.csv",
        "needles": ["NEXT2287_0_primary", "finite Z_q/M_q^2/j_q/J_q/B_R intake rows", "selected"],
        "role": "declares 2288 objective",
    },
    {
        "source_id": "SRC2288_03_2238_theta",
        "source_key": "2238_theta_omega_fill",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2238_THETA_OMEGA_FILL.csv",
        "needles": ["TO2238_0_theta_R", "TO2238_1_Omega_R", "EXACT_IF_AUXILIARY_BLOCK_AND_NO_DERIVATIVE_GRAMMAR_ARE_PARENT_SIGNED"],
        "role": "partial auxiliary-block theta/Omega fill",
    },
    {
        "source_id": "SRC2288_04_2238_vr",
        "source_key": "2238_vR_tangency",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2238_VR_TANGENCY_AUDIT.csv",
        "needles": ["VR2238_1_constraint_tangency", "FAILS_OFF_SHELL_FIRST_CLASS_TANGENCY", "DEMOTE_TO_SECOND_CLASS_ELIMINATION_ROUTE"],
        "role": "rejects first-class vertical gauge promotion",
    },
    {
        "source_id": "SRC2288_05_2238_elimination",
        "source_key": "2238_second_class",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2238_SECOND_CLASS_ELIMINATION_CONDITIONS.csv",
        "needles": ["ELIM2238_1_E_R", "PASS_ONLY_IF_SOURCES_ZERO", "ELIM2238_4_local_gr"],
        "role": "second-class elimination conditions",
    },
    {
        "source_id": "SRC2288_06_2238_validation",
        "source_key": "2238_validation",
        "source_path": OUT / "P8_Y5_BRR545_2238_VALIDATION.csv",
        "needles": ["VAL2238_OVERALL", "PASS"],
        "role": "confirms theta/Omega/vR checkpoint passed as nonclaim",
    },
    {
        "source_id": "SRC2288_07_2239_protection",
        "source_key": "2239_protection_audit",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2239_PROTECTION_PROOF_AUDIT.csv",
        "needles": ["PROT2239_0_JR_matter", "PROT2239_4_joint", "JOINT_PROTECTION_NOT_CLOSED"],
        "role": "source/boundary/readout/operator leak audit",
    },
    {
        "source_id": "SRC2288_08_2239_joint",
        "source_key": "2239_joint_gate",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2239_JB_READOUT_OPERATOR_JOINT_GATE.csv",
        "needles": ["JOINT2239_0_eliminate_auxiliary", "JOINT2239_3_verdict", "JOINT_PROTECTION_NOT_CLOSED"],
        "role": "joint gate blocks local claim if any leak survives",
    },
    {
        "source_id": "SRC2288_09_2239_validator",
        "source_key": "2239_validator_summary",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2239_FINITE_ZR_VALIDATOR_SUMMARY.csv",
        "needles": ["VS2239_0_scan_counts", "NO_ACCEPTED_SOURCE_READY_ROWS"],
        "role": "finite Z_R validator has no accepted source-ready rows",
    },
    {
        "source_id": "SRC2288_10_2239_validation",
        "source_key": "2239_validation",
        "source_path": OUT / "P8_Y5_BRR545_2239_VALIDATION.csv",
        "needles": ["VAL2239_OVERALL", "PASS"],
        "role": "confirms protection/validator checkpoint passed as nonclaim",
    },
    {
        "source_id": "SRC2288_11_2240_contract",
        "source_key": "2240_parent_contract",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2240_PARENT_PROTECTION_CONTRACT.csv",
        "needles": ["CON2240_0_parent_sorts", "CON2240_6_joint_contract", "CONTRACT_WRITTEN_NOT_SIGNED"],
        "role": "single protection contract sufficient if parent-signed",
    },
    {
        "source_id": "SRC2288_12_2240_theorem",
        "source_key": "2240_conditional_theorem",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2240_CONDITIONAL_THEOREM.csv",
        "needles": ["THM2240_0_statement", "EXACT_IF_CONTRACT_PARENT_SIGNED", "not a claim"],
        "role": "exact conditional theorem under unsigned contract",
    },
    {
        "source_id": "SRC2288_13_2240_acquisition",
        "source_key": "2240_acquisition_queue",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2240_LIVE_SOURCE_ACQUISITION_QUEUE.csv",
        "needles": ["ACQ2240_1_ZR", "ACQ2240_3_JR", "ACQ2240_8_tau_orbital"],
        "role": "finite residual coefficient/acquisition queue",
    },
    {
        "source_id": "SRC2288_14_2240_validation",
        "source_key": "2240_validation",
        "source_path": OUT / "P8_Y5_BRR545_2240_VALIDATION.csv",
        "needles": ["VAL2240_OVERALL", "PASS"],
        "role": "confirms parent-protection contract checkpoint passed as nonclaim",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2288_SOURCE_REGISTER.csv",
    "auxiliary_block": OUT / "P8_Y5_PARENT_QLOC_2288_AUXILIARY_BLOCK_INTEGRATION.csv",
    "contract_status": OUT / "P8_Y5_PARENT_QLOC_2288_PARENT_CONTRACT_STATUS.csv",
    "finite_intake": OUT / "P8_Y5_PARENT_QLOC_2288_FINITE_ZQ_INTAKE_GATE.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2288_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2288_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2288_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2288_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2288_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2288_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_contract": (OUTPUTS["contract_status"], QUEUE / "JR2288_PARENT_CONTRACT_STATUS_NONCLAIM.csv"),
    "queue_finite_intake": (OUTPUTS["finite_intake"], QUEUE / "JR2288_FINITE_ZQ_INTAKE_GATE_NONCLAIM.csv"),
    "branch_wep_refusal": (OUTPUTS["refusal"], MICROSCOPE / "RAB_auxiliary_or_finite_Zq_refusal_2288.csv"),
    "beta_docs": (OUTPUTS["auxiliary_block"], BETA_DOCS / "RAB_AUXILIARY_OR_FINITE_ZQ_2288_NONCLAIM.csv"),
}


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(value) for key, value in row.items()})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def validation_pass(path: Path) -> bool:
    if not path.exists() or not csv_parses(path):
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key, "").upper() == "PASS" for row in overall_rows)
    return all(row.get(result_key, "").upper() == "PASS" for row in rows)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def ignored_environment_path(path: Path) -> bool:
    ignored_parts = {".venv", ".venv-score", "__pycache__", "site-packages", ".git"}
    return any(part in ignored_parts for part in path.parts)


def formalization_has_2288_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    for candidate in FORMALIZATION.rglob("*2288*"):
        if candidate.is_file() and not ignored_environment_path(candidate.relative_to(FORMALIZATION)):
            return True
    return False


def formalization_touched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return False
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file() and not ignored_environment_path(candidate.relative_to(FORMALIZATION)):
            if candidate.stat().st_mtime >= START_TS:
                return True
    return False


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    def cell(value: Any) -> str:
        return stringify(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        source_path = Path(source["source_path"])
        source_text = read_text(source_path)
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": source_path,
                "exists": source_path.exists(),
                "needles": "; ".join(needles),
                "needles_present": all(needle in source_text for needle in needles),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def auxiliary_block_rows() -> list[dict[str, Any]]:
    return [
        {
            "block_id": "AUX2288_0_theta_omega",
            "object": "theta_R, Omega_R, Pi_R^n",
            "current_result": "ZERO_INSIDE_AUXILIARY_BLOCK_CONDITIONAL",
            "mathematical_content": "if R_AB and Lambda_R enter only algebraically, no derivative momentum or symplectic current is generated",
            "what_it_buys": "supports second-class elimination route without a plateau axiom",
            "blocking_gap": "auxiliary block and no-derivative grammar are not parent-derived",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "block_id": "AUX2288_1_vR_first_class",
            "object": "v_R vertical generator",
            "current_result": "REJECT_CURRENT_FIRST_CLASS_PROMOTION",
            "mathematical_content": "pure R_AB shifts fail compatibility-surface tangency; compatibility-preserving shifts are not q-vertical",
            "what_it_buys": "prevents us from claiming gauge-null magic where only algebraic elimination exists",
            "blocking_gap": "no off-shell first-class q-vertical generator",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "block_id": "AUX2288_2_second_class",
            "object": "second-class compatibility elimination",
            "current_result": "BEST_CONDITIONAL_ROUTE_RETAINED",
            "mathematical_content": "E_Lambda fixes R_AB=C_AB; E_R solves Lambda_R=0 only if J_R, B_R, and readout_regen vanish",
            "what_it_buys": "the cleanest route to local GR if protections close jointly",
            "blocking_gap": "source, boundary, readout, and operator protections unsigned",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "block_id": "AUX2288_3_finite_escape",
            "object": "finite q/Z_q branch",
            "current_result": "MANDATORY_IF_PROTECTION_FAILS",
            "mathematical_content": "if q is physical or derivative constructors survive, finite Z_q/M_q^2/j_q/J_q/B_R must be sourced and tested",
            "what_it_buys": "keeps the framework empirically honest rather than forcing exact GR by declaration",
            "blocking_gap": "no accepted finite source-ready rows",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def contract_status_rows() -> list[dict[str, Any]]:
    clauses = [
        ("CON2288_0_parent_sorts", "typed parent field/sort list", "decides whether R_AB/q is auxiliary compatibility data or a physical scalar", "SCHEMA_WRITTEN_NOT_DERIVED", "derive from motion/time/space primitives"),
        ("CON2288_1_action_image", "ParentGenerate image/exhaustion", "prevents independent R_AB kinetic, source, and boundary terms", "SCHEMA_WRITTEN_NOT_DERIVED", "prove object-language exhaustion"),
        ("CON2288_2_matter_descent", "matter descends through public quotient fields", "sets J_R=0 or gives finite source row if false", "UNSIGNED", "prove no material/readout marker depends on R_AB"),
        ("CON2288_3_boundary_descent", "boundary/corner terms descend through public boundary data", "sets B_R/Pi_R/Q_R=0 or gives finite boundary row if false", "UNSIGNED", "prove source-worldtube and corner no-hair"),
        ("CON2288_4_readout_closure", "readout/effective reduction preserves parent image", "prevents readout_regen and tau leakage", "UNSIGNED", "prove tree-level silence survives readout"),
        ("CON2288_5_operator_exclusion", "no D R_AB, D Lambda_R, vertical metric, or vertical connection", "sets Z_q=0 without adding a plateau axiom", "BLOCKED_EXACT_CONDITIONAL", "derive no-derivative grammar from primitives"),
        ("CON2288_6_joint_contract", "all clauses close as one contract", "kills J_R, B_R, readout_regen, and Z_q together", "CONTRACT_WRITTEN_NOT_PARENT_SIGNED", "one parent theorem binding all clauses"),
    ]
    return [
        {
            "contract_id": contract_id,
            "clause": clause,
            "effect_if_signed": effect,
            "current_status": status,
            "missing_for_claim": missing,
            "parent_signed": False,
            "valid_for_claim": False,
        }
        for contract_id, clause, effect, status, missing in clauses
    ]


def finite_intake_rows() -> list[dict[str, Any]]:
    entries = [
        ("FIN2288_0_Zq", "Z_q", "internal_theory", "operator exclusion theorem-zero or finite gradient coefficient with units", "R10;PPN;clock;orbital", "MISSING_ZQ_THEOREM_OR_COEFFICIENT"),
        ("FIN2288_1_Mq2", "M_q^2", "internal_theory", "parent Hessian/mass gap in same q normalization", "R10;PPN;clock;orbital", "MISSING_MQ2_SOURCE"),
        ("FIN2288_2_jq", "j_q/J_q", "internal_theory", "matter descent zero theorem or finite source coupling", "WEP;R10;PPN;clock", "MISSING_JQ_SOURCE_OR_ZERO"),
        ("FIN2288_3_boundary", "B_R/Pi_q/Q_R", "internal_theory", "boundary no-hair theorem or finite boundary momentum", "R10;PPN;orbital", "MISSING_BOUNDARY_SOURCE_OR_ZERO"),
        ("FIN2288_4_tau_R10", "tau_R10", "mixed_internal_external", "projection from finite q to alpha(lambda) plus external short-range bound", "R10", "MISSING_TAU_R10_PROJECTION"),
        ("FIN2288_5_tau_PPN", "tau_PPN", "mixed_internal_external", "projection from finite q to gamma/beta residual vector", "PPN", "MISSING_TAU_PPN_PROJECTION"),
        ("FIN2288_6_tau_clock", "tau_clock", "mixed_internal_external", "projection from finite q to clock/readout observable", "clock", "MISSING_TAU_CLOCK_PROJECTION"),
        ("FIN2288_7_tau_orbital", "tau_orbital", "mixed_internal_external", "projection from finite q to acceleration/timing observable", "orbital", "MISSING_TAU_ORBITAL_PROJECTION"),
    ]
    return [
        {
            "intake_id": intake_id,
            "target": target,
            "source_class": source_class,
            "needed_evidence": evidence,
            "arena_projection": arena,
            "current_status": status,
            "ready_for_raw": False,
            "ready_for_accepted": False,
            "score_ready": False,
            "valid_for_claim": False,
        }
        for intake_id, target, source_class, evidence, arena, status in entries
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"claim_id": "CG2288_0_auxiliary_block", "claim": "theta/Omega auxiliary block supports second-class route", "gate_pass": True, "reason": "partial fill exists only inside unsigned auxiliary/no-derivative block", "claim_allowed": False, "valid_for_claim": False},
        {"claim_id": "CG2288_1_first_class_vR", "claim": "v_R is a true first-class vertical gauge generator", "gate_pass": False, "reason": "2238 tangency audit rejects current first-class promotion", "claim_allowed": False, "valid_for_claim": False},
        {"claim_id": "CG2288_2_contract_signed", "claim": "parent protection contract is derived from primitives", "gate_pass": False, "reason": "contract is written and sufficient but not parent-signed", "claim_allowed": False, "valid_for_claim": False},
        {"claim_id": "CG2288_3_Zq_zero", "claim": "Z_q=0 is derived without plateau axiom", "gate_pass": False, "reason": "operator exclusion remains exact conditional", "claim_allowed": False, "valid_for_claim": False},
        {"claim_id": "CG2288_4_finite_rows", "claim": "finite residual source rows are score-ready", "gate_pass": False, "reason": "no raw/accepted source-backed rows are ready", "claim_allowed": False, "valid_for_claim": False},
        {"claim_id": "CG2288_5_local_GR", "claim": "local GR/Newton recovery is derived", "gate_pass": False, "reason": "neither signed zero theorem nor finite residual workflow is complete", "claim_allowed": False, "valid_for_claim": False},
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {"refusal_id": "REF2288_0_auxiliary_equals_claim", "attempted_claim": "claim local GR because the auxiliary block has theta_R=Omega_R=0 conditionally", "runner_result": "REFUSED_CONDITIONAL_BLOCK_NOT_PARENT_SIGNATURE", "blocked_by": "parent sort/no-derivative/object-language proof missing", "score_eligible": False, "valid_for_claim": False},
        {"refusal_id": "REF2288_1_first_class_language", "attempted_claim": "describe R_AB as a first-class vertical gauge direction", "runner_result": "REFUSED_TANGENCY_FAILURE", "blocked_by": "pure R_AB shifts fail compatibility tangency", "score_eligible": False, "valid_for_claim": False},
        {"refusal_id": "REF2288_2_separate_zero_conditions", "attempted_claim": "spend local-GR credit from separate unsigned J_R/B_R/readout/Z_q zero clauses", "runner_result": "REFUSED_NEEDS_JOINT_CONTRACT", "blocked_by": "one leak is enough to regenerate finite q residuals", "score_eligible": False, "valid_for_claim": False},
        {"refusal_id": "REF2288_3_score_templates", "attempted_claim": "score docs/template rows as finite residual predictions", "runner_result": "REFUSED_NO_ACCEPTED_SOURCE_ROWS", "blocked_by": "source path, anchor, units, normalization, and arena projection are absent", "score_eligible": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2288_0_progress",
            "decision": "SECOND_CLASS_ROUTE_CLARIFIED",
            "reason": "theta/Omega/Pi_Rn vanish conditionally for an algebraic auxiliary block, while first-class v_R promotion fails",
            "next_action": "try deriving the whole parent protection contract from motion/time/space primitives",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2288_1_contract",
            "decision": "PARENT_PROTECTION_CONTRACT_IS_THE_HINGE",
            "reason": "the single contract would jointly kill J_R, B_R, readout_regen, and Z_q without a plateau axiom",
            "next_action": "prove contract clauses together or demote to finite residual source acquisition",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2288_2_finite",
            "decision": "FINITE_ZQ_INTAKE_REMAINS_MANDATORY_FALLBACK",
            "reason": "if the contract cannot be derived, MTS must provide real finite coefficients/projections and face tests",
            "next_action": "fill first live nonclaim finite row only with source path, anchor, units, normalization, and arena projection",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2288_3_claim_policy",
            "decision": "KEEP_PRIVATE_NONCLAIM",
            "reason": "2288 integrates the hinge and refuses public local-GR credit",
            "next_action": "no GitHub action",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "NEXT2288_0_primary",
            "next_target": "2289-Y5-R2FR-parent-protection-contract-derivation-from-MTS-primitives-or-first-live-Zq-row.md",
            "script": "scripts/Y5_R2FR_parent_protection_contract_derivation_from_MTS_primitives_or_first_live_Zq_row_2289.py",
            "objective": "attempt to derive the typed parent protection contract from motion/time/space primitives; if it cannot be derived, fill the first source-backed nonclaim finite Z_q/M_q^2/j_q/B_R/tau row without scoring it",
            "selection_status": "selected",
            "success_condition": "either the parent protection contract is derived as one theorem, or the first finite residual row is live-quality with source path, anchor, units, normalization, and arena projection while valid_for_claim remains false",
            "valid_for_claim": False,
        }
    ]


def generated_claim_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    guarded_keys = {
        "parent_signed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "score_eligible",
        "ready_for_raw",
        "ready_for_accepted",
    }
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in guarded_keys and value.strip().lower() not in false_values:
                    return False
    return True


def copy_branch_files() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, (source_path, target_path) in COPY_TARGETS.items():
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "copy_id": copy_id,
                "source_path": source_path,
                "target_path": target_path,
                "target_exists": target_path.exists(),
                "target_parses": csv_parses(target_path),
                "reason": "branch copy for 2288 auxiliary-parent-sort/no-derivative or finite-Zq intake checkpoint",
            }
        )
    return rows


def validation_rows(all_generated_before_validation: list[Path], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    aux_rows = read_csv(OUTPUTS["auxiliary_block"])
    contract_rows = read_csv(OUTPUTS["contract_status"])
    finite_rows = read_csv(OUTPUTS["finite_intake"])
    claim_rows = read_csv(OUTPUTS["claim_gates"])
    refusal_runner_rows = read_csv(OUTPUTS["refusal"])
    decision_rows_local = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])

    contract_ids = {row["contract_id"] for row in contract_rows}
    finite_targets = {row["target"] for row in finite_rows}
    checks = [
        ("VAL2288_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        ("VAL2288_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        (
            "VAL2288_2_prior_validations",
            validation_pass(OUT / "P8_Y5_BRR545_2287_VALIDATION.csv")
            and validation_pass(OUT / "P8_Y5_BRR545_2238_VALIDATION.csv")
            and validation_pass(OUT / "P8_Y5_BRR545_2239_VALIDATION.csv")
            and validation_pass(OUT / "P8_Y5_BRR545_2240_VALIDATION.csv"),
            "2287, 2238, 2239, and 2240 validation files pass overall",
        ),
        (
            "VAL2288_3_auxiliary_clarified",
            any(row["current_result"] == "ZERO_INSIDE_AUXILIARY_BLOCK_CONDITIONAL" for row in aux_rows)
            and any(row["current_result"] == "REJECT_CURRENT_FIRST_CLASS_PROMOTION" for row in aux_rows)
            and any(row["current_result"] == "BEST_CONDITIONAL_ROUTE_RETAINED" for row in aux_rows),
            "auxiliary route is clarified as second-class conditional, not first-class gauge",
        ),
        (
            "VAL2288_4_contract_complete_unsigned",
            {
                "CON2288_0_parent_sorts",
                "CON2288_1_action_image",
                "CON2288_2_matter_descent",
                "CON2288_3_boundary_descent",
                "CON2288_4_readout_closure",
                "CON2288_5_operator_exclusion",
                "CON2288_6_joint_contract",
            }.issubset(contract_ids)
            and all(row["parent_signed"] == "False" for row in contract_rows),
            "parent protection contract clauses are complete and unsigned",
        ),
        (
            "VAL2288_5_finite_intake_complete_blocked",
            {"Z_q", "M_q^2", "j_q/J_q", "B_R/Pi_q/Q_R", "tau_R10", "tau_PPN", "tau_clock", "tau_orbital"}.issubset(finite_targets)
            and all(row["ready_for_raw"] == "False" and row["score_ready"] == "False" for row in finite_rows),
            "finite Zq intake covers coefficient and arena projections but remains blocked",
        ),
        (
            "VAL2288_6_claim_gates_blocked",
            any(row["claim_id"] == "CG2288_5_local_GR" and row["gate_pass"] == "False" for row in claim_rows)
            and all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in claim_rows),
            "local GR/Newton and finite scoring claims remain blocked",
        ),
        (
            "VAL2288_7_refusal_runner",
            {"REFUSED_CONDITIONAL_BLOCK_NOT_PARENT_SIGNATURE", "REFUSED_TANGENCY_FAILURE", "REFUSED_NEEDS_JOINT_CONTRACT", "REFUSED_NO_ACCEPTED_SOURCE_ROWS"}.issubset(
                {row["runner_result"] for row in refusal_runner_rows}
            ),
            "refusal runner blocks conditional promotion, first-class language, separate zeros, and template scoring",
        ),
        (
            "VAL2288_8_decision_next",
            any(row["decision"] == "PARENT_PROTECTION_CONTRACT_IS_THE_HINGE" for row in decision_rows_local)
            and any(row["next_target"] == "2289-Y5-R2FR-parent-protection-contract-derivation-from-MTS-primitives-or-first-live-Zq-row.md" for row in next_rows),
            "2289 parent contract derivation or first live finite row is selected next",
        ),
        ("VAL2288_9_csv_parse", all(csv_parses(path) for path in all_generated_before_validation), "all generated 2288 CSVs parse before validation file"),
        ("VAL2288_10_no_claim_flags", generated_claim_flags_false(all_generated_before_validation), "all generated claim/score/raw/accepted flags remain false"),
        ("VAL2288_11_branch_copies", all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows), "branch/queue copies exist and parse"),
        ("VAL2288_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL2288_13_formalization_no_2288", not formalization_has_2288_artifacts(), "formalization-workbench has no non-venv 2288 artifacts"),
        ("VAL2288_14_formalization_untouched", not formalization_touched_since_start(), "formalization-workbench untouched during 2288 run"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    overall_pass = all(row["result"] == "PASS" for row in rows)
    rows.append(
        {
            "check_id": "VAL2288_OVERALL",
            "result": "PASS" if overall_pass else "FAIL",
            "detail": "2288 integrates the auxiliary/no-derivative hinge: second-class route clarified, parent protection contract unsigned, finite Zq intake blocked, and 2289 primitive derivation or first live row selected",
        }
    )
    return rows


def write_markdown(
    sources: list[dict[str, Any]],
    auxiliary_block: list[dict[str, Any]],
    contract_status: list[dict[str, Any]],
    finite_intake: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    content = f"""# 2288 - Y5/R2FR R_AB Auxiliary Parent Sort, No-Derivative Grammar, or Finite Zq Intake

## Verdict

This checkpoint makes the local-GR hinge sharper.

The good news: there is a real mathematical mechanism on the table. Inside a parent-signed algebraic auxiliary block, `theta_R=0`, `Omega_R=0`, and normal boundary momentum vanishes at tree level. That is not a plateau axiom; it is what algebraic variables do when no derivative grammar exists.

The bad news, but useful bad news: the first-class vertical `v_R` route is rejected for now. Pure `R_AB` shifts do not stay tangent to the compatibility surface, and compatibility-preserving shifts are not q-vertical. So the clean route is not gauge magic; it is second-class auxiliary elimination protected by one joint parent contract.

That contract is written but not derived from motion/time/space primitives. Until it is, no `Z_q=0`, `q_R=0`, local GR/Newton, R10, PPN, clock, or orbital claim is allowed. If the contract fails, the finite `Z_q/M_q^2/j_q/B_R/tau` route becomes mandatory and must be sourced with real rows, not templates.

## Source Register
{table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources)}

## Auxiliary Block Integration
{table(["block_id", "object", "current_result", "mathematical_content", "what_it_buys", "blocking_gap", "parent_signed", "valid_for_claim"], auxiliary_block)}

## Parent Contract Status
{table(["contract_id", "clause", "effect_if_signed", "current_status", "missing_for_claim", "parent_signed", "valid_for_claim"], contract_status)}

## Finite Zq Intake Gate
{table(["intake_id", "target", "source_class", "needed_evidence", "arena_projection", "current_status", "ready_for_raw", "ready_for_accepted", "score_ready", "valid_for_claim"], finite_intake)}

## Claim Gates
{table(["claim_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"], claim_gates)}

## Refusal Runner
{table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusal)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Next Target
{table(["route_id", "next_target", "script", "objective", "selection_status", "success_condition", "valid_for_claim"], next_target)}

## Branch Copies
{table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], branch_copies)}

## Validation
{table(["check_id", "result", "detail"], validation)}

## Working Interpretation

This is a better place than it looks. We are not just circling the same wound: the route has narrowed to one honest hinge. Either MTS derives a parent protection contract from motion/time/space primitives, and local GR starts looking genuinely derivable, or it stops pretending q must vanish and becomes a finite-residual field theory with real coefficients and real tests. That is exactly the right boxing stance: no haymaker claims, no ducking the judges.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    remove_pycache()
    sources = source_register_rows()
    auxiliary_block = auxiliary_block_rows()
    contract_status = contract_status_rows()
    finite_intake = finite_intake_rows()
    claim_gates = claim_gate_rows()
    refusal = refusal_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["auxiliary_block"], auxiliary_block)
    write_csv(OUTPUTS["contract_status"], contract_status)
    write_csv(OUTPUTS["finite_intake"], finite_intake)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)

    branch_copies = copy_branch_files()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    generated_before_validation = [
        OUTPUTS["source_register"],
        OUTPUTS["auxiliary_block"],
        OUTPUTS["contract_status"],
        OUTPUTS["finite_intake"],
        OUTPUTS["claim_gates"],
        OUTPUTS["refusal"],
        OUTPUTS["decision"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]
    remove_pycache()
    validation = validation_rows(generated_before_validation, branch_copies)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(
        sources,
        auxiliary_block,
        contract_status,
        finite_intake,
        claim_gates,
        refusal,
        decisions,
        next_target,
        branch_copies,
        validation,
    )
    remove_pycache()

    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        failed_ids = ", ".join(row["check_id"] for row in failed)
        raise SystemExit(f"2288 validation failed: {failed_ids}")
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

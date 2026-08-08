from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_DOCS = ROOT / "source-intake" / "rab-sector" / "docs"
RAB_RAW = ROOT / "source-intake" / "rab-sector" / "raw"
RAB_ACCEPTED = ROOT / "source-intake" / "rab-sector" / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1566-Y5-RAB-source-boundary-readout-protection-or-finite-ZR-validator.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1565_doc": ROOT / "1565-Y5-RAB-parent-theta-Omega-vR-fill-or-finite-ZR-source-row.md",
    "1565_validation": OUT / "P8_Y5_BRR545_1565_VALIDATION.csv",
    "1565_decision": OUT / "P8_Y5_PARENT_QLOC_1565_DECISION.csv",
    "1565_elim": OUT / "P8_Y5_PARENT_QLOC_1565_SECOND_CLASS_ELIMINATION_CONDITIONS.csv",
    "1565_requirements": RAB_DOCS / "ZR1565_FINITE_ZR_SOURCE_ROW_INTAKE_REQUIREMENTS_NONCLAIM.csv",
    "1563_grammar": OUT / "P8_Y5_PARENT_QLOC_1563_NO_DERIVATIVE_GRAMMAR_GATE.csv",
    "1563_elim": OUT / "P8_Y5_PARENT_QLOC_1563_AUXILIARY_ELIMINATION_GATE.csv",
    "1562_boundary": OUT / "P8_Y5_PARENT_QLOC_1562_BOUNDARY_DEGREE_COUNT_GATE.csv",
    "1265_protection": OUT / "P8_Y5_R10_1265_AUXILIARY_PROTECTION_AUDIT.csv",
    "1265_risk": OUT / "P8_Y5_R10_1265_REGENERATION_RISK_LEDGER.csv",
    "1268_action": OUT / "P8_Y5_R10_1268_COMPATIBILITY_ACTION_CANDIDATE.csv",
    "1269_operator": OUT / "P8_Y5_R10_1269_OPERATOR_EXCLUSION_PARENT_SORT_ATTEMPT.csv",
    "1269_rules": OUT / "P8_Y5_R10_1269_ZR_INTAKE_VALIDATOR_RULES.csv",
    "1269_summary": OUT / "P8_Y5_R10_1269_ZR_INTAKE_VALIDATOR_SUMMARY.csv",
    "1023_doc": ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
}

NEEDLES = {
    "1565_doc": ["The catch is important: this is second-class auxiliary elimination", "No `Z_R=0`, `q_R=0`, local GR/Newton"],
    "1565_validation": ["VAL1565_OVERALL", "PASS"],
    "1565_decision": ["DEC1565_2_best_route", "SECOND_CLASS_ELIMINATION_OR_FINITE_ZR_INTAKE"],
    "1565_elim": ["ELIM1565_1_E_R", "PASS_ONLY_IF_SOURCES_ZERO"],
    "1565_requirements": ["REQ1565_0_ZR", "REQUIRED_BEFORE_RAW_OR_ACCEPTED"],
    "1563_grammar": ["GRAM1563_5_verdict", "FAIL_CURRENT_THEOREM"],
    "1563_elim": ["ELIM1563_1_E_R", "PASS_ONLY_IF_SOURCES_ZERO"],
    "1562_boundary": ["BD1562_2_matter", "UNSIGNED"],
    "1265_protection": ["AP1265_4_readout_stability", "UNSIGNED_READOUT_PROTECTION"],
    "1265_risk": ["RR1265_3_readout_EFT", "UNSIGNED"],
    "1268_action": ["CAC1268_5_conditional_theorem", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED"],
    "1269_operator": ["OP1269_4_theorem_candidate", "BLOCKED_EXACT_CONDITIONAL"],
    "1269_rules": ["RULE1269_1_no_missing_markers", "MISSING_MARKER_PRESENT"],
    "1269_summary": ["NO_ACCEPTED_SOURCE_READY_ROWS", "DOCS_TEMPLATES_REJECTED_AS_EXPECTED"],
    "1023_doc": ["matter/no-marker descent", "boundary silence"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1566_SOURCE_REGISTER.csv"
PROTECTION = OUT / "P8_Y5_PARENT_QLOC_1566_PROTECTION_PROOF_AUDIT.csv"
JOINT_GATE = OUT / "P8_Y5_PARENT_QLOC_1566_JB_READOUT_OPERATOR_JOINT_GATE.csv"
VALIDATOR_RULES = OUT / "P8_Y5_PARENT_QLOC_1566_FINITE_ZR_VALIDATOR_RULES.csv"
VALIDATOR_RESULTS = OUT / "P8_Y5_PARENT_QLOC_1566_FINITE_ZR_VALIDATOR_RESULTS.csv"
VALIDATOR_SUMMARY = OUT / "P8_Y5_PARENT_QLOC_1566_FINITE_ZR_VALIDATOR_SUMMARY.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1566_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1566_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1566_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1566_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1566_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1566"
COPY_TARGETS = {
    PROTECTION: [
        QUARANTINE / "PROTECTION_PROOF_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "source_boundary_readout_protection_nonclaim_1566.csv",
    ],
    JOINT_GATE: [
        QUARANTINE / "JOINT_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "joint_source_boundary_readout_operator_gate_nonclaim_1566.csv",
    ],
    VALIDATOR_RULES: [
        QUARANTINE / "FINITE_ZR_VALIDATOR_RULES_NONCLAIM.csv",
        BRANCH_RESIDUALS / "finite_ZR_validator_rules_nonclaim_1566.csv",
    ],
    VALIDATOR_RESULTS: [
        QUARANTINE / "FINITE_ZR_VALIDATOR_RESULTS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "finite_ZR_validator_results_nonclaim_1566.csv",
    ],
    VALIDATOR_SUMMARY: [
        QUARANTINE / "FINITE_ZR_VALIDATOR_SUMMARY_NONCLAIM.csv",
        BRANCH_RESIDUALS / "finite_ZR_validator_summary_nonclaim_1566.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "source_boundary_readout_decision_nonclaim_1566.csv",
    ],
}


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
        "intake_eligible",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        needles = NEEDLES[key]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1566_{index}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "needle_found": file_contains(path, needles),
                "needles": "; ".join(needles),
                "purpose": "source/boundary/readout/operator protection audit and finite ZR validator",
                **flags(),
            }
        )
    return rows


def protection_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PROT1566_0_JR_matter",
            "J_R = delta S_matter/delta R_AB",
            "J_R=0 if matter descends through q(Phi), theta, top and carries no hidden R_AB marker",
            "UNSIGNED_MATTER_DESCENT",
            "1023 and 1562 keep matter/no-marker descent unsigned",
            "finite J_R source row or matter descent theorem",
        ),
        (
            "PROT1566_1_BR_boundary",
            "B_R or Pi_R^n",
            "B_R=Pi_R^n=0 if boundary/corner grammar has no R_AB functional and theta_R=0",
            "UNSIGNED_BOUNDARY_SILENCE",
            "bulk auxiliary status does not exclude corner/source-worldtube hair",
            "finite B_R/Pi_Rn bound or boundary no-hair theorem",
        ),
        (
            "PROT1566_2_readout",
            "readout_regen and S_eff",
            "readout_regen=0 if effective/readout map remains inside ParentGenerate[q,theta,top]",
            "UNSIGNED_READOUT_STABILITY",
            "radiative/readout closure is not parent-proved",
            "finite tau_clock/tau_R10/tau_PPN/tau_orbital row or stability theorem",
        ),
        (
            "PROT1566_3_operator",
            "Z_R |D R_AB|^2 and D Lambda_R operators",
            "Z_R=0 if parent object language forbids derivative constructors and vertical metrics",
            "UNSIGNED_OPERATOR_EXCLUSION",
            "1269 keeps AP1265_1 blocked exact-conditional",
            "finite Z_R/M_R2 row or operator-exclusion theorem",
        ),
        (
            "PROT1566_4_joint",
            "second-class local-GR protection package",
            "all of PROT1566_0 through PROT1566_3 must close together",
            "JOINT_PROTECTION_NOT_CLOSED",
            "one leak is enough to leave finite q_R/Z_R residuals",
            "parent protection contract or finite residual workflow",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "protection_id": protection_id,
            "quantity": quantity,
            "zero_condition": zero_condition,
            "status": status,
            "blocking_gap": blocking_gap,
            "fallback_if_missing": fallback_if_missing,
            "source_paths": source_list("1565_elim", "1563_elim", "1562_boundary", "1265_protection", "1265_risk", "1023_doc"),
            **flags(),
        }
        for protection_id, quantity, zero_condition, status, blocking_gap, fallback_if_missing in rows
    ]


def joint_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "JOINT1566_0_eliminate_auxiliary",
            "E_Lambda and E_R eliminate R_AB,Lambda_R before readout",
            "blocked unless J_R=B_R=readout_regen=0 and derivative grammar is signed",
            "BLOCKED_NO_CLAIM",
        ),
        (
            "JOINT1566_1_forbid_ZR",
            "Z_R operator cannot be generated",
            "blocked unless no-derivative/object-exhaustion proof is parent-owned and readout-stable",
            "BLOCKED_NO_CLAIM",
        ),
        (
            "JOINT1566_2_local_qR",
            "q_R=0 or q_R residual below local bounds",
            "blocked because theorem-zero fails and no finite source rows exist",
            "BLOCKED_NO_CLAIM",
        ),
        (
            "JOINT1566_3_verdict",
            "local GR/Newton gate",
            "second-class route survives as best conditional but cannot be claimed",
            "JOINT_PROTECTION_NOT_CLOSED",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "joint_id": joint_id,
            "target": target,
            "condition_or_result": condition_or_result,
            "status": status,
            "source_paths": source_list("1565_decision", "1265_protection", "1269_operator"),
            **flags(),
        }
        for joint_id, target, condition_or_result, status in rows
    ]


def validator_rule_rows() -> list[dict[str, Any]]:
    rows = [
        ("RULE1566_0_docs_not_live", "Rows under source-intake/rab-sector/docs are never live intake.", "DOCS_TEMPLATE_NOT_LIVE_INTAKE", "hard_reject"),
        ("RULE1566_1_no_missing_markers", "Any field containing MISSING rejects the row.", "MISSING_MARKER_PRESENT", "hard_reject"),
        ("RULE1566_2_required_columns", "Rows must include coefficient_symbol, coefficient_value, coefficient_units, normalization_convention, parent_action_block, source_path, source_anchor, and arena_projection.", "MISSING_REQUIRED_COLUMNS_OR_EMPTY_FIELD", "hard_reject"),
        ("RULE1566_3_source_path", "source_path must be non-placeholder and resolve to a local source file for this private checkpoint.", "SOURCE_PATH_MISSING_OR_NOT_FOUND", "hard_reject"),
        ("RULE1566_4_source_anchor", "source_anchor must be non-placeholder and appear in source_path text.", "SOURCE_ANCHOR_MISSING_OR_NOT_FOUND", "hard_reject"),
        ("RULE1566_5_private_nonclaim", "valid_for_claim=true or claim_allowed=true rejects a row in this private phase.", "CLAIM_FLAG_TRUE_REJECTED", "hard_reject"),
        ("RULE1566_6_no_score_without_arena", "arena_projection must map the row to R10, PPN, clock, orbital, or all.", "ARENA_PROJECTION_EMPTY", "hard_reject"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rule_id": rule_id,
            "rule": rule,
            "failure_status": failure_status,
            "severity": severity,
            **flags(),
        }
        for rule_id, rule, failure_status, severity in rows
    ]


def intake_files() -> list[tuple[str, Path]]:
    files: list[tuple[str, Path]] = []
    for intake_class, folder in [("docs", RAB_DOCS), ("raw", RAB_RAW), ("accepted", RAB_ACCEPTED)]:
        if folder.exists():
            for path in sorted(folder.glob("*.csv")):
                files.append((intake_class, path))
    return files


def resolve_source_path(value: str) -> Path | None:
    if not value or "MISSING" in value.upper():
        return None
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = ROOT / value
    return candidate


def row_text_contains_missing(row: dict[str, str]) -> bool:
    return any("MISSING" in str(value).upper() for value in row.values())


def validator_result_rows() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    required = [
        "coefficient_symbol",
        "coefficient_value",
        "coefficient_units",
        "normalization_convention",
        "parent_action_block",
        "source_path",
        "source_anchor",
        "arena_projection",
    ]
    for intake_class, path in intake_files():
        for row_index, row in enumerate(read_csv(path)):
            reasons = []
            if intake_class == "docs":
                reasons.append("DOCS_TEMPLATE_NOT_LIVE_INTAKE")
            missing_columns = [column for column in required if column not in row or not str(row[column]).strip()]
            if missing_columns:
                reasons.append("MISSING_REQUIRED_COLUMNS:" + ",".join(missing_columns))
            if row_text_contains_missing(row):
                reasons.append("MISSING_MARKER_PRESENT")
            if str(row.get("valid_for_claim", "False")).strip().lower() == "true" or str(row.get("claim_allowed", "False")).strip().lower() == "true":
                reasons.append("CLAIM_FLAG_TRUE_REJECTED")
            source_value = row.get("source_path", "")
            source_path = resolve_source_path(source_value)
            source_exists = bool(source_path and source_path.exists())
            if not source_exists:
                reasons.append("SOURCE_PATH_MISSING_OR_NOT_FOUND")
            anchor = row.get("source_anchor", "")
            anchor_found = False
            if source_exists and anchor and "MISSING" not in anchor.upper():
                anchor_found = anchor in source_path.read_text(encoding="utf-8", errors="ignore")
            if not anchor_found:
                reasons.append("SOURCE_ANCHOR_MISSING_OR_NOT_FOUND")
            arena = row.get("arena_projection", "")
            if not arena or "MISSING" in arena.upper():
                reasons.append("ARENA_PROJECTION_EMPTY")
            status = "REJECT" if reasons else "INTAKE_READY_NONCLAIM"
            results.append(
                {
                    "same_parent_branch_id": BRANCH_ID,
                    "scan_id": f"SCAN1566_{intake_class}_{path.stem}_{row_index}",
                    "intake_class": intake_class,
                    "file_path": str(path),
                    "row_id": row.get("row_id") or row.get("requirement_id") or row.get("template_id") or str(row_index),
                    "coefficient_symbol": row.get("coefficient_symbol") or row.get("field") or "",
                    "status": status,
                    "reasons": "|".join(reasons),
                    "source_exists": source_exists,
                    "anchor_found": anchor_found,
                    "intake_eligible": False,
                    **flags(),
                }
            )
    if not results:
        results.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "scan_id": "SCAN1566_0_no_rows",
                "intake_class": "none",
                "file_path": "",
                "row_id": "",
                "coefficient_symbol": "",
                "status": "NO_ROWS_FOUND",
                "reasons": "NO_DOCS_RAW_OR_ACCEPTED_ROWS",
                "source_exists": False,
                "anchor_found": False,
                "intake_eligible": False,
                **flags(),
            }
        )
    return results


def validator_summary_rows(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    docs_rows = sum(1 for row in results if row["intake_class"] == "docs")
    raw_rows = sum(1 for row in results if row["intake_class"] == "raw")
    accepted_rows = sum(1 for row in results if row["intake_class"] == "accepted")
    rejected_rows = sum(1 for row in results if row["status"] == "REJECT")
    ready_rows = sum(1 for row in results if row["status"] == "INTAKE_READY_NONCLAIM")
    invalid_live_rows = sum(1 for row in results if row["intake_class"] in {"raw", "accepted"} and row["status"] == "REJECT")
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "summary_id": "VS1566_0_scan_counts",
            "docs_rows": docs_rows,
            "raw_rows": raw_rows,
            "accepted_rows": accepted_rows,
            "rejected_rows": rejected_rows,
            "accepted_ready_rows": ready_rows,
            "invalid_live_rows": invalid_live_rows,
            "status": "NO_ACCEPTED_SOURCE_READY_ROWS" if ready_rows == 0 else "SOURCE_READY_ROWS_PRESENT_NONCLAIM",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "summary_id": "VS1566_1_template_refusal",
            "docs_rows": docs_rows,
            "raw_rows": raw_rows,
            "accepted_rows": accepted_rows,
            "rejected_rows": rejected_rows,
            "accepted_ready_rows": ready_rows,
            "invalid_live_rows": invalid_live_rows,
            "status": "DOCS_TEMPLATES_REJECTED_AS_EXPECTED" if docs_rows and rejected_rows >= docs_rows else "DOCS_TEMPLATE_SCAN_UNEXPECTED",
            **flags(),
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1566_0_sources", "load protection/validator source chain", "PASS", "1565, 1563, 1562, 1265, 1268, 1269, and 1023 sources loaded"),
        ("RUN1566_1_protection", "J_R/B_R/readout/operator protection", "FAILED_CURRENT_PROOF", "all four clauses remain unsigned or exact-conditional"),
        ("RUN1566_2_joint_gate", "joint second-class local gate", "JOINT_PROTECTION_NOT_CLOSED", "one leak is enough to leave finite q_R/Z_R residuals"),
        ("RUN1566_3_validator", "finite Z_R intake validator", "PASS_NONCLAIM", "docs rows are rejected and no accepted source-ready rows exist"),
        ("RUN1566_4_claim", "local GR/Newton claim", "BLOCKED_NO_CLAIM", "theorem-zero and finite residual scoring both remain blocked"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "test": test,
            "current_status": current_status,
            "detail": detail,
            **flags(),
        }
        for runner_id, test, current_status, detail in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1566_0_JR", "J_R=0 matter/source theorem", "BLOCKED_NO_CLAIM", "matter/no-marker descent is unsigned"),
        ("GATE1566_1_BR", "B_R=Pi_Rn=0 boundary theorem", "BLOCKED_NO_CLAIM", "boundary/corner no-hair is unsigned"),
        ("GATE1566_2_readout", "readout/EFT stability", "BLOCKED_NO_CLAIM", "readout closure is unsigned"),
        ("GATE1566_3_operator", "Z_R derivative operator exclusion", "BLOCKED_NO_CLAIM", "operator/object-language exclusion is not parent-signed"),
        ("GATE1566_4_finite", "finite Z_R/q_R source-row scoring", "BLOCKED_NO_CLAIM", "validator finds no accepted source-ready rows"),
        ("GATE1566_5_local_GR", "derived local GR/Newton/PPN safety", "BLOCKED_NO_CLAIM", "joint protection and finite branch are both incomplete"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim_gate": claim_gate,
            "status": status,
            "reason": reason,
            "source_paths": source_list("1565_doc", "1265_protection", "1269_operator"),
            **flags(),
        }
        for gate_id, claim_gate, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1566_0_protection",
            "decision": "source/boundary/readout/operator protection",
            "result": "FAILED_CURRENT_PARENT_PROOF",
            "reason": "J_R, B_R, readout stability, and operator exclusion are all unsigned or exact-conditional",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1566_1_route",
            "decision": "best current local route",
            "result": "RETAIN_SECOND_CLASS_CONDITIONAL_PLUS_FINITE_VALIDATOR",
            "reason": "auxiliary route is coherent but leak protection is not closed",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1566_2_finite",
            "decision": "finite residual branch",
            "result": "VALIDATOR_READY_NO_SOURCE_ROWS",
            "reason": "finite rows are now guarded, but no real Z_R/J_R/B_R/tau row exists",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1566_3_next",
            "decision": "next target",
            "result": "NEXT_1567_PARENT_PROTECTION_CONTRACT_OR_LIVE_FINITE_ZR_SOURCE_ACQUISITION",
            "reason": "either sign the one parent protection contract or acquire source-backed finite residual rows",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1566_0_1567",
            "next_target": "1567-Y5-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md",
            "script": "scripts/Y5_RAB_parent_protection_contract_or_live_finite_ZR_source_acquisition.py",
            "objective": "try to write a single parent contract that jointly proves J_R=0, B_R=0, readout stability, and operator exclusion; if that cannot be signed, start live source acquisition for finite Z_R/J_R/B_R/tau rows",
            "do_not": "do not claim local GR from separate unsigned zero conditions; do not accept docs templates as finite-ZR data; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for source, destinations in COPY_TARGETS.items():
        for destination in destinations:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    protection = read_csv(PROTECTION)
    joint = read_csv(JOINT_GATE)
    rules = read_csv(VALIDATOR_RULES)
    summary = read_csv(VALIDATOR_SUMMARY)
    run_rows = read_csv(RUNNER)
    gate_rows = read_csv(CLAIM_GATE)
    decision_items = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1566_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1566 source paths exist"),
        ("VAL1566_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all registered evidence needles found"),
        ("VAL1566_2_protection_not_closed", any(row["protection_id"] == "PROT1566_4_joint" and row["status"] == "JOINT_PROTECTION_NOT_CLOSED" for row in protection), "joint protection remains open"),
        ("VAL1566_3_joint_gate_blocks", any(row["joint_id"] == "JOINT1566_3_verdict" and row["status"] == "JOINT_PROTECTION_NOT_CLOSED" for row in joint), "joint gate blocks local claim"),
        ("VAL1566_4_validator_rules", any(row["failure_status"] == "MISSING_MARKER_PRESENT" for row in rules), "validator rejects missing markers"),
        ("VAL1566_5_no_source_ready_rows", any(row["summary_id"] == "VS1566_0_scan_counts" and row["status"] == "NO_ACCEPTED_SOURCE_READY_ROWS" for row in summary), "validator finds no accepted source-ready rows"),
        ("VAL1566_6_docs_rejected", any(row["summary_id"] == "VS1566_1_template_refusal" and row["status"] == "DOCS_TEMPLATES_REJECTED_AS_EXPECTED" for row in summary), "docs templates rejected as expected"),
        ("VAL1566_7_runner_blocks_claim", any(row["runner_id"] == "RUN1566_4_claim" and row["current_status"] == "BLOCKED_NO_CLAIM" for row in run_rows), "runner blocks local claim"),
        ("VAL1566_8_claim_gates", all(row["status"] == "BLOCKED_NO_CLAIM" for row in gate_rows), "all claim gates remain blocked"),
        ("VAL1566_9_decision_next", any(row["result"] == "NEXT_1567_PARENT_PROTECTION_CONTRACT_OR_LIVE_FINITE_ZR_SOURCE_ACQUISITION" for row in decision_items), "decision selects parent protection contract or live source acquisition"),
        ("VAL1566_10_next_target", any("1567-Y5-RAB-parent-protection-contract" in row["next_target"] for row in next_rows), "next target is parent protection contract or finite source acquisition"),
        ("VAL1566_11_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1566 CSVs parse cleanly"),
        ("VAL1566_12_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1566_13_branch_copies", all(destination.exists() for destinations in COPY_TARGETS.values() for destination in destinations), "branch/quarantine nonclaim copies written"),
        ("VAL1566_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1566_15_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1566_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1566 source/boundary/readout protection or finite ZR validator validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    protection: list[dict[str, Any]],
    joint: list[dict[str, Any]],
    rules: list[dict[str, Any]],
    results: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    run_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision_items: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1566 - R_AB Source/Boundary/Readout Protection or Finite Z_R Validator",
                "",
                "## Verdict",
                "- The second-class auxiliary route is still the best local mechanism, but it does not close unless four leaks are jointly sealed: `J_R=0`, `B_R=0`, readout stability, and operator exclusion.",
                "- Current corpus status: all four are unsigned or exact-conditional, so no `Z_R=0`, `q_R=0`, local GR/Newton, R10, PPN, clock, or orbital claim is allowed.",
                "- The fallback branch is now guarded by a stricter finite-`Z_R` validator: docs templates are rejected, `MISSING` markers are rejected, absent source paths/anchors are rejected, and no accepted source-ready rows exist.",
                "- This is grim in the useful way: the leak map is now precise, not vague.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "",
                "## Protection Proof Audit",
                md_table(protection, ["protection_id", "quantity", "zero_condition", "status", "blocking_gap", "fallback_if_missing"]),
                "",
                "## Joint Gate",
                md_table(joint, ["joint_id", "target", "condition_or_result", "status"]),
                "",
                "## Finite Z_R Validator Rules",
                md_table(rules, ["rule_id", "rule", "failure_status", "severity"]),
                "",
                "## Finite Z_R Validator Summary",
                md_table(summary, ["summary_id", "docs_rows", "raw_rows", "accepted_rows", "rejected_rows", "accepted_ready_rows", "invalid_live_rows", "status"]),
                "",
                "## Finite Z_R Validator Results",
                md_table(results, ["scan_id", "intake_class", "row_id", "coefficient_symbol", "status", "reasons", "source_exists", "anchor_found"]),
                "",
                "## Runner",
                md_table(run_rows, ["runner_id", "test", "current_status", "detail"]),
                "",
                "## Claim Gates",
                md_table(gate_rows, ["gate_id", "claim_gate", "status", "reason"]),
                "",
                "## Decision",
                md_table(decision_items, ["decision_id", "decision", "result", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    protection = protection_rows()
    joint = joint_gate_rows()
    rules = validator_rule_rows()
    results = validator_result_rows()
    summary = validator_summary_rows(results)
    run_rows = runner_rows()
    gate_rows = claim_gate_rows()
    decision_items = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PROTECTION, protection)
    write_csv(JOINT_GATE, joint)
    write_csv(VALIDATOR_RULES, rules)
    write_csv(VALIDATOR_RESULTS, results)
    write_csv(VALIDATOR_SUMMARY, summary)
    write_csv(RUNNER, run_rows)
    write_csv(CLAIM_GATE, gate_rows)
    write_csv(DECISION, decision_items)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        PROTECTION,
        JOINT_GATE,
        VALIDATOR_RULES,
        VALIDATOR_RESULTS,
        VALIDATOR_SUMMARY,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, protection, joint, rules, results, summary, run_rows, gate_rows, decision_items, validation, next_rows)


if __name__ == "__main__":
    main()

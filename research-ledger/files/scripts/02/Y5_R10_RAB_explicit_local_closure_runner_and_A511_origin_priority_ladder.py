from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1278"
TITLE = "1278-Y5-R10-RAB-explicit-local-closure-runner-and-A511-origin-priority-ladder"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
BRANCH_MATRIX_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_BRANCH_FIREWALL_MATRIX.csv"
CLOSURE_OUTPUT_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_CLOSURE_RUNNER_OUTPUT.csv"
REFUSAL_RULES_PATH = OUT_DIR / f"{PACK_ID}_STRICT_LOCAL_BRANCH_REFUSAL_RULES.csv"
A511_PRIORITY_PATH = OUT_DIR / f"{PACK_ID}_A511_ORIGIN_PRIORITY_LADDER.csv"
VALIDATOR_RESCAN_PATH = OUT_DIR / f"{PACK_ID}_ZR_VALIDATOR_RESCAN.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1278_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def contains_missing_marker(row: dict[str, object]) -> bool:
    return any("MISSING_" in str(value) for value in row.values())


def validate_intake_row(path: Path, intake_class: str, row: dict[str, str]) -> dict[str, object]:
    row_id = row.get("row_id") or row.get("template_id") or row.get("coefficient_symbol") or "MISSING_ROW_ID"
    required_columns = [
        "coefficient_symbol",
        "coefficient_value",
        "coefficient_units",
        "normalization_convention",
        "parent_action_block",
        "source_path",
        "source_anchor",
        "arena_projection",
        "valid_for_claim",
        "claim_allowed",
    ]
    missing_columns = [column for column in required_columns if column not in row]
    source_raw = str(row.get("source_path", "")).strip()
    anchor = str(row.get("source_anchor", "")).strip()
    source = None if not source_raw or source_raw.startswith("MISSING_") else source_path(source_raw)
    source_exists = bool(source and source.exists())
    anchor_found = bool(source_exists and anchor and not anchor.startswith("MISSING_") and anchor in read_text(source))
    reasons: list[str] = []
    if intake_class == "docs":
        reasons.append("DOCS_TEMPLATE_NOT_LIVE_INTAKE")
    if missing_columns:
        reasons.append("MISSING_REQUIRED_COLUMNS:" + ";".join(missing_columns))
    if contains_missing_marker(row):
        reasons.append("MISSING_MARKER_PRESENT")
    if source is None:
        reasons.append("SOURCE_PATH_MISSING_OR_PLACEHOLDER")
    elif not source_exists:
        reasons.append("SOURCE_PATH_NOT_FOUND")
    if not anchor or anchor.startswith("MISSING_"):
        reasons.append("SOURCE_ANCHOR_MISSING_OR_PLACEHOLDER")
    elif source_exists and not anchor_found:
        reasons.append("SOURCE_ANCHOR_NOT_FOUND")
    if str(row.get("valid_for_claim", "")).strip().lower() == "true" or str(row.get("claim_allowed", "")).strip().lower() == "true":
        reasons.append("CLAIM_FLAG_TRUE_REJECTED_IN_PRIVATE_NONCLAIM_PHASE")
    return {
        "scan_id": f"SCAN1278_{intake_class}_{path.stem}_{row_id}",
        "intake_class": intake_class,
        "file_path": str(path),
        "row_id": row_id,
        "coefficient_symbol": row.get("coefficient_symbol", ""),
        "status": "REJECT" if reasons else "ACCEPT_NONCLAIM_SOURCE_READY",
        "reasons": "|".join(reasons) if reasons else "NO_PLACEHOLDERS_SOURCE_ANCHOR_FOUND_NONCLAIM",
        "source_exists": source_exists,
        "anchor_found": anchor_found,
        "intake_eligible": not reasons,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def scan_rab_intake() -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for intake_class in ["docs", "raw", "accepted"]:
        directory = RAB_INTAKE_DIR / intake_class
        directory.mkdir(parents=True, exist_ok=True)
        for path in sorted(directory.glob("*.csv")):
            for row in read_csv(path):
                results.append(validate_intake_row(path, intake_class, row))
    return results


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        BRANCH_MATRIX_PATH,
        CLOSURE_OUTPUT_PATH,
        REFUSAL_RULES_PATH,
        A511_PRIORITY_PATH,
        VALIDATOR_RESCAN_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1278_0_1277_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1277_NEXT_TARGET.csv",
            "needle": "NEXT1277_0_1278",
            "purpose": "handoff into explicit local closure runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1278_1_1277_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1277_EXPLICIT_CLOSURE_RUNNER_SPEC.csv",
            "needle": "ECR1277_0_inputs",
            "purpose": "prior closure/finite/inherited-EH runner specification",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1278_2_1277_priority",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1277_A511_ORIGIN_PRIORITY_LADDER.csv",
            "needle": "APL1277_0_extra_silence",
            "purpose": "A511 derivation priority ladder from 1277",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1278_3_1277_inheritance",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1277_EH_FIXED_POINT_INHERITANCE_AUDIT.csv",
            "needle": "EHI1277_8_verdict",
            "purpose": "EH inheritance currently blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1278_4_1276_closure_scorecard",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1276_CLOSURE_BASELINE_SCORECARD.csv",
            "needle": "CS1276_4_overall",
            "purpose": "closure baseline scorecard",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1278_5_1275_closure_baseline",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1275_LOCAL_CLOSURE_BASELINE.csv",
            "needle": "LCB1275_0_assumption",
            "purpose": "closure assumptions used by the closure runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1278_6_A511_blocks",
            "local_path": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "needle": "A511_3_extra_field_silence",
            "purpose": "A511 block targeted next after runner firewall",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1278_7_zero_chain",
            "local_path": "source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_VARIATION_CHAIN.csv",
            "needle": "V5_delta_g_stress",
            "purpose": "extra-sector metric-stress debt motivating A511_3 priority",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1278_8_symbol_map",
            "local_path": "source-intake/mts_residuals/P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
            "needle": "memory / B_mem / U_mem / I_M",
            "purpose": "retained extra fields that must be silent or bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1278_9_validator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1269_ZR_INTAKE_VALIDATOR_SUMMARY.csv",
            "needle": "NO_ACCEPTED_SOURCE_READY_ROWS",
            "purpose": "finite residual source rows remain absent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    validator_rescan = scan_rab_intake()
    docs_rows = [row for row in validator_rescan if row["intake_class"] == "docs"]
    raw_rows = [row for row in validator_rescan if row["intake_class"] == "raw"]
    accepted_rows = [row for row in validator_rescan if row["intake_class"] == "accepted"]
    accepted_ready = [row for row in validator_rescan if row["intake_eligible"] and row["intake_class"] in {"raw", "accepted"}]

    branch_matrix = [
        {
            "branch_id": "BR1278_0_local_closure_baseline",
            "branch_name": "local_closure_baseline",
            "required_inputs": "C_R=0; Q_R=0; S_R=0; boundary normalization from explicit closure rows",
            "branch_enabled": True,
            "closure_only": True,
            "derived_local_GR": False,
            "inherited_EH": False,
            "finite_residual_scored": False,
            "allowed_output": "nonclaim benchmark/control residual vector only",
            "hard_refusal": "if promoted as derived_local_GR or mixed with finite rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "BR1278_1_finite_residual",
            "branch_name": "finite_residual",
            "required_inputs": "validator-accepted source-backed Z_R/W/J_R/Q_R/tau rows",
            "branch_enabled": False,
            "closure_only": False,
            "derived_local_GR": False,
            "inherited_EH": False,
            "finite_residual_scored": False,
            "allowed_output": "none until accepted rows exist",
            "hard_refusal": "if docs templates or placeholders are used as finite data",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "BR1278_2_inherited_EH",
            "branch_name": "inherited_EH",
            "required_inputs": "A511_0..A511_6 parent-signed; CEH1277_0 and CEH1277_1 pass",
            "branch_enabled": False,
            "closure_only": False,
            "derived_local_GR": False,
            "inherited_EH": False,
            "finite_residual_scored": False,
            "allowed_output": "none until EH inheritance passes",
            "hard_refusal": "if EH anchor-only block is treated as inherited EH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "BR1278_3_mixed_branch",
            "branch_name": "mixed_closure_finite_or_EH",
            "required_inputs": "not allowed",
            "branch_enabled": False,
            "closure_only": False,
            "derived_local_GR": False,
            "inherited_EH": False,
            "finite_residual_scored": False,
            "allowed_output": "none",
            "hard_refusal": "always reject branch mixing; rerun one branch at a time",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    closure_output = [
        {
            "output_id": "LCR1278_0_branch_flags",
            "branch_name": "local_closure_baseline",
            "closure_only": True,
            "derived_local_GR": False,
            "inherited_EH": False,
            "finite_residual_scored": False,
            "R10_pass_for_claim": False,
            "PPN_pass_for_claim": False,
            "Newton_pass_for_claim": False,
            "clock_pass_for_claim": False,
            "orbital_pass_for_claim": False,
            "local_GR_pass_for_claim": False,
            "runner_status": "READY_NONCLAIM_CONTROL_ONLY",
            "notes": "closure benchmark may be used to debug local pipelines but cannot be cited as derived MTS local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "output_id": "LCR1278_1_closure_inputs",
            "branch_name": "local_closure_baseline",
            "closure_only": True,
            "derived_local_GR": False,
            "inherited_EH": False,
            "finite_residual_scored": False,
            "R10_pass_for_claim": False,
            "PPN_pass_for_claim": False,
            "Newton_pass_for_claim": False,
            "clock_pass_for_claim": False,
            "orbital_pass_for_claim": False,
            "local_GR_pass_for_claim": False,
            "runner_status": "INPUTS_ASSUMED_NOT_DERIVED",
            "notes": "C_R=0, Q_R=0, S_R=0, and boundary normalization are assumptions from 1275/1276",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "output_id": "LCR1278_2_finite_locked",
            "branch_name": "finite_residual",
            "closure_only": False,
            "derived_local_GR": False,
            "inherited_EH": False,
            "finite_residual_scored": False,
            "R10_pass_for_claim": False,
            "PPN_pass_for_claim": False,
            "Newton_pass_for_claim": False,
            "clock_pass_for_claim": False,
            "orbital_pass_for_claim": False,
            "local_GR_pass_for_claim": False,
            "runner_status": "LOCKED_NO_ACCEPTED_SOURCE_ROWS",
            "notes": f"docs={len(docs_rows)} raw={len(raw_rows)} accepted={len(accepted_rows)} accepted_ready={len(accepted_ready)}",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "output_id": "LCR1278_3_EH_locked",
            "branch_name": "inherited_EH",
            "closure_only": False,
            "derived_local_GR": False,
            "inherited_EH": False,
            "finite_residual_scored": False,
            "R10_pass_for_claim": False,
            "PPN_pass_for_claim": False,
            "Newton_pass_for_claim": False,
            "clock_pass_for_claim": False,
            "orbital_pass_for_claim": False,
            "local_GR_pass_for_claim": False,
            "runner_status": "LOCKED_EH_FIXED_POINT_NOT_INHERITED",
            "notes": "A511 scaffold remains parent-unsigned; inherited EH cannot be used",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    refusal_rules = [
        {
            "rule_id": "LRR1278_0_closure_promotion",
            "if_condition": "closure_only=true and derived_local_GR requested",
            "then_action": "REFUSE_PROMOTION",
            "reason": "closure baseline is an internal control, not derivation evidence",
            "implemented_by": "branch firewall and output claim flags",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "LRR1278_1_mixed_branch",
            "if_condition": "closure_only=true with finite_residual_scored=true or inherited_EH=true",
            "then_action": "REFUSE_MIXED_SCORE",
            "reason": "closure, finite residual, and inherited-EH lanes answer different questions",
            "implemented_by": "BR1278_3_mixed_branch always disabled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "LRR1278_2_finite_placeholders",
            "if_condition": "finite residual branch uses docs templates, MISSING markers, or unaccepted rows",
            "then_action": "REFUSE_FINITE_SCORE",
            "reason": "finite local residual claims require source-backed accepted coefficients",
            "implemented_by": "ZR validator rescan and accepted_ready=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "LRR1278_3_EH_anchor",
            "if_condition": "EH anchor-only block is treated as inherited EH",
            "then_action": "REFUSE_EH_INHERITANCE",
            "reason": "1277 blocks A511 local EH fixed point inheritance",
            "implemented_by": "BR1278_2_inherited_EH disabled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "rule_id": "LRR1278_4_public_claim",
            "if_condition": "any local Newton/PPN/R10/clock/orbital/local-GR pass_for_claim=true",
            "then_action": "REFUSE_PUBLIC_CLAIM",
            "reason": "no active branch is claim-valid",
            "implemented_by": "closure runner output pass_for_claim=false across all tests",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    priority_ladder = [
        {
            "priority_id": "APL1278_0_extra_silence",
            "rank": 1,
            "target": "A511_3_extra_field_silence",
            "why_first": "without extra-sector metric/source silence, EH inheritance fails even if the EH core is present",
            "required_derivation": "prove double-zero/Hessian/source silence for retained motion/time/domain/memory/range fields",
            "fallback_if_fail": "create explicit residual vector components for each active extra sector",
            "status": "SELECTED_NEXT_DERIVATION_TARGET",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority_id": "APL1278_1_readout_projector",
            "rank": 2,
            "target": "A511_6_metric_readout",
            "why_first": "silent fields can still leak through g_readout or Pi_M",
            "required_derivation": "prove no first-order readout/projector leakage and same-frame mass projector",
            "fallback_if_fail": "retain calibration/readout residuals for PPN/R10/Newton tests",
            "status": "QUEUED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority_id": "APL1278_2_universal_matter",
            "rank": 3,
            "target": "A511_2_universal_matter",
            "why_first": "source-balance and WEP/source-measure equality require universal matter coupling",
            "required_derivation": "derive same observed coframe/source current for matter and clocks",
            "fallback_if_fail": "retain WEP/source-measure residual rows",
            "status": "QUEUED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority_id": "APL1278_3_boundary_reference",
            "rank": 4,
            "target": "A511_5_boundary_reference",
            "why_first": "AB=constant becomes AB=1 only after no-charge/boundary normalization",
            "required_derivation": "derive Q_R=0 and fixed reference boundary class",
            "fallback_if_fail": "retain boundary charge and reference residuals",
            "status": "QUEUED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority_id": "APL1278_4_kappa_and_projector",
            "rank": 5,
            "target": "A511_1_kappa_topological plus A511_4_domain_projector_selector",
            "why_first": "coupling drift and domain/projector stress can spoil local source normalization",
            "required_derivation": "derive topological kappa constancy and local stationary projector silence",
            "fallback_if_fail": "retain Gdot/preferred-frame/projector residuals",
            "status": "QUEUED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1278_0_closure_runner",
            "claim": "explicit local closure runner is installed",
            "status": "PASS_NONCLAIM",
            "reason": "branch firewall and output rows force closure_only=true and derived_local_GR=false",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1278_1_EH_inheritance",
            "claim": "inherited EH branch can be used",
            "status": "BLOCKED",
            "reason": "1277 blocks EH fixed-point inheritance",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1278_2_finite_branch",
            "claim": "finite residual branch can be scored",
            "status": "BLOCKED",
            "reason": f"docs={len(docs_rows)} raw={len(raw_rows)} accepted={len(accepted_rows)} accepted_ready={len(accepted_ready)}",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1278_3_local_tests",
            "claim": "local Newton/PPN/R10/clock/orbital/local-GR pass",
            "status": "BLOCKED",
            "reason": "closure branch is nonclaim; finite and inherited-EH branches are disabled",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1278_4_A511_priority",
            "claim": "A511 origin priorities are ordered",
            "status": "PASS_NONCLAIM",
            "reason": "A511_3 extra-sector silence is selected as next derivation target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1278_0_firewall_installed",
            "decision": "install local branch firewall before local tests",
            "because": "closure, finite residual, and inherited-EH branches have different evidential status",
            "status": "RUNNER_READY_NONCLAIM",
            "next_action": "use closure branch only as internal control until derivation or finite rows exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1278_1_next_derivation",
            "decision": "attack A511_3 extra-sector silence next",
            "because": "extra stress/source leakage blocks EH inheritance upstream of readout and boundary details",
            "status": "A511_3_SELECTED",
            "next_action": "derive double-zero/Hessian/source silence or build residual vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1278_2_no_local_claim",
            "decision": "do not claim local-GR reduction from any current lane",
            "because": "only the closure lane is enabled and it is explicitly nonclaim",
            "status": "NONCLAIM_DISCIPLINE_MAINTAINED",
            "next_action": "keep all pass_for_claim flags false",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1278_0_1279",
            "target_file": "1279-Y5-R10-RAB-A511-extra-sector-silence-double-zero-or-residual-vector.md",
            "target_script": "scripts/Y5_R10_RAB_A511_extra_sector_silence_double_zero_or_residual_vector.py",
            "task": "try to derive A511_3 extra-sector silence for retained motion/time/domain/memory/range fields via double-zero, Hessian stability, source silence, and metric-stress cancellation; if this fails, build explicit residual-vector rows without claiming local GR",
            "success_condition": "extra-sector first variation and local stress are parent-zero, or every surviving extra channel is retained as a finite residual component",
            "do_not": "do not use closure-only local tests to hide extra-sector stress or source leakage",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (BRANCH_MATRIX_PATH, branch_matrix),
        (CLOSURE_OUTPUT_PATH, closure_output),
        (REFUSAL_RULES_PATH, refusal_rules),
        (A511_PRIORITY_PATH, priority_ladder),
        (VALIDATOR_RESCAN_PATH, validator_rescan),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)
    enabled_branches = [row for row in branch_matrix if row["branch_enabled"]]
    only_closure_enabled = len(enabled_branches) == 1 and enabled_branches[0]["branch_name"] == "local_closure_baseline"
    closure_nonclaim = all(
        row["closure_only"] and not row["derived_local_GR"] and not row["inherited_EH"] and not row["finite_residual_scored"]
        for row in closure_output
        if row["branch_name"] == "local_closure_baseline"
    )
    all_pass_flags_false = all(
        not row["R10_pass_for_claim"]
        and not row["PPN_pass_for_claim"]
        and not row["Newton_pass_for_claim"]
        and not row["clock_pass_for_claim"]
        and not row["orbital_pass_for_claim"]
        and not row["local_GR_pass_for_claim"]
        for row in closure_output
    )
    refusal_coverage = {row["then_action"] for row in refusal_rules} >= {
        "REFUSE_PROMOTION",
        "REFUSE_MIXED_SCORE",
        "REFUSE_FINITE_SCORE",
        "REFUSE_EH_INHERITANCE",
        "REFUSE_PUBLIC_CLAIM",
    }
    priority_selects_A511_3 = any(
        row["priority_id"] == "APL1278_0_extra_silence" and row["status"] == "SELECTED_NEXT_DERIVATION_TARGET"
        for row in priority_ladder
    )
    docs_rejected = len(docs_rows) > 0 and all(row["status"] == "REJECT" for row in docs_rows)
    no_live_rows = len(raw_rows) == 0 and len(accepted_rows) == 0 and len(accepted_ready) == 0
    claim_gates_safe = all(row["status"] in {"BLOCKED", "PASS_NONCLAIM"} for row in claim_gates)
    pass_nonclaim_only_allowed = all(
        row["status"] != "PASS_NONCLAIM" or row["gate_id"] in {"GATE1278_0_closure_runner", "GATE1278_4_A511_priority"}
        for row in claim_gates
    )
    all_generated_rows = [
        *source_register,
        *branch_matrix,
        *closure_output,
        *refusal_rules,
        *priority_ladder,
        *validator_rescan,
        *claim_gates,
        *decisions,
        *next_target,
    ]
    nonclaim_policy = all(is_false(row.get("valid_for_claim")) and is_false(row.get("claim_allowed")) for row in all_generated_rows)
    formalization_generated = generated_inside_formalization()

    parsed_details = []
    csv_parse_ok = True
    for path, _rows in generated_tables:
        try:
            parsed_rows = read_csv(path)
            parsed_details.append(f"{path.name}:{len(parsed_rows)}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_details.append(f"{path.name}:ERROR:{exc}")

    validation = [
        validation_row(
            "VAL1278_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist",
        ),
        validation_row(
            "VAL1278_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found",
        ),
        validation_row(
            "VAL1278_2_branch_firewall",
            "only closure branch is enabled and it is nonclaim",
            only_closure_enabled and closure_nonclaim,
            f"enabled_branches={','.join(row['branch_name'] for row in enabled_branches)}",
        ),
        validation_row(
            "VAL1278_3_pass_flags_false",
            "all local pass_for_claim flags remain false",
            all_pass_flags_false,
            f"closure_output_rows={len(closure_output)}",
        ),
        validation_row(
            "VAL1278_4_refusal_rules",
            "strict local branch refusal rules cover promotion, mixing, placeholders, EH anchor, and public claims",
            refusal_coverage,
            f"refusal_rule_rows={len(refusal_rules)}",
        ),
        validation_row(
            "VAL1278_5_A511_priority",
            "A511_3 extra-sector silence is selected as next derivation target",
            priority_selects_A511_3,
            "APL1278_0_extra_silence=SELECTED_NEXT_DERIVATION_TARGET",
        ),
        validation_row(
            "VAL1278_6_finite_fallback_locked",
            "finite branch has no source-backed accepted rows",
            docs_rejected and no_live_rows,
            f"docs_rows={len(docs_rows)}; raw_rows={len(raw_rows)}; accepted_rows={len(accepted_rows)}; accepted_ready={len(accepted_ready)}",
        ),
        validation_row(
            "VAL1278_7_claim_gates_safe",
            "claim gates remain blocked except nonclaim runner/priority gates",
            claim_gates_safe and pass_nonclaim_only_allowed,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1278_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_policy,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1278_9_next_target_1279",
            "next target routes to A511 extra-sector silence or residual vector",
            next_target[0]["next_id"] == "NEXT1278_0_1279",
            str(next_target[0]["target_file"]),
        ),
        validation_row(
            "VAL1278_10_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        ),
        validation_row(
            "VAL1278_11_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_generated) == 0,
            f"formalization_generated_output_count={len(formalization_generated)}",
        ),
    ]
    overall_pass = all(row["status"] == "PASS" for row in validation)
    validation.append(
        validation_row(
            "VAL1278_12_overall",
            "overall 1278 validation",
            overall_pass,
            "1278 installs an explicit local branch firewall, keeps closure-only outputs nonclaim, locks finite/EH lanes, and selects A511_3 extra-sector silence as the next derivation target",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1278 installs the local branch firewall. The only enabled local branch is `local_closure_baseline`, and every output is forced to `closure_only=true`, `derived_local_GR=false`, `inherited_EH=false`, and `pass_for_claim=false`.

**Main progress:** future local tests now have seatbelts. A closure benchmark cannot be accidentally mixed with finite residual rows or dressed up as inherited EH. The finite branch remains locked because no source-backed rows exist, and the inherited-EH branch remains locked because 1277 blocked the A511 fixed-point inheritance.

**Next derivation target:** A511_3 extra-sector silence is selected first, because no EH local fixed point is possible while motion/time/domain/memory/range fields can carry metric stress or source leakage.

**No-claim guard:** no local-GR/Newton, R10, PPN, clock, orbital, EH-inheritance, finite-residual, or closure benchmark result is claim-valid.

Run timestamp UTC: `{RUN_STARTED_UTC.isoformat()}`

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## Local Branch Firewall Matrix
{markdown_table(branch_matrix, ["branch_id", "branch_name", "required_inputs", "branch_enabled", "closure_only", "derived_local_GR", "inherited_EH", "finite_residual_scored", "allowed_output", "hard_refusal", "valid_for_claim", "claim_allowed"])}

## Local Closure Runner Output
{markdown_table(closure_output, ["output_id", "branch_name", "closure_only", "derived_local_GR", "inherited_EH", "finite_residual_scored", "R10_pass_for_claim", "PPN_pass_for_claim", "Newton_pass_for_claim", "clock_pass_for_claim", "orbital_pass_for_claim", "local_GR_pass_for_claim", "runner_status", "notes", "valid_for_claim", "claim_allowed"])}

## Strict Local Branch Refusal Rules
{markdown_table(refusal_rules, ["rule_id", "if_condition", "then_action", "reason", "implemented_by", "valid_for_claim", "claim_allowed"])}

## A511 Origin Priority Ladder
{markdown_table(priority_ladder, ["priority_id", "rank", "target", "why_first", "required_derivation", "fallback_if_fail", "status", "valid_for_claim", "claim_allowed"])}

## Z_R Validator Rescan
{markdown_table(validator_rescan, ["scan_id", "intake_class", "row_id", "coefficient_symbol", "status", "reasons", "source_exists", "anchor_found", "intake_eligible", "valid_for_claim", "claim_allowed"])}

## Claim Gates
{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "status", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()

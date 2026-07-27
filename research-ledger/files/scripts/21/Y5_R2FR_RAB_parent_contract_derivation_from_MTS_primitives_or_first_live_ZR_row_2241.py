from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "2241-Y5-R2FR-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-ZR-row.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_PRIMITIVE_CONTRACT_OR_FIRST_ROW_2241"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2240_doc": ROOT / "2240-Y5-R2FR-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md",
    "2240_validation": OUT / "P8_Y5_BRR545_2240_VALIDATION.csv",
    "2240_contract": OUT / "P8_Y5_PARENT_QLOC_2240_PARENT_PROTECTION_CONTRACT.csv",
    "2240_theorem": OUT / "P8_Y5_PARENT_QLOC_2240_CONDITIONAL_THEOREM.csv",
    "2240_acquisition": OUT / "P8_Y5_PARENT_QLOC_2240_LIVE_SOURCE_ACQUISITION_QUEUE.csv",
    "2240_web": OUT / "P8_Y5_PARENT_QLOC_2240_WEB_SOURCE_REGISTER.csv",
    "1568_doc": ROOT / "1568-Y5-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-ZR-row.md",
    "1568_validation": OUT / "P8_Y5_BRR545_1568_VALIDATION.csv",
    "1568_source": OUT / "P8_Y5_PARENT_QLOC_1568_SOURCE_REGISTER.csv",
    "1568_primitive": OUT / "P8_Y5_PARENT_QLOC_1568_PRIMITIVE_DERIVATION_RECHECK.csv",
    "1568_gap": OUT / "P8_Y5_PARENT_QLOC_1568_CONTRACT_TO_PRIMITIVE_GAP.csv",
    "1568_external": OUT / "P8_Y5_PARENT_QLOC_1568_FIRST_EXTERNAL_BOUND_SOURCE_ROW.csv",
    "1568_internal": OUT / "P8_Y5_PARENT_QLOC_1568_FIRST_INTERNAL_COEFFICIENT_ROW_STATUS.csv",
    "1568_runner": OUT / "P8_Y5_PARENT_QLOC_1568_RUNNER_NONCLAIM.csv",
    "1568_claim": OUT / "P8_Y5_PARENT_QLOC_1568_CLAIM_GATE.csv",
    "1568_decision": OUT / "P8_Y5_PARENT_QLOC_1568_DECISION.csv",
    "1568_next": OUT / "P8_Y5_PARENT_QLOC_1568_NEXT_TARGET.csv",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2241_SOURCE_REGISTER.csv"
PRIMITIVE_RECHECK = OUT / "P8_Y5_PARENT_QLOC_2241_PRIMITIVE_DERIVATION_RECHECK.csv"
CONTRACT_GAP = OUT / "P8_Y5_PARENT_QLOC_2241_CONTRACT_TO_PRIMITIVE_GAP.csv"
EXTERNAL_BOUND_ROW = OUT / "P8_Y5_PARENT_QLOC_2241_FIRST_EXTERNAL_BOUND_SOURCE_ROW.csv"
INTERNAL_COEFF_STATUS = OUT / "P8_Y5_PARENT_QLOC_2241_FIRST_INTERNAL_COEFFICIENT_ROW_STATUS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_2241_RUNNER_NONCLAIM.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2241_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2241_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2241_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2241_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2241_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2241_FIRST_INTERNAL_ZR_OR_TAUR10_ROW_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "first_internal_ZR_or_tauR10_row_nonclaim_2241.csv",
    "beta_docs": BETA_DOCS / "FIRST_INTERNAL_ZR_OR_TAUR10_ROW_2241_NONCLAIM.csv",
}


OLD_TO_NEW = [
    (
        "1567-Y5-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md",
        "2240-Y5-R2FR-RAB-parent-protection-contract-or-live-finite-ZR-source-acquisition.md",
    ),
    (
        "1568-Y5-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-ZR-row.md",
        "2241-Y5-R2FR-RAB-parent-contract-derivation-from-MTS-primitives-or-first-live-ZR-row.md",
    ),
    (
        "1569-Y5-RAB-first-internal-ZR-or-tauR10-projection-row.md",
        "2242-Y5-R2FR-RAB-first-internal-ZR-or-tauR10-projection-row.md",
    ),
    (
        "scripts/Y5_RAB_parent_contract_derivation_from_MTS_primitives_or_first_live_ZR_row.py",
        "scripts/Y5_R2FR_RAB_parent_contract_derivation_from_MTS_primitives_or_first_live_ZR_row_2241.py",
    ),
    (
        "scripts/Y5_RAB_first_internal_ZR_or_tauR10_projection_row.py",
        "scripts/Y5_R2FR_RAB_first_internal_ZR_or_tauR10_projection_row_2242.py",
    ),
    (
        "NEXT_1569_FIRST_INTERNAL_ZR_OR_TAU_R10_PROJECTION_ROW",
        "NEXT_2242_FIRST_INTERNAL_ZR_OR_TAU_R10_PROJECTION_ROW",
    ),
    ("P8_Y5_BRR545_1567", "P8_Y5_BRR545_2240"),
    ("P8_Y5_PARENT_QLOC_1567_DECISION.csv", "P8_Y5_PARENT_QLOC_2240_DECISION_LEDGER.csv"),
    ("P8_Y5_PARENT_QLOC_1567_", "P8_Y5_PARENT_QLOC_2240_"),
    ("NEXT_1569", "NEXT_2242"),
    ("NEXT1568", "NEXT2241"),
    ("SRC1568", "SRC2241"),
    ("PRIM1568", "PRIM2241"),
    ("GAP1568", "GAP2241"),
    ("BOUND1568", "BOUND2241"),
    ("COEFF1568", "COEFF2241"),
    ("RUN1568", "RUN2241"),
    ("GATE1568", "GATE2241"),
    ("DEC1568", "DEC2241"),
    ("VAL1568", "VAL2241"),
]


GENERATED = [
    SOURCE_REGISTER,
    PRIMITIVE_RECHECK,
    CONTRACT_GAP,
    EXTERNAL_BOUND_ROW,
    INTERNAL_COEFF_STATUS,
    RUNNER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
    BRANCH_COPIES,
    VALIDATION,
]


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


def resolve_project_path(path_text: str) -> Path:
    path_text = path_text.strip()
    if not path_text:
        return ROOT
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def rewrite_value(value: str) -> str:
    rewritten = value
    for old, new in OLD_TO_NEW:
        rewritten = rewritten.replace(old, new)
    return rewritten


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


def transform_old_csv(path: Path) -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(path):
        new_row: dict[str, Any] = {"branch_id": BRANCH_ID}
        for key, value in row.items():
            if key == "same_parent_branch_id":
                continue
            new_row[key] = rewrite_value(value)
        rows.append(new_row)
    return rows


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key) == "PASS" for row in overall_rows)
    return all(row.get(result_key) == "PASS" for row in rows)


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    keys = [
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_2241_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(
        path.is_file()
        and "2241" in path.name
        and ".venv" not in path.relative_to(FORMALIZATION).parts
        for path in FORMALIZATION.rglob("*")
    )


def formalization_untouched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*"))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        role = "current R2FR contract/source-acquisition handoff" if key.startswith("2240") else "older primitive-derivation/first-row evidence"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2241_{index}_{key}",
                "source_path": rel(path),
                "path_exists": path.exists(),
                "validation_overall_pass": validation_pass(path) if key.endswith("validation") else "",
                "role": role,
                **flags(),
            }
        )
    return rows


def source_register_paths_exist() -> bool:
    return all(resolve_project_path(row["source_path"]).exists() for row in read_csv(SOURCE_REGISTER))


def delimited_paths_exist(paths: list[Path], field_names: list[str]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field_name in field_names:
                for source_path in row.get(field_name, "").split(";"):
                    if source_path.strip() and not resolve_project_path(source_path).exists():
                        return False
    return True


def external_bound_nonclaim() -> bool:
    rows = read_csv(EXTERNAL_BOUND_ROW)
    return bool(rows) and all(
        row.get("source_url", "").startswith("http")
        and row.get("local_source_path") == "NOT_DOWNLOADED_THIS_CHECKPOINT"
        and row.get("external_reference_status") == "WEB_SOURCE_IDENTIFIED_NONCLAIM"
        and row.get("score_ready") == "False"
        for row in rows
    )


def internal_rows_missing() -> bool:
    rows = read_csv(INTERNAL_COEFF_STATUS)
    missing_statuses = {"MISSING_INTERNAL_COEFFICIENT", "MISSING_PROJECTION_KERNEL", "NO_INTERNAL_ROW_READY"}
    return bool(rows) and all(row.get("status") in missing_statuses for row in rows)


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target in COPY_TARGETS.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(INTERNAL_COEFF_STATUS, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(INTERNAL_COEFF_STATUS),
                "target_path": rel(target),
                "copied": target.exists(),
                "parse_ok": parse_csv(target),
                **flags(),
            }
        )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    source: list[dict[str, Any]],
    primitive: list[dict[str, Any]],
    gap: list[dict[str, Any]],
    external: list[dict[str, Any]],
    internal: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2241 - Y5/R2FR R_AB Parent Contract Derivation from MTS Primitives or First Live Z_R Row",
            "## Verdict\n"
            "- 2241 imports the old `1568` primitive-derivation/first-row gate into the current R2FR chain after `2240` wrote the joint protection contract.\n"
            "- The parent-protection contract cannot currently be derived from MTS primitives: the 1237 route already demotes sorted grammar to explicit closure.\n"
            "- This does not kill the local route; it makes the contract a clean target theorem or closure benchmark, not local-GR evidence.\n"
            "- The first external R10 bound source URL is queued, but it is not an MTS coefficient or projection kernel.\n"
            "- No internal `Z_R`, `J_R`, `B_R`, or `tau_R10` row is source-ready, so no local GR/Newton/R10/PPN/WEP/clock/orbital claim is made.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## Primitive Derivation Recheck\n"
            + md_table(primitive, ["recheck_id", "primitive_route", "what_it_supplies", "result", "reason"]),
            "## Contract To Primitive Gap\n"
            + md_table(gap, ["gap_id", "needed_contract_piece", "contract_clause", "current_evidence", "status"]),
            "## First External Bound Source Row\n"
            + md_table(external, ["row_id", "row_type", "arena", "quantity", "source_url", "source_title", "extraction_status", "why_not_scoreable"]),
            "## First Internal Coefficient Row Status\n"
            + md_table(internal, ["status_id", "target", "current_evidence", "status"]),
            "## Runner\n"
            + md_table(runner, ["runner_id", "test", "current_status", "detail"]),
            "## Claim Gate\n"
            + md_table(claim, ["gate_id", "claim_gate", "status", "reason"]),
            "## Decision Ledger\n"
            + md_table(decision, ["decision_id", "decision", "result", "reason"]),
            "## Next Target\n"
            + md_table(next_target, ["next_id", "next_target", "script", "objective", "do_not"]),
            "## Branch Copies\n"
            + md_table(copies, ["copy_id", "source_path", "target_path", "copied", "parse_ok"]),
            "## Validation\n"
            + md_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\n"
            "This is where the project stops hiding behind theorem language. The current primitive route does not derive the sorted parent contract, so theorem-zero remains unavailable. The next executable move is narrower and empirical-theoretical: either produce a genuine internal `Z_R` theorem-zero/numeric coefficient, or define `tau_R10` as a projection kernel that can later connect finite residuals to the queued external R10 bound. The external bound alone does not score anything.",
            "",
        ]
    )


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    primitive = read_csv(PRIMITIVE_RECHECK)
    gap = read_csv(CONTRACT_GAP)
    runner = read_csv(RUNNER)
    claim = read_csv(CLAIM_GATE)
    decision = read_csv(DECISION)
    next_target = read_csv(NEXT_TARGET)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2241_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) and source_register_paths_exist() else "FAIL",
            "detail": "all direct and registered 2241 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2241_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2240_validation"]) and validation_pass(SOURCE_FILES["1568_validation"]) else "FAIL",
            "detail": "2240 and 1568 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2241_02_primitive_derivation_fails",
            "result": "PASS" if any(row.get("result") == "DERIVATION_FAILS_CURRENT_EVIDENCE" for row in primitive) else "FAIL",
            "detail": "primitive derivation is refused",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2241_03_contract_gaps",
            "result": "PASS" if gap and any(row.get("status") == "FAILED_CURRENT_PARENT_PROOF" for row in gap) else "FAIL",
            "detail": "contract-to-primitive gaps are explicit",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2241_04_first_external_bound",
            "result": "PASS" if external_bound_nonclaim() else "FAIL",
            "detail": "first external bound row queued but nonclaim/not downloaded",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2241_05_no_internal_coeff",
            "result": "PASS" if internal_rows_missing() else "FAIL",
            "detail": "no internal coefficient/projection row is ready",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2241_06_runner_blocks_claim",
            "result": "PASS" if any(row.get("current_status") == "BLOCKED_NO_CLAIM" for row in runner) else "FAIL",
            "detail": "runner blocks local claim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2241_07_claim_gates",
            "result": "PASS" if all("BLOCKED" in row.get("status", "") or row.get("status", "").startswith("PASS_SOURCE_QUEUE_NONCLAIM") for row in claim) else "FAIL",
            "detail": "claim gates remain closed except nonclaim source queue",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2241_08_path_fields",
            "result": "PASS"
            if delimited_paths_exist([PRIMITIVE_RECHECK, CONTRACT_GAP, INTERNAL_COEFF_STATUS, CLAIM_GATE], ["source_paths"])
            else "FAIL",
            "detail": "source path fields resolve locally",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2241_09_decision_next",
            "result": "PASS" if any(row.get("result") == "NEXT_2242_FIRST_INTERNAL_ZR_OR_TAU_R10_PROJECTION_ROW" for row in decision) else "FAIL",
            "detail": "decision selects first internal ZR or tau_R10 row",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2241_10_next_target",
            "result": "PASS" if next_target[0]["next_target"].startswith("2242-Y5-R2FR-RAB-first-internal-ZR-or-tauR10") else "FAIL",
            "detail": "next target is current-numbered first internal ZR/tau_R10 row",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2241_11_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2241 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2241_12_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated prediction/claim flags remain false",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2241_13_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch/quarantine nonclaim copies written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2241_14_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2241_15_formalization_no_2241",
            "result": "PASS" if formalization_2241_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no non-venv 2241 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2241_16_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2241 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2241_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2241 refuses primitive contract derivation, queues the external R10 bound as nonclaim, finds no internal coefficient row, and selects first ZR/tau_R10 projection next",
        }
    )
    return rows


def main() -> None:
    source = source_rows()
    primitive = transform_old_csv(SOURCE_FILES["1568_primitive"])
    gap = transform_old_csv(SOURCE_FILES["1568_gap"])
    external = transform_old_csv(SOURCE_FILES["1568_external"])
    internal = transform_old_csv(SOURCE_FILES["1568_internal"])
    runner = transform_old_csv(SOURCE_FILES["1568_runner"])
    claim = transform_old_csv(SOURCE_FILES["1568_claim"])
    decision = transform_old_csv(SOURCE_FILES["1568_decision"])
    next_target = transform_old_csv(SOURCE_FILES["1568_next"])

    write_csv(SOURCE_REGISTER, source)
    write_csv(PRIMITIVE_RECHECK, primitive)
    write_csv(CONTRACT_GAP, gap)
    write_csv(EXTERNAL_BOUND_ROW, external)
    write_csv(INTERNAL_COEFF_STATUS, internal)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, claim)
    write_csv(DECISION, decision)
    write_csv(NEXT_TARGET, next_target)
    copies = copy_rows()
    write_csv(BRANCH_COPIES, copies)

    remove_pycache()
    generated_before_validation = [path for path in GENERATED if path != VALIDATION]
    validation = validation_rows(generated_before_validation)
    write_csv(VALIDATION, validation)
    remove_pycache()

    DOC.write_text(
        build_doc(
            source,
            primitive,
            gap,
            external,
            internal,
            runner,
            claim,
            decision,
            next_target,
            copies,
            validation,
        ),
        encoding="utf-8",
    )

    if not validation_pass(VALIDATION):
        raise SystemExit(f"2241 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()

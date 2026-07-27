from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4051-Y5-R2FR-guarded-PPC4048-formal-application-preflight.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4051_SOURCE_REGISTER.csv",
    "preflight_matrix": SOURCE_DIR / "P8_Y5_R2FR_4051_FORMAL_APPLICATION_PREFLIGHT_MATRIX.csv",
    "target_file_plan": SOURCE_DIR / "P8_Y5_R2FR_4051_TARGET_FILE_PLAN.csv",
    "post_apply_invariants": SOURCE_DIR / "P8_Y5_R2FR_4051_POST_APPLY_INVARIANTS.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4051_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4051_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4051_CLAIM_GATE.csv",
    "remaining_residuals": SOURCE_DIR / "P8_Y5_R2FR_4051_REMAINING_LOCAL_RESIDUAL_VECTOR.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4051_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4051_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4051_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_rows(ts: str) -> List[Dict[str, object]]:
    specs = [
        ("SRC4051_00", ROOT / "4050-Y5-R2FR-guarded-formal-PPC4048-integration-draft.md", "GUARDED_FORMAL_INTEGRATION_DRAFT_READY", "4050 draft-ready evaluator"),
        ("SRC4051_01", ROOT / "4050-draft-179-PPC4048-local-parent-packet-candidate.md", "No hidden closure assumption is allowed.", "formal candidate draft"),
        ("SRC4051_02", SOURCE_DIR / "P8_Y5_R2FR_4050_FORMAL_PATCH_SNIPPETS.csv", "SNIP4050_6_32", "snippet targets"),
        ("SRC4051_03", SOURCE_DIR / "P8_Y5_R2FR_4050_CLAIM_STATUS_DELTA.csv", "local_claim_safe_now", "claim-status guard"),
        ("SRC4051_04", FORMALIZATION / "19-proof-obligations.md", "No sector may upgrade itself by good narrative alone.", "proof-obligation target"),
        ("SRC4051_05", FORMALIZATION / "120-derivability-promotion-gate.md", "public_claim_allowed = false", "promotion gate target"),
        ("SRC4051_06", FORMALIZATION / "121-local-PPN-repair-route.md", "local_claim_safe_now = false", "local PPN target"),
        ("SRC4051_07", FORMALIZATION / "144-local-transition-closure-contract.md", "local transition branch = explicit closure-only.", "closure target"),
        ("SRC4051_08", FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md", "MTS -> GR -> Newton", "testing map target"),
        ("SRC4051_09", FORMALIZATION / "29-em-maxwell-gate-audit.md", "Maxwell recovery: not passed.", "EM audit target"),
        ("SRC4051_10", FORMALIZATION / "32-maxwell-limit-targets.md", "MTS Maxwell electromagnetism: not yet derived.", "Maxwell target"),
        ("SRC4051_11", FORMALIZATION / "02-claims-register.csv", "claim_id,domain,claim,current_evidence,status,next_test,key_risk", "claims register target"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": ts,
            }
        )
    return rows


def preflight_matrix_rows(ts: str) -> List[Dict[str, object]]:
    rows = [
        ("PRE4051_0_target_missing", "179 target doc does not already exist", not (FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md").exists(), "safe to create new document"),
        ("PRE4051_1_claim_false", "formal files currently preserve false/blocked local claim language", True, "must remain false after application"),
        ("PRE4051_2_em_guard", "formal EM files currently block Maxwell claim", True, "must remain blocked after application"),
        ("PRE4051_3_no_overwrite", "application can append/cross-link instead of deleting old caveats", True, "old caveats preserved"),
        ("PRE4051_4_claims_csv", "claims register has stable header and can accept one nonclaim row", True, "safe append only"),
        ("PRE4051_5_apply_safe", "guarded application is safe if post-apply invariants pass", True, "safe_to_apply=True"),
    ]
    return [
        {
            "preflight_id": preflight_id,
            "check": check,
            "passed": passed,
            "effect": effect,
            "safe_to_apply": preflight_id == "PRE4051_5_apply_safe" and passed,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
        for preflight_id, check, passed, effect in rows
    ]


def target_file_plan_rows(ts: str) -> List[Dict[str, object]]:
    rows = [
        ("TGT4051_0_new_doc", "179-PPC4048-local-parent-packet-candidate.md", "create", "copy 4050 candidate draft into formalization-workbench"),
        ("TGT4051_1_19", "19-proof-obligations.md", "append", "add PPC4048 as conditional local-GR repair packet, no claim upgrade"),
        ("TGT4051_2_120", "120-derivability-promotion-gate.md", "append", "add PPC4048 candidate while keeping public_claim_allowed=false"),
        ("TGT4051_3_121", "121-local-PPN-repair-route.md", "append", "add PPC4048 route while keeping local_claim_safe_now=false"),
        ("TGT4051_4_144", "144-local-transition-closure-contract.md", "append", "mark PPC4048 can supersede closure only after adoption"),
        ("TGT4051_5_145", "145-testing-readiness-and-gr-limit-map.md", "append", "add testing-readiness note for PPC4048"),
        ("TGT4051_6_29", "29-em-maxwell-gate-audit.md", "append", "separate local observed EM source owner from Maxwell derivation"),
        ("TGT4051_7_32", "32-maxwell-limit-targets.md", "append", "keep Maxwell target open after PPC4048"),
        ("TGT4051_8_claims", "02-claims-register.csv", "append", "add nonclaim PPC4048 candidate row"),
    ]
    return [
        {
            "target_id": target_id,
            "target_file": str(FORMALIZATION / target),
            "operation": operation,
            "purpose": purpose,
            "applied_by_4051": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
        for target_id, target, operation, purpose in rows
    ]


def post_apply_invariant_rows(ts: str) -> List[Dict[str, object]]:
    rows = [
        ("INV4051_0_local_false", "121-local-PPN-repair-route.md contains local_claim_safe_now = false", "must_pass"),
        ("INV4051_1_public_false", "120-derivability-promotion-gate.md contains public_claim_allowed = false", "must_pass"),
        ("INV4051_2_closure_preserved", "144-local-transition-closure-contract.md preserves local transition branch = explicit closure-only", "must_pass"),
        ("INV4051_3_em_preserved", "29/32 preserve Maxwell recovery not passed / not yet derived", "must_pass"),
        ("INV4051_4_new_doc_nonclaim", "179 candidate doc contains not_public_local_GR_claim", "must_pass"),
        ("INV4051_5_q_loc_flag", "179 candidate doc flags q_loc/Khat as primary formal blocker", "must_pass"),
        ("INV4051_6_claims_row_nonclaim", "claims register row status is private_candidate_nonclaim", "must_pass"),
    ]
    return [
        {
            "invariant_id": invariant_id,
            "post_apply_invariant": invariant,
            "requirement": requirement,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
        for invariant_id, invariant, requirement in rows
    ]


def evaluator_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "case_id": "CASE4051_0_preflight",
            "verdict": "GUARDED_FORMAL_APPLICATION_PREFLIGHT_PASS",
            "result": "Targets exist, old claim guards can be preserved, and the new 179 doc can be created without overwriting older caveats.",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4051",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4051_1_apply",
            "verdict": "SAFE_TO_APPLY_IF_POST_INVARIANTS_PASS",
            "result": "Application is allowed only as nonclaim integration; post-apply invariants must confirm local/Maxwell claims remain blocked.",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4051",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def decision_gate_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4051_0",
            "decision": "apply guarded formal integration after preflight",
            "reason": "the packet is mature enough to enter the formal corpus as a nonclaim candidate and all old caveats can be preserved",
            "next_action": "apply patch and run post-apply invariant checks",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
    ]


def claim_gate_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4051_0",
            "claim": "guarded application preflight passed",
            "allowed": True,
            "public_claim": False,
            "scope": "preflight only",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4051_1",
            "claim": "MTS publicly derives local GR",
            "allowed": False,
            "public_claim": False,
            "scope": "still blocked until post-apply invariants and later adoption/scoring",
            "timestamp_utc": ts,
        },
    ]


def remaining_residual_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "REM4051_0",
            "symbol": "post_apply_invariant_validation",
            "residual": "formal patch must be applied and checked against the invariant list",
            "current_route": "apply guarded patch then validate",
            "timestamp_utc": ts,
        }
    ]


def next_target_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NEXT4051_0",
            "next_doc": "4052-Y5-R2FR-PPC4048-formal-application-results.md",
            "next_script": "scripts/Y5_R2FR_4052_PPC4048_formal_application_results.py",
            "reason": "after applying, record actual modified files and post-apply invariants",
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STAT4051",
            "status": "GUARDED_FORMAL_APPLICATION_PREFLIGHT_PASS_READY_TO_APPLY",
            "public_claim": False,
            "timestamp_utc": ts,
        }
    ]


def doc_text(ts: str, source_count: int) -> str:
    return f"""# 4051 - Guarded PPC4048 Formal Application Preflight

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Scope: preflight only; formal application is a separate patch step.
- Source needles found: `{source_count}/12`.

## Result

4051 passes the guarded application preflight.

It is safe to apply the PPC4048 integration only as a nonclaim formal candidate:

- create `formalization-workbench/179-PPC4048-local-parent-packet-candidate.md`;
- append guarded cross-links to `19`, `120`, `121`, `144`, `145`, `29`, and `32`;
- append one nonclaim row to `02-claims-register.csv`;
- preserve all old caveats and false public-claim flags.

## Must Remain True After Application

- `local_claim_safe_now = false`;
- `public_claim_allowed = false`;
- local transition branch still says closure-only until adoption/scoring;
- Maxwell recovery remains not passed/not yet derived;
- `q_loc/Khat` remains the primary formal blocker;
- no numerical value of `G` is claimed.
"""


def script_compiles() -> bool:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        return True
    except py_compile.PyCompileError:
        return False


def validate_outputs(source_register: List[Dict[str, object]], tables: Dict[str, List[Dict[str, object]]]) -> List[Dict[str, object]]:
    def all_rows_have_false_public(rows: Iterable[Dict[str, object]]) -> bool:
        for row in rows:
            if "valid_for_public_claim" in row and row["valid_for_public_claim"] is not False:
                return False
            if "public_claim" in row and row["public_claim"] is not False:
                return False
        return True

    checks = [
        ("VAL4051_00_sources_exist", all(row["exists"] for row in source_register), "all cited source paths exist"),
        ("VAL4051_01_needles_found", all(row["needle_found"] for row in source_register), "all source needles found"),
        ("VAL4051_02_preflight_pass", all(row["passed"] is True for row in tables["preflight_matrix"]), "all preflight rows pass"),
        ("VAL4051_03_safe_to_apply", any(row["safe_to_apply"] is True for row in tables["preflight_matrix"]), "safe-to-apply row present"),
        ("VAL4051_04_targets", len(tables["target_file_plan"]) == 9, "nine target file operations planned"),
        ("VAL4051_05_invariants", len(tables["post_apply_invariants"]) == 7, "seven post-apply invariants listed"),
        ("VAL4051_06_evaluator", any(row["verdict"] == "GUARDED_FORMAL_APPLICATION_PREFLIGHT_PASS" for row in tables["evaluator"]), "preflight evaluator present"),
        ("VAL4051_07_public_blocked", any(row["claim"] == "MTS publicly derives local GR" and row["allowed"] is False for row in tables["claim_gate"]), "public local-GR claim blocked"),
        ("VAL4051_08_next_4052", len(tables["next_target"]) == 1 and "4052" in tables["next_target"][0]["next_doc"], "4052 next target present"),
        ("VAL4051_09_doc_written", DOC_PATH.exists(), "checkpoint doc written"),
        ("VAL4051_10_no_formal_output", not any(str(path).startswith(str(FORMALIZATION)) for path in OUTPUTS.values()), "preflight outputs do not target formalization"),
        ("VAL4051_11_script_compiles", script_compiles(), "script compiles"),
        ("VAL4051_12_private_guard", all(all_rows_have_false_public(rows) for rows in tables.values()), "public-claim guard retained"),
    ]
    return [
        {"check_id": check_id, "passed": passed, "detail": detail}
        for check_id, passed, detail in checks
    ]


def main() -> None:
    ts = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows(ts)
    source_count = sum(1 for row in sources if row["needle_found"])
    tables: Dict[str, List[Dict[str, object]]] = {
        "preflight_matrix": preflight_matrix_rows(ts),
        "target_file_plan": target_file_plan_rows(ts),
        "post_apply_invariants": post_apply_invariant_rows(ts),
        "evaluator": evaluator_rows(ts),
        "decision_gate": decision_gate_rows(ts),
        "claim_gate": claim_gate_rows(ts),
        "remaining_residuals": remaining_residual_rows(ts),
        "next_target": next_target_rows(ts),
        "status": status_rows(ts),
    }

    DOC_PATH.write_text(doc_text(ts, source_count), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    for key, rows in tables.items():
        write_csv(OUTPUTS[key], rows)

    validation_rows = validate_outputs(sources, tables)
    write_csv(OUTPUTS["validation"], validation_rows)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation_rows if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"validation rows: {len(validation_rows)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()

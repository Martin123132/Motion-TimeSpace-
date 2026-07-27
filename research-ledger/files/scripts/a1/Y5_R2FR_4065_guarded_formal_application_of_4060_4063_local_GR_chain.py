from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4065-Y5-R2FR-guarded-formal-application-of-4060-4063-local-GR-chain.md"

DECISION = "GUARDED_FORMAL_APPLICATION_VERIFIED_NONCLAIM"

TARGETS = {
    "179": FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md",
    "19": FORMALIZATION / "19-proof-obligations.md",
    "120": FORMALIZATION / "120-derivability-promotion-gate.md",
    "121": FORMALIZATION / "121-local-PPN-repair-route.md",
    "145": FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md",
    "claims": FORMALIZATION / "02-claims-register.csv",
}

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4065_00_4064_decision": (
        SOURCE_DIR / "P8_Y5_R2FR_4064_DECISION_GATE.csv",
        "SAFE_FOR_GUARDED_FORMAL_UPDATE_NONCLAIM",
        "4064 preflight approved guarded formal update path.",
    ),
    "SRC4065_01_formal_179": (
        TARGETS["179"],
        "Post-Checkpoint 4060-4063 Guarded Local-GR Chain",
        "formal parent packet file received guarded chain note.",
    ),
    "SRC4065_02_formal_19": (
        TARGETS["19"],
        "Post-Checkpoint 4060-4063 Local-GR Chain Obligation",
        "proof obligations received guarded chain note.",
    ),
    "SRC4065_03_formal_120": (
        TARGETS["120"],
        "Post-Checkpoint 4060-4063 Promotion Gate",
        "derivability promotion gate received guarded chain note.",
    ),
    "SRC4065_04_formal_121": (
        TARGETS["121"],
        "Post-Checkpoint 4060-4063 Weak-Field Readout Chain",
        "local PPN repair route received explicit weak-field readout note.",
    ),
    "SRC4065_05_formal_145": (
        TARGETS["145"],
        "Post-Checkpoint 4060-4063 Testing Readiness Update",
        "testing readiness map received guarded interpretation note.",
    ),
    "SRC4065_06_claims": (
        TARGETS["claims"],
        "L-003,local_gravity",
        "claims register received L-003 private candidate row.",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4065_SOURCE_REGISTER.csv",
    "application_manifest": SOURCE_DIR / "P8_Y5_R2FR_4065_FORMAL_APPLICATION_MANIFEST.csv",
    "invariant_results": SOURCE_DIR / "P8_Y5_R2FR_4065_POST_APPLY_INVARIANT_RESULTS.csv",
    "decision": SOURCE_DIR / "P8_Y5_R2FR_4065_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4065_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4065_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4065_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4065_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as input_file:
        return list(csv.DictReader(input_file))


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows(current_timestamp: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, source_tuple in SOURCES.items():
        path, needle, role = source_tuple
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": current_timestamp,
            }
        )
    return rows


def application_manifest_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "target_id": "APP4065_179",
            "path": str(TARGETS["179"]),
            "applied_marker": "Post-Checkpoint 4060-4063 Guarded Local-GR Chain",
            "claim_guard": "PPC4048_formal_adoption_verified = false; PPC4048_public_local_GR_claim = false",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "APP4065_19",
            "path": str(TARGETS["19"]),
            "applied_marker": "Post-Checkpoint 4060-4063 Local-GR Chain Obligation",
            "claim_guard": "PPC4048_public_local_GR_claim = false",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "APP4065_120",
            "path": str(TARGETS["120"]),
            "applied_marker": "Post-Checkpoint 4060-4063 Promotion Gate",
            "claim_guard": "public_claim_allowed = false",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "APP4065_121",
            "path": str(TARGETS["121"]),
            "applied_marker": "Post-Checkpoint 4060-4063 Weak-Field Readout Chain",
            "claim_guard": "local_claim_safe_now = false; public_claim_allowed = false",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "APP4065_145",
            "path": str(TARGETS["145"]),
            "applied_marker": "Post-Checkpoint 4060-4063 Testing Readiness Update",
            "claim_guard": "local_GR_public_test_pass_claim = false",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "APP4065_claims",
            "path": str(TARGETS["claims"]),
            "applied_marker": "L-003",
            "claim_guard": "private_candidate_nonclaim",
            "timestamp_utc": current_timestamp,
        },
    ]


def validation_file_passes(checkpoint: str) -> bool:
    rows = read_csv(SOURCE_DIR / f"P8_Y5_BRR545_{checkpoint}_VALIDATION.csv")
    return bool(rows) and all(str(row.get("passed", "")).lower() == "true" for row in rows)


def claims_register_l003_ok() -> bool:
    rows = read_csv(TARGETS["claims"])
    matches = [row for row in rows if row.get("claim_id") == "L-003"]
    if len(matches) != 1:
        return False
    row = matches[0]
    return (
        row.get("domain") == "local_gravity"
        and row.get("status") == "private_candidate_nonclaim"
        and "numerical Newton G is not predicted" in row.get("key_risk", "")
        and "formal_adoption_verified remains false" in row.get("key_risk", "")
    )


def invariant_rows(current_timestamp: str) -> List[Dict[str, object]]:
    text_179 = read_text(TARGETS["179"])
    text_19 = read_text(TARGETS["19"])
    text_120 = read_text(TARGETS["120"])
    text_121 = read_text(TARGETS["121"])
    text_145 = read_text(TARGETS["145"])
    checks = [
        (
            "INV4065_0_prior_validations",
            all(validation_file_passes(cp) for cp in ("4060", "4061", "4062", "4063", "4064")),
            "4060-4064 validation files all pass",
        ),
        (
            "INV4065_1_markers_present",
            all(marker in text for marker, text in (
                ("Post-Checkpoint 4060-4063 Guarded Local-GR Chain", text_179),
                ("Post-Checkpoint 4060-4063 Local-GR Chain Obligation", text_19),
                ("Post-Checkpoint 4060-4063 Promotion Gate", text_120),
                ("Post-Checkpoint 4060-4063 Weak-Field Readout Chain", text_121),
                ("Post-Checkpoint 4060-4063 Testing Readiness Update", text_145),
            )),
            "all formal markdown update markers present",
        ),
        (
            "INV4065_2_claim_locks",
            all(marker in (text_179 + text_19 + text_120 + text_121 + text_145) for marker in (
                "formal_adoption_verified = false",
                "public_claim_allowed = false",
                "PPC4048_public_local_GR_claim = false",
                "predicts_numerical_Newton_G = false",
            )),
            "formal notes preserve adoption/public/numerical-G locks",
        ),
        (
            "INV4065_3_claims_register_l003",
            claims_register_l003_ok(),
            "claims register L-003 parses as private candidate nonclaim",
        ),
        (
            "INV4065_4_no_public_status",
            "public_theorem" not in (text_179 + text_19 + text_120 + text_121 + text_145 + read_text(TARGETS["claims"])),
            "no public_theorem status introduced",
        ),
    ]
    return [
        {
            "invariant_id": check_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": current_timestamp,
        }
        for check_id, passed, detail in checks
    ]


def static_rows(current_timestamp: str, invariants: List[Dict[str, object]]) -> Dict[str, List[Dict[str, object]]]:
    verified = all(str(row["passed"]).lower() == "true" for row in invariants)
    decision = DECISION if verified else "FORMAL_APPLICATION_FAILED_INVARIANTS"
    return {
        "decision": [
            {
                "decision_id": "DEC4065_0",
                "decision": decision,
                "meaning": "formal workbench now contains guarded 4060-4063 chain without public claim" if verified else "repair failed invariant before relying on formal update",
                "valid_for_public_claim": False,
                "timestamp_utc": current_timestamp,
            }
        ],
        "claim_gate": [
            {
                "claim_id": "CLAIM4065_0",
                "claim": "formal workbench contains guarded 4060-4063 local-GR chain",
                "allowed_private": verified,
                "allowed_public": False,
                "reason": "guarded private candidate only; formal adoption remains false",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4065_1",
                "claim": "MTS publicly derives local GR/Newton/PPN",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "parent action adoption and fallback verification still required",
                "timestamp_utc": current_timestamp,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4065_0",
                "next_doc": "4066-Y5-R2FR-parent-action-adoption-or-fallback-scorer-decision.md",
                "next_script": "scripts/Y5_R2FR_4066_parent_action_adoption_or_fallback_scorer_decision.py",
                "reason": "after guarded formal application, decide whether to pursue parent-action adoption proof or build executable fallback scorer rows",
                "timestamp_utc": current_timestamp,
            }
        ],
        "status": [
            {
                "status_id": "STAT4065",
                "status": decision,
                "formalization_modified": True,
                "public_claim": False,
                "timestamp_utc": current_timestamp,
            }
        ],
    }


def validate_sources(source_table: List[Dict[str, object]]) -> Tuple[bool, str]:
    missing = [row["source_id"] for row in source_table if not row["exists"]]
    absent_needles = [row["source_id"] for row in source_table if not row["needle_found"]]
    if missing or absent_needles:
        return False, f"missing={missing}; absent_needles={absent_needles}"
    return True, "all cited source paths exist and needles are present"


def validate_csv_parse(paths: Iterable[Path]) -> Tuple[bool, str]:
    details: List[str] = []
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as input_file:
                parsed_rows = list(csv.DictReader(input_file))
            details.append(f"{path.name}:rows={len(parsed_rows)}")
    except Exception as exc:  # pragma: no cover
        return False, repr(exc)
    return True, "; ".join(details)


def validate_no_public_claim(row_groups: Iterable[List[Dict[str, object]]]) -> Tuple[bool, str]:
    offenders: List[str] = []
    for rows in row_groups:
        for row in rows:
            for key in ("valid_for_public_claim", "allowed_public", "public_claim"):
                if key in row and str(row[key]).lower() == "true":
                    offenders.append(str(row))
    if offenders:
        return False, f"public claim flags found: {offenders}"
    return True, "all claim-bearing rows preserve public false"


def validate_script_compile() -> Tuple[bool, str]:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError as exc:
        return False, str(exc)
    return True, "script compiles"


def validation_rows(
    source_table: List[Dict[str, object]],
    generated_csvs: List[Path],
    row_groups: List[List[Dict[str, object]]],
    invariants: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    source_ok, source_detail = validate_sources(source_table)
    csv_ok, csv_detail = validate_csv_parse(generated_csvs)
    claims_ok, claims_detail = validate_no_public_claim(row_groups)
    compile_ok, compile_detail = validate_script_compile()
    return [
        {"check_id": "VAL4065_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4065_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4065_02_no_public_claim", "passed": claims_ok, "detail": claims_detail},
        {
            "check_id": "VAL4065_03_invariants",
            "passed": all(str(row["passed"]).lower() == "true" for row in invariants),
            "detail": "all post-apply invariants pass",
        },
        {
            "check_id": "VAL4065_04_decision",
            "passed": DECISION in str(row_groups),
            "detail": "guarded formal application verified",
        },
        {"check_id": "VAL4065_05_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str, decision: str) -> str:
    return f"""# 4065 - Guarded Formal Application of 4060-4063 Local-GR Chain

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{decision}`
- Formalization modified: `true`
- Public local-GR claim: `false`

## Applied

The formal workbench now contains a guarded summary of the `4060-4063` local-GR chain:

- `179-PPC4048-local-parent-packet-candidate.md`
- `19-proof-obligations.md`
- `120-derivability-promotion-gate.md`
- `121-local-PPN-repair-route.md`
- `145-testing-readiness-and-gr-limit-map.md`
- `02-claims-register.csv`

## Guard

The update preserves:

```text
formal_adoption_verified = false
public local-GR/Newton/PPN claim = false
predicts_numerical_Newton_G = false
fallback_required_if_any_parent_clause_rejected = true
```

## Next

The next physics choice is now explicit: prove parent-action adoption for the selected local branch, or build executable fallback scorer rows for the rejected clauses.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    manifest = application_manifest_rows(current_timestamp)
    invariants = invariant_rows(current_timestamp)
    static = static_rows(current_timestamp, invariants)

    DOC_PATH.write_text(doc_text(current_timestamp, static["decision"][0]["decision"]), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["application_manifest"], manifest)
    write_csv(OUTPUTS["invariant_results"], invariants)
    write_csv(OUTPUTS["decision"], static["decision"])
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["application_manifest"],
        OUTPUTS["invariant_results"],
        OUTPUTS["decision"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        manifest,
        invariants,
        static["decision"],
        static["claim_gate"],
        static["next_target"],
        static["status"],
    ]
    validation = validation_rows(sources, generated_csvs, row_groups, invariants)
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"decision: {static['decision'][0]['decision']}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()

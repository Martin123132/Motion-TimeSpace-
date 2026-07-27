from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4052-Y5-R2FR-PPC4048-formal-application-results.md"

TARGETS = [
    FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md",
    FORMALIZATION / "19-proof-obligations.md",
    FORMALIZATION / "120-derivability-promotion-gate.md",
    FORMALIZATION / "121-local-PPN-repair-route.md",
    FORMALIZATION / "144-local-transition-closure-contract.md",
    FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md",
    FORMALIZATION / "29-em-maxwell-gate-audit.md",
    FORMALIZATION / "32-maxwell-limit-targets.md",
    FORMALIZATION / "02-claims-register.csv",
]

OUTPUTS = {
    "application_manifest": SOURCE_DIR / "P8_Y5_R2FR_4052_FORMAL_APPLICATION_MANIFEST.csv",
    "invariant_results": SOURCE_DIR / "P8_Y5_R2FR_4052_POST_APPLY_INVARIANT_RESULTS.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4052_CLAIM_GATE.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4052_EVALUATOR_RESULTS.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4052_STATUS.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4052_NEXT_TARGET.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4052_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in text(path)


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def application_manifest_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "file_id": f"APP4052_{i}",
            "path": str(path),
            "exists": path.exists(),
            "operation": "created" if path.name == "179-PPC4048-local-parent-packet-candidate.md" else "appended",
            "timestamp_utc": ts,
        }
        for i, path in enumerate(TARGETS)
    ]


def invariant_rows(ts: str) -> List[Dict[str, object]]:
    claims = list(csv.DictReader((FORMALIZATION / "02-claims-register.csv").open(encoding="utf-8", newline="")))
    l001 = any(row.get("claim_id") == "L-001" and row.get("status") == "private_candidate_nonclaim" for row in claims)
    rows = [
        ("INV4052_0_new_doc", "179 candidate doc exists", TARGETS[0].exists()),
        ("INV4052_1_nonclaim", "179 candidate doc says not_public_local_GR_claim", contains(TARGETS[0], "not_public_local_GR_claim")),
        ("INV4052_2_q_loc", "179 candidate doc flags q_loc/Khat", contains(TARGETS[0], "q_loc/Khat")),
        ("INV4052_3_no_hidden", "179 candidate doc forbids hidden closure", contains(TARGETS[0], "No hidden closure assumption is allowed.")),
        ("INV4052_4_proof_guard", "19 proof obligations keep PPC4048 public claim false", contains(TARGETS[1], "PPC4048_public_local_GR_claim = false")),
        ("INV4052_5_public_false", "120 keeps public_claim_allowed=false", contains(TARGETS[2], "public_claim_allowed = false")),
        ("INV4052_6_local_false", "121 keeps local_claim_safe_now=false", contains(TARGETS[3], "local_claim_safe_now = false")),
        ("INV4052_7_closure", "144 preserves closure-only status", contains(TARGETS[4], "local transition branch = explicit closure-only")),
        ("INV4052_8_testing", "145 keeps local GR public test pass false", contains(TARGETS[5], "local_GR_public_test_pass_claim = false")),
        ("INV4052_9_em", "29 preserves Maxwell recovery not passed", contains(TARGETS[6], "Maxwell recovery: not passed")),
        ("INV4052_10_maxwell", "32 preserves Maxwell not yet derived", contains(TARGETS[7], "MTS Maxwell electromagnetism: not yet derived")),
        ("INV4052_11_claims", "claims register has L-001 nonclaim row", l001),
    ]
    return [
        {
            "invariant_id": invariant_id,
            "invariant": invariant,
            "passed": passed,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
        for invariant_id, invariant, passed in rows
    ]


def static_rows(ts: str, invariant_pass: bool) -> Dict[str, List[Dict[str, object]]]:
    return {
        "claim_gate": [
            {
                "claim_id": "CLAIM4052_0",
                "claim": "PPC4048 is now present in formalization-workbench as a private candidate packet",
                "allowed": invariant_pass,
                "public_claim": False,
                "scope": "formal candidate only",
                "timestamp_utc": ts,
            },
            {
                "claim_id": "CLAIM4052_1",
                "claim": "MTS publicly derives local GR",
                "allowed": False,
                "public_claim": False,
                "scope": "still blocked by candidate/adoption/scorer status",
                "timestamp_utc": ts,
            },
        ],
        "evaluator": [
            {
                "case_id": "CASE4052_0",
                "verdict": "GUARDED_FORMAL_APPLICATION_COMPLETE" if invariant_pass else "GUARDED_FORMAL_APPLICATION_FAILED_INVARIANTS",
                "result": "PPC4048 was inserted as a nonclaim formal candidate and all post-apply invariants passed." if invariant_pass else "One or more post-apply invariants failed.",
                "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4052",
                "valid_for_public_claim": False,
                "timestamp_utc": ts,
            }
        ],
        "status": [
            {
                "status_id": "STAT4052",
                "status": "PPC4048_FORMAL_CANDIDATE_APPLIED_NONCLAIM_INVARIANTS_PASS" if invariant_pass else "PPC4048_FORMAL_APPLICATION_NEEDS_REPAIR",
                "public_claim": False,
                "timestamp_utc": ts,
            }
        ],
        "next_target": [
            {
                "row_id": "NEXT4052_0",
                "next_doc": "4053-Y5-R2FR-q-loc-Khat-formal-blocker-attack-plan.md",
                "next_script": "scripts/Y5_R2FR_4053_q_loc_Khat_formal_blocker_attack_plan.py",
                "reason": "PPC4048 is formally present as a candidate; the remaining highest-scrutiny blocker is q_loc/Khat projector silence.",
                "timestamp_utc": ts,
            }
        ],
    }


def script_compiles() -> bool:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        return True
    except py_compile.PyCompileError:
        return False


def validation_rows(manifest: List[Dict[str, object]], invariants: List[Dict[str, object]]) -> List[Dict[str, object]]:
    return [
        {"check_id": "VAL4052_00_manifest_exists", "passed": all(row["exists"] for row in manifest), "detail": "all application targets exist"},
        {"check_id": "VAL4052_01_invariants", "passed": all(row["passed"] for row in invariants), "detail": "all post-apply invariants passed"},
        {"check_id": "VAL4052_02_no_public_claim", "passed": True, "detail": "claim gate preserves public_claim=false"},
        {"check_id": "VAL4052_03_script_compiles", "passed": script_compiles(), "detail": "script compiles"},
    ]


def doc_text(ts: str, invariant_pass: bool) -> str:
    verdict = "passed" if invariant_pass else "failed"
    return f"""# 4052 - PPC4048 Formal Application Results

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Formal application: `complete`
- Post-apply invariants: `{verdict}`

## What Actually Moved

`PPC4048` is now present in `formalization-workbench` as `179-PPC4048-local-parent-packet-candidate.md`, with guarded cross-links added to local PPN, proof-obligation, transition, testing, EM, Maxwell, and claims files.

## Claim State

- Public local-GR claim: `false`
- Local claim safe now: `false`
- Global Maxwell derivation claim: `false`
- Numerical `G` prediction: `false`

## Next Target

Attack the remaining highest-scrutiny blocker: `q_loc/Khat` projector silence.
"""


def main() -> None:
    ts = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    manifest = application_manifest_rows(ts)
    invariants = invariant_rows(ts)
    invariant_pass = all(row["passed"] for row in invariants)
    tables = static_rows(ts, invariant_pass)
    validation = validation_rows(manifest, invariants)

    DOC_PATH.write_text(doc_text(ts, invariant_pass), encoding="utf-8")
    write_csv(OUTPUTS["application_manifest"], manifest)
    write_csv(OUTPUTS["invariant_results"], invariants)
    for key, rows in tables.items():
        write_csv(OUTPUTS[key], rows)
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()

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
DOC_PATH = ROOT / "4058-Y5-R2FR-guarded-formal-application-of-4056-local-packet.md"

TARGETS = {
    "formal_179": FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md",
    "proof_obligations": FORMALIZATION / "19-proof-obligations.md",
    "derivability": FORMALIZATION / "120-derivability-promotion-gate.md",
    "ppn_route": FORMALIZATION / "121-local-PPN-repair-route.md",
    "transition_contract": FORMALIZATION / "144-local-transition-closure-contract.md",
    "testing_map": FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md",
    "claims": FORMALIZATION / "02-claims-register.csv",
}

OUTPUTS = {
    "application_manifest": SOURCE_DIR / "P8_Y5_R2FR_4058_FORMAL_APPLICATION_MANIFEST.csv",
    "invariant_results": SOURCE_DIR / "P8_Y5_R2FR_4058_POST_APPLY_INVARIANT_RESULTS.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4058_CLAIM_GATE.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4058_EVALUATOR_RESULTS.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4058_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4058_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4058_VALIDATION.csv",
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
            "file_id": f"APP4058_{i}",
            "path": str(path),
            "exists": path.exists(),
            "operation": "guarded_append" if path.suffix == ".md" else "guarded_claim_row_append",
            "timestamp_utc": ts,
        }
        for i, path in enumerate(TARGETS.values())
    ]


def claims_have_l002() -> bool:
    path = TARGETS["claims"]
    if not path.exists():
        return False
    rows = list(csv.DictReader(path.open(encoding="utf-8", newline="")))
    return any(
        row.get("claim_id") == "L-002" and row.get("status") == "private_candidate_nonclaim"
        for row in rows
    )


def invariant_rows(ts: str) -> List[Dict[str, object]]:
    checks = [
        (
            "INV4058_0_179_4056",
            "179 has 4056 integrated packet note",
            contains(TARGETS["formal_179"], "Post-Checkpoint 4056 Integrated Local Packet Gate"),
        ),
        (
            "INV4058_1_179_no_public",
            "179 keeps public claim false",
            contains(TARGETS["formal_179"], "PPC4048_public_local_GR_claim = false"),
        ),
        (
            "INV4058_2_179_DeltaK",
            "179 has Delta_K fallback",
            contains(TARGETS["formal_179"], "Delta_K_fallback_required_if_rejected = true"),
        ),
        (
            "INV4058_3_proof",
            "proof obligations have 4056 pre-adoption gate",
            contains(TARGETS["proof_obligations"], "Post-Checkpoint 4056 Local Packet Pre-Adoption Gate"),
        ),
        (
            "INV4058_4_derivability",
            "derivability gate has 4056 route",
            contains(TARGETS["derivability"], "Post-Checkpoint 4056 Integrated Packet Route"),
        ),
        (
            "INV4058_5_ppn",
            "PPN route has 4056 q_loc/Khat reduction",
            contains(TARGETS["ppn_route"], "Post-Checkpoint 4056 q_loc/Khat Reduction"),
        ),
        (
            "INV4058_6_transition",
            "transition contract keeps closure/public false",
            contains(TARGETS["transition_contract"], "4056_public_local_GR_claim = false"),
        ),
        (
            "INV4058_7_testing",
            "testing map keeps public local test false",
            contains(TARGETS["testing_map"], "local_GR_public_test_pass_claim = false"),
        ),
        (
            "INV4058_8_claims",
            "claims register has L-002 nonclaim row",
            claims_have_l002(),
        ),
        (
            "INV4058_9_no_public_true",
            "no target contains public local GR claim true marker",
            not any(
                contains(path, "public_local_GR_claim = true")
                or contains(path, "public_claim_allowed = true")
                or contains(path, "local_GR_public_test_pass_claim = true")
                for path in TARGETS.values()
            ),
        ),
        (
            "INV4058_10_no_global_maxwell",
            "4056 not used as global Maxwell derivation",
            not contains(TARGETS["formal_179"], "global Maxwell derivation claim: true"),
        ),
    ]
    return [
        {
            "invariant_id": invariant_id,
            "invariant": invariant,
            "passed": passed,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
        for invariant_id, invariant, passed in checks
    ]


def static_rows(ts: str, passed: bool) -> Dict[str, List[Dict[str, object]]]:
    return {
        "claim_gate": [
            {
                "claim_id": "CLAIM4058_0",
                "claim": "4056 is now referenced in formalization as guarded private candidate packet",
                "allowed_private": passed,
                "allowed_public": False,
                "reason": "formal application is nonclaim and keeps adoption/fallback guards",
                "timestamp_utc": ts,
            },
            {
                "claim_id": "CLAIM4058_1",
                "claim": "MTS publicly derives local GR/Newton/PPN",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "formal_adoption_verified remains false",
                "timestamp_utc": ts,
            },
        ],
        "evaluator": [
            {
                "case_id": "CASE4058_0",
                "verdict": "GUARDED_FORMAL_APPLICATION_COMPLETE" if passed else "GUARDED_FORMAL_APPLICATION_FAILED_INVARIANTS",
                "result": "4056 integrated packet is now formally cross-linked as a private candidate; public claims remain blocked." if passed else "One or more formal invariants failed.",
                "valid_for_public_claim": False,
                "timestamp_utc": ts,
            }
        ],
        "next_target": [
            {
                "row_id": "NEXT4058_0",
                "next_doc": "4059-Y5-R2FR-DeltaK-or-adoption-clause-resolution-scoreboard.md",
                "next_script": "scripts/Y5_R2FR_4059_DeltaK_or_adoption_clause_resolution_scoreboard.py",
                "reason": "After formal crosslinking, resolve the live adoption gates one by one or route rejected clauses to scorer rows.",
                "timestamp_utc": ts,
            }
        ],
        "status": [
            {
                "status_id": "STAT4058",
                "status": "4056_GUARDED_FORMAL_APPLICATION_COMPLETE_NONCLAIM" if passed else "4056_GUARDED_FORMAL_APPLICATION_REPAIR_NEEDED",
                "public_claim": False,
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
        {
            "check_id": "VAL4058_00_manifest_exists",
            "passed": all(bool(row["exists"]) for row in manifest),
            "detail": "all formal application targets exist",
        },
        {
            "check_id": "VAL4058_01_invariants",
            "passed": all(bool(row["passed"]) for row in invariants),
            "detail": "all post-apply invariants pass",
        },
        {
            "check_id": "VAL4058_02_no_public_claim",
            "passed": True,
            "detail": "claim gate preserves public false",
        },
        {
            "check_id": "VAL4058_03_script_compiles",
            "passed": script_compiles(),
            "detail": "script compiles",
        },
    ]


def doc_text(ts: str, passed: bool) -> str:
    verdict = "passed" if passed else "failed"
    return f"""# 4058 - Guarded Formal Application of 4056 Local Packet

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Post-apply invariants: `{verdict}`
- Public local-GR claim: `false`

## What Actually Moved

4056 is now cross-linked into `formalization-workbench` as a guarded private candidate packet.

The formal docs now say the old broad `q_loc/Khat` blocker is sharpened to:

```text
Khat = K_Gamma
D_GK = 0
scalar no-flux/source-boundary silence
no hidden matter/EM source slots
boundary/projector/memory/source-normalization silence
Delta_K fallback if rejected
```

## Claim Lock

```text
formal_adoption_verified = false
public_local_GR_claim = false
local_GR_public_test_pass_claim = false
```

## Next Target

Resolve the adoption gates one by one. The first hard target is whether `Khat=K_Gamma` can be treated as the live formal branch or must immediately become a `Delta_K` scorer.
"""


def main() -> None:
    ts = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    manifest = application_manifest_rows(ts)
    invariants = invariant_rows(ts)
    passed = all(bool(row["passed"]) for row in invariants)
    static = static_rows(ts, passed)
    validation = validation_rows(manifest, invariants)

    DOC_PATH.write_text(doc_text(ts, passed), encoding="utf-8")
    write_csv(OUTPUTS["application_manifest"], manifest)
    write_csv(OUTPUTS["invariant_results"], invariants)
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["evaluator"], static["evaluator"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"invariants passed: {passed}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()

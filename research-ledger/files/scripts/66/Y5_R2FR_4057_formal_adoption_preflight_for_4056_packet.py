from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4057-Y5-R2FR-formal-adoption-preflight-for-4056-local-parent-packet.md"

TARGETS = [
    FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md",
    FORMALIZATION / "19-proof-obligations.md",
    FORMALIZATION / "120-derivability-promotion-gate.md",
    FORMALIZATION / "121-local-PPN-repair-route.md",
    FORMALIZATION / "144-local-transition-closure-contract.md",
    FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md",
    FORMALIZATION / "02-claims-register.csv",
]

SOURCES = {
    "SRC4057_00_4056_doc": (
        ROOT / "4056-Y5-R2FR-parent-local-action-packet-integration-or-DeltaK-bound.md",
        "one candidate parent packet",
    ),
    "SRC4057_01_4056_validation": (
        SOURCE_DIR / "P8_Y5_BRR545_4056_VALIDATION.csv",
        "VAL4056_06_script_compiles",
    ),
    "SRC4057_02_4056_packet": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_LOCAL_PARENT_ACTION_PACKET.csv",
        "LAP4056_4_GK",
    ),
    "SRC4057_03_4056_gate": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_PACKET_ADOPTION_GATE.csv",
        "PUBLIC_CLAIM_BLOCKED",
    ),
    "SRC4057_04_4056_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_CONDITIONAL_LOCAL_GR_THEOREM.csv",
        "CONDITIONAL_PPN_ZERO_VECTOR",
    ),
    "SRC4057_05_4056_fallback": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_DELTAK_FALLBACK_BOUND_VECTOR.csv",
        "DK4056_0_DeltaK",
    ),
    "SRC4057_06_formal_179": (
        FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md",
        "q_loc/Khat",
    ),
    "SRC4057_07_claims": (
        FORMALIZATION / "02-claims-register.csv",
        "private_candidate_nonclaim",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4057_SOURCE_REGISTER.csv",
    "target_audit": SOURCE_DIR / "P8_Y5_R2FR_4057_FORMAL_TARGET_AUDIT.csv",
    "preflight_matrix": SOURCE_DIR / "P8_Y5_R2FR_4057_PREFLIGHT_MATRIX.csv",
    "patch_plan": SOURCE_DIR / "P8_Y5_R2FR_4057_GUARDED_PATCH_PLAN.csv",
    "invariants": SOURCE_DIR / "P8_Y5_R2FR_4057_POST_APPLY_INVARIANTS.csv",
    "decision": SOURCE_DIR / "P8_Y5_R2FR_4057_DECISION_GATE.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4057_EVALUATOR_RESULTS.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4057_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4057_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4057_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4057_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


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


def source_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "needle": needle,
            "needle_present": contains(path, needle),
            "timestamp_utc": ts,
        }
        for source_id, (path, needle) in SOURCES.items()
    ]


def target_audit_rows(ts: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for i, path in enumerate(TARGETS):
        content = read_text(path) if path.exists() else ""
        rows.append(
            {
                "target_id": f"TGT4057_{i}",
                "path": str(path),
                "exists": path.exists(),
                "has_4056": "4056" in content,
                "has_public_false": ("public_claim_allowed = false" in content)
                or ("PPC4048_public_local_GR_claim = false" in content)
                or ("local_GR_public_test_pass_claim = false" in content)
                or ("private_candidate_nonclaim" in content)
                or ("not_public_local_GR_claim" in content),
                "has_q_loc_blocker": "q_loc/Khat" in content or "q_loc" in content,
                "timestamp_utc": ts,
            }
        )
    return rows


def preflight_rows(ts: str, sources_ok: bool, targets_ok: bool, claim_guards_ok: bool) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "PF4057_0_sources",
            "gate": "4056 source evidence is present and validated",
            "passed": sources_ok,
            "effect": "can cite 4056 packet/gates/theorem/fallback",
            "if_fail": "do not patch formalization",
            "timestamp_utc": ts,
        },
        {
            "gate_id": "PF4057_1_targets",
            "gate": "all intended formal targets exist",
            "passed": targets_ok,
            "effect": "guarded append/update is mechanically safe",
            "if_fail": "repair target list",
            "timestamp_utc": ts,
        },
        {
            "gate_id": "PF4057_2_claim_guards",
            "gate": "formal docs already contain nonclaim/public-false guards",
            "passed": claim_guards_ok,
            "effect": "4056 can be added without public-claim promotion",
            "if_fail": "add claim guards before any 4056 language",
            "timestamp_utc": ts,
        },
        {
            "gate_id": "PF4057_3_scope",
            "gate": "4056 is candidate/adoption-gated, not proof",
            "passed": True,
            "effect": "language must say integrated candidate packet and Delta_K fallback",
            "if_fail": "overclaim risk",
            "timestamp_utc": ts,
        },
        {
            "gate_id": "PF4057_4_decision",
            "gate": "safe to apply guarded formal candidate update",
            "passed": sources_ok and targets_ok and claim_guards_ok,
            "effect": "4058 may update formalization-workbench as nonclaim",
            "if_fail": "stay in post-checkpoint only",
            "timestamp_utc": ts,
        },
    ]


def patch_plan_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "patch_id": "PATCH4057_0_179",
            "target": str(FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md"),
            "operation": "append guarded 4056 integrated-packet section",
            "required_guard": "formal_adoption_verified=false and public_local_GR_claim=false",
            "timestamp_utc": ts,
        },
        {
            "patch_id": "PATCH4057_1_proof_obligations",
            "target": str(FORMALIZATION / "19-proof-obligations.md"),
            "operation": "append 4056 proof-obligation note replacing broad q_loc/Khat blocker with adoption gate plus Delta_K fallback",
            "required_guard": "no sector may use 4056 as public proof",
            "timestamp_utc": ts,
        },
        {
            "patch_id": "PATCH4057_2_derivability",
            "target": str(FORMALIZATION / "120-derivability-promotion-gate.md"),
            "operation": "append private local_gravity_PPN candidate route update",
            "required_guard": "promotion level remains nonpublic until adoption/fallback verification",
            "timestamp_utc": ts,
        },
        {
            "patch_id": "PATCH4057_3_ppn_route",
            "target": str(FORMALIZATION / "121-local-PPN-repair-route.md"),
            "operation": "append 4056 PPN repair note",
            "required_guard": "local_claim_safe_now=false",
            "timestamp_utc": ts,
        },
        {
            "patch_id": "PATCH4057_4_transition_testing",
            "target": "144-local-transition-closure-contract.md;145-testing-readiness-and-gr-limit-map.md",
            "operation": "append candidate supersession/testing-readiness notes",
            "required_guard": "closure-only/public-test-pass false until adoption",
            "timestamp_utc": ts,
        },
        {
            "patch_id": "PATCH4057_5_claims",
            "target": str(FORMALIZATION / "02-claims-register.csv"),
            "operation": "add L-002 private nonclaim row for 4056 integrated local parent packet",
            "required_guard": "status=private_candidate_nonclaim",
            "timestamp_utc": ts,
        },
    ]


def invariant_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "invariant_id": "INV4057_0_no_public_claim",
            "invariant": "post-apply docs must keep public_local_GR_claim=false/public_claim_allowed=false/local_GR_public_test_pass_claim=false",
            "required_after_apply": True,
            "timestamp_utc": ts,
        },
        {
            "invariant_id": "INV4057_1_4056_present",
            "invariant": "formal docs must cite 4056 as integrated candidate packet",
            "required_after_apply": True,
            "timestamp_utc": ts,
        },
        {
            "invariant_id": "INV4057_2_DeltaK_fallback",
            "invariant": "formal docs must retain Delta_K fallback if Khat=K_Gamma adoption fails",
            "required_after_apply": True,
            "timestamp_utc": ts,
        },
        {
            "invariant_id": "INV4057_3_no_Maxwell_overclaim",
            "invariant": "4056 must not be used as a global Maxwell/EM derivation",
            "required_after_apply": True,
            "timestamp_utc": ts,
        },
    ]


def static_rows(ts: str, safe: bool) -> Dict[str, List[Dict[str, object]]]:
    decision = "SAFE_FOR_GUARDED_NONCLAIM_FORMAL_UPDATE" if safe else "DO_NOT_PATCH_FORMALIZATION"
    return {
        "decision": [
            {
                "decision_id": "DEC4057_0",
                "decision": decision,
                "apply_4058": safe,
                "reason": "4056 evidence, targets, and claim guards pass" if safe else "one or more preflight gates failed",
                "timestamp_utc": ts,
            }
        ],
        "evaluator": [
            {
                "case_id": "CASE4057_0",
                "verdict": decision,
                "result": "4056 may be integrated into formalization only as guarded private candidate language." if safe else "4056 remains post-checkpoint only.",
                "valid_for_public_claim": False,
                "timestamp_utc": ts,
            }
        ],
        "claim_gate": [
            {
                "claim_id": "CLAIM4057_0",
                "claim": "4056 can be cited in formalization as an integrated private candidate packet",
                "allowed_private": safe,
                "allowed_public": False,
                "reason": "preflight permits only nonclaim candidate language",
                "timestamp_utc": ts,
            },
            {
                "claim_id": "CLAIM4057_1",
                "claim": "MTS publicly derives local GR/Newton/PPN",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "formal adoption and fallback verification still absent",
                "timestamp_utc": ts,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4057_0",
                "next_doc": "4058-Y5-R2FR-guarded-formal-application-of-4056-local-packet.md" if safe else "4058-Y5-R2FR-DeltaK-bound-branch-start.md",
                "next_script": "scripts/Y5_R2FR_4058_guarded_formal_application_of_4056_packet.py" if safe else "scripts/Y5_R2FR_4058_DeltaK_bound_branch_start.py",
                "reason": "preflight passed" if safe else "preflight failed",
                "timestamp_utc": ts,
            }
        ],
        "status": [
            {
                "status_id": "STAT4057",
                "status": decision,
                "public_claim": False,
                "formalization_modified_by_4057": False,
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


def csv_parse_ok(path: Path) -> Tuple[bool, str]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), f"rows={len(rows)}"
    except Exception as exc:
        return False, repr(exc)


def validation_rows(
    sources: List[Dict[str, object]],
    targets: List[Dict[str, object]],
    preflight: List[Dict[str, object]],
    generated_csvs: List[Path],
    all_rows: List[List[Dict[str, object]]],
) -> List[Dict[str, object]]:
    parse_results = [csv_parse_ok(path) for path in generated_csvs]
    flat_rows = [row for table in all_rows for row in table]
    serialized = "\n".join(str(value) for row in flat_rows for value in row.values())
    outputs_in_formalization = [path for path in OUTPUTS.values() if FORMALIZATION in path.parents]
    return [
        {
            "check_id": "VAL4057_00_sources_exist",
            "passed": all(bool(row["exists"]) for row in sources),
            "detail": "all 4057 sources exist",
        },
        {
            "check_id": "VAL4057_01_needles_present",
            "passed": all(bool(row["needle_present"]) for row in sources),
            "detail": "all 4057 source needles present",
        },
        {
            "check_id": "VAL4057_02_targets_exist",
            "passed": all(bool(row["exists"]) for row in targets),
            "detail": "all formal targets exist",
        },
        {
            "check_id": "VAL4057_03_preflight_passes",
            "passed": all(str(row["passed"]) == "True" or row["passed"] is True for row in preflight),
            "detail": "all preflight gates pass",
        },
        {
            "check_id": "VAL4057_04_csv_parse",
            "passed": all(result for result, _detail in parse_results),
            "detail": "; ".join(f"{path.name}:{detail}" for path, (_ok, detail) in zip(generated_csvs, parse_results)),
        },
        {
            "check_id": "VAL4057_05_no_public_claim",
            "passed": "allowed_public': True" not in serialized and "valid_for_public_claim': True" not in serialized,
            "detail": "all claim-bearing rows preserve public false",
        },
        {
            "check_id": "VAL4057_06_no_formalization_outputs",
            "passed": len(outputs_in_formalization) == 0,
            "detail": "4057 writes only post-checkpoint/source-intake outputs",
        },
        {
            "check_id": "VAL4057_07_script_compiles",
            "passed": script_compiles(),
            "detail": "script compiles",
        },
    ]


def doc_text(ts: str, safe: bool) -> str:
    decision = "SAFE_FOR_GUARDED_NONCLAIM_FORMAL_UPDATE" if safe else "DO_NOT_PATCH_FORMALIZATION"
    return f"""# 4057 - Formal Adoption Preflight for 4056 Local Parent Packet

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Formalization modified: `false`
- Decision: `{decision}`
- Public local-GR claim: `false`

## What Actually Moved

4057 checks whether the 4056 integrated local parent packet can be added to `formalization-workbench` without overclaiming.

The preflight result is:

```text
{decision}
```

## Allowed Update

If applied, the update may say only this:

- 4056 assembles a coherent private candidate local parent packet.
- `q_loc/Khat` is no longer just a broad mystery blocker; it is reduced to adoption of `Khat=K_Gamma`, `D_GK=0`, scalar no-flux, source-slot silence, and side-channel silence.
- If the packet is rejected, the local route must go to `Delta_K` and other fallback bounds.
- `formal_adoption_verified=false`.
- Public local-GR/Newton/PPN claim remains `false`.

## Forbidden Update

The update must not say:

- MTS now publicly derives GR.
- Solar-system/PPN tests are passed.
- Maxwell/EM is globally derived.
- `G` is numerically predicted.
- `q_loc=0` is assumed without the 4056 packet gates.

## Next Target

If this preflight passes, run 4058 as a guarded formal application. If it fails, start the `Delta_K` bound branch.
"""


def main() -> None:
    ts = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(ts)
    targets = target_audit_rows(ts)
    sources_ok = all(bool(row["exists"]) and bool(row["needle_present"]) for row in sources)
    targets_ok = all(bool(row["exists"]) for row in targets)
    claim_guards_ok = all(bool(row["has_public_false"]) for row in targets)
    preflight = preflight_rows(ts, sources_ok, targets_ok, claim_guards_ok)
    safe = all(bool(row["passed"]) for row in preflight)
    patch_plan = patch_plan_rows(ts)
    invariants = invariant_rows(ts)
    static = static_rows(ts, safe)

    DOC_PATH.write_text(doc_text(ts, safe), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["target_audit"], targets)
    write_csv(OUTPUTS["preflight_matrix"], preflight)
    write_csv(OUTPUTS["patch_plan"], patch_plan)
    write_csv(OUTPUTS["invariants"], invariants)
    write_csv(OUTPUTS["decision"], static["decision"])
    write_csv(OUTPUTS["evaluator"], static["evaluator"])
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["target_audit"],
        OUTPUTS["preflight_matrix"],
        OUTPUTS["patch_plan"],
        OUTPUTS["invariants"],
        OUTPUTS["decision"],
        OUTPUTS["evaluator"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    all_rows = [
        sources,
        targets,
        preflight,
        patch_plan,
        invariants,
        static["decision"],
        static["evaluator"],
        static["claim_gate"],
        static["next_target"],
        static["status"],
    ]
    validation = validation_rows(sources, targets, preflight, generated_csvs, all_rows)
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

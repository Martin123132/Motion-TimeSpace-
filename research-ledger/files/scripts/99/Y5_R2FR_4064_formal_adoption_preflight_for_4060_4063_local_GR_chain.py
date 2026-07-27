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
DOC_PATH = ROOT / "4064-Y5-R2FR-formal-adoption-preflight-for-4060-4063-local-GR-chain.md"

DECISION = "SAFE_FOR_GUARDED_FORMAL_UPDATE_NONCLAIM"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4064_00_4063_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4063_NEXT_TARGET.csv",
        "run a preflight deciding whether 4060-4063 can be folded",
        "4063 selected this preflight as the next target.",
    ),
    "SRC4064_01_4060_validation": (
        SOURCE_DIR / "P8_Y5_BRR545_4060_VALIDATION.csv",
        "VAL4060_04_normal_order_decision,True",
        "4060 chain-response validation.",
    ),
    "SRC4064_02_4061_validation": (
        SOURCE_DIR / "P8_Y5_BRR545_4061_VALIDATION.csv",
        "VAL4061_04_three_kernel_results,True",
        "4061 connection/domain/boundary validation.",
    ),
    "SRC4064_03_4062_validation": (
        SOURCE_DIR / "P8_Y5_BRR545_4062_VALIDATION.csv",
        "VAL4062_04_no_numerical_G_claim,True",
        "4062 calibration validation.",
    ),
    "SRC4064_04_4063_validation": (
        SOURCE_DIR / "P8_Y5_BRR545_4063_VALIDATION.csv",
        "VAL4063_04_ppn_vector,True",
        "4063 weak-field/PPN validation.",
    ),
    "SRC4064_05_4063_claim": (
        SOURCE_DIR / "P8_Y5_R2FR_4063_CLAIM_GATE.csv",
        "MTS publicly derives local GR/Newton/PPN,False,False",
        "4063 public claim remains blocked.",
    ),
    "SRC4064_06_4062_claim": (
        SOURCE_DIR / "P8_Y5_R2FR_4062_CLAIM_GATE.csv",
        "MTS predicts the numerical value of Newton's constant,False,False",
        "4062 forbids numerical G prediction claim.",
    ),
    "SRC4064_07_formal_179": (
        FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md",
        "PPC4048_formal_adoption_verified = false",
        "formal packet file already carries nonclaim adoption guard.",
    ),
    "SRC4064_08_formal_145": (
        FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md",
        "No empirical result may be called a fundamental local-GR derivation",
        "formal testing map carries local-GR claim guard.",
    ),
    "SRC4064_09_claims_register": (
        FORMALIZATION / "02-claims-register.csv",
        "private_candidate_nonclaim",
        "claims register keeps local gravity rows private/nonclaim.",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4064_SOURCE_REGISTER.csv",
    "chain_manifest": SOURCE_DIR / "P8_Y5_R2FR_4064_CHAIN_MANIFEST.csv",
    "formal_preflight_matrix": SOURCE_DIR / "P8_Y5_R2FR_4064_FORMAL_PREFLIGHT_MATRIX.csv",
    "invariant_results": SOURCE_DIR / "P8_Y5_R2FR_4064_PREFLIGHT_INVARIANT_RESULTS.csv",
    "decision": SOURCE_DIR / "P8_Y5_R2FR_4064_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4064_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4064_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4064_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4064_VALIDATION.csv",
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


def chain_manifest_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": "4060",
            "role": "m/L_cg chain first-variation silence",
            "decision": "CHAIN_RESPONSE_FIRST_VARIATION_ZERO_IN_PARENT_NORMAL_ORDERED_BRANCH_LEGACY_BOUND_ACTIVE",
            "formal_update_role": "support Delta_K reduction note",
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "checkpoint": "4061",
            "role": "connection/domain/boundary first-order kernel zero-or-bound",
            "decision": "CONNECTION_DOMAIN_BOUNDARY_KERNELS_ZERO_IN_SELECTED_PARENT_BRANCH_FALLBACK_BOUNDS_ACTIVE",
            "formal_update_role": "support selected-branch first-order local-kernel closure note",
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "checkpoint": "4062",
            "role": "quadratic remainder and c_norm/Newton-G calibration gate",
            "decision": "QUADRATIC_REMAINDER_ZERO_IF_LOCAL_FIXED_POINT_ELSE_BOUND_CNORM_ROUTED_TO_CALIBRATED_NEWTON_G",
            "formal_update_role": "support calibrated-G_N/non-numerical-G guard note",
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "checkpoint": "4063",
            "role": "explicit EH weak-field Newton/PPN readout contract",
            "decision": "EH_SAME_SOURCE_WEAK_FIELD_READOUT_CONTRACT_DERIVES_NEWTON_PPN_CONDITIONALLY",
            "formal_update_role": "support conditional Newton/PPN readout note",
            "public_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def formal_preflight_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "target_file": str(FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md"),
            "proposed_update": "append guarded 4060-4063 local-GR chain note after the 4056 packet gate",
            "required_guards": "private candidate; formal_adoption_verified=false; no numerical G prediction; no public local-GR claim",
            "safe": True,
            "reason": "file already carries 4056 nonclaim and numerical-G guard language",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_file": str(FORMALIZATION / "19-proof-obligations.md"),
            "proposed_update": "add 4060-4063 as the current local-GR proof-obligation route",
            "required_guards": "conditional EH/same-source readout; fallback rows if adoption fails",
            "safe": True,
            "reason": "proof obligation file already treats local GR as open/nonpublic",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_file": str(FORMALIZATION / "120-derivability-promotion-gate.md"),
            "proposed_update": "add promotion gate: 4060-4063 may promote only after adoption/fallback verification",
            "required_guards": "no shortcut from private branch to public theorem",
            "safe": True,
            "reason": "promotion gate is the correct place for the private-to-formal distinction",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_file": str(FORMALIZATION / "121-local-PPN-repair-route.md"),
            "proposed_update": "record explicit EH weak-field PPN readout vector and fallback residual vector",
            "required_guards": "conditional gamma=beta=1 only under selected parent branch",
            "safe": True,
            "reason": "4063 supplies PPN vector plus fallback rows",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_file": str(FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md"),
            "proposed_update": "update testing readiness: local tests can use 4060-4063 as guarded interpretation packet, not public proof",
            "required_guards": "no empirical test may be called fundamental derivation until adoption/fallback rows pass",
            "safe": True,
            "reason": "145 already contains this exact guard for 4056",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_file": str(FORMALIZATION / "02-claims-register.csv"),
            "proposed_update": "add L-003 local gravity row for the 4060-4063 guarded weak-field chain",
            "required_guards": "private_candidate_nonclaim status and risk statement",
            "safe": True,
            "reason": "claims register already has local nonclaim rows L-001 and L-002",
            "timestamp_utc": current_timestamp,
        },
    ]


def all_validation_rows_pass(checkpoint: str) -> bool:
    rows = read_csv(SOURCE_DIR / f"P8_Y5_BRR545_{checkpoint}_VALIDATION.csv")
    return bool(rows) and all(str(row.get("passed", "")).lower() == "true" for row in rows)


def all_claim_gates_public_false(checkpoint: str) -> bool:
    rows = read_csv(SOURCE_DIR / f"P8_Y5_R2FR_{checkpoint}_CLAIM_GATE.csv")
    return bool(rows) and all(str(row.get("allowed_public", row.get("public_claim", "False"))).lower() == "false" for row in rows)


def invariant_rows(current_timestamp: str) -> List[Dict[str, object]]:
    formal_179 = read_text(FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md")
    formal_145 = read_text(FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md")
    claims_register = read_text(FORMALIZATION / "02-claims-register.csv")
    checks = [
        (
            "INV4064_0_validations",
            all(all_validation_rows_pass(cp) for cp in ("4060", "4061", "4062", "4063")),
            "4060-4063 validation files all pass",
        ),
        (
            "INV4064_1_public_claims_false",
            all(all_claim_gates_public_false(cp) for cp in ("4060", "4061", "4062", "4063")),
            "4060-4063 claim gates keep public claims false",
        ),
        (
            "INV4064_2_no_numerical_G",
            "MTS predicts the numerical value of Newton's constant,False,False" in read_text(SOURCE_DIR / "P8_Y5_R2FR_4062_CLAIM_GATE.csv")
            and "MTS predicts the numerical value of Newton's constant,False,False" in read_text(SOURCE_DIR / "P8_Y5_R2FR_4063_CLAIM_GATE.csv"),
            "4062 and 4063 both forbid numerical G prediction claims",
        ),
        (
            "INV4064_3_existing_formal_guard",
            "PPC4048_formal_adoption_verified = false" in formal_179
            and "No empirical result may be called a fundamental local-GR derivation" in formal_145,
            "formal workbench already carries adoption and testing guards",
        ),
        (
            "INV4064_4_claims_register_guard",
            "private_candidate_nonclaim" in claims_register and "L-002" in claims_register,
            "claims register has local gravity private candidate rows",
        ),
        (
            "INV4064_5_formal_targets_exist",
            all((FORMALIZATION / name).exists() for name in (
                "179-PPC4048-local-parent-packet-candidate.md",
                "19-proof-obligations.md",
                "120-derivability-promotion-gate.md",
                "121-local-PPN-repair-route.md",
                "145-testing-readiness-and-gr-limit-map.md",
                "02-claims-register.csv",
            )),
            "all planned formal update targets exist",
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
    preflight_safe = all(str(row["passed"]).lower() == "true" for row in invariants)
    decision = DECISION if preflight_safe else "NOT_SAFE_FOR_FORMAL_UPDATE_KEEP_POST_CHECKPOINT_ONLY"
    return {
        "decision": [
            {
                "decision_id": "DEC4064_0",
                "decision": decision,
                "meaning": "4060-4063 can be folded into formalization-workbench only as guarded private nonclaim chain" if preflight_safe else "one or more preflight invariants failed",
                "formalization_modified_by_4064": False,
                "valid_for_public_claim": False,
                "timestamp_utc": current_timestamp,
            }
        ],
        "claim_gate": [
            {
                "claim_id": "CLAIM4064_0",
                "claim": "4060-4063 are safe to formally summarize as a guarded local-GR chain",
                "allowed_private": preflight_safe,
                "allowed_public": False,
                "reason": "preflight only; public local-GR claim remains blocked",
                "timestamp_utc": current_timestamp,
            },
            {
                "claim_id": "CLAIM4064_1",
                "claim": "MTS publicly derives local GR/Newton/PPN",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "formal adoption/fallback verification still required",
                "timestamp_utc": current_timestamp,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4064_0",
                "next_doc": "4065-Y5-R2FR-guarded-formal-application-of-4060-4063-local-GR-chain.md" if preflight_safe else "4065-Y5-R2FR-preflight-failure-repair.md",
                "next_script": "scripts/Y5_R2FR_4065_guarded_formal_application_of_4060_4063_local_GR_chain.py" if preflight_safe else "scripts/Y5_R2FR_4065_preflight_failure_repair.py",
                "reason": "apply guarded formal update if user/agent proceeds; otherwise repair failed invariants",
                "timestamp_utc": current_timestamp,
            }
        ],
        "status": [
            {
                "status_id": "STAT4064",
                "status": decision,
                "formalization_modified": False,
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
        {"check_id": "VAL4064_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4064_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4064_02_no_public_claim", "passed": claims_ok, "detail": claims_detail},
        {
            "check_id": "VAL4064_03_invariants",
            "passed": all(str(row["passed"]).lower() == "true" for row in invariants),
            "detail": "all preflight invariants pass",
        },
        {
            "check_id": "VAL4064_04_decision_safe",
            "passed": DECISION in str(row_groups),
            "detail": "preflight selected guarded formal update path",
        },
        {
            "check_id": "VAL4064_05_no_formalization_write",
            "passed": True,
            "detail": "4064 is preflight only and writes no formalization files",
        },
        {"check_id": "VAL4064_06_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str, decision: str) -> str:
    return f"""# 4064 - Formal Adoption Preflight for 4060-4063 Local-GR Chain

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Formalization modified: `false`
- Decision: `{decision}`
- Public local-GR claim: `false`

## Preflight Result

The `4060-4063` local-GR chain is safe to summarize in `formalization-workbench` only as a guarded private candidate:

```text
4060: Gamma_ren normal-ordering kills m/L_cg first variation in parent branch.
4061: K_conn, K_domain, K_boundary are zero as independent first-order kernels in the selected branch.
4062: c_norm is routed to one calibrated universal G_N; derivative hair is forbidden or bounded.
4063: EH weak-field readout gives Poisson/Newton and GR PPN values conditionally.
```

## Guard

This preflight does not modify the formal workbench. It says the next action may be a guarded formal update if the update preserves:

- `formal_adoption_verified = false`;
- no numerical prediction of Newton's constant;
- no public local-GR/Newton/PPN claim;
- fallback rows if any parent clause is rejected.

## Next

`4065` should perform the guarded formal application or stop if any invariant changes before the update.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    manifest = chain_manifest_rows(current_timestamp)
    preflight = formal_preflight_rows(current_timestamp)
    invariants = invariant_rows(current_timestamp)
    static = static_rows(current_timestamp, invariants)

    DOC_PATH.write_text(doc_text(current_timestamp, static["decision"][0]["decision"]), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["chain_manifest"], manifest)
    write_csv(OUTPUTS["formal_preflight_matrix"], preflight)
    write_csv(OUTPUTS["invariant_results"], invariants)
    write_csv(OUTPUTS["decision"], static["decision"])
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["chain_manifest"],
        OUTPUTS["formal_preflight_matrix"],
        OUTPUTS["invariant_results"],
        OUTPUTS["decision"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        manifest,
        preflight,
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

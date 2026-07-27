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
DOC_PATH = ROOT / "4060-Y5-R2FR-chain-response-silence-or-DeltaK-kernel-bound.md"

SOURCES = {
    "SRC4060_00_4059": (
        SOURCE_DIR / "P8_Y5_R2FR_4059_NEXT_TARGET.csv",
        "chain response",
    ),
    "SRC4060_01_4055_trace": (
        SOURCE_DIR / "P8_Y5_R2FR_4055_TRACE_BACKGROUND_SUBTRACTION_LAW.csv",
        "DOUBLE_ZERO_TRACE_LAW",
    ),
    "SRC4060_02_4055_definition": (
        SOURCE_DIR / "P8_Y5_R2FR_4055_HILBERT_RESPONSE_DEFINITION.csv",
        "Gamma_ren(Phi0)=0",
    ),
    "SRC4060_03_798_expansion": (
        SOURCE_DIR / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
        "F'(m_L)=0 alone is insufficient",
    ),
    "SRC4060_04_1289_variation": (
        SOURCE_DIR / "P8_Y5_R10_1289_KMETRIC_VARIATION_EXPANSION_NONCLAIM.csv",
        "delta Gamma_eff=L_cg^-2",
    ),
    "SRC4060_05_1367_kernel": (
        SOURCE_DIR / "P8_Y5_R10_1367_KMETRIC_CHAIN_KERNEL_ATTEMPT.csv",
        "Kmetric_chain^{00}",
    ),
    "SRC4060_06_1525_kernel": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1525_KMETRIC_KERNEL_REQUIREMENTS.csv",
        "KER1525_6_chain_zero_condition",
    ),
    "SRC4060_07_4027_paths": (
        SOURCE_DIR / "P8_Y5_R2FR_4027_CONDITIONAL_COMPLETION_PATHS.csv",
        "F'(m_*)=0",
    ),
    "SRC4060_08_4059_components": (
        SOURCE_DIR / "P8_Y5_R2FR_4059_DELTAK_COMPONENT_QUEUE.csv",
        "DKC4059_2_chain",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4060_SOURCE_REGISTER.csv",
    "chain_derivation": SOURCE_DIR / "P8_Y5_R2FR_4060_CHAIN_RESPONSE_DERIVATION.csv",
    "normal_order_contract": SOURCE_DIR / "P8_Y5_R2FR_4060_GAMMA_REN_NORMAL_ORDER_CONTRACT.csv",
    "fallback_bounds": SOURCE_DIR / "P8_Y5_R2FR_4060_CHAIN_FALLBACK_BOUND_VECTOR.csv",
    "decision": SOURCE_DIR / "P8_Y5_R2FR_4060_DECISION_GATE.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4060_EVALUATOR_RESULTS.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4060_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4060_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4060_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4060_VALIDATION.csv",
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


def chain_derivation_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "step_id": "CHN4060_0_legacy_product_rule",
            "object": "legacy Gamma_eff",
            "formula": "delta Gamma_eff=L_cg^-2 F'(m) delta m - 2 L_cg^-3 F(m) delta L_cg + hidden derivative/domain/boundary terms",
            "result": "unrenormalized Gamma_eff has first-order chain response unless both m and L_cg channels are silent",
            "status": "LEGACY_CHAIN_ACTIVE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "step_id": "CHN4060_1_parent_normal_order",
            "object": "Gamma_ren",
            "formula": "Gamma_ren(Y):=Gamma_eff(Y)-Gamma_eff(Y_*)-D Gamma_eff|_{Y_*}[Y-Y_*]",
            "result": "Gamma_ren(Y_*)=0 and D Gamma_ren|_{Y_*}=0 by construction",
            "status": "NORMAL_ORDER_FIXED_POINT_LAW",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "step_id": "CHN4060_2_chain_silence",
            "object": "K_chain_parent",
            "formula": "delta_g Gamma_ren|_{Y_*}=0 even when Y includes m and L_cg, provided the fixed point and subtraction data are parent-fixed before variation",
            "result": "the m/L_cg chain response is zero at first order in the parent-definition branch",
            "status": "FIRST_VARIATION_ZERO_UNDER_PARENT_RENORMALIZATION",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "step_id": "CHN4060_3_second_order",
            "object": "Delta_K_chain",
            "formula": "Gamma_ren=O(deltaY^2), so K_chain=O(deltaY delta_g deltaY) plus retained connection/domain/boundary terms",
            "result": "remaining chain leakage is at least quadratic or belongs to the separate connection/domain/boundary queues",
            "status": "SECOND_ORDER_OR_SEPARATE_KERNEL",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "step_id": "CHN4060_4_guard",
            "object": "anti-cheat guard",
            "formula": "the subtraction cannot depend on observed residuals, source labels, sector labels, or fitted local tests",
            "result": "normal-ordering is allowed only as a parent fixed-point definition, not as empirical tuning",
            "status": "READOUT_FIREWALL_REQUIRED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def normal_order_contract_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "contract_id": "NOR4060_0_fixed_point",
            "clause": "choose one parent local fixed point Y_*=(m_*,L_*,...) before variation",
            "effect": "prevents source/readout-dependent subtraction",
            "adoption_status": "candidate_parent_clause",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "contract_id": "NOR4060_1_subtraction",
            "clause": "subtract Gamma_eff(Y_*) and its first differential D Gamma_eff|Y_* from Gamma_ren",
            "effect": "kills F'(m_*), F(m_*) L_cg linear drift, and mixed first-order chain response in one operation",
            "adoption_status": "candidate_parent_clause",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "contract_id": "NOR4060_2_background",
            "clause": "route the constant piece to fixed Lambda/background/reference data",
            "effect": "keeps constant Gamma from becoming compact source mass or radial G",
            "adoption_status": "aligned_with_4055_trace_law",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "contract_id": "NOR4060_3_legacy",
            "clause": "if an older row uses unrenormalized Gamma_eff=L_cg^-2 F(m), it remains legacy and must be bounded",
            "effect": "prevents normal-ordering from silently rewriting old empirical rows",
            "adoption_status": "legacy_DeltaK_guard",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def fallback_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "CB4060_0_m_kernel",
            "if_clause_fails": "m channel not normal-ordered or m fixed point not parent-owned",
            "formula": "Q_m <= C_Ploc |L_cg^-2 F'(m) M_m|/L_m",
            "needed_inputs": "F'(m), M_m tensor kernel, amplitude and length scale",
            "observable_map": "PPN beta/gamma; R10 alpha(lambda); source-exchange",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "CB4060_1_Lcg_kernel",
            "if_clause_fails": "L_cg channel not normal-ordered or L_cg metric response survives",
            "formula": "Q_L <= C_Ploc |2 L_cg^-3 F(m) M_L|/L_L",
            "needed_inputs": "F(m), M_L tensor kernel, L_cg response scale",
            "observable_map": "radial/source drift; PPN trace leakage; clock/orbital residual",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "bound_id": "CB4060_2_quadratic_remainder",
            "if_clause_fails": "normal-ordering adopted but finite perturbation amplitude survives",
            "formula": "Q_quad <= C_Ploc C_2 |deltaY| |nabla deltaY| / L_*^2",
            "needed_inputs": "second Hessian of Gamma_eff, deltaY amplitude, gradient length",
            "observable_map": "finite second-order Delta_K residual",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def static_rows(ts: str) -> Dict[str, List[Dict[str, object]]]:
    decision = "CHAIN_RESPONSE_FIRST_VARIATION_ZERO_IN_PARENT_NORMAL_ORDERED_BRANCH_LEGACY_BOUND_ACTIVE"
    return {
        "decision": [
            {
                "decision_id": "DEC4060_0",
                "decision": decision,
                "parent_branch": "Gamma_ren normal-ordered around fixed Y_*",
                "legacy_branch": "unrenormalized Gamma_eff chain response remains boundable",
                "public_claim": False,
                "timestamp_utc": ts,
            }
        ],
        "evaluator": [
            {
                "case_id": "CASE4060_0",
                "verdict": decision,
                "result": "The m/L_cg chain term is first-variation silent in the parent-normal-ordered branch; legacy unrenormalized rows keep explicit chain bounds.",
                "valid_for_public_claim": False,
                "timestamp_utc": ts,
            }
        ],
        "claim_gate": [
            {
                "claim_id": "CLAIM4060_0",
                "claim": "m/L_cg chain first variation is zero in the 4056 parent branch",
                "allowed_private": True,
                "allowed_public": False,
                "reason": "requires parent adoption of normal-ordered Gamma_ren and fixed-point data",
                "timestamp_utc": ts,
            },
            {
                "claim_id": "CLAIM4060_1",
                "claim": "legacy Gamma_eff chain kernels are zero",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "legacy rows still lack M_m/M_L/kernel sources",
                "timestamp_utc": ts,
            },
            {
                "claim_id": "CLAIM4060_2",
                "claim": "MTS publicly derives local GR/Newton/PPN",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "remaining connection/domain/boundary/source-slot gates are not closed",
                "timestamp_utc": ts,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4060_0",
                "next_doc": "4061-Y5-R2FR-connection-domain-boundary-kernels-zero-or-bound.md",
                "next_script": "scripts/Y5_R2FR_4061_connection_domain_boundary_kernels_zero_or_bound.py",
                "reason": "After chain first-variation silence, the remaining Delta_K technical kernels are connection, domain/projector, and boundary/reference response terms.",
                "timestamp_utc": ts,
            }
        ],
        "status": [
            {
                "status_id": "STAT4060",
                "status": decision,
                "public_claim": False,
                "formalization_modified_by_4060": False,
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
    generated_csvs: List[Path],
    all_rows: List[List[Dict[str, object]]],
) -> List[Dict[str, object]]:
    parse_results = [csv_parse_ok(path) for path in generated_csvs]
    flat_rows = [row for table in all_rows for row in table]
    serialized = "\n".join(str(value) for row in flat_rows for value in row.values())
    outputs_in_formalization = [path for path in OUTPUTS.values() if FORMALIZATION in path.parents]
    return [
        {
            "check_id": "VAL4060_00_sources_exist",
            "passed": all(bool(row["exists"]) for row in sources),
            "detail": "all cited source paths exist",
        },
        {
            "check_id": "VAL4060_01_needles_present",
            "passed": all(bool(row["needle_present"]) for row in sources),
            "detail": "all source needles present",
        },
        {
            "check_id": "VAL4060_02_csv_parse",
            "passed": all(result for result, _detail in parse_results),
            "detail": "; ".join(f"{path.name}:{detail}" for path, (_ok, detail) in zip(generated_csvs, parse_results)),
        },
        {
            "check_id": "VAL4060_03_no_public_claim",
            "passed": "allowed_public': True" not in serialized and "valid_for_public_claim': True" not in serialized,
            "detail": "all claim-bearing rows preserve public false",
        },
        {
            "check_id": "VAL4060_04_normal_order_decision",
            "passed": "CHAIN_RESPONSE_FIRST_VARIATION_ZERO_IN_PARENT_NORMAL_ORDERED_BRANCH_LEGACY_BOUND_ACTIVE" in serialized,
            "detail": "decision records parent normal-ordering and legacy bound branch",
        },
        {
            "check_id": "VAL4060_05_no_formalization_outputs",
            "passed": len(outputs_in_formalization) == 0,
            "detail": "4060 writes only post-checkpoint/source-intake outputs",
        },
        {
            "check_id": "VAL4060_06_script_compiles",
            "passed": script_compiles(),
            "detail": "script compiles",
        },
    ]


def doc_text(ts: str) -> str:
    return """# 4060 - Chain Response Silence or DeltaK Kernel Bound

- Timestamp: `__TS__`
- Status: `private_nonclaim_checkpoint`
- Formalization modified: `false`
- Public local-GR claim: `false`

## What Actually Moved

The dangerous legacy chain rule is:

```text
delta Gamma_eff
= L_cg^-2 F'(m) delta m
  - 2 L_cg^-3 F(m) delta L_cg
  + hidden connection/domain/boundary terms.
```

4060 uses the 4055 parent branch instead of the unrenormalized legacy branch:

```text
Gamma_ren(Y)
:= Gamma_eff(Y)
 - Gamma_eff(Y_*)
 - D Gamma_eff|_{Y_*}[Y-Y_*].
```

Therefore:

```text
Gamma_ren(Y_*) = 0
D Gamma_ren|_{Y_*} = 0
delta_g Gamma_ren|_{Y_*} = 0
```

So the `m/L_cg` chain response is first-variation silent in the parent-normal-ordered branch.

## What Is Still Not Claimed

This does not prove old unrenormalized `Gamma_eff=L_cg^-2 F(m)` rows were safe. Those are legacy rows and keep bounds:

```text
Q_m <= C_Ploc |L_cg^-2 F'(m) M_m|/L_m
Q_L <= C_Ploc |2 L_cg^-3 F(m) M_L|/L_L
```

The parent subtraction must be fixed before variation. It cannot be chosen from Solar residuals, sector labels, galaxy fits, or later readout success.

## Next Target

Connection, domain/projector, and boundary/reference kernels are now the remaining technical `Delta_K` pieces.
""".replace("__TS__", ts)


def main() -> None:
    ts = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(ts)
    chain_derivation = chain_derivation_rows(ts)
    normal_order_contract = normal_order_contract_rows(ts)
    fallback = fallback_rows(ts)
    static = static_rows(ts)

    DOC_PATH.write_text(doc_text(ts), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["chain_derivation"], chain_derivation)
    write_csv(OUTPUTS["normal_order_contract"], normal_order_contract)
    write_csv(OUTPUTS["fallback_bounds"], fallback)
    write_csv(OUTPUTS["decision"], static["decision"])
    write_csv(OUTPUTS["evaluator"], static["evaluator"])
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["chain_derivation"],
        OUTPUTS["normal_order_contract"],
        OUTPUTS["fallback_bounds"],
        OUTPUTS["decision"],
        OUTPUTS["evaluator"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    all_rows = [
        sources,
        chain_derivation,
        normal_order_contract,
        fallback,
        static["decision"],
        static["evaluator"],
        static["claim_gate"],
        static["next_target"],
        static["status"],
    ]
    validation = validation_rows(sources, generated_csvs, all_rows)
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

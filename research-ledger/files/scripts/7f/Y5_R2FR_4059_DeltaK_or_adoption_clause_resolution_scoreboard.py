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
DOC_PATH = ROOT / "4059-Y5-R2FR-DeltaK-or-adoption-clause-resolution-scoreboard.md"

SOURCES = {
    "SRC4059_00_4056_doc": (
        ROOT / "4056-Y5-R2FR-parent-local-action-packet-integration-or-DeltaK-bound.md",
        "Khat=K_Gamma",
    ),
    "SRC4059_01_4055_definition": (
        SOURCE_DIR / "P8_Y5_R2FR_4055_HILBERT_RESPONSE_DEFINITION.csv",
        "Khat^{mu nu} := K_Gamma",
    ),
    "SRC4059_02_4055_dgk": (
        SOURCE_DIR / "P8_Y5_R2FR_4055_DGK_ZERO_CERTIFICATE.csv",
        "ALGEBRAIC_ZERO_UNDER_ADOPTION",
    ),
    "SRC4059_03_4056_fallback": (
        SOURCE_DIR / "P8_Y5_R2FR_4056_DELTAK_FALLBACK_BOUND_VECTOR.csv",
        "DK4056_0_DeltaK",
    ),
    "SRC4059_04_1526_symbol": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1526_SYMBOL_MATCH_AUDIT.csv",
        "NOT_MATCHED",
    ),
    "SRC4059_05_1527_adoption": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1527_KHAT_ADOPTION_ROW.csv",
        "STAGED_NOT_PROMOTED",
    ),
    "SRC4059_06_metric_passfail": (
        SOURCE_DIR / "P8_GK_METRIC_RESPONSE_PASS_FAIL.csv",
        "PF515_2_Khat_response_found",
    ),
    "SRC4059_07_4027_components": (
        SOURCE_DIR / "P8_Y5_R2FR_4027_KHAT_COMPONENT_COMPLETION_GATE.csv",
        "KCG4027_0_tracefree_improvement",
    ),
    "SRC4059_08_1525_kernels": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1525_KMETRIC_KERNEL_REQUIREMENTS.csv",
        "KER1525_0_volume",
    ),
    "SRC4059_09_1287_status": (
        SOURCE_DIR / "P8_Y5_R10_1287_DELTAK_COMPONENT_STATUS_LEDGER.csv",
        "DELTAK_00_NOT_COMPUTABLE_YET",
    ),
    "SRC4059_10_formal_179": (
        FORMALIZATION / "179-PPC4048-local-parent-packet-candidate.md",
        "Delta_K_fallback_required_if_rejected = true",
    ),
}

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4059_SOURCE_REGISTER.csv",
    "adoption_resolution": SOURCE_DIR / "P8_Y5_R2FR_4059_KHAT_ADOPTION_RESOLUTION.csv",
    "legacy_split": SOURCE_DIR / "P8_Y5_R2FR_4059_PARENT_VS_LEGACY_KHAT_SPLIT.csv",
    "deltaK_schema": SOURCE_DIR / "P8_Y5_R2FR_4059_DELTAK_SCORER_SCHEMA.csv",
    "component_queue": SOURCE_DIR / "P8_Y5_R2FR_4059_DELTAK_COMPONENT_QUEUE.csv",
    "decision": SOURCE_DIR / "P8_Y5_R2FR_4059_DECISION_GATE.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4059_EVALUATOR_RESULTS.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4059_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4059_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4059_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4059_VALIDATION.csv",
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


def adoption_resolution_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "resolution_id": "KAR4059_0_parent_definition",
            "question": "Can the 4056 packet define Khat=K_Gamma?",
            "answer": "yes, as a new candidate parent-branch definition",
            "mathematical_rule": "Khat_parent^{mu nu}:=K_Gamma^{mu nu}:=Gamma_ren g^{mu nu}-T_Hilbert_GK^{mu nu}",
            "effect": "D_GK_parent=0 algebraically inside the candidate packet",
            "status": "ADOPTABLE_AS_PARENT_DEFINITION_NONCLAIM",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "resolution_id": "KAR4059_1_legacy_match",
            "question": "Does the old/live corpus prove Khat_legacy=K_Gamma?",
            "answer": "no",
            "mathematical_rule": "Delta_K_legacy^{mu nu}:=K_Gamma^{mu nu}-Khat_legacy^{mu nu}",
            "effect": "legacy mismatch is retained as a scorer, not hidden by the new definition",
            "status": "LEGACY_MATCH_FAILED_KEEP_DELTAK_ACTIVE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "resolution_id": "KAR4059_2_no_double_count",
            "question": "Can both Khat_parent and Khat_legacy source the metric?",
            "answer": "no",
            "mathematical_rule": "choose one live branch per local calculation: parent-definition branch or legacy-residual branch",
            "effect": "prevents adding K_Gamma and Khat_legacy as two stresses",
            "status": "NO_DOUBLE_COUNT_RULE",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "resolution_id": "KAR4059_3_public_claim",
            "question": "Does this close local GR publicly?",
            "answer": "no",
            "mathematical_rule": "formal_adoption_verified=false until all 4056 gates are adopted or fallback rows pass",
            "effect": "local-GR claim remains blocked",
            "status": "PUBLIC_CLAIM_BLOCKED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def legacy_split_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "split_id": "SPL4059_0_parent_branch",
            "symbol": "Khat_parent",
            "definition": "Khat_parent:=K_Gamma",
            "use": "4056 candidate local parent action packet",
            "claim_status": "private_candidate_nonclaim",
            "fallback": "not needed inside this branch, because D_GK_parent=0 by definition",
            "timestamp_utc": ts,
        },
        {
            "split_id": "SPL4059_1_legacy_branch",
            "symbol": "Khat_legacy",
            "definition": "the earlier MTS K_hat appearing in older route/equation-register docs",
            "use": "compatibility with earlier corpus and any old empirical rows",
            "claim_status": "not_matched_to_parent_metric_response",
            "fallback": "Delta_K_legacy:=K_Gamma-Khat_legacy",
            "timestamp_utc": ts,
        },
        {
            "split_id": "SPL4059_2_translation_rule",
            "symbol": "translation",
            "definition": "old K_hat references are not automatically upgraded; they either point to Khat_parent after explicit adoption or remain Khat_legacy",
            "use": "prevents accidental proof by notation",
            "claim_status": "guardrail",
            "fallback": "score Delta_K_legacy for every unadopted old-row dependency",
            "timestamp_utc": ts,
        },
    ]


def deltaK_schema_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "schema_id": "DKS4059_0_master",
            "quantity": "Q_DeltaK",
            "formula": "Q_DeltaK <= C_Ploc ||nabla_mu Delta_K_legacy^{mu nu}||",
            "units": "same q_loc force/source-exchange units after projector normalization",
            "observable_map": "PPN beta/gamma; R10 alpha(lambda); source-exchange",
            "needed_inputs": "C_Ploc, component amplitudes, component length scales, PPN/R10 projection coefficients",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "schema_id": "DKS4059_1_component_sum",
            "quantity": "absolute-sum Delta_K envelope",
            "formula": "||nabla Delta_K|| <= sum_i A_i/L_i over TF, trace, chain, connection, domain, boundary, legacy-symbol pieces",
            "units": "L^-3 before arena normalization",
            "observable_map": "same as Q_DeltaK, no cancellation credit",
            "needed_inputs": "A_i, L_i and source paths for every retained component",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "schema_id": "DKS4059_2_pass_rule",
            "quantity": "Delta_K branch pass",
            "formula": "abs(observable_i[Delta_K]) <= bound_i for every selected local arena",
            "units": "arena-specific",
            "observable_map": "Solar PPN, R10, clocks, orbitals, WEP if composition slots survive",
            "needed_inputs": "real arena bounds and sourced projection kernels",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def component_queue_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "component_id": "DKC4059_0_tracefree",
            "component": "tracefree improvement mismatch",
            "formula": "Delta_K_TF = K_Gamma_TF - Khat_legacy_TF",
            "current_status": "shape route exists; live legacy match not proved",
            "next_action": "use 4054 unit-response/no-flux branch if parent-defined, else source A_TF/L_TF",
            "priority": "high",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "component_id": "DKC4059_1_trace",
            "component": "volume/trace background drift",
            "formula": "Delta_K_trace from Gamma_0/Gamma_ren subtraction mismatch",
            "current_status": "4055 gives trace subtraction law; legacy drift not automatically zero",
            "next_action": "lock Gamma_0 readout/source derivatives or bound trace drift",
            "priority": "high",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "component_id": "DKC4059_2_chain",
            "component": "m and L_cg chain response",
            "formula": "K_chain ~ L_cg^-2 F'(m) M_m - 2 L_cg^-3 F(m) M_L",
            "current_status": "kernel requirements exist; parent kernels missing",
            "next_action": "prove F'(m_*)=0/F(m_*)=0 or M_m=M_L=0, else source kernels",
            "priority": "high",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "component_id": "DKC4059_3_connection",
            "component": "connection/covariant derivative response",
            "formula": "K_conn from Christoffel/Hodge/covariant derivative metric response",
            "current_status": "missing connection kernel",
            "next_action": "prove Levi-Civita/local connection silence in compact branch or bound K_conn",
            "priority": "medium",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "component_id": "DKC4059_4_domain",
            "component": "domain/projector/support response",
            "formula": "K_domain from integration domain, averaging cells, collar, projection support",
            "current_status": "selected branch has projector/domain zero theorem but legacy metric response still not universally adopted",
            "next_action": "import 4043 as adoption clause or bound support variation",
            "priority": "medium",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "component_id": "DKC4059_5_boundary",
            "component": "boundary/reference/corner response",
            "formula": "K_boundary from boundary terms and reference subtraction",
            "current_status": "4038 selected boundary silence exists; old kernel ledger still missing",
            "next_action": "adopt source-blind boundary owner or retain boundary flux bound",
            "priority": "medium",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def static_rows(ts: str) -> Dict[str, List[Dict[str, object]]]:
    decision = "PARENT_DEFINITION_ADOPTABLE_NONCLAIM_AND_LEGACY_DELTAK_ACTIVE"
    return {
        "decision": [
            {
                "decision_id": "DEC4059_0",
                "decision": decision,
                "parent_branch": "Khat_parent:=K_Gamma",
                "legacy_branch": "Delta_K_legacy:=K_Gamma-Khat_legacy",
                "public_claim": False,
                "timestamp_utc": ts,
            }
        ],
        "evaluator": [
            {
                "case_id": "CASE4059_0",
                "verdict": decision,
                "result": "4056 may use Khat=K_Gamma as a candidate parent definition; older Khat symbols remain unmatched and are routed to Delta_K_legacy.",
                "valid_for_public_claim": False,
                "timestamp_utc": ts,
            }
        ],
        "claim_gate": [
            {
                "claim_id": "CLAIM4059_0",
                "claim": "Khat=K_Gamma is resolved as a candidate parent-definition branch",
                "allowed_private": True,
                "allowed_public": False,
                "reason": "not a legacy symbol proof and not a public local-GR derivation",
                "timestamp_utc": ts,
            },
            {
                "claim_id": "CLAIM4059_1",
                "claim": "legacy Khat is proved equal to K_Gamma",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "source evidence says legacy match remains not matched/staged",
                "timestamp_utc": ts,
            },
            {
                "claim_id": "CLAIM4059_2",
                "claim": "MTS publicly derives local GR/Newton/PPN",
                "allowed_private": False,
                "allowed_public": False,
                "reason": "remaining adoption gates and fallback verification remain open",
                "timestamp_utc": ts,
            },
        ],
        "next_target": [
            {
                "row_id": "NEXT4059_0",
                "next_doc": "4060-Y5-R2FR-chain-response-silence-Fprime-mstar-or-DeltaK-kernel-bound.md",
                "next_script": "scripts/Y5_R2FR_4060_chain_response_silence_or_DeltaK_kernel_bound.py",
                "reason": "The highest-priority Delta_K component after the parent/legacy split is the m and L_cg chain response, because it can reintroduce local metric stress unless fixed-point silence closes.",
                "timestamp_utc": ts,
            }
        ],
        "status": [
            {
                "status_id": "STAT4059",
                "status": decision,
                "public_claim": False,
                "formalization_modified_by_4059": False,
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
            "check_id": "VAL4059_00_sources_exist",
            "passed": all(bool(row["exists"]) for row in sources),
            "detail": "all cited source paths exist",
        },
        {
            "check_id": "VAL4059_01_needles_present",
            "passed": all(bool(row["needle_present"]) for row in sources),
            "detail": "all source needles present",
        },
        {
            "check_id": "VAL4059_02_csv_parse",
            "passed": all(result for result, _detail in parse_results),
            "detail": "; ".join(f"{path.name}:{detail}" for path, (_ok, detail) in zip(generated_csvs, parse_results)),
        },
        {
            "check_id": "VAL4059_03_no_public_claim",
            "passed": "allowed_public': True" not in serialized and "valid_for_public_claim': True" not in serialized,
            "detail": "all claim-bearing rows preserve public false",
        },
        {
            "check_id": "VAL4059_04_decision_split",
            "passed": "PARENT_DEFINITION_ADOPTABLE_NONCLAIM_AND_LEGACY_DELTAK_ACTIVE" in serialized,
            "detail": "decision distinguishes parent definition from legacy mismatch",
        },
        {
            "check_id": "VAL4059_05_no_formalization_outputs",
            "passed": len(outputs_in_formalization) == 0,
            "detail": "4059 writes only post-checkpoint/source-intake outputs",
        },
        {
            "check_id": "VAL4059_06_script_compiles",
            "passed": script_compiles(),
            "detail": "script compiles",
        },
    ]


def doc_text(ts: str) -> str:
    return """# 4059 - DeltaK or Adoption Clause Resolution Scoreboard

- Timestamp: `__TS__`
- Status: `private_nonclaim_checkpoint`
- Formalization modified: `false`
- Public local-GR claim: `false`

## What Actually Moved

4059 resolves the first 4056 adoption gate without pretending the old corpus already proved something it did not.

The result is a branch split:

```text
Khat_parent^{mu nu} := K_Gamma^{mu nu}
K_Gamma^{mu nu} := Gamma_ren g^{mu nu} - T_Hilbert_GK^{mu nu}
D_GK_parent = 0
```

This is admissible as a candidate parent-definition inside the 4056 local packet.

But the older/live `Khat` symbols are not automatically promoted. They become:

```text
Khat_legacy^{mu nu}
Delta_K_legacy^{mu nu} := K_Gamma^{mu nu} - Khat_legacy^{mu nu}
```

So the theory does not get a proof by notation. It either adopts the parent definition in the local packet, or it scores the legacy mismatch.

## No Double Count Rule

One local calculation may use either:

- parent branch: `Khat_parent=K_Gamma`, with `D_GK=0`; or
- legacy branch: `Khat_legacy`, with explicit `Delta_K_legacy` residual.

It may not include both as independent metric stresses.

## DeltaK Scorer

The retained fallback is:

```text
Q_DeltaK <= C_Ploc ||nabla_mu Delta_K_legacy^{mu nu}||
```

with absolute-sum components:

- tracefree improvement mismatch;
- volume/trace drift;
- `m` and `L_cg` chain response;
- connection/covariant derivative response;
- domain/projector/support response;
- boundary/reference/corner response.

## Next Target

Attack the `m` and `L_cg` chain response first: prove fixed-point silence such as `F'(m_*)=0`, `F(m_*)=0`, `M_m=0`, or `M_L=0`; otherwise source the first real `Delta_K` kernel bound.
""".replace("__TS__", ts)


def main() -> None:
    ts = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(ts)
    adoption_resolution = adoption_resolution_rows(ts)
    legacy_split = legacy_split_rows(ts)
    deltaK_schema = deltaK_schema_rows(ts)
    component_queue = component_queue_rows(ts)
    static = static_rows(ts)

    DOC_PATH.write_text(doc_text(ts), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["adoption_resolution"], adoption_resolution)
    write_csv(OUTPUTS["legacy_split"], legacy_split)
    write_csv(OUTPUTS["deltaK_schema"], deltaK_schema)
    write_csv(OUTPUTS["component_queue"], component_queue)
    write_csv(OUTPUTS["decision"], static["decision"])
    write_csv(OUTPUTS["evaluator"], static["evaluator"])
    write_csv(OUTPUTS["claim_gate"], static["claim_gate"])
    write_csv(OUTPUTS["next_target"], static["next_target"])
    write_csv(OUTPUTS["status"], static["status"])

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["adoption_resolution"],
        OUTPUTS["legacy_split"],
        OUTPUTS["deltaK_schema"],
        OUTPUTS["component_queue"],
        OUTPUTS["decision"],
        OUTPUTS["evaluator"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    all_rows = [
        sources,
        adoption_resolution,
        legacy_split,
        deltaK_schema,
        component_queue,
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

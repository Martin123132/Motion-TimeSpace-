from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4750"
CLAIM_ID = "L-592"
MARKER = "PPC4161_QTR_PARENT_RANK_TEST_AND_CQUAR_CTT_SOURCE_RUNNER_4750"
PACKET_MARKER = "PPC4161_PACKET_QTR_PARENT_RANK_TEST_AND_CQUAR_CTT_SOURCE_RUNNER_4750"
DECISION = "QTR_PARENT_RANK_RUNNER_AND_CQUAR_CTT_SOURCE_ROWS_STAGED_FAIL_CLOSED_NONCLAIM"
NEXT_TARGET = "4751-Y5-R2FR-qtr-map-source-search-or-static-gap-numeric-smoke.md"

DOC_PATH = POST / "4750-Y5-R2FR-qtr-parent-rank-test-and-Cquar-CTT-source-runner.md"
FORMAL_PATH = FORMAL / "766-PPC4161-qtr-parent-rank-test-and-Cquar-CTT-source-runner.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4750_SOURCE_REGISTER.csv"
QTR_SOURCE_SCHEMA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4750_QTR_PARENT_RANK_SOURCE_SCHEMA.csv"
CQUAR_RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4750_CQUAR_SOURCE_RUNNER.csv"
CTT_RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4750_CTT_SOURCE_RUNNER.csv"
STATIC_GAP_RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4750_STATIC_GAP_SCORE_RUNNER.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4750_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4750_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4750_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4750_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4750_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4750_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4750_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4750_0_4749_doc", POST / "4749-Y5-R2FR-quarantine-map-coercivity-source-or-TT-topological-kernel-contract.md", "s_q=s_min(J_q)>0", "4749 rank handoff"),
    ("SRC4750_1_4749_formal", FORMAL / "765-PPC4161-quarantine-map-coercivity-source-or-TT-topological-kernel-contract.md", "s_min(J_q)>0", "formal 4749 rank condition"),
    ("SRC4750_2_4749_QMC", SOURCE_DIR / "P8_Y5_R2FR_4749_QUARANTINE_MAP_CONTRACT.csv", "QMC4749_3_rank_condition", "quarantine map contract"),
    ("SRC4750_3_4749_QRT", SOURCE_DIR / "P8_Y5_R2FR_4749_QUARANTINE_RANK_COHERCIVITY_TEST.csv", "QRT4749_3_combined_constant", "quarantine rank/coercivity bound"),
    ("SRC4750_4_4749_TTK", SOURCE_DIR / "P8_Y5_R2FR_4749_TT_TOPOLOGICAL_KERNEL_CONTRACT.csv", "TTK4749_2_zero_condition", "TT zero/bound contract"),
    ("SRC4750_5_4749_GAP", SOURCE_DIR / "P8_Y5_R2FR_4749_UPDATED_STATIC_GAP_BOUND.csv", "GAP4749_2_static_gap", "updated static gap law"),
    ("SRC4750_6_4749_LEDGER", SOURCE_DIR / "P8_Y5_R2FR_4749_SOURCE_VALUE_LEDGER.csv", "SRCVAL4749_0_Jq", "missing source ledger"),
    ("SRC4750_7_4749_NEXT", SOURCE_DIR / "P8_Y5_R2FR_4749_NEXT_TARGET.csv", "q_tr parent-rank source runner", "4750 target handoff"),
    ("SRC4750_8_4748_FORMAL", FORMAL / "764-PPC4161-TT-quarantine-symbol-hardening-and-static-gap-smoke-runner.md", "c_TT=0 for exact TT divergence", "TT exact-divergence precedent"),
    ("SRC4750_9_4747_CP", SOURCE_DIR / "P8_Y5_R2FR_4747_STATIC_GAP_CONSTANT_SOURCE_TABLE.csv", "CONST4747_1_CP_canonical", "canonical Poincare constant precedent"),
    ("SRC4750_10_4746_RESIDUAL", SOURCE_DIR / "P8_Y5_R2FR_4746_RESIDUAL_BOUND_LAW.csv", "RB4746_0_static", "static residual bound precedent"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    QTR_SOURCE_SCHEMA_CSV,
    CQUAR_RUNNER_CSV,
    CTT_RUNNER_CSV,
    STATIC_GAP_RUNNER_CSV,
    ROUTE_MATRIX_CSV,
    PROMOTION_GATES_CSV,
    FIREWALL_CSV,
    DECISION_CSV,
    STATUS_CSV,
    NEXT_TARGET_CSV,
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path_object: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path_object}")
    path_object.parent.mkdir(parents=True, exist_ok=True)
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def parse_csv(path_object: Path) -> bool:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path_object, needle, role in SOURCE_SPECS:
        exists = path_object.exists()
        text = read_text(path_object) if exists else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path_object),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def qtr_source_schema_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "QTRSCHEMA4750_0_Jq",
            "J_q",
            "parent algebraic q_tr map",
            "matrix/tensor map from parent fields X_q to q_tr",
            "source_path, definition, component basis, gauge/projector convention, units",
            "MISSING_PARENT_MAP",
        ),
        (
            "QTRSCHEMA4750_1_rankJq",
            "rank(J_q)",
            "algebraic rank of q_tr channel",
            "integer rank in chi target space",
            "dim_chi, chosen basis, exact or numerically certified rank tolerance",
            "MISSING_RANK_CERTIFICATE",
        ),
        (
            "QTRSCHEMA4750_2_sminJq",
            "s_min(J_q)",
            "algebraic singular-value lower bound",
            "positive numeric lower bound in normalized local norm",
            "norm definition, collar normalization, source derivation, uncertainty",
            "MISSING_SOURCE_VALUE",
        ),
        (
            "QTRSCHEMA4750_3_JK",
            "J_K",
            "parent K_own map",
            "matrix/tensor map from parent fields X_K to K_own",
            "source_path, component basis, antisymmetry/symmetry convention, units",
            "MISSING_PARENT_MAP",
        ),
        (
            "QTRSCHEMA4750_4_sminJK",
            "s_min(J_K)",
            "K-channel singular-value lower bound",
            "positive numeric lower bound for derivative channel after projector",
            "norm definition, p_min convention, source derivation",
            "MISSING_SOURCE_VALUE",
        ),
        (
            "QTRSCHEMA4750_5_penalties",
            "C_cross,C_quar_kernel",
            "mixing and unresolved-kernel penalties",
            "nonnegative numeric penalty constants",
            "source path for cross-term bound and kernel leakage certificate",
            "MISSING_PENALTY_BOUNDS",
        ),
        (
            "QTRSCHEMA4750_6_TT",
            "C_TT_kernel",
            "TT leakage into static gap",
            "zero certificate or finite leakage bound",
            "Pi_TT/P_loc source, boundary/corner/readout proof, finite-bound ledger",
            "MISSING_TT_KERNEL_CERTIFICATE",
        ),
        (
            "QTRSCHEMA4750_7_static",
            "C_P,L_loc,Pi_owner",
            "static arena constants and owner projection",
            "positive numeric values with units/normalization",
            "source path, arena definition, boundary conditions, uncertainty",
            "MISSING_STATIC_ARENA_INPUTS",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "schema_id": schema_id,
            "symbol": symbol,
            "definition": definition,
            "required_value": required_value,
            "required_provenance": required_provenance,
            "live_status": live_status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for schema_id, symbol, definition, required_value, required_provenance, live_status in specs
    ]


def cquar_source_runner_rows(timestamp: str) -> list[dict[str, Any]]:
    smoke_sq = 1.0
    smoke_sk = 1.0
    smoke_pmin = 1.0
    smoke_cross = 0.0
    smoke_kernel = 0.0
    smoke_cquar = smoke_sq**2 + smoke_pmin**2 * smoke_sk**2 - smoke_cross - smoke_kernel
    specs = [
        (
            "CQUAR4750_0_live_fail_closed",
            "live_parent_source",
            "MISSING",
            "MISSING",
            "MISSING",
            "MISSING",
            "MISSING",
            "MISSING",
            "MISSING",
            "",
            "FAIL_CLOSED_MISSING_PARENT_INPUTS",
            False,
            "Live branch has no parent-owned J_q/J_K numeric source rows yet.",
        ),
        (
            "CQUAR4750_1_algebraic_rule",
            "symbolic_rule",
            "dim_chi",
            "rank(J_q)",
            "s_q=s_min(J_q)",
            "s_K=s_min(J_K)",
            "p_min",
            "C_cross",
            "C_quar_kernel",
            "c_quar >= s_q^2 + p_min^2 s_K^2 - C_cross - C_quar_kernel",
            "RULE_READY_SOURCE_MISSING",
            False,
            "Formula is source-ready but not evidence until the input rows are real.",
        ),
        (
            "CQUAR4750_2_algebraic_shortcut",
            "symbolic_rule",
            "dim_chi",
            "rank(J_q)=dim_chi",
            "s_q>0",
            "optional",
            "optional",
            "0 or bounded",
            "C_quar_kernel",
            "c_quar >= s_q^2 - C_quar_kernel",
            "RULE_READY_SOURCE_MISSING",
            False,
            "If J_q is full-rank, K is not needed for p-independent control.",
        ),
        (
            "CQUAR4750_3_canonical_smoke",
            "canonical_nonclaim_smoke",
            "4",
            "4",
            smoke_sq,
            smoke_sk,
            smoke_pmin,
            smoke_cross,
            smoke_kernel,
            smoke_cquar,
            "PIPELINE_PASS_NONCLAIM",
            False,
            "Toy values only test schema, units, arithmetic and gate behavior.",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "runner_id": runner_id,
            "branch": branch,
            "dim_chi": dim_chi,
            "rank_Jq": rank_jq,
            "s_min_Jq": s_min_jq,
            "s_min_JK": s_min_jk,
            "p_min": p_min,
            "C_cross": c_cross,
            "C_quar_kernel": c_quar_kernel,
            "c_quar_lower_bound": c_quar_lower_bound,
            "status": status,
            "score_ready": score_ready,
            "valid_for_claim": False,
            "note": note,
            "timestamp_utc": timestamp,
        }
        for runner_id, branch, dim_chi, rank_jq, s_min_jq, s_min_jk, p_min, c_cross, c_quar_kernel, c_quar_lower_bound, status, score_ready, note in specs
    ]


def ctt_source_runner_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "CTT4750_0_live_fail_closed",
            "live_TT_source",
            "MISSING",
            "MISSING",
            "MISSING",
            "MISSING",
            "",
            "FAIL_CLOSED_MISSING_TT_PROJECTOR_AND_BOUNDARY_INPUTS",
            False,
            "No parent-owned Pi_TT/P_loc/boundary certificate has been sourced.",
        ),
        (
            "CTT4750_1_zero_condition",
            "symbolic_zero_rule",
            "parent-fixed Pi_TT and P_loc",
            "exact transversality",
            "no boundary/corner/readout leakage",
            "0",
            "C_TT_kernel=0 iff Pi_TT/P_loc are parent-fixed, transverse, and silent at boundary/readout",
            "ZERO_RULE_READY_SOURCE_MISSING",
            False,
            "This is the cleanest route but still requires a parent certificate.",
        ),
        (
            "CTT4750_2_finite_bound_rule",
            "symbolic_bound_rule",
            "imperfect projector/readout",
            "bounded nonTT leakage",
            "finite boundary/readout terms",
            "C_nonTT + C_projector + C_boundary_TT + C_readout_TT",
            "C_TT_kernel <= C_nonTT + C_projector + C_boundary_TT + C_readout_TT",
            "BOUND_RULE_READY_SOURCE_MISSING",
            False,
            "Fallback if exact topological silence cannot be signed.",
        ),
        (
            "CTT4750_3_canonical_zero_smoke",
            "canonical_nonclaim_smoke",
            "exact projector",
            "exact TT",
            "zero leakage by assumption",
            "0",
            "C_TT_kernel=0",
            "PIPELINE_PASS_NONCLAIM",
            False,
            "Toy row proves the gate can carry a zero without promoting it.",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "runner_id": runner_id,
            "branch": branch,
            "projector_input": projector_input,
            "transversality_input": transversality_input,
            "boundary_readout_input": boundary_readout_input,
            "C_TT_kernel_value_or_bound": ctt_value,
            "formula": formula,
            "status": status,
            "score_ready": score_ready,
            "valid_for_claim": False,
            "note": note,
            "timestamp_utc": timestamp,
        }
        for runner_id, branch, projector_input, transversality_input, boundary_readout_input, ctt_value, formula, status, score_ready, note in specs
    ]


def static_gap_score_rows(timestamp: str) -> list[dict[str, Any]]:
    cp = 1.0 / math.pi**2
    l_loc = 1.0
    c_tf = 1.0
    c_quar = 2.0
    c_mix = 0.0
    c_tt = 0.0
    c_dn_eff = min(c_tf, c_quar) - c_mix - c_tt
    lambda_lower = c_dn_eff / (cp * l_loc**2)
    residual_upper = math.sqrt((0.0**2) + (1.0**2 + 0.0) * cp * l_loc**2 / c_dn_eff)
    specs = [
        (
            "STATIC4750_0_live_fail_closed",
            "live_static_score",
            "MISSING",
            "MISSING",
            "MISSING",
            "MISSING",
            "MISSING",
            "lambda_1^stat >= [min(c_TFRI,c_quar)-C_mix_eff-C_TT_kernel]/(C_P L_loc^2)",
            "",
            "C_res_static <= Pi_owner^stat sqrt(CzeroMode_stat^2+(C_Dstat^2+C_boundary_stat) C_P L_loc^2 / c_DN_eff)",
            "",
            "FAIL_CLOSED_MISSING_STATIC_ARENA_INPUTS",
            False,
        ),
        (
            "STATIC4750_1_canonical_gap_smoke",
            "canonical_nonclaim_smoke",
            c_tf,
            c_quar,
            c_mix,
            c_tt,
            cp,
            "lambda_1^stat >= [min(c_TFRI,c_quar)-C_mix_eff-C_TT_kernel]/(C_P L_loc^2)",
            lambda_lower,
            "C_res_static <= Pi_owner^stat sqrt(CzeroMode_stat^2+(C_Dstat^2+C_boundary_stat) C_P L_loc^2 / c_DN_eff)",
            residual_upper,
            "PIPELINE_PASS_NONCLAIM",
            False,
        ),
        (
            "STATIC4750_2_promotion_rule",
            "symbolic_rule",
            "c_TFRI",
            "c_quar",
            "C_mix_eff",
            "C_TT_kernel",
            "C_P,L_loc,Pi_owner",
            "score_ready iff c_DN_eff>0 and every input is parent-owned/source-backed",
            "",
            "no local-GR/Newton claim from canonical smoke or placeholder rows",
            "",
            "RULE_READY_SOURCE_MISSING",
            False,
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "runner_id": runner_id,
            "branch": branch,
            "c_TFRI": c_tfri,
            "c_quar": cquar_value,
            "C_mix_eff": cmix,
            "C_TT_kernel": ctt,
            "C_P_or_static_inputs": cp_or_inputs,
            "lambda_formula": lambda_formula,
            "lambda_lower_bound": lambda_bound,
            "residual_formula": residual_formula,
            "C_res_static_upper": residual_bound,
            "status": status,
            "score_ready": score_ready,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for runner_id, branch, c_tfri, cquar_value, cmix, ctt, cp_or_inputs, lambda_formula, lambda_bound, residual_formula, residual_bound, status, score_ready in specs
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "ROUTE4750_0_Jq_rank_source",
            "Source parent J_q, rank(J_q), and s_min(J_q)",
            "If s_min(J_q)>0 and C_quar_kernel is zero/bounded, local static gap can become numerically scoreable.",
            "BEST_ROUTE",
        ),
        (
            "ROUTE4750_1_TT_zero_source",
            "Source parent Pi_TT/P_loc and boundary/readout silence",
            "If exact zero closes, C_TT_kernel stops eating the gap.",
            "PARALLEL_ROUTE",
        ),
        (
            "ROUTE4750_2_static_numeric_smoke",
            "Run real static gap score after source rows exist",
            "Only after J_q/J_K/C_TT/static constants are source-backed.",
            "DEFER_UNTIL_SOURCED",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "payoff": payoff,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, payoff, status in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4750_0_parent_Jq", "J_q source path, rank(J_q), s_min(J_q)>0", "BLOCKED_MISSING_PARENT_MAP"),
        ("GATE4750_1_Cquar", "C_quar lower bound numeric and positive after penalties", "BLOCKED_MISSING_PENALTY_BOUNDS"),
        ("GATE4750_2_CTT", "C_TT_kernel=0 or finite source-backed bound", "BLOCKED_MISSING_TT_CERTIFICATE"),
        ("GATE4750_3_static", "C_P,L_loc,Pi_owner,c_TFRI,C_mix_eff sourced", "BLOCKED_MISSING_STATIC_ARENA_INPUTS"),
        ("GATE4750_4_claim", "No local-GR/Newton/PPN claim until every previous gate passes", "FAIL_CLOSED_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "requirement": requirement,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, requirement, status in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4750_0_no_placeholder_rank", "Do not promote rank(J_q)=dim(chi) unless J_q is parent-owned and source-backed."),
        ("FW4750_1_no_TT_fake_gap", "Do not use exact TT divergence as c_TT>0; it is kernel/topological unless finite leakage is sourced."),
        ("FW4750_2_no_smoke_as_evidence", "Canonical smoke rows are plumbing tests only, never evidence."),
        ("FW4750_3_no_static_score_without_inputs", "Static gap score remains blocked until all source constants and projections are real."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, rule in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "meaning": "4750 converts the q_tr/TT coupling gap into source-ready runners plus nonclaim smoke rows; live local-GR scoring remains closed.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_FAIL_CLOSED_NONCLAIM",
            "summary": "QTR parent-rank schema, C_quar runner, C_TT runner and static gap smoke runner generated.",
            "claim_status": "NO_LOCAL_GR_OR_NEWTON_CLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "The runner exists; now either source real J_q/J_K/TT/kernel constants or run a deliberately nonclaim numeric static-gap smoke with those inputs.",
            "preferred_route": "Search parent action/source files for explicit q_tr map J_q, rank(J_q), s_min(J_q), J_K and C_quar_kernel rows.",
            "fallback_route": "Keep local branch closure-only and use canonical static gap smoke solely to stress-test the scoring pipeline.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullet(rows: list[dict[str, Any]], key_field: str, value_field: str) -> str:
    return "\n".join(f"- `{row[key_field]}`: {row[value_field]}" for row in rows)


def write_docs(
    timestamp: str,
    qtr_schema: list[dict[str, Any]],
    cquar_rows: list[dict[str, Any]],
    ctt_rows: list[dict[str, Any]],
    static_rows: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4750 Y5 R2FR: q_tr Parent-Rank Test And Cquar/CTT Source Runner

Generated: `{timestamp}`

## Purpose

4750 turns the 4749 coupling result into an executable source runner. The live branch remains blocked because no parent-owned numeric rows for `J_q`, `J_K`, `s_min(J_q)`, `C_quar_kernel`, or `C_TT_kernel` have been sourced yet. The canonical rows are smoke tests only.

## Core Test

The parent quarantine operator is:

```text
D_quar[X]^nu = J_q[X_q]^nu + nabla_mu J_K[X_K]^{{mu nu}}.
```

The static symbol lower bound is:

```text
c_quar >= s_q^2 + p_min^2 s_K^2 - C_cross - C_quar_kernel.
```

The short route is:

```text
rank(J_q)=dim(chi) and s_q=s_min(J_q)>0 => c_quar >= s_q^2 - C_quar_kernel.
```

## Source Schema

{bullet(qtr_schema, "schema_id", "symbol")}

## Cquar Runner

{bullet(cquar_rows, "runner_id", "status")}

## CTT Runner

{bullet(ctt_rows, "runner_id", "status")}

## Static Gap Score Runner

{bullet(static_rows, "runner_id", "status")}

## Promotion Gates

{bullet(gates, "gate_id", "status")}

## Route Matrix

{bullet(routes, "route_id", "route")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 766 PPC4161: q_tr Parent-Rank Test And Cquar/CTT Source Runner

Generated: `{timestamp}`

## QTR Parent Rank Runner

4750 creates the live/source and canonical-smoke rows needed to test the 4749 quarantine coupling law:

```text
c_quar >= s_q^2 + p_min^2 s_K^2 - C_cross - C_quar_kernel.
```

The key promotion condition is `rank(J_q)=dim(chi)` with `s_min(J_q)>0`, plus sourced penalties.

## TT Kernel Runner

The TT branch is admitted only as:

```text
C_TT_kernel=0
```

from an exact parent-fixed topological/superpotential certificate, or as a finite leakage bound. It is not a positive gap source.

## Static Score

The nonclaim smoke row verifies:

```text
lambda_1^stat >= [min(c_TFRI,c_quar)-C_mix_eff-C_TT_kernel]/(C_P L_loc^2).
```

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4750 builds source-ready runners for `J_q`, `rank(J_q)`, `s_min(J_q)`, `J_K`, `C_quar_kernel`, `C_TT_kernel`, and static score constants.
- The live branch is fail-closed because parent-owned numeric source rows are still missing.
- The canonical smoke branch passes plumbing only and remains `valid_for_claim=false`.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4750 local packet update: the coupling hunt now has an executable rank/source runner. The next move is not another audit; it is to search/source the actual parent `q_tr` map or run a deliberately nonclaim static smoke with explicit placeholder labels.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4750-Y5-R2FR-qtr-parent-rank-test-and-Cquar-CTT-source-runner.md`

## Decision

`{DECISION}`

## What moved forward

- Built the source schema for `J_q`, `rank(J_q)`, `s_min(J_q)`, `J_K`, `s_min(J_K)`, `C_cross`, `C_quar_kernel`, `C_TT_kernel`, `C_P`, `L_loc`, and `Pi_owner`.
- Added fail-closed live runners for `c_quar`, `C_TT_kernel`, and the static local-test score.
- Added canonical nonclaim smoke rows proving the pipeline arithmetic and CSV gates work without pretending the values are sourced.
- Kept the local-GR/Newton branch closed until parent-owned coupling/source rows exist.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
"""
    write_text(RESUME_PATH, resume)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr_newton_bridge",
        "4750 builds the q_tr parent-rank source runner and Cquar/CTT/static-gap smoke gates without opening a local-GR claim.",
        "Generated source register, QTR source schema, Cquar runner, CTT runner, static gap score runner, route matrix, promotion gates, firewalls, decision, status, next target and validation.",
        "qtr_parent_rank_source_runner_fail_closed_nonclaim",
        NEXT_TARGET,
        "Treating toy smoke values or placeholder parent maps as evidence.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need real parent-owned J_q,J_K,s_min values, kernel penalties, TT projector silence and static arena constants.",
        "QTR parent rank test and Cquar/CTT source runner",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    qtr_schema: list[dict[str, Any]],
    cquar_rows: list[dict[str, Any]],
    ctt_rows: list[dict[str, Any]],
    static_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4750_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), "source register"))
    checks.append(("VAL4750_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), "source register"))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4750_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    schema_symbols = {row["symbol"] for row in qtr_schema}
    checks.append(("VAL4750_2_rank_schema", "schema includes J_q, rank(J_q), s_min(J_q)", {"J_q", "rank(J_q)", "s_min(J_q)"}.issubset(schema_symbols), str(QTR_SOURCE_SCHEMA_CSV)))
    checks.append(("VAL4750_3_Cquar_live_fail_closed", "Cquar runner has fail-closed live branch", any(row["branch"] == "live_parent_source" and "FAIL_CLOSED" in row["status"] for row in cquar_rows), str(CQUAR_RUNNER_CSV)))
    checks.append(("VAL4750_4_Cquar_smoke_nonclaim", "Cquar runner has nonclaim smoke branch", any(row["branch"] == "canonical_nonclaim_smoke" and row["valid_for_claim"] is False for row in cquar_rows), str(CQUAR_RUNNER_CSV)))
    checks.append(("VAL4750_5_CTT_zero_and_bound", "CTT runner has zero condition and finite bound", any("C_TT_kernel=0" in row["formula"] for row in ctt_rows) and any("C_nonTT" in row["formula"] for row in ctt_rows), str(CTT_RUNNER_CSV)))
    checks.append(("VAL4750_6_static_formulas", "static runner includes lambda_1^stat and C_res_static", any("lambda_1^stat" in row["lambda_formula"] for row in static_rows) and any("C_res_static" in row["residual_formula"] for row in static_rows), str(STATIC_GAP_RUNNER_CSV)))
    checks.append(("VAL4750_7_static_live_fail_closed", "static runner has fail-closed live branch", any(row["branch"] == "live_static_score" and "FAIL_CLOSED" in row["status"] for row in static_rows), str(STATIC_GAP_RUNNER_CSV)))
    checks.append(("VAL4750_8_gates_nonclaim", "promotion gates keep claim closed", all(row["valid_for_claim"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4750_9_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4750_10_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4750_11_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4750_12_claim_row", "claim row L-592 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4750_13_resume", "resume points from 4750 to 4751", "4750-Y5" in resume_text and "4751-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4750_14_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
    overall = all(item[2] for item in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": validation_id,
            "check": check,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for validation_id, check, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4750_OVERALL",
            "check": "all 4750 local generation and fail-closed source-runner checks pass",
            "status": "PASS" if overall else "FAIL",
            "detail": DECISION,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    qtr_schema = qtr_source_schema_rows(timestamp)
    cquar_rows = cquar_source_runner_rows(timestamp)
    ctt_rows = ctt_source_runner_rows(timestamp)
    static_rows = static_gap_score_rows(timestamp)
    routes = route_matrix_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(QTR_SOURCE_SCHEMA_CSV, qtr_schema)
    write_csv(CQUAR_RUNNER_CSV, cquar_rows)
    write_csv(CTT_RUNNER_CSV, ctt_rows)
    write_csv(STATIC_GAP_RUNNER_CSV, static_rows)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, qtr_schema, cquar_rows, ctt_rows, static_rows, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, qtr_schema, cquar_rows, ctt_rows, static_rows, gates, timestamp))


if __name__ == "__main__":
    main()

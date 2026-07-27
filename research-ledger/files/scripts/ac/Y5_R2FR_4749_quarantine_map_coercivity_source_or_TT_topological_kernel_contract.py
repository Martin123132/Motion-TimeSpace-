from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4749"
CLAIM_ID = "L-591"
MARKER = "PPC4161_QUARANTINE_MAP_COERCIVITY_SOURCE_OR_TT_TOPOLOGICAL_KERNEL_CONTRACT_4749"
PACKET_MARKER = "PPC4161_PACKET_QUARANTINE_MAP_COERCIVITY_SOURCE_OR_TT_TOPOLOGICAL_KERNEL_CONTRACT_4749"
DECISION = "QUARANTINE_COERCIVITY_REDUCED_TO_QTR_PARENT_RANK_SMIN_AND_KOWN_KERNEL_TT_TOPOLOGICAL_CONTRACT_STAGED_NONCLAIM"
NEXT_TARGET = "4750-Y5-R2FR-qtr-parent-rank-test-and-Cquar-CTT-source-runner.md"

DOC_PATH = POST / "4749-Y5-R2FR-quarantine-map-coercivity-source-or-TT-topological-kernel-contract.md"
FORMAL_PATH = FORMAL / "765-PPC4161-quarantine-map-coercivity-source-or-TT-topological-kernel-contract.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4749_SOURCE_REGISTER.csv"
QUAR_MAP_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4749_QUARANTINE_MAP_CONTRACT.csv"
QUAR_RANK_TEST_CSV = SOURCE_DIR / "P8_Y5_R2FR_4749_QUARANTINE_RANK_COHERCIVITY_TEST.csv"
TT_TOPO_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4749_TT_TOPOLOGICAL_KERNEL_CONTRACT.csv"
UPDATED_GAP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4749_UPDATED_STATIC_GAP_BOUND.csv"
SOURCE_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4749_SOURCE_VALUE_LEDGER.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4749_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4749_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4749_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4749_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4749_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4749_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4749_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4749_0_4748_doc", POST / "4748-Y5-R2FR-TT-quarantine-symbol-hardening-and-static-gap-smoke-runner.md", "`q_tr/K_own` parent map is nondegenerate", "4749 handoff doc"),
    ("SRC4749_1_4748_formal", FORMAL / "764-PPC4161-TT-quarantine-symbol-hardening-and-static-gap-smoke-runner.md", "quarantine is the better", "formal quarantine result"),
    ("SRC4749_2_4748_next", SOURCE_DIR / "P8_Y5_R2FR_4748_NEXT_TARGET.csv", "quarantine q_tr/K_own map", "4749 target"),
    ("SRC4749_3_4748_quar", SOURCE_DIR / "P8_Y5_R2FR_4748_QUARANTINE_SYMBOL_HARDENING.csv", "QUAR4748_3_coercivity_candidate", "quarantine symbol hardening"),
    ("SRC4749_4_4748_TT", SOURCE_DIR / "P8_Y5_R2FR_4748_TT_SYMBOL_HARDENING.csv", "TT4748_4_owner_role", "TT kernel role"),
    ("SRC4749_5_4748_DN", SOURCE_DIR / "P8_Y5_R2FR_4748_DN_CONSTANT_UPDATE.csv", "DNU4748_2_effective_gap", "updated cDN formula"),
    ("SRC4749_6_4748_gate", SOURCE_DIR / "P8_Y5_R2FR_4748_STATIC_SCORE_GATE.csv", "SSG4748_1_quar", "quarantine score gate"),
    ("SRC4749_7_4747_constants", SOURCE_DIR / "P8_Y5_R2FR_4747_STATIC_GAP_CONSTANT_SOURCE_TABLE.csv", "CONST4747_2_cDN", "source-ready constants"),
    ("SRC4749_8_4746_residual", SOURCE_DIR / "P8_Y5_R2FR_4746_RESIDUAL_BOUND_LAW.csv", "RB4746_0_static", "static residual law"),
    ("SRC4749_9_4740_quar", SOURCE_DIR / "P8_Y5_R2FR_4740_PARENT_TFRI_OWNER_ACTION_BLOCK.csv", "S_quar = int chi_nu", "parent quarantine action"),
    ("SRC4749_10_4739_delta", SOURCE_DIR / "P8_Y5_R2FR_4739_CDELTAKDIV_ZERO_OR_BOUND_LAW.csv", "CDK4739_1_TT_kernel_zero", "TT kernel precedent"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    QUAR_MAP_CONTRACT_CSV,
    QUAR_RANK_TEST_CSV,
    TT_TOPO_CONTRACT_CSV,
    UPDATED_GAP_CSV,
    SOURCE_LEDGER_CSV,
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


def quar_map_contract_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "QMC4749_0_parent_fields",
            "X_quar=(X_q,X_K), q_tr=J_q X_q, K_own=J_K X_K",
            "The quarantine map must be a parent map from actual fields, not a notation-only current.",
            "PARENT_MAP_CONTRACT_WRITTEN",
        ),
        (
            "QMC4749_1_operator",
            "D_quar[X]^nu = J_q[X_q]^nu + nabla_mu J_K[X_K]^{mu nu}",
            "This is the sourced version of q_tr+nabla K_own.",
            "OPERATOR_CONTRACT",
        ),
        (
            "QMC4749_2_static_symbol",
            "sigma_quar^dagger(p)chi = (J_q^dagger chi, -i p_mu J_K^dagger chi)",
            "The symbol acts on chi through algebraic q and derivative K channels.",
            "HARDENED_PARENT_SYMBOL",
        ),
        (
            "QMC4749_3_rank_condition",
            "rank(J_q)=dim(chi) or s_min(J_q)>0",
            "The algebraic q channel is the shortest route to positive coercivity.",
            "RANK_TEST_REQUIRED",
        ),
        (
            "QMC4749_4_kernel_condition",
            "ker(J_q^dagger) cap ker(p_mu J_K^dagger)=0 for every spatial p",
            "If q is rank-deficient, K can help only for nonzero p and only outside its kernel.",
            "FULL_SYMBOL_TEST_REQUIRED",
        ),
        (
            "QMC4749_5_nonclaim",
            "If J_q/J_K are not parent-owned, carry C_quar_kernel and do not score.",
            "Prevents algebraic-control by pure notation.",
            "FAIL_CLOSED_RULE",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "contract_id": contract_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for contract_id, formula, meaning, status in specs
    ]


def quar_rank_test_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "QRT4749_0_symbol_norm",
            "||sigma_quar^dagger(p)chi||^2 = ||J_q^dagger chi||^2 + |p|_h^2||J_K^dagger chi||^2 + cross_terms",
            "Norm identity for the quarantine symbol.",
            "DERIVED_SYMBOLIC",
        ),
        (
            "QRT4749_1_algebraic_lower",
            "if s_q:=s_min(J_q)>0 then ||sigma_quar^dagger(p)chi||^2 >= s_q^2||chi||^2",
            "Full-rank q_tr gives a positive p-independent lower bound.",
            "COERCIVITY_THEOREM_CONDITIONAL",
        ),
        (
            "QRT4749_2_K_lower",
            "if s_K:=s_min(J_K)>0 then K channel adds |p|_h^2 s_K^2||chi||^2 for p!=0",
            "The K channel helps the static symbol but cannot replace missing p=0 algebraic control by itself.",
            "DERIVED_SYMBOLIC",
        ),
        (
            "QRT4749_3_combined_constant",
            "c_quar >= s_q^2 + p_min^2 s_K^2 - C_cross - C_quar_kernel",
            "Source-ready lower-bound form for c_quar.",
            "SOURCE_READY_BOUND",
        ),
        (
            "QRT4749_4_static_unit",
            "on unit spatial cotangent p_min=1, c_quar >= s_q^2+s_K^2-C_cross-C_quar_kernel",
            "Canonical static symbol test once the collar normalization is fixed.",
            "STATIC_SYMBOL_ROUTE",
        ),
        (
            "QRT4749_5_blocker",
            "numeric c_quar requires J_q,J_K,weights,cross terms and kernel projection sources",
            "This is the exact source list for quarantine coercivity.",
            "MISSING_SOURCE_VALUES",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "rank_test_id": test_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for test_id, formula, meaning, status in specs
    ]


def tt_topological_contract_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "TTK4749_0_exact_TT_kernel",
            "p_mu Pi_TT(p)^{mu nu}_{ab}=0 => P_loc nabla_mu Pi_TT[U]^{mu nu}=0 in the exact static symbol",
            "Exact TT divergence belongs to the kernel/topological sector.",
            "KERNEL_ROUTE",
        ),
        (
            "TTK4749_1_topological_owner",
            "S_TT must be boundary/topological/superpotential with zero bulk local metric response",
            "TT can help local quiet only by not sourcing bulk local stress.",
            "TOPOLOGICAL_CONTRACT_REQUIRED",
        ),
        (
            "TTK4749_2_zero_condition",
            "C_TT_kernel=0 if Pi_TT/P_loc are parent-fixed, transverse, no boundary/corner/readout leakage",
            "Exact zero condition for TT leakage.",
            "ZERO_CONDITION_CONDITIONAL",
        ),
        (
            "TTK4749_3_bound_condition",
            "C_TT_kernel <= C_nonTT + C_projector + C_boundary_TT + C_readout_TT",
            "Finite fallback if exact TT topological contract is not signed.",
            "BOUND_LAW",
        ),
        (
            "TTK4749_4_forbidden_route",
            "Do not set c_TT>0 for exact transverse TT divergence",
            "Blocks fake gap contribution from TT.",
            "FIREWALL",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "tt_contract_id": contract_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for contract_id, formula, meaning, status in specs
    ]


def updated_gap_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "GAP4749_0_effective_DN",
            "c_DN_eff >= min(c_TFRI,c_quar)-C_mix_eff-C_TT_kernel",
            "Updated static gap from 4748.",
            "CARRIED_FORWARD",
        ),
        (
            "GAP4749_1_quar_insert",
            "c_quar >= s_q^2 + p_min^2 s_K^2 - C_cross - C_quar_kernel",
            "Quarantine rank test inserted into the static gap route.",
            "UPDATED_SYMBOLIC_BOUND",
        ),
        (
            "GAP4749_2_static_gap",
            "lambda_1^stat >= [min(c_TFRI,c_quar)-C_mix_eff-C_TT_kernel]/(C_P L_loc^2)",
            "Static gap law after quarantine/TT split.",
            "DERIVED_SOURCE_READY_FORMULA",
        ),
        (
            "GAP4749_3_residual",
            "C_res_static <= Pi_owner^stat sqrt(CzeroMode_stat^2+(C_Dstat^2+C_boundary_stat) C_P L_loc^2 / c_DN_eff)",
            "Static local-test residual bound.",
            "SYMBOLIC_NONCLAIM",
        ),
        (
            "GAP4749_4_claim_gate",
            "score_ready only if c_DN_eff>0 and all constants/projections/kernel bounds are source-backed",
            "No local-test claim from symbolic gap law.",
            "FAIL_CLOSED",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gap_id": gap_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gap_id, formula, meaning, status in specs
    ]


def source_ledger_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRCVAL4749_0_Jq", "J_q", "parent algebraic q_tr map", "MISSING_PARENT_MAP"),
        ("SRCVAL4749_1_JK", "J_K", "parent K_own map", "MISSING_PARENT_MAP"),
        ("SRCVAL4749_2_sq", "s_q=s_min(J_q)", "algebraic q rank/coercivity constant", "MISSING_SOURCE_VALUE"),
        ("SRCVAL4749_3_sK", "s_K=s_min(J_K)", "K channel singular-value constant", "MISSING_SOURCE_VALUE"),
        ("SRCVAL4749_4_Ccross", "C_cross", "q/K symbol mixing penalty", "MISSING_SOURCE_VALUE"),
        ("SRCVAL4749_5_Cquar", "C_quar_kernel", "quarantine map-kernel leakage", "MISSING_SOURCE_VALUE"),
        ("SRCVAL4749_6_CTT", "C_TT_kernel", "TT topological/kernel leakage", "MISSING_SOURCE_VALUE"),
        ("SRCVAL4749_7_projectors", "Pi_TT/P_loc/Q_perp symbols", "projector symbol and boundary behavior", "MISSING_PARENT_PROJECTOR"),
        ("SRCVAL4749_8_static", "C_P,L_loc,Pi_owner,c_TFRI", "static scoring constants", "MISSING_SOURCE_VALUE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "source_value_id": value_id,
            "symbol": symbol,
            "definition": definition,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for value_id, symbol, definition, status in specs
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4749_0_qtr_rank", "source/prove J_q full-rank and s_q>0", "best_next_route", "shortest route to c_quar>0"),
        ("ROUTE4749_1_TT_kernel", "source C_TT_kernel=0 or finite bound from topological/superpotential contract", "parallel_required_route", "needed because TT is not a gap source"),
        ("ROUTE4749_2_K_channel", "source J_K and s_K to strengthen static nonzero-p gap", "parallel_source_route", "helps once q channel is known"),
        ("ROUTE4749_3_static_score", "score static PPN/R10 now", "rejected", "J_q/J_K/C_TT/projectors/constants are missing"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "status": status,
            "reason_or_next_requirement": requirement,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, status, requirement in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4749_0_sources", "All cited 4749 source anchors exist and contain expected text.", "pass_internal", False),
        ("GATE4749_1_quar_contract", "Quarantine parent map/rank contract is written.", "conditional_pass", False),
        ("GATE4749_2_rank_bound", "c_quar lower-bound law is source-ready but nonnumeric.", "conditional_pass_nonclaim", False),
        ("GATE4749_3_TT_contract", "TT topological/kernel contract is written.", "conditional_pass_nonclaim", False),
        ("GATE4749_4_missing_values", "J_q,J_K,s_q,s_K,C_TT_kernel,C_quar_kernel/projectors remain unsourced.", "closed_unsigned", False),
        ("GATE4749_5_score", "Static/local scoring remains fail-closed.", "closed_unsigned", False),
        ("GATE4749_6_no_claim", "No local-GR, Newton, PPN, R10, WEP, clock or orbital claim from 4749.", "closed_firewall", False),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "valid_for_claim": valid_for_claim,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, status, valid_for_claim in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4749_0_no_notation_rank", "Do not treat q_tr identity as full rank unless J_q is a parent-owned map."),
        ("FW4749_1_no_K_only_p0", "Do not let the derivative K channel replace algebraic q control at p=0."),
        ("FW4749_2_no_TT_gap", "Do not use exact transverse TT divergence as a positive gap source."),
        ("FW4749_3_no_symbolic_score", "Do not score static tests from symbolic singular values or kernel bounds."),
        ("FW4749_4_no_github_action", "No GitHub action is performed by this local checkpoint."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "firewall": firewall,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, firewall in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "summary": "4749 reduces quarantine coercivity to a parent rank/singular-value test for J_q and J_K, with c_quar bounded by s_q, s_K, cross terms and C_quar_kernel. TT is put on a topological/superpotential kernel contract with C_TT_kernel=0 or a finite bound. Static scoring remains fail-closed.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4749_0_local_only",
            "status": "local_only_private_checkpoint",
            "detail": "Generated local post-checkpoint and formalization files only; no GitHub action.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4749_1_science_verdict",
            "status": "quarantine_rank_test_and_TT_kernel_contract_written",
            "detail": "The coupling hunt is now a sourceable rank/singular-value problem for q_tr/K_own plus a TT kernel bound.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "4749 leaves the shortest decisive blockers as J_q rank/singular value and C_TT_kernel/C_quar_kernel source values.",
            "preferred_route": "Build a q_tr parent-rank source runner that records J_q, rank(J_q), s_min(J_q), and C_quar_kernel.",
            "fallback_route": "Build a TT topological kernel source runner for C_TT_kernel=0 or a finite bound.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullet(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    timestamp: str,
    quar_contract: list[dict[str, Any]],
    rank_tests: list[dict[str, Any]],
    tt_contract: list[dict[str, Any]],
    gap_rows: list[dict[str, Any]],
    source_ledger: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4749 Y5 R2FR: Quarantine Map Coercivity Source Or TT Topological Kernel Contract

Generated: `{timestamp}`

## Summary

- Work is local-only and private.
- This checkpoint turns the quarantine coupling candidate into a rank/singular-value test.
- Parent quarantine map:

```text
X_quar=(X_q,X_K)
q_tr = J_q X_q
K_own = J_K X_K
D_quar[X]^nu = J_q[X_q]^nu + nabla_mu J_K[X_K]^{{mu nu}}
sigma_quar^dagger(p)chi = (J_q^dagger chi, -i p_mu J_K^dagger chi)
```

- Coercivity route:

```text
if s_q=s_min(J_q)>0:
  ||sigma_quar^dagger(p)chi||^2 >= s_q^2 ||chi||^2

c_quar >= s_q^2 + p_min^2 s_K^2 - C_cross - C_quar_kernel
```

- TT route:

```text
exact TT divergence => c_TT=0
TT must be topological/superpotential or carried as C_TT_kernel
```

- No local-GR or local-test claim is made.

## Quarantine Map Contract

{bullet(quar_contract, "contract_id", "formula")}

## Quarantine Rank / Coercivity Test

{bullet(rank_tests, "rank_test_id", "formula")}

## TT Topological Kernel Contract

{bullet(tt_contract, "tt_contract_id", "formula")}

## Updated Static Gap Bound

{bullet(gap_rows, "gap_id", "formula")}

## Source Value Ledger

{bullet(source_ledger, "source_value_id", "symbol")}

## Route Matrix

{bullet(routes, "route_id", "route")}

## Promotion Gates

{bullet(gates, "gate_id", "status")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 765 PPC4161: Quarantine Map Coercivity Source Or TT Topological Kernel Contract

Generated: `{timestamp}`

## Quarantine Coupling Test

4749 rewrites the coupling issue as a parent-rank problem:

```text
sigma_quar^dagger(p)chi = (J_q^dagger chi, -i p_mu J_K^dagger chi).
```

If the parent algebraic map `J_q` has `s_min(J_q)>0`, then:

```text
||sigma_quar^dagger(p)chi||^2 >= s_min(J_q)^2 ||chi||^2.
```

So the quarantine branch can provide a real positive local-suppression gap only after `J_q/J_K` are source-backed parent maps.

## TT Contract

Exact TT transversality gives `c_TT=0` for the divergence route. TT must therefore be a topological/superpotential kernel with `C_TT_kernel=0`, or a finite source term.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4749 reduces quarantine coercivity to a parent map rank/singular-value test: `s_q=s_min(J_q)>0`.
- It derives `c_quar >= s_q^2 + p_min^2 s_K^2 - C_cross - C_quar_kernel`.
- TT is put on a topological/superpotential kernel contract: `C_TT_kernel=0` or a finite bound, not `c_TT>0`.
- Static gap updates to `c_DN_eff >= min(c_TFRI,c_quar)-C_mix_eff-C_TT_kernel`.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4749 local packet update: the local coupling hunt is now a sourceable rank/singular-value problem for `q_tr/K_own`, plus a TT kernel/topological source value.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4749-Y5-R2FR-quarantine-map-coercivity-source-or-TT-topological-kernel-contract.md`

## Decision

`{DECISION}`

## What moved forward

- Converted the quarantine coupling candidate into parent maps `J_q` and `J_K`.
- Derived the rank/singular-value condition: `s_min(J_q)>0` gives algebraic coercivity for `chi`.
- Derived the source-ready bound `c_quar >= s_q^2 + p_min^2 s_K^2 - C_cross - C_quar_kernel`.
- Put TT on a topological/kernel contract with `C_TT_kernel=0` or finite bound instead of fake `c_TT>0`.

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
        "4749 reduces quarantine coercivity to a parent rank/singular-value test and writes a TT topological/kernel contract.",
        "Generated source register, quarantine map contract, quarantine rank/coercivity test, TT topological kernel contract, updated gap bound, source ledger, route matrix, gates, firewalls, decision, status, next target and validation.",
        "quarantine_rank_test_TT_kernel_contract_nonclaim",
        NEXT_TARGET,
        "Treating q_tr as full-rank without parent map evidence, or using TT as a fake gap source.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need J_q,J_K,s_q,s_K,C_cross,C_quar_kernel,C_TT_kernel, projector symbols and static constants before scoring.",
        "Quarantine map coercivity source or TT topological kernel contract",
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
    quar_contract: list[dict[str, Any]],
    rank_tests: list[dict[str, Any]],
    tt_contract: list[dict[str, Any]],
    gap_rows: list[dict[str, Any]],
    source_ledger: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4749_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), "source register"))
    checks.append(("VAL4749_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), "source register"))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4749_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4749_2_quar_contract", "quarantine contract defines J_q/J_K and sigma_quar", any("J_q" in row["formula"] and "J_K" in row["formula"] for row in quar_contract) and any("sigma_quar" in row["formula"] for row in quar_contract), str(QUAR_MAP_CONTRACT_CSV)))
    checks.append(("VAL4749_3_rank_test", "rank test includes s_min(J_q) and c_quar bound", any("s_min(J_q)" in row["formula"] for row in rank_tests) and any("c_quar >=" in row["formula"] for row in rank_tests), str(QUAR_RANK_TEST_CSV)))
    checks.append(("VAL4749_4_TT_contract", "TT contract keeps C_TT_kernel and forbids c_TT>0 route", any("C_TT_kernel" in row["formula"] for row in tt_contract) and any("c_TT>0" in row["formula"] for row in tt_contract), str(TT_TOPO_CONTRACT_CSV)))
    checks.append(("VAL4749_5_gap_update", "updated gap includes c_quar and C_TT_kernel", any("c_quar" in row["formula"] and "C_TT_kernel" in row["formula"] for row in gap_rows), str(UPDATED_GAP_CSV)))
    checks.append(("VAL4749_6_source_ledger", "source ledger carries J_q and C_TT_kernel as missing", any(row["symbol"] == "J_q" for row in source_ledger) and any(row["symbol"] == "C_TT_kernel" for row in source_ledger), str(SOURCE_LEDGER_CSV)))
    checks.append(("VAL4749_7_gates_nonclaim", "promotion gates keep claim closed", all(row["valid_for_claim"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4749_8_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4749_9_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4749_10_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4749_11_claim_row", "claim row L-591 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4749_12_resume", "resume points from 4749 to 4750", "4749-Y5" in resume_text and "4750-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4749_13_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
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
            "validation_id": "VAL4749_OVERALL",
            "check": "all 4749 local generation and nonclaim checks pass",
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
    quar_contract = quar_map_contract_rows(timestamp)
    rank_tests = quar_rank_test_rows(timestamp)
    tt_contract = tt_topological_contract_rows(timestamp)
    gap_rows = updated_gap_rows(timestamp)
    source_ledger = source_ledger_rows(timestamp)
    routes = route_matrix_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(QUAR_MAP_CONTRACT_CSV, quar_contract)
    write_csv(QUAR_RANK_TEST_CSV, rank_tests)
    write_csv(TT_TOPO_CONTRACT_CSV, tt_contract)
    write_csv(UPDATED_GAP_CSV, gap_rows)
    write_csv(SOURCE_LEDGER_CSV, source_ledger)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, quar_contract, rank_tests, tt_contract, gap_rows, source_ledger, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, quar_contract, rank_tests, tt_contract, gap_rows, source_ledger, gates, timestamp))


if __name__ == "__main__":
    main()

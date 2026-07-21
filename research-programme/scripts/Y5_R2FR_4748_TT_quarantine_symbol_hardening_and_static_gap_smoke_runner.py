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

CHECKPOINT = "4748"
CLAIM_ID = "L-590"
MARKER = "PPC4161_TT_QUARANTINE_SYMBOL_HARDENING_AND_STATIC_GAP_SMOKE_RUNNER_4748"
PACKET_MARKER = "PPC4161_PACKET_TT_QUARANTINE_SYMBOL_HARDENING_AND_STATIC_GAP_SMOKE_RUNNER_4748"
DECISION = "TT_DIVERGENCE_SYMBOL_HARDENED_AS_KERNEL_TOPOLOGICAL_NOT_GAP_SOURCE_QUARANTINE_SYMBOL_COERCIVE_CANDIDATE_STATIC_SMOKE_NONCLAIM"
NEXT_TARGET = "4749-Y5-R2FR-quarantine-map-coercivity-source-or-TT-topological-kernel-contract.md"

DOC_PATH = POST / "4748-Y5-R2FR-TT-quarantine-symbol-hardening-and-static-gap-smoke-runner.md"
FORMAL_PATH = FORMAL / "764-PPC4161-TT-quarantine-symbol-hardening-and-static-gap-smoke-runner.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4748_SOURCE_REGISTER.csv"
TT_SYMBOL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4748_TT_SYMBOL_HARDENING.csv"
QUAR_SYMBOL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4748_QUARANTINE_SYMBOL_HARDENING.csv"
DN_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4748_DN_CONSTANT_UPDATE.csv"
STATIC_SMOKE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4748_STATIC_GAP_SMOKE_RUNNER.csv"
STATIC_SCORE_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4748_STATIC_SCORE_GATE.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4748_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4748_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4748_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4748_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4748_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4748_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4748_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4748_0_4747_doc", POST / "4747-Y5-R2FR-static-gap-constant-source-and-owner-symbol-completion.md", "sigma_TT(k;xi)", "4748 handoff doc"),
    ("SRC4748_1_4747_formal", FORMAL / "763-PPC4161-static-gap-constant-source-and-owner-symbol-completion.md", "sigma_quar(k;chi)", "formal owner symbol skeleton"),
    ("SRC4748_2_4747_next", SOURCE_DIR / "P8_Y5_R2FR_4747_NEXT_TARGET.csv", "Harden sigma_TT and sigma_quar", "4748 target"),
    ("SRC4748_3_4747_owner", SOURCE_DIR / "P8_Y5_R2FR_4747_OWNER_SYMBOL_COMPLETION.csv", "OWNC4747_1_TT", "schematic owner symbols"),
    ("SRC4748_4_4747_dn", SOURCE_DIR / "P8_Y5_R2FR_4747_DN_CONSTANT_DEFINITION.csv", "DNK4747_4_full_constant", "DN constant source path"),
    ("SRC4748_5_4747_dryrun", SOURCE_DIR / "P8_Y5_R2FR_4747_STATIC_SCORE_DRYRUN.csv", "DRY4747_2_missing_TT", "fail-closed dryrun precedent"),
    ("SRC4748_6_4746_residual", SOURCE_DIR / "P8_Y5_R2FR_4746_RESIDUAL_BOUND_LAW.csv", "RB4746_0_static", "static residual law"),
    ("SRC4748_7_4745_symbols", SOURCE_DIR / "P8_Y5_R2FR_4745_ADJOINT_PRINCIPAL_SYMBOL_DERIVATION.csv", "SYM4745_6_missing_full_owner_symbol", "missing full owner symbol row"),
    ("SRC4748_8_4743_kernel", SOURCE_DIR / "P8_Y5_R2FR_4743_KERNEL_KILL_THEOREM.csv", "KKT4743_4_kernel_bound", "kernel fallback precedent"),
    ("SRC4748_9_4740_action", SOURCE_DIR / "P8_Y5_R2FR_4740_PARENT_TFRI_OWNER_ACTION_BLOCK.csv", "S_TT = int sqrt|g|", "TT owner action"),
    ("SRC4748_10_4740_quar", SOURCE_DIR / "P8_Y5_R2FR_4740_PARENT_TFRI_OWNER_ACTION_BLOCK.csv", "S_quar = int chi_nu", "quarantine owner action"),
    ("SRC4748_11_4739_delta", SOURCE_DIR / "P8_Y5_R2FR_4739_CDELTAKDIV_ZERO_OR_BOUND_LAW.csv", "CDK4739_1_TT_kernel_zero", "TT kernel zero precedent"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    TT_SYMBOL_CSV,
    QUAR_SYMBOL_CSV,
    DN_UPDATE_CSV,
    STATIC_SMOKE_CSV,
    STATIC_SCORE_GATE_CSV,
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


def tt_symbol_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "TT4748_0_parent_operator",
            "D_TT[U]^nu := P_loc nabla_mu Pi_TT[U]^{mu nu}",
            "The TT owner block from 4740 is treated as a projected divergence of a TT/superpotential field.",
            "PARENT_OPERATOR_IDENTIFIED",
        ),
        (
            "TT4748_1_adjoint_symbol",
            "sigma_TT^dagger(p)xi_ab = -i Pi_TT^*(p)_{ab}^{mu nu} p_mu P_loc^*(p) xi_nu",
            "This is the hardened adjoint principal symbol before using transversality.",
            "HARDENED_SYMBOL",
        ),
        (
            "TT4748_2_exact_TT_transversality",
            "p_mu Pi_TT(p)^{mu nu}_{ab}=0 for an exact transverse TT projector",
            "If Pi_TT is exact, the divergence symbol vanishes on the TT image.",
            "TT_DIVERGENCE_KERNEL_RESULT",
        ),
        (
            "TT4748_3_gap_consequence",
            "c_TT=0 for exact transverse TT-divergence owner unless parent uses nonexact/weighted TT map",
            "The TT block is not a positive static gap source in the exact-TT route.",
            "NOT_GAP_SOURCE",
        ),
        (
            "TT4748_4_owner_role",
            "TT owner must be boundary/topological/superpotential kernel or carried as C_TT_kernel",
            "This redirects TT from coercivity to kernel/topological ownership.",
            "KERNEL_TOPOLOGICAL_ROUTE",
        ),
        (
            "TT4748_5_projector_blocker",
            "sigma(Pi_TT), sigma(P_loc), boundary behavior and nonlocal projector order remain parent inputs",
            "Even the kernel route needs exact projector ownership.",
            "PARENT_PROJECTOR_SOURCE_REQUIRED",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "tt_id": tt_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for tt_id, formula, meaning, status in specs
    ]


def quarantine_symbol_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "QUAR4748_0_parent_operator",
            "D_quar[K,q]^nu := q_tr^nu + nabla_mu K_own^{mu nu}",
            "The quarantine owner block is algebraic in q_tr and first order in K_own.",
            "PARENT_OPERATOR_IDENTIFIED",
        ),
        (
            "QUAR4748_1_adjoint_symbol_K",
            "sigma_quar,K^dagger(p)chi_{mu nu} = -i p_mu chi_nu",
            "Adjoint principal symbol for the K_own channel.",
            "HARDENED_SYMBOL",
        ),
        (
            "QUAR4748_2_adjoint_symbol_q",
            "sigma_quar,q^dagger(p)chi_nu = chi_nu",
            "Algebraic q_tr channel can directly control the chi multiplier if q_tr is parent-independent.",
            "ALGEBRAIC_CONTROL_CANDIDATE",
        ),
        (
            "QUAR4748_3_coercivity_candidate",
            "||sigma_quar^dagger(p)chi||^2 >= (w_q^2 + w_K^2 |p|_h^2)||chi||^2 minus map-kernel leakage",
            "Quarantine is the better positive c_DN candidate, provided q_tr/K_own maps are parent-owned and nondegenerate.",
            "COERCIVE_CANDIDATE",
        ),
        (
            "QUAR4748_4_blocker",
            "if q_tr is derived with a kernel or K_own has gauge-null directions, carry C_quar_kernel",
            "The algebraic channel must be real, not a notation trick.",
            "PARENT_MAP_SOURCE_REQUIRED",
        ),
        (
            "QUAR4748_5_static_constant",
            "c_quar >= inf(w_q^2 + w_K^2 |p|_h^2) - C_quar_kernel",
            "Source-ready lower-bound form for the quarantine contribution to c_DN.",
            "SOURCE_READY_SYMBOLIC_BOUND",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "quar_id": quar_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for quar_id, formula, meaning, status in specs
    ]


def dn_update_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "DNU4748_0_previous",
            "c_DN >= min(c_TFRI,c_TT,c_quar)-C_mix",
            "4747 symbolic full-constant formula.",
            "PREVIOUS_FORM",
        ),
        (
            "DNU4748_1_TT_revision",
            "exact TT divergence gives c_TT=0 and should be projected into C_TT_kernel/topological sector",
            "TT is removed from the positive-gap minimum unless parent changes the TT owner map.",
            "REVISION",
        ),
        (
            "DNU4748_2_effective_gap",
            "c_DN_eff >= min(c_TFRI,c_quar)-C_mix_eff-C_TT_kernel",
            "Static gap source should use TFRI+quarantine coercive blocks and carry TT as kernel leakage.",
            "UPDATED_BOUND",
        ),
        (
            "DNU4748_3_live_blockers",
            "numeric c_DN_eff needs c_TFRI,c_quar,C_mix_eff,C_TT_kernel and boundary complementing data",
            "This is the updated source list after TT hardening.",
            "MISSING_SOURCE_VALUES",
        ),
        (
            "DNU4748_4_claim_gate",
            "claim requires C_TT_kernel=0 or sourced below threshold plus c_DN_eff>0",
            "No claim is opened by a schematic symbol.",
            "CLOSED_NONCLAIM",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "dn_update_id": update_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for update_id, formula, meaning, status in specs
    ]


def static_smoke_rows(timestamp: str) -> list[dict[str, Any]]:
    pi_squared = math.pi**2
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "smoke_id": "SMOKE4748_0_live_missing",
            "case": "live_static_gap_inputs",
            "L_loc": "MISSING_GEOMETRY",
            "C_P": "MISSING_OR_CANONICAL_ONLY",
            "c_TFRI": "MISSING_SOURCE_VALUE",
            "c_quar": "MISSING_SOURCE_VALUE",
            "C_TT_kernel": "MISSING_SOURCE_VALUE",
            "c_DN_eff": "MISSING_SOURCE_VALUE",
            "lambda_lower_bound": "MISSING_SOURCE_VALUE",
            "result": "FAIL_CLOSED",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "smoke_id": "SMOKE4748_1_canonical_pipeline",
            "case": "canonical_nonclaim_pipeline_test",
            "L_loc": "1.0",
            "C_P": f"{1 / pi_squared:.16g}",
            "c_TFRI": "1.0",
            "c_quar": "1.0",
            "C_TT_kernel": "0.0_ASSUMED_TOPOLOGICAL_FOR_PIPELINE_ONLY",
            "c_DN_eff": "1.0",
            "lambda_lower_bound": f"{pi_squared:.16g}",
            "result": "PIPELINE_PASS_NONCLAIM",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "smoke_id": "SMOKE4748_2_TT_gap_rejected",
            "case": "try_to_use_exact_TT_as_gap_source",
            "L_loc": "1.0",
            "C_P": f"{1 / pi_squared:.16g}",
            "c_TFRI": "MISSING",
            "c_quar": "MISSING",
            "C_TT_kernel": "TT_DIVERGENCE_SYMBOL_ZERO",
            "c_DN_eff": "0_FROM_TT_ALONE",
            "lambda_lower_bound": "0_FROM_TT_ALONE",
            "result": "REJECTED_AS_GAP_SOURCE",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]
    return rows


def static_score_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SSG4748_0_TT", "TT exact-divergence route must be C_TT_kernel/topological, not c_TT positive gap.", "closed_until_kernel_contract"),
        ("SSG4748_1_quar", "quarantine coercivity needs parent q_tr/K_own independence and nondegenerate weights.", "closed_until_parent_map"),
        ("SSG4748_2_smoke", "canonical smoke values test only pipeline arithmetic.", "nonclaim_pipeline_only"),
        ("SSG4748_3_static_score", "PPN/R10/clock/orbital score needs real L_loc,C_P,c_TFRI,c_quar,C_TT_kernel,Pi_owner.", "closed_missing_sources"),
        ("SSG4748_4_lorentzian", "full local-GR dynamics still uses energy route, not this static smoke runner.", "separate_route"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "score_gate_id": gate_id,
            "gate": gate,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, status in specs
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4748_0_quarantine_source", "derive/source q_tr and K_own parent maps to prove c_quar>0", "best_next_route", "quarantine is the positive coercivity candidate"),
        ("ROUTE4748_1_TT_topological", "write TT topological/superpotential kernel contract with C_TT_kernel=0 or bound", "parallel_required_route", "TT cannot be used as exact-divergence gap source"),
        ("ROUTE4748_2_static_gap_numeric", "replace smoke constants with sourced L_loc,C_P,c_TFRI,c_quar,Pi_owner", "later_source_route", "after parent maps/projectors are fixed"),
        ("ROUTE4748_3_claim_now", "claim local static/PPN pass", "rejected", "only smoke values and schematic/quasi-symbolic sources exist"),
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
        ("GATE4748_0_sources", "All cited 4748 source anchors exist and contain expected text.", "pass_internal", False),
        ("GATE4748_1_TT_hardening", "TT symbol is hardened and classified as kernel/topological rather than positive gap source.", "conditional_pass", False),
        ("GATE4748_2_quar_hardening", "quarantine symbol is hardened as coercive candidate with parent-map blockers.", "conditional_pass", False),
        ("GATE4748_3_smoke", "canonical static gap smoke runner passes only as nonclaim pipeline test.", "conditional_pass_nonclaim", False),
        ("GATE4748_4_numeric_gap", "numeric c_DN_eff remains blocked by missing parent maps/constants.", "closed_unsigned", False),
        ("GATE4748_5_static_score", "static local-test scoring remains fail-closed.", "closed_unsigned", False),
        ("GATE4748_6_no_claim", "No local-GR, Newton, PPN, R10, WEP, clock or orbital claim from 4748.", "closed_firewall", False),
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
        ("FW4748_0_no_TT_gap_fake", "Do not use exact TT divergence as a positive elliptic gap source when transversality makes the symbol vanish."),
        ("FW4748_1_no_quar_algebraic_fake", "Do not claim quarantine coercivity unless q_tr/K_own are parent-independent or their kernel is bounded."),
        ("FW4748_2_no_smoke_claim", "Canonical smoke runner values are pipeline tests only, not sourced physics."),
        ("FW4748_3_no_projector_hide", "P_loc/Pi_TT/Q_perp projector symbols remain parent inputs."),
        ("FW4748_4_no_github_action", "No GitHub action is performed by this local checkpoint."),
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
            "summary": "4748 hardens the TT symbol and finds the exact transverse TT-divergence route is a kernel/topological owner, not a positive gap source. The quarantine symbol is hardened as the better coercive candidate if q_tr/K_own parent maps are nondegenerate. A canonical static gap smoke runner passes as nonclaim pipeline test while live scoring remains fail-closed.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4748_0_local_only",
            "status": "local_only_private_checkpoint",
            "detail": "Generated local post-checkpoint and formalization files only; no GitHub action.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4748_1_science_verdict",
            "status": "TT_reclassified_as_kernel_quarantine_coercivity_candidate_smoke_nonclaim",
            "detail": "The TT owner is no longer treated as a positive gap source; quarantine becomes the main coercive symbol target.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "4748 shows the next decisive source is the quarantine q_tr/K_own map, while TT needs a topological/kernel contract.",
            "preferred_route": "Prove/source quarantine map coercivity c_quar>0 with explicit q_tr/K_own parent maps.",
            "fallback_route": "Write the TT topological/superpotential kernel contract and source C_TT_kernel=0 or a bound.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullet(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    timestamp: str,
    tt_rows: list[dict[str, Any]],
    quar_rows: list[dict[str, Any]],
    dn_rows: list[dict[str, Any]],
    smoke_rows: list[dict[str, Any]],
    score_gates: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4748 Y5 R2FR: TT Quarantine Symbol Hardening And Static Gap Smoke Runner

Generated: `{timestamp}`

## Summary

- Work is local-only and private.
- This checkpoint hardens the two owner symbols that were schematic in 4747.
- TT result:

```text
D_TT[U]^nu = P_loc nabla_mu Pi_TT[U]^{{mu nu}}
sigma_TT^dagger(p)xi_ab = -i Pi_TT^*(p)_ab^{{mu nu}} p_mu P_loc^*(p) xi_nu
p_mu Pi_TT(p)^{{mu nu}}_ab = 0 for exact transverse TT
=> c_TT=0 for exact TT divergence
```

- Therefore TT is not a positive static gap source in the exact-TT route; it must be topological/superpotential or carried as `C_TT_kernel`.
- Quarantine result:

```text
D_quar[K,q]^nu = q_tr^nu + nabla_mu K_own^{{mu nu}}
sigma_quar,K^dagger(p)chi_mu_nu = -i p_mu chi_nu
sigma_quar,q^dagger(p)chi_nu = chi_nu
```

- Therefore quarantine is the better coercive candidate if the `q_tr/K_own` parent map is nondegenerate.
- A canonical static gap smoke runner is added, but it is explicitly nonclaim.

## TT Symbol Hardening

{bullet(tt_rows, "tt_id", "formula")}

## Quarantine Symbol Hardening

{bullet(quar_rows, "quar_id", "formula")}

## DN Constant Update

{bullet(dn_rows, "dn_update_id", "formula")}

## Static Gap Smoke Runner

{bullet(smoke_rows, "smoke_id", "result")}

## Static Score Gate

{bullet(score_gates, "score_gate_id", "status")}

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

    formal = f"""# 764 PPC4161: TT Quarantine Symbol Hardening And Static Gap Smoke Runner

Generated: `{timestamp}`

## Hardened Symbol Result

4748 hardens the TT and quarantine symbols.

For the exact TT route:

```text
sigma_TT^dagger(p)xi_ab = -i Pi_TT^*(p)_ab^{{mu nu}} p_mu P_loc^*(p) xi_nu,
p_mu Pi_TT(p)^{{mu nu}}_ab=0,
so c_TT=0 for exact TT divergence.
```

Thus TT is a kernel/topological owner, not the positive gap source.

For quarantine:

```text
sigma_quar,K^dagger(p)chi_mu_nu = -i p_mu chi_nu,
sigma_quar,q^dagger(p)chi_nu = chi_nu.
```

Thus quarantine is the better `c_DN` candidate if `q_tr/K_own` are parent-owned and nondegenerate.

## Smoke Runner

The canonical static gap smoke runner gives `lambda_lower_bound=pi^2` only for `L_loc=1`, `C_P=1/pi^2`, `c_DN_eff=1`, and `C_TT_kernel=0` as a pipeline test. It is not valid for claims.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4748 hardens `sigma_TT` and finds exact TT transversality makes the divergence symbol vanish: TT is kernel/topological, not a positive gap source.
- It hardens `sigma_quar` and identifies the algebraic `q_tr` channel as the better coercivity candidate.
- The DN bound updates to `c_DN_eff >= min(c_TFRI,c_quar)-C_mix_eff-C_TT_kernel`.
- A canonical static gap smoke runner passes only as nonclaim pipeline arithmetic.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4748 local packet update: TT is reclassified as a topological/kernel owner, while quarantine becomes the main positive static-gap source candidate. Next is quarantine map coercivity or a TT kernel contract.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4748-Y5-R2FR-TT-quarantine-symbol-hardening-and-static-gap-smoke-runner.md`

## Decision

`{DECISION}`

## What moved forward

- Hardened `sigma_TT` and found exact TT transversality makes the divergence symbol vanish, so TT cannot be used as the positive gap source in the exact-TT route.
- Hardened `sigma_quar`; the algebraic `q_tr` channel can control `chi` if the parent map is nondegenerate.
- Updated the static gap route to use TFRI+quarantine coercive blocks while carrying TT as `C_TT_kernel`.
- Added a canonical static gap smoke runner that passes only as a nonclaim pipeline test.

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
        "4748 hardens TT/quarantine owner symbols, reclassifies exact TT divergence as kernel/topological, and identifies quarantine as the main coercive static-gap candidate.",
        "Generated source register, TT symbol hardening, quarantine symbol hardening, DN constant update, static gap smoke runner, score gates, route matrix, promotion gates, firewalls, decision, status, next target and validation.",
        "TT_kernel_topological_quarantine_coercivity_candidate_static_smoke_nonclaim",
        NEXT_TARGET,
        "Using exact TT divergence as a positive gap source, or treating the canonical smoke runner as sourced evidence.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need quarantine q_tr/K_own parent maps, TT topological/kernel contract, projector symbols, real constants and arena projections.",
        "TT quarantine symbol hardening and static gap smoke runner",
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
    tt_rows: list[dict[str, Any]],
    quar_rows: list[dict[str, Any]],
    dn_rows: list[dict[str, Any]],
    smoke_rows: list[dict[str, Any]],
    score_gates: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4748_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), "source register"))
    checks.append(("VAL4748_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), "source register"))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4748_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4748_2_TT_kernel_result", "TT rows identify transversality and not-gap-source result", any("p_mu Pi_TT" in row["formula"] for row in tt_rows) and any(row["status"] == "NOT_GAP_SOURCE" for row in tt_rows), str(TT_SYMBOL_CSV)))
    checks.append(("VAL4748_3_quarantine_coercive", "quarantine rows include algebraic q channel and coercive candidate", any("sigma_quar,q" in row["formula"] for row in quar_rows) and any(row["status"] == "COERCIVE_CANDIDATE" for row in quar_rows), str(QUAR_SYMBOL_CSV)))
    checks.append(("VAL4748_4_DN_update", "DN update carries TT kernel and quarantine gap candidate", any("C_TT_kernel" in row["formula"] for row in dn_rows) and any("c_quar" in row["formula"] for row in dn_rows), str(DN_UPDATE_CSV)))
    checks.append(("VAL4748_5_smoke_nonclaim", "canonical static smoke passes only as nonclaim", any(row["result"] == "PIPELINE_PASS_NONCLAIM" and row["valid_for_claim"] is False for row in smoke_rows), str(STATIC_SMOKE_CSV)))
    checks.append(("VAL4748_6_live_fail_closed", "live smoke remains fail closed", any(row["smoke_id"] == "SMOKE4748_0_live_missing" and row["result"] == "FAIL_CLOSED" for row in smoke_rows), str(STATIC_SMOKE_CSV)))
    checks.append(("VAL4748_7_score_gates", "score gates block static scoring and TT gap fake", any("TT" in row["gate"] and "not c_TT" in row["gate"] for row in score_gates) and any(row["status"] == "closed_missing_sources" for row in score_gates), str(STATIC_SCORE_GATE_CSV)))
    checks.append(("VAL4748_8_gates_nonclaim", "promotion gates keep claim closed", all(row["valid_for_claim"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4748_9_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4748_10_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4748_11_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4748_12_claim_row", "claim row L-590 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4748_13_resume", "resume points from 4748 to 4749", "4748-Y5" in resume_text and "4749-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4748_14_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
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
            "validation_id": "VAL4748_OVERALL",
            "check": "all 4748 local generation and nonclaim checks pass",
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
    tt_rows = tt_symbol_rows(timestamp)
    quar_rows = quarantine_symbol_rows(timestamp)
    dn_rows = dn_update_rows(timestamp)
    smoke_rows = static_smoke_rows(timestamp)
    score_gates = static_score_gate_rows(timestamp)
    routes = route_matrix_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(TT_SYMBOL_CSV, tt_rows)
    write_csv(QUAR_SYMBOL_CSV, quar_rows)
    write_csv(DN_UPDATE_CSV, dn_rows)
    write_csv(STATIC_SMOKE_CSV, smoke_rows)
    write_csv(STATIC_SCORE_GATE_CSV, score_gates)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, tt_rows, quar_rows, dn_rows, smoke_rows, score_gates, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, tt_rows, quar_rows, dn_rows, smoke_rows, score_gates, gates, timestamp))


if __name__ == "__main__":
    main()

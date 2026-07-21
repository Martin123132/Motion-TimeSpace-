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

CHECKPOINT = "4735"
CLAIM_ID = "L-577"
MARKER = "PPC4161_LCG_QBASIC_OWNER_OR_VLCG_SOURCE_ROW_4735"
PACKET_MARKER = "PPC4161_PACKET_LCG_QBASIC_OWNER_OR_VLCG_SOURCE_ROW_4735"
DECISION = "LCG_QBASIC_OWNER_EXACT_CONDITIONAL_UNSIGNED_VLCG_SOURCE_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4736-Y5-R2FR-GK-parent-owner-or-transition-shell-VLcg-bound.md"

DOC_PATH = POST / "4735-Y5-R2FR-Lcg-qbasic-owner-or-VLcg-source-row.md"
FORMAL_PATH = FORMAL / "751-PPC4161-Lcg-qbasic-owner-or-VLcg-source-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4735_SOURCE_REGISTER.csv"
LCG_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4735_LCG_QBASIC_OWNER_THEOREM.csv"
VLCG_BUDGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4735_VLCG_DERIVATIVE_BUDGET.csv"
GK_SUBBUDGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4735_GK_SOURCE_SUBBUDGET.csv"
PROPAGATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4735_PROPAGATION_TO_VXB_JM.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4735_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4735_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4735_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4735_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4735_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4735_VALIDATION.csv"

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    LCG_THEOREM_CSV,
    VLCG_BUDGET_CSV,
    GK_SUBBUDGET_CSV,
    PROPAGATION_CSV,
    GATES_CSV,
    FIREWALL_CSV,
    DECISION_CSV,
    STATUS_CSV,
    NEXT_TARGET_CSV,
]

SOURCE_SPECS = [
    ("SRC4735_0_4734_next", SOURCE_DIR / "P8_Y5_R2FR_4734_NEXT_TARGET.csv", "V_XB budget shows L_cg", "4734 selected L_cg as the next blocker"),
    ("SRC4735_1_4734_vxb", SOURCE_DIR / "P8_Y5_R2FR_4734_VXB_COMPONENT_BUDGET.csv", "VXB4734_6_Lcg", "4734 V_XB budget contains V_Lcg"),
    ("SRC4735_2_Lcg_87_status", FORMAL / "87-Lcg-coarse-graining-rule.md", "L_cg_coherence_rule_candidate_not_derived", "L_cg coherence rule not parent-derived"),
    ("SRC4735_3_Lcg_87_rule", FORMAL / "87-Lcg-coarse-graining-rule.md", "alpha_K G_K^2", "selected L_cg rule shape"),
    ("SRC4735_4_Lcg_88_warning", FORMAL / "88-Lcg-rule-gate.md", "open_Lcg_gradient_trace_warning", "L_cg gradient trace warning"),
    ("SRC4735_5_Lcg_88_parent", FORMAL / "88-Lcg-rule-gate.md", "parent theorem not derived", "parent theorem still open"),
    ("SRC4735_6_Lcg_89_GK", FORMAL / "89-source-model-curvature-Lcg-test.md", "G_K = |d ln K_B / dr|", "coherence-gradient definition"),
    ("SRC4735_7_Lcg_89_trace", FORMAL / "89-source-model-curvature-Lcg-test.md", "trace_gradient_proxy", "trace-gradient proxy"),
    ("SRC4735_8_Lcg_90_computable", FORMAL / "90-Lcg-gradient-trace-bound.md", "source-model L_cg is computable", "source-model L_cg computability"),
    ("SRC4735_9_Lcg_90_closure", FORMAL / "90-Lcg-gradient-trace-bound.md", "U_B^2 trace suppression survives locally as closure", "trace suppression closure row"),
    ("SRC4735_10_Lcg_91_viable", FORMAL / "91-trace-suppression-closure-gate.md", "U_B^2 is a viable closure candidate", "U_B trace closure viability"),
    ("SRC4735_11_Lcg_91_not_derived", FORMAL / "91-trace-suppression-closure-gate.md", "the U_B^2 law has not been derived", "trace closure not derived"),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path, existing + separator + block.rstrip() + "\n")


def source_path(source_id: str) -> str:
    for row_id, path, _needle, _role in SOURCE_SPECS:
        if row_id == source_id:
            return str(path)
    raise KeyError(source_id)


def source_register(ts: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": ts,
            }
        )
    return rows


def lcg_theorem_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "LCG4735_0_exact_derivative_identity",
            "For L_cg=S^-1/2 with S=L_H^-2+alpha_K G_K^2, D_v ln L_cg = -0.5 D_v ln S.",
            "exact algebraic identity",
            "closed_symbolically",
            "SRC4735_3_Lcg_87_rule",
            True,
        ),
        (
            "LCG4735_1_qbasic_sufficient_condition",
            "If D_v L_H=D_v alpha_K=D_v G_K=0, then D_v L_cg=0.",
            "sufficient q-basic theorem",
            "exact_conditional_only",
            "SRC4735_3_Lcg_87_rule",
            True,
        ),
        (
            "LCG4735_2_missing_parent_owner",
            "Actual parent ownership of K_B, G_K, alpha_K, support/projector and local readout is not signed in the present corpus.",
            "promotion blocker",
            "unsigned",
            "SRC4735_2_Lcg_87_status",
            False,
        ),
        (
            "LCG4735_3_no_constant_Lcg_escape",
            "A constant L_cg would hide the issue but prior gates treat constant L_cg as toy-only, not a final claim.",
            "anti-cheat guard",
            "blocked_as_final_claim",
            "SRC4735_4_Lcg_88_warning",
            False,
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": theorem_id,
            "statement": statement,
            "role": role,
            "status": status,
            "source_id": source_id,
            "source_path": source_path(source_id),
            "valid_for_claim": valid_for_claim,
            "timestamp_utc": ts,
        }
        for theorem_id, statement, role, status, source_id, valid_for_claim in specs
    ]


def vlcg_budget_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "VLCG4735_0_definition",
            "V_Lcg := sup_local |D_v ln L_cg|",
            "dimensionless amplitude under local vertical variation",
            "1",
            "source row definition",
            "SRC4735_1_4734_vxb",
            False,
        ),
        (
            "VLCG4735_1_exact_weight_decomposition",
            "V_Lcg <= Omega_H V_LH + Omega_K V_GK + 0.5 Omega_K V_alphaK",
            "Omega_H=L_H^-2/S, Omega_K=alpha_K G_K^2/S, S=L_H^-2+alpha_K G_K^2",
            "1",
            "derived bound from exact derivative identity",
            "SRC4735_3_Lcg_87_rule",
            True,
        ),
        (
            "VLCG4735_2_Hubble_cap_branch",
            "V_LH := sup_local |D_v ln L_H|",
            "zero only if the Hubble cap is fixed background/q-basic on the local branch",
            "1",
            "needs parent background/descent signature",
            "SRC4735_3_Lcg_87_rule",
            False,
        ),
        (
            "VLCG4735_3_alpha_branch",
            "V_alphaK := sup_local |D_v ln alpha_K|",
            "zero only if alpha_K is a universal parent coefficient rather than a fitted readout",
            "1",
            "needs parent coefficient source",
            "SRC4735_2_Lcg_87_status",
            False,
        ),
        (
            "VLCG4735_4_coherence_gradient_branch",
            "V_GK := sup_local |D_v ln G_K|",
            "dominant local uncertainty because G_K is built from projected gradients of K_B",
            "1",
            "needs G_K owner/subbudget",
            "SRC4735_6_Lcg_89_GK",
            False,
        ),
        (
            "VLCG4735_5_trace_proxy_bridge",
            "trace_gradient_proxy = 2 L_cg |d ln L_cg/dr| is a coordinate/source-model proxy, not the parent vertical bound",
            "turns old trace warning into a source-model diagnostic rather than a proof",
            "1",
            "useful but nonclaim",
            "SRC4735_7_Lcg_89_trace",
            False,
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "budget_id": budget_id,
            "expression": expression,
            "definition": definition,
            "units": units,
            "status": status,
            "source_id": source_id,
            "source_path": source_path(source_id),
            "valid_for_claim": valid_for_claim,
            "timestamp_utc": ts,
        }
        for budget_id, expression, definition, units, status, source_id, valid_for_claim in specs
    ]


def gk_subbudget_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "GK4735_0_definition",
            "G_K = |d ln K_B / dr| in the source-model file; covariant parent form should be ||P_perp nabla ln K_B||.",
            "definition translation",
            "qbasic_if_projector_and_KB_are_qbasic",
            "SRC4735_6_Lcg_89_GK",
        ),
        (
            "GK4735_1_KB_owner",
            "D_v K_B requires ownership of curvature/source scalars, source weights, H_bg floor and local matter readout.",
            "K_B parent ownership",
            "unsigned",
            "SRC4735_6_Lcg_89_GK",
        ),
        (
            "GK4735_2_gradient_commutator",
            "D_v ||P_perp nabla ln K_B|| can receive projector, connection, support and boundary terms even if K_B is scalar-built.",
            "gradient/readout ownership",
            "unsigned",
            "SRC4735_7_Lcg_89_trace",
        ),
        (
            "GK4735_3_subbudget",
            "V_GK <= V_KB_grad + V_projector + V_connection + V_support + V_boundary",
            "fallback bound",
            "source_row_staged",
            "SRC4735_7_Lcg_89_trace",
        ),
        (
            "GK4735_4_transition_warning",
            "Transition shells remain dangerous because U_B is order one there and trace suppression does not automatically kill the shell.",
            "transition branch warning",
            "next_target",
            "SRC4735_10_Lcg_91_viable",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "subbudget_id": subbudget_id,
            "statement": statement,
            "role": role,
            "status": status,
            "source_id": source_id,
            "source_path": source_path(source_id),
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for subbudget_id, statement, role, status, source_id in specs
    ]


def propagation_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        (
            "PROP4735_0_to_VXB",
            "V_XB <= V_XB_without_Lcg + V_Lcg + V_transition + V_readout",
            "propagates L_cg leakage into the X_B vertical budget",
            "SRC4735_1_4734_vxb",
        ),
        (
            "PROP4735_1_to_Jm_hidden",
            "|J_m_XB| <= L_R826_XB (V_XB_without_Lcg + V_Lcg + V_transition + V_readout)",
            "propagates L_cg leakage into the R826 hidden-source row",
            "SRC4735_1_4734_vxb",
        ),
        (
            "PROP4735_2_to_B826",
            "|B_826| inherits the L_R826_XB V_Lcg term until parent q-basic ownership or a numeric local bound closes it.",
            "keeps local-GR bridge nonclaim",
            "SRC4735_0_4734_next",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "propagation_id": propagation_id,
            "expression": expression,
            "meaning": meaning,
            "source_id": source_id,
            "source_path": source_path(source_id),
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for propagation_id, expression, meaning, source_id in specs
    ]


def gate_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4735_0_exact_identity", "Exact derivative identity for L_cg written.", "pass_structural_nonclaim", False),
        ("GATE4735_1_qbasic_owner", "Promote only if L_H, alpha_K and G_K are parent q-basic/fixed under local vertical variations.", "closed_unsigned", False),
        ("GATE4735_2_numeric_bound", "Promote only if V_Lcg is populated by source-backed numeric local bounds.", "closed_no_numeric_bound", False),
        ("GATE4735_3_transition_shell", "Promote local branch only if transition-shell q-current/trace contribution is bounded or routed.", "closed_transition_open", False),
        ("GATE4735_4_no_constant_escape", "Do not replace the missing owner proof with constant L_cg as final claim.", "closed_firewall", False),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "valid_for_claim": valid_for_claim,
            "timestamp_utc": ts,
        }
        for gate_id, gate, status, valid_for_claim in specs
    ]


def firewall_rows(ts: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4735_0_no_local_gr_claim", "No local-GR, PPN, R10 or Newtonian-limit pass is claimed by 4735."),
        ("FW4735_1_no_parent_theorem_overclaim", "The exact q-basic theorem is conditional only; the actual parent owner is unsigned."),
        ("FW4735_2_no_constant_Lcg_patch", "Constant L_cg remains toy-only and cannot be used as a final local closure."),
        ("FW4735_3_no_GitHub_action", "No GitHub action is performed by this checkpoint."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "firewall": firewall,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for firewall_id, firewall in specs
    ]


def decision_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "summary": "L_cg q-basic descent is proven only as an exact conditional theorem; the active nonclaim result is the V_Lcg derivative budget and G_K subbudget.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4735_0_local_only",
            "status": "local_only_private_checkpoint",
            "detail": "Generated local post-checkpoint and formalization files only.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4735_1_science_verdict",
            "status": "derivation_progress_nonclaim",
            "detail": "L_cg leakage is now decomposed into Omega_H V_LH + Omega_K V_GK + 0.5 Omega_K V_alphaK; G_K/transition remain the next owners.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        },
    ]


def next_target_rows(ts: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "V_Lcg is now reduced to V_GK, V_LH and V_alphaK; G_K and transition support are the active local blockers.",
            "preferred_route": "Try to prove G_K is parent-owned/q-basic from K_B and the projector/connection descent rules.",
            "fallback_route": "If the proof fails, create a transition-shell V_Lcg/q-current bound row with explicit source terms.",
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
    ]


def bullets(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    ts: str,
    theorem: list[dict[str, Any]],
    vlcg: list[dict[str, Any]],
    gk: list[dict[str, Any]],
    propagation: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4735 Y5 R2FR: Lcg Q-Basic Owner Or VLcg Source Row

Generated: `{ts}`

## Summary

- Work is local-only and private.
- Target: decide whether `L_cg` can be treated as q-basic/fixed under the local vertical variation.
- Result: exact conditional theorem exists, but the actual parent-owner proof is still unsigned.
- Progress: the missing piece is now a sharp source row, not a blank gap:

```text
V_Lcg := sup_local |D_v ln L_cg|
V_Lcg <= Omega_H V_LH + Omega_K V_GK + 0.5 Omega_K V_alphaK
Omega_H = L_H^-2 / (L_H^-2 + alpha_K G_K^2)
Omega_K = alpha_K G_K^2 / (L_H^-2 + alpha_K G_K^2)
```

## Exact Derivation

Start from the selected candidate:

```text
L_cg = (L_H^-2 + alpha_K G_K^2)^(-1/2)
S = L_H^-2 + alpha_K G_K^2
```

Then:

```text
D_v ln L_cg = -1/2 D_v ln S
D_v S = -2 L_H^-2 D_v ln L_H
        + alpha_K G_K^2 D_v ln alpha_K
        + 2 alpha_K G_K^2 D_v ln G_K
```

So the conservative amplitude bound is:

```text
V_Lcg <= Omega_H V_LH + Omega_K V_GK + 0.5 Omega_K V_alphaK.
```

Therefore `V_Lcg=0` is allowed only if the Hubble cap, alpha coefficient and coherence-gradient owner are all q-basic/fixed.

## Theorem Rows

{bullets(theorem, "theorem_id", "statement")}

## VLcg Budget

{bullets(vlcg, "budget_id", "expression")}

## G_K Subbudget

{bullets(gk, "subbudget_id", "statement")}

## Propagation

{bullets(propagation, "propagation_id", "expression")}

## Promotion Gates

{bullets(gates, "gate_id", "gate")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`

No GitHub action was performed.
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 751 PPC4161: Lcg Q-Basic Owner Or VLcg Source Row

Generated: `{ts}`

## Current Status

`{DECISION}`

`L_cg` is not promoted as parent q-basic. The exact conditional theorem is useful:

```text
L_cg = (L_H^-2 + alpha_K G_K^2)^(-1/2)
D_v ln L_cg = -1/2 D_v ln(L_H^-2 + alpha_K G_K^2)
```

But the actual parent ownership of `L_H`, `alpha_K`, `G_K`, the projector/connection, and transition support is not signed.

## Nonclaim Bound

```text
V_Lcg <= Omega_H V_LH + Omega_K V_GK + 0.5 Omega_K V_alphaK
V_GK <= V_KB_grad + V_projector + V_connection + V_support + V_boundary
|J_m_XB| <= L_R826_XB (V_XB_without_Lcg + V_Lcg + V_transition + V_readout)
```

## Interpretation

This improves the local-GR bridge because the previous `L_cg` hole has been decomposed into named, sourceable pieces. It does not close the bridge.

## Next

`{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(ts: str) -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""

## {MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Result: `L_cg` q-basic descent is exact only under signed ownership of `L_H`, `alpha_K` and `G_K`.
- Nonclaim bound: `V_Lcg <= Omega_H V_LH + Omega_K V_GK + 0.5 Omega_K V_alphaK`.
- Next local route: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""

## {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet update: the local bridge now carries an explicit `V_Lcg` derivative budget rather than treating `L_cg` leakage as an unspecified gap.
- Claim status: nonclaim; no local-GR/PPN/R10 pass.
""",
    )
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Updated: `{ts}`

## Latest completed checkpoint

`4735-Y5-R2FR-Lcg-qbasic-owner-or-VLcg-source-row.md`

## Decision

`{DECISION}`

## What moved forward

- `L_cg` descent now has an exact derivative identity.
- `V_Lcg` is now a sourceable amplitude row, not a vague missing term.
- The active owner has been narrowed to `G_K`, `L_H`, `alpha_K`, and transition/support readout.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
""",
    )


def add_claim_once(ts: str) -> None:
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_bridge",
        "claim": "4735 derives the exact L_cg vertical derivative identity and stages V_Lcg as a sourceable local leakage budget; parent q-basic ownership remains unsigned.",
        "current_evidence": "Generated source register, Lcg q-basic theorem rows, V_Lcg derivative budget, G_K subbudget, propagation rows, gates, firewalls, decision, status, next target and validation.",
        "status": "VLcg_source_row_staged_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating the conditional q-basic theorem or U_B^2 trace closure as a derived local-GR pass.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "G_K parent owner, transition-shell q-current, support/readout tails and numeric V_Lcg bounds remain unsourced.",
        "title": "Lcg q-basic owner or VLcg source row",
        "notes": f"{MARKER}; {DECISION}; generated {ts}",
    }
    for field in fieldnames:
        row.setdefault(field, "")
    rows.append(row)
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def parse_csv(path: Path) -> bool:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    vlcg: list[dict[str, Any]],
    gk: list[dict[str, Any]],
    propagation: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    ts: str,
) -> list[dict[str, Any]]:
    generated_with_validation = GENERATED_CSVS + [VALIDATION_CSV]
    checks = [
        ("VAL4735_0_sources_exist", all(row["exists"] for row in sources), "all cited 4735 source paths exist"),
        ("VAL4735_1_needles_found", all(row["needle_found"] for row in sources), "all cited 4735 source needles found"),
        ("VAL4735_2_exact_lcg_theorem_written", any(row["theorem_id"] == "LCG4735_1_qbasic_sufficient_condition" for row in theorem), "exact conditional q-basic theorem row is written"),
        ("VAL4735_3_VLcg_budget_written", any("Omega_H V_LH" in row["expression"] for row in vlcg), "V_Lcg derivative budget is written"),
        ("VAL4735_4_GK_subbudget_written", any("V_GK <=" in row["statement"] for row in gk), "G_K source subbudget is written"),
        ("VAL4735_5_propagation_written", any("L_R826_XB" in row["expression"] for row in propagation), "V_Lcg propagates to V_XB/J_m_hidden"),
        ("VAL4735_6_parent_qbasic_not_promoted", all(row["valid_for_claim"] is False for row in gates), "parent q-basic proof remains nonclaim"),
        ("VAL4735_7_docs_written", DOC_PATH.exists() and FORMAL_PATH.exists(), "checkpoint and formal documents written"),
        ("VAL4735_8_spine_packet_markers", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), "spine and packet markers inserted"),
        ("VAL4735_9_claim_row_added", CLAIM_ID in read_text(CLAIMS_PATH), "claims register contains L-577"),
        ("VAL4735_10_resume_updated", NEXT_TARGET in read_text(RESUME_PATH), "resume points to 4736 next target"),
        ("VAL4735_11_csv_parse", all(parse_csv(path) for path in generated_with_validation if path.exists()), "all generated 4735 CSV files parse cleanly"),
        ("VAL4735_12_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
    ]
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": ts,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4735_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "4735 Lcg q-basic owner or V_Lcg source row validation",
            "timestamp_utc": ts,
        }
    )
    return rows


def main() -> None:
    ts = now()
    sources = source_register(ts)
    theorem = lcg_theorem_rows(ts)
    vlcg = vlcg_budget_rows(ts)
    gk = gk_subbudget_rows(ts)
    propagation = propagation_rows(ts)
    gates = gate_rows(ts)
    firewalls = firewall_rows(ts)
    decisions = decision_rows(ts)
    statuses = status_rows(ts)
    next_targets = next_target_rows(ts)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(LCG_THEOREM_CSV, theorem)
    write_csv(VLCG_BUDGET_CSV, vlcg)
    write_csv(GK_SUBBUDGET_CSV, gk)
    write_csv(PROPAGATION_CSV, propagation)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(ts, theorem, vlcg, gk, propagation, gates)
    update_spine_packet_resume(ts)
    add_claim_once(ts)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, theorem, vlcg, gk, propagation, gates, ts))


if __name__ == "__main__":
    main()

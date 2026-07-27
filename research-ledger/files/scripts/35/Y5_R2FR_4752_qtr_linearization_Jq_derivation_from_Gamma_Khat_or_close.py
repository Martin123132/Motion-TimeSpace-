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

CHECKPOINT = "4752"
CLAIM_ID = "L-594"
MARKER = "PPC4161_QTR_LINEARIZATION_JQ_DERIVATION_FROM_GAMMA_KHAT_OR_CLOSE_4752"
PACKET_MARKER = "PPC4161_PACKET_QTR_LINEARIZATION_JQ_DERIVATION_FROM_GAMMA_KHAT_OR_CLOSE_4752"
DECISION = "QTR_LINEARIZATION_GIVES_DERIVATIVE_SYMBOL_NO_ALGEBRAIC_JQ_ZERO_MODE_OWNER_REQUIRED_NONCLAIM"
NEXT_TARGET = "4753-Y5-R2FR-zero-mode-owner-or-derivative-gap-bound.md"

DOC_PATH = POST / "4752-Y5-R2FR-qtr-linearization-Jq-derivation-from-Gamma-Khat-or-close.md"
FORMAL_PATH = FORMAL / "768-PPC4161-qtr-linearization-Jq-derivation-from-Gamma-Khat-or-close.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4752_SOURCE_REGISTER.csv"
LINEARIZATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4752_QTR_LINEARIZATION_DERIVATION.csv"
ZERO_MODE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4752_SYMBOL_AND_ZERO_MODE_AUDIT.csv"
JQ_VERDICT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4752_ALGEBRAIC_JQ_VERDICT.csv"
DERIV_GAP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4752_DERIVATIVE_GAP_BOUND.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4752_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4752_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4752_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4752_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4752_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4752_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4752_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4752_0_4751_next", SOURCE_DIR / "P8_Y5_R2FR_4751_NEXT_TARGET.csv", "D q_tr[X]", "4751 linearization handoff"),
    ("SRC4752_1_4751_verdict", SOURCE_DIR / "P8_Y5_R2FR_4751_PARENT_MAP_SOURCE_VERDICT.csv", "PMV4751_1_Jq_map", "4751 no parent Jq verdict"),
    ("SRC4752_2_4751_hits", SOURCE_DIR / "P8_Y5_R2FR_4751_QTR_CORPUS_HIT_LEDGER.csv", "FORMULA_DEFINITION_CAN_LINEARIZE", "4751 formula target hit"),
    ("SRC4752_3_claims_qtr", FORMAL / "02-claims-register.csv", "q_tr = grad Gamma_eff - div K_hat", "older exact variation target"),
    ("SRC4752_4_claims_khat", FORMAL / "02-claims-register.csv", "K_hat=K_Gamma+Delta_K", "older Khat right-inverse route"),
    ("SRC4752_5_4573_lift", SOURCE_DIR / "P8_Y5_R2FR_4573_SOURCE_LIFT_ZERO_CONTRACT.csv", "Sigma_metric[q_tr] :=", "source lift definition"),
    ("SRC4752_6_4749_rank", SOURCE_DIR / "P8_Y5_R2FR_4749_QUARANTINE_RANK_COHERCIVITY_TEST.csv", "QRT4749_3_combined_constant", "prior algebraic rank gap"),
    ("SRC4752_7_4750_schema", SOURCE_DIR / "P8_Y5_R2FR_4750_QTR_PARENT_RANK_SOURCE_SCHEMA.csv", "QTRSCHEMA4750_0_Jq", "4750 Jq source schema"),
    ("SRC4752_8_4751_validation", SOURCE_DIR / "P8_Y5_BRR545_4751_VALIDATION.csv", "VAL4751_OVERALL", "4751 validated source hunt"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    LINEARIZATION_CSV,
    ZERO_MODE_CSV,
    JQ_VERDICT_CSV,
    DERIV_GAP_CSV,
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


def linearization_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "QLIN4752_0_definition",
            "q_tr^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "Starting point selected by 4751 source hunt.",
            "DEFINITION_TARGET",
        ),
        (
            "QLIN4752_1_scalar_leg",
            "delta(nabla^nu Gamma_eff)=nabla^nu(delta Gamma_eff)+h^{nu rho} partial_rho Gamma_eff + lower-order connection/projection terms",
            "For scalar Gamma_eff the principal variation is a gradient of delta Gamma_eff; background-gradient terms are lower order and sign-unsigned.",
            "DERIVED_LINEARIZATION",
        ),
        (
            "QLIN4752_2_K_leg",
            "delta(nabla_mu K_hat^{mu nu})=nabla_mu(delta K_hat^{mu nu})+delta Gamma^mu_{mu lambda}K_hat^{lambda nu}+delta Gamma^nu_{mu lambda}K_hat^{mu lambda}",
            "The K leg is principally a divergence of delta K_hat plus connection-weighted lower-order terms.",
            "DERIVED_LINEARIZATION",
        ),
        (
            "QLIN4752_3_full_linearization",
            "Dq_tr[X]^nu=P_loc[nabla^nu D_Gamma[X]-nabla_mu D_K[X]^{mu nu}+L_conn[X]+L_bg[X]]+(DP_loc[X])q_raw^nu+B_boundary[X]^nu",
            "All possible non-principal leakage is made explicit rather than hidden inside J_q.",
            "DERIVED_OPERATOR_SPLIT",
        ),
        (
            "QLIN4752_4_principal_symbol",
            "sigma(Dq_tr)(p)[X]^nu = i p^nu D_Gamma[X] - i p_mu D_K[X]^{mu nu}",
            "The leading symbol is derivative-controlled and vanishes at p=0.",
            "DERIVED_SYMBOL",
        ),
        (
            "QLIN4752_5_algebraic_channel",
            "J_q^alg=0 for the bare Gamma_eff/K_hat formula unless a separate parent algebraic source block A_X is supplied",
            "The 4749 algebraic full-rank shortcut is not produced by this formula alone.",
            "NEGATIVE_DERIVATION_RESULT",
        ),
        (
            "QLIN4752_6_derivative_route",
            "c_quar^deriv >= p_min^2 c_GK - C_lower - C_boundary - C_zero",
            "A derivative elliptic route can survive only with p_min>0, a positive Gamma/K symbol constant, and zero-mode/boundary ownership.",
            "SURVIVING_ROUTE",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "derivation_id": derivation_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for derivation_id, formula, meaning, status in specs
    ]


def zero_mode_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ZM4752_0_p_zero", "p=0", "sigma(Dq_tr)(0)=0", "Algebraic full-rank control is absent for the formula-only route.", "BLOCKS_ALGEBRAIC_JQ_CLAIM"),
        ("ZM4752_1_constant_gamma", "constant delta Gamma_eff", "nabla delta Gamma_eff=0", "Constant scalar shifts sit in the derivative kernel unless fixed by gauge/boundary/normalization.", "ZERO_MODE_OWNER_REQUIRED"),
        ("ZM4752_2_divfree_K", "divergence-free delta K_hat", "nabla_mu delta K_hat^{mu nu}=0", "K variations in divergence kernel are invisible to q_tr unless extra constraints own them.", "ZERO_MODE_OWNER_REQUIRED"),
        ("ZM4752_3_projection_variation", "delta P_loc", "(DP_loc[X])q_raw^nu", "Projection variation is lower order but can leak unless parent-fixed or bounded.", "BOUND_REQUIRED"),
        ("ZM4752_4_background_terms", "h grad Gamma and delta-connection K", "L_bg[X]+L_conn[X]", "These are not positive algebraic rank terms without a sign/source theorem.", "SIGN_UNSIGNED"),
        ("ZM4752_5_boundary", "boundary/corner terms", "B_boundary[X]^nu", "Derivative integration needs boundary/no-flux/complementing conditions.", "BOUNDARY_OWNER_REQUIRED"),
        ("ZM4752_6_parent_addon", "separate algebraic source A_X", "Dq_tr includes A_X X", "Only a new parent action/source channel could restore the 4749 algebraic J_q route.", "OPTIONAL_DERIVATION_TARGET"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "zero_mode_id": zero_mode_id,
            "object": object_name,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for zero_mode_id, object_name, formula, meaning, status in specs
    ]


def jq_verdict_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "JQV4752_0_formula_route",
            "bare Gamma_eff/K_hat formula",
            "NO_FULL_RANK_ALGEBRAIC_JQ",
            "The principal map is ip^nu D_Gamma - ip_mu D_K^{mu nu}; it has no p-independent algebraic q channel.",
            "Do not use 4749 s_q shortcut from this route.",
        ),
        (
            "JQV4752_1_parent_addon",
            "separate parent algebraic source block A_X",
            "NOT_FOUND_BUT_LOGICALLY_ALLOWED",
            "If parent action adds A_X X directly to q_tr, then J_q=A_X could be ranked.",
            "Search/derive only if an action term supplies A_X.",
        ),
        (
            "JQV4752_2_derivative_gap",
            "Gamma/K derivative channel",
            "SURVIVES_AS_ELLIPTIC_ROUTE",
            "For p_min>0, a positive derivative symbol can support c_quar^deriv after zero-mode/boundary control.",
            "Move to zero-mode owner or derivative-gap bound.",
        ),
        (
            "JQV4752_3_local_branch_status",
            "local GR/Newton route",
            "NOT_DEAD_BUT_RECLASSIFIED",
            "The algebraic coupling shortcut fails from the formula, but a derivative elliptic proof route remains open.",
            "Do 4753 before demoting the branch.",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "verdict_id": verdict_id,
            "object": object_name,
            "verdict": verdict,
            "evidence": evidence,
            "next_action": next_action,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for verdict_id, object_name, verdict, evidence, next_action in specs
    ]


def derivative_gap_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "DGB4752_0_symbol_constant",
            "c_GK := inf_{|p|=1, X perp kernel} |p^nu D_Gamma[X]-p_mu D_K[X]^{mu nu}|^2/||X||^2",
            "Derivative symbol constant replacing the failed algebraic s_q^2 route.",
            "SOURCE_READY_VALUE_MISSING",
        ),
        (
            "DGB4752_1_gap_bound",
            "c_quar^deriv >= p_min^2 c_GK - C_lower - C_boundary - C_zero",
            "Derivative quarantine gap after lower-order, boundary and zero-mode losses.",
            "DERIVED_SOURCE_READY_BOUND",
        ),
        (
            "DGB4752_2_static_insert",
            "lambda_1^stat >= [min(c_TFRI,c_quar^deriv)-C_mix_eff-C_TT_kernel]/(C_P L_loc^2)",
            "Static local-test gap can be scored only after c_GK and all losses are sourced.",
            "NONCLAIM_INSERTION",
        ),
        (
            "DGB4752_3_failure_condition",
            "if p_min=0 or C_zero >= p_min^2 c_GK - C_lower - C_boundary then derivative gap does not prove local quiet",
            "Derivative route fails without zero-mode and boundary ownership.",
            "FAIL_CLOSED_RULE",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gap_id": gap_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gap_id, formula, meaning, status in specs
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4752_0_zero_mode_owner", "Prove p_min>0 and remove/fix constant Gamma plus div-free K kernels", "BEST_NEXT_ROUTE"),
        ("ROUTE4752_1_parent_addon", "Find a real parent algebraic source block A_X that creates J_q=A_X", "ONLY_IF_SOURCE_EXISTS"),
        ("ROUTE4752_2_finite_profile", "If derivative gap fails, carry finite q_tr/Sigma_metric profile bounds", "FALLBACK_ROUTE"),
        ("ROUTE4752_3_closure", "If no zero-mode owner and no profile bound, keep local transition branch closure-only", "HONEST_DEMOTION"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, status in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4752_0_no_algebraic_shortcut", "Do not use s_min(J_q)>0 from the bare Gamma/K formula", "PASS_BLOCKED_SHORTCUT"),
        ("GATE4752_1_cGK", "Source positive derivative symbol constant c_GK", "BLOCKED_SOURCE_VALUE_MISSING"),
        ("GATE4752_2_zero_mode", "Own p=0/constant/div-free kernels", "BLOCKED_ZERO_MODE_OWNER_MISSING"),
        ("GATE4752_3_boundary", "Source boundary/complementing conditions", "BLOCKED_BOUNDARY_OWNER_MISSING"),
        ("GATE4752_4_lower_order", "Bound projection/background/connection lower-order terms", "BLOCKED_LOWER_ORDER_BOUNDS_MISSING"),
        ("GATE4752_5_claim", "No local-GR/Newton claim until derivative gap is positive and sourced", "FAIL_CLOSED_NONCLAIM"),
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
        ("FW4752_0_no_Jq_decoration", "Do not rename a derivative symbol as algebraic J_q."),
        ("FW4752_1_no_lower_order_rank", "Do not use background-gradient or connection terms as positive rank without a sign theorem."),
        ("FW4752_2_no_zero_mode_hiding", "Do not ignore p=0, constant Gamma, divergence-free K, boundary or projector kernels."),
        ("FW4752_3_no_claim", "Derivative route is promising math, not local-GR evidence until sourced and positive."),
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
            "meaning": "Linearizing q_tr=grad Gamma_eff-div K_hat yields a derivative principal symbol, not the algebraic full-rank J_q shortcut; zero-mode owner/derivative gap is now the live route.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_DERIVATION_NONCLAIM",
            "summary": "Derived q_tr linearization; algebraic Jq shortcut fails for formula-only route; derivative elliptic gap route remains open.",
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
            "why": "4752 shows the formula gives a derivative symbol and a p=0 kernel; 4753 must prove/remove the zero mode or build the derivative gap bound.",
            "preferred_route": "Prove a zero-mode owner: fixed mean Gamma, divergence-free K quotient/gauge removal, boundary complementing conditions, and positive c_GK.",
            "fallback_route": "If zero modes cannot be owned, demote local transition route to closure/profile-bound only.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullet(rows: list[dict[str, Any]], key_field: str, value_field: str) -> str:
    return "\n".join(f"- `{row[key_field]}`: {row[value_field]}" for row in rows)


def write_docs(
    timestamp: str,
    linearization: list[dict[str, Any]],
    zero_modes: list[dict[str, Any]],
    jq_verdict: list[dict[str, Any]],
    gap_rows: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4752 Y5 R2FR: q_tr Linearization Jq Derivation From Gamma/Khat Or Close

Generated: `{timestamp}`

## Result

4752 attempts the derivation rather than searching again. Starting from:

```text
q_tr^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{{mu nu}})
```

the principal linearization is:

```text
sigma(Dq_tr)(p)[X]^nu = i p^nu D_Gamma[X] - i p_mu D_K[X]^{{mu nu}}.
```

This is a derivative symbol. Therefore the bare `Gamma_eff/K_hat` formula does **not** generate a p-independent full-rank algebraic `J_q`. The local branch is not dead, but it moves to a derivative elliptic-gap route with a zero-mode owner requirement.

## Linearization Rows

{bullet(linearization, "derivation_id", "status")}

## Zero-Mode Audit

{bullet(zero_modes, "zero_mode_id", "status")}

## Algebraic Jq Verdict

{bullet(jq_verdict, "verdict_id", "verdict")}

## Derivative Gap Bound

{bullet(gap_rows, "gap_id", "formula")}

## Route Matrix

{bullet(routes, "route_id", "status")}

## Promotion Gates

{bullet(gates, "gate_id", "status")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 768 PPC4161: q_tr Linearization Jq Derivation From Gamma/Khat Or Close

Generated: `{timestamp}`

## Derivation

From:

```text
q_tr^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{{mu nu}})
```

the frozen-principal symbol is:

```text
sigma(Dq_tr)(p)[X]^nu = i p^nu D_Gamma[X] - i p_mu D_K[X]^{{mu nu}}.
```

At `p=0`, this symbol vanishes. So the formula-only route gives:

```text
J_q^alg = 0
```

unless a separate parent algebraic source block is supplied.

## Surviving Route

The honest replacement is:

```text
c_quar^deriv >= p_min^2 c_GK - C_lower - C_boundary - C_zero.
```

This can still feed the static local-test gap, but only after zero modes, boundary terms, projection variation and lower-order connection/background terms are owned or bounded.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4752 linearizes the selected `q_tr = grad Gamma_eff - div K_hat` formula.
- The principal symbol is derivative: `sigma(Dq_tr)(p)[X]^nu = i p^nu D_Gamma[X] - i p_mu D_K[X]^{{mu nu}}`.
- Therefore the formula-only route has `J_q^alg=0` and cannot supply the 4749 algebraic full-rank shortcut.
- The live route becomes derivative elliptic control: `c_quar^deriv >= p_min^2 c_GK - C_lower - C_boundary - C_zero`.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4752 local packet update: the coupling is not just "missing"; the direct formula was linearized. It gives a derivative symbol, not an algebraic rank map. The next proof target is zero-mode ownership for the derivative gap.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4752-Y5-R2FR-qtr-linearization-Jq-derivation-from-Gamma-Khat-or-close.md`

## Decision

`{DECISION}`

## What moved forward

- Linearized the selected `q_tr = grad Gamma_eff - div K_hat` formula.
- Derived the principal derivative symbol `i p^nu D_Gamma - i p_mu D_K^{{mu nu}}`.
- Proved the formula-only route does not supply a p-independent full-rank algebraic `J_q`.
- Reclassified the live local route as derivative elliptic control with zero-mode, boundary and lower-order ownership requirements.

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
        "4752 linearizes q_tr=grad Gamma_eff-div K_hat and shows the bare formula gives a derivative symbol, not a full-rank algebraic J_q.",
        "Generated source register, qtr linearization derivation, zero-mode audit, algebraic Jq verdict, derivative gap bound, route matrix, gates, firewalls, decision, status, next target and validation.",
        "qtr_linearization_derivative_symbol_no_algebraic_Jq_nonclaim",
        NEXT_TARGET,
        "Renaming a derivative p-dependent symbol as algebraic J_q, hiding p=0 zero modes, or claiming local GR from an unsourced derivative gap.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need zero-mode owner, positive c_GK, boundary complementing conditions and lower-order bounds, or closure/profile demotion.",
        "q_tr linearization Jq derivation from Gamma/Khat or close",
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
    linearization: list[dict[str, Any]],
    zero_modes: list[dict[str, Any]],
    jq_verdict: list[dict[str, Any]],
    gap_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4752_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), "source register"))
    checks.append(("VAL4752_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), "source register"))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4752_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4752_2_principal_symbol", "linearization includes derivative principal symbol", any("sigma(Dq_tr)(p)" in row["formula"] and "p_mu" in row["formula"] for row in linearization), str(LINEARIZATION_CSV)))
    checks.append(("VAL4752_3_p_zero", "zero-mode audit includes p=0 kernel", any(row["object"] == "p=0" and "sigma(Dq_tr)(0)=0" in row["formula"] for row in zero_modes), str(ZERO_MODE_CSV)))
    checks.append(("VAL4752_4_no_alg_Jq", "Jq verdict blocks algebraic shortcut", any("NO_FULL_RANK_ALGEBRAIC_JQ" in row["verdict"] for row in jq_verdict), str(JQ_VERDICT_CSV)))
    checks.append(("VAL4752_5_derivative_gap", "derivative gap includes p_min, C_zero and boundary losses", any("p_min" in row["formula"] and "C_zero" in row["formula"] and "C_boundary" in row["formula"] for row in gap_rows), str(DERIV_GAP_CSV)))
    checks.append(("VAL4752_6_gates_nonclaim", "promotion gates keep claim closed", all(row["valid_for_claim"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4752_7_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4752_8_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4752_9_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4752_10_claim_row", "claim row L-594 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4752_11_resume", "resume points from 4752 to 4753", "4752-Y5" in resume_text and "4753-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4752_12_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
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
            "validation_id": "VAL4752_OVERALL",
            "check": "all 4752 derivation and nonclaim checks pass",
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
    linearization = linearization_rows(timestamp)
    zero_modes = zero_mode_rows(timestamp)
    jq_verdict = jq_verdict_rows(timestamp)
    gap_rows = derivative_gap_rows(timestamp)
    routes = route_matrix_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(LINEARIZATION_CSV, linearization)
    write_csv(ZERO_MODE_CSV, zero_modes)
    write_csv(JQ_VERDICT_CSV, jq_verdict)
    write_csv(DERIV_GAP_CSV, gap_rows)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, linearization, zero_modes, jq_verdict, gap_rows, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, linearization, zero_modes, jq_verdict, gap_rows, gates, timestamp))


if __name__ == "__main__":
    main()

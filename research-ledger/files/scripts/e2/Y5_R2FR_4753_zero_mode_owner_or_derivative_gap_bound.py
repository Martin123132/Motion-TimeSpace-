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

CHECKPOINT = "4753"
CLAIM_ID = "L-595"
MARKER = "PPC4161_ZERO_MODE_OWNER_OR_DERIVATIVE_GAP_BOUND_4753"
PACKET_MARKER = "PPC4161_PACKET_ZERO_MODE_OWNER_OR_DERIVATIVE_GAP_BOUND_4753"
DECISION = "UNRESTRICTED_DERIVATIVE_SYMBOL_HAS_CANCELLATION_KERNEL_KGAMMA_OWNER_OR_ANGLE_GAP_REQUIRED_NONCLAIM"
NEXT_TARGET = "4754-Y5-R2FR-KGamma-owner-adoption-or-cancellation-angle-bound.md"

DOC_PATH = POST / "4753-Y5-R2FR-zero-mode-owner-or-derivative-gap-bound.md"
FORMAL_PATH = FORMAL / "769-PPC4161-zero-mode-owner-or-derivative-gap-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4753_SOURCE_REGISTER.csv"
CANCELLATION_KERNEL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4753_DERIVATIVE_SYMBOL_CANCELLATION_KERNEL.csv"
ZERO_MODE_OWNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4753_ZERO_MODE_OWNER_CONDITIONS.csv"
DERIVATIVE_GAP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4753_DERIVATIVE_GAP_BOUND_REFINED.csv"
KGAMMA_IMPORT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4753_KGAMMA_ROUTE_IMPORT.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4753_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4753_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4753_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4753_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4753_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4753_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4753_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4753_0_4752_doc", POST / "4752-Y5-R2FR-qtr-linearization-Jq-derivation-from-Gamma-Khat-or-close.md", "sigma(Dq_tr)(p)", "4752 derivative-symbol derivation"),
    ("SRC4753_1_4752_formal", FORMAL / "768-PPC4161-qtr-linearization-Jq-derivation-from-Gamma-Khat-or-close.md", "J_q^alg = 0", "4752 no algebraic Jq result"),
    ("SRC4753_2_4752_zero", SOURCE_DIR / "P8_Y5_R2FR_4752_SYMBOL_AND_ZERO_MODE_AUDIT.csv", "ZM4752_0_p_zero", "4752 zero-mode audit"),
    ("SRC4753_3_4752_gap", SOURCE_DIR / "P8_Y5_R2FR_4752_DERIVATIVE_GAP_BOUND.csv", "DGB4752_1_gap_bound", "4752 derivative gap formula"),
    ("SRC4753_4_4752_next", SOURCE_DIR / "P8_Y5_R2FR_4752_NEXT_TARGET.csv", "zero-mode owner", "4753 handoff"),
    ("SRC4753_5_4341_contract", SOURCE_DIR / "P8_Y5_R2FR_4341_PARENT_SIGNATURE_CONTRACT.csv", "KRI4341_1_right_inverse_identity", "right-inverse owner contract"),
    ("SRC4753_6_4341_audit", SOURCE_DIR / "P8_Y5_R2FR_4341_ZERO_PROOF_AUDIT.csv", "AUD4341_2_algebraic_precedent", "K_L precedent audit"),
    ("SRC4753_7_4342_generator", SOURCE_DIR / "P8_Y5_R2FR_4342_KGAMMA_GENERATOR_ROWS.csv", "GEN4342_0_flat_Agamma", "KGamma generator construction"),
    ("SRC4753_8_4342_proof", SOURCE_DIR / "P8_Y5_R2FR_4342_PROOF_ROWS.csv", "PRF4342_0_flat_identity", "KGamma proof rows"),
    ("SRC4753_9_4342_bound", SOURCE_DIR / "P8_Y5_R2FR_4342_BOUND_ROWS.csv", "BND4342_2_CDeltaKdiv_kernel", "DeltaK/Kperp bound route"),
    ("SRC4753_10_4342_required", SOURCE_DIR / "P8_Y5_R2FR_4342_REQUIRED_INPUTS.csv", "IN4342_0_parent_adoption", "KGamma adoption missing inputs"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    CANCELLATION_KERNEL_CSV,
    ZERO_MODE_OWNER_CSV,
    DERIVATIVE_GAP_CSV,
    KGAMMA_IMPORT_CSV,
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


def cancellation_kernel_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "CK4753_0_symbol",
            "A_p(u,V)^nu = p^nu u - p_mu V^{mu nu}",
            "Frozen derivative symbol from 4752 after writing u=D_Gamma[X] and V=D_K[X].",
            "STARTING_SYMBOL",
        ),
        (
            "CK4753_1_pzero_kernel",
            "A_0(u,V)=0",
            "The p=0 zero mode cannot be controlled by a derivative symbol.",
            "ZERO_MODE_CONFIRMED",
        ),
        (
            "CK4753_2_Gamma_constant",
            "u=constant, p!=0 only sees gradients after inverse transform; mean u needs gauge/boundary fixing",
            "Scalar constant mode is harmless only if it is quotient/gauge or fixed by source normalization.",
            "OWNER_REQUIRED",
        ),
        (
            "CK4753_3_divfree_K",
            "p_mu V^{mu nu}=0 => A_p(0,V)=0",
            "Divergence-free K directions are invisible to q_tr and must be Kperp/gauge/boundary or finite metric residual.",
            "OWNER_REQUIRED",
        ),
        (
            "CK4753_4_mixed_cancellation",
            "for p!=0 choose V^{mu nu}=p^mu p^nu u/|p|^2, then p_mu V^{mu nu}=p^nu u and A_p(u,V)=0",
            "Even after p!=0, unrestricted independent Gamma and K variations have a cancellation kernel.",
            "COUNTERMODE_DERIVED",
        ),
        (
            "CK4753_5_unrestricted_constant",
            "c_GK_unrestricted=0",
            "The derivative symbol is not coercive on the unrestricted product space.",
            "NEGATIVE_COERCIVITY_RESULT",
        ),
        (
            "CK4753_6_survival_condition",
            "coercivity requires parent relation K=K_Gamma+Kperp, or angle margin between p u and p.V, or one leg frozen",
            "The branch survives only with an extra parent-owned domain restriction or finite bound.",
            "ROUTE_SPLIT",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "kernel_id": kernel_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for kernel_id, formula, meaning, status in specs
    ]


def zero_mode_owner_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ZMO4753_0_scalar_mean", "int_W delta Gamma_eff = 0 or delta Gamma_eff|boundary=0", "removes scalar constant mode", "PARENT_SOURCE_NORMALIZATION_OR_BOUNDARY_REQUIRED"),
        ("ZMO4753_1_K_divfree", "ker(div K) = K_perp quotient/gauge/topological sector or finite metric tail", "prevents invisible K from becoming hidden metric stress", "KPERP_OWNER_REQUIRED"),
        ("ZMO4753_2_mixed_kernel", "no free V_parallel=p^mu p^nu u/|p|^2 cancellation unless generated by K_Gamma owner", "kills mixed Gamma/K cancellation", "DOMAIN_RELATION_REQUIRED"),
        ("ZMO4753_3_boundary", "fixed Green boundary/collar and complementing conditions", "turns p_min into an actual spectral lower bound", "BOUNDARY_COMPLEMENTING_REQUIRED"),
        ("ZMO4753_4_projection", "D_v P_loc=0 or ||D_v P_loc|| bounded", "prevents local projector variation from reintroducing q_tr", "PROJECTION_OWNER_REQUIRED"),
        ("ZMO4753_5_lower_order", "C_lower=C_conn+C_bg+C_projection sourced and smaller than leading gap", "prevents lower-order terms from eating the gap", "LOWER_ORDER_BOUND_REQUIRED"),
        ("ZMO4753_6_metric_safety", "Sigma_metric[Kperp/S_RI] zero or below arena bounds", "cancelling q_tr cannot create a new metric source elsewhere", "METRIC_TRANSFER_REQUIRED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "owner_id": owner_id,
            "condition": condition,
            "purpose": purpose,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for owner_id, condition, purpose, status in specs
    ]


def derivative_gap_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "DGR4753_0_unrestricted",
            "c_GK_unrestricted=0",
            "Mixed Gamma/K cancellation shows no positive derivative gap on the unrestricted product domain.",
            "PROVED_NEGATIVE",
        ),
        (
            "DGR4753_1_angle_margin",
            "if |<p u, p.V>| <= rho_GK ||p u|| ||p.V|| with rho_GK<1, then ||A_p||^2 >= (1-rho_GK)(||p u||^2+||p.V||^2)",
            "A sourced cancellation-angle margin can restore coercivity.",
            "SOURCE_READY_CONDITIONAL",
        ),
        (
            "DGR4753_2_effective_gap",
            "c_quar^deriv >= p_min^2 (1-rho_GK)c_GK0 - C_lower - C_boundary - C_zero - C_Kperp_metric",
            "Refined derivative gap with cancellation, lower-order, boundary, zero-mode and metric-tail losses.",
            "REFINED_BOUND",
        ),
        (
            "DGR4753_3_KGamma_route",
            "K_hat=K_Gamma+K_perp, div K_Gamma=grad Gamma_eff => q_tr=-div K_perp + C_RI+C_conn+B_boundary",
            "The KGamma route cancels the dangerous mixed symbol by parent structure rather than angle-fitting.",
            "PREFERRED_ROUTE_CONDITIONAL",
        ),
        (
            "DGR4753_4_static_insert",
            "lambda_1^stat >= [min(c_TFRI,c_quar^deriv)-C_mix_eff-C_TT_kernel]/(C_P L_loc^2)",
            "Static scoring remains closed until the refined gap terms are sourced and positive.",
            "NONCLAIM_STATIC_INSERT",
        ),
        (
            "DGR4753_5_failure",
            "if rho_GK=1 or parent KGamma/domain relation is unsigned, c_quar^deriv is not claimable",
            "Prevents using derivative notation as a hidden closure axiom.",
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


def kgamma_import_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("KGI4753_0_4341_contract", "4341", "K_hat=K_Gamma+Delta_K parent-signature contract exists but parent owner is unsigned", "IMPORT_AS_REQUIREMENT"),
        ("KGI4753_1_4342_flat", "4342", "flat-patch KGamma from K_L satisfies div K_Gamma=grad Gamma_eff", "REAL_DIFFERENTIAL_IDENTITY"),
        ("KGI4753_2_4342_curved", "4342", "Ricci-corrected curved operator form exists if inverse/boundary data exist", "CONDITIONAL_CURVED_OPERATOR"),
        ("KGI4753_3_CRI", "4342", "C_RI=0 only on fixed flat branch; curved/boundary tail remains open", "COMMUTATOR_BOUND_REQUIRED"),
        ("KGI4753_4_Kperp", "4342", "DeltaK divergence reduced to Kperp kernel or finite Kperp metric-tail bound", "KPERP_OWNER_REQUIRED"),
        ("KGI4753_5_parent_adoption", "4342", "S_RI[A_Gamma,Gamma_eff] parent adoption is still missing", "BLOCKED_PARENT_ACTION_SIGNATURE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "import_id": import_id,
            "source_checkpoint": source_checkpoint,
            "result": result,
            "4753_role": role,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for import_id, source_checkpoint, result, role in specs
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4753_0_KGamma_owner", "Parent-adopt KGamma right-inverse owner and prove Kperp/metric-tail safety", "BEST_ROUTE"),
        ("ROUTE4753_1_angle_gap", "Source rho_GK<1 cancellation-angle margin plus p_min and lower-order bounds", "SECOND_ROUTE"),
        ("ROUTE4753_2_single_leg", "Show D_K=0 or D_Gamma=0 in the relevant branch and use scalar/Hodge Poincare gap", "NARROW_ROUTE"),
        ("ROUTE4753_3_profile_bound", "If no coercive route, carry finite q_tr/Sigma_metric profile residuals", "FALLBACK_ROUTE"),
        ("ROUTE4753_4_closure", "If no parent owner or finite profile, keep local transition as explicit closure-only", "HONEST_DEMOTION"),
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
        ("GATE4753_0_countermode", "Acknowledge unrestricted mixed cancellation gives c_GK=0", "PASS_NEGATIVE_DERIVATION"),
        ("GATE4753_1_KGamma", "Parent-adopt S_RI/KGamma or source equivalent domain relation", "BLOCKED_PARENT_OWNER_MISSING"),
        ("GATE4753_2_angle", "Alternatively source rho_GK<1 cancellation angle", "BLOCKED_ANGLE_SOURCE_MISSING"),
        ("GATE4753_3_zero_modes", "Fix scalar mean, Kperp divergence kernel and p_min boundary data", "BLOCKED_ZERO_MODE_OWNER_MISSING"),
        ("GATE4753_4_metric_tail", "Bound Kperp/S_RI metric transfer into PPN/R10/clock/orbit/WEP", "BLOCKED_METRIC_TRANSFER_MISSING"),
        ("GATE4753_5_claim", "No local-GR/Newton claim from derivative gap until all gates pass", "FAIL_CLOSED_NONCLAIM"),
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
        ("FW4753_0_no_unrestricted_gap", "Do not claim positive c_GK on unrestricted Gamma/K product space."),
        ("FW4753_1_no_angle_by_wish", "Do not set rho_GK<1 without a parent domain theorem or source row."),
        ("FW4753_2_no_KGamma_without_owner", "Do not use the KGamma differential identity as parent action adoption."),
        ("FW4753_3_no_metric_tail_hiding", "Do not cancel q_tr by Kperp/S_RI while ignoring metric stress transfer."),
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
            "meaning": "4753 proves the unrestricted derivative symbol has a mixed cancellation kernel; the live route is KGamma owner adoption or a sourced cancellation-angle/domain gap, with metric-tail controls.",
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
            "summary": "Zero-mode/coercivity audit completed; unrestricted derivative gap fails, KGamma owner or angle-gap route selected.",
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
            "why": "4753 shows no positive derivative gap exists without a parent relation or cancellation-angle bound; 4342 provides a real KGamma identity but parent owner adoption is still missing.",
            "preferred_route": "Attempt parent adoption of the KGamma right-inverse owner block S_RI and prove metric-tail safety for Kperp/S_RI.",
            "fallback_route": "If parent adoption fails, source a cancellation-angle bound rho_GK<1 or demote to finite profile/closure-only.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullet(rows: list[dict[str, Any]], key_field: str, value_field: str) -> str:
    return "\n".join(f"- `{row[key_field]}`: {row[value_field]}" for row in rows)


def write_docs(
    timestamp: str,
    kernels: list[dict[str, Any]],
    owners: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    imports: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4753 Y5 R2FR: Zero-Mode Owner Or Derivative Gap Bound

Generated: `{timestamp}`

## Result

4753 tests whether the derivative route from 4752 is coercive. With

```text
A_p(u,V)^nu = p^nu u - p_mu V^{{mu nu}},
```

the unrestricted product space has a mixed cancellation kernel:

```text
V^{{mu nu}} = p^mu p^nu u/|p|^2  =>  A_p(u,V)=0.
```

Therefore `c_GK_unrestricted=0`. The derivative route is not dead, but it requires a parent-owned domain relation, most naturally the `K_Gamma` right-inverse owner route, or a sourced cancellation-angle margin.

## Cancellation Kernel

{bullet(kernels, "kernel_id", "status")}

## Zero-Mode Owner Conditions

{bullet(owners, "owner_id", "status")}

## Refined Derivative Gap

{bullet(gaps, "gap_id", "formula")}

## KGamma Import

{bullet(imports, "import_id", "4753_role")}

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

    formal = f"""# 769 PPC4161: Zero-Mode Owner Or Derivative Gap Bound

Generated: `{timestamp}`

## Kernel Result

The 4752 derivative symbol is:

```text
A_p(u,V)^nu = p^nu u - p_mu V^{{mu nu}}.
```

For `p != 0`, the choice:

```text
V^{{mu nu}} = p^mu p^nu u/|p|^2
```

gives `A_p(u,V)=0`. Hence:

```text
c_GK_unrestricted = 0.
```

## Surviving Gap Law

A positive gap can only be claimed after a parent domain relation or angle bound:

```text
c_quar^deriv >= p_min^2 (1-rho_GK)c_GK0 - C_lower - C_boundary - C_zero - C_Kperp_metric.
```

The preferred route is the existing `K_Gamma` identity from 4342, but it must be parent-adopted and metric-safe before it can score.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`

Marker: `{MARKER}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4753 proves the unrestricted derivative symbol has a mixed Gamma/K cancellation kernel.
- Therefore `c_GK_unrestricted=0`; derivative notation alone cannot prove local quiet.
- The surviving routes are: parent-adopt `K_Gamma`, source a cancellation-angle/domain gap, freeze one leg, or fall back to finite profile/closure.
- The refined bound is `c_quar^deriv >= p_min^2 (1-rho_GK)c_GK0 - C_lower - C_boundary - C_zero - C_Kperp_metric`.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4753 local packet update: the derivative route has been stress-tested. It is not automatically coercive; it needs `K_Gamma` parent adoption or a sourced cancellation-angle bound.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4753-Y5-R2FR-zero-mode-owner-or-derivative-gap-bound.md`

## Decision

`{DECISION}`

## What moved forward

- Proved the unrestricted Gamma/K derivative symbol has a mixed cancellation kernel.
- Established `c_GK_unrestricted=0`, so the derivative gap cannot be claimed by notation.
- Imported the 4342 `K_Gamma` right-inverse identity as the best live route, but kept parent adoption and metric-tail safety open.
- Refined the derivative gap to include cancellation angle, zero-mode, boundary, lower-order and Kperp metric-tail losses.

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
        "4753 proves the unrestricted Gamma/K derivative symbol has a mixed cancellation kernel, so c_GK requires KGamma parent adoption or a sourced angle/domain gap.",
        "Generated source register, derivative symbol cancellation kernel, zero-mode owner conditions, refined derivative gap bound, KGamma import, route matrix, gates, firewalls, decision, status, next target and validation.",
        "unrestricted_derivative_gap_cancels_KGamma_or_angle_gap_required_nonclaim",
        NEXT_TARGET,
        "Claiming positive derivative coercivity while ignoring mixed Gamma/K cancellation, zero modes, or metric tails.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need parent adoption of KGamma/S_RI with metric safety, or a sourced rho_GK<1 cancellation-angle bound.",
        "Zero-mode owner or derivative gap bound",
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
    kernels: list[dict[str, Any]],
    owners: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    imports: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4753_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), "source register"))
    checks.append(("VAL4753_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), "source register"))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4753_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4753_2_countermode", "cancellation kernel includes explicit mixed countermode", any("p^mu p^nu u/|p|^2" in row["formula"] and "A_p(u,V)=0" in row["formula"] for row in kernels), str(CANCELLATION_KERNEL_CSV)))
    checks.append(("VAL4753_3_unrestricted_zero", "unrestricted c_GK is zero", any("c_GK_unrestricted=0" in row["formula"] for row in kernels + gaps), f"{CANCELLATION_KERNEL_CSV}; {DERIVATIVE_GAP_CSV}"))
    checks.append(("VAL4753_4_zero_owner", "zero-mode owners include scalar mean, K kernel and mixed kernel", all(any(key in row["condition"] for row in owners) for key in ["delta Gamma", "ker(div K)", "V_parallel"]), str(ZERO_MODE_OWNER_CSV)))
    checks.append(("VAL4753_5_refined_gap", "refined gap contains rho_GK and Kperp metric tail", any("rho_GK" in row["formula"] and "C_Kperp_metric" in row["formula"] for row in gaps), str(DERIVATIVE_GAP_CSV)))
    checks.append(("VAL4753_6_KGamma_import", "KGamma import carries 4342 flat identity and parent adoption blocker", any("flat-patch KGamma" in row["result"] for row in imports) and any("parent adoption" in row["result"] for row in imports), str(KGAMMA_IMPORT_CSV)))
    checks.append(("VAL4753_7_gates_nonclaim", "promotion gates keep claim closed", all(row["valid_for_claim"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4753_8_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4753_9_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4753_10_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4753_11_claim_row", "claim row L-595 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4753_12_resume", "resume points from 4753 to 4754", "4753-Y5" in resume_text and "4754-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4753_13_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
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
            "validation_id": "VAL4753_OVERALL",
            "check": "all 4753 zero-mode/cancellation and nonclaim checks pass",
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
    kernels = cancellation_kernel_rows(timestamp)
    owners = zero_mode_owner_rows(timestamp)
    gaps = derivative_gap_rows(timestamp)
    imports = kgamma_import_rows(timestamp)
    routes = route_matrix_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(CANCELLATION_KERNEL_CSV, kernels)
    write_csv(ZERO_MODE_OWNER_CSV, owners)
    write_csv(DERIVATIVE_GAP_CSV, gaps)
    write_csv(KGAMMA_IMPORT_CSV, imports)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, kernels, owners, gaps, imports, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, kernels, owners, gaps, imports, gates, timestamp))


if __name__ == "__main__":
    main()

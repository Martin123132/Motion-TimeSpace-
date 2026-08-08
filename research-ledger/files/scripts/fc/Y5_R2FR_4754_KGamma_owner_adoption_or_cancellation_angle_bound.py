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

CHECKPOINT = "4754"
CLAIM_ID = "L-596"
MARKER = "PPC4161_KGAMMA_OWNER_ADOPTION_OR_CANCELLATION_ANGLE_BOUND_4754"
PACKET_MARKER = "PPC4161_PACKET_KGAMMA_OWNER_ADOPTION_OR_CANCELLATION_ANGLE_BOUND_4754"
DECISION = "KGAMMA_OWNER_ACTION_CANDIDATE_IMPORTED_ADJOINT_ZERO_PACKET_REQUIRED_ANGLE_BOUND_FALLBACK_NONCLAIM"
NEXT_TARGET = "4755-Y5-R2FR-lambdaRI-boundary-Kperp-source-packet-or-profile-demotion.md"

DOC_PATH = POST / "4754-Y5-R2FR-KGamma-owner-adoption-or-cancellation-angle-bound.md"
FORMAL_PATH = FORMAL / "770-PPC4161-KGamma-owner-adoption-or-cancellation-angle-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4754_SOURCE_REGISTER.csv"
OWNER_ACTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4754_KGAMMA_OWNER_ACTION_ADOPTION_TEST.csv"
ADJOINT_PACKET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4754_ADJOINT_ZERO_SOURCE_PACKET.csv"
METRIC_TAIL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4754_METRIC_TAIL_AND_KPERP_TRANSFER_GATE.csv"
CANCELLATION_ANGLE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4754_CANCELLATION_ANGLE_FALLBACK.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4754_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4754_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4754_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4754_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4754_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4754_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4754_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4754_0_4753_doc", POST / "4753-Y5-R2FR-zero-mode-owner-or-derivative-gap-bound.md", "c_GK_unrestricted=0", "4753 cancellation-kernel result"),
    ("SRC4754_1_4753_formal", FORMAL / "769-PPC4161-zero-mode-owner-or-derivative-gap-bound.md", "c_quar^deriv", "4753 refined derivative bound"),
    ("SRC4754_2_4753_import", SOURCE_DIR / "P8_Y5_R2FR_4753_KGAMMA_ROUTE_IMPORT.csv", "KGI4753_5_parent_adoption", "4753 KGamma import blocker"),
    ("SRC4754_3_4753_next", SOURCE_DIR / "P8_Y5_R2FR_4753_NEXT_TARGET.csv", "KGamma right-inverse owner block", "4754 handoff"),
    ("SRC4754_4_4343_action", SOURCE_DIR / "P8_Y5_R2FR_4343_ACTION_CANDIDATE_ROWS.csv", "ACT4343_0_multiplier_owner", "KGamma owner action candidate"),
    ("SRC4754_5_4343_el", SOURCE_DIR / "P8_Y5_R2FR_4343_EULER_LAGRANGE_ROWS.csv", "EL4343_0_vary_Lambda", "Euler-Lagrange owner equation"),
    ("SRC4754_6_4343_metric", SOURCE_DIR / "P8_Y5_R2FR_4343_METRIC_NULL_AUDIT.csv", "MN4343_1_no_hidden_stress", "metric-null caveat"),
    ("SRC4754_7_4343_kperp", SOURCE_DIR / "P8_Y5_R2FR_4343_KPERP_BOUND_RUNNER.csv", "KP4343_3_total_vector", "Kperp finite transfer runner"),
    ("SRC4754_8_4344_adj", SOURCE_DIR / "P8_Y5_R2FR_4344_ADJOINT_ROWS.csv", "ADJ4344_2_lambda_RI_floor", "adjoint zero floor"),
    ("SRC4754_9_4344_theorem", SOURCE_DIR / "P8_Y5_R2FR_4344_THEOREM_ROWS.csv", "TH4344_0_adjoint_zero", "conditional adjoint zero theorem"),
    ("SRC4754_10_4344_boundary", SOURCE_DIR / "P8_Y5_R2FR_4344_BOUNDARY_ROWS.csv", "BD4344_0_Dirichlet", "boundary zero route"),
    ("SRC4754_11_4344_score", SOURCE_DIR / "P8_Y5_R2FR_4344_SCORE_ROWS.csv", "SCR4344_3_combined", "owner-tail plus Kperp score row"),
    ("SRC4754_12_4344_inputs", SOURCE_DIR / "P8_Y5_R2FR_4344_REQUIRED_INPUTS.csv", "IN4344_0_lambda_RI", "remaining source packet inputs"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    OWNER_ACTION_CSV,
    ADJOINT_PACKET_CSV,
    METRIC_TAIL_CSV,
    CANCELLATION_ANGLE_CSV,
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


def owner_action_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "OA4754_0_candidate",
            "S_RI=int_U sqrt(-g) Lambda_nu [L_RI A_Gamma^nu + nabla^nu Gamma_eff]",
            "Concrete multiplier owner action imported from 4343.",
            "CANDIDATE_ACTION_EXISTS",
        ),
        (
            "OA4754_1_constraint",
            "delta_Lambda S_RI=0 => L_RI A_Gamma^nu + nabla^nu Gamma_eff=0",
            "The KGamma right-inverse equation is parent-owned if this action is adopted.",
            "EULER_EQUATION_DERIVED",
        ),
        (
            "OA4754_2_multiplier",
            "delta_A S_RI=0 => L_RI^dagger Lambda=0 + boundary",
            "Metric silence needs Lambda=0, not merely the constraint equation.",
            "ADJOINT_ZERO_REQUIRED",
        ),
        (
            "OA4754_3_metric_tail",
            "T_RI = constraint-proportional + Lambda-proportional + B_RI",
            "Owner block is metric-null only if constraint=0, Lambda=0 and boundary/corner stress is zero/routed.",
            "METRIC_NULL_CONDITIONAL",
        ),
        (
            "OA4754_4_adoption_status",
            "parent action adoption of S_RI is not globally signed in the current corpus",
            "The candidate is useful but not yet a local-GR proof.",
            "PARENT_ADOPTION_UNSIGNED",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "owner_action_id": owner_action_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for owner_action_id, formula, meaning, status in specs
    ]


def adjoint_packet_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ADJPK4754_0_lambda_RI", "lambda_RI = Z_RI,min lambda_1(D_RI)+M_RI,min^2-Eta_RI > 0", "kills homogeneous Lambda on static collar", "FORMULA_READY_VALUE_UNSOURCED"),
        ("ADJPK4754_1_boundary", "B_Lambda=0 and B_RI=0, or routed boundary flux ledger", "prevents owner stress through boundary/corner", "MISSING_ZERO_OR_BOUND"),
        ("ADJPK4754_2_incoming", "I_RI=0 or finite incoming/hyperbolic mode bound", "guards against using static proof in dynamic branch", "MISSING_ZERO_OR_BOUND"),
        ("ADJPK4754_3_residual", "R_Lambda=0 or ||Lambda|| <= C_RI_adj R_Lambda/lambda_RI", "finite owner-tail branch if exact adjoint zero fails", "MISSING_IF_NONZERO_BRANCH"),
        ("ADJPK4754_4_Kperp", "Y_Kperp_i=|W_i^K| C_T(|S_T|+|B_T|+|I_T|+|Z_T|)", "first Kperp transfer row into local arenas", "VALUES_MISSING"),
        ("ADJPK4754_5_combined", "Y_a <= Pi_a^RI C_Lambda R_Lambda/lambda_RI + Pi_a^BRI B_RI + Pi_a^I I_RI + Y_Kperp_a", "complete nonclaim owner-tail vector", "SOURCE_PACKET_REQUIRED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "packet_id": packet_id,
            "formula": formula,
            "purpose": purpose,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for packet_id, formula, purpose, status in specs
    ]


def metric_tail_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("MT4754_0_clean_zero", "Y_owner=0", "if S_RI adopted, constraint=0, Lambda=0, B_RI=0, I_RI=0", "CONDITIONAL_ZERO_BRANCH"),
        ("MT4754_1_owner_tail", "Y_owner_a <= Pi_a^RI C_Lambda R_Lambda/lambda_RI + Pi_a^BRI B_RI + Pi_a^I I_RI", "finite owner stress tail if adjoint/boundary/incoming rows fail", "BOUND_FORMULA_READY_VALUES_MISSING"),
        ("MT4754_2_Kperp_clean", "R_i^K=0", "if K_perp is GR TT/radiative, quotient vertical, or routed boundary with parent-signed projection zero", "CLEAN_SECTOR_UNSIGNED"),
        ("MT4754_3_Kperp_finite", "|R_i^K| <= |W_i^K| C_T(|S_T|+|B_T|+|I_T|+|Z_T|)", "finite Kperp score branch", "VALUES_MISSING"),
        ("MT4754_4_total", "Y_a^4754 <= Y_owner_a + |W_a^K| C_T(|S_T|+|B_T|+|I_T|+|Z_T|)", "combined local residual vector for PPN/R10/clock/orbital/WEP", "NONCLAIM_VECTOR_READY_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "tail_id": tail_id,
            "formula": formula,
            "condition_or_meaning": condition,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for tail_id, formula, condition, status in specs
    ]


def cancellation_angle_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ANG4754_0_needed", "rho_GK < 1", "angle/correlation margin between p^nu D_Gamma and p_mu D_K", "MISSING_SOURCE_ROW"),
        ("ANG4754_1_bound", "c_quar^deriv >= p_min^2(1-rho_GK)c_GK0 - C_lower - C_boundary - C_zero - C_Kperp_metric", "fallback if KGamma owner adoption is not signed", "FORMULA_READY_VALUES_MISSING"),
        ("ANG4754_2_failure", "rho_GK=1", "recovers 4753 mixed cancellation kernel and c_GK=0", "FAIL_CLOSED_RULE"),
        ("ANG4754_3_source_rule", "rho_GK must be fixed by parent domain/operator relation before local data scoring", "prevents angle fitting to pass PPN/R10", "ANTI_TUNING_RULE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "angle_id": angle_id,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for angle_id, formula, meaning, status in specs
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4754_0_SRI_packet", "Build/source S_RI adoption + lambda_RI + boundary/incoming + Kperp packet", "BEST_ROUTE"),
        ("ROUTE4754_1_angle_bound", "If S_RI adoption fails, source rho_GK<1 and all refined derivative-gap losses", "SECOND_ROUTE"),
        ("ROUTE4754_2_profile", "If neither works, run finite profile residual vector Y_a^4754 against local arenas", "FALLBACK_ROUTE"),
        ("ROUTE4754_3_closure", "If no source packet/profile row exists, keep local transition branch closure-only", "HONEST_DEMOTION"),
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
        ("GATE4754_0_action", "S_RI parent adoption explicitly signed", "BLOCKED_PARENT_ADOPTION_UNSIGNED"),
        ("GATE4754_1_lambda", "lambda_RI>0 sourced for declared local collar", "BLOCKED_VALUE_UNSOURCED"),
        ("GATE4754_2_boundary", "B_Lambda/B_RI zero or bounded", "BLOCKED_BOUNDARY_ROW_MISSING"),
        ("GATE4754_3_incoming", "I_RI static/hyperbolic guard closed", "BLOCKED_INCOMING_ROW_MISSING"),
        ("GATE4754_4_Kperp", "Kperp clean sector or finite local transfer below bounds", "BLOCKED_KPERP_VALUES_MISSING"),
        ("GATE4754_5_angle", "rho_GK<1 sourced if using angle fallback", "BLOCKED_ANGLE_SOURCE_MISSING"),
        ("GATE4754_6_claim", "No local-GR/Newton claim until owner packet or angle fallback is source-complete", "FAIL_CLOSED_NONCLAIM"),
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
        ("FW4754_0_candidate_not_adoption", "Do not treat the S_RI candidate as globally parent-adopted."),
        ("FW4754_1_multiplier_stress", "Do not ignore Lambda or boundary stress in the metric variation."),
        ("FW4754_2_Gcal", "This route does not derive Newton's constant; keep calibrated G caveat."),
        ("FW4754_3_angle_tuning", "Do not choose rho_GK after seeing local-test bounds."),
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
            "meaning": "4754 imports the concrete KGamma multiplier owner candidate and reduces rescue to a source packet: S_RI adoption, lambda_RI, boundary/incoming silence and Kperp metric-tail bounds; angle fallback remains unsourced.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_OWNER_PACKET_NONCLAIM",
            "summary": "KGamma owner candidate imported; adjoint-zero/source packet and cancellation-angle fallback staged; no local claim opened.",
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
            "why": "The owner rescue now depends on sourcing lambda_RI, boundary/incoming rows and Kperp transfer coefficients, or else demoting to finite profile/closure.",
            "preferred_route": "Build the source packet for lambda_RI, B_Lambda/B_RI, I_RI, R_Lambda and Kperp coefficients, preserving nonclaim status.",
            "fallback_route": "If source packet cannot be built, demote the KGamma rescue to finite profile/closure-only and use the angle-bound route only with parent-sourced rho_GK.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullet(rows: list[dict[str, Any]], key_field: str, value_field: str) -> str:
    return "\n".join(f"- `{row[key_field]}`: {row[value_field]}" for row in rows)


def write_docs(
    timestamp: str,
    owner_rows: list[dict[str, Any]],
    adjoint_rows: list[dict[str, Any]],
    tail_rows: list[dict[str, Any]],
    angle_rows: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4754 Y5 R2FR: KGamma Owner Adoption Or Cancellation-Angle Bound

Generated: `{timestamp}`

## Result

4754 imports the concrete `K_Gamma` multiplier owner route from 4343/4344 and places it into the newer 4753 cancellation-kernel logic. The rescue route is mathematically plausible, but still nonclaim: the corpus has a candidate owner action, not a globally signed parent adoption.

## Owner Action Test

{bullet(owner_rows, "owner_action_id", "status")}

## Adjoint-Zero Source Packet

{bullet(adjoint_rows, "packet_id", "status")}

## Metric Tail / Kperp Gate

{bullet(tail_rows, "tail_id", "status")}

## Cancellation-Angle Fallback

{bullet(angle_rows, "angle_id", "status")}

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

    formal = f"""# 770 PPC4161: KGamma Owner Adoption Or Cancellation-Angle Bound

Generated: `{timestamp}`

## Owner Candidate

The candidate rescue action is:

```text
S_RI = int_U sqrt(-g) Lambda_nu [L_RI A_Gamma^nu + nabla^nu Gamma_eff].
```

It gives:

```text
delta_Lambda S_RI = 0 => L_RI A_Gamma^nu + nabla^nu Gamma_eff = 0.
```

Metric silence additionally requires:

```text
L_RI^dagger Lambda = 0,  B_Lambda=0,  B_RI=0,  I_RI=0.
```

The current packet is not source-complete. The fallback is:

```text
c_quar^deriv >= p_min^2(1-rho_GK)c_GK0 - C_lower - C_boundary - C_zero - C_Kperp_metric.
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

- 4754 imports the concrete `K_Gamma` multiplier owner candidate: `S_RI=int sqrt(-g) Lambda[L_RI A_Gamma+nabla Gamma_eff]`.
- It reduces metric safety to adjoint zero plus boundary/incoming silence: `lambda_RI>0`, `B_Lambda=0`, `B_RI=0`, `I_RI=0`.
- It retains Kperp/owner-tail finite transfer rows instead of hiding stress.
- Cancellation-angle fallback remains source-ready but unsourced.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4754 local packet update: the KGamma rescue now has a precise source packet. If the packet cannot be sourced, the local transition route must fall back to finite profile/closure.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4754-Y5-R2FR-KGamma-owner-adoption-or-cancellation-angle-bound.md`

## Decision

`{DECISION}`

## What moved forward

- Imported the concrete `K_Gamma` multiplier owner action candidate.
- Reduced owner metric silence to an explicit source packet: `lambda_RI`, `B_Lambda`, `B_RI`, `I_RI`, `R_Lambda`, and Kperp transfer coefficients.
- Kept the cancellation-angle fallback source-ready but unsourced.
- Preserved nonclaim status for local GR/Newton.

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
        "4754 imports the concrete KGamma owner action candidate and reduces the rescue route to adjoint-zero, boundary, incoming and Kperp source rows.",
        "Generated source register, KGamma owner adoption test, adjoint zero source packet, metric-tail/Kperp transfer gate, cancellation-angle fallback, route matrix, gates, firewalls, decision, status, next target and validation.",
        "KGamma_owner_packet_staged_nonclaim",
        NEXT_TARGET,
        "Treating a candidate owner action as parent adoption, or ignoring multiplier/boundary/Kperp metric tails.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need lambda_RI, boundary/incoming rows, R_Lambda and Kperp coefficients sourced before any local-GR/Newton claim.",
        "KGamma owner adoption or cancellation angle bound",
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
    owner_rows: list[dict[str, Any]],
    adjoint_rows: list[dict[str, Any]],
    tail_rows: list[dict[str, Any]],
    angle_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4754_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), "source register"))
    checks.append(("VAL4754_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), "source register"))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4754_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4754_2_owner_action", "owner action test includes S_RI candidate and parent-adoption unsigned", any("S_RI" in row["formula"] for row in owner_rows) and any("PARENT_ADOPTION_UNSIGNED" in row["status"] for row in owner_rows), str(OWNER_ACTION_CSV)))
    checks.append(("VAL4754_3_adjoint_packet", "adjoint packet includes lambda_RI and boundary rows", any("lambda_RI" in row["formula"] for row in adjoint_rows) and any("B_Lambda" in row["formula"] for row in adjoint_rows), str(ADJOINT_PACKET_CSV)))
    checks.append(("VAL4754_4_metric_tail", "metric tail includes owner and Kperp residual vectors", any("Y_owner_a" in row["formula"] for row in tail_rows) and any("Y_a^4754" in row["formula"] for row in tail_rows), str(METRIC_TAIL_CSV)))
    checks.append(("VAL4754_5_angle_fallback", "angle fallback includes rho_GK<1 and anti-tuning rule", any("rho_GK < 1" in row["formula"] for row in angle_rows) and any("ANTI_TUNING" in row["status"] for row in angle_rows), str(CANCELLATION_ANGLE_CSV)))
    checks.append(("VAL4754_6_gates_nonclaim", "promotion gates keep claim closed", all(row["valid_for_claim"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4754_7_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4754_8_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4754_9_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4754_10_claim_row", "claim row L-596 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4754_11_resume", "resume points from 4754 to 4755", "4754-Y5" in resume_text and "4755-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4754_12_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
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
            "validation_id": "VAL4754_OVERALL",
            "check": "all 4754 owner-packet and nonclaim checks pass",
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
    owner_rows = owner_action_rows(timestamp)
    adjoint_rows = adjoint_packet_rows(timestamp)
    tail_rows = metric_tail_rows(timestamp)
    angle_rows = cancellation_angle_rows(timestamp)
    routes = route_matrix_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(OWNER_ACTION_CSV, owner_rows)
    write_csv(ADJOINT_PACKET_CSV, adjoint_rows)
    write_csv(METRIC_TAIL_CSV, tail_rows)
    write_csv(CANCELLATION_ANGLE_CSV, angle_rows)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, owner_rows, adjoint_rows, tail_rows, angle_rows, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, owner_rows, adjoint_rows, tail_rows, angle_rows, gates, timestamp))


if __name__ == "__main__":
    main()

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

CHECKPOINT = "4765"
CLAIM_ID = "L-607"
MARKER = "PPC4161_QEDGE_SHELL_ZERO_CERTIFICATE_OR_DENOMINATOR_SOURCE_BOUND_PACK_4765"
PACKET_MARKER = "PPC4161_PACKET_QEDGE_SHELL_ZERO_CERTIFICATE_OR_DENOMINATOR_SOURCE_BOUND_PACK_4765"
DECISION = "QEDGE_SHELL_ZERO_CERTIFICATE_DERIVED_CONDITIONAL_TRACE_BIRTH_VALUES_MISSING_DENOMINATOR_PACK_PARALLEL_NONCLAIM"
NEXT_TARGET = "4766-Y5-R2FR-source-collar-trace-birth-inputs-or-Poynting-wall-flux-row.md"

DOC_PATH = POST / "4765-Y5-R2FR-Qedge-shell-zero-certificate-or-denominator-source-bound-pack.md"
FORMAL_PATH = FORMAL / "781-PPC4161-Qedge-shell-zero-certificate-or-denominator-source-bound-pack.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4765_SOURCE_REGISTER.csv"
ZERO_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4765_QEDGE_SHELL_ZERO_CERTIFICATE_AUDIT.csv"
BOUND_PACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4765_QEDGE_SHELL_BOUND_PACK.csv"
DENOMINATOR_PARALLEL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4765_DENOMINATOR_PARALLEL_PACK.csv"
QBARXH_PRODUCT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4765_QBARXH_PRODUCT_UPDATE.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4765_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4765_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4765_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4765_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4765_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4765_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4765_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4765_0_4764_decision", SOURCE_DIR / "P8_Y5_R2FR_4764_DECISION.csv", "MLOWER_PIM_DENOMINATOR_LEMMA_DERIVED", "4764 handoff decision"),
    ("SRC4765_1_4764_qedge", SOURCE_DIR / "P8_Y5_R2FR_4764_QEDGE_SHELL_SOURCE_ROW_READY.csv", "QE4764_1_bound_formula", "4764 Qedge shell row"),
    ("SRC4765_2_4764_denominator", SOURCE_DIR / "P8_Y5_R2FR_4764_DENOMINATOR_BOUND_PACK.csv", "DB4764_5_score_gate", "4764 denominator parallel pack"),
    ("SRC4765_3_4764_qbar", SOURCE_DIR / "P8_Y5_R2FR_4764_QBARXH_BOUND_UPDATE.csv", "QB4764_0_full_bound", "4764 QbarXH bound update"),
    ("SRC4765_4_4697_theorem", SOURCE_DIR / "P8_Y5_R2FR_4697_QEDGE_WORLDTUBE_BOUNDARY_THEOREM.csv", "QE4697_1_reynolds_shell_zero", "4697 Reynolds shell theorem"),
    ("SRC4765_5_4697_shell", SOURCE_DIR / "P8_Y5_R2FR_4697_QEDGE_REYNOLDS_SHELL_ROWS.csv", "QES4697_5_total", "4697 Qedge shell formula rows"),
    ("SRC4765_6_4697_boundary", SOURCE_DIR / "P8_Y5_R2FR_4697_QEDGE_BOUNDARY_FLUX_ROWS.csv", "QEB4697_6_total", "4697 boundary flux companion"),
    ("SRC4765_7_4588_reynolds", SOURCE_DIR / "P8_Y5_R2FR_4588_REYNOLDS_SUPPORT_THEOREM.csv", "RST4588_1_zero_trace_support", "4588 support zero theorem"),
    ("SRC4765_8_4588_clauses", SOURCE_DIR / "P8_Y5_R2FR_4588_REGULAR_SUPPORT_ZERO_CLAUSES.csv", "ZSR4588_2_zero_density_trace", "4588 zero clauses"),
    ("SRC4765_9_4587_density", SOURCE_DIR / "P8_Y5_R2FR_4587_DENSITY_QBASIC_THEOREM.csv", "DQT4587_1_qbasic_density_zero", "4587 density q-basic theorem"),
    ("SRC4765_10_4591_tau", SOURCE_DIR / "P8_Y5_R2FR_4591_TAU_EOBS_LOCK_THEOREM.csv", "TE4591_2_source_kernel_strict_zero", "4591 tau/eobs source lock"),
    ("SRC4765_11_4699_priority", SOURCE_DIR / "P8_Y5_R2FR_4699_FIRST_SOURCE_BACKED_PRIORITY_QUEUE.csv", "Q_edge_shell_abs", "4699 priority queue"),
    ("SRC4765_12_4699_rollup", SOURCE_DIR / "P8_Y5_R2FR_4699_QEDGE_ROLLUP_ROWS.csv", "EROLL4699_1_shell", "4699 Qedge rollup"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    ZERO_AUDIT_CSV,
    BOUND_PACK_CSV,
    DENOMINATOR_PARALLEL_CSV,
    QBARXH_PRODUCT_CSV,
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


def parse_csv(path_object: Path) -> bool:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


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


def zero_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "ZQ4765_0_object",
            "Q_edge_shell_abs",
            "Q_edge_shell is the Reynolds source-support edge contribution, not the full edge boundary flux.",
            "Q_edge_shell = int_partialW phi_edge W_lambda rho_H_tr V_n dSigma + <phi_edge W_lambda, mu_birth>",
            "DERIVED_OBJECT_SPLIT",
        ),
        (
            "ZQ4765_1_fixed_worldtube",
            "W_H",
            "W_H must be closure(supp J_H,total) selected before readout and descended through q.",
            "D_v W_H contributes only the Reynolds normal-velocity and birth-shell terms; no fitted residual mask is allowed.",
            "CONDITIONAL_PARENT_BRANCH_UNSIGNED",
        ),
        (
            "ZQ4765_2_density_descent",
            "rho_H dV_H",
            "If the matter plus EM Hilbert source functor is q-basic, then D_v(rho_H dV_H)=0 in the source bulk.",
            "This kills bulk source drift but does not by itself kill support-boundary trace or birth-shell terms.",
            "CONDITIONAL_FROM_4587",
        ),
        (
            "ZQ4765_3_zero_trace",
            "rho_H_trace_norm",
            "The boundary trace term is zero exactly when rho_H_tr is zero on partial W_H in the fixed q-basic collar.",
            "If rho_H_trace_norm=0, the term int_partialW phi_edge W_lambda rho_H_tr V_n dSigma vanishes for finite V_n.",
            "ZERO_INPUT_MISSING",
        ),
        (
            "ZQ4765_4_no_birth_shell",
            "mu_birth_TV",
            "The distributional birth/death term is zero exactly when no source layer is born or killed by the vertical probe.",
            "If mu_birth_TV=0, then <phi_edge W_lambda, mu_birth>=0 for bounded tests.",
            "ZERO_INPUT_MISSING",
        ),
        (
            "ZQ4765_5_bounded_tests",
            "Phi_edge and W_lambda_edge_max",
            "Finite test/kernel ceilings are sufficient for a bound and harmless under exact zero trace/no-shell.",
            "If Phi_edge and W_lambda_edge_max are finite, absolute value gives the shell bound.",
            "BOUND_SCHEMA_READY_VALUES_MISSING",
        ),
        (
            "ZQ4765_6_zero_theorem",
            "Q_edge_shell_abs=0",
            "If ZQ4765_1 through ZQ4765_5 are all parent-signed or source-backed, then Q_edge_shell_abs=0.",
            "This is a conditional theorem, not a live local-GR claim, because zero trace and no-birth inputs are unsigned.",
            "CONDITIONAL_ZERO_CERTIFICATE_DERIVED_NOT_CLAIMED",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": audit_id,
            "quantity": quantity,
            "clause": clause,
            "derivation_or_consequence": derivation,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, quantity, clause, derivation, status in specs
    ]


def bound_pack_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "QSB4765_0_worldtube",
            "W_H",
            "closure(supp J_H,total) in the same tau/e_obs branch before readout",
            "source/collar definition path; no fitted threshold mask",
            "MISSING_PARENT_SIGNED_WORLDTUBE",
        ),
        (
            "QSB4765_1_trace",
            "rho_H_trace_norm",
            "int_partialW |rho_H_tr| dSigma",
            "exact zero certificate or source-backed finite trace norm",
            "MISSING_ZERO_TRACE_CERTIFICATE_OR_VALUE",
        ),
        (
            "QSB4765_2_velocity",
            "V_n_bound",
            "sup_partialW |V_n| under the source-vertical probe",
            "fixed collar theorem or finite normal-support velocity bound",
            "MISSING_SUPPORT_VARIATION_BOUND",
        ),
        (
            "QSB4765_3_birth",
            "mu_birth_TV",
            "||mu_birth||_TV",
            "exact no-birth/no-death certificate or source-backed shell norm",
            "MISSING_NO_BIRTH_SHELL_CERTIFICATE_OR_VALUE",
        ),
        (
            "QSB4765_4_test",
            "Phi_edge",
            "sup_partialW |phi_edge|",
            "declared arena test ceiling with units/normalization",
            "MISSING_ARENA_TEST_BOUND",
        ),
        (
            "QSB4765_5_kernel",
            "W_lambda_edge_max",
            "sup_partialW |W_lambda|",
            "finite-range kernel ceiling on boundary collar",
            "MISSING_KERNEL_BOUND_VALUE",
        ),
        (
            "QSB4765_6_shell_total",
            "Q_edge_shell_abs",
            "Q_edge_shell_abs <= W_lambda_edge_max Phi_edge (rho_H_trace_norm V_n_bound + mu_birth_TV)",
            "all QSB4765 input rows exact-zero or source-backed",
            "FORMULA_READY_VALUES_MISSING",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "pack_id": pack_id,
            "quantity": quantity,
            "formula_or_definition": formula,
            "required_evidence": required,
            "current_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for pack_id, quantity, formula, required, status in specs
    ]


def denominator_parallel_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("DP4765_0_M0", "M_0", "baseline same-frame Hamiltonian/Hilbert denominator", "still required before any Qbar score"),
        ("DP4765_1_epsilon_abs", "epsilon_abs", "denominator drift ratio with epsilon_abs<1", "still required before division"),
        ("DP4765_2_PiM", "P_M_bound", "operator norm of fixed mass/source projector", "still required before numerator projection"),
        ("DP4765_3_Ecomm", "E_PiM_comm", "projector commutator zero or bound", "still required before score"),
        ("DP4765_4_parallel_verdict", "denominator_parallel_gate", "4765 can reduce Q_edge_shell but cannot replace denominator proof", "parallel nonclaim pack remains active"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "quantity": quantity,
            "role": role,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, role, status in specs
    ]


def qbar_product_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "QBU4765_0_shell_bound_insert",
            "|Q_edge_shell| <= W_lambda_edge_max Phi_edge (rho_H_trace_norm V_n_bound + mu_birth_TV)",
            "This is the concrete numerator insertion inherited by Qbar_XH.",
            "INSERT_READY_NONNUMERIC",
        ),
        (
            "QBU4765_1_edge_total",
            "|Q_edge| <= Q_edge_shell_abs + Q_edge_boundary_abs",
            "Killing the shell does not kill Hamiltonian/corner/reference/sidewall/radiative boundary flux.",
            "BOUNDARY_COMPANION_RETAINED",
        ),
        (
            "QBU4765_2_qbar_product",
            "|Qbar_XH| <= (P_M_bound(|Q_bulk|+Q_edge_shell_abs+Q_edge_boundary_abs+|Q_shadow|)+|E_PiM_comm|)/(M_0(1-epsilon_abs))",
            "This is now the honest local source-coupling envelope: numerator, projector and denominator all visible.",
            "PRODUCT_LAW_SHARPENED_NONCLAIM",
        ),
        (
            "QBU4765_3_zero_branch",
            "If rho_H_trace_norm=0 and mu_birth_TV=0, then Q_edge_shell_abs=0 in the same branch.",
            "This would remove one numerator term but still leave denominator, boundary and shadow gates.",
            "CONDITIONAL_ZERO_BRANCH",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": update_id,
            "formula_or_rule": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for update_id, formula, meaning, status in specs
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4765_0_zero_certificate", "prove exact Q_edge_shell_abs=0", "mathematically cleanest if trace and birth can be parent-signed", "ATTEMPTED_CONDITIONAL"),
        ("ROUTE4765_1_source_values", "source/collar trace-birth input pack", "next concrete fill row after zero proof stalls on unsigned trace/birth inputs", "SELECTED_NEXT"),
        ("ROUTE4765_2_denominator_pack", "M0 epsilon PiM Ecomm source-bound pack", "must proceed in parallel before any Qbar score", "PARALLEL_REQUIRED"),
        ("ROUTE4765_3_Poynting_wall", "Poynting wall/radiative flux row", "keeps the user's EM/Poynting hunch as an explicit boundary current, not a slogan", "SECONDARY_AFTER_TRACE_BIRTH"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "payoff": payoff,
            "selection_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, payoff, status in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PG4765_0_no_compact_shortcut", "Compact support alone does not imply Q_edge_shell_abs=0.", "requires zero trace plus no-birth certificate"),
        ("PG4765_1_same_branch", "All shell, denominator, projector and boundary rows must be in the same tau/e_obs/source branch.", "blocks branch mixing"),
        ("PG4765_2_no_boundary_erasure", "Q_edge_shell_abs=0 does not erase Q_edge_boundary_abs.", "blocks hiding Hamiltonian/Poynting boundary flux"),
        ("PG4765_3_no_score", "No local-GR, Newton, R10, PPN, WEP, clock, orbital or Maxwell score from this checkpoint.", "keeps result private/nonclaim"),
        ("PG4765_4_no_fitted_source", "W_H cannot be a threshold/readout residual mask or fitted local GM proxy.", "blocks circular source normalization"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "rule": rule,
            "enforced_effect": effect,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, rule, effect in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4765_0_no_zero_claim", "Do not claim Q_edge_shell_abs=0 until rho_H_trace_norm=0 and mu_birth_TV=0 are signed.", "NONCLAIM"),
        ("FW4765_1_no_full_edge_claim", "Do not equate shell zero with full Q_edge zero; boundary flux remains separate.", "NONCLAIM"),
        ("FW4765_2_no_Qbar_score", "Do not score QbarXH without denominator/projector and remaining numerator rows.", "NONCLAIM"),
        ("FW4765_3_poynting_visible", "Radiative/Poynting wall flux must be explicit if used, not hidden in source zero prose.", "SOURCE_DISCIPLINE"),
        ("FW4765_4_local_only", "No GitHub action from this checkpoint.", "LOCAL_ONLY"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, rule, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4765_0",
            "decision": DECISION,
            "summary": "4765 derives the exact conditional Qedge shell zero theorem from the Reynolds support identity. The zero route is not promoted because zero boundary trace and no birth/death shell are still unsigned. A source-ready bound pack is staged, and the denominator/projector pack remains parallel.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4765_0",
            "state": "completed_nonclaim",
            "meaning": "Qedge shell is no longer vague: it has an exact zero certificate and a source-bound formula, but the required trace/birth values are missing.",
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "The zero theorem reduced the missing content to trace/no-birth source-collar inputs, with Poynting wall flux retained as the next boundary/EM row.",
            "route_priority": "source_collar_trace_birth_inputs_then_Poynting_wall_flux_denominator_parallel",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| "
        + " | ".join(str(row[column]).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ") for column in columns)
        + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def write_docs(
    timestamp: str,
    zero_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    denominator_rows: list[dict[str, Any]],
    qbar_rows: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4765: Qedge Shell Zero Certificate or Denominator Source Bound Pack

Generated: `{timestamp}`

Marker: `{MARKER}`

## Result

4765 takes the selected numerator route seriously instead of just naming it.

- The Reynolds shell term is now explicit: `Q_edge_shell = int_partialW phi_edge W_lambda rho_H_tr V_n dSigma + <phi_edge W_lambda, mu_birth>`.
- Exact zero follows if the source worldtube is fixed/q-basic, the boundary trace vanishes, no birth/death shell appears, and the test/kernel ceilings are finite.
- The zero proof is conditional only: `rho_H_trace_norm=0` and `mu_birth_TV=0` are not parent-signed or source-backed yet.
- The fallback bound is now the next source pack: `Q_edge_shell_abs <= W_lambda_edge_max Phi_edge (rho_H_trace_norm V_n_bound + mu_birth_TV)`.
- Denominator/projector rows remain parallel blockers; shell zero alone cannot produce a local-GR or Newton claim.

## Zero Certificate Audit

{markdown_table(zero_rows, ["audit_id", "quantity", "clause", "status"])}

## Qedge Shell Bound Pack

{markdown_table(bound_rows, ["pack_id", "quantity", "formula_or_definition", "current_status"])}

## Denominator Parallel Pack

{markdown_table(denominator_rows, ["row_id", "quantity", "role", "status"])}

## QbarXH Product Update

{markdown_table(qbar_rows, ["update_id", "formula_or_rule", "status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "payoff", "selection_status"])}

## Promotion Gates

{markdown_table(gates, ["gate_id", "rule", "enforced_effect"])}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# PPC4161 4765: Qedge Shell Zero Certificate

Generated: `{timestamp}`

## Core Result

The Qedge shell term is the Reynolds support-boundary term:

```text
Q_edge_shell = int_partialW phi_edge W_lambda rho_H_tr V_n dSigma
               + <phi_edge W_lambda, mu_birth>.
```

Hence:

```text
Q_edge_shell_abs <= W_lambda_edge_max Phi_edge
                    (rho_H_trace_norm V_n_bound + mu_birth_TV).
```

Exact zero requires:

```text
rho_H_trace_norm = 0
mu_birth_TV = 0
finite Phi_edge and W_lambda_edge_max
same q-basic source collar and same tau/e_obs branch.
```

The updated product envelope is:

```text
|Qbar_XH| <= [P_M_bound(|Q_bulk| + Q_edge_shell_abs
              + Q_edge_boundary_abs + |Q_shadow|)
              + |E_PiM_comm|] / [M_0(1-epsilon_abs)].
```

Still nonclaim: zero trace, no-birth shell, denominator and projector values remain unsigned.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4765 derives the conditional Qedge shell zero certificate from the Reynolds support identity.
- `Q_edge_shell_abs=0` is exact if `rho_H_trace_norm=0` and `mu_birth_TV=0` in the same fixed q-basic source collar.
- The fallback source-bound formula is `Q_edge_shell_abs <= W_lambda_edge_max Phi_edge (rho_H_trace_norm V_n_bound + mu_birth_TV)`.
- The shell route remains nonclaim because trace/no-birth certificates and denominator/projector rows are missing.
- Poynting/radiative wall flux is preserved as an explicit boundary row, not hidden inside shell zero.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4765 packet update: Qedge shell has an exact conditional zero theorem and a source-bound pack. Next fill `rho_H_trace_norm`, `mu_birth_TV`, `V_n_bound`, `Phi_edge`, `W_lambda_edge_max`, while keeping denominator/projector rows parallel and Poynting wall flux explicit.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4765-Y5-R2FR-Qedge-shell-zero-certificate-or-denominator-source-bound-pack.md`

## Decision

`{DECISION}`

## What moved forward

- Derived the exact conditional Qedge shell zero certificate from the Reynolds support identity.
- Reduced the shell problem to `rho_H_trace_norm=0` plus `mu_birth_TV=0`, with finite test/kernel ceilings.
- Staged a source-ready bound pack for `Q_edge_shell_abs`.
- Kept denominator/projector and full boundary/Poynting rows open rather than hiding them.

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
        "local_gr_qedge_shell_zero_certificate",
        "4765 derives the conditional Qedge shell zero certificate and stages source-bound rows for trace, birth, velocity, test and kernel inputs.",
        "Generated source register, zero certificate audit, Qedge shell bound pack, denominator parallel pack, QbarXH product update, route matrix, gates, firewalls, decision, status, next target and validation.",
        "Qedge_shell_zero_certificate_conditional_trace_birth_values_missing_nonclaim",
        NEXT_TARGET,
        "Claiming compact support or shell zero without zero-trace/no-birth evidence, or erasing Poynting/boundary flux.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need source-collar trace/birth input values or exact certificates, while denominator/projector remains parallel.",
        "Qedge shell zero certificate or denominator source bound pack",
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
    zero_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    denominator_rows: list[dict[str, Any]],
    qbar_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4765_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4765_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4765_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4765_2_zero_audit", "zero audit has derived theorem but missing trace/birth inputs", any(row["status"] == "CONDITIONAL_ZERO_CERTIFICATE_DERIVED_NOT_CLAIMED" for row in zero_rows) and any(row["quantity"] == "rho_H_trace_norm" and "MISSING" in row["status"] for row in zero_rows) and any(row["quantity"] == "mu_birth_TV" and "MISSING" in row["status"] for row in zero_rows), str(ZERO_AUDIT_CSV)))
    checks.append(("VAL4765_3_bound_pack", "bound pack contains Qedge formula and all rows nonclaim", any(row["quantity"] == "Q_edge_shell_abs" and "W_lambda_edge_max" in row["formula_or_definition"] for row in bound_rows) and all(row["valid_for_claim"] is False for row in bound_rows), str(BOUND_PACK_CSV)))
    checks.append(("VAL4765_4_denominator_parallel", "denominator pack remains parallel blocker", any(row["quantity"] == "denominator_parallel_gate" for row in denominator_rows) and all(row["valid_for_claim"] is False for row in denominator_rows), str(DENOMINATOR_PARALLEL_CSV)))
    checks.append(("VAL4765_5_qbar_product", "Qbar product includes shell boundary denominator and nonclaim", any("Q_edge_boundary_abs" in row["formula_or_rule"] and "M_0(1-epsilon_abs)" in row["formula_or_rule"] for row in qbar_rows) and all(row["valid_for_claim"] is False for row in qbar_rows), str(QBARXH_PRODUCT_CSV)))
    checks.append(("VAL4765_6_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4765_7_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4765_8_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4765_9_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4765_10_claim_row", "claim row L-607 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4765_11_resume", "resume points from 4765 to 4766", "4765-Y5" in resume_text and "4766-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4765_12_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
    overall = all(passed for _, _, passed, _ in checks)
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
            "validation_id": "VAL4765_OVERALL",
            "check": "all 4765 Qedge shell zero/bound checks pass",
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
    zero_rows = zero_audit_rows(timestamp)
    bound_rows = bound_pack_rows(timestamp)
    denominator_rows = denominator_parallel_rows(timestamp)
    qbar_rows = qbar_product_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(ZERO_AUDIT_CSV, zero_rows)
    write_csv(BOUND_PACK_CSV, bound_rows)
    write_csv(DENOMINATOR_PARALLEL_CSV, denominator_rows)
    write_csv(QBARXH_PRODUCT_CSV, qbar_rows)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, zero_rows, bound_rows, denominator_rows, qbar_rows, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, zero_rows, bound_rows, denominator_rows, qbar_rows, gates, timestamp))


if __name__ == "__main__":
    main()

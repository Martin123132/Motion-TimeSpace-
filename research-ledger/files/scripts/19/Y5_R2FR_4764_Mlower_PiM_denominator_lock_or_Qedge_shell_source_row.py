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

CHECKPOINT = "4764"
CLAIM_ID = "L-606"
MARKER = "PPC4161_MLOWER_PIM_DENOMINATOR_LOCK_OR_QEDGE_SHELL_SOURCE_ROW_4764"
PACKET_MARKER = "PPC4161_PACKET_MLOWER_PIM_DENOMINATOR_LOCK_OR_QEDGE_SHELL_SOURCE_ROW_4764"
DECISION = "MLOWER_PIM_DENOMINATOR_LEMMA_DERIVED_CONDITIONAL_SOURCE_VALUES_MISSING_QEDGE_SHELL_ROW_READY_NONCLAIM"
NEXT_TARGET = "4765-Y5-R2FR-Qedge-shell-zero-certificate-or-denominator-source-bound-pack.md"

DOC_PATH = POST / "4764-Y5-R2FR-Mlower-PiM-denominator-lock-or-Qedge-shell-source-row.md"
FORMAL_PATH = FORMAL / "780-PPC4161-Mlower-PiM-denominator-lock-or-Qedge-shell-source-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4764_SOURCE_REGISTER.csv"
DENOMINATOR_LEMMA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4764_MLOWER_PIM_DENOMINATOR_LEMMA.csv"
DENOMINATOR_BOUND_PACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4764_DENOMINATOR_BOUND_PACK.csv"
QEDGE_SOURCE_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4764_QEDGE_SHELL_SOURCE_ROW_READY.csv"
QBARXH_BOUND_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4764_QBARXH_BOUND_UPDATE.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4764_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4764_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4764_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4764_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4764_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4764_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4764_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4764_0_4763_decision", SOURCE_DIR / "P8_Y5_R2FR_4763_DECISION.csv", "QBARXH_NUMERATOR_FIRST_FILL_SELECTS_QEDGE_SHELL", "4763 handoff"),
    ("SRC4764_1_4763_denominator", SOURCE_DIR / "P8_Y5_R2FR_4763_DENOMINATOR_PROJECTOR_GATE.csv", "DG4763_0_Mlower", "4763 denominator gate"),
    ("SRC4764_2_4763_qedge", SOURCE_DIR / "P8_Y5_R2FR_4763_QEDGE_SHELL_SOURCE_ROW_CONTRACT.csv", "QE4763_7_total", "4763 Qedge shell contract"),
    ("SRC4764_3_4604_mhref_theorem", SOURCE_DIR / "P8_Y5_R2FR_4604_MHREF_DENOMINATOR_THEOREM.csv", "MHR4604_2_inverse_denominator_lock", "4604 inverse denominator lock"),
    ("SRC4764_4_4604_mhref_inputs", SOURCE_DIR / "P8_Y5_R2FR_4604_MHREF_DENOMINATOR_INPUT_ROWS.csv", "MD4604_2_M_lower", "4604 Mlower input row"),
    ("SRC4764_5_4604_pim_theorem", SOURCE_DIR / "P8_Y5_R2FR_4604_PIM_PROJECTOR_THEOREM.csv", "PIM4604_2_projector_commutator_bound", "4604 PiM theorem"),
    ("SRC4764_6_4604_pim_inputs", SOURCE_DIR / "P8_Y5_R2FR_4604_PIM_PROJECTOR_INPUT_ROWS.csv", "PM4604_1_operator_norm", "4604 PiM input rows"),
    ("SRC4764_7_2665_gate", SOURCE_DIR / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_PROJECTOR_DENOMINATOR_GATE.csv", "PDG2665_7_verdict", "2665 projector denominator gate"),
    ("SRC4764_8_2665_contract", SOURCE_DIR / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv", "HLOCK2665_7_verdict", "2665 lock contract"),
    ("SRC4764_9_4589_mhref", SOURCE_DIR / "P8_Y5_R2FR_4589_MHREF_QBASIC_THEOREM.csv", "MHR4589_3_positive_denominator_guard", "4589 positive denominator guard"),
    ("SRC4764_10_4589_drift", SOURCE_DIR / "P8_Y5_R2FR_4589_DENOMINATOR_DRIFT_BOUND_ROWS.csv", "MDB4589_3_Mlower", "4589 denominator drift rows"),
    ("SRC4764_11_4590_mask", SOURCE_DIR / "P8_Y5_R2FR_4590_READOUT_MASK_THEOREM.csv", "ROM4590_2_operator_norm_fallback", "4590 mask fallback"),
    ("SRC4764_12_4591_tau", SOURCE_DIR / "P8_Y5_R2FR_4591_TAU_EOBS_LOCK_THEOREM.csv", "TE4591_2_source_kernel_strict_zero", "4591 strict source-kernel chain"),
    ("SRC4764_13_4697_qedge", SOURCE_DIR / "P8_Y5_R2FR_4697_QEDGE_REYNOLDS_SHELL_ROWS.csv", "QES4697_5_total", "4697 Qedge shell source row"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    DENOMINATOR_LEMMA_CSV,
    DENOMINATOR_BOUND_PACK_CSV,
    QEDGE_SOURCE_ROW_CSV,
    QBARXH_BOUND_UPDATE_CSV,
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


def denominator_lemma_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("DL4764_0_definition", "M_H_ref=H_tau[S_outer;tau_*,e_*]-H_ref[Sigma_ref;tau_*,e_*]", "same-frame Hamiltonian/reference denominator, not fitted GM", "DEFINITION_DERIVED_CONDITIONAL"),
        ("DL4764_1_qbasic_zero", "If H_tau,H_ref,tau_*,e_*,surfaces,reference descend through q, then D_v M_H_ref=0.", "strict branch denominator drift zero", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED"),
        ("DL4764_2_inverse_lock", "If M_H_ref=M_0+deltaM, M_0>0, |deltaM|<=epsilon_abs M_0, epsilon_abs<1, then M_lower=M_0(1-epsilon_abs)>0.", "this is the legal division lemma for Qbar_XH", "DERIVED_DENOMINATOR_LEMMA"),
        ("DL4764_3_projector_lock", "If Pi_M fixed-list is q-basic and selected before readout, [D_v,Pi_M]Q_tot=0.", "projector cannot move with source mask/readout", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED"),
        ("DL4764_4_projector_bound", "|Pi_M Q_tot| <= P_M_bound(|Q_bulk|+|Q_edge|+|Q_shadow|)+|E_PiM_comm|", "finite fallback when projector lock is unsigned", "BOUND_FORM_DERIVED_VALUES_MISSING"),
        ("DL4764_5_current_verdict", "M_lower/Pi_M lock remains nonclaim because M_0, epsilon_abs, P_M_bound and E_PiM_comm are not source-backed.", "do not score Qbar_XH yet", "CLAIM_BLOCKED_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "lemma_id": lemma_id,
            "statement_or_formula": statement,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for lemma_id, statement, meaning, status in specs
    ]


def denominator_bound_pack_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("DB4764_0_M0", "M_0", "baseline same-frame Hamiltonian/Hilbert denominator", "H_tau[S_outer]; H_ref; tau_*; e_*; surface family; units", "MISSING_SOURCE_BACKED_BASELINE_DENOMINATOR"),
        ("DB4764_1_epsilon_abs", "epsilon_abs", "(|D_vH_tau|+|D_vH_ref|+|E_symp|+|E_ref|+|E_frame|+|E_mask|)/M_0", "drift components and M_0", "MISSING_DENOMINATOR_DRIFT_COMPONENT_VALUES"),
        ("DB4764_2_Mlower", "M_lower", "M_0(1-epsilon_abs)", "M_0>0, 0<=epsilon_abs<1, same-frame units", "MISSING_POSITIVE_LOWER_BOUND"),
        ("DB4764_3_PiM_norm", "P_M_bound=||Pi_M^H||", "operator norm of fixed mass/source projector", "source vector norm, projector definition, units ledger", "MISSING_PROJECTOR_OPERATOR_NORM"),
        ("DB4764_4_Ecomm", "E_PiM_comm", "bound for [D_v,Pi_M]Q_tot or [d,Pi_M]J_H", "commutator theorem-zero or numeric residual", "MISSING_PROJECTOR_COMMUTATOR_ZERO_OR_BOUND"),
        ("DB4764_5_score_gate", "Qbar_denominator_gate", "score-ready iff M_lower>0, P_M_bound finite, E_PiM_comm zero/bounded, source paths exist", "all DB4764 rows", "CLAIM_BLOCKED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "pack_id": pack_id,
            "quantity": quantity,
            "formula_or_role": formula,
            "required_inputs": inputs,
            "current_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for pack_id, quantity, formula, inputs, status in specs
    ]


def qedge_source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("QE4764_0_zero_certificate", "Q_edge_shell_abs=0", "rho_H_trace_norm=0 and mu_birth_TV=0 in fixed q-basic collar", "ZERO_CERTIFICATE_TARGET"),
        ("QE4764_1_bound_formula", "Q_edge_shell_abs", "Q_edge_shell_abs <= W_lambda_edge_max Phi_edge (rho_H_trace_norm V_n_bound + mu_birth_TV)", "BOUND_FORMULA_READY"),
        ("QE4764_2_trace", "rho_H_trace_norm", "int_partialW |rho_H^tr| dSigma; zero trace certificate or finite trace norm", "SOURCE_VALUE_REQUIRED"),
        ("QE4764_3_velocity", "V_n_bound", "sup_partialW |V_n| under source-vertical probe; fixed boundary gives no contribution if trace also zero", "SOURCE_VALUE_REQUIRED"),
        ("QE4764_4_birth", "mu_birth_TV", "total variation norm of distributional birth/death shell", "SOURCE_VALUE_REQUIRED"),
        ("QE4764_5_kernel_test", "Phi_edge,W_lambda_edge_max", "arena test ceiling and finite-range kernel ceiling on boundary collar", "SOURCE_VALUE_REQUIRED"),
        ("QE4764_6_claim_gate", "valid_for_claim", "true only if all fields are exact-zero or source-backed with units and no MISSING markers", "FALSE_NOW"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "quantity": quantity,
            "formula_or_requirement": formula,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, formula, status in specs
    ]


def qbarxh_update_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("QB4764_0_full_bound", "|Qbar_XH| <= (P_M_bound(|Q_bulk|+|Q_edge|+|Q_shadow|)+|E_PiM_comm|)/[M_0(1-epsilon_abs)]", "legal only when M_0>0 and epsilon_abs<1", "UPDATED_BOUND_LAW"),
        ("QB4764_1_edge_insert", "Q_edge_abs <= Q_edge_shell_abs+Q_edge_boundary_abs", "Qedge shell row can reduce numerator but not denominator gate", "NUMERATOR_INSERT_READY"),
        ("QB4764_2_zero_branch", "Q_edge_shell_abs=0 if rho_H_trace_norm=0 and mu_birth_TV=0", "cleanest source-worldtube zero route", "EXACT_IF_CERTIFIED"),
        ("QB4764_3_nonclaim", "Qbar_XH score remains blocked by missing M_lower/PiM and other numerator components", "prevents premature local test scoring", "CLAIM_BLOCKED"),
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
        ("ROUTE4764_0_denominator_lock", "parent-sign or source M_lower/PiM gate", "highest anti-cheat priority; attempted but values missing", "ATTEMPTED_CONDITIONAL"),
        ("ROUTE4764_1_Qedge_shell_zero", "prove Qedge shell zero by trace/no-birth certificate", "cleanest numerator progress and next target", "SELECTED_NEXT"),
        ("ROUTE4764_2_denominator_source_pack", "fill M0/epsilon/PiM/Ecomm source pack", "parallel source-bound fallback", "PARALLEL_FALLBACK"),
        ("ROUTE4764_3_Poynting_wall", "fill Poynting wall flux row", "kept as real EM source route after shell/denominator", "DEFERRED_SECONDARY"),
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
        ("PG4764_0_positive_denominator", "No Qbar division unless M_0>0 and epsilon_abs<1 produce M_lower>0.", "blocks symbolic denominator"),
        ("PG4764_1_projector_fixed", "Pi_M must be fixed before readout or carry E_PiM_comm.", "blocks moving projector"),
        ("PG4764_2_no_fitted_GM", "M_H_ref cannot be orbital GM or fitted acceleration mass.", "blocks circular normalization"),
        ("PG4764_3_no_edge_slogan", "Compact support is not Qedge shell zero without trace/no-birth certificate.", "blocks compact-source shortcut"),
        ("PG4764_4_no_score", "No local arena score until denominator, projector, numerator, qbarXT, Z/range and tau rows are ready.", "blocks premature scoring"),
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
        ("FW4764_0_no_denominator_claim", "Do not claim M_lower/PiM is sourced or parent-signed.", "NONCLAIM"),
        ("FW4764_1_no_qedge_claim", "Do not claim Qedge shell zero without trace/no-birth certificate.", "NONCLAIM"),
        ("FW4764_2_no_Qbar_score", "Do not score QbarXH or R10/PPN from this checkpoint.", "NONCLAIM"),
        ("FW4764_3_local_only", "No GitHub action from this checkpoint.", "LOCAL_ONLY"),
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
            "decision_id": "DEC4764_0",
            "decision": DECISION,
            "summary": "4764 derives the exact Mlower/PiM denominator lemma and updates QbarXH to divide by M0(1-epsilon_abs). The lemma is not claim-ready because M0, epsilon_abs, PiM norm and commutator rows are missing. Qedge shell is staged as the cleanest next zero/bound row.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4764_0",
            "state": "completed_nonclaim",
            "meaning": "The denominator is now a precise positivity/projector lemma, and Qedge shell is the selected source row for the next derivation/fill pass.",
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "The denominator lemma is exact but value-missing; the best next move is Qedge shell zero certificate or denominator source-bound pack.",
            "route_priority": "Qedge_shell_zero_certificate_parallel_denominator_source_pack",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row[column]).replace("\n", " ") for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def write_docs(
    timestamp: str,
    lemma_rows: list[dict[str, Any]],
    bound_pack: list[dict[str, Any]],
    qedge_rows: list[dict[str, Any]],
    qbar_rows: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4764: Mlower/PiM Denominator Lock or Qedge Shell Source Row

Generated: `{timestamp}`

Marker: `{MARKER}`

## Result

4764 sharpens the denominator/projector gate into an actual lemma.

- If `M_H_ref=M_0+deltaM`, `M_0>0`, `|deltaM|<=epsilon_abs M_0` and `epsilon_abs<1`, then `M_lower=M_0(1-epsilon_abs)>0`.
- Therefore the source-side bound becomes `|Qbar_XH| <= (P_M_bound(|Q_bulk|+|Q_edge|+|Q_shadow|)+|E_PiM_comm|)/[M_0(1-epsilon_abs)]`.
- This is real progress, but not a claim: `M_0`, `epsilon_abs`, `P_M_bound` and `E_PiM_comm` are not source-backed or parent-signed.
- The cleanest next numerator route is `Q_edge_shell_abs=0` via zero trace plus no birth/death shell, or a source-backed shell bound.
- No local-GR, Newton, R10, PPN, WEP, clock, orbital or Maxwell pass is claimed.

## Denominator Lemma

{markdown_table(lemma_rows, ["lemma_id", "statement_or_formula", "status"])}

## Denominator Bound Pack

{markdown_table(bound_pack, ["pack_id", "quantity", "formula_or_role", "current_status"])}

## Qedge Shell Row

{markdown_table(qedge_rows, ["row_id", "quantity", "formula_or_requirement", "status"])}

## QbarXH Bound Update

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

    formal = f"""# PPC4161 4764: Mlower/PiM Denominator Lemma

Generated: `{timestamp}`

## Core Result

The denominator gate is now:

```text
M_H_ref = M_0 + deltaM
M_0 > 0
|deltaM| <= epsilon_abs M_0
epsilon_abs < 1
=> M_lower = M_0(1-epsilon_abs) > 0.
```

The Qbar bound becomes:

```text
|Qbar_XH| <= [P_M_bound(|Q_bulk|+|Q_edge|+|Q_shadow|)
              + |E_PiM_comm|] / [M_0(1-epsilon_abs)].
```

Still nonclaim: `M_0`, `epsilon_abs`, `P_M_bound` and `E_PiM_comm` are not filled.

Next selected numerator route:

```text
Q_edge_shell_abs <= W_lambda_edge_max Phi_edge
                    (rho_H_trace_norm V_n_bound + mu_birth_TV).
```

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4764 derives the denominator positivity lemma `M_lower=M_0(1-epsilon_abs)>0` under `M_0>0`, `epsilon_abs<1`.
- It updates the Qbar bound to divide by `M_0(1-epsilon_abs)` and retain `P_M_bound` plus `E_PiM_comm`.
- The lock is not claim-ready because `M_0`, `epsilon_abs`, `P_M_bound` and `E_PiM_comm` are missing source-backed or parent-signed values.
- The next concrete source row is `Q_edge_shell_abs`, with zero route `rho_H_trace_norm=0` and `mu_birth_TV=0`.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4764 packet update: denominator is no longer vague. Use `M_0(1-epsilon_abs)` and `P_M_bound/E_PiM_comm`. Next, try the Qedge shell zero certificate or fill the denominator source-bound pack.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4764-Y5-R2FR-Mlower-PiM-denominator-lock-or-Qedge-shell-source-row.md`

## Decision

`{DECISION}`

## What moved forward

- Derived the precise denominator lemma `M_lower=M_0(1-epsilon_abs)>0`.
- Updated the `Qbar_XH_abs` bound with `P_M_bound` and `E_PiM_comm`.
- Kept the denominator/projector gate nonclaim because required source values are missing.
- Selected `Q_edge_shell_abs` zero certificate or bound row as the next concrete move.

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
        "local_gr_denominator_projector_gate",
        "4764 derives the Mlower/PiM denominator lemma and stages Qedge shell as the next source row.",
        "Generated source register, denominator lemma, denominator bound pack, Qedge source row, Qbar bound update, route matrix, gates, firewalls, decision, status, next target and validation.",
        "Mlower_PiM_denominator_lemma_Qedge_shell_nonclaim",
        NEXT_TARGET,
        "Dividing by symbolic MHref or claiming Qedge shell zero without trace/no-birth certificate.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need Qedge shell zero certificate or denominator source-bound pack.",
        "Mlower/PiM denominator lock or Qedge shell source row",
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
    lemma_rows: list[dict[str, Any]],
    bound_pack: list[dict[str, Any]],
    qedge_rows: list[dict[str, Any]],
    qbar_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4764_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4764_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4764_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4764_2_lemma", "denominator lemma includes M0 epsilon Mlower and claim block", any("M_lower=M_0(1-epsilon_abs)>0" in row["statement_or_formula"] for row in lemma_rows) and any(row["status"] == "CLAIM_BLOCKED_VALUES_MISSING" for row in lemma_rows), str(DENOMINATOR_LEMMA_CSV)))
    checks.append(("VAL4764_3_bound_pack", "bound pack keeps Mlower PiM commutator missing", any(row["quantity"] == "M_lower" and "MISSING" in row["current_status"] for row in bound_pack) and any(row["quantity"] == "E_PiM_comm" and "MISSING" in row["current_status"] for row in bound_pack), str(DENOMINATOR_BOUND_PACK_CSV)))
    checks.append(("VAL4764_4_qedge", "Qedge row includes zero certificate and bound formula", any(row["quantity"] == "Q_edge_shell_abs=0" for row in qedge_rows) and any("W_lambda_edge_max" in row["formula_or_requirement"] for row in qedge_rows), str(QEDGE_SOURCE_ROW_CSV)))
    checks.append(("VAL4764_5_qbar_update", "Qbar update uses M0 denominator and remains blocked", any("M_0(1-epsilon_abs)" in row["formula_or_rule"] for row in qbar_rows) and any(row["status"] == "CLAIM_BLOCKED" for row in qbar_rows), str(QBARXH_BOUND_UPDATE_CSV)))
    checks.append(("VAL4764_6_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4764_7_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4764_8_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4764_9_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4764_10_claim_row", "claim row L-606 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4764_11_resume", "resume points from 4764 to 4765", "4764-Y5" in resume_text and "4765-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4764_12_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
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
            "validation_id": "VAL4764_OVERALL",
            "check": "all 4764 denominator/Qedge checks pass",
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
    lemma_rows = denominator_lemma_rows(timestamp)
    bound_pack = denominator_bound_pack_rows(timestamp)
    qedge_rows = qedge_source_rows(timestamp)
    qbar_rows = qbarxh_update_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(DENOMINATOR_LEMMA_CSV, lemma_rows)
    write_csv(DENOMINATOR_BOUND_PACK_CSV, bound_pack)
    write_csv(QEDGE_SOURCE_ROW_CSV, qedge_rows)
    write_csv(QBARXH_BOUND_UPDATE_CSV, qbar_rows)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, lemma_rows, bound_pack, qedge_rows, qbar_rows, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, lemma_rows, bound_pack, qedge_rows, qbar_rows, gates, timestamp))


if __name__ == "__main__":
    main()

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
RUNS = FORMAL / "runs"
FORMAL_SCRIPTS = FORMAL / "scripts"

CHECKPOINT = "4736"
CLAIM_ID = "L-578"
MARKER = "PPC4161_GK_PARENT_OWNER_OR_TRANSITION_SHELL_VLCG_BOUND_4736"
PACKET_MARKER = "PPC4161_PACKET_GK_PARENT_OWNER_OR_TRANSITION_SHELL_VLCG_BOUND_4736"
DECISION = "GK_QBASIC_OWNER_EXACT_CONDITIONAL_UNSIGNED_TRANSITION_SHELL_BOUND_FORCES_CURRENT_OR_KHAT_IDENTITY_NONCLAIM"
NEXT_TARGET = "4737-Y5-R2FR-transition-shell-current-solver-or-Khat-cancellation-identity.md"

DOC_PATH = POST / "4736-Y5-R2FR-GK-parent-owner-or-transition-shell-VLcg-bound.md"
FORMAL_PATH = FORMAL / "752-PPC4161-GK-parent-owner-or-transition-shell-VLcg-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_MODEL_SUMMARY = RUNS / "source_model_curvature_Lcg_20260527-211932" / "summary.csv"
TRACE_BOUND_SUMMARY = RUNS / "Lcg_gradient_trace_bound_20260527-214036" / "summary.csv"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4736_SOURCE_REGISTER.csv"
GK_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4736_GK_PARENT_OWNER_THEOREM.csv"
KB_OWNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4736_KB_OWNER_AUDIT.csv"
GK_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4736_GK_VERTICAL_DERIVATIVE_BOUND.csv"
TRANSITION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4736_TRANSITION_SHELL_NUMERIC_BOUND.csv"
PROPAGATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4736_PROPAGATION_TO_VLCG_JM.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4736_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4736_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4736_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4736_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4736_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4736_VALIDATION.csv"

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    GK_THEOREM_CSV,
    KB_OWNER_CSV,
    GK_BOUND_CSV,
    TRANSITION_CSV,
    PROPAGATION_CSV,
    GATES_CSV,
    FIREWALL_CSV,
    DECISION_CSV,
    STATUS_CSV,
    NEXT_TARGET_CSV,
]

SOURCE_SPECS = [
    ("SRC4736_0_4735_next", SOURCE_DIR / "P8_Y5_R2FR_4735_NEXT_TARGET.csv", "G_K and transition support are the active local blockers", "4735 selected G_K/transition as next blocker"),
    ("SRC4736_1_4735_gk", SOURCE_DIR / "P8_Y5_R2FR_4735_GK_SOURCE_SUBBUDGET.csv", "V_GK <= V_KB_grad", "4735 G_K subbudget"),
    ("SRC4736_2_89_GK", FORMAL / "89-source-model-curvature-Lcg-test.md", "G_K = |d ln K_B / dr|", "source-model G_K definition"),
    ("SRC4736_3_89_trace_proxy", FORMAL / "89-source-model-curvature-Lcg-test.md", "trace_gradient_proxy", "source-model trace proxy"),
    ("SRC4736_4_90_dry_bound", FORMAL / "90-Lcg-gradient-trace-bound.md", "S_PPN ~ |q| R L_cg^2 / u", "dry PPN proxy"),
    ("SRC4736_5_90_transition", FORMAL / "90-Lcg-gradient-trace-bound.md", "U_B is O(1) at the transition", "transition shell warning"),
    ("SRC4736_6_91_transition", FORMAL / "91-trace-suppression-closure-gate.md", "U_B^2 does not suppress the transition shell enough", "trace closure transition failure"),
    ("SRC4736_7_source_script_kb", FORMAL_SCRIPTS / "source_model_curvature_Lcg_test.py", "return params.w_c * point.c_abs", "K_B source-model constructor"),
    ("SRC4736_8_trace_script_q", FORMAL_SCRIPTS / "Lcg_gradient_trace_bound.py", "q_trace = f_effective * (n_t * dlnu + 2.0 * d_ln_lcg) / (l_cg * l_cg)", "q_trace dry-bound formula"),
    ("SRC4736_9_source_summary_transition", SOURCE_MODEL_SUMMARY, "solar_transition_shell_point_mass", "numeric transition source row"),
    ("SRC4736_10_trace_summary_transition", TRACE_BOUND_SUMMARY, "solar_transition_U_power_quarantine", "numeric transition trace row"),
    ("SRC4736_11_trace_summary_solver", TRACE_BOUND_SUMMARY, "transition_shell_current_PPN_solver", "open solver requirement"),
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


def source_register(timestamp: str) -> list[dict[str, Any]]:
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
                "timestamp_utc": timestamp,
            }
        )
    return rows


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def find_row(path: Path, column: str, value: str) -> dict[str, str]:
    for row in load_csv_rows(path):
        if row.get(column) == value:
            return row
    raise ValueError(f"missing row {column}={value} in {path}")


def numeric_value(row: dict[str, str], column: str) -> float | None:
    value = row.get(column, "")
    if value == "":
        return None
    return float(value)


def safe_ratio(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator in (None, 0.0):
        return None
    return numerator / denominator


def gk_theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "GK4736_0_covariant_definition",
            "Let Y_a=P_a^b nabla_b ln K_B and G_K=(h^{ab}Y_aY_b)^(1/2); the radial source-model expression is the 1D proxy.",
            "definition",
            "closed_symbolically",
            "SRC4736_2_89_GK",
            True,
        ),
        (
            "GK4736_1_exact_conditional_zero",
            "If K_B, P_a^b, h^{ab}, support, boundary and readout all descend through q, then D_v G_K=0 away from G_K=0.",
            "sufficient q-basic theorem",
            "exact_conditional_only",
            "SRC4736_1_4735_gk",
            True,
        ),
        (
            "GK4736_2_zero_set_caveat",
            "At G_K=0 the norm derivative is singular unless a regularized norm or separate homogeneous branch is used; FLRW uses the Hubble-cap branch.",
            "regularity caveat",
            "requires_branch_handling",
            "SRC4736_2_89_GK",
            False,
        ),
        (
            "GK4736_3_scalar_owner_not_enough",
            "K_B q-basic alone is insufficient because D_v G_K can still receive projector, connection, support and boundary/readout terms.",
            "anti-overclaim theorem",
            "blocks_promotion",
            "SRC4736_1_4735_gk",
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
            "timestamp_utc": timestamp,
        }
        for theorem_id, statement, role, status, source_id, valid_for_claim in specs
    ]


def kb_owner_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "KB4736_0_constructor",
            "K_B = w_C C_abs + w_R R_abs + eta_H H_bg^2/c^2",
            "source-model constructor",
            "source_model_only",
            "SRC4736_7_source_script_kb",
            False,
        ),
        (
            "KB4736_1_exact_qbasic_condition",
            "D_v K_B=0 if C_abs, R_abs, H_bg and all weights descend/fix under q.",
            "scalar owner condition",
            "exact_conditional_only",
            "SRC4736_7_source_script_kb",
            True,
        ),
        (
            "KB4736_2_weight_firewall",
            "w_C, w_R and eta_H cannot be chosen by sector or local test arena.",
            "anti-retuning guard",
            "closed_to_sector_tuning",
            "SRC4736_7_source_script_kb",
            False,
        ),
        (
            "KB4736_3_floor_owner",
            "H_bg floor must be background q-basic on the local branch; otherwise V_LH feeds V_Lcg.",
            "Hubble cap owner",
            "unsigned",
            "SRC4736_0_4735_next",
            False,
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "owner_id": owner_id,
            "statement": statement,
            "role": role,
            "status": status,
            "source_id": source_id,
            "source_path": source_path(source_id),
            "valid_for_claim": valid_for_claim,
            "timestamp_utc": timestamp,
        }
        for owner_id, statement, role, status, source_id, valid_for_claim in specs
    ]


def gk_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "VGTK4736_0_definition",
            "V_GK := sup_local |D_v ln G_K| on the nonzero-gradient branch.",
            "dimensionless",
            "definition",
            "SRC4736_1_4735_gk",
            False,
        ),
        (
            "VGTK4736_1_parent_bound",
            "V_GK <= V_KB_grad + V_projector + V_metric + V_connection + V_support + V_boundary + V_readout.",
            "dimensionless",
            "sourceable fallback bound",
            "SRC4736_1_4735_gk",
            False,
        ),
        (
            "VGTK4736_2_KB_grad",
            "V_KB_grad covers P nabla(D_v ln K_B), K_B zero/floor sensitivity and gradient-commutator terms.",
            "dimensionless",
            "unsigned",
            "SRC4736_2_89_GK",
            False,
        ),
        (
            "VGTK4736_3_projector_connection",
            "V_projector+V_metric+V_connection vanish only if the local spatial projector/connection descend through q.",
            "dimensionless",
            "unsigned",
            "SRC4736_1_4735_gk",
            False,
        ),
        (
            "VGTK4736_4_support_boundary",
            "V_support+V_boundary covers transition-shell support motion and integration/readout boundary terms.",
            "dimensionless",
            "active_transition_blocker",
            "SRC4736_5_90_transition",
            False,
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": bound_id,
            "expression": expression,
            "units": units,
            "status": status,
            "source_id": source_id,
            "source_path": source_path(source_id),
            "valid_for_claim": valid_for_claim,
            "timestamp_utc": timestamp,
        }
        for bound_id, expression, units, status, source_id, valid_for_claim in specs
    ]


def transition_numeric_rows(timestamp: str) -> list[dict[str, Any]]:
    source_transition = find_row(SOURCE_MODEL_SUMMARY, "case", "solar_transition_shell_point_mass")
    trace_constant = find_row(TRACE_BOUND_SUMMARY, "case", "solar_transition_constant_FL_quarantine")
    trace_u_power = find_row(TRACE_BOUND_SUMMARY, "case", "solar_transition_U_power_quarantine")

    trace_proxy = numeric_value(source_transition, "trace_gradient_proxy")
    vlcg_radial_proxy = None if trace_proxy is None else 0.5 * trace_proxy

    rows = [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "TRANS4736_0_source_shell",
            "source_case": source_transition["case"],
            "radius_m": source_transition["radius_m"],
            "G_K_Lm1": source_transition["G_K_Lm1"],
            "L_cg_m": source_transition["L_cg_m"],
            "U_B": source_transition["U_B"],
            "Pi_B": source_transition["Pi_B"],
            "trace_gradient_proxy": source_transition["trace_gradient_proxy"],
            "V_Lcg_radial_proxy": vlcg_radial_proxy,
            "q_trace_Lm3": "",
            "q_budget_Lm3": "",
            "PPN_ratio_to_budget": "",
            "required_cancellation_fraction": "",
            "open_requirement": "transition_shell_current_PPN_solver",
            "status": "source_model_transition_shell_quarantined",
            "source_path": str(SOURCE_MODEL_SUMMARY),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "TRANS4736_1_constant_F_bound",
            "source_case": trace_constant["case"],
            "radius_m": trace_constant["radius_m"],
            "G_K_Lm1": source_transition["G_K_Lm1"],
            "L_cg_m": trace_constant["L_cg_m"],
            "U_B": trace_constant["U_B"],
            "Pi_B": trace_constant["Pi_B"],
            "trace_gradient_proxy": trace_constant["trace_gradient_proxy"],
            "V_Lcg_radial_proxy": vlcg_radial_proxy,
            "q_trace_Lm3": trace_constant["q_trace_Lm3"],
            "q_budget_Lm3": trace_constant["q_budget_Lm3"],
            "PPN_ratio_to_budget": trace_constant["PPN_ratio_to_budget"],
            "required_cancellation_fraction": trace_constant["required_cancellation_fraction"],
            "open_requirement": trace_constant["open_requirements"],
            "status": "fails_dry_ppn_proxy_by_large_margin",
            "source_path": str(TRACE_BOUND_SUMMARY),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "TRANS4736_2_U_power_bound",
            "source_case": trace_u_power["case"],
            "radius_m": trace_u_power["radius_m"],
            "G_K_Lm1": source_transition["G_K_Lm1"],
            "L_cg_m": trace_u_power["L_cg_m"],
            "U_B": trace_u_power["U_B"],
            "Pi_B": trace_u_power["Pi_B"],
            "trace_gradient_proxy": trace_u_power["trace_gradient_proxy"],
            "V_Lcg_radial_proxy": vlcg_radial_proxy,
            "q_trace_Lm3": trace_u_power["q_trace_Lm3"],
            "q_budget_Lm3": trace_u_power["q_budget_Lm3"],
            "PPN_ratio_to_budget": trace_u_power["PPN_ratio_to_budget"],
            "required_cancellation_fraction": trace_u_power["required_cancellation_fraction"],
            "open_requirement": trace_u_power["open_requirements"],
            "status": "U_B_power_does_not_rescue_transition",
            "source_path": str(TRACE_BOUND_SUMMARY),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]

    for row in rows:
        q_trace = numeric_value(row, "q_trace_Lm3")
        q_budget = numeric_value(row, "q_budget_Lm3")
        ratio = safe_ratio(q_trace, q_budget)
        row["q_trace_over_budget"] = ratio if ratio is not None else ""
    return rows


def propagation_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "PROP4736_0_to_VGk",
            "V_GK <= V_KB_grad + V_projector + V_metric + V_connection + V_support + V_boundary + V_readout",
            "active G_K leakage budget",
            "SRC4736_1_4735_gk",
        ),
        (
            "PROP4736_1_to_VLcg",
            "V_Lcg <= Omega_H V_LH + Omega_K V_GK + 0.5 Omega_K V_alphaK",
            "G_K feeds the L_cg derivative budget through Omega_K",
            "SRC4736_0_4735_next",
        ),
        (
            "PROP4736_2_to_transition",
            "Transition shell requires q_current/K_hat cancellation or a dedicated current solver; U_B^2 is not enough there.",
            "forces next derivation route",
            "SRC4736_6_91_transition",
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
            "timestamp_utc": timestamp,
        }
        for propagation_id, expression, meaning, source_id in specs
    ]


def gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4736_0_exact_GK_theorem", "Promote G_K q-basic only if K_B plus projector/metric/connection/support/readout all descend.", "closed_unsigned", False),
        ("GATE4736_1_zero_set_regularized", "Handle G_K=0 branch with FLRW/Hubble-cap or regularized norm before using ln G_K.", "closed_branch_required", False),
        ("GATE4736_2_transition_bound", "Transition shell cannot pass from constant F or U_B^2 dry bound.", "closed_transition_fails_dry_bound", False),
        ("GATE4736_3_next_solver", "Move to transition current solver or exact K_hat cancellation identity.", "open_next_target", False),
        ("GATE4736_4_no_public_claim", "No local-GR, PPN, R10 or Newtonian-limit pass from this checkpoint.", "closed_firewall", False),
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
        ("FW4736_0_no_local_gr_claim", "No local-GR, PPN, R10 or Newtonian-limit pass is claimed by 4736."),
        ("FW4736_1_no_GK_scalar_shortcut", "Do not treat K_B scalar q-basic ownership as enough for G_K q-basic ownership."),
        ("FW4736_2_no_U_power_transition_escape", "Do not claim U_B^2 rescues transition shells; source rows show U_B is order one there."),
        ("FW4736_3_no_amplitude_retuning", "Do not tune F_L or transition width to the local PPN budget."),
        ("FW4736_4_no_GitHub_action", "No GitHub action is performed by this checkpoint."),
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
            "summary": "G_K q-basic ownership is exact only if K_B and the gradient/readout geometry descend; transition shell numeric rows force the next route to a current solver or exact K_hat cancellation identity.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4736_0_local_only",
            "status": "local_only_private_checkpoint",
            "detail": "Generated local post-checkpoint and formalization files only.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4736_1_science_verdict",
            "status": "derivation_progress_nonclaim",
            "detail": "G_K owner proof narrowed to K_B plus projector/connection/support descent; transition shell dry bounds remain catastrophically above PPN proxy.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "The transition shell remains the live local danger; U_B^2 and scalar G_K ownership do not close it.",
            "preferred_route": "Derive q_current = nabla Gamma_eff - nabla_mu K_hat^{mu nu} through the transition and test for an exact K_hat/current cancellation identity.",
            "fallback_route": "If no identity exists, build a transition-shell width/current bound row with source-backed numeric thresholds and keep local-GR blocked.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullets(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def transition_summary(transition_rows: list[dict[str, Any]]) -> str:
    lines = []
    for row in transition_rows:
        lines.append(
            f"- `{row['row_id']}`: status `{row['status']}`, U_B `{row['U_B']}`, "
            f"trace proxy `{row['trace_gradient_proxy']}`, PPN ratio `{row['PPN_ratio_to_budget']}`."
        )
    return "\n".join(lines)


def write_docs(
    timestamp: str,
    theorem: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    bound: list[dict[str, Any]],
    transition: list[dict[str, Any]],
    propagation: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4736 Y5 R2FR: G_K Parent Owner Or Transition-Shell V_Lcg Bound

Generated: `{timestamp}`

## Summary

- Work is local-only and private.
- Target: prove `G_K` is parent-owned/q-basic, or turn its failure into a sourceable local bound.
- Result: exact conditional theorem exists, but scalar ownership of `K_B` is not enough.
- The transition-shell numerical rows are severe: constant trace and `U_B^2` both remain quarantined, with dry PPN proxy ratios of order `1e16`.

## Exact G_K Owner Fork

Use the covariant parent form:

```text
Y_a = P_a^b nabla_b ln K_B
G_K = (h^ab Y_a Y_b)^(1/2)
```

Then `D_v G_K=0` follows only if:

```text
D_v K_B = 0
D_v P_a^b = 0
D_v h^ab = 0
D_v connection/readout/support/boundary = 0
```

This is the precise fork: `K_B` scalar descent is necessary but not sufficient.

## Theorem Rows

{bullets(theorem, "theorem_id", "statement")}

## K_B Owner Audit

{bullets(owner, "owner_id", "statement")}

## G_K Bound

{bullets(bound, "bound_id", "expression")}

## Transition Shell Numeric Rows

{transition_summary(transition)}

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

    formal = f"""# 752 PPC4161: G_K Parent Owner Or Transition-Shell V_Lcg Bound

Generated: `{timestamp}`

## Current Status

`{DECISION}`

## Derived Conditional

```text
G_K = ||P_perp nabla ln K_B||
D_v G_K = 0
```

only if the scalar `K_B`, the projector, the metric/connection, and the transition support/readout all descend through the quotient map.

## Nonclaim Bound

```text
V_GK <= V_KB_grad + V_projector + V_metric + V_connection + V_support + V_boundary + V_readout
V_Lcg <= Omega_H V_LH + Omega_K V_GK + 0.5 Omega_K V_alphaK
```

## Transition Verdict

The source-model transition shell remains quarantined. The dry PPN proxy rows require a dedicated transition current solver or an exact `K_hat` cancellation identity; amplitude suppression by `U_B^2` is not enough at the transition.

## Next

`{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""

## {MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Result: `G_K` q-basic ownership is exact only if `K_B` plus projector/metric/connection/support/readout all descend.
- Transition-shell verdict: dry PPN proxy rows stay quarantined; `U_B^2` is not enough at the shell.
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
- Packet update: the `G_K` throat is reduced to a conditional owner theorem plus a transition-shell numeric bound.
- Claim status: nonclaim; no local-GR/PPN/R10 pass.
""",
    )
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4736-Y5-R2FR-GK-parent-owner-or-transition-shell-VLcg-bound.md`

## Decision

`{DECISION}`

## What moved forward

- `G_K` now has an exact q-basic owner theorem with explicit required clauses.
- The fallback `V_GK` budget includes scalar, projector, metric, connection, support, boundary and readout terms.
- The transition shell is numerically identified as the next local danger; `U_B^2` does not rescue it.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
""",
    )


def add_claim_once(timestamp: str) -> None:
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_bridge",
        "claim": "4736 proves G_K q-basic ownership only as an exact conditional theorem and stages transition-shell numeric bounds that force a current/Khat identity next.",
        "current_evidence": "Generated source register, G_K theorem rows, K_B owner audit, G_K derivative bound, transition-shell numeric rows, propagation rows, gates, firewalls, decision, status, next target and validation.",
        "status": "GK_owner_conditional_transition_bound_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Promoting scalar K_B ownership, U_B^2 trace closure, or dry transition bounds to a local-GR pass.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Transition-shell q-current/Khat cancellation, support/readout descent and numeric local PPN/R10 bounds remain unresolved.",
        "title": "G_K parent owner or transition-shell V_Lcg bound",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    for fieldname in fieldnames:
        row.setdefault(fieldname, "")
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
    owner: list[dict[str, Any]],
    bound: list[dict[str, Any]],
    transition: list[dict[str, Any]],
    propagation: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    generated_with_validation = GENERATED_CSVS + [VALIDATION_CSV]
    transition_ratios = [
        float(row["PPN_ratio_to_budget"])
        for row in transition
        if row["PPN_ratio_to_budget"] != ""
    ]
    checks = [
        ("VAL4736_0_sources_exist", all(row["exists"] for row in sources), "all cited 4736 source paths exist"),
        ("VAL4736_1_needles_found", all(row["needle_found"] for row in sources), "all cited 4736 source needles found"),
        ("VAL4736_2_GK_theorem_written", any(row["theorem_id"] == "GK4736_1_exact_conditional_zero" for row in theorem), "G_K exact conditional theorem row is written"),
        ("VAL4736_3_KB_owner_written", any(row["owner_id"] == "KB4736_1_exact_qbasic_condition" for row in owner), "K_B owner audit is written"),
        ("VAL4736_4_GK_bound_written", any("V_GK <=" in row["expression"] for row in bound), "G_K derivative bound is written"),
        ("VAL4736_5_transition_numeric_rows", len(transition) == 3 and all(row["valid_for_claim"] is False for row in transition), "transition shell numeric rows are nonclaim"),
        ("VAL4736_6_transition_not_rescued", all(ratio > 1.0 for ratio in transition_ratios), "transition dry-bound ratios exceed budget"),
        ("VAL4736_7_propagation_written", any("V_Lcg <=" in row["expression"] for row in propagation), "G_K propagates to V_Lcg"),
        ("VAL4736_8_claim_gates_closed", all(row["valid_for_claim"] is False for row in gates), "all claim gates remain closed"),
        ("VAL4736_9_docs_written", DOC_PATH.exists() and FORMAL_PATH.exists(), "checkpoint and formal documents written"),
        ("VAL4736_10_spine_packet_markers", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), "spine and packet markers inserted"),
        ("VAL4736_11_claim_row_added", CLAIM_ID in read_text(CLAIMS_PATH), "claims register contains L-578"),
        ("VAL4736_12_resume_updated", NEXT_TARGET in read_text(RESUME_PATH), "resume points to 4737 next target"),
        ("VAL4736_13_csv_parse", all(parse_csv(path) for path in generated_with_validation if path.exists()), "all generated 4736 CSV files parse cleanly"),
        ("VAL4736_14_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
    ]
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4736_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "4736 G_K parent owner or transition-shell V_Lcg bound validation",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    theorem = gk_theorem_rows(timestamp)
    owner = kb_owner_rows(timestamp)
    bound = gk_bound_rows(timestamp)
    transition = transition_numeric_rows(timestamp)
    propagation = propagation_rows(timestamp)
    gates = gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(GK_THEOREM_CSV, theorem)
    write_csv(KB_OWNER_CSV, owner)
    write_csv(GK_BOUND_CSV, bound)
    write_csv(TRANSITION_CSV, transition)
    write_csv(PROPAGATION_CSV, propagation)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, theorem, owner, bound, transition, propagation, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, theorem, owner, bound, transition, propagation, gates, timestamp))


if __name__ == "__main__":
    main()

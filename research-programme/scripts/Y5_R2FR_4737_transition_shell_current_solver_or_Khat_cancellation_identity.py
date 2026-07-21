from __future__ import annotations

import csv
import json
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

CHECKPOINT = "4737"
CLAIM_ID = "L-579"
MARKER = "PPC4161_TRANSITION_SHELL_CURRENT_SOLVER_OR_KHAT_CANCELLATION_IDENTITY_4737"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_SHELL_CURRENT_SOLVER_OR_KHAT_CANCELLATION_IDENTITY_4737"
DECISION = "TRANSITION_CURRENT_REQUIRES_TRACEFREE_RIGHT_INVERSE_OR_QUARANTINE_EQUATIONS_NONCLAIM"
NEXT_TARGET = "4738-Y5-R2FR-tracefree-Khat-right-inverse-parent-action-or-conservation-quarantine-equations.md"

DOC_PATH = POST / "4737-Y5-R2FR-transition-shell-current-solver-or-Khat-cancellation-identity.md"
FORMAL_PATH = FORMAL / "753-PPC4161-transition-shell-current-solver-or-Khat-cancellation-identity.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOLAR_RUN = RUNS / "solar_transition_current_ppn_gate_20260527-215447"
EXACT_RUN = RUNS / "20260528-175258-exact-transition-cancellation-or-projector-theorem"
SOLAR_SUMMARY = SOLAR_RUN / "summary.csv"
SOLAR_STATUS = SOLAR_RUN / "status.json"
EXACT_SUMMARY = EXACT_RUN / "summary.csv"
EXACT_STATUS = EXACT_RUN / "status.json"
EXACT_GATE_CRITERIA = EXACT_RUN / "results" / "gate_criteria.csv"
EXACT_ALGEBRA = EXACT_RUN / "results" / "algebra_requirements.csv"
EXACT_BLOCKERS = EXACT_RUN / "results" / "remaining_blockers.csv"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4737_SOURCE_REGISTER.csv"
THRESHOLD_CSV = SOURCE_DIR / "P8_Y5_R2FR_4737_TRANSITION_CURRENT_THRESHOLD_ROWS.csv"
KHAT_IDENTITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4737_KHAT_CANCELLATION_IDENTITY_AUDIT.csv"
RIGHT_INVERSE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4737_TRACEFREE_RIGHT_INVERSE_CONTRACT.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4737_ROUTE_DECISION_MATRIX.csv"
PROPAGATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4737_PROPAGATION_ROWS.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4737_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4737_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4737_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4737_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4737_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4737_VALIDATION.csv"

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    THRESHOLD_CSV,
    KHAT_IDENTITY_CSV,
    RIGHT_INVERSE_CSV,
    ROUTE_MATRIX_CSV,
    PROPAGATION_CSV,
    GATES_CSV,
    FIREWALL_CSV,
    DECISION_CSV,
    STATUS_CSV,
    NEXT_TARGET_CSV,
]

SOURCE_SPECS = [
    ("SRC4737_0_4736_next", SOURCE_DIR / "P8_Y5_R2FR_4736_NEXT_TARGET.csv", "transition shell remains the live local danger", "4736 handoff"),
    ("SRC4737_1_4736_transition", SOURCE_DIR / "P8_Y5_R2FR_4736_TRANSITION_SHELL_NUMERIC_BOUND.csv", "TRANS4736_2_U_power_bound", "4736 transition numeric bound"),
    ("SRC4737_2_eq_q", FORMAL / "05-equation-register.md", "q^nu = nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}.", "core q-current identity"),
    ("SRC4737_3_eq_tracefree", FORMAL / "05-equation-register.md", "g_mu_nu K_hat^{mu nu} = 0", "K_hat trace-free split"),
    ("SRC4737_4_redteam_identity", FORMAL / "06-consistency-red-team.md", "cancellation must be an identity/theorem", "anti-numeric-cancellation warning"),
    ("SRC4737_5_solar_doc", FORMAL / "92-solar-transition-current-ppn-gate.md", "the Solar transition shell does not pass as a local metric source", "solar transition verdict"),
    ("SRC4737_6_solar_status", SOLAR_STATUS, "required_transition_q_suppression_factor", "solar transition threshold"),
    ("SRC4737_7_solar_summary", SOLAR_SUMMARY, "Khat_cancellation_transition_open", "Khat open route row"),
    ("SRC4737_8_exact_script", FORMAL_SCRIPTS / "exact_transition_cancellation_or_projector_theorem_gate.py", "local_Khat_divergence_identity", "exact cancellation prior gate"),
    ("SRC4737_9_exact_status", EXACT_STATUS, "exact_Khat_cancellation_parent_derived", "exact gate status"),
    ("SRC4737_10_exact_gate", EXACT_GATE_CRITERIA, "exact_Khat_cancellation", "gate criteria"),
    ("SRC4737_11_exact_algebra", EXACT_ALGEBRA, "tracefree split does not determine divergence", "algebra requirement"),
    ("SRC4737_12_exact_blockers", EXACT_BLOCKERS, "Khat_divergence_identity", "remaining blocker"),
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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def find_row(path: Path, column: str, value: str) -> dict[str, str]:
    for row in load_csv_rows(path):
        if row.get(column) == value:
            return row
    raise ValueError(f"missing row {column}={value} in {path}")


def threshold_rows(timestamp: str) -> list[dict[str, Any]]:
    solar_status = load_json(SOLAR_STATUS)
    exact_status = load_json(EXACT_STATUS)
    selected_cases = [
        "bare_transition_shell_fail",
        "U_B2_transition_shell_fail",
        "wide_transition_shell_scaling_fail",
        "Khat_cancellation_transition_open",
        "nonlocal_routed_transition_quarantine",
        "sector_tuned_transition_suppression_fail",
    ]
    rows: list[dict[str, Any]] = []
    for case_name in selected_cases:
        source_row = find_row(SOLAR_SUMMARY, "case", case_name)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "case": source_row["case"],
                "branch": source_row["branch"],
                "gate_status": source_row["gate_status"],
                "PPN_ratio_to_budget": source_row["PPN_ratio_to_budget"],
                "required_q_suppression_factor": source_row["required_q_suppression_factor"],
                "exact_theorem_assumed": source_row["exact_theorem_assumed"],
                "routed_nonlocal": source_row["routed_nonlocal"],
                "sector_tuned": source_row["sector_tuned"],
                "open_requirements": source_row["open_requirements"],
                "failed_requirements": source_row["failed_requirements"],
                "source_path": str(SOLAR_SUMMARY),
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "case": "status_required_suppression",
            "branch": "status_json",
            "gate_status": "threshold_import",
            "PPN_ratio_to_budget": solar_status["U_B2_transition_ratio_to_budget"],
            "required_q_suppression_factor": solar_status["required_transition_q_suppression_factor"],
            "exact_theorem_assumed": exact_status["exact_Khat_cancellation_parent_derived"],
            "routed_nonlocal": exact_status["conservation_owned_quarantine_only"],
            "sector_tuned": False,
            "open_requirements": exact_status["recommendation"],
            "failed_requirements": "derived_local_GR_blocked_at_transition",
            "source_path": str(SOLAR_STATUS),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def khat_identity_rows(timestamp: str) -> list[dict[str, Any]]:
    exact_status = load_json(EXACT_STATUS)
    specs = [
        (
            "KHAT4737_0_q_current",
            "q_tr^nu = nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}",
            "definition",
            "defined_not_zero",
            "SRC4737_2_eq_q",
            False,
        ),
        (
            "KHAT4737_1_tracefree_constraint",
            "g_mu_nu K_hat^{mu nu}=0, so the cheap K_hat=Gamma_eff g^{mu nu} cancellation is not an allowed K_hat residual.",
            "anti-cheat theorem",
            "trivial_metric_cancellation_rejected",
            "SRC4737_3_eq_tracefree",
            False,
        ),
        (
            "KHAT4737_2_parent_identity_needed",
            "A valid exact route needs a parent-signed trace-free right-inverse R_T^{mu nu}[Gamma_eff] with div R_T = grad Gamma_eff.",
            "identity contract",
            "open_not_parent_signed",
            "SRC4737_10_exact_gate",
            False,
        ),
        (
            "KHAT4737_3_prior_gate_status",
            f"Prior exact gate says exact_Khat_cancellation_parent_derived={exact_status['exact_Khat_cancellation_parent_derived']}.",
            "evidence import",
            "not_derived",
            "SRC4737_9_exact_status",
            False,
        ),
        (
            "KHAT4737_4_quarantine_route",
            "If no trace-free identity exists, transition current must be conservation-owned and nonlocal/quarantined, not local metric projected.",
            "fallback route",
            "quarantine_only",
            "SRC4737_12_exact_blockers",
            False,
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "identity_id": identity_id,
            "statement": statement,
            "role": role,
            "status": status,
            "source_id": source_id,
            "source_path": source_path(source_id),
            "valid_for_claim": valid_for_claim,
            "timestamp_utc": timestamp,
        }
        for identity_id, statement, role, status, source_id, valid_for_claim in specs
    ]


def right_inverse_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "RINV4737_0_decomposition",
            "K_hat^{mu nu}=R_T^{mu nu}[Gamma_eff]+Delta_K^{mu nu}",
            "g_mu_nu R_T^{mu nu}=0 and g_mu_nu Delta_K^{mu nu}=0",
            "required",
        ),
        (
            "RINV4737_1_divergence_identity",
            "nabla_mu R_T^{mu nu}=nabla^nu Gamma_eff",
            "must hold as parent identity, not by fitting a local shell profile",
            "required",
        ),
        (
            "RINV4737_2_residual_bound",
            "|nabla_mu Delta_K^{mu nu}| <= q_budget or P_metric,loc div Delta_K=0",
            "needed after the right-inverse split",
            "required",
        ),
        (
            "RINV4737_3_nonlocal_warning",
            "A trace-free right-inverse normally requires an inverse differential operator or boundary/superpotential data.",
            "closure unless parent action supplies it",
            "warning",
        ),
        (
            "RINV4737_4_source_signature",
            "Parent action must contain the multiplier, Ward identity, superpotential, or boundary term that generates R_T.",
            "source contract for 4738",
            "next_target",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "contract_id": contract_id,
            "condition": condition,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for contract_id, condition, meaning, status in specs
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    gate_rows = load_csv_rows(EXACT_GATE_CRITERIA)
    imported = [
        {
            "checkpoint": CHECKPOINT,
            "route_id": f"ROUTE4737_import_{row['criterion']}",
            "route": row["criterion"],
            "status": row["status"],
            "detail": row["detail"],
            "source_path": str(EXACT_GATE_CRITERIA),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in gate_rows
    ]
    imported.append(
        {
            "checkpoint": CHECKPOINT,
            "route_id": "ROUTE4737_new_tracefree_right_inverse",
            "route": "tracefree_right_inverse_parent_action",
            "status": "best_next_derivation_target",
            "detail": "This is the non-cheating version of Khat cancellation because it respects g.K_hat=0.",
            "source_path": str(EXACT_ALGEBRA),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return imported


def propagation_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "PROP4737_0_threshold",
            "Transition q must be reduced by about 4.2e-17 relative to the U_B2 shell row unless an exact identity/routing theorem removes local metric projection.",
            "imports the numeric severity into the local-GR bridge",
            "SRC4737_6_solar_status",
        ),
        (
            "PROP4737_1_tracefree",
            "K_hat=Gamma_eff g is forbidden because K_hat is trace-free; any cancellation must use a trace-free right inverse.",
            "prevents fake proof",
            "SRC4737_3_eq_tracefree",
        ),
        (
            "PROP4737_2_next",
            "4738 must hunt parent action/superpotential/quarantine equations rather than rerunning amplitude suppression.",
            "sets next route",
            "SRC4737_12_exact_blockers",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "propagation_id": propagation_id,
            "statement": statement,
            "meaning": meaning,
            "source_id": source_id,
            "source_path": source_path(source_id),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for propagation_id, statement, meaning, source_id in specs
    ]


def gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4737_0_no_trivial_metric_Khat", "Reject K_hat=Gamma_eff g because K_hat is trace-free residual.", "closed_firewall", False),
        ("GATE4737_1_parent_right_inverse", "Promote only if trace-free R_T with div R_T=grad Gamma_eff is parent-derived.", "closed_unsigned", False),
        ("GATE4737_2_transition_threshold", "Promote only if transition q suppression reaches the sourced 4.2e-17 threshold by identity, not tuning.", "closed_threshold", False),
        ("GATE4737_3_quarantine_equations", "If no identity exists, conservation-owned quarantine equations must be explicit.", "open_next_target", False),
        ("GATE4737_4_no_local_claim", "No local-GR/PPN/R10/Newtonian pass from this checkpoint.", "closed_firewall", False),
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
        ("FW4737_0_no_gmetric_cancellation", "Do not use K_hat=Gamma_eff g as a K_hat cancellation; it violates the trace-free split."),
        ("FW4737_1_no_numeric_cancellation", "Do not tune cancellation to 4.2e-17; it must be an identity/theorem."),
        ("FW4737_2_no_sector_routing", "Do not hide Solar transition current in galaxy/cosmology labels."),
        ("FW4737_3_no_public_claim", "No local-GR/PPN/R10/Newtonian/public claim from 4737."),
        ("FW4737_4_no_GitHub_action", "No GitHub action is performed by this checkpoint."),
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
            "summary": "Transition current cannot be made local-safe by U_B2, width, sector tuning, or trivial Khat=Gamma g. The remaining honest route is a parent-derived trace-free right-inverse/superpotential identity or explicit conservation-owned quarantine equations.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4737_0_local_only",
            "status": "local_only_private_checkpoint",
            "detail": "Generated local post-checkpoint and formalization files only.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4737_1_science_verdict",
            "status": "transition_identity_contract_nonclaim",
            "detail": "The transition shell needs a parent trace-free right-inverse/Khat identity or conservation-owned quarantine equations; local pass remains blocked.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "The exact Khat route must respect trace-free Khat, so the next derivation has to find a parent trace-free right inverse or demote to quarantine equations.",
            "preferred_route": "Search parent action/Noether/Ward/superpotential structure for a trace-free R_T with div R_T=grad Gamma_eff.",
            "fallback_route": "Write conservation-owned quarantine equations with q_metric,loc=0 and explicit nonlocal/transport exchange ownership.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullets(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def threshold_summary(rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        f"- `{row['case']}`: `{row['gate_status']}`, ratio `{row['PPN_ratio_to_budget']}`, required suppression `{row['required_q_suppression_factor']}`."
        for row in rows
    )


def write_docs(
    timestamp: str,
    threshold: list[dict[str, Any]],
    identity: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    route_matrix: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4737 Y5 R2FR: Transition-Shell Current Solver Or Khat Cancellation Identity

Generated: `{timestamp}`

## Summary

- Work is local-only and private.
- Target: decide whether the transition shell can be saved by an exact `K_hat`/current identity.
- Result: the trivial cancellation `K_hat = Gamma_eff g` is rejected because `K_hat` is trace-free.
- Therefore the only non-cheating exact route is a parent-derived trace-free right inverse/superpotential:

```text
K_hat^{{mu nu}} = R_T^{{mu nu}}[Gamma_eff] + Delta_K^{{mu nu}}
g_mu_nu R_T^{{mu nu}} = 0
nabla_mu R_T^{{mu nu}} = nabla^nu Gamma_eff
```

Without that, the transition must be explicitly conservation-owned and quarantined/nonlocal.

## Threshold Rows

{threshold_summary(threshold)}

## Khat Identity Audit

{bullets(identity, "identity_id", "statement")}

## Trace-Free Right-Inverse Contract

{bullets(contract, "contract_id", "condition")}

## Route Matrix

{bullets(route_matrix, "route_id", "route")}

## Promotion Gates

{bullets(gates, "gate_id", "gate")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`

No GitHub action was performed.
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 753 PPC4161: Transition-Shell Current Solver Or Khat Cancellation Identity

Generated: `{timestamp}`

## Current Status

`{DECISION}`

## Core Result

The transition current is:

```text
q_tr^nu = nabla^nu Gamma_eff - nabla_mu K_hat^{{mu nu}}
```

Because `K_hat` is trace-free, the metric-proportional shortcut is forbidden:

```text
K_hat^{{mu nu}} != Gamma_eff g^{{mu nu}}
```

A real exact cancellation requires:

```text
exists R_T^{{mu nu}}:
  g_mu_nu R_T^{{mu nu}} = 0
  nabla_mu R_T^{{mu nu}} = nabla^nu Gamma_eff
```

and the parent action must own this operator, boundary data, and residual `Delta_K`.

## Verdict

The source-backed transition threshold remains about `4.2e-17` in required q suppression. No local pass is claimed.

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
- Result: trivial `K_hat=Gamma_eff g` cancellation is forbidden by the trace-free split.
- Required exact route: parent-derived trace-free right inverse/superpotential with `div R_T = grad Gamma_eff`.
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
- Packet update: the transition shell current route now has a non-cheating trace-free `K_hat` identity contract.
- Claim status: nonclaim; no local-GR/PPN/R10 pass.
""",
    )
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4737-Y5-R2FR-transition-shell-current-solver-or-Khat-cancellation-identity.md`

## Decision

`{DECISION}`

## What moved forward

- The transition-current threshold from the older solver is imported into the current chain.
- `K_hat = Gamma_eff g` is explicitly rejected as a fake cancellation because `K_hat` is trace-free.
- The next theorem target is a trace-free right-inverse/superpotential parent identity, or explicit conservation-owned quarantine equations.

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
        "claim": "4737 imports the transition-current PPN threshold and derives the non-cheating Khat cancellation contract: Khat must be trace-free, so exact cancellation requires a parent trace-free right inverse or quarantine equations.",
        "current_evidence": "Generated source register, transition threshold rows, Khat identity audit, trace-free right-inverse contract, route matrix, propagation, gates, firewalls, decision, status, next target and validation.",
        "status": "transition_current_tracefree_identity_contract_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Using Khat=Gamma_eff g, numeric cancellation, sector routing, or U_B2 transition suppression as a local-GR pass.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Parent trace-free right inverse, superpotential/boundary ownership, Delta_K residual, and quarantine equations remain unresolved.",
        "title": "Transition-shell current solver or Khat cancellation identity",
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
    threshold: list[dict[str, Any]],
    identity: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    route_matrix: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    generated_with_validation = GENERATED_CSVS + [VALIDATION_CSV]
    exact_status = load_json(EXACT_STATUS)
    imported_suppression = float(load_json(SOLAR_STATUS)["required_transition_q_suppression_factor"])
    checks = [
        ("VAL4737_0_sources_exist", all(row["exists"] for row in sources), "all cited 4737 source paths exist"),
        ("VAL4737_1_needles_found", all(row["needle_found"] for row in sources), "all cited 4737 source needles found"),
        ("VAL4737_2_threshold_imported", imported_suppression < 1.0e-12, "transition q suppression threshold imported"),
        ("VAL4737_3_no_trivial_Khat", any(row["identity_id"] == "KHAT4737_1_tracefree_constraint" for row in identity), "trivial metric Khat cancellation is rejected"),
        ("VAL4737_4_parent_not_derived", exact_status["exact_Khat_cancellation_parent_derived"] is False, "prior exact Khat parent identity remains not derived"),
        ("VAL4737_5_right_inverse_contract", any(row["contract_id"] == "RINV4737_1_divergence_identity" for row in contract), "trace-free right-inverse contract is written"),
        ("VAL4737_6_route_matrix_imported", any(row["route"] == "exact_Khat_cancellation" for row in route_matrix), "prior exact route matrix is imported"),
        ("VAL4737_7_claim_gates_closed", all(row["valid_for_claim"] is False for row in gates), "all claim gates remain closed"),
        ("VAL4737_8_docs_written", DOC_PATH.exists() and FORMAL_PATH.exists(), "checkpoint and formal documents written"),
        ("VAL4737_9_spine_packet_markers", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), "spine and packet markers inserted"),
        ("VAL4737_10_claim_row_added", CLAIM_ID in read_text(CLAIMS_PATH), "claims register contains L-579"),
        ("VAL4737_11_resume_updated", NEXT_TARGET in read_text(RESUME_PATH), "resume points to 4738 next target"),
        ("VAL4737_12_csv_parse", all(parse_csv(path) for path in generated_with_validation if path.exists()), "all generated 4737 CSV files parse cleanly"),
        ("VAL4737_13_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
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
            "check_id": "VAL4737_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "4737 transition-shell current solver or Khat cancellation identity validation",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    threshold = threshold_rows(timestamp)
    identity = khat_identity_rows(timestamp)
    contract = right_inverse_rows(timestamp)
    route_matrix = route_matrix_rows(timestamp)
    propagation = propagation_rows(timestamp)
    gates = gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(THRESHOLD_CSV, threshold)
    write_csv(KHAT_IDENTITY_CSV, identity)
    write_csv(RIGHT_INVERSE_CSV, contract)
    write_csv(ROUTE_MATRIX_CSV, route_matrix)
    write_csv(PROPAGATION_CSV, propagation)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, threshold, identity, contract, route_matrix, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, threshold, identity, contract, route_matrix, gates, timestamp))


if __name__ == "__main__":
    main()

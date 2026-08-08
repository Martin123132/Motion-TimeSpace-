from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3847"
BRANCH = "MTS_R2FR_Y5_OBSERVER_COFRAME_COMPLETION_FROM_TS_3847"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3847-Y5-R2FR-observer-coframe-completion-from-TS-or-metric-bridge-demotion.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3846 = PCW / "3846-Y5-R2FR-MTS-to-visible-metric-bridge-or-action-candidate-reject.md"
P_3845 = PCW / "3845-Y5-R2FR-visible-metric-parent-action-candidate-from-MTS-or-Lovelock-failure.md"
P_10_OBSERVER = PCW / "10-observer-map-symplectic-contract.md"
P_09_CELL = PCW / "09-hamiltonian-radial-cell-derivation.md"

CSV_3846_THEOREM = OUT / "P8_Y5_R2FR_3846_METRIC_BRIDGE_THEOREM.csv"
CSV_3846_OWNERSHIP = OUT / "P8_Y5_R2FR_3846_MTS_PRIMITIVE_OWNERSHIP_AUDIT.csv"
CSV_3846_RESIDUALS = OUT / "P8_Y5_R2FR_3846_CONNECTION_READOUT_RESIDUALS.csv"
CSV_3846_NEXT = OUT / "P8_Y5_R2FR_3846_NEXT_TARGET.csv"
CSV_3846_VALIDATION = OUT / "P8_Y5_BRR545_3846_VALIDATION.csv"
CSV_3845_ACTION = OUT / "P8_Y5_R2FR_3845_VISIBLE_ACTION_CANDIDATE.csv"
CSV_943_COFRAME = OUT / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3847_SOURCE_REGISTER.csv",
    "coframe": OUT / "P8_Y5_R2FR_3847_OBSERVER_COFRAME_COMPLETION.csv",
    "domain": OUT / "P8_Y5_R2FR_3847_COFRAME_DOMAIN_AND_LIMITS.csv",
    "bridge_update": OUT / "P8_Y5_R2FR_3847_METRIC_BRIDGE_UPDATE.csv",
    "action_update": OUT / "P8_Y5_R2FR_3847_ACTION_CANDIDATE_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3847_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3847_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3847_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3847_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3847_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3847_0_3846_doc", P_3846, "algebraic bridge works conditionally"),
    ("SRC3847_1_3846_theorem", CSV_3846_THEOREM, "MBT3846_3_coframe_special_case"),
    ("SRC3847_2_3846_ownership", CSV_3846_OWNERSHIP, "MBO3846_0_tau_time"),
    ("SRC3847_3_3846_residuals", CSV_3846_RESIDUALS, "B_metric_bridge"),
    ("SRC3847_4_3846_next", CSV_3846_NEXT, "3847-Y5-R2FR-observer-coframe-completion"),
    ("SRC3847_5_3846_validation", CSV_3846_VALIDATION, "PASS"),
    ("SRC3847_6_3845_doc", P_3845, "minimal visible parent action candidate"),
    ("SRC3847_7_3845_action", CSV_3845_ACTION, "VAC3845_0_minimal_visible_EH_candidate"),
    ("SRC3847_8_observer_contract", P_10_OBSERVER, "theta_0 = T c dt"),
    ("SRC3847_9_cell_derivation", P_09_CELL, "radial"),
    ("SRC3847_10_943_coframe", CSV_943_COFRAME, "CFC943_1_observed_coframe_descent"),
]

COFRAME_FORMULA = "theta^0=c_* T dt; theta^1=sqrt(S) dr; theta^2=r dtheta; theta^3=r sin(theta) dphi"
METRIC_FORMULA = "g_obs=-(theta^0)^2+(theta^1)^2+(theta^2)^2+(theta^3)^2"
LINE_ELEMENT = "ds^2=-c_*^2 T(r)^2 dt^2 + S(r) dr^2 + r^2 dOmega^2"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": "input_for_observer_coframe_completion_from_TS",
                "claim_use": "nonclaim_spherical_branch_coframe_completion_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def coframe_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "OCF3847_0_time_leg",
            "object": "theta^0",
            "formula": "theta^0=c_* T dt",
            "derivation": "direct completion of the existing observer-map theta_0=T c dt with c renamed c_*",
            "result": "tau_time=T dt and theta^0=c_* tau_time",
            "status": "EXACT_SPHERICAL_BRANCH_LEG",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "OCF3847_1_radial_leg",
            "object": "theta^1",
            "formula": "theta^1=sqrt(S) dr",
            "derivation": "direct use of the existing observer-map radial spatial leg",
            "result": "radial h_rr=S",
            "status": "EXACT_SPHERICAL_BRANCH_LEG",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "OCF3847_2_angular_legs",
            "object": "theta^2,theta^3",
            "formula": "theta^2=r dtheta; theta^3=r sin(theta) dphi",
            "derivation": "standard spherical exterior angular area gauge completes the rank-3 spatial triad",
            "result": "h_angle=r^2 dOmega^2",
            "status": "EXACT_IF_AREA_RADIUS_GAUGE_OWNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "OCF3847_3_metric",
            "object": "g_obs",
            "formula": METRIC_FORMULA,
            "derivation": "insert OCF3847_0 through OCF3847_2 into eta_ab theta^a theta^b",
            "result": LINE_ELEMENT,
            "status": "EXACT_STATIC_SPHERICAL_METRIC_CANDIDATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "OCF3847_4_bridge_match",
            "object": "3846 bridge variables",
            "formula": "tau=T dt; h=S dr^2+r^2 dOmega^2; u=T^-1 partial_t; c_*=c_*",
            "derivation": "these values satisfy tau(u)=1, h(u,.)=0, and h positive on ker(tau) when T>0,S>0,r>0",
            "result": "3846 metric theorem applies on the static spherical exterior domain",
            "status": "EXACT_CONDITIONAL_BRIDGE_MATCH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "OCF3847_5_verdict",
            "object": "coframe completion",
            "formula": COFRAME_FORMULA,
            "derivation": "T,S observer map completes to a static spherical coframe, not yet a general local branch",
            "result": "metric bridge narrowed from abstract tau/h to an explicit spherical exterior coframe",
            "status": "SPHERICAL_COFRAME_COMPLETED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def domain_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "domain_id": "OCD3847_0_static",
            "domain_clause": "static exterior branch",
            "condition": "T=T(r), S=S(r), no g_ti shift, no explicit time dependence",
            "reason": "needed for the old radial observer-cell map to be the relevant branch",
            "if_missing": "retain B_shift_time and do not use spherical coframe as full local metric",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "domain_id": "OCD3847_1_area_radius",
            "domain_clause": "area-radius angular gauge",
            "condition": "theta^2=r dtheta, theta^3=r sin(theta)dphi are parent/geometry-owned rather than fitted",
            "reason": "otherwise angular completion can hide an extra radial gauge function",
            "if_missing": "retain B_area_radius_owner",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "domain_id": "OCD3847_2_positivity",
            "domain_clause": "Lorentzian exterior signs",
            "condition": "T>0, S>0, r>0, 0<theta<pi",
            "reason": "ensures theta^0 timelike and spatial triad positive",
            "if_missing": "retain B_signature_domain",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "domain_id": "OCD3847_3_parent_owner",
            "domain_clause": "T,S are parent fields/readouts before local fitting",
            "condition": "T and S are supplied by the MTS parent branch, not chosen to fit PPN coefficients",
            "reason": "prevents copying Schwarzschild/GR metric after the fact",
            "if_missing": "retain B_TS_parent_owner",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "domain_id": "OCD3847_4_scope",
            "domain_clause": "not full arbitrary local metric",
            "condition": "branch is static spherical exterior only",
            "reason": "enough for first Newton/PPN exterior route, not enough for general local GR",
            "if_missing": "do not overclaim global/local-GR completeness",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bridge_update_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "update_id": "MBU3847_0_coframe_completion",
            "observable": "B_tau_owner+B_h_owner+B_signature",
            "formula": "on static spherical branch, tau=T dt and h=S dr^2+r^2 dOmega^2 satisfy the 3846 bridge if T>0,S>0 and area-radius gauge is owned",
            "status": "CONDITIONAL_COMPONENT_COLLAPSE",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "MBU3847_1_current_bridge_bound",
            "observable": "B_metric_bridge",
            "formula": "B_metric_bridge <= B_TS_parent_owner + B_area_radius_owner + B_shift_time + B_connection_LC + B_no_shadow_readout + B_general_branch_gap",
            "status": "REFINED_STATIC_SPHERICAL_NONCLAIM_BOUND",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "update_id": "MBU3847_2_next_physics",
            "observable": "T,S dynamics",
            "formula": "local GR/Newton now requires field equations or parent constraints for T(r), S(r), not merely a metric bridge",
            "status": "NEXT_DYNAMICAL_TARGET",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def action_update_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "adoption_id": "ACU3847_0_action_candidate_status",
            "candidate": "3845 visible EH action candidate",
            "bridge_effect": "coframe target is explicit on static spherical exterior branch",
            "current_status": "STILL_NOT_ADOPTED",
            "reason": "T,S dynamics, parent ownership, source glue, and silent-sector clauses remain unsigned",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "adoption_id": "ACU3847_1_if_TS_dynamics_close",
            "candidate": "local exterior GR/Newton route",
            "bridge_effect": "with parent-owned T,S and equations forcing the GR weak-field coefficients, the visible action candidate gains real adoption pressure",
            "current_status": "CONDITIONAL_FUTURE_ADOPTION_PRESSURE",
            "reason": "metric branch now has a concrete coframe and line element to vary/test",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3847_0_coframe_completion",
            "gate": "T,S radial observer map completes to 4D static spherical coframe",
            "status": "PASS_EXACT_CONDITIONAL_COMPLETION",
            "claim_allowed": False,
            "reason": "theta^0,theta^1 plus angular area legs produce a Lorentzian metric candidate",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3847_1_parent_owner",
            "gate": "T,S and area-radius gauge are parent-owned",
            "status": "BLOCKED_PARENT_OWNERSHIP_REQUIRED",
            "claim_allowed": False,
            "reason": "coframe completion is exact but not signed as a parent-derived branch",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3847_2_scope",
            "gate": "branch is full local GR",
            "status": "BLOCKED_STATIC_SPHERICAL_ONLY",
            "claim_allowed": False,
            "reason": "this is the first exterior test branch, not arbitrary local geometry",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3847_3_dynamics",
            "gate": "T,S dynamics reduce to Newton/GR",
            "status": "BLOCKED_FIELD_EQUATION_OR_CONSTRAINT_REQUIRED",
            "claim_allowed": False,
            "reason": "metric existence alone does not derive T(r), S(r), gamma, or beta",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3847_4_no_overclaim",
            "gate": "no local-GR/action adoption claim is promoted",
            "status": "PASS_NO_CLAIM_PROMOTED",
            "claim_allowed": False,
            "reason": "all rows remain nonclaim and scope-limited",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3847_5_next_action",
            "gate": "next target attacks T,S dynamics",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "the bridge has a line element; next derive or bound equations for T(r), S(r)",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3847_0",
            "decision": "do not demote the metric bridge yet",
            "consequence": "the bridge has an exact static spherical coframe completion worth pursuing",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3847_1",
            "decision": "do not adopt the visible action yet",
            "consequence": "coframe existence is weaker than parent dynamics/source/action descent",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3847_2",
            "decision": "next target is T,S dynamics and observer-cell constraint",
            "consequence": "try to derive R_AB=ln(T^2 S)=0 or the weak-field T,S equations from MTS, otherwise keep residuals",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3847_0",
            "next_checkpoint": "3848-Y5-R2FR-TS-dynamics-RAB-zero-or-weak-field-equation-bound.md",
            "script": "scripts/Y5_R2FR_3848_TS_dynamics_RAB_zero_or_weak_field_equation_bound.py",
            "objective": "try to derive the dynamics/constraint for T(r), S(r), especially R_AB=ln(T^2 S)=0 or the weak-field equations needed for Newton/gamma/beta",
            "reason": "3847 completes the static spherical coframe; the next missing piece is not metric existence but dynamics of T and S",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_STATIC_SPHERICAL_COFRAME_COMPLETION",
            "claim": "no action adoption, local-GR, Newton, gamma, beta, or PPN claim",
            "next": "3848 T,S dynamics R_AB zero or weak-field equation bound",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        vals = [str(row.get(col, "")).replace("\n", " ").replace("|", "\\|") for col in columns]
        body.append("| " + " | ".join(vals) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, object]],
    coframe: list[dict[str, object]],
    domain: list[dict[str, object]],
    bridge_update: list[dict[str, object]],
    action_update: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3847 - Observer Coframe Completion From T,S Or Metric Bridge Demotion

Private checkpoint. This tests whether the old `T,S` observer map can become the concrete 4D coframe needed by the 3846 metric bridge. It does not claim local GR or adopt the 3845 action.

Generated: `{timestamp}`

## Result

The static spherical coframe completion is:

`{COFRAME_FORMULA}`.

The metric is:

`{METRIC_FORMULA}`,

so the line element is:

`{LINE_ELEMENT}`.

This is a genuine constructive step: the bridge is no longer abstract `tau,h`; it has a concrete local exterior coframe branch. But it remains nonclaim because T,S and the angular area-radius gauge still need parent ownership, and metric existence alone does not derive the dynamics of `T(r)` and `S(r)`.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Coframe Completion

{markdown_table(coframe, ["row_id", "object", "formula", "status", "result"])}

## Domain And Limits

{markdown_table(domain, ["domain_id", "domain_clause", "condition", "if_missing"])}

## Metric Bridge Update

{markdown_table(bridge_update, ["update_id", "observable", "formula", "status"])}

## Action Candidate Update

{markdown_table(action_update, ["adoption_id", "candidate", "current_status", "reason"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

Do not throw this route away. The 3846 bridge now has an explicit 3847 coframe on the static spherical branch. The next hard question is dynamics: does MTS derive `R_AB=ln(T^2 S)=0`, or derive weak-field equations for `T` and `S` that reproduce Newton/gamma/beta without importing Schwarzschild?

Next target: `3848-Y5-R2FR-TS-dynamics-RAB-zero-or-weak-field-equation-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3846", "Current State After 3847", 1)
    text = "\n".join(
        line for line in text.splitlines() if not line.startswith("<!-- Generated by 3847 at ")
    )
    paragraph = (
        "`3847` completes the old radial observer map into a concrete static spherical coframe: "
        "`theta^0=c_*Tdt`, `theta^1=sqrt(S)dr`, `theta^2=rdtheta`, `theta^3=r sin(theta)dphi`, giving "
        "`ds^2=-c_*^2T(r)^2dt^2+S(r)dr^2+r^2dOmega^2`. "
        "This narrows the 3846 abstract metric bridge to an explicit local exterior branch, so the bridge is not demoted. "
        "It remains nonclaim because parent ownership of `T,S`, area-radius gauge, staticity, connection lock, and source/action descent are unsigned. "
        "The next bottleneck is dynamics: derive `R_AB=ln(T^2S)=0` or weak-field equations for `T(r),S(r)` without importing Schwarzschild/GR.\n\n"
    )
    anchor = "`3846` proves"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3847-Y5-R2FR-observer-coframe-completion-from-TS-or-metric-bridge-demotion.md`

Target: derive a full 4D observed coframe/tau/h/c package from the existing `T,S` observer-map structure, or demote the metric bridge to closure-only.

This is the best next move because 3846 proves the algebraic metric bridge and identifies coframe ownership as the first unsigned component."""
    new_gate = """`3848-Y5-R2FR-TS-dynamics-RAB-zero-or-weak-field-equation-bound.md`

Target: derive the dynamics/constraint for `T(r),S(r)`, especially `R_AB=ln(T^2S)=0` or weak-field equations needed for Newton/gamma/beta.

This is the best next move because 3847 completes the static spherical coframe; the missing step is now dynamics, not metric existence."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3847_OBSERVER_COFRAME_COMPLETION.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3847_COFRAME_DOMAIN_AND_LIMITS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3847_METRIC_BRIDGE_UPDATE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3847_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3847_OBSERVER_COFRAME_COMPLETION.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3847 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    coframe: list[dict[str, object]],
    domain: list[dict[str, object]],
    bridge_update: list[dict[str, object]],
    action_update: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    all_text = " ".join(str(row) for row in coframe + domain + bridge_update + action_update + gates)
    add(
        "VAL3847_0_sources",
        "all cited local source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3847_1_coframe_formula",
        "coframe completion formula is present",
        COFRAME_FORMULA in all_text,
        "theta^0..theta^3 formula present",
    )
    add(
        "VAL3847_2_metric_formula",
        "line element is present",
        LINE_ELEMENT in all_text,
        "static spherical metric present",
    )
    add(
        "VAL3847_3_bridge_match",
        "3846 bridge variables are matched",
        "tau=T dt" in all_text and "h=S dr^2+r^2 dOmega^2" in all_text,
        "tau/h bridge match present",
    )
    add(
        "VAL3847_4_scope_guard",
        "static spherical scope guard is active",
        "STATIC_SPHERICAL_ONLY" in all_text and "not full arbitrary local metric" in all_text,
        "scope guard present",
    )
    add(
        "VAL3847_5_next_dynamics",
        "next target attacks T,S dynamics",
        DOC_PATH.exists() and "3848-Y5-R2FR-TS-dynamics-RAB-zero-or-weak-field-equation-bound" in read_text(DOC_PATH),
        "3848 T,S dynamics target visible",
    )
    add(
        "VAL3847_6_nonclaim",
        "all 3847 rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in coframe + domain + bridge_update + action_update + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3847_7_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3847_8_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "static spherical coframe completion" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3847*", "P8_Y5_BRR545_3847*", "*Y5_R2FR_3847*", "3847-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3847_9_formalization_clean",
        "formalization-workbench has no generated 3847 project files",
        len(fwb_hits) == 0,
        "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no generated 3847 project file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3847_10_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    coframe = coframe_rows(timestamp)
    domain = domain_rows(timestamp)
    bridge_update = bridge_update_rows(timestamp)
    action_update = action_update_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["coframe"], coframe)
    write_csv(OUTPUTS["domain"], domain)
    write_csv(OUTPUTS["bridge_update"], bridge_update)
    write_csv(OUTPUTS["action_update"], action_update)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, coframe, domain, bridge_update, action_update, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, coframe, domain, bridge_update, action_update, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_STATIC_SPHERICAL_COFRAME_COMPLETION")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3835"
BRANCH = "MTS_R2FR_Y5_INTEGRATED_GAMMA_NO_SLIP_LEDGER_AND_FIRST_THRESHOLD_DASHBOARD_3835"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3835-Y5-R2FR-integrated-gamma-no-slip-ledger-and-first-threshold-dashboard.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3834 = PCW / "3834-Y5-R2FR-boundary-harmonic-scalar-slip-zero-or-gamma-bound.md"
CSV_3834_BOUNDS = OUT / "P8_Y5_R2FR_3834_BOUNDARY_GAMMA_BOUND_ROWS.csv"
CSV_3834_VALIDATION = OUT / "P8_Y5_BRR545_3834_VALIDATION.csv"
CSV_3833_BOUNDS = OUT / "P8_Y5_R2FR_3833_PARENT_EXTRA_GAMMA_BOUND_ROWS.csv"
CSV_3832_GAMMA = OUT / "P8_Y5_R2FR_3832_GAMMA_BOUND_UPDATE.csv"
CSV_3831_BOUNDS = OUT / "P8_Y5_R2FR_3831_SIGMATF_BOUND_ROWS.csv"
CSV_3830_GAMMA = OUT / "P8_Y5_R2FR_3830_GAMMA_BOUND_SOURCE_ROWS.csv"
CSV_3829_BOUNDS = OUT / "P8_Y5_R2FR_3829_GAMMA_BETA_COEFFICIENT_BOUND_ROWS.csv"
CSV_3828_RESIDUAL = OUT / "P8_Y5_R2FR_3828_RESIDUAL_VECTOR_BOUND.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3835_SOURCE_REGISTER.csv",
    "ledger": OUT / "P8_Y5_R2FR_3835_GAMMA_NO_SLIP_LEDGER.csv",
    "dashboard": OUT / "P8_Y5_R2FR_3835_GAMMA_THRESHOLD_DASHBOARD.csv",
    "queue": OUT / "P8_Y5_R2FR_3835_GAMMA_SOURCE_FILL_QUEUE.csv",
    "local_status": OUT / "P8_Y5_R2FR_3835_LOCAL_TEST_STATUS.csv",
    "gates": OUT / "P8_Y5_R2FR_3835_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3835_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3835_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3835_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3835_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3835_0_3834_doc", P_3834, "Boundary/Harmonic Scalar Slip Zero Or Gamma Bound"),
    ("SRC3835_1_3834_boundary", CSV_3834_BOUNDS, "BGB3834_0_boundary"),
    ("SRC3835_2_3834_validation", CSV_3834_VALIDATION, "VAL3834_2_components"),
    ("SRC3835_3_3833_parent", CSV_3833_BOUNDS, "PGB3833_0_parent_extra"),
    ("SRC3835_4_3832_matter", CSV_3832_GAMMA, "GUP3832_0_matter_TF_update"),
    ("SRC3835_5_3831_sigmatf", CSV_3831_BOUNDS, "BTF3831_0_matter_total"),
    ("SRC3835_6_3830_gamma", CSV_3830_GAMMA, "GB3830_1_gamma_total"),
    ("SRC3835_7_3829_gamma", CSV_3829_BOUNDS, "BND3829_1_gamma"),
    ("SRC3835_8_3828_gamma", CSV_3828_RESIDUAL, "RPPN3828_0_gamma"),
]


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
                "role": "input_for_integrated_gamma_no_slip_dashboard",
                "claim_use": "threshold_dashboard_only_not_claim",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def ledger_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "component_id": "GLED3835_0_matter_TF",
            "component": "B_gamma_matter_TF",
            "formula": "B_gamma_matter_TF <= K_TF*(epsilon_ext_TF + epsilon_quad_TF + epsilon_apparatus_TF + epsilon_tensor_virial_TF + epsilon_EM_Poynting_TF)",
            "source_artifact": rel(CSV_3832_GAMMA),
            "status": "FORMULA_ONLY_NONCLAIM",
            "claim_blocker": "MISSING_NUMERIC_SIGMATF_SOURCE_ROWS",
            "priority": 1,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "GLED3835_1_parent_extra",
            "component": "B_gamma_parent_extra",
            "formula": "B_gamma_parent_extra <= B_disformal_slip + B_hidden_coeff_slip + B_readout_rep_slip + B_parent_metric_nonuniqueness",
            "source_artifact": rel(CSV_3833_BOUNDS),
            "status": "FORMULA_ONLY_NONCLAIM",
            "claim_blocker": "MISSING_PARENT_SINGLE_METRIC_READOUT_SIGNATURE_OR_NUMERIC_BOUNDS",
            "priority": 2,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "GLED3835_2_boundary",
            "component": "B_gamma_boundary",
            "formula": "B_gamma_boundary <= B_Dirichlet_slip + B_Neumann_slip + B_harmonic_l2 + B_Bzero_flux_slip + B_Delta_symp_slip",
            "source_artifact": rel(CSV_3834_BOUNDS),
            "status": "FORMULA_ONLY_NONCLAIM",
            "claim_blocker": "MISSING_SCALAR_SLIP_BOUNDARY_ROWS",
            "priority": 3,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "GLED3835_3_readout_direct",
            "component": "B_gamma_readout",
            "formula": "B_gamma_readout <= B_metric_projection + B_arena_readout_tail + B_clock_or_PPN_projection",
            "source_artifact": rel(CSV_3828_RESIDUAL),
            "status": "PLACEHOLDER_FORMULA_NONCLAIM",
            "claim_blocker": "MISSING_DIRECT_GAMMA_READOUT_RESIDUAL_ROWS",
            "priority": 4,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "GLED3835_4_eps_spatial",
            "component": "abs(eps_spatial/Phi)",
            "formula": "eps_spatial/Phi = residual spatial-metric readout tail outside C_s Phi",
            "source_artifact": rel(CSV_3828_RESIDUAL),
            "status": "PLACEHOLDER_FORMULA_NONCLAIM",
            "claim_blocker": "MISSING_EPS_SPATIAL_SOURCE_OR_ZERO_ROW",
            "priority": 5,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "GLED3835_5_total",
            "component": "B_gamma_total",
            "formula": "abs(gamma-1) <= B_gamma_matter_TF + B_gamma_parent_extra + B_gamma_boundary + B_gamma_readout + abs(eps_spatial/Phi)",
            "source_artifact": rel(CSV_3834_BOUNDS),
            "status": "INTEGRATED_NONCLAIM_LEDGER",
            "claim_blocker": "ALL_COMPONENTS_REQUIRE_ZERO_OR_SOURCE_BACKED_NUMERIC_BOUNDS_BELOW_THRESHOLD",
            "priority": 0,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def dashboard_rows(timestamp: str) -> list[dict[str, object]]:
    threshold_symbol = "theta_gamma_local"
    return [
        {
            "dashboard_id": "GDASH3835_0_threshold",
            "item": "gamma threshold",
            "current_value": "MISSING_NUMERIC_THRESHOLD",
            "threshold_symbol": threshold_symbol,
            "threshold_source": "MISSING_SOURCE_ROW_FOR_LOCAL_PPN_GAMMA_LIMIT",
            "test_status": "BLOCKED_THRESHOLD_SOURCE_REQUIRED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "dashboard_id": "GDASH3835_1_total_bound",
            "item": "B_gamma_total",
            "current_value": "FORMULA_ONLY",
            "threshold_symbol": threshold_symbol,
            "threshold_source": "requires numeric component bounds and sourced gamma limit",
            "test_status": "BLOCKED_NUMERIC_COMPONENTS_REQUIRED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "dashboard_id": "GDASH3835_2_pass_rule",
            "item": "local gamma pass rule",
            "current_value": "PASS iff B_gamma_total <= theta_gamma_local with all component rows valid_for_claim=true",
            "threshold_symbol": threshold_symbol,
            "threshold_source": "not yet sourced",
            "test_status": "RULE_DEFINED_NONCLAIM",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "dashboard_id": "GDASH3835_3_current_verdict",
            "item": "current gamma verdict",
            "current_value": "BLOCKED_NONCLAIM",
            "threshold_symbol": threshold_symbol,
            "threshold_source": "missing threshold and missing numeric component rows",
            "test_status": "BLOCKED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def queue_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "priority": 1,
            "queue_id": "GQ3835_0_gamma_threshold_source",
            "target": "theta_gamma_local",
            "needed_row": "source-backed local PPN gamma limit with units/CL/provenance",
            "why": "the dashboard cannot compare formula bounds without a declared sourced threshold",
            "feeds": "gamma dashboard numeric gate",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "priority": 2,
            "queue_id": "GQ3835_1_direct_readout_eps",
            "target": "B_gamma_readout + eps_spatial/Phi",
            "needed_row": "derive zero or source-bound direct spatial metric/readout residual",
            "why": "this is the least developed remaining gamma component",
            "feeds": "3836",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "priority": 3,
            "queue_id": "GQ3835_2_matter_EM_numbers",
            "target": "B_gamma_matter_TF",
            "needed_row": "numeric/source-backed SigmaTF matter/EM/Poynting components",
            "why": "Poynting is now formal but not quantified",
            "feeds": "local gamma smoke v2",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "priority": 4,
            "queue_id": "GQ3835_3_parent_boundary_numbers",
            "target": "B_gamma_parent_extra + B_gamma_boundary",
            "needed_row": "parent readout signature or bounds plus scalar-slip boundary rows",
            "why": "these are theorem-zero candidates if parent/boundary signatures close",
            "feeds": "local gamma smoke v2",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def local_status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "arena_id": "LOCAL_GAMMA_3835",
            "arena": "PPN gamma / no-slip",
            "formula_status": "STRUCTURALLY_INTEGRATED",
            "numeric_status": "NO_NUMERIC_PASS",
            "claim_allowed": False,
            "reason": "component bounds and threshold are not source-backed",
            "next_action": "derive/source B_gamma_readout and eps_spatial/Phi, then add sourced gamma threshold",
            "timestamp_utc": timestamp,
        },
        {
            "arena_id": "LOCAL_GR_3835",
            "arena": "local GR recovery",
            "formula_status": "PARTIAL_GAMMA_ONLY",
            "numeric_status": "BLOCKED_BETA_AND_GAMMA_COMPONENTS",
            "claim_allowed": False,
            "reason": "gamma dashboard is nonclaim; beta second-order vertex remains open",
            "next_action": "finish direct gamma readout rows, then return to beta S_beta branch",
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3835_0_integrated_ledger",
            "gate": "integrated gamma ledger exists",
            "status": "PASS_NONCLAIM",
            "claim_allowed": False,
            "reason": "matter, parent-extra, boundary, readout, eps_spatial, and total rows emitted",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3835_1_threshold_dashboard",
            "gate": "threshold dashboard exists",
            "status": "PASS_RULE_DEFINED_NONCLAIM",
            "claim_allowed": False,
            "reason": "pass rule exists but threshold and component rows are not source-backed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3835_2_gamma_claim",
            "gate": "gamma/no-slip claim",
            "status": "BLOCKED_NUMERIC_AND_SOURCE_ROWS_REQUIRED",
            "claim_allowed": False,
            "reason": "B_gamma_total is formula-only and theta_gamma_local is missing sourced value",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3835_3_local_GR_claim",
            "gate": "local GR claim",
            "status": "BLOCKED",
            "claim_allowed": False,
            "reason": "gamma is nonclaim and beta S_beta remains open",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3835_4_next_target",
            "gate": "next target fills direct gamma readout residuals",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "direct readout/eps_spatial is the least developed remaining gamma component",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3835_0_gamma_structural_success",
            "decision": "gamma/no-slip branch is structurally integrated but not claimable",
            "basis": "all major components now have named formula rows and blockers",
            "consequence": "future gamma work should source/fill rows rather than add more prose derivation fragments",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3835_1_no_threshold_smuggling",
            "decision": "do not insert an unsourced numeric PPN threshold",
            "basis": "the dashboard requires a source-backed threshold row before pass/fail claims",
            "consequence": "gamma remains blocked until threshold provenance and component values are real",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3835_2_next_gamma_gap",
            "decision": "fill direct readout and eps_spatial residuals next",
            "basis": "matter/EM, parent-extra, and boundary components are already decomposed; direct readout tail is still placeholder-level",
            "consequence": "3836 should attack B_gamma_readout and eps_spatial/Phi",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3835_0",
            "next_checkpoint": "3836-Y5-R2FR-direct-gamma-readout-eps-spatial-zero-or-source-bound.md",
            "script": "scripts/Y5_R2FR_3836_direct_gamma_readout_eps_spatial_zero_or_source_bound.py",
            "objective": "derive or source-bound B_gamma_readout and eps_spatial/Phi, the remaining direct spatial/readout gamma residuals in the integrated no-slip ledger",
            "reason": "3835 integrates the gamma ledger and shows direct readout/eps_spatial rows are the least developed remaining gamma components",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_INTEGRATED_GAMMA_DASHBOARD",
            "claim": "no gamma/no-slip/local-GR claim",
            "summary": "3835 integrates gamma/no-slip bound components into one dashboard and threshold rule while keeping all claims blocked.",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("|", "\\|") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(sources, ledger, dashboard, queue, local_status, gates, decisions, timestamp: str) -> None:
    text = f"""# 3835 — Integrated Gamma No-Slip Ledger And First Threshold Dashboard

Private checkpoint. This integrates the gamma/no-slip branch into one dashboard. It does not claim `gamma=1`.

Generated: `{timestamp}`

## Result

The integrated gamma bound is now:

`abs(gamma-1) <= B_gamma_matter_TF + B_gamma_parent_extra + B_gamma_boundary + B_gamma_readout + abs(eps_spatial/Phi)`.

The pass rule is also explicit:

`PASS iff B_gamma_total <= theta_gamma_local` and every component row plus the threshold row is source-backed and `valid_for_claim=true`.

Current verdict: `BLOCKED_NONCLAIM`. The formula is structured; the numbers and source rows are not.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Gamma No-Slip Ledger

{markdown_table(ledger, ["component_id", "component", "formula", "status", "claim_blocker"])}

## Threshold Dashboard

{markdown_table(dashboard, ["dashboard_id", "item", "current_value", "threshold_symbol", "test_status", "claim_allowed"])}

## Source Fill Queue

{markdown_table(queue, ["priority", "queue_id", "target", "needed_row", "feeds"])}

## Local Test Status

{markdown_table(local_status, ["arena_id", "arena", "formula_status", "numeric_status", "claim_allowed", "next_action"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

This is a useful checkpoint because the gamma branch has stopped being a forest of separate proof fragments. It is now a single ledger with a pass rule. The next gap is not philosophical: fill or derive `B_gamma_readout` and `eps_spatial/Phi`, then source the actual local gamma threshold.

Next target: `3836-Y5-R2FR-direct-gamma-readout-eps-spatial-zero-or-source-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3834", "Current State After 3835", 1)
    paragraph = (
        "`3835` integrates the gamma/no-slip branch into one nonclaim dashboard: "
        "`|gamma-1| <= B_gamma_matter_TF+B_gamma_parent_extra+B_gamma_boundary+B_gamma_readout+|eps_spatial/Phi|`. "
        "The pass rule is explicit but blocked: `B_gamma_total <= theta_gamma_local` only counts when every component row and the threshold row is source-backed and `valid_for_claim=true`. "
        "This makes gamma structurally test-ready, with direct readout/`eps_spatial` and threshold sourcing as the next gaps.\n\n"
    )
    anchor = "`3834` specializes"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3835-Y5-R2FR-integrated-gamma-no-slip-ledger-and-first-threshold-dashboard.md`

Target: integrate matter/EM, parent-extra, boundary, readout, and `eps_spatial` gamma rows into one no-slip ledger with source/numeric thresholds and claim-blocked local test status.

This is the best next move because 3834 gives the last major boundary/harmonic gamma bound component; the project needs one integrated gamma dashboard before more local tests."""
    new_gate = """`3836-Y5-R2FR-direct-gamma-readout-eps-spatial-zero-or-source-bound.md`

Target: derive or source-bound `B_gamma_readout` and `eps_spatial/Phi`, the remaining direct spatial/readout gamma residuals in the integrated no-slip ledger.

This is the best next move because 3835 integrates the gamma ledger and shows direct readout/`eps_spatial` rows are the least developed remaining gamma components."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3835_GAMMA_NO_SLIP_LEDGER.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3835_GAMMA_THRESHOLD_DASHBOARD.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3835_GAMMA_SOURCE_FILL_QUEUE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3835_LOCAL_TEST_STATUS.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3835_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3835_GAMMA_NO_SLIP_LEDGER.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    if f"Generated by 3835 at {timestamp}" not in text:
        text = text.rstrip() + f"\n\n<!-- Generated by 3835 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(sources, ledger, dashboard, queue, local_status, gates, timestamp: str):
    rows = []

    def add(check_id, check, passed, detail):
        rows.append({"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "detail": detail, "timestamp_utc": timestamp})

    all_text = " ".join(str(row) for row in ledger + dashboard + queue + local_status + gates)
    add("VAL3835_0_sources", "all cited source paths exist and needles are found", all(row["exists"] and row["needle_found"] for row in sources), f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved")
    add("VAL3835_1_components", "integrated gamma ledger has all five components plus total", all(token in all_text for token in ["B_gamma_matter_TF", "B_gamma_parent_extra", "B_gamma_boundary", "B_gamma_readout", "eps_spatial/Phi", "B_gamma_total"]), "gamma component tokens present")
    add("VAL3835_2_threshold_rule", "threshold pass rule exists and remains blocked", any(row["dashboard_id"] == "GDASH3835_2_pass_rule" for row in dashboard) and any(row["dashboard_id"] == "GDASH3835_3_current_verdict" and row["test_status"] == "BLOCKED" for row in dashboard), "pass rule and blocked verdict present")
    add("VAL3835_3_nonclaim", "all 3835 rows remain nonclaim", all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in ledger + dashboard + queue + local_status + gates), "valid_for_claim/claim_allowed false throughout")
    add("VAL3835_4_local_status", "local gamma and local GR statuses are present", {"LOCAL_GAMMA_3835", "LOCAL_GR_3835"} == {row["arena_id"] for row in local_status}, "local status rows present")
    add("VAL3835_5_next_gap", "source-fill queue targets direct readout and eps_spatial", any("eps_spatial" in row["target"] for row in queue), "direct readout/eps target present")
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            parsed = len(read_csv_rows(output_path)) > 0
            detail += f" rows={len(read_csv_rows(output_path))}"
        add(f"VAL3835_6_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add("VAL3835_7_doc", "markdown checkpoint document exists", DOC_PATH.exists() and "B_gamma_total" in read_text(DOC_PATH), rel(DOC_PATH))
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3835*", "P8_Y5_BRR545_3835*", "*Y5_R2FR_3835*", "3835-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add("VAL3835_8_formalization_clean", "formalization-workbench has no 3835 files", len(fwb_hits) == 0, "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3835 file hits under formalization-workbench")
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add("VAL3835_9_pycache_removed", "scripts __pycache__ removed", len(pycache_hits) == 0, "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories")
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    ledger = ledger_rows(timestamp)
    dashboard = dashboard_rows(timestamp)
    queue = queue_rows(timestamp)
    local_status = local_status_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["ledger"], ledger)
    write_csv(OUTPUTS["dashboard"], dashboard)
    write_csv(OUTPUTS["queue"], queue)
    write_csv(OUTPUTS["local_status"], local_status)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, ledger, dashboard, queue, local_status, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, ledger, dashboard, queue, local_status, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_INTEGRATED_GAMMA_DASHBOARD")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

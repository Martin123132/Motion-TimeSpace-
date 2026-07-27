from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3842"
BRANCH = "MTS_R2FR_Y5_EPS_TEMPORAL4_ORDER_GAUGE_DOMAIN_ZERO_OR_BETA_BOUND_3842"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3842-Y5-R2FR-eps-temporal4-order-gauge-domain-zero-or-beta-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3841 = PCW / "3841-Y5-R2FR-second-order-temporal-readout-projection-naturality-zero-or-beta-bound.md"
P_3837 = PCW / "3837-Y5-R2FR-beta-second-order-vertex-Sbeta-zero-or-bound.md"
CSV_3841_BETA = OUT / "P8_Y5_R2FR_3841_BETA_BOUND_UPDATE.csv"
CSV_3841_VALIDATION = OUT / "P8_Y5_BRR545_3841_VALIDATION.csv"
CSV_3837_EPS = OUT / "P8_Y5_R2FR_3837_EPS_TEMPORAL4_BOUND_ROWS.csv"
CSV_3837_BETA = OUT / "P8_Y5_R2FR_3837_BETA_BOUND_ROWS.csv"
CSV_3828_ANSATZ = OUT / "P8_Y5_R2FR_3828_PPN_READOUT_ANSATZ.csv"
CSV_3828_RESIDUAL = OUT / "P8_Y5_R2FR_3828_RESIDUAL_VECTOR_BOUND.csv"
CSV_3828_ZERO = OUT / "P8_Y5_R2FR_3828_ZERO_CONDITION_THEOREM.csv"
CSV_3836_EPS_SPATIAL = OUT / "P8_Y5_R2FR_3836_EPS_SPATIAL_ZERO_OR_BOUND_ROWS.csv"
CSV_3818_POISSON = OUT / "P8_Y5_R2FR_3818_WEAK_FIELD_POISSON_DERIVATION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3842_SOURCE_REGISTER.csv",
    "zero_audit": OUT / "P8_Y5_R2FR_3842_EPS_TEMPORAL4_ZERO_AUDIT.csv",
    "decomposition": OUT / "P8_Y5_R2FR_3842_EPS_TEMPORAL4_DECOMPOSITION.csv",
    "beta_update": OUT / "P8_Y5_R2FR_3842_BETA_BOUND_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3842_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3842_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3842_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3842_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3842_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3842_0_3841_doc", P_3841, "Second-Order Temporal Readout"),
    ("SRC3842_1_3841_beta", CSV_3841_BETA, "BUP3841_1_beta_total"),
    ("SRC3842_2_3841_validation", CSV_3841_VALIDATION, "VAL3841_6_sbeta_structural_completion"),
    ("SRC3842_3_3837_doc", P_3837, "eps_temporal4 Bound Rows"),
    ("SRC3842_4_3837_eps", CSV_3837_EPS, "ET43837_3_total"),
    ("SRC3842_5_3837_beta", CSV_3837_BETA, "BB3837_1_beta"),
    ("SRC3842_6_3828_ansatz", CSV_3828_ANSATZ, "ANS3828_0_Newtonian_temporal"),
    ("SRC3842_7_3828_residual", CSV_3828_RESIDUAL, "RPPN3828_1_beta"),
    ("SRC3842_8_3828_zero", CSV_3828_ZERO, "ZPPN3828_2_beta_lock"),
    ("SRC3842_9_3836_eps_spatial", CSV_3836_EPS_SPATIAL, "EPS3836_4_total"),
    ("SRC3842_10_3818_poisson", CSV_3818_POISSON, "POI3818_0_linearized_00"),
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
                "role": "input_for_eps_temporal4_order_gauge_domain_zero_or_beta_bound",
                "claim_use": "eps_temporal4_zero_or_bound_audit_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def zero_audit_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "ET4A3842_0_target_sharp",
            "requirement": "abs(eps_temporal4/Phi^2) is the remaining beta envelope term after all S_beta components have ledgers",
            "test": "BUP3841_1_beta_total and ET43837_3_total both contain eps_temporal4",
            "current_status": "PASS_TARGET_SHARP",
            "if_failed": "integrated beta ledger would miss non-S_beta temporal tails",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ET4A3842_1_no_order_smuggle",
            "requirement": "higher-order temporal terms beyond Phi^2 are not ignored or fitted into beta",
            "test": "PPN order separation requires O(Phi^3), source velocity, and 2PN/3PN tails below beta budget",
            "current_status": "ORDER_BOUND_REQUIRED",
            "if_failed": "retain B_eps_temporal_order",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ET4A3842_2_gauge_fixed",
            "requirement": "coordinate/gauge terms in g00 at beta extraction order are fixed or gauge-invariantly removed",
            "test": "declared PPN gauge and beta extraction are invariant under remaining coordinate freedom",
            "current_status": "GAUGE_FIX_SIGNATURE_REQUIRED",
            "if_failed": "retain B_eps_temporal_gauge",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ET4A3842_3_domain_limit",
            "requirement": "finite-domain/exterior cutoff does not shift the temporal Phi^2 coefficient",
            "test": "asymptotic/local exterior limit or source-backed finite-domain correction for g00/Phi^2",
            "current_status": "DOMAIN_BOUND_REQUIRED",
            "if_failed": "retain B_eps_temporal_domain",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ET4A3842_4_nonlinear_tail",
            "requirement": "nonlinear cross-sector temporal tails are assigned to named S_beta components or bounded separately",
            "test": "no unassigned matter/EM/scalar/boundary/readout cross-term remains in eps_temporal4",
            "current_status": "NONLINEAR_TAIL_BOUND_REQUIRED",
            "if_failed": "retain B_eps_temporal_nonlinear",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ET4A3842_5_multipole_motion",
            "requirement": "source multipoles, tides, motion, and preferred-frame terms do not contaminate scalar beta extraction",
            "test": "monopole/static local PPN projection is declared, or finite multipole/vector/time-dependence row is supplied",
            "current_status": "MULTIPOLE_MOTION_BOUND_REQUIRED",
            "if_failed": "retain B_eps_temporal_multipole_motion",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ET4A3842_6_normalization_floor",
            "requirement": "division by Phi^2 is safe on the claimed local domain",
            "test": "positive potential floor or restricted domain prevents eps/Phi^2 blow-up",
            "current_status": "PHI2_DENOMINATOR_GUARD_REQUIRED",
            "if_failed": "retain B_eps_temporal_denominator",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ET4A3842_7_verdict",
            "requirement": "all eps_temporal4 silence clauses close simultaneously",
            "test": "ET4A3842_1 through ET4A3842_6 all parent-signed or source-backed below threshold",
            "current_status": "EPS_TEMPORAL4_ZERO_NOT_CLAIMED",
            "if_failed": "eps_temporal4 remains a beta envelope residual rather than a hidden truncation assumption",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decomposition_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "component_id": "ET4M3842_0_order",
            "component": "B_eps_temporal_order",
            "definition": "temporal metric terms beyond beta-order Phi^2 truncation, including O(Phi^3) and higher PN terms",
            "zero_route": "strict PPN order separation and small-potential domain bound make O(Phi^3)/Phi^2 negligible",
            "bound_formula": "B_eps_temporal_order <= C_order * sup_domain abs(Phi) + O(Phi^2)",
            "status": "ORDER_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "ET4M3842_1_gauge",
            "component": "B_eps_temporal_gauge",
            "definition": "coordinate/gauge contribution to g00 at beta extraction order",
            "zero_route": "fixed PPN gauge and gauge-invariant beta extraction before fitting",
            "bound_formula": "B_eps_temporal_gauge <= abs(R_gauge_g00/Phi^2)",
            "status": "GAUGE_FIX_SIGNATURE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "ET4M3842_2_domain",
            "component": "B_eps_temporal_domain",
            "definition": "finite-radius/exterior-domain correction in temporal self-coupling",
            "zero_route": "asymptotic/local exterior limit or source-backed finite-domain correction",
            "bound_formula": "B_eps_temporal_domain <= abs(R_domain_g00/Phi^2)",
            "status": "DOMAIN_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "ET4M3842_3_nonlinear_tail",
            "component": "B_eps_temporal_nonlinear",
            "definition": "unassigned nonlinear matter/EM/scalar/boundary/readout temporal cross-term outside S_beta ledgers",
            "zero_route": "every nonlinear beta-order term is assigned to EH2, scalar2, boundary2, or readout2, with no leftover",
            "bound_formula": "B_eps_temporal_nonlinear <= abs(R_unassigned_temporal_cross/Phi^2)",
            "status": "NONLINEAR_TAIL_ASSIGNMENT_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "ET4M3842_4_multipole_motion",
            "component": "B_eps_temporal_multipole_motion",
            "definition": "source multipole, tidal, velocity, or preferred-frame temporal residue contaminating scalar beta extraction",
            "zero_route": "declared monopole/static local PPN projection or sourced multipole/vector/time-dependence row",
            "bound_formula": "B_eps_temporal_multipole_motion <= abs(R_multipole_tidal_velocity_g00/Phi^2)",
            "status": "MULTIPOLE_MOTION_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "ET4M3842_5_denominator",
            "component": "B_eps_temporal_denominator",
            "definition": "unsafe division by Phi^2 near zeros or outside the calibrated local exterior domain",
            "zero_route": "positive Phi floor/domain restriction or normed beta extraction denominator",
            "bound_formula": "B_eps_temporal_denominator <= eps_temporal4_norm/max(Phi_floor^2, Phi_ref^2)",
            "status": "PHI2_DENOMINATOR_GUARD_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "component_id": "ET4M3842_6_total",
            "component": "abs(eps_temporal4/Phi^2)",
            "definition": "total temporal residual outside the B_t Phi^2 beta-order readout",
            "zero_route": "all temporal residual components vanish or are below beta threshold budget",
            "bound_formula": "abs(eps_temporal4/Phi^2) <= B_eps_temporal_order + B_eps_temporal_gauge + B_eps_temporal_domain + B_eps_temporal_nonlinear + B_eps_temporal_multipole_motion + B_eps_temporal_denominator",
            "status": "FIRST_EPS_TEMPORAL4_DECOMPOSED_BOUND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def beta_update_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "BUP3842_0_eps_temporal4_update",
            "observable": "abs(eps_temporal4/Phi^2)",
            "formula": "abs(eps_temporal4/Phi^2) <= B_eps_temporal_order + B_eps_temporal_gauge + B_eps_temporal_domain + B_eps_temporal_nonlinear + B_eps_temporal_multipole_motion + B_eps_temporal_denominator",
            "new_detail": "eps_temporal4 is decomposed into order, gauge, domain, nonlinear-tail, multipole/motion, and denominator-guard channels",
            "status": "UPDATED_NONCLAIM_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BUP3842_1_beta_total",
            "observable": "beta-1",
            "formula": "abs(beta-1) <= B_EH2_vertex + B_extra_scalar2 + B_boundary2 + B_readout2 + B_eps_temporal_order + B_eps_temporal_gauge + B_eps_temporal_domain + B_eps_temporal_nonlinear + B_eps_temporal_multipole_motion + B_eps_temporal_denominator",
            "new_detail": "beta envelope is structurally complete: four S_beta ledgers plus decomposed eps_temporal4, all nonclaim pending source/theorem closure",
            "status": "STRUCTURALLY_COMPLETE_NONCLAIM_BETA_LEDGER",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "GATE3842_0_target_trace",
            "gate": "eps_temporal4 term traced to beta envelope",
            "status": "PASS_TARGET_SHARP",
            "claim_allowed": False,
            "reason": "eps_temporal4 is the remaining beta envelope term after S_beta component ledgers",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3842_1_no_truncation_smuggle",
            "gate": "higher-order/gauge/domain tails are not ignored",
            "status": "PASS_GUARD",
            "claim_allowed": False,
            "reason": "eps_temporal4 is decomposed rather than dropped from the beta claim",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3842_2_eps_temporal4_zero",
            "gate": "eps_temporal4 zero theorem",
            "status": "BLOCKED_ORDER_GAUGE_DOMAIN_SOURCE_ROWS_REQUIRED",
            "claim_allowed": False,
            "reason": "order, gauge, domain, nonlinear-tail, multipole/motion, and denominator guards are not source-backed",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3842_3_eps_temporal4_bound",
            "gate": "eps_temporal4 finite beta bound",
            "status": "PASS_FORMULA_ONLY_NONCLAIM",
            "claim_allowed": False,
            "reason": "bound formula exists but numeric/source-backed rows are not supplied",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3842_4_beta_claim",
            "gate": "beta/local PPN claim",
            "status": "BLOCKED_STRUCTURALLY_COMPLETE_NONCLAIM",
            "claim_allowed": False,
            "reason": "beta ledger is structurally complete but every component is still theorem-conditional or source-bound nonclaim",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3842_5_next_target",
            "gate": "next target builds integrated beta dashboard",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "all beta envelope terms have ledgers; next step is integrated threshold/dashboard gating",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3842_0_no_truncation_claim",
            "decision": "do not claim beta from S_beta closure while eps_temporal4 remains unbounded",
            "basis": "3837 beta formula includes eps_temporal4/Phi^2 as a separate envelope term",
            "consequence": "beta remains nonclaim until order/gauge/domain/tail rows are zeroed or bounded",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3842_1_beta_structural_completion",
            "decision": "treat beta as structurally decomposed but not proven",
            "basis": "EH2, scalar2, boundary2, readout2, and eps_temporal4 all now have explicit ledgers",
            "consequence": "next work can build threshold dashboards instead of inventing more beta categories",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3842_2_next_integrated_beta_dashboard",
            "decision": "move next to integrated beta ledger and source-fill dashboard",
            "basis": "all beta envelope terms are formulated as zero-or-bound components",
            "consequence": "3843 should report which components need theorem signatures, numeric source rows, or can be tested first",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3842_0",
            "next_checkpoint": "3843-Y5-R2FR-integrated-beta-ledger-threshold-dashboard-and-source-fill-queue.md",
            "script": "scripts/Y5_R2FR_3843_integrated_beta_ledger_threshold_dashboard_and_source_fill_queue.py",
            "objective": "combine EH2, scalar2, boundary2, readout2, and eps_temporal4 rows into an integrated beta/local-PPN dashboard with source-fill priorities",
            "reason": "3842 makes the beta envelope structurally complete but nonclaim",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_EPS_TEMPORAL4_BOUND_CONTRACT",
            "claim": "no beta/local-GR claim",
            "summary": "3842 decomposes eps_temporal4 into order, gauge, domain, nonlinear-tail, multipole/motion, and denominator residuals, completing the structural beta envelope.",
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


def write_doc(sources, zero_audit, decomposition, beta_update, gates, decisions, timestamp: str) -> None:
    text = f"""# 3842 - eps_temporal4 Order Gauge Domain Zero Or Beta Bound

Private checkpoint. This attacks `abs(eps_temporal4/Phi^2)`, the remaining beta-envelope term after all four `S_beta` components have ledgers. It does not claim `beta=1` or local GR.

Generated: `{timestamp}`

## Result

3842 blocks the shortcut:

`S_beta structurally decomposed != beta closed if eps_temporal4 is unbounded`.

The retained eps bound is:

`abs(eps_temporal4/Phi^2) <= B_eps_temporal_order + B_eps_temporal_gauge + B_eps_temporal_domain + B_eps_temporal_nonlinear + B_eps_temporal_multipole_motion + B_eps_temporal_denominator`.

Therefore the structurally complete beta envelope is:

`abs(beta-1) <= B_EH2_vertex + B_extra_scalar2 + B_boundary2 + B_readout2 + B_eps_temporal_order + B_eps_temporal_gauge + B_eps_temporal_domain + B_eps_temporal_nonlinear + B_eps_temporal_multipole_motion + B_eps_temporal_denominator`.

Current result: beta is structurally decomposed, not proven. Every component still needs a parent zero signature, a source-backed numeric row, or a threshold/dashboard decision.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## eps_temporal4 Zero Audit

{markdown_table(zero_audit, ["audit_id", "requirement", "test", "current_status", "if_failed"])}

## eps_temporal4 Decomposition

{markdown_table(decomposition, ["component_id", "component", "definition", "zero_route", "status"])}

## Beta Bound Update

{markdown_table(beta_update, ["row_id", "observable", "formula", "status"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

This is the first point where the beta/local-PPN branch is structurally complete: EH2, extra scalar2, boundary2, readout2, and eps_temporal4 are all explicit. It is not a pass. It is now ready for an integrated source-fill/threshold dashboard instead of more category hunting.

Next target: `3843-Y5-R2FR-integrated-beta-ledger-threshold-dashboard-and-source-fill-queue.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3841", "Current State After 3842", 1)
    paragraph = (
        "`3842` decomposes the remaining beta-envelope term `eps_temporal4`. "
        "The retained bound is `|eps_temporal4/Phi^2| <= B_eps_temporal_order+B_eps_temporal_gauge+B_eps_temporal_domain+B_eps_temporal_nonlinear+B_eps_temporal_multipole_motion+B_eps_temporal_denominator`, "
        "so beta is now structurally `|beta-1| <= B_EH2_vertex+B_extra_scalar2+B_boundary2+B_readout2+B_eps_temporal_order+B_eps_temporal_gauge+B_eps_temporal_domain+B_eps_temporal_nonlinear+B_eps_temporal_multipole_motion+B_eps_temporal_denominator`. "
        "No beta/local-GR claim is made, but the beta ledger is now structurally complete and ready for threshold/source-fill gating.\n\n"
    )
    anchor = "`3841` specializes"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3842-Y5-R2FR-eps-temporal4-order-gauge-domain-zero-or-beta-bound.md`

Target: decompose `abs(eps_temporal4/Phi^2)` into order, gauge, domain, and nonlinear-tail residuals, or source-bound it.

This is the best next move because 3841 formulates readout2; all `S_beta` components now have ledgers and `eps_temporal4` is the remaining beta envelope term."""
    new_gate = """`3843-Y5-R2FR-integrated-beta-ledger-threshold-dashboard-and-source-fill-queue.md`

Target: combine EH2, scalar2, boundary2, readout2, and eps_temporal4 rows into an integrated beta/local-PPN dashboard with source-fill priorities.

This is the best next move because 3842 makes the beta envelope structurally complete but nonclaim."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3842_EPS_TEMPORAL4_ZERO_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3842_EPS_TEMPORAL4_DECOMPOSITION.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3842_BETA_BOUND_UPDATE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3842_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3842_EPS_TEMPORAL4_ZERO_AUDIT.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    if f"Generated by 3842 at {timestamp}" not in text:
        text = text.rstrip() + f"\n\n<!-- Generated by 3842 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(sources, zero_audit, decomposition, beta_update, gates, timestamp: str) -> list[dict[str, object]]:
    rows = []

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

    all_text = " ".join(str(row) for row in zero_audit + decomposition + beta_update + gates)
    add(
        "VAL3842_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3842_1_target_trace",
        "eps_temporal4 is traced from existing beta envelope",
        "eps_temporal4" in all_text and "BUP3842_1_beta_total" in all_text,
        "target term present in zero audit and beta update",
    )
    add(
        "VAL3842_2_no_truncation_guard",
        "S_beta structural closure is not promoted to beta without eps bound",
        "S_beta structurally decomposed" in read_text(DOC_PATH) and any(row["gate_id"] == "GATE3842_1_no_truncation_smuggle" for row in gates),
        "truncation guard present",
    )
    add(
        "VAL3842_3_components",
        "eps_temporal4 components are decomposed",
        all(
            token in all_text
            for token in [
                "B_eps_temporal_order",
                "B_eps_temporal_gauge",
                "B_eps_temporal_domain",
                "B_eps_temporal_nonlinear",
                "B_eps_temporal_multipole_motion",
                "B_eps_temporal_denominator",
                "abs(eps_temporal4/Phi^2)",
            ]
        ),
        "eps_temporal4 component tokens present",
    )
    add(
        "VAL3842_4_nonclaim",
        "all 3842 rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in zero_audit + decomposition + beta_update + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3842_5_eps_gate_blocked",
        "eps_temporal4 zero remains blocked",
        any(row["gate_id"] == "GATE3842_2_eps_temporal4_zero" and row["status"].startswith("BLOCKED") for row in gates),
        "eps_temporal4 zero gate blocked",
    )
    add(
        "VAL3842_6_beta_structural_complete",
        "beta formula includes all S_beta and eps components",
        all(token in all_text for token in ["B_EH2_vertex", "B_extra_scalar2", "B_boundary2", "B_readout2", "B_eps_temporal_order", "B_eps_temporal_denominator"]),
        "full beta envelope tokens present",
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
        add(f"VAL3842_7_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3842_8_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "eps_temporal4" in read_text(DOC_PATH) and "B_eps_temporal_order" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3842*", "P8_Y5_BRR545_3842*", "*Y5_R2FR_3842*", "3842-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3842_9_formalization_clean",
        "formalization-workbench has no 3842 files",
        len(fwb_hits) == 0,
        "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3842 file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3842_10_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows(timestamp)
    zero_audit = zero_audit_rows(timestamp)
    decomposition = decomposition_rows(timestamp)
    beta_update = beta_update_rows(timestamp)
    gates = gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["zero_audit"], zero_audit)
    write_csv(OUTPUTS["decomposition"], decomposition)
    write_csv(OUTPUTS["beta_update"], beta_update)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, zero_audit, decomposition, beta_update, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, zero_audit, decomposition, beta_update, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_EPS_TEMPORAL4_BOUND_CONTRACT")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

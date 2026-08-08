from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3843"
BRANCH = "MTS_R2FR_Y5_INTEGRATED_BETA_LEDGER_THRESHOLD_DASHBOARD_3843"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3843-Y5-R2FR-integrated-beta-ledger-threshold-dashboard-and-source-fill-queue.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3838 = PCW / "3838-Y5-R2FR-EH2-parent-second-variation-vertex-match-or-beta-bound.md"
P_3839 = PCW / "3839-Y5-R2FR-extra-scalar-quadratic-self-energy-zero-or-beta-bound.md"
P_3840 = PCW / "3840-Y5-R2FR-second-order-boundary-reference-temporal-self-coupling-zero-or-beta-bound.md"
P_3841 = PCW / "3841-Y5-R2FR-second-order-temporal-readout-projection-naturality-zero-or-beta-bound.md"
P_3842 = PCW / "3842-Y5-R2FR-eps-temporal4-order-gauge-domain-zero-or-beta-bound.md"

CSV_3838_DECOMP = OUT / "P8_Y5_R2FR_3838_EH2_MISMATCH_DECOMPOSITION.csv"
CSV_3839_DECOMP = OUT / "P8_Y5_R2FR_3839_SCALAR2_DECOMPOSITION.csv"
CSV_3840_DECOMP = OUT / "P8_Y5_R2FR_3840_BOUNDARY2_DECOMPOSITION.csv"
CSV_3841_DECOMP = OUT / "P8_Y5_R2FR_3841_READOUT2_DECOMPOSITION.csv"
CSV_3842_DECOMP = OUT / "P8_Y5_R2FR_3842_EPS_TEMPORAL4_DECOMPOSITION.csv"
CSV_3838_BETA = OUT / "P8_Y5_R2FR_3838_BETA_BOUND_UPDATE.csv"
CSV_3839_BETA = OUT / "P8_Y5_R2FR_3839_BETA_BOUND_UPDATE.csv"
CSV_3840_BETA = OUT / "P8_Y5_R2FR_3840_BETA_BOUND_UPDATE.csv"
CSV_3841_BETA = OUT / "P8_Y5_R2FR_3841_BETA_BOUND_UPDATE.csv"
CSV_3842_BETA = OUT / "P8_Y5_R2FR_3842_BETA_BOUND_UPDATE.csv"
CSV_3838_VALIDATION = OUT / "P8_Y5_BRR545_3838_VALIDATION.csv"
CSV_3839_VALIDATION = OUT / "P8_Y5_BRR545_3839_VALIDATION.csv"
CSV_3840_VALIDATION = OUT / "P8_Y5_BRR545_3840_VALIDATION.csv"
CSV_3841_VALIDATION = OUT / "P8_Y5_BRR545_3841_VALIDATION.csv"
CSV_3842_VALIDATION = OUT / "P8_Y5_BRR545_3842_VALIDATION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3843_SOURCE_REGISTER.csv",
    "ledger": OUT / "P8_Y5_R2FR_3843_INTEGRATED_BETA_LEDGER.csv",
    "threshold": OUT / "P8_Y5_R2FR_3843_BETA_THRESHOLD_CONTRACT.csv",
    "queue": OUT / "P8_Y5_R2FR_3843_SOURCE_FILL_QUEUE.csv",
    "gates": OUT / "P8_Y5_R2FR_3843_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3843_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3843_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3843_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3843_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3843_0_3838_doc", P_3838, "core beta question"),
    ("SRC3843_1_3839_doc", P_3839, "Extra Scalar Quadratic"),
    ("SRC3843_2_3840_doc", P_3840, "Boundary Reference"),
    ("SRC3843_3_3841_doc", P_3841, "Temporal Readout"),
    ("SRC3843_4_3842_doc", P_3842, "eps_temporal4"),
    ("SRC3843_5_3838_decomp", CSV_3838_DECOMP, "EH2M3838_4_total"),
    ("SRC3843_6_3839_decomp", CSV_3839_DECOMP, "SC2M3839_6_total"),
    ("SRC3843_7_3840_decomp", CSV_3840_DECOMP, "BD2M3840_7_total"),
    ("SRC3843_8_3841_decomp", CSV_3841_DECOMP, "RO2M3841_7_total"),
    ("SRC3843_9_3842_decomp", CSV_3842_DECOMP, "ET4M3842_6_total"),
    ("SRC3843_10_3838_beta", CSV_3838_BETA, "BUP3838_1_beta_total"),
    ("SRC3843_11_3839_beta", CSV_3839_BETA, "BUP3839_1_beta_total"),
    ("SRC3843_12_3840_beta", CSV_3840_BETA, "BUP3840_1_beta_total"),
    ("SRC3843_13_3841_beta", CSV_3841_BETA, "BUP3841_1_beta_total"),
    ("SRC3843_14_3842_beta", CSV_3842_BETA, "BUP3842_1_beta_total"),
    ("SRC3843_15_3838_validation", CSV_3838_VALIDATION, "PASS"),
    ("SRC3843_16_3839_validation", CSV_3839_VALIDATION, "PASS"),
    ("SRC3843_17_3840_validation", CSV_3840_VALIDATION, "PASS"),
    ("SRC3843_18_3841_validation", CSV_3841_VALIDATION, "PASS"),
    ("SRC3843_19_3842_validation", CSV_3842_VALIDATION, "PASS"),
]

DECOMPOSITION_SOURCES = [
    ("EH2", "B_EH2_vertex", CSV_3838_DECOMP),
    ("scalar2", "B_extra_scalar2", CSV_3839_DECOMP),
    ("boundary2", "B_boundary2", CSV_3840_DECOMP),
    ("readout2", "B_readout2", CSV_3841_DECOMP),
    ("eps_temporal4", "abs(eps_temporal4/Phi^2)", CSV_3842_DECOMP),
]

BETA_TOTAL_FORMULA = (
    "abs(beta-1) <= B_EH2_vertex + B_extra_scalar2 + B_boundary2 + B_readout2 "
    "+ B_eps_temporal_order + B_eps_temporal_gauge + B_eps_temporal_domain "
    "+ B_eps_temporal_nonlinear + B_eps_temporal_multipole_motion + B_eps_temporal_denominator"
)

BETA_TERMS = [
    "B_EH2_vertex",
    "B_extra_scalar2",
    "B_boundary2",
    "B_readout2",
    "B_eps_temporal_order",
    "B_eps_temporal_gauge",
    "B_eps_temporal_domain",
    "B_eps_temporal_nonlinear",
    "B_eps_temporal_multipole_motion",
    "B_eps_temporal_denominator",
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
                "role": "input_for_integrated_beta_ledger_threshold_dashboard",
                "claim_use": "nonclaim_dashboard_and_source_fill_queue_only",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def classify_dependency(component: str, status: str) -> tuple[str, str, str]:
    token = f"{component} {status}".lower()
    if any(key in token for key in ["l2_operator", "grav_energy", "second_variation", "non_eh"]):
        return (
            "P0",
            "parent_action_second_variation",
            "attacks the GR-reduction core instead of patching an arena residual",
        )
    if any(key in token for key in ["gauge", "readout", "projection", "field_redef"]):
        return (
            "P1",
            "single_metric_readout_and_ppn_gauge_lock",
            "one proof can close several beta/readout/gauge leaks at once",
        )
    if any(key in token for key in ["source", "spurion", "mhref", "denominator", "fit_smuggling", "measure"]):
        return (
            "P1",
            "source_normalization_and_hilbert_measure_lock",
            "source ownership prevents hidden GM/beta calibration smuggling",
        )
    if any(key in token for key in ["scalar", "curvature_pole", "integrated_tail", "dof"]):
        return (
            "P2",
            "no_extra_local_scalar_or_hidden_dof_theorem",
            "keeps the local branch metric-only rather than scalar-tensor by accident",
        )
    if any(key in token for key in ["boundary", "domain", "harmonic", "flux", "multipole", "motion"]):
        return (
            "P2",
            "compact_exterior_boundary_domain_silence",
            "turns exterior/reference assumptions into explicit local-PPN conditions",
        )
    if any(key in token for key in ["order", "phi2"]):
        return (
            "P3",
            "ppn_order_and_domain_bookkeeping",
            "needed for numerical acceptance but less upstream than the parent action",
        )
    return (
        "P3",
        "component_specific_source_or_theorem_row",
        "required before any claim, but not the first leverage point",
    )


def ledger_rows(timestamp: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for family, aggregate_component, path in DECOMPOSITION_SOURCES:
        for source_row in read_csv_rows(path):
            component = source_row.get("component", "")
            status = source_row.get("status", "")
            priority, dependency_class, reason = classify_dependency(component, status)
            tier = "aggregate" if component == aggregate_component else "subcomponent"
            rows.append(
                {
                    "ledger_id": f"BL3843_{len(rows):02d}",
                    "family": family,
                    "aggregate_component": aggregate_component,
                    "source_component_id": source_row.get("component_id", ""),
                    "component": component,
                    "tier": tier,
                    "definition": source_row.get("definition", ""),
                    "zero_route": source_row.get("zero_route", ""),
                    "bound_formula": source_row.get("bound_formula", ""),
                    "current_status": status,
                    "dependency_class": dependency_class,
                    "priority_band": priority,
                    "why_this_priority": reason,
                    "source_file": rel(path),
                    "valid_for_claim": False,
                    "timestamp_utc": timestamp,
                }
            )
    rows.append(
        {
            "ledger_id": f"BL3843_{len(rows):02d}",
            "family": "integrated_beta",
            "aggregate_component": "beta-1",
            "source_component_id": "BUP3842_1_beta_total",
            "component": "beta_total_bound",
            "tier": "top_formula",
            "definition": "integrated local-PPN beta residual after EH2, scalar2, boundary2, readout2, and eps_temporal4 decomposition",
            "zero_route": "every listed component must be zero by parent theorem on the same compact exterior branch",
            "bound_formula": BETA_TOTAL_FORMULA,
            "current_status": "STRUCTURALLY_COMPLETE_NONCLAIM_BETA_LEDGER",
            "dependency_class": "integrated_threshold_and_claim_gate",
            "priority_band": "P0",
            "why_this_priority": "this is the single dashboard row that prevents accidental beta/local-GR overclaim",
            "source_file": rel(CSV_3842_BETA),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def threshold_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "contract_id": "BTC3843_0_empirical_threshold",
            "observable": "beta-1",
            "threshold_symbol": "tau_beta_empirical",
            "threshold_value": "MISSING_EXTERNAL_NUMERIC_PPN_BETA_SOURCE",
            "units": "dimensionless",
            "acceptance_condition": "abs(beta-1) <= tau_beta_empirical",
            "source_status": "MISSING_SOURCE_BACKED_NUMERIC_THRESHOLD",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "BTC3843_1_integrated_formula",
            "observable": "beta-1",
            "threshold_symbol": "tau_beta_empirical",
            "threshold_value": "symbolic_only",
            "units": "dimensionless",
            "acceptance_condition": BETA_TOTAL_FORMULA,
            "source_status": "FORMULA_COMPLETE_NUMERIC_ROWS_MISSING",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "BTC3843_2_zero_route",
            "observable": "local_GR_beta_limit",
            "threshold_symbol": "exact_zero",
            "threshold_value": "0",
            "units": "dimensionless",
            "acceptance_condition": "all B_* components in the integrated ledger vanish on the same parent-owned branch",
            "source_status": "PARENT_THEOREM_REQUIRED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "BTC3843_3_bound_route",
            "observable": "local_PPN_beta_bound",
            "threshold_symbol": "tau_beta_empirical",
            "threshold_value": "MISSING_EXTERNAL_NUMERIC_PPN_BETA_SOURCE",
            "units": "dimensionless",
            "acceptance_condition": "sum(source_backed_component_bounds) <= tau_beta_empirical",
            "source_status": "COMPONENT_NUMBERS_AND_EMPIRICAL_THRESHOLD_REQUIRED",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "BTC3843_4_budget_rule",
            "observable": "component_budget",
            "threshold_symbol": "tau_component_i",
            "threshold_value": "not_assigned_until_tau_beta_empirical_is_sourced",
            "units": "dimensionless",
            "acceptance_condition": "no component budget may be invented before the empirical beta threshold is source-backed",
            "source_status": "GUARD_AGAINST_FAKE_NUMERIC_FILL",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def source_fill_queue_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "queue_id": "SFQ3843_0",
            "priority": "P0",
            "target": "parent EH second-variation / nonlinear self-source proof",
            "closes_components": "B_L2_operator; B_grav_energy_source; B_nonEH2_operator; part of B_EH2_vertex",
            "route": "expand the parent action to second order around the compact local branch and compare the visible 00 vertex with EH/GR before any arena fit",
            "minimum_artifact": "second-variation operator identity or explicit residual norm row",
            "why_first": "this is the GR-reduction leap; if it closes, MTS stops looking like a post-hoc PPN patch",
            "current_status": "NEXT_DERIVATION_TARGET",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "queue_id": "SFQ3843_1",
            "priority": "P1",
            "target": "single metric readout plus PPN gauge lock",
            "closes_components": "B_field_redef_gauge; B_t2_metric_projection; B_t2_readout_second_derivative; B_t2_field_redef_gauge; B_eps_temporal_gauge",
            "route": "prove q_obs owns one visible metric through first and second order, then fix the PPN gauge before beta extraction",
            "minimum_artifact": "readout Hessian/gauge theorem or residual coefficient ledger",
            "why_first": "prevents the same local solution being re-read as different beta values",
            "current_status": "AFTER_EH2_OR_PARALLEL_IF_SHORT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "queue_id": "SFQ3843_2",
            "priority": "P1",
            "target": "source normalization / Hilbert measure lock",
            "closes_components": "B_grav_energy_source; B_scalar_source_spurion; B_MHref_frame2; B_t2_fit_smuggling; B_eps_temporal_denominator",
            "route": "show the same compact source measure fixes Newtonian C_t, gravitational self-energy, and beta normalization",
            "minimum_artifact": "same-source-measure theorem or numeric source-normalization residual rows",
            "why_first": "this is where fitted GM can accidentally hide theory failure",
            "current_status": "HIGH_LEVERAGE_DEPENDENCY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "queue_id": "SFQ3843_3",
            "priority": "P2",
            "target": "no extra local scalar / hidden-dof theorem",
            "closes_components": "B_scalar_dof; B_scalar_integrated_tail; B_scalar_curvature_pole; B_nonEH2_operator; B_scalar_readout2",
            "route": "prove the compact local quotient has no retained scalar/class degree of freedom that couples to visible g00 at beta order",
            "minimum_artifact": "dof-counting theorem, scalaron-zero condition, or sourced scalar coupling/range bound",
            "why_first": "keeps the branch metric/GR-like instead of silently scalar-tensor",
            "current_status": "SECOND_WAVE_DERIVATION_TARGET",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "queue_id": "SFQ3843_4",
            "priority": "P2",
            "target": "compact exterior boundary/domain silence",
            "closes_components": "B_boundary2; B_eps_temporal_domain; B_t2_Dirichlet; B_t2_Neumann_flux; B_t2_harmonic; B_boundary_counterterm2",
            "route": "specialize boundary/reference theorems to the second-order temporal exterior problem",
            "minimum_artifact": "Dirichlet/flux/harmonic/counterterm zero theorem or finite source-bound rows",
            "why_first": "turns local vacuum/exterior assumptions into derivable branch conditions",
            "current_status": "SECOND_WAVE_DERIVATION_TARGET",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "queue_id": "SFQ3843_5",
            "priority": "P3",
            "target": "empirical beta threshold source row",
            "closes_components": "tau_beta_empirical; beta acceptance budget",
            "route": "source a current local-PPN beta bound from a primary/review source before assigning component budgets",
            "minimum_artifact": "source-backed numeric tau_beta row with citation/path and confidence label",
            "why_first": "needed for a bound pass, but not as fundamental as deriving the parent EH2 vertex",
            "current_status": "SOURCE_ACQUISITION_AFTER_DERIVATION_TARGET_LOCK",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def gate_rows(ledger: list[dict[str, object]], threshold: list[dict[str, object]], queue: list[dict[str, object]], timestamp: str) -> list[dict[str, object]]:
    all_text = " ".join(str(row) for row in ledger + threshold + queue)
    return [
        {
            "gate_id": "GATE3843_0_sources_integrated",
            "gate": "3838-3842 beta ledgers are integrated",
            "status": "PASS_DASHBOARD_BUILT",
            "claim_allowed": False,
            "reason": "all five beta families are present in a single machine-readable ledger",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3843_1_formula_complete",
            "gate": "integrated beta formula contains all current terms",
            "status": "PASS_FORMULA_COMPLETE",
            "claim_allowed": False,
            "reason": "formula contains EH2, scalar2, boundary2, readout2, and all eps_temporal4 components",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3843_2_numeric_threshold",
            "gate": "empirical beta threshold is numeric/source-backed",
            "status": "BLOCKED_MISSING_EXTERNAL_NUMERIC_PPN_BETA_SOURCE",
            "claim_allowed": False,
            "reason": "tau_beta_empirical is deliberately symbolic until sourced",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3843_3_component_numbers",
            "gate": "every component has zero theorem or source-backed number",
            "status": "BLOCKED_COMPONENT_THEOREMS_OR_NUMERIC_ROWS_REQUIRED",
            "claim_allowed": False,
            "reason": "ledger is structurally complete but no component row is claim-valid",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3843_4_no_fake_claim",
            "gate": "nonclaim guard",
            "status": "PASS_NO_CLAIM_PROMOTED",
            "claim_allowed": False,
            "reason": "valid_for_claim remains false throughout dashboard, threshold contract, and queue",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3843_5_next_derivation_target",
            "gate": "next target selected from integrated leverage order",
            "status": "PASS_ACTIONABLE_NEXT",
            "claim_allowed": False,
            "reason": "3844 attacks the parent EH second variation because it is the highest-leverage GR-reduction dependency",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "GATE3843_6_sanity_tokens",
            "gate": "all beta terms are visible to validation",
            "status": "PASS" if all(term in all_text for term in BETA_TERMS) else "FAIL_MISSING_TERM",
            "claim_allowed": False,
            "reason": "validation requires all top beta terms in the dashboard text",
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3843_0",
            "decision": "do not treat beta/local-GR as passed",
            "consequence": "the dashboard is a control panel, not evidence of a local-GR limit",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3843_1",
            "decision": "prefer derivation over numeric source-fill first",
            "consequence": "3844 targets the parent EH2 vertex before fetching empirical beta thresholds",
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3843_2",
            "decision": "do not assign component budgets yet",
            "consequence": "budgets wait until tau_beta_empirical and at least one source-backed/theorem-backed component row exists",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3843_0",
            "next_checkpoint": "3844-Y5-R2FR-parent-action-second-variation-EH2-vertex-proof-or-source-bound.md",
            "script": "scripts/Y5_R2FR_3844_parent_action_second_variation_EH2_vertex_proof_or_source_bound.py",
            "objective": "try to prove the visible parent second variation is EH/GR through quadratic order, or emit explicit EH2 residual source-bound rows",
            "reason": "the integrated dashboard selects EH2 as the highest-leverage route to derived local GR rather than a patchwork PPN fit",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "status": "PASS_NONCLAIM_INTEGRATED_BETA_DASHBOARD",
            "claim": "no beta/local-GR claim",
            "next": "3844 parent action second-variation EH2 vertex proof or source-bound",
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
    ledger: list[dict[str, object]],
    threshold: list[dict[str, object]],
    queue: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    timestamp: str,
) -> None:
    p0_queue = [row for row in queue if row["priority"] == "P0"]
    aggregates = [row for row in ledger if row["tier"] in {"aggregate", "top_formula"}]
    text = f"""# 3843 - Integrated Beta Ledger Threshold Dashboard And Source-Fill Queue

Private checkpoint. This takes the 3838-3842 beta work out of scattered ledgers and into one control panel. It does not claim `beta=1`, local GR, or a PPN pass.

Generated: `{timestamp}`

## Result

The local beta problem is now a single explicit contract:

`{BETA_TOTAL_FORMULA}`.

This is useful progress because the project can now see the whole beta obstruction at once. It also makes the next move sharper: the highest-leverage route is not another pass saying "source rows missing"; it is a direct attack on the parent EH second variation.

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Integrated Aggregate Rows

{markdown_table(aggregates, ["ledger_id", "family", "component", "tier", "current_status", "priority_band", "dependency_class"])}

## Threshold Contract

{markdown_table(threshold, ["contract_id", "observable", "threshold_symbol", "threshold_value", "source_status", "claim_allowed"])}

## Source-Fill / Derivation Queue

{markdown_table(queue, ["queue_id", "priority", "target", "closes_components", "current_status"])}

## Immediate P0 Targets

{markdown_table(p0_queue, ["queue_id", "target", "minimum_artifact", "why_first"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "consequence"])}

## Bottom Line

3843 is the anti-circling checkpoint: it compresses the beta/local-GR blockage into a dashboard and selects one leap-forward target. The next checkpoint should try the derivation first: parent action second variation -> EH quadratic vertex -> GR-like beta self-coupling. If that fails, only then emit residual norm/source-bound rows.

Next target: `3844-Y5-R2FR-parent-action-second-variation-EH2-vertex-proof-or-source-bound.md`.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3842", "Current State After 3843", 1)
    paragraph = (
        "`3843` integrates the complete beta/local-PPN ledger into one dashboard instead of leaving EH2, scalar2, boundary2, readout2, and eps_temporal4 scattered across separate checkpoints. "
        "The retained master contract is `|beta-1| <= B_EH2_vertex+B_extra_scalar2+B_boundary2+B_readout2+B_eps_temporal_order+B_eps_temporal_gauge+B_eps_temporal_domain+B_eps_temporal_nonlinear+B_eps_temporal_multipole_motion+B_eps_temporal_denominator`. "
        "No beta/local-GR claim is made because no empirical `tau_beta` row or component theorem/source row is claim-valid. "
        "The dashboard selects the parent EH second variation as the next highest-leverage derivation target because it is the route that can make the local branch reduce to GR rather than merely fitting PPN numbers.\n\n"
    )
    anchor = "`3842` decomposes"
    if paragraph not in text and anchor in text:
        text = text.replace(anchor, paragraph + anchor, 1)
    old_gate = """`3843-Y5-R2FR-integrated-beta-ledger-threshold-dashboard-and-source-fill-queue.md`

Target: combine EH2, scalar2, boundary2, readout2, and eps_temporal4 rows into an integrated beta/local-PPN dashboard with source-fill priorities.

This is the best next move because 3842 makes the beta envelope structurally complete but nonclaim."""
    new_gate = """`3844-Y5-R2FR-parent-action-second-variation-EH2-vertex-proof-or-source-bound.md`

Target: try to prove the parent visible second variation matches the EH/GR quadratic vertex and gravitational self-source, or emit explicit residual source-bound rows.

This is the best next move because 3843 shows EH2 is the highest-leverage route from symbolic beta ledger to derived local GR."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3843_INTEGRATED_BETA_LEDGER.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3843_BETA_THRESHOLD_CONTRACT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3843_SOURCE_FILL_QUEUE.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3843_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3843_INTEGRATED_BETA_LEDGER.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    if f"Generated by 3843 at {timestamp}" not in text:
        text = text.rstrip() + f"\n\n<!-- Generated by 3843 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    ledger: list[dict[str, object]],
    threshold: list[dict[str, object]],
    queue: list[dict[str, object]],
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

    all_text = " ".join(str(row) for row in ledger + threshold + queue + gates)
    add(
        "VAL3843_0_sources",
        "all cited source paths exist and needles are found",
        all(row["exists"] and row["needle_found"] for row in sources),
        f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved",
    )
    add(
        "VAL3843_1_families",
        "all five beta families are represented",
        all(family in all_text for family in ["EH2", "scalar2", "boundary2", "readout2", "eps_temporal4"]),
        "EH2/scalar2/boundary2/readout2/eps_temporal4 family tokens present",
    )
    add(
        "VAL3843_2_terms",
        "integrated beta formula contains all top terms",
        all(term in all_text for term in BETA_TERMS),
        "top beta terms visible in dashboard text",
    )
    add(
        "VAL3843_3_threshold_blocked",
        "empirical beta threshold remains blocked until sourced",
        any(row["contract_id"] == "BTC3843_0_empirical_threshold" and "MISSING_EXTERNAL_NUMERIC" in str(row["threshold_value"]) for row in threshold),
        "tau_beta empirical row is explicitly missing/source-blocked",
    )
    add(
        "VAL3843_4_nonclaim",
        "all 3843 rows remain nonclaim",
        all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in ledger + threshold + queue + gates),
        "valid_for_claim/claim_allowed false throughout",
    )
    add(
        "VAL3843_5_p0_next",
        "P0 next target is parent EH second variation",
        any(row["queue_id"] == "SFQ3843_0" and "EH second-variation" in row["target"] for row in queue)
        and any(row["gate_id"] == "GATE3843_5_next_derivation_target" and row["status"] == "PASS_ACTIONABLE_NEXT" for row in gates),
        "source-fill queue selects EH2 as next derivation target",
    )
    add(
        "VAL3843_6_no_budget_smuggle",
        "component budgets are not assigned before tau_beta is sourced",
        "not_assigned_until_tau_beta_empirical_is_sourced" in all_text and "GUARD_AGAINST_FAKE_NUMERIC_FILL" in all_text,
        "budget guard present",
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
        add(f"VAL3843_7_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add(
        "VAL3843_8_doc",
        "markdown checkpoint document exists",
        DOC_PATH.exists() and "3844-Y5-R2FR-parent-action-second-variation" in read_text(DOC_PATH),
        rel(DOC_PATH),
    )
    fwb_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3843*", "P8_Y5_BRR545_3843*", "*Y5_R2FR_3843*", "3843-Y5-R2FR*"):
            fwb_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add(
        "VAL3843_9_formalization_clean",
        "formalization-workbench has no 3843 files",
        len(fwb_hits) == 0,
        "; ".join(str(path) for path in fwb_hits) if fwb_hits else "no 3843 file hits under formalization-workbench",
    )
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add(
        "VAL3843_10_pycache_removed",
        "scripts __pycache__ removed",
        len(pycache_hits) == 0,
        "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories",
    )
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(timestamp)
    ledger = ledger_rows(timestamp)
    threshold = threshold_rows(timestamp)
    queue = source_fill_queue_rows(timestamp)
    gates = gate_rows(ledger, threshold, queue, timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["ledger"], ledger)
    write_csv(OUTPUTS["threshold"], threshold)
    write_csv(OUTPUTS["queue"], queue)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, ledger, threshold, queue, gates, decisions, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, ledger, threshold, queue, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_NONCLAIM_INTEGRATED_BETA_DASHBOARD")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-bound-runner-v3-from-identity-stack"
STATUS = "local_bound_runner_v3_from_identity_stack_written_GR_null_baseline_sane_identity_closure_labelled_retained_residuals_budgeted_no_PPN_or_local_GR_pass"
CLAIM_CEILING = "local_bound_runner_v3_only_no_WEP_EH_Newton_PPN_fifth_force_boundary_bulk_domain_or_local_GR_pass"
NEXT_TARGET = "398-parent-action-contract-v2-after-identity-stack.md"


SOURCE_DOCS = [
    {
        "path": "374-fifth-force-preferred-frame-source-lock-manifest.md",
        "role": "preferred-frame, xi, alpha3, Gdot/G, and fifth-force source locks",
    },
    {
        "path": "377-fifth-force-range-coupling-map.md",
        "role": "alpha(lambda) force-law contract",
    },
    {
        "path": "383-local-bound-runner-v2-from-retained-residuals.md",
        "role": "runner-v2 state definitions and retained residual matrix",
    },
    {
        "path": "386-local-bound-runner-v2-smoke-matrix.md",
        "role": "same-pipeline GR/null baseline sanity and smoke scenario design",
    },
    {
        "path": "391-local-GR-stack-after-identity-coframe-closure.md",
        "role": "identity closure branch labels and remaining local-GR blocker queue",
    },
    {
        "path": "392-EH-operator-selection-under-identity-closure.md",
        "role": "EH operator selection failure and non-EH operator ledger",
    },
    {
        "path": "393-source-normalized-Newtonian-limit-under-identity-closure.md",
        "role": "source-normalization amplitude laws and GM absorption gates",
    },
    {
        "path": "394-boundary-bulk-nohair-joint-runner-under-identity-closure.md",
        "role": "joint boundary/bulk force-flux runner and q_BX contract",
    },
    {
        "path": "395-preferred-frame-domain-nohair-under-identity-closure.md",
        "role": "preferred-frame/domain split under identity closure",
    },
    {
        "path": "396-local-GR-reduction-sufficiency-stack-audit.md",
        "role": "local-GR sufficiency stack audit and runner-v3 readiness",
    },
    {
        "path": "runs/20260602-032500-local-GR-reduction-sufficiency-stack-audit/results/local_GR_sufficiency_stack.csv",
        "role": "machine-readable local-GR sufficiency rungs for runner-v3",
    },
    {
        "path": "runs/20260602-032500-local-GR-reduction-sufficiency-stack-audit/results/observable_row_rollup.csv",
        "role": "machine-readable observable row rollup for runner-v3",
    },
]


STATE_DEFINITIONS = [
    {
        "state": "derived_zero",
        "meaning": "parent theorem derives the residual is zero or harmless",
        "score_policy": "may be evaluated as zero with source path recorded",
        "pass_claim_policy": "still requires every coupled row closed",
    },
    {
        "state": "closure_zero",
        "meaning": "zero by explicit branch assumption, not parent derivation",
        "score_policy": "evaluate only inside labelled closure branch",
        "pass_claim_policy": "no parent-derived WEP/local-GR claim",
    },
    {
        "state": "conditional_theorem",
        "meaning": "theorem shape is valid if extra premises are assumed",
        "score_policy": "emit conditional branch or residual debt, not pass",
        "pass_claim_policy": "promotion blocked until premises are derived",
    },
    {
        "state": "retained_residual",
        "meaning": "operator/coefficient remains in the modified-gravity ledger",
        "score_policy": "map to observable rows or keep symbolic if not numeric",
        "pass_claim_policy": "no local-GR pass",
    },
    {
        "state": "budget_only",
        "meaning": "numeric source lock exists but MTS coefficient is missing",
        "score_policy": "emit suppression budget and smoke severity",
        "pass_claim_policy": "budget is not an observational pass",
    },
    {
        "state": "contingent_budget",
        "meaning": "numeric guardrail applies only if the channel exists",
        "score_policy": "keep row and score only when branch predicts the channel",
        "pass_claim_policy": "no pass and no failure until channel relevance is derived",
    },
    {
        "state": "unscored_parameterized",
        "meaning": "range/coupling/profile/source charge is missing",
        "score_policy": "retain alpha(lambda) or profile contract; no scalar score",
        "pass_claim_policy": "no fifth-force/delta_G pass",
    },
    {
        "state": "failed_open",
        "meaning": "required parent theorem is absent",
        "score_policy": "route to residual fallback or parent-action contract",
        "pass_claim_policy": "blocks local-GR promotion",
    },
]


RUNNER_V3_MATRIX = [
    {
        "row_id": "R0_identity_coframe_direct",
        "observable": "eta_WEP_direct_geometry",
        "state": "closure_zero",
        "source_lock": 2.8e-15,
        "source_lock_units": "dimensionless",
        "baseline_value": 0.0,
        "active_sources": "direct matter/coframe pullback only",
        "identity_stack_update": "closed by ehat=e branch label",
        "allowed_output": "closure-zero branch row; no parent-derived WEP claim",
    },
    {
        "row_id": "R1_WEP_source_charge",
        "observable": "eta_WEP_source_charge",
        "state": "contingent_budget",
        "source_lock": 2.8e-15,
        "source_lock_units": "dimensionless",
        "baseline_value": 0.0,
        "active_sources": "species-dependent source charge; X charge; source-normalization species split",
        "identity_stack_update": "not killed by coframe identity; only relevant if source-charge channel exists",
        "allowed_output": "contingent WEP-source guardrail",
    },
    {
        "row_id": "R2_clock_redshift",
        "observable": "alpha_clock_redshift",
        "state": "budget_only",
        "source_lock": 3.1e-5,
        "source_lock_units": "dimensionless",
        "baseline_value": 0.0,
        "active_sources": "clock constants; nonlocal/source drift; class-metric counterstress branch outside identity",
        "identity_stack_update": "direct matter geometry cleaned; source/nonlocal residues retained",
        "allowed_output": "budget only",
    },
    {
        "row_id": "R3_gamma",
        "observable": "gamma_minus_1",
        "state": "budget_only",
        "source_lock": 2.3e-5,
        "source_lock_units": "dimensionless",
        "baseline_value": 0.0,
        "active_sources": "non-EH operators; boundary shear/radial hair; bulk-X; domain/projector stress",
        "identity_stack_update": "EH/source/boundary/bulk/domain residuals retained",
        "allowed_output": "budget only",
    },
    {
        "row_id": "R4_beta",
        "observable": "beta_minus_1",
        "state": "budget_only",
        "source_lock": 7.8e-5,
        "source_lock_units": "dimensionless",
        "baseline_value": 0.0,
        "active_sources": "source normalization; boundary radial/flux; nonlinear bulk/source hair",
        "identity_stack_update": "source-normalized Newtonian limit conditional only",
        "allowed_output": "budget only",
    },
    {
        "row_id": "R5_alpha1",
        "observable": "alpha1",
        "state": "budget_only",
        "source_lock": 1.0e-4,
        "source_lock_units": "dimensionless",
        "baseline_value": 0.0,
        "active_sources": "B0i; domain vector; projector vector; marker leakage",
        "identity_stack_update": "coframe slip term removed by identity label; domain/projector residues retained",
        "allowed_output": "budget only",
    },
    {
        "row_id": "R6_alpha2",
        "observable": "alpha2",
        "state": "budget_only",
        "source_lock": 2.0e-9,
        "source_lock_units": "dimensionless",
        "baseline_value": 0.0,
        "active_sources": "B0i; domain vector/aniso; projector vector",
        "identity_stack_update": "domain/projector no-hair not parent-derived",
        "allowed_output": "budget only",
    },
    {
        "row_id": "R7_alpha3",
        "observable": "alpha3",
        "state": "contingent_budget",
        "source_lock": 4.0e-20,
        "source_lock_units": "dimensionless",
        "baseline_value": 0.0,
        "active_sources": "unowned boundary/bulk/domain/projector flux; momentum nonconservation",
        "identity_stack_update": "Ward flux not owned; use only if channel exists",
        "allowed_output": "contingent guardrail",
    },
    {
        "row_id": "R8_xi",
        "observable": "xi",
        "state": "budget_only",
        "source_lock": 4.0e-9,
        "source_lock_units": "dimensionless",
        "baseline_value": 0.0,
        "active_sources": "boundary trace-free shear; domain anisotropy; topology cycles; external-domain anisotropy",
        "identity_stack_update": "xi kept separate from gamma",
        "allowed_output": "budget only",
    },
    {
        "row_id": "R9_Gdot",
        "observable": "Gdot_over_G",
        "state": "contingent_budget",
        "source_lock": 9.6e-15,
        "source_lock_units": "yr^-1",
        "baseline_value": 0.0,
        "active_sources": "time-varying G_eff/M_eff; memory kernels; unowned flux; domain scale drift",
        "identity_stack_update": "source normalization and Ward flux not derived",
        "allowed_output": "contingent guardrail",
    },
    {
        "row_id": "R10_fifth_force",
        "observable": "delta_G_or_fifth_force_yukawa",
        "state": "unscored_parameterized",
        "source_lock": "alpha(lambda)",
        "source_lock_units": "range-dependent",
        "baseline_value": "no fifth force beyond measured GM",
        "active_sources": "bulk-X; boundary radial hair; scalar/class/nonlocal source-normalization residues",
        "identity_stack_update": "alpha_X/alpha_B/alpha_Y(lambda) missing",
        "allowed_output": "force-law contract only; no scalar score",
    },
    {
        "row_id": "R11_EH_operator_ledger",
        "observable": "non_EH_operator_coefficients",
        "state": "retained_residual",
        "source_lock": "symbolic",
        "source_lock_units": "operator family",
        "baseline_value": "EH plus Lambda",
        "active_sources": "R2/fR/Weyl/scalar-tensor/vector/nonlocal/source-normalization operators",
        "identity_stack_update": "EH not parent-derived",
        "allowed_output": "symbolic residual ledger",
    },
]


NUMERIC_ROW_IDS = [
    row["row_id"]
    for row in RUNNER_V3_MATRIX
    if isinstance(row["source_lock"], (int, float))
]


SMOKE_SCENARIOS = [
    {
        "scenario": "GR_null_baseline",
        "mode": "absolute",
        "value": 0.0,
        "branch": "baseline",
        "interpretation": "GR/null row through the same evaluator; must be inside every numeric source lock",
        "claim_policy": "baseline sanity only",
    },
    {
        "scenario": "identity_closure_zero_control",
        "mode": "absolute",
        "value": 0.0,
        "branch": "closure_zero",
        "interpretation": "what the direct identity-coframe closure row evaluates to inside the labelled branch",
        "claim_policy": "closure branch only, not parent-derived",
    },
    {
        "scenario": "one_tenth_budget_control",
        "mode": "fraction_of_limit",
        "value": 0.1,
        "branch": "budget_control",
        "interpretation": "toy retained coefficient safely below source lock",
        "claim_policy": "inside budget is not a derivation",
    },
    {
        "scenario": "edge_budget_control",
        "mode": "fraction_of_limit",
        "value": 1.0,
        "branch": "budget_edge",
        "interpretation": "toy retained coefficient exactly at source lock",
        "claim_policy": "edge is not stable evidence",
    },
    {
        "scenario": "ten_times_over_budget_control",
        "mode": "fraction_of_limit",
        "value": 10.0,
        "branch": "over_budget",
        "interpretation": "toy retained coefficient ten times too large",
        "claim_policy": "explicit smoke failure",
    },
    {
        "scenario": "floor_leak_1e_minus_12",
        "mode": "absolute",
        "value": 1.0e-12,
        "branch": "absolute_leak_floor",
        "interpretation": "tiny-looking absolute leak; exposes hardest local rows",
        "claim_policy": "diagnostic only",
    },
    {
        "scenario": "unit_coupling_stress",
        "mode": "absolute",
        "value": 1.0,
        "branch": "unit_response",
        "interpretation": "raw order-one retained coupling stress",
        "claim_policy": "must fail; shows required suppression factors",
    },
]


IDENTITY_CLOSURE_REGISTER = [
    {
        "closure": "identity_coframe",
        "mathematical_form": "ehat=e and S_matter=sum_A S_A[Psi_A,e,omega[e],theta_A]",
        "rows_closed": "eta_WEP_direct_geometry; direct coframe slip pieces of alpha1/clock/WEP",
        "state": "closure_zero",
        "forbidden_claim": "parent-derived WEP/local-GR",
    },
    {
        "closure": "no_nonmetric_matter_spurions",
        "mathematical_form": "partial_Z e=0 and partial_Z theta_A=0 for nonmetric Z inside the branch",
        "rows_closed": "direct matter-spurion clock/WEP terms",
        "state": "closure_zero",
        "forbidden_claim": "nonmetric sector absent from parent action",
    },
    {
        "closure": "class_metric_counterstress_separate",
        "mathematical_form": "class-metric pullback is a modified-gravity/counterstress branch, not the GR-facing identity branch",
        "rows_closed": "none; branch separation only",
        "state": "retained_residual",
        "forbidden_claim": "borrow identity closure for class-metric branch",
    },
]


RETAINED_RESIDUAL_FAMILIES = [
    {
        "family": "EH_operator_residuals",
        "state": "retained_residual",
        "rows": "gamma; beta; xi; fifth_force; source_normalization",
        "source_checkpoint": "392",
        "runner_action": "retain symbolic operator family; no EH pass",
    },
    {
        "family": "source_normalization_residuals",
        "state": "retained_residual",
        "rows": "delta_G; Gdot/G; beta; fifth_force; WEP_source",
        "source_checkpoint": "393",
        "runner_action": "emit delta_mu/mu law and keep exits active",
    },
    {
        "family": "boundary_bulk_residuals",
        "state": "retained_residual",
        "rows": "gamma; beta; alpha_i; xi; fifth_force; Gdot/G",
        "source_checkpoint": "394",
        "runner_action": "emit q_BX family and retain boundary/bulk coefficients",
    },
    {
        "family": "preferred_frame_domain_residuals",
        "state": "budget_only_or_contingent_budget",
        "rows": "alpha1; alpha2; alpha3; xi; Gdot/G",
        "source_checkpoint": "395",
        "runner_action": "budget source-locked rows; do not double-count coframe slip",
    },
    {
        "family": "fifth_force_range_residuals",
        "state": "unscored_parameterized",
        "rows": "delta_G_or_fifth_force_yukawa",
        "source_checkpoint": "377;393;394",
        "runner_action": "keep alpha(lambda) contract; no scalar score",
    },
]


PROMOTION_POLICY = [
    {
        "condition": "all_rows_derived_zero",
        "promotion_allowed": "theoretical possibility only",
        "current_status": "false",
        "reason": "identity branch has closure_zero and many retained/conditional rows",
    },
    {
        "condition": "closure_zero_present",
        "promotion_allowed": "internal branch testing only",
        "current_status": "true",
        "reason": "identity coframe is a labelled closure, not parent theorem",
    },
    {
        "condition": "budget_only_present",
        "promotion_allowed": "no pass",
        "current_status": "true",
        "reason": "source locks exist but MTS coefficients are missing",
    },
    {
        "condition": "contingent_budget_present",
        "promotion_allowed": "guardrail only",
        "current_status": "true",
        "reason": "alpha3/Gdot/WEP-source apply only if channel exists",
    },
    {
        "condition": "unscored_parameterized_present",
        "promotion_allowed": "no fifth-force/delta_G pass",
        "current_status": "true",
        "reason": "alpha(lambda), range, source/test charges missing",
    },
    {
        "condition": "retained_residual_present",
        "promotion_allowed": "no local-GR pass",
        "current_status": "true",
        "reason": "EH/operator/source/boundary/bulk/domain residual families retained",
    },
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "write parent-action contract v2 that names the exact variations needed to turn closure/conditional/retained runner-v3 rows into derived rows",
        "pass_condition": "every runner-v3 non-derived state has a parent-action obligation",
    },
    {
        "priority": 2,
        "target": "399-local-GR-status-for-human-review.md",
        "task": "write concise private status memo with strongest progress, blockers, and next empirical/theory tests",
        "pass_condition": "human-readable project overview with no public overclaim",
    },
    {
        "priority": 3,
        "target": "400-runner-v3-numeric-smoke-extension.md",
        "task": "extend runner-v3 from toy smoke controls toward real symbolic/numeric coefficient sweeps",
        "pass_condition": "GR/null baseline plus MTS retained residual sweeps run through same evaluator",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        rows.append(
            {
                "source_file": source_doc["path"],
                "exists": source_path.exists(),
                "role": source_doc["role"],
            }
        )
    return rows


def scenario_value(source_lock: float, scenario: dict[str, Any]) -> float:
    if scenario["mode"] == "fraction_of_limit":
        return source_lock * float(scenario["value"])
    return float(scenario["value"])


def classify_smoke(row: dict[str, Any], scenario: dict[str, Any], severity: float) -> str:
    state = str(row["state"])
    if scenario["scenario"] == "GR_null_baseline":
        return "baseline_sane" if severity == 0.0 else "baseline_broken"
    if scenario["scenario"] == "identity_closure_zero_control":
        return "closure_zero_visible" if state == "closure_zero" and severity == 0.0 else "zero_control_only"
    if state == "closure_zero":
        return "closure_row_no_promotion" if severity == 0.0 else "closure_row_would_fail_if_leak_exists"
    if state == "contingent_budget" and severity > 1.0:
        return "over_budget_if_channel_exists"
    if severity == 0.0:
        return "inside_budget_zero"
    if severity < 1.0:
        return "inside_budget_smoke_only"
    if severity == 1.0:
        return "on_budget_edge_unstable"
    return "over_budget"


def numeric_rows() -> list[dict[str, Any]]:
    return [row for row in RUNNER_V3_MATRIX if isinstance(row["source_lock"], (int, float))]


def smoke_matrix_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for local_row in numeric_rows():
        source_lock = float(local_row["source_lock"])
        for scenario in SMOKE_SCENARIOS:
            residual_value = scenario_value(source_lock, scenario)
            severity = abs(residual_value) / source_lock if source_lock else float("inf")
            rows.append(
                {
                    "row_id": local_row["row_id"],
                    "observable": local_row["observable"],
                    "state": local_row["state"],
                    "source_lock": source_lock,
                    "units": local_row["source_lock_units"],
                    "scenario": scenario["scenario"],
                    "branch": scenario["branch"],
                    "residual_value": residual_value,
                    "severity_ratio": severity,
                    "smoke_class": classify_smoke(local_row, scenario, severity),
                    "claim_allowed": False,
                    "interpretation": scenario["interpretation"],
                }
            )
    return rows


def baseline_sanity_rows(smoke_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    baseline_rows = [row for row in smoke_rows if row["scenario"] == "GR_null_baseline"]
    return [
        {
            "scenario": "GR_null_baseline",
            "numeric_rows_checked": len(baseline_rows),
            "inside_rows": sum(1 for row in baseline_rows if row["severity_ratio"] == 0.0),
            "broken_rows": sum(1 for row in baseline_rows if row["severity_ratio"] != 0.0),
            "verdict": "baseline_sane" if all(row["severity_ratio"] == 0.0 for row in baseline_rows) else "baseline_broken",
            "claim_policy": "pipeline sanity only, not MTS pass",
        }
    ]


def suppression_budget_summary_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for local_row in numeric_rows():
        source_lock = float(local_row["source_lock"])
        unit_severity = 1.0 / source_lock if source_lock else float("inf")
        rows.append(
            {
                "row_id": local_row["row_id"],
                "observable": local_row["observable"],
                "state": local_row["state"],
                "required_ceiling": source_lock,
                "units": local_row["source_lock_units"],
                "unit_coupling_severity": unit_severity,
                "always_relevant": local_row["state"] not in {"contingent_budget", "closure_zero"},
                "promotion_allowed": False,
            }
        )
    rows.sort(key=lambda row: float(row["unit_coupling_severity"]), reverse=True)
    return rows


def scenario_summary_rows(smoke_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for scenario in SMOKE_SCENARIOS:
        subset = [row for row in smoke_rows if row["scenario"] == scenario["scenario"]]
        rows.append(
            {
                "scenario": scenario["scenario"],
                "inside_rows": sum(1 for row in subset if row["severity_ratio"] < 1.0),
                "edge_rows": sum(1 for row in subset if row["severity_ratio"] == 1.0),
                "over_budget_rows": sum(1 for row in subset if row["severity_ratio"] > 1.0),
                "claim_policy": scenario["claim_policy"],
            }
        )
    return rows


def unscored_rows() -> list[dict[str, Any]]:
    return [
        row
        for row in RUNNER_V3_MATRIX
        if row["state"] in {"unscored_parameterized", "retained_residual"}
        or not isinstance(row["source_lock"], (int, float))
    ]


def gate_rows(source_rows: list[dict[str, Any]], smoke_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    baseline_rows = [row for row in smoke_rows if row["scenario"] == "GR_null_baseline"]
    baseline_sane = all(row["severity_ratio"] == 0.0 for row in baseline_rows)
    false_pass_rows = [
        row for row in RUNNER_V3_MATRIX if row["state"] != "derived_zero"
    ]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "state_definitions_written",
            "status": "pass",
            "evidence": f"{len(STATE_DEFINITIONS)} runner-v3 states recorded",
        },
        {
            "gate": "runner_v3_matrix_written",
            "status": "pass",
            "evidence": f"{len(RUNNER_V3_MATRIX)} local rows/families emitted",
        },
        {
            "gate": "identity_closure_label_visible",
            "status": "pass",
            "evidence": "direct coframe/WEP row is closure_zero, not derived_zero",
        },
        {
            "gate": "GR_null_baseline_same_evaluator",
            "status": "pass" if baseline_sane else "fail",
            "evidence": f"{len(baseline_rows)} numeric rows checked",
        },
        {
            "gate": "unscored_and_retained_rows_preserved",
            "status": "pass",
            "evidence": f"{len(unscored_rows())} unscored/retained symbolic rows preserved",
        },
        {
            "gate": "false_pass_blocked",
            "status": "pass",
            "evidence": f"{len(false_pass_rows)} non-derived rows have claim_allowed=false",
        },
        {
            "gate": "local_GR_or_PPN_promoted",
            "status": "fail",
            "evidence": "runner-v3 has closure_zero, retained_residual, budget_only, contingent_budget, and unscored_parameterized rows",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    smoke_rows = smoke_matrix_rows()

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "state_definitions.csv", STATE_DEFINITIONS)
    write_csv(results_dir / "runner_v3_matrix.csv", RUNNER_V3_MATRIX)
    write_csv(results_dir / "identity_closure_register.csv", IDENTITY_CLOSURE_REGISTER)
    write_csv(results_dir / "retained_residual_families.csv", RETAINED_RESIDUAL_FAMILIES)
    write_csv(results_dir / "baseline_sanity_matrix.csv", baseline_sanity_rows(smoke_rows))
    write_csv(results_dir / "residual_smoke_matrix.csv", smoke_rows)
    write_csv(results_dir / "scenario_summary.csv", scenario_summary_rows(smoke_rows))
    write_csv(results_dir / "suppression_budget_summary.csv", suppression_budget_summary_rows())
    write_csv(results_dir / "unscored_parameterized_rows.csv", unscored_rows())
    write_csv(results_dir / "promotion_policy.csv", PROMOTION_POLICY)
    write_csv(results_dir / "gate_results.csv", gate_rows(source_rows, smoke_rows))
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    baseline = baseline_sanity_rows(smoke_rows)[0]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "runner_v3_rows": len(RUNNER_V3_MATRIX),
        "numeric_rows": len(numeric_rows()),
        "unscored_or_retained_rows": len(unscored_rows()),
        "GR_null_baseline_verdict": baseline["verdict"],
        "identity_closure_label_visible": True,
        "derived_local_GR_claim_allowed": False,
        "PPN_pass_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


DECISION = [
    {
        "status": STATUS,
        "decision": "Runner-v3 implements the post-identity local stack as a machine-readable residual matrix. The GR/null baseline is sane through the same evaluator. Direct coframe/WEP geometry is closure_zero by label, not derived_zero. Source-charge WEP, clock, gamma, beta, alpha_i, xi, Gdot/G, fifth-force, and EH/operator residual families remain budgeted, contingent, unscored, or retained. No WEP, EH, Newtonian, PPN, fifth-force, boundary/bulk/domain, or local-GR pass is claimed.",
        "GR_null_baseline": "sane",
        "identity_branch": "closure_zero_visible",
        "local_GR_claim_allowed": False,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 397 local-bound runner v3 from identity stack artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()

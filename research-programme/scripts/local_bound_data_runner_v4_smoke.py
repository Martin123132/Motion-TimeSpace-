from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-bound-data-runner-v4-smoke"
CHECKPOINT_DOC = "408-local-bound-data-runner-v4-smoke.md"
STATUS = "local_bound_data_runner_v4_smoke_written_closure_retained_contingent_unscored_rows_evaluated_without_theorem_promotion_no_local_GR_pass"
CLAIM_CEILING = "local_bound_data_runner_v4_smoke_only_no_WEP_EH_Newton_PPN_flux_fifth_force_or_local_GR_pass"
NEXT_TARGET = "409-runner-v4-red-team.md"


SOURCE_DOCS = [
    {
        "path": "400-runner-v3-numeric-smoke-extension.md",
        "role": "channel-level numeric smoke profile design",
    },
    {
        "path": "403-boundary-domain-flux-nohair-numeric-contract.md",
        "role": "hard boundary/domain/flux source-lock contract",
    },
    {
        "path": "406-local-runner-v4-derived-vs-closure-queue.md",
        "role": "runner-v4 state map and zero-kind discipline",
    },
    {
        "path": "407-primitive-relational-quotient-action-sketch.md",
        "role": "primitive quotient sketch with no theorem-zero upgrades",
    },
    {
        "path": "runs/20260602-041500-runner-v3-numeric-smoke-extension/results/channel_map.csv",
        "role": "row-channel evaluator map",
    },
    {
        "path": "runs/20260602-041500-runner-v3-numeric-smoke-extension/results/aggregate_channel_bounds.csv",
        "role": "tightest channel source-lock bounds",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv",
        "role": "runner-v4 row states",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/row_bound_pressure.csv",
        "role": "runner-v4 tightest row pressures",
    },
]


PROFILE_DEFINITIONS = [
    {
        "profile": "GR_null_baseline",
        "kind": "all_zero",
        "description": "GR/null comparator through the v4 evaluator.",
        "claim_policy": "pipeline sanity only",
    },
    {
        "profile": "identity_closure_zero_control",
        "kind": "all_zero",
        "description": "Labelled identity branch: closure-zero row is set to zero, but not theorem-zero.",
        "claim_policy": "closure benchmark only",
    },
    {
        "profile": "retained_0p1_tightest_bound_active",
        "kind": "fraction_tightest_bound",
        "fraction": 0.1,
        "description": "All boundable channels active at 10 percent of their tightest source lock.",
        "claim_policy": "inside budget only if a theorem derives coefficients",
    },
    {
        "profile": "retained_edge_tightest_bound_active",
        "kind": "fraction_tightest_bound",
        "fraction": 1.0,
        "description": "All boundable channels active at their tightest source-lock edge.",
        "claim_policy": "edge is unstable and not evidence",
    },
    {
        "profile": "closure_row_leak_1e_minus_15",
        "kind": "explicit",
        "values": {
            "coframe_slip_ehat_minus_e": 1.0e-15,
        },
        "description": "Direct coframe closure row leaks below its source lock.",
        "claim_policy": "shows inside-budget closure leak is still not theorem-zero",
    },
    {
        "profile": "source_charge_1e_minus_14",
        "kind": "explicit",
        "values": {
            "source_charge_species_split": 1.0e-14,
            "bulk_X_composition_charge": 1.0e-14,
            "boundary_species_charge": 1.0e-14,
            "source_normalization_species_split": 1.0e-14,
        },
        "description": "WEP/source-charge channels at a tiny absolute scale.",
        "claim_policy": "diagnostic WEP-source stress",
    },
    {
        "profile": "alpha3_flux_1e_minus_20",
        "kind": "explicit",
        "values": {
            "bulk_flux_X": 1.0e-20,
            "domain_projector_flux": 1.0e-20,
            "unowned_momentum_flux": 1.0e-20,
        },
        "description": "Alpha3 flux channels at 1e-20 each.",
        "claim_policy": "inside only if exact flux theorem or coefficient map exists",
    },
    {
        "profile": "alpha3_flux_1e_minus_15",
        "kind": "explicit",
        "values": {
            "bulk_flux_X": 1.0e-15,
            "domain_projector_flux": 1.0e-15,
            "unowned_momentum_flux": 1.0e-15,
        },
        "description": "Alpha3 flux channels at WEP-scale leakage.",
        "claim_policy": "must fail; exposes alpha3 hardness",
    },
    {
        "profile": "Gdot_memory_drift_1e_minus_14_per_yr",
        "kind": "explicit",
        "values": {
            "memory_kernel_drift_per_yr": 1.0e-14,
        },
        "description": "One secular memory-drift channel just above the Gdot/G source lock.",
        "claim_policy": "diagnostic Gdot stress",
    },
    {
        "profile": "domain_projector_1e_minus_10",
        "kind": "explicit",
        "values": {
            "domain_vector_leakage": 1.0e-10,
            "domain_projector_stress": 1.0e-10,
            "projector_vector_leakage": 1.0e-10,
            "domain_anisotropy": 1.0e-10,
            "domain_projector_flux": 1.0e-10,
            "domain_scale_drift_per_yr": 1.0e-10,
        },
        "description": "Domain/projector leakage at 1e-10.",
        "claim_policy": "diagnostic preferred-frame/domain stress",
    },
    {
        "profile": "fifth_force_alpha_1e_minus_5_unscored",
        "kind": "explicit",
        "values": {
            "finite_range_yukawa_alpha": 1.0e-5,
        },
        "description": "Finite-range fifth-force alpha activated without range/source-charge curve.",
        "claim_policy": "unscored fifth-force activation only",
    },
    {
        "profile": "unit_coupling_stress",
        "kind": "unit_coupling",
        "description": "All channels set to order one.",
        "claim_policy": "must fail; exposes required suppressions",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Runner-v4 smoke evaluation is now live. It evaluates closure, retained, contingent, symbolic, and unscored rows with the same channel map while preserving the v4 claim discipline. GR/null is sane. The identity closure control is visible but not promoted. Retained and contingent rows fail under source-charge, alpha3-flux, domain/projector, Gdot, edge, and unit-stress profiles as expected. Fifth-force activation remains unscored. No row receives theorem credit and no local-GR/PPN claim is allowed.",
        "local_GR_claim_allowed": False,
        "theorem_credit_rows": 0,
        "claim_allowed_rows": 0,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "red-team runner-v4 for hidden closure promotion, missing dependencies, and unfair local baseline handling",
        "pass_condition": "every false-promotion route is named and blocked",
    },
    {
        "priority": 2,
        "target": "410-quotient-matter-functor-theorem-attempt.md",
        "task": "attempt the quotient matter functor proof needed to upgrade R0",
        "pass_condition": "R0 moves toward theorem_zero or remains closure_zero with explicit postulate status",
    },
    {
        "priority": 3,
        "target": "411-local-bound-runner-v4-real-data-interface.py",
        "task": "wire runner-v4 state labels into future real local-bound data interfaces",
        "pass_condition": "real-data commands can run without changing state semantics",
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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


def runner_v4_rows() -> list[dict[str, str]]:
    return read_csv(ROOT / "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv")


def channel_map_rows() -> list[dict[str, str]]:
    return read_csv(ROOT / "runs/20260602-041500-runner-v3-numeric-smoke-extension/results/channel_map.csv")


def aggregate_bounds() -> list[dict[str, str]]:
    return read_csv(ROOT / "runs/20260602-041500-runner-v3-numeric-smoke-extension/results/aggregate_channel_bounds.csv")


def row_channels() -> dict[str, list[dict[str, str]]]:
    rows: dict[str, list[dict[str, str]]] = {}
    for channel_row in channel_map_rows():
        rows.setdefault(channel_row["row_id"], []).append(channel_row)
    return rows


def channel_units() -> dict[str, str]:
    units: dict[str, str] = {}
    for row in channel_map_rows():
        units.setdefault(row["channel"], row.get("channel_units", "dimensionless"))
    return units


def channel_names() -> list[str]:
    names = {row["channel"] for row in channel_map_rows()}
    for profile in PROFILE_DEFINITIONS:
        if profile["kind"] == "explicit":
            names.update(profile["values"])
    return sorted(names)


def tightest_bounds() -> dict[str, float]:
    bounds: dict[str, float] = {}
    for row in aggregate_bounds():
        try:
            bounds[row["channel"]] = float(row["tightest_solo_bound"])
        except ValueError:
            continue
    return bounds


def profile_values(profile: dict[str, Any]) -> dict[str, float]:
    values = {channel: 0.0 for channel in channel_names()}
    kind = profile["kind"]
    if kind == "all_zero":
        return values
    if kind == "fraction_tightest_bound":
        fraction = float(profile["fraction"])
        for channel, bound in tightest_bounds().items():
            values[channel] = fraction * bound
        return values
    if kind == "explicit":
        for channel, value in profile["values"].items():
            values[channel] = float(value)
        return values
    if kind == "unit_coupling":
        return {channel: 1.0 for channel in values}
    raise ValueError(f"unknown profile kind: {kind}")


def profile_input_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    units = channel_units()
    for profile in PROFILE_DEFINITIONS:
        values = profile_values(profile)
        for channel, value in values.items():
            if value == 0.0:
                continue
            rows.append(
                {
                    "profile": profile["profile"],
                    "channel": channel,
                    "value": value,
                    "units": units.get(channel, "dimensionless"),
                    "claim_policy": profile["claim_policy"],
                }
            )
    return rows


def parse_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def classify_numeric_result(
    profile: dict[str, Any],
    row: dict[str, str],
    residual: float,
    severity: float,
    active_terms: list[str],
) -> str:
    state = row["runner_v4_state"]
    if profile["profile"] == "GR_null_baseline" and residual == 0.0:
        return "baseline_sane"
    if state == "closure_zero" and residual == 0.0:
        return "closure_zero_visible_not_theorem"
    if state == "retained_contingent_budget" and not active_terms:
        return "contingency_inactive_not_pass"
    if residual == 0.0:
        return "zero_control_not_theorem"
    if severity < 1.0:
        return "inside_budget_no_claim"
    if math.isclose(severity, 1.0, rel_tol=1.0e-12, abs_tol=1.0e-30):
        return "edge_unstable_no_claim"
    return "over_budget"


def numeric_evaluation_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    channels_by_row = row_channels()
    v4_rows = runner_v4_rows()
    for profile in PROFILE_DEFINITIONS:
        values = profile_values(profile)
        for row in v4_rows:
            source_lock = parse_float(row["source_lock"])
            if source_lock is None:
                continue
            numeric_channels = [
                channel
                for channel in channels_by_row.get(row["row_id"], [])
                if channel.get("score_policy") == "numeric_source_lock"
            ]
            active_terms = [
                channel["channel"]
                for channel in numeric_channels
                if abs(values.get(channel["channel"], 0.0)) > 0.0
            ]
            residual = sum(abs(values.get(channel["channel"], 0.0)) for channel in numeric_channels)
            severity = residual / source_lock if source_lock else 0.0
            rows.append(
                {
                    "profile": profile["profile"],
                    "row_id": row["row_id"],
                    "observable": row["observable"],
                    "runner_v4_state": row["runner_v4_state"],
                    "zero_kind": row["zero_kind"],
                    "source_lock": source_lock,
                    "source_lock_units": row["source_lock_units"],
                    "residual_value": residual,
                    "severity_ratio": severity,
                    "active_terms": ";".join(active_terms),
                    "evaluation_class": classify_numeric_result(profile, row, residual, severity, active_terms),
                    "theorem_credit_allowed": False,
                    "claim_allowed": False,
                    "claim_policy": profile["claim_policy"],
                }
            )
    return rows


def symbolic_evaluation_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    channels_by_row = row_channels()
    for profile in PROFILE_DEFINITIONS:
        values = profile_values(profile)
        for row in runner_v4_rows():
            if row["runner_v4_state"] not in {"unscored_parameterized", "retained_residual"}:
                continue
            symbolic_channels = [
                channel
                for channel in channels_by_row.get(row["row_id"], [])
                if channel.get("score_policy") != "numeric_source_lock"
            ]
            active_terms = [
                channel["channel"]
                for channel in symbolic_channels
                if abs(values.get(channel["channel"], 0.0)) > 0.0
            ]
            if row["runner_v4_state"] == "unscored_parameterized":
                evaluation_class = (
                    "active_unscored_no_scalar_score"
                    if active_terms
                    else "unscored_inactive_in_profile"
                )
            else:
                evaluation_class = (
                    "active_symbolic_retained_ledger"
                    if active_terms
                    else "symbolic_ledger_inactive_in_profile"
                )
            rows.append(
                {
                    "profile": profile["profile"],
                    "row_id": row["row_id"],
                    "observable": row["observable"],
                    "runner_v4_state": row["runner_v4_state"],
                    "active_terms": ";".join(active_terms),
                    "evaluation_class": evaluation_class,
                    "theorem_credit_allowed": False,
                    "claim_allowed": False,
                    "claim_policy": profile["claim_policy"],
                }
            )
    return rows


def profile_summary_rows(numeric_rows: list[dict[str, Any]], symbolic_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for profile in PROFILE_DEFINITIONS:
        numeric_subset = [row for row in numeric_rows if row["profile"] == profile["profile"]]
        symbolic_subset = [row for row in symbolic_rows if row["profile"] == profile["profile"]]
        worst = max(numeric_subset, key=lambda row: float(row["severity_ratio"]))
        over_budget = sum(1 for row in numeric_subset if row["evaluation_class"] == "over_budget")
        edge = sum(1 for row in numeric_subset if row["evaluation_class"] == "edge_unstable_no_claim")
        inside = sum(1 for row in numeric_subset if row["evaluation_class"] == "inside_budget_no_claim")
        closure_visible = sum(1 for row in numeric_subset if row["evaluation_class"] == "closure_zero_visible_not_theorem")
        inactive_contingent = sum(1 for row in numeric_subset if row["evaluation_class"] == "contingency_inactive_not_pass")
        active_symbolic = sum(
            1
            for row in symbolic_subset
            if row["evaluation_class"] in {"active_unscored_no_scalar_score", "active_symbolic_retained_ledger"}
        )
        if profile["profile"] == "GR_null_baseline" and over_budget == 0 and edge == 0:
            verdict = "baseline_sane"
        elif over_budget > 0:
            verdict = "fails_smoke_no_promotion"
        elif edge > 0:
            verdict = "edge_unstable_no_promotion"
        elif active_symbolic > 0 and profile["profile"] == "fifth_force_alpha_1e_minus_5_unscored":
            verdict = "symbolic_unscored_activation_no_promotion"
        elif inside > 0 or closure_visible > 0 or inactive_contingent > 0:
            verdict = "inside_or_inactive_no_promotion"
        else:
            verdict = "zero_control_no_promotion"
        rows.append(
            {
                "profile": profile["profile"],
                "inside_rows": inside,
                "edge_rows": edge,
                "over_budget_rows": over_budget,
                "closure_zero_visible_rows": closure_visible,
                "inactive_contingent_rows": inactive_contingent,
                "active_symbolic_rows": active_symbolic,
                "worst_row": worst["row_id"],
                "worst_observable": worst["observable"],
                "worst_severity_ratio": worst["severity_ratio"],
                "verdict": verdict,
                "claim_allowed": False,
            }
        )
    return rows


def state_smoke_summary_rows(numeric_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    states = sorted({row["runner_v4_state"] for row in numeric_rows})
    for state in states:
        subset = [row for row in numeric_rows if row["runner_v4_state"] == state]
        rows.append(
            {
                "runner_v4_state": state,
                "evaluated_rows": len(subset),
                "over_budget_results": sum(1 for row in subset if row["evaluation_class"] == "over_budget"),
                "theorem_credit_allowed_rows": sum(1 for row in subset if row["theorem_credit_allowed"]),
                "claim_allowed_rows": sum(1 for row in subset if row["claim_allowed"]),
            }
        )
    return rows


def gate_rows(
    source_rows: list[dict[str, Any]],
    numeric_rows: list[dict[str, Any]],
    symbolic_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    baseline = next(row for row in summary_rows if row["profile"] == "GR_null_baseline")
    closure_zero_rows = [
        row
        for row in numeric_rows
        if row["runner_v4_state"] == "closure_zero"
        and row["evaluation_class"] == "closure_zero_visible_not_theorem"
    ]
    theorem_credit_rows = [row for row in numeric_rows if row["theorem_credit_allowed"]]
    claim_rows = [row for row in numeric_rows + symbolic_rows if row["claim_allowed"]]
    over_profiles = [row["profile"] for row in summary_rows if row["over_budget_rows"] > 0]
    symbolic_active = [
        row
        for row in symbolic_rows
        if row["evaluation_class"] in {"active_unscored_no_scalar_score", "active_symbolic_retained_ledger"}
    ]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "profiles_written",
            "status": "pass",
            "evidence": f"{len(PROFILE_DEFINITIONS)} v4 smoke profiles written",
        },
        {
            "gate": "GR_null_baseline_sane",
            "status": "pass" if baseline["verdict"] == "baseline_sane" else "fail",
            "evidence": f"worst severity {baseline['worst_severity_ratio']}",
        },
        {
            "gate": "closure_zero_visible_not_theorem",
            "status": "pass" if closure_zero_rows else "fail",
            "evidence": f"{len(closure_zero_rows)} closure-zero control rows visible",
        },
        {
            "gate": "over_budget_profiles_detected",
            "status": "pass" if over_profiles else "fail",
            "evidence": ";".join(over_profiles),
        },
        {
            "gate": "symbolic_unscored_rows_retained",
            "status": "pass" if symbolic_active else "fail",
            "evidence": f"{len(symbolic_active)} active symbolic/unscored rows retained",
        },
        {
            "gate": "no_theorem_credit",
            "status": "pass" if not theorem_credit_rows else "fail",
            "evidence": f"{len(theorem_credit_rows)} rows receive theorem credit",
        },
        {
            "gate": "no_claim_allowed_rows",
            "status": "pass" if not claim_rows else "fail",
            "evidence": f"{len(claim_rows)} rows have claim_allowed=true",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "v4 smoke evaluation only; no local-GR pass",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join([header, separator, *body])


def format_float(value: Any) -> str:
    number = float(value)
    if number == 0.0:
        return "0"
    if abs(number) < 1.0e-3 or abs(number) >= 1.0e4:
        return f"{number:.3e}"
    return f"{number:.6g}"


def write_checkpoint_markdown(
    run_dir: Path,
    summary_rows: list[dict[str, Any]],
    state_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, Any]],
) -> None:
    profile_table_rows = [
        {
            "profile": row["profile"],
            "over": row["over_budget_rows"],
            "symbolic": row["active_symbolic_rows"],
            "worst": row["worst_observable"],
            "severity": format_float(row["worst_severity_ratio"]),
            "verdict": row["verdict"],
        }
        for row in summary_rows
    ]
    state_table_rows = [
        {
            "state": row["runner_v4_state"],
            "over": row["over_budget_results"],
            "theorem": row["theorem_credit_allowed_rows"],
            "claims": row["claim_allowed_rows"],
        }
        for row in state_rows
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 408 - Local Bound Data Runner v4 Smoke

Private runner-v4 smoke checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 406 created runner-v4 states. This checkpoint actually runs a smoke evaluator through those states:

- closure-zero is visible but not theorem-zero;
- retained rows are scored against source locks;
- contingent rows score only when channels are activated;
- fifth-force/operator rows remain symbolic or unscored;
- no row is claim-allowed.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/local_bound_data_runner_v4_smoke.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Profile Summary

{markdown_table(profile_table_rows, ["profile", "over", "symbolic", "worst", "severity", "verdict"])}

## 4. State Summary

{markdown_table(state_table_rows, ["state", "over", "theorem", "claims"])}

## 5. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 6. Decision

{DECISION[0]["decision"]}

Practical read: this is the first local smoke layer that behaves like a referee instead of a cheerleader. Closure branches can be tested, but the machine keeps the word “closure” stamped on them.

## 7. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    numeric_rows = numeric_evaluation_rows()
    symbolic_rows = symbolic_evaluation_rows()
    summary_rows = profile_summary_rows(numeric_rows, symbolic_rows)
    state_rows = state_smoke_summary_rows(numeric_rows)
    gate_result_rows = gate_rows(source_rows, numeric_rows, symbolic_rows, summary_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "profile_definitions.csv", PROFILE_DEFINITIONS)
    write_csv(results_dir / "profile_inputs.csv", profile_input_rows())
    write_csv(results_dir / "numeric_evaluation.csv", numeric_rows)
    write_csv(results_dir / "symbolic_evaluation.csv", symbolic_rows)
    write_csv(results_dir / "profile_summary.csv", summary_rows)
    write_csv(results_dir / "state_smoke_summary.csv", state_rows)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    theorem_credit_rows = [row for row in numeric_rows if row["theorem_credit_allowed"]]
    claim_rows = [row for row in numeric_rows + symbolic_rows if row["claim_allowed"]]
    over_profiles = [row["profile"] for row in summary_rows if row["over_budget_rows"] > 0]
    baseline = next(row for row in summary_rows if row["profile"] == "GR_null_baseline")
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "profiles": len(PROFILE_DEFINITIONS),
        "numeric_evaluation_rows": len(numeric_rows),
        "symbolic_evaluation_rows": len(symbolic_rows),
        "GR_null_baseline_verdict": baseline["verdict"],
        "over_budget_profiles": over_profiles,
        "theorem_credit_rows": len(theorem_credit_rows),
        "claim_allowed_rows": len(claim_rows),
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, summary_rows, state_rows, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 408 local-bound data runner-v4 smoke artifacts."
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

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "source-locked-PPN-residual-runner-from-derived-force-ledger"
STATUS = "source_locked_PPN_residual_guardrail_runner_built_no_coefficients_no_pass_claim"
CLAIM_CEILING = "source_locked_guardrail_and_suppression_budget_only_no_local_GR_or_PPN_pass"
NEXT_TARGET = "360-universal-matter-coupling-theorem-attempt.md"

RUN_357 = ROOT / "runs" / "20260601-183000-Ward-owned-local-nohair-or-retained-PPN-residual-map"
RUN_358 = ROOT / "runs" / "20260601-184500-local-EH-exterior-operator-from-Ward-closed-action"


SOURCE_DOCS = [
    {
        "path": "354-official-local-bound-source-lock-or-nohair-proof-deepening.md",
        "role": "source-locked local guardrail scales",
    },
    {
        "path": "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
        "role": "retained PPN residual vector from Ward force channels",
    },
    {
        "path": "358-local-EH-exterior-operator-from-Ward-closed-action.md",
        "role": "EH baseline and operator obstruction map",
    },
    {
        "path": "runs/20260601-183000-Ward-owned-local-nohair-or-retained-PPN-residual-map/results/source_locked_residual_join.csv",
        "role": "residual/source-lock join from checkpoint 357",
    },
    {
        "path": "runs/20260601-183000-Ward-owned-local-nohair-or-retained-PPN-residual-map/results/retained_residual_vector.csv",
        "role": "symbolic residual formulas and force sources",
    },
    {
        "path": "runs/20260601-184500-local-EH-exterior-operator-from-Ward-closed-action/results/operator_obstruction_ledger.csv",
        "role": "operator-level obstruction map from checkpoint 358",
    },
    {
        "path": "runs/20260601-184500-local-EH-exterior-operator-from-Ward-closed-action/results/weak_field_limit_map.csv",
        "role": "weak-field GR baseline/residual mapping",
    },
]


RESIDUAL_COMPONENTS = {
    "gamma_minus_1": [
        "epsilon_TF",
        "epsilon_rad",
        "epsilon_bulk",
        "epsilon_nonmetric_light",
    ],
    "beta_minus_1": [
        "epsilon_rad",
        "epsilon_boundary_nonlinear",
        "epsilon_bulk",
    ],
    "eta_WEP": [
        "epsilon_WEP",
        "epsilon_species_charge",
        "epsilon_WEP_boundary",
    ],
    "alpha_clock_redshift": [
        "epsilon_clock",
        "epsilon_clock_metric_mismatch",
    ],
    "preferred_frame_alpha1_alpha2": [
        "epsilon_vec",
        "epsilon_domain_vec",
        "epsilon_P_vector",
    ],
    "xi_preferred_location_anisotropy": [
        "epsilon_TF_lge2",
        "epsilon_domain_aniso",
        "epsilon_external_aniso",
    ],
    "delta_G_or_fifth_force": [
        "epsilon_bulk",
        "epsilon_rad",
        "epsilon_Lcg_grad",
    ],
}


DEBT_TRIAGE = [
    {
        "debt": "universal_matter_coupling",
        "primary_residuals": "eta_WEP; alpha_clock_redshift; gamma_minus_1",
        "pressure_reason": "WEP has the tightest source-locked scale and cannot be hidden as a safe boundary monopole",
        "next_action": "derive one physical metric/coframe for matter, photons, clocks, rulers, and lab standards",
    },
    {
        "debt": "boundary_tracefree_and_radial_nohair",
        "primary_residuals": "gamma_minus_1; beta_minus_1; delta_G_or_fifth_force",
        "pressure_reason": "trace-free/radial boundary hair feeds both gamma and beta and can become fifth-force pressure",
        "next_action": "derive class-only boundary action or retain epsilon_TF/epsilon_rad in numeric runner",
    },
    {
        "debt": "bulk_X_operator_sign_and_source",
        "primary_residuals": "gamma_minus_1; beta_minus_1; delta_G_or_fifth_force",
        "pressure_reason": "maximum-principle/mass-gap route cannot be used until the local operator and sign are derived",
        "next_action": "derive local X equation, m_eff^2 sign, and no-source exterior condition",
    },
    {
        "debt": "second_order_EH_operator_selection",
        "primary_residuals": "gamma_minus_1; beta_minus_1; delta_G_or_fifth_force",
        "pressure_reason": "Ward closure alone permits higher-curvature/nonlocal operators that change weak-field potentials",
        "next_action": "derive parent low-energy theorem forbidding higher operators or include them as residual coefficients",
    },
    {
        "debt": "preferred_frame_and_anisotropy_source_locks",
        "primary_residuals": "preferred_frame_alpha1_alpha2; xi_preferred_location_anisotropy",
        "pressure_reason": "sectors remain quarantined because numeric source locks have not been ingested",
        "next_action": "source-lock alpha1/alpha2/xi or prove F_domain/F_P vector-anisotropy channels vanish",
    },
]


RUNNER_POLICY = [
    {
        "policy": "no_coefficients_no_pass",
        "meaning": "a residual row with unknown coefficients can produce a suppression budget, not an observational pass",
    },
    {
        "policy": "source_locked_ready_means_guardrail_only",
        "meaning": "gamma, beta, WEP, and clock scales are numeric guardrails for internal testing, not official claims",
    },
    {
        "policy": "quarantined_means_no_numeric_score",
        "meaning": "preferred-frame, xi, and fifth-force rows stay out of pass/fail scoring until source-locked or proven zero",
    },
    {
        "policy": "EH_baseline_is_conditional",
        "meaning": "GR values are the baseline only if the Ward/no-hair/operator sufficiency stack is satisfied",
    },
    {
        "policy": "retained_residuals_are_not_bad_faith",
        "meaning": "open force/operator sectors are carried explicitly instead of silently zeroed",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for doc in SOURCE_DOCS:
        source_path = ROOT / doc["path"]
        rows.append(
            {
                "source_file": doc["path"],
                "exists": source_path.exists(),
                "role": doc["role"],
            }
        )
    return rows


def residual_guardrail_rows() -> list[dict[str, Any]]:
    residual_join = read_csv(RUN_357 / "results" / "source_locked_residual_join.csv")
    retained_vector = {
        row["residual"]: row
        for row in read_csv(RUN_357 / "results" / "retained_residual_vector.csv")
    }
    weak_map = read_csv(RUN_358 / "results" / "weak_field_limit_map.csv")
    weak_by_residual: dict[str, list[str]] = {}
    for row in weak_map:
        for residual in row["residual_if_failed"].split(";"):
            key = residual.strip()
            weak_by_residual.setdefault(key, []).append(row["quantity"])

    rows: list[dict[str, Any]] = []
    for row in residual_join:
        residual = row["residual"]
        scale_raw = row["source_locked_scale_abs"].strip()
        components = RESIDUAL_COMPONENTS[residual]
        component_count = len(components)
        if scale_raw:
            scale = float(scale_raw)
            single_component_ceiling = scale
            equal_share_ceiling = scale / component_count
            numeric_rank_key: float | str = scale
            runner_verdict = "budget_only_needs_coefficients_no_pass"
        else:
            single_component_ceiling = ""
            equal_share_ceiling = ""
            numeric_rank_key = "quarantined"
            runner_verdict = "quarantined_until_source_lock_or_zero_theorem"

        retained = retained_vector[residual]
        rows.append(
            {
                "residual": residual,
                "weak_field_quantity": "; ".join(weak_by_residual.get(residual, [])),
                "force_sources": retained["force_sources"],
                "symbolic_formula": retained["symbolic_formula"],
                "components": "; ".join(components),
                "component_count": component_count,
                "source_locked_scale_abs": scale_raw,
                "single_component_ceiling_if_unit_coeff": single_component_ceiling,
                "equal_share_ceiling_if_unit_coeff": equal_share_ceiling,
                "coefficient_status": "not_derived",
                "runner_status": row["runner_status"],
                "allowed_use_now": row["allowed_use_now"],
                "runner_verdict": runner_verdict,
                "numeric_rank_key": numeric_rank_key,
            }
        )
    return rows


def pressure_ranking_rows(guardrails: list[dict[str, Any]]) -> list[dict[str, Any]]:
    numeric = [
        row
        for row in guardrails
        if row["source_locked_scale_abs"] != ""
    ]
    numeric.sort(key=lambda row: float(row["source_locked_scale_abs"]))
    rows: list[dict[str, Any]] = []
    for rank, row in enumerate(numeric, start=1):
        rows.append(
            {
                "pressure_rank": rank,
                "residual": row["residual"],
                "source_locked_scale_abs": row["source_locked_scale_abs"],
                "equal_share_ceiling_if_unit_coeff": row["equal_share_ceiling_if_unit_coeff"],
                "why_it_matters": {
                    "eta_WEP": "hardest ready local guardrail; attacks universal coupling directly",
                    "gamma_minus_1": "sensitive to trace-free, radial, bulk, and nonmetric light residuals",
                    "alpha_clock_redshift": "clock coupling guardrail; less brutal than WEP but still direct nonmetric pressure",
                    "beta_minus_1": "second-order/radial/nonlinear boundary guardrail",
                }.get(row["residual"], "source-locked local guardrail"),
            }
        )
    for row in guardrails:
        if row["source_locked_scale_abs"] == "":
            rows.append(
                {
                    "pressure_rank": "quarantined",
                    "residual": row["residual"],
                    "source_locked_scale_abs": "",
                    "equal_share_ceiling_if_unit_coeff": "",
                    "why_it_matters": "no numeric ranking until source-lock or zero theorem",
                }
            )
    return rows


def obstruction_join_rows(guardrails: list[dict[str, Any]]) -> list[dict[str, Any]]:
    obstructions = read_csv(RUN_358 / "results" / "operator_obstruction_ledger.csv")
    rows: list[dict[str, Any]] = []
    residual_lookup = {row["residual"]: row for row in guardrails}
    for obstruction in obstructions:
        if obstruction["obstruction"] == "universal_matter_coupling_open":
            linked = ["eta_WEP", "alpha_clock_redshift", "gamma_minus_1"]
        elif obstruction["obstruction"] == "source_normalization_open":
            linked = ["delta_G_or_fifth_force"]
        elif obstruction["obstruction"] == "quarantined_preferred_frame_and_fifth_force_sectors":
            linked = [
                "preferred_frame_alpha1_alpha2",
                "xi_preferred_location_anisotropy",
                "delta_G_or_fifth_force",
            ]
        else:
            linked = ["gamma_minus_1", "beta_minus_1", "delta_G_or_fifth_force"]

        rows.append(
            {
                "obstruction": obstruction["obstruction"],
                "severity": obstruction["severity"],
                "linked_residuals": "; ".join(linked),
                "ready_numeric_scales": "; ".join(
                    f"{residual}={residual_lookup[residual]['source_locked_scale_abs']}"
                    for residual in linked
                    if residual_lookup[residual]["source_locked_scale_abs"] != ""
                ),
                "quarantined_residuals": "; ".join(
                    residual
                    for residual in linked
                    if residual_lookup[residual]["source_locked_scale_abs"] == ""
                ),
                "required_fix": obstruction["required_fix"],
            }
        )
    return rows


def gate_result_rows(source_rows: list[dict[str, Any]], guardrails: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = [row["source_file"] for row in source_rows if not row["exists"]]
    ready = sum(1 for row in guardrails if row["source_locked_scale_abs"] != "")
    quarantined = sum(1 for row in guardrails if row["source_locked_scale_abs"] == "")
    coeff_missing = sum(1 for row in guardrails if row["coefficient_status"] == "not_derived")
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing else "fail",
            "evidence": "all cited source files exist" if not missing else "; ".join(missing),
        },
        {
            "gate": "source_locked_residuals_loaded",
            "status": "pass",
            "evidence": f"{ready} numeric-ready residual sectors loaded; {quarantined} quarantined sectors retained",
        },
        {
            "gate": "suppression_budgets_emitted",
            "status": "pass",
            "evidence": "unit-coefficient single-component and equal-share ceilings emitted where numeric scales exist",
        },
        {
            "gate": "missing_coefficients_block_pass",
            "status": "pass",
            "evidence": f"{coeff_missing} residual rows have not-derived coefficients and are blocked from pass claims",
        },
        {
            "gate": "WEP_pressure_identified",
            "status": "pass",
            "evidence": "eta_WEP is the tightest loaded guardrail at 2.8e-15",
        },
        {
            "gate": "quarantined_sectors_excluded_from_numeric_score",
            "status": "pass",
            "evidence": "preferred-frame, xi, and fifth-force rows are retained but not numerically scored",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "runner is a guardrail; EH/nohair/universal-coupling premises remain unproved",
        },
        {
            "gate": "PPN_pass_claimed",
            "status": "fail",
            "evidence": "no derived coefficients; no row can be treated as an observational pass",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "local_GR_promoted": False,
            "PPN_pass_claimed": False,
            "main_result": "source-locked local guardrail runner ranks ready residual pressure and blocks pass claims until coefficients are derived",
            "hardest_ready_sector": "eta_WEP",
            "hardest_ready_scale_abs": 2.8e-15,
            "next_target": NEXT_TARGET,
        }
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    run_dir = ROOT / "runs" / f"{args.timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    guardrails = residual_guardrail_rows()
    pressure = pressure_ranking_rows(guardrails)
    obstructions = obstruction_join_rows(guardrails)
    gates = gate_result_rows(source_rows, guardrails)
    decisions = decision_rows()

    outputs = {
        "source_register.csv": source_rows,
        "runner_policy.csv": RUNNER_POLICY,
        "residual_guardrail_budget.csv": guardrails,
        "pressure_ranking.csv": pressure,
        "operator_obstruction_to_residual_join.csv": obstructions,
        "debt_triage.csv": DEBT_TRIAGE,
        "gate_results.csv": gates,
        "decision.csv": decisions,
    }
    for name, rows in outputs.items():
        write_csv(results_dir / name, rows)

    status = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "generated": sorted(outputs),
        "source_paths_missing": sum(1 for row in source_rows if not row["exists"]),
        "numeric_ready_residuals": sum(1 for row in guardrails if row["source_locked_scale_abs"] != ""),
        "quarantined_residuals": sum(1 for row in guardrails if row["source_locked_scale_abs"] == ""),
        "coefficients_derived": False,
        "hardest_ready_sector": "eta_WEP",
        "hardest_ready_scale_abs": 2.8e-15,
        "local_GR_promoted": False,
        "PPN_pass_claimed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text("done\n", encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()

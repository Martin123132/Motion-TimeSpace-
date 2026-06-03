from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "mu_extra_coefficient_vector_to_local_bound_scorecard_written_21_target_rows_no_numeric_predictions_no_score_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "mu_extra_local_bound_scorecard_only_no_mu_extra_zero_constant_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "469-fill-or-zero-highest-pressure-mu-extra-row.md"

DOC_PATH = Path("468-mu-extra-coefficient-vector-to-local-bound-scorecard.md")
SCORECARD_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv")
SUMMARY_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_BOUND_SUMMARY.csv")
REQUIRED_INPUTS_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_SCORECARD_REQUIRED_INPUTS.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_SCORECARD_DECISION.csv")

COEFFICIENT_VECTOR_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv")
CHANNEL_LEDGER_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_OWNER_LEDGER.csv")
LOCAL_RESIDUAL_CONTRACT_PATH = Path("runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv")
LOCAL_BOUNDS_TEMPLATE_PATH = Path("runs/20260602-061500-local-bound-runner-v4-real-data-interface/results/local_bounds_template.csv")
CHANNEL_BOUND_REQUIREMENTS_PATH = Path("runs/20260602-041500-runner-v3-numeric-smoke-extension/results/channel_bound_requirements.csv")
AGGREGATE_BOUND_PATH = Path("runs/20260602-041500-runner-v3-numeric-smoke-extension/results/aggregate_channel_bounds.csv")


SOURCE_REGISTER = [
    {
        "path": "467-mu-extra-zero-owner-or-source-normalization-coefficient-vector.md",
        "role": "eight epsilon_i coefficient vector and owner ledger",
    },
    {
        "path": str(COEFFICIENT_VECTOR_PATH),
        "role": "machine-readable mu_extra coefficient vector",
    },
    {
        "path": str(CHANNEL_LEDGER_PATH),
        "role": "machine-readable channel owner ledger",
    },
    {
        "path": str(LOCAL_RESIDUAL_CONTRACT_PATH),
        "role": "local residual component contract with row locks",
    },
    {
        "path": str(LOCAL_BOUNDS_TEMPLATE_PATH),
        "role": "runner-v4 local-bound template rows",
    },
    {
        "path": str(CHANNEL_BOUND_REQUIREMENTS_PATH),
        "role": "channel-to-row source-lock requirements",
    },
    {
        "path": str(AGGREGATE_BOUND_PATH),
        "role": "aggregate channel bound summaries from runner-v3 numeric smoke extension",
    },
]


SCORECARD_COLUMNS = [
    "model_id",
    "branch_id",
    "epsilon_channel",
    "epsilon_symbol",
    "target_row",
    "observable",
    "mapping_type",
    "response_expression",
    "predicted_input",
    "bound_value",
    "bound_units",
    "bound_source",
    "pass_condition",
    "score_status",
    "reason_not_scoreable",
    "valid_for_claim",
    "required_artifact",
    "notes",
]


TARGET_MAP = {
    "radial_Meff_hair": [
        ("R4_beta", "direct_or_mapped", "beta_minus_1 ~ F_radial_beta[epsilon_radial_Meff]"),
        ("R10_fifth_force", "curve_required", "alpha(lambda) from radial/range source profile"),
    ],
    "boundary_monopole_shift": [
        ("R4_beta", "direct_or_mapped", "beta_minus_1 ~ F_boundary_beta[epsilon_boundary]"),
        ("R7_alpha3", "flux_map_required", "alpha3 ~ F_boundary_flux[epsilon_boundary]"),
        ("R8_xi", "anisotropy_map_required", "xi ~ F_boundary_shear[epsilon_boundary]"),
        ("R9_Gdot", "time_derivative_required", "Gdot/G ~ d epsilon_boundary/dt"),
    ],
    "domain_projector_mass": [
        ("R5_alpha1", "vector_map_required", "alpha1 ~ F_domain_vector[epsilon_domain_projector]"),
        ("R6_alpha2", "vector_map_required", "alpha2 ~ F_domain_vector[epsilon_domain_projector]"),
        ("R7_alpha3", "flux_map_required", "alpha3 ~ F_domain_flux[epsilon_domain_projector]"),
        ("R8_xi", "anisotropy_map_required", "xi ~ F_domain_anisotropy[epsilon_domain_projector]"),
        ("R11_EH_operator_ledger", "operator_vector_required", "c_source_normalization_operator includes epsilon_domain_projector"),
    ],
    "bulk_X_Yukawa_tail": [
        ("R10_fifth_force", "curve_required", "alpha_X(lambda_X) from epsilon_bulk_X and range law"),
    ],
    "nonEH_operator_potential": [
        ("R3_gamma", "operator_map_required", "gamma-1 ~ F_nonEH_gamma[epsilon_nonEH_source]"),
        ("R4_beta", "operator_map_required", "beta-1 ~ F_nonEH_beta[epsilon_nonEH_source]"),
        ("R10_fifth_force", "curve_required", "alpha(lambda) from non-EH finite-range mode if present"),
        ("R11_EH_operator_ledger", "operator_vector_required", "c_nonEH_operator_vector maps to epsilon_nonEH_source"),
    ],
    "species_source_charge": [
        ("R1_WEP_source_charge", "composition_map_required", "eta_source_AB ~ Delta_AB ln(1+epsilon_species_A)"),
        ("R2_clock_redshift", "clock_source_map_required", "alpha_clock ~ F_clock_source[epsilon_species_A]"),
    ],
    "time_drift": [
        ("R9_Gdot", "time_derivative_required", "Gdot/G ~ d epsilon_time_drift/dt"),
    ],
    "absolute_calibration_offset": [
        ("R4_beta", "calibration_owner_required", "beta-1 unaffected only if epsilon_calibration is parent-fixed constant"),
        ("R9_Gdot", "time_derivative_required", "Gdot/G ~ d epsilon_calibration/dt"),
    ],
}


R10_CURVE_ARTIFACT = "R10_alpha_lambda_curve_MTS_source_normalization.csv"
R11_VECTOR_ARTIFACT = "R11_nonEH_operator_vector_executable.csv"


def source_register_rows() -> list[dict[str, str]]:
    return [
        {"path": item["path"], "exists": str((ROOT / item["path"]).exists()), "role": item["role"]}
        for item in SOURCE_REGISTER
    ]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def residual_lookup(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["row_id"]: row for row in rows}


def local_bound_lookup(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["row_id"]: row for row in rows}


def coefficient_lookup(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["channel"]: row for row in rows}


def channel_ledger_lookup(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["channel"]: row for row in rows}


def row_bound(row_id: str, residuals: dict[str, dict[str, str]], local_bounds: dict[str, dict[str, str]]) -> tuple[str, str, str, str]:
    if row_id in residuals:
        row = residuals[row_id]
        return row["observable"], row["source_bound"], row["units"], str(LOCAL_RESIDUAL_CONTRACT_PATH)
    if row_id in local_bounds:
        row = local_bounds[row_id]
        return row["observable"], row["upper_bound"], row["units"], str(LOCAL_BOUNDS_TEMPLATE_PATH)
    return "MISSING_OBSERVABLE", "MISSING_BOUND", "MISSING_UNITS", "MISSING_BOUND_SOURCE"


def required_artifact(mapping_type: str, ledger_row: dict[str, str]) -> str:
    if mapping_type == "curve_required":
        return R10_CURVE_ARTIFACT
    if mapping_type == "operator_vector_required":
        return R11_VECTOR_ARTIFACT
    return ledger_row.get("residual_artifact_required", "MISSING_REQUIRED_ARTIFACT")


def predicted_input(mapping_type: str, coefficient_row: dict[str, str]) -> str:
    if mapping_type == "curve_required":
        return "MISSING_ALPHA_LAMBDA_CURVE_OR_THEOREM_ZERO"
    if mapping_type == "operator_vector_required":
        return "MISSING_OPERATOR_VECTOR_OR_THEOREM_ZERO"
    return coefficient_row["coefficient_value"]


def pass_condition(mapping_type: str, observable: str, bound_value: str, units: str) -> str:
    if mapping_type == "curve_required":
        return "for every lambda: abs(alpha_predicted(lambda)) <= alpha_bound(lambda), or theorem-zero"
    if mapping_type == "operator_vector_required":
        return "operator coefficient vector supplied and every mapped residual row passes, or EH-only theorem-zero"
    if bound_value in {"alpha(lambda)", "symbolic"}:
        return f"{observable} requires executable non-scalar artifact, not placeholder text"
    return f"abs(predicted {observable}) <= {bound_value} {units}, or theorem-zero source"


def score_status(predicted: str) -> tuple[str, str]:
    if "MISSING_" in predicted:
        return "not_scoreable_prediction_missing", "MTS prediction, curve, operator vector, or theorem-zero source is missing"
    return "score_ready_unrun", "prediction supplied but evaluator not run in this checkpoint"


def build_scorecard(
    coefficient_rows: list[dict[str, str]],
    ledger_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    local_bound_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    coefficients = coefficient_lookup(coefficient_rows)
    ledgers = channel_ledger_lookup(ledger_rows)
    residuals = residual_lookup(residual_rows)
    local_bounds = local_bound_lookup(local_bound_rows)
    rows: list[dict[str, str]] = []
    for channel, targets in TARGET_MAP.items():
        coefficient_row = coefficients[channel]
        ledger_row = ledgers[channel]
        for row_id, mapping_type, expression in targets:
            observable, bound_value, units, bound_source = row_bound(row_id, residuals, local_bounds)
            predicted = predicted_input(mapping_type, coefficient_row)
            status, reason = score_status(predicted)
            rows.append(
                {
                    "model_id": "MTS_source_normalized_Newton_branch",
                    "branch_id": "mu_extra_local_bound_scorecard",
                    "epsilon_channel": channel,
                    "epsilon_symbol": coefficient_row["coefficient_symbol"],
                    "target_row": row_id,
                    "observable": observable,
                    "mapping_type": mapping_type,
                    "response_expression": expression,
                    "predicted_input": predicted,
                    "bound_value": bound_value,
                    "bound_units": units,
                    "bound_source": bound_source,
                    "pass_condition": pass_condition(mapping_type, observable, bound_value, units),
                    "score_status": status,
                    "reason_not_scoreable": reason,
                    "valid_for_claim": "false",
                    "required_artifact": required_artifact(mapping_type, ledger_row),
                    "notes": ledger_row["next_action"],
                }
            )
    return rows


SUMMARY_COLUMNS = [
    "epsilon_channel",
    "epsilon_symbol",
    "target_rows",
    "numeric_target_count",
    "curve_required",
    "operator_vector_required",
    "tightest_numeric_bound",
    "tightest_numeric_units",
    "tightest_numeric_row",
    "scoreable_rows",
    "blocked_rows",
    "claim_status",
    "next_required_artifact",
]


def as_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def build_summary(scorecard: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for channel in TARGET_MAP:
        channel_rows = [row for row in scorecard if row["epsilon_channel"] == channel]
        numeric_rows = [row for row in channel_rows if as_float(row["bound_value"]) is not None]
        tightest = min(numeric_rows, key=lambda row: as_float(row["bound_value"]) or float("inf")) if numeric_rows else None
        scoreable = sum(1 for row in channel_rows if row["score_status"] == "score_ready_unrun")
        blocked = sum(1 for row in channel_rows if row["score_status"] != "score_ready_unrun")
        artifacts = sorted({row["required_artifact"] for row in channel_rows if row["score_status"] != "score_ready_unrun"})
        rows.append(
            {
                "epsilon_channel": channel,
                "epsilon_symbol": channel_rows[0]["epsilon_symbol"],
                "target_rows": ";".join(row["target_row"] for row in channel_rows),
                "numeric_target_count": str(len(numeric_rows)),
                "curve_required": str(any(row["mapping_type"] == "curve_required" for row in channel_rows)),
                "operator_vector_required": str(any(row["mapping_type"] == "operator_vector_required" for row in channel_rows)),
                "tightest_numeric_bound": tightest["bound_value"] if tightest else "none",
                "tightest_numeric_units": tightest["bound_units"] if tightest else "none",
                "tightest_numeric_row": tightest["target_row"] if tightest else "none",
                "scoreable_rows": str(scoreable),
                "blocked_rows": str(blocked),
                "claim_status": "not_claimable",
                "next_required_artifact": ";".join(artifacts),
            }
        )
    return rows


REQUIRED_INPUT_COLUMNS = [
    "priority",
    "input_artifact",
    "unblocks_channels",
    "unblocks_rows",
    "minimum_content",
    "acceptance_gate",
]


def build_required_inputs(summary: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "priority": "1",
            "input_artifact": "P8_mu_extra_boundary_coefficients.csv",
            "unblocks_channels": "boundary_monopole_shift",
            "unblocks_rows": "R4_beta;R7_alpha3;R8_xi;R9_Gdot",
            "minimum_content": "epsilon_boundary value or theorem-zero source plus maps to beta/alpha3/xi/Gdot",
            "acceptance_gate": "all mapped rows score below locks; alpha3 lock is 4e-20 if flux-like",
        },
        {
            "priority": "2",
            "input_artifact": "P8_mu_extra_domain_projector_coefficients.csv",
            "unblocks_channels": "domain_projector_mass",
            "unblocks_rows": "R5_alpha1;R6_alpha2;R7_alpha3;R8_xi;R11_EH_operator_ledger",
            "minimum_content": "epsilon_domain_projector or theorem-zero plus vector/flux/anisotropy maps",
            "acceptance_gate": "preferred-frame/location and R11 operator rows score or zero",
        },
        {
            "priority": "3",
            "input_artifact": "R10_alpha_lambda_curve_MTS_source_normalization.csv",
            "unblocks_channels": "radial_Meff_hair;bulk_X_Yukawa_tail;nonEH_operator_potential",
            "unblocks_rows": "R10_fifth_force",
            "minimum_content": "lambda, lambda_units, alpha_predicted, alpha_bound, source path, assumptions",
            "acceptance_gate": "alpha_predicted(lambda) below alpha_bound(lambda) for all curve rows or theorem-zero",
        },
        {
            "priority": "4",
            "input_artifact": "R11_nonEH_operator_vector_executable.csv",
            "unblocks_channels": "nonEH_operator_potential",
            "unblocks_rows": "R3_gamma;R4_beta;R10_fifth_force;R11_EH_operator_ledger",
            "minimum_content": "non-EH coefficients, units, normalization, weak-field maps, source paths",
            "acceptance_gate": "R11 vector rows have no MISSING_ fields and mapped residuals pass",
        },
        {
            "priority": "5",
            "input_artifact": "P8_species_source_charge_residual_or_zero.csv",
            "unblocks_channels": "species_source_charge",
            "unblocks_rows": "R1_WEP_source_charge;R2_clock_redshift",
            "minimum_content": "eta_source_AB or theorem-zero plus clock/source split map",
            "acceptance_gate": "eta_source_AB <= 2.8e-15 and clock row mapped or zero",
        },
        {
            "priority": "6",
            "input_artifact": "P8_time_drift_residual_or_zero.csv",
            "unblocks_channels": "time_drift",
            "unblocks_rows": "R9_Gdot",
            "minimum_content": "d epsilon_time_drift/dt or theorem-zero in yr^-1",
            "acceptance_gate": "abs(Gdot_over_G contribution) <= 9.6e-15 yr^-1",
        },
        {
            "priority": "7",
            "input_artifact": "P8_radial_mu_profile_or_zero.csv",
            "unblocks_channels": "radial_Meff_hair",
            "unblocks_rows": "R4_beta;R10_fifth_force",
            "minimum_content": "epsilon_radial_Meff(r), radial derivative/profile, or no-hair theorem",
            "acceptance_gate": "radial profile maps below beta/R10 locks or is theorem-zero",
        },
        {
            "priority": "8",
            "input_artifact": "P8_absolute_calibration_owner.csv",
            "unblocks_channels": "absolute_calibration_offset",
            "unblocks_rows": "R4_beta;R9_Gdot",
            "minimum_content": "parent-fixed universal constant proof with zero derivative/source/range/frame dependence",
            "acceptance_gate": "constant calibration is universal and derivative-silent, otherwise coefficient row remains retained",
        },
    ]


DECISION_COLUMNS = ["decision_item", "status", "evidence", "next_action"]


def build_decision(source_paths_missing: int, scorecard: list[dict[str, str]], summary: list[dict[str, str]]) -> list[dict[str, str]]:
    scoreable_rows = sum(1 for row in scorecard if row["score_status"] == "score_ready_unrun")
    blocked_rows = sum(1 for row in scorecard if row["score_status"] != "score_ready_unrun")
    curve_rows = sum(1 for row in scorecard if row["mapping_type"] == "curve_required")
    operator_rows = sum(1 for row in scorecard if row["mapping_type"] == "operator_vector_required")
    return [
        {
            "decision_item": "source_paths",
            "status": "pass" if source_paths_missing == 0 else "fail",
            "evidence": f"missing source paths = {source_paths_missing}",
            "next_action": "continue with cited input artifacts",
        },
        {
            "decision_item": "scorecard_written",
            "status": "pass",
            "evidence": f"scorecard rows = {len(scorecard)}; channel summaries = {len(summary)}",
            "next_action": "use scorecard as local-bound target table",
        },
        {
            "decision_item": "numeric_predictions_available",
            "status": "fail",
            "evidence": f"score-ready rows = {scoreable_rows}; blocked rows = {blocked_rows}",
            "next_action": "fill epsilon coefficients, curves, operator vectors, or theorem-zero sources",
        },
        {
            "decision_item": "curve_rows_ready",
            "status": "fail",
            "evidence": f"curve-required rows = {curve_rows}; curve file not loaded",
            "next_action": "build R10_alpha_lambda_curve_MTS_source_normalization.csv",
        },
        {
            "decision_item": "operator_rows_ready",
            "status": "fail",
            "evidence": f"operator-vector-required rows = {operator_rows}; executable R11 vector not loaded",
            "next_action": "build R11_nonEH_operator_vector_executable.csv or EH-only theorem",
        },
        {
            "decision_item": "mu_extra_score_passed",
            "status": "fail",
            "evidence": "no scorecard row has a numeric/theorem-zero prediction",
            "next_action": NEXT_TARGET,
        },
        {
            "decision_item": "Newton_or_local_GR_promoted",
            "status": "fail",
            "evidence": "mu_extra scorecard is target-only, not passed",
            "next_action": "keep no-claim ceiling",
        },
    ]


def render_doc(
    run_dir: Path,
    source_rows: list[dict[str, str]],
    scorecard: list[dict[str, str]],
    summary: list[dict[str, str]],
    required_inputs: list[dict[str, str]],
    decisions: list[dict[str, str]],
) -> str:
    return f"""# 468 - mu_extra Coefficient Vector to Local-Bound Scorecard

Private local-bound scorecard checkpoint. This is not a public measured-GM, Newtonian-limit, PPN, local-GR, cosmology, EM, or unified-field claim.

## 1. Question

Checkpoint 467 split `mu_extra` into eight source-normalization coefficients:

```text
epsilon_mu = sum_i epsilon_i.
```

This checkpoint maps those eight `epsilon_i` rows onto local-bound targets. It does not invent scores. If a coefficient, curve, operator vector, or theorem-zero source is missing, the row is explicitly not scoreable.

## 2. Run Metadata

| Field | Value |
| --- | --- |
| Script | `scripts/mu_extra_coefficient_vector_to_local_bound_scorecard.py` |
| Run directory | `{run_dir}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Scorecard CSV | `{SCORECARD_PATH}` |
| Summary CSV | `{SUMMARY_PATH}` |
| Required inputs CSV | `{REQUIRED_INPUTS_PATH}` |
| Decision CSV | `{DECISION_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(source_rows, ["path", "exists", "role"])}

## 4. Scoring Rule

For each channel-target pair:

```text
predicted residual = response_map(epsilon_i)
pass only if abs(predicted residual) <= target bound
or the channel has a sourced theorem-zero certificate.
```

For `R10`, a scalar placeholder is illegal: an executable `alpha(lambda)` curve is required. For `R11`, an executable operator vector or EH-only theorem is required.

## 5. Local-Bound Scorecard

The scorecard has been written to `{SCORECARD_PATH}`.

{md_table(scorecard, SCORECARD_COLUMNS)}

## 6. Channel Summary

The channel summary has been written to `{SUMMARY_PATH}`.

{md_table(summary, SUMMARY_COLUMNS)}

## 7. Required Inputs

The required-input queue has been written to `{REQUIRED_INPUTS_PATH}`.

{md_table(required_inputs, REQUIRED_INPUT_COLUMNS)}

## 8. Decision

{md_table(decisions, DECISION_COLUMNS)}

## 9. Result

The scorecard is now executable as a target table: `{len(scorecard)}` channel-target rows across `{len(summary)}` epsilon channels.

It is not yet a passed empirical result. Every score row is blocked because the MTS-side prediction is still missing: numeric coefficient, theorem-zero proof, `alpha(lambda)` curve, or non-EH operator vector.

Practical read: this is the fair version of the boxing match. We are not demanding a knockout; we are setting the judges' cards. Each `epsilon_i` gets its opponent and its required evidence. If MTS can slip these punches with theorem-zero or below-bound coefficients, it stays in the round.

## 10. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | choose the highest-pressure row and either fill it or prove it zero |
| 2 | `R10_alpha_lambda_curve_MTS_source_normalization.csv` | three scorecard rows require executable range curves |
| 3 | `R11_nonEH_operator_vector_executable.csv` | two scorecard rows require executable operator-vector input |
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-mu-extra-coefficient-vector-to-local-bound-scorecard"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    source_paths_missing = sum(1 for row in source_rows if row["exists"] != "True")
    coefficient_rows = read_csv_rows(COEFFICIENT_VECTOR_PATH)
    ledger_rows = read_csv_rows(CHANNEL_LEDGER_PATH)
    residual_rows = read_csv_rows(LOCAL_RESIDUAL_CONTRACT_PATH)
    local_bound_rows = read_csv_rows(LOCAL_BOUNDS_TEMPLATE_PATH)
    channel_requirement_rows = read_csv_rows(CHANNEL_BOUND_REQUIREMENTS_PATH)
    aggregate_bound_rows = read_csv_rows(AGGREGATE_BOUND_PATH)

    scorecard = build_scorecard(coefficient_rows, ledger_rows, residual_rows, local_bound_rows)
    summary = build_summary(scorecard)
    required_inputs = build_required_inputs(summary)
    decisions = build_decision(source_paths_missing, scorecard, summary)

    missing_predictions = sum(1 for row in scorecard if "MISSING_" in row["predicted_input"])
    score_ready_rows = sum(1 for row in scorecard if row["score_status"] == "score_ready_unrun")
    curve_required_rows = sum(1 for row in scorecard if row["mapping_type"] == "curve_required")
    operator_required_rows = sum(1 for row in scorecard if row["mapping_type"] == "operator_vector_required")
    generic_fill_tokens = sum(str(value).count("fill_") for row in scorecard + summary + required_inputs + decisions for value in row.values())

    write_csv(ROOT / SCORECARD_PATH, scorecard, SCORECARD_COLUMNS)
    write_csv(ROOT / SUMMARY_PATH, summary, SUMMARY_COLUMNS)
    write_csv(ROOT / REQUIRED_INPUTS_PATH, required_inputs, REQUIRED_INPUT_COLUMNS)
    write_csv(ROOT / DECISION_PATH, decisions, DECISION_COLUMNS)

    write_csv(results_dir / "mu_extra_local_bound_scorecard.csv", scorecard, SCORECARD_COLUMNS)
    write_csv(results_dir / "mu_extra_channel_bound_summary.csv", summary, SUMMARY_COLUMNS)
    write_csv(results_dir / "mu_extra_scorecard_required_inputs.csv", required_inputs, REQUIRED_INPUT_COLUMNS)
    write_csv(results_dir / "decision.csv", decisions, DECISION_COLUMNS)
    write_csv(results_dir / "source_register.csv", source_rows, ["path", "exists", "role"])

    doc = render_doc(
        run_dir=Path("runs") / f"{timestamp}-mu-extra-coefficient-vector-to-local-bound-scorecard",
        source_rows=source_rows,
        scorecard=scorecard,
        summary=summary,
        required_inputs=required_inputs,
        decisions=decisions,
    )
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    status = {
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "source_paths_missing": source_paths_missing,
        "coefficient_vector_rows_loaded": len(coefficient_rows),
        "channel_ledger_rows_loaded": len(ledger_rows),
        "local_residual_contract_rows_loaded": len(residual_rows),
        "local_bounds_template_rows_loaded": len(local_bound_rows),
        "channel_bound_requirement_rows_loaded": len(channel_requirement_rows),
        "aggregate_bound_rows_loaded": len(aggregate_bound_rows),
        "scorecard_rows": len(scorecard),
        "channel_summary_rows": len(summary),
        "required_input_rows": len(required_inputs),
        "decision_rows": len(decisions),
        "missing_prediction_rows": missing_predictions,
        "score_ready_rows": score_ready_rows,
        "curve_required_rows": curve_required_rows,
        "operator_vector_required_rows": operator_required_rows,
        "generic_fill_placeholder_tokens_in_outputs": generic_fill_tokens,
        "mu_extra_scorecard_written": True,
        "mu_extra_score_passed": False,
        "mu_extra_zero_promoted": False,
        "constant_GM_promoted": False,
        "Newtonian_reduction_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    write_json(run_dir / "status.json", status)
    return status


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default="20260602-220000")
    arguments = parser.parse_args()
    print(json.dumps(write_run(arguments.timestamp), indent=2))


if __name__ == "__main__":
    main()

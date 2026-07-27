from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
OUT = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = ROOT / "scripts" / "Y5_R10_finite_kappa_alpha_bound_input_fill_and_prior_discipline.py"
DOC_PATH = ROOT / "645-Y5-R10-finite-kappa-alpha-bound-input-fill-and-prior-discipline.md"

STATUS = "Y5_R10_finite_kappa_alpha_prior_discipline_staged_clock_first_bound_fill_selected_nonclaim"
CLAIM_CEILING = "finite_kappa_alpha_input_plumbing_only_no_numeric_score_no_alpha_variation_claim_no_R10_WEP_clock_or_local_pass"
NEXT_TARGET = "646-Y5-R10-clock-alpha-sensitivity-source-fill-or-finite-prior-runner.md"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_register_rows() -> list[dict[str, object]]:
    sources = [
        ("S645_0", "checkpoint_644_doc", ROOT / "644-Y5-R10-parent-vertical-norm-coupling-owner-proof-or-demotion.md", "zero-route demotion and finite-branch trigger"),
        ("S645_1", "validation_644", OUT / "P8_Y5_BRR545_644_VALIDATION.csv", "prior validation input"),
        ("S645_2", "next_contract_644", OUT / "P8_Y5_R10_644_NEXT_CONTRACT.csv", "finite-branch next contract"),
        ("S645_3", "nonclaim_summary_644", OUT / "P8_Y5_R10_644_NONCLAIM_SUMMARY.csv", "demotion status source"),
        ("S645_4", "pressure_smoke_642", OUT / "P8_Y5_R10_642_PRESSURE_RUNNER_SMOKE.csv", "symbolic finite pressure rows"),
        ("S645_5", "cross_arena_reaction_641", OUT / "P8_Y5_R10_641_CROSS_ARENA_REACTION_MATRIX.csv", "arena reaction expressions"),
        ("S645_6", "local_bound_matrix_639", OUT / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv", "available local bound rows"),
        ("S645_7", "generator_script_645", SCRIPT_PATH, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": source_id,
            "label": label,
            "path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for source_id, label, path, role in sources
    ]


def finite_prior_rows() -> list[dict[str, object]]:
    return [
        {
            "prior_id": "KP645_0_zero_theorem_demoted",
            "branch": "kappa_alpha_zero",
            "definition": "kappa_alpha = D_v ln(alpha_EM) / D chi_X = 0",
            "status": "demoted_closure_contract",
            "allowed_use": "bookkeeping only; not an active evidence branch",
            "units": "per_dimensionless_chi_X_if_chi_X_is_later_defined",
            "numeric_values": "0",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "KP645_1_sign_free_log_sensitivity",
            "branch": "finite_sign_free",
            "definition": "kappa_alpha may be positive or negative; scan log-spaced absolute normalized factors",
            "status": "allowed_for_smoke_only",
            "allowed_use": "pressure/sensitivity runner after input maps exist",
            "units": "UNDEFINED_UNTIL_CHI_X_OR_XHAT_UNIT_DEFINED",
            "numeric_values": "-10,-1,-0.1,0.1,1,10 as normalized nonphysical probes",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "KP645_2_near_zero_linear_sensitivity",
            "branch": "finite_near_zero",
            "definition": "small signed normalized factors around zero for stability checks",
            "status": "allowed_for_smoke_only",
            "allowed_use": "detect whether future maps are catastrophically sensitive near zero",
            "units": "UNDEFINED_UNTIL_CHI_X_OR_XHAT_UNIT_DEFINED",
            "numeric_values": "-0.01,-0.001,0.001,0.01 as normalized nonphysical probes",
            "valid_for_claim": "false",
        },
        {
            "prior_id": "KP645_3_bound_saturating_diagnostic",
            "branch": "finite_bound_saturating",
            "definition": "solve |prediction(kappa_alpha)| = bound after projection maps exist",
            "status": "blocked",
            "allowed_use": "future diagnostic only",
            "units": "requires_bound_specific_tau_and_sensitivity_units",
            "numeric_values": "MISSING_PROJECTION_MAPS",
            "valid_for_claim": "false",
        },
    ]


def finite_coordinate_rows() -> list[dict[str, object]]:
    return [
        {
            "coordinate_id": "XC645_0_dimensionless_chi_X",
            "candidate_definition": "chi_X = Xhat / X0 or an equivalent dimensionless parent-local alpha-pressure coordinate",
            "current_status": "not_derived",
            "needed_to_score": "yes",
            "risk_if_missing": "kappa_alpha values are pure normalized probes and cannot be compared to bounds",
            "next_action": "derive X0 from parent vertical norm or explicitly declare a nonclaim finite prior scale",
            "valid_for_claim": "false",
        },
        {
            "coordinate_id": "XC645_1_local_delta_chi_X",
            "candidate_definition": "Delta chi_X for each arena: lab clock, WEP source/test body, R10 body separation, EM spectra setting",
            "current_status": "missing",
            "needed_to_score": "yes",
            "risk_if_missing": "bounds on observables cannot be turned into bounds on kappa_alpha",
            "next_action": "build arena-specific tau maps before any numeric score",
            "valid_for_claim": "false",
        },
    ]


def bound_input_rows() -> list[dict[str, object]]:
    local_bounds = {row["row_id"]: row for row in read_csv(OUT / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv")}
    selected = [
        ("BI645_0", "R2_clock_redshift", "clock_alpha_first", "direct_alpha_channel", "first_fill_target"),
        ("BI645_1", "R0_identity_coframe_direct", "WEP_direct_geometry", "composition_alpha_channel", "second_target"),
        ("BI645_2", "R1_WEP_source_charge", "WEP_source_charge", "composition_source_channel", "second_target"),
        ("BI645_3", "R10_fifth_force", "R10_short_range", "source_binding_channel", "third_target"),
    ]
    rows: list[dict[str, object]] = []
    for input_id, row_id, label, channel, priority in selected:
        source = local_bounds[row_id]
        rows.append(
            {
                "input_id": input_id,
                "source_row_id": row_id,
                "label": label,
                "arena": source["arena"],
                "observable": source["observable"],
                "bound_value": source["bound_value"],
                "bound_units": source["bound_units"],
                "bound_kind": source["bound_kind"],
                "reference_path_or_url": source["reference_path_or_url"],
                "prediction_law": source["prediction_law"],
                "required_mts_inputs": source["required_mts_inputs"],
                "alpha_channel": channel,
                "priority": priority,
                "numeric_score_ready": "false",
                "valid_for_claim": "false",
            }
        )
    rows.append(
        {
            "input_id": "BI645_4",
            "source_row_id": "EM_spectra_source_slot",
            "label": "EM_spectra_alpha_stability",
            "arena": "atomic/molecular/astrophysical spectra",
            "observable": "delta_alpha_over_alpha_or_transition_shift",
            "bound_value": "MISSING_SOURCE",
            "bound_units": "dimensionless_or_frequency_ratio",
            "bound_kind": "source_slot",
            "reference_path_or_url": "MISSING_SOURCE",
            "prediction_law": "delta_alpha/alpha ~ tau_EM kappa_alpha Delta chi_X",
            "required_mts_inputs": "kappa_alpha;tau_EM;Delta_chi_X;spectral_sensitivity_coefficients",
            "alpha_channel": "direct_alpha_channel",
            "priority": "source_acquisition_target",
            "numeric_score_ready": "false",
            "valid_for_claim": "false",
        }
    )
    return rows


def projection_readiness_rows() -> list[dict[str, object]]:
    return [
        {
            "readiness_id": "PR645_0_clock",
            "target_input": "BI645_0",
            "observable_projection": "alpha_clock ~ tau_clock (K_a_alpha - K_b_alpha) kappa_alpha",
            "has_numeric_bound": "true",
            "has_tau_map": "false",
            "has_sensitivity_coefficients": "false",
            "has_chi_X_unit": "false",
            "score_state": "blocked_but_first_target",
            "next_missing_input": "clock sensitivity pair K_a_alpha,K_b_alpha plus tau_clock",
            "valid_for_claim": "false",
        },
        {
            "readiness_id": "PR645_1_WEP",
            "target_input": "BI645_1;BI645_2",
            "observable_projection": "eta_AB ~ tau_WEP beta_source sum_i[(S_Ai-S_Bi) kappa_i]",
            "has_numeric_bound": "true",
            "has_tau_map": "false",
            "has_sensitivity_coefficients": "false",
            "has_chi_X_unit": "false",
            "score_state": "blocked",
            "next_missing_input": "material composition alpha sensitivities and source normalization beta_source",
            "valid_for_claim": "false",
        },
        {
            "readiness_id": "PR645_2_R10",
            "target_input": "BI645_3",
            "observable_projection": "alpha_R10(lambda) ~ tau_R10 beta_source beta_test c_eff(lambda)",
            "has_numeric_bound": "range_dependent_bound_source_exists_but_projection_missing",
            "has_tau_map": "false",
            "has_sensitivity_coefficients": "false",
            "has_chi_X_unit": "false",
            "score_state": "blocked",
            "next_missing_input": "body EM binding/source response, tau_R10(lambda), Z/lambda normalization",
            "valid_for_claim": "false",
        },
        {
            "readiness_id": "PR645_3_EM_spectra",
            "target_input": "BI645_4",
            "observable_projection": "delta_alpha/alpha ~ tau_EM kappa_alpha Delta chi_X",
            "has_numeric_bound": "false",
            "has_tau_map": "false",
            "has_sensitivity_coefficients": "false",
            "has_chi_X_unit": "false",
            "score_state": "source_missing",
            "next_missing_input": "source-backed spectra/clock alpha-stability bound and sensitivity coefficients",
            "valid_for_claim": "false",
        },
    ]


def acquisition_queue_rows() -> list[dict[str, object]]:
    return [
        {
            "queue_id": "AQ645_0_clock_alpha_sensitivity",
            "target": "clock sensitivity coefficients",
            "why_first": "clock row is the most direct alpha-channel bound already present in the local matrix",
            "required_fields": "transition_pair;K_a_alpha;K_b_alpha;tau_clock;bound_source;units;sign_convention",
            "success_condition": "can compute symbolic-to-numeric alpha_clock prediction without material composition model",
            "status": "selected_next",
            "valid_for_claim": "false",
        },
        {
            "queue_id": "AQ645_1_WEP_composition_sensitivity",
            "target": "material alpha sensitivities for WEP bodies",
            "why_first": "strong bound but more model-dependent than clocks",
            "required_fields": "material_A;material_B;S_A_alpha;S_B_alpha;beta_source;tau_WEP;bound_source",
            "success_condition": "eta_AB projection can be evaluated without hidden source-charge assumptions",
            "status": "queued",
            "valid_for_claim": "false",
        },
        {
            "queue_id": "AQ645_2_R10_body_binding",
            "target": "R10 source/test EM binding response",
            "why_first": "needed for short-range alpha pressure but indirect",
            "required_fields": "body_materials;beta_source;beta_test;tau_R10(lambda);lambda_X;Z_eff;bound_curve",
            "success_condition": "alpha(lambda) prediction uses sourced body response rather than raw alpha_EM derivative",
            "status": "queued",
            "valid_for_claim": "false",
        },
        {
            "queue_id": "AQ645_3_EM_spectra_bound",
            "target": "source-backed alpha stability/spectra bound",
            "why_first": "direct alpha channel but no row currently present in local matrix",
            "required_fields": "dataset;observable;bound_value;bound_units;sensitivity_coefficients;tau_EM",
            "success_condition": "new EM_spectra row has source path/url and numeric bound",
            "status": "source_slot",
            "valid_for_claim": "false",
        },
    ]


def score_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "SG645_0_zero_route",
            "gate": "zero theorem is active evidence",
            "result": "fail_demoted",
            "blocks": "using kappa_alpha=0 as proof",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "SG645_1_units",
            "gate": "finite kappa_alpha has physical chi_X/Xhat units",
            "result": "fail_missing",
            "blocks": "numeric finite score",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "SG645_2_tau_maps",
            "gate": "arena projection tau maps exist",
            "result": "fail_missing",
            "blocks": "clock/WEP/R10/EM score",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "SG645_3_sensitivities",
            "gate": "clock/material/spectral sensitivity coefficients exist",
            "result": "fail_missing",
            "blocks": "alpha-channel observable predictions",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "SG645_4_claim_policy",
            "gate": "no row valid_for_claim until all previous gates pass",
            "result": "pass_policy",
            "blocks": "overclaiming",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D645_0",
            "route": "clock_alpha_sensitivity_first",
            "decision": "selected",
            "why": "R2 has a numeric bound and the cleanest direct alpha projection once K coefficients and tau_clock are sourced",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D645_1",
            "route": "finite_prior_runner",
            "decision": "blocked_until_inputs",
            "why": "priors exist only as normalized probes until chi_X/Xhat units and tau maps are sourced",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "zero_route_demoted": "true",
            "finite_branch_active": "true_nonclaim",
            "selected_first_fill": "clock_alpha_sensitivity",
            "numeric_score_allowed": "false",
            "strongest_positive_result": "finite branch is now disciplined: priors, bound rows, and first acquisition target are explicit",
            "hardest_blocker": "physical chi_X/Xhat unit plus tau_clock and clock alpha sensitivity coefficients are still missing",
            "next_target": NEXT_TARGET,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    prior_rows: list[dict[str, object]],
    coordinate_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    projection_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    score_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V645_0_source_paths_exist", all(row["exists"] == "true" for row in source_rows), "all cited local source paths exist"))
    prior_validation = read_csv(OUT / "P8_Y5_BRR545_644_VALIDATION.csv")
    checks.append(("V645_1_prior_644_validation_clean", all(row.get("result") == "pass" for row in prior_validation), "644 validation remains clean"))
    prior_summary = read_csv(OUT / "P8_Y5_R10_644_NONCLAIM_SUMMARY.csv")[0]
    checks.append(("V645_2_zero_route_demoted_imported", prior_summary.get("zero_route_demoted") == "true", "zero route demotion imported"))
    checks.append(("V645_3_priors_nonclaim", all(row["valid_for_claim"] == "false" for row in prior_rows), "finite priors are nonclaim"))
    checks.append(("V645_4_coordinate_blocks_score", all(row["needed_to_score"] == "yes" and row["valid_for_claim"] == "false" for row in coordinate_rows), "coordinate/unit rows block score"))
    required_labels = {"clock_alpha_first", "WEP_direct_geometry", "WEP_source_charge", "R10_short_range"}
    checks.append(("V645_5_bound_rows_include_major_targets", required_labels.issubset({row["label"] for row in bound_rows}), "clock/WEP/R10 bound rows included"))
    checks.append(("V645_6_no_bound_row_score_ready", all(row["numeric_score_ready"] == "false" and row["valid_for_claim"] == "false" for row in bound_rows), "no bound row is score-ready"))
    checks.append(("V645_7_clock_selected_first", any(row["target"] == "clock sensitivity coefficients" and row["status"] == "selected_next" for row in acquisition_rows), "clock sensitivity selected first"))
    checks.append(("V645_8_projection_rows_blocked", all(row["score_state"] != "ready" and row["valid_for_claim"] == "false" for row in projection_rows), "projection rows remain blocked"))
    checks.append(("V645_9_score_gates_closed", all(row["valid_for_claim"] == "false" for row in score_rows) and any(row["gate_id"] == "SG645_4_claim_policy" and row["result"] == "pass_policy" for row in score_rows), "score gates are closed with policy gate"))
    checks.append(("V645_10_decisions_nonclaim", all(row["valid_for_claim"] == "false" for row in decision), "decision rows do not claim pass"))
    checks.append(("V645_11_summary_nonclaim", summary[0]["numeric_score_allowed"] == "false" and summary[0]["selected_first_fill"] == "clock_alpha_sensitivity", "summary stays nonclaim and selects clock target"))

    fw = ROOT.parent / "formalization-workbench"
    cutoff = datetime(2026, 5, 31, 14, 42, 0).timestamp()
    changed_after_cutoff = 0
    if fw.exists():
        for path in fw.rglob("*"):
            if path.is_file() and path.stat().st_mtime > cutoff:
                changed_after_cutoff += 1
    checks.append(("V645_12_formalization_workbench_unchanged", changed_after_cutoff == 0, f"formalization files changed after cutoff: {changed_after_cutoff}"))

    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now_iso(),
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("|", "\\|").replace("\n", " ")
            values.append(text)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    source_rows: list[dict[str, object]],
    prior_rows: list[dict[str, object]],
    coordinate_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    projection_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    score_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 645 Y5/R10 Finite Kappa-Alpha Bound Input Fill and Prior Discipline",
        "",
        "## Verdict",
        "",
        f"- Status: `{STATUS}`",
        f"- Claim ceiling: `{CLAIM_CEILING}`",
        "- The zero theorem stays demoted. Finite `kappa_alpha` is now the active private branch, but only as input plumbing.",
        "- Priors are normalized probes, not physical values, until a dimensionless `chi_X`/`Xhat` unit and arena `tau` maps exist.",
        "- First fill target selected: clock alpha sensitivity, because it is the cleanest direct alpha channel already represented in the bound matrix.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["source_id", "label", "path", "exists", "role"]),
        "",
        "## Finite Prior Discipline",
        "",
        markdown_table(prior_rows, ["prior_id", "branch", "status", "units", "numeric_values", "allowed_use"]),
        "",
        "## Finite Coordinate Requirement",
        "",
        markdown_table(coordinate_rows, ["coordinate_id", "candidate_definition", "current_status", "needed_to_score", "risk_if_missing", "next_action"]),
        "",
        "## Bound Input Ledger",
        "",
        markdown_table(bound_rows, ["input_id", "label", "observable", "bound_value", "bound_units", "alpha_channel", "priority", "numeric_score_ready"]),
        "",
        "## Projection Readiness",
        "",
        markdown_table(projection_rows, ["readiness_id", "target_input", "observable_projection", "score_state", "next_missing_input"]),
        "",
        "## Acquisition Queue",
        "",
        markdown_table(acquisition_rows, ["queue_id", "target", "status", "required_fields", "success_condition"]),
        "",
        "## Score Gates",
        "",
        markdown_table(score_rows, ["gate_id", "gate", "result", "blocks"]),
        "",
        "## Decision",
        "",
        markdown_table(decision, ["decision_id", "route", "decision", "why", "next_target"]),
        "",
        "## Validation",
        "",
        markdown_table(validation, ["check_id", "result", "detail"]),
        "",
        "## Interpretation",
        "",
        "- This is the engineering pivot: stop pretending alpha is silent and build the finite-coupling measurement corridor.",
        "- The first real punch is not R10. It is clocks, because their alpha sensitivity channel is direct and less source-composition tangled.",
        "- A future numeric run is allowed only after the clock sensitivity coefficients, `tau_clock`, and `chi_X` unit are real.",
        "",
        "## Nonclaim Summary",
        "",
        markdown_table(summary, ["status", "zero_route_demoted", "finite_branch_active", "selected_first_fill", "numeric_score_allowed", "hardest_blocker", "next_target"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register_rows()
    prior_rows = finite_prior_rows()
    coordinate_rows = finite_coordinate_rows()
    bound_rows = bound_input_rows()
    projection_rows = projection_readiness_rows()
    acquisition_rows = acquisition_queue_rows()
    score_rows = score_gate_rows()
    decision = decision_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(
        source_rows,
        prior_rows,
        coordinate_rows,
        bound_rows,
        projection_rows,
        acquisition_rows,
        score_rows,
        decision,
        summary,
    )

    write_csv(OUT / "P8_Y5_R10_645_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_645_FINITE_PRIOR_DISCIPLINE.csv", prior_rows)
    write_csv(OUT / "P8_Y5_R10_645_FINITE_COORDINATE_REQUIREMENT.csv", coordinate_rows)
    write_csv(OUT / "P8_Y5_R10_645_BOUND_INPUT_LEDGER.csv", bound_rows)
    write_csv(OUT / "P8_Y5_R10_645_PROJECTION_READINESS.csv", projection_rows)
    write_csv(OUT / "P8_Y5_R10_645_ACQUISITION_QUEUE.csv", acquisition_rows)
    write_csv(OUT / "P8_Y5_R10_645_SCORE_GATES.csv", score_rows)
    write_csv(OUT / "P8_Y5_BRR545_645_DECISION.csv", decision)
    write_csv(OUT / "P8_Y5_R10_645_NONCLAIM_SUMMARY.csv", summary)
    write_csv(OUT / "P8_Y5_BRR545_645_VALIDATION.csv", validation)
    write_doc(source_rows, prior_rows, coordinate_rows, bound_rows, projection_rows, acquisition_rows, score_rows, decision, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"wrote_doc={DOC_PATH}")
    print(f"wrote_csv_dir={OUT}")
    print(f"bound_inputs={len(bound_rows)}")
    print(f"selected_first_fill=clock_alpha_sensitivity")
    print(f"validation_rows={len(validation)}")
    print(f"validation_failures={len(failures)}")
    print(f"status={STATUS}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for row in failures:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()

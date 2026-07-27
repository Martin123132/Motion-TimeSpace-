from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1202"
TITLE = "1202-Y5-R10-conservative-geometry-kernel-or-qDT-profile-family"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
ASSUMPTIONS_PATH = OUT_DIR / f"{PACK_ID}_CONSERVATIVE_KERNEL_ASSUMPTIONS.csv"
SCENARIOS_PATH = OUT_DIR / f"{PACK_ID}_WR10_SCENARIO_FAMILY.csv"
ENVELOPE_PATH = OUT_DIR / f"{PACK_ID}_QDT_ALLOWED_ENVELOPE.csv"
PROFILE_REQUIREMENTS_PATH = OUT_DIR / f"{PACK_ID}_QDT_PROFILE_FAMILY_REQUIREMENTS.csv"
RUNNER_SUMMARY_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_SUMMARY.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1202_VALIDATION.csv"


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = ROOT / relative_path
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def fmt(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def md_escape(value: object) -> str:
    text = fmt(value)
    return text.replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1202_0_1201_handoff",
            "local_path": "1201-Y5-R10-WR10-official-kernel-source-or-toy-kernel-smoke-row.md",
            "needle": "NEXT1201_0_1202",
            "purpose": "handoff requiring a conservative kernel or qDT profile-family replacement for toy W_R10",
        },
        {
            "source_id": "SRC1202_1_1200_WR10_stub",
            "local_path": "1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md",
            "needle": "WRK1200_3_WR10_ratio",
            "purpose": "symbolic W_R10=N_DT/D_Y ratio and denominator positivity guard",
        },
        {
            "source_id": "SRC1202_2_1200_qDT_envelope",
            "local_path": "1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md",
            "needle": "QPE1200_0_total_envelope",
            "purpose": "absolute q_DT residual budget before R10 projection",
        },
        {
            "source_id": "SRC1202_3_1199_join_rule",
            "local_path": "1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md",
            "needle": "R10P1199_5_curve_join_rule",
            "purpose": "R10 pass inequality and no-cancellation rule",
        },
        {
            "source_id": "SRC1202_4_1199_W_definition",
            "local_path": "1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md",
            "needle": "R10P1199_2_W_R10_definition",
            "purpose": "definition of W_R10 as normalized R10 readout response",
        },
        {
            "source_id": "SRC1202_5_1035_harmonic_contract",
            "local_path": "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
            "needle": "KXD1035_4_R10_harmonic_projection",
            "purpose": "R10 harmonic projection contract precedent",
        },
        {
            "source_id": "SRC1202_6_437_yukawa_convention",
            "local_path": "437-R10-alpha-lambda-executable-curve-contract.md",
            "needle": "Yukawa_potential",
            "purpose": "alpha(lambda) Yukawa convention",
        },
        {
            "source_id": "SRC1202_7_review_candidate_curve",
            "local_path": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "needle": "R10_VECTOR_2020_REVIEW_0351",
            "purpose": "nonclaim review-candidate R10 alpha(lambda) curve used for private stress thresholds",
        },
    ]

    source_rows: list[dict[str, object]] = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_rows.append(
            {
                **spec,
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    assumptions = [
        {
            "assumption_id": "CGA1202_0_denominator_positive",
            "object": "D_Y(lambda)",
            "assumption": "For a private stress scenario only, normalize the unit-alpha Yukawa denominator to a finite positive value.",
            "formula_or_rule": "D_Y(lambda_i)=1 by declared scenario normalization; official R10 denominator still absent.",
            "source_anchor": "1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md::WRK1200_0_unit_alpha_denominator",
            "status": "SCENARIO_ASSUMPTION_NOT_OFFICIAL_KERNEL",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "assumption_id": "CGA1202_1_absolute_harmonic_sum",
            "object": "Pi_R10",
            "assumption": "Every retained harmonic and component is summed by absolute value; signed cancellation is banned.",
            "formula_or_rule": "Pi_R10 T -> sum_h |w_h T_h|; alpha_DT_envelope=W_R10*q_DT_bound.",
            "source_anchor": "1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md::R10P1199_5_curve_join_rule",
            "status": "CONSERVATIVE_GUARD_ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "assumption_id": "CGA1202_2_W_scenario_family",
            "object": "W_R10(lambda)",
            "assumption": "Use bracketed response multipliers W=1,10,100 to ask how small q_DT must be if projection leakage is matched, pessimistic, or brutal.",
            "formula_or_rule": "q_DT_allowed(lambda_i;W)=alpha_bound(lambda_i)/W.",
            "source_anchor": "1201-Y5-R10-WR10-official-kernel-source-or-toy-kernel-smoke-row.md::TOY1201_0_definition",
            "status": "PRIVATE_STRESS_ENVELOPE_NOT_EVIDENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "assumption_id": "CGA1202_3_curve_nonpromotion",
            "object": "R10 alpha_bound(lambda)",
            "assumption": "The review-candidate curve is used only to create nonclaim thresholds; it is not the live claim curve.",
            "formula_or_rule": "curve_valid_for_claim=false propagates to every 1202 envelope row.",
            "source_anchor": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "status": "NONCLAIM_REVIEW_CURVE_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    scenarios = [
        {
            "scenario_id": "WR10F1202_0_matched_yukawa",
            "scenario_name": "matched_yukawa_projection",
            "W_R10_assumed": 1.0,
            "denominator_rule": "D_Y=1 scenario normalization",
            "numerator_rule": "N_DT=1, qDT projects like unit-alpha Yukawa",
            "harmonic_guard": "absolute_sum_no_cancellation",
            "denominator_positive_assumed": True,
            "official_kernel": False,
            "status": "LOW_STRESS_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "scenario_id": "WR10F1202_1_pessimistic_10x",
            "scenario_name": "pessimistic_10x_projection",
            "W_R10_assumed": 10.0,
            "denominator_rule": "D_Y=1 scenario normalization",
            "numerator_rule": "N_DT=10, conservative harmonic/source leakage amplification",
            "harmonic_guard": "absolute_sum_no_cancellation",
            "denominator_positive_assumed": True,
            "official_kernel": False,
            "status": "PESSIMISTIC_STRESS_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "scenario_id": "WR10F1202_2_brutal_100x",
            "scenario_name": "brutal_100x_projection",
            "W_R10_assumed": 100.0,
            "denominator_rule": "D_Y=1 scenario normalization",
            "numerator_rule": "N_DT=100, intentionally harsh upper-envelope projection",
            "harmonic_guard": "absolute_sum_no_cancellation",
            "denominator_positive_assumed": True,
            "official_kernel": False,
            "status": "BRUTAL_STRESS_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    curve_path = ROOT / "source-intake" / "local_bounds" / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"
    curve_rows = load_csv(curve_path)
    sample_indices = [0, 195, 351, 389]
    envelope_rows: list[dict[str, object]] = []
    for sample_index in sample_indices:
        bound = curve_rows[sample_index]
        bound_id = bound.get("bound_id") or f"curve_row_{sample_index:04d}"
        alpha_bound = float(bound["alpha_bound"])
        lambda_value = float(bound["lambda_value"])
        curve_valid_for_claim = bound.get("valid_for_claim", "").strip().lower() == "true"
        for scenario in scenarios:
            w_value = float(scenario["W_R10_assumed"])
            qdt_allowed = alpha_bound / w_value
            toy_qdt_bound = 1.0
            alpha_from_toy = w_value * toy_qdt_bound
            toy_pass = abs(alpha_from_toy) <= alpha_bound
            envelope_rows.append(
                {
                    "row_id": f"QAE1202_{sample_index:04d}_{scenario['scenario_id']}",
                    "scenario_id": scenario["scenario_id"],
                    "source_bound_id": bound_id,
                    "source_curve_id": bound.get("curve_id", ""),
                    "sample_index": sample_index,
                    "lambda_value": lambda_value,
                    "lambda_units": bound.get("lambda_units", "m"),
                    "alpha_bound": alpha_bound,
                    "W_R10_assumed": w_value,
                    "qDT_allowed": qdt_allowed,
                    "toy_qDT_bound": toy_qdt_bound,
                    "alpha_from_toy_qDT": alpha_from_toy,
                    "toy_pass": toy_pass,
                    "curve_valid_for_claim": curve_valid_for_claim,
                    "valid_for_claim": False,
                    "claim_allowed": False,
                    "status": "SCENARIO_THRESHOLD_NONCLAIM",
                    "source_file": rel(curve_path),
                }
            )

    profile_requirements = [
        {
            "requirement_id": "QPR1202_0_G_res_profile",
            "component": "G_res^nu(x)",
            "needed_input": "profile_grid_or_formula; weighted norm; gauge/coframe/domain; units",
            "why_it_matters": "sets the source shape entering N_DT(lambda) and the residual amplitude entering q_DT_bound",
            "current_status": "PARENT_PROFILE_NOT_NUMERIC",
            "blocking_source_anchor": "1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md::GRP1199_0_G_res_profile",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "QPR1202_1_cokernel_fraction",
            "component": "f_coker",
            "needed_input": "D_T^dagger basis, inner product, local boundary class, projection norm",
            "why_it_matters": "dominates q_coker=f_coker||G_res|| if the local zero theorem stays unsigned",
            "current_status": "COKERNEL_PROJECTION_NOT_NUMERIC",
            "blocking_source_anchor": "1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md::GRP1199_1_P_coker_fraction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "QPR1202_2_boundary_norm",
            "component": "||B_T||",
            "needed_input": "boundary geometry, K_T trace norm, P_locV trace norm, zero certificate or finite bound",
            "why_it_matters": "boundary leakage must be zero or below the qDT_allowed threshold",
            "current_status": "BOUNDARY_NORM_NOT_NUMERIC",
            "blocking_source_anchor": "1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md::QPE1200_2_boundary_component",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "QPR1202_3_regularizer_residue",
            "component": "kappa_T C_T ||E_reg||",
            "needed_input": "regularizer coefficient, coercivity constant, residual norm, parent action status",
            "why_it_matters": "prevents a hidden regularizer residue from masquerading as GR recovery",
            "current_status": "REGULARIZER_INPUTS_NOT_NUMERIC",
            "blocking_source_anchor": "1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md::QPE1200_3_regularizer_component",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "QPR1202_4_projector_leakage",
            "component": "||Delta_P|| or eps_P||G_res||",
            "needed_input": "P_loc derivative, coframe/domain variation, C_CK eps_P absorption condition",
            "why_it_matters": "sets the gap between a clean quotient theorem and a residual local-force branch",
            "current_status": "PROJECTOR_LEAKAGE_NOT_NUMERIC",
            "blocking_source_anchor": "1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md::GRP1199_3_projector_leakage",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "QPR1202_5_profile_shape",
            "component": "G_DT_profile_shape",
            "needed_input": "normalized support/shape for the R10 numerator, or conservative envelope over allowed local profiles",
            "why_it_matters": "without this, W_R10 remains a scenario multiplier rather than an experiment-specific response",
            "current_status": "PROFILE_SHAPE_NOT_NUMERIC",
            "blocking_source_anchor": "1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md::QPE1200_5_profile_shape",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    min_row = min(envelope_rows, key=lambda row: float(row["qDT_allowed"]))
    toy_pass_count = sum(1 for row in envelope_rows if row["toy_pass"])
    toy_fail_count = len(envelope_rows) - toy_pass_count
    runner_summary = [
        {
            "summary_id": "RUN1202_0_conservative_envelope_runner",
            "status": "computed_nonclaim",
            "scenario_count": len(scenarios),
            "sample_count": len(sample_indices),
            "envelope_row_count": len(envelope_rows),
            "toy_pass_count": toy_pass_count,
            "toy_fail_count": toy_fail_count,
            "min_qDT_allowed": min_row["qDT_allowed"],
            "tightest_row_id": min_row["row_id"],
            "tightest_lambda_m": min_row["lambda_value"],
            "tightest_alpha_bound": min_row["alpha_bound"],
            "interpretation": "If W_R10 is as harsh as 100, q_DT must be below the quoted min threshold at the tightest sampled curve point; this is a private stress target, not a pass.",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    claim_gates = [
        {
            "gate_id": "GATE1202_0_official_WR10",
            "gate": "official or source-reconstructed W_R10(lambda)",
            "status": "BLOCKED",
            "reason": "1202 uses scenario multipliers, not official R10 geometry kernels.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1202_1_live_bound_curve",
            "gate": "promoted R10 alpha(lambda) curve",
            "status": "BLOCKED",
            "reason": "review-candidate curve remains valid_for_claim=false.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1202_2_parent_qDT_bound",
            "gate": "parent-derived numeric q_DT_bound components",
            "status": "BLOCKED",
            "reason": "G_res, f_coker, B_T, regularizer, projector leakage, and profile-shape inputs remain nonnumeric.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1202_3_claim_policy",
            "gate": "R10/local-GR pass",
            "status": "BLOCKED",
            "reason": "No 1202 row can be promoted because both theory-side and experiment-kernel sides are nonclaim.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_ledger = [
        {
            "decision_id": "DEC1202_0_route",
            "condition": "official W_R10 not acquired and q_DT components nonnumeric",
            "decision": "Use conservative W=1/10/100 stress envelopes to define target q_DT amplitudes.",
            "result": "R10 gate is now numerically interpretable as an allowed q_DT threshold, but it is still not evidence.",
            "next_action": "derive or bound q_DT component amplitudes against the tightest scenario threshold before any pass/fail claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    next_target = [
        {
            "next_id": "NEXT1202_0_1203",
            "target_file": "1203-Y5-R10-qDT-component-amplitude-law-against-conservative-envelope.md",
            "target_script": "scripts/Y5_R10_qDT_component_amplitude_law_against_conservative_envelope.py",
            "task": "derive or source numeric upper bounds for f_coker||G_res||, ||B_T||, kappa_T C_T||E_reg||, and ||Delta_P||, then compare their absolute sum against the 1202 qDT_allowed thresholds",
            "success_condition": "produce a parent-signed q_DT_bound_total or a precise blocked ledger showing which component prevents the R10/local-GR branch from becoming scoreable",
            "do_not_do": "do not claim R10 pass, do not promote review curve, do not tune signed cancellations, do not edit formalization-workbench, do not push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_fields = [
        "source_id",
        "local_path",
        "needle",
        "purpose",
        "path_exists",
        "needle_found",
        "valid_for_claim",
        "claim_allowed",
    ]
    assumption_fields = [
        "assumption_id",
        "object",
        "assumption",
        "formula_or_rule",
        "source_anchor",
        "status",
        "valid_for_claim",
        "claim_allowed",
    ]
    scenario_fields = [
        "scenario_id",
        "scenario_name",
        "W_R10_assumed",
        "denominator_rule",
        "numerator_rule",
        "harmonic_guard",
        "denominator_positive_assumed",
        "official_kernel",
        "status",
        "valid_for_claim",
        "claim_allowed",
    ]
    envelope_fields = [
        "row_id",
        "scenario_id",
        "source_bound_id",
        "source_curve_id",
        "sample_index",
        "lambda_value",
        "lambda_units",
        "alpha_bound",
        "W_R10_assumed",
        "qDT_allowed",
        "toy_qDT_bound",
        "alpha_from_toy_qDT",
        "toy_pass",
        "curve_valid_for_claim",
        "valid_for_claim",
        "claim_allowed",
        "status",
        "source_file",
    ]
    profile_fields = [
        "requirement_id",
        "component",
        "needed_input",
        "why_it_matters",
        "current_status",
        "blocking_source_anchor",
        "valid_for_claim",
        "claim_allowed",
    ]
    runner_fields = [
        "summary_id",
        "status",
        "scenario_count",
        "sample_count",
        "envelope_row_count",
        "toy_pass_count",
        "toy_fail_count",
        "min_qDT_allowed",
        "tightest_row_id",
        "tightest_lambda_m",
        "tightest_alpha_bound",
        "interpretation",
        "valid_for_claim",
        "claim_allowed",
    ]
    gate_fields = ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]
    decision_fields = ["decision_id", "condition", "decision", "result", "next_action", "valid_for_claim", "claim_allowed"]
    next_fields = ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"]

    write_csv(SOURCE_REGISTER_PATH, source_rows, source_fields)
    write_csv(ASSUMPTIONS_PATH, assumptions, assumption_fields)
    write_csv(SCENARIOS_PATH, scenarios, scenario_fields)
    write_csv(ENVELOPE_PATH, envelope_rows, envelope_fields)
    write_csv(PROFILE_REQUIREMENTS_PATH, profile_requirements, profile_fields)
    write_csv(RUNNER_SUMMARY_PATH, runner_summary, runner_fields)
    write_csv(CLAIM_GATES_PATH, claim_gates, gate_fields)
    write_csv(DECISION_LEDGER_PATH, decision_ledger, decision_fields)
    write_csv(NEXT_TARGET_PATH, next_target, next_fields)

    all_valid_flags_false = all(not bool(row.get("valid_for_claim")) for row in envelope_rows + scenarios + assumptions)
    source_paths_ok = all(bool(row["path_exists"]) for row in source_rows)
    source_needles_ok = all(bool(row["needle_found"]) for row in source_rows)
    scenario_values = sorted(float(row["W_R10_assumed"]) for row in scenarios)
    scenario_values_ok = scenario_values == [1.0, 10.0, 100.0]
    envelope_numeric_positive = all(float(row["lambda_value"]) > 0 and float(row["alpha_bound"]) > 0 and float(row["qDT_allowed"]) > 0 for row in envelope_rows)
    gate_bites = any(float(row["qDT_allowed"]) < 1.0 for row in envelope_rows)
    claim_gates_blocked = all(row["status"] == "BLOCKED" and not bool(row["valid_for_claim"]) for row in claim_gates)
    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if mtime >= RUN_STARTED_UTC:
                    formalization_recent.append(path)
    formalization_untouched = len(formalization_recent) == 0
    csvs_to_parse = [
        SOURCE_REGISTER_PATH,
        ASSUMPTIONS_PATH,
        SCENARIOS_PATH,
        ENVELOPE_PATH,
        PROFILE_REQUIREMENTS_PATH,
        RUNNER_SUMMARY_PATH,
        CLAIM_GATES_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
    ]
    csv_parse_ok = True
    parse_details: list[str] = []
    for csv_path in csvs_to_parse:
        try:
            rows = load_csv(csv_path)
            parse_details.append(f"{csv_path.name}:{len(rows)}")
        except Exception as exc:  # noqa: BLE001
            csv_parse_ok = False
            parse_details.append(f"{csv_path.name}:ERROR:{exc}")

    validation_rows = [
        validation_row("VAL1202_0_sources_exist", "all cited local source paths exist", source_paths_ok, f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"),
        validation_row("VAL1202_1_needles_found", "all cited source needles found", source_needles_ok, f"{sum(bool(row['needle_found']) for row in source_rows)}/{len(source_rows)} needles found"),
        validation_row("VAL1202_2_scenario_values", "W_R10 scenario family is exactly 1,10,100", scenario_values_ok, f"W values={scenario_values}"),
        validation_row("VAL1202_3_envelope_numeric", "qDT allowed envelope has positive numeric lambda alpha and qDT values", envelope_numeric_positive, f"rows={len(envelope_rows)}"),
        validation_row("VAL1202_4_gate_bites", "at least one conservative envelope threshold is below toy qDT=1", gate_bites, f"min_qDT_allowed={fmt(min_row['qDT_allowed'])} at {min_row['row_id']}"),
        validation_row("VAL1202_5_nonclaim_flags", "all stress rows remain nonclaim", all_valid_flags_false, "scenario, assumption, and envelope valid_for_claim flags are false"),
        validation_row("VAL1202_6_claim_gates_blocked", "all claim gates remain blocked", claim_gates_blocked, f"blocked={sum(row['status']=='BLOCKED' for row in claim_gates)}/{len(claim_gates)}"),
        validation_row("VAL1202_7_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parse_details)),
        validation_row("VAL1202_8_formalization_untouched", "formalization-workbench untouched during run", formalization_untouched, f"formalization_recent_after_run_start_count={len(formalization_recent)}"),
    ]
    validation_pass = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1202_9_overall",
            "overall 1202 validation",
            validation_pass,
            "1202 conservative nonclaim envelope is reproducible" if validation_pass else "one or more validation checks failed",
        )
    )
    validation_fields = ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"]
    write_csv(VALIDATION_PATH, validation_rows, validation_fields)

    doc = f"""# 1202 Y5/R10 Conservative Geometry Kernel Or qDT Profile Family

**Current verdict:** 1202 replaces the single toy `W_R10=1` smoke row with a declared nonclaim scenario family `W_R10={{1,10,100}}` and computes the allowed `q_DT` envelope against four review-candidate R10 curve samples.

**Main progress:** the R10 gate is now numerically interpretable as a target amplitude problem: for each sampled `lambda`, `q_DT_allowed = alpha_bound/W_R10`. This still does **not** claim an R10/local-GR pass because neither the official R10 kernel nor parent-derived `q_DT` component amplitudes are available.

## Source Register

{markdown_table(source_rows, source_fields)}

## Conservative Kernel Assumptions

{markdown_table(assumptions, assumption_fields)}

## W_R10 Scenario Family

{markdown_table(scenarios, scenario_fields)}

## qDT Allowed Envelope

{markdown_table(envelope_rows, envelope_fields)}

## qDT Profile Family Requirements

{markdown_table(profile_requirements, profile_fields)}

## Runner Summary

{markdown_table(runner_summary, runner_fields)}

## Claim Gates

{markdown_table(claim_gates, gate_fields)}

## Decision Ledger

{markdown_table(decision_ledger, decision_fields)}

## Next Target

{markdown_table(next_target, next_fields)}

## Validation

{markdown_table(validation_rows, validation_fields)}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"validation_pass={bool_text(validation_pass)}")
    print(f"tightest_row={min_row['row_id']} qDT_allowed={fmt(min_row['qDT_allowed'])}")


if __name__ == "__main__":
    main()

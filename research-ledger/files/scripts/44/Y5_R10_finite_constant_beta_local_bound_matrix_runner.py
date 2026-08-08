from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MTS_DIR = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS_DIR = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "639-Y5-R10-finite-constant-beta-local-bound-matrix-runner.md"
SCRIPT = ROOT / "scripts" / "Y5_R10_finite_constant_beta_local_bound_matrix_runner.py"

STATUS = "Y5_R10_finite_constant_beta_local_bound_matrix_built_bounds_present_predictions_symbolic_nonclaim"
CLAIM_CEILING = "local_bound_matrix_assembly_only_no_numeric_MTS_score_no_cg_zero_R10_WEP_PPN_clock_or_local_GR_pass"
NEXT_TARGET = "640-Y5-R10-charge-topology-or-kappa-alpha-numeric-prior.md"

PRIOR_638_DOC = ROOT / "638-Y5-R10-constant-sector-zero-or-finite-beta-derivation.md"
PRIOR_638_VALIDATION = MTS_DIR / "P8_Y5_BRR545_638_VALIDATION.csv"
PRIOR_638_BETA_LAWS = MTS_DIR / "P8_Y5_R10_638_FINITE_BETA_LAWS.csv"
PRIOR_638_ARENA = MTS_DIR / "P8_Y5_R10_638_ARENA_PROJECTION_MATRIX.csv"
PRIOR_638_VERDICT = MTS_DIR / "P8_Y5_R10_638_CONSTANT_VERDICT.csv"
PRIOR_635_R10_PRESSURE = MTS_DIR / "P8_Y5_R10_635_TWO_LEG_NUMERIC_INPUT_RUNNER.csv"
LOCAL_BOUND_CLAIMS = LOCAL_BOUNDS_DIR / "local_bound_claims.csv"
LOCAL_BOUND_README = LOCAL_BOUNDS_DIR / "README.md"
R10_REVIEW_CANDIDATE = LOCAL_BOUNDS_DIR / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv"

SOURCE_REGISTER = MTS_DIR / "P8_Y5_R10_639_SOURCE_REGISTER.csv"
SYMBOL_TABLE = MTS_DIR / "P8_Y5_R10_639_CONSTANT_BETA_SYMBOL_TABLE.csv"
LOCAL_BOUND_MATRIX = MTS_DIR / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv"
R10_PRESSURE_IMPORT = MTS_DIR / "P8_Y5_R10_639_R10_PRESSURE_IMPORT.csv"
NUMERIC_SLOT_LEDGER = MTS_DIR / "P8_Y5_R10_639_NUMERIC_SLOT_LEDGER.csv"
SCOREABILITY_GATE = MTS_DIR / "P8_Y5_R10_639_SCOREABILITY_GATE.csv"
DECISION = MTS_DIR / "P8_Y5_BRR545_639_DECISION.csv"
NEXT_CONTRACT = MTS_DIR / "P8_Y5_R10_639_NEXT_CONTRACT.csv"
NONCLAIM_SUMMARY = MTS_DIR / "P8_Y5_R10_639_NONCLAIM_SUMMARY.csv"
VALIDATION = MTS_DIR / "P8_Y5_BRR545_639_VALIDATION.csv"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def parse_float(value: Any) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (PRIOR_638_DOC, "immediate 638 checkpoint"),
        (PRIOR_638_VALIDATION, "638 validation gate"),
        (PRIOR_638_BETA_LAWS, "638 symbolic finite beta laws"),
        (PRIOR_638_ARENA, "638 arena projection matrix"),
        (PRIOR_638_VERDICT, "638 constant verdict"),
        (PRIOR_635_R10_PRESSURE, "R10 pressure-only two-leg envelope summary"),
        (LOCAL_BOUND_CLAIMS, "verified local bound claims table"),
        (LOCAL_BOUND_README, "local bound source intake rule"),
        (R10_REVIEW_CANDIDATE, "R10 vector curve review candidate, nonclaim"),
        (SCRIPT, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": f"SRC639_{index}",
            "source_path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for index, (path, role) in enumerate(sources)
    ]


def symbol_table_rows() -> list[dict[str, Any]]:
    return [
        {
            "symbol_id": "SYM639_0_kappa_alpha",
            "symbol": "kappa_alpha",
            "meaning": "d ln alpha_EM / dXhat",
            "units": "per_Xhat_unit",
            "needed_for": "EM spectra;clock ratios;WEP composition",
            "current_value": "MISSING_PARENT_NUMERIC",
            "owner_needed": "charge topology/gauge kinetic parent derivation or numeric finite prior",
            "valid_for_claim": "false",
        },
        {
            "symbol_id": "SYM639_1_kappa_mass",
            "symbol": "kappa_mass_i",
            "meaning": "d ln dimensionless mass/binding ratio i / dXhat",
            "units": "per_Xhat_unit",
            "needed_for": "WEP;clock ratios;body beta_A",
            "current_value": "MISSING_PARENT_NUMERIC",
            "owner_needed": "mass-spectrum/representation parent derivation or numeric sensitivity prior",
            "valid_for_claim": "false",
        },
        {
            "symbol_id": "SYM639_2_beta_A",
            "symbol": "beta_A",
            "meaning": "sum_i S_Ai kappa_i plus any material marker derivative",
            "units": "dimensionless_per_Xhat_unit",
            "needed_for": "R10;WEP;orbital source/test coupling",
            "current_value": "MISSING_COMPOSITION_NUMERIC",
            "owner_needed": "composition sensitivity matrix S_Ai and marker theorem/coefficients",
            "valid_for_claim": "false",
        },
        {
            "symbol_id": "SYM639_3_Z_eff",
            "symbol": "Z_eff",
            "meaning": "quadratic normalization of exchanged local residual mode",
            "units": "action_normalization",
            "needed_for": "R10 finite-range alpha_X(lambda)",
            "current_value": "MISSING_PARENT_HESSIAN",
            "owner_needed": "second variation of parent local action",
            "valid_for_claim": "false",
        },
        {
            "symbol_id": "SYM639_4_lambda_X",
            "symbol": "lambda_X",
            "meaning": "range of exchanged mode sqrt(Z_eff/M_X^2)",
            "units": "m",
            "needed_for": "R10;orbital finite-range profile",
            "current_value": "MISSING_PARENT_HESSIAN",
            "owner_needed": "local mode mass/range from Hessian and boundary/domain spectrum",
            "valid_for_claim": "false",
        },
        {
            "symbol_id": "SYM639_5_tau_arena",
            "symbol": "tau_R10,tau_WEP,tau_clock,tau_PPN,tau_orbital",
            "meaning": "arena-specific projection/normalization from beta law to observable",
            "units": "dimensionless_or_arena_units",
            "needed_for": "all local bound rows",
            "current_value": "MISSING_ARENA_PROJECTION",
            "owner_needed": "apparatus/source geometry, clock sensitivities, PPN map, orbital source normalization",
            "valid_for_claim": "false",
        },
        {
            "symbol_id": "SYM639_6_delta_GM",
            "symbol": "delta_GM",
            "meaning": "source-normalization/operator residual in measured GM",
            "units": "dimensionless_or_per_time",
            "needed_for": "Gdot;orbital;PPN source normalization",
            "current_value": "MISSING_GR_OPERATOR_NUMERIC",
            "owner_needed": "EH/PPN/source-normalization derivation",
            "valid_for_claim": "false",
        },
    ]


def expression_for_row(row_id: str, observable: str) -> tuple[str, str, str]:
    if row_id in {"R0_identity_coframe_direct", "R1_WEP_source_charge"}:
        return (
            "eta_AB ~ tau_WEP beta_source sum_i(S_Ai-S_Bi) kappa_i",
            "kappa_i;S_Ai;S_Bi;beta_source;tau_WEP",
            "WEP/composition beta vector",
        )
    if row_id == "R2_clock_redshift":
        return (
            "alpha_clock ~ tau_clock sum_i(K_ai-K_bi) kappa_i",
            "kappa_i;K_ai;K_bi;tau_clock",
            "clock sensitivity vector",
        )
    if row_id in {"R3_gamma", "R4_beta", "R5_alpha1", "R6_alpha2", "R7_alpha3", "R8_xi"}:
        return (
            f"{observable}_pred = PPN_operator_projection(delta_GM,disformal_residual,non_EH_vector)",
            "delta_GM;disformal_residual;non_EH_operator_vector;tau_PPN",
            "PPN/operator residual vector",
        )
    if row_id == "R9_Gdot":
        return (
            "Gdot/G = d(delta_GM)/dt + source_normalization_drift",
            "delta_GM;source_normalization_residual;time_map",
            "source-normalization/orbital drift",
        )
    if row_id == "R10_fifth_force":
        return (
            "alpha_X(lambda)=tau_R10(lambda) beta_source beta_test / Z_eff",
            "beta_source;beta_test;Z_eff;lambda_X;tau_R10;alpha_bound(lambda)",
            "R10 two-leg finite range",
        )
    if row_id == "R11_EH_operator_ledger":
        return (
            "non_EH_operator_coefficients -> PPN/source-normalization residual rows",
            "EH_operator_coefficients;boundary_terms;source_normalization",
            "EH/operator closure",
        )
    return (
        "MISSING_PROJECTION_LAW",
        "MISSING_INPUTS",
        "unmapped",
    )


def local_bound_matrix_rows() -> list[dict[str, Any]]:
    rows = []
    bound_rows = read_csv(LOCAL_BOUND_CLAIMS)
    for index, bound in enumerate(bound_rows):
        row_id = bound.get("row_id", "")
        observable = bound.get("observable", "")
        expression, inputs, route = expression_for_row(row_id, observable)
        upper_bound = bound.get("upper_bound", "")
        bound_numeric = parse_float(upper_bound) is not None
        bound_kind = "numeric_bound" if bound_numeric else upper_bound or "symbolic_bound"
        prediction_ready = "false"
        rows.append(
            {
                "matrix_id": f"LBM639_{index}",
                "row_id": row_id,
                "arena": bound.get("test_arena", ""),
                "observable": observable,
                "bound_value": upper_bound,
                "bound_units": bound.get("units", ""),
                "bound_kind": bound_kind,
                "reference_path_or_url": bound.get("reference_path_or_url", ""),
                "prediction_law": expression,
                "required_mts_inputs": inputs,
                "projection_route": route,
                "bound_present": bool_text(bool(upper_bound) or row_id == "R10_fifth_force"),
                "prediction_numeric_ready": prediction_ready,
                "runner_status": "bound_present_prediction_symbolic_nonclaim",
                "valid_for_claim": "false",
            }
        )
    return rows


def r10_pressure_import_rows() -> list[dict[str, Any]]:
    out = []
    for row in read_csv(PRIOR_635_R10_PRESSURE):
        out.append(
            {
                "pressure_id": f"R10P639_{len(out)}",
                "profile_factor": row.get("profile_factor", ""),
                "law": row.get("law", ""),
                "tightest_lambda_m": row.get("tightest_lambda_m", ""),
                "tightest_abs_c_eff_pressure_bound": row.get("tightest_abs_c_eff_pressure_bound", ""),
                "physical_inputs_ready": row.get("physical_inputs_ready", "false"),
                "missing_inputs": row.get("missing_inputs", ""),
                "import_status": "pressure_only_nonclaim",
                "source": rel(PRIOR_635_R10_PRESSURE),
                "valid_for_claim": "false",
            }
        )
    return out


def numeric_slot_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "slot_id": "NSL639_0_kappa_vector",
            "slot": "kappa_alpha,kappa_mass_i,kappa_binding_i,kappa_clock_i",
            "needed_by_rows": "R0;R1;R2;EM_spectra",
            "current_status": "MISSING_PARENT_NUMERIC",
            "minimum_to_score": "numeric values or theorem-zero for each dimensionless constant derivative",
            "valid_for_claim": "false",
        },
        {
            "slot_id": "NSL639_1_composition_sensitivities",
            "slot": "S_Ai,S_Bi,source/test material composition",
            "needed_by_rows": "R0;R1;R10",
            "current_status": "MISSING_COMPOSITION_NUMERIC",
            "minimum_to_score": "test/source body sensitivity vectors and material labels",
            "valid_for_claim": "false",
        },
        {
            "slot_id": "NSL639_2_mode_normalization",
            "slot": "Z_eff,M_X^2,lambda_X",
            "needed_by_rows": "R10;orbital finite-range",
            "current_status": "MISSING_PARENT_HESSIAN",
            "minimum_to_score": "local quadratic action/Hessian with units",
            "valid_for_claim": "false",
        },
        {
            "slot_id": "NSL639_3_arena_tau",
            "slot": "tau_R10,tau_WEP,tau_clock,tau_PPN,tau_orbital",
            "needed_by_rows": "all local matrix rows",
            "current_status": "MISSING_ARENA_PROJECTION",
            "minimum_to_score": "projection from MTS residual variables to each experimental observable",
            "valid_for_claim": "false",
        },
        {
            "slot_id": "NSL639_4_operator_vector",
            "slot": "delta_GM,disformal_residual,non_EH_operator_coefficients,boundary terms",
            "needed_by_rows": "R3;R4;R5;R6;R7;R8;R9;R11",
            "current_status": "MISSING_GR_OPERATOR_NUMERIC",
            "minimum_to_score": "local EH/PPN/source-normalization derivation or explicit coefficient bounds",
            "valid_for_claim": "false",
        },
        {
            "slot_id": "NSL639_5_bound_curve_promotion",
            "slot": "alpha_bound(lambda) claim-grade curve",
            "needed_by_rows": "R10",
            "current_status": "REVIEW_CANDIDATE_ONLY_FOR_R10_CURVE",
            "minimum_to_score": "verified table or human-QA promoted digitization; current pressure import remains nonclaim",
            "valid_for_claim": "false",
        },
    ]


def scoreability_gate_rows(
    matrix_rows: list[dict[str, Any]],
    pressure_rows: list[dict[str, Any]],
    slot_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    prediction_ready = [row for row in matrix_rows if row.get("prediction_numeric_ready") == "true"]
    claim_rows = [row for row in matrix_rows + pressure_rows + slot_rows if row.get("valid_for_claim") == "true"]
    numeric_bounds = [row for row in matrix_rows if row.get("bound_kind") == "numeric_bound"]
    return [
        {
            "gate_id": "SG639_0_bounds_loaded",
            "requirement": "local bound claims loaded into matrix",
            "result": "pass" if len(matrix_rows) >= 10 else "fail",
            "detail": f"matrix_rows={len(matrix_rows)};numeric_bounds={len(numeric_bounds)}",
            "score_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "SG639_1_predictions_numeric",
            "requirement": "MTS prediction side numeric for every score row",
            "result": "blocked",
            "detail": f"prediction_numeric_ready_rows={len(prediction_ready)}",
            "score_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "SG639_2_missing_slots",
            "requirement": "all kappa/beta/Z/lambda/tau/operator slots filled",
            "result": "blocked",
            "detail": f"missing_slot_rows={len(slot_rows)}",
            "score_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "SG639_3_r10_pressure_import",
            "requirement": "R10 pressure import allowed only as nonclaim diagnostic",
            "result": "pass" if len(pressure_rows) == 4 else "fail",
            "detail": f"pressure_rows={len(pressure_rows)}",
            "score_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "SG639_4_claim_leak",
            "requirement": "no matrix row or pressure row valid for claim",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
            "score_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D639_0_main_verdict",
            "decision": STATUS,
            "meaning": "local experimental bounds are assembled, but MTS prediction coefficients are still symbolic",
            "status": "matrix_ready_not_scoreable",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D639_1_r10",
            "decision": "R10_pressure_imported_nonclaim",
            "meaning": "unit-profile pressure bound remains |c_eff|~0.048 at lambda 0.000608 m, but beta/Z/lambda/profile inputs are missing",
            "status": "pressure_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D639_2_cross_arena",
            "decision": "same_constant_failure_vector_maps_to_WEP_clock_R10_PPN_orbital",
            "meaning": "the matrix now prevents testing one arena while ignoring the same coupling in the others",
            "status": "discipline_improvement",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D639_3_claim_ceiling",
            "decision": CLAIM_CEILING,
            "meaning": "no local score or pass until missing numeric slots are parent-owned or source-backed",
            "status": "hard_guardrail",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def next_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "NC639_0_kappa_alpha_route",
            "required_output": "derive charge/gauge coupling topologically or assign a sourced kappa_alpha prior for private pressure",
            "success_condition": "alpha_EM row is either theorem-zero or numeric finite input",
            "if_success": "EM/clock/WEP rows can be partially scored",
            "if_fail": "constant branch remains unscoreable",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NC639_1_mass_clock_sensitivities",
            "required_output": "fill mass/composition/clock sensitivity vectors or prove representation/topological silence",
            "success_condition": "beta_A and clock projection rows have numeric coefficients",
            "if_success": "WEP and clock pressure can run",
            "if_fail": "zero branch still blocked by constants",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "NC639_2_R10_numeric_side",
            "required_output": "fill beta_source,beta_test,Z_eff,lambda_X,tau_R10 and promote/QA alpha(lambda) curve before scoring R10",
            "success_condition": "R10 row has both numeric prediction and claim-grade bound curve",
            "if_success": "R10 local pressure can be evaluated",
            "if_fail": "R10 remains pressure-only",
            "valid_for_claim": "false",
        },
    ]


def nonclaim_summary_rows(
    matrix_rows: list[dict[str, Any]],
    pressure_rows: list[dict[str, Any]],
    slot_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    numeric_bounds = [row for row in matrix_rows if row.get("bound_kind") == "numeric_bound"]
    prediction_ready = [row for row in matrix_rows if row.get("prediction_numeric_ready") == "true"]
    unit_pressure = next((row for row in pressure_rows if row.get("profile_factor") == "1"), {})
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "matrix_rows": len(matrix_rows),
            "numeric_bound_rows": len(numeric_bounds),
            "prediction_numeric_ready_rows": len(prediction_ready),
            "missing_slot_rows": len(slot_rows),
            "r10_pressure_rows": len(pressure_rows),
            "unit_profile_tightest_abs_c_eff_pressure_bound": unit_pressure.get("tightest_abs_c_eff_pressure_bound", ""),
            "unit_profile_tightest_lambda_m": unit_pressure.get("tightest_lambda_m", ""),
            "finite_branch_scoreable": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        }
    ]


def validation_rows(
    source_rows: list[dict[str, Any]],
    symbol_rows: list[dict[str, Any]],
    matrix_rows: list[dict[str, Any]],
    pressure_rows: list[dict[str, Any]],
    slot_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row for row in source_rows if row.get("exists") != "true"]
    prior_rows = read_csv(PRIOR_638_VALIDATION)
    prior_fails = [row for row in prior_rows if row.get("result") != "pass"]
    bound_claim_rows = read_csv(LOCAL_BOUND_CLAIMS)
    prediction_ready = [row for row in matrix_rows if row.get("prediction_numeric_ready") == "true"]
    numeric_bounds = [row for row in matrix_rows if row.get("bound_kind") == "numeric_bound"]
    claim_rows = [
        row
        for group in (symbol_rows, matrix_rows, pressure_rows, slot_rows, gate_rows)
        for row in group
        if row.get("valid_for_claim") == "true"
    ]
    unit_pressure = next((row for row in pressure_rows if row.get("profile_factor") == "1"), {})
    unit_bound = parse_float(unit_pressure.get("tightest_abs_c_eff_pressure_bound"))
    return [
        {
            "check_id": "V639_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V639_1_prior_638_clean",
            "result": "pass" if prior_rows and not prior_fails else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V639_2_local_bounds_loaded",
            "result": "pass" if len(matrix_rows) == len(bound_claim_rows) and len(matrix_rows) >= 10 else "fail",
            "detail": f"matrix_rows={len(matrix_rows)};bound_claim_rows={len(bound_claim_rows)}",
        },
        {
            "check_id": "V639_3_numeric_bounds_present_predictions_blocked",
            "result": "pass" if len(numeric_bounds) >= 8 and not prediction_ready else "fail",
            "detail": f"numeric_bounds={len(numeric_bounds)};prediction_ready={len(prediction_ready)}",
        },
        {
            "check_id": "V639_4_symbol_table_complete",
            "result": "pass" if len(symbol_rows) == 7 else "fail",
            "detail": f"symbol_rows={len(symbol_rows)}",
        },
        {
            "check_id": "V639_5_r10_pressure_import_nonclaim",
            "result": "pass" if len(pressure_rows) == 4 and unit_bound is not None and unit_bound < 0.05 else "fail",
            "detail": f"pressure_rows={len(pressure_rows)};unit_bound={unit_bound}",
        },
        {
            "check_id": "V639_6_missing_slots_complete",
            "result": "pass" if len(slot_rows) == 6 else "fail",
            "detail": f"slot_rows={len(slot_rows)}",
        },
        {
            "check_id": "V639_7_scoreability_blocked",
            "result": "pass" if len(gate_rows) == 5 and all(row.get("score_allowed") == "false" for row in gate_rows) else "fail",
            "detail": f"gate_rows={len(gate_rows)}",
        },
        {
            "check_id": "V639_8_next_contract_written",
            "result": "pass" if len(contract_rows) == 3 else "fail",
            "detail": f"contract_rows={len(contract_rows)}",
        },
        {
            "check_id": "V639_9_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V639_10_no_local_claim",
            "result": "pass",
            "detail": "matrix_score=false;c_g_zero_claimed=false;finite_branch_scoreable=false;R10=false;WEP=false;PPN=false;clock=false;orbital=false;local_GR=false",
        },
    ]


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines) + "\n"


def write_doc(
    source_rows: list[dict[str, Any]],
    symbol_rows: list[dict[str, Any]],
    matrix_rows: list[dict[str, Any]],
    pressure_rows: list[dict[str, Any]],
    slot_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = "\n".join(
        [
            "# 639 Y5 R10 finite constant beta local bound matrix runner",
            "",
            f"Status: `{STATUS}`  ",
            f"Claim ceiling: `{CLAIM_CEILING}`  ",
            f"Next target: `{NEXT_TARGET}`",
            "",
            "## Verdict",
            "- The local bound matrix now exists: WEP, clocks, PPN, Gdot, R10, and EH-operator rows are mapped to the constant-beta prediction side.",
            "- Bounds are present, but MTS predictions are not numeric yet: `kappa_i`, `beta_A`, `Z_eff`, `lambda_X`, `tau_arena`, and the operator vector remain missing.",
            "- The R10 pressure import is retained as a private nonclaim diagnostic only.",
            "- No local test score or pass is allowed from this checkpoint.",
            "",
            "## Bound Matrix Logic",
            "Each row has the same structure:",
            "",
            "`observable_bound` from `local_bound_claims.csv`,",
            "",
            "`prediction_law` from the 638 constant-beta laws,",
            "",
            "`required_mts_inputs` naming the exact coefficients still missing.",
            "",
            "This prevents the old failure mode where R10 is tested in isolation while WEP, clocks, PPN, or source-normalization couplings are left in the fog.",
            "",
            "## Source Register",
            markdown_table(source_rows),
            "## Constant Beta Symbol Table",
            markdown_table(symbol_rows),
            "## Local Bound Matrix",
            markdown_table(matrix_rows),
            "## R10 Pressure Import",
            markdown_table(pressure_rows),
            "## Numeric Slot Ledger",
            markdown_table(slot_rows),
            "## Scoreability Gate",
            markdown_table(gate_rows),
            "## Decision",
            markdown_table(decision),
            "## Next Contract",
            markdown_table(contract_rows),
            "## Nonclaim Summary",
            markdown_table(summary),
            "## Validation",
            markdown_table(validation),
            "## Interpretation",
            "This is the boring-but-essential testing scaffold. The theory is not being scored yet; the matrix simply says what a score would require. The next useful move is to try the charge/topology route first because `kappa_alpha` feeds EM, clock, and WEP rows. If that fails, assign a private numeric prior/envelope for `kappa_alpha` and see how violently the matrix reacts.",
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    symbol_rows = symbol_table_rows()
    matrix_rows = local_bound_matrix_rows()
    pressure_rows = r10_pressure_import_rows()
    slot_rows = numeric_slot_ledger_rows()
    gate_rows = scoreability_gate_rows(matrix_rows, pressure_rows, slot_rows)
    decision = decision_rows()
    contract_rows = next_contract_rows()
    summary = nonclaim_summary_rows(matrix_rows, pressure_rows, slot_rows)
    validation = validation_rows(
        source_rows,
        symbol_rows,
        matrix_rows,
        pressure_rows,
        slot_rows,
        gate_rows,
        contract_rows,
    )

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(SYMBOL_TABLE, symbol_rows)
    write_csv(LOCAL_BOUND_MATRIX, matrix_rows)
    write_csv(R10_PRESSURE_IMPORT, pressure_rows)
    write_csv(NUMERIC_SLOT_LEDGER, slot_rows)
    write_csv(SCOREABILITY_GATE, gate_rows)
    write_csv(DECISION, decision)
    write_csv(NEXT_CONTRACT, contract_rows)
    write_csv(NONCLAIM_SUMMARY, summary)
    write_csv(VALIDATION, validation)
    write_doc(
        source_rows,
        symbol_rows,
        matrix_rows,
        pressure_rows,
        slot_rows,
        gate_rows,
        decision,
        contract_rows,
        summary,
        validation,
    )

    failed = [row for row in validation if row["result"] != "pass"]
    print(
        json.dumps(
            {
                "status": STATUS,
                "doc": str(DOC),
                "failed_checks": failed,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

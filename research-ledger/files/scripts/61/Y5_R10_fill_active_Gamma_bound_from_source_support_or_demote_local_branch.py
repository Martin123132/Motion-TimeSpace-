from __future__ import annotations

import csv
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "836-Y5-R10-fill-active-Gamma-bound-from-source-support-or-demote-local-branch.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_836_SOURCE_REGISTER.csv"
SOURCE_EXTRACTION_PATH = RESIDUALS / "P8_Y5_R10_836_SOURCE_SUPPORT_EXTRACTION.csv"
FILL_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_836_ACTIVE_GAMMA_FILL_ATTEMPT.csv"
SMOKE_INPUT_PATH = RESIDUALS / "P8_Y5_R10_836_SMOKE_RUNNER_INPUT.csv"
SMOKE_OUTPUT_PATH = RESIDUALS / "P8_Y5_R10_836_SMOKE_RUNNER_OUTPUT.csv"
DEMOTION_GATE_PATH = RESIDUALS / "P8_Y5_R10_836_DEMOTION_GATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_836_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_836_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_836_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_836_VALIDATION.csv"

STATUS = "Y5_R10_836_active_Gamma_source_support_fill_attempt_coefficients_response_missing_demoted_nonclaim"
CLAIM_CEILING = "source_support_fill_attempt_and_demotion_gate_only_no_sourced_local_response_pass"
NEXT_TARGET = "837-Y5-R10-source-active-Gamma-coefficients-or-local-branch-closure-label.md"

SOURCE_SPECS = [
    {
        "source_id": "835_doc",
        "path": POST_CHECKPOINT / "835-Y5-R10-Gamma-active-mode-bound-and-local-response-runner.md",
        "needles": [
            "active-Gamma local-test runner now exists",
            "CAG835_0_D_L2_symbolic",
            "836-Y5-R10-fill-active-Gamma-bound-from-source-support-or-demote-local-branch.md",
        ],
        "role": "immediate active-Gamma runner handoff",
    },
    {
        "source_id": "835_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_835_VALIDATION.csv",
        "needles": [
            "V835_2_input_schema_complete,pass",
            "V835_5_runner_blocks_missing_inputs,pass",
            "V835_10_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "800_support_powers",
        "path": POST_CHECKPOINT / "800-Y5-R10-universal-XB-PiB-support-powers-or-Kperp-boundary-zero-lemma.md",
        "needles": [
            "pS=1 is conditionally available",
            "pT=2 is not derived by Pi_B",
            "not_derived_as_parent_theorem",
        ],
        "role": "support-power derivation status",
    },
    {
        "source_id": "829_residual_budget",
        "path": POST_CHECKPOINT / "829-Y5-R10-baseline-lock-source-support-residual-budget.md",
        "needles": [
            "q_baseline = 0 after parent-derived baseline lock Gamma_L=Lambda_loc",
            "a_F, R_mm, C_X, A_B",
            "missing_parent_values",
        ],
        "role": "coefficient and response gaps",
    },
    {
        "source_id": "equation_register_support_values",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": [
            "window43_U_B = 3.7965595357794454e-7",
            "L_cg^-2 F_L - Lambda_loc = O(U_B^2)",
            "local point mass U_B^2 = 9.458639468826237e-27",
        ],
        "role": "formalization source-support values and warning rows",
    },
    {
        "source_id": "equation_register_D_L",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": [
            "D_L = U_B H_L",
            "D_L derivation overclaim",
            "Parent v0 does not derive `D_L` or the even/quadratic dependence.",
        ],
        "role": "D_L architecture and overclaim warning",
    },
]

REQUIRED_NUMERIC_FIELDS = [
    "dimension_n",
    "active_gamma_coeff",
    "small_parameter",
    "support_power",
    "K00_projection_fraction",
    "matter_curvature_norm",
    "metric_response_coeff",
    "observable_limit",
]
REQUIRED_SOURCE_FIELDS = [
    "gamma_formula_source_path",
    "small_parameter_source_path",
    "response_source_path",
    "bound_source_path",
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def check_needles(path: Path, needles: list[str]) -> str:
    text = read_text(path)
    if not text:
        return "missing_path"
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
    return "pass"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": str(path.exists()).lower(),
                "needle_check": check_needles(path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def source_extraction_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "extract_id": "SE836_0_U_B_window43",
            "quantity": "window43_U_B",
            "value": "3.7965595357794454e-7",
            "units": "dimensionless",
            "source_path": str(FORMALIZATION / "05-equation-register.md"),
            "status": "source_value_found_nonclaim",
            "usable_for_claim": "false",
            "reason": "proxy value exists but not tied to C_gamma, matter curvature, or arena response",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "extract_id": "SE836_1_point_mass_U_B2",
            "quantity": "local point mass U_B^2",
            "value": "9.458639468826237e-27",
            "units": "dimensionless",
            "source_path": str(FORMALIZATION / "05-equation-register.md"),
            "status": "source_value_found_nonclaim",
            "usable_for_claim": "false",
            "reason": "tiny suppression factor is promising but coefficient/response normalization are missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "extract_id": "SE836_2_D_L_architecture",
            "quantity": "D_L = U_B H_L",
            "value": "symbolic",
            "units": "dimensionless",
            "source_path": str(FORMALIZATION / "05-equation-register.md"),
            "status": "architecture_found_closure_only",
            "usable_for_claim": "false",
            "reason": "equation register says D_L derivation is an overclaim / parent v0 does not derive D_L",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "extract_id": "SE836_3_support_power_pT",
            "quantity": "pT=2 trace-baseline support",
            "value": "symbolic",
            "units": "dimensionless",
            "source_path": str(POST_CHECKPOINT / "800-Y5-R10-universal-XB-PiB-support-powers-or-Kperp-boundary-zero-lemma.md"),
            "status": "required_but_not_parent_derived",
            "usable_for_claim": "false",
            "reason": "800 says pT=2 needs a double-zero/fixed-point mechanism and does not follow from Pi_B alone",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "extract_id": "SE836_4_response_matrix",
            "quantity": "local response matrix",
            "value": "missing",
            "units": "arena_dependent",
            "source_path": str(POST_CHECKPOINT / "830-Y5-R10-Khat-boundary-owner-or-residual-vector-runner.md"),
            "status": "missing_response_matrix",
            "usable_for_claim": "false",
            "reason": "PPN/R10/clock/orbital/WEP response rows remain missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def fill_attempt_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "attempt_id": "FA836_0_D_L2_parent",
            "candidate": "Gamma_eff-Lambda_loc=C_D D_L^2",
            "filled_fields": "formula_family=sourced_from_equation_register",
            "missing_fields": "C_D;D_L;K00_projection_fraction;matter_curvature_norm;metric_response_coeff;observable_limit;source_paths",
            "result": "cannot_score",
            "demotion": "closure_only_until_parent_D_L_and_response_are_sourced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "FA836_1_U_B2_window43",
            "candidate": "Gamma_eff-Lambda_loc=C_U U_B^2 using window43_U_B",
            "filled_fields": "small_parameter=3.7965595357794454e-7;support_power=2",
            "missing_fields": "C_U;K00_projection_fraction;matter_curvature_norm;metric_response_coeff;observable_limit;response_source_path",
            "result": "smoke_only_not_claim",
            "demotion": "numeric_suppression_factor_available_but_not_evidence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "FA836_2_U_B2_point_mass",
            "candidate": "Gamma_eff-Lambda_loc=C_U U_B^2 using local point-mass U_B^2",
            "filled_fields": "small_parameter_squared=9.458639468826237e-27;support_power=2",
            "missing_fields": "C_U;K00_projection_fraction;matter_curvature_norm;metric_response_coeff;observable_limit;response_source_path",
            "result": "smoke_only_not_claim",
            "demotion": "promising_small_number_but_unscored",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "attempt_id": "FA836_3_metric_null",
            "candidate": "metric-null Khat carrier",
            "filled_fields": "none",
            "missing_fields": "delta_S_Khat_delta_g_obs_zero_theorem;boundary_improvement_theorem;matter_frame_readout",
            "result": "cannot_adopt",
            "demotion": "metric_null_route_candidate_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def smoke_input_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "smoke_U_B2_point_mass_missing_coeff_response",
            "arena": "PPN",
            "dimension_n": "4",
            "active_gamma_coeff": "MISSING_C_U",
            "small_parameter": str(math.sqrt(9.458639468826237e-27)),
            "support_power": "2",
            "K00_projection_fraction": "MISSING_K00_PROJECTION",
            "matter_curvature_norm": "MISSING_MATTER_CURVATURE",
            "metric_response_coeff": "MISSING_RESPONSE_MATRIX",
            "observable_limit": "MISSING_PPN_BOUND",
            "gamma_formula_source_path": str(FORMALIZATION / "05-equation-register.md"),
            "small_parameter_source_path": str(FORMALIZATION / "05-equation-register.md"),
            "response_source_path": "MISSING_SOURCE_PATH",
            "bound_source_path": "MISSING_SOURCE_PATH",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "notes": "uses sourced U_B^2 proxy only as a nonclaim smoke row",
            "generated_utc": generated_utc,
        },
        {
            "row_id": "smoke_window43_missing_coeff_response",
            "arena": "PPN",
            "dimension_n": "4",
            "active_gamma_coeff": "MISSING_C_U",
            "small_parameter": "3.7965595357794454e-7",
            "support_power": "2",
            "K00_projection_fraction": "MISSING_K00_PROJECTION",
            "matter_curvature_norm": "MISSING_MATTER_CURVATURE",
            "metric_response_coeff": "MISSING_RESPONSE_MATRIX",
            "observable_limit": "MISSING_PPN_BOUND",
            "gamma_formula_source_path": str(FORMALIZATION / "05-equation-register.md"),
            "small_parameter_source_path": str(FORMALIZATION / "05-equation-register.md"),
            "response_source_path": "MISSING_SOURCE_PATH",
            "bound_source_path": "MISSING_SOURCE_PATH",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "notes": "uses sourced window43 U_B only as a nonclaim smoke row",
            "generated_utc": generated_utc,
        },
    ]


def is_missing(value: object) -> bool:
    text = str(value).strip()
    if text == "":
        return True
    upper = text.upper()
    return "MISSING" in upper or upper in {"UNSOURCED", "NONE", "N/A"}


def as_float(value: object) -> float | None:
    if is_missing(value):
        return None
    try:
        parsed = float(str(value))
    except ValueError:
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def run_smoke_row(row: dict[str, object], generated_utc: str) -> dict[str, object]:
    missing_numeric = [field for field in REQUIRED_NUMERIC_FIELDS if as_float(row.get(field)) is None]
    missing_sources = [field for field in REQUIRED_SOURCE_FIELDS if is_missing(row.get(field))]
    missing = missing_numeric + missing_sources
    valid_for_claim = str(row.get("valid_for_claim")).lower() == "true"

    if missing:
        small_parameter = as_float(row.get("small_parameter"))
        support_power = as_float(row.get("support_power"))
        visible_suppression = "MISSING_INPUT"
        if small_parameter is not None and support_power is not None:
            visible_suppression = f"{small_parameter ** support_power:.16e}"
        return {
            "row_id": row["row_id"],
            "arena": row["arena"],
            "runner_status": "blocked_missing_inputs",
            "visible_suppression_factor": visible_suppression,
            "active_gamma_bound": "MISSING_INPUT",
            "observable_residual_bound": "MISSING_INPUT",
            "observable_pass": "false",
            "block_reason": "missing_fields:" + ";".join(missing),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }

    values = {field: as_float(row[field]) for field in REQUIRED_NUMERIC_FIELDS}
    assert all(value is not None for value in values.values())
    carrier_factor = math.sqrt(values["dimension_n"] / (values["dimension_n"] - 1.0)) if values["dimension_n"] > 1 else math.inf
    suppression = values["small_parameter"] ** values["support_power"]
    active_gamma = values["active_gamma_coeff"] * suppression
    observable = (
        abs(values["metric_response_coeff"])
        * abs(values["K00_projection_fraction"])
        * carrier_factor
        * active_gamma
        / abs(values["matter_curvature_norm"])
    )
    passes = valid_for_claim and observable <= values["observable_limit"]
    return {
        "row_id": row["row_id"],
        "arena": row["arena"],
        "runner_status": "computed_nonclaim" if not valid_for_claim else "computed",
        "visible_suppression_factor": f"{suppression:.16e}",
        "active_gamma_bound": f"{active_gamma:.16e}",
        "observable_residual_bound": f"{observable:.16e}",
        "observable_pass": str(passes).lower(),
        "block_reason": "row_valid_for_claim_false" if not valid_for_claim else "none",
        "valid_for_claim": "false",
        "generated_utc": generated_utc,
    }


def demotion_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "DG836_0_formula_form",
            "question": "Is an active-Gamma suppression formula available?",
            "answer": "yes_symbolic",
            "evidence": "O(D_L^2)/O(U_B^2) rows exist",
            "claim_effect": "formula form only, not a local pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "DG836_1_coefficients",
            "question": "Are C_D/C_U sourced?",
            "answer": "no",
            "evidence": "source-support rows give powers and proxy small parameters, not active-Gamma coefficients",
            "claim_effect": "runner remains unscored",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "DG836_2_response",
            "question": "Are local response matrices sourced?",
            "answer": "no",
            "evidence": "PPN/R10/clock/orbital/WEP response coefficients remain missing",
            "claim_effect": "no local-GR or local-test claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "DG836_3_demote_or_continue",
            "question": "Should the local branch be demoted now?",
            "answer": "demote_claim_not_route",
            "evidence": "mathematical route remains viable but current corpus cannot score it",
            "claim_effect": "local branch stays closure/input-acquisition until C_gamma and response rows are real",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D836_0",
            "finding": "source-support fills powers/proxies but not coefficients or response",
            "reason": "O(D_L^2)/O(U_B^2) and small U_B proxy values exist; C_D/C_U and local response matrices do not",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D836_1",
            "finding": "local branch claim is demoted, route remains live",
            "reason": "the theory has a concrete acquisition target rather than a proof: source C_gamma and response coefficients or label closure explicitly",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "source or derive C_D/C_U and local response coefficients, otherwise lock the local branch as closure-only",
            "include": "active-Gamma coefficient derivation, D_L/U_B source path, PPN/R10 response rows, matter descent, explicit closure label if missing",
            "exclude": "placeholder pass, local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "performed the active-Gamma source-support fill attempt and installed a demotion gate",
            "what_is_not_claimed": "C_D/C_U sourced, response matrices sourced, local-GR pass, PPN/R10/clock/orbital/WEP pass",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_valid_for_claim_false(row_groups: list[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if row.get("valid_for_claim") != "false":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, object]],
    extraction_rows: list[dict[str, object]],
    fill_rows: list[dict[str, object]],
    smoke_inputs: list[dict[str, object]],
    smoke_outputs: list[dict[str, object]],
    demotion_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_835_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    values_found = {"SE836_0_U_B_window43", "SE836_1_point_mass_U_B2"}.issubset({row["extract_id"] for row in extraction_rows})
    no_claim_values = all(row["usable_for_claim"] == "false" for row in extraction_rows)
    cannot_score = all(row["result"] in {"cannot_score", "smoke_only_not_claim", "cannot_adopt"} for row in fill_rows)
    smoke_blocks = bool(smoke_outputs) and all(row["observable_pass"] == "false" and row["runner_status"] == "blocked_missing_inputs" for row in smoke_outputs)
    no_missing_passes = not any(row["observable_pass"] == "true" and "missing_fields" in row["block_reason"] for row in smoke_outputs)
    demotion_ok = any(row["gate_id"] == "DG836_3_demote_or_continue" and row["answer"] == "demote_claim_not_route" for row in demotion_rows)
    no_claim = (
        not any(row["observable_pass"] == "true" for row in smoke_outputs)
        and not any(row["claim_allowed"] == "true" for row in decisions)
    )
    nonclaim_ok = all_valid_for_claim_false(
        [source_rows, extraction_rows, fill_rows, smoke_inputs, smoke_outputs, demotion_rows, decisions, next_targets, nonclaim]
    )
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {
            "check_id": "V836_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V836_1_prior_835_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V836_2_proxy_values_extracted",
            "result": "pass" if values_found else "fail",
            "detail": "window43_U_B and local point-mass U_B^2 extracted as nonclaim proxies",
        },
        {
            "check_id": "V836_3_proxy_values_not_claimed",
            "result": "pass" if no_claim_values else "fail",
            "detail": "all extracted source values remain unusable for claim without coefficients/response",
        },
        {
            "check_id": "V836_4_fill_attempt_cannot_score",
            "result": "pass" if cannot_score else "fail",
            "detail": "fill attempts remain blocked or smoke-only",
        },
        {
            "check_id": "V836_5_smoke_runner_blocks_missing",
            "result": "pass" if smoke_blocks else "fail",
            "detail": "smoke rows block before local-test comparison",
        },
        {
            "check_id": "V836_6_no_missing_input_passes",
            "result": "pass" if no_missing_passes else "fail",
            "detail": "no row with missing fields passes",
        },
        {
            "check_id": "V836_7_demote_claim_not_route",
            "result": "pass" if demotion_ok else "fail",
            "detail": "local claim demoted while derivation route remains live",
        },
        {
            "check_id": "V836_8_no_data_or_local_GR_claim",
            "result": "pass" if no_claim else "fail",
            "detail": "no local-GR or arena pass selected",
        },
        {
            "check_id": "V836_9_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V836_10_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V836_11_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V836_12_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]


def csv_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(text)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_document(
    source_rows: list[dict[str, object]],
    extraction_rows: list[dict[str, object]],
    fill_rows: list[dict[str, object]],
    smoke_inputs: list[dict[str, object]],
    smoke_outputs: list[dict[str, object]],
    demotion_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 836 - Y5 R10 Fill Active-Gamma Bound From Source-Support Or Demote Local Branch",
        "",
        "Current result: **source-support fills useful form and proxy small-parameter values, but not the active-Gamma coefficient or local response matrices**. `U_B^2` can be extremely small in a point-mass proxy, yet that is not evidence until `C_D/C_U`, `K00` projection, matter curvature, and PPN/R10/clock/orbital/WEP response coefficients are sourced. Therefore the local claim is demoted while the derivation route remains live.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Source-Support Extraction",
        "",
        csv_table(extraction_rows, ["extract_id", "quantity", "value", "status", "usable_for_claim", "reason", "valid_for_claim"]),
        "",
        "## Active-Gamma Fill Attempt",
        "",
        csv_table(fill_rows, ["attempt_id", "candidate", "filled_fields", "missing_fields", "result", "demotion", "valid_for_claim"]),
        "",
        "## Smoke Runner Input",
        "",
        csv_table(smoke_inputs, ["row_id", "arena", "dimension_n", "active_gamma_coeff", "small_parameter", "support_power", "metric_response_coeff", "observable_limit", "valid_for_claim"]),
        "",
        "## Smoke Runner Output",
        "",
        csv_table(smoke_outputs, ["row_id", "arena", "runner_status", "visible_suppression_factor", "active_gamma_bound", "observable_pass", "block_reason", "valid_for_claim"]),
        "",
        "## Demotion Gate",
        "",
        csv_table(demotion_rows, ["gate_id", "question", "answer", "evidence", "claim_effect", "valid_for_claim"]),
        "",
        "## Decision",
        "",
        csv_table(decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        csv_table(next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        csv_table(validation, ["check_id", "result", "detail"]),
        "",
    ]
    OUTPUT_DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    source_rows = source_register_rows(generated_utc)
    extraction_rows = source_extraction_rows(generated_utc)
    fill_rows = fill_attempt_rows(generated_utc)
    smoke_inputs = smoke_input_rows(generated_utc)
    smoke_outputs = [run_smoke_row(row, generated_utc) for row in smoke_inputs]
    demotion_rows = demotion_gate_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, extraction_rows, fill_rows, smoke_inputs, smoke_outputs, demotion_rows, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(SOURCE_EXTRACTION_PATH, extraction_rows, ["extract_id", "quantity", "value", "units", "source_path", "status", "usable_for_claim", "reason", "valid_for_claim", "generated_utc"])
    write_csv(FILL_ATTEMPT_PATH, fill_rows, ["attempt_id", "candidate", "filled_fields", "missing_fields", "result", "demotion", "valid_for_claim", "generated_utc"])
    write_csv(
        SMOKE_INPUT_PATH,
        smoke_inputs,
        [
            "row_id",
            "arena",
            "dimension_n",
            "active_gamma_coeff",
            "small_parameter",
            "support_power",
            "K00_projection_fraction",
            "matter_curvature_norm",
            "metric_response_coeff",
            "observable_limit",
            "gamma_formula_source_path",
            "small_parameter_source_path",
            "response_source_path",
            "bound_source_path",
            "numeric_ready",
            "valid_for_claim",
            "notes",
            "generated_utc",
        ],
    )
    write_csv(
        SMOKE_OUTPUT_PATH,
        smoke_outputs,
        ["row_id", "arena", "runner_status", "visible_suppression_factor", "active_gamma_bound", "observable_residual_bound", "observable_pass", "block_reason", "valid_for_claim", "generated_utc"],
    )
    write_csv(DEMOTION_GATE_PATH, demotion_rows, ["gate_id", "question", "answer", "evidence", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, extraction_rows, fill_rows, smoke_inputs, smoke_outputs, demotion_rows, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()

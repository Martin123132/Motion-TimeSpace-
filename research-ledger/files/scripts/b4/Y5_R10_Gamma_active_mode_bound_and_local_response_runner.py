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

OUTPUT_DOC = POST_CHECKPOINT / "835-Y5-R10-Gamma-active-mode-bound-and-local-response-runner.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_835_SOURCE_REGISTER.csv"
INPUT_SCHEMA_PATH = RESIDUALS / "P8_Y5_R10_835_ACTIVE_GAMMA_INPUT_SCHEMA.csv"
CANDIDATE_ROWS_PATH = RESIDUALS / "P8_Y5_R10_835_CANDIDATE_ACTIVE_GAMMA_ROWS.csv"
RESPONSE_REQUIREMENTS_PATH = RESIDUALS / "P8_Y5_R10_835_LOCAL_RESPONSE_REQUIREMENTS.csv"
RUNNER_INPUT_PATH = RESIDUALS / "P8_Y5_R10_835_ACTIVE_GAMMA_RUNNER_INPUT.csv"
RUNNER_OUTPUT_PATH = RESIDUALS / "P8_Y5_R10_835_ACTIVE_GAMMA_RUNNER_OUTPUT.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_835_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_835_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_835_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_835_VALIDATION.csv"

STATUS = "Y5_R10_835_active_Gamma_bound_runner_schema_ready_inputs_unsourced_nonclaim"
CLAIM_CEILING = "active_Gamma_response_runner_schema_only_no_sourced_local_test_pass"
NEXT_TARGET = "836-Y5-R10-fill-active-Gamma-bound-from-source-support-or-demote-local-branch.md"

SOURCE_SPECS = [
    {
        "source_id": "834_doc",
        "path": POST_CHECKPOINT / "834-Y5-R10-metric-null-Khat-carrier-or-Gamma-local-suppression-law.md",
        "needles": [
            "the dangerous Hessian `K_hat` carrier is sourced by the active nonconstant mode",
            "SL834_2_local_metric_fraction",
            "835-Y5-R10-Gamma-active-mode-bound-and-local-response-runner.md",
        ],
        "role": "immediate active-Gamma suppression-law handoff",
    },
    {
        "source_id": "834_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_834_VALIDATION.csv",
        "needles": [
            "V834_2_constant_mode_split_recorded,pass",
            "V834_4_suppression_law_calculator_ready,pass",
            "V834_10_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "830_response_gates",
        "path": POST_CHECKPOINT / "830-Y5-R10-Khat-boundary-owner-or-residual-vector-runner.md",
        "needles": [
            "OG830_1_PPN",
            "OG830_2_R10",
            "OG830_5_WEP",
        ],
        "role": "local arena response requirements",
    },
    {
        "source_id": "800_support_powers",
        "path": POST_CHECKPOINT / "800-Y5-R10-universal-XB-PiB-support-powers-or-Kperp-boundary-zero-lemma.md",
        "needles": [
            "SPD800_5_verdict",
            "pS=1,pL=2,pT=2,pB>=2,pK>=2",
            "not_derived_as_parent_theorem",
        ],
        "role": "support-power status and nonclaim warning",
    },
    {
        "source_id": "equation_register_active_gamma",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": [
            "L_cg^-2 F_L - Lambda_loc = O(D_L^2)",
            "L_cg^-2 F_L - Lambda_loc = O(U_B^2)",
            "Gamma_eff = L_cg^-2 [F_L + a_F(R(m)-R(m_L))]",
        ],
        "role": "equation-register active-Gamma formulas",
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
ARENAS = ["PPN", "R10", "clocks", "orbital", "WEP"]


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


def input_schema_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "field": "dimension_n",
            "meaning": "dimension used in the trace-free carrier factor sqrt(n/(n-1))",
            "units": "dimensionless",
            "required_source": "local branch geometry convention",
            "status": "missing_numeric_choice",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field": "active_gamma_coeff",
            "meaning": "C_gamma in ||Gamma_eff-Lambda_loc|| <= C_gamma s^p",
            "units": "L^-2",
            "required_source": "parent source-support or local expansion theorem",
            "status": "missing_parent_coefficient",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field": "small_parameter",
            "meaning": "D_L or U_B value in the local arena",
            "units": "dimensionless",
            "required_source": "source-support / boundary-amplitude law",
            "status": "missing_local_input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field": "support_power",
            "meaning": "p in C_gamma s^p",
            "units": "dimensionless",
            "required_source": "derived support-power theorem",
            "status": "missing_or_closure_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field": "K00_projection_fraction",
            "meaning": "fraction mapping carrier norm to local 00 source component",
            "units": "dimensionless",
            "required_source": "Khat component/readout theorem",
            "status": "missing_projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field": "matter_curvature_norm",
            "meaning": "normalizing local matter curvature, e.g. |4 pi G rho/c^2|",
            "units": "L^-2",
            "required_source": "arena matter model or bound convention",
            "status": "missing_local_matter_scale",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field": "metric_response_coeff",
            "meaning": "arena response coefficient from Khat carrier to observable residual",
            "units": "arena_dependent",
            "required_source": "PPN/R10/clock/orbital/WEP response matrix",
            "status": "missing_response_matrix",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field": "observable_limit",
            "meaning": "upper bound for the arena residual",
            "units": "arena_dependent",
            "required_source": "local test bound source",
            "status": "missing_bound_row",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def candidate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "candidate_id": "CAG835_0_D_L2_symbolic",
            "active_gamma_formula": "Gamma_eff-Lambda_loc = C_D D_L^2 + O(D_L^3)",
            "source_evidence": "equation register records L_cg^-2 F_L - Lambda_loc = O(D_L^2)",
            "numeric_status": "symbolic_only",
            "missing_for_claim": "C_D;D_L;K00_projection_fraction;metric_response_coeff;observable_limit",
            "runner_row_status": "blocked_missing_numeric_inputs",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "CAG835_1_U_B2_symbolic",
            "active_gamma_formula": "Gamma_eff-Lambda_loc = C_U U_B^2 + O(U_B^3)",
            "source_evidence": "equation register records L_cg^-2 F_L - Lambda_loc = O(U_B^2)",
            "numeric_status": "symbolic_only",
            "missing_for_claim": "C_U;U_B;K00_projection_fraction;metric_response_coeff;observable_limit",
            "runner_row_status": "blocked_missing_numeric_inputs",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def response_requirement_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "arena": "PPN",
            "observable": "delta_gamma, delta_beta, alpha1, alpha2, xi",
            "needed_response": "matrix from Khat_H, gamma_act, and q_residual to PPN coefficients",
            "current_status": "missing_response_matrix",
            "claim_gate": "all PPN residuals below sourced limits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arena": "R10",
            "observable": "alpha(lambda)",
            "needed_response": "map active carrier to Yukawa/fifth-force alpha(lambda)",
            "current_status": "missing_response_matrix",
            "claim_gate": "abs(alpha_predicted)<=alpha_bound(lambda)",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arena": "clocks",
            "observable": "clock_delta_z",
            "needed_response": "metric/coframe response to carrier and active Gamma",
            "current_status": "missing_response_matrix",
            "claim_gate": "clock/redshift residual below sourced bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arena": "orbital",
            "observable": "perihelion/range/ephemeris residual vector",
            "needed_response": "local metric solution and orbital response kernel",
            "current_status": "missing_response_matrix",
            "claim_gate": "orbital residual below sourced bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "arena": "WEP",
            "observable": "eta_AB/species coupling",
            "needed_response": "matter descent or species-coupling readout",
            "current_status": "missing_matter_descent",
            "claim_gate": "species-independent descent or eta_AB below sourced bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def runner_input_rows(generated_utc: str) -> list[dict[str, object]]:
    base = {
        "dimension_n": "MISSING_DIMENSION_CHOICE",
        "active_gamma_coeff": "MISSING_GAMMA_COEFFICIENT",
        "small_parameter": "MISSING_D_L_OR_U_B",
        "support_power": "MISSING_SUPPORT_POWER",
        "K00_projection_fraction": "MISSING_KHAT_COMPONENT_MAP",
        "matter_curvature_norm": "MISSING_LOCAL_MATTER_CURVATURE",
        "metric_response_coeff": "MISSING_ARENA_PROJECTION",
        "observable_limit": "MISSING_ARENA_BOUND",
        "gamma_formula_source_path": "MISSING_SOURCE_PATH",
        "small_parameter_source_path": "MISSING_SOURCE_PATH",
        "response_source_path": "MISSING_SOURCE_PATH",
        "bound_source_path": "MISSING_SOURCE_PATH",
        "valid_for_claim": "false",
        "generated_utc": generated_utc,
    }
    rows: list[dict[str, object]] = []
    for row_id, arena, formula_family in [
        ("template_D_L2_PPN", "PPN", "D_L2"),
        ("template_U_B2_PPN", "PPN", "U_B2"),
        ("template_D_L2_R10", "R10", "D_L2"),
        ("template_U_B2_clock_orbital_WEP", "multi_local", "U_B2"),
    ]:
        row = dict(base)
        row.update(
            {
                "row_id": row_id,
                "arena": arena,
                "formula_family": formula_family,
                "row_status": "blocked_missing_parent_and_response_inputs",
                "numeric_ready": "false",
                "notes": "nonclaim template; fill all numeric fields and source paths before any local-test comparison",
            }
        )
        rows.append(row)
    return rows


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


def run_active_gamma_row(row: dict[str, object], generated_utc: str) -> dict[str, object]:
    missing_numeric = [field for field in REQUIRED_NUMERIC_FIELDS if as_float(row.get(field)) is None]
    missing_sources = [field for field in REQUIRED_SOURCE_FIELDS if is_missing(row.get(field))]
    missing = missing_numeric + missing_sources
    valid_for_claim = str(row.get("valid_for_claim")).lower() == "true"

    if missing:
        return {
            "row_id": row["row_id"],
            "arena": row["arena"],
            "formula_family": row["formula_family"],
            "runner_status": "blocked_missing_inputs",
            "active_gamma_bound": "MISSING_INPUT",
            "Khat_norm_bound": "MISSING_INPUT",
            "observable_residual_bound": "MISSING_INPUT",
            "margin_to_limit": "MISSING_INPUT",
            "observable_pass": "false",
            "block_reason": "missing_fields:" + ";".join(missing),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }

    values = {field: as_float(row[field]) for field in REQUIRED_NUMERIC_FIELDS}
    assert all(value is not None for value in values.values())
    carrier_factor = math.sqrt(values["dimension_n"] / (values["dimension_n"] - 1.0)) if values["dimension_n"] > 1 else math.inf
    active_gamma = values["active_gamma_coeff"] * values["small_parameter"] ** values["support_power"]
    khat_norm = carrier_factor * active_gamma
    observable_residual = (
        abs(values["metric_response_coeff"])
        * abs(values["K00_projection_fraction"])
        * khat_norm
        / abs(values["matter_curvature_norm"])
    )
    margin = values["observable_limit"] - observable_residual
    passes = valid_for_claim and margin >= 0.0
    block_reason = "none" if passes else ("row_valid_for_claim_false" if not valid_for_claim else "observable_bound_exceeds_or_unvalidated")
    return {
        "row_id": row["row_id"],
        "arena": row["arena"],
        "formula_family": row["formula_family"],
        "runner_status": "computed_nonclaim" if not valid_for_claim else "computed",
        "active_gamma_bound": f"{active_gamma:.16e}",
        "Khat_norm_bound": f"{khat_norm:.16e}",
        "observable_residual_bound": f"{observable_residual:.16e}",
        "margin_to_limit": f"{margin:.16e}",
        "observable_pass": str(passes).lower(),
        "block_reason": block_reason,
        "valid_for_claim": "false",
        "generated_utc": generated_utc,
    }


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D835_0",
            "finding": "active-Gamma local test runner is schema-ready",
            "reason": "the runner has explicit fields for C_gamma, D_L/U_B, support power, Khat projection, matter curvature, response coefficient, and bound",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D835_1",
            "finding": "all current candidate rows remain symbolic/nonclaim",
            "reason": "equation-register O(D_L^2)/O(U_B^2) statements give form, not sourced coefficients or response matrices",
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
            "objective": "fill the active-Gamma runner with sourced source-support coefficients or explicitly demote the local branch to closure-only",
            "include": "C_D/C_U extraction, D_L/U_B source, support-power derivation, response coefficient sources, arena bounds",
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
            "what_changed": "created the active-Gamma local-response runner schema and symbolic candidate rows",
            "what_is_not_claimed": "sourced C_gamma, D_L/U_B, response matrices, local-GR pass, or any arena pass",
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
    schema_rows: list[dict[str, object]],
    candidates: list[dict[str, object]],
    response_rows: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    runner_outputs: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_834_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    schema_fields = {row["field"] for row in schema_rows}
    schema_ok = set(REQUIRED_NUMERIC_FIELDS).issubset(schema_fields)
    candidates_symbolic = bool(candidates) and all(row["numeric_status"] == "symbolic_only" for row in candidates)
    response_ok = set(ARENAS).issubset({row["arena"] for row in response_rows})
    runner_blocks = bool(runner_outputs) and all(row["observable_pass"] == "false" and row["runner_status"] == "blocked_missing_inputs" for row in runner_outputs)
    no_missing_passes = not any(row["observable_pass"] == "true" and "missing_fields" in row["block_reason"] for row in runner_outputs)
    no_claim = (
        not any(row["observable_pass"] == "true" for row in runner_outputs)
        and not any(row["claim_allowed"] == "true" for row in decisions)
    )
    nonclaim_ok = all_valid_for_claim_false(
        [source_rows, schema_rows, candidates, response_rows, runner_inputs, runner_outputs, decisions, next_targets, nonclaim]
    )
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {
            "check_id": "V835_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V835_1_prior_834_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V835_2_input_schema_complete",
            "result": "pass" if schema_ok else "fail",
            "detail": "all required numeric runner fields are described",
        },
        {
            "check_id": "V835_3_candidate_rows_symbolic_only",
            "result": "pass" if candidates_symbolic else "fail",
            "detail": "D_L2 and U_B2 candidates are symbolic/nonclaim",
        },
        {
            "check_id": "V835_4_response_requirements_complete",
            "result": "pass" if response_ok else "fail",
            "detail": "PPN, R10, clocks, orbital, and WEP requirements listed",
        },
        {
            "check_id": "V835_5_runner_blocks_missing_inputs",
            "result": "pass" if runner_blocks else "fail",
            "detail": "all runner rows block until numeric/source inputs exist",
        },
        {
            "check_id": "V835_6_no_missing_input_passes",
            "result": "pass" if no_missing_passes else "fail",
            "detail": "no row with missing fields passes",
        },
        {
            "check_id": "V835_7_no_data_or_local_GR_claim",
            "result": "pass" if no_claim else "fail",
            "detail": "no local-GR or arena pass selected",
        },
        {
            "check_id": "V835_8_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V835_9_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V835_10_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V835_11_validation_rows_ready",
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
    schema_rows: list[dict[str, object]],
    candidates: list[dict[str, object]],
    response_rows: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    runner_outputs: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 835 - Y5 R10 Gamma Active-Mode Bound And Local Response Runner",
        "",
        "Current result: **the active-Gamma local-test runner now exists, but every row is still blocked because the source-support coefficients and response matrices are not filled**. The useful advance is that the local-GR question is no longer foggy: a pass needs `C_gamma`, `D_L/U_B`, support power, `K00` projection, matter-curvature normalization, response coefficient, and arena bound for each tested local arena.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Active-Gamma Input Schema",
        "",
        csv_table(schema_rows, ["field", "meaning", "units", "required_source", "status", "valid_for_claim"]),
        "",
        "## Candidate Active-Gamma Rows",
        "",
        csv_table(candidates, ["candidate_id", "active_gamma_formula", "source_evidence", "numeric_status", "missing_for_claim", "runner_row_status", "valid_for_claim"]),
        "",
        "## Local Response Requirements",
        "",
        csv_table(response_rows, ["arena", "observable", "needed_response", "current_status", "claim_gate", "valid_for_claim"]),
        "",
        "## Runner Input",
        "",
        csv_table(runner_inputs, ["row_id", "arena", "formula_family", "row_status", "active_gamma_coeff", "small_parameter", "support_power", "metric_response_coeff", "observable_limit", "valid_for_claim"]),
        "",
        "## Runner Output",
        "",
        csv_table(runner_outputs, ["row_id", "arena", "formula_family", "runner_status", "observable_residual_bound", "margin_to_limit", "observable_pass", "block_reason", "valid_for_claim"]),
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
    schema_rows = input_schema_rows(generated_utc)
    candidates = candidate_rows(generated_utc)
    response_rows = response_requirement_rows(generated_utc)
    runner_inputs = runner_input_rows(generated_utc)
    runner_outputs = [run_active_gamma_row(row, generated_utc) for row in runner_inputs]
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, schema_rows, candidates, response_rows, runner_inputs, runner_outputs, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(INPUT_SCHEMA_PATH, schema_rows, ["field", "meaning", "units", "required_source", "status", "valid_for_claim", "generated_utc"])
    write_csv(CANDIDATE_ROWS_PATH, candidates, ["candidate_id", "active_gamma_formula", "source_evidence", "numeric_status", "missing_for_claim", "runner_row_status", "valid_for_claim", "generated_utc"])
    write_csv(RESPONSE_REQUIREMENTS_PATH, response_rows, ["arena", "observable", "needed_response", "current_status", "claim_gate", "valid_for_claim", "generated_utc"])
    write_csv(
        RUNNER_INPUT_PATH,
        runner_inputs,
        [
            "row_id",
            "arena",
            "formula_family",
            "row_status",
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
        RUNNER_OUTPUT_PATH,
        runner_outputs,
        [
            "row_id",
            "arena",
            "formula_family",
            "runner_status",
            "active_gamma_bound",
            "Khat_norm_bound",
            "observable_residual_bound",
            "margin_to_limit",
            "observable_pass",
            "block_reason",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, schema_rows, candidates, response_rows, runner_inputs, runner_outputs, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()

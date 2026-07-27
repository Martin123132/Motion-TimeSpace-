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

OUTPUT_DOC = POST_CHECKPOINT / "834-Y5-R10-metric-null-Khat-carrier-or-Gamma-local-suppression-law.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_834_SOURCE_REGISTER.csv"
MODE_SPLIT_PATH = RESIDUALS / "P8_Y5_R10_834_GAMMA_MODE_SPLIT_THEOREM.csv"
METRIC_NULL_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_834_METRIC_NULL_AUDIT.csv"
SUPPRESSION_LAW_PATH = RESIDUALS / "P8_Y5_R10_834_LOCAL_SUPPRESSION_LAW.csv"
RUNNER_INPUT_PATH = RESIDUALS / "P8_Y5_R10_834_SUPPRESSION_RUNNER_INPUT_TEMPLATE.csv"
RUNNER_OUTPUT_PATH = RESIDUALS / "P8_Y5_R10_834_SUPPRESSION_RUNNER_OUTPUT.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_834_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_834_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_834_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_834_VALIDATION.csv"

STATUS = "Y5_R10_834_Gamma_active_mode_suppression_law_derived_metric_null_not_signed_nonclaim"
CLAIM_CEILING = "active_Gamma_mode_bound_contract_only_no_metric_null_or_local_GR_pass"
NEXT_TARGET = "835-Y5-R10-Gamma-active-mode-bound-and-local-response-runner.md"

SOURCE_SPECS = [
    {
        "source_id": "833_doc",
        "path": POST_CHECKPOINT / "833-Y5-R10-Hessian-Khat-carrier-amplitude-and-metric-response-bound.md",
        "needles": [
            "the explicit Hessian `K_hat` carrier",
            "AL833_1_exact_L2_norm",
            "834-Y5-R10-metric-null-Khat-carrier-or-Gamma-local-suppression-law.md",
        ],
        "role": "immediate carrier-amplitude handoff",
    },
    {
        "source_id": "833_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_833_VALIDATION.csv",
        "needles": [
            "V833_2_amplitude_law_derived,pass",
            "V833_3_metric_safety_gates_complete,pass",
            "V833_9_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "828_baseline_lock",
        "path": POST_CHECKPOINT / "828-Y5-R10-XB-Lcg-local-constancy-or-Khat-owner-theorem.md",
        "needles": [
            "Gamma_L(X)=Lambda_loc=constant",
            "linear_trace_terms_removed_conditionally",
            "baseline lock is not the same as assuming X_B is constant",
        ],
        "role": "constant baseline/plateau split source",
    },
    {
        "source_id": "829_residual_budget",
        "path": POST_CHECKPOINT / "829-Y5-R10-baseline-lock-source-support-residual-budget.md",
        "needles": [
            "q_baseline = 0 after parent-derived baseline lock Gamma_L=Lambda_loc",
            "q_total <= q_quad + q_X2 + q_boundary + q_K",
            "source-backed numeric inputs and observable response matrices are still missing",
        ],
        "role": "post-lock residual budget",
    },
    {
        "source_id": "832_right_inverse",
        "path": POST_CHECKPOINT / "832-Y5-R10-tracefree-divergence-range-theorem-or-cokernel-bound.md",
        "needles": [
            "flat bulk trace-free `K_hat` carrier exists explicitly",
            "Delta inverse requires boundary/zero-mode choice",
            "Khat carrier can gravitate even when div Khat cancels grad Gamma",
        ],
        "role": "right-inverse and zero-mode warning",
    },
    {
        "source_id": "516_gamma_owner_candidate",
        "path": POST_CHECKPOINT / "516-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner.md",
        "needles": [
            "GO516_A_response_doublet_quadratic_density",
            "RD516_2_metric_response",
            "Gamma_eff_owner_derived_for_MTS=false",
        ],
        "role": "metric-null/scalar-density owner candidate but not proof",
    },
    {
        "source_id": "equation_register_support",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": [
            "L_cg^-2 F_L - Lambda_loc = O(D_L^2)",
            "L_cg^-2 F_L - Lambda_loc = O(U_B^2)",
            "The real Solar branch remains open until `q_loc(x)`, boundary data, and amplitude bounds are supplied.",
        ],
        "role": "existing local suppression law targets",
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
    "gamma_suppression_source_path",
    "small_parameter_source_path",
    "metric_response_source_path",
    "local_bound_source_path",
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


def mode_split_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "split_id": "GS834_0_decompose",
            "statement": "Split Gamma_eff into a local constant baseline plus an active nonconstant part: Gamma_eff=Lambda_loc+gamma_act.",
            "derivation": "The local q channel depends on nabla Gamma_eff, so nabla Lambda_loc=0 and only gamma_act sources the Hessian carrier.",
            "result": "constant_mode_excluded_from_Khat_carrier",
            "open_condition": "Lambda_loc/baseline lock must be parent-derived, not chosen after the fact",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "split_id": "GS834_1_refined_amplitude",
            "statement": "The 833 carrier amplitude law applies to gamma_act, not to the constant local baseline.",
            "derivation": "For nonzero/compatible modes, ||K||=sqrt(n/(n-1))||gamma_act||; the zero/constant mode does not enter D_T K=grad Gamma.",
            "result": "||K||_active=sqrt(n/(n-1))*||gamma_act||",
            "open_condition": "boundary and zero-mode convention must be fixed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "split_id": "GS834_2_source_support",
            "statement": "If the local branch derives gamma_act=O(D_L^2) or O(U_B^2), then the dangerous Khat carrier is also second-order supported.",
            "derivation": "Insert ||gamma_act||<=C_gamma s^p into GS834_1: ||K||<=sqrt(n/(n-1)) C_gamma s^p.",
            "result": "active_carrier_source_supported_if_Gamma_deviation_is_source_supported",
            "open_condition": "C_gamma, s, p, and source paths must be real before claims",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "split_id": "GS834_3_physical_warning",
            "statement": "The split helps only if the observed metric reads gamma_act, not Lambda_loc, as the local carrier source.",
            "derivation": "A cosmological-constant-like constant trace may be harmless locally, but a nonconstant trace-free carrier still needs a matter-frame response bound.",
            "result": "metric_response_gate_still_required",
            "open_condition": "matter-frame response matrix and WEP descent remain missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def metric_null_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "MN834_0_topological_or_improvement",
            "route": "metric-null Khat carrier",
            "required_identity": "delta S_Khat/delta g_obs=0 or exact boundary/improvement stress in the local matter frame",
            "current_status": "not_derived",
            "reason": "516/833 keep metric response and boundary flux open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "MN834_1_response_doublet",
            "route": "quadratic response-doublet scalar density",
            "required_identity": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B and Khat equals its full metric response, with physical Z-lock",
            "current_status": "candidate_not_current_MTS_derived",
            "reason": "GO516_A is coherent but RD516_2/RD516_5 remain unsigned",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "MN834_2_suppression_route_selected",
            "route": "active Gamma local suppression",
            "required_identity": "gamma_act=Gamma_eff-Lambda_loc is source-supported and below local metric-response limits",
            "current_status": "best_next_route",
            "reason": "equation register already records O(D_L^2)/O(U_B^2) targets; this route needs inputs rather than a new miracle tensor",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def suppression_law_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "law_id": "SL834_0_active_gamma_bound",
            "quantity": "active local Gamma deviation",
            "formula": "||gamma_act|| <= C_gamma s^p, where gamma_act:=Gamma_eff-Lambda_loc and s in {D_L,U_B}",
            "pass_condition": "C_gamma, s, p are parent-derived/source-backed",
            "status": "contract_derived_inputs_missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "law_id": "SL834_1_Khat_active_bound",
            "quantity": "Hessian Khat carrier",
            "formula": "||Khat_H|| <= sqrt(n/(n-1)) C_gamma s^p",
            "pass_condition": "boundary/zero mode fixed and 832 curved obstruction bounded",
            "status": "contract_derived_inputs_missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "law_id": "SL834_2_local_metric_fraction",
            "quantity": "Newton/PPN carrier fraction",
            "formula": "epsilon_K <= R_metric f_00 sqrt(n/(n-1)) C_gamma s^p / K_matter",
            "pass_condition": "epsilon_K <= epsilon_limit with sourced response coefficient and matter curvature",
            "status": "calculator_ready_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "law_id": "SL834_3_required_suppression",
            "quantity": "required active Gamma smallness",
            "formula": "C_gamma s^p <= epsilon_limit K_matter / (R_metric f_00 sqrt(n/(n-1)))",
            "pass_condition": "inequality holds for every local arena: PPN, R10, clocks, orbital, WEP",
            "status": "calculator_ready_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def runner_input_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "template_missing_active_gamma_inputs",
            "row_status": "blocked_missing_parent_and_response_inputs",
            "dimension_n": "MISSING_DIMENSION_CHOICE",
            "active_gamma_coeff": "MISSING_GAMMA_COEFFICIENT",
            "small_parameter": "MISSING_D_L_OR_U_B",
            "support_power": "MISSING_SUPPORT_POWER",
            "K00_projection_fraction": "MISSING_KHAT_COMPONENT_MAP",
            "matter_curvature_norm": "MISSING_LOCAL_MATTER_CURVATURE",
            "metric_response_coeff": "MISSING_ARENA_PROJECTION",
            "observable_limit": "MISSING_ARENA_BOUND",
            "gamma_suppression_source_path": "MISSING_SOURCE_PATH",
            "small_parameter_source_path": "MISSING_SOURCE_PATH",
            "metric_response_source_path": "MISSING_SOURCE_PATH",
            "local_bound_source_path": "MISSING_SOURCE_PATH",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "notes": "claim rows require sourced gamma_act bound, D_L/U_B, support power, Khat projection, metric response, and local bound",
            "generated_utc": generated_utc,
        }
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


def run_suppression_row(row: dict[str, object], generated_utc: str) -> dict[str, object]:
    missing_numeric = [field for field in REQUIRED_NUMERIC_FIELDS if as_float(row.get(field)) is None]
    missing_sources = [field for field in REQUIRED_SOURCE_FIELDS if is_missing(row.get(field))]
    missing = missing_numeric + missing_sources
    valid_for_claim = str(row.get("valid_for_claim")).lower() == "true"

    if missing:
        return {
            "row_id": row["row_id"],
            "runner_status": "blocked_missing_inputs",
            "active_gamma_bound": "MISSING_INPUT",
            "carrier_factor": "MISSING_INPUT",
            "Khat_norm_bound": "MISSING_INPUT",
            "newton_ppn_fraction_bound": "MISSING_INPUT",
            "required_gamma_bound": "MISSING_INPUT",
            "observable_pass": "false",
            "block_reason": "missing_fields:" + ";".join(missing),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }

    values = {field: as_float(row[field]) for field in REQUIRED_NUMERIC_FIELDS}
    assert all(value is not None for value in values.values())
    n = values["dimension_n"]
    carrier_factor = math.sqrt(n / (n - 1.0)) if n > 1 else math.inf
    active_gamma = values["active_gamma_coeff"] * values["small_parameter"] ** values["support_power"]
    khat_bound = carrier_factor * active_gamma
    newton_ppn_fraction = abs(values["metric_response_coeff"]) * abs(values["K00_projection_fraction"]) * khat_bound / abs(values["matter_curvature_norm"])
    required_gamma = values["observable_limit"] * abs(values["matter_curvature_norm"]) / (
        abs(values["metric_response_coeff"]) * max(abs(values["K00_projection_fraction"]), 1.0e-300) * carrier_factor
    )
    passes = valid_for_claim and newton_ppn_fraction <= values["observable_limit"]
    block_reason = "none" if passes else ("row_valid_for_claim_false" if not valid_for_claim else "observable_bound_exceeds_or_unvalidated")
    return {
        "row_id": row["row_id"],
        "runner_status": "computed_nonclaim" if not valid_for_claim else "computed",
        "active_gamma_bound": f"{active_gamma:.16e}",
        "carrier_factor": f"{carrier_factor:.16e}",
        "Khat_norm_bound": f"{khat_bound:.16e}",
        "newton_ppn_fraction_bound": f"{newton_ppn_fraction:.16e}",
        "required_gamma_bound": f"{required_gamma:.16e}",
        "observable_pass": str(passes).lower(),
        "block_reason": block_reason,
        "valid_for_claim": "false",
        "generated_utc": generated_utc,
    }


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D834_0",
            "finding": "constant local baseline is not the dangerous Hessian-carrier source",
            "reason": "q depends on gradients, so the carrier amplitude law applies to gamma_act=Gamma_eff-Lambda_loc rather than Lambda_loc itself",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D834_1",
            "finding": "metric-null route is not signed, active-Gamma suppression is the best next route",
            "reason": "response-doublet/metric-null ownership remains candidate-only, while O(D_L^2)/O(U_B^2) suppression targets already exist",
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
            "objective": "fill or bound the active Gamma mode inputs and local response coefficients needed to score epsilon_K",
            "include": "C_gamma, D_L/U_B, support power, K00 projection, matter curvature, PPN/R10/clock/orbital/WEP response rows",
            "exclude": "claiming baseline lock as derived, metric-null claim without variation proof, placeholder pass rows, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "separated constant Lambda_loc from active gamma_act and derived the active-mode Khat suppression law",
            "what_is_not_claimed": "parent-derived baseline lock, metric-null Khat, local-GR pass, PPN/R10/clocks/orbital/WEP pass, or sourced epsilon_K",
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
    mode_rows: list[dict[str, object]],
    metric_rows: list[dict[str, object]],
    law_rows: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    runner_outputs: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_833_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    split_ok = any(row["result"] == "constant_mode_excluded_from_Khat_carrier" for row in mode_rows) and any(
        row["result"] == "||K||_active=sqrt(n/(n-1))*||gamma_act||" for row in mode_rows
    )
    metric_null_not_claimed = any(row["audit_id"] == "MN834_0_topological_or_improvement" and row["current_status"] == "not_derived" for row in metric_rows)
    suppression_ok = any(row["law_id"] == "SL834_2_local_metric_fraction" for row in law_rows) and any(
        row["law_id"] == "SL834_3_required_suppression" for row in law_rows
    )
    runner_blocks = any(row["row_id"] == "template_missing_active_gamma_inputs" and row["observable_pass"] == "false" for row in runner_outputs)
    no_missing_passes = not any(row["observable_pass"] == "true" and "missing_fields" in row["block_reason"] for row in runner_outputs)
    no_claim = (
        not any(row["observable_pass"] == "true" for row in runner_outputs)
        and not any(row["claim_allowed"] == "true" for row in decisions)
    )
    nonclaim_ok = all_valid_for_claim_false(
        [source_rows, mode_rows, metric_rows, law_rows, runner_inputs, runner_outputs, decisions, next_targets, nonclaim]
    )
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {
            "check_id": "V834_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V834_1_prior_833_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V834_2_constant_mode_split_recorded",
            "result": "pass" if split_ok else "fail",
            "detail": "constant Lambda_loc excluded; active gamma carrier law recorded",
        },
        {
            "check_id": "V834_3_metric_null_not_claimed",
            "result": "pass" if metric_null_not_claimed else "fail",
            "detail": "metric-null Khat remains not derived",
        },
        {
            "check_id": "V834_4_suppression_law_calculator_ready",
            "result": "pass" if suppression_ok else "fail",
            "detail": "epsilon_K and required active-gamma bound formulas present",
        },
        {
            "check_id": "V834_5_runner_template_blocks_missing",
            "result": "pass" if runner_blocks else "fail",
            "detail": "template_missing_active_gamma_inputs is blocked before numeric use",
        },
        {
            "check_id": "V834_6_no_missing_input_passes",
            "result": "pass" if no_missing_passes else "fail",
            "detail": "no row with missing fields passes",
        },
        {
            "check_id": "V834_7_no_data_or_local_GR_claim",
            "result": "pass" if no_claim else "fail",
            "detail": "no data, local-GR, PPN, R10, clock, orbital, or WEP pass selected",
        },
        {
            "check_id": "V834_8_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V834_9_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V834_10_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V834_11_validation_rows_ready",
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
    mode_rows: list[dict[str, object]],
    metric_rows: list[dict[str, object]],
    law_rows: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    runner_outputs: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 834 - Y5 R10 Metric-Null Khat Carrier Or Gamma Local Suppression Law",
        "",
        "Current result: **the 833 amplitude problem is refined: the dangerous Hessian `K_hat` carrier is sourced by the active nonconstant mode `gamma_act = Gamma_eff - Lambda_loc`, not by the local constant baseline itself**. Since `q` depends on gradients, `nabla Lambda_loc=0`; the carrier law becomes `||Khat_H|| <= sqrt(n/(n-1)) ||gamma_act||`. This keeps the local route alive if `gamma_act` is genuinely source-supported, e.g. `O(D_L^2)` or `O(U_B^2)`, but no local-GR claim is allowed until the bound and metric response are sourced.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Gamma Mode Split",
        "",
        csv_table(mode_rows, ["split_id", "statement", "derivation", "result", "open_condition", "valid_for_claim"]),
        "",
        "## Metric-Null Audit",
        "",
        csv_table(metric_rows, ["audit_id", "route", "required_identity", "current_status", "reason", "valid_for_claim"]),
        "",
        "## Local Suppression Law",
        "",
        csv_table(law_rows, ["law_id", "quantity", "formula", "pass_condition", "status", "valid_for_claim"]),
        "",
        "## Suppression Runner Input Template",
        "",
        csv_table(runner_inputs, ["row_id", "row_status", "active_gamma_coeff", "small_parameter", "support_power", "metric_response_coeff", "numeric_ready", "valid_for_claim", "notes"]),
        "",
        "## Suppression Runner Output",
        "",
        csv_table(runner_outputs, ["row_id", "runner_status", "active_gamma_bound", "Khat_norm_bound", "newton_ppn_fraction_bound", "required_gamma_bound", "observable_pass", "block_reason", "valid_for_claim"]),
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
    mode_rows = mode_split_rows(generated_utc)
    metric_rows = metric_null_rows(generated_utc)
    law_rows = suppression_law_rows(generated_utc)
    runner_inputs = runner_input_rows(generated_utc)
    runner_outputs = [run_suppression_row(row, generated_utc) for row in runner_inputs]
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, mode_rows, metric_rows, law_rows, runner_inputs, runner_outputs, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(MODE_SPLIT_PATH, mode_rows, ["split_id", "statement", "derivation", "result", "open_condition", "valid_for_claim", "generated_utc"])
    write_csv(METRIC_NULL_AUDIT_PATH, metric_rows, ["audit_id", "route", "required_identity", "current_status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(SUPPRESSION_LAW_PATH, law_rows, ["law_id", "quantity", "formula", "pass_condition", "status", "valid_for_claim", "generated_utc"])
    write_csv(
        RUNNER_INPUT_PATH,
        runner_inputs,
        [
            "row_id",
            "row_status",
            "dimension_n",
            "active_gamma_coeff",
            "small_parameter",
            "support_power",
            "K00_projection_fraction",
            "matter_curvature_norm",
            "metric_response_coeff",
            "observable_limit",
            "gamma_suppression_source_path",
            "small_parameter_source_path",
            "metric_response_source_path",
            "local_bound_source_path",
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
            "runner_status",
            "active_gamma_bound",
            "carrier_factor",
            "Khat_norm_bound",
            "newton_ppn_fraction_bound",
            "required_gamma_bound",
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
    write_document(source_rows, mode_rows, metric_rows, law_rows, runner_inputs, runner_outputs, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()

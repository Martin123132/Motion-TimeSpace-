from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1869"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
RUNS = ROOT / "runs" / "1869-R10-template-dryrun" / "results"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1869-Y5-R2FR-finite-local-coefficient-bound-branch-setup.md"
R10_RUNNER = ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py"
LIVE_R10_BOUND = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1869_SOURCE_REGISTER.csv",
    "component_schema": RESIDUALS / "P8_Y5_PARENT_QLOC_1869_COMPONENT_INPUT_SCHEMA.csv",
    "arena_projection_map": RESIDUALS / "P8_Y5_PARENT_QLOC_1869_ARENA_PROJECTION_MAP.csv",
    "r10_alpha_template": RESIDUALS / "P8_Y5_PARENT_QLOC_1869_R10_MTS_ALPHA_TEMPLATE_NONCLAIM.csv",
    "runner_command_manifest": RESIDUALS / "P8_Y5_PARENT_QLOC_1869_RUNNER_COMMAND_MANIFEST.csv",
    "r10_dryrun_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1869_R10_DRYRUN_STATUS.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1869_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1869_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1869_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1869_VALIDATION.csv",
}


def as_bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def path_has_needle(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def md_escape(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_register() -> list[dict[str, Any]]:
    sources = [
        {
            "source_id": "SRC1869_0_1868_doc",
            "source_kind": "current_handoff",
            "source_path": ROOT / "1868-Y5-R2FR-typed-parent-grammar-for-radial-cell-or-coefficient-bound-branch.md",
            "required_needle": "NEXT1868_0_primary",
            "use_in_1869": "selects the finite local coefficient-bound branch setup.",
        },
        {
            "source_id": "SRC1869_1_1868_validation",
            "source_kind": "validation_anchor",
            "source_path": RESIDUALS / "P8_Y5_BRR545_1868_VALIDATION.csv",
            "required_needle": "VAL1868_OVERALL",
            "use_in_1869": "confirms typed grammar checkpoint passed.",
        },
        {
            "source_id": "SRC1869_2_1868_coefficients",
            "source_kind": "coefficient_seed",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1868_COEFFICIENT_BOUND_BRANCH.csv",
            "required_needle": "CBB1868_0_ZR",
            "use_in_1869": "imports the finite coefficient list.",
        },
        {
            "source_id": "SRC1869_3_1578_pack",
            "source_kind": "component_pack_schema",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1578_COMPONENT_PACK_SCHEMA.csv",
            "required_needle": "PACK1578_1_ZR",
            "use_in_1869": "provides the earlier RAB finite component schema and no-claim gates.",
        },
        {
            "source_id": "SRC1869_4_1632_r10_kernel",
            "source_kind": "R10_kernel_contract",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1632_TAU_R10_KERNEL_CONTRACT.csv",
            "required_needle": "KERN1632_2_finite_operator",
            "use_in_1869": "provides finite-range R10 kernel formula requirements.",
        },
        {
            "source_id": "SRC1869_5_1632_alpha_template",
            "source_kind": "R10_alpha_template_seed",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1632_ALPHA_TEMPLATE_NONCLAIM.csv",
            "required_needle": "ALPHA1632_0_reciprocal_R10_template",
            "use_in_1869": "provides the nonclaim alpha template status.",
        },
        {
            "source_id": "SRC1869_6_1691_PPN",
            "source_kind": "PPN_residual_vector",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1691_PPN_RESIDUAL_VECTOR.csv",
            "required_needle": "PPNV1691_3_full_gamma_vector",
            "use_in_1869": "provides q_R_hat/gamma residual-vector bridge.",
        },
        {
            "source_id": "SRC1869_7_R10_runner",
            "source_kind": "existing_runner",
            "source_path": R10_RUNNER,
            "required_needle": "MTS_REQUIRED_COLUMNS",
            "use_in_1869": "validates the generated MTS alpha template against the existing R10 runner schema.",
        },
        {
            "source_id": "SRC1869_8_live_R10_bound_placeholder",
            "source_kind": "live_bound_placeholder",
            "source_path": LIVE_R10_BOUND,
            "required_needle": "R10_BOUND_PLACEHOLDER_0",
            "use_in_1869": "keeps the current live bound file blocked until real digitized rows are promoted.",
        },
    ]
    rows: list[dict[str, Any]] = []
    for source_entry in sources:
        source_path = source_entry["source_path"]
        needle = source_entry["required_needle"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_entry["source_id"],
                "source_kind": source_entry["source_kind"],
                "source_path": str(source_path),
                "path_exists": as_bool_text(source_path.exists()),
                "required_needle": needle,
                "needle_found": as_bool_text(path_has_needle(source_path, needle)),
                "use_in_1869": source_entry["use_in_1869"],
                "valid_for_claim": as_bool_text(False),
            }
        )
    return rows


def component_schema() -> list[dict[str, Any]]:
    rows = [
        ("FLC1869_0_qRhat", "q_R_hat_or_Q_R", "local reciprocal hair amplitude", "PPN;orbital;local_GR", "MISSING_QR_VALUE_OR_ZERO_THEOREM", "parent no-charge theorem or numeric Q_R/q_R_hat with source denominator"),
        ("FLC1869_1_ZR", "Z_R", "reciprocal gradient stiffness", "R10;PPN;clock;orbital;local_GR", "MISSING_PARENT_OPERATOR_ZR", "parent Hessian/operator extraction with action normalization"),
        ("FLC1869_2_MR2", "M_R^2", "mass gap/range owner", "R10;clock;orbital", "MISSING_PARENT_OPERATOR_MR2", "parent mass-gap extraction; lambda_R=sqrt(Z_R/M_R^2) only after Z_R and M_R^2 are same-normalization"),
        ("FLC1869_3_lambdaR", "lambda_R", "finite interaction range", "R10;clock;orbital", "MISSING_RANGE_RELATION", "derive from Z_R/M_R^2 or source an independent parent range law"),
        ("FLC1869_4_beta_source", "beta_source_R", "source-leg reciprocal matter charge", "R10;WEP;clock", "MISSING_SOURCE_CHARGE_OR_ZERO_THEOREM", "source material charge or parent matter descent zero theorem"),
        ("FLC1869_5_beta_test", "beta_test_R", "test-leg reciprocal matter charge", "R10;WEP;clock", "MISSING_TEST_CHARGE_OR_ZERO_THEOREM", "test material/readout charge or parent matter descent zero theorem"),
        ("FLC1869_6_JR", "J_R", "bulk reciprocal source current", "PPN;orbital;local_GR", "MISSING_SOURCE_CURRENT", "source-current density with compact support/worldtube convention"),
        ("FLC1869_7_boundary", "B_R_or_Pi_Rn_or_epsilon_tail", "boundary/readout tail", "R10;PPN;clock;orbital;local_GR", "MISSING_BOUNDARY_TAIL_OR_ZERO_THEOREM", "absolute boundary tail or theorem-zero; no cancellation against bulk"),
        ("FLC1869_8_tau_R10", "tau_R10_or_K_R", "R10 alpha(lambda) projection", "R10", "MISSING_R10_PROJECTION_OR_ACCEPTED_CURVE", "R10 source/test support kernel plus accepted bound curve"),
        ("FLC1869_9_tau_PPN", "tau_PPN_or_C_QR", "PPN residual projection", "PPN;local_GR", "MISSING_PPN_PROJECTION", "q_R_hat/Q_R to gamma/beta/light-time mapping with same source frame"),
        ("FLC1869_10_tau_clock", "tau_clock", "clock/redshift projection", "clock;WEP", "MISSING_CLOCK_PROJECTION", "fractional-frequency/material sensitivity kernel"),
        ("FLC1869_11_tau_orbital", "tau_orbital", "orbital residual projection", "orbital;local_GR", "MISSING_ORBITAL_PROJECTION", "acceleration/precession/timing kernel in PPN-compatible frame"),
        ("FLC1869_12_SR_total", "S_R_total", "source side of D_R=partial_r C_R-S_R", "local_GR;PPN;orbital", "MISSING_SOURCE_MAP", "no-cancellation sum of q_loc, matter, boundary, readout, current, and reciprocal slots"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "component_id": component_id,
            "symbol": symbol,
            "role": role,
            "arenas": arenas,
            "status": status,
            "accepted_input_forms": accepted,
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "units": "MISSING_UNITS_OR_NORMALIZATION",
            "source_path": "MISSING_SOURCE_PATH",
            "parent_signed": as_bool_text(False),
            "score_ready": as_bool_text(False),
            "valid_prediction_row": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
        }
        for component_id, symbol, role, arenas, status, accepted in rows
    ]


def arena_projection_map() -> list[dict[str, Any]]:
    rows = [
        (
            "APM1869_0_R10",
            "R10_fifth_force",
            "alpha_R(lambda)=K_R^R10(lambda)*beta_source_R*beta_test_R+epsilon_tail_R",
            "lambda_R, Z_R, M_R^2, K_R^R10, beta_source_R, beta_test_R, epsilon_tail_R, accepted alpha_bound(lambda)",
            "R10 runner template is executable but current rows are invalid placeholders",
        ),
        (
            "APM1869_1_PPN",
            "PPN_gamma_beta_light_time",
            "gamma_minus_1=q_R_hat+delta_gauge+delta_source+delta_boundary+delta_readout+O(U_N); beta requires second-order source-owner gate",
            "q_R_hat/Q_R, kappa_W, source denominator, gauge/readout tails, beta/conservation/common-matter gates",
            "PPN residual vector exists but values are missing",
        ),
        (
            "APM1869_2_clock",
            "clock_redshift_constants",
            "delta_nu/nu=tau_clock*q_R_hat+clock_tail_R under declared material/clock convention",
            "tau_clock, clock material sensitivities, source frame, constant-superselection or finite material coefficients",
            "clock projection is a named row only",
        ),
        (
            "APM1869_3_orbital",
            "orbital_precession_acceleration",
            "delta_orbit=tau_orbital*q_R_hat+orbital_tail_R in the same source frame as PPN",
            "tau_orbital, source denominator, acceleration/precession/timing kernel, boundary tail",
            "orbital projection is a named row only",
        ),
        (
            "APM1869_4_local_GR",
            "local_GR_Newton_reduction",
            "local pass requires q_R_hat=Z_R=J_R=Q_R=boundary/readout/source tails=0 or all finite residuals bounded below local sensitivity",
            "typed grammar/no-charge theorem or complete finite residual bounds across R10/PPN/clock/orbital",
            "no local-GR/Newton claim",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "arena_id": arena_id,
            "arena": arena,
            "projection_formula": formula,
            "required_inputs": required_inputs,
            "current_status": "BLOCKED_NONCLAIM",
            "notes": notes,
            "score_ready": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
        }
        for arena_id, arena, formula, required_inputs, notes in rows
    ]


def r10_alpha_template() -> list[dict[str, Any]]:
    return [
        {
            "model_id": "MTS_R2FR_1869_finite_RAB_template",
            "branch_id": BRANCH_ID,
            "curve_id": "R10_ALPHA_1869_TEMPLATE_NONCLAIM",
            "lambda_value": "MISSING_LAMBDA_R_FROM_ZR_MR2",
            "lambda_units": "m",
            "alpha_predicted": "MISSING_KR_BETA_SOURCE_BETA_TEST_EPSILON_TAIL",
            "alpha_bound": "MISSING_JOINED_BOUND",
            "alpha_bound_source": rel(LIVE_R10_BOUND),
            "force_law_form": "alpha_R(lambda)=K_R^R10(lambda)*beta_source_R*beta_test_R+epsilon_tail_R",
            "derivation_status": "TEMPLATE_INVALID_MISSING_PARENT_COEFFICIENTS",
            "formula_reference": rel(RESIDUALS / "P8_Y5_PARENT_QLOC_1632_TAU_R10_KERNEL_CONTRACT.csv"),
            "source_file": "MISSING_SOURCE_FILE",
            "assumptions": "no single-coupling shortcut; no cancellation; beta_source and beta_test are separate legs",
            "valid_for_claim": "false",
            "notes": "schema-compatible placeholder for R10_alpha_lambda_bound_prediction_runner.py; expected to fail validation until parent coefficients and accepted bound curve exist",
        }
    ]


def runner_command_manifest() -> list[dict[str, Any]]:
    command = [
        sys.executable,
        str(R10_RUNNER),
        "--mts-curve",
        str(OUTPUTS["r10_alpha_template"]),
        "--bound-curve",
        str(LIVE_R10_BOUND),
        "--output-dir",
        str(RUNS),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "command_id": "RCM1869_0_R10_template_dryrun",
            "runner": str(R10_RUNNER),
            "command": " ".join(f'"{part}"' if " " in part else part for part in command),
            "mts_curve": str(OUTPUTS["r10_alpha_template"]),
            "bound_curve": str(LIVE_R10_BOUND),
            "output_dir": str(RUNS),
            "dryrun_only": as_bool_text(True),
            "expected_claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "command_id": "RCM1869_1_future_local_vector",
            "runner": "future finite-local vector runner",
            "command": "not_run_until_numeric_component_rows_exist",
            "mts_curve": str(OUTPUTS["component_schema"]),
            "bound_curve": "R10/PPN/clock/orbital source packs",
            "output_dir": "runs/<timestamp>-finite-local-vector",
            "dryrun_only": as_bool_text(True),
            "expected_claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def run_r10_dryrun() -> list[dict[str, Any]]:
    if RUNS.exists():
        shutil.rmtree(RUNS)
    RUNS.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        str(R10_RUNNER),
        "--mts-curve",
        str(OUTPUTS["r10_alpha_template"]),
        "--bound-curve",
        str(LIVE_R10_BOUND),
        "--output-dir",
        str(RUNS),
    ]
    completed = subprocess.run(command, cwd=str(ROOT), text=True, capture_output=True, timeout=120, check=False)
    status_path = RUNS / "R10_runner_status.json"
    if status_path.exists():
        status = json.loads(status_path.read_text(encoding="utf-8"))
    else:
        status = {}
    return [
        {
            "branch_id": BRANCH_ID,
            "dryrun_id": "R10DRY1869_0_template_runner",
            "return_code": completed.returncode,
            "status_path": str(status_path),
            "mts_rows": status.get("mts_rows", "MISSING_STATUS"),
            "bound_rows": status.get("bound_rows", "MISSING_STATUS"),
            "valid_mts_rows": status.get("valid_mts_rows", "MISSING_STATUS"),
            "valid_bound_rows": status.get("valid_bound_rows", "MISSING_STATUS"),
            "comparison_rows": status.get("comparison_rows", "MISSING_STATUS"),
            "R10_pass_for_claim": as_bool_text(bool(status.get("R10_pass_for_claim", False))),
            "claim_allowed": as_bool_text(bool(status.get("claim_allowed", False))),
            "expected_blocker": "template and live bound placeholders must produce zero claim-ready comparisons",
            "stdout_tail": completed.stdout[-500:],
            "stderr_tail": completed.stderr[-500:],
            "valid_for_claim": as_bool_text(False),
        }
    ]


def claim_gate() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1869_0_component_values",
            "claim": "finite local coefficients are sourced",
            "status": "BLOCKED",
            "blocking_reason": "MISSING_NUMERIC_VALUES_SOURCE_PATHS_UNITS",
            "required_before_claim": "fill component rows with theorem-zero or numeric source-backed values.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1869_1_R10",
            "claim": "R10 alpha(lambda) branch passes",
            "status": "BLOCKED",
            "blocking_reason": "R10_TEMPLATE_INVALID_AND_BOUND_CURVE_PLACEHOLDER",
            "required_before_claim": "valid MTS alpha rows plus accepted alpha_bound(lambda) curve and runner pass.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1869_2_PPN_clock_orbital",
            "claim": "PPN/clock/orbital finite residuals are below bounds",
            "status": "BLOCKED",
            "blocking_reason": "MISSING_ARENA_PROJECTIONS_AND_NUMERIC_COMPONENTS",
            "required_before_claim": "source tau_PPN, tau_clock, tau_orbital and run no-cancellation residual vector.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1869_3_local_GR",
            "claim": "finite branch establishes local GR/Newton reduction",
            "status": "BLOCKED",
            "blocking_reason": "FINITE_BOUND_SETUP_NOT_A_DERIVATION",
            "required_before_claim": "theorem-zero branch or complete cross-arena finite-bound demonstration with PPN beta/conservation/common matter.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1869_0_result",
            "decision": "FINITE_LOCAL_COEFFICIENT_BRANCH_SCHEMA_READY_NONCLAIM",
            "basis": "component schema unifies 1868 with earlier 1578/1632/1691 local-bound machinery.",
            "consequence": "future fills must use theorem-zero or source-backed numeric rows; no symbolic placeholders promoted.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1869_1_R10_dryrun",
            "decision": "R10_TEMPLATE_DRYRUN_BLOCKS_AS_EXPECTED",
            "basis": "existing R10 runner returns no claim pass on placeholder MTS and live placeholder bound files.",
            "consequence": "pipeline failure mode is executable and safe.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1869_2_next",
            "decision": "FIRST_FILL_TARGET_QR_ZR_MR2_SOURCE_CHAIN",
            "basis": "R10 and PPN both need range/amplitude/charge normalization before any arena score.",
            "consequence": "attack Q_R/Z_R/M_R^2 and source denominator first, then tau projections.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1869_0_primary",
            "target_doc": "1870-Y5-R2FR-QR-ZR-MR2-source-chain-first-fill-or-no-charge-return.md",
            "target_script": "scripts/Y5_R2FR_QR_ZR_MR2_source_chain_first_fill_or_no_charge_return_1870.py",
            "objective": "try to derive/source the minimal Q_R, Z_R, M_R^2, lambda_R and source-denominator chain needed by both R10 and PPN; if not, keep rows blocked.",
            "selection_status": "selected",
            "success_condition": "first theorem-zero or source-backed numeric row for range/amplitude/charge normalization, or an explicit blocker ledger proving no arena score is possible yet.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1869_1_parallel",
            "target_doc": "1870b-Y5-R2FR-accepted-R10-bound-curve-promotion-or-blocker.md",
            "target_script": "scripts/Y5_R2FR_accepted_R10_bound_curve_promotion_or_blocker_1870b.py",
            "objective": "separately promote a real accepted R10 bound curve or keep the live bound file placeholder-blocked.",
            "selection_status": "held_parallel",
            "success_condition": "claim-safe alpha_bound(lambda) curve or clear source/QA blocker.",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_fields = {
        "valid_for_claim",
        "claim_allowed",
        "claim_ready",
        "score_ready",
        "valid_prediction_row",
        "parent_signed",
        "R10_pass_for_claim",
        "expected_claim_allowed",
    }
    for rows in rows_by_name.values():
        for table_row in rows:
            for field_name in claim_fields:
                if str(table_row.get(field_name, "")).strip().lower() == "true":
                    return False
    return True


def missing_rows_not_ready(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for table_row in rows:
            contains_missing = any("MISSING_" in str(value) for value in table_row.values())
            if contains_missing:
                for field_name in ("valid_for_claim", "claim_allowed", "claim_ready", "score_ready", "valid_prediction_row"):
                    if str(table_row.get(field_name, "")).strip().lower() == "true":
                        return False
    return True


def csvs_parse(paths: list[Path]) -> bool:
    for csv_path in paths:
        with csv_path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
    return True


def copy_branch_outputs(paths: list[Path]) -> None:
    for branch_folder in (MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE):
        branch_folder.mkdir(parents=True, exist_ok=True)
    for output_path in paths:
        shutil.copy2(output_path, MICROSCOPE_RESIDUALS / output_path.name)
        shutil.copy2(output_path, QUARANTINE / output_path.name)
        shutil.copy2(output_path, RAB_QUEUE / f"JR1869_{output_path.name}")


def branch_copies_exist(paths: list[Path]) -> bool:
    for output_path in paths:
        expected_paths = [
            MICROSCOPE_RESIDUALS / output_path.name,
            QUARANTINE / output_path.name,
            RAB_QUEUE / f"JR1869_{output_path.name}",
        ]
        if not all(expected_path.exists() for expected_path in expected_paths):
            return False
    return True


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1869*"))


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], non_validation_paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    component_rows = rows_by_name["component_schema"]
    arena_rows = rows_by_name["arena_projection_map"]
    template_rows = rows_by_name["r10_alpha_template"]
    dryrun_rows = rows_by_name["r10_dryrun_status"]
    claim_rows = rows_by_name["claim_gate"]
    decision_rows = rows_by_name["decision_ledger"]
    next_rows = rows_by_name["next_target"]

    runner_status_path = RUNS / "R10_runner_status.json"
    runner_status = json.loads(runner_status_path.read_text(encoding="utf-8")) if runner_status_path.exists() else {}

    checks = [
        {
            "validation_id": "VAL1869_0_sources_exist",
            "status": "PASS" if all(row["path_exists"] == "True" for row in source_rows) else "FAIL",
            "detail": "all cited source paths exist",
        },
        {
            "validation_id": "VAL1869_1_needles_present",
            "status": "PASS" if all(row["needle_found"] == "True" for row in source_rows) else "FAIL",
            "detail": "all cited source needles are present",
        },
        {
            "validation_id": "VAL1869_2_component_schema_complete",
            "status": "PASS" if len(component_rows) >= 13 and any(row["symbol"] == "Z_R" for row in component_rows) else "FAIL",
            "detail": "component schema covers Z_R/M_R2/J_R/Q_R/tau rows",
        },
        {
            "validation_id": "VAL1869_3_arena_map_complete",
            "status": "PASS" if len(arena_rows) >= 5 and any(row["arena"] == "R10_fifth_force" for row in arena_rows) else "FAIL",
            "detail": "arena projection map covers R10/PPN/clock/orbital/local-GR",
        },
        {
            "validation_id": "VAL1869_4_R10_template_schema",
            "status": "PASS" if set(template_rows[0].keys()) >= {"model_id", "curve_id", "lambda_value", "alpha_predicted", "valid_for_claim"} else "FAIL",
            "detail": "R10 alpha template has runner-required shape",
        },
        {
            "validation_id": "VAL1869_5_R10_dryrun_blocks",
            "status": "PASS" if runner_status.get("R10_pass_for_claim") is False and runner_status.get("valid_mts_rows") == 0 else "FAIL",
            "detail": "existing R10 runner blocks placeholder template as expected",
        },
        {
            "validation_id": "VAL1869_6_dryrun_status_recorded",
            "status": "PASS" if dryrun_rows and dryrun_rows[0]["R10_pass_for_claim"] == "False" else "FAIL",
            "detail": "dryrun status CSV records no R10 claim pass",
        },
        {
            "validation_id": "VAL1869_7_claim_gates_blocked",
            "status": "PASS" if all(row["status"] == "BLOCKED" for row in claim_rows) else "FAIL",
            "detail": "all finite branch claim gates remain blocked",
        },
        {
            "validation_id": "VAL1869_8_no_claim_flags",
            "status": "PASS" if all_claim_flags_false(rows_by_name) else "FAIL",
            "detail": "no generated claim or gate-pass flag is true",
        },
        {
            "validation_id": "VAL1869_9_missing_not_ready",
            "status": "PASS" if missing_rows_not_ready(rows_by_name) else "FAIL",
            "detail": "no MISSING_* row is marked score-ready or claim-ready",
        },
        {
            "validation_id": "VAL1869_10_decision_next",
            "status": "PASS" if any(row["decision"] == "FIRST_FILL_TARGET_QR_ZR_MR2_SOURCE_CHAIN" for row in decision_rows) else "FAIL",
            "detail": "decision ledger selects Q_R/Z_R/M_R2 chain next",
        },
        {
            "validation_id": "VAL1869_11_next_selected",
            "status": "PASS" if any(row["route_id"] == "NEXT1869_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL",
            "detail": "next target selected",
        },
        {
            "validation_id": "VAL1869_12_csv_parse",
            "status": "PASS" if csvs_parse(non_validation_paths) else "FAIL",
            "detail": "all generated non-validation CSVs parse",
        },
        {
            "validation_id": "VAL1869_13_branch_copies",
            "status": "PASS" if branch_copies_exist(non_validation_paths) else "FAIL",
            "detail": "branch/quarantine/queue copies exist",
        },
        {
            "validation_id": "VAL1869_14_pycache_absent",
            "status": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent",
        },
        {
            "validation_id": "VAL1869_15_formalization_untouched",
            "status": "PASS" if formalization_untouched() else "FAIL",
            "detail": "no 1869 outputs found under formalization-workbench",
        },
    ]
    overall_status = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "validation_id": "VAL1869_OVERALL",
            "status": overall_status,
            "detail": "1869 finite local coefficient-bound branch setup checkpoint",
        }
    )
    return [{**row, "branch_id": BRANCH_ID, "valid_for_claim": as_bool_text(False)} for row in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1869 - Y5/R2FR Finite Local Coefficient-Bound Branch Setup",
        "",
        "## Verdict",
        "",
        "1869 turns the failed theorem-zero route into an executable finite-residual branch without pretending it is evidence. The component schema now unifies the local reciprocal quantities needed by R10, PPN, clock, orbital and local-GR checks: `q_R_hat/Q_R`, `Z_R`, `M_R^2`, `lambda_R`, source/test matter charges, `J_R`, boundary tails, and the `tau` projection maps.",
        "",
        "The existing R10 alpha runner was dry-run against the new MTS alpha template and the current live placeholder bound curve. It blocks exactly as it should: there are no valid MTS rows and no R10 pass for claim. That is progress because the local-bound pipeline is now fail-safe rather than vibes-safe.",
        "",
        "**Claim ceiling:** no finite coefficient value, no R10 pass, no PPN/clock/orbital pass, no local-GR/Newton reduction claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1869.",
        "",
        "## Source Register",
        "",
        markdown_table(
            rows_by_name["source_register"],
            ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_1869", "valid_for_claim"],
        ),
        "",
        "## Component Input Schema",
        "",
        markdown_table(
            rows_by_name["component_schema"],
            ["component_id", "symbol", "role", "arenas", "status", "accepted_input_forms", "score_ready", "valid_for_claim"],
        ),
        "",
        "## Arena Projection Map",
        "",
        markdown_table(
            rows_by_name["arena_projection_map"],
            ["arena_id", "arena", "projection_formula", "required_inputs", "current_status", "score_ready", "valid_for_claim"],
        ),
        "",
        "## R10 Alpha Template",
        "",
        markdown_table(
            rows_by_name["r10_alpha_template"],
            ["model_id", "curve_id", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status", "valid_for_claim"],
        ),
        "",
        "## Runner Command Manifest",
        "",
        markdown_table(
            rows_by_name["runner_command_manifest"],
            ["command_id", "runner", "command", "dryrun_only", "expected_claim_allowed", "valid_for_claim"],
        ),
        "",
        "## R10 Dryrun Status",
        "",
        markdown_table(
            rows_by_name["r10_dryrun_status"],
            ["dryrun_id", "return_code", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "valid_for_claim"],
        ),
        "",
        "## Claim Gate",
        "",
        markdown_table(
            rows_by_name["claim_gate"],
            ["claim_id", "claim", "status", "blocking_reason", "required_before_claim", "claim_allowed", "valid_for_claim"],
        ),
        "",
        "## Decision Ledger",
        "",
        markdown_table(
            rows_by_name["decision_ledger"],
            ["decision_id", "decision", "basis", "consequence", "claim_allowed", "valid_for_claim"],
        ),
        "",
        "## Next Target",
        "",
        markdown_table(
            rows_by_name["next_target"],
            ["route_id", "target_doc", "target_script", "objective", "selection_status", "success_condition", "valid_for_claim"],
        ),
        "",
        "## Validation",
        "",
        markdown_table(
            rows_by_name["validation"],
            ["validation_id", "status", "detail", "valid_for_claim"],
        ),
        "",
        "## Plain-English Status",
        "",
        "We have not pulled off local GR yet. But we have turned the missing coupling/range problem into a disciplined first-fill queue. The next best shot is `Q_R/Z_R/M_R^2`: that chain decides whether the surviving finite branch is a massless PPN hair problem, a finite-range R10 problem, or a theorem-zero/no-charge return.",
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "component_schema": component_schema(),
        "arena_projection_map": arena_projection_map(),
        "r10_alpha_template": r10_alpha_template(),
        "runner_command_manifest": runner_command_manifest(),
    }

    for output_name in ("source_register", "component_schema", "arena_projection_map", "r10_alpha_template", "runner_command_manifest"):
        write_csv(OUTPUTS[output_name], rows_by_name[output_name])

    rows_by_name["r10_dryrun_status"] = run_r10_dryrun()
    write_csv(OUTPUTS["r10_dryrun_status"], rows_by_name["r10_dryrun_status"])

    rows_by_name["claim_gate"] = claim_gate()
    rows_by_name["decision_ledger"] = decision_ledger()
    rows_by_name["next_target"] = next_target()
    for output_name in ("claim_gate", "decision_ledger", "next_target"):
        write_csv(OUTPUTS[output_name], rows_by_name[output_name])

    non_validation_paths = [path for name, path in OUTPUTS.items() if name != "validation"]
    copy_branch_outputs(non_validation_paths)
    remove_pycache()
    rows_by_name["validation"] = validation_rows(rows_by_name, non_validation_paths)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    copy_branch_outputs([OUTPUTS["validation"]])
    remove_pycache()


if __name__ == "__main__":
    main()

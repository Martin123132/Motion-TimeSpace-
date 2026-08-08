from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1314"
TITLE = "1314-Y5-R10-RAB-finite-alpha-coupling-scorepack-or-parent-primitive-source"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
INPUT_SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_ALPHA_SCOREPACK_INPUT_SCHEMA.csv"
SOURCE_ACQUISITION_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_ACQUISITION_LEDGER.csv"
RUNNER_ROWS_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_READY_NONCLAIM_ROWS.csv"
R10_GATE_PATH = OUT_DIR / f"{PACK_ID}_R10_FINITE_BRANCH_GATE.csv"
PARENT_PRIMITIVE_PATH = OUT_DIR / f"{PACK_ID}_PARENT_PRIMITIVE_ESCAPE_HATCH.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1314_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        INPUT_SCHEMA_PATH,
        SOURCE_ACQUISITION_PATH,
        RUNNER_ROWS_PATH,
        R10_GATE_PATH,
        PARENT_PRIMITIVE_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1314_0_1313_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1313_NEXT_TARGET.csv",
            "needle": "NEXT1313_0_1314",
            "role": "handoff into finite alpha coupling scorepack",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1314_1_1313_queue",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1313_FINITE_COUPLING_SCOREPACK_QUEUE.csv",
            "needle": "FSQ1313_3_r10",
            "role": "RAB alpha/clock/WEP/R10 scorepack queue",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1314_2_1313_alpha_inputs",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1313_ALPHA_PRODUCT_INPUT_BRIDGE_NONCLAIM.csv",
            "needle": "API1313_3_r10",
            "role": "RAB alpha product missing-input bridge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1314_3_1221_schema",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1221_FINITE_CLOSURE_INPUT_SCHEMA.csv",
            "needle": "SCHEMA1221_4_readout_kernel",
            "role": "generic finite closure input schema",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1314_4_1221_acq",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1221_SOURCE_ACQUISITION_LEDGER.csv",
            "needle": "ACQ1221_0_alpha",
            "role": "generic finite closure acquisition rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1314_5_1221_runner_rows",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1221_RUNNER_READY_NONCLAIM_ROWS.csv",
            "needle": "RUN1221_0_alpha",
            "role": "runner-ready nonclaim refusal pattern",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1314_6_1221_escape",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1221_PARENT_PRIMITIVE_ESCAPE_HATCH.csv",
            "needle": "PESC1221_0_parent_grammar",
            "role": "parent primitive escape hatch pattern",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1314_7_1222_score",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1222_FIRST_NONCLAIM_SCORE_TABLE.csv",
            "needle": "NCS1222_0_alpha",
            "role": "mechanical first nonclaim score table",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1314_8_1223_narrow",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1223_NARROWED_BLOCKER_LEDGER.csv",
            "needle": "NAR1223_0_alpha",
            "role": "narrowed proof/source blockers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1314_9_1112_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1112_ALPHA_PRODUCT_RUNNER_CONTRACT_NONCLAIM.csv",
            "needle": "APC1112_2_R10_alpha_product",
            "role": "strict alpha product runner contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1314_10_1113_acq",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1113_ALPHA_PRODUCT_INPUT_ACQUISITION_LEDGER.csv",
            "needle": "AQ1113_4_r10_branch",
            "role": "alpha product input acquisition rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1314_11_clock_bound",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
            "needle": "ACB1052_2",
            "role": "clock product bound source-backed but product-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1314_12_wep_pressure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv",
            "needle": "AWP1052_0_alpha_Coulomb",
            "role": "WEP alpha/Coulomb pressure target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1314_13_r10_bound_status",
            "local_path": "source-intake/local_bounds/P8_Y5_R10_570_REVIEW_CANDIDATE_QA.csv",
            "needle": "review_candidate",
            "role": "R10 review-candidate bound status remains nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    input_schema = [
        {
            "schema_id": "AS1314_0_coefficient",
            "input_name": "alpha coefficient or theorem-zero",
            "required_for": "clock;WEP;R10;EM alpha product rows",
            "minimum_usable_form": "numeric b_alpha/c_alpha with units, sign/absolute convention, branch_id, normalization, source_path, or signed theorem-zero",
            "refusal_if_missing": "alpha product rows remain score_ready=false",
            "current_status": "MISSING_SOURCE_BACKED_ALPHA_COEFFICIENT_OR_THEOREM_ZERO",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "AS1314_1_clock_tau",
            "input_name": "tau_clock_time or direct clock product",
            "required_for": "clock product route",
            "minimum_usable_form": "tau_clock/Xhat map or direct P_clock_alpha prediction with readout model and source path",
            "refusal_if_missing": "clock bound cannot become standalone b_alpha",
            "current_status": "MISSING_CLOCK_READOUT_MAP",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "AS1314_2_wep_source",
            "input_name": "beta_source_alpha, tau_WEP, material/readout map",
            "required_for": "MICROSCOPE/WEP alpha product",
            "minimum_usable_form": "source-normalization coefficient, tau_WEP, material pair/DeltaQ_alpha, readout kernel, source profile, and provenance",
            "refusal_if_missing": "WEP product cannot score; beta_source_alpha/tau_WEP cannot be set to unity",
            "current_status": "MISSING_SOURCE_NORMALIZATION_AND_TAU_WEP",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "AS1314_3_r10_vector",
            "input_name": "R10 finite alpha product vector",
            "required_for": "R10 short-range alpha(lambda)",
            "minimum_usable_form": "lambda_X, Z_X, K_X(lambda), beta_source(lambda), beta_test(lambda), tau_R10, epsilon_tail, promoted alpha_bound(lambda), source paths",
            "refusal_if_missing": "R10 alpha product cannot score",
            "current_status": "MISSING_R10_FINITE_BRANCH_INPUTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "AS1314_4_cross_arena",
            "input_name": "shared alpha branch/readout classifier",
            "required_for": "joint clock/WEP/R10/local evidence statement",
            "minimum_usable_form": "same parent Z_Q_eff branch, domain classifier, readout functor, and arena-specific product maps",
            "refusal_if_missing": "no clock-to-WEP/R10 transfer shortcut",
            "current_status": "MISSING_CROSS_ARENA_PARENT_MAP",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "AS1314_5_parent_primitive",
            "input_name": "new parent grammar primitive",
            "required_for": "reopening theorem-zero route",
            "minimum_usable_form": "primitive statement plus parent action clause, typed coefficient domain, no-hidden-argument rule, radiative/readout closure, source path",
            "refusal_if_missing": "typed grammar remains closure-only; finite rows remain live",
            "current_status": "NEW_PRIMITIVE_SOURCE_REQUIRED_TO_REOPEN_THEOREM_ROUTE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    source_acquisition = [
        {
            "acquisition_id": "ACQ1314_0_alpha",
            "scorepack_row": "RUN1314_0_alpha",
            "needed_object": "b_alpha/c_alpha coefficient or theorem-zero",
            "arena": "clock;WEP;R10;EM",
            "minimum_usable_form": "numeric coefficient with units/provenance/normalization or signed EM-F2/no-hidden/readout theorem",
            "available_pressure": "abs(c_alpha_DD) <= 8.3202449332435330e-10 threshold only",
            "missing_or_status": "MISSING_SOURCE_BACKED_ALPHA_COEFFICIENT_OR_PARENT_PRIMITIVE",
            "priority": "P0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acquisition_id": "ACQ1314_1_clock",
            "scorepack_row": "RUN1314_1_clock",
            "needed_object": "tau_clock_time or direct P_clock_alpha",
            "arena": "clock;spectroscopy",
            "minimum_usable_form": "direct MTS clock product or tau_clock/Xhat map with clock readout model and units",
            "available_pressure": "abs(b_alpha*tau_clock_time) <= 2.1e-18 yr^-1 bound only",
            "missing_or_status": "MISSING_CLOCK_READOUT_MAP_OR_DIRECT_PRODUCT",
            "priority": "P0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acquisition_id": "ACQ1314_2_wep",
            "scorepack_row": "RUN1314_2_wep",
            "needed_object": "beta_source_alpha*tau_WEP/material map or direct P_WEP_alpha",
            "arena": "MICROSCOPE_WEP;local source",
            "minimum_usable_form": "beta_source_alpha, tau_WEP, DeltaQ_alpha/material map, readout kernel, source/worldtube profile, source paths",
            "available_pressure": "abs(P_WEP_alpha) <= 4.7977805227320001e-05 pressure target only",
            "missing_or_status": "MISSING_SOURCE_NORMALIZATION_TAU_WEP_MATERIAL_READOUT",
            "priority": "P0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acquisition_id": "ACQ1314_3_r10",
            "scorepack_row": "RUN1314_3_r10",
            "needed_object": "finite R10 alpha(lambda) product vector",
            "arena": "R10_short_range",
            "minimum_usable_form": "lambda_X, Z_X, K_X(lambda), beta_source(lambda), beta_test(lambda), tau_R10, epsilon_tail, real promoted alpha_bound(lambda), source paths",
            "available_pressure": "review-candidate/anchor-only bound rows remain nonclaim",
            "missing_or_status": "MISSING_R10_FINITE_BRANCH_VECTOR_AND_PROMOTED_BOUND",
            "priority": "P0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acquisition_id": "ACQ1314_4_cross_arena",
            "scorepack_row": "RUN1314_4_cross_arena",
            "needed_object": "shared branch classifier across clock/WEP/R10",
            "arena": "cross_arena",
            "minimum_usable_form": "one parent branch/readout map or explicit statement that products are separate and cannot transfer",
            "available_pressure": "separate nonclaim pressure rows",
            "missing_or_status": "MISSING_CROSS_ARENA_PARENT_MAP",
            "priority": "P1",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "acquisition_id": "ACQ1314_5_parent_primitive",
            "scorepack_row": "PESC1314_0_parent_primitive",
            "needed_object": "new parent grammar primitive",
            "arena": "theory",
            "minimum_usable_form": "source-backed primitive clause that forbids hidden scalar visible coefficients and preserves readout",
            "available_pressure": "none in current corpus",
            "missing_or_status": "NEW_PRIMITIVE_SOURCE_NOT_FOUND",
            "priority": "P1_escape_hatch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_rows = [
        {
            "runner_row_id": "RUN1314_0_alpha",
            "observable_product": "abs(c_alpha_DD or b_alpha)",
            "threshold_abs": "8.3202449332435330e-10",
            "threshold_units": "dimensionless",
            "predicted_abs_value": "MISSING_PREDICTED_VALUE",
            "required_inputs": "b_alpha_or_c_alpha;units;source_path;normalization;theorem_zero_flag",
            "available_inputs": "threshold_abs_only",
            "missing_inputs": "MISSING_SOURCE_BACKED_ALPHA_COEFFICIENT_OR_PARENT_PRIMITIVE",
            "counterexample_lock": "HSC1313_1_alpha",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_row_id": "RUN1314_1_clock",
            "observable_product": "abs(b_alpha*tau_clock_time)",
            "threshold_abs": "2.1e-18",
            "threshold_units": "yr^-1",
            "predicted_abs_value": "MISSING_MTS_CLOCK_PRODUCT",
            "required_inputs": "direct_product_or_tau_clock;clock_readout_model;source_path",
            "available_inputs": "source_bound_only",
            "missing_inputs": "MISSING_CLOCK_READOUT_MAP_OR_DIRECT_PRODUCT",
            "counterexample_lock": "HSC1313_3_clock_readout",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_row_id": "RUN1314_2_wep",
            "observable_product": "abs(beta_source_alpha*b_alpha*tau_WEP)",
            "threshold_abs": "4.7977805227320001e-05",
            "threshold_units": "dimensionless",
            "predicted_abs_value": "MISSING_MTS_WEP_PRODUCT",
            "required_inputs": "beta_source_alpha;b_alpha_or_zero;tau_WEP;DeltaQ_alpha;material_map;readout_kernel;source_profile",
            "available_inputs": "pressure_target_only",
            "missing_inputs": "MISSING_SOURCE_NORMALIZATION_TAU_WEP_MATERIAL_READOUT",
            "counterexample_lock": "HSC1313_4_source_weight",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_row_id": "RUN1314_3_r10",
            "observable_product": "abs(P_R10_alpha(lambda))",
            "threshold_abs": "MISSING_PROMOTED_ALPHA_BOUND_CURVE",
            "threshold_units": "dimensionless_alpha_lambda",
            "predicted_abs_value": "MISSING_R10_NUMERIC_PRODUCT",
            "required_inputs": "lambda_X;Z_X;K_X;beta_source;beta_test;tau_R10;epsilon_tail;alpha_bound_lambda;source_path",
            "available_inputs": "review_candidate_or_anchor_only_nonclaim",
            "missing_inputs": "MISSING_R10_FINITE_BRANCH_VECTOR_AND_PROMOTED_BOUND",
            "counterexample_lock": "HSC1313_1_alpha;HSC1313_4_source_weight",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_row_id": "RUN1314_4_cross_arena",
            "observable_product": "shared alpha branch consistency",
            "threshold_abs": "not_a_numeric_threshold",
            "threshold_units": "branch_identity",
            "predicted_abs_value": "MISSING_PARENT_BRANCH_MAP",
            "required_inputs": "same_ZQeff_branch;domain_classifier;readout_functor;arena_product_maps",
            "available_inputs": "separate_pressure_rows_only",
            "missing_inputs": "MISSING_CROSS_ARENA_PARENT_MAP",
            "counterexample_lock": "HSC1313_0_generic;HSC1313_3_clock_readout",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    r10_gate = [
        {
            "gate_id": "R10G1314_0_product",
            "requirement": "finite R10 alpha product vector",
            "current_status": "MISSING_R10_NUMERIC_PRODUCT",
            "details": "lambda_X, Z_X, K_X(lambda), beta_source, beta_test, tau_R10, and epsilon_tail are not sourced",
            "runner_effect": "R10 row refused",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "R10G1314_1_bound_curve",
            "requirement": "promoted claim-valid alpha_bound(lambda) curve",
            "current_status": "MISSING_PROMOTED_BOUND_CURVE",
            "details": "review-candidate/anchor-only rows are useful smoke data, not claim-valid bound evidence",
            "runner_effect": "R10 row refused even if MTS product becomes numeric",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "R10G1314_2_source_test",
            "requirement": "source/test beta factors and finite-source/readout map",
            "current_status": "MISSING_SOURCE_TEST_PROJECTION",
            "details": "source-weight and test-body coupling counterexamples remain active",
            "runner_effect": "no symbolic source/test shortcut",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "R10G1314_3_verdict",
            "requirement": "R10 finite alpha branch score-ready",
            "current_status": "R10_SCOREPACK_SCHEMA_ONLY_NONCLAIM",
            "details": "both MTS product vector and promoted bound curve are missing",
            "runner_effect": "no R10 pass/fail result",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    parent_primitive = [
        {
            "primitive_id": "PESC1314_0_parent_grammar",
            "would_reopen_route": "typed no-hidden-visible theorem",
            "minimum_signature": "one parent grammar forbids hidden scalar arguments in visible coefficients before readout",
            "current_status": "NOT_FOUND_IN_CURRENT_CORPUS",
            "effect_if_found": "reopen theorem-zero route for alpha/source-weight branch",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "primitive_id": "PESC1314_1_alpha_F2",
            "would_reopen_route": "b_alpha/c_alpha theorem-zero",
            "minimum_signature": "f(I_hid)F_Q^2 is ill-typed, quotient-trivial, or radiatively/readout forbidden",
            "current_status": "COUNTEREXAMPLE_ACTIVE",
            "effect_if_found": "close RUN1314_0_alpha if readout closure also signs",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "primitive_id": "PESC1314_2_source_weight",
            "would_reopen_route": "WEP/R10 source normalization theorem-zero",
            "minimum_signature": "source-only species weights are syntactically impossible or quotient-gauge redundant",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "effect_if_found": "close beta_source_alpha/source-weight side after tau/readout projection",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "primitive_id": "PESC1314_3_readout",
            "would_reopen_route": "observed clock/WEP/R10 transfer",
            "minimum_signature": "S_eff, loops, spectroscopy, and local readout preserve the same coefficient domain",
            "current_status": "UNSIGNED",
            "effect_if_found": "prevent readout regeneration counterexample",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1314_0_rows_score_ready",
            "claim": "alpha/clock/WEP/R10 scorepack rows are executable claim rows",
            "status": "BLOCKED",
            "reason": "all runner rows have missing inputs and valid_prediction_row=false",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1314_1_parent_primitive",
            "claim": "parent primitive reopens theorem-zero route",
            "status": "BLOCKED",
            "reason": "no new primitive source found; escape hatch is only a schema",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1314_2_r10",
            "claim": "R10 alpha branch can score",
            "status": "BLOCKED",
            "reason": "R10 product vector and promoted bound curve missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1314_3_wep",
            "claim": "WEP alpha/source branch can score",
            "status": "BLOCKED",
            "reason": "beta_source_alpha, tau_WEP, material/readout map, and source profile missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1314_4_local_GR",
            "claim": "local GR/Newton/PPN follows",
            "status": "BLOCKED",
            "reason": "finite alpha coupling scorepack is not a GR derivation and source Hamiltonian/PPN gates remain separate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1314_0_scorepack_created",
            "decision": "create RAB alpha finite coupling scorepack as nonclaim source-acquisition interface",
            "because": "the theorem route is currently demoted and tests need explicit finite rows rather than symbolic placeholders",
            "next_action": "build a mechanical runner that reads RUN1314 rows and refuses all current rows for the recorded reasons",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1314_1_r10_status",
            "decision": "R10 remains schema-only",
            "because": "finite product vector and promoted real bound curve are both missing",
            "next_action": "after runner refusal, choose whether to source R10 bound/product inputs or attack source-weight owner first",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1314_2_parent_escape",
            "decision": "keep parent primitive escape hatch but do not use it as evidence",
            "because": "a new primitive would be powerful, but none is present in the current corpus",
            "next_action": "require source-backed primitive statement before reopening theorem-zero route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1314_0_1315",
            "target_file": "1315-Y5-R10-RAB-alpha-scorepack-runner-first-nonclaim-table.md",
            "target_script": "scripts/Y5_R10_RAB_alpha_scorepack_runner_first_nonclaim_table.py",
            "task": "build a mechanical runner that reads the 1314 scorepack rows and outputs an explicit first nonclaim table with refusal reasons and zero valid predictions",
            "success_condition": "runner parses every 1314 row, keeps all score_ready=false, and records exact missing inputs without allowing unity/threshold shortcuts",
            "do_not": "do not source-fill coefficients by assumption; do not claim WEP/R10/local-GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    output_specs = [
        (SOURCE_REGISTER_PATH, source_register),
        (INPUT_SCHEMA_PATH, input_schema),
        (SOURCE_ACQUISITION_PATH, source_acquisition),
        (RUNNER_ROWS_PATH, runner_rows),
        (R10_GATE_PATH, r10_gate),
        (PARENT_PRIMITIVE_PATH, parent_primitive),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decision),
        (NEXT_PATH, next_target),
    ]
    for path, rows in output_specs:
        write_csv(path, rows)

    validations: list[dict[str, object]] = []
    validations.append(
        validation_row(
            "VAL1314_0_sources_exist",
            "registered source paths exist and anchors are found",
            all(row["exists"] and row["needle_found"] for row in source_register),
            f"{sum(1 for row in source_register if row['exists'] and row['needle_found'])}/{len(source_register)} source anchors found",
        )
    )
    validations.append(
        validation_row(
            "VAL1314_1_schema_complete",
            "scorepack schema covers alpha, clock, WEP, R10, cross-arena, and parent primitive inputs",
            len(input_schema) == 6 and all(row["current_status"].startswith("MISSING") or row["current_status"].startswith("NEW_PRIMITIVE") for row in input_schema),
            ";".join(f"{row['schema_id']}={row['current_status']}" for row in input_schema),
        )
    )
    validations.append(
        validation_row(
            "VAL1314_2_acquisition_nonclaim",
            "source acquisition rows are nonclaim and priority-labelled",
            len(source_acquisition) == 6 and all(row["priority"].startswith("P") for row in source_acquisition),
            ";".join(f"{row['acquisition_id']}={row['missing_or_status']}" for row in source_acquisition),
        )
    )
    validations.append(
        validation_row(
            "VAL1314_3_runner_rows_refuse",
            "runner-ready rows all refuse current claims",
            all(row["score_ready"] is False and row["valid_prediction_row"] is False for row in runner_rows),
            ";".join(f"{row['runner_row_id']}={row['missing_inputs']}" for row in runner_rows),
        )
    )
    validations.append(
        validation_row(
            "VAL1314_4_r10_gate_blocks",
            "R10 finite branch gate blocks score readiness",
            r10_gate[-1]["current_status"] == "R10_SCOREPACK_SCHEMA_ONLY_NONCLAIM",
            ";".join(f"{row['gate_id']}={row['current_status']}" for row in r10_gate),
        )
    )
    validations.append(
        validation_row(
            "VAL1314_5_parent_escape_not_evidence",
            "parent primitive escape hatch has no current claim-valid source",
            all(row["claim_allowed_now"] is False for row in parent_primitive),
            ";".join(f"{row['primitive_id']}={row['current_status']}" for row in parent_primitive),
        )
    )
    validations.append(
        validation_row(
            "VAL1314_6_claim_gates_block",
            "claim gates block scorepack, parent primitive, R10, WEP, and local-GR claims",
            all(row["status"] == "BLOCKED" for row in claim_gates),
            ";".join(f"{row['gate_id']}={row['status']}" for row in claim_gates),
        )
    )

    parsed_details = []
    csv_parse_ok = True
    for path, _rows in output_specs:
        try:
            parsed_rows = read_csv(path)
            parsed_details.append(f"{path.name}:{len(parsed_rows)}")
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            parsed_details.append(f"{path.name}:ERROR:{exc}")
    validations.append(
        validation_row(
            "VAL1314_7_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        )
    )
    formalization_outputs = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1314_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_outputs) == 0,
            f"formalization_generated_output_count={len(formalization_outputs)}",
        )
    )
    tables = [
        source_register,
        input_schema,
        source_acquisition,
        runner_rows,
        r10_gate,
        parent_primitive,
        claim_gates,
        decision,
        next_target,
    ]
    validations.append(
        validation_row(
            "VAL1314_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim(tables),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1314_10_next_target_1315",
            "next target routes to alpha scorepack runner first nonclaim table",
            next_target[0]["next_id"] == "NEXT1314_0_1315",
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1314_11_overall",
            "overall 1314 validation",
            overall_pass,
            "1314 creates a RAB alpha finite coupling scorepack, keeps all rows nonclaim, and routes to a mechanical refusal runner",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# {TITLE}

**Current verdict:** 1314 creates the RAB alpha finite-coupling scorepack, but it does not score any physical claim. Alpha, clock, WEP, R10, cross-arena transfer, and parent-primitive rows all remain source-acquisition/nonclaim rows.

**Main progress:** the coupling branch is now runner-shaped. Every future alpha test must supply explicit coefficient, tau/readout, source-normalization, material, R10 product, bound-curve, and/or parent-primitive evidence before a row can become claim-valid.

**Decision:** build a mechanical first-runner next. It should refuse all current rows with exact blockers, so future source fills can be tested without smuggling unity assumptions or threshold-as-prediction moves.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Alpha Scorepack Input Schema

{markdown_table(input_schema, ["schema_id", "input_name", "required_for", "minimum_usable_form", "refusal_if_missing", "current_status", "valid_for_claim", "claim_allowed"])}

## Source Acquisition Ledger

{markdown_table(source_acquisition, ["acquisition_id", "scorepack_row", "needed_object", "arena", "minimum_usable_form", "available_pressure", "missing_or_status", "priority", "valid_for_claim", "claim_allowed"])}

## Runner-Ready Nonclaim Rows

{markdown_table(runner_rows, ["runner_row_id", "observable_product", "threshold_abs", "threshold_units", "predicted_abs_value", "required_inputs", "available_inputs", "missing_inputs", "counterexample_lock", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## R10 Finite Branch Gate

{markdown_table(r10_gate, ["gate_id", "requirement", "current_status", "details", "runner_effect", "valid_for_claim", "claim_allowed"])}

## Parent Primitive Escape Hatch

{markdown_table(parent_primitive, ["primitive_id", "would_reopen_route", "minimum_signature", "current_status", "effect_if_found", "claim_allowed_now", "valid_for_claim"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()

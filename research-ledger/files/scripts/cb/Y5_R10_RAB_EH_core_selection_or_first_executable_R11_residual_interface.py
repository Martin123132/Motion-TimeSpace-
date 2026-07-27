from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1340"
TITLE = "1340-Y5-R10-RAB-EH-core-selection-or-first-executable-R11-residual-interface"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
EH_CORE_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_EH_CORE_SELECTION_ATTEMPT.csv"
R11_INPUT_SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_R11_EXECUTABLE_INPUT_SCHEMA.csv"
R11_INPUT_TEMPLATE_PATH = OUT_DIR / f"{PACK_ID}_R11_EXECUTABLE_INPUT_TEMPLATE.csv"
R11_RUNNER_DRYRUN_PATH = OUT_DIR / f"{PACK_ID}_R11_RUNNER_DRYRUN.csv"
ZERO_ROUTE_REQUIREMENTS_PATH = OUT_DIR / f"{PACK_ID}_ZERO_ROUTE_REQUIREMENTS.csv"
BOUND_ROUTE_REQUIREMENTS_PATH = OUT_DIR / f"{PACK_ID}_BOUND_ROUTE_REQUIREMENTS.csv"
CLAIM_GATE_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATE.csv"
RUNNER_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_UPDATE.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1340_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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


def bool_false(value: object) -> bool:
    return str(value).strip().lower() == "false"


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    for table in tables:
        for row in table:
            if "valid_for_claim" in row and not bool_false(row.get("valid_for_claim", False)):
                return False
            if "claim_allowed" in row and not bool_false(row.get("claim_allowed", False)):
                return False
    return True


def generated_inside_formalization() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [path for path in FORMALIZATION.rglob("*1340*") if path.is_file()]


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def missing_markers(row: dict[str, object], fields: list[str]) -> list[str]:
    missing = []
    for field in fields:
        value = str(row.get(field, "")).strip()
        if value == "" or value.startswith("MISSING") or value in {"PLACEHOLDER", "TBD"}:
            missing.append(field)
    return missing


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1340_0_1339_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1339_NEXT_TARGET.csv",
            "needle": "NEXT1339_0_1340",
            "role": "selected 1340 target",
        },
        {
            "source_id": "SRC1340_1_1339_R11",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1339_R11_RESIDUAL_VECTOR_INTERFACE.csv",
            "needle": "R11V1339_0_R2_fR_scalar",
            "role": "1339 residual vector interface",
        },
        {
            "source_id": "SRC1340_2_1339_EH_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1339_EH_LEFT_HAND_REDUCTION_GATE.csv",
            "needle": "EHGate1339_2_second_order",
            "role": "1339 EH left-hand gate",
        },
        {
            "source_id": "SRC1340_3_1339_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1339_VALIDATION.csv",
            "needle": "VAL1339_12_overall",
            "role": "1339 pass gate",
        },
        {
            "source_id": "SRC1340_4_958_EH_attempt",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_958_EH_CORE_SELECTION_ATTEMPT.csv",
            "needle": "EH958_5_verdict",
            "role": "prior EH core selection attempt",
        },
        {
            "source_id": "SRC1340_5_958_R11_review",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_958_R11_NON_EH_VECTOR_REVIEW.csv",
            "needle": "R11REV958_1",
            "role": "prior R11 vector review",
        },
        {
            "source_id": "SRC1340_6_959_no_extra",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_959_NO_EXTRA_FIELD_CLAUSE_ATTEMPT.csv",
            "needle": "NEF959_5_verdict",
            "role": "no-extra-field clause",
        },
        {
            "source_id": "SRC1340_7_960_R2FR",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_960_R2_FR_ZERO_OR_BOUND_ATTEMPT.csv",
            "needle": "R2FR960_4_verdict",
            "role": "R2/fR zero-or-bound attempt",
        },
        {
            "source_id": "SRC1340_8_960_connection",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_960_P4_CONNECTION_SUBROW_REVIEW.csv",
            "needle": "P4REV960_0",
            "role": "torsion/nonmetricity connection subrow review",
        },
        {
            "source_id": "SRC1340_9_960_bound_pack",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_960_PRIORITY_BOUND_PACK.csv",
            "needle": "BPACK960_1",
            "role": "priority bound pack",
        },
        {
            "source_id": "SRC1340_10_963_runner_spec",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_963_R2FR_BOUND_RUNNER_SPEC.csv",
            "needle": "R2RUN963_4_decision_logic",
            "role": "R2/fR runner decision logic",
        },
        {
            "source_id": "SRC1340_11_964_template",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_964_R2FR_NONCLAIM_INPUT_TEMPLATE.csv",
            "needle": "R2IN964_0_mts_prediction_required",
            "role": "R2/fR nonclaim input template",
        },
        {
            "source_id": "SRC1340_12_964_runner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_964_R2FR_NONCLAIM_RUNNER_RESULT.csv",
            "needle": "R2RUN964_VERDICT",
            "role": "R2/fR nonclaim runner result",
        },
        {
            "source_id": "SRC1340_13_966_generator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_966_GENERATOR_ELIMINATION_LEDGER.csv",
            "needle": "GE966_6_orientation_time_arrow",
            "role": "orientation/connection residual generator",
        },
    ]
    source_register = []
    for spec in source_specs:
        exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "exists": exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    eh_core_attempt = [
        {
            "attempt_id": "EH1340_0_target",
            "claim": "derive metric-only second-order EH core for the local exterior",
            "formal_move": "show Fields_ext={g_obs}, Gamma=LC(g_obs), DeltaE_extra=0, and E[g] has at most second derivatives",
            "result": "TARGET_EXACT",
            "gap": "requires parent-signed no-extra-field, no-higher-derivative, and connection clauses",
            "promotion_status": "NOT_PROMOTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "EH1340_1_Lovelock_activation",
            "claim": "activate EH+Lambda by Lovelock-style conditions",
            "formal_move": "local 4D diffeo-invariant metric-only second-order equations imply E_munu=aG_munu+b g_munu",
            "result": "CONDITIONAL_MATHEMATICS_CLEAN",
            "gap": "MTS parent has not earned the conditions",
            "promotion_status": "CONDITIONAL_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "EH1340_2_R2FR_obstruction",
            "claim": "R2/fR terms are absent",
            "formal_move": "prove c_R2=c_fR=0 or topological/redundant",
            "result": "NOT_DERIVED",
            "gap": "second-order/no-extra-scalar theorem missing; bound route lacks coefficient/map/source inputs",
            "promotion_status": "R11_INTERFACE_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "EH1340_3_connection_obstruction",
            "claim": "torsion/nonmetricity/independent connection is absent",
            "formal_move": "prove Gamma=LC(g_obs) and no hypermomentum/connection residual couples locally",
            "result": "NOT_DERIVED",
            "gap": "Levi-Civita parent theorem and connection residual maps missing",
            "promotion_status": "R11_INTERFACE_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "EH1340_4_verdict",
            "claim": "EH core premises are parent-signed",
            "formal_move": "combine metric-only, second-order, LC, no-extra-sector, boundary harmlessness, and source-GM transfer",
            "result": "NOT_DERIVED_CURRENT_CORPUS",
            "gap": "at least R2/fR and torsion/nonmetricity remain live highest-priority residual families",
            "promotion_status": "BUILD_EXECUTABLE_R11_INTERFACE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    r11_input_schema = [
        {
            "schema_id": "R11SCHEMA1340_0_common",
            "operator_family": "all",
            "required_fields": "family;coefficient_symbol;coefficient_value;coefficient_units;normalization;branch_context;source_file;formula_reference;assumptions",
            "acceptance_rule": "reject if any coefficient/unit/normalization/source/formula field is missing or placeholder",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "R11SCHEMA1340_1_R2FR",
            "operator_family": "R2_fR_scalar_mode",
            "required_fields": "c_R2_or_c_fR;scalar_mass_or_lambda;alpha_scalar;gamma_beta_map;R10_alpha_lambda_map;screening_flag",
            "acceptance_rule": "zero theorem must be parent-signed OR numeric prediction must include scalar mass/coupling and source-backed bound curve",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "R11SCHEMA1340_2_connection",
            "operator_family": "torsion_nonmetricity",
            "required_fields": "c_T_or_c_Q;connection_component;WEP_map;clock_map;lightcone_map;spin_source_map;PPN_map",
            "acceptance_rule": "zero theorem must be parent-signed OR numeric prediction must include observable maps and source-backed bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    r11_input_template = [
        {
            "input_id": "R11IN1340_0_R2FR_prediction_required",
            "operator_family": "R2_fR_scalar_mode",
            "coefficient_symbol": "c_R2_or_c_fR",
            "coefficient_value": "MISSING_PARENT_INPUT",
            "coefficient_units": "MISSING_UNITS",
            "normalization": "MISSING_NORMALIZATION",
            "branch_context": "local_exterior_EH_residual",
            "weak_field_map": "MISSING_GAMMA_BETA_SCALAR_MASS_ALPHA_LAMBDA_MAP",
            "predicted_observable": "MISSING_ALPHA_LAMBDA_OR_PPN_VALUES",
            "bound_source": "MISSING_FULL_CURVE_OR_PPN_SOURCE",
            "formula_reference": "MISSING_FORMULA_REFERENCE",
            "source_file": "MISSING_SOURCE_FILE",
            "assumptions": "MISSING_ASSUMPTIONS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "R11IN1340_1_R2FR_zero_theorem_switch",
            "operator_family": "R2_fR_scalar_mode",
            "coefficient_symbol": "c_R2_or_c_fR",
            "coefficient_value": "0_IF_PARENT_SECOND_ORDER_NO_EXTRA_SCALAR_SIGNED_ELSE_MISSING",
            "coefficient_units": "not_applicable_if_zero",
            "normalization": "not_applicable_if_zero",
            "branch_context": "zero_route",
            "weak_field_map": "zero_if_parent_signed_else_missing",
            "predicted_observable": "zero_if_parent_signed_else_missing",
            "bound_source": "not_applicable_if_zero",
            "formula_reference": "962_relative_theorem_plus_missing_parent_signature",
            "source_file": "P8_Y5_R10_963_DERIVATIVE_ORDER_AUDIT.csv;P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv",
            "assumptions": "parent_second_order_no_extra_scalar_signature",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "R11IN1340_2_connection_prediction_required",
            "operator_family": "torsion_nonmetricity",
            "coefficient_symbol": "c_T_or_c_Q",
            "coefficient_value": "MISSING_PARENT_INPUT",
            "coefficient_units": "MISSING_UNITS",
            "normalization": "MISSING_CONNECTION_NORMALIZATION",
            "branch_context": "local_exterior_connection_residual",
            "weak_field_map": "MISSING_WEP_CLOCK_LIGHTCONE_SPIN_SOURCE_PPN_MAP",
            "predicted_observable": "MISSING_CONNECTION_RESIDUAL_VALUES",
            "bound_source": "MISSING_SOURCE_BACKED_CONNECTION_BOUND",
            "formula_reference": "MISSING_FORMULA_REFERENCE",
            "source_file": "MISSING_SOURCE_FILE",
            "assumptions": "MISSING_ASSUMPTIONS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "input_id": "R11IN1340_3_connection_zero_theorem_switch",
            "operator_family": "torsion_nonmetricity",
            "coefficient_symbol": "c_T_or_c_Q",
            "coefficient_value": "0_IF_PARENT_LEVI_CIVITA_CONNECTION_SIGNED_ELSE_MISSING",
            "coefficient_units": "not_applicable_if_zero",
            "normalization": "not_applicable_if_zero",
            "branch_context": "zero_route",
            "weak_field_map": "zero_if_parent_signed_else_missing",
            "predicted_observable": "zero_if_parent_signed_else_missing",
            "bound_source": "not_applicable_if_zero",
            "formula_reference": "P4 connection clause plus missing LC parent theorem",
            "source_file": "P8_Y5_R10_960_P4_CONNECTION_SUBROW_REVIEW.csv",
            "assumptions": "parent_Levi_Civita_connection_signature",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    required_template_fields = [
        "coefficient_value",
        "coefficient_units",
        "normalization",
        "weak_field_map",
        "predicted_observable",
        "bound_source",
        "formula_reference",
        "source_file",
        "assumptions",
    ]
    runner_dryrun = []
    for row in r11_input_template:
        missing = missing_markers(row, required_template_fields)
        zero_route = row["input_id"].endswith("zero_theorem_switch")
        parent_signed = False
        accepted = len(missing) == 0 and (not zero_route or parent_signed)
        if zero_route and not parent_signed:
            verdict = "REJECTED_ZERO_THEOREM_NOT_PARENT_SIGNED"
        elif missing:
            verdict = "REJECTED_MISSING_EXECUTABLE_INPUTS"
        else:
            verdict = "ACCEPTED_NONCLAIM_SMOKE_ONLY"
        runner_dryrun.append(
            {
                "run_id": row["input_id"].replace("R11IN", "R11RUN"),
                "input_id": row["input_id"],
                "operator_family": row["operator_family"],
                "accepted_for_scoring": accepted,
                "claim_allowed": False,
                "verdict": verdict,
                "missing_fields": ";".join(missing) if missing else "none",
                "reason": "strict R11 interface: no pass without parent-signed zero theorem or complete numeric prediction plus source-backed bound",
                "valid_for_claim": False,
            }
        )
    runner_dryrun.append(
        {
            "run_id": "R11RUN1340_VERDICT",
            "input_id": "all_rows",
            "operator_family": "R2_fR_scalar_mode;torsion_nonmetricity",
            "accepted_for_scoring": False,
            "claim_allowed": False,
            "verdict": "R11_BRANCH_BLOCKED_NONCLAIM",
            "missing_fields": "parent_zero_signature_or_numeric_prediction_and_source_backed_bounds",
            "reason": "first executable interface exists, but all rows remain rejected until real parent inputs or bound inputs are supplied",
            "valid_for_claim": False,
        }
    )

    zero_route_requirements = [
        {
            "zero_id": "ZERO1340_0_R2FR",
            "operator_family": "R2_fR_scalar_mode",
            "required_parent_theorem": "local exterior parent action is metric-only, second-order, and no-extra-scalar after reduction",
            "would_set": "c_R2_or_c_fR=0 and alpha_scalar=0",
            "current_status": "NOT_PARENT_SIGNED",
            "fallback_if_missing": "finite scalar mode R11 bound route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "zero_id": "ZERO1340_1_connection",
            "operator_family": "torsion_nonmetricity",
            "required_parent_theorem": "observed connection is Levi-Civita and independent torsion/nonmetricity carries no local source/readout coupling",
            "would_set": "c_T_or_c_Q=0",
            "current_status": "NOT_PARENT_SIGNED",
            "fallback_if_missing": "finite connection residual R11 bound route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    bound_route_requirements = [
        {
            "bound_id": "BOUND1340_0_R2FR",
            "operator_family": "R2_fR_scalar_mode",
            "needed_inputs": "c_R2_or_c_fR; units; scalar mass/coupling; gamma/beta map; alpha(lambda) map; screening context; source-backed R10/PPN bounds",
            "first_external_bound_family": "R10 alpha(lambda), Cassini/PPN gamma-beta, finite-range scalar tests",
            "current_status": "MISSING_EXECUTABLE_NUMERIC_INPUTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "BOUND1340_1_connection",
            "operator_family": "torsion_nonmetricity",
            "needed_inputs": "c_T_or_c_Q; units; connection component; WEP/clock/lightcone/spin/source/PPN maps; source-backed bounds",
            "first_external_bound_family": "WEP, clock, lightcone, spin-torsion, source-charge, and PPN connection tests",
            "current_status": "MISSING_EXECUTABLE_NUMERIC_INPUTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gate = [
        {
            "gate_id": "CLAIM1340_0_EH_core",
            "claim": "EH core selected",
            "allowed_if": "EH1340_4_verdict becomes parent-signed with all live residual families zeroed or retained below source-backed bounds",
            "current_status": "BLOCKED",
            "reason": "R2/fR and torsion/nonmetricity remain live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CLAIM1340_1_R11_score",
            "claim": "R11 residual branch score",
            "allowed_if": "runner accepts complete numeric prediction plus source-backed bound rows, or parent-signed zero theorem",
            "current_status": "BLOCKED",
            "reason": "runner dry-run rejects all rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CLAIM1340_2_local_GR_Newton",
            "claim": "local GR/Newton reduction",
            "allowed_if": "source closure derived/adopted, EH core selected or residuals bounded, GM transfer proven, PPN vector completed",
            "current_status": "BLOCKED",
            "reason": "1340 only creates first residual interface",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_update = [
        {
            "runner_id": "RUN1340_0_EH_core_selection",
            "target": "metric-only second-order EH core",
            "input_status": "PREMISES_UNSIGNED",
            "runner_status": "EH_CORE_NOT_DERIVED",
            "score_ready": False,
            "reason": "R2/fR and torsion/nonmetricity obstruction rows remain live",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1340_1_R11_interface",
            "target": "first executable R11 residual interface",
            "input_status": "SCHEMA_AND_REJECTION_RUNNER_WRITTEN",
            "runner_status": "EXECUTABLE_INTERFACE_NONCLAIM_READY",
            "score_ready": False,
            "reason": "interface can reject missing rows and accept future complete rows, but current rows are placeholders",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1340_0_EH_result",
            "decision": "EH core selection is not derived in 1340",
            "because": "highest-priority R2/fR and torsion/nonmetricity families remain zero-or-bound missing",
            "effect": "left-hand GR route remains conditional; R11 residual interface is now the honest next machinery",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1340_1_interface_result",
            "decision": "first executable R11 interface is established as strict nonclaim infrastructure",
            "because": "rows now state coefficient/unit/map/source requirements and the runner rejects placeholders",
            "effect": "future work can either derive zeros or fill real bound inputs without smuggling a pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1340_0_1341",
            "target_file": "1341-Y5-R10-RAB-R2FR-scalar-mode-zero-theorem-or-source-backed-bound-row.md",
            "target_script": "scripts/Y5_R10_RAB_R2FR_scalar_mode_zero_theorem_or_source_backed_bound_row.py",
            "task": "try the R2/fR scalar-mode zero theorem first; if it fails, prepare source-backed finite scalar bound rows using real R10/PPN bound inputs without claiming a pass",
            "success_condition": "either c_R2/c_fR is parent-zeroed, or the R2/fR branch has complete nonclaim coefficient/unit/map/source requirements ready for data acquisition",
            "do_not": "do not claim EH/local GR, do not treat anchor-only bound rows as full curve evidence, do not use missing MTS coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables_for_nonclaim = [
        source_register,
        eh_core_attempt,
        r11_input_schema,
        r11_input_template,
        runner_dryrun,
        zero_route_requirements,
        bound_route_requirements,
        claim_gate,
        runner_update,
        decision,
        next_target,
    ]

    source_anchor_count = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    eh_not_derived = any(row["attempt_id"] == "EH1340_4_verdict" and row["result"] == "NOT_DERIVED_CURRENT_CORPUS" for row in eh_core_attempt)
    schema_present = len(r11_input_schema) == 3 and len(r11_input_template) == 4
    runner_rejects_placeholders = all(row["accepted_for_scoring"] is False and row["claim_allowed"] is False for row in runner_dryrun)
    zero_routes_unsigned = all(row["current_status"] == "NOT_PARENT_SIGNED" for row in zero_route_requirements)
    bound_routes_missing = all(row["current_status"] == "MISSING_EXECUTABLE_NUMERIC_INPUTS" for row in bound_route_requirements)
    claims_blocked = all(row["current_status"] == "BLOCKED" for row in claim_gate)
    runners_not_scoreable = all(row["score_ready"] is False and row["valid_prediction_row"] is False for row in runner_update)
    nonclaim = all_nonclaim(tables_for_nonclaim)
    formal_clean = len(generated_inside_formalization()) == 0
    next_is_1341 = next_target[0]["target_file"].startswith("1341-")

    validations = [
        validation_row(
            "VAL1340_0_sources_exist",
            "registered local source paths exist and anchors are found",
            source_anchor_count == len(source_register),
            f"{source_anchor_count}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1340_1_EH_not_derived",
            "EH core selection is not promoted",
            eh_not_derived,
            "EH1340_4_verdict=NOT_DERIVED_CURRENT_CORPUS",
        ),
        validation_row(
            "VAL1340_2_schema_present",
            "R11 executable schema and templates are present",
            schema_present,
            f"schema_rows={len(r11_input_schema)};template_rows={len(r11_input_template)}",
        ),
        validation_row(
            "VAL1340_3_runner_rejects_placeholders",
            "R11 dry-run rejects placeholders and unsigned zero switches",
            runner_rejects_placeholders,
            ";".join(f"{row['run_id']}={row['verdict']}" for row in runner_dryrun),
        ),
        validation_row(
            "VAL1340_4_zero_routes_unsigned",
            "zero routes remain unsigned",
            zero_routes_unsigned,
            ";".join(f"{row['zero_id']}={row['current_status']}" for row in zero_route_requirements),
        ),
        validation_row(
            "VAL1340_5_bound_routes_missing",
            "finite bound routes remain missing executable numeric inputs",
            bound_routes_missing,
            ";".join(f"{row['bound_id']}={row['current_status']}" for row in bound_route_requirements),
        ),
        validation_row(
            "VAL1340_6_claims_blocked",
            "EH/R11/local-GR claims remain blocked",
            claims_blocked,
            ";".join(f"{row['gate_id']}={row['current_status']}" for row in claim_gate),
        ),
        validation_row(
            "VAL1340_7_runners_not_scoreable",
            "runners refuse EH/local-GR scoring",
            runners_not_scoreable,
            ";".join(f"{row['runner_id']}={row['runner_status']}" for row in runner_update),
        ),
        validation_row(
            "VAL1340_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim,
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1340_9_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            formal_clean,
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        ),
        validation_row(
            "VAL1340_10_next_target_1341",
            "next target routes to R2/fR scalar-mode zero theorem or source-backed bound row",
            next_is_1341,
            str(next_target[0]["target_file"]),
        ),
    ]
    validations.append(
        validation_row(
            "VAL1340_11_overall",
            "overall 1340 validation",
            all(row["status"] == "PASS" for row in validations),
            "1340 does not derive EH core, but creates a strict first executable nonclaim R11 interface for R2/fR and torsion/nonmetricity",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(EH_CORE_ATTEMPT_PATH, eh_core_attempt)
    write_csv(R11_INPUT_SCHEMA_PATH, r11_input_schema)
    write_csv(R11_INPUT_TEMPLATE_PATH, r11_input_template)
    write_csv(R11_RUNNER_DRYRUN_PATH, runner_dryrun)
    write_csv(ZERO_ROUTE_REQUIREMENTS_PATH, zero_route_requirements)
    write_csv(BOUND_ROUTE_REQUIREMENTS_PATH, bound_route_requirements)
    write_csv(CLAIM_GATE_PATH, claim_gate)
    write_csv(RUNNER_UPDATE_PATH, runner_update)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# {TITLE}

**Current verdict:** 1340 does not derive the EH core. The metric-only second-order route remains conditional because `R2/fR` and torsion/nonmetricity are still live highest-priority residual families.

**Main progress:** the first executable nonclaim R11 interface now exists. It gives strict coefficient/unit/normalization/weak-field-map/source requirements for `R2/fR scalar mode` and `torsion/nonmetricity`, and the dry-run rejects every placeholder or unsigned zero switch.

**Decision:** next target is `1341`: attack the `R2/fR` scalar-mode zero theorem first; if that fails, prepare source-backed finite scalar bound rows without pretending anchor-only evidence or missing MTS coefficients are enough.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## EH Core Selection Attempt
{markdown_table(eh_core_attempt, ["attempt_id", "claim", "formal_move", "result", "gap", "promotion_status", "valid_for_claim", "claim_allowed"])}

## R11 Executable Input Schema
{markdown_table(r11_input_schema, ["schema_id", "operator_family", "required_fields", "acceptance_rule", "valid_for_claim", "claim_allowed"])}

## R11 Executable Input Template
{markdown_table(r11_input_template, ["input_id", "operator_family", "coefficient_symbol", "coefficient_value", "coefficient_units", "normalization", "branch_context", "weak_field_map", "predicted_observable", "bound_source", "formula_reference", "source_file", "assumptions", "valid_for_claim", "claim_allowed"])}

## R11 Runner Dryrun
{markdown_table(runner_dryrun, ["run_id", "input_id", "operator_family", "accepted_for_scoring", "claim_allowed", "verdict", "missing_fields", "reason", "valid_for_claim"])}

## Zero Route Requirements
{markdown_table(zero_route_requirements, ["zero_id", "operator_family", "required_parent_theorem", "would_set", "current_status", "fallback_if_missing", "valid_for_claim", "claim_allowed"])}

## Bound Route Requirements
{markdown_table(bound_route_requirements, ["bound_id", "operator_family", "needed_inputs", "first_external_bound_family", "current_status", "valid_for_claim", "claim_allowed"])}

## Claim Gate
{markdown_table(claim_gate, ["gate_id", "claim", "allowed_if", "current_status", "reason", "valid_for_claim", "claim_allowed"])}

## Runner Update
{markdown_table(runner_update, ["runner_id", "target", "input_status", "runner_status", "score_ready", "reason", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decision, ["decision_id", "decision", "because", "effect", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()

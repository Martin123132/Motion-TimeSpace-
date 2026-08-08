from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "751-Y5-R10-minimal-Palpha3-response-operator-or-q_loc-component-input-builder.md"
NEXT_TARGET = "752-Y5-R10-Palpha3-operator-source-hunt-or-q_loc-template-dryrun.md"
STATUS = "Y5_R10_751_minimal_Palpha3_operator_contract_written_component_input_builder_template_created_nonclaim"
CLAIM_CEILING = "minimal_Palpha3_operator_contract_and_q_loc_input_builder_template_only_no_fqV_no_Wqalpha3_no_alpha3_PPN_R10_Newton_or_local_GR_pass"
Q_PROXY = 7.432631961576971e-06
ALPHA3_BOUND = 4.0e-20
WF_LIMIT = ALPHA3_BOUND / Q_PROXY
UNIT_RATIO = Q_PROXY / ALPHA3_BOUND
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_751_SOURCE_REGISTER.csv"
OPERATOR_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_751_MINIMAL_PALPHA3_OPERATOR_CONTRACT.csv"
OPERATOR_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_751_OPERATOR_DERIVATION_AUDIT.csv"
INPUT_BUILDER_TEMPLATE_PATH = RESIDUALS / "P8_Y5_R10_751_QLOC_COMPONENT_INPUT_BUILDER_TEMPLATE.csv"
INPUT_BUILDER_RULES_PATH = RESIDUALS / "P8_Y5_R10_751_INPUT_BUILDER_RULES.csv"
PRODUCT_TEMPLATE_PATH = RESIDUALS / "P8_Y5_R10_751_QLOC_ALPHA3_PRODUCT_ROW_TEMPLATE.csv"
DRYRUN_STATUS_PATH = RESIDUALS / "P8_Y5_R10_751_BUILDER_DRYRUN_STATUS.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_751_DECISION_MATRIX.csv"
Y5_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_751_Y5_RUNNER_UPDATE.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_751_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_751_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_751_VALIDATION.csv"

COMPONENT_INPUT_CANDIDATE = RESIDUALS / "P8_Y5_R10_750_QLOC_COMPONENT_INPUT_CANDIDATE.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "750_doc": {
        "path": POST_CHECKPOINT / "750-Y5-R10-q_loc-Hodge-component-field-source-acquisition-or-alpha3-response-runner.md",
        "needles": [
            "no claim-valid component-resolved q_loc field/profile exists",
            "751-Y5-R10-minimal-Palpha3-response-operator-or-q_loc-component-input-builder.md",
            "derive the minimal",
        ],
        "role": "immediate 751 handoff",
    },
    "750_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_750_VALIDATION.csv",
        "needles": ["V750_16_validation_rows_ready", "V750_13_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "750_input_schema": {
        "path": RESIDUALS / "P8_Y5_R10_750_QLOC_COMPONENT_INPUT_SCHEMA.csv",
        "needles": ["QIN750_3_q_loc_components", "component-resolved q_loc field/profile"],
        "role": "q_loc component input requirements",
    },
    "750_hodge_schema": {
        "path": RESIDUALS / "P8_Y5_R10_750_HODGE_COMPONENT_RUNNER_SCHEMA.csv",
        "needles": ["HRS750_3_fqV", "blocked_no_Palpha3_or_q_field"],
        "role": "Hodge/f_qV runner schema",
    },
    "750_alpha3_schema": {
        "path": RESIDUALS / "P8_Y5_R10_750_ALPHA3_RESPONSE_RUNNER_SCHEMA.csv",
        "needles": ["A3S750_3_response_weight", "W_q_alpha3 := alpha3_q/epsilon_q_momentum"],
        "role": "alpha3 response runner schema",
    },
    "749_alpha3_contract": {
        "path": RESIDUALS / "P8_Y5_R10_749_ALPHA3_RESPONSE_OPERATOR_CONTRACT.csv",
        "needles": ["A3R749_2_weight_definition", "operator norm"],
        "role": "prior alpha3 response operator contract",
    },
    "ppn_metric_contract": {
        "path": RESIDUALS / "P8_Y5_PPN_METRIC_EXPANSION_CONTRACT.csv",
        "needles": ["MEX524_3_gravitomagnetic_preferred_frame", "alpha1=alpha2=alpha3=0"],
        "role": "PPN metric expansion alpha3 location",
    },
    "ppn_residual_vector": {
        "path": RESIDUALS / "P8_Y5_PPN_RESIDUAL_VECTOR.csv",
        "needles": ["PPN524_5_alpha3_flux", "alpha3<=4e-20"],
        "role": "PPN alpha3 residual row",
    },
    "ppn_input_template": {
        "path": RESIDUALS / "P8_Y5_PPN_EVALUATOR_INPUT_TEMPLATE.csv",
        "needles": ["PPN524_5_alpha3_flux", "not_loaded"],
        "role": "PPN evaluator missing input template",
    },
    "ppn_source_gates": {
        "path": RESIDUALS / "P8_Y5_PPN_SOURCE_STABILITY_GATES.csv",
        "needles": ["PSG524_6_preferred_frame_location_zero", "not_derived_not_scored"],
        "role": "PPN preferred-frame gate",
    },
    "local_prediction_template": {
        "path": RESIDUALS / "MTS_local_residual_predictions_TEMPLATE.csv",
        "needles": ["R7_alpha3", "alpha3-equivalent self-acceleration"],
        "role": "canonical local residual prediction template",
    },
    "alpha3_numeric_template": {
        "path": RESIDUALS / "P8_ALPHA3_NUMERIC_PRODUCT_INPUT_TEMPLATE.csv",
        "needles": ["A3_TOTAL_GUARD", "no hidden cancellation"],
        "role": "alpha3 product template precedent",
    },
    "alpha3_bound_eval": {
        "path": RESIDUALS / "P8_ALPHA3_BOUND_PRODUCT_EVALUATION.csv",
        "needles": ["not_scoreable_inputs_missing", "MISSING_NUMERIC_PRODUCT_OR_THEOREM_ZERO"],
        "role": "alpha3 product evaluator precedent",
    },
    "local_gr_residual_vector": {
        "path": RESIDUALS / "P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv",
        "needles": ["LRV_TOTAL_ALPHA3_GUARD", "MISSING_CHANNEL_VALUES"],
        "role": "local GR no-cancellation alpha3 guard",
    },
    "r11_vector_status": {
        "path": RESIDUALS / "R11_EXECUTABLE_VECTOR_STATUS.csv",
        "needles": ["vector_preferred_frame", "template_only"],
        "role": "R11 vector operator blocker",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def under_post(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            count += 1
    return count


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(spec["path"]),
            "exists": bool_string(Path(spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(spec["path"]), spec["needles"])),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, spec in SOURCES.items()
    ]


def operator_contract_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "factor_id": "PA3751_0_domain",
            "operator_factor": "P_Hodge",
            "mathematical_form": "q_loc -> (q_T, D sigma_q, q_V, q_H)",
            "needed_input": "component-resolved q_loc field, observed frame, domain weights, boundary conditions",
            "current_status": "schema_only_no_input",
            "output_if_filled": "component norms and q_V/q_H flux candidates",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "factor_id": "PA3751_1_flux",
            "operator_factor": "P_flux",
            "mathematical_form": "(q_V,q_H,boundary flux) -> epsilon_q_momentum",
            "needed_input": "preferred-frame/momentum-flux projection and same-frame normalization",
            "current_status": "missing",
            "output_if_filled": "epsilon_q_momentum and f_qV",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "factor_id": "PA3751_2_green",
            "operator_factor": "G_PPN",
            "mathematical_form": "source flux -> delta g_0i in the observed matter frame",
            "needed_input": "gauge-fixed weak-field linearized equations and boundary/source normalization",
            "current_status": "missing",
            "output_if_filled": "vector metric response",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "factor_id": "PA3751_3_ppn_projection",
            "operator_factor": "Pi_alpha3^PPN",
            "mathematical_form": "delta g_0i/vector momentum terms -> alpha3_q",
            "needed_input": "PPN alpha3 extraction convention, frame/velocity normalization, sign convention",
            "current_status": "missing",
            "output_if_filled": "alpha3_q",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "factor_id": "PA3751_4_minimal_composition",
            "operator_factor": "P_alpha3_min",
            "mathematical_form": "P_alpha3_min := Pi_alpha3^PPN o G_PPN o P_flux o P_Hodge",
            "needed_input": "all previous factors plus source paths and units",
            "current_status": "abstract_operator_contract_only",
            "output_if_filled": "W_q_alpha3 and/or theorem-zero certificate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def operator_audit_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "OPA751_0_can_define_minimal_operator",
            "question": "Can P_alpha3 be defined without picking a number?",
            "answer": "yes_as_abstract_composition",
            "blocker": "abstract composition is not an executable response coefficient",
            "claim_effect": "does not fill W_q_alpha3",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "OPA751_1_can_compute_W",
            "question": "Can W_q_alpha3 be computed now?",
            "answer": "no",
            "blocker": "G_PPN and Pi_alpha3^PPN are missing and q_loc component input is absent",
            "claim_effect": "W_q_alpha3 remains MISSING_ALPHA3_RESPONSE_OPERATOR",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "OPA751_2_can_theorem_zero",
            "question": "Can the minimal operator prove P_alpha3 q_loc=0?",
            "answer": "no_current_corpus",
            "blocker": "no parent theorem kills vector/flux/harmonic q_loc components through the response operator",
            "claim_effect": "structural zero remains a target, not a result",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "OPA751_3_can_make_input_builder",
            "question": "Can a no-fake-data component input builder template be written?",
            "answer": "yes",
            "blocker": "template row is not data and must remain valid_for_claim=false",
            "claim_effect": "future real q_loc fields can be dry-run checked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def input_builder_template_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "template_id": "QIB751_TEMPLATE_ROW_DO_NOT_SCORE",
            "sample_id": "MISSING_SAMPLE_ID",
            "domain_id": "MISSING_DOMAIN_ID",
            "weight_dV": "MISSING_WEIGHT",
            "frame_convention": "MISSING_FRAME_CONVENTION",
            "u0": "MISSING_U0",
            "u1": "MISSING_U1",
            "u2": "MISSING_U2",
            "u3": "MISSING_U3",
            "q0": "MISSING_Q0",
            "q1": "MISSING_Q1",
            "q2": "MISSING_Q2",
            "q3": "MISSING_Q3",
            "boundary_tag": "MISSING_BOUNDARY_TAG",
            "boundary_condition": "MISSING_BOUNDARY_CONDITION",
            "P_alpha3_x": "MISSING_PALPHA3_X",
            "P_alpha3_y": "MISSING_PALPHA3_Y",
            "P_alpha3_z": "MISSING_PALPHA3_Z",
            "response_operator_id": "MISSING_RESPONSE_OPERATOR_ID",
            "source_file": "MISSING_SOURCE_FILE",
            "status": "template_only_no_data",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def input_builder_rule_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "rule_id": "QBR751_0_no_proxy_fabrication",
            "rule": "Do not generate q_loc component samples from q_proxy.",
            "pass_condition": "all component rows come from a real source file or a parent-derived formula",
            "failure_action": "block dry-run and keep valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rule_id": "QBR751_1_frame_required",
            "rule": "Observed frame/normalization must be declared before splitting q_T and q_perp.",
            "pass_condition": "u^mu or local orthonormal frame convention is present and normalized",
            "failure_action": "block Hodge split",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rule_id": "QBR751_2_boundary_required",
            "rule": "Boundary conditions/topology are required before Hodge transverse/harmonic split.",
            "pass_condition": "boundary tags and adjacency/operator metadata exist",
            "failure_action": "block f_qV",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rule_id": "QBR751_3_response_required",
            "rule": "P_alpha3 or response_operator_id must be sourced before alpha3 scoring.",
            "pass_condition": "P_flux, G_PPN, and Pi_alpha3^PPN are real or theorem-zero is supplied",
            "failure_action": "block W_q_alpha3",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def product_template_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "input_id": "A3_QLOC_NUMERIC_OR_ZERO",
            "channel": "q_loc_projection",
            "target_row": "R7_alpha3",
            "observable": "alpha3",
            "product_symbol": "W_q_alpha3_f_qV",
            "coefficient_symbol": "W_q_alpha3",
            "epsilon_symbol": "f_qV",
            "coefficient_value": "MISSING_ALPHA3_RESPONSE_OPERATOR",
            "epsilon_value": "MISSING_QLOC_HODGE_COMPONENTS",
            "explicit_product_value": "MISSING_NUMERIC_OR_THEOREM_ZERO_PRODUCT",
            "product_units": "dimensionless",
            "target_bound": f"{WF_LIMIT:.15g}",
            "bound_units": "dimensionless_product_before_q_proxy",
            "acceptance_gate": f"abs(W_q_alpha3*f_qV) <= {WF_LIMIT:.15g}; equivalently abs(alpha3_q)<=4e-20",
            "theorem_zero_certificate": "MISSING_PARENT_QLOC_ALPHA3_ZERO_CERTIFICATE",
            "numeric_source_file": "MISSING_NUMERIC_SOURCE",
            "formula_reference": str(OPERATOR_CONTRACT_PATH),
            "assumptions": "same observed frame; no hidden cancellation; q_proxy denominator compatibility",
            "no_cancellation_policy": "q_loc alpha3 channel must pass independently unless parent identity forces cancellation",
            "current_status": "template_unfilled",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def dryrun_rows(generated_utc: str) -> list[dict[str, Any]]:
    candidate_exists = COMPONENT_INPUT_CANDIDATE.exists()
    return [
        {
            "dryrun_id": "DRY751_0_template_written",
            "check": "component input builder template exists",
            "target": str(INPUT_BUILDER_TEMPLATE_PATH),
            "result": "pass",
            "detail": "template row written with MISSING_* markers and valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "DRY751_1_candidate_input",
            "check": "real candidate q_loc input exists",
            "target": str(COMPONENT_INPUT_CANDIDATE),
            "result": "pass" if candidate_exists else "blocked",
            "detail": "candidate input exists" if candidate_exists else "no real component input file found; no Hodge/alpha3 computation run",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "DRY751_2_operator_executable",
            "check": "minimal P_alpha3 operator executable",
            "target": "Pi_alpha3^PPN o G_PPN o P_flux o P_Hodge",
            "result": "blocked",
            "detail": "abstract composition exists but G_PPN/Pi_alpha3/source inputs are missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D751_0_operator",
            "decision": "write minimal P_alpha3 composition contract",
            "meaning": "the response map is now a named composition, not an unnamed missing coefficient",
            "claim_status": "abstract_contract_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D751_1_no_W_fill",
            "decision": "do not fill W_q_alpha3",
            "meaning": "G_PPN, Pi_alpha3^PPN, P_flux, and q_loc component input are missing",
            "claim_status": "operator_not_executable",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D751_2_builder",
            "decision": "create q_loc component input builder template",
            "meaning": "future real data can be inserted without fabricating samples from q_proxy",
            "claim_status": "template_only_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D751_3_next",
            "decision": "hunt source for P_alpha3 operator or dry-run a real component file",
            "meaning": "next step should fill a real source for the operator or a real q_loc component candidate",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def y5_update_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "Y5R751_alpha3_q_loc",
            "source_row": "R7_alpha3/q_loc",
            "status_after_751": "minimal_operator_contract_written_product_template_unfilled",
            "zero_or_input": f"need theorem-zero or abs(W_q_alpha3 f_qV)<= {WF_LIMIT:.15g}",
            "still_missing": "G_PPN; Pi_alpha3^PPN; P_flux; q_loc component input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R751_component_builder",
            "source_row": "q_loc component input builder",
            "status_after_751": "template_created_no_real_input",
            "zero_or_input": str(INPUT_BUILDER_TEMPLATE_PATH),
            "still_missing": str(COMPONENT_INPUT_CANDIDATE),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R751_PPN_vector",
            "source_row": "PPN524_5_alpha3_flux",
            "status_after_751": "not_promoted",
            "zero_or_input": "PPN alpha3 row still needs sourced derivation/vector file",
            "still_missing": "official/gauge-fixed extraction and weak-field response source",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU751_0_allowed",
            "allowed_after_751": "say P_alpha3_min is defined as an abstract response composition",
            "forbidden_after_751": "say W_q_alpha3 has been computed",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU751_1_allowed",
            "allowed_after_751": "use the component input builder template for future real q_loc data",
            "forbidden_after_751": "treat the template row as a candidate data row",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU751_2_allowed",
            "allowed_after_751": "hunt sources for G_PPN/Pi_alpha3/P_flux or derive theorem-zero",
            "forbidden_after_751": "choose response weights after seeing the alpha3 bound",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "minimal P_alpha3 operator composition written; q_loc component builder template created; no W/f product filled",
            "hard_blocker": "G_PPN, Pi_alpha3^PPN, P_flux, and real q_loc component input remain missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def make_validation(
    sources: list[dict[str, Any]],
    operator_contract: list[dict[str, Any]],
    operator_audit: list[dict[str, Any]],
    input_template: list[dict[str, Any]],
    builder_rules: list[dict[str, Any]],
    product_template: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    outputs: list[Path],
) -> list[dict[str, str]]:
    prior = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_750_VALIDATION.csv")
    all_rows = operator_contract + operator_audit + input_template + builder_rules + product_template + dryrun + decisions + y5_update + routes
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V751_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V751_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all source files contain expected evidence needles"})
    validation.append({"check_id": "V751_2_prior_750_clean", "result": "pass" if prior and all(row.get("result") == "pass" for row in prior) else "fail", "detail": "750 validation has no failures"})
    validation.append({"check_id": "V751_3_minimal_operator_written", "result": "pass" if any(row["operator_factor"] == "P_alpha3_min" for row in operator_contract) else "fail", "detail": "P_alpha3_min composition row exists"})
    validation.append({"check_id": "V751_4_operator_not_claimed", "result": "pass" if any(row["answer"] == "no" and row["audit_id"] == "OPA751_1_can_compute_W" for row in operator_audit) else "fail", "detail": "W_q_alpha3 not computed"})
    validation.append({"check_id": "V751_5_template_has_missing_markers", "result": "pass" if input_template and any("MISSING_" in str(value) for value in input_template[0].values()) else "fail", "detail": "component template is explicitly unfilled"})
    validation.append({"check_id": "V751_6_product_template_unfilled", "result": "pass" if product_template and product_template[0]["current_status"] == "template_unfilled" else "fail", "detail": "q_loc alpha3 product row unfilled"})
    validation.append({"check_id": "V751_7_dryrun_blocks_missing_input", "result": "pass" if any(row["dryrun_id"] == "DRY751_1_candidate_input" and row["result"] == "blocked" for row in dryrun) else "fail", "detail": "dry-run blocks without real input"})
    validation.append({"check_id": "V751_8_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_rows) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V751_9_no_local_arena_claim", "result": "pass" if "no_fqV_no_Wqalpha3_no_alpha3_PPN_R10_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "alpha3/PPN/R10/Newton/local-GR claims remain blocked"})
    validation.append({"check_id": "V751_10_next_target_selected", "result": "pass" if all(row.get("next_target") == NEXT_TARGET for row in decisions) else "fail", "detail": NEXT_TARGET})
    validation.append({"check_id": "V751_11_outputs_scoped", "result": "pass" if all(under_post(path) for path in outputs) else "fail", "detail": "all outputs under post-checkpoint-work"})
    changed = formalization_changed_after_cutoff()
    validation.append({"check_id": "V751_12_formalization_workbench_untouched", "result": "pass" if changed == 0 else "fail", "detail": f"formalization_changed_after_cutoff={changed}"})
    validation.append({"check_id": "V751_13_y5_rows_retained", "result": "pass" if {"Y5R751_alpha3_q_loc", "Y5R751_component_builder", "Y5R751_PPN_vector"}.issubset({row["runner_id"] for row in y5_update}) else "fail", "detail": "alpha3/component/PPN-vector rows retained"})
    validation.append({"check_id": "V751_14_route_forbids_template_as_data", "result": "pass" if any("template row as a candidate data row" in row["forbidden_after_751"] for row in routes) else "fail", "detail": "template cannot be treated as data"})
    validation.append({"check_id": "V751_15_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    operator_contract: list[dict[str, Any]],
    operator_audit: list[dict[str, Any]],
    input_template: list[dict[str, Any]],
    builder_rules: list[dict[str, Any]],
    product_template: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 751 - Y5 R10 Minimal Palpha3 Response Operator Or q_loc Component Input Builder

Start point: 750 proved that no claim-valid component-resolved `q_loc` field/profile exists yet. It also identified the response side of the product as missing:

```text
alpha3_q = W_q_alpha3 * f_qV * q_proxy
required: |W_q_alpha3 f_qV| <= {WF_LIMIT:.15g}
```

Current result: **a minimal `P_alpha3` response operator can be defined as an abstract composition, but it cannot be executed or used as evidence yet**:

```text
P_alpha3_min := Pi_alpha3^PPN o G_PPN o P_flux o P_Hodge
```

That is useful because it names exactly what has to be sourced. It is not a number, not a pass, and not a replacement for real component data. 751 also writes a no-fake-data `q_loc` component input builder template with explicit `MISSING_*` markers.

## Summary

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | minimal P_alpha3 operator contract written; component input builder template created |
| Next target | `{NEXT_TARGET}` |

## Minimal P_alpha3 Operator Contract

{markdown_table(operator_contract, ["factor_id", "operator_factor", "mathematical_form", "needed_input", "current_status", "output_if_filled", "valid_for_claim"])}

## Operator Derivation Audit

{markdown_table(operator_audit, ["audit_id", "question", "answer", "blocker", "claim_effect", "valid_for_claim"])}

## q_loc Component Input Builder Template

{markdown_table(input_template, ["template_id", "sample_id", "domain_id", "weight_dV", "frame_convention", "q0", "q1", "q2", "q3", "P_alpha3_x", "P_alpha3_y", "P_alpha3_z", "response_operator_id", "source_file", "status", "valid_for_claim"])}

## Input Builder Rules

{markdown_table(builder_rules, ["rule_id", "rule", "pass_condition", "failure_action", "valid_for_claim"])}

## q_loc Alpha3 Product Row Template

{markdown_table(product_template, ["input_id", "channel", "target_row", "observable", "product_symbol", "coefficient_value", "epsilon_value", "explicit_product_value", "target_bound", "acceptance_gate", "current_status", "valid_for_claim"])}

## Dry-Run Status

{markdown_table(dryrun, ["dryrun_id", "check", "target", "result", "detail", "valid_for_claim"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Y5 Runner Update

{markdown_table(y5_update, ["runner_id", "source_row", "status_after_751", "zero_or_input", "still_missing", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_751", "forbidden_after_751", "next_action", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is a useful tightening. We are no longer saying vaguely “need alpha3 projection”; we have the exact skeleton. But the skeleton is still missing its muscles: `P_flux`, `G_PPN`, `Pi_alpha3^PPN`, and real `q_loc` component rows. The safe next move is source-hunt those operator pieces, or dry-run a real component file if one is later produced.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    operator_contract = operator_contract_rows(generated_utc)
    operator_audit = operator_audit_rows(generated_utc)
    input_template = input_builder_template_rows(generated_utc)
    builder_rules = input_builder_rule_rows(generated_utc)
    product_template = product_template_rows(generated_utc)
    dryrun = dryrun_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    y5_update = y5_update_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)

    outputs = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        OPERATOR_CONTRACT_PATH,
        OPERATOR_AUDIT_PATH,
        INPUT_BUILDER_TEMPLATE_PATH,
        INPUT_BUILDER_RULES_PATH,
        PRODUCT_TEMPLATE_PATH,
        DRYRUN_STATUS_PATH,
        DECISION_PATH,
        Y5_UPDATE_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]

    validation = make_validation(
        sources,
        operator_contract,
        operator_audit,
        input_template,
        builder_rules,
        product_template,
        dryrun,
        decisions,
        y5_update,
        routes,
        outputs,
    )

    write_csv(
        SOURCE_REGISTER_PATH,
        sources,
        ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OPERATOR_CONTRACT_PATH,
        operator_contract,
        ["factor_id", "operator_factor", "mathematical_form", "needed_input", "current_status", "output_if_filled", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OPERATOR_AUDIT_PATH,
        operator_audit,
        ["audit_id", "question", "answer", "blocker", "claim_effect", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        INPUT_BUILDER_TEMPLATE_PATH,
        input_template,
        [
            "template_id",
            "sample_id",
            "domain_id",
            "weight_dV",
            "frame_convention",
            "u0",
            "u1",
            "u2",
            "u3",
            "q0",
            "q1",
            "q2",
            "q3",
            "boundary_tag",
            "boundary_condition",
            "P_alpha3_x",
            "P_alpha3_y",
            "P_alpha3_z",
            "response_operator_id",
            "source_file",
            "status",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        INPUT_BUILDER_RULES_PATH,
        builder_rules,
        ["rule_id", "rule", "pass_condition", "failure_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        PRODUCT_TEMPLATE_PATH,
        product_template,
        [
            "input_id",
            "channel",
            "target_row",
            "observable",
            "product_symbol",
            "coefficient_symbol",
            "epsilon_symbol",
            "coefficient_value",
            "epsilon_value",
            "explicit_product_value",
            "product_units",
            "target_bound",
            "bound_units",
            "acceptance_gate",
            "theorem_zero_certificate",
            "numeric_source_file",
            "formula_reference",
            "assumptions",
            "no_cancellation_policy",
            "current_status",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        DRYRUN_STATUS_PATH,
        dryrun,
        ["dryrun_id", "check", "target", "result", "detail", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        DECISION_PATH,
        decisions,
        ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        Y5_UPDATE_PATH,
        y5_update,
        ["runner_id", "source_row", "status_after_751", "zero_or_input", "still_missing", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        ROUTE_PATH,
        routes,
        ["route_id", "allowed_after_751", "forbidden_after_751", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SUMMARY_PATH,
        summary,
        ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, operator_contract, operator_audit, input_template, builder_rules, product_template, dryrun, decisions, y5_update, routes, validation)

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"751 validation failed: {failed}")
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "752-Y5-R10-Palpha3-operator-source-hunt-or-q_loc-template-dryrun.md"
NEXT_TARGET = "753-Y5-R10-Palpha3-source-pack-or-parent-zero-theorem.md"
STATUS = "Y5_R10_752_local_Palpha3_operator_source_hunt_failed_template_dryrun_blocked_nonclaim"
CLAIM_CEILING = "local_Palpha3_source_hunt_and_q_loc_template_dryrun_only_no_fqV_no_Wqalpha3_no_alpha3_PPN_R10_Newton_or_local_GR_pass"
Q_PROXY = 7.432631961576971e-06
ALPHA3_BOUND = 4.0e-20
WF_LIMIT = ALPHA3_BOUND / Q_PROXY
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_752_SOURCE_REGISTER.csv"
OPERATOR_SOURCE_HUNT_PATH = RESIDUALS / "P8_Y5_R10_752_PALPHA3_OPERATOR_SOURCE_HUNT.csv"
OPERATOR_PIECE_STATUS_PATH = RESIDUALS / "P8_Y5_R10_752_OPERATOR_PIECE_STATUS.csv"
TEMPLATE_DRYRUN_PATH = RESIDUALS / "P8_Y5_R10_752_QLOC_TEMPLATE_DRYRUN.csv"
SOURCE_REQUIREMENTS_PATH = RESIDUALS / "P8_Y5_R10_752_SOURCE_REQUIREMENTS_QUEUE.csv"
PRODUCT_STATUS_PATH = RESIDUALS / "P8_Y5_R10_752_QLOC_ALPHA3_PRODUCT_STATUS.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_752_DECISION_MATRIX.csv"
Y5_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_752_Y5_RUNNER_UPDATE.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_752_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_752_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_752_VALIDATION.csv"

COMPONENT_INPUT_CANDIDATE = RESIDUALS / "P8_Y5_R10_750_QLOC_COMPONENT_INPUT_CANDIDATE.csv"
BUILDER_TEMPLATE = RESIDUALS / "P8_Y5_R10_751_QLOC_COMPONENT_INPUT_BUILDER_TEMPLATE.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "751_doc": {
        "path": POST_CHECKPOINT / "751-Y5-R10-minimal-Palpha3-response-operator-or-q_loc-component-input-builder.md",
        "needles": [
            "P_alpha3_min := Pi_alpha3^PPN o G_PPN o P_flux o P_Hodge",
            "752-Y5-R10-Palpha3-operator-source-hunt-or-q_loc-template-dryrun.md",
            "say W_q_alpha3 has been computed",
        ],
        "role": "immediate 752 handoff",
    },
    "751_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_751_VALIDATION.csv",
        "needles": ["V751_15_validation_rows_ready", "V751_12_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "751_operator_contract": {
        "path": RESIDUALS / "P8_Y5_R10_751_MINIMAL_PALPHA3_OPERATOR_CONTRACT.csv",
        "needles": ["PA3751_4_minimal_composition", "abstract_operator_contract_only"],
        "role": "minimal operator composition",
    },
    "751_operator_audit": {
        "path": RESIDUALS / "P8_Y5_R10_751_OPERATOR_DERIVATION_AUDIT.csv",
        "needles": ["OPA751_1_can_compute_W", "W_q_alpha3 remains MISSING_ALPHA3_RESPONSE_OPERATOR"],
        "role": "operator not executable guard",
    },
    "751_input_template": {
        "path": BUILDER_TEMPLATE,
        "needles": ["QIB751_TEMPLATE_ROW_DO_NOT_SCORE", "MISSING_Q0", "template_only_no_data"],
        "role": "q_loc template dry-run target",
    },
    "751_product_template": {
        "path": RESIDUALS / "P8_Y5_R10_751_QLOC_ALPHA3_PRODUCT_ROW_TEMPLATE.csv",
        "needles": ["A3_QLOC_NUMERIC_OR_ZERO", "MISSING_ALPHA3_RESPONSE_OPERATOR"],
        "role": "q_loc alpha3 product template",
    },
    "750_alpha3_schema": {
        "path": RESIDUALS / "P8_Y5_R10_750_ALPHA3_RESPONSE_RUNNER_SCHEMA.csv",
        "needles": ["A3S750_3_response_weight", "contract_only"],
        "role": "alpha3 response runner schema",
    },
    "750_hodge_schema": {
        "path": RESIDUALS / "P8_Y5_R10_750_HODGE_COMPONENT_RUNNER_SCHEMA.csv",
        "needles": ["HRS750_3_fqV", "blocked_no_Palpha3_or_q_field"],
        "role": "Hodge/f_qV runner schema",
    },
    "749_response_contract": {
        "path": RESIDUALS / "P8_Y5_R10_749_ALPHA3_RESPONSE_OPERATOR_CONTRACT.csv",
        "needles": ["A3R749_2_weight_definition", "contract_written_no_value"],
        "role": "prior alpha3 response contract",
    },
    "ppn_metric_contract": {
        "path": RESIDUALS / "P8_Y5_PPN_METRIC_EXPANSION_CONTRACT.csv",
        "needles": ["MEX524_3_gravitomagnetic_preferred_frame", "not_derived"],
        "role": "local PPN g0i alpha3 gate",
    },
    "ppn_residual_vector": {
        "path": RESIDUALS / "P8_Y5_PPN_RESIDUAL_VECTOR.csv",
        "needles": ["PPN524_5_alpha3_flux", "unfilled"],
        "role": "local PPN alpha3 row",
    },
    "ppn_input_template": {
        "path": RESIDUALS / "P8_Y5_PPN_EVALUATOR_INPUT_TEMPLATE.csv",
        "needles": ["PPN524_5_alpha3_flux", "not_loaded"],
        "role": "PPN evaluator template",
    },
    "ppn_source_gates": {
        "path": RESIDUALS / "P8_Y5_PPN_SOURCE_STABILITY_GATES.csv",
        "needles": ["PSG524_6_preferred_frame_location_zero", "not_derived_not_scored"],
        "role": "PPN preferred-frame gate",
    },
    "alpha3_numeric_template": {
        "path": RESIDUALS / "P8_ALPHA3_NUMERIC_PRODUCT_INPUT_TEMPLATE.csv",
        "needles": ["A3_TOTAL_GUARD", "total alpha3 cannot be scored"],
        "role": "existing alpha3 product template policy",
    },
    "alpha3_eval": {
        "path": RESIDUALS / "P8_ALPHA3_BOUND_PRODUCT_EVALUATION.csv",
        "needles": ["not_scoreable_inputs_missing", "MISSING_NUMERIC_PRODUCT_OR_THEOREM_ZERO"],
        "role": "existing alpha3 evaluator status",
    },
    "r11_status": {
        "path": RESIDUALS / "R11_EXECUTABLE_VECTOR_STATUS.csv",
        "needles": ["vector_preferred_frame", "template_only"],
        "role": "R11 vector-source blocker",
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


def operator_source_hunt_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "hunt_id": "OSH752_0_P_Hodge",
            "operator_piece": "P_Hodge",
            "local_candidate": str(RESIDUALS / "P8_Y5_R10_750_HODGE_COMPONENT_RUNNER_SCHEMA.csv"),
            "what_it_provides": "schema for q_T/q_perp/Hodge split and f_qV computation",
            "claim_grade": "false",
            "blocker": "no component-resolved q_loc field, frame, boundary, or mesh/operator input",
            "next_action": "dry-run only after real q_loc component input exists",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "hunt_id": "OSH752_1_P_flux",
            "operator_piece": "P_flux",
            "local_candidate": str(RESIDUALS / "P8_Y5_R10_751_MINIMAL_PALPHA3_OPERATOR_CONTRACT.csv"),
            "what_it_provides": "names flux projection target",
            "claim_grade": "false",
            "blocker": "no sourced map from q_V/q_H/boundary flux to epsilon_q_momentum",
            "next_action": "derive from parent momentum/Noether current or source a response map",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "hunt_id": "OSH752_2_G_PPN",
            "operator_piece": "G_PPN",
            "local_candidate": str(RESIDUALS / "P8_Y5_PPN_METRIC_EXPANSION_CONTRACT.csv"),
            "what_it_provides": "states g0i/alpha_i gate and weak-field metric target",
            "claim_grade": "false",
            "blocker": "no gauge-fixed weak-field Green operator from q_loc source to delta g_0i",
            "next_action": "source or derive linearized field equation and gauge/normalization convention",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "hunt_id": "OSH752_3_Pi_alpha3_PPN",
            "operator_piece": "Pi_alpha3^PPN",
            "local_candidate": str(RESIDUALS / "P8_Y5_PPN_RESIDUAL_VECTOR.csv"),
            "what_it_provides": "alpha3 residual row and bound",
            "claim_grade": "false",
            "blocker": "no extraction formula from metric/vector potential coefficients to alpha3_q",
            "next_action": "source PPN convention/extraction formula before W_q_alpha3 can be computed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "hunt_id": "OSH752_4_product_evaluator",
            "operator_piece": "alpha3 product scoring",
            "local_candidate": str(RESIDUALS / "P8_ALPHA3_BOUND_PRODUCT_EVALUATION.csv"),
            "what_it_provides": "no-cancellation scoring policy and failure mode",
            "claim_grade": "false",
            "blocker": "product inputs are missing numeric/theorem-zero values",
            "next_action": "do not run evaluator until W_q_alpha3 and f_qV are sourced",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "hunt_id": "OSH752_5_verdict",
            "operator_piece": "P_alpha3_min executable chain",
            "local_candidate": "local_source_hunt",
            "what_it_provides": "partial schemas and guards only",
            "claim_grade": "false",
            "blocker": "P_flux, G_PPN, Pi_alpha3^PPN, and q_loc component input remain missing",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def operator_piece_status_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "piece_id": "OPS752_0_P_Hodge",
            "operator_piece": "P_Hodge",
            "status_after_752": "schema_ready_not_executable",
            "minimum_claim_input": "real q_loc component file plus frame/boundary data",
            "can_compute_now": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "piece_id": "OPS752_1_P_flux",
            "operator_piece": "P_flux",
            "status_after_752": "missing",
            "minimum_claim_input": "sourced momentum/preferred-frame flux projector",
            "can_compute_now": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "piece_id": "OPS752_2_G_PPN",
            "operator_piece": "G_PPN",
            "status_after_752": "missing",
            "minimum_claim_input": "gauge-fixed weak-field Green map from q_loc source to delta g_0i",
            "can_compute_now": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "piece_id": "OPS752_3_Pi_alpha3",
            "operator_piece": "Pi_alpha3^PPN",
            "status_after_752": "missing",
            "minimum_claim_input": "PPN extraction convention from delta g_0i/vector momentum terms to alpha3",
            "can_compute_now": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "piece_id": "OPS752_4_W_q_alpha3",
            "operator_piece": "W_q_alpha3",
            "status_after_752": "not_computed",
            "minimum_claim_input": "all operator pieces plus same-frame component norm",
            "can_compute_now": "false",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def template_dryrun_rows(generated_utc: str) -> list[dict[str, Any]]:
    template_exists = BUILDER_TEMPLATE.exists()
    candidate_exists = COMPONENT_INPUT_CANDIDATE.exists()
    template_rows = read_csv_rows(BUILDER_TEMPLATE)
    has_missing = bool(template_rows) and any("MISSING_" in str(value) for value in template_rows[0].values())
    return [
        {
            "dryrun_id": "QTD752_0_builder_template_exists",
            "check": "751 builder template exists",
            "target": str(BUILDER_TEMPLATE),
            "result": "pass" if template_exists else "fail",
            "detail": "template present" if template_exists else "template missing",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "QTD752_1_template_has_missing_markers",
            "check": "template row remains non-data",
            "target": str(BUILDER_TEMPLATE),
            "result": "pass" if has_missing else "fail",
            "detail": "MISSING_* markers present; template cannot be scored",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "QTD752_2_candidate_input_exists",
            "check": "real candidate q_loc component input exists",
            "target": str(COMPONENT_INPUT_CANDIDATE),
            "result": "pass" if candidate_exists else "blocked",
            "detail": "candidate exists" if candidate_exists else "candidate input absent; no component/Hodge run",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "QTD752_3_operator_chain_executable",
            "check": "P_alpha3_min executable",
            "target": "Pi_alpha3^PPN o G_PPN o P_flux o P_Hodge",
            "result": "blocked",
            "detail": "source hunt did not find executable P_flux/G_PPN/Pi_alpha3 pieces",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def source_requirements_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": "REQ752_0_component_input",
            "needed_source": "real q_loc component input",
            "minimum_contents": "sample/domain, weights, frame, q0..q3, boundary data, source file",
            "current_status": "missing",
            "blocks": "P_Hodge; f_qV",
            "next_action": "supply parent-derived field/profile or keep branch blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement_id": "REQ752_1_flux_projector",
            "needed_source": "P_flux",
            "minimum_contents": "map from q_loc vector/harmonic/boundary component to epsilon_q_momentum",
            "current_status": "missing",
            "blocks": "f_qV; W_q_alpha3 product",
            "next_action": "derive from Noether/momentum map or source a weak-field projector",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement_id": "REQ752_2_green_operator",
            "needed_source": "G_PPN",
            "minimum_contents": "gauge-fixed linearized response from q_loc source to g_0i",
            "current_status": "missing",
            "blocks": "W_q_alpha3",
            "next_action": "derive local weak-field equations or source a PPN-normalized response map",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "requirement_id": "REQ752_3_ppn_projection",
            "needed_source": "Pi_alpha3^PPN",
            "minimum_contents": "formula extracting alpha3 from g_0i/vector/self-acceleration terms",
            "current_status": "missing",
            "blocks": "alpha3_q; W_q_alpha3",
            "next_action": "source PPN convention and encode as response projector",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def product_status_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "product_id": "QAP752_0_q_proxy",
            "quantity": "q_proxy",
            "value": f"{Q_PROXY:.15g}",
            "status": "known_scalar_proxy_only",
            "claim_gate": "not component-resolved and not alpha3 score",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "product_id": "QAP752_1_f_qV",
            "quantity": "f_qV",
            "value": "MISSING_COMPONENT_INPUT_AND_PFLUX",
            "status": "missing",
            "claim_gate": "must be theorem-zero or sourced numeric",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "product_id": "QAP752_2_W_q_alpha3",
            "quantity": "W_q_alpha3",
            "value": "MISSING_GPPN_AND_PI_ALPHA3",
            "status": "missing",
            "claim_gate": "must be derived/bounded before score",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "product_id": "QAP752_3_gate",
            "quantity": "abs(W_q_alpha3*f_qV)",
            "value": f"must_be <= {WF_LIMIT:.15g}",
            "status": "not_scoreable",
            "claim_gate": "requires both product factors or exact zero theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D752_0_source_hunt",
            "decision": "local Palpha3 operator source hunt fails for executable chain",
            "meaning": "schemas exist, but P_flux/G_PPN/Pi_alpha3^PPN are not sourced as executable maps",
            "claim_status": "operator_source_missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D752_1_template_dryrun",
            "decision": "q_loc template dry-run blocks",
            "meaning": "the builder template still has MISSING_* markers and no real candidate input file",
            "claim_status": "input_missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D752_2_no_score",
            "decision": "do not run alpha3 evaluator",
            "meaning": "f_qV and W_q_alpha3 are both missing, so any numeric score would be fake",
            "claim_status": "no_alpha3_score",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D752_3_next",
            "decision": "build a sourced Palpha3 pack or derive parent zero theorem",
            "meaning": "the next useful progress is either external/parent source for operator pieces or a theorem killing the channel",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def y5_update_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "Y5R752_alpha3_q_loc",
            "source_row": "R7_alpha3/q_loc",
            "status_after_752": "operator_source_hunt_failed_no_score",
            "zero_or_input": f"need theorem-zero or abs(W_q_alpha3*f_qV)<={WF_LIMIT:.15g}",
            "still_missing": "P_flux; G_PPN; Pi_alpha3^PPN; q_loc component input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R752_component_template",
            "source_row": "QIB751_TEMPLATE_ROW_DO_NOT_SCORE",
            "status_after_752": "template_validated_as_nondata",
            "zero_or_input": "real component input file required",
            "still_missing": str(COMPONENT_INPUT_CANDIDATE),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R752_PPN_R11",
            "source_row": "PPN524_5/R11 vector",
            "status_after_752": "not_promoted",
            "zero_or_input": "PPN/R11 source pieces remain templates or missing",
            "still_missing": "PPN alpha3 extraction, weak-field map, vector coefficient/source path",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU752_0_allowed",
            "allowed_after_752": "say local source hunt did not find executable Palpha3 chain",
            "forbidden_after_752": "say Palpha3/W_q_alpha3 is sourced",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU752_1_allowed",
            "allowed_after_752": "use template dry-run as a blocker proof",
            "forbidden_after_752": "treat missing-marker template as data",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU752_2_allowed",
            "allowed_after_752": "source PPN/operator pieces or derive parent zero theorem next",
            "forbidden_after_752": "run alpha3 evaluator with missing products",
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
            "main_result": "local Palpha3 source hunt found no executable operator chain; q_loc template dry-run blocked as intended",
            "hard_blocker": "P_flux, G_PPN, Pi_alpha3^PPN, and real q_loc component input remain missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def make_validation(
    sources: list[dict[str, Any]],
    hunt: list[dict[str, Any]],
    status: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    product_status: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    outputs: list[Path],
) -> list[dict[str, str]]:
    prior = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_751_VALIDATION.csv")
    all_rows = hunt + status + dryrun + requirements + product_status + decisions + y5_update + routes
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V752_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V752_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all source files contain expected evidence needles"})
    validation.append({"check_id": "V752_2_prior_751_clean", "result": "pass" if prior and all(row.get("result") == "pass" for row in prior) else "fail", "detail": "751 validation has no failures"})
    validation.append({"check_id": "V752_3_operator_hunt_failed_cleanly", "result": "pass" if any(row["hunt_id"] == "OSH752_5_verdict" and row["claim_grade"] == "false" for row in hunt) else "fail", "detail": "no executable Palpha3 chain found"})
    validation.append({"check_id": "V752_4_core_pieces_missing", "result": "pass" if all(row["can_compute_now"] == "false" for row in status) else "fail", "detail": "operator pieces cannot compute now"})
    validation.append({"check_id": "V752_5_template_dryrun_blocks", "result": "pass" if any(row["dryrun_id"] == "QTD752_2_candidate_input_exists" and row["result"] == "blocked" for row in dryrun) else "fail", "detail": "candidate input absent"})
    validation.append({"check_id": "V752_6_template_has_missing_markers", "result": "pass" if any(row["dryrun_id"] == "QTD752_1_template_has_missing_markers" and row["result"] == "pass" for row in dryrun) else "fail", "detail": "template remains nondata"})
    validation.append({"check_id": "V752_7_requirements_queue_written", "result": "pass" if len(requirements) == 4 and all(row["current_status"] == "missing" for row in requirements) else "fail", "detail": "four missing source requirements queued"})
    validation.append({"check_id": "V752_8_product_not_scoreable", "result": "pass" if any(row["product_id"] == "QAP752_3_gate" and row["status"] == "not_scoreable" for row in product_status) else "fail", "detail": "alpha3 product remains blocked"})
    validation.append({"check_id": "V752_9_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_rows) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V752_10_no_local_arena_claim", "result": "pass" if "no_fqV_no_Wqalpha3_no_alpha3_PPN_R10_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "alpha3/PPN/R10/Newton/local-GR claims remain blocked"})
    validation.append({"check_id": "V752_11_next_target_selected", "result": "pass" if all(row.get("next_target") == NEXT_TARGET for row in decisions) else "fail", "detail": NEXT_TARGET})
    validation.append({"check_id": "V752_12_outputs_scoped", "result": "pass" if all(under_post(path) for path in outputs) else "fail", "detail": "all outputs under post-checkpoint-work"})
    changed = formalization_changed_after_cutoff()
    validation.append({"check_id": "V752_13_formalization_workbench_untouched", "result": "pass" if changed == 0 else "fail", "detail": f"formalization_changed_after_cutoff={changed}"})
    validation.append({"check_id": "V752_14_y5_rows_retained", "result": "pass" if {"Y5R752_alpha3_q_loc", "Y5R752_component_template", "Y5R752_PPN_R11"}.issubset({row["runner_id"] for row in y5_update}) else "fail", "detail": "alpha3/template/PPN-R11 rows retained"})
    validation.append({"check_id": "V752_15_route_forbids_missing_product_eval", "result": "pass" if any("missing products" in row["forbidden_after_752"] for row in routes) else "fail", "detail": "do not run evaluator with missing products"})
    validation.append({"check_id": "V752_16_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    hunt: list[dict[str, Any]],
    status: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    product_status: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 752 - Y5 R10 Palpha3 Operator Source Hunt Or q_loc Template Dryrun

Start point: 751 defined the minimal response chain:

```text
P_alpha3_min := Pi_alpha3^PPN o G_PPN o P_flux o P_Hodge
```

Current result: **the local source hunt does not find an executable `P_alpha3` chain**. The corpus has useful schemas, PPN row contracts, and alpha3 product policies, but not claim-grade sources for `P_flux`, `G_PPN`, or `Pi_alpha3^PPN`. The q_loc template dry-run also blocks correctly: the only available component builder row is a `MISSING_*` template, not data.

So there is no `W_q_alpha3`, no `f_qV`, and no alpha3 score.

## Summary

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | local Palpha3 source hunt failed; q_loc template dry-run blocked |
| Next target | `{NEXT_TARGET}` |

## Palpha3 Operator Source Hunt

{markdown_table(hunt, ["hunt_id", "operator_piece", "local_candidate", "what_it_provides", "claim_grade", "blocker", "next_action", "valid_for_claim"])}

## Operator Piece Status

{markdown_table(status, ["piece_id", "operator_piece", "status_after_752", "minimum_claim_input", "can_compute_now", "valid_for_claim"])}

## q_loc Template Dry-Run

{markdown_table(dryrun, ["dryrun_id", "check", "target", "result", "detail", "valid_for_claim"])}

## Source Requirements Queue

{markdown_table(requirements, ["requirement_id", "needed_source", "minimum_contents", "current_status", "blocks", "next_action", "valid_for_claim"])}

## q_loc Alpha3 Product Status

{markdown_table(product_status, ["product_id", "quantity", "value", "status", "claim_gate", "valid_for_claim"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Y5 Runner Update

{markdown_table(y5_update, ["runner_id", "source_row", "status_after_752", "zero_or_input", "still_missing", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_752", "forbidden_after_752", "next_action", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This checkpoint closes a loophole: we cannot pretend the operator is sourced just because the symbolic chain exists. Locally, `P_alpha3_min` is still a contract, not a calculator. The next real fork is either source the PPN/operator pieces properly, or try for a parent zero theorem that kills the q_loc alpha3 channel before the operator is needed.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    hunt = operator_source_hunt_rows(generated_utc)
    status = operator_piece_status_rows(generated_utc)
    dryrun = template_dryrun_rows(generated_utc)
    requirements = source_requirements_rows(generated_utc)
    product_status = product_status_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    y5_update = y5_update_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)

    outputs = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        OPERATOR_SOURCE_HUNT_PATH,
        OPERATOR_PIECE_STATUS_PATH,
        TEMPLATE_DRYRUN_PATH,
        SOURCE_REQUIREMENTS_PATH,
        PRODUCT_STATUS_PATH,
        DECISION_PATH,
        Y5_UPDATE_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]

    validation = make_validation(
        sources,
        hunt,
        status,
        dryrun,
        requirements,
        product_status,
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
        OPERATOR_SOURCE_HUNT_PATH,
        hunt,
        ["hunt_id", "operator_piece", "local_candidate", "what_it_provides", "claim_grade", "blocker", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OPERATOR_PIECE_STATUS_PATH,
        status,
        ["piece_id", "operator_piece", "status_after_752", "minimum_claim_input", "can_compute_now", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        TEMPLATE_DRYRUN_PATH,
        dryrun,
        ["dryrun_id", "check", "target", "result", "detail", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SOURCE_REQUIREMENTS_PATH,
        requirements,
        ["requirement_id", "needed_source", "minimum_contents", "current_status", "blocks", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        PRODUCT_STATUS_PATH,
        product_status,
        ["product_id", "quantity", "value", "status", "claim_gate", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        DECISION_PATH,
        decisions,
        ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        Y5_UPDATE_PATH,
        y5_update,
        ["runner_id", "source_row", "status_after_752", "zero_or_input", "still_missing", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        ROUTE_PATH,
        routes,
        ["route_id", "allowed_after_752", "forbidden_after_752", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SUMMARY_PATH,
        summary,
        ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, hunt, status, dryrun, requirements, product_status, decisions, y5_update, routes, validation)

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"752 validation failed: {failed}")
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")


if __name__ == "__main__":
    main()

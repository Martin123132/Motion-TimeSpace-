from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "750-Y5-R10-q_loc-Hodge-component-field-source-acquisition-or-alpha3-response-runner.md"
NEXT_TARGET = "751-Y5-R10-minimal-Palpha3-response-operator-or-q_loc-component-input-builder.md"
STATUS = "Y5_R10_750_no_claim_valid_q_loc_component_field_found_acquisition_schema_and_response_runner_contract_written_nonclaim"
CLAIM_CEILING = "q_loc_component_source_acquisition_and_runner_schema_only_no_fqV_no_Wqalpha3_no_alpha3_PPN_R10_Newton_or_local_GR_pass"
Q_PROXY = 7.432631961576971e-06
ALPHA3_BOUND = 4.0e-20
WF_LIMIT = ALPHA3_BOUND / Q_PROXY
UNIT_RATIO = Q_PROXY / ALPHA3_BOUND
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_750_SOURCE_REGISTER.csv"
ACQUISITION_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_750_QLOC_COMPONENT_SOURCE_ACQUISITION_LEDGER.csv"
INPUT_SCHEMA_PATH = RESIDUALS / "P8_Y5_R10_750_QLOC_COMPONENT_INPUT_SCHEMA.csv"
HODGE_RUNNER_SCHEMA_PATH = RESIDUALS / "P8_Y5_R10_750_HODGE_COMPONENT_RUNNER_SCHEMA.csv"
ALPHA3_RUNNER_SCHEMA_PATH = RESIDUALS / "P8_Y5_R10_750_ALPHA3_RESPONSE_RUNNER_SCHEMA.csv"
DRYRUN_STATUS_PATH = RESIDUALS / "P8_Y5_R10_750_DRYRUN_STATUS.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_750_DECISION_MATRIX.csv"
Y5_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_750_Y5_RUNNER_UPDATE.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_750_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_750_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_750_VALIDATION.csv"

COMPONENT_INPUT_CANDIDATE = RESIDUALS / "P8_Y5_R10_750_QLOC_COMPONENT_INPUT_CANDIDATE.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "749_doc": {
        "path": POST_CHECKPOINT / "749-Y5-R10-q_loc-vector-component-decomposition-or-alpha3-response-operator-fill.md",
        "needles": [
            "q_loc component decomposition can be stated exactly",
            "750-Y5-R10-q_loc-Hodge-component-field-source-acquisition-or-alpha3-response-runner.md",
            "scalar max-proxy",
        ],
        "role": "immediate 750 handoff",
    },
    "749_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_749_VALIDATION.csv",
        "needles": ["V749_15_validation_rows_ready", "V749_12_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "749_decomposition": {
        "path": RESIDUALS / "P8_Y5_R10_749_QLOC_COMPONENT_DECOMPOSITION_CONTRACT.csv",
        "needles": ["QCD749_7_verdict", "decomposition_not_filled_current_corpus"],
        "role": "component decomposition blocker",
    },
    "749_response": {
        "path": RESIDUALS / "P8_Y5_R10_749_ALPHA3_RESPONSE_OPERATOR_CONTRACT.csv",
        "needles": ["A3R749_2_weight_definition", "contract_written_no_value"],
        "role": "alpha3 response operator blocker",
    },
    "749_product": {
        "path": RESIDUALS / "P8_Y5_R10_749_WQFQV_PRODUCT_STATUS.csv",
        "needles": ["WFP749_1_vector_fraction", "MISSING_QLOC_HODGE_COMPONENTS"],
        "role": "missing f_qV/W product status",
    },
    "q_loc_bound_spec": {
        "path": RESIDUALS / "P8_QLOC_BOUND_RUNNER_SPEC.csv",
        "needles": ["QB516_0_compact_shell_budget", "map this dimensionless proxy"],
        "role": "old q_loc bound runner spec",
    },
    "q_loc_trigger": {
        "path": RESIDUALS / "P8_QLOC_BOUND_TRIGGER_LEDGER.csv",
        "needles": ["BT517_0_owner_match_fails", "run q_loc residual-bound branch"],
        "role": "q_loc bound trigger ledger",
    },
    "734_runner": {
        "path": RESIDUALS / "P8_Y5_R10_734_HYBRID_QLOC_RESIDUAL_RUNNER_FILLED.csv",
        "needles": ["HQR734_0_compact_shell_budget", "not_scoreable"],
        "role": "hybrid q_loc runner filled status",
    },
    "740_first_bound": {
        "path": RESIDUALS / "P8_Y5_R10_740_FIRST_QLOC_BOUND_ATTEMPT.csv",
        "needles": ["QBA740_0_compact_shell_proxy", "source_backed_proxy_not_arena_bound"],
        "role": "q_proxy source-backed but not arena-bound",
    },
    "740_observable_transfer": {
        "path": RESIDUALS / "P8_Y5_R10_740_QLOC_OBSERVABLE_TRANSFER_MAP.csv",
        "needles": ["QOT740_3_PPN_vector", "weak-field Green operator"],
        "role": "observable transfer missing weak-field map",
    },
    "742_free_pack": {
        "path": RESIDUALS / "P8_Y5_R10_742_QLOC_FREE_COEFFICIENT_PACK.csv",
        "needles": ["QFC742_3_PPN_vector", "activated_template_not_filled"],
        "role": "q_loc free coefficient pack",
    },
    "743_coeff_attempt": {
        "path": RESIDUALS / "P8_Y5_R10_743_QLOC_COEFFICIENT_ROW_ATTEMPT.csv",
        "needles": ["QCR743_4_c_q_PPN_vector", "blocked_not_filled"],
        "role": "q_loc coefficient attempt blocker",
    },
    "746_projection_contract": {
        "path": RESIDUALS / "P8_Y5_R10_746_QLOC_PROJECTION_CONTRACT.csv",
        "needles": ["QPC746_0_decompose_q_loc", "contract_written_components_unfilled"],
        "role": "q_loc projection contract",
    },
    "747_pressure": {
        "path": RESIDUALS / "P8_Y5_R10_747_WQALPHA3_COEFFICIENT_PRESSURE.csv",
        "needles": ["WQA747_0_product_definition", "definition_written_not_filled"],
        "role": "alpha3 product pressure",
    },
    "748_template": {
        "path": RESIDUALS / "P8_Y5_R10_748_WQALPHA3_SOURCE_ROW_TEMPLATE.csv",
        "needles": ["WQS748_0_q_vector_fraction", "MISSING_QLOC_VECTOR_DECOMPOSITION"],
        "role": "Wqalpha3 source row template",
    },
    "u2_bound": {
        "path": RESIDUALS / "P8_Y5_QLOC_U2_BOUND.csv",
        "needles": ["QBU526_3_required_source_path", "MISSING_PROFILE_OR_WARD_ZERO"],
        "role": "older q_loc profile missing row",
    },
    "597_runner_queue": {
        "path": RESIDUALS / "P8_Y5_R10_597_QLOC_RESIDUAL_RUNNER_INPUT_QUEUE.csv",
        "needles": ["QRR597_3_PPN_metric_tail", "weak-field map not filled"],
        "role": "older q_loc residual runner queue",
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


def acquisition_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "QSA750_0_bound_runner_spec",
            "candidate_file": str(RESIDUALS / "P8_QLOC_BOUND_RUNNER_SPEC.csv"),
            "evidence_found": "compact-shell proxy and arena triggers",
            "provides_q_loc_field": "false",
            "provides_frame": "false",
            "provides_boundary_conditions": "false",
            "provides_component_norm": "false",
            "claim_status": "proxy_only",
            "next_action": "use as provenance for q_proxy only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "QSA750_1_hybrid_runner_filled",
            "candidate_file": str(RESIDUALS / "P8_Y5_R10_734_HYBRID_QLOC_RESIDUAL_RUNNER_FILLED.csv"),
            "evidence_found": "q_proxy status plus channel blockers",
            "provides_q_loc_field": "false",
            "provides_frame": "false",
            "provides_boundary_conditions": "false",
            "provides_component_norm": "false",
            "claim_status": "not_scoreable",
            "next_action": "promote only after field/profile and weak-field maps are supplied",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "QSA750_2_first_bound_attempt",
            "candidate_file": str(RESIDUALS / "P8_Y5_R10_740_FIRST_QLOC_BOUND_ATTEMPT.csv"),
            "evidence_found": f"q_proxy={Q_PROXY:.15g}",
            "provides_q_loc_field": "false",
            "provides_frame": "false",
            "provides_boundary_conditions": "false",
            "provides_component_norm": "false",
            "claim_status": "source_backed_scalar_proxy_not_arena_bound",
            "next_action": "do not infer f_qV or alpha3 from this row",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "QSA750_3_u2_bound_profile_row",
            "candidate_file": str(RESIDUALS / "P8_Y5_QLOC_U2_BOUND.csv"),
            "evidence_found": "explicit MISSING_PROFILE_OR_WARD_ZERO row",
            "provides_q_loc_field": "false",
            "provides_frame": "false",
            "provides_boundary_conditions": "false",
            "provides_component_norm": "false",
            "claim_status": "profile_missing",
            "next_action": "fill q_loc profile or derive Ward zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "QSA750_4_749_component_contract",
            "candidate_file": str(RESIDUALS / "P8_Y5_R10_749_QLOC_COMPONENT_DECOMPOSITION_CONTRACT.csv"),
            "evidence_found": "Hodge/Helmholtz contract and f_qV definition",
            "provides_q_loc_field": "false",
            "provides_frame": "schema_only",
            "provides_boundary_conditions": "schema_only",
            "provides_component_norm": "schema_only",
            "claim_status": "contract_only",
            "next_action": "turn into input schema and runner validation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "QSA750_5_verdict",
            "candidate_file": "scan_over_q_loc_ledgers",
            "evidence_found": "no claim-valid component-resolved q_loc field/profile found",
            "provides_q_loc_field": "false",
            "provides_frame": "false",
            "provides_boundary_conditions": "false",
            "provides_component_norm": "false",
            "claim_status": "component_source_absent_current_corpus",
            "next_action": "write acquisition schema and alpha3-response runner contract",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def input_schema_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "field_id": "QIN750_0_sample_identity",
            "required_column": "sample_id; domain_id",
            "meaning": "stable row identity and compact-local domain/shell label",
            "units_or_type": "string",
            "required_for": "traceability and boundary grouping",
            "status": "schema_written_no_input_file",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field_id": "QIN750_1_weight_measure",
            "required_column": "weight_dV",
            "meaning": "integration measure or quadrature weight on the local slice/domain",
            "units_or_type": "volume or normalized dimensionless weight with declared convention",
            "required_for": "component norms and f_qV denominator",
            "status": "schema_written_no_input_file",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field_id": "QIN750_2_observed_frame",
            "required_column": "u0;u1;u2;u3 or frame_is_local_orthonormal=true",
            "meaning": "observed time direction used to split q_T and q_perp",
            "units_or_type": "dimensionless normalized frame",
            "required_for": "temporal/spatial split",
            "status": "schema_written_no_input_file",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field_id": "QIN750_3_q_loc_components",
            "required_column": "q0;q1;q2;q3 or q_T;q_x;q_y;q_z in declared frame",
            "meaning": "component-resolved q_loc field/profile, not just max scalar proxy",
            "units_or_type": "declared q_loc units or dimensionless normalized field",
            "required_for": "all component fractions",
            "status": "schema_written_no_input_file",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field_id": "QIN750_4_boundary_conditions",
            "required_column": "boundary_tag; boundary_condition; neighbor/topology metadata",
            "meaning": "data needed for Hodge/Helmholtz gradient/transverse/harmonic split",
            "units_or_type": "categorical plus mesh/adjacency reference",
            "required_for": "q_V versus q_H separation",
            "status": "schema_written_no_input_file",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "field_id": "QIN750_5_alpha3_projection",
            "required_column": "P_alpha3_x;P_alpha3_y;P_alpha3_z or response_operator_id",
            "meaning": "projection onto momentum/preferred-frame component or a sourced response operator",
            "units_or_type": "dimensionless projector/operator reference",
            "required_for": "f_qV and W_q_alpha3 product",
            "status": "schema_written_no_input_file",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def hodge_runner_schema_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "step_id": "HRS750_0_validate_input",
            "runner_step": "validate required columns and units",
            "formula_or_check": "input has sample/domain, measure, frame, q_loc components, boundary metadata",
            "output": "schema_pass=false until candidate input exists",
            "claim_status": "dry_run_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "HRS750_1_frame_split",
            "runner_step": "compute q_T and q_perp",
            "formula_or_check": "q_T=-u.q; q_perp=h q",
            "output": "temporal and spatial norms by domain",
            "claim_status": "blocked_no_input_field",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "HRS750_2_Hodge_split",
            "runner_step": "split q_perp into gradient, transverse, and harmonic/boundary pieces",
            "formula_or_check": "q_perp^i = D^i sigma_q + q_V^i + q_H^i with declared boundary conditions",
            "output": "norm_gradient, norm_transverse, norm_harmonic",
            "claim_status": "blocked_no_mesh_or_boundary_operator",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "HRS750_3_fqV",
            "runner_step": "compute alpha3 momentum fraction",
            "formula_or_check": "f_qV = ||P_alpha3 q_loc||_A / q_proxy",
            "output": "f_qV with source path and denominator check",
            "claim_status": "blocked_no_Palpha3_or_q_field",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "HRS750_4_acceptance",
            "runner_step": "only output claim-ready row if zero theorem or numeric product exists",
            "formula_or_check": f"abs(W_q_alpha3*f_qV) <= {WF_LIMIT:.15g}",
            "output": "nonclaim until W and f are both sourced",
            "claim_status": "guard_active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def alpha3_runner_schema_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "step_id": "A3S750_0_operator_input",
            "runner_step": "load gauge-fixed linearized weak-field operator",
            "required_input": "G_PPN_mn[source] with source-normalization convention",
            "current_status": "missing",
            "output_if_supplied": "metric response delta g_mn",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "A3S750_1_flux_projector",
            "runner_step": "load P_flux/P_alpha3 source projection",
            "required_input": "map from q_loc vector/flux component into g0i preferred-frame sector",
            "current_status": "missing",
            "output_if_supplied": "epsilon_q_momentum",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "A3S750_2_alpha3_projector",
            "runner_step": "load PPN alpha3 extraction convention",
            "required_input": "official PPN alpha3 normalization, frame/velocity convention, sign",
            "current_status": "missing",
            "output_if_supplied": "alpha3_q",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "A3S750_3_response_weight",
            "runner_step": "compute W_q_alpha3",
            "required_input": "alpha3_q and epsilon_q_momentum with same norm/source frame",
            "current_status": "contract_only",
            "output_if_supplied": "W_q_alpha3 := alpha3_q/epsilon_q_momentum",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "step_id": "A3S750_4_score",
            "runner_step": "score product with no-cancellation guard",
            "required_input": f"f_qV, W_q_alpha3, q_proxy={Q_PROXY:.15g}",
            "current_status": "not_runnable",
            "output_if_supplied": f"pass only if abs(W_q_alpha3*f_qV) <= {WF_LIMIT:.15g} or theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def dryrun_rows(generated_utc: str) -> list[dict[str, Any]]:
    exists = COMPONENT_INPUT_CANDIDATE.exists()
    return [
        {
            "dryrun_id": "DRY750_0_candidate_input_file",
            "check": "candidate component input file exists",
            "target": str(COMPONENT_INPUT_CANDIDATE),
            "result": "pass" if exists else "blocked",
            "detail": "input exists" if exists else "no candidate q_loc component field file found; dry-run stops before computation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "DRY750_1_no_long_run",
            "check": "no heavy computation started",
            "target": "Hodge/alpha3 runner",
            "result": "pass",
            "detail": "schema/dry-run only; no long computation and no token-wasting wait",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "dryrun_id": "DRY750_2_claim_guard",
            "check": "no claim without component field plus response operator",
            "target": "R7_alpha3/q_loc",
            "result": "pass",
            "detail": "f_qV and W_q_alpha3 both missing; product not scored",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D750_0_source_acquisition",
            "decision": "no claim-valid q_loc component field found",
            "meaning": "the corpus has q_proxy and contracts, not a local vector/profile with frame and boundary data",
            "claim_status": "source_absent",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D750_1_runner_schema",
            "decision": "write Hodge component input and runner schema",
            "meaning": "future data can be validated before any expensive computation",
            "claim_status": "schema_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D750_2_alpha3_response",
            "decision": "write alpha3 response runner contract",
            "meaning": "W_q_alpha3 remains an operator output, not a guessed coefficient",
            "claim_status": "operator_missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D750_3_next",
            "decision": "derive minimal P_alpha3 response operator or build candidate q_loc input",
            "meaning": "next work should fill one side of the product instead of adding another scalar smoke row",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def y5_update_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "Y5R750_alpha3_q_loc",
            "source_row": "R7_alpha3/q_loc",
            "status_after_750": "blocked_waiting_for_component_field_or_response_operator",
            "zero_or_input": f"need P_alpha3 q_loc=0 or abs(W_q_alpha3 f_qV)<= {WF_LIMIT:.15g}",
            "still_missing": "q_loc component input; P_alpha3/P_flux; W_q_alpha3 response operator",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R750_component_runner",
            "source_row": "q_loc Hodge component runner",
            "status_after_750": "schema_ready_dryrun_blocked_no_input",
            "zero_or_input": "component field/profile with frame and boundary data",
            "still_missing": str(COMPONENT_INPUT_CANDIDATE),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R750_PPN_R10",
            "source_row": "PPN/R10 component maps",
            "status_after_750": "not_promoted",
            "zero_or_input": "PPN response operator and R10 range kernel remain separate missing maps",
            "still_missing": "G_PPN, PPN alpha3 convention, lambda/alpha(lambda) kernel",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU750_0_allowed",
            "allowed_after_750": "say no component-resolved q_loc field was found",
            "forbidden_after_750": "treat q_proxy as component-resolved data",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU750_1_allowed",
            "allowed_after_750": "build a candidate input file only if real q_loc components/frame/boundary data exist",
            "forbidden_after_750": "fabricate q_loc samples from the scalar max proxy",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU750_2_allowed",
            "allowed_after_750": "derive P_alpha3/G_PPN response operator as an alternative route",
            "forbidden_after_750": "choose W_q_alpha3 after seeing the alpha3 bound",
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
            "main_result": "no claim-valid q_loc component field found; acquisition and alpha3 response runner schemas written",
            "hard_blocker": "f_qV and W_q_alpha3 remain missing; q_proxy is only scalar proxy provenance",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def make_validation(
    sources: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    input_schema: list[dict[str, Any]],
    hodge_schema: list[dict[str, Any]],
    alpha3_schema: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    outputs: list[Path],
) -> list[dict[str, str]]:
    prior = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_749_VALIDATION.csv")
    all_rows = acquisition + input_schema + hodge_schema + alpha3_schema + dryrun + decisions + y5_update + routes
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V750_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V750_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all source files contain expected evidence needles"})
    validation.append({"check_id": "V750_2_prior_749_clean", "result": "pass" if prior and all(row.get("result") == "pass" for row in prior) else "fail", "detail": "749 validation has no failures"})
    validation.append({"check_id": "V750_3_no_component_source_found", "result": "pass" if any(row["claim_status"] == "component_source_absent_current_corpus" for row in acquisition) else "fail", "detail": "component-resolved q_loc field absent"})
    validation.append({"check_id": "V750_4_qproxy_not_promoted", "result": "pass" if any(row["claim_status"] == "source_backed_scalar_proxy_not_arena_bound" for row in acquisition) else "fail", "detail": "q_proxy stays scalar proxy provenance"})
    validation.append({"check_id": "V750_5_input_schema_written", "result": "pass" if len(input_schema) >= 6 else "fail", "detail": "minimum component input columns declared"})
    validation.append({"check_id": "V750_6_hodge_runner_schema_written", "result": "pass" if any(row["step_id"] == "HRS750_3_fqV" for row in hodge_schema) else "fail", "detail": "f_qV runner step declared"})
    validation.append({"check_id": "V750_7_alpha3_runner_schema_written", "result": "pass" if any(row["step_id"] == "A3S750_3_response_weight" for row in alpha3_schema) else "fail", "detail": "W_q_alpha3 runner step declared"})
    validation.append({"check_id": "V750_8_dryrun_blocks_without_input", "result": "pass" if any(row["dryrun_id"] == "DRY750_0_candidate_input_file" and row["result"] == "blocked" for row in dryrun) else "fail", "detail": "dry-run stops before computation if no input file"})
    validation.append({"check_id": "V750_9_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_rows) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V750_10_no_local_arena_claim", "result": "pass" if "no_fqV_no_Wqalpha3_no_alpha3_PPN_R10_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "alpha3/PPN/R10/Newton/local-GR claims remain blocked"})
    validation.append({"check_id": "V750_11_next_target_selected", "result": "pass" if all(row.get("next_target") == NEXT_TARGET for row in decisions) else "fail", "detail": NEXT_TARGET})
    validation.append({"check_id": "V750_12_outputs_scoped", "result": "pass" if all(under_post(path) for path in outputs) else "fail", "detail": "all outputs under post-checkpoint-work"})
    changed = formalization_changed_after_cutoff()
    validation.append({"check_id": "V750_13_formalization_workbench_untouched", "result": "pass" if changed == 0 else "fail", "detail": f"formalization_changed_after_cutoff={changed}"})
    validation.append({"check_id": "V750_14_y5_rows_retained", "result": "pass" if {"Y5R750_alpha3_q_loc", "Y5R750_component_runner", "Y5R750_PPN_R10"}.issubset({row["runner_id"] for row in y5_update}) else "fail", "detail": "alpha3/component/PPN-R10 rows retained"})
    validation.append({"check_id": "V750_15_route_forbids_fabrication", "result": "pass" if any("fabricate q_loc samples" in row["forbidden_after_750"] for row in routes) else "fail", "detail": "no fabricated q_loc samples from proxy"})
    validation.append({"check_id": "V750_16_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    acquisition: list[dict[str, Any]],
    input_schema: list[dict[str, Any]],
    hodge_schema: list[dict[str, Any]],
    alpha3_schema: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 750 - Y5 R10 q_loc Hodge Component Field Source Acquisition Or alpha3 Response Runner

Start point: 749 proved the important bookkeeping point: `q_proxy = {Q_PROXY:.15g}` is a scalar max-proxy, not `f_qV`, not `W_q_alpha3`, and not an alpha3 score.

Current result: **no claim-valid component-resolved q_loc field/profile exists in the current corpus**. The scan found proxy provenance and runner contracts, but no local vector field with observed frame, domain/boundary data, component norm, and alpha3 projection.

So 750 writes the next executable contract instead of pretending to run a number:

```text
input needed: q_loc components + observed frame + domain weights + boundary data + P_alpha3/response operator
runner output: f_qV and/or W_q_alpha3
claim gate: |W_q_alpha3 f_qV| <= {WF_LIMIT:.15g}, or theorem-zero
```

This remains private/nonclaim.

## Summary

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | no component field found; acquisition schema and alpha3 response runner contract written |
| Next target | `{NEXT_TARGET}` |

## q_loc Component Source Acquisition Ledger

{markdown_table(acquisition, ["candidate_id", "candidate_file", "evidence_found", "provides_q_loc_field", "provides_frame", "provides_boundary_conditions", "provides_component_norm", "claim_status", "next_action", "valid_for_claim"])}

## q_loc Component Input Schema

{markdown_table(input_schema, ["field_id", "required_column", "meaning", "units_or_type", "required_for", "status", "valid_for_claim"])}

## Hodge Component Runner Schema

{markdown_table(hodge_schema, ["step_id", "runner_step", "formula_or_check", "output", "claim_status", "valid_for_claim"])}

## alpha3 Response Runner Schema

{markdown_table(alpha3_schema, ["step_id", "runner_step", "required_input", "current_status", "output_if_supplied", "valid_for_claim"])}

## Dry-Run Status

{markdown_table(dryrun, ["dryrun_id", "check", "target", "result", "detail", "valid_for_claim"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Y5 Runner Update

{markdown_table(y5_update, ["runner_id", "source_row", "status_after_750", "zero_or_input", "still_missing", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_750", "forbidden_after_750", "next_action", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is a clean stop sign, not a crash. We have enough to know what must be measured or derived, but not enough to score the alpha3 branch. The next useful move is to fill one side of the product: either build a real component input file for `q_loc`, or derive the minimal `P_alpha3/G_PPN` response operator. Anything else would be shadow-boxing the scalar proxy.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    acquisition = acquisition_rows(generated_utc)
    input_schema = input_schema_rows(generated_utc)
    hodge_schema = hodge_runner_schema_rows(generated_utc)
    alpha3_schema = alpha3_runner_schema_rows(generated_utc)
    dryrun = dryrun_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    y5_update = y5_update_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)

    outputs = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        ACQUISITION_LEDGER_PATH,
        INPUT_SCHEMA_PATH,
        HODGE_RUNNER_SCHEMA_PATH,
        ALPHA3_RUNNER_SCHEMA_PATH,
        DRYRUN_STATUS_PATH,
        DECISION_PATH,
        Y5_UPDATE_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]

    validation = make_validation(
        sources,
        acquisition,
        input_schema,
        hodge_schema,
        alpha3_schema,
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
        ACQUISITION_LEDGER_PATH,
        acquisition,
        [
            "candidate_id",
            "candidate_file",
            "evidence_found",
            "provides_q_loc_field",
            "provides_frame",
            "provides_boundary_conditions",
            "provides_component_norm",
            "claim_status",
            "next_action",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        INPUT_SCHEMA_PATH,
        input_schema,
        ["field_id", "required_column", "meaning", "units_or_type", "required_for", "status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        HODGE_RUNNER_SCHEMA_PATH,
        hodge_schema,
        ["step_id", "runner_step", "formula_or_check", "output", "claim_status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        ALPHA3_RUNNER_SCHEMA_PATH,
        alpha3_schema,
        ["step_id", "runner_step", "required_input", "current_status", "output_if_supplied", "valid_for_claim", "generated_utc"],
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
        ["runner_id", "source_row", "status_after_750", "zero_or_input", "still_missing", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        ROUTE_PATH,
        routes,
        ["route_id", "allowed_after_750", "forbidden_after_750", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SUMMARY_PATH,
        summary,
        ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, acquisition, input_schema, hodge_schema, alpha3_schema, dryrun, decisions, y5_update, routes, validation)

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"750 validation failed: {failed}")
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "749-Y5-R10-q_loc-vector-component-decomposition-or-alpha3-response-operator-fill.md"
NEXT_TARGET = "750-Y5-R10-q_loc-Hodge-component-field-source-acquisition-or-alpha3-response-runner.md"
STATUS = "Y5_R10_749_q_loc_component_decomposition_contract_written_no_fqV_or_Wqalpha3_fill_nonclaim"
CLAIM_CEILING = "q_loc_component_decomposition_contract_and_alpha3_response_operator_contract_only_no_alpha3_PPN_R10_Newton_or_local_GR_pass"
Q_PROXY = 7.432631961576971e-06
ALPHA3_BOUND = 4.0e-20
WF_LIMIT = ALPHA3_BOUND / Q_PROXY
UNIT_RATIO = Q_PROXY / ALPHA3_BOUND
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_749_SOURCE_REGISTER.csv"
DECOMPOSITION_PATH = RESIDUALS / "P8_Y5_R10_749_QLOC_COMPONENT_DECOMPOSITION_CONTRACT.csv"
RESPONSE_PATH = RESIDUALS / "P8_Y5_R10_749_ALPHA3_RESPONSE_OPERATOR_CONTRACT.csv"
COMPONENT_GATE_PATH = RESIDUALS / "P8_Y5_R10_749_COMPONENT_TO_OBSERVABLE_GATE.csv"
PRODUCT_GATE_PATH = RESIDUALS / "P8_Y5_R10_749_WQFQV_PRODUCT_STATUS.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_749_DECISION_MATRIX.csv"
Y5_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_749_Y5_RUNNER_UPDATE.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_749_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_749_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_749_VALIDATION.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "748_doc": {
        "path": POST_CHECKPOINT / "748-Y5-R10-q_loc-vector-parity-zero-theorem-or-Wqalpha3-source-row.md",
        "needles": [
            "vector parity zero theorem has a clean conditional form",
            "749-Y5-R10-q_loc-vector-component-decomposition-or-alpha3-response-operator-fill.md",
            "alpha3_q = W_q_alpha3 * f_qV * q_proxy",
        ],
        "role": "immediate 749 handoff",
    },
    "748_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_748_VALIDATION.csv",
        "needles": ["V748_14_validation_rows_ready", "V748_11_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "748_template": {
        "path": RESIDUALS / "P8_Y5_R10_748_WQALPHA3_SOURCE_ROW_TEMPLATE.csv",
        "needles": ["WQS748_0_q_vector_fraction", "MISSING_QLOC_VECTOR_DECOMPOSITION"],
        "role": "q_loc vector fraction missing row",
    },
    "748_product_gate": {
        "path": RESIDUALS / "P8_Y5_R10_748_ALPHA3_PRODUCT_GATE.csv",
        "needles": ["A3P748_0_product_definition", "5.38167370680806e-15"],
        "role": "alpha3 product pressure",
    },
    "746_projection_contract": {
        "path": RESIDUALS / "P8_Y5_R10_746_QLOC_PROJECTION_CONTRACT.csv",
        "needles": ["QPC746_0_decompose_q_loc", "q_loc^nu = q_T tau^nu + q_L n^nu + q_V^nu + q_TF^nu"],
        "role": "componentwise projection contract",
    },
    "746_channel_router": {
        "path": RESIDUALS / "P8_Y5_R10_746_QLOC_CHANNEL_ROUTER.csv",
        "needles": ["QCR746_2_alpha3_momentum_flux", "highest_pressure_branch_if_projection_applies"],
        "role": "alpha3 channel priority",
    },
    "740_mass_channel": {
        "path": RESIDUALS / "P8_Y5_R10_740_QLOC_MASS_CHANNEL_MAP.csv",
        "needles": ["QMM740_0_define_mass_channel", "parent-owned C_qnu"],
        "role": "q_loc mass-channel identity",
    },
    "740_observable_transfer": {
        "path": RESIDUALS / "P8_Y5_R10_740_QLOC_OBSERVABLE_TRANSFER_MAP.csv",
        "needles": ["QOT740_3_PPN_vector", "weak-field Green operator"],
        "role": "observable transfer map missing inputs",
    },
    "740_first_bound": {
        "path": RESIDUALS / "P8_Y5_R10_740_FIRST_QLOC_BOUND_ATTEMPT.csv",
        "needles": ["QBA740_0_compact_shell_proxy", "source_backed_proxy_not_arena_bound"],
        "role": "source-backed proxy status",
    },
    "741_unit_gate": {
        "path": RESIDUALS / "P8_Y5_R10_741_COMPACT_SHELL_UNIT_MAP_GATE.csv",
        "needles": ["CSU741_0_proxy_loaded", "dimensionless proxy has no C_q"],
        "role": "unit-map blocker",
    },
    "742_free_pack": {
        "path": RESIDUALS / "P8_Y5_R10_742_QLOC_FREE_COEFFICIENT_PACK.csv",
        "needles": ["QFC742_3_PPN_vector", "c_q_PPN_vector"],
        "role": "free PPN vector coefficient pack",
    },
    "743_coeff_attempt": {
        "path": RESIDUALS / "P8_Y5_R10_743_QLOC_COEFFICIENT_ROW_ATTEMPT.csv",
        "needles": ["QCR743_4_c_q_PPN_vector", "weak-field Green operator"],
        "role": "q_loc PPN coefficient blocker",
    },
    "744_cqm_contract": {
        "path": RESIDUALS / "P8_Y5_R10_744_CQM_COUPLING_CONTRACT.csv",
        "needles": ["CQM744_0_operator_norm_definition", "q_proxy remains a breadcrumb"],
        "role": "scalar coupling norm guard",
    },
    "747_pressure": {
        "path": RESIDUALS / "P8_Y5_R10_747_WQALPHA3_COEFFICIENT_PRESSURE.csv",
        "needles": ["WQA747_2_if_W_order_one", "5.38167370680806e-15"],
        "role": "alpha3 coefficient pressure",
    },
    "733_metric_response": {
        "path": RESIDUALS / "P8_Y5_R10_733_METRIC_RESPONSE_DERIVATION.csv",
        "needles": ["MRD733_4_q_loc_gate", "Project the Ward identity"],
        "role": "metric-response q_loc gate",
    },
    "734_formula_ledger": {
        "path": RESIDUALS / "P8_Y5_R10_734_RESIDUAL_FORMULA_LEDGER.csv",
        "needles": ["RFL734_0_reduced_Ward_shape", "RFL734_2_observed_residual_survives"],
        "role": "q_loc residual formula ledger",
    },
    "734_runner": {
        "path": RESIDUALS / "P8_Y5_R10_734_HYBRID_QLOC_RESIDUAL_RUNNER_FILLED.csv",
        "needles": ["HQR734_3_PPN_metric_tail", "weak-field Green operator"],
        "role": "hybrid q_loc runner status",
    },
    "739_channelwise": {
        "path": RESIDUALS / "P8_Y5_R10_739_CHANNELWISE_PROJECTION_LEDGER.csv",
        "needles": ["EX739_4_q_loc_mass_projection", "open_observed_q_loc_not_zero_C_qmu_missing"],
        "role": "channelwise projection ledger",
    },
    "r11_vector_status": {
        "path": RESIDUALS / "R11_EXECUTABLE_VECTOR_STATUS.csv",
        "needles": ["vector_preferred_frame", "template_only"],
        "role": "R11 vector operator status",
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


def decomposition_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "component_id": "QCD749_0_observed_frame",
            "object": "observed local frame",
            "definition": "choose unit time u^mu and spatial projector h^mu_nu = delta^mu_nu + u^mu u_nu",
            "exact_status": "kinematic_if_frame_supplied",
            "missing_for_numeric": "parent-normalized observed tau/u; local domain A; metric sign convention; source path",
            "observable_effect": "without frame, temporal/scalar and spatial/vector q_loc pieces cannot be separated",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "QCD749_1_temporal_scalar",
            "object": "q_T",
            "definition": "q_T := -u_nu q_loc^nu; q_parallel^mu = q_T u^mu",
            "exact_status": "definition_written_no_value",
            "missing_for_numeric": "q_loc field/profile, u^mu normalization, integration/norm convention",
            "observable_effect": "feeds mass/source-strength, clock/Gdot, and beta/gamma only through separate response maps",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "QCD749_2_spatial_projection",
            "object": "q_perp^mu",
            "definition": "q_perp^mu := h^mu_nu q_loc^nu",
            "exact_status": "definition_written_no_value",
            "missing_for_numeric": "h^mu_nu, q_loc field/profile, shell/domain measure",
            "observable_effect": "contains all possible preferred-frame/vector/flux danger",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "QCD749_3_Hodge_Helmholtz_split",
            "object": "q_perp^i = D^i sigma_q + q_V^i + q_H^i",
            "definition": "D_i q_V^i=0, q_H is harmonic/boundary-supported, and boundary conditions fix the split",
            "exact_status": "mathematical_contract_written_not_executable",
            "missing_for_numeric": "spatial slice geometry, boundary conditions, q_loc samples/field, norm for each component",
            "observable_effect": "separates scalar gradient/radial leakage from transverse vector and boundary/harmonic leakage",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "QCD749_4_alpha3_momentum_fraction",
            "object": "f_qV",
            "definition": "f_qV := ||P_alpha3 q_loc||_A / q_proxy, with P_alpha3 selecting momentum/preferred-frame flux",
            "exact_status": "definition_written_no_value",
            "missing_for_numeric": "P_alpha3, component norm, q_loc vector field, proof q_proxy is same denominator",
            "observable_effect": f"alpha3 needs |W_q_alpha3 f_qV| <= {WF_LIMIT:.15g}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "QCD749_5_q_proxy_guard",
            "object": "q_proxy",
            "definition": f"q_proxy = max_abs_Ploc_drelJrel = {Q_PROXY:.15g}",
            "exact_status": "source_backed_scalar_proxy_only",
            "missing_for_numeric": "component fractions, C_q/P_alpha3 unit map, arena normalization",
            "observable_effect": "cannot be treated as f_qV, W_q_alpha3, or an alpha3 prediction",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "QCD749_6_STF_guard",
            "object": "q_TF or anisotropy channel",
            "definition": "bare q_loc^mu is a vector; STF/tensor leakage must come from derivatives, stress response, or metric operator map",
            "exact_status": "guard_written",
            "missing_for_numeric": "weak-field metric-response map and stress/operator source",
            "observable_effect": "prevents hiding a tensor preferred-location effect inside the vector proxy",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "QCD749_7_verdict",
            "object": "component-filled q_loc row",
            "definition": "claim row requires q_T, q_perp, q_V, q_H, f_qV, source paths, units, and no-cancellation flag",
            "exact_status": "decomposition_not_filled_current_corpus",
            "missing_for_numeric": "actual q_loc field/component data or theorem-zero certificate",
            "observable_effect": "no alpha3/PPN/R10 promotion",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def response_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "operator_id": "A3R749_0_source_to_metric",
            "operator_piece": "linearized weak-field solve",
            "formula": "delta g_mn = G_PPN_mn[q_loc_source]",
            "required_inputs": "linearized field equations, gauge convention, source normalization, boundary conditions",
            "current_status": "missing",
            "claim_effect": "no W_q_alpha3 value",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "operator_id": "A3R749_1_metric_to_alpha3",
            "operator_piece": "PPN alpha3 projection",
            "formula": "alpha3_q = P_alpha3^PPN[delta g_0i, preferred-frame momentum terms]",
            "required_inputs": "official PPN basis, velocity/frame convention, sign/normalization, comparison row",
            "current_status": "missing",
            "claim_effect": "cannot map q_loc vector flux to observable alpha3",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "operator_id": "A3R749_2_weight_definition",
            "operator_piece": "W_q_alpha3",
            "formula": "W_q_alpha3 := alpha3_q / epsilon_q_momentum or operator norm ||P_alpha3^PPN G_PPN P_flux||",
            "required_inputs": "P_flux, G_PPN, PPN alpha3 projector, component norm",
            "current_status": "contract_written_no_value",
            "claim_effect": f"must combine with f_qV so |W_q_alpha3 f_qV| <= {WF_LIMIT:.15g}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "operator_id": "A3R749_3_zero_sufficient_condition",
            "operator_piece": "structural alpha3 zero",
            "formula": "P_alpha3^PPN G_PPN P_flux q_loc = 0",
            "required_inputs": "component theorem, response parity, local odd charge zero, boundary silence",
            "current_status": "not_parent_derived",
            "claim_effect": "would kill q_loc alpha3 branch without tiny coefficients",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "operator_id": "A3R749_4_numeric_sufficient_condition",
            "operator_piece": "source-backed product row",
            "formula": f"abs(W_q_alpha3 * f_qV * {Q_PROXY:.15g}) <= {ALPHA3_BOUND:.15g}",
            "required_inputs": "numeric W_q_alpha3, numeric f_qV, units, source paths, no hidden cancellation",
            "current_status": "not_loaded",
            "claim_effect": "template only; no alpha3 pass",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def component_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "COG749_0_temporal_scalar",
            "component": "q_T",
            "maps_to": "source mass, clock/Gdot, beta/gamma scalar response",
            "required_to_score": "c_qM/c_qt/W_even with same-frame denominator and units",
            "current_status": "unfilled",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "COG749_1_longitudinal_gradient",
            "component": "D^i sigma_q or radial q_L",
            "maps_to": "radial hair, gamma/beta slip, possible range kernel",
            "required_to_score": "radial profile, Green operator, range/lambda map if finite-range",
            "current_status": "unfilled",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "COG749_2_transverse_vector",
            "component": "q_V^i",
            "maps_to": "alpha1/alpha2/alpha3 preferred-frame rows",
            "required_to_score": f"f_qV and W_q_alpha3 product <= {WF_LIMIT:.15g}, or theorem-zero",
            "current_status": "highest_pressure_unfilled",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "COG749_3_harmonic_boundary",
            "component": "q_H^i/boundary flux",
            "maps_to": "alpha3, xi, boundary-source shifts",
            "required_to_score": "boundary conditions, no-flux theorem, or source-backed boundary coefficient",
            "current_status": "unfilled",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "COG749_4_STF_metric_response",
            "component": "metric/stress anisotropy response",
            "maps_to": "xi/preferred-location and tensor non-EH operator rows",
            "required_to_score": "stress/metric response operator; cannot be read from bare vector alone",
            "current_status": "guarded_unfilled",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def product_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "product_id": "WFP749_0_current_known_number",
            "quantity": "q_proxy",
            "value": f"{Q_PROXY:.15g}",
            "status": "known_scalar_proxy",
            "claim_gate": "not an alpha3 vector fraction",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "product_id": "WFP749_1_vector_fraction",
            "quantity": "f_qV",
            "value": "MISSING_QLOC_HODGE_COMPONENTS",
            "status": "not_filled",
            "claim_gate": "must be theorem-zero or numeric with source path",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "product_id": "WFP749_2_response_weight",
            "quantity": "W_q_alpha3",
            "value": "MISSING_ALPHA3_RESPONSE_OPERATOR",
            "status": "not_filled",
            "claim_gate": "must be derived/bounded from weak-field PPN response operator",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "product_id": "WFP749_3_product_limit",
            "quantity": "abs(W_q_alpha3 * f_qV)",
            "value": f"must_be <= {WF_LIMIT:.15g}",
            "status": "limit_written_no_value",
            "claim_gate": "claim only if product is exact zero or source-backed below bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "product_id": "WFP749_4_unit_pressure",
            "quantity": "q_proxy / alpha3_bound",
            "value": f"{UNIT_RATIO:.15g}",
            "status": "danger_scale_only",
            "claim_gate": "not evidence; only says unit vector response would be crushed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D749_0_decomposition",
            "decision": "write exact kinematic/Hodge decomposition contract",
            "meaning": "the vector geometry is now clean enough to tell what data would fill f_qV",
            "claim_status": "contract_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D749_1_no_numeric_fqV",
            "decision": "do not infer f_qV from q_proxy",
            "meaning": "q_proxy is a source-backed scalar max proxy, not a component-resolved vector norm",
            "claim_status": "numeric_fill_rejected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D749_2_response_operator",
            "decision": "write alpha3 response operator contract",
            "meaning": "W_q_alpha3 must come from a gauge-fixed weak-field PPN solve, not a guessed coefficient",
            "claim_status": "operator_missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D749_3_next",
            "decision": "acquire q_loc component field or build alpha3 response runner",
            "meaning": "the next useful object is executable component data, not another scalar smoke comparison",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def y5_update_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "Y5R749_alpha3_q_loc",
            "source_row": "R7_alpha3/q_loc",
            "status_after_749": "component_contract_written_product_unfilled",
            "zero_or_input": f"need f_qV=0, W_q_alpha3=0, or abs(W_q_alpha3 f_qV)<= {WF_LIMIT:.15g}",
            "still_missing": "component-resolved q_loc field; alpha3 response operator; source paths and units",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R749_PPN_scalar_vector",
            "source_row": "R3-R8/q_loc",
            "status_after_749": "componentwise_rows_retained",
            "zero_or_input": "each scalar/vector/STF component needs its own coefficient or zero theorem",
            "still_missing": "beta/gamma/alpha_i/xi response maps",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R749_R10",
            "source_row": "R10/q_loc",
            "status_after_749": "not_promoted",
            "zero_or_input": "range branch needs lambda kernel and alpha(lambda) coefficient",
            "still_missing": "range kernel and real bound comparison",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU749_0_allowed",
            "allowed_after_749": "say the q_loc component decomposition is defined but not populated",
            "forbidden_after_749": "say q_proxy is the transverse vector fraction",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU749_1_allowed",
            "allowed_after_749": "derive or source f_qV with a Hodge/Helmholtz component runner",
            "forbidden_after_749": "use a scalar mass smoke row as an alpha3 vector score",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU749_2_allowed",
            "allowed_after_749": "derive W_q_alpha3 from a gauge-fixed weak-field response operator",
            "forbidden_after_749": "choose W_q_alpha3 after seeing the bound",
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
            "main_result": "q_loc component decomposition and alpha3 response operator contracts written; f_qV and W_q_alpha3 remain unfilled",
            "hard_blocker": "q_proxy is not component-resolved; no q_loc field/Hodge split or alpha3 weak-field response operator exists yet",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def make_validation(
    sources: list[dict[str, Any]],
    decomposition: list[dict[str, Any]],
    response: list[dict[str, Any]],
    component_gate: list[dict[str, Any]],
    product_gate: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    outputs: list[Path],
) -> list[dict[str, str]]:
    prior = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_748_VALIDATION.csv")
    all_rows = decomposition + response + component_gate + product_gate + decisions + y5_update + routes
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V749_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V749_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all source files contain expected evidence needles"})
    validation.append({"check_id": "V749_2_prior_748_clean", "result": "pass" if prior and all(row.get("result") == "pass" for row in prior) else "fail", "detail": "748 validation has no failures"})
    validation.append({"check_id": "V749_3_decomposition_not_filled", "result": "pass" if any(row["exact_status"] == "decomposition_not_filled_current_corpus" for row in decomposition) else "fail", "detail": "component split remains nonclaim"})
    validation.append({"check_id": "V749_4_qproxy_guard", "result": "pass" if any(row["component_id"] == "QCD749_5_q_proxy_guard" and "cannot be treated as f_qV" in row["observable_effect"] for row in decomposition) else "fail", "detail": "q_proxy not promoted to vector fraction"})
    validation.append({"check_id": "V749_5_response_operator_missing", "result": "pass" if any(row["operator_id"] == "A3R749_2_weight_definition" and row["current_status"] == "contract_written_no_value" for row in response) else "fail", "detail": "W_q_alpha3 value not filled"})
    validation.append({"check_id": "V749_6_product_limit_written", "result": "pass" if any(f"{WF_LIMIT:.15g}" in row.get("value", "") or f"{WF_LIMIT:.15g}" in row.get("claim_gate", "") for row in product_gate) else "fail", "detail": f"WF_limit={WF_LIMIT:.15g}"})
    validation.append({"check_id": "V749_7_missing_inputs_explicit", "result": "pass" if any("MISSING_" in row["value"] for row in product_gate) else "fail", "detail": "missing f_qV/W inputs remain explicit"})
    validation.append({"check_id": "V749_8_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_rows) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V749_9_no_local_arena_claim", "result": "pass" if "no_alpha3_PPN_R10_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "alpha3/PPN/R10/Newton/local-GR claims remain blocked"})
    validation.append({"check_id": "V749_10_next_target_selected", "result": "pass" if all(row.get("next_target") == NEXT_TARGET for row in decisions) else "fail", "detail": NEXT_TARGET})
    validation.append({"check_id": "V749_11_outputs_scoped", "result": "pass" if all(under_post(path) for path in outputs) else "fail", "detail": "all outputs under post-checkpoint-work"})
    changed = formalization_changed_after_cutoff()
    validation.append({"check_id": "V749_12_formalization_workbench_untouched", "result": "pass" if changed == 0 else "fail", "detail": f"formalization_changed_after_cutoff={changed}"})
    validation.append({"check_id": "V749_13_y5_rows_retained", "result": "pass" if {"Y5R749_alpha3_q_loc", "Y5R749_PPN_scalar_vector", "Y5R749_R10"}.issubset({row["runner_id"] for row in y5_update}) else "fail", "detail": "alpha3/PPN/R10 rows retained"})
    validation.append({"check_id": "V749_14_route_forbids_scalar_as_alpha3", "result": "pass" if any("scalar mass smoke row" in row["forbidden_after_749"] for row in routes) else "fail", "detail": "scalar smoke cannot become alpha3 vector score"})
    validation.append({"check_id": "V749_15_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    decomposition: list[dict[str, Any]],
    response: list[dict[str, Any]],
    component_gate: list[dict[str, Any]],
    product_gate: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 749 - Y5 R10 q_loc Vector Component Decomposition Or alpha3 Response Operator Fill

Start point: 748 left the dangerous branch as

```text
alpha3_q = W_q_alpha3 * f_qV * q_proxy
q_proxy = {Q_PROXY:.15g}
required: |W_q_alpha3 f_qV| <= {WF_LIMIT:.15g}
```

Current result: **the q_loc component decomposition can be stated exactly as a kinematic/Hodge contract, but it cannot be numerically filled from the current corpus**. The known `q_proxy` is a scalar max-proxy. It is source-backed as an internal residual scale, but it is not a transverse vector fraction, not an alpha3 response coefficient, and not an arena score.

749 therefore separates two missing objects:

1. `f_qV`: the fraction of the q_loc residual lying in the alpha3 momentum/preferred-frame component.
2. `W_q_alpha3`: the weak-field PPN response weight mapping that component into observable alpha3.

Both remain unfilled. This is a clean wall, but a useful one: it tells us exactly what data or theorem has to exist next.

## Summary

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | component decomposition contract written; f_qV and W_q_alpha3 not filled |
| Next target | `{NEXT_TARGET}` |

## q_loc Component Decomposition Contract

{markdown_table(decomposition, ["component_id", "object", "definition", "exact_status", "missing_for_numeric", "observable_effect", "valid_for_claim"])}

## alpha3 Response Operator Contract

{markdown_table(response, ["operator_id", "operator_piece", "formula", "required_inputs", "current_status", "claim_effect", "valid_for_claim"])}

## Component To Observable Gate

{markdown_table(component_gate, ["gate_id", "component", "maps_to", "required_to_score", "current_status", "valid_for_claim"])}

## Wqalpha3 f_qV Product Status

{markdown_table(product_gate, ["product_id", "quantity", "value", "status", "claim_gate", "valid_for_claim"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Y5 Runner Update

{markdown_table(y5_update, ["runner_id", "source_row", "status_after_749", "zero_or_input", "still_missing", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_749", "forbidden_after_749", "next_action", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is the right kind of non-answer: we now know exactly why the previous scalar smoke number cannot decide the preferred-frame branch. To beat alpha3 honestly, MTS needs either a structural theorem that `P_alpha3 q_loc=0`, or an executable component field/response operator showing the product is below `5.38e-15`. No cheating, no panic: the path is now sharper.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    decomposition = decomposition_rows(generated_utc)
    response = response_rows(generated_utc)
    component_gate = component_gate_rows(generated_utc)
    product_gate = product_gate_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    y5_update = y5_update_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)

    outputs = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        DECOMPOSITION_PATH,
        RESPONSE_PATH,
        COMPONENT_GATE_PATH,
        PRODUCT_GATE_PATH,
        DECISION_PATH,
        Y5_UPDATE_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]

    validation = make_validation(sources, decomposition, response, component_gate, product_gate, decisions, y5_update, routes, outputs)

    write_csv(
        SOURCE_REGISTER_PATH,
        sources,
        ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        DECOMPOSITION_PATH,
        decomposition,
        ["component_id", "object", "definition", "exact_status", "missing_for_numeric", "observable_effect", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESPONSE_PATH,
        response,
        ["operator_id", "operator_piece", "formula", "required_inputs", "current_status", "claim_effect", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        COMPONENT_GATE_PATH,
        component_gate,
        ["gate_id", "component", "maps_to", "required_to_score", "current_status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        PRODUCT_GATE_PATH,
        product_gate,
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
        ["runner_id", "source_row", "status_after_749", "zero_or_input", "still_missing", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        ROUTE_PATH,
        routes,
        ["route_id", "allowed_after_749", "forbidden_after_749", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SUMMARY_PATH,
        summary,
        ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, decomposition, response, component_gate, product_gate, decisions, y5_update, routes, validation)

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"749 validation failed: {failed}")
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")


if __name__ == "__main__":
    main()

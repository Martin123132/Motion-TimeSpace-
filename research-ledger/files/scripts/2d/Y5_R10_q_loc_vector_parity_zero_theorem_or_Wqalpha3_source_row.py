from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "748-Y5-R10-q_loc-vector-parity-zero-theorem-or-Wqalpha3-source-row.md"
NEXT_TARGET = "749-Y5-R10-q_loc-vector-component-decomposition-or-alpha3-response-operator-fill.md"
STATUS = "Y5_R10_748_vector_parity_zero_not_parent_derived_Wqalpha3_source_row_template_written_nonclaim"
CLAIM_CEILING = "q_loc_vector_parity_zero_attempt_and_Wqalpha3_source_template_only_no_alpha3_PPN_R10_Newton_or_local_GR_pass"
Q_PROXY = 7.432631961576971e-06
ALPHA3_BOUND = 4.0e-20
WF_LIMIT = ALPHA3_BOUND / Q_PROXY
UNIT_RATIO = Q_PROXY / ALPHA3_BOUND
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_748_SOURCE_REGISTER.csv"
PARITY_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_748_VECTOR_PARITY_ZERO_THEOREM_AUDIT.csv"
SOURCE_TEMPLATE_PATH = RESIDUALS / "P8_Y5_R10_748_WQALPHA3_SOURCE_ROW_TEMPLATE.csv"
PRODUCT_GATE_PATH = RESIDUALS / "P8_Y5_R10_748_ALPHA3_PRODUCT_GATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_748_DECISION_MATRIX.csv"
Y5_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_748_Y5_RUNNER_UPDATE.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_748_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_748_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_748_VALIDATION.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "747_doc": {
        "path": POST_CHECKPOINT / "747-Y5-R10-alpha3-momentum-flux-zero-or-q_loc-vector-coefficient-bound.md",
        "needles": [
            "alpha3/q_loc momentum-flux zero theorem does not close",
            "748-Y5-R10-q_loc-vector-parity-zero-theorem-or-Wqalpha3-source-row.md",
            "|W_q_alpha3 f_qV| <= alpha3_bound/q_proxy",
        ],
        "role": "immediate 748 handoff",
    },
    "747_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_747_VALIDATION.csv",
        "needles": ["V747_14_validation_rows_ready", "V747_12_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "747_zero_audit": {
        "path": RESIDUALS / "P8_Y5_R10_747_ALPHA3_QLOC_ZERO_THEOREM_AUDIT.csv",
        "needles": ["AZ747_1_exchange_odd", "conditional_only", "AZ747_4_verdict"],
        "role": "prior q_loc alpha3 zero audit",
    },
    "747_pressure": {
        "path": RESIDUALS / "P8_Y5_R10_747_WQALPHA3_COEFFICIENT_PRESSURE.csv",
        "needles": ["WQA747_0_product_definition", "WQA747_4_acceptance"],
        "role": "prior Wqalpha3 pressure limit",
    },
    "746_alpha3_gate": {
        "path": RESIDUALS / "P8_Y5_R10_746_ALPHA3_MOMENTUM_FLUX_GATE.csv",
        "needles": ["A3Q746_0_product_law", "W_q_alpha3 * epsilon_q_momentum"],
        "role": "alpha3 product law origin",
    },
    "odd_split": {
        "path": RESIDUALS / "P8_SOURCE_NORMALIZATION_EVEN_ODD_SPLIT.csv",
        "needles": ["E1_odd_extra_source", "E2_even_extra_source"],
        "role": "even/odd source-normalization guard",
    },
    "odd_component_map": {
        "path": RESIDUALS / "P8_ODD_RESIDUAL_COMPONENT_MAP.csv",
        "needles": ["Y3_domain_vector", "conditional_best", "Y5_source_normalization"],
        "role": "odd-vector component status",
    },
    "odd_exchange": {
        "path": RESIDUALS / "P8_ODD_RESIDUAL_EXCHANGE_THEOREM.csv",
        "needles": ["E5_current_corpus", "conditional theorem only"],
        "role": "exchange theorem blocker",
    },
    "domain_no_vector_attempt": {
        "path": RESIDUALS / "P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
        "needles": ["T6_no_vector_verdict", "fail_current_corpus"],
        "role": "domain no-vector theorem attempt",
    },
    "domain_vector_coefficients": {
        "path": RESIDUALS / "P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENTS.csv",
        "needles": ["R7_alpha3", "W_domain_alpha3_epsilon_domain_flux"],
        "role": "domain vector coefficient precedent",
    },
    "domain_vector_gate": {
        "path": RESIDUALS / "P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENT_GATE.csv",
        "needles": ["G_R7_alpha3", "4e-20"],
        "role": "preferred-frame product gate precedent",
    },
    "domain_parent_clause": {
        "path": RESIDUALS / "P8_DOMAIN_SELECTOR_PARENT_ACTION_CLAUSE.csv",
        "needles": ["C5_R11_silence", "fail_current_corpus"],
        "role": "parent action clause showing R11 silence missing",
    },
    "r11_domain_minimum": {
        "path": RESIDUALS / "R11_DOMAIN_PROJECTOR_OPERATOR_VECTOR_MINIMUM.csv",
        "needles": ["vector_preferred_frame", "MISSING_DOMAIN_VECTOR_ABSENCE_THEOREM_OR_NUMERIC_COEFFICIENTS"],
        "role": "minimum vector operator row",
    },
    "r11_domain_missing": {
        "path": RESIDUALS / "R11_DOMAIN_PROJECTOR_VECTOR_MISSING_LEDGER.csv",
        "needles": ["vector_preferred_frame", "claim_blocked_until"],
        "role": "missing field ledger for vector operator",
    },
    "r11_executable_status": {
        "path": RESIDUALS / "R11_EXECUTABLE_VECTOR_STATUS.csv",
        "needles": ["vector_preferred_frame", "template_only"],
        "role": "global executable vector status",
    },
    "r11_nonEH_vector": {
        "path": RESIDUALS / "R11_nonEH_operator_vector_executable.csv",
        "needles": ["vector_preferred_frame", "MISSING_DOMAIN_VECTOR_ABSENCE_THEOREM_OR_NUMERIC_COEFFICIENTS"],
        "role": "non-EH operator vector row",
    },
    "momentum_map_theorem": {
        "path": RESIDUALS / "P8_Y5_R10_582_MOMENTUM_MAP_CLOSURE_THEOREM.csv",
        "needles": ["MMT582_4_no_pole_result", "conditional_theorem_only"],
        "role": "momentum-map closure blocker",
    },
    "momentum_map_contract": {
        "path": RESIDUALS / "P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv",
        "needles": ["NMC583_3_momentum_map", "not_derived"],
        "role": "Noether contract blocker",
    },
    "momentum_owner_test": {
        "path": RESIDUALS / "P8_Y5_R10_586_MOMENTUM_MAP_OWNER_TEST.csv",
        "needles": ["MMT586_1_vertical_generator", "blocked"],
        "role": "momentum-map owner test",
    },
    "mu_extra_alpha3_zero": {
        "path": RESIDUALS / "P8_MU_EXTRA_ALPHA3_ZERO_ATTEMPT.csv",
        "needles": ["ZA0_alpha3_exchange_owner", "conditional_identity_only", "ZA7_conclusion"],
        "role": "older alpha3 no-flux analogue",
    },
    "alpha3_fill_skeleton": {
        "path": RESIDUALS / "P8_MU_EXTRA_ALPHA3_FILL_INPUT_SKELETON.csv",
        "needles": ["target_bound", "4e-20", "MISSING_NUMERIC_OR_DERIVED_ZERO"],
        "role": "alpha3 fill skeleton precedent",
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


def parity_audit_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "VPZ748_0_theorem_shape",
            "needed_clause": "exchange/parity involution on q_loc vector sector",
            "mathematical_form": "E(q_V^i)=-q_V^i, E(S_parent)=S_parent, E(g_obs)=g_obs",
            "current_status": "conditional_shape_written",
            "blocker": "parent representative map and q_loc vector component certificate are not supplied",
            "effect_if_closed": "makes vector/momentum q_loc an odd sector candidate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "VPZ748_1_matter_evenness",
            "needed_clause": "matter and clocks see only exchange-even quotient geometry",
            "mathematical_form": "S_matter[Psi,e_obs(R_even)] with delta_{q_V} S_matter odd-free through PPN order",
            "current_status": "not_parent_derived",
            "blocker": "odd exchange theorem says matter evenness/component map is missing",
            "effect_if_closed": "prevents ordinary matter from sourcing alpha3 through q_V",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "VPZ748_2_local_odd_charge_zero",
            "needed_clause": "compact local branch has no odd vector/source charge",
            "mathematical_form": "J_qV=0 and int_boundary B_qV=0",
            "current_status": "not_derived",
            "blocker": "local odd boundary charge and no-flux clauses remain conditional",
            "effect_if_closed": "kills epsilon_q_momentum without tiny coefficients",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "VPZ748_3_alpha3_functional_parity",
            "needed_clause": "alpha3 response is odd in q_V and zero when odd charge vanishes",
            "mathematical_form": "alpha3_q[q_V]=W_q_alpha3 P_mom(q_V), alpha3_q[-q_V]=-alpha3_q[q_V]",
            "current_status": "response_operator_missing",
            "blocker": "W_q_alpha3 weak-field/PPN response operator is not sourced",
            "effect_if_closed": "turns parity into an observable alpha3 zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "VPZ748_4_even_source_leak_guard",
            "needed_clause": "source-normalization even leakage cannot re-enter alpha3/vector rows",
            "mathematical_form": "E(mu_extra_even)=+mu_extra_even but P_alpha3(mu_extra_even)=0 or separately scored",
            "current_status": "not_closed",
            "blocker": "even source-normalization offset survives exchange unless a deeper split is derived",
            "effect_if_closed": "prevents parity proof from hiding scalar/even leakage",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "VPZ748_5_momentum_map_owner",
            "needed_clause": "q_loc vector flux is a first-class vertical constraint or exact boundary-silent current",
            "mathematical_form": "G[epsilon]=int epsilon C_q + Q_boundary, i_v Omega=delta G, Q_boundary=0",
            "current_status": "blocked",
            "blocker": "symplectic potential, vertical generator, algebra closure, and boundary zero are missing",
            "effect_if_closed": "demotes q_V from physical preferred-frame source to gauge/constraint",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "VPZ748_6_verdict",
            "needed_clause": "claim alpha3_q=0 by vector parity",
            "mathematical_form": "VPZ748_0 through VPZ748_5 all parent-signed => alpha3_q=0",
            "current_status": "parity_zero_failed_current_corpus",
            "blocker": "at least five parent signatures are absent; source-row fallback required",
            "effect_if_closed": "would remove q_loc alpha3 pressure but not beta/gamma/R10 automatically",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def source_template_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "WQS748_0_q_vector_fraction",
            "target_row": "R7_alpha3/q_loc",
            "quantity": "f_qV",
            "formula": "epsilon_q_momentum / q_proxy",
            "current_value": "MISSING_QLOC_VECTOR_DECOMPOSITION",
            "required_for_claim": "derived_zero or numeric dimensionless f_qV with source path",
            "units": "dimensionless",
            "source_path": "MISSING_SOURCE_FILE",
            "status": "template_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "row_id": "WQS748_1_alpha3_response_weight",
            "target_row": "R7_alpha3/q_loc",
            "quantity": "W_q_alpha3",
            "formula": "alpha3_q / epsilon_q_momentum",
            "current_value": "MISSING_WEAK_FIELD_PPN_RESPONSE_OPERATOR",
            "required_for_claim": "derived response operator or bounded coefficient with gauge/source normalization declared",
            "units": "dimensionless_after_PPN_normalization",
            "source_path": "MISSING_SOURCE_FILE",
            "status": "template_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "row_id": "WQS748_2_product_gate",
            "target_row": "R7_alpha3/q_loc",
            "quantity": "W_q_alpha3_f_qV",
            "formula": "W_q_alpha3 * f_qV",
            "current_value": "MISSING_NUMERIC_OR_DERIVED_ZERO_PRODUCT",
            "required_for_claim": f"abs(W_q_alpha3 * f_qV) <= {WF_LIMIT:.15g}",
            "units": "dimensionless",
            "source_path": "MISSING_SOURCE_FILE",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "row_id": "WQS748_3_predicted_alpha3",
            "target_row": "R7_alpha3/q_loc",
            "quantity": "alpha3_q",
            "formula": "alpha3_q = W_q_alpha3 * f_qV * q_proxy",
            "current_value": "MISSING_NUMERIC_OR_DERIVED_ZERO_ALPHA3",
            "required_for_claim": f"abs(alpha3_q) <= {ALPHA3_BOUND:.15g}",
            "units": "dimensionless PPN alpha3",
            "source_path": "MISSING_SOURCE_FILE",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "row_id": "WQS748_4_zero_certificate",
            "target_row": "R7_alpha3/q_loc",
            "quantity": "derived_zero_certificate",
            "formula": "vector parity + local odd charge zero + boundary silence + response parity",
            "current_value": "NOT_DERIVED_CURRENT_CORPUS",
            "required_for_claim": "parent-signed theorem source that proves alpha3_q=0 without fitted cancellation",
            "units": "theorem",
            "source_path": "MISSING_SOURCE_FILE",
            "status": "blocked_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "row_id": "WQS748_5_no_cancellation_guard",
            "target_row": "R7_alpha3/q_loc",
            "quantity": "no_hidden_cancellation_policy",
            "formula": "q_loc alpha3 channel must pass independently unless a parent identity forces cancellation",
            "current_value": "POLICY_RETAINED",
            "required_for_claim": "independent q_loc pass or explicit parent cancellation identity",
            "units": "policy",
            "source_path": str(RESIDUALS / "P8_Y5_R10_747_ALPHA3_QLOC_ACCEPTANCE_GATE.csv"),
            "status": "guard_only_not_claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def product_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "A3P748_0_product_definition",
            "formula": "alpha3_q = W_q_alpha3 * f_qV * q_proxy",
            "numeric_value": "symbolic",
            "interpretation": "observable alpha3 needs both a vector fraction and a response weight",
            "pass_condition": f"abs(W_q_alpha3 * f_qV) <= {WF_LIMIT:.15g}",
            "current_status": "not_scoreable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "A3P748_1_pressure_scale",
            "formula": "q_proxy / alpha3_bound",
            "numeric_value": f"{UNIT_RATIO:.15g}",
            "interpretation": "unit vector fraction and unit response would exceed alpha3 by this factor",
            "pass_condition": "do not use unit projection as evidence; use only as pressure scale",
            "current_status": "danger_scale_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "A3P748_2_parity_zero_route",
            "formula": "VPZ clauses close => f_qV=0 or W_q_alpha3 f_qV=0",
            "numeric_value": "not_available",
            "interpretation": "best natural route is a structural zero",
            "pass_condition": "parent-signed theorem source",
            "current_status": "failed_current_corpus",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "A3P748_3_numeric_source_route",
            "formula": "real W_q_alpha3, real f_qV, source path, units, no cancellation",
            "numeric_value": "not_loaded",
            "interpretation": "fallback if theorem-zero fails",
            "pass_condition": f"abs(W_q_alpha3 * f_qV * q_proxy) <= {ALPHA3_BOUND:.15g}",
            "current_status": "template_only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D748_0_parity_zero",
            "decision": "do not claim vector parity zero",
            "meaning": "the parity theorem has the right shape but lacks parent-owned component, matter-even, boundary, and response clauses",
            "claim_status": "zero_failed_current_chain",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D748_1_source_template",
            "decision": "write W_q_alpha3 source-row template",
            "meaning": f"the needed product is abs(W_q_alpha3 f_qV) <= {WF_LIMIT:.15g}, or an exact zero",
            "claim_status": "template_only_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D748_2_best_route",
            "decision": "next attack should split q_loc into scalar/vector/flux components",
            "meaning": "without the decomposition, we cannot know whether alpha3 is active or structurally silent",
            "claim_status": "next_work_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def y5_update_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "Y5R748_alpha3_q_loc",
            "source_row": "R7_alpha3/q_loc",
            "status_after_748": "parity_zero_failed_source_template_written",
            "zero_or_input": f"theorem-zero or abs(W_q_alpha3 f_qV) <= {WF_LIMIT:.15g}",
            "still_missing": "q_loc vector decomposition; matter-even quotient proof; local odd-charge zero; W_q_alpha3 response operator",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R748_R11_vector",
            "source_row": "R11/vector_preferred_frame",
            "status_after_748": "still_blocks_local_branch",
            "zero_or_input": "derive absent/gauge/aligned q_loc vector or fill real vector coefficients",
            "still_missing": "claim-valid vector/operator rows and source-normalization silence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "Y5R748_PPN_R10",
            "source_row": "PPN/R10 local residual gates",
            "status_after_748": "not_promoted",
            "zero_or_input": "alpha3 pressure unresolved; beta/gamma/R10 maps still separate",
            "still_missing": "scalar beta/gamma maps and finite-range lambda kernel",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU748_0_allowed",
            "allowed_after_748": "say vector parity zero is a conditional theorem contract",
            "forbidden_after_748": "say alpha3 or local PPN passes",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU748_1_allowed",
            "allowed_after_748": "use the W_q_alpha3 source template as a future input contract",
            "forbidden_after_748": "fill it with placeholders and call it evidence",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU748_2_allowed",
            "allowed_after_748": "prioritize q_loc component decomposition or alpha3 response operator",
            "forbidden_after_748": "hide vector leakage inside scalar q_proxy",
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
            "main_result": "vector parity zero theorem has a clean conditional form but is not parent-derived; Wqalpha3 source template written",
            "hard_blocker": "q_loc vector/flux decomposition and alpha3 response operator are missing",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def make_validation(
    sources: list[dict[str, Any]],
    parity: list[dict[str, Any]],
    template: list[dict[str, Any]],
    product: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    outputs: list[Path],
) -> list[dict[str, str]]:
    prior = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_747_VALIDATION.csv")
    all_rows = parity + template + product + decisions + y5_update + routes
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V748_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V748_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all source files contain expected evidence needles"})
    validation.append({"check_id": "V748_2_prior_747_clean", "result": "pass" if prior and all(row.get("result") == "pass" for row in prior) else "fail", "detail": "747 validation has no failures"})
    validation.append({"check_id": "V748_3_parity_zero_not_promoted", "result": "pass" if any(row["current_status"] == "parity_zero_failed_current_corpus" for row in parity) else "fail", "detail": "vector parity zero remains nonclaim"})
    validation.append({"check_id": "V748_4_product_limit_written", "result": "pass" if any(f"{WF_LIMIT:.15g}" in row.get("pass_condition", "") for row in product) else "fail", "detail": f"WF_limit={WF_LIMIT:.15g}"})
    validation.append({"check_id": "V748_5_source_template_nonclaim", "result": "pass" if template and all(row["valid_for_claim"] == "false" for row in template) else "fail", "detail": "Wqalpha3 rows all false"})
    validation.append({"check_id": "V748_6_missing_inputs_not_hidden", "result": "pass" if any("MISSING_" in row["current_value"] for row in template) else "fail", "detail": "missing decomposition/operator/source fields remain explicit"})
    validation.append({"check_id": "V748_7_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_rows) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V748_8_no_local_arena_claim", "result": "pass" if "no_alpha3_PPN_R10_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "alpha3/PPN/R10/Newton/local-GR claims remain blocked"})
    validation.append({"check_id": "V748_9_next_target_selected", "result": "pass" if all(row.get("next_target") == NEXT_TARGET for row in decisions) else "fail", "detail": NEXT_TARGET})
    validation.append({"check_id": "V748_10_outputs_scoped", "result": "pass" if all(under_post(path) for path in outputs) else "fail", "detail": "all outputs under post-checkpoint-work"})
    changed = formalization_changed_after_cutoff()
    validation.append({"check_id": "V748_11_formalization_workbench_untouched", "result": "pass" if changed == 0 else "fail", "detail": f"formalization_changed_after_cutoff={changed}"})
    validation.append({"check_id": "V748_12_y5_rows_retained", "result": "pass" if {"Y5R748_alpha3_q_loc", "Y5R748_R11_vector", "Y5R748_PPN_R10"}.issubset({row["runner_id"] for row in y5_update}) else "fail", "detail": "alpha3/R11/PPN-R10 rows retained"})
    validation.append({"check_id": "V748_13_route_forbids_scalar_hiding", "result": "pass" if any("scalar q_proxy" in row["forbidden_after_748"] for row in routes) else "fail", "detail": "vector leakage cannot be hidden in scalar q_proxy"})
    validation.append({"check_id": "V748_14_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    parity: list[dict[str, Any]],
    template: list[dict[str, Any]],
    product: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    y5_update: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 748 - Y5 R10 q_loc Vector Parity Zero Theorem Or Wqalpha3 Source Row

Start point: 747 showed that `alpha3_q = W_q_alpha3 * f_qV * q_proxy` is the dangerous local branch, with `q_proxy = {Q_PROXY:.15g}` and `|W_q_alpha3 f_qV| <= {WF_LIMIT:.15g}` required by the alpha3 lock.

Current result: **the vector parity zero theorem has a clean conditional form, but it is not parent-derived in the current corpus**. The route is good physics discipline: if the q_loc vector/flux sector is exchange-odd, matter sees only the exchange-even quotient, local odd charge and boundary flux vanish, and the alpha3 response functional is odd, then the q_loc alpha3 branch is exactly zero. But those clauses are not yet signed.

So 748 writes the honest fallback contract:

```text
alpha3_q = W_q_alpha3 * f_qV * q_proxy
q_proxy = {Q_PROXY:.15g}
alpha3_bound = {ALPHA3_BOUND:.15g}
required: |W_q_alpha3 f_qV| <= {WF_LIMIT:.15g}
```

This is still **nonclaim**. The next move is not to celebrate or panic; it is to either decompose `q_loc` into scalar/vector/flux pieces, or derive the weak-field alpha3 response operator.

## Summary

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Main result | vector parity theorem conditional only; Wqalpha3 source template written |
| Next target | `{NEXT_TARGET}` |

## Vector Parity Zero-Theorem Audit

{markdown_table(parity, ["clause_id", "needed_clause", "mathematical_form", "current_status", "blocker", "effect_if_closed", "valid_for_claim"])}

## Wqalpha3 Source Row Template

{markdown_table(template, ["row_id", "target_row", "quantity", "formula", "current_value", "required_for_claim", "units", "source_path", "status", "valid_for_claim"])}

## Alpha3 Product Gate

{markdown_table(product, ["gate_id", "formula", "numeric_value", "interpretation", "pass_condition", "current_status", "valid_for_claim"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Y5 Runner Update

{markdown_table(y5_update, ["runner_id", "source_row", "status_after_748", "zero_or_input", "still_missing", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_748", "forbidden_after_748", "next_action", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This is a useful failure, not a dead end. The parity kill-switch is now exact enough to inspect: it needs q_loc's vector part to be a genuine odd, unsourced, boundary-silent branch, and it needs the alpha3 response to respect that oddness. We do not have those signatures yet. The theory survives this checkpoint only as an honest nonclaim: either prove the vector piece is structurally zero, or fill the `W_q_alpha3 f_qV` product with real sourced inputs.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    parity = parity_audit_rows(generated_utc)
    template = source_template_rows(generated_utc)
    product = product_gate_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    y5_update = y5_update_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)

    outputs = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        PARITY_AUDIT_PATH,
        SOURCE_TEMPLATE_PATH,
        PRODUCT_GATE_PATH,
        DECISION_PATH,
        Y5_UPDATE_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]

    validation = make_validation(sources, parity, template, product, decisions, y5_update, routes, outputs)

    write_csv(
        SOURCE_REGISTER_PATH,
        sources,
        ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        PARITY_AUDIT_PATH,
        parity,
        ["clause_id", "needed_clause", "mathematical_form", "current_status", "blocker", "effect_if_closed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SOURCE_TEMPLATE_PATH,
        template,
        ["row_id", "target_row", "quantity", "formula", "current_value", "required_for_claim", "units", "source_path", "status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        PRODUCT_GATE_PATH,
        product,
        ["gate_id", "formula", "numeric_value", "interpretation", "pass_condition", "current_status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        DECISION_PATH,
        decisions,
        ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        Y5_UPDATE_PATH,
        y5_update,
        ["runner_id", "source_row", "status_after_748", "zero_or_input", "still_missing", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        ROUTE_PATH,
        routes,
        ["route_id", "allowed_after_748", "forbidden_after_748", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SUMMARY_PATH,
        summary,
        ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, parity, template, product, decisions, y5_update, routes, validation)

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"748 validation failed: {failed}")
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")


if __name__ == "__main__":
    main()

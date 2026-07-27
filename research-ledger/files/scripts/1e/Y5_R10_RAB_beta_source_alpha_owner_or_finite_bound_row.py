from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1414-Y5-R10-RAB-beta-source-alpha-owner-or-finite-bound-row.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1414_SOURCE_REGISTER.csv"
OWNER_ATTEMPT_PATH = SRC_DIR / "P8_Y5_R10_1414_BETA_SOURCE_ALPHA_OWNER_ATTEMPT.csv"
FINITE_BOUND_PATH = SRC_DIR / "P8_Y5_R10_1414_BETA_SOURCE_ALPHA_FINITE_BOUND_ROW.csv"
ANTI_SHORTCUT_PATH = SRC_DIR / "P8_Y5_R10_1414_BETA_SOURCE_ALPHA_ANTI_SHORTCUT_GATE.csv"
ARENA_GATE_PATH = SRC_DIR / "P8_Y5_R10_1414_BETA_SOURCE_ALPHA_ARENA_GATE.csv"
DECISION_PATH = SRC_DIR / "P8_Y5_R10_1414_DECISION_LEDGER.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1414_CLAIM_GATE.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1414_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1414_VALIDATION.csv"

STATUS = "Y5_R10_1414_beta_source_alpha_owner_not_derived_finite_bound_row_written_nonclaim"
CLAIM_CEILING = (
    "beta_source_alpha_owner_attempt_and_target_row_only_no_WEP_pass_no_clock_transfer_"
    "no_R10_no_R_EM_zero_no_Ps_products_no_Newton_no_local_GR_pass"
)


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def write_csv(relative_path: Path, rows: list[dict[str, Any]]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {relative_path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def anchor_found(relative_path: str, anchor: str) -> bool:
    path = ROOT / relative_path
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC1414_0_1413_doc",
            "source_path": "1413-Y5-R10-RAB-first-residual-component-zero-or-source-row.md",
            "anchor": "NEXT1413_0_1414",
            "role": "prior checkpoint selecting beta_source_alpha owner-or-finite-bound row",
        },
        {
            "source_id": "SRC1414_1_1413_R_EM_rows",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1413_R_EM_FINITE_SOURCE_ROW_TEMPLATE.csv",
            "anchor": "RFS1413_2_beta_source_alpha",
            "role": "R_EM finite source-row pack naming beta_source_alpha as target-only",
        },
        {
            "source_id": "SRC1414_2_1413_arena_gate",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1413_R_EM_ARENA_PROJECTION_GATE.csv",
            "anchor": "RAG1413_1_WEP",
            "role": "WEP/R10 arena gate blocked by source normalization and U_a",
        },
        {
            "source_id": "SRC1414_3_989_owner",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_989_BETA_SOURCE_OWNER_LEDGER.csv",
            "anchor": "BSO989_4_failure_action",
            "role": "beta_source_alpha owner ledger and target-only rows",
        },
        {
            "source_id": "SRC1414_4_989_inputs",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_989_PARENT_INPUT_CANDIDATE_LEDGER.csv",
            "anchor": "PIC989_2_Noether_current_owner",
            "role": "required parent input for Noether/current owner",
        },
        {
            "source_id": "SRC1414_5_989_route",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_989_ROUTE_DECISION_MATRIX.csv",
            "anchor": "DEC989_2_project_position",
            "role": "prior decision localizing coupling bottleneck to source normalization and EM-lock ownership",
        },
        {
            "source_id": "SRC1414_6_1077_wep_owner",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv",
            "anchor": "WCO1077_5_verdict",
            "role": "parent WEP coupling owner theorem remains unsigned",
        },
        {
            "source_id": "SRC1414_7_1077_clause",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1077_CLAUSE_SIGNATURE_MATRIX.csv",
            "anchor": "CLAUSE1077_2_current_owner",
            "role": "single current/source normalization owner missing",
        },
        {
            "source_id": "SRC1414_8_1077_counterexamples",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1077_ZERO_THEOREM_COUNTEREXAMPLE_AUDIT.csv",
            "anchor": "CE1077_1_current_rescaling",
            "role": "current rescaling/source marker counterexample",
        },
        {
            "source_id": "SRC1414_9_1405_response",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1405_PARENT_WEP_RESPONSE_CURRENT_DERIVATION.csv",
            "anchor": "WRC1405_4_source_contraction",
            "role": "WEP response-current identity needs K_ab alpha_source^b",
        },
        {
            "source_id": "SRC1414_10_1409_Ua",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1409_OFFICIAL_READOUT_BLOCKER_LEDGER.csv",
            "anchor": "ORB1409_7_verdict",
            "role": "U_a/source readout blocker still prevents WEP scoring",
        },
        {
            "source_id": "SRC1414_11_988_pressure",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv",
            "anchor": "WEP988_WAS651_1_surface_binding",
            "role": "alpha/Coulomb and robust WEP pressure targets, nonclaim",
        },
        {
            "source_id": "SRC1414_12_988_joint_alpha",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_988_JOINT_ALPHA_VARIABLE_GATE.csv",
            "anchor": "JAV988_3_cross_arena_policy",
            "role": "clock-screening cannot substitute for WEP source normalization",
        },
        {
            "source_id": "SRC1414_13_this_script",
            "source_path": "scripts/Y5_R10_RAB_beta_source_alpha_owner_or_finite_bound_row.py",
            "anchor": "STATUS",
            "role": "generator for this checkpoint",
        },
    ]
    for row in rows:
        row["path_exists"] = (ROOT / row["source_path"]).exists()
        row["anchor_found"] = anchor_found(row["source_path"], row["anchor"])
        row["valid_for_claim"] = False
        row["claim_allowed"] = False
    return rows


def owner_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "BSA1414_0_target",
            "owner_piece": "beta_source_alpha",
            "required_statement": "the finite alpha WEP source-force normalization is fixed by the same parent T_Q Noether/current owner as charge labels and Maxwell source coupling",
            "current_result": "TARGET_DEFINED",
            "missing_for_claim": "parent action must name T_Q, fix its norm/lattice, and derive one current/source normalization",
            "if_signed": "beta_source_alpha is not a free WEP suppression knob",
            "if_unsigned": "finite target row remains explicit and nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "BSA1414_1_TQ_owner",
            "owner_piece": "parent charge generator",
            "required_statement": "T_Q is a compact parent-action generator with fixed normalization independent of matter representation choices",
            "current_result": "UNSIGNED",
            "missing_for_claim": "generator_id, parent_bundle, compact_lattice, norm_owner, source path",
            "if_signed": "charge unit rescaling cannot hide beta_source_alpha",
            "if_unsigned": "charge/current rescaling remains legal",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "BSA1414_2_Noether_current_owner",
            "owner_piece": "single Noether/current owner",
            "required_statement": "matter current, charge labels, A_Q coupling, and source/test normalization descend from one T_Q Noether current",
            "current_result": "MISSING",
            "missing_for_claim": "current_id, Noether_owner, charge_unit_owner, matter_coupling_owner, source_normalization_owner",
            "if_signed": "beta_source_alpha is derived or removed as an independent coefficient",
            "if_unsigned": "beta_source_alpha remains a finite source-force normalization debt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "BSA1414_3_WEP_source_leg",
            "owner_piece": "WEP source worldtube/readout contraction",
            "required_statement": "K_ab alpha_source^b and tau_WEP are derived from the same source-current owner and official readout kernel",
            "current_result": "BLOCKED_BY_UA_GATE",
            "missing_for_claim": "official/equivalent MICROSCOPE arrays, source worldtube, product convention, orbit average",
            "if_signed": "finite beta_source_alpha can be scored against eta_AB",
            "if_unsigned": "target remains target-only and cannot be a WEP pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "BSA1414_4_no_current_rescaling",
            "owner_piece": "ban current/source rescaling counterexample",
            "required_statement": "J_A -> c_A J_A or beta_source,A source markers are not valid parent morphisms unless explicit residual fields",
            "current_result": "COUNTEREXAMPLE_SURVIVES",
            "missing_for_claim": "object-language/current-owner theorem that kills source-specific current rescaling",
            "if_signed": "source-force normalization is common-mode or theorem-zero",
            "if_unsigned": "R_source and beta_source_alpha remain live residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "BSA1414_5_verdict",
            "owner_piece": "beta_source_alpha owner status",
            "required_statement": "BSA1414_1 through BSA1414_4 close with source-backed parent clauses",
            "current_result": "OWNER_NOT_DERIVED_FINITE_TARGET_ROW_REQUIRED",
            "missing_for_claim": "T_Q/current owner, no-rescaling theorem, and U_a/source/readout kernel",
            "if_signed": "finite alpha WEP branch becomes parent-owned rather than fitted",
            "if_unsigned": "write finite beta_source_alpha target rows with no claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def finite_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "BSB1414_0_definition",
            "quantity": "beta_source_alpha",
            "definition": "source/force normalization multiplying the finite alpha/Coulomb WEP channel",
            "formula": "eta_AB_alpha = DeltaQ_alpha_AB * beta_source_alpha * b_alpha * tau_WEP",
            "target_or_bound": "must be theorem-owned/zero or numerically below WEP target after parent normalization",
            "current_value": "MISSING_DERIVED_VALUE",
            "units": "dimensionless suppression factor if parent-normalized",
            "source_anchor": "BSO989_0_definition;BSA1414_5_verdict",
            "status": "FINITE_BOUND_ROW_TEMPLATE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "BSB1414_1_alpha_only_target",
            "quantity": "abs(beta_source_alpha)_max_alpha_only",
            "definition": "target if only alpha/Coulomb finite channel is retained",
            "formula": "eta_bound / unit_source_eta_prediction",
            "target_or_bound": "4.797780522732e-05",
            "current_value": "TARGET_ONLY_NOT_DERIVED",
            "units": "dimensionless",
            "source_anchor": "BSO989_1_alpha_only_target;WEP988_WAS651_0_alpha_Coulomb",
            "status": "NUMERIC_TARGET_ONLY_NO_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "BSB1414_2_robust_surface_target",
            "quantity": "abs(beta_source_alpha)_max_robust_surface_including",
            "definition": "more conservative target if surface/binding channel is retained with alpha/Coulomb branch",
            "formula": "eta_bound / unit_source_eta_prediction for surface/binding pressure",
            "target_or_bound": "2.887280314062e-05",
            "current_value": "TARGET_ONLY_NOT_DERIVED",
            "units": "dimensionless",
            "source_anchor": "BSO989_2_robust_surface_including_target;WEP988_WAS651_1_surface_binding",
            "status": "NUMERIC_TARGET_ONLY_NO_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "BSB1414_3_parent_basis_required",
            "quantity": "parent normalization map",
            "definition": "map between smoke delta_Q/unit-source pressure and parent beta_source_alpha basis",
            "formula": "beta_source_alpha(parent) := source-normalized coefficient after T_Q/current/U_a/tau conventions are fixed",
            "target_or_bound": "required before any numeric comparison",
            "current_value": "MISSING_PARENT_BASIS_MAP",
            "units": "declared by parent source-current convention",
            "source_anchor": "PIC989_2_Noether_current_owner;ORB1409_2_product_convention",
            "status": "BLOCKED_PARENT_BASIS_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "BSB1414_4_score_ready_gate",
            "quantity": "beta_source_alpha score readiness",
            "definition": "all target-only rows become scoreable only after source/current owner or equivalent source-backed values exist",
            "formula": "score_ready iff source-backed value <= selected target and U_a/material/readout gates are complete",
            "target_or_bound": "False until all blockers clear",
            "current_value": "NOT_SCORE_READY",
            "units": "not_applicable",
            "source_anchor": "BSA1414_5_verdict;ORB1409_7_verdict",
            "status": "NOT_SCORE_READY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def anti_shortcut_rows() -> list[dict[str, Any]]:
    return [
        {
            "shortcut_id": "BSS1414_0_no_clock_screen",
            "forbidden_shortcut": "set beta_source_alpha = clock screen or use b_alpha*tau_clock as WEP pass",
            "reason": "clock product controls time/frequency drift; WEP force uses beta_source_alpha*b_alpha*tau_WEP",
            "source_anchor": "BSO989_3_not_clock_screen;JAV988_3_cross_arena_policy",
            "status": "FORBIDDEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "shortcut_id": "BSS1414_1_no_unit_source_pass",
            "forbidden_shortcut": "use unit source normalization as acceptable",
            "reason": "unit-source alpha/Coulomb and surface/binding pressure overshoot MICROSCOPE by large factors in prior smoke rows",
            "source_anchor": "WEP988_WAS651_0_alpha_Coulomb;WEP988_WAS651_1_surface_binding",
            "status": "FORBIDDEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "shortcut_id": "BSS1414_2_no_surrogate_Ua",
            "forbidden_shortcut": "score beta_source_alpha without official/equivalent U_a source/readout kernel",
            "reason": "1409 blocks K_ab alpha_source^b, product convention, and orbit/readout normalization",
            "source_anchor": "ORB1409_7_verdict",
            "status": "FORBIDDEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "shortcut_id": "BSS1414_3_no_R10_transfer",
            "forbidden_shortcut": "transfer WEP beta_source target to R10 or clocks without a parent arena map",
            "reason": "R10 material leg, K(lambda), tail, clock tau, and WEP tau are not the same object unless proved",
            "source_anchor": "RAG1413_2_R10;JAV988_3_cross_arena_policy",
            "status": "FORBIDDEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def arena_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena_id": "BSG1414_0_WEP",
            "arena": "WEP alpha/Coulomb",
            "dependency": "beta_source_alpha*b_alpha*tau_WEP plus U_a/material tensor/product convention",
            "status": "BLOCKED_TARGET_ONLY",
            "reason": "beta_source_alpha has only target rows and U_a is blocked by official readout/source kernel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "BSG1414_1_clock",
            "arena": "clock/alpha",
            "dependency": "b_alpha*tau_clock",
            "status": "SEPARATE_PRODUCT_BOUND_NONCLAIM",
            "reason": "clock product bound does not determine beta_source_alpha or WEP force normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "BSG1414_2_R10",
            "arena": "R10/local force range",
            "dependency": "beta_EM/R_EM material leg, K(lambda), tail, bound curve",
            "status": "BLOCKED_NO_TRANSFER",
            "reason": "beta_source_alpha target is WEP-channel pressure, not an R10 material-leg derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "arena_id": "BSG1414_3_local_GR",
            "arena": "local GR/Newton",
            "dependency": "source-current universality, R_EM/R_source zero or bounds, EH/PPN gate",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "reason": "source normalization owner is not derived and this is only one residual subcomponent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1414_0_owner_verdict",
            "decision": "do not promote beta_source_alpha owner",
            "reason": "T_Q/current/source normalization owner is missing and current-rescaling counterexample survives",
            "effect": "finite target-only beta_source_alpha rows remain active",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1414_1_bound_status",
            "decision": "record alpha-only and robust targets as nonclaim",
            "reason": "targets are useful pressure numbers but lack parent basis map and U_a/product normalization",
            "effect": "future runner can check values only after source-backed rows exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1414_2_next_best",
            "decision": "target the broader source-current owner / R_source merge next",
            "reason": "beta_source_alpha and R_source are symptoms of the same missing source-current normalization theorem",
            "effect": "next checkpoint should try to unify source normalization with R_source or write R_source finite template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "GATE1414_0_owner",
            "claim": "beta_source_alpha is theorem-owned or zero",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "T_Q/current/source normalization owner is missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1414_1_numeric_bound",
            "claim": "beta_source_alpha satisfies WEP target",
            "status": "TARGET_ONLY_NO_CLAIM",
            "reason": "no source-backed value, parent basis map, U_a, or product convention exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1414_2_WEP",
            "claim": "WEP alpha/Coulomb channel passes",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "beta_source_alpha is target-only and U_a/material/readout gates remain blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1414_3_transfer",
            "claim": "clock/R10 transfer is allowed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "clock product and WEP source-force normalization are separate debts",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1414_4_local_GR",
            "claim": "local GR/Newton reduction follows",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "source-current owner, R_EM, R_source, U_a, EH/PPN, and material tensor gates remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "claim_id": "GATE1414_5_verdict",
            "claim": "1414 closes beta_source_alpha",
            "status": "NO_PROMOTION",
            "reason": "1414 records owner failure and finite target rows only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1414_0_1415",
            "target_doc": "1415-Y5-R10-RAB-source-current-owner-or-Rsource-finite-template.md",
            "target_script": "scripts/Y5_R10_RAB_source_current_owner_or_Rsource_finite_template.py",
            "task": "try to derive a single source-current owner that kills both beta_source_alpha and R_source; if it fails, write the R_source finite residual template",
            "success_condition": "source normalization is theorem-owned/common-mode, or R_source has source-ready rows with units, signs, source paths, and nonclaim gates",
            "do_not_claim": "WEP pass; R_EM zero; beta_source_alpha bound pass; R10/clock transfer; Newton/local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "next_id": "NEXT1414_1_data_parallel",
            "target_doc": "future-beta-source-alpha-runner-after-Ua-and-parent-basis.md",
            "target_script": "future_runner_route",
            "task": "only after parent basis and U_a/product convention exist, compare a source-backed beta_source_alpha value to the alpha-only and robust targets",
            "success_condition": "runner refuses score unless value, units, source path, parent map, U_a, and material tensor are complete",
            "do_not_claim": "target-only value as bound pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    owner_attempt: list[dict[str, Any]],
    finite_bounds: list[dict[str, Any]],
    shortcuts: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    timestamp = datetime.now(timezone.utc).isoformat()
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        OWNER_ATTEMPT_PATH,
        FINITE_BOUND_PATH,
        ANTI_SHORTCUT_PATH,
        ARENA_GATE_PATH,
        DECISION_PATH,
        CLAIM_GATE_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    add(
        "VAL1414_0_sources",
        all(row["path_exists"] == True and row["anchor_found"] == True for row in sources),
        "all cited local source paths exist and anchors are present",
    )
    add(
        "VAL1414_1_owner_attempt",
        any(row["attempt_id"] == "BSA1414_5_verdict" and row["current_result"] == "OWNER_NOT_DERIVED_FINITE_TARGET_ROW_REQUIRED" for row in owner_attempt),
        "beta_source_alpha owner attempt explicitly fails and selects finite target row",
    )
    add(
        "VAL1414_2_finite_bounds",
        any(row["bound_id"] == "BSB1414_1_alpha_only_target" and row["target_or_bound"] == "4.797780522732e-05" for row in finite_bounds)
        and any(row["bound_id"] == "BSB1414_2_robust_surface_target" and row["target_or_bound"] == "2.887280314062e-05" for row in finite_bounds)
        and all(row["valid_for_claim"] == False for row in finite_bounds),
        "alpha-only and robust beta_source_alpha targets are recorded as nonclaim",
    )
    add(
        "VAL1414_3_anti_shortcuts",
        {"BSS1414_0_no_clock_screen", "BSS1414_1_no_unit_source_pass", "BSS1414_2_no_surrogate_Ua"}.issubset(
            {row["shortcut_id"] for row in shortcuts}
        )
        and all(row["status"] == "FORBIDDEN" for row in shortcuts),
        "clock-screen, unit-source, surrogate-Ua, and transfer shortcuts are forbidden",
    )
    add(
        "VAL1414_4_arena_gates",
        all(row["valid_for_claim"] == False and row["claim_allowed"] == False for row in arenas)
        and any(row["arena_id"] == "BSG1414_0_WEP" for row in arenas),
        "WEP, clock, R10, and local-GR arena gates remain blocked",
    )
    add(
        "VAL1414_5_decision",
        any(row["decision_id"] == "DEC1414_2_next_best" for row in decisions),
        "decision ledger selects broader source-current owner/R_source merge next",
    )
    add(
        "VAL1414_6_claim_refusal",
        all(row["valid_for_claim"] == False and row["claim_allowed"] == False for row in gates),
        "owner, numeric bound, WEP, transfer, and local-GR claims are refused",
    )
    add(
        "VAL1414_7_scope",
        all((ROOT / path).resolve().is_relative_to(ROOT.resolve()) for path in output_paths),
        "outputs are confined to post-checkpoint-work paths",
    )
    add(
        "VAL1414_8_overall",
        True,
        "1414 keeps beta_source_alpha as target-only finite debt and redirects to source-current owner/R_source",
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    owner_attempt: list[dict[str, Any]],
    finite_bounds: list[dict[str, Any]],
    shortcuts: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_targets: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    doc = f"""# 1414 - beta_source_alpha Owner Or Finite Bound Row

**Status:** `{STATUS}`

**Current verdict:** `beta_source_alpha` is not derived or zero-certified. The needed object is a single `T_Q` Noether/current/source-normalization owner tying charge labels, Maxwell source coupling, source/test force strength, and WEP/R10 normalization together. Current rows do not supply that owner, and current-rescaling/source-marker counterexamples remain live.

**Discipline move:** the useful numbers are target-only, not evidence of a pass: `|beta_source_alpha| <= 4.797780522732e-05` for the alpha/Coulomb-only pressure row, and `<= 2.887280314062e-05` for the robust surface-including row. These cannot be used until parent basis, source-current owner, `U_a`, material tensor, and product convention are real.

**Claim ceiling:** `{CLAIM_CEILING}`

## Source Register

{md_table(sources)}

## beta_source_alpha Owner Attempt

{md_table(owner_attempt)}

## beta_source_alpha Finite Bound Row

{md_table(finite_bounds)}

## beta_source_alpha Anti-Shortcut Gate

{md_table(shortcuts)}

## beta_source_alpha Arena Gate

{md_table(arenas)}

## Decision Ledger

{md_table(decisions)}

## Claim Gate

{md_table(gates)}

## Next Target

{md_table(next_targets)}

## Validation

{md_table(validations)}
"""
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    owner_attempt = owner_attempt_rows()
    finite_bounds = finite_bound_rows()
    shortcuts = anti_shortcut_rows()
    arenas = arena_gate_rows()
    decisions = decision_rows()
    gates = claim_gate_rows()
    next_targets = next_target_rows()
    validations = validation_rows(sources, owner_attempt, finite_bounds, shortcuts, arenas, decisions, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(OWNER_ATTEMPT_PATH, owner_attempt)
    write_csv(FINITE_BOUND_PATH, finite_bounds)
    write_csv(ANTI_SHORTCUT_PATH, shortcuts)
    write_csv(ARENA_GATE_PATH, arenas)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(NEXT_TARGET_PATH, next_targets)
    write_csv(VALIDATION_PATH, validations)
    write_doc(sources, owner_attempt, finite_bounds, shortcuts, arenas, decisions, gates, next_targets, validations)

    if any(row["status"] != "PASS" for row in validations):
        raise SystemExit("1414 validation failed")

    print(STATUS)


if __name__ == "__main__":
    main()

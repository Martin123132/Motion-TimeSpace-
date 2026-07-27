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

OUTPUT_DOC = POST_CHECKPOINT / "830-Y5-R10-Khat-boundary-owner-or-residual-vector-runner.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_830_SOURCE_REGISTER.csv"
KHAT_OWNER_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_830_KHAT_OWNER_AUDIT.csv"
RUNNER_INPUT_PATH = RESIDUALS / "P8_Y5_R10_830_RUNNER_INPUT_TEMPLATE.csv"
RUNNER_OUTPUT_PATH = RESIDUALS / "P8_Y5_R10_830_RUNNER_OUTPUT.csv"
OBSERVABLE_GATE_PATH = RESIDUALS / "P8_Y5_R10_830_OBSERVABLE_GATE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_830_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_830_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_830_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_830_VALIDATION.csv"

STATUS = "Y5_R10_830_Khat_owner_unsigned_runner_blocks_placeholders_nonclaim"
CLAIM_CEILING = "residual_vector_schema_and_missing_input_gate_only_no_local_GR_pass"
NEXT_TARGET = "831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md"

SOURCE_SPECS = [
    {
        "source_id": "829_doc",
        "path": POST_CHECKPOINT / "829-Y5-R10-baseline-lock-source-support-residual-budget.md",
        "needles": [
            "q_total <= q_quad + q_X2 + q_boundary + q_K",
            "OV829_1_PPN",
            "830-Y5-R10-Khat-boundary-owner-or-residual-vector-runner.md",
        ],
        "role": "immediate residual-budget handoff",
    },
    {
        "source_id": "829_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_829_VALIDATION.csv",
        "needles": [
            "V829_5_observable_vector_complete,pass",
            "V829_6_promotion_blocked,pass",
            "V829_11_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "799_transition_calculator",
        "path": POST_CHECKPOINT / "799-Y5-R10-transition-current-bound-calculator-and-source-support-powers.md",
        "needles": [
            "TBF799_4_epsilon_q",
            "TCP799_1_compare_all_local_arenas",
            "template_missing_parent_values",
        ],
        "role": "older exchange-current runner and all-arena gate",
    },
    {
        "source_id": "800_support_powers",
        "path": POST_CHECKPOINT / "800-Y5-R10-universal-XB-PiB-support-powers-or-Kperp-boundary-zero-lemma.md",
        "needles": [
            "KBL800_0_needed_operator",
            "KBL800_3_failure",
            "SPD800_5_verdict",
        ],
        "role": "Kperp/tensor-owner obstruction source",
    },
    {
        "source_id": "equation_register_local_ppn",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": [
            "local_ppn_branch_framework_defined",
            "delta_phi_fraction",
            "clock_delta_z",
        ],
        "role": "local PPN vector fields and readout obligations",
    },
    {
        "source_id": "equation_register_solar_open",
        "path": FORMALIZATION / "05-equation-register.md",
        "needles": [
            "The real Solar branch remains open until `q_loc(x)`, boundary data, and amplitude bounds are supplied.",
            "Local `q_loc` source-profile bound",
            "Source-support / boundary-amplitude law",
        ],
        "role": "local Solar branch remains open until source and boundary data exist",
    },
]

REQUIRED_NUMERIC_FIELDS = [
    "U_B",
    "pS",
    "L_cg_m",
    "L_tr_m",
    "L_X_m",
    "L_sys_m",
    "K_matter_00",
    "a_F_abs",
    "R_mm_abs",
    "C_X_abs",
    "A_B_abs",
    "pB",
    "q_K",
]
REQUIRED_SOURCE_FIELDS = [
    "response_matrix_path",
    "matter_descent_path",
    "boundary_source_path",
    "source_paths",
]
OBSERVABLE_ARENAS = ["exchange", "PPN", "R10", "clocks", "orbital", "WEP"]


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


def khat_owner_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "clause_id": "KO830_0_parent_tensor_operator",
            "clause": "Parent action must produce a local tensor boundary-value equation L_T K_hat = S_T.",
            "required_parent_object": "explicit second-variation or constraint operator on trace-free/local K_hat sector",
            "source_evidence": "800 has KBL800_0_needed_operator and KBL800_3_failure",
            "current_status": "missing_parent_operator",
            "proof_result": "not_derived",
            "local_effect": "q_K cannot be set to zero or bounded from geometry alone",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "KO830_1_boundary_conditions",
            "clause": "Boundary data must silence representative K_hat modes without deleting physical local curvature.",
            "required_parent_object": "regularity/decay/no-incoming boundary condition tied to the local branch",
            "source_evidence": "829 leaves q_boundary and q_K open",
            "current_status": "missing_boundary_owner",
            "proof_result": "not_derived",
            "local_effect": "boundary/local projection residue remains in the residual budget",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "KO830_2_no_zero_modes",
            "clause": "The K_hat operator must have no unsourced homogeneous modes in the observable local sector.",
            "required_parent_object": "coercivity, gauge fixing, or Fredholm/range condition for L_T",
            "source_evidence": "800 says scalar support cannot remove transverse homogeneous Kperp modes",
            "current_status": "missing_no_zero_mode_theorem",
            "proof_result": "not_derived",
            "local_effect": "PPN and orbital residuals could receive undetermined tensor response",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "KO830_3_source_orthogonality",
            "clause": "The remaining source must lie in the controlled/range sector of the K_hat operator.",
            "required_parent_object": "projection identity or Ward/Bianchi compatibility condition for S_T",
            "source_evidence": "829 keeps Bianchi/exchange and response matrices blocked",
            "current_status": "missing_range_condition",
            "proof_result": "not_derived",
            "local_effect": "exchange-current residual cannot be promoted to conservation-safe",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "KO830_4_matter_descent",
            "clause": "Matter must descend through the quotient so species read the same local metric/coframe.",
            "required_parent_object": "quotient-invariant matter action and coframe/connection descent",
            "source_evidence": "829 marks WEP/matter readout as missing_matter_descent",
            "current_status": "missing_matter_descent",
            "proof_result": "not_derived",
            "local_effect": "WEP and clock sectors cannot be claimed from the geometry residual alone",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "clause_id": "KO830_5_verdict",
            "clause": "K_hat owner theorem status for the local branch.",
            "required_parent_object": "all KO830_0..KO830_4 clauses signed by parent action",
            "source_evidence": "one or more clauses remain unsigned",
            "current_status": "owner_not_closed",
            "proof_result": "no_local_GR_claim",
            "local_effect": "use missing-input residual-vector runner only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def runner_input_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "template_missing_parent_values",
            "row_status": "blocked_missing_parent_inputs",
            "U_B": "MISSING_PARENT_INPUT",
            "pS": "MISSING_PARENT_INPUT",
            "L_cg_m": "MISSING_PARENT_INPUT",
            "L_tr_m": "MISSING_PARENT_INPUT",
            "L_X_m": "MISSING_PARENT_INPUT",
            "L_sys_m": "MISSING_PARENT_INPUT",
            "K_matter_00": "MISSING_PARENT_INPUT",
            "a_F_abs": "MISSING_PARENT_INPUT",
            "R_mm_abs": "MISSING_PARENT_INPUT",
            "C_X_abs": "MISSING_PARENT_INPUT",
            "A_B_abs": "MISSING_PARENT_INPUT",
            "pB": "MISSING_PARENT_INPUT",
            "q_K": "MISSING_PARENT_INPUT",
            "response_matrix_path": "MISSING_ARENA_PROJECTION",
            "matter_descent_path": "MISSING_PARENT_INPUT",
            "boundary_source_path": "MISSING_PARENT_INPUT",
            "source_paths": "MISSING_PARENT_INPUT",
            "numeric_ready": "false",
            "valid_for_claim": "false",
            "notes": "claim rows require real sourced local amplitudes, lengths, Khat owner, matter descent, and arena response matrices",
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


def run_residual_row(row: dict[str, object], generated_utc: str) -> dict[str, object]:
    missing_numeric = [field for field in REQUIRED_NUMERIC_FIELDS if as_float(row.get(field)) is None]
    missing_sources = [field for field in REQUIRED_SOURCE_FIELDS if is_missing(row.get(field))]
    missing = missing_numeric + missing_sources
    valid_for_claim = str(row.get("valid_for_claim")).lower() == "true"

    if missing:
        return {
            "row_id": row["row_id"],
            "runner_status": "blocked_missing_inputs",
            "q_quad": "MISSING_INPUT",
            "q_X2": "MISSING_INPUT",
            "q_boundary": "MISSING_INPUT",
            "q_K": "MISSING_INPUT",
            "q_total": "MISSING_INPUT",
            "epsilon_q": "MISSING_INPUT",
            "observable_vector_status": "not_evaluated",
            "passes_all": "false",
            "block_reason": "missing_fields:" + ";".join(missing),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }

    values = {field: as_float(row[field]) for field in REQUIRED_NUMERIC_FIELDS}
    assert all(value is not None for value in values.values())
    q_quad = abs(values["a_F_abs"] * values["R_mm_abs"]) * values["U_B"] ** (2 * values["pS"]) / (
        values["L_cg_m"] ** 2 * values["L_tr_m"]
    )
    q_X2 = values["C_X_abs"] * values["U_B"] ** (2 * values["pS"]) / (
        values["L_cg_m"] ** 2 * values["L_X_m"]
    )
    q_boundary = values["A_B_abs"] * values["U_B"] ** values["pB"] / (
        values["L_cg_m"] ** 2 * values["L_tr_m"]
    )
    q_total = q_quad + q_X2 + values["q_K"] + q_boundary
    epsilon_q = values["L_sys_m"] * q_total / values["K_matter_00"]
    block_reason = "row_valid_for_claim_false" if not valid_for_claim else "observable_response_not_implemented"

    return {
        "row_id": row["row_id"],
        "runner_status": "computed_nonclaim" if not valid_for_claim else "computed_awaiting_arena_response",
        "q_quad": f"{q_quad:.16e}",
        "q_X2": f"{q_X2:.16e}",
        "q_boundary": f"{q_boundary:.16e}",
        "q_K": f"{values['q_K']:.16e}",
        "q_total": f"{q_total:.16e}",
        "epsilon_q": f"{epsilon_q:.16e}",
        "observable_vector_status": "not_evaluated_without_response_matrix",
        "passes_all": "false",
        "block_reason": block_reason,
        "valid_for_claim": "false",
        "generated_utc": generated_utc,
    }


def observable_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "gate_id": "OG830_0_exchange",
            "arena": "exchange",
            "required_input": "epsilon_q tolerance, K_matter_00, q_total, Bianchi/Ward compatibility",
            "current_status": "missing_parent_inputs",
            "pass_condition": "epsilon_q below sourced tolerance and Ward/Bianchi residual signed",
            "block_reason": "missing_parent_inputs",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "OG830_1_PPN",
            "arena": "PPN",
            "required_input": "response matrix from q_total and K_hat to delta_gamma, delta_beta, alpha1, alpha2, xi",
            "current_status": "missing_response_matrix",
            "pass_condition": "all PPN components are source-backed and below observational bounds",
            "block_reason": "missing_arena_projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "OG830_2_R10",
            "arena": "R10",
            "required_input": "map q_total/K_hat to alpha(lambda) with sourced lambda and bound curve",
            "current_status": "missing_response_matrix",
            "pass_condition": "abs(alpha_predicted)<=alpha_bound(lambda) with sourced coefficients",
            "block_reason": "missing_arena_projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "OG830_3_clocks",
            "arena": "clocks",
            "required_input": "metric/coframe response to clock_delta_z and local redshift residual",
            "current_status": "missing_response_matrix",
            "pass_condition": "clock_delta_z is source-backed and below clock/redshift bounds",
            "block_reason": "missing_arena_projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "OG830_4_orbital",
            "arena": "orbital",
            "required_input": "ephemeris/perihelion/range response vector from local metric perturbation",
            "current_status": "missing_response_matrix",
            "pass_condition": "orbital residual vector is source-backed and below arena bounds",
            "block_reason": "missing_arena_projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "OG830_5_WEP",
            "arena": "WEP",
            "required_input": "matter descent or species-coupling vector eta_AB",
            "current_status": "missing_matter_descent",
            "pass_condition": "matter action descends species-independently or eta_AB is bounded",
            "block_reason": "missing_parent_inputs",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D830_0",
            "finding": "K_hat owner theorem is not derived",
            "reason": "parent tensor operator, boundary conditions, no-zero-mode theorem, range condition, and matter descent remain unsigned",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D830_1",
            "finding": "residual-vector runner exists but refuses placeholders",
            "reason": "template rows with MISSING_PARENT_INPUT or MISSING_ARENA_PROJECTION cannot produce a pass",
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
            "objective": "attempt a parent-derived K_hat tensor operator with boundary/no-zero-mode clauses, or explicitly demote the local branch to closure-only",
            "include": "derive L_T K_hat=S_T, boundary data, coercivity/range condition, matter descent interface, and response-vector inputs",
            "exclude": "local-GR claim, numeric PPN/R10 pass with placeholders, data fitting, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "Khat owner audit and hard residual-vector missing-input gate added",
            "what_is_not_claimed": "local GR, PPN pass, R10 pass, clock/orbital/WEP pass, or Khat zero theorem",
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
    owner_rows: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    runner_outputs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_829_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    verdict_rows = [row for row in owner_rows if row["clause_id"] == "KO830_5_verdict"]
    owner_not_derived = bool(verdict_rows) and verdict_rows[0]["proof_result"] == "no_local_GR_claim"
    missing_template_blocks = any(
        row["row_id"] == "template_missing_parent_values"
        and row["runner_status"] == "blocked_missing_inputs"
        and row["passes_all"] == "false"
        for row in runner_outputs
    )
    no_missing_passes = not any(
        row["passes_all"] == "true" and "missing_fields" in row["block_reason"] for row in runner_outputs
    )
    gate_arenas = {row["arena"] for row in gates}
    gates_complete = set(OBSERVABLE_ARENAS).issubset(gate_arenas)
    nonclaim_ok = all_valid_for_claim_false(
        [source_rows, owner_rows, runner_inputs, runner_outputs, gates, decisions, next_targets, nonclaim]
    )
    no_claim = (
        not any(row["passes_all"] == "true" for row in runner_outputs)
        and not any(row["claim_allowed"] == "true" for row in decisions)
    )
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    rows = [
        {
            "check_id": "V830_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V830_1_prior_829_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V830_2_khat_owner_not_derived",
            "result": "pass" if owner_not_derived else "fail",
            "detail": "Khat owner theorem remains unsigned and nonclaim",
        },
        {
            "check_id": "V830_3_runner_template_blocks_missing",
            "result": "pass" if missing_template_blocks else "fail",
            "detail": "template_missing_parent_values is blocked before numeric use",
        },
        {
            "check_id": "V830_4_no_missing_input_passes",
            "result": "pass" if no_missing_passes else "fail",
            "detail": "no row with missing fields passes",
        },
        {
            "check_id": "V830_5_observable_gates_complete",
            "result": "pass" if gates_complete else "fail",
            "detail": "exchange, PPN, R10, clocks, orbital, and WEP gates are present",
        },
        {
            "check_id": "V830_6_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V830_7_no_data_or_local_GR_claim",
            "result": "pass" if no_claim else "fail",
            "detail": "no data, local-GR, PPN, R10, clock, orbital, or WEP pass selected",
        },
        {
            "check_id": "V830_8_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V830_9_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V830_10_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]
    return rows


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
    owner_rows: list[dict[str, object]],
    runner_inputs: list[dict[str, object]],
    runner_outputs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 830 - Y5 R10 Khat Boundary Owner Or Residual-Vector Runner",
        "",
        "Current result: **the Khat/boundary owner theorem is still unsigned, so 830 adds a hard residual-vector gate rather than a local-GR claim**. The runner refuses rows with `MISSING_PARENT_INPUT`, `MISSING_ARENA_PROJECTION`, or absent source paths, and keeps every output non-claim until parent coefficients and arena response matrices exist.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
        "",
        "## Khat Owner Audit",
        "",
        csv_table(owner_rows, ["clause_id", "clause", "current_status", "proof_result", "local_effect", "valid_for_claim"]),
        "",
        "## Runner Input Template",
        "",
        csv_table(runner_inputs, ["row_id", "row_status", "U_B", "L_cg_m", "response_matrix_path", "numeric_ready", "valid_for_claim", "notes"]),
        "",
        "## Runner Output",
        "",
        csv_table(runner_outputs, ["row_id", "runner_status", "q_total", "epsilon_q", "observable_vector_status", "passes_all", "block_reason", "valid_for_claim"]),
        "",
        "## Observable Gates",
        "",
        csv_table(gates, ["gate_id", "arena", "current_status", "pass_condition", "block_reason", "valid_for_claim"]),
        "",
        "## Decision",
        "",
        csv_table(decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        csv_table(next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
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
    owner_rows = khat_owner_audit_rows(generated_utc)
    runner_inputs = runner_input_rows(generated_utc)
    runner_outputs = [run_residual_row(row, generated_utc) for row in runner_inputs]
    gates = observable_gate_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, owner_rows, runner_inputs, runner_outputs, gates, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(
        KHAT_OWNER_AUDIT_PATH,
        owner_rows,
        ["clause_id", "clause", "required_parent_object", "source_evidence", "current_status", "proof_result", "local_effect", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RUNNER_INPUT_PATH,
        runner_inputs,
        [
            "row_id",
            "row_status",
            "U_B",
            "pS",
            "L_cg_m",
            "L_tr_m",
            "L_X_m",
            "L_sys_m",
            "K_matter_00",
            "a_F_abs",
            "R_mm_abs",
            "C_X_abs",
            "A_B_abs",
            "pB",
            "q_K",
            "response_matrix_path",
            "matter_descent_path",
            "boundary_source_path",
            "source_paths",
            "numeric_ready",
            "valid_for_claim",
            "notes",
            "generated_utc",
        ],
    )
    write_csv(
        RUNNER_OUTPUT_PATH,
        runner_outputs,
        ["row_id", "runner_status", "q_quad", "q_X2", "q_boundary", "q_K", "q_total", "epsilon_q", "observable_vector_status", "passes_all", "block_reason", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OBSERVABLE_GATE_PATH,
        gates,
        ["gate_id", "arena", "required_input", "current_status", "pass_condition", "block_reason", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        DECISION_PATH,
        decisions,
        ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        NEXT_TARGET_PATH,
        next_targets,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        NONCLAIM_SUMMARY_PATH,
        nonclaim,
        ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, owner_rows, runner_inputs, runner_outputs, gates, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()

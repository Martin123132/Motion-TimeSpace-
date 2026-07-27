from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1204"
TITLE = "1204-Y5-R10-boundary-projector-zero-or-finite-amplitude-bound"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
ZERO_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_BOUNDARY_PROJECTOR_ZERO_ATTEMPT.csv"
FINITE_TARGETS_PATH = OUT_DIR / f"{PACK_ID}_BOUNDARY_PROJECTOR_FINITE_TARGETS.csv"
EPSILON_TARGETS_PATH = OUT_DIR / f"{PACK_ID}_PROJECTOR_EPSILON_TARGETS.csv"
SOURCE_SCHEMA_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_READY_BOUND_ROWS.csv"
COMPARISON_PATH = OUT_DIR / f"{PACK_ID}_COMPARISON_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1204_VALIDATION.csv"


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = ROOT / relative_path
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def fmt(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def md_escape(value: object) -> str:
    return fmt(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1204_0_1203_next",
            "local_path": "1203-Y5-R10-qDT-component-amplitude-law-against-conservative-envelope.md",
            "needle": "NEXT1203_0_1204",
            "purpose": "handoff to boundary/projector zero-or-finite-bound attack",
        },
        {
            "source_id": "SRC1204_1_1203_thresholds",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1203_SCENARIO_PRESSURE_THRESHOLDS.csv",
            "needle": "THR1203_WR10F1202_2_brutal_100x",
            "purpose": "scenario amplitude thresholds for q_DT",
        },
        {
            "source_id": "SRC1204_2_1196_boundary",
            "local_path": "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md",
            "needle": "BP1196_0_tracefree_adjoint_boundary",
            "purpose": "explicit D_T adjoint boundary pairing and trace bound",
        },
        {
            "source_id": "SRC1204_3_1196_projector",
            "local_path": "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md",
            "needle": "CKZ1196_3_projector_perturbation_bound",
            "purpose": "projector leakage absorption condition C0 eps_P<1",
        },
        {
            "source_id": "SRC1204_4_1198_no_go",
            "local_path": "1198-Y5-R10-DT-parent-anchor-source-or-first-real-bound-input-fill.md",
            "needle": "DTA1198_5_verdict",
            "purpose": "generic natural-boundary shortcut rejected",
        },
        {
            "source_id": "SRC1204_5_1019_exactness",
            "local_path": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "needle": "BE1019_6_verdict",
            "purpose": "boundary exactness remains unsigned",
        },
        {
            "source_id": "SRC1204_6_1019_projector",
            "local_path": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "needle": "PO1019_5_verdict",
            "purpose": "projector orthogonality remains unsigned",
        },
        {
            "source_id": "SRC1204_7_1170_no_flux",
            "local_path": "1170-Y5-R10-topological-selector-boundary-flux-certificate-or-BC-primitive-owner.md",
            "needle": "PBC1170_1_no_flux_condition",
            "purpose": "no-flux condition as a sufficient but unsigned route",
        },
        {
            "source_id": "SRC1204_8_1200_components",
            "local_path": "1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md",
            "needle": "QPE1200_4_projector_component",
            "purpose": "q_projector component definition",
        },
    ]

    source_rows: list[dict[str, object]] = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_rows.append(
            {
                **spec,
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    threshold_path = OUT_DIR / "P8_Y5_R10_1203_SCENARIO_PRESSURE_THRESHOLDS.csv"
    thresholds = load_csv(threshold_path)
    for row in thresholds:
        row["_q"] = float(row["qDT_allowed_min"])
        row["_w"] = float(row["W_R10_assumed"])
    global_tight = min(thresholds, key=lambda row: row["_q"])

    zero_attempts = [
        {
            "zero_id": "ZBP1204_0_boundary_no_flux",
            "target_component": "q_boundary=||B_T||",
            "sufficient_condition": "pullback(P_loc V)=0 for all admissible adjoint test fields or n_mu K_T^(mu nu)=0 on partialD",
            "derivation": "B_T[V,K_T]=int_partialD n_mu K_T^(mu nu)(P_loc V)_nu dS, so either factor vanishing kills the pairing.",
            "current_parent_status": "NOT_PARENT_SIGNED",
            "failure_reason": "1198 shows the generic natural boundary condition controls residual momentum, not the needed K_T boundary contraction.",
            "finite_fallback": "||B_T|| <= ||n.K_T||_{H-1/2(partialD)} ||P_loc V||_{H1/2(partialD)}",
            "result": "CONDITIONAL_ZERO_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "zero_id": "ZBP1204_1_projector_exact_silence",
            "target_component": "q_projector=||Delta_P||",
            "sufficient_condition": "nabla P_loc=0, boundary pullback(P_loc) fixed/silent, and coframe/domain motion has no tracefree D_T projection",
            "derivation": "Delta_P is precisely the collection of derivative/projector/coframe/domain-motion leakage terms; if each source term is parent-silent, Delta_P=0.",
            "current_parent_status": "NOT_PARENT_SIGNED",
            "failure_reason": "1019/678 keep projector orthogonality and projector-stress silence conditional rather than signed.",
            "finite_fallback": "||Delta_P|| <= eps_P ||G_res|| or a direct source-bounded Delta_P_norm row",
            "result": "CONDITIONAL_ZERO_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "zero_id": "ZBP1204_2_projector_absorption",
            "target_component": "q_projector absorbed into D_T range theorem",
            "sufficient_condition": "||Delta_P[V]|| <= eps_P ||V||_H1 and C_CK eps_P < 1 in the same local domain/norm",
            "derivation": "Move the projector perturbation to the left side of the anchored CK/Korn inequality; smallness absorbs it.",
            "current_parent_status": "MISSING_C_CK_AND_EPS_P",
            "failure_reason": "no numeric/source-backed C_CK or eps_P exists in the current corpus",
            "finite_fallback": "if absorption is not proved, carry q_projector=eps_P||G_res|| as a positive term",
            "result": "ABSORPTION_CONTRACT_WRITTEN_NOT_CLOSED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "zero_id": "ZBP1204_3_no_shortcut_guard",
            "target_component": "boundary/projector route",
            "sufficient_condition": "same parent action owns boundary class, quotient, P_loc, coframe, source measure, and local arena readout",
            "derivation": "Different boundary/projector domains cannot be patched together without breaking covariance or deleting physical charges.",
            "current_parent_status": "GUARD_ACTIVE",
            "failure_reason": "prevents imposing artificial boundary silence that would also erase physical mass/time/rotation charges",
            "finite_fallback": "retain explicit q_boundary and q_projector rows until one parent-owned domain signs them",
            "result": "NO_CHEAP_BOUNDARY_OR_PROJECTOR_PASS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_targets: list[dict[str, object]] = []
    for row in sorted(thresholds, key=lambda item: item["_w"]):
        q_allowed = float(row["qDT_allowed_min"])
        finite_targets.extend(
            [
                {
                    "target_id": f"FBP1204_{row['scenario_id']}_boundary_only",
                    "scenario_id": row["scenario_id"],
                    "W_R10_assumed": row["W_R10_assumed"],
                    "qDT_allowed_min": q_allowed,
                    "active_terms_assumed": "only q_boundary live; q_coker=q_regularizer=q_projector=0",
                    "q_boundary_max": q_allowed,
                    "q_projector_max": 0.0,
                    "combined_boundary_projector_max": q_allowed,
                    "pass_condition": "||B_T|| <= qDT_allowed_min",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                },
                {
                    "target_id": f"FBP1204_{row['scenario_id']}_projector_only",
                    "scenario_id": row["scenario_id"],
                    "W_R10_assumed": row["W_R10_assumed"],
                    "qDT_allowed_min": q_allowed,
                    "active_terms_assumed": "only q_projector live; q_coker=q_regularizer=q_boundary=0",
                    "q_boundary_max": 0.0,
                    "q_projector_max": q_allowed,
                    "combined_boundary_projector_max": q_allowed,
                    "pass_condition": "||Delta_P|| <= qDT_allowed_min",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                },
                {
                    "target_id": f"FBP1204_{row['scenario_id']}_boundary_projector_split",
                    "scenario_id": row["scenario_id"],
                    "W_R10_assumed": row["W_R10_assumed"],
                    "qDT_allowed_min": q_allowed,
                    "active_terms_assumed": "q_boundary and q_projector live equally; q_coker=q_regularizer=0",
                    "q_boundary_max": q_allowed / 2.0,
                    "q_projector_max": q_allowed / 2.0,
                    "combined_boundary_projector_max": q_allowed,
                    "pass_condition": "||B_T|| + ||Delta_P|| <= qDT_allowed_min",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                },
                {
                    "target_id": f"FBP1204_{row['scenario_id']}_four_way_budget",
                    "scenario_id": row["scenario_id"],
                    "W_R10_assumed": row["W_R10_assumed"],
                    "qDT_allowed_min": q_allowed,
                    "active_terms_assumed": "all four q_DT terms live equally",
                    "q_boundary_max": q_allowed / 4.0,
                    "q_projector_max": q_allowed / 4.0,
                    "combined_boundary_projector_max": q_allowed / 2.0,
                    "pass_condition": "each q_DT component <= qDT_allowed_min/4",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                },
            ]
        )

    epsilon_targets: list[dict[str, object]] = []
    g_norm_scenarios = [0.1, 1.0, 10.0, 100.0]
    for row in sorted(thresholds, key=lambda item: item["_w"]):
        q_allowed = float(row["qDT_allowed_min"])
        for g_norm in g_norm_scenarios:
            epsilon_targets.append(
                {
                    "epsilon_target_id": f"EPT1204_{row['scenario_id']}_G{fmt(g_norm).replace('.', 'p')}",
                    "scenario_id": row["scenario_id"],
                    "W_R10_assumed": row["W_R10_assumed"],
                    "qDT_allowed_min": q_allowed,
                    "assumed_G_res_norm": g_norm,
                    "eps_P_max_if_projector_only": q_allowed / g_norm,
                    "eps_P_max_if_boundary_projector_equal_split": (q_allowed / 2.0) / g_norm,
                    "absorption_extra_requirement": "C_CK*eps_P < 1",
                    "status": "EPSILON_TARGET_ONLY_G_RES_AND_C_CK_NOT_SOURCED",
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )

    source_ready_rows = [
        {
            "schema_id": "SBR1204_0_boundary_zero_certificate",
            "row_type": "zero_certificate",
            "component": "q_boundary",
            "required_columns": "domain_id;boundary_class;condition_type;proof_source_path;physical_charge_guard;sign_convention;valid_for_claim",
            "acceptance_rule": "proof_source_path exists and proves pullback(P_loc V)=0 or n.K_T=0 without deleting physical charges",
            "current_status": "MISSING_PARENT_ZERO_CERTIFICATE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "SBR1204_1_boundary_finite_bound",
            "row_type": "finite_bound",
            "component": "q_boundary",
            "required_columns": "domain_id;boundary_geometry_path;K_T_normal_trace_norm;P_locV_trace_norm;trace_pairing_bound;units;source_path;valid_for_claim",
            "acceptance_rule": "trace_pairing_bound numeric nonnegative and <= selected q_boundary_max with all source paths real",
            "current_status": "SOURCE_READY_ROW_NOT_FILLED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "SBR1204_2_projector_zero_certificate",
            "row_type": "zero_certificate",
            "component": "q_projector",
            "required_columns": "domain_id;P_loc_definition_path;coframe_lock_path;domain_motion_path;projector_stress_path;zero_proof_source_path;valid_for_claim",
            "acceptance_rule": "same parent domain proves nablaP/coframe/domain-motion/projector-stress silence",
            "current_status": "MISSING_PARENT_ZERO_CERTIFICATE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "schema_id": "SBR1204_3_projector_finite_bound",
            "row_type": "finite_bound",
            "component": "q_projector",
            "required_columns": "domain_id;Delta_P_norm;eps_P;G_res_norm;C_CK;C_CK_eps_P;units;source_path;valid_for_claim",
            "acceptance_rule": "Delta_P_norm or eps_P*G_res_norm numeric; if using absorption then C_CK*eps_P<1",
            "current_status": "SOURCE_READY_ROW_NOT_FILLED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    comparison_rows = [
        {
            "comparison_id": "CMP1204_0_current",
            "q_boundary": "MISSING",
            "q_projector": "MISSING",
            "threshold_used": global_tight["threshold_id"],
            "threshold_value": global_tight["qDT_allowed_min"],
            "comparison_status": "BLOCKED_MISSING_BOUNDARY_AND_PROJECTOR_AMPLITUDES",
            "interpretation": "1204 derives exact zero/finite-bound contracts but no numeric component is filled.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "comparison_id": "CMP1204_1_both_zero_conditional",
            "q_boundary": "0",
            "q_projector": "0",
            "threshold_used": global_tight["threshold_id"],
            "threshold_value": global_tight["qDT_allowed_min"],
            "comparison_status": "CONDITIONAL_HELPFUL_IF_PARENT_SIGNED",
            "interpretation": "If both terms are theorem-zero, the remaining R10 pressure moves to q_coker and q_regularizer only.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "comparison_id": "CMP1204_2_equal_split_target",
            "q_boundary": float(global_tight["qDT_allowed_min"]) / 2.0,
            "q_projector": float(global_tight["qDT_allowed_min"]) / 2.0,
            "threshold_used": global_tight["threshold_id"],
            "threshold_value": global_tight["qDT_allowed_min"],
            "comparison_status": "NONCLAIM_TARGET_ONLY",
            "interpretation": "If only boundary and projector are live, each must be below half the harsh threshold.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1204_0_boundary_zero_or_bound",
            "gate": "q_boundary zero certificate or finite numeric bound",
            "status": "BLOCKED",
            "reason": "no parent-signed boundary zero certificate and no finite trace norm bound row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1204_1_projector_zero_or_bound",
            "gate": "q_projector zero/absorption certificate or finite numeric bound",
            "status": "BLOCKED",
            "reason": "no parent-signed projector silence and no eps_P/Delta_P/C_CK numeric row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1204_2_same_domain_guard",
            "gate": "same parent-owned local domain",
            "status": "ACTIVE_GUARD",
            "reason": "boundary and projector silence cannot be borrowed from different domains or quotient choices",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1204_3_R10_claim",
            "gate": "R10/local-GR pass",
            "status": "BLOCKED",
            "reason": "1204 creates target inequalities only; no component value is claim-ready",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC1204_0_verdict",
            "condition": "boundary/projector zero route has clean sufficient conditions but no parent signature",
            "decision": "retain theorem-zero route as conditional and use finite-bound targets for the next input fill",
            "result": f"harsh W=100 target requires ||B_T||+||Delta_P|| <= {fmt(global_tight['qDT_allowed_min'])} if coker and regularizer are zero",
            "next_action": "try to fill one source-ready row: either B_T trace-bound row or projector eps_P/C_CK absorption row",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    next_rows = [
        {
            "next_id": "NEXT1204_0_1205",
            "target_file": "1205-Y5-R10-first-BT-or-epsP-source-row-fill.md",
            "target_script": "scripts/Y5_R10_first_BT_or_epsP_source_row_fill.py",
            "task": "fill the first nonclaim source-ready finite row for either ||B_T|| or eps_P/C_CK/Delta_P, then compare it to the 1204 harsh and split targets",
            "success_condition": "one boundary/projector component has a real source path plus numeric nonnegative value, or a stricter blocker ledger proving why it cannot be sourced yet",
            "do_not_do": "do not claim R10 pass, do not use generic natural boundary wording as B_T=0, do not mix domains, do not edit formalization-workbench, do not push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_fields = ["source_id", "local_path", "needle", "purpose", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"]
    zero_fields = ["zero_id", "target_component", "sufficient_condition", "derivation", "current_parent_status", "failure_reason", "finite_fallback", "result", "valid_for_claim", "claim_allowed"]
    finite_fields = ["target_id", "scenario_id", "W_R10_assumed", "qDT_allowed_min", "active_terms_assumed", "q_boundary_max", "q_projector_max", "combined_boundary_projector_max", "pass_condition", "valid_for_claim", "claim_allowed"]
    epsilon_fields = ["epsilon_target_id", "scenario_id", "W_R10_assumed", "qDT_allowed_min", "assumed_G_res_norm", "eps_P_max_if_projector_only", "eps_P_max_if_boundary_projector_equal_split", "absorption_extra_requirement", "status", "valid_for_claim", "claim_allowed"]
    schema_fields = ["schema_id", "row_type", "component", "required_columns", "acceptance_rule", "current_status", "valid_for_claim", "claim_allowed"]
    comparison_fields = ["comparison_id", "q_boundary", "q_projector", "threshold_used", "threshold_value", "comparison_status", "interpretation", "valid_for_claim", "claim_allowed"]
    gate_fields = ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]
    decision_fields = ["decision_id", "condition", "decision", "result", "next_action", "valid_for_claim", "claim_allowed"]
    next_fields = ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"]

    write_csv(SOURCE_REGISTER_PATH, source_rows, source_fields)
    write_csv(ZERO_ATTEMPT_PATH, zero_attempts, zero_fields)
    write_csv(FINITE_TARGETS_PATH, finite_targets, finite_fields)
    write_csv(EPSILON_TARGETS_PATH, epsilon_targets, epsilon_fields)
    write_csv(SOURCE_SCHEMA_PATH, source_ready_rows, schema_fields)
    write_csv(COMPARISON_PATH, comparison_rows, comparison_fields)
    write_csv(CLAIM_GATES_PATH, claim_gates, gate_fields)
    write_csv(DECISION_LEDGER_PATH, decision_rows, decision_fields)
    write_csv(NEXT_TARGET_PATH, next_rows, next_fields)

    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if mtime >= RUN_STARTED_UTC:
                    formalization_recent.append(path)

    csvs_to_parse = [
        SOURCE_REGISTER_PATH,
        ZERO_ATTEMPT_PATH,
        FINITE_TARGETS_PATH,
        EPSILON_TARGETS_PATH,
        SOURCE_SCHEMA_PATH,
        COMPARISON_PATH,
        CLAIM_GATES_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
    ]
    csv_parse_ok = True
    parse_details: list[str] = []
    for csv_path in csvs_to_parse:
        try:
            rows = load_csv(csv_path)
            parse_details.append(f"{csv_path.name}:{len(rows)}")
        except Exception as exc:  # noqa: BLE001
            csv_parse_ok = False
            parse_details.append(f"{csv_path.name}:ERROR:{exc}")

    all_sources_exist = all(bool(row["path_exists"]) for row in source_rows)
    all_needles_found = all(bool(row["needle_found"]) for row in source_rows)
    zero_not_claimed = all(row["result"] != "CLAIMED_ZERO" and not bool(row["valid_for_claim"]) for row in zero_attempts)
    finite_targets_positive = all(float(row["combined_boundary_projector_max"]) >= 0 and float(row["qDT_allowed_min"]) > 0 for row in finite_targets)
    harsh_split = [
        row for row in finite_targets
        if row["scenario_id"] == "WR10F1202_2_brutal_100x" and row["target_id"].endswith("_boundary_projector_split")
    ][0]
    harsh_split_matches = abs(float(harsh_split["q_boundary_max"]) - float(global_tight["qDT_allowed_min"]) / 2.0) < 1e-16
    epsilon_positive = all(float(row["eps_P_max_if_projector_only"]) > 0 and float(row["eps_P_max_if_boundary_projector_equal_split"]) > 0 for row in epsilon_targets)
    schema_rows_present = len(source_ready_rows) == 4
    comparison_blocked = comparison_rows[0]["comparison_status"] == "BLOCKED_MISSING_BOUNDARY_AND_PROJECTOR_AMPLITUDES"
    claim_policy_ok = all(
        not bool(row.get("valid_for_claim")) and not bool(row.get("claim_allowed"))
        for row in zero_attempts + finite_targets + epsilon_targets + source_ready_rows + comparison_rows + claim_gates
    )
    formalization_untouched = len(formalization_recent) == 0

    validation_rows = [
        validation_row("VAL1204_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"),
        validation_row("VAL1204_1_needles_found", "all cited source needles found", all_needles_found, f"{sum(bool(row['needle_found']) for row in source_rows)}/{len(source_rows)} needles found"),
        validation_row("VAL1204_2_zero_not_claimed", "zero theorem attempts remain conditional", zero_not_claimed, "no boundary/projector zero is promoted"),
        validation_row("VAL1204_3_finite_targets_positive", "finite boundary/projector targets are numeric positive", finite_targets_positive, f"finite_target_rows={len(finite_targets)}"),
        validation_row("VAL1204_4_harsh_split_matches", "harsh boundary/projector split target matches 1203 threshold/2", harsh_split_matches, f"split={fmt(harsh_split['q_boundary_max'])};threshold={fmt(global_tight['qDT_allowed_min'])}"),
        validation_row("VAL1204_5_epsilon_targets_positive", "projector epsilon targets are positive", epsilon_positive, f"epsilon_rows={len(epsilon_targets)}"),
        validation_row("VAL1204_6_source_schema_present", "source-ready boundary/projector row schemas present", schema_rows_present, f"schema_rows={len(source_ready_rows)}"),
        validation_row("VAL1204_7_current_comparison_blocked", "current comparison does not claim a pass", comparison_blocked, comparison_rows[0]["comparison_status"]),
        validation_row("VAL1204_8_nonclaim_policy", "all generated rows remain nonclaim", claim_policy_ok, "valid_for_claim=false and claim_allowed=false throughout"),
        validation_row("VAL1204_9_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parse_details)),
        validation_row("VAL1204_10_formalization_untouched", "formalization-workbench untouched during run", formalization_untouched, f"formalization_recent_after_run_start_count={len(formalization_recent)}"),
    ]
    validation_pass = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1204_11_overall",
            "overall 1204 validation",
            validation_pass,
            "1204 boundary/projector zero-or-finite-bound gates are reproducible" if validation_pass else "one or more validation checks failed",
        )
    )
    validation_fields = ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"]
    write_csv(VALIDATION_PATH, validation_rows, validation_fields)

    doc = f"""# 1204 Y5/R10 Boundary Projector Zero Or Finite Amplitude Bound

**Current verdict:** 1204 does not prove `q_boundary=0` or `q_projector=0`, but it turns both into exact gates. The clean sufficient zero conditions are written, the no-shortcut guard is active, and the finite amplitude targets are now executable against the 1203 threshold.

**Main progress:** under the harsh private `W_R10=100` stress target, if `q_coker=q_regularizer=0`, then `||B_T||+||Delta_P|| <= {fmt(global_tight['qDT_allowed_min'])}` is required; an equal boundary/projector split gives each term `{fmt(float(global_tight['qDT_allowed_min']) / 2.0)}`.

## Source Register

{markdown_table(source_rows, source_fields)}

## Boundary Projector Zero Attempt

{markdown_table(zero_attempts, zero_fields)}

## Boundary Projector Finite Targets

{markdown_table(finite_targets, finite_fields)}

## Projector Epsilon Targets

{markdown_table(epsilon_targets, epsilon_fields)}

## Source Ready Bound Rows

{markdown_table(source_ready_rows, schema_fields)}

## Comparison Ledger

{markdown_table(comparison_rows, comparison_fields)}

## Claim Gates

{markdown_table(claim_gates, gate_fields)}

## Decision Ledger

{markdown_table(decision_rows, decision_fields)}

## Next Target

{markdown_table(next_rows, next_fields)}

## Validation

{markdown_table(validation_rows, validation_fields)}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"validation_pass={validation_pass}")
    print(f"harsh_boundary_projector_sum_target={fmt(global_tight['qDT_allowed_min'])}")
    print(f"harsh_equal_split_each={fmt(float(global_tight['qDT_allowed_min']) / 2.0)}")


if __name__ == "__main__":
    main()

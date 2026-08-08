from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1203"
TITLE = "1203-Y5-R10-qDT-component-amplitude-law-against-conservative-envelope"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
AMPLITUDE_LAW_PATH = OUT_DIR / f"{PACK_ID}_AMPLITUDE_LAW.csv"
SCENARIO_THRESHOLDS_PATH = OUT_DIR / f"{PACK_ID}_SCENARIO_PRESSURE_THRESHOLDS.csv"
COMPONENT_STATUS_PATH = OUT_DIR / f"{PACK_ID}_COMPONENT_BOUND_STATUS.csv"
ALLOCATION_TARGETS_PATH = OUT_DIR / f"{PACK_ID}_COMPONENT_ALLOCATION_TARGETS.csv"
SYMBOLIC_COMPARISON_PATH = OUT_DIR / f"{PACK_ID}_SYMBOLIC_COMPARISON.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1203_VALIDATION.csv"


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
            "source_id": "SRC1203_0_1202_next",
            "local_path": "1202-Y5-R10-conservative-geometry-kernel-or-qDT-profile-family.md",
            "needle": "NEXT1202_0_1203",
            "purpose": "handoff requiring q_DT component amplitude law against conservative envelope",
        },
        {
            "source_id": "SRC1203_1_1202_envelope",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1202_QDT_ALLOWED_ENVELOPE.csv",
            "needle": "QAE1202_0351_WR10F1202_2_brutal_100x",
            "purpose": "computed qDT_allowed thresholds from W_R10={1,10,100}",
        },
        {
            "source_id": "SRC1203_2_1199_budget",
            "local_path": "1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md",
            "needle": "R10P1199_1_qDT_residual_budget",
            "purpose": "absolute residual budget formula",
        },
        {
            "source_id": "SRC1203_3_1199_join",
            "local_path": "1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md",
            "needle": "R10P1199_5_curve_join_rule",
            "purpose": "R10 pass condition with no signed cancellation",
        },
        {
            "source_id": "SRC1203_4_1200_components",
            "local_path": "1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md",
            "needle": "QPE1200_0_total_envelope",
            "purpose": "q_DT component split",
        },
        {
            "source_id": "SRC1203_5_1196_cokernel",
            "local_path": "1196-Y5-R10-DT-cokernel-zero-boundary-theorem-or-parent-action-block.md",
            "needle": "CKZ1196_1_dirichlet_anchor_kills_kernel",
            "purpose": "conditional no-cokernel theorem route",
        },
        {
            "source_id": "SRC1203_6_1198_boundary_no_go",
            "local_path": "1198-Y5-R10-DT-parent-anchor-source-or-first-real-bound-input-fill.md",
            "needle": "DTA1198_5_verdict",
            "purpose": "natural-boundary shortcut rejected; boundary component remains live",
        },
        {
            "source_id": "SRC1203_7_1200_template",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1200_QDT_PROFILE_ENVELOPE.csv",
            "needle": "QPE1200_5_profile_shape",
            "purpose": "existing qDT profile component template",
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

    envelope_path = OUT_DIR / "P8_Y5_R10_1202_QDT_ALLOWED_ENVELOPE.csv"
    envelope_rows_in = load_csv(envelope_path)
    for row in envelope_rows_in:
        row["_qDT_allowed"] = float(row["qDT_allowed"])
        row["_W_R10_assumed"] = float(row["W_R10_assumed"])
        row["_lambda_value"] = float(row["lambda_value"])
        row["_alpha_bound"] = float(row["alpha_bound"])

    grouped: dict[str, list[dict[str, str]]] = {}
    for row in envelope_rows_in:
        grouped.setdefault(row["scenario_id"], []).append(row)

    scenario_thresholds: list[dict[str, object]] = []
    for scenario_id, rows in sorted(grouped.items()):
        tight = min(rows, key=lambda row: row["_qDT_allowed"])
        scenario_thresholds.append(
            {
                "threshold_id": f"THR1203_{scenario_id}",
                "scenario_id": scenario_id,
                "W_R10_assumed": tight["_W_R10_assumed"],
                "tightest_source_row": tight["row_id"],
                "lambda_value": tight["_lambda_value"],
                "lambda_units": tight["lambda_units"],
                "alpha_bound": tight["_alpha_bound"],
                "qDT_allowed_min": tight["_qDT_allowed"],
                "single_component_limit_if_others_zero": tight["_qDT_allowed"],
                "equal_two_component_limit": tight["_qDT_allowed"] / 2.0,
                "equal_four_component_limit": tight["_qDT_allowed"] / 4.0,
                "interpretation": "all active nonzero q_DT components must absolute-sum below qDT_allowed_min",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    global_tight = min(scenario_thresholds, key=lambda row: float(row["qDT_allowed_min"]))

    amplitude_law = [
        {
            "law_id": "LAW1203_0_absolute_budget",
            "object": "q_DT_bound_total",
            "formula": "q_DT_bound_total = q_coker + q_boundary + q_regularizer + q_projector",
            "derivation": "1200 split plus 1199 absolute-envelope rule; all terms are nonnegative upper bounds before R10 projection.",
            "status": "DERIVED_SYMBOLIC_COMPONENT_LAW",
            "source_anchor": "1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md::QPE1200_0_total_envelope",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "law_id": "LAW1203_1_cokernel_component",
            "object": "q_coker",
            "formula": "q_coker = f_coker ||G_res||",
            "derivation": "project G_res onto surviving Ker(D_T^dagger) modes; if the no-cokernel theorem is parent-signed, f_coker=0.",
            "status": "DERIVED_SYMBOLIC_COMPONENT_INPUTS_MISSING",
            "source_anchor": "1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md::GRP1199_1_P_coker_fraction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "law_id": "LAW1203_2_boundary_component",
            "object": "q_boundary",
            "formula": "q_boundary = ||B_T|| >= |int_partialD n_mu K_T^(mu nu)(P_loc V)_nu dS|",
            "derivation": "finite trace bound or zero certificate for the D_T adjoint boundary pairing.",
            "status": "DERIVED_SYMBOLIC_BOUNDARY_INPUT_MISSING",
            "source_anchor": "1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md::QPE1200_2_boundary_component",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "law_id": "LAW1203_3_regularizer_component",
            "object": "q_regularizer",
            "formula": "q_regularizer = kappa_T C_T ||E_reg||",
            "derivation": "regularizer residue enters the tracefree solver bound unless parent action makes it vanish.",
            "status": "DERIVED_SYMBOLIC_REGULARIZER_INPUTS_MISSING",
            "source_anchor": "1200-Y5-R10-WR10-kernel-stub-and-qDT-profile-envelope.md::QPE1200_3_regularizer_component",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "law_id": "LAW1203_4_projector_component",
            "object": "q_projector",
            "formula": "q_projector = ||Delta_P|| or eps_P ||G_res|| with C_CK eps_P < 1 for absorption",
            "derivation": "P_loc/coframe/domain-motion leakage is either absorbed by the Korn inequality or scored as a finite residual.",
            "status": "DERIVED_SYMBOLIC_PROJECTOR_INPUTS_MISSING",
            "source_anchor": "1199-Y5-R10-qDT-to-R10-projection-or-Gres-profile-source.md::GRP1199_3_projector_leakage",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "law_id": "LAW1203_5_R10_gate",
            "object": "R10 nonclaim gate",
            "formula": "q_DT_bound_total <= min_i[alpha_bound(lambda_i)/W_R10(lambda_i)]",
            "derivation": "from |alpha_DT(lambda_i)| <= W_R10(lambda_i) q_DT_bound_total <= alpha_bound(lambda_i).",
            "status": "DERIVED_EXECUTABLE_NONCLAIM_THRESHOLD",
            "source_anchor": "source-intake/mts_residuals/P8_Y5_R10_1202_QDT_ALLOWED_ENVELOPE.csv",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    components = [
        {
            "component_id": "COMP1203_0_cokernel",
            "component": "q_coker=f_coker||G_res||",
            "current_numeric_value": "",
            "current_source_path": "",
            "zero_route": "parent-signed Ker(D_T^dagger)=0 or f_coker=0 on the local quotient domain",
            "finite_route": "source f_coker and ||G_res|| in same norm/domain as R10 profile",
            "status": "MISSING_NUMERIC_PARENT_INPUT",
            "blocking_reason": "no D_T cokernel fraction or G_res norm row is source-backed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "COMP1203_1_boundary",
            "component": "q_boundary=||B_T||",
            "current_numeric_value": "",
            "current_source_path": "",
            "zero_route": "parent boundary condition kills int_partialD n_mu K_T^(mu nu)(P_loc V)_nu dS",
            "finite_route": "source a boundary trace norm bound below the qDT threshold",
            "status": "MISSING_NUMERIC_PARENT_INPUT",
            "blocking_reason": "1198 rejected generic natural boundary wording as insufficient",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "COMP1203_2_regularizer",
            "component": "q_regularizer=kappa_T C_T||E_reg||",
            "current_numeric_value": "",
            "current_source_path": "",
            "zero_route": "parent action has no retained regularizer residue in the local GR branch",
            "finite_route": "source kappa_T, C_T, and ||E_reg|| with compatible units",
            "status": "MISSING_NUMERIC_PARENT_INPUT",
            "blocking_reason": "regularizer coefficient/coercivity/residue rows are not numeric",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "component_id": "COMP1203_3_projector",
            "component": "q_projector=||Delta_P|| or eps_P||G_res||",
            "current_numeric_value": "",
            "current_source_path": "",
            "zero_route": "P_loc/coframe/domain-motion leakage vanishes or is absorbed with C_CK eps_P<1",
            "finite_route": "source Delta_P or eps_P and the absorption constant C_CK",
            "status": "MISSING_NUMERIC_PARENT_INPUT",
            "blocking_reason": "projector leakage and absorption constant are not source-backed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    allocation_rows: list[dict[str, object]] = []
    allocation_modes = [
        ("single_component_if_others_zero", "one live component; other three theorem-zero", 1.0),
        ("two_component_equal_split", "two live components; other two theorem-zero", 0.5),
        ("four_component_equal_split", "all four components live and equally budgeted", 0.25),
        ("one_order_safety_per_component", "all four live with tenfold safety margin per component", 0.025),
    ]
    for threshold in scenario_thresholds:
        q_allowed = float(threshold["qDT_allowed_min"])
        for mode_id, mode_desc, fraction in allocation_modes:
            allocation_rows.append(
                {
                    "allocation_id": f"ALLOC1203_{threshold['scenario_id']}_{mode_id}",
                    "scenario_id": threshold["scenario_id"],
                    "W_R10_assumed": threshold["W_R10_assumed"],
                    "tightest_source_row": threshold["tightest_source_row"],
                    "qDT_allowed_min": q_allowed,
                    "allocation_mode": mode_id,
                    "mode_description": mode_desc,
                    "component_limit": q_allowed * fraction,
                    "active_component_count_assumed": 1 if fraction == 1.0 else (2 if fraction == 0.5 else 4),
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )

    symbolic_comparison = [
        {
            "comparison_id": "CMP1203_0_current",
            "q_coker": "MISSING",
            "q_boundary": "MISSING",
            "q_regularizer": "MISSING",
            "q_projector": "MISSING",
            "q_DT_bound_total": "MISSING",
            "threshold_used": global_tight["threshold_id"],
            "threshold_value": global_tight["qDT_allowed_min"],
            "score_status": "BLOCKED_MISSING_COMPONENT_AMPLITUDES",
            "interpretation": "The inequality is executable, but current corpus lacks numeric q_DT component amplitudes.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "comparison_id": "CMP1203_1_zero_branch_sufficient_condition",
            "q_coker": "0",
            "q_boundary": "0",
            "q_regularizer": "0",
            "q_projector": "0",
            "q_DT_bound_total": "0",
            "threshold_used": global_tight["threshold_id"],
            "threshold_value": global_tight["qDT_allowed_min"],
            "score_status": "CONDITIONAL_PASS_IF_ALL_ZERO_THEOREMS_PARENT_SIGNED",
            "interpretation": "A real local-GR reduction route would pass this nonclaim envelope if all four components are theorem-zero from the parent action.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1203_0_component_values",
            "gate": "numeric q_DT component amplitudes",
            "status": "BLOCKED",
            "reason": "all four q_DT components remain missing parent-signed numeric values or zero certificates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1203_1_WR10_official",
            "gate": "official/source-reconstructed W_R10",
            "status": "BLOCKED",
            "reason": "1203 still uses 1202 scenario W values, not the official R10 geometry kernel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1203_2_bound_curve_promotion",
            "gate": "promoted R10 bound curve",
            "status": "BLOCKED",
            "reason": "review-candidate curve remains nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1203_3_no_tuned_cancellation",
            "gate": "absolute sum only",
            "status": "ACTIVE_GUARD",
            "reason": "component signs cannot cancel; every live component consumes positive qDT budget",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision_ledger = [
        {
            "decision_id": "DEC1203_0_verdict",
            "condition": "amplitude law derived but no component amplitudes sourced",
            "decision": "keep R10/local-GR branch blocked, but define the next target as a component-zero or component-bound attack",
            "result": f"global tightest private target is q_DT_bound_total <= {fmt(global_tight['qDT_allowed_min'])} under {global_tight['scenario_id']}",
            "next_action": "try to close the strongest component first: boundary B_T zero/bound or projector absorption, because those can remove whole positive terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    next_target = [
        {
            "next_id": "NEXT1203_0_1204",
            "target_file": "1204-Y5-R10-boundary-projector-zero-or-finite-amplitude-bound.md",
            "target_script": "scripts/Y5_R10_boundary_projector_zero_or_finite_amplitude_bound.py",
            "task": "attack q_boundary and q_projector first: either derive parent-signed zero/absorption conditions or produce finite source-ready bounds small enough for the 1203 amplitude targets",
            "success_condition": "at least one live positive q_DT component is either theorem-zero or has a numeric nonclaim upper bound; no R10/local-GR pass is claimed",
            "do_not_do": "do not tune cancellations, do not promote the review curve, do not edit formalization-workbench, do not push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_fields = ["source_id", "local_path", "needle", "purpose", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"]
    law_fields = ["law_id", "object", "formula", "derivation", "status", "source_anchor", "valid_for_claim", "claim_allowed"]
    threshold_fields = [
        "threshold_id",
        "scenario_id",
        "W_R10_assumed",
        "tightest_source_row",
        "lambda_value",
        "lambda_units",
        "alpha_bound",
        "qDT_allowed_min",
        "single_component_limit_if_others_zero",
        "equal_two_component_limit",
        "equal_four_component_limit",
        "interpretation",
        "valid_for_claim",
        "claim_allowed",
    ]
    component_fields = ["component_id", "component", "current_numeric_value", "current_source_path", "zero_route", "finite_route", "status", "blocking_reason", "valid_for_claim", "claim_allowed"]
    allocation_fields = ["allocation_id", "scenario_id", "W_R10_assumed", "tightest_source_row", "qDT_allowed_min", "allocation_mode", "mode_description", "component_limit", "active_component_count_assumed", "valid_for_claim", "claim_allowed"]
    comparison_fields = ["comparison_id", "q_coker", "q_boundary", "q_regularizer", "q_projector", "q_DT_bound_total", "threshold_used", "threshold_value", "score_status", "interpretation", "valid_for_claim", "claim_allowed"]
    gate_fields = ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]
    decision_fields = ["decision_id", "condition", "decision", "result", "next_action", "valid_for_claim", "claim_allowed"]
    next_fields = ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"]

    write_csv(SOURCE_REGISTER_PATH, source_rows, source_fields)
    write_csv(AMPLITUDE_LAW_PATH, amplitude_law, law_fields)
    write_csv(SCENARIO_THRESHOLDS_PATH, scenario_thresholds, threshold_fields)
    write_csv(COMPONENT_STATUS_PATH, components, component_fields)
    write_csv(ALLOCATION_TARGETS_PATH, allocation_rows, allocation_fields)
    write_csv(SYMBOLIC_COMPARISON_PATH, symbolic_comparison, comparison_fields)
    write_csv(CLAIM_GATES_PATH, claim_gates, gate_fields)
    write_csv(DECISION_LEDGER_PATH, decision_ledger, decision_fields)
    write_csv(NEXT_TARGET_PATH, next_target, next_fields)

    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if mtime >= RUN_STARTED_UTC:
                    formalization_recent.append(path)

    csvs_to_parse = [
        SOURCE_REGISTER_PATH,
        AMPLITUDE_LAW_PATH,
        SCENARIO_THRESHOLDS_PATH,
        COMPONENT_STATUS_PATH,
        ALLOCATION_TARGETS_PATH,
        SYMBOLIC_COMPARISON_PATH,
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
    threshold_values_positive = all(float(row["qDT_allowed_min"]) > 0 for row in scenario_thresholds)
    global_threshold_matches_1202 = abs(float(global_tight["qDT_allowed_min"]) - 2.344664300519378e-05) < 1e-16
    all_components_blocked = all(row["status"] == "MISSING_NUMERIC_PARENT_INPUT" for row in components)
    comparison_blocked = symbolic_comparison[0]["score_status"] == "BLOCKED_MISSING_COMPONENT_AMPLITUDES"
    zero_sufficient_but_nonclaim = symbolic_comparison[1]["score_status"] == "CONDITIONAL_PASS_IF_ALL_ZERO_THEOREMS_PARENT_SIGNED" and not symbolic_comparison[1]["valid_for_claim"]
    allocation_targets_positive = all(float(row["component_limit"]) > 0 for row in allocation_rows)
    claim_policy_ok = all(not bool(row["valid_for_claim"]) and not bool(row["claim_allowed"]) for row in amplitude_law + scenario_thresholds + components + allocation_rows + symbolic_comparison + claim_gates)
    formalization_untouched = len(formalization_recent) == 0

    validation_rows = [
        validation_row("VAL1203_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"),
        validation_row("VAL1203_1_needles_found", "all cited source needles found", all_needles_found, f"{sum(bool(row['needle_found']) for row in source_rows)}/{len(source_rows)} needles found"),
        validation_row("VAL1203_2_thresholds_positive", "scenario thresholds are positive", threshold_values_positive, f"scenario_threshold_count={len(scenario_thresholds)}"),
        validation_row("VAL1203_3_global_threshold", "global tight threshold inherited from 1202", global_threshold_matches_1202, f"global_tight={fmt(global_tight['qDT_allowed_min'])};source={global_tight['tightest_source_row']}"),
        validation_row("VAL1203_4_components_blocked", "component amplitudes remain explicitly blocked", all_components_blocked, f"blocked_components={sum(row['status']=='MISSING_NUMERIC_PARENT_INPUT' for row in components)}/{len(components)}"),
        validation_row("VAL1203_5_current_comparison_blocked", "current comparison does not claim a pass", comparison_blocked, symbolic_comparison[0]["score_status"]),
        validation_row("VAL1203_6_zero_branch_nonclaim", "zero branch is only conditional nonclaim", zero_sufficient_but_nonclaim, symbolic_comparison[1]["score_status"]),
        validation_row("VAL1203_7_allocations_positive", "component allocation targets are positive", allocation_targets_positive, f"allocation_rows={len(allocation_rows)}"),
        validation_row("VAL1203_8_nonclaim_policy", "all generated rows remain nonclaim", claim_policy_ok, "valid_for_claim=false and claim_allowed=false throughout"),
        validation_row("VAL1203_9_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parse_details)),
        validation_row("VAL1203_10_formalization_untouched", "formalization-workbench untouched during run", formalization_untouched, f"formalization_recent_after_run_start_count={len(formalization_recent)}"),
    ]
    validation_pass = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1203_11_overall",
            "overall 1203 validation",
            validation_pass,
            "1203 amplitude law and component pressure targets are reproducible" if validation_pass else "one or more validation checks failed",
        )
    )
    validation_fields = ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"]
    write_csv(VALIDATION_PATH, validation_rows, validation_fields)

    doc = f"""# 1203 Y5/R10 qDT Component Amplitude Law Against Conservative Envelope

**Current verdict:** 1203 derives the executable amplitude pressure law but does not close the R10/local-GR branch. The global tightest private threshold inherited from 1202 is `q_DT_bound_total <= {fmt(global_tight['qDT_allowed_min'])}` under `{global_tight['scenario_id']}`.

**Main progress:** the missing local-GR problem is now sharply localized: either prove theorem-zero for the cokernel, boundary, regularizer, and projector terms, or source finite bounds whose absolute sum stays below the scenario threshold. No signed cancellation is allowed.

## Source Register

{markdown_table(source_rows, source_fields)}

## Amplitude Law

{markdown_table(amplitude_law, law_fields)}

## Scenario Pressure Thresholds

{markdown_table(scenario_thresholds, threshold_fields)}

## Component Bound Status

{markdown_table(components, component_fields)}

## Component Allocation Targets

{markdown_table(allocation_rows, allocation_fields)}

## Symbolic Comparison

{markdown_table(symbolic_comparison, comparison_fields)}

## Claim Gates

{markdown_table(claim_gates, gate_fields)}

## Decision Ledger

{markdown_table(decision_ledger, decision_fields)}

## Next Target

{markdown_table(next_target, next_fields)}

## Validation

{markdown_table(validation_rows, validation_fields)}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"validation_pass={validation_pass}")
    print(f"global_tight={fmt(global_tight['qDT_allowed_min'])} from {global_tight['threshold_id']}")


if __name__ == "__main__":
    main()

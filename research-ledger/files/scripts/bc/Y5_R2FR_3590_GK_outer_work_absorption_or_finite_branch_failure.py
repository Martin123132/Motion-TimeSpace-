from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R2FR_Y5_GK_OUTER_WORK_ABSORPTION_3590"
CHECKPOINT_ID = "3590"
DOC = ROOT / "3590-Y5-R2FR-GK-outer-work-absorption-or-finite-branch-failure.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sources() -> dict[str, Path]:
    return {
        "next_3589": RESIDUALS / "P8_Y5_R2FR_3589_NEXT_TARGET.csv",
        "status_3589": RESIDUALS / "P8_Y5_R2FR_3589_STATUS.csv",
        "finite_3589": RESIDUALS / "P8_Y5_R2FR_3589_FIRST_FINITE_EPSILON_ROW.csv",
        "circularity_3589": RESIDUALS / "P8_Y5_R2FR_3589_CIRCULARITY_GATES.csv",
        "input_pack_3589": RESIDUALS / "P8_Y5_R2FR_3589_NONCOERCIVE_INPUT_PACK.csv",
        "validation_3589": RESIDUALS / "P8_Y5_BRR545_3589_VALIDATION.csv",
        "hair_3586": RESIDUALS / "P8_Y5_R2FR_3586_GK_HAIR_BOUND_ROWS.csv",
        "coercivity_2471": RESIDUALS / "P8_Y5_GK_OPERATOR_2471_COERCIVITY_AUDIT.csv",
        "coercivity_2561": RESIDUALS / "P8_Y5_NO_SHADOW_2561_COERCIVITY_AUDIT.csv",
        "missing_coeff_2473": RESIDUALS / "P8_Y5_GK_STRESS_BOUND_2473_MISSING_COEFFICIENT_LEDGER.csv",
        "noncoercive_2079": RESIDUALS / "P8_Y5_PARENT_QLOC_2079_FINITE_NONCOERCIVE_BRANCH.csv",
        "qloc_interface_2581": RESIDUALS / "P8_Y5_GAMMAKHAT_QLOC_2581_OFFICIAL_RESIDUAL_INTERFACE.csv",
        "qloc_gate_2581": RESIDUALS / "P8_Y5_GAMMAKHAT_QLOC_2581_DERIVATION_PROOF_GATE.csv",
        "projector_obstruction_549": RESIDUALS / "P8_Y5_BRR545_PROJECTOR_SYMPLECTIC_OBSTRUCTION_LEDGER.csv",
        "epsilon_3585": RESIDUALS / "P8_Y5_R2FR_3585_EPSILON_HAIR_BOUND_ROWS.csv",
        "geometry_3583": RESIDUALS / "P8_Y5_R2FR_3583_GEOMETRY_RESIDUAL_STACK.csv",
        "runner_inputs_2475": RESIDUALS / "P8_Y5_GK_BOUND_SOURCE_2475_RUNNER_INPUT_CANDIDATES.csv",
        "source_charge_1793": RESIDUALS / "P8_Y5_PARENT_QLOC_1793_Y5_SOURCE_CHARGE_OWNER_ATTEMPT.csv",
    }


def outputs() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3590_SOURCE_REGISTER.csv",
        "absorption_theorem": RESIDUALS / "P8_Y5_R2FR_3590_ABSORPTION_THEOREM.csv",
        "eta_budget": RESIDUALS / "P8_Y5_R2FR_3590_ETA_GK_BUDGET.csv",
        "outer_work_pack": RESIDUALS / "P8_Y5_R2FR_3590_OUTER_WORK_PACK.csv",
        "branch_verdict": RESIDUALS / "P8_Y5_R2FR_3590_BRANCH_VERDICT.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3590_ACTIVATION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3590_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3590_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_GK_outer_work_absorption_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3590_VALIDATION.csv",
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def file_contains(path: Path, token: str) -> bool:
    return token in path.read_text(encoding="utf-8", errors="ignore")


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": "3590 GK outer-work/absorption source",
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def absorption_theorem_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "ABS3590_0_starting_inequality",
            "X_GK^2 <= a_GK X_GK + F0_GK_abs + eta_GK X_GK^2",
            "separates linear work, noncircular fixed outer work, and quadratic self-defect",
            "DERIVED_ABSORPTION_FORM",
            "finite_3589",
        ),
        (
            "ABS3590_1_absorption_condition",
            "0 <= eta_GK < 1",
            "required to move quadratic defects to the left without reversing or losing the bound",
            "EXACT_NECESSARY_FOR_THIS_BRANCH",
            "circularity_3589",
        ),
        (
            "ABS3590_2_absorbed_bound",
            "X_GK <= [a_GK + sqrt(a_GK^2 + 4(1-eta_GK)F0_GK_abs)]/[2(1-eta_GK)]",
            "valid finite envelope after absorbing quadratic defects",
            "DERIVED_EXACT_QUADRATIC_ROOT",
            "noncoercive_2079",
        ),
        (
            "ABS3590_3_zero_fixed_work_limit",
            "if F0_GK_abs=0 and eta_GK<1 then X_GK <= a_GK/(1-eta_GK)",
            "shows the branch can still bound a purely source/boundary/topology-driven residual",
            "DERIVED_LIMIT_CASE",
            "finite_3589",
        ),
        (
            "ABS3590_4_failure_condition",
            "if eta_GK>=1 or eta_GK is unsigned, the finite branch cannot be score-ready",
            "prevents quadratic self-defects from masquerading as external forcing",
            "PASS_GUARD",
            "hair_3586",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": theorem_id,
            "mathematical_form": form,
            "meaning": meaning,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "uses_positive_lambda_denominator": False,
            "requires_eta_less_than_one": "eta_GK" in form,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for theorem_id, form, meaning, status, source_key in rows
    ]


def eta_budget_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "ETA3590_0_eta_cross",
            "eta_cross_GK",
            "max(0, |c_AG|C_cross - min(Z_A lambda1_A + m_A2, Z_G lambda1_G + m_G2))/N_GK",
            "absorbs the 3586 quadratic cross-excess term into eta_GK X_GK^2",
            "FORMULA_DERIVED_VALUES_MISSING",
            "hair_3586",
        ),
        (
            "ETA3590_1_eta_projector",
            "eta_projector_GK",
            "operator norm of field-dependent or noncommuting projector stress/leakage divided by X_GK^2",
            "absorbs P_loc commutator/variation terms if they are small rather than fixed",
            "MISSING_PROJECTOR_DESCENT_BOUND",
            "projector_obstruction_549",
        ),
        (
            "ETA3590_2_eta_boundary_feedback",
            "eta_boundary_feedback_GK",
            "quadratic part of boundary/symplectic feedback after fixed Phi_boundary_GK is removed",
            "absorbs boundary terms that scale with the unknown GK amplitude",
            "MISSING_BOUNDARY_FEEDBACK_BOUND",
            "missing_coeff_2473",
        ),
        (
            "ETA3590_3_eta_metric_response",
            "eta_metric_response_GK",
            "metric-response/observable backreaction coefficient from GK stress to the same X_GK norm",
            "absorbs arena or metric-response self-feedback if small",
            "MISSING_ARENA_PROJECTION_BOUND",
            "missing_coeff_2473",
        ),
        (
            "ETA3590_4_eta_sum",
            "eta_GK",
            "eta_cross_GK + eta_projector_GK + eta_boundary_feedback_GK + eta_metric_response_GK",
            "total quadratic defect coefficient for the absorbed finite branch",
            "SUM_FORMULA_READY_VALUES_MISSING",
            "coercivity_2471",
        ),
        (
            "ETA3590_5_eta_gate",
            "eta_GK<1",
            "parent-signed strict smallness of the total quadratic defect",
            "activation gate for the absorbed finite branch",
            "NOT_PARENT_SIGNED_CURRENT_CORPUS",
            "coercivity_2561",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "eta_id": eta_id,
            "symbol": symbol,
            "formula_or_definition": formula,
            "role": role,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "numeric_value_present": False,
            "parent_signed_eta_less_than_one": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for eta_id, symbol, formula, role, status, source_key in rows
    ]


def outer_work_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "FOUT3590_0_F_source_tail",
            "F_source_tail_GK_abs",
            "fixed source-support/current tail independent of X_GK after J_GK_norm is split into the linear term",
            "MISSING_FIXED_SOURCE_TAIL_VALUE_OR_ZERO",
            "qloc_interface_2581",
        ),
        (
            "FOUT3590_1_F_boundary_fixed",
            "F_boundary_fixed_GK_abs",
            "fixed boundary/reference/symplectic work independent of X_GK after Phi_boundary_GK is split into the trace-linear term",
            "MISSING_FIXED_BOUNDARY_VALUE_OR_ZERO",
            "input_pack_3589",
        ),
        (
            "FOUT3590_2_F_topology_fixed",
            "F_topology_fixed_GK_abs",
            "fixed topological/harmonic charge not controlled by local GK amplitude",
            "MISSING_TOPOLOGY_ZERO_OR_FINITE_VALUE",
            "projector_obstruction_549",
        ),
        (
            "FOUT3590_3_F_geometry_background",
            "F_geometry_background_GK_abs",
            "fixed stationary-domain/E_stat background leakage not proportional to u_GK",
            "MISSING_ESTAT_BACKGROUND_VALUE_OR_ZERO",
            "geometry_3583",
        ),
        (
            "FOUT3590_4_F0_sum",
            "F0_GK_abs",
            "F_source_tail_GK_abs + F_boundary_fixed_GK_abs + F_topology_fixed_GK_abs + F_geometry_background_GK_abs",
            "SUM_FORMULA_READY_VALUES_MISSING",
            "epsilon_3585",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "outer_id": outer_id,
            "symbol": symbol,
            "definition": definition,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "independent_of_X_GK_claimed": False,
            "numeric_value_present": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for outer_id, symbol, definition, status, source_key in rows
    ]


def branch_verdict_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "BV3590_0_absorbed_formula",
            "epsilon_GK_hair_absorbed",
            "K_GK*[a_GK + sqrt(a_GK^2 + 4(1-eta_GK)F0_GK_abs)]/[2(1-eta_GK)]",
            "AVAILABLE_CONDITIONAL_FORMULA",
            "valid only if eta_GK<1, F0_GK_abs is noncircular, K_GK is sourced, and units are locked",
            "noncoercive_2079",
            False,
        ),
        (
            "BV3590_1_current_eta_result",
            "eta_GK",
            "eta_GK<1 is not parent-signed; eta_cross has a formal expression but missing coefficients, while projector/boundary/metric feedback bounds are absent",
            "FAIL_CURRENT_SCORE",
            "cannot score or claim finite GK hair from the absorbed formula yet",
            "coercivity_2471",
            True,
        ),
        (
            "BV3590_2_current_F0_result",
            "F0_GK_abs",
            "no source-backed noncircular fixed outer-work value exists in the current corpus",
            "FAIL_CURRENT_SCORE",
            "outer work remains a ledger of finite slots, not a number or theorem-zero",
            "missing_coeff_2473",
            True,
        ),
        (
            "BV3590_3_demoted_residual_parameter",
            "X_GK_residual",
            "retain X_GK_residual as an explicit local-GR residual parameter rather than recycling the input-pack search",
            "STRUCTURAL_NON_SCORE_READY_RESIDUAL",
            "this avoids pretending that repeated symbolic refills produce an empirical prediction",
            "status_3589",
            True,
        ),
        (
            "BV3590_4_local_claim_policy",
            "local_GR_R10_PPN_claim",
            "blocked until eta_GK<1 or F0/K/source-boundary-topology rows are parent-signed and numeric/sourced",
            "CLAIM_BLOCKED",
            "finite branch remains useful as a derivation scaffold, not a claim",
            "runner_inputs_2475",
            True,
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "verdict_id": verdict_id,
            "symbol": symbol,
            "formula_or_decision": formula,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths[source_key]),
            "blocks_score": blocks_score,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for verdict_id, symbol, formula, status, detail, source_key, blocks_score in rows
    ]


def activation_gate_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("GATE3590_0_sources", "PASS", "all source paths and selected anchors exist", "next_3589"),
        ("GATE3590_1_absorption_theorem", "PASS_DERIVED", "exact eta absorption bound is derived from the quadratic inequality", "finite_3589"),
        ("GATE3590_2_no_lambda", "PASS_GUARD", "absorbed finite branch still does not use lambda_GK denominator", "circularity_3589"),
        ("GATE3590_3_eta_less_than_one", "FAIL_CURRENT_SCORE", "eta_GK<1 is not parent-signed", "coercivity_2471"),
        ("GATE3590_4_F0_noncircular", "FAIL_CURRENT_SCORE", "F0_GK_abs has no source-backed noncircular fixed value", "missing_coeff_2473"),
        ("GATE3590_5_demote_residual", "PASS_GUARD", "GK finite branch is retained as explicit residual parameter instead of endlessly refilled", "status_3589"),
        ("GATE3590_6_local_GR", "FAIL_CURRENT_CLAIM", "source coupling/Newton/PPN/local-GR closure remains blocked", "source_charge_1793"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, status, detail, source_key in rows
    ]


def status_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "ABSORPTION_THEOREM_DERIVED_GK_BRANCH_DEMOTED_TO_EXPLICIT_RESIDUAL",
            "strongest_result": "3590 derives the exact absorption law for the finite GK branch: from X_GK^2 <= a_GK X_GK + F0_GK_abs + eta_GK X_GK^2, eta_GK<1 gives X_GK <= [a_GK + sqrt(a_GK^2 + 4(1-eta_GK)F0_GK_abs)]/[2(1-eta_GK)]. This is the lawful replacement for smuggling epsilon_cross_hair_GK into F_outer.",
            "decision": "current corpus does not sign eta_GK<1 or provide noncircular F0_GK_abs, so GK finite hair is retained as an explicit residual parameter and not repeatedly refilled as if score-ready",
            "still_missing": "parent-signed eta_cross/eta_projector/eta_boundary/eta_metric bounds; noncircular fixed F0_GK_abs components; K_GK observable map; units/domain lock; source coupling/Newton/PPN closure",
            "public_claim_allowed": False,
            "valid_for_claim": False,
            "source_path": str(source_paths["status_3589"]),
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3590_0",
            "target_doc": "3591-Y5-R2FR-source-coupling-GM-calibration-or-residual-contract.md",
            "target_script": "scripts/Y5_R2FR_3591_source_coupling_GM_calibration_or_residual_contract.py",
            "objective": "pivot from GK finite-hair refill to source coupling: derive the parent Hilbert/Noether charge to Newtonian GM transfer, or write the explicit residual contract that carries unclosed GK/local hair into PPN/Newton tests",
            "success_gate": "either measured GM is connected to a parent-owned source charge with universal G_ref, or the remaining residual vector is explicitly propagated rather than hidden in fitted GM",
            "reason": "3590 prevents another loop on GK finite inputs; the next project-critical bottleneck is calibrated source coupling/Newton transfer",
            "valid_for_claim": False,
        }
    ]


def validation_rows(
    source_paths: dict[str, Path],
    out_paths: dict[str, Path],
    absorption: list[dict[str, object]],
    eta_budget: list[dict[str, object]],
    outer_work: list[dict[str, object]],
    verdicts: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in out_paths.items() if key != "validation"}
    needles = {
        "next_3589": "NEXT3589_0",
        "status_3589": "FIRST_NONCOERCIVE_EPSILON_ROW_DERIVED_INPUT_PACK_SOURCE_BLOCKED",
        "finite_3589": "FFE3589_1_X_GK_bound",
        "circularity_3589": "CIRC3589_3_absorption_alternative",
        "input_pack_3589": "NCI3589_6_F_outer_GK_abs",
        "validation_3589": "VAL3589_13_formalization_workbench_untouched",
        "hair_3586": "GHB3586_6_epsilon_cross_hair_GK",
        "coercivity_2471": "COER2471_2_eta_form",
        "coercivity_2561": "COER2561_3_completed_square",
        "missing_coeff_2473": "MISS2473_2_CX",
        "noncoercive_2079": "FIN2079_0_branch_law",
        "qloc_interface_2581": "QLOC2581_5_projector_gap",
        "qloc_gate_2581": "GK2581_5_projector_owner",
        "projector_obstruction_549": "PSO550_1_commutator_product_rule",
        "epsilon_3585": "EHB3585_7_epsilon_Estat_after_3585",
        "geometry_3583": "GRS3583_7_R_ann_abs_after_3583",
        "runner_inputs_2475": "RUN2475_R10_ANCHOR_INPUT",
        "source_charge_1793": "Y5SC1793_5_Gauss_orbital_calibration",
    }
    validations.append(("VAL3590_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3590 source paths exist"))
    validations.append(("VAL3590_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected 3590 anchors found"))
    validations.append(("VAL3590_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3590 output files written"))
    csvs_parse = True
    parse_details: list[str] = []
    for output_id, path in pre_validation_outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            row_count = len(read_csv(path))
            csvs_parse = csvs_parse and row_count > 0
            parse_details.append(f"{output_id}:{row_count}")
        except Exception as exc:
            csvs_parse = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3590_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3590_4_absorption_formula_present", any(row["theorem_id"] == "ABS3590_2_absorbed_bound" and "1-eta_GK" in row["mathematical_form"] for row in absorption), "absorbed eta bound is present"))
    required_eta = {"eta_cross_GK", "eta_projector_GK", "eta_boundary_feedback_GK", "eta_metric_response_GK", "eta_GK", "eta_GK<1"}
    validations.append(("VAL3590_5_eta_budget_complete", required_eta.issubset({str(row["symbol"]) for row in eta_budget}), "all eta budget rows are present"))
    validations.append(("VAL3590_6_F0_pack_complete", {"F_source_tail_GK_abs", "F_boundary_fixed_GK_abs", "F_topology_fixed_GK_abs", "F_geometry_background_GK_abs", "F0_GK_abs"}.issubset({str(row["symbol"]) for row in outer_work}), "all noncircular F0 slots are present"))
    validations.append(("VAL3590_7_no_lambda_denominator", all(str(row.get("uses_positive_lambda_denominator", False)).lower() == "false" for row in absorption), "absorption theorem does not use lambda_GK"))
    validations.append(("VAL3590_8_eta_not_signed", any(row["symbol"] == "eta_GK<1" and row["status"] == "NOT_PARENT_SIGNED_CURRENT_CORPUS" for row in eta_budget), "eta_GK<1 remains explicitly unsigned"))
    validations.append(("VAL3590_9_branch_demoted", any(row["verdict_id"] == "BV3590_3_demoted_residual_parameter" and row["status"] == "STRUCTURAL_NON_SCORE_READY_RESIDUAL" for row in verdicts), "GK branch demoted to explicit residual parameter"))
    validations.append(("VAL3590_10_score_blocked", any(row["gate_id"] == "GATE3590_3_eta_less_than_one" and row["status"] == "FAIL_CURRENT_SCORE" for row in gates) and any(row["gate_id"] == "GATE3590_4_F0_noncircular" and row["status"] == "FAIL_CURRENT_SCORE" for row in gates), "score remains blocked by eta and F0 gates"))
    generated_rows = absorption + eta_budget + outer_work + verdicts + gates + status + next_target
    validations.append(("VAL3590_11_no_claim_flags", all(str(row.get("valid_for_claim", False)).lower() == "false" and str(row.get("claim_allowed", False)).lower() == "false" for row in generated_rows), "all generated physics rows remain nonclaim"))
    validations.append(("VAL3590_12_next_target_selected", any(row["next_id"] == "NEXT3590_0" for row in next_target), "3591 source-coupling target selected"))
    validations.append(("VAL3590_13_generated_source_paths_exist", all(Path(str(row["source_path"])).exists() for row in absorption + eta_budget + outer_work + verdicts + gates + status), "every generated row source_path exists"))
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_3590*")) or any(FORMALIZATION.rglob("3590-Y5-R2FR*"))
    validations.append(("VAL3590_14_formalization_workbench_untouched", not formalization_touched, "no 3590 checkpoint output appears in formalization-workbench"))
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passes,
            "status": "PASS" if passes else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passes, detail in validations
    ]


def write_doc(
    absorption: list[dict[str, object]],
    eta_budget: list[dict[str, object]],
    outer_work: list[dict[str, object]],
    verdicts: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 3590 - GK outer work absorption or finite branch failure",
        "",
        "## Verdict",
        "3590 derives the lawful absorbed finite branch.  If",
        "",
        "`X_GK^2 <= a_GK X_GK + F0_GK_abs + eta_GK X_GK^2`,",
        "",
        "then `eta_GK < 1` gives",
        "",
        "`X_GK <= [a_GK + sqrt(a_GK^2 + 4(1-eta_GK)F0_GK_abs)]/[2(1-eta_GK)]`.",
        "",
        "The current corpus does not sign `eta_GK < 1` and does not supply noncircular `F0_GK_abs`, so the branch is retained as an explicit residual parameter rather than refilled again as if it were score-ready.",
        "",
        "## Absorption theorem",
    ]
    for row in absorption:
        lines.append(f"- `{row['theorem_id']}`: {row['status']} - {row['mathematical_form']}")
    lines.extend(["", "## Eta budget"])
    for row in eta_budget:
        lines.append(f"- `{row['eta_id']}` `{row['symbol']}`: {row['status']} - {row['formula_or_definition']}")
    lines.extend(["", "## Outer work pack"])
    for row in outer_work:
        lines.append(f"- `{row['outer_id']}` `{row['symbol']}`: {row['status']} - {row['definition']}")
    lines.extend(["", "## Branch verdict"])
    for row in verdicts:
        lines.append(f"- `{row['verdict_id']}` `{row['symbol']}`: {row['status']} - {row['formula_or_decision']}")
    lines.extend(["", "## Gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
        lines.append(f"- Decision: {row['decision']}")
        lines.append(f"- Still missing: {row['still_missing']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target"])
    for row in next_target:
        lines.append(f"- `{row['next_id']}` -> `{row['target_doc']}`")
        lines.append(f"- Objective: {row['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    out_paths = outputs()
    register = source_register(source_paths)
    absorption = absorption_theorem_rows(source_paths)
    eta_budget = eta_budget_rows(source_paths)
    outer_work = outer_work_rows(source_paths)
    verdicts = branch_verdict_rows(source_paths)
    gates = activation_gate_rows(source_paths)
    status = status_rows(source_paths)
    next_target = next_target_rows()
    for key, rows in {
        "source_register": register,
        "absorption_theorem": absorption,
        "eta_budget": eta_budget,
        "outer_work_pack": outer_work,
        "branch_verdict": verdicts,
        "activation_gates": gates,
        "status": status,
        "next_target": next_target,
        "canonical_status": status,
    }.items():
        write_csv(out_paths[key], rows)
    validation = validation_rows(source_paths, out_paths, absorption, eta_budget, outer_work, verdicts, gates, status, next_target)
    write_csv(out_paths["validation"], validation)
    write_doc(absorption, eta_budget, outer_work, verdicts, gates, status, next_target, validation)
    failures = [row for row in validation if row["status"] != "PASS"]
    if failures:
        raise SystemExit(f"3590 validation failed: {failures}")
    print(f"wrote {DOC}")
    for key, path in out_paths.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()

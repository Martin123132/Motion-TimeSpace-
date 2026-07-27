from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
R10 = ROOT / "source-intake" / "r10"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1505-Y5-R10-RAB-map-R10-residual-X-to-quotient-vertical-kernel-or-beta-bound.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1504_validation": OUT / "P8_Y5_BRR545_1504_VALIDATION.csv",
    "1504_verticality": OUT / "P8_Y5_R10_1504_R10_RESIDUAL_VERTICALITY_CONTRACT.csv",
    "1504_beta_theorem": OUT / "P8_Y5_R10_1504_BETA_ZERO_THEOREM_OR_COUNTERMODEL.csv",
    "1504_beta_closure": OUT / "P8_Y5_R10_1504_BETA_CLOSURE_BOUND_INPUT_ROWS.csv",
    "1504_blockers": OUT / "P8_Y5_R10_1504_TARGET_PROMOTION_BLOCKERS.csv",
    "local_residual_template": OUT / "MTS_local_residual_predictions_TEMPLATE.csv",
    "quotient_chain": ROOT / "runs" / "20260601-000090-quotient-configuration-principle-from-topological-projector" / "results" / "presymplectic_quotient_chain.csv",
    "quotient_gates": ROOT / "runs" / "20260601-000090-quotient-configuration-principle-from-topological-projector" / "results" / "gate_results.csv",
    "pullback_attempts": ROOT / "runs" / "20260602-013500-observed-coframe-selector-pullback-cancellation-theorem" / "results" / "theorem_attempts.csv",
    "full_cell_no_go": ROOT / "runs" / "20260601-203000-full-cell-equivalence-gauge-redundancy-gate" / "results" / "no_go_lemmas.csv",
    "full_cell_contract": ROOT / "runs" / "20260601-203000-full-cell-equivalence-gauge-redundancy-gate" / "results" / "gauge_redundancy_contract.csv",
    "fibre_route_audit": ROOT / "runs" / "20260601-204500-indistinguishable-cell-quotient-parent-action-gate" / "results" / "parent_variable_route_audit.csv",
    "fibre_no_go": ROOT / "runs" / "20260601-204500-indistinguishable-cell-quotient-parent-action-gate" / "results" / "no_go_lemmas.csv",
    "r10_curve_contract": ROOT / "runs" / "20260605-143500-Y5-R10-alpha-lambda-source-normalized-curve-data-or-no-range-theorem" / "results" / "P8_Y5_R10_MTS_CURVE_INPUT_CONTRACT.csv",
    "bulk_memory_fill": ROOT / "runs" / "20260605-142500-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill" / "results" / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_YUKAWA_FILL_ROW.csv",
}

CURVE_TARGET = R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
KERNEL_TARGET = R10 / "derived" / "R10_delta_w_kernel_lambda.csv"
C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

FIELD_MAP_AUDIT = OUT / "P8_Y5_R10_1505_R10_RESIDUAL_FIELD_MAP_AUDIT.csv"
VERTICALITY_TESTS = OUT / "P8_Y5_R10_1505_DQ_VERTICALITY_TESTS.csv"
THEOREM_LEDGER = OUT / "P8_Y5_R10_1505_QUOTIENT_VERTICAL_THEOREM_LEDGER.csv"
BETA_BOUND_ROWS = OUT / "P8_Y5_R10_1505_BETA_BOUND_INPUT_ROWS_NONCLAIM.csv"
ALPHA_ROUTE_MATRIX = OUT / "P8_Y5_R10_1505_ALPHA_ROUTE_MATRIX.csv"
FORMULA_REGISTER = OUT / "P8_Y5_R10_1505_FORMULA_REGISTER.csv"
TARGET_BLOCKERS = OUT / "P8_Y5_R10_1505_TARGET_PROMOTION_BLOCKERS.csv"
SCORE_READINESS = OUT / "P8_Y5_R10_1505_DELTA_W_SCORE_READINESS.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1505_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1505_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1505_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1505_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1505_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1505_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1505"
QUAR_FIELD_MAP = QUARANTINE / "R10_RESIDUAL_FIELD_MAP_AUDIT_NONCLAIM.csv"
QUAR_VERTICALITY = QUARANTINE / "DQ_VERTICALITY_TESTS_NONCLAIM.csv"
QUAR_THEOREM = QUARANTINE / "QUOTIENT_VERTICAL_THEOREM_LEDGER_NONCLAIM.csv"
QUAR_BOUND = QUARANTINE / "BETA_BOUND_INPUT_ROWS_NONCLAIM.csv"
BRANCH_FIELD_MAP = BRANCH_RESIDUALS / "r10_residual_field_map_audit_nonclaim_1505.csv"
BRANCH_VERTICALITY = BRANCH_RESIDUALS / "r10_dq_verticality_tests_nonclaim_1505.csv"
BRANCH_THEOREM = BRANCH_RESIDUALS / "r10_quotient_vertical_theorem_ledger_nonclaim_1505.csv"
BRANCH_BOUND = BRANCH_RESIDUALS / "r10_beta_bound_input_rows_nonclaim_1505.csv"


def flags() -> dict[str, bool]:
    return {"score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def field_map_rows() -> list[dict[str, Any]]:
    candidates = [
        (
            "XMAP1505_0_bulk_X_static_green",
            "bulk_X_Yukawa_tail",
            "finite-range bulk field with static Green function",
            "not quotient-vertical if it has source/test charge; must be zeroed or bounded",
            "PHYSICAL_RESIDUAL_CANDIDATE",
            "BLOCKED_NEEDS_ALPHA_BOUND",
        ),
        (
            "XMAP1505_1_memory_history_kernel",
            "memory_history_kernel",
            "nonlocal or history-tail residual projected into local fifth-force envelope",
            "vertical only if local tail is relative-exact/boundary-null; current contract marks it template-invalid",
            "CONDITIONAL_VERTICAL_CANDIDATE",
            "BLOCKED_NEEDS_TAIL_ENVELOPE",
        ),
        (
            "XMAP1505_2_Cperp_exact_rep",
            "Cperp / representative-exact residual",
            "raw representative shift in ker(P_D) or relative-exact sector",
            "safe beta-zero route if exactness, boundary, and presymplectic-null premises are parent-owned",
            "BEST_VERTICAL_ROUTE",
            "CONDITIONAL_NOT_PARENT_SIGNED",
        ),
        (
            "XMAP1505_3_projected_class_CD",
            "C_D or projected class observable",
            "class/projected observable seen by the matter metric",
            "not vertical by definition; if X_a changes C_D then beta can be physical",
            "NOT_VERTICAL_IF_ACTIVE",
            "REQUIRES_BETA_BOUND_OR_LOCAL_EXTREMUM",
        ),
        (
            "XMAP1505_4_fibre_active_readout",
            "fixed active-cell readout / P_active",
            "basis or cell active readout",
            "not a quotient observable unless dressed relationally; material marker route reopens couplings",
            "QUOTIENT_HAZARD",
            "BLOCKED_BY_MARKER_COUNTERMODEL",
        ),
        (
            "XMAP1505_5_no_range_zero",
            "no_range_zero theorem target",
            "operator/source/boundary/Hamiltonian projection all zero",
            "would remove R10 alpha without needing beta, but current inputs are missing",
            "THEOREM_ZERO_TARGET",
            "NOT_DERIVED",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "map_id": map_id,
            "candidate_X": candidate,
            "interpretation": interpretation,
            "verticality_readout": readout,
            "route_type": route_type,
            "current_status": status,
            **flags(),
        }
        for map_id, candidate, interpretation, readout, route_type, status in candidates
    ]


def verticality_test_rows() -> list[dict[str, Any]]:
    tests = [
        ("DQT1505_0_define_q", "q(Phi)=(e_obs,g_obs,source/readout data)", "explicit parent quotient/readout map exists", "PARTIAL_PRIOR_CONTRACT"),
        ("DQT1505_1_define_X", "X_a", "R10-active residual field is declared in parent tangent space", "MISSING_UNIFIED_X_BASIS"),
        ("DQT1505_2_apply_Dq", "Dq[X_a]", "compute quotient derivative rather than name verticality", "MISSING_COMPUTATION"),
        ("DQT1505_3_kernel_zero", "Dq[X_a]=0", "beta-zero acceptance test", "MISSING"),
        ("DQT1505_4_no_source_charge", "Q_X_source=q_test_X=0 or bounded", "vertical-to-matter is not enough if source/test charges survive", "MISSING"),
        ("DQT1505_5_no_marker", "no material marker or fixed active spurion", "quotient not reopened by extended marker state", "MISSING_PARENT_EXCLUSION"),
        ("DQT1505_6_effective_action", "effective corrections descend to quotient", "post-gauge-fix EFT does not reintroduce active beta/coupling", "OPEN"),
        ("DQT1505_7_boundary_readout", "R10 readout/projection silent or bounded", "arena projection cannot reintroduce beta-like response", "MISSING"),
        ("DQT1505_8_acceptance", "beta_a=0 or alpha_a=0", "allowed only if DQT1505_0 through DQT1505_7 close", "BLOCKED"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "test_id": test_id,
            "object": obj,
            "acceptance_test": acceptance,
            "current_status": status,
            **flags(),
        }
        for test_id, obj, acceptance, status in tests
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1505_0_vertical_residual_safe",
            "statement": "If X_a is a relative-exact or presymplectic-null representative direction, Dq[X_a]=0, no direct fixed-coframe matter vertex exists, and source/test charges vanish, then the R10 direct matter beta and alpha channel are zero to first order.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_sketch": "Dq[X_a]=0 kills the coframe pullback; no direct vertex kills fixed-frame matter variation; zero source/test charge kills the residual Yukawa force law.",
            "current_claim_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1505_1_vertical_to_coframe_not_enough",
            "statement": "Dq[X_a]=0 for the observed coframe is not by itself an R10 pass if X_a still carries source charge, test charge, marker readout, boundary flux, or finite-range operator response.",
            "proof_status": "COUNTERMODEL_ACTIVE",
            "proof_sketch": "A field can be invisible to e_obs but couple through an explicit source/test charge sector; then beta_a=0 while alpha_X(lambda) is still nonzero.",
            "current_claim_status": "BLOCKS_BETA_ONLY_SHORTCUT",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1505_2_current_branch_verdict",
            "statement": "Current evidence does not map the R10-active residual into ker(Dq) with zero source/test charge; therefore the beta/C route remains closure-bound rather than derived-zero.",
            "proof_status": "DERIVED_AS_GATE_LOGIC",
            "proof_sketch": "Prior quotient files give conditional routes and no-go warnings; the live R10 curve/kernel and C_parent imports remain absent.",
            "current_claim_status": "KEEP_BETA_AND_ALPHA_CLOSURE_BOUND",
            **flags(),
        },
    ]


def beta_bound_rows() -> list[dict[str, Any]]:
    rows = [
        ("BBOUND1505_0", "component_id", "R10_active_X_component", "MISSING_R10_FIELD_MAP"),
        ("BBOUND1505_1", "Dq_X", "0 if quotient-vertical, else numeric/functional derivative", "MISSING"),
        ("BBOUND1505_2", "beta_a", "partial ln e_obs / partial X_a", "MISSING_OR_DERIVED_ZERO_REQUIRED"),
        ("BBOUND1505_3", "Q_X_source", "source charge of X_a", "MISSING_OR_DERIVED_ZERO_REQUIRED"),
        ("BBOUND1505_4", "q_test_X", "test-body charge/readout of X_a", "MISSING_OR_DERIVED_ZERO_REQUIRED"),
        ("BBOUND1505_5", "alpha_X_lambda", "source-normalized R10 alpha prediction", "MISSING_SOURCE_NORMALIZED_ALPHA_LAMBDA_CURVE"),
        ("BBOUND1505_6", "claim_rule", "valid_for_claim only after all coefficients are real/zero and source-backed", "NONCLAIM_SCHEMA_ONLY"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": row_id,
            "field": field,
            "required_value_or_policy": policy,
            "current_status": status,
            "source_path": "MISSING_SOURCE_FILE",
            **flags(),
        }
        for row_id, field, policy, status in rows
    ]


def alpha_route_rows() -> list[dict[str, Any]]:
    rows = [
        ("AR1505_0_theorem_zero", "Dq[X]=0 plus Q_X=q_test=0 plus boundary/readout silence", "would give alpha_X(lambda)=0", "NOT_CLOSED"),
        ("AR1505_1_bound_route", "finite beta/source/test charge with source-backed alpha(lambda) rows", "empirical R10 comparison possible", "MISSING_INPUTS"),
        ("AR1505_2_no_range_route", "operator/source/boundary/Hamiltonian projection all zero", "R10 inactive without curve", "NOT_DERIVED"),
        ("AR1505_3_live_claim_route", "reviewed bound curve and kernel target populated", "runner can score", "LIVE_TARGETS_ABSENT"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "route_id": route_id,
            "route": route,
            "effect_if_closed": effect,
            "current_status": status,
            **flags(),
        }
        for route_id, route, effect, status in rows
    ]


def formula_rows() -> list[dict[str, Any]]:
    formulas = [
        ("FORM1505_0_verticality", "Dq[X_a]=0", "coframe beta-zero condition"),
        ("FORM1505_1_chain_rule", "delta_X e_obs = De_obs[Dq[X_a]]", "why verticality kills beta"),
        ("FORM1505_2_beta", "beta_a=partial ln e_obs/partial X_a", "direct matter readout"),
        ("FORM1505_3_source_charge_caveat", "alpha_X(lambda) ~ Q_X_source q_test_X/(G_N M m)", "vertical-to-coframe is not source-charge zero"),
        ("FORM1505_4_full_R10_zero", "Dq[X_a]=0 and Q_X_source=q_test_X=boundary_flux=tau_R10=0 => alpha_X=0", "safe theorem-zero shape"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "formula_id": formula_id,
            "formula": formula,
            "status": status,
            **flags(),
        }
        for formula_id, formula, status in formulas
    ]


def blocker_rows() -> list[dict[str, Any]]:
    blockers = [
        ("BLK1505_0_q", "MISSING_EXPLICIT_Q_MAP", "q(Phi) for observed coframe/source/readout remains partial", "parent_action"),
        ("BLK1505_1_X", "MISSING_R10_ACTIVE_X_BASIS", "R10-active residual field direction is not mapped in parent tangent space", "parent_action"),
        ("BLK1505_2_Dq", "MISSING_DQ_X_ZERO_COMPUTATION", "Dq[X_a]=0 has not been computed", "parent_action"),
        ("BLK1505_3_source_charge", "MISSING_SOURCE_TEST_CHARGE_ZERO_OR_VALUE", "beta zero is insufficient if X carries source/test charge", "parent_action"),
        ("BLK1505_4_marker", "MISSING_NO_MARKER_NO_SPURION_PROOF", "quotient route can be reopened by material marker/fixed readout", "parent_action"),
        ("BLK1505_5_kernel", "MISSING_R10_KERNEL", "R10 finite-source kernel remains absent", rel(KERNEL_TARGET)),
        ("BLK1505_6_curve", "MISSING_REVIEWED_R10_CURVE", "R10 alpha(lambda) bound remains non-live", rel(CURVE_TARGET)),
        ("BLK1505_7_coeff", "MISSING_BETA_C_COEFFICIENT_IMPORT", "no live beta/C row satisfies source/units/sign/basis", rel(C_PARENT_IMPORT)),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "blocking_marker": marker,
            "reason": reason,
            "target_path": target,
            **flags(),
        }
        for blocker_id, marker, reason, target in blockers
    ]


def simple_rows_from_blockers(blockers: list[dict[str, Any]], prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            f"{prefix}_id": f"{prefix.upper()}1505_{index}",
            "object": row["blocking_marker"],
            "path": row["target_path"],
            "status": "BLOCKED",
            "effect": row["reason"],
            **flags(),
        }
        for index, row in enumerate(blockers)
    ]


def c_parent_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "refusal_id": "CP1505_0_no_import",
            "path": rel(C_PARENT_IMPORT),
            "path_exists": C_PARENT_IMPORT.exists(),
            "imported_now": False,
            "reason": "1505 does not import beta/C because Dq[X] and source/test charges remain unmapped",
            "claim_effect": "R10/local-GR claim remains blocked",
            **flags(),
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    decisions = [
        ("DEC1505_0_keep_vertical_lemma", "keep quotient-verticality as the clean beta-zero theorem route", "the chain-rule proof is exact"),
        ("DEC1505_1_reject_beta_only_pass", "do not treat Dq[X]=0 as full R10 pass unless source/test charges also vanish", "R10 is a force test, not just a coframe-pullback test"),
        ("DEC1505_2_next", "derive source/test charge zero or build executable alpha row", "this is the next unavoidable local-GR/R10 fork"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, rationale in decisions
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1505_0_1506",
            "next_target": "1506-Y5-R10-RAB-source-test-charge-zero-or-executable-alpha-row.md",
            "script": "scripts/Y5_R10_RAB_source_test_charge_zero_or_executable_alpha_row.py",
            "objective": "try to prove Q_X_source=q_test_X=0 for R10-active residuals; if not, prepare executable nonclaim alpha(lambda) rows with beta/s/Z/source paths",
            **flags(),
        }
    ]


def generated_flags_false(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for column in ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]:
                value = row.get(column)
                if value not in (None, "", "False", "false", False):
                    return False
    return True


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    for src, dst in [
        (FIELD_MAP_AUDIT, QUAR_FIELD_MAP),
        (VERTICALITY_TESTS, QUAR_VERTICALITY),
        (THEOREM_LEDGER, QUAR_THEOREM),
        (BETA_BOUND_ROWS, QUAR_BOUND),
        (FIELD_MAP_AUDIT, BRANCH_FIELD_MAP),
        (VERTICALITY_TESTS, BRANCH_VERTICALITY),
        (THEOREM_LEDGER, BRANCH_THEOREM),
        (BETA_BOUND_ROWS, BRANCH_BOUND),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], theorem: list[dict[str, Any]], verticality: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values())
    exact_theorem = any(row["theorem_id"] == "THM1505_0_vertical_residual_safe" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem)
    beta_only_countermodel = any(row["theorem_id"] == "THM1505_1_vertical_to_coframe_not_enough" and row["proof_status"] == "COUNTERMODEL_ACTIVE" for row in theorem)
    acceptance_blocked = any(row["test_id"] == "DQT1505_8_acceptance" and row["current_status"] == "BLOCKED" for row in verticality)
    beta_bound_rows = BETA_BOUND_ROWS.exists() and len(read_csv(BETA_BOUND_ROWS)) >= 7
    live_targets_absent = not CURVE_TARGET.exists() and not KERNEL_TARGET.exists()
    c_parent_refused = read_csv(C_PARENT_REFUSAL)[0]["imported_now"] == "False"
    csv_parse_ok = all(parse_csv(path) for path in generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_FIELD_MAP, QUAR_VERTICALITY, QUAR_THEOREM, QUAR_BOUND, BRANCH_FIELD_MAP, BRANCH_VERTICALITY, BRANCH_THEOREM, BRANCH_BOUND])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    checks = [
        ("VAL1505_0_local_sources", source_paths_exist, "all cited quotient/R10 source paths exist"),
        ("VAL1505_1_exact_theorem", exact_theorem, "conditional quotient-vertical zero theorem recorded"),
        ("VAL1505_2_beta_only_countermodel", beta_only_countermodel, "Dq[X]=0 alone is not treated as full R10 pass"),
        ("VAL1505_3_acceptance_blocked", acceptance_blocked, "acceptance remains blocked until Dq/source/test/readout close"),
        ("VAL1505_4_beta_bound_rows", beta_bound_rows, "beta/source/test closure rows written"),
        ("VAL1505_5_live_targets_absent", live_targets_absent, "live R10 curve/kernel targets remain absent"),
        ("VAL1505_6_Cparent_refused", c_parent_refused, "C_parent import was not performed"),
        ("VAL1505_7_csv_parse", csv_parse_ok, "all generated 1505 CSVs parse cleanly"),
        ("VAL1505_8_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1505_9_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1505_10_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
        ("VAL1505_11_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1505_12_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1505 mapped the quotient-vertical beta-zero route and kept R10 blocked until source/test charges also close"
            if overall
            else "1505 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(
    field_map: list[dict[str, Any]],
    verticality: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    alpha_routes: list[dict[str, Any]],
    beta_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1505 - Map R10 Residual X to Quotient-Vertical Kernel or beta Bound",
                "",
                "## Verdict",
                "- The clean beta-zero route is exact: if the R10 residual is quotient-vertical and has no direct matter/source/test charge, the first-order R10 channel vanishes.",
                "- But verticality to the observed coframe alone is not a full R10 pass; source/test charges, markers, boundary flux, and finite-source projection can still generate alpha(lambda).",
                "- Current evidence does not map the R10-active residual X_a into ker(Dq), so beta/source/test coefficients remain closure-bound.",
                "",
                "## R10 Residual Field Map Audit",
                md_table(field_map, ["map_id", "candidate_X", "route_type", "current_status"]),
                "",
                "## Dq Verticality Tests",
                md_table(verticality, ["test_id", "object", "acceptance_test", "current_status"]),
                "",
                "## Quotient-Vertical Theorem Ledger",
                md_table(theorem, ["theorem_id", "proof_status", "current_claim_status"]),
                "",
                "## Alpha Route Matrix",
                md_table(alpha_routes, ["route_id", "route", "effect_if_closed", "current_status"]),
                "",
                "## beta/source/test Bound Rows",
                md_table(beta_rows, ["row_id", "field", "required_value_or_policy", "current_status"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    field_map = field_map_rows()
    verticality = verticality_test_rows()
    theorem = theorem_rows()
    beta_rows = beta_bound_rows()
    alpha_routes = alpha_route_rows()
    formulas = formula_rows()
    blockers = blocker_rows()
    readiness = simple_rows_from_blockers(blockers, "ready")
    c_parent = c_parent_refusal_rows()
    local_rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "local_status_id": "LRS1505_0",
            "object": "R10 quotient-vertical/local force branch",
            "status": "DQ_SOURCE_TEST_OR_ALPHA_BOUND_REQUIRED",
            "effect": "beta-zero route sharpened, but no local-GR/Newton/R10 claim",
            **flags(),
        }
    ]
    rejections = simple_rows_from_blockers(blockers, "rejection")
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(FIELD_MAP_AUDIT, field_map)
    write_csv(VERTICALITY_TESTS, verticality)
    write_csv(THEOREM_LEDGER, theorem)
    write_csv(BETA_BOUND_ROWS, beta_rows)
    write_csv(ALPHA_ROUTE_MATRIX, alpha_routes)
    write_csv(FORMULA_REGISTER, formulas)
    write_csv(TARGET_BLOCKERS, blockers)
    write_csv(SCORE_READINESS, readiness)
    write_csv(C_PARENT_REFUSAL, c_parent)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()

    generated_csvs = [
        FIELD_MAP_AUDIT,
        VERTICALITY_TESTS,
        THEOREM_LEDGER,
        BETA_BOUND_ROWS,
        ALPHA_ROUTE_MATRIX,
        FORMULA_REGISTER,
        TARGET_BLOCKERS,
        SCORE_READINESS,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, theorem, verticality)
    write_csv(VALIDATION, validation)
    write_doc(field_map, verticality, theorem, alpha_routes, beta_rows, validation, next_rows)
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()

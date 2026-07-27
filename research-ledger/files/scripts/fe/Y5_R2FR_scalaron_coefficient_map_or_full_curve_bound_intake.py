from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1588"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1588-Y5-R2FR-scalaron-coefficient-map-or-full-curve-bound-intake.md"

SOURCE_FILES = {
    "1587_doc": ROOT / "1587-Y5-R11-beta-vector-first-component-fill-R2FR-RicciWeyl-or-nohair.md",
    "1587_validation": OUT / "P8_Y5_BRR545_1587_VALIDATION.csv",
    "1587_fill": OUT / "P8_Y5_PARENT_QLOC_1587_FIRST_COMPONENT_FILL_ROWS.csv",
    "962_scalar_fallback": OUT / "P8_Y5_R10_962_SCALAR_BOUND_FALLBACK_ROWS.csv",
    "963_runner_spec": OUT / "P8_Y5_R10_963_R2FR_BOUND_RUNNER_SPEC.csv",
    "963_coefficient_owner": OUT / "P8_Y5_R10_963_R2FR_COEFFICIENT_OWNER_AUDIT.csv",
    "965_curve_manifest": OUT / "P8_Y5_R10_965_R2FR_FULL_CURVE_INTAKE_MANIFEST.csv",
    "review_candidate": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
    "review_qa": LOCAL_BOUNDS / "P8_Y5_R10_570_REVIEW_CANDIDATE_QA.csv",
    "review_summary": LOCAL_BOUNDS / "P8_Y5_R10_570_REVIEW_CURVE_SUMMARY.csv",
    "live_digitized": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
    "anchor_smoke": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv",
    "local_bounds": LOCAL_BOUNDS / "local_bound_claims.csv",
}

NEEDLES = {
    "1587_doc": ["NEXT_1588_R2FR_SCALARON_COEFFICIENT_MAP_OR_FULL_CURVE_BOUND_INTAKE", "FC1587_0_R2FR"],
    "1587_validation": ["VAL1587_OVERALL", "PASS"],
    "1587_fill": ["FC1587_0_R2FR", "MISSING_PARENT_COEFFICIENT_AND_FULL_CURVE"],
    "962_scalar_fallback": ["R2B962_1_fR_unscreened_map", "1/3_if_simple_unscreened_metric_fR"],
    "963_runner_spec": ["R2RUN963_0_model_input", "MISSING_PARENT_INPUT"],
    "963_coefficient_owner": ["CO963_4_verdict", "NO_EXECUTABLE_OWNER_FOUND"],
    "965_curve_manifest": ["R2FC965_0_Lee2020_full_curve_required", "R2FC965_3_MTS_R2FR_prediction_required"],
    "review_candidate": ["R10_VECTOR_2020_REVIEW_0000", "review_candidate_only_requires_official_supplement_or_human_visual_QA"],
    "review_qa": ["QA570_2_promotion_gate", "blocked=2"],
    "review_summary": ["CS570_0_rows", "390"],
    "live_digitized": ["MISSING_DIGITIZED_ALPHA_BOUND", "R10_BOUND_PLACEHOLDER_0"],
    "anchor_smoke": ["R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM", "R10_ANCHOR_EOTWASH_2007_ALPHA1_56UM"],
    "local_bounds": ["Will_2014_PPN_beta_table", "beta_minus_1", "7.8e-05"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1588_SOURCE_REGISTER.csv"
SCALARON_MAP = OUT / "P8_Y5_PARENT_QLOC_1588_R2FR_SCALARON_MAP.csv"
CURVE_INTAKE = OUT / "P8_Y5_PARENT_QLOC_1588_FULL_CURVE_INTAKE_STATUS.csv"
SMOKE_ROWS = OUT / "P8_Y5_PARENT_QLOC_1588_R2FR_NONCLAIM_SMOKE_ROWS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1588_R2FR_SCALARON_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1588_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1588_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1588_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1588_VALIDATION.csv"

COPY_TARGETS = {
    SCALARON_MAP: [
        QUARANTINE / "R2FR_SCALARON_MAP_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_scalaron_map_nonclaim_1588.csv",
    ],
    CURVE_INTAKE: [
        QUARANTINE / "FULL_CURVE_INTAKE_STATUS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_full_curve_intake_status_nonclaim_1588.csv",
    ],
    SMOKE_ROWS: [
        QUARANTINE / "R2FR_NONCLAIM_SMOKE_ROWS.csv",
        BRANCH_RESIDUALS / "R2FR_nonclaim_smoke_rows_1588.csv",
    ],
    RUNNER: [
        QUARANTINE / "R2FR_SCALARON_RUNNER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_scalaron_runner_nonclaim_1588.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_scalaron_or_full_curve_decision_nonclaim_1588.csv",
    ],
}


def flags() -> dict[str, bool]:
    return {
        "parent_signed": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source_index, (source_key, source_path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1588_{source_index}_{source_key}",
                "source_path": rel(source_path),
                "exists": source_path.exists(),
                "needle_found": file_contains(source_path, NEEDLES[source_key]),
                "needles": "; ".join(NEEDLES[source_key]),
                "purpose": "R2/fR scalaron coefficient map or full curve bound intake",
                **flags(),
            }
        )
    return rows


def scalaron_map_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SC1588_0_parent_zero",
            "parent theorem-zero route",
            "c_R2=c_fR=0 if the parent local exterior is metric-only, second-order and no-extra-scalar",
            "lambda_s=0-equivalent/no finite scalaron range; alpha_s=0 for the removed branch",
            "ZERO_THEOREM_UNSIGNED",
            "parent activator still missing from 963/964/1587",
        ),
        (
            "SC1588_1_formula",
            "finite scalaron formula",
            "for f(R)=R+c_R2 R^2 around flat space, m_s^2=1/(6 c_R2), lambda_s=sqrt(6 c_R2) in c=hbar=1 units",
            "maps a sourced c_R2/fRR into scalar range",
            "FORMULA_AVAILABLE_PARENT_COEFFICIENT_MISSING",
            "c_R2/fRR value, units and normalization are missing",
        ),
        (
            "SC1588_2_coupling",
            "simple unscreened metric f(R) coupling",
            "alpha_s=1/3 only for the simple unscreened metric f(R) scalar with universal matter coupling",
            "would give the Yukawa amplitude convention for R10 only under stated regime",
            "CONDITIONAL_COUPLING_NOT_MTS_PREDICTION",
            "screening flag, matter coupling and branch context are missing",
        ),
        (
            "SC1588_3_units_sign",
            "coefficient units and sign guard",
            "c_R2 has length^2/inverse-mass-squared units after EH normalization; c_R2>0 is required for non-tachyonic scalaron in the simple branch",
            "prevents dimensionless or sign-ambiguous curve scoring",
            "MISSING_UNITS_AND_SIGN_CONVENTION",
            "no parent coefficient row supplies units or sign",
        ),
        (
            "SC1588_4_screening_regime",
            "screening and solar-system regime",
            "R10/PPN scoring requires unscreened/screened context, source/test coupling, and whether the scalar range lies in lab or solar-system regime",
            "prevents transferring alpha(lambda) anchors into PPN or beta by hand",
            "MISSING_SCREENING_AND_REGIME_MAP",
            "no scalar environment/readout map exists",
        ),
        (
            "SC1588_5_verdict",
            "MTS R2/fR scalaron prediction",
            "c_R2/fRR, lambda_s, alpha_s, screening flag, source path and normalization all present",
            "would create a nonclaim prediction row eligible for strict curve comparison",
            "FAIL_CURRENT_CLAIM_NO_SCALARON_PREDICTION",
            "formula exists, but the MTS coefficient does not",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "map_id": map_id,
            "map_piece": map_piece,
            "formula_or_rule": formula_or_rule,
            "effect_if_filled": effect_if_filled,
            "status": status,
            "blocking_gap": blocking_gap,
            **flags(),
        }
        for map_id, map_piece, formula_or_rule, effect_if_filled, status, blocking_gap in rows
    ]


def curve_intake_rows() -> list[dict[str, Any]]:
    review_rows = read_csv(SOURCE_FILES["review_candidate"])
    live_rows = read_csv(SOURCE_FILES["live_digitized"])
    anchor_rows = read_csv(SOURCE_FILES["anchor_smoke"])
    rows = [
        (
            "CURVE1588_0_live_digitized",
            "live claim curve",
            rel(SOURCE_FILES["live_digitized"]),
            len(live_rows),
            "placeholder_invalid",
            "MISSING_DIGITIZED_ALPHA_BOUND rows remain in the live file",
            "BLOCKED_NOT_A_CURVE",
        ),
        (
            "CURVE1588_1_review_candidate",
            "2020 Eot-Wash vector review candidate",
            rel(SOURCE_FILES["review_candidate"]),
            len(review_rows),
            "review_candidate_nonclaim",
            "axis-calibrated 390-row candidate exists, but promotion gate requires official supplement or human visual QA",
            "AVAILABLE_FOR_SMOKE_NOT_CLAIM",
        ),
        (
            "CURVE1588_2_anchor_smoke",
            "anchor-only smoke rows",
            rel(SOURCE_FILES["anchor_smoke"]),
            len(anchor_rows),
            "anchor_only_non_curve",
            "2020 and 2007 alpha=1 thresholds are source-backed anchors only",
            "BLOCKED_ANCHOR_ONLY",
        ),
        (
            "CURVE1588_3_required_promotion",
            "claim-grade bound curve",
            "official supplemental table or review candidate promotion package",
            0,
            "required_for_claim",
            "positive numeric lambda/alpha rows, source URL/DOI, extraction method, curve identity, visual/official QA and valid_for_claim=true",
            "MISSING_PROMOTED_FULL_CURVE",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "curve_id": curve_id,
            "curve_type": curve_type,
            "path_or_source": path_or_source,
            "row_count": row_count,
            "curve_status": curve_status,
            "evidence": evidence,
            "status": status,
            **flags(),
        }
        for curve_id, curve_type, path_or_source, row_count, curve_status, evidence, status in rows
    ]


def smoke_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SMOKE1588_0_formula_only",
            "finite scalaron formula row",
            "lambda_s=sqrt(6 c_R2), alpha_s=1/3 if simple unscreened metric f(R)",
            "MISSING_C_R2_OR_FRR",
            "REJECTED_MISSING_MTS_PREDICTION",
        ),
        (
            "SMOKE1588_1_anchor_backsolve",
            "set lambda_s=38.6um because alpha=1 anchor exists",
            "backsolves a prediction from the bound",
            "FORBIDDEN_BOUND_TO_PREDICTION_INVERSION",
            "REJECTED_CLOSURE_ONLY",
        ),
        (
            "SMOKE1588_2_review_candidate_curve",
            "use 390-row review candidate curve for smoke only",
            "candidate rows are valid_for_claim=false and MTS prediction is absent",
            "NONCLAIM_CURVE_ONLY",
            "NOT_SCORED",
        ),
        (
            "SMOKE1588_3_parent_zero_if_signed",
            "zero theorem route",
            "if parent activator signs, c_R2=c_fR=0 and finite R2/fR scalar branch is absent",
            "ZERO_THEOREM_UNSIGNED",
            "REJECTED_UNTIL_PARENT_SIGNED",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "smoke_id": smoke_id,
            "case": case,
            "input_or_formula": input_or_formula,
            "blocking_gap": blocking_gap,
            "verdict": verdict,
            **flags(),
        }
        for smoke_id, case, input_or_formula, blocking_gap, verdict in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1588_0_parent_zero", "score parent zero theorem route", "NOT_RUN_ZERO_THEOREM_UNSIGNED", "parent second-order/no-extra-scalar/minimality activator is not signed"),
        ("RUN1588_1_scalaron_prediction", "build MTS alpha/lambda prediction", "NOT_RUN_COMPONENTS_MISSING", "c_R2/fRR, units, normalization, alpha_s and screening flag are missing"),
        ("RUN1588_2_live_curve", "score against live digitized curve", "NOT_RUN_PLACEHOLDER_CURVE", "live file contains placeholder MISSING_DIGITIZED_ALPHA_BOUND rows"),
        ("RUN1588_3_review_candidate", "smoke against review candidate curve", "NOT_RUN_PREDICTION_MISSING", "review candidate exists but valid_for_claim=false and no MTS prediction exists"),
        ("RUN1588_4_anchor_rows", "score using alpha=1 anchors", "REFUSE_ANCHOR_ONLY_SCORING", "anchor thresholds are not a full alpha(lambda) curve"),
        ("RUN1588_5_beta_local_gr", "claim beta/local-GR from R2/fR handling", "BLOCKED_NO_CLAIM", "R2/fR scalar branch, R11 vector, source normalization and local-GR gates remain open"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "can_score": False,
            **flags(),
        }
        for runner_id, case, status, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1588_0_parent_zero", "R2/fR theorem-zero", "BLOCKED_NO_CLAIM", "parent zero activator remains unsigned"),
        ("GATE1588_1_scalaron_prediction", "MTS scalaron alpha/lambda prediction", "BLOCKED_NO_CLAIM", "c_R2/fRR, lambda_s and alpha_s are missing"),
        ("GATE1588_2_full_curve", "claim-grade R10 bound curve", "BLOCKED_NO_CLAIM", "live curve is placeholder; review candidate and anchors are nonclaim"),
        ("GATE1588_3_R10_score", "finite R2/fR R10 score", "BLOCKED_NO_CLAIM", "prediction and claim-grade curve are both missing"),
        ("GATE1588_4_beta_local_gr", "beta/local-GR promotion", "BLOCKED_NO_CLAIM", "R2/fR handling alone does not close the R11/source/matter/conservation gates"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1588_0_formula_status",
            "SCALARON_FORMULA_AVAILABLE_NOT_MTS_PREDICTION",
            "the R2/fR scalaron formula and simple alpha_s=1/3 convention exist, but no parent c_R2/fRR coefficient exists",
            "do not create an alpha/lambda prediction row",
        ),
        (
            "DEC1588_1_curve_status",
            "REVIEW_CURVE_AVAILABLE_NONCLAIM_LIVE_CURVE_PLACEHOLDER",
            "a 390-row review candidate exists and anchors exist, but promotion is blocked and the live curve remains placeholder",
            "do not score claims; use candidate only for future smoke after prediction exists",
        ),
        (
            "DEC1588_2_priority",
            "MTS_COEFFICIENT_SIDE_IS_NOW_THE_BOTTLENECK",
            "without c_R2/fRR, even a perfect full curve cannot test the branch",
            "hunt parent coefficient/scalaron normalization before spending effort on curve promotion",
        ),
        (
            "DEC1588_3_next",
            "NEXT_1589_R2FR_PARENT_COEFFICIENT_SOURCE_HUNT_OR_CURVE_QA_PROMOTION",
            "the next step should try to derive/source c_R2/fRR from the R11 parent branch; if that fails, prepare strict curve-promotion QA as a separate nonclaim utility",
            "derive coefficient first; curve QA second; no anchor-only score",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            **flags(),
        }
        for decision_id, decision, reason, consequence in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1589-Y5-R2FR-parent-coefficient-source-hunt-or-curve-QA-promotion.md",
            "script": "scripts/Y5_R2FR_parent_coefficient_source_hunt_or_curve_QA_promotion.py",
            "objective": "try to derive or source c_R2/fRR from the parent R11 branch; if unavailable, build the exact curve QA/promotion gate for the existing 390-row Eot-Wash 2020 review candidate without claim promotion",
            "do_not": "do not backsolve c_R2 from R10 anchors, do not score review-candidate curves as claims, and do not promote beta/local-GR from formula-only rows",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def generated_flags_false(generated_csvs: list[Path]) -> bool:
    flag_columns = {"score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"}
    for csv_path in generated_csvs:
        for row in read_csv(csv_path):
            for flag_column in flag_columns.intersection(row):
                if row[flag_column] != "False":
                    return False
    return True


def formalization_scope_clean(generated_csvs: list[Path]) -> bool:
    if any(FORMALIZATION in csv_path.parents for csv_path in generated_csvs):
        return False
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT.parent), "status", "--short", "--", "formalization-workbench"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return True
    if result.returncode != 0:
        return True
    return len([line for line in result.stdout.splitlines() if line.strip()]) == 0


def has_1588_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1588" in csv_path.name for csv_path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    scalaron = read_csv(SCALARON_MAP)
    curves = read_csv(CURVE_INTAKE)
    smoke = read_csv(SMOKE_ROWS)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    required_claims = {
        "R2/fR theorem-zero",
        "MTS scalaron alpha/lambda prediction",
        "claim-grade R10 bound curve",
        "finite R2/fR R10 score",
        "beta/local-GR promotion",
    }
    checks = [
        ("VAL1588_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1588 source paths exist"),
        ("VAL1588_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all 1588 source needles found"),
        (
            "VAL1588_2_scalaron_map_blocks",
            any(row["map_id"] == "SC1588_5_verdict" and row["status"] == "FAIL_CURRENT_CLAIM_NO_SCALARON_PREDICTION" for row in scalaron),
            "scalaron formula exists but no MTS prediction is promoted",
        ),
        (
            "VAL1588_3_curve_intake_blocks",
            any(row["curve_id"] == "CURVE1588_0_live_digitized" and row["status"] == "BLOCKED_NOT_A_CURVE" for row in curves)
            and any(row["curve_id"] == "CURVE1588_1_review_candidate" and row["status"] == "AVAILABLE_FOR_SMOKE_NOT_CLAIM" and row["row_count"] == "390" for row in curves),
            "live curve is placeholder while 390-row review candidate remains nonclaim",
        ),
        (
            "VAL1588_4_smoke_rows_nonclaim",
            all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in smoke)
            and any(row["smoke_id"] == "SMOKE1588_1_anchor_backsolve" and row["verdict"] == "REJECTED_CLOSURE_ONLY" for row in smoke),
            "smoke rows reject anchor backsolve and remain nonclaim",
        ),
        (
            "VAL1588_5_runner_blocks",
            all(row["can_score"] == "False" for row in runner)
            and any(row["runner_id"] == "RUN1588_5_beta_local_gr" and row["status"] == "BLOCKED_NO_CLAIM" for row in runner),
            "runner blocks parent-zero, scalaron, curve and local-GR scoring",
        ),
        (
            "VAL1588_6_claim_gates_closed",
            {row["claim"] for row in gates} == required_claims
            and all(row["claim_allowed"] == "False" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates),
            "all 1588 claim gates remain closed",
        ),
        (
            "VAL1588_7_decision_next",
            any(row["decision"] == "NEXT_1589_R2FR_PARENT_COEFFICIENT_SOURCE_HUNT_OR_CURVE_QA_PROMOTION" for row in decisions),
            "decision selects parent coefficient hunt or curve QA promotion",
        ),
        ("VAL1588_8_csv_parse", all(len(read_csv(csv_path)) > 0 for csv_path in generated_csvs), "all generated 1588 CSVs parse cleanly"),
        ("VAL1588_9_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1588_10_no_raw_accepted", not has_1588_rows(RAB_RAW) and not has_1588_rows(RAB_ACCEPTED), "no 1588 rows written to raw/accepted finite directories"),
        ("VAL1588_11_branch_copies", all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths), "branch/quarantine nonclaim copies written"),
        ("VAL1588_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1588_13_formalization_untouched", formalization_scope_clean(generated_csvs), "all generated 1588 paths are outside formalization-workbench; git status is clean when available"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1588_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1588 R2/fR scalaron coefficient map or full curve bound intake validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, Any]],
    scalaron: list[dict[str, Any]],
    curves: list[dict[str, Any]],
    smoke: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1588 - R2/fR Scalaron Coefficient Map Or Full Curve Bound Intake",
                "## Verdict\n"
                "- The scalaron formula is now wired into the R11 beta path: for simple `f(R)=R+c_R2 R^2`, `m_s^2=1/(6 c_R2)`, `lambda_s=sqrt(6 c_R2)`, and `alpha_s=1/3` only in the simple unscreened metric-f(R) regime.\n"
                "- Current MTS still has no parent-owned `c_R2/fRR` value, units, sign, normalization, screening flag or source path, so no alpha/lambda prediction row is valid.\n"
                "- The R10 external side is better than empty but still nonclaim: the live curve is placeholder, the 2020 390-row vector curve is a review candidate, and the alpha=1 anchors are not a full curve.\n"
                "- Anchor backsolves are explicitly refused; the coefficient side is now the bottleneck before curve scoring can matter.\n"
                "- No R2/fR, R10, beta, EH, Newton, PPN, local-GR, WEP, clock, orbital, conservation or common-matter claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Scalaron Map",
                md_table(scalaron, ["map_id", "map_piece", "formula_or_rule", "effect_if_filled", "status", "blocking_gap"]),
                "## Full Curve Intake Status",
                md_table(curves, ["curve_id", "curve_type", "path_or_source", "row_count", "curve_status", "status", "evidence"]),
                "## Nonclaim Smoke Rows",
                md_table(smoke, ["smoke_id", "case", "input_or_formula", "blocking_gap", "verdict"]),
                "## Scalaron Runner",
                md_table(runner, ["runner_id", "case", "status", "reason", "can_score"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "consequence"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    scalaron = scalaron_map_rows()
    curves = curve_intake_rows()
    smoke = smoke_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        SCALARON_MAP,
        CURVE_INTAKE,
        SMOKE_ROWS,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(SCALARON_MAP, scalaron)
    write_csv(CURVE_INTAKE, curves)
    write_csv(SMOKE_ROWS, smoke)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, scalaron, curves, smoke, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()

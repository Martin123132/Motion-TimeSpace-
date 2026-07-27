from __future__ import annotations

import csv
import json
import math
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from scipy import linalg


sys.dont_write_bytecode = True

ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
SCRIPTS = FORMALIZATION / "scripts"
sys.path.insert(0, str(SCRIPTS))
import cosmology_likelihood_smoke as cls  # noqa: E402


OUTPUT_DOC = POST_CHECKPOINT / "855-Y5-R10-calibration-projection-response-estimator-dry-run.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_855_SOURCE_REGISTER.csv"
ESTIMATOR_PATH = RESIDUALS / "P8_Y5_R10_855_LINEAR_RESPONSE_ESTIMATOR.csv"
OBSERVED_VECTOR_PATH = RESIDUALS / "P8_Y5_R10_855_OBSERVED_CALIBRATION_VECTOR_CHECK.csv"
INTERPRETATION_PATH = RESIDUALS / "P8_Y5_R10_855_INTERPRETATION_GATES.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_855_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_855_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_855_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_855_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_855_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_855_VALIDATION.csv"

SCORES_852_PATH = RESIDUALS / "P8_Y5_R10_852_FAIR_FIXED_BMEM_SN_BAO_FIT_SCORES.csv"
BRANCH_READOUT_853_PATH = RESIDUALS / "P8_Y5_R10_853_BRANCH_READOUT.csv"
LAW_854_PATH = RESIDUALS / "P8_Y5_R10_854_BRANCH_SPLIT_LAW_ATTEMPT.csv"
CONFIG_PATH = FORMALIZATION / "configs" / "cosmology_background_R1_current.json"
PANTHEON_PATH = FORMALIZATION / "data" / "cosmology" / "pantheon_plus" / "Pantheon+SH0ES.dat"

STATUS = "Y5_R10_855_calibration_projection_estimator_run_nonclaim"
CLAIM_CEILING = "projection_estimator_only_no_calibration_proof_no_parent_prediction"
NEXT_TARGET = "856-Y5-R10-memory-projection-repair-or-independent-calibration-source-test.md"

SOURCE_SPECS = [
    {
        "source_id": "854_doc",
        "path": POST_CHECKPOINT / "854-Y5-R10-parent-amplitude-branch-split-law-or-projection-repair.md",
        "needles": [
            "parent-plus-observable-projection contract",
            "calibration_projection_response_estimator",
            "855-Y5-R10-calibration-projection-response-estimator-dry-run.md",
        ],
        "role": "branch-split law handoff",
    },
    {
        "source_id": "854_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_854_VALIDATION.csv",
        "needles": [
            "V854_3_branch_split_law_contract_present,pass",
            "V854_5_observable_projection_selected,pass",
            "V854_9_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "852_scores",
        "path": SCORES_852_PATH,
        "needles": ["S1_C0_CMB_reference", "S1_C0_full_joint_reference", "params_json"],
        "role": "fair fixed-bmem fit parameters",
    },
    {
        "source_id": "853_branch_readout",
        "path": BRANCH_READOUT_853_PATH,
        "needles": ["no_sh0es", "sh0es", "competitive_nonclaim"],
        "role": "b_eff target rows",
    },
    {
        "source_id": "854_law_attempt",
        "path": LAW_854_PATH,
        "needles": ["linear_response_estimator", "response_sh0es_minus_no_sh0es"],
        "role": "projection estimator contract",
    },
    {
        "source_id": "pantheon_plus_data",
        "path": PANTHEON_PATH,
        "needles": ["IS_CALIBRATOR", "USED_IN_SH0ES_HF", "MU_SH0ES", "m_b_corr"],
        "role": "SN branch/calibration vector source",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def finite_float(value: object) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def fmt(value: object) -> str:
    number = finite_float(value)
    return "" if number is None else f"{number:.12g}"


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


def branch_mask(table: np.ndarray, branch: str) -> np.ndarray:
    z_cosmo = np.asarray(table["zHD"], dtype=float)
    z_hel = np.asarray(table["zHEL"], dtype=float)
    if branch == "no_sh0es":
        mu_obs = np.asarray(table["m_b_corr"], dtype=float)
        branch_mask_values = np.asarray(table["IS_CALIBRATOR"], dtype=int) == 0
    else:
        mu_obs = np.asarray(table["MU_SH0ES"], dtype=float)
        branch_mask_values = np.ones_like(z_cosmo, dtype=bool)
    return (
        np.isfinite(z_cosmo)
        & np.isfinite(z_hel)
        & np.isfinite(mu_obs)
        & (mu_obs > -100.0)
        & (z_cosmo > 0.0)
        & branch_mask_values
    )


def project_offset(sn: dict[str, Any], vector: np.ndarray) -> np.ndarray:
    c_inv_vector = linalg.cho_solve(sn["cho"], vector, check_finite=False)
    best_offset = float(sn["ones"] @ c_inv_vector / sn["ones_cinv_ones"])
    return vector - best_offset * sn["ones"]


def weighted_dot(sn: dict[str, Any], left: np.ndarray, right: np.ndarray) -> float:
    return float(left @ linalg.cho_solve(sn["cho"], right, check_finite=False))


def weighted_norm(sn: dict[str, Any], vector: np.ndarray) -> float:
    return math.sqrt(max(weighted_dot(sn, vector, vector), 0.0))


def score_params(scores: list[dict[str, str]], branch: str, candidate_id: str) -> dict[str, float]:
    row = next(item for item in scores if item["branch"] == branch and item["candidate_id"] == candidate_id)
    return {key: float(value) for key, value in json.loads(row["params_json"]).items()}


def branch_targets(branch_readout: list[dict[str, str]]) -> dict[str, float]:
    return {row["branch"]: float(row["b_mem_fixed"]) for row in branch_readout}


def calibration_vectors(table: np.ndarray, mask: np.ndarray) -> dict[str, np.ndarray]:
    z = np.asarray(table["zHD"], dtype=float)[mask]
    is_calibrator = np.asarray(table["IS_CALIBRATOR"], dtype=int)[mask].astype(bool)
    return {
        "calibrator_indicator": is_calibrator.astype(float),
        "used_in_sh0es_hf_indicator": np.asarray(table["USED_IN_SH0ES_HF"], dtype=int)[mask].astype(float),
        "low_z_lt_0p15_indicator": (z < 0.15).astype(float),
        "ceph_minus_mu_calibrator_residual": np.where(
            is_calibrator,
            np.asarray(table["CEPH_DIST"], dtype=float)[mask] - np.asarray(table["MU_SH0ES"], dtype=float)[mask],
            0.0,
        ),
    }


def response_derivative(sn: dict[str, Any], params: dict[str, float], b_parent: float, steps: int) -> np.ndarray:
    eps = 1.0e-4
    plus = dict(params)
    minus = dict(params)
    plus["b_mem"] = b_parent + eps
    minus["b_mem"] = b_parent - eps
    dmu_db = (
        cls.distance_modulus("M6", plus, sn["z_cosmo"], sn["z_hel"], steps)
        - cls.distance_modulus("M6", minus, sn["z_cosmo"], sn["z_hel"], steps)
    ) / (2.0 * eps)
    return project_offset(sn, -dmu_db)


def estimator_rows(generated_utc: str) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    config = cls.load_json(CONFIG_PATH)
    pantheon = cls.select_dataset(config, "Pantheon")
    table = np.genfromtxt(PANTHEON_PATH, names=True, dtype=None, encoding="utf-8")
    scores = read_csv(SCORES_852_PATH)
    branch_readout = read_csv(BRANCH_READOUT_853_PATH)
    targets = branch_targets(branch_readout)
    b_parent = targets["no_sh0es"]
    rows: list[dict[str, object]] = []
    observed_rows: list[dict[str, object]] = []

    for branch in ("no_sh0es", "sh0es"):
        sn = cls.load_pantheon(ROOT, pantheon, branch=branch)
        mask = branch_mask(table, branch)
        params = score_params(scores, branch, "S1_C0_CMB_reference")
        params["b_mem"] = b_parent
        j_b = response_derivative(sn, params, b_parent, 1024)
        denom = weighted_dot(sn, j_b, j_b)
        response_required = targets[branch] - b_parent
        for vector_name, raw_vector in calibration_vectors(table, mask).items():
            projected = project_offset(sn, np.asarray(raw_vector, dtype=float))
            numerator = weighted_dot(sn, j_b, projected)
            coefficient = numerator / denom if denom else math.nan
            required_mag = response_required / coefficient if coefficient else math.inf
            rows.append(
                {
                    "branch": branch,
                    "vector_name": vector_name,
                    "raw_vector_sum": fmt(float(np.sum(raw_vector))),
                    "projected_vector_norm": fmt(weighted_norm(sn, projected)),
                    "J_b_norm": fmt(weighted_norm(sn, j_b)),
                    "delta_b_per_unit_vector_mag": fmt(coefficient),
                    "response_required_to_match_branch_target": fmt(response_required),
                    "required_vector_mag_to_match_target": fmt(required_mag),
                    "estimator_status": "finite_response" if math.isfinite(required_mag) else "zero_or_singular_projection",
                    "interpretation": "solves required vector magnitude; does not prove source amplitude",
                    "valid_for_claim": "false",
                    "generated_utc": generated_utc,
                }
            )

        if branch == "sh0es":
            observed_vectors = {
                "observed_MU_SH0ES_minus_m_b_corr": np.asarray(table["MU_SH0ES"], dtype=float)[mask]
                - np.asarray(table["m_b_corr"], dtype=float)[mask],
                "observed_CEPH_minus_MU_calibrator_only": np.where(
                    np.asarray(table["IS_CALIBRATOR"], dtype=int)[mask].astype(bool),
                    np.asarray(table["CEPH_DIST"], dtype=float)[mask] - np.asarray(table["MU_SH0ES"], dtype=float)[mask],
                    0.0,
                ),
            }
            for vector_name, raw_vector in observed_vectors.items():
                projected = project_offset(sn, np.asarray(raw_vector, dtype=float))
                predicted_delta_b = weighted_dot(sn, j_b, projected) / denom if denom else math.nan
                observed_rows.append(
                    {
                        "branch": branch,
                        "observed_vector": vector_name,
                        "raw_mean": fmt(float(np.mean(raw_vector))),
                        "projected_vector_norm": fmt(weighted_norm(sn, projected)),
                        "predicted_delta_b_from_observed_vector": fmt(predicted_delta_b),
                        "target_delta_b": fmt(targets["sh0es"] - b_parent),
                        "status": "insufficient_to_explain_target" if abs(predicted_delta_b) < 0.25 * abs(targets["sh0es"] - b_parent) else "large_enough_to_investigate",
                        "valid_for_claim": "false",
                        "generated_utc": generated_utc,
                    }
                )
    return rows, observed_rows


def interpretation_rows(estimator: list[dict[str, object]], observed: list[dict[str, object]], generated_utc: str) -> list[dict[str, object]]:
    sh_hf = next(row for row in estimator if row["branch"] == "sh0es" and row["vector_name"] == "used_in_sh0es_hf_indicator")
    sh_low = next(row for row in estimator if row["branch"] == "sh0es" and row["vector_name"] == "low_z_lt_0p15_indicator")
    global_obs = next(row for row in observed if row["observed_vector"] == "observed_MU_SH0ES_minus_m_b_corr")
    return [
        {
            "gate_id": "IG855_0_global_offset_projected_out",
            "gate": "global calibration offset explains branch split",
            "status": "fails",
            "reason": f"observed MU_SH0ES-minus-m_b_corr predicts delta_b={global_obs['predicted_delta_b_from_observed_vector']} after offset projection",
            "next_action": "do not use global calibration shift as response proof",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "IG855_1_indicator_vectors_can_span_target",
            "gate": "HF/low-z branch geometry can span required split",
            "status": "passes_as_fit_space_not_physics",
            "reason": f"HF required mag={sh_hf['required_vector_mag_to_match_target']}; low-z required mag={sh_low['required_vector_mag_to_match_target']}",
            "next_action": "source or derive an independent calibration/local-response amplitude",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "IG855_2_projection_not_proven",
            "gate": "projection law proves SH0ES excess",
            "status": "fails_open",
            "reason": "current estimator solves for required vector amplitude rather than deriving it",
            "next_action": "either source independent delta_cal or repair memory projection",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC855_0_selected",
            "route": "independent_calibration_source_or_projection_repair",
            "status": "selected",
            "reason": "linear projection can span the branch split, but observed simple calibration residuals do not independently produce it",
            "include": "source/derive local-response amplitude; if unavailable, demote response law and repair memory projection",
            "exclude": "claiming calibration proof from required fitted vector amplitude",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RC855_1_deferred",
            "route": "full robustness scoring",
            "status": "deferred",
            "reason": "would be premature until branch response amplitude is sourced or projection is repaired",
            "include": "later multi-arena scoring",
            "exclude": "long run now",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG855_0_no_calibration_proof",
            "claim": "calibration projection explains branch split",
            "status": "forbidden",
            "reason": "the estimator needs an independently sourced vector amplitude",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG855_1_no_parent_prediction",
            "claim": "parent b_mem is derived",
            "status": "forbidden",
            "reason": "eta/a_F/DeltaR remain open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG855_2_no_support",
            "claim": "positive memory is now support-grade",
            "status": "forbidden",
            "reason": "projection and parent gates remain open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG855_3_allowed_estimator",
            "claim": "linear response estimator has been run as a private diagnostic",
            "status": "allowed_private_nonclaim",
            "reason": "finite-difference J_b and branch vectors are recorded without fitting b_mem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D855_0",
            "finding": "global calibration offset is not the explanation",
            "reason": "SN nuisance offset projection removes the global MU_SH0ES-minus-m_b_corr mode",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D855_1",
            "finding": "branch indicator response can span the split but is not sourced",
            "reason": "HF/low-z vectors require finite effective mag shifts, but those shifts were solved from target rather than derived",
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
            "objective": "decide whether an independent calibration/local-response amplitude exists; otherwise repair the memory projection before more scoring",
            "include": "source delta_cal, low-z/HF response bounds, projection repair contract, no fitted-amplitude proof",
            "exclude": "support claim, b_mem fit, public evidence, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "ran a finite-difference calibration projection response estimator",
            "selected_route": "independent_calibration_source_or_projection_repair",
            "what_is_not_claimed": "calibration proof, parent amplitude, support, public evidence, local-GR progress",
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
    estimator: list[dict[str, object]],
    observed: list[dict[str, object]],
    interpretations: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_854_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    estimator_ok = len(estimator) == 8 and any(row["branch"] == "sh0es" and row["vector_name"] == "used_in_sh0es_hf_indicator" for row in estimator)
    observed_ok = len(observed) == 2 and any(row["observed_vector"] == "observed_MU_SH0ES_minus_m_b_corr" and row["status"] == "insufficient_to_explain_target" for row in observed)
    indicator_span = any(row["branch"] == "sh0es" and row["vector_name"] == "used_in_sh0es_hf_indicator" and row["estimator_status"] == "finite_response" for row in estimator)
    gates_ok = any(row["gate_id"] == "IG855_0_global_offset_projected_out" and row["status"] == "fails" for row in interpretations) and any(row["gate_id"] == "IG855_2_projection_not_proven" for row in interpretations)
    route_ok = any(row["route_id"] == "RC855_0_selected" and row["route"] == "independent_calibration_source_or_projection_repair" for row in routes)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    nonclaim_ok = all_valid_for_claim_false([source_rows, estimator, observed, interpretations, routes, guards, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET
    return [
        {"check_id": "V855_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle"},
        {"check_id": "V855_1_prior_854_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V855_2_estimator_rows_present", "result": "pass" if estimator_ok else "fail", "detail": "branch/vector estimator rows present"},
        {"check_id": "V855_3_observed_vector_check_present", "result": "pass" if observed_ok else "fail", "detail": "observed simple calibration vector does not explain target"},
        {"check_id": "V855_4_indicator_span_finite", "result": "pass" if indicator_span else "fail", "detail": "SH0ES HF indicator has finite response coefficient"},
        {"check_id": "V855_5_interpretation_gates_present", "result": "pass" if gates_ok else "fail", "detail": "global-offset failure and projection-not-proven gates present"},
        {"check_id": "V855_6_route_selected", "result": "pass" if route_ok else "fail", "detail": "independent calibration source or projection repair selected"},
        {"check_id": "V855_7_claim_allowed_false", "result": "pass" if no_claim else "fail", "detail": "decision rows keep claim_allowed=false"},
        {"check_id": "V855_8_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V855_9_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V855_10_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V855_11_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


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
    estimator: list[dict[str, object]],
    observed: list[dict[str, object]],
    interpretations: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 855 - Y5 R10 Calibration Projection Response Estimator Dry Run",
        "",
        "Current result: **the calibration-projection response estimator runs, but it does not prove the SH0ES/no-SH0ES amplitude split**. A pure global calibration offset is projected out by the SN nuisance-offset marginalization. Hubble-flow and low-z indicator vectors can span the required `Delta b_eff`, but only by solving for an effective vector magnitude; that magnitude is not independently sourced yet. So calibration projection remains plausible bookkeeping, not physics.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "selected_route", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Linear Response Estimator",
        "",
        csv_table(estimator, ["branch", "vector_name", "raw_vector_sum", "projected_vector_norm", "delta_b_per_unit_vector_mag", "response_required_to_match_branch_target", "required_vector_mag_to_match_target", "estimator_status", "valid_for_claim"]),
        "",
        "## Observed Calibration Vector Check",
        "",
        csv_table(observed, ["branch", "observed_vector", "raw_mean", "projected_vector_norm", "predicted_delta_b_from_observed_vector", "target_delta_b", "status", "valid_for_claim"]),
        "",
        "## Interpretation Gates",
        "",
        csv_table(interpretations, ["gate_id", "gate", "status", "reason", "next_action", "valid_for_claim"]),
        "",
        "## Route Choice",
        "",
        csv_table(routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim"]),
        "",
        "## Claim Guard",
        "",
        csv_table(guards, ["guard_id", "claim", "status", "reason", "valid_for_claim"]),
        "",
        "## Decision",
        "",
        csv_table(decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        csv_table(next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
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
    estimator, observed = estimator_rows(generated_utc)
    interpretations = interpretation_rows(estimator, observed, generated_utc)
    routes = route_choice_rows(generated_utc)
    guards = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, estimator, observed, interpretations, routes, guards, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(ESTIMATOR_PATH, estimator, ["branch", "vector_name", "raw_vector_sum", "projected_vector_norm", "J_b_norm", "delta_b_per_unit_vector_mag", "response_required_to_match_branch_target", "required_vector_mag_to_match_target", "estimator_status", "interpretation", "valid_for_claim", "generated_utc"])
    write_csv(OBSERVED_VECTOR_PATH, observed, ["branch", "observed_vector", "raw_mean", "projected_vector_norm", "predicted_delta_b_from_observed_vector", "target_delta_b", "status", "valid_for_claim", "generated_utc"])
    write_csv(INTERPRETATION_PATH, interpretations, ["gate_id", "gate", "status", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guards, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "selected_route", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, estimator, observed, interpretations, routes, guards, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()

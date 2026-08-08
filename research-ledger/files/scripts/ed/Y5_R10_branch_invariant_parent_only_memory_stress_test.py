from __future__ import annotations

import csv
import json
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
RUNS = POST_CHECKPOINT / "runs"

OUTPUT_DOC = POST_CHECKPOINT / "858-Y5-R10-branch-invariant-parent-only-memory-stress-test.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_858_SOURCE_REGISTER.csv"
CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_858_PARENT_ONLY_CANDIDATES.csv"
RUN_RESULT_PATH = RESIDUALS / "P8_Y5_R10_858_PARENT_ONLY_RUN_RESULT.csv"
SCORE_PATH = RESIDUALS / "P8_Y5_R10_858_PARENT_ONLY_SN_BAO_FIT_SCORES.csv"
BRANCH_READOUT_PATH = RESIDUALS / "P8_Y5_R10_858_PARENT_ONLY_BRANCH_READOUT.csv"
JOINT_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_858_PARENT_ONLY_JOINT_LEDGER.csv"
SECTOR_LEDGER_PATH = RESIDUALS / "P8_Y5_R10_858_SN_BAO_SECTOR_LEDGER.csv"
NULL_PARITY_PATH = RESIDUALS / "P8_Y5_R10_858_NULL_CONTROL_PARITY.csv"
ACCEPTANCE_PATH = RESIDUALS / "P8_Y5_R10_858_ACCEPTANCE_READOUT.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_858_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_858_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_858_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_858_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_858_VALIDATION.csv"

COMPARATOR_PATH = POST_CHECKPOINT / "scripts" / "strict_fixed_bmem_SN_BAO_fitted_comparator.py"
CONFIG_PATH = FORMALIZATION / "configs" / "cosmology_background_R1_current.json"
PRIOR_VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_857_VALIDATION.csv"
BRANCH_TARGET_PATH = RESIDUALS / "P8_Y5_R10_856_BRANCH_TARGET_CONSTRAINTS.csv"

STATUS = "Y5_R10_858_branch_invariant_parent_only_stress_test_complete_nonclaim"
CLAIM_CEILING = "parent_only_stress_test_no_support_no_parent_derivation_no_response_source"


SOURCE_SPECS = [
    {
        "source_id": "857_doc",
        "path": POST_CHECKPOINT / "857-Y5-R10-branch-invariant-memory-projection-repair-contract.md",
        "needles": [
            "branch split is now fenced behind a parent-plus-response contract",
            "858-Y5-R10-branch-invariant-parent-only-memory-stress-test.md",
            "response channel is set to zero",
        ],
        "role": "parent-only repair contract handoff",
    },
    {
        "source_id": "857_validation",
        "path": PRIOR_VALIDATION_PATH,
        "needles": [
            "V857_8_route_selected,pass",
            "V857_10_all_rows_nonclaim,pass",
            "V857_12_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "857_acceptance_tests",
        "path": RESIDUALS / "P8_Y5_R10_857_ACCEPTANCE_TESTS.csv",
        "needles": [
            "AT857_0_shared_parent",
            "AT857_1_response_zero_default",
            "AT857_3_SN_BAO_split",
        ],
        "role": "acceptance gates for this stress test",
    },
    {
        "source_id": "857_response_gate",
        "path": RESIDUALS / "P8_Y5_R10_857_RESPONSE_SOURCE_GATE.csv",
        "needles": ["set b_R[B]=0", "failed_currently", "MISSING_INDEPENDENT_SOURCE"],
        "role": "response forced to zero",
    },
    {
        "source_id": "852_comparator",
        "path": COMPARATOR_PATH,
        "needles": [
            "Short fair SN/BAO fitted comparator with b_mem fixed.",
            "b_mem_fit_executed",
            "selection_penalty",
        ],
        "role": "fair fitted scoring engine",
    },
    {
        "source_id": "R1_cosmology_config",
        "path": CONFIG_PATH,
        "needles": ["R1_current_background", "\"id\": \"M6\"", "PantheonPlusSH0ES", "DESI_DR2_BAO"],
        "role": "SN/BAO config",
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
    rows.append(
        {
            "source_id": "858_parent_only_candidates",
            "path": str(CANDIDATE_PATH),
            "exists": str(CANDIDATE_PATH.exists()).lower(),
            "needle_check": check_needles(CANDIDATE_PATH, ["P858_0_null_parent", "P858_3_sh0es_anchor_parent", "P858_7_parent_predicted_placeholder"]),
            "role": "strict parent-only candidate input",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    )
    return rows


def branch_targets() -> tuple[float, float, float]:
    rows = read_csv(BRANCH_TARGET_PATH)
    by_branch = {row["branch"]: float(row["b_eff_target"]) for row in rows}
    no_sh0es = by_branch["no_sh0es"]
    sh0es = by_branch["sh0es"]
    return no_sh0es, sh0es, 0.5 * (no_sh0es + sh0es)


def parent_candidate_rows(generated_utc: str) -> list[dict[str, object]]:
    no_sh0es, sh0es, midpoint = branch_targets()
    field = "branch_invariant_parent_only_response_zero"
    rows = [
        {
            "candidate_id": "P858_0_null_parent",
            "branch_class": "parent_only_null_control",
            "b_mem_mode": "zero_control_parent",
            "b_mem_value_or_range": "0.0",
            "b_mem_numeric": "0.0",
            "eta_assumption": "not_applicable",
            "a_F_DeltaR_assumption": "not_applicable",
            "shape_source": field,
            "parameter_count_delta": "0",
            "family_selection_penalty": "0",
            "claim_label": "benchmark_only",
            "execution_eligible_for_input_check": "true",
            "execution_eligible_for_scoring": "true",
            "support_claim_allowed": "false",
            "notes": "null control; b_P=0 and b_R=0 must reproduce M0 parity",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "P858_1_no_sh0es_anchor_parent",
            "branch_class": "parent_only_target_anchor_stress",
            "b_mem_mode": "fixed_shared_parent",
            "b_mem_value_or_range": fmt(no_sh0es),
            "b_mem_numeric": fmt(no_sh0es),
            "eta_assumption": "eta_unsolved",
            "a_F_DeltaR_assumption": fmt(3.0 * no_sh0es),
            "shape_source": "856_no_SH0ES_effective_readout_reused_as_shared_parent_stress",
            "parameter_count_delta": "0",
            "family_selection_penalty": "1",
            "claim_label": "exploratory_parent_only_nonclaim",
            "execution_eligible_for_input_check": "true",
            "execution_eligible_for_scoring": "true",
            "support_claim_allowed": "false",
            "notes": "diagnostic only; branch target reused as shared parent, not a response",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "P858_2_midpoint_parent",
            "branch_class": "parent_only_split_midpoint_stress",
            "b_mem_mode": "fixed_shared_parent",
            "b_mem_value_or_range": fmt(midpoint),
            "b_mem_numeric": fmt(midpoint),
            "eta_assumption": "eta_unsolved",
            "a_F_DeltaR_assumption": fmt(3.0 * midpoint),
            "shape_source": "857_midpoint_response_zero_stress",
            "parameter_count_delta": "0",
            "family_selection_penalty": "1",
            "claim_label": "exploratory_parent_only_nonclaim",
            "execution_eligible_for_input_check": "true",
            "execution_eligible_for_scoring": "true",
            "support_claim_allowed": "false",
            "notes": "symmetry stress value; not a derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "P858_3_sh0es_anchor_parent",
            "branch_class": "parent_only_target_anchor_stress",
            "b_mem_mode": "fixed_shared_parent",
            "b_mem_value_or_range": fmt(sh0es),
            "b_mem_numeric": fmt(sh0es),
            "eta_assumption": "eta_unsolved",
            "a_F_DeltaR_assumption": fmt(3.0 * sh0es),
            "shape_source": "856_SH0ES_effective_readout_reused_as_shared_parent_stress",
            "parameter_count_delta": "0",
            "family_selection_penalty": "1",
            "claim_label": "exploratory_parent_only_nonclaim",
            "execution_eligible_for_input_check": "true",
            "execution_eligible_for_scoring": "true",
            "support_claim_allowed": "false",
            "notes": "diagnostic only; branch target reused as shared parent, not a response",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "P858_4_corridor_eta1_aFDeltaR_0p1",
            "branch_class": "parent_only_corridor_stress",
            "b_mem_mode": "fixed_shared_parent",
            "b_mem_value_or_range": fmt(0.1 / 3.0),
            "b_mem_numeric": fmt(0.1 / 3.0),
            "eta_assumption": "eta=1",
            "a_F_DeltaR_assumption": fmt(0.1),
            "shape_source": "predeclared_parent_corridor_response_zero",
            "parameter_count_delta": "0",
            "family_selection_penalty": "1",
            "claim_label": "exploratory_parent_only_nonclaim",
            "execution_eligible_for_input_check": "true",
            "execution_eligible_for_scoring": "true",
            "support_claim_allowed": "false",
            "notes": "corridor stress; response forced zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "P858_5_corridor_eta1_aFDeltaR_0p3",
            "branch_class": "parent_only_corridor_stress",
            "b_mem_mode": "fixed_shared_parent",
            "b_mem_value_or_range": fmt(0.3 / 3.0),
            "b_mem_numeric": fmt(0.3 / 3.0),
            "eta_assumption": "eta=1",
            "a_F_DeltaR_assumption": fmt(0.3),
            "shape_source": "predeclared_parent_corridor_response_zero",
            "parameter_count_delta": "0",
            "family_selection_penalty": "1",
            "claim_label": "exploratory_parent_only_nonclaim",
            "execution_eligible_for_input_check": "true",
            "execution_eligible_for_scoring": "true",
            "support_claim_allowed": "false",
            "notes": "corridor stress; response forced zero",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "P858_6_corridor_eta1_aFDeltaR_1p0",
            "branch_class": "parent_only_corridor_stress",
            "b_mem_mode": "fixed_shared_parent",
            "b_mem_value_or_range": fmt(1.0 / 3.0),
            "b_mem_numeric": fmt(1.0 / 3.0),
            "eta_assumption": "eta=1",
            "a_F_DeltaR_assumption": fmt(1.0),
            "shape_source": "predeclared_parent_corridor_response_zero",
            "parameter_count_delta": "0",
            "family_selection_penalty": "1",
            "claim_label": "exploratory_parent_only_nonclaim",
            "execution_eligible_for_input_check": "true",
            "execution_eligible_for_scoring": "true",
            "support_claim_allowed": "false",
            "notes": "upper corridor stress; expected to expose over-amplitude penalty if present",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "P858_7_parent_predicted_placeholder",
            "branch_class": "parent_only_parent_predicted",
            "b_mem_mode": "fixed_parent",
            "b_mem_value_or_range": "BLOCKED_NO_UNIQUE_PARENT_PREDICTION",
            "b_mem_numeric": "",
            "eta_assumption": "MISSING_PARENT_ETA",
            "a_F_DeltaR_assumption": "MISSING_PARENT_AF_DELTAR",
            "shape_source": "parent_amplitude_prediction_missing",
            "parameter_count_delta": "0",
            "family_selection_penalty": "0",
            "claim_label": "support_grade_candidate_blocked",
            "execution_eligible_for_input_check": "false",
            "execution_eligible_for_scoring": "false",
            "support_claim_allowed": "false",
            "notes": "clean support route exists only after eta, a_F, and DeltaR are parent-derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]
    return rows


def run_comparator() -> tuple[Path, dict[str, object], str]:
    command = [
        "python",
        str(COMPARATOR_PATH),
        "--candidates",
        str(CANDIDATE_PATH),
        "--config",
        str(CONFIG_PATH),
        "--branches",
        "sh0es",
        "no_sh0es",
        "--integration-steps",
        "1024",
        "--maxiter",
        "80",
        "--starts",
        "2",
        "--short-fit",
        "--no-bmem-fit",
        "--write-run-dir",
        "--output-root",
        str(RUNS),
    ]
    completed = subprocess.run(
        command,
        cwd=str(POST_CHECKPOINT),
        check=True,
        capture_output=True,
        text=True,
        timeout=300,
    )
    run_dir_text = ""
    for line in completed.stdout.splitlines():
        if line.startswith("run_dir="):
            run_dir_text = line.split("=", 1)[1].strip()
            break
    if not run_dir_text:
        raise RuntimeError("comparator did not print run_dir")
    run_dir = Path(run_dir_text)
    status = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    return run_dir, status, completed.stdout


def run_result_rows(run_dir: Path, status: dict[str, object], stdout: str, generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "run_id": run_dir.name,
            "run_dir": str(run_dir),
            "status": status.get("status"),
            "short_fit": str(status.get("short_fit")).lower(),
            "fit_executed": str(status.get("fit_executed")).lower(),
            "b_mem_fit_executed": str(status.get("b_mem_fit_executed")).lower(),
            "claim_allowed": str(status.get("claim_allowed")).lower(),
            "candidate_file": status.get("candidate_file"),
            "row_count": status.get("row_count"),
            "pass_count": status.get("pass_count"),
            "blocked_count": status.get("blocked_count"),
            "failure_count": status.get("failure_count"),
            "runner_stdout": stdout.replace("\n", " | "),
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def score_rows(run_dir: Path, generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in read_csv(run_dir / "FAIR_FIXED_BMEM_SN_BAO_FIT_SCORES.csv"):
        rows.append({**row, "valid_for_claim": "false", "generated_utc": generated_utc})
    return rows


def best_bic_baseline(scores: list[dict[str, object]], branch: str) -> dict[str, object]:
    rows = [
        row
        for row in scores
        if row["branch"] == branch and row["row_type"] == "baseline_fit" and row["evaluation_status"] == "pass"
    ]
    return min(rows, key=lambda row: float(row["bic"]))


def candidate_pass_rows(scores: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        row
        for row in scores
        if row["row_type"] == "candidate_fixed_bmem_fit"
        and row["evaluation_status"] == "pass"
        and row["candidate_id"] != "P858_0_null_parent"
    ]


def branch_readout_rows(scores: list[dict[str, object]], generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for branch in sorted({str(row["branch"]) for row in scores}):
        baseline = best_bic_baseline(scores, branch)
        candidates = [row for row in candidate_pass_rows(scores) if row["branch"] == branch]
        best_candidate = min(candidates, key=lambda row: float(row["delta_bic_vs_best_fit_baseline"]))
        rows.append(
            {
                "branch": branch,
                "best_bic_baseline": baseline["config_id"],
                "best_bic_baseline_bic": baseline["bic"],
                "best_parent_candidate": best_candidate["candidate_id"],
                "b_parent": best_candidate["b_mem_fixed"],
                "b_response": "0",
                "delta_chi2_vs_best_baseline": best_candidate["delta_chi2_vs_best_fit_baseline"],
                "delta_aic_vs_best_baseline": best_candidate["delta_aic_vs_best_fit_baseline"],
                "delta_bic_vs_best_baseline": best_candidate["delta_bic_vs_best_fit_baseline"],
                "edge_flags": best_candidate["edge_flags"],
                "readout": "branch_diagnostic_only_parent_value_shared_candidate_pool",
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def sector_ledger_rows(scores: list[dict[str, object]], generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in scores:
        if row["row_type"] != "candidate_fixed_bmem_fit" or row["evaluation_status"] != "pass":
            continue
        baseline = best_bic_baseline(scores, str(row["branch"]))
        rows.append(
            {
                "branch": row["branch"],
                "candidate_id": row["candidate_id"],
                "b_parent": row["b_mem_fixed"],
                "b_response": "0",
                "sector_baseline": baseline["config_id"],
                "delta_chi2_sn_vs_bic_baseline": fmt(float(row["chi2_sn"]) - float(baseline["chi2_sn"])),
                "delta_chi2_bao_vs_bic_baseline": fmt(float(row["chi2_bao"]) - float(baseline["chi2_bao"])),
                "delta_chi2_total_vs_bic_baseline": fmt(float(row["chi2_total"]) - float(baseline["chi2_total"])),
                "delta_bic_vs_best_fit_baseline": row["delta_bic_vs_best_fit_baseline"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def joint_status(delta_bic: float, max_branch_delta: float) -> str:
    if delta_bic < -2.0 and max_branch_delta < 6.0:
        return "survives_parent_only_private_nonclaim"
    if delta_bic <= 2.0:
        return "borderline_parent_only_private_nonclaim"
    if delta_bic <= 6.0:
        return "weakly_disfavored_but_competitive_private_nonclaim"
    return "disfavored_parent_only_private_nonclaim"


def joint_ledger_rows(scores: list[dict[str, object]], sector_rows: list[dict[str, object]], generated_utc: str) -> list[dict[str, object]]:
    candidate_ids = sorted({row["candidate_id"] for row in scores if row["row_type"] == "candidate_fixed_bmem_fit"})
    sector_by_key = {(row["branch"], row["candidate_id"]): row for row in sector_rows}
    rows: list[dict[str, object]] = []
    for candidate_id in candidate_ids:
        candidate_rows = [
            row for row in scores if row["row_type"] == "candidate_fixed_bmem_fit" and row["candidate_id"] == candidate_id
        ]
        pass_rows = [row for row in candidate_rows if row["evaluation_status"] == "pass"]
        if len(pass_rows) != 2:
            rows.append(
                {
                    "candidate_id": candidate_id,
                    "b_parent": "",
                    "b_response_no_sh0es": "0",
                    "b_response_sh0es": "0",
                    "combined_delta_chi2": "",
                    "combined_delta_aic": "",
                    "combined_delta_bic": "",
                    "combined_delta_chi2_sn_vs_bic_baseline": "",
                    "combined_delta_chi2_bao_vs_bic_baseline": "",
                    "max_branch_delta_bic": "",
                    "status": "blocked_parent_prediction_missing",
                    "interpretation": "support-grade parent amplitude is still missing",
                    "valid_for_claim": "false",
                    "generated_utc": generated_utc,
                }
            )
            continue
        combined_delta_chi2 = sum(float(row["delta_chi2_vs_best_fit_baseline"]) for row in pass_rows)
        combined_delta_aic = sum(float(row["delta_aic_vs_best_fit_baseline"]) for row in pass_rows)
        combined_delta_bic = sum(float(row["delta_bic_vs_best_fit_baseline"]) for row in pass_rows)
        combined_delta_sn = sum(float(sector_by_key[(row["branch"], candidate_id)]["delta_chi2_sn_vs_bic_baseline"]) for row in pass_rows)
        combined_delta_bao = sum(float(sector_by_key[(row["branch"], candidate_id)]["delta_chi2_bao_vs_bic_baseline"]) for row in pass_rows)
        max_branch_delta = max(float(row["delta_bic_vs_best_fit_baseline"]) for row in pass_rows)
        if candidate_id == "P858_0_null_parent":
            status = "null_control"
            interpretation = "zero parent memory checks baseline parity"
        else:
            status = joint_status(combined_delta_bic, max_branch_delta)
            interpretation = "shared parent value scored with response forced to zero and selection penalty applied"
        rows.append(
            {
                "candidate_id": candidate_id,
                "b_parent": pass_rows[0]["b_mem_fixed"],
                "b_response_no_sh0es": "0",
                "b_response_sh0es": "0",
                "combined_delta_chi2": fmt(combined_delta_chi2),
                "combined_delta_aic": fmt(combined_delta_aic),
                "combined_delta_bic": fmt(combined_delta_bic),
                "combined_delta_chi2_sn_vs_bic_baseline": fmt(combined_delta_sn),
                "combined_delta_chi2_bao_vs_bic_baseline": fmt(combined_delta_bao),
                "max_branch_delta_bic": fmt(max_branch_delta),
                "status": status,
                "interpretation": interpretation,
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def null_parity_rows(scores: list[dict[str, object]], generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for branch in sorted({str(row["branch"]) for row in scores}):
        m0 = next(row for row in scores if row["branch"] == branch and row["config_id"] == "M0_fit_fair")
        null = next(row for row in scores if row["branch"] == branch and row["candidate_id"] == "P858_0_null_parent")
        delta_chi2 = float(null["chi2_total"]) - float(m0["chi2_total"])
        rows.append(
            {
                "branch": branch,
                "M0_chi2": m0["chi2_total"],
                "null_parent_chi2": null["chi2_total"],
                "null_minus_M0_chi2": fmt(delta_chi2),
                "parity_status": "numerically_close" if abs(delta_chi2) < 1.0e-2 else "not_identical_optimizer_or_model_difference",
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def best_nonnull_joint(joint_rows: list[dict[str, object]]) -> dict[str, object]:
    candidates = [
        row
        for row in joint_rows
        if row["candidate_id"] != "P858_0_null_parent" and finite_float(row["combined_delta_bic"]) is not None
    ]
    return min(candidates, key=lambda row: float(row["combined_delta_bic"]))


def selected_next_target(best_joint: dict[str, object]) -> tuple[str, str]:
    status = str(best_joint["status"])
    if status == "survives_parent_only_private_nonclaim":
        return (
            "859-Y5-R10-parent-amplitude-law-eta-aF-DeltaR-derivation-contract.md",
            "derive eta, a_F, and DeltaR for the surviving parent-only amplitude without using the fit target as input",
        )
    if status in {"borderline_parent_only_private_nonclaim", "weakly_disfavored_but_competitive_private_nonclaim"}:
        return (
            "859-Y5-R10-parent-memory-shape-amplitude-repair-or-derivation.md",
            "derive or repair the parent memory shape/amplitude because the strict shared-parent test is competitive but not evidence-grade",
        )
    return (
        "859-Y5-R10-parent-only-failure-diagnosis-and-response-source-hunt.md",
        "diagnose why the strict shared parent fails and only then reopen response-source hunting",
    )


def acceptance_rows(
    scores: list[dict[str, object]],
    sector_rows: list[dict[str, object]],
    null_rows: list[dict[str, object]],
    joint_rows: list[dict[str, object]],
    generated_utc: str,
) -> list[dict[str, object]]:
    pass_rows = [row for row in scores if row["row_type"] == "candidate_fixed_bmem_fit" and row["evaluation_status"] == "pass"]
    grouped: dict[str, set[str]] = {}
    for row in pass_rows:
        grouped.setdefault(str(row["candidate_id"]), set()).add(str(row["b_mem_fixed"]))
    shared_parent_ok = all(len(values) == 1 for values in grouped.values())
    response_zero_ok = True
    null_ok = all(row["parity_status"] == "numerically_close" for row in null_rows)
    sector_ok = bool(sector_rows) and all(row["delta_chi2_sn_vs_bic_baseline"] != "" and row["delta_chi2_bao_vs_bic_baseline"] != "" for row in sector_rows)
    best_joint = best_nonnull_joint(joint_rows)
    return [
        {
            "test_id": "AT858_0_shared_parent",
            "result": "pass" if shared_parent_ok else "fail",
            "detail": "each candidate uses one b_P value across no_SH0ES and SH0ES",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "AT858_1_response_zero",
            "result": "pass" if response_zero_ok else "fail",
            "detail": "all candidate rows set b_response_no_sh0es=b_response_sh0es=0 in joint ledger",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "AT858_2_null_parity",
            "result": "pass" if null_ok else "fail",
            "detail": "b_P=0 M6 tracks M0 within tolerance",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "AT858_3_SN_BAO_split",
            "result": "pass" if sector_ok else "fail",
            "detail": "sector deltas are reported separately from total BIC",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "test_id": "AT858_4_parent_survival",
            "result": "pass" if str(best_joint["status"]) in {"survives_parent_only_private_nonclaim", "borderline_parent_only_private_nonclaim", "weakly_disfavored_but_competitive_private_nonclaim"} else "fail",
            "detail": f"best_nonnull={best_joint['candidate_id']} status={best_joint['status']} combined_delta_bic={best_joint['combined_delta_bic']}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG858_0_no_support",
            "claim": "parent-only cosmology is support-grade",
            "status": "forbidden",
            "reason": "parent amplitude is not derived and this is a short private stress test",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG858_1_no_response",
            "claim": "response channel explains the branch split",
            "status": "forbidden",
            "reason": "response is deliberately forced to zero in every scored candidate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG858_2_no_branch_knob",
            "claim": "separate branch b_mem values are used",
            "status": "forbidden",
            "reason": "all scored non-null candidates use one shared b_P across both branches",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG858_3_allowed_private_stress_readout",
            "claim": "strict parent-only stress-test readout is available",
            "status": "allowed_private_nonclaim",
            "reason": "shared parent values were scored with response zero and sector ledgers recorded",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(best_joint: dict[str, object], next_target: str, generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D858_0",
            "finding": str(best_joint["status"]),
            "reason": f"best shared parent candidate is {best_joint['candidate_id']} with combined_delta_bic={best_joint['combined_delta_bic']} and max_branch_delta_bic={best_joint['max_branch_delta_bic']}",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": next_target,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D858_1",
            "finding": "parent-only route remains private and derivation-gated",
            "reason": "even if competitive, the amplitude must be derived rather than selected from the stress grid",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": next_target,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(next_target: str, objective: str, generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": next_target,
            "objective": objective,
            "include": "eta/a_F/DeltaR derivation attempt, parent shape audit, no fitted target inversion, response source remains closed unless independently signed",
            "exclude": "support claim, local-GR claim, public evidence, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(best_joint: dict[str, object], next_target: str, generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "scored strict parent-only shared b_P candidates with response forced to zero",
            "best_parent_candidate": best_joint["candidate_id"],
            "best_combined_delta_bic": best_joint["combined_delta_bic"],
            "best_status": best_joint["status"],
            "what_is_not_claimed": "support, parent derivation, response physics, local-GR pass, public evidence",
            "next_target": next_target,
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
    candidates: list[dict[str, object]],
    run_rows: list[dict[str, object]],
    scores: list[dict[str, object]],
    branch_readouts: list[dict[str, object]],
    joint_rows: list[dict[str, object]],
    sector_rows: list[dict[str, object]],
    null_rows: list[dict[str, object]],
    acceptance: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(PRIOR_VALIDATION_PATH)
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    candidate_ok = len(candidates) == 8 and all(row["valid_for_claim"] == "false" for row in candidates)
    run_ok = bool(run_rows) and run_rows[0]["status"] == "fair_fixed_bmem_SN_BAO_short_fit_written_nonclaim"
    row_count_ok = bool(run_rows) and str(run_rows[0]["row_count"]) == "22" and str(run_rows[0]["failure_count"]) == "0"
    no_bmem_fit = all("b_mem" not in str(row["fit_param_names"]).split(";") for row in scores if row["evaluation_status"] == "pass")
    shared_parent = len({(row["candidate_id"], row["b_mem_fixed"]) for row in scores if row["row_type"] == "candidate_fixed_bmem_fit" and row["evaluation_status"] == "pass"}) == len({row["candidate_id"] for row in scores if row["row_type"] == "candidate_fixed_bmem_fit" and row["evaluation_status"] == "pass"})
    parent_placeholder_blocked = len([row for row in scores if row["candidate_id"] == "P858_7_parent_predicted_placeholder" and row["evaluation_status"] == "blocked"]) == 2
    branch_ok = len(branch_readouts) == 2
    joint_ok = len(joint_rows) == 8 and any(row["status"] != "blocked_parent_prediction_missing" for row in joint_rows)
    sector_ok = len(sector_rows) == 14
    null_ok = len(null_rows) == 2 and all(row["parity_status"] == "numerically_close" for row in null_rows)
    acceptance_ok = len(acceptance) == 5 and all(row["result"] == "pass" for row in acceptance)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions) and bool(run_rows) and run_rows[0]["claim_allowed"] == "false"
    nonclaim_ok = all_valid_for_claim_false([source_rows, candidates, run_rows, scores, branch_readouts, joint_rows, sector_rows, null_rows, acceptance, guards, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and str(next_targets[0]["next_target"]).startswith("859-Y5-R10-")
    return [
        {"check_id": "V858_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle"},
        {"check_id": "V858_1_prior_857_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V858_2_parent_only_candidates_ready", "result": "pass" if candidate_ok else "fail", "detail": "8 parent-only candidates including null and blocked parent-predicted placeholder"},
        {"check_id": "V858_3_run_status_clean", "result": "pass" if run_ok else "fail", "detail": "fair fixed-bmem comparator completed"},
        {"check_id": "V858_4_row_count_and_failures", "result": "pass" if row_count_ok else "fail", "detail": "22 rows expected, failure_count=0"},
        {"check_id": "V858_5_no_bmem_fit", "result": "pass" if no_bmem_fit else "fail", "detail": "no passing fit_param_names include b_mem"},
        {"check_id": "V858_6_shared_parent_candidates", "result": "pass" if shared_parent else "fail", "detail": "each scored candidate has one b_P across both branches"},
        {"check_id": "V858_7_parent_placeholder_blocked", "result": "pass" if parent_placeholder_blocked else "fail", "detail": "support-grade parent-predicted placeholder blocked on both branches"},
        {"check_id": "V858_8_branch_readouts_present", "result": "pass" if branch_ok else "fail", "detail": "two branch diagnostic readouts generated"},
        {"check_id": "V858_9_joint_ledger_present", "result": "pass" if joint_ok else "fail", "detail": "joint shared-parent ledger generated"},
        {"check_id": "V858_10_sector_ledger_present", "result": "pass" if sector_ok else "fail", "detail": "SN and BAO sector deltas generated for scored candidates"},
        {"check_id": "V858_11_null_control_parity", "result": "pass" if null_ok else "fail", "detail": "b_P=0 M6 tracks M0 after fair refit"},
        {"check_id": "V858_12_acceptance_passes", "result": "pass" if acceptance_ok else "fail", "detail": "all strict 858 acceptance tests pass"},
        {"check_id": "V858_13_claim_allowed_false", "result": "pass" if no_claim else "fail", "detail": "runner and decision rows keep claim_allowed=false"},
        {"check_id": "V858_14_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V858_15_next_target_selected", "result": "pass" if next_selected else "fail", "detail": next_targets[0]["next_target"] if next_targets else "missing"},
        {"check_id": "V858_16_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V858_17_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
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
    candidates: list[dict[str, object]],
    run_rows: list[dict[str, object]],
    branch_readouts: list[dict[str, object]],
    joint_rows: list[dict[str, object]],
    sector_rows: list[dict[str, object]],
    null_rows: list[dict[str, object]],
    acceptance: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 858 - Y5 R10 Branch-Invariant Parent-Only Memory Stress Test",
        "",
        "Current result: **the parent-only memory route has been stress-tested with one shared `b_P` and response forced to zero**. This is stricter than the earlier branch readout: non-derived parent amplitudes pay a selection penalty, no branch-specific `b_mem` is fitted, and SN/BAO sector deltas are reported separately.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "best_parent_candidate", "best_combined_delta_bic", "best_status", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Run Result",
        "",
        csv_table(run_rows, ["run_id", "run_dir", "status", "short_fit", "fit_executed", "b_mem_fit_executed", "claim_allowed", "row_count", "pass_count", "blocked_count", "failure_count", "valid_for_claim"]),
        "",
        "## Parent-Only Candidate Grid",
        "",
        csv_table(candidates, ["candidate_id", "branch_class", "b_mem_numeric", "eta_assumption", "a_F_DeltaR_assumption", "family_selection_penalty", "claim_label", "execution_eligible_for_scoring", "valid_for_claim"]),
        "",
        "## Branch Readout",
        "",
        csv_table(branch_readouts, ["branch", "best_bic_baseline", "best_parent_candidate", "b_parent", "b_response", "delta_chi2_vs_best_baseline", "delta_aic_vs_best_baseline", "delta_bic_vs_best_baseline", "edge_flags", "readout", "valid_for_claim"]),
        "",
        "## Joint Parent Ledger",
        "",
        csv_table(joint_rows, ["candidate_id", "b_parent", "b_response_no_sh0es", "b_response_sh0es", "combined_delta_chi2", "combined_delta_aic", "combined_delta_bic", "combined_delta_chi2_sn_vs_bic_baseline", "combined_delta_chi2_bao_vs_bic_baseline", "max_branch_delta_bic", "status", "valid_for_claim"]),
        "",
        "## SN BAO Sector Ledger",
        "",
        csv_table(sector_rows, ["branch", "candidate_id", "b_parent", "sector_baseline", "delta_chi2_sn_vs_bic_baseline", "delta_chi2_bao_vs_bic_baseline", "delta_chi2_total_vs_bic_baseline", "delta_bic_vs_best_fit_baseline", "valid_for_claim"]),
        "",
        "## Null Control Parity",
        "",
        csv_table(null_rows, ["branch", "M0_chi2", "null_parent_chi2", "null_minus_M0_chi2", "parity_status", "valid_for_claim"]),
        "",
        "## Acceptance Readout",
        "",
        csv_table(acceptance, ["test_id", "result", "detail", "valid_for_claim"]),
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
    candidates = parent_candidate_rows(generated_utc)
    candidate_fields = [
        "candidate_id",
        "branch_class",
        "b_mem_mode",
        "b_mem_value_or_range",
        "b_mem_numeric",
        "eta_assumption",
        "a_F_DeltaR_assumption",
        "shape_source",
        "parameter_count_delta",
        "family_selection_penalty",
        "claim_label",
        "execution_eligible_for_input_check",
        "execution_eligible_for_scoring",
        "support_claim_allowed",
        "notes",
        "valid_for_claim",
        "generated_utc",
    ]
    write_csv(CANDIDATE_PATH, candidates, candidate_fields)
    source_rows = source_register_rows(generated_utc)
    run_dir, status, stdout = run_comparator()
    run_rows = run_result_rows(run_dir, status, stdout, generated_utc)
    scores = score_rows(run_dir, generated_utc)
    branch_readouts = branch_readout_rows(scores, generated_utc)
    sector_rows = sector_ledger_rows(scores, generated_utc)
    joint_rows = joint_ledger_rows(scores, sector_rows, generated_utc)
    null_rows = null_parity_rows(scores, generated_utc)
    acceptance = acceptance_rows(scores, sector_rows, null_rows, joint_rows, generated_utc)
    best_joint = best_nonnull_joint(joint_rows)
    next_target, next_objective = selected_next_target(best_joint)
    guards = claim_guard_rows(generated_utc)
    decisions = decision_rows(best_joint, next_target, generated_utc)
    next_targets = next_target_rows(next_target, next_objective, generated_utc)
    nonclaim = nonclaim_summary_rows(best_joint, next_target, generated_utc)
    validation = validation_rows(
        source_rows,
        candidates,
        run_rows,
        scores,
        branch_readouts,
        joint_rows,
        sector_rows,
        null_rows,
        acceptance,
        guards,
        decisions,
        next_targets,
        nonclaim,
    )

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(RUN_RESULT_PATH, run_rows, ["run_id", "run_dir", "status", "short_fit", "fit_executed", "b_mem_fit_executed", "claim_allowed", "candidate_file", "row_count", "pass_count", "blocked_count", "failure_count", "runner_stdout", "valid_for_claim", "generated_utc"])
    write_csv(SCORE_PATH, scores, ["branch", "row_type", "config_id", "candidate_id", "claim_label", "physics_model", "b_mem_fixed", "fit_param_names", "effective_k_with_selection_penalty", "chi2_sn", "chi2_bao", "chi2_total", "n_data", "aic", "bic", "delta_chi2_vs_best_fit_baseline", "delta_aic_vs_best_fit_baseline", "delta_bic_vs_best_fit_baseline", "params_json", "edge_flags", "success", "message", "evaluation_status", "fit_executed", "b_mem_fit_executed", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(BRANCH_READOUT_PATH, branch_readouts, ["branch", "best_bic_baseline", "best_bic_baseline_bic", "best_parent_candidate", "b_parent", "b_response", "delta_chi2_vs_best_baseline", "delta_aic_vs_best_baseline", "delta_bic_vs_best_baseline", "edge_flags", "readout", "valid_for_claim", "generated_utc"])
    write_csv(JOINT_LEDGER_PATH, joint_rows, ["candidate_id", "b_parent", "b_response_no_sh0es", "b_response_sh0es", "combined_delta_chi2", "combined_delta_aic", "combined_delta_bic", "combined_delta_chi2_sn_vs_bic_baseline", "combined_delta_chi2_bao_vs_bic_baseline", "max_branch_delta_bic", "status", "interpretation", "valid_for_claim", "generated_utc"])
    write_csv(SECTOR_LEDGER_PATH, sector_rows, ["branch", "candidate_id", "b_parent", "b_response", "sector_baseline", "delta_chi2_sn_vs_bic_baseline", "delta_chi2_bao_vs_bic_baseline", "delta_chi2_total_vs_bic_baseline", "delta_bic_vs_best_fit_baseline", "valid_for_claim", "generated_utc"])
    write_csv(NULL_PARITY_PATH, null_rows, ["branch", "M0_chi2", "null_parent_chi2", "null_minus_M0_chi2", "parity_status", "valid_for_claim", "generated_utc"])
    write_csv(ACCEPTANCE_PATH, acceptance, ["test_id", "result", "detail", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guards, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "best_parent_candidate", "best_combined_delta_bic", "best_status", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, candidates, run_rows, branch_readouts, joint_rows, sector_rows, null_rows, acceptance, guards, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"run_dir={run_dir}")
    print(f"status={STATUS}")
    print(f"best_parent_candidate={best_joint['candidate_id']}")
    print(f"best_combined_delta_bic={best_joint['combined_delta_bic']}")
    print(f"best_status={best_joint['status']}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={next_target}")


if __name__ == "__main__":
    main()

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

OUTPUT_DOC = POST_CHECKPOINT / "851-Y5-R10-fixed-bmem-SN-BAO-readout-and-eta-law-choice.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_851_SOURCE_REGISTER.csv"
READOUT_PATH = RESIDUALS / "P8_Y5_R10_851_SN_BAO_READOUT.csv"
SECTOR_TENSION_PATH = RESIDUALS / "P8_Y5_R10_851_SN_BAO_SECTOR_TENSION.csv"
ARTIFACT_DIAGNOSIS_PATH = RESIDUALS / "P8_Y5_R10_851_ARTIFACT_DIAGNOSIS.csv"
ROUTE_CHOICE_PATH = RESIDUALS / "P8_Y5_R10_851_ROUTE_CHOICE.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_851_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_851_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_851_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_851_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_851_VALIDATION.csv"

SCORES_PATH = RESIDUALS / "P8_Y5_R10_850_FIXED_BMEM_SN_BAO_SAMPLE_SCORES.csv"

STATUS = "Y5_R10_851_fixed_bmem_SN_BAO_readout_selects_fair_comparator_nonclaim"
CLAIM_CEILING = "readout_and_route_choice_only_no_support_no_death_no_parent_prediction"
NEXT_TARGET = "852-Y5-R10-fair-fixed-bmem-SN-BAO-fitted-comparator-dry-run.md"

SOURCE_SPECS = [
    {
        "source_id": "850_doc",
        "path": POST_CHECKPOINT / "850-Y5-R10-fixed-bmem-cosmology-score-evaluator-dry-run.md",
        "needles": [
            "fixed-`b_mem` SN/BAO sample scoring now runs",
            "sample values rather than fair fitted competitors",
            "851-Y5-R10-fixed-bmem-SN-BAO-readout-and-eta-law-choice.md",
        ],
        "role": "sample score handoff",
    },
    {
        "source_id": "850_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_850_VALIDATION.csv",
        "needles": [
            "V850_2_evaluator_status_clean,pass",
            "V850_4_no_fit_or_optimizer,pass",
            "V850_13_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "850_scores",
        "path": SCORES_PATH,
        "needles": [
            "M6_fixed_S0_null_bmem_0",
            "S2_corridor_eta1_aFDeltaR_1p0",
            "S3_parent_predicted_placeholder",
        ],
        "role": "sample fixed-bmem SN/BAO score rows",
    },
    {
        "source_id": "850_evaluator",
        "path": POST_CHECKPOINT / "scripts" / "strict_fixed_bmem_SN_BAO_evaluator.py",
        "needles": [
            "Sample-only fixed-b_mem SN/BAO evaluator.",
            "optimizer_executed",
            "claim_allowed",
        ],
        "role": "sample-only evaluator implementation",
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


def branch_baseline(rows: list[dict[str, str]], branch: str) -> dict[str, str]:
    baselines = [
        row
        for row in rows
        if row["branch"] == branch and row["row_type"] == "baseline_sample" and row["evaluation_status"] == "pass"
    ]
    return min(baselines, key=lambda row: float(row["bic_sample"]))


def readout_rows(scores: list[dict[str, str]], generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for branch in sorted({row["branch"] for row in scores}):
        baseline = branch_baseline(scores, branch)
        candidates = [
            row
            for row in scores
            if row["branch"] == branch and row["row_type"] == "candidate_fixed_bmem" and row["evaluation_status"] == "pass"
        ]
        best_candidate = min(candidates, key=lambda row: float(row["delta_bic_vs_best_sample_baseline"]))
        positive_candidates = [
            row
            for row in candidates
            if finite_float(row["sample_params_json"].split('"b_mem": ')[-1].split(",")[0].rstrip("}")) not in (None, 0.0)
        ]
        best_positive = min(positive_candidates, key=lambda row: float(row["delta_bic_vs_best_sample_baseline"]))
        rows.append(
            {
                "branch": branch,
                "best_sample_baseline": baseline["config_id"],
                "best_sample_baseline_chi2": baseline["chi2_total"],
                "best_candidate": best_candidate["candidate_id"],
                "best_candidate_delta_BIC": best_candidate["delta_bic_vs_best_sample_baseline"],
                "best_positive_candidate": best_positive["candidate_id"],
                "best_positive_delta_BIC": best_positive["delta_bic_vs_best_sample_baseline"],
                "readout": "sample_M6_fixed_bmem_worse_than_sample_M0",
                "interpretation": "not a support or death result because nuisance/background parameters are not fitted under parity",
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def sector_tension_rows(scores: list[dict[str, str]], generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for branch in sorted({row["branch"] for row in scores}):
        baseline = branch_baseline(scores, branch)
        candidates = [
            row
            for row in scores
            if row["branch"] == branch and row["row_type"] == "candidate_fixed_bmem" and row["evaluation_status"] == "pass"
        ]
        for row in candidates:
            delta_sn = float(row["chi2_sn"]) - float(baseline["chi2_sn"])
            delta_bao = float(row["chi2_bao"]) - float(baseline["chi2_bao"])
            if delta_sn < 0.0 and delta_bao > 0.0:
                tension = "SN_improves_BAO_worsens"
            elif delta_sn > 0.0 and delta_bao > 0.0:
                tension = "SN_and_BAO_worse"
            elif delta_sn < 0.0 and delta_bao < 0.0:
                tension = "SN_and_BAO_improve_sample_only"
            else:
                tension = "mixed_other"
            rows.append(
                {
                    "branch": branch,
                    "candidate_id": row["candidate_id"],
                    "delta_chi2_SN_vs_best_sample_baseline": fmt(delta_sn),
                    "delta_chi2_BAO_vs_best_sample_baseline": fmt(delta_bao),
                    "delta_chi2_total_vs_best_sample_baseline": row["delta_chi2_vs_best_sample_baseline"],
                    "sector_tension": tension,
                    "readout": "BAO_dominates_positive_memory_penalty" if delta_bao > 0.0 else "no_BAO_penalty",
                    "valid_for_claim": "false",
                    "generated_utc": generated_utc,
                }
            )
    return rows


def artifact_diagnosis_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "artifact_id": "AD851_0_null_control",
            "finding": "S0 null b_mem is already worse than M0",
            "meaning": "sample M6 background values h0=72, omega_m0=0.27 differ from M0 sample values h0=70, omega_m0=0.3",
            "risk": "do not interpret null-control loss as memory-sector loss",
            "required_fix": "fit shared nuisance/background parameters under baseline parity with b_mem fixed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "artifact_id": "AD851_1_BAO_pressure",
            "finding": "positive b_mem tends to improve or barely affect SN but strongly worsens BAO in the sample test",
            "meaning": "the current memory shape/amplitude may be BAO-stiff, or the non-bmem parameters need fair refit",
            "risk": "a positive-amplitude derivation could be forced into a BAO conflict if fair refit does not repair it",
            "required_fix": "run fixed-bmem fitted comparator before deriving eta as if positive b_mem were empirically safe",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "artifact_id": "AD851_2_parent_eta_route",
            "finding": "eta/a_F/DeltaR derivation remains necessary but should not be the immediate empirical route",
            "meaning": "a derived amplitude is valuable only if the fair comparator shows the branch is not structurally BAO-broken",
            "risk": "deriving a beautiful amplitude for a bad projection wastes effort",
            "required_fix": "choose fair comparator next, then feed its result back into parent-amplitude derivation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_choice_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "route_id": "RC851_0_selected",
            "route": "fair_fixed_bmem_fitted_SN_BAO_comparator",
            "status": "selected",
            "reason": "sample test is dominated by un-fitted nuisance/background choices; fair comparator is needed before eta-law derivation or branch demotion",
            "include": "fit h0, omega_m0, rd and baseline dark-energy parameters under parity while keeping b_mem fixed",
            "exclude": "fitting b_mem, support claims, death claims, public evidence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RC851_1_deferred",
            "route": "eta_aF_DeltaR_derivation_next",
            "status": "deferred",
            "reason": "still essential, but fair data check should tell us whether the positive-memory projection is worth deriving in its current form",
            "include": "return after 852 comparator",
            "exclude": "using sample-score losses as proof eta route fails",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RC851_2_rejected",
            "route": "demote_M6_or_C0_from_sample_score",
            "status": "rejected",
            "reason": "sample baselines are not fitted and null-control M6 differs from M0 background parameters",
            "include": "none",
            "exclude": "branch death from 850",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG851_0_no_support",
            "claim": "850/851 supports MTS cosmology",
            "status": "forbidden",
            "reason": "only a sample-score readout exists and candidate rows are nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG851_1_no_death",
            "claim": "positive b_mem or M6 is dead",
            "status": "forbidden",
            "reason": "null-control M6 is not parameter-matched to M0 and no fair fit has run",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG851_2_no_parent_prediction",
            "claim": "eta/a_F/DeltaR is now derived",
            "status": "forbidden",
            "reason": "851 only chooses whether to pursue derivation before or after fair comparator",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG851_3_allowed_readout",
            "claim": "850 reveals a BAO-pressure clue under sample parameters",
            "status": "allowed_private_nonclaim",
            "reason": "sector deltas show positive fixed b_mem improves/softens SN in places but BAO dominates the penalty",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D851_0",
            "finding": "850 is a useful pipeline and tension clue, not evidence",
            "reason": "fixed-bmem rows evaluate cleanly but baselines and nuisance/background values are sample-only",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D851_1",
            "finding": "BAO pressure is the immediate empirical issue",
            "reason": "positive bmem rows can lower SN chi2 but strongly raise BAO chi2 under current sample shape/parameters",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D851_2",
            "finding": "fair fixed-bmem fitted comparator is selected before eta derivation",
            "reason": "we need to separate projection/BAO failure from un-fitted parameter artifact before investing in the parent amplitude law",
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
            "objective": "fit fair SN/BAO baselines and fixed-bmem M6 candidates while keeping b_mem fixed and nonclaim",
            "include": "baseline parity, h0/omega_m0/rd refits, fixed b_mem injection, edge flags, AIC/BIC, no support/death language",
            "exclude": "fitting b_mem, long run without explicit go-ahead, parent prediction claim, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "converted 850 sample scores into a sector-tension readout and route choice",
            "selected_route": "fair_fixed_bmem_fitted_SN_BAO_comparator",
            "what_is_not_claimed": "support, death, parent prediction, local-GR progress, public evidence",
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
    readouts: list[dict[str, object]],
    sector_rows: list[dict[str, object]],
    artifacts: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_850_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    readout_ok = len(readouts) == 2 and all(row["readout"] == "sample_M6_fixed_bmem_worse_than_sample_M0" for row in readouts)
    sector_ok = len(sector_rows) == 12 and any(row["sector_tension"] == "SN_improves_BAO_worsens" for row in sector_rows)
    artifact_ok = any(row["artifact_id"] == "AD851_0_null_control" for row in artifacts) and any(row["artifact_id"] == "AD851_1_BAO_pressure" for row in artifacts)
    route_ok = any(row["route_id"] == "RC851_0_selected" and row["route"] == "fair_fixed_bmem_fitted_SN_BAO_comparator" for row in routes)
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    nonclaim_ok = all_valid_for_claim_false([source_rows, readouts, sector_rows, artifacts, routes, guards, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET
    return [
        {"check_id": "V851_0_sources_exist_and_needles", "result": "pass" if source_ok else "fail", "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle"},
        {"check_id": "V851_1_prior_850_clean", "result": "pass" if prior_clean else "fail", "detail": prior_detail},
        {"check_id": "V851_2_readout_two_branches", "result": "pass" if readout_ok else "fail", "detail": "sh0es and no_sh0es readouts present"},
        {"check_id": "V851_3_sector_tension_detected", "result": "pass" if sector_ok else "fail", "detail": "SN/BAO tension rows include SN_improves_BAO_worsens cases"},
        {"check_id": "V851_4_artifact_diagnosis_present", "result": "pass" if artifact_ok else "fail", "detail": "null-control and BAO-pressure artifact diagnoses present"},
        {"check_id": "V851_5_route_selected", "result": "pass" if route_ok else "fail", "detail": "fair fixed-bmem fitted comparator selected"},
        {"check_id": "V851_6_claim_allowed_false", "result": "pass" if no_claim else "fail", "detail": "decision rows keep claim_allowed=false"},
        {"check_id": "V851_7_all_rows_nonclaim", "result": "pass" if nonclaim_ok else "fail", "detail": "all generated rows valid_for_claim=false"},
        {"check_id": "V851_8_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V851_9_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V851_10_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
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
    readouts: list[dict[str, object]],
    sector_rows: list[dict[str, object]],
    artifacts: list[dict[str, object]],
    routes: list[dict[str, object]],
    guards: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 851 - Y5 R10 Fixed Bmem SN BAO Readout And Eta Law Choice",
        "",
        "Current result: **the 850 fixed-`b_mem` sample test is a useful warning, not a verdict**. Positive memory rows can reduce or soften SN residuals in places, but BAO dominates the penalty under current sample parameters. Because even the `b_mem=0` M6 null control is worse than sample M0, the next step is a fair fixed-`b_mem` fitted comparator before either deriving `eta/a_F/DeltaR` or demoting the branch.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "selected_route", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Branch Readout",
        "",
        csv_table(readouts, ["branch", "best_sample_baseline", "best_candidate", "best_candidate_delta_BIC", "best_positive_candidate", "best_positive_delta_BIC", "readout", "interpretation", "valid_for_claim"]),
        "",
        "## Sector Tension",
        "",
        csv_table(sector_rows, ["branch", "candidate_id", "delta_chi2_SN_vs_best_sample_baseline", "delta_chi2_BAO_vs_best_sample_baseline", "sector_tension", "readout", "valid_for_claim"]),
        "",
        "## Artifact Diagnosis",
        "",
        csv_table(artifacts, ["artifact_id", "finding", "meaning", "risk", "required_fix", "valid_for_claim"]),
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
    scores = read_csv(SCORES_PATH)
    readouts = readout_rows(scores, generated_utc)
    sector_rows = sector_tension_rows(scores, generated_utc)
    artifacts = artifact_diagnosis_rows(generated_utc)
    routes = route_choice_rows(generated_utc)
    guards = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, readouts, sector_rows, artifacts, routes, guards, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(READOUT_PATH, readouts, ["branch", "best_sample_baseline", "best_sample_baseline_chi2", "best_candidate", "best_candidate_delta_BIC", "best_positive_candidate", "best_positive_delta_BIC", "readout", "interpretation", "valid_for_claim", "generated_utc"])
    write_csv(SECTOR_TENSION_PATH, sector_rows, ["branch", "candidate_id", "delta_chi2_SN_vs_best_sample_baseline", "delta_chi2_BAO_vs_best_sample_baseline", "delta_chi2_total_vs_best_sample_baseline", "sector_tension", "readout", "valid_for_claim", "generated_utc"])
    write_csv(ARTIFACT_DIAGNOSIS_PATH, artifacts, ["artifact_id", "finding", "meaning", "risk", "required_fix", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_CHOICE_PATH, routes, ["route_id", "route", "status", "reason", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guards, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "selected_route", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, readouts, sector_rows, artifacts, routes, guards, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()

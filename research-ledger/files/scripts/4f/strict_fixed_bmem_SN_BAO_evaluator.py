from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
SCRIPTS = FORMALIZATION / "scripts"
DEFAULT_CANDIDATES = POST_CHECKPOINT / "source-intake" / "mts_residuals" / "P8_Y5_R10_847_STRICT_COSMOLOGY_CANDIDATES.csv"
DEFAULT_CONFIG = FORMALIZATION / "configs" / "cosmology_background_R1_current.json"
DEFAULT_RUNS = POST_CHECKPOINT / "runs"

sys.path.insert(0, str(SCRIPTS))
import cosmology_likelihood_smoke as cls  # noqa: E402


BASELINE_IDS = ("M0", "M2_wCDM", "M2_CPL")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sample-only fixed-b_mem SN/BAO evaluator.")
    parser.add_argument("--candidates", default=str(DEFAULT_CANDIDATES), help="Strict candidate CSV path.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Cosmology config path.")
    parser.add_argument("--branches", nargs="*", default=["sh0es", "no_sh0es"], help="Pantheon branches.")
    parser.add_argument("--integration-steps", type=int, default=1024, help="Distance integration steps.")
    parser.add_argument("--dry-run", action="store_true", help="Require dry-run mode.")
    parser.add_argument("--sample-score", action="store_true", help="Allow sample likelihood evaluation.")
    parser.add_argument("--no-fit", action="store_true", help="Forbid optimizer/fitting.")
    parser.add_argument("--write-run-dir", action="store_true", help="Write output run directory.")
    parser.add_argument("--output-root", default=str(DEFAULT_RUNS), help="Run output root.")
    return parser.parse_args()


def resolve_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    candidate = POST_CHECKPOINT / path
    if candidate.exists():
        return candidate
    return Path.cwd() / path


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def make_run_dir(output_root: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{stamp}-fixed-bmem-SN-BAO-sample-evaluator"
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_dir


def finite_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def format_float(value: Any) -> str:
    number = finite_float(value)
    return "" if number is None else f"{number:.12g}"


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def model_by_id(config: dict[str, Any], model_id: str) -> dict[str, Any]:
    for model in config.get("models", []):
        if model.get("id") == model_id:
            return model
    raise KeyError(f"missing model config: {model_id}")


def baseline_config(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(source["id"]) + "_sample_fixed",
        "physics_model_id": source["id"],
        "model_family": str(source["id"]) + "_sample_fixed",
        "prior_variant": "sample_no_fit",
        "sample_params": dict(source.get("sample_params", {})),
    }


def candidate_config(candidate: dict[str, str], base_m6: dict[str, Any]) -> dict[str, Any] | None:
    if not bool_text(candidate.get("execution_eligible_for_scoring", "false")):
        return None
    b_mem = finite_float(candidate.get("b_mem_numeric"))
    if b_mem is None:
        return None
    params = dict(base_m6.get("sample_params", {}))
    params["b_mem"] = b_mem
    return {
        "id": "M6_fixed_" + candidate["candidate_id"],
        "physics_model_id": "M6",
        "model_family": "M6_fixed_bmem_nonclaim",
        "prior_variant": "strict_candidate_sample_no_fit",
        "sample_params": params,
    }


def effective_k_for_candidate(candidate: dict[str, str]) -> int:
    total = 0
    for field in ("parameter_count_delta", "family_selection_penalty"):
        number = finite_float(candidate.get(field))
        if number is not None:
            total += int(number)
    return total


def score_row(
    *,
    branch: str,
    row_type: str,
    config_id: str,
    candidate: dict[str, str] | None,
    model_config: dict[str, Any],
    sn: dict[str, Any],
    bao: dict[str, Any],
    n_data: int,
    effective_k: int,
    integration_steps: int,
) -> dict[str, Any]:
    candidate_id = candidate.get("candidate_id", "") if candidate else ""
    claim_label = candidate.get("claim_label", "baseline_sample") if candidate else "baseline_sample"
    try:
        result = cls.evaluate_model(model_config, sn, bao, integration_steps)
        chi2_total = float(result["chi2_total"])
        aic = chi2_total + 2.0 * effective_k
        bic = chi2_total + math.log(float(n_data)) * effective_k
        return {
            "branch": branch,
            "row_type": row_type,
            "config_id": config_id,
            "candidate_id": candidate_id,
            "claim_label": claim_label,
            "physics_model": result.get("physics_model", ""),
            "chi2_sn": format_float(result.get("chi2_sn")),
            "chi2_bao": format_float(result.get("chi2_bao")),
            "chi2_total": format_float(chi2_total),
            "n_data": n_data,
            "effective_k_sample_penalty": effective_k,
            "aic_sample": format_float(aic),
            "bic_sample": format_float(bic),
            "delta_chi2_vs_best_sample_baseline": "",
            "delta_aic_vs_best_sample_baseline": "",
            "delta_bic_vs_best_sample_baseline": "",
            "sample_params_json": json.dumps(result.get("params", {}), sort_keys=True),
            "evaluation_status": "pass",
            "failure_reason": "",
            "fit_executed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "branch": branch,
            "row_type": row_type,
            "config_id": config_id,
            "candidate_id": candidate_id,
            "claim_label": claim_label,
            "physics_model": model_config.get("physics_model_id", model_config.get("id", "")),
            "chi2_sn": "",
            "chi2_bao": "",
            "chi2_total": "",
            "n_data": n_data,
            "effective_k_sample_penalty": effective_k,
            "aic_sample": "",
            "bic_sample": "",
            "delta_chi2_vs_best_sample_baseline": "",
            "delta_aic_vs_best_sample_baseline": "",
            "delta_bic_vs_best_sample_baseline": "",
            "sample_params_json": json.dumps(model_config.get("sample_params", {}), sort_keys=True),
            "evaluation_status": "fail",
            "failure_reason": repr(exc),
            "fit_executed": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        }


def add_baseline_deltas(rows: list[dict[str, Any]]) -> None:
    by_branch: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_branch.setdefault(row["branch"], []).append(row)
    for branch_rows in by_branch.values():
        baselines = [
            row
            for row in branch_rows
            if row["row_type"] == "baseline_sample" and row["evaluation_status"] == "pass"
        ]
        if not baselines:
            continue
        best_chi2 = min(float(row["chi2_total"]) for row in baselines)
        best_aic = min(float(row["aic_sample"]) for row in baselines)
        best_bic = min(float(row["bic_sample"]) for row in baselines)
        for row in branch_rows:
            if row["evaluation_status"] != "pass":
                continue
            row["delta_chi2_vs_best_sample_baseline"] = format_float(float(row["chi2_total"]) - best_chi2)
            row["delta_aic_vs_best_sample_baseline"] = format_float(float(row["aic_sample"]) - best_aic)
            row["delta_bic_vs_best_sample_baseline"] = format_float(float(row["bic_sample"]) - best_bic)


def evaluate(config: dict[str, Any], candidates: list[dict[str, str]], branches: list[str], integration_steps: int) -> list[dict[str, Any]]:
    bao = cls.load_bao(ROOT, cls.select_dataset(config, "BAO"))
    base_m6 = model_by_id(config, "M6")
    baseline_configs = [baseline_config(model_by_id(config, model_id)) for model_id in BASELINE_IDS]
    rows: list[dict[str, Any]] = []
    for branch in branches:
        sn = cls.load_pantheon(ROOT, cls.select_dataset(config, "Pantheon"), branch=branch)
        n_data = int(sn["n"] + bao["n"])
        for model_config in baseline_configs:
            rows.append(
                score_row(
                    branch=branch,
                    row_type="baseline_sample",
                    config_id=model_config["id"],
                    candidate=None,
                    model_config=model_config,
                    sn=sn,
                    bao=bao,
                    n_data=n_data,
                    effective_k=0,
                    integration_steps=integration_steps,
                )
            )
        for candidate in candidates:
            model_config = candidate_config(candidate, base_m6)
            if model_config is None:
                rows.append(
                    {
                        "branch": branch,
                        "row_type": "candidate_fixed_bmem",
                        "config_id": "M6_fixed_" + candidate.get("candidate_id", ""),
                        "candidate_id": candidate.get("candidate_id", ""),
                        "claim_label": candidate.get("claim_label", ""),
                        "physics_model": "M6",
                        "chi2_sn": "",
                        "chi2_bao": "",
                        "chi2_total": "",
                        "n_data": n_data,
                        "effective_k_sample_penalty": effective_k_for_candidate(candidate),
                        "aic_sample": "",
                        "bic_sample": "",
                        "delta_chi2_vs_best_sample_baseline": "",
                        "delta_aic_vs_best_sample_baseline": "",
                        "delta_bic_vs_best_sample_baseline": "",
                        "sample_params_json": "",
                        "evaluation_status": "blocked",
                        "failure_reason": "candidate_not_scoring_eligible_or_missing_numeric_b_mem",
                        "fit_executed": "false",
                        "claim_allowed": "false",
                        "valid_for_claim": "false",
                    }
                )
                continue
            rows.append(
                score_row(
                    branch=branch,
                    row_type="candidate_fixed_bmem",
                    config_id=model_config["id"],
                    candidate=candidate,
                    model_config=model_config,
                    sn=sn,
                    bao=bao,
                    n_data=n_data,
                    effective_k=effective_k_for_candidate(candidate),
                    integration_steps=integration_steps,
                )
            )
    add_baseline_deltas(rows)
    return rows


def write_outputs(run_dir: Path, config_path: Path, candidate_path: Path, rows: list[dict[str, Any]], args: argparse.Namespace) -> dict[str, Any]:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    score_path = run_dir / "FIXED_BMEM_SN_BAO_SAMPLE_SCORES.csv"
    fieldnames = [
        "branch",
        "row_type",
        "config_id",
        "candidate_id",
        "claim_label",
        "physics_model",
        "chi2_sn",
        "chi2_bao",
        "chi2_total",
        "n_data",
        "effective_k_sample_penalty",
        "aic_sample",
        "bic_sample",
        "delta_chi2_vs_best_sample_baseline",
        "delta_aic_vs_best_sample_baseline",
        "delta_bic_vs_best_sample_baseline",
        "sample_params_json",
        "evaluation_status",
        "failure_reason",
        "fit_executed",
        "claim_allowed",
        "valid_for_claim",
    ]
    write_csv(score_path, rows, fieldnames)
    passed = [row for row in rows if row["evaluation_status"] == "pass"]
    blocked = [row for row in rows if row["evaluation_status"] == "blocked"]
    failed = [row for row in rows if row["evaluation_status"] == "fail"]
    status = {
        "status": "fixed_bmem_SN_BAO_sample_scores_written_nonclaim" if not failed else "fixed_bmem_SN_BAO_sample_scores_with_failures",
        "dry_run_only": bool(args.dry_run),
        "sample_score": bool(args.sample_score),
        "no_fit": bool(args.no_fit),
        "fit_executed": False,
        "optimizer_executed": False,
        "claim_allowed": False,
        "config": str(config_path),
        "candidate_file": str(candidate_path),
        "branches": args.branches,
        "integration_steps": args.integration_steps,
        "row_count": len(rows),
        "pass_count": len(passed),
        "blocked_count": len(blocked),
        "failure_count": len(failed),
        "generated_utc": generated_utc,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2, sort_keys=True), encoding="utf-8")
    log_lines = [
        "fixed b_mem SN/BAO sample evaluator",
        f"generated_utc={generated_utc}",
        f"config={config_path}",
        f"candidate_file={candidate_path}",
        f"branches={','.join(args.branches)}",
        f"integration_steps={args.integration_steps}",
        "fit_executed=false",
        "optimizer_executed=false",
        "claim_allowed=false",
        f"row_count={len(rows)}",
        f"pass_count={len(passed)}",
        f"blocked_count={len(blocked)}",
        f"failure_count={len(failed)}",
    ]
    for row in rows:
        log_lines.append(
            f"{row['branch']}::{row['config_id']}: {row['evaluation_status']} "
            f"chi2={row['chi2_total']} delta_bic={row['delta_bic_vs_best_sample_baseline']} "
            f"claim_allowed={row['claim_allowed']}"
        )
    (run_dir / "log.txt").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    (run_dir / "COMPLETE.marker").write_text(generated_utc + "\n", encoding="utf-8")
    return status


def main() -> None:
    args = parse_args()
    if not args.dry_run or not args.no_fit or not args.sample_score:
        raise SystemExit("fixed-bmem evaluator requires --dry-run --sample-score --no-fit")
    candidate_path = resolve_path(args.candidates)
    config_path = resolve_path(args.config)
    if not candidate_path.exists():
        raise SystemExit(f"missing candidates file: {candidate_path}")
    if not config_path.exists():
        raise SystemExit(f"missing config: {config_path}")
    candidates = read_csv_rows(candidate_path)
    config = cls.load_json(config_path)
    rows = evaluate(config, candidates, args.branches, args.integration_steps)
    if args.write_run_dir:
        run_dir = make_run_dir(Path(args.output_root))
        status = write_outputs(run_dir, config_path, candidate_path, rows, args)
        print(f"run_dir={run_dir}")
        print(f"status={status['status']}")
        print(f"row_count={status['row_count']}")
        print(f"failure_count={status['failure_count']}")
        print(f"claim_allowed={status['claim_allowed']}")
    else:
        print(f"row_count={len(rows)}")
        print("fit_executed=false")
        print("claim_allowed=false")


if __name__ == "__main__":
    main()

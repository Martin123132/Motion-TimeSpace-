#!/usr/bin/env python3
"""Dry-run CMB distance-prior gate for the locked B_mem=2/27 branch.

This script deliberately does not score the model.  The CMB distance prior needs
a declared parameter map before a chi2 number is scientifically interpretable.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RUNS_ROOT = POST_CHECKPOINT / "runs"
FORMALIZATION_WORKBENCH = POST_CHECKPOINT.parent / "formalization-workbench"
CMB_DIR = (
    FORMALIZATION_WORKBENCH
    / "data"
    / "cosmology"
    / "growth_CMB"
    / "planck2018_distance_priors"
)
SOURCE_DIR = CMB_DIR / "source"
VECTOR_PATH = CMB_DIR / "planck2018_distance_prior_vector.csv"
COVARIANCE_PATH = CMB_DIR / "planck2018_distance_prior_covariance.csv"
VALIDATION_PATH = CMB_DIR / "covariance_validation.csv"
ROW_LOCK_PATH = CMB_DIR / "row_lock_manifest.json"

LOCKED_BRANCH = "canonical_R_2over27_locked_amplitude"
LOCKED_P = 3.0
LOCKED_U3 = 0.25
LOCKED_DELTA_R = 2.0 / 9.0
LOCKED_B_MEM = 2.0 / 27.0
LOCKED_ETA = 1.0
LOCKED_A_F = 1.0

STATUS = "locked_2over27_CMB_distance_dryrun_pass_score_blocked_pending_parameter_map"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def read_manifest() -> dict[str, Any]:
    with ROW_LOCK_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def expected_paths() -> list[Path]:
    paths = [VECTOR_PATH, COVARIANCE_PATH, VALIDATION_PATH, ROW_LOCK_PATH]
    if SOURCE_DIR.exists():
        paths.extend(sorted(path for path in SOURCE_DIR.iterdir() if path.is_file()))
    return paths


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in expected_paths():
        exists = path.exists()
        rows.append(
            {
                "source_id": "Planck2018_distance_priors_Chen_Huang_Wang",
                "kind": "directory_source" if path.parent == SOURCE_DIR else "machine_table",
                "path": str(path),
                "exists": exists,
                "readable": exists and path.is_file(),
                "bytes": path.stat().st_size if exists and path.is_file() else "",
                "sha256": file_sha256(path) if exists and path.is_file() else "",
                "issue": "" if exists else "missing",
            }
        )
    return rows


def vector_report_rows(vector_rows: list[dict[str, str]], manifest: dict[str, Any]) -> list[dict[str, Any]]:
    source_id = manifest.get("source_id", "")
    expected_parameters = list(manifest.get("parameters", []))
    manifest_models = [entry["model"] for entry in manifest.get("models", [])]
    rows: list[dict[str, Any]] = []
    by_model_parameter = {
        (row.get("model", ""), row.get("parameter", "")): row for row in vector_rows
    }

    for model in manifest_models:
        for parameter in expected_parameters:
            source_row = by_model_parameter.get((model, parameter), {})
            mean = source_row.get("mean", "")
            sigma = source_row.get("sigma_symmetrized", "")
            numeric_status = "pass"
            issue = ""
            try:
                mean_value = float(mean)
                sigma_value = float(sigma)
                if not np.isfinite(mean_value) or not np.isfinite(sigma_value) or sigma_value <= 0.0:
                    numeric_status = "fail"
                    issue = "mean_or_sigma_not_finite_positive"
            except Exception as exc:  # noqa: BLE001
                numeric_status = "fail"
                issue = str(exc)
            rows.append(
                {
                    "source_id": source_id,
                    "model": model,
                    "parameter": parameter,
                    "row_present": bool(source_row),
                    "mean": mean,
                    "sigma_symmetrized": sigma,
                    "default_for_C0": source_row.get("default_for_C0", ""),
                    "numeric_status": numeric_status if source_row else "fail",
                    "source": source_row.get("source", ""),
                    "source_table_detected_in_eprint": source_row.get(
                        "source_table_detected_in_eprint", ""
                    ),
                    "notes": source_row.get("notes", ""),
                    "issue": issue if source_row else "missing_vector_row",
                }
            )
    return rows


def covariance_report_rows(covariance_rows: list[dict[str, str]], manifest: dict[str, Any]) -> list[dict[str, Any]]:
    source_id = manifest.get("source_id", "")
    expected_parameters = list(manifest.get("parameters", []))
    manifest_models = [entry["model"] for entry in manifest.get("models", [])]
    rows: list[dict[str, Any]] = []

    by_model = {model: [] for model in manifest_models}
    for row in covariance_rows:
        if row.get("model") in by_model:
            by_model[row["model"]].append(row)

    for model in manifest_models:
        parameter_index = {parameter: index for index, parameter in enumerate(expected_parameters)}
        matrix = np.full((len(expected_parameters), len(expected_parameters)), np.nan, dtype=float)
        issues: list[str] = []

        for row in by_model.get(model, []):
            row_parameter = row.get("row_parameter", "")
            col_parameter = row.get("col_parameter", "")
            if row_parameter not in parameter_index or col_parameter not in parameter_index:
                issues.append(f"unexpected_parameter:{row_parameter}:{col_parameter}")
                continue
            try:
                matrix[parameter_index[row_parameter], parameter_index[col_parameter]] = float(
                    row.get("covariance", "")
                )
            except Exception as exc:  # noqa: BLE001
                issues.append(f"bad_covariance:{row_parameter}:{col_parameter}:{exc}")

        finite = bool(np.isfinite(matrix).all())
        symmetry_residual = float(np.nanmax(np.abs(matrix - matrix.T))) if finite else float("nan")
        symmetric = finite and bool(np.allclose(matrix, matrix.T, rtol=0.0, atol=1.0e-14))
        eigenvalues = np.linalg.eigvalsh(matrix) if finite and symmetric else np.array([])
        min_eigenvalue = float(eigenvalues[0]) if eigenvalues.size else ""
        max_eigenvalue = float(eigenvalues[-1]) if eigenvalues.size else ""
        cholesky_pass = False
        cholesky_detail = "not_attempted"
        if finite and symmetric:
            try:
                np.linalg.cholesky(matrix)
                cholesky_pass = True
                cholesky_detail = "cholesky_pass"
            except Exception as exc:  # noqa: BLE001
                cholesky_detail = f"cholesky_fail:{exc}"

        model_manifest = next(
            (entry for entry in manifest.get("models", []) if entry.get("model") == model),
            {},
        )
        status = "pass" if finite and symmetric and cholesky_pass and not issues else "fail"
        rows.append(
            {
                "source_id": source_id,
                "model": model,
                "parameter_order": ";".join(expected_parameters),
                "covariance_rows_seen": len(by_model.get(model, [])),
                "expected_elements": len(expected_parameters) ** 2,
                "dimension_status": model_manifest.get("dimension_status", ""),
                "finite": finite,
                "symmetric": symmetric,
                "max_symmetry_residual": symmetry_residual,
                "cholesky_pass": cholesky_pass,
                "cholesky_detail": cholesky_detail,
                "min_eigenvalue": min_eigenvalue,
                "max_eigenvalue": max_eigenvalue,
                "default_for_C0": model_manifest.get("default_for_C0", ""),
                "status": status,
                "issue": ";".join(issues),
            }
        )
    return rows


def prior_model_register_rows(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for entry in manifest.get("models", []):
        rows.append(
            {
                "source_id": manifest.get("source_id", ""),
                "model": entry.get("model", ""),
                "default_model": manifest.get("default_model", ""),
                "parameters": ";".join(manifest.get("parameters", [])),
                "vector_length": entry.get("vector_length", ""),
                "covariance_shape": f"{entry.get('covariance_rows', '')}x{entry.get('covariance_cols', '')}",
                "dimension_status": entry.get("dimension_status", ""),
                "symmetric": entry.get("symmetric", ""),
                "cholesky_pass": entry.get("cholesky_pass", ""),
                "default_for_C0": entry.get("default_for_C0", ""),
                "use_status": entry.get("use_status", ""),
                "claim_ceiling": "compressed_distance_prior_internal_stress_test_only",
            }
        )
    return rows


def locked_branch_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": LOCKED_BRANCH,
            "quantity": "p",
            "value": LOCKED_P,
            "status": "frozen",
            "source": "112-two-over-27-external-holdout-manifest",
            "claim_ceiling": "predeclared_empirical_closure",
        },
        {
            "branch": LOCKED_BRANCH,
            "quantity": "u3",
            "value": LOCKED_U3,
            "status": "frozen",
            "source": "112-two-over-27-external-holdout-manifest",
            "claim_ceiling": "predeclared_empirical_closure",
        },
        {
            "branch": LOCKED_BRANCH,
            "quantity": "DeltaR",
            "value": LOCKED_DELTA_R,
            "status": "frozen",
            "source": "112-two-over-27-external-holdout-manifest",
            "claim_ceiling": "endpoint_quadratic_target_not_parent_derived",
        },
        {
            "branch": LOCKED_BRANCH,
            "quantity": "B_mem",
            "value": LOCKED_B_MEM,
            "status": "frozen",
            "source": "112-two-over-27-external-holdout-manifest",
            "claim_ceiling": "locked_amplitude_not_fitted_in_holdout",
        },
        {
            "branch": LOCKED_BRANCH,
            "quantity": "eta",
            "value": LOCKED_ETA,
            "status": "frozen",
            "source": "112-two-over-27-external-holdout-manifest",
            "claim_ceiling": "normalization_choice_not_parent_derived",
        },
        {
            "branch": LOCKED_BRANCH,
            "quantity": "a_F",
            "value": LOCKED_A_F,
            "status": "frozen",
            "source": "112-two-over-27-external-holdout-manifest",
            "claim_ceiling": "normalization_choice_not_parent_derived",
        },
    ]


def cmb_parameter_map_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_item": "H0_or_h",
            "required_choice": "declare whether h is fitted, inherited from SN+BAO/BAO, or fixed to baseline Planck-compatible value",
            "current_status": "blocking_open",
            "baseline_symmetry_rule": "same freedom must be available to LCDM/wCDM/CPL comparisons",
            "score_action": "do_not_score_until_declared",
        },
        {
            "contract_item": "Omega_m0",
            "required_choice": "declare whether Omega_m0 is CMB-fitted, imported from BAO-only, or jointly optimized",
            "current_status": "blocking_open",
            "baseline_symmetry_rule": "same optimization protocol for baselines and locked branch",
            "score_action": "do_not_score_until_declared",
        },
        {
            "contract_item": "Omega_b_h2",
            "required_choice": "fix to prior-vector mean, fit with prior covariance, or set external baryon prior",
            "current_status": "blocking_open",
            "baseline_symmetry_rule": "same baryon treatment for all branches",
            "score_action": "do_not_score_until_declared",
        },
        {
            "contract_item": "n_s",
            "required_choice": "fix to prior-vector mean, fit with prior covariance, or declare unused in reduced distance-only score",
            "current_status": "blocking_open",
            "baseline_symmetry_rule": "same spectral-index treatment for all branches",
            "score_action": "do_not_score_until_declared",
        },
        {
            "contract_item": "radiation_sector",
            "required_choice": "lock Tcmb, N_eff, photon density, neutrino/radiation convention, and early-time E(z)",
            "current_status": "blocking_open",
            "baseline_symmetry_rule": "standard radiation conventions for all branches unless parent action derives otherwise",
            "score_action": "do_not_score_until_declared",
        },
        {
            "contract_item": "z_star_and_sound_horizon",
            "required_choice": "use repaired scale_factor_quad sound-horizon integral and declared z_star prescription",
            "current_status": "method_known_but_branch_map_open",
            "baseline_symmetry_rule": "same numerical integral and z_star prescription for all branches",
            "score_action": "block_score_until_written_as_contract",
        },
        {
            "contract_item": "distance_prior_choice",
            "required_choice": "score sensitivity to at least LCDM and wCDM compressed prior tables",
            "current_status": "warning_open",
            "baseline_symmetry_rule": "do not tune prior-table choice only for MTS",
            "score_action": "allowed_only_as_internal_sensitivity_after_parameter_map",
        },
        {
            "contract_item": "calibration_freedom",
            "required_choice": "no hidden CMB calibration rescue; any calibration parameter must be predeclared and shared with baselines",
            "current_status": "locked_guardrail",
            "baseline_symmetry_rule": "equal rescue freedom or no rescue freedom",
            "score_action": "enforce_in_score_script",
        },
        {
            "contract_item": "perturbation_level_claim",
            "required_choice": "distance-prior score is not a perturbation/CMB-spectrum proof",
            "current_status": "locked_claim_ceiling",
            "baseline_symmetry_rule": "not applicable",
            "score_action": "report_as_background_distance_stress_only",
        },
    ]


def dryrun_gate_rows(
    source_rows: list[dict[str, Any]],
    vector_rows: list[dict[str, Any]],
    covariance_rows: list[dict[str, Any]],
    manifest: dict[str, Any],
) -> list[dict[str, Any]]:
    missing_sources = [row["path"] for row in source_rows if not row["exists"]]
    vector_failures = [row for row in vector_rows if row["numeric_status"] != "pass"]
    covariance_failures = [row for row in covariance_rows if row["status"] != "pass"]
    default_model = manifest.get("default_model", "")
    default_available = any(
        row["model"] == default_model and parse_bool(row["default_for_C0"])
        for row in covariance_rows
    )
    return [
        {
            "gate": "source_files_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": f"missing_count={len(missing_sources)}",
            "next_action": "repair_source_paths_before_any_score" if missing_sources else "none",
        },
        {
            "gate": "distance_prior_vector_parse",
            "status": "pass" if not vector_failures else "fail",
            "evidence": f"vector_rows={len(vector_rows)} failures={len(vector_failures)}",
            "next_action": "repair_vector_rows" if vector_failures else "none",
        },
        {
            "gate": "distance_prior_covariance_reconstruct",
            "status": "pass" if not covariance_failures else "fail",
            "evidence": f"models={len(covariance_rows)} failures={len(covariance_failures)}",
            "next_action": "repair_covariance_rows" if covariance_failures else "none",
        },
        {
            "gate": "default_wCDM_prior_available",
            "status": "pass" if default_model == "wCDM" and default_available else "fail",
            "evidence": f"default_model={default_model} available={default_available}",
            "next_action": "audit_row_lock_manifest" if not default_available else "none",
        },
        {
            "gate": "locked_2over27_constants_frozen",
            "status": "pass",
            "evidence": "p=3; u3=1/4; DeltaR=2/9; B_mem=2/27; eta=1; a_F=1",
            "next_action": "none",
        },
        {
            "gate": "repaired_sound_horizon_method_required",
            "status": "pass",
            "evidence": "legacy CMB score demoted; future score must use scale_factor_quad",
            "next_action": "write method into next score contract",
        },
        {
            "gate": "compressed_prior_model_dependence",
            "status": "warning",
            "evidence": "distance priors are model-compressed; score must check LCDM and wCDM prior tables",
            "next_action": "run prior-table sensitivity after parameter map exists",
        },
        {
            "gate": "locked_branch_CMB_parameter_map",
            "status": "blocked",
            "evidence": "H0/h, Omega_m0, Omega_b_h2, n_s, radiation, z_star map not yet declared",
            "next_action": "create 115-locked-2over27-CMB-parameter-map-contract.md",
        },
        {
            "gate": "CMB_distance_score_execution",
            "status": "blocked",
            "evidence": "dry-run only; no chi2 generated",
            "next_action": "score only after parameter-map contract passes",
        },
    ]


def score_blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "CMB_MAP_001",
            "blocker": "H0/h treatment undeclared",
            "severity": "blocking",
            "why_it_matters": "R and l_A depend directly on distances and sound horizon normalization",
            "resolution_required": "predeclare fixed/fitted/imported h rule shared with baselines",
        },
        {
            "blocker_id": "CMB_MAP_002",
            "blocker": "Omega_m0 treatment undeclared",
            "severity": "blocking",
            "why_it_matters": "CMB distance and BAO distance comparisons cannot mix optimized and imported Omega_m rules",
            "resolution_required": "predeclare CMB-only, BAO-imported, or joint-optimized protocol",
        },
        {
            "blocker_id": "CMB_MAP_003",
            "blocker": "Omega_b_h2 and n_s nuisance treatment undeclared",
            "severity": "blocking",
            "why_it_matters": "the compressed prior vector includes these entries and their covariance",
            "resolution_required": "predeclare fixed means or covariance-fitted nuisance handling",
        },
        {
            "blocker_id": "CMB_MAP_004",
            "blocker": "early radiation and z_star convention undeclared for locked branch",
            "severity": "blocking",
            "why_it_matters": "sound horizon integral is sensitive to early-time assumptions",
            "resolution_required": "lock Tcmb, N_eff, radiation density, z_star, and scale_factor_quad integral",
        },
        {
            "blocker_id": "CMB_MAP_005",
            "blocker": "compressed-prior table sensitivity not yet run",
            "severity": "warning_after_map",
            "why_it_matters": "Planck distance-prior rows are model-dependent compressed summaries",
            "resolution_required": "score at minimum LCDM-prior and wCDM-prior tables after map is declared",
        },
        {
            "blocker_id": "CMB_MAP_006",
            "blocker": "no perturbation closure",
            "severity": "claim_ceiling",
            "why_it_matters": "distance priors do not test the full CMB spectrum or perturbation dynamics",
            "resolution_required": "report any result as background-distance stress only",
        },
    ]


def command_template_rows(script_path: Path) -> list[dict[str, Any]]:
    python_exe = POST_CHECKPOINT / ".venv-score" / "Scripts" / "python.exe"
    return [
        {
            "command_id": "dryrun_repeat",
            "status": "available",
            "command": f'"{python_exe}" "{script_path}" --dry-run',
            "purpose": "repeat the source/data/contract dry-run without scoring",
        },
        {
            "command_id": "future_score",
            "status": "blocked_pending_115_contract",
            "command": "not_emitted_until_CMB_parameter_map_contract_passes",
            "purpose": "avoid producing an uninterpretable CMB chi2",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "dryrun_status",
            "value": STATUS,
            "rationale": "Planck prior tables are present and valid; locked branch is registered; score is blocked until parameter map exists",
        },
        {
            "decision": "score_ran",
            "value": False,
            "rationale": "CMB distance score would be a disguised convention choice without H0/Omega_m/baryon/radiation contract",
        },
        {
            "decision": "theory_promotion_allowed",
            "value": False,
            "rationale": "This is only a dry-run gate, not a CMB prediction or parent-action derivation",
        },
        {
            "decision": "next_target",
            "value": "115-locked-2over27-CMB-parameter-map-contract.md",
            "rationale": "declare the exact fair CMB parameter map before scoring the locked branch",
        },
    ]


def run_dry_run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-locked-2over27-CMB-distance-dryrun"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    manifest = read_manifest()
    raw_vector_rows = read_csv_rows(VECTOR_PATH)
    raw_covariance_rows = read_csv_rows(COVARIANCE_PATH)

    sources = source_register_rows()
    vectors = vector_report_rows(raw_vector_rows, manifest)
    covariances = covariance_report_rows(raw_covariance_rows, manifest)
    prior_models = prior_model_register_rows(manifest)
    locked_branch = locked_branch_register_rows()
    parameter_contract = cmb_parameter_map_contract_rows()
    gates = dryrun_gate_rows(sources, vectors, covariances, manifest)
    blockers = score_blocker_rows()
    commands = command_template_rows(Path(__file__).resolve())
    decisions = decision_rows()

    write_csv(
        results_dir / "source_register.csv",
        sources,
        ["source_id", "kind", "path", "exists", "readable", "bytes", "sha256", "issue"],
    )
    write_csv(
        results_dir / "distance_prior_vector_report.csv",
        vectors,
        [
            "source_id",
            "model",
            "parameter",
            "row_present",
            "mean",
            "sigma_symmetrized",
            "default_for_C0",
            "numeric_status",
            "source",
            "source_table_detected_in_eprint",
            "notes",
            "issue",
        ],
    )
    write_csv(
        results_dir / "distance_prior_covariance_report.csv",
        covariances,
        [
            "source_id",
            "model",
            "parameter_order",
            "covariance_rows_seen",
            "expected_elements",
            "dimension_status",
            "finite",
            "symmetric",
            "max_symmetry_residual",
            "cholesky_pass",
            "cholesky_detail",
            "min_eigenvalue",
            "max_eigenvalue",
            "default_for_C0",
            "status",
            "issue",
        ],
    )
    write_csv(
        results_dir / "prior_model_register.csv",
        prior_models,
        [
            "source_id",
            "model",
            "default_model",
            "parameters",
            "vector_length",
            "covariance_shape",
            "dimension_status",
            "symmetric",
            "cholesky_pass",
            "default_for_C0",
            "use_status",
            "claim_ceiling",
        ],
    )
    write_csv(
        results_dir / "locked_branch_register.csv",
        locked_branch,
        ["branch", "quantity", "value", "status", "source", "claim_ceiling"],
    )
    write_csv(
        results_dir / "cmb_parameter_map_contract.csv",
        parameter_contract,
        [
            "contract_item",
            "required_choice",
            "current_status",
            "baseline_symmetry_rule",
            "score_action",
        ],
    )
    write_csv(
        results_dir / "dryrun_gates.csv",
        gates,
        ["gate", "status", "evidence", "next_action"],
    )
    write_csv(
        results_dir / "score_blockers.csv",
        blockers,
        ["blocker_id", "blocker", "severity", "why_it_matters", "resolution_required"],
    )
    write_csv(
        results_dir / "command_templates.csv",
        commands,
        ["command_id", "status", "command", "purpose"],
    )
    write_csv(
        results_dir / "decision.csv",
        decisions,
        ["decision", "value", "rationale"],
    )

    pass_count = sum(1 for row in gates if row["status"] == "pass")
    warning_count = sum(1 for row in gates if row["status"] == "warning")
    blocked_count = sum(1 for row in gates if row["status"] == "blocked")
    fail_count = sum(1 for row in gates if row["status"] == "fail")
    status = {
        "status": STATUS if fail_count == 0 else "locked_2over27_CMB_distance_dryrun_fail",
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "branch": LOCKED_BRANCH,
        "score_ran": False,
        "claim_ceiling": "CMB_distance_dryrun_only_not_score_not_prediction",
        "locked_constants": {
            "p": LOCKED_P,
            "u3": LOCKED_U3,
            "DeltaR": LOCKED_DELTA_R,
            "B_mem": LOCKED_B_MEM,
            "eta": LOCKED_ETA,
            "a_F": LOCKED_A_F,
        },
        "source_rows": len(sources),
        "vector_rows": len(vectors),
        "covariance_models": len(covariances),
        "gate_counts": {
            "pass": pass_count,
            "warning": warning_count,
            "blocked": blocked_count,
            "fail": fail_count,
        },
        "next_target": "115-locked-2over27-CMB-parameter-map-contract.md",
        "created_utc_note": "timestamp uses local machine time",
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Dry-run CMB distance-prior gate for the locked B_mem=2/27 branch."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run the dry-run gate. This is the only implemented mode; no scoring is performed.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=RUNS_ROOT,
        help="Directory where timestamped run artifacts are written.",
    )
    args = parser.parse_args()
    if not args.dry_run:
        raise SystemExit("Only --dry-run is implemented. CMB score is blocked pending parameter-map contract.")
    run_dry_run(args.output_root)


if __name__ == "__main__":
    main()

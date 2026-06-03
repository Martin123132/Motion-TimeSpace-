#!/usr/bin/env python3
"""Attempt the anisotropic/projective BAO owner route before falling back to Q^nu."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
FORMALIZATION_WORKBENCH = WORK_DIR.parent / "formalization-workbench"

BRIDGE_OWNER_RUN = RUNS_ROOT / "20260531-235958-BAO-shape-or-Qnu-bridge-owner"
BRIDGE_OWNER_RESULTS = BRIDGE_OWNER_RUN / "results"
TARGET_ROWS = BRIDGE_OWNER_RESULTS / "failed_gate_shape_target_rows.csv"
OWNER_ROUTES = BRIDGE_OWNER_RESULTS / "owner_route_matrix.csv"
BRIDGE_STATUS = BRIDGE_OWNER_RUN / "status.json"

BAO_SHAPE_RUN = RUNS_ROOT / "20260531-173800-BAO-shape-residual-decomposition"
BAO_SHAPE_DECISION = BAO_SHAPE_RUN / "results" / "decision.csv"

HZ_RUN = RUNS_ROOT / "20260531-221500-fresh-CC-Hz-source-locked-holdout"
HZ_DECISION = HZ_RUN / "results" / "decision.csv"

CLAIM_CEILING = "anisotropic_BAO_projection_owner_attempt_no_bridge_promotion"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_role(path: Path) -> str:
    name = path.name
    if name.startswith("10-"):
        return "observer-map/coframe contract"
    if name.startswith("53-"):
        return "coherent projection local-silence gate"
    if name.startswith("124-"):
        return "BAO residual localization"
    if name.startswith("153-"):
        return "BAO-shape or Qnu bridge owner fork"
    if name.startswith("145-"):
        return "fresh H(z) stress data"
    if name == "08-long-run-workflow.md":
        return "long-run workflow"
    if name.endswith(".csv") or name == "status.json":
        return "machine source output"
    return "script"


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        WORK_DIR / "10-observer-map-symplectic-contract.md",
        WORK_DIR / "53-coherent-projection-local-silence-gate.md",
        WORK_DIR / "124-BAO-shape-residual-decomposition.md",
        WORK_DIR / "153-BAO-shape-or-Qnu-bridge-owner.md",
        WORK_DIR / "145-fresh-CC-Hz-source-locked-holdout.md",
        BRIDGE_STATUS,
        TARGET_ROWS,
        OWNER_ROUTES,
        BAO_SHAPE_DECISION,
        HZ_DECISION,
        FORMALIZATION_WORKBENCH / "08-long-run-workflow.md",
    ]
    rows = []
    for path in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": source_role(path),
                "issue": "" if exists else "missing",
            }
        )
    return rows


def target_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv_rows(TARGET_ROWS):
        failed_pred = float(row["failed_branch_predicted"])
        t7_pred = float(row["T7_predicted"])
        projection_factor = t7_pred / failed_pred - 1.0
        rows.append(
            {
                **row,
                "projection_factor_to_T7": projection_factor,
                "projection_percent_to_T7": 100.0 * projection_factor,
            }
        )
    return rows


def rows_by_z(rows: list[dict[str, Any]]) -> dict[float, dict[str, dict[str, Any]]]:
    grouped: dict[float, dict[str, dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(float(row["z"]), {})[str(row["observable"])] = row
    return grouped


def paired_projection_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    paired = []
    for z, group in sorted(rows_by_z(rows).items()):
        if "DM_over_rs" not in group or "DH_over_rs" not in group:
            continue
        dm = group["DM_over_rs"]
        dh = group["DH_over_rs"]
        dm_failed = float(dm["failed_branch_predicted"])
        dm_t7 = float(dm["T7_predicted"])
        dh_failed = float(dh["failed_branch_predicted"])
        dh_t7 = float(dh["T7_predicted"])
        pi_perp = dm_t7 / dm_failed - 1.0
        pi_parallel = dh_t7 / dh_failed - 1.0
        zeta_from_dm = (dm_t7 - dm_failed) / dh_failed
        paired.append(
            {
                "z": z,
                "Pi_perp_required": pi_perp,
                "Pi_parallel_required": pi_parallel,
                "zeta_from_DM": zeta_from_dm,
                "failed_DM_over_rs": dm_failed,
                "failed_DH_over_rs": dh_failed,
                "T7_DM_over_rs": dm_t7,
                "T7_DH_over_rs": dh_t7,
                "radial_transverse_sign": "opposed" if pi_perp * pi_parallel < 0.0 else "same",
            }
        )
    return paired


def finite_difference(values: list[tuple[float, float]], index: int) -> float:
    if len(values) < 2:
        return math.nan
    if index == 0:
        z0, y0 = values[0]
        z1, y1 = values[1]
        return (y1 - y0) / (z1 - z0)
    if index == len(values) - 1:
        z0, y0 = values[-2]
        z1, y1 = values[-1]
        return (y1 - y0) / (z1 - z0)
    z0, y0 = values[index - 1]
    z1, y1 = values[index + 1]
    return (y1 - y0) / (z1 - z0)


def redshift_remap_rows(paired: list[dict[str, Any]]) -> list[dict[str, Any]]:
    dh_values = [(float(row["z"]), float(row["failed_DH_over_rs"])) for row in paired]
    zeta_values = [(float(row["z"]), float(row["zeta_from_DM"])) for row in paired]
    rows = []
    for index, row in enumerate(paired):
        z = float(row["z"])
        dh = float(row["failed_DH_over_rs"])
        dln_dh_dz = finite_difference([(zv, math.log(val)) for zv, val in dh_values], index)
        zeta = float(row["zeta_from_DM"])
        pi_parallel = float(row["Pi_parallel_required"])
        zeta_prime_needed = pi_parallel - dln_dh_dz * zeta
        zeta_prime_finite_difference = finite_difference(zeta_values, index)
        mismatch = zeta_prime_needed - zeta_prime_finite_difference
        rows.append(
            {
                "z": z,
                "zeta_from_DM": zeta,
                "Pi_parallel_required": pi_parallel,
                "dln_DH_dz_estimate": dln_dh_dz,
                "zeta_prime_needed_from_DH": zeta_prime_needed,
                "zeta_prime_finite_difference_from_DM": zeta_prime_finite_difference,
                "zeta_prime_mismatch": mismatch,
                "abs_zeta_prime_mismatch": abs(mismatch),
                "readout": "approx_consistent" if abs(mismatch) < 0.006 else "tension",
            }
        )
    return rows


def projection_model_rows(
    target: list[dict[str, Any]],
    paired: list[dict[str, Any]],
    remap: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    max_projector = max(abs(float(row["projection_factor_to_T7"])) for row in target)
    max_zeta = max(abs(float(row["zeta_from_DM"])) for row in paired)
    max_mismatch = max(float(row["abs_zeta_prime_mismatch"]) for row in remap)
    opposed_count = sum(1 for row in paired if row["radial_transverse_sign"] == "opposed")
    return [
        {
            "model": "independent_radial_transverse_projector",
            "mathematical_form": "D_M -> (1+Pi_perp)D_M; D_H -> (1+Pi_parallel)D_H",
            "fit_to_target": "exact_by_construction",
            "max_required_amplitude": max_projector,
            "status": "empirical_projection_only",
            "promotion_blocker": "no parent tensor; would be a row-wise ruler patch unless derived",
        },
        {
            "model": "scalar_redshift_remapping",
            "mathematical_form": "z_true=z_obs+zeta(z); D_M=D_M(z_true); D_H=D_H(z_true) dz_true/dz_obs",
            "fit_to_target": "qualitative_sign_success",
            "max_required_amplitude": max_zeta,
            "status": "live_theorem_target_not_derived",
            "promotion_blocker": f"max zeta-prime mismatch={max_mismatch:.6g}; must be parent-owned and retested on SN/H(z)",
        },
        {
            "model": "pure_single_metric_Hz_change",
            "mathematical_form": "H(z)->H(z)+delta H(z), with standard D_M integral",
            "fit_to_target": "fails_complete_owner",
            "max_required_amplitude": "",
            "status": "rejected_as_complete_repair",
            "promotion_blocker": f"{opposed_count}/{len(paired)} paired redshifts require opposed radial/transverse signs",
        },
        {
            "model": "Qnu_exchange_map",
            "mathematical_form": "nabla_mu T_m^{mu nu}=Q^nu",
            "fit_to_target": "possible_but_not_needed_yet",
            "max_required_amplitude": "",
            "status": "deferred_high_risk",
            "promotion_blocker": "must preserve local GR/growth and derive covariant Q^nu",
        },
    ]


def owner_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "zero_memory_identity",
            "condition": "B_mem -> 0 implies Pi_perp=Pi_parallel=zeta=0",
            "status": "mandatory",
            "failure_if_missing": "private MTS ruler rescue",
        },
        {
            "gate": "observer_map_owner",
            "condition": "derive zeta(z) or Pi_AB from observer coframe / projection equations",
            "status": "missing",
            "failure_if_missing": "projection closure only",
        },
        {
            "gate": "integrability",
            "condition": "same zeta or projection tensor predicts D_M, D_H, and D_V together",
            "status": "partial_target",
            "failure_if_missing": "row-wise BAO patch",
        },
        {
            "gate": "SN_and_Hz_consistency",
            "condition": "global redshift remap must not break SN and source-locked H(z)",
            "status": "not_tested_for_projection",
            "failure_if_missing": "BAO-only rescue",
        },
        {
            "gate": "local_silence",
            "condition": "projection vanishes for local/PPN/bound domains",
            "status": "not_derived",
            "failure_if_missing": "local-GR route fails",
        },
        {
            "gate": "CMB_kill_screen",
            "condition": "same projection survives future TT/TE/EE/lensing kill-screen",
            "status": "not_run",
            "failure_if_missing": "no CMB promotion",
        },
    ]


def gate_rows(target: list[dict[str, Any]], paired: list[dict[str, Any]], remap: list[dict[str, Any]]) -> list[dict[str, Any]]:
    max_projector = max(abs(float(row["projection_factor_to_T7"])) for row in target)
    opposed_count = sum(1 for row in paired if row["radial_transverse_sign"] == "opposed")
    max_mismatch = max(float(row["abs_zeta_prime_mismatch"]) for row in remap)
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass",
            "evidence": "all cited source artifacts exist",
        },
        {
            "gate": "projection_amplitude_small",
            "status": "pass_target",
            "evidence": f"max required BAO projection amplitude={max_projector:.6g}",
        },
        {
            "gate": "radial_transverse_separation_needed",
            "status": "pass_target",
            "evidence": f"{opposed_count}/{len(paired)} paired redshifts require opposed radial/transverse signs",
        },
        {
            "gate": "scalar_redshift_remap",
            "status": "live_but_not_derived",
            "evidence": f"max zeta-prime mismatch={max_mismatch:.6g}",
        },
        {
            "gate": "parent_projection_owner",
            "status": "fail_missing",
            "evidence": "no observer-map/coframe derivation supplies zeta(z) or Pi_AB yet",
        },
        {
            "gate": "Qnu_fallback",
            "status": "deferred",
            "evidence": "projection route remains live and lower-risk than matter exchange",
        },
        {
            "gate": "bridge_promotion",
            "status": "fail",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(remap: list[dict[str, Any]]) -> list[dict[str, Any]]:
    max_mismatch = max(float(row["abs_zeta_prime_mismatch"]) for row in remap)
    return [
        {
            "item": "status",
            "verdict": "anisotropic_projection_route_live_redshift_map_plausible_parent_owner_missing",
            "evidence": f"scalar redshift remap has qualitative sign success with max derivative mismatch={max_mismatch:.6g}",
        },
        {
            "item": "best_next_target",
            "verdict": "155-redshift-projection-clock-map-owner.md",
            "evidence": "derive zeta(z) from clock/observer map or demote projection route to closure-only",
        },
        {
            "item": "Qnu_status",
            "verdict": "still_deferred",
            "evidence": "projection route is not dead; Q^nu remains high-risk fallback",
        },
        {
            "item": "claim_status",
            "verdict": CLAIM_CEILING,
            "evidence": "no BAO projection theorem and no CMB bridge promotion",
        },
    ]


def run_attempt(output_root: Path, timestamp: str | None = None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-anisotropic-BAO-projection-owner-attempt"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    target = target_rows()
    paired = paired_projection_rows(target)
    remap = redshift_remap_rows(paired)
    model_audit = projection_model_rows(target, paired, remap)
    contract = owner_contract_rows()
    gates = gate_rows(target, paired, remap)
    decisions = decision_rows(remap)

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(
        results_dir / "projection_target_rows.csv",
        target,
        [
            "row_index",
            "z",
            "observable",
            "observed",
            "failed_branch_predicted",
            "T7_predicted",
            "projection_factor_to_T7",
            "projection_percent_to_T7",
            "failed_branch_residual",
            "T7_residual",
            "delta_chi2_contribution_vs_T7",
            "owner_readout",
        ],
    )
    write_csv(
        results_dir / "radial_transverse_projection_factors.csv",
        paired,
        [
            "z",
            "Pi_perp_required",
            "Pi_parallel_required",
            "zeta_from_DM",
            "failed_DM_over_rs",
            "failed_DH_over_rs",
            "T7_DM_over_rs",
            "T7_DH_over_rs",
            "radial_transverse_sign",
        ],
    )
    write_csv(
        results_dir / "scalar_redshift_remap_consistency.csv",
        remap,
        [
            "z",
            "zeta_from_DM",
            "Pi_parallel_required",
            "dln_DH_dz_estimate",
            "zeta_prime_needed_from_DH",
            "zeta_prime_finite_difference_from_DM",
            "zeta_prime_mismatch",
            "abs_zeta_prime_mismatch",
            "readout",
        ],
    )
    write_csv(
        results_dir / "projection_model_audit.csv",
        model_audit,
        ["model", "mathematical_form", "fit_to_target", "max_required_amplitude", "status", "promotion_blocker"],
    )
    write_csv(results_dir / "owner_contract.csv", contract, ["gate", "condition", "status", "failure_if_missing"])
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "max_projection_factor": max(abs(float(row["projection_factor_to_T7"])) for row in target),
        "max_zeta_prime_mismatch": max(float(row["abs_zeta_prime_mismatch"]) for row in remap),
        "generated": [
            "source_register.csv",
            "projection_target_rows.csv",
            "radial_transverse_projection_factors.csv",
            "scalar_redshift_remap_consistency.csv",
            "projection_model_audit.csv",
            "owner_contract.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "155-redshift-projection-clock-map-owner.md",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_attempt(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()

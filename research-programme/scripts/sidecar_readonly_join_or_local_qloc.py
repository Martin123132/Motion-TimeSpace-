#!/usr/bin/env python3
"""Checkpoint 218: choose local q_loc proxy before read-only galaxy join."""

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

CHECKPOINT_218_NAME = "sidecar-readonly-join-contract-or-local-qloc"
CHECKPOINT_217_RUN = RUNS_ROOT / "20260601-000034-load-morphology-sidecar-builder-dryrun"
CHECKPOINT_216_RUN = RUNS_ROOT / "20260601-000033-load-morphology-sidecar-galaxy-test-plan"
CHECKPOINT_212_RUN = RUNS_ROOT / "20260601-000029-composite-GK-local-BAO-galaxy-safety-gate"

STATUS = "local_qloc_proxy_chosen_compact_shells_pass_magnitude_gate_PPN_not_derived"
CLAIM_CEILING = "qloc_proxy_only_no_local_GR_or_galaxy_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

H0_KM_S_MPC = 67.50994528839665
LIGHT_SPEED_KM_S = 299_792.458
HUBBLE_RADIUS_MPC = LIGHT_SPEED_KM_S / H0_KM_S_MPC
OMEGA_MEM0 = 0.6957274800599553
LOCKED_B_MEM = 2.0 / 27.0
Q_R_LIKE_GATE = 2.3e-5

G_NEWTON = 6.67430e-11
LIGHT_SPEED_M_S = 299_792_458.0
MPC_M = 3.0856775814913673e22
KPC_M = MPC_M / 1000.0
AU_M = 149_597_870_700.0
M_SUN_KG = 1.98847e30
M_EARTH_KG = 5.9722e24
R_EARTH_M = 6_371_000.0
R_SUN_M = 695_700_000.0
R_MERCURY_ORBIT_M = 57_909_000_000.0
R_GPS_ORBIT_M = 26_560_000.0


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
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 218 q_loc fork script"),
        (WORK_DIR / "217-load-morphology-sidecar-builder-dryrun.md", "sidecar builder dry-run checkpoint"),
        (CHECKPOINT_217_RUN / "status.json", "checkpoint 217 machine status"),
        (CHECKPOINT_217_RUN / "results" / "sidecar_dryrun_output.csv", "checkpoint 217 dry-run sidecar output"),
        (WORK_DIR / "216-load-morphology-sidecar-galaxy-test-plan.md", "sidecar plan checkpoint"),
        (CHECKPOINT_216_RUN / "results" / "no_fit_policy.csv", "checkpoint 216 no-fit policy"),
        (WORK_DIR / "212-composite-GK-local-BAO-galaxy-safety-gate.md", "fixed G_K local/BAO/galaxy safety gate"),
        (CHECKPOINT_212_RUN / "results" / "fixed_closure_arena_readout.csv", "checkpoint 212 local G_K readout"),
        (WORK_DIR / "179-local-GR-PPN-silence-contract.md", "local PPN silence contract"),
        (WORK_DIR / "205-C-silence-source-bound-for-BAO-and-local-rulers.md", "local/BAO C-silence bounds"),
    ]
    rows: list[dict[str, Any]] = []
    for path, role in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": role,
                "issue": "" if exists else "missing",
            }
        )
    return rows


def fork_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "fork": "read_only_galaxy_join",
            "value": "needed for empirical galaxy discipline",
            "risk": "touches galaxy-adjacent workflow before local q_loc blocker is narrowed",
            "decision": "defer",
            "reason": "theory-critical local GR gate is higher priority",
        },
        {
            "fork": "compact_shell_q_loc_proxy",
            "value": "directly attacks P08 local GR / q_loc open row",
            "risk": "only a proxy, not a parent derivation",
            "decision": "choose_now",
            "reason": "moves the unified-field branch toward derived/local-GR discipline",
        },
    ]


def compact_shell_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "case": "solar_1AU_shell",
            "central_mass_kg": M_SUN_KG,
            "test_radius_m": AU_M,
            "source_radius_m": R_SUN_M,
            "sidecar_class": "compact_vacuum_shell",
            "sidecar_basis": "checkpoint217 toy_solar_1AU_shell",
            "use_in_gate": "yes",
        },
        {
            "case": "solar_Mercury_shell",
            "central_mass_kg": M_SUN_KG,
            "test_radius_m": R_MERCURY_ORBIT_M,
            "source_radius_m": R_SUN_M,
            "sidecar_class": "compact_vacuum_shell",
            "sidecar_basis": "checkpoint214 solar_Mercury_shell proxy",
            "use_in_gate": "yes",
        },
        {
            "case": "earth_GPS_shell",
            "central_mass_kg": M_EARTH_KG,
            "test_radius_m": R_GPS_ORBIT_M,
            "source_radius_m": R_EARTH_M,
            "sidecar_class": "compact_vacuum_shell",
            "sidecar_basis": "checkpoint217 toy_earth_GPS_shell",
            "use_in_gate": "yes",
        },
        {
            "case": "earth_surface_stress",
            "central_mass_kg": M_EARTH_KG,
            "test_radius_m": R_EARTH_M,
            "source_radius_m": R_EARTH_M,
            "sidecar_class": "surface_stress_not_vacuum_shell",
            "sidecar_basis": "checkpoint210/212 Earth-surface Weyl stress proxy",
            "use_in_gate": "stress_only",
        },
    ]


def weyl_gk_per_mpc(mass_kg: float, radius_m: float) -> float:
    sqrt_c2_m2 = math.sqrt(48.0) * G_NEWTON * mass_kg / (LIGHT_SPEED_M_S**2 * radius_m**3)
    return math.sqrt(sqrt_c2_m2) * MPC_M


def l_cg_mpc(g_k_per_mpc: float) -> float:
    return 1.0 / math.sqrt(HUBBLE_RADIUS_MPC ** -2 + g_k_per_mpc * g_k_per_mpc)


def local_q_proxy_rows(manifest_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in manifest_rows:
        radius_m = float(row["test_radius_m"])
        radius_mpc = radius_m / MPC_M
        g_k = weyl_gk_per_mpc(float(row["central_mass_kg"]), radius_m)
        scale = l_cg_mpc(g_k)
        delta_c_linear = LOCKED_B_MEM * radius_mpc / scale
        q_gradient_proxy = 0.5 * delta_c_linear
        q_cosmological_proxy = OMEGA_MEM0 * (H0_KM_S_MPC * radius_mpc / LIGHT_SPEED_KM_S) ** 2
        q_total_proxy = q_gradient_proxy + q_cosmological_proxy
        rows.append(
            {
                **row,
                "test_radius_Mpc": radius_mpc,
                "G_K_Weyl_per_Mpc": g_k,
                "L_cg_Mpc": scale,
                "DeltaC_linear_proxy": delta_c_linear,
                "q_gradient_proxy_half_DeltaC": q_gradient_proxy,
                "q_cosmological_tidal_proxy": q_cosmological_proxy,
                "q_total_proxy": q_total_proxy,
                "q_R_like_gate": Q_R_LIKE_GATE,
                "ratio_to_gate": q_total_proxy / Q_R_LIKE_GATE,
                "passes_proxy_gate": "yes" if q_total_proxy < Q_R_LIKE_GATE else "no",
                "claim_status": "magnitude_proxy_only_no_PPN_promotion",
            }
        )
    return rows


def ppn_residual_vector_rows(q_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    compact_rows = [row for row in q_rows if row["use_in_gate"] == "yes"]
    worst = max(float(row["q_total_proxy"]) for row in compact_rows)
    worst_case = max(compact_rows, key=lambda row: float(row["q_total_proxy"]))["case"]
    return [
        {
            "residual": "q_R_like_proxy",
            "value_or_bound": worst,
            "case": worst_case,
            "status": "passes_magnitude_proxy",
            "promotion_meaning": "not killed by q_R-like magnitude gate",
        },
        {
            "residual": "gamma_minus_1",
            "value_or_bound": f"not derived; proxy scale <= {worst}",
            "case": worst_case,
            "status": "not_parent_derived",
            "promotion_meaning": "no PPN promotion",
        },
        {
            "residual": "beta_minus_1",
            "value_or_bound": "not derived",
            "case": "all",
            "status": "not_parent_derived",
            "promotion_meaning": "no PPN promotion",
        },
        {
            "residual": "Phi_minus_Psi",
            "value_or_bound": "not derived from compact-shell parent variation",
            "case": "all",
            "status": "not_parent_derived",
            "promotion_meaning": "no PPN promotion",
        },
        {
            "residual": "q_loc_nu",
            "value_or_bound": "source projection still missing",
            "case": "all",
            "status": "blocking",
            "promotion_meaning": "main local-GR theorem target remains open",
        },
    ]


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker": "q_loc_source_projection",
            "status": "missing",
            "why_it_matters": "magnitude proxy is not the same as deriving q_loc^nu -> 0",
            "next_action": "derive compact-shell source projection or write closure-only residual bound",
        },
        {
            "blocker": "PPN_metric_map",
            "status": "missing",
            "why_it_matters": "gamma and beta require a metric-level map, not only a scalar q proxy",
            "next_action": "connect q_R-like residual to metric potentials before any PPN claim",
        },
        {
            "blocker": "J_rel_edge_owner",
            "status": "missing",
            "why_it_matters": "compact shell sidecar still uses closure-level edge silence",
            "next_action": "derive J_rel local trivial representative",
        },
        {
            "blocker": "read_only_galaxy_join",
            "status": "deferred",
            "why_it_matters": "future empirical pillar still needs fair sidecar split",
            "next_action": "return after q_loc proxy branch is pinned",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], q_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    compact_rows = [row for row in q_rows if row["use_in_gate"] == "yes"]
    proxy_failures = sum(row["passes_proxy_gate"] != "yes" for row in compact_rows)
    stress_failures = sum(row["passes_proxy_gate"] != "yes" for row in q_rows if row["use_in_gate"] == "stress_only")
    worst = max(float(row["q_total_proxy"]) for row in compact_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal q_loc proxy audit",
        },
        {
            "gate": "fork decision",
            "status": "pass",
            "evidence": "local q_loc proxy chosen before read-only galaxy join",
            "claim_allowed": "workflow decision",
        },
        {
            "gate": "compact shell sidecar available",
            "status": "pass",
            "evidence": "solar and Earth shells use compact_vacuum_shell sidecar class",
            "claim_allowed": "proxy input",
        },
        {
            "gate": "q_R-like magnitude proxy",
            "status": "pass" if proxy_failures == 0 else "fail",
            "evidence": f"compact_failures={proxy_failures}; worst_q={worst}; gate={Q_R_LIKE_GATE}",
            "claim_allowed": "not killed by magnitude proxy",
        },
        {
            "gate": "surface stress proxy",
            "status": "pass" if stress_failures == 0 else "fail",
            "evidence": f"stress_failures={stress_failures}",
            "claim_allowed": "stress diagnostic only",
        },
        {
            "gate": "PPN promotion",
            "status": "fail",
            "evidence": "gamma, beta, Phi-Psi, and q_loc^nu source projection not derived",
            "claim_allowed": "no",
        },
        {
            "gate": "real local observable run",
            "status": "not_run",
            "evidence": "no Mercury/Shapiro/Cassini likelihood or ephemeris fit run",
            "claim_allowed": "no local evidence claim",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The branch chooses local q_loc before a read-only galaxy join. Compact-shell sidecar cases pass a conservative q_R-like magnitude proxy using the fixed G_K/Weyl scale and half-DeltaC estimate, with the worst compact case still below the adopted gate. This is useful compatibility evidence for the closure, but gamma, beta, Phi-Psi, and q_loc^nu are not derived.",
            "main_gain": "compact-shell sidecar now feeds a quantitative local q_R-like magnitude proxy",
            "main_failure": "PPN metric map and q_loc source projection remain missing",
            "next_target": "219-compact-shell-q_loc-source-projection-attempt.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_218_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    fork_rows = fork_decision_rows()
    manifest_rows = compact_shell_manifest_rows()
    q_rows = local_q_proxy_rows(manifest_rows)
    ppn_rows = ppn_residual_vector_rows(q_rows)
    blockers = blocker_rows()
    gates = claim_gate_rows(source_rows, q_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "fork_decision.csv": (
            fork_rows,
            ["fork", "value", "risk", "decision", "reason"],
        ),
        "compact_shell_manifest.csv": (
            manifest_rows,
            ["case", "central_mass_kg", "test_radius_m", "source_radius_m", "sidecar_class", "sidecar_basis", "use_in_gate"],
        ),
        "local_q_proxy_readout.csv": (
            q_rows,
            [
                "case",
                "central_mass_kg",
                "test_radius_m",
                "source_radius_m",
                "sidecar_class",
                "sidecar_basis",
                "use_in_gate",
                "test_radius_Mpc",
                "G_K_Weyl_per_Mpc",
                "L_cg_Mpc",
                "DeltaC_linear_proxy",
                "q_gradient_proxy_half_DeltaC",
                "q_cosmological_tidal_proxy",
                "q_total_proxy",
                "q_R_like_gate",
                "ratio_to_gate",
                "passes_proxy_gate",
                "claim_status",
            ],
        ),
        "ppn_residual_vector.csv": (
            ppn_rows,
            ["residual", "value_or_bound", "case", "status", "promotion_meaning"],
        ),
        "blocker_ledger.csv": (
            blockers,
            ["blocker", "status", "why_it_matters", "next_action"],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            ["decision", "meaning", "main_gain", "main_failure", "next_target", "promotion_allowed", "claim_ceiling"],
        ),
    }
    for filename, (rows, fieldnames) in files.items():
        write_csv(results_dir / filename, rows, fieldnames)

    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    compact_rows = [row for row in q_rows if row["use_in_gate"] == "yes"]
    proxy_failures = sum(row["passes_proxy_gate"] != "yes" for row in compact_rows)
    worst_compact = max(float(row["q_total_proxy"]) for row in compact_rows)
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "fork_chosen": "compact_shell_q_loc_proxy",
        "compact_proxy_failures": proxy_failures,
        "worst_compact_q_total_proxy": worst_compact,
        "q_R_like_gate": Q_R_LIKE_GATE,
        "PPN_metric_map_derived": False,
        "q_loc_source_projection_derived": False,
        "read_only_galaxy_join_deferred": True,
        "promotion_allowed": False,
        "next_target": decision[0]["next_target"],
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(status_payload["status"] + "\n", encoding="utf-8")
    return status_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timestamp", default=None, help="Optional run timestamp prefix.")
    args = parser.parse_args()
    payload = run(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

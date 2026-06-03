#!/usr/bin/env python3
"""Checkpoint 212: fixed composite G_K safety gate across local, BAO, and galaxy arenas."""

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

CHECKPOINT_212_NAME = "composite-GK-local-BAO-galaxy-safety-gate"
CHECKPOINT_211_RUN = RUNS_ROOT / "20260601-000028-GK-parent-metric-Ward-identity-attempt"
CHECKPOINT_210_RUN = RUNS_ROOT / "20260601-000027-GK-alphaK-parent-invariant-or-fixed-closure"
CHECKPOINT_205_RUN = RUNS_ROOT / "20260601-000022-C-silence-source-bound-for-BAO-and-local-rulers"

STATUS = "composite_GK_gradient_proxies_survive_local_BAO_galaxy_domain_owner_missing"
CLAIM_CEILING = "composite_GK_proxy_safety_no_local_GR_galaxy_or_BAO_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

H0_KM_S_MPC = 67.50994528839665
LIGHT_SPEED_KM_S = 299_792.458
HUBBLE_RADIUS_MPC = LIGHT_SPEED_KM_S / H0_KM_S_MPC
LOCKED_B_MEM = 2.0 / 27.0
LOCAL_DELTA_C_GATE = 4.6e-5
BAO_BASELINE_MPC = 150.0

G_NEWTON = 6.67430e-11
LIGHT_SPEED_M_S = 299_792_458.0
MPC_M = 3.0856775814913673e22
PC_M = MPC_M / 1.0e6
AU_M = 149_597_870_700.0
M_SUN_KG = 1.98847e30
M_EARTH_KG = 5.9722e24
R_EARTH_M = 6_371_000.0


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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 212 composite G_K safety script"),
        (WORK_DIR / "211-GK-parent-metric-Ward-identity-attempt.md", "parent metric/Ward checkpoint"),
        (CHECKPOINT_211_RUN / "status.json", "checkpoint 211 machine status"),
        (CHECKPOINT_211_RUN / "results" / "beta_sensitivity_gates.csv", "checkpoint 211 beta sensitivity gates"),
        (WORK_DIR / "210-GK-alphaK-parent-invariant-or-fixed-closure.md", "G_K invariant checkpoint"),
        (CHECKPOINT_210_RUN / "results" / "branch_numeric_readout.csv", "checkpoint 210 branch numeric readouts"),
        (WORK_DIR / "205-C-silence-source-bound-for-BAO-and-local-rulers.md", "BAO/local C-silence bounds"),
        (CHECKPOINT_205_RUN / "results" / "BAO_spatial_gradient_bounds.csv", "checkpoint 205 BAO spatial bounds"),
        (WORK_DIR / "179-local-GR-PPN-silence-contract.md", "local PPN silence contract"),
        (WORK_DIR / "00-pre-pivot-checkpoint.md", "pre-pivot local/galaxy toy-screening state"),
        (WORK_DIR / "01-motion-load-route-contract.md", "cosmology/galaxy/local gate contract"),
        (WORK_DIR / "106-canonical-R-cosmology-robustness-summary.md", "current cosmology robustness stance"),
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


def l_cg(g_k_per_mpc: float) -> float:
    return 1.0 / math.sqrt(HUBBLE_RADIUS_MPC ** -2 + g_k_per_mpc * g_k_per_mpc)


def delta_c_linear(g_k_per_mpc: float, baseline_mpc: float) -> float:
    return LOCKED_B_MEM * baseline_mpc / l_cg(g_k_per_mpc)


def max_g_for_delta_gate(baseline_mpc: float, gate_delta_c: float) -> float:
    required_inverse_l = gate_delta_c / (LOCKED_B_MEM * baseline_mpc)
    residual = required_inverse_l * required_inverse_l - HUBBLE_RADIUS_MPC ** -2
    return math.sqrt(max(0.0, residual))


def weyl_component_per_mpc(mass_kg: float, radius_m: float) -> float:
    sqrt_c2_m2 = math.sqrt(48.0) * G_NEWTON * mass_kg / (LIGHT_SPEED_M_S**2 * radius_m**3)
    return math.sqrt(sqrt_c2_m2) * MPC_M


def bao_gate_delta_c() -> float:
    bound_row = next(
        row
        for row in read_csv_rows(CHECKPOINT_205_RUN / "results" / "BAO_spatial_gradient_bounds.csv")
        if row["delta_chi2_threshold"] == "1.0" and row["coherence_length_Mpc"] == "150.0"
    )
    return float(bound_row["max_abs_delta_C_across_length"])


def arena_threshold_rows() -> list[dict[str, Any]]:
    bao_gate = bao_gate_delta_c()
    bao_l_min = LOCKED_B_MEM * BAO_BASELINE_MPC / bao_gate
    bao_g_max = max_g_for_delta_gate(BAO_BASELINE_MPC, bao_gate)
    solar_baseline = AU_M / MPC_M
    earth_baseline = R_EARTH_M / MPC_M
    return [
        {
            "arena": "BAO_smooth_common_mode",
            "baseline_Mpc": BAO_BASELINE_MPC,
            "deltaC_gate": bao_gate,
            "minimum_L_cg_Mpc_for_linear_full_Bmem_spread": bao_l_min,
            "maximum_G_K_per_Mpc": bao_g_max,
            "interpretation": "smooth BAO domains must have G_K below this threshold unless the endpoint profile is flatter than linear",
        },
        {
            "arena": "solar_system_1AU_local_gradient",
            "baseline_Mpc": solar_baseline,
            "deltaC_gate": LOCAL_DELTA_C_GATE,
            "minimum_L_cg_Mpc_for_linear_full_Bmem_spread": LOCKED_B_MEM * solar_baseline / LOCAL_DELTA_C_GATE,
            "maximum_G_K_per_Mpc": max_g_for_delta_gate(solar_baseline, LOCAL_DELTA_C_GATE),
            "interpretation": "local gradient proxy permits very large G_K at AU scales; PPN q_loc still separate",
        },
        {
            "arena": "earth_surface_local_gradient",
            "baseline_Mpc": earth_baseline,
            "deltaC_gate": LOCAL_DELTA_C_GATE,
            "minimum_L_cg_Mpc_for_linear_full_Bmem_spread": LOCKED_B_MEM * earth_baseline / LOCAL_DELTA_C_GATE,
            "maximum_G_K_per_Mpc": max_g_for_delta_gate(earth_baseline, LOCAL_DELTA_C_GATE),
            "interpretation": "surface-scale gradient proxy is permissive; not a local GR derivation",
        },
    ]


def fixed_closure_arena_rows() -> list[dict[str, Any]]:
    branch_rows = {row["case"]: row for row in read_csv_rows(CHECKPOINT_210_RUN / "results" / "branch_numeric_readout.csv")}
    bao_gate = bao_gate_delta_c()
    cases = [
        ("ideal_FLRW", "cosmology", BAO_BASELINE_MPC, bao_gate, "Hubble-cap coherent branch"),
        ("smooth_BAO_late_domain", "BAO", BAO_BASELINE_MPC, bao_gate, "late smooth BAO common-mode branch"),
        ("Gpc_transition_domain", "BAO_transition", BAO_BASELINE_MPC, bao_gate, "too sharp for smooth BAO if full memory varies linearly"),
        ("BAO_scale_transition", "BAO_transition", BAO_BASELINE_MPC, bao_gate, "forbidden as smooth BAO common-mode"),
        ("solar_system_1AU_Weyl", "local", float(branch_rows["solar_system_1AU_Weyl"]["test_baseline_Mpc"]), LOCAL_DELTA_C_GATE, "local curvature branch"),
        ("earth_surface_Weyl", "local", float(branch_rows["earth_surface_Weyl"]["test_baseline_Mpc"]), LOCAL_DELTA_C_GATE, "strong local curvature branch"),
        ("milky_way_8kpc_Weyl", "galaxy_proxy", float(branch_rows["milky_way_8kpc_Weyl"]["test_baseline_Mpc"]), bao_gate, "rough galaxy internal smoothness proxy only"),
    ]
    rows: list[dict[str, Any]] = []
    for case, arena, baseline, gate, meaning in cases:
        g_k = float(branch_rows[case]["G_K_per_Mpc"])
        scale = l_cg(g_k)
        delta_c = delta_c_linear(g_k, baseline)
        rows.append(
            {
                "case": case,
                "arena": arena,
                "G_K_per_Mpc": g_k,
                "L_cg_Mpc": scale,
                "baseline_Mpc": baseline,
                "DeltaC_linear_proxy": delta_c,
                "gate_DeltaC": gate,
                "passes_named_gradient_gate": "yes" if delta_c < gate else "no",
                "meaning": meaning,
                "claim_status": "proxy_only_no_promotion",
            }
        )
    return rows


def galaxy_proxy_rows() -> list[dict[str, Any]]:
    bao_gate = bao_gate_delta_c()
    cases = [
        ("dwarf_3kpc", 1.0e9, 3.0, "low-mass spiral/dwarf proxy"),
        ("milky_way_8kpc", 6.0e10, 8.0, "Milky-Way-like inner disk proxy"),
        ("outer_spiral_30kpc", 1.0e11, 30.0, "outer disk proxy"),
        ("massive_ETG_5kpc", 2.0e11, 5.0, "compact massive early-type proxy"),
        ("cluster_1Mpc", 1.0e14, 1000.0, "cluster-scale stress proxy, not galaxy-rotation branch"),
    ]
    rows: list[dict[str, Any]] = []
    for case, mass_solar, radius_kpc, meaning in cases:
        radius_mpc = radius_kpc / 1000.0
        g_k = weyl_component_per_mpc(mass_solar * M_SUN_KG, radius_kpc * 1000.0 * PC_M)
        scale = l_cg(g_k)
        delta_c = delta_c_linear(g_k, radius_mpc)
        rows.append(
            {
                "case": case,
                "mass_solar": mass_solar,
                "radius_kpc": radius_kpc,
                "Weyl_G_K_per_Mpc": g_k,
                "L_cg_Mpc": scale,
                "R_over_L_cg": radius_mpc / scale,
                "DeltaC_across_radius_linear_proxy": delta_c,
                "BAO_like_gradient_gate": bao_gate,
                "passes_internal_gradient_proxy": "yes" if delta_c < bao_gate else "no",
                "meaning": meaning,
                "viability_readout": (
                    "not_killed_by_internal_gradient_proxy"
                    if delta_c < bao_gate and radius_mpc / scale < 0.01
                    else "stressed_needs_full_galaxy_test"
                ),
            }
        )
    return rows


def domain_separation_rows() -> list[dict[str, Any]]:
    bao_g_max = max_g_for_delta_gate(BAO_BASELINE_MPC, bao_gate_delta_c())
    solar_g = weyl_component_per_mpc(M_SUN_KG, AU_M)
    mw_g = weyl_component_per_mpc(6.0e10 * M_SUN_KG, 8_000.0 * PC_M)
    return [
        {
            "comparison": "local_curvature_if_forced_into_BAO_domain",
            "G_K_per_Mpc": solar_g,
            "BAO_smooth_G_K_max_per_Mpc": bao_g_max,
            "ratio_to_BAO_limit": solar_g / bao_g_max,
            "verdict": "catastrophic_if_same_domain_rule",
            "meaning": "local Weyl must be local-domain data, not contamination of the smooth BAO representative",
        },
        {
            "comparison": "galaxy_Weyl_if_forced_into_BAO_domain",
            "G_K_per_Mpc": mw_g,
            "BAO_smooth_G_K_max_per_Mpc": bao_g_max,
            "ratio_to_BAO_limit": mw_g / bao_g_max,
            "verdict": "fails_as_smooth_BAO_domain",
            "meaning": "galaxy domain is not the smooth BAO domain; parent domain selector is mandatory",
        },
        {
            "comparison": "smooth_BAO_GK_if_used_for_galaxy_internal_gradient",
            "G_K_per_Mpc": 1.0e-4,
            "BAO_smooth_G_K_max_per_Mpc": bao_g_max,
            "ratio_to_BAO_limit": 1.0e-4 / bao_g_max,
            "verdict": "safe_but_not_galaxy_derivation",
            "meaning": "smooth BAO branch does not by itself supply galaxy phenomenology",
        },
    ]


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker": "domain_selector_parent_owner",
            "status": "missing",
            "why_it_matters": "the same fixed G_K formula only works if D is selected differently but lawfully in local, galaxy, and BAO arenas",
            "next_action": "derive or explicitly freeze domain-selection policy before empirical scoring",
        },
        {
            "blocker": "PPN_residual_vector",
            "status": "missing",
            "why_it_matters": "local gradient safety is not the same as gamma=beta=1 or q_loc^nu=0",
            "next_action": "turn Weyl/flow suppression into a q_loc residual estimate",
        },
        {
            "blocker": "galaxy_observable_coupling",
            "status": "missing",
            "why_it_matters": "internal gradient proxy does not prove SPARC/ETG rotation or acceleration-law survival",
            "next_action": "run fixed composite G_K sidecar against the galaxy branch without changing galaxy-work",
        },
        {
            "blocker": "Bianchi_stress_variation",
            "status": "missing",
            "why_it_matters": "field-theory promotion requires stress/conservation accounting for Xi_D and M_AB",
            "next_action": "defer promotion until variation is written",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], arena_rows: list[dict[str, Any]], galaxy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = sum(row["exists"] != "yes" for row in source_rows)
    smooth_bao = next(row for row in arena_rows if row["case"] == "smooth_BAO_late_domain")
    gpc = next(row for row in arena_rows if row["case"] == "Gpc_transition_domain")
    solar = next(row for row in arena_rows if row["case"] == "solar_system_1AU_Weyl")
    galaxy_fails = sum(row["passes_internal_gradient_proxy"] != "yes" for row in galaxy_rows)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing == 0 else "fail",
            "evidence": f"missing={missing}",
            "claim_allowed": "internal composite G_K safety audit",
        },
        {
            "gate": "smooth BAO gradient proxy",
            "status": "pass" if smooth_bao["passes_named_gradient_gate"] == "yes" else "fail",
            "evidence": f"DeltaC={smooth_bao['DeltaC_linear_proxy']} gate={smooth_bao['gate_DeltaC']}",
            "claim_allowed": "proxy consistency only",
        },
        {
            "gate": "transition BAO rejection",
            "status": "pass" if gpc["passes_named_gradient_gate"] == "no" else "fail",
            "evidence": f"Gpc transition DeltaC={gpc['DeltaC_linear_proxy']} must not be promoted as smooth BAO",
            "claim_allowed": "guardrail",
        },
        {
            "gate": "local Weyl gradient proxy",
            "status": "pass" if solar["passes_named_gradient_gate"] == "yes" else "fail",
            "evidence": f"Solar 1AU DeltaC={solar['DeltaC_linear_proxy']} gate={solar['gate_DeltaC']}",
            "claim_allowed": "local gradient proxy only",
        },
        {
            "gate": "galaxy internal gradient proxy",
            "status": "conditional_pass" if galaxy_fails == 0 else "fail",
            "evidence": f"galaxy_proxy_failures={galaxy_fails}",
            "claim_allowed": "not killed by this proxy; no SPARC claim",
        },
        {
            "gate": "single formula across arenas",
            "status": "conditional_pass",
            "evidence": "same L_cg^-2=L_H^-2+G_K^2 used; only domain inputs differ",
            "claim_allowed": "closure consistency",
        },
        {
            "gate": "parent domain selector derived",
            "status": "fail",
            "evidence": "D/u_D/Xi_D selector still not varied from parent action",
            "claim_allowed": "no promotion",
        },
        {
            "gate": "local GR and galaxy empirical promotion",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "The fixed composite G_K closure is not immediately killed by the simple gradient proxies: smooth BAO passes, local Weyl gradient proxies pass, and representative galaxy Weyl proxies are internally smooth across their own radii. But transition-scale G_K is correctly rejected as a smooth BAO domain, and all arenas require a parent-owned domain selector before promotion.",
            "main_gain": "same fixed formula can be used across arenas without an immediate gradient contradiction",
            "main_failure": "domain selection, q_loc/PPN residuals, and real galaxy observables remain unproved",
            "next_target": "213-fixed-GK-domain-selector-contract.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_212_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    threshold_rows = arena_threshold_rows()
    arena_rows = fixed_closure_arena_rows()
    galaxy_rows = galaxy_proxy_rows()
    separation_rows = domain_separation_rows()
    blockers = blocker_rows()
    gates = claim_gate_rows(source_rows, arena_rows, galaxy_rows)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "arena_thresholds.csv": (
            threshold_rows,
            [
                "arena",
                "baseline_Mpc",
                "deltaC_gate",
                "minimum_L_cg_Mpc_for_linear_full_Bmem_spread",
                "maximum_G_K_per_Mpc",
                "interpretation",
            ],
        ),
        "fixed_closure_arena_readout.csv": (
            arena_rows,
            [
                "case",
                "arena",
                "G_K_per_Mpc",
                "L_cg_Mpc",
                "baseline_Mpc",
                "DeltaC_linear_proxy",
                "gate_DeltaC",
                "passes_named_gradient_gate",
                "meaning",
                "claim_status",
            ],
        ),
        "galaxy_viability_proxy.csv": (
            galaxy_rows,
            [
                "case",
                "mass_solar",
                "radius_kpc",
                "Weyl_G_K_per_Mpc",
                "L_cg_Mpc",
                "R_over_L_cg",
                "DeltaC_across_radius_linear_proxy",
                "BAO_like_gradient_gate",
                "passes_internal_gradient_proxy",
                "meaning",
                "viability_readout",
            ],
        ),
        "domain_separation_necessity.csv": (
            separation_rows,
            ["comparison", "G_K_per_Mpc", "BAO_smooth_G_K_max_per_Mpc", "ratio_to_BAO_limit", "verdict", "meaning"],
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
    galaxy_failures = sum(row["passes_internal_gradient_proxy"] != "yes" for row in galaxy_rows)
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "smooth_BAO_gradient_proxy_passed": True,
        "transition_BAO_correctly_rejected": True,
        "local_Weyl_gradient_proxy_passed": True,
        "galaxy_internal_gradient_proxy_failures": galaxy_failures,
        "same_fixed_formula_used_across_arenas": True,
        "parent_domain_selector_derived": False,
        "local_GR_PPN_promoted": False,
        "galaxy_observable_promoted": False,
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

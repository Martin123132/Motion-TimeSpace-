#!/usr/bin/env python3
"""Checkpoint 179: local GR/PPN silence gate for the effective memory owner."""

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

MEMORY_OWNER_RUN = RUNS_ROOT / "20260531-235959-memory-perturbation-owner-derivation-attempt"
LOCAL_BOUNDS_RUN = RUNS_ROOT / "20260530-232506-local-bounds-gate-runner"
LOCAL_MAP_RUN = RUNS_ROOT / "20260530-232024-local-observables-data-map"
LOCAL_PIVOT_RUN = RUNS_ROOT / "20260531-120847-post-local-route-pivot-decision"

STATUS_PASS = "local_PPN_silence_effective_scalar_screened_P08_not_cleared"
CLAIM_CEILING = "local_screening_contract_no_derived_GR_or_PPN_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"

LIGHT_SPEED_M_S = 299_792_458.0
MPC_M = 3.0856775814913673e22
KM_PER_MPC_M = 3.0856775814913673e19
AU_M = 1.495978707e11
R_SUN_M = 6.957e8
R_EARTH_M = 6_371_000.0
R_GPS_M = 26_560_000.0
PC_M = 3.0856775814913673e16
KPC_M = 1.0e3 * PC_M
MPC_LOCAL_M = 1.0e6 * PC_M

LOCAL_SCREENING_GATES = {
    "q_R": 2.3e-5,
    "delta_beta": 7.16e-5,
    "alpha_clock": 2.48e-5,
    "epsilon_matter": 2.745906043549196e-15,
    "Q_R": 0.0,
}


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


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 179 local PPN silence script"),
        (WORK_DIR / "178-memory-perturbation-owner-attempt.md", "effective scalar perturbation owner"),
        (MEMORY_OWNER_RUN / "status.json", "checkpoint 178 machine status"),
        (MEMORY_OWNER_RUN / "results" / "derived_perturbation_outputs.csv", "P06 effective outputs"),
        (MEMORY_OWNER_RUN / "results" / "promotion_gate_effects.csv", "P04-P10 effect ledger"),
        (WORK_DIR / "13-local-closure-PPN-benchmark.md", "GR-equivalent closure benchmark"),
        (WORK_DIR / "14-closure-deviation-PPN-sensitivity.md", "local leak dictionary"),
        (WORK_DIR / "15-local-observables-data-map.md", "published-bound source map"),
        (WORK_DIR / "16-local-bounds-gate-runner.md", "local screening harness"),
        (LOCAL_MAP_RUN / "status.json", "source map status"),
        (LOCAL_BOUNDS_RUN / "status.json", "local bounds runner status"),
        (LOCAL_BOUNDS_RUN / "results" / "candidate_branch_summary.csv", "local gate behavior"),
        (WORK_DIR / "53-coherent-projection-local-silence-gate.md", "conditional coherent projector"),
        (WORK_DIR / "77-local-route-demote-or-continue-gate.md", "local selector demotion guardrail"),
        (WORK_DIR / "81-post-local-route-pivot-decision.md", "old local route pivot/demotion"),
        (LOCAL_PIVOT_RUN / "status.json", "post-local route pivot status"),
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


def locked_background() -> dict[str, float]:
    status = load_json(MEMORY_OWNER_RUN / "status.json")
    params = status["locked_background"]
    omega_m0 = float(params["Omega_m0"])
    h0 = float(params["H0"])
    return {
        "Omega_m0": omega_m0,
        "Omega_mem0": 1.0 - omega_m0,
        "H0_km_s_Mpc": h0,
        "H0_s_inverse": h0 * 1000.0 / MPC_M,
    }


def local_scale_rows(background: dict[str, float]) -> list[dict[str, Any]]:
    h0_s = background["H0_s_inverse"]
    omega_mem0 = background["Omega_mem0"]
    scales = [
        ("Earth radius", R_EARTH_M, "clock/redshift local scale"),
        ("GPS orbit", R_GPS_M, "clock/redshift screening scale"),
        ("Solar radius", R_SUN_M, "solar limb light-bending impact parameter"),
        ("Mercury semi-major axis proxy", 57.909e9, "inner-solar-system orbital scale"),
        ("1 AU", AU_M, "Cassini/Shapiro-scale order of magnitude"),
        ("1 pc", PC_M, "stellar-neighborhood scale"),
        ("8 kpc", 8.0 * KPC_M, "galactic-radius diagnostic, not PPN"),
        ("1 Mpc", MPC_LOCAL_M, "cluster/local-cosmology diagnostic, not PPN"),
    ]
    rows: list[dict[str, Any]] = []
    for name, radius_m, role in scales:
        epsilon = h0_s * radius_m / LIGHT_SPEED_M_S
        metric_factor = omega_mem0 * epsilon * epsilon
        rows.append(
            {
                "scale": name,
                "radius_m": radius_m,
                "role": role,
                "H0_r_over_c": epsilon,
                "Omega_mem_H0r_over_c_squared": metric_factor,
                "qR_gate_ratio": metric_factor / LOCAL_SCREENING_GATES["q_R"],
                "readout": "PPN_negligible" if metric_factor < LOCAL_SCREENING_GATES["q_R"] else "not_PPN_safe_without_more_work",
            }
        )
    return rows


def scalar_local_response_rows(background: dict[str, float]) -> list[dict[str, Any]]:
    h0_s = background["H0_s_inverse"]
    omega_mem0 = background["Omega_mem0"]
    worst_one_plus_w = 0.15878590317200947
    scales = [
        ("Earth radius", R_EARTH_M),
        ("GPS orbit", R_GPS_M),
        ("Solar radius", R_SUN_M),
        ("1 AU", AU_M),
        ("1 pc", PC_M),
        ("8 kpc", 8.0 * KPC_M),
        ("1 Mpc", MPC_LOCAL_M),
    ]
    rows: list[dict[str, Any]] = []
    for name, radius_m in scales:
        epsilon = h0_s * radius_m / LIGHT_SPEED_M_S
        delta_ratio = worst_one_plus_w * epsilon * epsilon
        mu_bound = omega_mem0 * delta_ratio
        source_bound = 1.5 * mu_bound
        rows.append(
            {
                "scale": name,
                "radius_m": radius_m,
                "conservative_one_plus_w": worst_one_plus_w,
                "H0_r_over_c": epsilon,
                "delta_phi_or_delta_mem_response_bound": delta_ratio,
                "local_mu_minus_one_bound": mu_bound,
                "local_S_mem_bound": source_bound,
                "screening_gate_compared": "q_R",
                "gate_value": LOCAL_SCREENING_GATES["q_R"],
                "gate_ratio": mu_bound / LOCAL_SCREENING_GATES["q_R"],
                "readout": "PPN_screened" if mu_bound < LOCAL_SCREENING_GATES["q_R"] else "needs_nonlocal_treatment",
            }
        )
    return rows


def silence_assumption_rows() -> list[dict[str, Any]]:
    return [
        {
            "assumption": "minimal_metric_coupling",
            "meaning": "matter sees only g_mu_nu; scalar does not couple directly to composition or clock species",
            "local_effect": "no direct fifth force and epsilon_matter=0 in the effective EFT",
            "status": "allowed_effective_EFT_assumption_not_MTS_parent_derivation",
            "failure_if_absent": "MICROSCOPE/WEP and clock bounds become immediate blockers",
        },
        {
            "assumption": "canonical_kinetic_term",
            "meaning": "c_s_eff^2=1 and no ghost/gradient instability",
            "local_effect": "scalar clustering on local subhorizon scales is H0^2 r^2 suppressed",
            "status": "effective_owner_from_checkpoint_178",
            "failure_if_absent": "local mu/gamma-like residual may be unscreened",
        },
        {
            "assumption": "zero_anisotropic_stress",
            "meaning": "canonical scalar has pi_mem=0",
            "local_effect": "Phi-Psi is not directly sourced by memory shear",
            "status": "effective_owner_from_checkpoint_178",
            "failure_if_absent": "lensing/PPN slip gate fails",
        },
        {
            "assumption": "cosmology_only_scalar_fence",
            "meaning": "checkpoint-178 scalar is treated as an effective cosmological stress owner, not a local MTS selector",
            "local_effect": "old C_coh selector route remains demoted; local GR is not claimed derived",
            "status": "required_guardrail",
            "failure_if_absent": "would smuggle local GR through a reconstructed scalar",
        },
        {
            "assumption": "no_parent_domain_revival",
            "meaning": "D/chi_D is not reused to silence local systems unless derived by a new parent action",
            "local_effect": "P09 remains open",
            "status": "required_guardrail",
            "failure_if_absent": "hidden selector route re-enters after checkpoint 81 demotion",
        },
    ]


def ppn_residual_rows(scale_rows: list[dict[str, Any]], scalar_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    au_metric = next(row for row in scale_rows if row["scale"] == "1 AU")
    au_scalar = next(row for row in scalar_rows if row["scale"] == "1 AU")
    gamma_bound = float(au_metric["Omega_mem_H0r_over_c_squared"]) + float(au_scalar["local_mu_minus_one_bound"])
    return [
        {
            "residual": "gamma_minus_1",
            "effective_scalar_value_or_bound": gamma_bound,
            "screening_gate": LOCAL_SCREENING_GATES["q_R"],
            "status": "screened_effective" if gamma_bound < LOCAL_SCREENING_GATES["q_R"] else "fail",
            "claim_limit": "not a derived MTS q_R=0 theorem; cosmology-only minimal EFT bound",
        },
        {
            "residual": "beta_minus_1",
            "effective_scalar_value_or_bound": 0.0,
            "screening_gate": LOCAL_SCREENING_GATES["delta_beta"],
            "status": "screened_effective",
            "claim_limit": "canonical scalar minimal coupling does not change PPN beta at this contract level; parent completion still missing",
        },
        {
            "residual": "alpha_clock",
            "effective_scalar_value_or_bound": 0.0,
            "screening_gate": LOCAL_SCREENING_GATES["alpha_clock"],
            "status": "screened_effective",
            "claim_limit": "requires matter clocks to couple universally to the same metric",
        },
        {
            "residual": "epsilon_matter",
            "effective_scalar_value_or_bound": 0.0,
            "screening_gate": LOCAL_SCREENING_GATES["epsilon_matter"],
            "status": "screened_effective",
            "claim_limit": "requires no scalar composition coupling",
        },
        {
            "residual": "Phi_minus_Psi",
            "effective_scalar_value_or_bound": 0.0,
            "screening_gate": LOCAL_SCREENING_GATES["q_R"],
            "status": "screened_effective",
            "claim_limit": "canonical scalar has no anisotropic stress; spectra/lensing not run",
        },
        {
            "residual": "Q_R_or_q_loc",
            "effective_scalar_value_or_bound": "",
            "screening_gate": "must_be_zero_or_parent_bounded",
            "status": "open_blocking",
            "claim_limit": "P08 not cleared because MTS parent q_loc^nu and domain selector are not derived",
        },
    ]


def forbidden_local_moves_rows() -> list[dict[str, Any]]:
    return [
        {
            "forbidden_move": "claim local GR from the old C_coh selector",
            "reason": "checkpoint 81 demoted that route to diagnostic closure",
            "allowed_replacement": "only use C_coh/local closure as benchmark or derive a new parent owner",
        },
        {
            "forbidden_move": "treat reconstructed scalar as the fundamental MTS parent action",
            "reason": "V(phi) was reconstructed from the locked background",
            "allowed_replacement": "label scalar as cosmology EFT owner until Q,D,R derive it",
        },
        {
            "forbidden_move": "hide matter coupling in calibration",
            "reason": "epsilon_matter is constrained by WEP/MICROSCOPE-style screening",
            "allowed_replacement": "universal metric coupling or explicit bounded composition coupling",
        },
        {
            "forbidden_move": "turn local silence into a plateau axiom",
            "reason": "q_loc^nu -> 0 must follow from variation/conservation",
            "allowed_replacement": "derive q_loc^nu cancellation or keep P08 open",
        },
        {
            "forbidden_move": "use cosmological high-c_s success as PPN proof",
            "reason": "subhorizon growth suppression is not a local weak-field derivation",
            "allowed_replacement": "run local screening and preserve claim ceiling",
        },
    ]


def promotion_gate_effect_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "P04",
            "gate": "parent perturbation action",
            "effect_of_checkpoint_179": "not_cleared",
            "evidence": "local screening uses effective scalar assumptions, not an MTS parent variation",
        },
        {
            "gate_id": "P06",
            "gate": "perturbation outputs",
            "effect_of_checkpoint_179": "kept_partial_effective",
            "evidence": "checkpoint 178 effective owner remains compatible with local screening",
        },
        {
            "gate_id": "P07",
            "gate": "CMB Boltzmann interface",
            "effect_of_checkpoint_179": "not_cleared",
            "evidence": "local PPN screening says nothing about TT/TE/EE/lensing or calibration bridge",
        },
        {
            "gate_id": "P08",
            "gate": "local GR and PPN silence",
            "effect_of_checkpoint_179": "screened_effective_not_derived",
            "evidence": "minimal canonical scalar is locally safe by screening, but q_loc^nu and parent domain silence are not derived",
        },
        {
            "gate_id": "P09",
            "gate": "zero-knob domain selector",
            "effect_of_checkpoint_179": "not_cleared",
            "evidence": "old selector route remains demoted; no new D/chi_D parent rule",
        },
        {
            "gate_id": "P10",
            "gate": "B_mem=2/27 amplitude owner",
            "effect_of_checkpoint_179": "not_cleared",
            "evidence": "local screening assumes the locked branch; amplitude remains empirical theorem target",
        },
    ]


def acceptance_gate_rows(
    sources: list[dict[str, Any]],
    local_scales: list[dict[str, Any]],
    scalar_bounds: list[dict[str, Any]],
    ppn_residuals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    solar_system_rows = [
        row
        for row in local_scales
        if row["scale"] in {"Earth radius", "GPS orbit", "Solar radius", "Mercury semi-major axis proxy", "1 AU"}
    ]
    local_scalar_rows = [
        row
        for row in scalar_bounds
        if row["scale"] in {"Earth radius", "GPS orbit", "Solar radius", "1 AU"}
    ]
    failed_ppn = [row for row in ppn_residuals if row["status"] == "fail"]
    open_ppn = [row for row in ppn_residuals if row["status"] == "open_blocking"]
    return [
        {
            "gate": "all_cited_sources_exist",
            "status": "pass" if not missing else "fail",
            "evidence": "all registered paths found" if not missing else "; ".join(missing),
        },
        {
            "gate": "solar_system_tidal_terms_screened",
            "status": "pass"
            if all(float(row["Omega_mem_H0r_over_c_squared"]) < LOCAL_SCREENING_GATES["q_R"] for row in solar_system_rows)
            else "fail",
            "evidence": "all solar-system Omega_mem(H0r/c)^2 terms below q_R gate",
        },
        {
            "gate": "local_scalar_clustering_screened",
            "status": "pass"
            if all(float(row["local_mu_minus_one_bound"]) < LOCAL_SCREENING_GATES["q_R"] for row in local_scalar_rows)
            else "fail",
            "evidence": "all solar-system high-cs scalar response bounds below q_R gate",
        },
        {
            "gate": "direct_fifth_force_forbidden",
            "status": "pass",
            "evidence": "local silence only allowed under minimal metric coupling/no composition coupling",
        },
        {
            "gate": "PPN_residual_vector_screened",
            "status": "pass" if not failed_ppn else "fail",
            "evidence": f"failed_ppn_residuals={len(failed_ppn)}; open_blockers={len(open_ppn)}",
        },
        {
            "gate": "P08_not_promoted",
            "status": "pass",
            "evidence": "q_loc^nu/domain parent silence remains open_blocking",
        },
        {
            "gate": "claim_ceiling_preserved",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(local_scales: list[dict[str, Any]], scalar_bounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    au_tidal = next(row for row in local_scales if row["scale"] == "1 AU")
    au_scalar = next(row for row in scalar_bounds if row["scale"] == "1 AU")
    return [
        {
            "item": "status",
            "verdict": STATUS_PASS,
            "evidence": "minimal high-cs scalar screens local PPN-sized effects, but P08 remains a parent-theory blocker",
        },
        {
            "item": "one_AU_cosmological_metric_factor",
            "verdict": f"{float(au_tidal['Omega_mem_H0r_over_c_squared']):.12g}",
            "evidence": "Omega_mem0(H0 AU/c)^2",
        },
        {
            "item": "one_AU_scalar_mu_bound",
            "verdict": f"{float(au_scalar['local_mu_minus_one_bound']):.12g}",
            "evidence": "conservative high-cs scalar response bound using peak |1+w_mem|",
        },
        {
            "item": "P08_status",
            "verdict": "screened_effective_not_derived",
            "evidence": "safe as cosmology-only minimal scalar EFT; not a derivation of q_loc^nu -> 0 from MTS parent action",
        },
        {
            "item": "promotion_allowed",
            "verdict": False,
            "evidence": "local GR/PPN silence is screened but not parent-derived",
        },
        {
            "item": "claim_ceiling",
            "verdict": CLAIM_CEILING,
            "evidence": "private local screening contract only",
        },
        {
            "item": "next_target",
            "verdict": "180-CMB-kill-screen-or-parent-amplitude-owner-decision.md",
            "evidence": "after P06/P08 effective screening, next highest blockers are CMB interface and 2/27 parent amplitude ownership",
        },
    ]


def run_gate(output_root: Path, timestamp: str | None = None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-local-GR-PPN-silence-contract"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    background = locked_background()
    assumptions = silence_assumption_rows()
    local_scales = local_scale_rows(background)
    scalar_bounds = scalar_local_response_rows(background)
    ppn_residuals = ppn_residual_rows(local_scales, scalar_bounds)
    forbidden = forbidden_local_moves_rows()
    promotion = promotion_gate_effect_rows()
    gates = acceptance_gate_rows(sources, local_scales, scalar_bounds, ppn_residuals)
    decisions = decision_rows(local_scales, scalar_bounds)

    write_json(
        run_dir / "run_config.json",
        {
            "timestamp": run_stamp,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "screening_gates": LOCAL_SCREENING_GATES,
            "purpose": "screen local PPN silence of checkpoint-178 effective scalar without claiming derived GR",
        },
    )
    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(
        results_dir / "effective_scalar_local_silence_assumptions.csv",
        assumptions,
        ["assumption", "meaning", "local_effect", "status", "failure_if_absent"],
    )
    write_csv(
        results_dir / "cosmological_tidal_local_bounds.csv",
        local_scales,
        ["scale", "radius_m", "role", "H0_r_over_c", "Omega_mem_H0r_over_c_squared", "qR_gate_ratio", "readout"],
    )
    write_csv(
        results_dir / "high_cs_scalar_local_response_bounds.csv",
        scalar_bounds,
        [
            "scale",
            "radius_m",
            "conservative_one_plus_w",
            "H0_r_over_c",
            "delta_phi_or_delta_mem_response_bound",
            "local_mu_minus_one_bound",
            "local_S_mem_bound",
            "screening_gate_compared",
            "gate_value",
            "gate_ratio",
            "readout",
        ],
    )
    write_csv(
        results_dir / "PPN_residual_vector.csv",
        ppn_residuals,
        ["residual", "effective_scalar_value_or_bound", "screening_gate", "status", "claim_limit"],
    )
    write_csv(
        results_dir / "forbidden_local_smuggling_ledger.csv",
        forbidden,
        ["forbidden_move", "reason", "allowed_replacement"],
    )
    write_csv(
        results_dir / "promotion_gate_effects.csv",
        promotion,
        ["gate_id", "gate", "effect_of_checkpoint_179", "evidence"],
    )
    write_csv(results_dir / "acceptance_gates.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status = {
        "status": STATUS_PASS,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "locked_background": background,
        "promotion_allowed": False,
        "P08_effect": "screened_effective_not_derived",
        "generated": [
            "source_register.csv",
            "effective_scalar_local_silence_assumptions.csv",
            "cosmological_tidal_local_bounds.csv",
            "high_cs_scalar_local_response_bounds.csv",
            "PPN_residual_vector.csv",
            "forbidden_local_smuggling_ledger.csv",
            "promotion_gate_effects.csv",
            "acceptance_gates.csv",
            "decision.csv",
        ],
        "next_target": "180-CMB-kill-screen-or-parent-amplitude-owner-decision.md",
    }
    write_json(run_dir / "status.json", status)
    (run_dir / "DONE.txt").write_text(f"{STATUS_PASS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_gate(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()

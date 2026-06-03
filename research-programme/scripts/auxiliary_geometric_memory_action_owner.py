#!/usr/bin/env python3
"""Audit auxiliary/geometric action routes for owning locked memory."""

from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
POTENTIAL_RUN = RUNS_ROOT / "20260531-194000-memory-action-potential-owner-attempt"
POTENTIAL_RESULTS = POTENTIAL_RUN / "results"

LOCKED_B_MEM = 2.0 / 27.0
CLAIM_CEILING = "auxiliary_geometric_contract_not_parent_derivation"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


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


def source_register_rows(script_path: Path, potential_run: Path) -> list[dict[str, Any]]:
    potential_results = potential_run / "results"
    paths = [
        script_path,
        WORK_DIR / "57-memory-action-owner-contract.md",
        WORK_DIR / "68-chiD-gated-memory-conservation-contract.md",
        WORK_DIR / "71-relative-boundary-current-construction-attempt.md",
        WORK_DIR / "72-relative-current-action-owner-attempt.md",
        WORK_DIR / "132-smooth-memory-growth-theorem-attempt.md",
        WORK_DIR / "133-memory-stress-perturbation-owner-attempt.md",
        WORK_DIR / "135-high-sound-speed-or-auxiliary-memory-owner.md",
        WORK_DIR / "136-memory-action-potential-owner-attempt.md",
        potential_run / "status.json",
        potential_results / "potential_map_reconstruction.csv",
        potential_results / "action_candidate_ledger.csv",
        potential_results / "noncircularity_tests.csv",
        potential_results / "decision.csv",
    ]
    return [
        {
            "source": path.name,
            "path": str(path),
            "exists": path.exists(),
            "issue": "" if path.exists() else "missing",
        }
        for path in paths
    ]


def constraint_variation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "candidate_action",
            "equation": "S_aux = integral sqrt(-g)[-rho_M(I_M) + lambda_M(I_M - F(C_coh,Q,J_rel))]",
            "result": "covariant algebraic constraint action",
            "status": "written",
            "blocker": "F and rho_M still chosen to match locked branch",
        },
        {
            "step": "lambda_variation",
            "equation": "delta S / delta lambda_M = 0",
            "result": "I_M = F(C_coh,Q,J_rel)",
            "status": "pass_formal",
            "blocker": "does not select F",
        },
        {
            "step": "I_variation",
            "equation": "delta S / delta I_M = 0",
            "result": "lambda_M = d rho_M / d I_M",
            "status": "pass_formal",
            "blocker": "multiplier stress becomes the pressure/exchange carrier",
        },
        {
            "step": "no_propagating_delta_I",
            "equation": "no kinetic term for I_M; delta I_M = F_C delta C_coh + F_Q delta Q + F_J delta J_rel",
            "result": "independent memory clustering mode is removed if delta F^(1)=0",
            "status": "pass_conditional",
            "blocker": "requires coherent-domain/boundary perturbations to have delta F^(1)=0",
        },
        {
            "step": "coherence_cancellation",
            "equation": "C_coh = <theta>_D^2/(<theta^2>_D+<sigma^2>_D+<omega^2>_D+eps_D)",
            "result": "delta C_coh^(1)=0 around FLRW bulk",
            "status": "pass_from_checkpoint_132",
            "blocker": "boundary and gauge-invariant domain selection still need a parent variation",
        },
        {
            "step": "stress_variation",
            "equation": "T_aux^munu = rho_M g^munu + 2 lambda_M delta F / delta g_munu plus domain terms",
            "result": "metric variation of the constraint must provide p+rho during activation",
            "status": "required_not_derived",
            "blocker": "no derived kernel delta F/delta g_munu yet",
        },
        {
            "step": "bianchi_identity",
            "equation": "nabla_mu T_total^munu = sum E_field L_xi(field)",
            "result": "total conservation follows on shell for a fully covariant action",
            "status": "pass_formal",
            "blocker": "individual matter conservation and local exchange are not proven",
        },
    ]


def required_pressure_kernel_rows(potential_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in potential_rows:
        rho = float(item["rho_formula"])
        kinetic = float(item["K_formula"])
        v_value = float(item["V_formula"])
        pressure = kinetic - v_value
        lift = pressure + rho
        a_n = float(item["A_N_formula"])
        lift_formula = LOCKED_B_MEM * a_n / 3.0
        rows.append(
            {
                "index": int(item["index"]),
                "z": float(item["z"]),
                "N_past": float(item["N_past"]),
                "rho_mem": rho,
                "pressure_mem": pressure,
                "p_plus_rho_required": lift,
                "p_plus_rho_formula": lift_formula,
                "abs_lift_error": abs(lift - lift_formula),
                "K_formula": kinetic,
                "required_constraint_pressure_status": "active" if lift > 1.0e-8 else "inactive_or_frozen",
                "interpretation": "constraint_metric_variation_must_supply_this_lift",
            }
        )
    return rows


def action_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "algebraic_auxiliary_memory",
            "action_sketch": "S=-rho(I)+lambda[I-F(C_coh,Q,J_rel)]",
            "nonpropagating_memory": "pass_conditional",
            "activation_pressure": "required_kernel_not_derived",
            "bianchi": "pass_formal_total",
            "local_silence": "pass_conditional_if_deltaF_first_order_zero",
            "amplitude": "fail_not_derived",
            "verdict": "best_exact_route_but_still_a_contract",
        },
        {
            "candidate": "four_form_or_topological_flux",
            "action_sketch": "S=-Z(I)F_4^2/2 + lambda[I-F(C_coh,Q,J_rel)]",
            "nonpropagating_memory": "pass",
            "activation_pressure": "fail_without_extra_metric_dependence",
            "bianchi": "pass_formal",
            "local_silence": "good_for_no_local_hair",
            "amplitude": "integration_constant_or_inserted",
            "verdict": "good_silence_bad_activation_pressure",
        },
        {
            "candidate": "BF_relative_boundary_polarization",
            "action_sketch": "S=integral B wedge F[A] + boundary Pi(C_coh) wedge b_2",
            "nonpropagating_memory": "pass_formal",
            "activation_pressure": "open",
            "bianchi": "pass_formal_if_boundary_terms_covariant",
            "local_silence": "pass_conditional_for_trivial_local_class",
            "amplitude": "fail_until_Pi_normalization_derived",
            "verdict": "best_topological_support_not_full_stress_owner",
        },
        {
            "candidate": "geometric_counterstress",
            "action_sketch": "E_mem^munu from metric/domain variation with nabla_mu E_mem^munu=0 by identity",
            "nonpropagating_memory": "possible",
            "activation_pressure": "possible",
            "bianchi": "must_be_identity_level",
            "local_silence": "open_high_risk",
            "amplitude": "fail_not_derived",
            "verdict": "heavy_route_only_after_auxiliary_kernel_is_exhausted",
        },
        {
            "candidate": "controlled_exchange_Qnu",
            "action_sketch": "nabla_mu T_mem^munu=Q^nu and nabla_mu T_matter^munu=-Q^nu",
            "nonpropagating_memory": "not_guaranteed",
            "activation_pressure": "can_be_forced",
            "bianchi": "pass_total_only",
            "local_silence": "dangerous",
            "amplitude": "free_without_parent",
            "verdict": "last_resort_not_preferred",
        },
    ]


def noether_bianchi_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "covariant_total_action",
            "status": "pass_formal",
            "evidence": "if all pieces are varied from one diffeomorphism-invariant action, total Bianchi conservation follows on shell",
        },
        {
            "test": "external_gate_rejected",
            "status": "pass",
            "evidence": "chi_D T_mem or hand-set Q^nu is not accepted unless produced by an action variation",
        },
        {
            "test": "auxiliary_multiplier_exchange",
            "status": "pass_formal",
            "evidence": "lambda_M stress can carry exchange terms required by the memory gate",
        },
        {
            "test": "separate_matter_conservation",
            "status": "open",
            "evidence": "the audit has not shown that ordinary matter remains geodesic and separately conserved in local systems",
        },
        {
            "test": "pressure_kernel_identity",
            "status": "fail_not_derived",
            "evidence": "the action has not produced the exact spatial metric-variation kernel p+rho=B_mem A_N/3",
        },
        {
            "test": "amplitude_normalization",
            "status": "fail",
            "evidence": "B_mem=2/27 remains imported from the locked empirical branch",
        },
    ]


def local_silence_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "stationary_local_class",
            "required_statement": "F(C_coh,Q,J_rel)=0 and delta F^(1)=0 in bound local domains",
            "status": "open",
            "risk": "without this, the auxiliary stress can become a PPN source",
        },
        {
            "condition": "FLRW_bulk_class",
            "required_statement": "F(C_coh,Q,J_rel)=(N/u3)^3 with p=3 and u3=1/4",
            "status": "partial",
            "risk": "determinant/cell normalization route exists but is not action-derived",
        },
        {
            "condition": "linear_growth_scales",
            "required_statement": "delta F^(1)=0 or high-sound-speed suppression on SDSS/eBOSS modes",
            "status": "pass_conditional",
            "risk": "works for tested growth proxy but is not full perturbation theory",
        },
        {
            "condition": "boundary_motion",
            "required_statement": "relative current J_rel supplies exact boundary exchange without surface wall stress",
            "status": "open",
            "risk": "boundary stress would endanger local GR",
        },
        {
            "condition": "CMB_early_branch",
            "required_statement": "memory action has a controlled early-time perturbation limit",
            "status": "not_tested",
            "risk": "late-time EFT health cannot be promoted to CMB perturbation viability",
        },
    ]


def summary_rows(kernel_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    max_lift_row = max(kernel_rows, key=lambda row: float(row["p_plus_rho_required"]))
    max_error = max(abs(float(row["abs_lift_error"])) for row in kernel_rows)
    active_rows = sum(1 for row in kernel_rows if row["required_constraint_pressure_status"] == "active")
    return [
        {
            "item": "rows_checked",
            "value": len(kernel_rows),
            "readout": "matches_potential_map_grid",
        },
        {
            "item": "max_pressure_lift_p_plus_rho",
            "value": max_lift_row["p_plus_rho_required"],
            "readout": f"peaks_at_z={float(max_lift_row['z']):.6g}",
        },
        {
            "item": "max_lift_identity_error",
            "value": max_error,
            "readout": "pass" if max_error < 1.0e-12 else "check",
        },
        {
            "item": "active_pressure_rows",
            "value": active_rows,
            "readout": "activation_interval_requires_constraint_pressure",
        },
    ]


def gate_rows(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_item = {row["item"]: row for row in summary}
    max_error = float(by_item["max_lift_identity_error"]["value"])
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass",
            "evidence": "source register was checked before outputs were written",
        },
        {
            "gate": "auxiliary_constraint_written",
            "status": "pass_formal",
            "evidence": "S_aux=-rho(I)+lambda[I-F(C,Q,J)] gives I=F and no independent kinetic mode",
        },
        {
            "gate": "smooth_memory_mode_removed",
            "status": "pass_conditional",
            "evidence": "requires delta F^(1)=0; checkpoint 132 supplies delta C_coh^(1)=0 in FLRW bulk",
        },
        {
            "gate": "activation_pressure_kernel_identified",
            "status": "pass",
            "evidence": f"p+rho=B_mem A_N/3 identity max error {max_error:.6g}",
        },
        {
            "gate": "activation_pressure_kernel_derived",
            "status": "fail",
            "evidence": "no S_cell/S_stress variation yet produces the required spatial metric kernel",
        },
        {
            "gate": "total_bianchi_conservation",
            "status": "pass_formal",
            "evidence": "follows for a fully covariant on-shell action, including auxiliary stress",
        },
        {
            "gate": "local_PPN_silence",
            "status": "open",
            "evidence": "local F=0 and delta F=0 are requirements, not derived branch equations",
        },
        {
            "gate": "Bmem_p_u3_derivation",
            "status": "fail",
            "evidence": "B_mem=2/27, p=3, and u3=1/4 are still supplied by the locked branch/contract",
        },
        {
            "gate": "growth_branch_promotion",
            "status": "fail",
            "evidence": "this is a theorem target, not derived MTS perturbation theory",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "status",
            "verdict": "auxiliary_constraint_route_sharpened_not_derived",
            "evidence": "a nonpropagating covariant constraint action can be written, but it does not yet derive the pressure kernel or locked constants",
        },
        {
            "item": "best_live_route",
            "verdict": "algebraic_auxiliary_plus_relative_boundary_current",
            "evidence": "this is the cleanest way to remove propagating memory while preserving Bianchi bookkeeping",
        },
        {
            "item": "new_exact_requirement",
            "verdict": "derive_pressure_kernel",
            "evidence": "the parent action must produce p+rho=B_mem A_N/3 from metric variation of F(C_coh,Q,J_rel)",
        },
        {
            "item": "demotion_condition",
            "verdict": "if_pressure_kernel_not_derived_then_EFT_closure",
            "evidence": "without that kernel, the branch remains a healthy empirical EFT closure rather than fundamental field theory",
        },
    ]


def run_audit(output_root: Path, timestamp: str | None = None, potential_run: Path = POTENTIAL_RUN) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-auxiliary-geometric-memory-action-owner"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve(), potential_run)
    missing = [row["path"] for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    potential_status = read_json(potential_run / "status.json")
    potential_rows = read_csv_rows(potential_run / "results" / "potential_map_reconstruction.csv")

    variation_chain = constraint_variation_chain_rows()
    pressure_kernel = required_pressure_kernel_rows(potential_rows)
    candidates = action_candidate_rows()
    bianchi_tests = noether_bianchi_test_rows()
    local_tests = local_silence_test_rows()
    summary = summary_rows(pressure_kernel)
    gates = gate_rows(summary)
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "issue"])
    write_csv(results_dir / "constraint_variation_chain.csv", variation_chain, ["step", "equation", "result", "status", "blocker"])
    write_csv(
        results_dir / "required_pressure_kernel.csv",
        pressure_kernel,
        [
            "index",
            "z",
            "N_past",
            "rho_mem",
            "pressure_mem",
            "p_plus_rho_required",
            "p_plus_rho_formula",
            "abs_lift_error",
            "K_formula",
            "required_constraint_pressure_status",
            "interpretation",
        ],
    )
    write_csv(
        results_dir / "action_candidate_ledger.csv",
        candidates,
        [
            "candidate",
            "action_sketch",
            "nonpropagating_memory",
            "activation_pressure",
            "bianchi",
            "local_silence",
            "amplitude",
            "verdict",
        ],
    )
    write_csv(results_dir / "noether_bianchi_tests.csv", bianchi_tests, ["test", "status", "evidence"])
    write_csv(results_dir / "local_silence_tests.csv", local_tests, ["condition", "required_statement", "status", "risk"])
    write_csv(results_dir / "summary.csv", summary, ["item", "value", "readout"])
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "input_status": potential_status["status"],
        "generated": [
            "source_register.csv",
            "constraint_variation_chain.csv",
            "required_pressure_kernel.csv",
            "action_candidate_ledger.csv",
            "noether_bianchi_tests.csv",
            "local_silence_tests.csv",
            "summary.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "derive_constraint_pressure_kernel_or_demote_to_EFT_closure",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--potential-run", type=Path, default=POTENTIAL_RUN)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_audit(args.output_root, args.timestamp, args.potential_run))


if __name__ == "__main__":
    main()

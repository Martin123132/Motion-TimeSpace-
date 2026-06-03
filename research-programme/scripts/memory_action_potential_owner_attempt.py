#!/usr/bin/env python3
"""Attempt to own the reconstructed memory potential with a non-circular action."""

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
PREVIOUS_RUN = RUNS_ROOT / "20260531-192900-high-sound-speed-or-auxiliary-memory-owner"
PREVIOUS_RESULTS = PREVIOUS_RUN / "results"
PREVIOUS_RECONSTRUCTION = PREVIOUS_RESULTS / "canonical_reconstruction.csv"
PREVIOUS_STATUS = PREVIOUS_RUN / "status.json"

LOCKED_B_MEM = 2.0 / 27.0
LOCKED_P = 3.0
LOCKED_U3 = 0.25
CLAIM_CEILING = "potential_map_reconstructed_not_parent_action"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def source_register_rows(script_path: Path, previous_run: Path) -> list[dict[str, Any]]:
    previous_results = previous_run / "results"
    paths = [
        script_path,
        WORK_DIR / "57-memory-action-owner-contract.md",
        WORK_DIR / "130-growth-route-gate.md",
        WORK_DIR / "131-growth-perturbation-contract.md",
        WORK_DIR / "132-smooth-memory-growth-theorem-attempt.md",
        WORK_DIR / "133-memory-stress-perturbation-owner-attempt.md",
        WORK_DIR / "134-subhorizon-suppressed-growth-correction-gate.md",
        WORK_DIR / "135-high-sound-speed-or-auxiliary-memory-owner.md",
        previous_run / "status.json",
        previous_results / "canonical_reconstruction.csv",
        previous_results / "reconstruction_summary.csv",
        previous_results / "gate_results.csv",
        previous_results / "decision.csv",
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


def activation_from_i(i_m: float) -> float:
    return 1.0 - math.exp(-i_m)


def reconstruct_potential_map(
    canonical_rows: list[dict[str, str]], omega_m0: float
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in canonical_rows:
        n_past = float(item["N_past"])
        i_m = 0.0 if n_past <= 0.0 else (n_past / LOCKED_U3) ** LOCKED_P
        exp_minus_i = math.exp(-i_m)
        a_from_i = activation_from_i(i_m)
        di_dn = 0.0 if n_past <= 0.0 else LOCKED_P * n_past ** (LOCKED_P - 1.0) / (LOCKED_U3**LOCKED_P)
        a_n = exp_minus_i * di_dn
        rho_mem = 1.0 - omega_m0 + LOCKED_B_MEM * a_from_i
        e2 = omega_m0 * math.exp(3.0 * n_past) + rho_mem
        kinetic = LOCKED_B_MEM * a_n / 6.0
        potential = rho_mem - kinetic
        dphi_dn = math.sqrt(max(0.0, LOCKED_B_MEM * a_n / e2))
        if di_dn <= 0.0:
            dphi_di = math.inf
            im_kinetic_metric = math.inf
            im_metric_status = "singular_present_endpoint_limit"
        else:
            dphi_di = dphi_dn / di_dn
            im_kinetic_metric = dphi_di * dphi_di
            im_metric_status = "finite_sample"

        a_csv = float(item["A_mem"])
        rho_csv = float(item["rho_mem_over_rhocrit0"])
        kinetic_csv = float(item["canonical_K_over_rhocrit0"])
        potential_csv = float(item["canonical_V_over_rhocrit0"])
        dphi_csv = float(item["abs_dphi_dN_Mpl"])

        rows.append(
            {
                "index": int(item["index"]),
                "z": float(item["z"]),
                "N_past": n_past,
                "I_M_detQ_candidate": i_m,
                "A_from_I": a_from_i,
                "A_csv": a_csv,
                "abs_A_error": abs(a_from_i - a_csv),
                "dI_dN": di_dn,
                "A_N_formula": a_n,
                "rho_formula": rho_mem,
                "rho_csv": rho_csv,
                "abs_rho_error": abs(rho_mem - rho_csv),
                "K_formula": kinetic,
                "K_csv": kinetic_csv,
                "abs_K_error": abs(kinetic - kinetic_csv),
                "V_formula": potential,
                "V_csv": potential_csv,
                "abs_V_error": abs(potential - potential_csv),
                "dphi_dN_formula": dphi_dn,
                "dphi_dN_csv": dphi_csv,
                "abs_dphi_dN_error": abs(dphi_dn - dphi_csv),
                "phi_csv": float(item["phi_minus_phi0_Mpl"]),
                "V_of_phi": potential,
                "dphi_dI": dphi_di,
                "I_M_kinetic_metric": im_kinetic_metric,
                "I_M_metric_status": im_metric_status,
            }
        )
    return rows


def max_abs(rows: list[dict[str, Any]], key: str) -> float:
    return max(abs(float(row[key])) for row in rows)


def finite_values(rows: list[dict[str, Any]], key: str) -> list[float]:
    values = [float(row[key]) for row in rows]
    return [value for value in values if math.isfinite(value)]


def noncircularity_tests(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tolerance = 1.0e-10
    monotonic_failures = 0
    duplicate_conflicts = 0
    max_near_duplicate_v_jump = 0.0
    previous_phi = None
    previous_v = None
    for row in rows:
        phi = float(row["phi_csv"])
        v_value = float(row["V_of_phi"])
        if previous_phi is not None and previous_v is not None:
            delta_phi = phi - previous_phi
            delta_v = abs(v_value - previous_v)
            if delta_phi < -1.0e-12:
                monotonic_failures += 1
            if abs(delta_phi) < 1.0e-10 and delta_v > 1.0e-8:
                duplicate_conflicts += 1
                max_near_duplicate_v_jump = max(max_near_duplicate_v_jump, delta_v)
        previous_phi = phi
        previous_v = v_value

    finite_metric = finite_values(rows, "I_M_kinetic_metric")
    max_metric = max(finite_metric) if finite_metric else math.inf
    min_metric = min(finite_metric) if finite_metric else math.inf

    formula_max_error = max(
        max_abs(rows, "abs_A_error"),
        max_abs(rows, "abs_rho_error"),
        max_abs(rows, "abs_K_error"),
        max_abs(rows, "abs_V_error"),
        max_abs(rows, "abs_dphi_dN_error"),
    )

    return [
        {
            "test": "formula_reconstructs_checkpoint_135",
            "status": "pass" if formula_max_error < tolerance else "fail",
            "metric": formula_max_error,
            "evidence": "I_M -> A(N) reproduces rho, K, V, and dphi/dN from the previous canonical reconstruction",
        },
        {
            "test": "V_phi_single_valued",
            "status": "pass" if monotonic_failures == 0 and duplicate_conflicts == 0 else "fail",
            "metric": f"monotonic_failures={monotonic_failures}; duplicate_conflicts={duplicate_conflicts}; max_near_duplicate_v_jump={max_near_duplicate_v_jump}",
            "evidence": "phi(N) is nondecreasing, so the reconstructed potential can be tabulated as V(phi)",
        },
        {
            "test": "determinant_activation_non_circularity",
            "status": "partial",
            "metric": "A=1-exp(-I_M) works only after choosing I_M=(N/u3)^3",
            "evidence": "the determinant-like scalar can own the activation map but not the amplitude or stress law by itself",
        },
        {
            "test": "bare_I_M_kinetic_metric_regular",
            "status": "fail",
            "metric": f"finite_sample_min={min_metric}; finite_sample_max={max_metric}; endpoint_limit=singular",
            "evidence": "using I_M itself as the scalar coordinate requires a singular endpoint kinetic metric because dI_M/dN vanishes faster than dphi/dN at N=0",
        },
        {
            "test": "potential_owned_without_background_reconstruction",
            "status": "fail",
            "metric": "V(phi) is generated from the fitted locked background trajectory",
            "evidence": "no independent S_cell/S_stress variation has produced the same V(phi), B_mem, p, or u3",
        },
        {
            "test": "Bianchi_conservation_for_effective_owner",
            "status": "pass_effective",
            "metric": "minimal canonical scalar has on-shell covariant conservation",
            "evidence": "this repairs the effective stress owner but does not derive the parent memory tensor",
        },
        {
            "test": "local_GR_transfer",
            "status": "open",
            "metric": "not tested here",
            "evidence": "a healthy cosmological scalar is not automatically a proof of local silence or PPN recovery",
        },
    ]


def action_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "determinant_activation_only",
            "action_sketch": "I_M = det(Q) or equivalent coherent-domain invariant; A=1-exp(-I_M)",
            "what_it_owns": "activation shape once I_M=(N/u3)^3 is supplied",
            "reconstruction_status": "passes_activation_map",
            "noncircularity_status": "partial",
            "bianchi_status": "not_a_stress_tensor",
            "local_gr_status": "open",
            "verdict": "useful_variable_not_parent_action",
        },
        {
            "candidate": "potential_only_U_of_I",
            "action_sketch": "S = integral sqrt(-g)[-U(I_M)], U=rho_Lambda+B_mem(1-exp(-I_M))",
            "what_it_owns": "background energy density as a potential table",
            "reconstruction_status": "matches_rho_only",
            "noncircularity_status": "fails_pressure",
            "bianchi_status": "incomplete_without_I_M_equation",
            "local_gr_status": "open",
            "verdict": "rejected_as_full_owner_because_K_equals_zero_forces_w_equals_minus_one",
        },
        {
            "candidate": "canonical_reconstructed_phi",
            "action_sketch": "S = integral sqrt(-g)[-1/2(partial phi)^2 - V(phi)]",
            "what_it_owns": "rho, pressure, K, V, c_s^2=1, and on-shell conservation",
            "reconstruction_status": "passes",
            "noncircularity_status": "fails_as_parent_derivation",
            "bianchi_status": "pass_effective",
            "local_gr_status": "open",
            "verdict": "best_EFT_owner_not_fundamental_origin",
        },
        {
            "candidate": "I_M_kinetic_metric",
            "action_sketch": "S = integral sqrt(-g)[-1/2 G(I_M)(partial I_M)^2 - U(I_M)]",
            "what_it_owns": "can mimic canonical phi if G(I_M)=(dphi/dI_M)^2 is chosen",
            "reconstruction_status": "formally_possible",
            "noncircularity_status": "fails_regular_clean_origin",
            "bianchi_status": "pass_if_action_defined",
            "local_gr_status": "open",
            "verdict": "not_clean_because_metric_is_reconstructed_and_singular_at_present_endpoint",
        },
        {
            "candidate": "auxiliary_constraint",
            "action_sketch": "S = S_GR + S_mem + lambda[I_M - I_M(C_coh,Q)]",
            "what_it_owns": "could enforce nonpropagating smooth memory",
            "reconstruction_status": "open",
            "noncircularity_status": "open",
            "bianchi_status": "open_until_lambda_stress_is_derived",
            "local_gr_status": "possibly_best_exact_route",
            "verdict": "theorem_target_not_yet_constructed",
        },
        {
            "candidate": "geometric_counterstress",
            "action_sketch": "move memory into a divergence-free geometric tensor E_mem^munu",
            "what_it_owns": "could cancel perfect-fluid perturbation obstructions by identity",
            "reconstruction_status": "open",
            "noncircularity_status": "open",
            "bianchi_status": "must_be_identity_level",
            "local_gr_status": "high_risk_until_local_limit_derived",
            "verdict": "heavy_route_only_if_auxiliary_route_fails",
        },
    ]


def gate_rows(tests: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_test = {row["test"]: row for row in tests}
    formula_pass = by_test["formula_reconstructs_checkpoint_135"]["status"] == "pass"
    vphi_pass = by_test["V_phi_single_valued"]["status"] == "pass"
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass",
            "evidence": "source register was checked before outputs were written",
        },
        {
            "gate": "formula_reconstruction",
            "status": "pass" if formula_pass else "fail",
            "evidence": str(by_test["formula_reconstructs_checkpoint_135"]["metric"]),
        },
        {
            "gate": "V_phi_single_valued",
            "status": "pass" if vphi_pass else "fail",
            "evidence": str(by_test["V_phi_single_valued"]["metric"]),
        },
        {
            "gate": "canonical_EFT_owner",
            "status": "pass_effective",
            "evidence": "canonical scalar can own the reconstructed stress and c_s^2=1",
        },
        {
            "gate": "determinant_activation_owner",
            "status": "partial",
            "evidence": "I_M owns activation after u3 and p are supplied; it does not own B_mem or the stress tensor",
        },
        {
            "gate": "bare_I_M_action_regular",
            "status": "fail",
            "evidence": str(by_test["bare_I_M_kinetic_metric_regular"]["metric"]),
        },
        {
            "gate": "parent_action_non_circularity",
            "status": "fail",
            "evidence": "V(phi) and G(I_M) are reconstructed from the desired background rather than predicted",
        },
        {
            "gate": "Bmem_amplitude_derivation",
            "status": "fail",
            "evidence": "B_mem=2/27 remains inserted from the locked empirical branch",
        },
        {
            "gate": "exact_local_GR_transfer",
            "status": "open",
            "evidence": "cosmological EFT health does not prove local PPN silence",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "status",
            "verdict": "potential_map_reconstructed_parent_action_not_derived",
            "evidence": "the locked memory branch has a healthy V(phi) map, but the parent action still has not produced it non-circularly",
        },
        {
            "item": "what_was_proved",
            "verdict": "effective_action_owner_exists",
            "evidence": "rho, pressure, K, V, dphi/dN, and c_s^2=1 are mutually consistent for the locked background",
        },
        {
            "item": "what_failed",
            "verdict": "determinant_variable_is_not_enough",
            "evidence": "I_M can parameterize activation but cannot by itself derive a regular kinetic metric, potential, amplitude, or local-GR limit",
        },
        {
            "item": "next_target",
            "verdict": "try_auxiliary_or_geometric_action_owner",
            "evidence": "the next derivation should make I_M a constrained variable from C_coh/Q or demote the branch to explicit EFT closure",
        },
    ]


def run_audit(output_root: Path, timestamp: str | None = None, previous_run: Path = PREVIOUS_RUN) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-memory-action-potential-owner-attempt"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve(), previous_run)
    missing = [row["path"] for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    previous_status = read_json(previous_run / "status.json")
    omega_m0 = float(previous_status["locked_background"]["Omega_m0"])
    canonical_rows = read_csv_rows(previous_run / "results" / "canonical_reconstruction.csv")

    potential_map = reconstruct_potential_map(canonical_rows, omega_m0)
    tests = noncircularity_tests(potential_map)
    action_candidates = action_candidate_rows()
    gates = gate_rows(tests)
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "issue"])
    write_csv(
        results_dir / "potential_map_reconstruction.csv",
        potential_map,
        [
            "index",
            "z",
            "N_past",
            "I_M_detQ_candidate",
            "A_from_I",
            "A_csv",
            "abs_A_error",
            "dI_dN",
            "A_N_formula",
            "rho_formula",
            "rho_csv",
            "abs_rho_error",
            "K_formula",
            "K_csv",
            "abs_K_error",
            "V_formula",
            "V_csv",
            "abs_V_error",
            "dphi_dN_formula",
            "dphi_dN_csv",
            "abs_dphi_dN_error",
            "phi_csv",
            "V_of_phi",
            "dphi_dI",
            "I_M_kinetic_metric",
            "I_M_metric_status",
        ],
    )
    write_csv(
        results_dir / "action_candidate_ledger.csv",
        action_candidates,
        [
            "candidate",
            "action_sketch",
            "what_it_owns",
            "reconstruction_status",
            "noncircularity_status",
            "bianchi_status",
            "local_gr_status",
            "verdict",
        ],
    )
    write_csv(results_dir / "noncircularity_tests.csv", tests, ["test", "status", "metric", "evidence"])
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    formula_error = next(row["metric"] for row in tests if row["test"] == "formula_reconstructs_checkpoint_135")
    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "locked_background": previous_status["locked_background"],
        "formula_max_error": formula_error,
        "generated": [
            "source_register.csv",
            "potential_map_reconstruction.csv",
            "action_candidate_ledger.csv",
            "noncircularity_tests.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "auxiliary_or_geometric_memory_action_owner",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--previous-run", type=Path, default=PREVIOUS_RUN)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_audit(args.output_root, args.timestamp, args.previous_run))


if __name__ == "__main__":
    main()

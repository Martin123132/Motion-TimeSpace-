#!/usr/bin/env python3
"""Attempt to derive the locked memory density shape from additive hazard."""

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
VOLUME_RUN = RUNS_ROOT / "20260531-201500-coherent-volume-pressure-kernel-theorem"
VOLUME_RESULTS = VOLUME_RUN / "results"

LOCKED_B_MEM = 2.0 / 27.0
LOCKED_U3 = 0.25
LOCKED_P = 3.0
CLAIM_CEILING = "hazard_density_shape_conditional_amplitude_not_derived"


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


def source_register_rows(script_path: Path, volume_run: Path) -> list[dict[str, Any]]:
    volume_results = volume_run / "results"
    paths = [
        script_path,
        WORK_DIR / "50-parent-activation-law-attempt.md",
        WORK_DIR / "51-FLRW-memory-current-contract.md",
        WORK_DIR / "56-u3-quarter-parent-cell-theorem-attempt.md",
        WORK_DIR / "109-boundary-charge-two-ninth-theorem-attempt.md",
        WORK_DIR / "136-memory-action-potential-owner-attempt.md",
        WORK_DIR / "137-auxiliary-geometric-memory-action-owner.md",
        WORK_DIR / "138-coherent-volume-pressure-kernel-theorem.md",
        volume_run / "status.json",
        volume_results / "pressure_kernel_check.csv",
        volume_results / "gate_results.csv",
        volume_results / "decision.csv",
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


def hazard_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "additive_exposure",
            "statement": "I(D1 union D2)=I(D1)+I(D2) for independent coherent exposure increments",
            "result": "memory exposure is a cumulative hazard variable",
            "status": "assumption_contract",
            "blocker": "parent current must prove additivity for the physical coherent cells",
        },
        {
            "step": "survival_composition",
            "statement": "S(I1+I2)=S(I1)S(I2), S(0)=1, S continuous and monotone",
            "result": "Cauchy exponential survival equation",
            "status": "pass_math",
            "blocker": "requires independent increments / Markov-like coherent memory",
        },
        {
            "step": "exponential_solution",
            "statement": "S(I)=exp(-kappa I)",
            "result": "A(I)=1-S(I)=1-exp(-kappa I)",
            "status": "pass_math",
            "blocker": "kappa is a unit convention only if I normalization is parent-fixed",
        },
        {
            "step": "dimensionless_exposure_choice",
            "statement": "define I_M := kappa I so S=exp(-I_M)",
            "result": "A=1-exp(-I_M)",
            "status": "pass_conditional",
            "blocker": "normalization of I_M is tied to u3 / cell scale",
        },
        {
            "step": "determinant_exposure",
            "statement": "I_M=det(Q), Q^i_j=X delta^i_j on FLRW",
            "result": "I_M=X^3, so p=3 follows from spatial determinant",
            "status": "pass_conditional",
            "blocker": "Q itself is not parent-action-derived",
        },
        {
            "step": "quarter_cell_normalization",
            "statement": "X=4N_D=N_D/u3 from 3+1 coherent cell",
            "result": "u3=1/4",
            "status": "pass_conditional",
            "blocker": "3+1 cell split is not parent-action-derived",
        },
        {
            "step": "density_law",
            "statement": "rho_M=rho_Lambda+B_mem A(I_M)",
            "result": "density shape follows if B_mem is a fixed charge amplitude",
            "status": "partial",
            "blocker": "B_mem=2/27 is not derived by hazard law",
        },
    ]


def activation(n_past: float) -> float:
    if n_past <= 0.0:
        return 0.0
    return 1.0 - math.exp(-((n_past / LOCKED_U3) ** LOCKED_P))


def activation_derivative(n_past: float) -> float:
    if n_past <= 0.0:
        return 0.0
    i_m = (n_past / LOCKED_U3) ** LOCKED_P
    d_i_dn = LOCKED_P * n_past ** (LOCKED_P - 1.0) / (LOCKED_U3**LOCKED_P)
    return math.exp(-i_m) * d_i_dn


def activation_shape_rows(pressure_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    previous_a = None
    for item in pressure_rows:
        n_past = float(item["N_past"])
        i_m = 0.0 if n_past <= 0.0 else (n_past / LOCKED_U3) ** LOCKED_P
        survival = math.exp(-i_m)
        a_mem = activation(n_past)
        a_n = activation_derivative(n_past)
        d_i_dn = 0.0 if n_past <= 0.0 else LOCKED_P * n_past ** (LOCKED_P - 1.0) / (LOCKED_U3**LOCKED_P)
        hazard_rate = None if survival == 0.0 or d_i_dn == 0.0 else a_n / (survival * d_i_dn)
        bounded = 0.0 <= a_mem <= 1.0
        monotone_step = True if previous_a is None else a_mem + 1.0e-15 >= previous_a
        rows.append(
            {
                "index": int(item["index"]),
                "z": float(item["z"]),
                "N_past": n_past,
                "I_M": i_m,
                "survival_exp_minus_I": survival,
                "A_mem": a_mem,
                "A_N": a_n,
                "dI_dN": d_i_dn,
                "hazard_rate_dA_over_SdI": "" if hazard_rate is None else hazard_rate,
                "hazard_rate_abs_error_from_1": "" if hazard_rate is None else abs(hazard_rate - 1.0),
                "bounded_0_1": bounded,
                "monotone_step": monotone_step,
                "endpoint_double_zero": n_past > 0.0 or (abs(a_mem) < 1.0e-15 and abs(a_n) < 1.0e-15),
            }
        )
        previous_a = a_mem
    return rows


def survival_composition_rows() -> list[dict[str, Any]]:
    test_pairs = [
        (0.0, 0.0),
        (0.01, 0.02),
        (0.05, 0.10),
        (0.25, 0.50),
        (1.00, 2.00),
        (3.00, 4.00),
    ]
    rows: list[dict[str, Any]] = []
    for i1, i2 in test_pairs:
        left = math.exp(-(i1 + i2))
        right = math.exp(-i1) * math.exp(-i2)
        rows.append(
            {
                "I1": i1,
                "I2": i2,
                "S_I1_plus_I2": left,
                "S_I1_times_S_I2": right,
                "abs_composition_error": abs(left - right),
            }
        )
    return rows


def alternative_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "law": "exponential_hazard",
            "A_of_I": "1-exp(-I)",
            "bounded": "pass",
            "A0": "pass",
            "constant_hazard": "pass",
            "survival_composition": "pass",
            "endpoint_regular_with_I=N^3": "pass",
            "verdict": "retained_conditional_unique_shape",
        },
        {
            "law": "linear_exposure",
            "A_of_I": "I",
            "bounded": "fail",
            "A0": "pass",
            "constant_hazard": "fail",
            "survival_composition": "fail",
            "endpoint_regular_with_I=N^3": "pass_local_only",
            "verdict": "rejected_unbounded_not_survival_law",
        },
        {
            "law": "rational_saturation",
            "A_of_I": "I/(1+I)",
            "bounded": "pass",
            "A0": "pass",
            "constant_hazard": "fail",
            "survival_composition": "fail",
            "endpoint_regular_with_I=N^3": "pass",
            "verdict": "rejected_no_independent_increment_composition",
        },
        {
            "law": "tanh_saturation",
            "A_of_I": "tanh(I)",
            "bounded": "pass",
            "A0": "pass",
            "constant_hazard": "fail",
            "survival_composition": "fail",
            "endpoint_regular_with_I=N^3": "pass",
            "verdict": "rejected_no_hazard_composition",
        },
        {
            "law": "logistic_shifted",
            "A_of_I": "2/(1+exp(-I))-1",
            "bounded": "pass",
            "A0": "pass",
            "constant_hazard": "fail",
            "survival_composition": "fail",
            "endpoint_regular_with_I=N^3": "pass",
            "verdict": "rejected_extra_shape_without_parent_need",
        },
    ]


def amplitude_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "hazard_survival_law",
            "can_derive_shape": "yes_conditional",
            "can_derive_Bmem": "no",
            "issue": "hazard law fixes saturation shape, not the total charge released",
            "status": "shape_only",
        },
        {
            "route": "boundary_degree_count_2over3_times_trace_1over3",
            "can_derive_shape": "no",
            "can_derive_Bmem": "no",
            "issue": "degree counting is not a normalized charge theorem",
            "status": "rejected_as_derivation",
        },
        {
            "route": "normalized_boundary_charge",
            "can_derive_shape": "not_by_itself",
            "can_derive_Bmem": "possible_target",
            "issue": "requires Q_boundary, Q_star, and endpoint equations before data",
            "status": "best_amplitude_theorem_target",
        },
        {
            "route": "empirical_locked_branch",
            "can_derive_shape": "no",
            "can_derive_Bmem": "no",
            "issue": "robustness motivates theory time but does not predict the number",
            "status": "empirical_support_only",
        },
    ]


def summary_rows(shape_rows: list[dict[str, Any]], composition_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    hazard_errors = [
        float(row["hazard_rate_abs_error_from_1"])
        for row in shape_rows
        if row["hazard_rate_abs_error_from_1"] != ""
    ]
    max_hazard_error = max(hazard_errors) if hazard_errors else 0.0
    max_composition_error = max(float(row["abs_composition_error"]) for row in composition_rows)
    bounded_failures = sum(1 for row in shape_rows if not row["bounded_0_1"])
    monotone_failures = sum(1 for row in shape_rows if not row["monotone_step"])
    endpoint_failures = sum(1 for row in shape_rows if not row["endpoint_double_zero"])
    final_a = float(shape_rows[-1]["A_mem"])
    return [
        {
            "item": "rows_checked",
            "value": len(shape_rows),
            "readout": "matches_pressure_kernel_grid",
        },
        {
            "item": "max_hazard_rate_error",
            "value": max_hazard_error,
            "readout": "pass" if max_hazard_error < 1.0e-12 else "check",
        },
        {
            "item": "max_survival_composition_error",
            "value": max_composition_error,
            "readout": "pass" if max_composition_error < 1.0e-12 else "check",
        },
        {
            "item": "bounded_failures",
            "value": bounded_failures,
            "readout": "pass" if bounded_failures == 0 else "fail",
        },
        {
            "item": "monotone_failures",
            "value": monotone_failures,
            "readout": "pass" if monotone_failures == 0 else "fail",
        },
        {
            "item": "endpoint_failures",
            "value": endpoint_failures,
            "readout": "pass" if endpoint_failures == 0 else "fail",
        },
        {
            "item": "A_at_z3",
            "value": final_a,
            "readout": "saturated" if final_a > 0.999 else "check",
        },
    ]


def gate_rows(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_item = {row["item"]: row for row in summary}
    hazard_pass = float(by_item["max_hazard_rate_error"]["value"]) < 1.0e-12
    composition_pass = float(by_item["max_survival_composition_error"]["value"]) < 1.0e-12
    regular_pass = (
        int(by_item["bounded_failures"]["value"]) == 0
        and int(by_item["monotone_failures"]["value"]) == 0
        and int(by_item["endpoint_failures"]["value"]) == 0
    )
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass",
            "evidence": "source register was checked before outputs were written",
        },
        {
            "gate": "survival_law_from_additive_hazard",
            "status": "pass_conditional" if hazard_pass and composition_pass else "fail",
            "evidence": f"hazard_error={float(by_item['max_hazard_rate_error']['value']):.6g}; composition_error={float(by_item['max_survival_composition_error']['value']):.6g}",
        },
        {
            "gate": "activation_shape_regular",
            "status": "pass" if regular_pass else "fail",
            "evidence": f"bounded_failures={by_item['bounded_failures']['value']}; monotone_failures={by_item['monotone_failures']['value']}; endpoint_failures={by_item['endpoint_failures']['value']}",
        },
        {
            "gate": "p3_from_determinant",
            "status": "pass_conditional",
            "evidence": "I_M=det(Q) gives cubic exposure on FLRW if Q^i_j=X delta^i_j",
        },
        {
            "gate": "u3_from_3plus1_cell",
            "status": "pass_conditional",
            "evidence": "u3=1/4 follows only if the coherent 3+1 cell normalization is parent-owned",
        },
        {
            "gate": "density_shape_derived",
            "status": "pass_conditional",
            "evidence": "rho_M=rho_Lambda+B_mem[1-exp(-I_M)] follows as a saturated hazard shape once B_mem is supplied",
        },
        {
            "gate": "Bmem_amplitude_derived",
            "status": "fail",
            "evidence": "hazard law fixes shape, not total normalized charge B_mem=2/27",
        },
        {
            "gate": "domain_and_boundary_owner",
            "status": "open",
            "evidence": "coherent domain D and J_rel still must make I_M additive and local-silent",
        },
        {
            "gate": "parent_field_theory_promoted",
            "status": "fail",
            "evidence": "shape is theorem-shaped, but amplitude/domain/action ownership remain incomplete",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "status",
            "verdict": "density_hazard_shape_derived_conditionally_amplitude_not_derived",
            "evidence": "additive exposure plus multiplicative survival gives A=1-exp(-I_M); B_mem remains an external charge amplitude",
        },
        {
            "item": "what_improved",
            "verdict": "density_shape_no_longer_arbitrary_if_hazard_axioms_hold",
            "evidence": "the exponential saturation is selected by independent-increment composition, not by curve-fitting convenience",
        },
        {
            "item": "what_still_fails",
            "verdict": "Bmem_and_parent_current_not_derived",
            "evidence": "the theorem still needs normalized boundary charge, endpoint equations, and parent derivation of Q/u3/domain",
        },
        {
            "item": "next_target",
            "verdict": "derive_boundary_charge_amplitude_or_demote_amplitude",
            "evidence": "after the hazard shape, the live bottleneck is B_mem=2/27 and the domain/current owner",
        },
    ]


def run_audit(output_root: Path, timestamp: str | None = None, volume_run: Path = VOLUME_RUN) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-density-law-hazard-theorem-attempt"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve(), volume_run)
    missing = [row["path"] for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    volume_status = read_json(volume_run / "status.json")
    pressure_rows = read_csv_rows(volume_run / "results" / "pressure_kernel_check.csv")

    derivation = hazard_derivation_rows()
    shape = activation_shape_rows(pressure_rows)
    composition = survival_composition_rows()
    alternatives = alternative_law_rows()
    amplitude_routes = amplitude_route_rows()
    summary = summary_rows(shape, composition)
    gates = gate_rows(summary)
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "issue"])
    write_csv(results_dir / "hazard_derivation_chain.csv", derivation, ["step", "statement", "result", "status", "blocker"])
    write_csv(
        results_dir / "activation_shape_tests.csv",
        shape,
        [
            "index",
            "z",
            "N_past",
            "I_M",
            "survival_exp_minus_I",
            "A_mem",
            "A_N",
            "dI_dN",
            "hazard_rate_dA_over_SdI",
            "hazard_rate_abs_error_from_1",
            "bounded_0_1",
            "monotone_step",
            "endpoint_double_zero",
        ],
    )
    write_csv(results_dir / "survival_composition_tests.csv", composition, ["I1", "I2", "S_I1_plus_I2", "S_I1_times_S_I2", "abs_composition_error"])
    write_csv(results_dir / "alternative_law_ledger.csv", alternatives, ["law", "A_of_I", "bounded", "A0", "constant_hazard", "survival_composition", "endpoint_regular_with_I=N^3", "verdict"])
    write_csv(results_dir / "amplitude_route_ledger.csv", amplitude_routes, ["route", "can_derive_shape", "can_derive_Bmem", "issue", "status"])
    write_csv(results_dir / "summary.csv", summary, ["item", "value", "readout"])
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "input_status": volume_status["status"],
        "locked_values_used": {
            "B_mem": LOCKED_B_MEM,
            "u3": LOCKED_U3,
            "p": LOCKED_P,
        },
        "generated": [
            "source_register.csv",
            "hazard_derivation_chain.csv",
            "activation_shape_tests.csv",
            "survival_composition_tests.csv",
            "alternative_law_ledger.csv",
            "amplitude_route_ledger.csv",
            "summary.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "derive_boundary_charge_amplitude_or_demote_amplitude_to_empirical_closure",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--volume-run", type=Path, default=VOLUME_RUN)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_audit(args.output_root, args.timestamp, args.volume_run))


if __name__ == "__main__":
    main()

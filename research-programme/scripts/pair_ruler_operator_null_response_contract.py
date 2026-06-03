#!/usr/bin/env python3
"""Write the null-response contract for a BAO pair-ruler operator."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

SOURCE_LAW_RUN = RUNS_ROOT / "20260531-235959-trace-quadrupole-source-law-attempt"
SOURCE_LAW_RESULTS = SOURCE_LAW_RUN / "results"
TENSOR_RUN = RUNS_ROOT / "20260531-235959-ruler-projection-parent-tensor-attempt"
TENSOR_RESULTS = TENSOR_RUN / "results"
RULER_CONTRACT_RUN = RUNS_ROOT / "20260531-235959-ruler-only-projection-theorem-contract"
RULER_CONTRACT_RESULTS = RULER_CONTRACT_RUN / "results"

CLAIM_CEILING = "pair_ruler_operator_null_response_contract_no_bridge_promotion"
STATUS = "pair_ruler_null_response_contract_conditional_bilocal_operator_not_parent_derived"


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
    if name.startswith("162-") or name.endswith("pair_ruler_operator_null_response_contract.py"):
        return "current pair-ruler null-response contract"
    if name.startswith("161-") or "trace-quadrupole-source-law" in str(path):
        return "trace/quadrupole source-law candidate"
    if name.startswith("160-") or "ruler-projection-parent-tensor" in str(path):
        return "parent tensor decomposition"
    if name.startswith("159-") or "ruler-only-projection-theorem-contract" in str(path):
        return "no-smuggling ruler-only contract"
    if name.startswith("158-"):
        return "global clock demotion and ruler-only motivation"
    if name.startswith("53-") or name.startswith("54-"):
        return "coherent-domain/local-silence condition"
    return "supporting source"


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    paths = [
        script_path,
        WORK_DIR / "53-coherent-projection-local-silence-gate.md",
        WORK_DIR / "54-coherent-domain-and-u3-origin.md",
        WORK_DIR / "158-cell-clock-BAO-row-and-SN-Hz-failure-mode-audit.md",
        WORK_DIR / "159-ruler-only-projection-theorem-contract.md",
        WORK_DIR / "160-ruler-projection-parent-tensor-attempt.md",
        WORK_DIR / "161-trace-quadrupole-source-law-attempt.md",
        RULER_CONTRACT_RUN / "status.json",
        RULER_CONTRACT_RESULTS / "no_smuggling_gates.csv",
        RULER_CONTRACT_RESULTS / "formula_contract.csv",
        TENSOR_RUN / "status.json",
        TENSOR_RESULTS / "gate_results.csv",
        SOURCE_LAW_RUN / "status.json",
        SOURCE_LAW_RESULTS / "equation_contract.csv",
        SOURCE_LAW_RESULTS / "gate_results.csv",
        SOURCE_LAW_RESULTS / "decision.csv",
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


def operator_condition_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "bilocal_connected_operator",
            "formula": "delta ell^A(x,y)=K^A_B[D](x,y) ell^B(x,y)",
            "required_for": "BAO pair response without one-point metric/clock deformation",
            "status": "conditional_requirement",
            "failure_if_missing": "operator becomes an ad hoc BAO correction or a one-point field deformation",
        },
        {
            "condition": "zero_one_point_marginal",
            "formula": "integral_D dmu_y W_D(x,y) K^A_B(x,y)=0",
            "required_for": "SN/H(z)/local one-point null response at leading order",
            "status": "conditional_null_theorem",
            "failure_if_missing": "one-point observables inherit the projection",
        },
        {
            "condition": "non_metric_non_clock",
            "formula": "delta g_mu_nu=0, delta z_source=0, delta u^mu_observer=0 at this order",
            "required_for": "avoid reintroducing global clock/metric branch",
            "status": "mandatory",
            "failure_if_missing": "157/158 SN failure returns",
        },
        {
            "condition": "trace_quadrupole_eigenstructure",
            "formula": "K^A_B=T_D h^A_B+S_D(n^A n_B-h^A_B/3)",
            "required_for": "single tensor supplies radial and transverse BAO response",
            "status": "candidate_from_160_161",
            "failure_if_missing": "Pi_perp/Pi_parallel become row-wise closure functions",
        },
        {
            "condition": "zero_memory_and_local_silence",
            "formula": "B_mem->0 or F_D->0 or bound-domain X_D=0 implies K^A_B->0",
            "required_for": "protect local GR route and avoid projection in stationary domains",
            "status": "conditional_from_coherent_domain_work",
            "failure_if_missing": "local rods/clocks and PPN branch threatened",
        },
        {
            "condition": "late_ruler_CMB_safety",
            "formula": "delta r_d=0 unless full early-time Boltzmann branch derives otherwise",
            "required_for": "avoid uncontrolled CMB sound-horizon claim",
            "status": "open_mandatory",
            "failure_if_missing": "CMB bridge becomes a hidden calibration patch",
        },
        {
            "condition": "parent_variational_owner",
            "formula": "K^A_B follows from action/effective action variation or conservation identity",
            "required_for": "field-theory status instead of closure",
            "status": "missing",
            "failure_if_missing": "route remains empirical/effective closure only",
        },
    ]


def route_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "metric_deformation",
            "operator_type": "one-point universal geometry",
            "BAO_response": "yes",
            "SN_Hz_null": "no",
            "status": "rejected_for_ruler_only",
            "reason": "metric/geodesic deformation must hit SN, H(z), lensing, and local clocks",
        },
        {
            "route": "global_clock_or_redshift_map",
            "operator_type": "one-point clock/source-redshift map",
            "BAO_response": "yes",
            "SN_Hz_null": "no",
            "status": "demoted",
            "reason": "157/158 show SN penalties when the projection is globally coupled",
        },
        {
            "route": "one_point_observer_coframe_strain",
            "operator_type": "local coframe/lapse/rod deformation",
            "BAO_response": "yes",
            "SN_Hz_null": "no",
            "status": "rejected_for_null_branch",
            "reason": "local rods, clocks, and H(z) inherit one-point observer strain",
        },
        {
            "route": "connected_bilocal_pair_kernel_zero_marginal",
            "operator_type": "two-point pair-separation operator",
            "BAO_response": "yes",
            "SN_Hz_null": "conditional_yes",
            "status": "best_live_effective_route",
            "reason": "nonzero at finite pair separation while one-point marginal response vanishes",
        },
        {
            "route": "late_time_BAO_ruler_calibration",
            "operator_type": "effective standard-ruler transport",
            "BAO_response": "yes",
            "SN_Hz_null": "conditional_yes",
            "status": "live_high_risk",
            "reason": "can be observationally clean but risks becoming a calibration patch",
        },
        {
            "route": "ad_hoc_BAO_likelihood_shift",
            "operator_type": "data-space correction",
            "BAO_response": "yes",
            "SN_Hz_null": "by_declaration",
            "status": "rejected",
            "reason": "not field theory and not a derived operator",
        },
    ]


def observable_response_rows() -> list[dict[str, Any]]:
    return [
        {
            "observable": "BAO pair separation",
            "symbol": "ell_BAO^A(x,y)",
            "response_under_pair_kernel": "nonzero",
            "condition": "K^A_B(x,y) evaluated at finite pair separation",
            "status": "intended_response",
            "remaining_test": "fit/rerun BAO with fixed 161 laws and official covariance",
        },
        {
            "observable": "SN luminosity distance",
            "symbol": "D_L_SN(x)",
            "response_under_pair_kernel": "zero_at_linear_order",
            "condition": "zero one-point marginal and no metric/photon-geodesic deformation",
            "status": "conditional_null",
            "remaining_test": "prove from parent operator, then rerun Pantheon+ no-clock branch",
        },
        {
            "observable": "cosmic chronometer H(z)",
            "symbol": "H_CC(z)",
            "response_under_pair_kernel": "zero_at_linear_order",
            "condition": "no clock/lapse/redshift remap and no background equation deformation",
            "status": "conditional_null",
            "remaining_test": "prove background variation vanishes",
        },
        {
            "observable": "local rods/clocks/PPN",
            "symbol": "local coframe",
            "response_under_pair_kernel": "zero_if_bound_domain_silent",
            "condition": "K^A_B->0 in bound domains and no one-point coframe strain",
            "status": "conditional_null",
            "remaining_test": "connect to local fixed-point/local-silence branch",
        },
        {
            "observable": "lensing/correlation observables",
            "symbol": "C_ell, xi(r), growth/RSD",
            "response_under_pair_kernel": "open",
            "condition": "two-point matter statistics may inherit the operator",
            "status": "must_test_not_null_by_default",
            "remaining_test": "growth/RSD/lensing consistency audit",
        },
        {
            "observable": "CMB sound horizon",
            "symbol": "r_d",
            "response_under_pair_kernel": "zero_only_if_late_ruler_transport",
            "condition": "operator turns on after sound-horizon freeze-out or leaves early plasma untouched",
            "status": "open_mandatory",
            "remaining_test": "Boltzmann/CMB safety branch",
        },
    ]


def theorem_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "Define the BAO object as a connected two-point ruler observable.",
            "formula": "ell^A(x,y)=e^A_i[x,y](x-y)^i",
            "status": "definition_target",
            "failure_mode": "if BAO is treated as one-point distance only, the null split is impossible",
        },
        {
            "step": 2,
            "statement": "Let the MTS ruler operator act only on the pair separation.",
            "formula": "delta ell^A=K^A_B(x,y)ell^B",
            "status": "conditional_operator",
            "failure_mode": "if K is delta g or delta z, SN/H(z) inherit it",
        },
        {
            "step": 3,
            "statement": "Use the 160/161 trace-quadrupole source law as the finite-pair kernel.",
            "formula": "K^A_B=T_D h^A_B+S_D(n^A n_B-h^A_B/3)",
            "status": "candidate_source",
            "failure_mode": "source laws are not parent-derived yet",
        },
        {
            "step": 4,
            "statement": "Impose a zero one-point marginal.",
            "formula": "integral_D W_D(x,y)K^A_B(x,y)dmu_y=0",
            "status": "conditional_null_proof",
            "failure_mode": "without this, one-point observables receive an induced strain",
        },
        {
            "step": 5,
            "statement": "Then one-point linear response vanishes but pair response remains.",
            "formula": "delta O_1 proportional to integral K = 0; delta O_2 proportional to K(x,y) != 0",
            "status": "conditional_derivation",
            "failure_mode": "only valid at leading order and only if metric/clock deformation is absent",
        },
        {
            "step": 6,
            "statement": "Parent theory must derive the bilocal kernel or demote the route.",
            "formula": "K^A_B = delta^2 S_eff / delta pair fields, not fitted likelihood term",
            "status": "missing_parent_owner",
            "failure_mode": "closure-only",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_paths",
            "status": "pass",
            "evidence": "all required source paths exist",
        },
        {
            "gate": "conditional_null_algebra",
            "status": "pass_conditional",
            "evidence": "zero one-point marginal gives delta O_1=0 while K(x,y) gives delta O_2!=0",
        },
        {
            "gate": "metric_clock_exclusion",
            "status": "mandatory_condition_written",
            "evidence": "delta g=delta z=delta u=0 required at this order",
        },
        {
            "gate": "BAO_pair_operator",
            "status": "conditional_pass",
            "evidence": "connected bilocal pair kernel is the only live route that preserves SN/H(z) null response",
        },
        {
            "gate": "parent_action_owner",
            "status": "fail_open",
            "evidence": "no fundamental or effective action currently derives K^A_B and zero marginal",
        },
        {
            "gate": "locality",
            "status": "open_risk",
            "evidence": "bilocal operator is acceptable only as a derived effective/coarse-grained object, not arbitrary nonlocality",
        },
        {
            "gate": "lensing_growth_safety",
            "status": "open",
            "evidence": "two-point observables need not be null and must be tested",
        },
        {
            "gate": "CMB_r_d_safety",
            "status": "open_mandatory",
            "evidence": "late-ruler condition or full Boltzmann derivation still required",
        },
        {
            "gate": "promotion",
            "status": "fail",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "status",
            "verdict": STATUS,
            "evidence": "a conditional bilocal zero-marginal operator can explain BAO pair response with SN/H(z) null response, but parent derivation is missing",
        },
        {
            "item": "best_live_operator",
            "verdict": "connected_bilocal_pair_kernel_with_zero_one_point_marginal",
            "evidence": "nonzero K(x,y) moves BAO pair separation; integral K marginal vanishes for one-point observables",
        },
        {
            "item": "conditional_null_theorem",
            "verdict": "delta O_1=0 if integral_D K=0 and delta g=delta z=delta u=0",
            "evidence": "linear one-point response is proportional to the kernel marginal",
        },
        {
            "item": "rejected_routes",
            "verdict": "metric deformation; global clock map; one-point coframe strain; ad hoc BAO shift",
            "evidence": "all either hit SN/H(z)/local clocks or become a data-space patch",
        },
        {
            "item": "main_risk",
            "verdict": "derived_effective_bilocal_operator_or_closure_only",
            "evidence": "a bilocal kernel must emerge from coarse-grained parent theory, not be inserted by hand",
        },
        {
            "item": "claim_status",
            "verdict": CLAIM_CEILING,
            "evidence": "no bridge promotion; no CMB/local-GR claim; no parent action yet",
        },
        {
            "item": "next_target",
            "verdict": "163-effective-pair-action-owner-attempt.md",
            "evidence": "try to derive K^A_B and its zero marginal from a coarse-grained effective action/current",
        },
    ]


def run_contract(output_root: Path, timestamp: str | None) -> Path:
    run_stamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{run_stamp}-pair-ruler-operator-null-response-contract"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve())
    missing = [row["path"] for row in sources if row["exists"] != "yes"]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    conditions = operator_condition_rows()
    routes = route_audit_rows()
    responses = observable_response_rows()
    theorem_chain = theorem_chain_rows()
    gates = gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "sha256", "role", "issue"])
    write_csv(
        results_dir / "operator_condition_contract.csv",
        conditions,
        ["condition", "formula", "required_for", "status", "failure_if_missing"],
    )
    write_csv(
        results_dir / "route_null_response_audit.csv",
        routes,
        ["route", "operator_type", "BAO_response", "SN_Hz_null", "status", "reason"],
    )
    write_csv(
        results_dir / "observable_response_matrix.csv",
        responses,
        ["observable", "symbol", "response_under_pair_kernel", "condition", "status", "remaining_test"],
    )
    write_csv(
        results_dir / "theorem_chain.csv",
        theorem_chain,
        ["step", "statement", "formula", "status", "failure_mode"],
    )
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status = {
        "status": STATUS,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "best_live_operator": "connected_bilocal_pair_kernel_with_zero_one_point_marginal",
        "conditional_null_formula": "delta O_1 proportional to integral_D K = 0; delta O_2 proportional to K(x,y) != 0",
        "generated": [
            "source_register.csv",
            "operator_condition_contract.csv",
            "route_null_response_audit.csv",
            "observable_response_matrix.csv",
            "theorem_chain.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "163-effective-pair-action-owner-attempt.md",
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
    print(run_contract(args.output_root, args.timestamp))


if __name__ == "__main__":
    main()

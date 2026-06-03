#!/usr/bin/env python3
"""Consolidate the locked-memory branch into one claim-controlled contract."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"
AMPLITUDE_RUN = RUNS_ROOT / "20260531-204500-boundary-charge-amplitude-decision-gate"
AMPLITUDE_RESULTS = AMPLITUDE_RUN / "results"

CLAIM_CEILING = "locked_memory_empirical_EFT_closure_with_conditional_theory_mechanics"


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


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


def source_register_rows(script_path: Path, amplitude_run: Path) -> list[dict[str, Any]]:
    amplitude_results = amplitude_run / "results"
    paths = [
        script_path,
        WORK_DIR / "130-growth-route-gate.md",
        WORK_DIR / "134-subhorizon-suppressed-growth-correction-gate.md",
        WORK_DIR / "135-high-sound-speed-or-auxiliary-memory-owner.md",
        WORK_DIR / "138-coherent-volume-pressure-kernel-theorem.md",
        WORK_DIR / "139-density-law-hazard-theorem-attempt.md",
        WORK_DIR / "140-boundary-charge-amplitude-decision-gate.md",
        amplitude_run / "status.json",
        amplitude_results / "factor_ownership_ledger.csv",
        amplitude_results / "gate_results.csv",
        amplitude_results / "decision.csv",
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


def branch_equation_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "coherent_volume_time",
            "equation": "N_D = (1/3) ln(V_D0/V_D)",
            "status": "conditional_theory_route",
            "owner_or_evidence": "coherent-volume metric variation",
            "claim_allowed": "allowed_as_conditional",
            "missing_for_promotion": "derive domain selector D and boundary variation",
        },
        {
            "object": "activation_exposure",
            "equation": "I_M = det(Q), Q^i_j = X delta^i_j, X=N_D/u3",
            "status": "conditional_theory_route",
            "owner_or_evidence": "spatial determinant / 3+1 cell contracts",
            "claim_allowed": "allowed_as_theorem_target",
            "missing_for_promotion": "derive Q^i_j and u3=1/4 from parent action",
        },
        {
            "object": "activation_shape",
            "equation": "A = 1 - exp(-I_M)",
            "status": "conditional_theory_route",
            "owner_or_evidence": "additive hazard / survival composition",
            "claim_allowed": "allowed_as_conditional",
            "missing_for_promotion": "derive additive independent increments of memory exposure",
        },
        {
            "object": "memory_density",
            "equation": "rho_M = rho_Lambda + B_mem A",
            "status": "EFT_closure_with_conditional_shape",
            "owner_or_evidence": "hazard shape plus empirical amplitude",
            "claim_allowed": "allowed_as_closure",
            "missing_for_promotion": "derive B_mem=2/27",
        },
        {
            "object": "memory_pressure",
            "equation": "p_M = -rho_M + (1/3) d rho_M/dN_D",
            "status": "conditional_theory_route",
            "owner_or_evidence": "spatial metric variation of coherent volume",
            "claim_allowed": "allowed_as_conditional",
            "missing_for_promotion": "derive D/J_rel and full stress variation",
        },
        {
            "object": "amplitude",
            "equation": "B_mem = 2/27",
            "status": "empirical_locked_closure",
            "owner_or_evidence": "fixed-amplitude robustness, not parent theorem",
            "claim_allowed": "allowed_as_frozen_empirical_branch",
            "missing_for_promotion": "derive normalized boundary charge DeltaR=2/9 and projection DeltaR/3",
        },
        {
            "object": "effective_growth_owner",
            "equation": "canonical/high-sound-speed memory scalar can own late-time subhorizon stress",
            "status": "effective_EFT_support",
            "owner_or_evidence": "checkpoint 135 reconstruction and checkpoint 134 suppression bound",
            "claim_allowed": "allowed_as_late_time_subhorizon_EFT",
            "missing_for_promotion": "derive full perturbation action, lensing, CMB transfer, and local silence",
        },
    ]


def status_stack_rows() -> list[dict[str, Any]]:
    return [
        {
            "layer": "empirical",
            "status": "promising_locked_closure",
            "what_can_be_said": "B_mem=2/27 is a predeclared frozen branch that has survived several late-time checks",
            "what_cannot_be_said": "not a derived prediction and not a public support claim",
        },
        {
            "layer": "background_EFT",
            "status": "stronger_than_before",
            "what_can_be_said": "pressure and activation shape now have conditional mechanics",
            "what_cannot_be_said": "not a complete parent action",
        },
        {
            "layer": "perturbations",
            "status": "effective_subhorizon_only",
            "what_can_be_said": "late-time SDSS/eBOSS corrections are tiny under high-sound-speed owner",
            "what_cannot_be_said": "not CMB perturbation theory and not full growth/lensing derivation",
        },
        {
            "layer": "local_GR",
            "status": "open",
            "what_can_be_said": "local silence has sharp conditions N_D=0, delta N_D=0, F=0, delta F=0",
            "what_cannot_be_said": "not PPN-derived and not GR-reduction theorem",
        },
        {
            "layer": "parent_field_theory",
            "status": "not_achieved",
            "what_can_be_said": "there is a well-defined contract of required parent objects",
            "what_cannot_be_said": "not a unified field theory yet",
        },
    ]


def promotion_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement": "domain_owner",
            "must_prove": "D is selected by parent action, not smoothing choice",
            "current_status": "open",
            "promotion_gate": "derive D/J_rel and no wall stress",
        },
        {
            "requirement": "load_tensor_owner",
            "must_prove": "Q^i_j exists before FLRW and reduces to X delta^i_j",
            "current_status": "conditional",
            "promotion_gate": "derive Q from motion/time/space fields or constraints",
        },
        {
            "requirement": "u3_owner",
            "must_prove": "u3=1/4 follows from a 3+1 cell while exposure remains spatial cubic",
            "current_status": "conditional",
            "promotion_gate": "derive clock/spatial split from action",
        },
        {
            "requirement": "amplitude_owner",
            "must_prove": "B_mem=2/27 from normalized boundary charge",
            "current_status": "fail_not_derived",
            "promotion_gate": "derive endpoint quadratic and arrow before data",
        },
        {
            "requirement": "stress_owner",
            "must_prove": "full T_M^munu or geometric E_M^munu is conserved and locally silent",
            "current_status": "partial_EFT",
            "promotion_gate": "vary parent action and prove Bianchi/local PPN conditions",
        },
        {
            "requirement": "perturbation_owner",
            "must_prove": "mu, slip, sound speed, source terms for growth/CMB/lensing",
            "current_status": "late_subhorizon_proxy_only",
            "promotion_gate": "implement full perturbation equations and compare to baselines",
        },
    ]


def allowed_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test_arena": "SN_BAO_background",
            "allowed_branch": "locked B_mem=2/27 background closure",
            "allowed_claim": "competitive empirical closure branch",
            "forbidden_claim": "parent amplitude prediction",
        },
        {
            "test_arena": "BAO_Hz_noCMB",
            "allowed_branch": "locked background radial expansion",
            "allowed_claim": "late-time radial draw/preference test",
            "forbidden_claim": "CMB compatibility or full cosmology solved",
        },
        {
            "test_arena": "growth_fsigma8",
            "allowed_branch": "GR proxy / high-sound-speed EFT target",
            "allowed_claim": "late-time subhorizon effective stress check",
            "forbidden_claim": "derived MTS perturbation theory",
        },
        {
            "test_arena": "CMB_distance",
            "allowed_branch": "compressed background stress only",
            "allowed_claim": "distance-prior stress/draw diagnostic",
            "forbidden_claim": "passes CMB or perturbations",
        },
        {
            "test_arena": "local_PPN",
            "allowed_branch": "conditions ledger only until derived",
            "allowed_claim": "local silence target",
            "forbidden_claim": "derived local GR",
        },
    ]


def claim_control_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "MTS derives B_mem=2/27",
            "status": "forbidden",
            "replacement": "B_mem=2/27 is a frozen empirical closure and boundary-charge theorem target",
        },
        {
            "claim": "MTS derives the activation shape",
            "status": "too_strong",
            "replacement": "activation shape is conditionally derived if memory exposure is additive hazard",
        },
        {
            "claim": "MTS derives pressure",
            "status": "too_strong",
            "replacement": "pressure kernel follows conditionally from coherent-volume metric variation",
        },
        {
            "claim": "MTS has derived local GR",
            "status": "forbidden",
            "replacement": "local silence/PPN remains an open promotion gate",
        },
        {
            "claim": "MTS has a serious testable EFT closure branch",
            "status": "allowed_internal",
            "replacement": "use only with explicit caveats: empirical amplitude, conditional mechanics, no public support claim",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass",
            "evidence": "source register was checked before outputs were written",
        },
        {
            "gate": "branch_equations_consolidated",
            "status": "pass",
            "evidence": "equation ledger separates conditional theory routes from empirical closure",
        },
        {
            "gate": "amplitude_overclaim_blocked",
            "status": "pass",
            "evidence": "B_mem=2/27 is marked empirical_locked_closure, not theorem",
        },
        {
            "gate": "test_claims_limited",
            "status": "pass",
            "evidence": "allowed-test ledger defines claims and forbidden promotions",
        },
        {
            "gate": "parent_field_theory_complete",
            "status": "fail",
            "evidence": "domain, load tensor, amplitude, local GR, and perturbation owners remain incomplete",
        },
        {
            "gate": "next_work_defined",
            "status": "pass",
            "evidence": "promotion requirements identify domain/load/amplitude/stress/perturbation gates",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "status",
            "verdict": "locked_memory_branch_consolidated_as_empirical_EFT_closure",
            "evidence": "conditional mechanics retained; amplitude and parent field theory not promoted",
        },
        {
            "item": "claim_ceiling",
            "verdict": CLAIM_CEILING,
            "evidence": "use this ceiling for future writeups and tests",
        },
        {
            "item": "next_target",
            "verdict": "choose_next_promotion_gate_or_empirical_holdout",
            "evidence": "either attack domain/load tensor owner or run frozen-branch holdout tests with strict claim limits",
        },
    ]


def run_audit(output_root: Path, timestamp: str | None = None, amplitude_run: Path = AMPLITUDE_RUN) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-consolidated-locked-memory-branch-contract"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve(), amplitude_run)
    missing = [row["path"] for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    amplitude_status = read_json(amplitude_run / "status.json")
    factor_rows = read_csv_rows(amplitude_run / "results" / "factor_ownership_ledger.csv")

    branch_equations = branch_equation_rows()
    status_stack = status_stack_rows()
    promotion_requirements = promotion_requirement_rows()
    allowed_tests = allowed_test_rows()
    claim_controls = claim_control_rows()
    gates = gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "issue"])
    write_csv(results_dir / "branch_equation_contract.csv", branch_equations, ["object", "equation", "status", "owner_or_evidence", "claim_allowed", "missing_for_promotion"])
    write_csv(results_dir / "status_stack.csv", status_stack, ["layer", "status", "what_can_be_said", "what_cannot_be_said"])
    write_csv(results_dir / "promotion_requirements.csv", promotion_requirements, ["requirement", "must_prove", "current_status", "promotion_gate"])
    write_csv(results_dir / "allowed_test_matrix.csv", allowed_tests, ["test_arena", "allowed_branch", "allowed_claim", "forbidden_claim"])
    write_csv(results_dir / "claim_control_ledger.csv", claim_controls, ["claim", "status", "replacement"])
    write_csv(results_dir / "input_factor_ownership_ledger.csv", factor_rows, ["factor", "target", "current_owner", "status", "what_is_missing"])
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "input_status": amplitude_status["status"],
        "generated": [
            "source_register.csv",
            "branch_equation_contract.csv",
            "status_stack.csv",
            "promotion_requirements.csv",
            "allowed_test_matrix.csv",
            "claim_control_ledger.csv",
            "input_factor_ownership_ledger.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "choose_domain_load_tensor_promotion_gate_or_frozen_branch_holdout",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--amplitude-run", type=Path, default=AMPLITUDE_RUN)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_audit(args.output_root, args.timestamp, args.amplitude_run))


if __name__ == "__main__":
    main()

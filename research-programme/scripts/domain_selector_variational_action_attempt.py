#!/usr/bin/env python3
"""Attempt a zero-knob variational owner for the coherent domain selector."""

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
DOMAIN_LOAD_RUN = RUNS_ROOT / "20260531-211500-domain-load-tensor-owner-promotion-gate"
DOMAIN_LOAD_RESULTS = DOMAIN_LOAD_RUN / "results"

CLAIM_CEILING = "domain_selector_formal_action_not_parent_derived"


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


def source_register_rows(script_path: Path, domain_load_run: Path) -> list[dict[str, Any]]:
    domain_results = domain_load_run / "results"
    paths = [
        script_path,
        WORK_DIR / "64-binding-invariant-domain-selector-attempt.md",
        WORK_DIR / "65-Ccoh-phase-field-selector-attempt.md",
        WORK_DIR / "66-chiD-stress-and-scale-gate.md",
        WORK_DIR / "67-auxiliary-selector-parent-contract.md",
        WORK_DIR / "68-chiD-gated-memory-conservation-contract.md",
        WORK_DIR / "70-Ccoh-variation-and-boundary-current-audit.md",
        WORK_DIR / "71-relative-boundary-current-construction-attempt.md",
        WORK_DIR / "72-relative-current-action-owner-attempt.md",
        WORK_DIR / "142-domain-load-tensor-owner-promotion-gate.md",
        domain_load_run / "status.json",
        domain_results / "domain_selector_candidates.csv",
        domain_results / "phase_field_action_contract.csv",
        domain_results / "gate_results.csv",
        domain_results / "decision.csv",
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


def action_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "dynamic_phase_field_selector",
            "action_sketch": "S_chi=-rho_chi/2 integral sqrt(-g)[ell_chi^2 (nabla chi)^2 + (chi-C_coh)^2]",
            "selects_D": "partial",
            "zero_knob_status": "fail",
            "stress_status": "fail_open",
            "boundary_status": "open",
            "verdict": "rejected_for_promotion_due_to_scale_and_stress",
        },
        {
            "candidate": "algebraic_Ccoh_multiplier",
            "action_sketch": "S_aux=integral sqrt(-g) lambda_chi(chi_D-C_coh[D])",
            "selects_D": "no_selects_chi_given_D",
            "zero_knob_status": "pass_for_chi_not_D",
            "stress_status": "pass_conditional_if_memory_uncoupled_or_total_action_varied",
            "boundary_status": "fail_open",
            "verdict": "clean_selector_not_domain_owner",
        },
        {
            "candidate": "coherence_extremal_domain",
            "action_sketch": "choose D by delta_D C_coh[D]=0 plus maximal connected stable-sign rule",
            "selects_D": "formal",
            "zero_knob_status": "partial",
            "stress_status": "not_direct_field_stress",
            "boundary_status": "fail_open",
            "verdict": "best_domain_contract_not_local_action",
        },
        {
            "candidate": "auxiliary_domain_multiplier",
            "action_sketch": "S_D=<Lambda_D, E_D[C_coh,theta,sigma,omega]> with E_D=0 selecting extremal coherent domains",
            "selects_D": "formal",
            "zero_knob_status": "open",
            "stress_status": "pass_only_if_multiplier_stress_is_topological_or_exact",
            "boundary_status": "open",
            "verdict": "theorem_target_not_derived",
        },
        {
            "candidate": "relative_current_selector",
            "action_sketch": "S_rel=<Lambda_rel,d_rel J_rel> + boundary polarization from coherent expansion class",
            "selects_D": "no_selects_closure_not_representative",
            "zero_knob_status": "partial",
            "stress_status": "pass_conditional_if_topological",
            "boundary_status": "best_support",
            "verdict": "conservation_support_not_selector",
        },
        {
            "candidate": "external_threshold_selector",
            "action_sketch": "chi_D=Heaviside(C_coh-C_star)",
            "selects_D": "yes_by_threshold",
            "zero_knob_status": "fail",
            "stress_status": "not_action_owned",
            "boundary_status": "uncontrolled",
            "verdict": "rejected_rescue_knob",
        },
    ]


def variation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": "define_coherence_invariant",
            "equation": "C_coh[D]=<theta>_D^2/(<theta^2>_D+<sigma^2>_D+<omega^2>_D+eps_D)",
            "status": "available",
            "meaning": "distinguishes coherent expansion from shear/virial motion",
            "blocker": "eps_D and averaging domain must be parent-owned",
        },
        {
            "step": "algebraic_selector",
            "equation": "delta_lambda S=0 -> chi_D=C_coh[D]",
            "status": "pass_formal",
            "meaning": "no independent propagating chi field is required",
            "blocker": "D is still assumed",
        },
        {
            "step": "domain_variation",
            "equation": "delta_D C_coh[D]=bulk_terms + boundary_terms",
            "status": "required",
            "meaning": "domain selection must come from extremality or topology",
            "blocker": "boundary terms are not parent-owned",
        },
        {
            "step": "relative_current_closure",
            "equation": "d_rel(j_3,b_2)=0",
            "status": "pass_formal",
            "meaning": "can encode local trivial and FLRW nontrivial classes",
            "blocker": "does not select physical representative",
        },
        {
            "step": "maximality",
            "equation": "D=max connected domain satisfying coherence/stable-sign condition",
            "status": "contract",
            "meaning": "prevents tiny hand-picked domains",
            "blocker": "global maximality is not yet a local covariant Euler equation",
        },
        {
            "step": "stress_and_bianchi",
            "equation": "nabla_mu(T_mem+T_aux+T_boundary+T_matter)^munu=0",
            "status": "open",
            "meaning": "selector cannot be an external switch",
            "blocker": "C_coh and D variations must enter the Noether identity",
        },
    ]


def zero_knob_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "no_empirical_threshold",
            "status": "pass_for_Ccoh_contract",
            "evidence": "C_coh uses a ratio; no C_star threshold is required in the best contract",
        },
        {
            "test": "no_transition_length",
            "status": "fail_for_dynamic_phase_field_pass_for_auxiliary",
            "evidence": "dynamic chi introduces ell_chi; auxiliary chi avoids it but does not select D",
        },
        {
            "test": "no_selector_stress",
            "status": "pass_conditional_for_auxiliary_fail_for_dynamic",
            "evidence": "algebraic selector has no kinetic stress, but memory-coupled multiplier stress remains in total action",
        },
        {
            "test": "domain_not_chosen_by_outcome",
            "status": "partial",
            "evidence": "maximal coherent volume-flow rule is pre-data, but not parent-action derived",
        },
        {
            "test": "boundary_not_hand_tuned",
            "status": "fail_open",
            "evidence": "J_rel closure is formal; physical representative and boundary exchange are not selected",
        },
        {
            "test": "local_GR_not_imported",
            "status": "partial",
            "evidence": "C_coh avoids Newtonian binding/GR turnaround, but virial domain interpretation still risks importing lower-limit theory",
        },
    ]


def branch_readout_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "FLRW",
            "Ccoh": "1",
            "selector_result": "chi_D=1 and coherent domain active",
            "status": "pass_conditional",
            "risk": "homogeneous domain must be selected by parent rule",
        },
        {
            "branch": "Minkowski_or_stationary_local",
            "Ccoh": "0_or_low",
            "selector_result": "chi_D low and memory off",
            "status": "pass_conditional",
            "risk": "local domain selection and boundary stress not derived",
        },
        {
            "branch": "tracefree_shear",
            "Ccoh": "0",
            "selector_result": "chi_D=0 for scalar volume-memory channel",
            "status": "pass_conditional",
            "risk": "second-order shear/boundary terms not derived",
        },
        {
            "branch": "virialized_bound_system",
            "Ccoh": "time_averaged_low",
            "selector_result": "memory suppressed if stable volume domain is selected",
            "status": "open_conditional",
            "risk": "bound-domain rule may smuggle in Newton/GR",
        },
        {
            "branch": "collapse_or_merger",
            "Ccoh": "mixed_or_nonzero",
            "selector_result": "domain may become active",
            "status": "open_risk",
            "risk": "not PPN-safe until dynamic boundary response is derived",
        },
    ]


def boundary_stress_rows() -> list[dict[str, Any]]:
    return [
        {
            "source": "dynamic_phase_field_wall",
            "risk": "surface tension from chi gradient",
            "status": "rejected_for_promotion",
            "needed_fix": "remove kinetic wall or derive microscopic/topological stress suppression",
        },
        {
            "source": "algebraic_multiplier_boundary",
            "risk": "lambda_chi delta_g C_coh terms after memory coupling",
            "status": "open",
            "needed_fix": "derive total Noether identity including D variation",
        },
        {
            "source": "relative_current_representative",
            "risk": "closed current exists but physical representative not selected",
            "status": "open",
            "needed_fix": "derive local trivial / FLRW nontrivial representative from action",
        },
        {
            "source": "moving_domain_average",
            "risk": "delta_D <theta>_D creates boundary exchange",
            "status": "open",
            "needed_fix": "J_rel or equivalent boundary current must absorb exchange without wall stress",
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
            "gate": "dynamic_phase_field_promoted",
            "status": "fail",
            "evidence": "ell_chi and T_chi remain new scale/stress risks",
        },
        {
            "gate": "auxiliary_selector_safe",
            "status": "pass_conditional",
            "evidence": "chi_D=C_coh can be imposed without independent kinetic stress",
        },
        {
            "gate": "domain_selected_by_action",
            "status": "fail",
            "evidence": "no zero-knob Euler equation selects D; maximal coherent domain remains a contract",
        },
        {
            "gate": "boundary_exchange_owned",
            "status": "fail_open",
            "evidence": "relative current closure exists but representative/exchange current not parent-derived",
        },
        {
            "gate": "FLRW_local_split",
            "status": "pass_conditional",
            "evidence": "C_coh separates ideal FLRW from quiet local domains",
        },
        {
            "gate": "dynamic_local_safety",
            "status": "open_risk",
            "evidence": "collapse, mergers, and moving boundaries can activate selector response",
        },
        {
            "gate": "domain_promotion",
            "status": "fail",
            "evidence": "D remains closure-level; memory branch not promoted beyond EFT closure",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "item": "status",
            "verdict": "zero_knob_domain_selector_not_derived_auxiliary_contract_retained",
            "evidence": "auxiliary selector avoids scalar stress, but no parent action selects D and boundary representative",
        },
        {
            "item": "best_live_route",
            "verdict": "auxiliary_Ccoh_selector_plus_relative_boundary_current",
            "evidence": "best route avoids dynamic chi stress while keeping conservation bookkeeping explicit",
        },
        {
            "item": "demotion_condition",
            "verdict": "domain_remains_coarse_graining_closure_until_boundary_owner_exists",
            "evidence": "without D/J_rel action owner, local silence is conditional rather than derived",
        },
        {
            "item": "next_target",
            "verdict": "boundary_exchange_or_empirical_holdout",
            "evidence": "either derive J_rel representative/exchange or pause theory route and run frozen empirical holdouts",
        },
    ]


def run_audit(output_root: Path, timestamp: str | None = None, domain_load_run: Path = DOMAIN_LOAD_RUN) -> Path:
    timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-domain-selector-variational-action-attempt"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(Path(__file__).resolve(), domain_load_run)
    missing = [row["path"] for row in sources if not row["exists"]]
    if missing:
        raise FileNotFoundError(f"missing required source files: {missing}")

    domain_status = read_json(domain_load_run / "status.json")
    domain_candidates = read_csv_rows(domain_load_run / "results" / "domain_selector_candidates.csv")

    actions = action_candidate_rows()
    variation = variation_chain_rows()
    zero_knob = zero_knob_test_rows()
    branch_readout = branch_readout_rows()
    boundary = boundary_stress_rows()
    gates = gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_register.csv", sources, ["source", "path", "exists", "issue"])
    write_csv(results_dir / "action_candidate_ledger.csv", actions, ["candidate", "action_sketch", "selects_D", "zero_knob_status", "stress_status", "boundary_status", "verdict"])
    write_csv(results_dir / "variation_chain.csv", variation, ["step", "equation", "status", "meaning", "blocker"])
    write_csv(results_dir / "zero_knob_tests.csv", zero_knob, ["test", "status", "evidence"])
    write_csv(results_dir / "branch_readout.csv", branch_readout, ["branch", "Ccoh", "selector_result", "status", "risk"])
    write_csv(results_dir / "boundary_stress_ledger.csv", boundary, ["source", "risk", "status", "needed_fix"])
    write_csv(results_dir / "input_domain_selector_candidates.csv", domain_candidates, ["candidate", "definition", "FLRW", "local_silence", "noncircularity", "verdict"])
    write_csv(results_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(results_dir / "decision.csv", decisions, ["item", "verdict", "evidence"])

    status_value = next(row["verdict"] for row in decisions if row["item"] == "status")
    status = {
        "status": status_value,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "claim_ceiling": CLAIM_CEILING,
        "input_status": domain_status["status"],
        "generated": [
            "source_register.csv",
            "action_candidate_ledger.csv",
            "variation_chain.csv",
            "zero_knob_tests.csv",
            "branch_readout.csv",
            "boundary_stress_ledger.csv",
            "input_domain_selector_candidates.csv",
            "gate_results.csv",
            "decision.csv",
        ],
        "next_target": "derive_boundary_exchange_representative_or_run_frozen_holdout",
    }
    write_json(run_dir / "status.json", status)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=RUNS_ROOT)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--domain-load-run", type=Path, default=DOMAIN_LOAD_RUN)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(run_audit(args.output_root, args.timestamp, args.domain_load_run))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "parent-Hamiltonian-trace-current-gate"
STATUS = "Hamiltonian_trace_current_unit_inheritance_conditional_lambda_rescaling_no_go_blocks_promotion"
CLAIM_CEILING = "parent_Hamiltonian_trace_current_contract_no_Bmem_or_local_GR_promotion"
LOCKED_B_MEM = Fraction(2, 27)
SOURCE_331 = ROOT / "runs" / "20260601-181000-trace-normalized-Hamiltonian-amplitude-contract" / "results"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "19-constrained-parent-action-skeleton.md", "early constrained parent-action skeleton"),
        (ROOT / "207-domain-projector-action-and-Bianchi-identity.md", "domain projector variational/Bianchi warning"),
        (ROOT / "252-topological-projector-parent-action-skeleton.md", "topological projector parent-action skeleton"),
        (ROOT / "253-FLRW-reduction-of-topological-projector-or-Bmem-stays-closure.md", "FLRW reduction and Bmem rank target"),
        (ROOT / "260-C3-unit-stress-normalization-parent-action-attempt.md", "C3a/C3b split"),
        (ROOT / "261-Hstar-H0-scale-lock-and-local-silence-attempt.md", "Hstar/H0 scale-lock identity"),
        (ROOT / "262-boundary-Noether-scale-lock-attempt.md", "Noether/boundary scale-lock no-go"),
        (ROOT / "331-trace-normalized-Hamiltonian-amplitude-contract.md", "latest amplitude factorization checkpoint"),
        (SOURCE_331 / "release_split_amplitude_summary.csv", "331 release-split kappa corridor"),
        (SOURCE_331 / "theorem_factorization.csv", "331 theorem factors"),
        (SOURCE_331 / "gate_results.csv", "331 gate results"),
        (Path(__file__).resolve(), "this verifier"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": path.exists(),
            "issue": "" if path.exists() else "missing",
        }
        for path, role in sources
    ]


def candidate_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "projected_EH_Hamiltonian_subblock",
            "schematic_action": "S_mem is not added; it is the P_active trace of the already-normalized Hamiltonian constraint density",
            "epsilon_H_result": "epsilon_H=1 if the parent proves literal inheritance",
            "status": "conditional_best_route",
            "failure_mode": "if S_mem has its own coefficient, the coefficient is kappa_mem",
        },
        {
            "route": "added_FLRW_memory_potential",
            "schematic_action": "S_mem=-int N a^3 lambda_mem 3 M_Pl^2 H_star^2 q_trace F(N)",
            "epsilon_H_result": "epsilon_H=lambda_mem",
            "status": "fails_as_derivation",
            "failure_mode": "diffeomorphism/Bianchi consistency survives for any lambda_mem",
        },
        {
            "route": "Noether_or_Dirac_closure_only",
            "schematic_action": "memory term is separately covariant or separately first-class",
            "epsilon_H_result": "coefficient remains free under rescaling",
            "status": "fails_to_select_number",
            "failure_mode": "closure/conservation preserve equations but do not choose unit normalization",
        },
        {
            "route": "topological_BF_projector",
            "schematic_action": "int Xi wedge d_rel J + int Upsilon wedge(P_D J-d_rel A)",
            "epsilon_H_result": "no bulk stress amplitude by itself",
            "status": "supports_projector_not_amplitude",
            "failure_mode": "topological ownership can silence local projector stress without creating rho_c0 units",
        },
        {
            "route": "multiplier_sets_lambda_one",
            "schematic_action": "int mu(lambda_mem-1)",
            "epsilon_H_result": "epsilon_H=1 by constraint",
            "status": "imposition_not_derivation",
            "failure_mode": "the new constraint must itself be parent-owned or it is just the closure in disguise",
        },
        {
            "route": "unit_choice_or_renormalization",
            "schematic_action": "define H_star or q_trace so that lambda_mem is absorbed",
            "epsilon_H_result": "notation hides the free factor",
            "status": "rejected",
            "failure_mode": "observable kappa_mem reappears in B_mem",
        },
    ]


def conditional_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "H1_same_lapse_generator",
            "required_statement": "memory current is varied by the same lapse Hamiltonian constraint as the EH/FLRW background",
            "current_status": "not_parent_derived",
            "why_needed": "prevents a separate clock or independent memory Hamiltonian",
        },
        {
            "condition": "H2_literal_subblock_inheritance",
            "required_statement": "S_mem is the P_active trace component of the parent Hamiltonian current, not an added potential",
            "current_status": "missing_core_theorem",
            "why_needed": "this is the only route found that can forbid lambda_mem",
        },
        {
            "condition": "H3_canonical_trace_measure",
            "required_statement": "Tr(P_active)/dim(V_cell) is computed with the parent finite-cell trace measure",
            "current_status": "conditional_from_rank_contract",
            "why_needed": "prevents q_trace from being a hand normalization",
        },
        {
            "condition": "H4_no_independent_coupling_by_symmetry",
            "required_statement": "a parent gauge/quotient principle forbids lambda_mem P_active H as an independent invariant",
            "current_status": "not_derived",
            "why_needed": "diffeomorphism invariance alone allows lambda_mem",
        },
        {
            "condition": "H5_scale_lock",
            "required_statement": "H_star=H0 or equivalent boundary scale-lock is derived separately",
            "current_status": "closure_locked_from_261_262",
            "why_needed": "otherwise epsilon_H=1 still leaves B_mem=q_trace(H_star/H0)^2",
        },
        {
            "condition": "H6_projector_local_silence",
            "required_statement": "the same P_D/P_active is metric-independent/topological in local exterior reductions",
            "current_status": "conditional_from_252",
            "why_needed": "avoids buying the amplitude at the cost of local projector stress",
        },
        {
            "condition": "H7_total_Bianchi_accounting",
            "required_statement": "all projector/domain/boundary stresses are retained so total stress is conserved",
            "current_status": "conditional_from_207",
            "why_needed": "prevents hidden external forces from faking conservation",
        },
    ]


def release_corridor_rows() -> list[dict[str, Any]]:
    rows = read_csv(SOURCE_331 / "release_split_amplitude_summary.csv")
    corridor: list[dict[str, Any]] = []
    for row in rows:
        kappa = float(row["kappa_fit"])
        corridor.append(
            {
                "release": row["release"],
                "kappa_fit": kappa,
                "epsilon_H_if_Hstar_equals_H0": kappa,
                "Hstar_over_H0_if_epsilon_H_equals_1": math.sqrt(kappa),
                "abs_kappa_minus_1": abs(kappa - 1.0),
                "locked_minus_fitted_chi2": float(row["locked_minus_fitted_chi2"]),
                "locked_minus_fitted_BIC": float(row["locked_minus_fitted_BIC"]),
                "interpretation": "private empirical target corridor only; not a parent theorem",
            }
        )
    return corridor


def lambda_rescaling_rows() -> list[dict[str, Any]]:
    locked = float(LOCKED_B_MEM)
    lambdas = [0.5, 0.991149235153442, 1.0, 1.0061980866083466, 2.0]
    return [
        {
            "lambda_mem": value,
            "B_mem": locked * value,
            "B_mem_over_locked": value,
            "Bianchi_status": "still_formally_conserved_if_pressure_scales",
            "Dirac_Noether_status": "not_fixed_by_symmetry_without_literal_subblock_inheritance",
            "meaning": "lambda rescales amplitude while preserving the formal stress route",
        }
        for value in lambdas
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma": "diffeomorphism_invariance_not_selection",
            "statement": "a covariant scalar memory density can be multiplied by lambda_mem and remain covariant",
            "consequence": "Noether/Bianchi identities cannot choose epsilon_H=1",
        },
        {
            "lemma": "constraint_algebra_homogeneity",
            "statement": "if the memory term is separately first-class, rescaling its coefficient preserves formal closure",
            "consequence": "Dirac closure alone is too weak to set the coefficient",
        },
        {
            "lemma": "topological_stress_silence_not_stress_units",
            "statement": "wedge/relative-chain terms can have zero bulk metric variation",
            "consequence": "they can own P_D locally but cannot by themselves set rho_mem/rho_c0",
        },
        {
            "lemma": "subblock_inheritance_or_closure",
            "statement": "unit normalization follows only if memory is a projected subblock of an already-normalized Hamiltonian current",
            "consequence": "this becomes the exact parent-action theorem target",
        },
    ]


def gate_rows(sources: list[dict[str, Any]], corridor: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(bool(row["exists"]) for row in sources)
    max_kappa_shift = max(float(row["abs_kappa_minus_1"]) for row in corridor)
    locked_bic_preferred = all(float(row["locked_minus_fitted_BIC"]) < 0.0 for row in corridor)
    return [
        {"gate": "source_paths_exist", "status": "pass" if sources_ok else "fail", "evidence": sources_ok},
        {
            "gate": "post_331_kappa_corridor_imported",
            "status": "pass" if max_kappa_shift < 0.01 else "fail",
            "evidence": max_kappa_shift,
        },
        {
            "gate": "locked_branch_beats_kappa_free_by_BIC",
            "status": "pass" if locked_bic_preferred else "fail",
            "evidence": locked_bic_preferred,
        },
        {
            "gate": "unit_inheritance_route_written",
            "status": "pass",
            "evidence": "epsilon_H=1 follows conditionally only from literal projected-Hamiltonian subblock inheritance",
        },
        {
            "gate": "lambda_rescaling_counterexample",
            "status": "pass",
            "evidence": "covariant stress route survives lambda_mem rescaling",
        },
        {
            "gate": "Noether_or_Bianchi_selects_unit_coefficient",
            "status": "fail",
            "evidence": "conservation/closure is homogeneous in lambda_mem",
        },
        {
            "gate": "literal_parent_subblock_inheritance_derived",
            "status": "fail",
            "evidence": "no parent Hamiltonian trace-current construction yet",
        },
        {
            "gate": "epsilon_H_parent_derived",
            "status": "fail",
            "evidence": "unit coefficient remains conditional theorem target",
        },
        {
            "gate": "Bmem_parent_promotion_allowed",
            "status": "fail",
            "evidence": "Hstar and q_trace parent derivations also remain open",
        },
    ]


def decision_rows(corridor: list[dict[str, Any]]) -> list[dict[str, Any]]:
    kappa_values = [float(row["kappa_fit"]) for row in corridor]
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "kappa_fit_min": min(kappa_values),
            "kappa_fit_max": max(kappa_values),
            "meaning": (
                "A unit Hamiltonian trace-current theorem can be stated sharply: epsilon_H=1 follows if the memory "
                "term is literally the active trace subblock of the same already-normalized Hamiltonian constraint. "
                "However, every route that adds a separate covariant memory density admits lambda_mem rescaling, so "
                "Noether/Bianchi/Dirac consistency alone does not select the unit coefficient."
            ),
            "next_target": "construct_or_reject_literal_projected_Hamiltonian_subblock_from_parent_action",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    routes = candidate_route_rows()
    conditions = conditional_theorem_rows()
    corridor = release_corridor_rows()
    rescaling = lambda_rescaling_rows()
    no_go = no_go_rows()
    gates = gate_rows(sources, corridor)
    decisions = decision_rows(corridor)

    outputs = {
        "source_register.csv": (sources, ["source", "role", "exists", "issue"]),
        "candidate_routes.csv": (
            routes,
            ["route", "schematic_action", "epsilon_H_result", "status", "failure_mode"],
        ),
        "conditional_theorem_conditions.csv": (
            conditions,
            ["condition", "required_statement", "current_status", "why_needed"],
        ),
        "release_corridor.csv": (
            corridor,
            [
                "release",
                "kappa_fit",
                "epsilon_H_if_Hstar_equals_H0",
                "Hstar_over_H0_if_epsilon_H_equals_1",
                "abs_kappa_minus_1",
                "locked_minus_fitted_chi2",
                "locked_minus_fitted_BIC",
                "interpretation",
            ],
        ),
        "lambda_rescaling_counterexamples.csv": (
            rescaling,
            ["lambda_mem", "B_mem", "B_mem_over_locked", "Bianchi_status", "Dirac_Noether_status", "meaning"],
        ),
        "no_go_lemmas.csv": (no_go, ["lemma", "statement", "consequence"]),
        "gate_results.csv": (gates, ["gate", "status", "evidence"]),
        "decision.csv": (
            decisions,
            ["decision", "claim_ceiling", "kappa_fit_min", "kappa_fit_max", "meaning", "next_target"],
        ),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "epsilon_H_parent_derived": False,
        "unit_inheritance_route": "conditional_literal_projected_Hamiltonian_subblock",
        "lambda_rescaling_no_go": True,
        "promotion_allowed": False,
        "next_target": "construct_or_reject_literal_projected_Hamiltonian_subblock_from_parent_action",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parent Hamiltonian trace-current gate for epsilon_H=1.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

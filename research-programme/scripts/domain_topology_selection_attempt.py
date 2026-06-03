from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "domain-topology-selection-attempt"
STATUS = "coherent_domain_topology_selection_conditional_not_parent_derived"
CLAIM_CEILING = "conditional_B3_domain_theorem_only_no_Bmem_or_local_GR_promotion"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "276-coherent-domain-projector-from-parent-variables.md", "coherent domain projector and isotropic trace"),
        (ROOT / "277-domain-free-boundary-Euler-equation.md", "free-boundary equation degeneracy"),
        (ROOT / "278-admissible-domain-class-boundary-current-owner.md", "admissible domain class and boundary current owner"),
        (ROOT / "288-k9-Ward-index-level-attempt.md", "k=9 Ward/index target"),
        (ROOT / "292-relative-index-level-theorem-attempt.md", "conditional relative-index derivation of k=9"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def topology_candidate_rows() -> list[dict[str, Any]]:
    candidates = [
        {
            "domain": "B3_contractible_cell",
            "boundary": "S2",
            "boundary_components": 1,
            "betti_1": 0,
            "betti_2": 0,
            "so3_boundary": "yes",
            "single_scalar_mode": "yes",
            "chi_relative": -1,
            "relative_index_rank9": -9,
            "status": "target",
            "why": "unique minimal connected S2-boundary no-cycle cell",
        },
        {
            "domain": "solid_torus",
            "boundary": "T2",
            "boundary_components": 1,
            "betti_1": 1,
            "betti_2": 0,
            "so3_boundary": "no",
            "single_scalar_mode": "no",
            "chi_relative": 0,
            "relative_index_rank9": 0,
            "status": "rejected_by_isotropic_boundary_and_cycle_rule",
            "why": "contains a handle and torus boundary",
        },
        {
            "domain": "spherical_shell",
            "boundary": "S2_union_S2",
            "boundary_components": 2,
            "betti_1": 0,
            "betti_2": 1,
            "so3_boundary": "yes_each_component",
            "single_scalar_mode": "ambiguous_no",
            "chi_relative": -2,
            "relative_index_rank9": -18,
            "status": "rejected_by_single_boundary_and_no_internal_cavity",
            "why": "two S2 boundaries create a shell/cavity degree of freedom",
        },
        {
            "domain": "handlebody_genus_g",
            "boundary": "Sigma_g",
            "boundary_components": 1,
            "betti_1": "g",
            "betti_2": 0,
            "so3_boundary": "no_for_g_gt_0",
            "single_scalar_mode": "no",
            "chi_relative": "g-1",
            "relative_index_rank9": "9*(g-1)",
            "status": "rejected_unless_g0",
            "why": "nonzero handles are anisotropic/topological memory modes",
        },
        {
            "domain": "closed_3_domain",
            "boundary": "none",
            "boundary_components": 0,
            "betti_1": "model_dependent",
            "betti_2": "model_dependent",
            "so3_boundary": "not_applicable",
            "single_scalar_mode": "no_boundary_current",
            "chi_relative": 0,
            "relative_index_rank9": 0,
            "status": "rejected_for_boundary_current_route",
            "why": "no relative boundary source",
        },
    ]
    return candidates


def conditional_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "assumption": "compact_connected_oriented_3_domain",
            "parent_status": "reasonable_background_condition",
            "mathematical_role": "puts D in the class where relative cohomology and index are defined",
            "failure_if_absent": "index theorem route has no domain",
        },
        {
            "assumption": "single_connected_boundary",
            "parent_status": "not_derived",
            "mathematical_role": "rules out shell/cavity domains with index magnitude 18 or larger",
            "failure_if_absent": "multi-boundary domains change the level",
        },
        {
            "assumption": "SO3_isotropic_boundary",
            "parent_status": "conditional_from_FLRW_symmetry",
            "mathematical_role": "selects S2 rather than T2 or higher-genus boundary",
            "failure_if_absent": "handles/vortices become admissible",
        },
        {
            "assumption": "no_harmonic_1_or_2_modes",
            "parent_status": "not_parent_derived",
            "mathematical_role": "rules out internal cycle memory and cavity modes",
            "failure_if_absent": "topological sectors create extra unsilenced memory variables",
        },
        {
            "assumption": "irreducible_no_hidden_prime_factor",
            "parent_status": "not_parent_derived",
            "mathematical_role": "upgrades homology ball/S2-boundary to a genuine B3-type cell",
            "failure_if_absent": "exotic or knotted interiors can mimic simple homology",
        },
    ]


def variational_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "symmetry_only",
            "candidate_action_clause": "FLRW branch imposes SO(3) isotropy on boundary data",
            "what_it_derives": "S2 boundary shape",
            "what_it_does_not_derive": "single boundary component or absence of hidden cycles",
            "status": "partial",
        },
        {
            "route": "harmonic_mode_penalty",
            "candidate_action_clause": "positive terms for harmonic H1/H2 representatives",
            "what_it_derives": "zero active harmonic amplitudes",
            "what_it_does_not_derive": "topology itself; zero fields can live on nontrivial topology",
            "status": "insufficient",
        },
        {
            "route": "domain_complexity_penalty",
            "candidate_action_clause": "free-boundary action penalizes Betti numbers or boundary components",
            "what_it_derives": "B3 as minimal topology",
            "what_it_does_not_derive": "the penalty is inserted unless produced by parent measure/anomaly",
            "status": "closure_unless_parent_owned",
        },
        {
            "route": "relative_current_admissibility",
            "candidate_action_clause": "only domains with one nontrivial relative top class and no lower harmonic classes are admissible",
            "what_it_derives": "B3-like admissible class",
            "what_it_does_not_derive": "why admissibility is forced rather than declared",
            "status": "best_contract",
        },
        {
            "route": "local_silence_same_rule",
            "candidate_action_clause": "compact bound domains carry trivial measured periods while FLRW cell carries one top relative class",
            "what_it_derives": "possible bridge to local safety",
            "what_it_does_not_derive": "representative-selection law",
            "status": "open",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    source_missing = [source for source in source_register_rows() if source["exists"] != "yes"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not source_missing else "fail",
            "evidence": "all cited post-checkpoint sources exist" if not source_missing else ";".join(source["source"] for source in source_missing),
            "claim_effect": "audit traceable",
        },
        {
            "gate": "conditional_B3_theorem_formulated",
            "status": "pass",
            "evidence": "single S2 boundary plus no H1/H2 cycles plus irreducibility selects B3-type coherent cell",
            "claim_effect": "topology theorem target is precise",
        },
        {
            "gate": "FLRW_symmetry_selects_S2_boundary",
            "status": "conditional_pass",
            "evidence": "SO(3) isotropic compact boundary is S2-like",
            "claim_effect": "rules out torus/higher-genus boundary in the scalar FLRW branch",
        },
        {
            "gate": "single_boundary_component_derived",
            "status": "fail",
            "evidence": "parent action does not yet forbid shell/cavity domains",
            "claim_effect": "B3 selection remains conditional",
        },
        {
            "gate": "no_cycle_rule_derived",
            "status": "fail",
            "evidence": "no parent-owned penalty or admissibility theorem for H1/H2 cycles",
            "claim_effect": "topological memory sectors remain possible",
        },
        {
            "gate": "B3_domain_derived",
            "status": "fail",
            "evidence": "requires single boundary, no cycles, and irreducibility assumptions not yet parent-owned",
            "claim_effect": "relative-index k=9 remains conditional",
        },
        {
            "gate": "B_mem_derived",
            "status": "fail",
            "evidence": "even B3 would still need period normalization and endpoint law",
            "claim_effect": "locked empirical closure retained",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The coherent-domain topology route can be made mathematically sharp: an FLRW scalar memory cell "
                "with one S2 boundary, no H1/H2 harmonic cycle sectors, and irreducible interior is B3-like, "
                "which supplies chi(D,partial D)=-1 for the relative-index k=9 route. But the parent action has not "
                "yet derived single-boundary selection, no-cycle admissibility, or irreducibility."
            ),
            "next_target": "derive_no_cycle_admissibility_or_endpoint_occupancy_arrow",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "topology_candidates.csv": (
            topology_candidate_rows(),
            [
                "domain",
                "boundary",
                "boundary_components",
                "betti_1",
                "betti_2",
                "so3_boundary",
                "single_scalar_mode",
                "chi_relative",
                "relative_index_rank9",
                "status",
                "why",
            ],
        ),
        "conditional_theorem_assumptions.csv": (
            conditional_theorem_rows(),
            ["assumption", "parent_status", "mathematical_role", "failure_if_absent"],
        ),
        "variational_routes.csv": (
            variational_route_rows(),
            ["route", "candidate_action_clause", "what_it_derives", "what_it_does_not_derive", "status"],
        ),
        "gate_results.csv": (
            gate_rows(),
            ["gate", "status", "evidence", "claim_effect"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "meaning", "next_target"],
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
        "B3_domain_derived_now": False,
        "relative_index_k9_still_conditional": True,
        "B_mem_derived_now": False,
        "local_GR_promoted_now": False,
        "next_target": "derive_no_cycle_admissibility_or_endpoint_occupancy_arrow",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Coherent-domain topology selection attempt.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

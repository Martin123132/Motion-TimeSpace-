from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "representative-selection-boundary-polarization-no-go"
STATUS = "boundary_polarization_endpoint_constraints_underselect_representative_selection_not_derived"
CLAIM_CEILING = "polarization_no_go_for_parent_promotion_local_branch_remains_effective_closure"


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
        (ROOT / "70-Ccoh-variation-and-boundary-current-audit.md", "C_coh variation and boundary-current danger"),
        (ROOT / "72-relative-current-action-owner-attempt.md", "BF plus boundary polarization route named"),
        (ROOT / "208-domain-representative-selection-law.md", "older representative-selection law and missing scale"),
        (ROOT / "278-admissible-domain-class-boundary-current-owner.md", "admissible variation but no representative"),
        (ROOT / "scripts" / "representative_selection_boundary_polarization_no_go.py", "this polarization no-go gate"),
    ]
    return [
        {"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"}
        for path, role in sources
    ]


def endpoint_constraint_rows() -> list[dict[str, Any]]:
    return [
        {
            "constraint": "local_zero",
            "formula": "Pi(0)=0",
            "reason": "stationary local/trivial class should not polarize boundary memory",
            "selects_unique_function": "no",
        },
        {
            "constraint": "FLRW_nonzero",
            "formula": "Pi(1)=1 or fixed normalization",
            "reason": "homogeneous coherent expansion should allow nonzero representative",
            "selects_unique_function": "no",
        },
        {
            "constraint": "local_linear_safety",
            "formula": "Pi'(0)=0",
            "reason": "avoid first-order local boundary response near C_coh=0",
            "selects_unique_function": "no",
        },
        {
            "constraint": "FLRW_linear_safety",
            "formula": "Pi'(1)=0",
            "reason": "avoid first-order representative drift around homogeneous FLRW",
            "selects_unique_function": "no",
        },
        {
            "constraint": "monotonicity",
            "formula": "0 <= Pi(C) <= 1 and Pi' >= 0",
            "reason": "coherence should not invert branch assignment",
            "selects_unique_function": "no",
        },
    ]


def candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "linear_Pi",
            "formula": "Pi(C)=C",
            "passes_endpoints": "yes",
            "problem": "Pi'(0)=1 gives local first-order sensitivity; not forced",
            "verdict": "reject_for_promotion",
        },
        {
            "candidate": "smoothstep",
            "formula": "Pi(C)=3C^2-2C^3",
            "passes_endpoints": "yes_with_zero_endpoint_slopes",
            "problem": "one of infinitely many smoothstep choices",
            "verdict": "closure_candidate_only",
        },
        {
            "candidate": "smootherstep",
            "formula": "Pi(C)=10C^3-15C^4+6C^5",
            "passes_endpoints": "yes_with_more_zero_derivatives",
            "problem": "regularity preference still does not derive coefficient law",
            "verdict": "closure_candidate_only",
        },
        {
            "candidate": "threshold_or_sigmoid",
            "formula": "Pi(C)=Theta(C-C*) or sigmoid((C-C*)/w)",
            "passes_endpoints": "yes",
            "problem": "adds threshold/width scale unless derived",
            "verdict": "reject_without_parent_origin",
        },
        {
            "candidate": "topological_quantized_Pi",
            "formula": "Pi in {0,1} from relative class sector",
            "passes_endpoints": "possible",
            "problem": "requires class-selection theorem already missing",
            "verdict": "best_theorem_target_but_circular_today",
        },
        {
            "candidate": "BF_boundary_polarization",
            "formula": "S_boundary = integral_boundary Pi(C_coh) wedge b_2",
            "passes_endpoints": "formal",
            "problem": "delta Pi = Pi'(C) delta C reopens boundary/Bianchi terms",
            "verdict": "not_parent_derived",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "endpoint_constraints_unique",
            "result": "fail",
            "evidence": "linear, smoothstep, smootherstep, and infinitely many polynomials share required endpoints",
            "meaning": "endpoint branch behaviour underselects Pi",
        },
        {
            "test": "regularity_unique",
            "result": "fail",
            "evidence": "higher endpoint derivative constraints still leave infinite families",
            "meaning": "smoothness alone cannot select representative",
        },
        {
            "test": "no_new_scale",
            "result": "fail_for_thresholds",
            "evidence": "threshold/sigmoid requires C* or width w",
            "meaning": "would be a new domain selector knob",
        },
        {
            "test": "Bianchi_safe",
            "result": "open_fail",
            "evidence": "Pi'(C_coh) delta C_coh creates boundary exchange terms",
            "meaning": "must be absorbed by a parent current equation",
        },
        {
            "test": "representative_selected",
            "result": "fail",
            "evidence": "Pi biases a representative but does not derive why that representative is physical",
            "meaning": "selection problem remains",
        },
        {
            "test": "support_claim_allowed",
            "result": "fail",
            "evidence": "class selection, u3, Bmem, matter coupling, and local perturbation current remain underived",
            "meaning": "no local-GR/unification promotion",
        },
    ]


def branch_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "stationary_local",
            "desired_readout": "Pi(0)=0",
            "achieved_by_constraints": "yes",
            "promotion_issue": "many Pi choices achieve this",
        },
        {
            "branch": "near_local_perturbation",
            "desired_readout": "Pi'(0)=0 or suppressed",
            "achieved_by_constraints": "optional",
            "promotion_issue": "order of suppression is chosen unless derived",
        },
        {
            "branch": "FLRW_background",
            "desired_readout": "Pi(1) nonzero",
            "achieved_by_constraints": "yes",
            "promotion_issue": "normalization tied to amplitude closure",
        },
        {
            "branch": "FLRW_perturbation",
            "desired_readout": "controlled Pi'(1) response",
            "achieved_by_constraints": "optional",
            "promotion_issue": "perturbation stress/current still not solved",
        },
        {
            "branch": "transition_boundary",
            "desired_readout": "unique representative through 0<C<1",
            "achieved_by_constraints": "no",
            "promotion_issue": "exactly where Pi freedom matters most",
        },
    ]


def route_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "topological_quantization",
            "next_work": "derive Pi as a discrete class projector from boundary/cohomology sector",
            "allowed": "yes_as_theorem_target",
            "risk": "circular unless class sector independently selects representative",
        },
        {
            "route": "regularity_selected_smoothstep",
            "next_work": "choose lowest-degree smooth Pi with endpoint derivatives",
            "allowed": "only_as_explicit_closure",
            "risk": "mathematical elegance mistaken for derivation",
        },
        {
            "route": "empirical_fit_Pi",
            "next_work": "fit threshold/width to local/cosmology data",
            "allowed": "no_for_theory_promotion",
            "risk": "turns local branch into flexible selector",
        },
        {
            "route": "ledger_and_test_pivot",
            "next_work": "record derived/conditional/closure/failed pieces and move closure branch to empirical local/cosmology tests",
            "allowed": "yes_recommended",
            "risk": "less glamorous, much safer",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "Boundary polarization Pi(C_coh) can encode the desired local-zero and FLRW-nonzero representatives, but endpoint and regularity constraints underselect Pi. "
                "Any smooth Pi that works is a closure unless a parent symmetry/topological quantization forces it. "
                "The relative current can impose closure and admissibility, but representative selection is still not derived."
            ),
            "next_target": "local_branch_status_ledger_and_empirical_closure_test_pivot",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "endpoint_constraints.csv": (endpoint_constraint_rows(), ["constraint", "formula", "reason", "selects_unique_function"]),
        "polarization_candidates.csv": (
            candidate_rows(),
            ["candidate", "formula", "passes_endpoints", "problem", "verdict"],
        ),
        "no_go_tests.csv": (no_go_rows(), ["test", "result", "evidence", "meaning"]),
        "branch_impact.csv": (branch_impact_rows(), ["branch", "desired_readout", "achieved_by_constraints", "promotion_issue"]),
        "route_policy.csv": (route_policy_rows(), ["route", "next_work", "allowed", "risk"]),
        "decision.csv": (decision_rows(), ["decision", "claim_ceiling", "meaning", "next_target"]),
    }

    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "endpoint_constraints_unique": False,
        "regularity_unique": False,
        "Pi_parent_derived": False,
        "representative_selected": False,
        "new_scale_or_surface_stress_added": False,
        "support_claim_allowed": False,
        "recommended_next": "local_branch_status_ledger_and_empirical_closure_test_pivot",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Representative selection / boundary polarization no-go gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

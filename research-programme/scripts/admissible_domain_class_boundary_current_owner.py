from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "admissible-domain-class-boundary-current-owner"
STATUS = "relative_current_restricts_admissible_variations_but_does_not_select_physical_domain_class"
CLAIM_CEILING = "admissible_variation_contract_sharpened_no_domain_selection_or_local_GR_promotion"


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
        (ROOT / "60-relative-cohomology-boundary-contract.md", "relative local-zero / FLRW-nonzero contract"),
        (ROOT / "61-bound-domain-boundary-theorem-attempt.md", "volume-flux boundary theorem attempt"),
        (ROOT / "71-relative-boundary-current-construction-attempt.md", "relative pair J_rel=(j3,b2) construction"),
        (ROOT / "72-relative-current-action-owner-attempt.md", "action can impose d_rel closure but not representative"),
        (ROOT / "277-domain-free-boundary-Euler-equation.md", "free-boundary Euler degeneracy to be restricted"),
        (ROOT / "scripts" / "admissible_domain_class_boundary_current_owner.py", "this admissible variation gate"),
    ]
    return [
        {"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"}
        for path, role in sources
    ]


def relative_current_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "relative_pair",
            "formula": "J_rel=(j_3,b_2)",
            "status": "formal_object_available",
            "meaning": "bulk 3-current plus boundary 2-current/primitive",
        },
        {
            "object": "relative_closure",
            "formula": "d_rel J_rel=(d j_3, i* j_3 - d_boundary b_2)=0",
            "status": "imposable_by_multiplier_action",
            "meaning": "bulk closure plus boundary exchange compatibility",
        },
        {
            "object": "relative_charge",
            "formula": "Q_rel[D]=integral_D j_3 - integral_boundaryD b_2",
            "status": "class_observable",
            "meaning": "domain memory class rather than arbitrary scalar profile",
        },
        {
            "object": "admissible_variation",
            "formula": "delta_eta Q_rel[D]=0",
            "status": "candidate_condition",
            "meaning": "boundary variations must preserve the relative class unless a source/event changes it",
        },
        {
            "object": "local_trivial_class",
            "formula": "Q_rel=0",
            "status": "conditional_branch",
            "meaning": "stationary local domain carries no scalar volume-memory class",
        },
        {
            "object": "FLRW_expansion_class",
            "formula": "Q_rel=(N_D/u3)^3 or equivalent normalized expansion class",
            "status": "conditional_branch",
            "meaning": "coherent cosmological expansion carries nonzero domain class",
        },
    ]


def admissibility_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "A1_class_preserving",
            "formula": "delta_eta Q_rel=0",
            "effect_on_277_degeneracy": "removes arbitrary boundary moves that change memory class",
            "gap": "parent action must state why only class-preserving eta are gauge/admissible",
        },
        {
            "condition": "A2_boundary_exchange",
            "formula": "i_eta j_3 = delta_eta b_2 + d_boundary gamma_1 on boundary",
            "effect_on_277_degeneracy": "turns moving-boundary flux into exact boundary bookkeeping",
            "gap": "b_2 representative not selected",
        },
        {
            "condition": "A3_event_allowed_class_change",
            "formula": "delta_eta Q_rel = integral_event S_rel",
            "effect_on_277_degeneracy": "allows collapse/merger/domain transition rather than forcing silence",
            "gap": "event source law not derived",
        },
        {
            "condition": "A4_normalized_charge",
            "formula": "C_D = Q_rel / N_Domain",
            "effect_on_277_degeneracy": "can make homogeneous FLRW domains equivalent under normalization",
            "gap": "normalization still tied to u3/Bmem theorem targets",
        },
        {
            "condition": "A5_no_surface_stress",
            "formula": "J_rel topological / constrained, not a kinetic wall",
            "effect_on_277_degeneracy": "avoids new local PPN wall source",
            "gap": "topological stress cancellation must be proven on shell",
        },
    ]


def degeneracy_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "degeneracy": "FLRW_many_comoving_domains",
            "relative_current_effect": "groups homologous normalized expansion domains into same class",
            "resolved": "partly",
            "why_not_full": "does not select the cosmological domain normalization or u3",
        },
        {
            "degeneracy": "local_a_equals_zero_many_domains",
            "relative_current_effect": "class-preserving local deformations remain trivial Q_rel=0",
            "resolved": "partly",
            "why_not_full": "does not prove which local boundary is physical",
        },
        {
            "degeneracy": "tracefree_shear_boundaries",
            "relative_current_effect": "shear-only variations need not change scalar Q_rel",
            "resolved": "conditional",
            "why_not_full": "perturbative/current representative law still open",
        },
        {
            "degeneracy": "collapse_or_merger",
            "relative_current_effect": "can be treated as class-changing event source",
            "resolved": "no",
            "why_not_full": "event source law and energy exchange not derived",
        },
        {
            "degeneracy": "quiet_domain_choice",
            "relative_current_effect": "forbids changes that alter a pre-existing class",
            "resolved": "no",
            "why_not_full": "the pre-existing physical class is still selected by assumption unless parent action supplies it",
        },
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "stationary_local",
            "class_assignment": "Q_rel=0",
            "admissible_variations": "relative-boundary preserving deformations keep Q_rel=0",
            "status": "conditional_silence_not_selection",
        },
        {
            "branch": "FLRW",
            "class_assignment": "Q_rel nonzero expansion class",
            "admissible_variations": "homogeneous comoving deformations can be equivalent after normalization",
            "status": "conditional_nonzero_not_normalization_derivation",
        },
        {
            "branch": "local_dynamic",
            "class_assignment": "possible source/event class transition",
            "admissible_variations": "not purely gauge if Q_rel changes",
            "status": "open",
        },
        {
            "branch": "galaxy_empirical_pillar",
            "class_assignment": "do not erase with local scalar triviality",
            "admissible_variations": "requires separate bound/unbound or sidecar mapping",
            "status": "kept_separate",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "admissible_variation_condition_written",
            "result": "yes",
            "evidence": "delta_eta Q_rel=0 gives a class-preserving variation rule",
            "claim_effect": "277 degeneracy is constrained, not arbitrary",
        },
        {
            "gate": "relative_current_action_closure_available",
            "result": "yes_formal",
            "evidence": "prior S=<Lambda_rel,d_rel J_rel> can impose d_rel J_rel=0",
            "claim_effect": "closure can be action-owned",
        },
        {
            "gate": "physical_representative_selected",
            "result": "no",
            "evidence": "nothing here selects which Q_rel class or b2 representative is physically realized",
            "claim_effect": "domain selection remains open",
        },
        {
            "gate": "Euler_degeneracy_broken",
            "result": "partly_not_fully",
            "evidence": "arbitrary eta is restricted, but all class-preserving eta remain degenerate",
            "claim_effect": "problem moves from boundary calculus to class selection",
        },
        {
            "gate": "new_scale_or_surface_stress_added",
            "result": "no",
            "evidence": "relative current route is topological/constrained",
            "claim_effect": "safe as a theorem target",
        },
        {
            "gate": "support_claim_allowed",
            "result": "no",
            "evidence": "representative, normalization, class source law, u3, Bmem, and matter coupling remain underived",
            "claim_effect": "no local-GR/unification promotion",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "A relative boundary current can state a real admissibility rule: boundary variations are gauge/admissible only when they preserve the relative charge Q_rel. "
                "This restricts the arbitrary eta variations that made the free-boundary Euler equation degenerate, without adding a fitted length or surface-tension stress. "
                "However it does not select the physical representative or the initial class; the degeneracy is moved to a class-selection problem, not solved."
            ),
            "next_target": "representative_selection_or_polarization_no_go_then_local_branch_status_ledger",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "relative_current_objects.csv": (relative_current_rows(), ["object", "formula", "status", "meaning"]),
        "admissibility_conditions.csv": (
            admissibility_rows(),
            ["condition", "formula", "effect_on_277_degeneracy", "gap"],
        ),
        "degeneracy_tests.csv": (
            degeneracy_test_rows(),
            ["degeneracy", "relative_current_effect", "resolved", "why_not_full"],
        ),
        "branch_readout.csv": (branch_rows(), ["branch", "class_assignment", "admissible_variations", "status"]),
        "gate_results.csv": (gate_rows(), ["gate", "result", "evidence", "claim_effect"]),
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
        "admissible_variation_condition_written": True,
        "relative_current_action_closure_available": True,
        "physical_representative_selected": False,
        "Euler_degeneracy_broken": "partly_not_fully",
        "new_scale_or_surface_stress_added": False,
        "support_claim_allowed": False,
        "next_target": "representative_selection_or_polarization_no_go_then_local_branch_status_ledger",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Admissible domain class / boundary-current owner gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

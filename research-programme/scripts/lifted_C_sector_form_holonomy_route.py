from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "lifted-C-sector-form-holonomy-route"
STATUS = "lifted_C_sector_3form_boundary_route_identified_not_parent_derived_projected_metric_remains_closure"
CLAIM_CEILING = "lifted_C_sector_theorem_target_only_no_local_GR_or_unification_promotion"

B_MEM = 2.0 / 27.0
LOCAL_DELTA_C_GATE = 4.6e-05
LOCAL_QR_GATE = 2.3e-05


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
        (ROOT / "273-Cperp-relative-exactness-C-sector.md", "scalar Cperp exactness failure and closure label"),
        (ROOT / "51-FLRW-memory-current-contract.md", "FLRW memory-current / determinant contract"),
        (ROOT / "60-relative-cohomology-boundary-contract.md", "relative local-zero / FLRW-nonzero boundary contract"),
        (ROOT / "252-topological-projector-parent-action-skeleton.md", "topological projector parent action skeleton"),
        (ROOT / "272-quotient-configuration-principle-from-topological-projector.md", "presymplectic quotient route"),
        (ROOT / "scripts" / "lifted_C_sector_form_holonomy_route.py", "this lifted C-sector gate"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": "yes" if path.exists() else "no",
        }
        for path, role in sources
    ]


def candidate_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "scalar_Cperp_current_route",
            "lifted_object": "none; keep C as scalar",
            "local_exactness": "failed",
            "FLRW_nonzero": "possible only by closure",
            "main_obstruction": "scalar residual profiles are not relative-exact gauge by cohomology",
            "verdict": "rejected_as_derivation_current_branch",
        },
        {
            "route": "one_form_connection_holonomy",
            "lifted_object": "A_C with C_D as period/holonomy over domain cycle",
            "local_exactness": "A_C -> A_C + d lambda gives exact local residuals with zero periods",
            "FLRW_nonzero": "possible if coherent domain has nonzero cycle/endpoint period",
            "main_obstruction": "cycle/path/domain selector and matter coupling to holonomy not derived",
            "verdict": "possible_side_route",
        },
        {
            "route": "two_form_boundary_flux",
            "lifted_object": "B_C with C_D as normalized integral over boundary 2-surface",
            "local_exactness": "B_C -> B_C + d Lambda gives boundary-exact cancellation on closed surfaces",
            "FLRW_nonzero": "possible via coherent domain boundary flux",
            "main_obstruction": "must separate ordinary mass/Gauss flux from memory class",
            "verdict": "possible_side_route",
        },
        {
            "route": "three_form_domain_current",
            "lifted_object": "J_C or K_C 3-form with C_D as normalized integral over spatial domain",
            "local_exactness": "J_C -> J_C + d B_C changes C_D by boundary term; local stationary boundary can kill it",
            "FLRW_nonzero": "natural match to H^3(D,partial D), volume expansion class, and det(Q) memory exposure",
            "main_obstruction": "parent J_C from Q^i_j / coframe not derived; boundary theorem and normalization open",
            "verdict": "best_current_lifted_route",
        },
        {
            "route": "four_form_global_flux",
            "lifted_object": "F_4=dA_3 with C_D as spacetime/domain flux constant",
            "local_exactness": "local gauge residuals carry no propagating scalar dof",
            "FLRW_nonzero": "possible as global/domain integration constant",
            "main_obstruction": "too global unless domain transition/local readout and BAO timing are derived",
            "verdict": "clean_for_no_local_dof_but_rigid",
        },
    ]


def exactness_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "local_residual_exactness",
            "scalar_C": "fail",
            "one_form": "pass_if_zero_period",
            "two_form": "pass_if_closed_boundary",
            "three_form": "pass_if_boundary_primitive_zero",
            "four_form": "pass_as_gauge_flux",
            "best_route": "three_form_domain_current",
        },
        {
            "gate": "FLRW_nonzero_survival",
            "scalar_C": "closure_only",
            "one_form": "requires endpoint/cycle period",
            "two_form": "requires boundary flux",
            "three_form": "natural H3/domain volume class",
            "four_form": "global constant possible",
            "best_route": "three_form_domain_current",
        },
        {
            "gate": "BAO_same_domain_compatibility",
            "scalar_C": "closure_only",
            "one_form": "possible but path-dependence risk",
            "two_form": "possible with boundary-domain rule",
            "three_form": "good if domain current gives smooth C_D",
            "four_form": "too rigid unless domain-dependent",
            "best_route": "three_form_domain_current",
        },
        {
            "gate": "local_GR_silence",
            "scalar_C": "fails_as_derivation",
            "one_form": "gauge exact if matter sees holonomy class",
            "two_form": "gauge exact if matter sees flux class",
            "three_form": "gauge exact if local boundary primitive zero",
            "four_form": "no local scalar dof",
            "best_route": "three_form_or_four_form",
        },
        {
            "gate": "parent_current_from_existing_MTS",
            "scalar_C": "not enough",
            "one_form": "not in current corpus",
            "two_form": "not in current corpus",
            "three_form": "connects to J_M, H^3(D,boundary D), det(Q)",
            "four_form": "external/sequestering-like unless derived",
            "best_route": "three_form_domain_current",
        },
        {
            "gate": "amplitude_Bmem",
            "scalar_C": "not derived",
            "one_form": "not derived",
            "two_form": "not derived",
            "three_form": "rank-27/rank-2 target remains",
            "four_form": "not derived",
            "best_route": "none_yet",
        },
    ]


def three_form_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract": "T1_lifted_variable",
            "required_form": "replace scalar residual Cperp with a domain 3-form memory current J_C or boundary 2-form potential B_C",
            "status": "new_theorem_target",
            "failure_mode": "falls back to scalar Cperp closure",
        },
        {
            "contract": "T2_observable_scalar",
            "required_form": "C_D[D] = N_D^{-1} integral_D J_C or equivalent normalized boundary/domain class",
            "status": "contract",
            "failure_mode": "matter metric scalar remains inserted",
        },
        {
            "contract": "T3_local_exact_residual",
            "required_form": "J_C residual shifts by d_rel B_C with boundary primitive zero on stationary local domains",
            "status": "not_derived",
            "failure_mode": "local residual can be physical",
        },
        {
            "contract": "T4_FLRW_nonzero_class",
            "required_form": "coherent FLRW expansion gives nontrivial H^3(D,boundary D) class",
            "status": "conditional_previous",
            "failure_mode": "lift kills cosmological memory",
        },
        {
            "contract": "T5_parent_Q_origin",
            "required_form": "J_C or I_M derives from Q^i_j / det(Q) / coframe load current",
            "status": "not_derived",
            "failure_mode": "new form field is named to solve problem",
        },
        {
            "contract": "T6_universal_matter_class_coupling",
            "required_form": "matter metric uses exp(C_D[D])g because C_D is the class observable",
            "status": "not_derived",
            "failure_mode": "projected metric remains closure",
        },
        {
            "contract": "T7_Bianchi_domain_variation",
            "required_form": "domain labels, boundaries, form potentials, and projector stresses varied",
            "status": "open",
            "failure_mode": "hidden conservation failure",
        },
        {
            "contract": "T8_amplitude_normalization",
            "required_form": "rank-27/rank-2/unity normalization or equivalent derives B_mem",
            "status": "not_derived",
            "failure_mode": "no amplitude promotion",
        },
    ]


def decision_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "scalar_C_sector_repaired",
            "result": "no",
            "evidence": "checkpoint 273 failure remains",
            "claim_effect": "projected metric remains closure in current scalar branch",
        },
        {
            "gate": "lifted_C_route_exists",
            "result": "yes_conditional",
            "evidence": "form/holonomy/flux routes can make local residuals exact by gauge structure",
            "claim_effect": "future theorem route remains alive",
        },
        {
            "gate": "best_lifted_route",
            "result": "three_form_domain_current",
            "evidence": "matches H^3 relative memory class, FLRW volume expansion, and det(Q) current",
            "claim_effect": "next derivation target identified",
        },
        {
            "gate": "parent_lift_derived",
            "result": "not_derived",
            "evidence": "J_C/B_C and matter class coupling are contracts only",
            "claim_effect": "no local-GR or unification promotion",
        },
        {
            "gate": "empirical_closure_tests_allowed",
            "result": "yes_with_labels",
            "evidence": "projected metric closure is explicitly labelled after checkpoint 273",
            "claim_effect": "testing can proceed without pretending derivation",
        },
        {
            "gate": "support_claim_allowed",
            "result": "no",
            "evidence": "lifted C-sector, domain variation, and Bmem normalization not derived",
            "claim_effect": "no local-GR/CMB/BAO/unification promotion",
        },
    ]


def route_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "path": "continue_derivation",
            "next_work": "derive J_C 3-form/domain current from Q^i_j determinant/coframe load tensor",
            "allowed": "yes",
            "risk": "may become another named current unless Q origin is real",
        },
        {
            "path": "empirical_closure_tests",
            "next_work": "test projected metric as explicitly labelled closure/effective branch",
            "allowed": "yes",
            "risk": "not evidence for parent derivation; only viability of closure",
        },
        {
            "path": "public_claim",
            "next_work": "claim derived local GR or unified matter coupling",
            "allowed": "no",
            "risk": "unsupported by current derivation gates",
        },
        {
            "path": "return_to_scalar_C",
            "next_work": "treat scalar Cperp as exact/gauge",
            "allowed": "no",
            "risk": "contradicts checkpoint 273",
        },
    ]


def numeric_rows() -> list[dict[str, Any]]:
    return [
        {
            "quantity": "B_mem",
            "value": B_MEM,
            "meaning": "fixed closure/theorem target carried forward",
        },
        {
            "quantity": "epsilon_local_DeltaC_max",
            "value": LOCAL_DELTA_C_GATE / B_MEM,
            "meaning": "residual matter leak bound if closure branch leaks Cperp",
        },
        {
            "quantity": "epsilon_local_qR_max",
            "value": LOCAL_QR_GATE / B_MEM,
            "meaning": "stricter qR-like residual leak bound",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The scalar C-sector remains demoted, but a lifted C-sector route is coherent: the strongest candidate is a domain 3-form/boundary-class memory current whose normalized integral defines C_D. "
                "This can make local residuals exact by Stokes/presymplectic degeneracy while preserving a nonzero FLRW H^3 class, but J_C, matter class coupling, boundary theorem, and B_mem normalization are not parent-derived."
            ),
            "next_target": "derive_JC_three_form_memory_current_from_Qij_or_pivot_to_empirical_closure_status_ledger",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "candidate_routes.csv": (
            candidate_route_rows(),
            ["route", "lifted_object", "local_exactness", "FLRW_nonzero", "main_obstruction", "verdict"],
        ),
        "exactness_gates.csv": (
            exactness_gate_rows(),
            ["gate", "scalar_C", "one_form", "two_form", "three_form", "four_form", "best_route"],
        ),
        "three_form_contract.csv": (three_form_contract_rows(), ["contract", "required_form", "status", "failure_mode"]),
        "decision_gates.csv": (decision_gate_rows(), ["gate", "result", "evidence", "claim_effect"]),
        "route_policy.csv": (route_policy_rows(), ["path", "next_work", "allowed", "risk"]),
        "numeric_bounds.csv": (numeric_rows(), ["quantity", "value", "meaning"]),
        "decision.csv": (decision_rows(), ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status = decision_rows()[0]["decision"]
    payload = {
        "status": status,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "scalar_C_sector_repaired": False,
        "lifted_C_sector_route_exists": True,
        "best_lifted_route": "three_form_domain_current",
        "parent_lift_derived": False,
        "projected_metric_current_label": "explicit_effective_closure",
        "local_GR_or_unification_claim_allowed": False,
        "next_target": "derive_JC_three_form_memory_current_from_Qij_or_pivot_to_empirical_closure_status_ledger",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(status + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lifted C-sector form/holonomy route gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

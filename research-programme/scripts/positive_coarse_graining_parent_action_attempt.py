from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "positive-coarse-graining-parent-action-attempt"
STATUS = "positive_coarse_graining_time_derivable_only_with_open_onsager_sector"
CLAIM_CEILING = "open_boundary_parent_contract_only_no_full_Bmem_or_local_GR_promotion"


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
        (ROOT / "292-relative-index-level-theorem-attempt.md", "conditional k=9 relative index"),
        (ROOT / "293-domain-topology-selection-attempt.md", "conditional B3 topology route"),
        (ROOT / "294-endpoint-occupancy-arrow-law-attempt.md", "projector-rank endpoint law"),
        (ROOT / "295-arrow-semigroup-parent-time-attempt.md", "semigroup/H-theorem arrow and parent-time blocker"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def parent_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "ordinary_conservative_action",
            "candidate_equation": "Euler-Lagrange/Hamiltonian group flow",
            "gamma_sign": "not_fixed",
            "what_it_can_derive": "reversible oscillatory or constrained dynamics",
            "failure": "cannot produce a fundamental irreversible rank-forgetting semigroup without extra structure",
            "status": "no_go_for_arrow",
        },
        {
            "route": "Onsager_gradient_flow",
            "candidate_equation": "dq/dtau=-M grad F, F=(1/2)<q,R_aniso q>, M>=0",
            "gamma_sign": "gamma>=0 if mobility M is positive",
            "what_it_can_derive": "monotone decay of anisotropic residual and positive entropy production",
            "failure": "positive mobility is a parent constitutive/thermodynamic input",
            "status": "conditional_parent_route",
        },
        {
            "route": "Schwinger_Keldysh_influence_action",
            "candidate_equation": "S_eff=int q_a(dot q_r+Gamma R q_r)+(i/2)q_a N q_a",
            "gamma_sign": "Gamma>=0 if the noise kernel N>=0 and fluctuation-dissipation/KMS holds",
            "what_it_can_derive": "dissipative semigroup from integrating out boundary/environment modes",
            "failure": "requires explicit hidden/boundary sector and state condition",
            "status": "best_field_theory_contract",
        },
        {
            "route": "contact_or_metriplectic_action",
            "candidate_equation": "Hamiltonian reversible part plus symmetric entropy bracket",
            "gamma_sign": "gamma>=0 if entropy bracket is positive semidefinite",
            "what_it_can_derive": "time-oriented relaxation while keeping conservation laws in the reversible sector",
            "failure": "MTS parent action has not yet supplied the entropy variable/bracket",
            "status": "open_contract",
        },
        {
            "route": "observer_projection_only",
            "candidate_equation": "q_obs=P_iso q",
            "gamma_sign": "not_applicable",
            "what_it_can_derive": "apparent loss of axis information in observations",
            "failure": "projection is not physical time evolution",
            "status": "insufficient",
        },
    ]


def onsager_calculation_rows() -> list[dict[str, Any]]:
    examples = [
        ("axis_residual_unit", Fraction(1, 1), Fraction(1, 1)),
        ("axis_residual_two_units", Fraction(2, 1), Fraction(1, 2)),
        ("zero_residual", Fraction(0, 1), Fraction(1, 1)),
        ("negative_mobility_counterexample", Fraction(1, 1), Fraction(-1, 1)),
    ]
    rows: list[dict[str, Any]] = []
    for label, residual_norm_sq, mobility in examples:
        gamma = mobility
        d_free_energy = -gamma * residual_norm_sq
        entropy_production = gamma * residual_norm_sq
        if mobility > 0:
            status = "pass_positive_mobility"
        elif mobility == 0:
            status = "neutral_no_arrow"
        else:
            status = "fail_reversed_arrow"
        rows.append(
            {
                "case": label,
                "residual_norm_sq": residual_norm_sq,
                "mobility_gamma": gamma,
                "dF_dtau": d_free_energy,
                "entropy_production": entropy_production,
                "status": status,
            }
        )
    return rows


def field_theory_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_item": "resolved_field",
            "required_form": "q_r in diagonal axis-load sector A with residual R_aniso q_r",
            "derived_now": "yes_kinematic",
            "blocker": "field exists only in the post-checkpoint effective branch",
        },
        {
            "contract_item": "doubled_response_field",
            "required_form": "q_a enforces dot q_r + Gamma R_aniso q_r = 0",
            "derived_now": "constructed_as_contract",
            "blocker": "not present in the current parent action",
        },
        {
            "contract_item": "positive_noise_kernel",
            "required_form": "N>=0 in (i/2) q_a N q_a",
            "derived_now": "conditional",
            "blocker": "needs explicit environment/boundary state",
        },
        {
            "contract_item": "fluctuation_dissipation_relation",
            "required_form": "N=2 T Gamma with T>=0 or equivalent positivity theorem",
            "derived_now": "conditional",
            "blocker": "requires thermodynamic/KMS or causal boundary condition",
        },
        {
            "contract_item": "Ward_trace_coupling",
            "required_form": "only P_iso q_r sources FLRW stress after coarse-graining",
            "derived_now": "not_yet",
            "blocker": "still needs parent stress variation",
        },
        {
            "contract_item": "local_silence_filter",
            "required_form": "local bound domains have Gamma=0 or R_aniso charge unobservable/suppressed",
            "derived_now": "not_yet",
            "blocker": "needed for local GR/PPN safety",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "finite-dimensional Hamiltonian flow is invertible",
            "reason": "flow maps form a time-reversal group when the Hamiltonian is regular",
            "effect_on_arrow": "cannot equal a strict forgetful projection as fundamental evolution",
            "status": "no_go_for_plain_reversible_parent",
        },
        {
            "claim": "symplectic flow preserves phase-space volume",
            "reason": "Liouville theorem",
            "effect_on_arrow": "does not naturally produce monotone contraction of anisotropic residual volume",
            "status": "no_go_without_environment_or_constraint",
        },
        {
            "claim": "rank-forgetting limit Phi_infinity=P_iso is non-invertible",
            "reason": "two anisotropic directions are lost in the limit",
            "effect_on_arrow": "requires coarse-graining, boundary condition, or quotient map",
            "status": "requires_open_or_projected_theory",
        },
        {
            "claim": "dissipation can be variational only with extra structure",
            "reason": "Rayleigh/Onsager/contact/SK doubling or influence action",
            "effect_on_arrow": "parent theory must include that structure explicitly",
            "status": "contract_not_current_derivation",
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
            "gate": "ordinary_reversible_action_derives_arrow",
            "status": "fail",
            "evidence": "invertible conservative flows do not produce fundamental irreversible projection",
            "claim_effect": "plain parent action route rejected",
        },
        {
            "gate": "Onsager_gradient_flow_derives_positive_gamma",
            "status": "conditional_pass",
            "evidence": "dF/dtau=-gamma||R_aniso q||^2<=0 and entropy production=gamma||R_aniso q||^2>=0 for gamma>=0",
            "claim_effect": "positive coarse-graining time can be made exact if positive mobility is parent-owned",
        },
        {
            "gate": "influence_action_can_parent_own_gamma",
            "status": "conditional_pass",
            "evidence": "positive noise kernel plus fluctuation-dissipation can force Gamma>=0",
            "claim_effect": "best field-theoretic parent contract identified",
        },
        {
            "gate": "positive_mobility_parent_derived",
            "status": "fail",
            "evidence": "no explicit MTS parent entropy/noise/boundary sector currently derives M>=0",
            "claim_effect": "arrow remains conditional",
        },
        {
            "gate": "physical_time_identified",
            "status": "fail",
            "evidence": "tau is still coarse-graining time, not proven to be physical MTS time",
            "claim_effect": "no final parent-time promotion",
        },
        {
            "gate": "B_mem_derived",
            "status": "fail",
            "evidence": "2/27 still requires conditional k=9, B3 topology, trace partition, endpoint law, and open-sector arrow",
            "claim_effect": "locked empirical closure retained",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "open coarse-graining sector does not yet prove q_loc suppression or PPN safety",
            "claim_effect": "no local-GR promotion",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "A positive 3->1 coarse-graining arrow can be derived from an Onsager/Schwinger-Keldysh style open "
                "boundary sector: use F=(1/2)||R_aniso q||^2 and dq/dtau=-gamma R_aniso q with gamma>=0, or an "
                "influence action whose positive noise kernel and fluctuation-dissipation relation force Gamma>=0. "
                "However, an ordinary reversible parent action cannot supply this arrow by itself, and the current MTS "
                "parent stack has not derived the required positive mobility/noise sector or identified tau with physical time."
            ),
            "next_target": "write_closure_contract_or_construct_explicit_open_boundary_parent_sector",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "parent_routes.csv": (
            parent_route_rows(),
            ["route", "candidate_equation", "gamma_sign", "what_it_can_derive", "failure", "status"],
        ),
        "onsager_calculation.csv": (
            onsager_calculation_rows(),
            ["case", "residual_norm_sq", "mobility_gamma", "dF_dtau", "entropy_production", "status"],
        ),
        "field_theory_contract.csv": (
            field_theory_contract_rows(),
            ["contract_item", "required_form", "derived_now", "blocker"],
        ),
        "ordinary_action_no_go.csv": (
            no_go_rows(),
            ["claim", "reason", "effect_on_arrow", "status"],
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
        "positive_gamma_derived_conditionally": True,
        "ordinary_reversible_parent_no_go": True,
        "parent_time_derived_now": False,
        "B_mem_derived_now": False,
        "local_GR_promoted_now": False,
        "next_target": "write_closure_contract_or_construct_explicit_open_boundary_parent_sector",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Positive coarse-graining parent action attempt.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

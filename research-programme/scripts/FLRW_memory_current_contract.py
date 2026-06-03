#!/usr/bin/env python3
"""Write the parent-current contract needed for the FLRW p=3 activation route."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "08_phase_volume_doc": Path("08-phase-volume-reciprocity-origin.md"),
    "09_radial_cell_doc": Path("09-hamiltonian-radial-cell-derivation.md"),
    "21_cosmology_bridge_doc": Path("21-cosmology-parent-bridge-audit.md"),
    "50_parent_activation_doc": Path("50-parent-activation-law-attempt.md"),
    "50_status": Path("runs/20260531-032036-parent-activation-law-attempt/status.json"),
    "50_equations": Path("runs/20260531-032036-parent-activation-law-attempt/results/activation_law_equation_chain.csv"),
    "50_routes": Path("runs/20260531-032036-parent-activation-law-attempt/results/candidate_parent_derivation_routes.csv"),
    "50_contract": Path("runs/20260531-032036-parent-activation-law-attempt/results/parent_contract_requirements.csv"),
    "50_gates": Path("runs/20260531-032036-parent-activation-law-attempt/results/gate_results.csv"),
}


def absolute_source(key: str) -> Path:
    return POST_CHECKPOINT / SOURCE_PATHS[key]


def load_json(key: str) -> dict[str, Any]:
    return json.loads(absolute_source(key).read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, relative_path in SOURCE_PATHS.items():
        absolute_path = POST_CHECKPOINT / relative_path
        rows.append(
            {
                "source_key": key,
                "relative_path": str(relative_path),
                "absolute_path": str(absolute_path),
                "exists": absolute_path.exists(),
            }
        )
    missing = [row["absolute_path"] for row in rows if not row["exists"]]
    if missing:
        raise FileNotFoundError("missing source files: " + "; ".join(missing))
    return rows


def variable_contract_rows(status: dict[str, Any]) -> list[dict[str, Any]]:
    metrics = status["key_metrics"]
    return [
        {
            "symbol": "Q^i_j",
            "role": "dimensionless parent load tensor on FLRW spatial slices",
            "required_definition": "project parent motion/memory geometry into a 3x3 spatial load tensor",
            "current_status": "not_defined",
            "known_value_or_constraint": "FLRW isotropy must reduce it to X_FLRW delta^i_j",
            "failure_mode": "without Q, det(Q)=X^3 is just decorative algebra",
        },
        {
            "symbol": "X_FLRW",
            "role": "single isotropic load eigenvalue",
            "required_definition": "Q^i_j=X_FLRW delta^i_j on homogeneous/isotropic backgrounds",
            "current_status": "closure_identification",
            "known_value_or_constraint": f"current closure uses X_FLRW=N/u3 with u3={metrics['u3']}",
            "failure_mode": "if X=N/u3 is assumed rather than derived, transition scale remains fitted",
        },
        {
            "symbol": "I_M",
            "role": "dimensionless cumulative memory exposure",
            "required_definition": "I_M=det(Q) or another parent invariant that becomes X_FLRW^3 in FLRW",
            "current_status": "best_contract_candidate",
            "known_value_or_constraint": "I_M(0)=0 and I_M>=0 on the past-directed physical branch",
            "failure_mode": "if I_M is defined directly as X^3, p=3 is inserted by hand",
        },
        {
            "symbol": "J_M",
            "role": "memory current/hazard per e-fold load",
            "required_definition": "J_M=dI_M/dN from a parent continuity equation, constraint, Noether current, or action variation",
            "current_status": "conditional",
            "known_value_or_constraint": f"current closure needs J_M=3N^2/u3^3 with coefficient {3.0 / (metrics['u3'] ** 3)}",
            "failure_mode": "quadratic current remains a postulate",
        },
        {
            "symbol": "F",
            "role": "activation fraction",
            "required_definition": "F=1-exp(-I_M) from additive irreversible exposure or justified replacement",
            "current_status": "conditional_exact_given_I_M",
            "known_value_or_constraint": "F'=0 and F''=0 at N=0 for p=3",
            "failure_mode": "survival form is a closure assumption",
        },
        {
            "symbol": "u3",
            "role": "transition/load scale",
            "required_definition": "derive from parent coupling, threshold, cell scale, or boundary condition",
            "current_status": "borrowed_from_N50_match",
            "known_value_or_constraint": f"u3={metrics['u3']}; N50={metrics['N50']}",
            "failure_mode": "cosmology branch remains calibrated",
        },
        {
            "symbol": "b_mem",
            "role": "background memory amplitude",
            "required_definition": "derive from memory stress-energy, trace budget, or parent boundary law",
            "current_status": "not_derived_here",
            "known_value_or_constraint": "checkpoint-50 retained C2 branch but did not derive amplitude",
            "failure_mode": "score survives as closure, not theory",
        },
        {
            "symbol": "T^mu_nu_memory or modified-geometry owner",
            "role": "Bianchi/conservation owner",
            "required_definition": "state whether memory is a conserved fluid, exchanged sector, or modified geometric term",
            "current_status": "missing",
            "known_value_or_constraint": "must lift to perturbations and local limit",
            "failure_mode": "background equation is phenomenological only",
        },
    ]


def equation_contract_rows(status: dict[str, Any]) -> list[dict[str, Any]]:
    metrics = status["key_metrics"]
    u3 = metrics["u3"]
    return [
        {
            "step": 1,
            "equation": "Q^i_j = X_FLRW delta^i_j",
            "meaning": "homogeneous/isotropic parent load tensor has one eigenvalue",
            "contract_status": "required_not_derived",
            "non_circularity_test": "Q must be defined before imposing FLRW symmetry",
        },
        {
            "step": 2,
            "equation": "I_M = det(Q)",
            "meaning": "memory exposure is a 3D load-volume invariant",
            "contract_status": "best_candidate_contract",
            "non_circularity_test": "parent action must prefer determinant/3-form volume, not p=3 by name",
        },
        {
            "step": 3,
            "equation": "I_M|FLRW = det(X_FLRW delta^i_j)=X_FLRW^3",
            "meaning": "cubic exposure follows from three equal FLRW load directions",
            "contract_status": "conditional_pass",
            "non_circularity_test": "passes if Q and det(Q) are independently motivated",
        },
        {
            "step": 4,
            "equation": "dI_M/dN = det(Q) Tr(Q^{-1} dQ/dN)",
            "meaning": "Jacobi determinant identity gives the current",
            "contract_status": "mathematical_identity_where_Q_invertible",
            "non_circularity_test": "endpoint must be handled by smooth limiting form because Q=0 at N=0",
        },
        {
            "step": 5,
            "equation": "J_M|FLRW = 3 X_FLRW^2 dX_FLRW/dN",
            "meaning": "the required quadratic memory current is the FLRW determinant-current",
            "contract_status": "conditional_pass",
            "non_circularity_test": "valid if dX_FLRW/dN is parent-predicted",
        },
        {
            "step": 6,
            "equation": f"X_FLRW=N/u3, u3={u3}",
            "meaning": "current closure identifies the load eigenvalue with normalized e-fold lookback",
            "contract_status": "not_derived",
            "non_circularity_test": "must come from expansion/history scalar, not curve fitting",
        },
        {
            "step": 7,
            "equation": "F=1-exp(-I_M)",
            "meaning": "activation is a saturating exposure map",
            "contract_status": "conditional",
            "non_circularity_test": "must be justified by irreversible memory counting or replaced",
        },
    ]


def candidate_mechanism_rows() -> list[dict[str, Any]]:
    return [
        {
            "mechanism": "isotropic_load_tensor_determinant",
            "status": "best_contract_candidate_not_derivation",
            "what_it_gives": "p=3 from det(Q) when Q has three equal FLRW eigenvalues",
            "what_it_does_not_give": "origin of Q, u3, b_mem, conservation owner, perturbations, or local silence",
            "next_test": "try to define Q from parent motion/time/space geometry",
        },
        {
            "mechanism": "exact_three_form_memory_current",
            "status": "plausible_but_unbuilt",
            "what_it_gives": "a natural invariant volume/current route for cumulative memory exposure",
            "what_it_does_not_give": "the action term or field equation that makes the three-form physical",
            "next_test": "ask whether S_memory can be represented as a closed or sourced 3-form",
        },
        {
            "mechanism": "Raychaudhuri_or_expansion_load",
            "status": "partial_for_N_only",
            "what_it_gives": "a way to connect N=-ln(a) to integrated expansion",
            "what_it_does_not_give": "the normalization u3 or determinant exposure",
            "next_test": "derive X_FLRW as normalized integrated expansion/load from parent variables",
        },
        {
            "mechanism": "quadratic_hazard_postulate",
            "status": "too_circular_alone",
            "what_it_gives": "J_M proportional to X^2 and therefore p=3",
            "what_it_does_not_give": "any reason for the quadratic onset",
            "next_test": "only acceptable if recovered from determinant/Noether/constraint route",
        },
        {
            "mechanism": "local_double_zero_unification",
            "status": "consistency_principle_not_mechanism",
            "what_it_gives": "same double-zero design language as local PPN suppression",
            "what_it_does_not_give": "proof that local and FLRW projections share one parent current",
            "next_test": "derive both local q_loc^nu silence and FLRW J_M from one projected tensor",
        },
    ]


def circularity_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "do_not_define_I_as_X_cubed_without_reason",
            "status": "guarded_by_determinant_contract",
            "pass_condition": "I_M=det(Q) or equivalent parent invariant is motivated before FLRW reduction",
            "fail_condition": "the theory simply declares I=X^3 to recover the fitted law",
        },
        {
            "test": "do_not_define_X_as_N_over_u3_by_fit",
            "status": "fail_currently",
            "pass_condition": "X_FLRW follows from an integrated expansion/load scalar with predicted normalization",
            "fail_condition": "u3 remains inherited from N50",
        },
        {
            "test": "do_not_define_J_as_the_desired_answer",
            "status": "fail_currently",
            "pass_condition": "J_M follows from determinant identity plus parent evolution for Q",
            "fail_condition": "J_M=3X^2 dX/dN is postulated directly",
        },
        {
            "test": "conservation_is_not_optional",
            "status": "fail_currently",
            "pass_condition": "memory stress/geometric owner obeys Bianchi-compatible evolution",
            "fail_condition": "background E(z) term is added without pressure/exchange/geometric equation",
        },
        {
            "test": "same_parent_must_be_local_silent",
            "status": "open",
            "pass_condition": "local stationary/vacuum projection has vanishing coherent det(Q) current or screened source",
            "fail_condition": "cosmology mechanism creates local PPN hair",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "cubic_memory_current_contract_identified",
            "status": "pass_conditional",
            "reason": "I_M=det(Q) gives I_M=X^3 and J_M=3X^2 dX/dN in FLRW",
            "claim_allowed": "there is now a non-arbitrary contract route for p=3",
        },
        {
            "gate": "parent_load_tensor_defined",
            "status": "fail",
            "reason": "Q^i_j is named by the contract but not derived from parent MTS fields",
            "claim_allowed": "load tensor is a required next object",
        },
        {
            "gate": "X_FLRW_equals_N_over_u3_derived",
            "status": "fail",
            "reason": "the e-fold load relation and normalization remain closure-level",
            "claim_allowed": "X=N/u3 is a target, not a theorem",
        },
        {
            "gate": "u3_parent_predicted",
            "status": "fail",
            "reason": "u3 remains inherited from N50 matching",
            "claim_allowed": "transition scale not derived",
        },
        {
            "gate": "bmem_parent_predicted",
            "status": "fail",
            "reason": "amplitude remains outside this contract",
            "claim_allowed": "amplitude not derived",
        },
        {
            "gate": "conservation_owner_defined",
            "status": "fail",
            "reason": "memory stress/geometric Bianchi owner is still missing",
            "claim_allowed": "no covariant background claim",
        },
        {
            "gate": "local_silence_contract_defined",
            "status": "open",
            "reason": "determinant route suggests isotropic cosmology can be active while local coherent FLRW load can vanish, but this is not proven",
            "claim_allowed": "possible bridge, not a result",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "reason": "the mechanism is contractual, not derived or empirically promoted",
            "claim_allowed": "private theory-building only",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "FLRW_memory_current_contract",
            "status": "contract_identified_not_derived",
            "best_route": "isotropic_load_tensor_determinant",
            "meaning": "p=3 can be made non-arbitrary if memory exposure is the determinant of a parent 3D load tensor",
            "next_target": "52-load-tensor-origin-attempt.md",
        },
        {
            "decision": "promotion_status",
            "status": "no_promotion",
            "best_route": "continue_derivation",
            "meaning": "the contract sharpens the missing theorem but does not yet supply it",
            "next_target": "derive or reject Q^i_j from parent motion/time/space variables",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="FLRW memory-current contract.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_register = source_register_rows()
    status_50 = load_json("50_status")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-FLRW-memory-current-contract"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    variables = variable_contract_rows(status_50)
    equations = equation_contract_rows(status_50)
    mechanisms = candidate_mechanism_rows()
    circularity = circularity_test_rows()
    gates = gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_checkpoint_register.csv", source_register, list(source_register[0].keys()))
    write_csv(results_dir / "memory_current_variable_contract.csv", variables, list(variables[0].keys()))
    write_csv(results_dir / "memory_current_equation_contract.csv", equations, list(equations[0].keys()))
    write_csv(results_dir / "candidate_current_mechanisms.csv", mechanisms, list(mechanisms[0].keys()))
    write_csv(results_dir / "circularity_tests.csv", circularity, list(circularity[0].keys()))
    write_csv(results_dir / "gate_results.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    metrics = status_50["key_metrics"]
    status = {
        "status": "complete_FLRW_memory_current_contract",
        "readout": "FLRW_memory_current_contract_identified_not_derived",
        "recommendation": "attempt_load_tensor_origin_next",
        "next_target": "52-load-tensor-origin-attempt.md",
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "best_contract_route": "I_M=det(Q), Q^i_j|FLRW=X_FLRW delta^i_j",
        "key_metrics": {
            "u3": metrics["u3"],
            "N50": metrics["N50"],
            "endpoint_power": metrics["endpoint_power"],
            "dX_dN": 1.0 / metrics["u3"],
            "JM_quadratic_coefficient": 3.0 / (metrics["u3"] ** 3),
            "F_triple_prime_0": metrics["F_triple_prime_0"],
            "variable_contract_rows": len(variables),
            "equation_contract_rows": len(equations),
            "candidate_mechanisms": len(mechanisms),
            "open_or_failed_gates": sum(1 for row in gates if row["status"] in {"fail", "open"}),
        },
        "outputs": {
            "source_checkpoint_register": str(results_dir / "source_checkpoint_register.csv"),
            "memory_current_variable_contract": str(results_dir / "memory_current_variable_contract.csv"),
            "memory_current_equation_contract": str(results_dir / "memory_current_equation_contract.csv"),
            "candidate_current_mechanisms": str(results_dir / "candidate_current_mechanisms.csv"),
            "circularity_tests": str(results_dir / "circularity_tests.csv"),
            "gate_results": str(results_dir / "gate_results.csv"),
            "decision": str(results_dir / "decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(status["readout"] + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

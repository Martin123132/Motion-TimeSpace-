from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "boundary-exchange-nohair-theorem-attempt"
CHECKPOINT_DOC = "417-boundary-exchange-nohair-theorem-attempt.md"
STATUS = "boundary_exchange_nohair_theorem_attempt_written_conditional_topological_nohair_and_Ward_owner_routes_but_boundary_exchange_not_derived_no_local_GR_pass"
CLAIM_CEILING = "boundary_exchange_nohair_theorem_attempt_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "418-Cexp-domain-candidate-generator.md"


SOURCE_DOCS = [
    {
        "path": "68-chiD-gated-memory-conservation-contract.md",
        "role": "Bianchi gremlin and boundary exchange open",
    },
    {
        "path": "70-Ccoh-variation-and-boundary-current-audit.md",
        "role": "C_coh variation boundary current candidates",
    },
    {
        "path": "71-relative-boundary-current-construction-attempt.md",
        "role": "formal relative current J_rel=(j_3,b_2)",
    },
    {
        "path": "72-relative-current-action-owner-attempt.md",
        "role": "relative-current action owner and Bianchi failure",
    },
    {
        "path": "73-local-route-blocker-ledger-and-promotion-gate.md",
        "role": "local route blocker ledger naming boundary exchange and Bianchi gaps",
    },
    {
        "path": "403-boundary-domain-flux-nohair-numeric-contract.md",
        "role": "numeric no-hair source-lock contract",
    },
    {
        "path": "415-local-trivial-class-selector-theorem-attempt.md",
        "role": "local class theorem attempt requiring zero boundary exchange",
    },
    {
        "path": "416-binding-invariant-domain-selector-repair.md",
        "role": "binding selector repair pointing to boundary exchange no-hair",
    },
    {
        "path": "runs/20260531-113126-Ccoh-variation-and-boundary-current-audit/results/boundary_current_candidates.csv",
        "role": "boundary current candidate ledger",
    },
    {
        "path": "runs/20260531-113439-relative-boundary-current-construction-attempt/results/closure_tests.csv",
        "role": "relative current closure tests by arena",
    },
    {
        "path": "runs/20260531-113740-relative-current-action-owner-attempt/results/variation_attempt_chain.csv",
        "role": "relative current action variation chain",
    },
    {
        "path": "runs/20260602-044500-boundary-domain-flux-nohair-numeric-contract/results/numeric_bound_contract.csv",
        "role": "hard channel source-lock ceilings",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv",
        "role": "runner-v4 row states",
    },
]


EXCHANGE_OBJECTS = [
    {
        "object": "bulk_memory_current",
        "symbolic_form": "j_3 ~ C_coh L_mem volume 3-current",
        "local_nohair_need": "j_3=0 or exact in selected bound local domain",
        "status": "conditional_support",
    },
    {
        "object": "boundary_primitive",
        "symbolic_form": "b_2 with i_star j_3=d_boundary b_2",
        "local_nohair_need": "b_2=0/exact or pure topological bookkeeping",
        "status": "formal_constructed_not_parent_selected",
    },
    {
        "object": "Bianchi_gate_term",
        "symbolic_form": "T_memory^{mu nu} nabla_mu chi_D",
        "local_nohair_need": "vanishes, cancels with T_aux/T_boundary, or is retained",
        "status": "not_derived",
    },
    {
        "object": "relative_exchange_current",
        "symbolic_form": "d_rel J_rel=(d j_3, i_star j_3-d_boundary b_2)",
        "local_nohair_need": "d_rel J_rel=0 and local representative is zero/exact",
        "status": "formal_closure_possible",
    },
    {
        "object": "boundary_polarization",
        "symbolic_form": "Pi(C_exp or C_coh) wedge b_2",
        "local_nohair_need": "Pi(0)=0 locally and metric variation has no local wall stress",
        "status": "conditional_contract",
    },
    {
        "object": "projected_local_flux",
        "symbolic_form": "q_BDP^i=P_loc[nB+F_X+F_domain+F_projector+F_source]^i",
        "local_nohair_need": "zero by theorem or retained below 4e-20 alpha3 lock",
        "status": "not_derived",
    },
    {
        "object": "secular_exchange_drift",
        "symbolic_form": "dot_F_flux + dot_L_domain + dot_K_memory",
        "local_nohair_need": "zero by theorem or retained below 9.6e-15 yr^-1",
        "status": "not_derived",
    },
]


THEOREM_ROUTES = [
    {
        "route": "topological_exact_nohair",
        "theorem_shape": "local J_rel is exact/zero, b_2 pure boundary bookkeeping, Pi(0)=0, no metric wall stress",
        "would_pay": "R7/R9/domain rows can move toward theorem-zero",
        "result": "conditional_target_not_derived",
    },
    {
        "route": "Ward_owned_exchange",
        "theorem_shape": "exchange current exists but belongs to total Ward ledger and cancels exactly",
        "would_pay": "honest conservation route; rows may become owned coefficients",
        "result": "conditional_route_not_nohair",
    },
    {
        "route": "retained_coefficient_bound",
        "theorem_shape": "exchange current remains but coefficients/ranges/source charges are explicit and testable",
        "would_pay": "empirical robustness testing without claiming GR derivation",
        "result": "allowed_retained_route",
    },
    {
        "route": "dynamic_surface_wall",
        "theorem_shape": "boundary carries physical surface stress sigma_wall(C)",
        "would_pay": "nothing for local GR unless stress is bounded/tiny",
        "result": "rejected_as_theorem_zero",
    },
    {
        "route": "freeze_Ccoh",
        "theorem_shape": "set delta C_coh=0 during variation",
        "would_pay": "formally removes exchange terms",
        "result": "forbidden_freeze_move",
    },
]


CONDITIONAL_NOHAIR_CHAIN = [
    {
        "step": 1,
        "claim": "Parent action owns the relative pair.",
        "identity": "delta_Lambda S -> d_rel J_rel=0",
        "status": "formal_possible_not_physical_selection",
    },
    {
        "step": 2,
        "claim": "Local branch selects the trivial representative.",
        "identity": "C_exp=0 and Pi(0)=0 imply no local boundary polarization",
        "status": "conditional_if_selector_derived",
    },
    {
        "step": 3,
        "claim": "Boundary primitive is exact or zero.",
        "identity": "b_2=d_boundary a_1 or b_2=0 on partial D",
        "status": "not_derived",
    },
    {
        "step": 4,
        "claim": "Bianchi gate term is owned.",
        "identity": "T_memory nabla chi_D + div T_aux + div T_boundary = 0",
        "status": "not_derived",
    },
    {
        "step": 5,
        "claim": "Projected local exchange flux vanishes.",
        "identity": "P_loc[nB+F_X+F_D+F_P+F_source]=0",
        "status": "conditional_target_not_derived",
    },
    {
        "step": 6,
        "claim": "Secular drift vanishes.",
        "identity": "dot_F_flux+dot_L_domain+dot_K_memory=0",
        "status": "conditional_target_not_derived",
    },
    {
        "step": 7,
        "claim": "No local-GR flux/preferred-frame/domain rows remain.",
        "identity": "R5/R6/R7/R8/R9 affected channels theorem-zero",
        "status": "not_promoted",
    },
]


COUNTEREXCHANGE_CASES = [
    {
        "case": "transition_boundary_exchange",
        "construction": "local-to-FLRW boundary requires exchange primitive",
        "damage": "local boundary current can source alpha3/Gdot/preferred-frame rows",
        "needed_blocker": "prove exchange is outside local test domain or topological/exact",
    },
    {
        "case": "perturbed_FLRW_current",
        "construction": "delta C_coh nonzero in perturbations",
        "damage": "boundary current leaks into growth/lensing/local matching",
        "needed_blocker": "perturbative current construction and conservation",
    },
    {
        "case": "dynamic_wall_stress",
        "construction": "S_wall=int_boundary sqrt(gamma) sigma_wall(C)",
        "damage": "PPN-sized surface stress/fifth-force route",
        "needed_blocker": "topological/no-stress boundary action or retained coefficients",
    },
    {
        "case": "nonzero_local_relative_class",
        "construction": "d_rel J_rel=0 but [J_rel] != 0",
        "damage": "closed does not mean zero; marker survives as local class",
        "needed_blocker": "physical trivial representative selector",
    },
    {
        "case": "unowned_momentum_flux",
        "construction": "P_loc F_exchange^i != 0",
        "damage": "alpha3 lock is 4e-20, so tiny leaks matter",
        "needed_blocker": "exact Ward-owned flux silence or explicit coefficient map",
    },
]


NUMERIC_PRESSURE_ROWS = [
    {
        "family": "alpha3_flux",
        "channels": "bulk_flux_X;domain_projector_flux;unowned_momentum_flux",
        "tightest_lock": 4.0e-20,
        "units": "dimensionless",
        "theorem_need": "exact spatial exchange no-hair or Ward-owned cancellation",
    },
    {
        "family": "Gdot_drift",
        "channels": "domain_scale_drift_per_yr;flux_drift_per_yr;memory_kernel_drift_per_yr",
        "tightest_lock": 9.6e-15,
        "units": "yr^-1",
        "theorem_need": "no secular boundary/domain/memory exchange drift",
    },
    {
        "family": "domain_vector_alpha2",
        "channels": "boundary_vector_B0i;domain_vector_leakage;projector_vector_leakage",
        "tightest_lock": 2.0e-09,
        "units": "dimensionless",
        "theorem_need": "no vector boundary/projector representative",
    },
    {
        "family": "xi_anisotropy",
        "channels": "boundary_tracefree_shear;topology_cycle_anisotropy;external_domain_anisotropy",
        "tightest_lock": 4.0e-09,
        "units": "dimensionless",
        "theorem_need": "no preferred-location/topology anisotropy",
    },
    {
        "family": "gamma_beta_fifth_force_hair",
        "channels": "boundary_radial_hair;domain_projector_stress;bulk_X_metric_slip",
        "tightest_lock": 2.3e-05,
        "units": "dimensionless",
        "theorem_need": "no scalar/radial boundary hair beyond source-normalized monopole",
    },
]


ROW_TRANSITION_ATTEMPT = [
    {
        "row_id": "R5_alpha1",
        "attempted_upgrade": "retained_budget -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "retained_budget",
        "reason": "boundary/projector vector no-hair is conditional, not derived",
    },
    {
        "row_id": "R6_alpha2",
        "attempted_upgrade": "retained_budget -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "retained_budget",
        "reason": "domain anisotropy/vector leakage remains possible",
    },
    {
        "row_id": "R7_alpha3",
        "attempted_upgrade": "retained_contingent_budget -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "retained_contingent_budget",
        "reason": "exact Ward-owned flux silence or topological no-hair not derived",
    },
    {
        "row_id": "R8_xi",
        "attempted_upgrade": "retained_budget -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "retained_budget",
        "reason": "boundary/topology preferred-location anisotropy not theorem-zero",
    },
    {
        "row_id": "R9_Gdot",
        "attempted_upgrade": "retained_contingent_budget -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "retained_contingent_budget",
        "reason": "secular exchange drift not theorem-zero",
    },
    {
        "row_id": "R10_fifth_force",
        "attempted_upgrade": "unscored_parameterized -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "unscored_parameterized",
        "reason": "dynamic boundary/scalar wall route remains a possible fifth-force curve",
    },
    {
        "row_id": "R11_EH_operator_ledger",
        "attempted_upgrade": "retained_residual -> EH_selected",
        "result": "not_upgraded",
        "new_state": "retained_residual",
        "reason": "boundary exchange no-hair would not by itself select EH operator ledger",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Boundary-exchange no-hair is now split into the only honest routes. A true theorem would make the local relative current exact/zero, set Pi(0)=0, avoid metric wall stress, own the Bianchi gate term, and force the projected local exchange flux and secular exchange drift to vanish. That theorem is not derived. The best support is a formal relative-current/topological construction plus a conditional local-zero branch. The honest alternatives are Ward-owned exchange with exact cancellation, or retained coefficient maps tested against very hard locks such as 4e-20 for alpha3 and 9.6e-15/yr for Gdot. No row is promoted.",
        "conditional_topological_nohair_written": True,
        "Ward_owner_route_written": True,
        "boundary_exchange_nohair_derived": False,
        "Bianchi_gate_owned": False,
        "theorem_zero_upgrades": 0,
        "local_GR_claim_allowed": False,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "remove C_exp averaging-domain circularity by defining parent-generated candidate domains before scoring",
        "pass_condition": "C_exp evaluates domains generated by parent boundary/current variables, not data/posthoc windows",
    },
    {
        "priority": 2,
        "target": "419-boundary-exchange-coefficient-retained-evaluator.md",
        "task": "if theorem-zero fails, define retained exchange coefficients for alpha3/Gdot/domain rows",
        "pass_condition": "exchange rows become testable without claim leakage",
    },
    {
        "priority": 3,
        "target": "420-finite-fibre-spectrum-decoupling-theorem-attempt.md",
        "task": "test whether finite-cell fibre spectra can be integrated out or reduced to universal constants",
        "pass_condition": "finite fibre does not create local matter-visible marker channels",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        rows.append(
            {
                "source_file": source_doc["path"],
                "exists": source_path.exists(),
                "role": source_doc["role"],
            }
        )
    return rows


def runner_v4_rows() -> list[dict[str, str]]:
    return read_csv(ROOT / "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv")


def row_transition_rows() -> list[dict[str, Any]]:
    matrix_by_id = {row["row_id"]: row for row in runner_v4_rows()}
    rows: list[dict[str, Any]] = []
    for transition in ROW_TRANSITION_ATTEMPT:
        matrix_row = matrix_by_id.get(transition["row_id"], {})
        rows.append(
            {
                "row_id": transition["row_id"],
                "previous_state": matrix_row.get("runner_v4_state", "missing"),
                "new_state": transition["new_state"],
                "attempted_upgrade": transition["attempted_upgrade"],
                "result": transition["result"],
                "theorem_credit_allowed": False,
                "claim_allowed": False,
                "reason": transition["reason"],
            }
        )
    return rows


def gate_rows(
    source_rows: list[dict[str, Any]],
    transition_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    theorem_rows = [row for row in transition_rows if row["theorem_credit_allowed"]]
    claim_rows = [row for row in transition_rows if row["claim_allowed"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "exchange_objects_written",
            "status": "pass",
            "evidence": f"{len(EXCHANGE_OBJECTS)} exchange objects classified",
        },
        {
            "gate": "conditional_topological_nohair_written",
            "status": "conditional_pass",
            "evidence": "local exact/zero J_rel plus Pi(0)=0 route stated",
        },
        {
            "gate": "Ward_owner_route_written",
            "status": "conditional_pass",
            "evidence": "nonzero exchange can be honest only if total Ward ledger owns it",
        },
        {
            "gate": "boundary_exchange_nohair_derived",
            "status": "fail",
            "evidence": "b_2 exact/zero and physical local representative are not parent-derived",
        },
        {
            "gate": "Bianchi_gate_owned",
            "status": "fail",
            "evidence": "T_memory grad chi_D cancellation is not derived",
        },
        {
            "gate": "projected_local_flux_zero",
            "status": "fail",
            "evidence": "P_loc exchange flux zero is theorem target only",
        },
        {
            "gate": "secular_exchange_drift_zero",
            "status": "fail",
            "evidence": "Gdot-relevant flux/domain/memory drift closure not derived",
        },
        {
            "gate": "numeric_pressure_registered",
            "status": "pass",
            "evidence": f"{len(NUMERIC_PRESSURE_ROWS)} no-hair pressure families registered",
        },
        {
            "gate": "runner_rows_promoted_to_theorem_zero",
            "status": "fail",
            "evidence": f"{len(theorem_rows)} theorem-credit row upgrades",
        },
        {
            "gate": "claim_leaks",
            "status": "pass" if not claim_rows else "fail",
            "evidence": f"{len(claim_rows)} claim-allowed rows",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "boundary exchange no-hair attempt only; no EH/Newton/PPN/local-GR pass",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join([header, separator, *body])


def format_float(value: Any) -> str:
    number = float(value)
    if number == 0.0:
        return "0"
    if abs(number) < 1.0e-3 or abs(number) >= 1.0e4:
        return f"{number:.3e}"
    return f"{number:.6g}"


def write_checkpoint_markdown(
    run_dir: Path,
    transition_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, Any]],
) -> None:
    object_table_rows = [
        {
            "object": row["object"],
            "status": row["status"],
            "need": row["local_nohair_need"],
        }
        for row in EXCHANGE_OBJECTS
    ]
    route_table_rows = [
        {
            "route": row["route"],
            "result": row["result"],
            "would_pay": row["would_pay"],
        }
        for row in THEOREM_ROUTES
    ]
    chain_table_rows = [
        {
            "step": row["step"],
            "claim": row["claim"],
            "status": row["status"],
        }
        for row in CONDITIONAL_NOHAIR_CHAIN
    ]
    pressure_table_rows = [
        {
            "family": row["family"],
            "lock": format_float(row["tightest_lock"]),
            "units": row["units"],
            "need": row["theorem_need"],
        }
        for row in NUMERIC_PRESSURE_ROWS
    ]
    transition_table_rows = [
        {
            "row_id": row["row_id"],
            "previous_state": row["previous_state"],
            "new_state": row["new_state"],
            "result": row["result"],
        }
        for row in transition_rows
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 417 - Boundary Exchange No-Hair Theorem Attempt

Private boundary-exchange/local-GR checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 416 left one sharp blocker: the `chi_D`/memory gate creates boundary exchange and Bianchi terms. This checkpoint asks whether those terms can be made local no-hair, Ward-owned, or explicitly retained for testing.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/boundary_exchange_nohair_theorem_attempt.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Exchange Objects

{markdown_table(object_table_rows, ["object", "status", "need"])}

## 4. Honest Routes

{markdown_table(route_table_rows, ["route", "result", "would_pay"])}

## 5. Conditional No-Hair Chain

{markdown_table(chain_table_rows, ["step", "claim", "status"])}

## 6. Numeric Pressure

{markdown_table(pressure_table_rows, ["family", "lock", "units", "need"])}

## 7. Row Transition Attempt

{markdown_table(transition_table_rows, ["row_id", "previous_state", "new_state", "result"])}

## 8. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 9. Decision

{DECISION[0]["decision"]}

Practical read: the boundary route is still alive, but it is not free. Either the current is topological/exact and local-zero, or a total Ward identity owns it, or it becomes retained testable physics. What we cannot do is quietly delete it.

## 10. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    transition_rows = row_transition_rows()
    gate_result_rows = gate_rows(source_rows, transition_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "exchange_objects.csv", EXCHANGE_OBJECTS)
    write_csv(results_dir / "theorem_routes.csv", THEOREM_ROUTES)
    write_csv(results_dir / "conditional_nohair_chain.csv", CONDITIONAL_NOHAIR_CHAIN)
    write_csv(results_dir / "counterexchange_cases.csv", COUNTEREXCHANGE_CASES)
    write_csv(results_dir / "numeric_pressure_rows.csv", NUMERIC_PRESSURE_ROWS)
    write_csv(results_dir / "row_transition_attempt.csv", transition_rows)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "conditional_topological_nohair_written": True,
        "Ward_owner_route_written": True,
        "boundary_exchange_nohair_derived": False,
        "Bianchi_gate_owned": False,
        "numeric_pressure_families": len(NUMERIC_PRESSURE_ROWS),
        "theorem_zero_upgrades": 0,
        "claim_allowed_rows": 0,
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, transition_rows, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 417 boundary-exchange no-hair theorem attempt artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()

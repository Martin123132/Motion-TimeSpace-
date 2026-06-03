from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "same-frame-EH-source-Poisson-reduction-gate"
CHECKPOINT_DOC = "424-same-frame-EH-source-Poisson-reduction-gate.md"
STATUS = "same_frame_EH_source_Poisson_reduction_gate_written_exact_GR_to_Newton_bridge_but_parent_premises_not_derived_no_local_GR_pass"
CLAIM_CEILING = "same_frame_EH_source_Poisson_reduction_gate_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md"


SOURCE_DOCS = [
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH/source pair and weak-field algebra",
    },
    {
        "path": "405-same-frame-EH-source-derived-stack-audit.md",
        "role": "local-GR/Newton stack rungs and claim tiers",
    },
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "minimal parent action and source-normalization block",
    },
    {
        "path": "384-parent-action-first-variation-obstruction-map.md",
        "role": "observed-coframe selector pullback obstruction",
    },
    {
        "path": "392-EH-operator-selection-under-identity-closure.md",
        "role": "non-EH operator ledger and source-normalization next target",
    },
    {
        "path": "399-local-GR-status-for-human-review.md",
        "role": "GR/Newton status and source-normalization blockers",
    },
    {
        "path": "423-parent-action-minimality-no-extension-theorem-attempt.md",
        "role": "no-extension result and same-frame EH/source next gate",
    },
    {
        "path": "10-observer-map-symplectic-contract.md",
        "role": "Newton/PPN/conservation requirements from observer-map branch",
    },
    {
        "path": "13-local-closure-PPN-benchmark.md",
        "role": "closure PPN benchmark and gamma/beta caution",
    },
    {
        "path": "177-parent-action-perturbation-local-GR-contract.md",
        "role": "parent variation contract and Bianchi-compatible metric equation",
    },
    {
        "path": "179-local-GR-PPN-silence-contract.md",
        "role": "local PPN silence requirements",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv",
        "role": "runner-v4 row states for no-promotion audit",
    },
]


REDUCTION_REQUIREMENTS = [
    {
        "requirement": "same_matter_and_gravity_frame",
        "symbolic_form": "S_EH[g_obs] + S_matter[Psi_A,g_obs,theta_A]",
        "current_status": "conditional_not_parent_derived",
        "failure_if_missing": "field redefinition can hide source/operator debts in a different frame",
        "rows_at_risk": "R0;R2;R3;R4;R11",
    },
    {
        "requirement": "EH_operator_selection",
        "symbolic_form": "local 4D metric-only second-order exterior -> G_munu + Lambda g_munu",
        "current_status": "conditional_Lovelock_route_not_parent_derived",
        "failure_if_missing": "non-EH operators alter gamma, beta, slip, fifth force, or wave sector",
        "rows_at_risk": "R3;R4;R8;R10;R11",
    },
    {
        "requirement": "constant_universal_kappa",
        "symbolic_form": "partial_mu kappa_eff = partial_A kappa_eff = 0",
        "current_status": "not_parent_derived",
        "failure_if_missing": "Gdot/G, WEP-source charge, beta/source-normalization residues remain",
        "rows_at_risk": "R1;R4;R9",
    },
    {
        "requirement": "Bianchi_and_matter_conservation",
        "symbolic_form": "nabla_mu G^munu=0 and nabla_mu T_eff^munu=0 with no unowned q_loc^nu",
        "current_status": "not_fully_closed",
        "failure_if_missing": "extra local force/exchange appears in equations of motion",
        "rows_at_risk": "R7;R9;R10",
    },
    {
        "requirement": "nonrelativistic_static_source_limit",
        "symbolic_form": "T_00 ~= rho c^2, pressure/velocity/stress terms negligible or retained",
        "current_status": "conditional_standard_limit",
        "failure_if_missing": "Poisson source is not just mass density",
        "rows_at_risk": "R4;R10",
    },
    {
        "requirement": "measured_mass_normalization",
        "symbolic_form": "M_eff = integral rho_eff d^3x is conserved, universal, range-independent",
        "current_status": "not_parent_derived",
        "failure_if_missing": "mu_obs=G_eff M_eff gains hidden bulk/boundary/domain/source charge",
        "rows_at_risk": "R1;R4;R9;R10",
    },
    {
        "requirement": "no_extra_potential_channels",
        "symbolic_form": "mu_extra(r,t,A,lambda)=0 or explicitly retained",
        "current_status": "not_derived",
        "failure_if_missing": "Yukawa, radial hair, boundary flux, or domain projector force alters Newton",
        "rows_at_risk": "R3;R4;R7;R8;R10",
    },
    {
        "requirement": "PPN_completion",
        "symbolic_form": "gamma=1, beta=1, alpha_i=0, xi=0, Gdot=0 after retained rows vanish",
        "current_status": "not_promoted",
        "failure_if_missing": "Poisson limit alone is not a full local-GR/PPN pass",
        "rows_at_risk": "R3;R4;R5;R6;R7;R8;R9",
    },
]


POISSON_CHAIN = [
    {
        "step": 1,
        "stage": "same_frame_field_equation",
        "equation": "G_munu[g_obs] + Lambda g_obs_munu = kappa_eff T_eff_munu[g_obs]",
        "status": "conditional_target",
        "meaning": "matter and geometry must vary the same observed frame",
    },
    {
        "step": 2,
        "stage": "weak_field_metric",
        "equation": "g_00 = -1 - 2 Phi/c^2 + O(c^-4), g_ij = delta_ij(1 - 2 Psi/c^2) + ...",
        "status": "standard_limit_if_same_frame",
        "meaning": "one potential sources slow-particle acceleration; slip must be controlled",
    },
    {
        "step": 3,
        "stage": "nonrelativistic_source",
        "equation": "T_00 ~= rho_eff c^2, |T_ij| << T_00",
        "status": "conditional_standard_limit",
        "meaning": "Poisson source is rest-mass density only after extra stresses are silent or retained",
    },
    {
        "step": 4,
        "stage": "linearized_00_equation",
        "equation": "nabla^2 Phi = (kappa_eff c^4/2) rho_eff + source_residuals",
        "status": "algebra_written",
        "meaning": "the coefficient matches checkpoint 402 conventions",
    },
    {
        "step": 5,
        "stage": "G_eff_identification",
        "equation": "G_eff = kappa_eff c^4/(8 pi)",
        "status": "algebra_pass",
        "meaning": "then nabla^2 Phi = 4 pi G_eff rho_eff if source_residuals=0",
    },
    {
        "step": 6,
        "stage": "measured_GM",
        "equation": "mu_obs = G_eff M_eff + mu_extra",
        "status": "conditional_not_parent_derived",
        "meaning": "Newton requires mu_extra=0 and G_eff M_eff constant/universal/range-independent",
    },
    {
        "step": 7,
        "stage": "slow_particle_acceleration",
        "equation": "d^2 x^i/dt^2 = -partial_i Phi + a_extra^i",
        "status": "conditional",
        "meaning": "Newtonian mechanics follows only if a_extra^i=0 or retained below locks",
    },
]


NORMALIZATION_TESTS = [
    {
        "test": "constant_Geff",
        "required_identity": "partial_t G_eff = partial_r G_eff = partial_A G_eff = 0",
        "current_status": "not_derived",
        "residual_if_failed": "Gdot/G or WEP-source charge",
    },
    {
        "test": "conserved_mass",
        "required_identity": "dM_eff/dt = 0 on local bound systems",
        "current_status": "not_derived",
        "residual_if_failed": "source-normalization beta/Gdot channel",
    },
    {
        "test": "range_independent_GM",
        "required_identity": "partial_lambda mu_obs = 0 and no Yukawa tail",
        "current_status": "not_derived",
        "residual_if_failed": "fifth-force row",
    },
    {
        "test": "species_independent_source",
        "required_identity": "partial_A mu_obs = 0 for material species A",
        "current_status": "not_derived",
        "residual_if_failed": "WEP/source-charge row",
    },
    {
        "test": "boundary_bulk_domain_silence",
        "required_identity": "mu_extra[B,X,D,J_rel,P]=0 or retained",
        "current_status": "not_derived",
        "residual_if_failed": "gamma/beta/alpha/xi/Gdot/fifth-force residuals",
    },
    {
        "test": "PPN_second_order_completion",
        "required_identity": "g_00 = -1 - 2U/c^2 - 2U^2/c^4 + ... and g_ij = delta_ij(1 - 2U/c^2)+...",
        "current_status": "not_derived",
        "residual_if_failed": "beta/gamma rows",
    },
]


COUNTEREXAMPLE_BRANCHES = [
    {
        "counterexample": "frame_split_EH_and_matter",
        "symbolic_form": "S_EH[g] + S_matter[exp(F)g]",
        "why_it_breaks_newton": "same-looking matter action sources a different metric than the EH operator",
        "required_blocker": "same-frame matter/EH variation theorem",
    },
    {
        "counterexample": "drifting_kappa",
        "symbolic_form": "kappa_eff = kappa0(1 + epsilon C_D(t,x))",
        "why_it_breaks_newton": "Poisson coefficient becomes time/range/domain dependent",
        "required_blocker": "constant universal kappa theorem",
    },
    {
        "counterexample": "nonEH_operator_residue",
        "symbolic_form": "R^2, Weyl^2, scalar-tensor, torsion, nonmetricity, nonlocal kernel",
        "why_it_breaks_newton": "adds slip, fourth-order pieces, scalar modes, or fifth-force tails",
        "required_blocker": "EH-only operator selection or retained coefficient ledger",
    },
    {
        "counterexample": "hidden_source_charge",
        "symbolic_form": "M_eff = M_baryon + delta M_boundary + delta M_X + delta M_D",
        "why_it_breaks_newton": "measured GM absorbs new physics instead of deriving universal mass",
        "required_blocker": "source-normalization and no-hair theorem",
    },
    {
        "counterexample": "finite_range_force",
        "symbolic_form": "Phi = -G M/r (1 + alpha exp(-r/lambda))",
        "why_it_breaks_newton": "Poisson limit is range dependent unless alpha(lambda)=0 or bounded",
        "required_blocker": "fifth-force law or theorem-zero",
    },
    {
        "counterexample": "unowned_Bianchi_exchange",
        "symbolic_form": "nabla_mu T_eff^munu = q_loc^nu != 0",
        "why_it_breaks_newton": "slow-particle motion receives non-geodesic/exchange force",
        "required_blocker": "Ward/Bianchi exchange owner",
    },
    {
        "counterexample": "Poisson_only_false_GR_pass",
        "symbolic_form": "nabla^2 Phi = 4 pi G rho but gamma != 1 or beta != 1",
        "why_it_breaks_newton": "Newtonian force may pass while light bending/time delay/PPN fail",
        "required_blocker": "full PPN residual vector",
    },
]


ROW_IDS = [
    "R0_identity_coframe_direct",
    "R1_WEP_source_charge",
    "R2_clock_redshift",
    "R3_gamma",
    "R4_beta",
    "R5_alpha1",
    "R6_alpha2",
    "R7_alpha3",
    "R8_xi",
    "R9_Gdot",
    "R10_fifth_force",
    "R11_EH_operator_ledger",
]


DECISION = [
    {
        "decision": (
            "The exact local bridge is now machine-readable: if the parent action derives the same matter/gravity frame, "
            "selects the EH operator as the only local metric second-order exterior operator, fixes constant universal "
            "kappa, owns Bianchi conservation, normalizes measured mass, and kills or retains every extra potential, then "
            "the weak-field 00 equation reduces to Poisson with G_eff=kappa_eff c^4/(8 pi), and slow-particle Newtonian "
            "motion follows. The algebraic bridge is clean, but the parent premises are not derived in the current corpus. "
            "Therefore this is a reduction gate and test contract, not an EH/Newton/PPN/local-GR promotion."
        )
    }
]


NEXT_QUEUE = [
    {
        "target": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "reason": "Poisson gate fails mainly because non-EH operators and measured-GM/source-normalization remain retained",
    },
    {
        "target": "425-local-bound-real-data-source-plan.md",
        "reason": "move toward testing by mapping R3/R4/R9/R10/R11 to concrete local bounds and baselines",
    },
    {
        "target": "425-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "reason": "without q_loc^nu=0 or owned exchange, even EH-shaped equations do not produce Newtonian mechanics",
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
                "role": source_doc["role"],
                "exists": source_path.exists(),
            }
        )
    return rows


def runner_v4_rows() -> list[dict[str, str]]:
    return read_csv(ROOT / "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv")


def row_transition_rows() -> list[dict[str, Any]]:
    matrix_by_id = {row["row_id"]: row for row in runner_v4_rows()}
    reasons = {
        "R0_identity_coframe_direct": "same-frame bridge assumes one observed coframe; selector-blind matter remains closure-zero",
        "R1_WEP_source_charge": "species/source dependence of kappa or measured mass is not parent-derived zero",
        "R2_clock_redshift": "matter-frame and constant-sector clock residues remain retained",
        "R3_gamma": "EH-only operator and slip silence are not derived",
        "R4_beta": "source normalization and second-order PPN completion are not derived",
        "R5_alpha1": "domain/vector preferred-frame leakage can still alter the local metric",
        "R6_alpha2": "normal/vector sectors remain retained without no-hair",
        "R7_alpha3": "unowned Bianchi/Ward exchange can source acceleration",
        "R8_xi": "domain/class preferred-location terms are not silenced",
        "R9_Gdot": "constant universal G_eff M_eff is not derived",
        "R10_fifth_force": "range-dependent source/test charge law is not derived",
        "R11_EH_operator_ledger": "non-EH operator coefficients remain retained",
    }
    rows: list[dict[str, Any]] = []
    for row_id in ROW_IDS:
        previous_state = matrix_by_id.get(row_id, {}).get("runner_v4_state", "missing")
        rows.append(
            {
                "row_id": row_id,
                "previous_state": previous_state,
                "new_state": previous_state,
                "result": "not_upgraded",
                "reason": reasons[row_id],
                "theorem_credit": False,
                "claim_allowed": False,
            }
        )
    return rows


def gate_rows(
    source_rows: list[dict[str, Any]],
    transition_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row for row in source_rows if not row["exists"]]
    theorem_rows = [row for row in transition_rows if row["theorem_credit"]]
    claim_rows = [row for row in transition_rows if row["claim_allowed"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": "all cited source paths exist" if not missing_sources else f"{len(missing_sources)} missing source paths",
        },
        {
            "gate": "reduction_requirements_written",
            "status": "pass",
            "evidence": f"{len(REDUCTION_REQUIREMENTS)} reduction requirements recorded",
        },
        {
            "gate": "Poisson_chain_written",
            "status": "pass",
            "evidence": f"{len(POISSON_CHAIN)} weak-field chain stages recorded",
        },
        {
            "gate": "EH_to_Poisson_algebra",
            "status": "conditional_pass",
            "evidence": "nabla^2 Phi = (kappa c^4/2) rho = 4 pi G_eff rho when G_eff=kappa c^4/(8 pi)",
        },
        {
            "gate": "same_frame_parent_derived",
            "status": "fail",
            "evidence": "same matter/gravity frame remains conditional",
        },
        {
            "gate": "EH_operator_selection_derived",
            "status": "fail",
            "evidence": "metric-only local second-order exterior is not derived from MTS parent action",
        },
        {
            "gate": "constant_universal_kappa_derived",
            "status": "fail",
            "evidence": "kappa_eff/G_eff universality and time/range/species independence are not proven",
        },
        {
            "gate": "measured_GM_normalized",
            "status": "fail",
            "evidence": "M_eff and mu_extra are not parent-owned zero",
        },
        {
            "gate": "Bianchi_exchange_owned",
            "status": "fail",
            "evidence": "q_loc^nu/Ward exchange is not fully owned as zero or retained source law",
        },
        {
            "gate": "extra_potential_channels_zero",
            "status": "fail",
            "evidence": "boundary/bulk/domain/fifth-force channels remain retained or unscored",
        },
        {
            "gate": "PPN_completion_derived",
            "status": "fail",
            "evidence": "gamma/beta/preferred-frame/Gdot/fifth-force residual vector is not theorem-zero",
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
            "gate": "Newton_or_local_GR_promoted",
            "status": "fail",
            "evidence": "Poisson reduction gate only; no Newton/PPN/local-GR pass",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def md_cell(value: Any) -> str:
    return str(value).replace("|", ";")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row[column]) for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_checkpoint_markdown(
    run_dir: Path,
    transition_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, Any]],
) -> None:
    requirement_table_rows = [
        {
            "requirement": row["requirement"],
            "current_status": row["current_status"],
            "failure_if_missing": row["failure_if_missing"],
            "rows_at_risk": row["rows_at_risk"],
        }
        for row in REDUCTION_REQUIREMENTS
    ]
    poisson_table_rows = [
        {
            "step": row["step"],
            "stage": row["stage"],
            "status": row["status"],
            "meaning": row["meaning"],
        }
        for row in POISSON_CHAIN
    ]
    normalization_table_rows = [
        {
            "test": row["test"],
            "current_status": row["current_status"],
            "residual_if_failed": row["residual_if_failed"],
        }
        for row in NORMALIZATION_TESTS
    ]
    counterexample_table_rows = [
        {
            "counterexample": row["counterexample"],
            "why_it_breaks_newton": row["why_it_breaks_newton"],
            "required_blocker": row["required_blocker"],
        }
        for row in COUNTEREXAMPLE_BRANCHES
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
    text = f"""# 424 - Same-Frame EH Source Poisson Reduction Gate

Private GR/Newton reduction checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 423 clarified the no-extension/minimality wall. This checkpoint moves onto the direct GR-to-Newton bridge: if MTS ever derives the same-frame Einstein-Hilbert/source premises, does the weak-field limit reduce cleanly to Poisson and Newtonian mechanics?

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/same_frame_EH_source_Poisson_reduction_gate.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Reduction Requirements

{markdown_table(requirement_table_rows, ["requirement", "current_status", "failure_if_missing", "rows_at_risk"])}

## 4. EH to Poisson Chain

{markdown_table(poisson_table_rows, ["step", "stage", "status", "meaning"])}

Exact algebraic bridge:

```text
G_munu[g_obs] + Lambda g_obs_munu = kappa_eff T_eff_munu[g_obs]
T_00 ~= rho_eff c^2
nabla^2 Phi = (kappa_eff c^4 / 2) rho_eff + source_residuals
G_eff = kappa_eff c^4 / (8 pi)
=> nabla^2 Phi = 4 pi G_eff rho_eff if source_residuals = 0.
```

That bridge is algebraically clean. It becomes Newtonian mechanics only when `mu_obs=G_eff M_eff` is constant, universal, conserved, and range-independent, and when `a_extra^i=0` or retained below lock.

## 5. Source-Normalization Tests

{markdown_table(normalization_table_rows, ["test", "current_status", "residual_if_failed"])}

## 6. Counterexample Branches

{markdown_table(counterexample_table_rows, ["counterexample", "why_it_breaks_newton", "required_blocker"])}

## 7. Row Transition Attempt

{markdown_table(transition_table_rows, ["row_id", "previous_state", "new_state", "result"])}

## 8. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 9. Decision

{DECISION[0]["decision"]}

Practical read: this is a good sign in the Mayweather sense. The bridge is not wild; if the parent pays the same-frame/EH/source bills, Newton comes out by the standard weak-field algebra. The remaining issue is not the bridge, it is earning the premises without smuggling in GR.

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
    write_csv(results_dir / "reduction_requirements.csv", REDUCTION_REQUIREMENTS)
    write_csv(results_dir / "Poisson_chain.csv", POISSON_CHAIN)
    write_csv(results_dir / "source_normalization_tests.csv", NORMALIZATION_TESTS)
    write_csv(results_dir / "counterexample_branches.csv", COUNTEREXAMPLE_BRANCHES)
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
        "reduction_requirements": len(REDUCTION_REQUIREMENTS),
        "Poisson_chain_written": True,
        "EH_to_Poisson_algebra_written": True,
        "same_frame_parent_derived": False,
        "EH_operator_selection_derived": False,
        "constant_universal_kappa_derived": False,
        "measured_GM_normalized": False,
        "Bianchi_exchange_owned": False,
        "extra_potential_channels_zero": False,
        "PPN_completion_derived": False,
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
        description="Write checkpoint 424 same-frame EH source Poisson reduction gate artifacts."
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

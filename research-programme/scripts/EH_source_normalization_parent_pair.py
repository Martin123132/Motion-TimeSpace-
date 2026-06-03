from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "EH-source-normalization-parent-pair"
CHECKPOINT_DOC = "402-EH-source-normalization-parent-pair.md"
STATUS = "EH_source_normalization_parent_pair_written_same_frame_conditional_route_not_parent_derived_gamma_beta_source_rows_retained_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "EH_source_normalization_parent_pair_only_no_EH_Newton_PPN_fifth_force_boundary_bulk_domain_or_local_GR_pass"
NEXT_TARGET = "403-boundary-domain-flux-nohair-numeric-contract.md"


SOURCE_DOCS = [
    {
        "path": "356-parent-action-ward-identity-and-projector-variation.md",
        "role": "Ward force ledger and total conservation obligations",
    },
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "parent local action skeleton, EH/source conditions, and residual fallbacks",
    },
    {
        "path": "392-EH-operator-selection-under-identity-closure.md",
        "role": "conditional EH operator selection and non-EH operator ledger",
    },
    {
        "path": "393-source-normalized-Newtonian-limit-under-identity-closure.md",
        "role": "weak-field source algebra and measured-GM absorption contract",
    },
    {
        "path": "398-parent-action-contract-v2-after-identity-stack.md",
        "role": "parent-action obligations for EH and source-normalization rows",
    },
    {
        "path": "400-runner-v3-numeric-smoke-extension.md",
        "role": "numeric pressure map for gamma, beta, Gdot, fifth-force, and source rows",
    },
    {
        "path": "401-parent-matter-selector-theorem-attempt.md",
        "role": "same-frame matter selector status and field-redefinition warning",
    },
    {
        "path": "runs/20260602-033500-local-bound-runner-v3-from-identity-stack/results/runner_v3_matrix.csv",
        "role": "runner-v3 row states for gamma/beta/source/fifth-force/operator rows",
    },
    {
        "path": "runs/20260602-034500-parent-action-contract-v2-after-identity-stack/results/runner_row_parent_obligations.csv",
        "role": "row-to-parent-obligation map",
    },
    {
        "path": "runs/20260602-041500-runner-v3-numeric-smoke-extension/results/row_worst_case_summary.csv",
        "role": "numeric smoke worst-case rows after checkpoint 400",
    },
]


SAME_FRAME_THEOREM_PAIR = [
    {
        "block": "matter_metric_frame_alignment",
        "required_statement": "the coframe seen by local matter, clocks, rulers, photons, and the metric core is the same e, up to constant source-normalized units",
        "mathematical_form": "S_matter=sum_A S_A[Psi_A,e,omega[e],theta_A]",
        "current_status": "closure_or_conditional_not_parent_derived",
        "failure_mode": "field redefinition hides EH/source debts in a different frame",
    },
    {
        "block": "EH_operator_selection",
        "required_statement": "the compact local exterior action is metric-only, four-dimensional, local, and second-order",
        "mathematical_form": "delta S_core/delta g -> G_munu + Lambda g_munu",
        "current_status": "conditional_lovelock_route_not_parent_derived",
        "failure_mode": "conserved non-EH operators remain legal",
    },
    {
        "block": "nonEH_operator_elimination",
        "required_statement": "all R2, f(R), Weyl, scalar/vector, nonlocal, source-normalization, and class-metric operator coefficients are zero or explicitly retained",
        "mathematical_form": "c_R2=c_fR=c_Weyl=c_scalar=c_vector=c_nonlocal=c_source=0 or ledgered",
        "current_status": "retained_residual",
        "failure_mode": "gamma, beta, xi, fifth-force, and wave-sector rows stay active",
    },
    {
        "block": "constant_kappa_to_Geff",
        "required_statement": "the same-frame coupling is constant and universal",
        "mathematical_form": "G_eff = kappa_eff c^4/(8 pi), partial_t G_eff=partial_r G_eff=partial_A G_eff=0",
        "current_status": "not_parent_derived",
        "failure_mode": "delta_G, Gdot/G, beta, and WEP-source rows stay active",
    },
    {
        "block": "measured_mass_source_charge",
        "required_statement": "M_eff is the conserved source charge measured by orbital dynamics, not a hidden class/bulk/boundary/domain charge",
        "mathematical_form": "M_eff=integral rho_eff d^3x, dM_eff/dt=0, dM_eff/dr=0, Delta_A M_eff=0",
        "current_status": "not_parent_derived",
        "failure_mode": "radial hair, source charge, fifth force, or beta/source-normalization residue remains",
    },
    {
        "block": "measured_GM_absorption",
        "required_statement": "only constant universal range-independent mu_obs can be absorbed into measured GM",
        "mathematical_form": "mu_obs=G_eff M_eff + mu_extra = GM_measured, partial_{r,t,A,lambda} mu_obs=0",
        "current_status": "conditional_only",
        "failure_mode": "range/time/species/radial dependence is physics, not calibration",
    },
]


WEAK_FIELD_CHAIN = [
    {
        "step": 1,
        "assumption": "same-frame EH branch",
        "expression": "G_munu + Lambda g_munu = kappa_eff T_munu_eff",
        "status": "conditional",
    },
    {
        "step": 2,
        "assumption": "weak static slow-motion source",
        "expression": "g_00 = -1 - 2 Phi/c^2, T_00_eff ~= rho_eff c^2",
        "status": "standard weak-field algebra",
    },
    {
        "step": 3,
        "assumption": "Poisson limit",
        "expression": "nabla^2 Phi = (kappa_eff c^4/2) rho_eff",
        "status": "conditional_on_EH_frame",
    },
    {
        "step": 4,
        "assumption": "Newton constant definition",
        "expression": "G_eff := kappa_eff c^4/(8 pi)",
        "status": "definition_if_kappa_eff_constant",
    },
    {
        "step": 5,
        "assumption": "measured source charge",
        "expression": "mu_obs = G_eff M_eff + mu_extra",
        "status": "source_normalization_contract",
    },
    {
        "step": 6,
        "assumption": "safe GM absorption",
        "expression": "partial_r mu_obs = partial_t mu_obs = partial_A mu_obs = partial_lambda mu_obs = 0",
        "status": "not_parent_derived",
    },
]


EH_SELECTION_TESTS = [
    {
        "test": "identity coframe alone",
        "premise": "matter sees e",
        "result": "does not select EH",
        "verdict": "fail",
        "reason": "pure gravity conserved non-EH operators can still exist",
    },
    {
        "test": "Bianchi/Ward conservation alone",
        "premise": "divergence of total equations is controlled",
        "result": "does not select EH",
        "verdict": "fail",
        "reason": "conserved higher-derivative/scalar/vector tensors exist",
    },
    {
        "test": "Lovelock-style local metric-only second-order exterior",
        "premise": "4D local metric-only second-order equations in same matter frame",
        "result": "EH plus Lambda plus boundary/topological terms",
        "verdict": "conditional_pass",
        "reason": "sufficient if parent action derives these premises",
    },
    {
        "test": "no-hair/source/boundary/domain removal",
        "premise": "bulk, boundary, domain, projector, and vector residues vanish or are pure gauge/topological",
        "result": "operator ledger can shrink",
        "verdict": "open",
        "reason": "not proven by EH selection itself",
    },
]


SOURCE_NORMALIZATION_TESTS = [
    {
        "test": "kappa constant",
        "required_identity": "partial_t kappa_eff=partial_r kappa_eff=partial_A kappa_eff=0",
        "linked_rows": "R4_beta;R9_Gdot;R10_fifth_force",
        "verdict": "fail_open",
        "reason": "constant same-frame coupling not parent-derived",
    },
    {
        "test": "M_eff conserved",
        "required_identity": "dM_eff/dt=0 and no unowned boundary/bulk/domain/source flux",
        "linked_rows": "R4_beta;R7_alpha3;R9_Gdot;R10_fifth_force",
        "verdict": "fail_open",
        "reason": "flux ownership/no-hair remains open",
    },
    {
        "test": "M_eff radial hair absent",
        "required_identity": "partial_r M_eff=0 outside source except constant monopole",
        "linked_rows": "R4_beta;R10_fifth_force",
        "verdict": "fail_open",
        "reason": "boundary/bulk radial hair not parent-derived",
    },
    {
        "test": "species/source charge universal",
        "required_identity": "Delta_A ln mu_obs=0",
        "linked_rows": "R1_WEP_source_charge;R10_fifth_force",
        "verdict": "fail_open",
        "reason": "identity coframe does not forbid source/bulk/boundary species charge",
    },
    {
        "test": "range-independent measured GM",
        "required_identity": "partial_lambda mu_obs=0 or alpha(lambda) profile explicitly scored",
        "linked_rows": "R10_fifth_force",
        "verdict": "fail_open",
        "reason": "fifth-force range/coupling remains unscored without alpha(lambda)",
    },
    {
        "test": "constant universal GM absorption",
        "required_identity": "mu_obs=GM_measured constant universal",
        "linked_rows": "R4_beta;R9_Gdot;R10_fifth_force;R1_WEP_source_charge",
        "verdict": "conditional_pass_only",
        "reason": "valid algebraically but not parent-derived",
    },
]


PAIR_GATE_MATRIX = [
    {
        "pair_gate": "same matter/metric frame",
        "EH_side": "operator frame is the same e as matter",
        "source_side": "G_eff and M_eff are measured in that frame",
        "status": "conditional_only",
        "blocking_counterexample": "e_prime=ehat frame rename changes operator/source debts",
    },
    {
        "pair_gate": "EH plus constant kappa",
        "EH_side": "G_munu+Lambda g_munu selected",
        "source_side": "kappa_eff constant gives G_eff",
        "status": "not_parent_derived",
        "blocking_counterexample": "EH-shaped equations with drifting kappa_eff are not Newton",
    },
    {
        "pair_gate": "EH plus measured mass",
        "EH_side": "Poisson operator is standard",
        "source_side": "M_eff equals orbital source charge",
        "status": "not_parent_derived",
        "blocking_counterexample": "hidden bulk/boundary/domain charge changes measured GM",
    },
    {
        "pair_gate": "no fifth-force/source hair",
        "EH_side": "no scalar/vector/radial operator residue",
        "source_side": "mu_extra=0 or alpha(lambda) profile scored",
        "status": "open",
        "blocking_counterexample": "Yukawa/radial hair can mimic or alter GM at finite range",
    },
    {
        "pair_gate": "PPN gamma/beta readiness",
        "EH_side": "gamma=1 if non-EH/boundary/domain slip absent",
        "source_side": "beta=1 if nonlinear source hair absent",
        "status": "open",
        "blocking_counterexample": "gamma and beta can fail independently",
    },
]


COUNTEREXAMPLE_MODELS = [
    {
        "model": "EH_with_time_varying_Geff",
        "satisfies": "EH-shaped metric equation",
        "violates": "partial_t(G_eff M_eff)=0",
        "observable_exit": "Gdot/G and beta/source-normalization",
        "lesson": "EH shape alone is not Newtonian reduction",
    },
    {
        "model": "metric_only_but_fR_or_R2",
        "satisfies": "covariant metric dynamics and conservation",
        "violates": "second-order EH-only operator selection",
        "observable_exit": "gamma, beta, fifth-force, wave/operator ledger",
        "lesson": "Bianchi/Ward does not imply EH",
    },
    {
        "model": "same_matter_frame_with_hidden_boundary_monopole",
        "satisfies": "matter sees e and Poisson-looking potential",
        "violates": "M_eff equals conserved source charge with no radial/time/source hair",
        "observable_exit": "delta_G, beta, fifth-force, Gdot/G",
        "lesson": "GM absorption only works for constant universal monopole",
    },
    {
        "model": "scalar_tensor_common_frame",
        "satisfies": "one matter geometry",
        "violates": "no scalar/class/bulk operator and no finite-range source charge",
        "observable_exit": "gamma, beta, clock, fifth-force",
        "lesson": "universal coupling can still be modified gravity",
    },
]


ROW_TRANSITION_DECISION = [
    {
        "runner_row": "R3_gamma",
        "current_state": "budget_only",
        "attempt_result": "EH selection is conditional under same-frame Lovelock-style premises",
        "new_state": "budget_only",
        "why_not_promoted": "non-EH, boundary, bulk, domain, and projector slip coefficients are not parent-derived zero",
    },
    {
        "runner_row": "R4_beta",
        "current_state": "budget_only",
        "attempt_result": "Newtonian beta/source algebra is explicit",
        "new_state": "budget_only",
        "why_not_promoted": "constant universal G_eff M_eff and no nonlinear source hair are not parent-derived",
    },
    {
        "runner_row": "R9_Gdot",
        "current_state": "contingent_budget",
        "attempt_result": "Gdot/G closes only if partial_t ln(G_eff M_eff)=0",
        "new_state": "contingent_budget",
        "why_not_promoted": "time drift and unowned flux remain open channels",
    },
    {
        "runner_row": "R10_fifth_force",
        "current_state": "unscored_parameterized",
        "attempt_result": "mu_extra must be zero or alpha(lambda) scored",
        "new_state": "unscored_parameterized",
        "why_not_promoted": "finite-range law, source/test charge, and screening profile remain missing",
    },
    {
        "runner_row": "R11_EH_operator_ledger",
        "current_state": "retained_residual",
        "attempt_result": "same-frame EH route is identified",
        "new_state": "retained_residual",
        "why_not_promoted": "operator coefficients are retained until parent action derives metric-only local second-order exterior",
    },
]


NO_CHEAT_RULES = [
    {
        "rule": "EH is not selected by WEP",
        "forbidden_move": "using one matter coframe to delete non-EH metric operators",
        "safe_move": "derive metric-only local second-order exterior or keep operator coefficients",
    },
    {
        "rule": "Bianchi is not uniqueness",
        "forbidden_move": "using conservation to remove all conserved non-EH tensors",
        "safe_move": "explicitly ledger every conserved residual operator",
    },
    {
        "rule": "Newton needs source normalization",
        "forbidden_move": "calling EH-shaped equations Newtonian while kappa, M_eff, or mu_obs drift",
        "safe_move": "prove constant universal measured GM or retain delta_G/Gdot/fifth-force rows",
    },
    {
        "rule": "same frame or no GR reduction",
        "forbidden_move": "proving EH in one frame and matter/source normalization in another",
        "safe_move": "state every theorem in the matter frame e",
    },
    {
        "rule": "GM absorption is narrow",
        "forbidden_move": "absorbing radial, time, species, or range-dependent effects into mass",
        "safe_move": "absorb only constant universal range-independent monopole normalization",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The same-frame EH/source-normalization pair is now explicit. If the parent action derives that matter and metric dynamics use the same local frame, that the exterior operator is local 4D metric-only second-order, and that mu_obs=G_eff M_eff is constant, universal, conserved, and range-independent, then the branch has a real route to EH plus Newtonian measured-GM normalization. The existing corpus does not yet derive those premises. EH selection remains conditional, source normalization remains conditional, and gamma/beta/Gdot/fifth-force/operator rows stay retained or budgeted.",
        "same_frame_pair_available": True,
        "EH_parent_derived": False,
        "source_normalization_parent_derived": False,
        "Newtonian_claim_allowed": False,
        "PPN_claim_allowed": False,
        "local_GR_claim_allowed": False,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "attack the boundary/domain/flux channels that block alpha3, Gdot/G, xi, and source normalization",
        "pass_condition": "unowned flux and domain/projector channels become theorem-zero, Ward-owned, or explicit coefficients",
    },
    {
        "priority": 2,
        "target": "404-selector-blind-matter-axiom-origin.md",
        "task": "look for a deeper motion/time/space origin of selector-blind matter and same-frame selection",
        "pass_condition": "selector-blind matter is derived from primitive symmetry or declared a postulate",
    },
    {
        "priority": 3,
        "target": "405-same-frame-EH-source-derived-stack-audit.md",
        "task": "combine 401 and 402 into a strict necessary/sufficient local-GR stack",
        "pass_condition": "every rung is marked derived, conditional, retained, or closure-only",
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


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "same_frame_pair_written",
            "status": "pass",
            "evidence": f"{len(SAME_FRAME_THEOREM_PAIR)} theorem-pair blocks recorded",
        },
        {
            "gate": "weak_field_chain_written",
            "status": "pass",
            "evidence": "EH -> G_eff -> Poisson -> mu_obs chain recorded",
        },
        {
            "gate": "EH_conditional_selection_available",
            "status": "conditional_pass",
            "evidence": "metric-only local 4D second-order same-frame exterior would select EH plus Lambda",
        },
        {
            "gate": "EH_parent_derived",
            "status": "fail",
            "evidence": "existing parent action has not derived metric-only local second-order exterior or eliminated non-EH operators",
        },
        {
            "gate": "source_normalization_parent_derived",
            "status": "fail",
            "evidence": "constant universal conserved range-independent measured GM is not derived",
        },
        {
            "gate": "counterexamples_retained",
            "status": "pass",
            "evidence": f"{len(COUNTEREXAMPLE_MODELS)} same-frame/EH/source counterexamples written",
        },
        {
            "gate": "row_transitions_no_false_promotion",
            "status": "pass",
            "evidence": f"{len(ROW_TRANSITION_DECISION)} runner rows retained/budgeted/unscored",
        },
        {
            "gate": "Newton_PPN_or_local_GR_promoted",
            "status": "fail",
            "evidence": "same-frame pair is conditional only",
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


def write_checkpoint_markdown(run_dir: Path, gate_result_rows: list[dict[str, Any]]) -> None:
    theorem_rows = [
        {
            "block": row["block"],
            "status": row["current_status"],
            "failure": row["failure_mode"],
        }
        for row in SAME_FRAME_THEOREM_PAIR
    ]
    pair_rows = [
        {
            "gate": row["pair_gate"],
            "status": row["status"],
            "counterexample": row["blocking_counterexample"],
        }
        for row in PAIR_GATE_MATRIX
    ]
    transition_rows = [
        {
            "row": row["runner_row"],
            "new_state": row["new_state"],
            "reason": row["why_not_promoted"],
        }
        for row in ROW_TRANSITION_DECISION
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 402 - EH Source-Normalization Parent Pair

Private EH/source-normalization/local-GR checkpoint. This is not a public Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, boundary, bulk, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 401 showed that even the matter-frame selector is conditional. This checkpoint asks the next GR/Newton question anyway:

Can MTS derive, in the same frame matter sees, both:

```text
G_munu + Lambda g_munu = kappa_eff T_munu_eff
G_eff = kappa_eff c^4/(8 pi)
mu_obs = G_eff M_eff = GM_measured
```

If not, `gamma`, `beta`, `Gdot/G`, fifth-force, and non-EH operator rows must remain open.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/EH_source_normalization_parent_pair.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Same-Frame Theorem Pair

{markdown_table(theorem_rows, ["block", "status", "failure"])}

## 4. Weak-Field Chain

The algebraic route is clean:

```text
G_munu + Lambda g_munu = kappa_eff T_munu_eff
=> nabla^2 Phi = (kappa_eff c^4/2) rho_eff
=> nabla^2 Phi = 4 pi G_eff rho_eff
=> G_eff = kappa_eff c^4/(8 pi)
=> mu_obs = G_eff M_eff + mu_extra
```

The theorem only becomes Newton if:

```text
partial_r mu_obs = partial_t mu_obs = partial_A mu_obs = partial_lambda mu_obs = 0
```

Otherwise the residue is not calibration; it is `delta_G`, `Gdot/G`, beta/source hair, WEP-source charge, or fifth force.

## 5. Pair Gates

{markdown_table(pair_rows, ["gate", "status", "counterexample"])}

## 6. Row Transition Decision

{markdown_table(transition_rows, ["row", "new_state", "reason"])}

## 7. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 8. Decision

{DECISION[0]["decision"]}

Practical read: this is the right kind of narrowing. MTS does not need to beat GR by magic here; it needs to show that its parent action lands on the same local EH/Newton corner when the local nonmetric selectors, boundary/domain/flux channels, and source normalization become silent. The route exists conditionally, but the current parent action has not earned the silence yet.

## 9. Next Target

`{NEXT_TARGET}`

The numeric smoke in checkpoint 400 says the worst next local blockers are flux/domain/source channels, especially the `alpha3`/Ward rows. So the next move is to attack boundary/domain/flux no-hair with equations, not prose.
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "same_frame_theorem_pair.csv", SAME_FRAME_THEOREM_PAIR)
    write_csv(results_dir / "weak_field_chain.csv", WEAK_FIELD_CHAIN)
    write_csv(results_dir / "EH_selection_tests.csv", EH_SELECTION_TESTS)
    write_csv(results_dir / "source_normalization_tests.csv", SOURCE_NORMALIZATION_TESTS)
    write_csv(results_dir / "pair_gate_matrix.csv", PAIR_GATE_MATRIX)
    write_csv(results_dir / "counterexample_models.csv", COUNTEREXAMPLE_MODELS)
    write_csv(results_dir / "row_transition_decision.csv", ROW_TRANSITION_DECISION)
    write_csv(results_dir / "no_cheat_rules.csv", NO_CHEAT_RULES)
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
        "same_frame_pair_blocks": len(SAME_FRAME_THEOREM_PAIR),
        "EH_parent_derived": False,
        "source_normalization_parent_derived": False,
        "Newtonian_claim_allowed": False,
        "PPN_claim_allowed": False,
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 402 same-frame EH/source-normalization parent pair artifacts."
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

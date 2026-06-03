from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "quotient-matter-functor-theorem-attempt"
CHECKPOINT_DOC = "410-quotient-matter-functor-theorem-attempt.md"
STATUS = "quotient_matter_functor_theorem_attempt_written_conditional_factorization_theorem_counterexamples_block_parent_derivation_R0_remains_closure_zero_no_local_GR_pass"
CLAIM_CEILING = "quotient_matter_functor_theorem_attempt_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_cosmology_or_local_GR_pass"
NEXT_TARGET = "411-local-bound-runner-v4-real-data-interface.py"


SOURCE_DOCS = [
    {
        "path": "337-exact-parent-pullback-selection-rule-gate.md",
        "role": "exact parent readout/pullback theorem template",
    },
    {
        "path": "341-indistinguishable-cell-quotient-parent-action-gate.md",
        "role": "cell quotient/action gate and marker-extension hazard",
    },
    {
        "path": "365-lifted-C-boundary-primitive-and-domain-Euler-equation.md",
        "role": "representative-invariance and matter-coupling gap for lifted C",
    },
    {
        "path": "373-one-observed-coframe-parent-selector-or-WEP-closure.md",
        "role": "one-observed-coframe selector/WEP closure theorem target",
    },
    {
        "path": "385-observed-coframe-selector-pullback-cancellation-theorem.md",
        "role": "selector pullback cancellation theorem attempt and no-go branches",
    },
    {
        "path": "387-identity-coframe-or-class-metric-fork.md",
        "role": "identity coframe versus class-metric fork and demotion rules",
    },
    {
        "path": "401-parent-matter-selector-theorem-attempt.md",
        "role": "selector-blind matter theorem attempt and counterexample block",
    },
    {
        "path": "407-primitive-relational-quotient-action-sketch.md",
        "role": "primitive quotient/readout parent-action sketch",
    },
    {
        "path": "409-runner-v4-red-team.md",
        "role": "runner-v4 false-promotion red-team discipline",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv",
        "role": "machine-readable runner-v4 state matrix",
    },
    {
        "path": "runs/20260602-052500-primitive-relational-quotient-action-sketch/results/variational_tests.csv",
        "role": "machine-readable quotient-action variational tests",
    },
    {
        "path": "runs/20260602-054500-runner-v4-red-team/results/manual_review_items.csv",
        "role": "machine-readable runner-v4 manual red-team review items",
    },
]


FUNCTOR_REQUIREMENTS = [
    {
        "requirement": "parent quotient object",
        "symbolic_form": "Q = X_parent / G_rel",
        "needed_for": "matter cannot distinguish representative selector variables Z_I",
        "current_status": "sketched_not_derived",
    },
    {
        "requirement": "observed geometry functor",
        "symbolic_form": "Obs: Q -> e_obs, g_obs[e_obs]",
        "needed_for": "one observed coframe and one matter metric",
        "current_status": "conditional_template",
    },
    {
        "requirement": "matter action factorization",
        "symbolic_form": "S_m = sum_A S_A[Psi_A, Obs(Q), omega[Obs(Q)], theta_A]",
        "needed_for": "selector-blind matter chain-rule zero",
        "current_status": "sufficient_axiom_not_parent_derived",
    },
    {
        "requirement": "selector-kernel condition",
        "symbolic_form": "d Obs(Q) / d Z_I = 0 for representative selectors Z_I",
        "needed_for": "R0 direct coframe slip theorem-zero",
        "current_status": "conditional_template",
    },
    {
        "requirement": "constant-sector independence",
        "symbolic_form": "d theta_A / d Z_I = 0 and d theta_A / d I_Q = 0 locally",
        "needed_for": "WEP/source charge and clock rows",
        "current_status": "not_derived",
    },
    {
        "requirement": "no material marker extension",
        "symbolic_form": "no parent variable m or P_active with matter vertices",
        "needed_for": "prevents hidden spurion/background route",
        "current_status": "not_derived",
    },
]


CONDITIONAL_PROOF_CHAIN = [
    {
        "step": 1,
        "claim": "Work on quotient data only.",
        "identity": "physical parent states are Q-objects, not labelled representatives x",
        "status": "premise_open",
    },
    {
        "step": 2,
        "claim": "Observed coframe is a functor of quotient data.",
        "identity": "e_obs = Obs(Q)",
        "status": "conditional_template",
    },
    {
        "step": 3,
        "claim": "Matter factors through the observed coframe and internal constants only.",
        "identity": "S_m = sum_A S_A[Psi_A, e_obs, omega[e_obs], theta_A]",
        "status": "sufficient_if_assumed",
    },
    {
        "step": 4,
        "claim": "Representative selectors lie in the observation kernel.",
        "identity": "partial_ZI e_obs = 0 and partial_ZI omega[e_obs] = 0",
        "status": "conditional_if_Obs_is_exact",
    },
    {
        "step": 5,
        "claim": "Species constants carry no selector or class charge.",
        "identity": "partial_ZI theta_A = 0 and local partial_IQ theta_A = 0",
        "status": "open_hard_part",
    },
    {
        "step": 6,
        "claim": "Chain rule gives selector-blind matter.",
        "identity": "delta S_m / delta Z_I | e_obs = 0",
        "status": "conditional_theorem_not_parent_derivation",
    },
]


COUNTEREXAMPLE_FUNCTORS = [
    {
        "counterexample": "class_metric_common_pullback",
        "construction": "S_A[Psi_A, exp(F(I_Q)) e_obs, theta_A]",
        "why_it_survives_quotient_language": "I_Q is quotient-invariant, so quotient invariance alone does not erase common-mode class response",
        "damage": "clock/gamma/fifth-force pressure remains unless F is locally zero or sourced below bounds",
    },
    {
        "counterexample": "marker_extended_quotient",
        "construction": "Q_tilde = (X_parent, m) / G_rel with S_A[Psi_A, e_obs, m]",
        "why_it_survives_quotient_language": "the marker descends to an allowed quotient object unless a no-marker theorem forbids it",
        "damage": "active/readout background can re-enter as material spurion",
    },
    {
        "counterexample": "species_internal_constants",
        "construction": "theta_A = theta_A(I_Q) or theta_A(Z_I)",
        "why_it_survives_quotient_language": "constants can be functorial data unless universality is derived",
        "damage": "WEP/source-charge and clock rows stay retained",
    },
    {
        "counterexample": "Ward_owned_counterstress",
        "construction": "matter sees class metric while selector stress cancels in total Ward ledger",
        "why_it_survives_quotient_language": "honest modified-gravity cancellation is not the same as matter selector blindness",
        "damage": "alpha3/Gdot/PPN rows remain flux-owner debts",
    },
    {
        "counterexample": "reduced_readout_EFT",
        "construction": "vary S_reduced[P_active, e_obs] instead of varying S_parent then reading out observables",
        "why_it_survives_quotient_language": "post-readout EFT terms can be written covariantly after projection",
        "damage": "R0 can look zero in a chosen closure while theorem-zero is not earned",
    },
]


MATTER_ARGUMENT_AUDIT = [
    {
        "argument": "Psi_A",
        "allowed_if": "matter species fields are ordinary local fields over observed geometry",
        "hazard": "species labels can smuggle source charges",
        "required_control": "universal species/source representation or retained WEP budget",
    },
    {
        "argument": "e_obs",
        "allowed_if": "single observed coframe is parent-selected",
        "hazard": "multiple coframes or class metrics create direct WEP/clock pressure",
        "required_control": "one-observed-coframe theorem",
    },
    {
        "argument": "omega[e_obs]",
        "allowed_if": "connection is induced only from e_obs",
        "hazard": "independent connection/source torsion terms create PPN channels",
        "required_control": "connection compatibility or retained operator ledger",
    },
    {
        "argument": "theta_A",
        "allowed_if": "constants are selector-independent and universal where needed",
        "hazard": "theta_A(I_Q) produces source/clock dependence",
        "required_control": "constant-sector no-charge theorem",
    },
    {
        "argument": "I_Q",
        "allowed_if": "used only in sectors whose local value/gradient is theorem-zero",
        "hazard": "quotient-invariant is not necessarily locally invisible",
        "required_control": "local class silence theorem or explicit bound",
    },
    {
        "argument": "P_active or marker m",
        "allowed_if": "never in parent bulk matter action",
        "hazard": "readout/marker extension spoils selector blindness",
        "required_control": "no-marker theorem and readout-after-variation rule",
    },
]


NO_CHEAT_RULES = [
    {
        "rule": "quotient invariance is not local invisibility",
        "forbidden_move": "call every quotient-invariant scalar unobservable",
        "safe_move": "prove its local value/gradient is absent or bound it as a retained channel",
    },
    {
        "rule": "factorization must be parent-derived",
        "forbidden_move": "declare S_m factors through Obs without deriving the allowed arguments",
        "safe_move": "label it conditional theorem/axiom until the parent action enforces it",
    },
    {
        "rule": "constant sector counts as matter coupling",
        "forbidden_move": "hide selector dependence in masses, charges, clocks, or measured GM",
        "safe_move": "audit theta_A and source normalization as explicit rows",
    },
    {
        "rule": "Ward cancellation is not selector blindness",
        "forbidden_move": "use total conservation to erase direct matter pullback",
        "safe_move": "either derive cancellation coefficients or keep flux rows retained",
    },
    {
        "rule": "readout is after variation",
        "forbidden_move": "vary an independent projected/reduced action and call it parent-origin",
        "safe_move": "vary parent first, then map observables through exact readout",
    },
]


ROW_TRANSITION_POLICY = [
    {
        "row_id": "R0_identity_coframe_direct",
        "attempted_upgrade": "closure_zero -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "closure_zero",
        "reason": "conditional chain-rule theorem exists only if matter factorization/no-marker/no-class-charge premises are parent-derived",
    },
    {
        "row_id": "R1_WEP_source_charge",
        "attempted_upgrade": "retained_contingent_budget -> theorem_zero_or_retained_source_current",
        "result": "not_upgraded",
        "new_state": "retained_contingent_budget",
        "reason": "species constants/source charges can be quotient-functor data unless universality is derived",
    },
    {
        "row_id": "R2_clock_redshift",
        "attempted_upgrade": "retained_budget -> theorem_zero_or_metric_clock_only",
        "result": "not_upgraded",
        "new_state": "retained_budget",
        "reason": "theta_A(I_Q) and common class metric counterexamples keep clock pressure alive",
    },
    {
        "row_id": "R7_alpha3",
        "attempted_upgrade": "retained_contingent_budget -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "retained_contingent_budget",
        "reason": "Ward-owned counterstress remains an open honest route, not a selector-blind proof",
    },
    {
        "row_id": "R9_Gdot",
        "attempted_upgrade": "retained_contingent_budget -> theorem_zero",
        "result": "not_upgraded",
        "new_state": "retained_contingent_budget",
        "reason": "measured-GM/source drift closure still needs independent source-normalization theorem",
    },
    {
        "row_id": "R11_EH_operator_ledger",
        "attempted_upgrade": "retained_residual -> EH_selected",
        "result": "not_upgraded",
        "new_state": "retained_residual",
        "reason": "matter functor theorem would not by itself derive metric-only second-order EH exterior",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The quotient-matter functor route gives a clean conditional theorem: if the parent action derives a quotient object Q, an observed-geometry functor Obs(Q), matter factorization through Obs(Q), selector-independent constants, and no marker/readout EFT extension, then the direct selector derivative of matter vanishes by the chain rule. That would be the right kind of proof for R0. But the existing corpus does not yet derive the factorization/no-marker/no-class-charge premises. Several counterexample functors remain legal under quotient language. Therefore R0 stays closure_zero rather than theorem_zero, and no local-GR claim is promoted.",
        "conditional_theorem_written": True,
        "quotient_matter_functor_parent_derived": False,
        "theorem_zero_upgrades": 0,
        "R0_new_state": "closure_zero",
        "local_GR_claim_allowed": False,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "wire runner-v4 into a future real-data/local-bound interface without changing its claim semantics",
        "pass_condition": "real-data commands write status/log/results and preserve theorem_zero versus closure_zero separation",
    },
    {
        "priority": 2,
        "target": "412-v4-source-charge-channel-map-review.md",
        "task": "review whether R1 source-charge stress should count three or four active channels",
        "pass_condition": "source-charge channel count is intentional and documented",
    },
    {
        "priority": 3,
        "target": "413-no-marker-parent-action-theorem-attempt.md",
        "task": "try to derive the no-marker theorem needed by the quotient-matter functor route",
        "pass_condition": "marker extension is either forbidden by parent symmetry or demoted to explicit closure",
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


def row_transition_rows() -> list[dict[str, Any]]:
    matrix_rows = read_csv(ROOT / "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv")
    matrix_by_id = {row["row_id"]: row for row in matrix_rows}
    rows: list[dict[str, Any]] = []
    for policy in ROW_TRANSITION_POLICY:
        source_row = matrix_by_id.get(policy["row_id"], {})
        rows.append(
            {
                "row_id": policy["row_id"],
                "previous_state": source_row.get("runner_v4_state", "missing"),
                "previous_zero_kind": source_row.get("zero_kind", "missing"),
                "attempted_upgrade": policy["attempted_upgrade"],
                "result": policy["result"],
                "new_state": policy["new_state"],
                "claim_allowed": False,
                "theorem_credit_allowed": False,
                "reason": policy["reason"],
            }
        )
    return rows


def gate_rows(
    source_rows: list[dict[str, Any]],
    transition_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    theorem_zero_upgrades = sum(1 for row in transition_rows if row["new_state"] == "theorem_zero")
    claim_allowed_rows = sum(1 for row in transition_rows if row["claim_allowed"])
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "functor_requirements_written",
            "status": "pass",
            "evidence": f"{len(FUNCTOR_REQUIREMENTS)} requirements recorded",
        },
        {
            "gate": "conditional_chain_rule_theorem_written",
            "status": "conditional_pass",
            "evidence": "delta S_m/delta Z_I vanishes only under factorization plus selector-independent constants",
        },
        {
            "gate": "counterexample_functors_written",
            "status": "pass",
            "evidence": f"{len(COUNTEREXAMPLE_FUNCTORS)} counterexamples recorded",
        },
        {
            "gate": "quotient_matter_functor_parent_derived",
            "status": "fail",
            "evidence": "factorization/no-marker/no-class-charge premises are not parent-derived",
        },
        {
            "gate": "no_marker_theorem_derived",
            "status": "fail",
            "evidence": "marker-extended quotient remains a legal counterexample",
        },
        {
            "gate": "R0_promoted_to_theorem_zero",
            "status": "fail",
            "evidence": f"{theorem_zero_upgrades} theorem-zero row upgrades",
        },
        {
            "gate": "claim_leaks",
            "status": "pass" if claim_allowed_rows == 0 else "fail",
            "evidence": f"{claim_allowed_rows} claim-allowed rows",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "matter functor attempt only; no EH/Newton/PPN/local-GR pass",
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


def write_checkpoint_markdown(
    run_dir: Path,
    transition_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, Any]],
) -> None:
    requirement_rows = [
        {
            "requirement": row["requirement"],
            "status": row["current_status"],
            "needed_for": row["needed_for"],
        }
        for row in FUNCTOR_REQUIREMENTS
    ]
    proof_rows = [
        {
            "step": row["step"],
            "claim": row["claim"],
            "status": row["status"],
        }
        for row in CONDITIONAL_PROOF_CHAIN
    ]
    counterexample_rows = [
        {
            "counterexample": row["counterexample"],
            "damage": row["damage"],
        }
        for row in COUNTEREXAMPLE_FUNCTORS
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
    text = f"""# 410 - Quotient-Matter Functor Theorem Attempt

Private quotient-matter/local-GR checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 409 showed runner-v4 is not leaking claims. This checkpoint attacks the key proof behind `R0`: can matter be forced to see only quotient-observed geometry, so the local selector derivative vanishes as a theorem rather than as a closure choice?

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/quotient_matter_functor_theorem_attempt.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Conditional Functor Theorem

If the parent theory supplies a quotient object `Q`, an observed-geometry functor `Obs(Q)=e_obs`, and matter factorization

```text
S_matter = sum_A S_A[Psi_A, Obs(Q), omega[Obs(Q)], theta_A]
```

with `partial_ZI Obs(Q)=0` and `partial_ZI theta_A=0` for representative selectors `Z_I`, then the direct matter selector pullback is zero:

```text
delta S_matter / delta Z_I | e_obs = 0
```

That is the right theorem shape. It is not yet a parent-derived theorem because the factorization, no-marker rule, and constant-sector independence are still open.

{markdown_table(requirement_rows, ["requirement", "status", "needed_for"])}

## 4. Proof Chain

{markdown_table(proof_rows, ["step", "claim", "status"])}

## 5. Counterexample Functors

{markdown_table(counterexample_rows, ["counterexample", "damage"])}

## 6. Row Transition Attempt

{markdown_table(transition_table_rows, ["row_id", "previous_state", "new_state", "result"])}

## 7. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 8. Decision

{DECISION[0]["decision"]}

Practical read: this route is still worth chasing because it has the exact GR-style flavour we want: a structural reason matter cannot see the forbidden selector. But quotient language alone is not enough. We need the parent action to forbid marker/class/constant-sector leakage, or runner-v4 must keep the local branch closure-labelled.

## 9. Next Target

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
    write_csv(results_dir / "functor_requirements.csv", FUNCTOR_REQUIREMENTS)
    write_csv(results_dir / "conditional_proof_chain.csv", CONDITIONAL_PROOF_CHAIN)
    write_csv(results_dir / "counterexample_functors.csv", COUNTEREXAMPLE_FUNCTORS)
    write_csv(results_dir / "matter_argument_audit.csv", MATTER_ARGUMENT_AUDIT)
    write_csv(results_dir / "row_transition_attempt.csv", transition_rows)
    write_csv(results_dir / "no_cheat_rules.csv", NO_CHEAT_RULES)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    failed_gates = [row for row in gate_result_rows if row["status"] == "fail"]
    conditional_gates = [row for row in gate_result_rows if row["status"] == "conditional_pass"]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "functor_requirements": len(FUNCTOR_REQUIREMENTS),
        "conditional_chain_steps": len(CONDITIONAL_PROOF_CHAIN),
        "counterexample_functors": len(COUNTEREXAMPLE_FUNCTORS),
        "theorem_zero_upgrades": sum(1 for row in transition_rows if row["new_state"] == "theorem_zero"),
        "quotient_matter_functor_parent_derived": False,
        "R0_new_state": "closure_zero",
        "local_GR_claim_allowed": False,
        "failed_gates_by_design": len(failed_gates),
        "conditional_gates": len(conditional_gates),
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
        description="Write checkpoint 410 quotient-matter functor theorem attempt artifacts."
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

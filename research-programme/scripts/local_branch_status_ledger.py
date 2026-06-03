from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-branch-status-ledger"
STATUS = "local_branch_strongly_gated_but_unpromoted_empirical_pivot_recommended"
CLAIM_CEILING = "conditional_local_residual_suppression_theorem_no_local_GR_or_PPN_promotion"


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
        (ROOT / "298-open-boundary-parent-sector-attempt.md", "effective open boundary sector"),
        (ROOT / "299-local-silence-selector-attempt.md", "exact local silence selector target"),
        (ROOT / "300-boundary-state-local-silence-theorem-attempt.md", "IR boundary-state theorem target"),
        (ROOT / "301-epsilon-loc-local-bound-runner.md", "epsilon_loc local-bound runner"),
        (ROOT / "302-epsilon-loc-parent-coefficient-map-attempt.md", "parent coefficient map"),
        (ROOT / "303-second-order-beta-response-attempt.md", "second-order beta response"),
        (ROOT / "304-epsilon-loc-beta-guard-update.md", "beta guard update"),
        (ROOT / "305-fifth-force-gradient-runner.md", "fifth-force gradient runner"),
        (ROOT / "306-trace-source-profile-theorem-attempt.md", "trace-source profile theorem target"),
        (ROOT / "runs" / "20260601-000127-epsilon-loc-local-bound-runner" / "results" / "promotion_gates.csv", "updated epsilon/beta gate outputs"),
        (ROOT / "runs" / "20260601-000128-fifth-force-gradient-runner" / "results" / "promotion_gates.csv", "gradient gate outputs"),
        (ROOT / "runs" / "20260601-000129-trace-source-profile-theorem-attempt" / "results" / "promotion_gates.csv", "profile theorem gate outputs"),
        (ROOT / "scripts" / "local_branch_status_ledger.py", "this ledger script"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def local_stack_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "layer": "open_boundary_sector",
            "status": "constructed_effective_conditional",
            "earned": "q_r/q_a open sector, Gamma_D positivity contract, and scalar trace-source route are explicit",
            "blocker": "noise/FDT state, full covariant Ward identity, and local silence selector are not parent-derived",
            "next_requirement": "derive boundary state plus Bianchi-compatible conservation identity from the parent action",
            "source_paths": "298-open-boundary-parent-sector-attempt.md",
        },
        {
            "layer": "local_silence_selector",
            "status": "exact_sufficient_condition_written",
            "earned": "sigma_D=0 exactly turns off the local open-sector source",
            "blocker": "parent theory has not proved local domains force sigma_D=0 while cosmology remains active",
            "next_requirement": "prove local closed/gapped IR boundary class and FLRW open/nontrivial class are selected dynamically",
            "source_paths": "299-local-silence-selector-attempt.md;300-boundary-state-local-silence-theorem-attempt.md",
        },
        {
            "layer": "epsilon_loc_runner",
            "status": "quantitative_proxy_gate_ready",
            "earned": "exact silence passes, small leakage can pass, and deliberate failure probes fail",
            "blocker": "bounds are proxy/internal and coefficients are not a published PPN manifest",
            "next_requirement": "replace proxy thresholds with an official local-observable manifest only after parent coefficients are owned",
            "source_paths": "301-epsilon-loc-local-bound-runner.md;304-epsilon-loc-beta-guard-update.md",
        },
        {
            "layer": "gamma_clock_matter_channels",
            "status": "conditionally_suppressed",
            "earned": "trace-only common mode gives c_gamma=0; universal metric coupling kills direct clock/matter channels",
            "blocker": "trace-only projection and universal coupling are contracts, not parent theorems",
            "next_requirement": "derive the metric projection and matter coupling from the action rather than imposing them",
            "source_paths": "302-epsilon-loc-parent-coefficient-map-attempt.md",
        },
        {
            "layer": "second_order_beta_channel",
            "status": "formula_derived_parent_relation_missing",
            "earned": "beta_eff=B/A^2 and c_beta=b1-2a1 are explicit; the guard uses |c_beta|=2 for linear leakage",
            "blocker": "parent field equation has not proved B=A^2 or an equivalent second-order mass-renormalization law",
            "next_requirement": "derive the second-order local weak-field response from the parent action",
            "source_paths": "303-second-order-beta-response-attempt.md;304-epsilon-loc-beta-guard-update.md",
        },
        {
            "layer": "fifth_force_gradient_channel",
            "status": "gradient_gate_ready_profile_parent_missing",
            "earned": "exact, constant, tiny, or very flat trace-source profiles can pass; local gradients are caught",
            "blocker": "parent theory has not derived the profile scale or no-gradient boundary conditions",
            "next_requirement": "derive flatness or sufficient profile length scale from the local boundary-value problem",
            "source_paths": "305-fifth-force-gradient-runner.md;306-trace-source-profile-theorem-attempt.md",
        },
        {
            "layer": "flat_profile_theorem",
            "status": "conditional_theorem",
            "earned": "constant source plus Neumann no-flux boundary gives grad s_D=0",
            "blocker": "Neumann/no-inhomogeneous-source conditions are not parent-owned",
            "next_requirement": "show local domains enforce no trace-source flux and no spatially varying j_s",
            "source_paths": "306-trace-source-profile-theorem-attempt.md",
        },
        {
            "layer": "combined_local_residual_suppression",
            "status": "conditional_theorem_not_promotion",
            "earned": "if selector/profile/beta/universal-coupling premises hold, the local residual vector is zero or bounded",
            "blocker": "the key premises are still contracts or conditional theorems",
            "next_requirement": "turn each premise into a parent theorem before claiming local GR/PPN recovery",
            "source_paths": "299-local-silence-selector-attempt.md;302-epsilon-loc-parent-coefficient-map-attempt.md;303-second-order-beta-response-attempt.md;305-fifth-force-gradient-runner.md;306-trace-source-profile-theorem-attempt.md",
        },
    ]


def combined_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "premise_id": "P1",
            "premise": "universal metric matter coupling",
            "mathematical_condition": "delta S_m/dq_open = 0 except through g_eff",
            "derived_effect": "direct clock and direct matter WEP channels vanish",
            "current_status": "conditional_contract",
            "missing_parent_step": "derive matter coupling from the parent action",
        },
        {
            "premise_id": "P2",
            "premise": "trace-only common mode for local leakage",
            "mathematical_condition": "delta g_ij proportional to Phi delta_ij at leading local order",
            "derived_effect": "c_gamma=0, so gamma-1 is suppressed at first order",
            "current_status": "conditional_contract",
            "missing_parent_step": "derive trace-only projection instead of imposing it",
        },
        {
            "premise_id": "P3a",
            "premise": "exact local selector silence",
            "mathematical_condition": "sigma_D=0",
            "derived_effect": "epsilon_loc=0 and all local open-sector residuals vanish in the runner",
            "current_status": "exact_sufficient_condition",
            "missing_parent_step": "derive the local closed/gapped boundary-state selector",
        },
        {
            "premise_id": "P3b",
            "premise": "flat nonzero trace source alternative",
            "mathematical_condition": "j_s constant and n.grad s_D=0 on boundary D",
            "derived_effect": "grad s_D=0, so fifth-force-like residual vanishes despite nonzero epsilon_loc",
            "current_status": "conditional_theorem",
            "missing_parent_step": "derive Neumann/no-inhomogeneous-source conditions",
        },
        {
            "premise_id": "P4",
            "premise": "second-order beta closure",
            "mathematical_condition": "B=A^2 or equivalently c_beta=b1-2a1=0",
            "derived_effect": "beta_eff=1 and beta-1 is removed at second weak-field order",
            "current_status": "formula_derived_parent_relation_missing",
            "missing_parent_step": "derive B=A^2 from the local field equation",
        },
        {
            "premise_id": "P5",
            "premise": "profile-scale bound for residual gradients",
            "mathematical_condition": "epsilon_loc * shape_factor * L_test/L_profile below manifest bound",
            "derived_effect": "nonzero leakage remains locally safe if sufficiently tiny or flat",
            "current_status": "proxy_runner_ready",
            "missing_parent_step": "replace proxy bound and profile scale with official local-observable manifest",
        },
    ]


def residual_vector_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "component": "gamma_minus_1",
            "proxy_expression": "c_gamma * epsilon_loc",
            "zero_or_bound_condition": "c_gamma=0 under trace-only common mode, or epsilon_loc=0",
            "current_status": "conditionally_suppressed",
            "blocker": "trace-only common mode not parent-derived",
        },
        {
            "component": "beta_minus_1",
            "proxy_expression": "c_beta * epsilon_loc with c_beta=b1-2a1",
            "zero_or_bound_condition": "B=A^2 gives c_beta=0; runner guard uses |c_beta|=2 for linear leakage",
            "current_status": "formula_derived_guarded_not_parent_owned",
            "blocker": "second-order relation B=A^2 not derived",
        },
        {
            "component": "fifth_force_ratio",
            "proxy_expression": "epsilon_loc * shape_factor * L_test/L_profile",
            "zero_or_bound_condition": "epsilon_loc=0, shape_factor=0, or L_profile sufficiently large",
            "current_status": "runner_ready_conditional_profile_theorem",
            "blocker": "profile shape and official bound not parent-owned",
        },
        {
            "component": "clock_residual",
            "proxy_expression": "c_clock * epsilon_loc",
            "zero_or_bound_condition": "universal metric coupling gives c_clock=0",
            "current_status": "conditionally_suppressed",
            "blocker": "universal coupling not parent-derived",
        },
        {
            "component": "matter_nonuniversality",
            "proxy_expression": "c_matter * epsilon_loc",
            "zero_or_bound_condition": "universal metric coupling gives c_matter=0",
            "current_status": "conditionally_suppressed",
            "blocker": "direct matter channel not ruled out by parent theorem",
        },
        {
            "component": "local_conservation_leak",
            "proxy_expression": "nabla_mu Delta T_eff^{mu nu}",
            "zero_or_bound_condition": "Bianchi-compatible Ward identity for the open sector",
            "current_status": "not_closed",
            "blocker": "full covariant conservation identity missing",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    source_missing = [source for source in source_register_rows() if source["exists"] != "yes"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not source_missing else "fail",
            "evidence": "all cited local-branch checkpoints and scripts exist" if not source_missing else ";".join(source["source"] for source in source_missing),
            "claim_effect": "ledger traceable",
        },
        {
            "gate": "open_sector_constructed",
            "status": "pass",
            "evidence": "checkpoint 298 constructs q_r/q_a sector and trace source route",
            "claim_effect": "local branch has an effective open-sector language",
        },
        {
            "gate": "exact_silence_condition_written",
            "status": "pass",
            "evidence": "sigma_D=0 gives exact local source silence",
            "claim_effect": "there is a clean sufficient local-suppression condition",
        },
        {
            "gate": "conditional_local_suppression_theorem_written",
            "status": "pass",
            "evidence": "combined residual vector closes if selector/profile/beta/universal-coupling premises hold",
            "claim_effect": "local branch has a precise theorem target",
        },
        {
            "gate": "local_selector_parent_derived",
            "status": "fail",
            "evidence": "no parent theorem forces sigma_D=0 in local domains",
            "claim_effect": "exact silence cannot be promoted",
        },
        {
            "gate": "universal_metric_coupling_parent_derived",
            "status": "fail",
            "evidence": "universal matter coupling is still a contract",
            "claim_effect": "clock/matter channel not officially closed",
        },
        {
            "gate": "beta_parent_relation_derived",
            "status": "fail",
            "evidence": "B=A^2 has not been derived",
            "claim_effect": "beta channel remains conditional",
        },
        {
            "gate": "fifth_force_gradient_gate_ready",
            "status": "pass",
            "evidence": "checkpoint 305 catches local gradient failure probes",
            "claim_effect": "fifth-force residuals are no longer hand-waved",
        },
        {
            "gate": "flat_profile_theorem_conditional",
            "status": "conditional_pass",
            "evidence": "constant source plus Neumann no-flux gives grad s_D=0",
            "claim_effect": "nonzero epsilon has one mathematically clean local-safe route",
        },
        {
            "gate": "profile_parent_derived",
            "status": "fail",
            "evidence": "Neumann/no-inhomogeneous-source conditions are not parent-owned",
            "claim_effect": "flat profile cannot be assumed as local-GR recovery",
        },
        {
            "gate": "official_PPN_claim_allowed",
            "status": "fail",
            "evidence": "current thresholds are proxy/internal and key coefficients remain conditional",
            "claim_effect": "no public PPN/local-GR claim",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "selector, beta relation, universal coupling, and profile theorem remain conditional",
            "claim_effect": "local branch remains effective closure only",
        },
        {
            "gate": "B_mem_parent_derived",
            "status": "fail",
            "evidence": "local branch gates do not derive 2/27",
            "claim_effect": "B_mem remains empirical closure/theorem target",
        },
        {
            "gate": "empirical_pivot_recommended",
            "status": "pass",
            "evidence": "local branch is now well-gated enough to stop pretending it is settled",
            "claim_effect": "next value is holdout testing or a parent theorem attempt, not more local patching",
        },
    ]


def allowed_forbidden_claim_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_type": "allowed_private",
            "claim": "MTS now has a conditional local residual suppression theorem target.",
            "reason": "the residual vector closes if the listed selector/profile/beta/universal-coupling premises hold",
        },
        {
            "claim_type": "allowed_private",
            "claim": "Exact local silence is sufficient for zero local open-sector residuals in the current runner.",
            "reason": "sigma_D=0 maps to epsilon_loc=0",
        },
        {
            "claim_type": "allowed_private",
            "claim": "Nonzero local leakage can be safe if it is a constant or sufficiently flat trace renormalization.",
            "reason": "constant source plus Neumann no-flux gives grad s_D=0, and the runner tests flatness",
        },
        {
            "claim_type": "forbidden",
            "claim": "MTS has derived local GR or passed official PPN tests.",
            "reason": "selector, universal coupling, beta closure, profile theorem, and official bounds are not parent-owned",
        },
        {
            "claim_type": "forbidden",
            "claim": "MTS has proved there is no fifth force.",
            "reason": "localized trace sources or boundary mismatch generically create gradients",
        },
        {
            "claim_type": "forbidden",
            "claim": "B_mem=2/27 or Hstar=H0 is parent-derived.",
            "reason": "the local branch does not derive either global amplitude closure",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "target": "empirical_holdout_pivot",
            "question": "Does the no-clock/B_mem=2/27 branch survive stricter holdouts against fitted baselines?",
            "why_now": "local branch is gated but not promotable; empirical pressure can still guide which theorem target matters",
            "success_condition": "MTS stays competitive under blind splits without relying on edge priors or one-data-set pressure",
        },
        {
            "priority": 2,
            "target": "selector_parent_theorem",
            "question": "Can local closed/gapped domains force sigma_D=0 while FLRW domains remain open/nontrivial?",
            "why_now": "this is the cleanest exact local-GR route",
            "success_condition": "derive local silence as a boundary-state theorem, not an axiom",
        },
        {
            "priority": 3,
            "target": "profile_parent_theorem",
            "question": "Can Neumann/no-inhomogeneous-source conditions be derived for local trace-source profiles?",
            "why_now": "this is the cleanest nonzero-leakage local-safe route",
            "success_condition": "derive grad s_D=0 or a bound on L_profile/L_test from the action",
        },
        {
            "priority": 4,
            "target": "second_order_beta_parent_relation",
            "question": "Can the local weak-field expansion force B=A^2?",
            "why_now": "beta remains the central post-Newtonian algebraic blocker",
            "success_condition": "derive beta_eff=1 without fitting or imposing the second-order coefficient",
        },
        {
            "priority": 5,
            "target": "official_local_manifest",
            "question": "What exact local PPN/fifth-force observables and baselines should the branch face?",
            "why_now": "proxy gates are useful but not evidence",
            "success_condition": "replace proxy thresholds with cited observables and a GR baseline pipeline",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "decision": "local branch is mathematically sharper and no longer vague, but remains unpromoted",
            "recommended_next": "pivot to empirical holdout testing or attack one parent theorem directly",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"

    outputs = {
        "source_register": source_register_rows(),
        "local_stack_status": local_stack_status_rows(),
        "combined_theorem": combined_theorem_rows(),
        "residual_vector_contract": residual_vector_contract_rows(),
        "promotion_gates": promotion_gate_rows(),
        "allowed_forbidden_claims": allowed_forbidden_claim_rows(),
        "next_targets": next_target_rows(),
        "decision": decision_rows(),
    }

    write_csv(results_dir / "source_register.csv", outputs["source_register"], ["source", "role", "exists"])
    write_csv(
        results_dir / "local_stack_status.csv",
        outputs["local_stack_status"],
        ["layer", "status", "earned", "blocker", "next_requirement", "source_paths"],
    )
    write_csv(
        results_dir / "combined_theorem.csv",
        outputs["combined_theorem"],
        ["premise_id", "premise", "mathematical_condition", "derived_effect", "current_status", "missing_parent_step"],
    )
    write_csv(
        results_dir / "residual_vector_contract.csv",
        outputs["residual_vector_contract"],
        ["component", "proxy_expression", "zero_or_bound_condition", "current_status", "blocker"],
    )
    write_csv(
        results_dir / "promotion_gates.csv",
        outputs["promotion_gates"],
        ["gate", "status", "evidence", "claim_effect"],
    )
    write_csv(
        results_dir / "allowed_forbidden_claims.csv",
        outputs["allowed_forbidden_claims"],
        ["claim_type", "claim", "reason"],
    )
    write_csv(
        results_dir / "next_targets.csv",
        outputs["next_targets"],
        ["priority", "target", "question", "why_now", "success_condition"],
    )
    write_csv(results_dir / "decision.csv", outputs["decision"], ["status", "claim_ceiling", "decision", "recommended_next"])

    payload = {
        "run_slug": RUN_SLUG,
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": relpath(run_dir),
        "outputs": {name: len(rows) for name, rows in outputs.items()},
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "COMPLETE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the local branch status ledger and conditional suppression theorem.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "memory-stress-exchange-normalization-or-kappa-mem-free"
STATUS = (
    "kappa_mem_not_fixed_by_Bianchi_or_topology_Bmem_2over27_requires_"
    "separate_stress_normalization_theorem_closure_only"
)
CLAIM_CEILING = "kappa_mem_free_until_parent_stress_exchange_normalization_derived"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"
Q_RANK = 2.0 / 27.0


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (
            "amplitude normalization gate",
            ROOT / "82-amplitude-normalization-gate.md",
            "amplitude classifications and risk register",
        ),
        (
            "memory stress amplitude attempt",
            ROOT / "92-memory-stress-amplitude-prediction-attempt.md",
            "stress-exchange corridor and B_mem integral budget",
        ),
        (
            "memory perturbation owner attempt",
            ROOT / "178-memory-perturbation-owner-attempt.md",
            "effective conserved stress owner and perturbation limits",
        ),
        (
            "rank closure lock",
            ROOT / "254-rank-27-rank-2-cell-theorem-or-Bmem-closure-lock.md",
            "rank fraction target and closure lock",
        ),
        (
            "254 closure table",
            ROOT
            / "runs"
            / "20260601-000071-rank-27-rank-2-cell-theorem-or-Bmem-closure-lock"
            / "results"
            / "Bmem_closure_lock.csv",
            "machine-readable closure status",
        ),
    ]
    return [
        {
            "source": source,
            "path": relpath(path),
            "exists": "yes" if path.exists() else "no",
            "use_in_255": use,
        }
        for source, path, use in sources
    ]


def stress_equation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "equation": "q_rank = Tr(P_active)/dim(V_cell) = 2/27",
            "derivation_status": "closure_target_from_254",
            "what_it_fixes": "dimensionless channel fraction if rank theorem later succeeds",
            "what_it_does_not_fix": "stress normalization kappa_mem",
        },
        {
            "step": 2,
            "equation": "Omega_mem(N) = kappa_mem q_rank F(N)",
            "derivation_status": "definition_of_response_normalization",
            "what_it_fixes": "separates rank fraction from stress amplitude",
            "what_it_does_not_fix": "value of kappa_mem",
        },
        {
            "step": 3,
            "equation": "S_mem(N)=dOmega_mem/dN=kappa_mem q_rank F'(N)",
            "derivation_status": "identity",
            "what_it_fixes": "source profile once F and kappa_mem are supplied",
            "what_it_does_not_fix": "integrated source budget",
        },
        {
            "step": 4,
            "equation": "int_0^infty S_mem dN = kappa_mem q_rank",
            "derivation_status": "identity_if_F(0)=0_and_F(infty)=1",
            "what_it_fixes": "B_mem equals integrated memory-source budget",
            "what_it_does_not_fix": "why the budget equals q_rank rather than kappa_mem q_rank",
        },
        {
            "step": 5,
            "equation": "rho_mem' = 3(rho_mem+p_mem) for N=ln(a0/a)",
            "derivation_status": "Bianchi_continuity_identity",
            "what_it_fixes": "pressure required for a conserved effective memory fluid",
            "what_it_does_not_fix": "normalization of rho_mem",
        },
        {
            "step": 6,
            "equation": "p_mem = -rho_mem + rho_mem'/3",
            "derivation_status": "derived_from_continuity",
            "what_it_fixes": "effective equation of state for any chosen amplitude",
            "what_it_does_not_fix": "kappa_mem because amplitude cancels in w_mem",
        },
    ]


def kappa_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt": "Bianchi_conservation",
            "result": "fails_to_fix_kappa",
            "reason": "continuity fixes pressure/equation-of-state response for a supplied rho_mem, not rho_mem normalization",
            "allowed_use": "consistency check only",
        },
        {
            "attempt": "topological_projector_rank",
            "result": "fixes_fraction_not_stress",
            "reason": "rank fraction is dimensionless; it does not produce a metric stress tensor by itself",
            "allowed_use": "amplitude theorem target q_rank",
        },
        {
            "attempt": "pure_topological_action",
            "result": "cannot_source_FLRW_bulk_stress",
            "reason": "a metric-independent topological term has zero bulk metric variation",
            "allowed_use": "local N5 silence, not cosmology amplitude",
        },
        {
            "attempt": "metric_dependent_memory_stress",
            "result": "introduces_coupling",
            "reason": "to affect H^2 the memory sector needs metric variation with a coupling or normalization constant",
            "allowed_use": "valid route only if coupling is parent-fixed",
        },
        {
            "attempt": "trace_corridor",
            "result": "bounds_not_prediction",
            "reason": "B_mem=a_F DeltaR/(3 eta^2) still leaves a_F, DeltaR, and eta unowned",
            "allowed_use": "discipline prior/corridor",
        },
        {
            "attempt": "effective_scalar_reconstruction",
            "result": "legal_EFT_not_parent_derivation",
            "reason": "a reconstructed potential can conserve the stress but inherits the chosen background amplitude",
            "allowed_use": "perturbation proxy only",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "no_go": "Bianchi_amplitude_no_go",
            "statement": "For a conserved effective fluid, multiplying rho_mem by a constant leaves the continuity equation valid.",
            "consequence": "Bianchi identity cannot choose kappa_mem.",
            "escape_route": "derive a source normalization from a parent action or quantized charge.",
        },
        {
            "no_go": "topology_stress_no_go",
            "statement": "The same metric independence that protects local N5 removes bulk stress from the topological term.",
            "consequence": "P_D can select a channel but cannot by itself drive FLRW H^2.",
            "escape_route": "separate topological selector from metric stress response and derive their coupling.",
        },
        {
            "no_go": "rank_fraction_units_no_go",
            "statement": "Tr(P)/dim(V) is dimensionless bookkeeping, not an energy density.",
            "consequence": "q_rank needs kappa_mem or an equivalent stress map.",
            "escape_route": "derive a unit-normalized exchange current with int S_unit dN=1.",
        },
        {
            "no_go": "corridor_degeneracy_no_go",
            "statement": "B_mem=a_F DeltaR/(3 eta^2) contains multiple parent-side unknowns.",
            "consequence": "order-one compatibility is not a prediction.",
            "escape_route": "fix eta, a_F, and DeltaR independently before using data.",
        },
        {
            "no_go": "kappa_equals_one_by_choice",
            "statement": "Setting kappa_mem=1 because it makes B_mem=2/27 is a closure choice.",
            "consequence": "lead branch can be tested, not promoted.",
            "escape_route": "derive kappa_mem=1 from normalization of the stress-exchange action.",
        },
    ]


def closure_branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "strict_lead_closure",
            "formula": "B_mem = 2/27",
            "parameter_status": "fixed_closure",
            "use": "hard empirical stress test of lead branch",
            "claim": "not parent-derived",
        },
        {
            "branch": "kappa_ablation",
            "formula": "B_mem = kappa_mem (2/27)",
            "parameter_status": "one_amplitude_ablation",
            "use": "diagnose whether fixed 2/27 is too strict",
            "claim": "phenomenological only",
        },
        {
            "branch": "corridor_prior",
            "formula": "B_mem=a_F DeltaR/(3 eta^2)",
            "parameter_status": "bounded_corridor",
            "use": "private discipline bound before broad data tests",
            "claim": "bound not prediction",
        },
        {
            "branch": "parent_prediction_future",
            "formula": "kappa_mem fixed by S_memory variation",
            "parameter_status": "theorem_target",
            "use": "only route to promotion",
            "claim": "not available now",
        },
    ]


def next_derivation_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "target": "unit_normalized_exchange_current",
            "why": "the cleanest way to force kappa_mem=1",
            "success_condition": "derive int S_unit dN=1 before fitting B_mem",
        },
        {
            "rank": 2,
            "target": "metric_stress_response_action",
            "why": "topological selector alone has no bulk stress",
            "success_condition": "delta_g S_memory gives rho_mem with fixed coefficient",
        },
        {
            "rank": 3,
            "target": "trace_corridor_parameter_ownership",
            "why": "existing corridor is promising but underdetermined",
            "success_condition": "derive eta, a_F, and DeltaR independently",
        },
        {
            "rank": 4,
            "target": "kappa_ablation_test_manifest",
            "why": "testing fixed versus kappa-free branch tells us how punitive closure is",
            "success_condition": "fit fixed 2/27, kappa-free, and standard baselines with same pipeline",
        },
    ]


def claim_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "kappa_mem is fixed by Bianchi identity",
            "status": "forbidden",
            "reason": "Bianchi fixes pressure/conservation response, not amplitude normalization",
        },
        {
            "claim": "topology alone predicts B_mem",
            "status": "forbidden",
            "reason": "metric-independent topology has no bulk stress; rank fraction needs a stress map",
        },
        {
            "claim": "B_mem=2/27 remains the strict lead closure",
            "status": "allowed",
            "reason": "usable as a hard empirical branch, with no parent-prediction claim",
        },
        {
            "claim": "kappa-free branch may be tested",
            "status": "allowed_ablation",
            "reason": "diagnostic only; extra freedom must be penalized against baselines",
        },
        {
            "claim": "MTS derives cosmology amplitude",
            "status": "forbidden",
            "reason": "stress-exchange normalization theorem is missing",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_register_rows())
    no_go_count = len(no_go_rows())
    kappa_fail = any(row["attempt"] == "Bianchi_conservation" and row["result"] == "fails_to_fix_kappa" for row in kappa_attempt_rows())
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "promotion_allowed": "false",
        },
        {
            "gate": "Bianchi normalization test performed",
            "status": "pass" if kappa_fail else "fail",
            "evidence": "continuity leaves amplitude free",
            "promotion_allowed": "false",
        },
        {
            "gate": "topology/stress split explicit",
            "status": "pass",
            "evidence": "topology selects channel; stress action must set amplitude",
            "promotion_allowed": "conditional future only",
        },
        {
            "gate": "no-go lemmas written",
            "status": "pass" if no_go_count >= 5 else "fail",
            "evidence": f"no_go_count={no_go_count}",
            "promotion_allowed": "false",
        },
        {
            "gate": "kappa_mem fixed",
            "status": "fail",
            "evidence": "unit-normalized exchange current or stress action missing",
            "promotion_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "meaning": (
                "Bianchi conservation and topological projector ownership cannot fix kappa_mem. "
                "Bianchi supplies the pressure/conservation response for any chosen amplitude; a purely topological "
                "projector has zero bulk metric stress; and a metric-dependent memory stress term introduces a "
                "normalization/coupling unless a parent action fixes it. Therefore B_mem=2/27 remains a strict "
                "lead closure branch, while B_mem=kappa_mem(2/27) is only an ablation branch."
            ),
            "q_rank": f"{Q_RANK:.12f}",
            "promotion_allowed": "false",
            "next_target": "256-fixed-2over27-vs-kappa-free-cosmology-test-manifest.md",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_id = f"{timestamp}-{RUN_SLUG}"
    run_dir = ROOT / "runs" / run_id
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (
            source_register_rows(),
            ["source", "path", "exists", "use_in_255"],
        ),
        "stress_normalization_equations.csv": (
            stress_equation_rows(),
            ["step", "equation", "derivation_status", "what_it_fixes", "what_it_does_not_fix"],
        ),
        "kappa_derivation_attempts.csv": (
            kappa_attempt_rows(),
            ["attempt", "result", "reason", "allowed_use"],
        ),
        "normalization_no_go_lemmas.csv": (
            no_go_rows(),
            ["no_go", "statement", "consequence", "escape_route"],
        ),
        "closure_branch_policy.csv": (
            closure_branch_rows(),
            ["branch", "formula", "parameter_status", "use", "claim"],
        ),
        "next_derivation_queue.csv": (
            next_derivation_queue_rows(),
            ["rank", "target", "why", "success_condition"],
        ),
        "claim_policy_after_255.csv": (
            claim_policy_rows(),
            ["claim", "status", "reason"],
        ),
        "claim_gate_results.csv": (
            claim_gate_rows(),
            ["gate", "status", "evidence", "promotion_allowed"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "lead_branch", "meaning", "q_rank", "promotion_allowed", "next_target"],
        ),
    }

    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status_payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "missing_sources": sum(row["exists"] != "yes" for row in source_register_rows()),
        "q_rank": f"{Q_RANK:.12f}",
        "kappa_mem_fixed_by_Bianchi": False,
        "kappa_mem_fixed_by_topology": False,
        "kappa_mem_parent_derived": False,
        "Bmem_2over27_strict_closure": True,
        "kappa_free_branch_allowed_as_ablation": True,
        "promotion_allowed": False,
        "next_target": "256-fixed-2over27-vs-kappa-free-cosmology-test-manifest.md",
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return status_payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build checkpoint 255: memory stress-exchange normalization or kappa_mem remains free."
    )
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

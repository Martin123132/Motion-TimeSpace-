from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "amplitude-closure-claim-ledger-update"
STATUS = "claim_ledger_updated_Bmem_2over27_explicit_closure_not_parent_derived"
CLAIM_CEILING = "ledger_update_no_parent_derivation_claims"


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
        (ROOT / "330-official-wrapper-locked-branch-release-split.md", "latest locked 2/27 DR1/DR2 empirical scorecard"),
        (ROOT / "331-trace-normalized-Hamiltonian-amplitude-contract.md", "B_mem factorization and original amplitude theorem target"),
        (ROOT / "337-exact-parent-pullback-selection-rule-gate.md", "conditional exact-readout theorem"),
        (ROOT / "342-finite-fibre-basis-relabeling-gate.md", "finite-fibre conditional mechanism"),
        (ROOT / "343-dim27-rank2-origin-closure-decision-gate.md", "amplitude closure decision"),
        (Path(__file__).resolve(), "this ledger verifier"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": path.exists(),
            "issue": "" if path.exists() else "missing",
        }
        for path, role in sources
    ]


def claim_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_id": "A1_Bmem_2over27",
            "object": "B_mem = 2/27",
            "current_status": "explicit_closure_value",
            "evidence_basis": "343 closure decision after dim/rank derivation failed",
            "allowed_claim": "locked empirical closure branch and theorem target",
            "forbidden_claim": "parent-derived amplitude",
            "next_action": "test as fixed branch; do not spend more cycles claiming derivation without new parent theorem",
        },
        {
            "claim_id": "A2_epsilonH_unit",
            "object": "epsilon_H = 1",
            "current_status": "closure_or_fitted_coupling; conditional theorem under exact readout",
            "evidence_basis": "337 exact-readout theorem plus 343 closure decision",
            "allowed_claim": "unit value in locked closure branch",
            "forbidden_claim": "unconditional Hamiltonian normalization derived from parent action",
            "next_action": "only reopen if parent action derives exact readout/no-marker/dim/rank/Hstar chain",
        },
        {
            "claim_id": "A3_qtrace_2over27",
            "object": "q_trace = rank(P_active)/dim(V_cell) = 2/27",
            "current_status": "conditional algebraic identity, not parent-owned",
            "evidence_basis": "342 identity-current rank readout; 343 dim/rank not parent-derived",
            "allowed_claim": "exact if rank=2 and dim=27 are assumed",
            "forbidden_claim": "rank and dimension derived by MTS parent action",
            "next_action": "record as algebraic spine for future theorem, not current derivation",
        },
        {
            "claim_id": "A4_Hstar_H0",
            "object": "H_star = H0",
            "current_status": "closure/theorem target",
            "evidence_basis": "331 factorization leaves H_star/H0 as required factor",
            "allowed_claim": "fixed calibration in locked branch",
            "forbidden_claim": "parent-derived calibration",
            "next_action": "treat as independent theory gate if amplitude branch is revisited",
        },
        {
            "claim_id": "E1_locked_late_time_branch",
            "object": "no-clock locked B_mem=2/27, u3=1/4 branch",
            "current_status": "empirical closure branch retained",
            "evidence_basis": "330 DR1/DR2 locked branch retained; 343 closure demotion does not discard it",
            "allowed_claim": "late-time fixed-closure branch is competitive enough to keep testing",
            "forbidden_claim": "stable cosmological evidence or fundamental derivation",
            "next_action": "run robustness/holdout comparisons and keep baselines fair",
        },
        {
            "claim_id": "T1_finite_fibre_route",
            "object": "finite-fibre basis relabeling route",
            "current_status": "conditional mechanism",
            "evidence_basis": "342 verifies trace/spectral basis invariance and fixed P_active failure",
            "allowed_claim": "possible future parent theorem route",
            "forbidden_claim": "current proof of dim=27/rank=2/no-marker",
            "next_action": "freeze unless genuinely new parent construction is supplied",
        },
        {
            "claim_id": "T2_exact_readout_route",
            "object": "P_active as source/relational readout",
            "current_status": "conditional mechanism",
            "evidence_basis": "337-342 readout, Ward, quotient, finite-fibre gates",
            "allowed_claim": "counterterm is forbidden if exact readout/no-marker premises hold",
            "forbidden_claim": "P_active readout status parent-derived",
            "next_action": "do not use to promote amplitude; use only as theorem target",
        },
        {
            "claim_id": "L1_local_GR_PPN",
            "object": "local GR/PPN reduction",
            "current_status": "independent unresolved gate",
            "evidence_basis": "not changed by 343 amplitude closure decision",
            "allowed_claim": "separate theory gate remains necessary",
            "forbidden_claim": "local GR/PPN derived from amplitude closure",
            "next_action": "return to local GR/PPN only as independent derivation/closure audit",
        },
        {
            "claim_id": "C1_CMB_growth_bridge",
            "object": "CMB/growth perturbation bridge",
            "current_status": "independent unresolved gate",
            "evidence_basis": "late-time closure scores do not derive perturbations",
            "allowed_claim": "needs separate robustness and perturbation owner",
            "forbidden_claim": "CMB/growth safety from SN/BAO closure score alone",
            "next_action": "run bridge/killscreen gates after empirical ledger update",
        },
    ]


def transition_rows() -> list[dict[str, Any]]:
    return [
        {
            "transition": "amplitude_derivation_to_closure",
            "before_343": "B_mem=2/27 was a locked empirical lead and active theorem target",
            "after_343": "B_mem=2/27 is explicit closure and theorem target, not derived",
            "reason": "dim=27, rank=2, no-marker, effective stability, and Hstar ownership not proven",
        },
        {
            "transition": "theory_claim_ceiling",
            "before_343": "conditional exact-readout and finite-fibre mechanisms were being chased",
            "after_343": "mechanisms are archived as conditional routes only",
            "reason": "repeated gates sharpened but did not close parent ownership",
        },
        {
            "transition": "empirical_program",
            "before_343": "locked branch risked being described as near-derived",
            "after_343": "locked branch is a disciplined fixed-closure test pillar",
            "reason": "closure label makes empirical comparisons cleaner and less overclaimed",
        },
    ]


def next_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_next_gate": "empirical_locked_branch_robustness",
            "why": "now that amplitude is closure, testing is the productive path",
            "first_output": "post-343 locked closure robustness manifest",
            "claim_ceiling": "empirical_closure_scorecard_only",
            "priority": 1,
        },
        {
            "candidate_next_gate": "Hstar_H0_calibration_gate",
            "why": "factorization still contains H_star/H0 and this is independent of dim/rank",
            "first_output": "Hstar closure/theorem target audit",
            "claim_ceiling": "calibration_gate_no_parent_promotion",
            "priority": 2,
        },
        {
            "candidate_next_gate": "local_GR_PPN_independent_gate",
            "why": "a unified field theory must reduce to GR locally, closure amplitude does not solve this",
            "first_output": "local GR/PPN claim ledger refresh",
            "claim_ceiling": "local_reduction_gate_only",
            "priority": 3,
        },
        {
            "candidate_next_gate": "CMB_growth_bridge_gate",
            "why": "late-time closure branch cannot claim perturbation or early-universe safety",
            "first_output": "post-closure CMB/growth bridge kill-screen",
            "claim_ceiling": "bridge_diagnostic_only",
            "priority": 4,
        },
    ]


def gate_rows(sources: list[dict[str, Any]], claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(bool(row["exists"]) for row in sources)
    by_claim = {row["claim_id"]: row for row in claims}
    return [
        {"gate": "source_paths_exist", "status": "pass" if sources_ok else "fail", "evidence": sources_ok},
        {
            "gate": "Bmem_marked_explicit_closure",
            "status": "pass" if by_claim["A1_Bmem_2over27"]["current_status"] == "explicit_closure_value" else "fail",
            "evidence": by_claim["A1_Bmem_2over27"]["allowed_claim"],
        },
        {
            "gate": "Bmem_parent_derivation_forbidden",
            "status": "pass" if "parent-derived" in by_claim["A1_Bmem_2over27"]["forbidden_claim"] else "fail",
            "evidence": by_claim["A1_Bmem_2over27"]["forbidden_claim"],
        },
        {
            "gate": "epsilonH_not_unconditionally_derived",
            "status": "pass" if "closure" in by_claim["A2_epsilonH_unit"]["current_status"] else "fail",
            "evidence": by_claim["A2_epsilonH_unit"]["current_status"],
        },
        {
            "gate": "qtrace_marked_conditional",
            "status": "pass" if "conditional" in by_claim["A3_qtrace_2over27"]["current_status"] else "fail",
            "evidence": by_claim["A3_qtrace_2over27"]["current_status"],
        },
        {
            "gate": "empirical_branch_retained",
            "status": "pass" if by_claim["E1_locked_late_time_branch"]["current_status"] == "empirical closure branch retained" else "fail",
            "evidence": by_claim["E1_locked_late_time_branch"]["allowed_claim"],
        },
        {
            "gate": "local_GR_not_solved_by_amplitude",
            "status": "pass" if "independent" in by_claim["L1_local_GR_PPN"]["current_status"] else "fail",
            "evidence": by_claim["L1_local_GR_PPN"]["forbidden_claim"],
        },
        {
            "gate": "CMB_growth_not_solved_by_late_time_closure",
            "status": "pass" if "independent" in by_claim["C1_CMB_growth_bridge"]["current_status"] else "fail",
            "evidence": by_claim["C1_CMB_growth_bridge"]["forbidden_claim"],
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The local claim ledger now reflects checkpoint 343: B_mem=2/27 is an explicit locked closure value and "
                "empirical theorem target, not a parent-derived amplitude. Conditional finite-fibre/readout routes are "
                "archived as theorem targets. Next productive work should be empirical robustness or independent theory gates."
            ),
            "next_target": "post_343_empirical_locked_branch_or_independent_theory_gate",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    claims = claim_ledger_rows()
    transitions = transition_rows()
    next_gates = next_gate_rows()
    gates = gate_rows(sources, claims)
    decisions = decision_rows()

    outputs = {
        "source_register.csv": (sources, ["source", "role", "exists", "issue"]),
        "claim_ledger.csv": (
            claims,
            ["claim_id", "object", "current_status", "evidence_basis", "allowed_claim", "forbidden_claim", "next_action"],
        ),
        "transition_ledger.csv": (
            transitions,
            ["transition", "before_343", "after_343", "reason"],
        ),
        "next_gate_options.csv": (
            next_gates,
            ["candidate_next_gate", "why", "first_output", "claim_ceiling", "priority"],
        ),
        "gate_results.csv": (gates, ["gate", "status", "evidence"]),
        "decision.csv": (decisions, ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(result_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(result_dir),
        "generated": list(outputs),
        "Bmem_2over27_status": "explicit_closure_not_parent_derived",
        "epsilonH_status": "closure_or_conditional_theorem_target",
        "qtrace_status": "conditional_algebraic_identity",
        "empirical_branch_retained": True,
        "next_target": "post_343_empirical_locked_branch_or_independent_theory_gate",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update the post-343 amplitude closure claim ledger.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-phiC-zero-theorem-or-gradient-bound"
STATUS = "local_phiC_zero_conditional_on_boundary_state_and_trivial_class_gradient_bounds_remain_if_not_parent_derived"
CLAIM_CEILING = "conditional_zero_theorem_and_gradient_budget_only_no_clock_gamma_fifth_force_WEP_EH_or_local_GR_pass"
NEXT_TARGET = "373-one-observed-coframe-parent-selector-or-WEP-closure.md"


SOURCE_DOCS = [
    {
        "path": "300-boundary-state-local-silence-theorem-attempt.md",
        "role": "boundary-state local silence contract: local closed/gapped or trivial class implies effective silence",
    },
    {
        "path": "367-topological-class-selection-or-local-GR-closure-ledger.md",
        "role": "class selection not parent-derived; local route demoted to labelled closure and testing",
    },
    {
        "path": "370-common-mode-phiC-coefficient-map.md",
        "role": "weak-field phi_C budgets for clock, gamma, beta, and fifth-force pressure",
    },
    {
        "path": "371-WEP-species-universality-or-active-eta-runner.md",
        "role": "WEP remains active even if common-mode phi_C is silent",
    },
    {
        "path": "369-source-locked-closure-branch-local-bound-runner.md",
        "role": "source-locked closure branch runner and budget-only local rows",
    },
    {
        "path": "261-Hstar-H0-scale-lock-and-local-silence-attempt.md",
        "role": "earlier Hstar/local silence attempt and scale-lock context",
    },
    {
        "path": "195-late-CMB-domain-rule-and-local-silence-gate.md",
        "role": "late CMB domain rule and local silence gate context",
    },
]


ZERO_THEOREM_ASSUMPTIONS = [
    {
        "assumption": "class_metric_branch",
        "statement": "phi_C = lambda C_D or lambda P_D C in the labelled class-metric closure branch",
        "status": "branch_definition",
    },
    {
        "assumption": "local_trivial_class",
        "statement": "stationary local domains carry Q_rel=0 or exact lifted-C class",
        "status": "closure_branch_assignment_not_parent_derived",
    },
    {
        "assumption": "boundary_state_silence",
        "statement": "local bound domains are closed/gapped in the MTS boundary bath or have c_D=||[J_B]||=0",
        "status": "conditional_from_checkpoint_300",
    },
    {
        "assumption": "no_class_changing_event",
        "statement": "no horizon, merger, radiation, ordinary bath confusion, or local source changes the class",
        "status": "edge_case_open",
    },
    {
        "assumption": "normalization",
        "statement": "zero local class is normalized to phi_C=0 or a physically unobservable constant",
        "status": "allowed_branch_normalization",
    },
]


ZERO_THEOREM_DERIVATION = [
    {
        "step": 1,
        "statement": "Use the class metric branch.",
        "equation": "ghat_mn = exp(phi_C) g_mn, phi_C=lambda C_D",
        "status": "definition",
    },
    {
        "step": 2,
        "statement": "Define the local silence selector through boundary state and relative class.",
        "equation": "sigma_D = Theta(b_D)Theta(c_D), with c_D=||[J_B]_D||",
        "status": "conditional_contract",
    },
    {
        "step": 3,
        "statement": "For stationary local bound domains, impose the closure branch assignment.",
        "equation": "b_D=0 and/or c_D=0, Q_rel=0",
        "status": "not_parent_derived",
    },
    {
        "step": 4,
        "statement": "Then the local class observable is constant/trivial.",
        "equation": "C_D|local = 0 or constant",
        "status": "conditional_derivation_inside_branch",
    },
    {
        "step": 5,
        "statement": "Therefore the class metric has no local common-mode gradient.",
        "equation": "grad phi_C = 0, Delta phi_C = 0",
        "status": "conditional_zero_theorem",
    },
    {
        "step": 6,
        "statement": "If the parent theory does not derive the local trivial class/boundary-state split, use gradient budgets instead.",
        "equation": "r_grad <= 2.3e-5 and |Delta phi_C/Delta U| <= 6.2e-5",
        "status": "fallback_bound",
    },
]


GRADIENT_BOUND_MATRIX = [
    {
        "residual": "gamma_minus_1",
        "proxy": "gamma-1 ~ r_grad",
        "source_locked_target": 2.3e-5,
        "required_bound": "r_grad <= 2.3e-5",
        "zero_theorem_effect": "killed if grad phi_C=0",
        "status": "conditional_or_budget_only",
    },
    {
        "residual": "alpha_clock_redshift",
        "proxy": "alpha_clock ~ 0.5 |Delta phi_C/Delta U|",
        "source_locked_target": 3.1e-5,
        "required_bound": "|Delta phi_C/Delta U| <= 6.2e-5",
        "zero_theorem_effect": "killed if Delta phi_C=0",
        "status": "conditional_or_budget_only",
    },
    {
        "residual": "delta_G_or_fifth_force",
        "proxy": "a_extra/a_GR ~ 0.5 r_grad",
        "source_locked_target": "",
        "required_bound": "unscored until source-locked",
        "zero_theorem_effect": "class-metric gradient force killed if grad phi_C=0",
        "status": "quarantined",
    },
    {
        "residual": "beta_minus_1",
        "proxy": "depends on second-order phi_C expansion and residual EH operator",
        "source_locked_target": 7.8e-5,
        "required_bound": "no reliable bound until s1,s2/EH operator map exists",
        "zero_theorem_effect": "first-order phi_C pressure killed; beta still needs EH/second-order proof",
        "status": "blocked",
    },
    {
        "residual": "eta_WEP",
        "proxy": "species-specific F_A(C_D), not common-mode gradient",
        "source_locked_target": 2.8e-15,
        "required_bound": "universal F(C_D) theorem required",
        "zero_theorem_effect": "not killed by local phi_C silence alone",
        "status": "active_hardest_gate",
    },
]


EDGE_CASE_AUDIT = [
    {
        "edge_case": "ordinary_environmental_bath",
        "risk": "ordinary dissipation mimics MTS boundary bath b_D",
        "policy": "must isolate MTS-specific boundary-bath channel before claiming sigma_D=0",
    },
    {
        "edge_case": "black_hole_or_horizon",
        "risk": "local horizon can be gapless/nontrivial even in a bound system",
        "policy": "separate branch; do not fold into ordinary lab-local silence",
    },
    {
        "edge_case": "galaxy_or_cluster",
        "risk": "bound but not laboratory-local; silence theorem could erase empirical galaxy pillar",
        "policy": "keep galaxy pillar separate until class split is derived",
    },
    {
        "edge_case": "time_dependent_local_system",
        "risk": "radiation/low-frequency boundary activity makes b_D nonzero",
        "policy": "use runner/bounds; do not assume strict zero",
    },
    {
        "edge_case": "class_changing_event",
        "risk": "collapse/merger/domain transition changes Q_rel and produces phi_C gradient",
        "policy": "requires event source law and conservation bookkeeping",
    },
]


RUNNER_UPDATE = [
    {
        "runner_row": "gamma_minus_1",
        "if_zero_theorem": "class-metric gamma proxy killed",
        "if_not_zero": "require r_grad <= 2.3e-5",
        "claim_status": "conditional_or_budget_only",
    },
    {
        "runner_row": "alpha_clock_redshift",
        "if_zero_theorem": "class-metric clock drift killed",
        "if_not_zero": "require |Delta phi_C/Delta U| <= 6.2e-5",
        "claim_status": "conditional_or_budget_only",
    },
    {
        "runner_row": "delta_G_or_fifth_force",
        "if_zero_theorem": "class-metric gradient force killed",
        "if_not_zero": "source-lock before scoring",
        "claim_status": "quarantined",
    },
    {
        "runner_row": "beta_minus_1",
        "if_zero_theorem": "first-order phi_C pressure removed",
        "if_not_zero": "second-order map still missing",
        "claim_status": "blocked",
    },
    {
        "runner_row": "eta_WEP",
        "if_zero_theorem": "unchanged; species universality still missing",
        "if_not_zero": "unchanged plus possible species response",
        "claim_status": "active_hardest_gate",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Strict local phi_C silence follows conditionally inside the labelled local-trivial-class/boundary-state branch, but that branch is not parent-derived; otherwise clock/gamma require small gradients and no local pass follows.",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "attempt a parent selector for one observed coframe/common F(C_D), separate from representative invariance",
        "pass_condition": "species universality is derived or permanently labelled as closure axiom",
    },
    {
        "priority": 2,
        "target": "374-fifth-force-preferred-frame-source-lock-manifest.md",
        "task": "source-lock quarantined fifth-force/preferred-frame/xi sectors before scoring them",
        "pass_condition": "quarantined rows become ready targets or remain explicitly unscored",
    },
    {
        "priority": 3,
        "target": "375-EH-exterior-operator-or-residual-modified-gravity-ledger.md",
        "task": "separate EH derivation from residual modified-gravity operator testing",
        "pass_condition": "no local-GR promotion without EH operator or bounded residual operator",
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
            "gate": "conditional_zero_theorem_written",
            "status": "conditional_pass",
            "evidence": "local trivial class plus boundary-state silence gives grad phi_C=0 inside branch",
        },
        {
            "gate": "parent_boundary_state_split_derived",
            "status": "fail",
            "evidence": "local/FLRW boundary-state split remains a contract from checkpoint 300",
        },
        {
            "gate": "gradient_fallback_bounds_written",
            "status": "pass",
            "evidence": "gamma and clock gradient budgets imported from checkpoint 370",
        },
        {
            "gate": "edge_cases_closed",
            "status": "fail",
            "evidence": "ordinary baths, horizons, galaxies, time-dependent systems, and class-changing events remain open",
        },
        {
            "gate": "WEP_species_gate_solved",
            "status": "fail",
            "evidence": "local phi_C silence does not derive species universality",
        },
        {
            "gate": "local_bound_or_local_GR_pass_claim",
            "status": "fail",
            "evidence": "zero theorem is conditional and branch is not parent-derived",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "zero_theorem_assumptions.csv", ZERO_THEOREM_ASSUMPTIONS)
    write_csv(results_dir / "zero_theorem_derivation.csv", ZERO_THEOREM_DERIVATION)
    write_csv(results_dir / "gradient_bound_matrix.csv", GRADIENT_BOUND_MATRIX)
    write_csv(results_dir / "edge_case_audit.csv", EDGE_CASE_AUDIT)
    write_csv(results_dir / "runner_update.csv", RUNNER_UPDATE)
    write_csv(results_dir / "gate_results.csv", gate_rows(source_rows))
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
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 372 local phi_C zero theorem or gradient-bound artifacts."
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

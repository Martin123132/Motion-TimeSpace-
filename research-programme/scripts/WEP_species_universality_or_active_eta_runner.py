from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "WEP-species-universality-or-active-eta-runner"
STATUS = "species_universality_not_parent_derived_eta_WEP_remains_active_hardest_ready_gate"
CLAIM_CEILING = "WEP_species_gate_only_no_WEP_clock_PPN_EH_or_local_GR_pass"
NEXT_TARGET = "372-local-phiC-zero-theorem-or-gradient-bound.md"


SOURCE_DOCS = [
    {
        "path": "360-universal-matter-coupling-theorem-attempt.md",
        "role": "single observed coframe contract and forbidden direct species vertices",
    },
    {
        "path": "366-representative-invariant-matter-action-for-lifted-C.md",
        "role": "representative invariance descends matter to class observables but species universality remains open",
    },
    {
        "path": "369-source-locked-closure-branch-local-bound-runner.md",
        "role": "source-locked closure branch local-bound runner and eta_WEP budget row",
    },
    {
        "path": "370-common-mode-phiC-coefficient-map.md",
        "role": "common-mode phi_C does not solve species universality",
    },
    {
        "path": "354-official-local-bound-source-lock-or-nohair-proof-deepening.md",
        "role": "source-locked eta_WEP target scale from MICROSCOPE context",
    },
    {
        "path": "runs/20260601-221000-source-locked-closure-branch-local-bound-runner/results/ready_budget_rows.csv",
        "role": "machine-readable ready budget row including eta_WEP",
    },
    {
        "path": "runs/20260601-223000-common-mode-phiC-coefficient-map/results/coefficient_budgets.csv",
        "role": "machine-readable coefficient budget showing eta_WEP species-universality dependence",
    },
]


UNIVERSALITY_ROUTES = [
    {
        "route": "representative_invariance",
        "candidate_statement": "matter cannot depend on B_perp, b2, Cperp, or local representative data",
        "result": "conditional_pass_but_insufficient",
        "why": "it permits any species function F_A(C_D) because C_D is class-invariant",
    },
    {
        "route": "single_observed_coframe",
        "candidate_statement": "all sectors couple to one ehat(C_D,g) and the same F(C_D)",
        "result": "conditional_pass_if_postulated_or_parent_selected",
        "why": "one coframe kills direct composition dependence, but the parent selector is not derived",
    },
    {
        "route": "minimal_metric_coupling",
        "candidate_statement": "all matter uses the same metric connection and constants independent of C_D",
        "result": "closure_or_external_principle",
        "why": "standard local metric coupling is a powerful assumption, not yet an MTS derivation",
    },
    {
        "route": "species_charge_forbidden",
        "candidate_statement": "no q_A, m_A(C_D), alpha_A(C_D), or F_A(C_D) species labels exist",
        "result": "required_selection_rule",
        "why": "forbidden-vertex list is known, but no parent symmetry forbids all species labels yet",
    },
    {
        "route": "common_mode_phiC_silence",
        "candidate_statement": "grad phi_C=0 locally",
        "result": "irrelevant_to_species_split",
        "why": "it helps clock/gamma/fifth-force pressure, but cannot by itself enforce F_A=F_B",
    },
]


WEP_VERTEX_AUDIT = [
    {
        "vertex": "species_specific_metric",
        "form": "ghat_A = exp(F_A(C_D)) g",
        "representative_invariant": "yes",
        "WEP_status": "fail_unless_F_A_universal",
        "required_action": "derive F_A=F for all A or keep eta_WEP active",
    },
    {
        "vertex": "species_mass_response",
        "form": "m_A(C_D) psi_A psi_A",
        "representative_invariant": "yes",
        "WEP_status": "fail_unless_no_C_D_dependence_or_universal_metric_absorption",
        "required_action": "forbid species-dependent mass functions",
    },
    {
        "vertex": "electromagnetic_clock_response",
        "form": "alpha_EM,A(C_D) F^2 or clock-sector F_A(C_D)",
        "representative_invariant": "yes",
        "WEP_status": "clock_and_composition_risk",
        "required_action": "forbid direct class dependence of constants beyond universal geometry",
    },
    {
        "vertex": "representative_direct_coupling",
        "form": "B_perp O_A, b2 O_A, Cperp O_A",
        "representative_invariant": "no",
        "WEP_status": "conditionally_forbidden_by_lifted_C_symmetry",
        "required_action": "keep forbidden in branch; failure returns fifth-force/WEP risk",
    },
    {
        "vertex": "universal_class_metric",
        "form": "sum_A S_A[psi_A, exp(F(C_D))g, constants_A]",
        "representative_invariant": "yes",
        "WEP_status": "conditional_safe_for_direct_WEP",
        "required_action": "derive one observed coframe and common F from parent action",
    },
]


ETA_RUNNER_UPDATE = [
    {
        "residual": "eta_WEP",
        "source_locked_scale": 2.8e-15,
        "active_terms": "species_specific_F_A;species_mass_or_constant_response;representative_vertex_leakage",
        "equal_share_ceiling_if_three_unit_terms": 9.333333333333333e-16,
        "derived_zero_terms": "none_parent_derived",
        "conditionally_forbidden_terms": "representative_vertex_leakage_if_lifted_C_symmetry_holds",
        "runner_status": "active_hardest_ready_gate_no_pass",
    },
    {
        "residual": "alpha_clock_redshift",
        "source_locked_scale": 3.1e-5,
        "active_terms": "clock_sector_F_A(C_D);common_mode_phiC_drift",
        "equal_share_ceiling_if_two_unit_terms": 1.55e-5,
        "derived_zero_terms": "none_parent_derived",
        "conditionally_forbidden_terms": "direct_representative_clock_vertex_if_lifted_C_symmetry_holds",
        "runner_status": "active_budget_only",
    },
]


ACTIVE_ETA_FORMULAS = [
    {
        "formula": "Delta F_AB = F_A(C_D) - F_B(C_D)",
        "meaning": "species metric/class response split",
        "budget_pressure": "|Delta F_AB| less than about 2.8e-15 for unit WEP coefficient",
        "status": "not_derived_zero",
    },
    {
        "formula": "eta_WEP ~ c_AB Delta F_AB + c_rep eps_rep + c_m Delta m_A(C_D)",
        "meaning": "symbolic active eta row",
        "budget_pressure": "all terms must be zero by theorem or fit under MICROSCOPE-scale target",
        "status": "runner_formula",
    },
    {
        "formula": "S_matter = sum_A S_A[psi_A, ehat, omega[ehat], constants_A]",
        "meaning": "safe conditional universal action",
        "budget_pressure": "requires one parent-selected ehat and C_D-independent constants",
        "status": "conditional_contract",
    },
]


FAILURE_MODES = [
    {
        "failure": "representative_invariance_mistaken_for_WEP",
        "meaning": "forgetting that F_A(C_D) is representative-invariant but still species-dependent",
        "consequence": "false WEP pass",
    },
    {
        "failure": "single_metric_assumed_not_derived",
        "meaning": "using one observed coframe as a postulate while claiming parent derivation",
        "consequence": "closure hidden as theorem",
    },
    {
        "failure": "clock_constants_depend_on_class",
        "meaning": "spectroscopy or EM constants see C_D outside geometry",
        "consequence": "clock/redshift and composition residuals return",
    },
    {
        "failure": "local_phiC_zero_overclaimed",
        "meaning": "treating common-mode silence as species universality",
        "consequence": "eta_WEP remains unsolved even if clock/gamma improve",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Representative invariance forbids direct representative vertices but does not derive species universality; eta_WEP remains the active hardest ready gate unless one observed coframe and common F(C_D) are parent-derived.",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "derive strict local class silence grad(phi_C)=0 or bound r_grad against clock/gamma budgets",
        "pass_condition": "r_grad is theorem-zero, source-bounded, or marked failed",
    },
    {
        "priority": 2,
        "target": "373-one-observed-coframe-parent-selector-or-WEP-closure.md",
        "task": "attempt a parent selector for one observed coframe/common F(C_D), separate from representative invariance",
        "pass_condition": "species universality is derived or permanently labelled as closure axiom",
    },
    {
        "priority": 3,
        "target": "374-fifth-force-preferred-frame-source-lock-manifest.md",
        "task": "source-lock quarantined fifth-force/preferred-frame/xi sectors before scoring them",
        "pass_condition": "quarantined rows become ready targets or remain explicitly unscored",
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
            "gate": "representative_vertices_forbidden",
            "status": "conditional_pass",
            "evidence": "lifted-C representative symmetry forbids B_perp/b2/Cperp local matter vertices if parent-owned",
        },
        {
            "gate": "species_universality_derived",
            "status": "fail",
            "evidence": "representative invariance allows species-specific F_A(C_D)",
        },
        {
            "gate": "active_eta_runner_written",
            "status": "pass",
            "evidence": "eta_WEP row retains species, mass/constant, and representative-leakage terms",
        },
        {
            "gate": "WEP_pass_claim",
            "status": "fail",
            "evidence": "eta_WEP remains active at source-locked 2.8e-15 scale",
        },
        {
            "gate": "clock_species_constant_risk_retained",
            "status": "pass",
            "evidence": "clock/EM constants depending on C_D remain active failure mode",
        },
        {
            "gate": "local_GR_promotion",
            "status": "fail",
            "evidence": "WEP universality, local phi_C silence, EH operator, and class selection remain open",
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
    write_csv(results_dir / "universality_routes.csv", UNIVERSALITY_ROUTES)
    write_csv(results_dir / "WEP_vertex_audit.csv", WEP_VERTEX_AUDIT)
    write_csv(results_dir / "eta_runner_update.csv", ETA_RUNNER_UPDATE)
    write_csv(results_dir / "active_eta_formulas.csv", ACTIVE_ETA_FORMULAS)
    write_csv(results_dir / "failure_modes.csv", FAILURE_MODES)
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
        description="Write checkpoint 371 WEP species universality or active eta runner artifacts."
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

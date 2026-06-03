from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "common-mode-class-metric-clock-PPN-residual-gate"
STATUS = "class_metric_residual_gate_written_no_local_bound_pass_coefficients_and_source_locks_still_open"
CLAIM_CEILING = "residual_gate_only_no_WEP_clock_PPN_EH_or_local_GR_promotion"
NEXT_TARGET = "369-source-locked-closure-branch-local-bound-runner.md"


SOURCE_DOCS = [
    {
        "path": "354-official-local-bound-source-lock-or-nohair-proof-deepening.md",
        "role": "source-locked gamma, beta, WEP, and redshift internal target scales",
    },
    {
        "path": "359-source-locked-PPN-residual-runner-from-derived-force-ledger.md",
        "role": "source-locked residual runner policy and pressure ranking",
    },
    {
        "path": "360-universal-matter-coupling-theorem-attempt.md",
        "role": "universal matter coupling contract and forbidden direct vertices",
    },
    {
        "path": "366-representative-invariant-matter-action-for-lifted-C.md",
        "role": "representative-invariant lifted-C matter selector theorem shape",
    },
    {
        "path": "367-topological-class-selection-or-local-GR-closure-ledger.md",
        "role": "labelled closure pivot and residual-test queue",
    },
    {
        "path": "358-local-EH-exterior-operator-from-Ward-closed-action.md",
        "role": "Einstein-Hilbert exterior operator gate remains open",
    },
]


CLASS_METRIC_MODEL = [
    {
        "object": "class_metric_closure",
        "definition": "ghat_mn = exp(phi_C) g_mn",
        "phi_C": "phi_C = lambda C_D or lambda P_D C",
        "status": "labelled_closure_and_theorem_target",
        "allowed_use": "local residual gate and empirical branch testing",
    },
    {
        "object": "local_common_mode_ratio",
        "definition": "r_grad = |grad phi_C| / |grad U_GR|",
        "phi_C": "dimensionless local gradient pressure",
        "status": "coefficient_not_derived",
        "allowed_use": "clock/PPN/fifth-force budget estimate",
    },
    {
        "object": "species_nonuniversality_ratio",
        "definition": "Delta_lambda_AB or Delta F_AB(C_D)",
        "phi_C": "difference between matter-sector class responses",
        "status": "must_be_zero_by_theorem_or_WEP_bound",
        "allowed_use": "WEP residual guard",
    },
    {
        "object": "representative_vertex",
        "definition": "direct coupling to B_perp, b2, Cperp, or j3 representative data",
        "phi_C": "not allowed in representative-invariant branch",
        "status": "forbidden_conditionally",
        "allowed_use": "failure detector only",
    },
]


SOURCE_LOCKED_TARGETS = [
    {
        "residual": "gamma_minus_1",
        "source_locked_scale": 2.3e-5,
        "status": "ready_internal_target",
        "source_context": "Cassini/review lock in checkpoint 354",
    },
    {
        "residual": "beta_minus_1",
        "source_locked_scale": 7.8e-5,
        "status": "ready_internal_target",
        "source_context": "Mercury/Messenger/review lock in checkpoint 354",
    },
    {
        "residual": "eta_WEP",
        "source_locked_scale": 2.8e-15,
        "status": "ready_internal_target",
        "source_context": "MICROSCOPE lock in checkpoint 354",
    },
    {
        "residual": "alpha_clock_redshift",
        "source_locked_scale": 3.1e-5,
        "status": "ready_internal_target",
        "source_context": "Galileo redshift lock in checkpoint 354",
    },
    {
        "residual": "preferred_frame_alpha1_alpha2",
        "source_locked_scale": "",
        "status": "quarantined",
        "source_context": "sector identified but not numeric locked here",
    },
    {
        "residual": "xi_preferred_location_anisotropy",
        "source_locked_scale": "",
        "status": "quarantined",
        "source_context": "sector identified but not numeric locked here",
    },
    {
        "residual": "delta_G_or_fifth_force",
        "source_locked_scale": "",
        "status": "quarantined",
        "source_context": "needs dedicated source lock and coefficient map",
    },
]


RESIDUAL_GATE_MATRIX = [
    {
        "gate": "common_mode_clock_redshift",
        "branch_source": "phi_C local drift/gradient",
        "estimated_residual": "alpha_clock ~ coeff_clock * Delta phi_C / Delta U",
        "source_locked_target": "3.1e-5",
        "pass_condition": "derive coeff_clock=0 or bound |Delta phi_C/Delta U| below target with coefficient",
        "current_status": "open_no_pass",
    },
    {
        "gate": "PPN_gamma",
        "branch_source": "spatial/time conformal response of class metric relative to GR potential",
        "estimated_residual": "gamma-1 ~ coeff_gamma * r_grad",
        "source_locked_target": "2.3e-5",
        "pass_condition": "derive coeff_gamma=0/absorbed or bound r_grad below target",
        "current_status": "open_no_pass",
    },
    {
        "gate": "PPN_beta",
        "branch_source": "second-order/nonlinear response of phi_C and exterior operator",
        "estimated_residual": "beta-1 ~ coeff_beta1*r_grad + coeff_beta2*r_grad^2 + residual_EH_operator",
        "source_locked_target": "7.8e-5",
        "pass_condition": "derive second-order coefficients or bound all terms",
        "current_status": "open_no_pass",
    },
    {
        "gate": "WEP_species_universality",
        "branch_source": "hidden species-specific F_A(C_D) or representative vertices",
        "estimated_residual": "eta_WEP ~ coeff_WEP * |Delta F_AB|",
        "source_locked_target": "2.8e-15",
        "pass_condition": "prove universal F for all matter sectors or keep WEP residual active",
        "current_status": "open_no_pass_hardest_ready_gate",
    },
    {
        "gate": "fifth_force_delta_G",
        "branch_source": "grad phi_C, class-changing boundary events, bulk/domain fields",
        "estimated_residual": "a_extra/a_GR ~ coeff_5 * r_grad plus source terms",
        "source_locked_target": "quarantined",
        "pass_condition": "source-lock fifth-force bounds and derive/fit coefficients before scoring",
        "current_status": "quarantined_no_numeric_pass",
    },
    {
        "gate": "preferred_frame_anisotropy",
        "branch_source": "domain marker, boundary normal, noncovariant P_D/P_coh selection",
        "estimated_residual": "alpha1/alpha2/xi terms",
        "source_locked_target": "quarantined",
        "pass_condition": "prove no marker fields or source-lock preferred-frame/xi bounds",
        "current_status": "quarantined_no_numeric_pass",
    },
    {
        "gate": "EH_exterior_operator",
        "branch_source": "retained non-EH operator terms after Ward closure",
        "estimated_residual": "gamma/beta/slip/fifth-force operator vector",
        "source_locked_target": "indirect via gamma/beta/fifth-force",
        "pass_condition": "derive metric-only second-order EH exterior or retain residual operator in runner",
        "current_status": "open_no_local_GR_promotion",
    },
]


BASELINE_RULES = [
    {
        "comparison": "GR_local_baseline",
        "rule": "use GR values gamma=beta=1 and zero WEP/clock violation only as baseline, not as proof MTS reaches them",
        "failure_flag": "MTS residual coefficients missing or nonzero beyond source-locked budgets",
    },
    {
        "comparison": "closure_branch_vs_GR",
        "rule": "score the class-metric closure by residual vector size relative to GR, with all closure labels visible",
        "failure_flag": "closure branch needs tuned zeroes or hidden species universality",
    },
    {
        "comparison": "stress_test_symmetry",
        "rule": "if a stress test also applies to GR or LCDM, run/define the corresponding baseline check",
        "failure_flag": "pipeline failure or baseline failure must not be misread as MTS-only failure",
    },
    {
        "comparison": "empirical_closure_vs_theory_claim",
        "rule": "empirical survival of closure branch does not upgrade it to parent-derived local GR",
        "failure_flag": "fit success used as substitute for class-selection/EH derivation",
    },
]


DERIVATION_DEBTS = [
    {
        "debt": "derive_or_bound_phi_C_local_gradient",
        "why": "common-mode class metric can affect clocks, gamma, fifth force, and local acceleration",
        "next_action": "write coefficient map for r_grad and Delta phi_C / Delta U",
    },
    {
        "debt": "prove_species_universality",
        "why": "WEP target is 2.8e-15 and representative invariance alone permits species-specific F_A",
        "next_action": "derive universal F(C_D) from one observed coframe or keep eta_WEP active",
    },
    {
        "debt": "source_lock_quarantined_sectors",
        "why": "preferred-frame, xi, and fifth-force cannot be scored numerically yet",
        "next_action": "build dedicated source manifest before numeric claims",
    },
    {
        "debt": "separate_EH_operator_residual",
        "why": "class metric selector does not derive Einstein-Hilbert exterior dynamics",
        "next_action": "retain residual operator terms or prove EH uniqueness",
    },
    {
        "debt": "class_split_edge_cases",
        "why": "local Q_rel=0 and FLRW nonzero remain branch assignments",
        "next_action": "stress edge cases: horizons, galaxies, time-dependent local systems, ordinary baths",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The labelled class-metric branch has a concrete local residual gate, but all pass claims are blocked by missing coefficients, common-mode bounds, species universality, quarantined sectors, and EH operator debt.",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "prepare a source-locked local-bound runner for the class-metric closure branch",
        "pass_condition": "ready and quarantined rows are separated; every scored residual has coefficient assumptions visible",
    },
    {
        "priority": 2,
        "target": "370-common-mode-phiC-coefficient-map.md",
        "task": "derive or parameterize phi_C local gradients against Newtonian potential and clock/redshift observables",
        "pass_condition": "clock/gamma/beta/fifth-force coefficients are explicit or marked missing",
    },
    {
        "priority": 3,
        "target": "371-EH-exterior-operator-or-residual-modified-gravity-ledger.md",
        "task": "separate EH derivation from residual modified-gravity operator testing",
        "pass_condition": "no local-GR promotion without EH operator or bounded residual operator",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
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
            "gate": "class_metric_residual_model_written",
            "status": "pass",
            "evidence": "phi_C, r_grad, species nonuniversality, and representative vertices defined",
        },
        {
            "gate": "source_locked_ready_targets_loaded",
            "status": "pass",
            "evidence": "gamma, beta, WEP, and clock target scales imported from checkpoints 354/359",
        },
        {
            "gate": "quarantined_sectors_retained",
            "status": "pass",
            "evidence": "preferred-frame, xi, and fifth-force remain unscored until source-locked",
        },
        {
            "gate": "residual_gate_matrix_written",
            "status": "pass",
            "evidence": "clock, gamma, beta, WEP, fifth-force, preferred-frame, EH rows recorded",
        },
        {
            "gate": "residual_coefficients_derived",
            "status": "fail",
            "evidence": "coeff_clock, coeff_gamma, coeff_beta, coeff_WEP, coeff_5 not derived",
        },
        {
            "gate": "common_mode_phiC_bound_derived",
            "status": "fail",
            "evidence": "local phi_C gradient/drift is not zero-derived or source-bounded",
        },
        {
            "gate": "WEP_clock_PPN_or_local_GR_pass_claim",
            "status": "fail",
            "evidence": "gate is a residual test plan only",
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
    write_csv(results_dir / "class_metric_model.csv", CLASS_METRIC_MODEL)
    write_csv(results_dir / "source_locked_targets.csv", SOURCE_LOCKED_TARGETS)
    write_csv(results_dir / "residual_gate_matrix.csv", RESIDUAL_GATE_MATRIX)
    write_csv(results_dir / "baseline_rules.csv", BASELINE_RULES)
    write_csv(results_dir / "derivation_debts.csv", DERIVATION_DEBTS)
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
        description="Write checkpoint 368 common-mode class metric clock/PPN residual gate artifacts."
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

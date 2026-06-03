from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-bound-runner-v2-from-retained-residuals"
STATUS = "local_bound_runner_v2_matrix_written_retained_residuals_classified_budget_only_no_PPN_or_local_GR_pass"
CLAIM_CEILING = "local_bound_runner_v2_only_no_WEP_PPN_EH_fifth_force_boundary_bulk_source_or_local_GR_pass"
NEXT_TARGET = "384-parent-action-first-variation-obstruction-map.md"


SOURCE_DOCS = [
    {
        "path": "359-source-locked-PPN-residual-runner-from-derived-force-ledger.md",
        "role": "first source-locked local guardrail runner and pressure ranking",
    },
    {
        "path": "369-source-locked-closure-branch-local-bound-runner.md",
        "role": "closure-branch runner policy: budgets not passes",
    },
    {
        "path": "374-fifth-force-preferred-frame-source-lock-manifest.md",
        "role": "preferred-frame, xi, alpha3, Gdot, and fifth-force source-lock policy",
    },
    {
        "path": "375-EH-exterior-operator-or-residual-modified-gravity-ledger.md",
        "role": "operator residual coefficients and local observable joins",
    },
    {
        "path": "377-fifth-force-range-coupling-map.md",
        "role": "alpha_Y(lambda_Y) force-law contract and unscored fifth-force policy",
    },
    {
        "path": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "delta_G/Gdot/source-normalization fallback policy",
    },
    {
        "path": "379-class-only-boundary-action-noangular-theorem.md",
        "role": "boundary residual coefficients and observable map",
    },
    {
        "path": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "role": "bulk-X alpha_X(lambda_X) fallback and no-hair contract",
    },
    {
        "path": "381-local-GR-debt-ledger-rollup-after-360-380.md",
        "role": "local-GR debt ledger and observable row summary",
    },
    {
        "path": "382-parent-local-action-minimal-contract.md",
        "role": "residual fallback rows and parent-action contract",
    },
]


STATE_DEFINITIONS = [
    {
        "state": "derived_zero",
        "meaning": "parent variation/theorem derives the residual coefficient is zero",
        "score_policy": "may be treated as zero if source path is recorded",
        "claim_policy": "local pass still needs all coupled rows closed",
    },
    {
        "state": "conditional_zero",
        "meaning": "zero only if a named theorem premise is assumed but not parent-derived",
        "score_policy": "may be shown as conditional branch, not a pass",
        "claim_policy": "no public pass; premise must stay visible",
    },
    {
        "state": "closure_zero",
        "meaning": "zero by explicit closure axiom rather than parent derivation",
        "score_policy": "score only as labelled closure branch",
        "claim_policy": "no derivation or GR-reduction claim",
    },
    {
        "state": "budget_only",
        "meaning": "numeric source lock exists but MTS coefficient is missing",
        "score_policy": "emit suppression budget/equal-share ceiling",
        "claim_policy": "no observational pass",
    },
    {
        "state": "contingent_budget",
        "meaning": "numeric guardrail applies only if the channel exists",
        "score_policy": "keep row but do not count unless branch predicts the channel",
        "claim_policy": "no pass and no failure without channel derivation",
    },
    {
        "state": "unscored_parameterized",
        "meaning": "needs range/coupling/profile before a numeric local comparison is meaningful",
        "score_policy": "retain alpha(lambda) or profile contract; no scalar score",
        "claim_policy": "no fifth-force/delta_G pass",
    },
    {
        "state": "failed_open",
        "meaning": "required parent theorem is absent and no numeric coefficient or closure is supplied",
        "score_policy": "route to residual fallback before any test claim",
        "claim_policy": "blocks local-GR promotion",
    },
]


RUNNER_MATRIX = [
    {
        "row_id": "R1_WEP_species_universality",
        "observable": "eta_WEP",
        "state": "budget_only",
        "source_lock": "2.8e-15",
        "source_lock_units": "dimensionless",
        "active_sources": "species F_A(C_D); mass/constant response; direct X/test charge; source-normalization species split",
        "coefficient_needed": "Delta F_AB, Delta m_A, Delta alpha_A, q_test_A differences",
        "fallback_source": "one_coframe_or_universal_coupling",
        "baseline": "GR/universal metric gives eta_WEP=0",
        "allowed_output": "suppression budget only; hardest ready row",
    },
    {
        "row_id": "R2_clock_redshift",
        "observable": "alpha_clock_redshift",
        "state": "budget_only",
        "source_lock": "3.1e-5",
        "source_lock_units": "dimensionless",
        "active_sources": "clock metric mismatch; common-mode phi_C; varying constants; coframe closure",
        "coefficient_needed": "clock coupling coefficients and phi_C clock response",
        "fallback_source": "one_coframe_or_universal_coupling",
        "baseline": "metric GR clock redshift",
        "allowed_output": "budget only",
    },
    {
        "row_id": "R3_gamma",
        "observable": "gamma_minus_1",
        "state": "budget_only",
        "source_lock": "2.3e-5",
        "source_lock_units": "dimensionless",
        "active_sources": "boundary TF/radial hair; bulk X; scalar/common mode; higher curvature; nonmetric light",
        "coefficient_needed": "C_TF, C_rad, C_bulk, C_nonmetric_light, c_i operator coefficients",
        "fallback_source": "EH_operator_selection; boundary_class_only_or_Ward_flux; bulk_X_nohair_or_force_law",
        "baseline": "GR PPN gamma=1",
        "allowed_output": "budget only",
    },
    {
        "row_id": "R4_beta",
        "observable": "beta_minus_1",
        "state": "budget_only",
        "source_lock": "7.8e-5",
        "source_lock_units": "dimensionless",
        "active_sources": "radial boundary hair; nonlinear boundary/source terms; bulk X; higher-curvature operators",
        "coefficient_needed": "C_rad2, C_boundary_nl, C_bulk2, c_i nonlinear coefficients",
        "fallback_source": "EH_operator_selection; boundary_class_only_or_Ward_flux; source_normalization",
        "baseline": "GR PPN beta=1",
        "allowed_output": "budget only",
    },
    {
        "row_id": "R5_alpha1",
        "observable": "alpha1",
        "state": "budget_only",
        "source_lock": "1.0e-4",
        "source_lock_units": "dimensionless",
        "active_sources": "boundary B_0i; vector marker; domain normal; coframe slip",
        "coefficient_needed": "C_vec_alpha1, boundary/domain vector coefficients",
        "fallback_source": "preferred_frame_domain_covariance; boundary_class_only_or_Ward_flux",
        "baseline": "GR alpha1=0",
        "allowed_output": "budget only",
    },
    {
        "row_id": "R6_alpha2",
        "observable": "alpha2",
        "state": "budget_only",
        "source_lock": "2.0e-9",
        "source_lock_units": "dimensionless",
        "active_sources": "anisotropic coframe; domain vector; boundary B_0i; marker normal",
        "coefficient_needed": "C_vec_alpha2, anisotropic coframe/domain coefficients",
        "fallback_source": "preferred_frame_domain_covariance; boundary_class_only_or_Ward_flux",
        "baseline": "GR alpha2=0",
        "allowed_output": "budget only",
    },
    {
        "row_id": "R7_alpha3",
        "observable": "alpha3",
        "state": "contingent_budget",
        "source_lock": "4.0e-20",
        "source_lock_units": "dimensionless",
        "active_sources": "unowned boundary flux; momentum nonconservation; Ward-force leakage",
        "coefficient_needed": "flux/nonconservation channel coefficient and channel relevance",
        "fallback_source": "boundary_class_only_or_Ward_flux; preferred_frame_domain_covariance",
        "baseline": "GR alpha3=0",
        "allowed_output": "contingent guardrail only if channel exists",
    },
    {
        "row_id": "R8_xi",
        "observable": "xi",
        "state": "budget_only",
        "source_lock": "4.0e-9",
        "source_lock_units": "dimensionless",
        "active_sources": "trace-free boundary shear; domain/external anisotropy; projector/vector leakage",
        "coefficient_needed": "C_TF_lge2, C_domain_aniso, C_projector_aniso",
        "fallback_source": "boundary_class_only_or_Ward_flux; preferred_frame_domain_covariance; EH_operator_selection",
        "baseline": "GR xi=0",
        "allowed_output": "budget only",
    },
    {
        "row_id": "R9_Gdot",
        "observable": "Gdot_over_G",
        "state": "contingent_budget",
        "source_lock": "9.6e-15",
        "source_lock_units": "yr^-1",
        "active_sources": "G_eff/M_eff drift; time-dependent monopole; memory/source normalization; boundary flux",
        "coefficient_needed": "time derivative of G_eff, M_eff, source normalization, or flux channel",
        "fallback_source": "source_normalization; boundary_class_only_or_Ward_flux",
        "baseline": "GR constant G",
        "allowed_output": "contingent guardrail only if time variation channel exists",
    },
    {
        "row_id": "R10_fifth_force",
        "observable": "delta_G_or_fifth_force_yukawa",
        "state": "unscored_parameterized",
        "source_lock": "alpha_Y(lambda_Y) or alpha_X(lambda_X)",
        "source_lock_units": "range-dependent",
        "active_sources": "phi_C profile; bulk X; radial boundary hair; nonlocal kernel; source normalization",
        "coefficient_needed": "range lambda, coupling alpha, source charge, screening/composition law",
        "fallback_source": "bulk_X_nohair_or_force_law; source_normalization; boundary_class_only_or_Ward_flux",
        "baseline": "GR no fifth force beyond measured GM",
        "allowed_output": "force-law contract only; no scalar score",
    },
]


DERIVED_ZERO_BRANCHES = [
    {
        "branch": "one_coframe_if_parent_selected",
        "state": "conditional_zero",
        "zeros": "direct WEP/clock/nonmetric matter vertices",
        "premise": "one observed coframe/common F(C_D) is parent-derived",
        "current_status": "premise not derived; closure if assumed",
    },
    {
        "branch": "phiC_zero_if_boundary_state_and_trivial_class",
        "state": "conditional_zero",
        "zeros": "common-mode phi_C gradient contributions",
        "premise": "local boundary-state/trivial-class theorem holds",
        "current_status": "premise not parent-derived",
    },
    {
        "branch": "class_only_boundary_if_parent_forced",
        "state": "conditional_zero",
        "zeros": "B_TF and B_0i angular/vector boundary sources",
        "premise": "S_boundary has only scalar class arguments",
        "current_status": "class-only action not parent-derived",
    },
    {
        "branch": "bulk_X_mass_gap_if_parent_forced",
        "state": "conditional_zero",
        "zeros": "source-free regular decaying bulk X hair",
        "premise": "positive operator (-Delta+m_X^2), no exterior source, good boundary data",
        "current_status": "operator/source conditions not parent-derived",
    },
    {
        "branch": "EH_if_full_stack_closes",
        "state": "conditional_zero",
        "zeros": "non-EH local operator coefficients through PPN order",
        "premise": "Ward closure + no-hair + universal coupling + metric-only local 4D second-order exterior",
        "current_status": "stack not closed",
    },
]


BASELINE_COMPARISON_POLICY = [
    {
        "policy": "GR_baseline_explicit",
        "implementation": "every local row records the GR value or GR absence of channel",
        "reason": "local tests must compare against a baseline rather than treating MTS alone as guilty",
    },
    {
        "policy": "same_pipeline_for_baseline_when_possible",
        "implementation": "if a future numerical pipeline evaluates a row, run the GR/null branch through the same code path",
        "reason": "pipeline failures should not be confused with MTS-only failures",
    },
    {
        "policy": "no_fifth_force_scalar_shortcut",
        "implementation": "fifth-force row remains alpha(lambda)/profile based until range and coupling are derived",
        "reason": "one scalar fifth-force score is fake precision",
    },
    {
        "policy": "closure_branch_label_visible",
        "implementation": "closure_zero rows are separated from derived_zero rows in every output",
        "reason": "a closure can be tested but not advertised as a parent derivation",
    },
    {
        "policy": "budget_not_pass",
        "implementation": "numeric source locks produce ceilings but pass_claim_allowed remains false",
        "reason": "missing coefficients block observational pass claims",
    },
]


LOCAL_TEST_QUEUE = [
    {
        "priority": 1,
        "test": "WEP_species_budget_stress",
        "rows": "eta_WEP",
        "run_type": "symbolic/numeric budget matrix",
        "not_allowed": "WEP pass claim",
    },
    {
        "priority": 2,
        "test": "boundary_bulk_gamma_beta_budget",
        "rows": "gamma_minus_1; beta_minus_1",
        "run_type": "coefficient sensitivity matrix",
        "not_allowed": "PPN pass claim",
    },
    {
        "priority": 3,
        "test": "preferred_frame_xi_budget",
        "rows": "alpha1; alpha2; alpha3; xi",
        "run_type": "source-locked coefficient budget",
        "not_allowed": "preferred-frame pass claim",
    },
    {
        "priority": 4,
        "test": "source_normalization_Gdot_deltaG_guard",
        "rows": "Gdot_over_G; delta_G_or_fifth_force_yukawa",
        "run_type": "contingent/unscored guardrail",
        "not_allowed": "GM absorption or fifth-force pass claim",
    },
    {
        "priority": 5,
        "test": "GR_null_baseline_pipeline",
        "rows": "all numeric-ready rows",
        "run_type": "baseline sanity pass",
        "not_allowed": "declaring MTS failure before baseline pipeline is checked",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Local-bound runner v2 classifies every retained residual into derived-zero, conditional-zero, closure-zero, budget-only, contingent-budget, or unscored-parameterized states. Numeric source locks now produce stress budgets, not passes. Fifth-force/delta_G remains range/coupling based. The runner is ready for disciplined local stress tests but no WEP, PPN, fifth-force, EH, or local-GR claim is allowed.",
        "hardest_ready_row": "eta_WEP",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "attempt the first variation of the minimal parent action and identify which block obstructs closure first",
        "pass_condition": "the action contract is stress-tested by explicit variation rather than only a runner matrix",
    },
    {
        "priority": 2,
        "target": "385-local-bound-runner-v2-smoke-matrix.md",
        "task": "run a small coefficient-sensitivity smoke using symbolic coefficient priors and GR/null baseline rows",
        "pass_condition": "budgets populate without pass claims and baseline/null branch sanity is shown",
    },
    {
        "priority": 3,
        "target": "386-WEP-species-symmetry-or-closure-hardening.md",
        "task": "try to derive a species symmetry forcing common F(C_D), or harden the WEP closure status",
        "pass_condition": "eta_WEP either gets a parent selector route or remains the top active local debt",
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


def matrix_with_budgets() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in RUNNER_MATRIX:
        source_lock = row["source_lock"]
        numeric_scale = ""
        equal_share_two = ""
        equal_share_four = ""
        pass_claim_allowed = False
        if row["state"] in {"budget_only", "contingent_budget"}:
            try:
                numeric_scale = float(source_lock)
                equal_share_two = numeric_scale / 2.0
                equal_share_four = numeric_scale / 4.0
            except ValueError:
                numeric_scale = ""
        rows.append(
            {
                **row,
                "numeric_scale": numeric_scale,
                "equal_share_ceiling_two_terms": equal_share_two,
                "equal_share_ceiling_four_terms": equal_share_four,
                "coefficient_status": "missing",
                "pass_claim_allowed": pass_claim_allowed,
            }
        )
    return rows


def pressure_ranking_rows(matrix_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    numeric_rows = [
        row for row in matrix_rows if isinstance(row["numeric_scale"], float)
    ]
    numeric_rows.sort(key=lambda row: row["numeric_scale"])
    rows: list[dict[str, Any]] = []
    for rank, row in enumerate(numeric_rows, start=1):
        rows.append(
            {
                "rank": rank,
                "observable": row["observable"],
                "row_id": row["row_id"],
                "state": row["state"],
                "numeric_scale": row["numeric_scale"],
                "source_lock_units": row["source_lock_units"],
                "pressure_note": "hardest ready row" if row["observable"] == "eta_WEP" else "source-locked local budget row",
            }
        )
    for row in matrix_rows:
        if row["state"] == "unscored_parameterized":
            rows.append(
                {
                    "rank": "unscored",
                    "observable": row["observable"],
                    "row_id": row["row_id"],
                    "state": row["state"],
                    "numeric_scale": "",
                    "source_lock_units": row["source_lock_units"],
                    "pressure_note": "range/coupling/profile required before numeric ranking",
                }
            )
    return rows


def gate_rows(source_rows: list[dict[str, Any]], matrix_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    budget_rows = [row for row in matrix_rows if row["state"] == "budget_only"]
    contingent_rows = [row for row in matrix_rows if row["state"] == "contingent_budget"]
    unscored_rows = [row for row in matrix_rows if row["state"] == "unscored_parameterized"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "state_definitions_written",
            "status": "pass",
            "evidence": f"{len(STATE_DEFINITIONS)} runner states defined",
        },
        {
            "gate": "retained_residual_matrix_written",
            "status": "pass",
            "evidence": f"{len(matrix_rows)} retained observable rows classified",
        },
        {
            "gate": "numeric_budget_rows_loaded",
            "status": "pass",
            "evidence": f"{len(budget_rows)} budget-only rows and {len(contingent_rows)} contingent budget rows",
        },
        {
            "gate": "unscored_parameterized_rows_retained",
            "status": "pass",
            "evidence": f"{len(unscored_rows)} rows require range/coupling/profile before scoring",
        },
        {
            "gate": "baseline_policy_written",
            "status": "pass",
            "evidence": "GR/null baseline and same-pipeline policy recorded",
        },
        {
            "gate": "pass_claims_blocked",
            "status": "pass",
            "evidence": "all rows have missing coefficients or conditional states; no pass claims allowed",
        },
        {
            "gate": "local_GR_or_PPN_promoted",
            "status": "fail",
            "evidence": "runner matrix only; parent-action contract remains unsatisfied",
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
    matrix_rows = matrix_with_budgets()

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "state_definitions.csv", STATE_DEFINITIONS)
    write_csv(results_dir / "retained_residual_runner_matrix.csv", matrix_rows)
    write_csv(results_dir / "derived_zero_branch_register.csv", DERIVED_ZERO_BRANCHES)
    write_csv(results_dir / "pressure_ranking.csv", pressure_ranking_rows(matrix_rows))
    write_csv(results_dir / "baseline_comparison_policy.csv", BASELINE_COMPARISON_POLICY)
    write_csv(results_dir / "local_test_queue.csv", LOCAL_TEST_QUEUE)
    write_csv(results_dir / "gate_results.csv", gate_rows(source_rows, matrix_rows))
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
        "runner_states": len(STATE_DEFINITIONS),
        "retained_residual_rows": len(matrix_rows),
        "budget_only_rows": sum(1 for row in matrix_rows if row["state"] == "budget_only"),
        "contingent_budget_rows": sum(1 for row in matrix_rows if row["state"] == "contingent_budget"),
        "unscored_parameterized_rows": sum(1 for row in matrix_rows if row["state"] == "unscored_parameterized"),
        "hardest_ready_row": "eta_WEP",
        "pass_claim_allowed": False,
        "derived_local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 383 local-bound runner v2 artifacts."
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

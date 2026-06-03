from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "EH-operator-retained-ledger-and-source-normalization-test-plan"
CHECKPOINT_DOC = "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md"
STATUS = "EH_operator_retained_ledger_and_source_normalization_test_plan_written_operator_source_test_matrix_ready_no_data_claim_no_local_GR_pass"
CLAIM_CEILING = "EH_operator_retained_ledger_source_normalization_test_plan_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "426-local-bound-runner-v4-dryrun-wrapper.md"


SOURCE_DOCS = [
    {
        "path": "392-EH-operator-selection-under-identity-closure.md",
        "role": "EH selection obstruction, non-EH operator ledger, source-normalization blocker",
    },
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH/source pair and weak-field G_eff/M_eff algebra",
    },
    {
        "path": "405-same-frame-EH-source-derived-stack-audit.md",
        "role": "local GR/Newton stack rungs and no-promotion policy",
    },
    {
        "path": "408-local-bound-data-runner-v4-smoke.md",
        "role": "runner-v4 smoke profiles, edge failures, and baseline controls",
    },
    {
        "path": "411-local-bound-runner-v4-real-data-interface.md",
        "role": "bounds CSV schema, local data targets, and VS Code dry-run/evaluate workflow",
    },
    {
        "path": "412-v4-source-charge-channel-map-review.md",
        "role": "R1 source-charge channel split and direct/full WEP guardrail",
    },
    {
        "path": "419-boundary-exchange-coefficient-retained-evaluator.md",
        "role": "retained boundary/exchange coefficient locks and alpha3/Gdot/vector/shear/radial rows",
    },
    {
        "path": "423-parent-action-minimality-no-extension-theorem-attempt.md",
        "role": "minimality/no-extension obstruction and material-marker caveat",
    },
    {
        "path": "424-same-frame-EH-source-Poisson-reduction-gate.md",
        "role": "conditional EH to Poisson bridge and same-frame/source premises",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv",
        "role": "runner-v4 row-state matrix for R0-R11 no-promotion audit",
    },
    {
        "path": "runs/20260602-061500-local-bound-runner-v4-real-data-interface/results/local_data_targets.csv",
        "role": "local data target row locks and observable labels",
    },
    {
        "path": "runs/20260602-061500-local-bound-runner-v4-real-data-interface/results/local_bounds_template.csv",
        "role": "bounds CSV schema/template for future external-data fill",
    },
    {
        "path": "runs/20260602-073500-boundary-exchange-coefficient-retained-evaluator/results/retained_coefficients.csv",
        "role": "retained coefficient source-lock table for boundary/exchange rows",
    },
    {
        "path": "runs/20260602-084000-same-frame-EH-source-Poisson-reduction-gate/results/gate_results.csv",
        "role": "previous Poisson-gate status and claim ceiling",
    },
]


EH_OPERATOR_RETAINED_LEDGER = [
    {
        "operator_family": "EH_plus_Lambda_baseline",
        "role": "target GR/null baseline only after the full same-frame/source stack is earned",
        "affected_rows": "R0;R2;R3;R4;R5;R6;R7;R8;R9;R10;R11",
        "observable_locks": "all local-bound rows must be included as baseline controls",
        "test_policy": "always compare MTS stress rows against a GR/null baseline in the same pipeline",
        "current_status": "target_only_not_parent_derived",
        "promotion_condition": "same-frame EH operator, constant kappa, source-normalized measured mass, and Bianchi ownership derived",
    },
    {
        "operator_family": "boundary_topological_terms",
        "role": "boundary/topological terms can be harmless only if class-only, topological, or Ward-owned",
        "affected_rows": "R3;R4;R7;R8",
        "observable_locks": "gamma <= 2.3e-05; beta <= 7.8e-05; alpha3 <= 4e-20; xi <= 4e-09",
        "test_policy": "retain coefficients unless pure boundary/topological class theorem is supplied",
        "current_status": "retained",
        "promotion_condition": "prove zero local stress/exchange contribution or map coefficient into retained lock",
    },
    {
        "operator_family": "R2_fR_scalar_mode",
        "role": "higher-curvature scalar mode can mimic fifth force or PPN slip",
        "affected_rows": "R3;R4;R10;R11",
        "observable_locks": "gamma/beta locks plus symbolic alpha(lambda) curve",
        "test_policy": "range-sweep the scalar mass/coupling; do not treat symbolic R10/R11 as a pass",
        "current_status": "retained_symbolic",
        "promotion_condition": "derive infinite scalar mass, zero coupling, or explicit alpha(lambda) below data curve",
    },
    {
        "operator_family": "Ricci_Weyl_squared",
        "role": "quadratic tensor operators can shift slip, preferred-location, or wave-sector behavior",
        "affected_rows": "R3;R8;R11",
        "observable_locks": "gamma <= 2.3e-05; xi <= 4e-09; symbolic non-EH ledger",
        "test_policy": "keep coefficient ledger and wave-sector note separate from EH selection",
        "current_status": "retained_symbolic",
        "promotion_condition": "derive coefficient zero/pure boundary status or measured-safe coefficient range",
    },
    {
        "operator_family": "scalar_tensor_class_metric",
        "role": "class-metric or scalar-tensor branches can pass some tests while retaining clock/Gdot/fifth-force debts",
        "affected_rows": "R2;R3;R4;R9;R10;R11",
        "observable_locks": "clock <= 3.1e-05; gamma <= 2.3e-05; beta <= 7.8e-05; Gdot/G <= 9.6e-15 yr^-1",
        "test_policy": "score as retained comparison branch, never as derived EH",
        "current_status": "retained",
        "promotion_condition": "derive scalar silence, universal source charge, and constant G_eff",
    },
    {
        "operator_family": "vector_preferred_frame",
        "role": "vector/domain/projector hair threatens preferred-frame and self-acceleration rows",
        "affected_rows": "R5;R6;R7;R8;R11",
        "observable_locks": "alpha1 <= 1e-04; alpha2 <= 2e-09; alpha3 <= 4e-20; xi <= 4e-09",
        "test_policy": "retain vector coefficients and run alpha1/alpha2/alpha3/xi rows together",
        "current_status": "retained",
        "promotion_condition": "derive vector/domain no-hair or pure gauge status in the observed frame",
    },
    {
        "operator_family": "torsion_nonmetricity",
        "role": "torsion or nonmetricity can create WEP, clock, spin, or light-cone split channels",
        "affected_rows": "R0;R1;R2;R11",
        "observable_locks": "WEP <= 2.8e-15; clock <= 3.1e-05; symbolic non-EH ledger",
        "test_policy": "forbid only by compatibility theorem; otherwise retain source/light-cone rows",
        "current_status": "retained_symbolic",
        "promotion_condition": "derive metric compatibility and zero torsion in the local observed branch",
    },
    {
        "operator_family": "bulk_X_force_law",
        "role": "bulk-X coupling can source extra potentials, source charge, or fifth-force terms",
        "affected_rows": "R1;R3;R4;R10;R11",
        "observable_locks": "WEP <= 2.8e-15; gamma/beta locks; symbolic alpha(lambda)",
        "test_policy": "retain alpha_X(lambda_X) until local kernel/source silence is derived",
        "current_status": "retained",
        "promotion_condition": "derive alpha_X=0 or measured-safe mass/range/coupling curve",
    },
    {
        "operator_family": "nonlocal_memory_kernel",
        "role": "memory terms can drift G_eff, alter range dependence, or leak exchange currents",
        "affected_rows": "R7;R9;R10;R11",
        "observable_locks": "alpha3 <= 4e-20; Gdot/G <= 9.6e-15 yr^-1; symbolic alpha(lambda)",
        "test_policy": "test drift rows before any cosmology-memory interpretation is promoted locally",
        "current_status": "retained",
        "promotion_condition": "derive local kernel silence/screening and Bianchi-owned exchange",
    },
    {
        "operator_family": "source_normalization_operator",
        "role": "hidden source-charge/G_eff/M_eff normalization debts can make Poisson algebra look better than it is",
        "affected_rows": "R1;R4;R9;R10;R11",
        "observable_locks": "WEP <= 2.8e-15; beta <= 7.8e-05; Gdot/G <= 9.6e-15 yr^-1; symbolic alpha(lambda)",
        "test_policy": "split direct WEP channels from full source-normalization channel and keep both visible",
        "current_status": "retained_core_blocker",
        "promotion_condition": "derive constant, conserved, universal, range-independent measured GM",
    },
]


SOURCE_NORMALIZATION_CHANNEL_PLAN = [
    {
        "channel": "constant_Geff",
        "local_bound_rows": "R9",
        "observable": "Gdot/G",
        "source_lock": "9.6e-15 yr^-1",
        "required_parent_identity": "partial_t kappa_eff = partial_r kappa_eff = partial_A kappa_eff = 0",
        "test_output": "numeric residual ratio against Gdot/G row",
        "current_status": "not_derived",
    },
    {
        "channel": "species_independent_source",
        "local_bound_rows": "R1",
        "observable": "WEP source-charge split",
        "source_lock": "2.8e-15",
        "required_parent_identity": "partial_A mu_obs = 0 across material species",
        "test_output": "direct WEP subscore plus full four-channel R1 composite",
        "current_status": "not_derived",
    },
    {
        "channel": "conserved_measured_mass",
        "local_bound_rows": "R4;R9",
        "observable": "perihelion beta and Gdot/G",
        "source_lock": "7.8e-05; 9.6e-15 yr^-1",
        "required_parent_identity": "dM_eff/dt = 0 and no source-normalization pressure/stress residue",
        "test_output": "beta/Gdot residual flags",
        "current_status": "not_derived",
    },
    {
        "channel": "range_independent_GM",
        "local_bound_rows": "R10",
        "observable": "inverse-square/Yukawa alpha(lambda)",
        "source_lock": "symbolic alpha(lambda) curve",
        "required_parent_identity": "partial_lambda mu_obs = 0 and no finite-range extra potential",
        "test_output": "symbolic until a verified alpha(lambda) curve is supplied",
        "current_status": "not_derived_symbolic",
    },
    {
        "channel": "boundary_bulk_domain_mass_silence",
        "local_bound_rows": "R3;R4;R7;R8;R9",
        "observable": "gamma, beta, alpha3, xi, Gdot/G",
        "source_lock": "2.3e-05; 7.8e-05; 4e-20; 4e-09; 9.6e-15 yr^-1",
        "required_parent_identity": "mu_extra[B,X,D,J_rel,P] = 0 or coefficient-retained below lock",
        "test_output": "join to retained_coefficients.csv",
        "current_status": "retained",
    },
    {
        "channel": "same_frame_calibration",
        "local_bound_rows": "R0;R2;R11",
        "observable": "geometry/source/frame split",
        "source_lock": "closure row plus clock and symbolic non-EH ledger",
        "required_parent_identity": "matter and gravitational variation use the same observed metric/coframe",
        "test_output": "counterexample branch if frame split remains legal",
        "current_status": "not_parent_derived",
    },
    {
        "channel": "PPN_second_order_completion",
        "local_bound_rows": "R3;R4;R5;R6;R8",
        "observable": "gamma, beta, alpha1, alpha2, xi",
        "source_lock": "2.3e-05; 7.8e-05; 1e-04; 2e-09; 4e-09",
        "required_parent_identity": "second-order weak-field metric closes with no vector/scalar/projector residues",
        "test_output": "PPN residual vector",
        "current_status": "not_derived",
    },
]


LOCAL_BOUND_TEST_MATRIX = [
    {
        "test_id": "GR_null_baseline_same_pipeline",
        "target_rows": "R0-R11",
        "baseline_required": "yes",
        "input_needed": "runner-v4 internal locks",
        "expected_output": "all rows scored as GR/null control with no MTS theorem credit",
        "claim_policy": "baseline_only",
    },
    {
        "test_id": "identity_closure_zero_control",
        "target_rows": "R0",
        "baseline_required": "yes",
        "input_needed": "eta_WEP_direct_geometry closure-zero row",
        "expected_output": "closure zero visible but not promoted to WEP theorem",
        "claim_policy": "control_only",
    },
    {
        "test_id": "EH_operator_symbolic_ledger_dryrun",
        "target_rows": "R11",
        "baseline_required": "yes",
        "input_needed": "EH_OPERATOR_RETAINED_LEDGER",
        "expected_output": "non-EH operator rows remain symbolic/retained",
        "claim_policy": "no_symbolic_pass",
    },
    {
        "test_id": "scalar_mode_range_sweep_placeholder",
        "target_rows": "R3;R4;R10;R11",
        "baseline_required": "yes",
        "input_needed": "future alpha(lambda) curve and scalar mass/coupling map",
        "expected_output": "range grid only after verified curve exists",
        "claim_policy": "defer",
    },
    {
        "test_id": "source_normalization_four_channel_R1",
        "target_rows": "R1",
        "baseline_required": "yes",
        "input_needed": "direct WEP plus source-normalization channels from checkpoint 412",
        "expected_output": "direct subscore and full R1 composite both reported",
        "claim_policy": "retain_full_channel",
    },
    {
        "test_id": "Cassini_gamma_row",
        "target_rows": "R3",
        "baseline_required": "yes",
        "input_needed": "gamma residual estimate",
        "expected_output": "residual ratio against 2.3e-05 lock",
        "claim_policy": "numeric_only",
    },
    {
        "test_id": "perihelion_beta_row",
        "target_rows": "R4",
        "baseline_required": "yes",
        "input_needed": "beta/source-normalization residual estimate",
        "expected_output": "residual ratio against 7.8e-05 lock",
        "claim_policy": "numeric_only",
    },
    {
        "test_id": "preferred_frame_vector_rows",
        "target_rows": "R5;R6;R7;R8",
        "baseline_required": "yes",
        "input_needed": "vector/domain/projector residual estimates",
        "expected_output": "alpha1/alpha2/alpha3/xi vector residual vector",
        "claim_policy": "numeric_only",
    },
    {
        "test_id": "Gdot_source_drift_row",
        "target_rows": "R9",
        "baseline_required": "yes",
        "input_needed": "G_eff or M_eff drift estimate",
        "expected_output": "residual ratio against 9.6e-15 yr^-1 lock",
        "claim_policy": "numeric_only",
    },
    {
        "test_id": "fifth_force_curve_row",
        "target_rows": "R10",
        "baseline_required": "yes",
        "input_needed": "verified alpha(lambda) curve",
        "expected_output": "symbolic/unscored until curve supplied",
        "claim_policy": "no_symbolic_pass",
    },
    {
        "test_id": "boundary_exchange_retained_rows",
        "target_rows": "R3;R4;R7;R8;R9",
        "baseline_required": "yes",
        "input_needed": "retained_coefficients.csv",
        "expected_output": "coefficient-lock ratios and source owner labels",
        "claim_policy": "retained_coefficients_only",
    },
    {
        "test_id": "same_frame_vs_frame_split_counterexample",
        "target_rows": "R2;R3;R4;R11",
        "baseline_required": "yes",
        "input_needed": "frame-split counterexample residuals",
        "expected_output": "no local-GR promotion if matter/gravity frames diverge",
        "claim_policy": "counterexample_guard",
    },
]


RUNNER_V4_INTEGRATION_PLAN = [
    {
        "step": "load_runner_v4_matrix",
        "input_path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv",
        "operation": "read row_id, observable, row_state, promotion_policy",
        "output": "row-state map",
        "guardrail": "do not convert closure/retained rows into theorem zeros",
    },
    {
        "step": "load_local_data_targets",
        "input_path": "runs/20260602-061500-local-bound-runner-v4-real-data-interface/results/local_data_targets.csv",
        "operation": "read R0-R11 locks and observable labels",
        "output": "target-lock map",
        "guardrail": "R10/R11 remain symbolic unless a verified external curve/operator ledger is supplied",
    },
    {
        "step": "join_retained_coefficients",
        "input_path": "runs/20260602-073500-boundary-exchange-coefficient-retained-evaluator/results/retained_coefficients.csv",
        "operation": "join coefficient locks to rows R3/R4/R7/R8/R9",
        "output": "boundary/exchange coefficient residual ledger",
        "guardrail": "engineering tiny numbers can still fail alpha3 by orders of magnitude",
    },
    {
        "step": "score_numeric_rows_only",
        "input_path": "source-intake/local_bounds/local_bound_claims.csv",
        "operation": "compare residuals to numeric locks where units and row_id are explicit",
        "output": "external_bound_evaluation.csv",
        "guardrail": "symbolic rows report missing curve/operator data rather than pass",
    },
    {
        "step": "emit_R1_subscores",
        "input_path": "412-v4-source-charge-channel-map-review.md",
        "operation": "report direct WEP subscore and full source-normalization composite",
        "output": "source_charge_channel_report.csv",
        "guardrail": "do not hide source-normalization channel inside direct WEP success",
    },
    {
        "step": "write_status_markers",
        "input_path": "scripts/local_bound_runner_v4_real_data_interface.py",
        "operation": "write status.json, log.txt, DONE.txt in a timestamped run folder",
        "output": "runs/<timestamp>/status.json and DONE.txt",
        "guardrail": "long runs happen in VS Code; Codex inspects output after DONE",
    },
]


DRY_RUN_WORKFLOW = [
    {
        "workflow_step": "prepare_bounds_csv",
        "powershell_command": "$py = 'D:\\Users\\ollet\\Desktop\\Turn an intuitive research programme into a formal field-theoretic framework\\Motion-TimeSpace--main\\post-checkpoint-work\\.venv-score\\Scripts\\python.exe'; $pc = 'D:\\Users\\ollet\\Desktop\\Turn an intuitive research programme into a formal field-theoretic framework\\Motion-TimeSpace--main\\post-checkpoint-work'; & $py (Join-Path $pc 'scripts\\local_bound_runner_v4_real_data_interface.py') --mode dry-run",
        "wait_policy": "safe_short_run",
        "expected_marker": "DONE.txt",
    },
    {
        "workflow_step": "validate_schema",
        "powershell_command": "open the generated local_bounds_template.csv and fill only verified rows with source paths/URLs",
        "wait_policy": "manual_data_entry",
        "expected_marker": "local_bound_claims.csv exists",
    },
    {
        "workflow_step": "evaluate_short_smoke",
        "powershell_command": "$py = 'D:\\Users\\ollet\\Desktop\\Turn an intuitive research programme into a formal field-theoretic framework\\Motion-TimeSpace--main\\post-checkpoint-work\\.venv-score\\Scripts\\python.exe'; $pc = 'D:\\Users\\ollet\\Desktop\\Turn an intuitive research programme into a formal field-theoretic framework\\Motion-TimeSpace--main\\post-checkpoint-work'; & $py (Join-Path $pc 'scripts\\local_bound_runner_v4_real_data_interface.py') --mode evaluate --bounds-csv (Join-Path $pc 'source-intake\\local_bounds\\local_bound_claims.csv')",
        "wait_policy": "safe_short_run_after_data_file_exists",
        "expected_marker": "external_bound_evaluation.csv",
    },
    {
        "workflow_step": "write_run_marker",
        "powershell_command": "check runs/<timestamp>/status.json and DONE.txt before interpreting results",
        "wait_policy": "no_token_waiting",
        "expected_marker": "status.json plus DONE.txt",
    },
    {
        "workflow_step": "VS_Code_long_run_policy",
        "powershell_command": "if a future run becomes slow, start it in the VS Code terminal and prompt Codex only after DONE.txt appears",
        "wait_policy": "user_reprompts_after_completion",
        "expected_marker": "DONE.txt",
    },
]


ROW_TRANSITION_ATTEMPT = [
    {
        "row_id": "R0",
        "observable": "eta_WEP_direct_geometry",
        "previous_state": "closure_zero_control",
        "new_state": "control_only",
        "reason": "direct geometry closure remains a control, not a full source-normalization proof",
        "theorem_credit": "no",
    },
    {
        "row_id": "R1",
        "observable": "WEP_source_charge",
        "previous_state": "retained_contingent_budget",
        "new_state": "retained_four_channel_test_required",
        "reason": "direct WEP and source-normalization channels must both be visible",
        "theorem_credit": "no",
    },
    {
        "row_id": "R2",
        "observable": "clock_redshift",
        "previous_state": "retained_budget",
        "new_state": "retained_same_frame_clock_check",
        "reason": "frame split or nonmetricity can leak into clock tests",
        "theorem_credit": "no",
    },
    {
        "row_id": "R3",
        "observable": "Shapiro_gamma",
        "previous_state": "retained_budget",
        "new_state": "EH_operator_slip_test",
        "reason": "non-EH scalar/tensor/boundary terms can alter gamma",
        "theorem_credit": "no",
    },
    {
        "row_id": "R4",
        "observable": "perihelion_beta",
        "previous_state": "retained_budget",
        "new_state": "source_normalization_beta_test",
        "reason": "hidden measured-GM changes can show up as beta/source residuals",
        "theorem_credit": "no",
    },
    {
        "row_id": "R5",
        "observable": "preferred_frame_alpha1",
        "previous_state": "retained_budget",
        "new_state": "vector_preferred_frame_test",
        "reason": "vector/domain hair must be scored with same pipeline baseline",
        "theorem_credit": "no",
    },
    {
        "row_id": "R6",
        "observable": "preferred_frame_alpha2",
        "previous_state": "retained_budget",
        "new_state": "vector_preferred_frame_test",
        "reason": "alpha2 lock is tight and cannot be bypassed by EH algebra alone",
        "theorem_credit": "no",
    },
    {
        "row_id": "R7",
        "observable": "self_acceleration_alpha3",
        "previous_state": "retained_budget",
        "new_state": "boundary_exchange_ultratight_test",
        "reason": "alpha3 lock is severe enough that engineering-small leakage can still fail",
        "theorem_credit": "no",
    },
    {
        "row_id": "R8",
        "observable": "preferred_location_xi",
        "previous_state": "retained_budget",
        "new_state": "domain_shear_preferred_location_test",
        "reason": "domain/projector/shear terms need explicit coefficient locks",
        "theorem_credit": "no",
    },
    {
        "row_id": "R9",
        "observable": "Gdot_over_G",
        "previous_state": "retained_budget",
        "new_state": "memory_source_drift_test",
        "reason": "constant kappa and conserved measured mass remain unproved",
        "theorem_credit": "no",
    },
    {
        "row_id": "R10",
        "observable": "inverse_square_yukawa",
        "previous_state": "symbolic_source_lock",
        "new_state": "symbolic_curve_required",
        "reason": "no alpha(lambda) curve means no fifth-force pass",
        "theorem_credit": "no",
    },
    {
        "row_id": "R11",
        "observable": "non_EH_operator_ledger",
        "previous_state": "symbolic_operator_lock",
        "new_state": "retained_EH_operator_ledger",
        "reason": "operator families are now explicit but not eliminated",
        "theorem_credit": "no",
    },
]


DECISION = [
    {
        "decision": "Build and use the retained EH-operator/source-normalization local-bound test plan before any local-GR promotion. The Poisson bridge remains conditionally clean, but EH selection and measured-GM normalization are not parent-derived. This checkpoint converts that gap into explicit rows/tests rather than treating it as failure or success.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "stable_evidence": "no",
        "local_GR_pass": "no",
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "next_file": "426-local-bound-runner-v4-dryrun-wrapper.md",
        "task": "wrap runner-v4 dry-run/evaluate flow around this EH/source ledger and preserve GR/null baselines",
        "priority": "P0",
    },
    {
        "next_file": "426-source-normalization-bounds-csv-template-fill.md",
        "task": "prepare the verified external local-bound CSV source-intake template without making data claims",
        "priority": "P0",
    },
    {
        "next_file": "426-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "task": "try to derive the exchange-owner identity needed to make source_residuals vanish",
        "priority": "P1",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for item in SOURCE_DOCS:
        source_path = ROOT / item["path"]
        rows.append(
            {
                "source_file": item["path"],
                "exists": source_path.exists(),
                "role": item["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row for row in source_rows if not row["exists"]]
    theorem_credit_rows = [row for row in ROW_TRANSITION_ATTEMPT if row["theorem_credit"] == "yes"]
    symbolic_tests = [
        row
        for row in LOCAL_BOUND_TEST_MATRIX
        if "symbolic" in row["claim_policy"] or "defer" in row["claim_policy"]
    ]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": f"{len(missing_sources)} missing source paths",
        },
        {
            "gate": "EH_operator_ledger_written",
            "status": "pass",
            "evidence": f"{len(EH_OPERATOR_RETAINED_LEDGER)} operator families retained or targeted",
        },
        {
            "gate": "source_normalization_plan_written",
            "status": "pass",
            "evidence": f"{len(SOURCE_NORMALIZATION_CHANNEL_PLAN)} source-normalization channels",
        },
        {
            "gate": "local_bound_test_matrix_written",
            "status": "pass",
            "evidence": f"{len(LOCAL_BOUND_TEST_MATRIX)} local-bound tests with baseline policy",
        },
        {
            "gate": "runner_v4_integration_written",
            "status": "pass",
            "evidence": f"{len(RUNNER_V4_INTEGRATION_PLAN)} integration steps",
        },
        {
            "gate": "symbolic_rows_protected",
            "status": "pass",
            "evidence": f"{len(symbolic_tests)} tests explicitly block symbolic pass-through",
        },
        {
            "gate": "GR_null_baseline_required",
            "status": "pass",
            "evidence": "every local-bound test row requires same-pipeline baseline comparison",
        },
        {
            "gate": "R1_subscores_preserved",
            "status": "pass",
            "evidence": "direct WEP subscore and full four-channel R1 composite both required",
        },
        {
            "gate": "EH_operator_selection_derived",
            "status": "fail",
            "evidence": "operator families are retained/tested, not parent-eliminated",
        },
        {
            "gate": "source_normalization_parent_derived",
            "status": "fail",
            "evidence": "constant, conserved, universal, range-independent measured GM remains unproved",
        },
        {
            "gate": "real_external_data_loaded",
            "status": "not_run",
            "evidence": "this checkpoint writes the plan; no external local-bound CSV evaluated",
        },
        {
            "gate": "runner_rows_promoted_to_theorem_zero",
            "status": "pass" if not theorem_credit_rows else "fail",
            "evidence": f"{len(theorem_credit_rows)} rows granted theorem credit",
        },
        {
            "gate": "claim_leaks",
            "status": "pass",
            "evidence": "all decisions keep no-data-claim and no-local-GR ceiling",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "testing plan only; no WEP/EH/Newton/PPN/fifth-force pass",
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
    source_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, str]],
) -> None:
    source_table_rows = [
        {
            "source_file": row["source_file"],
            "exists": row["exists"],
            "role": row["role"],
        }
        for row in source_rows
    ]
    operator_table_rows = [
        {
            "operator_family": row["operator_family"],
            "affected_rows": row["affected_rows"],
            "current_status": row["current_status"],
            "test_policy": row["test_policy"],
        }
        for row in EH_OPERATOR_RETAINED_LEDGER
    ]
    source_channel_table_rows = [
        {
            "channel": row["channel"],
            "local_bound_rows": row["local_bound_rows"],
            "source_lock": row["source_lock"],
            "current_status": row["current_status"],
        }
        for row in SOURCE_NORMALIZATION_CHANNEL_PLAN
    ]
    test_matrix_table_rows = [
        {
            "test_id": row["test_id"],
            "target_rows": row["target_rows"],
            "baseline_required": row["baseline_required"],
            "claim_policy": row["claim_policy"],
        }
        for row in LOCAL_BOUND_TEST_MATRIX
    ]
    integration_table_rows = [
        {
            "step": row["step"],
            "output": row["output"],
            "guardrail": row["guardrail"],
        }
        for row in RUNNER_V4_INTEGRATION_PLAN
    ]
    dry_run_table_rows = [
        {
            "workflow_step": row["workflow_step"],
            "wait_policy": row["wait_policy"],
            "expected_marker": row["expected_marker"],
        }
        for row in DRY_RUN_WORKFLOW
    ]
    transition_table_rows = [
        {
            "row_id": row["row_id"],
            "observable": row["observable"],
            "new_state": row["new_state"],
            "theorem_credit": row["theorem_credit"],
        }
        for row in ROW_TRANSITION_ATTEMPT
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 425 - EH Operator Retained Ledger and Source-Normalization Test Plan

Private local-GR testing checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 424 showed that the algebraic EH-to-Poisson bridge is clean if the parent theory earns the same-frame EH/source premises. This checkpoint does the unglamorous but essential next thing: it turns the unearned EH-operator and measured-source-normalization premises into an explicit retained ledger and local-bound test plan.

The result is not grim. It is a way to stop the theory from accidentally helping itself to GR. We now have a checklist for what must be derived, what can be tested numerically, and what remains symbolic until real bounds or parent identities exist.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/EH_operator_retained_ledger_and_source_normalization_test_plan.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_table_rows, ["source_file", "exists", "role"])}

## 4. EH Operator Retained Ledger

{markdown_table(operator_table_rows, ["operator_family", "affected_rows", "current_status", "test_policy"])}

Core rule: `EH + Lambda` is the target baseline, not an entitlement. Any scalar, vector, boundary, torsion/nonmetricity, bulk, memory, or source-normalization operator is retained until the parent action either forbids it, makes it pure gauge/topological/Ward-owned, or maps it to a measured-safe residual.

## 5. Source-Normalization Channel Plan

{markdown_table(source_channel_table_rows, ["channel", "local_bound_rows", "source_lock", "current_status"])}

The fragile step is not the Poisson algebra itself. The fragile step is proving that the measured gravitational source is

```text
mu_obs = G_eff M_eff
```

with no species, time, range, boundary, bulk, domain, frame, or memory correction. Until then, `mu_extra` stays retained.

## 6. Local-Bound Test Matrix

{markdown_table(test_matrix_table_rows, ["test_id", "target_rows", "baseline_required", "claim_policy"])}

This deliberately scores the Mayweather version of the project: stay in the ring against GR/null baselines, keep the same pipeline honest, and only count a round when the comparison is fair and the row is not symbolic.

## 7. Runner-v4 Integration Plan

{markdown_table(integration_table_rows, ["step", "output", "guardrail"])}

## 8. Dry-Run Workflow

{markdown_table(dry_run_table_rows, ["workflow_step", "wait_policy", "expected_marker"])}

Exact command strings are stored in `runs/{run_dir.name}/results/dry_run_workflow.csv`. Future long jobs should be started from VS Code and inspected only after `DONE.txt` appears.

## 9. Row Transition Attempt

{markdown_table(transition_table_rows, ["row_id", "observable", "new_state", "theorem_credit"])}

## 10. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 11. Decision

{DECISION[0]["decision"]}

Practical read: the path is still alive, but it has narrowed into a very concrete job. To get derived local GR rather than closure-only GR, the next serious move is to run this ledger through runner-v4 and then try to derive the Ward/Bianchi exchange-owner identity that kills `source_residuals` and `mu_extra`.

## 12. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "EH_operator_retained_ledger.csv", EH_OPERATOR_RETAINED_LEDGER)
    write_csv(results_dir / "source_normalization_channel_plan.csv", SOURCE_NORMALIZATION_CHANNEL_PLAN)
    write_csv(results_dir / "local_bound_test_matrix.csv", LOCAL_BOUND_TEST_MATRIX)
    write_csv(results_dir / "runner_v4_integration_plan.csv", RUNNER_V4_INTEGRATION_PLAN)
    write_csv(results_dir / "dry_run_workflow.csv", DRY_RUN_WORKFLOW)
    write_csv(results_dir / "row_transition_attempt.csv", ROW_TRANSITION_ATTEMPT)
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
        "EH_operator_families": len(EH_OPERATOR_RETAINED_LEDGER),
        "source_normalization_channels": len(SOURCE_NORMALIZATION_CHANNEL_PLAN),
        "local_bound_tests": len(LOCAL_BOUND_TEST_MATRIX),
        "runner_v4_steps": len(RUNNER_V4_INTEGRATION_PLAN),
        "dry_run_workflow_steps": len(DRY_RUN_WORKFLOW),
        "row_transitions": len(ROW_TRANSITION_ATTEMPT),
        "theorem_zero_upgrades": 0,
        "same_frame_parent_derived": False,
        "EH_operator_selection_derived": False,
        "source_normalization_parent_derived": False,
        "real_external_data_loaded": False,
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, source_rows, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 425 EH operator retained ledger and source-normalization test-plan artifacts."
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

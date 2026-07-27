from __future__ import annotations

import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RUNS = ROOT / "runs"

DOC_PATH = ROOT / "586-Y5-R10-Vdef-owner-action-sketch-or-edge-runner-numeric-priors.md"
RUNNER = ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py"

PRIOR_585_DOC = ROOT / "585-Y5-R10-edge-alpha-runner-inputs-or-Vdef-owner-repair.md"
PRIOR_585_VALIDATION = RESIDUALS / "P8_Y5_BRR545_585_VALIDATION.csv"
PRIOR_585_SUMMARY = RESIDUALS / "P8_Y5_R10_585_NONCLAIM_SUMMARY.csv"
PRIOR_585_VDEF = RESIDUALS / "P8_Y5_R10_585_VDEF_OWNER_REPAIR_PASS.csv"
PRIOR_585_BLOCKERS = RESIDUALS / "P8_Y5_R10_585_EDGE_CLAIM_BLOCKER_LEDGER.csv"
PRIOR_585_SMOKE_CURVE = RESIDUALS / "R10_alpha_lambda_curve_MTS_edge_residual_smoke.csv"
EDGE_LAW_584 = RESIDUALS / "P8_Y5_R10_584_EDGE_ENVELOPE_LAW.csv"
PRESSURE_584 = RESIDUALS / "P8_Y5_R10_584_EDGE_PRESSURE_MATRIX.csv"
REVIEW_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_586_SOURCE_REGISTER.csv"
VDEF_ACTION_SKETCH_PATH = RESIDUALS / "P8_Y5_R10_586_VDEF_ACTION_SKETCH.csv"
CONDITIONAL_THEOREM_PATH = RESIDUALS / "P8_Y5_R10_586_CONDITIONAL_NO_POLE_THEOREM.csv"
MOMENTUM_MAP_TEST_PATH = RESIDUALS / "P8_Y5_R10_586_MOMENTUM_MAP_OWNER_TEST.csv"
BOUNDARY_TEST_PATH = RESIDUALS / "P8_Y5_R10_586_BOUNDARY_EXACTNESS_TEST.csv"
EDGE_PRIOR_GRID_PATH = RESIDUALS / "P8_Y5_R10_586_EDGE_NUMERIC_PRIOR_GRID.csv"
RUNNER_PRIOR_GRID_PATH = RESIDUALS / "R10_alpha_lambda_curve_MTS_edge_prior_grid_nonclaim.csv"
RUNNER_STATUS_PATH = RESIDUALS / "P8_Y5_R10_586_EDGE_PRIOR_RUNNER_STATUS.csv"
OWNER_DECISION_PATH = RESIDUALS / "P8_Y5_R10_586_OWNER_OR_PRIOR_DECISION.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_586_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_586_ROUTE_UPDATE.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_586_VALIDATION.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_586_NONCLAIM_SUMMARY.csv"

STATUS = "Y5_R10_Vdef_affine_owner_contract_found_but_not_parent_sourced_edge_prior_grid_written_nonclaim"
CLAIM_CEILING = "conditional_action_contract_and_numeric_prior_diagnostics_only_no_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "587-Y5-R10-affine-Vdef-parent-source-map-or-edge-prior-tightening.md"

MTS_REQUIRED_COLUMNS = [
    "model_id",
    "branch_id",
    "curve_id",
    "lambda_value",
    "lambda_units",
    "alpha_predicted",
    "alpha_bound",
    "alpha_bound_source",
    "force_law_form",
    "derivation_status",
    "formula_reference",
    "source_file",
    "assumptions",
    "valid_for_claim",
    "notes",
]

SOURCE_FILES = [
    ("585-Y5-R10-edge-alpha-runner-inputs-or-Vdef-owner-repair.md", "immediate Vdef/edge-runner handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_585_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_585_NONCLAIM_SUMMARY.csv", "prior nonclaim summary"),
    ("source-intake/mts_residuals/P8_Y5_R10_585_VDEF_OWNER_REPAIR_PASS.csv", "open Vdef repair ledger"),
    ("source-intake/mts_residuals/P8_Y5_R10_585_EDGE_CLAIM_BLOCKER_LEDGER.csv", "edge claim blockers"),
    ("source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_edge_residual_smoke.csv", "prior runner-shaped smoke curve"),
    ("source-intake/mts_residuals/P8_Y5_R10_584_EDGE_ENVELOPE_LAW.csv", "edge alpha envelope law"),
    ("source-intake/mts_residuals/P8_Y5_R10_584_EDGE_PRESSURE_MATRIX.csv", "private review-candidate pressure matrix"),
    ("source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv", "private review-candidate bound curve"),
    ("scripts/R10_alpha_lambda_bound_prediction_runner.py", "existing R10 comparator"),
    ("scripts/Y5_R10_Vdef_owner_action_sketch_or_edge_runner_numeric_priors.py", "this checkpoint generator"),
]

PRIOR_PRODUCTS = [1.0, 0.1, 0.01, 0.001, 0.0001]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, Any]], columns: list[str], limit: int | None = None) -> str:
    shown = rows if limit is None else rows[:limit]
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in shown:
        values: list[str] = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", "<br>").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    if limit is not None and len(rows) > limit:
        lines.append("| " + " | ".join(["..."] * len(columns)) + " |")
    return "\n".join(lines)


def source_register() -> list[dict[str, Any]]:
    return [
        {"source_file": source_file, "exists": str((ROOT / source_file).exists()), "role": role}
        for source_file, role in SOURCE_FILES
    ]


def make_vdef_action_sketch() -> list[dict[str, Any]]:
    return [
        {
            "sketch_id": "VAS586_0_generic_nonlinear_Vdef",
            "action_block": "S_def=int sqrt(-g) V_def(Y,Z), Z_{mu nu}=nabla_mu X_nu-A_{mu nu}[Y]",
            "variation_result": "P^{mu nu}=partial V_def/partial Z_{mu nu}; delta_X S gives C_X^nu=-nabla_mu P^{mu nu}+boundary",
            "what_it_derives": "P-owner only",
            "no_pole_condition": "fails unless Hessian partial^2 V_def/partial Z partial Z vanishes or X is quotient before variation",
            "current_verdict": "generic_Vdef_creates_X_Green_function_not_no_pole",
            "valid_for_claim": "false",
        },
        {
            "sketch_id": "VAS586_1_affine_Vdef_zero_Hessian",
            "action_block": "S_X=int sqrt(-g)[P^{mu nu}[Y](nabla_mu X_nu-A_{mu nu}[Y])+X_nu J_eff^nu[Y]]+S_boundary",
            "variation_result": "delta_X S=int sqrt(-g)(-nabla_mu P^{mu nu}+J_eff^nu)delta X_nu+int_boundary n_mu P^{mu nu}delta X_nu",
            "what_it_derives": "C_X^nu and B_X^nu from one action block",
            "no_pole_condition": "partial^2 V_def/partial Z partial Z=0 exactly; X is a Lagrange-multiplier/gauge coordinate, not a Yukawa field",
            "current_verdict": "conditional_mechanism_found_but_P_J_A_not_parent_sourced",
            "valid_for_claim": "false",
        },
        {
            "sketch_id": "VAS586_2_first_order_constraint_form",
            "action_block": "S_X=int sqrt(-g)[Pi^{mu nu}(nabla_mu X_nu-A_{mu nu}[Y])+X_nu J_eff^nu[Y]]",
            "variation_result": "delta_Pi imposes nabla_mu X_nu=A_{mu nu}[Y]; delta_X imposes -nabla_mu Pi^{mu nu}+J_eff^nu=0",
            "what_it_derives": "rank-zero/no kinetic X sector if no Pi^2 or derivative-Pi term is added",
            "no_pole_condition": "forbid quadratic Pi elimination terms that would regenerate (nabla X)^2",
            "current_verdict": "viable_topological_constraint_skeleton_not_mapped_to_MTS_parent_fields",
            "valid_for_claim": "false",
        },
        {
            "sketch_id": "VAS586_3_quotient_momentum_map_form",
            "action_block": "S_parent[Y] with vertical symmetry delta_epsilon Y=v_epsilon[Y] and no independent X in configuration space",
            "variation_result": "i_{v_epsilon} Omega_Y=delta G[epsilon], G[epsilon]=int_Sigma epsilon_nu C_X^nu+Q_boundary[epsilon]",
            "what_it_derives": "C_X as momentum-map constraint rather than physical field equation",
            "no_pole_condition": "matter and bulk actions factor through quotient; allowed epsilon are proper or have zero charge",
            "current_verdict": "best_no_pole_language_but_requires_parent_Omega_Y_and_v_epsilon",
            "valid_for_claim": "false",
        },
        {
            "sketch_id": "VAS586_4_matter_pullback_clause",
            "action_block": "S_matter[hat_g(Y),psi_m] with no hat_g(Y,X) dependence",
            "variation_result": "delta_X S_matter=0 only if the matter metric factors through the quotient map q:Y->Y/X",
            "what_it_derives": "qbar_XT=0 if quotient coupling is parent-owned",
            "no_pole_condition": "universal matter coupling must be X-blind, not merely tuned for one source",
            "current_verdict": "not_derived_from_current_corpus",
            "valid_for_claim": "false",
        },
        {
            "sketch_id": "VAS586_5_boundary_silence_clause",
            "action_block": "S_boundary chosen so n_mu P^{mu nu}delta X_nu+delta S_boundary=exact_or_zero on allowed boundary variations",
            "variation_result": "Q_edge[epsilon]=int_boundary epsilon_nu(n_mu P^{mu nu}+B_ct^nu)",
            "what_it_derives": "edge alpha zero only if Q_edge=0 as charge, not as a numerical hope",
            "no_pole_condition": "B_X exact/pure gauge or epsilon compact-supported/proper at the relevant boundary",
            "current_verdict": "not_derived; edge branch remains live fallback",
            "valid_for_claim": "false",
        },
    ]


def make_conditional_theorem() -> list[dict[str, Any]]:
    return [
        {
            "condition_id": "CNT586_0_affine_defect_block",
            "required_statement": "V_def is affine in Z=nabla X-A[Y], so H_ZZ=partial^2 V_def/partial Z partial Z=0 exactly",
            "why_needed": "nonzero H_ZZ supplies an invertible kinetic/Hessian block and creates a physical X Green function",
            "current_status": "contract_written_not_parent_sourced",
            "if_satisfied": "K_X=0 in the local fifth-force runner",
            "valid_for_claim": "false",
        },
        {
            "condition_id": "CNT586_1_Noether_current_owner",
            "required_statement": "J_eff^nu[Y] and P^{mu nu}[Y] are coefficients of one vertical Noether identity",
            "why_needed": "prevents declaring -nabla P+J by hand",
            "current_status": "not_derived",
            "if_satisfied": "C_X^nu is an identity/constraint rather than a fitted source equation",
            "valid_for_claim": "false",
        },
        {
            "condition_id": "CNT586_2_matter_quotient",
            "required_statement": "matter couples only to quotient fields q(Y), with no X-dependence in the matter metric or clocks",
            "why_needed": "kills the test-body charge qbar_XT without source-by-source tuning",
            "current_status": "not_derived",
            "if_satisfied": "qbar_XT=0 for universal matter",
            "valid_for_claim": "false",
        },
        {
            "condition_id": "CNT586_3_boundary_silence",
            "required_statement": "Q_boundary[epsilon]=0 and boundary cocycle K_boundary[epsilon,eta]=0 for allowed local transformations",
            "why_needed": "bulk no-pole is not enough if the edge carries charge",
            "current_status": "not_derived",
            "if_satisfied": "Qbar_edge_XH(lambda)=0",
            "valid_for_claim": "false",
        },
        {
            "condition_id": "CNT586_4_no_double_count",
            "required_statement": "Q_X=Q_bulk+Q_edge is an orthogonal split, with the quotient branch not counted again as edge Yukawa response",
            "why_needed": "prevents hiding a residual source in the boundary term",
            "current_status": "not_derived",
            "if_satisfied": "R10 alpha row can be either zero-theorem or finite-edge, not both",
            "valid_for_claim": "false",
        },
    ]


def make_momentum_map_test() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "MMT586_0_symplectic_potential",
            "required_object": "theta_Y(delta Y) from delta L_parent=E_Y delta Y+d theta_Y",
            "pass_condition": "Omega_Y=delta theta_Y exists and is nondegenerate only on quotient-reduced directions",
            "current_status": "missing_from_corpus",
            "owner_verdict": "blocked",
        },
        {
            "test_id": "MMT586_1_vertical_generator",
            "required_object": "v_epsilon[Y] generating the X/defect redundancy",
            "pass_condition": "i_{v_epsilon}Omega_Y=delta G[epsilon] with G differentiable",
            "current_status": "missing_from_corpus",
            "owner_verdict": "blocked",
        },
        {
            "test_id": "MMT586_2_constraint_identity",
            "required_object": "C_X^nu=-nabla_mu P^{mu nu}+J_eff^nu",
            "pass_condition": "C_X is produced by the Noether identity, not inserted after the fact",
            "current_status": "action_contract_written_only",
            "owner_verdict": "partial",
        },
        {
            "test_id": "MMT586_3_algebra_closure",
            "required_object": "{G[epsilon],G[eta]}=G[[epsilon,eta]]+K_boundary[epsilon,eta]",
            "pass_condition": "K_boundary=0 for allowed transformations",
            "current_status": "not_derived",
            "owner_verdict": "blocked",
        },
        {
            "test_id": "MMT586_4_matter_factorization",
            "required_object": "hat_g=q^* hat_g_red or equivalent quotient matter map",
            "pass_condition": "delta_X S_matter=0 universally",
            "current_status": "not_derived",
            "owner_verdict": "blocked",
        },
    ]


def make_boundary_test() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "BET586_0_compact_support",
            "boundary_condition": "epsilon_nu=0 on the relevant boundary",
            "charge_result": "Q_edge=0 by allowed-variation definition",
            "physics_cost": "only proves proper-gauge local silence, not asymptotic/improper charge silence",
            "current_status": "available_as_closure_only",
            "valid_for_claim": "false",
        },
        {
            "case_id": "BET586_1_exact_boundary_form",
            "boundary_condition": "n_mu P^{mu nu}epsilon_nu=d_boundary b_X",
            "charge_result": "Q_edge=int_boundary d b_X=0 on closed boundary",
            "physics_cost": "requires actual b_X from parent fields",
            "current_status": "not_derived",
            "valid_for_claim": "false",
        },
        {
            "case_id": "BET586_2_counterterm_cancellation",
            "boundary_condition": "B_ct^nu=-n_mu P^{mu nu} from a local covariant S_boundary",
            "charge_result": "differentiable generator with zero edge charge",
            "physics_cost": "counterterm must not remove physical ADM/Hilbert mass charge",
            "current_status": "not_derived",
            "valid_for_claim": "false",
        },
        {
            "case_id": "BET586_3_improper_edge_mode",
            "boundary_condition": "epsilon nonzero and B_X not exact",
            "charge_result": "finite Q_edge remains; edge-alpha branch needed",
            "physics_cost": "must supply lambda_edge,K_edge,Qbar_edge_XH,qbar_XT numerically/source-backed",
            "current_status": "fallback_live",
            "valid_for_claim": "false",
        },
    ]


def make_edge_prior_grid(pressure_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for pressure in pressure_rows:
        alpha_bound = float(pressure["review_candidate_alpha_bound"])
        lambda_m = float(pressure["lambda_m"])
        lambda_um = float(pressure["lambda_um"])
        for product in PRIOR_PRODUCTS:
            ratio = abs(product) / alpha_bound if alpha_bound > 0 else float("inf")
            rows.append(
                {
                    "prior_id": f"EPG586_{len(rows)}",
                    "lambda_m": f"{lambda_m:.9g}",
                    "lambda_um": f"{lambda_um:.9g}",
                    "review_candidate_alpha_bound": f"{alpha_bound:.12g}",
                    "edge_product_prior": f"{product:.12g}",
                    "alpha_edge_assuming_unit_kernel": f"{product:.12g}",
                    "ratio_to_review_bound": f"{ratio:.12g}",
                    "private_diagnostic_pass": str(ratio <= 1.0).lower(),
                    "pressure_band": pressure["pressure_band"],
                    "derivation_status": "numeric_prior_grid_not_source_backed",
                    "valid_for_claim": "false",
                    "notes": "diagnostic only: alpha_edge=K_edge*Qbar_edge_XH*qbar_XT prior inserted without parent coefficients",
                }
            )
    return rows


def make_runner_prior_grid(edge_prior_grid: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in edge_prior_grid:
        rows.append(
            {
                "model_id": "MTS_edge_prior_grid_nonclaim",
                "branch_id": "edge_numeric_prior_grid",
                "curve_id": "R10_alpha_lambda_curve_MTS_edge_prior_grid_nonclaim",
                "lambda_value": row["lambda_m"],
                "lambda_units": "m",
                "alpha_predicted": row["alpha_edge_assuming_unit_kernel"],
                "alpha_bound": row["review_candidate_alpha_bound"],
                "alpha_bound_source": "source-intake/mts_residuals/P8_Y5_R10_584_EDGE_PRESSURE_MATRIX.csv::private_review_candidate",
                "force_law_form": "edge_alpha_envelope",
                "derivation_status": "numeric_prior_grid_not_source_backed",
                "formula_reference": "586-Y5-R10-Vdef-owner-action-sketch-or-edge-runner-numeric-priors.md",
                "source_file": "source-intake/mts_residuals/P8_Y5_R10_586_EDGE_NUMERIC_PRIOR_GRID.csv",
                "assumptions": "alpha_edge=K_edge*Qbar_edge_XH*qbar_XT; unit kernel; review-candidate bound only",
                "valid_for_claim": "false",
                "notes": f"private_diagnostic_pass={row['private_diagnostic_pass']}; ratio_to_review_bound={row['ratio_to_review_bound']}",
            }
        )
    return rows


def run_runner(output_dir: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(RUNNER),
            "--mts-curve",
            str(RUNNER_PRIOR_GRID_PATH),
            "--bound-curve",
            str(REVIEW_CURVE),
            "--output-dir",
            str(output_dir),
        ],
        cwd=str(ROOT),
        check=True,
        capture_output=True,
        text=True,
    )
    status_path = output_dir / "R10_runner_status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    status["stdout"] = completed.stdout.strip()
    status["stderr"] = completed.stderr.strip()
    return status


def make_runner_status(run_root: Path, runner_status: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "R10_EDGE_PRIOR_GRID_REVIEW_CANDIDATE",
            "bound_curve": rel(REVIEW_CURVE),
            "output_dir": rel(run_root / "review_candidate_prior_grid" / "results"),
            "mts_rows": runner_status.get("mts_rows", ""),
            "valid_mts_rows": runner_status.get("valid_mts_rows", ""),
            "bound_rows": runner_status.get("bound_rows", ""),
            "valid_bound_rows": runner_status.get("valid_bound_rows", ""),
            "comparison_rows": runner_status.get("comparison_rows", ""),
            "passed_rows": runner_status.get("passed_rows", ""),
            "blocked_or_failed_rows": runner_status.get("blocked_or_failed_rows", ""),
            "claim_allowed": str(runner_status.get("claim_allowed", "")).lower(),
        }
    ]


def make_owner_decision(runner_status_rows: list[dict[str, Any]], edge_grid: list[dict[str, Any]]) -> list[dict[str, Any]]:
    passes = sum(1 for row in edge_grid if row["private_diagnostic_pass"] == "true")
    fails = sum(1 for row in edge_grid if row["private_diagnostic_pass"] == "false")
    claim_allowed = runner_status_rows[0]["claim_allowed"]
    return [
        {
            "decision_id": "OOD586_0_generic_Vdef_rejected",
            "decision": "generic nonlinear V_def is not the local-GR repair",
            "meaning": "unless the Z Hessian is exactly zero, X has a physical response block",
            "status": "reject_as_no_pole_proof",
            "next_action": NEXT_TARGET,
        },
        {
            "decision_id": "OOD586_1_affine_contract_promising",
            "decision": "affine/first-order V_def gives a clean conditional no-pole mechanism",
            "meaning": "X can be a Lagrange-multiplier or quotient coordinate if P,J,A,boundary are parent-owned",
            "status": "conditional_contract_not_claim",
            "next_action": NEXT_TARGET,
        },
        {
            "decision_id": "OOD586_2_edge_priors_written",
            "decision": "numeric edge-prior grid written as fallback pressure test",
            "meaning": f"{passes} private diagnostic rows pass and {fails} fail against the review-candidate pressure matrix, all nonclaim",
            "status": "fallback_ready_nonclaim",
            "next_action": NEXT_TARGET,
        },
        {
            "decision_id": "OOD586_3_runner_blocks_claim",
            "decision": "R10 runner still blocks the prior grid",
            "meaning": f"claim_allowed={claim_allowed} because rows remain valid_for_claim=false and review curve remains private/nonclaim",
            "status": "guardrail_pass",
            "next_action": NEXT_TARGET,
        },
    ]


def make_decision() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D586_0_affine_owner_contract",
            "decision": "the derivable route now has an exact contract: V_def must be affine in Z or topological/quotient",
            "claim_status": "not_claimed",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D586_1_nonlinear_Vdef_fails",
            "decision": "a generic V_def potential cannot be used for local silence because it creates a physical X Hessian/pole",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D586_2_edge_prior_grid",
            "decision": "fallback edge numeric-prior grid is executable but deliberately invalid for claim",
            "claim_status": "nonclaim_diagnostic",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU586_0_allowed",
            "allowed_after_586": "try to map P^{mu nu}[Y], J_eff^nu[Y], and A_{mu nu}[Y] to actual MTS parent variables",
            "forbidden_after_586": "use a generic nonlinear V_def as a no-pole proof",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU586_1_allowed",
            "allowed_after_586": "treat affine V_def as a conditional theorem skeleton",
            "forbidden_after_586": "promote K_X=0 without quotient matter coupling and boundary silence",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU586_2_allowed",
            "allowed_after_586": "use edge prior grid to see how small the product must be if owner repair fails",
            "forbidden_after_586": "set prior-grid rows valid_for_claim=true or copy them into live claim files",
            "next_action": NEXT_TARGET,
        },
    ]


def make_summary(owner_decision: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "summary_id": "S586_0",
            "claim_allowed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "best_private_read": "A useful theorem-repair narrowing: local silence requires affine/topological/quotient Vdef, not a generic potential.",
            "next_target": NEXT_TARGET,
        },
        {
            "summary_id": "S586_1",
            "claim_allowed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "best_private_read": owner_decision[1]["meaning"],
            "next_target": NEXT_TARGET,
        },
    ]


def make_validation(
    sources: list[dict[str, Any]],
    vdef_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    momentum_rows: list[dict[str, Any]],
    boundary_rows: list[dict[str, Any]],
    edge_grid: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    runner_status_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    prior_585_validation_rows = read_csv(PRIOR_585_VALIDATION)
    prior_failures = [
        row for row in prior_585_validation_rows if str(row.get("result", "")).strip().lower() != "pass"
    ]
    source_missing = [row["source_file"] for row in sources if row["exists"] != "True"]
    vdef_claims = [row for row in vdef_rows if row["valid_for_claim"] == "true"]
    theorem_claims = [row for row in theorem_rows if row["valid_for_claim"] == "true"]
    boundary_claims = [row for row in boundary_rows if row["valid_for_claim"] == "true"]
    edge_claims = [row for row in edge_grid if row["valid_for_claim"] == "true"]
    runner_claims = [row for row in runner_rows if row["valid_for_claim"] == "true"]
    diagnostic_passes = [row for row in edge_grid if row["private_diagnostic_pass"] == "true"]
    diagnostic_fails = [row for row in edge_grid if row["private_diagnostic_pass"] == "false"]
    generic_vdef_rejected = any(
        row["sketch_id"] == "VAS586_0_generic_nonlinear_Vdef"
        and "not_no_pole" in row["current_verdict"]
        for row in vdef_rows
    )
    affine_contract_present = any(row["sketch_id"] == "VAS586_1_affine_Vdef_zero_Hessian" for row in vdef_rows)
    runner_claim_allowed = runner_status_rows[0]["claim_allowed"] == "true"
    return [
        {
            "check_id": "V586_0_source_paths_exist",
            "result": "pass" if not source_missing else "fail",
            "detail": f"missing={len(source_missing)}",
        },
        {
            "check_id": "V586_1_prior_585_clean",
            "result": "pass" if prior_585_validation_rows and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_585_validation_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V586_2_generic_Vdef_rejected",
            "result": "pass" if generic_vdef_rejected else "fail",
            "detail": "nonlinear Hessian route cannot be a no-pole proof",
        },
        {
            "check_id": "V586_3_affine_contract_present_not_promoted",
            "result": "pass" if affine_contract_present and not vdef_claims and not theorem_claims else "fail",
            "detail": f"vdef_rows={len(vdef_rows)};theorem_rows={len(theorem_rows)};claim_rows={len(vdef_claims)+len(theorem_claims)}",
        },
        {
            "check_id": "V586_4_momentum_boundary_still_blocked",
            "result": "pass"
            if any(row["owner_verdict"] == "blocked" for row in momentum_rows) and not boundary_claims
            else "fail",
            "detail": f"momentum_rows={len(momentum_rows)};boundary_claim_rows={len(boundary_claims)}",
        },
        {
            "check_id": "V586_5_edge_prior_grid_nonclaim_with_pressure",
            "result": "pass" if edge_grid and diagnostic_passes and diagnostic_fails and not edge_claims else "fail",
            "detail": f"grid_rows={len(edge_grid)};diagnostic_passes={len(diagnostic_passes)};diagnostic_fails={len(diagnostic_fails)};claim_rows={len(edge_claims)}",
        },
        {
            "check_id": "V586_6_runner_prior_grid_schema_nonclaim",
            "result": "pass"
            if runner_rows
            and set(MTS_REQUIRED_COLUMNS).issubset(runner_rows[0].keys())
            and not runner_claims
            else "fail",
            "detail": f"runner_rows={len(runner_rows)};claim_rows={len(runner_claims)}",
        },
        {
            "check_id": "V586_7_existing_runner_blocks_claim",
            "result": "pass" if not runner_claim_allowed else "fail",
            "detail": f"claim_allowed={runner_status_rows[0]['claim_allowed']};valid_mts_rows={runner_status_rows[0]['valid_mts_rows']}",
        },
        {
            "check_id": "V586_8_no_R10_or_local_GR_claim",
            "result": "pass",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    run_root: Path,
    sources: list[dict[str, Any]],
    vdef_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    momentum_rows: list[dict[str, Any]],
    boundary_rows: list[dict[str, Any]],
    edge_grid: list[dict[str, Any]],
    runner_status_rows: list[dict[str, Any]],
    owner_decision: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    text = f"""# 586 Y5 R10 Vdef owner action sketch or edge-runner numeric priors

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- The derivation attempt did produce a useful contract: a local-silent `V_def` cannot be generic. It must be affine/topological/quotient so the `Z` Hessian is exactly zero.
- The affine block derives `C_X^nu=-nabla_mu P^{{mu nu}}+J_eff^nu` and the boundary charge from one action variation, but it does not yet source `P`, `J_eff`, `A`, the quotient matter map, or the boundary counterterm from the MTS parent variables.
- Therefore this checkpoint is progress but not a local-GR/R10 pass.
- A nonclaim numeric edge-prior grid is now written so the fallback branch has a pressure dial if the owner theorem fails.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Vdef Action Sketch
{markdown_table(vdef_rows, ["sketch_id", "action_block", "variation_result", "what_it_derives", "no_pole_condition", "current_verdict", "valid_for_claim"])}

## Conditional No-Pole Theorem Contract
{markdown_table(theorem_rows, ["condition_id", "required_statement", "why_needed", "current_status", "if_satisfied", "valid_for_claim"])}

## Momentum-Map Owner Test
{markdown_table(momentum_rows, ["test_id", "required_object", "pass_condition", "current_status", "owner_verdict"])}

## Boundary Exactness Test
{markdown_table(boundary_rows, ["case_id", "boundary_condition", "charge_result", "physics_cost", "current_status", "valid_for_claim"])}

## Edge Numeric-Prior Grid
Full grid written to `{rel(EDGE_PRIOR_GRID_PATH)}`. Preview:

{markdown_table(edge_grid, ["prior_id", "lambda_um", "review_candidate_alpha_bound", "edge_product_prior", "ratio_to_review_bound", "private_diagnostic_pass", "pressure_band", "valid_for_claim"], limit=18)}

## Runner Status
{markdown_table(runner_status_rows, ["runner_id", "bound_curve", "output_dir", "mts_rows", "valid_mts_rows", "bound_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "claim_allowed"])}

## Owner Or Prior Decision
{markdown_table(owner_decision, ["decision_id", "decision", "meaning", "status", "next_action"])}

## Decision
{markdown_table(decisions, ["decision_id", "decision", "claim_status", "next_target"])}

## Route Update
{markdown_table(route_rows, ["route_id", "allowed_after_586", "forbidden_after_586", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
The good news is that the local branch did not collapse into pure numerology here: the derivation tells us something sharp. The bad news is also sharp: a generic `V_def` potential is not allowed if we want derived local silence. The next move is to map the affine/topological ingredients (`P`, `J_eff`, `A`, quotient matter coupling, and boundary silence) onto actual MTS parent fields; if that fails, the edge-prior grid tells us how tiny the residual product must be.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_root = RUNS / f"{stamp}-Y5-R10-Vdef-owner-action-sketch-or-edge-runner-numeric-priors"
    runner_output_dir = run_root / "review_candidate_prior_grid" / "results"
    run_root.mkdir(parents=True, exist_ok=True)

    sources = source_register()
    pressure_rows = read_csv(PRESSURE_584)
    vdef_rows = make_vdef_action_sketch()
    theorem_rows = make_conditional_theorem()
    momentum_rows = make_momentum_map_test()
    boundary_rows = make_boundary_test()
    edge_grid = make_edge_prior_grid(pressure_rows)
    runner_grid = make_runner_prior_grid(edge_grid)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(
        VDEF_ACTION_SKETCH_PATH,
        vdef_rows,
        ["sketch_id", "action_block", "variation_result", "what_it_derives", "no_pole_condition", "current_verdict", "valid_for_claim"],
    )
    write_csv(
        CONDITIONAL_THEOREM_PATH,
        theorem_rows,
        ["condition_id", "required_statement", "why_needed", "current_status", "if_satisfied", "valid_for_claim"],
    )
    write_csv(
        MOMENTUM_MAP_TEST_PATH,
        momentum_rows,
        ["test_id", "required_object", "pass_condition", "current_status", "owner_verdict"],
    )
    write_csv(
        BOUNDARY_TEST_PATH,
        boundary_rows,
        ["case_id", "boundary_condition", "charge_result", "physics_cost", "current_status", "valid_for_claim"],
    )
    write_csv(
        EDGE_PRIOR_GRID_PATH,
        edge_grid,
        [
            "prior_id",
            "lambda_m",
            "lambda_um",
            "review_candidate_alpha_bound",
            "edge_product_prior",
            "alpha_edge_assuming_unit_kernel",
            "ratio_to_review_bound",
            "private_diagnostic_pass",
            "pressure_band",
            "derivation_status",
            "valid_for_claim",
            "notes",
        ],
    )
    write_csv(RUNNER_PRIOR_GRID_PATH, runner_grid, MTS_REQUIRED_COLUMNS)

    runner_status = run_runner(runner_output_dir)
    runner_status_rows = make_runner_status(run_root, runner_status)
    write_csv(
        RUNNER_STATUS_PATH,
        runner_status_rows,
        [
            "runner_id",
            "bound_curve",
            "output_dir",
            "mts_rows",
            "valid_mts_rows",
            "bound_rows",
            "valid_bound_rows",
            "comparison_rows",
            "passed_rows",
            "blocked_or_failed_rows",
            "claim_allowed",
        ],
    )

    owner_decision = make_owner_decision(runner_status_rows, edge_grid)
    decisions = make_decision()
    route_rows = make_route_update()
    summary_rows = make_summary(owner_decision)
    validation_rows = make_validation(
        sources,
        vdef_rows,
        theorem_rows,
        momentum_rows,
        boundary_rows,
        edge_grid,
        runner_grid,
        runner_status_rows,
    )

    write_csv(
        OWNER_DECISION_PATH,
        owner_decision,
        ["decision_id", "decision", "meaning", "status", "next_action"],
    )
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "claim_status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_rows, ["route_id", "allowed_after_586", "forbidden_after_586", "next_action"])
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        ["summary_id", "claim_allowed", "R10_pass", "WEP_pass", "PPN_pass", "local_GR_pass", "best_private_read", "next_target"],
    )
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_markdown(
        generated,
        run_root,
        sources,
        vdef_rows,
        theorem_rows,
        momentum_rows,
        boundary_rows,
        edge_grid,
        runner_status_rows,
        owner_decision,
        decisions,
        route_rows,
        validation_rows,
    )

    status_payload = {
        "generated": generated,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": rel(DOC_PATH),
        "validation": rel(VALIDATION_PATH),
        "runner_claim_allowed": runner_status_rows[0]["claim_allowed"],
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    (run_root / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    (run_root / "COMPLETE.marker").write_text("complete\n", encoding="utf-8")
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()

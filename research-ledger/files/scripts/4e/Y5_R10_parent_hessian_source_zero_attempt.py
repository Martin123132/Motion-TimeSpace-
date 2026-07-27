from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import run_runner


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_R10_parent_Hessian_extraction_derived_source_zero_reduced_to_coframe_pullback_and_boundary_premises"
CLAIM_CEILING = "parent_Hessian_contract_only_no_numeric_alpha_no_R10_fifth_force_PPN_or_local_GR_pass"
NEXT_TARGET = "565-Y5-R10-coframe-pullback-zero-or-finite-alpha-coefficient.md"

DOC_PATH = Path("564-Y5-R10-parent-hessian-source-zero-attempt.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_564_SOURCE_REGISTER.csv")
HESSIAN_FORMULA_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_564_HESSIAN_EXTRACTION_FORMULA.csv")
SOURCE_ZERO_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_564_SOURCE_ZERO_THEOREM_ATTEMPT.csv")
MATTER_PULLBACK_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_564_MATTER_PULLBACK_CHARGE_MAP.csv")
PARENT_REQUIREMENTS_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_564_PARENT_ACTION_REQUIREMENTS.csv")
ALPHA_POLICY_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_564_ALPHA_ROW_POLICY.csv")
RUNNER_SUMMARY_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_564_RUNNER_SUMMARY.csv")
EVALUATOR_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_564_EVALUATOR.csv")
BLOCKER_LEDGER_PATH = Path("source-intake/mts_residuals/P8_Y5_R10_564_BLOCKER_LEDGER.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_564_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_564_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_564_ROUTE_UPDATE.csv")

PRIOR_VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_BRR545_563_VALIDATION.csv")
LIVE_MTS_CURVE_PATH = Path("source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv")
LIVE_BOUND_CURVE_PATH = Path("source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv")


SOURCE_REGISTER = [
    {
        "source_file": "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md",
        "role": "upstream real-anchor/non-claim R10 data gate",
    },
    {
        "source_file": "562-Y5-R10-ZX-lambda-mass-gap-and-bound-curve-fill-or-theorem-zero.md",
        "role": "lambda_X and K_X conditional derivation",
    },
    {
        "source_file": "561-Y5-R10-source-test-charge-and-PiM-projection-zero-or-coefficient-fill.md",
        "role": "R10 numerator factorization and zero-route failure",
    },
    {
        "source_file": "384-parent-action-first-variation-obstruction-map.md",
        "role": "observed-coframe pullback obstruction",
    },
    {
        "source_file": "382-parent-local-action-minimal-contract.md",
        "role": "minimal parent action block list and bulk-X identity contract",
    },
    {
        "source_file": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "role": "bulk-X no-hair/Yukawa fallback contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_ZX_LAMBDA_PREFACtOR_FORMULA_REGISTER.csv",
        "role": "562 formula register",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_NUMERATOR_COEFFICIENT_VECTOR.csv",
        "role": "561 numerator coefficient vector",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_ALPHA_LAW_PARENT_INPUTS.csv",
        "role": "560 parent input debt ledger",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_563_VALIDATION.csv",
        "role": "prior validation gate",
    },
    {
        "source_file": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "role": "live MTS placeholder curve retained unchanged",
    },
    {
        "source_file": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "role": "live bound placeholder file retained unchanged",
    },
    {
        "source_file": "scripts/R10_alpha_lambda_bound_prediction_runner.py",
        "role": "existing R10 runner reused as guardrail",
    },
    {
        "source_file": "scripts/Y5_R10_parent_hessian_source_zero_attempt.py",
        "role": "this checkpoint generator",
    },
]


HESSIAN_FORMULA_ROWS = [
    {
        "formula_id": "H564_0_parent_expansion",
        "object": "parent action near local branch",
        "expression": "S_parent[X]=S0+int sqrt(-g) E_X|0 deltaX + 1/2 int sqrt(-g)[H_grad^{mu nu} nabla_mu deltaX nabla_nu deltaX - H_0 deltaX^2]+...",
        "derivation_status": "exact_second_variation_definition",
        "meaning": "Z_X and M_X^2 are not free fit knobs; they are Hessian residues of the same parent action.",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "H564_1_ZX_extraction",
        "object": "kinetic/elliptic residue",
        "expression": "Z_X = (1/3) h_{mu nu} H_grad^{mu nu} in the locally isotropic static branch",
        "derivation_status": "conditional_extraction_formula_derived",
        "meaning": "positive local elliptic branch requires spatial Hessian positive: Z_X>0.",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "H564_2_MX_extraction",
        "object": "mass/Hessian curvature",
        "expression": "M_X^2 = H_0 after sign convention chosen so E_X=(-Z_X Delta + M_X^2)X-J_X",
        "derivation_status": "conditional_extraction_formula_derived",
        "meaning": "finite stable range requires M_X^2>0 in the same canonical convention as Z_X.",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "H564_3_operator",
        "object": "static Euler equation",
        "expression": "(-Z_X Delta + M_X^2)X = J_X",
        "derivation_status": "derived_from_quadratic_parent_expansion",
        "meaning": "this recovers lambda_X=sqrt(Z_X/M_X^2) only if both Hessian residues are parent-owned and positive.",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "H564_4_source_decomposition",
        "object": "physical source",
        "expression": "J_X=J_matter_pullback+J_boundary+J_projector+J_memory+J_domain+J_direct_MTS",
        "derivation_status": "derived_by_total_variation_bookkeeping",
        "meaning": "source-zero is a channelwise parent identity, not the absence of a visible matter term in one block.",
        "valid_for_claim": "false",
    },
    {
        "formula_id": "H564_5_yukawa_or_zero_fork",
        "object": "R10 fork",
        "expression": "if J_X=0 and boundary flux=0 then X=0; else X(r)=Q_X^H exp(-r/lambda_X)/(4*pi Z_X r)",
        "derivation_status": "conditional_fork_derived",
        "meaning": "the local branch is either theorem-zero or a finite alpha(lambda) residual; there is no honest third option.",
        "valid_for_claim": "false",
    },
]


SOURCE_ZERO_ROWS = [
    {
        "test_id": "SZ564_0_stationary_branch",
        "zero_target": "background source term",
        "required_identity": "E_X|0=0 on the chosen local branch",
        "attempted_derivation": "expand around an extremal local vacuum rather than arbitrary X=0",
        "result": "conditional_pass",
        "failure_mode": "if the chosen local branch is not an extremum, X has a tadpole and theorem-zero fails immediately",
        "repair": "parent action must name the branch and prove E_X|0=0",
        "valid_for_claim": "false",
    },
    {
        "test_id": "SZ564_1_positive_Hessian",
        "zero_target": "massive elliptic operator",
        "required_identity": "Z_X>0 and M_X^2>0 from parent Hessian",
        "attempted_derivation": "use second variation to define Hessian residues",
        "result": "formula_pass_value_fail",
        "failure_mode": "no explicit parent Lagrangian coefficients are available to sign or evaluate the residues",
        "repair": "supply explicit S_X or promote a parent action clause that fixes the Hessian",
        "valid_for_claim": "false",
    },
    {
        "test_id": "SZ564_2_matter_pullback_zero",
        "zero_target": "ordinary matter does not source X",
        "required_identity": "delta_X S_matter[psi,hat_g(X)] = 0 equivalently T_hat^{mu nu} partial_X hat_g_{mu nu}=0",
        "attempted_derivation": "apply the 384 first-variation chain to the X component of the observed coframe",
        "result": "fail_current_claim",
        "failure_mode": "if hat_g depends on X, ordinary matter stress generically sources X",
        "repair": "derive strict identity/selector-blind coframe with partial_X hat_g=0, or retain qbar_XT and Qbar_XH",
        "valid_for_claim": "false",
    },
    {
        "test_id": "SZ564_3_boundary_projector_zero",
        "zero_target": "no hidden exterior/boundary source",
        "required_identity": "J_boundary=J_projector=J_memory=J_domain=0 and boundary flux int dS Z_X X n.gradX=0",
        "attempted_derivation": "fold 561/380 source decomposition into the no-hair identity",
        "result": "fail_current_claim",
        "failure_mode": "boundary/projector/memory/domain pieces remain explicit retained channels",
        "repair": "derive channelwise Ward/topological zero or bounded coefficient rows",
        "valid_for_claim": "false",
    },
    {
        "test_id": "SZ564_4_nohair_identity",
        "zero_target": "X=0 in regular decaying local exterior",
        "required_identity": "int[Z_X|grad X|^2+M_X^2 X^2]=0",
        "attempted_derivation": "multiply (-Z_X Delta+M_X^2)X=0 by X and integrate",
        "result": "conditional_pass",
        "failure_mode": "identity only closes if SZ564_1 through SZ564_3 are all passed",
        "repair": "use this as certificate once the parent premises are actually signed",
        "valid_for_claim": "false",
    },
    {
        "test_id": "SZ564_5_verdict",
        "zero_target": "R10 theorem-zero",
        "required_identity": "positive Hessian plus zero matter pullback plus zero boundary/projector/memory/domain source",
        "attempted_derivation": "combine the Hessian extraction with source decomposition",
        "result": "not_derived_current_claim",
        "failure_mode": "coframe pullback and hidden source channels are not zeroed by the current corpus",
        "repair": "next attack partial_X hat_g=0 or fill finite alpha(lambda) coefficients",
        "valid_for_claim": "false",
    },
]


MATTER_PULLBACK_ROWS = [
    {
        "map_id": "MP564_0_particle_action",
        "object": "test body charge",
        "expression": "S_T=-m_T int d tau_hat; q_X^T=-delta S_T/dX = (m_T/2) u_hat^mu u_hat^nu partial_X hat_g_{mu nu} in point-particle normalization up to sign convention",
        "zero_condition": "partial_X hat_g_{mu nu}=0 along ordinary matter readout or pure gauge contraction with T_hat",
        "if_nonzero": "qbar_XT=q_X^T/m_T becomes the R10 test-charge coefficient",
        "status": "derived_expression_not_zeroed",
        "valid_for_claim": "false",
    },
    {
        "map_id": "MP564_1_continuum_source",
        "object": "source charge density",
        "expression": "J_matter_pullback=(1/2) sqrt(-hat_g) T_hat^{mu nu} partial_X hat_g_{mu nu}",
        "zero_condition": "observed coframe/metric is X-blind or a Ward identity cancels this full stress contraction",
        "if_nonzero": "Q_X^H(lambda)=int_H J_matter_pullback F_lambda + hidden source channels",
        "status": "derived_expression_not_zeroed",
        "valid_for_claim": "false",
    },
    {
        "map_id": "MP564_2_nonrel_limit",
        "object": "Newtonian test charge readout",
        "expression": "qbar_XT approximately -1/2 partial_X hat_g_00 for slow bodies after sign convention is fixed",
        "zero_condition": "partial_X hat_g_00=0 in the local ordinary-matter frame",
        "if_nonzero": "finite-range fifth-force alpha is generically active even if universal and WEP-safe",
        "status": "derived_expression_not_zeroed",
        "valid_for_claim": "false",
    },
    {
        "map_id": "MP564_3_universal_nonzero",
        "object": "universal matter coupling",
        "expression": "qbar_XA=qbar_XB=constant does not imply alpha_X=0",
        "zero_condition": "constant coupling must also be lambda/r/time/species independent and infinite-range calibration-safe, or exactly zero",
        "if_nonzero": "WEP can survive while R10 fifth-force bounds still apply",
        "status": "guardrail_retained",
        "valid_for_claim": "false",
    },
]


PARENT_REQUIREMENT_ROWS = [
    {
        "requirement_id": "PR564_0_explicit_SX",
        "needed_object": "Z_X and M_X^2",
        "required_parent_clause": "an explicit quadratic X block or constraint block in S_parent",
        "acceptable_success": "Z_X>0 and M_X^2>0, or X is a nonpropagating constraint with no finite Yukawa mode",
        "current_status": "not_supplied",
        "next_action": "derive or write the parent X block",
    },
    {
        "requirement_id": "PR564_1_X_blind_observed_coframe",
        "needed_object": "qbar_XT=0 and J_matter_pullback=0",
        "required_parent_clause": "partial_X hat_g_{mu nu}=0 for ordinary local matter, or exact Ward-owned cancellation",
        "acceptable_success": "matter pullback source vanishes channelwise",
        "current_status": "not_supplied",
        "next_action": "attack coframe pullback zero in 565",
    },
    {
        "requirement_id": "PR564_2_hidden_source_zero",
        "needed_object": "Q_boundary, Q_projector, Q_memory, Q_domain",
        "required_parent_clause": "topological/Ward no-flux identity or source-measure orthogonality",
        "acceptable_success": "all hidden source channels vanish, not cancel numerically",
        "current_status": "not_supplied",
        "next_action": "keep source channels as coefficient rows if no theorem appears",
    },
    {
        "requirement_id": "PR564_3_same_frame_alpha",
        "needed_object": "dimensionless alpha_X(lambda)",
        "required_parent_clause": "same-frame measured G_obs, M_H, m_T normalization with Qbar_XH and qbar_XT",
        "acceptable_success": "numeric/source-backed alpha row or theorem-zero certificate",
        "current_status": "not_supplied",
        "next_action": "do not promote R10 until coefficients or theorem-zero are real",
    },
]


ALPHA_POLICY_ROWS = [
    {
        "policy_id": "AP564_0_if_coframe_X_blind",
        "case": "partial_X hat_g=0 and hidden sources zero",
        "alpha_policy": "theorem-zero candidate",
        "runner_action": "write certificate before setting alpha=0",
        "claim_status": "blocked_until_parent_certificate",
    },
    {
        "policy_id": "AP564_1_if_coframe_X_charged",
        "case": "partial_X hat_g nonzero",
        "alpha_policy": "finite Yukawa residual",
        "runner_action": "fill qbar_XT, Qbar_XH, Z_X, lambda_X and compare with real bound curve",
        "claim_status": "blocked_until_numeric_coefficients_and_bound_curve",
    },
    {
        "policy_id": "AP564_2_if_X_constraint",
        "case": "no quadratic Hessian, X is multiplier/constraint",
        "alpha_policy": "no finite lambda_X row unless constraint leaves a residual kernel",
        "runner_action": "prove constraint removes physical source or retain closure residual",
        "claim_status": "blocked_until_constraint_algebra_signed",
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    columns = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in SOURCE_REGISTER:
        source_file = row["source_file"]
        rows.append(
            {
                "source_file": source_file,
                "role": row["role"],
                "exists": str((ROOT / source_file).exists()),
            }
        )
    return rows


def build_runner_summary(result: dict[str, Any]) -> list[dict[str, Any]]:
    status = result["status"]
    return [
        {
            "runner_id": "R10_RUNNER_564_LIVE_PLACEHOLDER_RECHECK",
            "mts_curve": status["mts_curve"],
            "bound_curve": status["bound_curve"],
            "mts_rows": status["mts_rows"],
            "valid_mts_rows": status["valid_mts_rows"],
            "bound_rows": status["bound_rows"],
            "valid_bound_rows": status["valid_bound_rows"],
            "comparison_rows": status["comparison_rows"],
            "passed_rows": status["passed_rows"],
            "blocked_or_failed_rows": status["blocked_or_failed_rows"],
            "R10_pass_for_claim": status["R10_pass_for_claim"],
            "claim_allowed": status["claim_allowed"],
            "notes": "live placeholders remain blocked; 564 is derivation only",
        }
    ]


def build_evaluator(runner_result: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "E564_0_Hessian_extraction",
            "gate": "derive formal parent-Hessian extraction for Z_X and M_X^2",
            "result": "conditional_pass",
            "detail": "Z_X and M_X^2 are exact second-variation residues, but not numeric or signed from an explicit parent action",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "E564_1_operator_fork",
            "gate": "derive theorem-zero/Yukawa fork",
            "result": "conditional_pass",
            "detail": "positive source-free operator gives X=0; sourced branch gives finite Yukawa alpha(lambda)",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "E564_2_matter_pullback",
            "gate": "derive matter source term",
            "result": "pass_expression_fail_zero",
            "detail": "J_matter=(1/2)sqrt(-hat_g)T_hat^{mu nu}partial_X hat_g_{mu nu}; zero requires X-blind observed coframe or Ward cancellation",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "E564_3_theorem_zero",
            "gate": "prove R10 source-zero/no-hair",
            "result": "fail_current_claim",
            "detail": "coframe pullback and boundary/projector/memory/domain source zeros are not parent-signed",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "E564_4_numeric_alpha",
            "gate": "produce numeric/source-backed alpha(lambda)",
            "result": "fail_current_claim",
            "detail": "Z_X, M_X^2, Qbar_XH, qbar_XT, and full bound curve remain unavailable",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "E564_5_runner_guardrail",
            "gate": "R10 runner remains blocked",
            "result": "pass" if not runner_result["status"]["R10_pass_for_claim"] else "fail",
            "detail": f"valid_mts={runner_result['status']['valid_mts_rows']};valid_bound={runner_result['status']['valid_bound_rows']};R10_pass={runner_result['status']['R10_pass_for_claim']}",
            "valid_for_claim": "false",
        },
    ]


def build_blocker_rows() -> list[dict[str, str]]:
    return [
        {
            "blocker_id": "B564_0_no_explicit_parent_X_block",
            "blocker": "Z_X and M_X^2 are definable as Hessian residues but not evaluated or signed.",
            "why_it_matters": "lambda_X and K_X cannot become claim rows without parent-owned signs/values.",
            "next_action": "write or derive the explicit X quadratic/constraint block",
            "claim_blocked": "true",
        },
        {
            "blocker_id": "B564_1_coframe_pullback_sources_X",
            "blocker": "ordinary matter generically sources X if the observed metric/coframe depends on X.",
            "why_it_matters": "source-zero fails unless partial_X hat_g=0 or a Ward identity cancels the full stress contraction.",
            "next_action": "derive coframe X-blindness or retain qbar_XT/Qbar_XH coefficients",
            "claim_blocked": "true",
        },
        {
            "blocker_id": "B564_2_hidden_source_channels_open",
            "blocker": "boundary, projector, memory, and domain source channels are not zeroed.",
            "why_it_matters": "no-hair identity requires channelwise zero source and zero boundary flux.",
            "next_action": "prove channelwise Ward/topological zero or bound every channel",
            "claim_blocked": "true",
        },
    ]


def build_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D564_0_Hessian_contract_derived",
            "decision": "parent-Hessian extraction formula written",
            "meaning": "Z_X and M_X^2 are second-variation residues, not fit knobs",
            "status": "conditional_progress",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D564_1_source_zero_not_derived",
            "decision": "theorem-zero fails current claim",
            "meaning": "matter coframe pullback plus hidden source channels remain active",
            "status": "R10_retained",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D564_2_next_fork",
            "decision": "attack coframe pullback zero or fill finite alpha coefficients",
            "meaning": "the next hinge is partial_X hat_g=0 versus a real Yukawa residual",
            "status": "sharp_fork",
            "next_target": NEXT_TARGET,
        },
    ]


def build_route_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU564_0_allowed",
            "allowed_after_564": "MTS may cite the parent-Hessian extraction formulas and the exact matter-pullback source expression.",
            "forbidden_after_564": "MTS may not claim numeric Z_X, numeric lambda_X, theorem-zero, R10 pass, PPN pass, or local-GR pass.",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU564_1_theory_fork",
            "allowed_after_564": "MTS may now target partial_X hat_g=0 as the clean source-zero route.",
            "forbidden_after_564": "MTS may not hide nonzero universal finite-range coupling as measured GM.",
            "next_action": "if coframe pullback does not zero, construct coefficient-fill route",
        },
    ]


def build_validation_rows(
    source_rows: list[dict[str, str]],
    prior_rows: list[dict[str, str]],
    runner_result: dict[str, Any],
) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in source_rows if row["exists"] != "True"]
    prior_fails = [row for row in prior_rows if row.get("result") != "pass"]
    claim_rows = [
        row
        for table in [
            HESSIAN_FORMULA_ROWS,
            SOURCE_ZERO_ROWS,
            MATTER_PULLBACK_ROWS,
            PARENT_REQUIREMENT_ROWS,
            ALPHA_POLICY_ROWS,
        ]
        for row in table
        if str(row.get("valid_for_claim", "")).lower() == "true"
    ]
    has_pullback_expression = any("partial_X hat_g" in row["expression"] for row in MATTER_PULLBACK_ROWS)
    has_hessian_formula = any("Z_X" in row["expression"] and "H_grad" in row["expression"] for row in HESSIAN_FORMULA_ROWS)
    no_overclaim = not runner_result["status"]["R10_pass_for_claim"] and not claim_rows
    return [
        {
            "check_id": "V564_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V564_1_prior_563_clean",
            "result": "pass" if prior_rows and not prior_fails else "fail",
            "detail": f"prior_validation_rows={len(prior_rows)};prior_fails={len(prior_fails)}",
        },
        {
            "check_id": "V564_2_Hessian_formula_written",
            "result": "pass" if has_hessian_formula else "fail",
            "detail": f"hessian_rows={len(HESSIAN_FORMULA_ROWS)}",
        },
        {
            "check_id": "V564_3_matter_pullback_expression_written",
            "result": "pass" if has_pullback_expression else "fail",
            "detail": f"pullback_rows={len(MATTER_PULLBACK_ROWS)}",
        },
        {
            "check_id": "V564_4_source_zero_not_overclaimed",
            "result": "pass" if all(row["valid_for_claim"] == "false" for row in SOURCE_ZERO_ROWS) else "fail",
            "detail": f"source_zero_rows={len(SOURCE_ZERO_ROWS)};claim_rows=0",
        },
        {
            "check_id": "V564_5_runner_still_blocks_placeholders",
            "result": "pass" if not runner_result["status"]["R10_pass_for_claim"] else "fail",
            "detail": f"valid_mts={runner_result['status']['valid_mts_rows']};valid_bound={runner_result['status']['valid_bound_rows']};R10_pass={runner_result['status']['R10_pass_for_claim']}",
        },
        {
            "check_id": "V564_6_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V564_7_no_overclaim",
            "result": "pass" if no_overclaim else "fail",
            "detail": "numeric_ZX=false;numeric_MX=false;source_zero=false;R10_pass=false;Newton=false;PPN=false;local_GR=false",
        },
    ]


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    columns = list(rows[0].keys())
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(
    source_rows: list[dict[str, str]],
    runner_summary: list[dict[str, Any]],
    evaluator_rows: list[dict[str, str]],
    blocker_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    route_rows: list[dict[str, str]],
) -> None:
    body = f"""# 564 Y5 R10 parent-Hessian source-zero attempt

Generated: {datetime.now(timezone.utc).isoformat()}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- The parent-Hessian extraction was derived as a contract: `Z_X` and `M_X^2` are second-variation residues of the same parent action.
- The theorem-zero route was sharpened but not closed: it requires positive Hessian, zero matter pullback, zero hidden source channels, and zero boundary flux.
- The key obstruction is now explicit: if ordinary matter sees an observed metric/coframe `hat_g(X)`, then `T_hat^{{mu nu}} partial_X hat_g_mu nu` generically sources `X`.
- Therefore this checkpoint gives a real derivation fork, not a pass: prove `partial_X hat_g=0`/Ward cancellation, or keep the finite Yukawa alpha row.

## Core Derivation
For a local branch expanded about `X=0`,

```text
S_parent[X]=S0 + int sqrt(-g) E_X|0 deltaX
  + 1/2 int sqrt(-g)[H_grad^{{mu nu}} nabla_mu deltaX nabla_nu deltaX - H_0 deltaX^2]+...
```

The static local equation is therefore:

```text
(-Z_X Delta + M_X^2)X = J_X,
lambda_X = sqrt(Z_X/M_X^2),
J_X = J_matter_pullback + J_boundary + J_projector + J_memory + J_domain + J_direct_MTS.
```

The ordinary-matter pullback source is:

```text
J_matter_pullback = (1/2) sqrt(-hat_g) T_hat^{{mu nu}} partial_X hat_g_{{mu nu}}.
```

This is the uncomfortable but useful result: one-coframe/universal matter is not enough by itself. The observed coframe must be `X`-blind, pure gauge in the stress contraction, or Ward-cancelled by a parent-owned counterterm.

## Hessian Extraction Formula
{markdown_table(HESSIAN_FORMULA_ROWS)}

## Source-Zero Theorem Attempt
{markdown_table(SOURCE_ZERO_ROWS)}

## Matter Pullback Charge Map
{markdown_table(MATTER_PULLBACK_ROWS)}

## Parent Action Requirements
{markdown_table(PARENT_REQUIREMENT_ROWS)}

## Alpha Row Policy
{markdown_table(ALPHA_POLICY_ROWS)}

## Runner Summary
{markdown_table(runner_summary)}

## Evaluator
{markdown_table(evaluator_rows)}

## Blocker Ledger
{markdown_table(blocker_rows)}

## Decision
{markdown_table(decision_rows)}

## Source Register
{markdown_table(source_rows)}

## Validation
{markdown_table(validation_rows)}

## Route Update
{markdown_table(route_rows)}

## Practical Read
This is progress, but not the shiny kind. We did not get to say `X` vanishes. We got the exact place the knife has to go: the parent action must make the observed coframe `X`-blind, or it must own a Ward cancellation of the matter pullback. If it cannot do that, R10 is not dead; it becomes a finite Yukawa residual with `alpha_X(lambda)=K_X Qbar_XH qbar_XT` and must be tested.
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_root = ROOT / "runs" / f"{timestamp}-Y5-R10-parent-hessian-source-zero-attempt" / "results"
    runner_result = run_runner(ROOT / LIVE_MTS_CURVE_PATH, ROOT / LIVE_BOUND_CURVE_PATH, run_root / "live_placeholder_runner")

    source_rows = source_register_rows()
    prior_rows = read_csv(ROOT / PRIOR_VALIDATION_PATH)
    runner_summary = build_runner_summary(runner_result)
    evaluator_rows = build_evaluator(runner_result)
    blocker_rows = build_blocker_rows()
    decision_rows = build_decision_rows()
    route_rows = build_route_rows()
    validation_rows = build_validation_rows(source_rows, prior_rows, runner_result)

    write_csv(SOURCE_REGISTER_PATH, source_rows)
    write_csv(HESSIAN_FORMULA_PATH, HESSIAN_FORMULA_ROWS)
    write_csv(SOURCE_ZERO_PATH, SOURCE_ZERO_ROWS)
    write_csv(MATTER_PULLBACK_PATH, MATTER_PULLBACK_ROWS)
    write_csv(PARENT_REQUIREMENTS_PATH, PARENT_REQUIREMENT_ROWS)
    write_csv(ALPHA_POLICY_PATH, ALPHA_POLICY_ROWS)
    write_csv(RUNNER_SUMMARY_PATH, runner_summary)
    write_csv(EVALUATOR_PATH, evaluator_rows)
    write_csv(BLOCKER_LEDGER_PATH, blocker_rows)
    write_csv(DECISION_PATH, decision_rows)
    write_csv(VALIDATION_PATH, validation_rows)
    write_csv(ROUTE_UPDATE_PATH, route_rows)
    write_doc(source_rows, runner_summary, evaluator_rows, blocker_rows, decision_rows, validation_rows, route_rows)

    summary = {
        "status": STATUS,
        "doc": rel(ROOT / DOC_PATH),
        "hessian_formula": rel(ROOT / HESSIAN_FORMULA_PATH),
        "source_zero_attempt": rel(ROOT / SOURCE_ZERO_PATH),
        "matter_pullback_map": rel(ROOT / MATTER_PULLBACK_PATH),
        "validation": rel(ROOT / VALIDATION_PATH),
        "validation_failed": [row for row in validation_rows if row["result"] != "pass"],
        "claim_ceiling": CLAIM_CEILING,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

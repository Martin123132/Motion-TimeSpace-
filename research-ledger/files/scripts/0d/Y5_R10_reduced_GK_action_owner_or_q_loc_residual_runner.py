from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
RUNS = ROOT / "runs"

SLUG = "Y5-R10-reduced-GK-action-owner-or-q_loc-residual-runner"
DOC_PATH = ROOT / "597-Y5-R10-reduced-GK-action-owner-or-q_loc-residual-runner.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_597_SOURCE_REGISTER.csv"
OWNER_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_597_REDUCED_GK_ACTION_OWNER_ATTEMPT.csv"
METRIC_RESPONSE_PATH = RESIDUALS / "P8_Y5_R10_597_METRIC_RESPONSE_DERIVATION.csv"
WARD_GATE_PATH = RESIDUALS / "P8_Y5_R10_597_WARD_ZERO_GATE.csv"
RESIDUAL_RUNNER_PATH = RESIDUALS / "P8_Y5_R10_597_QLOC_RESIDUAL_RUNNER_INPUT_QUEUE.csv"
FORK_PATH = RESIDUALS / "P8_Y5_R10_597_OWNER_OR_RUNNER_FORK.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_597_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_597_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_597_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_597_VALIDATION.csv"

PRIOR_596_VALIDATION = RESIDUALS / "P8_Y5_BRR545_596_VALIDATION.csv"

STATUS = "Y5_R10_reduced_GK_owner_contract_written_current_symbol_match_failed_q_loc_residual_runner_triggered"
CLAIM_CEILING = "reduced_GK_owner_contract_and_residual_runner_queue_only_no_R10_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "598-Y5-R10-fill-q_loc-residual-runner-or-derive-first-zero-row.md"

SOURCE_FILES = [
    ("596-Y5-R10-test-Gamma-Khat-qloc-factor-through-pi-or-demote.md", "immediate q_loc demotion handoff"),
    ("source-intake/mts_residuals/P8_Y5_BRR545_596_VALIDATION.csv", "prior validation gate"),
    ("source-intake/mts_residuals/P8_Y5_R10_596_GAMMA_KHAT_PI_FACTOR_TEST.csv", "Gamma/Khat factor-through-pi test"),
    ("source-intake/mts_residuals/P8_Y5_R10_596_QLOC_EXACTNESS_OR_RESIDUAL_GATE.csv", "exactness or residual fork"),
    ("source-intake/mts_residuals/P8_Y5_R10_596_DEMOTION_ROUTING.csv", "596 demotion routing"),
    ("513-Gamma-Khat-q_loc-first-variation-or-demotion.md", "stress-divergence identity"),
    ("514-construct-GK-stress-action-or-residual-bound.md", "candidate S_GK action"),
    ("515-match-Gamma-eff-Khat-to-metric-response-action.md", "current symbol-match failure audit"),
    ("516-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner.md", "Gamma owner candidates and q_loc bound runner spec"),
    ("517-response-doublet-action-variation-ledger-or-run-q_loc-bound.md", "response-doublet variation and Y5/Y6 blockers"),
    ("518-Y5-source-normalization-owner-or-q_loc-bound-implementation.md", "source-normalization residual runner input"),
    ("source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_CONTRACT.csv", "metric-response contract"),
    ("source-intake/mts_residuals/P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv", "match audit failures"),
    ("source-intake/mts_residuals/P8_QLOC_BOUND_RUNNER_SPEC.csv", "q_loc runner spec"),
    ("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT.csv", "Y5/q_loc source-normalization queue"),
    ("source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv", "response-doublet action contract"),
    ("source-intake/mts_residuals/P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv", "Y0-Y6 source ledger"),
    ("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_NUMERIC_INPUT_TEMPLATE.csv", "source-normalization numeric templates"),
    ("source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv", "PPN/source residual vector template"),
    ("scripts/Y5_R10_reduced_GK_action_owner_or_q_loc_residual_runner.py", "this checkpoint generator"),
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", "<br>").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def make_sources() -> list[dict[str, str]]:
    return [
        {
            "source_file": source_file,
            "exists": str((ROOT / source_file).exists()),
            "role": role,
        }
        for source_file, role in SOURCE_FILES
    ]


def make_owner_rows() -> list[dict[str, str]]:
    return [
        {
            "owner_id": "RGA597_A_reduced_scalar_density_owner",
            "candidate": "S_GK^red[Q_obs] = - integral_M sqrt(-g_obs) gamma(g_obs,Phi_red,D Phi_red,topological data) + integral_boundary B_GK",
            "owned_objects": "Gamma_eff=gamma; K_hat=metric response kappa_gamma; T_GK=gamma g_obs-K_hat",
            "would_derive": "Gamma/Khat/q_loc are reduced Q_obs objects and the vertical-X quotient branch has no hidden local source",
            "blocker": "current corpus has no actual Gamma_eff scalar-density definition and no K_hat metric-response match",
            "current_status": "contract_written_not_matched",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "RGA597_B_response_doublet_density",
            "candidate": "gamma = gamma0 + 1/2 M_AB(g_obs,R_even,D) Z^A Z^B + O(Z^4)",
            "owned_objects": "exchange-odd residual doublets Z^A with formal double-zero at Z=0",
            "would_derive": "F_1=0 for auxiliary response variables and a clean positive-operator/no-hair route if Z is physical",
            "blocker": "Y5 source normalization, Y6 extra stress, PPN lock, and boundary response are not killed by parity alone",
            "current_status": "formal_candidate_Y5_Y6_blocked",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "RGA597_C_positive_auxiliary_nohair",
            "candidate": "gamma = V(Phi) + 1/2 G_AB(Phi) nabla Phi^A nabla Phi^B with positive local operator",
            "owned_objects": "source-free auxiliary reduced fields Phi_red",
            "would_derive": "E_A=0 plus positive boundary conditions force Phi=Phi0 and q_loc=0 on compact local vacuum",
            "blocker": "source-free local Euler equations and no-boundary/no-marker theorem are not derived for current MTS",
            "current_status": "candidate_not_component_locked",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "RGA597_D_exact_topological_improvement",
            "candidate": "T_GK=dB_GK or an improvement stress whose compact local flux is zero",
            "owned_objects": "exact/improvement stress and fixed boundary reference",
            "would_derive": "bulk q_loc zero without a propagating field",
            "blocker": "boundary/source-measure flux and ADM/reference subtraction remain open",
            "current_status": "boundary_risk_open",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "RGA597_E_residual_runner",
            "candidate": "no owner accepted for current claim; retain q_loc as reduced observed residual",
            "owned_objects": "runner rows for compact-shell, source normalization, PPN, R10/R11 operator, and boundary channels",
            "would_derive": "nothing by theorem; instead tests whether the residual is small enough with sourced inputs",
            "blocker": "numeric/source-backed projection coefficients are not filled yet",
            "current_status": "triggered_for_current_claim",
            "valid_for_claim": "false",
        },
    ]


def make_metric_rows() -> list[dict[str, str]]:
    return [
        {
            "step_id": "MRD597_0_define_reduced_action",
            "derivation_step": "Choose reduced variables Q_obs=(g_obs,Phi_red,matter readout after variation,boundary reference class) and define S_GK^red on Q_obs only.",
            "formula": "S_GK^red = - int sqrt(-g_obs) gamma[Q_obs] + int_boundary B_GK",
            "passes_if": "gamma has units, covariance, and no representative marker dependence",
            "current_status": "formal_definition_available",
            "valid_for_claim": "false",
        },
        {
            "step_id": "MRD597_1_metric_response",
            "derivation_step": "Define K_hat by metric response rather than independently.",
            "formula": "K_hat^{mu nu} := K_gamma^{mu nu} under the 514 convention, so T_GK^{mu nu}=gamma g_obs^{mu nu}-K_gamma^{mu nu}",
            "passes_if": "existing K_hat tensor structure equals this variation including derivative and boundary terms",
            "current_status": "definition_possible_existing_match_failed",
            "valid_for_claim": "false",
        },
        {
            "step_id": "MRD597_2_vertical_blindness",
            "derivation_step": "Because S_GK^red is a functional of Q_obs, v_X cannot vary it if d pi(v_X)=0.",
            "formula": "delta_X S_GK^red = dS_GK^red[d pi(v_X)] = 0",
            "passes_if": "Gamma_eff, K_hat, P_loc and boundary reference all factor through Q_obs",
            "current_status": "conditional_pass",
            "valid_for_claim": "false",
        },
        {
            "step_id": "MRD597_3_Ward_identity",
            "derivation_step": "Diffeomorphism invariance of the reduced action controls the divergence of T_GK.",
            "formula": "nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi_red^A + boundary_flux^nu",
            "passes_if": "E_A=0 in compact local vacuum and boundary_flux=0 after fixed reference subtraction",
            "current_status": "conditional_only",
            "valid_for_claim": "false",
        },
        {
            "step_id": "MRD597_4_q_loc_gate",
            "derivation_step": "Project the Ward identity only after ownership is established.",
            "formula": "q_loc^nu=P_loc nabla_mu T_GK^{mu nu}=P_loc(sum_A E_A nabla^nu Phi_A + boundary_flux^nu)",
            "passes_if": "P_loc is parent-owned and does not hide unprojected components",
            "current_status": "projector_ownership_open",
            "valid_for_claim": "false",
        },
    ]


def make_ward_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "WZG597_0_current_symbol_match",
            "needed_for_zero": "actual current Gamma_eff and K_hat match gamma and K_gamma",
            "status": "fail_for_current_claim",
            "evidence": "515 match audit: no scalar-density owner or K_hat metric response found",
            "fallback": "retain q_loc residual row",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "WZG597_1_Euler_source_free",
            "needed_for_zero": "reduced fields entering gamma obey E_A=0 in compact local vacuum",
            "status": "not_derived",
            "evidence": "516/517 keep Y5 and Y6 source ledgers active",
            "fallback": "score source-normalization and extra-stress residual components",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "WZG597_2_double_zero",
            "needed_for_zero": "T_GK(Phi0) is background-subtracted and first variation vanishes",
            "status": "formal_for_auxiliary_Z_not_physical_lock",
            "evidence": "response-doublet density gives formal F_1=0, but Z=physical PPN/source residual is unproved",
            "fallback": "fill PPN lock or residual vector",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "WZG597_3_projector_ownership",
            "needed_for_zero": "P_loc is parent-owned and commutes with local/readout limit",
            "status": "open",
            "evidence": "513/514/596 keep P_loc ownership open",
            "fallback": "carry full unprojected residual or derive projector algebra",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "WZG597_4_boundary_no_flux",
            "needed_for_zero": "metric response and integrations by parts have no compact local source/mass flux",
            "status": "open",
            "evidence": "boundary/source-measure flux repeatedly retained as active risk",
            "fallback": "compact-shell q_loc/source-measure bound",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "WZG597_5_Y5_source_normalization",
            "needed_for_zero": "measured GM/source strength equals one parent EH/Hilbert source charge with no extra projection",
            "status": "hard_blocker_active",
            "evidence": "518 writes owner theorem but marks all premises not parent-derived",
            "fallback": "Y5 source-normalization bound runner",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "WZG597_6_Y6_extra_stress",
            "needed_for_zero": "extra stress is topological/invisible or below PPN/operator locks",
            "status": "hard_blocker_active",
            "evidence": "517 marks Y6 stress_Bianchi retained debt",
            "fallback": "T_extra/PPN/operator residual vector",
            "valid_for_claim": "false",
        },
    ]


def make_residual_runner_rows() -> list[dict[str, str]]:
    return [
        {
            "runner_id": "QRR597_0_compact_shell_budget",
            "quantity": "max |P_loc d_rel J_rel| or q_loc compact leakage proxy",
            "current_input": "7.432631961576971e-06 dimensionless proxy from 220",
            "needed_to_score": "map proxy into PPN/source-normalization units and sign convention",
            "acceptance_gate": "cannot be claim-valid until mapping is sourced",
            "status": "queued_not_scored",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "QRR597_1_source_normalization_Y5",
            "quantity": "q_loc projection into measured-GM/source-normalization channel",
            "current_input": "P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT rows all missing/not_scored",
            "needed_to_score": "C_qmu projection operator, units, and source-backed/theorem-zero values for Gdot, Mdot, radial, species, range, frame, beta, PPN",
            "acceptance_gate": "each channel derived zero or below official local row locks",
            "status": "queued_not_scored",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "QRR597_2_alpha3_boundary_pressure",
            "quantity": "preferred-frame/momentum-flux equivalent",
            "current_input": "alpha3 lock 4e-20 where applicable",
            "needed_to_score": "coefficient from q_loc/boundary flux to alpha3-equivalent row",
            "acceptance_gate": "source-backed coefficient below alpha3 lock or derived boundary zero",
            "status": "queued_not_scored",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "QRR597_3_PPN_metric_tail",
            "quantity": "Delta_PPN={gamma-1,beta-1,alpha_i,xi,zeta_i}_source",
            "current_input": "template only; weak-field map not filled",
            "needed_to_score": "linearized metric solution sourced by q_loc and source-normalization split",
            "acceptance_gate": "all PPN components below bounds or theorem-zero",
            "status": "queued_not_scored",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "QRR597_4_R10_range_tail",
            "quantity": "alpha(lambda) or range-dependent source strength",
            "current_input": "real bound curve infrastructure exists but q_loc-to-alpha coefficient is missing",
            "needed_to_score": "lambda, alpha coefficient, source path, and bound-curve comparison",
            "acceptance_gate": "abs(alpha_predicted)<=alpha_bound with source-backed rows",
            "status": "queued_not_scored",
            "valid_for_claim": "false",
        },
        {
            "runner_id": "QRR597_5_R11_operator_vector",
            "quantity": "non-EH/operator/source-normalization coefficient vector",
            "current_input": "symbolic until operator family and normalization are filled",
            "needed_to_score": "operator basis, units, weak-field normalization, and bound comparison",
            "acceptance_gate": "operator vector below R11/local locks or derived zero",
            "status": "queued_not_scored",
            "valid_for_claim": "false",
        },
    ]


def make_fork_rows() -> list[dict[str, str]]:
    return [
        {
            "fork_id": "F597_A_owner_acceptance",
            "condition": "Gamma_eff scalar density, K_hat metric response, Ward zero, Y5/Y6 closure, boundary no-flux, and P_loc ownership all pass",
            "decision": "promote reduced GK owner to theorem candidate for q_loc zero only",
            "current_status": "not_triggered",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "fork_id": "F597_B_owner_partial",
            "condition": "reduced owner can be defined but actual current Gamma/Khat symbol match is not proven",
            "decision": "keep owner as contract and trigger residual runner",
            "current_status": "triggered",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "fork_id": "F597_C_owner_failure",
            "condition": "Gamma/Khat cannot be reduced-action objects or P_loc/readout/boundary smuggle residuals",
            "decision": "demote q_loc route fully to residual/edge/diffeo-current backup",
            "current_status": "not_yet_final",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
        },
    ]


def make_decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "D597_0_reduced_owner_contract_written",
            "decision": "write reduced S_GK owner theorem-contract on Q_obs",
            "meaning": "there is a legitimate route to q_loc=0 if Gamma/Khat are reduced action/metric-response objects",
            "claim_status": "contract_only",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D597_1_current_match_failed",
            "decision": "do not accept owner for current MTS claim",
            "meaning": "515/596 still block actual Gamma_eff scalar-density and K_hat metric-response match",
            "claim_status": "q_loc_zero_false_for_current_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D597_2_residual_runner_triggered",
            "decision": "queue q_loc residual runner rows",
            "meaning": "next work must either derive a first zero row or fill source-backed numeric residual inputs",
            "claim_status": "runner_ready_not_scored",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update_rows() -> list[dict[str, str]]:
    return [
        {
            "route_id": "RU597_0_allowed",
            "allowed_after_597": "cite reduced S_GK as a theorem contract only",
            "forbidden_after_597": "claim current MTS has derived q_loc=0",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU597_1_allowed",
            "allowed_after_597": "use residual runner rows for q_loc/source-normalization/PPN/R10/R11 channels",
            "forbidden_after_597": "call queued residual rows scored or below bounds",
            "next_action": NEXT_TARGET,
        },
        {
            "route_id": "RU597_2_allowed",
            "allowed_after_597": "try to derive one first zero row before filling numeric coefficients",
            "forbidden_after_597": "hide Y5/Y6 or boundary flux behind the reduced-action contract",
            "next_action": NEXT_TARGET,
        },
    ]


def make_summary_rows() -> list[dict[str, str]]:
    return [
        {
            "summary_id": "S597_0",
            "claim_allowed": "false",
            "R10_pass": "false",
            "WEP_pass": "false",
            "PPN_pass": "false",
            "local_GR_pass": "false",
            "owner_status": "reduced_contract_written_current_match_failed",
            "runner_status": "triggered_not_scored",
            "best_private_read": "The reduced GK owner is mathematically coherent as a contract, but current MTS still lacks the Gamma/Khat metric-response match and Y5/Y6/boundary closure. The honest next move is either derive a first zero row or fill q_loc residual runner inputs.",
            "next_target": NEXT_TARGET,
        }
    ]


def make_validation(
    sources: list[dict[str, str]],
    owner_rows: list[dict[str, str]],
    metric_rows: list[dict[str, str]],
    ward_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    fork_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    prior_rows = read_csv(PRIOR_596_VALIDATION)
    prior_failures = [row for row in prior_rows if row.get("result", "").strip().lower() != "pass"]
    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_rows = [
        *[row for row in owner_rows if row["valid_for_claim"] == "true"],
        *[row for row in metric_rows if row["valid_for_claim"] == "true"],
        *[row for row in ward_rows if row["valid_for_claim"] == "true"],
        *[row for row in runner_rows if row["valid_for_claim"] == "true"],
        *[row for row in fork_rows if row["valid_for_claim"] == "true"],
    ]
    owner_contract = any(row["owner_id"] == "RGA597_A_reduced_scalar_density_owner" for row in owner_rows)
    metric_response = any(row["step_id"] == "MRD597_1_metric_response" for row in metric_rows)
    current_match_fail = any(row["gate_id"] == "WZG597_0_current_symbol_match" and row["status"] == "fail_for_current_claim" for row in ward_rows)
    y5_y6_retained = all(
        any(row["gate_id"] == gate_id and "blocker" in row["status"] for row in ward_rows)
        for gate_id in ["WZG597_5_Y5_source_normalization", "WZG597_6_Y6_extra_stress"]
    )
    runner_triggered = any(row["fork_id"] == "F597_B_owner_partial" and row["current_status"] == "triggered" for row in fork_rows)
    runner_coverage = len(runner_rows) >= 6
    return [
        {
            "check_id": "V597_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V597_1_prior_596_clean",
            "result": "pass" if prior_rows and not prior_failures else "fail",
            "detail": f"prior_rows={len(prior_rows)};prior_failures={len(prior_failures)}",
        },
        {
            "check_id": "V597_2_reduced_owner_contract_present",
            "result": "pass" if owner_contract else "fail",
            "detail": f"owner_rows={len(owner_rows)}",
        },
        {
            "check_id": "V597_3_metric_response_derivation_present",
            "result": "pass" if metric_response else "fail",
            "detail": f"metric_rows={len(metric_rows)}",
        },
        {
            "check_id": "V597_4_current_match_failure_retained",
            "result": "pass" if current_match_fail else "fail",
            "detail": "Gamma/Khat match still fails for current claim",
        },
        {
            "check_id": "V597_5_Y5_Y6_retained",
            "result": "pass" if y5_y6_retained else "fail",
            "detail": "Y5 source normalization and Y6 extra stress remain blockers",
        },
        {
            "check_id": "V597_6_residual_runner_triggered",
            "result": "pass" if runner_triggered and runner_coverage else "fail",
            "detail": f"runner_rows={len(runner_rows)};triggered={runner_triggered}",
        },
        {
            "check_id": "V597_7_no_claim_rows",
            "result": "pass" if not claim_rows else "fail",
            "detail": f"claim_rows={len(claim_rows)}",
        },
        {
            "check_id": "V597_8_no_R10_or_local_GR_claim",
            "result": "pass",
            "detail": "claim_allowed=false;R10_pass=false;WEP=false;PPN=false;local_GR=false",
        },
    ]


def write_markdown(
    generated: str,
    run_root: Path,
    sources: list[dict[str, str]],
    owner_rows: list[dict[str, str]],
    metric_rows: list[dict[str, str]],
    ward_rows: list[dict[str, str]],
    runner_rows: list[dict[str, str]],
    fork_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    route_update_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 597 Y5 R10 reduced GK action owner or q_loc residual runner

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`  
Run root: `{rel(run_root)}`

## Verdict
- The reduced GK owner route can be written cleanly: define `S_GK^red[Q_obs]`, take `Gamma_eff=gamma`, and define `K_hat` as the metric response so `T_GK=gamma g_obs-K_hat`.
- This gives the right Ward route: `q_loc=P_loc nabla_mu T_GK^{{mu nu}}` becomes zero only if the reduced Euler equations, projector ownership, and boundary no-flux gates pass.
- Current MTS does not pass those gates. The actual `Gamma_eff/K_hat` symbol match is still missing, and Y5/Y6 remain hard blockers.
- So 597 triggers the honest fallback: `q_loc` is now queued as a reduced observed residual runner unless 598 derives a first zero row.

## Source Register
{markdown_table(sources, ["source_file", "exists", "role"])}

## Reduced GK Action Owner Attempt
{markdown_table(owner_rows, ["owner_id", "candidate", "owned_objects", "would_derive", "blocker", "current_status", "valid_for_claim"])}

## Metric Response Derivation
{markdown_table(metric_rows, ["step_id", "derivation_step", "formula", "passes_if", "current_status", "valid_for_claim"])}

## Ward Zero Gate
{markdown_table(ward_rows, ["gate_id", "needed_for_zero", "status", "evidence", "fallback", "valid_for_claim"])}

## Qloc Residual Runner Input Queue
{markdown_table(runner_rows, ["runner_id", "quantity", "current_input", "needed_to_score", "acceptance_gate", "status", "valid_for_claim"])}

## Owner Or Runner Fork
{markdown_table(fork_rows, ["fork_id", "condition", "decision", "current_status", "next_action", "valid_for_claim"])}

## Decision
{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])}

## Route Update
{markdown_table(route_update_rows, ["route_id", "allowed_after_597", "forbidden_after_597", "next_action"])}

## Validation
{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read
This is not bad news; it is the right accounting. We now have a clean reduced-action door, but the current symbols have not walked through it. Until they do, `q_loc` stops being a mystical local-GR proof and becomes a residual vector we can either kill one row at a time or score against local gates.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> int:
    generated = datetime.now(timezone.utc).isoformat()
    run_root = RUNS / f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{SLUG}"
    run_root.mkdir(parents=True, exist_ok=True)

    sources = make_sources()
    owner_rows = make_owner_rows()
    metric_rows = make_metric_rows()
    ward_rows = make_ward_rows()
    runner_rows = make_residual_runner_rows()
    fork_rows = make_fork_rows()
    decision_rows = make_decision_rows()
    route_update_rows = make_route_update_rows()
    summary_rows = make_summary_rows()
    validation_rows = make_validation(sources, owner_rows, metric_rows, ward_rows, runner_rows, fork_rows)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_file", "exists", "role"])
    write_csv(OWNER_ATTEMPT_PATH, owner_rows, ["owner_id", "candidate", "owned_objects", "would_derive", "blocker", "current_status", "valid_for_claim"])
    write_csv(METRIC_RESPONSE_PATH, metric_rows, ["step_id", "derivation_step", "formula", "passes_if", "current_status", "valid_for_claim"])
    write_csv(WARD_GATE_PATH, ward_rows, ["gate_id", "needed_for_zero", "status", "evidence", "fallback", "valid_for_claim"])
    write_csv(RESIDUAL_RUNNER_PATH, runner_rows, ["runner_id", "quantity", "current_input", "needed_to_score", "acceptance_gate", "status", "valid_for_claim"])
    write_csv(FORK_PATH, fork_rows, ["fork_id", "condition", "decision", "current_status", "next_action", "valid_for_claim"])
    write_csv(DECISION_PATH, decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target"])
    write_csv(ROUTE_UPDATE_PATH, route_update_rows, ["route_id", "allowed_after_597", "forbidden_after_597", "next_action"])
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        [
            "summary_id",
            "claim_allowed",
            "R10_pass",
            "WEP_pass",
            "PPN_pass",
            "local_GR_pass",
            "owner_status",
            "runner_status",
            "best_private_read",
            "next_target",
        ],
    )
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_markdown(
        generated,
        run_root,
        sources,
        owner_rows,
        metric_rows,
        ward_rows,
        runner_rows,
        fork_rows,
        decision_rows,
        route_update_rows,
        validation_rows,
    )

    status_payload = {
        "generated": generated,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": rel(DOC_PATH),
        "validation": rel(VALIDATION_PATH),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    (run_root / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    (run_root / "COMPLETE.marker").write_text("complete\n", encoding="utf-8")
    print(json.dumps(status_payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

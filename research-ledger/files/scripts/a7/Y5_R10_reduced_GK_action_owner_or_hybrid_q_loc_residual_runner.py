from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
RUNS = POST_CHECKPOINT / "runs"
FORMALIZATION = POST_CHECKPOINT.parent / "formalization-workbench"
OUTPUT_DOC = POST_CHECKPOINT / "733-Y5-R10-reduced-GK-action-owner-or-hybrid-q_loc-residual-runner.md"
NEXT_TARGET = "734-Y5-R10-fill-hybrid-q_loc-residual-runner-or-derive-first-zero-row.md"
CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

STATUS = "Y5_R10_733_reduced_GK_owner_contract_written_current_symbol_match_failed_hybrid_q_loc_runner_triggered"
CLAIM_CEILING = "hybrid_reduced_GK_owner_contract_and_residual_runner_queue_only_no_R10_WEP_PPN_Newton_or_local_GR_pass"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_733_SOURCE_REGISTER.csv"
OWNER_ATTEMPT_PATH = RESIDUALS / "P8_Y5_R10_733_REDUCED_GK_OWNER_ATTEMPT.csv"
METRIC_RESPONSE_PATH = RESIDUALS / "P8_Y5_R10_733_METRIC_RESPONSE_DERIVATION.csv"
WARD_ZERO_PATH = RESIDUALS / "P8_Y5_R10_733_WARD_ZERO_GATE.csv"
RESIDUAL_RUNNER_PATH = RESIDUALS / "P8_Y5_R10_733_HYBRID_QLOC_RESIDUAL_RUNNER_QUEUE.csv"
OWNER_RUNNER_FORK_PATH = RESIDUALS / "P8_Y5_R10_733_OWNER_OR_RUNNER_FORK.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_733_DECISION_MATRIX.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_733_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_733_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_733_VALIDATION.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "732_doc": {
        "path": POST_CHECKPOINT / "732-Y5-R10-construct-hybrid-pi-observed-quotient-map-or-demote.md",
        "role": "immediate hybrid q_loc demotion handoff",
        "needles": ["hybrid map constructed, exact local silence not derived", OUTPUT_DOC.name, "reduced GK action owner"],
    },
    "732_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_732_VALIDATION.csv",
        "role": "prior validation gate",
        "needles": ["V732_12_next_target_selected", OUTPUT_DOC.name, "V732_15_formalization_workbench_untouched"],
    },
    "732_factor": {
        "path": RESIDUALS / "P8_Y5_R10_732_GAMMA_KHAT_QLOC_FACTORISATION_TEST.csv",
        "role": "current Gamma/Khat/q_loc factorisation target",
        "needles": ["HFT732_2_Gamma_Khat_q_loc", "vertical_blind_condition_written_exact_zero_not_derived", "false"],
    },
    "732_exactness": {
        "path": RESIDUALS / "P8_Y5_R10_732_QLOC_EXACTNESS_OR_RESIDUAL_GATE.csv",
        "role": "current exactness/residual fork",
        "needles": ["QEG732_2_Ward_owner_gate", "not_for_current_MTS", "false"],
    },
    "732_demotion": {
        "path": RESIDUALS / "P8_Y5_R10_732_DEMOTION_GATE.csv",
        "role": "current demotion routing",
        "needles": ["DR732_C_observed_reduced_residual", "promoted_as_honest_fallback", "false"],
    },
    "597_doc": {
        "path": POST_CHECKPOINT / "597-Y5-R10-reduced-GK-action-owner-or-q_loc-residual-runner.md",
        "role": "older reduced GK owner / q_loc runner checkpoint",
        "needles": ["reduced GK owner route", "q_loc residual runner", "Y5/Y6"],
    },
    "596_doc": {
        "path": POST_CHECKPOINT / "596-Y5-R10-test-Gamma-Khat-qloc-factor-through-pi-or-demote.md",
        "role": "older pullback lemma and exactness demotion checkpoint",
        "needles": ["q_loc being a quotient pullback does not imply q_loc=0", "Ward owner", "observed reduced residual"],
    },
    "514_doc": {
        "path": POST_CHECKPOINT / "514-construct-GK-stress-action-or-residual-bound.md",
        "role": "GK stress action candidate",
        "needles": ["S_GK = - integral sqrt(-g) Gamma_eff", "K_hat = metric response", "residual branch retained"],
    },
    "515_doc": {
        "path": POST_CHECKPOINT / "515-match-Gamma-eff-Khat-to-metric-response-action.md",
        "role": "current symbol-match failure audit",
        "needles": ["No current corpus source proves", "Gamma_eff is a covariant scalar action density", "K_hat is the metric variation"],
    },
    "516_doc": {
        "path": POST_CHECKPOINT / "516-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner.md",
        "role": "Gamma owner candidate / q_loc bound runner spec",
        "needles": ["response doublets", "Y5/Y6", "q_loc residual-bound runner"],
    },
    "518_doc": {
        "path": POST_CHECKPOINT / "518-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
        "role": "Y5 source-normalization owner or bound implementation",
        "needles": ["mu_obs", "Y5 source-normalization", "q_loc_projection"],
    },
    "513_doc": {
        "path": POST_CHECKPOINT / "513-Gamma-Khat-q_loc-first-variation-or-demotion.md",
        "role": "q_loc stress-divergence identity",
        "needles": ["q_loc^nu = P_loc nabla_mu T_GK", "conditional_derivation_route", "not_supplied"],
    },
}


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def text_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def prior_validation_clean(path: Path) -> bool:
    rows = read_csv(path)
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def source_path_string(*keys: str) -> str:
    return ";".join(str(SOURCES[key]["path"]) for key in keys)


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(POST_CHECKPOINT)).replace("\\", "/")
    except ValueError:
        return str(path)


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        cells = []
        for field in fields:
            value = str(row.get(field, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime)
        if modified > CUTOFF:
            count += 1
    return count


def under_post_checkpoint(paths: list[Path]) -> bool:
    root = POST_CHECKPOINT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root)
        except ValueError:
            return False
    return True


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": key,
            "path": str(info["path"]),
            "exists": bool_text(info["path"].exists()),
            "needle_check": bool_text(text_contains(info["path"], info["needles"])),
            "role": info["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for key, info in SOURCES.items()
    ]


def make_owner_attempt(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "owner_id": "RGA733_A_hybrid_reduced_scalar_density_owner",
            "candidate": "S_GK^hyb[Q_obs^hybrid] = - integral_M sqrt(-g_obs) gamma(g_obs,Phi_red,D Phi_red,topological data) + integral_boundary B_GK",
            "owned_objects": "Gamma_eff=gamma; K_hat=metric response K_gamma; T_GK=gamma g_obs-K_gamma",
            "would_derive": "Gamma/Khat/q_loc are observed reduced objects and representative-X is not a hidden local source",
            "blocker": "current corpus has no actual Gamma_eff scalar-density definition and no K_hat metric-response match",
            "current_status": "contract_written_not_matched",
            "valid_for_claim": "false",
            "source_paths": source_path_string("732_doc", "514_doc", "515_doc"),
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "RGA733_B_response_doublet_density",
            "candidate": "gamma = gamma0 + 1/2 M_AB(g_obs,R_even,D) Z^A Z^B + O(Z^4)",
            "owned_objects": "exchange-odd residual doublets Z^A with formal double-zero at Z=0",
            "would_derive": "F_1=0 for auxiliary response variables and positive-operator/no-hair route if Z is physical and source-free",
            "blocker": "Y5 source normalization, Y6 extra stress, PPN lock, and boundary response are not killed by parity alone",
            "current_status": "formal_candidate_Y5_Y6_blocked",
            "valid_for_claim": "false",
            "source_paths": source_path_string("516_doc", "518_doc", "597_doc"),
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "RGA733_C_positive_auxiliary_nohair",
            "candidate": "gamma = V(Phi_red) + 1/2 G_AB(Phi_red) nabla Phi_red^A nabla Phi_red^B with positive local operator",
            "owned_objects": "source-free auxiliary reduced fields Phi_red",
            "would_derive": "E_A=0 plus positive boundary conditions force Phi_red=Phi0 and q_loc=0 on compact local vacuum",
            "blocker": "source-free Euler equations, no-marker theorem, and no-boundary/no-flux conditions are not derived for current MTS",
            "current_status": "candidate_not_component_locked",
            "valid_for_claim": "false",
            "source_paths": source_path_string("514_doc", "516_doc", "732_doc"),
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "RGA733_D_exact_topological_improvement",
            "candidate": "T_GK=dB_GK or an improvement stress whose compact local flux is zero",
            "owned_objects": "exact/improvement stress and fixed boundary reference",
            "would_derive": "bulk q_loc zero without a propagating field",
            "blocker": "boundary/source-measure flux, corner symplectic flux, and ADM/reference subtraction remain open",
            "current_status": "boundary_risk_open",
            "valid_for_claim": "false",
            "source_paths": source_path_string("514_doc", "732_doc"),
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "RGA733_E_hybrid_residual_runner",
            "candidate": "no owner accepted for current claim; retain q_loc as an observed reduced residual on Q_obs^hybrid",
            "owned_objects": "runner rows for compact-shell, Y5 source normalization, PPN tail, R10/R11 operator, boundary flux, and q_loc projection",
            "would_derive": "nothing by theorem; instead tests whether the residual is small enough with sourced inputs or derived zero rows",
            "blocker": "numeric/source-backed projection coefficients are not filled yet",
            "current_status": "triggered_for_current_claim",
            "valid_for_claim": "false",
            "source_paths": source_path_string("597_doc", "518_doc", "732_demotion"),
            "generated_utc": generated_utc,
        },
    ]


def make_metric_response(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "step_id": "MRD733_0_define_hybrid_reduced_action",
            "derivation_step": "Choose Q_obs^hybrid=(g_obs,Phi_red,matter readout after variation,boundary reference class) and define S_GK^hyb on Q_obs^hybrid only.",
            "formula": "S_GK^hyb = - int sqrt(-g_obs) gamma[Q_obs^hybrid] + int_boundary B_GK",
            "passes_if": "gamma has units, covariance, and no representative marker dependence",
            "current_status": "formal_definition_available",
            "valid_for_claim": "false",
            "source_paths": source_path_string("732_doc", "514_doc"),
            "generated_utc": generated_utc,
        },
        {
            "step_id": "MRD733_1_metric_response",
            "derivation_step": "Define K_hat by metric response rather than independently.",
            "formula": "K_hat^{mu nu} := K_gamma^{mu nu} under the fixed 514 convention, so T_GK^{mu nu}=gamma g_obs^{mu nu}-K_gamma^{mu nu}",
            "passes_if": "existing K_hat tensor structure equals this variation including derivative and boundary terms",
            "current_status": "definition_possible_existing_match_failed",
            "valid_for_claim": "false",
            "source_paths": source_path_string("514_doc", "515_doc"),
            "generated_utc": generated_utc,
        },
        {
            "step_id": "MRD733_2_representative_vertical_blindness",
            "derivation_step": "Because S_GK^hyb is a functional of Q_obs^hybrid, v_X^rep cannot vary it if d pi_h(v_X^rep)=0.",
            "formula": "delta_X S_GK^hyb = dS_GK^hyb[d pi_h(v_X^rep)] = 0",
            "passes_if": "Gamma_eff, K_hat, P_loc, and boundary reference all factor through Q_obs^hybrid",
            "current_status": "conditional_pass",
            "valid_for_claim": "false",
            "source_paths": source_path_string("732_doc"),
            "generated_utc": generated_utc,
        },
        {
            "step_id": "MRD733_3_reduced_Ward_identity",
            "derivation_step": "Diffeomorphism invariance of the reduced action controls divergence of T_GK.",
            "formula": "nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi_red^A + boundary_flux^nu",
            "passes_if": "E_A=0 in compact local vacuum and boundary_flux=0 after fixed reference subtraction",
            "current_status": "conditional_only",
            "valid_for_claim": "false",
            "source_paths": source_path_string("513_doc", "596_doc"),
            "generated_utc": generated_utc,
        },
        {
            "step_id": "MRD733_4_q_loc_gate",
            "derivation_step": "Project the Ward identity only after ownership is established.",
            "formula": "q_loc^nu=P_loc nabla_mu T_GK^{mu nu}=P_loc(sum_A E_A nabla^nu Phi_A + boundary_flux^nu)",
            "passes_if": "P_loc is parent-owned and does not hide unprojected components",
            "current_status": "projector_ownership_open",
            "valid_for_claim": "false",
            "source_paths": source_path_string("513_doc", "732_doc"),
            "generated_utc": generated_utc,
        },
    ]


def make_ward_zero(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "WZG733_0_current_symbol_match",
            "needed_for_zero": "actual current Gamma_eff and K_hat match gamma and K_gamma on Q_obs^hybrid",
            "status": "fail_for_current_claim",
            "evidence": "515 match audit: no scalar-density owner or K_hat metric response found",
            "fallback": "retain hybrid q_loc residual row",
            "valid_for_claim": "false",
            "source_paths": source_path_string("515_doc", "732_exactness"),
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "WZG733_1_Euler_source_free",
            "needed_for_zero": "reduced fields entering gamma obey E_A=0 in compact local vacuum",
            "status": "not_derived",
            "evidence": "516/517/518 keep Y5 and Y6 source ledgers active",
            "fallback": "score source-normalization and extra-stress residual components",
            "valid_for_claim": "false",
            "source_paths": source_path_string("516_doc", "518_doc"),
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "WZG733_2_double_zero",
            "needed_for_zero": "T_GK(Phi0) is background-subtracted and first variation vanishes",
            "status": "formal_for_auxiliary_Z_not_physical_lock",
            "evidence": "response-doublet density gives formal F_1=0, but Z=physical PPN/source residual is unproved",
            "fallback": "fill PPN lock or residual vector",
            "valid_for_claim": "false",
            "source_paths": source_path_string("516_doc", "518_doc"),
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "WZG733_3_projector_ownership",
            "needed_for_zero": "P_loc is parent-owned and commutes with local/readout limit",
            "status": "open",
            "evidence": "513/514/596/732 keep P_loc ownership open",
            "fallback": "carry full unprojected residual or derive projector algebra",
            "valid_for_claim": "false",
            "source_paths": source_path_string("513_doc", "514_doc", "732_doc"),
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "WZG733_4_boundary_no_flux",
            "needed_for_zero": "metric response and integrations by parts have no compact local source/mass flux",
            "status": "open",
            "evidence": "boundary/source-measure flux repeatedly retained as active risk",
            "fallback": "compact-shell q_loc/source-measure bound",
            "valid_for_claim": "false",
            "source_paths": source_path_string("732_doc", "597_doc"),
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "WZG733_5_Y5_source_normalization",
            "needed_for_zero": "measured GM/source strength equals one parent EH/Hilbert source charge with no extra projection",
            "status": "hard_blocker_active",
            "evidence": "518 writes owner theorem but marks all premises not parent-derived",
            "fallback": "Y5 source-normalization bound runner",
            "valid_for_claim": "false",
            "source_paths": source_path_string("518_doc"),
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "WZG733_6_Y6_extra_stress",
            "needed_for_zero": "extra stress is topological/invisible or below PPN/operator locks",
            "status": "hard_blocker_active",
            "evidence": "old 597/517 trail keeps Y6 stress/Bianchi debt active",
            "fallback": "T_extra/PPN/operator residual vector",
            "valid_for_claim": "false",
            "source_paths": source_path_string("597_doc", "516_doc"),
            "generated_utc": generated_utc,
        },
    ]


def make_residual_runner(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "HQR733_0_compact_shell_budget",
            "quantity": "max |P_loc d_rel J_rel| or q_loc compact leakage proxy",
            "current_input": "7.432631961576971e-06 dimensionless proxy from old compact-shell route",
            "needed_to_score": "map proxy into PPN/source-normalization units and sign convention",
            "acceptance_gate": "cannot be claim-valid until mapping is sourced",
            "status": "queued_not_scored",
            "valid_for_claim": "false",
            "source_paths": source_path_string("597_doc"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "HQR733_1_source_normalization_Y5",
            "quantity": "q_loc projection into measured-GM/source-normalization channel",
            "current_input": "Y5/q_loc source-normalization rows exist but are missing/not_scored",
            "needed_to_score": "C_qmu projection operator, units, and source-backed/theorem-zero values for Gdot, Mdot, radial, species, range, frame, beta, PPN",
            "acceptance_gate": "each channel derived zero or below official local row locks",
            "status": "queued_not_scored",
            "valid_for_claim": "false",
            "source_paths": source_path_string("518_doc", "597_doc"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "HQR733_2_boundary_pressure_alpha3",
            "quantity": "preferred-frame/momentum-flux equivalent from boundary or corner flux",
            "current_input": "alpha3 lock 4e-20 where applicable",
            "needed_to_score": "coefficient from q_loc/boundary flux to alpha3-equivalent row",
            "acceptance_gate": "source-backed coefficient below alpha3 lock or derived boundary zero",
            "status": "queued_not_scored",
            "valid_for_claim": "false",
            "source_paths": source_path_string("518_doc", "732_doc"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "HQR733_3_PPN_metric_tail",
            "quantity": "Delta_PPN={gamma-1,beta-1,alpha_i,xi,zeta_i}_source",
            "current_input": "template only; weak-field map not filled",
            "needed_to_score": "linearized metric solution sourced by hybrid q_loc and source-normalization split",
            "acceptance_gate": "all PPN components below bounds or theorem-zero",
            "status": "queued_not_scored",
            "valid_for_claim": "false",
            "source_paths": source_path_string("518_doc", "597_doc"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "HQR733_4_R10_range_tail",
            "quantity": "alpha(lambda) or range-dependent source strength",
            "current_input": "real bound curve infrastructure exists but q_loc-to-alpha coefficient is missing",
            "needed_to_score": "lambda, alpha coefficient, source path, and bound-curve comparison",
            "acceptance_gate": "abs(alpha_predicted)<=alpha_bound with source-backed rows",
            "status": "queued_not_scored",
            "valid_for_claim": "false",
            "source_paths": source_path_string("597_doc", "732_demotion"),
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "HQR733_5_R11_operator_vector",
            "quantity": "non-EH/operator/source-normalization coefficient vector",
            "current_input": "symbolic until operator family and normalization are filled",
            "needed_to_score": "operator basis, units, weak-field normalization, and bound comparison",
            "acceptance_gate": "operator vector below R11/local locks or derived zero",
            "status": "queued_not_scored",
            "valid_for_claim": "false",
            "source_paths": source_path_string("597_doc", "518_doc"),
            "generated_utc": generated_utc,
        },
    ]


def make_fork(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "fork_id": "F733_A_owner_acceptance",
            "condition": "Gamma_eff scalar density, K_hat metric response, Ward zero, Y5/Y6 closure, boundary no-flux, and P_loc ownership all pass",
            "decision": "promote reduced GK owner to theorem candidate for q_loc zero only",
            "current_status": "not_triggered",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "F733_B_owner_partial",
            "condition": "reduced owner can be defined but actual current Gamma/Khat symbol match is not proven",
            "decision": "keep owner as contract and trigger hybrid residual runner",
            "current_status": "triggered",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fork_id": "F733_C_owner_failure",
            "condition": "Gamma/Khat cannot be reduced-action objects or P_loc/readout/boundary smuggle residuals",
            "decision": "demote q_loc route fully to residual/edge/diffeo-current backup",
            "current_status": "not_yet_final",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_decision(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D733_0_reduced_owner_contract_written",
            "decision": "write hybrid reduced S_GK owner theorem-contract on Q_obs^hybrid",
            "meaning": "there is a legitimate route to q_loc=0 if Gamma/Khat are reduced action/metric-response objects",
            "claim_status": "contract_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D733_1_current_match_failed",
            "decision": "do not accept owner for current MTS claim",
            "meaning": "515/732 still block actual Gamma_eff scalar-density and K_hat metric-response match",
            "claim_status": "q_loc_zero_false_for_current_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D733_2_hybrid_residual_runner_triggered",
            "decision": "queue hybrid q_loc residual runner rows",
            "meaning": "next work must either derive a first zero row or fill source-backed numeric residual inputs",
            "claim_status": "runner_ready_not_scored",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_route_update(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU733_0_allowed",
            "allowed_after_733": "cite reduced S_GK as a theorem contract only",
            "forbidden_after_733": "claim current MTS has derived q_loc=0",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU733_1_allowed",
            "allowed_after_733": "use hybrid residual runner rows for q_loc/source-normalization/PPN/R10/R11 channels",
            "forbidden_after_733": "call queued residual rows scored or below bounds",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU733_2_allowed",
            "allowed_after_733": "try to derive one first zero row before filling numeric coefficients",
            "forbidden_after_733": "hide Y5/Y6 or boundary flux behind the reduced-action contract",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def make_summary(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "hybrid reduced GK owner contract is written but current Gamma/Khat symbol match fails",
            "hard_blocker": "Y5/Y6, P_loc ownership, K_hat metric response, source-free Euler equations, and boundary no-flux remain open",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_generated_claim_false(paths: list[Path]) -> bool:
    for path in paths:
        rows = read_csv(path)
        if not rows or "valid_for_claim" not in rows[0]:
            continue
        if any(row.get("valid_for_claim", "").lower() != "false" for row in rows):
            return False
    return True


def make_validation(
    source_register: list[dict[str, Any]],
    owner_rows: list[dict[str, Any]],
    metric_rows: list[dict[str, Any]],
    ward_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    fork_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    output_paths: list[Path],
) -> list[dict[str, Any]]:
    generated_tables = [
        SOURCE_REGISTER_PATH,
        OWNER_ATTEMPT_PATH,
        METRIC_RESPONSE_PATH,
        WARD_ZERO_PATH,
        RESIDUAL_RUNNER_PATH,
        OWNER_RUNNER_FORK_PATH,
        DECISION_PATH,
        ROUTE_UPDATE_PATH,
        SUMMARY_PATH,
    ]
    source_paths_ok = all(row["exists"] == "true" for row in source_register)
    source_needles_ok = all(row["needle_check"] == "true" for row in source_register)
    prior_clean = prior_validation_clean(SOURCES["732_validation"]["path"])
    selected_733 = text_contains(SOURCES["732_validation"]["path"], ["V732_12_next_target_selected", OUTPUT_DOC.name])
    owner_contract = any(row["owner_id"] == "RGA733_A_hybrid_reduced_scalar_density_owner" for row in owner_rows)
    metric_contract = any(row["step_id"] == "MRD733_1_metric_response" for row in metric_rows)
    match_failure = any(row["gate_id"] == "WZG733_0_current_symbol_match" and row["status"] == "fail_for_current_claim" for row in ward_rows)
    y5_y6 = any(row["gate_id"] == "WZG733_5_Y5_source_normalization" for row in ward_rows) and any(
        row["gate_id"] == "WZG733_6_Y6_extra_stress" for row in ward_rows
    )
    runner_triggered = any(row["owner_id"] == "RGA733_E_hybrid_residual_runner" and row["current_status"] == "triggered_for_current_claim" for row in owner_rows)
    runner_has_channels = {"HQR733_1_source_normalization_Y5", "HQR733_3_PPN_metric_tail", "HQR733_4_R10_range_tail"}.issubset(
        {row["runner_id"] for row in runner_rows}
    )
    fork_triggered = any(row["fork_id"] == "F733_B_owner_partial" and row["current_status"] == "triggered" for row in fork_rows)
    next_selected = all(row["next_target"] == NEXT_TARGET for row in decision_rows)
    claim_false = all_generated_claim_false(generated_tables)
    outputs_scoped = under_post_checkpoint(output_paths)
    formalization_count = formalization_changed_after_cutoff()
    return [
        {"check_id": "V733_0_source_paths_exist", "result": "pass" if source_paths_ok else "fail", "detail": f"source_rows={len(source_register)}"},
        {"check_id": "V733_1_source_needles_present", "result": "pass" if source_needles_ok else "fail", "detail": "all source files contain expected evidence needles"},
        {"check_id": "V733_2_prior_732_clean", "result": "pass" if prior_clean else "fail", "detail": "732 validation has no failures"},
        {"check_id": "V733_3_732_selected_733", "result": "pass" if selected_733 else "fail", "detail": "732 selected this checkpoint"},
        {"check_id": "V733_4_reduced_owner_contract_present", "result": "pass" if owner_contract else "fail", "detail": f"owner_rows={len(owner_rows)}"},
        {"check_id": "V733_5_metric_response_derivation_present", "result": "pass" if metric_contract else "fail", "detail": f"metric_rows={len(metric_rows)}"},
        {"check_id": "V733_6_current_match_failure_retained", "result": "pass" if match_failure else "fail", "detail": "Gamma/Khat match still fails for current claim"},
        {"check_id": "V733_7_Y5_Y6_retained", "result": "pass" if y5_y6 else "fail", "detail": "Y5 source normalization and Y6 extra stress remain blockers"},
        {"check_id": "V733_8_residual_runner_triggered", "result": "pass" if runner_triggered and runner_has_channels and fork_triggered else "fail", "detail": f"runner_rows={len(runner_rows)};triggered={runner_triggered};channels={runner_has_channels};fork={fork_triggered}"},
        {"check_id": "V733_9_next_target_selected", "result": "pass" if next_selected else "fail", "detail": NEXT_TARGET},
        {"check_id": "V733_10_no_claim_rows_promoted", "result": "pass" if claim_false else "fail", "detail": "all generated rows with valid_for_claim remain false"},
        {"check_id": "V733_11_outputs_scoped", "result": "pass" if outputs_scoped else "fail", "detail": "all outputs under post-checkpoint-work"},
        {"check_id": "V733_12_formalization_workbench_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={formalization_count}"},
        {"check_id": "V733_13_no_local_arena_claim", "result": "pass", "detail": "R10/WEP/PPN/Newton/local-GR claims remain blocked"},
        {"check_id": "V733_14_validation_rows_ready", "result": "pass", "detail": "validation table constructed"},
    ]


def write_markdown(
    generated_utc: str,
    run_root: Path,
    source_register: list[dict[str, Any]],
    owner_rows: list[dict[str, Any]],
    metric_rows: list[dict[str, Any]],
    ward_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    fork_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    text = f"""# 733 - Y5 R10 Reduced GK Action Owner Or Hybrid q_loc Residual Runner

## Summary

This checkpoint tries the reduced `GK` owner demanded by 732.

```text
S_GK^hyb[Q_obs^hybrid] = - int sqrt(-g_obs) gamma[Q_obs^hybrid] + int_boundary B_GK
K_hat := metric response of gamma
T_GK^{{mu nu}} = gamma g_obs^{{mu nu}} - K_hat^{{mu nu}}
q_loc^nu = P_loc nabla_mu T_GK^{{mu nu}}
```

Current verdict: **owner contract written, current symbol match failed**. The reduced-action door is coherent, but current MTS still does not prove `Gamma_eff` is the scalar density, `K_hat` is its metric response, `P_loc` is parent-owned, or Y5/Y6 and boundary no-flux close. Therefore hybrid `q_loc` is queued as an observed reduced residual runner.

| Field | Value |
| --- | --- |
| Generated UTC | `{generated_utc}` |
| Claim status | private/nonclaim checkpoint |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |
| Run root | `{relative(run_root)}` |

## Reduced GK Action Owner Attempt

{markdown_table(owner_rows, ["owner_id", "candidate", "owned_objects", "would_derive", "blocker", "current_status", "valid_for_claim"])}

## Metric Response Derivation

{markdown_table(metric_rows, ["step_id", "derivation_step", "formula", "passes_if", "current_status", "valid_for_claim"])}

## Ward Zero Gate

{markdown_table(ward_rows, ["gate_id", "needed_for_zero", "status", "evidence", "fallback", "valid_for_claim"])}

## Hybrid q_loc Residual Runner Queue

{markdown_table(runner_rows, ["runner_id", "quantity", "current_input", "needed_to_score", "acceptance_gate", "status", "valid_for_claim"])}

## Owner Or Runner Fork

{markdown_table(fork_rows, ["fork_id", "condition", "decision", "current_status", "next_action", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decision_rows, ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(route_rows, ["route_id", "allowed_after_733", "forbidden_after_733", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_register, ["source_id", "path", "exists", "needle_check", "role"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Practical Read

This is not bad; it is the accounting getting sharper. We now have a clean reduced-action door, but the current symbols have not walked through it. Until they do, `q_loc` is not a mystical local-GR proof. It is a reduced observed residual vector that we either kill one row at a time or score against local gates.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_root = RUNS / f"{stamp}-Y5-R10-reduced-GK-owner-hybrid-qloc-runner"
    run_root.mkdir(parents=True, exist_ok=True)

    source_register = make_source_register(generated_utc)
    owner_rows = make_owner_attempt(generated_utc)
    metric_rows = make_metric_response(generated_utc)
    ward_rows = make_ward_zero(generated_utc)
    runner_rows = make_residual_runner(generated_utc)
    fork_rows = make_fork(generated_utc)
    decision_rows = make_decision(generated_utc)
    route_rows = make_route_update(generated_utc)
    summary_rows = make_summary(generated_utc)

    output_paths = [
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        OWNER_ATTEMPT_PATH,
        METRIC_RESPONSE_PATH,
        WARD_ZERO_PATH,
        RESIDUAL_RUNNER_PATH,
        OWNER_RUNNER_FORK_PATH,
        DECISION_PATH,
        ROUTE_UPDATE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
        run_root / "status.json",
        run_root / "COMPLETE.marker",
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(
        OWNER_ATTEMPT_PATH,
        owner_rows,
        ["owner_id", "candidate", "owned_objects", "would_derive", "blocker", "current_status", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        METRIC_RESPONSE_PATH,
        metric_rows,
        ["step_id", "derivation_step", "formula", "passes_if", "current_status", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        WARD_ZERO_PATH,
        ward_rows,
        ["gate_id", "needed_for_zero", "status", "evidence", "fallback", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUAL_RUNNER_PATH,
        runner_rows,
        ["runner_id", "quantity", "current_input", "needed_to_score", "acceptance_gate", "status", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        OWNER_RUNNER_FORK_PATH,
        fork_rows,
        ["fork_id", "condition", "decision", "current_status", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        DECISION_PATH,
        decision_rows,
        ["decision_id", "decision", "meaning", "claim_status", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        ROUTE_UPDATE_PATH,
        route_rows,
        ["route_id", "allowed_after_733", "forbidden_after_733", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"],
    )

    validation_rows = make_validation(source_register, owner_rows, metric_rows, ward_rows, runner_rows, fork_rows, decision_rows, output_paths)
    write_csv(VALIDATION_PATH, validation_rows, ["check_id", "result", "detail"])

    write_markdown(
        generated_utc,
        run_root,
        source_register,
        owner_rows,
        metric_rows,
        ward_rows,
        runner_rows,
        fork_rows,
        decision_rows,
        route_rows,
        summary_rows,
        validation_rows,
    )

    status_payload = {
        "generated_utc": generated_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
        "doc": str(OUTPUT_DOC),
        "validation": str(VALIDATION_PATH),
        "all_validation_pass": all(row["result"] == "pass" for row in validation_rows),
    }
    (run_root / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    (run_root / "COMPLETE.marker").write_text("complete\n", encoding="utf-8")
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()

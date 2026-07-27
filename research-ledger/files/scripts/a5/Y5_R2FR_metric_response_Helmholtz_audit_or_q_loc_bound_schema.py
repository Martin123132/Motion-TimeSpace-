from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
QUARANTINE = MICROSCOPE / "quarantine" / "1618"
INPUT_1618 = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1618-Y5-R2FR-metric-response-Helmholtz-audit-or-q_loc-bound-schema.md"

SOURCE_FILES = {
    "1617_doc": ROOT / "1617-Y5-R2FR-q_loc-action-reopen-pack-or-residual-bound-roadmap.md",
    "1617_validation": OUT / "P8_Y5_BRR545_1617_VALIDATION.csv",
    "1617_next": OUT / "P8_Y5_PARENT_QLOC_1617_NEXT_TARGET.csv",
    "1617_reopen_pack": OUT / "P8_Y5_PARENT_QLOC_1617_QLOC_ACTION_REOPEN_PACK.csv",
    "1617_certificate": OUT / "P8_Y5_PARENT_QLOC_1617_CERTIFICATE_STATUS_LEDGER.csv",
    "513_rewrite": OUT / "P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv",
    "513_contract": OUT / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
    "514_contract": OUT / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
    "514_candidates": OUT / "P8_GK_STRESS_ACTION_CANDIDATES.csv",
    "514_fixed_point": OUT / "P8_GK_LOCAL_FIXED_POINT_GATES.csv",
    "515_match": OUT / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
    "515_pass_fail": OUT / "P8_GK_METRIC_RESPONSE_PASS_FAIL.csv",
    "516_owner": OUT / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
    "1010_theorem": OUT / "P8_Y5_R10_1010_THEOREM_ATTEMPT.csv",
    "1010_schema": OUT / "P8_Y5_R10_1010_HELMHOLTZ_ACTION_SCHEMA.csv",
    "1011_doublet": OUT / "P8_Y5_R10_1011_RESPONSED_DOUBLET_THEOREM_ATTEMPT.csv",
    "1011_bounds": OUT / "P8_Y5_R10_1011_QLOC_BOUND_FILL_ROWS.csv",
}

NEEDLES = {
    "1617_doc": ["metric-response/Helmholtz is the fastest sharp test", "VAL1617_OVERALL"],
    "1617_validation": ["VAL1617_OVERALL", "PASS"],
    "1617_next": ["1618-Y5-R2FR-metric-response-Helmholtz-audit-or-q_loc-bound-schema.md", "metric-response/Helmholtz"],
    "1617_reopen_pack": ["QRA1617_2_metric_response", "MISSING_METRIC_RESPONSE_MATCH"],
    "1617_certificate": ["CERT1617_3_helmholtz", "OPEN_NOT_CHECKED"],
    "513_rewrite": ["SR513_0_define_extra_stress", "algebraic_identity"],
    "513_contract": ["GK513_0_action_existence", "not_supplied"],
    "514_contract": ["MR514_1_Khat_metric_response", "MR514_5_double_zero"],
    "514_candidates": ["GK514_A_metric_response_scalar_density", "fallback_required"],
    "514_fixed_point": ["FG514_2_metric_response_identity", "FG514_3_double_zero"],
    "515_match": ["MA515_1_Khat_metric_response", "fail_for_current_claim"],
    "515_pass_fail": ["Gamma", "fail"],
    "516_owner": ["GO516_A_response_doublet_quadratic_density", "best_candidate_not_current_MTS_derived"],
    "1010_theorem": ["GKT1010_2_Helmholtz_integrability", "not_checked_current_claim"],
    "1010_schema": ["HGS1010_2_Helmholtz", "second_variation_symmetry"],
    "1011_doublet": ["RDT1011_7_verdict", "fail_current_claim"],
    "1011_bounds": ["QBF1011_0_compact_shell_budget", "anchor_proxy_not_claim_curve"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1618_SOURCE_REGISTER.csv"
METRIC_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1618_METRIC_RESPONSE_AUDIT.csv"
HELMHOLTZ_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1618_HELMHOLTZ_AUDIT.csv"
CANDIDATE_DECISION = OUT / "P8_Y5_PARENT_QLOC_1618_ACTION_CANDIDATE_DECISION_MATRIX.csv"
QLOC_BOUND_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_1618_QLOC_BOUND_SCHEMA_UPGRADE.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1618_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1618_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1618_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1618_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1618_VALIDATION.csv"

COPY_TARGETS = {
    METRIC_AUDIT: [
        QUARANTINE / "METRIC_RESPONSE_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_metric_response_audit_nonclaim_1618.csv",
    ],
    HELMHOLTZ_AUDIT: [
        QUARANTINE / "HELMHOLTZ_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_helmholtz_audit_nonclaim_1618.csv",
    ],
    QLOC_BOUND_SCHEMA: [
        QUARANTINE / "QLOC_BOUND_SCHEMA_UPGRADE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_q_loc_bound_schema_upgrade_nonclaim_1618.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1618.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1618.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1618_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1618_metric_response_helmholtz_gate_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def metric_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "MRG1618_0_scalar_density_owner",
            "Gamma_eff must be an explicit covariant scalar density in S_GK with fields, metric dependence, units, and no fitted readout selector.",
            "MA515_0 and HGS1010_0 say the current corpus has Gamma_eff as route/readout/relaxation/boundary-charge symbol, not as a signed scalar-density owner.",
            "FAIL_CURRENT_CLAIM",
            "Without a parent density, no Hilbert stress can be varied; Gamma_eff remains an independent residual symbol.",
        ),
        (
            "MRG1618_1_Khat_metric_variation",
            "K_hat^{mu nu} must equal the metric response of sqrt(-g) Gamma_eff under one fixed sign/volume convention.",
            "MA515_1, GKT1010_1, and MR514_1 all mark this as required but not matched to current symbols.",
            "FAIL_CURRENT_CLAIM",
            "Gamma_eff and K_hat are still two knobs, so q_loc cannot be proved zero by action ownership.",
        ),
        (
            "MRG1618_2_volume_sign_convention",
            "The volume term in delta[sqrt(-g) Gamma_eff] must be separated so Gamma_eff g^{mu nu}-K_hat^{mu nu} is not double-counted.",
            "No existing row fixes the sign and volume convention for the candidate S_GK stress.",
            "MISSING_PARENT_CONVENTION",
            "Even a later candidate action cannot be compared to K_hat until this convention is declared.",
        ),
        (
            "MRG1618_3_derivative_boundary_terms",
            "If Gamma_eff depends on derivatives, all integrations by parts and boundary/improvement stresses must be accounted for.",
            "MA515_5 and FG514_4 keep boundary/no-flux open.",
            "OPEN_BOUNDARY_RESPONSE",
            "A bulk metric-response match can still leak local force or source mass through worldtube/boundary terms.",
        ),
        (
            "MRG1618_4_Ward_identity",
            "Diffeomorphism invariance of S_GK should give nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A plus controlled boundary terms.",
            "SR513_2 gives the conditional route, but MA515_3 says the specific S_GK Ward identity is not matched.",
            "CONDITIONAL_ONLY",
            "The identity is structurally plausible but not yet a proof for this MTS sector.",
        ),
        (
            "MRG1618_5_fixed_point_double_zero",
            "After Gamma0/background subtraction, T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0 must hold.",
            "GKT1010_4, MA515_4, and FG514_3 keep the double-zero unproved.",
            "FAIL_CURRENT_CLAIM",
            "Linear PPN/source-normalization leakage remains possible.",
        ),
        (
            "MRG1618_6_units_normalization",
            "Gamma_eff, K_hat, q_loc, and observable projections need stress-density/source-normalization units.",
            "MA515_6 says current appearances are symbolic and not unit-normalized.",
            "FAIL_CURRENT_CLAIM",
            "No local bound or residual vector can be claim-ready until units and normalization are declared.",
        ),
        (
            "MRG1618_7_verdict",
            "The action-ownership route is allowed only if MRG1618_0 through MRG1618_6 pass together.",
            "At least scalar-density owner, metric variation, convention, double-zero, and units fail or remain open.",
            "METRIC_RESPONSE_GATE_FAILS_CURRENT_CLAIM",
            "Do not reopen local GR; move to explicit S_GK construction or nonclaim q_loc bounds.",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "required_clause": required_clause,
            "current_evidence": evidence,
            "result": result,
            "effect": effect,
            "source_anchors": "P8_GK_METRIC_RESPONSE_CONTRACT.csv; P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv; P8_Y5_R10_1010_THEOREM_ATTEMPT.csv",
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, required_clause, evidence, result, effect in rows
    ]


def helmholtz_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "HLA1618_0_exact_condition",
            "For a proposed T_GK to be variational, the second metric variation operator must be symmetric under exchange of metric variations, up to boundary/gauge terms.",
            "delta[sqrt(-g)T_GK^{mu nu}(x)]/delta g_{alpha beta}(y) equals the adjoint-exchanged variation after boundary/gauge handling.",
            "CONDITION_RECORDED_NOT_CHECKED",
            "This is the right mathematical test, but it needs an explicit functional form.",
        ),
        (
            "HLA1618_1_functional_input",
            "S_GK or Gamma_eff(g,Phi,nabla Phi,D,...) must be supplied before the second variation is calculable.",
            "Current inputs give candidate templates, not a source-signed functional.",
            "MISSING_EXPLICIT_FUNCTIONAL",
            "No real Helmholtz calculation can be performed yet.",
        ),
        (
            "HLA1618_2_Khat_operator_input",
            "K_hat must have a tensor/operator expression rather than just an identity slot in q_loc.",
            "MA515_1 says K_hat metric-response expression is absent.",
            "MISSING_KHAT_OPERATOR",
            "The second variation cannot be compared to current K_hat structure.",
        ),
        (
            "HLA1618_3_boundary_symmetry",
            "Boundary and improvement terms must make the variational operator self-adjoint on the local compact branch.",
            "Boundary/no-flux remains open in MA515_5 and FG514_4.",
            "OPEN_BOUNDARY_SYMMETRY",
            "A formal bulk action could still fail local source-measure tests.",
        ),
        (
            "HLA1618_4_variable_domain",
            "The field domain, gauge fixing, projector P_loc, and allowed variations must be declared.",
            "FG514_5 keeps P_loc parent ownership open.",
            "MISSING_VARIATION_DOMAIN",
            "Helmholtz symmetry is not meaningful until the domain of variations is fixed.",
        ),
        (
            "HLA1618_5_verdict",
            "Run the Helmholtz test only after HLA1618_1 through HLA1618_4 are supplied.",
            "The corpus does not yet supply a calculable operator pair.",
            "HELMHOLTZ_NOT_RUNNABLE_INPUTS_MISSING",
            "This is not a no-go theorem; it is a strict no-claim result.",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "required_clause": required_clause,
            "mathematical_form": mathematical_form,
            "result": result,
            "effect": effect,
            "source_anchors": "P8_Y5_R10_1010_HELMHOLTZ_ACTION_SCHEMA.csv; P8_Y5_R10_1010_THEOREM_ATTEMPT.csv; P8_GK_LOCAL_FIXED_POINT_GATES.csv",
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for audit_id, required_clause, mathematical_form, result, effect in rows
    ]


def candidate_decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CAND1618_0_metric_response_density",
            "GK514_A_metric_response_scalar_density",
            "S_GK=-int sqrt(-g) Gamma_eff",
            "best formal route, but current MTS symbol match fails",
            "keep as target contract, not claim",
            "source-signed Gamma_eff and K_hat metric response",
            False,
        ),
        (
            "CAND1618_1_response_doublet_quadratic",
            "GO516_A_response_doublet_quadratic_density",
            "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
            "promising double-zero mechanism, but not current-MTS-derived",
            "combine with positive auxiliary normal form",
            "derive exchange doublets, positive M_AB, and source-current zero",
            True,
        ),
        (
            "CAND1618_2_positive_auxiliary_fields",
            "GO516_B_positive_auxiliary_energy_density",
            "Gamma_eff=V(Phi)+1/2 G_AB nabla Phi^A nabla Phi^B",
            "promising local silence mechanism, but source-current/no-boundary not derived",
            "select as 1619 construction target paired with response doublet",
            "derive local no-hair/silence and match stress to Gamma g-K_hat",
            True,
        ),
        (
            "CAND1618_3_topological_boundary_density",
            "GK514_C/GO516_C_topological_boundary_density",
            "S_GK=int dB_GK or normalized topological density",
            "could kill bulk q_loc, but boundary flux risk is the core problem",
            "defer until boundary charge/unit owner is sharper",
            "prove no local worldtube/source-measure leakage",
            False,
        ),
        (
            "CAND1618_4_residual_branch",
            "GK514_D/GO516_D_residual_bound_runner",
            "no action accepted",
            "required fallback if construction fails",
            "keep nonclaim bound schema live",
            "q_loc profile/operator rows with units and observable maps",
            False,
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "candidate_row": candidate_row,
            "source_candidate": source_candidate,
            "normal_form": normal_form,
            "status_now": status_now,
            "decision": decision,
            "missing_input": missing_input,
            "selected_next": selected_next,
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for candidate_row, source_candidate, normal_form, status_now, decision, missing_input, selected_next in rows
    ]


def qloc_bound_schema_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QBS1618_0_profile",
            "q_loc^nu",
            "MISSING_QLOC_PROFILE_OPERATOR",
            "MISSING_UNITS",
            "MISSING_NORMALIZATION",
            "MISSING_SOURCE_PATH",
            "METRIC_RESPONSE_GATE_FAILS_CURRENT_CLAIM",
            "HELMHOLTZ_NOT_RUNNABLE_INPUTS_MISSING",
            "not_yet_testable",
            "MISSING_BOUND_VALUE",
            "MISSING_BOUND_UNITS",
            "base residual profile row required before PPN/R10/clock/orbital use",
        ),
        (
            "QBS1618_1_PPN_projection",
            "P_loc q_loc^nu -> PPN residual vector",
            "MISSING_PPN_OPERATOR_MAP",
            "PPN_dimensionless_or_acceleration_units_undeclared",
            "MISSING_PPN_NORMALIZATION",
            "MISSING_SOURCE_PATH",
            "blocked",
            "blocked",
            "gamma,beta,alpha_i,xi",
            "MISSING_PPN_BOUND",
            "dimensionless_or_SI_undeclared",
            "no local GR/PPN claim without projection matrix",
        ),
        (
            "QBS1618_2_source_normalization",
            "q_loc^nu -> GM/M_eff/source measure",
            "MISSING_R11_SOURCE_OPERATOR",
            "MISSING_SOURCE_UNITS",
            "MISSING_GM_CONVENTION",
            "MISSING_SOURCE_PATH",
            "blocked",
            "blocked",
            "R11/source-normalization",
            "MISSING_SOURCE_BOUND",
            "fractional_or_SI_undeclared",
            "cannot borrow measured G or measured GM as derivation",
        ),
        (
            "QBS1618_3_clock_orbital_time",
            "time component of q_loc^nu",
            "MISSING_TIME_PROJECTION",
            "yr^-1_or_s^-1_undeclared",
            "MISSING_CLOCK_NORMALIZATION",
            "MISSING_SOURCE_PATH",
            "blocked",
            "blocked",
            "clock/Gdot/GMdot/orbital drift",
            "MISSING_TIME_BOUND",
            "yr^-1_or_s^-1",
            "no clock/orbital pass until projection is sourced",
        ),
        (
            "QBS1618_4_boundary_flux",
            "worldtube/boundary projection",
            "MISSING_BOUNDARY_FLUX_OPERATOR",
            "MISSING_FLUX_UNITS",
            "MISSING_WORLDTUBE_NORMALIZATION",
            "MISSING_SOURCE_PATH",
            "open_boundary_response",
            "open_boundary_symmetry",
            "boundary/no-flux/source measure",
            "MISSING_FLUX_BOUND",
            "stress_flux_units_undeclared",
            "bulk zero is insufficient without no-flux or bound",
        ),
        (
            "QBS1618_5_R10_alpha_bridge",
            "q_loc/coupling tail -> alpha(lambda)",
            "MISSING_ARENA_PROJECTION",
            "dimensionless_alpha_required",
            "MISSING_LAMBDA_NORMALIZATION",
            "MISSING_SOURCE_PATH",
            "blocked",
            "blocked",
            "R10/fifth-force alpha-lambda",
            "MISSING_REAL_BOUND_ROW",
            "dimensionless",
            "R10 remains nonclaim until parent coefficients and real bounds are sourced",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "schema_row_id": row_id,
            "q_loc_component": component,
            "operator_or_profile": operator_or_profile,
            "units": units,
            "normalization": normalization,
            "source_path": source_path,
            "metric_response_status": metric_status,
            "helmholtz_status": helmholtz_status,
            "observable_map": observable_map,
            "bound_value": bound_value,
            "bound_units": bound_units,
            "blocker": blocker,
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for (
            row_id,
            component,
            operator_or_profile,
            units,
            normalization,
            source_path,
            metric_status,
            helmholtz_status,
            observable_map,
            bound_value,
            bound_units,
            blocker,
        ) in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1618_0_sources", "source register and 1617 target imported", "SOURCE_CONTEXT_READY", "all 1618 gates are source-anchored"),
        ("RUN1618_1_metric_response", "Gamma owner/Khat metric variation/units/double-zero fail or remain open", "METRIC_RESPONSE_GATE_FAILS_CURRENT_CLAIM", "action ownership is not accepted"),
        ("RUN1618_2_helmholtz", "no explicit S_GK functional and Khat operator pair", "HELMHOLTZ_NOT_RUNNABLE_INPUTS_MISSING", "do not call this a no-go; require calculable candidate"),
        ("RUN1618_3_bound_schema", "fallback needs strict residual rows", "QLOC_BOUND_SCHEMA_UPGRADED_NONCLAIM", "future tests get units/source/observable gate fields"),
        ("RUN1618_4_local_GR", "metric and Helmholtz gates fail current claim", "DO_NOT_REOPEN_LOCAL_GR", "local GR/Newton recovery remains blocked"),
        ("RUN1618_5_next", "best next route is constructive positive auxiliary/response doublet S_GK", "SELECT_1619_POSITIVE_AUXILIARY_SGK_NORMAL_FORM_OR_QLOC_PROFILE_ROW", "try proof first; profile row if construction fails"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "input_state": input_state,
            "runner_result": result,
            "effect": effect,
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_id, input_state, result, effect in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG1618_0_q_loc_identity", "q_loc as projected stress-divergence residual", "CLOSED_DEFINITION_ONLY", "identity/reclassification from 1617 survives but does not prove zero"),
        ("CG1618_1_SGK_action", "S_GK parent action exists", "BLOCKED", "explicit scalar-density owner missing"),
        ("CG1618_2_metric_response", "K_hat is metric response of Gamma_eff", "BLOCKED", "metric-response match fails current claim"),
        ("CG1618_3_Helmholtz", "T_GK is variational stress", "BLOCKED", "second variation not runnable without explicit functional and operator"),
        ("CG1618_4_double_zero", "F_1=0/local fixed-point double-zero", "BLOCKED", "T_GK(Phi0)=0 and first variation zero not derived"),
        ("CG1618_5_residual_bound", "q_loc residual rows are claim-ready", "BLOCKED", "profile, units, normalization, and observable maps missing"),
        ("CG1618_6_local_GR", "derived local GR/Newton recovery", "BLOCKED", "1616 demotion remains active and 1618 does not reopen it"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1618_0_metric_gate", "METRIC_RESPONSE_GATE_FAILS_CURRENT_CLAIM", "Gamma_eff/K_hat are not yet one parent metric-response object", "construct explicit S_GK or retain residual q_loc"),
        ("DEC1618_1_helmholtz_gate", "HELMHOLTZ_AUDIT_NOT_RUNNABLE_WITHOUT_EXPLICIT_FUNCTIONAL", "no second-variation operator can be checked yet", "do not claim no-go; demand calculable functional"),
        ("DEC1618_2_bound_schema", "QLOC_BOUND_SCHEMA_UPGRADED_NONCLAIM", "fallback branch now has stricter row fields for units/source/observable maps", "fill only with sourced non-placeholder inputs"),
        ("DEC1618_3_no_promotion", "LOCAL_GR_NOT_REOPENED", "metric, Helmholtz, double-zero, boundary, and observable-map gates remain blocked", "keep all local claims private/nonclaim"),
        ("DEC1618_4_next", "NEXT_1619_POSITIVE_AUXILIARY_SGK_NORMAL_FORM_OR_QLOC_PROFILE_ROW", "positive auxiliary/response-doublet route is the most derivation-friendly constructive route", "try proof first; stage q_loc profile if it fails"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1619-Y5-R2FR-positive-auxiliary-SGK-normal-form-or-q_loc-profile-row.md",
            "script": "scripts/Y5_R2FR_positive_auxiliary_SGK_normal_form_or_q_loc_profile_row.py",
            "objective": "try to construct a positive auxiliary/response-doublet S_GK normal form that owns Gamma_eff, K_hat, local silence, and double-zero; if it fails, stage the first strict q_loc profile row",
            "success_condition": "either a calculable parent action candidate is produced with metric-response/Helmholtz inputs, or a nonclaim q_loc profile schema row is made explicit with missing inputs named",
            "do_not": "do not promote local GR, do not use plateau axiom, do not import EH-only stress, do not tune cancellations, do not use measured G/GM as derivation",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for field in ("reopens_local_claim", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if truthy(row.get(field, "")):
                    return False
    return True


def no_formalization_1618() -> bool:
    if not FORMALIZATION.exists():
        return True
    artifact_markers = (
        "1618-Y5",
        "P8_Y5_PARENT_QLOC_1618",
        "P8_Y5_BRR545_1618",
        "Y5_R2FR_metric_response_Helmholtz",
        "R2FR_metric_response_audit_nonclaim_1618",
        "R2FR_helmholtz_audit_nonclaim_1618",
        "R2FR_q_loc_bound_schema_upgrade_nonclaim_1618",
    )
    return not any(any(marker in path.name for marker in artifact_markers) for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    metric = read_csv(METRIC_AUDIT)
    helmholtz = read_csv(HELMHOLTZ_AUDIT)
    candidates = read_csv(CANDIDATE_DECISION)
    schema = read_csv(QLOC_BOUND_SCHEMA)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1618_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1618 local source paths exist"),
        ("VAL1618_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1618 source needles found"),
        ("VAL1618_2_input_dir_ready", INPUT_1618.exists(), "1618 quarantine input directory exists"),
        ("VAL1618_3_metric_gate_fails_current_claim", any(row["result"] == "METRIC_RESPONSE_GATE_FAILS_CURRENT_CLAIM" for row in metric), "metric-response audit refuses current local claim"),
        ("VAL1618_4_helmholtz_not_runnable", any(row["result"] == "HELMHOLTZ_NOT_RUNNABLE_INPUTS_MISSING" for row in helmholtz), "Helmholtz audit names missing explicit functional/operator inputs"),
        ("VAL1618_5_candidate_next_selected", any(truthy(row.get("selected_next")) for row in candidates), "positive auxiliary/response-doublet construction selected as next route"),
        ("VAL1618_6_q_loc_schema_nonclaim", all(not truthy(row.get("valid_for_claim")) and not truthy(row.get("claim_allowed")) for row in schema), "q_loc bound schema remains nonclaim"),
        ("VAL1618_7_runner_blocks_local_gr", any(row["runner_result"] == "DO_NOT_REOPEN_LOCAL_GR" for row in runner), "runner refuses local-GR reopening"),
        ("VAL1618_8_claim_gates_closed", all(row["status"] in {"CLOSED_DEFINITION_ONLY", "BLOCKED"} and not truthy(row["claim_allowed"]) for row in gates), "all claim gates remain closed/nonclaim"),
        ("VAL1618_9_decision_no_promotion", any(row["decision"] == "LOCAL_GR_NOT_REOPENED" for row in decisions), "decision ledger keeps local GR blocked"),
        ("VAL1618_10_next_target_selected", any("1619-Y5-R2FR-positive-auxiliary-SGK-normal-form-or-q_loc-profile-row.md" in row["next_target"] for row in next_rows), "next target selected"),
        ("VAL1618_11_csv_parse", csv_parses(generated_csvs), "all generated 1618 CSVs parse"),
        ("VAL1618_12_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1618 rows reopen local claims, score-ready rows, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1618_13_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1618_14_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1618_15_formalization_untouched", no_formalization_1618(), "no 1618 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1618_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1618 metric-response Helmholtz audit or q_loc bound schema validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    columns = columns or list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "/").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    source_rows = read_csv(SOURCE_REGISTER)
    metric_rows = read_csv(METRIC_AUDIT)
    helmholtz_rows = read_csv(HELMHOLTZ_AUDIT)
    candidate_rows = read_csv(CANDIDATE_DECISION)
    schema_rows = read_csv(QLOC_BOUND_SCHEMA)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)
    validation = read_csv(VALIDATION)
    content = f"""# 1618 - R2/fR Metric-Response Helmholtz Audit Or q_loc Bound Schema

## Verdict
- 1618 does not reopen local GR/Newton recovery: the metric-response gate fails the current claim because `Gamma_eff` and `K_hat` are not yet one source-signed Hilbert-stress object.
- The Helmholtz test is now sharply stated, but it is not runnable without an explicit `S_GK`/`Gamma_eff` functional, `K_hat` operator expression, boundary convention, and variation domain.
- This is not a no-go theorem. It says the proof route is still alive only as a construction problem, not as a current derived result.
- The fallback branch is hardened: future `q_loc` residual rows must carry units, normalization, source path, metric-response status, Helmholtz status, observable map, and bound fields.
- Best next route: try a positive auxiliary / response-doublet `S_GK` normal form; if it cannot be made calculable, stage the first strict `q_loc` profile row.
- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "needles"])}

## Metric-Response Audit

{md_table(metric_rows, ["audit_id", "required_clause", "current_evidence", "result", "effect"])}

## Helmholtz Audit

{md_table(helmholtz_rows, ["audit_id", "required_clause", "mathematical_form", "result", "effect"])}

## Action Candidate Decision Matrix

{md_table(candidate_rows, ["candidate_row", "source_candidate", "normal_form", "status_now", "decision", "missing_input", "selected_next"])}

## q_loc Bound Schema Upgrade

{md_table(schema_rows, ["schema_row_id", "q_loc_component", "operator_or_profile", "units", "normalization", "source_path", "metric_response_status", "helmholtz_status", "observable_map", "bound_value", "bound_units", "blocker"])}

## Runner

{md_table(runner, ["runner_id", "input_state", "runner_result", "effect"])}

## Claim Gates

{md_table(gates, ["gate_id", "claim", "status", "reason"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"])}

## Validation

{md_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    INPUT_1618.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)

    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        METRIC_AUDIT: metric_audit_rows(),
        HELMHOLTZ_AUDIT: helmholtz_audit_rows(),
        CANDIDATE_DECISION: candidate_decision_rows(),
        QLOC_BOUND_SCHEMA: qloc_bound_schema_rows(),
        RUNNER: runner_rows(),
        CLAIM_GATE: claim_gate_rows(),
        DECISION: decision_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    copy_outputs()
    generated_csvs = list(outputs.keys())
    remove_pycache()
    write_csv(VALIDATION, validation_rows(generated_csvs))
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()

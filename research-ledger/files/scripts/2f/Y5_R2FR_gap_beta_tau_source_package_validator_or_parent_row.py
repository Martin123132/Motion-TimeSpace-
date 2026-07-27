from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1748"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1748 - Gap Beta Tau Source Package Validator Or Parent Row"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1748_0_1747_doc",
        "source_key": "1747_handoff",
        "source_path": ROOT / "1747-Y5-R2FR-canonical-gap-coupling-source-silence-or-wall-bound-row.md",
        "needles": ["NEXT1747_0_primary", "TARGET_GAP_BETA_TAU_SOURCE_PACKAGE_VALIDATOR"],
    },
    {
        "source_id": "SRC1748_1_1747_gap_gate",
        "source_key": "1747_gap_amplitude_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1747_GAP_AMPLITUDE_SOURCE_GATE.csv",
        "needles": ["GAS1747_0_mu_m2", "MISSING_SOURCE_BACKED_CANONICAL_GAP"],
    },
    {
        "source_id": "SRC1748_2_1747_claim_gate",
        "source_key": "1747_claim_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1747_CLAIM_GATE.csv",
        "needles": ["GATE1747_5_local_GR", "BLOCKED_NO_LOCAL_REENTRY"],
    },
    {
        "source_id": "SRC1748_3_1746_tail_theorem",
        "source_key": "1746_tail_derivative_theorem",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1746_TAIL_DERIVATIVE_THEOREM.csv",
        "needles": ["TD1746_2_canonical_gap_rewrite", "MISSING_SOURCE_BACKED_MU_M2"],
    },
    {
        "source_id": "SRC1748_4_1746_canonical_sources",
        "source_key": "1746_canonical_source_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1746_CANONICAL_SOURCE_ROWS.csv",
        "needles": ["CSR1746_3_beta_source_test", "PRODUCT_LAW_READY_VALUES_MISSING"],
    },
    {
        "source_id": "SRC1748_5_1594_beta_validator",
        "source_key": "1594_strict_beta_validator",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1594_BETA_ROW_VALIDATOR_SPEC.csv",
        "needles": ["BVS1594_6_status", "reject MISSING, TEMPLATE, NONCLAIM, TOY, PLACEHOLDER"],
    },
    {
        "source_id": "SRC1748_6_1596_tau_law",
        "source_key": "1596_tau_contraction_law",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1596_TAU_WEP_CONTRACTION_LAW.csv",
        "needles": ["TCL1596_1_product_bound", "abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15"],
    },
    {
        "source_id": "SRC1748_7_1596_tau_factors",
        "source_key": "1596_tau_factor_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1596_TAU_FACTOR_AUDIT.csv",
        "needles": ["TFA1596_0_source_worldtube", "MISSING_SOURCE_PROFILE_WEIGHTING"],
    },
    {
        "source_id": "SRC1748_8_1596_tau_acquisition",
        "source_key": "1596_tau_acquisition_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1596_TAU_SOURCE_ACQUISITION_ROWS.csv",
        "needles": ["TSA1596_3_tau_min", "DERIVATION_OR_SOURCE_NEEDED"],
    },
    {
        "source_id": "SRC1748_9_1596_delta_w_status",
        "source_key": "1596_delta_w_bound_status",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1596_DELTA_W_BOUND_STATUS.csv",
        "needles": ["DWB1596_0_product_anchor", "NO_TAU_MIN_SOURCE"],
    },
    {
        "source_id": "SRC1748_10_1597_tau_bound",
        "source_key": "1597_tau_lower_bound_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1597_TAU_LOWER_BOUND_THEOREM_AUDIT.csv",
        "needles": ["TLB1597_1_sufficient_lower_bound", "TAU_MIN_REQUIRES_ALIGNMENT_NOT_JUST_NONZERO_FACTORS"],
    },
    {
        "source_id": "SRC1748_11_1695_projection",
        "source_key": "1695_tau_projection_readiness",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1695_TAU_WEP_PROJECTION_READINESS.csv",
        "needles": ["TAU1695_7_parser_status", "BLOCKED"],
    },
    {
        "source_id": "SRC1748_12_1696_tau_min",
        "source_key": "1696_tau_min_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1696_TAU_MIN_LOWER_BOUND_GATE.csv",
        "needles": ["TAUMIN1696_8_verdict", "TAU_MIN_NOT_DERIVED_OR_SOURCED"],
    },
    {
        "source_id": "SRC1748_13_1697_acquisition_pack",
        "source_key": "1697_wep_tau_min_acquisition_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1697_WEP_TAU_MIN_ACQUISITION_PACK.csv",
        "needles": ["ACQ1697_4_tau_min", "strictly positive lower bound"],
    },
    {
        "source_id": "SRC1748_14_1702_product_row",
        "source_key": "1702_wep_source_weight_product",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1702_WEP_SOURCE_WEIGHT_PRODUCT_ROW.csv",
        "needles": ["WEP1702_4_refusal", "REFUSAL_ACTIVE"],
    },
    {
        "source_id": "SRC1748_15_1703_tau_route",
        "source_key": "1703_tau_wep_route",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1703_TAU_WEP_ROUTE.csv",
        "needles": ["TWR1703_7_verdict", "BLOCKED_MISSING_INPUTS"],
    },
    {
        "source_id": "SRC1748_16_1694_bound_anchor",
        "source_key": "1694_current_bound_anchor",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1694_SOURCE_BACKED_BETA_DELTAW_CURRENT_ROWS.csv",
        "needles": ["BDW1694_0_MICROSCOPE_Delta_w_tau_bound_anchor", "BDW1694_4_verdict"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1748_SOURCE_REGISTER.csv",
    "validator_spec": RESIDUALS / "P8_Y5_PARENT_QLOC_1748_PACKAGE_VALIDATOR_SPEC.csv",
    "package_evaluation": RESIDUALS / "P8_Y5_PARENT_QLOC_1748_CURRENT_PACKAGE_EVALUATION.csv",
    "parent_zero_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1748_PARENT_ZERO_OR_SOURCE_ROW_AUDIT.csv",
    "acquisition_queue": RESIDUALS / "P8_Y5_PARENT_QLOC_1748_ACQUISITION_QUEUE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1748_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1748_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1748_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1748_VALIDATION.csv",
}


COPY_MAP = {
    "validator_spec": "R2FR_1748_PACKAGE_VALIDATOR_SPEC.csv",
    "package_evaluation": "R2FR_1748_CURRENT_PACKAGE_EVALUATION.csv",
    "parent_zero_audit": "R2FR_1748_PARENT_ZERO_OR_SOURCE_ROW_AUDIT.csv",
    "acquisition_queue": "R2FR_1748_ACQUISITION_QUEUE.csv",
    "decision": "R2FR_1748_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1748_CLAIM_GATE.csv",
    "next_target": "R2FR_1748_NEXT_TARGET.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def source_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(exists),
                "needles": ";".join(needles),
                "needles_present": yesno(exists and all(needle in text for needle in needles)),
                "checked_utc": UTC,
            }
        )
    return rows


def validator_spec_rows() -> list[dict[str, Any]]:
    spec = [
        ("VSP1748_0_branch", "same_parent_branch_id", "must equal the 1428 finite source branch", "reject blank or branch-mismatched rows"),
        ("VSP1748_1_quantity", "quantity and role", "must name one of gap/amplitude/source leg/test leg/tau/product/tail/wall/projection/direct product", "reject vague coupling symbols"),
        ("VSP1748_2_units", "units", "must be concrete and compatible with the declared role", "reject missing, mixed, or convention-only units"),
        ("VSP1748_3_source", "source_path/source_anchor/extraction_method", "must cite local source evidence or a parent derivation", "reject unsourced templates and toy numbers"),
        ("VSP1748_4_convention", "normalization/convention", "must state canonical gap, beta, tau, product, or wall convention", "reject hidden tau=1 or measured-G absorption shortcuts"),
        ("VSP1748_5_arena", "arena map", "must name R10/PPN/WEP/clock/orbital/Newton/local-GR role", "reject rows with no observable map"),
        ("VSP1748_6_status", "current_status", "claim scoring needs SOURCE_BACKED_NUMERIC, THEOREM_ZERO_PARENT_SIGNED, or EXPLICIT_BOUND_SOURCE_BACKED plus prediction ownership", "reject MISSING, BLOCKED, NONCLAIM, TEMPLATE, PLACEHOLDER for scoring"),
        ("VSP1748_7_bound_anchor", "bound-only exception", "a source-backed external bound may be retained as bound input with valid_prediction_row=false", "reject promoting a bound anchor into an MTS prediction"),
        ("VSP1748_8_missing_guard", "MISSING_* guard", "any row containing MISSING_* must keep score_ready=false and claim_allowed=false", "reject readiness on placeholder rows"),
        ("VSP1748_9_zero_theorem", "parent zero route", "zero rows need an explicit parent-signed theorem and boundary/readout silence", "reject post-hoc setting of beta, tau, c_g, or q_loc to zero"),
        ("VSP1748_10_verdict", "validator policy", "this validator is a private nonclaim gate before any local score", "no local-GR/Newton/PPN/R10/WEP claim from 1748"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "spec_id": spec_id,
            "field_or_gate": field,
            "requirement": requirement,
            "failure_rule": failure,
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for spec_id, field, requirement, failure in spec
    ]


def package_evaluation_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "EVAL1748_0_mu_m2",
            "mu_m^2",
            "canonical gap; ell_tr=1/sqrt(mu_m^2)",
            "local screened-tail and PPN/R10 range",
            "MISSING_SOURCE_BACKED_CANONICAL_GAP",
            "P8_Y5_PARENT_QLOC_1747_GAP_AMPLITUDE_SOURCE_GATE.csv:GAS1747_0_mu_m2",
            "parent Hessian/kinetic ratio or direct canonical gap theorem",
        ),
        (
            "EVAL1748_1_Phi_S",
            "Phi_S",
            "boundary/source amplitude for exterior tail",
            "local residual amplitude",
            "MISSING_CANONICAL_AMPLITUDE",
            "P8_Y5_PARENT_QLOC_1747_GAP_AMPLITUDE_SOURCE_GATE.csv:GAS1747_1_Phi_S",
            "source/boundary amplitude theorem or sourced finite bound",
        ),
        (
            "EVAL1748_2_domain_distance",
            "d",
            "distance from local support to active transition/source boundary",
            "tail suppression exponent",
            "MISSING_DOMAIN_DISTANCE",
            "P8_Y5_PARENT_QLOC_1747_GAP_AMPLITUDE_SOURCE_GATE.csv:GAS1747_2_d",
            "local arena worldtube/support geometry",
        ),
        (
            "EVAL1748_3_beta_source_test",
            "beta_source*beta_test",
            "finite exchange coupling product if zero theorem fails",
            "R10/PPN/WEP/clock/orbital force residual",
            "PRODUCT_LAW_READY_VALUES_MISSING",
            "P8_Y5_PARENT_QLOC_1746_CANONICAL_SOURCE_ROWS.csv:CSR1746_3_beta_source_test",
            "source-backed beta legs or parent coupling-zero theorem",
        ),
        (
            "EVAL1748_4_delta_w_tau_bound",
            "abs(Delta_w_TiPt*tau_WEP)",
            "MICROSCOPE product bound anchor",
            "WEP bound input only",
            "EXPLICIT_BOUND_SOURCE_BACKED_NONPREDICTION",
            "P8_Y5_PARENT_QLOC_1596_DELTA_W_BOUND_STATUS.csv:DWB1596_0_product_anchor",
            "tau_WEP and MTS Delta_w prediction before any score",
        ),
        (
            "EVAL1748_5_tau_WEP",
            "tau_WEP",
            "branch-locked source/orbit/readout projection",
            "WEP product-to-Delta_w conversion",
            "FORMAL_DEFINITION_ONLY_INPUTS_MISSING",
            "P8_Y5_PARENT_QLOC_1703_TAU_WEP_ROUTE.csv:TWR1703_0_definition",
            "official readout, source worldtube, material tensor, product convention",
        ),
        (
            "EVAL1748_6_tau_min",
            "tau_min",
            "strict lower bound abs(tau_WEP)>=tau_min>0",
            "finite Delta_w amplitude law",
            "NO_TAU_MIN_SOURCE",
            "P8_Y5_PARENT_QLOC_1696_TAU_MIN_LOWER_BOUND_GATE.csv:TAUMIN1696_8_verdict",
            "alignment/non-null theorem or sourced projection lower bound",
        ),
        (
            "EVAL1748_7_epsilon_tail",
            "epsilon_tail",
            "hidden frame/readout/boundary/non-EH tail envelope",
            "tail theorem correction control",
            "MISSING_TAIL_ENVELOPE",
            "P8_Y5_PARENT_QLOC_1746_CANONICAL_SOURCE_ROWS.csv:CSR1746_4_epsilon_tail",
            "component bounds or theorem-zero clauses",
        ),
        (
            "EVAL1748_8_projection_norms",
            "A_ref;N_div;N_G;N_D",
            "operator/projection/normalization bridge to observables",
            "observable residual vector",
            "MISSING_OPERATOR_PROJECTION_NORMS",
            "P8_Y5_PARENT_QLOC_1747_GAP_AMPLITUDE_SOURCE_GATE.csv:GAS1747_4_projection",
            "arena operator maps and norm convention",
        ),
        (
            "EVAL1748_9_wall_bound",
            "Q_wall_grad;Q_shell_boundary",
            "finite transition-wall and boundary-shell residuals",
            "fallback when support intersects transition wall",
            "BOUND_FORM_ONLY_NONCLAIM",
            "P8_Y5_PARENT_QLOC_1747_WALL_BOUND_ROW.csv:WBR1747_0_transition_wall_gradient",
            "wall width, support overlap, amplitude and projection norms",
        ),
        (
            "EVAL1748_10_direct_product",
            "P_WEP_source_weight",
            "direct parent product without Delta_w/tau split",
            "WEP shortcut only if genuinely parent-owned",
            "MISSING_DIRECT_PRODUCT",
            "P8_Y5_PARENT_QLOC_1702_WEP_SOURCE_WEIGHT_PRODUCT_ROW.csv:WEP1702_3_direct_product",
            "numeric/theorem direct product with units and source path",
        ),
        (
            "EVAL1748_11_c_parent_zero",
            "C_parent or action-measure owner",
            "zero theorem or finite parent coefficient in same branch",
            "coupling closure and local-GR reentry",
            "MISSING_C_PARENT_OR_ZERO_CERTIFICATE",
            "P8_Y5_PARENT_QLOC_1703_TAU_WEP_ROUTE.csv:TWR1703_5_c_parent",
            "parent-signed action/measure/current owner theorem",
        ),
        (
            "EVAL1748_12_overall",
            "canonical local source package",
            "gap + amplitude + coupling + tau + tails + wall/projection rows",
            "local GR/Newton/PPN/R10/WEP reopening",
            "PACKAGE_FAILS_CURRENT_CLAIM",
            "P8_Y5_PARENT_QLOC_1747_CLAIM_GATE.csv:GATE1747_5_local_GR",
            "all non-bound rows source-backed/theorem-zero and no missing markers",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "eval_id": eval_id,
            "quantity": quantity,
            "definition": definition,
            "arena_role": arena_role,
            "current_status": status,
            "source_anchor": source_anchor,
            "needed_to_promote": needed,
            "accepted_as_bound_input": "True" if eval_id == "EVAL1748_4_delta_w_tau_bound" else no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for eval_id, quantity, definition, arena_role, status, source_anchor, needed in rows
    ]


def parent_zero_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PZA1748_0_tail_derivative",
            "screened-tail derivative law",
            "CONDITIONAL_THEOREM_AVAILABLE",
            "1746 gives the tail derivative theorem, but not parent ownership of mu_m^2/Phi_S/source silence",
            "retain conditional theorem; do not claim local q_loc=0",
        ),
        (
            "PZA1748_1_gap_theorem",
            "parent mass gap mu_m^2",
            "NOT_PARENT_SOURCE_BACKED",
            "canonical rewrite exists but Hessian/kinetic ratio is not sourced from the parent action",
            "try derive mu_m^2 from parent quadratic action",
        ),
        (
            "PZA1748_2_coupling_zero",
            "g_c=0 or beta_source beta_test zero",
            "ZERO_THEOREM_NOT_CLOSED",
            "matter functor/action-weight/current-owner/boundary clauses remain unsigned",
            "finite beta rows remain mandatory",
        ),
        (
            "PZA1748_3_tau_lower_bound",
            "abs(tau_WEP)>=tau_min>0",
            "CONDITIONAL_ALIGNMENT_THEOREM_ONLY",
            "1597 derives a sufficient condition but not the needed alignment/source data",
            "source tau factors or prove non-orthogonality",
        ),
        (
            "PZA1748_4_direct_product",
            "direct WEP source-weight product",
            "MISSING_DIRECT_PRODUCT",
            "1702 refuses unity tau, G absorption, cancellation and unsourced factor choices",
            "do not bypass tau/source map",
        ),
        (
            "PZA1748_5_action_measure_owner",
            "single action-measure/current owner",
            "ACTIVE_COUNTEREXAMPLE_RETAINED",
            "independent action-weight terms remain possible unless parent action excludes them",
            "derive common measure/coframe/current descent or keep finite Delta_w",
        ),
        (
            "PZA1748_6_verdict",
            "parent-zero route",
            "NO_PARENT_ZERO_THEOREM_CLOSED_IN_1748",
            "1748 is a validator/source-row checkpoint, not a local-GR closure",
            "next target must close one row or keep finite empirical branch",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "target": target,
            "current_status": status,
            "reason": reason,
            "next_action": action,
            "parent_signed": no(),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for audit_id, target, status, reason, action in rows
    ]


def acquisition_queue_rows() -> list[dict[str, Any]]:
    rows = [
        ("ACQ1748_0_mu_m2", "P_LOCAL_mu_m2_gap_source_row.csv", "mu_m^2", "parent quadratic Hessian/kinetic ratio; units; sign; branch assumptions; source path", "derivation_first", "highest"),
        ("ACQ1748_1_Phi_S", "P_LOCAL_Phi_S_boundary_amplitude.csv", "Phi_S", "source/boundary amplitude; exterior domain; uncertainty; source path", "derivation_or_bound", "highest"),
        ("ACQ1748_2_beta", "P_LOCAL_beta_source_test_row.csv", "beta_source*beta_test", "source leg; test leg; normalization; units; parent coefficient or zero theorem", "derivation_or_source", "highest"),
        ("ACQ1748_3_readout", "P_WEP_K_CMSM_readout.csv", "K_CMSM/P_WEP_readout", "time; session; segment; gx/gz/Sxx/Sxz; masks; calibration; orbit/attitude convention; units", "external_source", "high"),
        ("ACQ1748_4_worldtube", "P_WEP_R_source_Earth_worldtube.csv", "Earth/source worldtube", "radius/shell; density/stress proxy; composition; orbit kernel; source-weight convention; units", "external_source", "high"),
        ("ACQ1748_5_material", "P_WEP_TiPt_material_response_tensor.csv", "Ti/Pt material tensor", "TA6V and PtRh10 response tensor; composition; uncertainty; source-weight convention", "external_source_or_parent_matter", "high"),
        ("ACQ1748_6_product", "P_WEP_eta_product_convention.csv", "eta product convention", "formula; sign; absolute-value policy; unit map; normalization; no-cancellation guard", "definition_source", "high"),
        ("ACQ1748_7_tau_min", "P_WEP_tau_min_lower_bound.csv", "tau_min", "tau_min; confidence; derivation/source; assumptions; valid range; alignment guard", "derivation_or_source", "highest"),
        ("ACQ1748_8_tail", "P_LOCAL_epsilon_tail_envelope.csv", "epsilon_tail", "curvature/readout/boundary/tail correction bounds and assumptions", "derivation_or_bound", "medium"),
        ("ACQ1748_9_projection", "P_LOCAL_operator_projection_norms.csv", "A_ref;N_div;N_G;N_D", "arena operator maps, norm convention, uncertainty, units", "derivation_or_numeric_bound", "medium"),
        ("ACQ1748_10_wall", "P_LOCAL_transition_wall_bound_inputs.csv", "wall/shell residuals", "C_wall;A_S;U_B;L_wall;support overlap;projection norms", "fallback_bound", "medium"),
        ("ACQ1748_11_parent_owner", "parent_action_measure_owner_theorem.md", "action-measure/current owner theorem", "common measure; coframe; quotient descent; no representative action weights; boundary terms", "derivation_first", "highest_parallel"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "acq_id": acq_id,
            "needed_artifact": artifact,
            "quantity": quantity,
            "required_fields": required_fields,
            "route": route,
            "priority": priority,
            "current_status": "SOURCE_OR_DERIVATION_NEEDED",
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for acq_id, artifact, quantity, required_fields, route, priority in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1748_0_real_row_status",
            "ONE_REAL_BOUND_ANCHOR_RETAINED",
            "MICROSCOPE supplies a source-backed product bound, but it is external bound input, not an MTS prediction",
            "keep it in the ledger with valid_prediction_row=false",
        ),
        (
            "DEC1748_1_package_status",
            "LOCAL_SOURCE_PACKAGE_NOT_CLOSED",
            "mu_m2, Phi_S, beta legs, tau_WEP, tau_min, projection norms and wall inputs are still absent or conditional",
            "do not reopen local-GR/Newton/PPN/R10/WEP scoring",
        ),
        (
            "DEC1748_2_parent_zero_status",
            "NO_ZERO_THEOREM_CLOSED",
            "coupling zero, action-measure owner, tau lower bound and direct product routes all remain unsigned",
            "finite empirical residual rows remain live",
        ),
        (
            "DEC1748_3_best_next",
            "TARGET_PARENT_GAP_OR_SOURCE_AMPLITUDE_FIRST",
            "the cleanest derivation-first route is to try to source mu_m^2/Phi_S from the parent quadratic action before doing more external WEP plumbing",
            "build 1749 parent gap/amplitude row; keep tau_min acquisition as fallback",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for decision_id, decision, reason, next_action in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("GATE1748_0_validator", "1748 package validator can score local rows", "BLOCKED_NO_ACCEPTED_PREDICTION_ROWS"),
        ("GATE1748_1_bound_anchor", "MICROSCOPE product bound is an MTS prediction", "BLOCKED_BOUND_ANCHOR_ONLY"),
        ("GATE1748_2_gap_profile", "mu_m^2/Phi_S profile is parent-signed", "BLOCKED_GAP_AMPLITUDE_SOURCE_ROWS"),
        ("GATE1748_3_beta_tau", "beta and tau package closes", "BLOCKED_BETA_TAU_SOURCE_ROWS"),
        ("GATE1748_4_zero_theorem", "parent zero theorem closes local residuals", "BLOCKED_PARENT_ZERO_UNSIGNED"),
        ("GATE1748_5_local_reentry", "local GR/Newton/PPN/R10/WEP branch can claim", "BLOCKED_NO_LOCAL_REENTRY"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": blocker,
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for gate_id, claim, blocker in gates
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1748_0_primary",
            "next_target": "1749-Y5-R2FR-parent-gap-amplitude-row-or-tau-min-source-pack.md",
            "script": "scripts/Y5_R2FR_parent_gap_amplitude_row_or_tau_min_source_pack.py",
            "objective": "try to derive/source the first claim-grade canonical local row: mu_m^2 and Phi_S from the parent quadratic action; if that fails, stage tau_min source acquisition without scoring",
            "success_condition": "one source-backed/theorem-zero row passes the 1748 validator without opening a local claim, or a sharper blocker ledger identifies exactly why it cannot",
            "selection_status": "selected",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1748_1_fallback",
            "next_target": "1749b-Y5-R2FR-WEP-tau-min-source-import-pack.md",
            "script": "scripts/Y5_R2FR_WEP_tau_min_source_import_pack.py",
            "objective": "prepare official readout/source/material/product rows for tau_WEP and tau_min if derivation-first gap route stalls",
            "success_condition": "source-ready nonclaim import manifest for tau projection inputs",
            "selection_status": "held_fallback",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "validator_spec": validator_spec_rows(),
        "package_evaluation": package_evaluation_rows(),
        "parent_zero_audit": parent_zero_audit_rows(),
        "acquisition_queue": acquisition_queue_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1748_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1748_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {
        "claim_allowed",
        "gate_pass",
        "parent_signed",
        "score_ready",
        "valid_for_claim",
        "valid_prediction_row",
    }
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    readiness = {"claim_allowed", "gate_pass", "score_ready", "valid_for_claim", "valid_prediction_row"}
    for rows in rows_map.values():
        for row in rows:
            contains_missing = any("MISSING_" in str(value) for value in row.values())
            if contains_missing and any(str(row.get(flag, "")).lower() == "true" for flag in readiness):
                return False
    return True


def bound_anchor_only_nonprediction(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["package_evaluation"]
    return any(
        row["eval_id"] == "EVAL1748_4_delta_w_tau_bound"
        and row["accepted_as_bound_input"] == "True"
        and row["valid_prediction_row"] == "False"
        and row["claim_allowed"] == "False"
        for row in rows
    )


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1748_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1748_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1748*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    sources = rows_map["source_register"]
    specs = rows_map["validator_spec"]
    package = rows_map["package_evaluation"]
    parent = rows_map["parent_zero_audit"]
    acquisition = rows_map["acquisition_queue"]
    decisions = rows_map["decision"]
    claims = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]

    validation = [
        check("VAL1748_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1748_1_needles_present", all(row["needles_present"] == "True" for row in sources), "required source needles are present", "one or more source needles missing"),
        check("VAL1748_2_validator_spec_guard", any(row["spec_id"] == "VSP1748_8_missing_guard" for row in specs), "missing-row guard is explicit", "missing-row guard absent"),
        check("VAL1748_3_mu_gap_blocked", any(row["eval_id"] == "EVAL1748_0_mu_m2" and "MISSING_SOURCE_BACKED_CANONICAL_GAP" in row["current_status"] for row in package), "mu_m2 remains blocked", "mu_m2 blocker missing"),
        check("VAL1748_4_beta_tau_blocked", any(row["eval_id"] == "EVAL1748_6_tau_min" and row["current_status"] == "NO_TAU_MIN_SOURCE" for row in package), "tau_min remains blocked", "tau_min blocker missing"),
        check("VAL1748_5_bound_anchor_safe", bound_anchor_only_nonprediction(rows_map), "bound anchor retained as nonprediction only", "bound anchor missing or promoted"),
        check("VAL1748_6_parent_zero_not_closed", any(row["audit_id"] == "PZA1748_6_verdict" and row["current_status"] == "NO_PARENT_ZERO_THEOREM_CLOSED_IN_1748" for row in parent), "parent zero theorem remains unclosed", "parent zero verdict missing"),
        check("VAL1748_7_acquisition_queue_ready", len(acquisition) >= 10 and all(row["valid_for_claim"] == "False" for row in acquisition), "acquisition queue is populated and nonclaim", "acquisition queue incomplete or claim-enabled"),
        check("VAL1748_8_decision_next", any(row["decision_id"] == "DEC1748_3_best_next" and row["decision"] == "TARGET_PARENT_GAP_OR_SOURCE_AMPLITUDE_FIRST" for row in decisions), "decision selects parent gap/amplitude first", "best-next decision missing"),
        check("VAL1748_9_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claims), "all claim gates remain blocked", "one or more claim gates opened"),
        check("VAL1748_10_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check("VAL1748_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check("VAL1748_12_next_selected", any(row["route_id"] == "NEXT1748_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selected", "next target missing"),
        check("VAL1748_13_csv_parse", parsed_ok, "all generated 1748 CSVs parse", "one or more generated 1748 CSVs failed to parse"),
        check("VAL1748_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1748_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1748_16_formalization_untouched", formalization_untouched(), "no 1748 outputs found under formalization-workbench", "1748 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1748_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1748 gap/beta/tau source package validator checkpoint" if overall else "one or more 1748 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1748 turns the current local-recovery problem into a strict source-package validator instead of another informal theory note.",
        "- The strongest real row is still the MICROSCOPE `abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15` product-bound anchor, but it remains bound input only, not an MTS prediction.",
        "- The live blockers are precise: `mu_m^2`, `Phi_S`, `beta_source*beta_test`, `tau_WEP`, `tau_min`, tail corrections, projection norms, and wall inputs are not source-backed or parent-signed together.",
        "- No parent zero theorem closes here: coupling zero, action-measure owner, direct WEP product, and tau lower-bound routes all remain unsigned.",
        "- Best next attack is derivation-first: try to obtain `mu_m^2` and `Phi_S` from the parent quadratic action; keep WEP/tau source acquisition as the fallback data route.",
        "- No local-GR, Newton, PPN, WEP, clock, orbital, R10, `q_loc=0`, or public claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Validator Spec",
        markdown_table(rows_map["validator_spec"], ["spec_id", "field_or_gate", "requirement", "failure_rule"]),
        "",
        "## Current Package Evaluation",
        markdown_table(rows_map["package_evaluation"], ["eval_id", "quantity", "arena_role", "current_status", "needed_to_promote", "accepted_as_bound_input"]),
        "",
        "## Parent Zero Or Source Row Audit",
        markdown_table(rows_map["parent_zero_audit"], ["audit_id", "target", "current_status", "reason", "next_action"]),
        "",
        "## Acquisition Queue",
        markdown_table(rows_map["acquisition_queue"], ["acq_id", "needed_artifact", "quantity", "route", "priority", "current_status"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "This is not grim; it is finally narrow enough to be honest. The branch is no longer hand-waving about local GR recovery. It now has a finite shopping list: either the parent action supplies a canonical gap/amplitude/coupling silence package, or the theory carries finite residuals into WEP/PPN/R10/clock/orbital tests. The next win is not a big claim; it is one clean row that passes this validator without cheating.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1748-Y5-R2FR-gap-beta-tau-source-package-validator-or-parent-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1748_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1748 validation FAIL")
    print("1748 validation PASS")


if __name__ == "__main__":
    main()

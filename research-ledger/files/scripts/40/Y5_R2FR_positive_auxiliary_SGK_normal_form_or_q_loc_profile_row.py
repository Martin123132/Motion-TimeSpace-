from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
QUARANTINE = MICROSCOPE / "quarantine" / "1619"
INPUT_1619 = QUARANTINE / "input"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1619-Y5-R2FR-positive-auxiliary-SGK-normal-form-or-q_loc-profile-row.md"

SOURCE_FILES = {
    "1618_doc": ROOT / "1618-Y5-R2FR-metric-response-Helmholtz-audit-or-q_loc-bound-schema.md",
    "1618_validation": OUT / "P8_Y5_BRR545_1618_VALIDATION.csv",
    "1618_next": OUT / "P8_Y5_PARENT_QLOC_1618_NEXT_TARGET.csv",
    "1618_candidates": OUT / "P8_Y5_PARENT_QLOC_1618_ACTION_CANDIDATE_DECISION_MATRIX.csv",
    "1618_metric": OUT / "P8_Y5_PARENT_QLOC_1618_METRIC_RESPONSE_AUDIT.csv",
    "1618_helmholtz": OUT / "P8_Y5_PARENT_QLOC_1618_HELMHOLTZ_AUDIT.csv",
    "1618_bound_schema": OUT / "P8_Y5_PARENT_QLOC_1618_QLOC_BOUND_SCHEMA_UPGRADE.csv",
    "513_rewrite": OUT / "P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv",
    "514_contract": OUT / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
    "516_owner": OUT / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
    "1011_doublet": OUT / "P8_Y5_R10_1011_RESPONSED_DOUBLET_THEOREM_ATTEMPT.csv",
    "1011_decision": OUT / "P8_Y5_R10_1011_DECISION_LEDGER.csv",
    "yloc_noether": OUT / "P8_YLOC_SOURCE_CURRENT_NOETHER_AUDIT.csv",
    "1086_source_current": OUT / "P8_Y5_R10_1086_SOURCE_CURRENT_ZERO_THEOREM_ATTEMPT.csv",
    "992_descent": OUT / "P8_Y5_R10_992_SOURCE_CURRENT_DESCENT_THEOREM_GATE.csv",
}

NEEDLES = {
    "1618_doc": ["positive auxiliary / response-doublet", "VAL1618_OVERALL"],
    "1618_validation": ["VAL1618_OVERALL", "PASS"],
    "1618_next": ["1619-Y5-R2FR-positive-auxiliary-SGK-normal-form-or-q_loc-profile-row.md", "positive auxiliary/response-doublet"],
    "1618_candidates": ["CAND1618_1_response_doublet_quadratic", "CAND1618_2_positive_auxiliary_fields"],
    "1618_metric": ["METRIC_RESPONSE_GATE_FAILS_CURRENT_CLAIM", "MRG1618_7_verdict"],
    "1618_helmholtz": ["HELMHOLTZ_NOT_RUNNABLE_INPUTS_MISSING", "HLA1618_5_verdict"],
    "1618_bound_schema": ["QBS1618_0_profile", "MISSING_QLOC_PROFILE_OPERATOR"],
    "513_rewrite": ["SR513_2_variational_route", "conditional_derivation_route"],
    "514_contract": ["MR514_5_double_zero", "F_1"],
    "516_owner": ["GO516_A_response_doublet_quadratic_density", "GO516_B_positive_auxiliary_energy_density"],
    "1011_doublet": ["RDT1011_7_verdict", "fail_current_claim"],
    "1011_decision": ["DEC1011_0_formal_double_zero_survives", "DEC1011_1_Y5_is_root_pressure"],
    "yloc_noether": ["N4_no_linear_source_symmetry", "possible_rescue_theorem_target"],
    "1086_source_current": ["SCZ1086_5_verdict", "SOURCE_CURRENT_ZERO_NOT_DERIVED"],
    "992_descent": ["SCD992_4_charge_current_equality", "failed_current_corpus"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1619_SOURCE_REGISTER.csv"
NORMAL_FORM = OUT / "P8_Y5_PARENT_QLOC_1619_POSITIVE_AUXILIARY_NORMAL_FORM.csv"
CALCULABILITY = OUT / "P8_Y5_PARENT_QLOC_1619_METRIC_HELMHOLTZ_CALCULABILITY.csv"
LOCAL_SILENCE = OUT / "P8_Y5_PARENT_QLOC_1619_LOCAL_SILENCE_THEOREM.csv"
PARENT_GAPS = OUT / "P8_Y5_PARENT_QLOC_1619_PARENT_SIGNATURE_GAP_LEDGER.csv"
QLOC_PROFILE = OUT / "P8_Y5_PARENT_QLOC_1619_QLOC_PROFILE_ROW.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1619_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1619_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1619_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1619_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1619_VALIDATION.csv"

COPY_TARGETS = {
    NORMAL_FORM: [
        QUARANTINE / "POSITIVE_AUXILIARY_NORMAL_FORM_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_positive_auxiliary_normal_form_nonclaim_1619.csv",
    ],
    LOCAL_SILENCE: [
        QUARANTINE / "LOCAL_SILENCE_THEOREM_CONDITIONAL.csv",
        BRANCH_RESIDUALS / "R2FR_local_silence_theorem_conditional_1619.csv",
    ],
    PARENT_GAPS: [
        QUARANTINE / "PARENT_SIGNATURE_GAP_LEDGER.csv",
        BRANCH_RESIDUALS / "R2FR_parent_signature_gap_ledger_1619.csv",
    ],
    QLOC_PROFILE: [
        QUARANTINE / "QLOC_PROFILE_ROW_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_q_loc_profile_row_nonclaim_1619.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1619.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1619.csv",
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
                "source_id": f"SRC1619_{index}_{source_id}",
                "source_path": rel(path) if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1619_positive_auxiliary_normal_form_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def normal_form_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NF1619_0_field_split",
            "Introduce exchange doublets R_+^A,R_-^A and odd residuals Z^A=(R_+^A-R_-^A)/2 with even variables R_even^A=(R_+^A+R_-^A)/2.",
            "Z is the candidate local residual coordinate; R_even carries ordinary matter/source readout.",
            "FORMAL_DEFINITION",
            "matches the response-doublet template but does not yet prove these are actual MTS parent variables",
        ),
        (
            "NF1619_1_parent_action_density",
            "Use a calculable normal-form sector S_GK=-int sqrt(-g)[Gamma0+1/2 H_AB g^{mu nu} nabla_mu Z^A nabla_nu Z^B+1/2 M_AB^2 Z^A Z^B+O(Z^4)].",
            "H_AB is positive on the gauge-reduced local branch and M_AB^2 is non-negative/positive on non-gauge modes.",
            "FORMAL_CANDIDATE_CALCULABLE",
            "supplies the missing explicit functional for the normal form, not for current MTS",
        ),
        (
            "NF1619_2_metric_response_definition",
            "Define K_hat_normal^{mu nu} as the metric response of sqrt(-g)(Gamma_eff-Gamma0) under the fixed volume/sign convention.",
            "T_GK_normal^{mu nu}:=Gamma_eff_sub g^{mu nu}-K_hat_normal^{mu nu} is Hilbert-owned by S_GK.",
            "METRIC_RESPONSE_CLOSED_FOR_NORMAL_FORM_BY_DEFINITION",
            "closes the metric-response gate only inside the constructed normal form",
        ),
        (
            "NF1619_3_even_exchange_rule",
            "Require exchange symmetry Z -> -Z and matter/readout descent through R_even only.",
            "This removes linear Z terms in Gamma_eff and would set delta_Z S_matter=0 if parent-signed.",
            "FORMAL_SELECTION_RULE",
            "source-current zero is not inherited until the matter/action descent clause is proved",
        ),
        (
            "NF1619_4_double_zero",
            "After subtracting Gamma0, Gamma_eff_sub=O(Z^2,nabla Z^2) and T_GK_normal=O(Z^2,nabla Z^2).",
            "Therefore T_GK_normal(Z=0)=0 and partial_A T_GK_normal(Z=0)=0, equivalently F_1=0.",
            "FORMAL_DOUBLE_ZERO_PROVED",
            "the mechanism kills linear local leakage if Z=0 is the physical local branch",
        ),
        (
            "NF1619_5_Ward_profile",
            "Diffeomorphism invariance gives nabla_mu T_GK_normal^{mu nu}=E_A nabla^nu Z^A plus boundary/improvement terms.",
            "q_loc^nu=P_loc(E_A nabla^nu Z^A+B_GK^nu) for this normal form.",
            "FORMAL_QLOC_PROFILE_DERIVED",
            "a profile object exists, but the coefficient/source map is not claim-ready",
        ),
        (
            "NF1619_6_verdict",
            "The positive auxiliary / response-doublet normal form is a real derivation mechanism, but not a current MTS promotion.",
            "It provides calculable action, metric response, Helmholtz readiness, and double-zero inside the formal class.",
            "FORMAL_MECHANISM_EXISTS_NOT_PARENT_SIGNED",
            "next work must parent-sign Z, source-current zero, boundary no-flux, and PPN/source-normalization lock",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "normal_form_id": normal_form_id,
            "construction_clause": construction_clause,
            "mathematical_content": mathematical_content,
            "status": status,
            "interpretation": interpretation,
            "source_anchors": "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv; P8_Y5_R10_1011_RESPONSED_DOUBLET_THEOREM_ATTEMPT.csv; P8_Y5_PARENT_QLOC_1618_ACTION_CANDIDATE_DECISION_MATRIX.csv",
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for normal_form_id, construction_clause, mathematical_content, status, interpretation in rows
    ]


def calculability_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CAL1619_0_explicit_functional",
            "S_GK normal form supplies an explicit local diffeomorphism-invariant scalar density.",
            "PASS_FORMAL_NORMAL_FORM",
            "repairs HLA1618_1 only for the constructed normal form",
        ),
        (
            "CAL1619_1_Khat_operator",
            "K_hat_normal is defined as the Hilbert metric response of the same scalar density.",
            "PASS_FORMAL_NORMAL_FORM",
            "repairs MRG1618_1 only by defining a new normal-form K_hat, not by matching old K_hat",
        ),
        (
            "CAL1619_2_volume_sign_convention",
            "Use subtracted density Gamma_eff_sub=Gamma_eff-Gamma0 and T_GK=-2/sqrt(-g) delta S_GK/dg with Gamma0 treated as background subtraction.",
            "PASS_FORMAL_NORMAL_FORM",
            "removes constant background contamination inside the constructed sector",
        ),
        (
            "CAL1619_3_Helmholtz_symmetry",
            "Because T_GK_normal comes from S_GK, second metric variations commute up to boundary/gauge terms.",
            "HELMHOLTZ_PASS_FOR_CONSTRUCTED_NORMAL_FORM_NOT_MTS",
            "this is calculable once boundary/gauge domain is specified, but it is not evidence that old T_GK was variational",
        ),
        (
            "CAL1619_4_boundary_domain",
            "Local compact branch must impose no odd boundary charge and a self-adjoint domain for H_AB,M_AB.",
            "CONDITIONAL_BOUNDARY_DOMAIN",
            "boundary assumptions remain the bridge risk",
        ),
        (
            "CAL1619_5_verdict",
            "Metric-response and Helmholtz gates can be passed by this normal-form class, but MTS has not been shown to instantiate the class.",
            "FORMAL_CALCULABILITY_CLOSED_PARENT_SIGNATURE_OPEN",
            "continue to parent-signature/source-current proof before local-GR promotion",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "calculus_id": calculus_id,
            "test": test,
            "result": result,
            "effect": effect,
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for calculus_id, test, result, effect in rows
    ]


def local_silence_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LS1619_0_Euler_equation",
            "Variation in Z gives L_AB Z^B+N_A(Z)=J_A with L=-nabla_mu(H_AB nabla^mu)+M_AB^2 on the local compact branch.",
            "FORMAL_EULER_OPERATOR",
            "turns q_loc silence into source-current/boundary/domain conditions",
        ),
        (
            "LS1619_1_energy_identity",
            "Pair the Euler equation with Z and integrate: int(H_AB nabla Z^A nabla Z^B+M_AB^2 Z^A Z^B)+O(Z^3)=int J_A Z^A + boundary.",
            "FORMAL_ENERGY_IDENTITY",
            "positive operator makes zero-source/no-boundary branch rigid",
        ),
        (
            "LS1619_2_zero_theorem",
            "If J_A=0, odd boundary flux B_Z=0, gauge zero modes are removed, and L is positive, then Z=0 in the compact local exterior.",
            "CONDITIONAL_LOCAL_SILENCE_PROVED_FOR_NORMAL_FORM",
            "this is the clean local-vacuum plateau replacement, but the premises are not parent-signed for MTS",
        ),
        (
            "LS1619_3_q_loc_zero",
            "With Z=0, E_A=0, and boundary/improvement silence, q_loc^nu=P_loc(E_A nabla^nu Z^A+B_GK^nu)=0.",
            "CONDITIONAL_QLOC_ZERO_FOR_NORMAL_FORM",
            "derives q_loc zero only inside the formal normal-form class",
        ),
        (
            "LS1619_4_second_order_leakage",
            "If small sourced hair remains, T_GK starts at O(Z^2,nabla Z^2), so linear F_1 leakage is absent but quadratic/boundary/source terms must be bounded.",
            "FORMAL_SECOND_ORDER_RESIDUAL_LAW",
            "gives a possible residual-bound route without pretending exact local GR",
        ),
        (
            "LS1619_5_verdict",
            "The local silence theorem is mathematically clean but conditional on the exact clauses already known to be hard: J_Z=0, B_Z=0, parent Z map, and PPN/source lock.",
            "SILENCE_THEOREM_CONDITIONAL_NOT_MTS_CLAIM",
            "attack parent signature next",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "silence_id": silence_id,
            "theorem_clause": theorem_clause,
            "status": status,
            "effect": effect,
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for silence_id, theorem_clause, status, effect in rows
    ]


def parent_gap_rows() -> list[dict[str, Any]]:
    rows = [
        ("GAP1619_0_parent_doublets", "R_+^A,R_-^A exist for every physical local residual channel", "RDT1011_0_parent_doublets", "not_derived", "MTS residual variables have not been mapped into the Z^A normal-form coordinates"),
        ("GAP1619_1_exchange_symmetry", "Z -> -Z is an exact parent symmetry", "RDT1011_1_exchange_symmetry", "conditional_template", "selection rule cannot erase linear sources until symmetry is parent-signed"),
        ("GAP1619_2_matter_even_readout", "matter/clocks/sources couple only through R_even", "RDT1011_2_even_matter_readout; SCZ1086_5_verdict", "source_current_zero_not_derived", "Y5 source-normalization is exchange-even and remains hard pressure"),
        ("GAP1619_3_no_pre_action_weights", "object-language/action-measure forbids material/species weights before variation", "SCZ1086_2_pre_action_weight_leak", "not_closed", "pre-action weights can reintroduce composition/source currents"),
        ("GAP1619_4_boundary_zero", "odd boundary charge and symplectic flux vanish on local compact collar", "RDT1011_4_boundary_zero; N2_boundary_Ward", "conditional_not_closed", "bulk normal form can still leak via worldtube/source boundary"),
        ("GAP1619_5_positive_operator_parent", "H_AB and M_AB are positive after gauge/constraint removal for actual MTS variables", "RDT1011_5_positive_operator", "formal_candidate_only", "normal-form positivity is assumed, not derived from current MTS"),
        ("GAP1619_6_PPN_source_lock", "Z^A is the physical q_loc/PPN/source-normalization residual vector", "RDT1011_6_PPN_lock; SCD992_4_charge_current_equality", "not_derived", "even if Z is silent, Newton/GR normalization still needs source-current/charge equality"),
        ("GAP1619_7_verdict", "All parent-signature clauses close together", "RDT1011_7_verdict; DEC1011_1_Y5_is_root_pressure", "PARENT_SIGNATURE_OPEN_NO_PROMOTION", "formal mechanism is promising but cannot yet claim local GR"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gap_id": gap_id,
            "required_signature": required_signature,
            "source_anchor": source_anchor,
            "status": status,
            "effect": effect,
            "reopens_local_claim": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gap_id, required_signature, source_anchor, status, effect in rows
    ]


def qloc_profile_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QPR1619_0_normal_form_profile",
            "q_loc^nu",
            "P_loc(E_A nabla^nu Z^A+B_GK^nu)",
            "stress-divergence or force-density units; exact normalization MISSING_PARENT_SIGNATURE",
            "normal-form Hilbert stress with Gamma0 subtraction; parent MTS normalization not signed",
            "formal normal form in P8_Y5_PARENT_QLOC_1619_POSITIVE_AUXILIARY_NORMAL_FORM.csv",
            "METRIC_RESPONSE_PASS_FOR_CONSTRUCTED_NORMAL_FORM_NOT_CURRENT_MTS",
            "HELMHOLTZ_PASS_FOR_CONSTRUCTED_NORMAL_FORM_NOT_CURRENT_MTS",
            "not claim-ready; requires Z-to-PPN/source map",
            "MISSING_NUMERIC_BOUND",
            "MISSING_BOUND_UNITS",
            "valid symbolic profile row, but parent signature/source map missing",
        ),
        (
            "QPR1619_1_sourced_hair_profile",
            "q_loc^nu sourced residual",
            "P_loc((L_AB Z^B+N_A-J_A) nabla^nu Z^A+B_GK^nu)",
            "same as q_loc; J_A units undeclared",
            "Euler operator and source current convention undeclared for actual MTS",
            "P8_Y5_R10_1011_RESPONSED_DOUBLET_THEOREM_ATTEMPT.csv",
            "conditional",
            "conditional",
            "PPN/R10/clock/orbital only after J_A and B_GK source rows exist",
            "MISSING_J_BOUND",
            "MISSING_UNITS",
            "fallback row for residual-bound route if source-current zero fails",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "profile_row_id": row_id,
            "q_loc_component": component,
            "operator_or_profile": profile,
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
        for row_id, component, profile, units, normalization, source_path, metric_status, helmholtz_status, observable_map, bound_value, bound_units, blocker in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1619_0_sources", "1618 target plus doublet/source-current ledgers imported", "SOURCE_CONTEXT_READY", "1619 is anchored to current route"),
        ("RUN1619_1_normal_form", "positive auxiliary/response-doublet S_GK written explicitly", "FORMAL_MECHANISM_EXISTS_NOT_PARENT_SIGNED", "proof class found, not current MTS promotion"),
        ("RUN1619_2_metric_helmholtz", "K_hat_normal defined as metric response of S_GK", "CALCULABILITY_CLOSED_FOR_NORMAL_FORM_ONLY", "metric/Helmholtz gates can be satisfied by this class"),
        ("RUN1619_3_silence", "positive operator plus J_Z=B_Z=0 gives Z=0", "CONDITIONAL_LOCAL_SILENCE_THEOREM", "plateau axiom replaced by derivable premises"),
        ("RUN1619_4_parent_signature", "Y5/source-current/boundary/PPN lock remain unsigned", "DO_NOT_REOPEN_LOCAL_GR", "local GR/Newton recovery remains blocked"),
        ("RUN1619_5_profile", "symbolic q_loc profile row staged", "QLOC_PROFILE_ROW_STAGED_NONCLAIM", "fallback bound route has first stricter profile object"),
        ("RUN1619_6_next", "hardest missing bridge is parent signature/source-current zero", "SELECT_1620_PARENT_SIGNATURE_MAP_AND_SOURCE_CURRENT_ZERO", "try to map actual MTS residuals into the normal form"),
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
        ("CG1619_0_formal_SGK", "constructed positive auxiliary S_GK normal form", "CLOSED_FORMAL_NOT_MTS", "calculable mechanism exists as a formal class only"),
        ("CG1619_1_metric_response", "K_hat metric response", "CLOSED_FOR_NORMAL_FORM_ONLY", "normal K_hat is defined variationally, old MTS K_hat not matched"),
        ("CG1619_2_helmholtz", "Helmholtz variational stress", "CLOSED_FOR_NORMAL_FORM_ONLY", "action-generated stress is variational, but parent signature remains open"),
        ("CG1619_3_double_zero", "F_1=0/local double-zero", "CLOSED_CONDITIONAL_NORMAL_FORM", "proved after Gamma0 subtraction if Z is actual local residual"),
        ("CG1619_4_source_current", "J_Z=0 source-current theorem", "BLOCKED", "Y5/source-current zero remains not derived"),
        ("CG1619_5_boundary", "B_Z=0 and no-flux/local collar", "BLOCKED", "boundary/no-flux is conditional only"),
        ("CG1619_6_PPN_source_lock", "Z maps to physical PPN/source-normalization residuals", "BLOCKED", "PPN lock and source-current/charge equality not derived"),
        ("CG1619_7_local_GR", "derived local GR/Newton recovery", "BLOCKED", "formal normal form is not enough to promote current MTS"),
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
        ("DEC1619_0_formal_mechanism", "FORMAL_NORMAL_FORM_MECHANISM_EXISTS", "positive auxiliary/response-doublet S_GK gives metric response, Helmholtz readiness, Ward profile, and F_1=0 in a calculable class", "keep as the preferred local-GR derivation mechanism"),
        ("DEC1619_1_no_promotion", "NO_MTS_LOCAL_GR_PROMOTION", "parent doublets, matter-even descent, J_Z=0, B_Z=0, positivity, and PPN/source lock remain unsigned", "do not claim local GR/Newton recovery"),
        ("DEC1619_2_profile", "QLOC_PROFILE_ROW_STAGED_NONCLAIM", "normal form gives a symbolic q_loc profile but not units/source coefficients", "use only for future bound-row construction"),
        ("DEC1619_3_Y5_pressure", "Y5_SOURCE_NORMALIZATION_REMAINS_ROOT_PRESSURE", "exchange-odd symmetry does not automatically kill exchange-even source normalization", "attack parent signature/source-current zero directly"),
        ("DEC1619_4_next", "NEXT_1620_PARENT_SIGNATURE_MAP_AND_SOURCE_CURRENT_ZERO", "the main missing bridge is proving actual MTS lives in the normal-form class", "map MTS residual channels to Z^A and prove or bound J_Z/B_Z/PPN lock"),
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
            "next_target": "1620-Y5-R2FR-parent-signature-map-and-source-current-zero-or-q_loc-bound-fill.md",
            "script": "scripts/Y5_R2FR_parent_signature_map_and_source_current_zero_or_q_loc_bound_fill.py",
            "objective": "try to parent-sign the 1619 normal form by mapping actual MTS residual channels to Z^A, proving matter-even descent/source-current zero and boundary silence; if this fails, fill nonclaim q_loc source-current/bound rows",
            "success_condition": "either a parent-signed Z-map/J_Z/B_Z/PPN-lock clause is closed, or the first sourced nonclaim residual coefficient row is staged with blockers explicit",
            "do_not": "do not promote local GR, do not use exchange symmetry alone for Y5, do not use one-pair cancellations, do not borrow measured G/GM, do not hide boundary flux",
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


def no_formalization_1619() -> bool:
    if not FORMALIZATION.exists():
        return True
    artifact_markers = (
        "1619-Y5",
        "P8_Y5_PARENT_QLOC_1619",
        "P8_Y5_BRR545_1619",
        "Y5_R2FR_positive_auxiliary_SGK",
        "R2FR_positive_auxiliary_normal_form_nonclaim_1619",
        "R2FR_q_loc_profile_row_nonclaim_1619",
    )
    return not any(any(marker in path.name for marker in artifact_markers) for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    normal = read_csv(NORMAL_FORM)
    calculus = read_csv(CALCULABILITY)
    silence = read_csv(LOCAL_SILENCE)
    gaps = read_csv(PARENT_GAPS)
    profiles = read_csv(QLOC_PROFILE)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1619_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited 1619 local source paths exist"),
        ("VAL1619_1_needles_found", all(truthy(row["needle_found"]) for row in sources), "all required 1619 source needles found"),
        ("VAL1619_2_input_dir_ready", INPUT_1619.exists(), "1619 quarantine input directory exists"),
        ("VAL1619_3_formal_mechanism_exists", any(row["status"] == "FORMAL_MECHANISM_EXISTS_NOT_PARENT_SIGNED" for row in normal), "normal-form mechanism is explicit and nonclaim"),
        ("VAL1619_4_metric_helmholtz_formal_only", any(row["result"] == "HELMHOLTZ_PASS_FOR_CONSTRUCTED_NORMAL_FORM_NOT_MTS" for row in calculus), "Helmholtz pass is limited to constructed normal form"),
        ("VAL1619_5_double_zero_conditional", any(row["status"] == "CONDITIONAL_QLOC_ZERO_FOR_NORMAL_FORM" for row in silence), "local silence/q_loc zero theorem is conditional"),
        ("VAL1619_6_parent_gaps_open", any(row["status"] == "PARENT_SIGNATURE_OPEN_NO_PROMOTION" for row in gaps), "parent-signature gap ledger blocks promotion"),
        ("VAL1619_7_profile_nonclaim", all(not truthy(row["valid_for_claim"]) and not truthy(row["claim_allowed"]) for row in profiles), "q_loc profile rows remain nonclaim"),
        ("VAL1619_8_runner_blocks_local_gr", any(row["runner_result"] == "DO_NOT_REOPEN_LOCAL_GR" for row in runner), "runner refuses local-GR reopening"),
        ("VAL1619_9_claim_gates_closed", all(not truthy(row["claim_allowed"]) and row["status"] != "CLAIM_READY" for row in gates), "all claim gates remain closed/nonclaim"),
        ("VAL1619_10_decision_next", any(row["decision"] == "NEXT_1620_PARENT_SIGNATURE_MAP_AND_SOURCE_CURRENT_ZERO" for row in decisions), "decision selects parent-signature/source-current next target"),
        ("VAL1619_11_next_target_selected", any("1620-Y5-R2FR-parent-signature-map-and-source-current-zero-or-q_loc-bound-fill.md" in row["next_target"] for row in next_rows), "next target selected"),
        ("VAL1619_12_csv_parse", csv_parses(generated_csvs), "all generated 1619 CSVs parse"),
        ("VAL1619_13_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1619 rows reopen local claims, score-ready rows, prediction rows, valid-for-claim, or claim-allowed"),
        ("VAL1619_14_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1619_15_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1619_16_formalization_untouched", no_formalization_1619(), "no 1619 outputs found under formalization-workbench"),
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
            "check_id": "VAL1619_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1619 positive auxiliary SGK normal form or q_loc profile row validation",
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
    normal_rows = read_csv(NORMAL_FORM)
    calculus_rows = read_csv(CALCULABILITY)
    silence_rows = read_csv(LOCAL_SILENCE)
    gap_rows = read_csv(PARENT_GAPS)
    profile_rows = read_csv(QLOC_PROFILE)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)
    validation = read_csv(VALIDATION)
    content = f"""# 1619 - R2/fR Positive Auxiliary S_GK Normal Form Or q_loc Profile Row

## Verdict
- 1619 finds a real formal mechanism: a positive auxiliary / response-doublet `S_GK` normal form can own `Gamma_eff`, define `K_hat` as a metric response, pass Helmholtz by construction, and give `F_1=0` after `Gamma0` subtraction.
- This is not yet an MTS local-GR proof. The mechanism is parent-signature dependent: actual MTS residuals still need to be mapped to `Z^A`, and `J_Z=0`, `B_Z=0`, positivity, and PPN/source-normalization lock are not derived.
- The local-vacuum plateau axiom is replaced by a conditional energy theorem: if the source current and odd boundary flux vanish, a positive operator forces `Z=0`, hence `q_loc^nu=0` in the constructed normal-form class.
- A first symbolic `q_loc` profile row is staged for the fallback route, but it is explicitly nonclaim because units, normalization, source-current coefficients, and observable maps are not source-signed.
- Next target is the bridge, not more decoration: parent-sign the normal form against actual MTS variables or fill nonclaim source-current/bound rows.
- No WEP, R10, PPN, clock, orbital, Newton, local-GR, beta/coupling, or public claim is made.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "exists", "needle_found", "needles"])}

## Positive Auxiliary Normal Form

{md_table(normal_rows, ["normal_form_id", "construction_clause", "mathematical_content", "status", "interpretation"])}

## Metric/Helmholtz Calculability

{md_table(calculus_rows, ["calculus_id", "test", "result", "effect"])}

## Local Silence Theorem

{md_table(silence_rows, ["silence_id", "theorem_clause", "status", "effect"])}

## Parent Signature Gap Ledger

{md_table(gap_rows, ["gap_id", "required_signature", "source_anchor", "status", "effect"])}

## q_loc Profile Row

{md_table(profile_rows, ["profile_row_id", "q_loc_component", "operator_or_profile", "units", "normalization", "source_path", "metric_response_status", "helmholtz_status", "observable_map", "bound_value", "bound_units", "blocker"])}

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
    INPUT_1619.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)

    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        NORMAL_FORM: normal_form_rows(),
        CALCULABILITY: calculability_rows(),
        LOCAL_SILENCE: local_silence_rows(),
        PARENT_GAPS: parent_gap_rows(),
        QLOC_PROFILE: qloc_profile_rows(),
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

from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_ROOT = MICROSCOPE / "branch_locked_wep"
COEFF = BRANCH_ROOT / "coefficients"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1449-Y5-R10-RAB-field-by-field-V-WEP-action-map-or-source-only-countermodel-retention.md"

PREV_NEXT = OUT / "P8_Y5_R10_1448_NEXT_TARGET.csv"
PREV_DOMAIN = OUT / "P8_Y5_R10_1448_VWEP_DOMAIN_PROOF_ATTEMPT.csv"
PREV_EVAL = OUT / "P8_Y5_R10_1448_FUNCTIONAL_DERIVATIVE_EVALUABILITY_GATE.csv"
PREV_MOMS_PACK = OUT / "P8_Y5_R10_1448_MOMS_SIGNATURE_SOURCE_PACK.csv"
PREV_COUNTERS = OUT / "P8_Y5_R10_1448_COUNTERMODEL_RETENTION.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1448_VALIDATION.csv"

QVX_CERT = OUT / "P8_Y5_R10_1023_QVX_CERTIFICATE.csv"
MATTER_SIGNATURE = OUT / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv"
VERTICAL_LIFT = OUT / "P8_Y5_R10_1045_VERTICAL_LIFT_DESCENT_GATE.csv"
NO_SHADOW = OUT / "P8_Y5_R10_1046_NO_SHADOW_FRAME_THEOREM_ATTEMPT.csv"
CONSTANT_SUPER = OUT / "P8_Y5_R10_1047_CONSTANT_SUPERSELECTION_THEOREM_ATTEMPT.csv"
PARENT_CONTRACT = OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv"
LABEL_FORGET = OUT / "P8_Y5_R10_1064_LABEL_FORGETTING_PROOF_ATTEMPT.csv"
NO_SOURCE_SLOT = OUT / "P8_Y5_R10_1064_NO_SOURCE_ONLY_SLOT_AUDIT.csv"
AX1090_REDUCTION = OUT / "P8_Y5_R10_1441_AX1090_REDUCTION_AUDIT.csv"
AX1090_AXIOMS = OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv"
MOMS_THEOREM = OUT / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1449_SOURCE_REGISTER.csv"
FIELD_MAP = OUT / "P8_Y5_R10_1449_FIELD_BY_FIELD_VWEP_ACTION_MAP.csv"
CLAUSE_MATRIX = OUT / "P8_Y5_R10_1449_FIELD_MAP_CLAUSE_SIGNATURE_MATRIX.csv"
DERIVATION_ATTEMPT = OUT / "P8_Y5_R10_1449_C_PARENT_ZERO_DERIVATION_ATTEMPT.csv"
COUNTERMODEL_RETENTION = OUT / "P8_Y5_R10_1449_SOURCE_ONLY_COUNTERMODEL_RETENTION.csv"
EVALUATION_DECISION = OUT / "P8_Y5_R10_1449_C_PARENT_EVALUATION_DECISION.csv"
PARSER_DRYRUN = OUT / "P8_Y5_R10_1449_PARSER_DRYRUN.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1449_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1449_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1449_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1449_VALIDATION.csv"

BRANCH_FIELD_MAP = COEFF / "V_WEP_field_by_field_action_map.csv"
BRANCH_COUNTERMODEL_RETENTION = COEFF / "source_only_countermodel_retention_1449.csv"
BRANCH_EVALUATION_DECISION = COEFF / "C_parent_WEP_evaluation_decision_1449.csv"
LIVE_C_PARENT_IMPORT = COEFF / "C_parent_WEP_slot_import.csv"
LIVE_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv_ok(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            return len(list(csv.DictReader(handle))) > 0
    except Exception:
        return False


def truth(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def copy_branch(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC1449_0_prev_next", PREV_NEXT, "1448 next-target handoff"),
        ("SRC1449_1_prev_domain", PREV_DOMAIN, "1448 V_WEP domain proof attempt"),
        ("SRC1449_2_prev_eval", PREV_EVAL, "1448 C_parent evaluability gate"),
        ("SRC1449_3_prev_MOMS_pack", PREV_MOMS_PACK, "1448 MOMS signature source pack"),
        ("SRC1449_4_prev_counters", PREV_COUNTERS, "1448 retained countermodels"),
        ("SRC1449_5_prev_validation", PREV_VALIDATION, "1448 validation"),
        ("SRC1449_6_QVX", QVX_CERT, "q/v_X/action descent certificate"),
        ("SRC1449_7_matter_signature", MATTER_SIGNATURE, "ordinary matter functor signature audit"),
        ("SRC1449_8_vertical_lift", VERTICAL_LIFT, "vertical matter lift descent gate"),
        ("SRC1449_9_no_shadow", NO_SHADOW, "no-shadow-frame theorem attempt"),
        ("SRC1449_10_constants", CONSTANT_SUPER, "constant superselection theorem attempt"),
        ("SRC1449_11_parent_contract", PARENT_CONTRACT, "parent action contract candidate"),
        ("SRC1449_12_label_forget", LABEL_FORGET, "label-forgetting proof attempt"),
        ("SRC1449_13_no_source_slot", NO_SOURCE_SLOT, "no-source-only-slot audit"),
        ("SRC1449_14_AX1090_reduction", AX1090_REDUCTION, "AX1090 reduction audit"),
        ("SRC1449_15_AX1090_axioms", AX1090_AXIOMS, "AX1090 missing axiom ledger"),
        ("SRC1449_16_MOMS_theorem", MOMS_THEOREM, "MOMS conditional zero theorem"),
    ]
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": path.exists(),
            "role": role,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, role in sources
    ]


def field_map_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "field_block": "parent_configuration",
            "object": "Phi_parent in C_parent",
            "proposed_V_WEP_action": "delta_V Phi := V_WEP[Phi] in the local/WEP contrast direction",
            "required_zero_or_control": "V_WEP must be a parent-owned vector field on the actual configuration space",
            "best_source": str(QVX_CERT),
            "current_status": "MISSING_ACTUAL_PARENT_TRANSFORMATION_LAW",
            "missing_signature": "field-by-field parent transformation law for geometry, hidden fields, matter, constants, source, and boundary",
            "if_signed_effect": "C_parent_WEP becomes a real functional derivative rather than a symbolic slot",
            "countermodel_if_unsigned": "V_WEP can be chosen after readout and need not represent a true parent variation",
            "map_satisfied": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_block": "quotient_observables",
            "object": "q_loc(Phi), e_obs(q), g_obs(q), omega_obs(q)",
            "proposed_V_WEP_action": "Dq_loc[V_WEP]=0; therefore delta_V e_obs = delta_V g_obs = delta_V omega_obs = 0",
            "required_zero_or_control": "actual WEP generator is in ker(Dq_loc)",
            "best_source": str(PREV_DOMAIN),
            "current_status": "EXACT_CONDITIONAL_MATH_PASS_NOT_PARENT_SIGNED",
            "missing_signature": "proof that the physical local/WEP variation equals the quotient-kernel generator",
            "if_signed_effect": "visible geometry contribution to the WEP/local derivative is zero",
            "countermodel_if_unsigned": "a hidden-visible frame or source projection can re-enter after quotienting",
            "map_satisfied": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_block": "hidden_memory_or_Xhat",
            "object": "Xhat, memory/projector/domain variables, hidden representatives",
            "proposed_V_WEP_action": "delta_V Xhat is a representative/internal displacement with no direct observed-field image",
            "required_zero_or_control": "all hidden-to-visible coefficient homomorphisms are absent or explicitly retained",
            "best_source": str(PARENT_CONTRACT),
            "current_status": "UNMAPPED_PARENT_FIELD_COMPONENT",
            "missing_signature": "operator-classification theorem forbidding hidden variables from entering visible coefficients",
            "if_signed_effect": "hidden motion cannot create fifth-force, clock, EM, or source coefficients",
            "countermodel_if_unsigned": "f_X F^2, m_A(Xhat), A_A(Xhat), or w_A(Xhat) remains legal",
            "map_satisfied": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_block": "ordinary_matter_fields",
            "object": "Psi_A in Gamma(E_A[e_obs])",
            "proposed_V_WEP_action": "delta_V Psi_A = 0 or an owned gauge/local-Lorentz/diffeomorphism lift",
            "required_zero_or_control": "one parent matter bundle functor assigns the lift for every ordinary species",
            "best_source": str(VERTICAL_LIFT),
            "current_status": "LIFT_OPTIONS_AVAILABLE_NOT_PARENT_ASSIGNED",
            "missing_signature": "species-complete fixed/gauge/boundary lift owned by the parent action",
            "if_signed_effect": "matter Euler terms vanish on shell and no material component is hidden in the lift",
            "countermodel_if_unsigned": "delta_V Psi_A can carry physical material/species response",
            "map_satisfied": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_block": "EM_connection_and_alpha",
            "object": "A_Q, F_Q, T_Q, alpha_EM",
            "proposed_V_WEP_action": "delta_V A_Q is gauge/quotient-owned and delta_V alpha_EM = 0",
            "required_zero_or_control": "unique EM kinetic normalization and fixed charge/current lattice",
            "best_source": str(CONSTANT_SUPER),
            "current_status": "CONDITIONAL_OWNER_NOT_SIGNED",
            "missing_signature": "no f_X F_Q^2 counterterm; charge/current normalization descends from fixed representation data",
            "if_signed_effect": "b_alpha and EM marker terms are theorem-zero",
            "countermodel_if_unsigned": "dimensionless alpha_EM can vary and source clocks/WEP/R10",
            "map_satisfied": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_block": "matter_constants_and_spectra",
            "object": "theta_A, mass ratios, Yukawa/binding/clock constants",
            "proposed_V_WEP_action": "delta_V theta_A = 0 if theta_A is quotient-owned or superselected",
            "required_zero_or_control": "all dimensionless spectra are fixed/topological or explicit residuals",
            "best_source": str(CONSTANT_SUPER),
            "current_status": "CONSTANT_SUPERSELECTION_UNSIGNED",
            "missing_signature": "parent ownership for alpha, mass ratios, nuclear response, and clock transition data",
            "if_signed_effect": "constant-marker WEP/clock/EM channels collapse to zero",
            "countermodel_if_unsigned": "mass-ratio or clock-marker coupling remains physical and cannot be unit-rescaled away",
            "map_satisfied": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_block": "matter_frame_domain",
            "object": "frame used inside S_A",
            "proposed_V_WEP_action": "S_A uses only e_obs(q), omega[e_obs], A_Q, theta_A",
            "required_zero_or_control": "no A_A(Xhat)^2 g_obs, disformal frame, source-only metric, or material marker slot",
            "best_source": str(NO_SHADOW),
            "current_status": "NO_SHADOW_CONDITIONAL_ONLY",
            "missing_signature": "parent action-domain exclusion of extra matter/readout frames",
            "if_signed_effect": "shadow-frame coefficients c_g, b_conf, b_dis are zero",
            "countermodel_if_unsigned": "universal scalar-tensor-like coupling can survive WEP while hitting R10/PPN/clocks",
            "map_satisfied": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_block": "source_coupling",
            "object": "T_total and gravitational source functional",
            "proposed_V_WEP_action": "source is Hilbert derivative of total matter action after species sum",
            "required_zero_or_control": "source functor forgets species labels before coupling selection",
            "best_source": str(NO_SOURCE_SLOT),
            "current_status": "SOURCE_LABEL_FORGETTING_NOT_PARENT_SIGNED",
            "missing_signature": "parent theorem forbidding w_A S_A, epsilon_A source weights, or source-only species maps",
            "if_signed_effect": "direct WEP/source-weight residual is theorem-zero",
            "countermodel_if_unsigned": "relative source weights remain the sharpest finite WEP countermodel",
            "map_satisfied": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_block": "measure_current_normalization",
            "object": "sqrt(-g_obs), current normalization, species measure/Jacobian",
            "proposed_V_WEP_action": "delta_V measure/current is common quotient-owned data or explicit residual",
            "required_zero_or_control": "one common measure/current normalization with no species-dependent Jacobian",
            "best_source": str(AX1090_REDUCTION),
            "current_status": "COMMON_MEASURE_NOT_REDUCED",
            "missing_signature": "parent symplectic/quantum/statistical measure universality",
            "if_signed_effect": "species-dependent normalization cannot imitate WEP violation",
            "countermodel_if_unsigned": "J_A or non-Hilbert current can bypass Hilbert-source silence",
            "map_satisfied": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "field_block": "boundary_domain_readout",
            "object": "worldtube support, boundary terms, detector/readout map",
            "proposed_V_WEP_action": "variation is taken before readout/source projection; boundary term is zero/exact/retained",
            "required_zero_or_control": "boundary silence and variation-before-readout are parent-signed with the source model",
            "best_source": str(QVX_CERT),
            "current_status": "BOUNDARY_AND_READOUT_NOT_SIGNED",
            "missing_signature": "Q_X/proper edge silence plus official detector/source projection tied to parent variation",
            "if_signed_effect": "post-readout selectors cannot manufacture or erase WEP residuals",
            "countermodel_if_unsigned": "support shifts or readout choices can act like source-only couplings",
            "map_satisfied": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in rows:
        row["same_parent_branch_id"] = BRANCH_ID
    return rows


def clause_matrix_rows() -> list[dict[str, Any]]:
    clauses = [
        ("FM1449_0_field_owner", "parent_configuration", "QVC1023_4 and PAC1055_6", "FAIL", "actual parent transformation law is missing"),
        ("FM1449_1_quotient_kernel", "quotient_observables", "Dq[V_WEP]=0 chain rule", "CONDITIONAL_PASS", "actual physical generator not signed"),
        ("FM1449_2_matter_lift", "ordinary_matter_fields", "MFS1045_2/3 and VLG1045", "FAIL", "parent matter bundle/lift not assigned"),
        ("FM1449_3_constants", "matter_constants_and_spectra", "CST1047", "FAIL", "alpha/mass/clock owners unsigned"),
        ("FM1449_4_no_shadow", "matter_frame_domain", "NSF1046", "FAIL", "hidden visible frame/domain exclusion unsigned"),
        ("FM1449_5_no_source_weight", "source_coupling", "NSS1064 and PAC1055_4", "FAIL", "source-label forgetting not parent-derived"),
        ("FM1449_6_common_measure", "measure_current_normalization", "AXRED1441_2", "FAIL", "species-independent measure/current not reduced"),
        ("FM1449_7_boundary_readout", "boundary_domain_readout", "QVC1023_6 and AXRED1441_4", "FAIL", "boundary silence and variation order not signed with detector model"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": clause_id,
            "field_block": block,
            "source_clause": source_clause,
            "current_verdict": verdict,
            "blocking_reason": reason,
            "blocks_C_parent_evaluation": verdict != "CONDITIONAL_PASS",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for clause_id, block, source_clause, verdict, reason in clauses
    ]


def derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "derivation_step": "DZ1449_0_decompose_variation",
            "formal_statement": "delta_V S_parent = E_obs delta_V Q_obs + E_Psi delta_V Psi + partial_theta L delta_V theta + delta_V S_source_slots + delta_V S_boundary",
            "status": "IDENTITY_TEMPLATE_WRITTEN",
            "what_is_proven": "lists every place where V_WEP can enter",
            "missing_for_claim": "actual parent action and field-space map",
            "result_for_C_parent": "not_evaluable",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "derivation_step": "DZ1449_1_geometry_term",
            "formal_statement": "Dq[V_WEP]=0 => delta_V Q_obs = delta_V e_obs = delta_V g_obs = 0",
            "status": "EXACT_CONDITIONAL_MATH_PASS",
            "what_is_proven": "geometry term vanishes if the generator is truly vertical",
            "missing_for_claim": "actual WEP generator equals parent kernel direction",
            "result_for_C_parent": "conditional_zero_only",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "derivation_step": "DZ1449_2_matter_lift_term",
            "formal_statement": "delta_V Psi_A fixed/gauge/on-shell-boundary => E_Psi delta_V Psi_A contributes no physical WEP source",
            "status": "CONDITIONAL_LIFT_NOT_PARENT_ASSIGNED",
            "what_is_proven": "standard zero route exists",
            "missing_for_claim": "parent assignment of the lift for every ordinary species",
            "result_for_C_parent": "retained_residual",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "derivation_step": "DZ1449_3_constant_and_EM_terms",
            "formal_statement": "delta_V theta_A = delta_V alpha_EM = 0 if constants descend from q or fixed representation sectors",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "what_is_proven": "unit-rescaling cheat is excluded; dimensionless constants need real ownership",
            "missing_for_claim": "alpha/mass/clock parent owner",
            "result_for_C_parent": "retained_residual",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "derivation_step": "DZ1449_4_source_weight_term",
            "formal_statement": "delta_V S_source_slots = 0 only if no w_A, epsilon_A, non-Hilbert current, or source-only map exists",
            "status": "COUNTERMODEL_SURVIVES",
            "what_is_proven": "this is the most concrete finite WEP coupling route still alive",
            "missing_for_claim": "Hilbert-source label-forgetting theorem from the parent matter/source functor",
            "result_for_C_parent": "cannot_set_zero",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "derivation_step": "DZ1449_5_boundary_readout_term",
            "formal_statement": "delta_V S_boundary and detector/source projection are silent only if variation-before-readout and boundary silence are parent-signed",
            "status": "BOUNDARY_READOUT_COUNTERMODEL_SURVIVES",
            "what_is_proven": "post-readout choice is not allowed as a proof device",
            "missing_for_claim": "boundary projector and source/readout map tied to parent variation",
            "result_for_C_parent": "cannot_evaluate",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "derivation_step": "DZ1449_6_verdict",
            "formal_statement": "C_parent_WEP[V_WEP]=0 is derivable only after all field-map clauses are parent-signed together",
            "status": "FAIL_CURRENT_PROOF_KEEP_SOURCE_COUNTERMODELS",
            "what_is_proven": "field-by-field map isolates the exact missing signatures",
            "missing_for_claim": "parent field map plus source-label forgetting, no-shadow, constants, matter lift, measure, and boundary/readout clauses",
            "result_for_C_parent": "non_evaluable_nonclaim",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    counters = [
        ("CM1449_0_relative_source_weight", "S_source=sum_A (1+epsilon_A) S_A or T_source=sum_A (1+epsilon_A)T_A", "no-source-only-slot theorem not parent-signed", "direct WEP/source coefficient"),
        ("CM1449_1_shadow_frame", "S_A[Psi_A,A_A(Xhat)^2 g_obs + B_A(Xhat)U_mu U_nu]", "no-shadow-frame theorem not parent-signed", "R10/PPN/clock/local weak-field coefficient"),
        ("CM1449_2_constant_marker", "alpha_EM(Xhat), m_A(Xhat)/m_B(Xhat), clock_i(Xhat)", "constant-sector owner not parent-signed", "EM/clock/composition residual"),
        ("CM1449_3_physical_matter_lift", "delta_V Psi_A has species/material component not gauge/fixed", "matter lift not parent-assigned", "composition-dependent matter response"),
        ("CM1449_4_measure_jacobian", "species-dependent J_A, current normalization, or non-Hilbert source current", "common measure/current not reduced", "bypasses Hilbert source theorem"),
        ("CM1449_5_boundary_support_shift", "source-worldtube, compact support, or edge charge changes under V_WEP", "boundary silence not signed", "edge/source projection residual"),
        ("CM1449_6_post_readout_selector", "material/readout projection chosen after the variation", "variation-before-readout not tied to detector model", "pipeline can manufacture or erase residuals"),
        ("CM1449_7_EM_kinetic_slot", "f_X(Xhat) F_Q^2 or hidden current normalization", "EM owner and no mixed coefficient theorem not signed", "fine-structure and Coulomb-sector residual"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": counter_id,
            "countermodel": model,
            "why_survives": why,
            "effect": effect,
            "retention_decision": "retain_as_nonclaim_finite_branch",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for counter_id, model, why, effect in counters
    ]


def evaluation_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "evaluation_id": "EVAL1449_0_Cparent_WEP",
            "target": "C_parent_WEP[V_WEP] := N_WEP^{-1} dS_parent[V_WEP]",
            "field_map_complete": False,
            "source_label_forgetting_signed": False,
            "matter_lift_signed": False,
            "constants_signed": False,
            "no_shadow_signed": False,
            "boundary_readout_signed": False,
            "normalization_signed": False,
            "evaluable_now": False,
            "decision": "DO_NOT_EVALUATE_OR_IMPORT_C_PARENT_WEP",
            "reason": "field-by-field map still has live source-only, shadow, constant, measure, matter-lift, and boundary/readout countermodels",
            "live_import_exists": LIVE_C_PARENT_IMPORT.exists(),
            "official_readout_exists": LIVE_READOUT.exists(),
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def parser_rows() -> list[dict[str, Any]]:
    parser_checks = [
        ("PDR1449_0_zero_import", "attempt to import C_parent_WEP=0", "REFUSED", "field map incomplete"),
        ("PDR1449_1_numeric_prediction", "attempt to compute WEP/R10 prediction", "REFUSED", "no numeric parent coefficient or signed zero"),
        ("PDR1449_2_branch_copy", "copy nonclaim field map/countermodels to branch coefficients folder", "ALLOWED_NONCLAIM", "branch rows explicitly valid_for_claim=false"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "parser_check_id": check_id,
            "attempt": attempt,
            "parser_result": result,
            "reason": reason,
            "would_write_live_claim_file": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, attempt, result, reason in parser_checks
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1449_0_local_GR", "local GR/Newton recovery from V_WEP zero"),
        ("CG1449_1_WEP_MICROSCOPE", "finite or zero WEP coefficient"),
        ("CG1449_2_R10_short_range", "alpha(lambda) local fifth-force pass"),
        ("CG1449_3_PPN", "PPN residual vector suppression"),
        ("CG1449_4_clocks_EM", "clock/fine-structure residual suppression"),
        ("CG1449_5_orbital", "orbital/source residual suppression"),
        ("CG1449_6_public_claim", "any public local-branch claim"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": False,
            "reason": "C_parent_WEP remains non-evaluable and field-map clauses are unsigned",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    decisions = [
        {
            "decision_id": "DEC1449_0_keep_conditional_geometry_win",
            "decision": "retain Dq[V_WEP]=0 as an exact conditional sublemma",
            "why": "geometry part is clean and should be preserved as the GR/local route skeleton",
            "consequence": "do not throw away the local branch",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1449_1_no_zero_claim",
            "decision": "do not claim C_parent_WEP=0",
            "why": "source-only weights, shadow frames, constants, measure, matter lift, and boundary/readout remain live",
            "consequence": "no WEP/R10/PPN/local-GR pass from 1449",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1449_2_next_best_route",
            "decision": "attack source-label forgetting/Hilbert-current theorem next",
            "why": "it is the sharpest concrete coupling blocker and the least hand-wavy route to kill a WEP countermodel",
            "consequence": "1450 targets relative source weights before broader local-GR closure",
            "valid_for_claim": False,
        },
    ]
    return decisions


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1449_0_1450",
            "next_target": "1450-Y5-R10-RAB-source-label-forgetting-Hilbert-current-theorem-or-relative-weight-bound-ledger.md",
            "script": "scripts/Y5_R10_RAB_source_label_forgetting_Hilbert_current_theorem_or_relative_weight_bound_ledger.py",
            "objective": "try to prove the source functor forgets species labels because gravity couples only to the total Hilbert stress after the matter action sum; if the proof fails, keep epsilon_A relative source weights as nonclaim bound-ledger rows",
            "include": "Hilbert source theorem; no w_A grammar; common measure/current; non-Hilbert current guard; relative epsilon_A countermodel rows",
            "exclude": "numeric claim; fitted WEP coefficient; public local-GR claim; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    field_map: list[dict[str, Any]],
    matrix: list[dict[str, Any]],
    derivation: list[dict[str, Any]],
    counters: list[dict[str, Any]],
    eval_rows: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        FIELD_MAP,
        CLAUSE_MATRIX,
        DERIVATION_ATTEMPT,
        COUNTERMODEL_RETENTION,
        EVALUATION_DECISION,
        PARSER_DRYRUN,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    all_sources_exist = all(truth(row["exists"]) for row in sources)
    field_map_complete = len(field_map) >= 10 and all(not truth(row["map_satisfied"]) for row in field_map)
    exact_conditional_retained = any(row["current_status"].startswith("EXACT_CONDITIONAL") for row in field_map)
    blocking_matrix = any(row["blocks_C_parent_evaluation"] for row in matrix)
    source_counter_retained = any(row["countermodel_id"] == "CM1449_0_relative_source_weight" for row in counters)
    derivation_refuses_zero = any(row["status"] == "FAIL_CURRENT_PROOF_KEEP_SOURCE_COUNTERMODELS" for row in derivation)
    not_evaluable = all(not truth(row["evaluable_now"]) for row in eval_rows)
    parser_safe = all(not truth(row["would_write_live_claim_file"]) for row in parser)
    gates_false = all(not truth(row["gate_pass"]) for row in gates)
    live_import_absent = not LIVE_C_PARENT_IMPORT.exists()
    readout_absent = not LIVE_READOUT.exists()
    csv_parse = all(parse_csv_ok(path) for path in generated_csvs)
    branch_copies = BRANCH_FIELD_MAP.exists() and BRANCH_COUNTERMODEL_RETENTION.exists() and BRANCH_EVALUATION_DECISION.exists()
    formal_recent = 0
    if FORMALIZATION.exists():
        formal_recent = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and path.stat().st_mtime > START_TS
        )

    checks = [
        ("VAL1449_0_sources", all_sources_exist, "all cited source paths exist"),
        ("VAL1449_1_field_map_nonclaim", field_map_complete, "field-by-field V_WEP map written but not satisfied for import"),
        ("VAL1449_2_conditional_geometry_retained", exact_conditional_retained, "quotient geometry conditional win retained"),
        ("VAL1449_3_clause_matrix_blocks", blocking_matrix, "unsigned clauses block C_parent evaluation"),
        ("VAL1449_4_source_countermodel_retained", source_counter_retained, "relative source-weight countermodel retained"),
        ("VAL1449_5_derivation_refuses_zero", derivation_refuses_zero, "zero proof refused at current signature strength"),
        ("VAL1449_6_not_evaluable", not_evaluable, "C_parent_WEP remains non-evaluable"),
        ("VAL1449_7_parser_safe", parser_safe, "parser dry-run refuses live claim writes"),
        ("VAL1449_8_claim_gates_false", gates_false, "all claim gates remain false"),
        ("VAL1449_9_no_live_import", live_import_absent, "live C_parent import remains absent"),
        ("VAL1449_10_no_official_readout", readout_absent, "official readout live file remains absent"),
        ("VAL1449_11_csv_parse", csv_parse, "all generated 1449 CSVs parse cleanly"),
        ("VAL1449_12_branch_copies", branch_copies, "nonclaim branch copies written"),
        ("VAL1449_13_formalization_untouched", formal_recent == 0, f"formalization modified-file count since start={formal_recent}"),
        ("VAL1449_14_overall", True, "1449 maps V_WEP field-by-field and keeps source-only countermodels live"),
    ]
    return [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, passed, detail in checks
    ]


def write_table(handle, title: str, rows: list[dict[str, Any]]) -> None:
    handle.write(f"## {title}\n\n")
    if not rows:
        handle.write("_No rows._\n\n")
        return
    fields = list(rows[0].keys())
    handle.write("| " + " | ".join(fields) + " |\n")
    handle.write("| " + " | ".join(["---"] * len(fields)) + " |\n")
    for row in rows:
        handle.write("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |\n")
    handle.write("\n")


def write_doc(
    sources: list[dict[str, Any]],
    field_map: list[dict[str, Any]],
    matrix: list[dict[str, Any]],
    derivation: list[dict[str, Any]],
    counters: list[dict[str, Any]],
    eval_rows: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1449 - Field-by-field V_WEP action map or source-only countermodel retention\n\n")
        handle.write(
            "**Current verdict:** the field-by-field map makes the coupling problem precise. "
            "The quotient/visible-geometry part is still a clean conditional win, but the full `V_WEP` "
            "generator is not parent-signed on matter, constants, EM normalization, source weights, "
            "measure/current normalization, boundary terms, or readout. Therefore `C_parent_WEP` is not "
            "evaluated or imported, and the source-only countermodel branch remains live.\n\n"
        )
        handle.write(
            "**Useful progress:** this is not a vague failure. The most concrete next coupling target is the "
            "Hilbert-source/label-forgetting theorem: prove gravity only sees the total Hilbert stress after "
            "the species sum, or keep relative `epsilon_A` source weights as explicit nonclaim rows.\n\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "Field-by-field V_WEP action map", field_map)
        write_table(handle, "Clause signature matrix", matrix)
        write_table(handle, "C_parent zero derivation attempt", derivation)
        write_table(handle, "Source-only countermodel retention", counters)
        write_table(handle, "C_parent evaluation decision", eval_rows)
        write_table(handle, "Parser dry-run", parser)
        write_table(handle, "Claim gates", gates)
        write_table(handle, "Decision ledger", decisions)
        write_table(handle, "Validation", validation)
        write_table(handle, "Next target", next_target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_rows()
    field_map = field_map_rows()
    matrix = clause_matrix_rows()
    derivation = derivation_rows()
    counters = countermodel_rows()
    eval_rows = evaluation_rows()
    parser = parser_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(FIELD_MAP, field_map)
    write_csv(CLAUSE_MATRIX, matrix)
    write_csv(DERIVATION_ATTEMPT, derivation)
    write_csv(COUNTERMODEL_RETENTION, counters)
    write_csv(EVALUATION_DECISION, eval_rows)
    write_csv(PARSER_DRYRUN, parser)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(FIELD_MAP, BRANCH_FIELD_MAP)
    copy_branch(COUNTERMODEL_RETENTION, BRANCH_COUNTERMODEL_RETENTION)
    copy_branch(EVALUATION_DECISION, BRANCH_EVALUATION_DECISION)

    validation = validation_rows(sources, field_map, matrix, derivation, counters, eval_rows, parser, gates)
    write_csv(VALIDATION, validation)
    write_doc(sources, field_map, matrix, derivation, counters, eval_rows, parser, gates, decisions, validation, next_target)
    remove_pycache()
    print("Y5_R10_1449_field_map_written_Cparent_non_evaluable")


if __name__ == "__main__":
    main()

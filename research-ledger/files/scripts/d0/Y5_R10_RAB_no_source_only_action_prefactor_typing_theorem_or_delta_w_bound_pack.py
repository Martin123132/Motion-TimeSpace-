from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1479"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1479-Y5-R10-RAB-no-source-only-action-prefactor-typing-theorem-or-delta-w-bound-pack.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1478_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1478_VALIDATION.csv"
PREV_SYNTAX = OUT / "P8_Y5_R10_1478_PARENT_ACTION_SYNTAX_CHECKLIST.csv"
PREV_PROOF = OUT / "P8_Y5_R10_1478_SINGLE_ACTION_DENSITY_LINE_PROOF_ATTEMPT.csv"
PREV_BASIS = OUT / "P8_Y5_R10_1478_COMPONENT_DELTA_W_BASIS_NONCLAIM.csv"
PREV_VECTOR = OUT / "P8_Y5_R10_1478_COMPONENT_DELTA_W_VECTOR_INPUT_TEMPLATE_NONCLAIM.csv"
PREV_ARENAS = OUT / "P8_Y5_R10_1478_COMPONENT_DELTA_W_ARENA_PROJECTION_MATRIX.csv"

OLT_1066 = OUT / "P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv"
ODR_1066 = OUT / "P8_Y5_R10_1066_OPERATOR_DOMAIN_RULE_AUDIT.csv"
SSE_1066 = OUT / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv"
PAC_1055 = OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv"
ZC_1054 = OUT / "P8_Y5_R10_1054_ZERO_THEOREM_CLAUSE_AUDIT.csv"
OBS_1054 = OUT / "P8_Y5_R10_1054_COUNTEREXAMPLE_OBSTRUCTION_LEDGER.csv"
TC_1031 = OUT / "P8_Y5_R10_1031_TERMINALITY_INSUFFICIENCY_COUNTEREXAMPLES.csv"
ISO_1051 = OUT / "P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv"
PREM_1062 = OUT / "P8_Y5_R10_1062_PREMISE_SIGNATURE_AUDIT.csv"
THM_1062 = OUT / "P8_Y5_R10_1062_PARENT_PRODUCT_THEOREM_ATTEMPT.csv"
THM_1063 = OUT / "P8_Y5_R10_1063_SOURCE_FORGETTING_THEOREM_ATTEMPT.csv"
RWP_1063 = OUT / "P8_Y5_R10_1063_RELATIVE_WEIGHT_PRIOR_MATRIX.csv"
NSS_1214 = OUT / "P8_Y5_R10_1214_NO_SOURCE_ONLY_SLOT_SIGNATURE_AUDIT.csv"
DSB_1214 = OUT / "P8_Y5_R10_1214_DELTA_SPECIES_BOUND_FILL.csv"
ARENA_1214 = OUT / "P8_Y5_R10_1214_ARENA_PROJECTION_LEDGER.csv"
NSP_1333 = OUT / "P8_Y5_R10_1333_NO_SOURCE_PREFACTOR_DERIVATION_ATTEMPT.csv"
EB_1333 = OUT / "P8_Y5_R10_1333_ELECTRON_RESIDUAL_BOUND_CONTRACT.csv"
ADM_1426 = OUT / "P8_Y5_R10_1426_ACTIVE_SOURCE_PREFACTOR_ADMISSIBILITY_AUDIT.csv"
PACK_1426 = OUT / "P8_Y5_R10_1426_FINITE_WEP_COEFFICIENT_INPUT_PACK.csv"
OG_1451 = OUT / "P8_Y5_R10_1451_NO_SOURCE_ONLY_SLOT_OPERATOR_GRAMMAR_THEOREM_ATTEMPT.csv"
REQ_1451 = OUT / "P8_Y5_R10_1451_EPSILON_A_BOUND_INPUT_REQUIREMENTS.csv"
ANCH_1451 = OUT / "P8_Y5_R10_1451_ARENA_BOUND_ANCHOR_MAP_NONCLAIM.csv"
RSC_1416 = OUT / "P8_Y5_R10_1416_FIRST_RSOURCE_COEFFICIENT_ROW.csv"
CM_1416 = OUT / "P8_Y5_R10_1416_SOURCE_SLOT_COUNTERMODEL_LEDGER.csv"
HT_1450 = OUT / "P8_Y5_R10_1450_HILBERT_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv"
MAT_983 = OUT / "P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv"
MAT_1080 = OUT / "P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv"
COMP_1232 = OUT / "P8_Y5_R10_1232_COMPONENT_FRACTION_FORMULA_LEDGER.csv"
FSP_1232 = OUT / "P8_Y5_R10_1232_TIPT_COMPONENT_FRACTION_SOURCE_PACK.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1479_SOURCE_REGISTER.csv"
TYPING_THEOREM = OUT / "P8_Y5_R10_1479_NO_SOURCE_ONLY_ACTION_PREFACTOR_TYPING_THEOREM_ATTEMPT.csv"
HOM_AUDIT = OUT / "P8_Y5_R10_1479_HOM_SPECIES_TO_SOURCE_PREFACTOR_AUDIT.csv"
COUNTERMODELS = OUT / "P8_Y5_R10_1479_SOURCE_ONLY_PREFACTOR_COUNTERMODEL_LEDGER.csv"
BOUND_ANCHORS = OUT / "P8_Y5_R10_1479_DELTA_W_BOUND_ANCHOR_PACK_NONCLAIM.csv"
BOUND_INPUTS = OUT / "P8_Y5_R10_1479_DELTA_W_BOUND_INPUT_REQUIREMENTS.csv"
COMPONENT_BOUND_PACK = OUT / "P8_Y5_R10_1479_COMPONENT_DELTA_W_BOUND_PACK_NONCLAIM.csv"
CLAIM_FIREWALL = OUT / "P8_Y5_R10_1479_CLAIM_FIREWALL_AND_NO_BOUND_INVERSION.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1479_REDUCTION_GATES.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1479_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1479_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1479_VALIDATION.csv"

QUAR_THEOREM = QUARANTINE / "NO_SOURCE_ONLY_ACTION_PREFACTOR_TYPING_THEOREM_ATTEMPT_NONCLAIM.csv"
QUAR_PACK = QUARANTINE / "COMPONENT_DELTA_W_BOUND_PACK_NONCLAIM.csv"
BRANCH_THEOREM = COEFF / "no_source_only_prefactor_typing_theorem_nonclaim_1479.csv"
BRANCH_PACK = COEFF / "component_delta_w_bound_pack_nonclaim_1479.csv"
BRANCH_GATES = COEFF / "no_source_only_prefactor_reduction_gates_1479.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_csv(path: Path) -> bool:
    with path.open(newline="", encoding="utf-8") as handle:
        list(csv.DictReader(handle))
    return True


def copy_nonclaim(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC1479_0_prev_next", PREV_NEXT, "1478 handoff selecting no-source-only prefactor typing theorem or delta_w bound pack"),
        ("SRC1479_1_prev_validation", PREV_VALIDATION, "1478 validation baseline"),
        ("SRC1479_2_prev_syntax", PREV_SYNTAX, "parent action syntax checklist"),
        ("SRC1479_3_prev_proof", PREV_PROOF, "single action-density line proof attempt"),
        ("SRC1479_4_prev_basis", PREV_BASIS, "component delta_w basis"),
        ("SRC1479_5_prev_vector", PREV_VECTOR, "component vector template"),
        ("SRC1479_6_prev_arenas", PREV_ARENAS, "component arena projection matrix"),
        ("SRC1479_7_OLT1066", OLT_1066, "object-language typing audit"),
        ("SRC1479_8_ODR1066", ODR_1066, "operator-domain rule audit"),
        ("SRC1479_9_SSE1066", SSE_1066, "source scalar exclusion lemma"),
        ("SRC1479_10_PAC1055", PAC_1055, "parent action contract candidate"),
        ("SRC1479_11_ZC1054", ZC_1054, "zero theorem clause audit"),
        ("SRC1479_12_OBS1054", OBS_1054, "counterexample obstruction ledger"),
        ("SRC1479_13_TC1031", TC_1031, "terminality insufficiency counterexamples"),
        ("SRC1479_14_ISO1051", ISO_1051, "invariant scalar obstruction audit"),
        ("SRC1479_15_PREM1062", PREM_1062, "premise signature audit"),
        ("SRC1479_16_THM1062", THM_1062, "parent product theorem attempt"),
        ("SRC1479_17_THM1063", THM_1063, "source forgetting theorem attempt"),
        ("SRC1479_18_RWP1063", RWP_1063, "relative weight prior matrix"),
        ("SRC1479_19_NSS1214", NSS_1214, "no-source-only slot signature audit"),
        ("SRC1479_20_DSB1214", DSB_1214, "delta species bound fill"),
        ("SRC1479_21_ARENA1214", ARENA_1214, "arena projection ledger"),
        ("SRC1479_22_NSP1333", NSP_1333, "no source prefactor derivation attempt"),
        ("SRC1479_23_EB1333", EB_1333, "electron residual bound contract"),
        ("SRC1479_24_ADM1426", ADM_1426, "active source prefactor admissibility audit"),
        ("SRC1479_25_PACK1426", PACK_1426, "finite WEP coefficient input pack"),
        ("SRC1479_26_OG1451", OG_1451, "operator grammar theorem attempt"),
        ("SRC1479_27_REQ1451", REQ_1451, "epsilon_A bound input requirements"),
        ("SRC1479_28_ANCH1451", ANCH_1451, "arena bound anchor map"),
        ("SRC1479_29_RSC1416", RSC_1416, "first R_source coefficient row"),
        ("SRC1479_30_CM1416", CM_1416, "source slot countermodel ledger"),
        ("SRC1479_31_HT1450", HT_1450, "Hilbert source label-forgetting theorem attempt"),
        ("SRC1479_32_local_bounds", LOCAL_BOUNDS, "local bound anchors for WEP/clock/PPN/Gdot/R10"),
        ("SRC1479_33_MAT983", MAT_983, "MICROSCOPE material constituents"),
        ("SRC1479_34_MAT1080", MAT_1080, "material composition and tensor candidates"),
        ("SRC1479_35_COMP1232", COMP_1232, "component fraction formula ledger"),
        ("SRC1479_36_FSP1232", FSP_1232, "Ti/Pt component fraction source pack"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": source_id,
            "path_or_url": rel(path),
            "exists": path.exists(),
            "usage": usage,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, usage in sources
    ]


def typing_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NST1479_0_target",
            "claim_piece": "no source-only action/source prefactor slot",
            "formal_statement": "Hom_parent(species_label or hidden_marker, R_+^active-source-prefactor) is empty or common-constant only; terms sum_A w_A S_A are ill-typed unless w_A is a measured nongravitational parameter already in theta_A",
            "proof_move": "classify admissible parent arguments as geometry, matter fields, gauge/current data, representation constants, or universal constants",
            "status": "TARGET_EXACT",
            "if_signed": "relative delta_w_A source/action weights are theorem-zero modulo common calibration",
            "current_gap": "the object-language/admissibility principle is still a parent grammar contract, not derived from deeper MTS primitives",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NST1479_1_conditional_typing",
            "claim_piece": "typed object-language theorem",
            "formal_statement": "If Arg(S_parent) is restricted to typed observable geometry, dynamical matter fields, gauge/current data, fixed representation data, and universal constants, then inert source-only w_A is not an admissible argument",
            "proof_move": "combine OLT1066_0..6, SSE1066_0..5, and OG1451_0..6",
            "status": "EXACT_CONDITIONAL_META_THEOREM",
            "if_signed": "source-only action prefactors vanish as syntax, not by tuning",
            "current_gap": "the restriction itself is not yet derived; hidden invariant and source-label countermodels remain live",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NST1479_2_operator_domain",
            "claim_piece": "no Hom into visible/source coefficient target",
            "formal_statement": "Allowed[Coeff(O_vis)] subset O(Q_obs) x Theta_rep x Level_EM and Hom(C_hid or species_label, Coeff_source-only) is absent/constant",
            "proof_move": "use ODR1066_0..4 and PAC1055_3 but test against ISO1051 scalar obstruction",
            "status": "POWERFUL_IF_SIGNED_NOT_REDUCED",
            "if_signed": "hidden/source marker coefficient maps cannot feed w_A, kappa_A, f_X, mass, clock, or source terms",
            "current_gap": "any surviving invariant scalar or species label can still feed continuous source coefficients unless target is forbidden",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NST1479_3_same_action_limit",
            "claim_piece": "same-action Hilbert source is insufficient alone",
            "formal_statement": "S_matter=sum_A w_A S_A still gives a same-action Hilbert source T_source=sum_A w_A T_A, so same-action/covariance/additivity do not ban relative prefactors",
            "proof_move": "retain HT1450_1..4, NSP1333_1..3, and CM1416_0",
            "status": "NO_GO_GUARD",
            "if_signed": "prevents false proof by covariance or classical EOM scaling",
            "current_gap": "none; guard remains active",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "NST1479_4_verdict",
            "claim_piece": "no-source-only prefactor proof status",
            "formal_statement": "The theorem is exact as a typing/grammar condition but not parent-derived in the current corpus",
            "proof_move": "refuse theorem-zero promotion and require source-ready delta_w bound/acquisition pack",
            "status": "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED",
            "if_signed": "CI1474_1 source-weight residual could move toward theorem-zero",
            "current_gap": "primitive parent object language, no hidden-visible Hom, common measure/current owner, and readout/no-spurion closure remain unsigned",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def hom_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("HOM1479_0_common_constant", "Hom(unit, R_+ common calibration)", "one derivative-silent common factor w_*", "CALIBRATION_ONLY_IF_UNIVERSAL_SILENT", "must be absorbed into measured G_N/GM only after no species/time/range/frame dependence", "PMO1463_2_common_calibration"),
        ("HOM1479_1_species_to_prefactor", "Hom(species label, R_+ active source/action prefactor)", "w_A S_A or kappa_A T_A", "FORBIDDEN_BY_CONTRACT_NOT_PARENT_DERIVED", "requires typed object-language theorem or common action-measure owner", "OLT1066_4_inert_source_scalar;OG1451_5_countermodel"),
        ("HOM1479_2_hidden_invariant_to_prefactor", "Hom(hidden invariant I_hid, R_+ source coefficient)", "w_A(I_hid), kappa(I_hid), or f_X(I_hid)", "OBSTRUCTION_SURVIVES", "requires hidden invariant algebra triviality or coefficient target exclusion", "ISO1051_0_hidden_scalar_I;ODR1066_1_continuous_target_obstruction"),
        ("HOM1479_3_marker_to_prefactor", "Hom(material/domain/boundary marker, R_+ source coefficient)", "w(marker_A, domain, boundary)", "OBSTRUCTION_SURVIVES", "requires no-marker/no-spurion closure and readout no-reentry", "ISO1051_3_domain_marker;OBS1054_4_radiative_readout"),
        ("HOM1479_4_current_to_prefactor", "Hom(current label, R_+ source current normalization)", "J_A -> c_A J_A or beta_source,A", "CURRENT_OWNER_UNSIGNED", "requires current owner and Hilbert/non-Hilbert source split", "RSC1416_1_current_rescaling;CM1416_2_current_rescaling"),
        ("HOM1479_5_readout_to_prefactor", "Hom(readout/source-worldtube label, R_+ active source weight)", "post-variation source/readout selector", "READOUT_TRANSFER_UNSIGNED", "requires variation-before-readout plus official/source-worldtube transfer", "SSE1066_2_variation_before_readout;HT1450_5_nonHilbert_guard"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "hom_id": hom_id,
            "domain_target": domain_target,
            "example": example,
            "current_status": status,
            "required_to_close": required,
            "source_anchor": anchor,
            "theorem_zero_allowed_now": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for hom_id, domain_target, example, status, required, anchor in rows
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    countermodels = [
        ("CM1479_0_wA_action", "S_matter=sum_A w_A S_A", "covariant/additive and can preserve isolated EOM form while changing Hilbert source", "delta_w_component_vector; WEP/source; Newton/local_GR", "CM1416_0_wA_action;NSP1333_2_same_action"),
        ("CM1479_1_kappaA_source", "F((T_A,A))=kappa_A T_A", "source labels can survive if source functor domain is labelled pairs", "source-label forgetting; WEP/R10 source charge", "OBS1054_3_source_labels;THM1063_0_target"),
        ("CM1479_2_hidden_marker_weight", "w_A=w(marker_A,domain,boundary,I_hid)", "marker/domain scalar can smuggle source weight unless coefficient targets are sealed", "marker/domain residual; clock/WEP/source", "ISO1051_3_domain_marker;CM1416_3_hidden_marker"),
        ("CM1479_3_current_rescaling", "J_A -> c_A J_A or beta_source,A", "current/source normalization owner is not signed", "current_rescaling_residual; PPN/local_GR", "RSC1416_1_current_rescaling;CM1416_2_current_rescaling"),
        ("CM1479_4_nonHilbert_readout", "J_src=T_Hilbert+sum_A zeta_A J_NH,A", "non-Hilbert/readout currents have not been proven absent/exact/projected silent", "zeta_A; local conservation/PPN", "HT1450_5_nonHilbert_guard;CM1416_4_readout_current"),
        ("CM1479_5_terminal_labels", "terminal visible metric with labels retained in matter/source data", "terminality does not erase labels or coefficient data before action evaluation", "object-language typing; no-source-only Hom", "TC1031_1_terminal_with_labels"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": countermodel_id,
            "countermodel": countermodel,
            "why_survives": why,
            "blocks": blocks,
            "source_anchor": source_anchor,
            "retained": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for countermodel_id, countermodel, why, blocks, source_anchor in countermodels
    ]


def bound_anchor_rows() -> list[dict[str, Any]]:
    anchors = [
        ("BAN1479_0_WEP", "WEP/MICROSCOPE Ti-Pt", "R1_WEP_source_charge", "2.8e-15", "dimensionless", rel(LOCAL_BOUNDS), "numeric anchor for eta source-charge proxy; product/projection missing"),
        ("BAN1479_1_clock", "clock/redshift", "R2_clock_redshift", "2.48e-05", "dimensionless", rel(LOCAL_BOUNDS), "guard only; cannot screen WEP/source residual"),
        ("BAN1479_2_PPN_gamma", "PPN gamma", "R3_gamma", "2.3e-05", "dimensionless", rel(LOCAL_BOUNDS), "needs source-normalization to gamma projection"),
        ("BAN1479_3_PPN_beta", "PPN beta", "R4_beta", "7.8e-05", "dimensionless", rel(LOCAL_BOUNDS), "needs source-normalization to beta projection"),
        ("BAN1479_4_Gdot", "Newton/GM time drift", "R9_Gdot", "9.6e-15", "yr^-1", rel(LOCAL_BOUNDS), "needs time/worldtube source map"),
        ("BAN1479_5_R10", "R10 inverse-square", "R10_fifth_force", "alpha(lambda)", "range-dependent", rel(LOCAL_BOUNDS), "symbolic curve anchor only; real curve/kernel required"),
        ("BAN1479_6_electron_proxy", "WEP electron component proxy", "EB1333_0_unit_kernel_electron_prefactor", "8.948213306283e-11", "dimensionless coefficient under unit-kernel smoke assumptions", rel(EB_1333), "finite proxy only; tau/readout/source normalization missing"),
        ("BAN1479_7_DD_alpha_smoke", "external DD alpha/Coulomb smoke", "PACK1426_6_DD_alpha_pressure", "1.407170315973e-12", "external coefficient scale", rel(PACK_1426), "external smoke not MTS parent basis"),
        ("BAN1479_8_DD_surface_smoke", "external DD surface smoke", "PACK1426_7_DD_surface_pressure", "8.468280557212e-13", "external coefficient scale", rel(PACK_1426), "external smoke not MTS parent basis"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "anchor_id": anchor_id,
            "arena_or_channel": arena,
            "source_row": row,
            "bound_value": value,
            "bound_units": units,
            "source_path": source,
            "why_nonclaim": why,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for anchor_id, arena, row, value, units, source, why in anchors
    ]


def bound_input_rows() -> list[dict[str, Any]]:
    requirements = [
        ("BIN1479_0_parent_basis", "parent delta_w component basis and normalization", "same basis across WEP/R10/PPN/clock/orbital/local_GR", "MISSING_PARENT_COUPLING_BASIS", rel(RSC_1416), "RSC1416_2_parent_basis"),
        ("BIN1479_1_component_values", "delta_w_vec values or theorem-zero certificates", "dimensionless component vector with uncertainty/covariance", "MISSING_COMPONENT_VECTOR", rel(PREV_VECTOR), "CDW1478_0_parent_component_vector"),
        ("BIN1479_2_material_tensor", "Ti/Pt source/test material response tensor", "claim-grade component fractions, isotope/alloy averaging, no double counting", "MISSING_FULL_PARENT_MATERIAL_TENSOR", rel(FSP_1232), "FSP1232_0 through FSP1232_7"),
        ("BIN1479_3_projection_kernel", "arena projection kernels", "tau_WEP, tau_R10(lambda), PPN response, clock/source, orbital/worldtube", "MISSING_ARENA_PROJECTIONS", rel(PREV_ARENAS), "ARE1478_0_WEP through ARE1478_5_local_GR"),
        ("BIN1479_4_no_cancellation", "covariance/no-cancellation envelope", "norm/covariance policy for component cancellations", "MISSING_NO_CANCELLATION_ENVELOPE", rel(PREV_VECTOR), "CDW1478_2_no_cancellation_covariance"),
        ("BIN1479_5_same_branch", "same-branch product convention", "source coefficient, material tensor, readout kernel, and bound in one convention", "MISSING_SAME_BRANCH_PRODUCT_CONVENTION", rel(PACK_1426), "PACK1426_0_C_parent;PACK1426_3_R_source;PACK1426_5_K_CMSM"),
        ("BIN1479_6_claim_grade_R10_curve", "real R10 alpha(lambda) bound curve", "digitized/sourced curve plus lambda convention", "MISSING_PROMOTED_CURVE_AND_KERNEL", rel(ANCH_1451), "ANCH1451_5_R10"),
        ("BIN1479_7_current_nonHilbert", "current/non-Hilbert residual definition", "J_NH,A absent/exact/projected silent or numeric zeta_A projection", "MISSING_NONHILBERT_CURRENT_OWNER", rel(REQ_1451), "REQ1451_6_nonHilbert"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": req_id,
            "required_input": required,
            "acceptance_rule": rule,
            "current_status": status,
            "source_path": source,
            "source_anchor": anchor,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for req_id, required, rule, status, source, anchor in requirements
    ]


def component_bound_pack_rows() -> list[dict[str, Any]]:
    rows = [
        ("CBP1479_0_delta_w_common", "delta_w_common", "common source/action calibration mode", "BAN1479_4_Gdot plus G_N/GM calibration split", "MISSING_TIME_RANGE_FRAME_SILENCE", "not scoreable; common mode only harmless after derivative-silence proof"),
        ("CBP1479_1_delta_w_e", "delta_w_e", "electron/lepton source-weight component", "BAN1479_6_electron_proxy", "PROXY_UNIT_KERNEL_ONLY", "finite proxy bound exists but tau/source/readout/product convention missing"),
        ("CBP1479_2_delta_w_EM", "delta_w_EM", "EM/Coulomb component", "BAN1479_7_DD_alpha_smoke", "EXTERNAL_SMOKE_NOT_PARENT_BASIS", "needs MTS parent EM/Coulomb component map"),
        ("CBP1479_3_delta_w_q", "delta_w_q", "light-quark/sigma component", "FSP1232_3_light_quark_fraction", "MISSING_PARENT_OR_PHENOMENOLOGICAL_BASIS", "needs sourced mass-decomposition basis"),
        ("CBP1479_4_delta_w_g", "delta_w_g", "QCD/gluon/bulk binding component", "FSP1232_4_QCD_gluon_fraction", "MISSING_PARENT_OR_PHENOMENOLOGICAL_BASIS", "bulk/common split unresolved"),
        ("CBP1479_5_delta_w_nuc", "delta_w_nuc", "nuclear binding/surface/asymmetry component", "BAN1479_8_DD_surface_smoke", "EXTERNAL_SMOKE_NOT_FULL_TENSOR", "needs isotope/alloy-averaged nuclear binding model"),
        ("CBP1479_6_delta_J_A", "delta_J_A", "species-only measure/Jacobian residual", "JEX1463_0_JA", "MISSING_MEASURE_OWNER_OR_BOUND", "requires measure theorem or numeric projection"),
        ("CBP1479_7_delta_c_A", "delta_c_A", "current/source normalization residual", "RSC1416_1_current_rescaling", "MISSING_CURRENT_OWNER_OR_COEFFICIENT", "requires current-owner theorem or finite c_A row"),
        ("CBP1479_8_zeta_A", "zeta_A", "non-Hilbert/readout source-current residual", "REQ1451_6_nonHilbert", "MISSING_NONHILBERT_CURRENT_OWNER", "requires J_NH definition and projection/silence proof"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "pack_id": pack_id,
            "component": component,
            "meaning": meaning,
            "best_current_anchor": anchor,
            "current_status": status,
            "claim_grade_requirement": requirement,
            "numeric_value": "MISSING_OR_PROXY_NONCLAIM" if status != "PROXY_UNIT_KERNEL_ONLY" else "8.948213306283e-11",
            "units": "dimensionless source/action coefficient unless declared otherwise",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for pack_id, component, meaning, anchor, status, requirement in rows
    ]


def claim_firewall_rows() -> list[dict[str, Any]]:
    rows = [
        ("FW1479_0_no_typing_to_claim", "do not treat a grammar contract as a parent derivation", "proof rows remain parent_signed=false", "ACTIVE"),
        ("FW1479_1_no_bound_inversion", "do not infer delta_w=0 from WEP/PPN/Gdot/R10 bounds", "bounds constrain products only after projection exists", "ACTIVE"),
        ("FW1479_2_no_unit_kernel_claim", "do not treat electron unit-kernel proxy as MTS bound", "EB1333 proxy lacks tau/source/readout normalization", "ACTIVE"),
        ("FW1479_3_no_common_G_cheat", "do not absorb relative weights into measured G", "only derivative-silent common mode is calibration", "ACTIVE"),
        ("FW1479_4_no_external_DD_as_MTS", "do not treat DD smoke coefficients as parent MTS coefficients", "requires explicit MTS-to-DD coefficient map", "ACTIVE"),
        ("FW1479_5_no_arena_retuning", "same component vector must feed all local arenas", "prevents bespoke WEP/R10/PPN couplings", "ACTIVE"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "firewall_id": firewall_id,
            "rule": rule,
            "enforcement": enforcement,
            "status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for firewall_id, rule, enforcement, status in rows
    ]


def gate_rows(
    theorem: list[dict[str, Any]],
    homs: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    anchors: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    pack: list[dict[str, Any]],
    firewall: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    conditional = any(row["theorem_id"] == "NST1479_1_conditional_typing" and row["status"] == "EXACT_CONDITIONAL_META_THEOREM" for row in theorem)
    refused = any(row["theorem_id"] == "NST1479_4_verdict" and row["status"] == "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED" for row in theorem)
    hom_blocked = any(row["current_status"] != "CALIBRATION_ONLY_IF_UNIVERSAL_SILENT" and not row["theorem_zero_allowed_now"] for row in homs)
    cms = all(row["retained"] for row in countermodels)
    anchors_nonclaim = all(not row["score_ready"] and not row["valid_for_claim"] for row in anchors)
    inputs_missing = all(not row["score_ready"] for row in inputs)
    pack_nonclaim = all(not row["score_ready"] and not row["valid_for_claim"] for row in pack)
    firewalls_active = all(row["status"] == "ACTIVE" for row in firewall)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1479_0_conditional_theorem",
            "gate": "no-source-only prefactor typing theorem is exact conditional",
            "gate_pass": conditional,
            "claim_effect": "contract exists; no claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1479_1_theorem_refused",
            "gate": "parent-signed theorem-zero promotion is refused",
            "gate_pass": refused,
            "claim_effect": "delta_w_A remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1479_2_hom_blocked",
            "gate": "Hom species/hidden/marker/readout to source prefactor remains blocked",
            "gate_pass": hom_blocked,
            "claim_effect": "must keep source-only coefficient pack",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1479_3_countermodels_retained",
            "gate": "all source-only prefactor countermodels retained",
            "gate_pass": cms,
            "claim_effect": "no GR/Newton source-universality pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1479_4_anchor_pack_nonclaim",
            "gate": "bound anchors are present but nonclaim",
            "gate_pass": anchors_nonclaim,
            "claim_effect": "data plumbing only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1479_5_inputs_missing",
            "gate": "source-ready input requirements remain missing",
            "gate_pass": inputs_missing and pack_nonclaim,
            "claim_effect": "component pack is acquisition-ready, not score-ready",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1479_6_firewalls",
            "gate": "anti-shortcut firewalls active",
            "gate_pass": firewalls_active,
            "claim_effect": "no bound inversion, no unit-kernel claim, no common-G cheat",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1479_0_theorem_status",
            "decision": "no-source-only action/source prefactor theorem is exact conditional, not parent-derived",
            "reason": "typing/no-Hom rule is a grammar contract until derived from MTS primitives",
            "consequence": "do not set delta_w_A to zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1479_1_bound_pack_status",
            "decision": "delta_w bound/acquisition pack is now consolidated but nonclaim",
            "reason": "anchors exist, but component vector, material tensor, projections, covariance, and same-branch convention are missing",
            "consequence": "future empirical work can fill rows without rewriting the theory gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1479_2_next_route",
            "decision": "attack no hidden/source coefficient Hom at the coefficient-domain level next",
            "reason": "this is the smallest route that could convert the typing theorem from contract to derivation",
            "consequence": "1480 should either prove coefficient-domain exclusion or produce first same-branch WEP delta_w smoke runner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1479_0_1480",
            "next_target": "1480-Y5-R10-RAB-coefficient-domain-Hom-exclusion-or-same-branch-WEP-delta-w-smoke-runner.md",
            "script": "scripts/Y5_R10_RAB_coefficient_domain_Hom_exclusion_or_same_branch_WEP_delta_w_smoke_runner.py",
            "objective": "try to prove the coefficient-domain exclusion Hom(C_hid/species, Coeff_source)=Const/absent; if it fails, build a same-branch WEP delta_w smoke runner using explicit component vector, material tensor, tau/readout, and no-cancellation placeholders",
            "include": "operator-domain typing; hidden invariant scalar obstruction; source-label Hom; WEP Ti/Pt material tensor; eta bound; unit-kernel/electron proxy quarantine",
            "exclude": "GitHub action; formalization-workbench edits; local-GR pass; WEP/R10/PPN claim promotion; bound inversion",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    homs: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    anchors: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    pack: list[dict[str, Any]],
    firewall: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_paths = [
        SOURCE_REGISTER,
        TYPING_THEOREM,
        HOM_AUDIT,
        COUNTERMODELS,
        BOUND_ANCHORS,
        BOUND_INPUTS,
        COMPONENT_BOUND_PACK,
        CLAIM_FIREWALL,
        REDUCTION_GATES,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    csv_parse_ok = True
    for path in generated_paths:
        try:
            parse_csv(path)
        except Exception:
            csv_parse_ok = False

    branch_copies = all(path.exists() for path in [QUAR_THEOREM, QUAR_PACK, BRANCH_THEOREM, BRANCH_PACK, BRANCH_GATES])
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = not any(
        file.stat().st_mtime >= START_TS
        for file in FORMALIZATION.rglob("*")
        if file.is_file()
    ) if FORMALIZATION.exists() else True

    conditional = any(row["theorem_id"] == "NST1479_1_conditional_typing" and row["status"] == "EXACT_CONDITIONAL_META_THEOREM" for row in theorem)
    proof_refused = any(row["theorem_id"] == "NST1479_4_verdict" and row["status"] == "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED" for row in theorem)
    homs_nonclaim = all(not row["theorem_zero_allowed_now"] and not row["valid_for_claim"] for row in homs)
    countermodels_retained = all(row["retained"] for row in countermodels)
    anchors_nonclaim = len(anchors) >= 9 and all(not row["score_ready"] and not row["claim_allowed"] for row in anchors)
    inputs_missing = all(not row["score_ready"] for row in inputs)
    pack_nonclaim = len(pack) >= 9 and all(not row["score_ready"] and not row["valid_for_claim"] for row in pack)
    firewalls_active = all(row["status"] == "ACTIVE" for row in firewall)
    claim_gates_false = all(not row["valid_for_claim"] and not row["claim_allowed"] for row in gates)

    checks = [
        ("VAL1479_0_sources", all(row["exists"] for row in sources), "all cited local source paths exist"),
        ("VAL1479_1_conditional_theorem", conditional, "no-source-only prefactor theorem is exact conditional"),
        ("VAL1479_2_promotion_refused", proof_refused, "parent-signed theorem-zero promotion refused"),
        ("VAL1479_3_hom_nonclaim", homs_nonclaim, "Hom audit rows remain nonclaim/theorem-zero false"),
        ("VAL1479_4_countermodels_retained", countermodels_retained, "source-only prefactor countermodels retained"),
        ("VAL1479_5_anchor_pack", anchors_nonclaim, "bound anchor pack includes WEP/clock/PPN/Gdot/R10/proxy rows as nonclaim"),
        ("VAL1479_6_inputs_missing", inputs_missing, "source-ready input requirements remain missing"),
        ("VAL1479_7_component_pack_nonclaim", pack_nonclaim, "component delta_w bound pack remains nonclaim"),
        ("VAL1479_8_firewalls_active", firewalls_active, "claim firewalls active"),
        ("VAL1479_9_claim_gates_false", claim_gates_false, "all reduction gates keep valid_for_claim/claim_allowed false"),
        ("VAL1479_10_generated_csv_parse", csv_parse_ok, "all generated 1479 CSVs parse cleanly"),
        ("VAL1479_11_branch_copies", branch_copies, "nonclaim branch/quarantine copies written"),
        ("VAL1479_12_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1479_13_formalization_untouched", formalization_untouched, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1479_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1479 refuses no-source-only prefactor theorem-zero and consolidates nonclaim delta_w bound pack",
            "generated_utc": now(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    homs: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    anchors: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    pack: list[dict[str, Any]],
    firewall: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines: list[str] = []
    lines.append("# 1479 — R10/RAB No-Source-Only Action Prefactor Typing Theorem Or Delta-w Bound Pack")
    lines.append("")
    lines.append("## Verdict")
    lines.append("- The no-source-only prefactor theorem is clean as a typing theorem: if `Hom(species_label, R_+ active-source-prefactor)` is absent, relative `delta_w_A` cannot enter the parent action.")
    lines.append("- It is not parent-derived yet: the current corpus still treats the no-Hom/object-language rule as a contract or closure condition, not as a theorem from deeper MTS primitives.")
    lines.append("- The fallback is now a consolidated nonclaim `delta_w` bound/acquisition pack with WEP, clock, PPN, Gdot, R10, electron-proxy, and DD-smoke anchors separated from claim-grade inputs.")
    lines.append("")
    lines.append("## Typing Theorem Attempt")
    lines.append("| theorem_id | status | current_gap |")
    lines.append("|---|---|---|")
    for row in theorem:
        lines.append(f"| {row['theorem_id']} | {row['status']} | {row['current_gap']} |")
    lines.append("")
    lines.append("## Hom Audit")
    lines.append("| hom_id | current_status | required_to_close |")
    lines.append("|---|---|---|")
    for row in homs:
        lines.append(f"| {row['hom_id']} | {row['current_status']} | {row['required_to_close']} |")
    lines.append("")
    lines.append("## Countermodels")
    lines.append("| countermodel_id | retained | countermodel |")
    lines.append("|---|---:|---|")
    for row in countermodels:
        lines.append(f"| {row['countermodel_id']} | {row['retained']} | {row['countermodel']} |")
    lines.append("")
    lines.append("## Bound Anchors")
    lines.append("| anchor_id | arena_or_channel | bound_value | why_nonclaim |")
    lines.append("|---|---|---|---|")
    for row in anchors:
        lines.append(f"| {row['anchor_id']} | {row['arena_or_channel']} | {row['bound_value']} | {row['why_nonclaim']} |")
    lines.append("")
    lines.append("## Bound Inputs")
    lines.append("| requirement_id | current_status | acceptance_rule |")
    lines.append("|---|---|---|")
    for row in inputs:
        lines.append(f"| {row['requirement_id']} | {row['current_status']} | {row['acceptance_rule']} |")
    lines.append("")
    lines.append("## Component Bound Pack")
    lines.append("| pack_id | component | current_status | score_ready |")
    lines.append("|---|---|---|---:|")
    for row in pack:
        lines.append(f"| {row['pack_id']} | {row['component']} | {row['current_status']} | {row['score_ready']} |")
    lines.append("")
    lines.append("## Claim Firewall")
    lines.append("| firewall_id | status | rule |")
    lines.append("|---|---|---|")
    for row in firewall:
        lines.append(f"| {row['firewall_id']} | {row['status']} | {row['rule']} |")
    lines.append("")
    lines.append("## Gates")
    lines.append("| gate_id | gate_pass | claim_effect |")
    lines.append("|---|---:|---|")
    for row in gates:
        lines.append(f"| {row['gate_id']} | {row['gate_pass']} | {row['claim_effect']} |")
    lines.append("")
    lines.append("## Decision Ledger")
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} — {row['consequence']}.")
    lines.append("")
    lines.append("## Validation")
    lines.append("| check_id | result | detail |")
    lines.append("|---|---|---|")
    for row in validation:
        lines.append(f"| {row['check_id']} | {row['result']} | {row['detail']} |")
    lines.append("")
    lines.append("## Source Register")
    lines.append("| source_id | exists | path_or_url | usage |")
    lines.append("|---|---:|---|---|")
    for row in sources:
        lines.append(f"| {row['source_id']} | {row['exists']} | `{row['path_or_url']}` | {row['usage']} |")
    lines.append("")
    lines.append("## Next Target")
    for row in next_target:
        lines.append(f"- `{row['next_target']}` via `{row['script']}`: {row['objective']}")
    lines.append("")
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    sources = source_rows()
    theorem = typing_theorem_rows()
    homs = hom_audit_rows()
    countermodels = countermodel_rows()
    anchors = bound_anchor_rows()
    inputs = bound_input_rows()
    pack = component_bound_pack_rows()
    firewall = claim_firewall_rows()
    gates = gate_rows(theorem, homs, countermodels, anchors, inputs, pack, firewall)
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(TYPING_THEOREM, theorem)
    write_csv(HOM_AUDIT, homs)
    write_csv(COUNTERMODELS, countermodels)
    write_csv(BOUND_ANCHORS, anchors)
    write_csv(BOUND_INPUTS, inputs)
    write_csv(COMPONENT_BOUND_PACK, pack)
    write_csv(CLAIM_FIREWALL, firewall)
    write_csv(REDUCTION_GATES, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_nonclaim(TYPING_THEOREM, QUAR_THEOREM)
    copy_nonclaim(COMPONENT_BOUND_PACK, QUAR_PACK)
    copy_nonclaim(TYPING_THEOREM, BRANCH_THEOREM)
    copy_nonclaim(COMPONENT_BOUND_PACK, BRANCH_PACK)
    copy_nonclaim(REDUCTION_GATES, BRANCH_GATES)

    validation = validation_rows(sources, theorem, homs, countermodels, anchors, inputs, pack, firewall, gates)
    write_csv(VALIDATION, validation)
    write_doc(sources, theorem, homs, countermodels, anchors, inputs, pack, firewall, gates, decisions, validation, next_target)
    print("Y5_R10_1479_no_source_prefactor_typing_conditional_delta_w_bound_pack_nonclaim")


if __name__ == "__main__":
    main()

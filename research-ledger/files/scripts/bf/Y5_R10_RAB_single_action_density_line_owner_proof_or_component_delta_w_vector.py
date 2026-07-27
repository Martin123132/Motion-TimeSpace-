from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1478"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1478-Y5-R10-RAB-single-action-density-line-owner-proof-or-component-delta-w-vector.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1477_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1477_VALIDATION.csv"
PREV_GRAPH_CERT = OUT / "P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_CERTIFICATE.csv"
PREV_ACTION_AUDIT = OUT / "P8_Y5_R10_1477_ACTION_DENSITY_LINE_OWNER_AUDIT.csv"
PREV_DSUM = OUT / "P8_Y5_R10_1477_DIRECT_SUM_OBSTRUCTION_LEDGER.csv"
PREV_SCHEMA = OUT / "P8_Y5_R10_1477_DELTA_W_TAU_WEP_SCHEMA_V2.csv"
PREV_TEMPLATE = OUT / "P8_Y5_R10_1477_DELTA_W_TAU_WEP_INPUT_TEMPLATE_NONCLAIM.csv"

OWNER_1224 = OUT / "P8_Y5_R10_1224_OWNER_PROOF_CLAUSES.csv"
OBSTRUCTION_1224 = OUT / "P8_Y5_R10_1224_SOURCE_WEIGHT_OBSTRUCTION_LEDGER.csv"
ACTION_SCALE_1067 = OUT / "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv"
HBAR_AUDIT_1067 = OUT / "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv"
SOURCE_SCALAR_1066 = OUT / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv"
FIELD_MEASURE_1066 = OUT / "P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv"
MATTER_FUNCTOR_1045 = OUT / "P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv"
CATEGORY_953 = OUT / "P8_Y5_R10_953_PARENT_CATEGORY_CONTRACT.csv"
MEASURE_CURRENT_1452 = OUT / "P8_Y5_R10_1452_COMMON_MEASURE_CURRENT_THEOREM_ATTEMPT.csv"
ACTION_MEASURE_1452 = OUT / "P8_Y5_R10_1452_ACTION_SCALE_MEASURE_AUDIT.csv"
EPSILON_UPDATE_1452 = OUT / "P8_Y5_R10_1452_EPSILON_JA_REQUIREMENT_UPDATE.csv"
MEASURE_OWNER_1463 = OUT / "P8_Y5_R10_1463_PARENT_MEASURE_OWNER_CONTRACT.csv"
JACOBIAN_1463 = OUT / "P8_Y5_R10_1463_SPECIES_JACOBIAN_EXCLUSION_CONTRACT.csv"
CONNECTED_1464 = OUT / "P8_Y5_R10_1464_CONNECTED_MATTER_CATEGORY_PROOF_ATTEMPT.csv"
LOCK_1418 = OUT / "P8_Y5_R10_1418_ACTION_SCALE_CURRENT_OWNER_LOCK_ATTEMPT.csv"
ARENA_1418 = OUT / "P8_Y5_R10_1418_QBAR_SOURCE_WEIGHT_ARENA_ACQUISITION_LEDGER.csv"
COMP_FORMULA_1232 = OUT / "P8_Y5_R10_1232_COMPONENT_FRACTION_FORMULA_LEDGER.csv"
COMP_SOURCE_PACK_1232 = OUT / "P8_Y5_R10_1232_TIPT_COMPONENT_FRACTION_SOURCE_PACK.csv"
SOURCE_COUPLING_1229 = OUT / "P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1478_SOURCE_REGISTER.csv"
PROOF_ATTEMPT = OUT / "P8_Y5_R10_1478_SINGLE_ACTION_DENSITY_LINE_PROOF_ATTEMPT.csv"
SYNTAX_CHECKLIST = OUT / "P8_Y5_R10_1478_PARENT_ACTION_SYNTAX_CHECKLIST.csv"
NO_GO = OUT / "P8_Y5_R10_1478_ACTION_LINE_NO_GO_THEOREM_LEDGER.csv"
COMPONENT_BASIS = OUT / "P8_Y5_R10_1478_COMPONENT_DELTA_W_BASIS_NONCLAIM.csv"
COMPONENT_VECTOR_TEMPLATE = OUT / "P8_Y5_R10_1478_COMPONENT_DELTA_W_VECTOR_INPUT_TEMPLATE_NONCLAIM.csv"
ARENA_MATRIX = OUT / "P8_Y5_R10_1478_COMPONENT_DELTA_W_ARENA_PROJECTION_MATRIX.csv"
EVALUATOR_RULES = OUT / "P8_Y5_R10_1478_COMPONENT_DELTA_W_EVALUATOR_RULES.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1478_REDUCTION_GATES.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1478_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1478_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1478_VALIDATION.csv"

QUAR_PROOF = QUARANTINE / "SINGLE_ACTION_DENSITY_LINE_PROOF_ATTEMPT_NONCLAIM.csv"
QUAR_VECTOR = QUARANTINE / "COMPONENT_DELTA_W_VECTOR_INPUT_TEMPLATE_NONCLAIM.csv"
BRANCH_PROOF = COEFF / "single_action_density_line_proof_attempt_nonclaim_1478.csv"
BRANCH_VECTOR = COEFF / "component_delta_w_vector_template_nonclaim_1478.csv"
BRANCH_GATES = COEFF / "single_action_density_line_reduction_gates_1478.csv"


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
        ("SRC1478_0_prev_next", PREV_NEXT, "1477 handoff selecting action-density line owner or component vector"),
        ("SRC1478_1_prev_validation", PREV_VALIDATION, "1477 validation baseline"),
        ("SRC1478_2_prev_graph", PREV_GRAPH_CERT, "connected matter graph template/nonclaim result"),
        ("SRC1478_3_prev_action_audit", PREV_ACTION_AUDIT, "single action-density owner audit"),
        ("SRC1478_4_prev_dsum", PREV_DSUM, "direct-sum obstruction ledger"),
        ("SRC1478_5_prev_schema", PREV_SCHEMA, "delta_w/tau schema v2"),
        ("SRC1478_6_prev_template", PREV_TEMPLATE, "nonclaim delta_w/tau input template"),
        ("SRC1478_7_owner_1224", OWNER_1224, "owner clauses for finite source-weight theorem"),
        ("SRC1478_8_obstruction_1224", OBSTRUCTION_1224, "source-weight obstruction ledger"),
        ("SRC1478_9_action_scale_1067", ACTION_SCALE_1067, "parent action-scale owner attempt"),
        ("SRC1478_10_hbar_audit_1067", HBAR_AUDIT_1067, "hbar/measure/current owner audit"),
        ("SRC1478_11_source_scalar_1066", SOURCE_SCALAR_1066, "source scalar exclusion lemma"),
        ("SRC1478_12_field_measure_1066", FIELD_MEASURE_1066, "field/measure/quantum normalization audit"),
        ("SRC1478_13_matter_functor_1045", MATTER_FUNCTOR_1045, "parent matter functor signature audit"),
        ("SRC1478_14_category_953", CATEGORY_953, "parent matter/source category contract"),
        ("SRC1478_15_measure_current_1452", MEASURE_CURRENT_1452, "common measure/current theorem attempt"),
        ("SRC1478_16_action_measure_1452", ACTION_MEASURE_1452, "action-scale measure audit"),
        ("SRC1478_17_epsilon_update_1452", EPSILON_UPDATE_1452, "epsilon/J_A requirement update"),
        ("SRC1478_18_measure_owner_1463", MEASURE_OWNER_1463, "parent measure owner contract"),
        ("SRC1478_19_jacobian_1463", JACOBIAN_1463, "species Jacobian exclusion contract"),
        ("SRC1478_20_connected_1464", CONNECTED_1464, "connected matter category proof attempt"),
        ("SRC1478_21_lock_1418", LOCK_1418, "action-scale/current owner lock attempt"),
        ("SRC1478_22_arena_1418", ARENA_1418, "qbar source-weight arena acquisition ledger"),
        ("SRC1478_23_comp_formula_1232", COMP_FORMULA_1232, "component fraction/delta_w formula ledger"),
        ("SRC1478_24_comp_pack_1232", COMP_SOURCE_PACK_1232, "Ti/Pt component fraction source pack"),
        ("SRC1478_25_source_coupling_1229", SOURCE_COUPLING_1229, "local-GR source coupling residual contract"),
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


def proof_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "SAL1478_0_target",
            "claim_piece": "single parent ordinary-matter action-density line",
            "formal_statement": "S_ord = integral dmu_parent L_ord(Psi_A, gauge, theta_A, e_obs) / hbar_parent, with one parent measure and no independent pre-variation w_A S_A slots",
            "proof_move": "try to type all ordinary matter sectors as sections over one L_action owner before source variation",
            "status": "TARGET_EXACT",
            "if_signed": "relative source/action weights become common calibration or inadmissible parent objects",
            "current_blocker": "L_action, hbar_parent, Dmu_parent, and ordinary matter object language are not parent-constructed as one syntax",
            "theorem_zero_promoted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "SAL1478_1_conditional_theorem",
            "claim_piece": "conditional action-line theorem",
            "formal_statement": "If S_ord has one parent action-density line, one hbar/measure owner, connected source-normalization morphisms, and no readout/non-Hilbert reentry, then delta_w_A=0 modulo common constant w_*",
            "proof_move": "combine PMO1463_0..6, CON1464_1, ACL1418_0..6, and THM1229_0..3",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "if_signed": "CI1474_1 source-weight residual can move to theorem-zero/common-mode route",
            "current_blocker": "premises remain closure clauses rather than derivations from parent MTS primitives",
            "theorem_zero_promoted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "SAL1478_2_classical_rescaling_rejection",
            "claim_piece": "classical EOM scaling does not prove source universality",
            "formal_statement": "delta(w_A S_A)/delta Psi_A=0 can match matter EOM while delta(w_A S_A)/delta g_obs = w_A T_A changes active source",
            "proof_move": "reuse ASO1067_1 and ACL1418_1 as a no-go guard",
            "status": "NO_GO_GUARD",
            "if_signed": "prevents false derivation by engineering-style equation scaling alone",
            "current_blocker": "none; this guard is retained",
            "theorem_zero_promoted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "SAL1478_3_direct_sum_countermodel",
            "claim_piece": "direct-sum independent component weights",
            "formal_statement": "If C_ord decomposes into disconnected source-normalization components, w_i can be independent constants while preserving additivity/naturality inside each component",
            "proof_move": "retain DSO1477_0, PMO1463_5, and OBS1224_2",
            "status": "COUNTERMODEL_SURVIVES",
            "if_signed": "would be killed only by parent-owned connected graph plus single line owner",
            "current_blocker": "parent-owned graph/action line not signed",
            "theorem_zero_promoted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "SAL1478_4_verdict",
            "claim_piece": "single action-density line owner proof status",
            "formal_statement": "Current corpus gives a clean conditional theorem but not a parent derivation of the one-line ordinary matter action owner",
            "proof_move": "refuse promotion and emit component delta_w vector fallback",
            "status": "PROOF_NOT_CLOSED_COMPONENT_VECTOR_REQUIRED",
            "if_signed": "future route can promote delta_w_A theorem-zero after all syntax/readout clauses close",
            "current_blocker": "single L_action syntax, hbar/measure owner, current owner, direct-sum policy, and readout transfer remain unsigned",
            "theorem_zero_promoted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def syntax_checklist_rows() -> list[dict[str, Any]]:
    clauses = [
        ("SYN1478_0_L_action", "one ordinary-matter action-density line L_action", "S_ord is not a direct sum of independently normalizable S_A blocks", "MISSING_PARENT_SYNTAX", MEASURE_OWNER_1463, "PMO1463_0_action_density_line"),
        ("SYN1478_1_hbar_parent", "one hbar/action phase normalization", "no effective hbar_A or w_A phase weighting", "NOT_PARENT_OWNED", HBAR_AUDIT_1067, "HMO1067_0_hbar_parent"),
        ("SYN1478_2_measure_parent", "species-blind path/statistical measure", "no J_A species-only measure Jacobian", "NOT_PARENT_OWNED", HBAR_AUDIT_1067, "HMO1067_1_measure_parent"),
        ("SYN1478_3_current_owner", "Hilbert/current/source normalization extracted from the same owner", "no c_A J_A or beta_source,A source-only current rescaling", "MISSING_CURRENT_OWNER", LOCK_1418, "ACL1418_3_current_owner"),
        ("SYN1478_4_connected_graph", "parent-owned ordinary-matter source-normalization graph is connected", "naturality collapses component weights to common w_*", "TEMPLATE_ONLY_NOT_PARENT_SIGNED", PREV_GRAPH_CERT, "GRC1477_1_parent_owned_connectivity"),
        ("SYN1478_5_direct_sum_no_prefactor", "direct sums do not create independent action prefactors", "direct-sum decomposition is bookkeeping only", "COUNTERMODEL_RETAINED", PREV_DSUM, "DSO1477_0_component_weights"),
        ("SYN1478_6_variation_before_readout", "source variation occurs before material/readout projection", "post-variation labels cannot recreate kappa_A", "CONDITIONAL_CLEAN_UNSIGNED", LOCK_1418, "ACL1418_4_variation_before_readout"),
        ("SYN1478_7_nonHilbert_silence", "non-Hilbert source currents absent/exact/projected silent", "no zeta_A J_NH,A bypass", "NOT_EXCLUDED", JACOBIAN_1463, "JEX1463_3_zetaA"),
        ("SYN1478_8_common_calibration_silence", "common w_* is derivative-silent and absorbed into measured G_N/GM", "common mode does not become time/range/source dependent", "NOT_SIGNED", MEASURE_OWNER_1463, "PMO1463_2_common_calibration"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "syntax_id": syntax_id,
            "required_clause": clause,
            "formal_effect": effect,
            "current_status": status,
            "source_artifact": rel(source),
            "source_anchor": anchor,
            "blocks_theorem_zero": status not in {"EXACT_CONDITIONAL_THEOREM", "NO_GO_GUARD"},
            "next_action": "derive from parent action syntax or keep component delta_w vector live",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for syntax_id, clause, effect, status, source, anchor in clauses
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "no_go_id": "NG1478_0_classical_EOM_scaling",
            "false_route": "treat w_A S_A as harmless because classical field equations can be rescaled",
            "why_invalid": "Hilbert stress/source variation and quantum/statistical phase still see w_A",
            "source_artifact": rel(ACTION_SCALE_1067),
            "source_anchor": "ASO1067_1_classical_EOM_vs_source;ASO1067_2_path_integral_measure",
            "retained": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "no_go_id": "NG1478_1_field_redefinition_only",
            "false_route": "remove w_A by field normalization independently in each sector",
            "why_invalid": "rescaling must preserve interactions, charge normalization, composites, Hilbert stress, and measure simultaneously",
            "source_artifact": rel(ACTION_MEASURE_1452),
            "source_anchor": "ASA1452_2_field_rescaling",
            "retained": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "no_go_id": "NG1478_2_common_G_absorption",
            "false_route": "hide relative component weights inside measured G_N or GM",
            "why_invalid": "only one derivative-silent common factor can be calibrated away; relative material/source/range/time dependence remains observable",
            "source_artifact": rel(MEASURE_OWNER_1463),
            "source_anchor": "PMO1463_2_common_calibration",
            "retained": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "no_go_id": "NG1478_3_template_graph_as_proof",
            "false_route": "use physical connectedness of ordinary matter as if it were a parent morphism certificate",
            "why_invalid": "1477 shows template connectivity but parent-owned component count remains disconnected",
            "source_artifact": rel(PREV_GRAPH_CERT),
            "source_anchor": "GRC1477_0_template_connectivity;GRC1477_1_parent_owned_connectivity",
            "retained": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def component_basis_rows() -> list[dict[str, Any]]:
    basis = [
        ("CWB1478_0_common_bulk", "delta_w_common", "common calibration mode", "bulk ordinary matter source normalization", "must be derivative-silent and absorbed into measured G_N/GM before harmless"),
        ("CWB1478_1_lepton_electron", "delta_w_e", "electron/lepton rest and leptonic binding contribution", "WEP, clocks, atomic matter", "requires electron fraction/energy fraction and readout convention"),
        ("CWB1478_2_EM_Coulomb", "delta_w_EM", "electromagnetic field/Coulomb binding contribution", "WEP, clocks, R10 charge-like source map", "requires EM/Coulomb energy fraction and alpha/readout convention"),
        ("CWB1478_3_light_quark", "delta_w_q", "light-quark mass/sigma-term contribution", "WEP, nuclear matter", "requires mass-decomposition basis with isotope/alloy averaging"),
        ("CWB1478_4_QCD_gluon", "delta_w_g", "QCD/gluon/bulk hadronic binding contribution", "WEP, Newton/GM, local_GR", "dominant common/bulk mode must not be double-counted with common calibration"),
        ("CWB1478_5_nuclear_binding", "delta_w_nuc", "nuclear surface/asymmetry/binding contribution", "WEP composition contrast", "requires nuclear binding model and isotope/alloy averaging"),
        ("CWB1478_6_measure_jacobian", "delta_J_A", "species-only measure/Jacobian residual", "all local source arenas", "requires measure-owner theorem or numeric bound"),
        ("CWB1478_7_current_rescaling", "delta_c_A", "post-variation current/source normalization residual", "WEP, PPN, local_GR", "requires current-owner/readout-order theorem or numeric projection"),
        ("CWB1478_8_nonHilbert_bypass", "zeta_A", "non-Hilbert source current bypass", "PPN/local_GR/source conservation", "requires J_NH absence/exactness/projection silence"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "basis_id": basis_id,
            "component_symbol": symbol,
            "component_name": name,
            "arena_relevance": relevance,
            "required_input_before_scoring": required,
            "current_value": "MISSING_THEOREM_ZERO_OR_NUMERIC_COMPONENT_VALUE",
            "units": "dimensionless source/action weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for basis_id, symbol, name, relevance, required in basis
    ]


def vector_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "vector_row_id": "CDW1478_0_parent_component_vector",
            "quantity": "delta_w_component_vector",
            "basis": "delta_w_common,delta_w_e,delta_w_EM,delta_w_q,delta_w_g,delta_w_nuc,delta_J_A,delta_c_A,zeta_A",
            "formula": "delta_w_A = component_fraction_A dot delta_w_component_vector + readout/measure/nonHilbert residuals",
            "accepted_evidence": "parent theorem-zero for every component OR numeric/source-backed component values with covariance/no-cancellation policy",
            "current_value": "MISSING_COMPONENT_VECTOR",
            "uncertainty": "MISSING_COMPONENT_COVARIANCE",
            "units": "dimensionless",
            "source_artifact": rel(COMP_FORMULA_1232),
            "source_anchor": "FORM1232_2_delta_w_prediction",
            "numeric_input_present": False,
            "theorem_zero_present": False,
            "passes_schema": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "vector_row_id": "CDW1478_1_TiPt_material_contrast",
            "quantity": "DeltaF_TiPt_component_vector",
            "basis": "electron,EM,light_quark,QCD,nuclear_binding,measure/readout residual",
            "formula": "Delta_w_TiPt = DeltaF_TiPt dot delta_w_component_vector + DeltaK_TiPt",
            "accepted_evidence": "official/material-source-backed component fraction tensor with isotope/alloy averaging",
            "current_value": "MISSING_CLAIM_GRADE_COMPONENT_FRACTIONS",
            "uncertainty": "MISSING_COMPONENT_FRACTION_UNCERTAINTY",
            "units": "dimensionless material fraction",
            "source_artifact": rel(COMP_SOURCE_PACK_1232),
            "source_anchor": "FSP1232_0 through FSP1232_7",
            "numeric_input_present": False,
            "theorem_zero_present": False,
            "passes_schema": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "vector_row_id": "CDW1478_2_no_cancellation_covariance",
            "quantity": "component covariance/no-cancellation envelope",
            "basis": "same as CDW1478_0",
            "formula": "score with norm or covariance; no cherry-picked cancellation unless parent covariance/source model supplies it",
            "accepted_evidence": "declared covariance matrix or conservative independent-bound envelope",
            "current_value": "MISSING_NO_CANCELLATION_ENVELOPE",
            "uncertainty": "MISSING_COVARIANCE",
            "units": "dimensionless covariance",
            "source_artifact": rel(PREV_SCHEMA),
            "source_anchor": "SC1477_13_no_cancellation_statement",
            "numeric_input_present": False,
            "theorem_zero_present": False,
            "passes_schema": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def arena_matrix_rows() -> list[dict[str, Any]]:
    arenas = [
        ("ARE1478_0_WEP", "WEP/MICROSCOPE Ti-Pt", "eta_TiPt = tau_WEP * (DeltaF_TiPt dot delta_w_vec + DeltaK_TiPt)", "DeltaF_TiPt; delta_w_vec; tau_WEP; sign convention; no-cancellation envelope; eta bound", ARENA_1418, "QAA1418_0_WEP_source_charge"),
        ("ARE1478_1_R10", "R10 inverse-square/fifth-force", "alpha(lambda)=K(lambda)*(source_vec dot delta_w_vec)*(test_vec dot delta_w_vec) or direct kernel", "alpha(lambda) bound curve; range convention; K(lambda); source/test component maps; no tau=1 shortcut", ARENA_1418, "QAA1418_2_R10_fifth_force"),
        ("ARE1478_2_PPN", "PPN gamma/beta/preferred frame", "PPN_residual = P_PPN[delta_w_vec, current_rescaling, q_source]", "weak-field response operator; source-current owner or finite residual coefficients; units/signs", ARENA_1418, "QAA1418_3_PPN_gamma_beta"),
        ("ARE1478_3_clock", "clock/readout cross-check", "clock_residual = P_clock[delta_w_vec, hbar*c/readout constants]", "readout transfer; hbar/alpha/mass clock sensitivity; no using clock pass as WEP pass", ARENA_1418, "QAA1418_5_clock_readout_guard"),
        ("ARE1478_4_orbital", "Newton/GM/orbital", "GM_residual = common_mode + source_profile dot delta_w_vec + time/range drift", "worldtube/source profile; measured-GM calibration split; time/range dependence", ARENA_1418, "QAA1418_1_Newton_GM_orbital"),
        ("ARE1478_5_local_GR", "local GR/Newton source side", "q_source^nu = P_loc nabla_mu[sum_c delta_w_c T_c^{mu nu}] plus boundary/projector/readout terms", "EH reduction; Bianchi/conservation check; source-current theorem or residual vector norm", SOURCE_COUPLING_1229, "THM1229_3_residual_vector"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "arena_id": arena_id,
            "arena": arena,
            "projection_formula": formula,
            "required_inputs": inputs,
            "source_artifact": rel(source),
            "source_anchor": anchor,
            "current_status": "NOT_SCOREABLE_MISSING_COMPONENT_VECTOR_OR_PROJECTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for arena_id, arena, formula, inputs, source, anchor in arenas
    ]


def evaluator_rule_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rule_id": "EV1478_0_theorem_zero",
            "rule": "accept delta_w theorem-zero only if every syntax clause in SYN1478 passes parent-signed and every no-go countermodel is killed",
            "current_status": "FAIL_UNSIGNED_SYNTAX",
            "effect": "CI1474_1 remains failing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "rule_id": "EV1478_1_component_vector_numeric",
            "rule": "accept numeric scoring only if delta_w_vec, component fractions, arena projection, units, sign convention, covariance/no-cancellation, and source paths are present",
            "current_status": "FAIL_MISSING_COMPONENT_INPUTS",
            "effect": "component rows are templates only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "rule_id": "EV1478_2_common_mode_guard",
            "rule": "one common derivative-silent mode may calibrate G_N/GM; relative component modes cannot be hidden in common calibration",
            "current_status": "PASS_GUARD_ACTIVE",
            "effect": "prevents measured-G absorption cheat",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "rule_id": "EV1478_3_cross_arena_basis_lock",
            "rule": "the same component vector basis must feed WEP, R10, PPN, clock, orbital, and local_GR rows",
            "current_status": "PASS_SCHEMA_GUARD",
            "effect": "prevents one-off coupling choices per test",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def reduction_gate_rows(
    proofs: list[dict[str, Any]],
    syntax: list[dict[str, Any]],
    no_go: list[dict[str, Any]],
    vector: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    conditional_theorem = any(row["proof_id"] == "SAL1478_1_conditional_theorem" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in proofs)
    proof_refused = any(row["proof_id"] == "SAL1478_4_verdict" and row["status"] == "PROOF_NOT_CLOSED_COMPONENT_VECTOR_REQUIRED" for row in proofs)
    syntax_blocked = any(bool(row["blocks_theorem_zero"]) for row in syntax)
    no_go_retained = all(bool(row["retained"]) for row in no_go)
    vector_failing = all(not bool(row["passes_schema"]) for row in vector)
    arenas_blocked = all(row["current_status"] == "NOT_SCOREABLE_MISSING_COMPONENT_VECTOR_OR_PROJECTION" for row in arenas)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1478_0_conditional_theorem",
            "gate": "single action-density line theorem is mathematically exact conditional",
            "gate_pass": conditional_theorem,
            "claim_effect": "useful proof contract, not a claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1478_1_syntax_blocked",
            "gate": "parent syntax clauses still block theorem-zero",
            "gate_pass": syntax_blocked,
            "claim_effect": "must keep delta_w vector live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1478_2_no_go_retained",
            "gate": "false proof routes are retained as guards",
            "gate_pass": no_go_retained,
            "claim_effect": "prevents EOM/G/field-redefinition shortcuts",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1478_3_component_vector_failing",
            "gate": "component delta_w vector exists but is not numeric/theorem-zero",
            "gate_pass": vector_failing,
            "claim_effect": "fallback is acquisition-ready, not score-ready",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1478_4_arenas_blocked",
            "gate": "all local arenas remain blocked without component vector/projections",
            "gate_pass": arenas_blocked,
            "claim_effect": "no WEP/R10/PPN/clock/orbital/local-GR claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "GATE1478_5_claim_refusal",
            "gate": "source-weight/Newton/local-GR promotion refused",
            "gate_pass": proof_refused and syntax_blocked and vector_failing,
            "claim_effect": "CI1474_1 remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1478_0_theorem_status",
            "decision": "single action-density line route is exact conditional but not parent-derived",
            "reason": "the current corpus lacks parent syntax for L_action, hbar/measure owner, current owner, direct-sum policy, and transfer to readout",
            "consequence": "delta_w_A cannot be set to zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1478_1_fallback",
            "decision": "emit component delta_w vector as the honest fallback",
            "reason": "the direct-sum/source-weight countermodel survives",
            "consequence": "future tests must score the same component vector across WEP/R10/PPN/clock/orbital/local_GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1478_2_best_next_step",
            "decision": "attack the parent object-language line owner next",
            "reason": "without a typed no-source-only-prefactor theorem, component weights remain legal",
            "consequence": "1479 should either prove no Hom(species label, action prefactor) or harden source-only coefficient bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1478_0_1479",
            "next_target": "1479-Y5-R10-RAB-no-source-only-action-prefactor-typing-theorem-or-delta-w-bound-pack.md",
            "script": "scripts/Y5_R10_RAB_no_source_only_action_prefactor_typing_theorem_or_delta_w_bound_pack.py",
            "objective": "try to prove the typed parent object-language theorem forbidding Hom(species label, positive action/source prefactor); if it fails, build the first source-ready delta_w bound/acquisition pack for component weights",
            "include": "object-language typing; no inert source-only scalar; Hom(species,R_+) exclusion; component vector source paths; WEP/R10/PPN/orbital/local_GR projection requirements",
            "exclude": "GitHub action; formalization-workbench edits; local-GR pass; WEP/R10/clock claim promotion; bound inversion",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    proofs: list[dict[str, Any]],
    syntax: list[dict[str, Any]],
    no_go: list[dict[str, Any]],
    basis: list[dict[str, Any]],
    vector: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
    rules: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_paths = [
        SOURCE_REGISTER,
        PROOF_ATTEMPT,
        SYNTAX_CHECKLIST,
        NO_GO,
        COMPONENT_BASIS,
        COMPONENT_VECTOR_TEMPLATE,
        ARENA_MATRIX,
        EVALUATOR_RULES,
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

    branch_copies = all(path.exists() for path in [QUAR_PROOF, QUAR_VECTOR, BRANCH_PROOF, BRANCH_VECTOR, BRANCH_GATES])
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = not any(
        file.stat().st_mtime >= START_TS
        for file in FORMALIZATION.rglob("*")
        if file.is_file()
    ) if FORMALIZATION.exists() else True

    conditional = any(row["proof_id"] == "SAL1478_1_conditional_theorem" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in proofs)
    refused = any(row["proof_id"] == "SAL1478_4_verdict" and row["status"] == "PROOF_NOT_CLOSED_COMPONENT_VECTOR_REQUIRED" for row in proofs)
    syntax_blocked = any(row["blocks_theorem_zero"] for row in syntax)
    no_go_retained = all(row["retained"] for row in no_go)
    basis_nonclaim = len(basis) >= 8 and all(not row["valid_for_claim"] and not row["claim_allowed"] for row in basis)
    vector_fails = all(not row["passes_schema"] and not row["numeric_input_present"] and not row["theorem_zero_present"] for row in vector)
    arenas_blocked = all(row["current_status"] == "NOT_SCOREABLE_MISSING_COMPONENT_VECTOR_OR_PROJECTION" for row in arenas)
    guards_active = any(row["rule_id"] == "EV1478_2_common_mode_guard" and row["current_status"] == "PASS_GUARD_ACTIVE" for row in rules)
    claim_gate_refuses = any(row["gate_id"] == "GATE1478_5_claim_refusal" and row["gate_pass"] for row in gates)

    checks = [
        ("VAL1478_0_sources", all(row["exists"] for row in sources), "all cited local source paths exist"),
        ("VAL1478_1_conditional_theorem", conditional, "single action-density theorem written as exact conditional"),
        ("VAL1478_2_promotion_refused", refused, "theorem-zero promotion refused"),
        ("VAL1478_3_syntax_blocks", syntax_blocked, "parent syntax checklist blocks claim"),
        ("VAL1478_4_no_go_retained", no_go_retained, "false proof routes retained"),
        ("VAL1478_5_basis_nonclaim", basis_nonclaim, "component delta_w basis written as nonclaim"),
        ("VAL1478_6_vector_fails", vector_fails, "component vector template remains missing numeric/theorem-zero inputs"),
        ("VAL1478_7_arenas_blocked", arenas_blocked, "WEP/R10/PPN/clock/orbital/local_GR projections remain blocked"),
        ("VAL1478_8_common_mode_guard", guards_active, "common-G absorption guard active"),
        ("VAL1478_9_claim_gate_refuses", claim_gate_refuses, "claim refusal gate passes"),
        ("VAL1478_10_generated_csv_parse", csv_parse_ok, "all generated 1478 CSVs parse cleanly"),
        ("VAL1478_11_branch_copies", branch_copies, "nonclaim branch/quarantine copies written"),
        ("VAL1478_12_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1478_13_formalization_untouched", formalization_untouched, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1478_14_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1478 keeps one-line action owner conditional and emits component delta_w vector fallback",
            "generated_utc": now(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    proofs: list[dict[str, Any]],
    syntax: list[dict[str, Any]],
    no_go: list[dict[str, Any]],
    basis: list[dict[str, Any]],
    vector: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
    rules: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines: list[str] = []
    lines.append("# 1478 — R10/RAB Single Action-Density Line Owner Proof Or Component Delta-w Vector")
    lines.append("")
    lines.append("## Verdict")
    lines.append("- The clean theorem exists: one parent ordinary-matter action-density line plus one measure/current/readout owner would kill relative source weights modulo a common calibration.")
    lines.append("- The parent derivation is still missing: current files do not construct `L_action`, `hbar_parent`, `Dmu_parent`, current ownership, direct-sum policy, and readout transfer as one signed syntax.")
    lines.append("- So `delta_w_A = 0` is not promoted; the fallback is now an explicit component `delta_w` vector that must feed WEP, R10, PPN, clock, orbital, and local-GR projections consistently.")
    lines.append("")
    lines.append("## Proof Attempt")
    lines.append("| proof_id | status | current_blocker |")
    lines.append("|---|---|---|")
    for row in proofs:
        lines.append(f"| {row['proof_id']} | {row['status']} | {row['current_blocker']} |")
    lines.append("")
    lines.append("## Parent Syntax Checklist")
    lines.append("| syntax_id | current_status | blocks_theorem_zero | source_anchor |")
    lines.append("|---|---|---:|---|")
    for row in syntax:
        lines.append(f"| {row['syntax_id']} | {row['current_status']} | {row['blocks_theorem_zero']} | {row['source_anchor']} |")
    lines.append("")
    lines.append("## No-Go Guards")
    lines.append("| no_go_id | retained | false_route |")
    lines.append("|---|---:|---|")
    for row in no_go:
        lines.append(f"| {row['no_go_id']} | {row['retained']} | {row['false_route']} |")
    lines.append("")
    lines.append("## Component Delta-w Basis")
    lines.append("| basis_id | component_symbol | current_value | required_input_before_scoring |")
    lines.append("|---|---|---|---|")
    for row in basis:
        lines.append(f"| {row['basis_id']} | {row['component_symbol']} | {row['current_value']} | {row['required_input_before_scoring']} |")
    lines.append("")
    lines.append("## Component Vector Template")
    lines.append("| vector_row_id | quantity | current_value | passes_schema |")
    lines.append("|---|---|---|---:|")
    for row in vector:
        lines.append(f"| {row['vector_row_id']} | {row['quantity']} | {row['current_value']} | {row['passes_schema']} |")
    lines.append("")
    lines.append("## Arena Projection Matrix")
    lines.append("| arena_id | arena | current_status |")
    lines.append("|---|---|---|")
    for row in arenas:
        lines.append(f"| {row['arena_id']} | {row['arena']} | {row['current_status']} |")
    lines.append("")
    lines.append("## Evaluator Rules")
    lines.append("| rule_id | current_status | effect |")
    lines.append("|---|---|---|")
    for row in rules:
        lines.append(f"| {row['rule_id']} | {row['current_status']} | {row['effect']} |")
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
    proofs = proof_attempt_rows()
    syntax = syntax_checklist_rows()
    no_go = no_go_rows()
    basis = component_basis_rows()
    vector = vector_template_rows()
    arenas = arena_matrix_rows()
    rules = evaluator_rule_rows()
    gates = reduction_gate_rows(proofs, syntax, no_go, vector, arenas)
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PROOF_ATTEMPT, proofs)
    write_csv(SYNTAX_CHECKLIST, syntax)
    write_csv(NO_GO, no_go)
    write_csv(COMPONENT_BASIS, basis)
    write_csv(COMPONENT_VECTOR_TEMPLATE, vector)
    write_csv(ARENA_MATRIX, arenas)
    write_csv(EVALUATOR_RULES, rules)
    write_csv(REDUCTION_GATES, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_nonclaim(PROOF_ATTEMPT, QUAR_PROOF)
    copy_nonclaim(COMPONENT_VECTOR_TEMPLATE, QUAR_VECTOR)
    copy_nonclaim(PROOF_ATTEMPT, BRANCH_PROOF)
    copy_nonclaim(COMPONENT_VECTOR_TEMPLATE, BRANCH_VECTOR)
    copy_nonclaim(REDUCTION_GATES, BRANCH_GATES)

    validation = validation_rows(sources, proofs, syntax, no_go, basis, vector, arenas, rules, gates)
    write_csv(VALIDATION, validation)
    write_doc(sources, proofs, syntax, no_go, basis, vector, arenas, rules, gates, decisions, validation, next_target)
    print("Y5_R10_1478_single_action_line_conditional_component_delta_w_vector_nonclaim")


if __name__ == "__main__":
    main()

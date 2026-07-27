from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1485-Y5-R10-RAB-C-parent-WEP-functional-derivative-or-universal-matter-double-zero-proof.md"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1484_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1484_VALIDATION.csv"
PREV_INTERFACE = OUT / "P8_Y5_R10_1484_BRANCH_LOCKED_WEP_PRODUCT_INTERFACE.csv"
PREV_C_PARENT = OUT / "P8_Y5_R10_1484_C_PARENT_COUPLING_DERIVATION_ATTEMPT.csv"
PREV_CLAUSES = OUT / "P8_Y5_R10_1484_C_PARENT_CLAUSE_GATES.csv"
PREV_LOCAL = OUT / "P8_Y5_R10_1484_LOCAL_GR_NEWTON_LINK_LEDGER.csv"
PREV_REFUSALS = OUT / "P8_Y5_R10_1484_INTERFACE_REFUSAL_TESTS.csv"
PREV_REJECTIONS = OUT / "P8_Y5_R10_1484_REJECTION_LEDGER.csv"

MCD_716 = OUT / "P8_Y5_R10_716_MATTER_COUPLING_DERIVATION.csv"
THM_1229 = OUT / "P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv"
MOMS_1088 = OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv"
MOMS_ZERO_1088 = OUT / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv"
SYN_1090 = OUT / "P8_Y5_R10_1090_SYNTHESIS_ATTEMPT.csv"
AX_1090 = OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv"
HT_1450 = OUT / "P8_Y5_R10_1450_HILBERT_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv"
NSSR_1450 = OUT / "P8_Y5_R10_1450_NO_SOURCE_ONLY_SLOT_REDUCTION_AUDIT.csv"
CON_1464 = OUT / "P8_Y5_R10_1464_CONNECTED_MATTER_CATEGORY_PROOF_ATTEMPT.csv"
CAL_1464 = OUT / "P8_Y5_R10_1464_COMMON_CALIBRATION_SILENCE_CONTRACT.csv"
GRC_1477 = OUT / "P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_CERTIFICATE.csv"
SAL_1478 = OUT / "P8_Y5_R10_1478_SINGLE_ACTION_DENSITY_LINE_PROOF_ATTEMPT.csv"
PREF_1479 = OUT / "P8_Y5_R10_1479_NO_SOURCE_ONLY_ACTION_PREFACTOR_TYPING_THEOREM_ATTEMPT.csv"
HOM_1479 = OUT / "P8_Y5_R10_1479_HOM_SPECIES_TO_SOURCE_PREFACTOR_AUDIT.csv"

C_PARENT_SCHEMA = BRANCH_COEFF / "C_parent_import_schema.csv"
C_PARENT_CONTRACT = BRANCH_COEFF / "C_parent_WEP_coupling_theorem_contract.csv"
C_PARENT_AUDIT = BRANCH_COEFF / "C_parent_WEP_contract_clause_reduction_audit.csv"
C_PARENT_ZERO = BRANCH_COEFF / "C_parent_WEP_slot_zero_attempt.csv"
C_PARENT_CANDIDATES = BRANCH_COEFF / "C_parent_WEP_parent_action_coupling_candidate_ledger.csv"
DOUBLE_ZERO_1473 = BRANCH_COEFF / "parent_coupling_double_zero_theorem_attempt_nonclaim_1473.csv"
CI_MAP_1474 = BRANCH_COEFF / "complete_Ci_parent_action_map_nonclaim_1474.csv"
C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1485_SOURCE_REGISTER.csv"
V_GENERATOR = OUT / "P8_Y5_R10_1485_V_WEP_GENERATOR_CONTRACT.csv"
FUNCTIONAL_DERIVATIVE = OUT / "P8_Y5_R10_1485_FUNCTIONAL_DERIVATIVE_DEFINITION.csv"
DOUBLE_ZERO_ATTEMPT = OUT / "P8_Y5_R10_1485_UNIVERSAL_MATTER_DOUBLE_ZERO_THEOREM_ATTEMPT.csv"
SIGNATURE_GATES = OUT / "P8_Y5_R10_1485_PARENT_SIGNATURE_CLAUSE_GATES.csv"
PREFATOR_GATES = OUT / "P8_Y5_R10_1485_NO_SOURCE_ONLY_PREFACTOR_GATES.csv"
IMPORT_REFUSAL = OUT / "P8_Y5_R10_1485_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_REDUCTION = OUT / "P8_Y5_R10_1485_LOCAL_GR_NEWTON_REDUCTION_VERDICT.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1485_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1485_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1485_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1485_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1485"
QUAR_DZERO = QUARANTINE / "UNIVERSAL_MATTER_DOUBLE_ZERO_ATTEMPT_NONCLAIM.csv"
QUAR_FDERIV = QUARANTINE / "FUNCTIONAL_DERIVATIVE_DEFINITION_NONCLAIM.csv"
QUAR_IMPORT = QUARANTINE / "C_PARENT_IMPORT_REFUSAL_NONCLAIM.csv"
BRANCH_DZERO = BRANCH_COEFF / "universal_matter_double_zero_attempt_nonclaim_1485.csv"
BRANCH_FDERIV = BRANCH_COEFF / "C_parent_WEP_functional_derivative_definition_nonclaim_1485.csv"
BRANCH_IMPORT_REFUSAL = BRANCH_COEFF / "C_parent_WEP_import_refusal_nonclaim_1485.csv"


def utc_now() -> str:
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
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC1485_0_prev_next", PREV_NEXT, "1484 handoff"),
        ("SRC1485_1_prev_validation", PREV_VALIDATION, "1484 validation"),
        ("SRC1485_2_prev_interface", PREV_INTERFACE, "branch-locked WEP product interface"),
        ("SRC1485_3_prev_C_parent", PREV_C_PARENT, "1484 C_parent derivation attempt"),
        ("SRC1485_4_prev_clauses", PREV_CLAUSES, "1484 C_parent clause gates"),
        ("SRC1485_5_prev_local", PREV_LOCAL, "local GR/Newton link ledger"),
        ("SRC1485_6_prev_refusals", PREV_REFUSALS, "shortcut refusals"),
        ("SRC1485_7_prev_rejections", PREV_REJECTIONS, "1484 rejection ledger"),
        ("SRC1485_8_MCD716", MCD_716, "matter coupling derivation and zero condition"),
        ("SRC1485_9_THM1229", THM_1229, "local-GR source coupling theorem contract"),
        ("SRC1485_10_MOMS1088", MOMS_1088, "minimal ordinary-matter signature clauses"),
        ("SRC1485_11_ZERO1088", MOMS_ZERO_1088, "conditional MOMS zero theorem"),
        ("SRC1485_12_SYN1090", SYN_1090, "MOMS parent-action synthesis attempt"),
        ("SRC1485_13_AX1090", AX_1090, "missing MOMS axiom ledger"),
        ("SRC1485_14_HT1450", HT_1450, "Hilbert source label-forgetting theorem"),
        ("SRC1485_15_NSSR1450", NSSR_1450, "no source-only slot audit"),
        ("SRC1485_16_CON1464", CON_1464, "connected matter category proof"),
        ("SRC1485_17_CAL1464", CAL_1464, "common calibration silence contract"),
        ("SRC1485_18_GRC1477", GRC_1477, "connected matter graph certificate"),
        ("SRC1485_19_SAL1478", SAL_1478, "single action-density line proof"),
        ("SRC1485_20_PREF1479", PREF_1479, "no-source-only action prefactor theorem attempt"),
        ("SRC1485_21_HOM1479", HOM_1479, "Hom species/source prefactor audit"),
        ("SRC1485_22_C_parent_schema", C_PARENT_SCHEMA, "C_parent import schema"),
        ("SRC1485_23_C_parent_contract", C_PARENT_CONTRACT, "C_parent coupling theorem contract"),
        ("SRC1485_24_C_parent_audit", C_PARENT_AUDIT, "C_parent clause reduction audit"),
        ("SRC1485_25_C_parent_zero", C_PARENT_ZERO, "C_parent zero attempt"),
        ("SRC1485_26_C_parent_candidates", C_PARENT_CANDIDATES, "parent action coupling candidates"),
        ("SRC1485_27_double_zero1473", DOUBLE_ZERO_1473, "parent coupling double-zero theorem attempt"),
        ("SRC1485_28_Ci_map1474", CI_MAP_1474, "complete local coefficient map"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": source_id,
            "path_or_url": rel(path),
            "source_kind": "local_file",
            "exists_or_resolved": path.exists(),
            "usage": usage,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, usage in sources
    ]


def v_generator_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "VGEN1485_0_target",
            "V_WEP,X",
            "parent-basis WEP generator for Ti/Pt material contrast and source/readout projection",
            "V_WEP,X must be defined before empirical eta fitting and before readout/source projection",
            "DEFINED_SYMBOLICALLY_NOT_PARENT_OWNED",
            "parent object language and material/source basis owner",
        ),
        (
            "VGEN1485_1_verticality",
            "V_WEP,X in ker(Dq)",
            "generator must be quotient-vertical so q(Phi_s)=q(Phi) along the tested fibre",
            "Dq[V_WEP,X]=0 over a neighbourhood, not merely at one point",
            "UNSIGNED_NEIGHBOURHOOD_VERTICALITY",
            "parent quotient map q and fibre-invariance certificate",
        ),
        (
            "VGEN1485_2_matter_lift",
            "delta_V Psi_A",
            "ordinary matter lift is fixed, gauge, diffeo, local-Lorentz, or boundary-only",
            "bulk Hilbert/current variation cannot receive species/source term",
            "MISSING_PARENT_MATTER_BUNDLE_FUNCTOR",
            "species-complete parent matter bundle functor",
        ),
        (
            "VGEN1485_3_no_readout_reentry",
            "readout/source projection after variation",
            "readout and source-worldtube selectors must not reintroduce a source-only label after Hilbert variation",
            "variation-before-readout over same action",
            "READOUT_TRANSFER_UNSIGNED",
            "official readout/source rows plus parent variation-order theorem",
        ),
        (
            "VGEN1485_4_verdict",
            "V_WEP,X generator",
            "the generator is now typed well enough for a theorem target but not parent-owned",
            "cannot evaluate or zero C_parent from it yet",
            "GENERATOR_CONTRACT_ONLY",
            "prove neighbourhood fibre invariance and matter-bundle ownership",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "generator_id": generator_id,
            "symbol": symbol,
            "definition": definition,
            "required_condition": condition,
            "current_status": status,
            "missing_for_claim": missing,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for generator_id, symbol, definition, condition, status, missing in rows
    ]


def functional_derivative_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FD1485_0_definition",
            "C_parent_X := N_X^{-1} d/ds S_ord[Phi_s, Psi_s, theta] |_{s=0}",
            "Phi_s generated by V_WEP,X; N_X is the declared material/source/readout normalization",
            "DEFINITION_EXACT_CONDITIONAL",
            "needs V_WEP,X, N_X, and S_ord parent-owned",
        ),
        (
            "FD1485_1_parent_action_slot",
            "S_ord must be a subfunctional of one S_parent before projection/readout",
            "variation is taken on the parent ordinary-matter action, not on an empirical eta model",
            "CONTRACT_STATED_NOT_SOURCE_SIGNED",
            "single parent action object and ordinary matter domain",
        ),
        (
            "FD1485_2_units_sign_basis",
            "C_parent_X units/sign/basis must be inherited from N_X and V_WEP,X",
            "import row must declare basis_id, component_id, units, sign_convention, source path, and parent_status",
            "SCHEMA_KNOWN_VALUE_MISSING",
            "live C_parent_WEP_slot_import.csv absent",
        ),
        (
            "FD1485_3_zero_option",
            "DERIVED_ZERO is valid only if C_parent_X vanishes as a parent theorem",
            "closure preference, stationarity, or MICROSCOPE bound cannot define zero",
            "ZERO_OPTION_NOT_CERTIFIED",
            "neighbourhood quotient descent or universal-matter double-zero proof",
        ),
        (
            "FD1485_4_finite_option",
            "finite C_parent_X is valid only if source-backed independent of MICROSCOPE",
            "empirical bound can test but not choose C_parent",
            "FINITE_OPTION_MISSING_SOURCE",
            "source-backed finite coefficient row",
        ),
        (
            "FD1485_5_verdict",
            "functional derivative route",
            "definition is exact as a contract, but not evaluable from current parent action files",
            "NOT_EVALUABLE",
            "derive parent action slot and generator ownership",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "definition_id": definition_id,
            "formal_definition": formal_definition,
            "meaning": meaning,
            "current_status": status,
            "missing_for_import": missing,
            "import_allowed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for definition_id, formal_definition, meaning, status, missing in rows
    ]


def double_zero_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DZ1485_0_exact_neighbourhood_theorem",
            "If S_ord = Sbar_ord[q(Phi), Psi[q(Phi)], theta] on an open neighbourhood U and V_X is vertical on every fibre in U, then C_parent_X(Phi)=0 throughout U.",
            "Differentiate Sbar_ord(q(Phi_s)) with q(Phi_s)=q(Phi); the derivative is identically zero on U.",
            "EXACT_CONDITIONAL_THEOREM",
            "prove neighbourhood quotient descent, not just pointwise fixed-point stationarity",
        ),
        (
            "DZ1485_1_double_zero_corollary",
            "If C_parent_X(Phi)=0 throughout U, then C_parent_X(Phi0)=0 and partial_A C_parent_X(Phi0)=0 for all local perturbation coordinates A.",
            "An identically zero function on U has zero value and zero first derivative at Phi0.",
            "EXACT_CONDITIONAL_COROLLARY",
            "same neighbourhood theorem plus smooth local coordinate chart",
        ),
        (
            "DZ1485_2_universal_matter_branch",
            "Universal observed coframe, one action-density line, fixed constants, no w_A, and no shadow/readout reentry are sufficient premises for the neighbourhood theorem.",
            "These clauses remove every source-only target hit by V_WEP,X.",
            "SUFFICIENT_CONDITIONS_IDENTIFIED",
            "parent-sign MOMS1088 clauses 0-6 / AX1090 0-4",
        ),
        (
            "DZ1485_3_fixed_point_no_go",
            "A compact local fixed point alone does not imply double zero.",
            "C(Phi)=c0+c1(Phi-Phi0)+... may have nonzero c0 or c1 even if Phi0 extremizes another functional.",
            "NO_GO_GUARD_RETAINED",
            "tie C_parent to same descended parent action or keep residual",
        ),
        (
            "DZ1485_4_current_corpus_check",
            "Current ledgers contain the exact conditional math but not the parent-signed action signature.",
            "1088/1090/1450/1464/1477/1478/1479 all leave parent ownership unsigned or countermodels alive.",
            "NOT_PARENT_DERIVED",
            "no C_parent zero import allowed",
        ),
        (
            "DZ1485_5_verdict",
            "Universal-matter double-zero proof status",
            "We have the clean theorem: exact neighbourhood quotient descent implies double zero. The corpus has not proven that descent.",
            "PROOF_SHARPENED_NOT_CLOSED",
            "next target must prove/source neighbourhood descent and the ordinary-matter action signature",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": theorem_id,
            "formal_statement": statement,
            "proof_move": proof_move,
            "current_status": status,
            "missing_for_parent_claim": missing,
            "parent_signed": False,
            "theorem_zero_import_allowed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for theorem_id, statement, proof_move, status, missing in rows
    ]


def signature_gate_rows() -> list[dict[str, Any]]:
    moms_rows = read_csv(MOMS_1088)
    rows: list[dict[str, Any]] = []
    for row in moms_rows:
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "gate_id": f"SIG1485_{row['clause_id']}",
                "clause": row["minimal_signature_clause"],
                "current_status": row["current_status"],
                "missing_for_adoption": row["missing_for_adoption"],
                "needed_for": "universal matter double-zero theorem",
                "gate_pass": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def prefactor_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PREFG1485_0_wA",
            "w_A source/action prefactor",
            "must be absent from parent object language or quotient-equivalent to common derivative-silent w_*",
            "NOT_PARENT_SIGNED",
            "relative WEP/source coupling remains live",
        ),
        (
            "PREFG1485_1_connected_graph",
            "ordinary matter connected graph",
            "parent-owned nonzero morphism graph must collapse weights by naturality",
            "TEMPLATE_ONLY_NOT_PARENT_OWNED",
            "direct-sum countermodel survives",
        ),
        (
            "PREFG1485_2_single_line",
            "one action-density line",
            "ordinary matter sectors must share one measure/action owner before source variation",
            "PROOF_NOT_CLOSED",
            "component delta_w vector remains needed",
        ),
        (
            "PREFG1485_3_hidden_spurion",
            "hidden/domain/readout/source marker to prefactor Hom",
            "operator domain must exclude source-only coefficient targets or retain them explicitly",
            "OBSTRUCTION_SURVIVES",
            "hidden source coefficient can re-enter",
        ),
        (
            "PREFG1485_4_common_calibration",
            "common w_* absorption into measured G",
            "only derivative-silent universal constant can be absorbed",
            "NOT_SIGNED",
            "Gdot/range/source-normalization rows stay live",
        ),
        (
            "PREFG1485_5_verdict",
            "no-source-only prefactor gate",
            "all source-only prefactor channels must close together before C_parent zero import",
            "FAIL_CURRENT_PROOF",
            "no C_parent zero import",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "target_slot": slot,
            "required_signature": required,
            "current_status": status,
            "if_missing": if_missing,
            "gate_pass": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, slot, required, status, if_missing in rows
    ]


def import_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("IMP1485_0_live_file", str(C_PARENT_IMPORT), C_PARENT_IMPORT.exists(), "REFUSED_LIVE_IMPORT_ABSENT"),
        ("IMP1485_1_functional_derivative", "normalized delta S_parent / delta V_WEP,X", False, "REFUSED_FUNCTIONAL_DERIVATIVE_NOT_EVALUABLE"),
        ("IMP1485_2_derived_zero", "C_parent_X=0 and partial_A C_parent_X=0", False, "REFUSED_DOUBLE_ZERO_NOT_PARENT_SIGNED"),
        ("IMP1485_3_finite_source", "source-backed finite C_parent", False, "REFUSED_FINITE_SOURCE_MISSING"),
        ("IMP1485_4_bound_inversion", "MICROSCOPE bound as coefficient", False, "REFUSED_BOUND_INVERSION_FORBIDDEN"),
        ("IMP1485_5_closure_only", "closure-only C_parent=0", False, "REFUSED_CLOSURE_ONLY_ZERO"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "import_id": import_id,
            "candidate": candidate,
            "candidate_exists_or_passes": passes,
            "import_status": status,
            "import_allowed": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for import_id, candidate, passes, status in rows
    ]


def local_reduction_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LRD1485_0_Newton",
            "Newton source side",
            "T_eff = w_* sum_A T_A with w_* derivative-silent and absorbed into G_N",
            "requires no relative source prefactor and common calibration silence",
            "CONDITIONAL_ONLY",
        ),
        (
            "LRD1485_1_GR_WEP",
            "GR equivalence principle",
            "ordinary matter follows one observed coframe; V_WEP has no bulk matter current",
            "requires parent matter bundle and no species/source-only action weights",
            "CONDITIONAL_ONLY",
        ),
        (
            "LRD1485_2_PPN",
            "PPN/readout residual",
            "same-frame metric readout must not reintroduce source/material labels after variation",
            "requires readout transfer and metric PPN coefficient map",
            "OPEN",
        ),
        (
            "LRD1485_3_WEP_product",
            "MICROSCOPE eta product",
            "eta_pred vanishes if C_parent_X is theorem-zero for every active X; otherwise finite products need bounds",
            "requires C_parent zero/import plus R_material, tau_eff, source/readout data",
            "BLOCKED",
        ),
        (
            "LRD1485_4_verdict",
            "local GR/Newton derivability route",
            "best derivation route is now exact neighbourhood quotient descent of ordinary matter",
            "not signed yet; do not claim local GR",
            "NEXT_DERIVATION_TARGET",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "reduction_id": reduction_id,
            "target_limit": target,
            "required_reduction": required,
            "missing_for_claim": missing,
            "current_status": status,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for reduction_id, target, required, missing, status in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1485_0_parent_action", "MISSING_PARENT_ACTION_OBJECT", "one parent ordinary-matter action object is not source-signed"),
        ("REJ1485_1_neighbourhood_descent", "UNSIGNED_NEIGHBOURHOOD_QUOTIENT_DESCENT", "double-zero needs descent on an open fibre neighbourhood"),
        ("REJ1485_2_generator", "V_WEP_GENERATOR_NOT_PARENT_OWNED", "WEP generator is typed but not parent-derived"),
        ("REJ1485_3_prefactor", "NO_SOURCE_ONLY_PREFACTOR_GATES_OPEN", "w_A/hidden/current/readout prefactor slots remain unsigned"),
        ("REJ1485_4_C_parent", "C_PARENT_IMPORT_REFUSED", "no derived-zero or finite source-backed import row"),
        ("REJ1485_5_local_GR", "LOCAL_GR_REDUCTION_CONDITIONAL_ONLY", "GR/Newton local reduction not yet parent-derived"),
        ("REJ1485_6_no_claim", "CLAIM_PROMOTION_FORBIDDEN", "no WEP/local-GR/Newton claim allowed from 1485"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "blocking_marker": marker,
            "reason": reason,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for rejection_id, marker, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    decisions = [
        ("DEC1485_0_theorem_sharpened", "upgrade the double-zero target from fixed-point stationarity to neighbourhood quotient descent", "this is the mathematically clean way to get C_parent=0 and dC_parent=0", "future proof has a precise parent-signature target"),
        ("DEC1485_1_no_import", "refuse C_parent import", "functional derivative is not evaluable and zero theorem is conditional only", "C_parent remains explicit closure debt"),
        ("DEC1485_2_best_route", "prioritise parent ordinary-matter action signature over more WEP data scoring", "data cannot derive the coupling coefficient", "1486 should try to source/prove neighbourhood descent and MOMS clauses"),
        ("DEC1485_3_local_GR_status", "local GR/Newton route is promising but unclaimed", "we now know exactly what would reduce MTS to GR locally", "claim stays blocked until parent descent is signed"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "why": why,
            "consequence": consequence,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, why, consequence in decisions
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1485_0_1486",
            "next_target": "1486-Y5-R10-RAB-neighbourhood-quotient-descent-or-MOMS-parent-signature-source-map.md",
            "script": "scripts/Y5_R10_RAB_neighbourhood_quotient_descent_or_MOMS_parent_signature_source_map.py",
            "objective": "try to prove/source the open-neighbourhood quotient descent and parent ordinary-matter signature clauses that would turn the conditional C_parent double-zero theorem into a parent-signed local GR/Newton reduction",
            "include": "q-neighbourhood fibre invariance; parent action object; matter bundle functor; fixed constants; no species weights; no shadow/domain/readout reentry; MOMS clause source map",
            "exclude": "GitHub action; formalization-workbench edits; C_parent import; numeric WEP score; closure-only axiom adoption",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def all_claim_flags_false(groups: list[list[dict[str, Any]]]) -> bool:
    for group in groups:
        for row in group:
            if str(row.get("valid_prediction_row", "False")) == "True":
                return False
            if str(row.get("valid_for_claim", "False")) != "False":
                return False
            if str(row.get("claim_allowed", "False")) != "False":
                return False
    return True


def validation_rows(
    sources: list[dict[str, Any]],
    generator: list[dict[str, Any]],
    derivative: list[dict[str, Any]],
    double_zero: list[dict[str, Any]],
    signature: list[dict[str, Any]],
    prefactor: list[dict[str, Any]],
    imports: list[dict[str, Any]],
    local: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated = [
        SOURCE_REGISTER,
        V_GENERATOR,
        FUNCTIONAL_DERIVATIVE,
        DOUBLE_ZERO_ATTEMPT,
        SIGNATURE_GATES,
        PREFATOR_GATES,
        IMPORT_REFUSAL,
        LOCAL_REDUCTION,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    sources_exist = all(row["exists_or_resolved"] for row in sources)
    generator_contract = any(row["generator_id"] == "VGEN1485_4_verdict" and row["current_status"] == "GENERATOR_CONTRACT_ONLY" for row in generator)
    derivative_defined = any(row["definition_id"] == "FD1485_0_definition" and row["current_status"] == "DEFINITION_EXACT_CONDITIONAL" for row in derivative)
    double_zero_sharp = any(row["theorem_id"] == "DZ1485_1_double_zero_corollary" and row["current_status"] == "EXACT_CONDITIONAL_COROLLARY" for row in double_zero)
    double_zero_not_signed = any(row["theorem_id"] == "DZ1485_5_verdict" and row["current_status"] == "PROOF_SHARPENED_NOT_CLOSED" for row in double_zero)
    signature_blocked = len(signature) >= 8 and all(not row["gate_pass"] for row in signature)
    prefactor_blocked = len(prefactor) >= 6 and all(not row["gate_pass"] for row in prefactor)
    import_refused = all(not row["import_allowed"] and not row["claim_allowed"] for row in imports)
    no_live_import = not C_PARENT_IMPORT.exists()
    local_conditional = any(row["reduction_id"] == "LRD1485_4_verdict" and row["current_status"] == "NEXT_DERIVATION_TARGET" for row in local)
    rejections_block = len(rejections) >= 7 and all(not row["claim_allowed"] for row in rejections)
    decisions_nonclaim = all(not row["claim_allowed"] for row in decisions)
    next_ok = len(next_target) == 1 and next_target[0]["next_id"] == "NEXT1485_0_1486"
    csv_parse = all(path.exists() and parse_csv(path) for path in generated)
    copies_exist = all(path.exists() for path in [QUAR_DZERO, QUAR_FDERIV, QUAR_IMPORT, BRANCH_DZERO, BRANCH_FDERIV, BRANCH_IMPORT_REFUSAL])
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = (
        not any(path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*") if path.is_file())
        if FORMALIZATION.exists()
        else True
    )
    claim_flags_false = all_claim_flags_false([sources, generator, derivative, double_zero, signature, prefactor, imports, local, rejections, decisions, next_target])
    checks = [
        ("VAL1485_0_sources", sources_exist, "all cited local source paths exist"),
        ("VAL1485_1_generator_contract", generator_contract, "V_WEP generator is typed but contract-only"),
        ("VAL1485_2_functional_derivative", derivative_defined, "functional derivative definition written exactly as conditional"),
        ("VAL1485_3_double_zero_exact", double_zero_sharp, "neighbourhood descent double-zero corollary written"),
        ("VAL1485_4_double_zero_not_signed", double_zero_not_signed, "double-zero proof remains not parent-signed"),
        ("VAL1485_5_signature_blocked", signature_blocked, "MOMS signature gates remain blocked"),
        ("VAL1485_6_prefactor_blocked", prefactor_blocked, "no-source-only prefactor gates remain blocked"),
        ("VAL1485_7_import_refused", import_refused, "C_parent import refused"),
        ("VAL1485_8_no_live_import", no_live_import, "live C_parent_WEP_slot_import.csv remains absent"),
        ("VAL1485_9_local_conditional", local_conditional, "local GR/Newton reduction remains conditional"),
        ("VAL1485_10_rejections", rejections_block, "rejection ledger blocks claim"),
        ("VAL1485_11_decisions", decisions_nonclaim, "decision ledger keeps claim false"),
        ("VAL1485_12_next", next_ok, "1486 handoff written"),
        ("VAL1485_13_csv_parse", csv_parse, "all generated 1485 CSVs parse cleanly"),
        ("VAL1485_14_branch_copies", copies_exist, "branch/quarantine copies written"),
        ("VAL1485_15_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1485_16_formalization_untouched", formalization_untouched, "formalization modified-file count since start=0"),
        ("VAL1485_17_claim_flags_false", claim_flags_false, "all prediction/claim flags remain false"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": utc_now(),
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1485_18_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1485 sharpens C_parent double-zero to exact neighbourhood descent but keeps local-GR claim blocked",
            "generated_utc": utc_now(),
        }
    )
    return rows


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_COEFF.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(DOUBLE_ZERO_ATTEMPT, QUAR_DZERO)
    shutil.copyfile(FUNCTIONAL_DERIVATIVE, QUAR_FDERIV)
    shutil.copyfile(IMPORT_REFUSAL, QUAR_IMPORT)
    shutil.copyfile(DOUBLE_ZERO_ATTEMPT, BRANCH_DZERO)
    shutil.copyfile(FUNCTIONAL_DERIVATIVE, BRANCH_FDERIV)
    shutil.copyfile(IMPORT_REFUSAL, BRANCH_IMPORT_REFUSAL)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> list[str]:
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return lines


def write_doc(
    generator: list[dict[str, Any]],
    derivative: list[dict[str, Any]],
    double_zero: list[dict[str, Any]],
    signature: list[dict[str, Any]],
    prefactor: list[dict[str, Any]],
    imports: list[dict[str, Any]],
    local: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines = [
        "# 1485 - C Parent WEP Functional Derivative Or Universal Matter Double-Zero Proof",
        "",
        "## Verdict",
        "- The derivation target is now sharper: `C_parent_X` is a parent functional derivative along a WEP generator `V_WEP,X`.",
        "- Exact result: if ordinary matter descends through the quotient on an open fibre neighbourhood, then `C_parent_X=0` throughout that neighbourhood, so both `C_parent_X(Phi0)=0` and `partial_A C_parent_X(Phi0)=0` follow.",
        "- Current corpus does not yet sign that neighbourhood quotient descent or the MOMS ordinary-matter action signature, so no `C_parent` import or local-GR/WEP claim is allowed.",
        "",
        "## V WEP Generator",
    ]
    lines.extend(markdown_table(generator, ["generator_id", "symbol", "current_status", "missing_for_claim"]))
    lines.extend(["", "## Functional Derivative"])
    lines.extend(markdown_table(derivative, ["definition_id", "current_status", "missing_for_import"]))
    lines.extend(["", "## Double-Zero Attempt"])
    lines.extend(markdown_table(double_zero, ["theorem_id", "current_status", "missing_for_parent_claim"]))
    lines.extend(["", "## Signature Gates"])
    lines.extend(markdown_table(signature, ["gate_id", "current_status", "missing_for_adoption"]))
    lines.extend(["", "## Prefactor Gates"])
    lines.extend(markdown_table(prefactor, ["gate_id", "target_slot", "current_status", "if_missing"]))
    lines.extend(["", "## Import Refusal"])
    lines.extend(markdown_table(imports, ["import_id", "candidate_exists_or_passes", "import_status"]))
    lines.extend(["", "## Local GR/Newton Reduction"])
    lines.extend(markdown_table(local, ["reduction_id", "target_limit", "current_status", "missing_for_claim"]))
    lines.extend(["", "## Rejection Ledger"])
    lines.extend(markdown_table(rejections, ["rejection_id", "blocking_marker", "reason"]))
    lines.extend(["", "## Decision Ledger"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} - {row['consequence']}.")
    lines.extend(["", "## Validation"])
    lines.extend(markdown_table(validation, ["check_id", "result", "detail"]))
    lines.extend(["", "## Next Target"])
    lines.extend(markdown_table(next_target, ["next_id", "next_target", "script", "objective"]))
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    generator = v_generator_rows()
    derivative = functional_derivative_rows()
    double_zero = double_zero_attempt_rows()
    signature = signature_gate_rows()
    prefactor = prefactor_gate_rows()
    imports = import_refusal_rows()
    local = local_reduction_rows()
    rejections = rejection_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(V_GENERATOR, generator)
    write_csv(FUNCTIONAL_DERIVATIVE, derivative)
    write_csv(DOUBLE_ZERO_ATTEMPT, double_zero)
    write_csv(SIGNATURE_GATES, signature)
    write_csv(PREFATOR_GATES, prefactor)
    write_csv(IMPORT_REFUSAL, imports)
    write_csv(LOCAL_REDUCTION, local)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)
    copy_outputs()
    validation = validation_rows(sources, generator, derivative, double_zero, signature, prefactor, imports, local, rejections, decisions, next_target)
    write_csv(VALIDATION, validation)
    write_doc(generator, derivative, double_zero, signature, prefactor, imports, local, rejections, decisions, validation, next_target)
    print("Y5_R10_1485_C_parent_double_zero_sharpened_nonclaim")


if __name__ == "__main__":
    main()

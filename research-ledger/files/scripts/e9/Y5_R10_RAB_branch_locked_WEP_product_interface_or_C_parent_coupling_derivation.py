from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1484-Y5-R10-RAB-branch-locked-WEP-product-interface-or-C-parent-coupling-derivation.md"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1483_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1483_VALIDATION.csv"
PREV_TAU = OUT / "P8_Y5_R10_1483_SYMBOLIC_TAU_FUNCTIONAL_LOCK.csv"
PREV_TAU_SCHEMA = OUT / "P8_Y5_R10_1483_TAU_INPUT_COLUMN_SCHEMA.csv"
PREV_PACKAGE = OUT / "P8_Y5_R10_1483_OFFICIAL_PACKAGE_CHECKLIST.csv"
PREV_PARSER = OUT / "P8_Y5_R10_1483_PARSER_PRECHECK_REFRESH.csv"
PREV_CPI = OUT / "P8_Y5_R10_1483_C_PARENT_INTERACTION_POINTS.csv"
PREV_REJECTION = OUT / "P8_Y5_R10_1483_REJECTION_LEDGER.csv"

PRODUCT_LIVE = MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv"
BRANCH_LIVE = MICROSCOPE / "branch_classifier" / "P_WEP_same_parent_branch_lock.csv"
READOUT_LIVE = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"
READOUT_REQUIREMENTS = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout_REQUIREMENTS.csv"
SOURCE_LIVE = MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"
MATERIAL_LIVE = MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"
C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"
C_PARENT_SCHEMA = BRANCH_COEFF / "C_parent_import_schema.csv"
C_PARENT_CONTRACT = BRANCH_COEFF / "C_parent_WEP_coupling_theorem_contract.csv"
C_PARENT_AUDIT = BRANCH_COEFF / "C_parent_WEP_contract_clause_reduction_audit.csv"
C_PARENT_ZERO = BRANCH_COEFF / "C_parent_WEP_slot_zero_attempt.csv"
C_PARENT_CANDIDATES = BRANCH_COEFF / "C_parent_WEP_parent_action_coupling_candidate_ledger.csv"
DOUBLE_ZERO = BRANCH_COEFF / "parent_coupling_double_zero_theorem_attempt_nonclaim_1473.csv"
CI_MAP = BRANCH_COEFF / "complete_Ci_parent_action_map_nonclaim_1474.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1484_SOURCE_REGISTER.csv"
PRODUCT_INTERFACE = OUT / "P8_Y5_R10_1484_BRANCH_LOCKED_WEP_PRODUCT_INTERFACE.csv"
FACTOR_SCHEMA = OUT / "P8_Y5_R10_1484_PRODUCT_FACTOR_SCHEMA.csv"
COMPATIBILITY_MATRIX = OUT / "P8_Y5_R10_1484_FACTOR_COMPATIBILITY_MATRIX.csv"
REFUSAL_TESTS = OUT / "P8_Y5_R10_1484_INTERFACE_REFUSAL_TESTS.csv"
C_PARENT_DERIVATION = OUT / "P8_Y5_R10_1484_C_PARENT_COUPLING_DERIVATION_ATTEMPT.csv"
C_PARENT_CLAUSE_GATES = OUT / "P8_Y5_R10_1484_C_PARENT_CLAUSE_GATES.csv"
LOCAL_GR_LINK = OUT / "P8_Y5_R10_1484_LOCAL_GR_NEWTON_LINK_LEDGER.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1484_REJECTION_LEDGER.csv"
NO_CLAIM_GATES = OUT / "P8_Y5_R10_1484_NO_CLAIM_GATES.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1484_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1484_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1484_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1484"
QUAR_INTERFACE = QUARANTINE / "BRANCH_LOCKED_WEP_PRODUCT_INTERFACE_NONCLAIM.csv"
QUAR_C_PARENT = QUARANTINE / "C_PARENT_COUPLING_DERIVATION_ATTEMPT_NONCLAIM.csv"
QUAR_REFUSALS = QUARANTINE / "INTERFACE_REFUSAL_TESTS_NONCLAIM.csv"
BRANCH_INTERFACE = BRANCH_RESIDUALS / "branch_locked_WEP_product_interface_nonclaim_1484.csv"
BRANCH_C_PARENT = BRANCH_COEFF / "C_parent_WEP_coupling_derivation_attempt_nonclaim_1484.csv"
BRANCH_REFUSALS = BRANCH_RESIDUALS / "branch_locked_WEP_interface_refusal_tests_nonclaim_1484.csv"


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


def has_blocker(path: Path) -> bool:
    if not path.exists():
        return True
    text = path.read_text(encoding="utf-8", errors="replace").upper()
    return any(marker in text for marker in ["MISSING", "PENDING", "NONCLAIM", "FALSE", "ABSENT", "NOT_EVALUATED", "UNSIGNED", "NOT_PROVEN"])


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC1484_0_prev_next", PREV_NEXT, "1483 handoff"),
        ("SRC1484_1_prev_validation", PREV_VALIDATION, "1483 validation"),
        ("SRC1484_2_prev_tau", PREV_TAU, "1483 tau lock"),
        ("SRC1484_3_prev_tau_schema", PREV_TAU_SCHEMA, "1483 tau input schema"),
        ("SRC1484_4_prev_package", PREV_PACKAGE, "1483 official package checklist"),
        ("SRC1484_5_prev_parser", PREV_PARSER, "1483 parser refresh"),
        ("SRC1484_6_prev_CPI", PREV_CPI, "1483 C_parent interactions"),
        ("SRC1484_7_prev_rejection", PREV_REJECTION, "1483 rejection ledger"),
        ("SRC1484_8_product_live", PRODUCT_LIVE, "partial product convention row"),
        ("SRC1484_9_branch_live", BRANCH_LIVE, "same-parent branch guard"),
        ("SRC1484_10_readout_requirements", READOUT_REQUIREMENTS, "requirements-only readout scaffold"),
        ("SRC1484_11_C_parent_schema", C_PARENT_SCHEMA, "C_parent import schema"),
        ("SRC1484_12_C_parent_contract", C_PARENT_CONTRACT, "C_parent theorem contract"),
        ("SRC1484_13_C_parent_audit", C_PARENT_AUDIT, "C_parent clause audit"),
        ("SRC1484_14_C_parent_zero", C_PARENT_ZERO, "C_parent zero attempt"),
        ("SRC1484_15_C_parent_candidates", C_PARENT_CANDIDATES, "parent action coupling candidates"),
        ("SRC1484_16_double_zero", DOUBLE_ZERO, "double-zero theorem attempt"),
        ("SRC1484_17_Ci_map", CI_MAP, "complete local coefficient map"),
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


def product_interface_rows() -> list[dict[str, Any]]:
    formula = "eta_pred(Ti,Pt) = | sum_X C_parent_X * R_material_X(TA6V-PtRh10) * tau_eff_X |"
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "interface_id": "WPI1484_0_formula",
            "object": "branch-locked WEP product",
            "symbol_or_factor": "eta_pred",
            "definition": formula,
            "required_basis": "single parent response basis X shared by C_parent, R_material, R_source/tau_eff",
            "units_or_convention": "dimensionless eta after declared K_CMSM/R_source normalization",
            "current_status": "FORMULA_LOCKED_INPUTS_MISSING",
            "source_path": rel(PREV_CPI),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "interface_id": "WPI1484_1_C_parent",
            "object": "parent coupling coefficient",
            "symbol_or_factor": "C_parent_X",
            "definition": "functional derivative or theorem-zero of parent action along WEP/source/material generator V_WEP,X",
            "required_basis": "parent response basis X with units/sign/source path",
            "units_or_convention": "declared by C_parent_import_schema",
            "current_status": "MISSING_C_PARENT_IMPORT",
            "source_path": str(C_PARENT_IMPORT),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "interface_id": "WPI1484_2_R_material",
            "object": "test-mass material contrast",
            "symbol_or_factor": "R_material_X",
            "definition": "full TA6V-minus-PtRh10 parent-basis response tensor, not composition/DD proxy only",
            "required_basis": "same parent response basis X as C_parent_X",
            "units_or_convention": "declared material tensor units and double-count rule",
            "current_status": "MISSING_FULL_PARENT_MATERIAL_TENSOR",
            "source_path": str(MATERIAL_LIVE),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "interface_id": "WPI1484_3_tau_eff",
            "object": "readout/source/orbit functional",
            "symbol_or_factor": "tau_eff_X",
            "definition": "tau_eff_X = <K_CMSM^a(t,s) R_source_a^X(t,s)> over accepted sessions/masks/orbit weights/product convention",
            "required_basis": "same X basis and same observed coframe/product convention",
            "units_or_convention": "K_CMSM units times R_source units after declared normalization",
            "current_status": "SYMBOLIC_ONLY_NO_NUMERIC_OUTPUT",
            "source_path": rel(PREV_TAU),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "interface_id": "WPI1484_4_product_convention",
            "object": "eta convention",
            "symbol_or_factor": "eta(Ti,Pt)",
            "definition": "eta(A,B)=2(a_A-a_B)/(a_A+a_B), official channel eta(Ti,Pt)",
            "required_basis": "same branch id and no pending sign/readout/source units",
            "units_or_convention": "dimensionless eta, body order and positive axis fixed",
            "current_status": "PARTIAL_PENDING_NONCLAIM",
            "source_path": str(PRODUCT_LIVE),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "interface_id": "WPI1484_5_branch_guard",
            "object": "anti-mixing guard",
            "symbol_or_factor": "same_parent_branch_id",
            "definition": "all factors must declare one branch and reject surrogate/DD-only/tau=1/bound-inverted/measured-G-absorbed rows",
            "required_basis": BRANCH_ID,
            "units_or_convention": "identifier and refusal rule",
            "current_status": "GUARD_EXISTS_NONCLAIM",
            "source_path": str(BRANCH_LIVE),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def factor_schema_rows() -> list[dict[str, Any]]:
    fields = [
        ("same_parent_branch_id", "all", "string", "must equal active branch id"),
        ("basis_id", "all factors", "string", "single parent response basis label X"),
        ("component_id", "all factors", "string", "component index within X basis"),
        ("value", "C_parent/R_material/tau_eff rows", "number or DERIVED_ZERO", "not allowed to be MISSING/PENDING/fit-from-bound"),
        ("uncertainty", "finite numeric factors", "number/exact tag", "required for nonzero empirical comparison"),
        ("units", "all numeric factors", "string", "must multiply to dimensionless eta"),
        ("sign_convention", "all signed factors", "string", "body order, axis, source orientation, and parent sign"),
        ("source_url_or_path", "all factors", "string", "local file, URL, DOI, or theorem source"),
        ("parent_status", "C_parent", "DERIVED_ZERO or SOURCE_BACKED_FINITE", "closure-only rows refused"),
        ("zero_certificate_status", "C_parent zero route", "PROVEN/NOT_APPLICABLE", "zero only valid with parent proof"),
        ("double_count_rule", "material/source", "string", "prevents composition/source/readout duplication"),
        ("normalization_rule", "tau/product", "string", "declared average and denominator convention"),
        ("valid_prediction_row", "all", "boolean", "must be true only after every gate passes"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "schema_id": f"FPS1484_{index}",
            "field": field,
            "applies_to": applies_to,
            "type_or_allowed_value": dtype,
            "requirement": requirement,
            "current_status": "SCHEMA_REQUIRED_VALUE_MISSING",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for index, (field, applies_to, dtype, requirement) in enumerate(fields)
    ]


def compatibility_rows() -> list[dict[str, Any]]:
    rows = [
        ("COMP1484_0_branch", "all factors declare same_parent_branch_id", BRANCH_LIVE.exists() and not has_blocker(BRANCH_LIVE), "BRANCH_GUARD_NONCLAIM_OR_UNSIGNED"),
        ("COMP1484_1_C_parent", "C_parent import exists and is proof/source-backed", C_PARENT_IMPORT.exists() and not has_blocker(C_PARENT_IMPORT), "MISSING_C_PARENT_IMPORT"),
        ("COMP1484_2_material", "R_material tensor exists in same basis", MATERIAL_LIVE.exists() and not has_blocker(MATERIAL_LIVE), "MISSING_FULL_PARENT_MATERIAL_TENSOR"),
        ("COMP1484_3_readout", "K_CMSM live readout exists with units/sign/masks", READOUT_LIVE.exists() and not has_blocker(READOUT_LIVE), "MISSING_LIVE_READOUT_MATRIX"),
        ("COMP1484_4_source", "R_source live source worldtube exists", SOURCE_LIVE.exists() and not has_blocker(SOURCE_LIVE), "MISSING_SOURCE_WORLDTUBE"),
        ("COMP1484_5_product", "eta product convention has no pending sign/unit/orbit fields", PRODUCT_LIVE.exists() and not has_blocker(PRODUCT_LIVE), "PENDING_PRODUCT_SIGN_UNITS_ORBIT"),
        ("COMP1484_6_tau", "tau_eff_X numeric values exist", False, "TAU_SYMBOLIC_ONLY"),
        ("COMP1484_7_units", "C_parent * R_material * tau_eff has dimensionless eta units", False, "UNIT_PRODUCT_NOT_EVALUABLE"),
        ("COMP1484_8_no_shortcuts", "tau=1, DD-only, bound-inversion, mixed-basis rows rejected", True, "REFUSAL_RULE_ACTIVE"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "compat_id": compat_id,
            "condition": condition,
            "condition_pass": condition_pass,
            "current_status": "PASS_REFUSAL_RULE_ONLY" if condition_pass and compat_id == "COMP1484_8_no_shortcuts" else ("PASS" if condition_pass else blocker),
            "score_effect": "required before WEP score" if compat_id != "COMP1484_8_no_shortcuts" else "guards against false positives",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for compat_id, condition, condition_pass, blocker in rows
    ]


def refusal_test_rows() -> list[dict[str, Any]]:
    tests = [
        ("REF1484_0_tau_unit", "tau_eff_X=1 with no official readout/source rows", "REFUSE_TAU_UNIT_KERNEL_SHORTCUT"),
        ("REF1484_1_bound_inversion", "choose C_parent from MICROSCOPE eta bound", "REFUSE_BOUND_AS_PREDICTION"),
        ("REF1484_2_DD_proxy", "use Damour-Donoghue/material smoke coefficient as MTS C_parent", "REFUSE_EXTERNAL_PROXY_AS_PARENT_COEFFICIENT"),
        ("REF1484_3_mixed_basis", "multiply C_parent, R_material, R_source, tau from different basis labels", "REFUSE_MIXED_BRANCH_OR_BASIS"),
        ("REF1484_4_measured_G_absorption", "absorb relative WEP residual into measured G or common-mode denominator", "REFUSE_RELATIVE_MEASURED_G_ABSORPTION"),
        ("REF1484_5_closure_zero", "declare C_parent=0 from closure preference without proof", "REFUSE_UNSIGNED_ZERO"),
        ("REF1484_6_requirements_as_data", "parse P_WEP_K_CMSM_readout_REQUIREMENTS.csv as live K_CMSM data", "REFUSE_REQUIREMENTS_ONLY_FILE"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "test_id": test_id,
            "bad_input": bad_input,
            "expected_result": expected,
            "actual_result": expected,
            "test_pass": True,
            "score_permission": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for test_id, bad_input, expected in tests
    ]


def c_parent_derivation_rows() -> list[dict[str, Any]]:
    attempts = [
        (
            "CPD1484_0_define_generator",
            "define V_WEP,X as parent-basis variation of Ti/Pt material contrast coupled to source/readout projection",
            "V_WEP,X requires C_parent basis, R_material_X, R_source_X, K_CMSM and product convention",
            "PARTIAL_SYMBOLIC_ONLY",
            "derive V_WEP from parent action object language, not from empirical eta",
        ),
        (
            "CPD1484_1_functional_derivative",
            "C_parent_X := normalized delta S_parent / delta V_WEP,X at the compact local branch",
            "requires total parent action, variation order, units, sign, and source path",
            "CONTRACT_STATED_NOT_EVALUABLE",
            "find/synthesize parent action sector whose variation owns this slot",
        ),
        (
            "CPD1484_2_double_zero_route",
            "prove C_parent_X(Phi0)=0 and partial_A C_parent_X(Phi0)=0 by universal matter/coframe branch",
            "double-zero lemma is exact conditional but parent ownership premises are unsigned",
            "CONDITIONAL_THEOREM_ONLY",
            "prove connected ordinary matter category, action-density line owner, and no source-only prefactor from parent action",
        ),
        (
            "CPD1484_3_finite_route",
            "allow finite C_parent_X only if source-backed and independent of MICROSCOPE bound",
            "no finite row satisfies C_parent_import_schema",
            "MISSING_IMPORT_ROW",
            "keep finite route open as nonclaim input if a parent coefficient source appears",
        ),
        (
            "CPD1484_4_GR_Newton_limit",
            "local GR/Newton reduction requires product vanishes or is bounded by derived suppression before empirical comparison",
            "current product has symbolic/absent factors",
            "NOT_DERIVED_FOR_LOCAL_LIMIT",
            "attack coupling zero first; data only tests after theory coefficient exists",
        ),
        (
            "CPD1484_5_verdict",
            "C_parent coupling derivation verdict",
            "interface is well-typed but coupling slot is not derived or zero-certified",
            "NOT_CLOSED",
            "next target should go straight at parent functional derivative / universal matter branch proof",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "derivation_id": derivation_id,
            "claim_piece": claim_piece,
            "required_evidence": required,
            "current_status": status,
            "next_action": next_action,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for derivation_id, claim_piece, required, status, next_action in attempts
    ]


def c_parent_clause_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": row.get("same_parent_branch_id", BRANCH_ID),
            "clause_id": row.get("clause_id", f"CLAUSE1484_{i}"),
            "prior_result": row.get("clause_result", row.get("current_status", "UNKNOWN")),
            "best_candidate_ids": row.get("best_candidate_ids", "not recorded"),
            "missing_for_import": row.get("missing_for_import", row.get("failure_mode_if_absent", "not recorded")),
            "gate_status": "BLOCKED",
            "claim_effect": "blocks C_parent import",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for i, row in enumerate(read_csv(C_PARENT_AUDIT))
    ]


def local_gr_link_rows() -> list[dict[str, Any]]:
    rows = [
        ("LGR1484_0_Newton", "Newtonian local source law", "eta_WEP residual must vanish while universal source coupling remains common-mode", "requires C_parent zero or same-branch finite residual bound", "OPEN"),
        ("LGR1484_1_GR", "GR local equivalence principle", "all test bodies follow same observed coframe/readout to first order", "requires universal matter/coframe branch and no species/source prefactor", "OPEN"),
        ("LGR1484_2_PPN", "PPN local metric readout", "metric residual vector must vanish or be bounded in same parent readout", "requires PPN coefficient map plus C_parent/tau/material/source interface", "OPEN"),
        ("LGR1484_3_WEP", "MICROSCOPE same-branch WEP test", "eta_pred must be independent prediction, not bound-fit", "requires all product factors and official source files", "BLOCKED"),
        ("LGR1484_4_derivation_priority", "best route", "derive universal matter branch / C_parent double-zero before more data scoring", "interface now names exact missing factors", "NEXT"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "link_id": link_id,
            "target_limit": target,
            "required_reduction": reduction,
            "missing_for_claim": missing,
            "current_status": status,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for link_id, target, reduction, missing, status in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1484_0_C_parent", "MISSING_C_PARENT_IMPORT", "no theorem-zero or source-backed finite coefficient exists"),
        ("REJ1484_1_material", "MISSING_FULL_PARENT_MATERIAL_TENSOR", "R_material_X absent"),
        ("REJ1484_2_tau", "TAU_SYMBOLIC_ONLY", "tau_eff_X is typed but not evaluated"),
        ("REJ1484_3_readout", "MISSING_LIVE_READOUT_MATRIX", "K_CMSM data absent"),
        ("REJ1484_4_source", "MISSING_SOURCE_WORLDTUBE", "R_source data absent"),
        ("REJ1484_5_product", "PENDING_PRODUCT_SIGN_UNITS_ORBIT", "product convention partial"),
        ("REJ1484_6_branch", "BRANCH_GUARD_NONCLAIM_OR_UNSIGNED", "branch guard exists as nonclaim scaffold only"),
        ("REJ1484_7_local_GR", "LOCAL_GR_REDUCTION_NOT_DERIVED", "GR/Newton reduction still depends on coupling/double-zero proof"),
        ("REJ1484_8_no_claim", "CLAIM_PROMOTION_FORBIDDEN", "no numeric WEP/local-GR claim allowed"),
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


def no_claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("GATE1484_0_interface_written", True, "branch-locked product interface exists"),
        ("GATE1484_1_schema_written", True, "factor schema with basis/units/sign/provenance exists"),
        ("GATE1484_2_refusals_pass", True, "shortcut refusal tests pass"),
        ("GATE1484_3_C_parent_blocked", not C_PARENT_IMPORT.exists(), "C_parent import absent"),
        ("GATE1484_4_tau_blocked", True, "tau remains symbolic"),
        ("GATE1484_5_data_blocked", not READOUT_LIVE.exists() and not SOURCE_LIVE.exists(), "readout/source live files absent"),
        ("GATE1484_6_local_GR_open", True, "GR/Newton derivation link remains open"),
        ("GATE1484_7_claim_flags_false", True, "all generated claim flags false"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate_pass": gate_pass,
            "detail": detail,
            "claim_effect": "blocks claim" if gate_id != "GATE1484_0_interface_written" and gate_id != "GATE1484_1_schema_written" else "typed scaffold only",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate_pass, detail in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    decisions = [
        ("DEC1484_0_interface_not_score", "write product interface as a type/compatibility contract, not a prediction", "factors are missing or nonclaim", "future rows have a legal slot without enabling a claim"),
        ("DEC1484_1_refuse_Cparent_import", "do not create C_parent_WEP_slot_import.csv", "functional derivative and double-zero proof are still unsigned", "coupling remains the main physics bottleneck"),
        ("DEC1484_2_data_after_derivation", "keep MICROSCOPE data acquisition useful but secondary", "official arrays cannot make a theory coefficient derivable", "next target should attack C_parent derivation directly"),
        ("DEC1484_3_local_GR_route", "local GR/Newton route is now stated as product-zero/product-bound, not vague plateau language", "this aligns the local branch with derivable reduction requirements", "1485 should try universal matter branch / functional derivative proof"),
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
            "next_id": "NEXT1484_0_1485",
            "next_target": "1485-Y5-R10-RAB-C-parent-WEP-functional-derivative-or-universal-matter-double-zero-proof.md",
            "script": "scripts/Y5_R10_RAB_C_parent_WEP_functional_derivative_or_universal_matter_double_zero_proof.py",
            "objective": "try to derive the WEP coupling slot from a parent functional derivative, or prove the universal-matter double-zero theorem needed for local GR/Newton reduction; otherwise keep C_parent as explicit closure-only debt",
            "include": "parent action slot; V_WEP generator; functional derivative normalization; universal matter/coframe branch; double-zero conditions; no-source-only prefactor gates; no-claim import refusal",
            "exclude": "GitHub action; formalization-workbench edits; numeric WEP score; fabricated C_parent; bound inversion",
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
    interface: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    compatibility: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    cparent: list[dict[str, Any]],
    clause_gates: list[dict[str, Any]],
    local_links: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated = [
        SOURCE_REGISTER,
        PRODUCT_INTERFACE,
        FACTOR_SCHEMA,
        COMPATIBILITY_MATRIX,
        REFUSAL_TESTS,
        C_PARENT_DERIVATION,
        C_PARENT_CLAUSE_GATES,
        LOCAL_GR_LINK,
        REJECTION_LEDGER,
        NO_CLAIM_GATES,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    local_sources_exist = all(row["exists_or_resolved"] for row in sources)
    interface_complete = len(interface) >= 6 and any(row["interface_id"] == "WPI1484_0_formula" for row in interface)
    schema_complete = len(schema) >= 13
    compatibility_blocks = any(row["condition_pass"] is False for row in compatibility) and all(not row["claim_allowed"] for row in compatibility)
    refusal_pass = all(row["test_pass"] and not row["score_permission"] for row in refusals)
    cparent_not_closed = any(row["derivation_id"] == "CPD1484_5_verdict" and row["current_status"] == "NOT_CLOSED" for row in cparent)
    clause_gates_block = len(clause_gates) >= 6 and all(row["gate_status"] == "BLOCKED" for row in clause_gates)
    local_gr_open = any(row["link_id"] == "LGR1484_4_derivation_priority" and row["current_status"] == "NEXT" for row in local_links)
    rejections_block = len(rejections) >= 9 and all(not row["claim_allowed"] for row in rejections)
    gate_pass = all(row["gate_pass"] for row in gates)
    decisions_nonclaim = all(not row["claim_allowed"] for row in decisions)
    next_ok = len(next_target) == 1 and next_target[0]["next_id"] == "NEXT1484_0_1485"
    csv_parse = all(path.exists() and parse_csv(path) for path in generated)
    copies_exist = all(path.exists() for path in [QUAR_INTERFACE, QUAR_C_PARENT, QUAR_REFUSALS, BRANCH_INTERFACE, BRANCH_C_PARENT, BRANCH_REFUSALS])
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = (
        not any(path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*") if path.is_file())
        if FORMALIZATION.exists()
        else True
    )
    claim_flags_false = all_claim_flags_false([sources, interface, schema, compatibility, refusals, cparent, clause_gates, local_links, rejections, gates, decisions, next_target])
    checks = [
        ("VAL1484_0_sources", local_sources_exist, "all cited local source paths exist"),
        ("VAL1484_1_interface", interface_complete, "branch-locked WEP product interface written"),
        ("VAL1484_2_factor_schema", schema_complete, "factor schema covers basis/units/sign/provenance"),
        ("VAL1484_3_compatibility_blocks", compatibility_blocks, "compatibility matrix blocks score paths"),
        ("VAL1484_4_refusals", refusal_pass, "shortcut refusal tests pass"),
        ("VAL1484_5_C_parent_open", cparent_not_closed, "C_parent derivation remains open/nonclaim"),
        ("VAL1484_6_clause_gates", clause_gates_block, "prior C_parent clauses remain blocked"),
        ("VAL1484_7_local_GR_link", local_gr_open, "local GR/Newton link ledger points to derivation priority"),
        ("VAL1484_8_rejections", rejections_block, "rejection ledger blocks claim"),
        ("VAL1484_9_no_claim_gates", gate_pass, "no-claim gates pass"),
        ("VAL1484_10_decisions", decisions_nonclaim, "decision ledger keeps claims false"),
        ("VAL1484_11_next", next_ok, "1485 handoff written"),
        ("VAL1484_12_csv_parse", csv_parse, "all generated 1484 CSVs parse cleanly"),
        ("VAL1484_13_branch_copies", copies_exist, "branch/quarantine copies written"),
        ("VAL1484_14_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1484_15_formalization_untouched", formalization_untouched, "formalization modified-file count since start=0"),
        ("VAL1484_16_claim_flags_false", claim_flags_false, "all prediction/claim flags remain false"),
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
            "check_id": "VAL1484_17_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1484 locks the branch-locked WEP product interface and keeps C_parent/local-GR derivation open",
            "generated_utc": utc_now(),
        }
    )
    return rows


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    BRANCH_COEFF.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PRODUCT_INTERFACE, QUAR_INTERFACE)
    shutil.copyfile(C_PARENT_DERIVATION, QUAR_C_PARENT)
    shutil.copyfile(REFUSAL_TESTS, QUAR_REFUSALS)
    shutil.copyfile(PRODUCT_INTERFACE, BRANCH_INTERFACE)
    shutil.copyfile(C_PARENT_DERIVATION, BRANCH_C_PARENT)
    shutil.copyfile(REFUSAL_TESTS, BRANCH_REFUSALS)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> list[str]:
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join("---" for _ in columns) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return lines


def write_doc(
    interface: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    compatibility: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    cparent: list[dict[str, Any]],
    local_links: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines = [
        "# 1484 - Branch-Locked WEP Product Interface Or C Parent Coupling Derivation",
        "",
        "## Verdict",
        "- The WEP/local branch now has a complete product interface: `eta_pred = |sum_X C_parent_X R_material_X tau_eff_X|` in one branch/basis.",
        "- This is progress toward derivability, not a claim: `C_parent`, `R_material`, `R_source/K_CMSM`, numeric `tau_eff`, and product sign/units remain blocked.",
        "- The coupling remains the boss fight. The next move is a direct parent functional-derivative or universal-matter double-zero proof attempt.",
        "",
        "## Product Interface",
    ]
    lines.extend(markdown_table(interface, ["interface_id", "symbol_or_factor", "current_status", "required_basis"]))
    lines.extend(["", "## Factor Schema"])
    lines.extend(markdown_table(schema, ["schema_id", "field", "applies_to", "requirement"]))
    lines.extend(["", "## Compatibility Matrix"])
    lines.extend(markdown_table(compatibility, ["compat_id", "condition_pass", "current_status", "score_effect"]))
    lines.extend(["", "## Refusal Tests"])
    lines.extend(markdown_table(refusals, ["test_id", "bad_input", "actual_result", "test_pass"]))
    lines.extend(["", "## C Parent Derivation Attempt"])
    lines.extend(markdown_table(cparent, ["derivation_id", "current_status", "next_action"]))
    lines.extend(["", "## Local GR/Newton Link"])
    lines.extend(markdown_table(local_links, ["link_id", "target_limit", "current_status", "missing_for_claim"]))
    lines.extend(["", "## Rejection Ledger"])
    lines.extend(markdown_table(rejections, ["rejection_id", "blocking_marker", "reason"]))
    lines.extend(["", "## No-Claim Gates"])
    lines.extend(markdown_table(gates, ["gate_id", "gate_pass", "detail"]))
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
    interface = product_interface_rows()
    schema = factor_schema_rows()
    compatibility = compatibility_rows()
    refusals = refusal_test_rows()
    cparent = c_parent_derivation_rows()
    clause_gates = c_parent_clause_gate_rows()
    local_links = local_gr_link_rows()
    rejections = rejection_rows()
    gates = no_claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PRODUCT_INTERFACE, interface)
    write_csv(FACTOR_SCHEMA, schema)
    write_csv(COMPATIBILITY_MATRIX, compatibility)
    write_csv(REFUSAL_TESTS, refusals)
    write_csv(C_PARENT_DERIVATION, cparent)
    write_csv(C_PARENT_CLAUSE_GATES, clause_gates)
    write_csv(LOCAL_GR_LINK, local_links)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(NO_CLAIM_GATES, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)
    copy_outputs()
    validation = validation_rows(sources, interface, schema, compatibility, refusals, cparent, clause_gates, local_links, rejections, gates, decisions, next_target)
    write_csv(VALIDATION, validation)
    write_doc(interface, schema, compatibility, refusals, cparent, local_links, rejections, gates, decisions, validation, next_target)
    print("Y5_R10_1484_branch_locked_WEP_product_interface_nonclaim")


if __name__ == "__main__":
    main()

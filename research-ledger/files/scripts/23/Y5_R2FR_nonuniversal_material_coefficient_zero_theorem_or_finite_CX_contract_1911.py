from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1911"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1911-Y5-R2FR-nonuniversal-material-coefficient-zero-theorem-or-finite-CX-contract.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1910_doc": ROOT / "1910-Y5-R2FR-parent-material-response-functional-or-exact-mass-defect-tensor-contract.md",
    "1910_validation": OUT / "P8_Y5_BRR545_1910_VALIDATION.csv",
    "1910_response": OUT / "P8_Y5_PARENT_QLOC_1910_PARENT_MATERIAL_RESPONSE_FUNCTIONAL_ATTEMPT.csv",
    "1910_common_mode": OUT / "P8_Y5_PARENT_QLOC_1910_COMMON_MODE_ZERO_THEOREM_CONDITIONAL.csv",
    "1910_tensor_contract": OUT / "P8_Y5_PARENT_QLOC_1910_EXACT_MASS_DEFECT_TENSOR_CONTRACT_NONCLAIM.csv",
    "1910_next": OUT / "P8_Y5_PARENT_QLOC_1910_NEXT_TARGET.csv",
    "minimal_parent_clause": MICROSCOPE_COEFFS / "C_parent_WEP_minimal_parent_clause.csv",
    "universal_double_zero": MICROSCOPE_COEFFS / "universal_matter_double_zero_attempt_nonclaim_1485.csv",
    "no_source_slot": MICROSCOPE_COEFFS / "no_source_only_slot_operator_grammar_theorem_attempt_1451.csv",
    "no_source_slot_decision": MICROSCOPE_COEFFS / "C_parent_WEP_no_source_slot_signing_decision_1451.csv",
    "source_label_forgetting": MICROSCOPE_COEFFS / "source_label_forgetting_proof_attempt_nonclaim_1476.csv",
    "source_label_decision": MICROSCOPE_COEFFS / "source_label_forgetting_signing_decision_1476.csv",
    "connected_category_decision": MICROSCOPE_COEFFS / "C_parent_WEP_connected_matter_category_signing_decision_1464.csv",
    "common_measure_decision": MICROSCOPE_COEFFS / "C_parent_WEP_common_measure_current_signature_decision_1462.csv",
    "readout_order_decision": MICROSCOPE_COEFFS / "C_parent_WEP_readout_order_signing_decision_1454.csv",
    "hidden_invariant_decision": MICROSCOPE_COEFFS / "C_parent_WEP_hidden_invariant_signing_decision_1469.csv",
    "em_decision": MICROSCOPE_COEFFS / "C_parent_WEP_EM_edge_signing_decision_1466.csv",
    "cparent_contract": OUT / "P8_Y5_R10_1080_C_PARENT_COEFFICIENT_CONTRACT.csv",
}


SOURCE_NEEDLES = {
    "1910_doc": ["NEXT1910_0_primary", "1911-Y5-R2FR-nonuniversal-material-coefficient-zero-theorem-or-finite-CX-contract.md"],
    "1910_validation": ["VAL1910_OVERALL,PASS"],
    "1910_response": ["MRF1910_5_verdict", "CONDITIONAL_RESPONSE_FUNCTIONAL_DERIVED_PARENT_PROMOTION_BLOCKED"],
    "1910_common_mode": ["CMZ1910_3_verdict", "LOCAL_GR_ROUTE_SHARP_BUT_UNSIGNED"],
    "1910_tensor_contract": ["MDT1910_7_source_readout_product", "MISSING_SOURCE_READOUT_TAU_KERNEL"],
    "1910_next": ["NEXT1910_0_primary", "nonuniversal material coefficient zero theorem"],
    "minimal_parent_clause": ["MPC1439_4_verdict", "NOT_ADOPTED_NOT_ZERO_CERTIFIED"],
    "universal_double_zero": ["DZ1485_5_verdict", "PROOF_SHARPENED_NOT_CLOSED"],
    "no_source_slot": ["OG1451_6_verdict", "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED"],
    "no_source_slot_decision": ["SIGN1451_0_no_slot", "REFUSE_ZERO_IMPORT_KEEP_BOUND_INPUTS"],
    "source_label_forgetting": ["SLF1476_4_verdict", "NOT_PARENT_DERIVED_EMIT_DELTA_W_INPUT_ROW"],
    "source_label_decision": ["SIGN1476_0_source_label_forgetting", "REFUSE_SOURCE_LABEL_FORGETTING_PROMOTION"],
    "connected_category_decision": ["SIGN1464_0_connected_matter_category", "KEEP_CONNECTEDNESS_CONDITIONAL"],
    "common_measure_decision": ["SIGN1462_0_common_measure_current", "REFUSE_COMMON_MEASURE_ZERO_IMPORT"],
    "readout_order_decision": ["SIGN1454_0_readout_order", "REFUSE_READOUT_ORDER_ZERO_IMPORT"],
    "hidden_invariant_decision": ["SIGN1469_0_hidden_invariant", "REFUSE_HIDDEN_ALGEBRA_PROMOTION"],
    "em_decision": ["SIGN1466_0_EM_edge", "KEEP_EM_EDGE_AS_EXACT_CONDITIONAL"],
    "cparent_contract": ["CP1080_0_definition", "MISSING_PARENT_COEFFICIENT"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1911_SOURCE_REGISTER.csv",
    "zero_theorem": OUT / "P8_Y5_PARENT_QLOC_1911_NONUNIVERSAL_COEFFICIENT_ZERO_THEOREM_ATTEMPT.csv",
    "premise_matrix": OUT / "P8_Y5_PARENT_QLOC_1911_ZERO_THEOREM_PREMISE_MATRIX_NONCLAIM.csv",
    "finite_cx_contract": OUT / "P8_Y5_PARENT_QLOC_1911_FINITE_CX_CONTRACT_NONCLAIM.csv",
    "zero_import_tests": OUT / "P8_Y5_PARENT_QLOC_1911_ZERO_IMPORT_REFUSAL_TESTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1911_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1911_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1911_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1911_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1911_VALIDATION.csv",
}


BRANCH_COPIES = {
    "zero_theorem": SOURCE_WEIGHT_DOCS / "NONUNIVERSAL_CX_ZERO_THEOREM_1911_NONCLAIM.csv",
    "finite_cx_contract": MICROSCOPE_COEFFS / "C_parent_WEP_finite_CX_contract_1911_nonclaim.csv",
    "premise_matrix": QUEUE / "JR1911_ZERO_THEOREM_PREMISE_MATRIX_NONCLAIM.csv",
}


def ensure_dirs() -> None:
    for path in [OUT, MICROSCOPE_RESIDUALS, MICROSCOPE_COEFFS, QUEUE, SOURCE_WEIGHT_DOCS, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value).strip().lower()


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        missing = [needle for needle in SOURCE_NEEDLES[source_id] if needle not in text]
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle_count": len(SOURCE_NEEDLES[source_id]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "SOURCE_OR_NEEDLE_MISSING",
                "valid_for_claim": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def zero_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "CXZ1911_0_target",
            "claim_piece": "nonuniversal material coefficient zero theorem",
            "formal_statement": "For each nonuniversal material response channel X in {electron, light_quark, EM_Coulomb, nuclear_binding, QCD_gluon, lattice}, prove C_X=0 before WEP readout.",
            "proof_status": "TARGET_SHARP",
            "proof_move": "reduce every nonuniversal material variation to a vertical variation in ker(Dq_obs) of a descended ordinary-matter action",
            "current_blocker": "ordinary-matter neighbourhood quotient descent is not parent-signed",
            "source_anchor": "CMZ1910_3_verdict; DZ1485_5_verdict",
            "zero_import_allowed": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "CXZ1911_1_descent_theorem",
            "claim_piece": "quotient descent implies C_X=0",
            "formal_statement": "If S_ord = Sbar_ord[q(Phi), Psi[q(Phi)], theta] on an open neighbourhood U and V_X is vertical on every fibre in U, then C_X(Phi)=delta_VX S_ord(Phi)=0 throughout U.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_move": "differentiate Sbar_ord(q(Phi_s)); q(Phi_s) is constant along a vertical fibre, so the derivative is identically zero",
            "current_blocker": "neighbourhood quotient descent and ordinary-matter action signature remain unsigned",
            "source_anchor": "DZ1485_0_exact_neighbourhood_theorem; MPC1439_1_formal_zero",
            "zero_import_allowed": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "CXZ1911_2_material_link",
            "claim_piece": "material response channels are exactly the forbidden vertical slots",
            "formal_statement": "The 1910 law DeltaR_AB^X=sum_c Deltaf_c gamma_cX can create WEP residuals only if parent action contains a nonuniversal coefficient/generator gamma_cX visible to ordinary matter.",
            "proof_status": "EXACT_LINK_TO_1910_RESPONSE_LAW",
            "proof_move": "if the parent action has no such visible generator, gamma_cX has no domain and C_X is theorem-zero rather than small",
            "current_blocker": "no-hidden-visible-hom, source-label forgetting, common measure/current, and no spurion return are not jointly signed",
            "source_anchor": "MRF1910_3_sector_response_law; OG1451_6_verdict",
            "zero_import_allowed": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "CXZ1911_3_countermodels",
            "claim_piece": "why covariance alone cannot prove zero",
            "formal_statement": "Covariant actions of the form S_matter=sum_A w_A S_A, hidden f(X)F_Q^2, species Jacobians, or post-readout source selectors can preserve broad covariance while producing nonuniversal source response.",
            "proof_status": "COUNTERMODELS_SURVIVE",
            "proof_move": "these countermodels are legal unless parent object-language and descent premises explicitly remove their codomain",
            "current_blocker": "current corpus has not removed all countermodels",
            "source_anchor": "OG1451_5_countermodel; SLF1476_3_countermodel; SIGN1469_0_hidden_invariant",
            "zero_import_allowed": False,
            "valid_for_claim": False,
        },
        {
            "attempt_id": "CXZ1911_4_verdict",
            "claim_piece": "1911 coefficient-zero theorem verdict",
            "formal_statement": "The exact theorem is available conditionally: neighbourhood quotient descent kills all vertical nonuniversal material coefficients. Current evidence does not parent-sign the premises.",
            "proof_status": "ZERO_THEOREM_SHARP_NOT_PARENT_SIGNED",
            "proof_move": "do not import C_X=0; emit finite C_X contract and move the proof target to neighbourhood quotient descent",
            "current_blocker": "descent/no-hidden-hom/common-measure/readout premises unsigned",
            "source_anchor": "CXZ1911_0_target through CXZ1911_3_countermodels",
            "zero_import_allowed": False,
            "valid_for_claim": False,
        },
    ]


def premise_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "premise_id": "PREM1911_0_neighbourhood_descent",
            "needed_premise": "ordinary matter action descends through q_obs on an open neighbourhood",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "blocking_evidence": "DZ1485_5_verdict says proof sharpened not closed",
            "if_signed": "all vertical V_X material coefficients vanish on U",
            "source_anchor": "universal_matter_double_zero_attempt_nonclaim_1485.csv:DZ1485_5_verdict",
            "zero_import_allowed": False,
            "valid_for_claim": False,
        },
        {
            "premise_id": "PREM1911_1_no_source_only_slot",
            "needed_premise": "parent grammar has no Hom(hidden/source label, visible coefficient) slot",
            "current_status": "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED",
            "blocking_evidence": "AX1090 no-hidden-visible-hom and common measure/current remain unsigned",
            "if_signed": "w_A, f_X F^2, m_A(Xhat), and source multipliers lose legal domain",
            "source_anchor": "no_source_only_slot_operator_grammar_theorem_attempt_1451.csv:OG1451_6_verdict",
            "zero_import_allowed": False,
            "valid_for_claim": False,
        },
        {
            "premise_id": "PREM1911_2_source_label_forgetting",
            "needed_premise": "source functor forgets species/material labels after Hilbert variation",
            "current_status": "NOT_PARENT_DERIVED",
            "blocking_evidence": "source functor domain and readout no-reentry are unsigned",
            "if_signed": "relative material/source weights cannot be formed after variation",
            "source_anchor": "source_label_forgetting_proof_attempt_nonclaim_1476.csv:SLF1476_4_verdict",
            "zero_import_allowed": False,
            "valid_for_claim": False,
        },
        {
            "premise_id": "PREM1911_3_connected_matter_category",
            "needed_premise": "ordinary matter sectors form one parent-owned connected interaction category",
            "current_status": "CONDITIONAL_ONLY",
            "blocking_evidence": "connected graph parent signature and calibration silence are missing",
            "if_signed": "naturality collapses action-density/source weights to common mode",
            "source_anchor": "C_parent_WEP_connected_matter_category_signing_decision_1464.csv:SIGN1464_0_connected_matter_category",
            "zero_import_allowed": False,
            "valid_for_claim": False,
        },
        {
            "premise_id": "PREM1911_4_common_measure_current",
            "needed_premise": "single hbar/measure/current owner with species-blind Jacobian",
            "current_status": "REFUSE_COMMON_MEASURE_ZERO_IMPORT",
            "blocking_evidence": "parent measure owner, species Jacobian zero, current owner, and nonHilbert silence are unsigned",
            "if_signed": "pre-variation source weights and current rescalings reduce to common mode or zero",
            "source_anchor": "C_parent_WEP_common_measure_current_signature_decision_1462.csv:SIGN1462_0_common_measure_current",
            "zero_import_allowed": False,
            "valid_for_claim": False,
        },
        {
            "premise_id": "PREM1911_5_readout_order",
            "needed_premise": "variation-before-readout and no post-selector coefficient re-entry",
            "current_status": "REFUSE_READOUT_ORDER_ZERO_IMPORT",
            "blocking_evidence": "parent domain, variation order, and official readout model are not signed/imported",
            "if_signed": "readout/source selectors cannot create or hide C_X after variation",
            "source_anchor": "C_parent_WEP_readout_order_signing_decision_1454.csv:SIGN1454_0_readout_order",
            "zero_import_allowed": False,
            "valid_for_claim": False,
        },
        {
            "premise_id": "PREM1911_6_hidden_invariant_closure",
            "needed_premise": "no extra hidden invariants, shadow sectors, or discrete-sector spurion return",
            "current_status": "REFUSE_HIDDEN_ALGEBRA_PROMOTION",
            "blocking_evidence": "orbit transitivity/no-extra-invariant/discrete/radiative clauses are unsigned",
            "if_signed": "hidden variables cannot reintroduce nonuniversal material coefficients",
            "source_anchor": "C_parent_WEP_hidden_invariant_signing_decision_1469.csv:SIGN1469_0_hidden_invariant",
            "zero_import_allowed": False,
            "valid_for_claim": False,
        },
        {
            "premise_id": "PREM1911_7_unique_EM_owner",
            "needed_premise": "unique EM/F_Q^2 owner and no hidden representative EM branch",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "blocking_evidence": "unique parent EM owner, source label forgetting, and radiative closure remain missing",
            "if_signed": "EM/Coulomb material coefficient can be either parent-derived zero or a declared visible coupling",
            "source_anchor": "C_parent_WEP_EM_edge_signing_decision_1466.csv:SIGN1466_0_EM_edge",
            "zero_import_allowed": False,
            "valid_for_claim": False,
        },
    ]


def finite_cx_contract_rows() -> list[dict[str, Any]]:
    components = [
        ("CX1911_electron", "electron", "C_e := normalized parent derivative along electron rest-mass generator V_e"),
        ("CX1911_light_quark", "light_quark_or_nucleon_rest", "C_q := normalized parent derivative along light-quark/nucleon rest generator V_q"),
        ("CX1911_EM", "EM_Coulomb", "C_alpha := normalized parent derivative along EM/Coulomb binding generator V_alpha"),
        ("CX1911_nuclear", "nuclear_binding", "C_bind := normalized parent derivative along retained nuclear binding generator V_bind"),
        ("CX1911_QCD", "QCD_gluon", "C_QCD := normalized parent derivative along QCD residual generator V_Lambda"),
        ("CX1911_lattice", "lattice_impurity_coating", "C_lat := normalized parent derivative along lattice/chemical/coating generator V_lat"),
        ("CX1911_nonHilbert", "nonHilbert_readout_or_shadow", "C_shadow := coefficient for any non-Hilbert/readout/shadow re-entry channel"),
    ]
    rows: list[dict[str, Any]] = []
    for coefficient_id, component, definition in components:
        rows.append(
            {
                "coefficient_id": coefficient_id,
                "component": component,
                "definition": definition,
                "accepted_forms": "DERIVED_ZERO with parent proof; finite numeric/source-backed value with units and prior; or retained nuisance clearly labelled nonclaim",
                "forbidden_forms": "MICROSCOPE bound inversion; alloy proxy normalization; DD smoke coefficient import without basis map; tau=1 absorption",
                "current_value": "MISSING_PARENT_COEFFICIENT",
                "units": "dimensionless in declared parent WEP basis unless parent action gives units",
                "required_source_or_proof": "parent action functional derivative, theorem-zero certificate, or explicit finite coefficient source independent of the WEP bound",
                "matching_tensor_row": f"component={component}",
                "status": "FINITE_CX_CONTRACT_ONLY_NOT_FILLED",
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def zero_import_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "ZIT1911_0_all_premises_signed",
            "neighbourhood_descent": True,
            "no_source_slot": True,
            "source_label_forgetting": True,
            "common_measure_current": True,
            "readout_order": True,
            "hidden_invariant_closure": True,
            "expected_status": "WOULD_ACCEPT_THEOREM_ZERO_IMPORT",
            "actual_current_status": "HYPOTHETICAL_ONLY_NOT_CURRENT_CORPUS",
            "valid_for_claim": False,
        },
        {
            "case_id": "ZIT1911_1_current_corpus",
            "neighbourhood_descent": False,
            "no_source_slot": False,
            "source_label_forgetting": False,
            "common_measure_current": False,
            "readout_order": False,
            "hidden_invariant_closure": False,
            "expected_status": "REFUSE_ZERO_IMPORT_USE_FINITE_CX_CONTRACT",
            "actual_current_status": "MATCHES_CURRENT_CORPUS",
            "valid_for_claim": False,
        },
        {
            "case_id": "ZIT1911_2_covariance_only",
            "neighbourhood_descent": False,
            "no_source_slot": False,
            "source_label_forgetting": False,
            "common_measure_current": False,
            "readout_order": True,
            "hidden_invariant_closure": False,
            "expected_status": "REFUSE_COVARIANCE_ONLY_COUNTERMODELS_SURVIVE",
            "actual_current_status": "ANTI_SHORTCUT_GUARD",
            "valid_for_claim": False,
        },
        {
            "case_id": "ZIT1911_3_bound_or_proxy_as_coefficient",
            "neighbourhood_descent": False,
            "no_source_slot": False,
            "source_label_forgetting": False,
            "common_measure_current": False,
            "readout_order": False,
            "hidden_invariant_closure": False,
            "expected_status": "REFUSE_BOUND_PROXY_COEFFICIENT_IMPORT",
            "actual_current_status": "ANTI_SHORTCUT_GUARD",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1911_0_exact_theorem",
            "condition": "descent theorem proving C_X=0 is mathematically exact",
            "current_status": "PASS_CONDITIONAL_THEOREM_ONLY",
            "source_anchor": "CXZ1911_1_descent_theorem",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1911_1_parent_premises",
            "condition": "all zero-theorem premises are parent-signed together",
            "current_status": "FAIL_PREMISES_UNSIGNED",
            "source_anchor": OUTPUTS["premise_matrix"].name,
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1911_2_finite_contract",
            "condition": "finite C_X rows are filled if zero theorem fails",
            "current_status": "FAIL_FINITE_CX_CONTRACT_UNFILLED",
            "source_anchor": OUTPUTS["finite_cx_contract"].name,
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1911_3_claim",
            "condition": "1911 supports WEP/local-GR material coefficient claim",
            "current_status": "CLAIM_BLOCKED",
            "source_anchor": "CG1911_0_exact_theorem through CG1911_2_finite_contract",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1911_0_keep",
            "decision": "keep coefficient-zero theorem as primary derivation route",
            "reason": "neighbourhood quotient descent would kill all vertical nonuniversal material coefficients exactly",
            "status": "THEOREM_ROUTE_SHARPENED",
            "next_dependency": "parent-sign descent/signature premises",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1911_1_refuse",
            "decision": "do not import C_X=0 yet",
            "reason": "countermodels survive unless no-source-slot/source-label/common-measure/readout/hidden-invariant clauses are signed together",
            "status": "ZERO_IMPORT_REFUSED",
            "next_dependency": "1912 neighbourhood quotient descent proof",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1911_2_contract",
            "decision": "stage finite C_X contract as fallback",
            "reason": "if the local-GR zero theorem fails, a finite coefficient branch must be explicit and nonclaim",
            "status": "FINITE_CX_CONTRACT_STAGED_NONCLAIM",
            "next_dependency": "source independent finite coefficients or theorem-zero rows",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1911_0_primary",
            "selection_status": "selected",
            "target_doc": "1912-Y5-R2FR-neighbourhood-quotient-descent-signature-proof-or-axiom-ledger.md",
            "target_script": "scripts/Y5_R2FR_neighbourhood_quotient_descent_signature_proof_or_axiom_ledger_1912.py",
            "objective": "try to parent-sign ordinary-matter neighbourhood quotient descent and action signature; if it fails, isolate the minimal axiom/debt ledger",
            "success_condition": "signed descent theorem closing C_X=0, or exact minimal missing-axiom ledger with no EEP smuggling",
            "do_not": "do not adopt metric universality/EEP as an axiom and call it derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT1911_0_gain",
            "area": "local GR route",
            "summary": "the nonuniversal C_X zero theorem is now exact conditionally: neighbourhood quotient descent kills vertical material coefficients",
            "risk_level": "HIGH_VALUE_CONDITIONAL_THEOREM",
            "project_meaning": "this is the cleanest derivation path to GR-like local universality",
            "next_action": "prove descent/signature premises",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT1911_1_block",
            "area": "proof debt",
            "summary": "the missing item is now sharply named: ordinary-matter neighbourhood quotient descent plus no-hidden source/measure/readout re-entry",
            "risk_level": "CENTRAL_PREMISE_UNSIGNED",
            "project_meaning": "the coupling problem has collapsed to a precise parent-action signature problem",
            "next_action": "1912 descent proof or axiom ledger",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT1911_2_fallback",
            "area": "finite coefficient branch",
            "summary": "if zero theorem cannot be derived, finite C_X rows must be sourced independently and remain nonclaim until tested",
            "risk_level": "FALLBACK_READY_NONCLAIM",
            "project_meaning": "no silent retreat into proxy fitting or bound inversion",
            "next_action": "keep finite C_X contract staged",
            "valid_for_claim": False,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "zero_theorem": zero_theorem_rows(),
        "premise_matrix": premise_matrix_rows(),
        "finite_cx_contract": finite_cx_contract_rows(),
        "zero_import_tests": zero_import_test_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def copy_branch_artifacts() -> None:
    for key, target in BRANCH_COPIES.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUTPUTS[key], target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        try:
            rows = csv_rows(path)
            if not rows:
                bad.append(f"{path.name}:empty")
        except Exception as exc:
            bad.append(f"{path.name}:{exc}")
    return not bad, "; ".join(bad) if bad else f"parsed {len(paths)} csv files"


def claim_flags_safe(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in [
                "valid_for_claim",
                "claim_allowed",
                "valid_prediction_row",
                "score_ready",
                "gate_pass",
                "zero_import_allowed",
            ]:
                if field in row and bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all claim/zero-import flags remain false"


def zero_theorem_valid(rows: list[dict[str, str]]) -> tuple[bool, str]:
    required = {
        "CXZ1911_1_descent_theorem": "EXACT_CONDITIONAL_THEOREM",
        "CXZ1911_3_countermodels": "COUNTERMODELS_SURVIVE",
        "CXZ1911_4_verdict": "ZERO_THEOREM_SHARP_NOT_PARENT_SIGNED",
    }
    bad = []
    row_by_id = {row["attempt_id"]: row for row in rows}
    for row_id, status in required.items():
        if row_id not in row_by_id:
            bad.append(f"{row_id}:missing")
        elif row_by_id[row_id]["proof_status"] != status:
            bad.append(f"{row_id}:{row_by_id[row_id]['proof_status']}")
    return not bad, "; ".join(bad) if bad else "zero theorem is exact conditional, countermodels retained, verdict blocked"


def premise_matrix_valid(rows: list[dict[str, str]]) -> tuple[bool, str]:
    bad = []
    if len(rows) < 8:
        bad.append(f"too_few_rows={len(rows)}")
    if any(bool_string(row["zero_import_allowed"]) == "true" for row in rows):
        bad.append("zero_import_allowed_true")
    if not any(row["premise_id"] == "PREM1911_0_neighbourhood_descent" for row in rows):
        bad.append("missing_neighbourhood_descent")
    return not bad, "; ".join(bad) if bad else "all zero-theorem premises tracked and zero import refused"


def finite_contract_valid(rows: list[dict[str, str]]) -> tuple[bool, str]:
    required = {"electron", "light_quark_or_nucleon_rest", "EM_Coulomb", "nuclear_binding", "QCD_gluon", "lattice_impurity_coating", "nonHilbert_readout_or_shadow"}
    present = {row["component"] for row in rows}
    bad = []
    missing = required - present
    if missing:
        bad.append(f"missing={sorted(missing)}")
    for row in rows:
        if row["current_value"] != "MISSING_PARENT_COEFFICIENT":
            bad.append(f"{row['coefficient_id']}:unexpected_value")
        if bool_string(row["score_ready"]) == "true" or bool_string(row["claim_allowed"]) == "true":
            bad.append(f"{row['coefficient_id']}:claim_flag_true")
    return not bad, "; ".join(bad) if bad else "finite C_X contract components present and unfilled"


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []
    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append(
        {
            "validation_id": "VAL1911_00_sources",
            "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL",
            "detail": "all local source paths exist and needles found",
            "valid_for_claim": False,
        }
    )
    zero_ok, zero_detail = zero_theorem_valid(csv_rows(OUTPUTS["zero_theorem"]))
    checks.append({"validation_id": "VAL1911_01_zero_theorem", "status": "PASS" if zero_ok else "FAIL", "detail": zero_detail, "valid_for_claim": False})
    premise_ok, premise_detail = premise_matrix_valid(csv_rows(OUTPUTS["premise_matrix"]))
    checks.append({"validation_id": "VAL1911_02_premise_matrix", "status": "PASS" if premise_ok else "FAIL", "detail": premise_detail, "valid_for_claim": False})
    contract_ok, contract_detail = finite_contract_valid(csv_rows(OUTPUTS["finite_cx_contract"]))
    checks.append({"validation_id": "VAL1911_03_finite_cx_contract", "status": "PASS" if contract_ok else "FAIL", "detail": contract_detail, "valid_for_claim": False})
    tests = csv_rows(OUTPUTS["zero_import_tests"])
    checks.append(
        {
            "validation_id": "VAL1911_04_zero_import_tests",
            "status": "PASS" if any(row["case_id"] == "ZIT1911_1_current_corpus" and row["expected_status"] == "REFUSE_ZERO_IMPORT_USE_FINITE_CX_CONTRACT" for row in tests) else "FAIL",
            "detail": "current corpus zero import is refused",
            "valid_for_claim": False,
        }
    )
    gates = csv_rows(OUTPUTS["claim_gate"])
    checks.append(
        {
            "validation_id": "VAL1911_05_claim_gate",
            "status": "PASS" if any(row["gate_id"] == "CG1911_3_claim" and row["current_status"] == "CLAIM_BLOCKED" for row in gates) else "FAIL",
            "detail": "claim remains blocked",
            "valid_for_claim": False,
        }
    )
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append(
        {
            "validation_id": "VAL1911_06_next_target",
            "status": "PASS" if any(row["route_id"] == "NEXT1911_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL",
            "detail": "1912 neighbourhood quotient descent route selected",
            "valid_for_claim": False,
        }
    )
    flags_ok, flags_detail = claim_flags_safe(generated_without_validation)
    checks.append({"validation_id": "VAL1911_07_claim_flags_safe", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1911_08_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})
    checks.append({"validation_id": "VAL1911_09_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1911_10_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})
    formalization_hits = []
    if FORMALIZATION.exists():
        artifact_needles = [
            "1911-Y5-R2FR-nonuniversal-material",
            "P8_Y5_PARENT_QLOC_1911",
            "Y5_R2FR_nonuniversal_material_coefficient_zero_theorem_or_finite_CX_contract_1911",
        ]
        formalization_hits = [
            path
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and any(needle in path.name for needle in artifact_needles)
        ]
    checks.append({"validation_id": "VAL1911_11_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1911_artifact_count={len(formalization_hits)}", "valid_for_claim": False})
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1911_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1911 nonuniversal material coefficient zero theorem or finite C_X contract", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1911 - Nonuniversal Material Coefficient Zero Theorem Or Finite C_X Contract

## Purpose

This checkpoint tries the derivation-first route demanded by the local-GR programme: prove that all nonuniversal material coefficients `C_X` vanish before WEP readout. It succeeds as an exact conditional theorem but not as a parent-signed theorem. The fallback finite-`C_X` contract is therefore staged without claim promotion.

## Result

- The zero theorem is now exact in form: neighbourhood quotient descent of ordinary matter implies `C_X=0` for vertical nonuniversal material directions.
- The theorem is not parent-signed because no-source-slot, source-label forgetting, common measure/current, readout order, hidden-invariant closure, and unique EM owner are still unsigned together.
- The current corpus must refuse `C_X=0` import.
- A finite `C_X` contract is staged for every nonuniversal material channel if the zero theorem fails.
- Next target is the real bottleneck: parent-sign neighbourhood quotient descent, or isolate the minimal axiom/debt ledger.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Coefficient Zero Theorem Attempt

{markdown_table(rows_by_name["zero_theorem"])}

## Zero-Theorem Premise Matrix

{markdown_table(rows_by_name["premise_matrix"])}

## Finite C_X Contract

{markdown_table(rows_by_name["finite_cx_contract"])}

## Zero-Import Refusal Tests

{markdown_table(rows_by_name["zero_import_tests"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()

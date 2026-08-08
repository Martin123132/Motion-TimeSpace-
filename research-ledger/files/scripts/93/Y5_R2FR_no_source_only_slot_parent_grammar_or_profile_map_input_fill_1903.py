from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1903"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1903-Y5-R2FR-no-source-only-slot-parent-grammar-or-profile-map-input-fill.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1902_doc": ROOT / "1902-Y5-R2FR-source-label-forgetting-before-GM-calibration-or-profile-source-vector-map.md",
    "1902_validation": OUT / "P8_Y5_BRR545_1902_VALIDATION.csv",
    "1902_label": OUT / "P8_Y5_PARENT_QLOC_1902_SOURCE_LABEL_FORGETTING_BEFORE_GM_ATTEMPT.csv",
    "1902_no_slot_gate": OUT / "P8_Y5_PARENT_QLOC_1902_NO_SOURCE_SLOT_GATE.csv",
    "1902_profile_map": OUT / "P8_Y5_PARENT_QLOC_1902_PROFILE_SOURCE_VECTOR_MAP_NONCLAIM.csv",
    "1902_next": OUT / "P8_Y5_PARENT_QLOC_1902_NEXT_TARGET.csv",
    "1886_no_source_slot": OUT / "P8_Y5_PARENT_QLOC_1886_NO_SOURCE_ONLY_SLOT_PROOF_AUDIT.csv",
    "1887_object_language": OUT / "P8_Y5_PARENT_QLOC_1887_OBJECT_LANGUAGE_TYPING_PROOF_AUDIT.csv",
    "1887_action_scale": OUT / "P8_Y5_PARENT_QLOC_1887_ACTION_SCALE_NORMALIZATION_AUDIT.csv",
    "1895_prefactor_attempt": OUT / "P8_Y5_PARENT_QLOC_1895_NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_ATTEMPT.csv",
    "1895_typing_gate": OUT / "P8_Y5_PARENT_QLOC_1895_SOURCE_PREFACTOR_TYPING_GATE.csv",
    "1896_nohom_attempt": OUT / "P8_Y5_PARENT_QLOC_1896_PARENT_SORT_DISJOINTNESS_NOHOM_ATTEMPT.csv",
    "1896_nohom_gate": OUT / "P8_Y5_PARENT_QLOC_1896_NOHOM_GATE.csv",
    "1236_certificate": OUT / "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
    "1114_no_hidden_visible": OUT / "P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv",
    "1107_exhaustion": OUT / "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv",
    "1092_invariant_triviality": OUT / "P8_Y5_R10_1092_HIDDEN_INVARIANT_TRIVIALITY_ATTEMPT.csv",
    "1051_scalar_obstruction": OUT / "P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv",
    "1899_wep_input_pack": OUT / "P8_Y5_PARENT_QLOC_1899_WEP_INPUT_PACK_NONCLAIM.csv",
    "1900_point_source": OUT / "P8_Y5_PARENT_QLOC_1900_WEP_POINT_SOURCE_RESIDUAL_LEDGER_NONCLAIM.csv",
    "1900_official_data": OUT / "P8_Y5_PARENT_QLOC_1900_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv",
    "1901_gm_guard": OUT / "P8_Y5_PARENT_QLOC_1901_COMMON_MODE_ABSORPTION_ALGEBRA.csv",
    "1901_source_vector": OUT / "P8_Y5_PARENT_QLOC_1901_SOURCE_VECTOR_FILL_NONCLAIM.csv",
    "1084_profile_kernel": OUT / "P8_Y5_R10_1084_SOURCE_PROFILE_KERNEL_DERIVATION_LEDGER.csv",
    "1084_profile_gates": OUT / "P8_Y5_R10_1084_PROFILE_CLOSURE_GATES.csv",
    "1083_caveat": OUT / "P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv",
    "1424_source_contract": OUT / "P8_Y5_R10_1424_SOURCE_VECTOR_CONTRACT.csv",
}


SOURCE_NEEDLES = {
    "1902_doc": ["NEXT_TARGET_SELECTED", "1903-Y5-R2FR-no-source-only-slot-parent-grammar-or-profile-map-input-fill.md"],
    "1902_validation": ["VAL1902_OVERALL,PASS"],
    "1902_label": ["SLG1902_6_verdict", "SOURCE_LABEL_FORGETTING_BEFORE_GM_NOT_PARENT_DERIVED"],
    "1902_no_slot_gate": ["NSG1902_5_verdict", "SOURCE_LABEL_FORGETTING_CLAIM_BLOCKED"],
    "1902_profile_map": ["PSM1902_6_verdict", "PROFILE_SOURCE_VECTOR_MAP_NOT_EXECUTABLE_NONCLAIM"],
    "1902_next": ["NEXT1902_0_primary", "no-source-only slot/no-Hom parent grammar"],
    "1886_no_source_slot": ["NSS1886_7_verdict", "NO_SOURCE_ONLY_SLOT_NOT_PARENT_DERIVED"],
    "1887_object_language": ["OLT1887_9_verdict", "OBJECT_LANGUAGE_TYPING_NOT_PARENT_DERIVED"],
    "1887_action_scale": ["ASN1887_5_verdict", "ACTION_SCALE_OWNER_UNSIGNED"],
    "1895_prefactor_attempt": ["NSP1895_5_verdict", "NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_PROOF_NOT_PARENT_DERIVED"],
    "1895_typing_gate": ["TYP1895_5_verdict", "NO_SOURCE_PREFACTOR_TYPING_CLAIM_BLOCKED"],
    "1896_nohom_attempt": ["NH1896_5_verdict", "PARENT_SORT_DISJOINTNESS_NOHOM_NOT_DERIVED"],
    "1896_nohom_gate": ["NHG1896_4_verdict", "NOHOM_CLAIM_BLOCKED"],
    "1236_certificate": ["CERT1236_6_current_verdict", "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED"],
    "1114_no_hidden_visible": ["NHV1114_6_verdict", "NO_HIDDEN_VISIBLE_MORPHISM_NOT_DERIVED"],
    "1107_exhaustion": ["EXH1107_6_verdict", "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED"],
    "1092_invariant_triviality": ["HIT1092_5_verdict", "TRIVIALITY_NOT_DERIVED"],
    "1051_scalar_obstruction": ["ISO1051_3_domain_marker", "LIVE_LABEL_OBSTRUCTION"],
    "1899_wep_input_pack": ["WIP1899_8_verdict", "WEP_INPUT_PACK_NOT_EXECUTABLE_NONCLAIM"],
    "1900_point_source": ["PSE1900_6_verdict", "POINT_SOURCE_RESIDUAL_PACK_NOT_EXECUTABLE_NONCLAIM"],
    "1900_official_data": ["OFFICIAL_DATA_TARGET_NOT_ACQUIRED_NONCLAIM", "SURROGATE_DESIGN_MATRIX_NOT_OFFICIAL"],
    "1901_gm_guard": ["ALG1901_3_claim_limit", "NO_CLAIM_PROMOTION"],
    "1901_source_vector": ["SVF1901_6_verdict", "SOURCE_VECTOR_NOT_EXECUTABLE_NONCLAIM"],
    "1084_profile_kernel": ["K1084_1_effective_source_charge", "FINITE_RANGE_PROFILE_DEPENDENCY_RETAINED"],
    "1084_profile_gates": ["PCG1084_2_source_charge_basis", "PARENT_TO_DD_MAP_NOT_DERIVED"],
    "1083_caveat": ["SCG1083_0_profile_weighting", "MISSING_SOURCE_PROFILE_WEIGHTING"],
    "1424_source_contract": ["SRCMAP1424_0_R_source", "MISSING_SOURCE_VECTOR"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1903_SOURCE_REGISTER.csv",
    "grammar_attempt": OUT / "P8_Y5_PARENT_QLOC_1903_NO_SOURCE_ONLY_SLOT_PARENT_GRAMMAR_ATTEMPT.csv",
    "constructor_gate": OUT / "P8_Y5_PARENT_QLOC_1903_NOHOM_CONSTRUCTOR_GATE.csv",
    "profile_fill": OUT / "P8_Y5_PARENT_QLOC_1903_PROFILE_MAP_INPUT_FILL_NONCLAIM.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1903_GRAMMAR_PROFILE_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1903_GRAMMAR_PROFILE_DRYRUN_RESULTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1903_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1903_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1903_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1903_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1903_VALIDATION.csv",
}


BRANCH_COPIES = {
    "grammar_attempt": MICROSCOPE_RESIDUALS / OUTPUTS["grammar_attempt"].name,
    "profile_fill": SOURCE_WEIGHT_DOCS / "PROFILE_MAP_INPUT_FILL_1903_NONCLAIM.csv",
    "constructor_gate": QUEUE / "JR1903_NOHOM_CONSTRUCTOR_GATE_NONCLAIM.csv",
    "dryrun_results": QUARANTINE / OUTPUTS["dryrun_results"].name,
}


def ensure_dirs() -> None:
    for path in [OUT, MICROSCOPE_RESIDUALS, QUEUE, SOURCE_WEIGHT_DOCS, QUARANTINE]:
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


def grammar_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "NSG1903_0_target",
            "claim_piece": "no-source-only slot parent grammar",
            "formal_statement": "Before variation the parent grammar has no constructor w_A:S_A->source strength and no Hom_parent(SpeciesLabel,Coeff_active_source).",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "this is the exact theorem needed for source universality without tuning: w_A is not small, it is unformable",
            "source_anchor": "P8_Y5_PARENT_QLOC_1902_NEXT_TARGET.csv:NEXT1902_0_primary",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "NSG1903_1_inside_typed_grammar",
            "claim_piece": "typed grammar proof",
            "formal_statement": "Given derived disjoint sorts and Arg(Coeff_active_source) subset Q_obs x Theta_rep x UniversalCalibration x RetainedResidual, SpeciesLabel has no target slot.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "inside the grammar the proof is immediate: a term with no constructor and no target sort is not a legal parent term",
            "source_anchor": "P8_Y5_PARENT_QLOC_1896_PARENT_SORT_DISJOINTNESS_NOHOM_ATTEMPT.csv:NH1896_1_conditional_typed_proof; P8_Y5_PARENT_QLOC_1895_NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_ATTEMPT.csv:NSP1895_1_exact_if_typed",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "NSG1903_2_source_functor_order",
            "claim_piece": "variation-before-readout source functor",
            "formal_statement": "S_matter is varied as one total object before source/readout projection, so q_src returns T_total rather than labelled pairs {(T_A,A)}.",
            "status": "EXACT_IF_SOURCE_FUNCTOR_PARENT_SIGNED",
            "proof_or_obstruction": "this would make 1901 measured-G absorption safe because only one universal scalar reaches calibration",
            "source_anchor": "P8_Y5_PARENT_QLOC_1902_SOURCE_LABEL_FORGETTING_BEFORE_GM_ATTEMPT.csv:SLG1902_1_label_forgotten_uniqueness; P8_Y5_PARENT_QLOC_1895_SOURCE_PREFACTOR_TYPING_GATE.csv:TYP1895_2_total_variation_order",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "NSG1903_3_parent_generator_gap",
            "claim_piece": "parent-generated constructor list",
            "formal_statement": "Every ordinary-sector coefficient is generated by ParentGenerate[q(Phi),theta_rep,topological level] and no extra source-only coefficient algebra exists.",
            "status": "CONSTRUCTOR_EXHAUSTION_NOT_DERIVED",
            "proof_or_obstruction": "the chain-rule/no-Hom proof works after membership in Image(ParentGenerate), but membership is still not derived from motion/time/space primitives",
            "source_anchor": "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv:EXH1107_6_verdict; P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv:CERT1236_6_current_verdict",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "NSG1903_4_countermodel",
            "claim_piece": "direct-sum and hidden-marker countermodels",
            "formal_statement": "Disconnected ordinary sectors, surviving hidden invariant scalars, material markers, or readout labels can still define c_A or w_A unless parent grammar forbids them.",
            "status": "COUNTERMODELS_RETAINED",
            "proof_or_obstruction": "covariance, gauge invariance, and naturality do not by themselves erase legal scalar or species-family coefficient maps",
            "source_anchor": "P8_Y5_PARENT_QLOC_1887_OBJECT_LANGUAGE_TYPING_PROOF_AUDIT.csv:OLT1887_3_direct_sum_counterexample; P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv:ISO1051_3_domain_marker",
            "conditional_theorem": False,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "NSG1903_5_action_measure_gap",
            "claim_piece": "one action scale / hbar / measure owner",
            "formal_statement": "Relative action weights must be quotient gauge, forbidden terms, or retained finite residuals; classical EOM rescaling cannot be used as proof.",
            "status": "ACTION_SCALE_MEASURE_OWNER_UNSIGNED",
            "proof_or_obstruction": "w_A can leave matter equations looking ordinary while changing the Hilbert/coframe source, so one action-scale owner is essential",
            "source_anchor": "P8_Y5_PARENT_QLOC_1887_ACTION_SCALE_NORMALIZATION_AUDIT.csv:ASN1887_1_classical_eom_false_positive;ASN1887_5_verdict",
            "conditional_theorem": False,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "NSG1903_6_readout_radiative_gap",
            "claim_piece": "readout/radiative stability",
            "formal_statement": "Loops, effective reduction, clocks, source-worldtube maps, and local projections preserve the same source coefficient domain.",
            "status": "READOUT_RADIATIVE_STABILITY_UNSIGNED",
            "proof_or_obstruction": "a tree-level no-slot theorem would still fail claim-grade status if readout or matching regenerates source coefficients",
            "source_anchor": "P8_Y5_PARENT_QLOC_1895_SOURCE_PREFACTOR_TYPING_GATE.csv:TYP1895_4_radiative_readout; P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv:NHV1114_5_radiative_readout",
            "conditional_theorem": False,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "NSG1903_7_verdict",
            "claim_piece": "promote no-source-only slot theorem",
            "formal_statement": "Current MTS parent primitives derive that source-only species weights are ungrammatical before variation.",
            "status": "NO_SOURCE_ONLY_SLOT_PARENT_GRAMMAR_NOT_DERIVED",
            "proof_or_obstruction": "the typed/no-Hom theorem is exact conditionally, but parent constructor exhaustion, action-scale owner, no-marker/no-hidden scalar closure, and readout/radiative stability are not all signed",
            "source_anchor": "NSG1903_0_target through NSG1903_6_readout_radiative_gap",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def constructor_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "NHG1903_0_parent_sorts", "required_clause": "disjoint parent sorts derived from MTS primitives", "current_status": "FAIL_SCHEMA_WRITTEN_NOT_DERIVED", "if_pass": "source coefficient membership becomes checkable", "if_fail": "grammar is a closure contract", "source_anchor": "P8_Y5_PARENT_QLOC_1895_SOURCE_PREFACTOR_TYPING_GATE.csv:TYP1895_0_parent_sorts", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "NHG1903_1_nohom", "required_clause": "Hom(SpeciesLabel,Coeff_active_source)=empty", "current_status": "FAIL_EXACT_CONDITIONAL_NOT_PARENT_SIGNED", "if_pass": "w_A has no legal target sort", "if_fail": "relative source-weight countermodel survives", "source_anchor": "P8_Y5_PARENT_QLOC_1896_NOHOM_GATE.csv:NHG1896_4_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "NHG1903_2_constructor_exhaustion", "required_clause": "all ordinary-sector coefficients lie in Image(ParentGenerate)", "current_status": "FAIL_OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED", "if_pass": "hidden/source labels cannot target coefficient spaces", "if_fail": "extra local counterterm algebra remains legal", "source_anchor": "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv:EXH1107_6_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "NHG1903_3_no_marker_scalar", "required_clause": "no hidden invariant or marker can be retyped as source coefficient data", "current_status": "FAIL_SCALAR_LABEL_OBSTRUCTION_LIVE", "if_pass": "domain/material/readout markers cannot sneak w_A back in", "if_fail": "finite source-vector/material tensor route remains required", "source_anchor": "P8_Y5_R10_1092_HIDDEN_INVARIANT_TRIVIALITY_ATTEMPT.csv:HIT1092_5_verdict; P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv:ISO1051_3_domain_marker", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "NHG1903_4_action_scale", "required_clause": "one action-scale/hbar/measure owner for ordinary sectors", "current_status": "FAIL_ACTION_SCALE_OWNER_UNSIGNED", "if_pass": "classical EOM false positive is removed", "if_fail": "w_A can alter Hilbert source while matter EOM look normal", "source_anchor": "P8_Y5_PARENT_QLOC_1887_ACTION_SCALE_NORMALIZATION_AUDIT.csv:ASN1887_5_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "NHG1903_5_readout", "required_clause": "readout/radiative maps preserve no-source-only domain", "current_status": "FAIL_READOUT_RADIATIVE_UNSIGNED", "if_pass": "tree-level no-slot proof reaches observations", "if_fail": "source-worldtube/readout residuals remain finite", "source_anchor": "P8_Y5_PARENT_QLOC_1895_SOURCE_PREFACTOR_TYPING_GATE.csv:TYP1895_4_radiative_readout", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "NHG1903_6_verdict", "required_clause": "no-source-only slot/no-Hom theorem is parent-signed", "current_status": "NO_SOURCE_ONLY_SLOT_CLAIM_BLOCKED", "if_pass": "relative source weights become theorem-zero after common calibration", "if_fail": "profile/source-vector fallback remains the disciplined path", "source_anchor": "NHG1903_0_parent_sorts through NHG1903_5_readout", "gate_pass": False, "valid_for_claim": False},
    ]


def profile_fill_rows() -> list[dict[str, Any]]:
    return [
        {"fill_id": "PF1903_0_bound_anchor", "object": "MICROSCOPE eta bound anchor", "current_value": "eta(Pt,Ti)=(-1.5 +/- 2.3)e-15; local bound claims row R1_WEP_source_charge uses 2.8e-15", "current_status": "SOURCE_PDF_CACHED_BOUND_ANCHOR_ONLY", "missing_for_claim": "prediction-side source/material/readout map", "source_anchor": "P8_Y5_PARENT_QLOC_1899_WEP_INPUT_PACK_NONCLAIM.csv:WIP1899_0_bound_anchor", "units": "dimensionless eta", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"fill_id": "PF1903_1_lambda_owner", "object": "lambda_WEP / range owner", "current_value": "MISSING", "current_status": "MISSING_PARENT_RANGE_OWNER", "missing_for_claim": "derive carrier/range from parent residual sector or declare retained nuisance with sourced prior", "source_anchor": "P8_Y5_R10_1084_SOURCE_PROFILE_KERNEL_DERIVATION_LEDGER.csv:K1084_2_long_range_limit", "units": "m or lambda/R_E", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"fill_id": "PF1903_2_earth_profile", "object": "Earth source worldtube density/composition profile", "current_value": "MISSING", "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING", "missing_for_claim": "source-backed rho(r), composition shells, and same-frame worldtube convention", "source_anchor": "P8_Y5_PARENT_QLOC_1899_WEP_INPUT_PACK_NONCLAIM.csv:WIP1899_1_source_worldtube_profile;WIP1899_2_source_composition", "units": "kg m^-3 or normalized shell fractions", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"fill_id": "PF1903_3_parent_basis_map", "object": "MTS parent residual vector -> DD/source basis", "current_value": "MISSING", "current_status": "MISSING_PARENT_OPERATOR_BASIS_MAP", "missing_for_claim": "linear map from parent residual coefficients to source/material response basis", "source_anchor": "P8_Y5_R10_1084_PROFILE_CLOSURE_GATES.csv:PCG1084_2_source_charge_basis; P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv:SCG1083_1_parent_to_DD_map", "units": "dimensionless response matrix", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"fill_id": "PF1903_4_material_response", "object": "PtRh10 minus TA6V test-body response tensor", "current_value": "MISSING", "current_status": "MISSING_FULL_MATERIAL_TENSOR", "missing_for_claim": "material response tensor in same residual/source basis", "source_anchor": "P8_Y5_PARENT_QLOC_1899_WEP_INPUT_PACK_NONCLAIM.csv:WIP1899_3_material_tensor", "units": "dimensionless sensitivities", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"fill_id": "PF1903_5_readout_arrays", "object": "official MICROSCOPE CMSM/readout arrays", "current_value": "not acquired; local metadata/surrogate exist only", "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED", "missing_for_claim": "official arrays or validated equivalent with masks, orbit, attitude, calibration flags", "source_anchor": "P8_Y5_PARENT_QLOC_1900_OFFICIAL_READOUT_DATA_TARGETS_NONCLAIM.csv:cmsm_ds_onera_root; P8_Y5_PARENT_QLOC_1900_WEP_POINT_SOURCE_RESIDUAL_LEDGER_NONCLAIM.csv:PSE1900_5_kernel_nullspace", "units": "time/frame/readout kernel units", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"fill_id": "PF1903_6_measured_G_guard", "object": "no measured-G hiding certificate", "current_value": "common scalar only; relative/source-profile residual remains explicit", "current_status": "GUARD_DERIVED_NONCLAIM", "missing_for_claim": "source-label theorem-zero or executable finite source-vector row", "source_anchor": "P8_Y5_PARENT_QLOC_1901_COMMON_MODE_ABSORPTION_ALGEBRA.csv:ALG1901_3_claim_limit; P8_Y5_PARENT_QLOC_1901_SOURCE_VECTOR_FILL_NONCLAIM.csv:SVF1901_5_absorption_guard", "units": "calibration policy / dimensionless residual", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"fill_id": "PF1903_7_verdict", "object": "profile-map input fill", "current_value": "NONCLAIM_LEDGER_ONLY", "current_status": "PROFILE_MAP_INPUTS_NOT_SCORE_READY", "missing_for_claim": "PF1903_1 through PF1903_5 filled or theorem-zero, plus parent residual coefficients", "source_anchor": "PF1903_0_bound_anchor through PF1903_6_measured_G_guard", "units": "mixed", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY1903_0_nohom_unsigned", "typed_grammar_signed": False, "constructor_exhausted": False, "action_scale_owned": False, "readout_stable": False, "profile_inputs_filled": False, "uses_closure_as_claim": False, "expected_status": "REFUSED_NO_SOURCE_ONLY_SLOT_NOT_PARENT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY1903_1_constructor_missing", "typed_grammar_signed": True, "constructor_exhausted": False, "action_scale_owned": False, "readout_stable": False, "profile_inputs_filled": False, "uses_closure_as_claim": False, "expected_status": "REFUSED_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY1903_2_action_scale_missing", "typed_grammar_signed": True, "constructor_exhausted": True, "action_scale_owned": False, "readout_stable": False, "profile_inputs_filled": False, "uses_closure_as_claim": False, "expected_status": "REFUSED_ACTION_SCALE_OWNER_UNSIGNED", "valid_for_claim": False},
        {"case_id": "DRY1903_3_readout_missing", "typed_grammar_signed": True, "constructor_exhausted": True, "action_scale_owned": True, "readout_stable": False, "profile_inputs_filled": False, "uses_closure_as_claim": False, "expected_status": "REFUSED_READOUT_RADIATIVE_STABILITY_UNSIGNED", "valid_for_claim": False},
        {"case_id": "DRY1903_4_closure_as_claim", "typed_grammar_signed": False, "constructor_exhausted": False, "action_scale_owned": False, "readout_stable": False, "profile_inputs_filled": False, "uses_closure_as_claim": True, "expected_status": "REFUSED_CLOSURE_NOT_CLAIM", "valid_for_claim": False},
        {"case_id": "DRY1903_5_profile_missing", "typed_grammar_signed": False, "constructor_exhausted": False, "action_scale_owned": False, "readout_stable": False, "profile_inputs_filled": False, "uses_closure_as_claim": False, "expected_status": "REFUSED_NO_SOURCE_ONLY_SLOT_NOT_PARENT_DERIVED", "valid_for_claim": False},
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    if bool_string(row["uses_closure_as_claim"]) == "true":
        status = "REFUSED_CLOSURE_NOT_CLAIM"
    elif bool_string(row["typed_grammar_signed"]) != "true":
        status = "REFUSED_NO_SOURCE_ONLY_SLOT_NOT_PARENT_DERIVED"
    elif bool_string(row["constructor_exhausted"]) != "true":
        status = "REFUSED_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED"
    elif bool_string(row["action_scale_owned"]) != "true":
        status = "REFUSED_ACTION_SCALE_OWNER_UNSIGNED"
    elif bool_string(row["readout_stable"]) != "true":
        status = "REFUSED_READOUT_RADIATIVE_STABILITY_UNSIGNED"
    elif bool_string(row["profile_inputs_filled"]) != "true":
        status = "REFUSED_PROFILE_MAP_INPUTS_NOT_SCORE_READY"
    else:
        status = "WOULD_REQUIRE_FULL_NUMERIC_NONCLAIM_REVIEW"
    return {
        "case_id": row["case_id"],
        "computed_status": status,
        "expected_status": row["expected_status"],
        "status_match": status == row["expected_status"],
        "claim_allowed": False,
        "valid_for_claim": False,
        "generated_utc": GENERATED_UTC,
    }


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [validate_dryrun_case(row) for row in cases]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "CG1903_0_grammar", "condition": "no-source-only slot/no-Hom parent grammar is signed", "current_status": "FAIL_NO_SOURCE_ONLY_SLOT_PARENT_GRAMMAR_NOT_DERIVED", "source_anchor": "P8_Y5_PARENT_QLOC_1903_NO_SOURCE_ONLY_SLOT_PARENT_GRAMMAR_ATTEMPT.csv:NSG1903_7_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1903_1_constructor", "condition": "ordinary coefficient constructor list is exhausted by parent generator", "current_status": "FAIL_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED", "source_anchor": "P8_Y5_PARENT_QLOC_1903_NOHOM_CONSTRUCTOR_GATE.csv:NHG1903_2_constructor_exhaustion", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1903_2_action_readout", "condition": "action-scale owner and readout/radiative stability are signed", "current_status": "FAIL_ACTION_SCALE_READOUT_UNSIGNED", "source_anchor": "P8_Y5_PARENT_QLOC_1903_NOHOM_CONSTRUCTOR_GATE.csv:NHG1903_4_action_scale;NHG1903_5_readout", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1903_3_profile", "condition": "profile/source-vector fallback is executable if theorem route fails", "current_status": "FAIL_PROFILE_MAP_INPUTS_NOT_SCORE_READY", "source_anchor": "P8_Y5_PARENT_QLOC_1903_PROFILE_MAP_INPUT_FILL_NONCLAIM.csv:PF1903_7_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1903_4_verdict", "condition": "1903 supports WEP/local-GR source universality claim", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG1903_0_grammar through CG1903_3_profile", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC1903_0_theorem", "decision": "do not promote no-source-only slot theorem", "reason": "inside a typed grammar the proof is clean, but current corpus has not derived the parent grammar/constructor exhaustion/action-scale/readout closure", "status": "THEOREM_ROUTE_EXACT_BUT_UNSIGNED", "next_dependency": "derive parent constructor exhaustion or action-scale/measure owner", "valid_for_claim": False},
        {"decision_id": "DEC1903_1_fallback", "decision": "keep profile/source-vector fallback explicit", "reason": "if source weights are not theorem-zero, WEP/local source work needs lambda owner, source profile, material tensor, parent basis map, and official readout arrays", "status": "PROFILE_INPUT_FILL_STAGED_NONCLAIM", "next_dependency": "fill or theorem-zero profile-map inputs", "valid_for_claim": False},
        {"decision_id": "DEC1903_2_next", "decision": "attack parent constructor exhaustion/action-scale owner next", "reason": "this is the least post-hoc route: derive what terms the parent action can generate rather than tuning source weights after tests", "status": "NEXT_TARGET_SELECTED", "next_dependency": "1904 parent action constructor exhaustion or action-scale owner", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1903_0_primary",
            "selection_status": "selected",
            "target_doc": "1904-Y5-R2FR-parent-action-constructor-exhaustion-or-action-scale-owner.md",
            "target_script": "scripts/Y5_R2FR_parent_action_constructor_exhaustion_or_action_scale_owner_1904.py",
            "objective": "try to derive that ordinary-sector coefficients are exhausted by the parent action generator and that one action-scale/measure owner forbids relative source weights",
            "success_condition": "parent-signed constructor exhaustion plus action-scale/readout stability, or explicit finite source-weight residual branch retained",
            "do_not": "do not treat the typed grammar as a claim by itself, do not divide away w_A using matter EOM, and do not score WEP without profile/source/readout inputs",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT1903_0_good_news", "area": "local-GR source route", "summary": "the route is now sharp: source universality follows if the parent grammar really has no source-only coefficient slot before variation", "risk_level": "THEOREM_ROUTE_CLEAR", "project_meaning": "we are not wandering; the remaining local-GR problem has a precise mathematical pressure point", "next_action": "derive constructor exhaustion/action-scale owner", "valid_for_claim": False},
        {"status_id": "STAT1903_1_gap", "area": "parent derivation", "summary": "current MTS files write the typed grammar but do not derive it from motion/time/space primitives", "risk_level": "CORE_PARENT_GRAMMAR_GAP", "project_meaning": "this is the coupling problem in its cleanest form", "next_action": "prove the parent action generator cannot produce w_A", "valid_for_claim": False},
        {"status_id": "STAT1903_2_empirical", "area": "WEP/profile fallback", "summary": "profile-map inputs are explicit but not executable; official data and source/material tensors remain missing", "risk_level": "EMPIRICAL_FALLBACK_NOT_SCORE_READY", "project_meaning": "if derivation fails, the nonclaim test route is still disciplined and not handwavy", "next_action": "fill profile/source/material/readout inputs only after theorem route stalls", "valid_for_claim": False},
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    return {
        "source_register": source_register_rows(),
        "grammar_attempt": grammar_attempt_rows(),
        "constructor_gate": constructor_gate_rows(),
        "profile_fill": profile_fill_rows(),
        "dryrun_cases": cases,
        "dryrun_results": dryrun_result_rows(cases),
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


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in fields.intersection(row.keys()):
                if bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all generated claim/scoring/signature flags remain false"


def blocked_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    markers = ["MISSING", "UNSIGNED", "NOT_DERIVED", "NOT_PARENT", "BLOCKED", "FAIL", "COUNTER", "NONCLAIM", "NOT_SCORE_READY", "REFUSED"]
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            text = " ".join(str(value) for value in row.values())
            if any(marker in text for marker in markers):
                for field in fields.intersection(row.keys()):
                    if bool_string(row[field]) == "true":
                        bad.append(f"{path.name}:{index}:{field}=true despite blocked marker")
    return not bad, "; ".join(bad) if bad else "blocked/unsigned/nonclaim rows are not score-ready"


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


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []
    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append({"validation_id": "VAL1903_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False})
    grammar_rows = csv_rows(OUTPUTS["grammar_attempt"])
    checks.append({"validation_id": "VAL1903_01_grammar_verdict", "status": "PASS" if any(row["attempt_id"] == "NSG1903_7_verdict" and row["status"] == "NO_SOURCE_ONLY_SLOT_PARENT_GRAMMAR_NOT_DERIVED" for row in grammar_rows) else "FAIL", "detail": "no-source-only slot remains unsigned", "valid_for_claim": False})
    constructor_rows = csv_rows(OUTPUTS["constructor_gate"])
    checks.append({"validation_id": "VAL1903_02_constructor_gate", "status": "PASS" if any(row["gate_id"] == "NHG1903_6_verdict" and row["current_status"] == "NO_SOURCE_ONLY_SLOT_CLAIM_BLOCKED" for row in constructor_rows) else "FAIL", "detail": "constructor/no-Hom gate blocks claim", "valid_for_claim": False})
    profile_rows = csv_rows(OUTPUTS["profile_fill"])
    checks.append({"validation_id": "VAL1903_03_profile_fill", "status": "PASS" if any(row["fill_id"] == "PF1903_7_verdict" and row["current_status"] == "PROFILE_MAP_INPUTS_NOT_SCORE_READY" for row in profile_rows) and all(bool_string(row["valid_prediction_row"]) == "false" for row in profile_rows) else "FAIL", "detail": "profile-map input fill remains nonclaim/not score-ready", "valid_for_claim": False})
    dry_rows = csv_rows(OUTPUTS["dryrun_results"])
    checks.append({"validation_id": "VAL1903_04_dryrun", "status": "PASS" if all(bool_string(row["status_match"]) == "true" and bool_string(row["claim_allowed"]) == "false" for row in dry_rows) else "FAIL", "detail": "dry-run refuses unsigned grammar, closure-as-claim, and incomplete profile inputs", "valid_for_claim": False})
    gate_rows = csv_rows(OUTPUTS["claim_gate"])
    checks.append({"validation_id": "VAL1903_05_claim_gate", "status": "PASS" if any(row["gate_id"] == "CG1903_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in gate_rows) else "FAIL", "detail": "claim remains blocked", "valid_for_claim": False})
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append({"validation_id": "VAL1903_06_next_target", "status": "PASS" if any(row["route_id"] == "NEXT1903_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL", "detail": "1904 target selected", "valid_for_claim": False})
    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append({"validation_id": "VAL1903_07_claim_flags_false", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})
    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append({"validation_id": "VAL1903_08_blocked_markers_not_ready", "status": "PASS" if blocked_ok else "FAIL", "detail": blocked_detail, "valid_for_claim": False})
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1903_09_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})
    checks.append({"validation_id": "VAL1903_10_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1903_11_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})
    formalization_hits = list(FORMALIZATION.rglob("*1903*")) if FORMALIZATION.exists() else []
    checks.append({"validation_id": "VAL1903_12_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1903_count={len(formalization_hits)}", "valid_for_claim": False})
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1903_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1903 no-source-only slot parent grammar or profile-map input fill", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1903 - No-Source-Only Slot Parent Grammar Or Profile-Map Input Fill

## Purpose

This checkpoint tries the clean derivation route first: make source-only species weights ungrammatical before variation. If that cannot be parent-signed, it sharpens the nonclaim profile/source-vector fallback.

## Result

- Inside a typed parent grammar, the no-source-only slot proof is exact.
- The current corpus has not yet derived the parent constructor list, action-scale owner, no-marker/no-hidden-scalar closure, or readout/radiative stability from MTS primitives.
- Therefore `w_A` cannot be claimed theorem-zero yet.
- The profile/source-vector fallback is now input-filled as a nonclaim ledger: range owner, Earth profile/composition, parent basis map, material response, and official readout arrays remain missing.
- No WEP, local-GR, or source-universality claim is made.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Parent Grammar Attempt

{markdown_table(rows_by_name["grammar_attempt"])}

## No-Hom Constructor Gate

{markdown_table(rows_by_name["constructor_gate"])}

## Profile-Map Input Fill

{markdown_table(rows_by_name["profile_fill"])}

## Dry-Run Cases

{markdown_table(rows_by_name["dryrun_cases"])}

## Dry-Run Results

{markdown_table(rows_by_name["dryrun_results"])}

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

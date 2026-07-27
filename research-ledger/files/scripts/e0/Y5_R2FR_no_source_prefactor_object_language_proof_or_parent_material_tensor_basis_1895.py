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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1895"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1895-Y5-R2FR-no-source-prefactor-object-language-proof-or-parent-material-tensor-basis.md"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1894_doc": ROOT / "1894-Y5-R2FR-source-domain-quotient-constructor-or-wep-material-tensor-intake.md",
    "1894_validation": OUT / "P8_Y5_BRR545_1894_VALIDATION.csv",
    "1894_qsrc": OUT / "P8_Y5_PARENT_QLOC_1894_SOURCE_DOMAIN_QUOTIENT_CONSTRUCTOR_ATTEMPT.csv",
    "1894_qgate": OUT / "P8_Y5_PARENT_QLOC_1894_QSRC_CLAUSE_GATE.csv",
    "1894_material": OUT / "P8_Y5_PARENT_QLOC_1894_WEP_MATERIAL_TENSOR_INTAKE_NONCLAIM.csv",
    "1894_next": OUT / "P8_Y5_PARENT_QLOC_1894_NEXT_TARGET.csv",
    "1887_ol": OUT / "P8_Y5_PARENT_QLOC_1887_OBJECT_LANGUAGE_TYPING_PROOF_AUDIT.csv",
    "1887_action_scale": OUT / "P8_Y5_PARENT_QLOC_1887_ACTION_SCALE_NORMALIZATION_AUDIT.csv",
    "1887_finite_contract": OUT / "P8_Y5_PARENT_QLOC_1887_FINITE_SOURCE_WEIGHT_VECTOR_INTAKE_CONTRACT.csv",
    "1887_template": OUT / "P8_Y5_PARENT_QLOC_1887_SOURCE_WEIGHT_VECTOR_TEMPLATE_NONCLAIM.csv",
    "1220_typed_signature": OUT / "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
    "1235_requirements": OUT / "P8_Y5_R10_1235_TYPED_DOMAIN_REQUIREMENTS.csv",
    "1236_certificate": OUT / "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
    "1055_contract": OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
    "954_action_clause": OUT / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
    "955_matter_lemma": OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
    "955_prefactor_class": OUT / "P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv",
    "1080_material_candidates": OUT / "P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv",
    "1424_material_vectors": OUT / "P8_Y5_R10_1424_TIPT_MATERIAL_VECTOR_CANDIDATES.csv",
}


SOURCE_NEEDLES = {
    "1894_doc": ["q_src", "NEXT1894_0_primary"],
    "1894_validation": ["VAL1894_OVERALL,PASS"],
    "1894_qsrc": ["QSRC1894_3_no_prefactor_obstruction", "SOURCE_DOMAIN_QUOTIENT_CONSTRUCTOR_NOT_PARENT_DERIVED"],
    "1894_qgate": ["QG1894_2_no_source_prefactors", "QSRC_CLAIM_BLOCKED"],
    "1894_material": ["WMI1894_3_full_parent_tensor", "MISSING_FULL_PARENT_MATERIAL_TENSOR"],
    "1894_next": ["NEXT1894_0_primary", "source-only w_A is not a well-typed parent object"],
    "1887_ol": ["OLT1887_1_exact_conditional_certificate", "OBJECT_LANGUAGE_TYPING_NOT_PARENT_DERIVED"],
    "1887_action_scale": ["ASN1887_1_classical_eom_false_positive", "ACTION_SCALE_OWNER_UNSIGNED"],
    "1887_finite_contract": ["FSV1887_1_component_basis", "FSV1887_6_K_Qbar_projection"],
    "1887_template": ["FSV1887_PARENT_ZERO_TEMPLATE", "MISSING_PARENT_OBJECT_LANGUAGE_THEOREM"],
    "1220_typed_signature": ["PTOL1220_3_source_weight_exclusion", "PARENT_TYPED_OBJECT_LANGUAGE_SIGNATURE_NOT_DERIVED"],
    "1235_requirements": ["TREQ1235_0_parent_object_language", "MISSING_PARENT_SIGNATURE"],
    "1236_certificate": ["CERT1236_5_source_label_forgetting", "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED"],
    "1055_contract": ["PAC1055_4_source_label_forgetting", "PAC1055_6_single_parent_action"],
    "954_action_clause": ["PAC954_1_no_source_prefactors", "PAC954_5_GR_source_limit_clause"],
    "955_matter_lemma": ["MMA955_5_minimal_schema", "MMA955_6_verdict"],
    "955_prefactor_class": ["SPC955_2_relative_species_weight", "SPC955_4_nonHilbert_weight"],
    "1080_material_candidates": ["MAT1080_4_full_tensor_upgrade", "MISSING_FULL_MATERIAL_TENSOR"],
    "1424_material_vectors": ["MAT1424_0_Z_over_A_toy", "SMOKE_CONTEXT_NOT_PARENT_EM_OWNER"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1895_SOURCE_REGISTER.csv",
    "object_language_attempt": OUT / "P8_Y5_PARENT_QLOC_1895_NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_ATTEMPT.csv",
    "typing_gate": OUT / "P8_Y5_PARENT_QLOC_1895_SOURCE_PREFACTOR_TYPING_GATE.csv",
    "material_basis": OUT / "P8_Y5_PARENT_QLOC_1895_PARENT_MATERIAL_TENSOR_BASIS_NONCLAIM.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1895_OBJECT_LANGUAGE_MATERIAL_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1895_OBJECT_LANGUAGE_MATERIAL_DRYRUN_RESULTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1895_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1895_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1895_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1895_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1895_VALIDATION.csv",
}


BRANCH_COPIES = {
    "object_language_attempt": MICROSCOPE_RESIDUALS / OUTPUTS["object_language_attempt"].name,
    "typing_gate": QUEUE / "JR1895_SOURCE_PREFACTOR_TYPING_GATE_NONCLAIM.csv",
    "material_basis": SOURCE_WEIGHT_DOCS / "PARENT_MATERIAL_TENSOR_BASIS_1895_NONCLAIM.csv",
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
        for row in rows:
            writer.writerow(row)


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
        needles = SOURCE_NEEDLES[source_id]
        missing_needles = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle_count": len(needles),
                "missing_needles": "; ".join(missing_needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing_needles else "SOURCE_OR_NEEDLE_MISSING",
                "valid_for_claim": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def object_language_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "NSP1895_0_target",
            "claim_piece": "source-only prefactor object-language exclusion",
            "formal_statement": "Source-only w_A is not a well-typed parent object: it has no nongravitational observable owner, no gauge/representation role, no quotient-geometry role, and no admissible coefficient target sort before variation",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "would kill the pre-action bypass that defeated q_src in 1894",
            "source_anchor": "P8_Y5_PARENT_QLOC_1894_SOURCE_DOMAIN_QUOTIENT_CONSTRUCTOR_ATTEMPT.csv:QSRC1894_3_no_prefactor_obstruction; P8_Y5_PARENT_QLOC_1887_OBJECT_LANGUAGE_TYPING_PROOF_AUDIT.csv:OLT1887_0_target",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "NSP1895_1_exact_if_typed",
            "claim_piece": "typed exclusion theorem",
            "formal_statement": "If parent sorts are derived and disjoint, Arg(Coeff_active_source) excludes SpeciesLabel, and variation precedes readout, then w_A S_A is ill-typed unless w_A is an owned ordinary matter constant or retained finite residual",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "the formal proof is syntax/category-level: no source-only coefficient constructor exists in the parent language",
            "source_anchor": "P8_Y5_PARENT_QLOC_1887_OBJECT_LANGUAGE_TYPING_PROOF_AUDIT.csv:OLT1887_1_exact_conditional_certificate; P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv:CERT1236_0_parent_sorts;CERT1236_5_source_label_forgetting",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "NSP1895_2_current_signature",
            "claim_piece": "current corpus parent typed signature",
            "formal_statement": "The current corpus derives the typed parent object-language/action domain from MTS primitives rather than adopting it as closure",
            "status": "PARENT_TYPED_OBJECT_LANGUAGE_NOT_DERIVED",
            "proof_or_obstruction": "1220 and 1236 both mark the grammar/certificate as written but not derived",
            "source_anchor": "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv:PTOL1220_7_verdict; P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv:CERT1236_6_current_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "NSP1895_3_direct_sum_counterexample",
            "claim_piece": "species-family constants counterexample",
            "formal_statement": "Direct-sum ordinary matter sectors can carry independent constants or multipliers c_A unless the parent functor forbids disconnected species-family coefficient objects",
            "status": "DIRECT_SUM_COUNTEREXAMPLE_SURVIVES",
            "proof_or_obstruction": "connectedness/naturality is not enough; this is exactly the source-only w_A danger in typed form",
            "source_anchor": "P8_Y5_PARENT_QLOC_1887_OBJECT_LANGUAGE_TYPING_PROOF_AUDIT.csv:OLT1887_3_direct_sum_counterexample; P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv:SPC955_2_relative_species_weight",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "NSP1895_4_action_scale_readout",
            "claim_piece": "action-scale and readout stability",
            "formal_statement": "Even a tree-level type exclusion is claim-grade only if one action-scale/measure owner and radiative/readout closure prevent w_A returning through hbar, measure, loops, clocks, or local readout",
            "status": "ACTION_SCALE_READOUT_OWNER_UNSIGNED",
            "proof_or_obstruction": "classical matter EOM can hide a relative action weight while Hilbert/coframe source still changes",
            "source_anchor": "P8_Y5_PARENT_QLOC_1887_ACTION_SCALE_NORMALIZATION_AUDIT.csv:ASN1887_1_classical_eom_false_positive;ASN1887_5_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "NSP1895_5_verdict",
            "claim_piece": "promote no-source-prefactor object-language proof",
            "formal_statement": "NoSourceOnlySpeciesSlot follows from current MTS parent primitives without extra closure grammar",
            "status": "NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_PROOF_NOT_PARENT_DERIVED",
            "proof_or_obstruction": "the exclusion is exact if typed, but parent sort derivation, no-Hom theorem, source-label forgetting, action-scale owner, no-marker theorem, and readout/radiative closure are not simultaneously signed",
            "source_anchor": "NSP1895_0_target through NSP1895_4_action_scale_readout",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def typing_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "TYP1895_0_parent_sorts",
            "required_clause": "parent sorts are derived and disjoint before fitting/readout",
            "formal_condition": "Q_obs, Theta_rep, SpeciesLabel, Coeff_active_source, Readout, and hidden/marker sorts have declared non-overlapping constructor rules",
            "current_status": "SCHEMA_WRITTEN_NOT_DERIVED",
            "if_pass": "source-only coefficient membership can be checked rather than assumed",
            "if_fail": "syntax-by-decree is only closure",
            "source_anchor": "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv:PTOL1220_0_parent_domain; P8_Y5_R10_1235_TYPED_DOMAIN_REQUIREMENTS.csv:TREQ1235_0_parent_object_language",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "TYP1895_1_no_species_to_source_coeff",
            "required_clause": "Hom(SpeciesLabel,Coeff_active_source)=empty",
            "formal_condition": "no parent morphism maps A, material marker, boundary class, or readout label to a source-only coefficient before variation",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "if_pass": "w_A has no target sort and cannot enter S_matter as source-only data",
            "if_fail": "relative source-weight countermodel survives",
            "source_anchor": "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv:PTOL1220_3_source_weight_exclusion; P8_Y5_PARENT_QLOC_1887_OBJECT_LANGUAGE_TYPING_PROOF_AUDIT.csv:OLT1887_7_no_marker_protection",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "TYP1895_2_total_variation_order",
            "required_clause": "variation-before-readout is parent-owned",
            "formal_condition": "S_matter is varied as one total object before material/source/readout projection",
            "current_status": "CONDITIONAL_MATH_CLEAN_NOT_PARENT_COMPLETE",
            "if_pass": "bookkeeping species labels cannot become coupling selectors after variation",
            "if_fail": "post-variation current rescale remains legal",
            "source_anchor": "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv:PAC954_2_total_Hilbert_derivative; P8_Y5_PARENT_QLOC_1894_QSRC_CLAUSE_GATE.csv:QG1894_1_total_hilbert_source",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "TYP1895_3_action_scale_measure",
            "required_clause": "one action-scale/hbar/measure owner covers all ordinary sectors",
            "formal_condition": "relative species action multipliers are not independent quantum/measure normalizations",
            "current_status": "ACTION_SCALE_OWNER_UNSIGNED",
            "if_pass": "classical-EOM rescaling false positive is removed",
            "if_fail": "w_A can hide as measure/action-scale debt",
            "source_anchor": "P8_Y5_PARENT_QLOC_1887_ACTION_SCALE_NORMALIZATION_AUDIT.csv:ASN1887_3_quantum_path_integral_scale;ASN1887_5_verdict",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "TYP1895_4_radiative_readout",
            "required_clause": "typed exclusion survives effective/readout reduction",
            "formal_condition": "loops, spectroscopy, clocks, source-worldtube readouts, and projections preserve the same source coefficient domain",
            "current_status": "READOUT_RADIATIVE_UNSIGNED",
            "if_pass": "tree-level no-slot proof transfers to observables",
            "if_fail": "readout coefficient drift remains finite closure debt",
            "source_anchor": "P8_Y5_PARENT_QLOC_1887_ACTION_SCALE_NORMALIZATION_AUDIT.csv:ASN1887_4_radiative_readout_stability; P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv:PTOL1220_5_radiative_readout_closure",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "TYP1895_5_verdict",
            "required_clause": "NoSourceOnlySpeciesSlot is a parent theorem",
            "formal_condition": "TYP1895_0 through TYP1895_4 all pass",
            "current_status": "NO_SOURCE_PREFACTOR_TYPING_CLAIM_BLOCKED",
            "if_pass": "Delta_w_species theorem-zero source route opens",
            "if_fail": "finite Delta_w/material tensor branch remains required",
            "source_anchor": "TYP1895_0_parent_sorts through TYP1895_4_radiative_readout",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def material_basis_rows() -> list[dict[str, Any]]:
    return [
        {
            "basis_id": "PMTB1895_0_parent_basis_target",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "parent material response basis X",
            "definition": "a finite parent-owned basis of material/source generators V_WEP,X shared by C_parent_X, R_material_X, R_source_X, and tau_eff_X",
            "current_status": "MISSING_PARENT_RESPONSE_BASIS",
            "source_anchor": "P8_Y5_PARENT_QLOC_1894_WEP_MATERIAL_TENSOR_INTAKE_NONCLAIM.csv:WMI1894_3_full_parent_tensor",
            "missing_for_claim": "parent generator list, units, signs, no-double-counting rule, coefficient owner",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "PMTB1895_1_context_composition",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "source-backed composition context",
            "definition": "PtRh10 and TA6V elemental mass-fraction context can seed a future tensor but is not the tensor",
            "current_status": "SOURCE_BACKED_CONTEXT_ONLY",
            "source_anchor": "P8_Y5_PARENT_QLOC_1894_WEP_MATERIAL_TENSOR_INTAKE_NONCLAIM.csv:WMI1894_0_pair_context;WMI1894_1_constituent_table",
            "missing_for_claim": "isotope/alloy averaging and parent basis response map",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "PMTB1895_2_proxy_inventory",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "toy/proxy material vectors",
            "definition": "Z/A, neutron-excess, electron-mass, alpha/Coulomb smoke vectors are retained as context/proxy only",
            "current_status": "PROXY_CONTEXT_NOT_PARENT_TENSOR",
            "source_anchor": "P8_Y5_R10_1424_TIPT_MATERIAL_VECTOR_CANDIDATES.csv:MAT1424_0_Z_over_A_toy..MAT1424_3_alpha_Coulomb_smoke_abs",
            "missing_for_claim": "MTS parent basis map and proof proxies span the allowed source response space",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "PMTB1895_3_tensor_formula",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "full tensor formula",
            "definition": "R_material_X(A,B)=partial_X ln M_A - partial_X ln M_B in the parent response basis, with common-mode and double-counted rest-mass pieces projected out",
            "current_status": "FORMULA_STUB_PARENT_BASIS_MISSING",
            "source_anchor": "P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv:MAT1080_4_full_tensor_upgrade",
            "missing_for_claim": "parent basis X, mass functional, binding/EM/nuclear decomposition, isotope averaging, source normalization",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "PMTB1895_4_acceptance",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "parent material tensor basis acceptance",
            "definition": "basis is acceptable only when every tensor component has parent meaning, units, sign convention, source path, and matching parent coefficient/tau leg",
            "current_status": "PARENT_MATERIAL_TENSOR_BASIS_BLOCKED_NONCLAIM",
            "source_anchor": "P8_Y5_PARENT_QLOC_1894_WEP_MATERIAL_TENSOR_INTAKE_NONCLAIM.csv:WMI1894_6_acceptance",
            "missing_for_claim": "PMTB1895_0 parent basis plus PMTB1895_3 full tensor formula instantiated with sourced values",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "DRY1895_0_typing_unsigned",
            "typed_parent_signature_signed": False,
            "uses_syntax_by_decree": False,
            "action_scale_owner_signed": False,
            "material_basis_level": "missing",
            "uses_proxy_as_tensor": False,
            "expected_status": "REFUSED_PARENT_TYPED_OBJECT_LANGUAGE_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1895_1_syntax_by_decree",
            "typed_parent_signature_signed": False,
            "uses_syntax_by_decree": True,
            "action_scale_owner_signed": False,
            "material_basis_level": "missing",
            "uses_proxy_as_tensor": False,
            "expected_status": "REFUSED_SYNTAX_BY_DECREE",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1895_2_action_scale_unsigned",
            "typed_parent_signature_signed": True,
            "uses_syntax_by_decree": False,
            "action_scale_owner_signed": False,
            "material_basis_level": "missing",
            "uses_proxy_as_tensor": False,
            "expected_status": "REFUSED_ACTION_SCALE_OWNER_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1895_3_material_basis_missing",
            "typed_parent_signature_signed": True,
            "uses_syntax_by_decree": False,
            "action_scale_owner_signed": True,
            "material_basis_level": "missing",
            "uses_proxy_as_tensor": False,
            "expected_status": "REFUSED_PARENT_MATERIAL_RESPONSE_BASIS_MISSING",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1895_4_proxy_tensor",
            "typed_parent_signature_signed": True,
            "uses_syntax_by_decree": False,
            "action_scale_owner_signed": True,
            "material_basis_level": "proxy_only",
            "uses_proxy_as_tensor": True,
            "expected_status": "REFUSED_PROXY_VECTOR_NOT_PARENT_TENSOR",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1895_5_schema_only",
            "typed_parent_signature_signed": True,
            "uses_syntax_by_decree": False,
            "action_scale_owner_signed": True,
            "material_basis_level": "schema_only",
            "uses_proxy_as_tensor": False,
            "expected_status": "SCHEMA_ONLY_NOT_EVIDENCE",
            "valid_for_claim": False,
        },
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    typed_signed = bool_string(row["typed_parent_signature_signed"]) == "true"
    syntax_by_decree = bool_string(row["uses_syntax_by_decree"]) == "true"
    scale_signed = bool_string(row["action_scale_owner_signed"]) == "true"
    material_level = str(row["material_basis_level"])
    proxy_tensor = bool_string(row["uses_proxy_as_tensor"]) == "true"

    if syntax_by_decree:
        status = "REFUSED_SYNTAX_BY_DECREE"
    elif not typed_signed:
        status = "REFUSED_PARENT_TYPED_OBJECT_LANGUAGE_UNSIGNED"
    elif not scale_signed:
        status = "REFUSED_ACTION_SCALE_OWNER_UNSIGNED"
    elif proxy_tensor or material_level == "proxy_only":
        status = "REFUSED_PROXY_VECTOR_NOT_PARENT_TENSOR"
    elif material_level == "schema_only":
        status = "SCHEMA_ONLY_NOT_EVIDENCE"
    elif material_level == "missing":
        status = "REFUSED_PARENT_MATERIAL_RESPONSE_BASIS_MISSING"
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
        {
            "gate_id": "CG1895_0_object_language",
            "condition": "parent typed object language excludes source-only prefactor objects",
            "current_status": "FAIL_NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_PROOF_NOT_PARENT_DERIVED",
            "source_anchor": "P8_Y5_PARENT_QLOC_1895_NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_ATTEMPT.csv:NSP1895_5_verdict",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1895_1_action_scale",
            "condition": "action-scale/measure/readout owner prevents relative w_A returning outside syntax",
            "current_status": "FAIL_ACTION_SCALE_READOUT_OWNER_UNSIGNED",
            "source_anchor": "P8_Y5_PARENT_QLOC_1895_NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_ATTEMPT.csv:NSP1895_4_action_scale_readout",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1895_2_material_basis",
            "condition": "WEP parent material tensor basis is constructed, not proxy-only",
            "current_status": "FAIL_PARENT_MATERIAL_TENSOR_BASIS_BLOCKED_NONCLAIM",
            "source_anchor": "P8_Y5_PARENT_QLOC_1895_PARENT_MATERIAL_TENSOR_BASIS_NONCLAIM.csv:PMTB1895_4_acceptance",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1895_3_verdict",
            "condition": "source prefactor zero or WEP material score is claim-ready",
            "current_status": "CLAIM_BLOCKED",
            "source_anchor": "CG1895_0_object_language through CG1895_2_material_basis",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1895_0_typing",
            "decision": "typed exclusion is mathematically clean but not parent-derived",
            "reason": "the grammar certificate exists, but deriving the sorts/no-Hom rule from MTS primitives is still missing",
            "status": "OBJECT_LANGUAGE_ROUTE_SHARP_BUT_UNSIGNED",
            "next_dependency": "derive parent sort disjointness/no-Hom theorem or demote to closure",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1895_1_material",
            "decision": "material tensor basis is staged only as a nonclaim skeleton",
            "reason": "composition/proxy context exists, but the parent response basis and full tensor formula are not instantiated",
            "status": "PARENT_MATERIAL_BASIS_SKELETON_NONCLAIM",
            "next_dependency": "parent response basis X and no-double-counting rule",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1895_2_next",
            "decision": "attack parent sort disjointness / no-Hom constructor next",
            "reason": "this is the precise missing theorem behind the object-language proof",
            "status": "NEXT_TARGET_SELECTED",
            "next_dependency": "1896 parent sort disjointness no-Hom proof or finite Delta_w vector basis",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1895_0_primary",
            "selection_status": "selected",
            "target_doc": "1896-Y5-R2FR-parent-sort-disjointness-nohom-proof-or-finite-deltaw-basis.md",
            "target_script": "scripts/Y5_R2FR_parent_sort_disjointness_nohom_proof_or_finite_deltaw_basis_1896.py",
            "objective": "try to derive the parent sort disjointness/no-Hom theorem that forbids SpeciesLabel -> Coeff_active_source; if it fails, build the finite Delta_w component basis needed for later WEP/R10 scoring",
            "success_condition": "parent-signed no-Hom theorem, or nonclaim finite Delta_w basis rows with common-mode projector, norm, and no-cancellation policy",
            "do_not": "do not claim source-weight zero by syntax decree, do not treat proxies as parent tensors, and do not score any WEP/R10 row",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT1895_0_typing",
            "area": "source coupling / object language",
            "summary": "the best theorem route is now exactly a parent sort disjointness/no-Hom proof",
            "risk_level": "NARROW_PARENT_GRAMMAR_GAP",
            "project_meaning": "the source-coupling problem has been narrowed from vague coupling worry to one typed parent-language theorem",
            "next_action": "derive no-Hom(SpeciesLabel,Coeff_active_source) or accept finite Delta_w branch",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT1895_1_material",
            "area": "WEP tensor fallback",
            "summary": "a parent material tensor basis skeleton exists but cannot score without parent response basis",
            "risk_level": "EMPIRICAL_FALLBACK_NOT_READY",
            "project_meaning": "the testing route is preserved without allowing proxy shortcuts",
            "next_action": "build finite Delta_w basis and parent response-basis map",
            "valid_for_claim": False,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    return {
        "source_register": source_register_rows(),
        "object_language_attempt": object_language_attempt_rows(),
        "typing_gate": typing_gate_rows(),
        "material_basis": material_basis_rows(),
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
    flag_fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in flag_fields.intersection(row.keys()):
                if bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all generated claim/scoring/signature flags remain false"


def blocked_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    blocked_markers = [
        "MISSING",
        "UNSIGNED",
        "NOT_DERIVED",
        "NOT_PARENT",
        "BLOCKED",
        "FAIL",
        "COUNTER",
        "PROXY",
        "NONCLAIM",
        "SCHEMA",
        "CLAIM_BLOCKED",
    ]
    readiness_fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            row_text = " ".join(str(value) for value in row.values())
            if any(marker in row_text for marker in blocked_markers):
                for field in readiness_fields.intersection(row.keys()):
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
    checks.append({"validation_id": "VAL1895_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL", "detail": "all source paths exist and needles found", "valid_for_claim": False})

    attempt_rows_loaded = csv_rows(OUTPUTS["object_language_attempt"])
    checks.append({"validation_id": "VAL1895_01_object_language_verdict", "status": "PASS" if any(row["attempt_id"] == "NSP1895_5_verdict" and row["status"] == "NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_PROOF_NOT_PARENT_DERIVED" for row in attempt_rows_loaded) else "FAIL", "detail": "object-language exclusion remains unsigned", "valid_for_claim": False})

    typing_rows_loaded = csv_rows(OUTPUTS["typing_gate"])
    checks.append({"validation_id": "VAL1895_02_typing_gate", "status": "PASS" if any(row["gate_id"] == "TYP1895_5_verdict" and row["current_status"] == "NO_SOURCE_PREFACTOR_TYPING_CLAIM_BLOCKED" for row in typing_rows_loaded) else "FAIL", "detail": "typing gate blocks source-weight zero claim", "valid_for_claim": False})

    material_rows_loaded = csv_rows(OUTPUTS["material_basis"])
    checks.append({"validation_id": "VAL1895_03_material_basis", "status": "PASS" if len(material_rows_loaded) >= 5 and all(row["score_ready"] == "False" and row["valid_prediction_row"] == "False" for row in material_rows_loaded) else "FAIL", "detail": "parent material tensor basis skeleton remains nonclaim/not score-ready", "valid_for_claim": False})

    dry_rows_loaded = csv_rows(OUTPUTS["dryrun_results"])
    checks.append({"validation_id": "VAL1895_04_dryrun", "status": "PASS" if all(row["status_match"] == "True" and row["claim_allowed"] == "False" for row in dry_rows_loaded) else "FAIL", "detail": "dry-run refuses unsigned typing, syntax decree, unsigned action scale, missing basis, proxy tensor, and schema-only rows", "valid_for_claim": False})

    gate_rows_loaded = csv_rows(OUTPUTS["claim_gate"])
    checks.append({"validation_id": "VAL1895_05_claim_gate", "status": "PASS" if any(row["gate_id"] == "CG1895_3_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in gate_rows_loaded) else "FAIL", "detail": "claim remains blocked", "valid_for_claim": False})

    next_rows_loaded = csv_rows(OUTPUTS["next_target"])
    checks.append({"validation_id": "VAL1895_06_next_target", "status": "PASS" if any(row["route_id"] == "NEXT1895_0_primary" and row["selection_status"] == "selected" for row in next_rows_loaded) else "FAIL", "detail": "1896 no-Hom target selected", "valid_for_claim": False})

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append({"validation_id": "VAL1895_07_claim_flags_false", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})

    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append({"validation_id": "VAL1895_08_blocked_markers_not_ready", "status": "PASS" if blocked_ok else "FAIL", "detail": blocked_detail, "valid_for_claim": False})

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1895_09_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})

    checks.append({"validation_id": "VAL1895_10_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1895_11_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})

    formalization_hits = list(FORMALIZATION.rglob("*1895*")) if FORMALIZATION.exists() else []
    checks.append({"validation_id": "VAL1895_12_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1895_count={len(formalization_hits)}", "valid_for_claim": False})

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1895_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1895 no-source-prefactor object-language proof or parent material tensor basis", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1895 - No-Source-Prefactor Object-Language Proof Or Parent Material Tensor Basis

## Purpose

This checkpoint tries the best derivation route for killing the coupling: prove `w_A` is not a well-typed parent object before variation. If that fails, it builds the parent material tensor basis skeleton needed for WEP without promoting proxy vectors.

## Result

- The typed theorem is exact if the parent grammar is signed: a source-only `w_A` has no owner, no transformation law, and no admissible source coefficient target.
- The current corpus still does not derive that grammar from MTS primitives. The verdict is `NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_PROOF_NOT_PARENT_DERIVED`.
- The material-tensor fallback is clearer but still nonclaim: composition/proxy context exists, while the parent response basis and full tensor remain missing.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Object-Language Attempt

{markdown_table(rows_by_name["object_language_attempt"])}

## Typing Gate

{markdown_table(rows_by_name["typing_gate"])}

## Parent Material Tensor Basis

{markdown_table(rows_by_name["material_basis"])}

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

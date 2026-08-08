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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1896"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1896-Y5-R2FR-parent-sort-disjointness-nohom-proof-or-finite-deltaw-basis.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1895_doc": ROOT / "1895-Y5-R2FR-no-source-prefactor-object-language-proof-or-parent-material-tensor-basis.md",
    "1895_validation": OUT / "P8_Y5_BRR545_1895_VALIDATION.csv",
    "1895_attempt": OUT / "P8_Y5_PARENT_QLOC_1895_NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_ATTEMPT.csv",
    "1895_typing_gate": OUT / "P8_Y5_PARENT_QLOC_1895_SOURCE_PREFACTOR_TYPING_GATE.csv",
    "1895_material_basis": OUT / "P8_Y5_PARENT_QLOC_1895_PARENT_MATERIAL_TENSOR_BASIS_NONCLAIM.csv",
    "1895_next": OUT / "P8_Y5_PARENT_QLOC_1895_NEXT_TARGET.csv",
    "1114_no_hidden_visible": OUT / "P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv",
    "1107_exhaustion": OUT / "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv",
    "1066_typing": OUT / "P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv",
    "1078_object_proof": OUT / "P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv",
    "1092_triviality": OUT / "P8_Y5_R10_1092_HIDDEN_INVARIANT_TRIVIALITY_ATTEMPT.csv",
    "1051_scalar_obstruction": OUT / "P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv",
    "1676_no_marker": OUT / "P8_Y5_PARENT_QLOC_1676_OBJECT_LANGUAGE_NO_MARKER_THEOREM_ATTEMPT.csv",
    "1338_ol_theorem": OUT / "P8_Y5_R10_1338_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv",
    "1888_finite": OUT / "P8_Y5_PARENT_QLOC_1888_FINITE_DELTAW_VECTOR_ROW_INTAKE.csv",
    "1889_basis": OUT / "P8_Y5_PARENT_QLOC_1889_REAL_DELTAW_COMPONENT_BASIS_ACQUISITION.csv",
    "1891_coeff": OUT / "P8_Y5_PARENT_QLOC_1891_DELTAW_SPECIES_COEFFICIENT_ROW_NONCLAIM.csv",
}


SOURCE_NEEDLES = {
    "1895_doc": ["NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_PROOF_NOT_PARENT_DERIVED", "NEXT1895_0_primary"],
    "1895_validation": ["VAL1895_OVERALL,PASS"],
    "1895_attempt": ["NSP1895_5_verdict", "NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_PROOF_NOT_PARENT_DERIVED"],
    "1895_typing_gate": ["TYP1895_1_no_species_to_source_coeff", "NO_SOURCE_PREFACTOR_TYPING_CLAIM_BLOCKED"],
    "1895_material_basis": ["PMTB1895_4_acceptance", "PARENT_MATERIAL_TENSOR_BASIS_BLOCKED_NONCLAIM"],
    "1895_next": ["NEXT1895_0_primary", "SpeciesLabel -> Coeff_active_source"],
    "1114_no_hidden_visible": ["NHV1114_1_typed_language", "NO_HIDDEN_VISIBLE_MORPHISM_NOT_DERIVED"],
    "1107_exhaustion": ["EXH1107_1_chain_rule", "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED"],
    "1066_typing": ["OLT1066_4_inert_source_scalar", "conditional_not_parent_derived"],
    "1078_object_proof": ["OL1078_3_counterexample", "OBJECT_LANGUAGE_NOT_SIGNED"],
    "1092_triviality": ["HIT1092_3_scalar_counterexample", "TRIVIALITY_NOT_DERIVED"],
    "1051_scalar_obstruction": ["ISO1051_3_domain_marker", "LIVE_LABEL_OBSTRUCTION"],
    "1676_no_marker": ["NSS1676_5_verdict", "NO_SOURCE_ONLY_SLOT_THEOREM_NOT_PROVED"],
    "1338_ol_theorem": ["OLT1338_0_target", "NOT_DERIVED_CURRENT_CORPUS"],
    "1888_finite": ["FDV1888_0_core_vector", "MISSING_PARENT_COMPONENT_BASIS"],
    "1889_basis": ["CB1889_1_pre_action_species_prefactor", "CB1889_4_nonHilbert_current"],
    "1891_coeff": ["DWS1891_0_delta_w_species_coefficient_slot", "SYMBOLIC_FREE_COEFFICIENT_NO_PARENT_VALUE"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1896_SOURCE_REGISTER.csv",
    "nohom_attempt": OUT / "P8_Y5_PARENT_QLOC_1896_PARENT_SORT_DISJOINTNESS_NOHOM_ATTEMPT.csv",
    "nohom_gate": OUT / "P8_Y5_PARENT_QLOC_1896_NOHOM_GATE.csv",
    "deltaw_basis": OUT / "P8_Y5_PARENT_QLOC_1896_FINITE_DELTAW_COMPONENT_BASIS_NONCLAIM.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1896_NOHOM_DELTABASIS_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1896_NOHOM_DELTABASIS_DRYRUN_RESULTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1896_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1896_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1896_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1896_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1896_VALIDATION.csv",
}


BRANCH_COPIES = {
    "nohom_attempt": MICROSCOPE_RESIDUALS / OUTPUTS["nohom_attempt"].name,
    "nohom_gate": QUEUE / "JR1896_NOHOM_GATE_NONCLAIM.csv",
    "deltaw_basis": SOURCE_WEIGHT_DOCS / "FINITE_DELTAW_COMPONENT_BASIS_1896_NONCLAIM.csv",
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


def nohom_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "NH1896_0_target",
            "claim_piece": "parent sort disjointness / no-Hom theorem",
            "formal_statement": "Hom_parent(SpeciesLabel, Coeff_active_source)=empty and Hom_parent(Marker_hidden, Coeff_active_source)=empty before variation/readout",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "this is the exact parent-language theorem needed to make source-only w_A unformable",
            "source_anchor": "P8_Y5_PARENT_QLOC_1895_SOURCE_PREFACTOR_TYPING_GATE.csv:TYP1895_1_no_species_to_source_coeff",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "NH1896_1_conditional_typed_proof",
            "claim_piece": "typed no-Hom proof",
            "formal_statement": "If parent sorts are derived/disjoint and Coeff_active_source has domain Q_obs x Theta_rep x UniversalCalibration x RetainedResidual only, then no morphism from SpeciesLabel or hidden marker can target active source coefficients",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "well-typed terms cannot be formed without an argument slot; this is formal grammar, not small-coupling dynamics",
            "source_anchor": "P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv:NHV1114_1_typed_language; P8_Y5_PARENT_QLOC_1895_NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_ATTEMPT.csv:NSP1895_1_exact_if_typed",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "NH1896_2_product_category_route",
            "claim_piece": "product/sequester route",
            "formal_statement": "If C_parent=C_vis x C_label and visible/source coefficient functors factor only through pi_vis plus fixed representation data, then label tangents annihilate source coefficients",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "chain rule works once factorization is parent-derived; current corpus has not derived this product-category source factorization",
            "source_anchor": "P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv:NHV1114_2_product_category; P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv:EXH1107_1_chain_rule",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "NH1896_3_counterexamples",
            "claim_piece": "why no-Hom is not current proof",
            "formal_statement": "Direct-sum species constants, surviving hidden invariant scalars, domain/material markers, and action-scale/readout routes can still define source coefficient maps unless explicitly typed out",
            "status": "COUNTEREXAMPLES_RETAINED",
            "proof_or_obstruction": "naturality/gauge/diffeomorphism and candidate typing do not erase legal scalar or species-family coefficient maps",
            "source_anchor": "P8_Y5_R10_1078_OBJECT_LANGUAGE_PROOF_ATTEMPT.csv:OL1078_3_counterexample; P8_Y5_R10_1092_HIDDEN_INVARIANT_TRIVIALITY_ATTEMPT.csv:HIT1092_3_scalar_counterexample; P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv:ISO1051_3_domain_marker",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "NH1896_4_readout_measure_gap",
            "claim_piece": "readout/measure stability",
            "formal_statement": "Even if tree-level no-Hom is adopted, S_eff, loops, spectroscopy, clocks, local projections, hbar/measure, and source-worldtube readout must preserve the no-Hom domain",
            "status": "READOUT_MEASURE_STABILITY_UNSIGNED",
            "proof_or_obstruction": "1895 and 1887 keep action-scale and radiative/readout gates unsigned",
            "source_anchor": "P8_Y5_PARENT_QLOC_1895_SOURCE_PREFACTOR_TYPING_GATE.csv:TYP1895_3_action_scale_measure;TYP1895_4_radiative_readout",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "NH1896_5_verdict",
            "claim_piece": "promote no-Hom theorem",
            "formal_statement": "Current MTS parent primitives derive Hom(SpeciesLabel,Coeff_active_source)=empty",
            "status": "PARENT_SORT_DISJOINTNESS_NOHOM_NOT_DERIVED",
            "proof_or_obstruction": "typed/product proof is exact conditionally, but parent sort derivation, object-language exhaustion, hidden invariant/no-marker exclusion, and readout/measure stability remain unsigned",
            "source_anchor": "NH1896_0_target through NH1896_4_readout_measure_gap",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def nohom_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "NHG1896_0_parent_sort_derivation",
            "required_clause": "parent sorts are derived from MTS primitives",
            "current_status": "MISSING_PARENT_SIGNATURE",
            "if_pass": "no-Hom is theorem-level rather than syntax decree",
            "if_fail": "object-language route remains private closure",
            "source_anchor": "P8_Y5_R10_1235_TYPED_DOMAIN_REQUIREMENTS.csv:TREQ1235_0_parent_object_language; P8_Y5_PARENT_QLOC_1895_SOURCE_PREFACTOR_TYPING_GATE.csv:TYP1895_0_parent_sorts",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "NHG1896_1_no_species_hom",
            "required_clause": "SpeciesLabel has no morphism to active source coefficient slots",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "if_pass": "pre-action Delta_w_species is ill-typed",
            "if_fail": "relative species prefactor remains live",
            "source_anchor": "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv:PTOL1220_3_source_weight_exclusion",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "NHG1896_2_no_marker_hom",
            "required_clause": "hidden/domain/boundary/readout markers cannot be retyped as source coefficients",
            "current_status": "NO_MARKER_THEOREM_NOT_PROVED",
            "if_pass": "Delta_w_marker_hidden is theorem-zero",
            "if_fail": "hidden marker source weights stay in finite basis",
            "source_anchor": "P8_Y5_PARENT_QLOC_1676_OBJECT_LANGUAGE_NO_MARKER_THEOREM_ATTEMPT.csv:NSS1676_2_no_hidden_marker;NSS1676_5_verdict",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "NHG1896_3_exhaustion_stability",
            "required_clause": "parent-generated coefficient image is exhausted and stable under readout",
            "current_status": "OBJECT_LANGUAGE_EXHAUSTION_NOT_DERIVED",
            "if_pass": "no extra source coefficients can appear in S_eff/readout",
            "if_fail": "finite residual route is mandatory",
            "source_anchor": "P8_Y5_R10_1107_OBJECT_LANGUAGE_EXHAUSTION_ATTEMPT.csv:EXH1107_6_verdict",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "NHG1896_4_verdict",
            "required_clause": "no-Hom source-weight zero theorem",
            "current_status": "NOHOM_CLAIM_BLOCKED",
            "if_pass": "Delta_w source components become theorem-zero subject to projection/readout gates",
            "if_fail": "finite Delta_w basis is the honest branch",
            "source_anchor": "NHG1896_0_parent_sort_derivation through NHG1896_3_exhaustion_stability",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def deltaw_basis_rows() -> list[dict[str, Any]]:
    return [
        {
            "basis_id": "DWB1896_0_vector_space",
            "component": "Delta_w_vector_space",
            "definition": "finite source-weight residual vector after removing the universal common calibration mode",
            "basis_formula": "Delta_w = P_perp w, with P_perp u_common=0; component norm ||Delta_w||_1 or declared arena norm before scoring",
            "source_anchor": "P8_Y5_PARENT_QLOC_1888_FINITE_DELTAW_VECTOR_ROW_INTAKE.csv:FDV1888_0_core_vector; P8_Y5_PARENT_QLOC_1891_DELTAW_SPECIES_COEFFICIENT_ROW_NONCLAIM.csv:DWS1891_1_common_mode_projector",
            "current_status": "BASIS_SCHEMA_NONCLAIM_PARENT_COMPONENT_VALUES_MISSING",
            "missing_for_claim": "parent coefficient vector, composition weights p_A, norm choice, no-cancellation policy, source path",
            "units": "dimensionless",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "DWB1896_1_preaction_species",
            "component": "Delta_w_species",
            "definition": "relative pre-variation species/action/source prefactor w_A/w_B after common-mode subtraction",
            "basis_formula": "w_A=w_common(1+epsilon_A), sum_A p_A epsilon_A=0",
            "source_anchor": "P8_Y5_PARENT_QLOC_1889_REAL_DELTAW_COMPONENT_BASIS_ACQUISITION.csv:CB1889_1_pre_action_species_prefactor; P8_Y5_PARENT_QLOC_1891_DELTAW_SPECIES_COEFFICIENT_ROW_NONCLAIM.csv:DWS1891_0_delta_w_species_coefficient_slot",
            "current_status": "LIVE_COUNTERMODEL_COMPONENT_SYMBOLIC_ONLY",
            "missing_for_claim": "parent epsilon_A vector or no-Hom theorem-zero",
            "units": "dimensionless",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "DWB1896_2_current_rescale",
            "component": "c_A_current_rescale",
            "definition": "post-variation species/source current rescale J_A -> c_A J_A",
            "basis_formula": "Delta J_src = sum_A (c_A-c_common) J_A",
            "source_anchor": "P8_Y5_PARENT_QLOC_1889_REAL_DELTAW_COMPONENT_BASIS_ACQUISITION.csv:CB1889_2_post_variation_current_rescale",
            "current_status": "CURRENT_OWNER_MISSING_NONCLAIM",
            "missing_for_claim": "source-current owner/no-rescale theorem or coefficient row",
            "units": "dimensionless",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "DWB1896_3_marker_spurion",
            "component": "Delta_w_marker_hidden",
            "definition": "hidden invariant, material marker, boundary/domain class, or readout mask that reweights source strength",
            "basis_formula": "w_A=w_common[1+epsilon_marker I_marker(A,D,boundary,readout)]",
            "source_anchor": "P8_Y5_PARENT_QLOC_1889_REAL_DELTAW_COMPONENT_BASIS_ACQUISITION.csv:CB1889_3_hidden_marker_spurion; P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv:ISO1051_3_domain_marker",
            "current_status": "NO_MARKER_THEOREM_UNSIGNED_NONCLAIM",
            "missing_for_claim": "no-marker/no-hidden-visible theorem or finite marker coefficient bounds",
            "units": "dimensionless",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "DWB1896_4_nonhilbert_current",
            "component": "J_NH_retained",
            "definition": "non-Hilbert, boundary, exchange, memory, range, connection, spin/torsion, or improvement current bypassing Hilbert source",
            "basis_formula": "J_src=kappa_univ T_Hilbert + J_NH_retained",
            "source_anchor": "P8_Y5_PARENT_QLOC_1889_REAL_DELTAW_COMPONENT_BASIS_ACQUISITION.csv:CB1889_4_nonHilbert_current",
            "current_status": "OPEN_PARALLEL_GATE_NONCLAIM",
            "missing_for_claim": "formula-level K_owner and q_retained zero proof or finite coefficient row",
            "units": "declared by current channel",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "DWB1896_5_mass_projector",
            "component": "Delta_mu_projector",
            "definition": "measured-GM/orbital mass projector, exchange, boundary, anomaly, or Gauss calibration residual",
            "basis_formula": "Delta mu_obs = Pi_M(J_Hilbert+J_exchange+J_boundary)-Pi_M(J_Hilbert)",
            "source_anchor": "P8_Y5_PARENT_QLOC_1889_REAL_DELTAW_COMPONENT_BASIS_ACQUISITION.csv:CB1889_5_mass_projector_flux",
            "current_status": "PROJECTED_FLUX_OPEN_NONCLAIM",
            "missing_for_claim": "closed calibrated mass projector or finite Delta_mu row",
            "units": "dimensionless or declared GM units",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "DWB1896_6_no_cancellation_policy",
            "component": "basis_policy",
            "definition": "multi-component scores use a no-cancellation envelope unless a parent identity proves signed cancellation",
            "basis_formula": "observable_bound uses sum_i |K_i Delta_w_i| or declared covariance envelope; no fitted cancellations",
            "source_anchor": "P8_Y5_PARENT_QLOC_1887_FINITE_SOURCE_WEIGHT_VECTOR_INTAKE_CONTRACT.csv:FSV1887_8_product_law",
            "current_status": "POLICY_WRITTEN_NONCLAIM",
            "missing_for_claim": "arena K/tau/material projections and parent coefficient values",
            "units": "policy",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY1896_0_nohom_unsigned", "nohom_parent_signed": False, "uses_syntax_decree": False, "basis_has_parent_values": False, "uses_cancellation": False, "score_attempt": False, "expected_status": "REFUSED_NOHOM_NOT_PARENT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY1896_1_syntax_decree", "nohom_parent_signed": False, "uses_syntax_decree": True, "basis_has_parent_values": False, "uses_cancellation": False, "score_attempt": False, "expected_status": "REFUSED_SYNTAX_BY_DECREE", "valid_for_claim": False},
        {"case_id": "DRY1896_2_basis_no_values", "nohom_parent_signed": True, "uses_syntax_decree": False, "basis_has_parent_values": False, "uses_cancellation": False, "score_attempt": False, "expected_status": "REFUSED_PARENT_DELTAAW_VALUES_MISSING", "valid_for_claim": False},
        {"case_id": "DRY1896_3_cancellation", "nohom_parent_signed": True, "uses_syntax_decree": False, "basis_has_parent_values": True, "uses_cancellation": True, "score_attempt": False, "expected_status": "REFUSED_CANCELLATION_ONLY", "valid_for_claim": False},
        {"case_id": "DRY1896_4_score_symbolic", "nohom_parent_signed": False, "uses_syntax_decree": False, "basis_has_parent_values": False, "uses_cancellation": False, "score_attempt": True, "expected_status": "REFUSED_SYMBOLIC_BASIS_NOT_SCORE_READY", "valid_for_claim": False},
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    nohom_signed = bool_string(row["nohom_parent_signed"]) == "true"
    syntax_decree = bool_string(row["uses_syntax_decree"]) == "true"
    has_values = bool_string(row["basis_has_parent_values"]) == "true"
    cancellation = bool_string(row["uses_cancellation"]) == "true"
    score_attempt = bool_string(row["score_attempt"]) == "true"

    if syntax_decree:
        status = "REFUSED_SYNTAX_BY_DECREE"
    elif score_attempt and not has_values:
        status = "REFUSED_SYMBOLIC_BASIS_NOT_SCORE_READY"
    elif not nohom_signed:
        status = "REFUSED_NOHOM_NOT_PARENT_DERIVED"
    elif not has_values:
        status = "REFUSED_PARENT_DELTAAW_VALUES_MISSING"
    elif cancellation:
        status = "REFUSED_CANCELLATION_ONLY"
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
        {"gate_id": "CG1896_0_nohom", "condition": "parent no-Hom theorem is signed", "current_status": "FAIL_PARENT_SORT_DISJOINTNESS_NOHOM_NOT_DERIVED", "source_anchor": "P8_Y5_PARENT_QLOC_1896_PARENT_SORT_DISJOINTNESS_NOHOM_ATTEMPT.csv:NH1896_5_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1896_1_deltaw_values", "condition": "finite Delta_w basis has parent coefficient values or theorem-zero rows", "current_status": "FAIL_BASIS_SCHEMA_NONCLAIM_PARENT_COMPONENT_VALUES_MISSING", "source_anchor": "P8_Y5_PARENT_QLOC_1896_FINITE_DELTAW_COMPONENT_BASIS_NONCLAIM.csv:DWB1896_0_vector_space", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1896_2_projection", "condition": "arena projection/tau/material kernels are sourced before scoring", "current_status": "FAIL_PROJECTION_KERNELS_NOT_READY", "source_anchor": "P8_Y5_PARENT_QLOC_1888_FINITE_DELTAW_VECTOR_ROW_INTAKE.csv:FDV1888_2_WEP_MICROSCOPE;FDV1888_3_R10", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1896_3_verdict", "condition": "source-weight zero or finite Delta_w branch can claim pass", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG1896_0_nohom through CG1896_2_projection", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC1896_0_nohom", "decision": "do not promote no-Hom theorem", "reason": "typed/product proof is exact conditionally but parent sort derivation and stability gates remain unsigned", "status": "NOHOM_ROUTE_SHARP_BUT_UNSIGNED", "next_dependency": "derive parent sort grammar or action-scale/readout stability", "valid_for_claim": False},
        {"decision_id": "DEC1896_1_basis", "decision": "finite Delta_w basis is now staged as the honest fallback", "reason": "components, common-mode projector, and no-cancellation policy are explicit but have no parent values", "status": "FINITE_DELTAW_BASIS_STAGED_NONCLAIM", "next_dependency": "source parent coefficient values or build arena projection kernels", "valid_for_claim": False},
        {"decision_id": "DEC1896_2_next", "decision": "attack action-scale/readout stability next", "reason": "even a clean no-Hom tree theorem is not claim-grade if w_A can return through measure/readout", "status": "NEXT_TARGET_SELECTED", "next_dependency": "1897 action-scale/readout stability or Delta_w projection matrix", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1896_0_primary",
            "selection_status": "selected",
            "target_doc": "1897-Y5-R2FR-action-scale-readout-stability-or-deltaw-projection-matrix.md",
            "target_script": "scripts/Y5_R2FR_action_scale_readout_stability_or_deltaw_projection_matrix_1897.py",
            "objective": "try to prove one action-scale/measure/readout owner prevents source weights from returning after tree-level no-Hom; if it fails, build the Delta_w arena projection matrix as nonclaim",
            "success_condition": "parent-signed action-scale/readout stability, or nonclaim Delta_w projection matrix rows with all tau/K/material/source dependencies explicit",
            "do_not": "do not claim source-weight zero from a tree-level grammar alone, do not score symbolic Delta_w rows, and do not allow cancellation-only passes",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT1896_0_nohom", "area": "source coupling theorem", "summary": "the no-Hom target is now exact but still parent-unsigned", "risk_level": "NARROW_PARENT_GRAMMAR_GAP", "project_meaning": "the coupling problem is reduced to a parent sort/grammar plus stability theorem", "next_action": "derive action-scale/readout stability or parent sort grammar", "valid_for_claim": False},
        {"status_id": "STAT1896_1_finite_branch", "area": "finite residual testing", "summary": "Delta_w finite basis is explicit enough for future projection matrices but has no parent coefficient values", "risk_level": "TEST_BRANCH_STRUCTURED_NOT_NUMERIC", "project_meaning": "if derivation fails, the empirical branch is no longer amorphous", "next_action": "build projection matrix or source coefficients", "valid_for_claim": False},
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    return {
        "source_register": source_register_rows(),
        "nohom_attempt": nohom_attempt_rows(),
        "nohom_gate": nohom_gate_rows(),
        "deltaw_basis": deltaw_basis_rows(),
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
    markers = ["MISSING", "UNSIGNED", "NOT_DERIVED", "NOT_PARENT", "BLOCKED", "FAIL", "COUNTER", "SYMBOLIC", "NONCLAIM", "CLAIM_BLOCKED"]
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
    checks.append({"validation_id": "VAL1896_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL", "detail": "all source paths exist and needles found", "valid_for_claim": False})
    nohom_rows = csv_rows(OUTPUTS["nohom_attempt"])
    checks.append({"validation_id": "VAL1896_01_nohom_verdict", "status": "PASS" if any(row["attempt_id"] == "NH1896_5_verdict" and row["status"] == "PARENT_SORT_DISJOINTNESS_NOHOM_NOT_DERIVED" for row in nohom_rows) else "FAIL", "detail": "no-Hom theorem remains unsigned", "valid_for_claim": False})
    basis_rows = csv_rows(OUTPUTS["deltaw_basis"])
    checks.append({"validation_id": "VAL1896_02_deltaw_basis", "status": "PASS" if len(basis_rows) >= 7 and all(row["score_ready"] == "False" and row["valid_prediction_row"] == "False" for row in basis_rows) else "FAIL", "detail": "finite Delta_w basis rows are nonclaim/not score-ready", "valid_for_claim": False})
    dry_rows = csv_rows(OUTPUTS["dryrun_results"])
    checks.append({"validation_id": "VAL1896_03_dryrun", "status": "PASS" if all(row["status_match"] == "True" and row["claim_allowed"] == "False" for row in dry_rows) else "FAIL", "detail": "dry-run refuses unsigned no-Hom, syntax decree, missing values, cancellation, and symbolic scoring", "valid_for_claim": False})
    gate_rows = csv_rows(OUTPUTS["claim_gate"])
    checks.append({"validation_id": "VAL1896_04_claim_gate", "status": "PASS" if any(row["gate_id"] == "CG1896_3_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in gate_rows) else "FAIL", "detail": "claim remains blocked", "valid_for_claim": False})
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append({"validation_id": "VAL1896_05_next_target", "status": "PASS" if any(row["route_id"] == "NEXT1896_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL", "detail": "1897 target selected", "valid_for_claim": False})
    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append({"validation_id": "VAL1896_06_claim_flags_false", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})
    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append({"validation_id": "VAL1896_07_blocked_markers_not_ready", "status": "PASS" if blocked_ok else "FAIL", "detail": blocked_detail, "valid_for_claim": False})
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1896_08_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})
    checks.append({"validation_id": "VAL1896_09_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1896_10_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})
    formalization_hits = list(FORMALIZATION.rglob("*1896*")) if FORMALIZATION.exists() else []
    checks.append({"validation_id": "VAL1896_11_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1896_count={len(formalization_hits)}", "valid_for_claim": False})
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1896_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1896 parent sort disjointness no-Hom proof or finite Delta_w basis", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1896 - Parent Sort Disjointness No-Hom Proof Or Finite Delta_w Basis

## Purpose

This checkpoint tries to derive `Hom(SpeciesLabel, Coeff_active_source)=empty`. If that no-Hom theorem remains unsigned, it builds the finite `Delta_w` component basis needed for later nonclaim projection work.

## Result

- The no-Hom proof is exact if the parent grammar/product-category sequester is signed.
- The current corpus still does not derive the parent sort grammar, hidden/marker no-Hom, coefficient exhaustion, or readout/measure stability.
- The finite `Delta_w` basis is now explicit: common-mode projector, species prefactor, current rescale, marker spurion, non-Hilbert current, mass-projector residual, and no-cancellation policy.
- No component is score-ready and no local-GR/WEP/R10 claim is made.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## No-Hom Attempt

{markdown_table(rows_by_name["nohom_attempt"])}

## No-Hom Gate

{markdown_table(rows_by_name["nohom_gate"])}

## Finite Delta_w Component Basis

{markdown_table(rows_by_name["deltaw_basis"])}

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

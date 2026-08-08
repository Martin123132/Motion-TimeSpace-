from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2650"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2650-Y5-R2FR-no-source-prefactor-object-language-proof-or-parent-material-tensor-basis.md"

CHECKPOINT = "2650"
BRANCH_ID = "Y5_R2FR_NO_SOURCE_PREF_OBJECTLANG_OR_PARENT_MATERIAL_BASIS_2650"
PREFIX = "P8_Y5_SOURCE_PREF_OBJECTLANG_2650"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "object_language_attempt": RESIDUALS / f"{PREFIX}_NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_ATTEMPT.csv",
    "typing_gate": RESIDUALS / f"{PREFIX}_SOURCE_PREFACTOR_TYPING_GATE.csv",
    "material_basis": RESIDUALS / f"{PREFIX}_PARENT_MATERIAL_TENSOR_BASIS_NONCLAIM.csv",
    "dryrun_cases": RESIDUALS / f"{PREFIX}_OBJECT_LANGUAGE_MATERIAL_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / f"{PREFIX}_OBJECT_LANGUAGE_MATERIAL_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2650_SOURCE_PREF_TYPING_AND_MATERIAL_BASIS_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "source_prefactor_material_basis_2650_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "PARENT_MATERIAL_TENSOR_BASIS_2650_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2650_SOURCE_PREF_MATERIAL_BASIS_NONCLAIM.csv",
    "quarantine": QUARANTINE / "P8_Y5_2650_OBJECT_LANGUAGE_MATERIAL_DRYRUN_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2649_doc": {
        "path": ROOT / "2649-Y5-R2FR-source-domain-quotient-constructor-or-WEP-material-tensor-intake.md",
        "needles": ["QSRC2649_3_no_prefactor_bypass", "WMI2649_3_full_parent_tensor", "VAL2649_OVERALL"],
        "role": "q_src handoff and WEP material-intake blocker",
    },
    "2645_doc": {
        "path": ROOT / "2645-Y5-R2FR-no-source-prefactor-parent-action-clause-or-first-JH-DqZ-component-row.md",
        "needles": ["NSP2645_5_pre_action_countermodel", "NSP2645_7_verdict"],
        "role": "pre-action w_A countermodel and Delta_w_species component",
    },
    "2646_doc": {
        "path": ROOT / "2646-Y5-R2FR-matter-normalization-owner-or-Delta-w-species-coefficient-source-row.md",
        "needles": ["MNO2646_2_natural_nohom_route", "MNO2646_6_verdict", "DWS2646_0_delta_w_species"],
        "role": "matter-normalization owner and no-Hom route",
    },
    "2647_doc": {
        "path": ROOT / "2647-Y5-R2FR-ordinary-matter-action-signature-or-Delta-w-projection-kernels.md",
        "needles": ["OMC2647_4_source_functor_label_forgetting", "OMC2647_7_verdict"],
        "role": "ordinary matter action signature and source-label forgetting gate",
    },
    "1066_doc": {
        "path": ROOT / "1066-Y5-R10-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width.md",
        "needles": ["SSE1066_5_verdict", "OLT1066_6_verdict", "TWP1066_7_verdict"],
        "role": "source scalar exclusion and WEP tau projection contract",
    },
    "1080_doc": {
        "path": ROOT / "1080-Y5-R10-finite-WEP-source-vector-and-material-tensor-acquisition-pack.md",
        "needles": ["MAT1080_4_full_tensor_upgrade", "BOUND1080_0_MICROSCOPE_WEP_source_charge"],
        "role": "finite WEP source-vector/material tensor acquisition context",
    },
    "1225_doc": {
        "path": ROOT / "1225-Y5-R10-tau-WEP-source-worldtube-readout-projection.md",
        "needles": ["ACQ1225_0_official_readout_arrays", "ACQ1225_4_material_tensor", "VAL1225_4_acquisition_table_complete"],
        "role": "tau_WEP source-worldtube/readout missing-source ledger",
    },
    "1895_doc": {
        "path": ROOT / "1895-Y5-R2FR-no-source-prefactor-object-language-proof-or-parent-material-tensor-basis.md",
        "needles": ["NSP1895_5_verdict", "PMTB1895_4_acceptance", "VAL1895_OVERALL"],
        "role": "older branch analogue for object-language/material-basis route",
    },
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in list(OUTPUTS.values()) + list(BRANCH_COPIES.values()) + [DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    header = "| " + " | ".join(fieldnames) + " |"
    separator = "| " + " | ".join("---" for _ in fieldnames) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fieldnames]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    timestamp = generated_utc()
    for source_id, spec in SOURCE_SPECS.items():
        path = Path(spec["path"])
        text = read_text(path)
        missing_needles = [needle for needle in spec["needles"] if needle not in text]
        exists = path.exists()
        rows.append(
            {
                "source_id": f"SRC2650_{source_id}",
                "role": spec["role"],
                "path": str(path),
                "exists": exists,
                "needles_required": len(spec["needles"]),
                "missing_needles": "; ".join(missing_needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing_needles else "MISSING_SOURCE_OR_NEEDLE",
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def object_language_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NSP2650_0_target",
            "clause": "source-only prefactor object-language exclusion",
            "attempted_statement": "NoSourceOnlySpeciesSlot: a relative w_A is not an allowed parent object before Hilbert/coframe variation unless it is an owned ordinary matter parameter inside S_A or a universal common calibration scalar.",
            "status": "TARGET_SHARP",
            "what_it_would_kill": "the pre-action w_A S_A bypass that defeated q_src in 2649",
            "source_anchor": "2649:QSRC2649_3_no_prefactor_bypass;2645:NSP2645_5_pre_action_countermodel",
            "signed_by_parent": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "NSP2650_1_exact_if_grammar_signed",
            "clause": "typed exclusion theorem",
            "attempted_statement": "If the parent grammar has no morphism SpeciesLabel/material marker/readout label -> Coeff_active_source, variation precedes readout, and the action-density line is common, then relative source-only w_A S_A is ill-typed.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "what_it_would_kill": "Delta_w_species theorem-zero on the source-prefactor branch",
            "source_anchor": "2646:MNO2646_2_natural_nohom_route;1066:OLT1066_6_verdict;1895:NSP1895_1_exact_if_typed",
            "signed_by_parent": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "NSP2650_2_current_parent_signature_gap",
            "clause": "current MTS parent grammar derives the needed sorts",
            "attempted_statement": "The present MTS parent action derives ordinary matter fields, geometry, constants, readout maps, and source coefficients from one grammar with no extra active-source coefficient sort.",
            "status": "PARENT_TYPED_OBJECT_LANGUAGE_NOT_DERIVED",
            "what_it_would_kill": "syntax-by-decree objections",
            "source_anchor": "2647:OMC2647_7_verdict;1895:NSP1895_5_verdict",
            "signed_by_parent": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "NSP2650_3_disconnected_species_countermodel",
            "clause": "direct-sum species-family coefficient obstruction",
            "attempted_statement": "A disconnected ordinary-matter category can carry independent component scalars c_A unless the parent functor proves no natural target exists for active-source-only coefficients.",
            "status": "DIRECT_SUM_COUNTERMODEL_SURVIVES",
            "what_it_would_kill": "overconfident naturality-only proof",
            "source_anchor": "1066:SSE1066_5_verdict;1895:NSP1895_3_direct_sum_counterexample",
            "signed_by_parent": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "NSP2650_4_action_scale_measure_gap",
            "clause": "single action-density/hbar/measure owner",
            "attempted_statement": "All ordinary sectors share one parent action-density line and one measure/hbar normalization, so a relative multiplier cannot hide as a path-integral or Jacobian normalization.",
            "status": "ACTION_SCALE_MEASURE_OWNER_UNSIGNED",
            "what_it_would_kill": "classical-EOM rescaling false positive",
            "source_anchor": "2646:MNO2646_4_measure_action_density_line;1066:FMQ1066_4_verdict",
            "signed_by_parent": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "NSP2650_5_readout_radiative_gap",
            "clause": "no marker/readout/radiative return",
            "attempted_statement": "Boundary markers, local readout maps, renormalized constants, and source-worldtube projectors do not reintroduce species-dependent active-source coefficients after the grammar exclusion.",
            "status": "READOUT_RADIATIVE_CLOSURE_UNSIGNED",
            "what_it_would_kill": "post-grammar leakage into WEP/clock/PPN/local source tests",
            "source_anchor": "2645:NSP2645_6_measure_coframe_readout;1225:ACQ1225_0_official_readout_arrays",
            "signed_by_parent": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "NSP2650_6_verdict",
            "clause": "promote no-source-prefactor object-language proof",
            "attempted_statement": "NoSourceOnlySpeciesSlot follows from current MTS parent primitives without adding a closure axiom.",
            "status": "NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_PROOF_NOT_PARENT_DERIVED",
            "what_it_would_kill": "Delta_w_species theorem-zero and the q_src pre-action bypass",
            "source_anchor": "NSP2650_0_target through NSP2650_5_readout_radiative_gap",
            "signed_by_parent": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def typing_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "TYP2650_0_parent_sorts",
            "required_clause": "parent sorts are derived, not declared ad hoc",
            "pass_condition": "MatterField, GeometryObservable, OrdinaryConstant, ReadoutMap, BoundaryData, HilbertSource, and Coeff_active_source are all typed by the parent action grammar.",
            "current_status": "PARENT_SORT_DERIVATION_UNSIGNED",
            "if_passes": "source-only w_A cannot be inserted as a hidden extra argument",
            "if_fails": "syntax-by-decree objection survives",
            "source_anchor": "1895:TYP1895_0_parent_sorts;2647:OMC2647_7_verdict",
            "gate_passed": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "TYP2650_1_no_species_to_source_coeff",
            "required_clause": "Hom(SpeciesLabel, Coeff_active_source)=empty",
            "pass_condition": "No parent morphism maps species labels, alloy markers, boundary classes, or readout labels to relative active-source coefficients.",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "if_passes": "w_A has no target sort and cannot multiply S_A as source-only data",
            "if_fails": "relative source-weight countermodel survives",
            "source_anchor": "2646:MNO2646_2_natural_nohom_route;1895:TYP1895_1_no_species_to_source_coeff",
            "gate_passed": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "TYP2650_2_variation_before_readout",
            "required_clause": "Hilbert/coframe source is taken from the total action before material/readout projection",
            "pass_condition": "J_H = delta S_matter / delta e_obs is computed before WEP, clock, PPN, source-worldtube, or material basis readout maps.",
            "current_status": "CONDITIONAL_MATH_CLEAN_NOT_PARENT_COMPLETE",
            "if_passes": "bookkeeping labels cannot become coupling selectors after variation",
            "if_fails": "post-variation current rescale remains legal",
            "source_anchor": "2649:QG2649_1_total_hilbert_source;2647:OMC2647_4_source_functor_label_forgetting",
            "gate_passed": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "TYP2650_3_action_scale_measure",
            "required_clause": "one action-scale/hbar/measure owner covers all ordinary sectors",
            "pass_condition": "Relative species action multipliers are neither independent quantum normalizations nor hidden measure/Jacobian factors.",
            "current_status": "ACTION_SCALE_OWNER_UNSIGNED",
            "if_passes": "classical-EOM rescaling false positive is removed",
            "if_fails": "w_A can hide as action-scale/measure debt",
            "source_anchor": "1066:FMQ1066_3_measure_jacobian;2646:MNO2646_4_measure_action_density_line",
            "gate_passed": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "TYP2650_4_no_marker_readout_return",
            "required_clause": "markers/projectors/readout maps cannot return source-only coefficients",
            "pass_condition": "Boundary, material, source-worldtube, clock and local readout projectors commute with source extraction without label-dependent active-source scalars.",
            "current_status": "READOUT_RADIATIVE_CLOSURE_UNSIGNED",
            "if_passes": "local/WEP test branches inherit the source-prefactor zero",
            "if_fails": "arena-specific finite residuals must be carried",
            "source_anchor": "1225:ACQ1225_0_official_readout_arrays;2649:QG2649_4_projected_mass",
            "gate_passed": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "TYP2650_5_verdict",
            "required_clause": "NoSourceOnlySpeciesSlot is a parent theorem",
            "pass_condition": "TYP2650_0 through TYP2650_4 all pass.",
            "current_status": "NO_SOURCE_PREFACTOR_TYPING_CLAIM_BLOCKED",
            "if_passes": "Delta_w_species theorem-zero branch opens",
            "if_fails": "finite Delta_w/material tensor branch remains required",
            "source_anchor": "TYP2650_0_parent_sorts through TYP2650_4_no_marker_readout_return",
            "gate_passed": False,
            "claim_allowed": False,
        },
    ]


def material_basis_rows() -> list[dict[str, Any]]:
    return [
        {
            "basis_id": "PMTB2650_0_parent_basis_owner",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "parent material response basis X",
            "definition": "A finite parent-owned basis of response generators X shared by C_parent_X, R_material_X, R_source_X and tau_eff_X.",
            "current_status": "MISSING_PARENT_RESPONSE_BASIS",
            "source_anchor": "2649:WMI2649_3_full_parent_tensor;1895:PMTB1895_0_parent_basis_target",
            "missing_for_claim": "parent generator list, units, signs, no-double-counting rule, and coefficient owner",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "PMTB2650_1_mass_functional",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "mass/source response functional",
            "definition": "R_material_X(A,B)=partial_X ln M_A - partial_X ln M_B after common-mode, rest-mass, calibration, and double-counted source pieces are projected out.",
            "current_status": "FORMULA_STUB_PARENT_FUNCTIONAL_MISSING",
            "source_anchor": "1080:MAT1080_4_full_tensor_upgrade;1895:PMTB1895_3_tensor_formula",
            "missing_for_claim": "M_A functional, binding decomposition, isotope/alloy averaging, source normalization and X-basis units",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "PMTB2650_2_no_double_counting",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "ordinary constants versus active-source coefficients",
            "definition": "Mass, charge, binding and EM constants may enter ordinary matter spectra, but a second active-source multiplier for the same data is disallowed unless retained as Delta_w_species.",
            "current_status": "NO_DOUBLE_COUNTING_RULE_CONDITIONAL",
            "source_anchor": "2646:MNO2646_3_constant_owner_separation;1066:OLT1066_4_inert_source_scalar",
            "missing_for_claim": "parent-signed owner map separating representation constants from active-source coefficients",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "PMTB2650_3_TA6V_PtRh10_context",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "source-backed composition context",
            "definition": "TA6V and PtRh10 composition context can seed future material tensor components but is not a parent-basis tensor by itself.",
            "current_status": "SOURCE_BACKED_CONTEXT_ONLY",
            "source_anchor": "2649:WMI2649_0_pair_context;1080:MAT1080_0_PtRh10_MICROSCOPE;MAT1080_1_TA6V_MICROSCOPE",
            "missing_for_claim": "isotope/alloy averaging and parent basis response map",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "PMTB2650_4_proxy_quarantine",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "proxy material vectors",
            "definition": "Z/A, neutron-excess, electron-mass and alpha/Coulomb smoke vectors remain context/proxy rows only, not parent tensors.",
            "current_status": "PROXY_CONTEXT_NOT_PARENT_TENSOR",
            "source_anchor": "1080:MAT1080_4_full_tensor_upgrade;1895:PMTB1895_2_proxy_inventory",
            "missing_for_claim": "proof that proxies span the allowed parent response space, with units/signs and no-double-counting",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "PMTB2650_5_tau_readout_source_dependency",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "tau/readout/source product dependency",
            "definition": "eta_AB needs parent coefficient vector x material tensor x tau/source-worldtube/readout kernel in one convention.",
            "current_status": "TAU_READOUT_SOURCE_PRODUCT_NOT_FILLED",
            "source_anchor": "1225:ACQ1225_0_official_readout_arrays;ACQ1225_4_material_tensor;2649:WMI2649_5_tau_readout_dependency",
            "missing_for_claim": "official readout arrays, source-worldtube weighting, orbit average, product convention and tau_eff",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "PMTB2650_6_acceptance",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "parent material tensor basis acceptance",
            "definition": "The material-basis fallback is claim-ready only when parent X, R_material_X, coefficient vector, tau/readout kernel and no-cancellation convention are all filled.",
            "current_status": "PARENT_MATERIAL_TENSOR_BASIS_BLOCKED_NONCLAIM",
            "source_anchor": "PMTB2650_0 through PMTB2650_5",
            "missing_for_claim": "all parent basis, material, coefficient, tau/readout and source normalization legs",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "DRY2650_0_current_unsigned",
            "typed_parent_signature_signed": False,
            "uses_syntax_by_decree": False,
            "action_scale_owner_signed": False,
            "material_basis_level": "missing",
            "uses_proxy_as_tensor": False,
            "tau_readout_filled": False,
            "expected_status": "REFUSED_OBJECT_LANGUAGE_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY2650_1_syntax_by_decree",
            "typed_parent_signature_signed": False,
            "uses_syntax_by_decree": True,
            "action_scale_owner_signed": False,
            "material_basis_level": "missing",
            "uses_proxy_as_tensor": False,
            "tau_readout_filled": False,
            "expected_status": "REFUSED_SYNTAX_BY_DECREE",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY2650_2_action_scale_missing",
            "typed_parent_signature_signed": True,
            "uses_syntax_by_decree": False,
            "action_scale_owner_signed": False,
            "material_basis_level": "missing",
            "uses_proxy_as_tensor": False,
            "tau_readout_filled": False,
            "expected_status": "REFUSED_ACTION_SCALE_MEASURE_OWNER_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY2650_3_material_basis_missing",
            "typed_parent_signature_signed": True,
            "uses_syntax_by_decree": False,
            "action_scale_owner_signed": True,
            "material_basis_level": "missing",
            "uses_proxy_as_tensor": False,
            "tau_readout_filled": False,
            "expected_status": "REFUSED_PARENT_MATERIAL_RESPONSE_BASIS_MISSING",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY2650_4_proxy_as_tensor",
            "typed_parent_signature_signed": True,
            "uses_syntax_by_decree": False,
            "action_scale_owner_signed": True,
            "material_basis_level": "proxy",
            "uses_proxy_as_tensor": True,
            "tau_readout_filled": False,
            "expected_status": "REFUSED_PROXY_VECTOR_NOT_PARENT_TENSOR",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY2650_5_tau_readout_missing",
            "typed_parent_signature_signed": True,
            "uses_syntax_by_decree": False,
            "action_scale_owner_signed": True,
            "material_basis_level": "parent_basis_symbolic",
            "uses_proxy_as_tensor": False,
            "tau_readout_filled": False,
            "expected_status": "REFUSED_TAU_READOUT_SOURCE_PRODUCT_NOT_FILLED",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY2650_6_counterfactual_full_package",
            "typed_parent_signature_signed": True,
            "uses_syntax_by_decree": False,
            "action_scale_owner_signed": True,
            "material_basis_level": "full_parent_basis",
            "uses_proxy_as_tensor": False,
            "tau_readout_filled": True,
            "expected_status": "COUNTERFACTUAL_CONTRACT_READY_NOT_CURRENT_CLAIM",
            "valid_for_claim": False,
        },
    ]


def evaluate_dryrun_case(row: dict[str, Any]) -> str:
    if bool(row["uses_syntax_by_decree"]):
        return "REFUSED_SYNTAX_BY_DECREE"
    if not bool(row["typed_parent_signature_signed"]):
        return "REFUSED_OBJECT_LANGUAGE_UNSIGNED"
    if not bool(row["action_scale_owner_signed"]):
        return "REFUSED_ACTION_SCALE_MEASURE_OWNER_UNSIGNED"
    if str(row["material_basis_level"]) == "missing":
        return "REFUSED_PARENT_MATERIAL_RESPONSE_BASIS_MISSING"
    if bool(row["uses_proxy_as_tensor"]):
        return "REFUSED_PROXY_VECTOR_NOT_PARENT_TENSOR"
    if not bool(row["tau_readout_filled"]):
        return "REFUSED_TAU_READOUT_SOURCE_PRODUCT_NOT_FILLED"
    return "COUNTERFACTUAL_CONTRACT_READY_NOT_CURRENT_CLAIM"


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    timestamp = generated_utc()
    for case in cases:
        actual_status = evaluate_dryrun_case(case)
        rows.append(
            {
                "case_id": case["case_id"],
                "expected_status": case["expected_status"],
                "actual_status": actual_status,
                "matched_expected": actual_status == case["expected_status"],
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2650_0_object_language",
            "gate": "parent typed object language excludes source-only prefactor objects",
            "current_status": "FAIL_NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_PROOF_NOT_PARENT_DERIVED",
            "source_anchor": f"{OUTPUTS['object_language_attempt'].name}:NSP2650_6_verdict",
            "gate_passed": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2650_1_action_scale_measure",
            "gate": "action-scale/measure/readout owner prevents relative w_A returning outside syntax",
            "current_status": "FAIL_ACTION_SCALE_MEASURE_READOUT_UNSIGNED",
            "source_anchor": f"{OUTPUTS['object_language_attempt'].name}:NSP2650_4_action_scale_measure_gap;NSP2650_5_readout_radiative_gap",
            "gate_passed": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2650_2_material_basis",
            "gate": "WEP parent material tensor basis is constructed and not proxy-only",
            "current_status": "FAIL_PARENT_MATERIAL_TENSOR_BASIS_BLOCKED_NONCLAIM",
            "source_anchor": f"{OUTPUTS['material_basis'].name}:PMTB2650_6_acceptance",
            "gate_passed": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2650_3_tau_readout",
            "gate": "tau/source-worldtube/readout product is filled in same convention as material tensor",
            "current_status": "FAIL_TAU_READOUT_SOURCE_PRODUCT_NOT_FILLED",
            "source_anchor": f"{OUTPUTS['material_basis'].name}:PMTB2650_5_tau_readout_source_dependency",
            "gate_passed": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2650_4_verdict",
            "gate": "source prefactor zero or WEP material score is claim-ready",
            "current_status": "CLAIM_BLOCKED",
            "source_anchor": "CG2650_0_object_language through CG2650_3_tau_readout",
            "gate_passed": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2650_0_typing",
            "decision": "OBJECT_LANGUAGE_ROUTE_SHARP_BUT_UNSIGNED",
            "reason": "The proof is clean only after parent sort disjointness/no-Hom, action-scale owner, and no readout/radiative return are signed together.",
            "action": "do not set Delta_w_species=0 from syntax alone",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2650_1_material",
            "decision": "PARENT_MATERIAL_BASIS_SKELETON_NONCLAIM",
            "reason": "Composition/proxy context exists, but the parent response basis, tensor functional, coefficient vector and tau/readout product are not instantiated.",
            "action": "preserve finite empirical route without scoring proxy rows",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2650_2_no_more_free_circling",
            "decision": "NEXT_ROUTE_MUST_EITHER_PROVE_NOHOM_OR_BUILD_FINITE_BASIS",
            "reason": "The same gap is now localized: Hom(SpeciesLabel,Coeff_active_source)=empty plus action-scale owner, or finite Delta_w/material basis acquisition.",
            "action": "2651 should be a hard fork: prove the no-Hom constructor or begin finite Delta_w basis rows.",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2650_0_selected",
            "status": "selected",
            "next_doc": "2651-Y5-R2FR-parent-sort-nohom-constructor-or-finite-Delta-w-basis.md",
            "next_script": "scripts/Y5_R2FR_parent_sort_nohom_constructor_or_finite_Delta_w_basis_2651.py",
            "target": "Try to derive Hom(SpeciesLabel,Coeff_active_source)=empty from the parent sort constructor; if it fails, stop trying to erase Delta_w_species and build the finite Delta_w component/material basis needed for WEP/R10/PPN scoring.",
            "must_include": "parent sort constructor; no-Hom theorem; action-density owner dependency; finite Delta_w basis; common-mode projector; no-cancellation norm; material/tau/readout requirements",
            "must_exclude": "syntax-by-decree, Ward-only proof, proxy tensor scoring, MICROSCOPE bound as prediction, tau=1 shortcut, local-GR/WEP claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT2650_0_coupling_gap",
            "sector": "source coupling / object language",
            "finding": "the coupling gap is no longer vague: it is a typed no-Hom/action-scale/readout closure package",
            "status": "NARROW_BUT_UNSIGNED",
            "meaning": "this is progress, not a pass; the exact theorem target is now visible",
            "next_action": "prove no-Hom from parent sorts or retain finite Delta_w branch",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT2650_1_WEP_fallback",
            "sector": "WEP/local empirical fallback",
            "finding": "material tensor path is protected from proxy shortcuts and bound-as-prediction mistakes",
            "status": "EMPIRICAL_ROUTE_NOT_SCORE_READY",
            "meaning": "testing can proceed later only after parent material basis and tau/readout/source product are filled",
            "next_action": "build finite basis rows rather than use Z/A toys as claims",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT2650_2_overall",
            "sector": "MTS GR/Newton reduction programme",
            "finding": "source universality is still the main local-GR bridge debt",
            "status": "DERIVATION_TARGET_LOCALIZED",
            "meaning": "the route is hard but crisp: either source universality is a parent theorem or it becomes a finite residual to bound",
            "next_action": "2651 hard fork",
            "valid_for_claim": False,
        },
    ]


def branch_copy_rows(material_rows: list[dict[str, Any]], dryrun_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    write_csv(BRANCH_COPIES["queue"], material_rows)
    write_csv(BRANCH_COPIES["local_bounds"], material_rows)
    write_csv(BRANCH_COPIES["source_weight"], material_rows)
    write_csv(BRANCH_COPIES["microscope"], material_rows)
    write_csv(BRANCH_COPIES["quarantine"], dryrun_rows)
    rows: list[dict[str, Any]] = []
    for copy_id, path in BRANCH_COPIES.items():
        rows.append(
            {
                "copy_id": copy_id,
                "path": str(path),
                "exists": path.exists(),
                "parseable_csv": path.exists() and len(csv_rows(path)) >= 1,
                "purpose": "2650 object-language/material-basis nonclaim handoff",
                "valid_for_claim": False,
            }
        )
    return rows


def generated_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_COPIES.values())


def all_generated_csv_parse(paths: list[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".csv":
            continue
        try:
            csv_rows(path)
        except Exception:
            return False
    return True


def formalization_hit_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = [
        "*2650-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2650*",
        "*Y5_R2FR_no_source_prefactor_object_language_proof_or_parent_material_tensor_basis_2650*",
        "*JR2650*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows_by_name["source_register"])
    object_verdict_ok = any(
        row["row_id"] == "NSP2650_6_verdict"
        and row["status"] == "NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_PROOF_NOT_PARENT_DERIVED"
        and not row["claim_allowed"]
        for row in rows_by_name["object_language_attempt"]
    )
    typing_gate_ok = any(
        row["gate_id"] == "TYP2650_5_verdict"
        and row["current_status"] == "NO_SOURCE_PREFACTOR_TYPING_CLAIM_BLOCKED"
        and not row["gate_passed"]
        for row in rows_by_name["typing_gate"]
    )
    material_basis_ok = any(
        row["basis_id"] == "PMTB2650_6_acceptance"
        and row["current_status"] == "PARENT_MATERIAL_TENSOR_BASIS_BLOCKED_NONCLAIM"
        and not row["claim_allowed"]
        for row in rows_by_name["material_basis"]
    )
    dryrun_ok = all(row["matched_expected"] and not row["claim_allowed"] for row in rows_by_name["dryrun_results"])
    claim_gates_ok = all(not row["gate_passed"] and not row["claim_allowed"] for row in rows_by_name["claim_gates"])
    decision_ok = any(row["decision_id"] == "DEC2650_2_no_more_free_circling" for row in rows_by_name["decision"])
    next_ok = any("2651-Y5-R2FR-parent-sort-nohom-constructor" in row["next_doc"] for row in rows_by_name["next_target"])
    branch_ok = all(row["exists"] and row["parseable_csv"] for row in rows_by_name["branch_copies"])
    csv_ok = all_generated_csv_parse(paths)
    formalization_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks_data = [
        ("VAL2650_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2650_01_object_language_verdict", object_verdict_ok, "object-language exclusion remains exact conditional, not parent theorem"),
        ("VAL2650_02_typing_gate", typing_gate_ok, "typing/no-Hom gate remains blocked"),
        ("VAL2650_03_material_basis", material_basis_ok, "parent material tensor basis remains nonclaim/not score-ready"),
        ("VAL2650_04_dryrun", dryrun_ok, "dry-run refuses unsigned typing, syntax decree, unsigned action scale, missing basis, proxy tensor, and tau/readout missing"),
        ("VAL2650_05_claim_gates_false", claim_gates_ok, "all claim gates remain blocked"),
        ("VAL2650_06_decision_next", decision_ok, "decision forces hard fork: prove no-Hom or build finite basis"),
        ("VAL2650_07_next_target", next_ok, "2651 next target is recorded"),
        ("VAL2650_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2650_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2650_10_formalization_untouched", formalization_ok, "no 2650 outputs are written under formalization-workbench"),
        ("VAL2650_11_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
    ]
    timestamp = generated_utc()
    for validation_id, passed, detail in checks_data:
        checks.append(
            {
                "timestamp_utc": timestamp,
                "checkpoint": CHECKPOINT,
                "branch_id": BRANCH_ID,
                "valid_for_claim": False,
                "claim_allowed": False,
                "validation_id": validation_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
            }
        )
    overall_pass = all(row["status"] == "PASS" for row in checks)
    checks.append(
        {
            "timestamp_utc": timestamp,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": "VAL2650_OVERALL",
            "status": "PASS" if overall_pass else "FAIL",
            "detail": "2650 localizes the no-source-prefactor proof to no-Hom/action-scale/readout closure, keeps material basis nonclaim, and selects the 2651 hard fork",
        }
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 2650 - No-Source-Prefactor Object-Language Proof Or Parent Material Tensor Basis

## Purpose

This checkpoint attacks the coupling gap directly: prove that a source-only `w_A` is not a legal parent object before variation. If that cannot be parent-signed, it stages the parent material tensor basis needed for WEP without turning proxy material vectors into claims.

## Result

- The proof route is exact as a conditional theorem: if the parent sort/no-Hom/action-scale/readout package is signed, `w_A S_A` is ill-typed except as common calibration or owned ordinary matter data.
- The current corpus still does not derive that whole package from MTS primitives, so `Delta_w_species` is not theorem-zero.
- The fallback testing route is preserved but nonclaim: WEP needs a parent material response basis, coefficient vector, tau/source-worldtube/readout product, and no-cancellation convention before scoring.
- The next step is deliberately not more soft circling: either prove the no-Hom constructor or build finite `Delta_w` basis rows.

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

## Claim Gates

{markdown_table(rows_by_name["claim_gates"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Branch Copies

{markdown_table(rows_by_name["branch_copies"])}

## Validation

{markdown_table(validation)}
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def build_rows() -> dict[str, list[dict[str, Any]]]:
    dryrun_cases = dryrun_case_rows()
    dryrun_results = dryrun_result_rows(dryrun_cases)
    material_rows = material_basis_rows()
    rows_by_name = {
        "source_register": source_register_rows(),
        "object_language_attempt": object_language_attempt_rows(),
        "typing_gate": typing_gate_rows(),
        "material_basis": material_rows,
        "dryrun_cases": dryrun_cases,
        "dryrun_results": dryrun_results,
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }
    rows_by_name["branch_copies"] = branch_copy_rows(material_rows, dryrun_results)
    return rows_by_name


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows_by_name = build_rows()
    for name, rows in rows_by_name.items():
        if name in OUTPUTS and name != "validation":
            write_csv(OUTPUTS[name], rows)
    paths = generated_paths()
    remove_pycache()
    rows_by_name["validation"] = validation_rows(rows_by_name, paths)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()

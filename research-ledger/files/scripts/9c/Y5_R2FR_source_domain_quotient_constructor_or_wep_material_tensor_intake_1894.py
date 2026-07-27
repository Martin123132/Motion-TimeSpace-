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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1894"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1894-Y5-R2FR-source-domain-quotient-constructor-or-wep-material-tensor-intake.md"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1893_doc": ROOT / "1893-Y5-R2FR-source-functor-label-forgetting-or-deltaw-wep-kernel-v0.md",
    "1893_validation": OUT / "P8_Y5_BRR545_1893_VALIDATION.csv",
    "1893_label_attempt": OUT / "P8_Y5_PARENT_QLOC_1893_SOURCE_FUNCTOR_LABEL_FORGETTING_ATTEMPT.csv",
    "1893_clause_audit": OUT / "P8_Y5_PARENT_QLOC_1893_LABEL_FORGETTING_CLAUSE_AUDIT.csv",
    "1893_wep_kernel": OUT / "P8_Y5_PARENT_QLOC_1893_DELTAW_WEP_KERNEL_V0_NONCLAIM.csv",
    "1893_next": OUT / "P8_Y5_PARENT_QLOC_1893_NEXT_TARGET.csv",
    "953_source_functor": OUT / "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv",
    "953_category_contract": OUT / "P8_Y5_R10_953_PARENT_CATEGORY_CONTRACT.csv",
    "954_label_attempt": OUT / "P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv",
    "954_action_clause": OUT / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
    "955_matter_lemma": OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
    "955_prefactor_class": OUT / "P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv",
    "955_schema": OUT / "P8_Y5_R10_955_RESIDUAL_INPUT_SCHEMA.csv",
    "ward_contract": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "1481_material_pack": OUT / "P8_Y5_R10_1481_WEP_MATERIAL_CONTEXT_PACK.csv",
    "1484_wep_interface": OUT / "P8_Y5_R10_1484_BRANCH_LOCKED_WEP_PRODUCT_INTERFACE.csv",
    "1080_material_candidates": OUT / "P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv",
    "983_constituents": OUT / "P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv",
    "983_proxy_vectors": OUT / "P8_Y5_R10_983_MATERIAL_PROXY_CHARGE_VECTORS.csv",
    "1424_material_vectors": OUT / "P8_Y5_R10_1424_TIPT_MATERIAL_VECTOR_CANDIDATES.csv",
    "1491_readiness": OUT / "P8_Y5_R10_1491_DELTA_W_READINESS_MATRIX.csv",
}


SOURCE_NEEDLES = {
    "1893_doc": ["SOURCE_FUNCTOR_LABEL_FORGETTING_NOT_PARENT_DERIVED", "NEXT1893_0_primary"],
    "1893_validation": ["VAL1893_OVERALL,PASS"],
    "1893_label_attempt": ["SFL1893_5_verdict", "SOURCE_FUNCTOR_LABEL_FORGETTING_NOT_PARENT_DERIVED"],
    "1893_clause_audit": ["LFA1893_0_domain_quotient", "SOURCE_LABEL_FORGETTING_NOT_DERIVED"],
    "1893_wep_kernel": ["WEPK1893_2_material_tensor", "MISSING_FULL_PARENT_MATERIAL_TENSOR"],
    "1893_next": ["NEXT1893_0_primary", "source-domain quotient"],
    "953_source_functor": ["NSF953_1_domain_fork", "NSF953_5_verdict"],
    "953_category_contract": ["PMC953_1_label_forgetting_quotient", "PMC953_5_contract_verdict"],
    "954_label_attempt": ["PLF954_0_target", "PLF954_5_verdict"],
    "954_action_clause": ["PAC954_1_no_source_prefactors", "PAC954_5_GR_source_limit_clause"],
    "955_matter_lemma": ["MMA955_3_relative_prefactor", "MMA955_6_verdict"],
    "955_prefactor_class": ["SPC955_2_relative_species_weight", "SPC955_3_hidden_marker_weight"],
    "955_schema": ["RIS955_0_epsilon_vector", "RIS955_1_composition_projection"],
    "ward_contract": ["SC3_universal_kappa_coupling", "SC6_closed_calibrated_mass_projector"],
    "1481_material_pack": ["MAT1481_6_full_tensor", "MISSING_FULL_PARENT_MATERIAL_TENSOR"],
    "1484_wep_interface": ["WPI1484_2_R_material", "MISSING_FULL_PARENT_MATERIAL_TENSOR"],
    "1080_material_candidates": ["MAT1080_4_full_tensor_upgrade", "MISSING_FULL_MATERIAL_TENSOR"],
    "983_constituents": ["M983_0_PtRh10", "M983_1_TiAlloy"],
    "983_proxy_vectors": ["proxy_charge_vector_computed"],
    "1424_material_vectors": ["MAT1424_2_electron_mass_fraction", "TOY_NOT_PARENT_DERIVED"],
    "1491_readiness": ["RDY1491_0_MICROSCOPE", "bound anchor exists"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1894_SOURCE_REGISTER.csv",
    "qsrc_constructor": OUT / "P8_Y5_PARENT_QLOC_1894_SOURCE_DOMAIN_QUOTIENT_CONSTRUCTOR_ATTEMPT.csv",
    "qsrc_clause_gate": OUT / "P8_Y5_PARENT_QLOC_1894_QSRC_CLAUSE_GATE.csv",
    "wep_material_intake": OUT / "P8_Y5_PARENT_QLOC_1894_WEP_MATERIAL_TENSOR_INTAKE_NONCLAIM.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1894_QSRC_WEP_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1894_QSRC_WEP_DRYRUN_RESULTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1894_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1894_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1894_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1894_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1894_VALIDATION.csv",
}


BRANCH_COPIES = {
    "qsrc_constructor": MICROSCOPE_RESIDUALS / OUTPUTS["qsrc_constructor"].name,
    "qsrc_clause_gate": QUEUE / "JR1894_QSRC_CLAUSE_GATE_NONCLAIM.csv",
    "wep_material_intake": SOURCE_WEIGHT_DOCS / "WEP_MATERIAL_TENSOR_INTAKE_1894_NONCLAIM.csv",
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


def qsrc_constructor_rows() -> list[dict[str, Any]]:
    return [
        {
            "constructor_id": "QSRC1894_0_definition",
            "claim_piece": "source-domain quotient object",
            "mathematical_statement": "Given a labelled finite family J_lab={(T_A,A)}, define an equivalence relation J_lab ~ J'_lab iff sum_A T_A = sum_B T'_B as the total Hilbert/coframe current on the observed frame; q_src(J_lab)=T_total",
            "status": "MATHEMATICAL_CONSTRUCTOR_WRITTEN",
            "proof_or_obstruction": "the quotient is well-defined as a mathematical map, but parent physics must still require all source couplings to factor through it",
            "source_anchor": "P8_Y5_R10_953_PARENT_CATEGORY_CONTRACT.csv:PMC953_1_label_forgetting_quotient; P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv:PLF954_0_target",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "constructor_id": "QSRC1894_1_factorization_theorem",
            "claim_piece": "unique source map after quotient",
            "mathematical_statement": "If F_src is local, covariant, additive/natural, and has domain Im(q_src), then F_src(T_total)=kappa_univ T_total up to the single calibrated common source scale",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "relative kappa_A cannot be formed once A labels are removed from the domain",
            "source_anchor": "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv:NSF953_2_conditional_uniqueness;NSF953_4_calibration_limit",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "constructor_id": "QSRC1894_2_parent_gap",
            "claim_piece": "parent adoption of q_src",
            "mathematical_statement": "The MTS parent category/action declares C_parent -> C_source to be q_src before coupling selection and gives no morphism from labels, hidden markers, or readout masks into source coefficients",
            "status": "SOURCE_DOMAIN_QUOTIENT_NOT_PARENT_SIGNED",
            "proof_or_obstruction": "current files state the exact missing clause but do not derive it from MTS primitives or one parent action grammar",
            "source_anchor": "P8_Y5_R10_953_PARENT_CATEGORY_CONTRACT.csv:PMC953_5_contract_verdict; P8_Y5_PARENT_QLOC_1893_LABEL_FORGETTING_CLAUSE_AUDIT.csv:LFA1893_0_domain_quotient",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "constructor_id": "QSRC1894_3_no_prefactor_obstruction",
            "claim_piece": "quotient bypass by legal pre-action weights",
            "mathematical_statement": "If S_matter=sum_A w_A S_A is legal before variation, then q_src maps the weighted variational source to sum_A w_A T_A rather than the unweighted total, so the quotient alone does not kill Delta_w_species",
            "status": "PREACTION_WEIGHT_BYPASS_SURVIVES",
            "proof_or_obstruction": "q_src needs the no-source-prefactor parent clause; otherwise the label can be encoded before the quotient",
            "source_anchor": "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv:PAC954_1_no_source_prefactors; P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv:MMA955_3_relative_prefactor",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "constructor_id": "QSRC1894_4_projected_mass_gap",
            "claim_piece": "Newton/GM projection after q_src",
            "mathematical_statement": "Even after q_src, measured-GM/Newton source normalization needs a closed calibrated mass projector with no exchange, boundary, anomaly, range, or time-drift leakage",
            "status": "PROJECTED_MASS_CALIBRATION_OPEN",
            "proof_or_obstruction": "source-domain quotient attacks species weights but does not by itself prove orbital/Newton mass calibration",
            "source_anchor": "P8_source_current_Ward_universality_CONTRACT.csv:SC6_closed_calibrated_mass_projector; P8_Y5_PARENT_QLOC_1893_LABEL_FORGETTING_CLAUSE_AUDIT.csv:LFA1893_4_projected_mass",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "constructor_id": "QSRC1894_5_verdict",
            "claim_piece": "promote q_src constructor as current MTS theorem",
            "mathematical_statement": "The current MTS parent theory forces all ordinary source couplings to factor through q_src(J_lab)=sum_A T_A",
            "status": "SOURCE_DOMAIN_QUOTIENT_CONSTRUCTOR_NOT_PARENT_DERIVED",
            "proof_or_obstruction": "constructor is exact as a contract, but parent adoption, no-prefactor exclusion, no-spurion return, non-Hilbert-current silence, and projected mass calibration remain unsigned",
            "source_anchor": "QSRC1894_0_definition through QSRC1894_4_projected_mass_gap",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def qsrc_clause_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "QG1894_0_parent_category",
            "required_clause": "parent source category declares q_src before F_src is formed",
            "formal_condition": "C_parent -> C_source quotients labelled current families by total Hilbert current",
            "current_status": "EXACT_MISSING_CLAUSE_NOT_PARENT_SIGNED",
            "if_pass": "source labels are absent from coupling-map arguments",
            "if_fail": "kappa_A and Delta_w_species stay legal",
            "source_anchor": "P8_Y5_R10_953_PARENT_CATEGORY_CONTRACT.csv:PMC953_1_label_forgetting_quotient",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "QG1894_1_total_hilbert_source",
            "required_clause": "active source is the total Hilbert/coframe derivative of one matter action",
            "formal_condition": "T_total=delta S_matter/delta e_obs=sum_A delta S_A/delta e_obs",
            "current_status": "CONDITIONAL_MATH_CLEAN_NOT_PARENT_COMPLETE",
            "if_pass": "labelled decomposition becomes bookkeeping after variation",
            "if_fail": "source current can be fitted/readout-defined",
            "source_anchor": "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv:PAC954_2_total_Hilbert_derivative",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "QG1894_2_no_source_prefactors",
            "required_clause": "no source-only species prefactor is an argument of S_matter",
            "formal_condition": "partial S_matter/partial w_A undefined or forbidden for source-only w_A",
            "current_status": "EXACT_HIGH_PRESSURE_MISSING_CLAUSE",
            "if_pass": "weighted-source countermodel is killed",
            "if_fail": "q_src can receive already-weighted source terms",
            "source_anchor": "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv:PAC954_1_no_source_prefactors; P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv:SPC955_2_relative_species_weight",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "QG1894_3_no_spurion_nonHilbert",
            "required_clause": "no hidden marker, boundary, domain, readout mask, or non-Hilbert current reintroduces label-dependent source strength",
            "formal_condition": "partial_A kappa=partial_marker kappa=0 and J_NH_retained=0 or separately bounded",
            "current_status": "NO_SPURION_AND_NONHILBERT_GATES_OPEN",
            "if_pass": "label forgetting survives readout and boundary/source-current bypasses",
            "if_fail": "Delta_w_marker_hidden and J_NH_retained remain live",
            "source_anchor": "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv:PAC954_3_no_hidden_spurion_return;PAC954_4_nonHilbert_current_split",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "QG1894_4_projected_mass",
            "required_clause": "measured-GM mass projector is closed and calibrated",
            "formal_condition": "d(Pi_M J_Hilbert)=0 with no exchange/boundary/anomaly flux and one common G_ref calibration",
            "current_status": "PROJECTED_FLUX_OPEN",
            "if_pass": "Newtonian source normalization can follow the GR source side",
            "if_fail": "orbital/Newton source normalization remains a separate residual",
            "source_anchor": "P8_source_current_Ward_universality_CONTRACT.csv:SC6_closed_calibrated_mass_projector",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "QG1894_5_verdict",
            "required_clause": "q_src can be used as a theorem-zero source coupling gate",
            "formal_condition": "QG1894_0 through QG1894_4 all pass",
            "current_status": "QSRC_CLAIM_BLOCKED",
            "if_pass": "Delta_w_species source side can be theorem-zero subject to left-hand field equation gates",
            "if_fail": "finite Delta_w/WEP material tensor intake remains the honest route",
            "source_anchor": "QG1894_0_parent_category through QG1894_4_projected_mass",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def wep_material_intake_rows() -> list[dict[str, Any]]:
    return [
        {
            "intake_id": "WMI1894_0_pair_context",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "TA6V_minus_PtRh10 material pair",
            "value_or_status": "TA6V=Ti0.90 Al0.06 V0.04; PtRh10=Pt0.90 Rh0.10",
            "source_path": str(INPUTS["1080_material_candidates"]),
            "source_anchor": "P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv:MAT1080_0_PtRh10_MICROSCOPE;MAT1080_1_TA6V_MICROSCOPE",
            "filled_level": "SOURCE_BACKED_COMPOSITION_CONTEXT",
            "missing_for_claim": "parent response basis and full material tensor",
            "units": "mass fractions",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "intake_id": "WMI1894_1_constituent_table",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "elemental A,Z,mass-fraction rows",
            "value_or_status": "constituent rows exist for Pt,Rh,Ti,Al,V",
            "source_path": str(INPUTS["983_constituents"]),
            "source_anchor": "P8_Y5_R10_983_MATERIAL_CONSTITUENTS.csv:M983_0_PtRh10;M983_1_TiAlloy",
            "filled_level": "SOURCE_BACKED_COMPOSITION_CONTEXT",
            "missing_for_claim": "isotopic averaging, binding/EM response basis, parent source tensor",
            "units": "A,Z,mass fraction",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "intake_id": "WMI1894_2_proxy_vectors",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "proxy charge vectors",
            "value_or_status": "Z/A, neutron-excess, electron-mass, alpha/Coulomb smoke proxies exist",
            "source_path": str(INPUTS["983_proxy_vectors"]),
            "source_anchor": "P8_Y5_R10_983_MATERIAL_PROXY_CHARGE_VECTORS.csv:proxy_charge_vector_computed; P8_Y5_R10_1424_TIPT_MATERIAL_VECTOR_CANDIDATES.csv:MAT1424_0_Z_over_A_toy..MAT1424_3_alpha_Coulomb_smoke_abs",
            "filled_level": "PROXY_CONTEXT_ONLY",
            "missing_for_claim": "MTS parent response basis, no-double-counting rule, tau_eff, source coefficient owner",
            "units": "dimensionless proxies",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "intake_id": "WMI1894_3_full_parent_tensor",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "full TA6V-minus-PtRh10 parent-basis material tensor",
            "value_or_status": "MISSING_FULL_PARENT_MATERIAL_TENSOR",
            "source_path": str(INPUTS["1481_material_pack"]),
            "source_anchor": "P8_Y5_R10_1481_WEP_MATERIAL_CONTEXT_PACK.csv:MAT1481_6_full_tensor; P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv:MAT1080_4_full_tensor_upgrade",
            "filled_level": "BLOCKED",
            "missing_for_claim": "parent basis, full response map, isotope/alloy averaging, source/readout environment stack",
            "units": "parent-basis response units",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "intake_id": "WMI1894_4_parent_coefficient_dependency",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "parent epsilon/C_parent vector dependency",
            "value_or_status": "MISSING_PARENT_EPSILON_OR_C_PARENT_VECTOR",
            "source_path": str(INPUTS["1893_wep_kernel"]),
            "source_anchor": "P8_Y5_PARENT_QLOC_1893_DELTAW_WEP_KERNEL_V0_NONCLAIM.csv:WEPK1893_1_parent_coefficient",
            "filled_level": "BLOCKED",
            "missing_for_claim": "parent numeric/theorem-zero coefficient vector with units/sign/source path",
            "units": "dimensionless or declared parent-basis units",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "intake_id": "WMI1894_5_tau_dependency",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "tau_eff/source/readout dependency",
            "value_or_status": "TAU_EFF_NOT_FILLED",
            "source_path": str(INPUTS["1893_wep_kernel"]),
            "source_anchor": "P8_Y5_PARENT_QLOC_1893_DELTAW_WEP_KERNEL_V0_NONCLAIM.csv:WEPK1893_3_tau_eff",
            "filled_level": "BLOCKED",
            "missing_for_claim": "official CMSM arrays, Earth/source worldtube, orbit/session average, product convention",
            "units": "declared by readout/source normalization",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "intake_id": "WMI1894_6_acceptance",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "material tensor intake acceptance",
            "value_or_status": "WEP_MATERIAL_TENSOR_INTAKE_BLOCKED_NONCLAIM",
            "source_path": str(INPUTS["1491_readiness"]),
            "source_anchor": "P8_Y5_R10_1491_DELTA_W_READINESS_MATRIX.csv:RDY1491_0_MICROSCOPE; P8_Y5_PARENT_QLOC_1893_DELTAW_WEP_KERNEL_V0_NONCLAIM.csv:WEPK1893_5_acceptance",
            "filled_level": "NONCLAIM_CONTEXT_ONLY",
            "missing_for_claim": "full parent tensor plus parent coefficient vector plus tau_eff; MICROSCOPE bound remains comparator only",
            "units": "dimensionless eta only after product convention",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "DRY1894_0_qsrc_math_only",
            "qsrc_parent_signed": False,
            "no_prefactor_signed": False,
            "uses_ward_as_label_forgetting": False,
            "wep_material_level": "context_only",
            "uses_proxy_as_tensor": False,
            "uses_bound_as_prediction": False,
            "expected_status": "REFUSED_QSRC_CONSTRUCTOR_NOT_PARENT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1894_1_ward_shortcut",
            "qsrc_parent_signed": False,
            "no_prefactor_signed": False,
            "uses_ward_as_label_forgetting": True,
            "wep_material_level": "context_only",
            "uses_proxy_as_tensor": False,
            "uses_bound_as_prediction": False,
            "expected_status": "REFUSED_WARD_ONLY_NOT_LABEL_FORGETTING",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1894_2_no_prefactor_missing",
            "qsrc_parent_signed": True,
            "no_prefactor_signed": False,
            "uses_ward_as_label_forgetting": False,
            "wep_material_level": "context_only",
            "uses_proxy_as_tensor": False,
            "uses_bound_as_prediction": False,
            "expected_status": "REFUSED_PREACTION_WEIGHT_BYPASS_SURVIVES",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1894_3_proxy_tensor",
            "qsrc_parent_signed": True,
            "no_prefactor_signed": True,
            "uses_ward_as_label_forgetting": False,
            "wep_material_level": "proxy_only",
            "uses_proxy_as_tensor": True,
            "uses_bound_as_prediction": False,
            "expected_status": "REFUSED_PROXY_MATERIAL_VECTOR_NOT_PARENT_TENSOR",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1894_4_full_tensor_missing",
            "qsrc_parent_signed": True,
            "no_prefactor_signed": True,
            "uses_ward_as_label_forgetting": False,
            "wep_material_level": "missing_full_tensor",
            "uses_proxy_as_tensor": False,
            "uses_bound_as_prediction": False,
            "expected_status": "REFUSED_FULL_PARENT_MATERIAL_TENSOR_MISSING",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1894_5_bound_shortcut",
            "qsrc_parent_signed": True,
            "no_prefactor_signed": True,
            "uses_ward_as_label_forgetting": False,
            "wep_material_level": "full_tensor",
            "uses_proxy_as_tensor": False,
            "uses_bound_as_prediction": True,
            "expected_status": "REFUSED_BOUND_ANCHOR_NOT_PREDICTION",
            "valid_for_claim": False,
        },
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    qsrc_signed = bool_string(row["qsrc_parent_signed"]) == "true"
    no_prefactor_signed = bool_string(row["no_prefactor_signed"]) == "true"
    ward_shortcut = bool_string(row["uses_ward_as_label_forgetting"]) == "true"
    material_level = str(row["wep_material_level"])
    proxy_as_tensor = bool_string(row["uses_proxy_as_tensor"]) == "true"
    bound_shortcut = bool_string(row["uses_bound_as_prediction"]) == "true"

    if ward_shortcut:
        status = "REFUSED_WARD_ONLY_NOT_LABEL_FORGETTING"
    elif not qsrc_signed:
        status = "REFUSED_QSRC_CONSTRUCTOR_NOT_PARENT_DERIVED"
    elif not no_prefactor_signed:
        status = "REFUSED_PREACTION_WEIGHT_BYPASS_SURVIVES"
    elif proxy_as_tensor or material_level == "proxy_only":
        status = "REFUSED_PROXY_MATERIAL_VECTOR_NOT_PARENT_TENSOR"
    elif material_level == "missing_full_tensor":
        status = "REFUSED_FULL_PARENT_MATERIAL_TENSOR_MISSING"
    elif bound_shortcut:
        status = "REFUSED_BOUND_ANCHOR_NOT_PREDICTION"
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
            "gate_id": "CG1894_0_qsrc",
            "condition": "parent action/category forces all ordinary source coupling maps to factor through q_src",
            "current_status": "FAIL_SOURCE_DOMAIN_QUOTIENT_CONSTRUCTOR_NOT_PARENT_DERIVED",
            "source_anchor": "P8_Y5_PARENT_QLOC_1894_SOURCE_DOMAIN_QUOTIENT_CONSTRUCTOR_ATTEMPT.csv:QSRC1894_5_verdict",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1894_1_no_prefactor",
            "condition": "no source-only pre-action species prefactor can enter before q_src",
            "current_status": "FAIL_PREACTION_WEIGHT_BYPASS_SURVIVES",
            "source_anchor": "P8_Y5_PARENT_QLOC_1894_SOURCE_DOMAIN_QUOTIENT_CONSTRUCTOR_ATTEMPT.csv:QSRC1894_3_no_prefactor_obstruction",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1894_2_material_tensor",
            "condition": "WEP material tensor is full parent-basis tensor, not proxy context",
            "current_status": "FAIL_MISSING_FULL_PARENT_MATERIAL_TENSOR",
            "source_anchor": "P8_Y5_PARENT_QLOC_1894_WEP_MATERIAL_TENSOR_INTAKE_NONCLAIM.csv:WMI1894_3_full_parent_tensor",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1894_3_verdict",
            "condition": "local source/WEP branch can claim derived or scored pass",
            "current_status": "CLAIM_BLOCKED",
            "source_anchor": "CG1894_0_qsrc through CG1894_2_material_tensor",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1894_0_qsrc",
            "decision": "q_src is mathematically constructed but not parent-derived",
            "reason": "the parent must still force factorization through q_src and forbid source labels before/after the quotient",
            "status": "CONSTRUCTOR_CONTRACT_WRITTEN_NOT_THEOREM",
            "next_dependency": "derive no-source-prefactor from parent object language, or keep finite Delta_w branch",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1894_1_material",
            "decision": "WEP material intake can use composition/proxy context only as nonclaim scaffolding",
            "reason": "the full MTS parent-basis material tensor is still missing",
            "status": "MATERIAL_CONTEXT_STAGED_NONCLAIM",
            "next_dependency": "parent response basis and full tensor construction",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1894_2_next",
            "decision": "attack the no-source-prefactor parent object-language proof next",
            "reason": "q_src fails mainly because a legal pre-action w_A can encode the label before the quotient",
            "status": "NEXT_TARGET_SELECTED",
            "next_dependency": "1895 no-source-prefactor object-language proof or parent material tensor basis",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1894_0_primary",
            "selection_status": "selected",
            "target_doc": "1895-Y5-R2FR-no-source-prefactor-object-language-proof-or-parent-material-tensor-basis.md",
            "target_script": "scripts/Y5_R2FR_no_source_prefactor_object_language_proof_or_parent_material_tensor_basis_1895.py",
            "objective": "try to derive that source-only w_A is not a well-typed parent object before variation; if it fails, build the parent material tensor basis needed for WEP without promoting proxies",
            "success_condition": "parent-signed object-language exclusion of source-only prefactors, or nonclaim parent material tensor basis rows with all proxy/shortcut gates explicit",
            "do_not": "do not claim q_src as parent theorem, do not use Ward as label forgetting, do not score proxy WEP tensors, and do not use MICROSCOPE bound as prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT1894_0_qsrc",
            "area": "source-domain quotient",
            "summary": "q_src is now explicitly constructed as the quotient from labelled species currents to total Hilbert current",
            "risk_level": "GOOD_CONTRACT_NOT_PARENT_THEOREM",
            "project_meaning": "we know exactly what object would close species-label coupling, but the parent action has not forced it yet",
            "next_action": "prove source-only w_A is not a legal parent object",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT1894_1_wep",
            "area": "WEP empirical branch",
            "summary": "composition context exists, but full parent-basis material tensor is still missing",
            "risk_level": "DATA_CONTEXT_NOT_SCORE_READY",
            "project_meaning": "testing route is organized, but no WEP score is allowed from proxies",
            "next_action": "construct parent material response basis or wait for parent coefficient basis",
            "valid_for_claim": False,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    return {
        "source_register": source_register_rows(),
        "qsrc_constructor": qsrc_constructor_rows(),
        "qsrc_clause_gate": qsrc_clause_gate_rows(),
        "wep_material_intake": wep_material_intake_rows(),
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
        "BYPASS",
        "NONCLAIM",
        "ANCHOR",
        "PROXY",
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
    checks.append({"validation_id": "VAL1894_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL", "detail": "all source paths exist and needles found", "valid_for_claim": False})

    constructor_rows_loaded = csv_rows(OUTPUTS["qsrc_constructor"])
    checks.append(
        {
            "validation_id": "VAL1894_01_qsrc_verdict",
            "status": "PASS" if any(row["constructor_id"] == "QSRC1894_5_verdict" and row["status"] == "SOURCE_DOMAIN_QUOTIENT_CONSTRUCTOR_NOT_PARENT_DERIVED" for row in constructor_rows_loaded) else "FAIL",
            "detail": "q_src constructor is contract-only, not parent theorem",
            "valid_for_claim": False,
        }
    )

    qgate_rows_loaded = csv_rows(OUTPUTS["qsrc_clause_gate"])
    checks.append(
        {
            "validation_id": "VAL1894_02_qsrc_gate",
            "status": "PASS" if any(row["gate_id"] == "QG1894_5_verdict" and row["current_status"] == "QSRC_CLAIM_BLOCKED" for row in qgate_rows_loaded) else "FAIL",
            "detail": "q_src claim gate remains blocked",
            "valid_for_claim": False,
        }
    )

    material_rows_loaded = csv_rows(OUTPUTS["wep_material_intake"])
    material_ok = len(material_rows_loaded) >= 7 and all(row["score_ready"] == "False" and row["valid_prediction_row"] == "False" for row in material_rows_loaded)
    checks.append(
        {
            "validation_id": "VAL1894_03_wep_material_intake",
            "status": "PASS" if material_ok and any(row["intake_id"] == "WMI1894_3_full_parent_tensor" and row["value_or_status"] == "MISSING_FULL_PARENT_MATERIAL_TENSOR" for row in material_rows_loaded) else "FAIL",
            "detail": "WEP material context is staged but full parent tensor remains missing/nonclaim",
            "valid_for_claim": False,
        }
    )

    dry_rows_loaded = csv_rows(OUTPUTS["dryrun_results"])
    checks.append(
        {
            "validation_id": "VAL1894_04_dryrun",
            "status": "PASS" if all(row["status_match"] == "True" and row["claim_allowed"] == "False" for row in dry_rows_loaded) else "FAIL",
            "detail": "dry-run refuses q_src math-only, Ward shortcut, preaction weight bypass, proxy tensor, missing full tensor, and bound shortcut",
            "valid_for_claim": False,
        }
    )

    gate_rows_loaded = csv_rows(OUTPUTS["claim_gate"])
    checks.append({"validation_id": "VAL1894_05_claim_gate", "status": "PASS" if any(row["gate_id"] == "CG1894_3_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in gate_rows_loaded) else "FAIL", "detail": "claim remains blocked", "valid_for_claim": False})

    next_rows_loaded = csv_rows(OUTPUTS["next_target"])
    checks.append({"validation_id": "VAL1894_06_next_target", "status": "PASS" if any(row["route_id"] == "NEXT1894_0_primary" and row["selection_status"] == "selected" for row in next_rows_loaded) else "FAIL", "detail": "1895 no-source-prefactor object-language target selected", "valid_for_claim": False})

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append({"validation_id": "VAL1894_07_claim_flags_false", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})

    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append({"validation_id": "VAL1894_08_blocked_markers_not_ready", "status": "PASS" if blocked_ok else "FAIL", "detail": blocked_detail, "valid_for_claim": False})

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1894_09_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})

    checks.append({"validation_id": "VAL1894_10_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1894_11_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})

    formalization_hits = list(FORMALIZATION.rglob("*1894*")) if FORMALIZATION.exists() else []
    checks.append({"validation_id": "VAL1894_12_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1894_count={len(formalization_hits)}", "valid_for_claim": False})

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1894_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1894 source-domain quotient constructor or WEP material tensor intake", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1894 - Source-Domain Quotient Constructor Or WEP Material Tensor Intake

## Purpose

This checkpoint tries to construct the parent source-domain quotient `q_src` that would make species labels unavailable to the coupling map. If the parent theorem still fails, it stages WEP material tensor intake as nonclaim context only.

## Result

- `q_src` can be written cleanly as a mathematical quotient: labelled species currents are identified when their total Hilbert/coframe current is the same.
- This is not yet a parent theorem. The parent action/category has not forced all source maps to factor through `q_src`.
- The main obstruction survives: a legal pre-action `w_A` can encode species dependence before the quotient unless the no-source-prefactor object-language proof is signed.
- WEP material composition context exists, but the full parent-basis material tensor remains missing and proxies are not promoted.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## q_src Constructor Attempt

{markdown_table(rows_by_name["qsrc_constructor"])}

## q_src Clause Gate

{markdown_table(rows_by_name["qsrc_clause_gate"])}

## WEP Material Tensor Intake

{markdown_table(rows_by_name["wep_material_intake"])}

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

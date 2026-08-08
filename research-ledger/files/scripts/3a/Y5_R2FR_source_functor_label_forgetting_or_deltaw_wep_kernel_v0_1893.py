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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1893"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1893-Y5-R2FR-source-functor-label-forgetting-or-deltaw-wep-kernel-v0.md"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1892_doc": ROOT / "1892-Y5-R2FR-ordinary-matter-action-signature-or-deltaw-species-projection-kernels.md",
    "1892_validation": OUT / "P8_Y5_BRR545_1892_VALIDATION.csv",
    "1892_clause_matrix": OUT / "P8_Y5_PARENT_QLOC_1892_SIGNATURE_CLAUSE_MATRIX.csv",
    "1892_kernel_stubs": OUT / "P8_Y5_PARENT_QLOC_1892_DELTAW_PROJECTION_KERNEL_STUBS_NONCLAIM.csv",
    "1892_next": OUT / "P8_Y5_PARENT_QLOC_1892_NEXT_TARGET.csv",
    "1889_ward_attempt": OUT / "P8_Y5_PARENT_QLOC_1889_SOURCE_CURRENT_WARD_OWNER_ATTEMPT.csv",
    "1889_label_contract": OUT / "P8_Y5_PARENT_QLOC_1889_NO_SPECIES_LABEL_FUNCTOR_CONTRACT.csv",
    "1889_component_basis": OUT / "P8_Y5_PARENT_QLOC_1889_REAL_DELTAW_COMPONENT_BASIS_ACQUISITION.csv",
    "1889_claim_gate": OUT / "P8_Y5_PARENT_QLOC_1889_CLAIM_GATE.csv",
    "1236_certificate": OUT / "P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
    "1491_delta_w_pack": OUT / "P8_Y5_R10_1491_REAL_DELTA_W_INPUT_PACK_NONCLAIM.csv",
    "1491_projection_requirements": OUT / "P8_Y5_R10_1491_ARENA_PROJECTION_REQUIREMENTS.csv",
    "1491_readiness": OUT / "P8_Y5_R10_1491_DELTA_W_READINESS_MATRIX.csv",
    "1481_material_pack": OUT / "P8_Y5_R10_1481_WEP_MATERIAL_CONTEXT_PACK.csv",
    "1481_tau_pack": OUT / "P8_Y5_R10_1481_WEP_TAU_SOURCE_READOUT_PACK.csv",
    "1484_wep_interface": OUT / "P8_Y5_R10_1484_BRANCH_LOCKED_WEP_PRODUCT_INTERFACE.csv",
    "1427_wep_schema": OUT / "P8_Y5_R10_1427_BRANCH_LOCKED_WEP_SCHEMA.csv",
}


SOURCE_NEEDLES = {
    "1892_doc": ["source functor that forgets species labels", "Delta_w Projection Kernel Stubs"],
    "1892_validation": ["VAL1892_OVERALL,PASS"],
    "1892_clause_matrix": ["OMC1892_4_source_functor_label_forgetting", "CONDITIONAL_LEMMA_NOT_PARENT_DERIVED"],
    "1892_kernel_stubs": ["DK1892_1_WEP", "KERNEL_STUB_NONCLAIM_MATERIAL_TENSOR_MISSING"],
    "1892_next": ["NEXT1892_0_primary", "source functor that forgets species labels"],
    "1889_ward_attempt": ["SWO1889_2_Ward_homogeneity", "WARD_ONLY_NOT_SPECIES_BLIND"],
    "1889_label_contract": ["NSF1889_0_domain", "LABEL_FORGETTING_NOT_PARENT_SIGNED"],
    "1889_component_basis": ["CB1889_1_pre_action_species_prefactor", "LIVE_COUNTERMODEL_COMPONENT"],
    "1889_claim_gate": ["BLOCKED_SOURCE_CURRENT_WARD_OWNER_NOT_DERIVED"],
    "1236_certificate": ["CERT1236_5_source_label_forgetting", "CONDITIONAL_LEMMA_NOT_PARENT_DERIVED"],
    "1491_delta_w_pack": ["DWI1491_1_MICROSCOPE_TiPt", "BOUND_ANCHOR_AVAILABLE_PROJECTION_BLOCKED"],
    "1491_projection_requirements": ["APR1491_1_material_source", "APR1491_2_tau_projection"],
    "1491_readiness": ["RDY1491_0_MICROSCOPE", "bound anchor exists"],
    "1481_material_pack": ["MAT1481_6_full_tensor", "MISSING_FULL_PARENT_MATERIAL_TENSOR"],
    "1481_tau_pack": ["TAU1481_6_symbolic_tau", "TAU_EFF_NOT_FILLED"],
    "1484_wep_interface": ["WPI1484_0_formula", "FORMULA_LOCKED_INPUTS_MISSING"],
    "1427_wep_schema": ["SCHEMA1427_0_branch_lock", "SCHEMA1427_3_no_shortcut"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1893_SOURCE_REGISTER.csv",
    "label_forgetting_attempt": OUT / "P8_Y5_PARENT_QLOC_1893_SOURCE_FUNCTOR_LABEL_FORGETTING_ATTEMPT.csv",
    "label_clause_audit": OUT / "P8_Y5_PARENT_QLOC_1893_LABEL_FORGETTING_CLAUSE_AUDIT.csv",
    "wep_kernel_v0": OUT / "P8_Y5_PARENT_QLOC_1893_DELTAW_WEP_KERNEL_V0_NONCLAIM.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1893_SOURCE_FUNCTOR_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1893_SOURCE_FUNCTOR_DRYRUN_RESULTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1893_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1893_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1893_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1893_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1893_VALIDATION.csv",
}


BRANCH_COPIES = {
    "label_forgetting_attempt": MICROSCOPE_RESIDUALS / OUTPUTS["label_forgetting_attempt"].name,
    "label_clause_audit": QUEUE / "JR1893_LABEL_FORGETTING_CLAUSE_AUDIT_NONCLAIM.csv",
    "wep_kernel_v0": SOURCE_WEIGHT_DOCS / "DELTAW_WEP_KERNEL_V0_1893_NONCLAIM.csv",
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


def label_forgetting_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "SFL1893_0_target",
            "claim_piece": "source functor label forgetting",
            "mathematical_statement": "q_src({(T_A,A)}) = T_total and F_src(q_src({(T_A,A)})) = kappa_univ T_total, with no access to A labels, w_A, kappa_A, material masks, or post-readout species selectors",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "this is the narrow theorem that would erase Delta_w_species from the parent source domain",
            "source_anchor": "P8_Y5_PARENT_QLOC_1889_NO_SPECIES_LABEL_FUNCTOR_CONTRACT.csv:NSF1889_0_domain; P8_Y5_PARENT_QLOC_1892_SIGNATURE_CLAUSE_MATRIX.csv:OMC1892_4_source_functor_label_forgetting",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "SFL1893_1_ward_bridge",
            "claim_piece": "Ward conservation bridge",
            "mathematical_statement": "diffeomorphism invariance of same-frame S_matter gives nabla_mu T_total^{mu nu}=0 on matter equations",
            "status": "VALID_CONDITIONAL_WARD_IDENTITY",
            "proof_or_obstruction": "conservation applies to the chosen current but does not choose the source functor domain or forbid weighted conserved sums",
            "source_anchor": "P8_Y5_PARENT_QLOC_1889_SOURCE_CURRENT_WARD_OWNER_ATTEMPT.csv:SWO1889_1_Ward_bridge",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "SFL1893_2_ward_countermodel",
            "claim_piece": "Ward is not label forgetting",
            "mathematical_statement": "E_munu = sum_A kappa_A T_A_munu can remain conserved for constant kappa_A, so Ward conservation alone permits species-weighted source currents",
            "status": "WARD_ONLY_NOT_SPECIES_BLIND",
            "proof_or_obstruction": "label forgetting must be parent grammar/category, not inferred from conservation",
            "source_anchor": "P8_Y5_PARENT_QLOC_1889_SOURCE_CURRENT_WARD_OWNER_ATTEMPT.csv:SWO1889_2_Ward_homogeneity",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "SFL1893_3_conditional_uniqueness",
            "claim_piece": "label-forgotten covariant additive source",
            "mathematical_statement": "if F_src only sees T_total, is local/covariant/additive/natural on one observed coframe, and has one calibrated source scale, then F_src(T_total)=kappa_univ T_total",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "relative weights cannot be formed once source labels are absent, but the label-forgetting quotient is not parent-signed",
            "source_anchor": "P8_Y5_PARENT_QLOC_1889_SOURCE_CURRENT_WARD_OWNER_ATTEMPT.csv:SWO1889_3_no_species_label_conditional; P8_Y5_PARENT_QLOC_1889_NO_SPECIES_LABEL_FUNCTOR_CONTRACT.csv:NSF1889_3_naturality",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "SFL1893_4_prefactor_obstruction",
            "claim_piece": "pre-action weight leak",
            "mathematical_statement": "S_matter=sum_A w_A S_A still Hilbert-varies to T_source=sum_A w_A T_A if w_A is legal before variation",
            "status": "PRE_ACTION_WEIGHT_COUNTERMODEL_SURVIVES",
            "proof_or_obstruction": "source label forgetting must pair with no pre-action source prefactors and no spurion return",
            "source_anchor": "P8_Y5_PARENT_QLOC_1889_SOURCE_CURRENT_WARD_OWNER_ATTEMPT.csv:SWO1889_5_pre_action_weight_leak; P8_Y5_PARENT_QLOC_1889_NO_SPECIES_LABEL_FUNCTOR_CONTRACT.csv:NSF1889_2_no_prefactors",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "SFL1893_5_verdict",
            "claim_piece": "promote source-label forgetting for current MTS",
            "mathematical_statement": "the parent source functor forgets species labels and returns only total Hilbert stress-energy before coupling selection",
            "status": "SOURCE_FUNCTOR_LABEL_FORGETTING_NOT_PARENT_DERIVED",
            "proof_or_obstruction": "domain quotient, no prefactors, no spurion return, and projected mass calibration remain unsigned",
            "source_anchor": "SFL1893_0_target through SFL1893_4_prefactor_obstruction",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def label_clause_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "LFA1893_0_domain_quotient",
            "required_clause": "source domain quotient forgets species labels before coupling",
            "formal_condition": "q_src({(T_A,A)})=T_total=sum_A T_A and F_src accepts only T_total",
            "current_status": "LABEL_FORGETTING_NOT_PARENT_SIGNED",
            "if_signed": "relative kappa_A/kappa_B cannot be formed",
            "if_unsigned": "Delta_w_species remains live",
            "source_anchor": "P8_Y5_PARENT_QLOC_1889_NO_SPECIES_LABEL_FUNCTOR_CONTRACT.csv:NSF1889_0_domain",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "LFA1893_1_total_variation",
            "required_clause": "source current is total Hilbert/coframe variation",
            "formal_condition": "T_total := delta S_matter/delta e_obs = sum_A delta S_A/delta e_obs",
            "current_status": "CONDITIONAL_MATH_CLEAN",
            "if_signed": "source object is the sum, not a labelled family",
            "if_unsigned": "non-Hilbert current or post-variation rescale remains possible",
            "source_anchor": "P8_Y5_PARENT_QLOC_1889_NO_SPECIES_LABEL_FUNCTOR_CONTRACT.csv:NSF1889_1_total_variation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "LFA1893_2_no_prefactors",
            "required_clause": "no independent source-only species prefactors before variation",
            "formal_condition": "partial S_matter/partial w_A=0 for source-only w_A",
            "current_status": "EXACT_HIGH_PRESSURE_MISSING_CLAUSE",
            "if_signed": "T_source=sum_A w_A T_A countermodel is removed",
            "if_unsigned": "pre-action species prefactor remains the main live component",
            "source_anchor": "P8_Y5_PARENT_QLOC_1889_NO_SPECIES_LABEL_FUNCTOR_CONTRACT.csv:NSF1889_2_no_prefactors; P8_Y5_PARENT_QLOC_1890_MATTER_NORMALIZATION_OWNER_AUDIT.csv:MNO1890_5_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "LFA1893_3_no_spurion_return",
            "required_clause": "no hidden/readout/domain marker reintroduces species labels",
            "formal_condition": "partial_A kappa = partial_marker kappa = partial_boundary kappa = partial_readout kappa = 0",
            "current_status": "NAMED_BUT_NOT_PARENT_SIGNED",
            "if_signed": "label forgetting survives hidden and readout routes",
            "if_unsigned": "species dependence can return after the source map",
            "source_anchor": "P8_Y5_PARENT_QLOC_1889_NO_SPECIES_LABEL_FUNCTOR_CONTRACT.csv:NSF1889_4_no_spurion_return",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "LFA1893_4_projected_mass",
            "required_clause": "measured-GM mass projector is closed and calibrated from Hilbert source",
            "formal_condition": "d(Pi_M J_Hilbert)=0 plus no exchange/boundary/anomaly flux",
            "current_status": "PROJECTED_FLUX_OPEN",
            "if_signed": "Newton/GM source normalization has a route to GR/Newton limit",
            "if_unsigned": "orbital/source calibration remains an independent residual",
            "source_anchor": "P8_Y5_PARENT_QLOC_1889_NO_SPECIES_LABEL_FUNCTOR_CONTRACT.csv:NSF1889_5_projected_mass; P8_Y5_PARENT_QLOC_1889_SOURCE_CURRENT_WARD_OWNER_ATTEMPT.csv:SWO1889_6_projected_mass_flux",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "LFA1893_5_verdict",
            "required_clause": "source-label forgetting is parent-derived",
            "formal_condition": "LFA1893_0 through LFA1893_4 all parent-signed",
            "current_status": "SOURCE_LABEL_FORGETTING_NOT_DERIVED",
            "if_signed": "Delta_w_species=0 can be promoted on the source side",
            "if_unsigned": "WEP kernel v0 remains nonclaim fallback",
            "source_anchor": "LFA1893_0_domain_quotient through LFA1893_4_projected_mass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def wep_kernel_v0_rows() -> list[dict[str, Any]]:
    return [
        {
            "kernel_id": "WEPK1893_0_formula",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "branch-locked Delta_w WEP product",
            "formula": "eta_pred(Ti,Pt)=tau_WEP * DeltaQ_TiPt dot epsilon_perp",
            "mapped_branch_formula": "eta_pred=|sum_X C_parent_X * R_material_X(TA6V-PtRh10) * tau_eff_X|",
            "current_status": "FORMULA_LOCKED_INPUTS_MISSING",
            "required_inputs": "parent epsilon/C_parent vector; full material tensor; tau_eff/source/readout kernel; product convention; branch lock",
            "bound_or_value": "2.8e-15 anchor only",
            "units": "dimensionless eta",
            "source_anchor": "P8_Y5_PARENT_QLOC_1892_DELTAW_PROJECTION_KERNEL_STUBS_NONCLAIM.csv:DK1892_1_WEP; P8_Y5_R10_1484_BRANCH_LOCKED_WEP_PRODUCT_INTERFACE.csv:WPI1484_0_formula",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "WEPK1893_1_parent_coefficient",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "epsilon_perp or C_parent_X",
            "formula": "epsilon_perp=P_perp epsilon or C_parent_X=delta S_parent/delta V_WEP,X",
            "mapped_branch_formula": "same X basis must be shared by parent coefficient, material tensor, and tau_eff",
            "current_status": "MISSING_PARENT_EPSILON_OR_C_PARENT_VECTOR",
            "required_inputs": "parent numeric/theorem-zero coefficient vector with units/sign/source path",
            "bound_or_value": "MISSING",
            "units": "dimensionless or declared parent-basis units",
            "source_anchor": "P8_Y5_PARENT_QLOC_1891_DELTAW_SPECIES_COEFFICIENT_ROW_NONCLAIM.csv:DWS1891_0_delta_w_species_coefficient_slot; P8_Y5_R10_1484_BRANCH_LOCKED_WEP_PRODUCT_INTERFACE.csv:WPI1484_1_C_parent",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "WEPK1893_2_material_tensor",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "DeltaQ_TiPt / R_material_X",
            "formula": "full TA6V-minus-PtRh10 response tensor in same parent basis as epsilon_perp",
            "mapped_branch_formula": "not DD proxy only and not Ye-only smoke context",
            "current_status": "MISSING_FULL_PARENT_MATERIAL_TENSOR",
            "required_inputs": "isotope/alloy averaged material response tensor and double-counting rule",
            "bound_or_value": "context proxies exist but not claim tensor",
            "units": "parent-basis response units",
            "source_anchor": "P8_Y5_R10_1481_WEP_MATERIAL_CONTEXT_PACK.csv:MAT1481_6_full_tensor; P8_Y5_R10_1484_BRANCH_LOCKED_WEP_PRODUCT_INTERFACE.csv:WPI1484_2_R_material",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "WEPK1893_3_tau_eff",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "tau_WEP / tau_eff_X",
            "formula": "tau_eff_X=<K_CMSM^a(t,s) R_source_a^X(t,s)> over accepted sessions/masks/orbit weights",
            "mapped_branch_formula": "readout/source/orbit functional converting source coupling to eta channel",
            "current_status": "SYMBOLIC_ONLY_NO_NUMERIC_OUTPUT",
            "required_inputs": "official CMSM arrays, Earth/source stress worldtube, orbit/session average, product convention",
            "bound_or_value": "TAU_EFF_NOT_FILLED",
            "units": "declared by readout/source normalization",
            "source_anchor": "P8_Y5_R10_1481_WEP_TAU_SOURCE_READOUT_PACK.csv:TAU1481_0_official_arrays;TAU1481_6_symbolic_tau; P8_Y5_R10_1484_BRANCH_LOCKED_WEP_PRODUCT_INTERFACE.csv:WPI1484_3_tau_eff",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "WEPK1893_4_branch_and_shortcut_guards",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "same branch/product/no-shortcut gate",
            "formula": "all factors share branch id, units/sign, and refuse tau=1, DD-as-MTS, surrogate arrays, bound inversion, or measured-G absorption",
            "mapped_branch_formula": "schema guard rather than physics claim",
            "current_status": "GUARD_EXISTS_NONCLAIM",
            "required_inputs": "branch-locked files for all numeric rows and accepted product convention",
            "bound_or_value": "guard only",
            "units": "dimensionless eta after declared convention",
            "source_anchor": "P8_Y5_R10_1427_BRANCH_LOCKED_WEP_SCHEMA.csv:SCHEMA1427_0_branch_lock;SCHEMA1427_3_no_shortcut; P8_Y5_R10_1484_BRANCH_LOCKED_WEP_PRODUCT_INTERFACE.csv:WPI1484_5_branch_guard",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_id": "WEPK1893_5_acceptance",
            "arena": "WEP_MICROSCOPE_TiPt",
            "object": "WEP kernel v0 acceptance verdict",
            "formula": "score only if parent coefficient, material tensor, tau_eff, product convention, and branch lock are all sourced",
            "mapped_branch_formula": "bound anchor is a comparator only after eta_pred exists",
            "current_status": "WEP_KERNEL_V0_BLOCKED_NONCLAIM",
            "required_inputs": "WEPK1893_1 through WEPK1893_4 promoted from missing/nonclaim to sourced rows",
            "bound_or_value": "2.8e-15 not used as prediction",
            "units": "dimensionless eta",
            "source_anchor": "P8_Y5_R10_1491_DELTA_W_READINESS_MATRIX.csv:RDY1491_0_MICROSCOPE; P8_Y5_R10_1491_ARENA_PROJECTION_REQUIREMENTS.csv:APR1491_1_material_source;APR1491_2_tau_projection",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "DRY1893_0_ward_only",
            "label_forgetting_parent_signed": False,
            "uses_ward_as_species_blindness": True,
            "no_prefactor_signed": False,
            "wep_kernel_inputs": "missing",
            "uses_bound_as_prediction": False,
            "expected_status": "REFUSED_WARD_ONLY_NOT_SPECIES_BLIND",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1893_1_label_forgetting_unsigned",
            "label_forgetting_parent_signed": False,
            "uses_ward_as_species_blindness": False,
            "no_prefactor_signed": False,
            "wep_kernel_inputs": "missing",
            "uses_bound_as_prediction": False,
            "expected_status": "REFUSED_LABEL_FORGETTING_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1893_2_prefactor_unsigned",
            "label_forgetting_parent_signed": True,
            "uses_ward_as_species_blindness": False,
            "no_prefactor_signed": False,
            "wep_kernel_inputs": "missing",
            "uses_bound_as_prediction": False,
            "expected_status": "REFUSED_NO_PREACTION_PREFACTOR_THEOREM",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1893_3_wep_kernel_missing",
            "label_forgetting_parent_signed": True,
            "uses_ward_as_species_blindness": False,
            "no_prefactor_signed": True,
            "wep_kernel_inputs": "missing",
            "uses_bound_as_prediction": False,
            "expected_status": "REFUSED_WEP_KERNEL_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1893_4_bound_shortcut",
            "label_forgetting_parent_signed": True,
            "uses_ward_as_species_blindness": False,
            "no_prefactor_signed": True,
            "wep_kernel_inputs": "sourced",
            "uses_bound_as_prediction": True,
            "expected_status": "REFUSED_BOUND_ANCHOR_NOT_PREDICTION",
            "valid_for_claim": False,
        },
        {
            "case_id": "DRY1893_5_schema_only",
            "label_forgetting_parent_signed": False,
            "uses_ward_as_species_blindness": False,
            "no_prefactor_signed": False,
            "wep_kernel_inputs": "schema_only",
            "uses_bound_as_prediction": False,
            "expected_status": "SCHEMA_ONLY_NOT_EVIDENCE",
            "valid_for_claim": False,
        },
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    label_signed = bool_string(row["label_forgetting_parent_signed"]) == "true"
    ward_only = bool_string(row["uses_ward_as_species_blindness"]) == "true"
    no_prefactor_signed = bool_string(row["no_prefactor_signed"]) == "true"
    wep_inputs = str(row["wep_kernel_inputs"])
    bound_shortcut = bool_string(row["uses_bound_as_prediction"]) == "true"

    if ward_only:
        status = "REFUSED_WARD_ONLY_NOT_SPECIES_BLIND"
    elif wep_inputs == "schema_only":
        status = "SCHEMA_ONLY_NOT_EVIDENCE"
    elif not label_signed:
        status = "REFUSED_LABEL_FORGETTING_UNSIGNED"
    elif not no_prefactor_signed:
        status = "REFUSED_NO_PREACTION_PREFACTOR_THEOREM"
    elif wep_inputs != "sourced":
        status = "REFUSED_WEP_KERNEL_INPUTS_MISSING"
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
            "gate_id": "CG1893_0_label_forgetting",
            "condition": "source functor forgets species labels before coupling selection",
            "current_status": "FAIL_SOURCE_FUNCTOR_LABEL_FORGETTING_NOT_PARENT_DERIVED",
            "source_anchor": "P8_Y5_PARENT_QLOC_1893_SOURCE_FUNCTOR_LABEL_FORGETTING_ATTEMPT.csv:SFL1893_5_verdict",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1893_1_no_prefactors",
            "condition": "no pre-action source-only species prefactor is legal",
            "current_status": "FAIL_PREACTION_WEIGHT_COUNTERMODEL_SURVIVES",
            "source_anchor": "P8_Y5_PARENT_QLOC_1893_LABEL_FORGETTING_CLAUSE_AUDIT.csv:LFA1893_2_no_prefactors",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1893_2_wep_kernel",
            "condition": "WEP kernel has parent coefficient, material tensor, tau/readout/source map, and branch guards",
            "current_status": "FAIL_WEP_KERNEL_V0_BLOCKED_NONCLAIM",
            "source_anchor": "P8_Y5_PARENT_QLOC_1893_DELTAW_WEP_KERNEL_V0_NONCLAIM.csv:WEPK1893_5_acceptance",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1893_3_verdict",
            "condition": "source-coupling local GR/WEP branch can claim pass",
            "current_status": "CLAIM_BLOCKED",
            "source_anchor": "CG1893_0_label_forgetting through CG1893_2_wep_kernel",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1893_0_label_forgetting",
            "decision": "do not promote Ward conservation to species-blind coupling",
            "reason": "constant species-weighted source currents can remain Ward-conserved",
            "status": "WARD_BRIDGE_RETAINED_NOT_PROMOTED",
            "next_dependency": "parent source-domain quotient q_src must be constructed",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1893_1_wep_kernel",
            "decision": "WEP kernel v0 exists only as a nonclaim formula/input ledger",
            "reason": "bound anchor exists, but parent coefficient, material tensor, and tau/readout/source map are missing",
            "status": "WEP_KERNEL_V0_BLOCKED_NONCLAIM",
            "next_dependency": "source-domain quotient theorem or WEP material/tau intake",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1893_2_next",
            "decision": "attack the source-domain quotient constructor next",
            "reason": "it is the missing parent object that would make label forgetting a theorem rather than a rule",
            "status": "NEXT_TARGET_SELECTED",
            "next_dependency": "1894 source-domain quotient constructor or WEP material tensor intake",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1893_0_primary",
            "selection_status": "selected",
            "target_doc": "1894-Y5-R2FR-source-domain-quotient-constructor-or-wep-material-tensor-intake.md",
            "target_script": "scripts/Y5_R2FR_source_domain_quotient_constructor_or_wep_material_tensor_intake_1894.py",
            "objective": "try to construct the parent source-domain quotient q_src that maps labelled species currents to total Hilbert stress before coupling; if it fails, stage the WEP material tensor intake with explicit missing source paths",
            "success_condition": "parent-signed q_src label-forgetting constructor, or nonclaim WEP material tensor intake rows that cannot score without parent epsilon/C_parent and tau_eff",
            "do_not": "do not use Ward conservation as label forgetting, do not use MICROSCOPE bound as prediction, and do not promote proxy material vectors",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT1893_0_source_coupling",
            "area": "local source coupling",
            "summary": "the narrow missing theorem is now source-domain quotient construction, not generic conservation",
            "risk_level": "CENTRAL_COUPLING_OBJECT_MISSING",
            "project_meaning": "this is the exact object needed for GR/Newton source universality",
            "next_action": "construct q_src or demote to finite WEP/source-weight branch",
            "valid_for_claim": False,
        },
        {
            "status_id": "STAT1893_1_wep_empirical",
            "area": "WEP kernel",
            "summary": "a WEP kernel v0 formula exists, but every claim-critical factor remains missing or nonclaim",
            "risk_level": "TEST_READY_SHAPE_NOT_INPUT_READY",
            "project_meaning": "we can now see what data would be needed without mistaking the bound for a prediction",
            "next_action": "fill material tensor/tau only after parent coefficient basis is declared",
            "valid_for_claim": False,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    return {
        "source_register": source_register_rows(),
        "label_forgetting_attempt": label_forgetting_attempt_rows(),
        "label_clause_audit": label_clause_audit_rows(),
        "wep_kernel_v0": wep_kernel_v0_rows(),
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
    flag_fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in flag_fields.intersection(row.keys()):
                if bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all generated claim/scoring flags remain false"


def blocked_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    blocked_markers = [
        "MISSING",
        "UNSIGNED",
        "NOT_DERIVED",
        "NOT_PARENT",
        "BLOCKED",
        "FAIL",
        "COUNTERMODEL",
        "NONCLAIM",
        "ANCHOR",
        "PROXY",
        "CLAIM_BLOCKED",
    ]
    readiness_fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass"}
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
    checks.append({"validation_id": "VAL1893_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL", "detail": "all source paths exist and needles found", "valid_for_claim": False})

    attempt_rows_loaded = csv_rows(OUTPUTS["label_forgetting_attempt"])
    checks.append(
        {
            "validation_id": "VAL1893_01_label_forgetting_verdict",
            "status": "PASS"
            if any(row["attempt_id"] == "SFL1893_5_verdict" and row["status"] == "SOURCE_FUNCTOR_LABEL_FORGETTING_NOT_PARENT_DERIVED" for row in attempt_rows_loaded)
            else "FAIL",
            "detail": "source-label forgetting remains unsigned",
            "valid_for_claim": False,
        }
    )

    audit_rows_loaded = csv_rows(OUTPUTS["label_clause_audit"])
    checks.append(
        {
            "validation_id": "VAL1893_02_clause_audit",
            "status": "PASS" if any(row["clause_id"] == "LFA1893_5_verdict" and row["current_status"] == "SOURCE_LABEL_FORGETTING_NOT_DERIVED" for row in audit_rows_loaded) else "FAIL",
            "detail": "label-forgetting clauses recorded with unsigned verdict",
            "valid_for_claim": False,
        }
    )

    kernel_rows_loaded = csv_rows(OUTPUTS["wep_kernel_v0"])
    checks.append(
        {
            "validation_id": "VAL1893_03_wep_kernel_v0",
            "status": "PASS" if len(kernel_rows_loaded) >= 6 and all(row["score_ready"] == "False" and row["valid_prediction_row"] == "False" for row in kernel_rows_loaded) else "FAIL",
            "detail": "WEP kernel v0 exists but is nonclaim/not score-ready",
            "valid_for_claim": False,
        }
    )

    dry_rows_loaded = csv_rows(OUTPUTS["dryrun_results"])
    checks.append(
        {
            "validation_id": "VAL1893_04_dryrun",
            "status": "PASS" if all(row["status_match"] == "True" and row["claim_allowed"] == "False" for row in dry_rows_loaded) else "FAIL",
            "detail": "dry-run refuses Ward-only, unsigned label forgetting, missing no-prefactor theorem, missing WEP inputs, bound shortcuts, and schema-only rows",
            "valid_for_claim": False,
        }
    )

    gate_rows_loaded = csv_rows(OUTPUTS["claim_gate"])
    checks.append({"validation_id": "VAL1893_05_claim_gate", "status": "PASS" if any(row["gate_id"] == "CG1893_3_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in gate_rows_loaded) else "FAIL", "detail": "claim remains blocked", "valid_for_claim": False})

    next_rows_loaded = csv_rows(OUTPUTS["next_target"])
    checks.append({"validation_id": "VAL1893_06_next_target", "status": "PASS" if any(row["route_id"] == "NEXT1893_0_primary" and row["selection_status"] == "selected" for row in next_rows_loaded) else "FAIL", "detail": "1894 source-domain quotient target selected", "valid_for_claim": False})

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append({"validation_id": "VAL1893_07_claim_flags_false", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})

    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append({"validation_id": "VAL1893_08_blocked_markers_not_ready", "status": "PASS" if blocked_ok else "FAIL", "detail": blocked_detail, "valid_for_claim": False})

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1893_09_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})

    checks.append({"validation_id": "VAL1893_10_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1893_11_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})

    formalization_hits = list(FORMALIZATION.rglob("*1893*")) if FORMALIZATION.exists() else []
    checks.append({"validation_id": "VAL1893_12_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1893_count={len(formalization_hits)}", "valid_for_claim": False})

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1893_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1893 source functor label forgetting or Delta_w WEP kernel v0", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1893 - Source-Functor Label Forgetting Or Delta_w WEP Kernel v0

## Purpose

This checkpoint attacks the narrow coupling theorem: the source functor must forget species labels before coupling selection. If that theorem remains unsigned, the WEP fallback is kept as an explicit nonclaim kernel.

## Result

- Ward conservation is useful but not enough: species-weighted conserved currents can exist.
- The label-forgetting theorem is clean only if the parent source-domain quotient `q_src` is signed and no pre-action `w_A`/spurion route survives.
- Current verdict: `SOURCE_FUNCTOR_LABEL_FORGETTING_NOT_PARENT_DERIVED`.
- WEP kernel v0 is staged as a formula/input ledger only; the MICROSCOPE bound is not used as a prediction.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Source-Functor Label Forgetting Attempt

{markdown_table(rows_by_name["label_forgetting_attempt"])}

## Label-Forgetting Clause Audit

{markdown_table(rows_by_name["label_clause_audit"])}

## Delta_w WEP Kernel v0

{markdown_table(rows_by_name["wep_kernel_v0"])}

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

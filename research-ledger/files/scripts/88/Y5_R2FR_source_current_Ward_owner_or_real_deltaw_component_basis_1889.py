from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1889"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1889-Y5-R2FR-source-current-Ward-owner-or-real-deltaw-component-basis.md"

INPUTS = {
    "1888_doc": ROOT / "1888-Y5-R2FR-action-scale-owner-readout-stability-or-finite-deltaw-vector.md",
    "1888_validation": OUT / "P8_Y5_BRR545_1888_VALIDATION.csv",
    "1888_action_owner": OUT / "P8_Y5_PARENT_QLOC_1888_ACTION_SCALE_OWNER_PROOF_ATTEMPT.csv",
    "1888_finite_intake": OUT / "P8_Y5_PARENT_QLOC_1888_FINITE_DELTAW_VECTOR_ROW_INTAKE.csv",
    "1888_next": OUT / "P8_Y5_PARENT_QLOC_1888_NEXT_TARGET.csv",
    "951_ward": OUT / "P8_Y5_R10_951_SOURCE_CURRENT_WARD_ACTION_ATTEMPT.csv",
    "952_selection": OUT / "P8_Y5_R10_952_SINGLE_SOURCE_SELECTION_ATTEMPT.csv",
    "953_functor": OUT / "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv",
    "953_category": OUT / "P8_Y5_R10_953_PARENT_CATEGORY_CONTRACT.csv",
    "954_clause": OUT / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
    "954_label_forgetting": OUT / "P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv",
    "955_matter_lemma": OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
    "source_current_contract": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "1677_owner": OUT / "P8_Y5_PARENT_QLOC_1677_SOURCE_CURRENT_OWNER_ATTEMPT.csv",
    "1680_zero_clauses": OUT / "P8_Y5_PARENT_QLOC_1680_SOURCE_CURRENT_OWNER_ZERO_THEOREM_CLAUSES.csv",
    "1683_derivation": OUT / "P8_Y5_PARENT_QLOC_1683_SOURCE_CURRENT_OWNER_DERIVATION_ATTEMPT.csv",
    "1086_zero": OUT / "P8_Y5_R10_1086_SOURCE_CURRENT_ZERO_THEOREM_ATTEMPT.csv",
    "1549_variational_law": OUT / "P8_Y5_PARENT_QLOC_1549_VARIATIONAL_SOURCE_CURRENT_LAW.csv",
    "1620_chain_rule": OUT / "P8_Y5_PARENT_QLOC_1620_CHAIN_RULE_SOURCE_CURRENT_ZERO_ATTEMPT.csv",
    "1621_finite_rows": OUT / "P8_Y5_PARENT_QLOC_1621_FINITE_SOURCE_CURRENT_COEFFICIENT_ROWS.csv",
    "1780_impact": OUT / "P8_Y5_PARENT_QLOC_1780_SOURCE_CURRENT_IMPACT_LEDGER.csv",
    "576_counterexamples": OUT / "P8_Y5_R10_576_SOURCE_CURRENT_COUNTEREXAMPLES.csv",
    "737_ward_flux": OUT / "P8_Y5_R10_737_SOURCE_CURRENT_WARD_FLUX_ATTEMPT.csv",
    "1762_deltaw": OUT / "P8_Y5_PARENT_QLOC_1762_DELTAW_BOUND_INTERFACE.csv",
    "1491_delta_w_pack": OUT / "P8_Y5_R10_1491_REAL_DELTA_W_INPUT_PACK_NONCLAIM.csv",
    "local_bounds": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
}

SOURCE_NEEDLES = {
    "1888_doc": ["SELECT_1889_SOURCE_CURRENT_WARD_OWNER_OR_REAL_DELTAW_COMPONENT_BASIS", "ZTH1888_2_current_owner"],
    "1888_validation": ["VAL1888_OVERALL,PASS"],
    "1888_action_owner": ["ASO1888_6_countermodel", "ACTION_SCALE_OWNER_NOT_DERIVED"],
    "1888_finite_intake": ["FDV1888_0_core_vector", "MISSING_PARENT_COMPONENT_BASIS"],
    "1888_next": ["NEXT1888_0_primary", "do not use Ward conservation of the total current as species-blindness"],
    "951_ward": ["SWA951_3_species_weight_countermodel", "not_closed_current_corpus"],
    "952_selection": ["SSC952_1_Ward_symmetry", "SSC952_5_verdict"],
    "953_functor": ["NSF953_2_conditional_uniqueness", "NSF953_5_verdict"],
    "953_category": ["PMC953_1_label_forgetting_quotient", "PMC953_5_contract_verdict"],
    "954_clause": ["PAC954_1_no_source_prefactors", "PAC954_5_GR_source_limit_clause"],
    "954_label_forgetting": ["PLF954_2_prefactor_obstruction", "PLF954_5_verdict"],
    "955_matter_lemma": ["MMA955_3_relative_prefactor", "MMA955_6_verdict"],
    "source_current_contract": ["SC3_universal_kappa_coupling", "SC8_second_order_source_stability"],
    "1677_owner": ["SCO1677_5_verdict", "SOURCE_CURRENT_OWNER_NOT_DERIVED"],
    "1680_zero_clauses": ["CL1680_4", "MISSING_CURRENT_OWNER"],
    "1683_derivation": ["OWN1683_5_verdict", "OWNER_DERIVATION_FAILS_CURRENT_CORPUS"],
    "1086_zero": ["SCZ1086_2_pre_action_weight_leak", "SOURCE_CURRENT_ZERO_NOT_DERIVED"],
    "1549_variational_law": ["VAR1549_4_no_readout_definition", "NOT_SCORE_READY"],
    "1620_chain_rule": ["CR1620_3_pre_action_countermodel", "CHAIN_RULE_THEOREM_CLOSED_APPLICATION_BLOCKED"],
    "1621_finite_rows": ["FCR1621_5_source_weight", "MISSING_WEIGHT_BOUND"],
    "1780_impact": ["SCI1780_1_Newton", "Newton source normalization blocked"],
    "576_counterexamples": ["CE576_1_species_weighted_kappa", "CE576_5_mass_calibration_split"],
    "737_ward_flux": ["WFA737_2_projected_mass_flux_target", "not_derived_for_current_claim"],
    "1762_deltaw": ["DW1762_1_delta_w_A", "MISSING_COMPONENT_BASIS_OR_THEOREM_ZERO"],
    "1491_delta_w_pack": ["DWI1491_0_core_model", "MISSING_PARENT_COMPONENT_BASIS"],
    "local_bounds": ["R1_WEP_source_charge", "2.8e-15"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1889_SOURCE_REGISTER.csv",
    "ward_owner_attempt": OUT / "P8_Y5_PARENT_QLOC_1889_SOURCE_CURRENT_WARD_OWNER_ATTEMPT.csv",
    "functor_contract": OUT / "P8_Y5_PARENT_QLOC_1889_NO_SPECIES_LABEL_FUNCTOR_CONTRACT.csv",
    "component_basis": OUT / "P8_Y5_PARENT_QLOC_1889_REAL_DELTAW_COMPONENT_BASIS_ACQUISITION.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1889_COMPONENT_BASIS_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1889_COMPONENT_BASIS_DRYRUN_RESULTS.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_1889_RUNNER_REFUSAL.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1889_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1889_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1889_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1889_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1889_VALIDATION.csv",
}

SOURCE_WEIGHT_TEMPLATE_COPY = SOURCE_WEIGHT_DOCS / "DELTAW_COMPONENT_BASIS1889_ACQUISITION_NONCLAIM.csv"


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def path_has_needles(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "MISSING_SOURCE_PATH"
    text = path.read_text(encoding="utf-8", errors="ignore")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "MISSING_NEEDLES=" + ";".join(missing)
    return True, "OK"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        ok, detail = path_has_needles(path, SOURCE_NEEDLES[source_id])
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle_status": "PASS" if ok else "FAIL",
                "needle_detail": detail,
                "required_needles": "; ".join(SOURCE_NEEDLES[source_id]),
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def ward_owner_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SWO1889_0_target",
            "claim": "parent source-current Ward owner makes T_total/J_source species-blind",
            "mathematical_statement": "S_matter=sum_A S_A on one observed coframe, T_total=delta S_matter/delta e_obs, F_src(T_total)=kappa_univ T_total",
            "result": "TARGET_EXACT",
            "what_it_proves": "would remove relative kappa_A, w_A, and post-readout source masks from the source-side GR/Newton route",
            "gap": "the target is a parent category/action theorem, not a consequence of Ward conservation alone",
            "source_anchor": "P8_Y5_PARENT_QLOC_1888_NEXT_TARGET.csv:NEXT1888_0_primary",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SWO1889_1_Ward_bridge",
            "claim": "Ward identity conserves the owned Hilbert current",
            "mathematical_statement": "diffeomorphism invariance of same-frame S_matter gives nabla_mu T_matter^{mu nu}=0 on matter equations",
            "result": "VALID_CONDITIONAL_WARD_IDENTITY",
            "what_it_proves": "conservation of the current chosen by the action",
            "gap": "does not choose one universal coupling or erase species labels",
            "source_anchor": "P8_Y5_R10_951_SOURCE_CURRENT_WARD_ACTION_ATTEMPT.csv:SWA951_0_matter_Ward;P8_Y5_R10_737_SOURCE_CURRENT_WARD_FLUX_ATTEMPT.csv:WFA737_0_same_frame_matter_Ward",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SWO1889_2_Ward_homogeneity",
            "claim": "Ward conservation forces kappa_A=kappa_B",
            "mathematical_statement": "E_munu=sum_A kappa_A T_A_munu with constant kappa_A can conserve a weighted total current",
            "result": "WARD_ONLY_NOT_SPECIES_BLIND",
            "what_it_proves": "Ward is a bridge, not the owner of source normalization",
            "gap": "relative kappa_A survive unless the parent source functor forgets labels",
            "source_anchor": "P8_Y5_R10_951_SOURCE_CURRENT_WARD_ACTION_ATTEMPT.csv:SWA951_3_species_weight_countermodel;P8_Y5_R10_952_SINGLE_SOURCE_SELECTION_ATTEMPT.csv:SSC952_1_Ward_symmetry",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SWO1889_3_no_species_label_conditional",
            "claim": "label-forgotten covariant additive source functor has one coupling",
            "mathematical_statement": "if F_src only sees T_total, is local/covariant/additive, and has one observed coframe, then F_src(T_total)=kappa_univ T_total",
            "result": "CONDITIONAL_UNIQUENESS_CLEAN",
            "what_it_proves": "relative source weights cannot be written once A labels are absent from the source-functor domain",
            "gap": "parent label-forgetting quotient is not signed",
            "source_anchor": "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv:NSF953_2_conditional_uniqueness;NSF953_5_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SWO1889_4_total_variation_route",
            "claim": "total Hilbert variation gives label-forgotten source",
            "mathematical_statement": "T_total=(2/sqrt(-g_obs)) delta S_matter/delta g_obs with S_matter=sum_A S_A",
            "result": "EXACT_IF_NO_PRE_ACTION_PREFACTOR",
            "what_it_proves": "species decomposition becomes bookkeeping after variation of one total matter action",
            "gap": "if S_matter=sum_A w_A S_A, variation gives T_source=sum_A w_A T_A",
            "source_anchor": "P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv:PLF954_1_total_variation_route;PLF954_2_prefactor_obstruction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SWO1889_5_pre_action_weight_leak",
            "claim": "current owner kills weights inserted before variation",
            "mathematical_statement": "S_matter=sum_A w_A S_A still Hilbert-varies to a weighted source if w_A is legal before variation",
            "result": "PRE_ACTION_WEIGHT_COUNTERMODEL_SURVIVES",
            "what_it_proves": "source-current owner must be paired with a no-source-prefactor parent action clause",
            "gap": "NoSourceOnlySpeciesSlot/no-prefactor clause remains unsigned",
            "source_anchor": "P8_Y5_R10_1086_SOURCE_CURRENT_ZERO_THEOREM_ATTEMPT.csv:SCZ1086_2_pre_action_weight_leak;P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv:MMA955_3_relative_prefactor",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SWO1889_6_projected_mass_flux",
            "claim": "same-frame Hilbert conservation closes Newton/GM source normalization",
            "mathematical_statement": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H + Pi_M J_exchange + A_parent",
            "result": "PROJECTED_FLUX_NOT_CLOSED_BY_WARD",
            "what_it_proves": "projected measured mass is stronger than unprojected Hilbert-current conservation",
            "gap": "Pi_M ownership, exchange current, boundary/anomaly flux, Gauss/orbital calibration remain unsigned",
            "source_anchor": "P8_Y5_R10_737_SOURCE_CURRENT_WARD_FLUX_ATTEMPT.csv:WFA737_2_projected_mass_flux_target;WFA737_4_full_source_normalized_Newton",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "SWO1889_7_verdict",
            "claim": "source-current Ward owner derives GR/Newton source side",
            "mathematical_statement": "Ward + label-forgotten source functor + no pre-action prefactors + projected mass calibration => one calibrated source coupling",
            "result": "SOURCE_CURRENT_WARD_OWNER_NOT_DERIVED",
            "what_it_proves": "the conditional spine is now exact enough to state",
            "gap": "parent no-source-prefactor clause and source-domain label-forgetting are still the narrow missing theorem",
            "source_anchor": "SWO1889_0 through SWO1889_6",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def functor_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "NSF1889_0_domain",
            "required_clause": "source domain forgets species labels before coupling selection",
            "formal_condition": "q_src({(T_A,A)})=T_total=sum_A T_A",
            "if_signed": "relative kappa_A/kappa_B cannot be formed",
            "current_status": "LABEL_FORGETTING_NOT_PARENT_SIGNED",
            "source_anchor": "P8_Y5_R10_953_PARENT_CATEGORY_CONTRACT.csv:PMC953_1_label_forgetting_quotient",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "NSF1889_1_total_variation",
            "required_clause": "active source is total Hilbert/coframe derivative of one total matter action",
            "formal_condition": "T_total := delta S_matter/delta e_obs = sum_A delta S_A/delta e_obs",
            "if_signed": "source object is the sum, not a labelled family",
            "current_status": "CONDITIONAL_MATH_CLEAN",
            "source_anchor": "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv:PAC954_2_total_Hilbert_derivative",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "NSF1889_2_no_prefactors",
            "required_clause": "no independent species/source prefactors multiply matter actions before variation",
            "formal_condition": "partial S_matter/partial w_A=0 for source-only w_A",
            "if_signed": "T_source=sum_A w_A T_A countermodel is removed",
            "current_status": "EXACT_HIGH_PRESSURE_MISSING_CLAUSE",
            "source_anchor": "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv:PAC954_1_no_source_prefactors",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "NSF1889_3_naturality",
            "required_clause": "source map is natural, covariant, additive, and local in observed coframe data",
            "formal_condition": "F_src(phi_*T)=phi_*F_src(T); F_src(T+U)=F_src(T)+F_src(U)",
            "if_signed": "label-forgotten source has only one scalar multiple",
            "current_status": "CONDITIONAL_MATHEMATICS_CLEAR",
            "source_anchor": "P8_Y5_R10_953_PARENT_CATEGORY_CONTRACT.csv:PMC953_2_natural_additive_map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "NSF1889_4_no_spurion_return",
            "required_clause": "no hidden constants, markers, boundary classes, source masks, or post-readout maps reintroduce species dependence",
            "formal_condition": "partial_A kappa = partial_marker kappa = partial_boundary kappa = partial_readout kappa = 0",
            "if_signed": "label-forgetting survives hidden/readout routes",
            "current_status": "NAMED_BUT_NOT_PARENT_SIGNED",
            "source_anchor": "P8_Y5_R10_953_PARENT_CATEGORY_CONTRACT.csv:PMC953_3_no_hidden_source_spurion;P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv:PAC954_3_no_hidden_spurion_return",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "NSF1889_5_projected_mass",
            "required_clause": "measured-GM mass projector is closed and calibrated from the Hilbert source",
            "formal_condition": "d(Pi_M J_Hilbert)=0 and M_eff=(4 pi G_ref)^-1 int_S2 Pi_M J_Hilbert",
            "if_signed": "Newton/GM source normalization has a route to GR/Newton limit",
            "current_status": "PROJECTED_FLUX_OPEN",
            "source_anchor": "P8_source_current_Ward_universality_CONTRACT.csv:SC6_closed_calibrated_mass_projector;P8_Y5_R10_737_SOURCE_CURRENT_WARD_FLUX_ATTEMPT.csv:WFA737_2_projected_mass_flux_target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def component_basis_rows() -> list[dict[str, Any]]:
    return [
        {
            "basis_id": "CB1889_0_common_mode",
            "component": "common_source_normalization",
            "meaning": "one universal kappa_univ or w_common after uniqueness",
            "status": "CALIBRATION_ONLY_AFTER_UNIQUENESS",
            "observable_projection": "G_N/GM calibration common mode, not WEP-visible by itself",
            "required_source": "parent uniqueness theorem before absorption into G_ref",
            "source_path": str(INPUTS["953_functor"]),
            "source_anchor": "NSF953_4_calibration_limit",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "CB1889_1_pre_action_species_prefactor",
            "component": "Delta_w_species",
            "meaning": "relative pre-variation species/action prefactor w_A/w_B",
            "status": "LIVE_COUNTERMODEL_COMPONENT",
            "observable_projection": "WEP, R10 source/test product, PPN beta source, Newton source normalization",
            "required_source": "no-prefactor theorem or numeric parent coefficient vector",
            "source_path": str(INPUTS["954_clause"]),
            "source_anchor": "PAC954_1_no_source_prefactors",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "CB1889_2_post_variation_current_rescale",
            "component": "c_A_current_rescale",
            "meaning": "J_A -> c_A J_A or beta_source,A after Hilbert extraction",
            "status": "CURRENT_OWNER_MISSING",
            "observable_projection": "source-current/WEP/R10/Newton residual rows",
            "required_source": "source-current owner/no-rescale theorem or coefficient row",
            "source_path": str(INPUTS["1677_owner"]),
            "source_anchor": "SCO1677_2_current_rescaling_guard",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "CB1889_3_hidden_marker_spurion",
            "component": "Delta_w_marker_hidden",
            "meaning": "hidden invariant, material marker, boundary class, domain selector, or readout mask reweights source",
            "status": "NO_SPURION_THEOREM_UNSIGNED",
            "observable_projection": "composition/source charge, clock/source product, R10 range-dependent source coupling",
            "required_source": "no-hidden-spurion theorem or finite marker coefficient bounds",
            "source_path": str(INPUTS["953_category"]),
            "source_anchor": "PMC953_3_no_hidden_source_spurion",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "CB1889_4_nonHilbert_current",
            "component": "J_NH_retained",
            "meaning": "bulk, boundary, domain, memory, range, connection, spin/torsion or improvement current bypasses Hilbert source",
            "status": "OPEN_PARALLEL_GATE",
            "observable_projection": "boundary/exchange source vector, R10/local residual, PPN source stability",
            "required_source": "formula-level K_owner and q_retained zero proof or finite coefficient row",
            "source_path": str(INPUTS["source_current_contract"]),
            "source_anchor": "SC4_no_nonHilbert_source_current",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "CB1889_5_mass_projector_flux",
            "component": "Delta_mu_projector",
            "meaning": "measured-GM/orbital mass projector, exchange, boundary, anomaly, or Gauss calibration residual",
            "status": "PROJECTED_FLUX_OPEN",
            "observable_projection": "Newtonian limit, orbital GM drift, PPN source normalization",
            "required_source": "closed calibrated mass projector or finite Delta_mu row",
            "source_path": str(INPUTS["737_ward_flux"]),
            "source_anchor": "WFA737_2_projected_mass_flux_target",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY1889_0_Ward_only", "ward_identity": True, "label_forgetting": False, "no_prefactor": False, "component_source": False, "parent_vector": False, "tau": False, "K_projection": False, "bound_anchor": False, "G_absorption": False, "cancellation": False, "schema_only": False, "expected_status": "REFUSED_WARD_ONLY_NOT_SPECIES_BLIND", "valid_for_claim": False, "claim_allowed": False},
        {"case_id": "DRY1889_1_label_unsigned", "ward_identity": True, "label_forgetting": False, "no_prefactor": True, "component_source": False, "parent_vector": False, "tau": False, "K_projection": False, "bound_anchor": False, "G_absorption": False, "cancellation": False, "schema_only": False, "expected_status": "REFUSED_LABEL_FORGETTING_UNSIGNED", "valid_for_claim": False, "claim_allowed": False},
        {"case_id": "DRY1889_2_prefactor_leak", "ward_identity": True, "label_forgetting": True, "no_prefactor": False, "component_source": False, "parent_vector": False, "tau": False, "K_projection": False, "bound_anchor": False, "G_absorption": False, "cancellation": False, "schema_only": False, "expected_status": "REFUSED_PRE_ACTION_WEIGHT_COUNTERMODEL", "valid_for_claim": False, "claim_allowed": False},
        {"case_id": "DRY1889_3_missing_component_source", "ward_identity": False, "label_forgetting": False, "no_prefactor": False, "component_source": False, "parent_vector": True, "tau": True, "K_projection": True, "bound_anchor": False, "G_absorption": False, "cancellation": False, "schema_only": False, "expected_status": "REFUSED_MISSING_COMPONENT_SOURCE", "valid_for_claim": False, "claim_allowed": False},
        {"case_id": "DRY1889_4_bound_anchor", "ward_identity": False, "label_forgetting": False, "no_prefactor": False, "component_source": False, "parent_vector": False, "tau": False, "K_projection": False, "bound_anchor": True, "G_absorption": False, "cancellation": False, "schema_only": False, "expected_status": "REFUSED_BOUND_ANCHOR_NOT_PREDICTION", "valid_for_claim": False, "claim_allowed": False},
        {"case_id": "DRY1889_5_missing_tau", "ward_identity": False, "label_forgetting": False, "no_prefactor": False, "component_source": True, "parent_vector": True, "tau": False, "K_projection": True, "bound_anchor": False, "G_absorption": False, "cancellation": False, "schema_only": False, "expected_status": "REFUSED_MISSING_TAU_PROJECTION", "valid_for_claim": False, "claim_allowed": False},
        {"case_id": "DRY1889_6_missing_K", "ward_identity": False, "label_forgetting": False, "no_prefactor": False, "component_source": True, "parent_vector": True, "tau": True, "K_projection": False, "bound_anchor": False, "G_absorption": False, "cancellation": False, "schema_only": False, "expected_status": "REFUSED_MISSING_K_QBAR_PROJECTION", "valid_for_claim": False, "claim_allowed": False},
        {"case_id": "DRY1889_7_G_absorption", "ward_identity": False, "label_forgetting": False, "no_prefactor": False, "component_source": True, "parent_vector": True, "tau": True, "K_projection": True, "bound_anchor": False, "G_absorption": True, "cancellation": False, "schema_only": False, "expected_status": "REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_GUARD", "valid_for_claim": False, "claim_allowed": False},
        {"case_id": "DRY1889_8_cancellation", "ward_identity": False, "label_forgetting": False, "no_prefactor": False, "component_source": True, "parent_vector": True, "tau": True, "K_projection": True, "bound_anchor": False, "G_absorption": False, "cancellation": True, "schema_only": False, "expected_status": "REFUSED_CANCELLATION_ONLY", "valid_for_claim": False, "claim_allowed": False},
        {"case_id": "DRY1889_9_schema_only", "ward_identity": False, "label_forgetting": False, "no_prefactor": False, "component_source": True, "parent_vector": True, "tau": True, "K_projection": True, "bound_anchor": False, "G_absorption": False, "cancellation": False, "schema_only": True, "expected_status": "SCHEMA_MATH_ONLY_NOT_EVIDENCE", "valid_for_claim": False, "claim_allowed": False},
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    if bool_string(row["bound_anchor"]) == "true":
        status = "REFUSED_BOUND_ANCHOR_NOT_PREDICTION"
        detail = "bound anchors constrain products; they are not parent coefficients"
    elif bool_string(row["ward_identity"]) == "true" and bool_string(row["label_forgetting"]) != "true" and bool_string(row["no_prefactor"]) != "true":
        status = "REFUSED_WARD_ONLY_NOT_SPECIES_BLIND"
        detail = "Ward conserves the current supplied by the action"
    elif bool_string(row["ward_identity"]) == "true" and bool_string(row["label_forgetting"]) != "true":
        status = "REFUSED_LABEL_FORGETTING_UNSIGNED"
        detail = "source functor still sees species labels"
    elif bool_string(row["ward_identity"]) == "true" and bool_string(row["no_prefactor"]) != "true":
        status = "REFUSED_PRE_ACTION_WEIGHT_COUNTERMODEL"
        detail = "pre-action species prefactors survive current ownership"
    elif bool_string(row["component_source"]) != "true":
        status = "REFUSED_MISSING_COMPONENT_SOURCE"
        detail = "component basis row lacks source-backed coefficient origin"
    elif bool_string(row["parent_vector"]) != "true":
        status = "REFUSED_MISSING_PARENT_DELTAW_VECTOR"
        detail = "component basis exists but parent coefficient vector is missing"
    elif bool_string(row["tau"]) != "true":
        status = "REFUSED_MISSING_TAU_PROJECTION"
        detail = "arena projection tau is missing"
    elif bool_string(row["K_projection"]) != "true":
        status = "REFUSED_MISSING_K_QBAR_PROJECTION"
        detail = "K/Qbar/material projection is missing"
    elif bool_string(row["G_absorption"]) == "true":
        status = "REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_GUARD"
        detail = "relative source components cannot be absorbed into G"
    elif bool_string(row["cancellation"]) == "true":
        status = "REFUSED_CANCELLATION_ONLY"
        detail = "component cancellations require parent identity"
    elif bool_string(row["schema_only"]) == "true":
        status = "SCHEMA_MATH_ONLY_NOT_EVIDENCE"
        detail = "schema math is not evidence"
    else:
        status = "REFUSED_UNCLASSIFIED_NONCLAIM"
        detail = "case remains nonclaim"
    return {
        **row,
        "observed_status": status,
        "status_detail": detail,
        "status_matches_expected": status == row["expected_status"],
        "valid_prediction_row": False,
        "score_ready": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def dryrun_result_rows() -> list[dict[str, Any]]:
    return [validate_dryrun_case(row) for row in dryrun_case_rows()]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN1889_0_Ward_owner",
            "input_kind": "source_current_Ward_owner",
            "runner_status": "REFUSED_WARD_OWNER_NOT_PARENT_DERIVED",
            "reason": "Ward bridge is real but label-forgetting/no-prefactor parent clauses are unsigned",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1889_1_component_basis",
            "input_kind": "Delta_w_component_basis",
            "runner_status": "REFUSED_COMPONENT_BASIS_NOT_NUMERIC_PREDICTION",
            "reason": "basis slots are source-backed acquisition targets but no parent coefficient vector exists",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1889_2_bounds",
            "input_kind": "WEP_R10_clock_orbital_bound_anchors",
            "runner_status": "REFUSED_BOUND_ANCHORS_NOT_PREDICTIONS",
            "reason": "bounds cannot define source-current components",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE1889_0_Ward_owner",
            "claim": "source-current Ward owner derives species-blind coupling",
            "required": "Ward bridge, source-label forgetting, no pre-action prefactors, no spurion return, projected mass calibration",
            "current_status": "BLOCKED_SOURCE_CURRENT_WARD_OWNER_NOT_DERIVED",
            "pass_gate": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1889_1_finite_component_basis",
            "claim": "component basis is score-ready",
            "required": "basis plus parent coefficients plus arena tau/K/Qbar/material projections",
            "current_status": "BLOCKED_COMPONENT_BASIS_ACQUISITION_NONCLAIM",
            "pass_gate": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1889_2_Newton_GR_source",
            "claim": "source side reduces to GR/Newton",
            "required": "one calibrated kappa_univ source plus closed measured-GM projector and no non-Hilbert current",
            "current_status": "BLOCKED_PROJECTED_FLUX_AND_LEFT_HAND_GATES_OPEN",
            "pass_gate": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1889_0_Ward",
            "question": "does Ward conservation prove species-blind source coupling?",
            "answer": "no",
            "basis": "Ward conservation is homogeneous and permits constant species-weighted currents",
            "decision": "WARD_BRIDGE_RETAINED_NOT_PROMOTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1889_1_functor",
            "question": "what theorem would actually close the source coupling?",
            "answer": "label-forgotten source functor plus no pre-action source prefactors",
            "basis": "then the source domain contains only T_total and the covariant additive map has one scalar",
            "decision": "NO_SOURCE_PREFACTOR_PARENT_ACTION_CLAUSE_IS_NEXT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1889_2_fallback",
            "question": "is the component basis ready to score?",
            "answer": "no",
            "basis": "basis slots are now named, but parent coefficients and arena projections are absent",
            "decision": "KEEP_COMPONENT_BASIS_ACQUISITION_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1889_0_primary",
            "selection_status": "selected",
            "target_doc": "1890-Y5-R2FR-no-source-prefactor-parent-action-clause-or-component-basis-first-source-row.md",
            "target_script": "scripts/Y5_R2FR_no_source_prefactor_parent_action_clause_or_component_basis_first_source_row_1890.py",
            "objective": "try to derive the parent no-source-prefactor/no-double-counting matter-normalization clause that forbids w_A before variation; if it fails, source the first nonclaim component-basis row with explicit WEP/R10/PPN projection requirements",
            "success_condition": "parent-signed no-source-prefactor theorem, or first source-backed nonclaim component row with coefficient origin, units, tau/K/Qbar requirements, and no bound-anchor shortcut",
            "do_not": "do not claim local GR, do not use Ward conservation as species-blindness, do not absorb relative components into G, and do not score bound anchors as predictions",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS1889_0_progress",
            "area": "coupling derivation",
            "status": "Ward bridge separated from source-owner theorem",
            "detail": "we now know Ward is necessary support but not the thing that chooses kappa_univ",
            "risk_level": "USEFUL_PROGRESS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "STATUS1889_1_main_bottleneck",
            "area": "no source-prefactor parent clause",
            "status": "unsigned",
            "detail": "the exact missing theorem is that source-only w_A cannot appear before total Hilbert variation",
            "risk_level": "MAIN_BOTTLENECK",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "STATUS1889_2_fallback",
            "area": "finite Delta_w component basis",
            "status": "basis slots named, coefficients missing",
            "detail": "component rows are acquisition targets, not scored predictions",
            "risk_level": "BLOCKED_FOR_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "ward_owner_attempt": ward_owner_attempt_rows(),
        "functor_contract": functor_contract_rows(),
        "component_basis": component_basis_rows(),
        "dryrun_cases": dryrun_case_rows(),
        "dryrun_results": dryrun_result_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details: list[str] = []
    for path in paths:
        try:
            rows = csv_rows(path)
        except Exception as exc:  # noqa: BLE001
            return False, f"{path.name}:{exc}"
        details.append(f"{path.name}:{len(rows)}")
    return True, "; ".join(details)


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    for path in paths:
        for row in csv_rows(path):
            for field in ("valid_for_claim", "claim_allowed"):
                if field in row and bool_string(row[field]) == "true":
                    return False, f"{path.name}:{field}=true"
    return True, "all claim flags false"


def blocked_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            joined = " ".join(row.values()).upper()
            if any(marker in joined for marker in ("MISSING", "UNSIGNED", "BLOCKED", "NOT_DERIVED", "COUNTERMODEL")):
                if bool_string(row.get("score_ready", "false")) == "true" or bool_string(row.get("valid_for_claim", "false")) == "true":
                    return False, f"{path.name}:row{index}:blocked marker marked ready"
    return True, "blocked-marker rows are not claim-ready"


def copy_branch_artifacts() -> None:
    shutil.copy2(OUTPUTS["ward_owner_attempt"], MICROSCOPE_RESIDUALS / OUTPUTS["ward_owner_attempt"].name)
    shutil.copy2(OUTPUTS["functor_contract"], QUEUE / "JR1889_NO_SPECIES_LABEL_FUNCTOR_CONTRACT_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["component_basis"], SOURCE_WEIGHT_TEMPLATE_COPY)
    shutil.copy2(OUTPUTS["dryrun_results"], QUARANTINE / OUTPUTS["dryrun_results"].name)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []

    source_rows = csv_rows(OUTPUTS["source_register"])
    checks.append({"validation_id": "VAL1889_0_sources_exist", "status": "PASS" if all(bool_string(row["exists"]) == "true" for row in source_rows) else "FAIL", "detail": f"{sum(bool_string(row['exists']) == 'true' for row in source_rows)}/{len(source_rows)} sources exist", "valid_for_claim": False})
    checks.append({"validation_id": "VAL1889_1_needles_found", "status": "PASS" if all(row["needle_status"] == "PASS" for row in source_rows) else "FAIL", "detail": f"{sum(row['needle_status'] == 'PASS' for row in source_rows)}/{len(source_rows)} source needles found", "valid_for_claim": False})

    ward_rows = csv_rows(OUTPUTS["ward_owner_attempt"])
    checks.append({"validation_id": "VAL1889_2_Ward_not_promoted", "status": "PASS" if any(row["attempt_id"] == "SWO1889_7_verdict" and row["result"] == "SOURCE_CURRENT_WARD_OWNER_NOT_DERIVED" for row in ward_rows) else "FAIL", "detail": "Ward/source-current owner remains conditional", "valid_for_claim": False})
    checks.append({"validation_id": "VAL1889_3_countermodel_retained", "status": "PASS" if any(row["result"] == "PRE_ACTION_WEIGHT_COUNTERMODEL_SURVIVES" for row in ward_rows) else "FAIL", "detail": "pre-action source-weight countermodel remains explicit", "valid_for_claim": False})

    contract_rows = csv_rows(OUTPUTS["functor_contract"])
    checks.append({"validation_id": "VAL1889_4_functor_contract_fields", "status": "PASS" if {"NSF1889_0_domain", "NSF1889_2_no_prefactors", "NSF1889_5_projected_mass"}.issubset({row["contract_id"] for row in contract_rows}) else "FAIL", "detail": f"functor_contract_rows={len(contract_rows)}", "valid_for_claim": False})

    basis_rows = csv_rows(OUTPUTS["component_basis"])
    checks.append({"validation_id": "VAL1889_5_component_basis_nonclaim", "status": "PASS" if all(bool_string(row["score_ready"]) == "false" and bool_string(row["valid_for_claim"]) == "false" for row in basis_rows) else "FAIL", "detail": f"component_basis_rows={len(basis_rows)} all nonclaim", "valid_for_claim": False})

    dryrun_rows = csv_rows(OUTPUTS["dryrun_results"])
    expected_statuses = {
        "REFUSED_WARD_ONLY_NOT_SPECIES_BLIND",
        "REFUSED_LABEL_FORGETTING_UNSIGNED",
        "REFUSED_PRE_ACTION_WEIGHT_COUNTERMODEL",
        "REFUSED_MISSING_COMPONENT_SOURCE",
        "REFUSED_BOUND_ANCHOR_NOT_PREDICTION",
        "REFUSED_MISSING_TAU_PROJECTION",
        "REFUSED_MISSING_K_QBAR_PROJECTION",
        "REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_GUARD",
        "REFUSED_CANCELLATION_ONLY",
        "SCHEMA_MATH_ONLY_NOT_EVIDENCE",
    }
    observed_statuses = {row["observed_status"] for row in dryrun_rows}
    checks.append({"validation_id": "VAL1889_6_dryrun_failure_modes", "status": "PASS" if expected_statuses.issubset(observed_statuses) and all(bool_string(row["status_matches_expected"]) == "true" for row in dryrun_rows) else "FAIL", "detail": "dryrun_statuses=" + ",".join(row["observed_status"] for row in dryrun_rows), "valid_for_claim": False})

    runner_rows = csv_rows(OUTPUTS["runner_refusal"])
    checks.append({"validation_id": "VAL1889_7_runner_refusal", "status": "PASS" if all(bool_string(row["score_ready"]) == "false" for row in runner_rows) else "FAIL", "detail": "all runners refuse claim scoring", "valid_for_claim": False})

    gate_rows = csv_rows(OUTPUTS["claim_gate"])
    checks.append({"validation_id": "VAL1889_8_claim_gates", "status": "PASS" if all(bool_string(row["pass_gate"]) == "false" for row in gate_rows) else "FAIL", "detail": "all claim gates remain blocked", "valid_for_claim": False})

    decision_rows_loaded = csv_rows(OUTPUTS["decision"])
    checks.append({"validation_id": "VAL1889_9_decision", "status": "PASS" if any(row["decision"] == "NO_SOURCE_PREFACTOR_PARENT_ACTION_CLAUSE_IS_NEXT" for row in decision_rows_loaded) else "FAIL", "detail": "decision selects no-source-prefactor parent action clause next", "valid_for_claim": False})

    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append({"validation_id": "VAL1889_10_next_target", "status": "PASS" if any(row["route_id"] == "NEXT1889_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL", "detail": "1890 no-source-prefactor/component first row selected", "valid_for_claim": False})

    status_rows = csv_rows(OUTPUTS["project_status"])
    checks.append({"validation_id": "VAL1889_11_project_status", "status": "PASS" if any(row["risk_level"] == "MAIN_BOTTLENECK" for row in status_rows) else "FAIL", "detail": "project status snapshot keeps no-source-prefactor clause as main bottleneck", "valid_for_claim": False})

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append({"validation_id": "VAL1889_12_claim_flags_false", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})

    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append({"validation_id": "VAL1889_13_blocked_markers_not_ready", "status": "PASS" if blocked_ok else "FAIL", "detail": blocked_detail, "valid_for_claim": False})

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1889_14_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["ward_owner_attempt"].name,
        QUEUE / "JR1889_NO_SPECIES_LABEL_FUNCTOR_CONTRACT_NONCLAIM.csv",
        SOURCE_WEIGHT_TEMPLATE_COPY,
        QUARANTINE / OUTPUTS["dryrun_results"].name,
    ]
    checks.append({"validation_id": "VAL1889_15_branch_copies", "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL", "detail": ";".join(str(path) for path in copied_paths), "valid_for_claim": False})

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1889_16_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})

    formalization_hits = list(FORMALIZATION.rglob("*1889*")) if FORMALIZATION.exists() else []
    checks.append({"validation_id": "VAL1889_17_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1889_count={len(formalization_hits)}", "valid_for_claim": False})

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1889_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1889 source-current Ward owner or real Delta_w component basis", "valid_for_claim": False})
    return checks


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1889 - Source-Current Ward Owner Or Real Delta_w Component Basis

**Private status:** derivation-first coupling checkpoint; no WEP/R10/PPN/Newton/local-GR claim.

## Result

1889 separates the Ward bridge from the actual source-owner theorem:

```text
diffeomorphism Ward identity -> conserves the current in the action
not -> proves the action chose a species-blind current
```

The useful conditional theorem is now exact:

```text
q_src({{(T_A,A)}})=T_total
F_src local + covariant + additive on one observed coframe
=> F_src(T_total)=kappa_univ T_total
```

But that only fires if the parent first forgets species labels and forbids pre-variation source prefactors. If `S_matter=sum_A w_A S_A` is legal, Ward conservation still survives while `T_source=sum_A w_A T_A` changes. So the next theorem is not “Ward harder”; it is the parent no-source-prefactor/no-double-counting matter-normalization clause.

The fallback is improved too: 1889 names a real nonclaim component-basis acquisition pack instead of one vague `Delta_w`.

## Source-Current Ward Owner Attempt

{markdown_table(rows_by_name["ward_owner_attempt"])}

## No-Species-Label Functor Contract

{markdown_table(rows_by_name["functor_contract"])}

## Real Delta_w Component-Basis Acquisition

{markdown_table(rows_by_name["component_basis"])}

## Component-Basis Dry-Run Cases

{markdown_table(rows_by_name["dryrun_cases"])}

## Component-Basis Dry-Run Results

{markdown_table(rows_by_name["dryrun_results"])}

## Runner Refusal

{markdown_table(rows_by_name["runner_refusal"])}

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = all_output_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()

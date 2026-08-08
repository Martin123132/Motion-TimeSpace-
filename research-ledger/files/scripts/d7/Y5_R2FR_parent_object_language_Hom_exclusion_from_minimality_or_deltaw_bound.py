from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1762"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1762_0_1761_handoff",
        "source_key": "1761_hom_next",
        "source_path": ROOT / "1761-Y5-R2FR-no-direct-matter-X-vertex-grammar-or-Amatter-coefficient-pack.md",
        "needles": ["NEXT1761_0_primary", "Hom"],
    },
    {
        "source_id": "SRC1762_1_1761_hom",
        "source_key": "1761_no_source_only_hom_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1761_NO_SOURCE_ONLY_HOM_AUDIT.csv",
        "needles": ["HOM1761_4_verdict", "FAIL_CURRENT_CLAIM_HOM_NOT_DERIVED"],
    },
    {
        "source_id": "SRC1762_2_1761_coeff",
        "source_key": "1761_deltaw_coeff_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1761_AMATTER_COEFFICIENT_PACK.csv",
        "needles": ["CP1761_1_delta_w_A", "RETAINED_RESIDUAL_SYMBOLIC"],
    },
    {
        "source_id": "SRC1762_3_1758_doc",
        "source_key": "1758_minimality_invariant_doc",
        "source_path": ROOT / "1758-Y5-R2FR-primitive-minimality-invariant-algebra-or-Aaffine-bound.md",
        "needles": ["PRIMITIVE_MINIMALITY_NOT_PROVED", "LOCAL_INVARIANT_ALGEBRA_NOT_TRIVIALIZED"],
    },
    {
        "source_id": "SRC1762_4_1758_minimality",
        "source_key": "1758_primitive_minimality",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1758_PRIMITIVE_MINIMALITY_ATTEMPT.csv",
        "needles": ["PM1758_2_material_marker_no_extension", "NOT_DERIVED"],
    },
    {
        "source_id": "SRC1762_5_1758_invariant",
        "source_key": "1758_invariant_algebra",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1758_INVARIANT_ALGEBRA_AUDIT.csv",
        "needles": ["IA1758_0_target", "MISSING_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY"],
    },
    {
        "source_id": "SRC1762_6_1758_constants",
        "source_key": "1758_constant_source",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1758_CONSTANT_SOURCE_UNIVERSALITY_AUDIT.csv",
        "needles": ["CS1758_6_verdict", "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED"],
    },
    {
        "source_id": "SRC1762_7_573_minimality",
        "source_key": "573_primitive_minimality",
        "source_path": RESIDUALS / "P8_Y5_R10_573_PRIMITIVE_MINIMAL_THEOREM_ATTEMPT.csv",
        "needles": ["PM573_3_local_invariant_algebra", "fail_current_claim"],
    },
    {
        "source_id": "SRC1762_8_573_debt",
        "source_key": "573_invariant_generator_debt",
        "source_path": RESIDUALS / "P8_Y5_R10_573_INVARIANT_GENERATOR_DEBT.csv",
        "needles": ["IG573_4_species_constants", "not_universalized"],
    },
    {
        "source_id": "SRC1762_9_575_lock",
        "source_key": "575_constant_source_lock",
        "source_path": RESIDUALS / "P8_Y5_R10_575_CONSTANT_SOURCE_LOCK_CONTRACT.csv",
        "needles": ["CL575_4_universal_coupling", "not_parent_derived"],
    },
    {
        "source_id": "SRC1762_10_953_contract",
        "source_key": "953_parent_category_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_953_PARENT_CATEGORY_CONTRACT.csv",
        "needles": ["PMC953_1_label_forgetting_quotient", "PMC953_5_contract_verdict"],
    },
    {
        "source_id": "SRC1762_11_953_theorem",
        "source_key": "953_source_functor_theorem",
        "source_path": RESIDUALS / "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv",
        "needles": ["NSF953_2_conditional_uniqueness", "conditional_proof_not_parent_derivation"],
    },
    {
        "source_id": "SRC1762_12_954_clause",
        "source_key": "954_parent_action_clause",
        "source_path": RESIDUALS / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
        "needles": ["PAC954_1_no_source_prefactors", "exact_high_pressure_missing_clause"],
    },
    {
        "source_id": "SRC1762_13_955_minimal",
        "source_key": "955_minimal_matter_action_lemma",
        "source_path": RESIDUALS / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
        "needles": ["MMA955_3_relative_prefactor", "counterexample_survives"],
    },
    {
        "source_id": "SRC1762_14_955_classification",
        "source_key": "955_prefactor_classification",
        "source_path": RESIDUALS / "P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv",
        "needles": ["SPC955_2_relative_species_weight", "live_countermodel"],
    },
    {
        "source_id": "SRC1762_15_1488_doc",
        "source_key": "1488_hom_and_deltaw_lock_doc",
        "source_path": ROOT / "1488-Y5-R10-RAB-ordinary-matter-subaction-current-chain-owner-or-explicit-wA-residual-lock.md",
        "needles": ["HOMG1488_5_verdict", "WA1488_7_lock_verdict"],
    },
    {
        "source_id": "SRC1762_16_1488_hom",
        "source_key": "1488_no_source_only_hom_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_1488_NO_SOURCE_ONLY_HOM_GATE.csv",
        "needles": ["HOMG1488_5_verdict", "not parent-derived"],
    },
    {
        "source_id": "SRC1762_17_1488_deltaw",
        "source_key": "1488_wA_deltaW_lock",
        "source_path": RESIDUALS / "P8_Y5_R10_1488_WA_DELTAW_RESIDUAL_LOCK.csv",
        "needles": ["WA1488_1_component_vector", "NONCLAIM_LOCK"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1762_SOURCE_REGISTER.csv",
    "hom_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1762_HOM_EXCLUSION_THEOREM_ATTEMPT.csv",
    "minimality_import": RESIDUALS / "P8_Y5_PARENT_QLOC_1762_MINIMALITY_IMPORT_AUDIT.csv",
    "invariant_hom": RESIDUALS / "P8_Y5_PARENT_QLOC_1762_INVARIANT_ALGEBRA_HOM_AUDIT.csv",
    "source_functor": RESIDUALS / "P8_Y5_PARENT_QLOC_1762_LABEL_FORGETTING_SOURCE_FUNCTOR_AUDIT.csv",
    "deltaw_bound": RESIDUALS / "P8_Y5_PARENT_QLOC_1762_DELTAW_BOUND_INTERFACE.csv",
    "source_zero_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1762_SOURCE_ZERO_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1762_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1762_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1762_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1762_VALIDATION.csv",
}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": all(needle in text for needle in needles),
                "needles": ";".join(needles),
                "role": "parent object-language Hom exclusion from minimality or delta_w bound",
                "valid_for_claim": False,
            }
        )
    return rows


def hom_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HOM1762_0_target",
            "claim_piece": "no source-only Hom theorem",
            "mathematical_form": "Hom_parent(SpeciesLabel or I_hid or ReadoutSelector, R_+ active-source-prefactor)=CommonConst only",
            "theorem_status": "TARGET_EXACT",
            "proof_result": "WOULD_KILL_DELTA_W_AND_A_DIRECT_PREFACOR_BRANCH",
            "gap": "needs parent object language, primitive minimality, invariant algebra triviality, label-forgetting source functor and constant/source universality",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HOM1762_1_conditional_meta_theorem",
            "claim_piece": "minimal typed grammar implies no source-only prefactor",
            "mathematical_form": "If Obj_parent has only q-owned geometry, matter fields, gauge data, fixed Rep labels and CommonConst, no object exists that can feed w_A except CommonConst",
            "theorem_status": "EXACT_CONDITIONAL_META_THEOREM",
            "proof_result": "relative w_A undefined; only w_star calibration remains",
            "gap": "current MTS has not parent-signed that object inventory",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HOM1762_2_minimality_import",
            "claim_piece": "primitive minimality supplies object inventory",
            "mathematical_form": "Conf_parent=Q_MTS and no Q_tilde=(Q_MTS,m)/G_rel marker/source extension",
            "theorem_status": "BLOCKED_CURRENT_CLAIM",
            "proof_result": "fixed external labels excluded conditionally, but co-moving material/source markers remain legal",
            "gap": "material marker no-extension theorem is not derived",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HOM1762_3_invariant_algebra_import",
            "claim_piece": "local invariant algebra has no source-prefactor generators",
            "mathematical_form": "I_loc(Q_MTS)=I_geom[J^k(e_obs)] tensor Const, with no fibre/domain/chi/memory/species/readout generators",
            "theorem_status": "BLOCKED_CURRENT_CLAIM",
            "proof_result": "generator debts remain",
            "gap": "finite fibre spectrum, domain class, chi_D, memory scalar, species constants and readout projector are not eliminated",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HOM1762_4_source_functor_import",
            "claim_piece": "label-forgetting source functor removes species weights",
            "mathematical_form": "q_src({(T_A,A)})=T_total before F_src; covariant additive F_src gives kappa_univ T_total",
            "theorem_status": "EXACT_CONDITIONAL_THEOREM_PARENT_UNSIGNED",
            "proof_result": "if source labels are forgotten before coupling, relative kappa_A/w_A vanish",
            "gap": "label forgetting is a parent category contract, not a derived parent theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "HOM1762_5_current_verdict",
            "claim_piece": "current MTS signs no-source-only Hom",
            "mathematical_form": "HOM1762_1 through HOM1762_4 close in one parent branch",
            "theorem_status": "THEOREM_CONTRACT_READY_PARENT_UNSIGNED",
            "proof_result": "DELTA_W_RETAINED",
            "gap": "minimality and invariant algebra fail current claim; constant/source universality and label forgetting remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def minimality_import_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "MIN1762_0_fixed_spurions",
            "import_clause": "fixed external labels are excluded",
            "mathematical_form": "m_fixed is not a function on Q=Phi/G_rep",
            "current_status": "CONDITIONAL_PASS_IF_STRICT_QUOTIENT",
            "effect_on_hom": "removes non-orbit covectors as parent-action source weights",
            "remaining_gap": "does not exclude co-moving material markers or quotient-invariant class scalars",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "MIN1762_1_no_marker_extension",
            "import_clause": "no co-moving material/source marker quotient extension",
            "mathematical_form": "Conf_parent=Q_MTS, not Q_tilde=(Q_MTS,m)/G_rel",
            "current_status": "NOT_DERIVED",
            "effect_on_hom": "would forbid Hom(m, R_+ source prefactor)",
            "remaining_gap": "current corpus does not prove marker extensions impossible",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "MIN1762_2_no_marker_functor",
            "import_clause": "no nonconstant natural marker functor on local branch",
            "mathematical_form": "Nat(Q_MTS, Marker)_loc = constants",
            "current_status": "REDUCED_TO_INVARIANT_ALGEBRA_TRIVIALITY",
            "effect_on_hom": "would reduce hidden-marker Hom to common constants",
            "remaining_gap": "local invariant algebra still has source-like generators",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "MIN1762_3_verdict",
            "import_clause": "primitive minimality derives no-source-only Hom",
            "mathematical_form": "MIN1762_0 through MIN1762_2 close with source-label forgetting",
            "current_status": "FAIL_CURRENT_CLAIM_MINIMALITY_NOT_PROVED",
            "effect_on_hom": "would remove delta_w_marker and direct marker source weights",
            "remaining_gap": "retain delta_w_marker/A_marker/A_direct rows",
            "valid_for_claim": False,
        },
    ]


def invariant_hom_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "generator_id": "IH1762_0_target",
            "generator": "target local invariant algebra",
            "hom_risk": "I_loc(Q_MTS)=I_geom[J^k(e_obs)] tensor Const would leave only common source calibration",
            "current_status": "TARGET_EXACT",
            "hom_if_survives": "none if proved",
            "needed_elimination": "MISSING_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "generator_id": "IH1762_1_fibre",
            "generator": "finite_cell_fibre_spectrum",
            "hom_risk": "can act as material/source marker or effective charge label",
            "current_status": "NOT_TRIVIALIZED",
            "hom_if_survives": "delta_w_hidden or delta_w_species",
            "needed_elimination": "MISSING_FIBRE_SPECTRUM_UNIVERSAL_OR_GAUGE_PROOF",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "generator_id": "IH1762_2_domain",
            "generator": "relative_boundary_domain_class",
            "hom_risk": "can carry local source class, boundary/domain charge, or worldtube mask",
            "current_status": "NOT_DERIVED",
            "hom_if_survives": "delta_w_marker or delta_w_readout",
            "needed_elimination": "MISSING_LOCAL_TRIVIAL_CLASS_OR_CLASS_NOHAIR",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "generator_id": "IH1762_3_selector",
            "generator": "chi_D/domain_selector",
            "hom_risk": "can become preferred-frame/source-normalization/R10/R11 marker",
            "current_status": "NOT_DERIVED",
            "hom_if_survives": "delta_w_hidden or source-normalization coefficient",
            "needed_elimination": "MISSING_SELECTOR_GAUGE_OR_LOCAL_TRIVIAL_BRANCH",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "generator_id": "IH1762_4_memory",
            "generator": "memory_or_class_scalar",
            "hom_risk": "can enter clock/source/fifth-force channels",
            "current_status": "NOT_SILENCED_AS_THEOREM",
            "hom_if_survives": "delta_w_hidden or A_mu_even",
            "needed_elimination": "MISSING_LOCAL_VALUE_GRADIENT_ZERO_OR_BOUND",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "generator_id": "IH1762_5_species_constants",
            "generator": "species_charge_constants",
            "hom_risk": "can generate theta_A(X), kappa_A, source weights or relative matter normalization",
            "current_status": "NOT_UNIVERSALIZED",
            "hom_if_survives": "delta_w_species, b_theta or b_kappa",
            "needed_elimination": "MISSING_CONSTANT_SOURCE_UNIVERSALITY",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "generator_id": "IH1762_6_readout",
            "generator": "post_readout_projector",
            "hom_risk": "can re-enter as reduced-action source after apparent closure",
            "current_status": "NO_CHEAT_RULE_ONLY",
            "hom_if_survives": "delta_w_readout",
            "needed_elimination": "MISSING_FULL_PARENT_DOMAIN_READOUT_AUDIT",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "generator_id": "IH1762_7_verdict",
            "generator": "source-prefactor generator debts",
            "hom_risk": "at least one legal Hom source target remains unless all generators are eliminated or bounded",
            "current_status": "FAIL_CURRENT_CLAIM_GENERATOR_DEBTS_RETAINED",
            "hom_if_survives": "delta_w coefficient pack remains mandatory",
            "needed_elimination": "derive each generator zero or source each coefficient",
            "valid_for_claim": False,
        },
    ]


def source_functor_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SF1762_0_label_forgetting",
            "required_clause": "source functor sees total Hilbert current, not labelled family",
            "mathematical_form": "q_src({(T_A,A)})=T_total=sum_A T_A",
            "current_status": "EXACT_MATH_CONTRACT_PARENT_UNSIGNED",
            "if_signed": "species labels cannot feed relative source weight",
            "if_unsigned": "delta_w_species remains",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SF1762_1_covariant_additive_map",
            "required_clause": "source map is natural, covariant, additive and local after labels are forgotten",
            "mathematical_form": "F_src(T+U)=F_src(T)+F_src(U), F_src(phi_*T)=phi_*F_src(T)",
            "current_status": "CONDITIONAL_THEOREM_CLEAN",
            "if_signed": "one scalar kappa_univ remains",
            "if_unsigned": "cannot infer unique source coupling",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SF1762_2_common_calibration",
            "required_clause": "common scalar is calibrated by measured G and not treated as composition field",
            "mathematical_form": "kappa_univ <-> 8 pi G_ref/c^4",
            "current_status": "COMMON_MODE_ONLY",
            "if_signed": "w_star/kappa common mode separated from residual vector",
            "if_unsigned": "common normalization nuisance remains but not a relative WEP proof",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SF1762_3_no_hidden_return",
            "required_clause": "no hidden constants, masks, markers, boundary classes or post-readout maps reintroduce species dependence",
            "mathematical_form": "partial_A kappa=partial_m kappa=partial_boundary kappa=partial_D kappa=0",
            "current_status": "NAMED_BY_CONTRACTS_NOT_PARENT_SIGNED",
            "if_signed": "delta_w_hidden/marker/readout close",
            "if_unsigned": "source weights return under another name",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SF1762_4_verdict",
            "required_clause": "source functor derives no-source-only Hom",
            "mathematical_form": "SF1762_0 through SF1762_3 all signed",
            "current_status": "FAIL_CURRENT_CLAIM_SOURCE_FUNCTOR_PARENT_UNSIGNED",
            "if_signed": "relative delta_w_A=0",
            "if_unsigned": "retain delta_w component vector",
            "valid_for_claim": False,
        },
    ]


def deltaw_bound_rows() -> list[dict[str, Any]]:
    source_path = str(RESIDUALS / "P8_Y5_PARENT_QLOC_1761_AMATTER_COEFFICIENT_PACK.csv")
    return [
        {
            "branch_id": BRANCH_ID,
            "bound_id": "DW1762_0_zero_condition",
            "quantity": "Z_delta_w",
            "required_form": "True only if minimality, invariant algebra, label-forgetting source functor, no hidden return and constant/source universality are all parent-signed",
            "current_status": "FALSE_PARENT_UNSIGNED",
            "units": "dimensionless",
            "formula": "delta_w_A=0 theorem condition",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "DW1762_1_delta_w_A",
            "quantity": "delta_w_A",
            "required_form": "component vector over source-relevant ordinary matter sectors with declared basis and norm",
            "current_status": "MISSING_COMPONENT_BASIS_OR_THEOREM_ZERO",
            "units": "dimensionless",
            "formula": "w_A=w_star(1+delta_w_A)",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "DW1762_2_delta_w_species",
            "quantity": "delta_w_species",
            "required_form": "species-label source prefactor bound or Hom(species,R_+) zero theorem",
            "current_status": "MISSING_HOM_SPECIES_EXCLUSION_OR_NUMERIC_BOUND",
            "units": "dimensionless",
            "formula": "relative species source-weight amplitude",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "DW1762_3_delta_w_hidden",
            "quantity": "delta_w_hidden",
            "required_form": "hidden invariant source coefficient bound or invariant-algebra zero theorem",
            "current_status": "MISSING_HIDDEN_INVARIANT_ZERO_OR_BOUND",
            "units": "dimensionless",
            "formula": "source-prefactor dependence on hidden invariant",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "DW1762_4_delta_w_marker",
            "quantity": "delta_w_marker",
            "required_form": "material/domain/boundary marker coefficient bound or no-marker theorem",
            "current_status": "MISSING_NO_MARKER_THEOREM_OR_BOUND",
            "units": "dimensionless",
            "formula": "source-prefactor dependence on co-moving marker/domain class",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "DW1762_5_delta_w_readout",
            "quantity": "delta_w_readout",
            "required_form": "readout/worldtube transfer coefficient bound or before-readout owner theorem",
            "current_status": "MISSING_READOUT_TRANSFER_ZERO_OR_BOUND",
            "units": "dimensionless",
            "formula": "post-variation source-mask/source-support transfer",
            "source_path": source_path,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "DW1762_6_A_direct_response",
            "quantity": "A_direct_matter",
            "required_form": "||delta_v V_m||_{E*} <= K_w ||delta_w|| or theorem-zero",
            "current_status": "MISSING_K_W_OPERATOR_NORM_DELTAW_NORM_OR_THEOREM_ZERO",
            "units": "E*_dual_or_declared_arena_units",
            "formula": "A_direct_matter response to source-prefactor vector",
            "source_path": source_path,
            "valid_for_claim": False,
        },
    ]


def source_zero_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1762_0_Hom",
            "quantity": "no-source-only Hom",
            "current_status": "NOT_DERIVED",
            "evidence": "conditional meta-theorem written, but minimality/invariant/source-functor clauses are parent-unsigned",
            "remaining_gap": "primitive minimality, local invariant algebra triviality, label forgetting and no hidden return",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1762_1_delta_w",
            "quantity": "delta_w_A",
            "current_status": "RETAINED_NONCLAIM",
            "evidence": "relative prefactor countermodel survives unless Hom exclusion is parent-signed",
            "remaining_gap": "component basis, numeric/source-backed bounds or theorem-zero",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1762_2_A_direct",
            "quantity": "A_direct_matter",
            "current_status": "NOT_ZEROED",
            "evidence": "A_direct can be killed by no-Hom/no-marker/no-hidden-frame package, but package fails current claim",
            "remaining_gap": "K_w, E* norm, delta_w bounds, or zero theorem",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1762_3_local_GR",
            "quantity": "GR/Newton source side",
            "current_status": "NOT_CLAIMABLE",
            "evidence": "source-side matter grammar is still nonclaim; other hidden-source channels remain from 1756",
            "remaining_gap": "A_hidden_total still open plus source-to-Poisson/orbital calibration gates",
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1762_0_conditional_theorem",
            "decision": "NO_HOM_THEOREM_IS_EXACT_CONDITIONAL",
            "reason": "minimal typed object language plus label forgetting leaves only a common calibration constant",
            "next_action": "keep the theorem as parent-action contract",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1762_1_current_result",
            "decision": "NO_HOM_NOT_PARENT_DERIVED",
            "reason": "primitive minimality and invariant algebra triviality are not proved; source functor label forgetting remains unsigned",
            "next_action": "do not set delta_w_A or A_direct_matter to zero",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1762_2_bound",
            "decision": "DELTAW_BOUND_INTERFACE_WRITTEN_NONCLAIM",
            "reason": "if the theorem stalls, delta_w must become a finite residual vector with declared basis, units and source paths",
            "next_action": "use bound rows only as nonclaim plumbing until sourced",
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1762_3_best_next",
            "decision": "INVARIANT_GENERATOR_ELIMINATION_IS_NEXT_BEST_DERIVATION_ROUTE",
            "reason": "no-Hom now reduces to the same live debts: fibre/domain/chi/memory/species/readout generators",
            "next_action": "build 1763 invariant-generator elimination priority or delta_w bound source acquisition",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1762_0_no_Hom",
            "claim": "no-source-only Hom is parent-derived",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_MINIMALITY_INVARIANT_ALGEBRA_LABEL_FORGETTING_UNSIGNED",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1762_1_delta_w_zero",
            "claim": "delta_w_A=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_NO_HOM_NOT_DERIVED",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1762_2_delta_w_bound",
            "claim": "delta_w_A is finite and source-backed",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_COMPONENT_BASIS_NUMERIC_BOUNDS_AND_SOURCE_PATHS_MISSING",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1762_3_A_direct_zero_or_bound",
            "claim": "A_direct_matter is zero or source-backed finite",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_K_W_ESTAR_NORM_AND_DELTAW_VECTOR_MISSING",
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1762_4_local_GR_Newton",
            "claim": "local GR/Newton/PPN/R10/WEP/clock/orbital branch can claim",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_SIDE_AND_HIDDEN_SOURCE_ENVELOPE_NOT_CLOSED",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1762_0_primary",
            "next_target": "1763-Y5-R2FR-invariant-generator-elimination-priority-or-deltaw-source-acquisition.md",
            "script": "scripts/Y5_R2FR_invariant_generator_elimination_priority_or_deltaw_source_acquisition.py",
            "objective": "rank fibre/domain/chi/memory/species/readout generator debts by their ability to source delta_w and A_direct; attempt the least-scrutiny zero proof first, otherwise create source-ready bound rows",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1762_1_fallback",
            "next_target": "1763b-Y5-R2FR-deltaw-component-bound-source-pack.md",
            "script": "scripts/Y5_R2FR_deltaw_component_bound_source_pack.py",
            "objective": "build a nonclaim component-basis and source-acquisition pack for delta_w_species, delta_w_hidden, delta_w_marker and delta_w_readout",
            "selection_status": "held_fallback",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "hom_theorem": hom_theorem_rows(),
        "minimality_import": minimality_import_rows(),
        "invariant_hom": invariant_hom_rows(),
        "source_functor": source_functor_rows(),
        "deltaw_bound": deltaw_bound_rows(),
        "source_zero_status": source_zero_status_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv_ok(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            return bool(list(csv.DictReader(handle)))
    except Exception:
        return False


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1762_SOURCE_REGISTER.csv")
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1762_{key.upper()}.csv")


def claim_like_field(key: str) -> bool:
    return key.lower() in {
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "prediction_allowed",
        "score_allowed",
        "claim_pass",
    }


def boolish_true(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if claim_like_field(key) and boolish_true(value):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    status_keys = {"current_status", "theorem_status", "status", "row_status", "proof_result"}
    for rows in rows_map.values():
        for row in rows:
            combined_status = " ".join(str(row.get(key, "")) for key in status_keys)
            if "MISSING_" in combined_status:
                for key, value in row.items():
                    if claim_like_field(key) and boolish_true(value):
                        return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1762_SOURCE_REGISTER.csv").exists():
        return False
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1762_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched_for_1762() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1762*"))


def csv_parse_all() -> bool:
    return all(parse_csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def conditional_theorem_present(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["theorem_id"] == "HOM1762_1_conditional_meta_theorem"
        and row["theorem_status"] == "EXACT_CONDITIONAL_META_THEOREM"
        and row["valid_for_claim"] is False
        for row in rows_map["hom_theorem"]
    )


def hom_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["theorem_id"] == "HOM1762_5_current_verdict"
        and row["proof_result"] == "DELTA_W_RETAINED"
        and row["valid_for_claim"] is False
        for row in rows_map["hom_theorem"]
    )


def generator_debts_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["generator_id"] == "IH1762_7_verdict"
        and row["current_status"] == "FAIL_CURRENT_CLAIM_GENERATOR_DEBTS_RETAINED"
        and row["valid_for_claim"] is False
        for row in rows_map["invariant_hom"]
    )


def deltaw_interface_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["deltaw_bound"]
    return any(row["quantity"] == "delta_w_A" and row["valid_for_claim"] is False for row in rows) and all(
        row["valid_for_claim"] is False for row in rows
    )


def source_zero_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["status_id"] == "SZ1762_3_local_GR"
        and row["current_status"] == "NOT_CLAIMABLE"
        and row["claim_allowed"] is False
        for row in rows_map["source_zero_status"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["route_id"] == "NEXT1762_0_primary" and row["selection_status"] == "selected"
        for row in rows_map["next_target"]
    )


def check_row(check_id: str, condition: bool, pass_detail: str, fail_detail: str) -> dict[str, str]:
    return {
        "branch_id": BRANCH_ID,
        "check_id": check_id,
        "result": "PASS" if condition else "FAIL",
        "detail": pass_detail if condition else fail_detail,
    }


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    sources = rows_map["source_register"]
    claim_gates = rows_map["claim_gate"]
    checks = [
        check_row("VAL1762_0_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check_row("VAL1762_1_needles_present", all(row["needles_present"] for row in sources), "required source needles are present", "one or more source needles missing"),
        check_row("VAL1762_2_conditional_theorem", conditional_theorem_present(rows_map), "no-Hom conditional theorem recorded", "conditional no-Hom theorem missing or promoted"),
        check_row("VAL1762_3_hom_not_promoted", hom_not_promoted(rows_map), "no-Hom theorem remains unpromoted", "no-Hom theorem promoted or verdict missing"),
        check_row("VAL1762_4_generator_debts_retained", generator_debts_retained(rows_map), "invariant-generator debts retained", "generator debt verdict missing or promoted"),
        check_row("VAL1762_5_deltaw_interface_nonclaim", deltaw_interface_nonclaim(rows_map), "delta_w interface remains nonclaim", "delta_w interface missing or promoted"),
        check_row("VAL1762_6_source_zero_blocked", source_zero_blocked(rows_map), "source/local-GR status remains blocked", "source/local-GR status missing or promoted"),
        check_row("VAL1762_7_claim_gates_safe", all(row["gate_pass"] is False and row["status"] == "BLOCKED" for row in claim_gates), "all claim gates remain blocked", "one or more claim gates opened"),
        check_row("VAL1762_8_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL1762_9_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row(
            "VAL1762_10_decision_next",
            any(row["decision_id"] == "DEC1762_3_best_next" and row["decision"] == "INVARIANT_GENERATOR_ELIMINATION_IS_NEXT_BEST_DERIVATION_ROUTE" for row in rows_map["decision"]),
            "decision selects invariant-generator elimination route",
            "best-next decision missing",
        ),
        check_row("VAL1762_11_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL1762_12_csv_parse", csv_parse_all(), "all generated 1762 CSVs parse", "one or more generated 1762 CSVs fail to parse"),
        check_row("VAL1762_13_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "branch copies missing"),
        check_row("VAL1762_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check_row("VAL1762_15_formalization_untouched", formalization_untouched_for_1762(), "no 1762 outputs found under formalization-workbench", "1762 outputs found under formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in checks)
    checks.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1762_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1762 parent object-language Hom exclusion from minimality or delta_w bound",
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    sections = [
        "# 1762 - Parent Object-Language Hom Exclusion From Minimality Or Delta_w Bound",
        "",
        "## Verdict",
        "- 1762 tries the clean derivation path for the `delta_w_A` obstruction: prove there is no parent object-language morphism from species/hidden/readout data to an active-source prefactor, except a common calibration constant.",
        "- The conditional theorem is exact: primitive minimality + local invariant-algebra triviality + fixed representation data + label-forgetting source functor would make relative `w_A` undefined and leave only `w_star`.",
        "- Current MTS does not yet parent-sign the needed package. Fixed external labels can be excluded conditionally, but co-moving material markers, invariant generators, species constants, and readout/worldtube masks remain legal.",
        "- Therefore `delta_w_A`, `A_direct_matter`, and the `A_matter` source envelope remain explicit nonclaim residuals.",
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Hom Exclusion Theorem Attempt",
        markdown_table(rows_map["hom_theorem"], ["theorem_id", "claim_piece", "mathematical_form", "theorem_status", "proof_result", "gap"]),
        "",
        "## Minimality Import Audit",
        markdown_table(rows_map["minimality_import"], ["audit_id", "import_clause", "mathematical_form", "current_status", "effect_on_hom", "remaining_gap"]),
        "",
        "## Invariant Algebra Hom Audit",
        markdown_table(rows_map["invariant_hom"], ["generator_id", "generator", "hom_risk", "current_status", "hom_if_survives", "needed_elimination"]),
        "",
        "## Label-Forgetting Source Functor Audit",
        markdown_table(rows_map["source_functor"], ["audit_id", "required_clause", "mathematical_form", "current_status", "if_signed", "if_unsigned"]),
        "",
        "## Delta-w Bound Interface",
        markdown_table(rows_map["deltaw_bound"], ["bound_id", "quantity", "required_form", "current_status", "units", "formula"]),
        "",
        "## Source-Zero Status",
        markdown_table(rows_map["source_zero_status"], ["status_id", "quantity", "current_status", "evidence", "remaining_gap"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "This is a useful squeeze. The source-prefactor problem is no longer a vague coupling worry: it is exactly a missing parent object-language theorem. If minimality and invariant algebra close, `delta_w_A` disappears as a definable object. If they do not, `delta_w_A` is not philosophical weakness; it is a finite source vector to bound. The next derivation-first step should rank and attack the surviving invariant generators, because they are now the live source of the no-Hom failure.",
        "",
    ]
    return "\n".join(sections)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1762-Y5-R2FR-parent-object-language-Hom-exclusion-from-minimality-or-deltaw-bound.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1762 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()

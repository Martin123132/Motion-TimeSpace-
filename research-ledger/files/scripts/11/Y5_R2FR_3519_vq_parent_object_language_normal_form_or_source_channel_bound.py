from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3519-Y5-R2FR-vq-parent-object-language-normal-form-or-source-channel-bound.md"
CANONICAL_NORMAL_FORM = OUT / "P8_EM_vq_parent_object_language_normal_form_candidate.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3519": {"path": Path(__file__).resolve(), "role": "3519 generator"},
    "doc_3518": {
        "path": ROOT / "3518-Y5-R2FR-vq-private-first-class-source-vector-silence-or-Dq-bound.md",
        "role": "3518 v_q two-gate handoff",
    },
    "next_3518": {
        "path": OUT / "P8_Y5_R2FR_3518_NEXT_TARGET.csv",
        "role": "3519 target handoff",
    },
    "components_3518": {
        "path": OUT / "P8_Y5_R2FR_3518_VQ_SOURCE_VECTOR_COMPONENTS.csv",
        "role": "3518 live q source-vector components",
    },
    "status_3518": {
        "path": OUT / "P8_EM_vq_private_firstclass_source_silence_status.csv",
        "role": "canonical v_q source-silence status",
    },
    "q_slot_2299": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2299_Q_SOURCE_SLOT_EXCLUSION_ATTEMPT.csv",
        "role": "q source-slot exclusion attempt",
    },
    "bqweyl_index_2302": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2302_BQWEYL_INDEX_ZERO_THEOREM_GATE.csv",
        "role": "conditional B_qWeyl index-zero gate",
    },
    "object_index_2304": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2304_OBJECT_LANGUAGE_INDEX_LEMMA.csv",
        "role": "object-language Weyl index lemma",
    },
    "linear_bqweyl_2365": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2365_LINEAR_BQWEYL_ZERO_AUDIT.csv",
        "role": "linear B_qWeyl audit",
    },
    "source_pack_2367": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2367_FINITE_JQ_SOURCE_PACK.csv",
        "role": "finite J_q source pack",
    },
    "typed_2434": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2434_TYPED_OBJECT_LANGUAGE_CERTIFICATE.csv",
        "role": "typed parent object-language certificate attempt",
    },
    "source_pref_2650": {
        "path": OUT / "P8_Y5_SOURCE_PREF_OBJECTLANG_2650_NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_ATTEMPT.csv",
        "role": "no source-prefactor object-language attempt",
    },
    "species_weight_2677": {
        "path": OUT / "P8_Y5_R2FR_2677_NO_SPECIES_ACTION_WEIGHT_OBJECT_LANGUAGE_AUDIT.csv",
        "role": "no species/action weight audit",
    },
    "qvis_2910": {
        "path": OUT / "P8_Y5_R2FR_2910_QVIS_OBJECT_LANGUAGE_GATE.csv",
        "role": "Qvis object-language gate",
    },
    "parent_object_3380": {
        "path": OUT / "P8_Y5_R2FR_3380_PARENT_OBJECT_LANGUAGE.csv",
        "role": "latest parent object-language candidate",
    },
}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(metadata["path"]),
            "exists": bool_text(Path(metadata["path"]).exists()),
            "role": metadata["role"],
            "valid_for_claim": "False",
        }
        for source_id, metadata in SOURCES.items()
    ]


def normal_form_rows() -> list[dict[str, Any]]:
    return [
        {
            "rule_id": "NF3519_0_parent_domain",
            "sort_or_rule": "ParentDomain",
            "allowed": "Phi_parent fields, universal constants, gauge bundles, fixed boundary/reference data before variation",
            "forbidden": "source labels chosen after solving, fitted readout weights, post-variation source masks",
            "derivation_role": "sets the action domain before empirical readout; prevents source fit knobs from becoming field variables",
            "effect_on_q_source": "prevents epsilon_q_source from being introduced as a late source scalar",
            "current_status": "CANDIDATE_NORMAL_FORM_NOT_PARENT_SIGNED",
            "source_path": str(SOURCES["parent_object_3380"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "rule_id": "NF3519_1_quotient_visible_stack",
            "sort_or_rule": "Qvis",
            "allowed": "q(Phi), e_obs(qPhi), g_obs, nabla_obs, volume density, ordinary gauge connection A_obs",
            "forbidden": "second source metric, source-only disformal frame, hidden coframe coupled only to active mass",
            "derivation_role": "all ordinary matter and Hilbert source variation see one public geometry stack",
            "effect_on_q_source": "if Lie_vq Qvis=0, chain rule kills direct v_q matter variation through the visible stack",
            "current_status": "STRUCTURAL_RULE_DEFINED_NEEDS_PARENT_QMAP_SIGNING",
            "source_path": str(SOURCES["qvis_2910"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "rule_id": "NF3519_2_matter_functor",
            "sort_or_rule": "MatterAction",
            "allowed": "S_matter=sum_A S_A[psi_A,Qvis,theta_A,A_obs] with theta_A representation/superselection data",
            "forbidden": "S_A[psi_A,Qvis,q_private], q_private T_A, w_A(q_private) S_A, species/action source prefactors",
            "derivation_role": "turns no-direct-q-source from taste into a typed-domain statement",
            "effect_on_q_source": "C_qT=0 and j_matter=0 if Lie_vq Qvis=0 and Lie_vq theta_A=0",
            "current_status": "EXACT_CONDITIONAL_NORMAL_FORM",
            "source_path": str(SOURCES["q_slot_2299"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "rule_id": "NF3519_3_curvature_language",
            "sort_or_rule": "CurvatureOperators",
            "allowed": "metric/epsilon contractions of Riemann, Ricci, scalar curvature and declared higher-curvature invariants",
            "forbidden": "q_private P_W^{abcd} C_abcd, hidden Weyl spurion, post-variation Weyl readout kernel",
            "derivation_role": "separates true Ricci/scalar operators from linear Weyl spurion operators",
            "effect_on_q_source": "linear B_qWeyl=0 under metric/epsilon-only grammar; Weyl^2 remains a separate higher-curvature residual",
            "current_status": "EXACT_CONDITIONAL_INDEX_NORMAL_FORM",
            "source_path": str(SOURCES["object_index_2304"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "rule_id": "NF3519_4_universal_scale",
            "sort_or_rule": "UniversalScale",
            "allowed": "one common kappa/G_ref/hbar/action-density normalization or common calibrated mode",
            "forbidden": "species/readout dependent kappa_A, hbar_A, kappa_source, active-source-only current rescaling",
            "derivation_role": "blocks the classical-EOM rescaling loophole where source weights change T while leaving matter EOM intact",
            "effect_on_q_source": "j_weight and action-scale source terms vanish only if common-mode owner is signed",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "source_path": str(SOURCES["species_weight_2677"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "rule_id": "NF3519_5_readout_firewall",
            "sort_or_rule": "ReadoutAfterVariation",
            "allowed": "maps from solved fields to clocks, PPN, R10, orbital, SPARC, cosmology and EM observables",
            "forbidden": "readout object reentering S_matter or source normalization before Hilbert/coframe variation",
            "derivation_role": "keeps prediction extraction downstream of the source definition",
            "effect_on_q_source": "blocks projector/readout tails only after variation-domain ordering is signed",
            "current_status": "FIREWALL_DEFINED_NOT_DERIVED",
            "source_path": str(SOURCES["parent_object_3380"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "rule_id": "NF3519_6_boundary_reference",
            "sort_or_rule": "BoundaryReference",
            "allowed": "source-blind fixed reference subtraction and zero-flux/proper boundary class",
            "forbidden": "source-dependent H_ref, B_ref, corner term or compact boundary class that shifts active mass",
            "derivation_role": "prevents boundary bookkeeping from becoming a source coupling",
            "effect_on_q_source": "j_boundary=0 only when fixed/proper boundary rule is parent signed",
            "current_status": "CANDIDATE_USES_BOUNDARY_CONTRACT",
            "source_path": str(SOURCES["parent_object_3380"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM3519_0_q_private_gauge_invariance",
            "claim": "A direct q_private source vertex is incompatible with v_q gauge invariance unless its coefficient vanishes or q_private is promoted to a physical source scalar.",
            "proof_sketch": "For a term Integral mu C_qT q_private T with Lie_vq T=0 and Lie_vq mu=0, invariance gives delta_vq S = Integral mu C_qT (Lie_vq q_private) T. For arbitrary matter stress T and nonzero vertical motion of q_private, C_qT must be zero. If Lie_vq q_private=0 instead, q_private is not vertical and must be treated as a physical scalar with a bound.",
            "premises_required": "v_q is a gauge/vertical generator; Qvis and matter stress are v_q-basic; arbitrary source stress allowed; no compensating source-only counterterm",
            "current_evidence": "3518 has v_q candidate and 3380/2910 define candidate Qvis, but parent generator and no-counterterm clause are not signed together.",
            "result_if_premises_signed": "C_qT=0;j_matter=0",
            "current_status": "EXACT_CONDITIONAL_THEOREM_NOT_FIRED",
            "fires_now": "False",
            "source_path": str(SOURCES["q_slot_2299"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3519_1_chain_rule_matter_descent",
            "claim": "If S_matter factors through Qvis and DQvis[v_q]=0, then delta S_matter/delta v_q=0.",
            "proof_sketch": "Write S_matter=Sbar[Qvis(Phi),psi,theta]. Then D_vq S_matter = DSbar[DQvis[v_q]] + partial_theta Sbar Lie_vq theta. The derivative vanishes when DQvis[v_q]=0 and theta is representation/superselection data with Lie_vq theta=0.",
            "premises_required": "typed factorization through Qvis; DQvis[v_q]=0; no theta/marker/readout return",
            "current_evidence": "3516/3517 provide the chain-rule hook; 2434/2910 leave Qvis map, no-marker and readout closure unsigned.",
            "result_if_premises_signed": "j_matter=0;source-coordinate matter pullback closed",
            "current_status": "EXACT_CONDITIONAL_THEOREM_NOT_FIRED",
            "fires_now": "False",
            "source_path": str(SOURCES["qvis_2910"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3519_2_linear_weyl_no_spurion",
            "claim": "A scalar/density q cannot form a nonzero scalar density linear in one Weyl tensor without a Weyl-type spurion or readout projector.",
            "proof_sketch": "Metric contractions trace a Weyl pair and vanish; epsilon contraction of one Weyl vanishes by pair symmetries and the first Bianchi identity. A nonzero linear term has the form q P^{abcd} C_abcd, so P^{abcd} is exactly the forbidden extra object.",
            "premises_required": "q scalar/quotient/pure density; metric/epsilon-only local grammar; no P_W spurion; no post-variation readout Weyl kernel; boundary does not regenerate the term",
            "current_evidence": "2304/2365 prove the index lemma, but 2302 says q representation, no-spurion and readout/boundary closure are not parent signed.",
            "result_if_premises_signed": "B_qWeyl(linear)=0",
            "current_status": "EXACT_CONDITIONAL_THEOREM_NOT_FIRED",
            "fires_now": "False",
            "source_path": str(SOURCES["object_index_2304"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3519_3_source_prefactor_ban",
            "claim": "Relative source-only action weights are ill-typed if the parent ordinary-matter category has one action-density line and no Hom(source/readout label, active-source coefficient).",
            "proof_sketch": "A term w_A(q_private) S_A may preserve classical matter equations but changes Hilbert/coframe source by w_A T_A. Therefore it is not killed by EOM equivalence; it is killed only by typed-domain exclusion or a common-mode owner.",
            "premises_required": "single action-density/hbar/measure owner; no source-label coefficient target; no radiative/readout return",
            "current_evidence": "2650 and 2677 establish the exact conditional theorem and the EOM-rescaling rejection, but the parent measure/common-mode owner is not signed.",
            "result_if_premises_signed": "j_weight=0;relative source-normalization branch removed",
            "current_status": "EXACT_CONDITIONAL_THEOREM_NOT_FIRED",
            "fires_now": "False",
            "source_path": str(SOURCES["source_pref_2650"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3519_4_normal_form_total_gate",
            "claim": "The v_q source vector is zero if the normal-form rules NF3519_0 through NF3519_6 are all parent signed and DQvis[v_q]=0.",
            "proof_sketch": "Matter, source-weight, curvature, readout, tail and boundary channels each become either ill-typed, q-basic, or fixed/proper before variation. The no-cancellation policy is then satisfied termwise, not by tuning signs.",
            "premises_required": "all normal-form rules signed in one parent branch; DQvis[v_q]=0; no hidden closure extension after variation",
            "current_evidence": "3380 is a candidate grammar and 3518 lists live channels; no current source proves the full rule stack as a derived parent theorem.",
            "result_if_premises_signed": "Z_vq_source_silent=True;Z_Dq_vq_zero can proceed to first-class/local charge gate",
            "current_status": "CANDIDATE_NORMAL_FORM_TOTAL_THEOREM_NOT_FIRED",
            "fires_now": "False",
            "source_path": str(SOURCES["parent_object_3380"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def operator_rows() -> list[dict[str, Any]]:
    return [
        {
            "operator_id": "OP3519_0_CqT",
            "operator": "C_qT q_private T",
            "typed_status_under_normal_form": "FORBIDDEN_IF_QPRIVATE_VERTICAL",
            "reason": "direct q_private matter/source argument is outside MatterAction; gauge invariance forces C_qT=0 for arbitrary T",
            "if_not_signed": "retain C_qT bound row",
            "residual_bound": "E_T <= C_T |C_qT| ||P_T T||",
            "current_claim": "False",
            "source_path": str(SOURCES["q_slot_2299"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "operator_id": "OP3519_1_prefactor",
            "operator": "w_A(q_private) S_A",
            "typed_status_under_normal_form": "FORBIDDEN_IF_NO_SOURCE_COEFFICIENT_SORT",
            "reason": "classical EOM equivalence is not enough; source variation changes by w_A T_A",
            "if_not_signed": "retain j_weight/source-normalization bound row",
            "residual_bound": "E_weight <= sup_A |partial_q ln w_A| ||T_A||",
            "current_claim": "False",
            "source_path": str(SOURCES["species_weight_2677"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "operator_id": "OP3519_2_BqWeyl",
            "operator": "B_qWeyl q_private P_W^{abcd} C_abcd",
            "typed_status_under_normal_form": "FORBIDDEN_IF_NO_WEYL_SPURION",
            "reason": "metric/epsilon-only grammar kills one-Weyl scalar; nonzero term needs forbidden P_W",
            "if_not_signed": "retain B_qWeyl bound row",
            "residual_bound": "E_W <= C_W |B_qWeyl| ||P_W W||",
            "current_claim": "False",
            "source_path": str(SOURCES["linear_bqweyl_2365"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "operator_id": "OP3519_3_BqR",
            "operator": "B_qR q_private R or q_private R_ab u^a u^b",
            "typed_status_under_normal_form": "SEPARATE_RICCI_SCALAR_RESIDUAL",
            "reason": "Ricci/scalar terms are not killed by Weyl index algebra; they require second-order/EH/minimality or finite scalar-mode bounds",
            "if_not_signed": "retain R2/fR/scalar-mode bound row",
            "residual_bound": "E_R <= C_R |B_qR| ||P_R R||",
            "current_claim": "False",
            "source_path": str(SOURCES["object_index_2304"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "operator_id": "OP3519_4_readout_tail",
            "operator": "post-variation Pi_readout(q_private) or projector/domain tail",
            "typed_status_under_normal_form": "FORBIDDEN_ONLY_BY_READOUT_FIREWALL",
            "reason": "readout must not reenter S_matter or source normalization before variation",
            "if_not_signed": "retain E_readout/E_tail bound rows",
            "residual_bound": "E_readout <= ||D_q Pi|| ||source profile||",
            "current_claim": "False",
            "source_path": str(SOURCES["qvis_2910"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "operator_id": "OP3519_5_boundary",
            "operator": "q_private boundary/reference/corner source term",
            "typed_status_under_normal_form": "FORBIDDEN_ONLY_BY_FIXED_PROPER_BOUNDARY",
            "reason": "source-dependent reference subtraction can mimic a source coupling unless boundary class is fixed before variation",
            "if_not_signed": "retain E_boundary bound row",
            "residual_bound": "E_boundary <= ||delta_q B_boundary|| + ||delta_q H_ref||",
            "current_claim": "False",
            "source_path": str(SOURCES["parent_object_3380"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3519_0_normal_form_written",
            "quantity": "parent_q_object_language_normal_form",
            "value": "candidate_written",
            "meaning": "3519 now gives the actual syntax needed to forbid direct q source couplings",
            "claim_effect": "private construction progress, not a public theorem",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3519_1_CqT_zero",
            "quantity": "Z_CqT",
            "value": "False",
            "meaning": "C_qT is zero only after the q-private vertical/gauge and MatterAction factorization premises are parent signed",
            "claim_effect": "C_qT remains bounded, not zero-claimed",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3519_2_BqWeyl_zero",
            "quantity": "Z_BqWeyl",
            "value": "False",
            "meaning": "linear Weyl index theorem is exact but no-spurion/readout/boundary premises are not parent signed",
            "claim_effect": "B_qWeyl remains bounded, not zero-claimed",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3519_3_source_silence",
            "quantity": "Z_vq_source_silent",
            "value": "False",
            "meaning": "normal-form total gate is written but not signed as a parent-derived theorem",
            "claim_effect": "v_q source silence remains open",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3519_4_best_route",
            "quantity": "next_best_route",
            "value": "derive_normal_form_from_quotient_action_principle",
            "meaning": "do not spend the next step digitizing bounds until the clean quotient-action derivation has been attempted",
            "claim_effect": "continue derivation-first rather than closure-first",
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "SCB3519_0_total_q_source",
            "source_channel": "J_q_total_if_normal_form_unsigned",
            "bound_formula": "||J_q|| <= |C_qT| ||P_T T|| + |B_qWeyl| ||P_W W|| + |B_qR| ||P_R R|| + E_weight + E_readout + E_boundary + E_tail",
            "required_numeric_inputs": "C_qT,B_qWeyl,B_qR,source stress profile,Weyl/Ricci profiles,weight/readout/boundary/tail norms",
            "prediction_value": "MISSING_TOTAL_JQ_BOUND",
            "bound_value": "MISSING_LOCAL_ARENA_TOLERANCE",
            "status": "NONCLAIM_IF_GRAMMAR_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "SCB3519_1_CqT",
            "source_channel": "direct_matter_source",
            "bound_formula": "E_T <= |C_qT| ||P_T T||",
            "required_numeric_inputs": "C_qT coefficient; matter stress projection; source/test support normalization",
            "prediction_value": "MISSING_CQT_COEFFICIENT",
            "bound_value": "MISSING_STRESS_PROJECTION_BOUND",
            "status": "NONCLAIM_IF_GRAMMAR_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "SCB3519_2_BqWeyl",
            "source_channel": "linear_weyl_tail",
            "bound_formula": "E_W <= |B_qWeyl| ||P_W W||",
            "required_numeric_inputs": "B_qWeyl coefficient; no-spurion verdict or Weyl projection/profile",
            "prediction_value": "MISSING_BQWEYL_COEFFICIENT",
            "bound_value": "MISSING_WEYL_PROJECTION_BOUND",
            "status": "NONCLAIM_IF_GRAMMAR_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "SCB3519_3_source_prefactor",
            "source_channel": "source_weight_action_scale",
            "bound_formula": "E_weight <= sup_A |partial_q ln w_A| ||T_A||",
            "required_numeric_inputs": "source weight derivative or common-mode theorem; material/source basis",
            "prediction_value": "MISSING_SOURCE_WEIGHT_DERIVATIVE",
            "bound_value": "MISSING_WEP_CLOCK_PPN_TOLERANCE",
            "status": "NONCLAIM_IF_GRAMMAR_UNSIGNED",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3519_0_not_just_missing",
            "decision": "replace the vague object-language gap with a concrete parent q normal form",
            "rationale": "The grammar now states exactly which q appearances are allowed and which operators become illegal.",
            "effect": "C_qT and B_qWeyl have real zero theorems if the normal form is derived or adopted.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3519_1_do_not_overclaim",
            "decision": "do not claim C_qT=0 or B_qWeyl=0 yet",
            "rationale": "The normal form is a candidate contract; current sources do not prove it from the parent action.",
            "effect": "finite source-channel bounds stay alive as fallback rows.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3519_2_derivation_first",
            "decision": "try to derive the normal form from quotient action principle next",
            "rationale": "If all physical actions are functions on the quotient of configurations, direct q_private source slots become gauge-variant and illegal.",
            "effect": "3520 should attempt the derivation before moving to numerical/source-bound acquisition.",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3520-Y5-R2FR-quotient-action-principle-derives-q-normal-form-or-finite-source-bounds.md",
            "next_script": "scripts/Y5_R2FR_3520_quotient_action_principle_derives_q_normal_form_or_finite_source_bounds.py",
            "objective": "Attempt to derive the 3519 q normal form from a quotient action principle: S_parent must be a functional on physical equivalence classes before matter/source variation.",
            "success_gate": "Either prove direct q_private source operators are gauge-variant/ill-typed and therefore absent, or keep C_qT/B_qWeyl/source-prefactor rows as finite nonclaim bounds.",
            "why_next": "3519 produced the grammar; 3520 must decide whether it is derivable field theory or merely a closure/adoption contract.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    normal_form: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    operators: list[dict[str, Any]],
    status: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append(
        {
            "check_id": "VAL3519_0_sources_exist",
            "passed": bool_text(all(row["exists"] == "True" for row in sources)),
            "detail": "all cited local source paths exist",
            "valid_for_claim": "False",
        }
    )
    normal_text = " ".join(row["allowed"] + " " + row["forbidden"] for row in normal_form)
    checks.append(
        {
            "check_id": "VAL3519_1_normal_form_has_allow_forbid",
            "passed": bool_text(len(normal_form) >= 6 and "q_private T_A" in normal_text and "P_W" in normal_text),
            "detail": "normal form includes explicit allowed and forbidden q appearances",
            "valid_for_claim": "False",
        }
    )
    theorem_results = " ".join(row["result_if_premises_signed"] for row in theorem)
    checks.append(
        {
            "check_id": "VAL3519_2_zero_theorems_present",
            "passed": bool_text("C_qT=0" in theorem_results and "B_qWeyl(linear)=0" in theorem_results),
            "detail": "conditional zero theorems for C_qT and B_qWeyl are present",
            "valid_for_claim": "False",
        }
    )
    operator_names = {row["operator_id"] for row in operators}
    checks.append(
        {
            "check_id": "VAL3519_3_live_operator_inventory",
            "passed": bool_text({"OP3519_0_CqT", "OP3519_2_BqWeyl", "OP3519_4_readout_tail"}.issubset(operator_names)),
            "detail": "; ".join(sorted(operator_names)),
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3519_4_no_claim_flags_true",
            "passed": bool_text(
                all(row["fires_now"] == "False" and row["valid_for_claim"] == "False" for row in theorem)
                and all(row["current_claim"] == "False" and row["valid_for_claim"] == "False" for row in operators)
                and all(row["valid_for_claim"] == "False" for row in normal_form + status + bounds)
            ),
            "detail": "normal-form route is explicit but not claimed as signed parent theorem",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3519_5_bounds_blocked_if_unsigned",
            "passed": bool_text(all(row["prediction_value"].startswith("MISSING_") and row["status"] == "NONCLAIM_IF_GRAMMAR_UNSIGNED" for row in bounds)),
            "detail": "finite source-channel bounds stay nonclaim until numeric inputs are sourced",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3519_6_next_target_derivation_first",
            "passed": bool_text(any("quotient-action-principle" in row["next_doc"] or "quotient_action_principle" in row["next_script"] for row in next_rows)),
            "detail": "3520 derivation-first target selected",
            "valid_for_claim": "False",
        }
    )
    csvs_parse = True
    parse_details: list[str] = []
    for name, path in outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        if name == "validation" and not path.exists():
            parse_details.append("validation:deferred_until_written")
            continue
        try:
            read_csv_rows(path)
            parse_details.append(name)
        except Exception as exc:
            csvs_parse = False
            parse_details.append(f"{name}:{exc}")
    checks.append(
        {
            "check_id": "VAL3519_7_csvs_parse",
            "passed": bool_text(csvs_parse),
            "detail": "; ".join(parse_details),
            "valid_for_claim": "False",
        }
    )
    output_paths_in_root = all(str(path).startswith(str(ROOT)) for path in outputs.values()) and str(DOC).startswith(str(ROOT))
    checks.append(
        {
            "check_id": "VAL3519_8_outputs_stay_in_post_checkpoint_work",
            "passed": bool_text(output_paths_in_root),
            "detail": f"root={ROOT}",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3519_9_formalization_workbench_not_targeted",
            "passed": "True",
            "detail": str(FORMALIZATION),
            "valid_for_claim": "False",
        }
    )
    passed = all(row["passed"] == "True" for row in checks)
    checks.append(
        {
            "check_id": "VAL3519_SUMMARY",
            "passed": bool_text(passed),
            "detail": "PASS" if passed else "FAIL",
            "valid_for_claim": "False",
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    normal_form: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    operators: list[dict[str, Any]],
    status: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3519 - v_q Parent Object-Language Normal Form Or Source-Channel Bound

## Summary
- **Actual forward move:** the q-coupling problem is converted from "missing parent object language" into a concrete parent normal form.
- **Clean route:** if `q_private` is vertical/gauge and all physical matter/source functionals factor through `Qvis`, direct `q_private T` terms are gauge-variant and force `C_qT=0`.
- **Weyl route:** the linear `B_qWeyl` term is killed by the exact index theorem when the grammar is metric/epsilon-only and has no Weyl spurion or readout projector.
- **Still not claimed:** the normal form is candidate/conditional, not yet derived from the parent action; `C_qT`, `B_qWeyl`, readout, boundary and source-prefactor rows remain finite nonclaim bounds.
- **Next move:** derive this normal form from a quotient action principle, or demote it to an explicit closure/adoption contract with finite bounds.

## Core Derivation
For a direct source term

`S_direct = Integral mu C_qT q_private T`,

with `Lie_vq T=0` and `Lie_vq mu=0`, vertical/gauge invariance gives

`Lie_vq S_direct = Integral mu C_qT (Lie_vq q_private) T`.

If `v_q` is a genuine vertical generator, `Lie_vq q_private` is not identically zero. Since the source stress `T` is arbitrary, the only gauge-invariant normal-form answer is `C_qT=0`, unless `q_private` is promoted to a physical source scalar. In that promoted case the local branch cannot use the vertical theorem and must use finite bounds.

For a linear Weyl term, metric contractions trace the Weyl tensor and vanish, while the one-epsilon contraction vanishes by Weyl symmetries/Bianchi identity. A nonzero linear term needs a separate `P_W^abcd`, which is precisely the spurion/readout object the normal form forbids.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Parent q Normal Form
{markdown_table(normal_form, ["rule_id", "sort_or_rule", "allowed", "forbidden", "derivation_role", "effect_on_q_source", "current_status", "valid_for_claim"])}

## Conditional Theorems
{markdown_table(theorem, ["theorem_id", "claim", "proof_sketch", "premises_required", "current_evidence", "result_if_premises_signed", "current_status", "fires_now", "valid_for_claim"])}

## Operator Inventory
{markdown_table(operators, ["operator_id", "operator", "typed_status_under_normal_form", "reason", "if_not_signed", "residual_bound", "current_claim", "valid_for_claim"])}

## Canonical Status
{markdown_table(status, ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"])}

## Finite Bounds If Unsigned
{markdown_table(bounds, ["bound_id", "source_channel", "bound_formula", "required_numeric_inputs", "prediction_value", "bound_value", "status", "valid_for_claim"])}

## Decisions
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}

Generated: {now_utc()}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    normal_form = normal_form_rows()
    theorem = theorem_rows()
    operators = operator_rows()
    status = status_rows()
    bounds = bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3519_SOURCE_REGISTER.csv",
        "normal_form": OUT / "P8_Y5_R2FR_3519_PARENT_Q_OBJECT_LANGUAGE_NORMAL_FORM.csv",
        "canonical_normal_form": CANONICAL_NORMAL_FORM,
        "theorem": OUT / "P8_Y5_R2FR_3519_Q_GRAMMAR_ZERO_THEOREMS.csv",
        "operators": OUT / "P8_Y5_R2FR_3519_FORBIDDEN_OPERATOR_INVENTORY.csv",
        "status": OUT / "P8_Y5_R2FR_3519_Q_OBJECT_LANGUAGE_STATUS.csv",
        "bounds": OUT / "P8_Y5_R2FR_3519_SOURCE_CHANNEL_BOUNDS_IF_UNSIGNED.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3519_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3519_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3519_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    normal_fields = ["rule_id", "sort_or_rule", "allowed", "forbidden", "derivation_role", "effect_on_q_source", "current_status", "source_path", "valid_for_claim"]
    write_csv(outputs["normal_form"], normal_form, normal_fields)
    write_csv(outputs["canonical_normal_form"], normal_form, normal_fields)
    write_csv(outputs["theorem"], theorem, ["theorem_id", "claim", "proof_sketch", "premises_required", "current_evidence", "result_if_premises_signed", "current_status", "fires_now", "source_path", "valid_for_claim"])
    write_csv(outputs["operators"], operators, ["operator_id", "operator", "typed_status_under_normal_form", "reason", "if_not_signed", "residual_bound", "current_claim", "source_path", "valid_for_claim"])
    write_csv(outputs["status"], status, ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"])
    write_csv(outputs["bounds"], bounds, ["bound_id", "source_channel", "bound_formula", "required_numeric_inputs", "prediction_value", "bound_value", "status", "valid_for_claim"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])

    validation_rows = validate(outputs, sources, normal_form, theorem, operators, status, bounds, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, normal_form, theorem, operators, status, bounds, decisions, next_rows, validation_rows)

    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()

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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1764"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1764_0_1763_handoff",
        "source_key": "1763_species_route_selected",
        "source_path": ROOT / "1763-Y5-R2FR-invariant-generator-elimination-priority-or-deltaw-source-acquisition.md",
        "needles": ["NEXT1763_0_primary", "SPECIES_LABEL_FORGETTING_PARENT_PROOF_IS_NEXT"],
    },
    {
        "source_id": "SRC1764_1_1763_species_attempt",
        "source_key": "1763_species_zero_attempt",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1763_SPECIES_LABEL_ZERO_ATTEMPT.csv",
        "needles": ["SLZ1763_1_conditional_uniqueness", "DELTA_W_SPECIES_RETAINED"],
    },
    {
        "source_id": "SRC1764_2_953_doc",
        "source_key": "953_no_species_label_doc",
        "source_path": ROOT / "953-Y5-R10-no-species-label-source-functor-theorem-or-filled-coefficient-intake-review.md",
        "needles": ["The good news", "The bad news"],
    },
    {
        "source_id": "SRC1764_3_953_theorem",
        "source_key": "953_source_functor_theorem",
        "source_path": RESIDUALS / "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv",
        "needles": ["NSF953_1_domain_fork", "NSF953_5_verdict"],
    },
    {
        "source_id": "SRC1764_4_953_contract",
        "source_key": "953_parent_category_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_953_PARENT_CATEGORY_CONTRACT.csv",
        "needles": ["PMC953_1_label_forgetting_quotient", "PMC953_5_contract_verdict"],
    },
    {
        "source_id": "SRC1764_5_953_countermodel",
        "source_key": "953_labelled_source_countermodel",
        "source_path": RESIDUALS / "P8_Y5_R10_953_COUNTERMODEL_LEDGER.csv",
        "needles": ["CM953_0_labelled_additive_functor", "CM953_4_verdict"],
    },
    {
        "source_id": "SRC1764_6_954_doc",
        "source_key": "954_parent_action_doc",
        "source_path": ROOT / "954-Y5-R10-parent-matter-category-no-species-label-clause-or-source-functor-countermodel-bound.md",
        "needles": ["single total matter action", "no independent species source prefactors"],
    },
    {
        "source_id": "SRC1764_7_954_action_clause",
        "source_key": "954_parent_action_clause",
        "source_path": RESIDUALS / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
        "needles": ["PAC954_1_no_source_prefactors", "PAC954_2_total_Hilbert_derivative"],
    },
    {
        "source_id": "SRC1764_8_954_label_attempt",
        "source_key": "954_label_forgetting_attempt",
        "source_path": RESIDUALS / "P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv",
        "needles": ["PLF954_2_prefactor_obstruction", "PLF954_5_verdict"],
    },
    {
        "source_id": "SRC1764_9_955_minimal_matter",
        "source_key": "955_minimal_matter_lemma",
        "source_path": RESIDUALS / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
        "needles": ["MMA955_3_relative_prefactor", "MMA955_6_verdict"],
    },
    {
        "source_id": "SRC1764_10_977_constant_certificate",
        "source_key": "977_constant_source_certificate",
        "source_path": RESIDUALS / "P8_Y5_R10_977_CONSTANT_SOURCE_CERTIFICATE_ATTEMPT.csv",
        "needles": ["CSC977_1_theta_representation_data", "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED"],
    },
    {
        "source_id": "SRC1764_11_1488_residual_lock",
        "source_key": "1488_wA_deltaW_lock",
        "source_path": RESIDUALS / "P8_Y5_R10_1488_WA_DELTAW_RESIDUAL_LOCK.csv",
        "needles": ["WA1488_2_species_label_slot", "RETAINED_RESIDUAL_SYMBOLIC"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1764_SOURCE_REGISTER.csv",
    "label_forgetting": RESIDUALS / "P8_Y5_PARENT_QLOC_1764_LABEL_FORGETTING_PROOF_ATTEMPT.csv",
    "source_domain": RESIDUALS / "P8_Y5_PARENT_QLOC_1764_SOURCE_DOMAIN_FORK_AUDIT.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1764_COUNTERMODEL_LEDGER.csv",
    "deltaw_species": RESIDUALS / "P8_Y5_PARENT_QLOC_1764_DELTAW_SPECIES_BOUND_INTERFACE.csv",
    "source_zero_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1764_SOURCE_ZERO_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1764_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1764_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1764_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1764_VALIDATION.csv",
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
                "role": "species-label forgetting source functor parent proof or delta_w_species bound interface",
                "valid_for_claim": False,
            }
        )
    return rows


def label_forgetting_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LF1764_0_target",
            "claim_piece": "parent source functor forgets species labels before coupling selection",
            "mathematical_form": "q_src({(T_A,A)})=T_total=sum_A T_A",
            "proof_status": "TARGET_EXACT",
            "proof_result": "WOULD_REMOVE_DELTA_W_SPECIES_DOMAIN_SLOT",
            "parent_signed": False,
            "gap": "the source-domain quotient is identified but not yet forced by the parent action",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LF1764_1_conditional_theorem",
            "claim_piece": "label-forgotten source functor has one coupling",
            "mathematical_form": "S_matter=sum_A S_A; T_total=delta S_matter/delta e_obs; F_src(T_total)=kappa_univ T_total",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_result": "if no w_A slot and no hidden source spurion exists, relative kappa_A/kappa_B cannot be written",
            "parent_signed": False,
            "gap": "no-source-prefactor and no-spurion clauses remain unsigned parent premises",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LF1764_2_variation_order",
            "claim_piece": "variation-before-decomposition mechanism",
            "mathematical_form": "delta(S_1+...+S_N)/delta e_obs = sum_A delta S_A/delta e_obs, with the source object T_total formed before labels are exposed",
            "proof_status": "DERIVED_WITHIN_CONTRACT",
            "proof_result": "bookkeeping labels disappear if the active source owner is the total Hilbert/coframe derivative",
            "parent_signed": False,
            "gap": "the parent action must declare the total Hilbert derivative as the only ordinary active-source owner",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LF1764_3_needed_signatures",
            "claim_piece": "minimal parent signature for species zero",
            "mathematical_form": "PAC954_0 + PAC954_1 + PAC954_2 + CSC977_1..4 + no hidden post-variation source spurion",
            "proof_status": "CONTRACT_LIST_SHARP",
            "proof_result": "these clauses would make delta_w_species=0 a structural theorem rather than a fitted assumption",
            "parent_signed": False,
            "gap": "PAC954_1 and the source-domain quotient are the highest-pressure unsigned clauses",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LF1764_4_failed_current_proof",
            "claim_piece": "current MTS parent action proves the source quotient",
            "mathematical_form": "parent action entails not exists w_A and not exists label-carrying F_src argument",
            "proof_status": "FAIL_CURRENT_PARENT_SIGNATURE",
            "proof_result": "the proof cannot be promoted because labelled additive source maps and weighted matter actions remain legal countermodels",
            "parent_signed": False,
            "gap": "existing files provide a contract and countermodel ledger, not a parent-level exclusion theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LF1764_5_current_verdict",
            "claim_piece": "delta_w_species=0 for current MTS local branch",
            "mathematical_form": "delta_w_species=0",
            "proof_status": "THEOREM_CONTRACT_READY_PARENT_UNSIGNED",
            "proof_result": "DELTA_W_SPECIES_RETAINED",
            "parent_signed": False,
            "gap": "no-source-prefactor clause and source-label quotient still need parent proof or sourced finite bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def source_domain_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SDF1764_0_unlabelled_domain",
            "domain_choice": "label-forgotten total Hilbert current",
            "mathematical_form": "Obj(Source)=T_total, not {(T_A,A)}",
            "consequence": "F_src has no species argument and can only carry one calibrated common scalar",
            "status": "CLEAN_ZERO_ROUTE_IF_PARENT_SIGNED",
            "remaining_gap": "parent category/source owner not signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SDF1764_1_total_hilbert_owner",
            "domain_choice": "source extracted by total variation of one matter functional",
            "mathematical_form": "T_total := delta S_matter[Psi,e_obs,theta]/delta e_obs",
            "consequence": "species decomposition becomes bookkeeping after source extraction",
            "status": "CONDITIONAL_MECHANISM_VALID",
            "remaining_gap": "must prove total Hilbert derivative is the only ordinary active-source owner",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SDF1764_2_labelled_domain",
            "domain_choice": "labelled species current family",
            "mathematical_form": "Obj(Source)={(T_A,A)} and F_src({(T_A,A)})=sum_A kappa_A T_A",
            "consequence": "relative species couplings remain covariant, additive and Ward-compatible",
            "status": "COUNTERDOMAIN_OPEN",
            "remaining_gap": "must exclude labels before source functor formation",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SDF1764_3_weighted_action_domain",
            "domain_choice": "weighted matter action before variation",
            "mathematical_form": "S_matter=sum_A w_A S_A gives T_source=sum_A w_A T_A",
            "consequence": "the source quotient is not enough unless w_A slots are absent",
            "status": "PREFATOR_OBSTRUCTION_OPEN",
            "remaining_gap": "PAC954_1 no-source-prefactors is unsigned",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SDF1764_4_minimal_normalization_clause",
            "domain_choice": "nongravitational normalization fixes matter constants and forbids source-only weights",
            "mathematical_form": "theta_A fixed by Rep_A and experiments; w_A source-only slot is not an allowed parent coordinate",
            "consequence": "would demote relative weights to forbidden double counting rather than physical couplings",
            "status": "BEST_NEXT_PARENT_CLAUSE",
            "remaining_gap": "needs explicit parent object-language/action signature",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SDF1764_5_fork_verdict",
            "domain_choice": "source-domain fork",
            "mathematical_form": "unlabelled source domain closes delta_w_species; labelled or weighted domain keeps it alive",
            "consequence": "the next derivation must sign no-source-prefactor/total-Hilbert-source ownership",
            "status": "FORK_NOT_RESOLVED",
            "remaining_gap": "no current local-GR/WEP/R10 claim",
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1764_0_labelled_additive_source_functor",
            "countermodel": "species labels remain source-functor arguments",
            "mathematical_form": "F_src({(T_A,A)})=sum_A kappa_A T_A",
            "survives_current_constraints": True,
            "why_survives": "covariance, additivity and Ward conservation do not force kappa_A=kappa_B",
            "what_kills_it": "parent proof that q_src forgets A before F_src is formed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1764_1_weighted_action_before_variation",
            "countermodel": "relative source-only weights multiply species actions",
            "mathematical_form": "S_matter=sum_A w_A S_A",
            "survives_current_constraints": True,
            "why_survives": "constant w_A can preserve diffeomorphism covariance and species Ward identities",
            "what_kills_it": "no-source-prefactor parent clause plus nongravitational normalization owner",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1764_2_hidden_spurion_return",
            "countermodel": "material marker returns after variation",
            "mathematical_form": "T_active=T_total + sum_A sigma_A P_A(T_A)",
            "survives_current_constraints": True,
            "why_survives": "a hidden source projector can reintroduce material labels unless object language forbids it",
            "what_kills_it": "no hidden source-spurion/post-readout-source clause",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1764_3_nonHilbert_current_split",
            "countermodel": "non-Hilbert spin/torsion/boundary current carries species labels",
            "mathematical_form": "T_active=T_Hilbert + J_nonHilbert[A]",
            "survives_current_constraints": True,
            "why_survives": "standard Hilbert-current uniqueness does not silence extra parent currents by itself",
            "what_kills_it": "explicit absence/silence theorem for non-Hilbert ordinary source currents",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1764_4_representation_constant_leakage",
            "countermodel": "matter constants depend on MTS invariant or material marker",
            "mathematical_form": "theta_A=theta_A(X,I_Q,m,h) or kappa_A=kappa(theta_A)",
            "survives_current_constraints": True,
            "why_survives": "the constant-source certificate is relative and parent unsigned",
            "what_kills_it": "fixed representation-data theorem for theta_A and one global kappa",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1764_5_verdict",
            "countermodel": "species source-prefactor leakage",
            "mathematical_form": "not(parent_forgets_A and no w_A and no hidden source spurion) => delta_w_species retained",
            "survives_current_constraints": True,
            "why_survives": "current parent action has contract gaps exactly where the countermodels enter",
            "what_kills_it": "1765 no-source-prefactor/total-Hilbert-owner proof or finite sourced bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def deltaw_species_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWS1764_0_delta_w_species",
            "quantity": "delta_w_species",
            "meaning": "species-label leakage into active ordinary source prefactor",
            "mathematical_form": "T_active=sum_A (1+delta_w_A) T_A; delta_w_species is the label-dependent component",
            "units": "dimensionless",
            "required_input": "parent proof of no labelled source domain or numeric bound on delta_w_A-delta_w_B",
            "status": "MISSING_PARENT_NO_PREFACTOR_OR_NUMERIC_BOUND",
            "source_path": str(RESIDUALS / "P8_Y5_R10_1488_WA_DELTAW_RESIDUAL_LOCK.csv"),
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWS1764_1_component_basis",
            "quantity": "species/component basis",
            "meaning": "which ordinary matter components carry independent source-weight residuals",
            "mathematical_form": "A in {electron, proton, neutron, nuclear binding, EM binding, ...} or a parent-derived smaller basis",
            "units": "labels",
            "required_input": "basis owner and composition projection",
            "status": "MISSING_COMPONENT_BASIS",
            "source_path": "TBD",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWS1764_2_test_body_projection",
            "quantity": "composition projection",
            "meaning": "map from delta_w_species to measured differential acceleration/source charge",
            "mathematical_form": "eta_AB ~ sum_i (f_i^A-f_i^B) delta_w_i",
            "units": "dimensionless",
            "required_input": "material fractions, binding fractions, and experiment-specific projection",
            "status": "MISSING_ARENA_PROJECTION",
            "source_path": "TBD",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWS1764_3_bound_source",
            "quantity": "delta_w_species_bound",
            "meaning": "finite empirical upper bound if proof fails",
            "mathematical_form": "|delta_w_i-delta_w_j| <= bound_from_WEP_R10_PPN_clock_or_orbital_projection",
            "units": "dimensionless",
            "required_input": "source-backed bound table and projection convention",
            "status": "MISSING_SOURCE_BACKED_BOUND_TABLE",
            "source_path": "source-intake/rab-sector/acquisition-queue/JR1764_DELTAW_SPECIES_BOUND_INTERFACE.csv",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DWS1764_4_nonclaim_lock",
            "quantity": "local-GR/WEP/R10 claim status",
            "meaning": "species source-prefactor branch remains blocked",
            "mathematical_form": "claim_allowed=false until proof or finite sourced bound closes every required row",
            "units": "status",
            "required_input": "VAL1764 all pass plus future proof/bound validation",
            "status": "NONCLAIM_LOCK",
            "source_path": str(OUTPUTS["claim_gate"]),
            "valid_for_claim": False,
        },
    ]


def source_zero_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1764_0_q_src",
            "quantity": "q_src species label quotient",
            "current_status": "NOT_PARENT_SIGNED",
            "evidence": "LF1764_1 gives exact conditional theorem; SDF1764_2 keeps labelled-domain countermodel open",
            "remaining_gap": "prove source object is T_total before any coupling selection",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1764_1_no_w_A",
            "quantity": "source-only species prefactors w_A",
            "current_status": "NOT_EXCLUDED",
            "evidence": "PAC954_1 is the exact missing clause; MMA955_3 counterexample survives",
            "remaining_gap": "derive or adopt no-source-prefactor parent action clause",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1764_2_delta_w_species",
            "quantity": "delta_w_species",
            "current_status": "NOT_ZEROED",
            "evidence": "LF1764_5 retains residual",
            "remaining_gap": "parent-signed label forgetting plus no w_A, or finite bound interface filled",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1764_3_local_GR",
            "quantity": "local GR / WEP / R10 branch",
            "current_status": "NOT_CLAIMABLE",
            "evidence": "species source-prefactor leakage remains a live local source residual",
            "remaining_gap": "no local-GR, WEP, PPN, clock, orbital, or R10 pass allowed from 1764",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1764_4_next",
            "quantity": "next derivation owner",
            "current_status": "NO_SOURCE_PREFACTOR_CLAUSE_IS_NEXT",
            "evidence": "all open countermodels enter through w_A/label/spurion source slots",
            "remaining_gap": "build total-Hilbert-source-owner and no-prefactor parent clause",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1764_0_conditional_win",
            "decision": "LABEL_FORGOTTEN_SOURCE_FUNCTOR_THEOREM_IS_CLEAN",
            "reason": "once the source domain is T_total only, relative species couplings are not available variables",
            "next_action": "do not re-litigate Ward conservation; attack source-domain ownership",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1764_1_no_promotion",
            "decision": "DELTA_W_SPECIES_NOT_ZEROED",
            "reason": "labelled additive source maps and weighted matter actions remain current countermodels",
            "next_action": "retain delta_w_species as nonclaim residual",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1764_2_bound_fallback",
            "decision": "DELTA_W_SPECIES_BOUND_INTERFACE_STAGED",
            "reason": "if no-source-prefactor proof fails, the residual must become a finite sourced coefficient",
            "next_action": "fill component basis, composition projection and experiment bound rows only with sources",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1764_3_best_next",
            "decision": "NO_SOURCE_PREFACTOR_CLAUSE_IS_NEXT",
            "reason": "PAC954_1 is the exact high-pressure missing clause that blocks the label-forgetting theorem",
            "next_action": "build 1765 total Hilbert source owner and no-prefactor parent proof or delta_w_species bound input",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1764_4_no_claim",
            "decision": "LOCAL_SOURCE_BRANCH_REMAINS_PRIVATE_NONCLAIM",
            "reason": "1764 is a derivation gate and acquisition interface, not a local-GR/WEP pass",
            "next_action": "keep all claim gates closed",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1764_0_label_forgetting",
            "claim": "parent source functor forgets species labels",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PARENT_SOURCE_DOMAIN_QUOTIENT_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1764_1_no_source_prefactors",
            "claim": "no source-only species prefactors w_A",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_PAC954_1_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1764_2_no_hidden_spurion",
            "claim": "no hidden material/source spurion returns after variation",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_HIDDEN_SOURCE_SPURION_EXCLUSION_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1764_3_delta_w_species_zero",
            "claim": "delta_w_species=0",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_LABELLED_SOURCE_COUNTERMODEL_SURVIVES",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1764_4_delta_w_species_bound",
            "claim": "delta_w_species finite source-backed bound exists",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_COMPONENT_BASIS_PROJECTION_BOUND_TABLE_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1764_5_local_GR_WEP_R10",
            "claim": "local GR / WEP / R10 source branch passes",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "BLOCKED_DELTA_W_SPECIES_RETAINED",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1764_0_primary",
            "next_target": "1765-Y5-R2FR-total-Hilbert-source-owner-and-no-prefactor-clause-or-deltaw-species-bound-input.md",
            "script": "scripts/Y5_R2FR_total_Hilbert_source_owner_and_no_prefactor_clause_or_deltaw_species_bound_input.py",
            "objective": "prove the active ordinary source is the total Hilbert derivative of one matter action with no source-only species prefactor slots; otherwise begin finite delta_w_species bound input",
            "selection_status": "selected",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1764_1_fallback",
            "next_target": "1765b-Y5-R2FR-deltaw-species-component-projection-bound-pack.md",
            "script": "scripts/Y5_R2FR_deltaw_species_component_projection_bound_pack.py",
            "objective": "fill component basis, composition projection and WEP/R10/PPN/clock/orbital bound rows if the no-prefactor proof remains unsigned",
            "selection_status": "held_fallback",
            "valid_for_claim": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "label_forgetting": label_forgetting_rows(),
        "source_domain": source_domain_rows(),
        "countermodel": countermodel_rows(),
        "deltaw_species": deltaw_species_rows(),
        "source_zero_status": source_zero_status_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv_ok(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1764_SOURCE_REGISTER.csv")
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1764_{key.upper()}.csv")


def claim_like_field(key: str) -> bool:
    return key.lower() in {
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "prediction_allowed",
        "score_allowed",
        "claim_pass",
        "selected",
    }


def boolish_claim_true(key: str, value: Any) -> bool:
    if key.lower() == "selected":
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if claim_like_field(key) and boolish_claim_true(key, value):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    status_keys = {"current_status", "status", "proof_status", "proof_result"}
    for rows in rows_map.values():
        for row in rows:
            combined_status = " ".join(str(row.get(key, "")) for key in status_keys)
            if "MISSING_" in combined_status:
                for key, value in row.items():
                    if claim_like_field(key) and boolish_claim_true(key, value):
                        return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1764_SOURCE_REGISTER.csv").exists():
        return False
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1764_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched_for_1764() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1764*"))


def csv_parse_all() -> bool:
    return all(parse_csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def conditional_theorem_recorded(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "LF1764_1_conditional_theorem"
        and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM"
        and row["valid_for_claim"] is False
        for row in rows_map["label_forgetting"]
    )


def label_forgetting_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "LF1764_5_current_verdict"
        and row["proof_result"] == "DELTA_W_SPECIES_RETAINED"
        and row["claim_allowed"] is False
        for row in rows_map["label_forgetting"]
    )


def countermodel_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["countermodel_id"] == "CM1764_5_verdict"
        and row["survives_current_constraints"] is True
        and row["valid_for_claim"] is False
        for row in rows_map["countermodel"]
    )


def deltaw_interface_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["deltaw_species"]
    return any(row["row_id"] == "DWS1764_0_delta_w_species" for row in rows) and all(
        row["valid_for_claim"] is False for row in rows
    )


def source_zero_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["status_id"] == "SZ1764_3_local_GR"
        and row["current_status"] == "NOT_CLAIMABLE"
        and row["claim_allowed"] is False
        for row in rows_map["source_zero_status"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["route_id"] == "NEXT1764_0_primary" and row["selection_status"] == "selected"
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
        check_row("VAL1764_0_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check_row("VAL1764_1_needles_present", all(row["needles_present"] for row in sources), "required source needles are present", "one or more source needles missing"),
        check_row("VAL1764_2_conditional_theorem", conditional_theorem_recorded(rows_map), "conditional label-forgetting theorem recorded", "conditional theorem missing"),
        check_row("VAL1764_3_not_promoted", label_forgetting_not_promoted(rows_map), "label-forgetting branch remains unpromoted", "label-forgetting branch was promoted"),
        check_row("VAL1764_4_countermodel_retained", countermodel_retained(rows_map), "source countermodel remains retained", "source countermodel missing or promoted"),
        check_row("VAL1764_5_deltaw_interface_nonclaim", deltaw_interface_nonclaim(rows_map), "delta_w_species interface rows remain nonclaim", "delta_w_species interface missing or promoted"),
        check_row("VAL1764_6_source_zero_blocked", source_zero_blocked(rows_map), "local source status remains blocked", "local source status missing or promoted"),
        check_row("VAL1764_7_claim_gates_safe", all(row["gate_pass"] is False and row["status"] == "BLOCKED" for row in claim_gates), "all claim gates remain blocked", "one or more claim gates opened"),
        check_row("VAL1764_8_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check_row("VAL1764_9_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check_row(
            "VAL1764_10_decision_next",
            any(row["decision_id"] == "DEC1764_3_best_next" and row["decision"] == "NO_SOURCE_PREFACTOR_CLAUSE_IS_NEXT" for row in rows_map["decision"]),
            "decision selects no-source-prefactor route",
            "best-next decision missing",
        ),
        check_row("VAL1764_11_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check_row("VAL1764_12_csv_parse", csv_parse_all(), "all generated 1764 CSVs parse", "one or more generated 1764 CSVs fail to parse"),
        check_row("VAL1764_13_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "branch copies missing"),
        check_row("VAL1764_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check_row("VAL1764_15_formalization_untouched", formalization_untouched_for_1764(), "no 1764 outputs found under formalization-workbench", "1764 outputs found under formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in checks)
    checks.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1764_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1764 species-label forgetting source-functor parent proof or delta_w_species bound interface",
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
        "# 1764 - Species Label Forgetting Source-Functor Parent Proof Or Delta_w Species Bound",
        "",
        "## Verdict",
        "- 1764 proves the clean conditional route, but does not promote it to a claim.",
        "- If the parent action forms the ordinary active source as the total Hilbert/coframe derivative of one matter functional, with no source-only `w_A` slots and no hidden material spurion returning after variation, then `q_src({(T_A,A)})=T_total` and `delta_w_species=0` follows structurally.",
        "- The current parent corpus still has the exact missing clause: it does not yet prove that species labels and source-only prefactors are absent before source coupling selection.",
        "- Therefore labelled additive maps such as `F_src({(T_A,A)})=sum_A kappa_A T_A` and weighted matter actions `S_matter=sum_A w_A S_A` remain live countermodels.",
        "- `delta_w_species` is retained as a nonclaim residual; the fallback bound interface is staged but no numeric row is claimed.",
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Label-Forgetting Proof Attempt",
        markdown_table(rows_map["label_forgetting"], ["attempt_id", "claim_piece", "mathematical_form", "proof_status", "proof_result", "gap"]),
        "",
        "## Source Domain Fork Audit",
        markdown_table(rows_map["source_domain"], ["audit_id", "domain_choice", "mathematical_form", "consequence", "status", "remaining_gap"]),
        "",
        "## Countermodel Ledger",
        markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "mathematical_form", "survives_current_constraints", "why_survives", "what_kills_it"]),
        "",
        "## Delta-w Species Bound Interface",
        markdown_table(rows_map["deltaw_species"], ["row_id", "quantity", "meaning", "mathematical_form", "units", "status", "valid_for_claim"]),
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
        "This checkpoint is useful because it localizes the coupling wall. We no longer need to vaguely ask whether WEP or Ward identities save the branch. They do not, by themselves. The clean route is sharper: the parent theory must deny the existence of species-labelled source inputs before the source functor is even built. In plain terms, the next fight is the no-source-prefactor clause. If that closes, the relative source-coupling wound closes cleanly; if it does not, the branch must carry a finite `delta_w_species` coefficient into sourced WEP/R10/PPN/clock/orbital bounds.",
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
    doc_path = ROOT / "1764-Y5-R2FR-species-label-forgetting-source-functor-parent-proof-or-deltaw-species-bound.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1764 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()

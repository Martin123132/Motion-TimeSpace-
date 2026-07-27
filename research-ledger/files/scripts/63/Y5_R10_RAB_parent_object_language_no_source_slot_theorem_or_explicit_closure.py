from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1338"
TITLE = "1338-Y5-R10-RAB-parent-object-language-no-source-slot-theorem-or-explicit-closure"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
OBJECT_LANGUAGE_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_OBJECT_LANGUAGE_THEOREM_ATTEMPT.csv"
NO_SOURCE_SLOT_CLOSURE_PATH = OUT_DIR / f"{PACK_ID}_NO_SOURCE_SLOT_CLOSURE_CONDITION.csv"
LIVE_COUNTERMODEL_PATH = OUT_DIR / f"{PACK_ID}_LIVE_COUNTERMODEL_BOUNDARIES.csv"
PROMOTION_EVIDENCE_PATH = OUT_DIR / f"{PACK_ID}_PROMOTION_EVIDENCE_REQUIREMENTS.csv"
LOCAL_GR_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_GR_BRANCH_CONTRACT.csv"
THEOREM_STATUS_PATH = OUT_DIR / f"{PACK_ID}_COMMON_MODE_THEOREM_STATUS.csv"
RUNNER_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_UPDATE.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1338_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def bool_false(value: object) -> bool:
    return str(value).strip().lower() == "false"


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    for table in tables:
        for row in table:
            if "valid_for_claim" in row and not bool_false(row.get("valid_for_claim", False)):
                return False
            if "claim_allowed" in row and not bool_false(row.get("claim_allowed", False)):
                return False
    return True


def generated_inside_formalization() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [path for path in FORMALIZATION.rglob("*1338*") if path.is_file()]


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1338_0_1337_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1337_NEXT_TARGET.csv",
            "needle": "NEXT1337_0_1338",
            "role": "selected 1338 target",
        },
        {
            "source_id": "SRC1338_1_1337_premise",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1337_COMMON_MODE_PREMISE_REDUCTION.csv",
            "needle": "RED1337_3_no_source_only_species_slot",
            "role": "sharp missing premise from 1337",
        },
        {
            "source_id": "SRC1338_2_1337_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1337_MINIMAL_PARENT_ACTION_CONTRACT.csv",
            "needle": "PACT1337_2_no_source_only_species_slot",
            "role": "minimal parent action contract",
        },
        {
            "source_id": "SRC1338_3_1337_countermodel",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1337_ADMISSIBLE_COUNTERMODEL_LEDGER.csv",
            "needle": "CM1337_0_relative_source_weight",
            "role": "relative source-weight countermodel",
        },
        {
            "source_id": "SRC1338_4_1337_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1337_VALIDATION.csv",
            "needle": "VAL1337_11_overall",
            "role": "1337 pass gate",
        },
        {
            "source_id": "SRC1338_5_1214_no_slot",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1214_NO_SOURCE_ONLY_SLOT_SIGNATURE_AUDIT.csv",
            "needle": "NSS1214_5_verdict",
            "role": "previous no-source-only-slot verdict",
        },
        {
            "source_id": "SRC1338_6_1319_signature",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1319_MINIMAL_SIGNATURE_CANDIDATE.csv",
            "needle": "SIG1319_4_source_weight_exclusion",
            "role": "minimal signature candidate",
        },
        {
            "source_id": "SRC1338_7_1088_moms",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv",
            "needle": "MOMS1088_4_no_species_weights",
            "role": "minimal ordinary matter signature clause",
        },
        {
            "source_id": "SRC1338_8_1104_parent_signature",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1104_PARENT_SIGNATURE_LEDGER.csv",
            "needle": "SIG1104_4_source_weight_exclusion",
            "role": "ordinary-sector parent signature ledger",
        },
        {
            "source_id": "SRC1338_9_1236_meta",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1236_NO_HIDDEN_VISIBLE_COEFFICIENT_META_THEOREM.csv",
            "needle": "META1236_2_local_GR_consequence",
            "role": "typed coefficient meta-theorem local-GR consequence",
        },
        {
            "source_id": "SRC1338_10_1219_type",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_NO_HIDDEN_ARGUMENT_CONDITIONAL_THEOREM.csv",
            "needle": "NHA1219_0_type_rule",
            "role": "typed visible coefficient argument theorem",
        },
        {
            "source_id": "SRC1338_11_1046_forbidden_vertex",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1046_FORBIDDEN_VERTEX_CATALOG.csv",
            "needle": "FV1046_6_source_only_weight",
            "role": "forbidden source-only weight vertex catalog",
        },
        {
            "source_id": "SRC1338_12_1098_forbidden_audit",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1098_FORBIDDEN_VERTEX_AUDIT.csv",
            "needle": "FV1098_6_source_weight_X",
            "role": "source-weight forbidden-required audit",
        },
        {
            "source_id": "SRC1338_13_1065_grammar",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv",
            "needle": "PGG1065_5_verdict",
            "role": "parent grammar audit",
        },
        {
            "source_id": "SRC1338_14_1066_source_scalar",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
            "needle": "SSE1066_5_verdict",
            "role": "source-scalar exclusion lemma",
        },
        {
            "source_id": "SRC1338_15_1220_signature",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
            "needle": "PTOL1220_7_verdict",
            "role": "parent typed object-language verdict",
        },
    ]
    source_register = []
    for spec in source_specs:
        exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "exists": exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    object_language_attempt = [
        {
            "attempt_id": "OLT1338_0_target",
            "claim": "derive NoSourceOnlySpeciesSlot from the MTS parent object language",
            "formal_test": "show SpeciesLabel has no morphism into Coeff_active_source, while masses/charges/representations remain allowed matter data",
            "result": "TARGET_EXACT",
            "gap": "requires a parent-derived object-language constructor list, not a preferred action ansatz",
            "promotion_status": "NOT_PROMOTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "OLT1338_1_typed_domain",
            "claim": "typed coefficient domains exclude source-only species arguments",
            "formal_test": "Coeff_active_source accepts only observed geometry, fixed representation data, universal constants, and retained residual fields",
            "result": "EXACT_IF_GRAMMAR_ACCEPTED",
            "gap": "grammar acceptance remains conditional in 1219/1220/1236",
            "promotion_status": "CONDITIONAL_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "OLT1338_2_MTS_primitive_constructor",
            "claim": "motion/time/space primitives themselves generate no species source-weight constructor",
            "formal_test": "construct parent syntax from primitive motion, time, space, quotient, observed frame, and matter representation objects",
            "result": "NOT_DERIVED_CURRENT_CORPUS",
            "gap": "no authoritative primitive-to-parent-object-language derivation file is present",
            "promotion_status": "FAILED_TO_PROVE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "OLT1338_3_naturality",
            "claim": "category naturality forces source weights to be common",
            "formal_test": "Nat(ordinary species category,R_+) contains only constants",
            "result": "HELPFUL_BUT_INSUFFICIENT",
            "gap": "ordinary species can be disconnected simple objects unless the matter category is parent-connected",
            "promotion_status": "COUNTERMODEL_SURVIVES",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "OLT1338_4_action_scale_owner",
            "claim": "one parent action scale and measure makes w_A S_A impossible or gauge",
            "formal_test": "show all species action multipliers are quotient redundancies after quantum/path-integral/readout normalization",
            "result": "NOT_PARENT_SIGNED",
            "gap": "classical EOM rescaling does not remove Hilbert-source/path-integral weighting",
            "promotion_status": "COUNTERMODEL_SURVIVES",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "OLT1338_5_readout_stability",
            "claim": "EFT/radiative/readout maps preserve the no-source-slot grammar",
            "formal_test": "show loops, spectroscopy, WEP readout, and local projections cannot regenerate source-only coefficients",
            "result": "UNSIGNED_PARALLEL_GATE",
            "gap": "radiative/readout closure remains repeatedly unsigned",
            "promotion_status": "NOT_PROMOTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "OLT1338_6_verdict",
            "claim": "NoSourceOnlySpeciesSlot is a derived theorem",
            "formal_test": "assemble typed domain, primitive constructor list, naturality, action-scale owner, and readout stability",
            "result": "NOT_DERIVED_CURRENT_CORPUS",
            "gap": "the parent object language remains a closure grammar rather than a theorem from MTS primitives",
            "promotion_status": "DEMOTE_TO_EXPLICIT_CLOSURE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    closure_condition = [
        {
            "closure_id": "CLOS1338_0_parent_domain",
            "closure_clause": "one parent object language is declared before local tests, readout, or fitting",
            "formal_condition": "Arg(S_parent) is fixed before WEP/PPN/R10/clock/cosmology scoring",
            "protects": "prevents arena-by-arena source/readout slots",
            "if_absent": "hidden finite coefficients remain legal",
            "closure_status": "EXPLICIT_LOCAL_GR_SOURCE_CLOSURE_REQUIRED",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "CLOS1338_1_observed_descent",
            "closure_clause": "ordinary matter sees only the descended observed frame and owned observed gauge data",
            "formal_condition": "S_A=S_A[Psi_A,e_obs(q(Phi)),omega(e_obs),A_obs(q(Phi)),theta_A]",
            "protects": "kills representative-only frame/source leakage",
            "if_absent": "shadow frame and hidden marker countermodels remain",
            "closure_status": "EXPLICIT_LOCAL_GR_SOURCE_CLOSURE_REQUIRED",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "CLOS1338_2_no_source_only_species_slot",
            "closure_clause": "species labels do not select active gravitational source multipliers",
            "formal_condition": "Hom(SpeciesLabel,Coeff_active_source)=empty",
            "protects": "kills S_m=sum_A w_A S_A as a relative WEP/source residual",
            "if_absent": "relative source-weight branch remains live",
            "closure_status": "SHARPEST_EXPLICIT_CLOSURE",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "CLOS1338_3_single_measure_action_scale",
            "closure_clause": "ordinary matter shares one parent measure/action-scale/source normalization",
            "formal_condition": "no species-dependent measure Jacobian, hbar/action multiplier, or source-only scale",
            "protects": "prevents w_A from re-entering as measure/action normalization",
            "if_absent": "species measure-weight countermodel remains live",
            "closure_status": "EXPLICIT_LOCAL_GR_SOURCE_CLOSURE_REQUIRED",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "CLOS1338_4_variation_before_readout",
            "closure_clause": "Hilbert/source current extraction precedes material/readout projection",
            "formal_condition": "T_total := delta S_m/delta g_obs before WEP/readout/source-worldtube reduction",
            "protects": "blocks post-variation source selectors",
            "if_absent": "readout can manufacture species source weights",
            "closure_status": "EXPLICIT_LOCAL_GR_SOURCE_CLOSURE_REQUIRED",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "CLOS1338_5_radiative_readout_preservation",
            "closure_clause": "effective actions and readout maps preserve the same coefficient domain",
            "formal_condition": "S_eff/readout coefficients factor through q_obs, representation constants, or retained residuals",
            "protects": "prevents loop/readout regeneration of source-only weights",
            "if_absent": "bare zero theorem cannot be transferred to observable rows",
            "closure_status": "EXPLICIT_LOCAL_GR_SOURCE_CLOSURE_REQUIRED",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    countermodel_boundaries = [
        {
            "countermodel_id": "CM1338_0_relative_wA",
            "form": "S_m=sum_A w_A S_A with constant relative w_A",
            "why_allowed_without_closure": "covariant, additive, compatible with same Hilbert variation, and not killed by observed descent alone",
            "closure_clause_that_kills_it": "CLOS1338_2_no_source_only_species_slot",
            "if_not_killed": "must be bounded as finite source/WEP coefficient",
            "status": "LIVE_COUNTERMODEL_UNTIL_CLOSURE_DERIVED_OR_ADOPTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CM1338_1_species_measure_weight",
            "form": "S_m=sum_A integral w_A mu(g_obs)L_A",
            "why_allowed_without_closure": "scalar measure-weight version of the same source normalization issue",
            "closure_clause_that_kills_it": "CLOS1338_3_single_measure_action_scale",
            "if_not_killed": "must be retained as source-normalization residual",
            "status": "LIVE_COUNTERMODEL_UNTIL_CLOSURE_DERIVED_OR_ADOPTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CM1338_2_hidden_marker_relabel",
            "form": "w_A=w(marker_A,domain,boundary,hidden invariant)",
            "why_allowed_without_closure": "source-only slot can be smuggled through a marker/domain scalar if coefficient domains are not sealed",
            "closure_clause_that_kills_it": "CLOS1338_0_parent_domain;CLOS1338_5_radiative_readout_preservation",
            "if_not_killed": "must be carried into PPN/WEP/clock/readout residual vector",
            "status": "LIVE_COUNTERMODEL_UNTIL_CLOSURE_DERIVED_OR_ADOPTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CM1338_3_nonHilbert_readout_current",
            "form": "J_source=T_Hilbert+sum_A zeta_A J_A_readout",
            "why_allowed_without_closure": "can be covariant if the added currents are conserved or projected",
            "closure_clause_that_kills_it": "CLOS1338_4_variation_before_readout;CLOS1338_5_radiative_readout_preservation",
            "if_not_killed": "source-side local GR remains closure-only",
            "status": "LIVE_COUNTERMODEL_UNTIL_CLOSURE_DERIVED_OR_ADOPTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    promotion_evidence = [
        {
            "requirement_id": "REQ1338_0_primitive_constructor_list",
            "needed_evidence": "parent object-language constructors derived from motion/time/space primitives",
            "would_prove": "there is no constructor that maps SpeciesLabel to active-source coefficient",
            "current_evidence": "not found in current 1338 source trail",
            "status": "MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "REQ1338_1_species_representation_split",
            "needed_evidence": "proof that species labels only choose matter representations/theta_A, never gravitational source multipliers",
            "would_prove": "masses/charges remain physical while w_A is syntactically impossible",
            "current_evidence": "conditional typing rows only",
            "status": "MISSING_PARENT_PROOF",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "REQ1338_2_action_measure_owner",
            "needed_evidence": "one parent action scale, measure, and source normalization owner across ordinary matter",
            "would_prove": "species action multipliers cannot re-enter as measure or quantum normalization",
            "current_evidence": "repeatedly marked unsigned",
            "status": "MISSING_PARENT_PROOF",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "REQ1338_3_variation_readout_order",
            "needed_evidence": "proof that all WEP/PPN/clock/readout projections operate after Hilbert current extraction",
            "would_prove": "readout cannot manufacture a source-only species current",
            "current_evidence": "conditional subtheorem only",
            "status": "MISSING_PARENT_PROOF",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "REQ1338_4_radiative_stability",
            "needed_evidence": "proof that S_eff, loops, spectroscopy, and local readouts preserve the typed coefficient domain",
            "would_prove": "bare no-source-slot closure survives to observed tests",
            "current_evidence": "explicitly unsigned in 1220/1319/1104",
            "status": "MISSING_PARENT_PROOF",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    local_gr_contract = [
        {
            "contract_id": "LGRCON1338_0_source_side_closure",
            "branch": "local-GR source side",
            "condition": "CLOS1338_0 through CLOS1338_5 are derived or explicitly adopted as closure",
            "result_if_condition_holds": "ordinary matter source is one calibrated Hilbert T_total with no relative species source weights",
            "result_now": "CONDITIONAL_CLOSURE_ONLY",
            "blocks_full_GR_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "LGRCON1338_1_geometric_left_hand",
            "branch": "local-GR geometric side",
            "condition": "observed field equation left-hand side reduces to EH/Newton/PPN operator",
            "result_if_condition_holds": "source-side closure could be combined with geometry for a real GR limit proof",
            "result_now": "STILL_REQUIRED_SEPARATE_PROOF",
            "blocks_full_GR_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "LGRCON1338_2_finite_residual_route",
            "branch": "if no-source-slot closure is not adopted",
            "condition": "w_A/source/readout residuals remain live",
            "result_if_condition_holds": "local WEP/PPN/clock/orbital branches need explicit finite coefficient bounds",
            "result_now": "RETAINED_FALLBACK_BRANCH",
            "blocks_full_GR_claim": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    theorem_status = [
        {
            "status_id": "THMSTAT1338_0_no_source_slot",
            "statement": "NoSourceOnlySpeciesSlot is not derived from current MTS primitives",
            "classification": "EXPLICIT_CLOSURE_CONDITION",
            "reason": "all available proofs depend on a parent grammar/action-domain certificate that is itself unsigned",
            "effect": "common-mode source coupling cannot be advertised as theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "THMSTAT1338_1_common_mode",
            "statement": "common-mode source coupling remains a strong exact conditional theorem",
            "classification": "CONDITIONAL_LOCAL_GR_SOURCE_ROUTE",
            "reason": "if the closure clauses are signed/adopted, relative source weights collapse into calibrated common mode",
            "effect": "usable as private discipline branch, not public local-GR claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "THMSTAT1338_2_countermodel_policy",
            "statement": "without closure, the finite relative-source branch remains live",
            "classification": "FINITE_RESIDUAL_OR_BOUND_ROUTE",
            "reason": "w_A countermodels satisfy the currently derived constraints",
            "effect": "retain WEP/PPN/clock/orbital bound interface",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_update = [
        {
            "runner_id": "RUN1338_0_no_source_slot_theorem",
            "target": "derive NoSourceOnlySpeciesSlot",
            "input_status": "PARENT_GRAMMAR_UNSIGNED",
            "runner_status": "DERIVATION_FAILED_DEMOTED_TO_CLOSURE",
            "score_ready": False,
            "reason": "no primitive constructor proof or parent grammar certificate exists",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1338_1_common_mode_closure",
            "target": "explicit local-GR source-side closure",
            "input_status": "CLOSURE_CONDITIONS_WRITTEN",
            "runner_status": "CONDITIONAL_BRANCH_READY_NOT_CLAIMED",
            "score_ready": False,
            "reason": "closure is explicit but not parent-derived; geometric EH/Newton side still separate",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1338_0_no_minimality_as_proof",
            "shortcut": "treat absence from a preferred action as derivation",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1338_1_no_type_rule_overclaim",
            "shortcut": "promote conditional type rules without parent grammar certificate",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1338_2_no_countermodel_erasure",
            "shortcut": "delete w_A countermodels because they are ugly",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1338_3_no_local_GR_claim",
            "shortcut": "claim local GR/Newton reduction from source-side closure",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1338_0_theorem_result",
            "decision": "NoSourceOnlySpeciesSlot is not derived in the current corpus",
            "because": "typed/object-language proofs require a parent grammar certificate that is not derived from MTS primitives",
            "effect": "common-mode source coupling is now explicitly closure-only unless future work derives the grammar",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1338_1_framework_hygiene",
            "decision": "keep the closure because it is the precise GR-like source premise, but label it honestly",
            "because": "it prevents hidden post-hoc coupling choices while preserving the live finite-residual route",
            "effect": "the project is cleaner: either derive this closure later or bound the residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1338_2_next_route",
            "decision": "move toward the local-GR spine under explicit source closure while separately tracking the missing derivation",
            "because": "remaining stuck on the same unsigned grammar would stall; the geometric EH/Newton side is the other required half",
            "effect": "next target builds the closure-declared source-side ledger into a geometric left-hand reduction gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1338_0_1339",
            "target_file": "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md",
            "target_script": "scripts/Y5_R10_RAB_source_closure_to_EH_left_hand_local_GR_reduction_gate.py",
            "task": "with source-side common mode now explicit as closure, build the next local-GR gate: whether the observed field equation left-hand side reduces to EH/Newton/PPN or retains an explicit residual vector",
            "success_condition": "a clean separation between source-side closure, EH/Newton geometric reduction, and retained PPN/readout residuals",
            "do_not": "do not claim full local GR, do not hide NoSourceOnlySpeciesSlot as derived, do not drop live finite source-weight countermodels",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables_for_nonclaim = [
        source_register,
        object_language_attempt,
        closure_condition,
        countermodel_boundaries,
        promotion_evidence,
        local_gr_contract,
        theorem_status,
        runner_update,
        anti_shortcut,
        decision,
        next_target,
    ]

    source_anchor_count = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    theorem_not_derived = any(row["attempt_id"] == "OLT1338_6_verdict" and row["result"] == "NOT_DERIVED_CURRENT_CORPUS" for row in object_language_attempt)
    closure_explicit = any(row["closure_id"] == "CLOS1338_2_no_source_only_species_slot" and row["closure_status"] == "SHARPEST_EXPLICIT_CLOSURE" for row in closure_condition)
    countermodels_live = all(str(row["status"]).startswith("LIVE_COUNTERMODEL") for row in countermodel_boundaries)
    promotion_missing = all(str(row["status"]).startswith("MISSING") for row in promotion_evidence)
    local_gr_blocked = all(row["blocks_full_GR_claim"] is True for row in local_gr_contract)
    runners_not_scoreable = all(row["score_ready"] is False and row["valid_prediction_row"] is False for row in runner_update)
    shortcuts_enforced = all(row["status"] == "ENFORCED" for row in anti_shortcut)
    nonclaim = all_nonclaim(tables_for_nonclaim)
    formal_clean = len(generated_inside_formalization()) == 0
    next_is_1339 = next_target[0]["target_file"].startswith("1339-")

    validations = [
        validation_row(
            "VAL1338_0_sources_exist",
            "registered local source paths exist and anchors are found",
            source_anchor_count == len(source_register),
            f"{source_anchor_count}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1338_1_theorem_not_derived",
            "NoSourceOnlySpeciesSlot is not promoted as derived",
            theorem_not_derived,
            "OLT1338_6_verdict=NOT_DERIVED_CURRENT_CORPUS",
        ),
        validation_row(
            "VAL1338_2_closure_explicit",
            "NoSourceOnlySpeciesSlot is written as explicit closure",
            closure_explicit,
            "CLOS1338_2_no_source_only_species_slot=SHARPEST_EXPLICIT_CLOSURE",
        ),
        validation_row(
            "VAL1338_3_countermodels_live",
            "all source-slot countermodels remain live unless closure is derived or adopted",
            countermodels_live,
            ";".join(row["countermodel_id"] for row in countermodel_boundaries),
        ),
        validation_row(
            "VAL1338_4_promotion_evidence_missing",
            "promotion requirements remain missing parent proofs",
            promotion_missing,
            ";".join(f"{row['requirement_id']}={row['status']}" for row in promotion_evidence),
        ),
        validation_row(
            "VAL1338_5_local_GR_blocked",
            "full local GR/Newton claim remains blocked",
            local_gr_blocked,
            ";".join(f"{row['contract_id']}={row['result_now']}" for row in local_gr_contract),
        ),
        validation_row(
            "VAL1338_6_runners_not_scoreable",
            "runners refuse WEP/local-GR scoring",
            runners_not_scoreable,
            ";".join(f"{row['runner_id']}={row['runner_status']}" for row in runner_update),
        ),
        validation_row(
            "VAL1338_7_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            shortcuts_enforced,
            ";".join(row["gate_id"] for row in anti_shortcut),
        ),
        validation_row(
            "VAL1338_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim,
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1338_9_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            formal_clean,
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        ),
        validation_row(
            "VAL1338_10_next_target_1339",
            "next target routes to EH-left-hand local-GR reduction gate",
            next_is_1339,
            str(next_target[0]["target_file"]),
        ),
    ]
    validations.append(
        validation_row(
            "VAL1338_11_overall",
            "overall 1338 validation",
            all(row["status"] == "PASS" for row in validations),
            "1338 demotes NoSourceOnlySpeciesSlot to explicit closure and preserves local-GR/source claims as conditional only",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(OBJECT_LANGUAGE_ATTEMPT_PATH, object_language_attempt)
    write_csv(NO_SOURCE_SLOT_CLOSURE_PATH, closure_condition)
    write_csv(LIVE_COUNTERMODEL_PATH, countermodel_boundaries)
    write_csv(PROMOTION_EVIDENCE_PATH, promotion_evidence)
    write_csv(LOCAL_GR_CONTRACT_PATH, local_gr_contract)
    write_csv(THEOREM_STATUS_PATH, theorem_status)
    write_csv(RUNNER_UPDATE_PATH, runner_update)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# {TITLE}

**Current verdict:** 1338 does **not** derive `NoSourceOnlySpeciesSlot` from current MTS primitives. The typed/object-language route is powerful, but it depends on a parent grammar certificate that the corpus still marks unsigned.

**Main progress:** the missing source-side GR premise is no longer vague. It is now an explicit closure condition: species labels may choose representation data, masses, charges, and measured matter constants, but may not choose an active gravitational source multiplier `w_A`.

**Decision:** common-mode source coupling is retained as a strong conditional local-GR source branch, not as a derived theorem. Next work should use this source closure honestly while attacking the other half of local GR: the EH/Newton/PPN left-hand reduction gate.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Object-Language Theorem Attempt
{markdown_table(object_language_attempt, ["attempt_id", "claim", "formal_test", "result", "gap", "promotion_status", "valid_for_claim", "claim_allowed"])}

## No-Source-Slot Closure Condition
{markdown_table(closure_condition, ["closure_id", "closure_clause", "formal_condition", "protects", "if_absent", "closure_status", "parent_signed", "valid_for_claim", "claim_allowed"])}

## Live Countermodel Boundaries
{markdown_table(countermodel_boundaries, ["countermodel_id", "form", "why_allowed_without_closure", "closure_clause_that_kills_it", "if_not_killed", "status", "valid_for_claim", "claim_allowed"])}

## Promotion Evidence Requirements
{markdown_table(promotion_evidence, ["requirement_id", "needed_evidence", "would_prove", "current_evidence", "status", "valid_for_claim", "claim_allowed"])}

## Local GR Branch Contract
{markdown_table(local_gr_contract, ["contract_id", "branch", "condition", "result_if_condition_holds", "result_now", "blocks_full_GR_claim", "valid_for_claim", "claim_allowed"])}

## Common-Mode Theorem Status
{markdown_table(theorem_status, ["status_id", "statement", "classification", "reason", "effect", "valid_for_claim", "claim_allowed"])}

## Runner Update
{markdown_table(runner_update, ["runner_id", "target", "input_status", "runner_status", "score_ready", "reason", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## Anti-Shortcut Gates
{markdown_table(anti_shortcut, ["gate_id", "shortcut", "enforcement", "status", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decision, ["decision_id", "decision", "because", "effect", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()

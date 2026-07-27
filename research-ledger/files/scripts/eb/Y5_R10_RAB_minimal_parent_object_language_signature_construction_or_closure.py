from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1319"
TITLE = "1319-Y5-R10-RAB-minimal-parent-object-language-signature-construction-or-closure"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
SIGNATURE_CANDIDATE_PATH = OUT_DIR / f"{PACK_ID}_MINIMAL_SIGNATURE_CANDIDATE.csv"
CLAUSE_CONSTRUCTION_PATH = OUT_DIR / f"{PACK_ID}_CLAUSE_CONSTRUCTION_ATTEMPT.csv"
DERIVATION_GAP_PATH = OUT_DIR / f"{PACK_ID}_DERIVATION_GAP_LEDGER.csv"
CLOSURE_DEMOTION_PATH = OUT_DIR / f"{PACK_ID}_THEOREM_ROUTE_CLOSURE_DEMOTION.csv"
FINITE_SOURCE_MAP_PATH = OUT_DIR / f"{PACK_ID}_FINITE_SOURCE_ROW_SURVIVAL_MAP.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1319_VALIDATION.csv"


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


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        SIGNATURE_CANDIDATE_PATH,
        CLAUSE_CONSTRUCTION_PATH,
        DERIVATION_GAP_PATH,
        CLOSURE_DEMOTION_PATH,
        FINITE_SOURCE_MAP_PATH,
        ANTI_SHORTCUT_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def compact_bool(value: object) -> bool:
    return str(value).strip().lower() == "true"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1319_0_1318_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1318_NEXT_TARGET.csv",
            "needle": "NEXT1318_0_1319",
            "role": "handoff into minimal parent object-language construction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1319_1_1055_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
            "needle": "PAC1055_6_single_parent_action",
            "role": "single parent action contract candidate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1319_2_1055_adoption",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1055_CONTRACT_ADOPTION_GATES.csv",
            "needle": "ADG1055_4_radiative_closure",
            "role": "contract adoption and radiative closure gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1319_3_1065_parent_grammar",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv",
            "needle": "PGG1065_5_verdict",
            "role": "parent grammar verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1319_4_1065_allowed",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1065_ALLOWED_ACTION_GRAMMAR.csv",
            "needle": "AAG1065_4_source_only_species_scalar",
            "role": "allowed/prohibited action grammar slots",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1319_5_1065_wzero",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1065_WA_THEOREM_ZERO_CLAUSES.csv",
            "needle": "WTZ1065_4_verdict",
            "role": "w_A theorem-zero verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1319_6_1066_typing",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv",
            "needle": "OLT1066_6_verdict",
            "role": "object-language typing audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1319_7_1066_domain",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_OPERATOR_DOMAIN_RULE_AUDIT.csv",
            "needle": "ODR1066_4_verdict",
            "role": "operator-domain rule audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1319_8_1066_scalar",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
            "needle": "SSE1066_5_verdict",
            "role": "source-scalar exclusion lemma",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1319_9_1066_fmq",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv",
            "needle": "FMQ1066_4_verdict",
            "role": "field/measure/quantum normalization audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1319_10_1220_signature",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
            "needle": "PARENT_TYPED_OBJECT_LANGUAGE_SIGNATURE_NOT_DERIVED",
            "role": "latest parent typed signature attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1319_11_1219_functor",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1219_TYPED_VISIBLE_COEFFICIENT_FUNCTOR_ATTEMPT.csv",
            "needle": "TYPED_VISIBLE_COEFFICIENT_FUNCTOR_NOT_DERIVED",
            "role": "typed visible coefficient functor attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1319_12_1114_nohidden",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv",
            "needle": "NO_HIDDEN_VISIBLE_MORPHISM_NOT_DERIVED",
            "role": "no-hidden-visible morphism attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1319_13_1115_invariant",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1115_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY_ATTEMPT.csv",
            "needle": "LOCAL_INVARIANT_ALGEBRA_TRIVIALITY_NOT_DERIVED",
            "role": "local invariant algebra triviality attempt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    signature_candidate = [
        {
            "candidate_id": "SIG1319_0_single_parent_action",
            "signature_clause": "one parent variational object owns geometry, EM, matter, source, and readout",
            "minimal_form": "S_parent=S_geom[Phi]+S_hidden[Phi]+S_EM[q(Phi),A_Q,ell_EM]+sum_A S_A[Psi_A,q(Phi),A_Q,theta_A]+S_boundary[q(Phi)]",
            "best_evidence": "PAC1055_6_single_parent_action;PTOL1220_0_parent_domain",
            "construction_status": "CONTRACT_FORM_READY_NOT_DERIVED",
            "why_not_signed": "schema is written as a discipline contract, not derived from deeper MTS primitives",
            "if_signed_effect": "prevents post-hoc source/readout closures after local tests",
            "closure_status": "CLOSURE_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "SIG1319_1_visible_coefficient_domain",
            "signature_clause": "visible coefficients depend only on q_loc and fixed representation/topological data",
            "minimal_form": "Coeff(O_vis) subset Alg[q_loc,Theta_rep,Level_EM]",
            "best_evidence": "PAC1055_3_no_mixed_coefficients;ODR1066_0_allowed_coefficient_ring;PTOL1220_1_visible_coefficient_domain",
            "construction_status": "POWERFUL_RULE_NOT_DERIVED",
            "why_not_signed": "operator-domain exclusion is a powerful rule, but the parent operator classification is not derived",
            "if_signed_effect": "kills f(I_hid)F_Q^2, hidden mass/readout coefficients, and source-weight maps",
            "closure_status": "CLOSURE_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "SIG1319_2_no_hidden_argument_rule",
            "signature_clause": "hidden/local representatives are not well-typed coefficient arguments",
            "minimal_form": "Hom(C_hid,Coeff(O_vis)) is absent in the parent syntax",
            "best_evidence": "TVC1219_1_typed_domain_theorem;NHV1114_1_typed_language",
            "construction_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "why_not_signed": "the type theorem works if the grammar is accepted, but grammar acceptance is not derived",
            "if_signed_effect": "turns no-hidden-visible coefficient morphism into theorem-zero route",
            "closure_status": "CLOSURE_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "SIG1319_3_matter_functor",
            "signature_clause": "ordinary matter descends through observed coframe and fixed measured matter parameters",
            "minimal_form": "S_A=S_A[Psi_A,e_obs(q),omega(e_obs(q)),A_Q,theta_A] with Lie_v theta_A=0",
            "best_evidence": "PAC1055_2_matter_functor;PTOL1220_2_matter_bundle_constants",
            "construction_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "why_not_signed": "matter bundle/category and fixed vertical lift for all ordinary species are not constructed",
            "if_signed_effect": "blocks hidden mass, binding, and clock marker dependence",
            "closure_status": "CLOSURE_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "SIG1319_4_source_weight_exclusion",
            "signature_clause": "source-only species weights are not parent matter-language objects",
            "minimal_form": "w_A not in Obj(Language); Hilbert source is species-blind after variation",
            "best_evidence": "PGG1065_5_verdict;SSE1066_5_verdict;WTZ1065_4_verdict",
            "construction_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "why_not_signed": "parent category object-language and action-scale owner are still unsigned",
            "if_signed_effect": "sets relative source-weight branch to zero before WEP/R10 products",
            "closure_status": "CLOSURE_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "SIG1319_5_measure_action_scale_owner",
            "signature_clause": "one parent action scale/measure/hbar owner covers ordinary matter",
            "minimal_form": "no species-dependent w_A S_A, measure Jacobian, or effective hbar source multiplier",
            "best_evidence": "FMQ1066_4_verdict;PTOL1220_4_action_scale_measure_owner",
            "construction_status": "NOT_PARENT_SIGNED",
            "why_not_signed": "field/measure/quantum normalization can still reintroduce source weights",
            "if_signed_effect": "removes action-scale source-weight counterexample",
            "closure_status": "CLOSURE_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "SIG1319_6_no_extension_no_marker",
            "signature_clause": "no marker/domain/boundary/hidden invariant extends coefficient domains",
            "minimal_form": "no co-moving marker, domain selector, boundary class, or nonconstant hidden invariant enters Coeff(O_vis)",
            "best_evidence": "PTOL1220_6_no_extension_no_marker;LIA1115_6_verdict",
            "construction_status": "NOT_DERIVED",
            "why_not_signed": "surviving scalar/invariant generator debts remain active",
            "if_signed_effect": "removes continuous hidden scalar counterexample",
            "closure_status": "CLOSURE_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "SIG1319_7_radiative_readout_closure",
            "signature_clause": "effective/readout maps preserve the same typed coefficient domain",
            "minimal_form": "S_eff and clock/WEP/R10/local readout maps remain in Alg[q_loc,Theta_rep,Level_EM]",
            "best_evidence": "PAC1055_5_radiative_readout_closure;PTOL1220_5_radiative_readout_closure;NHV1114_5_radiative_readout",
            "construction_status": "UNSIGNED_CRITICAL",
            "why_not_signed": "loops, spectroscopy, MICROSCOPE/readout projection, and local readout are not proven to preserve the domain",
            "if_signed_effect": "lets bare theorem-zero statements survive into observable products",
            "closure_status": "CLOSURE_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    clause_construction = [
        {
            "step_id": "CONST1319_0_domain",
            "attempt": "derive parent object domain from MTS primitives",
            "input_clauses": "PAC1055_0_configuration_and_quotient;PAC1055_6_single_parent_action",
            "construction_test": "is q_loc/pi_const/vertical distribution forced by MTS rather than adopted?",
            "result": "FAILED_DERIVATION_CONTRACT_ONLY",
            "consequence": "parent object-language remains an axiom-shaped closure, not a theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "step_id": "CONST1319_1_coefficient_ring",
            "attempt": "derive visible coefficient ring restriction",
            "input_clauses": "PAC1055_3_no_mixed_coefficients;ODR1066_0_allowed_coefficient_ring",
            "construction_test": "does the parent syntax force Coeff(O_vis) subset Alg[q_loc,Theta_rep,Level_EM]?",
            "result": "FAILED_DERIVATION_POWERFUL_IF_SIGNED",
            "consequence": "f(I_hid)F_Q^2 and hidden continuous coefficient maps remain legal closure terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "step_id": "CONST1319_2_no_hidden",
            "attempt": "derive no hidden-visible coefficient morphism",
            "input_clauses": "TVC1219_1_typed_domain_theorem;NHV1114_1_typed_language",
            "construction_test": "can the exact conditional type theorem be parent-signed?",
            "result": "FAILED_DERIVATION_EXACT_CONDITIONAL_ONLY",
            "consequence": "conditional theorem retained, but not usable as b_alpha=0 proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "step_id": "CONST1319_3_source_scalar",
            "attempt": "derive source-only scalar exclusion",
            "input_clauses": "PGG1065_5_verdict;SSE1066_5_verdict;WTZ1065_4_verdict",
            "construction_test": "does parent matter grammar forbid inert source-only species scalars before variation?",
            "result": "FAILED_DERIVATION_CONDITIONAL_ONLY",
            "consequence": "WEP/R10 source-weight branch remains finite/source-backed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "step_id": "CONST1319_4_measure_owner",
            "attempt": "derive common action-scale/measure owner",
            "input_clauses": "FMQ1066_4_verdict;PTOL1220_4_action_scale_measure_owner",
            "construction_test": "are action-scale multipliers gauge/quotient redundant for source and quantum measure?",
            "result": "FAILED_DERIVATION_NOT_PARENT_SIGNED",
            "consequence": "species-dependent action multipliers remain source-coupling counterexamples",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "step_id": "CONST1319_5_readout",
            "attempt": "derive radiative/readout closure",
            "input_clauses": "PAC1055_5_radiative_readout_closure;PTOL1220_5_radiative_readout_closure",
            "construction_test": "do loops/readout maps preserve the typed coefficient domain?",
            "result": "FAILED_DERIVATION_UNSIGNED_CRITICAL",
            "consequence": "bare-action zeros cannot be transferred to clock/WEP/R10/local observables",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    derivation_gap = [
        {
            "gap_id": "GAP1319_0_deeper_mts_q",
            "missing_derivation": "q_loc, pi_const, and vertical distribution forced by MTS primitives",
            "blocks": "single parent object-language signature",
            "current_best": "PAC1055 contract form",
            "required_to_promote": "derive q_loc/pi_const/ker(Dq) cap ker(Dpi_const) from parent fields, not from post-hoc discipline",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gap_id": "GAP1319_1_operator_classification",
            "missing_derivation": "parent operator classification forbids hidden arguments in visible coefficients",
            "blocks": "b_alpha=0, mass/clock/source theorem-zero",
            "current_best": "ODR1066 and TVC1219 exact conditional rules",
            "required_to_promote": "show Hom(C_hid,Coeff(O_vis)) is absent from the object language",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gap_id": "GAP1319_2_invariant_algebra",
            "missing_derivation": "hidden invariant algebra is trivial or forbidden as coefficient argument",
            "blocks": "continuous scalar coefficient counterexample",
            "current_best": "LIA1115 conditional sufficiency plus obstruction",
            "required_to_promote": "kill all surviving marker/domain/memory/readout scalar generators",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gap_id": "GAP1319_3_source_language",
            "missing_derivation": "source-only species weights are syntactically impossible",
            "blocks": "WEP/R10 source-weight theorem-zero",
            "current_best": "PGG1065/SSE1066 conditional source-scalar exclusion",
            "required_to_promote": "derive parent matter category and source-label forgetting before coupling selection",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gap_id": "GAP1319_4_measure_owner",
            "missing_derivation": "universal action-scale/measure/hbar owner",
            "blocks": "field/measure/quantum source-normalization loophole",
            "current_best": "FMQ1066 audit",
            "required_to_promote": "show species action multipliers cannot affect Hilbert source or quantum measure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gap_id": "GAP1319_5_readout_closure",
            "missing_derivation": "RG/effective/readout maps preserve the typed domain",
            "blocks": "observable clock/WEP/R10/local theorem-zero transfer",
            "current_best": "PAC1055_5 and PTOL1220_5 state required closure",
            "required_to_promote": "prove loops/spectroscopy/MICROSCOPE/local projections cannot regenerate hidden coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    closure_demotion = [
        {
            "demotion_id": "DEM1319_0_parent_signature",
            "route": "minimal parent object-language theorem-zero route",
            "status": "DEMOTED_TO_CLOSURE_ONLY_FOR_NOW",
            "because": "construction attempt yields a coherent contract candidate but no derivation from MTS primitives",
            "consequence": "cannot claim b_alpha=0, source-weight zero, cross-arena transfer, or local-GR silence from this route",
            "reopen_condition": "derive every GAP1319 clause or add a source-backed parent primitive",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "demotion_id": "DEM1319_1_alpha",
            "route": "b_alpha/c_alpha theorem-zero",
            "status": "CLOSURE_ONLY",
            "because": "visible coefficient-domain and radiative/readout clauses are unsigned",
            "consequence": "1317 alpha coefficient/source row remains active",
            "reopen_condition": "signed alpha F2 owner plus no-hidden/radiative closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "demotion_id": "DEM1319_2_wep_r10_source",
            "route": "source-weight theorem-zero",
            "status": "CLOSURE_ONLY",
            "because": "source grammar and action-scale/measure owner are unsigned",
            "consequence": "WEP and R10 source normalization inputs remain active",
            "reopen_condition": "signed source-scalar exclusion plus measure/action-scale owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "demotion_id": "DEM1319_3_readout_transfer",
            "route": "clock/WEP/R10/local readout transfer",
            "status": "CLOSURE_ONLY",
            "because": "radiative/readout closure is explicitly unsigned",
            "consequence": "no bound transfer between arenas without a direct product map",
            "reopen_condition": "RG/effective/readout theorem preserving parent coefficient domain",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_source_map = [
        {
            "survival_id": "SURV1319_0_alpha",
            "source_row": "RUN1317_0_run1314_0_alpha",
            "survives_because": "b_alpha/c_alpha theorem-zero closure not signed",
            "needed_next_input": "numeric b_alpha/c_alpha or signed alpha F2 owner certificate",
            "priority": "P0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "survival_id": "SURV1319_1_clock",
            "source_row": "RUN1317_1_run1314_1_clock",
            "survives_because": "readout transfer closure not signed",
            "needed_next_input": "tau_clock/readout map or direct clock alpha product",
            "priority": "P0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "survival_id": "SURV1319_2_wep",
            "source_row": "RUN1317_2_run1314_2_wep",
            "survives_because": "source-weight theorem-zero closure not signed",
            "needed_next_input": "beta_source_alpha, tau_WEP, material response, source profile, readout kernel",
            "priority": "P0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "survival_id": "SURV1319_3_r10",
            "source_row": "RUN1317_3_run1314_3_r10",
            "survives_because": "alpha/source theorem-zero and R10 product vector/bound curve are not signed",
            "needed_next_input": "lambda_X, Z_X, K_X(lambda), beta_source/test, tau_R10, epsilon_tail, promoted alpha_bound(lambda)",
            "priority": "P0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "survival_id": "SURV1319_4_cross_arena",
            "source_row": "RUN1317_4_run1314_4_cross_arena",
            "survives_because": "parent branch/readout functor not signed",
            "needed_next_input": "same-branch classifier and arena maps or explicit nontransfer declaration",
            "priority": "P1",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1319_0_no_contract_as_derivation",
            "shortcut": "treat a coherent contract candidate as derived parent theorem",
            "status": "ENFORCED",
            "reason": "1055/1220 explicitly mark the parent signature as not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1319_1_no_conditional_as_signed",
            "shortcut": "use exact conditional typed theorem as signed proof",
            "status": "ENFORCED",
            "reason": "TVC1219/NHV1114 are exact only if parent grammar is signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1319_2_no_absence_as_zero",
            "shortcut": "promote absence of f(I_hid)F_Q^2 or w_A in a written action to theorem-zero",
            "status": "ENFORCED",
            "reason": "operator-domain and source-scalar exclusions are not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1319_3_no_readout_transfer",
            "shortcut": "transfer bare-action silence into clock/WEP/R10/local readout",
            "status": "ENFORCED",
            "reason": "radiative/readout closure is unsigned critical",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1319_0_construction_attempt",
            "decision": "minimal parent object-language signature construction attempted",
            "because": "1055/1065/1066 provide a coherent contract candidate and exact conditional grammar pieces",
            "next_action": "do not promote; record closure-only status and use finite source rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1319_1_no_parent_signature_claim",
            "decision": "parent signature is not derived from current corpus",
            "because": "every essential clause is contract-only, conditional-only, unsigned, or blocked by surviving counterexamples",
            "next_action": "demote theorem-zero route to closure-only until a deeper parent primitive is added",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1319_2_finite_source_route",
            "decision": "finite source/testing route remains the honest path",
            "because": "the derivation route did not close P0 alpha/source/readout debts",
            "next_action": "build a closure-only consequence ledger and finite-source priority map for first real fill targets",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1319_0_1320",
            "target_file": "1320-Y5-R10-RAB-closure-only-consequence-ledger-and-finite-source-priority-map.md",
            "target_script": "scripts/Y5_R10_RAB_closure_only_consequence_ledger_and_finite_source_priority_map.py",
            "task": "turn the 1319 closure-only demotion into a ranked finite-source work plan, choosing first-fill targets for alpha, clock, WEP, R10, and cross-arena rows without claiming theorem-zero",
            "success_condition": "each surviving finite row has ranked inputs, source/proof route, acceptance gate, and no theorem-zero shortcut; R10/clock/WEP are ordered by payoff and feasibility",
            "do_not": "do not re-open parent signature without a new primitive; do not fill coefficients by assumption; do not claim local-GR/R10/WEP",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    validation = []
    sources_ok = all(compact_bool(row["exists"]) and compact_bool(row["needle_found"]) for row in source_register)
    validation.append(
        validation_row(
            "VAL1319_0_sources_exist",
            "registered source paths exist and anchors are found",
            sources_ok,
            f"{sum(compact_bool(row['exists']) and compact_bool(row['needle_found']) for row in source_register)}/{len(source_register)} source anchors found",
        )
    )
    validation.append(
        validation_row(
            "VAL1319_1_signature_candidate_complete",
            "minimal signature candidate covers parent domain, coefficient domain, matter, source, measure, no-extension, and readout",
            len(signature_candidate) == 8
            and all(row["closure_status"] == "CLOSURE_ONLY" for row in signature_candidate),
            ";".join(row["candidate_id"] for row in signature_candidate),
        )
    )
    validation.append(
        validation_row(
            "VAL1319_2_construction_attempt_failed_cleanly",
            "construction attempt records exact failed derivation steps",
            len(clause_construction) == 6
            and all(str(row["result"]).startswith("FAILED_DERIVATION") for row in clause_construction),
            ";".join(row["step_id"] for row in clause_construction),
        )
    )
    validation.append(
        validation_row(
            "VAL1319_3_derivation_gaps_recorded",
            "all promotion-critical derivation gaps are recorded",
            len(derivation_gap) == 6,
            ";".join(row["gap_id"] for row in derivation_gap),
        )
    )
    validation.append(
        validation_row(
            "VAL1319_4_theorem_route_demoted",
            "theorem-zero route is demoted to closure-only for now",
            len(closure_demotion) == 4
            and all("CLOSURE" in row["status"] for row in closure_demotion),
            ";".join(row["demotion_id"] + ":" + row["status"] for row in closure_demotion),
        )
    )
    validation.append(
        validation_row(
            "VAL1319_5_finite_rows_survive",
            "finite source rows remain active after demotion",
            len(finite_source_map) == 5
            and all(row["priority"] in {"P0", "P1"} for row in finite_source_map),
            ";".join(row["survival_id"] for row in finite_source_map),
        )
    )
    validation.append(
        validation_row(
            "VAL1319_6_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            all(row["status"] == "ENFORCED" for row in anti_shortcut),
            ";".join(row["gate_id"] for row in anti_shortcut),
        )
    )
    csv_tables = [
        ("source", source_register),
        ("signature", signature_candidate),
        ("construction", clause_construction),
        ("gaps", derivation_gap),
        ("demotion", closure_demotion),
        ("finite", finite_source_map),
        ("anti", anti_shortcut),
        ("decisions", decisions),
        ("next", next_target),
    ]
    validation.append(
        validation_row(
            "VAL1319_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([rows for _, rows in csv_tables]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validation.append(
        validation_row(
            "VAL1319_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not generated_inside_formalization(),
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        )
    )
    validation.append(
        validation_row(
            "VAL1319_9_next_target_1320",
            "next target routes to closure-only consequence/source priority map",
            next_target[0]["target_file"].startswith("1320-Y5-R10-RAB-closure-only"),
            str(next_target[0]["target_file"]),
        )
    )
    validation.append(
        validation_row(
            "VAL1319_10_overall",
            "overall 1319 validation",
            all(row["status"] == "PASS" for row in validation),
            "1319 attempts minimal parent object-language construction, demotes theorem-zero route to closure-only, and keeps finite source rows active",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(SIGNATURE_CANDIDATE_PATH, signature_candidate)
    write_csv(CLAUSE_CONSTRUCTION_PATH, clause_construction)
    write_csv(DERIVATION_GAP_PATH, derivation_gap)
    write_csv(CLOSURE_DEMOTION_PATH, closure_demotion)
    write_csv(FINITE_SOURCE_MAP_PATH, finite_source_map)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(DECISION_PATH, decisions)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# 1319: RAB Minimal Parent Object-Language Signature Construction Or Closure

**Current verdict:** 1319 attempts the minimal parent object-language construction and does not derive it. The corpus contains a coherent and useful parent contract candidate, but it is not yet forced by deeper MTS primitives.

**Main progress:** the theorem-zero route is now explicitly demoted to closure-only rather than left in limbo. The exact gaps are named: parent quotient/domain derivation, visible operator-domain classification, hidden invariant elimination, source-scalar exclusion, action-scale/measure ownership, and radiative/readout closure.

**Decision:** stop trying to cash the parent signature as proof until a new primitive appears. The finite source/testing rows survive and should be ranked next for real fill targets.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Minimal Signature Candidate
{markdown_table(signature_candidate, ["candidate_id", "signature_clause", "minimal_form", "best_evidence", "construction_status", "why_not_signed", "if_signed_effect", "closure_status", "valid_for_claim", "claim_allowed"])}

## Clause Construction Attempt
{markdown_table(clause_construction, ["step_id", "attempt", "input_clauses", "construction_test", "result", "consequence", "valid_for_claim", "claim_allowed"])}

## Derivation Gap Ledger
{markdown_table(derivation_gap, ["gap_id", "missing_derivation", "blocks", "current_best", "required_to_promote", "valid_for_claim", "claim_allowed"])}

## Theorem Route Closure Demotion
{markdown_table(closure_demotion, ["demotion_id", "route", "status", "because", "consequence", "reopen_condition", "valid_for_claim", "claim_allowed"])}

## Finite Source Row Survival Map
{markdown_table(finite_source_map, ["survival_id", "source_row", "survives_because", "needed_next_input", "priority", "valid_for_claim", "claim_allowed"])}

## Anti-Shortcut Gates
{markdown_table(anti_shortcut, ["gate_id", "shortcut", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()

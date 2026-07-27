from __future__ import annotations

import math
from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2159-Y5-R2FR-parent-ordinary-matter-signature-or-first-coupling-bound-row.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOCS = {
    "2158": ROOT / "2158-Y5-R2FR-JX-qbarXT-source-zero-or-bounded-coupling-component-pack.md",
    "2158_validation": OUT / "P8_Y5_BRR545_2158_VALIDATION.csv",
    "2158_next": OUT / "P8_Y5_PARENT_QLOC_2158_NEXT_TARGET.csv",
    "1089": ROOT / "1089-Y5-R10-parent-ordinary-matter-signature-source-hunt-or-DD-intake-review.md",
    "1090": ROOT / "1090-Y5-R10-MOMS-parent-action-synthesis-or-explicit-missing-axiom-ledger.md",
    "1090_validation": OUT / "P8_Y5_BRR545_1090_VALIDATION.csv",
    "1851": ROOT / "1851-Y5-R2FR-first-real-local-coupling-bound-source-table.md",
    "1851_validation": OUT / "P8_Y5_BRR545_1851_VALIDATION.csv",
    "1852": ROOT / "1852-Y5-R2FR-PPN-common-frame-cg-translation-gate.md",
    "1852_validation": OUT / "P8_Y5_BRR545_1852_VALIDATION.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2159_SOURCE_REGISTER.csv",
    "moms_signature_attempt": OUT / "P8_Y5_PARENT_QLOC_2159_MOMS_SIGNATURE_ATTEMPT.csv",
    "missing_axiom_reduction": OUT / "P8_Y5_PARENT_QLOC_2159_MISSING_AXIOM_REDUCTION.csv",
    "first_bound_source": OUT / "P8_Y5_PARENT_QLOC_2159_FIRST_COUPLING_BOUND_SOURCE_ROW.csv",
    "cg_translation_gate": OUT / "P8_Y5_PARENT_QLOC_2159_CG_PPN_TRANSLATION_GATE.csv",
    "component_bound_status": OUT / "P8_Y5_PARENT_QLOC_2159_COMPONENT_BOUND_STATUS.csv",
    "local_claim_gate": OUT / "P8_Y5_PARENT_QLOC_2159_LOCAL_CLAIM_GATE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2159_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2159_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2159_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2159_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2159_VALIDATION.csv",
}


CASSINI_DELTA_GAMMA_BOUND = 6.7e-5
CASSINI_ALPHA_PROXY = math.sqrt(CASSINI_DELTA_GAMMA_BOUND / (2.0 - CASSINI_DELTA_GAMMA_BOUND))


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def has_any(text: str, alternatives: list[str]) -> bool:
    return any(item in text for item in alternatives)


def find_line(path: Path, alternatives: list[str]) -> tuple[int, str]:
    text = read_text(path) if path.exists() else ""
    for line_number, line in enumerate(text.splitlines(), start=1):
        if has_any(line, alternatives):
            return line_number, line.strip()
    return 0, "MISSING_NEEDLE"


def formalization_has_2159_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2159-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2159*",
        "*P8_Y5_BRR545_2159*",
        "*Y5_R2FR_parent_ordinary_matter_signature_or_first_coupling_bound_row_2159*",
        "*AFRAME_MOMS_CG_2159*",
        "*JR2159*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2159_00_2158_handoff", DOCS["2158"], [["NEXT2158_0_2159"], ["SZI2158_4_verdict"], ["BCP2158_10_total"]], "current 2158 selects parent ordinary-matter signature or first coupling bound row."),
        ("SRC2159_01_2158_next", DOCS["2158_next"], [["NEXT2158_0_2159"], ["ordinary-matter"], ["coupling component"]], "machine-readable 2159 target."),
        ("SRC2159_02_2158_validation", DOCS["2158_validation"], [["VAL2158_OVERALL"], ["PASS"]], "2158 validation passed as nonclaim."),
        ("SRC2159_03_1089_hunt", DOCS["1089"], [["HUNT1089_8_verdict"], ["NO_PARENT_SIGNATURE_SOURCE_FOUND"], ["NEXT1089_0_1090"]], "1089 source hunt found contracts but no parent-signed MOMS source."),
        ("SRC2159_04_1090_synthesis", DOCS["1090"], [["SYN1090_8_verdict"], ["SYNTHESIS_FAILS_MISSING_AXIOMS"], ["AX1090_0_parent_object"]], "1090 synthesis fails without explicit missing axioms."),
        ("SRC2159_05_1090_validation", DOCS["1090_validation"], [["V1090_SUMMARY"], ["pass"]], "1090 validation passed as nonclaim."),
        ("SRC2159_06_1851_sources", DOCS["1851"], [["OBS1851_2_PPN_CASSINI_2003"], ["TRG1851_0_cg_to_PPN"], ["VAL1851_OVERALL"]], "1851 records real local observable anchors and identifies c_g-to-PPN translation as clean first gate."),
        ("SRC2159_07_1851_validation", DOCS["1851_validation"], [["VAL1851_OVERALL"], ["PASS"]], "1851 validation passed as nonclaim."),
        ("SRC2159_08_1852_cg_gate", DOCS["1852"], [["PPN1852_1_scalar_tensor_alpha0_proxy"], ["CGB1852_1_cg_conditional"], ["VAL1852_OVERALL"]], "1852 computes Cassini scalar-tensor proxy and blocks direct MTS c_g bound."),
        ("SRC2159_09_1852_validation", DOCS["1852_validation"], [["VAL1852_OVERALL"], ["PASS"]], "1852 validation passed as nonclaim."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, needles_found=needles_found, expected_needles="; ".join(" OR ".join(group) for group in needle_groups), role=role))
    return rows


def moms_signature_attempt_rows() -> list[dict[str, object]]:
    data = [
        ("MOM2159_0_action_object", "one parent ordinary-matter action object exists before readout/projection/fitting", "S_parent=S_geom[Phi]+sum_A S_A[Psi_A,E(q(Phi)),Omega(E(q(Phi))),A_obs(q(Phi)),theta_A]+S_boundary", "SCHEMA_AVAILABLE_NOT_DERIVED", "parent action object from MTS primitives, not a consistency contract"),
        ("MOM2159_1_quotient_pullback", "observed coframe/gauge data descend through q", "Dq[v_X]=0 implies Lie_v e_obs=Lie_v g_obs=0 by chain rule", "EXACT_CONDITIONAL_LEMMA_NOT_PARENT_SIGNED", "parent-owned q and observed functor for the same v_X/Xhat"),
        ("MOM2159_2_matter_bundle_lift", "ordinary matter bundle and vertical lift are parent-selected", "delta_v Psi_A is zero, gauge, EOM, local-Lorentz, diffeo or boundary-only", "MATTER_CATEGORY_NOT_CONSTRUCTED", "species-complete matter functor and boundary class"),
        ("MOM2159_3_constant_sector", "masses, charges, alpha_EM, clocks and representation labels are fixed or topological", "Lie_v theta_A=0 for all ordinary matter constants", "SUPERSELECTION_NOT_DERIVED", "operator-domain/no-hidden-visible-hom theorem or explicit residual fields"),
        ("MOM2159_4_no_species_weights", "no w_A(X)S_A or kappa_A(X) source multiplier exists", "single action measure/current owner forbids relative source weights", "MEASURE_CURRENT_OWNER_UNSIGNED", "common hbar/action measure and source-label forgetting theorem"),
        ("MOM2159_5_no_shadow_readout", "no shadow conformal/disformal frame, domain marker or post-readout selector survives", "ordinary matter has no hidden-visible coefficient hom except q-observables or fixed representation data", "OPERATOR_DOMAIN_NOT_DERIVED", "no-hidden-visible-hom theorem and variation-before-readout owner"),
        ("MOM2159_6_zero_if_signed", "if MOM2159_0 through MOM2159_5 pass, J_X=qbar_XT=0", "delta_v S_matter=0 up to gauge/boundary terms; source current and test charge vanish", "EXACT_CONDITIONAL_THEOREM", "all premises signed by one parent branch"),
        ("MOM2159_7_verdict", "MOMS-style parent ordinary-matter signature closes in active branch", "one parent action signs action object, quotient functor, matter lift, constants, measure, no-shadow and readout order", "FAIL_CURRENT_CLAIM", "same five missing beams as 1090 remain unsigned"),
    ]
    return [row(clause_id=clause_id, clause=clause, statement=statement, current_status=current_status, missing_for_claim=missing_for_claim) for clause_id, clause, statement, current_status, missing_for_claim in data]


def missing_axiom_reduction_rows() -> list[dict[str, object]]:
    data = [
        ("AXR2159_0_parent_object", "one parent action object", "all MOMS clauses need one action owner", "MISSING_NOT_ADOPTED", "derive parent ordinary-matter action from primitive MTS object language"),
        ("AXR2159_1_no_hidden_visible_hom", "no hidden-visible coefficient homomorphism", "kills alpha_EM(X), m_A(X), shadow frames, material markers and source-only coefficient maps", "BEST_NEXT_DERIVATION_TARGET", "operator-domain theorem from parent category and quotient"),
        ("AXR2159_2_common_measure", "common hbar/action measure/current normalization", "forbids species-dependent action weights that survive classical covariance", "MISSING_NOT_ADOPTED", "derive measure/current owner or retain delta_kappa_A rows"),
        ("AXR2159_3_fixed_constants", "fixed ordinary constant sector", "removes mass, charge, clock and alpha_EM source currents", "REDUCES_TO_NO_HIDDEN_VISIBLE_HOM_IF_SIGNED", "derive representation/topological constant ownership"),
        ("AXR2159_4_variation_order", "variation-before-readout tied to same parent action", "prevents post-variation selectors from manufacturing or hiding source current", "MISSING_NOT_ADOPTED", "derive current/readout owner or retain C_readout row"),
        ("AXR2159_5_verdict", "smallest next derivation beam", "AXR2159_1 no-hidden-visible-hom attacks constants, shadow frames, markers, source weights and readout leakage at once", "SELECT_OPERATOR_DOMAIN_OR_CG_TRANSLATION_NEXT", "derive theorem first; fallback to c_g PPN translation if proof fails"),
    ]
    return [row(axiom_id=axiom_id, object=object_name, why_needed=why_needed, current_status=current_status, repair_path=repair_path) for axiom_id, object_name, why_needed, current_status, repair_path in data]


def first_bound_source_rows() -> list[dict[str, object]]:
    data = [
        (
            "FBS2159_0_Cassini_gamma",
            "PPN",
            "gamma_minus_1",
            2.1e-5,
            2.3e-5,
            CASSINI_DELTA_GAMMA_BOUND,
            "|central| + 2*sigma from Cassini 2003 as carried by 1851/1852",
            "dimensionless",
            "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            True,
            False,
        ),
        (
            "FBS2159_1_scalar_tensor_alpha_proxy",
            "PPN",
            "alpha_PPN_proxy",
            "",
            "",
            CASSINI_ALPHA_PROXY,
            "sqrt(delta_gamma/(2-delta_gamma)) for unscreened massless single-scalar tensor proxy",
            "dimensionless",
            "1852-Y5-R2FR-PPN-common-frame-cg-translation-gate.md",
            True,
            False,
        ),
        (
            "FBS2159_2_cg_conditional_row",
            "PPN",
            "c_g",
            "",
            "",
            "MISSING_NX_TAU_PPN",
            "|c_g| <= alpha_PPN_proxy/|N_X tau_PPN| if MTS reduces to the scalar-tensor common-frame limit",
            "dimensionless_per_normalized_Xhat",
            str(DOCS["1852"]),
            True,
            False,
        ),
        (
            "FBS2159_3_current_verdict",
            "PPN",
            "first active-branch coupling bound row",
            "",
            "",
            "SOURCE_BACKED_PROXY_DIRECT_MTS_BOUND_MISSING",
            "Cassini source/proxy is real; MTS c_g bound is not direct until N_X, tau_PPN, range/screening and contamination gates close",
            "gate",
            str(DOCS["1852"]),
            True,
            False,
        ),
    ]
    return [
        row(
            bound_id=bound_id,
            arena=arena,
            observable_or_component=observable_or_component,
            central_value=central_value,
            one_sigma=one_sigma,
            conservative_or_proxy_bound=conservative_or_proxy_bound,
            bound_rule=bound_rule,
            units=units,
            source=source,
            source_backed_observable=source_backed_observable,
            direct_mts_component_bound=direct_mts_component_bound,
        )
        for bound_id, arena, observable_or_component, central_value, one_sigma, conservative_or_proxy_bound, bound_rule, units, source, source_backed_observable, direct_mts_component_bound in data
    ]


def cg_translation_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CGT2159_0_universal_common_frame", "all ordinary matter sees A_g(Xhat)^2 g_E with one c_g", "map c_g into PPN gamma", "NOT_PARENT_SIGNED", "species/frame/readout terms can split PPN and WEP"),
        ("CGT2159_1_canonical_normalization", "Xhat normalization maps to canonical scalar varphi/M_Pl", "alpha_PPN=N_X c_g", "MISSING_NX_FROM_PARENT_HESSIAN", "field rescaling can fake any c_g bound"),
        ("CGT2159_2_range_transfer", "X mode is long-range on solar-system Cassini scales or transfer S_PPN(lambda) is known", "apply Cassini gamma bound to MTS c_g", "MISSING_LAMBDA_OR_SCREENING_TRANSFER", "finite-range/screened branch may evade or move to R10"),
        ("CGT2159_3_contamination_vector", "b_dis, q_nonH, support, boundary and readout components are zero or included in PPN vector", "isolate c_g or score absolute PPN residual vector", "MISSING_PPN_RESIDUAL_VECTOR", "single-parameter c_g bound would be fake"),
        ("CGT2159_4_verdict", "Cassini proxy becomes direct MTS c_g bound", "|N_X tau_PPN c_g| <= 0.0057880154", "FAIL_CURRENT_CLAIM_TRANSLATION_MISSING", "derive N_X, tau_PPN, range/screening and contamination map"),
    ]
    return [row(gate_id=gate_id, assumption=assumption, needed_for=needed_for, current_status=current_status, failure_if_missing=failure_if_missing) for gate_id, assumption, needed_for, current_status, failure_if_missing in data]


def component_bound_status_rows() -> list[dict[str, object]]:
    data = [
        ("CBS2159_0_cg", "c_g", "FBS2159_0_Cassini_gamma;FBS2159_1_scalar_tensor_alpha_proxy", "MISSING_NX_TAU_PPN_RANGE_VECTOR", "SOURCE_BACKED_PROXY_TRANSLATION_MISSING", False),
        ("CBS2159_1_bdis", "b_dis", "PPN/clock anchors in 1851", "MISSING_DISFORMAL_PROJECTION", "OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING", False),
        ("CBS2159_2_bA", "b_A", "MICROSCOPE/LLR anchors in 1851", "MISSING_MATERIAL_SENSITIVITY_MAP", "OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING", False),
        ("CBS2159_3_balpha", "b_alpha", "Rosenband clock anchor in 1851", "MISSING_X_PROFILE_OR_TIME_PROJECTION", "OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING", False),
        ("CBS2159_4_delta_kappa_A", "delta_kappa_A", "MICROSCOPE/LLR anchors in 1851", "MISSING_SOURCE_COMPOSITION_MAP", "OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING", False),
        ("CBS2159_5_qnonH_support_boundary", "q_nonH;Delta_W_support;q_boundary;C_readout", "LLR/orbital anchors in 1851", "MISSING_ORBITAL_SOURCE_SUPPORT_MAP", "OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING", False),
        ("CBS2159_6_total", "J_X_bound_abs;qbar_XT_bound_abs", "2158 component envelope plus 1851 observable anchors", "MISSING_ALL_TRANSLATION_GATES", "SOURCE_TABLE_READY_COMPONENT_CLAIM_BLOCKED", False),
    ]
    return [row(component_id=component_id, symbol=symbol, source_backed_observable_anchors=source_backed_observable_anchors, component_numeric_bound=component_numeric_bound, best_current_status=best_current_status, component_bound_claim=component_bound_claim) for component_id, symbol, source_backed_observable_anchors, component_numeric_bound, best_current_status, component_bound_claim in data]


def local_claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("LCG2159_0_MOMS_signature", "MOMS-style ordinary-matter signature derived", False, "MOM2159_7_verdict=FAIL_CURRENT_CLAIM"),
        ("LCG2159_1_source_zero", "J_X=qbar_XT=0 active theorem", False, "source-zero theorem remains conditional on unsigned MOMS clauses"),
        ("LCG2159_2_first_bound_source", "first real observable/proxy bound source staged", True, "Cassini gamma and scalar-tensor alpha proxy are numeric/source-backed but nonclaim"),
        ("LCG2159_3_direct_cg_bound", "MTS c_g has direct numeric bound", False, "N_X/tau_PPN/range/vector translation missing"),
        ("LCG2159_4_component_vector", "all live coupling components have theorem-zero or numeric bounds", False, "component translation gates remain missing"),
        ("LCG2159_5_local_GR_Newton", "local GR/Newton source side recovered", False, "neither source-zero nor bounded residual vector closes"),
    ]
    return [row(gate_id=gate_id, claim=claim, gate_pass=gate_pass, reason=reason) for gate_id, claim, gate_pass, reason in data]


def refusal_rows() -> list[dict[str, object]]:
    data = [
        ("REF2159_0_MOMS_derived", "MOMS ordinary-matter signature is derived", "SYNTHESIS_FAILS_MISSING_AXIOMS", "BLOCKED", "MOM2159_0 through MOM2159_5 do not close from one parent branch", False),
        ("REF2159_1_JX_qbar_zero", "J_X=qbar_XT=0", "CONDITIONAL_ZERO_THEOREM_ONLY", "BLOCKED", "MOMS signature remains unsigned", False),
        ("REF2159_2_cg_direct_bound", "Cassini gives direct MTS c_g bound", "SOURCE_BACKED_PROXY_TRANSLATION_MISSING", "BLOCKED", "N_X, tau_PPN, range/screening and PPN residual vector missing", False),
        ("REF2159_3_local_GR", "local GR/Newton recovered", "SOURCE_ZERO_AND_COMPONENT_VECTOR_OPEN", "BLOCKED", "source-zero and bounded-coupling routes both incomplete", False),
        ("REF2159_4_empirical_pass", "R10/WEP/PPN/clock/orbital pass", "TRANSLATION_GATES_MISSING", "BLOCKED", "observable anchors exist but no MTS component vector is score-ready", False),
    ]
    return [row(refusal_id=refusal_id, attempted_claim=attempted_claim, input_status=input_status, runner_result=runner_result, blocked_by=blocked_by, score_eligible=score_eligible) for refusal_id, attempted_claim, input_status, runner_result, blocked_by, score_eligible in data]


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2159_0_signature_result", "Do not claim the parent ordinary-matter signature.", "The active synthesis inherits 1090's exact failure: the same missing parent object, no-hidden-visible-hom, common measure, constants and readout-order beams remain unsigned.", "attack the smallest beam or keep source components explicit"),
        ("DEC2159_1_first_bound_result", "The first coupling-bound row exists only as a source-backed proxy.", "Cassini gives a clean scalar-tensor alpha proxy, but direct MTS c_g still lacks normalization, range and vector projection.", "derive the c_g translation gate before using the number"),
        ("DEC2159_2_best_derivation_route", "Best derivation route is still no-hidden-visible-hom/operator-domain.", "That one theorem would hit constants, shadow frames, marker leakage and direct alpha/mass vertices together.", "keep as parallel derivation target"),
        ("DEC2159_3_best_empirical_route", "Best empirical route is active-branch PPN c_g translation.", "The source anchor is already in hand and the missing assumptions are precise.", "2160-Y5-R2FR-PPN-common-frame-cg-translation-and-normalization-gate.md"),
    ]
    return [row(decision_id=decision_id, decision=decision, because=because, next_action=next_action) for decision_id, decision, because, next_action in data]


def next_target_rows() -> list[dict[str, object]]:
    data = [
        (
            "NEXT2159_0_2160",
            "2160-Y5-R2FR-PPN-common-frame-cg-translation-and-normalization-gate.md",
            "scripts/Y5_R2FR_PPN_common_frame_cg_translation_and_normalization_gate_2160.py",
            "derive or reject the active-branch map from MTS common-frame c_g into PPN gamma, including N_X, tau_PPN, lambda/range/screening and residual-vector contamination gates",
            "selected",
            "c_g obtains a conditional normalized PPN bound with all assumptions explicit, or the PPN route is demoted to source-only proxy and the no-hidden-visible-hom theorem becomes primary",
        ),
        (
            "NEXT2159_1_parallel",
            "2160b-Y5-R2FR-no-hidden-visible-hom-operator-domain-theorem.md",
            "scripts/Y5_R2FR_no_hidden_visible_hom_operator_domain_theorem_2160b.py",
            "try to derive the operator-domain theorem that forbids alpha_EM(X), m_A(X), shadow frames, material markers and source-only coefficient maps",
            "held",
            "operator-domain theorem closes enough MOMS clauses to reopen J_X=qbar_XT source-zero",
        ),
    ]
    return [row(route_id=route_id, next_target=next_target, script=script, objective=objective, selection_status=selection_status, success_condition=success_condition) for route_id, next_target, script, objective, selection_status, success_condition in data]


def write_branch_copies(signature: list[dict[str, object]], bound: list[dict[str, object]], cg_gate: list[dict[str, object]], next_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        ("COPY2159_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_MOMS_CG_2159_NONCLAIM.csv", signature + cg_gate),
        ("COPY2159_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2159_FIRST_BOUND_NONCLAIM.csv", bound + cg_gate),
        ("COPY2159_2_acquisition_queue", QUEUE / "JR2159_PPN_CG_TRANSLATION_OR_OPERATOR_DOMAIN_QUEUE.csv", next_rows + cg_gate),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    signature: list[dict[str, object]],
    axioms: list[dict[str, object]],
    bound: list[dict[str, object]],
    cg_gate: list[dict[str, object]],
    components: list[dict[str, object]],
    local_gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    signature_ok = any(item["clause_id"] == "MOM2159_7_verdict" and item["current_status"] == "FAIL_CURRENT_CLAIM" for item in signature)
    axioms_ok = any(item["axiom_id"] == "AXR2159_5_verdict" and "OPERATOR_DOMAIN" in str(item["current_status"]) for item in axioms)
    bound_proxy_ok = any(item["bound_id"] == "FBS2159_1_scalar_tensor_alpha_proxy" and float(item["conservative_or_proxy_bound"]) > 0 for item in bound)
    bound_nonclaim_ok = all(not truthy(item.get("direct_mts_component_bound", False)) and not truthy(item.get("valid_for_claim", False)) for item in bound)
    cg_gate_ok = any(item["gate_id"] == "CGT2159_4_verdict" and item["current_status"] == "FAIL_CURRENT_CLAIM_TRANSLATION_MISSING" for item in cg_gate)
    components_ok = any(item["component_id"] == "CBS2159_6_total" and item["component_numeric_bound"] == "MISSING_ALL_TRANSLATION_GATES" for item in components)
    local_ok = any(item["gate_id"] == "LCG2159_2_first_bound_source" and truthy(item["gate_pass"]) for item in local_gates) and all(not truthy(item.get("claim_allowed", False)) for item in local_gates)
    refusal_ok = all(item["runner_result"] == "BLOCKED" and not truthy(item.get("score_eligible", False)) for item in refusals)
    decisions_ok = any(item["decision_id"] == "DEC2159_3_best_empirical_route" and "2160" in str(item["next_action"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2159_0_2160" and item["selection_status"] == "selected" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    missing_not_ready = all(not truthy(item.get("valid_for_claim", False)) for group in (signature, axioms, bound, cg_gate, components) for item in group if "MISSING_" in " ".join(str(value) for value in item.values()))
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, signature, axioms, bound, cg_gate, components, local_gates, refusals, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2159_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, signature_ok, axioms_ok, bound_proxy_ok, bound_nonclaim_ok, cg_gate_ok, components_ok, local_ok, refusal_ok, decisions_ok, next_ok, copies_ok, csv_ok, missing_not_ready, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2159_00_sources", sources_ok, "2158 handoff plus 1089/1090 and 1851/1852 precedents validate"),
        ("VAL2159_01_signature_blocks", signature_ok, "MOMS-style signature remains unsigned"),
        ("VAL2159_02_axiom_reduction", axioms_ok, "missing axiom reduction selects operator-domain/c_g routes"),
        ("VAL2159_03_bound_proxy_numeric", bound_proxy_ok, "Cassini scalar-tensor proxy is positive numeric"),
        ("VAL2159_04_bound_nonclaim", bound_nonclaim_ok, "first coupling-bound row is source-backed proxy only, not direct MTS claim"),
        ("VAL2159_05_cg_translation_blocks", cg_gate_ok, "c_g direct bound remains translation-missing"),
        ("VAL2159_06_component_status", components_ok, "total component vector remains missing all translation gates"),
        ("VAL2159_07_local_claim_gate", local_ok, "real source/proxy gate exists but no local claims allowed"),
        ("VAL2159_08_refusals", refusal_ok, "refusal runner blocks MOMS, zero, direct c_g, local-GR and empirical claims"),
        ("VAL2159_09_decision_next", decisions_ok, "decision ledger selects active PPN c_g translation gate"),
        ("VAL2159_10_next", next_ok, "2160 next target selected"),
        ("VAL2159_11_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2159_12_csv_parse", csv_ok, "all generated 2159 CSVs parse cleanly"),
        ("VAL2159_13_missing_not_ready", missing_not_ready, "MISSING_* rows stay nonclaim"),
        ("VAL2159_14_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2159_15_formalization_clean", formalization_clean, "formalization-workbench untouched by 2159"),
        ("VAL2159_16_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2159_OVERALL", all_ok, "2159 keeps MOMS unsigned and stages first c_g/Cassini coupling-bound proxy."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    signature: list[dict[str, object]],
    axioms: list[dict[str, object]],
    bound: list[dict[str, object]],
    cg_gate: list[dict[str, object]],
    components: list[dict[str, object]],
    local_gates: list[dict[str, object]],
    refusals: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    line_2158, _ = find_line(DOCS["2158"], ["NEXT2158_0_2159"])
    line_1090, _ = find_line(DOCS["1090"], ["SYN1090_8_verdict"])
    line_1852, _ = find_line(DOCS["1852"], ["CGB1852_1_cg_conditional"])
    content = "\n\n".join(
        [
            "# 2159 - Y5/R2FR Parent Ordinary-Matter Signature Or First Coupling Bound Row",
            "## Current Verdict",
            "2159 does **not** prove the MOMS-style ordinary-matter parent signature, `J_X=qbar_XT=0`, a direct `c_g` bound, local GR/Newton, or any public claim.",
            "It does make the fallback more concrete: the active branch now carries the first source-backed coupling-bound proxy, the Cassini PPN scalar-tensor `alpha_PPN` proxy, while explicitly refusing to call it an MTS `c_g` bound until `N_X`, `tau_PPN`, range/screening and residual-vector gates close.",
            "The derivation side is also narrowed: the smallest load-bearing theorem is still the no-hidden-visible-hom/operator-domain rule, because it would hit constant superselection, shadow frames, material markers, direct alpha/mass vertices, source weights and readout leakage together.",
            f"This follows the 2158 handoff at line {line_2158}, the 1090 MOMS synthesis failure at line {line_1090}, and the 1852 conditional `c_g` row at line {line_1852}.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## MOMS Signature Attempt",
            md_table(signature, ["clause_id", "clause", "statement", "current_status", "missing_for_claim", "valid_for_claim"]),
            "## Missing Axiom Reduction",
            md_table(axioms, ["axiom_id", "object", "why_needed", "current_status", "repair_path", "valid_for_claim"]),
            "## First Coupling Bound Source Row",
            md_table(bound, ["bound_id", "arena", "observable_or_component", "central_value", "one_sigma", "conservative_or_proxy_bound", "bound_rule", "units", "source", "source_backed_observable", "direct_mts_component_bound", "valid_for_claim"]),
            "## c_g PPN Translation Gate",
            md_table(cg_gate, ["gate_id", "assumption", "needed_for", "current_status", "failure_if_missing", "valid_for_claim"]),
            "## Component Bound Status",
            md_table(components, ["component_id", "symbol", "source_backed_observable_anchors", "component_numeric_bound", "best_current_status", "component_bound_claim", "valid_for_claim"]),
            "## Local Claim Gate",
            md_table(local_gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Refusal Runner",
            md_table(refusals, ["refusal_id", "attempted_claim", "input_status", "runner_result", "blocked_by", "score_eligible", "claim_allowed", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "selection_status", "success_condition", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
            "## Working Interpretation",
            "This is a good active-branch tightening. The source-zero derivation route remains alive but unpaid. The fallback is no longer empty: Cassini puts real pressure on any long-range unscreened common-frame branch. The next move is to decide whether MTS actually maps into that PPN proxy or whether the proxy stays external pressure only.",
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    signature = moms_signature_attempt_rows()
    axioms = missing_axiom_reduction_rows()
    bound = first_bound_source_rows()
    cg_gate = cg_translation_gate_rows()
    components = component_bound_status_rows()
    local_gates = local_claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["moms_signature_attempt"], signature)
    write_csv(OUTPUTS["missing_axiom_reduction"], axioms)
    write_csv(OUTPUTS["first_bound_source"], bound)
    write_csv(OUTPUTS["cg_translation_gate"], cg_gate)
    write_csv(OUTPUTS["component_bound_status"], components)
    write_csv(OUTPUTS["local_claim_gate"], local_gates)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    copies = write_branch_copies(signature, bound, cg_gate, next_rows)
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(sources, signature, axioms, bound, cg_gate, components, local_gates, refusals, decisions, next_rows, copies, csv_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, signature, axioms, bound, cg_gate, components, local_gates, refusals, decisions, next_rows, copies, validation)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"2159 validation {validation[-1]['status']}")


if __name__ == "__main__":
    main()

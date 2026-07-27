from __future__ import annotations

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


DOC = ROOT / "2168-Y5-R2FR-object-language-radial-cell-constraint-or-finite-ZRJR-intake.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOCS = {
    "2167": ROOT / "2167-Y5-R2FR-reciprocity-selector-operator-or-Hcore-source-equation.md",
    "2167_validation": OUT / "P8_Y5_BRR545_2167_VALIDATION.csv",
    "2167_next": OUT / "P8_Y5_PARENT_QLOC_2167_NEXT_TARGET.csv",
    "1868": ROOT / "1868-Y5-R2FR-typed-parent-grammar-for-radial-cell-or-coefficient-bound-branch.md",
    "1868_validation": OUT / "P8_Y5_BRR545_1868_VALIDATION.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2168_SOURCE_REGISTER.csv",
    "typed_grammar": OUT / "P8_Y5_PARENT_QLOC_2168_TYPED_PARENT_GRAMMAR_AUDIT.csv",
    "legality": OUT / "P8_Y5_PARENT_QLOC_2168_RAB_TERM_LEGALITY_MATRIX.csv",
    "conditional": OUT / "P8_Y5_PARENT_QLOC_2168_CONDITIONAL_GRAMMAR_THEOREM.csv",
    "coefficient_branch": OUT / "P8_Y5_PARENT_QLOC_2168_COEFFICIENT_BOUND_BRANCH_ROWS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2168_CLAIM_GATE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2168_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2168_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2168_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2168_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2168_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight": SOURCE_WEIGHT_DOCS / "AFRAME_TYPED_RADIAL_CELL_GRAMMAR_2168_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2168_FINITE_ZRJR_BRANCH_NONCLAIM.csv",
    "queue": QUEUE / "JR2168_FINITE_LOCAL_COEFFICIENT_BRANCH_QUEUE.csv",
}


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


def formalization_has_2168_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2168-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2168*",
        "*P8_Y5_BRR545_2168*",
        "*Y5_R2FR_object_language_radial_cell_constraint_or_finite_ZRJR_intake_2168*",
        "*AFRAME_TYPED_RADIAL_CELL_GRAMMAR_2168*",
        "*JR2168*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2168_00_2167_handoff", DOCS["2167"], [["NEXT2167_0_2168"], ["RSA2167_5_verdict"], ["VAL2167_OVERALL"]], "2167 selects object-language radial-cell proof or finite Z_R/J_R intake."),
        ("SRC2168_01_2167_validation", DOCS["2167_validation"], [["VAL2167_OVERALL"], ["PASS"]], "2167 validation passed as nonclaim."),
        ("SRC2168_02_2167_next_csv", DOCS["2167_next"], [["NEXT2167_0_2168"], ["compatibility"], ["finite"]], "machine-readable 2168 handoff."),
        ("SRC2168_03_1868_typed_grammar", DOCS["1868"], [["TGA1868_4_verdict"], ["CBB1868_0_ZR"], ["VAL1868_OVERALL"]], "prior typed-grammar attempt writes the exact conditional theorem and selects coefficient branch."),
        ("SRC2168_04_1868_validation", DOCS["1868_validation"], [["VAL1868_OVERALL"], ["PASS"]], "1868 validation passed as nonclaim."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, needles_found=needles_found, expected_needles="; ".join(" OR ".join(group) for group in needle_groups), role=role))
    return rows


def typed_grammar_rows() -> list[dict[str, object]]:
    data = [
        ("TPG2168_0_primitives", "parent primitive list", "T,S/coframe/transport primitives plus allowed compatibility constructors are declared before local reduction", "CONTRACT_WRITTEN_NOT_DERIVED", "missing parent category principle"),
        ("TPG2168_1_cell_object", "radial-cell compatibility object", "J_q=T sqrt(S), u=ln(J_q), C_R=R_AB=2u", "EXACT_DEFINITION", "target object is unambiguous but not zero"),
        ("TPG2168_2_no_independent_RAB", "category exclusion", "R_AB may appear only as compatibility data or constrained auxiliary target, not as an independent dynamical field", "MISSING_PARENT_CATEGORY_PRINCIPLE", "this would forbid generic Z_R/J_R if derived"),
        ("TPG2168_3_derivative_permissions", "operator permissions", "derivatives act on parent primitives/transport/matter, not R_AB as standalone scalar", "CONDITIONAL_FORBIDS_ZR", "type alone is too weak; coframe derivative countermodels survive"),
        ("TPG2168_4_auxiliary_constraint", "Lambda_R C_R route", "parent-owned Lambda_R imposes C_R=0 only if auxiliary origin, Dirac preservation, matter descent and boundary silence close", "CONDITIONAL_EXACT_ROUTE", "currently closure template only"),
        ("TPG2168_5_matter_boundary", "descent and boundary", "matter/boundary/readout cannot directly source or charge R_AB", "MISSING_MATTER_BOUNDARY_DESCENT", "J_R/Q_R cannot be zeroed yet"),
        ("TPG2168_6_verdict", "typed parent grammar", "typed grammar would give clean local reciprocity if signed, but current corpus has not derived it", "TYPED_PARENT_GRAMMAR_NOT_DERIVED_CURRENT_CORPUS", "switch to coefficient-bound branch unless new parent category principle appears"),
    ]
    return [row(grammar_id=grammar_id, grammar_layer=grammar_layer, candidate_rule=candidate_rule, status=status, failure_mode=failure_mode) for grammar_id, grammar_layer, candidate_rule, status, failure_mode in data]


def legality_rows() -> list[dict[str, object]]:
    data = [
        ("TLM2168_0_ZR_kinetic", "1/2 Z_R h^ij D_i R_AB D_j R_AB", "ILLEGAL_IF_CATEGORY_RULE_SIGNED", "LEGAL_COUNTERMODEL_IF_NOT_SIGNED", "dangerous fifth-force/hair term; type exclusion would kill it but general coframe locality can regenerate it"),
        ("TLM2168_1_MR2_potential", "1/2 M_R^2 R_AB^2", "ILLEGAL_OR_AUXILIARY_ONLY_IF_CATEGORY_RULE_SIGNED", "LEGAL_COUNTERMODEL_IF_NOT_SIGNED", "smooth potential makes C_R finite residual instead of exact constraint"),
        ("TLM2168_2_lambda_constraint", "Lambda_R C_R", "LEGAL_IF_PARENT_AUXILIARY_SIGNED", "CLOSURE_INSERTION_IF_NOT_SIGNED", "clean exact route only if Lambda_R is parent-owned and preserved"),
        ("TLM2168_3_direct_source", "J_R C_R", "ILLEGAL_IF_MATTER_DESCENT_SIGNED", "LEGAL_COUNTERMODEL_IF_NOT_SIGNED", "direct matter source shifts reciprocal mode"),
        ("TLM2168_4_boundary_charge", "B_R(C_R) or Q_R surface flux", "ILLEGAL_IF_BOUNDARY_NO_CHARGE_SIGNED", "LEGAL_COUNTERMODEL_IF_NOT_SIGNED", "boundary/corner terms revive reciprocal hair"),
        ("TLM2168_5_readout_reentry", "C_readout(C_R) or projection leakage", "ILLEGAL_IF_PURE_READOUT_SIGNED", "LEGAL_COUNTERMODEL_IF_NOT_SIGNED", "post-variation readout can reinsert local metric residuals"),
    ]
    return [row(term_id=term_id, term=term, status_if_grammar_signed=status_if_grammar_signed, status_current_corpus=status_current_corpus, interpretation=interpretation) for term_id, term, status_if_grammar_signed, status_current_corpus, interpretation in data]


def conditional_rows() -> list[dict[str, object]]:
    data = [
        ("CGT2168_0_hypotheses", "conditional typed-grammar local reciprocity theorem", "If R_AB is compatibility data only, Lambda_R C_R is parent-owned, matter/boundary/readout descend silently, and no derivative/source terms on R_AB are legal, then C_R=0 before readout.", "CONDITIONAL_THEOREM_ONLY", "MISSING_PARENT_CATEGORY_PRINCIPLE"),
        ("CGT2168_1_ZR", "gradient coefficient", "Under signed category rule, Z_R is absent rather than tuned small.", "CONDITIONAL_ZERO", "MISSING_DERIVATIVE_PERMISSION_PROOF"),
        ("CGT2168_2_JR", "direct matter source", "Under signed matter descent, J_R is absent because matter couples to parent coframe/readout rather than C_R.", "CONDITIONAL_ZERO", "MISSING_MATTER_DESCENT_PROOF"),
        ("CGT2168_3_QR", "reciprocal boundary charge", "Under signed boundary no-charge class, Q_R is absent or fixed to zero.", "CONDITIONAL_ZERO", "MISSING_BOUNDARY_NO_CHARGE_THEOREM"),
        ("CGT2168_4_local_GR", "local GR/Newton reduction", "C_R=0 plus source/charge silence is necessary for the MTS local branch to inherit reciprocal GR-style structure.", "LOCAL_GR_NOT_DERIVED", "MISSING_PARENT_GRAMMAR_AND_PPN_RESIDUAL_ZERO"),
    ]
    return [row(theorem_id=theorem_id, object=object_name, statement=statement, status=status, missing_input=missing_input) for theorem_id, object_name, statement, status, missing_input in data]


def coefficient_branch_rows() -> list[dict[str, object]]:
    data = [
        ("CBB2168_0_ZR", "Z_R", "gradient stiffness", "derive coefficient or bound from local fifth-force/PPN behavior", "MISSING_NUMERIC_PARENT_COEFFICIENT", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
        ("CBB2168_1_MR2", "M_R^2", "mass/stiffness scale", "derive ell_R=sqrt(Z_R/M_R^2) or bound scale separation", "MISSING_NUMERIC_PARENT_COEFFICIENT", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
        ("CBB2168_2_JR", "J_R", "direct matter source", "derive matter descent zero or bound source coupling", "MISSING_MATTER_SOURCE_COEFFICIENT", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
        ("CBB2168_3_BR", "B_R", "boundary/corner reciprocal source", "derive zero-flux class or bound collar/source flux", "MISSING_BOUNDARY_COEFFICIENT", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
        ("CBB2168_4_QR", "Q_R", "exterior reciprocal charge/hair", "derive no-charge theorem or finite exterior charge bound", "MISSING_BOUNDARY_INPUT", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
        ("CBB2168_5_SR", "S_R", "total local reciprocal source residual", "map finite residual components into D_R source side", "MISSING_SOURCE_MAP", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
        ("CBB2168_6_tau_R10", "tau_R10", "short-range projection", "map finite reciprocal branch to alpha(lambda)", "MISSING_ARENA_PROJECTION", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
        ("CBB2168_7_tau_PPN", "tau_PPN", "post-Newtonian projection", "map C_R residual to gamma/beta/light-time observables", "MISSING_ARENA_PROJECTION", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
    ]
    return [row(coefficient_id=coefficient_id, symbol=symbol, role=role, required_source=required_source, status=status, numeric_value=numeric_value, source_path=source_path) for coefficient_id, symbol, role, required_source, status, numeric_value, source_path in data]


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2168_0_typed_grammar", "typed parent grammar is derived", False, "parent category principle missing"),
        ("CG2168_1_ZR_JR_zero", "Z_R=0 and J_R=0 are theorem zeros", False, "derivative permission and matter descent not signed"),
        ("CG2168_2_QR_zero", "Q_R boundary/no-charge theorem closes", False, "boundary no-charge missing"),
        ("CG2168_3_local_GR", "MTS derives local GR/Newton branch", False, "typed grammar, no-charge, matter descent and residual gates open"),
        ("CG2168_4_finite_bounds", "finite coefficient branch passes local tests", False, "numeric coefficients and arena projections missing"),
    ]
    return [row(gate_id=gate_id, claim=claim, gate_pass=gate_pass, reason=reason) for gate_id, claim, gate_pass, reason in data]


def refusal_rows() -> list[dict[str, object]]:
    data = [
        ("REF2168_0_type_only", "claim type alone forbids Z_R", "COFRAME_DERIVATIVE_COUNTERMODEL", "BLOCKED", "need stronger category principle or quotient invariance", False),
        ("REF2168_1_lambda_axiom", "insert Lambda_R C_R and call it derived", "AUXILIARY_ORIGIN_UNSIGNED", "BLOCKED", "Dirac/matter/boundary chain missing", False),
        ("REF2168_2_unimodular_axiom", "impose J_q=1 as derivation", "CLOSURE_ONLY", "BLOCKED", "algebra works but parent origin missing", False),
        ("REF2168_3_finite_pass", "claim finite coefficient branch passes", "MISSING_VALUES_PROJECTIONS", "BLOCKED", "coefficient rows are placeholders", False),
        ("REF2168_4_local_gr", "claim local GR/Newton", "GRAMMAR_AND_RESIDUAL_GATES_OPEN", "BLOCKED", "conditional theorem only", False),
    ]
    return [row(refusal_id=refusal_id, attempted_claim=attempted_claim, input_status=input_status, runner_result=runner_result, blocked_by=blocked_by, score_eligible=score_eligible) for refusal_id, attempted_claim, input_status, runner_result, blocked_by, score_eligible in data]


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2168_0_result", "TYPED_PARENT_GRAMMAR_NOT_DERIVED_CURRENT_CORPUS", "type exclusion is coherent but type alone cannot forbid coframe derivative countermodels", "do not claim Z_R/J_R/Q_R theorem zeros"),
        ("DEC2168_1_conditional_win", "CONDITIONAL_GRAMMAR_THEOREM_READY", "if parent category principle, auxiliary constraint, matter descent and boundary silence are signed, C_R=0 follows cleanly", "future derivation has exact hypotheses"),
        ("DEC2168_2_practical_route", "COEFFICIENT_BOUND_BRANCH_SELECTED_NEXT", "without a new parent category principle, honest progress is to source or bound Z_R,M_R^2,J_R,Q_R and arena projections", "move to finite local coefficient branch"),
    ]
    return [row(decision_id=decision_id, decision=decision, because=because, next_action=next_action) for decision_id, decision, because, next_action in data]


def next_target_rows() -> list[dict[str, object]]:
    data = [
        ("NEXT2168_0_2169", "2169-Y5-R2FR-finite-local-coefficient-bound-branch-setup.md", "scripts/Y5_R2FR_finite_local_coefficient_bound_branch_setup_2169.py", "build the finite local coefficient branch for Z_R, M_R^2, J_R, B_R, Q_R, S_R and R10/PPN/clock/orbital projections without claiming a pass", "selected", "all finite local residual coefficients/projections are represented as sourced-or-missing rows with claim gates and runner-ready schema"),
        ("NEXT2168_1_theory_parallel", "2169b-Y5-R2FR-parent-category-principle-for-compatibility-objects.md", "scripts/Y5_R2FR_parent_category_principle_for_compatibility_objects_2169b.py", "attempt a deeper parent principle that makes compatibility objects non-dynamical rather than ordinary scalars", "held", "new parent category principle signs the grammar or fails explicitly"),
    ]
    return [row(route_id=route_id, next_target=next_target, script=script, objective=objective, selection_status=selection_status, success_condition=success_condition) for route_id, next_target, script, objective, selection_status, success_condition in data]


def write_branch_copies(typed_grammar, legality, coefficient_branch, next_rows) -> list[dict[str, object]]:
    copies = [
        ("COPY2168_0_source_weight_docs", BRANCH_COPIES["source_weight"], typed_grammar + legality),
        ("COPY2168_1_branch_locked_wep", BRANCH_COPIES["branch_wep"], coefficient_branch),
        ("COPY2168_2_acquisition_queue", BRANCH_COPIES["queue"], next_rows + coefficient_branch),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(sources, typed_grammar, legality, conditional, coefficient_branch, gates, refusals, decisions, next_rows, copies, csv_paths):
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    grammar_ok = any(item["grammar_id"] == "TPG2168_6_verdict" and item["status"] == "TYPED_PARENT_GRAMMAR_NOT_DERIVED_CURRENT_CORPUS" for item in typed_grammar)
    legality_ok = any(item["term_id"] == "TLM2168_0_ZR_kinetic" and item["status_current_corpus"] == "LEGAL_COUNTERMODEL_IF_NOT_SIGNED" for item in legality)
    conditional_ok = any(item["theorem_id"] == "CGT2168_0_hypotheses" and item["status"] == "CONDITIONAL_THEOREM_ONLY" for item in conditional)
    coeff_ok = len(coefficient_branch) == 8 and all(not truthy(item.get("valid_for_claim", False)) for item in coefficient_branch)
    gate_ok = all(not truthy(item["gate_pass"]) for item in gates) and all(not truthy(item.get("claim_allowed", False)) for item in gates)
    refusal_ok = all(item["runner_result"] == "BLOCKED" and not truthy(item.get("score_eligible", False)) for item in refusals)
    decisions_ok = any(item["decision_id"] == "DEC2168_2_practical_route" and "COEFFICIENT_BOUND_BRANCH_SELECTED_NEXT" in str(item["decision"]) for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2168_0_2169" and item["selection_status"] == "selected" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False)) for group in (sources, typed_grammar, legality, conditional, coefficient_branch, gates, refusals, decisions, next_rows, copies) for item in group)
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2168_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, grammar_ok, legality_ok, conditional_ok, coeff_ok, gate_ok, refusal_ok, decisions_ok, next_ok, copies_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2168_00_sources", sources_ok, "2167 and 1868 source paths and needles validate"),
        ("VAL2168_01_grammar", grammar_ok, "typed grammar remains not derived"),
        ("VAL2168_02_legality", legality_ok, "coframe derivative countermodel remains legal unless grammar is signed"),
        ("VAL2168_03_conditional", conditional_ok, "conditional grammar theorem is recorded only as conditional"),
        ("VAL2168_04_coefficient_branch", coeff_ok, "coefficient-bound rows are nonclaim placeholders"),
        ("VAL2168_05_claim_gates", gate_ok, "typed-grammar/local-test claim gates remain blocked"),
        ("VAL2168_06_refusals", refusal_ok, "refusal runner blocks type-only, lambda, unimodular, finite-pass and local-GR claims"),
        ("VAL2168_07_decision", decisions_ok, "decision ledger selects finite coefficient-bound branch"),
        ("VAL2168_08_next", next_ok, "2169 next target selected"),
        ("VAL2168_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2168_10_csv_parse", csv_ok, "all generated 2168 CSVs parse cleanly"),
        ("VAL2168_11_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2168_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2168"),
        ("VAL2168_13_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2168_OVERALL", all_ok, "2168 keeps the typed grammar theorem conditional and selects the finite local coefficient-bound branch."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(sources, typed_grammar, legality, conditional, coefficient_branch, gates, refusals, decisions, next_rows, copies, validation) -> None:
    line_2167, _ = find_line(DOCS["2167"], ["NEXT2167_0_2168"])
    line_1868, _ = find_line(DOCS["1868"], ["TGA1868_4_verdict"])
    content = "\n\n".join(
        [
            "# 2168 - Y5/R2FR Object-Language Radial-Cell Constraint Or Finite Z_R/J_R Intake",
            "## Current Verdict",
            "2168 does **not** derive the typed parent grammar, does **not** prove `Z_R=0`, `J_R=0`, or `Q_R=0`, and does **not** claim local GR/Newton.",
            "It does write the clean conditional theorem: if `C_R/R_AB` is compatibility data only, if `Lambda_R C_R` is parent-owned, and if matter, boundary and readout descend silently, then reciprocal hair is forbidden before local readout. But current MTS has not derived the parent category principle, and type alone is too weak because coframe derivative countermodels survive.",
            "Therefore the next honest branch is finite coefficient intake for `Z_R`, `M_R^2`, `J_R`, `B_R`, `Q_R`, `S_R`, and arena projections, while keeping the deeper category-principle derivation as a parallel theory route.",
            f"This follows the 2167 handoff at line {line_2167} and imports the 1868 typed-grammar verdict at line {line_1868}.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Typed Parent Grammar Audit",
            md_table(typed_grammar, ["grammar_id", "grammar_layer", "candidate_rule", "status", "failure_mode", "valid_for_claim"]),
            "## R_AB Term Legality Matrix",
            md_table(legality, ["term_id", "term", "status_if_grammar_signed", "status_current_corpus", "interpretation", "valid_for_claim"]),
            "## Conditional Grammar Theorem",
            md_table(conditional, ["theorem_id", "object", "statement", "status", "missing_input", "valid_for_claim"]),
            "## Coefficient-Bound Branch Rows",
            md_table(coefficient_branch, ["coefficient_id", "symbol", "role", "required_source", "status", "numeric_value", "source_path", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
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
            "This is the clean failure of the derivation-first route. The exact theorem exists, but the missing object is a genuine parent category principle: why compatibility objects are non-dynamical. Until that appears, the project must test the finite local coefficient branch honestly rather than smuggle in local GR by type language.",
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    typed_grammar = typed_grammar_rows()
    legality = legality_rows()
    conditional = conditional_rows()
    coefficient_branch = coefficient_branch_rows()
    gates = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["typed_grammar"], typed_grammar)
    write_csv(OUTPUTS["legality"], legality)
    write_csv(OUTPUTS["conditional"], conditional)
    write_csv(OUTPUTS["coefficient_branch"], coefficient_branch)
    write_csv(OUTPUTS["claim_gate"], gates)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    copies = write_branch_copies(typed_grammar, legality, coefficient_branch, next_rows)
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(sources, typed_grammar, legality, conditional, coefficient_branch, gates, refusals, decisions, next_rows, copies, csv_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, typed_grammar, legality, conditional, coefficient_branch, gates, refusals, decisions, next_rows, copies, validation)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"2168 validation {validation[-1]['status']}")


if __name__ == "__main__":
    main()

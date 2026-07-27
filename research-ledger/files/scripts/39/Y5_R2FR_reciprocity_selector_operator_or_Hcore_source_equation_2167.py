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


DOC = ROOT / "2167-Y5-R2FR-reciprocity-selector-operator-or-Hcore-source-equation.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOCS = {
    "2166": ROOT / "2166-Y5-R2FR-local-GR-reduction-contract-and-residual-vector-prioritizer.md",
    "2166_validation": OUT / "P8_Y5_BRR545_2166_VALIDATION.csv",
    "2166_next": OUT / "P8_Y5_PARENT_QLOC_2166_NEXT_TARGET.csv",
    "1866": ROOT / "1866-Y5-R2FR-reciprocity-selector-operator-or-Hcore-source-equation.md",
    "1866_validation": OUT / "P8_Y5_BRR545_1866_VALIDATION.csv",
    "1867": ROOT / "1867-Y5-R2FR-object-language-radial-cell-constraint-or-finite-ZRJR-intake.md",
    "1867_validation": OUT / "P8_Y5_BRR545_1867_VALIDATION.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2167_SOURCE_REGISTER.csv",
    "selector_audit": OUT / "P8_Y5_PARENT_QLOC_2167_RECIPROCITY_SELECTOR_AUDIT.csv",
    "hcore": OUT / "P8_Y5_PARENT_QLOC_2167_HCORE_SOURCE_EQUATION_TEST.csv",
    "finite": OUT / "P8_Y5_PARENT_QLOC_2167_FINITE_ZRJR_REQUIREMENTS.csv",
    "no_smuggle": OUT / "P8_Y5_PARENT_QLOC_2167_NO_SMUGGLING_GUARDS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2167_CLAIM_GATE.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2167_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2167_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2167_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2167_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2167_VALIDATION.csv",
}

BRANCH_COPIES = {
    "source_weight": SOURCE_WEIGHT_DOCS / "AFRAME_RECIPROCITY_SELECTOR_2167_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2167_ZRJR_NONCLAIM.csv",
    "queue": QUEUE / "JR2167_TYPED_PARENT_GRAMMAR_OR_ZRJR_QUEUE.csv",
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


def formalization_has_2167_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2167-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2167*",
        "*P8_Y5_BRR545_2167*",
        "*Y5_R2FR_reciprocity_selector_operator_or_Hcore_source_equation_2167*",
        "*AFRAME_RECIPROCITY_SELECTOR_2167*",
        "*JR2167*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2167_00_2166_handoff", DOCS["2166"], [["NEXT2166_0_2167"], ["PR2166_0_reciprocity_selector"], ["VAL2166_OVERALL"]], "2166 selects reciprocity selector/H_core gate."),
        ("SRC2167_01_2166_validation", DOCS["2166_validation"], [["VAL2166_OVERALL"], ["PASS"]], "2166 validation passed as nonclaim."),
        ("SRC2167_02_2166_next_csv", DOCS["2166_next"], [["NEXT2166_0_2167"], ["H_core", "Hcore"], ["selector"]], "machine-readable 2167 handoff."),
        ("SRC2167_03_1866_selector", DOCS["1866"], [["RSA1866_5_verdict"], ["HSE1866_1_Euler_equation"], ["VAL1866_OVERALL"]], "prior selector/Hcore attempt: selector not derived; finite route retained."),
        ("SRC2167_04_1866_validation", DOCS["1866_validation"], [["VAL1866_OVERALL"], ["PASS"]], "1866 validation passed as nonclaim."),
        ("SRC2167_05_1867_object_language", DOCS["1867"], [["OLA1867_5_verdict"], ["FINT1867_0_ZR"], ["NEXT1867_0_primary"]], "downstream object-language radial-cell route and finite intake precedent."),
        ("SRC2167_06_1867_validation", DOCS["1867_validation"], [["VAL1867_OVERALL"], ["PASS"]], "1867 validation passed as nonclaim."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, needles_found=needles_found, expected_needles="; ".join(" OR ".join(group) for group in needle_groups), role=role))
    return rows


def selector_rows() -> list[dict[str, object]]:
    data = [
        ("RSA2167_0_target_orientation", "parent Euler orientation for C_R", "D_R_NORMAL_FORM_DERIVED_IF_PARENT_SIGNED", "TARGET_DEFINED_NOT_DERIVED", "MISSING_RECIPROCITY_SELECTOR_ORIENTATION", "test concrete selector routes rather than assume E_time-E_radial selects C_R"),
        ("RSA2167_1_object_language", "C_R/R_AB as parent compatibility data", "FORBIDS_INDEPENDENT_ZR_JR_IF_TYPED_PARENT_GRAMMAR_SIGNED", "BEST_ROUTE_NOT_SIGNED", "MISSING_TYPED_PARENT_PRIMITIVE_CONSTRUCTOR_LIST", "select typed parent grammar as next proof"),
        ("RSA2167_2_linear_multiplier", "lambda_R C_R or lambda_R(partial_r C_R-S_R)", "EXACT_LOCAL_RECIPROCITY_IF_PARENT_OWNED", "FORMAL_PASS_NOT_PARENT_SIGNED", "MISSING_LAMBDAR_PARENT_ORIGIN_DIRAC_MATTER_BOUNDARY", "closure template only"),
        ("RSA2167_3_second_order_Hcore", "ordinary H_core with Z_R,M_R^2,J_R", "FINITE_ELLIPTIC_SUPPRESSION_OR_MASS_GAP", "FINITE_BRANCH_NOT_ZERO_PROOF", "MISSING_ZR_MR2_JR_BOUNDARY_SOURCE_AND_NO_CHARGE", "source-ready residual branch only"),
        ("RSA2167_4_cell_current", "conserved reciprocal cell current", "Q_R_ZERO_IF_PARENT_NO_CHARGE_THEOREM", "CONSERVATION_ONLY_LEAVES_HAIR", "MISSING_QR_ZERO_THEOREM_AND_BOUNDARY_CHARGE_CLASS", "parallel boundary theorem target"),
        ("RSA2167_5_verdict", "reciprocity selector proof", "LOCAL_GR_SELECTOR_DERIVED", "RECIPROCITY_SELECTOR_NOT_DERIVED_CURRENT_CORPUS", "MISSING_PARENT_OBJECT_LANGUAGE_OR_SIGNED_HCORE", "demote D_R to closure benchmark and move to typed object-language or finite Z_R/J_R intake"),
    ]
    return [row(selector_id=selector_id, candidate_selector=candidate_selector, best_possible_result=best_possible_result, actual_status=actual_status, missing_input=missing_input, decision=decision) for selector_id, candidate_selector, best_possible_result, actual_status, missing_input, decision in data]


def hcore_rows() -> list[dict[str, object]]:
    data = [
        ("HSE2167_0_density", "reciprocal H_core density", "H_R=int sqrt(h)[1/2 Z_R h^ij D_i R_AB D_j R_AB + 1/2 M_R^2 R_AB^2 + lambda_R R_AB + J_R R_AB]+B_R", "FORMAL_TEMPLATE_ONLY", "MISSING_PARENT_ORIGIN_OF_ZR_MR2_LAMBDAR_JR_BR"),
        ("HSE2167_1_euler", "R_AB Euler/source equation", "E_R=-D_i(Z_R D^i R_AB)+M_R^2 R_AB+lambda_R+J_R+coefficient_variation_terms=0", "FINITE_RESIDUAL_BY_DEFAULT", "MISSING_SELECTOR_ZERO_THEOREM"),
        ("HSE2167_2_multiplier", "lambda_R exact branch", "lambda_R enforces R_AB=0 or partial_r C_R-S_R=0 only if parent-owned and Dirac-stable", "LAMBDAR_PARENT_ORIGIN_NOT_DERIVED", "MISSING_PARENT_CANONICAL_GRAMMAR"),
        ("HSE2167_3_verdict", "H_core source equation", "ordinary H_core does not prove local GR; it defines finite reciprocal residual physics unless the object-language/multiplier proof closes", "HCORE_FINITE_BRANCH_NOT_EXACT_ZERO", "source Z_R/M_R^2/J_R/B_R/Q_R/S_R or derive typed grammar"),
    ]
    return [row(hcore_id=hcore_id, object=object_name, equation_or_statement=equation_or_statement, status=status, missing_input=missing_input) for hcore_id, object_name, equation_or_statement, status, missing_input in data]


def finite_rows() -> list[dict[str, object]]:
    data = [
        ("FZR2167_0_ZR", "Z_R", "reciprocal gradient stiffness", "parent H_core coefficient or theorem Z_R=0", "MISSING_PARENT_INPUT", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
        ("FZR2167_1_MR2", "M_R^2", "reciprocal mass/gap", "parent H_core coefficient or protected zero theorem", "MISSING_PARENT_INPUT", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
        ("FZR2167_2_JR", "J_R", "direct source drive of reciprocal mode", "matter descent map or proof direct source forbidden", "MISSING_PARENT_INPUT", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
        ("FZR2167_3_BR", "B_R", "boundary/corner reciprocal source", "boundary class or flux/collar coefficient", "MISSING_BOUNDARY_INPUT", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
        ("FZR2167_4_QR", "Q_R", "exterior reciprocal charge/hair", "no-charge theorem or finite charge row", "MISSING_BOUNDARY_INPUT", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
        ("FZR2167_5_SR", "S_R", "total local reciprocal source residual", "coefficient map from q_loc, matter descent, boundary, readout and current slots", "MISSING_PARENT_INPUT", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
        ("FZR2167_6_tau_R10", "tau_R10", "short-range fifth-force projection", "map finite R_AB residual to alpha(lambda) style bounds", "MISSING_ARENA_PROJECTION", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
        ("FZR2167_7_tau_PPN", "tau_PPN", "post-Newtonian residual vector", "map finite C_R/R_AB residual to gamma,beta,light-deflection,Shapiro", "MISSING_ARENA_PROJECTION", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
    ]
    return [row(finite_id=finite_id, symbol=symbol, role=role, required_source=required_source, status=status, numeric_value=numeric_value, source_path=source_path) for finite_id, symbol, role, required_source, status, numeric_value, source_path in data]


def no_smuggling_rows() -> list[dict[str, object]]:
    data = [
        ("NSG2167_0_no_EH_identity", "use GR radial Einstein-equation difference as MTS selector", "imports local-GR fixed point before deriving it", "ACTIVE_BLOCK"),
        ("NSG2167_1_no_unimodular_axiom", "impose J_q=1 and call it derived", "unimodular radial-cell condition is closure unless parent-signed", "ACTIVE_BLOCK"),
        ("NSG2167_2_no_gauge_slogan", "use gauge/Noether words to create R_AB=0", "Noether identities relate owned equations; they do not create the missing constraint", "ACTIVE_BLOCK"),
        ("NSG2167_3_no_test_claim", "treat finite intake rows as local-test pass", "all rows are placeholders until numeric parent coefficients and projections exist", "ACTIVE_BLOCK"),
    ]
    return [row(guard_id=guard_id, forbidden_move=forbidden_move, reason=reason, status=status) for guard_id, forbidden_move, reason, status in data]


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("CG2167_0_selector", "parent reciprocity selector has been derived", False, "object-language/multiplier/Hcore routes remain unsigned"),
        ("CG2167_1_DR", "D_R=partial_r C_R-S_R is a derived parent Euler equation", False, "selector not derived"),
        ("CG2167_2_ZR_zero", "Z_R=0 is derived rather than chosen", False, "R_AB independence not excluded"),
        ("CG2167_3_JR_zero", "J_R=0 follows from matter descent", False, "matter descent proof missing"),
        ("CG2167_4_local_GR", "local GR/Newton reduction is derived", False, "selector, no-charge, source and readout gates open"),
        ("CG2167_5_finite_ready", "finite Z_R/J_R branch is score-ready", False, "numeric values/source paths/projections missing"),
    ]
    return [row(gate_id=gate_id, claim=claim, gate_pass=gate_pass, reason=reason) for gate_id, claim, gate_pass, reason in data]


def refusal_rows() -> list[dict[str, object]]:
    data = [
        ("REF2167_0_selector_claim", "claim reciprocity selector is proven", "PARENT_SELECTOR_MISSING", "BLOCKED", "no route is parent-signed", False),
        ("REF2167_1_hcore_zero", "claim ordinary Hcore gives exact C_R=0", "FINITE_BRANCH_BY_DEFAULT", "BLOCKED", "ordinary Hcore permits Z_R/M_R^2/J_R residuals", False),
        ("REF2167_2_lambda_closure", "use lambda_R as derived multiplier", "LAMBDAR_ORIGIN_MISSING", "BLOCKED", "Dirac/matter/boundary checks unsigned", False),
        ("REF2167_3_finite_score", "score finite Z_R/J_R rows now", "VALUES_SOURCES_PROJECTIONS_MISSING", "BLOCKED", "intake rows are nonclaim placeholders", False),
        ("REF2167_4_local_gr", "claim local GR/Newton", "SELECTOR_AND_SR_GATES_OPEN", "BLOCKED", "D_R remains closure benchmark", False),
    ]
    return [row(refusal_id=refusal_id, attempted_claim=attempted_claim, input_status=input_status, runner_result=runner_result, blocked_by=blocked_by, score_eligible=score_eligible) for refusal_id, attempted_claim, input_status, runner_result, blocked_by, score_eligible in data]


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2167_0_result", "RECIPROCITY_SELECTOR_NOT_DERIVED_CURRENT_CORPUS", "object-language, multiplier, Hcore and cell-current routes all remain parent-unsigned", "no local-GR/Newton claim"),
        ("DEC2167_1_demote_DR", "D_R_DEMOTED_TO_CLOSURE_BENCHMARK", "the normal form is exact as target but not derived from live parent action", "organize residuals/tests but do not promote"),
        ("DEC2167_2_best_route", "OBJECT_LANGUAGE_RADIAL_CELL_CONSTRAINT_SELECTED", "only typed parent grammar can forbid independent Z_R/J_R before readout", "try to build typed primitive/constructor grammar"),
        ("DEC2167_3_fallback", "FINITE_ZR_JR_REQUIREMENT_LEDGER_READY", "ordinary Hcore branch becomes finite residual physics if typed grammar fails", "source coefficients and projections before tests"),
    ]
    return [row(decision_id=decision_id, decision=decision, because=because, next_action=next_action) for decision_id, decision, because, next_action in data]


def next_target_rows() -> list[dict[str, object]]:
    data = [
        ("NEXT2167_0_2168", "2168-Y5-R2FR-object-language-radial-cell-constraint-or-finite-ZRJR-intake.md", "scripts/Y5_R2FR_object_language_radial_cell_constraint_or_finite_ZRJR_intake_2168.py", "prove C_R/R_AB is a parent compatibility/constraint object with no independent derivative grammar; if this fails, generate finite Z_R/J_R/Q_R/S_R source-ready rows", "selected", "typed parent object-language closes the selector without GR import, or all finite reciprocal residual coefficients/projections are explicit nonclaim rows"),
        ("NEXT2167_1_parallel_QR", "2168b-Y5-R2FR-boundary-no-charge-theorem-for-reciprocal-hair.md", "scripts/Y5_R2FR_boundary_no_charge_theorem_for_reciprocal_hair_2168b.py", "attack Q_R=0 separately from boundary/source neutrality", "held", "no-charge theorem or finite Q_R source row"),
    ]
    return [row(route_id=route_id, next_target=next_target, script=script, objective=objective, selection_status=selection_status, success_condition=success_condition) for route_id, next_target, script, objective, selection_status, success_condition in data]


def write_branch_copies(selector: list[dict[str, object]], hcore: list[dict[str, object]], finite: list[dict[str, object]], next_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        ("COPY2167_0_source_weight_docs", BRANCH_COPIES["source_weight"], selector + hcore),
        ("COPY2167_1_branch_locked_wep", BRANCH_COPIES["branch_wep"], finite),
        ("COPY2167_2_acquisition_queue", BRANCH_COPIES["queue"], next_rows + finite),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(sources, selector, hcore, finite, guards, gates, refusals, decisions, next_rows, copies, csv_paths):
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    selector_ok = any(item["selector_id"] == "RSA2167_5_verdict" and item["actual_status"] == "RECIPROCITY_SELECTOR_NOT_DERIVED_CURRENT_CORPUS" for item in selector)
    hcore_ok = any(item["hcore_id"] == "HSE2167_3_verdict" and item["status"] == "HCORE_FINITE_BRANCH_NOT_EXACT_ZERO" for item in hcore)
    finite_ok = len(finite) == 8 and all(not truthy(item.get("valid_for_claim", False)) for item in finite)
    guards_ok = all(item["status"] == "ACTIVE_BLOCK" for item in guards)
    gate_ok = all(not truthy(item["gate_pass"]) for item in gates) and all(not truthy(item.get("claim_allowed", False)) for item in gates)
    refusal_ok = all(item["runner_result"] == "BLOCKED" and not truthy(item.get("score_eligible", False)) for item in refusals)
    decisions_ok = any(item["decision_id"] == "DEC2167_2_best_route" for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2167_0_2168" and item["selection_status"] == "selected" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False)) for group in (sources, selector, hcore, finite, guards, gates, refusals, decisions, next_rows, copies) for item in group)
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2167_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, selector_ok, hcore_ok, finite_ok, guards_ok, gate_ok, refusal_ok, decisions_ok, next_ok, copies_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2167_00_sources", sources_ok, "2166 plus 1866/1867 source paths and needles validate"),
        ("VAL2167_01_selector", selector_ok, "reciprocity selector remains nonclaim"),
        ("VAL2167_02_hcore", hcore_ok, "ordinary Hcore branch is finite residual by default"),
        ("VAL2167_03_finite", finite_ok, "finite Z_R/J_R/Q_R/S_R intake rows are nonclaim"),
        ("VAL2167_04_guards", guards_ok, "no-smuggling guards are active"),
        ("VAL2167_05_claim_gates", gate_ok, "all selector/local-GR/finite-score claim gates remain blocked"),
        ("VAL2167_06_refusals", refusal_ok, "refusal runner blocks selector, Hcore-zero, lambda closure, finite-score and local-GR claims"),
        ("VAL2167_07_decision", decisions_ok, "decision ledger selects typed object-language route"),
        ("VAL2167_08_next", next_ok, "2168 next target selected"),
        ("VAL2167_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2167_10_csv_parse", csv_ok, "all generated 2167 CSVs parse cleanly"),
        ("VAL2167_11_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2167_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2167"),
        ("VAL2167_13_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2167_OVERALL", all_ok, "2167 rejects selector/Hcore exact-zero derivation and selects object-language radial-cell proof or finite ZRJR intake."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(sources, selector, hcore, finite, guards, gates, refusals, decisions, next_rows, copies, validation) -> None:
    line_2166, _ = find_line(DOCS["2166"], ["NEXT2166_0_2167"])
    line_1866, _ = find_line(DOCS["1866"], ["RSA1866_5_verdict"])
    line_1867, _ = find_line(DOCS["1867"], ["OLA1867_5_verdict"])
    content = "\n\n".join(
        [
            "# 2167 - Y5/R2FR Reciprocity Selector Operator Or Hcore Source Equation",
            "## Current Verdict",
            "2167 does **not** derive the reciprocity selector, does **not** derive `D_R=partial_r C_R-S_R`, and does **not** claim local GR/Newton.",
            "It sharpens the fork: a signed object-language rule that makes `C_R/R_AB` compatibility data could forbid independent `Z_R` and direct `J_R`; ordinary `H_core` instead gives a finite reciprocal residual branch by default.",
            "So the exact-zero local branch is fenced but alive only through typed parent grammar. If that grammar fails, the honest route is finite `Z_R/J_R/Q_R/S_R` coefficients with arena projections.",
            f"This follows the 2166 handoff at line {line_2166}, imports the 1866 selector verdict at line {line_1866}, and uses the 1867 object-language verdict at line {line_1867}.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Reciprocity Selector Audit",
            md_table(selector, ["selector_id", "candidate_selector", "best_possible_result", "actual_status", "missing_input", "decision", "valid_for_claim"]),
            "## Hcore Source-Equation Test",
            md_table(hcore, ["hcore_id", "object", "equation_or_statement", "status", "missing_input", "valid_for_claim"]),
            "## Finite Z_R/J_R Requirements",
            md_table(finite, ["finite_id", "symbol", "role", "required_source", "status", "numeric_value", "source_path", "valid_for_claim"]),
            "## No-Smuggling Guards",
            md_table(guards, ["guard_id", "forbidden_move", "reason", "status", "valid_for_claim"]),
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
            "The clean route is now almost brutally clear: do not invent a force; write the parent grammar so the reciprocal cell is not allowed to be an independent field with a kinetic term or direct source. That is a serious GR-reduction route. If it cannot be derived, we stop pretending and test the finite reciprocal residual branch.",
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    selector = selector_rows()
    hcore = hcore_rows()
    finite = finite_rows()
    guards = no_smuggling_rows()
    gates = claim_gate_rows()
    refusals = refusal_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["selector_audit"], selector)
    write_csv(OUTPUTS["hcore"], hcore)
    write_csv(OUTPUTS["finite"], finite)
    write_csv(OUTPUTS["no_smuggle"], guards)
    write_csv(OUTPUTS["claim_gate"], gates)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    copies = write_branch_copies(selector, hcore, finite, next_rows)
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(sources, selector, hcore, finite, guards, gates, refusals, decisions, next_rows, copies, csv_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, selector, hcore, finite, guards, gates, refusals, decisions, next_rows, copies, validation)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"2167 validation {validation[-1]['status']}")


if __name__ == "__main__":
    main()

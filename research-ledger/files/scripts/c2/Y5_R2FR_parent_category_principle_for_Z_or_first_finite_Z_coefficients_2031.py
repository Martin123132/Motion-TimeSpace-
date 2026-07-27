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


DOC = ROOT / "2031-Y5-R2FR-parent-category-principle-for-Z-or-first-finite-Z-coefficients.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def formalization_has_2031_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        return any(FORMALIZATION.rglob("*2031*Z*")) or any(FORMALIZATION.rglob("*2031*category*"))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2031_00_2030_handoff",
            ROOT / "2030-Y5-R2FR-parent-object-language-Z-removal-or-SZ-coefficient-acquisition.md",
            ["NEXT2030_0_2031", "OLZ2030_5_removal_theorem", "VAL2030_OVERALL"],
            "2030 handoff selects parent category principle or first finite Z coefficients.",
        ),
        (
            "SRC2031_01_2030_next",
            OUT / "P8_Y5_PARENT_QLOC_2030_NEXT_TARGET.csv",
            ["NEXT2030_0_2031"],
            "machine-readable 2031 target.",
        ),
        (
            "SRC2031_02_06_nohair",
            ROOT / "06-reciprocal-charge-source-neutrality.md",
            ["Pi_R = 0 -> Q_R = 0 -> R_AB = 0 -> AB = 1.", "R_AB is not a scalar hair mode at all."],
            "early source-boundary/no-scalar-hair route.",
        ),
        (
            "SRC2031_03_07_nonpropagating",
            ROOT / "07-nonpropagating-reciprocity-constraint.md",
            ["S_constraint = integral lambda_R R_AB.", "no R_AB kinetic term;", "kinetic R_AB route = demoted;"],
            "nonpropagating reciprocity constraint route.",
        ),
        (
            "SRC2031_04_10_observer",
            ROOT / "10-observer-map-symplectic-contract.md",
            ["R_AB = ln(T^2 S) = 2 ln(J_q).", "gamma - 1 = 0 after R_AB=0."],
            "observer map relation between reciprocal strain and PPN gamma.",
        ),
        (
            "SRC2031_05_05_countermodel",
            ROOT / "05-reciprocity-theorem-attempt.md",
            ["S_R = integral dr [0.5 W(r) (R_AB')^2 + J_R R_AB].", "Asymptotic flatness alone does not kill `Q_R`."],
            "kinetic/current-hair countermodel for finite reciprocal scalar route.",
        ),
        (
            "SRC2031_06_1581_ppn",
            ROOT / "1581-Y5-RAB-qRhat-profile-and-Cassini-bound-row-or-no-charge-return.md",
            ["PROF1581_3_ppn_ratio", "NCR1581_0_source_boundary", "VAL1581_OVERALL"],
            "finite Q_R hair maps to PPN/Cassini pressure but remains nonclaim.",
        ),
        (
            "SRC2031_07_1579_finite",
            ROOT / "1579-Y5-RAB-finite-component-source-acquisition-ledger-and-comparator-dry-run.md",
            ["ACQ1579_1_ZR", "ACQ1579_2_MR2", "DEC1579_0_acquisition_state"],
            "finite component source acquisition ledger has no internal values.",
        ),
        (
            "SRC2031_08_1868_grammar",
            ROOT / "source-intake" / "microscope" / "quarantine" / "1868" / "P8_Y5_PARENT_QLOC_1868_CANDIDATE_PARENT_GRAMMAR.csv",
            ["CPG1868_2_no_independent_RAB", "CPG1868_3_derivative_permission", "CPG1868_4_constraint_admission"],
            "typed parent grammar candidate.",
        ),
        (
            "SRC2031_09_1868_terms",
            ROOT / "source-intake" / "microscope" / "quarantine" / "1868" / "P8_Y5_PARENT_QLOC_1868_TERM_LEGALITY_MATRIX.csv",
            ["TLM1868_0_ZR_kinetic", "TLM1868_1_MR2_potential", "TLM1868_2_lambda_constraint"],
            "term legality matrix with kinetic/potential countermodels.",
        ),
        (
            "SRC2031_10_Cperp_conditions",
            ROOT / "runs" / "20260601-000088-Cperp-residual-shift-constraint-attempt" / "results" / "first_class_conditions.csv",
            ["F2_no_Cperp_kinetic_term", "F3_no_Cperp_gradient_stiffness", "F4_no_Cperp_potential"],
            "representative-shift conditions: no kinetic, gradient, or potential representative energy.",
        ),
    ]
    rows = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def category_principle_rows() -> list[dict[str, object]]:
    data = [
        (
            "CAT2031_0_primitive_list",
            "primitive object list",
            "Let the parent action vary only MTS primitives: motion/time/space coframes or routing fields, transport/connection data, matter fields, and boundary/domain variables.",
            "FORMAL_CONTRACT_NOT_PARENT_DERIVED",
            "Z/R_AB is not automatically a primitive just because it is definable from readout variables.",
            "the full primitive list is not sourced from one parent action",
        ),
        (
            "CAT2031_1_derived_compatibility",
            "derived compatibility scalar",
            "R_AB=ln(T^2 S)=2 ln(J_q) is a derived compatibility/readout scalar; treating it as an independent field is an extra dynamical choice.",
            "DEFINITIONAL_THEOREM",
            "this supports the category route: derived compatibility data should not get its own local scalar energy by default.",
            "definition alone does not forbid all primitive invariants from projecting onto R_AB",
        ),
        (
            "CAT2031_2_admissible_operator_rule",
            "admissible operator grammar",
            "Allowed local operators are built from primitives and their covariant/exterior derivatives; raw Z/R_AB may enter only as quotient/compatibility data, constraint target, exact boundary class, or post-variation readout.",
            "EXACT_CONDITIONAL_RULE",
            "forbids standalone K_Z(dZ)^2, M_Z^2 Z^2, J_Z Z, and B_Z boundary flux in the exact-removal branch.",
            "operator grammar is proposed, not derived from MTS primitives",
        ),
        (
            "CAT2031_3_chain_rule_guard",
            "chain-rule derivative guard",
            "If primitive derivatives induce derivatives of R_AB by algebraic substitution, that is not a standalone Z kinetic term unless a new independent coefficient survives after rewriting the primitive action.",
            "NO_FAKE_KINETIC_THEOREM",
            "prevents both overclaiming and over-penalizing: primitive geometry can vary while raw representative Z is still nonphysical.",
            "requires a parent action rewrite to identify whether an independent coefficient survives",
        ),
        (
            "CAT2031_4_constraint_permission",
            "constraint/auxiliary permission",
            "A Lambda_Z C_Z block is admissible only if Lambda_Z and C_Z arise from parent compatibility/Dirac preservation, not as a magic multiplier inserted to force GR.",
            "EXACT_CONDITIONAL_RULE",
            "keeps the clean exact route without permitting closure-only axioms.",
            "auxiliary origin and Dirac/boundary checks remain missing",
        ),
        (
            "CAT2031_5_matter_boundary_guard",
            "matter/source/boundary guard",
            "Matter, source normalization, clocks, EM, and boundary maps must descend through quotient-owned observed variables; any direct Z source slot moves the branch to finite residuals.",
            "EXACT_CONDITIONAL_RULE",
            "blocks WEP, clock, R10, and source-weight leaks.",
            "matter/readout descent and boundary no-charge are not parent-signed",
        ),
        (
            "CAT2031_6_category_principle",
            "parent category principle",
            "If CAT2031_0 through CAT2031_5 are parent-signed, raw Z/R_AB is compatibility/constraint/readout data rather than a propagating local scalar; local Z fifth-force terms are illegal in the exact branch.",
            "EXACT_CONDITIONAL_THEOREM",
            "this would derive local Z-removal without tuning K0,V0,mZ2 or hiding scalar hair.",
            "premises are not parent-signed together",
        ),
        (
            "CAT2031_7_verdict",
            "2031 category-principle verdict",
            "The category principle is mathematically coherent and now precisely stated, but current evidence does not prove it from MTS primitives. The branch remains nonclaim; if the principle fails, finite Z coefficients must be acquired.",
            "THEOREM_TARGET_NOT_ACTIVATED",
            "we have a real decision point instead of a vague gap.",
            "parent primitive grammar/source action missing",
        ),
    ]
    rows = []
    for row_id, clause, statement, status, payoff, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "clause": clause,
                "statement": statement,
                "status": status,
                "payoff": payoff,
                "blocker": blocker,
            }
        )
        rows.append(row)
    return rows


def countermodel_rows() -> list[dict[str, object]]:
    data = [
        (
            "CM2031_0_kinetic_hair",
            "K_Z(dZ)^2 survives",
            "S_R=int dr [0.5 W(R_AB')^2 + J_R R_AB] gives W R_AB'=Q_R and asymptotic flatness alone does not kill Q_R.",
            "FINITE_SCALAR_HAIR_COUNTERMODEL",
            "must prove category-forbidden or acquire Q_R/q_R_hat bounds",
        ),
        (
            "CM2031_1_mass_term",
            "M_Z^2 Z^2 survives",
            "A smooth potential makes Z a finite local field unless it is auxiliary/constraint-owned or double-zero sourced.",
            "FINITE_MASSIVE_SCALAR_COUNTERMODEL",
            "must source M_Z^2 and range or prove term illegal",
        ),
        (
            "CM2031_2_direct_source",
            "J_Z Z survives",
            "Direct source coupling shifts the local residual and blocks theorem-zero even if pure geometry is quotient-clean.",
            "SOURCE_SLOT_COUNTERMODEL",
            "must prove matter/source descent or acquire J_Z",
        ),
        (
            "CM2031_3_boundary_charge",
            "B_Z/Q_Z survives",
            "Boundary/corner flux revives reciprocal hair even if bulk terms are constrained.",
            "BOUNDARY_COUNTERMODEL",
            "must prove no-charge/exact boundary or acquire Q_Z/B_Z",
        ),
        (
            "CM2031_4_GR_identity_import",
            "GR identity used as proof",
            "Einstein radial identities or Schwarzschild AB=1 can check the end-state but cannot derive MTS Z removal.",
            "CIRCULAR_PROOF_COUNTERMODEL",
            "no-GR-import guard remains active",
        ),
    ]
    rows = []
    for row_id, countermodel, statement, status, required_response in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "countermodel": countermodel,
                "statement": statement,
                "status": status,
                "required_response": required_response,
            }
        )
        rows.append(row)
    return rows


def finite_coefficient_rows() -> list[dict[str, object]]:
    data = [
        ("FZ2031_0_ZR", "Z_R", "gradient stiffness / kinetic coefficient", "prove forbidden or source numeric value", "MISSING_PARENT_INPUT"),
        ("FZ2031_1_MR2", "M_R^2", "mass/stiffness scale and range denominator", "prove absent/auxiliary or source numeric value", "MISSING_PARENT_INPUT"),
        ("FZ2031_2_QR", "Q_R", "exterior reciprocal charge from W R_AB'=Q_R", "prove Q_R=0 or source finite value", "MISSING_BOUNDARY_OR_SOURCE_VALUE"),
        ("FZ2031_3_qRhat", "q_R_hat", "R_AB^(1)/(2U_N) or -Q_R/(2 kappa_W G M)", "source Q_R,kappa_W,M,tails or prove zero", "MISSING_PPN_SOURCE_DENOMINATOR"),
        ("FZ2031_4_JR", "J_R", "direct source drive for reciprocal mode", "prove matter descent zero or source coefficient", "MISSING_MATTER_DESCENT"),
        ("FZ2031_5_BR", "B_R", "boundary/corner reciprocal term", "prove no-charge or source boundary value", "MISSING_BOUNDARY_INPUT"),
        ("FZ2031_6_tau_R10", "tau_R10", "short-range fifth-force projection", "map to alpha(lambda) with accepted bound curve", "MISSING_ARENA_PROJECTION"),
        ("FZ2031_7_tau_PPN", "tau_PPN", "PPN projection for gamma/beta/light/Shapiro", "map finite residual to PPN vector", "MISSING_ARENA_PROJECTION"),
        ("FZ2031_8_tau_clock", "tau_clock", "clock/redshift projection", "map to fractional frequency/redshift", "MISSING_ARENA_PROJECTION"),
        ("FZ2031_9_tau_orbital", "tau_orbital", "orbital/precession projection", "map to acceleration/precession residual", "MISSING_ARENA_PROJECTION"),
    ]
    rows = []
    for row_id, symbol, definition, requirement, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "requirement": requirement,
                "status": status,
                "source_path": "MISSING_PARENT_OR_DATA_SOURCE",
                "claim_status": "RETAINED_NONCLAIM_FINITE_COEFFICIENT",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2031_0_progress", "The parent category principle is now stated as an exact conditional theorem, not a slogan.", "future work can attack precise premises instead of circling Dq/kinectic terms"),
        ("DEC2031_1_not_closed", "The theorem is not activated because the parent primitive grammar and operator admission rule are not derived from one action.", "no local-GR claim"),
        ("DEC2031_2_best_next", "The next least-scrutiny target is deriving the primitive/operator grammar from motion/time/space coframe-routing primitives.", "if this closes, kinetic/potential scalar-hair terms become illegal by type"),
        ("DEC2031_3_backstop", "If the category principle does not close, switch to finite Z coefficients and local arena projections.", "the finite branch is testable but not a derived-GR route"),
    ]
    rows = []
    for decision_id, decision, consequence in data:
        row = base_row()
        row.update({"decision_id": decision_id, "decision": decision, "consequence": consequence})
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2031_0_category_theorem", "parent category theorem is written", "CAT2031_6", "PASS_CONDITIONAL_NONCLAIM", False),
        ("GATE2031_1_primitive_grammar", "primitive/operator grammar is parent-derived", "CAT2031_0;CAT2031_2", "FAIL_UNSIGNED", False),
        ("GATE2031_2_constraint_origin", "constraint/auxiliary route is parent-owned", "CAT2031_4", "FAIL_UNSIGNED", False),
        ("GATE2031_3_matter_boundary", "matter/readout/boundary direct Z slots are absent", "CAT2031_5", "FAIL_UNSIGNED", False),
        ("GATE2031_4_countermodels_closed", "kinetic/potential/source/boundary countermodels are closed", "CM2031_*", "FAIL_COUNTERMODELS_ACTIVE", False),
        ("GATE2031_5_finite_coefficients", "finite Z coefficients are source-backed", "FZ2031_*", "FAIL_MISSING_VALUES", False),
        ("GATE2031_6_local_GR_claim", "local GR/Newton/PPN/R10 pass can be claimed", "GATE2031_1..5", "FAIL_BLOCKED", False),
    ]
    rows = []
    for gate_id, claim, required_rows, status, allowed in data:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "claim": claim,
                "required_rows": required_rows,
                "status": status,
                "claim_allowed": allowed,
                "reason": "category principle is conditional and finite coefficients remain missing",
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "next_id": "NEXT2031_0_2032",
            "target_doc": "2032-Y5-R2FR-primitive-operator-grammar-derivation-or-finite-Z-source-runner.md",
            "objective": "derive the primitive/operator grammar from motion/time/space coframe-routing primitives so raw Z kinetic/potential/source terms are illegal, or start the finite Z coefficient source runner",
            "required_inputs": "one parent primitive list; admissible local operator grammar; proof R_AB/Z is derived compatibility data; auxiliary origin; matter/readout descent; boundary no-charge; finite source rows if grammar fails",
            "exclusions": "local-GR claim; magic multiplier; GR identity import; Dq-only proof; ignoring Q_R countermodel; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def write_branch_copies(
    category_rows: list[dict[str, object]],
    countermodel_rows_: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2031_0_source_weight", SOURCE_WEIGHT_DOCS / "AFRAME_PARENT_CATEGORY_Z_2031_NONCLAIM.csv", category_rows),
        ("COPY2031_1_wep_lock", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2031_CATEGORY_COUNTERMODELS_NONCLAIM.csv", countermodel_rows_),
        ("COPY2031_2_acquisition_queue", QUEUE / "JR2031_FIRST_FINITE_Z_COEFFICIENT_QUEUE.csv", finite_rows),
    ]
    rows = []
    for copy_id, path, payload in copies:
        write_csv(path, payload)
        row = base_row()
        row.update(
            {
                "copy_id": copy_id,
                "path": str(path),
                "status": "WRITTEN_NONCLAIM_COPY" if path.exists() and csv_rows_parse(path) else "COPY_WRITE_FAIL",
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    source_rows: list[dict[str, object]],
    category_rows: list[dict[str, object]],
    countermodel_rows_: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2031_00_sources_exist", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows), "all cited source paths and needles exist"))
    checks.append(("VAL2031_01_csv_parse", all(path.exists() and csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2031_02_category_theorem", any(row["row_id"] == "CAT2031_6_category_principle" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in category_rows), "category theorem is explicit"))
    checks.append(("VAL2031_03_chain_rule_guard", any(row["row_id"] == "CAT2031_3_chain_rule_guard" for row in category_rows), "chain-rule derivative guard is present"))
    checks.append(("VAL2031_04_countermodels_active", len(countermodel_rows_) == 5 and all("COUNTERMODEL" in str(row["status"]) or row["status"] == "CIRCULAR_PROOF_COUNTERMODEL" for row in countermodel_rows_), "countermodels remain active"))
    checks.append(("VAL2031_05_finite_rows_nonclaim", all(row["valid_for_claim"] is False and str(row["status"]).startswith("MISSING_") for row in finite_rows), "finite coefficient rows remain missing/nonclaim"))
    checks.append(("VAL2031_06_claims_blocked", all(row["claim_allowed"] is False for row in gate_rows), "all local claims remain blocked"))
    checks.append(("VAL2031_07_next_selected", len(next_rows) == 1 and next_rows[0]["next_id"] == "NEXT2031_0_2032", "next target is selected"))
    checks.append(("VAL2031_08_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2031_09_no_formalization_2031_artifacts", not formalization_has_2031_artifacts(), "no 2031 Z/category artifacts were written under formalization-workbench"))
    rows = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    overall = base_row()
    overall.update(
        {
            "check_id": "VAL2031_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2031 parent category principle for Z checkpoint is internally valid and nonclaim.",
        }
    )
    rows.append(overall)
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    category_rows: list[dict[str, object]],
    countermodel_rows_: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    lines = [
        "# 2031 Y5 R2FR Parent Category Principle For Z Or First Finite Z Coefficients",
        "",
        "## Current Verdict",
        "The category principle is now precise: raw `Z/R_AB` may be local compatibility/readout/constraint data without being a propagating scalar. If the parent primitive/operator grammar is signed, standalone `K_Z(dZ)^2`, `M_Z^2 Z^2`, `J_Z Z`, and boundary `Q_Z` terms are illegal in the exact local-GR branch. This would remove the local fifth-force channel without tuning. Current MTS does not yet derive that grammar from one parent action, so the result remains nonclaim; if the grammar fails, finite `Z_R/M_R^2/Q_R/J_R/B_R` rows must be acquired.",
        "",
        "## Source Register",
        md_table(source_rows, ["source_id", "source_path", "status", "needles", "note", "valid_for_claim"]),
        "## Category Principle Attempt",
        md_table(category_rows, ["row_id", "clause", "statement", "status", "payoff", "blocker", "valid_for_claim"]),
        "## Countermodel Ledger",
        md_table(countermodel_rows_, ["row_id", "countermodel", "statement", "status", "required_response", "valid_for_claim"]),
        "## First Finite Z Coefficient Queue",
        md_table(finite_rows, ["row_id", "symbol", "definition", "requirement", "status", "source_path", "claim_status", "valid_for_claim"]),
        "## Claim Gate",
        md_table(gate_rows, ["gate_id", "claim", "required_rows", "status", "claim_allowed", "reason", "valid_for_claim"]),
        "## Decision Ledger",
        md_table(decision_rows_, ["decision_id", "decision", "consequence", "valid_for_claim"]),
        "## Next Target",
        md_table(next_rows, ["next_id", "target_doc", "objective", "required_inputs", "exclusions", "valid_for_claim"]),
        "## Branch Copies",
        md_table(branch_rows, ["copy_id", "path", "status", "valid_for_claim"]),
        "## Validation",
        md_table(validation_rows_, ["check_id", "status", "detail", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    category_rows = category_principle_rows()
    countermodel_rows_ = countermodel_rows()
    finite_rows = finite_coefficient_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "source": OUT / "P8_Y5_PARENT_QLOC_2031_SOURCE_REGISTER.csv",
        "category": OUT / "P8_Y5_PARENT_QLOC_2031_CATEGORY_PRINCIPLE_ATTEMPT.csv",
        "countermodels": OUT / "P8_Y5_PARENT_QLOC_2031_COUNTERMODEL_LEDGER.csv",
        "finite": OUT / "P8_Y5_PARENT_QLOC_2031_FIRST_FINITE_Z_COEFFICIENT_QUEUE.csv",
        "gate": OUT / "P8_Y5_PARENT_QLOC_2031_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2031_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2031_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2031_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2031_VALIDATION.csv",
    }
    write_csv(paths["source"], source_rows)
    write_csv(paths["category"], category_rows)
    write_csv(paths["countermodels"], countermodel_rows_)
    write_csv(paths["finite"], finite_rows)
    write_csv(paths["gate"], gate_rows)
    write_csv(paths["decision"], decision_rows_)
    write_csv(paths["next"], next_rows)
    branch_rows = write_branch_copies(category_rows, countermodel_rows_, finite_rows)
    write_csv(paths["branch"], branch_rows)

    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [
        Path(row["path"]) for row in branch_rows
    ]
    validation_rows_ = validation_rows(
        source_rows,
        category_rows,
        countermodel_rows_,
        finite_rows,
        gate_rows,
        next_rows,
        csv_paths_without_validation,
    )
    write_csv(paths["validation"], validation_rows_)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in branch_rows]
    validation_rows_ = validation_rows(
        source_rows,
        category_rows,
        countermodel_rows_,
        finite_rows,
        gate_rows,
        next_rows,
        csv_paths,
    )
    write_csv(paths["validation"], validation_rows_)
    write_doc(
        source_rows,
        category_rows,
        countermodel_rows_,
        finite_rows,
        gate_rows,
        decision_rows_,
        next_rows,
        branch_rows,
        validation_rows_,
    )
    remove_pycache()


if __name__ == "__main__":
    main()

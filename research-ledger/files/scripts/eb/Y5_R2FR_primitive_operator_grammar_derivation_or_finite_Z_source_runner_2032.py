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


DOC = ROOT / "2032-Y5-R2FR-primitive-operator-grammar-derivation-or-finite-Z-source-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def formalization_has_2032_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        return any(FORMALIZATION.rglob("*2032*grammar*")) or any(FORMALIZATION.rglob("*2032*finite*Z*"))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2032_00_2031_handoff",
            ROOT / "2031-Y5-R2FR-parent-category-principle-for-Z-or-first-finite-Z-coefficients.md",
            ["NEXT2031_0_2032", "CAT2031_6_category_principle", "VAL2031_OVERALL"],
            "2031 handoff selects primitive/operator grammar or finite Z source runner.",
        ),
        (
            "SRC2032_01_2031_next",
            OUT / "P8_Y5_PARENT_QLOC_2031_NEXT_TARGET.csv",
            ["NEXT2031_0_2032"],
            "machine-readable 2032 target.",
        ),
        (
            "SRC2032_02_02_motion_load",
            ROOT / "02-motion-load-local-GR-reduction.md",
            ["If the clock residue and spatial routing are reciprocal:", "parent origin of reciprocal routing = missing;"],
            "motion-load reciprocal-routing intuition and missing parent origin.",
        ),
        (
            "SRC2032_03_10_observer",
            ROOT / "10-observer-map-symplectic-contract.md",
            ["The local observer coframe must be defined before any PPN claim:", "R_AB = ln(T^2 S) = 2 ln(J_q)."],
            "observer coframe/readout and derived reciprocal strain.",
        ),
        (
            "SRC2032_04_1009_parent_contract",
            ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            ["PCS1009_9_total_parent_contract", "CG1009_0_total_parent_action", "DEC1009_0_contract_not_parent_action"],
            "total parent action/field-list contract is useful but not promoted.",
        ),
        (
            "SRC2032_05_1868_grammar",
            ROOT / "source-intake" / "microscope" / "quarantine" / "1868" / "P8_Y5_PARENT_QLOC_1868_CANDIDATE_PARENT_GRAMMAR.csv",
            ["CPG1868_0_parent_primitives", "CPG1868_2_no_independent_RAB", "CPG1868_3_derivative_permission"],
            "candidate primitive grammar and derivative permission rule.",
        ),
        (
            "SRC2032_06_Cperp_shift_conditions",
            ROOT / "runs" / "20260601-000088-Cperp-residual-shift-constraint-attempt" / "results" / "first_class_conditions.csv",
            ["F2_no_Cperp_kinetic_term", "F3_no_Cperp_gradient_stiffness", "F4_no_Cperp_potential"],
            "representative-shift grammar conditions.",
        ),
        (
            "SRC2032_07_2031_finite",
            OUT / "P8_Y5_PARENT_QLOC_2031_FIRST_FINITE_Z_COEFFICIENT_QUEUE.csv",
            ["FZ2031_0_ZR", "FZ2031_1_MR2", "FZ2031_9_tau_orbital"],
            "finite Z coefficient queue from 2031.",
        ),
        (
            "SRC2032_08_1579_finite",
            ROOT / "1579-Y5-RAB-finite-component-source-acquisition-ledger-and-comparator-dry-run.md",
            ["ACQ1579_1_ZR", "DRY1579_0_R10", "DEC1579_0_acquisition_state"],
            "older finite component acquisition/dry-run state.",
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


def grammar_derivation_rows() -> list[dict[str, object]]:
    data = [
        (
            "GRAM2032_0_action_ontology",
            "parent action ontology",
            "Only fields in the parent variational field list may carry independent kinetic, potential, source, and boundary-charge terms.",
            "EXACT_FIELD_THEORY_RULE",
            "This is standard variational discipline: no variable gets a propagator without being a parent field or an explicit auxiliary/constraint object.",
            "the MTS parent field list is not yet signed by one action",
        ),
        (
            "GRAM2032_1_MTS_primitives",
            "candidate MTS primitives",
            "Candidate primitives are motion/time/space coframe-routing variables, transport/connection data, matter fields, and boundary/domain variables before metric/readout projection.",
            "CANDIDATE_PRIMITIVE_LIST",
            "This matches the MTS language and avoids starting from GR as an axiom.",
            "candidate list is not yet a parent variation with theta/current",
        ),
        (
            "GRAM2032_2_derived_readout",
            "derived readout exclusion",
            "R_AB=ln(T^2 S)=2 ln(J_q) is derived compatibility/readout data; it is not automatically an independent parent scalar.",
            "DERIVED_COMPATIBILITY_RULE",
            "Z/R_AB can be measured or constrained without becoming a new local degree of freedom.",
            "derived status does not by itself forbid all primitive action projections",
        ),
        (
            "GRAM2032_3_operator_admission",
            "operator admission rule",
            "Primitive derivatives are admissible; standalone raw-Z operators K_Z(dZ)^2, M_Z^2 Z^2, J_Z Z, and Q_Z are admissible only if Z is promoted to a parent field or retained as finite residual.",
            "EXACT_CONDITIONAL_GRAMMAR",
            "This is the real fork: exact removal or finite scalar branch.",
            "parent action ontology is unsigned",
        ),
        (
            "GRAM2032_4_substitution_test",
            "substitution/no-fake-kinetic test",
            "Rewrite primitive action terms in readout variables; if a Z-derivative appears only by substitution with no independent coefficient, it is primitive-sector stress, not a standalone Z propagator.",
            "DERIVED_TEST",
            "prevents accidentally inventing scalar hair from a change of variables.",
            "requires actual primitive action terms to rewrite",
        ),
        (
            "GRAM2032_5_promotion_test",
            "promotion-to-field test",
            "If a standalone coefficient remains after rewriting, Z has been promoted to a physical finite field and must enter the finite coefficient runner.",
            "COUNTERMODEL_TRIGGER",
            "keeps the route honest under scrutiny.",
            "finite source values are missing",
        ),
        (
            "GRAM2032_6_constraint_admission",
            "constraint admission",
            "A Lambda_Z C_Z block is legal only as a parent-derived auxiliary/constraint with preservation, bracket/degree, boundary, and matter/readout descent checks.",
            "EXACT_CONDITIONAL_GRAMMAR",
            "permits exact local removal without magic multipliers.",
            "auxiliary origin and Dirac checks remain missing",
        ),
        (
            "GRAM2032_7_verdict",
            "2032 grammar verdict",
            "The primitive/operator grammar can be derived as a conditional field-theory rule, but current MTS does not yet own the parent action ontology. Therefore the grammar blocks claims but does not yet prove local GR.",
            "GRAMMAR_DERIVED_CONDITIONAL_NOT_ACTIVATED",
            "next work must sign the parent action ontology or run finite coefficient acquisition.",
            "one parent primitive list/current chain missing",
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


def admission_matrix_rows() -> list[dict[str, object]]:
    data = [
        ("ADM2032_0_primitive_kinetic", "derivatives of parent primitives", "ADMIT", "owned by parent field list and theta/current", "requires parent action source"),
        ("ADM2032_1_readout_definition", "R_AB=ln(T^2 S) as readout definition", "ADMIT_AS_READOUT", "not a new kinetic scalar", "requires observer map/source matching"),
        ("ADM2032_2_raw_Z_kinetic", "K_Z(dZ)^2", "REJECT_EXACT_BRANCH", "promotes Z to finite scalar hair", "source Z_R or prove forbidden"),
        ("ADM2032_3_raw_Z_potential", "M_Z^2 Z^2 or V(Z)", "REJECT_EXACT_BRANCH", "promotes Z to finite massive scalar", "source M_R^2/m_Z^2 or prove forbidden"),
        ("ADM2032_4_direct_source", "J_Z Z", "REJECT_EXACT_BRANCH", "direct matter/source slot", "prove matter descent or source J_Z"),
        ("ADM2032_5_boundary_charge", "B_Z or Q_Z surface flux", "REJECT_EXACT_BRANCH", "edge charge bypass", "prove boundary no-charge or source Q_Z"),
        ("ADM2032_6_constraint", "Lambda_Z C_Z", "ADMIT_IF_PARENT_DERIVED", "nonpropagating exact route", "derive auxiliary origin and preservation"),
        ("ADM2032_7_exact_boundary", "dB_Z with Q_Z=0/proper", "ADMIT_IF_CERTIFIED", "topological/exact local silence", "derive exact primitive or source boundary row"),
    ]
    rows = []
    for row_id, operator, decision, reason, required_action in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "operator": operator,
                "decision": decision,
                "reason": reason,
                "required_action": required_action,
                "claim_status": "NONCLAIM_ADMISSION_RULE",
            }
        )
        rows.append(row)
    return rows


def finite_runner_rows() -> list[dict[str, object]]:
    data = [
        ("RUN2032_0_schema", "finite Z source runner schema exists", "Z_R,M_R^2,Q_R,J_R,B_R,q_R_hat,tau_R10,tau_PPN,tau_clock,tau_orbital", "READY_SCHEMA_NONCLAIM"),
        ("RUN2032_1_values", "internal coefficient values", "all finite coefficients have numeric values, units, source paths", "MISSING_VALUES"),
        ("RUN2032_2_projection", "arena projections", "R10/PPN/WEP/clock/orbital maps with no missing tails", "MISSING_PROJECTIONS"),
        ("RUN2032_3_no_cancellation", "absolute-sum/no-cancellation guard", "all residual components evaluated before any pass/fail", "MISSING_COMPONENTS"),
        ("RUN2032_4_claim", "finite branch can claim pass", "values plus projections below thresholds", "FAIL_BLOCKED"),
    ]
    rows = []
    for row_id, item, requirement, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "item": item,
                "requirement": requirement,
                "status": status,
                "claim_status": "FINITE_RUNNER_DRY_SCHEMA",
            }
        )
        rows.append(row)
    return rows


def dryrun_rows() -> list[dict[str, object]]:
    cases = [
        ("CASE2032_0_grammar_signed", True, False, False, "THEOREM_ZERO_IF_PARENT_SIGNED_NOT_CURRENT"),
        ("CASE2032_1_kinetic_countermodel", False, True, False, "REFUSE_CLAIM_REQUIRE_ZR_QR"),
        ("CASE2032_2_source_countermodel", False, False, True, "REFUSE_CLAIM_REQUIRE_JR_BOUND"),
        ("CASE2032_3_all_missing", False, False, False, "REFUSE_CLAIM_MISSING_ALL"),
    ]
    rows = []
    for case_id, grammar_signed, finite_values, projections, expected in cases:
        claim_allowed = grammar_signed and finite_values and projections
        row = base_row()
        row.update(
            {
                "case_id": case_id,
                "grammar_signed": grammar_signed,
                "finite_values": finite_values,
                "arena_projections": projections,
                "expected_result": expected,
                "claim_allowed": claim_allowed,
                "status": "DRYRUN_REFUSES_CLAIM" if not claim_allowed else "DRYRUN_SCHEMA_ONLY_NOT_EVIDENCE",
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2032_0_grammar_written", "primitive/operator grammar is written", "GRAM2032_*", "PASS_CONDITIONAL_NONCLAIM", False),
        ("GATE2032_1_parent_ontology", "one parent primitive field list/current chain is signed", "GRAM2032_0..1", "FAIL_UNSIGNED", False),
        ("GATE2032_2_operator_admission_active", "admission matrix is parent-owned", "ADM2032_*", "FAIL_UNSIGNED", False),
        ("GATE2032_3_substitution_test_executed", "primitive action rewritten to detect independent Z coefficients", "GRAM2032_4..5", "FAIL_NO_PARENT_ACTION", False),
        ("GATE2032_4_finite_runner_ready", "finite runner has real values and projections", "RUN2032_*", "FAIL_MISSING_VALUES", False),
        ("GATE2032_5_local_GR_claim", "local GR/Newton/PPN/R10 pass can be claimed", "GATE2032_1..4", "FAIL_BLOCKED", False),
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
                "reason": "grammar is conditional and finite runner values are missing",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2032_0_progress", "Primitive/operator grammar is now operational enough to classify terms.", "we can distinguish exact-removal branch from finite-scalar branch"),
        ("DEC2032_1_blocker", "The blocker is not the grammar shape; it is ownership by one parent action/current chain.", "derive parent ontology or keep claims blocked"),
        ("DEC2032_2_next", "The next best target is a parent action ontology owner row: field list, variations, theta/current, and operator-admission policy.", "without it, finite runner is the honest fallback"),
        ("DEC2032_3_fallback", "Finite runner is staged but cannot score without Z_R/M_R^2/Q_R/J_R/B_R and arena projections.", "no empirical pass until source rows exist"),
    ]
    rows = []
    for decision_id, decision, consequence in data:
        row = base_row()
        row.update({"decision_id": decision_id, "decision": decision, "consequence": consequence})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "next_id": "NEXT2032_0_2033",
            "target_doc": "2033-Y5-R2FR-parent-action-ontology-owner-or-first-finite-Z-row.md",
            "objective": "derive a parent action ontology owner row with primitive field list, variations, theta/current and operator-admission policy; if not, acquire the first real finite Z_R/M_R^2/Q_R/J_R/B_R row",
            "required_inputs": "parent action field list; variation variables; symplectic/current chain; operator grammar owner; rewrite/substitution test; finite coefficient source paths if ontology fails",
            "exclusions": "local-GR claim; grammar-by-assertion; magic multiplier; GR import; cancellation-only finite runner; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def write_branch_copies(
    grammar_rows: list[dict[str, object]],
    admission_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2032_0_source_weight", SOURCE_WEIGHT_DOCS / "AFRAME_PRIMITIVE_OPERATOR_GRAMMAR_2032_NONCLAIM.csv", grammar_rows),
        ("COPY2032_1_wep_lock", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2032_ADMISSION_MATRIX_NONCLAIM.csv", admission_rows),
        ("COPY2032_2_acquisition_queue", QUEUE / "JR2032_FINITE_Z_SOURCE_RUNNER_SCHEMA.csv", finite_rows),
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
    grammar_rows: list[dict[str, object]],
    admission_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    dry_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2032_00_sources_exist", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows), "all cited source paths and needles exist"))
    checks.append(("VAL2032_01_csv_parse", all(path.exists() and csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2032_02_grammar_verdict", any(row["row_id"] == "GRAM2032_7_verdict" and row["status"] == "GRAMMAR_DERIVED_CONDITIONAL_NOT_ACTIVATED" for row in grammar_rows), "conditional grammar verdict is present"))
    checks.append(("VAL2032_03_admission_rejects_raw_Z", any(row["row_id"] == "ADM2032_2_raw_Z_kinetic" and row["decision"] == "REJECT_EXACT_BRANCH" for row in admission_rows), "raw Z kinetic term is rejected in exact branch"))
    checks.append(("VAL2032_04_finite_runner_blocked", any(row["row_id"] == "RUN2032_4_claim" and row["status"] == "FAIL_BLOCKED" for row in finite_rows), "finite runner remains blocked"))
    checks.append(("VAL2032_05_dryrun_refuses_claims", all(row["claim_allowed"] is False for row in dry_rows), "dry-run cases do not claim evidence"))
    checks.append(("VAL2032_06_claims_blocked", all(row["claim_allowed"] is False for row in gate_rows), "all local claims remain blocked"))
    checks.append(("VAL2032_07_next_selected", len(next_rows) == 1 and next_rows[0]["next_id"] == "NEXT2032_0_2033", "next target is selected"))
    checks.append(("VAL2032_08_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2032_09_no_formalization_2032_artifacts", not formalization_has_2032_artifacts(), "no 2032 grammar/finite-Z artifacts were written under formalization-workbench"))
    rows = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    overall = base_row()
    overall.update(
        {
            "check_id": "VAL2032_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2032 primitive/operator grammar checkpoint is internally valid and nonclaim.",
        }
    )
    rows.append(overall)
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    grammar_rows: list[dict[str, object]],
    admission_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    dry_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    lines = [
        "# 2032 Y5 R2FR Primitive Operator Grammar Derivation Or Finite Z Source Runner",
        "",
        "## Current Verdict",
        "The primitive/operator grammar is now operational as a conditional field-theory rule: only parent primitives may carry independent kinetic/potential/source/boundary operators. `R_AB/Z` can be derived compatibility/readout data, a constraint target, or exact boundary data; if a standalone `K_Z(dZ)^2`, `M_Z^2 Z^2`, `J_Z Z`, or `Q_Z` coefficient survives the parent-action rewrite, the theory has a finite scalar branch and must source coefficients. The grammar is not yet active because MTS still lacks one parent action ontology owner row.",
        "",
        "## Source Register",
        md_table(source_rows, ["source_id", "source_path", "status", "needles", "note", "valid_for_claim"]),
        "## Primitive Operator Grammar",
        md_table(grammar_rows, ["row_id", "clause", "statement", "status", "payoff", "blocker", "valid_for_claim"]),
        "## Admission Matrix",
        md_table(admission_rows, ["row_id", "operator", "decision", "reason", "required_action", "claim_status", "valid_for_claim"]),
        "## Finite Source Runner Schema",
        md_table(finite_rows, ["row_id", "item", "requirement", "status", "claim_status", "valid_for_claim"]),
        "## Dry-Run Cases",
        md_table(dry_rows, ["case_id", "grammar_signed", "finite_values", "arena_projections", "expected_result", "claim_allowed", "status", "valid_for_claim"]),
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
    grammar_rows = grammar_derivation_rows()
    admission_rows = admission_matrix_rows()
    finite_rows = finite_runner_rows()
    dry_rows = dryrun_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "source": OUT / "P8_Y5_PARENT_QLOC_2032_SOURCE_REGISTER.csv",
        "grammar": OUT / "P8_Y5_PARENT_QLOC_2032_PRIMITIVE_OPERATOR_GRAMMAR.csv",
        "admission": OUT / "P8_Y5_PARENT_QLOC_2032_ADMISSION_MATRIX.csv",
        "finite": OUT / "P8_Y5_PARENT_QLOC_2032_FINITE_SOURCE_RUNNER_SCHEMA.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2032_DRYRUN_CASES.csv",
        "gate": OUT / "P8_Y5_PARENT_QLOC_2032_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2032_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2032_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2032_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2032_VALIDATION.csv",
    }
    write_csv(paths["source"], source_rows)
    write_csv(paths["grammar"], grammar_rows)
    write_csv(paths["admission"], admission_rows)
    write_csv(paths["finite"], finite_rows)
    write_csv(paths["dry"], dry_rows)
    write_csv(paths["gate"], gate_rows)
    write_csv(paths["decision"], decision_rows_)
    write_csv(paths["next"], next_rows)
    branch_rows = write_branch_copies(grammar_rows, admission_rows, finite_rows)
    write_csv(paths["branch"], branch_rows)

    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [
        Path(row["path"]) for row in branch_rows
    ]
    validation_rows_ = validation_rows(
        source_rows,
        grammar_rows,
        admission_rows,
        finite_rows,
        dry_rows,
        gate_rows,
        next_rows,
        csv_paths_without_validation,
    )
    write_csv(paths["validation"], validation_rows_)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in branch_rows]
    validation_rows_ = validation_rows(
        source_rows,
        grammar_rows,
        admission_rows,
        finite_rows,
        dry_rows,
        gate_rows,
        next_rows,
        csv_paths,
    )
    write_csv(paths["validation"], validation_rows_)
    write_doc(
        source_rows,
        grammar_rows,
        admission_rows,
        finite_rows,
        dry_rows,
        gate_rows,
        decision_rows_,
        next_rows,
        branch_rows,
        validation_rows_,
    )
    remove_pycache()


if __name__ == "__main__":
    main()

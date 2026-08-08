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


DOC = ROOT / "2030-Y5-R2FR-parent-object-language-Z-removal-or-SZ-coefficient-acquisition.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def formalization_has_2030_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        return any(FORMALIZATION.rglob("*2030*Z*")) or any(FORMALIZATION.rglob("*2030*object*language*"))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2030_00_2029_handoff",
            ROOT / "2029-Y5-R2FR-source-SZ-normal-form-and-local-profile-pack.md",
            ["NEXT2029_0_2030", "SZR2029_5_verdict", "VAL2029_OVERALL"],
            "2029 handoff selects parent object-language Z removal or coefficient acquisition.",
        ),
        (
            "SRC2030_01_2029_next",
            OUT / "P8_Y5_PARENT_QLOC_2029_NEXT_TARGET.csv",
            ["NEXT2029_0_2030"],
            "machine-readable 2030 target.",
        ),
        (
            "SRC2030_02_1868_grammar",
            ROOT / "source-intake" / "microscope" / "quarantine" / "1868" / "P8_Y5_PARENT_QLOC_1868_CANDIDATE_PARENT_GRAMMAR.csv",
            ["CPG1868_2_no_independent_RAB", "CPG1868_3_derivative_permission", "CPG1868_4_constraint_admission"],
            "typed parent grammar candidate for forbidding standalone reciprocal/Z dynamics.",
        ),
        (
            "SRC2030_03_1868_terms",
            ROOT / "source-intake" / "microscope" / "quarantine" / "1868" / "P8_Y5_PARENT_QLOC_1868_TERM_LEGALITY_MATRIX.csv",
            ["TLM1868_0_ZR_kinetic", "TLM1868_1_MR2_potential", "TLM1868_2_lambda_constraint"],
            "term legality matrix: kinetic/potential countermodels and legal constraint route.",
        ),
        (
            "SRC2030_04_1858_constraint",
            ROOT / "1858-Y5-R2FR-parent-constraint-package-no-GR-import-gate.md",
            ["PCP1858_2_generator_or_auxiliary_solve", "ORG1858_4_second_class_auxiliary", "VAL1858_OVERALL"],
            "constraint/auxiliary local-GR route with no-GR-import guard.",
        ),
        (
            "SRC2030_05_1866_requirements",
            ROOT / "source-intake" / "microscope" / "quarantine" / "1866" / "P8_Y5_PARENT_QLOC_1866_FINITE_ZRJR_REQUIREMENTS.csv",
            ["FZR1866_0_ZR", "FZR1866_1_MR2", "FZR1866_7_R10_projection"],
            "finite Z_R/J_R requirement rows if object-language removal fails.",
        ),
        (
            "SRC2030_06_1867_intake",
            ROOT / "source-intake" / "microscope" / "quarantine" / "1867" / "P8_Y5_PARENT_QLOC_1867_FINITE_ZRJR_INTAKE_ROWS.csv",
            ["FINT1867_0_ZR", "FINT1867_1_MR2", "FINT1867_9_tau_orbital"],
            "finite Z_R/J_R intake rows remain missing/nonclaim.",
        ),
        (
            "SRC2030_07_Cperp_shift_conditions",
            ROOT / "runs" / "20260601-000088-Cperp-residual-shift-constraint-attempt" / "results" / "first_class_conditions.csv",
            ["F2_no_Cperp_kinetic_term", "F3_no_Cperp_gradient_stiffness", "F4_no_Cperp_potential"],
            "representative-shift first-class conditions prohibit kinetic/gradient/potential representative energy.",
        ),
        (
            "SRC2030_08_Cperp_constraint",
            ROOT / "runs" / "20260601-000088-Cperp-residual-shift-constraint-attempt" / "results" / "constraint_algebra.csv",
            ["candidate_generator", "Hamiltonian_bracket", "preservation_condition"],
            "constraint algebra requires Hamiltonian independence from representative Cperp.",
        ),
        (
            "SRC2030_09_Cperp_quotient_gate",
            ROOT / "runs" / "20260601-000089-parent-no-Cperp-action-or-closure" / "results" / "gate_results.csv",
            ["no_Cperp_action_writeable", "Hamiltonian_Cperp_independence"],
            "quotient action skeleton conditionally omits representative Cperp.",
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


def object_language_rows() -> list[dict[str, object]]:
    data = [
        (
            "OLZ2030_0_parent_primitives",
            "typed parent primitives",
            "Parent action must be written in motion/time/space coframe-routing primitives, transport/connection data, matter fields, and boundary/domain variables before metric readout.",
            "CONTRACT_READY_NOT_PARENT_DERIVED",
            "prevents beginning by importing GR metric variables",
            "does not yet forbid a coframe-volume scalar from becoming dynamical",
        ),
        (
            "OLZ2030_1_Z_as_derived_compatibility",
            "Z/R_AB as compatibility data",
            "Z-like reciprocal/cell variables may appear only as derived compatibility data or constrained auxiliary elimination targets, not independent local matter fields.",
            "BEST_EXACT_ROUTE_CONDITIONAL",
            "blocks ordinary scalar kinetic/potential hair if parent-signed",
            "currently asserted as grammar, not forced by a parent variational principle",
        ),
        (
            "OLZ2030_2_derivative_permission",
            "no standalone derivative operators on Z",
            "Covariant/exterior derivatives act on parent primitives, transport fields, and matter, but not on raw Z/R_AB as a standalone scalar.",
            "CONDITIONAL_FORBIDS_PROPAGATING_Z",
            "forbids kinetic/gradient fifth-force channels without tuning K0=0",
            "coframe derivative invariants could regenerate equivalent derivatives unless grammar is proven",
        ),
        (
            "OLZ2030_3_constraint_admission",
            "legal auxiliary/constraint block",
            "A Lambda_Z C_Z block is legal only when Lambda_Z is parent-owned and preservation, matter descent, and boundary silence close.",
            "CONDITIONAL_EXACT_ROUTE",
            "gives exact local removal without a propagating scalar",
            "lambda/multiplier origin and Dirac/boundary checks are missing",
        ),
        (
            "OLZ2030_4_matter_boundary_descent",
            "matter/readout/boundary blindness",
            "Matter, source normalization, clocks, EM, and boundary/readout maps must descend through quotient-owned observed variables and not direct-source Z.",
            "REQUIRED_SIDE_CLAUSE",
            "prevents source-only and edge-charge bypasses",
            "universal matter descent and boundary no-charge theorem are unsigned",
        ),
        (
            "OLZ2030_5_removal_theorem",
            "Z removal theorem",
            "If OLZ2030_1..4 hold, then raw Z has no kinetic/potential/source/boundary local stress; it is quotient, constraint, auxiliary, or exact-boundary data, so local GR is not polluted by a Z fifth force at first order.",
            "EXACT_CONDITIONAL_THEOREM",
            "this is the least-scrutiny route because it avoids inventing a hidden scalar and then tuning it away",
            "premises are not parent-signed together",
        ),
        (
            "OLZ2030_6_verdict",
            "2030 object-language verdict",
            "The object-language route is coherent and preferable, but current MTS does not yet derive the category principle. Therefore Z-removal remains a theorem target, not a local-GR claim.",
            "ROUTE_OPEN_NOT_CLOSED",
            "next proof must derive the category principle from motion/time/space primitives or fall back to finite coefficients",
            "parent category principle missing",
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


def term_legality_rows() -> list[dict[str, object]]:
    data = [
        ("TERM2030_0_Z_kinetic", "1/2 Z_R h^ij D_i R_AB D_j R_AB", "FORBIDDEN_IF_GRAMMAR_SIGNED", "LEGAL_COUNTERMODEL_IF_NOT_SIGNED", "dangerous fifth-force/hair term"),
        ("TERM2030_1_Z_potential", "1/2 M_R^2 R_AB^2 or V(Z)", "FORBIDDEN_OR_AUXILIARY_ONLY_IF_GRAMMAR_SIGNED", "LEGAL_COUNTERMODEL_IF_NOT_SIGNED", "turns compatibility residual into finite scalar mode"),
        ("TERM2030_2_lambda_constraint", "Lambda_Z C_Z[B,U]", "LEGAL_IF_PARENT_AUXILIARY_SIGNED", "CLOSURE_INSERTION_IF_NOT_SIGNED", "clean exact route if multiplier origin and Dirac checks close"),
        ("TERM2030_3_direct_source", "J_Z Z or J_R C_R", "FORBIDDEN_IF_MATTER_DESCENT_SIGNED", "LEGAL_COUNTERMODEL_IF_NOT_SIGNED", "direct source slot blocks theorem-zero"),
        ("TERM2030_4_boundary_charge", "B_Z(Z) or Q_Z surface flux", "FORBIDDEN_IF_BOUNDARY_NO_CHARGE_SIGNED", "LEGAL_COUNTERMODEL_IF_NOT_SIGNED", "edge charge revives local hair"),
        ("TERM2030_5_exact_boundary", "dB_Z with Q_Z=0/proper/exact", "LEGAL_IF_BOUNDARY_CERTIFIED", "OPEN_IF_BOUNDARY_UNSIGNED", "topological/exact escape route"),
        ("TERM2030_6_gauge_fixing", "representative gauge fixing with ghost/stress accounted", "LEGAL_ONLY_IF_NOT_PHYSICAL_STRESS", "COUNTERMODEL_IF_STRESS_LEAKS", "must not become a hidden energy source"),
        ("TERM2030_7_GR_identity", "import Einstein radial identity or Schwarzschild AB=1", "FORBIDDEN_AS_PARENT_PROOF", "CIRCULAR_IF_USED", "allowed only as end-state check"),
    ]
    rows = []
    for row_id, term, if_signed, if_unsigned, implication in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "term": term,
                "if_grammar_signed": if_signed,
                "if_grammar_unsigned": if_unsigned,
                "implication": implication,
                "claim_status": "NONCLAIM_LEGALITY_AUDIT",
            }
        )
        rows.append(row)
    return rows


def proof_obligation_rows() -> list[dict[str, object]]:
    data = [
        ("ZRO2030_0_category_principle", "derive category principle", "why Z/R_AB is compatibility/constraint data rather than independent local field", "MISSING_PARENT_CATEGORY_PRINCIPLE"),
        ("ZRO2030_1_no_derivative_invariants", "forbid derivative invariants", "show allowed coframe/transport invariants cannot regenerate standalone D_i Z D^i Z", "MISSING_OPERATOR_CLOSURE"),
        ("ZRO2030_2_auxiliary_origin", "own Lambda_Z or auxiliary block", "derive multiplier/auxiliary from MTS primitives, not as magic zero insertion", "MISSING_AUXILIARY_ORIGIN"),
        ("ZRO2030_3_local_solve", "algebraic/local solve", "E_Lambda/E_Z eliminate Z before readout with no Green-function tail", "MISSING_LOCAL_SOLVE"),
        ("ZRO2030_4_bracket_degree", "bracket/degree count", "prove first-class or second-class elimination removes exactly the dangerous pair", "MISSING_BRACKET_DEGREE_COUNT"),
        ("ZRO2030_5_boundary", "boundary charge silence", "Q_Z is zero/proper/exact or retained as finite residual", "MISSING_BOUNDARY_ZERO"),
        ("ZRO2030_6_matter_readout", "matter/readout descent", "ordinary matter, EM, clocks, PPN, orbit readouts see reduced variables only", "MISSING_MATTER_READOUT_DESCENT"),
        ("ZRO2030_7_component_lock", "physical component lock", "eliminated Z is the local fifth-force/reciprocal component, not a cosmology/galaxy memory mode needed elsewhere", "MISSING_COMPONENT_LOCK"),
        ("ZRO2030_8_no_GR_import", "no-GR-import audit", "derive without Schwarzschild AB=1, Einstein vacuum equations, or GR-matched ansatz", "PASS_GUARD_NONCLAIM"),
    ]
    rows = []
    for row_id, obligation, requirement, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "obligation": obligation,
                "requirement": requirement,
                "status": status,
                "source_path": "MISSING_PARENT_OR_DATA_SOURCE" if status != "PASS_GUARD_NONCLAIM" else "1858 no-GR-import guard",
                "claim_status": "NONCLAIM_PROOF_OBLIGATION",
            }
        )
        rows.append(row)
    return rows


def finite_acquisition_rows() -> list[dict[str, object]]:
    data = [
        ("ZFA2030_0_ZR", "Z_R", "gradient stiffness of reciprocal/Z mode", "prove forbidden or source numeric value", "MISSING_PARENT_INPUT"),
        ("ZFA2030_1_MR2", "M_R^2 or m_Z^2", "mass/stiffness scale and local range", "prove absent/auxiliary or source numeric value", "MISSING_PARENT_INPUT"),
        ("ZFA2030_2_JR", "J_R/J_Z", "direct matter/source drive", "prove matter descent zero or source coefficient", "MISSING_PARENT_INPUT"),
        ("ZFA2030_3_BR", "B_R/B_Z", "boundary/corner source term", "prove no-charge or source finite bound", "MISSING_BOUNDARY_INPUT"),
        ("ZFA2030_4_QR", "Q_R/Q_Z", "exterior charge/hair", "derive no-charge theorem or source charge row", "MISSING_BOUNDARY_INPUT"),
        ("ZFA2030_5_SR_total", "S_R/S_Z total", "full local source residual after q_loc/matter/boundary/readout", "source map with units", "MISSING_SOURCE_MAP"),
        ("ZFA2030_6_tau_R10", "tau_R10", "short-range fifth-force projection", "alpha(lambda) or force-ratio mapping", "MISSING_ARENA_PROJECTION"),
        ("ZFA2030_7_tau_PPN", "tau_PPN", "PPN gamma/beta/light/Shapiro residual projection", "dimensionless PPN mapping", "MISSING_ARENA_PROJECTION"),
        ("ZFA2030_8_tau_clock", "tau_clock", "clock/redshift projection", "fractional frequency/redshift mapping", "MISSING_ARENA_PROJECTION"),
        ("ZFA2030_9_tau_orbital", "tau_orbital", "orbital/precession projection", "acceleration/precession mapping", "MISSING_ARENA_PROJECTION"),
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
                "claim_status": "RETAINED_NONCLAIM_ACQUISITION_ROW",
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2030_0_object_language", "parent grammar proves Z is nonpropagating compatibility/constraint data", "OLZ2030_0..6;ZRO2030_0..2", "FAIL_UNSIGNED", False),
        ("GATE2030_1_constraint_elimination", "constraint/auxiliary solve removes Z before readout", "ZRO2030_2..4", "FAIL_UNSIGNED", False),
        ("GATE2030_2_boundary_matter", "boundary and matter/readout are Z-blind", "ZRO2030_5..7", "FAIL_UNSIGNED", False),
        ("GATE2030_3_no_GR_import", "no forbidden GR premise is used", "ZRO2030_8", "PASS_GUARD_NONCLAIM", False),
        ("GATE2030_4_finite_acquisition", "finite Z coefficients are source-backed and score-ready", "ZFA2030_*", "FAIL_MISSING_VALUES", False),
        ("GATE2030_5_local_GR_claim", "local GR/Newton/PPN/R10 pass can be claimed", "GATE2030_0..4", "FAIL_BLOCKED", False),
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
                "reason": "object-language/constraint removal is coherent but not parent-derived",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2030_0_route_status", "Object-language Z removal is the cleanest exact route, but it is not yet derived.", "keep local-GR claim blocked while preserving the route"),
        ("DEC2030_1_key_risk", "If the grammar cannot forbid kinetic/potential/direct-source terms, Z becomes a finite scalar/hair channel.", "then finite coefficient acquisition becomes mandatory"),
        ("DEC2030_2_best_next", "The next derivation target is the parent category principle: why motion/time/space primitives allow compatibility constraints but not standalone Z dynamics.", "this is upstream of bracket/boundary cleanup"),
        ("DEC2030_3_empirical_backstop", "If parent category proof fails, use ZFA2030 rows to build a local residual vector for R10/PPN/WEP/clocks/orbits.", "keeps the work testable rather than rhetorical"),
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
            "next_id": "NEXT2030_0_2031",
            "target_doc": "2031-Y5-R2FR-parent-category-principle-for-Z-or-first-finite-Z-coefficients.md",
            "objective": "derive the parent category principle that forbids standalone Z kinetic/potential/source terms, or acquire the first finite Z_R/M_R^2/J_R/B_R/Q_R coefficient rows",
            "required_inputs": "MTS primitive object list; admissible operator grammar; proof Z is compatibility/constraint data; auxiliary origin; matter/readout descent; boundary no-charge; finite coefficient source paths if proof fails",
            "exclusions": "local-GR claim; magic multiplier; GR identity import; Dq-only proof; ignoring kinetic/potential countermodels; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def write_branch_copies(
    object_rows: list[dict[str, object]],
    obligation_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2030_0_source_weight", SOURCE_WEIGHT_DOCS / "AFRAME_Z_OBJECT_LANGUAGE_REMOVAL_2030_NONCLAIM.csv", object_rows),
        ("COPY2030_1_wep_lock", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2030_Z_REMOVAL_STATUS_NONCLAIM.csv", obligation_rows),
        ("COPY2030_2_acquisition_queue", QUEUE / "JR2030_FINITE_Z_COEFFICIENT_ACQUISITION_QUEUE.csv", acquisition_rows),
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
    object_rows: list[dict[str, object]],
    term_rows: list[dict[str, object]],
    obligation_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2030_00_sources_exist", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows), "all cited source paths and needles exist"))
    checks.append(("VAL2030_01_csv_parse", all(path.exists() and csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2030_02_removal_theorem", any(row["row_id"] == "OLZ2030_5_removal_theorem" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in object_rows), "object-language removal theorem is explicit"))
    checks.append(("VAL2030_03_countermodels_recorded", any(row["row_id"] == "TERM2030_0_Z_kinetic" and "LEGAL_COUNTERMODEL" in str(row["if_grammar_unsigned"]) for row in term_rows), "kinetic/potential countermodel risk is recorded"))
    checks.append(("VAL2030_04_constraint_route_present", any(row["row_id"] == "TERM2030_2_lambda_constraint" and "LEGAL_IF_PARENT_AUXILIARY_SIGNED" in str(row["if_grammar_signed"]) for row in term_rows), "constraint/auxiliary route is present"))
    checks.append(("VAL2030_05_obligations_nonclaim", all(row["valid_for_claim"] is False and (str(row["status"]).startswith("MISSING_") or row["status"] == "PASS_GUARD_NONCLAIM") for row in obligation_rows), "proof obligations remain nonclaim"))
    checks.append(("VAL2030_06_acquisition_rows_nonclaim", all(row["valid_for_claim"] is False and str(row["status"]).startswith("MISSING_") for row in acquisition_rows), "finite acquisition rows remain nonclaim/missing"))
    checks.append(("VAL2030_07_claims_blocked", all(row["claim_allowed"] is False for row in gate_rows), "all local claims remain blocked"))
    checks.append(("VAL2030_08_next_selected", len(next_rows) == 1 and next_rows[0]["next_id"] == "NEXT2030_0_2031", "next target is selected"))
    checks.append(("VAL2030_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2030_10_no_formalization_2030_artifacts", not formalization_has_2030_artifacts(), "no 2030 Z/object-language artifacts were written under formalization-workbench"))
    rows = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    overall = base_row()
    overall.update(
        {
            "check_id": "VAL2030_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2030 parent object-language Z-removal gate is internally valid and nonclaim.",
        }
    )
    rows.append(overall)
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    object_rows: list[dict[str, object]],
    term_rows: list[dict[str, object]],
    obligation_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    lines = [
        "# 2030 Y5 R2FR Parent Object-Language Z Removal Or S_Z Coefficient Acquisition",
        "",
        "## Current Verdict",
        "The cleanest route is now explicit: make `Z` a compatibility/constraint/auxiliary representative rather than a propagating local scalar. If the parent object-language proves that raw `Z` cannot carry kinetic, gradient, potential, direct-source, or boundary-charge terms, then the local fifth-force channel is removed before tuning. Current MTS has not yet derived that category principle, so this is a strong theorem target, not a local-GR claim. If the category principle fails, finite `Z_R/M_R^2/J_R/B_R/Q_R` coefficient rows must be acquired and tested.",
        "",
        "## Source Register",
        md_table(source_rows, ["source_id", "source_path", "status", "needles", "note", "valid_for_claim"]),
        "## Object-Language Removal Attempt",
        md_table(object_rows, ["row_id", "clause", "statement", "status", "payoff", "blocker", "valid_for_claim"]),
        "## Term Legality Audit",
        md_table(term_rows, ["row_id", "term", "if_grammar_signed", "if_grammar_unsigned", "implication", "claim_status", "valid_for_claim"]),
        "## Proof Obligations",
        md_table(obligation_rows, ["row_id", "obligation", "requirement", "status", "source_path", "claim_status", "valid_for_claim"]),
        "## Finite Coefficient Acquisition",
        md_table(acquisition_rows, ["row_id", "symbol", "definition", "requirement", "status", "source_path", "claim_status", "valid_for_claim"]),
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
    object_rows = object_language_rows()
    term_rows = term_legality_rows()
    obligation_rows = proof_obligation_rows()
    acquisition_rows = finite_acquisition_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "source": OUT / "P8_Y5_PARENT_QLOC_2030_SOURCE_REGISTER.csv",
        "object": OUT / "P8_Y5_PARENT_QLOC_2030_OBJECT_LANGUAGE_REMOVAL_ATTEMPT.csv",
        "terms": OUT / "P8_Y5_PARENT_QLOC_2030_TERM_LEGALITY_AUDIT.csv",
        "obligations": OUT / "P8_Y5_PARENT_QLOC_2030_PROOF_OBLIGATIONS.csv",
        "acquisition": OUT / "P8_Y5_PARENT_QLOC_2030_FINITE_COEFFICIENT_ACQUISITION.csv",
        "gate": OUT / "P8_Y5_PARENT_QLOC_2030_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2030_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2030_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2030_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2030_VALIDATION.csv",
    }
    write_csv(paths["source"], source_rows)
    write_csv(paths["object"], object_rows)
    write_csv(paths["terms"], term_rows)
    write_csv(paths["obligations"], obligation_rows)
    write_csv(paths["acquisition"], acquisition_rows)
    write_csv(paths["gate"], gate_rows)
    write_csv(paths["decision"], decision_rows_)
    write_csv(paths["next"], next_rows)
    branch_rows = write_branch_copies(object_rows, obligation_rows, acquisition_rows)
    write_csv(paths["branch"], branch_rows)

    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [
        Path(row["path"]) for row in branch_rows
    ]
    validation_rows_ = validation_rows(
        source_rows,
        object_rows,
        term_rows,
        obligation_rows,
        acquisition_rows,
        gate_rows,
        next_rows,
        csv_paths_without_validation,
    )
    write_csv(paths["validation"], validation_rows_)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in branch_rows]
    validation_rows_ = validation_rows(
        source_rows,
        object_rows,
        term_rows,
        obligation_rows,
        acquisition_rows,
        gate_rows,
        next_rows,
        csv_paths,
    )
    write_csv(paths["validation"], validation_rows_)
    write_doc(
        source_rows,
        object_rows,
        term_rows,
        obligation_rows,
        acquisition_rows,
        gate_rows,
        decision_rows_,
        next_rows,
        branch_rows,
        validation_rows_,
    )
    remove_pycache()


if __name__ == "__main__":
    main()

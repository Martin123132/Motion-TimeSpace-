from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1868"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1868-Y5-R2FR-typed-parent-grammar-for-radial-cell-or-coefficient-bound-branch.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1868_SOURCE_REGISTER.csv",
    "candidate_parent_grammar": RESIDUALS / "P8_Y5_PARENT_QLOC_1868_CANDIDATE_PARENT_GRAMMAR.csv",
    "term_legality_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1868_TERM_LEGALITY_MATRIX.csv",
    "conditional_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1868_CONDITIONAL_GRAMMAR_THEOREM.csv",
    "derivation_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1868_TYPED_GRAMMAR_DERIVATION_ATTEMPT.csv",
    "coefficient_bound_branch": RESIDUALS / "P8_Y5_PARENT_QLOC_1868_COEFFICIENT_BOUND_BRANCH.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1868_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1868_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1868_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1868_VALIDATION.csv",
}


def as_bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def path_has_needle(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def md_escape(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register() -> list[dict[str, Any]]:
    sources = [
        {
            "source_id": "SRC1868_0_1867_doc",
            "source_kind": "current_handoff",
            "source_path": ROOT / "1867-Y5-R2FR-object-language-radial-cell-constraint-or-finite-ZRJR-intake.md",
            "required_needle": "NEXT1867_0_primary",
            "use_in_1868": "selects the typed parent grammar or coefficient-bound branch.",
        },
        {
            "source_id": "SRC1868_1_1867_validation",
            "source_kind": "validation_anchor",
            "source_path": RESIDUALS / "P8_Y5_BRR545_1867_VALIDATION.csv",
            "required_needle": "VAL1867_OVERALL",
            "use_in_1868": "confirms the object-language checkpoint passed.",
        },
        {
            "source_id": "SRC1868_2_1867_contract",
            "source_kind": "typed_contract_seed",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1867_TYPED_OBJECT_CONTRACT.csv",
            "required_needle": "TOC1867_0_primitives",
            "use_in_1868": "imports the explicit grammar clauses needed for the proof.",
        },
        {
            "source_id": "SRC1868_3_1867_countermodel",
            "source_kind": "countermodel_seed",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1867_COUNTERMODEL_AUDIT.csv",
            "required_needle": "CMA1867_0_locality_scalar",
            "use_in_1868": "keeps the ordinary scalar countermodel alive until forbidden by parent grammar.",
        },
        {
            "source_id": "SRC1868_4_1867_finite_intake",
            "source_kind": "finite_branch_seed",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1867_FINITE_ZRJR_INTAKE_ROWS.csv",
            "required_needle": "FINT1867_0_ZR",
            "use_in_1868": "imports finite coefficient rows for the fallback bound branch.",
        },
        {
            "source_id": "SRC1868_5_1866_selector",
            "source_kind": "selector_gate",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1866_SELECTOR_ROUTE_AUDIT.csv",
            "required_needle": "RECIPROCITY_SELECTOR_NOT_DERIVED_CURRENT_CORPUS",
            "use_in_1868": "prevents treating typed grammar as an already-derived selector.",
        },
        {
            "source_id": "SRC1868_6_1257_selector",
            "source_kind": "ZR_lambda_selector_clause",
            "source_path": RESIDUALS / "P8_Y5_R10_1257_ZR_LAMBDAR_SELECTOR_CLAUSES.csv",
            "required_needle": "SEL1257_0_field_exclusion",
            "use_in_1868": "states the conditional field-exclusion route for Z_R=0.",
        },
        {
            "source_id": "SRC1868_7_1274_unimodular",
            "source_kind": "unimodular_cell_audit",
            "source_path": RESIDUALS / "P8_Y5_R10_1274_UNIMODULAR_CELL_ORIGIN_AUDIT.csv",
            "required_needle": "CLOSURE_ONLY_NOT_DERIVED",
            "use_in_1868": "keeps imposed radial-cell unimodularity marked closure-only.",
        },
        {
            "source_id": "SRC1868_8_1272_matrix",
            "source_kind": "cell_principle_matrix",
            "source_path": RESIDUALS / "P8_Y5_R10_1272_CELL_PRINCIPLE_TEST_MATRIX.csv",
            "required_needle": "CPT1272_5_constrained_action",
            "use_in_1868": "identifies constrained action as conditional and unsigned.",
        },
        {
            "source_id": "SRC1868_9_07_nonpropagating",
            "source_kind": "nonpropagating_constraint_note",
            "source_path": ROOT / "07-nonpropagating-reciprocity-constraint.md",
            "required_needle": "nonpropagating_reciprocity_constraint_clean_but_parent_origin_open",
            "use_in_1868": "records the clean algebraic constraint route with open parent origin.",
        },
        {
            "source_id": "SRC1868_10_12_noether",
            "source_kind": "gauge_noether_guard",
            "source_path": ROOT / "12-gauge-noether-origin-audit.md",
            "required_needle": "gauge_noether_origin_not_derived_closure_only",
            "use_in_1868": "blocks gauge/Noether slogans from replacing parent grammar.",
        },
    ]
    rows: list[dict[str, Any]] = []
    for source_entry in sources:
        source_path = source_entry["source_path"]
        needle = source_entry["required_needle"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_entry["source_id"],
                "source_kind": source_entry["source_kind"],
                "source_path": str(source_path),
                "path_exists": as_bool_text(source_path.exists()),
                "required_needle": needle,
                "needle_found": as_bool_text(path_has_needle(source_path, needle)),
                "use_in_1868": source_entry["use_in_1868"],
                "valid_for_claim": as_bool_text(False),
            }
        )
    return rows


def candidate_parent_grammar() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "CPG1868_0_parent_primitives",
            "grammar_layer": "primitive objects",
            "candidate_rule": "The parent action is written in motion/time/space coframe-routing primitives, transport/connection data, and matter fields before metric readout.",
            "derivation_value": "prevents starting from GR metric variables as axioms.",
            "failure_mode": "does not by itself forbid a coframe-volume mode from becoming dynamical.",
            "status": "CONTRACT_READY_NOT_PARENT_DERIVED",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "CPG1868_1_derived_cell_volume",
            "grammar_layer": "derived compatibility object",
            "candidate_rule": "J_q=T sqrt(S), u=ln(J_q), and C_R=R_AB=2u are derived radial-cell compatibility scalars.",
            "derivation_value": "the local target is exact and does not need to be guessed.",
            "failure_mode": "a derived scalar can still be used inside an action unless a category rule forbids it.",
            "status": "DEFINITION_EXACT_NOT_ZERO_THEOREM",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "CPG1868_2_no_independent_RAB",
            "grammar_layer": "category exclusion",
            "candidate_rule": "R_AB is not an independent field and may appear only as compatibility data or a constrained auxiliary elimination target.",
            "derivation_value": "would block ordinary scalar dynamics for the reciprocal cell mode.",
            "failure_mode": "currently asserted as a proposed category rule, not forced by a parent variational principle.",
            "status": "MISSING_PARENT_CATEGORY_PRINCIPLE",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "CPG1868_3_derivative_permission",
            "grammar_layer": "operator permissions",
            "candidate_rule": "Covariant/exterior derivatives act on parent primitives, connection/transport fields, and matter, but not on R_AB as a standalone scalar.",
            "derivation_value": "would set Z_R=0 by legality rather than tuning.",
            "failure_mode": "coframe derivative invariants can still project onto derivatives of ln(J_q) unless this rule is parent-signed.",
            "status": "CONDITIONAL_FORBIDS_ZR",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "CPG1868_4_constraint_admission",
            "grammar_layer": "auxiliary/constraint block",
            "candidate_rule": "A parent-owned Lambda_R C_R block is legal only if Lambda_R is a parent primitive or auxiliary with closed preservation, matter descent, and boundary silence.",
            "derivation_value": "would give C_R=0 exactly without kinetic reciprocal hair.",
            "failure_mode": "the current corpus has the block as a formal closure template, not a derived primitive.",
            "status": "CONDITIONAL_EXACT_ROUTE",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "grammar_id": "CPG1868_5_matter_boundary",
            "grammar_layer": "descent and boundary",
            "candidate_rule": "Matter and boundary terms descend through parent coframe/readout and cannot directly source or charge R_AB.",
            "derivation_value": "would set J_R=0 and Q_R=0 when combined with the constraint block.",
            "failure_mode": "universal matter descent and boundary no-charge theorem are not signed.",
            "status": "MISSING_MATTER_BOUNDARY_DESCENT",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def term_legality_matrix() -> list[dict[str, Any]]:
    rows = [
        (
            "TLM1868_0_ZR_kinetic",
            "1/2 Z_R h^ij D_i R_AB D_j R_AB",
            "ILLEGAL_IF_CATEGORY_RULE_SIGNED",
            "LEGAL_COUNTERMODEL_IF_NOT_SIGNED",
            "This is the dangerous fifth-force/hair term. Type exclusion would kill it, but general coframe locality can regenerate an equivalent derivative of J_q.",
        ),
        (
            "TLM1868_1_MR2_potential",
            "1/2 M_R^2 R_AB^2",
            "ILLEGAL_OR_AUXILIARY_ONLY_IF_CATEGORY_RULE_SIGNED",
            "LEGAL_COUNTERMODEL_IF_NOT_SIGNED",
            "A smooth potential makes C_R a finite residual variable rather than an exact local-GR constraint.",
        ),
        (
            "TLM1868_2_lambda_constraint",
            "Lambda_R C_R",
            "LEGAL_IF_PARENT_AUXILIARY_SIGNED",
            "CLOSURE_INSERTION_IF_NOT_SIGNED",
            "This is the clean exact route, but only after Lambda_R is parent-owned and Dirac/boundary checks close.",
        ),
        (
            "TLM1868_3_direct_source",
            "J_R C_R",
            "ILLEGAL_IF_MATTER_DESCENT_SIGNED",
            "LEGAL_COUNTERMODEL_IF_NOT_SIGNED",
            "Direct matter sourcing shifts the reciprocal mode and blocks theorem-zero.",
        ),
        (
            "TLM1868_4_boundary_charge",
            "B_R(C_R) or Q_R surface flux",
            "ILLEGAL_IF_BOUNDARY_NO_CHARGE_SIGNED",
            "LEGAL_COUNTERMODEL_IF_NOT_SIGNED",
            "Boundary/corner terms can revive reciprocal hair even if the bulk is constrained.",
        ),
        (
            "TLM1868_5_GR_radial_identity",
            "import E_t-E_r from Einstein equations",
            "FORBIDDEN_AS_PARENT_PROOF",
            "CIRCULAR_IF_USED",
            "A GR identity can be an end-state check but not the MTS derivation.",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "term_id": term_id,
            "term": term,
            "status_if_grammar_signed": signed_status,
            "status_current_corpus": current_status,
            "interpretation": interpretation,
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        }
        for term_id, term, signed_status, current_status, interpretation in rows
    ]


def conditional_theorem() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "CGT1868_0_hypotheses",
            "theorem_piece": "conditional typed-grammar local reciprocity theorem",
            "statement": "If R_AB is compatibility data only, Lambda_R C_R is parent-owned, matter/boundary/readout descend silently, and no derivative/source terms on R_AB are legal, then C_R=0 before readout.",
            "proof_status": "CONDITIONAL_THEOREM_ONLY",
            "missing_for_unconditional": "MISSING_PARENT_CATEGORY_PRINCIPLE",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "CGT1868_1_ZR",
            "theorem_piece": "gradient coefficient",
            "statement": "Under the signed category rule, Z_R is absent rather than tuned small.",
            "proof_status": "CONDITIONAL_ZERO",
            "missing_for_unconditional": "MISSING_DERIVATIVE_PERMISSION_PROOF",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "CGT1868_2_JR",
            "theorem_piece": "direct matter source",
            "statement": "Under signed matter descent, J_R is absent because matter couples to parent coframe/readout rather than C_R.",
            "proof_status": "CONDITIONAL_ZERO",
            "missing_for_unconditional": "MISSING_MATTER_DESCENT_PROOF",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "CGT1868_3_QR",
            "theorem_piece": "reciprocal charge",
            "statement": "Under signed boundary/readout silence, no Q_R hair is revived after the bulk constraint.",
            "proof_status": "CONDITIONAL_ZERO",
            "missing_for_unconditional": "MISSING_BOUNDARY_NO_CHARGE_THEOREM",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "CGT1868_4_local_GR",
            "theorem_piece": "local GR/Newton reduction",
            "statement": "C_R=0 plus source/charge silence is necessary for the MTS local branch to inherit the GR/Newton radial reciprocal structure.",
            "proof_status": "LOCAL_GR_NOT_DERIVED",
            "missing_for_unconditional": "MISSING_PARENT_GRAMMAR_AND_PPN_RESIDUAL_ZERO",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def derivation_attempt() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "TGA1868_0_define_grammar",
            "attempt": "write a parent grammar with primitives, derived compatibility objects, operator permissions, and descent rules",
            "result": "GRAMMAR_CONTRACT_WRITTEN",
            "obstruction": "CONTRACT_NOT_DERIVATION",
            "technical_reason": "A grammar can be proposed consistently, but the current corpus has not derived why this grammar is mandatory from motion/time/space primitives.",
            "next_action": "seek a parent category principle or accept finite coefficient branch.",
            "proof_closed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "TGA1868_1_type_exclusion_test",
            "attempt": "prove type alone forbids Z_R",
            "result": "TYPE_ALONE_TOO_WEAK",
            "obstruction": "COFRAME_DERIVATIVE_COUNTERMODEL",
            "technical_reason": "Even if R_AB is derived from T and S, a general local coframe action can contain derivative invariants whose radial reduction depends on derivatives of ln(T sqrt(S)).",
            "next_action": "need a stronger category principle, quotient invariance, or auxiliary constraint.",
            "proof_closed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "TGA1868_2_auxiliary_route_test",
            "attempt": "make Lambda_R C_R the parent-owned constrained route",
            "result": "EXACT_IF_PARENT_OWNED",
            "obstruction": "LAMBDA_PARENT_ORIGIN_STILL_UNSIGNED",
            "technical_reason": "Variation gives C_R=0 exactly, but this is still an inserted closure unless Lambda_R is forced by the parent grammar and preserved by the Hamiltonian/boundary/matter chain.",
            "next_action": "derive Lambda_R as a parent auxiliary or demote to closure.",
            "proof_closed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "TGA1868_3_matter_boundary_test",
            "attempt": "derive J_R=0 and Q_R=0 from descent",
            "result": "DESCENT_NOT_SIGNED",
            "obstruction": "MISSING_MATTER_BOUNDARY_READOUT_SILENCE",
            "technical_reason": "Without universal descent and boundary class, direct source and exterior charge countermodels remain legal.",
            "next_action": "separate boundary no-charge theorem or finite source rows.",
            "proof_closed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "TGA1868_4_verdict",
            "attempt": "derive typed parent grammar for radial-cell compatibility",
            "result": "TYPED_PARENT_GRAMMAR_NOT_DERIVED_CURRENT_CORPUS",
            "obstruction": "MISSING_PARENT_CATEGORY_PRINCIPLE_AND_DESCENT",
            "technical_reason": "The exact conditional theorem is now written, but every nontrivial hypothesis is still a contract rather than a parent-signed result.",
            "next_action": "switch to coefficient-bound branch unless a new parent category principle is supplied.",
            "proof_closed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def coefficient_bound_branch() -> list[dict[str, Any]]:
    rows = [
        ("CBB1868_0_ZR", "Z_R", "gradient stiffness", "derive coefficient or bound it from local fifth-force/PPN behavior", "MISSING_NUMERIC_PARENT_COEFFICIENT"),
        ("CBB1868_1_MR2", "M_R^2", "mass/stiffness scale", "derive ell_R=sqrt(Z_R/M_R^2) or bound scale separation", "MISSING_NUMERIC_PARENT_COEFFICIENT"),
        ("CBB1868_2_JR", "J_R", "direct matter source", "derive matter descent zero or bound source coupling", "MISSING_MATTER_SOURCE_COEFFICIENT"),
        ("CBB1868_3_BR", "B_R", "boundary/corner term", "derive no-charge boundary class or bound surface charge", "MISSING_BOUNDARY_CLASS"),
        ("CBB1868_4_QR", "Q_R", "exterior reciprocal hair", "derive Q_R=0 or bound from local/orbital residuals", "MISSING_NO_CHARGE_THEOREM"),
        ("CBB1868_5_tau_R10", "tau_R10", "short-range projection", "map finite reciprocal branch to alpha(lambda)", "MISSING_ARENA_PROJECTION"),
        ("CBB1868_6_tau_PPN", "tau_PPN", "post-Newtonian projection", "map C_R residual to gamma/beta/light-time observables", "MISSING_ARENA_PROJECTION"),
        ("CBB1868_7_tau_clock", "tau_clock", "clock/redshift projection", "map residual to fractional frequency/redshift", "MISSING_ARENA_PROJECTION"),
        ("CBB1868_8_tau_orbital", "tau_orbital", "orbital projection", "map residual to precession/acceleration anomalies", "MISSING_ARENA_PROJECTION"),
        ("CBB1868_9_SR_total", "S_R_total", "total D_R source side", "assemble q_loc, matter, boundary, readout, current and reciprocal slots", "MISSING_SOURCE_MAP"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "bound_row_id": row_id,
            "coefficient_or_projection": coefficient,
            "role": role,
            "next_required_work": next_required,
            "status": status,
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "units": "MISSING_UNITS_OR_NORMALIZATION",
            "claim_ready": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        }
        for row_id, coefficient, role, next_required, status in rows
    ]


def claim_gate() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1868_0_typed_grammar",
            "claim": "typed parent grammar is derived",
            "status": "BLOCKED",
            "blocking_reason": "MISSING_PARENT_CATEGORY_PRINCIPLE",
            "required_before_claim": "derive primitive list, constructor permissions, and category exclusion from parent motion/time/space principle.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1868_1_ZR_JR_zero",
            "claim": "Z_R=0 and J_R=0 are theorem zeros",
            "status": "BLOCKED",
            "blocking_reason": "DERIVATIVE_PERMISSION_AND_MATTER_DESCENT_NOT_SIGNED",
            "required_before_claim": "prove R_AB cannot carry derivative terms and matter cannot source it directly.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1868_2_QR_zero",
            "claim": "Q_R=0 is a boundary theorem",
            "status": "BLOCKED",
            "blocking_reason": "MISSING_BOUNDARY_NO_CHARGE_THEOREM",
            "required_before_claim": "prove boundary/corner class forbids reciprocal flux.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1868_3_local_GR",
            "claim": "MTS derives local GR/Newton branch",
            "status": "BLOCKED",
            "blocking_reason": "TYPED_PARENT_GRAMMAR_NOT_DERIVED_CURRENT_CORPUS",
            "required_before_claim": "close typed grammar, no-charge, matter descent, and PPN residual zero.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1868_4_finite_bounds",
            "claim": "finite coefficient branch passes local tests",
            "status": "BLOCKED",
            "blocking_reason": "MISSING_NUMERIC_COEFFICIENTS_AND_ARENA_PROJECTIONS",
            "required_before_claim": "source numeric rows and run R10/PPN/clock/orbital projections.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1868_0_result",
            "decision": "TYPED_PARENT_GRAMMAR_NOT_DERIVED_CURRENT_CORPUS",
            "basis": "type exclusion is coherent but type alone cannot forbid coframe derivative countermodels.",
            "consequence": "do not claim Z_R/J_R/Q_R theorem zeros.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1868_1_conditional_win",
            "decision": "CONDITIONAL_GRAMMAR_THEOREM_READY",
            "basis": "if parent category principle, auxiliary constraint, matter descent, and boundary silence are signed, C_R=0 follows cleanly.",
            "consequence": "future derivation has exact hypotheses instead of a vague plateau axiom.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1868_2_practical_route",
            "decision": "COEFFICIENT_BOUND_BRANCH_SELECTED_NEXT",
            "basis": "without a new parent category principle, the honest progress route is to source or bound Z_R, M_R^2, J_R, Q_R, and arena projections.",
            "consequence": "move from pure derivation attempt to finite local-bound branch while preserving the conditional theorem.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1868_0_primary",
            "target_doc": "1869-Y5-R2FR-finite-local-coefficient-bound-branch-setup.md",
            "target_script": "scripts/Y5_R2FR_finite_local_coefficient_bound_branch_setup_1869.py",
            "objective": "build the finite local coefficient branch for Z_R, M_R^2, J_R, B_R, Q_R, S_R and R10/PPN/clock/orbital projections without claiming a pass.",
            "selection_status": "selected",
            "success_condition": "all finite local residual coefficients/projections are represented as sourced-or-missing rows with claim gates and runner-ready schema.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1868_1_theory_parallel",
            "target_doc": "1869b-Y5-R2FR-parent-category-principle-for-compatibility-objects.md",
            "target_script": "scripts/Y5_R2FR_parent_category_principle_for_compatibility_objects_1869b.py",
            "objective": "attempt a deeper parent principle that makes compatibility objects non-dynamical rather than ordinary scalars.",
            "selection_status": "held_parallel",
            "success_condition": "new parent category principle signs the grammar or fails explicitly.",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_fields = {
        "valid_for_claim",
        "claim_allowed",
        "claim_ready",
        "proof_closed",
        "gate_closed",
        "passes_claim_gate",
    }
    for rows in rows_by_name.values():
        for table_row in rows:
            for field_name in claim_fields:
                if str(table_row.get(field_name, "")).strip().lower() == "true":
                    return False
    return True


def missing_rows_not_ready(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for table_row in rows:
            contains_missing = any("MISSING_" in str(value) for value in table_row.values())
            if contains_missing:
                if str(table_row.get("valid_for_claim", "")).strip().lower() == "true":
                    return False
                if str(table_row.get("claim_allowed", "")).strip().lower() == "true":
                    return False
                if str(table_row.get("claim_ready", "")).strip().lower() == "true":
                    return False
    return True


def csvs_parse(paths: list[Path]) -> bool:
    for csv_path in paths:
        with csv_path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
    return True


def copy_branch_outputs(paths: list[Path]) -> None:
    for branch_folder in (MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE):
        branch_folder.mkdir(parents=True, exist_ok=True)
    for output_path in paths:
        shutil.copy2(output_path, MICROSCOPE_RESIDUALS / output_path.name)
        shutil.copy2(output_path, QUARANTINE / output_path.name)
        shutil.copy2(output_path, RAB_QUEUE / f"JR1868_{output_path.name}")


def branch_copies_exist(paths: list[Path]) -> bool:
    for output_path in paths:
        expected_paths = [
            MICROSCOPE_RESIDUALS / output_path.name,
            QUARANTINE / output_path.name,
            RAB_QUEUE / f"JR1868_{output_path.name}",
        ]
        if not all(expected_path.exists() for expected_path in expected_paths):
            return False
    return True


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1868*"))


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], non_validation_paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    grammar_rows = rows_by_name["candidate_parent_grammar"]
    legality_rows = rows_by_name["term_legality_matrix"]
    theorem_rows = rows_by_name["conditional_theorem"]
    attempt_rows = rows_by_name["derivation_attempt"]
    coefficient_rows = rows_by_name["coefficient_bound_branch"]
    claim_rows = rows_by_name["claim_gate"]
    decision_rows = rows_by_name["decision_ledger"]
    next_rows = rows_by_name["next_target"]

    checks = [
        {
            "validation_id": "VAL1868_0_sources_exist",
            "status": "PASS" if all(row["path_exists"] == "True" for row in source_rows) else "FAIL",
            "detail": "all cited source paths exist",
        },
        {
            "validation_id": "VAL1868_1_needles_present",
            "status": "PASS" if all(row["needle_found"] == "True" for row in source_rows) else "FAIL",
            "detail": "all cited source needles are present",
        },
        {
            "validation_id": "VAL1868_2_grammar_contract_written",
            "status": "PASS" if len(grammar_rows) >= 6 and any(row["status"] == "MISSING_PARENT_CATEGORY_PRINCIPLE" for row in grammar_rows) else "FAIL",
            "detail": "candidate grammar names the category-principle blocker",
        },
        {
            "validation_id": "VAL1868_3_legality_matrix_blocks_claim",
            "status": "PASS" if any(row["status_current_corpus"] == "LEGAL_COUNTERMODEL_IF_NOT_SIGNED" for row in legality_rows) else "FAIL",
            "detail": "legality matrix keeps countermodels alive until grammar is signed",
        },
        {
            "validation_id": "VAL1868_4_conditional_theorem_only",
            "status": "PASS" if any(row["proof_status"] == "CONDITIONAL_THEOREM_ONLY" for row in theorem_rows) else "FAIL",
            "detail": "local reciprocity theorem remains conditional",
        },
        {
            "validation_id": "VAL1868_5_derivation_not_closed",
            "status": "PASS" if any(row["result"] == "TYPED_PARENT_GRAMMAR_NOT_DERIVED_CURRENT_CORPUS" for row in attempt_rows) else "FAIL",
            "detail": "typed grammar derivation is not promoted",
        },
        {
            "validation_id": "VAL1868_6_coefficient_branch_ready_nonclaim",
            "status": "PASS" if len(coefficient_rows) >= 10 and all(row["valid_for_claim"] == "False" for row in coefficient_rows) else "FAIL",
            "detail": "coefficient-bound branch rows are present and nonclaim",
        },
        {
            "validation_id": "VAL1868_7_claim_gates_blocked",
            "status": "PASS" if all(row["status"] == "BLOCKED" for row in claim_rows) else "FAIL",
            "detail": "all typed-grammar/local-test claim gates remain blocked",
        },
        {
            "validation_id": "VAL1868_8_no_claim_flags",
            "status": "PASS" if all_claim_flags_false(rows_by_name) else "FAIL",
            "detail": "no generated claim or gate-pass flag is true",
        },
        {
            "validation_id": "VAL1868_9_missing_not_ready",
            "status": "PASS" if missing_rows_not_ready(rows_by_name) else "FAIL",
            "detail": "no MISSING_* row is marked claim-ready",
        },
        {
            "validation_id": "VAL1868_10_decision_next",
            "status": "PASS" if any(row["decision"] == "COEFFICIENT_BOUND_BRANCH_SELECTED_NEXT" for row in decision_rows) else "FAIL",
            "detail": "decision ledger selects finite coefficient-bound branch next",
        },
        {
            "validation_id": "VAL1868_11_next_selected",
            "status": "PASS" if any(row["route_id"] == "NEXT1868_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL",
            "detail": "next target selected",
        },
        {
            "validation_id": "VAL1868_12_csv_parse",
            "status": "PASS" if csvs_parse(non_validation_paths) else "FAIL",
            "detail": "all generated non-validation CSVs parse",
        },
        {
            "validation_id": "VAL1868_13_branch_copies",
            "status": "PASS" if branch_copies_exist(non_validation_paths) else "FAIL",
            "detail": "branch/quarantine/queue copies exist",
        },
        {
            "validation_id": "VAL1868_14_pycache_absent",
            "status": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent",
        },
        {
            "validation_id": "VAL1868_15_formalization_untouched",
            "status": "PASS" if formalization_untouched() else "FAIL",
            "detail": "no 1868 outputs found under formalization-workbench",
        },
    ]
    overall_status = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "validation_id": "VAL1868_OVERALL",
            "status": overall_status,
            "detail": "1868 typed parent grammar or coefficient-bound branch checkpoint",
        }
    )
    return [{**row, "branch_id": BRANCH_ID, "valid_for_claim": as_bool_text(False)} for row in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1868 - Y5/R2FR Typed Parent Grammar For Radial Cell Or Coefficient-Bound Branch",
        "",
        "## Verdict",
        "",
        "1868 writes the exact conditional theorem we wanted, but it does not close it. If the parent language can prove that `R_AB=C_R=ln(T^2 S)` is only radial-cell compatibility data, and if `Lambda_R C_R` is a parent-owned auxiliary constraint with silent matter/boundary/readout descent, then `C_R=0`, `Z_R=0`, `J_R=0`, and no reciprocal hair follow cleanly. That would be the elegant route to the local-GR branch.",
        "",
        "The current corpus does not yet derive the category principle. Type alone is too weak: a general local coframe action can contain derivative invariants whose radial reduction depends on derivatives of `ln(T sqrt(S))`, which is effectively a `Z_R` countermodel unless the parent grammar forbids it. So the honest next move is to preserve the conditional theorem but build the finite coefficient-bound branch.",
        "",
        "**Claim ceiling:** no typed-grammar theorem, no `Z_R=0`, no `J_R=0`, no `Q_R=0`, no local-GR/Newton reduction claim, no finite-bound pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1868.",
        "",
        "## Source Register",
        "",
        markdown_table(
            rows_by_name["source_register"],
            ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_1868", "valid_for_claim"],
        ),
        "",
        "## Candidate Parent Grammar",
        "",
        markdown_table(
            rows_by_name["candidate_parent_grammar"],
            ["grammar_id", "grammar_layer", "candidate_rule", "derivation_value", "failure_mode", "status", "valid_for_claim"],
        ),
        "",
        "## Term Legality Matrix",
        "",
        markdown_table(
            rows_by_name["term_legality_matrix"],
            ["term_id", "term", "status_if_grammar_signed", "status_current_corpus", "interpretation", "claim_allowed", "valid_for_claim"],
        ),
        "",
        "## Conditional Grammar Theorem",
        "",
        markdown_table(
            rows_by_name["conditional_theorem"],
            ["theorem_id", "theorem_piece", "statement", "proof_status", "missing_for_unconditional", "claim_allowed", "valid_for_claim"],
        ),
        "",
        "## Typed Grammar Derivation Attempt",
        "",
        markdown_table(
            rows_by_name["derivation_attempt"],
            ["attempt_id", "attempt", "result", "obstruction", "technical_reason", "next_action", "proof_closed", "valid_for_claim"],
        ),
        "",
        "## Coefficient-Bound Branch",
        "",
        markdown_table(
            rows_by_name["coefficient_bound_branch"],
            ["bound_row_id", "coefficient_or_projection", "role", "next_required_work", "status", "numeric_value", "source_path", "claim_ready", "valid_for_claim"],
        ),
        "",
        "## Claim Gate",
        "",
        markdown_table(
            rows_by_name["claim_gate"],
            ["claim_id", "claim", "status", "blocking_reason", "required_before_claim", "claim_allowed", "valid_for_claim"],
        ),
        "",
        "## Decision Ledger",
        "",
        markdown_table(
            rows_by_name["decision_ledger"],
            ["decision_id", "decision", "basis", "consequence", "claim_allowed", "valid_for_claim"],
        ),
        "",
        "## Next Target",
        "",
        markdown_table(
            rows_by_name["next_target"],
            ["route_id", "target_doc", "target_script", "objective", "selection_status", "success_condition", "valid_for_claim"],
        ),
        "",
        "## Validation",
        "",
        markdown_table(
            rows_by_name["validation"],
            ["validation_id", "status", "detail", "valid_for_claim"],
        ),
        "",
        "## Plain-English Status",
        "",
        "This is the cleanest possible failure of the derivation-first attack: we found the exact theorem, then found the exact place it still needs a parent principle. That is not grim; it is disciplined. The local-GR route now has two honest lanes: either discover the deeper category principle that makes compatibility objects non-dynamical, or treat `Z_R/M_R^2/J_R/Q_R` as finite residual coefficients and make them survive local tests.",
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "candidate_parent_grammar": candidate_parent_grammar(),
        "term_legality_matrix": term_legality_matrix(),
        "conditional_theorem": conditional_theorem(),
        "derivation_attempt": derivation_attempt(),
        "coefficient_bound_branch": coefficient_bound_branch(),
        "claim_gate": claim_gate(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
    }

    non_validation_paths = [path for name, path in OUTPUTS.items() if name != "validation"]
    for output_name, output_path in OUTPUTS.items():
        if output_name != "validation":
            write_csv(output_path, rows_by_name[output_name])

    copy_branch_outputs(non_validation_paths)
    remove_pycache()
    rows_by_name["validation"] = validation_rows(rows_by_name, non_validation_paths)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    copy_branch_outputs([OUTPUTS["validation"]])
    remove_pycache()


if __name__ == "__main__":
    main()

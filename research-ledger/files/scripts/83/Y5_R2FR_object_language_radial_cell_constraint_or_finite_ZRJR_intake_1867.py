from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1867"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1867-Y5-R2FR-object-language-radial-cell-constraint-or-finite-ZRJR-intake.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1867_SOURCE_REGISTER.csv",
    "typed_object_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1867_TYPED_OBJECT_CONTRACT.csv",
    "object_language_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1867_OBJECT_LANGUAGE_DERIVATION_ATTEMPT.csv",
    "countermodel_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1867_COUNTERMODEL_AUDIT.csv",
    "finite_intake": RESIDUALS / "P8_Y5_PARENT_QLOC_1867_FINITE_ZRJR_INTAKE_ROWS.csv",
    "no_smuggling_guard": RESIDUALS / "P8_Y5_PARENT_QLOC_1867_NO_SMUGGLING_GUARD.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1867_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1867_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1867_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1867_VALIDATION.csv",
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
            "source_id": "SRC1867_0_1866_doc",
            "source_kind": "current_handoff",
            "source_path": ROOT / "1866-Y5-R2FR-reciprocity-selector-operator-or-Hcore-source-equation.md",
            "required_needle": "NEXT1866_0_primary",
            "use_in_1867": "selects the object-language radial-cell constraint route.",
        },
        {
            "source_id": "SRC1867_1_1866_validation",
            "source_kind": "validation_anchor",
            "source_path": RESIDUALS / "P8_Y5_BRR545_1866_VALIDATION.csv",
            "required_needle": "VAL1866_OVERALL",
            "use_in_1867": "confirms the selector/Hcore gate passed before this attempt.",
        },
        {
            "source_id": "SRC1867_2_1866_finite",
            "source_kind": "finite_requirement_seed",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1866_FINITE_ZRJR_REQUIREMENTS.csv",
            "required_needle": "FZR1866_0_ZR",
            "use_in_1867": "imports the fallback source rows if the object-language proof fails.",
        },
        {
            "source_id": "SRC1867_3_1274_unimodular",
            "source_kind": "unimodular_cell_origin_audit",
            "source_path": RESIDUALS / "P8_Y5_R10_1274_UNIMODULAR_CELL_ORIGIN_AUDIT.csv",
            "required_needle": "URO1274_5_verdict",
            "use_in_1867": "states that radial-cell unimodularity works only if parent-signed.",
        },
        {
            "source_id": "SRC1867_4_1272_variational",
            "source_kind": "radial_cell_variational_attempt",
            "source_path": RESIDUALS / "P8_Y5_R10_1272_RADIAL_CELL_VARIATIONAL_DERIVATION_ATTEMPT.csv",
            "required_needle": "RCD1272_7_verdict",
            "use_in_1867": "records that radial-cell necessity is not yet derived.",
        },
        {
            "source_id": "SRC1867_5_1272_matrix",
            "source_kind": "cell_principle_test_matrix",
            "source_path": RESIDUALS / "P8_Y5_R10_1272_CELL_PRINCIPLE_TEST_MATRIX.csv",
            "required_needle": "CPT1272_5_constrained_action",
            "use_in_1867": "compares constrained action against Liouville/current/gauge alternatives.",
        },
        {
            "source_id": "SRC1867_6_1273_uv",
            "source_kind": "u_v_variable_split",
            "source_path": RESIDUALS / "P8_Y5_R10_1273_UV_RADIAL_CELL_VARIABLE_CHANGE.csv",
            "required_needle": "UV1273_0_u_cell_volume",
            "use_in_1867": "supplies u=ln(J_q)=R_AB/2 as the object-language target.",
        },
        {
            "source_id": "SRC1867_7_1257_selector",
            "source_kind": "ZR_lambda_selector_clause",
            "source_path": RESIDUALS / "P8_Y5_R10_1257_ZR_LAMBDAR_SELECTOR_CLAUSES.csv",
            "required_needle": "SEL1257_0_field_exclusion",
            "use_in_1867": "states the conditional field-exclusion clause.",
        },
        {
            "source_id": "SRC1867_8_1622_object_language",
            "source_kind": "lambdaR_object_language_audit",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1622_LAMBDAR_PARENT_ORIGIN_AUDIT.csv",
            "required_needle": "ORG1622_3_object_language",
            "use_in_1867": "documents that the typed constructor list has not yet been parent-derived.",
        },
        {
            "source_id": "SRC1867_9_1859_no_GR",
            "source_kind": "no_GR_import_route",
            "source_path": ROOT / "1859-Y5-R2FR-motion-load-phase-volume-parent-origin-no-GR-import-derivation.md",
            "required_needle": "BEST_NONCIRCULAR_ROUTE",
            "use_in_1867": "keeps field-equation derivation separate from closure imposition.",
        },
        {
            "source_id": "SRC1867_10_07_nonprop",
            "source_kind": "nonpropagating_constraint_note",
            "source_path": ROOT / "07-nonpropagating-reciprocity-constraint.md",
            "required_needle": "nonpropagating_reciprocity_constraint_clean_but_parent_origin_open",
            "use_in_1867": "shows the algebraic nonpropagating route is clean but parent origin is open.",
        },
        {
            "source_id": "SRC1867_11_12_noether",
            "source_kind": "gauge_noether_origin_audit",
            "source_path": ROOT / "12-gauge-noether-origin-audit.md",
            "required_needle": "gauge_noether_origin_not_derived_closure_only",
            "use_in_1867": "prevents replacing parent object-language with a bare Noether slogan.",
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
                "use_in_1867": source_entry["use_in_1867"],
                "valid_for_claim": as_bool_text(False),
            }
        )
    return rows


def typed_object_contract() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": "TOC1867_0_primitives",
            "object_language_clause": "parent primitives must be declared before local metric readout",
            "proposed_content": "motion/time/space coframe or routing primitives; connection/transport primitives; matter fields; allowed measures.",
            "why_needed": "without typed primitives, R_AB can be reintroduced as an ordinary scalar by locality.",
            "current_status": "MISSING_PARENT_PRIMITIVE_LIST",
            "would_close": "no; prerequisite only",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "TOC1867_1_derived_cell",
            "object_language_clause": "radial cell-volume mode is derived compatibility data",
            "proposed_content": "J_q=T sqrt(S), u=ln(J_q), C_R=R_AB=2u.",
            "why_needed": "makes the target exact before choosing dynamics.",
            "current_status": "DEFINITION_EXACT_NOT_DYNAMICS",
            "would_close": "no; it defines the object but does not forbid dynamics.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "TOC1867_2_forbid_independent_RAB",
            "object_language_clause": "R_AB cannot be an independent action variable",
            "proposed_content": "R_AB may appear only inside compatibility constraints or auxiliary elimination equations, not as a field with its own variations.",
            "why_needed": "this is the exact rule that would forbid Z_R and generic J_R.",
            "current_status": "PROPOSED_RULE_NOT_PARENT_SIGNED",
            "would_close": "yes, if derived from parent grammar and stable under matter/readout.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "TOC1867_3_forbid_derivatives",
            "object_language_clause": "no D_i R_AB D^i R_AB term",
            "proposed_content": "derivatives act on parent primitives or curvature/transport objects, not on the compatibility scalar itself.",
            "why_needed": "forbids reciprocal hair and fifth-force kinetic leakage.",
            "current_status": "CONDITIONAL_ON_TOC1867_2",
            "would_close": "yes only after the independent-R_AB exclusion is signed.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "TOC1867_4_matter_descent",
            "object_language_clause": "matter couples to parent coframe/readout, not directly to R_AB",
            "proposed_content": "J_R=0 follows only if matter action descends through the allowed primitives without a direct reciprocal source slot.",
            "why_needed": "prevents local sources from shifting the constraint and reintroducing finite residuals.",
            "current_status": "MISSING_MATTER_DESCENT_PROOF",
            "would_close": "partially; still needs boundary/readout no-hair.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "TOC1867_5_boundary_readout",
            "object_language_clause": "boundary and readout cannot revive Q_R/R_AB hair",
            "proposed_content": "boundary terms and observer maps respect eliminated compatibility data.",
            "why_needed": "without this, an exact bulk constraint may still leak through boundary/corner data.",
            "current_status": "MISSING_BOUNDARY_READOUT_SILENCE",
            "would_close": "partially; must combine with Dirac/auxiliary closure.",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def object_language_attempt() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "OLA1867_0_definition",
            "attempt": "identify the radial-cell object",
            "derivation_step": "From the local observer coframe, J_q=T sqrt(S), so C_R=ln(T^2 S)=2 ln(J_q).",
            "result": "EXACT_IDENTITY",
            "obstruction": "NONE_AS_DEFINITION",
            "consequence": "the target object is unambiguous.",
            "proof_closed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "OLA1867_1_type_claim",
            "attempt": "type C_R as compatibility data rather than a scalar field",
            "derivation_step": "Demand that C_R measures consistency of time-capacity and radial-routing cells, not an extra physical degree of freedom.",
            "result": "PHYSICALLY_COHERENT_CONTRACT",
            "obstruction": "MISSING_PARENT_OBJECT_LANGUAGE_AXIOMS",
            "consequence": "this is the right-looking theory sentence, but it is not yet a derivation.",
            "proof_closed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "OLA1867_2_derivative_exclusion",
            "attempt": "forbid Z_R by grammar",
            "derivation_step": "If C_R is compatibility data, D_i C_R D^i C_R is a category error rather than a small coefficient.",
            "result": "CONDITIONAL_ZERO_OF_ZR",
            "obstruction": "CATEGORY_RULE_NOT_PARENT_SIGNED",
            "consequence": "Z_R=0 is available only as a conditional theorem.",
            "proof_closed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "OLA1867_3_source_exclusion",
            "attempt": "forbid J_R by matter descent",
            "derivation_step": "If matter couples only to the descended coframe and not the compatibility scalar, direct J_R vanishes.",
            "result": "CONDITIONAL_ZERO_OF_JR",
            "obstruction": "MATTER_DESCENT_NOT_SIGNED",
            "consequence": "J_R=0 cannot be claimed yet.",
            "proof_closed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "OLA1867_4_auxiliary_elimination",
            "attempt": "use a second-class auxiliary block",
            "derivation_step": "A parent-owned Lambda_R C_R block would eliminate C_R before readout, with lambda_R fixed by the companion equation.",
            "result": "BEST_CONDITIONAL_EXACT_ROUTE",
            "obstruction": "LAMBDA_ORIGIN_DIRAC_BOUNDARY_NOT_SIGNED",
            "consequence": "keep as closure mechanism, not current theorem.",
            "proof_closed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "OLA1867_5_verdict",
            "attempt": "derive object-language radial-cell constraint",
            "derivation_step": "Definitions are exact and the category route is coherent, but no parent primitive list/constructor grammar forces the category rule.",
            "result": "OBJECT_LANGUAGE_CONSTRAINT_NOT_DERIVED_CURRENT_CORPUS",
            "obstruction": "MISSING_TYPED_PARENT_GRAMMAR",
            "consequence": "demote to exact contract; keep finite Z_R/J_R intake live.",
            "proof_closed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def countermodel_audit() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CMA1867_0_locality_scalar",
            "countermodel": "admit R_AB as an ordinary scalar/strain variable under locality",
            "allowed_term_if_not_forbidden": "1/2 Z_R h^ij D_i R_AB D_j R_AB",
            "damage": "reciprocal exterior hair and local fifth-force style residuals become legal.",
            "why_it_survives": "no signed parent grammar forbids independent R_AB.",
            "status": "COUNTERMODEL_SURVIVES",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CMA1867_1_source_scalar",
            "countermodel": "matter descent includes a direct reciprocal source",
            "allowed_term_if_not_forbidden": "J_R R_AB",
            "damage": "local matter shifts C_R away from zero even if a mass/stiffness suppresses it.",
            "why_it_survives": "no universal matter-descent proof has removed J_R.",
            "status": "COUNTERMODEL_SURVIVES",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CMA1867_2_boundary_charge",
            "countermodel": "boundary class permits reciprocal flux",
            "allowed_term_if_not_forbidden": "B_R or Q_R surface charge",
            "damage": "bulk zero/source equation can still carry exterior reciprocal hair.",
            "why_it_survives": "no boundary/corner no-charge theorem is signed.",
            "status": "COUNTERMODEL_SURVIVES",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CMA1867_3_gauge_slogan",
            "countermodel": "call C_R=0 a gauge choice",
            "allowed_term_if_not_forbidden": "observer readout hides the reciprocal mode",
            "damage": "the proof becomes circular because local metric readout is fixed by the desired result.",
            "why_it_survives": "Noether/gauge audit says a symmetry can preserve a constraint but cannot conjure it.",
            "status": "REJECT_AS_DERIVATION_SHORTCUT",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def finite_intake() -> list[dict[str, Any]]:
    intake_rows = [
        (
            "FINT1867_0_ZR",
            "Z_R",
            "gradient stiffness of reciprocal cell mode",
            "source parent H_core coefficient or prove category-forbidden",
            "MISSING_PARENT_INPUT",
        ),
        (
            "FINT1867_1_MR2",
            "M_R^2",
            "mass/stiffness suppressing reciprocal residual",
            "source parent potential/auxiliary coefficient or prove absent",
            "MISSING_PARENT_INPUT",
        ),
        (
            "FINT1867_2_JR",
            "J_R",
            "direct matter/source drive of reciprocal mode",
            "source matter descent map or prove direct source forbidden",
            "MISSING_PARENT_INPUT",
        ),
        (
            "FINT1867_3_BR",
            "B_R",
            "boundary/corner reciprocal term",
            "source boundary variational class or prove no-charge",
            "MISSING_BOUNDARY_INPUT",
        ),
        (
            "FINT1867_4_QR",
            "Q_R",
            "exterior reciprocal charge/hair",
            "derive no-charge theorem or source finite charge row",
            "MISSING_BOUNDARY_INPUT",
        ),
        (
            "FINT1867_5_SR_total",
            "S_R_total",
            "full source side of D_R=partial_r C_R-S_R",
            "combine q_loc, matter, boundary, readout, and current coefficients",
            "MISSING_SOURCE_MAP",
        ),
        (
            "FINT1867_6_tau_R10",
            "tau_R10",
            "short-range fifth-force projection",
            "map finite R_AB residual to alpha(lambda) style bounds",
            "MISSING_ARENA_PROJECTION",
        ),
        (
            "FINT1867_7_tau_PPN",
            "tau_PPN",
            "post-Newtonian residual vector",
            "map finite C_R/R_AB residual to gamma, beta, light-deflection, Shapiro terms",
            "MISSING_ARENA_PROJECTION",
        ),
        (
            "FINT1867_8_tau_clock",
            "tau_clock",
            "clock/redshift projection",
            "map reciprocal residual to fractional frequency/redshift residual",
            "MISSING_ARENA_PROJECTION",
        ),
        (
            "FINT1867_9_tau_orbital",
            "tau_orbital",
            "orbital/precession projection",
            "map reciprocal residual to acceleration and precession anomalies",
            "MISSING_ARENA_PROJECTION",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for intake_id, coefficient, role, needed_source, status in intake_rows:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "intake_id": intake_id,
                "coefficient_or_projection": coefficient,
                "role": role,
                "needed_source": needed_source,
                "status": status,
                "numeric_value": "MISSING_NUMERIC_VALUE",
                "source_path": "MISSING_SOURCE_PATH",
                "units": "MISSING_UNITS_OR_NORMALIZATION",
                "claim_ready": as_bool_text(False),
                "valid_for_claim": as_bool_text(False),
            }
        )
    return rows


def no_smuggling_guard() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "guard_id": "NSG1867_0_no_category_postulate_as_proof",
            "forbidden_move": "declare R_AB non-independent without a parent object grammar",
            "why_forbidden": "that is the exact point under test.",
            "allowed_move": "write the grammar as a contract and keep the claim blocked.",
            "guard_status": "ACTIVE_BLOCK",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "guard_id": "NSG1867_1_no_unimodular_axiom_as_derivation",
            "forbidden_move": "impose J_q=1 and call it derived",
            "why_forbidden": "unimodular radial-cell condition works algebraically but is closure-only unless parent-signed.",
            "allowed_move": "derive it from primitives or label it closure.",
            "guard_status": "ACTIVE_BLOCK",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "guard_id": "NSG1867_2_no_gauge_slogan",
            "forbidden_move": "use gauge/Noether language to create R_AB=0 from nothing",
            "why_forbidden": "Noether identities relate owned equations; they do not create the missing constraint.",
            "allowed_move": "construct the constrained parent action first.",
            "guard_status": "ACTIVE_BLOCK",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "guard_id": "NSG1867_3_no_local_test_claim",
            "forbidden_move": "treat finite coefficient intake as a pass of local tests",
            "why_forbidden": "all rows are source-ready placeholders until numeric parent coefficients and projections exist.",
            "allowed_move": "use intake rows only to plan data-bound work.",
            "guard_status": "ACTIVE_BLOCK",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def claim_gate() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1867_0_object_language",
            "claim": "C_R/R_AB is proven to be parent compatibility data",
            "status": "BLOCKED",
            "blocking_reason": "MISSING_TYPED_PARENT_GRAMMAR",
            "required_before_claim": "explicit primitive list, constructors, allowed derivatives, matter descent, and boundary/readout silence.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1867_1_ZR_zero",
            "claim": "Z_R=0 is derived rather than chosen",
            "status": "BLOCKED",
            "blocking_reason": "R_AB_INDEPENDENCE_NOT_EXCLUDED",
            "required_before_claim": "category proof that derivative terms on R_AB are illegal.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1867_2_JR_zero",
            "claim": "J_R=0 follows from matter descent",
            "status": "BLOCKED",
            "blocking_reason": "MISSING_MATTER_DESCENT_PROOF",
            "required_before_claim": "universal matter coupling/readout map with no direct reciprocal source.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1867_3_local_GR",
            "claim": "local GR/Newton branch is derived",
            "status": "BLOCKED",
            "blocking_reason": "OBJECT_LANGUAGE_CONSTRAINT_NOT_DERIVED_CURRENT_CORPUS",
            "required_before_claim": "C_R=0 plus Q_R=0 plus PPN residual zero from parent grammar.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1867_0_result",
            "decision": "OBJECT_LANGUAGE_CONSTRAINT_NOT_DERIVED_CURRENT_CORPUS",
            "basis": "the exact cell object is defined, but the parent typed grammar that forbids independent R_AB is not present.",
            "consequence": "do not claim Z_R=0, J_R=0, or local GR from object-language alone.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1867_1_best_survivor",
            "decision": "TYPED_PARENT_GRAMMAR_CONTRACT_READY",
            "basis": "the required clauses are now explicit and source-backed.",
            "consequence": "next proof can target the primitive/constructor list directly.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1867_2_fallback",
            "decision": "FINITE_ZRJR_INTAKE_ROWS_READY_NONCLAIM",
            "basis": "countermodels survive unless the category rule is proved.",
            "consequence": "if 1868 cannot sign the grammar, move to sourcing coefficients/projections instead of pretending zero.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1867_0_primary",
            "target_doc": "1868-Y5-R2FR-typed-parent-grammar-for-radial-cell-or-coefficient-bound-branch.md",
            "target_script": "scripts/Y5_R2FR_typed_parent_grammar_for_radial_cell_or_coefficient_bound_branch_1868.py",
            "objective": "try to construct the explicit parent primitive/constructor grammar that makes C_R/R_AB compatibility data; if it fails, switch to finite coefficient/bound branch.",
            "selection_status": "selected",
            "success_condition": "derive category exclusion of independent R_AB and direct J_R, or make the finite local branch fully source-ready.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1867_1_secondary",
            "target_doc": "1868b-Y5-R2FR-boundary-no-charge-theorem-for-reciprocal-hair.md",
            "target_script": "scripts/Y5_R2FR_boundary_no_charge_theorem_for_reciprocal_hair_1868b.py",
            "objective": "attack Q_R=0 separately from boundary/source neutrality.",
            "selection_status": "held_parallel",
            "success_condition": "no-charge theorem or finite Q_R source row.",
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
        "selector_signed",
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
        shutil.copy2(output_path, RAB_QUEUE / f"JR1867_{output_path.name}")


def branch_copies_exist(paths: list[Path]) -> bool:
    for output_path in paths:
        expected_paths = [
            MICROSCOPE_RESIDUALS / output_path.name,
            QUARANTINE / output_path.name,
            RAB_QUEUE / f"JR1867_{output_path.name}",
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
    return not any(FORMALIZATION.rglob("*1867*"))


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], non_validation_paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    contract_rows = rows_by_name["typed_object_contract"]
    attempt_rows = rows_by_name["object_language_attempt"]
    counter_rows = rows_by_name["countermodel_audit"]
    intake_rows = rows_by_name["finite_intake"]
    guard_rows = rows_by_name["no_smuggling_guard"]
    claim_rows = rows_by_name["claim_gate"]
    decision_rows = rows_by_name["decision_ledger"]
    next_rows = rows_by_name["next_target"]

    checks = [
        {
            "validation_id": "VAL1867_0_sources_exist",
            "status": "PASS" if all(row["path_exists"] == "True" for row in source_rows) else "FAIL",
            "detail": "all cited source paths exist",
        },
        {
            "validation_id": "VAL1867_1_needles_present",
            "status": "PASS" if all(row["needle_found"] == "True" for row in source_rows) else "FAIL",
            "detail": "all cited source needles are present",
        },
        {
            "validation_id": "VAL1867_2_contract_complete",
            "status": "PASS" if len(contract_rows) >= 6 and any(row["current_status"] == "MISSING_PARENT_PRIMITIVE_LIST" for row in contract_rows) else "FAIL",
            "detail": "typed object-language contract names primitive-list blocker",
        },
        {
            "validation_id": "VAL1867_3_object_language_not_derived",
            "status": "PASS" if any(row["result"] == "OBJECT_LANGUAGE_CONSTRAINT_NOT_DERIVED_CURRENT_CORPUS" for row in attempt_rows) else "FAIL",
            "detail": "object-language proof remains nonclaim",
        },
        {
            "validation_id": "VAL1867_4_countermodels_survive",
            "status": "PASS" if any(row["status"] == "COUNTERMODEL_SURVIVES" for row in counter_rows) else "FAIL",
            "detail": "ordinary scalar/source/boundary countermodels are recorded",
        },
        {
            "validation_id": "VAL1867_5_finite_intake_nonclaim",
            "status": "PASS" if len(intake_rows) >= 10 and all(row["valid_for_claim"] == "False" for row in intake_rows) else "FAIL",
            "detail": "finite Z_R/J_R/Q_R/S_R intake rows are nonclaim",
        },
        {
            "validation_id": "VAL1867_6_no_smuggling_guards_active",
            "status": "PASS" if all(row["guard_status"] == "ACTIVE_BLOCK" for row in guard_rows) else "FAIL",
            "detail": "category/unimodular/gauge/local-test smuggling guards are active",
        },
        {
            "validation_id": "VAL1867_7_claim_gates_blocked",
            "status": "PASS" if all(row["status"] == "BLOCKED" for row in claim_rows) else "FAIL",
            "detail": "all object-language/local-GR claims remain blocked",
        },
        {
            "validation_id": "VAL1867_8_no_claim_flags",
            "status": "PASS" if all_claim_flags_false(rows_by_name) else "FAIL",
            "detail": "no generated claim or gate-pass flag is true",
        },
        {
            "validation_id": "VAL1867_9_missing_not_ready",
            "status": "PASS" if missing_rows_not_ready(rows_by_name) else "FAIL",
            "detail": "no MISSING_* row is marked claim-ready",
        },
        {
            "validation_id": "VAL1867_10_decision_next",
            "status": "PASS" if any(row["decision"] == "TYPED_PARENT_GRAMMAR_CONTRACT_READY" for row in decision_rows) else "FAIL",
            "detail": "decision ledger selects typed parent grammar next",
        },
        {
            "validation_id": "VAL1867_11_next_selected",
            "status": "PASS" if any(row["route_id"] == "NEXT1867_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL",
            "detail": "next target selected",
        },
        {
            "validation_id": "VAL1867_12_csv_parse",
            "status": "PASS" if csvs_parse(non_validation_paths) else "FAIL",
            "detail": "all generated non-validation CSVs parse",
        },
        {
            "validation_id": "VAL1867_13_branch_copies",
            "status": "PASS" if branch_copies_exist(non_validation_paths) else "FAIL",
            "detail": "branch/quarantine/queue copies exist",
        },
        {
            "validation_id": "VAL1867_14_pycache_absent",
            "status": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent",
        },
        {
            "validation_id": "VAL1867_15_formalization_untouched",
            "status": "PASS" if formalization_untouched() else "FAIL",
            "detail": "no 1867 outputs found under formalization-workbench",
        },
    ]
    overall_status = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "validation_id": "VAL1867_OVERALL",
            "status": overall_status,
            "detail": "1867 object-language radial-cell constraint or finite ZRJR intake checkpoint",
        }
    )
    return [{**row, "branch_id": BRANCH_ID, "valid_for_claim": as_bool_text(False)} for row in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1867 - Y5/R2FR Object-Language Radial-Cell Constraint Or Finite Z_R/J_R Intake",
        "",
        "## Verdict",
        "",
        "1867 tries the cleanest route after 1866: make `C_R/R_AB` a parent object-language compatibility constraint instead of a physical scalar field. The algebra is exact: `J_q=T sqrt(S)`, `u=ln(J_q)`, and `C_R=R_AB=2u`. If a parent grammar proves that this object is compatibility data only, then `Z_R`, direct `J_R`, and ordinary reciprocal hair can be forbidden before readout.",
        "",
        "The current corpus does not yet sign that grammar. The typed contract is now explicit, but the parent primitive list, constructors, derivative permissions, matter descent, boundary silence, and readout stability remain missing. So 1867 does not derive local GR; it sharpens the next theorem and preserves a finite coefficient branch if the theorem fails.",
        "",
        "**Claim ceiling:** no object-language proof, no derived `Z_R=0`, no derived `J_R=0`, no `Q_R=0`, no local-GR/Newton reduction claim, no R10/PPN/clock/orbital pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1867.",
        "",
        "## Source Register",
        "",
        markdown_table(
            rows_by_name["source_register"],
            ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_1867", "valid_for_claim"],
        ),
        "",
        "## Typed Object-Language Contract",
        "",
        markdown_table(
            rows_by_name["typed_object_contract"],
            ["contract_id", "object_language_clause", "current_status", "why_needed", "would_close", "valid_for_claim"],
        ),
        "",
        "## Object-Language Derivation Attempt",
        "",
        markdown_table(
            rows_by_name["object_language_attempt"],
            ["attempt_id", "attempt", "result", "obstruction", "consequence", "proof_closed", "valid_for_claim"],
        ),
        "",
        "## Countermodel Audit",
        "",
        markdown_table(
            rows_by_name["countermodel_audit"],
            ["countermodel_id", "countermodel", "allowed_term_if_not_forbidden", "damage", "why_it_survives", "status", "valid_for_claim"],
        ),
        "",
        "## Finite Z_R/J_R Intake Rows",
        "",
        markdown_table(
            rows_by_name["finite_intake"],
            ["intake_id", "coefficient_or_projection", "role", "needed_source", "status", "numeric_value", "source_path", "claim_ready", "valid_for_claim"],
        ),
        "",
        "## No-Smuggling Guard",
        "",
        markdown_table(
            rows_by_name["no_smuggling_guard"],
            ["guard_id", "forbidden_move", "why_forbidden", "allowed_move", "guard_status", "valid_for_claim"],
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
        "This checkpoint is a useful kind of failure. We now know the clean route is not 'invent a coupling'; it is 'write the parent grammar so the reciprocal cell object is not the kind of thing that can have a kinetic term or direct matter source'. If that grammar can be derived from motion/time/space primitives, local GR becomes a serious derived branch. If it cannot, the honest path is finite residual coefficients and local tests.",
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "typed_object_contract": typed_object_contract(),
        "object_language_attempt": object_language_attempt(),
        "countermodel_audit": countermodel_audit(),
        "finite_intake": finite_intake(),
        "no_smuggling_guard": no_smuggling_guard(),
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

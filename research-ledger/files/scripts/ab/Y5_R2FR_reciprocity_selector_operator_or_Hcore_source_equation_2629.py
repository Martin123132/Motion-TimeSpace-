from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2629-Y5-R2FR-reciprocity-selector-operator-or-Hcore-source-equation.md"

PREFIX = "P8_Y5_SELECTOR_HCORE_2629"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "lineage": RESIDUALS / f"{PREFIX}_LINEAGE_LEDGER.csv",
    "selector_gate": RESIDUALS / f"{PREFIX}_SELECTOR_GATE.csv",
    "hcore_audit": RESIDUALS / f"{PREFIX}_HCORE_SOURCE_EQUATION_AUDIT.csv",
    "object_language": RESIDUALS / f"{PREFIX}_OBJECT_LANGUAGE_GRAMMAR_AUDIT.csv",
    "finite_branch": RESIDUALS / f"{PREFIX}_FINITE_BRANCH_STATUS.csv",
    "normalization": RESIDUALS / f"{PREFIX}_CR_DENOMINATOR_HANDOFF.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2629_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2629_00_2628_handoff",
        "role": "2628 selects reciprocity selector/Hcore source equation",
        "path": ROOT / "2628-Y5-R2FR-constraint-auxiliary-memory-source-elimination-or-residual-interface.md",
        "needles": [
            "DEC2628_3_best_next",
            "RECIPROCITY_SELECTOR_OPERATOR_OR_HCORE_SOURCE_EQUATION_NEXT",
            "DRI2628_2_selector_operator",
        ],
    },
    {
        "source_id": "SRC2629_01_2628_validation",
        "role": "2628 validation pass",
        "path": RESIDUALS / "P8_Y5_BRR545_2628_VALIDATION.csv",
        "needles": ["VAL2628_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC2629_02_1866_selector",
        "role": "selector/Hcore attempt and finite fallback",
        "path": ROOT / "1866-Y5-R2FR-reciprocity-selector-operator-or-Hcore-source-equation.md",
        "needles": [
            "RSA1866_5_verdict",
            "RECIPROCITY_SELECTOR_NOT_DERIVED_CURRENT_CORPUS",
            "HSE1866_0_minimal_density",
        ],
    },
    {
        "source_id": "SRC2629_03_1867_object_language",
        "role": "object-language radial-cell constraint attempt",
        "path": ROOT / "1867-Y5-R2FR-object-language-radial-cell-constraint-or-finite-ZRJR-intake.md",
        "needles": [
            "OLA1867_5_verdict",
            "OBJECT_LANGUAGE_CONSTRAINT_NOT_DERIVED_CURRENT_CORPUS",
            "J_q=T sqrt(S)",
        ],
    },
    {
        "source_id": "SRC2629_04_1868_typed_grammar",
        "role": "typed grammar theorem and countermodel",
        "path": ROOT / "1868-Y5-R2FR-typed-parent-grammar-for-radial-cell-or-coefficient-bound-branch.md",
        "needles": [
            "CGT1868_0_hypotheses",
            "TYPED_PARENT_GRAMMAR_NOT_DERIVED_CURRENT_CORPUS",
            "COEFFICIENT_BOUND_BRANCH_SELECTED_NEXT",
        ],
    },
    {
        "source_id": "SRC2629_05_1869_finite_schema",
        "role": "finite coefficient schema and R10 fail-safe dry run",
        "path": ROOT / "1869-Y5-R2FR-finite-local-coefficient-bound-branch-setup.md",
        "needles": [
            "DEC1869_0_result",
            "FINITE_LOCAL_COEFFICIENT_BRANCH_SCHEMA_READY_NONCLAIM",
            "R10_TEMPLATE_DRYRUN_BLOCKS_AS_EXPECTED",
        ],
    },
    {
        "source_id": "SRC2629_06_1870_first_fill",
        "role": "first-fill attempt and denominator convention blocker",
        "path": ROOT / "1870-Y5-R2FR-QR-ZR-MR2-source-chain-first-fill-or-no-charge-return.md",
        "needles": [
            "SCA1870_7_verdict",
            "NO_FIRST_FILL_READY",
            "MISSING_CONVENTION_LOCK",
        ],
    },
    {
        "source_id": "SRC2629_07_1871_denominator",
        "role": "canonical C_R denominator convention handoff",
        "path": ROOT / "1871-Y5-R2FR-QR-normalization-convention-lock-or-source-denominator-row.md",
        "needles": [
            "DEC1871_0_result",
            "CANONICAL_C_R_DENOMINATOR_CONVENTION_LOCKED_NONCLAIM",
            "NEXT1871_0_primary",
        ],
    },
    {
        "source_id": "SRC2629_08_1871_validation",
        "role": "1871 validation pass",
        "path": RESIDUALS / "P8_Y5_BRR545_1871_VALIDATION.csv",
        "needles": ["VAL1871_OVERALL", "PASS"],
    },
]


def ensure_dirs() -> None:
    for directory_path in (RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE):
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as output_handle:
        writer = csv.DictWriter(output_handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as input_handle:
        return list(csv.DictReader(input_handle))


def csv_parses(path: Path) -> bool:
    try:
        return bool(read_csv(path))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        source_path = source["path"]
        text = read_text(source_path)
        exists = source_path.exists()
        needles_present = exists and all(needle in text for needle in source["needles"])
        rows.append(
            {
                "source_id": source["source_id"],
                "role": source["role"],
                "source_path": str(source_path),
                "exists": bool_text(exists),
                "needles_present": bool_text(needles_present),
                "needles": "; ".join(source["needles"]),
                "valid_for_claim": "False",
            }
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    return [
        {
            "lineage_id": "LIN2629_0_2628_target",
            "input_checkpoint": "2628",
            "result_taken_forward": "D_R normal form is the exact target, but selector/Hcore is the primary missing object.",
            "use_now": "audit whether existing 1866-1871 branch already supplies the selector or only a nonclaim handoff",
            "status": "selector_target_active",
            "valid_for_claim": "False",
        },
        {
            "lineage_id": "LIN2629_1_1866_selector_attempt",
            "input_checkpoint": "1866",
            "result_taken_forward": "reciprocity selector is not derived; ordinary Hcore gives finite reciprocal residual branch by default.",
            "use_now": "do not claim local GR from selector; keep finite Hcore branch as backstop",
            "status": "selector_not_derived",
            "valid_for_claim": "False",
        },
        {
            "lineage_id": "LIN2629_2_1867_1868_object_language",
            "input_checkpoint": "1867/1868",
            "result_taken_forward": "R_AB=C_R=ln(T^2 S) can be exact compatibility data only if a parent category principle, matter descent, and boundary silence are signed.",
            "use_now": "retain exact conditional theorem, but do not promote Z_R=0, J_R=0, or Q_R=0",
            "status": "conditional_theorem_parent_unsigned",
            "valid_for_claim": "False",
        },
        {
            "lineage_id": "LIN2629_3_1869_1870_finite_branch",
            "input_checkpoint": "1869/1870",
            "result_taken_forward": "finite local coefficient schema exists; Q_R/Z_R/M_R^2/J_R first fill found no numeric or theorem-zero row.",
            "use_now": "source or bound finite branch only after normalization and arena projections are explicit",
            "status": "finite_branch_schema_ready_nonclaim",
            "valid_for_claim": "False",
        },
        {
            "lineage_id": "LIN2629_4_1871_denominator",
            "input_checkpoint": "1871",
            "result_taken_forward": "canonical C_R denominator convention is locked for nonclaim handoff; massless C_R tail routes to PPN/orbital rather than R10.",
            "use_now": "next live fork is C_R=0/Pi_R=0 theorem versus absolute C_R/Pi_R tail bound",
            "status": "denominator_handoff_ready_next_fork_selected",
            "valid_for_claim": "False",
        },
    ]


def selector_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "selector_id": "SEL2629_0_target_operator",
            "object": "D_R[MTS]",
            "required_statement": "A parent operator P_R must contract the time/radial Euler equations so that P_R(E_parent)=partial_r C_R-S_R.",
            "current_status": "EXACT_TARGET_NOT_DERIVED",
            "blocking_countermodel": "generic Euler differences can select x, y, x+y, derivative mixtures, or coframe derivative invariants instead of C_R",
            "missing_for_proof": "MISSING_SELECTOR_KERNEL;MISSING_PARENT_ORIENTATION;MISSING_L_MTS_CORE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "selector_id": "SEL2629_1_kernel_orientation",
            "object": "selector kernel/orientation",
            "required_statement": "The parent grammar must define the reciprocity direction C_R=ln(T^2 S) as the unique kernel/image component seen by the local radial equation.",
            "current_status": "PRIMARY_MISSING_OBJECT",
            "blocking_countermodel": "a nearby parent action can make the same variables generate a different normal form or extra source term",
            "missing_for_proof": "MISSING_PARENT_CATEGORY_PRINCIPLE;MISSING_KERNEL_CERTIFICATE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "selector_id": "SEL2629_2_no_gr_import_guard",
            "object": "no-GR-import guard",
            "required_statement": "AB=1, p=1, Einstein-vacuum identity, or local-GR plateau cannot be inserted as premises.",
            "current_status": "GUARD_ACTIVE",
            "blocking_countermodel": "using the GR answer as the selector would make the reduction circular",
            "missing_for_proof": "MISSING_PARENT_SOURCE_EQUATION_NOT_GR_IMPORTED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "selector_id": "SEL2629_3_boundary_source_silence",
            "object": "boundary/source silence",
            "required_statement": "If the selector produces partial_r C_R, integration gives local GR only when C_R infinity/reference and Q_R/Pi_R/source tails vanish or are bounded.",
            "current_status": "NOT_SIGNED",
            "blocking_countermodel": "nonzero boundary momentum or source current leaves a massless 1/r reciprocal tail",
            "missing_for_proof": "MISSING_CR_ZERO_THEOREM;MISSING_PIR_ZERO_THEOREM;MISSING_ABSOLUTE_TAIL_BOUND",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "selector_id": "SEL2629_4_verdict",
            "object": "reciprocity selector/Hcore source equation",
            "required_statement": "The current corpus must supply the selector/Hcore source equation before D_R can be treated as derived.",
            "current_status": "RECIPROCITY_SELECTOR_NOT_DERIVED_CURRENT_CORPUS",
            "blocking_countermodel": "ordinary Hcore and object-language routes both remain parent-unsigned",
            "missing_for_proof": "MISSING_SELECTOR_KERNEL_OR_HCORE_SOURCE_EQUATION",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def hcore_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "hcore_id": "HCA2629_0_formal_template",
            "candidate": "H_R density",
            "statement": "H_R=int sqrt(h)[1/2 Z_R h^ij D_i R_AB D_j R_AB + 1/2 M_R^2 R_AB^2 + lambda_R R_AB + J_R R_AB]+B_R.",
            "derivation_status": "FORMAL_VARIATIONAL_TEMPLATE_ONLY",
            "consequence": "ordinary Hcore makes R_AB a finite residual field unless a stronger grammar/constraint forbids it",
            "missing": "MISSING_PARENT_ORIGIN_OF_ZR_MR2_LAMBDAR_JR_BR",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "hcore_id": "HCA2629_1_exact_zero_route",
            "candidate": "compatibility/constraint-owned C_R",
            "statement": "If R_AB=C_R is compatibility data only and Lambda_R C_R is parent-owned before readout, then C_R=0, Z_R=0, J_R=0, Q_R=0 can follow conditionally.",
            "derivation_status": "EXACT_CONDITIONAL_THEOREM_PARENT_UNSIGNED",
            "consequence": "best route to derived local GR, but not yet active",
            "missing": "MISSING_CATEGORY_PRINCIPLE;MISSING_AUXILIARY_CONSTRAINT_ORIGIN;MISSING_MATTER_BOUNDARY_DESCENT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "hcore_id": "HCA2629_2_finite_mass_gap",
            "candidate": "finite reciprocal branch",
            "statement": "If Z_R>0 and M_R^2>0, ell_R=sqrt(Z_R/M_R^2) gives finite suppression only after J_R, boundary charge, and arena projections are sourced.",
            "derivation_status": "SOURCE_READY_ONLY",
            "consequence": "can become a bounded physics branch, not a derived-GR proof by itself",
            "missing": "MISSING_ZR;MISSING_MR2;MISSING_JR;MISSING_BOUNDARY_SOURCE;MISSING_TAU_ARENAS",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "hcore_id": "HCA2629_3_selector_verdict",
            "candidate": "H_core/L_MTS_core source equation",
            "statement": "No inspected source supplies a parent-signed H_core source equation that uniquely yields D_R=partial_r C_R-S_R.",
            "derivation_status": "NOT_DERIVED_CURRENT_CORPUS",
            "consequence": "D_R remains a theorem contract/closure benchmark, not a live local-GR derivation",
            "missing": "MISSING_HCORE_SOURCE_EQUATION",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def object_language_rows() -> list[dict[str, Any]]:
    return [
        {
            "object_id": "OBJ2629_0_exact_cell_identity",
            "claim_piece": "cell identity",
            "statement": "J_q=T sqrt(S), u=ln(J_q), and C_R=R_AB=2u=ln(T^2 S).",
            "status": "ALGEBRAIC_IDENTITY_AVAILABLE",
            "missing_for_zero": "identity alone does not forbid dynamics or source terms",
            "valid_for_claim": "False",
        },
        {
            "object_id": "OBJ2629_1_derivative_legality",
            "claim_piece": "Z_R=0 by grammar",
            "statement": "Derivative terms on R_AB are illegal only if parent grammar says R_AB is compatibility data, not an independent scalar/coframe invariant.",
            "status": "CONDITIONAL_FORBIDS_ZR",
            "missing_for_zero": "MISSING_PARENT_CATEGORY_PRINCIPLE;COFRAME_DERIVATIVE_COUNTERMODEL_SURVIVES",
            "valid_for_claim": "False",
        },
        {
            "object_id": "OBJ2629_2_matter_descent",
            "claim_piece": "J_R=0 by descent",
            "statement": "Matter cannot directly source C_R only if all matter/readout terms descend through parent coframe/readout after the constraint.",
            "status": "CONDITIONAL_FORBIDS_JR",
            "missing_for_zero": "MISSING_UNIVERSAL_MATTER_DESCENT;MISSING_NO_SHADOW_SOURCE_SLOT",
            "valid_for_claim": "False",
        },
        {
            "object_id": "OBJ2629_3_boundary_silence",
            "claim_piece": "Q_R/Pi_R=0 by boundary class",
            "statement": "A massless exterior tail disappears only if boundary variation and source neutrality prove Pi_R=0 or C_R absolute tail is bounded to zero.",
            "status": "BOUNDARY_NO_CHARGE_NOT_SIGNED",
            "missing_for_zero": "MISSING_BOUNDARY_VARIATION_CLASS;MISSING_SOURCE_NEUTRALITY;MISSING_REFERENCE_MATCHING",
            "valid_for_claim": "False",
        },
        {
            "object_id": "OBJ2629_4_verdict",
            "claim_piece": "object-language local-GR route",
            "statement": "The clean theorem exists as a contract, but it is not parent-signed in the current corpus.",
            "status": "OBJECT_LANGUAGE_GRAMMAR_CONDITIONAL_NOT_ACTIVATED",
            "missing_for_zero": "MISSING_PARENT_CATEGORY_PRINCIPLE_AND_DESCENT",
            "valid_for_claim": "False",
        },
    ]


def finite_branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "component_id": "FBR2629_0_C_R",
            "symbol": "C_R",
            "meaning": "canonical reciprocal tail coefficient / radial-cell compatibility amplitude",
            "current_status": "DENOMINATOR_CONVENTION_LOCKED_NONCLAIM",
            "missing_for_score": "MISSING_NUMERIC_C_R_OR_ZERO_THEOREM;MISSING_SAME_FRAME_MSTAR;MISSING_NO_CANCELLATION_BUDGET",
            "arena_link": "PPN;orbital;local_GR",
            "valid_for_claim": "False",
        },
        {
            "component_id": "FBR2629_1_Q_cur",
            "symbol": "Q_cur",
            "meaning": "current charge in W(r) dR_AB/dr=Q_cur",
            "current_status": "SYMBOLIC_SPLIT_FROM_C_R",
            "missing_for_score": "MISSING_KAPPA_W_NUMERIC;MISSING_SIGN_ORIENTATION;MISSING_Q_CUR_VALUE_OR_ZERO",
            "arena_link": "PPN;orbital",
            "valid_for_claim": "False",
        },
        {
            "component_id": "FBR2629_2_Pi_R",
            "symbol": "Pi_R",
            "meaning": "boundary momentum / reciprocal boundary charge",
            "current_status": "BOUNDARY_RELATION_SYMBOLIC_NOT_PARENT_SIGNED",
            "missing_for_score": "MISSING_BOUNDARY_VARIATION_CLASS;MISSING_PIR_ZERO_OR_ABSOLUTE_BOUND",
            "arena_link": "local_GR;PPN;orbital",
            "valid_for_claim": "False",
        },
        {
            "component_id": "FBR2629_3_Z_R",
            "symbol": "Z_R",
            "meaning": "reciprocal gradient stiffness",
            "current_status": "MISSING_PARENT_OPERATOR",
            "missing_for_score": "MISSING_ZR_VALUE_OR_THEOREM_ABSENT;MISSING_SOURCE_PATH;MISSING_UNITS",
            "arena_link": "R10;clock;orbital;PPN",
            "valid_for_claim": "False",
        },
        {
            "component_id": "FBR2629_4_M_R2",
            "symbol": "M_R^2",
            "meaning": "reciprocal mass/stiffness scale",
            "current_status": "MISSING_PARENT_OPERATOR",
            "missing_for_score": "MISSING_MR2_VALUE_OR_THEOREM_ABSENT;MISSING_RANGE_CONVENTION",
            "arena_link": "R10;clock;orbital;PPN",
            "valid_for_claim": "False",
        },
        {
            "component_id": "FBR2629_5_J_R",
            "symbol": "J_R",
            "meaning": "direct matter/source drive of reciprocal cell mode",
            "current_status": "MISSING_MATTER_DESCENT_ZERO_OR_SOURCE_COEFFICIENT",
            "missing_for_score": "MISSING_JR_ZERO_THEOREM;MISSING_NUMERIC_SOURCE_MAP",
            "arena_link": "WEP;R10;PPN;clock",
            "valid_for_claim": "False",
        },
        {
            "component_id": "FBR2629_6_tau_R10",
            "symbol": "tau_R10",
            "meaning": "projection from finite reciprocal branch to alpha(lambda)",
            "current_status": "BLOCKED",
            "missing_for_score": "MISSING_ZR_MR2_LAMBDA_RANGE;MISSING_ALPHA_BOUND_CURVE_VALID_FOR_CLAIM;MISSING_SOURCE_TEST_CHARGES",
            "arena_link": "R10",
            "valid_for_claim": "False",
        },
        {
            "component_id": "FBR2629_7_tau_PPN",
            "symbol": "tau_PPN",
            "meaning": "projection from massless C_R tail to PPN/orbital residuals",
            "current_status": "HANDOFF_TEMPLATE_READY_NONCLAIM",
            "missing_for_score": "MISSING_ABSOLUTE_C_R_BOUND_OR_ZERO;MISSING_EXTERNAL_GAMMA_BOUND_SOURCE;MISSING_NO_CANCELLATION_VECTOR",
            "arena_link": "PPN;orbital",
            "valid_for_claim": "False",
        },
    ]


def normalization_rows() -> list[dict[str, Any]]:
    return [
        {
            "handoff_id": "NORM2629_0_canonical_denominator",
            "branch": "massless C_R tail",
            "formula": "q_R = C_R c^2/(2 G M_*)",
            "equivalent_current_formula": "q_R = -Q_cur c^2/(2 kappa_W G M_*)",
            "boundary_formula_held": "if Q_cur=-Pi_R then q_R=Pi_R c^2/(2 kappa_W G M_*), pending sign lock",
            "current_status": "SYMBOLIC_CONVENTION_LOCKED_NONCLAIM",
            "guard": "requires C_R or Q_cur, same-frame M_*, kappa_W if using current charge, sign orientation, and no-cancellation budget",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "handoff_id": "NORM2629_1_massless_guard",
            "branch": "PPN/orbital",
            "formula": "Delta gamma order q_R for a massless 1/r reciprocal tail",
            "equivalent_current_formula": "use C_R convention rather than ambiguous Q_R naming",
            "boundary_formula_held": "Pi_R substitution held until boundary sign and silence are signed",
            "current_status": "PPN_ORBITAL_BRANCH_ONLY",
            "guard": "do not route massless C_R/r hair into R10 alpha(lambda)",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "handoff_id": "NORM2629_2_finite_yukawa_guard",
            "branch": "finite R10 branch",
            "formula": "ell_R=sqrt(Z_R/M_R^2) only after Z_R>0 and M_R^2>0 are sourced",
            "equivalent_current_formula": "alpha(lambda) requires finite-range owner plus source/test charges",
            "boundary_formula_held": "C_R denominator alone is insufficient for R10",
            "current_status": "FINITE_RANGE_OWNER_MISSING",
            "guard": "R10 remains blocked until Z_R, M_R^2, J_R, tau_R10 and bound curve are claim-valid",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "handoff_id": "NORM2629_3_next_fork",
            "branch": "C_R theorem-zero versus absolute tail bound",
            "formula": "C_R=0/Pi_R=0 gives local-GR candidate; otherwise absolute C_R/Pi_R bound feeds q_R",
            "equivalent_current_formula": "Q_cur only after kappa_W/sign convention and source class are fixed",
            "boundary_formula_held": "prove boundary silence first; if not, stage nonclaim bound rows",
            "current_status": "NEXT_TARGET_SELECTED",
            "guard": "no local-GR/PPN/orbital claim until theorem-zero or sourced bound rows exist",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE2629_0_selector",
            "claim": "reciprocity selector/Hcore source equation is derived",
            "current_evidence": "1866 and 2629 audit say selector/Hcore is a formal target, not parent-signed",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE2629_1_object_language_zero",
            "claim": "C_R, Z_R, J_R, and Q_R are theorem-zero by object language",
            "current_evidence": "1868 conditional theorem exists, but category principle, descent, and boundary silence are unsigned",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE2629_2_hcore_finite_score",
            "claim": "finite reciprocal branch is source-backed and scoreable",
            "current_evidence": "Z_R, M_R^2, J_R, tau_R10, tau_PPN and source/test charges remain missing or nonclaim",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE2629_3_denominator",
            "claim": "C_R denominator convention is sufficient for local test pass",
            "current_evidence": "1871 locks symbolic denominator only; numeric C_R/zero theorem and source mass frame remain missing",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE2629_4_local_GR_Newton",
            "claim": "MTS locally reduces to GR/Newton in this branch",
            "current_evidence": "selector, C_R zero, boundary silence, S_R zero/bound, and PPN residual vector remain open",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE2629_5_local_tests",
            "claim": "R10/WEP/PPN/clock/orbital arenas pass",
            "current_evidence": "no generated 2629 row is numeric, source-backed, and valid_for_claim",
            "gate_pass": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2629_0_result",
            "decision": "RECIPROCITY_SELECTOR_OR_HCORE_NOT_DERIVED_CURRENT_CORPUS",
            "reason": "1866-1871 supply exact contracts and fail-safe handoffs, but no parent-signed selector kernel or H_core source equation.",
            "next_action": "keep D_R as a theorem contract and attack the now-sharp C_R zero/bound fork",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2629_1_best_derivation_lane",
            "decision": "OBJECT_LANGUAGE_CONDITIONAL_THEOREM_RETAINED",
            "reason": "R_AB=C_R as compatibility data remains the least-scrutiny route because it avoids adding a propagating fifth-force scalar.",
            "next_action": "only promote it if category principle, matter descent, and boundary silence are parent-signed",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2629_2_practical_progress",
            "decision": "CANONICAL_C_R_DENOMINATOR_HANDOFF_RETAINED_NONCLAIM",
            "reason": "1871 repaired the Q_cur/C_R/Pi_R naming collision enough for PPN/orbital handoff rows, but not for a claim.",
            "next_action": "use C_R for massless local tail; do not feed it into R10 alpha(lambda)",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2629_3_next",
            "decision": "CR_ZERO_THEOREM_OR_ABSOLUTE_TAIL_BOUND_SELECTED_NEXT",
            "reason": "after the selector audit, the smallest non-circular test of local-GR recovery is whether boundary/source silence forces C_R=0/Pi_R=0, or leaves a bounded PPN tail.",
            "next_action": "attempt theorem-zero first; if it fails, stage absolute C_R/Pi_R/Delta_gamma bound rows with no claim",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": "2630-Y5-R2FR-CR-zero-theorem-or-absolute-tail-bound-row.md",
            "script": "scripts/Y5_R2FR_CR_zero_theorem_or_absolute_tail_bound_row_2630.py",
            "objective": "prove C_R=0/Pi_R=0 from parent boundary silence, source neutrality, and reference matching; if not, stage source-ready absolute C_R/Pi_R/Delta_gamma bound rows using the 1871 convention.",
            "include": "C_R denominator convention; Pi_R boundary variation; source neutrality; same-frame M_*; PPN/orbital bound link; no-cancellation envelope",
            "exclude": "AB=1 or p=1 as premise, Einstein-equation import, invented numeric tails, R10 alpha claim from massless C_R, GitHub action, formalization-workbench edits",
            "selected": "True",
            "valid_for_claim": "False",
        },
        {
            "next_target": "2630b-Y5-R2FR-ZR-MR2-range-owner-or-Yukawa-row.md",
            "script": "scripts/Y5_R2FR_ZR_MR2_range_owner_or_Yukawa_row_2630b.py",
            "objective": "in parallel only, source Z_R/M_R^2/lambda_R for the finite R10 branch without mixing it with the massless C_R tail.",
            "include": "Z_R; M_R^2; ell_R; J_R; tau_R10; finite-range source/test charges",
            "exclude": "PPN massless tail scored as Yukawa R10 alpha(lambda)",
            "selected": "False",
            "valid_for_claim": "False",
        },
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("COPY2629_selector_gate", "selector_Hcore_gate", OUTPUTS["selector_gate"], LOCAL_BOUNDS / "Selector_Hcore_gate_2629_NONCLAIM.csv"),
        ("COPY2629_finite_branch", "reciprocal_finite_branch_status", OUTPUTS["finite_branch"], LOCAL_BOUNDS / "Reciprocal_finite_branch_status_2629_NONCLAIM.csv"),
        ("COPY2629_denominator", "CR_denominator_convention_handoff", OUTPUTS["normalization"], LOCAL_BOUNDS / "CR_denominator_convention_handoff_2629_NONCLAIM.csv"),
        ("COPY2629_next_target", "CR_zero_or_absolute_tail_next", OUTPUTS["next_target"], RAB_QUEUE / "JR2629_CR_ZERO_OR_ABSOLUTE_TAIL_BOUND_NEXT.csv"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, label, source_path, destination_path in copy_specs:
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, destination_path)
        rows.append(
            {
                "copy_id": copy_id,
                "label": label,
                "source_path": str(source_path),
                "destination_path": str(destination_path),
                "destination_exists": bool_text(destination_path.exists()),
                "csv_parses": bool_text(csv_parses(destination_path)),
                "row_count": len(read_csv(destination_path)) if destination_path.exists() else 0,
            }
        )
    return rows


def any_claim_promoted(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for table_rows in rows_by_name.values():
        for row in table_rows:
            if row.get("valid_for_claim") == "True" or row.get("claim_allowed") == "True":
                return True
    return False


def missing_row_promoted(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for table_rows in rows_by_name.values():
        for row in table_rows:
            row_text = " ".join(str(value) for value in row.values())
            promoted = row.get("valid_for_claim") == "True" or row.get("claim_allowed") == "True"
            if "MISSING_" in row_text and promoted:
                return True
    return False


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    selector_rows = rows_by_name["selector_gate"]
    hcore_rows = rows_by_name["hcore_audit"]
    object_rows = rows_by_name["object_language"]
    normalization_rows_local = rows_by_name["normalization"]
    claim_rows = rows_by_name["claim_gates"]
    next_rows = rows_by_name["next_target"]
    branch_rows = rows_by_name["branch_copies"]
    generated_csv_paths = [path for name, path in OUTPUTS.items() if name != "validation"]

    checks: list[tuple[str, bool, str]] = [
        (
            "VAL2629_00_sources_exist",
            all(row["exists"] == "True" and row["needles_present"] == "True" for row in source_rows),
            "all cited source paths exist and needles are present",
        ),
        (
            "VAL2629_01_selector_not_promoted",
            any(row["current_status"] == "RECIPROCITY_SELECTOR_NOT_DERIVED_CURRENT_CORPUS" for row in selector_rows)
            and not any(row.get("claim_allowed") == "True" for row in selector_rows),
            "selector/Hcore verdict remains not derived",
        ),
        (
            "VAL2629_02_hcore_nonclaim",
            any(row["derivation_status"] == "FORMAL_VARIATIONAL_TEMPLATE_ONLY" for row in hcore_rows)
            and any(row["derivation_status"] == "SOURCE_READY_ONLY" for row in hcore_rows),
            "Hcore branch is formal/source-ready only",
        ),
        (
            "VAL2629_03_object_language_conditional",
            any(row["status"] == "OBJECT_LANGUAGE_GRAMMAR_CONDITIONAL_NOT_ACTIVATED" for row in object_rows),
            "object-language theorem is retained as conditional and parent unsigned",
        ),
        (
            "VAL2629_04_denominator_handoff",
            any(row["current_status"] == "SYMBOLIC_CONVENTION_LOCKED_NONCLAIM" for row in normalization_rows_local),
            "C_R denominator convention handoff exists and remains nonclaim",
        ),
        (
            "VAL2629_05_massless_not_R10",
            any("do not route massless C_R/r hair into R10" in row["guard"] for row in normalization_rows_local),
            "massless C_R tail is not routed into R10 alpha(lambda)",
        ),
        (
            "VAL2629_06_claim_gates_false",
            all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claim_rows),
            "all local/theory/test claim gates are false",
        ),
        (
            "VAL2629_07_no_claim_flags",
            not any_claim_promoted(rows_by_name),
            "no generated claim-sensitive row is promoted",
        ),
        (
            "VAL2629_08_missing_not_ready",
            not missing_row_promoted(rows_by_name),
            "no MISSING_* row is marked claim-ready",
        ),
        (
            "VAL2629_09_next_target",
            any(row["selected"] == "True" and "CR-zero-theorem" in row["next_target"] for row in next_rows),
            "2630 C_R zero theorem or absolute tail bound is selected",
        ),
        (
            "VAL2629_10_branch_copies",
            all(row["destination_exists"] == "True" and row["csv_parses"] == "True" for row in branch_rows),
            "branch/local/queue copies exist and parse",
        ),
        (
            "VAL2629_11_formalization_untouched",
            not any(str(path).startswith(str(FORMALIZATION)) for path in generated_csv_paths + [DOC_PATH]),
            "no 2629 outputs are written under formalization-workbench",
        ),
        (
            "VAL2629_12_csv_parse",
            all(csv_parses(path) for path in generated_csv_paths),
            "all generated 2629 CSVs parse",
        ),
        (
            "VAL2629_13_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
    ]
    validation = [
        {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "False",
        }
        for check_id, passed, detail in checks
    ]
    validation.append(
        {
            "check_id": "VAL2629_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in validation) else "FAIL",
            "detail": "2629 reciprocity selector/Hcore source equation checkpoint",
            "valid_for_claim": "False",
        }
    )
    return validation


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        safe_values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(safe_values) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    sections = [
        ("Source Register", rows_by_name["source_register"]),
        ("Lineage Ledger", rows_by_name["lineage"]),
        ("Selector Gate", rows_by_name["selector_gate"]),
        ("Hcore Source Equation Audit", rows_by_name["hcore_audit"]),
        ("Object-Language Grammar Audit", rows_by_name["object_language"]),
        ("Finite Branch Status", rows_by_name["finite_branch"]),
        ("C_R Denominator Handoff", rows_by_name["normalization"]),
        ("Claim Gates", rows_by_name["claim_gates"]),
        ("Decision Ledger", rows_by_name["decision"]),
        ("Next Target", rows_by_name["next_target"]),
        ("Branch Copies", rows_by_name["branch_copies"]),
        ("Validation", rows_by_name["validation"]),
    ]
    body = [
        "# 2629 - Y5 R2/f(R) Reciprocity Selector Operator Or Hcore Source Equation",
        "",
        f"Generated: `{generated_at}`",
        "",
        "Status: `Y5_R2FR_2629_selector_Hcore_not_derived_CR_denominator_handoff_ready_CR_zero_or_tail_bound_next_nonclaim`",
        "",
        "Claim ceiling: no reciprocity selector/Hcore derivation, no `C_R=0`, no `Pi_R=0`, no `Z_R=0`, no `J_R=0`, no local-GR/Newton reduction, no R10/WEP/PPN/clock/orbital pass, no GitHub action, and no `formalization-workbench` edit is made.",
        "",
        "## Summary",
        "",
        "2629 audits the missing gear named by 2628: the parent reciprocity selector or `H_core/L_MTS_core` source equation that would make the local Euler combination select `C_R` rather than smuggling in a plateau.",
        "",
        "Verdict: it is still not derived. The best derivation lane remains the object-language route where `R_AB=C_R=ln(T^2 S)` is compatibility data, but that only works if a parent category principle, matter descent, and boundary silence are signed. Type alone is too weak because coframe derivative countermodels can regenerate an effective `Z_R`.",
        "",
        "The useful progress is 1871: the `C_R` denominator convention is now safe enough for nonclaim handoff rows. Massless `C_R/r` hair belongs to PPN/orbital tail bounds, not R10 alpha(lambda). The next sharp fork is therefore: prove `C_R=0/Pi_R=0`, or stage an absolute tail-bound row.",
        "",
    ]
    for title, table_rows in sections:
        body.extend([f"## {title}", "", markdown_table(table_rows), ""])
    body.extend(
        [
            "## Plain-English Verdict",
            "",
            "This is not circling for the sake of circling; it is the selector gate snapping into focus. We now know the elegant route and the ugly-but-testable route.",
            "",
            "Elegant route: prove `C_R` is pure compatibility/constraint data and prove boundary/source silence, so the local reciprocal tail never becomes physical. Ugly-but-testable route: accept a finite or massless residual and bound `C_R`, `Pi_R`, `Z_R`, `M_R^2`, and `J_R` against PPN/orbital/R10 arenas.",
            "",
            "Next best shot: theorem-zero first. Try to prove `C_R=0` or `Pi_R=0` from boundary silence/source neutrality. If that fails, do not hand-wave it away; build the absolute tail-bound row and let local tests judge it. That is the least-cheatable route from here.",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(body), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "lineage": lineage_rows(),
        "selector_gate": selector_gate_rows(),
        "hcore_audit": hcore_audit_rows(),
        "object_language": object_language_rows(),
        "finite_branch": finite_branch_rows(),
        "normalization": normalization_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, table_rows in rows_by_name.items():
        write_csv(OUTPUTS[name], table_rows)

    rows_by_name["branch_copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)

    print(f"wrote {DOC_PATH}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()

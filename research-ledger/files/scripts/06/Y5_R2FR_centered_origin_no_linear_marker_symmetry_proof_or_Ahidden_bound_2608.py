from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_AFFINE_SOURCE_GATE_2608"
CHECKPOINT_ID = "2608"

DOC = ROOT / "2608-Y5-R2FR-centered-origin-no-linear-marker-symmetry-proof-or-Ahidden-bound.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_AFFINE_SOURCE_GATE_2608_SOURCE_REGISTER.csv",
    "lineage_ledger": OUT / "P8_Y5_AFFINE_SOURCE_GATE_2608_LINEAGE_LEDGER.csv",
    "centered_origin": OUT / "P8_Y5_AFFINE_SOURCE_GATE_2608_CENTERED_ORIGIN_THEOREM_ATTEMPT.csv",
    "no_linear_marker": OUT / "P8_Y5_AFFINE_SOURCE_GATE_2608_NO_LINEAR_MARKER_THEOREM_ATTEMPT.csv",
    "affine_bound": OUT / "P8_Y5_AFFINE_SOURCE_GATE_2608_AFFINE_SOURCE_BOUND_ROWS.csv",
    "proof_obligations": OUT / "P8_Y5_AFFINE_SOURCE_GATE_2608_PRIMITIVE_PACKAGE_OBLIGATIONS.csv",
    "source_zero": OUT / "P8_Y5_AFFINE_SOURCE_GATE_2608_SOURCE_ZERO_STATUS.csv",
    "claim_gates": OUT / "P8_Y5_AFFINE_SOURCE_GATE_2608_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_AFFINE_SOURCE_GATE_2608_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_AFFINE_SOURCE_GATE_2608_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_AFFINE_SOURCE_GATE_2608_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2608_VALIDATION.csv",
}

COPY_TARGETS = {
    "affine_bound": LOCAL_BOUNDS / "Affine_source_bound_rows_2608_NONCLAIM.csv",
    "source_zero": LOCAL_BOUNDS / "Affine_source_zero_status_2608_NONCLAIM.csv",
    "proof_obligations": LOCAL_BOUNDS / "Primitive_package_obligations_2608_NONCLAIM.csv",
    "next_target": QUEUE / "JR2608_PRIMITIVE_MINIMALITY_INVARIANT_ALGEBRA_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def false_flags() -> dict[str, bool]:
    return {
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "accepted_for_scoring": False,
    }


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC2608_00_2607_handoff_doc",
            "source_path": ROOT / "2607-Y5-R2FR-source-support-or-boundary-no-flux-first-residual-zero-bound.md",
            "needles": ["NEXT2607_0_selected", "HSC2607_0_shifted_origin", "HSC2607_1_linear_marker_covector", "VAL2607_OVERALL"],
            "role": "current handoff selecting centered-origin/no-linear-marker hidden source gate",
        },
        {
            "source_id": "SRC2608_01_2607_hidden_source_csv",
            "source_path": OUT / "P8_Y5_FIRST_RESIDUAL_GATE_2607_HIDDEN_SOURCE_LEDGER.csv",
            "needles": ["HSC2607_0_shifted_origin", "HSC2607_1_linear_marker_covector", "HSC2607_9_verdict"],
            "role": "current hidden source vector containing shifted-origin and marker-covector channels",
        },
        {
            "source_id": "SRC2608_02_2607_source_status",
            "source_path": OUT / "P8_Y5_FIRST_RESIDUAL_GATE_2607_FIRST_RESIDUAL_STATUS.csv",
            "needles": ["FRS2607_2_source_exact_zero", "FRS2607_3_hidden_source_vector", "FRS2607_7_verdict"],
            "role": "current source residual status requiring hidden source zero proof or finite bound",
        },
        {
            "source_id": "SRC2608_03_1757_doc",
            "source_path": ROOT / "1757-Y5-R2FR-centered-origin-no-linear-marker-symmetry-proof-or-Ahidden-bound.md",
            "needles": ["CO1757_4_verdict", "NLM1757_6_verdict", "VAL1757_OVERALL"],
            "role": "prior centered-origin/no-linear-marker proof attempt",
        },
        {
            "source_id": "SRC2608_04_1757_centered_origin",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1757_CENTERED_ORIGIN_THEOREM_ATTEMPT.csv",
            "needles": ["CO1757_0_problem", "CO1757_2_norm_square_owner", "CO1757_4_verdict"],
            "role": "prior centered-origin theorem contract rows",
        },
        {
            "source_id": "SRC2608_05_1757_no_marker",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1757_NO_LINEAR_MARKER_THEOREM_ATTEMPT.csv",
            "needles": ["NLM1757_0_problem", "NLM1757_2_invariant_covector_zero", "NLM1757_6_verdict"],
            "role": "prior no-linear-marker theorem contract rows",
        },
        {
            "source_id": "SRC2608_06_1757_affine_bounds",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1757_AFFINE_SOURCE_BOUND_ROWS.csv",
            "needles": ["ASB1757_0_A_shift", "ASB1757_1_A_marker", "ASB1757_2_A_affine"],
            "role": "prior affine source fallback interface",
        },
        {
            "source_id": "SRC2608_07_1758_roadmap_doc",
            "source_path": ROOT / "1758-Y5-R2FR-primitive-minimality-invariant-algebra-or-Aaffine-bound.md",
            "needles": ["PM1758_4_promotion", "DEC1758_4_best_next", "VAL1758_OVERALL"],
            "role": "prior roadmap showing the common primitive-minimality/invariant-algebra package",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        missing_needles = path_has_needles(spec["source_path"], spec["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": spec["source_id"],
                    "source_path": spec["source_path"],
                    "exists": spec["source_path"].exists(),
                    "missing_needles": missing_needles,
                    "source_pass": spec["source_path"].exists() and not missing_needles,
                    "role": spec["role"],
                    **false_flags(),
                }
            )
        )
    return rows


def lineage_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "step_id": "LIN2608_0_2607",
            "checkpoint": "2607",
            "question": "Which hidden source channels are lowest-level?",
            "result": "Shifted kinetic origin and linear marker covector are the leading affine source channels inside J_hidden.",
            "status": "CURRENT_HANDOFF_REBASED",
            "next_dependency": "centered-origin and no-linear-marker theorem contracts",
        },
        {
            "step_id": "LIN2608_1_1757_centered_origin",
            "checkpoint": "1757",
            "question": "Can X0(q)=0 be derived?",
            "result": "Conditionally yes: parent zero section plus norm-square kinetic owner plus no affine displacement would force X0(q)=0.",
            "status": "THEOREM_CONTRACT_READY_PARENT_UNSIGNED",
            "next_dependency": "primitive zero-section/minimality proof",
        },
        {
            "step_id": "LIN2608_2_1757_no_marker",
            "checkpoint": "1757",
            "question": "Can ell_marker=0 be derived?",
            "result": "Conditionally yes: strict quotient plus no invariant dual plus no marker functor and constant/source universality would force ell_marker=0.",
            "status": "THEOREM_SHAPE_EXACT_PARENT_UNSIGNED",
            "next_dependency": "local invariant-algebra triviality and constant universality",
        },
        {
            "step_id": "LIN2608_3_1757_affine_bound",
            "checkpoint": "1757",
            "question": "What if the zero proof fails?",
            "result": "Carry A_shift, A_marker, and A_affine in a common E* norm instead of hiding F_1.",
            "status": "FINITE_FALLBACK_INTERFACE_RETAINED",
            "next_dependency": "E* norm and arena projection if proof package fails",
        },
        {
            "step_id": "LIN2608_4_1758_preview",
            "checkpoint": "1758",
            "question": "What common parent package is missing?",
            "result": "Primitive minimality and invariant-algebra triviality are the common missing reasons behind X0(q)=0 and ell_marker=0.",
            "status": "ROADMAP_IMPORTED_NOT_REPLAYED_AS_CLAIM",
            "next_dependency": "2609 primitive-minimality/invariant-algebra gate",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def centered_origin_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CO2608_0_problem",
            "shifted origin is the leading affine kinetic source",
            "S_X=1/2 <X-X0(q),L_X(X-X0(q))> gives J_shift=-L_X X0(q) at X=0",
            "OBSTRUCTION_IDENTIFIED",
            "SHIFTED_ORIGIN_COUNTEREXAMPLE_RETAINED",
            "need parent reason that the local memory fibre has primitive zero section X0(q)=0 rather than a calibrated moving origin",
        ),
        (
            "CO2608_1_zero_section_contract",
            "parent zero section",
            "Conf_parent contains a vector/fibre bundle E_X -> Q with parent-owned zero section 0_X(q)",
            "CLEAN_CONTRACT_WRITTEN",
            "NOT_PARENT_DERIVED",
            "current corpus treats X=0 as candidate local branch, not yet as primitive zero section forced by the parent action",
        ),
        (
            "CO2608_2_norm_square_owner",
            "norm-square-only activation",
            "S_X^kin=1/2 <X,L_X X> with positive h_X/L_X and no affine displacement term",
            "RELATIVE_THEOREM_SHAPE",
            "PARENT_FIBRE_METRIC_AND_NORMSQUARE_ONLY_UNSIGNED",
            "parent h_X, L_X, and exclusion of X0(q) are not all signed",
        ),
        (
            "CO2608_3_natural_zero_section",
            "no nonzero natural section",
            "if primitive minimality gives no local invariant that can build a nonzero section X0(q), then X0(q)=0",
            "EXACT_CONDITIONAL_THEOREM",
            "REDUCED_TO_PRIMITIVE_MINIMALITY_AND_INVARIANT_ALGEBRA",
            "must show no quotient extension, source class, material scalar, chi_D, memory scalar, or readout class can generate X0",
        ),
        (
            "CO2608_4_projection_lock_limit",
            "projection lock is not enough",
            "F_1 projection locks one trace/readout derivative but does not ban every shifted local source",
            "PARTIAL_WIN_NOT_FULL_ORIGIN",
            "DO_NOT_PROMOTE",
            "projection hygiene is useful but cannot replace a parent zero-section theorem",
        ),
        (
            "CO2608_5_verdict",
            "centered-origin theorem verdict",
            "X0(q)=0 follows from parent zero-section + norm-square-only kinetic owner + no nonzero natural section",
            "THEOREM_CONTRACT_READY_PARENT_UNSIGNED",
            "CENTERED_ORIGIN_NOT_CLOSED",
            "A_shift remains live until zero-section/minimality/no-affine premises are signed",
        ),
    ]
    return [
        with_stamp(
            {
                "attempt_id": attempt_id,
                "claim_piece": claim_piece,
                "mathematical_form": mathematical_form,
                "status": status,
                "proof_status": proof_status,
                "gap": gap,
                **false_flags(),
            }
        )
        for attempt_id, claim_piece, mathematical_form, status, proof_status, gap in rows
    ]


def no_linear_marker_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NLM2608_0_problem",
            "linear marker covector is the leading F_1 obstruction",
            "F(X)=F(0)+ell_marker(X)+1/2 H_X(X,X)+O(||X||^3)",
            "OBSTRUCTION_IDENTIFIED",
            "ell_marker sources J_X(0) unless forbidden",
            "need parent reason ell_marker cannot exist",
        ),
        (
            "NLM2608_1_fixed_spurion",
            "fixed external covectors are excluded by strict quotient",
            "fixed ell is not a function on E_X/G_X unless it is G_X-invariant",
            "CONDITIONAL_PASS",
            "STRICT_QUOTIENT_REQUIRED",
            "strict quotient parent domain is not signed for every local branch",
        ),
        (
            "NLM2608_2_invariant_covector_zero",
            "no invariant dual vector",
            "ell in (E_X*)^{G_X}; if (E_X*)^{G_X}=0 then ell=0",
            "RELATIVE_THEOREM_DERIVED",
            "PARENT_GX_EX_AND_NO_TRIVIAL_DUAL_UNSIGNED",
            "G_X, E_X, and absence of trivial dual subrepresentation are not parent-proved",
        ),
        (
            "NLM2608_3_marker_functor",
            "no E_X*-valued marker functor",
            "m:I_loc(Q_MTS)->E_X*; if I_loc=I_geom tensor Const and (E_X*)^{G_X}=0 then m=0",
            "RELATIVE_THEOREM_DERIVED",
            "INVARIANT_ALGEBRA_TRIVIALITY_UNSIGNED",
            "finite fibre spectrum, domain class, chi_D, memory scalar, species constants and readout projectors remain legal generators",
        ),
        (
            "NLM2608_4_material_constant_failure",
            "co-moving material/constants survive",
            "theta_A=theta_A(I_Q,m,h) or kappa_A=kappa_A(I_Q,m) can generate material/source-weight covectors",
            "FAIL_CURRENT_CORPUS",
            "COUNTEREXAMPLES_RETAINED",
            "primitive minimality, constant-sector trivial action, and universal kappa remain unsigned",
        ),
        (
            "NLM2608_5_readout_hygiene_limit",
            "readout marker hygiene is useful but insufficient",
            "post-readout projector notin Args(S_parent) blocks fake readout sources, but does not remove material/domain/constant markers",
            "HYGIENE_ONLY",
            "DO_NOT_PROMOTE_TO_SOURCE_ZERO",
            "ordinary source-side marker channels survive readout cleanup",
        ),
        (
            "NLM2608_6_verdict",
            "no-linear-marker theorem verdict",
            "strict quotient + (E_X*)^{G_X}=0 + no E_X*-valued marker functor + constant/source universality would force ell_marker=0",
            "THEOREM_SHAPE_EXACT_PARENT_UNSIGNED",
            "NO_LINEAR_MARKER_NOT_CLOSED",
            "A_marker remains live until primitive minimality, invariant algebra triviality, and constant/source universality are signed",
        ),
    ]
    return [
        with_stamp(
            {
                "attempt_id": attempt_id,
                "claim_piece": claim_piece,
                "mathematical_form": mathematical_form,
                "status": status,
                "proof_status": proof_status,
                "gap": gap,
                **false_flags(),
            }
        )
        for attempt_id, claim_piece, mathematical_form, status, proof_status, gap in rows
    ]


def affine_bound_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ASB2608_0_A_shift",
            "A_shift",
            "shifted kinetic origin",
            "A_shift=||L_X X0(q)||_{E*}",
            "MISSING_CENTERED_ORIGIN_ZERO_OR_A_SHIFT",
            "E*_dual_or_declared_arena_units",
            "contributes to A_affine and J_hidden",
            OUTPUTS["source_register"],
        ),
        (
            "ASB2608_1_A_marker",
            "A_marker",
            "linear marker covector",
            "A_marker=||ell_marker||_{E*}",
            "MISSING_NO_MARKER_THEOREM_OR_A_MARKER",
            "E*_dual_or_declared_arena_units",
            "contributes to A_affine and J_hidden",
            OUTPUTS["source_register"],
        ),
        (
            "ASB2608_2_A_affine",
            "A_affine",
            "leading affine hidden source",
            "A_affine<=A_shift+A_marker in a single declared E* norm",
            "MISSING_COMMON_ESTAR_NORM_AND_AFFINE_VALUES",
            "same_E*_dual_units_for_A_shift_and_A_marker",
            "leading nonclaim source envelope for the F_1 obstruction",
            "ASB2608_0_A_shift;ASB2608_1_A_marker",
        ),
        (
            "ASB2608_3_R_source_affine",
            "R_source_affine",
            "explicit U_B-weighted source residual",
            "||R_source,affine||_{E*}<=U_B A_affine",
            "MISSING_AAFFINE_AND_ESTAR_UNITS",
            "E*_dual_or_declared_arena_units",
            "keeps repaired p_total=1+p_int bookkeeping for affine p_int=0 branch",
            "P8_Y5_FIRST_RESIDUAL_GATE_2607_SOURCE_POWER_CONVENTION.csv",
        ),
        (
            "ASB2608_4_observable_insert",
            "R_affine_arena",
            "arena-projected affine response",
            "||R_affine,arena||<=U_B ||P_arena L_X^{-1}|| A_affine",
            "MISSING_OPERATOR_INVERSE_AND_ARENA_PROJECTION_NORMS",
            "arena_declared_units",
            "turns affine source into explicit residual rather than hidden zero",
            "ASB2608_2_A_affine;ESN2607_5_arena_projection",
        ),
    ]
    return [
        with_stamp(
            {
                "bound_id": bound_id,
                "quantity": quantity,
                "source_channel": source_channel,
                "definition": definition,
                "current_status": current_status,
                "units": units,
                "use_if_proof_fails": use_if_proof_fails,
                "source_path": source_path,
                **false_flags(),
            }
        )
        for bound_id, quantity, source_channel, definition, current_status, units, use_if_proof_fails, source_path in rows
    ]


def proof_obligation_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PO2608_0_parent_zero_section",
            "zero-section ownership",
            "E_X -> Q has primitive parent zero section 0_X(q)",
            "needed to make X0(q)=0 a theorem rather than a gauge choice",
            "MISSING_PARENT_ZERO_SECTION",
        ),
        (
            "PO2608_1_norm_square_kinetic",
            "norm-square kinetic owner",
            "S_X^kin=1/2<X,L_X X> and excludes affine displacement",
            "needed to remove J_shift=-L_X X0(q)",
            "MISSING_NORMSQUARE_ONLY_OWNER",
        ),
        (
            "PO2608_2_primitive_minimality",
            "primitive minimality",
            "Conf_parent=Q_MTS rather than extended Q_tilde=(Q_MTS,m)/G_rel",
            "needed to forbid material/domain/source marker quotient extensions",
            "MISSING_PRIMITIVE_MINIMALITY_THEOREM",
        ),
        (
            "PO2608_3_no_invariant_dual",
            "no invariant dual",
            "(E_X*)^{G_X}=0",
            "needed to force strict quotient-compatible linear covectors to vanish",
            "MISSING_GX_EX_AND_NO_TRIVIAL_DUAL_PROOF",
        ),
        (
            "PO2608_4_invariant_algebra_triviality",
            "local invariant algebra triviality",
            "I_loc(Q_MTS) supplies no marker/source generator capable of mapping into E_X*",
            "needed to kill marker functors and nonzero natural sections",
            "MISSING_INVARIANT_GENERATOR_ELIMINATION",
        ),
        (
            "PO2608_5_constant_source_universality",
            "constant/source universality",
            "species constants and source weights do not transform into local marker covectors",
            "needed to prevent material/source-weight ell_marker channels",
            "MISSING_CONSTANT_SECTOR_TRIVIAL_ACTION_AND_UNIVERSAL_KAPPA",
        ),
        (
            "PO2608_6_common_Estar",
            "common E* fallback norm",
            "A_shift, A_marker and A_affine share one declared E* norm and arena projection map",
            "needed if zero proof fails",
            "MISSING_ESTAR_AAFFINE_INTERFACE",
        ),
    ]
    return [
        with_stamp(
            {
                "obligation_id": obligation_id,
                "obligation": obligation,
                "required_statement": required_statement,
                "why_it_matters": why_it_matters,
                "current_status": current_status,
                **false_flags(),
            }
        )
        for obligation_id, obligation, required_statement, why_it_matters, current_status in rows
    ]


def source_zero_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SZ2608_0_F1",
            "F_1 / affine source",
            "NARROWED_NOT_ZEROED",
            "centered-origin and no-linear-marker theorem contracts are exact but parent unsigned",
            "A_shift and A_marker still live",
        ),
        (
            "SZ2608_1_shift",
            "J_shift",
            "NOT_ZEROED",
            "X0(q)=0 would follow from zero-section/norm-square/minimality package",
            "zero-section/minimality/no-affine premises unsigned",
        ),
        (
            "SZ2608_2_marker",
            "J_marker",
            "NOT_ZEROED",
            "ell_marker=0 would follow from strict quotient/no invariant dual/no marker functor package",
            "invariant algebra/constant universality unsigned",
        ),
        (
            "SZ2608_3_affine_bound",
            "A_affine",
            "FINITE_INTERFACE_STAGED_NONCLAIM",
            "A_affine<=A_shift+A_marker and ||R_source,affine||<=U_B A_affine",
            "numeric/source-backed E* values and projection norms missing",
        ),
        (
            "SZ2608_4_source_silence",
            "S_cg(D_L=0,Y)",
            "NOT_DERIVED",
            "even if affine source dies, coupling chain, matter/worldtube, boundary/history, tower, mu_even and kernel sources remain",
            "J_hidden not zero",
        ),
        (
            "SZ2608_5_GR_Newton",
            "local GR/Newton bridge",
            "CLOSER_BUT_BLOCKED",
            "leading p=1 affine obstruction is isolated into exact theorem obligations or A_affine rows",
            "primitive package plus sibling hidden-source residuals remain open",
        ),
    ]
    return [
        with_stamp(
            {
                "status_id": status_id,
                "quantity": quantity,
                "current_status": current_status,
                "evidence": evidence,
                "remaining_gap": remaining_gap,
                **false_flags(),
            }
        )
        for status_id, quantity, current_status, evidence, remaining_gap in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2608_0_centered_origin", "X0(q)=0 is parent-derived", "BLOCKED_PARENT_ZERO_SECTION_AND_NO_AFFINE_ORIGIN_UNSIGNED"),
        ("GATE2608_1_no_linear_marker", "ell_marker=0 is parent-derived", "BLOCKED_INVARIANT_ALGEBRA_AND_NO_TRIVIAL_DUAL_UNSIGNED"),
        ("GATE2608_2_affine_zero", "F_1 affine source is zero", "BLOCKED_A_SHIFT_A_MARKER_LIVE"),
        ("GATE2608_3_affine_finite_score", "A_affine can be scored in local arenas", "BLOCKED_ESTAR_AAFFINE_OPERATOR_PROJECTION_MISSING"),
        ("GATE2608_4_source_silence", "S_cg(D_L=0,Y)=0 is proven", "BLOCKED_SIBLING_HIDDEN_SOURCES_ACTIVE"),
        ("GATE2608_5_local_GR_Newton", "local GR/Newton/PPN/R10/WEP branch can claim", "BLOCKED_NO_LOCAL_REENTRY"),
    ]
    return [
        with_stamp(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_pass": False,
                "status": "BLOCKED_NO_CLAIM",
                "blocker": blocker,
                **false_flags(),
            }
        )
        for gate_id, claim, blocker in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2608_0_centered_origin",
            "decision": "centered-origin theorem shape is accepted but not promoted",
            "reason": "X0(q)=0 follows cleanly from zero-section/norm-square/minimality clauses, but those clauses are not parent-signed",
            "effect": "A_shift remains live",
        },
        {
            "decision_id": "DEC2608_1_no_linear_marker",
            "decision": "no-linear-marker theorem shape is accepted but not promoted",
            "reason": "strict quotient and representation triviality would kill ell_marker, but invariant algebra and constant/source universality remain unsigned",
            "effect": "A_marker remains live",
        },
        {
            "decision_id": "DEC2608_2_affine_status",
            "decision": "reduce leading F_1 obstruction to A_shift plus A_marker",
            "reason": "the lowest-level hidden source is now a named affine package, not an undefined failure",
            "effect": "use A_affine<=A_shift+A_marker if proof package fails",
        },
        {
            "decision_id": "DEC2608_3_power_convention",
            "decision": "keep explicit U_B on affine source residual",
            "reason": "2607 repaired the convention: affine hidden source has p_int=0, so R_source,affine carries p_total=1",
            "effect": "no accidental U_B^2 promotion from a single explicit switch",
        },
        {
            "decision_id": "DEC2608_4_best_next",
            "decision": "select primitive-minimality/invariant-algebra proof or Aaffine bound",
            "reason": "that package is the common missing parent reason behind X0=0, ell_marker=0, and constant/source universality",
            "effect": "2609 should attack primitive minimality and generator debts before coupling-chain cleanup",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2608_0_selected",
            "selection_status": "selected",
            "target_file": "2609-Y5-R2FR-primitive-minimality-invariant-algebra-or-Aaffine-bound.md",
            "target_script": "scripts/Y5_R2FR_primitive_minimality_invariant_algebra_or_Aaffine_bound_2609.py",
            "task": "try to prove no extended marker quotient and no local invariant-algebra generators capable of producing X0(q) or ell_marker; otherwise build A_affine bound rows",
            "success_condition": "primitive minimality/invariant algebra kills A_shift and A_marker, or A_affine is explicit with E* units and source paths",
            "fallback_condition": "if affine package stays blocked, move to coupling-chain double-zero or A_chain bound",
            "guardrails": "no plateau axiom; no marker hiding by readout hygiene alone; no local-GR claim; no GitHub; no formalization-workbench edits",
        },
        {
            "route_id": "NEXT2608_1_coupling_fallback",
            "selection_status": "held_fallback",
            "target_file": "2609b-Y5-R2FR-coupling-chain-source-double-zero-proof-or-Achain-bound.md",
            "target_script": "scripts/Y5_R2FR_coupling_chain_source_double_zero_proof_or_Achain_bound_2609b.py",
            "task": "after affine source handling, try to derive f(0)=f'(0)=0 or delta_X chi_D=0",
            "success_condition": "observable coupling chain source is theorem-zero or finite bounded in E*",
            "fallback_condition": "hidden source envelope runner if no zero proof closes",
            "guardrails": "do not tune f after local tests",
        },
        {
            "route_id": "NEXT2608_2_finite_fallback",
            "selection_status": "held_fallback",
            "target_file": "2609c-Y5-R2FR-Aaffine-E-star-bound-runner.md",
            "target_script": "scripts/Y5_R2FR_Aaffine_E_star_bound_runner_2609c.py",
            "task": "turn A_shift/A_marker/A_affine into a runnable nonclaim source-envelope interface with units and projection norms",
            "success_condition": "finite affine residual can be evaluated as nonclaim input",
            "fallback_condition": "local branch remains closure-only",
            "guardrails": "score only after units, E* norm, operator inverse, and arena projections are real",
        },
    ]
    return [with_stamp({**row, **false_flags()}) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, target in COPY_TARGETS.items():
        source = OUTPUTS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2608_{key}",
                    "source_path": source,
                    "target_path": target,
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                    **false_flags(),
                }
            )
        )
    return rows


def generated_rows_have_no_claim_flags(data: dict[str, list[dict[str, Any]]]) -> bool:
    forbidden_true_fields = {"valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring", "valid_prediction_row"}
    for rows in data.values():
        for row in rows:
            for field in forbidden_true_fields:
                if row.get(field) is True:
                    return False
    return True


def missing_rows_not_ready(data: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in data.values():
        for row in rows:
            joined = " ".join(row_value(value) for value in row.values())
            if "MISSING" in joined:
                if row.get("score_ready") is True or row.get("claim_allowed") is True or row.get("valid_prediction_row") is True:
                    return False
    return True


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(with_stamp({"check_id": check_id, "status": "PASS" if condition else "FAIL", "notes": notes, "detail": detail, "valid_for_claim": False}))

    add("VAL2608_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited source paths exist and needles are present")
    add("VAL2608_01_lineage_complete", {"2607", "1757", "1758"}.issubset({row["checkpoint"] for row in data["lineage"]}), "lineage covers current handoff plus prior affine source route")
    add("VAL2608_02_centered_origin_not_promoted", any(row["attempt_id"] == "CO2608_5_verdict" and row["proof_status"] == "CENTERED_ORIGIN_NOT_CLOSED" for row in data["centered_origin"]), "centered-origin theorem remains parent unsigned")
    add("VAL2608_03_no_marker_not_promoted", any(row["attempt_id"] == "NLM2608_6_verdict" and row["proof_status"] == "NO_LINEAR_MARKER_NOT_CLOSED" for row in data["no_linear_marker"]), "no-linear-marker theorem remains parent unsigned")
    add("VAL2608_04_relative_theorems_present", any(row["attempt_id"] == "CO2608_3_natural_zero_section" for row in data["centered_origin"]) and any(row["attempt_id"] == "NLM2608_2_invariant_covector_zero" for row in data["no_linear_marker"]), "relative theorem shapes are recorded")
    add("VAL2608_05_affine_rows_nonclaim", all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in data["affine_bound"]), "A_shift/A_marker/A_affine rows remain nonclaim")
    add("VAL2608_06_U_B_power_retained", any(row["bound_id"] == "ASB2608_3_R_source_affine" and "U_B A_affine" in row["definition"] for row in data["affine_bound"]), "explicit U_B source-residual factor retained")
    add("VAL2608_07_obligations_written", {"PO2608_2_primitive_minimality", "PO2608_4_invariant_algebra_triviality", "PO2608_5_constant_source_universality"}.issubset({row["obligation_id"] for row in data["proof_obligations"]}), "primitive package obligations are written")
    add("VAL2608_08_source_zero_blocked", any(row["status_id"] == "SZ2608_0_F1" and row["current_status"] == "NARROWED_NOT_ZEROED" for row in data["source_zero"]), "F_1 is narrowed but not zeroed")
    add("VAL2608_09_sibling_sources_retained", any(row["status_id"] == "SZ2608_4_source_silence" and row["current_status"] == "NOT_DERIVED" for row in data["source_zero"]), "sibling hidden source currents remain active")
    add("VAL2608_10_claim_gates_safe", all(row["claim_allowed"] is False and row["gate_pass"] is False for row in data["claim_gates"]), "all claim gates remain blocked")
    add("VAL2608_11_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row promotes scoring or claim flags")
    add("VAL2608_12_missing_not_ready", missing_rows_not_ready(data), "no MISSING_* row is marked ready")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*AFFINE_SOURCE_GATE_2608*", "2608-Y5-R2FR-centered-origin-no-linear-marker-symmetry-proof-or-Ahidden-bound.md", "*JR2608_PRIMITIVE_MINIMALITY_INVARIANT_ALGEBRA_NEXT*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2608_13_no_formalization_artifacts", not formalization_artifacts, "no 2608 affine-source artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))
    add("VAL2608_14_decision_next", any(row["decision_id"] == "DEC2608_4_best_next" for row in data["decisions"]), "decision selects primitive-minimality/invariant-algebra route")
    add("VAL2608_15_next_selected", any(row["route_id"] == "NEXT2608_0_selected" and row["selection_status"] == "selected" for row in data["next"]), "next target selected")
    add("VAL2608_16_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")
    add("VAL2608_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2608_CSV_{path.stem}", parsed, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2608_COPY_CSV_{key}", parsed, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(with_stamp({"check_id": "VAL2608_OVERALL", "status": "PASS" if overall else "FAIL", "notes": "2608 centered-origin/no-linear-marker gate narrows leading affine source but keeps A_affine nonclaim", "detail": "", "valid_for_claim": False}))
    return rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(row_value(row.get(field, "")).replace("|", "/") for field in fields) + " |")
    return "\n".join([header, divider, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2608: R2FR Centered-Origin / No-Linear-Marker Symmetry Proof Or Ahidden Bound",
        "",
        "**Status:** private nonclaim current-branch affine-source checkpoint. This does not claim `F_1=0`, source silence, local GR, Newton, PPN, R10, WEP, clocks, or orbital closure.",
        "",
        "**Main result:** the leading affine obstruction is now cleanly split. A shifted kinetic origin gives `J_shift=-L_X X0(q)`; a linear marker covector gives `J_marker=ell_marker`. The centered-origin theorem is exact only conditionally: parent zero section, norm-square-only kinetic owner, and no nonzero natural section would force `X0(q)=0`. The no-linear-marker theorem is also exact only conditionally: strict quotient, no invariant dual, no marker functor, and constant/source universality would force `ell_marker=0`. Current MTS has not parent-signed those packages, so `A_shift`, `A_marker`, and `A_affine<=A_shift+A_marker` remain explicit nonclaim residual inputs. The repaired 2607 source-power convention is retained: `||R_source,affine||<=U_B A_affine`, not a hidden `U_B^2` win.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Lineage Ledger",
        markdown_table(data["lineage"], ["step_id", "checkpoint", "question", "result", "status", "next_dependency", "valid_for_claim", "claim_allowed"]),
        "",
        "## Centered-Origin Theorem Attempt",
        markdown_table(data["centered_origin"], ["attempt_id", "claim_piece", "mathematical_form", "status", "proof_status", "gap", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## No-Linear-Marker Theorem Attempt",
        markdown_table(data["no_linear_marker"], ["attempt_id", "claim_piece", "mathematical_form", "status", "proof_status", "gap", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Affine Source Bound Rows",
        markdown_table(data["affine_bound"], ["bound_id", "quantity", "source_channel", "definition", "current_status", "units", "use_if_proof_fails", "source_path", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Primitive Package Obligations",
        markdown_table(data["proof_obligations"], ["obligation_id", "obligation", "required_statement", "why_it_matters", "current_status", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Source-Zero Status",
        markdown_table(data["source_zero"], ["status_id", "quantity", "current_status", "evidence", "remaining_gap", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_pass", "status", "blocker", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "guardrails", "valid_for_claim"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists", "valid_for_claim"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail", "valid_for_claim"]),
        "",
        "## Private Verdict",
        "",
        "This is the right sort of annoying progress. We did not get `F_1=0`, but we have reduced the leading affine source to two named beasts: `A_shift` and `A_marker`. The next lever is the common parent package: primitive minimality plus invariant-algebra triviality. If that package closes, the local branch gets a real derivation win. If it does not, `A_affine` becomes an honest finite residual instead of a hidden assumption.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def build_data() -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(),
        "lineage": lineage_rows(),
        "centered_origin": centered_origin_rows(),
        "no_linear_marker": no_linear_marker_rows(),
        "affine_bound": affine_bound_rows(),
        "proof_obligations": proof_obligation_rows(),
        "source_zero": source_zero_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }


def main() -> None:
    data = build_data()

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["lineage_ledger"], data["lineage"])
    write_csv(OUTPUTS["centered_origin"], data["centered_origin"])
    write_csv(OUTPUTS["no_linear_marker"], data["no_linear_marker"])
    write_csv(OUTPUTS["affine_bound"], data["affine_bound"])
    write_csv(OUTPUTS["proof_obligations"], data["proof_obligations"])
    write_csv(OUTPUTS["source_zero"], data["source_zero"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2608_OVERALL")
    print(f"wrote {DOC}")
    print(f"validation={OUTPUTS['validation']}")
    print(f"overall={overall['status']}")


if __name__ == "__main__":
    main()

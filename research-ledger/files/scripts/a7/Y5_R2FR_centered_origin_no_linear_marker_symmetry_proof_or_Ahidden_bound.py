from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1757"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1757 - Centered-Origin No-Linear-Marker Symmetry Proof Or Ahidden Bound"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1757_0_1756_doc",
        "source_key": "1756_handoff",
        "source_path": ROOT / "1756-Y5-R2FR-two-slot-source-free-owner-or-hidden-source-counterexample-ledger.md",
        "needles": ["X0(q)=0", "ell_marker=0", "A_shift", "A_marker"],
    },
    {
        "source_id": "SRC1757_1_1756_hidden_sources",
        "source_key": "1756_hidden_source_ledger",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1756_HIDDEN_SOURCE_COUNTEREXAMPLE_LEDGER.csv",
        "needles": ["HSC1756_0_shifted_origin", "HSC1756_1_linear_marker_covector"],
    },
    {
        "source_id": "SRC1757_2_1756_residual_rows",
        "source_key": "1756_hidden_source_residual_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1756_HIDDEN_SOURCE_FINITE_RESIDUAL_ROWS.csv",
        "needles": ["HSR1756_0_shift", "HSR1756_1_marker"],
    },
    {
        "source_id": "SRC1757_3_974_parent_origin_gate",
        "source_key": "974_parent_origin_acceptance_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_974_PARENT_ORIGIN_ACCEPTANCE_GATE.csv",
        "needles": ["POA974_2_even_symmetry", "POA974_4_no_shifted_origin"],
    },
    {
        "source_id": "SRC1757_4_974_zero_origin_evenness",
        "source_key": "974_zero_origin_evenness",
        "source_path": RESIDUALS / "P8_Y5_R10_974_ZERO_ORIGIN_EVENNESS_ATTEMPT.csv",
        "needles": ["ZOE974_2_evenness_kills_linear", "ZOE974_6_verdict"],
    },
    {
        "source_id": "SRC1757_5_975_no_linear_marker",
        "source_key": "975_no_linear_marker_theorem",
        "source_path": RESIDUALS / "P8_Y5_R10_975_NO_LINEAR_MARKER_THEOREM_ATTEMPT.csv",
        "needles": ["NLM975_2_invariant_covector_lemma", "NLM975_7_verdict"],
    },
    {
        "source_id": "SRC1757_6_975_claim_gate",
        "source_key": "975_claim_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_975_CLAIM_GATE.csv",
        "needles": ["CGATE975_0_invariant_covector_zero", "CGATE975_2_p2_normsquare_promotion"],
    },
    {
        "source_id": "SRC1757_7_609_no_linear_gate",
        "source_key": "609_no_linear_marker_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_609_NO_LINEAR_MARKER_SYMMETRY_GATE.csv",
        "needles": ["NL609_4_no_linear_verdict", "finite_p1_branch_retained"],
    },
    {
        "source_id": "SRC1757_8_608_counterexample_gate",
        "source_key": "608_counterexamples",
        "source_path": RESIDUALS / "P8_Y5_R10_608_COUNTEREXAMPLE_GATE.csv",
        "needles": ["CE608_0_linear_marker_covector", "CE608_1_epsilon_already_squared"],
    },
    {
        "source_id": "SRC1757_9_573_minimality",
        "source_key": "573_primitive_minimality",
        "source_path": RESIDUALS / "P8_Y5_R10_573_PRIMITIVE_MINIMAL_THEOREM_ATTEMPT.csv",
        "needles": ["PM573_1_material_marker_no_extension", "PM573_3_local_invariant_algebra"],
    },
    {
        "source_id": "SRC1757_10_575_constant_source",
        "source_key": "575_constant_source_lock",
        "source_path": RESIDUALS / "P8_Y5_R10_575_CONSTANT_SOURCE_LOCK_CONTRACT.csv",
        "needles": ["CL575_1_trivial_MTS_action", "CL575_4_universal_coupling"],
    },
    {
        "source_id": "SRC1757_11_977_constant_source_certificate",
        "source_key": "977_constant_source_certificate",
        "source_path": RESIDUALS / "P8_Y5_R10_977_CONSTANT_SOURCE_CERTIFICATE_ATTEMPT.csv",
        "needles": ["CSC977_7_verdict", "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED"],
    },
    {
        "source_id": "SRC1757_12_986_parent_zero_theorem",
        "source_key": "986_parent_zero_theorem",
        "source_path": RESIDUALS / "P8_Y5_R10_986_PARENT_ZERO_THEOREM_GATE.csv",
        "needles": ["PZT986_3_verdict", "ZERO_THEOREM_RELATIVE_NOT_PARENT_SIGNED"],
    },
    {
        "source_id": "SRC1757_13_124_extremality",
        "source_key": "124_fixed_point_extremality",
        "source_path": FORMALIZATION / "124-fixed-point-extremality-origin.md",
        "needles": ["F_1 projection lock = partially derived", "double-zero origin"],
    },
    {
        "source_id": "SRC1757_14_128_frame_symmetry",
        "source_key": "128_leakage_frame_symmetry",
        "source_path": FORMALIZATION / "128-leakage-frame-symmetry.md",
        "needles": ["Z2/time-reversal-like symmetry", "scalar double-zero behaviour remains an explicit local closure law"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1757_SOURCE_REGISTER.csv",
    "centered_origin_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1757_CENTERED_ORIGIN_THEOREM_ATTEMPT.csv",
    "no_linear_marker_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1757_NO_LINEAR_MARKER_THEOREM_ATTEMPT.csv",
    "affine_source_bound": RESIDUALS / "P8_Y5_PARENT_QLOC_1757_AFFINE_SOURCE_BOUND_ROWS.csv",
    "proof_obligations": RESIDUALS / "P8_Y5_PARENT_QLOC_1757_PROOF_OBLIGATIONS.csv",
    "source_zero_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1757_SOURCE_ZERO_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1757_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1757_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1757_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1757_VALIDATION.csv",
}


COPY_MAP = {
    "centered_origin_attempt": "R2FR_1757_CENTERED_ORIGIN_THEOREM_ATTEMPT.csv",
    "no_linear_marker_attempt": "R2FR_1757_NO_LINEAR_MARKER_THEOREM_ATTEMPT.csv",
    "affine_source_bound": "R2FR_1757_AFFINE_SOURCE_BOUND_ROWS.csv",
    "proof_obligations": "R2FR_1757_PROOF_OBLIGATIONS.csv",
    "source_zero_status": "R2FR_1757_SOURCE_ZERO_STATUS.csv",
    "decision": "R2FR_1757_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1757_CLAIM_GATE.csv",
    "next_target": "R2FR_1757_NEXT_TARGET.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        needles_present = all(needle in text for needle in needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(exists),
                "needles": "; ".join(needles),
                "needles_present": yesno(needles_present),
                "used_for": "1757 centered-origin/no-linear-marker proof or Ahidden bound",
                "timestamp_utc": UTC,
            }
        )
    return rows


def centered_origin_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "CO1757_0_problem",
            "claim_piece": "shifted origin is the leading affine kinetic source",
            "mathematical_form": "S_X=1/2 <X-X0(q),L_X(X-X0(q))> gives J_shift=-L_X X0(q) at X=0",
            "status": "OBSTRUCTION_IDENTIFIED",
            "proof_status": "SHIFTED_ORIGIN_COUNTEREXAMPLE_RETAINED",
            "gap": "need parent reason the local memory fibre has zero section X0(q)=0, not a calibrated moving origin",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "CO1757_1_zero_section_contract",
            "claim_piece": "parent zero section",
            "mathematical_form": "Conf_parent contains a vector/fibre bundle E_X -> Q with a parent-owned zero section 0_X(q)",
            "status": "CLEAN_CONTRACT_WRITTEN",
            "proof_status": "NOT_PARENT_DERIVED",
            "gap": "current corpus treats X=0 as a candidate local branch, not as a primitive zero section forced by the parent action",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "CO1757_2_norm_square_owner",
            "claim_piece": "norm-square-only activation",
            "mathematical_form": "S_X^kin=1/2 <X,L_X X> with h_X and no affine displacement term",
            "status": "RELATIVE_THEOREM_SHAPE",
            "proof_status": "PARENT_FIBRE_METRIC_AND_NORMSQUARE_ONLY_UNSIGNED",
            "gap": "parent h_X, L_X, and exclusion of X0(q) are not all signed",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "CO1757_3_projection_lock_limit",
            "claim_piece": "projection lock is not enough",
            "mathematical_form": "F_1 projection lock = partially derived, but scalar double-zero origin remains local closure unless Z_L/zero section is parent-owned",
            "status": "PARTIAL_WIN_NOT_FULL_ORIGIN",
            "proof_status": "DO_NOT_PROMOTE",
            "gap": "projection lock helps one trace derivative; it does not ban every shifted local source",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "CO1757_4_verdict",
            "claim_piece": "centered-origin theorem verdict",
            "mathematical_form": "X0(q)=0 would follow from parent zero-section + norm-square-only kinetic owner + no affine displacement",
            "status": "THEOREM_CONTRACT_READY_PARENT_UNSIGNED",
            "proof_status": "CENTERED_ORIGIN_NOT_CLOSED",
            "gap": "A_shift remains live until zero-section/minimality/no-affine premises are signed",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def no_linear_marker_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NLM1757_0_problem",
            "claim_piece": "linear marker covector is the leading F_1 obstruction",
            "mathematical_form": "F(X)=F(0)+ell_marker(X)+1/2 H_X(X,X)+O(||X||^3)",
            "status": "OBSTRUCTION_IDENTIFIED",
            "proof_status": "ell_marker sources J_X(0) unless forbidden",
            "gap": "need parent reason ell_marker cannot exist",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NLM1757_1_fixed_spurion",
            "claim_piece": "fixed external covectors are excluded by strict quotient",
            "mathematical_form": "fixed ell is not a function on E_X/G_X unless it is G_X-invariant",
            "status": "CONDITIONAL_PASS",
            "proof_status": "STRICT_QUOTIENT_REQUIRED",
            "gap": "strict quotient parent domain not signed for every local branch",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NLM1757_2_invariant_covector_zero",
            "claim_piece": "no invariant dual vector",
            "mathematical_form": "ell in (E_X*)^{G_X}; if (E_X*)^{G_X}=0 then ell=0",
            "status": "RELATIVE_THEOREM_DERIVED",
            "proof_status": "PARENT_GX_EX_AND_NO_TRIVIAL_DUAL_UNSIGNED",
            "gap": "G_X, E_X, and absence of trivial dual subrepresentation are not parent-proved",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NLM1757_3_marker_functor",
            "claim_piece": "no E_X*-valued marker functor",
            "mathematical_form": "m: I_loc(Q_MTS) -> E_X*; if I_loc=I_geom tensor Const and (E_X*)^{G_X}=0 then m=0",
            "status": "RELATIVE_THEOREM_DERIVED",
            "proof_status": "INVARIANT_ALGEBRA_TRIVIALITY_UNSIGNED",
            "gap": "finite fibre spectrum, domain class, chi_D, memory scalar, species constants, and readout projectors remain legal generators",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NLM1757_4_material_constant_failure",
            "claim_piece": "co-moving material/constants survive",
            "mathematical_form": "theta_A=theta_A(I_Q,m,h) or kappa_A=kappa_A(I_Q,m) can generate material/source-weight covectors",
            "status": "FAIL_CURRENT_CORPUS",
            "proof_status": "COUNTEREXAMPLES_RETAINED",
            "gap": "primitive minimality, constant-sector trivial action, and universal kappa remain unsigned",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NLM1757_5_readout_hygiene_limit",
            "claim_piece": "readout marker hygiene is useful but insufficient",
            "mathematical_form": "post-readout projector notin Args(S_parent) blocks fake readout sources, but does not remove material/domain/constant markers",
            "status": "HYGIENE_ONLY",
            "proof_status": "DO_NOT_PROMOTE_TO_SOURCE_ZERO",
            "gap": "ordinary source-side marker channels survive readout cleanup",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "NLM1757_6_verdict",
            "claim_piece": "no-linear-marker theorem verdict",
            "mathematical_form": "strict quotient + (E_X*)^{G_X}=0 + no E_X*-valued marker functor + constant/source universality would force ell_marker=0",
            "status": "THEOREM_SHAPE_EXACT_PARENT_UNSIGNED",
            "proof_status": "NO_LINEAR_MARKER_NOT_CLOSED",
            "gap": "A_marker remains live until primitive minimality, invariant algebra triviality, and constant/source universality are signed",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def affine_source_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "bound_id": "ASB1757_0_A_shift",
            "quantity": "A_shift",
            "source_channel": "shifted kinetic origin",
            "definition": "A_shift = ||L_X X0(q)||_{E*}",
            "current_status": "MISSING_CENTERED_ORIGIN_ZERO_OR_A_SHIFT",
            "units": "E*_dual_or_declared_arena_units",
            "use_if_proof_fails": "contributes to A_affine and J_hidden",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1756_HIDDEN_SOURCE_FINITE_RESIDUAL_ROWS.csv"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "ASB1757_1_A_marker",
            "quantity": "A_marker",
            "source_channel": "linear marker covector",
            "definition": "A_marker = ||ell_marker||_{E*}",
            "current_status": "MISSING_NO_MARKER_THEOREM_OR_A_MARKER",
            "units": "E*_dual_or_declared_arena_units",
            "use_if_proof_fails": "contributes to A_affine and J_hidden",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1756_HIDDEN_SOURCE_FINITE_RESIDUAL_ROWS.csv"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "ASB1757_2_A_affine",
            "quantity": "A_affine",
            "source_channel": "leading affine hidden source",
            "definition": "A_affine <= A_shift + A_marker in a single declared E* norm",
            "current_status": "MISSING_COMMON_ESTAR_NORM_AND_AFFINE_VALUES",
            "units": "same_E*_dual_units_for_A_shift_and_A_marker",
            "use_if_proof_fails": "leading nonclaim source envelope for F_1 obstruction",
            "source_path": "ASB1757_0_A_shift; ASB1757_1_A_marker",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "bound_id": "ASB1757_3_source_residual_insert",
            "quantity": "R_affine",
            "source_channel": "affine part of R_source",
            "definition": "||R_affine|| <= ||P_arena L_X^{-1}|| A_affine, with operator/projection norms declared",
            "current_status": "MISSING_OPERATOR_INVERSE_AND_ARENA_PROJECTION_NORMS",
            "units": "arena_declared_units",
            "use_if_proof_fails": "turns affine source into explicit residual rather than hidden zero",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1757_AFFINE_SOURCE_BOUND_ROWS.csv"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def proof_obligation_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "obligation_id": "PO1757_0_primitive_X",
            "obligation": "parent-owned primitive local memory fibre",
            "needed_for": "defines X, E_X, G_X, h_X, zero section, and dual representation",
            "current_status": "MISSING_PARENT_PRIMITIVE_X",
            "failure_if_missing": "X0 and ell are coordinate/proxy artefacts that cannot be scored cleanly",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "obligation_id": "PO1757_1_strict_quotient",
            "obligation": "strict quotient parent domain",
            "needed_for": "excludes fixed non-orbit spurion covectors",
            "current_status": "CONDITIONAL_PASS_NOT_GLOBAL_SIGNATURE",
            "failure_if_missing": "fixed external labels can source X",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "obligation_id": "PO1757_2_no_trivial_dual",
            "obligation": "(E_X*)^{G_X}=0",
            "needed_for": "kills invariant linear covectors",
            "current_status": "MISSING_REPRESENTATION_TRIVIAL_DUAL_AUDIT",
            "failure_if_missing": "an invariant ell survives while preserving formal symmetry",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "obligation_id": "PO1757_3_primitive_minimality",
            "obligation": "no extended quotient objects Q_tilde=(Q_MTS,m)/G_rel",
            "needed_for": "blocks co-moving material/domain marker functors",
            "current_status": "MISSING_PRIMITIVE_MINIMALITY_THEOREM",
            "failure_if_missing": "marker covectors descend as legal quotient data",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "obligation_id": "PO1757_4_invariant_algebra",
            "obligation": "I_loc(Q_MTS)=I_geom tensor Const with no extra local marker generators",
            "needed_for": "blocks natural E_X*-valued marker functors",
            "current_status": "MISSING_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY",
            "failure_if_missing": "finite fibre spectrum, chi_D, memory scalar, domain class, or species constants can build ell_marker",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "obligation_id": "PO1757_5_constant_source_universality",
            "obligation": "matter constants and source weights are fixed representation data with one universal kappa",
            "needed_for": "prevents theta_A(X), m_A(X), alpha_EM(X), kappa_A(X), and species source-weight covectors",
            "current_status": "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED",
            "failure_if_missing": "WEP/clock/source-normalization channels return",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
    ]


def source_zero_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1757_0_F1",
            "quantity": "F_1 / affine source",
            "current_status": "NARROWED_NOT_ZEROED",
            "evidence": "centered-origin and no-linear-marker theorem contracts are exact but parent unsigned",
            "remaining_gap": "A_shift and A_marker still live",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1757_1_source_silence",
            "quantity": "S_cg(D_L=0,Y)",
            "current_status": "NOT_DERIVED",
            "evidence": "even if affine source dies, coupling chain, matter/worldtube, boundary/history, tower, mu_even, and kernel sources remain",
            "remaining_gap": "J_hidden not zero",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1757_2_GR_Newton",
            "quantity": "local GR/Newton bridge",
            "current_status": "CLOSER_BUT_BLOCKED",
            "evidence": "the leading p=1 affine obstruction is isolated into exact theorem obligations or A_affine rows",
            "remaining_gap": "primitive minimality/invariant algebra/constant universality plus sibling residuals",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1757_0_centered_origin",
            "decision": "CENTERED_ORIGIN_THEOREM_CONTRACT_READY_NOT_PARENT_SIGNED",
            "reason": "X0=0 follows from a parent zero-section/norm-square owner, but that owner is not yet extracted from the parent action",
            "next_action": "retain A_shift unless primitive fibre/zero-section theorem is proved",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1757_1_no_linear_marker",
            "decision": "NO_LINEAR_MARKER_THEOREM_EXACT_PARENT_UNSIGNED",
            "reason": "strict quotient plus no invariant dual plus no marker functor kills ell_marker, but primitive minimality and invariant algebra remain unsigned",
            "next_action": "retain A_marker unless no-marker package is parent-signed",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1757_2_affine_status",
            "decision": "AFFINE_OBSTRUCTION_REDUCED_TO_A_SHIFT_A_MARKER",
            "reason": "the leading p=1 source is now cleanly separated into shifted-origin and marker-covector channels",
            "next_action": "prove primitive minimality/invariant algebra or fill A_affine in E* units",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1757_3_best_next",
            "decision": "PRIMITIVE_MINIMALITY_INVARIANT_ALGEBRA_IS_NEXT_BEST_ROUTE",
            "reason": "that package is the common missing parent reason behind X0=0, ell_marker=0, and constant/source universality",
            "next_action": "build 1758 primitive-minimality/local-invariant-algebra proof or A_affine bound runner",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1757_0_centered_origin",
            "claim": "X0(q)=0 is parent-derived",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_PARENT_ZERO_SECTION_AND_NO_AFFINE_ORIGIN_UNSIGNED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1757_1_no_linear_marker",
            "claim": "ell_marker=0 is parent-derived",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_PRIMITIVE_MINIMALITY_INVARIANT_ALGEBRA_CONSTANT_UNIVERSALITY_UNSIGNED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1757_2_A_affine_bound",
            "claim": "A_affine is finite and sourced in a declared E* norm",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_A_SHIFT_A_MARKER_COMMON_ESTAR_NORM_MISSING",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1757_3_source_zero",
            "claim": "leading affine part of J_hidden is zero",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_A_SHIFT_A_MARKER_STILL_LIVE",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1757_4_local_GR_Newton",
            "claim": "local GR/Newton/PPN/R10/WEP/clock/orbital branch can claim",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_AFFINE_SOURCE_AND_OTHER_HIDDEN_SOURCE_CHANNELS_ACTIVE",
            "claim_allowed": no(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1757_0_primary",
            "next_target": "1758-Y5-R2FR-primitive-minimality-invariant-algebra-or-Aaffine-bound.md",
            "script": "scripts/Y5_R2FR_primitive_minimality_invariant_algebra_or_Aaffine_bound.py",
            "objective": "try to prove the parent has no extended marker quotient and no local invariant algebra generators capable of producing X0(q) or ell_marker; otherwise build A_affine bound rows",
            "success_condition": "either primitive minimality/invariant algebra kills A_shift and A_marker, or A_affine is an explicit nonclaim residual with units and source paths",
            "selection_status": "selected",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1757_1_fallback",
            "next_target": "1758b-Y5-R2FR-coupling-chain-source-double-zero-proof-or-Achain-bound.md",
            "script": "scripts/Y5_R2FR_coupling_chain_source_double_zero_proof_or_Achain_bound.py",
            "objective": "after affine source handling, try to derive f(0)=f'(0)=0 or delta_X chi_D=0; otherwise carry A_chain",
            "success_condition": "observable coupling chain source is theorem-zero or becomes an explicit finite residual",
            "selection_status": "held_fallback",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "centered_origin_attempt": centered_origin_attempt_rows(),
        "no_linear_marker_attempt": no_linear_marker_attempt_rows(),
        "affine_source_bound": affine_source_bound_rows(),
        "proof_obligations": proof_obligation_rows(),
        "source_zero_status": source_zero_status_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1757_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1757_{key.upper()}.csv")


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for field in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if row.get(field) == "True":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values())
            if "MISSING_" in text:
                for field in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                    if row.get(field) == "True":
                        return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1757_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1757_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1757*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def centered_origin_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "CO1757_4_verdict"
        and row["proof_status"] == "CENTERED_ORIGIN_NOT_CLOSED"
        for row in rows_map["centered_origin_attempt"]
    )


def no_marker_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "NLM1757_6_verdict"
        and row["proof_status"] == "NO_LINEAR_MARKER_NOT_CLOSED"
        for row in rows_map["no_linear_marker_attempt"]
    )


def affine_bound_rows_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["affine_source_bound"]
    return len(rows) >= 4 and all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in rows)


def source_zero_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["status_id"] == "SZ1757_1_source_silence"
        and row["current_status"] == "NOT_DERIVED"
        for row in rows_map["source_zero_status"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["route_id"] == "NEXT1757_0_primary"
        and row["selection_status"] == "selected"
        for row in rows_map["next_target"]
    )


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    sources = rows_map["source_register"]
    claims = rows_map["claim_gate"]

    validation = [
        check("VAL1757_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1757_1_needles_present", all(row["needles_present"] == "True" for row in sources), "required source needles are present", "one or more source needles missing"),
        check("VAL1757_2_centered_origin_not_promoted", centered_origin_not_promoted(rows_map), "centered-origin theorem remains parent unsigned", "centered-origin theorem missing or promoted"),
        check("VAL1757_3_no_marker_not_promoted", no_marker_not_promoted(rows_map), "no-linear-marker theorem remains parent unsigned", "no-linear-marker theorem missing or promoted"),
        check("VAL1757_4_affine_rows_nonclaim", affine_bound_rows_nonclaim(rows_map), "A_shift/A_marker/A_affine rows remain nonclaim", "affine bound rows missing or promoted"),
        check("VAL1757_5_source_zero_blocked", source_zero_blocked(rows_map), "source-zero status remains blocked", "source-zero status missing or promoted"),
        check("VAL1757_6_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claims), "all claim gates remain blocked", "one or more claim gates opened"),
        check("VAL1757_7_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check("VAL1757_8_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check("VAL1757_9_decision_next", any(row["decision_id"] == "DEC1757_3_best_next" and row["decision"] == "PRIMITIVE_MINIMALITY_INVARIANT_ALGEBRA_IS_NEXT_BEST_ROUTE" for row in rows_map["decision"]), "decision selects primitive-minimality/invariant-algebra route", "best-next decision missing"),
        check("VAL1757_10_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check("VAL1757_11_csv_parse", parsed_ok, "all generated 1757 CSVs parse", "one or more generated 1757 CSVs failed to parse"),
        check("VAL1757_12_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1757_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1757_14_formalization_untouched", formalization_untouched(), "no 1757 outputs found under formalization-workbench", "1757 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1757_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1757 centered-origin/no-linear-marker proof or Ahidden bound" if overall else "one or more 1757 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1757 tries to kill the leading affine obstruction: `J_affine = -L_X X0(q) + ell_marker`.",
        "- The centered-origin route is theorem-shaped: a parent-owned zero section plus norm-square kinetic owner would force `X0(q)=0`.",
        "- The no-linear-marker route is theorem-shaped: strict quotient plus `(E_X*)^{G_X}=0` plus no marker functor plus constant/source universality would force `ell_marker=0`.",
        "- Current result: neither route is parent-signed. `A_shift`, `A_marker`, and `A_affine` remain explicit nonclaim residual rows.",
        "- This narrows the `F_1` problem substantially, but it does not derive `S_cg(D_L=0,Y)=0` or local GR/Newton.",
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Centered-Origin Theorem Attempt",
        markdown_table(rows_map["centered_origin_attempt"], ["attempt_id", "claim_piece", "mathematical_form", "status", "proof_status", "gap"]),
        "",
        "## No-Linear-Marker Theorem Attempt",
        markdown_table(rows_map["no_linear_marker_attempt"], ["attempt_id", "claim_piece", "mathematical_form", "status", "proof_status", "gap"]),
        "",
        "## Affine Source Bound Rows",
        markdown_table(rows_map["affine_source_bound"], ["bound_id", "quantity", "source_channel", "definition", "current_status"]),
        "",
        "## Proof Obligations",
        markdown_table(rows_map["proof_obligations"], ["obligation_id", "obligation", "needed_for", "current_status", "failure_if_missing"]),
        "",
        "## Source-Zero Status",
        markdown_table(rows_map["source_zero_status"], ["status_id", "quantity", "current_status", "evidence", "remaining_gap"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "This is progress of the useful, slightly annoying kind. The old vague `F_1` problem is now a clean affine source package: either parent geometry supplies a genuine zero section and no invariant marker covector, or the theory must carry `A_affine`. The best next move is to attack the common missing parent package: primitive minimality and local invariant-algebra triviality. If that fails, `A_affine` becomes a finite residual input instead of a hidden assumption.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1757-Y5-R2FR-centered-origin-no-linear-marker-symmetry-proof-or-Ahidden-bound.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1757_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1757 validation FAIL")
    print("1757 validation PASS")


if __name__ == "__main__":
    main()

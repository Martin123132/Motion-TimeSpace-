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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1755"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1755 - Source-Silent Fixed Point Theorem Or E-star Source Norm Row"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1755_0_1754_doc",
        "source_key": "1754_handoff",
        "source_path": ROOT / "1754-Y5-R2FR-ZL-DL-parent-leakage-vector-or-A-src-norm-acquisition.md",
        "needles": ["Source win still needs", "S_cg(D_L=0,Y)=0"],
    },
    {
        "source_id": "SRC1755_1_123_source_power",
        "source_key": "123_local_source_power_theorem",
        "source_path": FORMALIZATION / "123-local-source-power-theorem.md",
        "needles": [
            "local_source_power_theorem_form_constructed_not_parent_derived",
            "source_power_theorem_parent_derived = false",
            "S_cg(0,Y) = 0",
            "S_cg = O(D_L)",
        ],
    },
    {
        "source_id": "SRC1755_2_123_source_power_run",
        "source_key": "123_run_theorem_conditions",
        "source_path": FORMALIZATION
        / "runs"
        / "20260528-140716-local-source-power-theorem"
        / "results"
        / "theorem_conditions.csv",
        "needles": ["source_silence_surface", "S_cg(0,Y)=0"],
    },
    {
        "source_id": "SRC1755_3_971_parent_split",
        "source_key": "971_parent_split_derivation",
        "source_path": RESIDUALS / "P8_Y5_R10_971_PARENT_SPLIT_DERIVATION_ATTEMPT.csv",
        "needles": ["PSD971_4_matter_source", "source-free S_X^kin and quotient matter blindness are not parent-signed"],
    },
    {
        "source_id": "SRC1755_4_972_local_zero_gate",
        "source_key": "972_local_zero_theorem_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_972_LOCAL_ZERO_THEOREM_GATE.csv",
        "needles": ["LZG972_2_source_zero", "source-free S_X^kin, quotient matter blindness, and no hidden marker remain unsigned"],
    },
    {
        "source_id": "SRC1755_5_973_source_free_sxkin",
        "source_key": "973_source_free_sxkin_lemma",
        "source_path": RESIDUALS / "P8_Y5_R10_973_SOURCE_FREE_SXKIN_LEMMA.csv",
        "needles": ["SFL973_1_variation", "SFL973_5_hidden_source_counterexamples", "SFL973_6_verdict"],
    },
    {
        "source_id": "SRC1755_6_974_zero_origin",
        "source_key": "974_zero_origin_evenness",
        "source_path": RESIDUALS / "P8_Y5_R10_974_ZERO_ORIGIN_EVENNESS_ATTEMPT.csv",
        "needles": ["ZOE974_3_zero_origin_stationary", "ZOE974_5_even_scalar_warning"],
    },
    {
        "source_id": "SRC1755_7_974_marker_counterexamples",
        "source_key": "974_marker_counterexample_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_974_MARKER_COUNTEREXAMPLE_AUDIT.csv",
        "needles": ["MCE974_0_linear_marker_covector", "MCE974_5_verdict"],
    },
    {
        "source_id": "SRC1755_8_1751_elliptic_owner",
        "source_key": "1751_elliptic_functional_source_owner",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1751_ELLIPTIC_FUNCTIONAL_OWNERSHIP_CONTRACT.csv",
        "needles": ["EFO1751_4_source_owner", "MISSING_SOURCE_MAP"],
    },
    {
        "source_id": "SRC1755_9_1754_asrc_ledger",
        "source_key": "1754_asrc_estar_ledger",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1754_ASRC_NORM_ACQUISITION_LEDGER.csv",
        "needles": ["ANA1754_2_A1", "ANA1754_4_Estar"],
    },
    {
        "source_id": "SRC1755_10_local_eh_reduction",
        "source_key": "506_local_eh_reduction",
        "source_path": RESIDUALS / "P8_LOCAL_EH_REDUCTION_THEOREM_ATTEMPT.csv",
        "needles": ["T506_EH_plus_silent_reduction", "field-specific operators"],
    },
    {
        "source_id": "SRC1755_11_red_team",
        "source_key": "06_red_team_source_silence",
        "source_path": FORMALIZATION / "06-consistency-red-team.md",
        "needles": ["Generic analytic source silence gives:", "Even if scalar source silence works"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1755_SOURCE_REGISTER.csv",
    "theorem_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1755_SOURCE_SILENT_FIXED_POINT_THEOREM_ATTEMPT.csv",
    "two_slot_owner_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1755_TWO_SLOT_SOURCE_FREE_OWNER_AUDIT.csv",
    "estar_norm_acquisition": RESIDUALS / "P8_Y5_PARENT_QLOC_1755_ESTAR_SOURCE_NORM_ACQUISITION.csv",
    "residual_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1755_SOURCE_RESIDUAL_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1755_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1755_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1755_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1755_VALIDATION.csv",
}


COPY_MAP = {
    "theorem_attempt": "R2FR_1755_SOURCE_SILENT_FIXED_POINT_THEOREM_ATTEMPT.csv",
    "two_slot_owner_audit": "R2FR_1755_TWO_SLOT_SOURCE_FREE_OWNER_AUDIT.csv",
    "estar_norm_acquisition": "R2FR_1755_ESTAR_SOURCE_NORM_ACQUISITION.csv",
    "residual_status": "R2FR_1755_SOURCE_RESIDUAL_STATUS.csv",
    "decision": "R2FR_1755_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1755_CLAIM_GATE.csv",
    "next_target": "R2FR_1755_NEXT_TARGET.csv",
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
                "used_for": "1755 source-silent fixed point theorem or E* source norm row",
                "timestamp_utc": UTC,
            }
        )
    return rows


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SSF1755_0_target_statement",
            "premise_or_step": "source-silent local fixed point target",
            "mathematical_statement": "S_cg(D_L=0,Y)=0",
            "derivation_status": "TARGET_NEEDED_NOT_PROVED",
            "consequence": "with C1 regularity, S_cg(D_L,Y)=D_L S_1(Y)+O(D_L^2)",
            "blocker": "MISSING_PARENT_SOURCE_ZERO_AT_LOCAL_FIXED_POINT",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SSF1755_1_two_slot_variation_route",
            "premise_or_step": "conditional two-slot source-free route",
            "mathematical_statement": "S_parent=S_core[q(Phi),Psi,theta]+S_X^kin[X]+f(chi_D)C_obs[X,q(Phi),Psi]+S_matter[q(Phi),Psi,theta]",
            "derivation_status": "EXACT_CONDITIONAL_VARIATION_ROUTE",
            "consequence": "if f(0)=0, S_X^kin is homogeneous about X=0, and matter descends through q, then delta_X S_parent|local = L_X X and X=0 is source-silent",
            "blocker": "MISSING_PARENT_OWNERSHIP_OF_TWO_SLOT_ACTION_AND_SOURCE_FREE_KINETIC_ORIGIN",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SSF1755_2_regularity_to_linear_silence",
            "premise_or_step": "regular source-map expansion",
            "mathematical_statement": "S_cg in C1 near D_L=0 and S_cg(0,Y)=0",
            "derivation_status": "EXACT_CONDITIONAL_THEOREM",
            "consequence": "S_cg(D_L,Y)=D_L S_1(Y)+O(D_L^2)",
            "blocker": "MISSING_SOURCE_MAP_REGULARITY_RADIUS_AND_ESTAR_NORM",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SSF1755_3_hidden_source_counterexample_guard",
            "premise_or_step": "exclude hidden local sources",
            "mathematical_statement": "X0(q)=0, affine marker covectors vanish, no matter/worldtube X-vertex, no material/domain/readout marker, no boundary/history tail",
            "derivation_status": "COUNTEREXAMPLES_RETAINED",
            "consequence": "without this guard, J_X(0) can be nonzero and S_cg(D_L=0,Y)=0 fails",
            "blocker": "MISSING_NO_SHIFTED_ORIGIN_NO_MARKER_NO_BOUNDARY_TAIL_THEOREM",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SSF1755_4_finite_bound_if_signed",
            "premise_or_step": "combine source silence with 1754 D_L bound",
            "mathematical_statement": "D_L<=C_H U_B, ||S_1||_{E*}<=A_1, and ||S_2||_{E*}<=A_2",
            "derivation_status": "EXACT_CONDITIONAL_BOUND_FORM",
            "consequence": "||R_source|| <= C_H A_1 U_B^2 + C_H^2 A_2 U_B^3 in the far-local branch",
            "blocker": "MISSING_C_H_A1_A2_ESTAR_AND_ARENA_PROJECTION",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SSF1755_5_verdict",
            "premise_or_step": "source-silent fixed point theorem verdict",
            "mathematical_statement": "the theorem shape is correct, but the parent action has not yet signed every source-free premise",
            "derivation_status": "DERIVATION_ATTEMPT_FAILS_CURRENT_PARENT_SIGNATURE",
            "consequence": "source residual remains an active finite residual/nonclaim row rather than a local-GR pass",
            "blocker": "MISSING_PARENT_TWO_SLOT_SOURCE_FREE_OWNER_OR_REAL_ESTAR_SOURCE_NORM",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def two_slot_owner_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TSO1755_0_parent_contract",
            "clause": "two-slot action belongs to the primitive parent action",
            "required_signature": "S_parent separates quotient matter from an ungated homogeneous X-sector plus an explicitly gated observable coupling",
            "current_status": "CONTRACT_FORM_AVAILABLE_NOT_PARENT_EXTRACTED",
            "failure_mode_if_missing": "source silence becomes a closure axiom",
            "missing_input": "MISSING_PARENT_PRIMITIVE_ACTION_TWO_SLOT_DECOMPOSITION",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TSO1755_1_homogeneous_X_kinetic",
            "clause": "source-free homogeneous X kinetic sector",
            "required_signature": "S_X^kin=1/2 <X,L_X X> with no linear term and no shifted origin X0(q)",
            "current_status": "RELATIVE_LEMMA_READY_PARENT_UNSIGNED",
            "failure_mode_if_missing": "X0(q) or an affine covector generates J_X(0) != 0",
            "missing_input": "MISSING_NO_AFFINE_TERM_NO_SHIFTED_ORIGIN_THEOREM",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TSO1755_2_quotient_matter_blindness",
            "clause": "matter descends through q",
            "required_signature": "S_matter=Sbar_matter[q(Phi),Psi,theta] and carries no direct X, marker, species, or worldtube vertex outside q",
            "current_status": "NEEDED_NOT_PARENT_SIGNED",
            "failure_mode_if_missing": "ordinary matter sources X locally and WEP/PPN rows become material dependent",
            "missing_input": "MISSING_QUOTIENT_INVARIANT_MATTER_ACTION_AND_NO_MARKER_VERTEX",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TSO1755_3_observable_coupling_gate",
            "clause": "observable coupling is silent at the local fixed point",
            "required_signature": "f(chi_D)=0 at chi_D=0 and X-variation does not reintroduce a chain-source through chi_D(X)",
            "current_status": "GATE_SHAPE_AVAILABLE_CHAIN_SOURCE_UNSIGNED",
            "failure_mode_if_missing": "the coupling sector generates J_X(0) even when f(0)=0 in notation",
            "missing_input": "MISSING_INDEPENDENT_CHI_D_OR_NO_CHAIN_SOURCE_THEOREM",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TSO1755_4_no_linear_marker",
            "clause": "no material/domain/readout marker covector",
            "required_signature": "local parent symmetry excludes every allowed ell(X) built from material species, domain class, readout frame, spin, or boundary label",
            "current_status": "COUNTEREXAMPLES_RETAINED",
            "failure_mode_if_missing": "linear marker terms return and source-free branch becomes environment dependent",
            "missing_input": "MISSING_NO_LINEAR_MARKER_COVECTOR_THEOREM",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TSO1755_5_boundary_history_tail",
            "clause": "boundary and history terms do not source X",
            "required_signature": "zero local boundary flux plus no retained memory/history affine tail at D_L=0",
            "current_status": "NEEDED_NOT_PARENT_SIGNED",
            "failure_mode_if_missing": "source-silent bulk equations are spoiled by a boundary/history current",
            "missing_input": "MISSING_BOUNDARY_NOFLUX_AND_HISTORY_TAIL_ZERO_CERTIFICATE",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TSO1755_6_positive_operator_not_enough",
            "clause": "operator positivity is downstream of source zero",
            "required_signature": "L_X positive/coercive and J_X=0 in the same local functional",
            "current_status": "POSITIVE_OPERATOR_CONDITIONAL_ONLY",
            "failure_mode_if_missing": "positive operator bounds the response but does not erase a nonzero source current",
            "missing_input": "MISSING_LX_SIGNS_AND_JX_ZERO_IN_SAME_PARENT_FUNCTIONAL",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TSO1755_7_verdict",
            "clause": "two-slot source-free owner verdict",
            "required_signature": "all clauses TSO1755_0 through TSO1755_6 parent-signed with no hidden source counterexample",
            "current_status": "NOT_SIGNED_NEXT_PRIMARY_TARGET",
            "failure_mode_if_missing": "1755 remains a closure/finiteness branch, not a derived local-GR branch",
            "missing_input": "MISSING_SOURCE_FREE_TWO_SLOT_PARENT_OWNER",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def estar_norm_acquisition_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": "ESN1755_0_E_space_owner",
            "quantity": "E",
            "role": "local energy space for the 1751 coercive elliptic functional",
            "required_form": "source-backed function space, boundary conditions, measure, and operator domain used by the local residual identity",
            "current_status": "MISSING_E_SPACE_OWNER",
            "why_needed": "without E, E* is not a defined dual norm",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1751_ELLIPTIC_FUNCTIONAL_OWNERSHIP_CONTRACT.csv"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "ESN1755_1_Estar_owner",
            "quantity": "E*",
            "role": "dual norm for S_cg and J_eff source currents",
            "required_form": "dual of E with units, projection map, and arena restriction declared",
            "current_status": "MISSING_ESTAR_NORM_OWNER",
            "why_needed": "prevents mixing a formal source coefficient with an unrelated observable norm",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1754_ASRC_NORM_ACQUISITION_LEDGER.csv"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "ESN1755_2_A1",
            "quantity": "A_1 = ||partial_D S_cg(0,Y)||_{E*}",
            "role": "linear source coefficient in S_cg=D_L S_1+O(D_L^2)",
            "required_form": "finite numeric or theorem-bounded coefficient in the same E* norm",
            "current_status": "MISSING_A1_ESTAR_NORM",
            "why_needed": "sets the leading finite source residual C_H A_1 U_B^2",
            "source_path": str(FORMALIZATION / "123-local-source-power-theorem.md"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "ESN1755_3_A2",
            "quantity": "A_2 = ||S_2||_{E*}",
            "role": "quadratic remainder coefficient in the source expansion",
            "required_form": "finite numeric or theorem-bounded remainder norm over a declared D_L radius",
            "current_status": "MISSING_A2_ESTAR_REMAINDER",
            "why_needed": "blocks singular hidden remainders masquerading as O(D_L^2)",
            "source_path": str(FORMALIZATION / "123-local-source-power-theorem.md"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "ESN1755_4_CH",
            "quantity": "C_H",
            "role": "leakage-map norm bound in D_L<=C_H U_B",
            "required_form": "positive universal/local-domain bound from the Z_L/D_L parent leakage map",
            "current_status": "MISSING_C_H_BOUND",
            "why_needed": "connects source expansion in D_L to observable far-local U_B suppression",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1754_ZL_DL_LEAKAGE_VECTOR_CONTRACT.csv"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "ESN1755_5_arena_projection",
            "quantity": "P_arena",
            "role": "projects E* source norm into R10/WEP/PPN/clock/orbital readout arenas",
            "required_form": "operator norm and units for each arena with source paths",
            "current_status": "MISSING_ARENA_PROJECTION_NORMS",
            "why_needed": "a finite local source residual is not automatically below every observable bound",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1751_RESIDUAL_VECTOR.csv"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "ESN1755_6_regular_radius",
            "quantity": "rho_D",
            "role": "radius of validity for the C1/analytic D_L expansion",
            "required_form": "local-domain radius excluding transition shells and singular source maps",
            "current_status": "MISSING_REGULARITY_RADIUS",
            "why_needed": "prevents using far-local expansion through U_B=O(1) shells",
            "source_path": str(FORMALIZATION / "123-local-source-power-theorem.md"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "ESN1755_7_hidden_source_envelope",
            "quantity": "A_hidden or Z_hidden",
            "role": "zero certificate or finite envelope for shifted origins, marker covectors, worldtube vertices, and history tails",
            "required_form": "parent theorem-zero or source-backed bound per hidden-source channel",
            "current_status": "MISSING_HIDDEN_SOURCE_ZERO_OR_BOUND",
            "why_needed": "keeps the counterexamples from silently reentering through a different name",
            "source_path": str(RESIDUALS / "P8_Y5_R10_974_MARKER_COUNTEREXAMPLE_AUDIT.csv"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "ESN1755_8_shell_quarantine",
            "quantity": "Q_shell",
            "role": "transition shell projector/quarantine for U_B=O(1) regions",
            "required_form": "parent projector or explicit residual quarantine preventing far-local theorem misuse",
            "current_status": "MISSING_TRANSITION_SHELL_PROJECTOR_OR_QUARANTINE",
            "why_needed": "the U_B^2 source win is far-local only",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1754_SOURCE_RESIDUAL_STATUS.csv"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def residual_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RV1755_0_source_zero",
            "quantity": "S_cg(D_L=0,Y)",
            "formula_or_description": "local fixed-point source current evaluated on the leakage-zero branch",
            "current_status": "PRIMARY_THEOREM_TARGET_UNSIGNED",
            "missing_to_promote": "MISSING_SOURCE_FREE_TWO_SLOT_OWNER; MISSING_NO_HIDDEN_SOURCE_THEOREM",
            "impact": "without this, source residual cannot be called zero",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RV1755_1_linear_silence",
            "quantity": "S_cg=D_L S_1+O(D_L^2)",
            "formula_or_description": "regular expansion follows if S_cg(0,Y)=0 and source map is C1",
            "current_status": "EXACT_CONDITIONAL_THEOREM_PREMISES_UNSIGNED",
            "missing_to_promote": "MISSING_SOURCE_ZERO; MISSING_SOURCE_MAP_REGULARITY; MISSING_ESTAR_NORM",
            "impact": "gives the desired power route but remains nonclaim",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RV1755_2_finite_bound",
            "quantity": "||R_source||",
            "formula_or_description": "||R_source|| <= C_H A_1 U_B^2 + C_H^2 A_2 U_B^3 in far-local branch",
            "current_status": "FINITE_BOUND_FORM_READY_INPUTS_MISSING",
            "missing_to_promote": "MISSING_C_H; MISSING_A_1; MISSING_A_2; MISSING_P_ARENA; MISSING_SHELL_QUARANTINE",
            "impact": "would convert the gap into a source-backed residual row, not automatic local GR",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RV1755_3_GR_reduction_gap",
            "quantity": "local GR/Newton bridge",
            "formula_or_description": "EH reduction requires source-free positive sectors, silent boundary/history terms, measured-source matching, K_perp control, and arena projections",
            "current_status": "CLOSER_BUT_NOT_CLOSED",
            "missing_to_promote": "MISSING_SOURCE_SILENCE; MISSING_BOUNDARY_NOFLUX; MISSING_KPERP_BOUND; MISSING_SOURCE_NORMALIZATION; MISSING_ARENA_PROJECTIONS",
            "impact": "1755 narrows the first source-current gap but does not derive local GR",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1755_0_derivation_result",
            "decision": "SOURCE_SILENCE_DERIVATION_CONDITIONAL_NOT_PARENT_SIGNED",
            "reason": "the variation route works if the parent action really has a source-free two-slot form, but the corpus still retains shifted-origin, marker, worldtube, boundary, and history-tail counterexamples",
            "next_action": "do not claim S_cg(D_L=0,Y)=0; attack the two-slot owner clauses directly",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1755_1_best_route",
            "decision": "TWO_SLOT_SOURCE_FREE_OWNER_IS_BEST_NEXT_ROUTE",
            "reason": "it is cleaner than fitting a source coefficient because it can make the source term vanish by parent action structure rather than by small-number scoring",
            "next_action": "build 1756 two-slot source-free owner or hidden-source counterexample ledger",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1755_2_fallback",
            "decision": "ESTAR_NORM_ROWS_STAGED_AS_FALLBACK",
            "reason": "if source zero cannot be proved, the least-bad route is a finite A_1/A_2 residual in the exact E* norm used by the local elliptic identity",
            "next_action": "source E, E*, A_1, A_2, C_H, arena projections, and shell quarantine before scoring",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1755_3_claim_status",
            "decision": "NO_LOCAL_GR_OR_NEWTON_CLAIM",
            "reason": "source silence is still unsigned and several sibling residuals remain active",
            "next_action": "keep this checkpoint private and nonclaim",
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
            "gate_id": "GATE1755_0_source_silent_fixed_point",
            "claim": "S_cg(D_L=0,Y)=0 is parent-derived",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_FREE_TWO_SLOT_OWNER_UNSIGNED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1755_1_no_hidden_source",
            "claim": "all hidden source counterexamples are parent-excluded",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_SHIFTED_ORIGIN_MARKER_WORLDTUBE_BOUNDARY_HISTORY_COUNTEREXAMPLES",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1755_2_regular_Estar_source_norm",
            "claim": "S_cg regularity and A_1/A_2 E* norms are sourced",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_ESTAR_A1_A2_REGULARITY_INPUTS_MISSING",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1755_3_finite_source_residual",
            "claim": "R_source finite residual is below local bounds in every arena",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_C_H_ARENA_PROJECTION_AND_SHELL_QUARANTINE_MISSING",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1755_4_local_GR_Newton",
            "claim": "local GR/Newton/PPN/R10/WEP/clock/orbital branch can claim",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_RESIDUAL_AND_SIBLING_LOCAL_RESIDUALS_ACTIVE",
            "claim_allowed": no(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1755_0_primary",
            "next_target": "1756-Y5-R2FR-two-slot-source-free-owner-or-hidden-source-counterexample-ledger.md",
            "script": "scripts/Y5_R2FR_two_slot_source_free_owner_or_hidden_source_counterexample_ledger.py",
            "objective": "attempt to parent-own the two-slot source-free action and exclude shifted origins, marker covectors, matter/worldtube vertices, boundary fluxes, and history tails",
            "success_condition": "either all hidden-source clauses are parent-excluded, or each surviving source channel is converted into an explicit finite residual row",
            "selection_status": "selected",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1755_1_fallback",
            "next_target": "1756b-Y5-R2FR-E-star-source-norm-runner-and-arena-projection-ledger.md",
            "script": "scripts/Y5_R2FR_E_star_source_norm_runner_and_arena_projection_ledger.py",
            "objective": "if source-zero cannot be proved, source E/E*/A_1/A_2/C_H and arena projection rows for a finite nonclaim residual",
            "success_condition": "finite source residual rows parse with real units, source paths, and valid_for_claim=false until bounds are met",
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
        "theorem_attempt": theorem_attempt_rows(),
        "two_slot_owner_audit": two_slot_owner_audit_rows(),
        "estar_norm_acquisition": estar_norm_acquisition_rows(),
        "residual_status": residual_status_rows(),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1755_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1755_{key.upper()}.csv")


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
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1755_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1755_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1755*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def theorem_route_written(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["theorem_id"] == "SSF1755_1_two_slot_variation_route"
        and "S_parent" in row["mathematical_statement"]
        and row["derivation_status"] == "EXACT_CONDITIONAL_VARIATION_ROUTE"
        for row in rows_map["theorem_attempt"]
    )


def theorem_not_promoted(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["theorem_id"] == "SSF1755_5_verdict"
        and row["derivation_status"] == "DERIVATION_ATTEMPT_FAILS_CURRENT_PARENT_SIGNATURE"
        for row in rows_map["theorem_attempt"]
    )


def hidden_source_blocks_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["audit_id"] == "TSO1755_4_no_linear_marker"
        and row["current_status"] == "COUNTEREXAMPLES_RETAINED"
        for row in rows_map["two_slot_owner_audit"]
    ) and any(
        row["audit_id"] == "TSO1755_5_boundary_history_tail"
        and "MISSING_BOUNDARY_NOFLUX" in row["missing_input"]
        for row in rows_map["two_slot_owner_audit"]
    )


def estar_rows_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["estar_norm_acquisition"]
    return len(rows) >= 8 and all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in rows)


def finite_bound_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["residual_id"] == "RV1755_2_finite_bound"
        and "U_B^2" in row["formula_or_description"]
        and row["current_status"] == "FINITE_BOUND_FORM_READY_INPUTS_MISSING"
        for row in rows_map["residual_status"]
    )


def residual_active(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["residual_id"] == "RV1755_0_source_zero"
        and row["current_status"] == "PRIMARY_THEOREM_TARGET_UNSIGNED"
        for row in rows_map["residual_status"]
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
    next_rows = rows_map["next_target"]

    validation = [
        check("VAL1755_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1755_1_needles_present", all(row["needles_present"] == "True" for row in sources), "required source needles are present", "one or more source needles missing"),
        check("VAL1755_2_theorem_route_written", theorem_route_written(rows_map), "two-slot variation route written", "two-slot variation route missing"),
        check("VAL1755_3_theorem_not_promoted", theorem_not_promoted(rows_map), "source-silent theorem remains parent unsigned", "source-silent theorem accidentally promoted"),
        check("VAL1755_4_hidden_source_blocks", hidden_source_blocks_retained(rows_map), "hidden-source counterexamples retained", "hidden-source blockers missing"),
        check("VAL1755_5_estar_rows_nonclaim", estar_rows_nonclaim(rows_map), "E*/A_1/A_2 acquisition rows remain nonclaim", "E* acquisition rows missing or promoted"),
        check("VAL1755_6_finite_bound_retained", finite_bound_retained(rows_map), "finite U_B^2 source-bound form retained", "finite source-bound form missing"),
        check("VAL1755_7_residual_active", residual_active(rows_map), "source residual remains active", "source residual was accidentally closed"),
        check("VAL1755_8_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claims), "all claim gates remain blocked", "one or more claim gates opened"),
        check("VAL1755_9_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check("VAL1755_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check("VAL1755_11_decision_next", any(row["decision_id"] == "DEC1755_1_best_route" and row["decision"] == "TWO_SLOT_SOURCE_FREE_OWNER_IS_BEST_NEXT_ROUTE" for row in rows_map["decision"]), "decision selects two-slot source-free owner route", "best-next decision missing"),
        check("VAL1755_12_next_selected", any(row["route_id"] == "NEXT1755_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selected", "next target missing"),
        check("VAL1755_13_csv_parse", parsed_ok, "all generated 1755 CSVs parse", "one or more generated 1755 CSVs failed to parse"),
        check("VAL1755_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1755_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1755_16_formalization_untouched", formalization_untouched(), "no 1755 outputs found under formalization-workbench", "1755 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1755_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1755 source-silent fixed point or E* source norm row checkpoint" if overall else "one or more 1755 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1755 tries the derivation-first route for `S_cg(D_L=0,Y)=0`.",
        "- The clean theorem exists conditionally: a source-free two-slot parent action with quotient-blind matter makes `X=0` stationary and gives source silence.",
        "- The current corpus does not yet parent-sign the dangerous clauses: shifted origins, marker covectors, matter/worldtube vertices, boundary fluxes, and history tails remain legal counterexamples.",
        "- The fallback is now precise: source `E`, `E*`, `A_1`, `A_2`, `C_H`, arena projections, and shell quarantine before any finite residual can be scored.",
        "- No local-GR, Newton, PPN, WEP, clock, orbital, R10, `q_loc=0`, or public claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Source-Silent Fixed Point Theorem Attempt",
        markdown_table(rows_map["theorem_attempt"], ["theorem_id", "premise_or_step", "mathematical_statement", "derivation_status", "consequence", "blocker"]),
        "",
        "## Two-Slot Source-Free Owner Audit",
        markdown_table(rows_map["two_slot_owner_audit"], ["audit_id", "clause", "required_signature", "current_status", "failure_mode_if_missing", "missing_input"]),
        "",
        "## E-star Source Norm Acquisition",
        markdown_table(rows_map["estar_norm_acquisition"], ["input_id", "quantity", "role", "required_form", "current_status"]),
        "",
        "## Residual Status",
        markdown_table(rows_map["residual_status"], ["residual_id", "quantity", "formula_or_description", "current_status", "missing_to_promote"]),
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
        "This is a useful failed proof, not a dead end. We now know the exact door: if the parent action truly owns a two-slot, source-free local sector with quotient-blind matter and no hidden marker/boundary/history source, the local source current dies at the fixed point. If that door will not open, the project must stop pretending the source is zero and instead carry a real `E*` finite residual. The best next move is therefore 1756: attack the two-slot owner clauses directly.",
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
    doc_path = ROOT / "1755-Y5-R2FR-source-silent-fixed-point-theorem-or-E-star-source-norm-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1755_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1755 validation FAIL")
    print("1755 validation PASS")


if __name__ == "__main__":
    main()

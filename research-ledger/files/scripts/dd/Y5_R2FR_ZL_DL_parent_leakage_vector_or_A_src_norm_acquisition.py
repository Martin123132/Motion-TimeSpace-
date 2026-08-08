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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1754"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1754 - Z_L D_L Parent Leakage Vector Or A_src Norm Acquisition"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1754_0_1753_doc",
        "source_key": "1753_handoff",
        "source_path": ROOT / "1753-Y5-R2FR-source-support-parent-invariant-or-A-src-coefficient-row.md",
        "needles": ["p_total = 1 + p_int", "D_L <= C_D U_B"],
    },
    {
        "source_id": "SRC1754_1_123_source_power",
        "source_key": "123_local_source_power_theorem",
        "source_path": FORMALIZATION / "123-local-source-power-theorem.md",
        "needles": ["local_source_power_theorem_form_constructed_not_parent_derived", "S_cg = O(D_L)"],
    },
    {
        "source_id": "SRC1754_2_125_ZL_invariant",
        "source_key": "125_local_leakage_vector",
        "source_path": FORMALIZATION / "125-local-leakage-vector-invariant.md",
        "needles": ["local_leakage_vector_invariant_candidate_defined_not_parent_derived", "D_L <= U_B"],
    },
    {
        "source_id": "SRC1754_3_126_evenness",
        "source_key": "126_scalar_evenness",
        "source_path": FORMALIZATION / "126-scalar-evenness-origin.md",
        "needles": ["scalar_evenness_origin_parity_candidate_not_parent_derived", "signed_leakage_parity"],
    },
    {
        "source_id": "SRC1754_4_127_signed_coordinates",
        "source_key": "127_signed_leakage_coordinates",
        "source_path": FORMALIZATION / "127-signed-leakage-coordinate-map.md",
        "needles": ["signed_leakage_coordinate_map_candidate_defined_symmetry_not_derived", "z_L^A"],
    },
    {
        "source_id": "SRC1754_5_128_symmetry",
        "source_key": "128_leakage_frame_symmetry",
        "source_path": FORMALIZATION / "128-leakage-frame-symmetry.md",
        "needles": ["leakage_frame_symmetry_partial_vector_tensor_only_scalar_channels_block", "scalar_linear_terms_removed = false"],
    },
    {
        "source_id": "SRC1754_6_129_stationarity",
        "source_key": "129_scalar_channel_stationarity",
        "source_path": FORMALIZATION / "129-scalar-channel-stationarity.md",
        "needles": ["scalar_channel_stationarity_not_parent_derived_zLcg_pruned_repair_required", "z_Lcg_pruned_until_reference_derived = true"],
    },
    {
        "source_id": "SRC1754_7_130_repair",
        "source_key": "130_smooth_scalar_repair",
        "source_path": FORMALIZATION / "130-smooth-scalar-channel-repair.md",
        "needles": ["smooth_scalar_channel_repair_clean_closure_not_parent_derived_gradients_open", "D_L = U_B sqrt(S_smooth)"],
    },
    {
        "source_id": "SRC1754_8_802_ZL_gate",
        "source_key": "802_parent_ZL_gate",
        "source_path": ROOT / "802-Y5-R10-parent-ZL-evenness-and-gradient-signature-gate.md",
        "needles": ["D802_0_ZL_parent_signature", "SIG802_1_distance_bound"],
    },
    {
        "source_id": "SRC1754_9_signed_coordinate_run",
        "source_key": "signed_coordinate_run",
        "source_path": FORMALIZATION / "runs" / "20260528-162417-signed-leakage-coordinate-map" / "results" / "coordinate_construction.csv",
        "needles": ["signed_coordinate_bundle", "leakage_metric"],
    },
    {
        "source_id": "SRC1754_10_stationarity_run",
        "source_key": "stationarity_run",
        "source_path": FORMALIZATION / "runs" / "20260528-171053-scalar-channel-stationarity" / "results" / "mechanism_tests.csv",
        "needles": ["parent_variational_extremum", "smooth_even_invariant_repair"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1754_SOURCE_REGISTER.csv",
    "leakage_vector_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1754_ZL_DL_LEAKAGE_VECTOR_CONTRACT.csv",
    "source_silence_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1754_SOURCE_SILENCE_THEOREM_ATTEMPT.csv",
    "asrc_norm_acquisition": RESIDUALS / "P8_Y5_PARENT_QLOC_1754_ASRC_NORM_ACQUISITION_LEDGER.csv",
    "residual_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1754_SOURCE_RESIDUAL_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1754_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1754_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1754_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1754_VALIDATION.csv",
}


COPY_MAP = {
    "leakage_vector_contract": "R2FR_1754_ZL_DL_LEAKAGE_VECTOR_CONTRACT.csv",
    "source_silence_theorem": "R2FR_1754_SOURCE_SILENCE_THEOREM_ATTEMPT.csv",
    "asrc_norm_acquisition": "R2FR_1754_ASRC_NORM_ACQUISITION_LEDGER.csv",
    "residual_status": "R2FR_1754_SOURCE_RESIDUAL_STATUS.csv",
    "decision": "R2FR_1754_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1754_CLAIM_GATE.csv",
    "next_target": "R2FR_1754_NEXT_TARGET.csv",
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
                "used_for": "1754 Z_L/D_L parent leakage vector and A_src norm acquisition",
                "timestamp_utc": UTC,
            }
        )
    return rows


def leakage_vector_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": "ZLC1754_0_signed_coordinates",
            "clause": "signed primitive leakage coordinates",
            "mathematical_form": "z_L^A = {z_theta, z_dotB, z_Bgrad_i, z_grad_i, z_shear_ij, z_rot_ij}; z_Lcg pruned until its reference is parent-derived",
            "conditional_result": "candidate coordinate bundle exists without sector labels",
            "current_status": "CANDIDATE_NOT_PARENT_SIGNED",
            "blocker": "MISSING_PARENT_COARSE_GRAINING_MAP_AND_FRAME_REFERENCE",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "ZLC1754_1_bounded_map",
            "clause": "bounded leakage map",
            "mathematical_form": "Z_L^A = U_B H_L^A(X_B), ||H_L||_G <= C_H",
            "conditional_result": "if G_AB is positive and H_L bounded, then D_L=sqrt(G_AB Z_L^A Z_L^B) <= C_H U_B",
            "current_status": "EXACT_CONDITIONAL_DISTANCE_BOUND",
            "blocker": "MISSING_G_AB_PARENT_METRIC; MISSING_H_L_BOUND; MISSING_C_H_VALUE",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "ZLC1754_2_gradient_bound",
            "clause": "far-local leakage-gradient bound",
            "mathematical_form": "nabla Z_L=(nabla U_B)H_L + U_B nabla H_L",
            "conditional_result": "if nabla U_B=O(U_B/L_B) and nabla H_L=O(1/L_B), then nabla Z_L=O(U_B/L_B)",
            "current_status": "CONDITIONAL_FAR_LOCAL_GRADIENT_BOUND",
            "blocker": "MISSING_L_B; MISSING_H_L_LOG_GRADIENT; TRANSITION_SHELL_U_B_ORDER_ONE_NOT_SAFE",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "ZLC1754_3_scalar_evenness_limit",
            "clause": "evenness/stationarity limitation",
            "mathematical_form": "vector/tensor signed channels can be even by local isotropy; scalar channels z_theta and z_dotB can remain linear unless parent stationarity holds",
            "conditional_result": "Z_L route only partially closes evenness; true scalar linears remain blockers",
            "current_status": "SCALAR_CHANNEL_BLOCK_RETAINED",
            "blocker": "MISSING_PARENT_SCALAR_STATIONARITY_OR_SMOOTH_QUADRATIC_SOURCE_MAP",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "ZLC1754_4_verdict",
            "clause": "Z_L/D_L parent leakage vector verdict",
            "mathematical_form": "Z_L/D_L is a legitimate candidate contract, not a parent theorem",
            "conditional_result": "contract can support R_source=O(U_B^2) only after source-silence and norm rows are signed",
            "current_status": "CONTRACT_BUILT_PARENT_SIGNATURE_MISSING",
            "blocker": "MISSING_Z_L_PARENT_SIGNATURE; MISSING_SOURCE_SILENT_FIXED_POINT; MISSING_A_SRC_NORM",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def source_silence_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SST1754_0_source_zero_at_fixed_point",
            "premise_or_step": "source-silent fixed point",
            "mathematical_statement": "S_cg(D_L=0,Y)=0",
            "consequence": "regularity then gives S_cg = D_L S_1 + O(D_L^2)",
            "status": "NEEDED_NOT_PARENT_DERIVED",
            "blocker": "MISSING_PARENT_SOURCE_SILENCE_AT_LOCAL_FIXED_POINT",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SST1754_1_regular_source_map",
            "premise_or_step": "regular source expansion",
            "mathematical_statement": "S_cg(D_L,Y) is C^1 or analytic in D_L near the local branch",
            "consequence": "S_1 is a finite coefficient rather than a singular hidden source",
            "status": "REGULARITY_REQUIRED_NOT_SOURCED",
            "blocker": "MISSING_SOURCE_MAP_REGULARITY_AND_NORM",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SST1754_2_linear_silence_bound",
            "premise_or_step": "combine source silence with D_L bound",
            "mathematical_statement": "D_L<=C_H U_B and ||S_1||_{E*}<=A_1 imply ||R_source|| <= C_H A_1 U_B^2 + O(U_B^3)",
            "consequence": "source residual gains p_total>=2 without exact zero",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "blocker": "MISSING_C_H; MISSING_A_1; MISSING_ESTAR_NORM",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SST1754_3_transition_shell_warning",
            "premise_or_step": "far-local restriction",
            "mathematical_statement": "the U_B^2 gain is a far-local statement; transition shells with U_B=O(1) need exact cancellation/projector/quarantine",
            "consequence": "do not use this theorem as a universal local-GR pass",
            "status": "SHELL_BLOCK_RETAINED",
            "blocker": "MISSING_TRANSITION_SHELL_PROJECTOR_OR_EXACT_CANCELLATION",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "SST1754_4_verdict",
            "premise_or_step": "source silence theorem verdict",
            "mathematical_statement": "1754 has the theorem contract for p_total>=2 but not the parent proof or coefficient norms",
            "consequence": "R_source remains finite nonclaim input rather than derived local nohair",
            "status": "THEOREM_CONTRACT_ONLY_NONCLAIM",
            "blocker": "MISSING_SOURCE_SILENT_FIXED_POINT_OR_REAL_A_SRC_NORM",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def asrc_norm_acquisition_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": "ANA1754_0_GAB",
            "quantity": "G_AB",
            "role": "positive leakage metric defining D_L^2",
            "required_form": "source-backed positive matrix/tensor on signed leakage coordinate bundle",
            "current_status": "MISSING_PARENT_METRIC",
            "claim_effect": "without G_AB, D_L is a candidate norm not a parent scalar",
            "source_path": str(FORMALIZATION / "125-local-leakage-vector-invariant.md"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "ANA1754_1_CH",
            "quantity": "C_H",
            "role": "bound in ||H_L||_G<=C_H and D_L<=C_H U_B",
            "required_form": "numeric universal upper bound with source path and local-domain assumptions",
            "current_status": "MISSING_H_BOUND",
            "claim_effect": "without C_H, the source residual coefficient cannot score",
            "source_path": str(FORMALIZATION / "125-local-leakage-vector-invariant.md"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "ANA1754_2_A1",
            "quantity": "A_1 = ||S_1||_{E*}",
            "role": "linear source coefficient in S_cg=D_L S_1+O(D_L^2)",
            "required_form": "finite source-backed E* dual norm in the same local elliptic functional used by 1751",
            "current_status": "MISSING_A1_ESTAR_NORM",
            "claim_effect": "without A_1, p_total>=2 is still only a shape",
            "source_path": str(FORMALIZATION / "123-local-source-power-theorem.md"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "ANA1754_3_A2",
            "quantity": "A_2 = ||O(D_L^2)||_{E*}/D_L^2",
            "role": "remainder coefficient in finite source bound",
            "required_form": "finite source-backed second-order remainder norm",
            "current_status": "MISSING_A2_REMAINDER_NORM",
            "claim_effect": "needed to prevent a hidden singular remainder",
            "source_path": str(FORMALIZATION / "123-local-source-power-theorem.md"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "ANA1754_4_Estar",
            "quantity": "E* norm",
            "role": "dual norm for source term in coercive local elliptic residual",
            "required_form": "same norm as 1751 energy identity; source path to parent/open-system functional",
            "current_status": "MISSING_ESTAR_NORM_OWNER",
            "claim_effect": "prevents mixing incompatible source norms",
            "source_path": str(ROOT / "1751-Y5-R2FR-parent-elliptic-functional-ownership-or-finite-residual-vector.md"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "ANA1754_5_shell_projector",
            "quantity": "transition shell local projector",
            "role": "decides whether far-local Z_L suppression can be applied or shell current must be quarantined",
            "required_form": "parent identity/projection theorem, not a sector label or after-fit switch",
            "current_status": "MISSING_TRANSITION_SHELL_PROJECTOR",
            "claim_effect": "blocks universal local-GR use of far-local suppression",
            "source_path": str(ROOT / "802-Y5-R10-parent-ZL-evenness-and-gradient-signature-gate.md"),
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
            "residual_id": "RV1754_0_ZL_contract",
            "parent_residual_id": "RV1753_1_parent_invariant",
            "quantity": "Z_L/D_L source route",
            "formula_or_description": "Z_L=U_B H_L and D_L<=C_H U_B gives the distance side of source suppression conditionally",
            "current_status": "CONTRACT_READY_PARENT_SIGNATURE_MISSING",
            "missing_to_promote": "MISSING_G_AB; MISSING_H_BOUND; MISSING_PARENT_COORDINATE_MAP",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RV1754_1_source_silence",
            "parent_residual_id": "RV1753_1_parent_invariant",
            "quantity": "S_cg linear silence",
            "formula_or_description": "S_cg(D_L=0,Y)=0 and regularity imply S_cg=D_L S_1+O(D_L^2)",
            "current_status": "THEOREM_SHAPE_READY_PARENT_SOURCE_ZERO_MISSING",
            "missing_to_promote": "MISSING_SOURCE_SILENT_FIXED_POINT; MISSING_A1_NORM",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RV1754_2_finite_bound",
            "parent_residual_id": "RV1753_2_A_src_thresholds",
            "quantity": "R_source finite bound",
            "formula_or_description": "||R_source|| <= C_H A_1 U_B^2 + C_H^2 A_2 U_B^3 in far-local branch",
            "current_status": "FINITE_BOUND_FORM_DERIVED_INPUTS_MISSING",
            "missing_to_promote": "MISSING_C_H; MISSING_A1; MISSING_A2; MISSING_ESTAR_NORM; MISSING_ARENA_PROJECTION",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RV1754_3_verdict",
            "parent_residual_id": "RV1751_10_verdict",
            "quantity": "source residual",
            "formula_or_description": "source residual is now a precise theorem-contract/input-acquisition problem, not an undefined gap",
            "current_status": "SOURCE_RESIDUAL_ACTIVE_NONCLAIM_CONTRACT_SHARPENED",
            "missing_to_promote": "MISSING_SOURCE_SILENT_FIXED_POINT_OR_REAL_A_SRC_NORM",
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
            "decision_id": "DEC1754_0_ZL_status",
            "decision": "ZL_DL_CONTRACT_BUILT_NOT_PARENT_SIGNED",
            "reason": "signed coordinates, bounded map, and distance bound are theorem-shaped but the parent metric/map/bounds are missing",
            "next_action": "do not claim S_cg=O(U_B) from Z_L yet",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1754_1_source_status",
            "decision": "SOURCE_SILENT_FIXED_POINT_IS_PRIMARY_MISSING_STEP",
            "reason": "D_L<=U_B is not enough; R_source needs S_cg(D_L=0)=0 and a regular finite S_1 norm",
            "next_action": "try to derive source-silent fixed point or source the E* norm coefficients",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1754_2_shell_status",
            "decision": "FAR_LOCAL_ONLY_TRANSITION_SHELL_BLOCK_RETAINED",
            "reason": "U_B^2 suppression helps far-local domains, but transition shells with U_B=O(1) still need a projector/quarantine theorem",
            "next_action": "keep shell projector as separate active residual, not silently erased by Z_L",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1754_3_best_next",
            "decision": "TARGET_SOURCE_SILENT_FIXED_POINT_OR_ESTAR_NORM",
            "reason": "the fastest source-residual win is either S_cg(D_L=0)=0 from parent dynamics or a real E* norm for S_1/A_src",
            "next_action": "build 1755 source-silent fixed point theorem or E* source norm row",
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
            "gate_id": "GATE1754_0_ZL",
            "claim": "Z_L/D_L is parent-owned",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_PARENT_COORDINATE_MAP_METRIC_AND_BOUNDS",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1754_1_source_silence",
            "claim": "S_cg(D_L=0)=0 is parent-derived",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_SILENT_FIXED_POINT",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1754_2_A_src_norm",
            "claim": "A_src/A_1/A_2 are sourced in E* norm",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_ESTAR_SOURCE_NORM",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1754_3_shell",
            "claim": "far-local source suppression controls transition shells",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_TRANSITION_SHELL_PROJECTOR_OR_QUARANTINE",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1754_4_local_reentry",
            "claim": "local GR/Newton/PPN/R10/WEP branch can claim",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_SOURCE_RESIDUAL_ACTIVE_NONCLAIM",
            "claim_allowed": no(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1754_0_primary",
            "next_target": "1755-Y5-R2FR-source-silent-fixed-point-theorem-or-E-star-source-norm-row.md",
            "script": "scripts/Y5_R2FR_source_silent_fixed_point_theorem_or_E_star_source_norm_row.py",
            "objective": "try to derive S_cg(D_L=0,Y)=0 and source-map regularity from parent dynamics; fallback to E* source norm acquisition rows for S_1/A_1 and A_2",
            "success_condition": "source residual obtains parent-signed linear silence or a real finite A_src/E* norm row while all local claims remain blocked",
            "selection_status": "selected",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1754_1_fallback",
            "next_target": "1755b-Y5-R2FR-transition-shell-projector-or-source-residual-quarantine.md",
            "script": "scripts/Y5_R2FR_transition_shell_projector_or_source_residual_quarantine.py",
            "objective": "separate far-local Z_L source suppression from transition-shell local projection, or keep shell residual as explicit quarantine row",
            "success_condition": "shell contribution is parent-projected away from local metric branch or retained as finite nonclaim residual",
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
        "leakage_vector_contract": leakage_vector_contract_rows(),
        "source_silence_theorem": source_silence_theorem_rows(),
        "asrc_norm_acquisition": asrc_norm_acquisition_rows(),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1754_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1754_{key.upper()}.csv")


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
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1754_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1754_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1754*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def contract_built_not_signed(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["contract_id"] == "ZLC1754_4_verdict"
        and row["current_status"] == "CONTRACT_BUILT_PARENT_SIGNATURE_MISSING"
        for row in rows_map["leakage_vector_contract"]
    )


def distance_bound_present(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["contract_id"] == "ZLC1754_1_bounded_map"
        and "D_L=sqrt" in row["conditional_result"]
        and "C_H U_B" in row["conditional_result"]
        for row in rows_map["leakage_vector_contract"]
    )


def source_silence_missing(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["theorem_id"] == "SST1754_0_source_zero_at_fixed_point"
        and row["status"] == "NEEDED_NOT_PARENT_DERIVED"
        for row in rows_map["source_silence_theorem"]
    )


def finite_bound_form_present(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["theorem_id"] == "SST1754_2_linear_silence_bound"
        and "U_B^2" in row["mathematical_statement"]
        and row["status"] == "EXACT_CONDITIONAL_THEOREM"
        for row in rows_map["source_silence_theorem"]
    )


def acquisition_rows_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["asrc_norm_acquisition"]
    return len(rows) >= 6 and all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in rows)


def source_residual_active(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["residual_id"] == "RV1754_3_verdict"
        and row["current_status"] == "SOURCE_RESIDUAL_ACTIVE_NONCLAIM_CONTRACT_SHARPENED"
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
        check("VAL1754_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1754_1_needles_present", all(row["needles_present"] == "True" for row in sources), "required source needles are present", "one or more source needles missing"),
        check("VAL1754_2_contract_built_not_signed", contract_built_not_signed(rows_map), "Z_L/D_L contract built but parent signature missing", "Z_L/D_L verdict missing or promoted"),
        check("VAL1754_3_distance_bound_present", distance_bound_present(rows_map), "conditional D_L<=C_H U_B distance bound present", "distance bound theorem missing"),
        check("VAL1754_4_source_silence_missing", source_silence_missing(rows_map), "source-silent fixed point remains missing", "source-silent fixed point was accidentally promoted"),
        check("VAL1754_5_finite_bound_form", finite_bound_form_present(rows_map), "finite R_source U_B^2 bound form written", "finite source bound theorem missing"),
        check("VAL1754_6_acquisition_nonclaim", acquisition_rows_nonclaim(rows_map), "A_src/E* acquisition rows remain nonclaim", "A_src acquisition rows missing or promoted"),
        check("VAL1754_7_residual_active", source_residual_active(rows_map), "source residual remains active and sharpened", "source residual verdict missing"),
        check("VAL1754_8_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claims), "all claim gates remain blocked", "one or more claim gates opened"),
        check("VAL1754_9_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check("VAL1754_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check("VAL1754_11_decision_next", any(row["decision_id"] == "DEC1754_3_best_next" and row["decision"] == "TARGET_SOURCE_SILENT_FIXED_POINT_OR_ESTAR_NORM" for row in rows_map["decision"]), "decision selects source-silent fixed point/E* norm target", "best-next decision missing"),
        check("VAL1754_12_next_selected", any(row["route_id"] == "NEXT1754_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selected", "next target missing"),
        check("VAL1754_13_csv_parse", parsed_ok, "all generated 1754 CSVs parse", "one or more generated 1754 CSVs failed to parse"),
        check("VAL1754_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1754_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1754_16_formalization_untouched", formalization_untouched(), "no 1754 outputs found under formalization-workbench", "1754 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1754_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1754 Z_L/D_L leakage vector or A_src norm acquisition checkpoint" if overall else "one or more 1754 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1754 builds the exact theorem contract for the `Z_L/D_L` route, but does not promote it to a parent-derived result.",
        "- Conditional win: if `Z_L^A = U_B H_L^A`, `G_AB` is positive, and `||H_L||_G <= C_H`, then `D_L <= C_H U_B`.",
        "- Source win still needs one missing theorem: `S_cg(D_L=0,Y)=0` plus source-map regularity, giving `S_cg = D_L S_1 + O(D_L^2)`.",
        "- If those hold, the source residual becomes `||R_source|| <= C_H A_1 U_B^2 + C_H^2 A_2 U_B^3` in the far-local branch.",
        "- Transition shells remain outside this win; `U_B=O(1)` shells still need a parent projector, exact cancellation, or quarantine.",
        "- No local-GR, Newton, PPN, WEP, clock, orbital, R10, `q_loc=0`, or public claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Z_L/D_L Leakage Vector Contract",
        markdown_table(rows_map["leakage_vector_contract"], ["contract_id", "clause", "mathematical_form", "conditional_result", "current_status", "blocker"]),
        "",
        "## Source Silence Theorem Attempt",
        markdown_table(rows_map["source_silence_theorem"], ["theorem_id", "premise_or_step", "mathematical_statement", "consequence", "status", "blocker"]),
        "",
        "## A_src Norm Acquisition Ledger",
        markdown_table(rows_map["asrc_norm_acquisition"], ["input_id", "quantity", "role", "required_form", "current_status"]),
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
        "This is progress in the Grossmann sense: the missing mathematics is now smaller and named. `Z_L` can give the right distance scaling, but the source residual does not shrink unless the local fixed point is genuinely source-silent and the source coefficient lives in the same dual norm as the 1751 energy identity. The next move is therefore not more switch algebra; it is the source-silent fixed-point theorem or a real `E*` source-norm row.",
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
    doc_path = ROOT / "1754-Y5-R2FR-ZL-DL-parent-leakage-vector-or-A-src-norm-acquisition.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1754_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1754 validation FAIL")
    print("1754 validation PASS")


if __name__ == "__main__":
    main()

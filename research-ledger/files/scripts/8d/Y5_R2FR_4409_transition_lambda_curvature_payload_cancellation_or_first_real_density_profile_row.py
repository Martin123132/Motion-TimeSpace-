from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from Eprofile_source_shadow_gate import evaluate_eprofile_bound_rows, read_csv, write_csv  # noqa: E402
from finite_payload_vector_runner import evaluate_payload_rows  # noqa: E402
from lambda_curvature_source_gate import (  # noqa: E402
    evaluate_bound_rows,
    evaluate_cancellation_rows,
    evaluate_ricci_zero_rows,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4409"
CLAIM_ID = "L-250"
MARKER = "PPC4161_TRANSITION_LAMBDA_CURVATURE_PAYLOAD_CANCELLATION_OR_FIRST_REAL_DENSITY_PROFILE_ROW_4409"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_LAMBDA_CURVATURE_PAYLOAD_CANCELLATION_OR_FIRST_REAL_DENSITY_PROFILE_ROW_4409"
DECISION = "LAMBDA_CURVATURE_SOURCE_REBASED_TO_RICCI_UU_PAYLOAD_RUNNERS_CURRENT_CHAIN_NONCLAIM"
NEXT_TARGET = "4410-Y5-R2FR-transition-local-Ricci-survivor-vector-zero-or-first-real-Ruu-source-row.md"

FORMAL_PATH = FORMAL / "425-PPC4161-transition-lambda-curvature-payload-cancellation-or-first-real-density-profile-row.md"
DOC_PATH = POST / "4409-Y5-R2FR-transition-lambda-curvature-payload-cancellation-or-first-real-density-profile-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4409_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
LAMBDA_GATE_PATH = SCRIPT_DIR / "lambda_curvature_source_gate.py"
PAYLOAD_RUNNER_PATH = SCRIPT_DIR / "finite_payload_vector_runner.py"
EPROFILE_GATE_PATH = SCRIPT_DIR / "Eprofile_source_shadow_gate.py"

RICCI_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4409_RICCI_ZERO_GATE_INPUT.csv"
RICCI_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4409_RICCI_ZERO_GATE_OUTPUT.csv"
CANCELLATION_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4409_PARENT_CANCELLATION_INPUT.csv"
CANCELLATION_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4409_PARENT_CANCELLATION_OUTPUT.csv"
LAMBDA_BOUND_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4409_LAMBDA_CURVATURE_BOUND_INPUT.csv"
LAMBDA_BOUND_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4409_LAMBDA_CURVATURE_BOUND_OUTPUT.csv"
PAYLOAD_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4409_FINITE_PAYLOAD_VECTOR_INPUT.csv"
PAYLOAD_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4409_FINITE_PAYLOAD_VECTOR_OUTPUT.csv"
PROFILE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4409_PROFILE_FALLBACK_INPUT.csv"
PROFILE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4409_PROFILE_FALLBACK_OUTPUT.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4408 = SOURCE_DIR / "P8_Y5_R2FR_4408_NEXT_TARGET.csv"
FORMAL_424 = FORMAL / "424-PPC4161-transition-affine-double-divergence-owner-or-first-real-density-profile-row.md"
FORMAL_416 = FORMAL / "416-PPC4161-transition-composite-US-parent-functional-or-finite-payload-vector-runner.md"
FORMAL_417 = FORMAL / "417-PPC4161-transition-curvature-sourced-lambda-payload-bound-or-parent-cancellation.md"
FORMAL_418 = FORMAL / "418-PPC4161-transition-Ricci-uu-local-vacuum-equation-or-first-real-Etrace-bound-row.md"
FORMAL_419 = FORMAL / "419-PPC4161-transition-Lambda-eff-residual-zero-or-local-cosmological-payload-bound.md"
DERIV_4401 = SOURCE_DIR / "P8_Y5_R2FR_4401_LAMBDA_SOURCE_DERIVATIONS.csv"
BOUND_4401 = SOURCE_DIR / "P8_Y5_R2FR_4401_LAMBDA_CURVATURE_BOUND_OUTPUT.csv"
RICCI_4401 = SOURCE_DIR / "P8_Y5_R2FR_4401_RICCI_ZERO_GATE_OUTPUT.csv"
PAYLOAD_4401 = SOURCE_DIR / "P8_Y5_R2FR_4401_FINITE_PAYLOAD_VECTOR_OUTPUT.csv"

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4409_00_4408_next": (
        NEXT_4408,
        "lambda_S curvature source",
        "4408 handoff to lambda-curvature cancellation/bound or real profile row.",
    ),
    "SRC4409_01_4408_formal": (
        FORMAL_424,
        "U[sigma]R sources lambda_S",
        "4408 identifies the current obstruction.",
    ),
    "SRC4409_02_4401_formal": (
        FORMAL_417,
        "R_uu = 0",
        "4401 narrows the obstruction to Ricci-normal payload.",
    ),
    "SRC4409_03_trace_source": (
        DERIV_4401,
        "LCS4401_0_trace_electric_source_is_Ricci_uu",
        "Trace-electric curvature source classification.",
    ),
    "SRC4409_04_elliptic_bound": (
        DERIV_4401,
        "LCS4401_3_elliptic_lambda_payload_bound",
        "Elliptic payload bound law.",
    ),
    "SRC4409_05_ricci_trace": (
        FORMAL_418,
        "R_uu = E_res_uu - 1/2 g_uu E_res + Lambda_eff g_uu",
        "4402 shows matter vacuum alone is not enough.",
    ),
    "SRC4409_06_residual_vector": (
        FORMAL_419,
        "retained local residual payload is c_Gamma, c_R2/M_R, Lambda_eff",
        "4403 names the survivor vector feeding R_uu.",
    ),
    "SRC4409_07_4401_bound_output": (
        BOUND_4401,
        "LCB4401_0_missing_live_Etrace_bound",
        "Prior lambda-bound runner blocks without real F_E/R_uu source.",
    ),
    "SRC4409_08_4401_ricci_output": (
        RICCI_4401,
        "RZ4401_1_local_vacuum_template",
        "Prior Ricci zero template blocks on parent metric equation.",
    ),
    "SRC4409_09_4401_payload_output": (
        PAYLOAD_4401,
        "FPV4401_0_lambda_bound_insert_smoke_nonclaim",
        "Finite payload vector can consume the lambda score.",
    ),
    "SRC4409_10_lambda_gate": (
        LAMBDA_GATE_PATH,
        "def evaluate_bound_rows",
        "Executable lambda curvature-source gate.",
    ),
    "SRC4409_11_payload_runner": (
        PAYLOAD_RUNNER_PATH,
        "def evaluate_payload_rows",
        "Executable finite payload vector runner.",
    ),
    "SRC4409_12_profile_gate": (
        EPROFILE_GATE_PATH,
        "def evaluate_eprofile_bound_rows",
        "Executable density-profile fallback gate.",
    ),
}


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def locate(path: Path, needle: str) -> Tuple[bool, int]:
    if not path.exists():
        return False, -1
    for line_number, line in enumerate(text(path).splitlines(), 1):
        if needle in line:
            return True, line_number
    return False, -1


def csv_line(row: Iterable[str]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(list(row))
    return buffer.getvalue()


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def markdown_table(rows: List[Dict[str, object]]) -> str:
    if not rows:
        return ""
    fields = list(rows[0].keys())
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    current = text(path)
    if marker in current:
        return
    path.write_text(current.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    current = text(path)
    if f"\n{claim_id}," in current:
        return
    if current and not current.endswith("\n"):
        current += "\n"
    path.write_text(current + csv_line(row), encoding="utf-8")


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        found, line_number = locate(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": found,
                "line_number": line_number,
                "role": role,
                "valid_for_claim": False,
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "LC4409_0_current_chain_rebase",
            "object": "lambda_S curvature source",
            "statement": "In the 4408 sigma/electric owner route, the curvature source in the lambda_S equation is the Ricci-normal trace R_uu, not arbitrary Weyl tidal curvature.",
            "derivation": "For trace-electric S^{ij}=c^2h^{ij}sigma_S, partial(U.R)/partial sigma_S is proportional to c^2 h^{ij}R_{0i0j}. In the local rest frame this is R_{mu nu}u^mu u^nu up to projector/extrinsic conventions.",
            "result": "The obstruction is narrower and more attackable than generic curvature.",
            "status": "TRACE_ELECTRIC_SOURCE_REBASED_TO_RICCI_UU",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "LC4409_1_local_vacuum_zero_route",
            "object": "homogeneous lambda branch",
            "statement": "If the parent local metric equation gives R_uu=0 on the same tau/coframe support, with matter excluded/bounded and projector/boundary terms silent, the lambda_S equation returns to the homogeneous 4393 branch.",
            "derivation": "Delta_h^dagger lambda_S = -K_E c^2 R_uu + B_projector + B_boundary. Setting these terms to zero leaves the elliptic uniqueness condition for lambda_S=0.",
            "result": "The clean proof target is parent Ricci-vacuum/residual silence, not a tuned cancellation.",
            "status": "Ruu_ZERO_SUFFICIENT_CONDITION_DERIVED_NOT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "LC4409_2_no_counterterm_shortcut",
            "object": "parent cancellation",
            "statement": "An opposite U[sigma]R term is not an acceptable cancellation unless it arises from the same parent variation, preserves the density-owner term, and cancels Ward/boundary/EM side terms without a tuned coefficient.",
            "derivation": "A hand-added negative kernel either deletes the improvement mechanism or introduces an unsourced counterterm.",
            "result": "The cancellation route is gated but currently blocked.",
            "status": "TRIVIAL_COUNTERTERM_REJECTED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "LC4409_3_elliptic_payload_bound",
            "object": "finite lambda payload",
            "statement": "If R_uu is not zero, the finite branch is ||lambda_S||_2 <= C_P^2||F_E||_2, ||Dlambda_S||_2 <= C_P||F_E||_2, and ||lambda_S||_{H2} <= C_E||F_E||_2.",
            "derivation": "Use Poincare and elliptic regularity for anchored Dirichlet, zero-mean Neumann, or mixed anchored data.",
            "result": "A real F_E/R_uu source row plus domain constants can now decide whether the branch is numerically safe.",
            "status": "ELLIPTIC_BOUND_RUNNER_REBASED_CURRENT_CHAIN",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "LC4409_4_residual_vector_connection",
            "object": "R_uu source input",
            "statement": "In local matter vacuum, R_uu is sourced by E_res_uu, E_res_trace, Lambda_eff and projector/boundary terms, so those survivor components must be parent-zeroed or sourced.",
            "derivation": "Trace-reverse the conditional local metric equation and set ordinary matter to zero only after keeping residual and Lambda terms.",
            "result": "The next non-circling target is the local Ricci survivor vector or the first real R_uu/F_E source row.",
            "status": "NEXT_TARGET_SHARPENED_TO_RICCI_SURVIVOR_VECTOR",
            "valid_for_claim": False,
        },
    ]


def ricci_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "candidate_id": "RZ4409_0_trace_electric_source_rebased",
            "route": "hij_R0i0j_equals_Ricci_uu_current_chain",
            "trace_electric_identified_as_Ricci_uu": True,
            "local_vacuum_domain_declared": False,
            "parent_metric_equation_Ricci_uu_zero": False,
            "matter_support_excluded_or_bounded": False,
            "projector_extrinsic_terms_bounded": False,
            "boundary_zero_mode_fixed": False,
            "parent_authority": "MISSING_PARENT_SIGNED_RICCI_ZERO_EQUATION",
            "source_path": str(FORMAL_417),
            "input_valid_for_claim": False,
            "notes": "classification imported into 4408/4409 current chain; zero certificate not present",
        },
        {
            "candidate_id": "RZ4409_1_local_vacuum_parent_equation_template",
            "route": "parent_local_vacuum_Ricci_uu_zero",
            "trace_electric_identified_as_Ricci_uu": True,
            "local_vacuum_domain_declared": True,
            "parent_metric_equation_Ricci_uu_zero": False,
            "matter_support_excluded_or_bounded": True,
            "projector_extrinsic_terms_bounded": True,
            "boundary_zero_mode_fixed": True,
            "parent_authority": "MISSING_PARENT_SIGNED_LOCAL_VACUUM_RICCI_EQUATION",
            "source_path": str(FORMAL_418),
            "input_valid_for_claim": False,
            "notes": "serious zero route; blocks only on parent metric equation and claim authority",
        },
        {
            "candidate_id": "RZ4409_2_future_Ricci_zero_smoke",
            "route": "future_parent_Ricci_zero_schema_smoke",
            "trace_electric_identified_as_Ricci_uu": True,
            "local_vacuum_domain_declared": True,
            "parent_metric_equation_Ricci_uu_zero": True,
            "matter_support_excluded_or_bounded": True,
            "projector_extrinsic_terms_bounded": True,
            "boundary_zero_mode_fixed": True,
            "parent_authority": "PARENT_SIGNED_RICCI_ZERO_SMOKE",
            "source_path": str(FORMAL_418),
            "input_valid_for_claim": False,
            "notes": "proves the gate can recognize the route but remains nonclaim",
        },
    ]


def cancellation_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "candidate_id": "CAN4409_0_current_parent_source_owner_search",
            "route": "current_sources_parent_cancellation",
            "parent_counter_source_declared": False,
            "same_parent_variation": False,
            "opposite_kernel_exact": False,
            "no_new_tuned_coefficient": False,
            "does_not_cancel_density_owner": True,
            "boundary_terms_cancel": False,
            "Ward_EM_guard": False,
            "parent_authority": "MISSING_PARENT_SIGNED_COUNTER_SOURCE",
            "source_path": str(FORMAL_416),
            "input_valid_for_claim": False,
            "notes": "current sources expose the obstruction but do not contain a signed opposite parent source",
        },
        {
            "candidate_id": "CAN4409_1_trivial_negative_U_counterterm_trap",
            "route": "add_minus_U_sigma_R_by_hand",
            "parent_counter_source_declared": True,
            "same_parent_variation": True,
            "opposite_kernel_exact": True,
            "no_new_tuned_coefficient": False,
            "does_not_cancel_density_owner": False,
            "boundary_terms_cancel": False,
            "Ward_EM_guard": False,
            "parent_authority": "NO_AUTHORITY_TRIVIAL_COUNTERTERM",
            "source_path": str(FORMAL_416),
            "input_valid_for_claim": False,
            "notes": "detected trap: cancellation by deleting/tuning the same mechanism is not a derivation",
        },
        {
            "candidate_id": "CAN4409_2_future_source_owner_cancellation_certificate",
            "route": "same_parent_stress_improvement_sector_opposite_kernel",
            "parent_counter_source_declared": True,
            "same_parent_variation": False,
            "opposite_kernel_exact": False,
            "no_new_tuned_coefficient": False,
            "does_not_cancel_density_owner": True,
            "boundary_terms_cancel": False,
            "Ward_EM_guard": False,
            "parent_authority": "MISSING_PARENT_SIGNED_SOURCE_OWNER_CANCELLATION",
            "source_path": str(FORMAL_417),
            "input_valid_for_claim": False,
            "notes": "future route allowed only with a real parent source-owner derivation",
        },
    ]


def lambda_bound_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "LCB4409_0_missing_live_Ruu_F_E_bound",
            "arena": "local_GR_Newton_PPN",
            "F_E_norm": "MISSING_RICCI_UU_OR_E_TRACE_NORM",
            "C_poincare": "MISSING_DOMAIN_CONSTANT",
            "C_elliptic_H2": "MISSING_ELLIPTIC_CONSTANT",
            "K_lambda_stress": "MISSING_STRESS_PROJECTION",
            "K_projection": "MISSING_ARENA_PROJECTION",
            "arena_threshold": "MISSING_ARENA_THRESHOLD",
            "boundary_condition": "MISSING_BOUNDARY_CONDITION",
            "zero_mode_fixed": False,
            "boundary_flux_silent": False,
            "source_path": "MISSING_SOURCE_PATH",
            "support_certificate_path": "MISSING_SUPPORT_CERTIFICATE",
            "input_valid_for_claim": False,
            "notes": "live bound still needs real R_uu/F_E norm, domain constants, support and arena threshold",
        },
        {
            "bound_id": "LCB4409_1_zero_Ruu_schema_nonclaim",
            "arena": "local_GR_Newton_PPN",
            "F_E_norm": "0",
            "C_poincare": "1",
            "C_elliptic_H2": "1",
            "K_lambda_stress": "1",
            "K_projection": "1",
            "arena_threshold": "1e-6",
            "boundary_condition": "Dirichlet",
            "zero_mode_fixed": True,
            "boundary_flux_silent": True,
            "source_path": str(LAMBDA_GATE_PATH),
            "support_certificate_path": str(LAMBDA_GATE_PATH),
            "input_valid_for_claim": False,
            "notes": "zero-source schema row; nonclaim because not parent-sourced",
        },
        {
            "bound_id": "LCB4409_2_small_elliptic_payload_smoke_nonclaim",
            "arena": "local_GR_Newton_PPN",
            "F_E_norm": "0.001",
            "C_poincare": "1",
            "C_elliptic_H2": "2",
            "K_lambda_stress": "1",
            "K_projection": "1",
            "arena_threshold": "0.01",
            "boundary_condition": "zero_mean_Neumann",
            "zero_mode_fixed": True,
            "boundary_flux_silent": True,
            "source_path": str(LAMBDA_GATE_PATH),
            "support_certificate_path": str(LAMBDA_GATE_PATH),
            "input_valid_for_claim": False,
            "notes": "nonclaim smoke row proving the elliptic payload formula computes cleanly",
        },
        {
            "bound_id": "LCB4409_3_large_payload_fail_control",
            "arena": "local_GR_Newton_PPN",
            "F_E_norm": "0.01",
            "C_poincare": "2",
            "C_elliptic_H2": "4",
            "K_lambda_stress": "2",
            "K_projection": "1",
            "arena_threshold": "0.005",
            "boundary_condition": "mixed_anchored",
            "zero_mode_fixed": True,
            "boundary_flux_silent": True,
            "source_path": str(LAMBDA_GATE_PATH),
            "support_certificate_path": str(LAMBDA_GATE_PATH),
            "input_valid_for_claim": False,
            "notes": "failure control: too-large curvature source fails threshold",
        },
    ]


def payload_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "payload_id": "FPV4409_0_missing_live_payload_vector",
            "target": "local_GR_Newton_PPN",
            "R_S_score": "MISSING_R_S",
            "J_U_score": "MISSING_J_U",
            "pressure_aniso_score": "MISSING_PRESSURE",
            "curvature_boundary_score": "MISSING_CURVATURE_BOUNDARY",
            "lambda_kernel_score": "MISSING_LAMBDA_KERNEL",
            "EM_overlap_score": "MISSING_EM_OVERLAP",
            "lambda_curvature_source_score": "MISSING_LAMBDA_CURVATURE",
            "delta_threshold": "MISSING_THRESHOLD",
            "source_path": "MISSING_SOURCE_PATH",
            "same_support_certificate": "MISSING_SUPPORT_CERTIFICATE",
            "no_cancellation_guard": False,
            "input_valid_for_claim": False,
            "notes": "live finite payload vector still needs real components",
        },
        {
            "payload_id": "FPV4409_1_lambda_bound_insert_smoke_nonclaim",
            "target": "runner_schema_from_elliptic_lambda_bound",
            "R_S_score": "0.001",
            "J_U_score": "0.001",
            "pressure_aniso_score": "0.001",
            "curvature_boundary_score": "0.001",
            "lambda_kernel_score": "0.001",
            "EM_overlap_score": "0.001",
            "lambda_curvature_source_score": "0.004",
            "delta_threshold": "0.02",
            "source_path": str(LAMBDA_BOUND_OUTPUT),
            "same_support_certificate": str(LAMBDA_BOUND_OUTPUT),
            "no_cancellation_guard": True,
            "input_valid_for_claim": False,
            "notes": "consumes a lambda payload score inside the finite vector; smoke only",
        },
        {
            "payload_id": "FPV4409_2_payload_vector_fail_control",
            "target": "runner_threshold_fail",
            "R_S_score": "0.01",
            "J_U_score": "0.01",
            "pressure_aniso_score": "0.01",
            "curvature_boundary_score": "0.01",
            "lambda_kernel_score": "0.01",
            "EM_overlap_score": "0.01",
            "lambda_curvature_source_score": "0.2",
            "delta_threshold": "0.05",
            "source_path": str(LAMBDA_BOUND_OUTPUT),
            "same_support_certificate": str(LAMBDA_BOUND_OUTPUT),
            "no_cancellation_guard": True,
            "input_valid_for_claim": False,
            "notes": "failure control for no-cancellation payload vector",
        },
    ]


def profile_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "PF4409_0_missing_real_density_profile_row",
            "arena": "Newton_source_profile",
            "branch": "first_real_profile_row_required_if_lambda_route_fails",
            "source_path": str(FORMAL_424),
            "K_N": "0.00943177578696",
            "delta_N": "MISSING_DELTA_N",
            "E_shadow": "MISSING_E_SHADOW",
            "E_top_profile": "MISSING_E_TOP_PROFILE",
            "E_nonHilbert_profile": "MISSING_E_NONHILBERT_PROFILE",
            "E_readout_profile": "MISSING_E_READOUT_PROFILE",
            "input_valid_for_claim": False,
        },
        {
            "bound_id": "PF4409_1_profile_zero_schema_smoke",
            "arena": "Newton_source_profile",
            "branch": "profile_zero_schema_smoke",
            "source_path": str(EPROFILE_GATE_PATH),
            "K_N": "0.00943177578696",
            "delta_N": "1e-5",
            "E_shadow": "0",
            "E_top_profile": "0",
            "E_nonHilbert_profile": "0",
            "E_readout_profile": "0",
            "input_valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "G4409_0_trace_electric_source",
            "gate": "lambda_source_is_Ricci_uu",
            "claim_allowed": False,
            "reason": "source narrowed to Ricci_uu, but parent R_uu=0 or real R_uu/F_E bound is not live.",
        },
        {
            "gate_id": "G4409_1_parent_cancellation",
            "gate": "nontrivial_parent_lambda_cancellation",
            "claim_allowed": False,
            "reason": "no same-parent nontrivial opposite-kernel cancellation certificate exists.",
        },
        {
            "gate_id": "G4409_2_elliptic_bound",
            "gate": "finite_lambda_curvature_payload",
            "claim_allowed": False,
            "reason": "elliptic runner is executable but real F_E/domain/support/threshold rows are missing.",
        },
        {
            "gate_id": "G4409_3_local_GR_Newton",
            "gate": "local_GR_Newton_PPN_R10",
            "claim_allowed": False,
            "reason": "local Ricci survivor vector and density-profile gates remain nonclaim.",
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4409_0",
            "decision": DECISION,
            "summary": "4409 rebases the 4401 lambda-curvature result onto the current 4408 sigma/electric owner route. The key improvement is that the curvature source is not generic Weyl curvature: for the trace-electric branch it is the Ricci-normal payload R_uu. Therefore the clean route is a parent local-vacuum/residual-silence theorem giving R_uu=0 on the same tau/coframe support; the finite route is an elliptic payload bound from ||F_E|| with domain constants. No claim fires because the parent Ricci-zero equation is unsigned and no real R_uu/F_E row is sourced. The next target is the local Ricci survivor vector: c_Gamma, c_R2/M_R, Lambda_eff, spin/torsion, and projector/boundary leakage, or the first real R_uu source row.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STAT4409_0",
            "item": "lambda source",
            "status": "REBASED_TO_RICCI_UU",
            "notes": "trace-electric source is R_uu, not generic Weyl/tidal curvature.",
        },
        {
            "status_id": "STAT4409_1",
            "item": "clean branch",
            "status": "PARENT_RICCI_ZERO_UNSIGNED",
            "notes": "R_uu=0 would restore homogeneous lambda branch but is not signed.",
        },
        {
            "status_id": "STAT4409_2",
            "item": "finite branch",
            "status": "ELLIPTIC_PAYLOAD_RUNNER_READY",
            "notes": "needs real F_E/R_uu norm, domain constants, support and threshold.",
        },
        {
            "status_id": "STAT4409_3",
            "item": "next target",
            "status": "RICCI_SURVIVOR_VECTOR_OR_REAL_RUU_ROW",
            "notes": NEXT_TARGET,
        },
    ]


def next_target_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4409_0",
            "target": NEXT_TARGET,
            "question": "Can the local Ricci survivor vector be parent-zeroed/bounded on the same tau/coframe support, or must the first real R_uu/F_E source row be imported?",
            "preferred_route": "derive local residual/Lambda/projector silence for c_Gamma, c_R2/M_R, Lambda_eff, spin/torsion, and boundary leakage so R_uu=0 or below threshold.",
            "fallback_route": "source or compute a real R_uu/F_E norm with domain constants and pass it through the lambda and finite-payload runners.",
            "avoid": "treating Weyl/tidal curvature as the live source, adding tuned counterterms, or claiming local vacuum from T_H=0 while E_res/Lambda_eff remain.",
            "valid_for_claim": False,
        }
    ]


def write_formal_doc(
    sources: List[Dict[str, object]],
    derivations: List[Dict[str, object]],
    ricci_output: List[Dict[str, object]],
    cancellation_output: List[Dict[str, object]],
    lambda_output: List[Dict[str, object]],
    payload_output: List[Dict[str, object]],
    profile_output: List[Dict[str, object]],
    gates: List[Dict[str, object]],
    decisions: List[Dict[str, object]],
    next_targets: List[Dict[str, object]],
) -> None:
    FORMAL_PATH.write_text(
        f"""# 425 PPC4161 transition lambda curvature payload cancellation or first real density-profile row

Marker: `{MARKER}`

Generated UTC: `{STAMP}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove public local GR, Newtonian mechanics, Maxwell/EM closure, calibrated `G_N`, R10, PPN, clock, orbital, WEP, or full local-vacuum safety.

## Current-Chain Result

4409 rebases the earlier lambda-curvature work onto the 4408 sigma/electric owner route.

For the trace-electric branch:

```text
S^{{ij}} = c^2 h^{{ij}} sigma_S,
partial(U.R)/partial sigma_S ~ K_E c^2 h^{{ij}} R_{{0i0j}},
h^{{ij}} R_{{0i0j}} = R_{{mu nu}} u^mu u^nu + projector/extrinsic terms.
```

So the live source is:

```text
Delta_h^dagger lambda_S = -K_E c^2 R_uu + B_projector + B_boundary.
```

This is progress: the source is Ricci-normal payload, not generic Weyl/tidal curvature.

The clean branch is:

```text
R_uu = 0
B_projector = 0
B_boundary = 0
zero mode fixed
=> homogeneous lambda_S branch.
```

The finite branch is:

```text
||lambda_S||_2 <= C_P^2 ||F_E||_2,
||D lambda_S||_2 <= C_P ||F_E||_2,
||lambda_S||_H2 <= C_E ||F_E||_2.
```

## Remaining Obstruction

Matter vacuum alone is not enough:

```text
R_uu = E_res_uu - 1/2 g_uu E_res + Lambda_eff g_uu
```

plus projector/boundary terms. Therefore the next object is the local Ricci survivor vector, not another generic coupling sweep.

## Source Register

{markdown_table(sources)}

## Derivation Rows

{markdown_table(derivations)}

## Ricci-Zero Gate Output

{markdown_table(ricci_output)}

## Parent-Cancellation Gate Output

{markdown_table(cancellation_output)}

## Lambda Curvature Bound Output

{markdown_table(lambda_output)}

## Finite Payload Vector Output

{markdown_table(payload_output)}

## Profile Fallback Output

{markdown_table(profile_output)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_targets)}
""",
        encoding="utf-8",
    )


def write_post_doc(decisions: List[Dict[str, object]], next_targets: List[Dict[str, object]]) -> None:
    DOC_PATH.write_text(
        f"""# 4409 lambda curvature payload cancellation or first real density-profile row

Marker: `{MARKER}`

## Private outcome

4409 narrows the lambda obstruction:

```text
lambda_S source = R_uu payload, not generic Weyl curvature.
```

The clean proof route is local `R_uu=0` on the same tau/coframe support. The finite route is a sourced `F_E/R_uu` elliptic bound. No claim fires because both live inputs are still missing.

## Decision

{markdown_table(decisions)}

## Next

{markdown_table(next_targets)}
""",
        encoding="utf-8",
    )


def update_spine() -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""## 4409 local spine update: lambda source is Ricci-normal

Marker: `{MARKER}`

Spine update: in the current sigma/electric U route, the `lambda_S` curvature source is now rebased as a Ricci-normal payload `R_uu`, not generic Weyl/tidal curvature. The clean branch is parent `R_uu=0` plus projector/boundary/zero-mode silence; the finite branch is an elliptic payload bound from real `F_E`/`R_uu` source rows. The next non-circling target is the local Ricci survivor vector: `c_Gamma`, `c_R2/M_R`, `Lambda_eff`, spin/torsion and projector/boundary leakage.
""",
    )


def update_packet() -> None:
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4409 packet update: lambda-curvature payload narrowed

Marker: `{PACKET_MARKER}`

Packet update: 4409 turns the lambda obstruction into a Ricci-normal source problem. Do not treat Weyl/tidal curvature as the current blocker; the route is now local `R_uu=0` or finite `F_E` payload, with residual/Lambda/projector terms retained until parent-zeroed or sourced.
""",
    )


def update_claims() -> None:
    append_claim_once(
        CLAIMS_PATH,
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4409 rebases the lambda_S curvature payload onto the current sigma/electric owner route. The trace-electric source is narrowed to the Ricci-normal payload R_uu rather than generic Weyl/tidal curvature. The clean branch would be parent R_uu=0 plus projector/boundary/zero-mode silence; the finite branch uses an elliptic payload bound from real F_E/R_uu norms and domain constants. No local-GR/Newton/PPN/R10/clock/orbital claim fires because the parent Ricci-zero equation and real R_uu/F_E source rows are missing.",
            "4409 source register, derivation rows, Ricci-zero gate, parent-cancellation gate, lambda curvature bound output, finite payload vector output, profile fallback output, claim gates, decision, status, next target and validation CSV.",
            "lambda_curvature_source_rebased_to_Ricci_uu_payload_runners_ready_nonclaim",
            "Zero/bound the local Ricci survivor vector or fill the first real R_uu/F_E source row.",
            "Treating Weyl/tidal curvature as the live source, adding tuned counterterms, or claiming local vacuum from T_H=0 while E_res/Lambda_eff remain.",
        ],
    )


def validation_rows(csv_paths: List[Path]) -> List[Dict[str, object]]:
    sources = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4409_SOURCE_REGISTER.csv")
    derivations = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4409_DERIVATIONS.csv")
    ricci_output = read_csv(RICCI_OUTPUT)
    cancellation_output = read_csv(CANCELLATION_OUTPUT)
    lambda_output = read_csv(LAMBDA_BOUND_OUTPUT)
    payload_output = read_csv(PAYLOAD_OUTPUT)
    profile_output = read_csv(PROFILE_OUTPUT)
    gates = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4409_CLAIM_GATES.csv")
    rows: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail})

    add("VAL4409_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source exists")
    add("VAL4409_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle resolves")
    add("VAL4409_2_derivations_written", len(derivations) >= 5, "derivation rows written")
    add("VAL4409_3_ricci_source_rebased", any(row["candidate_id"] == "RZ4409_0_trace_electric_source_rebased" and row["source_classified"] == "True" and row["ricci_zero_certificate_ready"] == "False" for row in ricci_output), "Ricci source is classified but not zero-certified")
    add("VAL4409_4_local_vacuum_template_blocks", any(row["candidate_id"] == "RZ4409_1_local_vacuum_parent_equation_template" and row["current_status"] == "RICCI_TRACE_SOURCE_IDENTIFIED_PARENT_VACUUM_EQUATION_UNSIGNED" for row in ricci_output), "local vacuum template blocks on parent equation")
    add("VAL4409_5_counterterm_trap_detected", any(row["candidate_id"] == "CAN4409_1_trivial_negative_U_counterterm_trap" and row["trivial_counterterm_trap"] == "True" for row in cancellation_output), "trivial counterterm trap detected")
    add("VAL4409_6_missing_lambda_bound_blocks", any(row["bound_id"] == "LCB4409_0_missing_live_Ruu_F_E_bound" and row["current_status"] == "LAMBDA_CURVATURE_PAYLOAD_BOUND_BLOCKED" for row in lambda_output), "missing live lambda bound blocks")
    add("VAL4409_7_zero_lambda_bound_nonclaim", any(row["bound_id"] == "LCB4409_1_zero_Ruu_schema_nonclaim" and row["payload_within_threshold"] == "True" and row["claim_allowed"] == "False" for row in lambda_output), "zero lambda bound schema remains nonclaim")
    add("VAL4409_8_lambda_fail_detected", any(row["bound_id"] == "LCB4409_3_large_payload_fail_control" and row["current_status"] == "LAMBDA_CURVATURE_PAYLOAD_BOUND_FAILS_THRESHOLD" for row in lambda_output), "lambda payload fail control detected")
    add("VAL4409_9_payload_vector_consumes_lambda", any(row["payload_id"] == "FPV4409_1_lambda_bound_insert_smoke_nonclaim" and row["schema_ready"] == "True" and row["payload_within_threshold"] == "True" for row in payload_output), "finite payload vector consumes lambda score")
    add("VAL4409_10_payload_vector_fail_detected", any(row["payload_id"] == "FPV4409_2_payload_vector_fail_control" and row["current_status"] == "FINITE_PAYLOAD_VECTOR_FAILS_THRESHOLD" for row in payload_output), "finite payload vector fail detected")
    add("VAL4409_11_profile_fallback_blocks", any(row["bound_id"] == "PF4409_0_missing_real_density_profile_row" and row["current_status"] == "EPROFILE_BOUND_BLOCKED" for row in profile_output), "profile fallback missing row blocks")
    add("VAL4409_12_claim_gates_false", all(row["claim_allowed"] == "False" for row in gates), "claim gates false")
    add("VAL4409_13_formal_marker", MARKER in text(FORMAL_PATH), "formal marker present")
    add("VAL4409_14_post_marker", MARKER in text(DOC_PATH), "post marker present")
    add("VAL4409_15_spine_marker", MARKER in text(SPINE_PATH), "spine marker present")
    add("VAL4409_16_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker present")
    add("VAL4409_17_claim_row", f"\n{CLAIM_ID}," in text(CLAIMS_PATH), "claim row present")
    add("VAL4409_18_csv_parse", all(len(read_csv(path)) > 0 for path in csv_paths), "all generated CSVs parse")
    add("VAL4409_19_generated_nonclaim", all(row.get("valid_for_claim", "False") == "False" for path in csv_paths for row in read_csv(path)), "generated rows stay nonclaim")
    add("VAL4409_20_gate_scripts_exist", LAMBDA_GATE_PATH.exists() and PAYLOAD_RUNNER_PATH.exists() and EPROFILE_GATE_PATH.exists(), "gate scripts exist")
    add("VAL4409_21_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent")
    return rows


def remove_pycache() -> None:
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_rows()
    derivations = derivation_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()
    csv_paths: List[Path] = []
    csv_payloads: Dict[str, List[Dict[str, object]]] = {
        "P8_Y5_R2FR_4409_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R2FR_4409_DERIVATIONS.csv": derivations,
        "P8_Y5_R2FR_4409_CLAIM_GATES.csv": gates,
        "P8_Y5_R2FR_4409_DECISION.csv": decisions,
        "P8_Y5_R2FR_4409_STATUS.csv": statuses,
        "P8_Y5_R2FR_4409_NEXT_TARGET.csv": next_targets,
    }
    for filename, rows in csv_payloads.items():
        path = SOURCE_DIR / filename
        write_csv(path, rows)
        csv_paths.append(path)

    write_csv(RICCI_INPUT, ricci_input_rows())
    ricci_output = evaluate_ricci_zero_rows(RICCI_INPUT)
    write_csv(RICCI_OUTPUT, ricci_output)
    csv_paths.extend([RICCI_INPUT, RICCI_OUTPUT])

    write_csv(CANCELLATION_INPUT, cancellation_input_rows())
    cancellation_output = evaluate_cancellation_rows(CANCELLATION_INPUT)
    write_csv(CANCELLATION_OUTPUT, cancellation_output)
    csv_paths.extend([CANCELLATION_INPUT, CANCELLATION_OUTPUT])

    write_csv(LAMBDA_BOUND_INPUT, lambda_bound_input_rows())
    lambda_output = evaluate_bound_rows(LAMBDA_BOUND_INPUT)
    write_csv(LAMBDA_BOUND_OUTPUT, lambda_output)
    csv_paths.extend([LAMBDA_BOUND_INPUT, LAMBDA_BOUND_OUTPUT])

    write_csv(PAYLOAD_INPUT, payload_input_rows())
    payload_output = evaluate_payload_rows(PAYLOAD_INPUT)
    write_csv(PAYLOAD_OUTPUT, payload_output)
    csv_paths.extend([PAYLOAD_INPUT, PAYLOAD_OUTPUT])

    write_csv(PROFILE_INPUT, profile_input_rows())
    profile_output = evaluate_eprofile_bound_rows(PROFILE_INPUT)
    write_csv(PROFILE_OUTPUT, profile_output)
    csv_paths.extend([PROFILE_INPUT, PROFILE_OUTPUT])

    write_formal_doc(
        sources,
        derivations,
        ricci_output,
        cancellation_output,
        lambda_output,
        payload_output,
        profile_output,
        gates,
        decisions,
        next_targets,
    )
    write_post_doc(decisions, next_targets)
    update_spine()
    update_packet()
    update_claims()
    remove_pycache()
    write_csv(VALIDATION_PATH, validation_rows(csv_paths))


if __name__ == "__main__":
    main()

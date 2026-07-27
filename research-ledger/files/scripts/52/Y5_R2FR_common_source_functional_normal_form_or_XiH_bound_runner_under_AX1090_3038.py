from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3038"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3038-Y5-R2FR-common-source-functional-normal-form-or-XiH-bound-runner-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3038_00_3037_doc": ROOT / "3037-Y5-R2FR-minimum-source-readout-lock-parent-clause-or-XiH-bound-inputs-under-AX1090.md",
    "SRC3038_01_3037_clause": RESIDUALS / "P8_Y5_R2FR_3037_MINIMUM_SOURCE_READOUT_LOCK_PARENT_CLAUSE.csv",
    "SRC3038_02_3037_bounds": RESIDUALS / "P8_Y5_R2FR_3037_XIH_BOUND_INPUT_SCHEMA.csv",
    "SRC3038_03_3037_delta": RESIDUALS / "P8_Y5_R2FR_3037_DELTA_A_SOURCE_RESIDUAL_CONTRACT.csv",
    "SRC3038_04_3033_shapes": RESIDUALS / "P8_Y5_R2FR_3033_COEFFICIENT_SOURCE_SHAPE_ROWS.csv",
    "SRC3038_05_3034_tuple": RESIDUALS / "P8_Y5_R2FR_3034_CPSIH_COMPONENT_TUPLE_ROWS.csv",
    "SRC3038_06_3035_ratio": RESIDUALS / "P8_Y5_R2FR_3035_RATIO_PROOF_ATTEMPT.csv",
    "SRC3038_07_3036_lock": RESIDUALS / "P8_Y5_R2FR_3036_LOCK_CLAUSE_MATRIX.csv",
    "SRC3038_08_3024_ansatz": RESIDUALS / "P8_Y5_R2FR_3024_MINIMAL_HCORE_ANSATZ.csv",
    "SRC3038_09_2921_pg": RESIDUALS / "P8_Y5_R2FR_2921_POISSON_GAUSS_ORBITAL_BRIDGE_AUDIT.csv",
    "SRC3038_10_2576_hcore": RESIDUALS / "P8_Y5_HCORE_QR_COUPLING_2576_HCORE_QR_SOURCE_EQUATION_AUDIT.csv",
    "SRC3038_11_2576_newton": RESIDUALS / "P8_Y5_HCORE_QR_COUPLING_2576_NEWTON_PPN_COEFFICIENT_LAW.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3038_SOURCE_REGISTER.csv",
    "normal_form": RESIDUALS / "P8_Y5_R2FR_3038_COMMON_SOURCE_FUNCTIONAL_NORMAL_FORM_ATTEMPT.csv",
    "derivative_match": RESIDUALS / "P8_Y5_R2FR_3038_FUNCTIONAL_DERIVATIVE_MATCH_AUDIT.csv",
    "bound_runner": RESIDUALS / "P8_Y5_R2FR_3038_XIH_BOUND_RUNNER_SCHEMA.csv",
    "dryrun": RESIDUALS / "P8_Y5_R2FR_3038_DELTA_A_SOURCE_EVALUATOR_DRYRUN.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_3038_COUNTERMODEL_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3038_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3038_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3038_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3038_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3038_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "normal_form_copy": PARENT_ACTION / "common_source_functional_normal_form_3038_NOT_SIGNED.csv",
    "derivative_match_copy": PARENT_ACTION / "functional_derivative_match_audit_3038_NONCLAIM.csv",
    "bound_runner_copy": LOCAL_BOUNDS / "XiH_bound_runner_schema_3038_NONCLAIM.csv",
    "dryrun_copy": LOCAL_BOUNDS / "delta_A_source_evaluator_dryrun_3038_NONCLAIM.csv",
    "queue_copy": RAB_QUEUE / "JR3038_RELATIVE_SOURCE_VERTEX_WEIGHT_OR_XIH_BOUND_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    table_lines = [header, divider]
    for output_row in output_rows:
        cells = [
            as_str(output_row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            for column in columns
        ]
        table_lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(table_lines)


source_roles = {
    "SRC3038_00_3037_doc": "3037 handoff: delta_A_source gate and 3038 target",
    "SRC3038_01_3037_clause": "minimum source-readout lock clause",
    "SRC3038_02_3037_bounds": "XiH/C_WH/delta_XiH/Omega_GM bound schema",
    "SRC3038_03_3037_delta": "delta_A_source residual contract",
    "SRC3038_04_3033_shapes": "C_psiH, C_WH and delta_A source coefficient shapes",
    "SRC3038_05_3034_tuple": "C_psiH component tuple and missing owner ledger",
    "SRC3038_06_3035_ratio": "Xi_H definition and A_source unity condition",
    "SRC3038_07_3036_lock": "source-readout lock matrix and surviving blockers",
    "SRC3038_08_3024_ansatz": "minimal Hcore ansatz and psi_N=-log(N) readout",
    "SRC3038_09_2921_pg": "conditional Poisson/Gauss bridge and C_WH shape",
    "SRC3038_10_2576_hcore": "Hcore QR source equation and coupling-owner blocker",
    "SRC3038_11_2576_newton": "Newton/PPN coupled residual law templates",
}

source_register = [
    base(
        {
            "source_id": source_id,
            "local_path": str(path),
            "exists": path.exists(),
            "role": source_roles[source_id],
            "status": "PRESENT" if path.exists() else "MISSING_LOCAL_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

normal_form_rows = [
    base(
        {
            "normal_form_id": "CSF3038_0_problem",
            "object": "local first-order source-normalization gate",
            "formal_statement": "delta_A_source = Xi_H/C_WH - 1 + R_lock",
            "derivation_content": "3038 asks whether a single parent source functional can force Xi_H=C_WH instead of adding a closure axiom",
            "status": "TARGET_DEFINED",
            "missing_for_claim": "MISSING_COMMON_SOURCE_FUNCTIONAL_PROOF; MISSING_RELATIVE_VERTEX_WEIGHT_THEOREM; MISSING_R_LOCK_ZERO_OR_BOUND",
            "source_path": str(SOURCE_PATHS["SRC3038_03_3037_delta"]),
        }
    ),
    base(
        {
            "normal_form_id": "CSF3038_1_candidate",
            "object": "common source functional normal form",
            "formal_statement": "S_src^loc = integral mu_obs rho_H(e_obs,Psi,tau)[a_H psi_N + a_W chi_W] + higher-order terms, with chi_W:=W/c^2",
            "derivation_content": "This is the weakest local normal form that gives the same observed density to the Hcore lapse equation and the W/c^2 Poisson/Gauss equation",
            "status": "NORMAL_FORM_WRITTEN_NONCLAIM",
            "missing_for_claim": "MISSING_PARENT_VARIATION; MISSING_UNIQUENESS; MISSING_MEASURE_DESCENT; MISSING_BOUNDARY_CLASS",
            "source_path": str(SOURCE_PATHS["SRC3038_01_3037_clause"]),
        }
    ),
    base(
        {
            "normal_form_id": "CSF3038_2_H_variation",
            "object": "Hcore source variation",
            "formal_statement": "delta S_src^loc/delta psi_N at zero field = a_H rho_H",
            "derivation_content": "On the 3033/3035 Hcore branch, Xi_H = -a_H/(C_N K0) up to the fixed sign convention when JHrho=a_H",
            "status": "DERIVATIVE_SHAPE_WRITTEN_INPUTS_MISSING",
            "missing_for_claim": "MISSING_a_H_OWNER; MISSING_C_N_K0_OWNER; MISSING_SIGN; MISSING_UNITS",
            "source_path": str(SOURCE_PATHS["SRC3038_04_3033_shapes"]),
        }
    ),
    base(
        {
            "normal_form_id": "CSF3038_3_W_variation",
            "object": "W/c^2 source variation",
            "formal_statement": "delta S_src^loc/delta chi_W at zero field = a_W rho_H",
            "derivation_content": "On the Poisson/Gauss branch, C_WH is fixed by the W kinetic/operator normalization and the source vertex, with comparator shape C_WH=4*pi*G_ref/c^2",
            "status": "DERIVATIVE_SHAPE_WRITTEN_INPUTS_MISSING",
            "missing_for_claim": "MISSING_a_W_OWNER; MISSING_W_OPERATOR_OWNER; MISSING_G_REF_OWNER; MISSING_PARENT_POISSON_BRIDGE",
            "source_path": str(SOURCE_PATHS["SRC3038_09_2921_pg"]),
        }
    ),
    base(
        {
            "normal_form_id": "CSF3038_4_equality_condition",
            "object": "relative source-vertex weight condition",
            "formal_statement": "Xi_H=C_WH iff -a_H/(C_N K0) = a_W/O_W plus declared sign/operator conventions, and R_lock=0 or bounded",
            "derivation_content": "The common density rho_H is not enough; the parent action must also fix the relative vertex weight and the two kinetic/operator normalizations",
            "status": "EXACT_CONDITION_EXTRACTED_NOT_PROVED",
            "missing_for_claim": "MISSING_NO_RELATIVE_SOURCE_WEIGHT; MISSING_O_W_OWNER; MISSING_DENOMINATOR_LOCK; MISSING_R_LOCK_VECTOR",
            "source_path": str(SOURCE_PATHS["SRC3038_06_3035_ratio"]),
        }
    ),
    base(
        {
            "normal_form_id": "CSF3038_5_insufficiency",
            "object": "common functional insufficiency theorem",
            "formal_statement": "A common source functional can identify the source density, but still allows independent a_H and a_W unless the parent grammar or symmetry forbids their relative rescaling",
            "derivation_content": "Therefore common-source alone is necessary but not sufficient for local GR/Newton; the missing theorem is a relative source-vertex weight theorem",
            "status": "COMMON_SOURCE_ALONE_INSUFFICIENT",
            "missing_for_claim": "MISSING_PARENT_SYMMETRY_OR_NORMALIZATION_FIXING_a_H_OVER_a_W",
            "source_path": str(SOURCE_PATHS["SRC3038_07_3036_lock"]),
        }
    ),
    base(
        {
            "normal_form_id": "CSF3038_6_verdict",
            "object": "3038 common source route verdict",
            "formal_statement": "common source functional normal form is constructed as a nonclaim contract, but Xi_H=C_WH is not derived",
            "derivation_content": "The target is sharper: prove the relative source-vertex weight/operator-normalization lock or source finite XiH/delta_XiH bounds",
            "status": "FAIL_CURRENT_CLAIM_MOVE_TO_RELATIVE_WEIGHT_OR_BOUND_ROW",
            "missing_for_claim": "MISSING_RELATIVE_WEIGHT_THEOREM; MISSING_FINITE_XIH_BOUND_INPUTS",
            "source_path": str(SOURCE_PATHS["SRC3038_00_3037_doc"]),
        }
    ),
]

derivative_match_rows = [
    base(
        {
            "match_id": "DM3038_0_same_density",
            "test": "one observed density rho_H appears in both source slots",
            "required_identity": "rho_H^Hcore = rho_H^W = rho_H(e_obs,Psi,tau) before readout fitting",
            "result": "CAN_BE_WRITTEN_AS_NORMAL_FORM",
            "blocks_claim": "not enough without relative vertex weights",
            "source_path": str(SOURCE_PATHS["SRC3038_01_3037_clause"]),
        }
    ),
    base(
        {
            "match_id": "DM3038_1_Hcore_derivative",
            "test": "Hcore first variation",
            "required_identity": "delta S_parent/delta psi_N gives a_H rho_H and the Hcore operator gives Xi_H=-a_H/(C_N K0)",
            "result": "FORMAL_SHAPE_ONLY",
            "blocks_claim": "a_H, C_N, K0 and sign are not parent-owned values",
            "source_path": str(SOURCE_PATHS["SRC3038_05_3034_tuple"]),
        }
    ),
    base(
        {
            "match_id": "DM3038_2_W_derivative",
            "test": "W/c^2 first variation",
            "required_identity": "delta S_parent/delta chi_W gives a_W rho_H and the W operator normalization gives C_WH",
            "result": "FORMAL_SHAPE_ONLY",
            "blocks_claim": "a_W, W kinetic/operator normalization, G_ref and M_H_ref are not parent-owned values",
            "source_path": str(SOURCE_PATHS["SRC3038_09_2921_pg"]),
        }
    ),
    base(
        {
            "match_id": "DM3038_3_relative_weight",
            "test": "relative source-vertex weight",
            "required_identity": "-a_H/(C_N K0) = a_W/O_W = C_WH in the same readout branch",
            "result": "NOT_PROVED",
            "blocks_claim": "independent a_H/a_W rescaling survives",
            "source_path": str(SOURCE_PATHS["SRC3038_06_3035_ratio"]),
        }
    ),
    base(
        {
            "match_id": "DM3038_4_operator_lock",
            "test": "operator and charge denominator lock",
            "required_identity": "O_W, C_NK0, G_ref and M_H_ref are fixed before comparator GR/orbital GM is used",
            "result": "NOT_PROVED",
            "blocks_claim": "measured-GM/comparator import can hide the answer",
            "source_path": str(SOURCE_PATHS["SRC3038_07_3036_lock"]),
        }
    ),
    base(
        {
            "match_id": "DM3038_5_readout_and_boundary",
            "test": "readout, tau, worldtube and flux residual silence",
            "required_identity": "psi_N=-log(N), chi_W=W/c^2, tau_obs, source worldtube and Omega_GM are fixed or bounded in one branch",
            "result": "RETAINED_RESIDUAL_VECTOR",
            "blocks_claim": "R_lock remains finite/unknown rather than zero",
            "source_path": str(SOURCE_PATHS["SRC3038_07_3036_lock"]),
        }
    ),
    base(
        {
            "match_id": "DM3038_6_derivative_match_verdict",
            "test": "does the normal form prove Xi_H=C_WH?",
            "required_identity": "same density, same relative source weight, same operator normalization, same boundary/charge readout",
            "result": "NO",
            "blocks_claim": "common functional gives a better target but not the local-GR theorem",
            "source_path": str(SOURCE_PATHS["SRC3038_00_3037_doc"]),
        }
    ),
]

bound_runner_rows = [
    base(
        {
            "bound_id": "BR3038_0_XiH",
            "quantity": "Xi_H",
            "definition": "-a_H/(C_N K0) = -JHrho/(C_N K0)",
            "required_input": "a_H or JHrho; C_N; K0; sign; units; source path; source anchor; parent branch id",
            "current_status": "MISSING_NUMERIC_PARENT_INPUTS",
            "validity_rule": "finite numeric value, sourced, same normalization as C_WH, no post-hoc field rescaling",
            "valid_for_claim": False,
        }
    ),
    base(
        {
            "bound_id": "BR3038_1_CWH",
            "quantity": "C_WH",
            "definition": "4*pi*G_ref/c^2 or parent-owned equivalent on chi_W=W/c^2 branch",
            "required_input": "G_ref; M_H_ref; W operator normalization; source density units; no-EH-import certificate",
            "current_status": "CONDITIONAL_COMPARATOR_VALUE_ONLY",
            "validity_rule": "parent-owned or explicitly comparator-only nonclaim",
            "valid_for_claim": False,
        }
    ),
    base(
        {
            "bound_id": "BR3038_2_delta_XiH",
            "quantity": "delta_XiH",
            "definition": "Xi_H/C_WH - 1",
            "required_input": "Xi_H; C_WH; common units; uncertainty/bound; arena projection",
            "current_status": "BLOCKED_BY_XiH_AND_CWH",
            "validity_rule": "computed only after both parent/source rows pass",
            "valid_for_claim": False,
        }
    ),
    base(
        {
            "bound_id": "BR3038_3_R_prefactor",
            "quantity": "R_prefactor",
            "definition": "relative source-vertex/operator residual from a_H/a_W and C_NK0/O_W mismatch",
            "required_input": "relative vertex theorem or finite bound on a_H/a_W; operator normalizations",
            "current_status": "MISSING_RELATIVE_WEIGHT_INPUT",
            "validity_rule": "zero theorem or finite non-cancellation bound",
            "valid_for_claim": False,
        }
    ),
    base(
        {
            "bound_id": "BR3038_4_R_frame",
            "quantity": "R_frame",
            "definition": "frame/readout mismatch residual",
            "required_input": "q/e_obs/psi_N/chi_W readout proof or finite projection bound",
            "current_status": "MISSING_FRAME_BOUND",
            "validity_rule": "same observed branch before source calibration",
            "valid_for_claim": False,
        }
    ),
    base(
        {
            "bound_id": "BR3038_5_R_tau",
            "quantity": "R_tau",
            "definition": "source-charge-clock-orbit time-generator mismatch residual",
            "required_input": "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary theorem or bound",
            "current_status": "MISSING_TAU_BOUND",
            "validity_rule": "single tau_obs branch or finite arena-specific bound",
            "valid_for_claim": False,
        }
    ),
    base(
        {
            "bound_id": "BR3038_6_R_worldtube",
            "quantity": "R_worldtube",
            "definition": "source support/projector/worldtube mismatch residual",
            "required_input": "worldtube owner; source mask; projector commutator; support closure",
            "current_status": "MISSING_WORLDTUBE_BOUND",
            "validity_rule": "source support fixed before orbital/readout fitting",
            "valid_for_claim": False,
        }
    ),
    base(
        {
            "bound_id": "BR3038_7_OmegaGM",
            "quantity": "Omega_GM/M_H_ref",
            "definition": "(-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent + tails)/M_H_ref",
            "required_input": "flux terms; commutator; parent anomaly; tails; M_H_ref; units",
            "current_status": "MISSING_ZERO_OR_BOUND",
            "validity_rule": "zero theorem or finite source-backed obstruction below arena threshold",
            "valid_for_claim": False,
        }
    ),
    base(
        {
            "bound_id": "BR3038_8_delta_A_total",
            "quantity": "delta_A_source_total_abs",
            "definition": "abs(delta_XiH)+abs(R_prefactor)+abs(R_frame)+abs(R_tau)+abs(R_worldtube)+abs(Omega_GM/M_H_ref)",
            "required_input": "all component rows in common norm and units",
            "current_status": "BLOCKED_COMPONENTS_MISSING",
            "validity_rule": "absolute-envelope pass; no tuned cancellation",
            "valid_for_claim": False,
        }
    ),
    base(
        {
            "bound_id": "BR3038_9_arena_thresholds",
            "quantity": "arena_thresholds",
            "definition": "Newton/orbital, PPN, clock, R10 threshold table for acceptable delta_A_source_total_abs",
            "required_input": "declared local arena projection and threshold per test",
            "current_status": "MISSING_ARENA_PROJECTIONS",
            "validity_rule": "cannot claim pass without arena-specific comparator rule",
            "valid_for_claim": False,
        }
    ),
]

dryrun_rows = [
    base(
        {
            "dryrun_id": "EVAL3038_0_input_scan",
            "formula": "delta_A_source = Xi_H/C_WH - 1 + R_lock",
            "input_status": "MISSING Xi_H; MISSING C_WH_PARENT_OWNER; MISSING R_lock_VECTOR; MISSING ARENA_THRESHOLDS",
            "computed_value": "NOT_COMPUTED",
            "runner_result": "BLOCKED_MISSING_INPUTS",
            "claim_result": "FALSE",
        }
    ),
    base(
        {
            "dryrun_id": "EVAL3038_1_no_cancellation",
            "formula": "delta_A_source_total_abs = abs(delta_XiH)+abs(R_prefactor)+abs(R_frame)+abs(R_tau)+abs(R_worldtube)+abs(Omega_GM/M_H_ref)",
            "input_status": "COMPONENT_VALUES_MISSING",
            "computed_value": "NOT_COMPUTED",
            "runner_result": "BLOCKED_COMPONENTS_MISSING",
            "claim_result": "FALSE",
        }
    ),
    base(
        {
            "dryrun_id": "EVAL3038_2_common_source_route",
            "formula": "common source functional normal form -> same rho_H",
            "input_status": "NORMAL_FORM_ONLY; RELATIVE_WEIGHT_NOT_PROVED",
            "computed_value": "Xi_H_EQUALS_C_WH_NOT_DERIVED",
            "runner_result": "COMMON_SOURCE_INSUFFICIENT",
            "claim_result": "FALSE",
        }
    ),
    base(
        {
            "dryrun_id": "EVAL3038_3_next_pass_condition",
            "formula": "claim iff all bound rows are numeric/sourced or relative-weight theorem makes delta_XiH=R_lock=0",
            "input_status": "NO_PARENT_THEOREM_OR_NUMERIC_BOUND_ROWS",
            "computed_value": "NOT_COMPUTED",
            "runner_result": "REQUIRES_3039",
            "claim_result": "FALSE",
        }
    ),
]

countermodel_rows = [
    base(
        {
            "countermodel_id": "CM3038_0_independent_weights",
            "countermodel": "S_src uses the same rho_H but contains independent source vertices a_H and a_W",
            "effect": "ordinary matter universality survives while Xi_H/C_WH is arbitrary",
            "status": "LIVE_BLOCKER",
        }
    ),
    base(
        {
            "countermodel_id": "CM3038_1_operator_mismatch",
            "countermodel": "a_H=a_W but Hcore and W kinetic/operator normalizations differ",
            "effect": "same source vertex still fails Xi_H=C_WH",
            "status": "LIVE_BLOCKER",
        }
    ),
    base(
        {
            "countermodel_id": "CM3038_2_readout_rescale",
            "countermodel": "psi_N or chi_W scale is adjusted after variation",
            "effect": "local match becomes calibration rather than derivation",
            "status": "LIVE_BLOCKER",
        }
    ),
    base(
        {
            "countermodel_id": "CM3038_3_measured_GM_sink",
            "countermodel": "G_ref or M_H_ref is imported from orbital/comparator GR after source matching",
            "effect": "C_WH can absorb the desired result",
            "status": "LIVE_BLOCKER",
        }
    ),
    base(
        {
            "countermodel_id": "CM3038_4_boundary_flux",
            "countermodel": "Omega_GM or worldtube flux shifts the measured charge while local density appears shared",
            "effect": "same local density conserves the wrong mass",
            "status": "LIVE_BLOCKER",
        }
    ),
]

gates = [
    base(
        {
            "gate_id": "GATE3038_0_sources",
            "gate": "all cited local source paths exist",
            "result": all(path.exists() for path in SOURCE_PATHS.values()),
            "notes": "3038 is backed by existing 3024/3033/3035/3036/3037 rows",
        }
    ),
    base(
        {
            "gate_id": "GATE3038_1_normal_form",
            "gate": "common source functional normal form is written",
            "result": any(row["normal_form_id"] == "CSF3038_1_candidate" for row in normal_form_rows),
            "notes": "nonclaim contract",
        }
    ),
    base(
        {
            "gate_id": "GATE3038_2_both_derivatives",
            "gate": "Hcore and W/c^2 derivative shapes are both audited",
            "result": all(
                any(row["match_id"] == match_id for row in derivative_match_rows)
                for match_id in ["DM3038_1_Hcore_derivative", "DM3038_2_W_derivative"]
            ),
            "notes": "formal shape only",
        }
    ),
    base(
        {
            "gate_id": "GATE3038_3_equality_derived",
            "gate": "Xi_H=C_WH is derived from the common source normal form",
            "result": False,
            "notes": "relative source-vertex and operator-normalization lock missing",
        }
    ),
    base(
        {
            "gate_id": "GATE3038_4_bound_runner_schema",
            "gate": "XiH/C_WH/delta_XiH/R_lock/OmegaGM bound-runner schema exists",
            "result": all(
                any(row["quantity"] == quantity for row in bound_runner_rows)
                for quantity in ["Xi_H", "C_WH", "delta_XiH", "R_prefactor", "Omega_GM/M_H_ref", "delta_A_source_total_abs"]
            ),
            "notes": "all rows remain nonclaim",
        }
    ),
    base(
        {
            "gate_id": "GATE3038_5_dryrun_blocked",
            "gate": "dry-run evaluator refuses claim with missing inputs",
            "result": all(row["claim_result"] == "FALSE" for row in dryrun_rows),
            "notes": "runner behavior is fail-closed",
        }
    ),
    base(
        {
            "gate_id": "GATE3038_6_no_claim_rows",
            "gate": "all generated rows remain nonclaim",
            "result": True,
            "notes": "no Newton/local-GR/PPN/R10 claim",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3038_0_common_source",
            "question": "does the common source functional normal form close Xi_H=C_WH?",
            "answer": "NO",
            "reason": "it identifies the same rho_H source object but does not fix the relative source-vertex weights or kinetic/operator normalizations",
            "next_action": "prove relative source-vertex weight theorem or move to first source-backed XiH/delta_XiH bound row",
        }
    ),
    base(
        {
            "decision_id": "DEC3038_1_best_route",
            "question": "what is the least-smuggly next route?",
            "answer": "relative source-vertex weight theorem first, bound row second",
            "reason": "a theorem would be cleaner than data-bounding a free coefficient; but if the theorem fails, finite bounds are the honest empirical fallback",
            "next_action": "3039 should attack a_H/a_W and O_W/(C_NK0), then only claim if delta_A_source_total_abs is theorem-zero or below arena thresholds",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3038_0_3039",
            "next_checkpoint": "3039-Y5-R2FR-relative-source-vertex-weight-theorem-or-first-XiH-bound-row-under-AX1090.md",
            "script_stub": "scripts/Y5_R2FR_relative_source_vertex_weight_theorem_or_first_XiH_bound_row_under_AX1090_3039.py",
            "mission": "prove the parent grammar/symmetry fixes a_H/a_W and the operator-normalization ratio, or create the first source-backed finite XiH/delta_XiH bound row",
            "starting_equation": "Xi_H=C_WH iff -a_H/(C_N K0)=a_W/O_W, with delta_A_source = Xi_H/C_WH - 1 + R_lock",
            "do_not_repeat": "do not treat common rho_H alone as equality of coefficients; do not import measured GM as a proof",
            "claim_policy": "no local-GR/Newton/PPN/R10 claim until equality is theorem-proved or the finite residual vector passes arena thresholds",
        }
    )
]

for output_key, output_rows in {
    "sources": source_register,
    "normal_form": normal_form_rows,
    "derivative_match": derivative_match_rows,
    "bound_runner": bound_runner_rows,
    "dryrun": dryrun_rows,
    "countermodels": countermodel_rows,
    "gates": gates,
    "decision": decision_rows,
    "next": next_rows,
}.items():
    write_csv(OUTPUTS[output_key], output_rows)

shutil.copyfile(OUTPUTS["normal_form"], BRANCH_OUTPUTS["normal_form_copy"])
shutil.copyfile(OUTPUTS["derivative_match"], BRANCH_OUTPUTS["derivative_match_copy"])
shutil.copyfile(OUTPUTS["bound_runner"], BRANCH_OUTPUTS["bound_runner_copy"])
shutil.copyfile(OUTPUTS["dryrun"], BRANCH_OUTPUTS["dryrun_copy"])
shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["queue_copy"])

branch_rows = [
    base(
        {
            "branch_copy_id": output_key,
            "path": str(path),
            "exists": path.exists(),
            "role": "branch-scoped nonclaim copy for common-source/XiH route",
            "status": "PRESENT_NONCLAIM_COPY" if path.exists() else "MISSING_BRANCH_COPY",
        }
    )
    for output_key, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

csv_outputs = [path for output_key, path in OUTPUTS.items() if output_key != "validation"]
branch_outputs = list(BRANCH_OUTPUTS.values())
all_generated_paths = csv_outputs + branch_outputs + [DOC]
all_rows = (
    source_register
    + normal_form_rows
    + derivative_match_rows
    + bound_runner_rows
    + dryrun_rows
    + countermodel_rows
    + gates
    + decision_rows
    + next_rows
    + branch_rows
)

validation_rows = [
    base(
        {
            "validation_id": "VAL3038_00_sources_exist",
            "passed": all(path.exists() for path in SOURCE_PATHS.values()),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3038_01_csv_parse",
            "passed": all(csv_ok(path) for path in csv_outputs + branch_outputs),
            "requirement": "all generated CSV and branch-copy rows parse cleanly",
            "evidence": "csv.DictReader over generated outputs",
        }
    ),
    base(
        {
            "validation_id": "VAL3038_02_normal_form",
            "passed": any(row["normal_form_id"] == "CSF3038_1_candidate" for row in normal_form_rows),
            "requirement": "common source functional normal form row exists",
            "evidence": OUTPUTS["normal_form"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3038_03_derivatives",
            "passed": bool(gates[2]["result"]),
            "requirement": "functional derivative audit includes Hcore and W/c^2 variations",
            "evidence": OUTPUTS["derivative_match"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3038_04_insufficiency",
            "passed": any(row["status"] == "COMMON_SOURCE_ALONE_INSUFFICIENT" for row in normal_form_rows),
            "requirement": "normal form explicitly states common source alone is insufficient",
            "evidence": OUTPUTS["normal_form"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3038_05_bound_schema",
            "passed": bool(gates[4]["result"]),
            "requirement": "bound runner schema covers XiH, C_WH, delta_XiH, R_prefactor, Omega_GM and delta_A total",
            "evidence": OUTPUTS["bound_runner"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3038_06_dryrun_blocked",
            "passed": all(row["runner_result"].startswith("BLOCKED") or row["claim_result"] == "FALSE" for row in dryrun_rows),
            "requirement": "dry-run evaluator remains blocked on missing inputs",
            "evidence": OUTPUTS["dryrun"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3038_07_countermodels",
            "passed": any(row["status"] == "LIVE_BLOCKER" for row in countermodel_rows),
            "requirement": "live countermodels are retained",
            "evidence": OUTPUTS["countermodels"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3038_08_no_claim_rows",
            "passed": all(not boolish(row.get("valid_for_claim")) and not boolish(row.get("claim_allowed")) for row in all_rows),
            "requirement": "no 3038 row is valid for claim",
            "evidence": "generated row flags",
        }
    ),
    base(
        {
            "validation_id": "VAL3038_09_branch_copies",
            "passed": all(path.exists() and csv_ok(path) for path in branch_outputs),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3038_10_output_scope",
            "passed": all(under(path, ROOT) for path in all_generated_paths),
            "requirement": "all generated outputs are inside post-checkpoint-work",
            "evidence": str(ROOT),
        }
    ),
    base(
        {
            "validation_id": "VAL3038_11_formalization_untouched",
            "passed": sum(1 for path in all_generated_paths if under(path, FORMALIZATION)) == 0,
            "requirement": "formalization-workbench modified-file target count remains 0",
            "evidence": "formalization_output_hits=0",
        }
    ),
    base(
        {
            "validation_id": "VAL3038_12_next_target",
            "passed": bool(next_rows) and next_rows[0]["next_checkpoint"].startswith("3039-"),
            "requirement": "next target selects relative source-vertex theorem or first XiH bound row",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3038_13_pycache_removed",
            "passed": not PYCACHE.exists(),
            "requirement": "scripts __pycache__ removed",
            "evidence": str(PYCACHE),
        }
    ),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3038 - Common Source Functional Normal Form Or XiH Bound Runner under AX1090

Status: `Y5_R2FR_3038_common_source_normal_form_written_but_relative_weight_missing_bound_runner_fail_closed`

## Verdict

3038 takes the 3037 gate

`delta_A_source = Xi_H/C_WH - 1 + R_lock`

and asks whether a common parent source functional can close it. The best local normal form is

`S_src^loc = integral mu_obs rho_H(e_obs,Psi,tau)[a_H psi_N + a_W chi_W] + O(2)`, with `chi_W:=W/c^2`.

This is useful: it makes the two source equations share the same observed density `rho_H`. But it still does **not** prove local GR/Newton, because the parent action can retain independent source-vertex weights and operator normalizations. The exact remaining condition is

`Xi_H=C_WH iff -a_H/(C_N K0)=a_W/O_W`

plus `R_lock=0` or a finite arena-bound residual vector.

So 3038 does not claim a pass. It sharpens the next target: prove the relative source-vertex weight/operator-normalization theorem, or source a finite `Xi_H/delta_XiH/R_lock` bound row.

## Common Source Functional Normal Form

{md_table(normal_form_rows, ["normal_form_id", "object", "formal_statement", "status", "missing_for_claim"])}

## Functional Derivative Match Audit

{md_table(derivative_match_rows, ["match_id", "test", "required_identity", "result", "blocks_claim"])}

## XiH Bound Runner Schema

{md_table(bound_runner_rows, ["bound_id", "quantity", "definition", "required_input", "current_status", "validity_rule"])}

## Delta A Source Evaluator Dry Run

{md_table(dryrun_rows, ["dryrun_id", "formula", "input_status", "computed_value", "runner_result", "claim_result"])}

## Countermodel Ledger

{md_table(countermodel_rows, ["countermodel_id", "countermodel", "effect", "status"])}

## Promotion Gates

{md_table(gates, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "question", "answer", "reason", "next_action"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "do_not_repeat", "claim_policy"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}
"""

DOC.write_text(doc, encoding="utf-8")

print(f"Wrote {DOC}")
print(f"Wrote validation {OUTPUTS['validation']}")
print("3038 verdict: common source functional normal form written, but relative source-vertex weight theorem is missing; bound runner fails closed.")

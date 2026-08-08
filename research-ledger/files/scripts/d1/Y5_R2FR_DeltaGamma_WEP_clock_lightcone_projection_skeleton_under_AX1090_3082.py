from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3082"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3082-Y5-R2FR-DeltaGamma-WEP-clock-lightcone-projection-skeleton-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3082_00_3081_doc": ROOT / "3081-Y5-R2FR-DeltaGamma-component-map-to-P4-observables-under-AX1090.md",
    "SRC3082_01_3081_next": RESIDUALS / "P8_Y5_R2FR_3081_NEXT_TARGET.csv",
    "SRC3082_02_3081_projection_queue": RESIDUALS / "P8_Y5_R2FR_3081_PROJECTION_MATRIX_QUEUE_NONCLAIM.csv",
    "SRC3082_03_3081_component_map": RESIDUALS / "P8_Y5_R2FR_3081_DELTAGAMMA_COMPONENT_OBSERVABLE_MAP_NONCLAIM.csv",
    "SRC3082_04_3081_arena_requirements": RESIDUALS / "P8_Y5_R2FR_3081_ARENA_PROJECTION_REQUIREMENTS_NONCLAIM.csv",
    "SRC3082_05_3081_score_blockers": RESIDUALS / "P8_Y5_R2FR_3081_SCORE_BLOCKER_LEDGER.csv",
    "SRC3082_06_3081_missing_artifacts": RESIDUALS / "P8_Y5_R2FR_3081_MISSING_PRIOR_ARTIFACTS_LEDGER.csv",
    "SRC3082_07_1835_arena": RESIDUALS / "P8_Y5_PARENT_QLOC_1835_ARENA_PROJECTION_REQUIREMENTS.csv",
    "SRC3082_08_1835_map": RESIDUALS / "P8_Y5_PARENT_QLOC_1835_DELTAGAMMA_COMPONENT_OBSERVABLE_MAP.csv",
    "SRC3082_09_1836_decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1836_DECISION_LEDGER.csv",
    "SRC3082_10_dotg_target": DOTG_TARGET,
}

MISSING_PRIOR_ARTIFACTS = {
    "MISS3082_0_1836_wcl_skeleton": RESIDUALS
    / "P8_Y5_PARENT_QLOC_1836_DELTAGAMMA_WEP_CLOCK_LIGHTCONE_PROJECTION_SKELETON.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3082_SOURCE_REGISTER.csv",
    "projection_skeleton": RESIDUALS / "P8_Y5_R2FR_3082_WEP_CLOCK_LIGHTCONE_PROJECTION_SKELETON_NONCLAIM.csv",
    "wep_requirements": RESIDUALS / "P8_Y5_R2FR_3082_WEP_RESPONSE_OPERATOR_REQUIREMENTS.csv",
    "clock_requirements": RESIDUALS / "P8_Y5_R2FR_3082_CLOCK_RESPONSE_OPERATOR_REQUIREMENTS.csv",
    "lightcone_requirements": RESIDUALS / "P8_Y5_R2FR_3082_LIGHTCONE_RESPONSE_OPERATOR_REQUIREMENTS.csv",
    "projective_guard": RESIDUALS / "P8_Y5_R2FR_3082_PROJECTIVE_GUARD_REQUIREMENTS.csv",
    "score_blockers": RESIDUALS / "P8_Y5_R2FR_3082_SCORE_BLOCKER_LEDGER.csv",
    "missing_artifacts": RESIDUALS / "P8_Y5_R2FR_3082_MISSING_PRIOR_ARTIFACTS_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3082_DECISION_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3082_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3082_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3082_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3082_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "projection_skeleton_copy": LOCAL_BOUNDS / "DeltaGamma_WEP_clock_lightcone_projection_skeleton_3082_NONCLAIM.csv",
    "wep_requirements_copy": LOCAL_BOUNDS / "DeltaGamma_WEP_requirements_3082_NONCLAIM.csv",
    "clock_lightcone_requirements_copy": LOCAL_BOUNDS
    / "DeltaGamma_clock_lightcone_requirements_3082_NONCLAIM.csv",
    "projective_guard_copy": LOCAL_BOUNDS / "DeltaGamma_projective_guard_3082_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3082_PWEP_from_matter_functor_or_component_bound_NEXT_NONCLAIM.csv",
}

for output_path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    output_path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


def file_hash(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "passed"}


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_ok(path) if path.suffix.lower() == ".csv" else True


def row_count(path: Path) -> int:
    if not path.exists():
        return 0
    if path.suffix.lower() == ".csv":
        return len(rows(path))
    return len(path.read_text(encoding="utf-8").splitlines())


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for output_row in output_rows:
            writer.writerow({key: output_row.get(key, "") for key in fieldnames})


def under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def has_claim_true(input_rows: list[dict[str, Any]]) -> bool:
    claim_fields = {
        "valid_for_claim",
        "claim_allowed",
        "valid_prediction_row",
        "score_ready",
        "claim_active",
        "projection_ready",
        "matrix_ready",
        "numeric_ready",
        "score_allowed",
        "arena_ready",
        "local_gr_claim",
        "component_claim",
        "operator_ready",
        "coefficient_ready",
        "bound_ready",
    }
    for input_row in input_rows:
        for field in claim_fields:
            if field in input_row and boolish(input_row[field]):
                return True
    return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": "false",
        "valid_prediction_row": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
        **row,
    }


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(table_rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not table_rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for table_row in table_rows:
        lines.append("| " + " | ".join(md_escape(table_row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def copy_csv(source_path: Path, destination_path: Path) -> None:
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_path, destination_path)


remove_pycache()
dotg_hash_before = file_hash(DOTG_TARGET)

source_register = [
    base(
        {
            "source_id": source_id,
            "source_path": str(source_path),
            "exists": str(source_path.exists()),
            "parse_ok": str(source_parse_ok(source_path)),
            "row_count": row_count(source_path),
            "role": "WEP_clock_lightcone_projection_skeleton_evidence"
            if source_id != "SRC3082_10_dotg_target"
            else "append_guard_target",
            "status": "PRESENT" if source_path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, source_path in SOURCE_PATHS.items()
]

projection_rows = [
    base(
        {
            "projection_id": "P_WCL_0_WEP",
            "projection_name": "P_DeltaGamma_to_eta_AB",
            "observable": "eta_AB;eta_source_AB",
            "domain": "Delta_spin;Delta_material_marker;Delta_clock_rod;Delta_projective_boundary",
            "codomain": "eta_AB;eta_source_AB",
            "skeleton_equation": "eta_AB = P_WEP_spin*Delta_spin + P_WEP_material*Delta_material_marker + P_WEP_clock*Delta_clock_rod + P_WEP_projective*Delta_projective_boundary",
            "units_required": "dimensionless_eta_output;common_DeltaGamma_normalization;composition_response_units",
            "missing_for_claim": "MISSING_MATERIAL_TENSOR;MISSING_COMPOSITION_RESPONSE;MISSING_NO_SPECIES_REENTRY;MISSING_UNITS;MISSING_SOURCE_BACKED_BOUND",
            "projection_ready": "false",
            "matrix_ready": "false",
            "coefficient_ready": "false",
            "source_ids": "SRC3082_02_3081_projection_queue;SRC3082_03_3081_component_map;SRC3082_07_1835_arena",
            "status": "SKELETON_ONLY_NONCLAIM",
        }
    ),
    base(
        {
            "projection_id": "P_WCL_1_clock",
            "projection_name": "P_DeltaGamma_to_clock_functional",
            "observable": "clock_residual;redshift_fractional_deviation",
            "domain": "Delta_clock_rod;Delta_spin;Delta_material_marker;Delta_projective_boundary",
            "codomain": "clock_residual;redshift_fractional_deviation",
            "skeleton_equation": "clock_residual = P_clock_clockrod*Delta_clock_rod + P_clock_spin*Delta_spin + P_clock_material*Delta_material_marker + P_clock_projective*Delta_projective_boundary",
            "units_required": "fractional_frequency_or_redshift_units;common_DeltaGamma_normalization;clock_species_basis",
            "missing_for_claim": "MISSING_CLOCK_FUNCTIONAL;MISSING_CLOCK_SPECIES_BASIS;MISSING_COFIELD_LOCK;MISSING_REDSHIFT_UNITS",
            "projection_ready": "false",
            "matrix_ready": "false",
            "coefficient_ready": "false",
            "source_ids": "SRC3082_02_3081_projection_queue;SRC3082_03_3081_component_map;SRC3082_07_1835_arena",
            "status": "SKELETON_ONLY_NONCLAIM",
        }
    ),
    base(
        {
            "projection_id": "P_WCL_2_lightcone",
            "projection_name": "P_DeltaGamma_to_null_cone",
            "observable": "lightcone_residual;gamma_minus_1",
            "domain": "Delta_lightcone;Delta_clock_rod;Delta_spin",
            "codomain": "lightcone_residual;gamma_minus_1",
            "skeleton_equation": "lightcone_residual = P_light_lightcone*Delta_lightcone + P_light_clockrod*Delta_clock_rod + P_light_spin*Delta_spin",
            "units_required": "dimensionless_metric_or_null_cone_residual;common_DeltaGamma_normalization;gauge_declared",
            "missing_for_claim": "MISSING_LIGHTCONE_OPERATOR;MISSING_GAUGE_CHOICE;MISSING_PHOTON_BRANCH;MISSING_GAMMA_OUTPUT_CONVENTION",
            "projection_ready": "false",
            "matrix_ready": "false",
            "coefficient_ready": "false",
            "source_ids": "SRC3082_02_3081_projection_queue;SRC3082_03_3081_component_map;SRC3082_07_1835_arena",
            "status": "SKELETON_ONLY_NONCLAIM",
        }
    ),
    base(
        {
            "projection_id": "P_WCL_3_projective_guard",
            "projection_name": "P_projective_invariance_all_sectors",
            "observable": "projective_invariance_certificate;residual_if_not_invariant",
            "domain": "Delta_projective_boundary",
            "codomain": "WEP_projective_residual;clock_projective_residual;source_projective_residual;boundary_tail",
            "skeleton_equation": "Delta_projective_boundary is ignorable only if P_projective_to_all_observed_sectors = 0; otherwise bound each residual channel",
            "units_required": "trace_connection_units;sector_response_units;boundary_projection_units",
            "missing_for_claim": "MISSING_ALL_SECTOR_PROJECTIVE_INVARIANCE;MISSING_TRACE_COUPLING_BOUND;MISSING_BOUNDARY_NO_FLUX_MAP",
            "projection_ready": "false",
            "matrix_ready": "false",
            "coefficient_ready": "false",
            "source_ids": "SRC3082_02_3081_projection_queue;SRC3082_03_3081_component_map",
            "status": "GUARD_ACTIVE_NONCLAIM",
        }
    ),
    base(
        {
            "projection_id": "P_WCL_4_combined_block",
            "projection_name": "P_WCL_combined_local_projection_block",
            "observable": "eta_AB;clock_residual;lightcone_residual",
            "domain": "Delta_spin;Delta_material_marker;Delta_clock_rod;Delta_lightcone;Delta_projective_boundary",
            "codomain": "eta_AB;clock_residual;lightcone_residual",
            "skeleton_equation": "(eta_AB, clock_residual, lightcone_residual)^T = P_WCL*(Delta_spin, Delta_material_marker, Delta_clock_rod, Delta_lightcone, Delta_projective_boundary)^T",
            "units_required": "block_diagonal_or_common_normalization_declared_before_any_score",
            "missing_for_claim": "MISSING_P_WEP;MISSING_P_CLOCK;MISSING_P_LIGHTCONE;MISSING_PROJECTIVE_GUARD;MISSING_COMPONENT_VALUES_OR_ZERO_THEOREMS",
            "projection_ready": "false",
            "matrix_ready": "false",
            "coefficient_ready": "false",
            "source_ids": "SRC3082_01_3081_next;SRC3082_02_3081_projection_queue",
            "status": "COMBINED_SKELETON_ONLY_NONCLAIM",
        }
    ),
]

wep_requirement_rows = [
    base(
        {
            "requirement_id": "WEPREQ3082_0_material_tensor",
            "operator": "P_WEP_material",
            "requirement": "derive or source the material/composition tensor mapping Delta_material_marker into differential acceleration",
            "needed_artifact": "matter functor species basis plus material tensor M_AB",
            "blocks": "eta_AB;eta_source_AB",
            "status": "MISSING_PARENT_INPUT",
            "operator_ready": "false",
        }
    ),
    base(
        {
            "requirement_id": "WEPREQ3082_1_composition_response",
            "operator": "P_WEP_spin;P_WEP_clock;P_WEP_projective",
            "requirement": "declare composition response matrix for spin, clock/rod and projective leakage channels",
            "needed_artifact": "composition response C_A^i - C_B^i in a common species frame",
            "blocks": "WEP score;no cancellation guard",
            "status": "MISSING_COMPOSITION_RESPONSE",
            "operator_ready": "false",
        }
    ),
    base(
        {
            "requirement_id": "WEPREQ3082_2_no_species_reentry",
            "operator": "matter_source_functor_guard",
            "requirement": "prove species/source labels do not re-enter through readout or explicitly bound the re-entry residual",
            "needed_artifact": "no species re-entry theorem or source-backed residual row",
            "blocks": "local-GR and WEP claim",
            "status": "MISSING_NO_SPECIES_REENTRY",
            "operator_ready": "false",
        }
    ),
    base(
        {
            "requirement_id": "WEPREQ3082_3_units_and_bound",
            "operator": "eta_normalization",
            "requirement": "lock dimensionless eta units and later compare to a source-backed WEP bound",
            "needed_artifact": "eta_AB normalization;MICROSCOPE/Ti-Pt or equivalent source row",
            "blocks": "numeric WEP comparator",
            "status": "MISSING_UNITS_AND_BOUND_SOURCE",
            "operator_ready": "false",
        }
    ),
]

clock_requirement_rows = [
    base(
        {
            "requirement_id": "CLKREQ3082_0_clock_functional",
            "operator": "P_clock_clockrod",
            "requirement": "derive the clock functional from matter/coframe coupling instead of assigning a drift coefficient",
            "needed_artifact": "clock action or clock readout functional C_clock[Phi,Psi,theta]",
            "blocks": "clock_residual",
            "status": "MISSING_CLOCK_FUNCTIONAL",
            "operator_ready": "false",
        }
    ),
    base(
        {
            "requirement_id": "CLKREQ3082_1_clock_species_basis",
            "operator": "P_clock_material;P_clock_spin",
            "requirement": "declare which clock species/basis responds to spin and material DeltaGamma channels",
            "needed_artifact": "clock species basis and sensitivity coefficients as derived or sourced rows",
            "blocks": "redshift_fractional_deviation",
            "status": "MISSING_CLOCK_SPECIES_BASIS",
            "operator_ready": "false",
        }
    ),
    base(
        {
            "requirement_id": "CLKREQ3082_2_coframe_lock",
            "operator": "observed_time_lock",
            "requirement": "prove the observed clock/coframe frame is locked or write the extra frame drift residual",
            "needed_artifact": "coframe lock theorem or frame-drift residual bound",
            "blocks": "clock and WEP cross-claim",
            "status": "MISSING_COFIELD_LOCK",
            "operator_ready": "false",
        }
    ),
    base(
        {
            "requirement_id": "CLKREQ3082_3_redshift_units",
            "operator": "redshift_normalization",
            "requirement": "define fractional-frequency/redshift units and source-backed comparison target",
            "needed_artifact": "dimensionless redshift convention plus clock/redshift bound source row",
            "blocks": "clock comparator",
            "status": "MISSING_REDSHIFT_UNITS",
            "operator_ready": "false",
        }
    ),
]

lightcone_requirement_rows = [
    base(
        {
            "requirement_id": "LGTREQ3082_0_null_cone_operator",
            "operator": "P_light_lightcone",
            "requirement": "derive the null-cone response operator from metric/coframe/nonmetricity branch",
            "needed_artifact": "linearized null-cone operator acting on Delta_lightcone",
            "blocks": "lightcone_residual;gamma_minus_1",
            "status": "MISSING_LIGHTCONE_OPERATOR",
            "operator_ready": "false",
        }
    ),
    base(
        {
            "requirement_id": "LGTREQ3082_1_gauge_choice",
            "operator": "lightcone_gauge_guard",
            "requirement": "state the gauge and prove the residual is gauge-invariant or keep the gauge blocker active",
            "needed_artifact": "gauge convention plus invariant residual definition",
            "blocks": "PPN gamma and lightcone score",
            "status": "MISSING_GAUGE_CHOICE",
            "operator_ready": "false",
        }
    ),
    base(
        {
            "requirement_id": "LGTREQ3082_2_photon_branch",
            "operator": "P_light_photon_readout",
            "requirement": "declare whether photons follow the same coframe/connection branch as material clocks",
            "needed_artifact": "photon/readout branch statement derived from parent action",
            "blocks": "lightcone-clock consistency",
            "status": "MISSING_PHOTON_BRANCH",
            "operator_ready": "false",
        }
    ),
    base(
        {
            "requirement_id": "LGTREQ3082_3_gamma_convention",
            "operator": "gamma_output_map",
            "requirement": "define the conversion from lightcone residual to gamma_minus_1 without hiding fitted-G/source terms",
            "needed_artifact": "gamma output convention and source-normalization split",
            "blocks": "PPN bridge",
            "status": "MISSING_GAMMA_OUTPUT_CONVENTION",
            "operator_ready": "false",
        }
    ),
]

projective_guard_rows = [
    base(
        {
            "guard_id": "PGRD3082_0_all_sector_invariance",
            "guard": "all-sector projective invariance",
            "condition": "P_projective_to_WEP = P_projective_to_clock = P_projective_to_source = P_projective_to_lightcone = 0",
            "why_needed": "a projective trace may be gauge only if every observed sector is invariant",
            "failure_mode": "hidden species, clock, source or boundary force leakage",
            "status": "UNSIGNED_GUARD_ACTIVE",
            "bound_ready": "false",
        }
    ),
    base(
        {
            "guard_id": "PGRD3082_1_trace_coupling_bound",
            "guard": "explicit trace coupling bound",
            "condition": "if any projective projection is nonzero, source the coefficient and bound the residual",
            "why_needed": "prevents claiming projective invisibility by notation",
            "failure_mode": "false local-GR pass from gauge assumption",
            "status": "MISSING_TRACE_COUPLING_BOUND",
            "bound_ready": "false",
        }
    ),
    base(
        {
            "guard_id": "PGRD3082_2_boundary_silence",
            "guard": "boundary/local projection silence",
            "condition": "boundary term contributes no local residual or has a source-backed bound",
            "why_needed": "Delta_projective_boundary can leak into R10/WEP/clock tails",
            "failure_mode": "unbounded local boundary force",
            "status": "MISSING_BOUNDARY_NO_FLUX_MAP",
            "bound_ready": "false",
        }
    ),
]

score_blocker_rows = [
    base(
        {
            "blocker_id": "SBL3082_0_projection_matrices",
            "blocks": "WEP/clock/lightcone scores",
            "missing": "P_WEP, P_clock, P_lightcone and projective guard matrices",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3082_1_component_values",
            "blocks": "all local arenas",
            "missing": "DeltaGamma component values or parent zero theorems",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3082_2_common_units",
            "blocks": "combined P_WCL vector",
            "missing": "common DeltaGamma normalization and observable output units",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3082_3_no_cancellation_guard",
            "blocks": "combined local pass",
            "missing": "individual component pass or parent cancellation identity",
            "status": "GUARD_ACTIVE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3082_4_source_bounds",
            "blocks": "claim comparison",
            "missing": "source-backed WEP, clock and lightcone bounds connected to the skeleton units",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
]

missing_artifact_rows = [
    base(
        {
            "artifact_id": artifact_id,
            "artifact_path": str(artifact_path),
            "exists": str(artifact_path.exists()),
            "impact": "prior 1836 decision says a WEP/clock/lightcone skeleton existed, but the artifact is absent; 3082 therefore refreshes it from 3081 and records non-reliance",
            "status": "MISSING_PRIOR_ACKNOWLEDGED_NOT_USED_FOR_CLAIM"
            if not artifact_path.exists()
            else "PRESENT_BUT_NOT_NEEDED_FOR_CLAIM",
        }
    )
    for artifact_id, artifact_path in MISSING_PRIOR_ARTIFACTS.items()
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3082_0_skeleton_result",
            "decision": "WEP_CLOCK_LIGHTCONE_PROJECTION_SKELETON_WRITTEN_NONCLAIM",
            "reason": "3082 declares the combined projection block and the individual WEP, clock, lightcone and projective guard equations without inserting coefficients",
            "next_action": "do not score WEP/clock/lightcone yet",
        }
    ),
    base(
        {
            "decision_id": "DEC3082_1_core_gap",
            "decision": "RESPONSE_OPERATORS_NOT_DERIVED",
            "reason": "P_WEP, P_clock, P_lightcone, projective all-sector silence, units and component values remain unsigned",
            "next_action": "derive the first response operator rather than fit it",
        }
    ),
    base(
        {
            "decision_id": "DEC3082_2_best_next",
            "decision": "P_WEP_FROM_MATTER_FUNCTOR_OR_COMPONENT_BOUND_NEXT",
            "reason": "WEP is the harshest local-coupling test and shares the missing matter-functor machinery with clocks and source charge",
            "next_action": "3083-Y5-R2FR-PWEP-response-operator-from-matter-functor-or-component-bound-under-AX1090.md",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3082_0_projection_skeleton",
            "claim": "P_WCL skeleton is a predictive local test",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "domains and codomains are declared but response operators and coefficients are not derived",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3082_1_WEP_clock_lightcone",
            "claim": "WEP/clock/lightcone pass",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "missing P_WEP, P_clock, P_lightcone, units, source bounds and component values",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3082_2_local_GR",
            "claim": "local GR/Newton recovery follows",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "DeltaGamma, DeltaK, P4 and arena projections remain open",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3082_0_3083",
            "next_checkpoint": "3083-Y5-R2FR-PWEP-response-operator-from-matter-functor-or-component-bound-under-AX1090.md",
            "script": "scripts/Y5_R2FR_PWEP_response_operator_from_matter_functor_or_component_bound_under_AX1090_3083.py",
            "mission": "derive P_WEP from the matter/source functor, or stage source-ready WEP component-bound rows if the functor cannot be signed",
            "starting_equation": "eta_AB = P_WEP_spin*Delta_spin + P_WEP_material*Delta_material_marker + P_WEP_clock*Delta_clock_rod + P_WEP_projective*Delta_projective_boundary",
            "claim_policy": "no WEP, local-GR or Newton claim until P_WEP, units, material tensor, no species/source re-entry, and component values or zero theorems exist",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["projection_skeleton"], projection_rows)
write_csv(OUTPUTS["wep_requirements"], wep_requirement_rows)
write_csv(OUTPUTS["clock_requirements"], clock_requirement_rows)
write_csv(OUTPUTS["lightcone_requirements"], lightcone_requirement_rows)
write_csv(OUTPUTS["projective_guard"], projective_guard_rows)
write_csv(OUTPUTS["score_blockers"], score_blocker_rows)
write_csv(OUTPUTS["missing_artifacts"], missing_artifact_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["projection_skeleton"], BRANCH_OUTPUTS["projection_skeleton_copy"])
copy_csv(OUTPUTS["wep_requirements"], BRANCH_OUTPUTS["wep_requirements_copy"])

clock_lightcone_combined = clock_requirement_rows + lightcone_requirement_rows
write_csv(BRANCH_OUTPUTS["clock_lightcone_requirements_copy"], clock_lightcone_combined)
copy_csv(OUTPUTS["projective_guard"], BRANCH_OUTPUTS["projective_guard_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "source_path": str(source_path),
            "copy_path": str(copy_path),
            "copy_exists": str(copy_path.exists()),
            "copy_parse_ok": str(csv_ok(copy_path)),
            "status": "BRANCH_COPY_READY_NONCLAIM" if copy_path.exists() else "BRANCH_COPY_MISSING",
        }
    )
    for copy_id, source_path, copy_path in [
        ("BR3082_0_projection_skeleton", OUTPUTS["projection_skeleton"], BRANCH_OUTPUTS["projection_skeleton_copy"]),
        ("BR3082_1_wep_requirements", OUTPUTS["wep_requirements"], BRANCH_OUTPUTS["wep_requirements_copy"]),
        (
            "BR3082_2_clock_lightcone_requirements",
            OUTPUTS["clock_requirements"],
            BRANCH_OUTPUTS["clock_lightcone_requirements_copy"],
        ),
        ("BR3082_3_projective_guard", OUTPUTS["projective_guard"], BRANCH_OUTPUTS["projective_guard_copy"]),
        ("BR3082_4_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
]
write_csv(OUTPUTS["branches"], branch_rows)

DOC.write_text("# 3082 - DeltaGamma WEP/Clock/Lightcone Projection Skeleton\n\nPreparing validation.\n", encoding="utf-8")

dotg_hash_after = file_hash(DOTG_TARGET)
generated_csvs = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
generated_rows = (
    source_register
    + projection_rows
    + wep_requirement_rows
    + clock_requirement_rows
    + lightcone_requirement_rows
    + projective_guard_rows
    + score_blocker_rows
    + missing_artifact_rows
    + decision_rows
    + claim_rows
    + next_rows
    + branch_rows
)
formalization_output_count = sum(1 for output_path in generated_csvs + [DOC] if under(output_path, FORMALIZATION))
required_projection_ids = {
    "P_WCL_0_WEP",
    "P_WCL_1_clock",
    "P_WCL_2_lightcone",
    "P_WCL_3_projective_guard",
    "P_WCL_4_combined_block",
}
required_wep_requirements = {"WEPREQ3082_0_material_tensor", "WEPREQ3082_1_composition_response", "WEPREQ3082_2_no_species_reentry", "WEPREQ3082_3_units_and_bound"}
required_clock_requirements = {"CLKREQ3082_0_clock_functional", "CLKREQ3082_1_clock_species_basis", "CLKREQ3082_2_coframe_lock", "CLKREQ3082_3_redshift_units"}
required_lightcone_requirements = {"LGTREQ3082_0_null_cone_operator", "LGTREQ3082_1_gauge_choice", "LGTREQ3082_2_photon_branch", "LGTREQ3082_3_gamma_convention"}
required_projective_guards = {"PGRD3082_0_all_sector_invariance", "PGRD3082_1_trace_coupling_bound", "PGRD3082_2_boundary_silence"}

validation_rows = [
    base(
        {
            "validation_id": "VAL3082_00_sources_exist",
            "passed": str(all(row["exists"] == "True" for row in source_register)),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3082_01_sources_parse",
            "passed": str(all(row["parse_ok"] == "True" for row in source_register)),
            "requirement": "all cited CSV sources parse and markdown sources exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3082_02_csv_parse",
            "passed": str(all(csv_ok(output_path) for output_path in generated_csvs if output_path != OUTPUTS["validation"])),
            "requirement": "all generated and branch-copy CSVs parse cleanly before validation write",
            "evidence": "csv.DictReader parse check",
        }
    ),
    base(
        {
            "validation_id": "VAL3082_03_projection_rows_present",
            "passed": str(required_projection_ids.issubset({row["projection_id"] for row in projection_rows})),
            "requirement": "WEP, clock, lightcone, projective guard and combined block rows are present",
            "evidence": OUTPUTS["projection_skeleton"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3082_04_projection_rows_nonclaim",
            "passed": str(not has_claim_true(projection_rows)),
            "requirement": "all projection skeleton rows remain nonclaim and unready",
            "evidence": OUTPUTS["projection_skeleton"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3082_05_wep_requirements_complete",
            "passed": str(required_wep_requirements.issubset({row["requirement_id"] for row in wep_requirement_rows}) and not has_claim_true(wep_requirement_rows)),
            "requirement": "WEP material tensor, composition response, no species re-entry and units/bound requirements are recorded",
            "evidence": OUTPUTS["wep_requirements"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3082_06_clock_requirements_complete",
            "passed": str(required_clock_requirements.issubset({row["requirement_id"] for row in clock_requirement_rows}) and not has_claim_true(clock_requirement_rows)),
            "requirement": "clock functional, clock species basis, coframe lock and redshift units requirements are recorded",
            "evidence": OUTPUTS["clock_requirements"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3082_07_lightcone_requirements_complete",
            "passed": str(required_lightcone_requirements.issubset({row["requirement_id"] for row in lightcone_requirement_rows}) and not has_claim_true(lightcone_requirement_rows)),
            "requirement": "null-cone operator, gauge choice, photon branch and gamma convention requirements are recorded",
            "evidence": OUTPUTS["lightcone_requirements"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3082_08_projective_guard_complete",
            "passed": str(required_projective_guards.issubset({row["guard_id"] for row in projective_guard_rows}) and not has_claim_true(projective_guard_rows)),
            "requirement": "projective all-sector invariance, trace coupling and boundary silence guards are active",
            "evidence": OUTPUTS["projective_guard"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3082_09_score_blockers_active",
            "passed": str(not has_claim_true(score_blocker_rows) and all(row["status"] in {"BLOCKS_SCORE", "GUARD_ACTIVE"} for row in score_blocker_rows)),
            "requirement": "projection, values, units, no-cancellation and source-bound blockers remain active",
            "evidence": OUTPUTS["score_blockers"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3082_10_missing_1836_recorded",
            "passed": str(any(row["artifact_id"] == "MISS3082_0_1836_wcl_skeleton" and row["exists"] == "False" for row in missing_artifact_rows)),
            "requirement": "missing prior 1836 WEP/clock/lightcone skeleton artifact is acknowledged and not relied on",
            "evidence": OUTPUTS["missing_artifacts"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3082_11_no_claim_promoted",
            "passed": str(not has_claim_true(generated_rows)),
            "requirement": "no WEP, clock, lightcone, score, Newton or local-GR claim is promoted",
            "evidence": "claim field scan",
        }
    ),
    base(
        {
            "validation_id": "VAL3082_12_next_target_selected",
            "passed": str(next_rows[0]["next_checkpoint"].startswith("3083-Y5-R2FR-PWEP-response-operator")),
            "requirement": "next target moves to P_WEP response operator from matter functor or component bound",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3082_13_branch_copies_exist",
            "passed": str(all(row["copy_exists"] == "True" and row["copy_parse_ok"] == "True" for row in branch_rows)),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3082_14_dotg_unchanged",
            "passed": str(dotg_hash_before == dotg_hash_after),
            "requirement": "P8_time_drift_residual_or_zero.csv is not modified",
            "evidence": f"{dotg_hash_before}->{dotg_hash_after}",
        }
    ),
    base(
        {
            "validation_id": "VAL3082_15_outputs_under_post_checkpoint",
            "passed": str(all(under(output_path, ROOT) for output_path in generated_csvs + [DOC])),
            "requirement": "all outputs are under post-checkpoint-work",
            "evidence": "path containment check",
        }
    ),
    base(
        {
            "validation_id": "VAL3082_16_no_formalization_outputs",
            "passed": str(formalization_output_count == 0),
            "requirement": "formalization-workbench modified-file count for 3082 outputs remains zero",
            "evidence": f"formalization_3082_output_paths={formalization_output_count}",
        }
    ),
    base(
        {
            "validation_id": "VAL3082_17_pycache_absent",
            "passed": str(not PYCACHE.exists()),
            "requirement": "scripts __pycache__ is absent at generator completion",
            "evidence": str(PYCACHE),
        }
    ),
    base(
        {
            "validation_id": "VAL3082_18_doc_written",
            "passed": str(DOC.exists()),
            "requirement": "checkpoint markdown document is written",
            "evidence": str(DOC),
        }
    ),
]

write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3082 - DeltaGamma WEP/Clock/Lightcone Projection Skeleton

Status: `Y5_R2FR_3082_WEP_clock_lightcone_projection_skeleton_nonclaim`

Generated: `{RUN_UTC}`

## Verdict

3082 builds the first concrete local-observable projection block after the `Delta_Gamma` map. It does **not** derive the response matrices yet and it does **not** claim WEP, clock, lightcone, Newtonian or local-GR success.

The useful step is that the local coupling problem is now written as one explicit block:

`(eta_AB, clock_residual, lightcone_residual)^T = P_WCL * (Delta_spin, Delta_material_marker, Delta_clock_rod, Delta_lightcone, Delta_projective_boundary)^T`

This makes the missing work sharp. The next fight is not vague "does MTS reduce to GR"; it is whether the matter/source functor derives `P_WEP` and whether the remaining clock/lightcone/projective rows can be signed or bounded without fitted rescue terms.

## Projection Skeleton

{md_table(projection_rows, ["projection_id", "projection_name", "domain", "codomain", "skeleton_equation", "status"])}

## WEP Response Requirements

{md_table(wep_requirement_rows, ["requirement_id", "operator", "requirement", "status"])}

## Clock Response Requirements

{md_table(clock_requirement_rows, ["requirement_id", "operator", "requirement", "status"])}

## Lightcone Response Requirements

{md_table(lightcone_requirement_rows, ["requirement_id", "operator", "requirement", "status"])}

## Projective Guard

{md_table(projective_guard_rows, ["guard_id", "guard", "condition", "status"])}

## Score Blockers

{md_table(score_blocker_rows, ["blocker_id", "blocks", "missing", "status"])}

## Missing Prior Artifacts

{md_table(missing_artifact_rows, ["artifact_id", "exists", "impact", "status"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "reason", "next_action"])}

## Claim Status

{md_table(claim_rows, ["claim_id", "claim", "claim_active", "status", "reason"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "claim_policy"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files

- Source register: `{OUTPUTS["sources"]}`
- Projection skeleton: `{OUTPUTS["projection_skeleton"]}`
- WEP requirements: `{OUTPUTS["wep_requirements"]}`
- Clock requirements: `{OUTPUTS["clock_requirements"]}`
- Lightcone requirements: `{OUTPUTS["lightcone_requirements"]}`
- Projective guard: `{OUTPUTS["projective_guard"]}`
- Score blockers: `{OUTPUTS["score_blockers"]}`
- Missing prior artifacts: `{OUTPUTS["missing_artifacts"]}`
- Claim status: `{OUTPUTS["claim_status"]}`
- Next target: `{OUTPUTS["next"]}`
- Validation: `{OUTPUTS["validation"]}`
- Branch copy: `{BRANCH_OUTPUTS["projection_skeleton_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["wep_requirements_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["clock_lightcone_requirements_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["projective_guard_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["next_copy"]}`
"""

DOC.write_text(doc_text, encoding="utf-8")
remove_pycache()

print(f"Wrote {DOC}")
print(f"Wrote {OUTPUTS['validation']}")
print(f"Validation passed {sum(1 for row in validation_rows if row['passed'] == 'True')}/{len(validation_rows)}")

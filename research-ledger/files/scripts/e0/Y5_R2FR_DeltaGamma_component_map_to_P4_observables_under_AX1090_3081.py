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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3081"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3081-Y5-R2FR-DeltaGamma-component-map-to-P4-observables-under-AX1090.md"
DOTG_TARGET = RESIDUALS / "P8_time_drift_residual_or_zero.csv"

SOURCE_PATHS = {
    "SRC3081_00_3080_doc": ROOT / "3080-Y5-R2FR-no-hypermomentum-source-readout-functor-or-DeltaGamma-bound-under-AX1090.md",
    "SRC3081_01_3080_next": RESIDUALS / "P8_Y5_R2FR_3080_NEXT_TARGET.csv",
    "SRC3081_02_3080_bounds": RESIDUALS / "P8_Y5_R2FR_3080_DELTAGAMMA_BOUND_COMPONENTS_NONCLAIM.csv",
    "SRC3081_03_3080_sector": RESIDUALS / "P8_Y5_R2FR_3080_SOURCE_READOUT_SECTOR_SPLIT_LEDGER.csv",
    "SRC3081_04_3080_arenas": RESIDUALS / "P8_Y5_R2FR_3080_LOCAL_ARENA_BLOCKERS_NONCLAIM.csv",
    "SRC3081_05_3080_decision": RESIDUALS / "P8_Y5_R2FR_3080_DECISION_LEDGER.csv",
    "SRC3081_06_1835_map": RESIDUALS / "P8_Y5_PARENT_QLOC_1835_DELTAGAMMA_COMPONENT_OBSERVABLE_MAP.csv",
    "SRC3081_07_1835_arena": RESIDUALS / "P8_Y5_PARENT_QLOC_1835_ARENA_PROJECTION_REQUIREMENTS.csv",
    "SRC3081_08_1835_blockers": RESIDUALS / "P8_Y5_PARENT_QLOC_1835_SCORE_BLOCKER_LEDGER.csv",
    "SRC3081_09_1835_decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1835_DECISION_LEDGER.csv",
    "SRC3081_10_1835_next": RESIDUALS / "P8_Y5_PARENT_QLOC_1835_NEXT_TARGET.csv",
    "SRC3081_11_1836_decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1836_DECISION_LEDGER.csv",
    "SRC3081_12_dotg_target": DOTG_TARGET,
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3081_SOURCE_REGISTER.csv",
    "component_map": RESIDUALS / "P8_Y5_R2FR_3081_DELTAGAMMA_COMPONENT_OBSERVABLE_MAP_NONCLAIM.csv",
    "arena_requirements": RESIDUALS / "P8_Y5_R2FR_3081_ARENA_PROJECTION_REQUIREMENTS_NONCLAIM.csv",
    "projection_queue": RESIDUALS / "P8_Y5_R2FR_3081_PROJECTION_MATRIX_QUEUE_NONCLAIM.csv",
    "score_blockers": RESIDUALS / "P8_Y5_R2FR_3081_SCORE_BLOCKER_LEDGER.csv",
    "missing_artifacts": RESIDUALS / "P8_Y5_R2FR_3081_MISSING_PRIOR_ARTIFACTS_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3081_DECISION_LEDGER.csv",
    "claim_status": RESIDUALS / "P8_Y5_R2FR_3081_CLAIM_STATUS.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3081_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3081_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3081_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "component_map_copy": LOCAL_BOUNDS / "DeltaGamma_component_observable_map_3081_NONCLAIM.csv",
    "arena_requirements_copy": LOCAL_BOUNDS / "DeltaGamma_arena_projection_requirements_3081_NONCLAIM.csv",
    "projection_queue_copy": LOCAL_BOUNDS / "DeltaGamma_projection_matrix_queue_3081_NONCLAIM.csv",
    "blockers_copy": LOCAL_BOUNDS / "DeltaGamma_score_blockers_3081_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3081_DeltaGamma_WEP_clock_lightcone_projection_skeleton_NEXT_NONCLAIM.csv",
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
            "role": "DeltaGamma_component_to_observable_map_evidence" if source_id != "SRC3081_12_dotg_target" else "append_guard_target",
            "status": "PRESENT" if source_path.exists() else "MISSING_SOURCE",
        }
    )
    for source_id, source_path in SOURCE_PATHS.items()
]

component_map_rows = [
    base(
        {
            "map_id": "DGOM3081_0_spin",
            "DeltaGamma_component": "Delta_spin",
            "connection_channel": "axial_torsion_spin_coupling",
            "primary_observables": "spin_torsion_residual;clock_residual;lightcone_residual;eta_WEP;operator_ledger",
            "projection_required": "P_spin_to_axial_torsion;P_spin_to_clock;P_spin_to_lightcone;P_spin_to_WEP",
            "needed_inputs": "spin current norm;spin connection normalization;matter species basis;source path",
            "current_status": "MAP_SKELETON_ONLY_MISSING_PROJECTION",
            "projection_ready": "false",
            "component_claim": "false",
            "source_ids": "SRC3081_06_1835_map;SRC3081_02_3080_bounds",
        }
    ),
    base(
        {
            "map_id": "DGOM3081_1_material",
            "DeltaGamma_component": "Delta_material_marker",
            "connection_channel": "species_source_charge",
            "primary_observables": "eta_source_AB;eta_WEP;clock_redshift;operator_ledger",
            "projection_required": "P_material_to_composition;P_material_to_clock;P_material_to_source_charge",
            "needed_inputs": "material tensor;marker derivative;same-frame source basis;no hidden species theorem or bound",
            "current_status": "MAP_SKELETON_ONLY_MISSING_PROJECTION",
            "projection_ready": "false",
            "component_claim": "false",
            "source_ids": "SRC3081_06_1835_map",
        }
    ),
    base(
        {
            "map_id": "DGOM3081_2_source_support",
            "DeltaGamma_component": "Delta_source",
            "connection_channel": "source_normalization_operator",
            "primary_observables": "source_charge_residual;alpha(lambda);gamma_minus_1;beta_minus_1;orbital_GM;operator_ledger",
            "projection_required": "P_source_support_to_GM;P_source_support_to_R10;P_source_support_to_PPN",
            "needed_inputs": "worldtube support;source current norm;radial profile;range scale;GM transfer convention",
            "current_status": "MAP_SKELETON_ONLY_MISSING_PROJECTION",
            "projection_ready": "false",
            "component_claim": "false",
            "source_ids": "SRC3081_06_1835_map;SRC3081_02_3080_bounds",
        }
    ),
    base(
        {
            "map_id": "DGOM3081_3_clock_rods",
            "DeltaGamma_component": "Delta_clock_rod",
            "connection_channel": "nonmetricity_weyl_trace",
            "primary_observables": "clock_residual;rod_residual;redshift_fractional_deviation;eta_WEP;operator_ledger",
            "projection_required": "P_nonmetricity_to_clock;P_nonmetricity_to_rods;P_clock_to_WEP",
            "needed_inputs": "clock functional;rod calibration functional;Q_trace normalization;redshift bound source",
            "current_status": "MAP_SKELETON_ONLY_MISSING_PROJECTION",
            "projection_ready": "false",
            "component_claim": "false",
            "source_ids": "SRC3081_06_1835_map",
        }
    ),
    base(
        {
            "map_id": "DGOM3081_4_photon_lightcone",
            "DeltaGamma_component": "Delta_lightcone",
            "connection_channel": "nonmetricity_shear_lightcone",
            "primary_observables": "lightcone_residual;gamma_minus_1;clock_residual;eta_WEP;operator_ledger",
            "projection_required": "P_shearQ_to_lightcone;P_lightcone_to_gamma;P_lightcone_to_clock",
            "needed_inputs": "lightcone response operator;trace-free Q normalization;gauge choice;photon/readout branch",
            "current_status": "MAP_SKELETON_ONLY_MISSING_PROJECTION",
            "projection_ready": "false",
            "component_claim": "false",
            "source_ids": "SRC3081_06_1835_map",
        }
    ),
    base(
        {
            "map_id": "DGOM3081_5_orbital_readout",
            "DeltaGamma_component": "Delta_orbital_readout",
            "connection_channel": "source_readout_connection_current",
            "primary_observables": "orbital_GM;Gdot_over_G;alpha(lambda);beta_minus_1;gamma_minus_1;operator_ledger",
            "projection_required": "P_orbital_readout_to_GM;P_orbital_readout_to_Gdot;P_orbital_readout_to_fifth_force",
            "needed_inputs": "test-body readout action;inverse-square split;time/range law;no fitted GM absorption guard",
            "current_status": "MAP_SKELETON_ONLY_MISSING_PROJECTION",
            "projection_ready": "false",
            "component_claim": "false",
            "source_ids": "SRC3081_06_1835_map;SRC3081_03_3080_sector",
        }
    ),
    base(
        {
            "map_id": "DGOM3081_6_projective_boundary",
            "DeltaGamma_component": "Delta_projective_boundary",
            "connection_channel": "torsion_trace_projective_mode + boundary_connection_leakage",
            "primary_observables": "eta_WEP;source_charge_residual;clock_residual;projective_invariance_certificate;R10_boundary_tail;operator_ledger",
            "projection_required": "P_projective_to_source;P_projective_to_clock;P_projective_invariance_all_sectors;P_boundary_to_R10",
            "needed_inputs": "projective gauge rule;all-sector invariance proof;source/readout trace coupling bound;boundary no-flux map",
            "current_status": "MAP_SKELETON_ONLY_MISSING_PROJECTION",
            "projection_ready": "false",
            "component_claim": "false",
            "source_ids": "SRC3081_06_1835_map;SRC3081_02_3080_bounds",
        }
    ),
]

arena_requirement_rows = [
    base(
        {
            "arena_id": "ARENA3081_0_R10",
            "arena": "R10_short_range_inverse_square",
            "observable": "alpha(lambda)",
            "DeltaGamma_components": "Delta_source;Delta_orbital_readout;Delta_boundary",
            "required_projection": "P_DeltaGamma_to_alpha_lambda with source geometry, lambda scale and no fitted-G absorption",
            "current_status": "MISSING_R10_PROJECTION_AND_FULL_BOUND_CURVE",
            "arena_ready": "false",
            "source_ids": "SRC3081_07_1835_arena;SRC3081_04_3080_arenas",
        }
    ),
    base(
        {
            "arena_id": "ARENA3081_1_WEP",
            "arena": "WEP_MICROSCOPE",
            "observable": "eta_AB",
            "DeltaGamma_components": "Delta_spin;Delta_material_marker;Delta_clock_rod;Delta_projective_boundary",
            "required_projection": "P_DeltaGamma_to_eta_AB with material tensor and no measured-G absorption",
            "current_status": "MISSING_WEP_PROJECTION_MATRIX",
            "arena_ready": "false",
            "source_ids": "SRC3081_07_1835_arena;SRC3081_04_3080_arenas",
        }
    ),
    base(
        {
            "arena_id": "ARENA3081_2_PPN",
            "arena": "PPN",
            "observable": "gamma_minus_1;beta_minus_1;alpha1;alpha2;alpha3;xi",
            "DeltaGamma_components": "Delta_source;Delta_lightcone;Delta_orbital_readout;Delta_projective_boundary",
            "required_projection": "P_DeltaGamma_to_metric_PPN with gauge, trace-reversal and source-normalization split",
            "current_status": "MISSING_PPN_RESPONSE_OPERATOR",
            "arena_ready": "false",
            "source_ids": "SRC3081_07_1835_arena;SRC3081_04_3080_arenas",
        }
    ),
    base(
        {
            "arena_id": "ARENA3081_3_CLOCK",
            "arena": "clock_redshift",
            "observable": "redshift_fractional_deviation;clock_residual",
            "DeltaGamma_components": "Delta_clock_rod;Delta_spin;Delta_material_marker;Delta_projective_boundary",
            "required_projection": "P_DeltaGamma_to_clock_functional with clock species and coframe lock",
            "current_status": "MISSING_CLOCK_PROJECTION",
            "arena_ready": "false",
            "source_ids": "SRC3081_07_1835_arena;SRC3081_04_3080_arenas",
        }
    ),
    base(
        {
            "arena_id": "ARENA3081_4_LIGHTCONE",
            "arena": "lightcone_photon",
            "observable": "lightcone_residual;gamma_minus_1",
            "DeltaGamma_components": "Delta_lightcone;Delta_clock_rod;Delta_spin",
            "required_projection": "P_DeltaGamma_to_null_cone with photon/readout branch and gauge control",
            "current_status": "MISSING_LIGHTCONE_PROJECTION",
            "arena_ready": "false",
            "source_ids": "SRC3081_07_1835_arena",
        }
    ),
    base(
        {
            "arena_id": "ARENA3081_5_ORBITAL",
            "arena": "orbital_Newton_source_normalization",
            "observable": "orbital_GM;Gdot_over_G;anomalous_radial_acceleration",
            "DeltaGamma_components": "Delta_orbital_readout;Delta_source;Delta_projective_boundary",
            "required_projection": "P_DeltaGamma_to_orbital_readout with inverse-square split and no fitted-G shortcut",
            "current_status": "MISSING_ORBITAL_SOURCE_PROJECTION",
            "arena_ready": "false",
            "source_ids": "SRC3081_07_1835_arena;SRC3081_04_3080_arenas",
        }
    ),
]

projection_queue_rows = [
    base(
        {
            "projection_id": "PMQ3081_0_WEP",
            "projection_matrix": "P_DeltaGamma_to_eta_AB",
            "priority": "first",
            "why_first": "WEP is the harshest local-coupling channel and shares the missing matter/source functor machinery",
            "domain": "Delta_spin;Delta_material_marker;Delta_clock_rod;Delta_projective_boundary",
            "codomain": "eta_AB;eta_source_AB",
            "matrix_ready": "false",
            "missing_for_claim": "MISSING_MATERIAL_TENSOR;MISSING_COMPOSITION_RESPONSE;MISSING_NO_SPECIES_REENTRY;MISSING_UNITS",
        }
    ),
    base(
        {
            "projection_id": "PMQ3081_1_clock",
            "projection_matrix": "P_DeltaGamma_to_clock_functional",
            "priority": "first_block_with_WEP",
            "why_first": "clock and WEP channels share rod/clock/source-label leakage",
            "domain": "Delta_clock_rod;Delta_spin;Delta_material_marker;Delta_projective_boundary",
            "codomain": "clock_residual;redshift_fractional_deviation",
            "matrix_ready": "false",
            "missing_for_claim": "MISSING_CLOCK_FUNCTIONAL;MISSING_CLOCK_SPECIES_BASIS;MISSING_COFIELD_LOCK",
        }
    ),
    base(
        {
            "projection_id": "PMQ3081_2_lightcone",
            "projection_matrix": "P_DeltaGamma_to_null_cone",
            "priority": "first_block_with_WEP",
            "why_first": "lightcone response catches shear nonmetricity and spin/light coupling leakage",
            "domain": "Delta_lightcone;Delta_clock_rod;Delta_spin",
            "codomain": "lightcone_residual;gamma_minus_1",
            "matrix_ready": "false",
            "missing_for_claim": "MISSING_LIGHTCONE_OPERATOR;MISSING_GAUGE_CHOICE;MISSING_PHOTON_BRANCH",
        }
    ),
    base(
        {
            "projection_id": "PMQ3081_3_R10",
            "projection_matrix": "P_DeltaGamma_to_alpha_lambda",
            "priority": "secondary",
            "why_first": "held until source/orbital support map and range scale are declared",
            "domain": "Delta_source;Delta_orbital_readout;Delta_boundary",
            "codomain": "alpha(lambda);force_gradient",
            "matrix_ready": "false",
            "missing_for_claim": "MISSING_SOURCE_GEOMETRY;MISSING_LENGTH_SCALE;MISSING_FULL_BOUND_CURVE",
        }
    ),
    base(
        {
            "projection_id": "PMQ3081_4_PPN_orbital",
            "projection_matrix": "P_DeltaGamma_to_PPN_orbital",
            "priority": "secondary",
            "why_first": "requires gauge, source-normalization and no fitted-G shortcut guards",
            "domain": "Delta_source;Delta_lightcone;Delta_orbital_readout;Delta_projective_boundary",
            "codomain": "PPN vector;orbital_GM;Gdot_over_G;radial_acceleration",
            "matrix_ready": "false",
            "missing_for_claim": "MISSING_GAUGE;MISSING_TRACE_REVERSAL;MISSING_SOURCE_NORMALIZATION_SPLIT",
        }
    ),
    base(
        {
            "projection_id": "PMQ3081_5_projective",
            "projection_matrix": "P_projective_invariance_all_sectors",
            "priority": "guard",
            "why_first": "projective modes may be gauge, but only if every sector is invariant",
            "domain": "Delta_projective_boundary",
            "codomain": "projective_invariance_certificate;residual_if_not_invariant",
            "matrix_ready": "false",
            "missing_for_claim": "MISSING_ALL_SECTOR_PROJECTIVE_INVARIANCE;MISSING_TRACE_COUPLING_BOUND",
        }
    ),
]

score_blocker_rows = [
    base(
        {
            "blocker_id": "SBL3081_0_component_values",
            "blocks": "all arenas",
            "missing": "component numeric values or parent zero certificates",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3081_1_common_units",
            "blocks": "DeltaGamma total norm",
            "missing": "common dual-connection units and normalization across components",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3081_2_projection_matrices",
            "blocks": "observable maps",
            "missing": "P_R10, P_WEP, P_PPN, P_clock, P_lightcone, P_orbital",
            "status": "BLOCKS_SCORE",
            "score_allowed": "false",
        }
    ),
    base(
        {
            "blocker_id": "SBL3081_3_no_cancellation",
            "blocks": "combined residual pass",
            "missing": "individual component pass or parent cancellation identity",
            "status": "GUARD_ACTIVE",
            "score_allowed": "false",
        }
    ),
]

missing_artifact_rows = [
    base(
        {
            "artifact_id": "MISS3081_0_1836_skeleton",
            "expected_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1836_DELTAGAMMA_WEP_CLOCK_LIGHTCONE_PROJECTION_SKELETON.csv"),
            "exists": str((RESIDUALS / "P8_Y5_PARENT_QLOC_1836_DELTAGAMMA_WEP_CLOCK_LIGHTCONE_PROJECTION_SKELETON.csv").exists()),
            "impact": "1836 decision exists but skeleton artifact is missing; 3082 should recreate it in current chain",
            "status": "MISSING_PRIOR_ARTIFACT_NONBLOCKING",
        }
    )
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3081_0_map",
            "decision": "DeltaGamma observable map skeleton refreshed",
            "reason": "3080 components and 1835 skeleton agree on observable channels, but projection matrices remain missing",
            "consequence": "components are now routed to arenas but not scoreable",
            "next_action": "do not score any local arena yet",
        }
    ),
    base(
        {
            "decision_id": "DEC3081_1_first_projection",
            "decision": "WEP/clock/lightcone projection skeleton next",
            "reason": "these channels are most directly tied to hypermomentum, nonmetricity and matter-functor leakage",
            "consequence": "first projection block should declare domains, units and response operators without coefficients",
            "next_action": "3082-Y5-R2FR-DeltaGamma-WEP-clock-lightcone-projection-skeleton-under-AX1090.md",
        }
    ),
    base(
        {
            "decision_id": "DEC3081_2_secondary",
            "decision": "R10/PPN/orbital held secondary",
            "reason": "source/orbital maps need range scale, gauge and no fitted-G shortcuts after the first matter/readout block",
            "consequence": "R10 and PPN remain blocked but explicitly queued",
            "next_action": "hold R10/PPN/orbital skeleton until WEP/clock/lightcone block exists",
        }
    ),
]

claim_rows = [
    base(
        {
            "claim_id": "CLAIM3081_0_component_map",
            "claim": "DeltaGamma component maps are predictive",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "maps are skeletons; projection matrices and values are missing",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3081_1_local_scores",
            "claim": "R10/PPN/WEP/clock/lightcone/orbital scores can run",
            "claim_active": "false",
            "status": "NOT_CLAIMED",
            "reason": "component values, units and projection matrices are absent",
        }
    ),
    base(
        {
            "claim_id": "CLAIM3081_2_local_GR",
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
            "next_id": "NEXT3081_0_3082",
            "next_checkpoint": "3082-Y5-R2FR-DeltaGamma-WEP-clock-lightcone-projection-skeleton-under-AX1090.md",
            "script": "scripts/Y5_R2FR_DeltaGamma_WEP_clock_lightcone_projection_skeleton_under_AX1090_3082.py",
            "mission": "build the first nonclaim projection skeleton from DeltaGamma spin/material/clock/lightcone/projective components into WEP, clock and lightcone residuals",
            "starting_equation": "eta_AB, clock_residual, lightcone_residual = P_WCL * (Delta_spin, Delta_material, Delta_clock_rod, Delta_lightcone, Delta_projective)",
            "claim_policy": "declare domains, units, response operators and blockers only; no coefficients, scores or local-GR claim",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["component_map"], component_map_rows)
write_csv(OUTPUTS["arena_requirements"], arena_requirement_rows)
write_csv(OUTPUTS["projection_queue"], projection_queue_rows)
write_csv(OUTPUTS["score_blockers"], score_blocker_rows)
write_csv(OUTPUTS["missing_artifacts"], missing_artifact_rows)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["claim_status"], claim_rows)
write_csv(OUTPUTS["next"], next_rows)

copy_csv(OUTPUTS["component_map"], BRANCH_OUTPUTS["component_map_copy"])
copy_csv(OUTPUTS["arena_requirements"], BRANCH_OUTPUTS["arena_requirements_copy"])
copy_csv(OUTPUTS["projection_queue"], BRANCH_OUTPUTS["projection_queue_copy"])
copy_csv(OUTPUTS["score_blockers"], BRANCH_OUTPUTS["blockers_copy"])
copy_csv(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

branch_rows = [
    base(
        {
            "copy_id": copy_id,
            "source_path": str(source_path),
            "copy_path": str(destination_path),
            "copy_exists": str(destination_path.exists()),
            "copy_parse_ok": str(csv_ok(destination_path)),
            "status": "COPIED_NONCLAIM",
        }
    )
    for copy_id, source_path, destination_path in [
        ("BC3081_0_component_map", OUTPUTS["component_map"], BRANCH_OUTPUTS["component_map_copy"]),
        ("BC3081_1_arena_requirements", OUTPUTS["arena_requirements"], BRANCH_OUTPUTS["arena_requirements_copy"]),
        ("BC3081_2_projection_queue", OUTPUTS["projection_queue"], BRANCH_OUTPUTS["projection_queue_copy"]),
        ("BC3081_3_blockers", OUTPUTS["score_blockers"], BRANCH_OUTPUTS["blockers_copy"]),
        ("BC3081_4_next", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
]
write_csv(OUTPUTS["branches"], branch_rows)
write_csv(
    OUTPUTS["validation"],
    [
        base(
            {
                "validation_id": "VAL3081_PRE",
                "passed": "False",
                "requirement": "placeholder overwritten by final validation",
                "evidence": "generator ordering guard",
            }
        )
    ],
)
DOC.write_text("# 3081 draft\n", encoding="utf-8")

remove_pycache()
dotg_hash_after = file_hash(DOTG_TARGET)
generated_csvs = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
generated_rows = (
    component_map_rows
    + arena_requirement_rows
    + projection_queue_rows
    + score_blocker_rows
    + missing_artifact_rows
    + decision_rows
    + claim_rows
    + next_rows
)
formalization_output_count = sum(1 for output_path in generated_csvs + [DOC] if under(output_path, FORMALIZATION))
required_components = {
    "Delta_spin",
    "Delta_material_marker",
    "Delta_source",
    "Delta_clock_rod",
    "Delta_lightcone",
    "Delta_orbital_readout",
    "Delta_projective_boundary",
}
required_arenas = {"R10_short_range_inverse_square", "WEP_MICROSCOPE", "PPN", "clock_redshift", "lightcone_photon", "orbital_Newton_source_normalization"}
required_projection_ids = {"PMQ3081_0_WEP", "PMQ3081_1_clock", "PMQ3081_2_lightcone", "PMQ3081_3_R10", "PMQ3081_4_PPN_orbital", "PMQ3081_5_projective"}

validation_rows = [
    base(
        {
            "validation_id": "VAL3081_00_sources_exist",
            "passed": str(all(row["exists"] == "True" for row in source_register)),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3081_01_sources_parse",
            "passed": str(all(row["parse_ok"] == "True" for row in source_register)),
            "requirement": "all cited CSV sources parse and markdown sources exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3081_02_csv_parse",
            "passed": str(all(csv_ok(output_path) for output_path in generated_csvs)),
            "requirement": "all generated and branch-copy CSVs parse cleanly",
            "evidence": "csv.DictReader parse check",
        }
    ),
    base(
        {
            "validation_id": "VAL3081_03_components_complete",
            "passed": str(required_components.issubset({row["DeltaGamma_component"] for row in component_map_rows})),
            "requirement": "DeltaGamma observable map covers spin, material, source, clock/rod, lightcone, orbital and projective/boundary channels",
            "evidence": OUTPUTS["component_map"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3081_04_arenas_complete",
            "passed": str(required_arenas.issubset({row["arena"] for row in arena_requirement_rows})),
            "requirement": "arena projection rows cover R10, WEP, PPN, clock, lightcone and orbital",
            "evidence": OUTPUTS["arena_requirements"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3081_05_projection_queue_complete",
            "passed": str(required_projection_ids.issubset({row["projection_id"] for row in projection_queue_rows}) and not has_claim_true(projection_queue_rows)),
            "requirement": "projection matrix queue includes WEP, clock, lightcone, R10, PPN/orbital and projective guards, all nonclaim",
            "evidence": OUTPUTS["projection_queue"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3081_06_score_blockers_active",
            "passed": str(not has_claim_true(score_blocker_rows) and all(row["status"] in {"BLOCKS_SCORE", "GUARD_ACTIVE"} for row in score_blocker_rows)),
            "requirement": "score blockers remain active",
            "evidence": OUTPUTS["score_blockers"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3081_07_missing_1836_recorded",
            "passed": str(any(row["artifact_id"] == "MISS3081_0_1836_skeleton" and row["exists"] == "False" for row in missing_artifact_rows)),
            "requirement": "missing prior 1836 skeleton artifact is recorded",
            "evidence": OUTPUTS["missing_artifacts"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3081_08_no_claim_promoted",
            "passed": str(not has_claim_true(generated_rows)),
            "requirement": "no component, arena, score or local-GR claim is promoted",
            "evidence": "claim field scan",
        }
    ),
    base(
        {
            "validation_id": "VAL3081_09_next_target_selected",
            "passed": str(next_rows[0]["next_checkpoint"].startswith("3082-Y5-R2FR-DeltaGamma-WEP-clock-lightcone")),
            "requirement": "next target moves to WEP/clock/lightcone projection skeleton",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3081_10_branch_copies_exist",
            "passed": str(all(row["copy_exists"] == "True" and row["copy_parse_ok"] == "True" for row in branch_rows)),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3081_11_dotg_unchanged",
            "passed": str(dotg_hash_before == dotg_hash_after),
            "requirement": "P8_time_drift_residual_or_zero.csv is not modified",
            "evidence": f"{dotg_hash_before}->{dotg_hash_after}",
        }
    ),
    base(
        {
            "validation_id": "VAL3081_12_outputs_under_post_checkpoint",
            "passed": str(all(under(output_path, ROOT) for output_path in generated_csvs + [DOC])),
            "requirement": "all outputs are under post-checkpoint-work",
            "evidence": "path containment check",
        }
    ),
    base(
        {
            "validation_id": "VAL3081_13_no_formalization_outputs",
            "passed": str(formalization_output_count == 0),
            "requirement": "formalization-workbench modified-file count for 3081 outputs remains zero",
            "evidence": f"formalization_3081_output_paths={formalization_output_count}",
        }
    ),
    base(
        {
            "validation_id": "VAL3081_14_pycache_absent",
            "passed": str(not PYCACHE.exists()),
            "requirement": "scripts __pycache__ is absent at generator completion",
            "evidence": str(PYCACHE),
        }
    ),
    base(
        {
            "validation_id": "VAL3081_15_doc_written",
            "passed": str(DOC.exists()),
            "requirement": "checkpoint markdown document is written",
            "evidence": str(DOC),
        }
    ),
]

write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3081 - DeltaGamma Component Map to P4 Observables

Status: `Y5_R2FR_3081_component_observable_map_nonclaim_WCL_next`

Generated: `{RUN_UTC}`

## Verdict

3081 turned the `Delta_Gamma` source-current obstruction into an observable-channel map. This is not a score and not a local-GR proof. It is the routing table needed before any honest score can exist.

The useful result is that each retained component now has named observables and named projection operators: spin, material/source marker, source support, clock/rod nonmetricity, lightcone shear, orbital readout, and projective/boundary leakage.

The hard blocker is unchanged: all projection matrices are missing. There are no component values, common dual-connection units, response matrices, or source-backed arena maps. Therefore 3081 does **not** claim R10, PPN, WEP, clock, lightcone, orbital, Newtonian or local-GR success.

The next target is the first projection block: WEP/clock/lightcone. This is the best first bite because it hits the same matter-functor, spin, nonmetricity and readout leakage that blocks the GR route.

## Component Observable Map

{md_table(component_map_rows, ["map_id", "DeltaGamma_component", "connection_channel", "primary_observables", "current_status"])}

## Arena Requirements

{md_table(arena_requirement_rows, ["arena_id", "arena", "observable", "DeltaGamma_components", "current_status"])}

## Projection Matrix Queue

{md_table(projection_queue_rows, ["projection_id", "projection_matrix", "priority", "domain", "codomain", "matrix_ready"])}

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
- Component observable map: `{OUTPUTS["component_map"]}`
- Arena projection requirements: `{OUTPUTS["arena_requirements"]}`
- Projection matrix queue: `{OUTPUTS["projection_queue"]}`
- Score blockers: `{OUTPUTS["score_blockers"]}`
- Missing prior artifacts: `{OUTPUTS["missing_artifacts"]}`
- Claim status: `{OUTPUTS["claim_status"]}`
- Next target: `{OUTPUTS["next"]}`
- Validation: `{OUTPUTS["validation"]}`
- Branch copy: `{BRANCH_OUTPUTS["component_map_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["arena_requirements_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["projection_queue_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["blockers_copy"]}`
- Branch copy: `{BRANCH_OUTPUTS["next_copy"]}`
"""

DOC.write_text(doc_text, encoding="utf-8")
print(f"Wrote {DOC}")
print(f"Wrote {OUTPUTS['validation']}")
print(f"Validation passed {sum(1 for row in validation_rows if row['passed'] == 'True')}/{len(validation_rows)}")

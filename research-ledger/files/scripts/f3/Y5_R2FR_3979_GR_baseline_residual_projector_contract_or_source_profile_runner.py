from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3979"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3979-Y5-R2FR-GR-baseline-residual-projector-contract-or-source-profile-runner.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3979_SOURCE_REGISTER.csv",
    "contract": SRC / "P8_Y5_R2FR_3979_GR_BASELINE_RESIDUAL_PROJECTOR_CONTRACT.csv",
    "smoke_inputs": SRC / "P8_Y5_R2FR_3979_SOURCE_PROFILE_SMOKE_INPUTS.csv",
    "dryrun": SRC / "P8_Y5_R2FR_3979_PROJECTOR_DRYRUN_RESULTS.csv",
    "schema": SRC / "P8_Y5_R2FR_3979_PROJECTOR_READY_SCHEMA.csv",
    "bounds": SRC / "P8_Y5_R2FR_3979_PROJECTOR_BOUND_FEED_ROWS.csv",
    "feed": SRC / "P8_Y5_R2FR_3979_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3979_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3979_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3979_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3979_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3979_VALIDATION.csv",
}

NEXT_DOC = "3980-Y5-R2FR-first-real-local-source-profile-row-or-parent-zero-certificate.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3980_first_real_local_source_profile_row_or_parent_zero_certificate.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3979_00_3978_next", SRC / "P8_Y5_R2FR_3978_NEXT_TARGET.csv", "NEXT3978_0", "3978 handoff"),
        ("SRC3979_01_3978_source_zero", SRC / "P8_Y5_R2FR_3978_CLOSED_SOURCE_TENSOR_VIRIAL_THEOREM.csv", "CST3978_0_target", "source residual zero theorem"),
        ("SRC3979_02_3978_GR_guard", SRC / "P8_Y5_R2FR_3978_CLOSED_SOURCE_TENSOR_VIRIAL_THEOREM.csv", "CST3978_3_GR_multipole_guard", "GR multipole guard"),
        ("SRC3979_03_3978_broad_refusal", SRC / "P8_Y5_R2FR_3978_CLOSED_SOURCE_TENSOR_VIRIAL_THEOREM.csv", "CST3978_4_no_broad_source_zero", "broad zero refusal"),
        ("SRC3979_04_3978_certificate", SRC / "P8_Y5_R2FR_3978_CLOSED_SOURCE_TENSOR_VIRIAL_THEOREM.csv", "CST3978_5_certificate", "source zero certificate"),
        ("SRC3979_05_3978_schema_total", SRC / "P8_Y5_R2FR_3978_SOURCE_PROFILE_ACQUISITION_SCHEMA.csv", "SPS3978_04_Q_lm_total", "Q total schema"),
        ("SRC3979_06_3978_schema_GR", SRC / "P8_Y5_R2FR_3978_SOURCE_PROFILE_ACQUISITION_SCHEMA.csv", "SPS3978_05_Q_lm_GR_baseline", "GR baseline schema"),
        ("SRC3979_07_3978_schema_res", SRC / "P8_Y5_R2FR_3978_SOURCE_PROFILE_ACQUISITION_SCHEMA.csv", "SPS3978_06_Q_lm_residual", "residual schema"),
        ("SRC3979_08_3978_schema_worldtube", SRC / "P8_Y5_R2FR_3978_SOURCE_PROFILE_ACQUISITION_SCHEMA.csv", "SPS3978_09_worldtube_definition", "worldtube schema"),
        ("SRC3979_09_3978_schema_EM", SRC / "P8_Y5_R2FR_3978_SOURCE_PROFILE_ACQUISITION_SCHEMA.csv", "SPS3978_11_includes_EM", "EM inclusion schema"),
        ("SRC3979_10_3978_source_bound", SRC / "P8_Y5_R2FR_3978_SOURCE_RESIDUAL_BOUND_ROWS.csv", "SRB3978_0_source_total", "source total bound"),
        ("SRC3979_11_3978_quad_bound", SRC / "P8_Y5_R2FR_3978_SOURCE_RESIDUAL_BOUND_ROWS.csv", "SRB3978_4_quad_residual", "quadrupole residual bound"),
        ("SRC3979_12_3978_extra_bound", SRC / "P8_Y5_R2FR_3978_SOURCE_RESIDUAL_BOUND_ROWS.csv", "SRB3978_6_extra_MTS", "extra MTS residual bound"),
        ("SRC3979_13_3978_GR_cert", SRC / "P8_Y5_R2FR_3978_Z_SOURCE_ZERO_UPDATE.csv", "ZSRC3978_5_GR", "GR routing certificate"),
        ("SRC3979_14_3978_poynting_cert", SRC / "P8_Y5_R2FR_3978_Z_SOURCE_ZERO_UPDATE.csv", "ZSRC3978_4_poynting", "Poynting certificate"),
        ("SRC3979_15_3978_feed_next", SRC / "P8_Y5_R2FR_3978_FEED_UPDATE.csv", "CSF3978_5_next", "3978 next feed"),
        ("SRC3979_16_3977_GR_route", SRC / "P8_Y5_R2FR_3977_MULTIPOLE_PROFILE_DECOMPOSITION.csv", "MPD3977_3_GR_multipole_routing", "GR multipole routing decomposition"),
        ("SRC3979_17_3977_extra", SRC / "P8_Y5_R2FR_3977_MULTIPOLE_PROFILE_BOUND_ROWS.csv", "MPB3977_3_GR_baseline_route", "extra MTS bound"),
        ("SRC3979_18_3831_quad", SRC / "P8_Y5_R2FR_3831_SIGMATF_MATTER_DECOMPOSITION.csv", "SIGMATF3831_2_quadrupole_multipole", "quadrupole multipole component"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": exists,
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def contract_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "PJR3979_0_operator",
            "name": "GR baseline residual projector",
            "mathematical_form": "P_residual(Q_lm) = P_claim P_l>=1 P_same_source P_same_frame_units P_GR_baseline P_total_source [Q_lm_total - Q_lm_GR_baseline]",
            "meaning": "test extra MTS angular hair only after ordinary GR multipoles for the same source have been routed/subtracted",
            "failure_mode": "if any projector factor fails, no residual claim is allowed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "PJR3979_1_monopole",
            "name": "monopole routing",
            "mathematical_form": "l=0 rows are routed to Newton/source-calibration gates, not angular-hair tests",
            "meaning": "prevents mixing G_obs/M_obs calibration with quadrupole/higher multipole residuals",
            "failure_mode": "l=0 in this runner returns ROUTED_MONOPOLE_NOT_ANGULAR_HAIR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "PJR3979_2_same_source",
            "name": "same-source comparator",
            "mathematical_form": "source support, worldtube, frame/coframe, units, r_eval, and l,m must match between total and GR baseline",
            "meaning": "a GR baseline from a different source or frame cannot be subtracted",
            "failure_mode": "MISMATCH_SOURCE_OR_FRAME_OR_UNITS_OR_RADIUS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "PJR3979_3_total_source",
            "name": "total-source inclusion",
            "mathematical_form": "includes_matter * includes_EM * includes_binding * (includes_apparatus or apparatus_outside_projection) must hold, or finite residual rows stay active",
            "meaning": "Poynting/apparatus/binding cannot be silently dropped before the GR subtraction",
            "failure_mode": "MISSING_TOTAL_SOURCE_COMPONENT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "PJR3979_4_numeric_rule",
            "name": "numeric dry-run rule",
            "mathematical_form": "if all projector gates pass, Q_lm_residual = Q_lm_total - Q_lm_GR_baseline and epsilon_extra_MTS_l_ge_1 = |Q_lm_residual|/|M_H_ref|",
            "meaning": "creates a minimal testable operator before real profile data are loaded",
            "failure_mode": "NONNUMERIC_OR_MISSING_VALUE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "PJR3979_5_nonclaim",
            "name": "nonclaim smoke only",
            "mathematical_form": "toy dry-run rows can validate schema/operator behavior but never count as evidence",
            "meaning": "real claims require sourced profile rows or parent-signed zero certificate",
            "failure_mode": "TOY_ROW_NOT_EVIDENCE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def smoke_input_rows(timestamp: str) -> list[dict[str, Any]]:
    source_path = str(PCW / "3978-Y5-R2FR-closed-total-source-tensor-virial-poynting-inclusion-or-multipole-profile-acquisition.md")
    rows = [
        {
            "source_id": "SMK3979_0_GR_clean_toy",
            "arena": "toy_ppn_clean",
            "l": 2,
            "m": 0,
            "Q_lm_total": "1.2e-6",
            "Q_lm_GR_baseline": "1.2e-6",
            "M_H_ref": "1.0",
            "r_eval": "1.0",
            "worldtube_definition": "toy_closed_total_worldtube",
            "baseline_worldtube_definition": "toy_closed_total_worldtube",
            "units": "toy_Q_units",
            "baseline_units": "toy_Q_units",
            "frame_or_coframe": "toy_local_orthonormal",
            "baseline_frame_or_coframe": "toy_local_orthonormal",
            "includes_matter": True,
            "includes_EM": True,
            "includes_binding": True,
            "includes_apparatus": True,
            "apparatus_outside_projection": False,
            "GR_routing_flag": True,
            "boundary_flux_TF": "0.0",
            "d2I_TF_dt2": "0.0",
            "poynting_bound": "0.0",
            "source_path": source_path,
            "row_kind": "TOY_OPERATOR_SMOKE_NOT_EVIDENCE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "source_id": "SMK3979_1_extra_MTS_toy",
            "arena": "toy_ppn_extra_hair",
            "l": 2,
            "m": 1,
            "Q_lm_total": "1.5e-6",
            "Q_lm_GR_baseline": "1.2e-6",
            "M_H_ref": "1.0",
            "r_eval": "1.0",
            "worldtube_definition": "toy_closed_total_worldtube",
            "baseline_worldtube_definition": "toy_closed_total_worldtube",
            "units": "toy_Q_units",
            "baseline_units": "toy_Q_units",
            "frame_or_coframe": "toy_local_orthonormal",
            "baseline_frame_or_coframe": "toy_local_orthonormal",
            "includes_matter": True,
            "includes_EM": True,
            "includes_binding": True,
            "includes_apparatus": True,
            "apparatus_outside_projection": False,
            "GR_routing_flag": True,
            "boundary_flux_TF": "0.0",
            "d2I_TF_dt2": "0.0",
            "poynting_bound": "0.0",
            "source_path": source_path,
            "row_kind": "TOY_OPERATOR_SMOKE_NOT_EVIDENCE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "source_id": "SMK3979_2_missing_GR_baseline",
            "arena": "toy_missing_baseline",
            "l": 2,
            "m": 0,
            "Q_lm_total": "1.0e-6",
            "Q_lm_GR_baseline": "",
            "M_H_ref": "1.0",
            "r_eval": "1.0",
            "worldtube_definition": "toy_closed_total_worldtube",
            "baseline_worldtube_definition": "toy_closed_total_worldtube",
            "units": "toy_Q_units",
            "baseline_units": "toy_Q_units",
            "frame_or_coframe": "toy_local_orthonormal",
            "baseline_frame_or_coframe": "toy_local_orthonormal",
            "includes_matter": True,
            "includes_EM": True,
            "includes_binding": True,
            "includes_apparatus": True,
            "apparatus_outside_projection": False,
            "GR_routing_flag": False,
            "boundary_flux_TF": "0.0",
            "d2I_TF_dt2": "0.0",
            "poynting_bound": "0.0",
            "source_path": source_path,
            "row_kind": "NEGATIVE_SMOKE_EXPECT_BLOCK",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "source_id": "SMK3979_3_frame_mismatch",
            "arena": "toy_frame_mismatch",
            "l": 3,
            "m": 1,
            "Q_lm_total": "2.0e-6",
            "Q_lm_GR_baseline": "2.0e-6",
            "M_H_ref": "1.0",
            "r_eval": "1.0",
            "worldtube_definition": "toy_closed_total_worldtube",
            "baseline_worldtube_definition": "toy_closed_total_worldtube",
            "units": "toy_Q_units",
            "baseline_units": "toy_Q_units",
            "frame_or_coframe": "toy_local_orthonormal",
            "baseline_frame_or_coframe": "toy_rotated_frame",
            "includes_matter": True,
            "includes_EM": True,
            "includes_binding": True,
            "includes_apparatus": True,
            "apparatus_outside_projection": False,
            "GR_routing_flag": True,
            "boundary_flux_TF": "0.0",
            "d2I_TF_dt2": "0.0",
            "poynting_bound": "0.0",
            "source_path": source_path,
            "row_kind": "NEGATIVE_SMOKE_EXPECT_BLOCK",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "source_id": "SMK3979_4_poynting_missing",
            "arena": "toy_missing_poynting",
            "l": 2,
            "m": -1,
            "Q_lm_total": "1.2e-6",
            "Q_lm_GR_baseline": "1.2e-6",
            "M_H_ref": "1.0",
            "r_eval": "1.0",
            "worldtube_definition": "toy_closed_total_worldtube",
            "baseline_worldtube_definition": "toy_closed_total_worldtube",
            "units": "toy_Q_units",
            "baseline_units": "toy_Q_units",
            "frame_or_coframe": "toy_local_orthonormal",
            "baseline_frame_or_coframe": "toy_local_orthonormal",
            "includes_matter": True,
            "includes_EM": False,
            "includes_binding": True,
            "includes_apparatus": True,
            "apparatus_outside_projection": False,
            "GR_routing_flag": True,
            "boundary_flux_TF": "0.0",
            "d2I_TF_dt2": "0.0",
            "poynting_bound": "",
            "source_path": source_path,
            "row_kind": "NEGATIVE_SMOKE_EXPECT_BLOCK",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "source_id": "SMK3979_5_monopole_routed",
            "arena": "toy_monopole",
            "l": 0,
            "m": 0,
            "Q_lm_total": "2.0",
            "Q_lm_GR_baseline": "1.9",
            "M_H_ref": "1.0",
            "r_eval": "1.0",
            "worldtube_definition": "toy_closed_total_worldtube",
            "baseline_worldtube_definition": "toy_closed_total_worldtube",
            "units": "toy_Q_units",
            "baseline_units": "toy_Q_units",
            "frame_or_coframe": "toy_local_orthonormal",
            "baseline_frame_or_coframe": "toy_local_orthonormal",
            "includes_matter": True,
            "includes_EM": True,
            "includes_binding": True,
            "includes_apparatus": True,
            "apparatus_outside_projection": False,
            "GR_routing_flag": True,
            "boundary_flux_TF": "0.0",
            "d2I_TF_dt2": "0.0",
            "poynting_bound": "0.0",
            "source_path": source_path,
            "row_kind": "ROUTING_SMOKE_NOT_ANGULAR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]
    return rows


def project_row(row: dict[str, Any], timestamp: str) -> dict[str, Any]:
    blockers: list[str] = []
    l_value = int(row["l"])
    q_total = parse_float(row["Q_lm_total"])
    q_gr = parse_float(row["Q_lm_GR_baseline"])
    m_ref = parse_float(row["M_H_ref"])
    source_path = Path(str(row["source_path"]))

    if l_value < 1:
        return {
            "source_id": row["source_id"],
            "projector_status": "ROUTED_MONOPOLE_NOT_ANGULAR_HAIR",
            "Q_lm_residual": "",
            "epsilon_extra_MTS_l_ge_1": "0.0",
            "blockers": "l=0 routed to Newton/source-calibration gates",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }

    if q_total is None:
        blockers.append("MISSING_Q_LM_TOTAL")
    if q_gr is None:
        blockers.append("MISSING_Q_LM_GR_BASELINE")
    if m_ref is None or m_ref == 0:
        blockers.append("MISSING_OR_ZERO_M_H_REF")
    if not parse_bool(row["GR_routing_flag"]):
        blockers.append("GR_ROUTING_FLAG_FALSE")
    if row["worldtube_definition"] != row["baseline_worldtube_definition"]:
        blockers.append("MISMATCH_WORLDTUBE")
    if row["units"] != row["baseline_units"]:
        blockers.append("MISMATCH_UNITS")
    if row["frame_or_coframe"] != row["baseline_frame_or_coframe"]:
        blockers.append("MISMATCH_FRAME_OR_COFRAME")
    if not source_path.exists():
        blockers.append("MISSING_SOURCE_PATH")
    if not parse_bool(row["includes_matter"]):
        blockers.append("MISSING_MATTER_COMPONENT")
    if not parse_bool(row["includes_binding"]):
        blockers.append("MISSING_BINDING_COMPONENT")
    if not (parse_bool(row["includes_apparatus"]) or parse_bool(row["apparatus_outside_projection"])):
        blockers.append("MISSING_APPARATUS_OR_PROJECTION_EXCLUSION")
    if not parse_bool(row["includes_EM"]) and parse_float(row["poynting_bound"]) is None:
        blockers.append("MISSING_EM_OR_POYNTING_BOUND")

    if blockers:
        return {
            "source_id": row["source_id"],
            "projector_status": "BLOCKED_" + "+".join(blockers),
            "Q_lm_residual": "",
            "epsilon_extra_MTS_l_ge_1": "",
            "blockers": "|".join(blockers),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }

    assert q_total is not None
    assert q_gr is not None
    assert m_ref is not None
    residual = q_total - q_gr
    epsilon = abs(residual) / abs(m_ref)
    status = "PROJECTOR_PASS_ZERO_RESIDUAL_TOY" if epsilon == 0 else "PROJECTOR_PASS_NONZERO_RESIDUAL_TOY"
    return {
        "source_id": row["source_id"],
        "projector_status": status,
        "Q_lm_residual": f"{residual:.12g}",
        "epsilon_extra_MTS_l_ge_1": f"{epsilon:.12g}",
        "blockers": "TOY_ROW_NOT_EVIDENCE",
        "claim_allowed": False,
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
    }


def dryrun_rows(inputs: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    return [project_row(row, timestamp) for row in inputs]


def schema_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "schema_id": "PRS3979_0_required_inputs",
            "object": "source_profile_row",
            "required_fields": "source_id,arena,l,m,Q_lm_total,Q_lm_GR_baseline,M_H_ref,r_eval,worldtube_definition,baseline_worldtube_definition,units,baseline_units,frame_or_coframe,baseline_frame_or_coframe,includes_matter,includes_EM,includes_binding,includes_apparatus,apparatus_outside_projection,GR_routing_flag,source_path",
            "pass_rule": "all required fields populated and compatible",
            "failure_rule": "missing/false/mismatched fields block residual claim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "schema_id": "PRS3979_1_output",
            "object": "projector_result_row",
            "required_fields": "source_id,projector_status,Q_lm_residual,epsilon_extra_MTS_l_ge_1,blockers,claim_allowed,valid_for_claim",
            "pass_rule": "residual and epsilon computed only when projector gates pass",
            "failure_rule": "blocked rows must carry explicit blockers and blank residual value",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "schema_id": "PRS3979_2_claim_promotion",
            "object": "future_real_profile_claim",
            "required_fields": "non-toy source_path, sourced Q_lm_total, sourced Q_lm_GR_baseline, real M_H_ref, units/frame proof, total-source inclusion proof, Poynting inclusion/bound",
            "pass_rule": "valid_for_claim can become true only after all fields are real and projector_status passes",
            "failure_rule": "toy rows and symbolic placeholders remain valid_for_claim=false",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "PBF3979_0_projector",
            "symbol": "epsilon_extra_MTS_l_ge_1",
            "formula": "epsilon_extra_MTS_l_ge_1 = |P_residual(Q_lm_total-Q_lm_GR_baseline)|/|M_H_ref|",
            "units": "dimensionless",
            "required_input_or_theorem": "projector pass with sourced same-source GR baseline and total-source inclusion",
            "feeds_or_blocks": "SRB3978_6_extra_MTS",
            "current_status": "DRYRUN_OPERATOR_READY_REAL_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PBF3979_1_quad",
            "symbol": "epsilon_quad_residual_TF",
            "formula": "epsilon_quad_residual_TF = C_Q |Q_TF_total-Q_TF_GR_baseline|/(M r^2)",
            "units": "dimensionless",
            "required_input_or_theorem": "same-source GR quadrupole comparator",
            "feeds_or_blocks": "SRB3978_4_quad_residual",
            "current_status": "PROJECTOR_CONTRACT_READY_CQ_AND_REAL_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "PBF3979_2_source",
            "symbol": "epsilon_source_l_ge_1",
            "formula": "epsilon_source_l_ge_1 <= epsilon_closed_source_failure + epsilon_tensor_virial_TF + epsilon_quad_residual_TF + epsilon_EM_Poynting_TF + epsilon_apparatus_TF",
            "units": "dimensionless",
            "required_input_or_theorem": "3978 source residual components plus projector output",
            "feeds_or_blocks": "Delta_PPN_source_abs and Z_SO3_boundary",
            "current_status": "BOUND_CHAIN_READY_REAL_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "feed_id": "PRF3979_0_GR_route",
            "target": "Z_GR_multipole_routing",
            "update": "defined as a dry-runnable projector with same-source/frame/units/worldtube gates",
            "effect": "ordinary GR multipoles can now be separated from extra MTS residual hair mechanically",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "PRF3979_1_extra",
            "target": "epsilon_extra_MTS_l_ge_1",
            "update": "computed in toy dry-run as |Q_total-Q_GR|/|M_H_ref| when gates pass",
            "effect": "first nonclaim residual operator smoke pass exists",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "PRF3979_2_source",
            "target": "epsilon_source_l_ge_1",
            "update": "projector output feeds 3978 source residual bound chain",
            "effect": "source angular residual can now be moved from prose to runner rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "PRF3979_3_PPN",
            "target": "Delta_PPN_source_abs",
            "update": "extra MTS multipole hair enters PPN residual only after GR baseline subtraction",
            "effect": "fair comparator rule is enforced before PPN penalty",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "PRF3979_4_next",
            "target": "first_real_local_source_profile_row",
            "update": f"move to {NEXT_DOC}",
            "effect": "replace toy smoke rows with the first real or theorem-zero local source profile row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3979_0_projector",
            "decision": "define P_residual explicitly",
            "status": "PROJECTOR_CONTRACT_READY",
            "reason": "fair comparison requires subtracting same-source GR baseline before judging extra MTS hair",
            "next_action": "load real source profile rows or theorem-zero certificate",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3979_1_smoke",
            "decision": "run nonclaim toy smoke rows",
            "status": "DRYRUN_PASS_AND_BLOCKS_WORK",
            "reason": "operator computes zero/nonzero residuals and blocks missing baseline, frame mismatch, and missing Poynting inclusion",
            "next_action": "promote only with real sourced rows",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3979_2_monopole",
            "decision": "route l=0 away from angular hair",
            "status": "MONOPOLE_ROUTED_TO_SOURCE_CALIBRATION",
            "reason": "Newton/G_obs/M_obs calibration must not be mixed with l>=1 angular residuals",
            "next_action": "keep l=0 in source-coupling/Newtonian branch",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3979_3_next",
            "decision": "next target selected",
            "status": "MOVE_TO_FIRST_REAL_PROFILE_OR_PARENT_ZERO",
            "reason": "the projector exists; the next progress must be a real local source row or a stronger parent zero certificate",
            "next_action": NEXT_DOC,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3979_0_projector",
            "gate": "projector claim promotion",
            "requirement": "non-toy source rows with sourced Q_lm_total, Q_lm_GR_baseline, M_H_ref, same frame/units/worldtube, and total-source/Poynting inclusion",
            "status": "BLOCKED_TOY_ROWS_ONLY",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3979_1_GR",
            "gate": "GR baseline",
            "requirement": "same-source GR comparator exists for every l,m row being tested",
            "status": "BLOCKED_REAL_BASELINE_ROWS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3979_2_poynting",
            "gate": "Poynting/total source",
            "requirement": "EM/Poynting included in total source or finite sourced Poynting residual bound",
            "status": "BLOCKED_REAL_POYNTING_ROWS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3979_3_local_GR",
            "gate": "local GR",
            "requirement": "projector plus real source/boundary/external residual rows and PPN gates",
            "status": "LOCAL_GR_STILL_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3979_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "replace toy projector rows with a first real local source profile row, or derive a parent zero certificate for that row",
            "success_condition": "one local source profile row is real/source-backed or theorem-zero, and the projector produces a nonclaim but non-toy residual result",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, sources: list[dict[str, Any]], dryrun: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    pass_rows = sum(str(row["projector_status"]).startswith("PROJECTOR_PASS") for row in dryrun)
    blocked_rows = sum(str(row["projector_status"]).startswith("BLOCKED") for row in dryrun)
    routed_rows = sum(str(row["projector_status"]).startswith("ROUTED") for row in dryrun)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "GR_BASELINE_RESIDUAL_PROJECTOR_DRYRUN_READY_NONCLAIM",
            "sources_found": found,
            "sources_total": len(sources),
            "dryrun_pass_rows": pass_rows,
            "dryrun_blocked_rows": blocked_rows,
            "dryrun_routed_rows": routed_rows,
            "main_result": "P_residual now subtracts same-source GR baseline from total multipoles, blocks missing/mismatched/Poynting-incomplete rows, routes l=0 away from angular hair, and computes toy epsilon_extra_MTS_l_ge_1 rows without claim promotion",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, sources: list[dict[str, Any]], dryrun: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    pass_rows = sum(str(row["projector_status"]).startswith("PROJECTOR_PASS") for row in dryrun)
    blocked_rows = sum(str(row["projector_status"]).startswith("BLOCKED") for row in dryrun)
    routed_rows = sum(str(row["projector_status"]).startswith("ROUTED") for row in dryrun)
    return f"""# 3979 - GR Baseline Residual Projector Contract Or Source Profile Runner

Timestamp: `{timestamp}`

## Result

3979 turns the fair-comparison rule into an operator:

```text
P_residual(Q_lm) =
  P_claim
  P_l>=1
  P_same_source
  P_same_frame_units
  P_GR_baseline
  P_total_source
  [Q_lm_total - Q_lm_GR_baseline]
```

If all gates pass:

```text
Q_lm_residual = Q_lm_total - Q_lm_GR_baseline
epsilon_extra_MTS_l_ge_1 = |Q_lm_residual| / |M_H_ref|
```

## Dry-Run

Toy smoke rows were generated to prove operator behavior only:

```text
pass rows: {pass_rows}
blocked rows: {blocked_rows}
routed l=0 rows: {routed_rows}
```

The runner blocks missing GR baselines, frame/coframe mismatches, and missing EM/Poynting inclusion. It also routes `l=0` to the Newton/source-calibration branch instead of angular hair.

## Claim Status

No claim is made. These are toy rows, not evidence.

Real promotion requires non-toy source rows with:

```text
Q_lm_total, Q_lm_GR_baseline, M_H_ref,
same source/worldtube/frame/units/r_eval,
total-source inclusion,
Poynting included or bounded,
source path and units.
```

Next target:

```text
{NEXT_DOC}
```

Source needles found: `{found}/{len(sources)}`.
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3979 - GR Baseline Residual Projector

- Timestamp: `{timestamp}`
- Status: `GR_BASELINE_RESIDUAL_PROJECTOR_DRYRUN_READY_NONCLAIM`
- Operator:
  `P_residual(Q_lm)=P_claim P_l>=1 P_same_source P_same_frame_units P_GR_baseline P_total_source [Q_lm_total-Q_lm_GR_baseline]`.
- Dry-run behavior:
  computes `epsilon_extra_MTS_l_ge_1=|Q_lm_residual|/|M_H_ref|` for passing toy rows, blocks missing baseline/frame mismatch/Poynting-incomplete rows, and routes `l=0` to source calibration.
- Claim status:
  nonclaim; toy rows validate operator behavior only.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3979 - GR Baseline Residual Projector"
    block = spine_block(timestamp)
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def all_rows(timestamp: str) -> dict[str, list[dict[str, Any]]]:
    sources = source_register_rows(timestamp)
    smoke_inputs = smoke_input_rows(timestamp)
    dryrun = dryrun_rows(smoke_inputs, timestamp)
    return {
        "sources": sources,
        "contract": contract_rows(timestamp),
        "smoke_inputs": smoke_inputs,
        "dryrun": dryrun,
        "schema": schema_rows(timestamp),
        "bounds": bound_rows(timestamp),
        "feed": feed_rows(timestamp),
        "decision": decision_rows(timestamp),
        "claim_gate": claim_gate_rows(timestamp),
        "next": next_rows(timestamp),
        "status": status_rows(timestamp, sources, dryrun),
    }


def validation_rows(timestamp: str, rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = rows["sources"]
    contract = rows["contract"]
    smoke_inputs = rows["smoke_inputs"]
    dryrun = rows["dryrun"]
    schema = rows["schema"]
    bounds = rows["bounds"]
    feed = rows["feed"]
    decisions = rows["decision"]
    claims = rows["claim_gate"]
    next_target = rows["next"]

    def val(validation_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": timestamp,
        }

    parsed = True
    parse_detail = "generated CSV files parse cleanly"
    for path in generated_csvs:
        try:
            read_csv(path)
        except Exception as exc:
            parsed = False
            parse_detail = f"{path} failed to parse: {exc}"
            break

    contract_ids = {row["contract_id"] for row in contract}
    input_ids = {row["source_id"] for row in smoke_inputs}
    dry_statuses = {row["projector_status"] for row in dryrun}
    dry_by_id = {row["source_id"]: row for row in dryrun}
    schema_objects = {row["object"] for row in schema}
    bound_symbols = {row["symbol"] for row in bounds}
    feed_targets = {row["target"] for row in feed}
    decision_statuses = {row["status"] for row in decisions}
    claim_statuses = {row["status"] for row in claims}

    return [
        val("VAL3979_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3979_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3979_02_contract", {"PJR3979_0_operator", "PJR3979_1_monopole", "PJR3979_2_same_source", "PJR3979_3_total_source", "PJR3979_4_numeric_rule", "PJR3979_5_nonclaim"} <= contract_ids, "projector operator, routing, compatibility, total-source, numeric, and nonclaim clauses present"),
        val("VAL3979_03_inputs", {"SMK3979_0_GR_clean_toy", "SMK3979_1_extra_MTS_toy", "SMK3979_2_missing_GR_baseline", "SMK3979_3_frame_mismatch", "SMK3979_4_poynting_missing", "SMK3979_5_monopole_routed"} <= input_ids, "toy smoke inputs include pass, residual, blocked, and routed cases"),
        val("VAL3979_04_zero_pass", dry_by_id["SMK3979_0_GR_clean_toy"]["projector_status"] == "PROJECTOR_PASS_ZERO_RESIDUAL_TOY" and dry_by_id["SMK3979_0_GR_clean_toy"]["epsilon_extra_MTS_l_ge_1"] == "0", "GR-clean toy row projects to zero residual"),
        val("VAL3979_05_nonzero_pass", dry_by_id["SMK3979_1_extra_MTS_toy"]["projector_status"] == "PROJECTOR_PASS_NONZERO_RESIDUAL_TOY" and parse_float(dry_by_id["SMK3979_1_extra_MTS_toy"]["epsilon_extra_MTS_l_ge_1"]) is not None and parse_float(dry_by_id["SMK3979_1_extra_MTS_toy"]["epsilon_extra_MTS_l_ge_1"]) > 0, "extra-hair toy row projects to nonzero residual"),
        val("VAL3979_06_missing_baseline_blocks", "MISSING_Q_LM_GR_BASELINE" in dry_by_id["SMK3979_2_missing_GR_baseline"]["blockers"], "missing GR baseline blocks"),
        val("VAL3979_07_frame_mismatch_blocks", "MISMATCH_FRAME_OR_COFRAME" in dry_by_id["SMK3979_3_frame_mismatch"]["blockers"], "frame mismatch blocks"),
        val("VAL3979_08_poynting_blocks", "MISSING_EM_OR_POYNTING_BOUND" in dry_by_id["SMK3979_4_poynting_missing"]["blockers"], "missing EM/Poynting inclusion blocks"),
        val("VAL3979_09_monopole_routes", dry_by_id["SMK3979_5_monopole_routed"]["projector_status"] == "ROUTED_MONOPOLE_NOT_ANGULAR_HAIR", "l=0 routes to source-calibration branch"),
        val("VAL3979_10_schema", {"source_profile_row", "projector_result_row", "future_real_profile_claim"} <= schema_objects, "projector-ready schemas present"),
        val("VAL3979_11_bounds", {"epsilon_extra_MTS_l_ge_1", "epsilon_quad_residual_TF", "epsilon_source_l_ge_1"} <= bound_symbols, "projector bound feed rows present"),
        val("VAL3979_12_feed", {"Z_GR_multipole_routing", "epsilon_extra_MTS_l_ge_1", "epsilon_source_l_ge_1", "Delta_PPN_source_abs", "first_real_local_source_profile_row"} <= feed_targets, "feeds reach GR routing, source residual, PPN, and next real row"),
        val("VAL3979_13_decision", {"PROJECTOR_CONTRACT_READY", "DRYRUN_PASS_AND_BLOCKS_WORK", "MONOPOLE_ROUTED_TO_SOURCE_CALIBRATION", "MOVE_TO_FIRST_REAL_PROFILE_OR_PARENT_ZERO"} <= decision_statuses, "decision gate records projector, dry-run, monopole route, and next real-row move"),
        val("VAL3979_14_claim_gate", {"BLOCKED_TOY_ROWS_ONLY", "BLOCKED_REAL_BASELINE_ROWS_MISSING", "BLOCKED_REAL_POYNTING_ROWS_MISSING", "LOCAL_GR_STILL_OPEN"} <= claim_statuses, "claim gates block toy, baseline, Poynting, and local GR promotion"),
        val("VAL3979_15_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to first real local source profile row or parent zero certificate"),
        val("VAL3979_16_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3979_17_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3979_18_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3979_19_spine_updated", SPINE_PATH.exists() and "3979 - GR Baseline Residual Projector" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3979_20_csv_parse", parsed, parse_detail),
        val("VAL3979_21_script_compile", True, "script compiled before validation write"),
        val("VAL3979_22_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
        val("VAL3979_23_statuses", {"PROJECTOR_PASS_ZERO_RESIDUAL_TOY", "PROJECTOR_PASS_NONZERO_RESIDUAL_TOY", "ROUTED_MONOPOLE_NOT_ANGULAR_HAIR"} <= dry_statuses, "dry-run statuses include zero pass, nonzero pass, and monopole route"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["contract"], rows["contract"])
    write_csv(OUTPUTS["smoke_inputs"], rows["smoke_inputs"])
    write_csv(OUTPUTS["dryrun"], rows["dryrun"])
    write_csv(OUTPUTS["schema"], rows["schema"])
    write_csv(OUTPUTS["bounds"], rows["bounds"])
    write_csv(OUTPUTS["feed"], rows["feed"])
    write_csv(OUTPUTS["decision"], rows["decision"])
    write_csv(OUTPUTS["claim_gate"], rows["claim_gate"])
    write_csv(OUTPUTS["next"], rows["next"])
    write_csv(OUTPUTS["status"], rows["status"])

    DOC_PATH.write_text(doc_text(timestamp, rows["sources"], rows["dryrun"]), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, rows)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"3979 validation failed: {failed}")

    print(f"3979 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("GR-baseline residual projector contract and nonclaim dry-run assembled")


if __name__ == "__main__":
    run()

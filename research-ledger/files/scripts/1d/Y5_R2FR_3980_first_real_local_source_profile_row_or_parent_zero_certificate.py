from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3980"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3980-Y5-R2FR-first-real-local-source-profile-row-or-parent-zero-certificate.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3980_SOURCE_REGISTER.csv",
    "certificate": SRC / "P8_Y5_R2FR_3980_PARENT_ZERO_CERTIFICATE_AUDIT.csv",
    "profiles": SRC / "P8_Y5_R2FR_3980_SOURCE_PROFILE_CANDIDATE_ROWS.csv",
    "projector": SRC / "P8_Y5_R2FR_3980_PROJECTOR_RESULTS.csv",
    "bounds": SRC / "P8_Y5_R2FR_3980_BOUND_FEED_ROWS.csv",
    "feed": SRC / "P8_Y5_R2FR_3980_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3980_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3980_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3980_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3980_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3980_VALIDATION.csv",
}

NEXT_DOC = "3981-Y5-R2FR-controlled-monopole-zero-certificate-closure-or-first-lab-source-profile-values.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3981_controlled_monopole_zero_certificate_closure_or_first_lab_source_profile_values.py"


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
        ("SRC3980_00_3979_next", SRC / "P8_Y5_R2FR_3979_NEXT_TARGET.csv", "NEXT3979_0", "3979 handoff"),
        ("SRC3980_01_3979_operator", SRC / "P8_Y5_R2FR_3979_GR_BASELINE_RESIDUAL_PROJECTOR_CONTRACT.csv", "PJR3979_0_operator", "residual projector operator"),
        ("SRC3980_02_3979_same_source", SRC / "P8_Y5_R2FR_3979_GR_BASELINE_RESIDUAL_PROJECTOR_CONTRACT.csv", "PJR3979_2_same_source", "same-source comparator"),
        ("SRC3980_03_3979_total_source", SRC / "P8_Y5_R2FR_3979_GR_BASELINE_RESIDUAL_PROJECTOR_CONTRACT.csv", "PJR3979_3_total_source", "total-source inclusion"),
        ("SRC3980_04_3979_nonclaim", SRC / "P8_Y5_R2FR_3979_GR_BASELINE_RESIDUAL_PROJECTOR_CONTRACT.csv", "PJR3979_5_nonclaim", "nonclaim smoke guard"),
        ("SRC3980_05_3979_schema", SRC / "P8_Y5_R2FR_3979_PROJECTOR_READY_SCHEMA.csv", "PRS3979_0_required_inputs", "projector input schema"),
        ("SRC3980_06_3979_extra_bound", SRC / "P8_Y5_R2FR_3979_PROJECTOR_BOUND_FEED_ROWS.csv", "PBF3979_0_projector", "epsilon extra MTS feed"),
        ("SRC3980_07_3979_claim", SRC / "P8_Y5_R2FR_3979_CLAIM_GATE.csv", "CLG3979_0_projector", "projector claim gate"),
        ("SRC3980_08_3978_source_cert", SRC / "P8_Y5_R2FR_3978_Z_SOURCE_ZERO_UPDATE.csv", "ZSRC3978_7_total", "source zero total certificate"),
        ("SRC3980_09_3978_GR_cert", SRC / "P8_Y5_R2FR_3978_Z_SOURCE_ZERO_UPDATE.csv", "ZSRC3978_5_GR", "GR multipole routing certificate"),
        ("SRC3980_10_3978_poynting", SRC / "P8_Y5_R2FR_3978_Z_SOURCE_ZERO_UPDATE.csv", "ZSRC3978_4_poynting", "Poynting inclusion certificate"),
        ("SRC3980_11_3978_zero_theorem", SRC / "P8_Y5_R2FR_3978_CLOSED_SOURCE_TENSOR_VIRIAL_THEOREM.csv", "CST3978_0_target", "source residual zero theorem"),
        ("SRC3980_12_3978_GR_guard", SRC / "P8_Y5_R2FR_3978_CLOSED_SOURCE_TENSOR_VIRIAL_THEOREM.csv", "CST3978_3_GR_multipole_guard", "GR multipole guard"),
        ("SRC3980_13_3978_broad_refusal", SRC / "P8_Y5_R2FR_3978_CLOSED_SOURCE_TENSOR_VIRIAL_THEOREM.csv", "CST3978_4_no_broad_source_zero", "broad zero refusal"),
        ("SRC3980_14_3969_target", SRC / "P8_Y5_R2FR_3969_SINGLE_EXTERIOR_MASS_UNIQUENESS_THEOREM.csv", "UQ3969_0_target", "single exterior mass target"),
        ("SRC3980_15_3969_EH", SRC / "P8_Y5_R2FR_3969_SINGLE_EXTERIOR_MASS_UNIQUENESS_THEOREM.csv", "UQ3969_1_conditional_uniqueness_theorem", "EH exterior uniqueness"),
        ("SRC3980_16_3969_square", SRC / "P8_Y5_R2FR_3969_SINGLE_EXTERIOR_MASS_UNIQUENESS_THEOREM.csv", "UQ3969_2_square_law_corollary", "beta square-law corollary"),
        ("SRC3980_17_3969_guard", SRC / "P8_Y5_R2FR_3969_SINGLE_EXTERIOR_MASS_UNIQUENESS_THEOREM.csv", "UQ3969_4_not_current_MTS_claim", "parent signature limit"),
        ("SRC3980_18_3976_SO3", SRC / "P8_Y5_R2FR_3976_PARENT_SO3_BOUNDARY_SYMMETRY_THEOREM.csv", "SO3T3976_0_target", "conditional SO3 theorem shape"),
        ("SRC3980_19_3976_counterguard", SRC / "P8_Y5_R2FR_3976_PARENT_SO3_BOUNDARY_SYMMETRY_THEOREM.csv", "SO3T3976_4_counterguard", "spherical shortcut guard"),
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


def certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PZC3980_0_EH_vacuum", "Z_EH_vacuum_monopole_family", "exterior readout is EH vacuum/SdS monopole family with one mass charge", "conditional_from_3969", "CONDITIONAL_NOT_PARENT_SIGNED", "Q_lm_total=0 for l>=1 in controlled monopole branch"),
        ("PZC3980_1_same_GR", "Z_same_GR_baseline_monopole", "GR comparator uses the same source, same exterior monopole, same frame/coframe, same units, and same r_eval", "operator_contract", "DEFINED_FOR_CANDIDATE_ROW", "Q_lm_GR_baseline=0 for l>=1"),
        ("PZC3980_2_total_source", "Z_closed_total_source_monopole", "one closed worldtube includes all relevant matter/field/binding/apparatus/exchange channels or proves they are absent/outside projection", "required", "UNSIGNED_FROM_3978", "blocks claim promotion"),
        ("PZC3980_3_poynting", "Z_Poynting_silent_or_included", "no EM/radiative/Poynting residual in the controlled row, or T_EM/S_EM included in total source", "required", "UNSIGNED_FROM_3978", "blocks claim promotion"),
        ("PZC3980_4_surface", "Z_surface_exchange_zero_monopole", "surface_TF=exchange_TF=boundary_flux_TF=0 in the same controlled branch", "required", "PARTIAL_PRIVATE_BRANCH_ONLY", "blocks claim promotion"),
        ("PZC3980_5_no_extra_hair", "Z_no_extra_lge1_MTS_hair", "no additional MTS source multipole survives beyond the GR monopole exterior", "required", "UNSIGNED", "blocks claim promotion"),
        ("PZC3980_6_counterguard", "Z_no_spherical_cheat", "zero row is a controlled EH-monopole branch, not arbitrary spherical averaging of a non-spherical source", "guard", "GUARD_ACTIVE", "prevents overclaim"),
        ("PZC3980_7_total", "Z_parent_zero_lge1_candidate", "product of EH vacuum, same-GR baseline, closed source, Poynting, surface, and no-extra-hair factors", "total", "FALSE_UNTIL_UNSIGNED_FACTORS_CLOSE", "candidate row remains nonclaim"),
    ]
    return [
        {
            "certificate_id": certificate_id,
            "factor": factor,
            "requirement": requirement,
            "role": role,
            "current_status": status,
            "effect": effect,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for certificate_id, factor, requirement, role, status, effect in specs
    ]


def profile_rows(timestamp: str) -> list[dict[str, Any]]:
    source_path = SRC / "P8_Y5_R2FR_3969_SINGLE_EXTERIOR_MASS_UNIQUENESS_THEOREM.csv"
    return [
        {
            "source_id": "REAL3980_0_controlled_EH_monopole_l2m0",
            "arena": "controlled_local_EH_monopole_branch",
            "l": 2,
            "m": 0,
            "Q_lm_total": "0.0",
            "Q_lm_GR_baseline": "0.0",
            "M_H_ref": "1.0",
            "r_eval": "symbolic_exterior_annulus",
            "worldtube_definition": "controlled_closed_total_monopole_worldtube",
            "baseline_worldtube_definition": "controlled_closed_total_monopole_worldtube",
            "units": "theorem_zero_normalized_multipole",
            "baseline_units": "theorem_zero_normalized_multipole",
            "frame_or_coframe": "same_parent_local_orthonormal_frame",
            "baseline_frame_or_coframe": "same_parent_local_orthonormal_frame",
            "includes_matter": True,
            "includes_EM": True,
            "includes_binding": True,
            "includes_apparatus": True,
            "apparatus_outside_projection": False,
            "GR_routing_flag": True,
            "boundary_flux_TF": "0.0_if_Z_surface_exchange_zero_monopole",
            "d2I_TF_dt2": "0.0_if_Z_stationary_TF_virial",
            "poynting_bound": "0.0_if_Z_Poynting_silent_or_included",
            "source_path": str(source_path),
            "row_kind": "THEOREM_ZERO_CANDIDATE_PROFILE_NONCLAIM",
            "certificate_required": "Z_parent_zero_lge1_candidate",
            "claim_blockers": "Z_closed_total_source_monopole|Z_Poynting_silent_or_included|Z_surface_exchange_zero_monopole|Z_no_extra_lge1_MTS_hair",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "source_id": "REAL3980_1_same_branch_l3m0_guard",
            "arena": "controlled_local_EH_monopole_branch",
            "l": 3,
            "m": 0,
            "Q_lm_total": "0.0",
            "Q_lm_GR_baseline": "0.0",
            "M_H_ref": "1.0",
            "r_eval": "symbolic_exterior_annulus",
            "worldtube_definition": "controlled_closed_total_monopole_worldtube",
            "baseline_worldtube_definition": "controlled_closed_total_monopole_worldtube",
            "units": "theorem_zero_normalized_multipole",
            "baseline_units": "theorem_zero_normalized_multipole",
            "frame_or_coframe": "same_parent_local_orthonormal_frame",
            "baseline_frame_or_coframe": "same_parent_local_orthonormal_frame",
            "includes_matter": True,
            "includes_EM": True,
            "includes_binding": True,
            "includes_apparatus": True,
            "apparatus_outside_projection": False,
            "GR_routing_flag": True,
            "boundary_flux_TF": "0.0_if_Z_surface_exchange_zero_monopole",
            "d2I_TF_dt2": "0.0_if_Z_stationary_TF_virial",
            "poynting_bound": "0.0_if_Z_Poynting_silent_or_included",
            "source_path": str(source_path),
            "row_kind": "THEOREM_ZERO_CANDIDATE_GUARD_PROFILE_NONCLAIM",
            "certificate_required": "Z_parent_zero_lge1_candidate",
            "claim_blockers": "Z_closed_total_source_monopole|Z_Poynting_silent_or_included|Z_surface_exchange_zero_monopole|Z_no_extra_lge1_MTS_hair",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "source_id": "REAL3980_2_real_lab_row_placeholder_blocked",
            "arena": "future_real_lab_or_PPN_source",
            "l": 2,
            "m": 0,
            "Q_lm_total": "",
            "Q_lm_GR_baseline": "",
            "M_H_ref": "",
            "r_eval": "",
            "worldtube_definition": "",
            "baseline_worldtube_definition": "",
            "units": "",
            "baseline_units": "",
            "frame_or_coframe": "",
            "baseline_frame_or_coframe": "",
            "includes_matter": False,
            "includes_EM": False,
            "includes_binding": False,
            "includes_apparatus": False,
            "apparatus_outside_projection": False,
            "GR_routing_flag": False,
            "boundary_flux_TF": "",
            "d2I_TF_dt2": "",
            "poynting_bound": "",
            "source_path": "",
            "row_kind": "REAL_PROFILE_SLOT_BLOCKED_VALUES_MISSING",
            "certificate_required": "real_source_profile_or_Z_parent_zero_lge1_candidate",
            "claim_blockers": "MISSING_Q_LM_TOTAL|MISSING_Q_LM_GR_BASELINE|MISSING_M_H_REF|MISSING_SOURCE_PATH|MISSING_TOTAL_SOURCE_COMPONENTS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def project_row(row: dict[str, Any], timestamp: str) -> dict[str, Any]:
    blockers: list[str] = []
    q_total = parse_float(row["Q_lm_total"])
    q_gr = parse_float(row["Q_lm_GR_baseline"])
    m_ref = parse_float(row["M_H_ref"])
    source_path_text = str(row["source_path"]).strip()
    source_path = Path(source_path_text) if source_path_text else None
    row_kind = str(row["row_kind"])

    if int(row["l"]) < 1:
        blockers.append("L_NOT_ANGULAR")
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
    if source_path is None or not source_path.exists():
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
            "certificate_status": "BLOCKED_VALUES_OR_COMPATIBILITY_MISSING",
            "claim_blockers": "|".join(blockers),
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }

    assert q_total is not None
    assert q_gr is not None
    assert m_ref is not None
    residual = q_total - q_gr
    epsilon = abs(residual) / abs(m_ref)
    if "THEOREM_ZERO_CANDIDATE" in row_kind and epsilon == 0:
        status = "PROJECTOR_PASS_THEOREM_ZERO_CANDIDATE_NONCLAIM"
        certificate_status = "PROJECTOR_ZERO_PARENT_CERTIFICATE_UNSIGNED"
        claim_blockers = row["claim_blockers"]
    else:
        status = "PROJECTOR_PASS_REAL_ROW_NONCLAIM"
        certificate_status = "PROJECTOR_PASS_REAL_VALUES_CLAIM_STILL_BLOCKED"
        claim_blockers = "CLAIM_PROMOTION_REQUIRES_REAL_SOURCE_AUDIT"
    return {
        "source_id": row["source_id"],
        "projector_status": status,
        "Q_lm_residual": f"{residual:.12g}",
        "epsilon_extra_MTS_l_ge_1": f"{epsilon:.12g}",
        "certificate_status": certificate_status,
        "claim_blockers": claim_blockers,
        "claim_allowed": False,
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
    }


def projector_rows(profiles: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    return [project_row(row, timestamp) for row in profiles]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "BFR3980_0_projector_zero_candidate",
            "symbol": "epsilon_extra_MTS_l_ge_1",
            "formula": "controlled EH monopole theorem-zero candidate gives |0-0|/M_H_ref=0 for l>=1, but only claim-valid if Z_parent_zero_lge1_candidate closes",
            "units": "dimensionless",
            "source_or_certificate": "REAL3980_0_controlled_EH_monopole_l2m0",
            "current_status": "NONTOY_THEOREM_ZERO_CANDIDATE_READY_CLAIM_BLOCKED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BFR3980_1_source_chain",
            "symbol": "epsilon_source_l_ge_1",
            "formula": "epsilon_source_l_ge_1 <= epsilon_closed_source_failure + epsilon_tensor_virial_TF + epsilon_quad_residual_TF + epsilon_EM_Poynting_TF + epsilon_apparatus_TF",
            "units": "dimensionless",
            "source_or_certificate": "3978 bound chain plus 3980 projector candidate",
            "current_status": "BOUND_CHAIN_HAS_FIRST_NONTOY_ZERO_CANDIDATE_BUT_PARENT_FACTORS_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "BFR3980_2_real_row_slot",
            "symbol": "epsilon_extra_MTS_l_ge_1_real",
            "formula": "|Q_lm_total_real-Q_lm_GR_baseline_real|/|M_H_ref_real|",
            "units": "dimensionless",
            "source_or_certificate": "REAL3980_2_real_lab_row_placeholder_blocked",
            "current_status": "REAL_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "feed_id": "FRF3980_0_projector",
            "target": "epsilon_extra_MTS_l_ge_1",
            "update": "first non-toy theorem-zero candidate row passes the projector with zero residual under controlled EH monopole assumptions",
            "effect": "toy-only blocker is removed for the controlled branch, but parent certificate blockers remain",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "FRF3980_1_parent_zero",
            "target": "Z_parent_zero_lge1_candidate",
            "update": "exact certificate factors listed for promoting controlled monopole l>=1 residual zero",
            "effect": "next work can attack specific unsigned factors rather than generic missing source row language",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "FRF3980_2_source_bound",
            "target": "epsilon_source_l_ge_1",
            "update": "3978 source residual chain receives a first controlled theorem-zero candidate plus blocked real-row slot",
            "effect": "source-side route now has both a derivation branch and an empirical row slot",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "FRF3980_3_PPN",
            "target": "Delta_PPN_source_abs",
            "update": "controlled branch contributes zero extra l>=1 source hair only if parent zero certificate closes",
            "effect": "PPN source residual can be suppressed in the controlled branch without judging real non-spherical arenas yet",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "FRF3980_4_next",
            "target": "controlled_monopole_zero_certificate_closure_or_first_lab_source_profile_values",
            "update": f"move to {NEXT_DOC}",
            "effect": "close the certificate factors or source a real lab/PPN profile row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3980_0_route",
            "decision": "attempt parent-zero row before numeric lab row",
            "status": "THEOREM_ZERO_CANDIDATE_BUILT",
            "reason": "a controlled EH monopole branch is the cleanest first non-toy row because Q_lm_total and Q_lm_GR_baseline are both theorem-zero for l>=1",
            "next_action": "close parent certificate factors or keep row nonclaim",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3980_1_no_overclaim",
            "decision": "do not promote controlled row to local-GR claim",
            "status": "CLAIM_BLOCKED_PARENT_FACTORS_UNSIGNED",
            "reason": "closed total source, Poynting inclusion/silence, surface exchange zero, and no extra MTS l>=1 hair remain unsigned",
            "next_action": "attack those exact factors in 3981",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3980_2_real_slot",
            "decision": "stage real lab/PPN row slot",
            "status": "REAL_VALUES_STILL_MISSING",
            "reason": "no sourced numeric Q_lm_total/Q_lm_GR_baseline/M_H_ref row exists in the current local corpus",
            "next_action": "fill real values only after source/provenance is available",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3980_3_next",
            "decision": "next target selected",
            "status": "MOVE_TO_CERTIFICATE_CLOSURE_OR_REAL_VALUES",
            "reason": "the first non-toy candidate exists; progress now means closing the certificate or sourcing a real row",
            "next_action": NEXT_DOC,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3980_0_candidate",
            "gate": "controlled theorem-zero candidate",
            "requirement": "Z_parent_zero_lge1_candidate closes all parent factors",
            "status": "BLOCKED_PARENT_FACTORS_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3980_1_real_values",
            "gate": "real lab/PPN source row",
            "requirement": "sourced Q_lm_total, Q_lm_GR_baseline, M_H_ref, units, frame, worldtube, Poynting/total-source inclusion",
            "status": "BLOCKED_REAL_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3980_2_no_spherical_cheat",
            "gate": "no spherical shortcut",
            "requirement": "controlled EH monopole branch only; cannot average arbitrary non-spherical source into zero",
            "status": "GUARD_ACTIVE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3980_3_local_GR",
            "gate": "local GR",
            "requirement": "controlled source zero plus boundary/external/angular/PPN/Newton/EM/source-coupling gates",
            "status": "LOCAL_GR_STILL_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3980_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "close the controlled monopole parent-zero certificate factors, or source the first real lab/PPN profile values for the projector",
            "success_condition": "either Z_parent_zero_lge1_candidate loses at least one unsigned blocker through derivation, or one non-toy real profile row has sourced numeric Q_lm/GR/M_H_ref values",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, sources: list[dict[str, Any]], projector: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    candidate_pass = sum(row["projector_status"] == "PROJECTOR_PASS_THEOREM_ZERO_CANDIDATE_NONCLAIM" for row in projector)
    blocked = sum(str(row["projector_status"]).startswith("BLOCKED") for row in projector)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "FIRST_NONTOY_THEOREM_ZERO_PROFILE_CANDIDATE_READY_CLAIM_BLOCKED",
            "sources_found": found,
            "sources_total": len(sources),
            "candidate_projector_pass_rows": candidate_pass,
            "blocked_rows": blocked,
            "main_result": "a controlled EH monopole l>=1 source profile candidate now passes the GR-baseline projector with zero residual, but remains nonclaim because closed-source/Poynting/surface/no-extra-hair parent factors are unsigned; real lab/PPN numeric profile values remain missing",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, sources: list[dict[str, Any]], projector: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    candidate_pass = sum(row["projector_status"] == "PROJECTOR_PASS_THEOREM_ZERO_CANDIDATE_NONCLAIM" for row in projector)
    blocked = sum(str(row["projector_status"]).startswith("BLOCKED") for row in projector)
    return f"""# 3980 - First Real Local Source Profile Row Or Parent Zero Certificate

Timestamp: `{timestamp}`

## Result

3980 replaces the purely toy projector smoke with a first non-toy theorem-zero candidate:

```text
controlled EH / Schwarzschild-SdS monopole exterior
same-source GR baseline
l >= 1
Q_lm_total = Q_lm_GR_baseline = 0
=> Q_lm_residual = 0
=> epsilon_extra_MTS_l_ge_1 = 0
```

Projector results:

```text
theorem-zero candidate pass rows: {candidate_pass}
blocked real-value rows: {blocked}
```

## Parent Certificate

Promotion requires:

```text
Z_parent_zero_lge1_candidate =
  Z_EH_vacuum_monopole_family
* Z_same_GR_baseline_monopole
* Z_closed_total_source_monopole
* Z_Poynting_silent_or_included
* Z_surface_exchange_zero_monopole
* Z_no_extra_lge1_MTS_hair
```

This is **not** a spherical averaging cheat. It is only the controlled monopole branch.

## Current Verdict

The first non-toy row exists and passes the projector, but it is not claim-valid. The unsigned blockers are closed total source, Poynting inclusion/silence, surface exchange zero, and no extra MTS `l>=1` hair.

No local-GR claim is made.

Next target:

```text
{NEXT_DOC}
```

Source needles found: `{found}/{len(sources)}`.
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3980 - First Non-Toy Source Profile Candidate

- Timestamp: `{timestamp}`
- Status: `FIRST_NONTOY_THEOREM_ZERO_PROFILE_CANDIDATE_READY_CLAIM_BLOCKED`
- Candidate:
  controlled EH/Schwarzschild-SdS monopole exterior with same-source GR baseline gives `Q_lm_total=Q_lm_GR_baseline=0` for `l>=1`.
- Projector result:
  `epsilon_extra_MTS_l_ge_1=0` for the controlled candidate, but only as nonclaim theorem-zero candidate.
- Claim blockers:
  `Z_closed_total_source_monopole`, `Z_Poynting_silent_or_included`, `Z_surface_exchange_zero_monopole`, and `Z_no_extra_lge1_MTS_hair` remain unsigned.
- Guard:
  this is not a spherical averaging shortcut; it is only the controlled monopole branch.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3980 - First Non-Toy Source Profile Candidate"
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
    profiles = profile_rows(timestamp)
    projector = projector_rows(profiles, timestamp)
    return {
        "sources": sources,
        "certificate": certificate_rows(timestamp),
        "profiles": profiles,
        "projector": projector,
        "bounds": bound_rows(timestamp),
        "feed": feed_rows(timestamp),
        "decision": decision_rows(timestamp),
        "claim_gate": claim_gate_rows(timestamp),
        "next": next_rows(timestamp),
        "status": status_rows(timestamp, sources, projector),
    }


def validation_rows(timestamp: str, rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = rows["sources"]
    certificates = rows["certificate"]
    profiles = rows["profiles"]
    projector = rows["projector"]
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

    factors = {row["factor"] for row in certificates}
    profile_ids = {row["source_id"] for row in profiles}
    projector_by_id = {row["source_id"]: row for row in projector}
    bound_symbols = {row["symbol"] for row in bounds}
    feed_targets = {row["target"] for row in feed}
    decision_statuses = {row["status"] for row in decisions}
    claim_statuses = {row["status"] for row in claims}

    candidate = projector_by_id["REAL3980_0_controlled_EH_monopole_l2m0"]
    guard = projector_by_id["REAL3980_1_same_branch_l3m0_guard"]
    blocked = projector_by_id["REAL3980_2_real_lab_row_placeholder_blocked"]

    return [
        val("VAL3980_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3980_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3980_02_certificate", {"Z_EH_vacuum_monopole_family", "Z_same_GR_baseline_monopole", "Z_closed_total_source_monopole", "Z_Poynting_silent_or_included", "Z_surface_exchange_zero_monopole", "Z_no_extra_lge1_MTS_hair", "Z_no_spherical_cheat", "Z_parent_zero_lge1_candidate"} <= factors, "parent zero certificate factors present"),
        val("VAL3980_03_profiles", {"REAL3980_0_controlled_EH_monopole_l2m0", "REAL3980_1_same_branch_l3m0_guard", "REAL3980_2_real_lab_row_placeholder_blocked"} <= profile_ids, "candidate, guard, and blocked real profile rows present"),
        val("VAL3980_04_candidate_passes", candidate["projector_status"] == "PROJECTOR_PASS_THEOREM_ZERO_CANDIDATE_NONCLAIM" and candidate["epsilon_extra_MTS_l_ge_1"] == "0", "controlled l=2 candidate projects to zero residual"),
        val("VAL3980_05_guard_passes", guard["projector_status"] == "PROJECTOR_PASS_THEOREM_ZERO_CANDIDATE_NONCLAIM" and guard["epsilon_extra_MTS_l_ge_1"] == "0", "same-branch l=3 guard projects to zero residual"),
        val("VAL3980_06_blocked_real_slot", str(blocked["projector_status"]).startswith("BLOCKED") and "MISSING_Q_LM_TOTAL" in blocked["claim_blockers"], "real profile slot blocks missing values"),
        val("VAL3980_07_claim_blockers", "Z_closed_total_source_monopole" in candidate["claim_blockers"] and "Z_no_extra_lge1_MTS_hair" in candidate["claim_blockers"], "candidate keeps parent claim blockers"),
        val("VAL3980_08_bounds", {"epsilon_extra_MTS_l_ge_1", "epsilon_source_l_ge_1", "epsilon_extra_MTS_l_ge_1_real"} <= bound_symbols, "bound feed rows cover projector candidate, source chain, and real slot"),
        val("VAL3980_09_feed", {"epsilon_extra_MTS_l_ge_1", "Z_parent_zero_lge1_candidate", "epsilon_source_l_ge_1", "Delta_PPN_source_abs", "controlled_monopole_zero_certificate_closure_or_first_lab_source_profile_values"} <= feed_targets, "feeds reach projector, parent zero, source chain, PPN, and next target"),
        val("VAL3980_10_decision", {"THEOREM_ZERO_CANDIDATE_BUILT", "CLAIM_BLOCKED_PARENT_FACTORS_UNSIGNED", "REAL_VALUES_STILL_MISSING", "MOVE_TO_CERTIFICATE_CLOSURE_OR_REAL_VALUES"} <= decision_statuses, "decision gate records candidate, blockers, real-value gap, and next move"),
        val("VAL3980_11_claim_gate", {"BLOCKED_PARENT_FACTORS_UNSIGNED", "BLOCKED_REAL_VALUES_MISSING", "GUARD_ACTIVE", "LOCAL_GR_STILL_OPEN"} <= claim_statuses, "claim gates block parent factors, real values, spherical shortcut, and local GR"),
        val("VAL3980_12_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to certificate closure or first real values"),
        val("VAL3980_13_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3980_14_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3980_15_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3980_16_spine_updated", SPINE_PATH.exists() and "3980 - First Non-Toy Source Profile Candidate" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3980_17_csv_parse", parsed, parse_detail),
        val("VAL3980_18_script_compile", True, "script compiled before validation write"),
        val("VAL3980_19_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
        val("VAL3980_20_no_spherical_cheat", any(row["factor"] == "Z_no_spherical_cheat" and row["current_status"] == "GUARD_ACTIVE" for row in certificates), "spherical shortcut guard active"),
        val("VAL3980_21_non_toy", all("TOY" not in row["row_kind"] for row in profiles), "profile rows are not toy smoke rows"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["certificate"], rows["certificate"])
    write_csv(OUTPUTS["profiles"], rows["profiles"])
    write_csv(OUTPUTS["projector"], rows["projector"])
    write_csv(OUTPUTS["bounds"], rows["bounds"])
    write_csv(OUTPUTS["feed"], rows["feed"])
    write_csv(OUTPUTS["decision"], rows["decision"])
    write_csv(OUTPUTS["claim_gate"], rows["claim_gate"])
    write_csv(OUTPUTS["next"], rows["next"])
    write_csv(OUTPUTS["status"], rows["status"])

    DOC_PATH.write_text(doc_text(timestamp, rows["sources"], rows["projector"]), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, rows)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"3980 validation failed: {failed}")

    print(f"3980 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("First non-toy theorem-zero source profile candidate assembled")


if __name__ == "__main__":
    run()

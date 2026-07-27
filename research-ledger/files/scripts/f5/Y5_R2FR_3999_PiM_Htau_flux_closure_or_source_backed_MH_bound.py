from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3999"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3999-Y5-R2FR-PiM-Htau-flux-closure-or-source-backed-MH-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3999_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3999_FLUX_CLOSURE_THEOREM.csv",
    "audit": SRC / "P8_Y5_R2FR_3999_ZERO_PROOF_AUDIT.csv",
    "bounds": SRC / "P8_Y5_R2FR_3999_MH_FLUX_BOUND_VECTOR.csv",
    "cases": SRC / "P8_Y5_R2FR_3999_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_3999_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_3999_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3999_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3999_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3999_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3999_VALIDATION.csv",
}

NEXT_DOC = "4000-Y5-R2FR-EM-Poynting-stress-inside-Hilbert-source-or-radiative-MH-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4000_EM_Poynting_stress_inside_Hilbert_source_or_radiative_MH_bound.py"


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


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3999_00_next", SRC / "P8_Y5_R2FR_3998_NEXT_TARGET.csv", "NEXT3998_0", "3998 handoff"),
        ("SRC3999_01_3964_identity", SRC / "P8_Y5_R2FR_3964_HILBERT_SOURCE_DENOMINATOR_IDENTITY.csv", "HDI3964_2_flux", "surface flux identity"),
        ("SRC3999_02_3964_product", SRC / "P8_Y5_R2FR_3964_HILBERT_SOURCE_DENOMINATOR_IDENTITY.csv", "HDI3964_3_product_rule", "Pi_M product rule"),
        ("SRC3999_03_3964_residual", SRC / "P8_Y5_R2FR_3964_MEFF_FLUX_RESIDUAL_VECTOR.csv", "MFR3964_0_Delta_flux", "flux residual vector"),
        ("SRC3999_04_projector", SRC / "P8_Y5_R2FR_3965_PROJECTOR_STRESS_SPLIT.csv", "PSS3965_1_domain_variation", "projector/domain variation"),
        ("SRC3999_05_boundary", SRC / "P8_Y5_R2FR_3965_PROJECTOR_STRESS_SPLIT.csv", "PSS3965_2_boundary_projector", "boundary/reference projector flux"),
        ("SRC3999_06_readout_guard", SRC / "P8_Y5_R2FR_3965_PROJECTOR_STRESS_SPLIT.csv", "PSS3965_3_readout_guard", "no post-readout projector mask"),
        ("SRC3999_07_active_mass", SRC / "P8_Y5_R2FR_3820_KOMAR_TOLMAN_ACTIVE_MASS_DERIVATION.csv", "KT3820_6_verdict", "active mass route"),
        ("SRC3999_08_active_residual", SRC / "P8_Y5_R2FR_3820_ACTIVE_MASS_RESIDUAL_ROWS.csv", "R3820_5_total", "active mass residual total"),
        ("SRC3999_09_gauss", SRC / "P8_Y5_R2FR_3884_GAUSS_MONOPOLE_CALIBRATION_CHAIN.csv", "GMC3884_2_surface_independence", "Gauss surface independence"),
        ("SRC3999_10_mass_bound", SRC / "P8_Y5_R2FR_3884_MASS_GAUSS_RESIDUAL_BOUND_ROWS.csv", "MGR3884_2_Gauss", "mass/Gauss residual"),
        ("SRC3999_11_orbital_guard", SRC / "P8_Y5_R2FR_3884_ORBITAL_NEWTON_READOUT_CHAIN.csv", "ORB3884_1_no_range", "orbital readout guard"),
        ("SRC3999_12_bridge", SRC / "P8_Y5_R2FR_3966_GAUSS_ORBITAL_BRIDGE_THEOREM_OR_BOUND.csv", "GOB3966_4_delta_cal", "calibration bridge"),
        ("SRC3999_13_3998_theorem", SRC / "P8_Y5_R2FR_3998_HILBERT_MASS_DENOMINATOR_THEOREM.csv", "HDL3998_1_surface_independence", "3998 denominator theorem"),
        ("SRC3999_14_3998_bounds", SRC / "P8_Y5_R2FR_3998_MHREF_BOUND_VECTOR.csv", "MHB3998_2_projector", "3998 projector bound"),
        ("SRC3999_15_3998_results", SRC / "P8_Y5_R2FR_3998_EVALUATOR_RESULTS.csv", "CASE3998_4_missing_parent_rows", "3998 missing-parent guard"),
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


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "FCT3999_0_surface_difference_identity",
            "claim_piece": "surface difference is exact flux",
            "mathematical_form": "M_H[S2]-M_H[S1] = N_G int_A d(Pi_M J_H[tau])",
            "derivation": "Stokes on the annulus A between linked source surfaces S1 and S2 applied to the parent mass-current form.",
            "zero_condition": "d(Pi_M J_H[tau])=0 in A",
            "status": "EXACT_IDENTITY",
            "source_path": str(SRC / "P8_Y5_R2FR_3964_HILBERT_SOURCE_DENOMINATOR_IDENTITY.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "FCT3999_1_Hilbert_Ward_current",
            "claim_piece": "Hilbert current closes in a stationary exterior",
            "mathematical_form": "d J_H[tau] = star((nabla_mu T_H^{mu nu})tau_nu + T_H^{mu nu} nabla_(mu tau_{nu)}) + source_crossing + radiative_flux",
            "derivation": "Diffeomorphism Ward identity gives nabla_mu T_H^{mu nu}=0 on shell; a stationary/Killing exterior makes T_H^{mu nu} nabla_(mu tau_{nu)}=0; no matter crossing and no radiative/Poynting leakage remove the remaining flux terms.",
            "zero_condition": "field equations + Ward conservation + tau stationary/Killing + no source/radiative flux through A",
            "status": "CONDITIONAL_ZERO_THEOREM_COMPONENT",
            "source_path": str(SRC / "P8_Y5_R2FR_3820_KOMAR_TOLMAN_ACTIVE_MASS_DERIVATION.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "FCT3999_2_projector_commutation",
            "claim_piece": "mass projector must commute with exterior transport",
            "mathematical_form": "d(Pi_M J_H)=Pi_M dJ_H + (D Pi_M) wedge J_H + [d,Pi_M]_ref J_H",
            "derivation": "The product rule isolates the only allowed projector obstruction. If Pi_M is parent-owned and covariantly constant on A, then the last two terms vanish before readout.",
            "zero_condition": "D_A Pi_M=0 and [d,Pi_M]_ref J_H=0 with no fitted/readout projector mask",
            "status": "CONDITIONAL_ZERO_THEOREM_COMPONENT",
            "source_path": str(SRC / "P8_Y5_R2FR_3965_PROJECTOR_STRESS_SPLIT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "FCT3999_3_flux_closure_theorem",
            "claim_piece": "Pi_M/H_tau flux closure",
            "mathematical_form": "If FCT3999_1 and FCT3999_2 hold and boundary/reference/non-EH channels are silent, then d(Pi_M J_H[tau])=0 and M_H[S2]=M_H[S1].",
            "derivation": "Insert the Ward-current zero and the projector-commutator zero into the product rule. The annulus flux then vanishes term by term.",
            "zero_condition": "Ward zero + stationary tau + parent-constant Pi_M + fixed reference boundary + no non-EH/memory/range/radiative monopole leakage",
            "status": "DERIVED_CONDITIONAL_LOCAL_STATIONARY_EXTERIOR_ZERO",
            "source_path": str(SRC / "P8_Y5_R2FR_3998_HILBERT_MASS_DENOMINATOR_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "FCT3999_4_absolute_bound_if_not_zero",
            "claim_piece": "failed zero theorem becomes a bounded source residual",
            "mathematical_form": "|Delta M_H|/M_ref <= |N_G|/M_ref int_A (|Pi_M dJ_H| + |D Pi_M wedge J_H| + |dB_ref| + |J_rad/Poynting| + |J_nonEH| + |J_source_crossing|)",
            "derivation": "Triangle inequality on the exact flux identity; no term is allowed to be absorbed into orbital GM.",
            "zero_condition": "all integrand residuals vanish, or each is numeric/source-backed and below the required arena tolerance",
            "status": "EXECUTABLE_BOUND_VECTOR",
            "source_path": str(SRC / "P8_Y5_R2FR_3998_MHREF_BOUND_VECTOR.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "FCT3999_5_Newton_consequence",
            "claim_piece": "Newton source denominator consequence",
            "mathematical_form": "flux closure plus Gauss gives int grad Phi.dS = 4 pi G0 M_H and the exterior monopole Phi=-G0 M_H/r up to retained multipole/range/PPN residuals",
            "derivation": "The closed Hilbert mass fixes the source side of Poisson; orbital motion can then test the resulting potential but cannot define M_H.",
            "zero_condition": "FCT3999_3 plus no range/direct-force/readout residuals",
            "status": "CONDITIONAL_NEWTON_SOURCE_ROUTE_NOT_CLAIM",
            "source_path": str(SRC / "P8_Y5_R2FR_3884_GAUSS_MONOPOLE_CALIBRATION_CHAIN.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "ZP3999_0_EOM_Ward",
            "clause": "parent equations imply Hilbert/Ward current conservation",
            "required_signature": "nabla_mu T_H^{mu nu}=0 for the selected parent branch",
            "current_evidence": "conditional Noether/Ward route recorded, but parent branch still not signed globally",
            "verdict": "CONDITIONAL_NOT_GLOBAL_CLAIM",
            "feeds_bound": "Delta_Ward",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ZP3999_1_tau_stationary",
            "clause": "tau is stationary/Killing in the exterior annulus",
            "required_signature": "T_H^{mu nu} nabla_(mu tau_{nu)}=0 on A",
            "current_evidence": "works for static/stationary exterior branch; not a cosmological or time-dependent source theorem",
            "verdict": "LOCAL_STATIONARY_BRANCH_ONLY",
            "feeds_bound": "Delta_tau",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ZP3999_2_projector_constancy",
            "clause": "Pi_M is parent-owned and covariantly constant on A",
            "required_signature": "D_A Pi_M=0 and [d,Pi_M]_ref J_H=0 before readout",
            "current_evidence": "3965 forbids readout projector masks but does not yet prove parent constancy",
            "verdict": "OPEN_PARENT_PROJECTOR_SIGNATURE",
            "feeds_bound": "Delta_PiM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ZP3999_3_boundary_reference",
            "clause": "boundary and reference subtraction are fixed across S1/S2",
            "required_signature": "dB_ref=0 or numeric/source-backed boundary flux",
            "current_evidence": "boundary projector row exists; source-backed zero/bound not yet signed",
            "verdict": "OPEN_BOUNDARY_REFERENCE_SIGNATURE",
            "feeds_bound": "Delta_boundary",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ZP3999_4_radiation_Poynting_silence",
            "clause": "radiative and Poynting flux do not leak source mass through A",
            "required_signature": "int_A J_rad/Poynting=0, or include EM/wave stress inside J_H with a numeric leakage bound",
            "current_evidence": "newly promoted to explicit residual, not ignored",
            "verdict": "OPEN_BUT_NOW_EXPLICIT",
            "feeds_bound": "Delta_rad_Poynting",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ZP3999_5_nonEH_memory_range",
            "clause": "non-EH, memory, range, and direct-force monopole channels are silent",
            "required_signature": "J_nonEH=0 or source-backed bound",
            "current_evidence": "retained from 3998 as extra mass channel",
            "verdict": "OPEN_EXTRA_CHANNEL_SIGNATURE",
            "feeds_bound": "Delta_nonEH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ZP3999_6_zero_proof_verdict",
            "clause": "local-vacuum/stationary exterior mass plateau",
            "required_signature": "all upstream clauses signed on the same annulus and same tau/Pi_M/reference choices",
            "current_evidence": "conditional theorem derived; global/local-GR claim still blocked by unsigned clauses",
            "verdict": "ZERO_THEOREM_CONSTRUCTED_AS_CONDITIONAL_BRANCH",
            "feeds_bound": "epsilon_MH_flux_3999",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "MHF3999_0_master",
            "target": "epsilon_MH_flux_3999",
            "formula": "|Delta_Ward|+|Delta_tau|+|Delta_PiM|+|Delta_boundary|+|Delta_rad_Poynting|+|Delta_nonEH|+|Delta_source_crossing|",
            "numeric_value": "MISSING_PARENT_SIGNED_COMPONENTS",
            "units": "dimensionless",
            "status": "EXECUTABLE_VECTOR_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "MHF3999_1_Ward",
            "target": "Delta_Ward",
            "formula": "M_ref^-1 |N_G int_A Pi_M dJ_H|",
            "numeric_value": "ZERO_IF_PARENT_EOM_WARD_SIGNED_ELSE_BOUND_REQUIRED",
            "units": "dimensionless",
            "status": "CONDITIONAL_ZERO_OR_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "MHF3999_2_tau",
            "target": "Delta_tau",
            "formula": "M_ref^-1 |N_G int_A Pi_M star(T_H^{mu nu} nabla_(mu tau_{nu)})|",
            "numeric_value": "ZERO_FOR_STATIONARY_KILLING_TAU_ELSE_BOUND_REQUIRED",
            "units": "dimensionless",
            "status": "LOCAL_STATIONARY_BRANCH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "MHF3999_3_projector",
            "target": "Delta_PiM",
            "formula": "M_ref^-1 |N_G int_A ((D Pi_M) wedge J_H + [d,Pi_M]_ref J_H)|",
            "numeric_value": "MISSING_PARENT_PROJECTOR_CONSTANCY",
            "units": "dimensionless",
            "status": "OPEN_PARENT_PROJECTOR_SIGNATURE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "MHF3999_4_boundary",
            "target": "Delta_boundary",
            "formula": "M_ref^-1 |N_G int_A dB_ref|",
            "numeric_value": "MISSING_REFERENCE_BOUNDARY_ZERO_OR_BOUND",
            "units": "dimensionless",
            "status": "OPEN_BOUNDARY_REFERENCE_SIGNATURE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "MHF3999_5_radiation_Poynting",
            "target": "Delta_rad_Poynting",
            "formula": "M_ref^-1 |N_G int_A J_rad/Poynting|, with stationary EM stress included in J_H rather than dropped",
            "numeric_value": "ZERO_STATIC_SILENT_BRANCH_ELSE_SOURCE_BACKED_FLUX_BOUND_REQUIRED",
            "units": "dimensionless",
            "status": "EXPLICIT_EM_WAVE_FLUX_GATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "MHF3999_6_nonEH",
            "target": "Delta_nonEH",
            "formula": "M_ref^-1 |N_G int_A J_nonEH/memory/range/direct|",
            "numeric_value": "MISSING_EXTRA_MONOPOLE_ZERO_OR_BOUND",
            "units": "dimensionless",
            "status": "OPEN_EXTRA_CHANNEL_SIGNATURE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "MHF3999_7_source_crossing",
            "target": "Delta_source_crossing",
            "formula": "M_ref^-1 |N_G int_A J_matter_crossing|",
            "numeric_value": "ZERO_FOR_CLOSED_WORLDTUBE_ELSE_BOUND_REQUIRED",
            "units": "dimensionless",
            "status": "CLOSED_SOURCE_WORLDTUBE_GATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE3999_0_conditional_zero_exterior",
            "route": "stationary_exterior_zero_theorem",
            "M_ref": 1.0,
            "Delta_Ward": 0.0,
            "Delta_tau": 0.0,
            "Delta_PiM": 0.0,
            "Delta_boundary": 0.0,
            "Delta_rad_Poynting": 0.0,
            "Delta_nonEH": 0.0,
            "Delta_source_crossing": 0.0,
            "uses_orbital_as_mass_denominator": False,
            "input_status": "CONDITIONAL_ZERO_CLAUSES_UNSIGNED",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3999_1_static_EM_stress_inside_JH",
            "route": "static_EM_no_Poynting_leakage",
            "M_ref": 1.0,
            "Delta_Ward": 0.0,
            "Delta_tau": 0.0,
            "Delta_PiM": 2.0e-6,
            "Delta_boundary": 1.0e-6,
            "Delta_rad_Poynting": 0.0,
            "Delta_nonEH": 0.0,
            "Delta_source_crossing": 0.0,
            "uses_orbital_as_mass_denominator": False,
            "input_status": "EM_STRESS_RETAINED_NUMERIC_SMOKE_ONLY",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3999_2_radiative_Poynting_leakage",
            "route": "wave_flux_bound_needed",
            "M_ref": 1.0,
            "Delta_Ward": 0.0,
            "Delta_tau": 0.0,
            "Delta_PiM": 0.0,
            "Delta_boundary": 0.0,
            "Delta_rad_Poynting": 4.0e-5,
            "Delta_nonEH": 0.0,
            "Delta_source_crossing": 0.0,
            "uses_orbital_as_mass_denominator": False,
            "input_status": "RADIATIVE_FLUX_NONZERO",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3999_3_projector_drift",
            "route": "PiM_commutator_bound_needed",
            "M_ref": 1.0,
            "Delta_Ward": 0.0,
            "Delta_tau": 0.0,
            "Delta_PiM": 7.0e-5,
            "Delta_boundary": 0.0,
            "Delta_rad_Poynting": 0.0,
            "Delta_nonEH": 0.0,
            "Delta_source_crossing": 0.0,
            "uses_orbital_as_mass_denominator": False,
            "input_status": "PROJECTOR_COMMUTATOR_NONZERO",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3999_4_orbital_backfill_refused",
            "route": "forbidden_orbital_mass_source",
            "M_ref": 1.0,
            "Delta_Ward": 0.0,
            "Delta_tau": 0.0,
            "Delta_PiM": 0.0,
            "Delta_boundary": 0.0,
            "Delta_rad_Poynting": 0.0,
            "Delta_nonEH": 0.0,
            "Delta_source_crossing": 0.0,
            "uses_orbital_as_mass_denominator": True,
            "input_status": "ORBITAL_MU_USED_AS_MH_SOURCE",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3999_5_missing_parent_rows",
            "route": "missing_flux_source_components",
            "M_ref": "",
            "Delta_Ward": "",
            "Delta_tau": "",
            "Delta_PiM": "",
            "Delta_boundary": "",
            "Delta_rad_Poynting": "",
            "Delta_nonEH": "",
            "Delta_source_crossing": "",
            "uses_orbital_as_mass_denominator": False,
            "input_status": "MISSING_PARENT_FLUX_COMPONENT_VECTOR",
            "timestamp_utc": timestamp,
        },
    ]


NUMERIC_FIELDS = [
    "M_ref",
    "Delta_Ward",
    "Delta_tau",
    "Delta_PiM",
    "Delta_boundary",
    "Delta_rad_Poynting",
    "Delta_nonEH",
    "Delta_source_crossing",
]


def optional_float(value: Any) -> float | None:
    text = str(value).strip()
    if not text or text.upper().startswith("MISSING"):
        return None
    return float(text)


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def evaluate_case(row: dict[str, Any]) -> dict[str, Any]:
    values = {field: optional_float(row.get(field)) for field in NUMERIC_FIELDS}
    backfill = as_bool(row.get("uses_orbital_as_mass_denominator"))
    result: dict[str, Any] = {
        "case_id": row["case_id"],
        "route": row["route"],
        "input_status": row["input_status"],
        "M_ref": "MISSING",
        "epsilon_MH_flux_3999": "MISSING",
        "epsilon_conservation_abs": "MISSING",
        "epsilon_projector_boundary_abs": "MISSING",
        "epsilon_radiation_extra_abs": "MISSING",
        "uses_orbital_as_mass_denominator": backfill,
        "passes_schema": False,
        "passes_no_orbital_backfill": not backfill,
        "conditional_zero_theorem_applies": False,
        "bound_ready": False,
        "claim_allowed": False,
        "valid_for_claim": False,
    }
    if any(value is None for value in values.values()) or values["M_ref"] is None or values["M_ref"] <= 0:
        return result
    m_ref = values["M_ref"] or 1.0
    conservation = (abs(values["Delta_Ward"] or 0.0) + abs(values["Delta_tau"] or 0.0)) / m_ref
    projector_boundary = (abs(values["Delta_PiM"] or 0.0) + abs(values["Delta_boundary"] or 0.0)) / m_ref
    radiation_extra = (
        abs(values["Delta_rad_Poynting"] or 0.0)
        + abs(values["Delta_nonEH"] or 0.0)
        + abs(values["Delta_source_crossing"] or 0.0)
    ) / m_ref
    total = conservation + projector_boundary + radiation_extra
    result.update(
        {
            "M_ref": f"{m_ref:.12e}",
            "epsilon_MH_flux_3999": f"{total:.12e}",
            "epsilon_conservation_abs": f"{conservation:.12e}",
            "epsilon_projector_boundary_abs": f"{projector_boundary:.12e}",
            "epsilon_radiation_extra_abs": f"{radiation_extra:.12e}",
            "passes_schema": True,
            "passes_no_orbital_backfill": not backfill,
            "conditional_zero_theorem_applies": total == 0.0 and not backfill,
            "bound_ready": not backfill,
        }
    )
    return result


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows = [evaluate_case(row) for row in cases]
    for row in rows:
        row["timestamp_utc"] = timestamp
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3999_0",
            "finding": "The local stationary exterior flux plateau can be derived conditionally, not axiomatized.",
            "evidence": "d(Pi_M J_H)=0 follows from Ward conservation, stationary tau, parent-constant Pi_M, fixed reference boundary, and no radiation/non-EH/source-crossing flux.",
            "limitation": "Those clauses are not all parent-signed in the current corpus, so no local-GR/Newton source claim is allowed.",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3999_1",
            "finding": "Poynting/radiative flux is now an explicit gate rather than a handwave.",
            "evidence": "Delta_rad_Poynting enters the M_H flux vector and nonzero wave flux changes the source denominator unless it is included in J_H or bounded.",
            "limitation": "Static EM stress must be shown to sit inside the Hilbert source; radiative leakage needs a source-backed bound.",
            "next_action": "derive EM/Poynting stress-inside-J_H split",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CLAIM3999_0_flux_plateau",
            "claim": "M_H is surface independent for local sources",
            "allowed": False,
            "reason": "conditional zero theorem is derived, but projector/radiation/boundary/non-EH clauses are unsigned globally",
            "required_exit": "sign all zero-proof clauses on same annulus or provide source-backed component bounds",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3999_1_Newton_source",
            "claim": "Newton source denominator is fully derived",
            "allowed": False,
            "reason": "M_H flux closure is conditional and source-backed M_H rows are not yet claim-grade",
            "required_exit": NEXT_DOC,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3999_2_orbital_backfill",
            "claim": "orbital GM can close missing M_H rows",
            "allowed": False,
            "reason": "orbital backfill is explicitly refused by the evaluator",
            "required_exit": "non-orbital parent/source mass evidence",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3999_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive whether EM stress/Poynting flux is inside the Hilbert source current or must be bounded as radiative M_H leakage",
            "success_condition": "static EM stress contributes to J_H without extra source drift, while nonzero wave/Poynting leakage becomes a numeric/source-backed Delta_rad_Poynting row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "CONDITIONAL_PIM_HTAU_FLUX_ZERO_THEOREM_AND_EXPLICIT_MH_BOUND_VECTOR",
            "headline": "d(Pi_M J_H)=0 is derived for a stationary exterior branch when Ward, tau, projector, boundary, radiation/Poynting, and non-EH clauses vanish; otherwise each obstruction is now a bounded M_H residual.",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(bool(row["needle_found"]) for row in sources)
    lines = [
        "# 3999 - PiM/Htau Flux Closure Or Source-Backed MH Bound",
        "",
        f"Timestamp: `{timestamp}`",
        "",
        "## Result",
        "",
        "This rung does not merely say the mass plateau is missing. It derives the exact conditional route:",
        "",
        "`d(Pi_M J_H[tau]) = 0`",
        "",
        "holds in a local stationary exterior annulus if the Hilbert/Ward current closes, `tau` is stationary/Killing, `Pi_M` is parent-owned and constant on the annulus, boundary/reference terms are fixed, and no radiative/Poynting, source-crossing, memory/range, or non-EH monopole flux leaks through the annulus.",
        "",
        "## Flux Derivation",
        "",
        "The starting identity remains",
        "",
        "`M_H[S2]-M_H[S1] = N_G int_A d(Pi_M J_H[tau])`.",
        "",
        "The product rule gives",
        "",
        "`d(Pi_M J_H)=Pi_M dJ_H + (D Pi_M) wedge J_H + [d,Pi_M]_ref J_H + boundary/exchange terms`.",
        "",
        "On shell, the Hilbert stress Ward identity gives `nabla_mu T_H^{mu nu}=0`. Contracting with a stationary/Killing `tau` gives `dJ_H[tau]=0`, except for explicit source crossing and radiative/Poynting leakage. If the projector and reference terms also commute, the whole flux vanishes.",
        "",
        "## Bound If Closure Fails",
        "",
        "`|Delta M_H|/M_ref <= |N_G|/M_ref int_A (|Pi_M dJ_H| + |D Pi_M wedge J_H| + |dB_ref| + |J_rad/Poynting| + |J_nonEH| + |J_source_crossing|)`.",
        "",
        "So a failed plateau is not a vague failure anymore. It is the vector `epsilon_MH_flux_3999`.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: status `{row['input_status']}`, epsilon `{row['epsilon_MH_flux_3999']}`, zero={row['conditional_zero_theorem_applies']}, no_backfill={row['passes_no_orbital_backfill']}, claim={row['claim_allowed']}"
        )
    lines.extend(
        [
            "",
        "## Verdict",
        "",
        "We have a real conditional local-vacuum/stationary-exterior mass plateau theorem. We do not yet have a global local-GR claim, because the parent projector, reference boundary, radiation/Poynting silence, and non-EH channel clauses still need to be signed or bounded on the same annulus with the same `tau`, `Pi_M`, and reference choice.",
            "",
            "## Next Target",
            "",
            "The sharpest next move is the EM/Poynting split: prove static EM stress is part of the Hilbert source current, and isolate true radiative flux as a boundable `Delta_rad_Poynting` leakage term.",
            "",
            f"- `{NEXT_DOC}`",
            f"- `{NEXT_SCRIPT}`",
            "",
            "## Source Count",
            "",
            f"- source needles found: `{found}/{len(sources)}`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def append_spine(timestamp: str) -> None:
    marker = "## 3999 - PiM/Htau Flux Closure"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: a conditional stationary-exterior zero theorem is now derived: `d(Pi_M J_H[tau])=0` when Ward conservation, stationary `tau`, parent-constant `Pi_M`, fixed reference boundary, and no radiation/Poynting/non-EH/source-crossing flux all hold on the same annulus.
- Bound route: if any clause fails, `epsilon_MH_flux_3999 = |Delta_Ward|+|Delta_tau|+|Delta_PiM|+|Delta_boundary|+|Delta_rad_Poynting|+|Delta_nonEH|+|Delta_source_crossing|`.
- Important upgrade: Poynting/radiative flux is explicit, not ignored; static EM stress must be shown to live inside `J_H`, while true wave leakage must be bounded.
- Claim status: no local-GR/Newton source claim yet; this is a conditional derivation plus executable residual vector.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    source_paths = [Path(row["path"]) for row in sources]
    add("VAL3999_00_sources_exist", all(path.exists() for path in source_paths), "every cited source path exists")
    add("VAL3999_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    add("VAL3999_02_surface_identity", any(row["theorem_id"] == "FCT3999_0_surface_difference_identity" for row in theorem), "surface flux identity present")
    add("VAL3999_03_Ward_current", any(row["theorem_id"] == "FCT3999_1_Hilbert_Ward_current" for row in theorem), "Ward current row present")
    add("VAL3999_04_projector_commutation", any(row["theorem_id"] == "FCT3999_2_projector_commutation" for row in theorem), "projector commutation row present")
    add("VAL3999_05_zero_theorem", any(row["theorem_id"] == "FCT3999_3_flux_closure_theorem" for row in theorem), "conditional zero theorem present")
    add("VAL3999_06_bound_theorem", any(row["theorem_id"] == "FCT3999_4_absolute_bound_if_not_zero" for row in theorem), "absolute bound theorem present")
    add("VAL3999_07_Newton_consequence", any(row["theorem_id"] == "FCT3999_5_Newton_consequence" for row in theorem), "Newton consequence row present")
    add("VAL3999_08_audit_verdict", any(row["audit_id"] == "ZP3999_6_zero_proof_verdict" for row in audit), "zero-proof verdict audit present")
    add("VAL3999_09_Poynting_audit", any(row["audit_id"] == "ZP3999_4_radiation_Poynting_silence" for row in audit), "Poynting/radiation audit present")
    add("VAL3999_10_master_bound", any(row["bound_id"] == "MHF3999_0_master" for row in bounds), "master flux bound present")
    add("VAL3999_11_Poynting_bound", any(row["bound_id"] == "MHF3999_5_radiation_Poynting" for row in bounds), "Poynting bound present")
    zero = next(row for row in results if row["case_id"] == "CASE3999_0_conditional_zero_exterior")
    static_em = next(row for row in results if row["case_id"] == "CASE3999_1_static_EM_stress_inside_JH")
    radiative = next(row for row in results if row["case_id"] == "CASE3999_2_radiative_Poynting_leakage")
    projector = next(row for row in results if row["case_id"] == "CASE3999_3_projector_drift")
    backfill = next(row for row in results if row["case_id"] == "CASE3999_4_orbital_backfill_refused")
    missing = next(row for row in results if row["case_id"] == "CASE3999_5_missing_parent_rows")
    add("VAL3999_12_zero_case", float(zero["epsilon_MH_flux_3999"]) == 0.0 and str(zero["conditional_zero_theorem_applies"]).lower() == "true", "zero theorem case clean")
    add("VAL3999_13_static_EM_case", float(static_em["epsilon_projector_boundary_abs"]) > 0.0 and float(static_em["epsilon_radiation_extra_abs"]) == 0.0, "static EM stress retained without Poynting leakage")
    add("VAL3999_14_radiative_case", float(radiative["epsilon_radiation_extra_abs"]) > 0.0, "radiative/Poynting leakage produces residual")
    add("VAL3999_15_projector_case", float(projector["epsilon_projector_boundary_abs"]) > 0.0, "projector drift produces residual")
    add("VAL3999_16_backfill_refused", str(backfill["passes_schema"]).lower() == "true" and str(backfill["passes_no_orbital_backfill"]).lower() == "false", "orbital backfill refused")
    add("VAL3999_17_missing_blocks", missing["epsilon_MH_flux_3999"] == "MISSING" and str(missing["passes_schema"]).lower() == "false", "missing parent rows block")
    add("VAL3999_18_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL3999_19_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL3999_20_doc_exists", DOC_PATH.exists() and "Poynting" in read_text(DOC_PATH) and "conditional" in read_text(DOC_PATH), "document written")
    add("VAL3999_21_spine_updated", SPINE_PATH.exists() and "## 3999 - PiM/Htau Flux Closure" in read_text(SPINE_PATH), "spine updated")
    add("VAL3999_22_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL3999_23_compile", compile_ok, "script compiles")
    add("VAL3999_24_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL3999_25_status_exists", OUTPUTS["status"].exists(), "status file exists")
    add("VAL3999_26_results_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for row in results), "all evaluator results remain nonclaim")
    add("VAL3999_27_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL3999_28_same_annulus_guard", DOC_PATH.exists() and "same annulus" in read_text(DOC_PATH), "same-annulus guard recorded")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    audit = audit_rows(timestamp)
    bounds = bound_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["bounds"], bounds)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, results)
    append_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(timestamp, sources, theorem, audit, bounds, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"3999 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()

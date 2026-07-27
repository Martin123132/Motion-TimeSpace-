from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3998"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3998-Y5-R2FR-Hilbert-mass-projector-and-GM-source-denominator-lock.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3998_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3998_HILBERT_MASS_DENOMINATOR_THEOREM.csv",
    "contract": SRC / "P8_Y5_R2FR_3998_GM_ANTI_BACKFILL_CONTRACT.csv",
    "bounds": SRC / "P8_Y5_R2FR_3998_MHREF_BOUND_VECTOR.csv",
    "cases": SRC / "P8_Y5_R2FR_3998_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_3998_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_3998_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3998_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3998_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3998_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3998_VALIDATION.csv",
}

NEXT_DOC = "3999-Y5-R2FR-PiM-Htau-flux-closure-or-source-backed-MH-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3999_PiM_Htau_flux_closure_or_source_backed_MH_bound.py"


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
        ("SRC3998_00_3997_next", SRC / "P8_Y5_R2FR_3997_NEXT_TARGET.csv", "NEXT3997_0", "3997 handoff"),
        ("SRC3998_01_3997_newton", SRC / "P8_Y5_R2FR_3997_G_PRODUCT_AND_NEWTON_MAP.csv", "GN3997_3_GM_guard", "GM anti-circularity input"),
        ("SRC3998_02_3964_identity", SRC / "P8_Y5_R2FR_3964_HILBERT_SOURCE_DENOMINATOR_IDENTITY.csv", "HDI3964_0_definition", "Hilbert denominator identity"),
        ("SRC3998_03_3964_flux", SRC / "P8_Y5_R2FR_3964_MEFF_FLUX_RESIDUAL_VECTOR.csv", "MFR3964_0_Delta_flux", "Meff flux residual vector"),
        ("SRC3998_04_3965_projector", SRC / "P8_Y5_R2FR_3965_PROJECTOR_STRESS_SPLIT.csv", "PSS3965_3_readout_guard", "projector/readout guard"),
        ("SRC3998_05_3819_active", SRC / "P8_Y5_R2FR_3819_ACTIVE_MASS_LAW.csv", "AML3819_2_Poisson_density_refinement", "active mass law"),
        ("SRC3998_06_3819_guard", SRC / "P8_Y5_R2FR_3819_GM_ANTI_CIRCULARITY_CONTRACT.csv", "GM3819_0_observable_split", "GM anti-circularity contract"),
        ("SRC3998_07_3820_mass", SRC / "P8_Y5_R2FR_3820_KOMAR_TOLMAN_ACTIVE_MASS_DERIVATION.csv", "KT3820_6_verdict", "Komar/Tolman active mass route"),
        ("SRC3998_08_3820_residuals", SRC / "P8_Y5_R2FR_3820_ACTIVE_MASS_RESIDUAL_ROWS.csv", "R3820_5_total", "active mass residual rows"),
        ("SRC3998_09_3820_split", SRC / "P8_Y5_R2FR_3820_GM_SPLIT_TEST_CONTRACT.csv", "GST3820_1_independent_mass_gate", "GM split test contract"),
        ("SRC3998_10_3884_gauss", SRC / "P8_Y5_R2FR_3884_GAUSS_MONOPOLE_CALIBRATION_CHAIN.csv", "GMC3884_1_Gauss", "Gauss bridge"),
        ("SRC3998_11_3884_bound", SRC / "P8_Y5_R2FR_3884_MASS_GAUSS_RESIDUAL_BOUND_ROWS.csv", "MGR3884_2_Gauss", "Gauss residual row"),
        ("SRC3998_12_3884_orbital", SRC / "P8_Y5_R2FR_3884_ORBITAL_NEWTON_READOUT_CHAIN.csv", "ORB3884_1_no_range", "orbital readout guard"),
        ("SRC3998_13_3966_bridge", SRC / "P8_Y5_R2FR_3966_GAUSS_ORBITAL_BRIDGE_THEOREM_OR_BOUND.csv", "GOB3966_4_delta_cal", "delta calibration bridge"),
        ("SRC3998_14_3985_schema", SRC / "P8_Y5_R2FR_3985_NEWTONIAN_GM_BOUND_RUNNER_SCHEMA.csv", "epsilon_closed_source_failure_3985", "GM runner schema"),
        ("SRC3998_15_3985_smoke", SRC / "P8_Y5_R2FR_3985_NEWTONIAN_GM_BOUND_SMOKE_RESULTS.csv", "SMOKE3985_2_real_parent_rows_missing", "GM smoke results"),
        ("SRC3998_16_3986_bound", SRC / "P8_Y5_R2FR_3986_GM_SOURCE_AMPLITUDE_BOUND_ROWS.csv", "GMA3986_3_parent_JH", "GM amplitude vector"),
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
            "theorem_id": "HDL3998_0_definition",
            "claim_piece": "Hilbert mass denominator definition",
            "mathematical_form": "M_H_ref[S] := N_G int_S Pi_M J_H[tau], with J_H[tau]=star(T_H(tau,.)) obtained by Hilbert/coframe variation before readout.",
            "derived_result": "the Newton source denominator is a parent projected Hilbert current, not mu_obs/G0",
            "status": "EXACT_CONDITIONAL_DEFINITION",
            "source_path": str(SRC / "P8_Y5_R2FR_3964_HILBERT_SOURCE_DENOMINATOR_IDENTITY.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "HDL3998_1_surface_independence",
            "claim_piece": "surface/worldtube independence",
            "mathematical_form": "M_H_ref[S2]-M_H_ref[S1]=N_G int_A d(Pi_M J_H); if d(Pi_M J_H)=0 in the exterior annulus, the monopole is surface-independent.",
            "derived_result": "radial mass hair is exactly flux/projector failure, not a fit parameter",
            "status": "EXACT_FLUX_IDENTITY_ZERO_IF_CLOSED",
            "source_path": str(SRC / "P8_Y5_R2FR_3964_HILBERT_SOURCE_DENOMINATOR_IDENTITY.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "HDL3998_2_active_mass_refinement",
            "claim_piece": "active mass is Komar/Tolman/Hamiltonian charge",
            "mathematical_form": "M_active=(2/c^2) int_Sigma (T_ab-1/2 T g_ab)n^a tau^b dSigma + boundary/reference terms, reducing to rest/internal/binding/field mass in slow weak closed systems.",
            "derived_result": "rho_H in Poisson is the selected active Hilbert source density; bare T00/c^2 is allowed only after corrections are zeroed or bounded",
            "status": "EXACT_CONDITIONAL_ACTIVE_MASS_LAW",
            "source_path": str(SRC / "P8_Y5_R2FR_3820_KOMAR_TOLMAN_ACTIVE_MASS_DERIVATION.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "HDL3998_3_Gauss_orbital_bridge",
            "claim_piece": "source denominator to orbital monopole",
            "mathematical_form": "nabla^2 Phi=4*pi*G0 rho_H and surface independence imply int grad Phi.dS=4*pi*G0 M_H_ref; slow geodesic exterior gives mu_obs=G0 M_H_ref only when radial/range/frame/direct-force tails vanish or are bounded.",
            "derived_result": "orbital GM is safe verification only after the source denominator is independently owned",
            "status": "EXACT_CONDITIONAL_GAUSS_ORBITAL_CHAIN",
            "source_path": str(SRC / "P8_Y5_R2FR_3884_GAUSS_MONOPOLE_CALIBRATION_CHAIN.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "HDL3998_4_verdict",
            "claim_piece": "3998 current verdict",
            "mathematical_form": "M_H_ref is lockable by parent Hilbert current/projector/flux clauses, otherwise epsilon_GM_denominator is an absolute residual vector.",
            "derived_result": "Newton amplitude cannot be claimed from orbital agreement alone; the next hard gate is Pi_M/H_tau flux closure or independent source-backed M_H rows",
            "status": "DENOMINATOR_ROUTE_REDUCED_NO_NEWTON_CLAIM",
            "source_path": str(SRC / "P8_Y5_R2FR_3985_NEWTONIAN_GM_BOUND_RUNNER_SCHEMA.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def contract_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "GMC3998_0_split_law",
            "rule": "mu_obs = G0 M_H_ref (1+delta_cal+delta_range+delta_frame+delta_PPN+delta_boundary+delta_nonEH)",
            "allowed_use": "orbital data constrain the residual product after G0 and M_H_ref are independently fixed",
            "forbidden_use": "do not set M_H_ref=mu_obs/G0 and then claim Newton/source recovery",
            "status": "EXACT_ANTI_BACKFILL_CONTRACT",
            "source_path": str(SRC / "P8_Y5_R2FR_3819_GM_ANTI_CIRCULARITY_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "GMC3998_1_independent_source_gate",
            "rule": "claim-grade M_H_ref needs parent Hamiltonian/Hilbert charge or non-orbital source evidence with units/frame/tau/reference uncertainty",
            "allowed_use": "lab/calorimetry/density-volume/composition rows or parent charge calculation",
            "forbidden_use": "ephemeris GM as the same arena denominator",
            "status": "SOURCE_LEDGER_REQUIRED",
            "source_path": str(SRC / "P8_Y5_R2FR_3820_GM_SPLIT_TEST_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "GMC3998_2_shared_vector",
            "rule": "the same epsilon_source_total vector must feed WEP/R10/PPN/clocks/orbital/EM stress",
            "allowed_use": "cross-arena constraints on one source-normalization vector",
            "forbidden_use": "per-arena mass/G/readout retuning",
            "status": "NO_PER_ARENA_TUNING",
            "source_path": str(SRC / "P8_Y5_R2FR_3820_GM_SPLIT_TEST_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "GMC3998_3_projector_before_readout",
            "rule": "Pi_M/worldtube/reference surfaces are fixed before orbital/PPN scoring",
            "allowed_use": "parent-owned projector or finite projector-stress bound",
            "forbidden_use": "post-readout Pi_M mask chosen to make GM work",
            "status": "PROJECTOR_READOUT_GUARD",
            "source_path": str(SRC / "P8_Y5_R2FR_3965_PROJECTOR_STRESS_SPLIT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "MHB3998_0_master",
            "target": "epsilon_GM_denominator_3998",
            "formula": "|delta_M_source_Hilbert|/M_ref + |epsilon_PiM_projector_ownership| + |epsilon_extra_mass_channel| + |epsilon_GM_amplitude_calibration| + |epsilon_PPN_source_stability|",
            "numeric_value": "MISSING_PARENT_OR_SOURCE_BACKED_COMPONENTS",
            "units": "dimensionless",
            "status": "EXECUTABLE_ABSOLUTE_VECTOR_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "MHB3998_1_delta_M_source_Hilbert",
            "target": "delta_M_source_Hilbert/M_ref",
            "formula": "|M_dressed - M_H_ref|/M_ref",
            "numeric_value": "MISSING_INDEPENDENT_SOURCE_ROW_OR_PARENT_CHARGE",
            "units": "dimensionless",
            "status": "OPEN_SOURCE_LEDGER_OR_ZERO_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "MHB3998_2_projector",
            "target": "epsilon_PiM_projector_ownership",
            "formula": "|Delta_PiM| + |Delta_flux| + |Delta_symp|",
            "numeric_value": "MISSING_PIM_HTAU_FLUX_BOUND",
            "units": "dimensionless",
            "status": "NEXT_GATE_PROJECTOR_FLUX",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "MHB3998_3_extra_mass",
            "target": "epsilon_extra_mass_channel",
            "formula": "|Delta_extra| + |Delta_nonEH| + |boundary/domain/memory monopole|",
            "numeric_value": "MISSING_EXTRA_MONOPOLE_ZERO_OR_BOUND",
            "units": "dimensionless",
            "status": "OPEN_EXTRA_MONOPOLE_CHANNEL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "MHB3998_4_delta_cal",
            "target": "epsilon_GM_amplitude_calibration",
            "formula": "|mu_obs/(G0 M_H_ref)-1| after source denominator is fixed",
            "numeric_value": "MISSING_SOURCE_DENOMINATOR_FIRST",
            "units": "dimensionless",
            "status": "ORBITAL_PRODUCT_ONLY_UNTIL_MH_LOCK",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "MHB3998_5_PPN",
            "target": "epsilon_PPN_source_stability",
            "formula": "|gamma-1|+|beta-1|+sum|alpha_i|+sum|zeta_i|+|xi| after fixed U=G0 M_H/r",
            "numeric_value": "SYMBOLIC_PPN_SOURCE_VECTOR",
            "units": "dimensionless",
            "status": "PPN_RETAINED_AFTER_NEWTON",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE3998_0_parent_Hilbert_denominator_zero",
            "route": "parent_charge_zero_theorem",
            "M_ref": 1.0,
            "delta_M_source_Hilbert": 0.0,
            "epsilon_PiM_projector_ownership": 0.0,
            "epsilon_extra_mass_channel": 0.0,
            "epsilon_GM_amplitude_calibration": 0.0,
            "epsilon_PPN_source_stability": 0.0,
            "uses_orbital_as_mass_denominator": False,
            "input_status": "CONDITIONAL_ZERO_PARENT_UNSIGNED",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3998_1_small_residual_vector",
            "route": "finite_vector_smoke",
            "M_ref": 1.0,
            "delta_M_source_Hilbert": 1.0e-6,
            "epsilon_PiM_projector_ownership": 2.0e-6,
            "epsilon_extra_mass_channel": 3.0e-6,
            "epsilon_GM_amplitude_calibration": 4.0e-6,
            "epsilon_PPN_source_stability": 5.0e-6,
            "uses_orbital_as_mass_denominator": False,
            "input_status": "NUMERIC_SMOKE_ONLY_NOT_EVIDENCE",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3998_2_orbital_backfill_refused",
            "route": "forbidden_orbital_backfill",
            "M_ref": 1.0,
            "delta_M_source_Hilbert": 0.0,
            "epsilon_PiM_projector_ownership": 0.0,
            "epsilon_extra_mass_channel": 0.0,
            "epsilon_GM_amplitude_calibration": 0.0,
            "epsilon_PPN_source_stability": 0.0,
            "uses_orbital_as_mass_denominator": True,
            "input_status": "ORBITAL_GM_USED_AS_MASS_DENOMINATOR",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3998_3_pressure_binding_open",
            "route": "active_mass_corrections",
            "M_ref": 1.0,
            "delta_M_source_Hilbert": 1.0e-4,
            "epsilon_PiM_projector_ownership": 0.0,
            "epsilon_extra_mass_channel": 2.0e-5,
            "epsilon_GM_amplitude_calibration": 0.0,
            "epsilon_PPN_source_stability": 0.0,
            "uses_orbital_as_mass_denominator": False,
            "input_status": "PRESSURE_BINDING_VECTOR_NONZERO",
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE3998_4_missing_parent_rows",
            "route": "missing_source_denominator",
            "M_ref": "",
            "delta_M_source_Hilbert": "",
            "epsilon_PiM_projector_ownership": "",
            "epsilon_extra_mass_channel": "",
            "epsilon_GM_amplitude_calibration": "",
            "epsilon_PPN_source_stability": "",
            "uses_orbital_as_mass_denominator": False,
            "input_status": "MISSING_MHREF_COMPONENT_VECTOR",
            "timestamp_utc": timestamp,
        },
    ]


NUMERIC_FIELDS = [
    "M_ref",
    "delta_M_source_Hilbert",
    "epsilon_PiM_projector_ownership",
    "epsilon_extra_mass_channel",
    "epsilon_GM_amplitude_calibration",
    "epsilon_PPN_source_stability",
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
        "epsilon_GM_denominator_3998": "MISSING",
        "epsilon_source_mass_abs": "MISSING",
        "epsilon_projector_extra_abs": "MISSING",
        "epsilon_orbital_cal_PPN_abs": "MISSING",
        "uses_orbital_as_mass_denominator": backfill,
        "passes_schema": False,
        "passes_anti_backfill": not backfill,
        "score_ready": False,
        "claim_allowed": False,
        "valid_for_claim": False,
    }
    if any(value is None for value in values.values()) or values["M_ref"] is None or values["M_ref"] <= 0:
        return result
    m_ref = values["M_ref"] or 1.0
    source_mass = abs(values["delta_M_source_Hilbert"] or 0.0) / m_ref
    projector_extra = abs(values["epsilon_PiM_projector_ownership"] or 0.0) + abs(values["epsilon_extra_mass_channel"] or 0.0)
    orbital_ppn = abs(values["epsilon_GM_amplitude_calibration"] or 0.0) + abs(values["epsilon_PPN_source_stability"] or 0.0)
    total = source_mass + projector_extra + orbital_ppn
    result.update(
        {
            "M_ref": f"{m_ref:.12e}",
            "epsilon_GM_denominator_3998": f"{total:.12e}",
            "epsilon_source_mass_abs": f"{source_mass:.12e}",
            "epsilon_projector_extra_abs": f"{projector_extra:.12e}",
            "epsilon_orbital_cal_PPN_abs": f"{orbital_ppn:.12e}",
            "passes_schema": True,
            "passes_anti_backfill": not backfill,
            "score_ready": False,
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
            "decision_id": "DEC3998_0",
            "finding": "Newton amplitude is no longer allowed to hide inside orbital GM",
            "evidence": "M_H_ref defined as parent projected Hilbert current; evaluator refuses orbital-backfilled denominator",
            "limitation": "Pi_M/H_tau flux closure and independent source rows remain unsigned",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3998_1",
            "finding": "active mass source is sharper than bare density",
            "evidence": "Komar/Tolman/Hamiltonian source law retains pressure, binding, boundary and non-EH corrections",
            "limitation": "cold weak sources may suppress corrections, but no universal drop is claimed",
            "next_action": "prove PiM/Htau flux closure or fill first source-backed M_H bound row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CLAIM3998_0_Newton_amplitude",
            "claim": "Newtonian source amplitude is derived",
            "allowed": False,
            "reason": "Hilbert denominator theorem is conditional and source/projector/flux rows remain unsigned",
            "required_exit": NEXT_DOC,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3998_1_orbital_GM",
            "claim": "orbital GM agreement proves M_H_ref",
            "allowed": False,
            "reason": "orbital data are product evidence unless source denominator is independently fixed",
            "required_exit": "independent M_H source ledger or parent charge calculation",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM3998_2_local_GR",
            "claim": "local GR/PPN pass",
            "allowed": False,
            "reason": "Newton source denominator is only first-order; PPN and non-EH residuals remain",
            "required_exit": "componentwise PPN/vector residual closure after fixed U=G0 M_H/r",
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3998_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "prove Pi_M/H_tau flux closure or produce the first source-backed M_H bound row without orbital backfill",
            "success_condition": "d(Pi_M J_H)=0 and projector/reference/worldtube terms vanish, or M_H residual components are numeric, sourced, and nonclaim-evaluated",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "HILBERT_MASS_DENOMINATOR_LOCK_THEOREM_AND_ANTI_BACKFILL_RUNNER",
            "headline": "M_H_ref is now defined as parent projected Hilbert current; orbital GM is explicitly forbidden as the source denominator until flux/projector/source rows close",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(bool(row["needle_found"]) for row in sources)
    lines = [
        "# 3998 - Hilbert Mass Projector And GM Source Denominator Lock",
        "",
        f"Timestamp: `{timestamp}`",
        "",
        "## Result",
        "",
        "The Newton amplitude route is now forced through a real source denominator:",
        "",
        "`M_H_ref[S] := N_G int_S Pi_M J_H[tau]`.",
        "",
        "This is a parent projected Hilbert/coframe current varied before readout. It is not allowed to be defined as `mu_obs/G0`.",
        "",
        "## Denominator Lock",
        "",
        "Surface independence is the exact flux identity",
        "",
        "`M_H_ref[S2]-M_H_ref[S1] = N_G int_A d(Pi_M J_H)`.",
        "",
        "So the next real proof target is concrete: close `d(Pi_M J_H)=0`, or bound its flux/projector/reference residuals.",
        "",
        "## Active Mass",
        "",
        "The source in Poisson is the selected active Hilbert/Hamiltonian source. In stationary branches this is Komar/Tolman-like, and in slow weak closed systems it reduces to rest/internal/binding/field mass only after pressure, stress, boundary and non-EH corrections are retained or bounded.",
        "",
        "## Anti-Backfill Contract",
        "",
        "`mu_obs = G0 M_H_ref (1+delta_cal+delta_range+delta_frame+delta_PPN+delta_boundary+delta_nonEH)`.",
        "",
        "Orbital data can test the product after `G0` and `M_H_ref` are independently fixed. It cannot define both.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: status `{row['input_status']}`, epsilon `{row['epsilon_GM_denominator_3998']}`, schema={row['passes_schema']}, anti_backfill={row['passes_anti_backfill']}, claim={row['claim_allowed']}"
        )
    lines.extend(
        [
            "",
            "## Next Target",
            "",
            "The sharpest next gate is `Pi_M/H_tau` flux closure or the first genuinely source-backed `M_H` bound row. That is where Newtonian mechanics starts becoming a derivation instead of a `GM` fit.",
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
    marker = "## 3998 - Hilbert Mass Denominator Lock"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: `M_H_ref` is now defined as `N_G int_S Pi_M J_H[tau]`, a parent projected Hilbert current before readout, not `mu_obs/G0`.
- Exact identity: `M_H_ref[S2]-M_H_ref[S1]=N_G int_A d(Pi_M J_H)`, so radial/source drift is flux/projector failure.
- Guard: orbital `GM` is product evidence only; it cannot define the source denominator for the same Newton claim.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    source_paths = [Path(row["path"]) for row in sources]
    add("VAL3998_00_sources_exist", all(path.exists() for path in source_paths), "every cited source path exists")
    add("VAL3998_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    add("VAL3998_02_definition", any(row["theorem_id"] == "HDL3998_0_definition" for row in theorem), "Hilbert denominator definition row present")
    add("VAL3998_03_flux_identity", any(row["theorem_id"] == "HDL3998_1_surface_independence" for row in theorem), "surface flux identity row present")
    add("VAL3998_04_active_mass", any(row["theorem_id"] == "HDL3998_2_active_mass_refinement" for row in theorem), "active mass refinement row present")
    add("VAL3998_05_gauss_bridge", any(row["theorem_id"] == "HDL3998_3_Gauss_orbital_bridge" for row in theorem), "Gauss/orbital bridge row present")
    add("VAL3998_06_anti_backfill_contract", any(row["contract_id"] == "GMC3998_0_split_law" for row in contract), "anti-backfill split law present")
    add("VAL3998_07_source_gate", any(row["contract_id"] == "GMC3998_1_independent_source_gate" for row in contract), "independent source gate present")
    add("VAL3998_08_bound_master", any(row["bound_id"] == "MHB3998_0_master" for row in bounds), "master bound row present")
    add("VAL3998_09_projector_bound", any(row["bound_id"] == "MHB3998_2_projector" for row in bounds), "projector bound row present")
    zero = next(row for row in results if row["case_id"] == "CASE3998_0_parent_Hilbert_denominator_zero")
    small = next(row for row in results if row["case_id"] == "CASE3998_1_small_residual_vector")
    backfill = next(row for row in results if row["case_id"] == "CASE3998_2_orbital_backfill_refused")
    pressure = next(row for row in results if row["case_id"] == "CASE3998_3_pressure_binding_open")
    missing = next(row for row in results if row["case_id"] == "CASE3998_4_missing_parent_rows")
    add("VAL3998_10_zero_case", float(zero["epsilon_GM_denominator_3998"]) == 0.0 and str(zero["passes_anti_backfill"]).lower() == "true", "zero case clean")
    add("VAL3998_11_small_case", float(small["epsilon_GM_denominator_3998"]) > 0.0 and str(small["valid_for_claim"]).lower() == "false", "small residual vector computes nonclaim")
    add("VAL3998_12_backfill_refused", str(backfill["passes_schema"]).lower() == "true" and str(backfill["passes_anti_backfill"]).lower() == "false", "orbital backfill refused")
    add("VAL3998_13_pressure_open", float(pressure["epsilon_GM_denominator_3998"]) > 0.0 and str(pressure["passes_anti_backfill"]).lower() == "true", "pressure/binding branch retained")
    add("VAL3998_14_missing_blocks", missing["epsilon_GM_denominator_3998"] == "MISSING" and str(missing["passes_schema"]).lower() == "false", "missing parent rows block")
    add("VAL3998_15_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL3998_16_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL3998_17_doc_exists", DOC_PATH.exists() and "not allowed to be defined as `mu_obs/G0`" in read_text(DOC_PATH), "document written")
    add("VAL3998_18_spine_updated", SPINE_PATH.exists() and "## 3998 - Hilbert Mass Denominator Lock" in read_text(SPINE_PATH), "spine updated")
    add("VAL3998_19_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL3998_20_compile", compile_ok, "script compiles")
    add("VAL3998_21_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    add("VAL3998_22_status_exists", OUTPUTS["status"].exists(), "status file exists")
    add("VAL3998_23_results_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for row in results), "all evaluator results remain nonclaim")
    add("VAL3998_24_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL3998_25_orbital_guard_doc", DOC_PATH.exists() and "It cannot define both" in read_text(DOC_PATH), "orbital GM guard recorded")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    contract = contract_rows(timestamp)
    bounds = bound_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["contract"], contract)
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

    validation = build_validation_rows(timestamp, sources, theorem, contract, bounds, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"3998 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()

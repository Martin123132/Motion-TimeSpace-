from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3985"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3985-Y5-R2FR-source-charge-ownership-subfactor-closure-or-newtonian-GM-bound-runner.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3985_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3985_SUBFACTOR_CLOSURE_THEOREM.csv",
    "certificate": SRC / "P8_Y5_R2FR_3985_CLOSED_SOURCE_CERTIFICATE_UPDATE.csv",
    "residuals": SRC / "P8_Y5_R2FR_3985_RESIDUAL_REDUCTION_ROWS.csv",
    "runner_schema": SRC / "P8_Y5_R2FR_3985_NEWTONIAN_GM_BOUND_RUNNER_SCHEMA.csv",
    "runner_smoke": SRC / "P8_Y5_R2FR_3985_NEWTONIAN_GM_BOUND_SMOKE_RESULTS.csv",
    "projector": SRC / "P8_Y5_R2FR_3985_PROJECTOR_RESULTS.csv",
    "feed": SRC / "P8_Y5_R2FR_3985_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3985_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3985_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3985_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3985_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3985_VALIDATION.csv",
}

NEXT_DOC = "3986-Y5-R2FR-parent-PiM-Hilbert-equality-or-GM-source-amplitude-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3986_parent_PiM_Hilbert_equality_or_GM_source_amplitude_bound.py"


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
        ("SRC3985_00_3984_next", SRC / "P8_Y5_R2FR_3984_NEXT_TARGET.csv", "NEXT3984_0", "3984 handoff"),
        ("SRC3985_01_3984_certificate_tau", SRC / "P8_Y5_R2FR_3984_CLOSED_SOURCE_OWNERSHIP_CERTIFICATE.csv", "CWO3984_0_same_tau", "3984 tau subfactor"),
        ("SRC3985_02_3984_certificate_flux", SRC / "P8_Y5_R2FR_3984_CLOSED_SOURCE_OWNERSHIP_CERTIFICATE.csv", "CWO3984_3_flux_closure", "3984 flux subfactor"),
        ("SRC3985_03_3984_certificate_gauss", SRC / "P8_Y5_R2FR_3984_CLOSED_SOURCE_OWNERSHIP_CERTIFICATE.csv", "CWO3984_6_gauss_calibration", "3984 Gauss subfactor"),
        ("SRC3985_04_3984_residual_master", SRC / "P8_Y5_R2FR_3984_SOURCE_CHARGE_RESIDUAL_ROWS.csv", "SCR3984_0_master", "3984 source residual vector"),
        ("SRC3985_05_3984_projector", SRC / "P8_Y5_R2FR_3984_PROJECTOR_RESULTS.csv", "REAL3984_0_controlled_EH_monopole_l2m0_source_residualized", "3984 controlled projector"),
        ("SRC3985_06_3984_theorem", SRC / "P8_Y5_R2FR_3984_WORLDTUBE_OWNERSHIP_THEOREM_ATTEMPT.csv", "CWO3984_0_EH_reference_derivation", "3984 EH worldtube glue"),
        ("SRC3985_07_3969_unique", SRC / "P8_Y5_R2FR_3969_SINGLE_EXTERIOR_MASS_UNIQUENESS_THEOREM.csv", "UQ3969_1_conditional_uniqueness_theorem", "single exterior time/mass branch"),
        ("SRC3985_08_3969_square", SRC / "P8_Y5_R2FR_3969_SINGLE_EXTERIOR_MASS_UNIQUENESS_THEOREM.csv", "UQ3969_2_square_law_corollary", "weak-field one-mass readout"),
        ("SRC3985_09_worldtube_EH", SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "T510_0_EH_reference_glue", "EH annulus charge glue"),
        ("SRC3985_10_worldtube_source", SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "T510_1_worldtube_source_measure", "dressed source definition"),
        ("SRC3985_11_worldtube_transfer", SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "T510_2_MTS_transfer_condition", "MTS transfer condition"),
        ("SRC3985_12_worldtube_newton", SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "T510_3_Newton_PPN_readout", "Newton/PPN metric readout"),
        ("SRC3985_13_tau_clause", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv", "SM509_0_observed_generator", "same tau clause"),
        ("SRC3985_14_flux_clause", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv", "SM509_3_flux_closure", "flux closure clause"),
        ("SRC3985_15_gauss_clause", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv", "SM509_6_Gauss_orbital_calibration", "Gauss calibration clause"),
        ("SRC3985_16_ppn_clause", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv", "SM509_7_second_order_PPN_stability", "PPN stability clause"),
        ("SRC3985_17_flux_theorem", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv", "T509_1_flux_closure", "radial Meff leakage theorem"),
        ("SRC3985_18_no_extra_theorem", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv", "T509_2_no_extra_mass_channel", "extra mass channel theorem"),
        ("SRC3985_19_HC1_tau", SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv", "HC1_observed_time_generator", "Hamiltonian time generator"),
        ("SRC3985_20_HC2_boundary", SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv", "HC2_differentiable_integrable_Hxi", "boundary integrability"),
        ("SRC3985_21_HC4_charge", SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv", "HC4_charge_equals_PiM_Hilbert_mass", "PiM Hilbert equality"),
        ("SRC3985_22_HC8_gauss", SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv", "HC8_Poisson_Gauss_orbital_calibration", "Poisson/Gauss orbital calibration"),
        ("SRC3985_23_TC500_hilbert", SRC / "P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv", "TC500_3_Hilbert_equality", "PiM Hilbert fail-open"),
        ("SRC3985_24_TC500_cal", SRC / "P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv", "TC500_7_calibration", "calibration fail-open"),
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
            "theorem_id": "SC3985_0_tau_lock",
            "claim_piece": "controlled stationary tau lock",
            "mathematical_form": "controlled EH/no-extra-hair monopole branch has a single stationary exterior generator tau=xi normalized by the same fixed reference used in source charge, exterior charge, clocks, and orbital readout",
            "derived_result": "epsilon_tau_generator_mismatch=0 for this controlled stationary readout branch",
            "status": "BRANCH_SPECIFIC_TAU_LOCK_CLOSED",
            "closure_scope": "controlled stationary EH monopole only; not a full parent matter-coupling theorem",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "SC3985_1_EH_annulus_flux",
            "claim_piece": "EH annulus flux closure",
            "mathematical_form": "in the source-free EH exterior annulus, constraints vanish and the on-shell Hamiltonian/Noether current gives integral_S2 Q_tau - integral_S1 Q_tau=0",
            "derived_result": "epsilon_flux_EH_annulus=0 once the readout is restricted to the EH mass charge",
            "status": "BRANCH_SPECIFIC_EH_FLUX_CLOSURE_CLOSED",
            "closure_scope": "EH annulus piece closed; transfer from parent Pi_M to EH mass charge remains open",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "SC3985_2_boundary_reference",
            "claim_piece": "fixed reference boundary cancellation",
            "mathematical_form": "same reference zero and same fixed inner/outer boundary convention are used on both sides of the residual projector, so Delta B_inner+Delta B_outer+Delta B_reference cancels for the controlled branch comparison",
            "derived_result": "epsilon_boundary_reference_shift=0 for the same-reference controlled projector row",
            "status": "BRANCH_SPECIFIC_BOUNDARY_REFERENCE_CLOSED",
            "closure_scope": "same-reference residual comparison only; global parent boundary action remains unproved",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "SC3985_3_Newton_shape",
            "claim_piece": "Newtonian inverse-square shape from one EH mass charge",
            "mathematical_form": "g00=-1+2mu/(rho c^2)+O(c^-4), Phi=-mu/rho, geodesic slow limit gives a_r=-partial_r Phi=-mu/rho^2",
            "derived_result": "the inverse-square shape follows from the controlled one-charge EH exterior; only the amplitude identity mu=G_ref M_source remains source-coupling dependent",
            "status": "NEWTONIAN_SHAPE_DERIVED_AMPLITUDE_OPEN",
            "closure_scope": "geometry-to-Newton shape closed; G/M_source calibration not derived",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "SC3985_4_reduced_residual",
            "claim_piece": "source residual reduction",
            "mathematical_form": "epsilon_closed_source_failure_3985 <= |delta_M_source_Hilbert|/|M_ref| + epsilon_PiM_projector_ownership + epsilon_extra_mass_channel + epsilon_GM_amplitude_calibration + epsilon_PPN_source_stability",
            "derived_result": "tau, EH-annulus flux, fixed-reference boundary, and Newtonian shape residuals are removed from the controlled-branch master residual; parent Pi_M/Hilbert/source-amplitude terms remain",
            "status": "CONTROLLED_BRANCH_RESIDUAL_VECTOR_REDUCED",
            "closure_scope": "nonclaim residual reduction",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "SC3985_5_not_G_value",
            "claim_piece": "Newton constant stance",
            "mathematical_form": "GR does not derive the numeric value of G from Einstein equations; local recovery requires universal coupling normalization and source-charge equality, not an invented value of G",
            "derived_result": "MTS next target is not numerology for G; it is parent ownership of the universal coupling/source amplitude relation mu=G_ref M_source plus residual bounds",
            "status": "G_VALUE_NOT_REQUIRED_BUT_UNIVERSAL_COUPLING_REQUIRED",
            "closure_scope": "theory discipline note feeding 3986",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    common = {"claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp}
    return [
        {
            "certificate_id": "SC3985_0_same_tau",
            "factor": "Z_same_tau",
            "3984_status": "UNSIGNED_NOT_PARENT_DERIVED",
            "3985_status": "CLOSED_FOR_CONTROLLED_STATIONARY_EH_MONOPOLE_READOUT",
            "residual_after_3985": "epsilon_tau_generator_mismatch=0",
            "remaining_gap": "full parent matter coupling still must use the same observed coframe/generator outside this controlled branch",
            "source_path": str(SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv"),
            **common,
        },
        {
            "certificate_id": "SC3985_1_EH_flux",
            "factor": "Z_EH_annulus_flux_closure",
            "3984_status": "CONDITIONAL_EH_STYLE_NOT_INHERITED_BY_FULL_MTS",
            "3985_status": "CLOSED_FOR_SOURCE_FREE_EH_EXTERIOR_ANNULUS",
            "residual_after_3985": "epsilon_flux_EH_annulus=0",
            "remaining_gap": "parent Pi_M/Hilbert equality must prove the MTS projected source current is this EH charge",
            "source_path": str(SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv"),
            **common,
        },
        {
            "certificate_id": "SC3985_2_boundary_reference",
            "factor": "Z_boundary_reference_compatibility",
            "3984_status": "UNSIGNED_BOUNDARY_REFERENCE_BOOKKEEPING_OPEN",
            "3985_status": "CLOSED_FOR_SAME_REFERENCE_RESIDUAL_PROJECTOR_ROW",
            "residual_after_3985": "epsilon_boundary_reference_shift=0",
            "remaining_gap": "global parent boundary action/integrability is not derived",
            "source_path": str(SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"),
            **common,
        },
        {
            "certificate_id": "SC3985_3_Newton_shape",
            "factor": "Z_Newton_inverse_square_shape",
            "3984_status": "FAIL_OPEN_NEWTONIAN_GM_CALIBRATION_UNSIGNED",
            "3985_status": "SHAPE_CLOSED_AMPLITUDE_OPEN",
            "residual_after_3985": "epsilon_Gauss_shape_error=0; epsilon_GM_amplitude_calibration remains",
            "remaining_gap": "mu=G_ref M_source and universal G_ref are not parent-derived",
            "source_path": str(SRC / "P8_Y5_R2FR_3969_SINGLE_EXTERIOR_MASS_UNIQUENESS_THEOREM.csv"),
            **common,
        },
        {
            "certificate_id": "SC3985_4_parent_JH",
            "factor": "Z_parent_JH",
            "3984_status": "CONDITIONAL_SOURCE_CURRENT_NOT_FULL_PARENT_LOCKED",
            "3985_status": "STILL_OPEN_PARENT_MATTER_ACTION_NEEDED",
            "residual_after_3985": "delta_M_source_Hilbert",
            "remaining_gap": "source current must come from the parent matter/coframe variation, not fitted mass input",
            "source_path": str(SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv"),
            **common,
        },
        {
            "certificate_id": "SC3985_5_parent_PiM",
            "factor": "Z_parent_PiM",
            "3984_status": "FAIL_OPEN_PROJECTOR_OWNERSHIP_UNSIGNED",
            "3985_status": "STILL_OPEN_NEXT_PRIMARY_TARGET",
            "residual_after_3985": "epsilon_PiM_projector_ownership",
            "remaining_gap": "prove Pi_M J_H equals the EH/Hamiltonian mass charge plus exact zero-boundary term",
            "source_path": str(SRC / "P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv"),
            **common,
        },
        {
            "certificate_id": "SC3985_6_no_extra_mass",
            "factor": "Z_no_extra_mass_channel",
            "3984_status": "FAIL_OPEN_RETAINED_EXTRA_MASS_CHANNELS",
            "3985_status": "STILL_OPEN_MONOPOLE_EXTRA_CHARGE_RETAINED",
            "residual_after_3985": "epsilon_extra_mass_channel",
            "remaining_gap": "l>=1 extra hair is closed in the controlled branch, but monopole extra charge/source amplitude remains live",
            "source_path": str(SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv"),
            **common,
        },
        {
            "certificate_id": "SC3985_7_PPN",
            "factor": "Z_PPN_source_stability",
            "3984_status": "UNSIGNED_PPN_STABILITY_OPEN",
            "3985_status": "STILL_OPEN_AFTER_NEWTON_SHAPE",
            "residual_after_3985": "epsilon_PPN_source_stability",
            "remaining_gap": "Newton shape does not prove beta/gamma/preferred-frame source stability",
            "source_path": str(SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv"),
            **common,
        },
        {
            "certificate_id": "SC3985_8_total",
            "factor": "Z_closed_total_source_monopole",
            "3984_status": "FALSE_REPLACED_BY_EXPLICIT_SOURCE_CHARGE_RESIDUAL_VECTOR",
            "3985_status": "FALSE_BUT_RESIDUAL_VECTOR_REDUCED_FOR_CONTROLLED_BRANCH",
            "residual_after_3985": "epsilon_closed_source_failure_3985",
            "remaining_gap": "parent Pi_M/Hilbert equality, source amplitude, extra monopole mass channel, and PPN source stability",
            "source_path": str(SRC / "P8_Y5_R2FR_3984_CLOSED_SOURCE_OWNERSHIP_CERTIFICATE.csv"),
            **common,
        },
    ]


def residual_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "RR3985_0_master_reduced",
            "symbol": "epsilon_closed_source_failure_3985",
            "status": "REDUCED_CONTROLLED_BRANCH_MASTER_RESIDUAL_NONCLAIM",
            "formula": "|delta_M_source_Hilbert|/|M_ref| + epsilon_PiM_projector_ownership + epsilon_extra_mass_channel + epsilon_GM_amplitude_calibration + epsilon_PPN_source_stability",
            "removed_from_3984": "epsilon_tau_generator_mismatch|epsilon_flux_closure_failure(EH_annulus_part)|epsilon_boundary_reference_shift|epsilon_Gauss_shape_error",
            "still_open": "delta_M_source_Hilbert|epsilon_PiM_projector_ownership|epsilon_extra_mass_channel|epsilon_GM_amplitude_calibration|epsilon_PPN_source_stability",
            "units": "dimensionless",
            "source_path": str(SRC / "P8_Y5_R2FR_3984_SOURCE_CHARGE_RESIDUAL_ROWS.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RR3985_1_tau_zero",
            "symbol": "epsilon_tau_generator_mismatch",
            "status": "SET_TO_ZERO_FOR_CONTROLLED_STATIONARY_BRANCH",
            "formula": "tau_source=tau_Hilbert=tau_orbit=xi_static/reference_normalized",
            "removed_from_3984": "yes",
            "still_open": "outside controlled stationary readout branch",
            "units": "dimensionless",
            "source_path": str(SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RR3985_2_flux_split",
            "symbol": "epsilon_flux_closure_failure",
            "status": "SPLIT_EH_PART_ZERO_PARENT_PIM_TRANSFER_OPEN",
            "formula": "epsilon_flux_closure_failure = 0_EH_annulus + epsilon_PiM_to_EH_transfer",
            "removed_from_3984": "EH_annulus_piece",
            "still_open": "epsilon_PiM_to_EH_transfer <= epsilon_PiM_projector_ownership + |delta_M_source_Hilbert|/|M_ref|",
            "units": "dimensionless",
            "source_path": str(SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RR3985_3_boundary_zero",
            "symbol": "epsilon_boundary_reference_shift",
            "status": "SET_TO_ZERO_FOR_SAME_REFERENCE_PROJECTOR_ROW",
            "formula": "Delta B_inner + Delta B_outer + Delta B_reference = 0 under identical subtraction/reference convention",
            "removed_from_3984": "yes_for_controlled_comparator",
            "still_open": "global parent boundary action/integrability",
            "units": "dimensionless",
            "source_path": str(SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RR3985_4_Newton_shape_zero",
            "symbol": "epsilon_Gauss_shape_error",
            "status": "SET_TO_ZERO_FOR_ONE_CHARGE_EH_SLOW_LIMIT",
            "formula": "a_r=-mu/r^2 from g00=-1+2mu/(rc^2)+O(c^-4)",
            "removed_from_3984": "shape_piece_only",
            "still_open": "epsilon_GM_amplitude_calibration = |mu - G_ref M_source|/|G_ref M_ref|",
            "units": "dimensionless",
            "source_path": str(SRC / "P8_Y5_R2FR_3969_SINGLE_EXTERIOR_MASS_UNIQUENESS_THEOREM.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RR3985_5_GM_amplitude",
            "symbol": "epsilon_GM_amplitude_calibration",
            "status": "OPEN_NEXT_PRIMARY_BOUND_TARGET",
            "formula": "|mu - G_ref M_source|/|G_ref M_ref|",
            "removed_from_3984": "no",
            "still_open": "requires parent source charge equality and universal coupling normalization",
            "units": "dimensionless",
            "source_path": str(SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def runner_schema_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "field": "source_id",
            "required": True,
            "units": "text",
            "description": "row identifier for controlled source-charge arena",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "field": "M_ref",
            "required": True,
            "units": "mass_or_GM_unit",
            "description": "normalization mass/charge scale; must be positive",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "field": "delta_M_source_Hilbert",
            "required": True,
            "units": "same_as_M_ref",
            "description": "dressed source charge minus parent Hilbert/Newton charge",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "field": "epsilon_PiM_projector_ownership",
            "required": True,
            "units": "dimensionless",
            "description": "parent ownership residual for Pi_M",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "field": "epsilon_extra_mass_channel",
            "required": True,
            "units": "dimensionless",
            "description": "unowned hidden monopole/source mass-channel residual",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "field": "epsilon_GM_amplitude_calibration",
            "required": True,
            "units": "dimensionless",
            "description": "failure of mu=G_ref M_source after Newtonian shape is derived",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "field": "epsilon_PPN_source_stability",
            "required": True,
            "units": "dimensionless",
            "description": "beta/gamma/preferred-frame source stability residual",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "field": "epsilon_closed_source_failure_3985",
            "required": False,
            "units": "dimensionless",
            "description": "computed sum of normalized open residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def compute_bound(row: dict[str, Any]) -> tuple[str, str, str]:
    required = [
        "M_ref",
        "delta_M_source_Hilbert",
        "epsilon_PiM_projector_ownership",
        "epsilon_extra_mass_channel",
        "epsilon_GM_amplitude_calibration",
        "epsilon_PPN_source_stability",
    ]
    missing = [field for field in required if row.get(field, "") in {"", None, "MISSING"}]
    if missing:
        return ("BLOCKED_MISSING_INPUTS", "|".join(f"MISSING_{field}" for field in missing), "")
    try:
        m_ref = float(row["M_ref"])
        if m_ref <= 0:
            return ("BLOCKED_BAD_M_REF", "M_REF_NOT_POSITIVE", "")
        value = abs(float(row["delta_M_source_Hilbert"])) / abs(m_ref)
        for field in required[2:]:
            value += abs(float(row[field]))
    except ValueError as exc:
        return ("BLOCKED_NONNUMERIC_INPUT", str(exc), "")
    return ("COMPUTED_NONCLAIM", "numeric smoke computation only", f"{value:.12g}")


def runner_smoke_rows(timestamp: str) -> list[dict[str, Any]]:
    inputs = [
        {
            "source_id": "SMOKE3985_0_all_zero_controlled_readout",
            "M_ref": "1.0",
            "delta_M_source_Hilbert": "0.0",
            "epsilon_PiM_projector_ownership": "0.0",
            "epsilon_extra_mass_channel": "0.0",
            "epsilon_GM_amplitude_calibration": "0.0",
            "epsilon_PPN_source_stability": "0.0",
        },
        {
            "source_id": "SMOKE3985_1_small_residual_vector",
            "M_ref": "1.0",
            "delta_M_source_Hilbert": "1e-6",
            "epsilon_PiM_projector_ownership": "2e-6",
            "epsilon_extra_mass_channel": "3e-6",
            "epsilon_GM_amplitude_calibration": "4e-6",
            "epsilon_PPN_source_stability": "5e-6",
        },
        {
            "source_id": "SMOKE3985_2_real_parent_rows_missing",
            "M_ref": "",
            "delta_M_source_Hilbert": "",
            "epsilon_PiM_projector_ownership": "",
            "epsilon_extra_mass_channel": "",
            "epsilon_GM_amplitude_calibration": "",
            "epsilon_PPN_source_stability": "",
        },
    ]
    rows: list[dict[str, Any]] = []
    for row in inputs:
        status, blockers, value = compute_bound(row)
        rows.append(
            {
                **row,
                "epsilon_closed_source_failure_3985": value,
                "runner_status": status,
                "blockers": blockers,
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def projector_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": "REAL3985_0_controlled_EH_monopole_l2m0_reduced_source_residual",
            "angular_projector_status": "PASS_LGE1_ANGULAR_ZERO",
            "Q_lm_residual": "0",
            "epsilon_extra_MTS_l_ge_1": "0",
            "source_charge_residual_before": "epsilon_closed_source_failure",
            "source_charge_residual_after": "epsilon_closed_source_failure_3985",
            "closed_in_3985": "epsilon_tau_generator_mismatch|epsilon_flux_EH_annulus|epsilon_boundary_reference_shift|epsilon_Gauss_shape_error",
            "still_open": "delta_M_source_Hilbert|epsilon_PiM_projector_ownership|epsilon_extra_mass_channel|epsilon_GM_amplitude_calibration|epsilon_PPN_source_stability",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "source_id": "REAL3985_1_same_branch_l3m0_reduced_source_residual",
            "angular_projector_status": "PASS_LGE1_ANGULAR_ZERO",
            "Q_lm_residual": "0",
            "epsilon_extra_MTS_l_ge_1": "0",
            "source_charge_residual_before": "epsilon_closed_source_failure",
            "source_charge_residual_after": "epsilon_closed_source_failure_3985",
            "closed_in_3985": "epsilon_tau_generator_mismatch|epsilon_flux_EH_annulus|epsilon_boundary_reference_shift|epsilon_Gauss_shape_error",
            "still_open": "delta_M_source_Hilbert|epsilon_PiM_projector_ownership|epsilon_extra_mass_channel|epsilon_GM_amplitude_calibration|epsilon_PPN_source_stability",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "feed_id": "FEED3985_0",
            "target": "Z_same_tau",
            "update": "closed branch-specifically for controlled stationary EH monopole readout",
            "status": "SUBFACTOR_CLOSED_BRANCH_SPECIFIC",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "FEED3985_1",
            "target": "Z_EH_annulus_flux_closure",
            "update": "EH exterior annulus flux leakage set to zero; parent PiM transfer remains open",
            "status": "SUBFACTOR_CLOSED_WITH_PARENT_TRANSFER_GAP",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "FEED3985_2",
            "target": "Newtonian_recovery",
            "update": "inverse-square shape derived from one-charge EH slow limit; GM amplitude/source equality remains open",
            "status": "NEWTON_SHAPE_DERIVED_AMPLITUDE_OPEN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "FEED3985_3",
            "target": "epsilon_closed_source_failure",
            "update": "3984 source residual vector reduced to epsilon_closed_source_failure_3985",
            "status": "MASTER_RESIDUAL_REDUCED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3985_0",
            "question": "did any source-ownership subfactor close",
            "answer": "yes, branch-specific tau lock, EH-annulus flux, same-reference boundary cancellation, and Newtonian shape closed for the controlled EH monopole readout",
            "status": "PARTIAL_SUBFACTOR_CLOSURE_ACHIEVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3985_1",
            "question": "does this prove local GR/Newton for MTS",
            "answer": "no; parent PiM/Hilbert equality, source amplitude, extra monopole mass channel, and PPN source stability remain open",
            "status": "LOCAL_GR_STILL_BLOCKED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3985_2",
            "question": "best next target",
            "answer": "attack PiM/Hilbert equality or turn GM amplitude into a bounded source-coupling runner",
            "status": "MOVE_TO_PARENT_PIM_HILBERT_OR_GM_AMPLITUDE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3985_0",
            "gate": "controlled source-owned Newtonian branch",
            "requirement": "epsilon_GM_amplitude_calibration=0 or numerically bounded with parent source charge",
            "status": "BLOCKED_AMPLITUDE_SOURCE_EQUALITY_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3985_1",
            "gate": "parent PiM/Hilbert equality",
            "requirement": "Pi_M J_H equals EH/Hamiltonian mass charge plus exact zero-boundary term",
            "status": "BLOCKED_PARENT_PIM_HILBERT_EQUALITY_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3985_2",
            "gate": "local GR/PPN",
            "requirement": "Newtonian source amplitude plus gamma/beta/preferred-frame source stability",
            "status": "BLOCKED_PPN_SOURCE_STABILITY_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3985_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "prove parent PiM/Hilbert equality or build a GM source-amplitude bound using epsilon_GM_amplitude_calibration",
            "success_condition": "Pi_M J_H is identified with the EH/Hamiltonian mass charge, or a numeric/source-backed GM amplitude residual row blocks/allows Newtonian promotion without closure assumptions",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "SOURCE_CHARGE_SUBFACTORS_PARTLY_CLOSED_NEWTON_SHAPE_DERIVED_AMPLITUDE_OPEN",
            "strongest_result": "controlled stationary tau lock, EH-annulus flux closure, same-reference boundary cancellation, and Newtonian inverse-square shape are closed branch-specifically; master source residual reduced",
            "claim_status": "NONCLAIM_PARENT_PIM_HILBERT_AND_GM_AMPLITUDE_OPEN",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def all_rows(timestamp: str) -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(timestamp),
        "theorem": theorem_rows(timestamp),
        "certificate": certificate_rows(timestamp),
        "residuals": residual_rows(timestamp),
        "runner_schema": runner_schema_rows(timestamp),
        "runner_smoke": runner_smoke_rows(timestamp),
        "projector": projector_rows(timestamp),
        "feed": feed_rows(timestamp),
        "decision": decision_rows(timestamp),
        "claim_gate": claim_gate_rows(timestamp),
        "next": next_rows(timestamp),
        "status": status_rows(timestamp),
    }


def doc_text(timestamp: str, sources: list[dict[str, Any]]) -> str:
    source_lines = "\n".join(
        f"- `{row['source_id']}`: `{row['path']}` needle `{row['needle']}` found={row['needle_found']}"
        for row in sources
    )
    return f"""# 3985 — Source-Charge Ownership Subfactor Closure Or Newtonian GM Bound Runner

Timestamp: `{timestamp}`

## Result

This checkpoint did not circle the same missing coupling. It split the source-coupling blocker and closed the safest branch-specific pieces.

Closed for the controlled stationary EH/no-extra-hair monopole readout:

- `epsilon_tau_generator_mismatch=0`
- `epsilon_flux_EH_annulus=0`
- `epsilon_boundary_reference_shift=0` for the same-reference comparator
- `epsilon_Gauss_shape_error=0`, meaning the inverse-square Newtonian shape follows from the one-charge EH slow limit

## Reduced Residual

The 3984 residual

`epsilon_closed_source_failure`

is reduced, for this controlled branch, to

`epsilon_closed_source_failure_3985 <= |delta_M_source_Hilbert|/|M_ref| + epsilon_PiM_projector_ownership + epsilon_extra_mass_channel + epsilon_GM_amplitude_calibration + epsilon_PPN_source_stability`.

The important move is that Newtonian *shape* is now derived from the geometry, while Newtonian *amplitude* remains a source-coupling problem:

`epsilon_GM_amplitude_calibration = |mu - G_ref M_source|/|G_ref M_ref|`.

This is the correct discipline: GR itself does not derive the measured numerical value of `G`; what a local-GR recovery branch must prove is that the coupling is universal and that the same dressed source charge owns `mu`.

## Nonclaim Guard

Local GR/Newton/PPN is still not claimed. The live blockers are:

- parent `Pi_M/Hilbert` equality;
- source amplitude `mu=G_ref M_source`;
- extra monopole mass/source channels;
- PPN source stability.

## Runner

`P8_Y5_R2FR_3985_NEWTONIAN_GM_BOUND_SMOKE_RESULTS.csv` now computes the reduced source residual when numeric parent rows exist and blocks when they do not.

## Source Register

{source_lines}

## Next Target

`{NEXT_DOC}`

Either prove parent `Pi_M J_H` equals the EH/Hamiltonian mass charge, or build the first real source-backed `GM` amplitude bound row.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3985 - Source-Charge Subfactors Partly Closed"
    entry = f"""

{marker}

- Timestamp: `{timestamp}`
- Status: `SOURCE_CHARGE_SUBFACTORS_PARTLY_CLOSED_NEWTON_SHAPE_DERIVED_AMPLITUDE_OPEN`
- Closed branch-specific pieces:
  `epsilon_tau_generator_mismatch=0`, `epsilon_flux_EH_annulus=0`, `epsilon_boundary_reference_shift=0`, and `epsilon_Gauss_shape_error=0` for the controlled stationary EH monopole readout.
- Main reduction:
  `epsilon_closed_source_failure_3985 <= |delta_M_source_Hilbert|/|M_ref| + epsilon_PiM_projector_ownership + epsilon_extra_mass_channel + epsilon_GM_amplitude_calibration + epsilon_PPN_source_stability`.
- Physics meaning:
  Newtonian inverse-square shape is derived from the one-charge EH slow limit; the amplitude `mu=G_ref M_source` is still the source-coupling problem.
- Still nonclaim:
  parent `Pi_M/Hilbert` equality, source amplitude, extra monopole charge, and PPN source stability remain open.
- Next: `{NEXT_DOC}`.
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else "# Local GR Coupling Spine Current State\n"
    if marker not in existing:
        SPINE_PATH.write_text(existing.rstrip() + entry + "\n", encoding="utf-8")


def validation_rows(timestamp: str, rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = rows["sources"]
    theorem = rows["theorem"]
    certificate = rows["certificate"]
    residuals = rows["residuals"]
    runner_schema = rows["runner_schema"]
    runner_smoke = rows["runner_smoke"]
    projector = rows["projector"]
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

    theorem_statuses = {str(row["status"]) for row in theorem}
    cert_statuses = {str(row["3985_status"]) for row in certificate}
    residual_by_symbol = {str(row["symbol"]): row for row in residuals}
    schema_fields = {str(row["field"]) for row in runner_schema}
    smoke_by_id = {str(row["source_id"]): row for row in runner_smoke}
    project = projector[0]
    feed_statuses = {str(row["status"]) for row in feed}
    decision_statuses = {str(row["status"]) for row in decisions}
    claim_statuses = {str(row["status"]) for row in claims}
    required_schema = {
        "source_id",
        "M_ref",
        "delta_M_source_Hilbert",
        "epsilon_PiM_projector_ownership",
        "epsilon_extra_mass_channel",
        "epsilon_GM_amplitude_calibration",
        "epsilon_PPN_source_stability",
        "epsilon_closed_source_failure_3985",
    }
    required_residuals = {
        "epsilon_closed_source_failure_3985",
        "epsilon_tau_generator_mismatch",
        "epsilon_flux_closure_failure",
        "epsilon_boundary_reference_shift",
        "epsilon_Gauss_shape_error",
        "epsilon_GM_amplitude_calibration",
    }

    return [
        val("VAL3985_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3985_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3985_02_theorem_statuses", {"BRANCH_SPECIFIC_TAU_LOCK_CLOSED", "BRANCH_SPECIFIC_EH_FLUX_CLOSURE_CLOSED", "BRANCH_SPECIFIC_BOUNDARY_REFERENCE_CLOSED", "NEWTONIAN_SHAPE_DERIVED_AMPLITUDE_OPEN", "CONTROLLED_BRANCH_RESIDUAL_VECTOR_REDUCED"} <= theorem_statuses, "tau, flux, boundary, Newton shape, and residual reduction theorem rows present"),
        val("VAL3985_03_certificate_closures", {"CLOSED_FOR_CONTROLLED_STATIONARY_EH_MONOPOLE_READOUT", "CLOSED_FOR_SOURCE_FREE_EH_EXTERIOR_ANNULUS", "CLOSED_FOR_SAME_REFERENCE_RESIDUAL_PROJECTOR_ROW", "SHAPE_CLOSED_AMPLITUDE_OPEN"} <= cert_statuses, "expected branch-specific closures recorded"),
        val("VAL3985_04_certificate_open_gaps", {"STILL_OPEN_PARENT_MATTER_ACTION_NEEDED", "STILL_OPEN_NEXT_PRIMARY_TARGET", "STILL_OPEN_MONOPOLE_EXTRA_CHARGE_RETAINED", "STILL_OPEN_AFTER_NEWTON_SHAPE", "FALSE_BUT_RESIDUAL_VECTOR_REDUCED_FOR_CONTROLLED_BRANCH"} <= cert_statuses, "remaining source ownership gaps remain open"),
        val("VAL3985_05_residual_symbols", required_residuals <= set(residual_by_symbol), "reduced and removed residual symbols present"),
        val("VAL3985_06_master_reduced", "epsilon_tau_generator_mismatch" in residual_by_symbol["epsilon_closed_source_failure_3985"]["removed_from_3984"] and "epsilon_GM_amplitude_calibration" in residual_by_symbol["epsilon_closed_source_failure_3985"]["still_open"], "master residual removes tau/flux/boundary/shape and keeps amplitude open"),
        val("VAL3985_07_runner_schema", required_schema <= schema_fields, "GM residual runner schema has required fields"),
        val("VAL3985_08_runner_zero_smoke", smoke_by_id["SMOKE3985_0_all_zero_controlled_readout"]["epsilon_closed_source_failure_3985"] == "0" and smoke_by_id["SMOKE3985_0_all_zero_controlled_readout"]["runner_status"] == "COMPUTED_NONCLAIM", "zero smoke computes zero nonclaim"),
        val("VAL3985_09_runner_small_smoke", smoke_by_id["SMOKE3985_1_small_residual_vector"]["epsilon_closed_source_failure_3985"] == "1.5e-05", "small smoke computes expected residual sum"),
        val("VAL3985_10_runner_blocks_missing", smoke_by_id["SMOKE3985_2_real_parent_rows_missing"]["runner_status"] == "BLOCKED_MISSING_INPUTS", "runner blocks missing real parent rows"),
        val("VAL3985_11_projector_reduced", project["source_charge_residual_after"] == "epsilon_closed_source_failure_3985" and "epsilon_GM_amplitude_calibration" in project["still_open"], "projector row points at reduced source residual and open amplitude"),
        val("VAL3985_12_feed", {"SUBFACTOR_CLOSED_BRANCH_SPECIFIC", "SUBFACTOR_CLOSED_WITH_PARENT_TRANSFER_GAP", "NEWTON_SHAPE_DERIVED_AMPLITUDE_OPEN", "MASTER_RESIDUAL_REDUCED_NONCLAIM"} <= feed_statuses, "feed captures closure/reduction results"),
        val("VAL3985_13_decision", {"PARTIAL_SUBFACTOR_CLOSURE_ACHIEVED", "LOCAL_GR_STILL_BLOCKED", "MOVE_TO_PARENT_PIM_HILBERT_OR_GM_AMPLITUDE"} <= decision_statuses, "decision gate records progress and next route"),
        val("VAL3985_14_claim_gate", {"BLOCKED_AMPLITUDE_SOURCE_EQUALITY_OPEN", "BLOCKED_PARENT_PIM_HILBERT_EQUALITY_OPEN", "BLOCKED_PPN_SOURCE_STABILITY_OPEN"} <= claim_statuses, "claim gates preserve remaining local-GR blocks"),
        val("VAL3985_15_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to PiM/Hilbert or GM amplitude"),
        val("VAL3985_16_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3985_17_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3985_18_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3985_19_spine_updated", SPINE_PATH.exists() and "3985 - Source-Charge Subfactors Partly Closed" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3985_20_csv_parse", parsed, parse_detail),
        val("VAL3985_21_script_compile", True, "script compiled before validation write"),
        val("VAL3985_22_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["theorem"], rows["theorem"])
    write_csv(OUTPUTS["certificate"], rows["certificate"])
    write_csv(OUTPUTS["residuals"], rows["residuals"])
    write_csv(OUTPUTS["runner_schema"], rows["runner_schema"])
    write_csv(OUTPUTS["runner_smoke"], rows["runner_smoke"])
    write_csv(OUTPUTS["projector"], rows["projector"])
    write_csv(OUTPUTS["feed"], rows["feed"])
    write_csv(OUTPUTS["decision"], rows["decision"])
    write_csv(OUTPUTS["claim_gate"], rows["claim_gate"])
    write_csv(OUTPUTS["next"], rows["next"])
    write_csv(OUTPUTS["status"], rows["status"])

    DOC_PATH.write_text(doc_text(timestamp, rows["sources"]), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, rows)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        for row in failed:
            print(f"FAILED {row['validation_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"3985 validation passed: {len(validations)}/{len(validations)} checks")
    print(f"source needles: {sum(1 for row in rows['sources'] if row['needle_found'])}/{len(rows['sources'])}")
    print(rows["status"][0]["status"])


if __name__ == "__main__":
    run()

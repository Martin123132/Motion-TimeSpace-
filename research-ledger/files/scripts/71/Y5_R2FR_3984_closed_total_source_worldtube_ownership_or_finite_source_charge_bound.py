from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3984"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3984-Y5-R2FR-closed-total-source-worldtube-ownership-or-finite-source-charge-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3984_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3984_WORLDTUBE_OWNERSHIP_THEOREM_ATTEMPT.csv",
    "certificate": SRC / "P8_Y5_R2FR_3984_CLOSED_SOURCE_OWNERSHIP_CERTIFICATE.csv",
    "residuals": SRC / "P8_Y5_R2FR_3984_SOURCE_CHARGE_RESIDUAL_ROWS.csv",
    "projector": SRC / "P8_Y5_R2FR_3984_PROJECTOR_RESULTS.csv",
    "bounds": SRC / "P8_Y5_R2FR_3984_BOUND_FEED_ROWS.csv",
    "feed": SRC / "P8_Y5_R2FR_3984_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3984_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3984_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3984_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3984_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3984_VALIDATION.csv",
}

NEXT_DOC = "3985-Y5-R2FR-source-charge-ownership-subfactor-closure-or-newtonian-GM-bound-runner.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3985_source_charge_ownership_subfactor_closure_or_newtonian_GM_bound_runner.py"


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
        ("SRC3984_00_3983_next", SRC / "P8_Y5_R2FR_3983_NEXT_TARGET.csv", "NEXT3983_0", "3983 handoff to closed-source ownership"),
        ("SRC3984_01_3983_total_source", SRC / "P8_Y5_R2FR_3983_PARENT_ZERO_CERTIFICATE_UPDATE.csv", "PZC3983_2_total_source", "remaining closed-source blocker"),
        ("SRC3984_02_3983_total", SRC / "P8_Y5_R2FR_3983_PARENT_ZERO_CERTIFICATE_UPDATE.csv", "PZC3983_7_total", "parent zero total still false"),
        ("SRC3984_03_3983_projector", SRC / "P8_Y5_R2FR_3983_PROJECTOR_RESULTS.csv", "REAL3983_0_controlled_EH_monopole_l2m0_noextra_closed", "controlled projector candidate"),
        ("SRC3984_04_3983_theorem", SRC / "P8_Y5_R2FR_3983_CONTROLLED_NO_EXTRA_LGE1_HAIR_THEOREM.csv", "NEH3983_2_closed_source_not_smuggled", "no-extra hair does not prove source ownership"),
        ("SRC3984_05_source_identity", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv", "T509_0_charge_identity_needed", "measured GM/source identity needed"),
        ("SRC3984_06_flux_closure", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv", "T509_1_flux_closure", "projected flux closure condition"),
        ("SRC3984_07_no_extra_mass", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv", "T509_2_no_extra_mass_channel", "no extra mass-channel condition"),
        ("SRC3984_08_same_tau", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv", "SM509_0_observed_generator", "same generator clause"),
        ("SRC3984_09_source_current", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv", "SM509_1_source_current", "parent source-current clause"),
        ("SRC3984_10_parent_projector", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv", "SM509_2_parent_mass_projector", "parent projector clause"),
        ("SRC3984_11_worldtube_measure", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv", "SM509_4_worldtube_source_measure", "worldtube source measure clause"),
        ("SRC3984_12_gauss_calibration", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv", "SM509_6_Gauss_orbital_calibration", "Gauss/orbital calibration clause"),
        ("SRC3984_13_ppn_stability", SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv", "SM509_7_second_order_PPN_stability", "PPN source stability clause"),
        ("SRC3984_14_worldtube_reference", SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "T510_0_EH_reference_glue", "EH reference worldtube glue"),
        ("SRC3984_15_worldtube_definition", SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "T510_1_worldtube_source_measure", "dressed source definition"),
        ("SRC3984_16_MTS_transfer", SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "T510_2_MTS_transfer_condition", "MTS transfer condition"),
        ("SRC3984_17_Newton_PPN_readout", SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv", "T510_3_Newton_PPN_readout", "Newton and PPN readout condition"),
        ("SRC3984_18_worldtube_parent_diff", SRC / "P8_WORLDTUBE_SOURCE_MEASURE_CLAUSES.csv", "WG510_0_parent_diffeomorphism_invariance", "parent diffeomorphism clause"),
        ("SRC3984_19_worldtube_same_frame", SRC / "P8_WORLDTUBE_SOURCE_MEASURE_CLAUSES.csv", "WG510_1_minimal_observed_matter_coupling", "same observed matter frame clause"),
        ("SRC3984_20_hamiltonian_charge", SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv", "HC4_charge_equals_PiM_Hilbert_mass", "Hamiltonian-to-Hilbert charge equality"),
        ("SRC3984_21_hidden_charge", SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv", "HC5_no_extra_hidden_charge", "hidden charge fail-open"),
        ("SRC3984_22_orbital_calibration", SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv", "HC8_Poisson_Gauss_orbital_calibration", "Poisson/Gauss/orbital calibration"),
        ("SRC3984_23_residual_fallback", SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv", "HC9_retained_residual_fallback", "residual fallback policy"),
        ("SRC3984_24_pim_hilbert", SRC / "P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv", "TC500_3_Hilbert_equality", "topological PiM Hilbert equality fail-open"),
        ("SRC3984_25_pim_calibration", SRC / "P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv", "TC500_7_calibration", "topological PiM calibration fail-open"),
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
            "theorem_id": "CWO3984_0_EH_reference_derivation",
            "claim_piece": "conditional worldtube charge glue",
            "mathematical_form": "J_tau = theta(phi,L_tau phi)-i_tau L; on shell J_tau=dQ_tau+C_tau. If C_tau=0 in the exterior annulus and boundary flux is silent, integral_S2 Q_tau - integral_S1 Q_tau=0.",
            "derived_result": "a dressed Hamiltonian/Noether source charge is independent of linking sphere for an EH-style source-free exterior",
            "status": "CONDITIONAL_GR_STYLE_WORLDTUBE_GLUE_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CWO3984_1_MTS_transfer_contract",
            "claim_piece": "MTS closed-source transfer condition",
            "mathematical_form": "Z_closed_total_source_monopole = Z_same_tau * Z_parent_JH * Z_parent_PiM * Z_flux_closure * Z_worldtube_source_measure * Z_no_extra_mass_channel * Z_Gauss_orbital_calibration * Z_PPN_source_stability",
            "derived_result": "the exact subfactor contract for promoting the controlled monopole from angular theorem-zero to local source-owned GR branch",
            "status": "EXACT_CERTIFICATE_DECOMPOSITION_BUILT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CWO3984_2_zero_proof_audit",
            "claim_piece": "zero proof attempt",
            "mathematical_form": "Z_closed_total_source_monopole=1 only if every ownership subfactor is parent-signed; existing ledgers mark tau, Pi_M, Hilbert equality, Gauss calibration, and PPN stability open",
            "derived_result": "zero proof fails cleanly; no local-GR or R10/PPN/orbital pass is claimed from source ownership",
            "status": "ZERO_PROOF_REJECTED_UNSIGNED_SUBFACTORS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CWO3984_3_finite_residual_bound",
            "claim_piece": "finite source-charge residual fallback",
            "mathematical_form": "epsilon_closed_source_failure <= |delta_M_source_Hilbert|/|M_ref| + epsilon_tau + epsilon_PiM + epsilon_flux + epsilon_extra_mass + epsilon_Gauss + epsilon_PPN_source + epsilon_boundary_reference",
            "derived_result": "the remaining source-ownership blocker is no longer vague; it is an executable residual vector with named coefficients",
            "status": "FINITE_SOURCE_CHARGE_BOUND_VECTOR_DERIVED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CWO3984_4_monopole_effect",
            "claim_piece": "effect on controlled monopole candidate",
            "mathematical_form": "P_residual(Q_lm)=0 for l>=1 remains true on the controlled EH/no-extra-hair branch, but local source ownership is tracked by epsilon_closed_source_failure",
            "derived_result": "angular theorem-zero survives as a controlled branch result; local GR remains blocked by source-charge ownership residuals",
            "status": "ANGULAR_ZERO_SURVIVES_SOURCE_OWNERSHIP_REMAINS_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    common = {"claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp}
    rows = [
        {
            "certificate_id": "CWO3984_0_same_tau",
            "factor": "Z_same_tau",
            "requirement": "the same observed generator tau is used in matter variation, exterior charge, and orbital/clock readout",
            "source_clause": "SM509_0_observed_generator|WG510_2_time_generator_lock|HC1_observed_time_generator",
            "current_status": "UNSIGNED_NOT_PARENT_DERIVED",
            "residual_if_open": "epsilon_tau_generator_mismatch",
            "effect": "measured GM may be a frame-mixed calibration",
            **common,
        },
        {
            "certificate_id": "CWO3984_1_parent_JH",
            "factor": "Z_parent_JH",
            "requirement": "parent matter/source action defines the Hilbert source current before phenomenological readout",
            "source_clause": "SM509_1_source_current|WG510_1_minimal_observed_matter_coupling",
            "current_status": "CONDITIONAL_SOURCE_CURRENT_NOT_FULL_PARENT_LOCKED",
            "residual_if_open": "delta_M_source_Hilbert",
            "effect": "source mass can be fitted rather than derived from matter/action",
            **common,
        },
        {
            "certificate_id": "CWO3984_2_parent_PiM",
            "factor": "Z_parent_PiM",
            "requirement": "Pi_M is fixed by the parent symplectic/projector algebra and not tuned by source, radius, or arena",
            "source_clause": "SM509_2_parent_mass_projector|WG510_5_projector_ownership|TC500_3_Hilbert_equality",
            "current_status": "FAIL_OPEN_PROJECTOR_OWNERSHIP_UNSIGNED",
            "residual_if_open": "epsilon_PiM_projector_ownership",
            "effect": "projector freedom can absorb failures",
            **common,
        },
        {
            "certificate_id": "CWO3984_3_flux_closure",
            "factor": "Z_flux_closure",
            "requirement": "d(Pi_M J_H)=0 in compact source-free exterior annuli by a parent Ward/Euler/topological identity",
            "source_clause": "T509_1_flux_closure|SM509_3_flux_closure|T510_0_EH_reference_glue",
            "current_status": "CONDITIONAL_EH_STYLE_NOT_INHERITED_BY_FULL_MTS",
            "residual_if_open": "epsilon_flux_closure_failure",
            "effect": "M_eff can leak radially between linking spheres",
            **common,
        },
        {
            "certificate_id": "CWO3984_4_worldtube_measure",
            "factor": "Z_worldtube_source_measure",
            "requirement": "the dressed worldtube source measure equals the exterior parent charge on linking spheres",
            "source_clause": "SM509_4_worldtube_source_measure|T510_1_worldtube_source_measure",
            "current_status": "DEFINITION_CORRECTED_BUT_PARENT_EQUALITY_UNSIGNED",
            "residual_if_open": "delta_M_source_Hilbert",
            "effect": "bare source mass is not falsely equated with measured gravitational mass",
            **common,
        },
        {
            "certificate_id": "CWO3984_5_no_extra_mass",
            "factor": "Z_no_extra_mass_channel",
            "requirement": "nonEH, projector, boundary, domain, memory, range, coupling, and frame sectors carry zero independent mass charge or are retained",
            "source_clause": "T509_2_no_extra_mass_channel|SM509_5_no_extra_channel|HC5_no_extra_hidden_charge",
            "current_status": "FAIL_OPEN_RETAINED_EXTRA_MASS_CHANNELS",
            "residual_if_open": "epsilon_extra_mass_channel",
            "effect": "hidden source charge remains an explicit residual rather than a theorem zero",
            **common,
        },
        {
            "certificate_id": "CWO3984_6_gauss_calibration",
            "factor": "Z_Gauss_orbital_calibration",
            "requirement": "closed charge normalizes to Poisson/Gauss inverse-square orbital acceleration with one universal G_ref",
            "source_clause": "SM509_6_Gauss_orbital_calibration|HC8_Poisson_Gauss_orbital_calibration|TC500_7_calibration",
            "current_status": "FAIL_OPEN_NEWTONIAN_GM_CALIBRATION_UNSIGNED",
            "residual_if_open": "epsilon_Gauss_orbital_calibration",
            "effect": "Newton recovery remains a readout/calibration premise",
            **common,
        },
        {
            "certificate_id": "CWO3984_7_PPN_source_stability",
            "factor": "Z_PPN_source_stability",
            "requirement": "the same source charge survives beta/gamma/preferred-frame PPN expansion without hidden second-order derivative hair",
            "source_clause": "SM509_7_second_order_PPN_stability|T510_3_Newton_PPN_readout",
            "current_status": "UNSIGNED_PPN_STABILITY_OPEN",
            "residual_if_open": "epsilon_PPN_source_stability",
            "effect": "a leading Newton-looking pass would not yet be a local-GR pass",
            **common,
        },
        {
            "certificate_id": "CWO3984_8_boundary_reference",
            "factor": "Z_boundary_reference_compatibility",
            "requirement": "reference zero, inner worldtube boundary, and outer linking surface have compatible boundary terms",
            "source_clause": "WG510_6_reference_zero_and_boundary|HC2_differentiable_integrable_Hxi",
            "current_status": "UNSIGNED_BOUNDARY_REFERENCE_BOOKKEEPING_OPEN",
            "residual_if_open": "epsilon_boundary_reference_shift",
            "effect": "charge equality can be shifted by reference or boundary bookkeeping",
            **common,
        },
        {
            "certificate_id": "CWO3984_9_total_source",
            "factor": "Z_closed_total_source_monopole",
            "requirement": "product of all source-ownership factors closes for the controlled monopole branch",
            "source_clause": "CWO3984_0_same_tau..CWO3984_8_boundary_reference",
            "current_status": "FALSE_REPLACED_BY_EXPLICIT_SOURCE_CHARGE_RESIDUAL_VECTOR",
            "residual_if_open": "epsilon_closed_source_failure",
            "effect": "closed-source blocker is converted to an executable residual bound, not claimed",
            **common,
        },
        {
            "certificate_id": "CWO3984_10_parent_zero_candidate",
            "factor": "Z_parent_zero_lge1_candidate",
            "requirement": "controlled angular theorem-zero plus closed source ownership",
            "source_clause": "PZC3983_7_total|CWO3984_9_total_source",
            "current_status": "FALSE_UNTIL_SOURCE_CHARGE_RESIDUAL_VECTOR_IS_ZERO_OR_BOUNDED_BELOW_TARGET",
            "residual_if_open": "epsilon_closed_source_failure",
            "effect": "projector zero remains nonclaim until source-charge residual is controlled",
            **common,
        },
    ]
    return rows


def residual_rows(timestamp: str) -> list[dict[str, Any]]:
    base_source = str(SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv")
    return [
        {
            "row_id": "SCR3984_0_master",
            "symbol": "epsilon_closed_source_failure",
            "sector": "local_source_charge",
            "definition": "total failure of controlled worldtube source ownership after angular residuals have been projected against same-source GR",
            "formula": "|delta_M_source_Hilbert|/|M_ref| + epsilon_tau_generator_mismatch + epsilon_PiM_projector_ownership + epsilon_flux_closure_failure + epsilon_extra_mass_channel + epsilon_Gauss_orbital_calibration + epsilon_PPN_source_stability + epsilon_boundary_reference_shift",
            "units": "dimensionless",
            "source_path": base_source,
            "status": "DERIVED_RESIDUAL_VECTOR_NONCLAIM",
            "arena": "R2FR/R10/PPN/orbital/local-GR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCR3984_1_mass_equality",
            "symbol": "delta_M_source_Hilbert",
            "sector": "local_source_charge",
            "definition": "difference between dressed worldtube source charge and exterior parent Hilbert/Newton charge",
            "formula": "M_source[W] - (4*pi*G_ref)^-1 integral_S Pi_M J_H",
            "units": "mass or GM/c^2 equivalent before normalization",
            "source_path": str(SRC / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv"),
            "status": "PARENT_EQUALITY_UNSIGNED_RETAINED",
            "arena": "Newtonian GM/source ownership",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCR3984_2_tau",
            "symbol": "epsilon_tau_generator_mismatch",
            "sector": "local_source_charge",
            "definition": "penalty for using different observed time generators in source variation, exterior charge, and orbital readout",
            "formula": "norm(tau_source - tau_Hilbert) + norm(tau_Hilbert - tau_orbit)",
            "units": "dimensionless after chosen generator norm",
            "source_path": str(SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv"),
            "status": "UNSIGNED_RETAINED",
            "arena": "clock/orbital/PPN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCR3984_3_PiM",
            "symbol": "epsilon_PiM_projector_ownership",
            "sector": "local_source_charge",
            "definition": "projector ownership residual if Pi_M is not generated by the parent symplectic/constraint algebra",
            "formula": "norm(delta_parent Pi_M) + norm(Pi_M J_H - J_M_parent)",
            "units": "dimensionless after current normalization",
            "source_path": str(SRC / "P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv"),
            "status": "FAIL_OPEN_RETAINED",
            "arena": "R10/PPN/source coupling",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCR3984_4_flux",
            "symbol": "epsilon_flux_closure_failure",
            "sector": "local_source_charge",
            "definition": "radial leakage of projected Hilbert mass current between exterior linking spheres",
            "formula": "|integral_A d(Pi_M J_H)|/|integral_S Pi_M J_H|",
            "units": "dimensionless",
            "source_path": base_source,
            "status": "CONDITIONAL_CLOSURE_NOT_PARENT_DERIVED",
            "arena": "orbital/radial Meff stability",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCR3984_5_extra_mass",
            "symbol": "epsilon_extra_mass_channel",
            "sector": "local_source_charge",
            "definition": "unowned mass charge carried by nonEH, symplectic, projector, memory, domain, range, coupling, kappa, or frame sectors",
            "formula": "|Q_nonEH+Q_symp+Q_PiM+Q_domain+Q_memory+Q_range+Q_delta_kappa+Q_frame|/|M_ref|",
            "units": "dimensionless",
            "source_path": str(SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"),
            "status": "FAIL_OPEN_RETAINED",
            "arena": "local-GR/R10/PPN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCR3984_6_gauss",
            "symbol": "epsilon_Gauss_orbital_calibration",
            "sector": "local_source_charge",
            "definition": "failure of the closed charge to normalize to Poisson/Gauss inverse-square orbital acceleration with universal G_ref",
            "formula": "|a_r + G_ref*M_source/r^2|/|G_ref*M_source/r^2|",
            "units": "dimensionless",
            "source_path": str(SRC / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"),
            "status": "FAIL_OPEN_RETAINED",
            "arena": "Newtonian mechanics/orbital systems",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCR3984_7_PPN",
            "symbol": "epsilon_PPN_source_stability",
            "sector": "local_source_charge",
            "definition": "second-order local-GR source stability residual after leading source charge is selected",
            "formula": "|gamma-1| + |beta-1| + sum_i |alpha_i| + sum_i |zeta_i| + |xi_PPN|",
            "units": "dimensionless",
            "source_path": str(SRC / "P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv"),
            "status": "UNSIGNED_RETAINED",
            "arena": "PPN/local-GR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SCR3984_8_boundary",
            "symbol": "epsilon_boundary_reference_shift",
            "sector": "local_source_charge",
            "definition": "reference-zero, inner-boundary, or outer-linking-surface bookkeeping shift in the Hamiltonian charge",
            "formula": "|Delta B_inner + Delta B_outer + Delta B_reference|/|M_ref|",
            "units": "dimensionless",
            "source_path": str(SRC / "P8_WORLDTUBE_SOURCE_MEASURE_CLAUSES.csv"),
            "status": "UNSIGNED_RETAINED",
            "arena": "Hamiltonian charge/worldtube definition",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def projector_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": "REAL3984_0_controlled_EH_monopole_l2m0_source_residualized",
            "projector_status": "PROJECTOR_PASS_ANGULAR_ZERO_SOURCE_OWNERSHIP_RESIDUALIZED_NONCLAIM",
            "Q_lm_residual": "0",
            "epsilon_extra_MTS_l_ge_1": "0",
            "source_charge_residual": "epsilon_closed_source_failure",
            "certificate_status": "ANGULAR_ZERO_HELD_CLOSED_SOURCE_NOT_PROVED",
            "claim_blockers": "epsilon_closed_source_failure",
            "removed_blockers": "Z_Poynting_silent_or_included|Z_surface_exchange_zero_monopole|Z_no_extra_lge1_MTS_hair",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "source_id": "REAL3984_1_same_branch_l3m0_source_residualized",
            "projector_status": "PROJECTOR_PASS_ANGULAR_ZERO_SOURCE_OWNERSHIP_RESIDUALIZED_NONCLAIM",
            "Q_lm_residual": "0",
            "epsilon_extra_MTS_l_ge_1": "0",
            "source_charge_residual": "epsilon_closed_source_failure",
            "certificate_status": "ANGULAR_ZERO_HELD_CLOSED_SOURCE_NOT_PROVED",
            "claim_blockers": "epsilon_closed_source_failure",
            "removed_blockers": "Z_Poynting_silent_or_included|Z_surface_exchange_zero_monopole|Z_no_extra_lge1_MTS_hair",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "source_id": "REAL3984_2_finite_lab_source_needed",
            "projector_status": "BLOCKED_PENDING_REAL_SOURCE_CHARGE_INPUTS",
            "Q_lm_residual": "",
            "epsilon_extra_MTS_l_ge_1": "",
            "source_charge_residual": "epsilon_tau_generator_mismatch|epsilon_PiM_projector_ownership|epsilon_flux_closure_failure|epsilon_extra_mass_channel|epsilon_Gauss_orbital_calibration|epsilon_PPN_source_stability|epsilon_boundary_reference_shift",
            "certificate_status": "MISSING_NUMERIC_SOURCE_CHARGE_ROWS",
            "claim_blockers": "MISSING_M_REF|MISSING_TAU_LOCK|MISSING_PIM_PARENT|MISSING_GAUSS_CALIBRATION|MISSING_PPN_SOURCE_STABILITY",
            "removed_blockers": "",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_feed_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for residual in residual_rows(timestamp):
        rows.append(
            {
                "bound_id": residual["row_id"].replace("SCR", "BND"),
                "symbol": residual["symbol"],
                "definition": residual["definition"],
                "formula": residual["formula"],
                "units": residual["units"],
                "needed_for": "controlled monopole source ownership / Newtonian GM / PPN/local-GR promotion",
                "numeric_value": "",
                "status": "AWAITING_PARENT_DERIVATION_OR_REAL_BOUND_INPUT",
                "source_path": residual["source_path"],
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "feed_id": "FEED3984_0",
            "target": "Z_closed_total_source_monopole",
            "update": "not closed; decomposed into exact source-ownership subfactors and replaced by epsilon_closed_source_failure residual vector",
            "status": "BLOCKER_RESIDUALIZED_NOT_CLAIMED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "FEED3984_1",
            "target": "controlled_monopole_projector",
            "update": "l>=1 angular residual theorem-zero remains, but only as controlled nonclaim row with source ownership residual attached",
            "status": "ANGULAR_ZERO_HELD_WITH_SOURCE_RESIDUAL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "FEED3984_2",
            "target": "Newtonian_GM_recovery",
            "update": "next derivation must lock tau, Pi_M, dressed source charge, flux closure, and Gauss/orbital calibration or bound their residuals",
            "status": "NEXT_ROUTE_DEFINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3984_0",
            "question": "can Z_closed_total_source_monopole be parent-proved now",
            "answer": "no",
            "reason": "tau lock, Pi_M ownership, Hilbert equality, extra mass-channel silence, Gauss calibration, and PPN source stability remain unsigned in source ledgers",
            "status": "ZERO_PROOF_REJECTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3984_1",
            "question": "is the remaining blocker now concrete enough to test",
            "answer": "yes",
            "reason": "epsilon_closed_source_failure is decomposed into named finite residual rows with source paths and formulas",
            "status": "SOURCE_CHARGE_RESIDUAL_VECTOR_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3984_2",
            "question": "next best target",
            "answer": "attack one source-ownership subfactor or build Newtonian GM bound runner",
            "reason": "this is the narrowest route from controlled angular zero toward derived Newton/GR recovery",
            "status": "MOVE_TO_SOURCE_CHARGE_SUBFACTOR_OR_GM_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3984_0_controlled_candidate",
            "gate": "controlled monopole local-GR candidate",
            "requirement": "epsilon_closed_source_failure=0 or bounded below arena target with sourced numeric inputs",
            "status": "BLOCKED_SOURCE_CHARGE_RESIDUAL_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3984_1_Newton",
            "gate": "Newtonian mechanics recovery",
            "requirement": "same dressed source charge normalizes to Poisson/Gauss inverse-square law with universal G_ref",
            "status": "BLOCKED_GAUSS_ORBITAL_CALIBRATION_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3984_2_PPN",
            "gate": "PPN/local-GR recovery",
            "requirement": "source charge stable through gamma/beta/preferred-frame expansion",
            "status": "BLOCKED_PPN_SOURCE_STABILITY_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3984_3_R10",
            "gate": "R10/local force bounds",
            "requirement": "source-coupling rows have real parent coefficients and real numeric bound inputs",
            "status": "BLOCKED_NONCLAIM_NUMERIC_INPUTS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3984_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "try to close the source-charge ownership subfactor ladder starting with tau/Pi_M/Hilbert equality, or build a Newtonian GM residual bound runner using epsilon_closed_source_failure",
            "success_condition": "one subfactor becomes parent-signed, or the Newtonian/PPN source-charge residual rows become executable bounded rows without claiming local GR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "CLOSED_SOURCE_OWNERSHIP_ZERO_PROOF_REJECTED_RESIDUAL_VECTOR_READY",
            "strongest_result": "conditional EH-style worldtube charge glue derived; MTS transfer contract decomposed; closed-source blocker converted into epsilon_closed_source_failure residual vector",
            "claim_status": "NONCLAIM_LOCAL_GR_BLOCKED_BY_SOURCE_CHARGE_OWNERSHIP",
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
        "projector": projector_rows(timestamp),
        "bounds": bound_feed_rows(timestamp),
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
    return f"""# 3984 — Closed Total Source Worldtube Ownership Or Finite Source-Charge Bound

Timestamp: `{timestamp}`

## Result

This checkpoint took the last direct controlled-monopole blocker, `Z_closed_total_source_monopole`, and tried the actual zero proof.

The derivation that *does* go through is the conditional GR-style worldtube charge glue:

`J_tau = theta(phi,L_tau phi)-i_tau L`, and on shell `J_tau=dQ_tau+C_tau`.

If the exterior annulus is source-free, the constraints vanish, the boundary/reference terms are compatible, and the same generator `tau` is used everywhere, then the dressed Hamiltonian/Noether charge is independent of linking sphere. That is the clean route by which the source can own the exterior `GM`.

## Why The MTS Promotion Still Does Not Close

For MTS, that conditional result transfers only under the product

`Z_closed_total_source_monopole = Z_same_tau * Z_parent_JH * Z_parent_PiM * Z_flux_closure * Z_worldtube_source_measure * Z_no_extra_mass_channel * Z_Gauss_orbital_calibration * Z_PPN_source_stability`.

The current corpus does not parent-sign those factors. The zero proof is therefore rejected, not smuggled.

## Concrete Forward Motion

The blocker is no longer a vague “source missing” note. It is now the finite residual vector

`epsilon_closed_source_failure <= |delta_M_source_Hilbert|/|M_ref| + epsilon_tau_generator_mismatch + epsilon_PiM_projector_ownership + epsilon_flux_closure_failure + epsilon_extra_mass_channel + epsilon_Gauss_orbital_calibration + epsilon_PPN_source_stability + epsilon_boundary_reference_shift`.

The controlled angular result survives:

`P_residual(Q_lm)=0` for `l>=1` on the controlled EH/no-extra-hair monopole branch.

But local GR/Newton/PPN promotion remains blocked until the source-charge vector is zeroed or bounded with real parent/numeric inputs.

## Outputs

- `source-intake/mts_residuals/P8_Y5_R2FR_3984_CLOSED_SOURCE_OWNERSHIP_CERTIFICATE.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3984_SOURCE_CHARGE_RESIDUAL_ROWS.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3984_PROJECTOR_RESULTS.csv`
- `source-intake/mts_residuals/P8_Y5_R2FR_3984_BOUND_FEED_ROWS.csv`
- `source-intake/mts_residuals/P8_Y5_BRR545_3984_VALIDATION.csv`

## Source Register

{source_lines}

## Next Target

`{NEXT_DOC}`

Try to close the source-charge ownership subfactor ladder, starting with the least slippery pieces: same generator `tau`, parent-owned `Pi_M`, Hilbert/source equality, and Newtonian Gauss/orbital calibration. If those do not close, turn the same residual vector into a real Newtonian/PPN bound runner.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3984 - Closed Source Ownership Residualized"
    entry = f"""

{marker}

- Timestamp: `{timestamp}`
- Status: `CLOSED_SOURCE_OWNERSHIP_ZERO_PROOF_REJECTED_RESIDUAL_VECTOR_READY`
- Conditional derivation:
  EH-style worldtube glue gives a dressed Hamiltonian/Noether charge independent of linking sphere when the exterior constraints, boundary/reference terms, and generator choice are controlled.
- Exact MTS transfer contract:
  `Z_closed_total_source_monopole = Z_same_tau * Z_parent_JH * Z_parent_PiM * Z_flux_closure * Z_worldtube_source_measure * Z_no_extra_mass_channel * Z_Gauss_orbital_calibration * Z_PPN_source_stability`.
- Current result:
  the transfer does not close; the blocker is converted to `epsilon_closed_source_failure` and its sub-residuals.
- Still useful:
  controlled `l>=1` angular theorem-zero remains, but source ownership blocks local GR/Newton/PPN promotion.
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

    theorem_statuses = {str(row["status"]) for row in theorem}
    factors = {str(row["factor"]): row for row in certificate}
    residual_symbols = {str(row["symbol"]) for row in residuals}
    bound_symbols = {str(row["symbol"]) for row in bounds}
    project_by_id = {str(row["source_id"]): row for row in projector}
    decision_statuses = {str(row["status"]) for row in decisions}
    claim_statuses = {str(row["status"]) for row in claims}
    feed_statuses = {str(row["status"]) for row in feed}
    candidate = project_by_id["REAL3984_0_controlled_EH_monopole_l2m0_source_residualized"]
    required_factors = {
        "Z_same_tau",
        "Z_parent_JH",
        "Z_parent_PiM",
        "Z_flux_closure",
        "Z_worldtube_source_measure",
        "Z_no_extra_mass_channel",
        "Z_Gauss_orbital_calibration",
        "Z_PPN_source_stability",
        "Z_boundary_reference_compatibility",
        "Z_closed_total_source_monopole",
        "Z_parent_zero_lge1_candidate",
    }
    required_residuals = {
        "epsilon_closed_source_failure",
        "delta_M_source_Hilbert",
        "epsilon_tau_generator_mismatch",
        "epsilon_PiM_projector_ownership",
        "epsilon_flux_closure_failure",
        "epsilon_extra_mass_channel",
        "epsilon_Gauss_orbital_calibration",
        "epsilon_PPN_source_stability",
        "epsilon_boundary_reference_shift",
    }

    return [
        val("VAL3984_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3984_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3984_02_theorem_attempt", {"CONDITIONAL_GR_STYLE_WORLDTUBE_GLUE_DERIVED", "EXACT_CERTIFICATE_DECOMPOSITION_BUILT", "ZERO_PROOF_REJECTED_UNSIGNED_SUBFACTORS", "FINITE_SOURCE_CHARGE_BOUND_VECTOR_DERIVED_NONCLAIM"} <= theorem_statuses, "conditional derivation, exact certificate, rejection, and residual vector present"),
        val("VAL3984_03_certificate_factors", required_factors <= set(factors), "all source ownership certificate factors present"),
        val("VAL3984_04_total_not_closed", factors["Z_closed_total_source_monopole"]["current_status"] == "FALSE_REPLACED_BY_EXPLICIT_SOURCE_CHARGE_RESIDUAL_VECTOR", "closed-source total is not claimed"),
        val("VAL3984_05_parent_zero_false", factors["Z_parent_zero_lge1_candidate"]["current_status"] == "FALSE_UNTIL_SOURCE_CHARGE_RESIDUAL_VECTOR_IS_ZERO_OR_BOUNDED_BELOW_TARGET", "parent zero candidate remains false"),
        val("VAL3984_06_fail_open_subfactors", any("FAIL_OPEN" in str(row["current_status"]) for row in certificate), "fail-open source ownership subfactors remain explicit"),
        val("VAL3984_07_residual_symbols", required_residuals <= residual_symbols, "all source-charge residual symbols present"),
        val("VAL3984_08_bound_symbols", required_residuals <= bound_symbols, "all source-charge residual symbols mirrored into bound feed rows"),
        val("VAL3984_09_projector_candidate", candidate["projector_status"] == "PROJECTOR_PASS_ANGULAR_ZERO_SOURCE_OWNERSHIP_RESIDUALIZED_NONCLAIM" and candidate["source_charge_residual"] == "epsilon_closed_source_failure", "controlled candidate keeps angular zero with source residual attached"),
        val("VAL3984_10_claim_blocker_residualized", candidate["claim_blockers"] == "epsilon_closed_source_failure", "old closed-source blocker converted to explicit residual"),
        val("VAL3984_11_no_local_GR_claim", {"BLOCKED_SOURCE_CHARGE_RESIDUAL_OPEN", "BLOCKED_GAUSS_ORBITAL_CALIBRATION_UNSIGNED", "BLOCKED_PPN_SOURCE_STABILITY_UNSIGNED", "BLOCKED_NONCLAIM_NUMERIC_INPUTS_MISSING"} <= claim_statuses, "claim gates block local GR/Newton/PPN/R10 promotion"),
        val("VAL3984_12_decision", {"ZERO_PROOF_REJECTED", "SOURCE_CHARGE_RESIDUAL_VECTOR_READY", "MOVE_TO_SOURCE_CHARGE_SUBFACTOR_OR_GM_BOUND"} <= decision_statuses, "decision gate records rejection, residualization, and next route"),
        val("VAL3984_13_feed", {"BLOCKER_RESIDUALIZED_NOT_CLAIMED", "ANGULAR_ZERO_HELD_WITH_SOURCE_RESIDUAL", "NEXT_ROUTE_DEFINED"} <= feed_statuses, "feed rows update closed source, angular candidate, and next route"),
        val("VAL3984_14_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to source charge subfactor/GM bound"),
        val("VAL3984_15_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3984_16_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3984_17_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3984_18_spine_updated", SPINE_PATH.exists() and "3984 - Closed Source Ownership Residualized" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3984_19_csv_parse", parsed, parse_detail),
        val("VAL3984_20_script_compile", True, "script compiled before validation write"),
        val("VAL3984_21_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["theorem"], rows["theorem"])
    write_csv(OUTPUTS["certificate"], rows["certificate"])
    write_csv(OUTPUTS["residuals"], rows["residuals"])
    write_csv(OUTPUTS["projector"], rows["projector"])
    write_csv(OUTPUTS["bounds"], rows["bounds"])
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
    print(f"3984 validation passed: {len(validations)}/{len(validations)} checks")
    print(f"source needles: {sum(1 for row in rows['sources'] if row['needle_found'])}/{len(rows['sources'])}")
    print(rows["status"][0]["status"])


if __name__ == "__main__":
    run()

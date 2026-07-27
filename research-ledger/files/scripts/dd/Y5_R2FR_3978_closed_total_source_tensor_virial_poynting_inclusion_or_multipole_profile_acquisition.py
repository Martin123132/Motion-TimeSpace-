from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3978"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3978-Y5-R2FR-closed-total-source-tensor-virial-poynting-inclusion-or-multipole-profile-acquisition.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3978_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3978_CLOSED_SOURCE_TENSOR_VIRIAL_THEOREM.csv",
    "poynting": SRC / "P8_Y5_R2FR_3978_POYNTING_INCLUSION_CONTRACT.csv",
    "schema": SRC / "P8_Y5_R2FR_3978_SOURCE_PROFILE_ACQUISITION_SCHEMA.csv",
    "bounds": SRC / "P8_Y5_R2FR_3978_SOURCE_RESIDUAL_BOUND_ROWS.csv",
    "certificate": SRC / "P8_Y5_R2FR_3978_Z_SOURCE_ZERO_UPDATE.csv",
    "feed": SRC / "P8_Y5_R2FR_3978_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3978_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3978_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3978_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3978_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3978_VALIDATION.csv",
}

NEXT_DOC = "3979-Y5-R2FR-GR-baseline-residual-projector-contract-or-source-profile-runner.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3979_GR_baseline_residual_projector_contract_or_source_profile_runner.py"


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
        ("SRC3978_00_3977_next", SRC / "P8_Y5_R2FR_3977_NEXT_TARGET.csv", "NEXT3977_0", "3977 handoff"),
        ("SRC3978_01_3977_target", SRC / "P8_Y5_R2FR_3977_ANGULAR_MOMENT_SILENCE_THEOREM.csv", "ANG3977_0_target", "angular moment silence target"),
        ("SRC3978_02_3977_source_route", SRC / "P8_Y5_R2FR_3977_ANGULAR_MOMENT_SILENCE_THEOREM.csv", "ANG3977_1_source_route", "source zero route"),
        ("SRC3978_03_3977_poynting_guard", SRC / "P8_Y5_R2FR_3977_ANGULAR_MOMENT_SILENCE_THEOREM.csv", "ANG3977_4_poynting_guard", "Poynting guard"),
        ("SRC3978_04_3977_certificate", SRC / "P8_Y5_R2FR_3977_ANGULAR_MOMENT_SILENCE_THEOREM.csv", "ANG3977_6_certificate", "angular silence certificate"),
        ("SRC3978_05_3977_decomp_source", SRC / "P8_Y5_R2FR_3977_MULTIPOLE_PROFILE_DECOMPOSITION.csv", "MPD3977_0_source_residual", "source residual decomposition"),
        ("SRC3978_06_3977_GR_route", SRC / "P8_Y5_R2FR_3977_MULTIPOLE_PROFILE_DECOMPOSITION.csv", "MPD3977_3_GR_multipole_routing", "GR multipole routing"),
        ("SRC3978_07_3977_source_bound", SRC / "P8_Y5_R2FR_3977_MULTIPOLE_PROFILE_BOUND_ROWS.csv", "MPB3977_0_source_profile", "source profile bound"),
        ("SRC3978_08_3977_extra_bound", SRC / "P8_Y5_R2FR_3977_MULTIPOLE_PROFILE_BOUND_ROWS.csv", "MPB3977_3_GR_baseline_route", "extra MTS residual route"),
        ("SRC3978_09_3977_closed_source", SRC / "P8_Y5_R2FR_3977_Z_ANGULAR_MOMENT_SILENCE_UPDATE.csv", "ZANG3977_0_closed_source", "closed total source certificate"),
        ("SRC3978_10_3977_tensor_virial", SRC / "P8_Y5_R2FR_3977_Z_ANGULAR_MOMENT_SILENCE_UPDATE.csv", "ZANG3977_1_tensor_virial", "tensor virial certificate"),
        ("SRC3978_11_3977_poynting_cert", SRC / "P8_Y5_R2FR_3977_Z_ANGULAR_MOMENT_SILENCE_UPDATE.csv", "ZANG3977_2_poynting", "Poynting total-source certificate"),
        ("SRC3978_12_3977_GR_cert", SRC / "P8_Y5_R2FR_3977_Z_ANGULAR_MOMENT_SILENCE_UPDATE.csv", "ZANG3977_5_GR_route", "GR multipole routing certificate"),
        ("SRC3978_13_3831_ext", SRC / "P8_Y5_R2FR_3831_SIGMATF_MATTER_DECOMPOSITION.csv", "SIGMATF3831_0_exterior_material", "exterior material term"),
        ("SRC3978_14_3831_virial", SRC / "P8_Y5_R2FR_3831_SIGMATF_MATTER_DECOMPOSITION.csv", "SIGMATF3831_1_tensor_virial", "tensor virial term"),
        ("SRC3978_15_3831_quad", SRC / "P8_Y5_R2FR_3831_SIGMATF_MATTER_DECOMPOSITION.csv", "SIGMATF3831_2_quadrupole_multipole", "quadrupole term"),
        ("SRC3978_16_3831_poynting", SRC / "P8_Y5_R2FR_3831_SIGMATF_MATTER_DECOMPOSITION.csv", "SIGMATF3831_3_EM_Poynting", "EM/Poynting term"),
        ("SRC3978_17_3831_apparatus", SRC / "P8_Y5_R2FR_3831_SIGMATF_MATTER_DECOMPOSITION.csv", "SIGMATF3831_4_apparatus_binding", "apparatus term"),
        ("SRC3978_18_3831_closed", SRC / "P8_Y5_R2FR_3831_TENSOR_VIRIAL_NO_SLIP_CONDITIONS.csv", "TV3831_0_closed_total_source", "closed source condition"),
        ("SRC3978_19_3831_stationary", SRC / "P8_Y5_R2FR_3831_TENSOR_VIRIAL_NO_SLIP_CONDITIONS.csv", "TV3831_1_stationary_TF_inertia", "stationary inertia condition"),
        ("SRC3978_20_3831_surface", SRC / "P8_Y5_R2FR_3831_TENSOR_VIRIAL_NO_SLIP_CONDITIONS.csv", "TV3831_2_surface_exchange_silence", "surface exchange condition"),
        ("SRC3978_21_3831_EM", SRC / "P8_Y5_R2FR_3831_TENSOR_VIRIAL_NO_SLIP_CONDITIONS.csv", "TV3831_3_EM_radiation_separation", "EM/radiation condition"),
        ("SRC3978_22_3831_tf_theorem", SRC / "P8_Y5_R2FR_3831_TRACeless_STRESS_OPERATOR_THEOREM.csv", "TF3831_2_tensor_virial_average", "tensor virial average theorem"),
        ("SRC3978_23_3831_tf_bound", SRC / "P8_Y5_R2FR_3831_TRACeless_STRESS_OPERATOR_THEOREM.csv", "TF3831_3_gamma_bound_from_TF_source", "TF source bound"),
        ("SRC3978_24_3930_total_system", SRC / "P8_Y5_R2FR_3930_POYNTING_BOUNDARY_GUARD.csv", "PYG3930_0_total_system", "total Hilbert/Maxwell source guard"),
        ("SRC3978_25_3930_internal_flow", SRC / "P8_Y5_R2FR_3930_POYNTING_BOUNDARY_GUARD.csv", "PYG3930_1_internal_flow_allowed", "internal Poynting allowed guard"),
        ("SRC3978_26_3930_no_em_overclaim", SRC / "P8_Y5_R2FR_3930_POYNTING_BOUNDARY_GUARD.csv", "PYG3930_2_no_em_overclaim", "no EM-origin overclaim guard"),
        ("SRC3978_27_3930_flux", SRC / "P8_Y5_R2FR_3930_BOUNDARY_HARMONIC_ZERO_RESULT.csv", "BHZ3930_2_Phi_B", "closed boundary flux zero route"),
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
            "theorem_id": "CST3978_0_target",
            "claim_piece": "source residual angular zero",
            "mathematical_form": "Z_source_Q_zero => Q_lm^source,res = 0 for l>=1",
            "derivation": "if a single compact worldtube contains matter, EM field energy, binding, apparatus/exchange stresses, and the descended MTS source contribution, and if its total stress balance has no boundary flux, then the source residual must be computed from the total conserved system rather than a matter-only subset",
            "status": "CONDITIONAL_ZERO_THEOREM_SHAPE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CST3978_1_tensor_virial",
            "claim_piece": "integrated TF stress suppression",
            "mathematical_form": "d2I_TF/dt2 = 2 int_W T_TF^tot d3x + surface_TF + exchange_TF",
            "derivation": "stationary or time-averaged closed total source with surface_TF=exchange_TF=0 gives int_W T_TF^tot d3x=0; this can kill the integrated stress residual, not arbitrary mass multipoles",
            "status": "DERIVED_CONDITIONAL_AVERAGE_ZERO_NOT_POINTWISE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CST3978_2_poynting_inclusion",
            "claim_piece": "EM/Poynting inclusion",
            "mathematical_form": "T_tot = T_matter + T_EM + T_binding + T_apparatus + T_MTS_source, with int_boundary T_tot^{i nu} n_i dS=0",
            "derivation": "internal S_EM circulation is allowed; only the total boundary flux is required to vanish. Omitting T_EM makes epsilon_EM_Poynting_TF an active residual",
            "status": "POYNTING_INCLUDED_OR_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CST3978_3_GR_multipole_guard",
            "claim_piece": "ordinary GR multipoles are not MTS failures",
            "mathematical_form": "Q_lm^source,res := P_residual[Q_lm^total - Q_lm^GR_baseline]",
            "derivation": "tensor virial does not erase real quadrupole/tidal structure; standard GR multipoles must be routed into the comparator metric before testing extra MTS hair",
            "status": "GR_BASELINE_ROUTING_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CST3978_4_no_broad_source_zero",
            "claim_piece": "broad source zero refusal",
            "mathematical_form": "closed total source + tensor virial does not imply pointwise T_TF=0 and does not imply every Q_lm^mass=0",
            "derivation": "the only honest zero is residual source hair after total-system inclusion, boundary silence, time averaging, and GR-baseline subtraction",
            "status": "BROAD_ZERO_REJECTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CST3978_5_certificate",
            "claim_piece": "source zero certificate",
            "mathematical_form": "Z_source_Q_zero = Z_closed_worldtube * Z_total_balance * Z_stationary_TF_virial * Z_surface_exchange_zero * Z_Poynting_included * Z_GR_multipole_routing * Z_exterior_vacuum_annulus",
            "derivation": "if this product closes, epsilon_source_l_ge_1 can be theorem-zero for residual MTS hair; otherwise source profile acquisition is required",
            "status": "CERTIFICATE_DEFINED_CURRENTLY_FALSE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CST3978_6_current_verdict",
            "claim_piece": "current source-side status",
            "mathematical_form": "current corpus supports the theorem shape and the fair residual definition, but not all parent-owned certificate factors",
            "derivation": "profile rows must be staged for Q_lm^total, Q_lm^GR_baseline, Q_lm^residual, Poynting flux, and virial terms",
            "status": "PROFILE_ACQUISITION_REQUIRED_UNLESS_CERTIFICATE_CLOSES",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def poynting_contract_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "PIC3978_0_total_source",
            "requirement": "source stress must be total Hilbert/Maxwell source, not matter-only",
            "mathematical_test": "T_tot includes T_matter, T_EM, binding, apparatus/exchange, and any descended MTS source stress in the same worldtube W",
            "if_missing": "retain epsilon_EM_Poynting_TF + epsilon_apparatus_TF + epsilon_tensor_virial_TF",
            "current_status": "UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "PIC3978_1_boundary_flux",
            "requirement": "closed total boundary flux",
            "mathematical_test": "int_boundary(W) T_tot^{i nu} n_i dS = 0 on the claimed averaging/readout interval",
            "if_missing": "retain surface_TF + exchange_TF + Phi_B source terms",
            "current_status": "CONDITIONAL_FROM_PRIVATE_BOUNDARY_BRANCH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "PIC3978_2_internal_flow_allowed",
            "requirement": "do not set internal Poynting to zero pointwise",
            "mathematical_test": "S_EM may circulate inside W; only total boundary flux and residual TF projection are constrained",
            "if_missing": "overclaim risk: deleting real EM angular momentum/stress by gauge or tube choice",
            "current_status": "GUARD_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "PIC3978_3_radiation",
            "requirement": "radiative EM/gravitational flux absent, included, or bounded",
            "mathematical_test": "radiative stress crossing W is zero, part of T_tot with no net boundary flux, or numerically bounded as epsilon_rad_TF",
            "if_missing": "retain epsilon_EM_Poynting_TF and epsilon_radiative_flux_TF",
            "current_status": "UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "contract_id": "PIC3978_4_no_charge_claim",
            "requirement": "Poynting inclusion is not an EM unification proof",
            "mathematical_test": "does not derive charge normalization, alpha, Maxwell emergence, or Coulomb law; it only prevents false deletion of EM stress in local GR reduction",
            "if_missing": "overclaim risk",
            "current_status": "GUARD_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def schema_rows(timestamp: str) -> list[dict[str, Any]]:
    fields = [
        ("source_id", "string", "stable row id for the source/profile"),
        ("arena", "string", "R10/PPN/clock/orbital/lab source context"),
        ("l", "integer", "spherical harmonic degree, l>=1 for active residual rows"),
        ("m", "integer", "spherical harmonic order"),
        ("Q_lm_total", "numeric_or_symbolic", "total source multipole before GR subtraction"),
        ("Q_lm_GR_baseline", "numeric_or_symbolic", "same-source GR comparator multipole"),
        ("Q_lm_residual", "numeric_or_symbolic", "P_residual(Q_lm_total-Q_lm_GR_baseline)"),
        ("M_H_ref", "numeric", "normalizing source/Hilbert mass scale"),
        ("r_eval", "numeric", "readout/evaluation radius if needed by bound"),
        ("worldtube_definition", "string", "what is included in W"),
        ("includes_matter", "bool", "matter included in total source"),
        ("includes_EM", "bool", "EM field/Poynting included in total source"),
        ("includes_binding", "bool", "binding/internal stress included"),
        ("includes_apparatus", "bool", "apparatus/exchange stress included or excluded by projection"),
        ("boundary_flux_TF", "numeric_or_symbolic", "surface/exchange/radiative TF boundary term"),
        ("d2I_TF_dt2", "numeric_or_symbolic", "stationary/time-averaged TF inertia term"),
        ("GR_routing_flag", "bool", "ordinary GR multipole routed before residual test"),
        ("units", "string", "units of multipole and normalizer"),
        ("frame_or_coframe", "string", "declared frame/coframe used by profile"),
        ("source_path", "path", "local/web source for numeric/profile row"),
        ("valid_for_claim", "bool", "false unless all numeric/source/certificate checks pass"),
    ]
    return [
        {
            "schema_id": f"SPS3978_{idx:02d}_{name}",
            "field": name,
            "type": field_type,
            "meaning": meaning,
            "required_for_claim": True,
            "current_status": "SCHEMA_READY_VALUE_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for idx, (name, field_type, meaning) in enumerate(fields)
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "SRB3978_0_source_total",
            "epsilon_source_l_ge_1",
            "epsilon_source_l_ge_1 <= epsilon_closed_source_failure + epsilon_tensor_virial_TF + epsilon_quad_residual_TF + epsilon_EM_Poynting_TF + epsilon_apparatus_TF",
            "dimensionless",
            "Z_source_Q_zero=1 or source profile rows populated",
            "MPB3977_0_source_profile",
        ),
        (
            "SRB3978_1_closed_failure",
            "epsilon_closed_source_failure",
            "(|surface_TF|+|exchange_TF|+|boundary_flux_TF|)/M_H_ref",
            "dimensionless",
            "closed total worldtube and no boundary/exchange flux",
            "Z_closed_worldtube and Z_total_balance",
        ),
        (
            "SRB3978_2_virial",
            "epsilon_tensor_virial_TF",
            "||d2I_TF/dt2 + surface_TF + exchange_TF||/(M c^2)",
            "dimensionless",
            "stationary/time-averaged tensor virial data",
            "Z_stationary_TF_virial",
        ),
        (
            "SRB3978_3_poynting",
            "epsilon_EM_Poynting_TF",
            "sup ||P_TF T_EM + S_i S_j/c^2||/(rho_source c^2) or closed-source cancellation certificate",
            "dimensionless",
            "EM/Poynting inclusion or numeric field-stress bound",
            "Z_Poynting_included",
        ),
        (
            "SRB3978_4_quad_residual",
            "epsilon_quad_residual_TF",
            "C_Q |Q_TF_total-Q_TF_GR_baseline|/(M r^2)",
            "dimensionless",
            "same-source GR baseline multipole subtraction",
            "Z_GR_multipole_routing",
        ),
        (
            "SRB3978_5_apparatus",
            "epsilon_apparatus_TF",
            "||P_TF T_apparatus||/(M_source c^2) unless included in closed source or outside projection",
            "dimensionless",
            "apparatus inclusion/exclusion certificate",
            "Z_closed_worldtube",
        ),
        (
            "SRB3978_6_extra_MTS",
            "epsilon_extra_MTS_l_ge_1",
            "||P_residual(Q_lm_total-Q_lm_GR_baseline)||/M_H_ref",
            "dimensionless",
            "residual projector and source profile runner",
            "MPB3977_3_GR_baseline_route",
        ),
    ]
    return [
        {
            "bound_id": bound_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "required_input_or_theorem": requirement,
            "feeds_or_blocks": feeds,
            "current_status": "BOUND_READY_VALUES_OR_ZERO_CERTIFICATE_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for bound_id, symbol, formula, units, requirement, feeds in specs
    ]


def certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ZSRC3978_0_worldtube", "Z_closed_worldtube", "one worldtube includes every stress/field/exchange component relevant to the source residual", "required", "UNSIGNED", "epsilon_closed_source_failure"),
        ("ZSRC3978_1_balance", "Z_total_balance", "total stress balance or conservation law has no unaccounted boundary/exchange flux", "required", "UNSIGNED", "epsilon_closed_source_failure"),
        ("ZSRC3978_2_virial", "Z_stationary_TF_virial", "d2I_TF/dt2=0 after declared averaging and surface/exchange terms vanish", "required", "UNSIGNED", "epsilon_tensor_virial_TF"),
        ("ZSRC3978_3_surface", "Z_surface_exchange_zero", "surface_TF=exchange_TF=boundary_flux_TF=0 in the same branch", "required", "PARTIAL_PRIVATE_BOUNDARY_BRANCH_ONLY", "epsilon_closed_source_failure"),
        ("ZSRC3978_4_poynting", "Z_Poynting_included", "T_EM and S_EM are included in T_tot or a sourced Poynting bound is supplied", "required", "UNSIGNED", "epsilon_EM_Poynting_TF"),
        ("ZSRC3978_5_GR", "Z_GR_multipole_routing", "ordinary GR multipoles are subtracted/routed before residual MTS hair is tested", "required", "DEFINED_NOT_IMPLEMENTED", "epsilon_quad_residual_TF"),
        ("ZSRC3978_6_exterior", "Z_exterior_vacuum_annulus", "readout annulus excludes ordinary matter/apparatus/radiative support or bounds it", "required", "UNSIGNED", "epsilon_ext_TF"),
        ("ZSRC3978_7_total", "Z_source_Q_zero", "product of closed worldtube, total balance, virial, surface, Poynting, GR routing, and exterior-vacuum certificates", "total", "FALSE_UNTIL_ALL_FACTORS_SIGNED", "epsilon_source_l_ge_1"),
    ]
    return [
        {
            "certificate_id": certificate_id,
            "factor": factor,
            "requirement": requirement,
            "role": role,
            "current_status": status,
            "feeds_or_blocks": feeds,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for certificate_id, factor, requirement, role, status, feeds in specs
    ]


def feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "feed_id": "CSF3978_0_source_zero",
            "target": "epsilon_source_l_ge_1",
            "update": "source zero now requires Z_source_Q_zero; otherwise source profile rows are mandatory",
            "effect": "prevents closed-source language from hiding Poynting/apparatus/boundary exchange",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "CSF3978_1_poynting",
            "target": "epsilon_EM_Poynting_TF",
            "update": "Poynting is included in total stress or retained as a finite residual; internal flow is allowed",
            "effect": "answers the Poynting-vector fork without cheating Maxwell stress away",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "CSF3978_2_GR_route",
            "target": "epsilon_extra_MTS_l_ge_1",
            "update": "ordinary GR quadrupoles/tides must be comparator-routed before residual source hair is tested",
            "effect": "keeps MTS judged against GR fairly instead of punishing shared multipoles",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "CSF3978_3_SO3",
            "target": "Z_SO3_boundary",
            "update": "source-side angular silence can feed SO3 only through Z_source_Q_zero",
            "effect": "SO3 remains blocked until source residual channel closes or is bounded",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "CSF3978_4_PPN",
            "target": "Delta_PPN_source_abs",
            "update": "source Poynting/virial/GR-routing residuals enter the local PPN residual vector",
            "effect": "local GR branch gets a concrete source residual contract",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "CSF3978_5_next",
            "target": "GR_baseline_residual_projector",
            "update": f"move to {NEXT_DOC}",
            "effect": "build the exact projector/runner needed to turn profile rows into real tests",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3978_0_derivation",
            "decision": "derive source-side zero theorem shape",
            "status": "CONDITIONAL_ZERO_THEOREM_SHAPE_READY",
            "reason": "tensor virial plus total stress balance can suppress integrated residual TF stress only under closed total-system conditions",
            "next_action": "do not claim zero until all Z_source_Q_zero factors are signed",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3978_1_poynting",
            "decision": "include Poynting rather than delete it",
            "status": "POYNTING_INCLUDED_OR_BOUND_REQUIRED",
            "reason": "EM stress and internal S_EM flow are real source channels; matter-only tubes falsely remove them",
            "next_action": "retain epsilon_EM_Poynting_TF unless total-source inclusion is signed",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3978_2_quad",
            "decision": "do not use tensor virial to erase GR multipoles",
            "status": "GR_BASELINE_ROUTING_REQUIRED",
            "reason": "real mass quadrupoles/tides are allowed in GR and must be subtracted before testing extra MTS residual hair",
            "next_action": "build GR baseline residual projector",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3978_3_profile",
            "decision": "stage source profile acquisition schema",
            "status": "PROFILE_SCHEMA_READY_VALUES_MISSING",
            "reason": "the certificate is not signed for real arenas, so the fallback needs actual Q_lm/Poynting/virial rows",
            "next_action": NEXT_DOC,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3978_0_source_zero",
            "gate": "source residual zero",
            "requirement": "Z_source_Q_zero=1 or all source profile bounds populated and below threshold",
            "status": "BLOCKED_CERTIFICATE_AND_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3978_1_poynting",
            "gate": "Poynting/EM stress",
            "requirement": "T_EM/S_EM included in closed total source or epsilon_EM_Poynting_TF sourced numerically",
            "status": "BLOCKED_POYNTING_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3978_2_GR_route",
            "gate": "fair GR baseline",
            "requirement": "same-source GR multipoles routed/subtracted before residual MTS hair is judged",
            "status": "BLOCKED_PROJECTOR_NOT_IMPLEMENTED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3978_3_local_GR",
            "gate": "local GR",
            "requirement": "source zero/profile plus boundary/external/angular and PPN gates",
            "status": "LOCAL_GR_STILL_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3978_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "define and dry-run the GR-baseline residual projector P_residual(Q_lm_total-Q_lm_GR_baseline), then create the first source profile runner rows",
            "success_condition": "ordinary GR multipoles are separated from extra MTS residual hair with a parseable schema and nonclaim smoke rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "CLOSED_SOURCE_TENSOR_VIRIAL_POYNTING_CONTRACT_AND_PROFILE_SCHEMA_READY",
            "sources_found": found,
            "sources_total": len(sources),
            "main_result": "source-side Q_lm residual can be theorem-zero only under a closed total-system tensor-virial branch with EM/Poynting included and GR multipoles routed into the comparator; current corpus does not sign every factor, so source profile acquisition rows are staged",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, sources: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return f"""# 3978 - Closed Total Source Tensor-Virial Poynting Inclusion Or Multipole Profile Acquisition

Timestamp: `{timestamp}`

## Result

3978 takes the source-side route seriously.

The strongest honest zero certificate is:

```text
Z_source_Q_zero =
  Z_closed_worldtube
* Z_total_balance
* Z_stationary_TF_virial
* Z_surface_exchange_zero
* Z_Poynting_included
* Z_GR_multipole_routing
* Z_exterior_vacuum_annulus

Z_source_Q_zero = 1
=> Q_lm^source,res = 0 for l >= 1
```

## What This Actually Proves

Tensor virial can suppress the integrated tracefree stress residual of a closed stationary total source:

```text
d2I_TF/dt2 = 2 int_W T_TF^tot d3x + surface_TF + exchange_TF
```

So if `d2I_TF/dt2=0` and the surface/exchange terms vanish, `int_W T_TF^tot d3x=0`.

That does **not** erase real GR mass quadrupoles. Those must be routed into the GR comparator before judging extra MTS residual hair:

```text
Q_lm^source,res := P_residual(Q_lm^total - Q_lm^GR_baseline)
```

## Poynting Decision

The Poynting vector is not deleted. It is either included inside the closed total Hilbert/Maxwell source or retained as:

```text
epsilon_EM_Poynting_TF
```

Internal `S_EM` circulation is allowed. Only the total boundary flux is constrained.

## Fallback Bound

Until the certificate is parent-signed:

```text
epsilon_source_l_ge_1 <=
  epsilon_closed_source_failure
+ epsilon_tensor_virial_TF
+ epsilon_quad_residual_TF
+ epsilon_EM_Poynting_TF
+ epsilon_apparatus_TF
```

No local-GR, SO3, or EM-origin claim is made.

Next target:

```text
{NEXT_DOC}
```

Source needles found: `{found}/{len(sources)}`.
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3978 - Closed Total Source Tensor-Virial Poynting Inclusion

- Timestamp: `{timestamp}`
- Status: `CLOSED_SOURCE_TENSOR_VIRIAL_POYNTING_CONTRACT_AND_PROFILE_SCHEMA_READY`
- Strongest source zero certificate:
  `Z_source_Q_zero = Z_closed_worldtube * Z_total_balance * Z_stationary_TF_virial * Z_surface_exchange_zero * Z_Poynting_included * Z_GR_multipole_routing * Z_exterior_vacuum_annulus`.
- Conditional consequence:
  `Z_source_Q_zero=1 => Q_lm^source,res=0` for `l>=1`.
- Guard:
  tensor virial suppresses integrated residual TF stress; it does not erase real GR mass quadrupoles.
- Poynting route:
  `S_EM` is included in the total Hilbert/Maxwell source or retained as `epsilon_EM_Poynting_TF`; internal flow is allowed.
- Fallback:
  `epsilon_source_l_ge_1 <= epsilon_closed_source_failure + epsilon_tensor_virial_TF + epsilon_quad_residual_TF + epsilon_EM_Poynting_TF + epsilon_apparatus_TF`.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3978 - Closed Total Source Tensor-Virial Poynting Inclusion"
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
    return {
        "sources": sources,
        "theorem": theorem_rows(timestamp),
        "poynting": poynting_contract_rows(timestamp),
        "schema": schema_rows(timestamp),
        "bounds": bound_rows(timestamp),
        "certificate": certificate_rows(timestamp),
        "feed": feed_rows(timestamp),
        "decision": decision_rows(timestamp),
        "claim_gate": claim_gate_rows(timestamp),
        "next": next_rows(timestamp),
        "status": status_rows(timestamp, sources),
    }


def validation_rows(timestamp: str, rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = rows["sources"]
    theorem = rows["theorem"]
    poynting = rows["poynting"]
    schema = rows["schema"]
    bounds = rows["bounds"]
    certificate = rows["certificate"]
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

    theorem_statuses = {row["status"] for row in theorem}
    theorem_pieces = {row["claim_piece"] for row in theorem}
    poynting_requirements = {row["requirement"] for row in poynting}
    schema_fields = {row["field"] for row in schema}
    bound_symbols = {row["symbol"] for row in bounds}
    certificate_factors = {row["factor"] for row in certificate}
    feed_targets = {row["target"] for row in feed}
    decision_statuses = {row["status"] for row in decisions}
    claim_statuses = {row["status"] for row in claims}

    required_schema = {
        "source_id",
        "arena",
        "l",
        "m",
        "Q_lm_total",
        "Q_lm_GR_baseline",
        "Q_lm_residual",
        "M_H_ref",
        "worldtube_definition",
        "includes_EM",
        "boundary_flux_TF",
        "d2I_TF_dt2",
        "GR_routing_flag",
        "source_path",
        "valid_for_claim",
    }

    return [
        val("VAL3978_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3978_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3978_02_theorem_shape", {"CONDITIONAL_ZERO_THEOREM_SHAPE", "DERIVED_CONDITIONAL_AVERAGE_ZERO_NOT_POINTWISE", "POYNTING_INCLUDED_OR_BOUND_REQUIRED", "GR_BASELINE_ROUTING_REQUIRED", "BROAD_ZERO_REJECTED", "CERTIFICATE_DEFINED_CURRENTLY_FALSE", "PROFILE_ACQUISITION_REQUIRED_UNLESS_CERTIFICATE_CLOSES"} <= theorem_statuses, "source theorem, virial limit, Poynting route, GR guard, broad-zero refusal, certificate, and profile verdict present"),
        val("VAL3978_03_theorem_pieces", {"source residual angular zero", "integrated TF stress suppression", "EM/Poynting inclusion", "ordinary GR multipoles are not MTS failures", "source zero certificate"} <= theorem_pieces, "theorem covers source zero, virial, Poynting, GR routing, and certificate"),
        val("VAL3978_04_poynting_contract", {"source stress must be total Hilbert/Maxwell source, not matter-only", "closed total boundary flux", "do not set internal Poynting to zero pointwise", "Poynting inclusion is not an EM unification proof"} <= poynting_requirements, "Poynting contract blocks matter-only deletion and EM overclaim"),
        val("VAL3978_05_schema", required_schema <= schema_fields, "source profile schema has required Q_lm, worldtube, Poynting, virial, routing, and provenance fields"),
        val("VAL3978_06_bounds", {"epsilon_source_l_ge_1", "epsilon_closed_source_failure", "epsilon_tensor_virial_TF", "epsilon_EM_Poynting_TF", "epsilon_quad_residual_TF", "epsilon_apparatus_TF", "epsilon_extra_MTS_l_ge_1"} <= bound_symbols, "source residual bound rows present"),
        val("VAL3978_07_certificate", {"Z_closed_worldtube", "Z_total_balance", "Z_stationary_TF_virial", "Z_surface_exchange_zero", "Z_Poynting_included", "Z_GR_multipole_routing", "Z_exterior_vacuum_annulus", "Z_source_Q_zero"} <= certificate_factors, "Z_source_Q_zero factors present"),
        val("VAL3978_08_feed", {"epsilon_source_l_ge_1", "epsilon_EM_Poynting_TF", "epsilon_extra_MTS_l_ge_1", "Z_SO3_boundary", "Delta_PPN_source_abs", "GR_baseline_residual_projector"} <= feed_targets, "feeds reach source, Poynting, GR residual, SO3, PPN, and next projector target"),
        val("VAL3978_09_decision", {"CONDITIONAL_ZERO_THEOREM_SHAPE_READY", "POYNTING_INCLUDED_OR_BOUND_REQUIRED", "GR_BASELINE_ROUTING_REQUIRED", "PROFILE_SCHEMA_READY_VALUES_MISSING"} <= decision_statuses, "decision gate records derivation, Poynting inclusion, GR routing, and profile fallback"),
        val("VAL3978_10_claim_gate", {"BLOCKED_CERTIFICATE_AND_VALUES_MISSING", "BLOCKED_POYNTING_UNSIGNED", "BLOCKED_PROJECTOR_NOT_IMPLEMENTED", "LOCAL_GR_STILL_OPEN"} <= claim_statuses, "claim gates block source zero, Poynting, projector, and local GR"),
        val("VAL3978_11_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to GR baseline residual projector/source profile runner"),
        val("VAL3978_12_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3978_13_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3978_14_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3978_15_spine_updated", SPINE_PATH.exists() and "3978 - Closed Total Source Tensor-Virial Poynting Inclusion" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3978_16_csv_parse", parsed, parse_detail),
        val("VAL3978_17_script_compile", True, "script compiled before validation write"),
        val("VAL3978_18_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
        val("VAL3978_19_fair_comparator_guard", any(row["symbol"] == "epsilon_quad_residual_TF" for row in bounds), "quadrupole term is residual after GR baseline, not a blanket MTS penalty"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["theorem"], rows["theorem"])
    write_csv(OUTPUTS["poynting"], rows["poynting"])
    write_csv(OUTPUTS["schema"], rows["schema"])
    write_csv(OUTPUTS["bounds"], rows["bounds"])
    write_csv(OUTPUTS["certificate"], rows["certificate"])
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
        raise SystemExit(f"3978 validation failed: {failed}")

    print(f"3978 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("Closed-source tensor-virial/Poynting contract and source profile schema assembled")


if __name__ == "__main__":
    run()

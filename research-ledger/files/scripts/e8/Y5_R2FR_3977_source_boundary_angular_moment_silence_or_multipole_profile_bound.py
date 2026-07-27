from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3977"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3977-Y5-R2FR-source-boundary-angular-moment-silence-or-multipole-profile-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3977_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3977_ANGULAR_MOMENT_SILENCE_THEOREM.csv",
    "decomposition": SRC / "P8_Y5_R2FR_3977_MULTIPOLE_PROFILE_DECOMPOSITION.csv",
    "bounds": SRC / "P8_Y5_R2FR_3977_MULTIPOLE_PROFILE_BOUND_ROWS.csv",
    "certificate": SRC / "P8_Y5_R2FR_3977_Z_ANGULAR_MOMENT_SILENCE_UPDATE.csv",
    "feed": SRC / "P8_Y5_R2FR_3977_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3977_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3977_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3977_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3977_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3977_VALIDATION.csv",
}

NEXT_DOC = "3978-Y5-R2FR-closed-total-source-tensor-virial-poynting-inclusion-or-multipole-profile-acquisition.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3978_closed_total_source_tensor_virial_poynting_inclusion_or_multipole_profile_acquisition.py"


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
        ("SRC3977_00_3976_next", SRC / "P8_Y5_R2FR_3976_NEXT_TARGET.csv", "NEXT3976_0", "3976 handoff"),
        ("SRC3977_01_3976_source_moments", SRC / "P8_Y5_R2FR_3976_PARENT_SO3_BOUNDARY_SYMMETRY_THEOREM.csv", "SO3T3976_1_source_moments", "SO3 source/boundary/external moment requirement"),
        ("SRC3977_02_3976_counterguard", SRC / "P8_Y5_R2FR_3976_PARENT_SO3_BOUNDARY_SYMMETRY_THEOREM.csv", "SO3T3976_4_counterguard", "stationary/spherical shortcut guard"),
        ("SRC3977_03_3976_verdict", SRC / "P8_Y5_R2FR_3976_PARENT_SO3_BOUNDARY_SYMMETRY_THEOREM.csv", "SO3T3976_5_current_verdict", "SO3 not closed verdict"),
        ("SRC3977_04_3976_source_audit", SRC / "P8_Y5_R2FR_3976_SO3_PARENT_SIGNATURE_AUDIT.csv", "SO3A3976_1_source_moments", "source moment audit"),
        ("SRC3977_05_3976_boundary_audit", SRC / "P8_Y5_R2FR_3976_SO3_PARENT_SIGNATURE_AUDIT.csv", "SO3A3976_2_boundary_moments", "boundary moment audit"),
        ("SRC3977_06_3976_external_audit", SRC / "P8_Y5_R2FR_3976_SO3_PARENT_SIGNATURE_AUDIT.csv", "SO3A3976_3_external_tides", "external tide audit"),
        ("SRC3977_07_3976_source_bound", SRC / "P8_Y5_R2FR_3976_MULTIPOLE_HAIR_BOUND_ROWS.csv", "MHB3976_0_source_multipole", "source multipole bound row"),
        ("SRC3977_08_3976_boundary_bound", SRC / "P8_Y5_R2FR_3976_MULTIPOLE_HAIR_BOUND_ROWS.csv", "MHB3976_1_boundary_multipole", "boundary multipole bound row"),
        ("SRC3977_09_3976_total_bound", SRC / "P8_Y5_R2FR_3976_MULTIPOLE_HAIR_BOUND_ROWS.csv", "MHB3976_6_total_SO3_failure", "total SO3 failure bound"),
        ("SRC3977_10_3831_ext", SRC / "P8_Y5_R2FR_3831_SIGMATF_MATTER_DECOMPOSITION.csv", "SIGMATF3831_0_exterior_material", "exterior material TF component"),
        ("SRC3977_11_3831_virial", SRC / "P8_Y5_R2FR_3831_SIGMATF_MATTER_DECOMPOSITION.csv", "SIGMATF3831_1_tensor_virial", "tensor virial TF component"),
        ("SRC3977_12_3831_quad", SRC / "P8_Y5_R2FR_3831_SIGMATF_MATTER_DECOMPOSITION.csv", "SIGMATF3831_2_quadrupole_multipole", "quadrupole leakage component"),
        ("SRC3977_13_3831_poynting", SRC / "P8_Y5_R2FR_3831_SIGMATF_MATTER_DECOMPOSITION.csv", "SIGMATF3831_3_EM_Poynting", "EM/Poynting TF component"),
        ("SRC3977_14_3831_apparatus", SRC / "P8_Y5_R2FR_3831_SIGMATF_MATTER_DECOMPOSITION.csv", "SIGMATF3831_4_apparatus_binding", "apparatus TF component"),
        ("SRC3977_15_3831_closed", SRC / "P8_Y5_R2FR_3831_TENSOR_VIRIAL_NO_SLIP_CONDITIONS.csv", "TV3831_0_closed_total_source", "closed total source condition"),
        ("SRC3977_16_3831_surface", SRC / "P8_Y5_R2FR_3831_TENSOR_VIRIAL_NO_SLIP_CONDITIONS.csv", "TV3831_2_surface_exchange_silence", "surface/exchange silence condition"),
        ("SRC3977_17_3831_EM", SRC / "P8_Y5_R2FR_3831_TENSOR_VIRIAL_NO_SLIP_CONDITIONS.csv", "TV3831_3_EM_radiation_separation", "EM/radiation separation condition"),
        ("SRC3977_18_3831_operator", SRC / "P8_Y5_R2FR_3831_TRACeless_STRESS_OPERATOR_THEOREM.csv", "TF3831_3_gamma_bound_from_TF_source", "TF source bound contract"),
        ("SRC3977_19_3930_boundary_zero", SRC / "P8_Y5_R2FR_3930_BOUNDARY_HARMONIC_ZERO_RESULT.csv", "BHZ3930_1_B_harmonic_boundary", "boundary harmonic zero route"),
        ("SRC3977_20_3930_flux_zero", SRC / "P8_Y5_R2FR_3930_BOUNDARY_HARMONIC_ZERO_RESULT.csv", "BHZ3930_2_Phi_B", "boundary flux zero route"),
        ("SRC3977_21_3930_wall_zero", SRC / "P8_Y5_R2FR_3930_BOUNDARY_HARMONIC_ZERO_RESULT.csv", "BHZ3930_3_tau_wall_TF", "wall/shear zero route"),
        ("SRC3977_22_3930_fallback", SRC / "P8_Y5_R2FR_3930_BOUNDARY_HARMONIC_FALLBACK_ROWS.csv", "BFB3930_4_total", "boundary harmonic fallback"),
        ("SRC3977_23_3930_poynting_guard", SRC / "P8_Y5_R2FR_3930_POYNTING_BOUNDARY_GUARD.csv", "PYG3930_0_total_system", "total-system Poynting guard"),
        ("SRC3977_24_3931_history", SRC / "P8_Y5_R2FR_3931_HISTORY_SUPPRESSION_BOUND_ROWS.csv", "HSB3931_4_total", "history/nonlocal fallback"),
        ("SRC3977_25_3929_domain", SRC / "P8_Y5_R2FR_3929_ACTIVE_PROJECTOR_FALLBACK_ROWS.csv", "FB3929_4_total", "domain/projector fallback"),
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
            "theorem_id": "ANG3977_0_target",
            "claim_piece": "angular moment silence",
            "mathematical_form": "Q_lm^source = B_lm^boundary = E_lm^external = 0 for all l >= 1 before residual local readout",
            "conditional_derivation": "if the parent local branch supplies a closed total source, an exact exterior vacuum annulus, tensor-virial silence, isolated boundary/collar flux silence, no external tide, Poynting included in the total Hilbert/Maxwell source, and ordinary GR multipoles routed to the metric baseline, then residual angular moments vanish",
            "status": "CONDITIONAL_THEOREM_SHAPE_WRITTEN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "ANG3977_1_source_route",
            "claim_piece": "source multipole silence",
            "mathematical_form": "Q_lm^source,res = 0 for l>=1 if epsilon_ext_TF=epsilon_tensor_virial_TF=epsilon_quad_TF=epsilon_EM_Poynting_TF=epsilon_apparatus_TF=0 after GR-baseline routing",
            "conditional_derivation": "3831 gives the component split; tensor virial can kill only a closed stationary total source with surface/exchange and EM/radiation handled",
            "status": "SOURCE_ZERO_ROUTE_CONDITIONAL_NOT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "ANG3977_2_boundary_route",
            "claim_piece": "boundary angular moment silence",
            "mathematical_form": "B_lm^boundary,res = 0 if boundary harmonic data, flux, wall/shear stress, corner data, history kernel, and domain/projector motion vanish in the same parent branch",
            "conditional_derivation": "3930 gives isolated-boundary zero rows but only in the private isolated branch; 3931 and 3929 keep history/domain fallbacks if reset or fixed-domain assumptions fail",
            "status": "BOUNDARY_ZERO_ROUTE_CONDITIONAL_NOT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "ANG3977_3_external_route",
            "claim_piece": "external tide silence",
            "mathematical_form": "E_lm^external,res = 0 if local arena has no unresolved external STF/tidal source or it is explicitly included in the GR comparison metric",
            "conditional_derivation": "external tides are not killed by stationarity; they need an arena certificate or a sourced bound",
            "status": "EXTERNAL_TIDE_ZERO_ROUTE_CONDITIONAL_NOT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "ANG3977_4_poynting_guard",
            "claim_piece": "Poynting/vector stress guard",
            "mathematical_form": "S_EM circulation inside the worldtube is allowed; only the closed total boundary flux can be zero",
            "conditional_derivation": "do not delete EM/Poynting stress by choosing a matter-only tube; either include it in the closed total source or bound epsilon_EM_Poynting_TF",
            "status": "GUARD_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "ANG3977_5_spherical_shortcut_refusal",
            "claim_piece": "no spherical averaging cheat",
            "mathematical_form": "stationarity or a chosen spherical readout surface does not imply Q_lm=B_lm=E_lm=0",
            "conditional_derivation": "the parent must own the angular moment silence or the bound rows stay in the residual vector",
            "status": "SHORTCUT_REFUSED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "ANG3977_6_certificate",
            "claim_piece": "angular silence certificate",
            "mathematical_form": "Z_ang_silence = Z_closed_total_source * Z_tensor_virial * Z_boundary_isolated * Z_external_tide_silence * Z_Poynting_total_source * Z_GR_multipole_routing",
            "conditional_derivation": "Z_ang_silence=1 would feed Z_SO3_boundary and eliminate epsilon_source_l_ge_1, epsilon_boundary_scalar_l_ge_1, and epsilon_external_tidal_l_ge_1",
            "status": "CERTIFICATE_DEFINED_CURRENTLY_FALSE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "ANG3977_7_current_verdict",
            "claim_piece": "current angular moment status",
            "mathematical_form": "current corpus provides useful conditional zero routes but not parent-signed zeroes for real local arenas",
            "conditional_derivation": "therefore the right next move is source-side tensor-virial/Poynting inclusion, not another broad SO3 assertion",
            "status": "PROFILE_BOUND_ROUTE_ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decomposition_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "MPD3977_0_source_residual",
            "symbol": "epsilon_source_l_ge_1",
            "profile_object": "Q_lm^source,res",
            "decomposition": "epsilon_ext_TF + epsilon_tensor_virial_TF + epsilon_quad_TF + epsilon_EM_Poynting_TF + epsilon_apparatus_TF",
            "zero_route": "closed total source + exterior vacuum + tensor virial + no unresolved quadrupole residual + EM/Poynting included + apparatus included/outside projection",
            "required_profile_inputs": "l_max, Q_lm table, r_eval, M_H_ref, source support, worldtube definition, GR-baseline routing flag",
            "current_status": "DECOMPOSED_VALUES_OR_ZERO_CERTIFICATE_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MPD3977_1_boundary_residual",
            "symbol": "epsilon_boundary_scalar_l_ge_1",
            "profile_object": "B_lm^boundary,res",
            "decomposition": "epsilon_boundary_harmonic_l_ge_1 + epsilon_boundary_flux_TF + epsilon_boundary_wall_TF + epsilon_boundary_corner_l_ge_1 + epsilon_history_nonlocal_l_ge_1 + epsilon_domain_projector_abs",
            "zero_route": "isolated stationary collar + no harmonic boundary data + no total Hilbert/Maxwell flux + scalar wall stress + no corner source + reset/common-mode history + fixed projector/domain",
            "required_profile_inputs": "boundary harmonic coefficients, Phi_B, tau_wall_TF, corner terms, history kernel norm, domain/projector norm",
            "current_status": "DECOMPOSED_VALUES_OR_ZERO_CERTIFICATE_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MPD3977_2_external_residual",
            "symbol": "epsilon_external_tidal_l_ge_1",
            "profile_object": "E_lm^external,res",
            "decomposition": "epsilon_external_tidal_TF + epsilon_arena_anisotropy + epsilon_environment_coupling",
            "zero_route": "arena has no unresolved external STF field or it is entirely present in the GR comparison metric and absent from the MTS residual source",
            "required_profile_inputs": "external tidal tensor/multipoles, arena isolation certificate, GR-baseline inclusion flag",
            "current_status": "NEW_BOUND_ROW_READY_VALUES_OR_ZERO_CERTIFICATE_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MPD3977_3_GR_multipole_routing",
            "symbol": "epsilon_GR_routed_l_ge_1",
            "profile_object": "ordinary GR multipoles",
            "decomposition": "physical quadrupoles/tides allowed in baseline metric, but not as extra MTS residual hair",
            "zero_route": "subtract/route standard GR multipoles before testing residual MTS angular hair",
            "required_profile_inputs": "baseline GR metric/multipole model, same source support, same readout radius, declared residual operator",
            "current_status": "ROUTING_CONTRACT_DEFINED_NOT_NUMERIC",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "MPD3977_4_total_no_cancellation",
            "symbol": "epsilon_angular_moment_abs",
            "profile_object": "absolute angular residual budget",
            "decomposition": "epsilon_source_l_ge_1 + epsilon_boundary_scalar_l_ge_1 + epsilon_external_tidal_l_ge_1",
            "zero_route": "all three parent zero routes signed in the same branch",
            "required_profile_inputs": "source, boundary, and external profiles or theorem-zero certificates",
            "current_status": "TOTAL_BOUND_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "MPB3977_0_source_profile",
            "symbol": "epsilon_source_l_ge_1",
            "formula": "epsilon_source_l_ge_1 <= epsilon_ext_TF + epsilon_tensor_virial_TF + epsilon_quad_TF + epsilon_EM_Poynting_TF + epsilon_apparatus_TF",
            "units": "dimensionless",
            "required_input_or_theorem": "source Q_lm profile or Z_closed_total_source*Z_tensor_virial*Z_Poynting_total_source*Z_GR_multipole_routing=1",
            "feeds_or_blocks": "SO3A3976_1_source_moments",
            "current_status": "PROFILE_BOUND_READY_VALUES_OR_ZERO_CERTIFICATE_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "MPB3977_1_boundary_profile",
            "symbol": "epsilon_boundary_scalar_l_ge_1",
            "formula": "epsilon_boundary_scalar_l_ge_1 <= epsilon_boundary_harmonic_l_ge_1 + epsilon_boundary_flux_TF + epsilon_boundary_wall_TF + epsilon_boundary_corner_l_ge_1 + epsilon_history_nonlocal_l_ge_1 + epsilon_domain_projector_abs",
            "units": "dimensionless",
            "required_input_or_theorem": "boundary B_lm profile or Z_boundary_isolated*Z_history_reset*Z_fixed_domain=1",
            "feeds_or_blocks": "SO3A3976_2_boundary_moments",
            "current_status": "PROFILE_BOUND_READY_VALUES_OR_ZERO_CERTIFICATE_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "MPB3977_2_external_profile",
            "symbol": "epsilon_external_tidal_l_ge_1",
            "formula": "epsilon_external_tidal_l_ge_1 <= epsilon_external_tidal_TF + epsilon_arena_anisotropy + epsilon_environment_coupling",
            "units": "dimensionless",
            "required_input_or_theorem": "arena tidal certificate or sourced external multipole/tidal profile",
            "feeds_or_blocks": "SO3A3976_3_external_tides",
            "current_status": "PROFILE_BOUND_READY_VALUES_OR_ZERO_CERTIFICATE_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "MPB3977_3_GR_baseline_route",
            "symbol": "epsilon_extra_MTS_l_ge_1",
            "formula": "epsilon_extra_MTS_l_ge_1 := ||P_residual(Q_lm^total - Q_lm^GR_baseline)||/M_H_ref",
            "units": "dimensionless",
            "required_input_or_theorem": "same-source GR baseline profile and residual projection operator",
            "feeds_or_blocks": "prevents punishing MTS for ordinary GR multipoles while keeping extra hair testable",
            "current_status": "ROUTING_BOUND_READY_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "bound_id": "MPB3977_4_total_angular",
            "symbol": "epsilon_angular_moment_abs",
            "formula": "epsilon_angular_moment_abs = epsilon_source_l_ge_1 + epsilon_boundary_scalar_l_ge_1 + epsilon_external_tidal_l_ge_1",
            "units": "dimensionless",
            "required_input_or_theorem": "all source/boundary/external profile rows sourced or theorem-zero",
            "feeds_or_blocks": "epsilon_SO3_failure_abs and Delta_PPN_source_abs",
            "current_status": "TOTAL_BOUND_READY_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ZANG3977_0_closed_source", "Z_closed_total_source", "source worldtube includes matter + fields + binding + apparatus/exchange or proves they are outside projection", "required", "UNSIGNED", "epsilon_source_l_ge_1"),
        ("ZANG3977_1_tensor_virial", "Z_tensor_virial", "d2I_TF/dt2=0 and surface_TF=exchange_TF=0 on the claimed timescale", "required", "UNSIGNED", "epsilon_tensor_virial_TF"),
        ("ZANG3977_2_poynting", "Z_Poynting_total_source", "EM/radiative/Poynting stress is included in closed Hilbert/Maxwell source or separately bounded", "required", "UNSIGNED", "epsilon_EM_Poynting_TF"),
        ("ZANG3977_3_boundary", "Z_boundary_isolated", "no B_lm boundary harmonic, no Phi_B total flux, no tau_wall_TF, no corner/history/domain leakage", "required", "CONDITIONAL_PRIVATE_BRANCH_ONLY", "epsilon_boundary_scalar_l_ge_1"),
        ("ZANG3977_4_external", "Z_external_tide_silence", "no unresolved external STF/tidal multipole in the residual channel", "required", "UNSIGNED", "epsilon_external_tidal_l_ge_1"),
        ("ZANG3977_5_GR_route", "Z_GR_multipole_routing", "ordinary GR multipoles are routed into the comparator metric before residual extraction", "required", "DEFINED_NOT_SIGNED", "epsilon_extra_MTS_l_ge_1"),
        ("ZANG3977_6_total", "Z_ang_silence", "product of closed-source, tensor-virial, Poynting, boundary, external, and GR-routing certificates", "total", "FALSE_UNTIL_ALL_FACTORS_SIGNED", "Z_SO3_boundary"),
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
            "feed_id": "ANGF3977_0_source",
            "target": "epsilon_source_l_ge_1",
            "update": "replace single opaque source moment row with decomposed source TF/virial/quadrupole/Poynting/apparatus budget",
            "effect": "source angular moment channel is now derivation-first but bound-ready",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "ANGF3977_1_boundary",
            "target": "epsilon_boundary_scalar_l_ge_1",
            "update": "replace opaque boundary moment row with harmonic/flux/wall/corner/history/domain budget",
            "effect": "3930 isolated-boundary result can be used only if its branch certificates are parent-signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "ANGF3977_2_external",
            "target": "epsilon_external_tidal_l_ge_1",
            "update": "new explicit external-tide residual row added",
            "effect": "SO3/local branch cannot hide environmental STF moments",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "ANGF3977_3_SO3",
            "target": "Z_SO3_boundary",
            "update": "Z_ang_silence can feed SO3 only after source, boundary, external, Poynting, and GR-routing certificates close",
            "effect": "SO3 route remains nonclaim but more exact",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "ANGF3977_4_PPN",
            "target": "Delta_PPN_source_abs",
            "update": "angular moment residuals enter PPN through no-cancellation epsilon_angular_moment_abs",
            "effect": "PPN residual vector gets an explicit multipole/profile channel",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "ANGF3977_5_next",
            "target": "closed_total_source_tensor_virial_poynting_inclusion",
            "update": f"move to {NEXT_DOC}",
            "effect": "attack the highest-leverage source-side zero proof first",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3977_0_attempt",
            "decision": "attempt angular moment silence proof",
            "status": "CONDITIONAL_THEOREM_SHAPE_WRITTEN",
            "reason": "source/boundary/external zeroes can be derived only under stronger closed-total-source, boundary-isolation, external-tide, and GR-routing premises",
            "next_action": "try to sign the source-side premises first",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3977_1_reject_broad_zero",
            "decision": "do not claim Q_lm=B_lm=E_lm=0 broadly",
            "status": "BROAD_ZERO_REJECTED",
            "reason": "real local arenas can have quadrupoles, Poynting stress, apparatus stress, boundary flux, domain motion, and external tides",
            "next_action": "carry profile bounds unless parent signs a specific zero branch",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3977_2_route",
            "decision": "separate ordinary GR multipoles from extra MTS residual hair",
            "status": "GR_BASELINE_ROUTING_REQUIRED",
            "reason": "a fair comparison should not count standard GR quadrupoles/tides against MTS, but extra residual hair must be bounded",
            "next_action": "define residual projection against the same-source GR baseline",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3977_3_next",
            "decision": "next target selected",
            "status": "MOVE_TO_SOURCE_SIDE_ZERO_PROOF_OR_PROFILE_ACQUISITION",
            "reason": "source Q_lm is the most physics-dense obstruction and directly touches tensor virial plus Poynting/vector stress concerns",
            "next_action": NEXT_DOC,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3977_0_angular_silence",
            "gate": "angular moment silence",
            "requirement": "Z_ang_silence=1 or all source/boundary/external profile rows are numeric, sourced, and below threshold",
            "status": "BLOCKED_PARENT_SIGNATURE_AND_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3977_1_SO3",
            "gate": "SO3 promotion",
            "requirement": "angular moment silence plus no-spurion/common-mode/uniqueness certificates",
            "status": "BLOCKED_ANGULAR_MOMENT_SILENCE_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3977_2_PPN",
            "gate": "local PPN/GR",
            "requirement": "source/boundary/external angular residuals vanish or are bounded inside the full PPN residual vector",
            "status": "LOCAL_GR_STILL_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3977_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "prove closed-total-source tensor-virial plus EM/Poynting inclusion kills residual Q_lm^source, or create the first source multipole/Poynting profile acquisition rows",
            "success_condition": "source-side angular residual is parent-zeroed for the local branch or reduced to explicit sourced profile inputs with GR-baseline routing",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "ANGULAR_MOMENT_SILENCE_THEOREM_SHAPE_AND_PROFILE_BOUNDS_READY",
            "sources_found": found,
            "sources_total": len(sources),
            "main_result": "Q_lm/B_lm/E_lm silence is conditionally derivable only for a closed total source, isolated boundary, no external tide, EM/Poynting-included branch with ordinary GR multipoles routed to the comparator; current corpus does not sign this, so source/boundary/external profile bounds are active",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, sources: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in sources)
    return f"""# 3977 - Source/Boundary Angular-Moment Silence Or Multipole Profile Bound

Timestamp: `{timestamp}`

## Result

3977 tries the requested derivation instead of only listing the gap.

The exact non-smuggled zero route is:

```text
Z_ang_silence =
  Z_closed_total_source
* Z_tensor_virial
* Z_Poynting_total_source
* Z_boundary_isolated
* Z_external_tide_silence
* Z_GR_multipole_routing

Z_ang_silence = 1
=> Q_lm^source,res = B_lm^boundary,res = E_lm^external,res = 0 for l >= 1
```

## What Was Derived

The local branch can kill residual angular moments only if it is a closed total-system branch, not a matter-only or spherical-averaged shortcut.

The source obstruction decomposes as:

```text
epsilon_source_l_ge_1 <=
  epsilon_ext_TF
+ epsilon_tensor_virial_TF
+ epsilon_quad_TF
+ epsilon_EM_Poynting_TF
+ epsilon_apparatus_TF
```

The boundary obstruction decomposes as:

```text
epsilon_boundary_scalar_l_ge_1 <=
  epsilon_boundary_harmonic_l_ge_1
+ epsilon_boundary_flux_TF
+ epsilon_boundary_wall_TF
+ epsilon_boundary_corner_l_ge_1
+ epsilon_history_nonlocal_l_ge_1
+ epsilon_domain_projector_abs
```

The external obstruction is now explicit:

```text
epsilon_external_tidal_l_ge_1 <=
  epsilon_external_tidal_TF
+ epsilon_arena_anisotropy
+ epsilon_environment_coupling
```

## Verdict

Broad `Q_lm=B_lm=E_lm=0` is rejected for now. Real local arenas can have quadrupoles, Poynting stress, apparatus stress, boundary flux, domain motion, and external tides.

This is still progress: ordinary GR multipoles are separated from extra MTS residual hair, so the next test is fair rather than guilty-until-proven-innocent.

No local-GR or SO3 claim is made.

Next target:

```text
{NEXT_DOC}
```

Source needles found: `{found}/{len(sources)}`.
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3977 - Source/Boundary Angular-Moment Silence Or Multipole Profile Bound

- Timestamp: `{timestamp}`
- Status: `ANGULAR_MOMENT_SILENCE_THEOREM_SHAPE_AND_PROFILE_BOUNDS_READY`
- Derived route:
  `Z_ang_silence = Z_closed_total_source * Z_tensor_virial * Z_Poynting_total_source * Z_boundary_isolated * Z_external_tide_silence * Z_GR_multipole_routing`.
- Conditional consequence:
  `Z_ang_silence=1 => Q_lm^source,res = B_lm^boundary,res = E_lm^external,res = 0` for `l>=1`.
- Current claim status: nonclaim. Broad zero is rejected because real arenas can carry quadrupoles, Poynting/apparatus stress, boundary/domain leakage, and external tides.
- New residual budget:
  `epsilon_angular_moment_abs = epsilon_source_l_ge_1 + epsilon_boundary_scalar_l_ge_1 + epsilon_external_tidal_l_ge_1`.
- Important improvement:
  ordinary GR multipoles must be routed into the comparator metric before extra MTS residual hair is judged.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3977 - Source/Boundary Angular-Moment Silence Or Multipole Profile Bound"
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
        "decomposition": decomposition_rows(timestamp),
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
    decomposition = rows["decomposition"]
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
    decomposition_symbols = {row["symbol"] for row in decomposition}
    bound_symbols = {row["symbol"] for row in bounds}
    certificate_factors = {row["factor"] for row in certificate}
    feed_targets = {row["target"] for row in feed}
    decision_statuses = {row["status"] for row in decisions}
    claim_statuses = {row["status"] for row in claims}

    return [
        val("VAL3977_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3977_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3977_02_theorem_shape", {"CONDITIONAL_THEOREM_SHAPE_WRITTEN", "GUARD_ACTIVE", "SHORTCUT_REFUSED", "PROFILE_BOUND_ROUTE_ACTIVE"} <= theorem_statuses, "conditional theorem, Poynting guard, shortcut refusal, and profile verdict present"),
        val("VAL3977_03_theorem_targets", {"angular moment silence", "source multipole silence", "boundary angular moment silence", "external tide silence", "Poynting/vector stress guard"} <= theorem_pieces, "source, boundary, external, and Poynting theorem pieces present"),
        val("VAL3977_04_decomposition", {"epsilon_source_l_ge_1", "epsilon_boundary_scalar_l_ge_1", "epsilon_external_tidal_l_ge_1", "epsilon_GR_routed_l_ge_1", "epsilon_angular_moment_abs"} <= decomposition_symbols, "profile decomposition covers source, boundary, external, GR routing, and total budget"),
        val("VAL3977_05_bounds", {"epsilon_source_l_ge_1", "epsilon_boundary_scalar_l_ge_1", "epsilon_external_tidal_l_ge_1", "epsilon_extra_MTS_l_ge_1", "epsilon_angular_moment_abs"} <= bound_symbols, "multipole profile bound rows present"),
        val("VAL3977_06_certificate", {"Z_closed_total_source", "Z_tensor_virial", "Z_Poynting_total_source", "Z_boundary_isolated", "Z_external_tide_silence", "Z_GR_multipole_routing", "Z_ang_silence"} <= certificate_factors, "Z_ang_silence certificate factors present"),
        val("VAL3977_07_feed", {"epsilon_source_l_ge_1", "epsilon_boundary_scalar_l_ge_1", "epsilon_external_tidal_l_ge_1", "Z_SO3_boundary", "Delta_PPN_source_abs", "closed_total_source_tensor_virial_poynting_inclusion"} <= feed_targets, "feeds reach SO3, PPN, and next source-side target"),
        val("VAL3977_08_decision", {"CONDITIONAL_THEOREM_SHAPE_WRITTEN", "BROAD_ZERO_REJECTED", "GR_BASELINE_ROUTING_REQUIRED", "MOVE_TO_SOURCE_SIDE_ZERO_PROOF_OR_PROFILE_ACQUISITION"} <= decision_statuses, "decision gate records theorem attempt, broad-zero rejection, fair GR routing, and next move"),
        val("VAL3977_09_claim_gate", {"BLOCKED_PARENT_SIGNATURE_AND_VALUES_MISSING", "BLOCKED_ANGULAR_MOMENT_SILENCE_UNSIGNED", "LOCAL_GR_STILL_OPEN"} <= claim_statuses, "claim gates block angular silence, SO3, and local GR"),
        val("VAL3977_10_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to source-side tensor-virial/Poynting route"),
        val("VAL3977_11_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3977_12_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3977_13_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3977_14_spine_updated", SPINE_PATH.exists() and "3977 - Source/Boundary Angular-Moment Silence Or Multipole Profile Bound" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3977_15_csv_parse", parsed, parse_detail),
        val("VAL3977_16_script_compile", True, "script compiled before validation write"),
        val("VAL3977_17_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
        val("VAL3977_18_fair_comparator_guard", any(row["symbol"] == "epsilon_extra_MTS_l_ge_1" for row in bounds), "ordinary GR multipoles are separated from extra MTS residual hair"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["theorem"], rows["theorem"])
    write_csv(OUTPUTS["decomposition"], rows["decomposition"])
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
        raise SystemExit(f"3977 validation failed: {failed}")

    print(f"3977 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("Angular-moment theorem shape and profile-bound route assembled")


if __name__ == "__main__":
    run()

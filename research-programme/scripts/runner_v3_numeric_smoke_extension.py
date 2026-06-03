from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "runner-v3-numeric-smoke-extension"
CHECKPOINT_DOC = "400-runner-v3-numeric-smoke-extension.md"
STATUS = "runner_v3_numeric_smoke_extension_written_GR_null_baseline_sane_channel_bounds_and_retained_residual_sweeps_no_PPN_or_local_GR_pass"
CLAIM_CEILING = "runner_v3_numeric_smoke_extension_only_no_WEP_EH_Newton_PPN_fifth_force_boundary_bulk_domain_or_local_GR_pass"
NEXT_TARGET = "401-parent-matter-selector-theorem-attempt.md"


SOURCE_DOCS = [
    {
        "path": "374-fifth-force-preferred-frame-source-lock-manifest.md",
        "role": "preferred-frame, xi, Gdot/G, and fifth-force source-lock policy",
    },
    {
        "path": "377-fifth-force-range-coupling-map.md",
        "role": "Yukawa alpha(lambda) force-law contract and no fake scalar fifth-force score",
    },
    {
        "path": "397-local-bound-runner-v3-from-identity-stack.md",
        "role": "runner-v3 row states and source locks",
    },
    {
        "path": "398-parent-action-contract-v2-after-identity-stack.md",
        "role": "parent-action obligations for each runner-v3 row",
    },
    {
        "path": "399-local-GR-status-for-human-review.md",
        "role": "current project status and next target",
    },
    {
        "path": "runs/20260602-033500-local-bound-runner-v3-from-identity-stack/results/runner_v3_matrix.csv",
        "role": "machine-readable runner-v3 matrix",
    },
    {
        "path": "runs/20260602-033500-local-bound-runner-v3-from-identity-stack/results/residual_smoke_matrix.csv",
        "role": "runner-v3 same-evaluator smoke controls",
    },
    {
        "path": "runs/20260602-034500-parent-action-contract-v2-after-identity-stack/results/runner_row_parent_obligations.csv",
        "role": "machine-readable row-to-parent-obligation map",
    },
]


NUMERIC_ROW_EQUATIONS = {
    "R0_identity_coframe_direct": [
        "coframe_slip_ehat_minus_e",
    ],
    "R1_WEP_source_charge": [
        "source_charge_species_split",
        "bulk_X_composition_charge",
        "boundary_species_charge",
        "source_normalization_species_split",
    ],
    "R2_clock_redshift": [
        "clock_constant_drift",
        "source_clock_normalization_drift",
        "nonlocal_clock_drift",
    ],
    "R3_gamma": [
        "nonEH_operator_coefficient",
        "scalar_tensor_operator_coefficient",
        "boundary_tracefree_shear",
        "bulk_X_metric_slip",
        "domain_projector_stress",
    ],
    "R4_beta": [
        "source_normalization_beta",
        "boundary_radial_hair",
        "nonlinear_bulk_source_hair",
        "scalar_tensor_operator_coefficient",
        "nonEH_operator_coefficient",
    ],
    "R5_alpha1": [
        "boundary_vector_B0i",
        "domain_vector_leakage",
        "projector_vector_leakage",
        "marker_leakage",
    ],
    "R6_alpha2": [
        "boundary_vector_B0i",
        "domain_vector_leakage",
        "domain_anisotropy",
        "projector_vector_leakage",
    ],
    "R7_alpha3": [
        "unowned_momentum_flux",
        "bulk_flux_X",
        "domain_projector_flux",
    ],
    "R8_xi": [
        "boundary_tracefree_shear",
        "domain_anisotropy",
        "topology_cycle_anisotropy",
        "external_domain_anisotropy",
    ],
    "R9_Gdot": [
        "geff_meff_drift_per_yr",
        "memory_kernel_drift_per_yr",
        "flux_drift_per_yr",
        "domain_scale_drift_per_yr",
    ],
}


SYMBOLIC_ROW_CHANNELS = {
    "R10_fifth_force": [
        "finite_range_yukawa_alpha",
        "bulk_X_metric_slip",
        "boundary_radial_hair",
        "scalar_tensor_operator_coefficient",
        "source_charge_species_split",
        "bulk_X_composition_charge",
    ],
    "R11_EH_operator_ledger": [
        "nonEH_operator_coefficient",
        "scalar_tensor_operator_coefficient",
        "nonlocal_operator_coefficient",
    ],
}


CHANNEL_METADATA = {
    "coframe_slip_ehat_minus_e": {
        "sector": "WEP/coframe",
        "units": "dimensionless",
        "meaning": "nonmetric matter pullback leakage ehat-e",
    },
    "source_charge_species_split": {
        "sector": "WEP/source",
        "units": "dimensionless",
        "meaning": "species-dependent source charge or q/m split",
    },
    "bulk_X_composition_charge": {
        "sector": "bulk-X/source",
        "units": "dimensionless",
        "meaning": "bulk-X composition charge coupled to source/test masses",
    },
    "boundary_species_charge": {
        "sector": "boundary/source",
        "units": "dimensionless",
        "meaning": "boundary/class charge that distinguishes species",
    },
    "source_normalization_species_split": {
        "sector": "source normalization",
        "units": "dimensionless",
        "meaning": "species split in measured GM normalization",
    },
    "clock_constant_drift": {
        "sector": "clock/time",
        "units": "dimensionless",
        "meaning": "clock-sector constant drift or nonmetric clock coupling",
    },
    "source_clock_normalization_drift": {
        "sector": "clock/source",
        "units": "dimensionless",
        "meaning": "source-normalization drift visible to redshift clocks",
    },
    "nonlocal_clock_drift": {
        "sector": "clock/nonlocal",
        "units": "dimensionless",
        "meaning": "nonlocal or memory-clock residue",
    },
    "nonEH_operator_coefficient": {
        "sector": "metric/operator",
        "units": "dimensionless",
        "meaning": "effective non-Einstein-Hilbert operator coefficient",
    },
    "scalar_tensor_operator_coefficient": {
        "sector": "metric/scalar",
        "units": "dimensionless",
        "meaning": "scalar-tensor or extra metric-slip operator coefficient",
    },
    "boundary_tracefree_shear": {
        "sector": "boundary",
        "units": "dimensionless",
        "meaning": "trace-free boundary shear or angular hair",
    },
    "bulk_X_metric_slip": {
        "sector": "bulk-X",
        "units": "dimensionless",
        "meaning": "bulk-X stress visible as metric slip or radial force residue",
    },
    "domain_projector_stress": {
        "sector": "domain/projector",
        "units": "dimensionless",
        "meaning": "domain/projector stress residue in local metric equations",
    },
    "source_normalization_beta": {
        "sector": "source normalization",
        "units": "dimensionless",
        "meaning": "nonlinear measured-GM/source-normalization beta residue",
    },
    "boundary_radial_hair": {
        "sector": "boundary",
        "units": "dimensionless",
        "meaning": "radial boundary hair not absorbed into measured GM",
    },
    "nonlinear_bulk_source_hair": {
        "sector": "bulk/source",
        "units": "dimensionless",
        "meaning": "nonlinear bulk/source hair in the Newtonian limit",
    },
    "boundary_vector_B0i": {
        "sector": "preferred-frame/boundary",
        "units": "dimensionless",
        "meaning": "boundary vector component B0i",
    },
    "domain_vector_leakage": {
        "sector": "preferred-frame/domain",
        "units": "dimensionless",
        "meaning": "domain vector representative leakage",
    },
    "projector_vector_leakage": {
        "sector": "preferred-frame/projector",
        "units": "dimensionless",
        "meaning": "projector vector representative leakage",
    },
    "marker_leakage": {
        "sector": "preferred-frame/markers",
        "units": "dimensionless",
        "meaning": "physical leakage of marker labels",
    },
    "domain_anisotropy": {
        "sector": "domain/anisotropy",
        "units": "dimensionless",
        "meaning": "domain anisotropy or preferred-location residue",
    },
    "unowned_momentum_flux": {
        "sector": "Ward/flux",
        "units": "dimensionless",
        "meaning": "unowned momentum flux in total Ward identity",
    },
    "bulk_flux_X": {
        "sector": "bulk-X/flux",
        "units": "dimensionless",
        "meaning": "bulk-X momentum flux not cancelled by the Ward ledger",
    },
    "domain_projector_flux": {
        "sector": "domain/projector flux",
        "units": "dimensionless",
        "meaning": "domain/projector flux not owned by the total stress ledger",
    },
    "topology_cycle_anisotropy": {
        "sector": "topology/domain",
        "units": "dimensionless",
        "meaning": "topology cycle anisotropy visible as preferred location",
    },
    "external_domain_anisotropy": {
        "sector": "external domain",
        "units": "dimensionless",
        "meaning": "external-domain anisotropy not gauge/topological",
    },
    "geff_meff_drift_per_yr": {
        "sector": "source/time",
        "units": "yr^-1",
        "meaning": "time drift of G_eff M_eff",
    },
    "memory_kernel_drift_per_yr": {
        "sector": "memory/time",
        "units": "yr^-1",
        "meaning": "memory-kernel drift visible as Gdot/G",
    },
    "flux_drift_per_yr": {
        "sector": "Ward/time",
        "units": "yr^-1",
        "meaning": "unowned secular flux drift",
    },
    "domain_scale_drift_per_yr": {
        "sector": "domain/time",
        "units": "yr^-1",
        "meaning": "domain scale drift visible as Gdot/G",
    },
    "finite_range_yukawa_alpha": {
        "sector": "fifth-force",
        "units": "dimensionless",
        "meaning": "Yukawa alpha(lambda) coefficient; cannot be scalar-scored without range/profile/source charges",
    },
    "nonlocal_operator_coefficient": {
        "sector": "nonlocal/operator",
        "units": "dimensionless",
        "meaning": "nonlocal operator coefficient retained in the modified-gravity ledger",
    },
}


PROFILE_SPECS = [
    {
        "profile": "GR_null_baseline",
        "kind": "all_zero",
        "description": "GR/null comparator through the same evaluator.",
        "claim_policy": "pipeline sanity only",
    },
    {
        "profile": "identity_closure_clean_zero_residuals",
        "kind": "all_zero",
        "description": "Best-case labelled identity branch with all retained channels set to zero by hand.",
        "claim_policy": "zero control only, not parent derivation",
    },
    {
        "profile": "derived_suppression_target_0p1_tightest_bound",
        "kind": "fraction_tightest_bound",
        "fraction": 0.1,
        "description": "Each channel is placed at 10 percent of its tightest solo source-lock bound.",
        "claim_policy": "inside budget only if a parent theorem derives these suppressions",
    },
    {
        "profile": "edge_tightest_bound",
        "kind": "fraction_tightest_bound",
        "fraction": 1.0,
        "description": "Each channel is placed at its solo source-lock edge; multi-channel rows should become unstable.",
        "claim_policy": "edge is not stable evidence",
    },
    {
        "profile": "identity_branch_nonclosure_floor_1e_minus_12",
        "kind": "absolute_floor",
        "dimensionless_floor": 1.0e-12,
        "per_year_floor": 1.0e-12,
        "zero_channels": ["coframe_slip_ehat_minus_e"],
        "description": "Identity coframe row held closed while every other open channel leaks at 1e-12.",
        "claim_policy": "diagnostic leak floor",
    },
    {
        "profile": "full_floor_all_channels_1e_minus_12",
        "kind": "absolute_floor",
        "dimensionless_floor": 1.0e-12,
        "per_year_floor": 1.0e-12,
        "description": "All channels, including direct coframe slip, leak at 1e-12.",
        "claim_policy": "diagnostic leak floor",
    },
    {
        "profile": "source_charge_floor_1e_minus_14",
        "kind": "explicit",
        "values": {
            "source_charge_species_split": 1.0e-14,
            "bulk_X_composition_charge": 1.0e-14,
            "source_normalization_species_split": 1.0e-14,
        },
        "description": "Composition/source charge residue at a tiny but WEP-relevant scale.",
        "claim_policy": "diagnostic WEP-source stress",
    },
    {
        "profile": "boundary_vector_flux_1e_minus_10",
        "kind": "explicit",
        "values": {
            "boundary_vector_B0i": 1.0e-10,
            "boundary_tracefree_shear": 1.0e-10,
            "boundary_radial_hair": 1.0e-10,
            "unowned_momentum_flux": 1.0e-10,
        },
        "description": "Boundary vector/shear/radial/flux residue at 1e-10.",
        "claim_policy": "diagnostic boundary stress",
    },
    {
        "profile": "domain_projector_1e_minus_10",
        "kind": "explicit",
        "values": {
            "domain_vector_leakage": 1.0e-10,
            "domain_projector_stress": 1.0e-10,
            "projector_vector_leakage": 1.0e-10,
            "domain_anisotropy": 1.0e-10,
            "domain_projector_flux": 1.0e-10,
            "domain_scale_drift_per_yr": 1.0e-10,
        },
        "description": "Domain/projector residue at 1e-10.",
        "claim_policy": "diagnostic domain/projector stress",
    },
    {
        "profile": "EH_operator_1e_minus_5",
        "kind": "explicit",
        "values": {
            "nonEH_operator_coefficient": 1.0e-5,
            "scalar_tensor_operator_coefficient": 1.0e-5,
        },
        "description": "Non-EH operator leakage at 1e-5.",
        "claim_policy": "diagnostic metric-operator stress",
    },
    {
        "profile": "Gdot_memory_drift_1e_minus_14_per_yr",
        "kind": "explicit",
        "values": {
            "memory_kernel_drift_per_yr": 1.0e-14,
        },
        "description": "One memory/time channel just above the Gdot/G guardrail scale.",
        "claim_policy": "diagnostic secular-drift stress",
    },
    {
        "profile": "fifth_force_alpha_1e_minus_5_unscored",
        "kind": "explicit",
        "values": {
            "finite_range_yukawa_alpha": 1.0e-5,
        },
        "description": "Finite-range Yukawa alpha present but no lambda/profile/source charges supplied.",
        "claim_policy": "unscored fifth-force activation only",
    },
    {
        "profile": "unit_coupling_stress",
        "kind": "unit_coupling",
        "description": "All channels set to order one.",
        "claim_policy": "must fail; exposes required suppression",
    },
]


FIFTH_FORCE_PROBES = [
    {"lambda_m": 1.0e-3, "radius_m": 1.0e-3, "alpha_Y": 1.0e-2},
    {"lambda_m": 1.0e-3, "radius_m": 1.0e-2, "alpha_Y": 1.0e-2},
    {"lambda_m": 1.0, "radius_m": 1.0, "alpha_Y": 1.0e-5},
    {"lambda_m": 1.0e3, "radius_m": 1.0e3, "alpha_Y": 1.0e-5},
    {"lambda_m": 1.0e9, "radius_m": 1.5e11, "alpha_Y": 1.0e-10},
    {"lambda_m": 1.5e11, "radius_m": 1.5e11, "alpha_Y": 1.0e-10},
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        rows.append(
            {
                "source_file": source_doc["path"],
                "exists": source_path.exists(),
                "role": source_doc["role"],
            }
        )
    return rows


def runner_rows() -> list[dict[str, Any]]:
    source_path = ROOT / "runs/20260602-033500-local-bound-runner-v3-from-identity-stack/results/runner_v3_matrix.csv"
    rows: list[dict[str, Any]] = []
    for row in read_csv(source_path):
        parsed = dict(row)
        try:
            parsed["source_lock_float"] = float(row["source_lock"])
            parsed["numeric_source_lock"] = True
        except ValueError:
            parsed["source_lock_float"] = None
            parsed["numeric_source_lock"] = False
        rows.append(parsed)
    return rows


def channel_names() -> list[str]:
    names = set(CHANNEL_METADATA)
    for terms in NUMERIC_ROW_EQUATIONS.values():
        names.update(terms)
    for terms in SYMBOLIC_ROW_CHANNELS.values():
        names.update(terms)
    return sorted(names)


def channel_map_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    row_by_id = {row["row_id"]: row for row in rows}
    mapped_rows: list[dict[str, Any]] = []
    for row_id, channels in NUMERIC_ROW_EQUATIONS.items():
        runner_row = row_by_id[row_id]
        for channel in channels:
            metadata = CHANNEL_METADATA[channel]
            mapped_rows.append(
                {
                    "row_id": row_id,
                    "observable": runner_row["observable"],
                    "row_state": runner_row["state"],
                    "source_lock": runner_row["source_lock"],
                    "source_lock_units": runner_row["source_lock_units"],
                    "channel": channel,
                    "response_weight": 1.0,
                    "channel_sector": metadata["sector"],
                    "channel_units": metadata["units"],
                    "meaning": metadata["meaning"],
                    "score_policy": "numeric_source_lock",
                }
            )
    for row_id, channels in SYMBOLIC_ROW_CHANNELS.items():
        runner_row = row_by_id[row_id]
        for channel in channels:
            metadata = CHANNEL_METADATA[channel]
            mapped_rows.append(
                {
                    "row_id": row_id,
                    "observable": runner_row["observable"],
                    "row_state": runner_row["state"],
                    "source_lock": runner_row["source_lock"],
                    "source_lock_units": runner_row["source_lock_units"],
                    "channel": channel,
                    "response_weight": "symbolic",
                    "channel_sector": metadata["sector"],
                    "channel_units": metadata["units"],
                    "meaning": metadata["meaning"],
                    "score_policy": "retained_unscored",
                }
            )
    return mapped_rows


def row_equation_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    row_by_id = {row["row_id"]: row for row in rows}
    equation_rows: list[dict[str, Any]] = []
    for row_id, terms in NUMERIC_ROW_EQUATIONS.items():
        runner_row = row_by_id[row_id]
        equation_rows.append(
            {
                "row_id": row_id,
                "observable": runner_row["observable"],
                "row_state": runner_row["state"],
                "source_lock": runner_row["source_lock"],
                "equation": " + ".join(f"abs({term})" for term in terms),
                "score_policy": "residual/source_lock; no claim_allowed promotion",
            }
        )
    for row_id, terms in SYMBOLIC_ROW_CHANNELS.items():
        runner_row = row_by_id[row_id]
        equation_rows.append(
            {
                "row_id": row_id,
                "observable": runner_row["observable"],
                "row_state": runner_row["state"],
                "source_lock": runner_row["source_lock"],
                "equation": "active if any of " + ", ".join(terms) + " is nonzero",
                "score_policy": "symbolic retained debt; fifth force needs alpha(lambda), operator ledger needs parent theorem",
            }
        )
    return equation_rows


def channel_bound_requirement_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    row_by_id = {row["row_id"]: row for row in rows}
    requirement_rows: list[dict[str, Any]] = []
    for row_id, channels in NUMERIC_ROW_EQUATIONS.items():
        runner_row = row_by_id[row_id]
        source_lock = runner_row["source_lock_float"]
        if source_lock is None:
            continue
        for channel in channels:
            requirement_rows.append(
                {
                    "channel": channel,
                    "row_id": row_id,
                    "observable": runner_row["observable"],
                    "source_lock": source_lock,
                    "source_lock_units": runner_row["source_lock_units"],
                    "response_weight": 1.0,
                    "solo_channel_bound": source_lock,
                    "meaning": CHANNEL_METADATA[channel]["meaning"],
                }
            )
    return requirement_rows


def tightest_channel_bounds(requirement_rows: list[dict[str, Any]]) -> dict[str, float]:
    bounds: dict[str, float] = {}
    for row in requirement_rows:
        channel = row["channel"]
        bound = float(row["solo_channel_bound"])
        if channel not in bounds or bound < bounds[channel]:
            bounds[channel] = bound
    return bounds


def aggregate_channel_bound_rows(requirement_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_channel: dict[str, list[dict[str, Any]]] = {}
    for row in requirement_rows:
        by_channel.setdefault(row["channel"], []).append(row)
    aggregate_rows: list[dict[str, Any]] = []
    for channel, linked_rows in sorted(by_channel.items()):
        tightest = min(linked_rows, key=lambda item: float(item["solo_channel_bound"]))
        aggregate_rows.append(
            {
                "channel": channel,
                "tightest_solo_bound": tightest["solo_channel_bound"],
                "bound_units": tightest["source_lock_units"],
                "tightest_row": tightest["row_id"],
                "tightest_observable": tightest["observable"],
                "linked_numeric_rows": ";".join(row["row_id"] for row in linked_rows),
                "sector": CHANNEL_METADATA[channel]["sector"],
                "meaning": CHANNEL_METADATA[channel]["meaning"],
            }
        )
    aggregate_rows.sort(key=lambda row: float(row["tightest_solo_bound"]))
    return aggregate_rows


def build_profile_values(
    profile: dict[str, Any],
    tightest_bounds: dict[str, float],
) -> dict[str, float]:
    values = {channel: 0.0 for channel in channel_names()}
    kind = profile["kind"]
    if kind == "all_zero":
        return values
    if kind == "fraction_tightest_bound":
        fraction = float(profile["fraction"])
        for channel, bound in tightest_bounds.items():
            values[channel] = fraction * bound
        return values
    if kind == "absolute_floor":
        dimensionless_floor = float(profile["dimensionless_floor"])
        per_year_floor = float(profile["per_year_floor"])
        zero_channels = set(profile.get("zero_channels", []))
        for channel in values:
            if channel in zero_channels:
                values[channel] = 0.0
                continue
            units = CHANNEL_METADATA[channel]["units"]
            values[channel] = per_year_floor if units == "yr^-1" else dimensionless_floor
        return values
    if kind == "explicit":
        for channel, value in profile["values"].items():
            values[channel] = float(value)
        return values
    if kind == "unit_coupling":
        return {channel: 1.0 for channel in values}
    raise ValueError(f"unknown profile kind: {kind}")


def profile_input_rows(tightest_bounds: dict[str, float]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for profile in PROFILE_SPECS:
        values = build_profile_values(profile, tightest_bounds)
        for channel in channel_names():
            value = values[channel]
            if value == 0.0:
                continue
            rows.append(
                {
                    "profile": profile["profile"],
                    "channel": channel,
                    "value": value,
                    "units": CHANNEL_METADATA[channel]["units"],
                    "sector": CHANNEL_METADATA[channel]["sector"],
                    "meaning": CHANNEL_METADATA[channel]["meaning"],
                }
            )
    return rows


def smoke_class(profile_name: str, severity_ratio: float) -> str:
    if profile_name == "GR_null_baseline" and severity_ratio == 0.0:
        return "baseline_sane"
    if profile_name == "identity_closure_clean_zero_residuals" and severity_ratio == 0.0:
        return "zero_control_not_derivation"
    if severity_ratio < 1.0:
        return "inside_budget_smoke_only"
    if math.isclose(severity_ratio, 1.0, rel_tol=1.0e-12, abs_tol=1.0e-30):
        return "on_budget_edge_unstable"
    return "over_budget"


def evaluate_numeric_profiles(rows: list[dict[str, Any]], tightest_bounds: dict[str, float]) -> list[dict[str, Any]]:
    row_by_id = {row["row_id"]: row for row in rows}
    result_rows: list[dict[str, Any]] = []
    for profile in PROFILE_SPECS:
        values = build_profile_values(profile, tightest_bounds)
        for row_id, terms in NUMERIC_ROW_EQUATIONS.items():
            runner_row = row_by_id[row_id]
            source_lock = float(runner_row["source_lock_float"])
            term_values = [abs(values[term]) for term in terms]
            residual = sum(term_values)
            severity = residual / source_lock if source_lock else math.inf
            result_rows.append(
                {
                    "profile": profile["profile"],
                    "row_id": row_id,
                    "observable": runner_row["observable"],
                    "row_state": runner_row["state"],
                    "source_lock": source_lock,
                    "source_lock_units": runner_row["source_lock_units"],
                    "residual_value": residual,
                    "severity_ratio": severity,
                    "active_terms": ";".join(
                        term for term in terms if abs(values[term]) > 0.0
                    ),
                    "smoke_class": smoke_class(profile["profile"], severity),
                    "claim_allowed": False,
                    "interpretation": profile["claim_policy"],
                }
            )
    return result_rows


def profile_summary_rows(result_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary_rows: list[dict[str, Any]] = []
    for profile in PROFILE_SPECS:
        subset = [row for row in result_rows if row["profile"] == profile["profile"]]
        worst_row = max(subset, key=lambda row: float(row["severity_ratio"]))
        over_budget = sum(1 for row in subset if float(row["severity_ratio"]) > 1.0)
        edge = sum(
            1
            for row in subset
            if math.isclose(float(row["severity_ratio"]), 1.0, rel_tol=1.0e-12, abs_tol=1.0e-30)
        )
        inside = sum(1 for row in subset if float(row["severity_ratio"]) < 1.0)
        if profile["profile"] == "GR_null_baseline" and over_budget == 0 and edge == 0:
            verdict = "baseline_sane"
        elif profile["profile"] == "identity_closure_clean_zero_residuals" and over_budget == 0 and edge == 0:
            verdict = "zero_control_only_not_derivation"
        elif profile["profile"] == "fifth_force_alpha_1e_minus_5_unscored":
            verdict = "fifth_force_active_unscored_not_numeric_pass"
        elif profile["profile"] == "EH_operator_1e_minus_5" and over_budget == 0 and edge == 0:
            verdict = "inside_numeric_rows_but_operator_ledger_retained"
        elif over_budget == 0 and edge == 0:
            verdict = "inside_budget_if_parent_derives_coefficients"
        elif over_budget == 0:
            verdict = "edge_unstable_not_evidence"
        else:
            verdict = "fails_numeric_smoke"
        summary_rows.append(
            {
                "profile": profile["profile"],
                "inside_rows": inside,
                "edge_rows": edge,
                "over_budget_rows": over_budget,
                "worst_row": worst_row["row_id"],
                "worst_observable": worst_row["observable"],
                "worst_severity_ratio": worst_row["severity_ratio"],
                "verdict": verdict,
                "claim_policy": profile["claim_policy"],
                "description": profile["description"],
            }
        )
    return summary_rows


def row_worst_case_rows(result_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id in NUMERIC_ROW_EQUATIONS:
        subset = [row for row in result_rows if row["row_id"] == row_id]
        worst = max(subset, key=lambda row: float(row["severity_ratio"]))
        non_unit_subset = [row for row in subset if row["profile"] != "unit_coupling_stress"]
        worst_non_unit = max(non_unit_subset, key=lambda row: float(row["severity_ratio"]))
        rows.append(
            {
                "row_id": row_id,
                "observable": worst["observable"],
                "worst_profile": worst["profile"],
                "worst_severity_ratio": worst["severity_ratio"],
                "worst_non_unit_profile": worst_non_unit["profile"],
                "worst_non_unit_severity_ratio": worst_non_unit["severity_ratio"],
                "row_state": worst["row_state"],
                "claim_allowed": False,
            }
        )
    rows.sort(key=lambda row: float(row["worst_non_unit_severity_ratio"]), reverse=True)
    return rows


def symbolic_activation_rows(rows: list[dict[str, Any]], tightest_bounds: dict[str, float]) -> list[dict[str, Any]]:
    row_by_id = {row["row_id"]: row for row in rows}
    activation_rows: list[dict[str, Any]] = []
    for profile in PROFILE_SPECS:
        values = build_profile_values(profile, tightest_bounds)
        for row_id, channels in SYMBOLIC_ROW_CHANNELS.items():
            active_channels = [channel for channel in channels if abs(values[channel]) > 0.0]
            runner_row = row_by_id[row_id]
            if row_id == "R10_fifth_force":
                status = "active_unscored_needs_alpha_lambda_profile" if active_channels else "inactive_in_profile"
            else:
                status = "active_retained_operator_ledger" if active_channels else "inactive_in_profile"
            activation_rows.append(
                {
                    "profile": profile["profile"],
                    "row_id": row_id,
                    "observable": runner_row["observable"],
                    "row_state": runner_row["state"],
                    "active": bool(active_channels),
                    "active_channels": ";".join(active_channels),
                    "status": status,
                    "claim_allowed": False,
                }
            )
    return activation_rows


def fifth_force_probe_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for probe in FIFTH_FORCE_PROBES:
        lambda_m = float(probe["lambda_m"])
        radius_m = float(probe["radius_m"])
        alpha_y = float(probe["alpha_Y"])
        acceleration_ratio = alpha_y * (1.0 + radius_m / lambda_m) * math.exp(-radius_m / lambda_m)
        rows.append(
            {
                "lambda_m": lambda_m,
                "radius_m": radius_m,
                "alpha_Y": alpha_y,
                "a_extra_over_a_GR": acceleration_ratio,
                "formula": "alpha_Y*(1+r/lambda)*exp(-r/lambda)",
                "score_status": "diagnostic_only_no_alpha_lambda_source_curve_loaded",
                "claim_allowed": False,
            }
        )
    return rows


def gate_rows(
    source_rows: list[dict[str, Any]],
    result_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    aggregate_bound_rows: list[dict[str, Any]],
    activation_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    baseline = next(row for row in summary_rows if row["profile"] == "GR_null_baseline")
    suppression_target = next(
        row for row in summary_rows if row["profile"] == "derived_suppression_target_0p1_tightest_bound"
    )
    over_budget_profiles = [
        row["profile"] for row in summary_rows if int(row["over_budget_rows"]) > 0
    ]
    symbolic_active_count = sum(1 for row in activation_rows if row["active"])
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "same_evaluator_GR_null_baseline",
            "status": "pass" if baseline["verdict"] == "baseline_sane" else "fail",
            "evidence": f"worst severity {baseline['worst_severity_ratio']}",
        },
        {
            "gate": "channel_bound_requirements_written",
            "status": "pass" if aggregate_bound_rows else "fail",
            "evidence": f"{len(aggregate_bound_rows)} aggregate channel bounds written",
        },
        {
            "gate": "retained_residual_profiles_evaluated",
            "status": "pass" if result_rows else "fail",
            "evidence": f"{len(PROFILE_SPECS)} profiles x {len(NUMERIC_ROW_EQUATIONS)} numeric rows",
        },
        {
            "gate": "over_budget_smoke_detected",
            "status": "pass" if over_budget_profiles else "fail",
            "evidence": ";".join(over_budget_profiles),
        },
        {
            "gate": "conservative_suppression_target_inside",
            "status": "pass" if suppression_target["verdict"] == "inside_budget_if_parent_derives_coefficients" else "fail",
            "evidence": suppression_target["verdict"],
        },
        {
            "gate": "symbolic_fifth_force_and_operator_rows_retained",
            "status": "pass" if symbolic_active_count > 0 else "fail",
            "evidence": f"{symbolic_active_count} symbolic activations kept unpromoted",
        },
        {
            "gate": "local_GR_or_PPN_promoted",
            "status": "fail",
            "evidence": "numeric smoke is coefficient-pressure only; coefficients are not parent-derived",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows(summary_rows: list[dict[str, Any]], aggregate_bound_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    hardest = aggregate_bound_rows[:5]
    hardest_text = "; ".join(
        f"{row['channel']}<={row['tightest_solo_bound']} via {row['tightest_observable']}"
        for row in hardest
    )
    failed_profiles = [
        row["profile"] for row in summary_rows if row["verdict"] == "fails_numeric_smoke"
    ]
    return [
        {
            "status": STATUS,
            "decision": "Checkpoint 400 converts runner-v3 from row-level toy controls into a channel-level numeric smoke evaluator. GR/null is sane. A conservative 0.1-tightest-bound profile stays inside numeric locks only by inserted suppressions. Edge, floor, source-charge, boundary/domain/flux, Gdot, and unit profiles expose how violently several local rows fail without parent-derived zero/suppression laws. This is useful pressure, not a PPN or local-GR pass.",
            "hardest_channel_bounds": hardest_text,
            "failed_profiles": ";".join(failed_profiles),
            "local_GR_claim_allowed": False,
            "PPN_pass_claim_allowed": False,
            "claim_ceiling": CLAIM_CEILING,
            "next_target": NEXT_TARGET,
        }
    ]


def next_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "target": NEXT_TARGET,
            "task": "attempt the parent matter-selector theorem that would turn identity closure from labelled closure into derived WEP/coframe suppression",
            "pass_condition": "R0 becomes derived_zero or remains explicitly closure_only with no promotion",
        },
        {
            "priority": 2,
            "target": "402-EH-source-normalization-parent-pair.md",
            "task": "attempt EH operator selection and measured-GM/source-normalization theorem pair",
            "pass_condition": "gamma/beta/source-normalization rows either derive zero or receive explicit retained coefficients",
        },
        {
            "priority": 3,
            "target": "403-boundary-domain-flux-nohair-numeric-contract.md",
            "task": "use the hardest channel bounds to attack boundary/domain/flux no-hair rather than prose-close them",
            "pass_condition": "alpha2/alpha3/xi/Gdot channels are theorem-zero or quantitatively coefficient-mapped",
        },
    ]


def format_float(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if number == 0.0:
        return "0"
    if abs(number) < 1.0e-3 or abs(number) >= 1.0e4:
        return f"{number:.3e}"
    return f"{number:.6g}"


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_checkpoint_markdown(
    run_dir: Path,
    summary_rows: list[dict[str, Any]],
    aggregate_bound_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, Any]],
    decision: list[dict[str, Any]],
) -> None:
    hardest_rows = [
        {
            "channel": row["channel"],
            "bound": format_float(row["tightest_solo_bound"]),
            "row": row["tightest_row"],
            "observable": row["tightest_observable"],
        }
        for row in aggregate_bound_rows[:10]
    ]
    summary_table_rows = [
        {
            "profile": row["profile"],
            "over": row["over_budget_rows"],
            "worst": row["worst_observable"],
            "severity": format_float(row["worst_severity_ratio"]),
            "verdict": row["verdict"],
        }
        for row in summary_rows
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 400 - Runner-v3 Numeric Smoke Extension

Private local-bound/numeric-smoke checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, boundary, bulk, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 397 had a sane same-pipeline GR/null baseline, but mostly toy row-level controls. Checkpoint 400 pushes one step harder: each open local-GR blocker is represented as an explicit residual channel, each channel is mapped to the runner-v3 observable rows it can contaminate, and named coefficient profiles are scored against the same source-lock evaluator.

This is still not a derivation. It is a pressure map for the derivation programme.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/runner_v3_numeric_smoke_extension.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. What Changed

The new evaluator writes:

| Artifact | Role |
| --- | --- |
| `row_equation_map.csv` | symbolic residual equation for each runner-v3 row |
| `channel_map.csv` | parent-action residual channels mapped to affected observables |
| `channel_bound_requirements.csv` | per-row solo bounds for each channel |
| `aggregate_channel_bounds.csv` | tightest required suppression per channel |
| `profile_inputs.csv` | explicit coefficient values used in each smoke profile |
| `numeric_profile_results.csv` | profile x observable severity ratios |
| `symbolic_residual_activation.csv` | fifth-force/operator debts retained unscored |
| `fifth_force_probe.csv` | diagnostic Yukawa alpha(lambda) acceleration ratios, not a source-bound score |

## 4. Hardest Suppressions

The brutal local rows are not gamma and beta first. They are WEP/source, direct coframe if identity is not derived, alpha3/Ward flux, Gdot/G drift, and alpha2/domain-vector leakage.

{markdown_table(hardest_rows, ["channel", "bound", "row", "observable"])}

## 5. Profile Results

{markdown_table(summary_table_rows, ["profile", "over", "worst", "severity", "verdict"])}

Interpretation:

- `GR_null_baseline` passing means the evaluator is sane before judging MTS.
- `derived_suppression_target_0p1_tightest_bound` passing means the path is numerically possible if the parent action derives those suppressions.
- `edge_tightest_bound` becoming unstable means budget-edge claims are not evidence.
- `identity_branch_nonclosure_floor_1e_minus_12` failing shows that even tiny unowned source/flux/time residues can kill the local branch.
- Fifth-force and non-EH operator activations remain retained debts, not wins or scalar failures.

## 6. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 7. Decision

{decision[0]["decision"]}

Strongest honest read: this is not grim in the “dead theory” sense. It is grim in the useful engineering sense: the tolerances are now explicit. If MTS can derive identity/coframe selection, Ward-owned flux, source-normalized measured GM, no physical domain/projector vector leakage, and EH-only local exterior, the local-GR route has a clear shape. If those remain inserted suppressions, the local branch stays closure-only.

## 8. Next Target

`{NEXT_TARGET}`

Try to turn the cleanest closure into an actual parent theorem:

```text
delta S_matter / delta Z_I | e = 0
```

for every nonmetric local selector variable `Z_I`, or keep `R0` explicitly labelled as closure-only.
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    rows = runner_rows()
    requirement_rows = channel_bound_requirement_rows(rows)
    aggregate_bound_rows = aggregate_channel_bound_rows(requirement_rows)
    tightest_bounds = tightest_channel_bounds(requirement_rows)
    numeric_results = evaluate_numeric_profiles(rows, tightest_bounds)
    summary_rows = profile_summary_rows(numeric_results)
    activation_rows = symbolic_activation_rows(rows, tightest_bounds)
    gate_result_rows = gate_rows(
        source_rows,
        numeric_results,
        summary_rows,
        aggregate_bound_rows,
        activation_rows,
    )
    decision = decision_rows(summary_rows, aggregate_bound_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "row_equation_map.csv", row_equation_rows(rows))
    write_csv(results_dir / "channel_map.csv", channel_map_rows(rows))
    write_csv(results_dir / "channel_bound_requirements.csv", requirement_rows)
    write_csv(results_dir / "aggregate_channel_bounds.csv", aggregate_bound_rows)
    write_csv(results_dir / "profile_inputs.csv", profile_input_rows(tightest_bounds))
    write_csv(results_dir / "numeric_profile_results.csv", numeric_results)
    write_csv(results_dir / "profile_summary.csv", summary_rows)
    write_csv(results_dir / "row_worst_case_summary.csv", row_worst_case_rows(numeric_results))
    write_csv(results_dir / "symbolic_residual_activation.csv", activation_rows)
    write_csv(results_dir / "fifth_force_probe.csv", fifth_force_probe_rows())
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", decision)
    write_csv(results_dir / "next_queue.csv", next_queue_rows())

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    failed_profiles = [
        row["profile"] for row in summary_rows if row["verdict"] == "fails_numeric_smoke"
    ]
    baseline = next(row for row in summary_rows if row["profile"] == "GR_null_baseline")
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "numeric_rows": len(NUMERIC_ROW_EQUATIONS),
        "symbolic_rows": len(SYMBOLIC_ROW_CHANNELS),
        "profiles": len(PROFILE_SPECS),
        "aggregate_channel_bounds": len(aggregate_bound_rows),
        "GR_null_baseline_verdict": baseline["verdict"],
        "failed_numeric_profiles": failed_profiles,
        "derived_local_GR_claim_allowed": False,
        "PPN_pass_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, summary_rows, aggregate_bound_rows, gate_result_rows, decision)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 400 runner-v3 numeric smoke extension artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()

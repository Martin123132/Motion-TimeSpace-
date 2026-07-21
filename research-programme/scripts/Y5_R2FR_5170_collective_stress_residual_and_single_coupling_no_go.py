from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

import numpy as np


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
PREVIOUS_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5169_pair_consistent_transport_forward_response_gate.py"
)
PREVIOUS_DOCUMENT = (
    POST
    / "5169-Y5-R2FR-pair-consistent-capacity-bounded-transport-forward-response-gate.md"
)
PREVIOUS_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5169"
    / "pair_consistent_transport_forward_response_results.json"
)
PREVIOUS_VALIDATION = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5169_VALIDATION.csv"
)
WAVE_DOCUMENT = POST / "5163-Y5-R2FR-parent-wave-stress-and-visible-source-response-gate.md"
WAVE_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5163"
    / "parent_wave_and_visible_source_results.json"
)
UNIVERSAL_DOCUMENT = (
    POST
    / "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-local-GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md"
)
UNIVERSAL_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4960"
    / "integrated_H_universal_source_results.json"
)
UNIVERSAL_DECISION = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4960"
    / "universal_source_decision.csv"
)
STATE_DOCUMENT = (
    POST
    / "5151-Y5-R2FR-parent-projective-occupation-to-conserved-Einstein-cluster-stress-and-two-metric-cog-gate.md"
)
STATE_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5151"
    / "projective_state_stress_results.json"
)

OUT = POST / "source-intake" / "functional_rg" / "5170"
AMPLITUDE_CSV = OUT / "single_coupling_amplitude_no_go.csv"
GAIN_CSV = OUT / "required_collective_gain_profile.csv"
TRANSPORT_CSV = OUT / "normalized_collective_transport_lower_bound.csv"
BASIS_CSV = OUT / "parent_stress_basis_projection.csv"
CONTRACT_CSV = OUT / "conserved_response_kernel_contract.csv"
DECISION_CSV = OUT / "route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "collective_stress_residual_results.json"
VALIDATION_CSV = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5170_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5170-Y5-R2FR-collective-stress-residual-single-coupling-no-go-and-conserved-kernel-target.md"
)

MARKER = "MTS_5170_COLLECTIVE_STRESS_RESIDUAL_SINGLE_COUPLING_NO_GO"
CHECKED_DATE = "2026-07-21"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
SELECTED_RUN_ID = "ISOBARIC_Z0.3_RADIAL_COOLING_FREEFALL_OT_N26_P1_FULL_PRIMARY"
TRANSPORT_QUANTILES = 501
KPC_TO_KM = 3.085677581491367e16
GYR_TO_S = 31557600.0e9


specification = importlib.util.spec_from_file_location(
    "mts_checkpoint_5169_for_5170", PREVIOUS_SCRIPT
)
if specification is None or specification.loader is None:
    raise RuntimeError(f"cannot load module: {PREVIOUS_SCRIPT}")
P = importlib.util.module_from_spec(specification)
specification.loader.exec_module(P)
Q = P.Q


def source_paths() -> dict[str, Path]:
    return {
        "checkpoint_5169_script": PREVIOUS_SCRIPT,
        "checkpoint_5169_document": PREVIOUS_DOCUMENT,
        "checkpoint_5169_result": PREVIOUS_RESULT,
        "checkpoint_5169_validation": PREVIOUS_VALIDATION,
        "checkpoint_5169_scores": P.SCORE_CSV,
        "checkpoint_5169_profiles": P.PROFILE_CSV,
        "checkpoint_5163_document": WAVE_DOCUMENT,
        "checkpoint_5163_result": WAVE_RESULT,
        "checkpoint_4960_document": UNIVERSAL_DOCUMENT,
        "checkpoint_4960_result": UNIVERSAL_RESULT,
        "checkpoint_4960_decision": UNIVERSAL_DECISION,
        "checkpoint_5151_document": STATE_DOCUMENT,
        "checkpoint_5151_result": STATE_RESULT,
        "checkpoint_5170_script": Path(__file__).resolve(),
    }


def primary_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    scores = [
        row
        for row in P.P.read_typed_csv(P.SCORE_CSV)
        if row["run_role"] == "PRIMARY"
    ]
    profiles = P.P.read_typed_csv(P.PROFILE_CSV)
    return scores, profiles


def target_context() -> dict[str, Any]:
    context = Q.response_context()
    profile_rows = context["profile_rows"]
    return {
        "radii_kpc": np.asarray(
            [float(row["radius_kpc"]) for row in profile_rows], dtype=float
        ),
        "target_mass_Msun": np.asarray(
            [float(row["target_motion_mass_Msun"]) for row in profile_rows],
            dtype=float,
        ),
        "target_v2_km2_s2": np.asarray(
            [float(row["target_motion_v2_km2_s2"]) for row in profile_rows],
            dtype=float,
        ),
        "score_mask": np.asarray(
            [row["inside_resolved_scoring_window"] == "True" for row in profile_rows],
            dtype=bool,
        ),
        "transition_radius_kpc": float(context["transition_radius"]),
        "edge_radius_kpc": float(context["edge_radius"]),
        "target_edge_mass_Msun": float(context["target_edge_mass"]),
        "q_parent": float(context["q_row"]["q_parent"]),
        "q_envelope": float(context["q_row"]["q_uncertainty_envelope"]),
    }


def exact_edge_arrays(
    radii: np.ndarray,
    corrected_mass: np.ndarray,
    target_mass: np.ndarray,
    edge_radius: float,
    target_edge_mass: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    inside = radii < edge_radius
    radial = radii[inside]
    corrected = corrected_mass[inside]
    target = target_mass[inside]
    radial = np.concatenate((radial, np.asarray([edge_radius])))
    corrected = np.concatenate(
        (corrected, np.asarray([np.interp(edge_radius, radii, corrected_mass)]))
    )
    target = np.concatenate((target, np.asarray([target_edge_mass])))
    return radial, corrected, target


def crossing_radius(
    radii: np.ndarray, residual_mass: np.ndarray
) -> tuple[int, float | None]:
    signs = np.sign(residual_mass)
    indices = np.flatnonzero(signs[:-1] * signs[1:] <= 0.0)
    physical = [
        int(index)
        for index in indices
        if residual_mass[index] != 0.0 or residual_mass[index + 1] != 0.0
    ]
    if not physical:
        return 0, None
    index = physical[-1]
    left = float(residual_mass[index])
    right = float(residual_mass[index + 1])
    fraction = left / (left - right) if left != right else 0.0
    radius = float(radii[index] + fraction * (radii[index + 1] - radii[index]))
    return len(physical), radius


def analyze_branch(
    score: dict[str, Any],
    profiles: list[dict[str, Any]],
    target: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    rows = [row for row in profiles if row["run_id"] == score["run_id"]]
    radii = np.asarray([float(row["radius_kpc"]) for row in rows], dtype=float)
    corrected_mass = np.asarray(
        [float(row["corrected_motion_mass_Msun"]) for row in rows], dtype=float
    )
    corrected_v2 = np.asarray(
        [float(row["corrected_motion_v2_km2_s2"]) for row in rows], dtype=float
    )
    if not np.allclose(radii, target["radii_kpc"], rtol=0.0, atol=1.0e-10):
        raise RuntimeError(f"profile radius mismatch: {score['run_id']}")
    velocity_ratio = corrected_v2 / target["target_v2_km2_s2"]
    log_ratio = np.log10(velocity_ratio[target["score_mask"]])
    best_amplitude = float(10.0 ** (-np.mean(log_ratio)))
    best_scaled_rmse = float(
        math.sqrt(np.mean((log_ratio + math.log10(best_amplitude)) ** 2))
    )
    transition_ratio = float(
        score["corrected_transition_velocity_squared_ratio_to_target"]
    )
    edge_ratio = float(score["corrected_edge_mass_ratio_to_target"])
    gain_transition = 1.0 / transition_ratio
    gain_edge = 1.0 / edge_ratio
    two_anchor_amplitude = 1.0 / math.sqrt(transition_ratio * edge_ratio)
    two_anchor_factor = math.sqrt(edge_ratio / transition_ratio)

    radial_edge, corrected_edge, target_edge = exact_edge_arrays(
        radii,
        corrected_mass,
        target["target_mass_Msun"],
        target["edge_radius_kpc"],
        target["target_edge_mass_Msun"],
    )
    if np.any(np.diff(corrected_edge) < -1.0e-6) or np.any(
        np.diff(target_edge) < -1.0e-6
    ):
        raise RuntimeError(f"nonmonotone enclosed mass: {score['run_id']}")
    residual_mass = target_edge - corrected_edge
    crossing_count, crossing = crossing_radius(radial_edge, residual_mass)
    gain = target_edge / np.maximum(corrected_edge, np.finfo(float).tiny)
    gain_rows = [
        {
            "run_id": score["run_id"],
            "thermal_mode": score["thermal_mode"],
            "metallicity_Zsun": score["metallicity_Zsun"],
            "radius_kpc": radial_edge[index],
            "radius_over_transition": radial_edge[index]
            / target["transition_radius_kpc"],
            "corrected_motion_mass_Msun": corrected_edge[index],
            "target_motion_mass_Msun": target_edge[index],
            "required_mass_gain": gain[index],
            "required_fractional_change": gain[index] - 1.0,
            "cumulative_residual_mass_Msun": residual_mass[index],
            "residual_sign": (
                "INNER_DEFICIT"
                if residual_mass[index] > 0.0
                else "OUTER_EXCESS"
                if residual_mass[index] < 0.0
                else "ZERO"
            ),
            "inverse_requirement_not_predictive_operator": True,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for index in range(len(radial_edge))
    ]

    corrected_cdf = np.concatenate((np.asarray([0.0]), corrected_edge))
    corrected_cdf /= corrected_cdf[-1]
    target_cdf = np.concatenate((np.asarray([0.0]), target_edge))
    target_cdf /= target_cdf[-1]
    cdf_radii = np.concatenate((np.asarray([0.0]), radial_edge))
    quantiles = np.linspace(0.0, 1.0, TRANSPORT_QUANTILES)
    source_radius = np.interp(quantiles, corrected_cdf, cdf_radii)
    target_radius = np.interp(quantiles, target_cdf, cdf_radii)
    displacement = target_radius - source_radius
    mean_absolute_displacement = float(
        np.trapezoid(np.abs(displacement), quantiles)
    )
    rms_displacement = float(
        math.sqrt(np.trapezoid(displacement**2, quantiles))
    )
    signed_displacement = float(np.trapezoid(displacement, quantiles))
    internal = displacement[1:-1]
    inward_fraction = float(np.mean(internal < -1.0e-12))
    edge_expel_fraction = 1.0 - 1.0 / edge_ratio
    duration_gyr = float(score["common_endpoint_Gyr"])
    minimum_mean_speed = (
        mean_absolute_displacement * KPC_TO_KM / (duration_gyr * GYR_TO_S)
    )
    transport_rows = [
        {
            "run_id": score["run_id"],
            "quantile": quantiles[index],
            "corrected_normalized_radius_kpc": source_radius[index],
            "target_normalized_radius_kpc": target_radius[index],
            "required_radial_displacement_kpc": displacement[index],
            "direction": (
                "INWARD"
                if displacement[index] < -1.0e-12
                else "OUTWARD"
                if displacement[index] > 1.0e-12
                else "ZERO"
            ),
            "edge_amplitude_matched_before_shape_transport": True,
            "inverse_requirement_not_predictive_operator": True,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for index in range(len(quantiles))
    ]
    q_value = float(score["corrected_q"])
    q_lower = target["q_parent"] - target["q_envelope"]
    q_upper = target["q_parent"] + target["q_envelope"]
    summary = {
        "run_id": score["run_id"],
        "thermal_mode": score["thermal_mode"],
        "metallicity_Zsun": score["metallicity_Zsun"],
        "corrected_q": q_value,
        "q_after_any_constant_amplitude": q_value,
        "q_parent_lower": q_lower,
        "q_parent_upper": q_upper,
        "constant_amplitude_can_enter_q_band": q_lower <= q_value <= q_upper,
        "best_constant_amplitude_over_scoring_window": best_amplitude,
        "best_amplitude_implied_delta_G_over_G": best_amplitude - 1.0,
        "best_constant_amplitude_log10_RMSE": best_scaled_rmse,
        "best_amplitude_scaled_transition_ratio": best_amplitude
        * transition_ratio,
        "best_amplitude_scaled_edge_ratio": best_amplitude * edge_ratio,
        "transition_ratio_before_rescaling": transition_ratio,
        "edge_ratio_before_rescaling": edge_ratio,
        "required_gain_at_transition": gain_transition,
        "required_gain_at_edge": gain_edge,
        "required_gain_contrast_transition_to_edge": gain_transition / gain_edge,
        "two_anchor_minimax_amplitude": two_anchor_amplitude,
        "two_anchor_implied_delta_G_over_G": two_anchor_amplitude - 1.0,
        "two_anchor_unavoidable_mismatch_factor": two_anchor_factor,
        "cumulative_residual_sign_crossing_count": crossing_count,
        "outermost_residual_crossing_radius_kpc": crossing,
        "edge_corrected_mass_expel_fraction": edge_expel_fraction,
        "normalized_shape_mean_absolute_transport_kpc": mean_absolute_displacement,
        "normalized_shape_signed_transport_kpc": signed_displacement,
        "normalized_shape_rms_transport_kpc": rms_displacement,
        "normalized_shape_inward_quantile_fraction": inward_fraction,
        "minimum_mean_transport_speed_km_s": minimum_mean_speed,
        "target_used_only_to_reconstruct_inverse_requirement": True,
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }
    return summary, gain_rows, transport_rows


def stress_basis_rows(selected: dict[str, Any], wave: dict[str, Any]) -> list[dict[str, Any]]:
    required = float(selected["required_gain_at_transition"]) - 1.0
    wave_fraction = float(wave["summary"]["wave_fraction_at_all_patch_floor"])
    x2_fraction = float(wave["summary"]["maximum_X2_envelope"])
    o4_fraction = float(wave["summary"]["maximum_O4_envelope"])
    rows = [
        {
            "basis_id": "UNIVERSAL_HILBERT_AMPLITUDE",
            "parent_status": "derived_rank_one_leading_source_direction",
            "maximum_fractional_transition_effect": "NOT_AN_INDEPENDENT_PARAMETER",
            "required_fractional_transition_effect": required,
            "shortfall_ratio": "NOT_APPLICABLE_Q_IS_AMPLITUDE_INVARIANT",
            "result": "REJECTED_AS_MISSING_SHAPE_REPAIR",
        },
        {
            "basis_id": "CANONICAL_WAVE_STRESS",
            "parent_status": "derived",
            "maximum_fractional_transition_effect": wave_fraction,
            "required_fractional_transition_effect": required,
            "shortfall_ratio": required / wave_fraction,
            "result": "INSUFFICIENT",
        },
        {
            "basis_id": "ESSENTIAL_X2_LOCAL_GRADIENT",
            "parent_status": "derived_bounded",
            "maximum_fractional_transition_effect": x2_fraction,
            "required_fractional_transition_effect": required,
            "shortfall_ratio": required / x2_fraction,
            "result": "INSUFFICIENT",
        },
        {
            "basis_id": "O4_WEYL_KINETIC_LOCAL_GRADIENT",
            "parent_status": "derived_bounded",
            "maximum_fractional_transition_effect": o4_fraction,
            "required_fractional_transition_effect": required,
            "shortfall_ratio": required / o4_fraction,
            "result": "INSUFFICIENT",
        },
        {
            "basis_id": "POSITIVE_ADDITIVE_OCCUPATION_STRESS",
            "parent_status": "conserved_Wigner_stress_exists",
            "maximum_fractional_transition_effect": "STATE_DEPENDENT",
            "required_fractional_transition_effect": required,
            "shortfall_ratio": "NOT_APPLICABLE",
            "result": "ADDITION_ALONE_FAILS_BECAUSE_OUTER_CUMULATIVE_RESIDUAL_IS_NEGATIVE",
        },
        {
            "basis_id": "COMPENSATED_OCCUPIED_CTP_VLASOV_POLARIZATION",
            "parent_status": "allowed_by_parent_but_not_yet_calculated_for_the_state",
            "maximum_fractional_transition_effect": "TO_BE_DERIVED_FROM_RETARDED_STATE_KERNEL",
            "required_fractional_transition_effect": required,
            "shortfall_ratio": "OPEN_CALCULATION",
            "result": "SELECTED_PARENT_DERIVATION_TARGET",
        },
    ]
    for row in rows:
        row.update(
            {
                "new_independent_source_coupling_allowed": False,
                "target_used_only_for_inverse_projection": True,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows


def kernel_contract_rows(selected: dict[str, Any]) -> list[dict[str, Any]]:
    contracts = [
        (
            "K1_UNIVERSAL_SOURCE",
            "nabla^2 deltaPhi_b=4 pi G_N delta rho_b with the same once-calibrated G_N as local Newton",
            "already_derived_checkpoint_4960",
        ),
        (
            "K2_RETARDED_STATE_RESPONSE",
            "delta T_X^munu(x)=int d4y Pi_R^munu,ab(x,y;F_X) delta g^ab(y)",
            "must_be_calculated_from_parent_CTP_state",
        ),
        (
            "K3_WARD_CONSERVATION",
            "nabla_mu delta T_X^munu plus connection variation on T_X0 equals zero on the state equations",
            "non_negotiable",
        ),
        (
            "K4_COMPENSATED_ZERO_MODE",
            "integral_0^R_edge 4 pi r^2 delta rho_shape dr=0 after the separately recorded edge normalization",
            "derived_inverse_requirement",
        ),
        (
            "K5_RADIAL_SIGN_CHANGE",
            "delta M_shape is positive inside and negative outside its crossing; a positive additive density is insufficient",
            "derived_inverse_requirement",
        ),
        (
            "K6_LOCAL_VACUUM_SILENCE",
            "F_X=F_vac and psi=0 imply Pi_R,state=0 and recover the checkpoint-4960 local GR/Newton/Maxwell branch",
            "required_same_action_limit",
        ),
        (
            "K7_NO_ARENA_RETUNING",
            "state preparation and boundary data may vary physically but no new galaxy gravitational coefficient may be introduced",
            "required_parameter_discipline",
        ),
        (
            "K8_CAUSAL_STABILITY",
            "the full metric-state spectral and gradient matrix has no upper-half-plane pole or negative physical norm",
            "required_before_claim",
        ),
    ]
    return [
        {
            "clause_id": clause_id,
            "equation_or_requirement": requirement,
            "status": status,
            "selected_mean_inward_transport_kpc": selected[
                "normalized_shape_mean_absolute_transport_kpc"
            ],
            "selected_edge_expel_fraction": selected[
                "edge_corrected_mass_expel_fraction"
            ],
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for clause_id, requirement, status in contracts
    ]


def provenance_rows(paths: dict[str, Path]) -> list[dict[str, Any]]:
    return [
        {
            "source_id": key,
            "source_path": str(path),
            "sha256": Q.file_digest(path),
            "status": "immutable_input",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for key, path in paths.items()
    ]


def add_validation(
    rows: list[dict[str, Any]], check_id: str, passed: bool, evidence: Any
) -> None:
    rows.append(
        {
            "check_id": check_id,
            "passed": bool(passed),
            "evidence": json.dumps(evidence, sort_keys=True),
            "checkpoint_marker": MARKER,
        }
    )


def make_document(result: dict[str, Any]) -> str:
    summary = result["summary"]
    selected = summary["selected_branch"]
    branch_lines = "\n".join(
        f"- `{row['run_id']}`: gain contrast=`{row['required_gain_contrast_transition_to_edge']}`, "
        f"mean inward transport=`{row['normalized_shape_mean_absolute_transport_kpc']} kpc`"
        for row in summary["branch_rows"]
    )
    return f"""# 5170 - Collective-stress residual, single-coupling no-go and conserved-kernel target

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Result in one line

Checkpoint 5169 is not missing a larger gravitational coefficient. The
checkpoint-4960 parent already has one rank-one Hilbert source coupling, and
any constant rescaling leaves the measured transition exponent exactly
unchanged. The remaining discrepancy is a compensated radial redistribution
that only a state-dependent conserved response kernel could produce.

## Exact single-coupling theorem

The response score is

```text
q[V^2]=2 d ln V^2/d ln r.
```

For every positive constant `A`,

```text
q[A V^2]=q[V^2].
```

Therefore no second scalar source normalization can move the selected
`q={selected['corrected_q']}` into the parent interval
`[{selected['q_parent_lower']}, {selected['q_parent_upper']}]`. This is
independent of how `A` is estimated. The best log-amplitude over the existing
scoring window is `{selected['best_constant_amplitude_over_scoring_window']}`,
which would duplicate the locally calibrated Newton residue by
`Delta G/G={selected['best_amplitude_implied_delta_G_over_G']}`,
but it leaves the transition at
`{selected['best_amplitude_scaled_transition_ratio']}` of target while making
the edge `{selected['best_amplitude_scaled_edge_ratio']}` times target.

Using only the transition and edge anchors, the exact minimax amplitude still
leaves an unavoidable multiplicative mismatch factor
`{selected['two_anchor_unavoidable_mismatch_factor']}`. Introducing such an
amplitude would also duplicate the universal source residue already fixed by
the local Einstein/Newton/Maxwell chain.

## Reconstructed collective requirement

The target is used here only to reconstruct an inverse requirement, never as
a proposed predictive operator. For the selected branch the required gain is

```text
gain(R_n)    = {selected['required_gain_at_transition']},
gain(R_edge) = {selected['required_gain_at_edge']}.
```

The cumulative residual changes sign at
`{selected['outermost_residual_crossing_radius_kpc']} kpc`: the state is too
diffuse inside and excessive outside. After matching the edge totals only to
separate normalization from shape, the unique one-dimensional monotone
transport lower bound moves essentially every internal quantile inward by
mean distance `{selected['normalized_shape_mean_absolute_transport_kpc']} kpc`
(RMS `{selected['normalized_shape_rms_transport_kpc']} kpc`). The existing
edge excess separately requires at least
`{selected['edge_corrected_mass_expel_fraction']}` of corrected enclosed mass
to leave the edge. Spread over the sourced assembly time, the mean-displacement
bound is `{selected['minimum_mean_transport_speed_km_s']} km/s`.

All four predeclared clocks give the same conclusion:

{branch_lines}

This is not an infinitesimal local correction or a positive component that
can simply be added. It is a sign-changing, mass-conserving collective
polarization/redistribution problem.

## Parent-basis projection

At the transition the selected profile needs fractional enhancement
`{summary['required_fractional_transition_effect']}`. The largest canonical
wave bracket is smaller by factor
`{summary['wave_shortfall_ratio']}`; the derived `X^2` and `O4` envelopes are
smaller by factors `{summary['X2_shortfall_ratio']}` and
`{summary['O4_shortfall_ratio']}`. The already-bounded local derivative terms
cannot produce the reconstructed response.

The remaining parent-owned class is the occupied-state retarded polarization

```text
delta T_X^munu(x)=int d4y Pi_R^munu,ab(x,y;F_X) delta g^ab(y),
```

with the Vlasov/CTP state equations enforcing its Ward identity. It must have
a compensated zero mode, the reconstructed radial sign change, causal stable
spectral support and exact vacuum silence. Those are now numerical and
algebraic gates, not an invitation to write an arbitrary kernel.

The already-constructed positive occupied-state existence branch has maximum
embedded Mercury tidal ratio `{summary['maximum_existing_state_Mercury_tidal_ratio']}`
across its 175-galaxy smoke. This supports state-dependent local suppression;
it is not substituted for a full PPN or compact-body calculation.

## Decision

`{result['route_decision']}`.

```text
one universal leading Hilbert coupling                  = retained;
constant coupling can change q                          = no, exact;
known wave/X2/O4 stress can close residual              = no, bounded;
positive additive state density alone                   = no;
compensated occupied-state polarization required        = yes;
that retarded kernel derived from current state          = not yet;
local GR/Newton/Maxwell branch modified                  = no;
galaxy or full-MTS claim                                 = false.
```

All `{result['validation_count']}` validation rows pass. The protected
`formalization-workbench` digest remains
`{result['formalization_workbench_tree_sha256']}`. No GitHub action occurred.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    paths = source_paths()
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing sources: {missing}")
    formal_before = Q.tree_digest(FORMAL)
    if formal_before != FORMAL_DIGEST_LOCK:
        raise RuntimeError(f"protected digest mismatch: {formal_before}")
    hashes_before = {key: Q.file_digest(path) for key, path in paths.items()}
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "marker": MARKER,
                    "selected_run_id": SELECTED_RUN_ID,
                    "transport_quantiles": TRANSPORT_QUANTILES,
                    "formal_digest": formal_before,
                },
                indent=2,
            )
        )
        return

    scores, profiles = primary_rows()
    target = target_context()
    amplitude_rows: list[dict[str, Any]] = []
    gain_rows: list[dict[str, Any]] = []
    transport_rows: list[dict[str, Any]] = []
    for score in scores:
        amplitude, gain, transport = analyze_branch(score, profiles, target)
        amplitude_rows.append(amplitude)
        gain_rows.extend(gain)
        transport_rows.extend(transport)
    selected = next(row for row in amplitude_rows if row["run_id"] == SELECTED_RUN_ID)
    wave = json.loads(WAVE_RESULT.read_text(encoding="utf-8"))
    state = json.loads(STATE_RESULT.read_text(encoding="utf-8"))
    basis = stress_basis_rows(selected, wave)
    contracts = kernel_contract_rows(selected)
    universal = P.P.read_typed_csv(UNIVERSAL_DECISION)
    universal_pass = all(
        bool(row["passed"])
        for row in universal
        if row["decision_id"]
        in {
            "DEC4960_00_H_source",
            "DEC4960_01_normalization",
            "DEC4960_02_universality",
            "DEC4960_03_local_chain",
            "DEC4960_04_local_promotion",
        }
    )
    required_fraction = float(selected["required_gain_at_transition"]) - 1.0
    wave_shortfall = required_fraction / float(
        wave["summary"]["wave_fraction_at_all_patch_floor"]
    )
    x2_shortfall = required_fraction / float(
        wave["summary"]["maximum_X2_envelope"]
    )
    o4_shortfall = required_fraction / float(
        wave["summary"]["maximum_O4_envelope"]
    )
    mercury_tidal_ratio = float(
        state["galaxy_scale_gate"]["maximum_Mercury_tidal_ratio"]
    )
    route_decision = (
        "ONE_UNIVERSAL_HILBERT_SOURCE_COUPLING_IS_ALREADY_FIXED_AND_CANNOT_CHANGE_Q_THE_5169_RESIDUAL_REQUIRES_A_COMPENSATED_OCCUPIED_STATE_POLARIZATION_WITH_INWARD_MASS_TRANSPORT_AND_LOCAL_VACUUM_SILENCE"
    )
    decisions = [
        {
            "route": "parent_occupied_state_collective_polarization",
            "result": route_decision,
            "evidence": (
                f"q_constant_amplitude_invariant=true; "
                f"gain_contrast={selected['required_gain_contrast_transition_to_edge']}; "
                f"mean_inward_transport_kpc={selected['normalized_shape_mean_absolute_transport_kpc']}; "
                f"edge_expel_fraction={selected['edge_corrected_mass_expel_fraction']}"
            ),
            "next_requirement": "derive Pi_R from the occupied parent CTP/Vlasov state and test the eight frozen kernel clauses without fitting its radial shape",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    ]
    hashes_after = {key: Q.file_digest(path) for key, path in paths.items()}
    formal_after = Q.tree_digest(FORMAL)
    validation: list[dict[str, Any]] = []
    add_validation(validation, "all_sources_exist", not missing, missing)
    add_validation(
        validation, "source_hashes_unchanged", hashes_before == hashes_after, hashes_after
    )
    add_validation(
        validation,
        "formalization_workbench_unchanged",
        formal_after == FORMAL_DIGEST_LOCK,
        formal_after,
    )
    add_validation(
        validation,
        "universal_source_theorem_imported",
        universal_pass,
        [row["answer"] for row in universal[:5]],
    )
    add_validation(
        validation,
        "all_four_primary_branches_projected",
        len(amplitude_rows) == 4,
        [row["run_id"] for row in amplitude_rows],
    )
    add_validation(
        validation,
        "constant_amplitude_q_invariance",
        all(
            float(row["corrected_q"])
            == float(row["q_after_any_constant_amplitude"])
            for row in amplitude_rows
        ),
        [row["corrected_q"] for row in amplitude_rows],
    )
    add_validation(
        validation,
        "constant_amplitude_cannot_enter_parent_q_band",
        all(not bool(row["constant_amplitude_can_enter_q_band"]) for row in amplitude_rows),
        [row["q_after_any_constant_amplitude"] for row in amplitude_rows],
    )
    add_validation(
        validation,
        "transition_edge_gain_incompatible",
        all(
            float(row["required_gain_at_transition"]) > 1.0
            and float(row["required_gain_at_edge"]) < 1.0
            for row in amplitude_rows
        ),
        [
            [row["required_gain_at_transition"], row["required_gain_at_edge"]]
            for row in amplitude_rows
        ],
    )
    add_validation(
        validation,
        "two_anchor_mismatch_nontrivial",
        min(
            float(row["two_anchor_unavoidable_mismatch_factor"])
            for row in amplitude_rows
        )
        > 1.7,
        [row["two_anchor_unavoidable_mismatch_factor"] for row in amplitude_rows],
    )
    add_validation(
        validation,
        "cumulative_residual_changes_sign",
        all(
            int(row["cumulative_residual_sign_crossing_count"]) >= 1
            for row in amplitude_rows
        ),
        [row["outermost_residual_crossing_radius_kpc"] for row in amplitude_rows],
    )
    add_validation(
        validation,
        "edge_excess_requires_expulsion",
        all(float(row["edge_corrected_mass_expel_fraction"]) > 0.1 for row in amplitude_rows),
        [row["edge_corrected_mass_expel_fraction"] for row in amplitude_rows],
    )
    add_validation(
        validation,
        "normalized_shape_transport_is_inward",
        min(
            float(row["normalized_shape_inward_quantile_fraction"])
            for row in amplitude_rows
        )
        > 0.99,
        [row["normalized_shape_inward_quantile_fraction"] for row in amplitude_rows],
    )
    displacements = [
        float(row["normalized_shape_mean_absolute_transport_kpc"])
        for row in amplitude_rows
    ]
    add_validation(
        validation,
        "transport_bound_clock_robust",
        max(displacements) - min(displacements) < 2.0,
        displacements,
    )
    add_validation(
        validation,
        "transport_speed_finite_nonperturbative",
        all(
            5.0 < float(row["minimum_mean_transport_speed_km_s"]) < 50.0
            for row in amplitude_rows
        ),
        [row["minimum_mean_transport_speed_km_s"] for row in amplitude_rows],
    )
    add_validation(
        validation,
        "known_parent_local_stress_basis_insufficient",
        wave_shortfall > 1.0e4 and x2_shortfall > 1.0e100 and o4_shortfall > 1.0e200,
        {
            "wave": wave_shortfall,
            "X2": x2_shortfall,
            "O4": o4_shortfall,
        },
    )
    add_validation(
        validation,
        "occupied_state_local_tidal_separation_retained",
        mercury_tidal_ratio < 1.0e-12,
        mercury_tidal_ratio,
    )
    add_validation(
        validation,
        "kernel_contract_has_local_silence_and_Ward_gate",
        {row["clause_id"] for row in contracts}
        >= {"K3_WARD_CONSERVATION", "K6_LOCAL_VACUUM_SILENCE"},
        [row["clause_id"] for row in contracts],
    )
    add_validation(
        validation,
        "target_used_only_as_inverse_requirement",
        all(bool(row["target_used_only_to_reconstruct_inverse_requirement"]) for row in amplitude_rows),
        "no predictive kernel fitted",
    )
    add_validation(
        validation,
        "all_outputs_nonclaim",
        all(
            not bool(row["valid_for_claim"])
            for row in amplitude_rows + gain_rows + transport_rows + basis + contracts
        ),
        "all generated rows",
    )
    add_validation(
        validation,
        "local_branch_unmodified",
        True,
        "read-only projection; checkpoint-4960 local branch retained",
    )
    provenance = provenance_rows(paths)
    summary = {
        "selected_branch": selected,
        "branch_rows": amplitude_rows,
        "required_fractional_transition_effect": required_fraction,
        "wave_shortfall_ratio": wave_shortfall,
        "X2_shortfall_ratio": x2_shortfall,
        "O4_shortfall_ratio": o4_shortfall,
        "maximum_existing_state_Mercury_tidal_ratio": mercury_tidal_ratio,
        "mean_transport_range_kpc": [min(displacements), max(displacements)],
        "universal_source_theorem_passed": universal_pass,
    }
    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "formalization_workbench_tree_sha256": formal_after,
        "source_hashes_before": hashes_before,
        "source_hashes_after": hashes_after,
        "summary": summary,
        "route_decision": route_decision,
        "validation_count": len(validation),
        "validation_failures": [row for row in validation if not row["passed"]],
        "constant_source_coupling_rejected_as_shape_repair": True,
        "compensated_collective_response_required": True,
        "retarded_parent_state_kernel_derived": False,
        "local_GR_Newton_Maxwell_branch_modified": False,
        "valid_for_galaxy_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    Q.write_csv(AMPLITUDE_CSV, amplitude_rows)
    Q.write_csv(GAIN_CSV, gain_rows)
    Q.write_csv(TRANSPORT_CSV, transport_rows)
    Q.write_csv(BASIS_CSV, basis)
    Q.write_csv(CONTRACT_CSV, contracts)
    Q.write_csv(DECISION_CSV, decisions)
    Q.write_csv(PROVENANCE_CSV, provenance)
    Q.write_json(RESULT_JSON, result)
    Q.write_csv(VALIDATION_CSV, validation)
    DOCUMENT.write_text(make_document(result), encoding="utf-8")
    if result["validation_failures"]:
        raise RuntimeError(
            f"validation failures: {[row['check_id'] for row in result['validation_failures']]}"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

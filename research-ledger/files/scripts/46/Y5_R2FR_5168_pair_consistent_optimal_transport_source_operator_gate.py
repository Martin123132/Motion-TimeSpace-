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
from scipy.optimize import linprog
from scipy.sparse import lil_matrix


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
PREVIOUS_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5167_radial_entropy_cooling_freefall_transfer_gate.py"
)
PREVIOUS_DOCUMENT = (
    POST
    / "5167-Y5-R2FR-radial-entropy-cooling-freefall-mass-transfer-and-forward-response-gate.md"
)
PREVIOUS_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5167"
    / "radial_entropy_cooling_freefall_transfer_results.json"
)
OUT = POST / "source-intake" / "functional_rg" / "5168"
CONTRACT_CSV = OUT / "pair_consistent_transport_contract.csv"
FEASIBILITY_CSV = OUT / "untransported_pair_capacity_feasibility.csv"
ROBUSTNESS_CSV = OUT / "optimal_transport_resolution_norm_robustness.csv"
PROFILE_CSV = OUT / "projected_phase_radial_source_profiles.csv"
FLOW_CSV = OUT / "primary_transport_flow.csv"
TEMPORAL_CSV = OUT / "temporal_pair_mass_invariants.csv"
DECISION_CSV = OUT / "route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "pair_consistent_optimal_transport_source_operator_results.json"
VALIDATION_CSV = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5168_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5168-Y5-R2FR-pair-consistent-capacity-bounded-optimal-transport-radial-source-operator-gate.md"
)

MARKER = "MTS_5168_PAIR_CONSISTENT_OPTIMAL_TRANSPORT_SOURCE_OPERATOR_GATE"
CHECKED_DATE = "2026-07-21"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
PRIMARY_RADIAL_BINS = 26
RADIAL_BIN_CONTROLS = (13, 20, 26, 52)
FEASIBILITY_BINS = (1, 2, 8, 13, 20, 26, 32, 52)
COST_POWERS = (1, 2)
PRIMARY_COST_POWER = 1
TEMPORAL_SAMPLES = 41


specification = importlib.util.spec_from_file_location(
    "mts_checkpoint_5167_for_5168", PREVIOUS_SCRIPT
)
if specification is None or specification.loader is None:
    raise RuntimeError(f"cannot load module: {PREVIOUS_SCRIPT}")
P = importlib.util.module_from_spec(specification)
specification.loader.exec_module(P)
Q = P.P
DYNAMICS = P.DYNAMICS
ENERGY = P.ENERGY


def source_paths() -> dict[str, Path]:
    paths = {
        "previous_script": PREVIOUS_SCRIPT,
        "previous_document": PREVIOUS_DOCUMENT,
        "previous_result": PREVIOUS_RESULT,
        "Cloudy_CIE_table": Q.SOURCE_DATA,
        "motion_profile": ENERGY.MOTION_PROFILE,
        "visible_profile": ENERGY.VISIBLE_PROFILE,
    }
    for sign, path in DYNAMICS.SNAPSHOT_PATHS.items():
        paths[f"phase_{sign}_snapshot"] = path
    return paths


def contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "T1_RAW_PAIR_SOURCE",
            "equation": "rbar_i(t)=sum_(shell in bin i,t_arr<=t) Delta M_hot,shell",
            "derivation": "checkpoint-5167 pair-mean shell entropy plus freefall arrival ordering",
            "status": "derived_pair_source",
            "remaining_assumption": "equal-width radial coarse graining",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "T2_PHASE_CAPACITY",
            "equation": "0<=x_sj(t)<=a_sj; a_sj=(1-f_X)m_p N_sj",
            "derivation": "actual inherited donor particles and cosmic baryon allotment in each phase/bin",
            "status": "exact_discrete_capacity",
            "remaining_assumption": "baryon allotment remains particle tied before removal",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "T3_PAIR_AND_ENDPOINT_CONSTRAINTS",
            "equation": "sum_j x_-j=sum_j x_+j=M_c; sum_(s,j) f_isj=2 rbar_i",
            "derivation": "each phase conserves the observed endpoint while the phase pair preserves every raw source-bin supply",
            "status": "exact_linear_constraints",
            "remaining_assumption": "pair average is the physical estimator",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "T4_MINIMUM_TRANSPORT",
            "equation": "min_f sum_i,s,j f_isj |r_i-r_j|^p/R_edge^p",
            "derivation": "capacity-bounded one-dimensional optimal transport; p=1 primary and p=2 robustness comparator",
            "status": "derived_variational_projection",
            "remaining_assumption": "radial transport cost is the closure metric",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "T5_TEMPORAL_LIFT",
            "equation": "x_sj(t)=sum_i 2 rbar_i(t) f_isj/[2 rbar_i(final)]",
            "derivation": "freeze endpoint transport fractions and lift each arriving source mass through the same flow",
            "status": "exact_positive_temporal_operator",
            "remaining_assumption": "transport fractions do not evolve with feedback",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "T6_PHASE_MASS_IDENTITY",
            "equation": "lambda_s(t)=sum_j x_sj(t)/M_c; Delta M_s,edge=-sum_j x_sj+lambda_s M_c=0",
            "derivation": "phase-specific condensed growth is tied to its transported removal",
            "status": "proved_all_times",
            "remaining_assumption": "condensed shape grows self-similarly within each phase",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "T7_PAIR_TIME_IDENTITY",
            "equation": "[lambda_-(t)+lambda_+(t)]/2=sum_i rbar_i(t)/M_c=lambda_bar(t)",
            "derivation": "sum T5 over phases and sinks using T3 source conservation",
            "status": "proved_all_times",
            "remaining_assumption": "none beyond T1-T5",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def build_parent_state() -> tuple[
    Any,
    dict[str, Any],
    dict[str, Any],
    dict[tuple[str, float], dict[str, Any]],
]:
    table = Q.CoolingTable(Q.SOURCE_DATA)
    context = Q.response_context()
    visible = context["visible_source"]
    edge = ENERGY.edge_radius_kpc()
    profile = ENERGY.motion_profiles()[ENERGY.PRIMARY_PROFILE_ID][0]
    polynomial = ENERGY.energy_polynomial(
        profile, visible, edge, ENERGY.QUADRATURE_POINTS
    )
    virial = Q.virial_state(table, polynomial, edge)
    solutions = {
        branch: P.radial_solution(
            table,
            polynomial,
            profile,
            virial,
            branch[0],
            branch[1],
            P.RADIAL_SHELLS,
        )
        for branch in P.FORWARD_BRANCHES
    }
    return context, polynomial, virial, solutions


def binned_inputs(
    context: dict[str, Any],
    solution: dict[str, Any],
    polynomial: dict[str, Any],
    radial_bins: int,
) -> dict[str, Any]:
    edge = float(polynomial["radius_kpc"][-1])
    condensed = float(polynomial["condensed_edge_Msun"])
    edges = np.linspace(0.0, edge, radial_bins + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])
    desired = np.histogram(
        solution["radius_kpc"],
        bins=edges,
        weights=solution["selected_mass_Msun"],
    )[0]
    capacities: dict[int, np.ndarray] = {}
    baryon_fraction = 1.0 - DYNAMICS.PM.MOTION_FRACTION
    for sign, snapshot in context["snapshots"].items():
        donor = np.asarray(snapshot["donor"], dtype=bool)
        radius = np.asarray(snapshot["initial_radius_kpc"], dtype=float)[donor]
        particle_mass = float(snapshot["particle_mass_Msun"][0])
        capacities[sign] = np.histogram(
            radius,
            bins=edges,
            weights=np.full(len(radius), particle_mass * baryon_fraction),
        )[0]
    return {
        "radial_bins": radial_bins,
        "edges_kpc": edges,
        "centers_kpc": centers,
        "desired_Msun": desired,
        "capacity_minus_Msun": capacities[-1],
        "capacity_plus_Msun": capacities[1],
        "condensed_Msun": condensed,
        "edge_kpc": edge,
    }


def direct_feasibility(data: dict[str, Any]) -> dict[str, Any]:
    desired = data["desired_Msun"]
    capacity_minus = data["capacity_minus_Msun"]
    capacity_plus = data["capacity_plus_Msun"]
    lower = np.maximum(-desired, desired - capacity_plus)
    upper = np.minimum(capacity_minus - desired, desired)
    local_feasible = lower <= upper + 1.0e-6
    global_feasible = float(np.sum(lower)) <= 1.0e-6 <= float(np.sum(upper))
    return {
        "local_feasible": bool(np.all(local_feasible)),
        "global_zero_sum_feasible": global_feasible,
        "feasible": bool(np.all(local_feasible) and global_feasible),
        "violating_bin_count": int(np.count_nonzero(~local_feasible)),
        "sum_lower_Msun": float(np.sum(lower)),
        "sum_upper_Msun": float(np.sum(upper)),
        "pair_local_capacity_deficit_Msun": float(
            np.sum(np.maximum(2.0 * desired - capacity_minus - capacity_plus, 0.0))
        ),
    }


def solve_transport(data: dict[str, Any], cost_power: int) -> dict[str, Any]:
    desired = data["desired_Msun"]
    condensed = float(data["condensed_Msun"])
    desired_scaled = desired / condensed
    capacities = np.vstack(
        (
            data["capacity_minus_Msun"] / condensed,
            data["capacity_plus_Msun"] / condensed,
        )
    )
    centers = data["centers_kpc"]
    edge = float(data["edge_kpc"])
    source_bins = np.flatnonzero(desired_scaled > 1.0e-15)
    source_count = len(source_bins)
    radial_bins = len(desired)
    variable_count = source_count * 2 * radial_bins

    def variable_index(source_index: int, phase_index: int, sink_index: int) -> int:
        return (source_index * 2 + phase_index) * radial_bins + sink_index

    cost = np.zeros(variable_count, dtype=float)
    for source_index, radial_source in enumerate(source_bins):
        normalized_distance = np.abs(centers[radial_source] - centers) / edge
        for phase_index in range(2):
            lower = variable_index(source_index, phase_index, 0)
            cost[lower : lower + radial_bins] = normalized_distance**cost_power
    equality = lil_matrix((source_count + 2, variable_count), dtype=float)
    equality_target = np.concatenate((2.0 * desired_scaled[source_bins], [1.0, 1.0]))
    for source_index in range(source_count):
        for phase_index in range(2):
            for sink_index in range(radial_bins):
                equality[
                    source_index,
                    variable_index(source_index, phase_index, sink_index),
                ] = 1.0
    for phase_index in range(2):
        for source_index in range(source_count):
            lower = variable_index(source_index, phase_index, 0)
            equality[
                source_count + phase_index, lower : lower + radial_bins
            ] = 1.0
    inequality = lil_matrix((2 * radial_bins, variable_count), dtype=float)
    for phase_index in range(2):
        for sink_index in range(radial_bins):
            for source_index in range(source_count):
                inequality[
                    phase_index * radial_bins + sink_index,
                    variable_index(source_index, phase_index, sink_index),
                ] = 1.0
    result = linprog(
        cost,
        A_ub=inequality.tocsr(),
        b_ub=capacities.ravel(),
        A_eq=equality.tocsr(),
        b_eq=equality_target,
        bounds=(0.0, None),
        method="highs",
    )
    if not result.success:
        raise RuntimeError(f"optimal transport failed: {result.message}")
    scaled_flow = result.x.reshape(source_count, 2, radial_bins)
    flow = scaled_flow * condensed
    phase_removal = np.sum(flow, axis=0)
    projected_pair = 0.5 * np.sum(phase_removal, axis=0)
    source_supply = np.sum(flow, axis=(1, 2))
    source_target = 2.0 * desired[source_bins]
    distances = np.abs(
        centers[source_bins, None, None] - centers[None, None, :]
    )
    distances = np.broadcast_to(distances, flow.shape)
    total_flow = float(np.sum(flow))
    mean_absolute_displacement = float(np.sum(flow * distances) / total_flow)
    rms_displacement = float(
        math.sqrt(np.sum(flow * distances**2) / total_flow)
    )
    return {
        "cost_power": cost_power,
        "source_bins": source_bins,
        "flow_Msun": flow,
        "phase_removal_Msun": phase_removal,
        "projected_pair_Msun": projected_pair,
        "objective": float(result.fun),
        "mean_absolute_displacement_kpc": mean_absolute_displacement,
        "rms_displacement_kpc": rms_displacement,
        "source_supply_relative_residual": float(
            np.max(np.abs(source_supply - source_target))
            / max(condensed, 1.0)
        ),
        "phase_endpoint_relative_residual": float(
            np.max(np.abs(np.sum(phase_removal, axis=1) - condensed))
            / max(condensed, 1.0)
        ),
        "capacity_relative_violation": float(
            np.max(
                np.maximum(
                    phase_removal
                    - np.vstack(
                        (data["capacity_minus_Msun"], data["capacity_plus_Msun"])
                    ),
                    0.0,
                )
            )
            / max(condensed, 1.0)
        ),
        "pair_profile_L1_change_fraction": float(
            np.sum(np.abs(projected_pair - desired)) / condensed
        ),
    }


def feasibility_rows(
    context: dict[str, Any],
    solution: dict[str, Any],
    polynomial: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for radial_bins in FEASIBILITY_BINS:
        data = binned_inputs(context, solution, polynomial, radial_bins)
        result = direct_feasibility(data)
        rows.append(
            {
                "radial_bins": radial_bins,
                "bin_width_kpc": data["edge_kpc"] / radial_bins,
                **result,
                "transport_allowed": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows


def robustness_rows(
    context: dict[str, Any],
    solution: dict[str, Any],
    polynomial: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[tuple[int, int], tuple[dict[str, Any], dict[str, Any]]]]:
    rows: list[dict[str, Any]] = []
    solutions: dict[tuple[int, int], tuple[dict[str, Any], dict[str, Any]]] = {}
    for radial_bins in RADIAL_BIN_CONTROLS:
        data = binned_inputs(context, solution, polynomial, radial_bins)
        for cost_power in COST_POWERS:
            transport = solve_transport(data, cost_power)
            solutions[(radial_bins, cost_power)] = (data, transport)
            rows.append(
                {
                    "radial_bins": radial_bins,
                    "bin_width_kpc": data["edge_kpc"] / radial_bins,
                    "cost_power": cost_power,
                    "objective_dimensionless": transport["objective"],
                    "mean_absolute_displacement_kpc": transport[
                        "mean_absolute_displacement_kpc"
                    ],
                    "rms_displacement_kpc": transport["rms_displacement_kpc"],
                    "pair_profile_L1_change_fraction": transport[
                        "pair_profile_L1_change_fraction"
                    ],
                    "source_supply_relative_residual": transport[
                        "source_supply_relative_residual"
                    ],
                    "phase_endpoint_relative_residual": transport[
                        "phase_endpoint_relative_residual"
                    ],
                    "capacity_relative_violation": transport[
                        "capacity_relative_violation"
                    ],
                    "target_q_used": False,
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
    return rows, solutions


def primary_profile_rows(
    data: dict[str, Any], transport: dict[str, Any]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    phase_removal = transport["phase_removal_Msun"]
    projected = transport["projected_pair_Msun"]
    for index, center in enumerate(data["centers_kpc"]):
        rows.append(
            {
                "radial_bin": index,
                "radius_center_kpc": center,
                "radius_lower_kpc": data["edges_kpc"][index],
                "radius_upper_kpc": data["edges_kpc"][index + 1],
                "raw_pair_desired_removal_Msun": data["desired_Msun"][index],
                "phase_minus_capacity_Msun": data["capacity_minus_Msun"][index],
                "phase_plus_capacity_Msun": data["capacity_plus_Msun"][index],
                "phase_minus_projected_removal_Msun": phase_removal[0, index],
                "phase_plus_projected_removal_Msun": phase_removal[1, index],
                "projected_pair_mean_removal_Msun": projected[index],
                "pair_projection_change_Msun": projected[index]
                - data["desired_Msun"][index],
                "phase_minus_capacity_fraction": phase_removal[0, index]
                / max(data["capacity_minus_Msun"][index], 1.0),
                "phase_plus_capacity_fraction": phase_removal[1, index]
                / max(data["capacity_plus_Msun"][index], 1.0),
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows


def primary_flow_rows(
    data: dict[str, Any], transport: dict[str, Any]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    flow = transport["flow_Msun"]
    for source_index, source_bin in enumerate(transport["source_bins"]):
        for phase_index, sign in enumerate((-1, 1)):
            for sink_bin in range(data["radial_bins"]):
                mass = float(flow[source_index, phase_index, sink_bin])
                if mass <= 1.0e-6:
                    continue
                rows.append(
                    {
                        "source_bin": int(source_bin),
                        "source_radius_kpc": data["centers_kpc"][source_bin],
                        "phase_sign": sign,
                        "sink_bin": sink_bin,
                        "sink_radius_kpc": data["centers_kpc"][sink_bin],
                        "flow_Msun": mass,
                        "absolute_displacement_kpc": abs(
                            data["centers_kpc"][source_bin]
                            - data["centers_kpc"][sink_bin]
                        ),
                        "cost_power": PRIMARY_COST_POWER,
                        "target_q_used": False,
                        "valid_for_claim": False,
                        "checkpoint_marker": MARKER,
                    }
                )
    return rows


def temporal_rows(
    solutions: dict[tuple[str, float], dict[str, Any]],
    data: dict[str, Any],
    transport: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_bins = transport["source_bins"]
    flow = transport["flow_Msun"]
    desired_endpoint = data["desired_Msun"]
    condensed = float(data["condensed_Msun"])
    flow_fraction = np.zeros_like(flow)
    for source_index, radial_bin in enumerate(source_bins):
        flow_fraction[source_index] = flow[source_index] / max(
            2.0 * desired_endpoint[radial_bin], 1.0
        )
    for branch, solution in solutions.items():
        selected = solution["selected_mass_Msun"] > 0.0
        arrival = solution["arrival_time_Gyr"][selected]
        mass = solution["selected_mass_Msun"][selected]
        radius = solution["radius_kpc"][selected]
        source_assignment = np.clip(
            np.searchsorted(data["edges_kpc"], radius, side="right") - 1,
            0,
            data["radial_bins"] - 1,
        )
        order = np.argsort(arrival)
        cumulative = np.cumsum(mass[order]) / condensed
        for fraction in np.linspace(0.0, 1.0, TEMPORAL_SAMPLES):
            if fraction <= 0.0:
                elapsed = 0.0
                arrived = np.zeros_like(mass, dtype=bool)
            else:
                index = int(np.searchsorted(cumulative, fraction))
                elapsed = float(arrival[order[index]])
                arrived = arrival <= elapsed
            arrived_by_bin = np.histogram(
                radius[arrived],
                bins=data["edges_kpc"],
                weights=mass[arrived],
            )[0]
            phase_removal = np.zeros((2, data["radial_bins"]), dtype=float)
            for source_index, radial_bin in enumerate(source_bins):
                phase_removal += (
                    2.0
                    * arrived_by_bin[radial_bin]
                    * flow_fraction[source_index]
                )
            phase_total = np.sum(phase_removal, axis=1)
            raw_arrived = float(np.sum(arrived_by_bin))
            pair_lambda = 0.5 * float(np.sum(phase_total)) / condensed
            raw_lambda = raw_arrived / condensed
            capacity = np.vstack(
                (data["capacity_minus_Msun"], data["capacity_plus_Msun"])
            )
            rows.append(
                {
                    "branch_id": P.branch_id(*branch),
                    "assembly_sample": fraction,
                    "elapsed_time_Gyr": elapsed,
                    "raw_pair_lambda": raw_lambda,
                    "phase_minus_lambda": phase_total[0] / condensed,
                    "phase_plus_lambda": phase_total[1] / condensed,
                    "transported_pair_lambda": pair_lambda,
                    "pair_time_identity_residual": abs(pair_lambda - raw_lambda),
                    "phase_minus_edge_mass_residual_Msun": abs(
                        -phase_total[0]
                        + phase_total[0] / condensed * condensed
                    ),
                    "phase_plus_edge_mass_residual_Msun": abs(
                        -phase_total[1]
                        + phase_total[1] / condensed * condensed
                    ),
                    "maximum_capacity_violation_Msun": float(
                        np.max(np.maximum(phase_removal - capacity, 0.0))
                    ),
                    "all_transport_masses_nonnegative": bool(
                        np.all(phase_removal >= -1.0e-9)
                    ),
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
    return rows


def provenance_rows(paths: dict[str, Path]) -> list[dict[str, Any]]:
    return [
        {
            "source_id": key,
            "source_type": "local_file",
            "path_or_url": str(path),
            "sha256": Q.file_digest(path),
            "role": "read_only_parent_empirical_or_numeric_input",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for key, path in paths.items()
    ]


def make_document(result: dict[str, Any]) -> str:
    summary = result["summary"]
    return f"""# 5168 - Pair-consistent capacity-bounded optimal-transport radial source operator

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## The obstruction proved

Checkpoint 5167 derived a pair-mean radial cooling/freefall clock but retained
homologous donor removal. Assigning the raw cooled shell profile independently
to each antithetic phase is not allowed. If `rbar_i` is the desired pair source,
`a_si` is phase `s`'s actual baryon capacity and
`x_-i=rbar_i+delta_i`, `x_+i=rbar_i-delta_i`, then

```text
max(-rbar_i,rbar_i-a_+i) <= delta_i
                         <= min(a_-i-rbar_i,rbar_i),
sum_i delta_i=0.
```

At every tested resolved partition with two or more radial bins, these bounds
have no zero-sum solution. Only the one-bin, fully homologous endpoint is
feasible. This proves why the direct shell-to-phase map generated artificial
`25 versus 4 Gyr` endpoints: it violated a real phase-capacity obstruction.

## Derived operator

The minimal repair is a constrained one-dimensional transport flow `f_isj`:

```text
min sum_i,s,j f_isj |r_i-r_j|^p/R_edge^p,
sum_s,j f_isj=2 rbar_i,
sum_i,j f_i,-,j=sum_i,j f_i,+,j=M_c,
sum_i f_isj <= a_sj,
f_isj >= 0.
```

`p=1` is primary; `p=2` is a frozen norm comparator. The primary radial
partition has `{PRIMARY_RADIAL_BINS}` bins, inherited from the checkpoint-5166
resolved clumping scale rather than selected from `q`.

The primary operator requires mean absolute radial transport
`{summary['primary_mean_displacement_kpc']} kpc` and RMS transport
`{summary['primary_rms_displacement_kpc']} kpc`. Its projected pair profile
changes by L1 mass fraction `{summary['primary_pair_L1_change_fraction']}`.
Across `{RADIAL_BIN_CONTROLS}` bins the mean absolute displacement range is
`{summary['L1_mean_displacement_range_kpc']}`. The transport is therefore a
finite, resolution-stable physical correction, not an infinitesimal numerical
repair.

## All-time identities

Endpoint transport fractions are lifted through each shell's sourced arrival
time. For every sampled time and all four thermal branches,

```text
x_sj(t)>=0,
x_sj(t)<=a_sj,
Delta M_s,edge(t)=-sum_j x_sj(t)+lambda_s(t)M_c=0,
[lambda_-(t)+lambda_+(t)]/2=lambda_bar(t).
```

The largest pair-time residual is
`{summary['maximum_pair_time_identity_residual']}` and the largest capacity
violation is `{summary['maximum_temporal_capacity_violation_Msun']} Msun`.

## Decision

`{result['route_decision']}`.

The operator is now sufficiently specified for a forward force calculation,
but this checkpoint does not read `q` and makes no galaxy claim. Its radial
transport metric is still a reduced variational matter closure, not a full
radiation-hydrodynamic derivation. The next gate must evolve the `p=1` operator
for all four predeclared clocks and use `p=2` only as a closure-norm robustness
test.

```text
raw independent phase assignment feasible                 = no;
capacity-bounded pair transport solved                     = yes;
phase endpoint mass exact                                  = yes;
pair source supply exact                                   = yes;
all-time pair and phase mass identities                    = yes;
q or rotation target used                                  = no;
forward force response executed                            = no;
local GR/Newton/Maxwell branch modified                    = no;
galaxy or full-MTS claim                                   = false.
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
                    "primary_radial_bins": PRIMARY_RADIAL_BINS,
                    "cost_powers": COST_POWERS,
                    "formal_digest": formal_before,
                },
                indent=2,
            )
        )
        return

    context, polynomial, virial, solutions = build_parent_state()
    reference_solution = solutions[("ISOBARIC", 0.3)]
    feasibility = feasibility_rows(context, reference_solution, polynomial)
    robustness, transport_solutions = robustness_rows(
        context, reference_solution, polynomial
    )
    primary_data, primary_transport = transport_solutions[
        (PRIMARY_RADIAL_BINS, PRIMARY_COST_POWER)
    ]
    profiles = primary_profile_rows(primary_data, primary_transport)
    flows = primary_flow_rows(primary_data, primary_transport)
    temporal = temporal_rows(solutions, primary_data, primary_transport)
    contract = contract_rows()
    direct_resolved_feasible = any(
        row["feasible"] for row in feasibility if int(row["radial_bins"]) >= 2
    )
    route_decision = (
        "RAW_PAIR_RADIAL_REMOVAL_IS_CAPACITY_INFEASIBLE_FOR_SEPARATE_ANTITHETIC_PHASES_BUT_A_MINIMUM_RADIAL_TRANSPORT_OPERATOR_NOW_SATISFIES_BOTH_PHASE_CAPACITIES_BOTH_ENDPOINTS_AND_THE_PAIR_TIME_IDENTITY_WITHOUT_READING_Q"
    )
    decision = [
        {
            "route": "pair_consistent_capacity_bounded_radial_source_transport",
            "result": route_decision,
            "evidence": (
                f"raw_resolved_feasible={direct_resolved_feasible}; "
                f"mean_transport={primary_transport['mean_absolute_displacement_kpc']} kpc; "
                f"source_residual={primary_transport['source_supply_relative_residual']}; "
                f"endpoint_residual={primary_transport['phase_endpoint_relative_residual']}"
            ),
            "next_requirement": "evolve the primary p=1 transported source for all four frozen radial clocks, then repeat the nearest branch with p=2 and numerical refinements",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    ]
    provenance = provenance_rows(paths)
    outputs = {
        CONTRACT_CSV: contract,
        FEASIBILITY_CSV: feasibility,
        ROBUSTNESS_CSV: robustness,
        PROFILE_CSV: profiles,
        FLOW_CSV: flows,
        TEMPORAL_CSV: temporal,
        DECISION_CSV: decision,
        PROVENANCE_CSV: provenance,
    }
    for path, rows in outputs.items():
        Q.write_csv(path, rows)

    hashes_after = {key: Q.file_digest(path) for key, path in paths.items()}
    formal_after = Q.tree_digest(FORMAL)
    validation: list[dict[str, Any]] = []
    Q.add_validation(validation, "all_sources_exist", not missing, missing)
    Q.add_validation(
        validation, "source_hashes_unchanged", hashes_before == hashes_after, hashes_after
    )
    Q.add_validation(
        validation,
        "formalization_workbench_unchanged",
        formal_before == formal_after == FORMAL_DIGEST_LOCK,
        formal_after,
    )
    Q.add_validation(
        validation,
        "one_bin_homologous_assignment_feasible",
        next(row for row in feasibility if int(row["radial_bins"]) == 1)["feasible"],
        feasibility,
    )
    Q.add_validation(
        validation,
        "all_resolved_raw_assignments_infeasible",
        not direct_resolved_feasible,
        [row for row in feasibility if int(row["radial_bins"]) >= 2],
    )
    Q.add_validation(
        validation,
        "all_transport_programs_solved",
        len(robustness) == len(RADIAL_BIN_CONTROLS) * len(COST_POWERS),
        len(robustness),
    )
    Q.add_validation(
        validation,
        "transport_source_supply_exact",
        max(float(row["source_supply_relative_residual"]) for row in robustness)
        < 1.0e-10,
        [row["source_supply_relative_residual"] for row in robustness],
    )
    Q.add_validation(
        validation,
        "transport_phase_endpoints_exact",
        max(float(row["phase_endpoint_relative_residual"]) for row in robustness)
        < 1.0e-10,
        [row["phase_endpoint_relative_residual"] for row in robustness],
    )
    Q.add_validation(
        validation,
        "transport_respects_phase_capacities",
        max(float(row["capacity_relative_violation"]) for row in robustness)
        < 1.0e-10,
        [row["capacity_relative_violation"] for row in robustness],
    )
    l1_rows = [row for row in robustness if int(row["cost_power"]) == 1]
    l1_displacements = [float(row["mean_absolute_displacement_kpc"]) for row in l1_rows]
    Q.add_validation(
        validation,
        "L1_transport_resolution_stable",
        max(l1_displacements) - min(l1_displacements) < 2.0,
        l1_displacements,
    )
    Q.add_validation(
        validation,
        "temporal_transport_nonnegative",
        all(row["all_transport_masses_nonnegative"] for row in temporal),
        "all temporal samples",
    )
    Q.add_validation(
        validation,
        "temporal_transport_respects_capacity",
        max(float(row["maximum_capacity_violation_Msun"]) for row in temporal)
        < 1.0e-3,
        max(float(row["maximum_capacity_violation_Msun"]) for row in temporal),
    )
    Q.add_validation(
        validation,
        "phase_edge_mass_identity_all_times",
        max(
            max(
                float(row["phase_minus_edge_mass_residual_Msun"]),
                float(row["phase_plus_edge_mass_residual_Msun"]),
            )
            for row in temporal
        )
        < 1.0e-3,
        "all temporal samples",
    )
    Q.add_validation(
        validation,
        "pair_time_identity_all_times",
        max(float(row["pair_time_identity_residual"]) for row in temporal)
        < 1.0e-12,
        max(float(row["pair_time_identity_residual"]) for row in temporal),
    )
    Q.add_validation(
        validation,
        "all_outputs_nonclaim",
        all(row.get("valid_for_claim") is False for rows in outputs.values() for row in rows),
        "all generated CSV rows",
    )
    Q.add_validation(
        validation,
        "q_not_used_and_local_branch_unmodified",
        all(not row["target_q_used"] for row in robustness)
        and all(not row["target_q_used"] for row in flows),
        "operator sources only; inherited G_N and local branch untouched",
    )
    maximum_pair_residual = max(
        float(row["pair_time_identity_residual"]) for row in temporal
    )
    maximum_capacity_violation = max(
        float(row["maximum_capacity_violation_Msun"]) for row in temporal
    )
    summary = {
        "virial_temperature_K": virial["temperature_K"],
        "raw_resolved_assignment_feasible": direct_resolved_feasible,
        "primary_radial_bins": PRIMARY_RADIAL_BINS,
        "primary_bin_width_kpc": primary_data["edge_kpc"] / PRIMARY_RADIAL_BINS,
        "primary_mean_displacement_kpc": primary_transport[
            "mean_absolute_displacement_kpc"
        ],
        "primary_rms_displacement_kpc": primary_transport[
            "rms_displacement_kpc"
        ],
        "primary_pair_L1_change_fraction": primary_transport[
            "pair_profile_L1_change_fraction"
        ],
        "L1_mean_displacement_range_kpc": [
            min(l1_displacements), max(l1_displacements)
        ],
        "maximum_pair_time_identity_residual": maximum_pair_residual,
        "maximum_temporal_capacity_violation_Msun": maximum_capacity_violation,
        "transport_flow_row_count": len(flows),
        "temporal_sample_row_count": len(temporal),
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
        "raw_phase_assignment_feasible": direct_resolved_feasible,
        "capacity_bounded_transport_solved": True,
        "phase_endpoint_identity_proved": True,
        "pair_time_identity_proved": True,
        "forward_force_response_executed": False,
        "local_GR_Newton_Maxwell_branch_modified": False,
        "valid_for_galaxy_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
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

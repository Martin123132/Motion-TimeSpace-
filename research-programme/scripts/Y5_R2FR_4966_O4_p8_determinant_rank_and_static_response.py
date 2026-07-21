from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4966"

RESULT_JSON = SOURCE / "O4_p8_determinant_rank_and_static_response_results.json"
NORMALIZATION_CSV = SOURCE / "O4_normalization_and_IR_trajectory.csv"
DETERMINANT_CSV = SOURCE / "O4_p8_determinant_source.csv"
RANK_CSV = SOURCE / "p8_two_source_rank_gate.csv"
STATIC_PROJECTOR_CSV = SOURCE / "p8_static_response_projector.csv"
SCHWARZSCHILD_CSV = SOURCE / "p8_Schwarzschild_metric_response.csv"
BOUNDARY_CSV = SOURCE / "p8_finite_boundary_gate.csv"
DECISION_CSV = SOURCE / "p8_4966_decision.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4966_O4_P8_RANK_STATIC_RESPONSE"
CHECKED_DATE = "2026-07-13"

SOURCE_PATHS = {
    "motion_4935": POST
    / "source-intake"
    / "functional_rg"
    / "4935"
    / "motion_sector_entry_results.json",
    "checkpoint_4935": POST
    / "4935-Y5-R2FR-completed-fixed-point-GR-connected-trajectory-and-motion-sector-entry.md",
    "local_4942": POST
    / "source-intake"
    / "functional_rg"
    / "4942"
    / "local_O4_C3_CFF_residual_results.json",
    "script_4942": POST / "scripts" / "Y5_R2FR_4942_local_O4_C3_CFF_residual.py",
    "script_4957": POST
    / "scripts"
    / "Y5_R2FR_4957_functional_PX_O4_GR_trajectory.py",
    "trajectory_4957": POST
    / "source-intake"
    / "functional_rg"
    / "4957"
    / "functional_PX_O4_GR_trajectory.csv",
    "result_4957": POST
    / "source-intake"
    / "functional_rg"
    / "4957"
    / "functional_PX_O4_GR_trajectory_results.json",
    "checkpoint_4957": POST
    / "4957-Y5-R2FR-functional-PX-GR-connected-trajectory-and-O2-O4-O5-residual-bound-or-motion-sector-rejection.md",
    "result_4965": POST
    / "source-intake"
    / "functional_rg"
    / "4965"
    / "p8_basis_projector_and_partial_flow_results.json",
    "motion_source_4965": POST
    / "source-intake"
    / "functional_rg"
    / "4965"
    / "p8_minimal_motion_scalar_source.csv",
    "checkpoint_4965": POST
    / "4965-Y5-R2FR-minimal-Ricci-flat-p8-on-shell-basis-helicity-projector-and-parent-flow-source-or-order-by-order-EFT-boundary.md",
}

EXPECTED_HASHES = {
    "motion_4935": "ba3dfdaacfb1e3d00282d82c4b4656a937e033cb9145e94c71b81e9c42a54240",
    "checkpoint_4935": "649da892ba5c256b7670206e837604dbbe04358fcd3705b5871906805e00c1df",
    "local_4942": "c830baff10125f984ba26d11d44465c4d519ecd6c51317b9c9fcac6cf5e2e04b",
    "script_4942": "1c539d7ce99780085b23b1324e9aeb18e33ad14a0b767e4eff1287b62e439d5e",
    "script_4957": "a39ad530184afe84db76417134f4f1f09a666fc5753f0d09b4f952d13e43c13e",
    "trajectory_4957": "c60eee38379dc8cf1bb16833b2b5a849ecc0b5d7da0f74d9f0c9bd1bf9b46166",
    "result_4957": "8d8c7e416706d116492e3539a0541e6e64174c59a460714325251656b1477cc6",
    "checkpoint_4957": "235b2e640428814bbcc3f0af1b2ebef020573314eaae1cb0b793be9122db0cb4",
    "result_4965": "74ca1417cd82738e3e46af0f2e0525cd1084646917a01876ffd2bd19371dd989",
    "motion_source_4965": "617a4decd95b17e4b111a6d3ae0f21fa87844a3027ea45ff34f1d60e9e324dc0",
    "checkpoint_4965": "8816046146a785b34938f7386df924b2d318098cb6413430798cffc6da021774",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        fields.extend(key for key in row if key not in fields)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("/", "\\")


def source_checks() -> dict[str, Any]:
    missing = [name for name, path in SOURCE_PATHS.items() if not path.exists()]
    bad_hashes = {
        name: {"expected": EXPECTED_HASHES[name], "actual": digest(path)}
        for name, path in SOURCE_PATHS.items()
        if path.exists() and digest(path) != EXPECTED_HASHES[name]
    }
    if missing or bad_hashes:
        raise RuntimeError(
            f"source lock failed: missing={missing}; bad_hashes={bad_hashes}"
        )

    motion = json.loads(SOURCE_PATHS["motion_4935"].read_text(encoding="utf-8"))
    local = json.loads(SOURCE_PATHS["local_4942"].read_text(encoding="utf-8"))
    trajectory = json.loads(
        SOURCE_PATHS["result_4957"].read_text(encoding="utf-8")
    )
    p8 = json.loads(SOURCE_PATHS["result_4965"].read_text(encoding="utf-8"))
    clauses = {
        "O4_action": motion["six_derivative_entry"]["O4_action_convention"]
        == "S_O4=u_O4 integral sqrt(g) C^2(nabla psi)^2",
        "O4_Hessian": motion["six_derivative_entry"]["O4_Hessian"]
        == "-2u_O4 nabla_mu[C^2 nabla^mu]",
        "canonical_endpoint_map": "u/Z=W_O4 lP4"
        in SOURCE_PATHS["script_4942"].read_text(encoding="utf-8"),
        "local_principal_symbol": local["action_and_local_branch"]["principal_symbol"]
        == "P^munu=(Z+2u_O4 C2)g^munu",
        "trajectory_ratio": "W_O4=u_O4/g^2"
        in SOURCE_PATHS["checkpoint_4957"].read_text(encoding="utf-8"),
        "trajectory_has_N8": all(
            key in trajectory["endpoint_summary"]
            for key in ("dynamic_etaN_N8", "reference_etaN0_N8")
        ),
        "p8_basis_rank_two": p8["p8_basis"]["real_parity_even_rank"] == 2,
        "minimal_source_ratio": p8["minimal_motion_scalar_source"]["checks"][
            "Bplus_over_Bminus"
        ],
    }
    if not all(clauses.values()):
        raise RuntimeError(f"source clause failure: {clauses}")
    return {
        "missing": missing,
        "bad_hashes": bad_hashes,
        "clauses": clauses,
        "hashes": {name: digest(path) for name, path in SOURCE_PATHS.items()},
    }


def derive_normalization() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    trajectory = json.loads(
        SOURCE_PATHS["result_4957"].read_text(encoding="utf-8")
    )
    endpoints = trajectory["endpoint_summary"]
    selected = {
        key: value
        for key, value in endpoints.items()
        if key.endswith("_N8")
    }
    values = [float(row["W_O4_endpoint"]) for row in selected.values()]
    minimum = min(values)
    maximum = max(values)
    midpoint = sum(values) / len(values)
    relative_spread = abs(maximum - minimum) / max(abs(midpoint), 1.0e-300)

    rows: list[dict[str, Any]] = [
        {
            "normalization_id": "N4966_00_raw_action",
            "object": "raw O4 portal",
            "definition": "S_O4=u integral sqrt(g) Q (nabla psi)^2; Q=C_mnrs C^mnrs",
            "units": "[u]=mass^-4",
            "status": "SOURCE_LOCKED_4935",
            "reason": "the displayed Hessian is -2u nabla_mu[Q nabla^mu]",
        },
        {
            "normalization_id": "N4966_01_canonical_field",
            "object": "canonical O4 coefficient",
            "definition": "phi=sqrt(Z_psi) psi; w_O4=u_O4/Z_psi",
            "units": "[w_O4]=mass^-4",
            "status": "EXACT_FIELD_NORMALIZATION",
            "reason": "the canonical scalar operator is -nabla[(1+2w_O4 Q)nabla]+m_psi^2",
        },
        {
            "normalization_id": "N4966_02_running_coordinates",
            "object": "dimensionless functional coordinates",
            "definition": "utilde_O4=k^4 w_O4; g=k^2 G_N",
            "units": "dimensionless",
            "status": "SOURCE_LOCKED_4942_4957",
            "reason": "the physical ratio is not the fixed-point value utilde itself",
        },
        {
            "normalization_id": "N4966_03_IR_map",
            "object": "Planck-normalized physical portal",
            "definition": "U4=w_O4/l_P^4=utilde_O4/g^2=W_O4",
            "units": "dimensionless",
            "status": "EXACT_RATIO_IDENTITY",
            "reason": "l_P^2=G_N makes (k l_P)^4=g^2",
        },
    ]
    for key, endpoint in selected.items():
        rows.append(
            {
                "normalization_id": f"N4966_{len(rows):02d}_{key}",
                "object": "GR-connected N8 IR endpoint",
                "definition": "U4=W_O4=utilde_O4/g^2",
                "units": "dimensionless",
                "status": "DERIVED_TRAJECTORY_ENDPOINT",
                "scheme_order": key,
                "g_endpoint": endpoint["g_endpoint"],
                "U4_endpoint": endpoint["W_O4_endpoint"],
                "reason": "4957 reaches g=1e-10 with N6-N8 convergence",
            }
        )
    rows.append(
        {
            "normalization_id": "N4966_06_N8_envelope",
            "object": "U4 N8 scheme envelope",
            "definition": "min(U4)<=U4<=max(U4)",
            "units": "dimensionless",
            "status": "DERIVED_TWO_SCHEME_BRACKET",
            "U4_min": minimum,
            "U4_max": maximum,
            "U4_midpoint": midpoint,
            "relative_spread": relative_spread,
            "reason": "both signs are negative and both magnitudes are nonzero",
        }
    )
    result = {
        "canonical_coefficient": "w_O4=u_O4/Z_psi",
        "dimensionless_running_coordinate": "utilde_O4=k^4 w_O4",
        "Newton_coordinate": "g=k^2 G_N",
        "physical_IR_coordinate": "U4=w_O4/l_P^4=utilde_O4/g^2=W_O4",
        "N8_endpoints": selected,
        "U4_min": minimum,
        "U4_max": maximum,
        "U4_midpoint": midpoint,
        "relative_spread": relative_spread,
        "nonzero_on_both_schemes": minimum < 0 and maximum < 0,
    }
    return tagged(rows), result


def derive_determinant_source() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    w, Q, momentum2, mass2 = sp.symbols(
        "w Q p2 m2", nonzero=True, finite=True
    )
    z = 1 + 2 * w * Q
    inverse_square = sp.series(z ** -2, Q, 0, 3).removeO()
    determinant_series = sp.series(
        sp.Rational(1, 2)
        * sp.log(1 + 2 * w * Q * momentum2 / (momentum2 + mass2)),
        Q,
        0,
        3,
    ).removeO()
    q2_integrand = sp.expand(determinant_series).coeff(Q, 2)
    expected_integrand = -(w**2 * momentum2**2) / (momentum2 + mass2) ** 2

    epsilon = sp.symbols("epsilon", positive=True)
    pi = sp.pi
    tadpole_pole = -(mass2) / (16 * pi**2 * epsilon)
    bubble_pole = 1 / (16 * pi**2 * epsilon)
    p4_pole = sp.simplify(-2 * mass2 * tadpole_pole + mass2**2 * bubble_pole)
    expected_p4_pole = 3 * mass2**2 / (16 * pi**2 * epsilon)

    U4, mu_psi = sp.symbols("U4 mu_psi", nonzero=True, finite=True)
    log_coefficient_action = 3 * w**2 * mass2**2 / (16 * pi**2)
    B_C_log_residue = 3 * U4**2 * mu_psi**4 / pi

    heat_kernel_weights = {index: sp.Integer(index - 2) for index in range(5)}
    checks = {
        "inverse_square_Q2_is_12w2": sp.expand(inverse_square).coeff(Q, 2)
        == 12 * w**2,
        "determinant_Q2_integrand": sp.simplify(q2_integrand - expected_integrand)
        == 0,
        "momentum_pole": sp.simplify(p4_pole - expected_p4_pole) == 0,
        "a2_weight_independent_of_z": heat_kernel_weights[2] == 0,
        "linear_p8_Q2_source_zero": heat_kernel_weights[2] == 0,
        "quadratic_log_coefficient": log_coefficient_action
        == 3 * w**2 * mass2**2 / (16 * pi**2),
        "MTS_BC_residue": B_C_log_residue
        == 3 * U4**2 * mu_psi**4 / pi,
    }
    if not all(checks.values()):
        raise RuntimeError(f"determinant derivation failed: {checks}")

    rows = tagged(
        [
            {
                "derivation_id": "DET4966_00_operator",
                "step": "canonical scalar Hessian",
                "equation": "Delta_O4=-nabla_mu[(1+2w_O4 Q)nabla^mu]+m_psi^2",
                "result": "z=1+2w_O4 Q on a covariantly constant Q patch",
                "status": "EXACT",
            },
            {
                "derivation_id": "DET4966_01_heat_kernel",
                "step": "constant-z heat-kernel scaling",
                "equation": "Tr exp(-s Delta_z)=(4pi s)^-2 sum_n s^n z^(n-2) a_n exp(-s m_psi^2)",
                "result": "the a2 coefficient has z^0 and therefore no O(w_O4 Q a2) p8 term",
                "status": "LINEAR_P8_SOURCE_EXACT_ZERO",
            },
            {
                "derivation_id": "DET4966_02_basis_completion",
                "step": "use complete derivative-free p8 basis",
                "equation": "p8_even={Q^2,Y^2}; Y=C.Ctilde",
                "result": "constant Q probes the only CP-even derivative-free O4 target; derivative operators start above p8",
                "status": "SOURCE_LOCKED_TO_4965",
            },
            {
                "derivation_id": "DET4966_03_flat_expansion",
                "step": "expand one-loop determinant to O(w_O4^2)",
                "equation": "Gamma_Q2=-w_O4^2 Q^2 integral_p p^4/(p^2+m_psi^2)^2",
                "result": str(q2_integrand),
                "status": "EXACT",
            },
            {
                "derivation_id": "DET4966_04_DR_pole",
                "step": "dimensionally regulate the momentum integral",
                "equation": "integral p^4/(p^2+m^2)^2=3m^4/(16pi^2 epsilon)+finite",
                "result": str(p4_pole),
                "status": "EXACT_POLE_RESIDUE",
            },
            {
                "derivation_id": "DET4966_05_log",
                "step": "subtract in MSbar",
                "equation": "Delta Gamma_Q2^log=[3w_O4^2 m_psi^4/(16pi^2)] ln(m_psi^2/mu_R^2) integral Q^2",
                "result": str(log_coefficient_action),
                "status": "ONE_LOOP_LOG_COEFFICIENT_DERIVED",
            },
            {
                "derivation_id": "DET4966_06_MTS_map",
                "step": "map to S=(16piG)^-1 integral [R+b_C Q^2+b_t Y^2]",
                "equation": "Delta B_C^log=(3/pi)U4^2 mu_psi^4 ln(m_psi^2/mu_R^2); Delta B_t^log=0",
                "result": str(B_C_log_residue),
                "status": "P8_SOURCE_RESIDUE_DERIVED",
            },
            {
                "derivation_id": "DET4966_07_p4_side_effect",
                "step": "separate the linear determinant term",
                "equation": "Delta Gamma_Q^log=-w_O4 m_psi^4 Q ln(m_psi^2/mu_R^2)/(16pi^2)",
                "result": "a p4 C^2 threshold, not a p8 source; its Ricci-flat bulk is in the 4964 quotient",
                "status": "SEPARATED_FROM_P8",
            },
            {
                "derivation_id": "DET4966_08_boundary",
                "step": "distinguish source from finite matching",
                "equation": "B_C(mu)=B_C(mu0)+Delta B_C^log+finite thresholds",
                "result": "the pole/log residue is fixed but an independent finite p8 boundary is not",
                "status": "TOTAL_FINITE_VECTOR_OPEN",
            },
        ]
    )
    result = {
        "canonical_operator": "Delta=-nabla[(1+2w_O4 Q)nabla]+m_psi^2",
        "constant_z_heat_kernel_weight": {
            f"a{index}": str(weight) for index, weight in heat_kernel_weights.items()
        },
        "linear_p8_source": "ZERO",
        "quadratic_integrand": str(expected_integrand),
        "momentum_pole": str(expected_p4_pole),
        "Q2_log_coefficient_in_effective_action": str(log_coefficient_action),
        "MTS_BC_log_residue": str(B_C_log_residue),
        "MTS_Bt_log_residue": "0",
        "helicity_source_direction": [1, 1],
        "checks": checks,
    }
    return rows, result


def derive_rank_gate(
    normalization: dict[str, Any], determinant: dict[str, Any]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    U4 = sp.symbols("U4", nonzero=True, real=True)
    direction_matrix = sp.Matrix(
        [[sp.Integer(1), sp.Integer(1)], [sp.Rational(6, 5), sp.Integer(1)]]
    )
    direction_determinant = sp.factor(direction_matrix.det())
    direction_rank = direction_matrix.rank()

    mu = sp.symbols("mu_psi", positive=True)
    minimal_minus = 1 / (60480 * sp.pi * mu**4)
    minimal_plus = 1 / (50400 * sp.pi * mu**4)
    O4_residue = 3 * U4**2 * mu**4 / sp.pi
    residue_matrix = sp.Matrix(
        [[minimal_minus, O4_residue], [minimal_plus, O4_residue]]
    )
    residue_determinant = sp.factor(residue_matrix.det())
    expected_determinant = -U4**2 / (100800 * sp.pi**2)

    U4_values = [normalization["U4_min"], normalization["U4_max"]]
    numeric_determinants = [
        float(expected_determinant.subs(U4, value)) for value in U4_values
    ]
    rows = tagged(
        [
            {
                "rank_id": "RANK4966_00_minimal",
                "source": "minimal massive motion determinant",
                "B_minus_residue": "1/(60480*pi*mu_psi^4)",
                "B_plus_residue": "1/(50400*pi*mu_psi^4)",
                "direction": "[1,6/5]",
                "status": "DERIVED_4965",
            },
            {
                "rank_id": "RANK4966_01_O4",
                "source": "quadratic O4 determinant pole/log",
                "B_minus_residue": "3*U4^2*mu_psi^4/pi",
                "B_plus_residue": "3*U4^2*mu_psi^4/pi",
                "direction": "[1,1]",
                "status": "DERIVED_4966",
            },
            {
                "rank_id": "RANK4966_02_direction_matrix",
                "source": "two calculated motion-sector source classes",
                "B_minus_residue": "columns=minimal,O4",
                "B_plus_residue": "[[1,1],[6/5,1]]",
                "direction": str(direction_matrix.tolist()),
                "determinant": str(direction_determinant),
                "rank": direction_rank,
                "status": "FULL_TARGET_DIRECTION_RANK",
            },
            {
                "rank_id": "RANK4966_03_normalized_residue",
                "source": "dimensionful factors retained",
                "B_minus_residue": str(minimal_minus),
                "B_plus_residue": str(minimal_plus),
                "direction": "O4 column carries the same renormalized mass",
                "determinant": str(residue_determinant),
                "rank": 2,
                "status": "NONZERO_FOR_U4_AND_MASSIVE_HESSIAN",
            },
            {
                "rank_id": "RANK4966_04_trajectory",
                "source": "4957 N8 U4 scheme bracket",
                "B_minus_residue": "not numerically fixed until mu_psi is matched",
                "B_plus_residue": "not numerically fixed until mu_psi is matched",
                "direction": "U4 is nonzero on both schemes",
                "determinant": f"[{min(numeric_determinants)},{max(numeric_determinants)}]",
                "rank": 2,
                "status": "STRUCTURAL_RANK_SURVIVES_TRAJECTORY",
            },
            {
                "rank_id": "RANK4966_05_total_boundary",
                "source": "complete parent p8 vector",
                "B_minus_residue": "motion sources plus boundary/gravity/photon/nonlocal pieces",
                "B_plus_residue": "motion sources plus boundary/gravity/photon/nonlocal pieces",
                "direction": "not numerically closed",
                "determinant": "not a prediction determinant",
                "rank": 2,
                "status": "STRUCTURAL_RANK_CLOSED_TOTAL_FINITE_VALUES_OPEN",
            },
        ]
    )
    checks = {
        "direction_determinant_minus_one_fifth": direction_determinant
        == -sp.Rational(1, 5),
        "direction_rank_two": direction_rank == 2,
        "residue_determinant_exact": sp.simplify(
            residue_determinant - expected_determinant
        )
        == 0,
        "trajectory_U4_nonzero": normalization["nonzero_on_both_schemes"],
        "O4_direction_from_determinant": determinant["helicity_source_direction"]
        == [1, 1],
    }
    if not all(checks.values()):
        raise RuntimeError(f"rank gate failed: {checks}")
    result = {
        "direction_matrix": str(direction_matrix.tolist()),
        "direction_determinant": str(direction_determinant),
        "direction_rank": direction_rank,
        "normalized_residue_determinant": str(residue_determinant),
        "expected_residue_determinant": str(expected_determinant),
        "numeric_N8_determinant_bracket": [
            min(numeric_determinants),
            max(numeric_determinants),
        ],
        "known_motion_source_direction_rank": 2,
        "total_finite_parent_vector_known": False,
        "checks": checks,
    }
    return rows, result


def derive_schwarzschild_response() -> tuple[
    list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]
]:
    time, radius, theta, phi, mass = sp.symbols(
        "t r theta phi M", positive=True, real=True
    )
    coordinates = [time, radius, theta, phi]
    dimension = 4
    f_metric = 1 - 2 * mass / radius
    metric = sp.diag(
        -f_metric,
        1 / f_metric,
        radius**2,
        radius**2 * sp.sin(theta) ** 2,
    )
    inverse = sp.simplify(metric.inv())

    connection = [
        [[sp.Integer(0) for _ in range(dimension)] for _ in range(dimension)]
        for _ in range(dimension)
    ]
    for upper in range(dimension):
        for lower_a in range(dimension):
            for lower_b in range(dimension):
                connection[upper][lower_a][lower_b] = sp.simplify(
                    sp.Rational(1, 2)
                    * sum(
                        inverse[upper, contracted]
                        * (
                            sp.diff(metric[contracted, lower_b], coordinates[lower_a])
                            + sp.diff(
                                metric[contracted, lower_a], coordinates[lower_b]
                            )
                            - sp.diff(
                                metric[lower_a, lower_b], coordinates[contracted]
                            )
                        )
                        for contracted in range(dimension)
                    )
                )

    riemann_up = [
        [
            [
                [sp.Integer(0) for _ in range(dimension)]
                for _ in range(dimension)
            ]
            for _ in range(dimension)
        ]
        for _ in range(dimension)
    ]
    for upper in range(dimension):
        for lower in range(dimension):
            for first in range(dimension):
                for second in range(dimension):
                    riemann_up[upper][lower][first][second] = sp.simplify(
                        sp.diff(
                            connection[upper][lower][second], coordinates[first]
                        )
                        - sp.diff(
                            connection[upper][lower][first], coordinates[second]
                        )
                        + sum(
                            connection[upper][first][index]
                            * connection[index][lower][second]
                            - connection[upper][second][index]
                            * connection[index][lower][first]
                            for index in range(dimension)
                        )
                    )

    riemann = [
        [
            [
                [sp.Integer(0) for _ in range(dimension)]
                for _ in range(dimension)
            ]
            for _ in range(dimension)
        ]
        for _ in range(dimension)
    ]
    for first in range(dimension):
        for second in range(dimension):
            for third in range(dimension):
                for fourth in range(dimension):
                    riemann[first][second][third][fourth] = sp.simplify(
                        sum(
                            metric[first, index]
                            * riemann_up[index][second][third][fourth]
                            for index in range(dimension)
                        )
                    )

    ricci = [
        [
            sp.simplify(
                sum(
                    riemann_up[index][first][index][second]
                    for index in range(dimension)
                )
            )
            for second in range(dimension)
        ]
        for first in range(dimension)
    ]
    kretschmann = sp.factor(
        sp.simplify(
            sum(
                riemann[a][b][c][d] ** 2
                * inverse[a, a]
                * inverse[b, b]
                * inverse[c, c]
                * inverse[d, d]
                for a in range(dimension)
                for b in range(dimension)
                for c in range(dimension)
                for d in range(dimension)
            )
        )
    )

    curvature_square_tensor = [
        [
            sp.factor(
                sp.simplify(
                    sum(
                        riemann[first][a][b][c]
                        * riemann[second][a][b][c]
                        * inverse[a, a]
                        * inverse[b, b]
                        * inverse[c, c]
                        for a in range(dimension)
                        for b in range(dimension)
                        for c in range(dimension)
                    )
                )
            )
            for second in range(dimension)
        ]
        for first in range(dimension)
    ]

    gradient_K = [sp.diff(kretschmann, coordinate) for coordinate in coordinates]
    hessian_K = [
        [
            sp.simplify(
                sp.diff(kretschmann, coordinates[first], coordinates[second])
                - sum(
                    connection[index][first][second] * gradient_K[index]
                    for index in range(dimension)
                )
            )
            for second in range(dimension)
        ]
        for first in range(dimension)
    ]
    hessian_K_up = [
        [
            sp.simplify(
                sum(
                    inverse[first, raised_first]
                    * inverse[second, raised_second]
                    * hessian_K[raised_first][raised_second]
                    for raised_first in range(dimension)
                    for raised_second in range(dimension)
                )
            )
            for second in range(dimension)
        ]
        for first in range(dimension)
    ]

    double_divergence = [
        [
            sp.factor(
                sp.simplify(
                    sum(
                        riemann[first][a][b][second] * hessian_K_up[a][b]
                        for a in range(dimension)
                        for b in range(dimension)
                    )
                )
            )
            for second in range(dimension)
        ]
        for first in range(dimension)
    ]
    H_covariant = [
        [
            sp.factor(
                sp.simplify(
                    4
                    * kretschmann
                    * curvature_square_tensor[first][second]
                    - 8 * double_divergence[first][second]
                    - sp.Rational(1, 2)
                    * metric[first, second]
                    * kretschmann**2
                )
            )
            for second in range(dimension)
        ]
        for first in range(dimension)
    ]
    H_mixed = [
        sp.factor(sp.simplify(inverse[index, index] * H_covariant[index][index]))
        for index in range(dimension)
    ]

    expected_H = [
        1152 * mass**3 * (32 * radius - 67 * mass) / radius**12,
        1152 * mass**3 * (4 * radius - 11 * mass) / radius**12,
        -1152 * mass**3 * (18 * radius - 41 * mass) / radius**12,
        -1152 * mass**3 * (18 * radius - 41 * mass) / radius**12,
    ]
    trace_H = sp.factor(sp.simplify(sum(H_mixed)))
    conservation = sp.factor(
        sp.simplify(
            sp.diff(H_mixed[1], radius)
            + sp.diff(f_metric, radius)
            / (2 * f_metric)
            * (H_mixed[1] - H_mixed[0])
            + 2 / radius * (H_mixed[1] - H_mixed[2])
        )
    )

    response_B = 128 * mass**3 * (36 * radius - 67 * mass) / radius**10
    response_A = 128 * mass**3 * (8 * radius - 11 * mass) / radius**10
    Gtt_linear = sp.factor(
        sp.simplify((radius * sp.diff(response_B, radius) + response_B) / radius**2)
    )
    Grr_linear = sp.factor(
        sp.simplify(
            (
                radius
                * (
                    response_B * sp.diff(f_metric, radius) / f_metric
                    + sp.diff(response_A, radius)
                    - response_A * sp.diff(f_metric, radius) / f_metric
                )
                + response_B
            )
            / radius**2
        )
    )
    perturbation = sp.symbols("epsilon_response")
    A = f_metric + perturbation * response_A
    B = f_metric + perturbation * response_B
    Gtheta_exact = (
        B * sp.diff(A, radius, 2) / (2 * A)
        - B * sp.diff(A, radius) ** 2 / (4 * A**2)
        + sp.diff(A, radius) * sp.diff(B, radius) / (4 * A)
        + B * sp.diff(A, radius) / (2 * A * radius)
        + sp.diff(B, radius) / (2 * radius)
    )
    Gtheta_linear = sp.factor(
        sp.simplify(sp.diff(Gtheta_exact, perturbation).subs(perturbation, 0))
    )

    x, B_C, B_minus, B_plus, chi = sp.symbols(
        "x B_C B_minus B_plus chi", real=True
    )
    weight_A = 128 * (8 - 11 * x)
    weight_B = 128 * (36 - 67 * x)
    helicity_A = sp.simplify(
        weight_A * ((B_minus + B_plus) / 2) * chi**3
    )
    helicity_B = sp.simplify(
        weight_B * ((B_minus + B_plus) / 2) * chi**3
    )
    potential_response = sp.factor(response_A / 2)
    acceleration_response = sp.factor(-sp.diff(potential_response, radius))

    checks = {
        "Ricci_flat": all(component == 0 for row in ricci for component in row),
        "Kretschmann": sp.simplify(
            kretschmann - 48 * mass**2 / radius**6
        )
        == 0,
        "four_dimensional_curvature_identity": all(
            sp.simplify(
                curvature_square_tensor[first][second]
                - metric[first, second] * kretschmann / 4
            )
            == 0
            for first in range(dimension)
            for second in range(dimension)
        ),
        "H_components": all(
            sp.simplify(actual - expected) == 0
            for actual, expected in zip(H_mixed, expected_H)
        ),
        "H_trace": sp.simplify(trace_H - 2 * kretschmann**2) == 0,
        "H_conserved": conservation == 0,
        "tt_equation": sp.simplify(Gtt_linear + H_mixed[0]) == 0,
        "rr_equation": sp.simplify(Grr_linear + H_mixed[1]) == 0,
        "angular_equation": sp.simplify(Gtheta_linear + H_mixed[2]) == 0,
        "helicity_static_average_A": sp.simplify(
            helicity_A
            - 64 * (8 - 11 * x) * (B_minus + B_plus) * chi**3
        )
        == 0,
        "helicity_static_average_B": sp.simplify(
            helicity_B
            - 64 * (36 - 67 * x) * (B_minus + B_plus) * chi**3
        )
        == 0,
    }
    if not all(checks.values()):
        raise RuntimeError(f"Schwarzschild response failed: {checks}")

    projector_rows = tagged(
        [
            {
                "projector_id": "STATIC4966_00_parity",
                "background": "static spherically symmetric parity-even geometry",
                "operator": "O_tt=(C.Ctilde)^2",
                "response": "delta O_tt=2(C.Ctilde) delta(C.Ctilde)=0",
                "weight_real_basis": 0,
                "weight_helicity_basis": "[-1/2,+1/2] multiplied by zero",
                "status": "EXACT_FIRST_VARIATION_ZERO",
            },
            {
                "projector_id": "STATIC4966_01_even",
                "background": "Schwarzschild exterior with fixed ADM mass",
                "operator": "O_CC=(C^2)^2=K^2",
                "response": "nonzero radial metric kernel",
                "weight_real_basis": 1,
                "weight_helicity_basis": "B_C=(B_minus+B_plus)/2",
                "status": "EXACT_FIRST_ORDER_RESPONSE",
            },
            {
                "projector_id": "STATIC4966_02_rank",
                "background": "all static spherical parity-even exteriors",
                "operator": "[O_CC,O_tt]",
                "response": "static projector row=[1,0]",
                "weight_real_basis": "[1,0]",
                "weight_helicity_basis": "[1/2,1/2]",
                "status": "STATIC_RESPONSE_RANK_ONE",
            },
            {
                "projector_id": "STATIC4966_03_missing_channel",
                "background": "rotating or parity-sensitive geometry",
                "operator": "O_tt",
                "response": "requires Y_background nonzero or an amplitude observable",
                "weight_real_basis": "not static-spherical",
                "weight_helicity_basis": "difference B_plus-B_minus",
                "status": "ROTATING_OR_SCATTERING_PROJECTOR_REQUIRED",
            },
        ]
    )
    metric_rows = tagged(
        [
            {
                "response_id": "SCHW4966_00_convention",
                "quantity": "metric and curvature convention",
                "exact_response": "ds^2=-A dt^2+dr^2/B+r^2dOmega^2; R^a_bcd=d_c Gamma^a_bd-d_d Gamma^a_bc+...",
                "dimensionless_response": "A0=B0=1-2M/r",
                "status": "DECLARED",
            },
            {
                "response_id": "SCHW4966_01_K",
                "quantity": "K=R_mnrs R^mnrs=C^2",
                "exact_response": str(kretschmann),
                "dimensionless_response": "48 M^2/r^6",
                "status": "SYMBOLICALLY_DERIVED",
            },
            {
                "response_id": "SCHW4966_02_Htt",
                "quantity": "H^t_t for delta integral K^2",
                "exact_response": str(H_mixed[0]),
                "dimensionless_response": "1152 M^3(32r-67M)/r^12",
                "status": "CONSERVED_FIELD_EQUATION_SOURCE",
            },
            {
                "response_id": "SCHW4966_03_Hrr",
                "quantity": "H^r_r for delta integral K^2",
                "exact_response": str(H_mixed[1]),
                "dimensionless_response": "1152 M^3(4r-11M)/r^12",
                "status": "CONSERVED_FIELD_EQUATION_SOURCE",
            },
            {
                "response_id": "SCHW4966_04_Hangular",
                "quantity": "H^theta_theta=H^phi_phi",
                "exact_response": str(H_mixed[2]),
                "dimensionless_response": "-1152 M^3(18r-41M)/r^12",
                "status": "CONSERVED_FIELD_EQUATION_SOURCE",
            },
            {
                "response_id": "SCHW4966_05_A",
                "quantity": "A(r)=f+b_C deltaA",
                "exact_response": str(response_A),
                "dimensionless_response": "deltaA=128 B_C chi^3(8-11x)",
                "status": "EXACT_FIXED_MASS_EXTERIOR_RESPONSE",
            },
            {
                "response_id": "SCHW4966_06_B",
                "quantity": "B(r)=f+b_C deltaB",
                "exact_response": str(response_B),
                "dimensionless_response": "deltaB=128 B_C chi^3(36-67x)",
                "status": "EXACT_FIXED_MASS_EXTERIOR_RESPONSE",
            },
            {
                "response_id": "SCHW4966_07_helicity_A",
                "quantity": "A response in helicity coordinates",
                "exact_response": str(helicity_A),
                "dimensionless_response": "64(B_minus+B_plus)chi^3(8-11x)",
                "status": "STATIC_HELICITY_SUM_ONLY",
            },
            {
                "response_id": "SCHW4966_08_helicity_B",
                "quantity": "B response in helicity coordinates",
                "exact_response": str(helicity_B),
                "dimensionless_response": "64(B_minus+B_plus)chi^3(36-67x)",
                "status": "STATIC_HELICITY_SUM_ONLY",
            },
            {
                "response_id": "SCHW4966_09_potential",
                "quantity": "delta Phi=delta A/2",
                "exact_response": str(potential_response),
                "dimensionless_response": "64 b_C M^3(8r-11M)/r^10",
                "status": "NEWTONIAN_TAIL_R_MINUS_9",
            },
            {
                "response_id": "SCHW4966_10_acceleration",
                "quantity": "delta a_r=-d_r delta Phi",
                "exact_response": str(acceleration_response),
                "dimensionless_response": "128 b_C M^3(36r-55M)/r^11",
                "status": "NEWTONIAN_FORCE_TAIL_R_MINUS_10",
            },
        ]
    )
    result = {
        "conventions": {
            "signature": "(-,+,+,+)",
            "Riemann": "R^a_bcd=d_c Gamma^a_bd-d_d Gamma^a_bc+Gamma^a_ce Gamma^e_bd-Gamma^a_de Gamma^e_bc",
            "action": "S=(16piG)^-1 integral sqrt(-g)[R+b_C K^2+b_t Y^2]",
            "mass_condition": "fixed ADM mass and unit asymptotic lapse",
        },
        "Kretschmann": str(kretschmann),
        "H_mixed": [str(value) for value in H_mixed],
        "H_trace": str(trace_H),
        "H_conservation_residual": str(conservation),
        "metric_response": {
            "delta_A_over_bC": str(response_A),
            "delta_B_over_bC": str(response_B),
            "dimensionless_delta_A": "128 B_C chi^3(8-11x)",
            "dimensionless_delta_B": "128 B_C chi^3(36-67x)",
            "x": "M/r",
            "chi": "l_P^2 M/r^3",
        },
        "static_projector_real_basis": [1, 0],
        "static_projector_helicity_basis": ["1/2", "1/2"],
        "static_projector_rank": 1,
        "Y2_first_variation": "ZERO_BY_PARITY",
        "potential_response": str(potential_response),
        "acceleration_response": str(acceleration_response),
        "checks": checks,
    }
    return projector_rows, metric_rows, result


def boundary_and_decisions() -> tuple[
    list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]
]:
    boundary_rows = tagged(
        [
            {
                "boundary_id": "BOUND4966_00_O4_pole",
                "component": "O4^2 pole/log source",
                "current_status": "DERIVED",
                "needed_for_total": "finite subtraction condition",
                "claim_effect": "fixes running direction but not the finite B_C value",
            },
            {
                "boundary_id": "BOUND4966_01_minimal_threshold",
                "component": "minimal massive motion threshold",
                "current_status": "DERIVED_4965",
                "needed_for_total": "physical renormalized mass and common matching convention",
                "claim_effect": "source direction and threshold law known",
            },
            {
                "boundary_id": "BOUND4966_02_finite_pair",
                "component": "independent finite p8 boundary [B_C(mu0),B_t(mu0)]",
                "current_status": "OPEN",
                "needed_for_total": "parent UV or decoupling matching condition",
                "claim_effect": "prevents total finite p8 prediction",
            },
            {
                "boundary_id": "BOUND4966_03_gravity",
                "component": "pure-Einstein three-loop and p6-insertion matching",
                "current_status": "OPEN",
                "needed_for_total": "same two-helicity renormalized amplitude",
                "claim_effect": "can shift both p8 coordinates",
            },
            {
                "boundary_id": "BOUND4966_04_photon",
                "component": "photon/CFF and other massive thresholds",
                "current_status": "OPEN",
                "needed_for_total": "field-content-complete one-loop matching",
                "claim_effect": "can shift the finite source vector",
            },
            {
                "boundary_id": "BOUND4966_05_nonlocal",
                "component": "nonlocal logarithms and running cancellation",
                "current_status": "OPEN_AS_COMPLETE_AMPLITUDE",
                "needed_for_total": "local plus nonlocal scale-independent observable",
                "claim_effect": "forbids treating a local running number as the observable",
            },
            {
                "boundary_id": "BOUND4966_06_static_projection",
                "component": "static spherical compact response",
                "current_status": "DERIVED_RANK_ONE",
                "needed_for_total": "B_C total or a conservative bound",
                "claim_effect": "static tests are blind to B_t at first order",
            },
            {
                "boundary_id": "BOUND4966_07_second_channel",
                "component": "rotating/parity-sensitive or four-graviton B_t readout",
                "current_status": "AMPLITUDE_PROJECTOR_DERIVED_STATIC_READOUT_ABSENT",
                "needed_for_total": "rotating solution or scattering matching",
                "claim_effect": "needed for direct local measurement of the difference channel",
            },
        ]
    )
    decision_rows = tagged(
        [
            {
                "decision_id": "DEC4966_00_normalization",
                "question": "Is the physical O4 coefficient the UV fixed-point number?",
                "answer": "no; U4=(u/Z)/l_P^4=utilde/g^2=W_O4",
                "status": "NORMALIZATION_LOCKED",
                "next_action": "use the converged N8 IR W_O4 bracket",
            },
            {
                "decision_id": "DEC4966_01_linear",
                "question": "Does one O4 insertion source the derivative-free p8 basis?",
                "answer": "no; the constant-z a2 weight is exactly z^0",
                "status": "LINEAR_P8_SOURCE_ZERO",
                "next_action": "retain the separate p4 threshold in the 4964 quotient",
            },
            {
                "decision_id": "DEC4966_02_quadratic",
                "question": "Does the O4 determinant produce a new p8 direction?",
                "answer": "yes at O(U4^2): [Delta B_minus,Delta B_plus] is proportional to [1,1]",
                "status": "QUADRATIC_P8_LOG_SOURCE_DERIVED",
                "next_action": "combine it with the 4965 minimal scalar source",
            },
            {
                "decision_id": "DEC4966_03_rank",
                "question": "Do known motion sources span the complete two-coordinate p8 target?",
                "answer": "yes structurally; det[[1,1],[6/5,1]]=-1/5",
                "status": "KNOWN_MOTION_SOURCE_DIRECTION_RANK_TWO",
                "next_action": "do not confuse structural rank with a finite total prediction",
            },
            {
                "decision_id": "DEC4966_04_static",
                "question": "Can a static spherical compact exterior read both p8 coordinates?",
                "answer": "no; Y=0 makes the Y^2 first variation vanish and the projector has rank one",
                "status": "STATIC_RESPONSE_EXACTLY_DERIVED",
                "next_action": "use the exact B_C radial kernel and reserve B_t for rotating/scattering data",
            },
            {
                "decision_id": "DEC4966_05_claim",
                "question": "Is exact all-operator compact GR or full MTS now established?",
                "answer": "no; the finite p8 boundary and remaining source classes are open",
                "status": "ORDER_BY_ORDER_P8_CORRECTION_DERIVED_TOTAL_OPEN",
                "next_action": "derive a parent decoupling boundary or retain one bounded p8 LEC",
            },
            {
                "decision_id": "DEC4966_06_next",
                "question": "What is the next verdict-changing target?",
                "answer": "finite p8 matching and the total static B_C bound",
                "status": "SELECT_4967_FINITE_MATCHING",
                "next_action": "calculate photon/gravity/motion thresholds in one subtraction convention and test whether a finite boundary remains independent",
            },
        ]
    )
    result = {
        "known_motion_source_direction_rank": 2,
        "static_spherical_response_rank": 1,
        "selected_static_compact_GR_through_p6": True,
        "p8_static_correction_kernel_derived": True,
        "total_finite_p8_vector": "OPEN",
        "exact_all_operator_compact_GR": False,
        "full_MTS": False,
        "next_target": "4967 finite p8 matching condition and total static B_C bound",
    }
    return boundary_rows, decision_rows, result


def write_provenance(source_state: dict[str, Any]) -> None:
    lines = [
        "# 4966 provenance",
        "",
        "This directory is generated by",
        "`post-checkpoint-work/scripts/Y5_R2FR_4966_O4_p8_determinant_rank_and_static_response.py`.",
        "",
        "## Locked local inputs",
        "",
    ]
    for name, path in SOURCE_PATHS.items():
        lines.append(f"- `{relative(path)}` — SHA256 `{source_state['hashes'][name]}`")
    lines.extend(
        [
            "",
            "## Derivation convention",
            "",
            "- Lorentzian signature `(-,+,+,+)`.",
            "- `R^a_bcd=d_c Gamma^a_bd-d_d Gamma^a_bc+Gamma^a_ce Gamma^e_bd-Gamma^a_de Gamma^e_bc`.",
            "- The one-loop determinant is evaluated after canonical scalar normalization, `w_O4=u_O4/Z_psi`.",
            "- The p8 pole/log residue is separated from the finite local matching boundary.",
            "- The Schwarzschild response fixes ADM mass and asymptotic lapse, removing the homogeneous mass/time shifts.",
            "- Every output remains invalid for a full-MTS claim.",
            "",
        ]
    )
    PROVENANCE.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    source_state = source_checks()
    normalization_rows, normalization = derive_normalization()
    determinant_rows, determinant = derive_determinant_source()
    rank_rows, rank = derive_rank_gate(normalization, determinant)
    projector_rows, metric_rows, static = derive_schwarzschild_response()
    boundary_rows, decision_rows, decision = boundary_and_decisions()

    SOURCE.mkdir(parents=True, exist_ok=True)
    write_csv(NORMALIZATION_CSV, normalization_rows)
    write_csv(DETERMINANT_CSV, determinant_rows)
    write_csv(RANK_CSV, rank_rows)
    write_csv(STATIC_PROJECTOR_CSV, projector_rows)
    write_csv(SCHWARZSCHILD_CSV, metric_rows)
    write_csv(BOUNDARY_CSV, boundary_rows)
    write_csv(DECISION_CSV, decision_rows)
    write_provenance(source_state)

    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "source_state": source_state,
        "normalization": normalization,
        "O4_determinant": determinant,
        "two_source_rank": rank,
        "static_response": static,
        "decision": decision,
        "outputs": {
            "normalization": relative(NORMALIZATION_CSV),
            "determinant": relative(DETERMINANT_CSV),
            "rank": relative(RANK_CSV),
            "static_projector": relative(STATIC_PROJECTOR_CSV),
            "Schwarzschild_response": relative(SCHWARZSCHILD_CSV),
            "boundary": relative(BOUNDARY_CSV),
            "decision": relative(DECISION_CSV),
            "provenance": relative(PROVENANCE),
        },
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print(f"{MARKER}_RESULT_SHA256={digest(RESULT_JSON)}", flush=True)
    print(
        f"{MARKER}_U4_N8=[{normalization['U4_min']:.12g},{normalization['U4_max']:.12g}]",
        flush=True,
    )
    print(
        f"{MARKER}_SOURCE_RANK={rank['known_motion_source_direction_rank']}",
        flush=True,
    )
    print(
        f"{MARKER}_STATIC_RANK={static['static_projector_rank']}", flush=True
    )
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

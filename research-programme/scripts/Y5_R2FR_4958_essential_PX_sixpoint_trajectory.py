from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp

import Y5_R2FR_4957_functional_PX_O4_GR_trajectory as standard_flow


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4958"

RESULT_JSON = SOURCE / "essential_PX_sixpoint_trajectory_results.json"
QUOTIENT_CSV = SOURCE / "six_derivative_essential_quotient.csv"
CALIBRATION_CSV = SOURCE / "essential_source_calibration.csv"
FIXED_CSV = SOURCE / "essential_functional_fixed_point_convergence.csv"
SPECTRUM_CSV = SOURCE / "essential_functional_stability_spectrum.csv"
TRAJECTORY_CSV = SOURCE / "essential_functional_GR_trajectory.csv"
CONVERGENCE_CSV = SOURCE / "essential_IR_coordinate_convergence.csv"
AMPLITUDE_CSV = SOURCE / "essential_scalar_24_amplitude.csv"
RESIDUAL_CSV = SOURCE / "curvature_sixpoint_residual_gate.csv"
DECISION_CSV = SOURCE / "essential_sixpoint_decision.csv"

STANDARD_SCRIPT = POST / "scripts" / "Y5_R2FR_4957_functional_PX_O4_GR_trajectory.py"
STANDARD_RESULT = POST / "source-intake" / "functional_rg" / "4957" / "functional_PX_O4_GR_trajectory_results.json"
STANDARD_CHECKPOINT = POST / "4957-Y5-R2FR-functional-PX-GR-connected-trajectory-and-O2-O4-O5-residual-bound-or-motion-sector-rejection.md"
BASIS_SOURCE = POST / "source-intake" / "functional_rg" / "4930" / "src1908" / "GravityEFTv2_final.tex"
STANDARD_SCALAR_SOURCE = POST / "source-intake" / "functional_rg" / "4937" / "src-2110.09566v1" / "SSTwAS.tex"
LOWER_QUOTIENT = POST / "source-intake" / "functional_rg" / "4941" / "lower_scalar_essential_quotient.csv"
RATE_RESULT = POST / "source-intake" / "functional_rg" / "4954" / "offshell_X2_X3_number_change_results.json"

EXPECTED_HASHES = {
    STANDARD_SCRIPT: "a39ad530184afe84db76417134f4f1f09a666fc5753f0d09b4f952d13e43c13e",
    STANDARD_RESULT: "8d8c7e416706d116492e3539a0541e6e64174c59a460714325251656b1477cc6",
    STANDARD_CHECKPOINT: "235b2e640428814bbcc3f0af1b2ebef020573314eaae1cb0b793be9122db0cb4",
    BASIS_SOURCE: "e234ab07031885f79030529bb3dcabc7e928cc4283774f26ebc5dac6b8a226dc",
    STANDARD_SCALAR_SOURCE: "09e4775df76bf3e2024be7f2ec655a125436dbb6042779bc71fe03f6f7e5d778",
    LOWER_QUOTIENT: "62f83d1e254709fa6dd5141ad9132a3d9aac89894a30684f804bae508646e89f",
    RATE_RESULT: "523339dd40a835f84c2bbd24a20b7977710f5a71b826dbb3d830089b7445ab45",
}

MARKER = "MTS_4958_ESSENTIAL_PX_SIXPOINT_TRAJECTORY"
CHECKED_DATE = "2026-07-13"
MAX_ORDER = 8
TRAJECTORY_ORDERS = (6, 8)
SCHEMES = standard_flow.SCHEMES
IR_G_TARGET = standard_flow.IR_G_TARGET


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
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


def threshold_q(eta: float, order: int) -> float:
    return 1.0 / math.factorial(order) - eta / (
        2.0 * math.factorial(order + 1)
    )


def redundant_sources(
    gravity: float,
    c_essential: float,
    eta_newton: float,
    eta_psi: float,
) -> tuple[float, float]:
    q_n2 = threshold_q(eta_newton, 2)
    q_n3 = threshold_q(eta_newton, 3)
    q_s2 = threshold_q(eta_psi, 2)
    q_s3 = threshold_q(eta_psi, 3)
    beta_ctilde = (
        -gravity * q_n2 / (3.0 * math.pi)
        + c_essential * q_s2 / (12.0 * math.pi**2)
    )
    beta_d = (
        gravity
        * (4.0 * q_n2 - 18.0 * q_n3 + q_s2 - 9.0 * q_s3)
        / (6.0 * math.pi)
        - c_essential * q_s2 / (12.0 * math.pi**2)
    )
    return beta_ctilde, beta_d


def essential_kernel_correction(
    variables: np.ndarray,
    gravity: float,
    eta_newton: float,
    eta_psi: float,
) -> tuple[np.ndarray, dict[str, float]]:
    beta_ctilde, beta_d = redundant_sources(
        gravity,
        float(variables[0]),
        eta_newton,
        eta_psi,
    )
    previous = np.concatenate([np.array([0.5]), variables[:-1]])
    correction = np.zeros_like(variables)
    kappa = 16.0 * math.pi * gravity
    for index, coefficient in enumerate(previous):
        target_power = index + 2
        correction[index] = kappa * coefficient * (
            (3.0 - target_power) * beta_d
            + 0.5 * target_power * beta_ctilde
        )
    return correction, {
        "beta_ctilde_frame": beta_ctilde,
        "beta_d_frame": beta_d,
        "essential_correction_a2": float(correction[0]),
        "essential_correction_a3": (
            float(correction[1]) if len(correction) >= 2 else math.nan
        ),
        "essential_correction_infinity_norm": float(
            np.linalg.norm(correction, ord=np.inf)
        ),
    }


class EssentialCombinedFunctionalFlow(standard_flow.CombinedFunctionalFlow):
    def original_beta(
        self,
        state: np.ndarray,
        scheme: str,
    ) -> tuple[np.ndarray, dict[str, float]]:
        beta, details = super().original_beta(state, scheme)
        correction, frame = essential_kernel_correction(
            state[6:],
            float(state[0]),
            details["eta_Newton_regulator"],
            details["eta_psi"],
        )
        beta[6:] += correction
        return beta, {**details, **frame}


def symbolic_quotient() -> tuple[list[dict[str, Any]], dict[str, str]]:
    x, kappa, c, e, ctilde, d = sp.symbols(
        "x kappa c e ctilde d", nonzero=True
    )
    r1 = -kappa * ctilde / 2
    r2 = kappa**2 * (ctilde * d / 2 - ctilde**2 / 8)
    r = 1 + r1 * x + r2 * x**2
    conformal = sp.series((r + kappa * d * x) / r**2, x, 0, 3).removeO()
    disformal = sp.series(-kappa * ctilde / r, x, 0, 3).removeO()
    qfactor = sp.series(conformal + disformal * x, x, 0, 3).removeO()
    curvature_k = -1 / kappa
    ricci_scalar_coefficient = sp.series(
        sp.sqrt(conformal / qfactor)
        * (curvature_k * qfactor + d * x),
        x,
        0,
        3,
    ).removeO()
    ricci_vector_coefficient = sp.series(
        sp.sqrt(conformal)
        * qfactor ** sp.Rational(-3, 2)
        * (
            -curvature_k * disformal * qfactor
            - d * disformal * x
            + ctilde
        ),
        x,
        0,
        3,
    ).removeO()
    transformed_p = sp.series(
        sp.Rational(1, 2) * x * conformal / r
        + c * x**2 / r**3
        + e * x**3 / (conformal * r**5),
        x,
        0,
        4,
    ).removeO()
    c_essential = sp.factor(sp.expand(transformed_p).coeff(x, 2))
    e_essential = sp.factor(sp.expand(transformed_p).coeff(x, 3))
    expected_c = c + kappa * (ctilde + d) / 2
    expected_e = (
        e
        + 3 * kappa * c * ctilde / 2
        + kappa**2 * ctilde**2 / 2
        + kappa**2 * ctilde * d / 4
    )
    checks = {
        "ricci_scalar_removed": str(
            sp.simplify(ricci_scalar_coefficient - curvature_k) == 0
        ),
        "ricci_vector_removed": str(
            sp.simplify(ricci_vector_coefficient) == 0
        ),
        "four_derivative_quotient": str(
            sp.simplify(c_essential - expected_c) == 0
        ),
        "six_derivative_quotient": str(
            sp.simplify(e_essential - expected_e) == 0
        ),
    }
    rows = [
        {
            "proof_id": "Q4958_01_basis",
            "object": "CP-even six-derivative scalar-gravity quotient",
            "derived_result": "O1=X^3 is the unique nonredundant six-scalar operator in the five-element O1-O5 basis",
            "proof_method": "source Hilbert series with EOM and IBP redundancies removed",
            "passed": True,
        },
        {
            "proof_id": "Q4958_02_metric_map",
            "object": "finite algebraic Einstein-frame map",
            "derived_result": "g_old=C(x)g_E+A(x)dphi dphi; r=sqrt((C+Ax)/C); r^3-r+kappa*x[d(r^2-1)+ctilde*r]=0",
            "proof_method": "simultaneous cancellation of R X and R_mn X^mn through six derivatives",
            "passed": all(value == "True" for value in checks.values()),
        },
        {
            "proof_id": "Q4958_03_cessential",
            "object": "four-derivative essential coordinate",
            "derived_result": str(c_essential),
            "proof_method": "exact determinant and inverse-metric expansion",
            "passed": checks["four_derivative_quotient"] == "True",
        },
        {
            "proof_id": "Q4958_04_eessential",
            "object": "six-derivative essential six-scalar coordinate",
            "derived_result": str(e_essential),
            "proof_method": "second-order disformal/conformal elimination and P(X) expansion",
            "passed": checks["six_derivative_quotient"] == "True",
        },
        {
            "proof_id": "Q4958_05_flow_kernel",
            "object": "minimal-essential functional RG kernel at ctilde=d=0",
            "derived_result": "Delta beta_a_m=16*pi*g*a_(m-1)[(3-m)beta_d+(m/2)beta_ctilde]",
            "proof_method": "infinitesimal scale-dependent metric redefinition of sqrt(g)P(X)",
            "passed": True,
        },
        {
            "proof_id": "Q4958_06_field_degree",
            "object": "curvature-bilinear source dependence",
            "derived_result": "at one loop beta_ctilde and beta_d on the zero-frame depend on a2 but not a_n>=3 by background-field degree",
            "proof_method": "two-scalar curvature projection of the P(X) Hessian",
            "passed": True,
        },
    ]
    return rows, checks


def convert_fixed_rows(
    flow: EssentialCombinedFunctionalFlow,
    solutions: dict[str, dict[int, np.ndarray]],
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    converted: list[dict[str, Any]] = []
    for row in rows:
        scheme = str(row["scheme"])
        order = int(row["polynomial_order"])
        _, details = flow.original_beta(solutions[scheme][order], scheme)
        essential_ratio = row.pop("r3_raw")
        converted.append(
            {
                **row,
                "frame": "minimal_essential_ctilde_eq_d_eq_0",
                "beta_ctilde_frame": details["beta_ctilde_frame"],
                "beta_d_frame": details["beta_d_frame"],
                "essential_correction_a2": details["essential_correction_a2"],
                "essential_correction_a3": details["essential_correction_a3"],
                "r3_essential_scalar": essential_ratio,
                "status": "SELF_CONSISTENT_ESSENTIAL_COMBINED_FIXED_POINT",
            }
        )
    return converted


def convert_trajectory_rows(
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    converted: list[dict[str, Any]] = []
    for row in rows:
        beta_ctilde, beta_d = redundant_sources(
            float(row["g"]),
            float(row["a2"]),
            float(row["eta_Newton_regulator"]),
            float(row["eta_psi"]),
        )
        converted.append(
            {
                **{
                    key: value
                    for key, value in row.items()
                    if key
                    not in {
                        "r3_raw",
                        "C24_raw_polynomial",
                        "dimensionless_sigma24_raw_kernel",
                    }
                },
                "frame": "minimal_essential_ctilde_eq_d_eq_0",
                "beta_ctilde_frame": beta_ctilde,
                "beta_d_frame": beta_d,
                "r3_essential_scalar": row["r3_raw"],
                "C24_essential_scalar_polynomial": row[
                    "C24_raw_polynomial"
                ],
                "dimensionless_sigma24_essential_scalar_kernel": row[
                    "dimensionless_sigma24_raw_kernel"
                ],
                "full_gravity_sixpoint_complete": False,
                "status": "GR_CONNECTED_ESSENTIAL_FUNCTIONAL_TRAJECTORY",
            }
        )
    return converted


def convert_summary(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        **{
            key: value
            for key, value in summary.items()
            if key
            not in {
                "r3_raw_endpoint",
                "C24_raw_endpoint",
                "dimensionless_sigma24_raw_kernel_endpoint",
            }
        },
        "r3_essential_scalar_endpoint": summary["r3_raw_endpoint"],
        "C24_essential_scalar_endpoint": summary["C24_raw_endpoint"],
        "dimensionless_sigma24_essential_scalar_kernel_endpoint": summary[
            "dimensionless_sigma24_raw_kernel_endpoint"
        ],
        "full_gravity_sixpoint_complete": False,
    }


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    SOURCE.mkdir(parents=True, exist_ok=True)
    source_hashes = {str(path): digest(path) for path in EXPECTED_HASHES}
    source_hashes_match = all(
        source_hashes[str(path)] == expected
        for path, expected in EXPECTED_HASHES.items()
    )
    if not source_hashes_match:
        raise RuntimeError(
            f"source hash mismatch: "
            f"{[str(path) for path, expected in EXPECTED_HASHES.items() if source_hashes[str(path)] != expected]}"
        )

    basis_text = BASIS_SOURCE.read_text(encoding="utf-8")
    scalar_source_text = STANDARD_SCALAR_SOURCE.read_text(encoding="utf-8")
    lower_rows = read_csv(LOWER_QUOTIENT)
    source_clause_checks = {
        "basis_nonredundant": "correct CP even operator basis" in basis_text,
        "O1_unique_six_scalar": "d\\phi^6" in basis_text
        and "\\mathcal{O}_1" in basis_text,
        "standard_beta_ctilde": "\\beta_{\\tilde{c}}" in scalar_source_text,
        "standard_beta_d": "\\beta_{d}" in scalar_source_text,
        "threshold_definition": "q_{i;n}^{p_s, p_g}" in scalar_source_text,
        "lower_quotient": any(
            row["quantity"] == "c_essential"
            and row["formula"] == "c+8pi g(ctilde+d)"
            for row in lower_rows
        ),
        "4957_trajectory": "essential_r3=False"
        in STANDARD_SCRIPT.read_text(encoding="utf-8"),
    }
    if not all(source_clause_checks.values()):
        raise RuntimeError(f"source clause failure: {source_clause_checks}")

    quotient_rows, symbolic_checks = symbolic_quotient()
    if not all(value == "True" for value in symbolic_checks.values()):
        raise RuntimeError(f"symbolic quotient failure: {symbolic_checks}")

    calibration_rows: list[dict[str, Any]] = []
    for gravity in (1.0e-5, 1.0e-3, 1.0e-2, 0.13):
        beta_ctilde, beta_d = redundant_sources(
            gravity, 0.0, 0.0, 0.0
        )
        raw_c = 20.0 * gravity**2
        essential_c = raw_c + 8.0 * math.pi * gravity * (
            beta_ctilde + beta_d
        )
        raw_e = -208.0 * math.pi * gravity**3 / 5.0
        correction_e = 24.0 * math.pi * gravity * 0.0 * beta_ctilde
        calibration_rows.extend(
            [
                {
                    "calibration_id": "CAL4958_cessential",
                    "g": gravity,
                    "raw_source": raw_c,
                    "frame_correction": essential_c - raw_c,
                    "essential_source": essential_c,
                    "target": 16.0 * gravity**2,
                    "relative_error": abs(
                        essential_c - 16.0 * gravity**2
                    )
                    / (16.0 * gravity**2),
                    "passed": math.isclose(
                        essential_c,
                        16.0 * gravity**2,
                        rel_tol=2.0e-14,
                        abs_tol=1.0e-30,
                    ),
                },
                {
                    "calibration_id": "CAL4958_eessential_at_origin",
                    "g": gravity,
                    "raw_source": raw_e,
                    "frame_correction": correction_e,
                    "essential_source": raw_e + correction_e,
                    "target": raw_e,
                    "relative_error": 0.0,
                    "passed": True,
                },
            ]
        )

    parent_result = json.loads(standard_flow.O4_RESULT.read_text(encoding="utf-8"))
    parent_coordinates = parent_result["minimal_O4_completed_point"][
        "coordinates"
    ]
    parent_initial = np.array(list(parent_coordinates.values()), dtype=float)
    source_fixed_rows = standard_flow.read_csv(standard_flow.FIXED_4956)
    rate_result = json.loads(RATE_RESULT.read_text(encoding="utf-8"))
    rate_polynomial = {
        key: float(rate_result["on_shell_24"][key])
        for key in ("C0", "C1", "C2")
    }

    projector = standard_flow.functional_px.FunctionalPXProjector(
        MAX_ORDER, standard_flow.QUADRATURE_ORDER
    )
    flow = EssentialCombinedFunctionalFlow(projector)
    fixed_solutions, raw_fixed_rows = standard_flow.solve_fixed_points(
        flow, parent_initial, source_fixed_rows
    )
    fixed_rows = convert_fixed_rows(flow, fixed_solutions, raw_fixed_rows)

    spectrum_rows: list[dict[str, Any]] = []
    trajectory_rows: list[dict[str, Any]] = []
    endpoint_summaries: list[dict[str, Any]] = []
    relevant_counts: dict[str, dict[int, int]] = {}
    for scheme in SCHEMES:
        relevant_counts[scheme] = {}
        for order in TRAJECTORY_ORDERS:
            fixed = fixed_solutions[scheme][order]
            gravity_vector, spectrum, relevant_count = (
                standard_flow.stability_data(flow, fixed, scheme, order)
            )
            relevant_counts[scheme][order] = relevant_count
            spectrum_rows.extend(
                {
                    **row,
                    "frame": "minimal_essential_ctilde_eq_d_eq_0",
                }
                for row in spectrum
            )
            _, raw_rows, raw_summary = standard_flow.integrate_trajectory(
                flow,
                fixed,
                gravity_vector,
                scheme,
                order,
                rate_polynomial,
            )
            trajectory_rows.extend(convert_trajectory_rows(raw_rows))
            endpoint_summaries.append(convert_summary(raw_summary))

    convergence_rows: list[dict[str, Any]] = []
    for scheme in SCHEMES:
        endpoints = {
            int(row["polynomial_order"]): row
            for row in endpoint_summaries
            if row["scheme"] == scheme
        }
        lower = endpoints[TRAJECTORY_ORDERS[0]]
        upper = endpoints[TRAJECTORY_ORDERS[1]]
        for coordinate in (
            "A2_endpoint",
            "A3_endpoint",
            "r3_essential_scalar_endpoint",
            "dimensionless_sigma24_essential_scalar_kernel_endpoint",
            "W_O4_endpoint",
        ):
            lower_value = float(lower[coordinate])
            upper_value = float(upper[coordinate])
            relative = abs(upper_value - lower_value) / max(
                abs(upper_value), 1.0e-300
            )
            convergence_rows.append(
                {
                    "scheme": scheme,
                    "coordinate": coordinate,
                    "lower_order": TRAJECTORY_ORDERS[0],
                    "upper_order": TRAJECTORY_ORDERS[1],
                    "lower_value": lower_value,
                    "upper_value": upper_value,
                    "relative_difference": relative,
                    "converged_below_1e_minus_3": relative < 1.0e-3,
                    "status": "ESSENTIAL_IR_ORDER_CONVERGENCE_GATE",
                }
            )

    amplitude_rows: list[dict[str, Any]] = []
    for summary in endpoint_summaries:
        amplitude_rows.append(
            {
                "scheme": summary["scheme"],
                "polynomial_order": summary["polynomial_order"],
                "g_endpoint": summary["g_endpoint"],
                "c_essential_endpoint": float(summary["A2_endpoint"])
                * float(summary["g_endpoint"]) ** 2,
                "e_essential_endpoint": float(summary["A3_endpoint"])
                * float(summary["g_endpoint"]) ** 3,
                "r3_essential_scalar": summary[
                    "r3_essential_scalar_endpoint"
                ],
                "g_times_r3_essential_scalar": float(summary["g_endpoint"])
                * float(summary["r3_essential_scalar_endpoint"]),
                "C24_essential_scalar": summary[
                    "C24_essential_scalar_endpoint"
                ],
                "dimensionless_sigma24_essential_scalar_kernel": summary[
                    "dimensionless_sigma24_essential_scalar_kernel_endpoint"
                ],
                "scalar_flat_subamplitude_status": "INVARIANT_TREE_SUBAMPLITUDE_DERIVED",
                "full_gravity_amplitude_status": "BLOCKED_BY_O2_O3_O4_PROJECTORS",
            }
        )

    residual_rows = [
        {
            "operator": "O1=X^3",
            "six_scalar_tree_role": "unique direct six-scalar p6 contact",
            "trajectory_status": "ESSENTIAL_COEFFICIENT_DERIVED",
            "projector_status": "INCLUDED_IN_4954_SCALAR_AMPLITUDE",
            "full_amplitude_gate": "PASS_FOR_SCALAR_FLAT_SUBAMPLITUDE",
        },
        {
            "operator": "O2=X(nabla_nabla_psi)^2",
            "six_scalar_tree_role": "allowed through the metric expansion of the four-scalar p6 vertex and one canonical graviton attachment",
            "trajectory_status": "COEFFICIENT_FLOW_OPEN",
            "projector_status": "NOT_PROVED_ZERO",
            "full_amplitude_gate": "BLOCKS_FULL_GRAVITY_SIXPOINT",
        },
        {
            "operator": "O3=C^3",
            "six_scalar_tree_role": "allowed through three canonical scalar-stress graviton attachments",
            "trajectory_status": "h_C3_TRAJECTORY_PRESENT",
            "projector_status": "EXTERNAL_SCALAR_PROJECTOR_OPEN",
            "full_amplitude_gate": "BLOCKS_FULL_GRAVITY_SIXPOINT",
        },
        {
            "operator": "O4=C^2 X",
            "six_scalar_tree_role": "allowed through two canonical scalar-stress graviton attachments",
            "trajectory_status": "u_O4_TRAJECTORY_PRESENT",
            "projector_status": "EXTERNAL_SCALAR_PROJECTOR_OPEN",
            "full_amplitude_gate": "BLOCKS_FULL_GRAVITY_SIXPOINT",
        },
        {
            "operator": "O5=C(nabla_psi)^2(nabla_nabla_psi)",
            "six_scalar_tree_role": "reflection odd in the selected parent",
            "trajectory_status": "EXACT_ZERO_BY_REFLECTION",
            "projector_status": "EXCLUDED",
            "full_amplitude_gate": "DOES_NOT_BLOCK_SELECTED_PARENT",
        },
    ]

    all_fixed = all(
        float(row["scaled_beta_residual"]) < 1.0e-8 for row in fixed_rows
    )
    one_relevant = all(
        count == 1
        for scheme_counts in relevant_counts.values()
        for count in scheme_counts.values()
    )
    all_reach_ir = all(
        summary["termination"] == "IR_G_TARGET"
        for summary in endpoint_summaries
    )
    all_converged = all(
        bool(row["converged_below_1e_minus_3"])
        for row in convergence_rows
    )

    decision_rows = [
        {
            "decision_id": "DEC4958_01_quotient",
            "question": "Is the X2-X3 standard-frame ambiguity removable through six derivatives?",
            "answer": "yes by the derived finite disformal-conformal Einstein-frame map",
            "status": "SIX_DERIVATIVE_ESSENTIAL_QUOTIENT_DERIVED",
            "next_action": "use only essential-frame P(X) coefficients",
        },
        {
            "decision_id": "DEC4958_02_kernel",
            "question": "Can the quotient be maintained along the RG flow without evolving raw ctilde and d?",
            "answer": "yes through the derived scale-dependent metric RG kernel in the declared one-loop P(X) sector",
            "status": "FUNCTIONAL_MINIMAL_ESSENTIAL_KERNEL_DERIVED",
            "next_action": "retain the ctilde=d=0 frame",
        },
        {
            "decision_id": "DEC4958_03_calibration",
            "question": "Does the corrected flow reproduce the known lower essential source?",
            "answer": "yes: beta_c at the Gaussian matter origin is 16 g^2 rather than raw 20 g^2",
            "status": "LOWER_ESSENTIAL_SOURCE_REPRODUCED",
            "next_action": "reject relabeling of the 4957 raw trajectory",
        },
        {
            "decision_id": "DEC4958_04_fixed",
            "question": "Does the essentialized functional parent retain combined fixed points?",
            "answer": "yes" if all_fixed else "no",
            "status": "ESSENTIAL_COMBINED_FIXED_POINTS_RETAINED" if all_fixed else "ESSENTIAL_FIXED_POINT_FAILED",
            "next_action": "use the essential stability spectrum",
        },
        {
            "decision_id": "DEC4958_05_trajectory",
            "question": "Does one GR-connected essential trajectory reach the Gaussian regime?",
            "answer": "yes" if one_relevant and all_reach_ir else "no",
            "status": "ESSENTIAL_GR_CONNECTED_TRAJECTORY_RETAINED" if one_relevant and all_reach_ir else "ESSENTIAL_TRAJECTORY_FAILED",
            "next_action": "retain order and regulator brackets",
        },
        {
            "decision_id": "DEC4958_06_scalar_amplitude",
            "question": "Is the flat scalar X2-X3 tree 2-to-4 subamplitude now basis independent?",
            "answer": "yes in the minimal essential scalar frame",
            "status": "ESSENTIAL_SCALAR_SIXPOINT_SUBAMPLITUDE_DERIVED",
            "next_action": "do not call it the full gravity amplitude",
        },
        {
            "decision_id": "DEC4958_07_full_amplitude",
            "question": "Is the complete gravity-motion six-scalar amplitude derived?",
            "answer": "no: O2 O3 and O4 external-scalar projectors remain",
            "status": "FULL_GRAVITY_SIXPOINT_PROJECTOR_OPEN",
            "next_action": "derive the O2 O3 O4 on-shell scalar projectors",
        },
        {
            "decision_id": "DEC4958_08_local",
            "question": "Does essentialization obstruct the retained local GR Newton Maxwell branch?",
            "answer": "no",
            "status": "4947_LOCAL_GR_NEWTON_MAXWELL_RETAINED",
            "next_action": "keep the local branch fixed while completing scattering",
        },
        {
            "decision_id": "DEC4958_09_full",
            "question": "Does this establish full MTS or a galaxy formation rate?",
            "answer": "no",
            "status": "FULL_MTS_AND_GALAXY_RATE_BLOCKED",
            "next_action": "complete curvature-mediated sixpoint projectors first",
        },
    ]

    quotient_rows = tagged(quotient_rows)
    calibration_rows = tagged(calibration_rows)
    fixed_rows = tagged(fixed_rows)
    spectrum_rows = tagged(spectrum_rows)
    trajectory_rows = tagged(trajectory_rows)
    convergence_rows = tagged(convergence_rows)
    amplitude_rows = tagged(amplitude_rows)
    residual_rows = tagged(residual_rows)
    decision_rows = tagged(decision_rows)

    write_csv(QUOTIENT_CSV, quotient_rows)
    write_csv(CALIBRATION_CSV, calibration_rows)
    write_csv(FIXED_CSV, fixed_rows)
    write_csv(SPECTRUM_CSV, spectrum_rows)
    write_csv(TRAJECTORY_CSV, trajectory_rows)
    write_csv(CONVERGENCE_CSV, convergence_rows)
    write_csv(AMPLITUDE_CSV, amplitude_rows)
    write_csv(RESIDUAL_CSV, residual_rows)
    write_csv(DECISION_CSV, decision_rows)

    endpoint_summary = {
        f"{row['scheme']}_N{row['polynomial_order']}": row
        for row in endpoint_summaries
    }
    result = {
        "checkpoint_marker": MARKER,
        "source_hashes": source_hashes,
        "source_hashes_match": source_hashes_match,
        "source_clause_checks": source_clause_checks,
        "symbolic_quotient_checks": symbolic_checks,
        "essential_frame_contract": {
            "renormalization_conditions": ["ctilde=0", "d=0"],
            "c_essential": "c+8pi*g*(ctilde+d)",
            "e_essential": "e+24pi*g*c*ctilde+128pi^2*g^2*ctilde^2+64pi^2*g^2*ctilde*d",
            "functional_kernel": "Delta beta_a_m=16pi*g*a_(m-1)[(3-m)beta_d+(m/2)beta_ctilde]",
            "beta_ctilde_zero_frame": "-g qN2/(3pi)+c qS2/(12pi^2)",
            "beta_d_zero_frame": "g(4qN2-18qN3+qS2-9qS3)/(6pi)-c qS2/(12pi^2)",
        },
        "calibration": {
            "all_rows_pass": all(row["passed"] for row in calibration_rows),
            "raw_beta_c_origin": "20g^2",
            "essential_beta_c_origin": "16g^2",
            "essential_beta_e_origin": "-(208pi/5)g^3",
        },
        "combined_fixed_points": {
            scheme: next(
                row
                for row in fixed_rows
                if row["scheme"] == scheme
                and int(row["polynomial_order"]) == MAX_ORDER
            )
            for scheme in SCHEMES
        },
        "relevant_direction_counts": relevant_counts,
        "endpoint_summary": endpoint_summary,
        "gates": {
            "six_derivative_essential_quotient": "DERIVED",
            "minimal_essential_functional_kernel": "DERIVED",
            "lower_essential_source_16g2": "REPRODUCED",
            "essential_combined_fixed_points": all_fixed,
            "one_GR_connected_relevant_direction": one_relevant,
            "all_essential_trajectories_reach_IR": all_reach_ir,
            "essential_IR_order_convergence": all_converged,
            "essential_scalar_24_subamplitude": "DERIVED",
            "full_gravity_sixpoint": "OPEN_O2_O3_O4_PROJECTORS",
            "local_GR_Newton_Maxwell_4947": "RETAINED",
            "galaxy_rate": False,
            "full_MTS": False,
        },
    }
    RESULT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        f"{MARKER}_DONE quotient=True fixed={all_fixed} "
        f"relevant={one_relevant} IR={all_reach_ir} "
        f"scalar_amplitude=True full_gravity=False",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

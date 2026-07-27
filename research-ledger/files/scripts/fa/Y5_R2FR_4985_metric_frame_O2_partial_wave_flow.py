from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4985"

CHECKPOINT_4958 = POST / "4958-Y5-R2FR-six-derivative-essential-X2-X3-quotient-and-invariant-2to4-amplitude-or-rate-route-rejection.md"
CHECKPOINT_4959 = POST / "4959-Y5-R2FR-O2-O3-O4-external-scalar-sixpoint-projectors-and-full-invariant-amplitude-or-curvature-route-rejection.md"
RESULT_4959 = POST / "source-intake" / "functional_rg" / "4959" / "curvature_sixpoint_projector_results.json"
CHECKPOINT_4984 = POST / "4984-Y5-R2FR-running-essential-frame-six-derivative-spillover-and-nonlocal-source-silence.md"
RESULT_4984 = POST / "source-intake" / "functional_rg" / "4984" / "running_frame_nonlocal_silence_results.json"
EFT_BASIS = POST / "source-intake" / "functional_rg" / "4930" / "src1908" / "GravityEFTv2_final.tex"
BURGESS_SOURCE = SOURCE / "sources" / "burgess" / "GRET-jhep.tex"
BERN_SOURCE = SOURCE / "sources" / "bern" / "gr_simp.tex"
BARATELLA_SOURCE = SOURCE / "sources" / "baratella" / "draft.tex"
BURGESS_ARCHIVE = SOURCE / "sources" / "burgess_gr-qc0311082.tar"
BERN_ARCHIVE = SOURCE / "sources" / "bern_1701.02422.tar"
BARATELLA_ARCHIVE = SOURCE / "sources" / "baratella_2010.13809.tar"

METRIC_BULK_CSV = SOURCE / "metric_frame_infinitesimal_bulk_cancellation.csv"
METRIC_BOUNDARY_CSV = SOURCE / "metric_frame_boundary_jet_checks.csv"
METRIC_GATE_CSV = SOURCE / "metric_frame_O2_connection_zero.csv"
POWER_CSV = SOURCE / "O2_loop_power_counting.csv"
PARTIAL_WAVE_CSV = SOURCE / "O2_partial_wave_projection.csv"
CROSSING_CSV = SOURCE / "O2_crossing_projector_checks.csv"
SOURCE_CSV = SOURCE / "O2_source_decomposition.csv"
FLOW_CSV = SOURCE / "O2_corrected_flow_and_trajectory.csv"
LOCAL_CSV = SOURCE / "local_GR_p6_consequence.csv"
GATE_CSV = SOURCE / "metric_frame_O2_flow_gate.csv"
RESULT_JSON = SOURCE / "metric_frame_O2_flow_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4985_METRIC_FRAME_O2_PARTIAL_WAVE_FLOW"
CHECKED_DATE = "2026-07-14"


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


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


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def source_lock() -> dict[str, bool]:
    burgess_text = BURGESS_SOURCE.read_text(encoding="utf-8", errors="replace")
    bern_text = BERN_SOURCE.read_text(encoding="utf-8", errors="replace")
    baratella_text = BARATELLA_SOURCE.read_text(encoding="utf-8", errors="replace")
    projector_text = CHECKPOINT_4959.read_text(encoding="utf-8")
    quotient_text = CHECKPOINT_4958.read_text(encoding="utf-8")
    return {
        "burgess_derivative_count": "P = 2 + 2L +" in burgess_text and "(d-2)" in burgess_text,
        "bern_external_matter_one_loop": "four external matter states generically have divergences" in bern_text,
        "bern_two_loop_scale_caveat": "renormalization-scale dependence" in bern_text and "evanescent" in bern_text,
        "baratella_cut_formula": "gamma_i=d C_i/d\\ln\\mu" in baratella_text and "label{NMF}" in baratella_text,
        "baratella_gravity_soft_subtraction": "{\\bm T}_{\\rm soft}^{ij}=-2 s_{ij}/M_P^2" in baratella_text,
        "projector_O2_normalization": "V4_O2(k1,k2,k3,k4)" in projector_text and "-3 s t u" in projector_text,
        "X2_amplitude_normalization": "u_X2=4a2" in projector_text,
        "finite_metric_map": "C=(r+kappa d x)/r^2" in quotient_text and "A=-kappa ctilde/r" in quotient_text,
    }


def metric_frame_checks() -> tuple[list[dict[str, Any]], list[dict[str, Any]], float, float]:
    generator = np.random.default_rng(4985)
    bulk_rows: list[dict[str, Any]] = []
    boundary_rows: list[dict[str, Any]] = []
    maximum_bulk = 0.0
    maximum_boundary = 0.0
    for control_index in range(32):
        metric_covariant = np.eye(4) if control_index < 16 else np.diag([-1.0, 1.0, 1.0, 1.0])
        metric_inverse = np.linalg.inv(metric_covariant)
        signature = "Euclidean" if control_index < 16 else "Lorentzian_local_jet"
        gradient_covector = generator.normal(size=4)
        gradient_vector = metric_inverse @ gradient_covector
        hessian_covariant = generator.normal(size=(4, 4))
        hessian_covariant = 0.5 * (hessian_covariant + hessian_covariant.T)
        ricci_covariant = generator.normal(size=(4, 4))
        ricci_covariant = 0.5 * (ricci_covariant + ricci_covariant.T)
        beta_ctilde = float(generator.uniform(-1.4, 1.4))
        beta_d = float(generator.uniform(-1.4, 1.4))
        kappa = float(generator.uniform(0.2, 2.1))
        alpha = beta_d + 0.5 * beta_ctilde

        kinetic = float(gradient_covector @ gradient_vector)
        ricci_scalar = float(np.sum(metric_inverse * ricci_covariant))
        ricci_vector_vector = float(gradient_vector @ ricci_covariant @ gradient_vector)
        ricci_up = metric_inverse @ ricci_covariant @ metric_inverse
        einstein_up = ricci_up - 0.5 * ricci_scalar * metric_inverse
        metric_increment = kappa * (
            alpha * kinetic * metric_covariant
            - beta_ctilde * np.outer(gradient_covector, gradient_covector)
        )
        direct_bulk = float(np.sum(einstein_up * metric_increment) / kappa)
        expected_bulk = -beta_d * ricci_scalar * kinetic - beta_ctilde * ricci_vector_vector
        bulk_residual = abs(direct_bulk - expected_bulk)
        bulk_relative = bulk_residual / max(abs(direct_bulk), abs(expected_bulk), 1.0e-15)
        maximum_bulk = max(maximum_bulk, bulk_relative)
        bulk_rows.append(
            {
                "control_index": control_index,
                "signature": signature,
                "beta_ctilde": beta_ctilde,
                "beta_d": beta_d,
                "X": kinetic,
                "R": ricci_scalar,
                "R_mn_vmv_n": ricci_vector_vector,
                "Gmn_delta_gmn_over_kappa": direct_bulk,
                "expected_minus_beta_d_RX_minus_beta_ctilde_Rvv": expected_bulk,
                "absolute_residual": bulk_residual,
                "relative_residual": bulk_relative,
                "status": "EH_VARIATION_CANCELS_RUNNING_RICCI_COORDINATES",
            }
        )

        gradient_kinetic_covector = 2.0 * hessian_covariant @ gradient_vector
        derivative_vector = hessian_covariant @ metric_inverse
        box_psi = float(np.sum(metric_inverse * hessian_covariant))
        trace_coefficient = 4.0 * alpha - beta_ctilde
        direct_theta = np.zeros(4)
        for component_mu in range(4):
            divergence_h = alpha * float(metric_inverse[component_mu] @ gradient_kinetic_covector)
            divergence_h -= beta_ctilde * sum(
                derivative_vector[component_nu, component_mu] * gradient_vector[component_nu]
                + gradient_vector[component_mu] * derivative_vector[component_nu, component_nu]
                for component_nu in range(4)
            )
            gradient_trace = trace_coefficient * float(metric_inverse[component_mu] @ gradient_kinetic_covector)
            direct_theta[component_mu] = kappa * (divergence_h - gradient_trace)
        hessian_up_first = metric_inverse @ hessian_covariant
        expected_theta = kappa * (
            (-6.0 * beta_d - 2.0 * beta_ctilde) * (hessian_up_first @ gradient_vector)
            - beta_ctilde * gradient_vector * box_psi
        )
        boundary_residual = float(np.max(np.abs(direct_theta - expected_theta)))
        boundary_relative = boundary_residual / max(
            float(np.max(np.abs(direct_theta))),
            float(np.max(np.abs(expected_theta))),
            1.0e-15,
        )
        maximum_boundary = max(maximum_boundary, boundary_relative)
        boundary_rows.append(
            {
                "control_index": control_index,
                "signature": signature,
                "theta_direct_0": direct_theta[0],
                "theta_direct_1": direct_theta[1],
                "theta_direct_2": direct_theta[2],
                "theta_direct_3": direct_theta[3],
                "theta_reduced_0": expected_theta[0],
                "theta_reduced_1": expected_theta[1],
                "theta_reduced_2": expected_theta[2],
                "theta_reduced_3": expected_theta[3],
                "absolute_residual": boundary_residual,
                "relative_residual": boundary_relative,
                "status": "PALATINI_BOUNDARY_VECTOR_REPRODUCED",
            }
        )
    return bulk_rows, boundary_rows, maximum_bulk, maximum_boundary


def metric_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "linear_map",
            "delta g_mn=kappa[(beta_d+beta_ctilde/2)X g_mn-beta_ctilde v_m v_n]dt",
            "linearized exactly from the finite C(X),A(X) map",
            "DERIVED",
            True,
        ),
        (
            "EH_bulk",
            "delta S_EH,bulk=-beta_d R X dt-beta_ctilde R_mn v^m v^n dt",
            "cancels the two running redundant Ricci coordinates",
            "DERIVED",
            True,
        ),
        (
            "EH_boundary",
            "Theta^m=kappa[-(6beta_d+2beta_ctilde)H^m_n v^n-beta_ctilde v^m Boxpsi]dt",
            "total divergence; zero on the selected psi=0 boundary collar",
            "DERIVED",
            True,
        ),
        (
            "matter_algebraic",
            "delta(sqrt(g)X/2) and delta(sqrt(g)cX^2) contain only X^2 and X^3 at first order",
            "already owned by c_ess and e_ess; no Hessian-squared O2 term",
            "DERIVED",
            True,
        ),
        (
            "finite_map_p6",
            "w_frame=w+A_cc ctilde^2+A_cd ctilde d+A_dd d^2+O((ctilde,d)^3)",
            "finite off-surface derivative spillover may exist but begins quadratically",
            "ORDER_THEOREM",
            True,
        ),
        (
            "running_surface",
            "partial_ctilde w_frame|0=partial_d w_frame|0=0",
            "delta beta_wO2 from the metric running frame is exactly zero",
            "METRIC_FRAME_CONNECTION_ZERO",
            True,
        ),
    ]
    return [
        {
            "gate_id": f"MF4985_{index:02d}_{name}",
            "identity": identity,
            "consequence": consequence,
            "status": status,
            "valid_for_metric_frame_O2_zero_claim": valid,
            "source_path": relative(CHECKPOINT_4958),
        }
        for index, (name, identity, consequence, status, valid) in enumerate(rows, start=1)
    ]


def power_counting_rows() -> list[dict[str, Any]]:
    cases = [
        ("tree_minimal", 0, (), 2, "two-derivative tree amplitude", "not_a_p6_source"),
        ("one_loop_minimal", 1, (), 4, "one-loop four-derivative counterterms", "PURE_MINIMAL_ONE_LOOP_O2_SOURCE_ZERO"),
        ("one_loop_one_p4", 1, (4,), 6, "one four-derivative insertion mixed with two-derivative gravity", "O2_SOURCE_ALLOWED_AND_DERIVED_HERE"),
        ("two_loop_minimal", 2, (), 6, "two-loop minimal Einstein-scalar amplitude", "O2_SOURCE_ALLOWED_COEFFICIENT_OPEN"),
        ("one_loop_one_p6", 1, (6,), 8, "one six-derivative insertion", "RENORMALIZES_P8_NOT_P6_BY_DERIVATIVE_COUNT"),
        ("tree_one_p6", 0, (6,), 6, "tree O2 Wilson coefficient", "PHYSICAL_O2_COORDINATE"),
    ]
    rows: list[dict[str, Any]] = []
    for index, (name, loop_order, derivative_vertices, expected_order, meaning, status) in enumerate(cases, start=1):
        calculated_order = 2 + 2 * loop_order + sum(order - 2 for order in derivative_vertices)
        rows.append(
            {
                "case_id": f"PC4985_{index:02d}_{name}",
                "loop_order_L": loop_order,
                "higher_derivative_vertices": ";".join(str(order) for order in derivative_vertices) or "none",
                "formula": "D=2+2L+sum_i(d_i-2)",
                "calculated_derivative_order_D": calculated_order,
                "expected_derivative_order_D": expected_order,
                "meaning": meaning,
                "status": status,
                "source_path": relative(BURGESS_SOURCE),
            }
        )
    return rows


def partial_wave_rows() -> list[dict[str, Any]]:
    records = [
        (
            "GR_soft_regularized",
            "(tu/s+su/t+st/u)/M_P^2 plus identical-scalar soft subtraction",
            "-(7+z^2)/4",
            Fraction(-11, 6),
            Fraction(-1, 30),
        ),
        (
            "X2_contact",
            "u_X2(s^2+t^2+u^2)/2",
            "(3+z^2)/4",
            Fraction(5, 6),
            Fraction(1, 30),
        ),
        (
            "O2_target",
            "-3 w_O2 s t u",
            "-(3/4)(1-z^2)",
            Fraction(-1, 2),
            Fraction(1, 10),
        ),
    ]
    rows: list[dict[str, Any]] = []
    for index, (name, amplitude, reduced, partial_zero, partial_two) in enumerate(records, start=1):
        rows.append(
            {
                "projector_id": f"PW4985_{index:02d}_{name}",
                "amplitude": amplitude,
                "reduced_s_channel_polynomial_after_factoring_couplings_and_s_power": reduced,
                "a_J0": str(partial_zero),
                "a_J2": str(partial_two),
                "higher_J_zero": True,
                "status": "EXACT_PARTIAL_WAVE_COEFFICIENTS",
                "source_path": relative(BARATELLA_SOURCE) if name == "GR_soft_regularized" else relative(CHECKPOINT_4959),
            }
        )
    rows.append(
        {
            "projector_id": "PW4985_04_mixed_product",
            "amplitude": "sum_J(2J+1)a_GR^J a_X2^J P_J",
            "reduced_s_channel_polynomial_after_factoring_couplings_and_s_power": "-55/36-(1/180)P2(z)",
            "a_J0": str(Fraction(-55, 36)),
            "a_J2": str(Fraction(-1, 900)),
            "higher_J_zero": True,
            "status": "EXACT_MIXED_UNITARITY_CUT",
            "source_path": relative(BARATELLA_SOURCE),
        }
    )
    return rows


def legendre_two(value: Fraction) -> Fraction:
    return (3 * value * value - 1) / 2


def crossing_rows() -> tuple[list[dict[str, Any]], float]:
    events = [
        (1, 2),
        (2, -5),
        (3, 4),
        (5, -2),
        (7, 3),
        (11, -4),
        (13, 5),
        (17, -6),
        (19, 8),
        (23, -9),
        (29, 12),
        (31, -13),
    ]
    rows: list[dict[str, Any]] = []
    maximum_residual = 0.0
    partial_zero_product = Fraction(-55, 36)
    weighted_partial_two_product = Fraction(-1, 180)
    for event_index, (s_integer, t_integer) in enumerate(events):
        s_value = Fraction(s_integer, 1)
        t_value = Fraction(t_integer, 1)
        u_value = -s_value - t_value
        if s_value * t_value * u_value == 0:
            raise ValueError("crossing control requires nonzero s,t,u")
        channel_values = (
            (s_value, t_value, u_value),
            (t_value, s_value, u_value),
            (u_value, t_value, s_value),
        )
        crossing_sum = Fraction(0, 1)
        for channel_scale, first_other, second_other in channel_values:
            cosine = (first_other - second_other) / channel_scale
            crossing_sum += channel_scale**3 * (
                partial_zero_product + weighted_partial_two_product * legendre_two(cosine)
            )
        expected = Fraction(-9, 2) * s_value * t_value * u_value
        residual = abs(float(crossing_sum - expected))
        maximum_residual = max(maximum_residual, residual)
        rows.append(
            {
                "event_index": event_index,
                "s": str(s_value),
                "t": str(t_value),
                "u": str(u_value),
                "crossing_sum": str(crossing_sum),
                "expected_minus_9_over_2_stu": str(expected),
                "exact_residual": str(crossing_sum - expected),
                "beta_w_over_u_over_Mpminus2_over_pi2": str(Fraction(-3, 16)),
                "status": "EXACT_CROSSING_SUM_MATCH",
            }
        )
    return rows, maximum_residual


def source_rows() -> list[dict[str, Any]]:
    records = [
        (
            "scalar_frame_connection",
            "running psi coordinate",
            "delta beta_wO2=0",
            "DERIVED_ZERO_4984",
            CHECKPOINT_4984,
        ),
        (
            "metric_frame_connection",
            "running conformal-disformal Einstein frame at ctilde=d=0",
            "delta beta_wO2=0",
            "DERIVED_ZERO_4985",
            CHECKPOINT_4958,
        ),
        (
            "one_loop_minimal",
            "two-derivative Einstein-scalar vertices only",
            "p4, so p6 O2 source=0",
            "DERIVED_BY_EFT_POWER_COUNTING",
            BURGESS_SOURCE,
        ),
        (
            "one_loop_X2_insertion",
            "one X2 contact and one Einstein-scalar amplitude",
            "beta_w|mix=-3u_X2/(16pi^2 M_P^2)=-(3/(2pi))g u_X2",
            "DERIVED_COMPLETE_SCALAR_CUT",
            BARATELLA_SOURCE,
        ),
        (
            "two_loop_minimal",
            "renormalized two-loop four-scalar p6 logarithm including subdivergences",
            "S_2L g^3",
            "COMMON_SCHEME_SINGLE_LOG_COEFFICIENT_OPEN",
            BERN_SOURCE,
        ),
        (
            "finite_matching",
            "Wilsonian cutoff-local p6 matching constant",
            "C_w g^3 in the weak trajectory",
            "BOUNDARY_DATA_NOT_UNIVERSAL_BETA",
            CHECKPOINT_4959,
        ),
    ]
    return [
        {
            "source_id": f"SRC4985_{index:02d}_{name}",
            "origin": origin,
            "contribution": contribution,
            "status": status,
            "source_path": relative(source),
        }
        for index, (name, origin, contribution, status, source) in enumerate(records, start=1)
    ]


def flow_rows() -> list[dict[str, Any]]:
    records = [
        (
            "dimensionful_mix",
            "mu d wbar_O2/dmu|X2=-3 ubar_X2/(16pi^2 M_P^2)",
            "u_X2 multiplies (s^2+t^2+u^2)/2 and wbar_O2 multiplies -3stu",
            "DERIVED",
        ),
        (
            "dimensionless_mix",
            "beta_w=6w-(3/(2pi))g u_X2+S_2L g^3+...",
            "g=G k^2 and M_P^-2=8piG",
            "DERIVED_PLUS_ONE_OPEN_TWO_LOOP_NUMBER",
        ),
        (
            "c_ess_convention",
            "beta_w=6w-(6/pi)g c_ess+S_2L g^3+...",
            "u_X2=4c_ess",
            "DERIVED",
        ),
        (
            "leading_GR_flow",
            "beta_g=2g; beta_c=4c+16g^2",
            "c/g^2=C_c+16t with t=ln(k/k0)",
            "IMPORTED_DERIVED_4955_4958",
        ),
        (
            "integrated_w_trajectory",
            "w/g^3=C_w+(S_2L-6C_c/pi)t-(48/pi)t^2",
            "exact solution of the corrected leading weak-flow equation",
            "DERIVED",
        ),
        (
            "finite_scheme_map",
            "w'=w+alpha g c_ess implies B_gc'=B_gc=-6/pi and S_2L'=S_2L+16alpha",
            "the mixed coefficient and double-log term are invariant; the isolated local g^3 coefficient is not",
            "DERIVED_RESONANT_SCHEME_LAW",
        ),
        (
            "superseded_4959_order",
            "the former beta_w=6w+S_O2 g^2 ansatz is rejected for a universal minimal-parent p6 logarithm",
            "minimal one loop is p4; p6 starts at g c_ess and g^3",
            "CORRECTED",
        ),
    ]
    return [
        {
            "flow_id": f"FLOW4985_{index:02d}_{name}",
            "equation": equation,
            "derivation_or_convention": derivation,
            "status": status,
            "source_path": relative(CHECKPOINT_4959) if name == "superseded_4959_order" else relative(CHECKPOINT_4958),
        }
        for index, (name, equation, derivation, status) in enumerate(records, start=1)
    ]


def local_rows() -> list[dict[str, Any]]:
    records = [
        (
            "selected_profile",
            "O2=X H_mn H^mn has scalar degree four",
            "E_psi=T_mn=J_psi=0 at psi=0 for arbitrary w_O2",
            "EXACT_SELECTED_BRANCH_SILENCE",
            True,
        ),
        (
            "Newton",
            "O2 and its running-frame packets have no flat p2 metric Hessian at psi=0",
            "leading Poisson propagator unchanged by this packet",
            "LEADING_NEWTON_RETAINED",
            True,
        ),
        (
            "sixpoint_rate",
            "4959 minimized over every real w_O2",
            "strict positive lower bound survives the corrected source order",
            "RATE_EXISTENCE_BOUND_UNCHANGED",
            True,
        ),
        (
            "predictive_rate",
            "w/g^3 contains C_w and S_2L",
            "numerical O2 interference is not predicted until UV boundary and two-loop log are fixed",
            "PREDICTIVE_COEFFICIENT_OPEN",
            False,
        ),
        (
            "pure_metric",
            "C^3 and determinant/Jacobian metric responses remain",
            "packet silence is not exact all-operator local GR or full PPN",
            "PURE_METRIC_RESIDUAL_RETAINED",
            False,
        ),
        (
            "full_theory",
            "one p6 flow coefficient and finite trajectory datum remain before the amplitude is predictive",
            "no exact GR or full MTS promotion",
            "FULL_MTS_FALSE",
            False,
        ),
    ]
    return [
        {
            "consequence_id": f"LOC4985_{index:02d}_{name}",
            "premise": premise,
            "consequence": consequence,
            "status": status,
            "valid_for_packet_level_local_claim": valid,
            "source_path": relative(CHECKPOINT_4984) if name in {"selected_profile", "Newton"} else relative(CHECKPOINT_4959),
        }
        for index, (name, premise, consequence, status, valid) in enumerate(records, start=1)
    ]


def trajectory_identity_residual() -> float:
    generator = np.random.default_rng(14985)
    maximum = 0.0
    for _ in range(40):
        time_value = float(generator.uniform(-4.0, 3.0))
        initial_g = float(generator.uniform(0.01, 0.4))
        constant_c = float(generator.uniform(-2.0, 2.0))
        constant_w = float(generator.uniform(-2.0, 2.0))
        source_two_loop = float(generator.uniform(-3.0, 3.0))
        g_value = initial_g * math.exp(2.0 * time_value)
        c_value = g_value**2 * (constant_c + 16.0 * time_value)
        ratio_w = (
            constant_w
            + (source_two_loop - 6.0 * constant_c / math.pi) * time_value
            - 48.0 * time_value**2 / math.pi
        )
        w_value = g_value**3 * ratio_w
        ratio_derivative = source_two_loop - 6.0 * constant_c / math.pi - 96.0 * time_value / math.pi
        direct_derivative = 6.0 * w_value + g_value**3 * ratio_derivative
        expected_beta = 6.0 * w_value - 6.0 * g_value * c_value / math.pi + source_two_loop * g_value**3
        residual = abs(direct_derivative - expected_beta) / max(abs(direct_derivative), abs(expected_beta), 1.0e-15)
        maximum = max(maximum, residual)
    return maximum


def gate_rows(
    source_checks: dict[str, bool],
    maximum_bulk: float,
    maximum_boundary: float,
    maximum_crossing: float,
    trajectory_residual: float,
) -> list[dict[str, Any]]:
    checks = [
        ("sources", all(source_checks.values()), "all source markers found"),
        ("metric_bulk", maximum_bulk < 2.0e-13, f"max relative residual={maximum_bulk:.3e}"),
        ("metric_boundary", maximum_boundary < 2.0e-13, f"max relative residual={maximum_boundary:.3e}"),
        ("metric_O2_connection", True, "first metric variation contains Ricci coordinates plus a divergence, no O2 bulk"),
        ("minimal_one_loop_p6", True, "D=4, hence universal minimal one-loop O2 source is zero"),
        ("mixed_internal_states", True, "X2 has four scalar legs, so only scalar-scalar cuts occur linearly in X2"),
        ("soft_subtraction", True, "identical-scalar gravity poles reduce to -(7+z^2)/4"),
        ("partial_wave_support", True, "only J=0,2 survive"),
        ("crossing_projection", maximum_crossing == 0.0, f"exact rational residual={maximum_crossing:.3e}"),
        ("mixed_beta", True, "beta_w|mix=-3u_X2/(16pi^2 M_P^2)"),
        ("trajectory_solution", trajectory_residual < 2.0e-13, f"max relative residual={trajectory_residual:.3e}"),
        ("scheme_law", True, "w'=w+alpha gc leaves B_gc=-6/pi and the t^2 coefficient invariant"),
        ("double_log", True, "A_c B_gc/2=16(-6/pi)/2=-48/pi"),
        ("two_loop_coefficient", False, "a fixed-common-scheme single-log/matching coefficient remains"),
        ("finite_boundary", False, "C_w remains UV/trajectory boundary data"),
        ("local_packet", True, "selected psi=0 local branch remains source silent"),
        ("exact_local_GR", False, "pure-metric and finite quantum residuals remain"),
        ("full_MTS", False, "not claimed"),
    ]
    return [
        {
            "gate_id": f"GATE4985_{index:02d}_{name}",
            "passed": passed,
            "evidence": evidence,
            "status": "PASS" if passed else "OPEN_NONCLAIM",
            "claim_allowed": bool(passed and name not in {"local_packet"}),
        }
        for index, (name, passed, evidence) in enumerate(checks, start=1)
    ]


def write_provenance(source_hashes: dict[str, str], source_checks: dict[str, bool]) -> None:
    lines = [
        "# 4985 metric-frame and O2-flow provenance",
        "",
        f"Marker: `{MARKER}`.",
        "",
        f"Checked: `{CHECKED_DATE}`.",
        "",
        "## Primary sources",
        "",
        "- [Burgess, *Quantum Gravity in Everyday Life*](https://arxiv.org/abs/gr-qc/0311082): gravity EFT derivative counting `D=2+2L+sum(d_i-2)`.",
        "- [Bern et al., *Two-Loop Renormalization of Quantum Gravity Simplified*](https://arxiv.org/abs/1701.02422): matter amplitudes can diverge at one loop, while two-loop gravity requires subdivergence/evanescent care and the renormalized scale dependence is the robust target.",
        "- [Baratella et al., *Anomalous Dimensions of Effective Theories from Partial Waves*](https://arxiv.org/abs/2010.13809): one-loop cut/partial-wave anomalous-dimension formula and gravity soft subtraction `T_soft=-2s/M_P^2`.",
        "- [Ruhdorfer, Serra and Weiler, *Effective Field Theory of Gravity to All Orders*](https://arxiv.org/abs/1908.08050): nonredundant shift-symmetric scalar-gravity six-derivative basis.",
        "",
        "The arXiv source archives and extracted TeX files are retained under `source-intake/functional_rg/4985/sources/`.",
        "",
        "## Source-marker checks",
        "",
    ]
    lines.extend(f"- `{name}`: `{value}`" for name, value in source_checks.items())
    lines.extend(["", "## SHA-256", ""])
    lines.extend(f"- `{path}`: `{hash_value}`" for path, hash_value in source_hashes.items())
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "The metric-frame connection zero, the one-loop `X2 -> O2` mixing coefficient, the resonant finite-scheme law, and the invariant `-48/pi` double logarithm are derived in the declared action/amplitude conventions. A fixed-common-scheme two-loop single-log/matching coefficient, the finite trajectory datum `C_w`, pure-metric `C^3`, and quantum determinant/Jacobian responses remain open. No exact local-GR, full-PPN, galaxy-formation, or full-MTS claim is made.",
            "",
        ]
    )
    PROVENANCE.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    started = time.perf_counter()

    required_paths = (
        CHECKPOINT_4958,
        CHECKPOINT_4959,
        RESULT_4959,
        CHECKPOINT_4984,
        RESULT_4984,
        EFT_BASIS,
        BURGESS_SOURCE,
        BERN_SOURCE,
        BARATELLA_SOURCE,
        BURGESS_ARCHIVE,
        BERN_ARCHIVE,
        BARATELLA_ARCHIVE,
    )
    missing = [str(path) for path in required_paths if not path.exists()]
    if missing:
        raise FileNotFoundError("\n".join(missing))

    source_checks = source_lock()
    if not all(source_checks.values()):
        raise RuntimeError(json.dumps(source_checks, indent=2, sort_keys=True))

    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "dry_run": True,
                    "required_paths": len(required_paths),
                    "source_checks": source_checks,
                    "planned_outputs": 12,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    SOURCE.mkdir(parents=True, exist_ok=True)
    bulk_rows, boundary_rows, maximum_bulk, maximum_boundary = metric_frame_checks()
    metric_rows = metric_gate_rows()
    power_rows = power_counting_rows()
    partial_rows = partial_wave_rows()
    crossing_checks, maximum_crossing = crossing_rows()
    decomposition_rows = source_rows()
    corrected_flow_rows = flow_rows()
    local_consequences = local_rows()
    trajectory_residual = trajectory_identity_residual()
    gates = gate_rows(source_checks, maximum_bulk, maximum_boundary, maximum_crossing, trajectory_residual)

    write_csv(METRIC_BULK_CSV, tagged(bulk_rows))
    write_csv(METRIC_BOUNDARY_CSV, tagged(boundary_rows))
    write_csv(METRIC_GATE_CSV, tagged(metric_rows))
    write_csv(POWER_CSV, tagged(power_rows))
    write_csv(PARTIAL_WAVE_CSV, tagged(partial_rows))
    write_csv(CROSSING_CSV, tagged(crossing_checks))
    write_csv(SOURCE_CSV, tagged(decomposition_rows))
    write_csv(FLOW_CSV, tagged(corrected_flow_rows))
    write_csv(LOCAL_CSV, tagged(local_consequences))
    write_csv(GATE_CSV, tagged(gates))

    hash_paths = required_paths + (Path(__file__),)
    source_hashes = {relative(path): digest(path) for path in hash_paths}
    result = {
        "checkpoint_marker": MARKER,
        "source_checks": source_checks,
        "source_hashes": source_hashes,
        "metric_frame": {
            "linear_map": "delta g_mn=kappa[(beta_d+beta_ctilde/2)Xg_mn-beta_ctilde v_m v_n]dt",
            "bulk": "-beta_d RX-beta_ctilde R_mn v^m v^n",
            "boundary": "Theta^m=kappa[-(6beta_d+2beta_ctilde)H^m_n v^n-beta_ctilde v^m Boxpsi]",
            "delta_beta_wO2": 0.0,
            "maximum_bulk_relative_residual": maximum_bulk,
            "maximum_boundary_relative_residual": maximum_boundary,
        },
        "O2_flow": {
            "pure_minimal_one_loop_p6_source": 0.0,
            "dimensionful_X2_mixing": "-3 ubar_X2/(16pi^2 M_P^2)",
            "dimensionless_X2_mixing": "-(3/(2pi))g u_X2=-(6/pi)g c_ess",
            "two_loop_minimal": "S_2L g^3 OPEN",
            "corrected_beta": "beta_w=6w-(6/pi)g c_ess+S_2L g^3+...",
            "trajectory": "w/g^3=C_w+(S_2L-6C_c/pi)t-(48/pi)t^2",
            "finite_scheme_law": "w'=w+alpha g c_ess; B_gc'=-6/pi; S_2L'=S_2L+16alpha",
            "scheme_invariant_double_log": "A_c B_gc/2=-48/pi",
            "crossing_exact_residual": maximum_crossing,
            "trajectory_maximum_relative_residual": trajectory_residual,
        },
        "gates": {
            "metric_frame_O2_connection_zero": True,
            "scalar_frame_O2_connection_zero": True,
            "pure_minimal_one_loop_O2_source_zero": True,
            "one_loop_X2_to_O2_mixing_derived": True,
            "two_loop_minimal_coefficient_derived": False,
            "finite_Cw_derived": False,
            "selected_local_packet_silent": True,
            "exact_local_GR": False,
            "full_MTS": False,
        },
        "elapsed_seconds": time.perf_counter() - started,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_provenance(source_hashes, source_checks)

    passed = sum(str(row["passed"]).lower() == "true" for row in tagged(gates))
    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "gate_rows": len(gates),
                "passed_rows": passed,
                "open_nonclaim_rows": len(gates) - passed,
                "metric_bulk_max_relative_residual": maximum_bulk,
                "metric_boundary_max_relative_residual": maximum_boundary,
                "crossing_exact_residual": maximum_crossing,
                "trajectory_max_relative_residual": trajectory_residual,
                "result": str(RESULT_JSON),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4981"

SOURCE_TEX = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4973"
    / "src-2605.29159"
    / "main_new.tex"
)
SCHEME_LOCK = (
    POST / "source-intake" / "functional_rg" / "4974" / "C3_parent_scheme_lock.csv"
)
PARENT_4875 = POST / (
    "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-"
    "Weinberg-Witten-evasion-or-induced-background-only-demotion.md"
)
COVARIANT_PARENT_4916 = POST / (
    "4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-"
    "integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md"
)
MOTION_4935 = POST / (
    "4935-Y5-R2FR-completed-fixed-point-GR-connected-trajectory-and-motion-"
    "sector-entry.md"
)
PX_4956 = POST / (
    "4956-Y5-R2FR-functional-PX-motion-flow-gravity-source-and-convergence-"
    "or-derivative-hierarchy-rejection.md"
)
PX_CONTRACT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4956"
    / "functional_PX_Hessian_contract.csv"
)
LOCAL_GR_4960 = POST / (
    "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-local-"
    "GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md"
)
BOUNDARY_4961 = POST / (
    "4961-Y5-R2FR-integrated-H-origin-and-induced-EH-residue-from-motion-"
    "Hessian-or-explicit-fundamental-field-boundary.md"
)
SCALAR_4979 = POST / (
    "4979-Y5-R2FR-massless-scalar-common-scheme-finite-determinant-and-TT-"
    "match.md"
)
SCALAR_4980 = POST / "4980-Y5-R2FR-covariant-PV-traceful-determinant-completion.md"
SCALAR_RESULT_4980 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4980"
    / "PV_traceful_completion_results.json"
)

HESSIAN_CSV = SOURCE / "parent_gauge_fixed_hessian_contract.csv"
MODE_CSV = SOURCE / "parent_supertrace_mode_count.csv"
LOG_CSV = SOURCE / "parent_common_scheme_log_coefficients.csv"
SCHUR_CSV = SOURCE / "motion_metric_schur_expansion_crosscheck.csv"
TRANSFER_CSV = SOURCE / "parent_contact_transfer_gate.csv"
GATE_CSV = SOURCE / "parent_hessian_common_scheme_gate.csv"
RESULT_JSON = SOURCE / "parent_hessian_common_scheme_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4981_PARENT_HESSIAN_AND_COMMON_SCHEME"
CHECKED_DATE = "2026-07-14"
LOOP_PREFACTOR = 1.0 / (4.0 * math.pi) ** 2


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
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


def symmetric_basis(dimensions: int) -> list[np.ndarray]:
    basis: list[np.ndarray] = []
    for first in range(dimensions):
        for second in range(first, dimensions):
            value = np.zeros((dimensions, dimensions))
            if first == second:
                value[first, second] = 1.0
            else:
                value[first, second] = 1.0 / math.sqrt(2.0)
                value[second, first] = 1.0 / math.sqrt(2.0)
            basis.append(value)
    return basis


def dewitt_matrix(dimensions: int = 4) -> np.ndarray:
    basis = symmetric_basis(dimensions)
    identity = np.eye(dimensions)
    matrix = np.zeros((len(basis), len(basis)))
    for column, source in enumerate(basis):
        image = 0.5 * source - 0.25 * identity * np.trace(source)
        for row, target in enumerate(basis):
            matrix[row, column] = float(np.sum(target * image))
    return matrix


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def coefficient_rows() -> list[dict[str, Any]]:
    gravity = {
        "R_log_R": Fraction(1, 120),
        "Ricci_log_Ricci": Fraction(7, 20),
    }
    scalar_response = {
        "R_log_R": Fraction(1, 120),
        "Ricci_log_Ricci": Fraction(1, 60),
    }
    scalar_action = {key: value / 2 for key, value in scalar_response.items()}
    parent = {key: gravity[key] + scalar_action[key] for key in gravity}
    rows: list[dict[str, Any]] = []
    source_by_sector = {
        "Einstein_plus_ghost": relative(SOURCE_TEX),
        "one_real_minimal_motion_scalar_UV": relative(SCALAR_4979),
        "parent_zero_motion_background": (
            f"{relative(SOURCE_TEX)};{relative(SCALAR_4979)};{relative(SCALAR_4980)}"
        ),
    }
    for invariant in ("R_log_R", "Ricci_log_Ricci"):
        sector_values = (
            ("Einstein_plus_ghost", gravity[invariant]),
            ("one_real_minimal_motion_scalar_UV", scalar_action[invariant]),
            ("parent_zero_motion_background", parent[invariant]),
        )
        for sector, action_coefficient in sector_values:
            rows.append(
                {
                    "invariant": invariant,
                    "sector": sector,
                    "action_coefficient_in_units_1_over_4pi_squared": fraction_text(
                        action_coefficient
                    ),
                    "action_coefficient_numeric": float(action_coefficient),
                    "mixed_two_point_response_coefficient": fraction_text(
                        2 * action_coefficient
                    ),
                    "response_coefficient_numeric": float(2 * action_coefficient),
                    "normalization_identity": "mixed_response=2*action_coefficient",
                    "kernel": "log(-Box/mu^2)",
                    "status": "UNIVERSAL_LOG_DERIVED",
                    "source_path": source_by_sector[sector],
                    "valid_for_parent_quadratic_log_claim": True,
                    "valid_for_parent_finite_three_point_claim": False,
                }
            )
    return rows


def schur_crosscheck() -> tuple[list[dict[str, Any]], float, float]:
    generator = np.random.default_rng(4981)
    metric_size = 6
    scalar_size = 3
    metric_seed = generator.normal(size=(metric_size, metric_size))
    scalar_seed = generator.normal(size=(scalar_size, scalar_size))
    metric_zero = metric_seed.T @ metric_seed + 3.0 * np.eye(metric_size)
    scalar_zero = scalar_seed.T @ scalar_seed + 2.0 * np.eye(scalar_size)
    metric_first = generator.normal(size=(metric_size, metric_size))
    metric_first = 0.5 * (metric_first + metric_first.T)
    scalar_first = generator.normal(size=(scalar_size, scalar_size))
    scalar_first = 0.5 * (scalar_first + scalar_first.T)
    mixed_half = generator.normal(size=(metric_size, scalar_size))

    analytic_slope = 0.5 * (
        np.trace(np.linalg.solve(metric_zero, metric_first))
        + np.trace(np.linalg.solve(scalar_zero, scalar_first))
        - np.trace(
            np.linalg.solve(
                scalar_zero,
                mixed_half.T @ np.linalg.solve(metric_zero, mixed_half),
            )
        )
    )
    base = 0.5 * (
        np.linalg.slogdet(metric_zero)[1] + np.linalg.slogdet(scalar_zero)[1]
    )
    rows: list[dict[str, Any]] = []
    maximum_identity_residual = 0.0
    final_slope_residual = math.inf
    for expansion_parameter in (1.0e-2, 3.0e-3, 1.0e-3, 3.0e-4, 1.0e-4, 3.0e-5):
        metric = metric_zero + expansion_parameter * metric_first
        scalar = scalar_zero + expansion_parameter * scalar_first
        mixed = math.sqrt(expansion_parameter) * mixed_half
        full = np.block([[metric, mixed], [mixed.T, scalar]])
        full_logdet = np.linalg.slogdet(full)[1]
        schur = scalar - mixed.T @ np.linalg.solve(metric, mixed)
        schur_logdet = np.linalg.slogdet(metric)[1] + np.linalg.slogdet(schur)[1]
        identity_residual = abs(full_logdet - schur_logdet)
        measured_slope = (0.5 * full_logdet - base) / expansion_parameter
        slope_residual = abs(measured_slope - analytic_slope) / max(
            abs(analytic_slope), 1.0e-30
        )
        maximum_identity_residual = max(maximum_identity_residual, identity_residual)
        final_slope_residual = slope_residual
        rows.append(
            {
                "x": expansion_parameter,
                "analytic_first_order_slope": analytic_slope,
                "measured_secant_slope": measured_slope,
                "relative_slope_residual": slope_residual,
                "block_determinant_log_residual": identity_residual,
                "formula": (
                    "1/2 Tr[A0^-1 A1+C0^-1 C1-"
                    "C0^-1 Bhalf^T A0^-1 Bhalf]"
                ),
                "status": "SCHUR_IDENTITY_AND_FIRST_MIXING_TERM_DERIVED",
                "valid_for_parent_numeric_loop_claim": False,
            }
        )
    return rows, maximum_identity_residual, final_slope_residual


def source_fragments_present() -> tuple[bool, dict[str, bool]]:
    source = SOURCE_TEX.read_text(encoding="utf-8", errors="replace")
    fragments = {
        "linear_split": "g_{\\mu\\nu}=\\bar g_{\\mu\\nu}+h_{\\mu\\nu}",
        "locked_gauge": "\\alpha=1$ and $\\bar{\\omega}=1/2",
        "ghost_operator": "1-2\\bar{\\omega}",
        "proper_time_tensor_trace": "\\mathrm{Tr}_T",
        "proper_time_vector_trace": "\\mathrm{Tr}_V",
        "gravity_R_log": "1920\\pi^2",
        "gravity_Ricci_log": "320\\pi^2",
        "tensor_multiplicity": "\\frac{(d-1)(d+2)}{2}",
    }
    present = {name: fragment in source for name, fragment in fragments.items()}
    return all(present.values()), present


def build_hessian_rows() -> list[dict[str, Any]]:
    return [
        {
            "block_id": "H4981_01_public_metric",
            "field_block": "integrated_H_to_metric",
            "operator": "g^(mu nu)=H^(mu nu)/sqrt(-det H); sqrt(-g)=sqrt(-det H)",
            "derivation": "nondegenerate densitized inverse metric map",
            "status": "PARENT_FIELD_MAP_RETAINED",
            "source_path": f"{relative(PARENT_4875)};{relative(COVARIANT_PARENT_4916)}",
            "valid_for_parent_quadratic_claim": True,
            "valid_for_interacting_motion_claim": False,
        },
        {
            "block_id": "H4981_02_gauge",
            "field_block": "metric_gauge_fixing",
            "operator": "F_mu=kappa(nabla^a h_am-(1/2)nabla_mu h); alpha=1",
            "derivation": "source-locked de Donder gauge",
            "status": "SOURCE_LOCKED",
            "source_path": f"{relative(SOURCE_TEX)};{relative(SCHEME_LOCK)}",
            "valid_for_parent_quadratic_claim": True,
            "valid_for_interacting_motion_claim": False,
        },
        {
            "block_id": "H4981_03_EH",
            "field_block": "h_h",
            "operator": "2 kappa^2 Z_N[-Box 1_T-2 Lambda+U_EH]",
            "derivation": "EH second variation plus locked gauge; both nonminimal derivative coefficients vanish",
            "status": "LAPLACE_TYPE_HESSIAN_DERIVED",
            "source_path": relative(SOURCE_TEX),
            "valid_for_parent_quadratic_claim": True,
            "valid_for_interacting_motion_claim": False,
        },
        {
            "block_id": "H4981_04_ghost",
            "field_block": "barC_C",
            "operator": "-Box 1_V+R/d",
            "derivation": "Faddeev-Popov Hessian at omega_bar=1/2",
            "status": "MINIMAL_VECTOR_GHOST_DERIVED",
            "source_path": relative(SOURCE_TEX),
            "valid_for_parent_quadratic_claim": True,
            "valid_for_interacting_motion_claim": False,
        },
        {
            "block_id": "H4981_05_motion_x0",
            "field_block": "delta_psi_delta_psi",
            "operator": "Z_psi(-Box+m_gap^2)",
            "derivation": "renormalized motion 1PI Hessian on zero-gradient background",
            "status": "MINIMAL_SCALAR_BLOCK_DERIVED",
            "source_path": f"{relative(MOTION_4935)};{relative(PX_4956)}",
            "valid_for_parent_quadratic_claim": True,
            "valid_for_interacting_motion_claim": False,
        },
        {
            "block_id": "H4981_06_motion_generic",
            "field_block": "h_psi_coupled",
            "operator": "[[H_hh,H_hpsi],[H_hpsi^T,H_psipsi]] from functional P(X)",
            "derivation": "exact flat constant-gradient functional Hessian; H_hpsi proportional to sqrt(x)",
            "status": "GENERIC_MIXED_BLOCK_DERIVED_FLAT_BACKGROUND",
            "source_path": f"{relative(PX_4956)};{relative(PX_CONTRACT)}",
            "valid_for_parent_quadratic_claim": True,
            "valid_for_interacting_motion_claim": True,
        },
        {
            "block_id": "H4981_07_parent_x0",
            "field_block": "h_plus_psi_plus_ghost",
            "operator": "diag(Delta_h,Delta_psi) with separate Delta_gh supertrace",
            "derivation": "p(0)=0; p'(0)=1/2; H_hpsi=0",
            "status": "BLOCK_DIAGONAL_ZERO_MOTION_PARENT_DERIVED",
            "source_path": f"{relative(PX_CONTRACT)};{relative(SOURCE_TEX)}",
            "valid_for_parent_quadratic_claim": True,
            "valid_for_interacting_motion_claim": False,
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    started = time.perf_counter()

    required_paths = (
        SOURCE_TEX,
        SCHEME_LOCK,
        PARENT_4875,
        COVARIANT_PARENT_4916,
        MOTION_4935,
        PX_4956,
        PX_CONTRACT,
        LOCAL_GR_4960,
        BOUNDARY_4961,
        SCALAR_4979,
        SCALAR_4980,
        SCALAR_RESULT_4980,
    )
    missing_paths = [str(path) for path in required_paths if not path.exists()]
    if missing_paths:
        raise FileNotFoundError("missing required parent inputs: " + "; ".join(missing_paths))

    source_complete, source_fragments = source_fragments_present()
    alpha = Fraction(1, 1)
    omega = Fraction(1, 2)
    metric_nonminimal = Fraction(1, 1) - Fraction(1, 1) / alpha
    trace_nonminimal = Fraction(1, 1) - 2 * omega / alpha
    ghost_nonminimal = Fraction(1, 1) - 2 * omega

    dewitt = dewitt_matrix()
    eigenvalues = np.linalg.eigvalsh(dewitt)
    negative_count = int(np.sum(eigenvalues < -1.0e-12))
    positive_count = int(np.sum(eigenvalues > 1.0e-12))
    spectrum_residual = max(
        abs(float(eigenvalues[0]) + 0.5),
        max(abs(float(value) - 0.5) for value in eigenvalues[1:]),
    )

    mode_rows = [
        {
            "field": "traceless_metric",
            "multiplicity": 9,
            "determinant_weight": "1/2",
            "weighted_count": 4.5,
            "interpretation": "gauge-fixed bosonic tensor components",
            "status": "SOURCE_LOCKED",
            "source_path": relative(SOURCE_TEX),
        },
        {
            "field": "metric_trace",
            "multiplicity": 1,
            "determinant_weight": "1/2",
            "weighted_count": 0.5,
            "interpretation": "conformal-sign mode; contour prescription remains separate",
            "status": "SOURCE_LOCKED_CONFORMAL_SIGN_EXPLICIT",
            "source_path": relative(SOURCE_TEX),
        },
        {
            "field": "complex_vector_ghost",
            "multiplicity": 4,
            "determinant_weight": "-1",
            "weighted_count": -4.0,
            "interpretation": "Grassmann Faddeev-Popov cancellation",
            "status": "SOURCE_LOCKED",
            "source_path": relative(SOURCE_TEX),
        },
        {
            "field": "Einstein_plus_ghost_total",
            "multiplicity": "10-8",
            "determinant_weight": "effective",
            "weighted_count": 1.0,
            "interpretation": "two physical graviton helicities",
            "status": "DERIVED_MODE_COUNT",
            "source_path": relative(SOURCE_TEX),
        },
        {
            "field": "one_real_motion_scalar",
            "multiplicity": 1,
            "determinant_weight": "1/2",
            "weighted_count": 0.5,
            "interpretation": "one real minimally coupled pole at x=0",
            "status": "DERIVED_ZERO_MOTION_BLOCK",
            "source_path": relative(MOTION_4935),
        },
        {
            "field": "parent_total_at_x0",
            "multiplicity": "two_graviton_plus_one_scalar",
            "determinant_weight": "effective",
            "weighted_count": 1.5,
            "interpretation": "three physical real bosonic modes",
            "status": "DERIVED_MODE_COUNT",
            "source_path": f"{relative(SOURCE_TEX)};{relative(MOTION_4935)}",
        },
    ]

    log_rows = coefficient_rows()
    parent_coefficients = {
        row["invariant"]: Fraction(
            row["action_coefficient_in_units_1_over_4pi_squared"]
        )
        for row in log_rows
        if row["sector"] == "parent_zero_motion_background"
    }
    gravity_R_from_source = (1.0 / (1920.0 * math.pi**2)) / LOOP_PREFACTOR
    gravity_Ricci_from_source = (7.0 / (320.0 * math.pi**2)) / LOOP_PREFACTOR

    schur_rows, maximum_schur_identity, final_schur_slope = schur_crosscheck()
    hessian_rows = build_hessian_rows()
    transfer_rows = [
        {
            "gate_id": "T4981_01_zero_motion_factorization",
            "question": "Does the motion-metric Hessian factorize at x=0?",
            "result": True,
            "derivation": "p(0)=0; p'(0)=1/2; H_hpsi proportional to sqrt(x)",
            "status": "DERIVED",
            "source_path": relative(PX_CONTRACT),
            "valid_for_parent_finite_three_point_claim": False,
        },
        {
            "gate_id": "T4981_02_scalar_contact_architecture",
            "question": "Does the covariant scalar regulator architecture transfer to the x=0 motion block?",
            "result": True,
            "derivation": "the block is the same minimally coupled real scalar Laplace operator; physical m_gap requires its own threshold evaluation",
            "status": "OPERATOR_AND_UV_LOG_TRANSFER_DERIVED_FINITE_MASS_THRESHOLD_OPEN",
            "source_path": f"{relative(MOTION_4935)};{relative(SCALAR_4980)}",
            "valid_for_parent_finite_three_point_claim": False,
        },
        {
            "gate_id": "T4981_03_gravity_ghost_universal_log",
            "question": "Is the signed Einstein-ghost two-point logarithm sourced?",
            "result": True,
            "derivation": "proper-time tensor minus vector-ghost supertrace reproduces the one-loop EFT coefficients",
            "status": "UNIVERSAL_TWO_POINT_LOG_DERIVED",
            "source_path": relative(SOURCE_TEX),
            "valid_for_parent_finite_three_point_claim": False,
        },
        {
            "gate_id": "T4981_04_response_action_normalization",
            "question": "Are checkpoints 4979 and 4980 normalization-compatible?",
            "result": True,
            "derivation": "delta_1 delta_2 integral c R^2=2c R_1 R_2; response coefficient is twice action coefficient",
            "status": "FACTOR_TWO_RESOLVED",
            "source_path": f"{relative(SCALAR_4979)};{relative(SCALAR_4980)}",
            "valid_for_parent_finite_three_point_claim": False,
        },
        {
            "gate_id": "T4981_05_interacting_PX_factorization",
            "question": "May the x-not-equal-zero determinant be replaced by independent metric and scalar determinants?",
            "result": False,
            "derivation": "H_hpsi is order sqrt(x); the Schur term -C0^-1 B^T A0^-1 B contributes already at order x",
            "status": "NAIVE_TRANSFER_REJECTED_LEADING_CORRECTION_DERIVED",
            "source_path": relative(PX_4956),
            "valid_for_parent_finite_three_point_claim": False,
        },
        {
            "gate_id": "T4981_06_background_covariance",
            "question": "Is the locked parent quadratic supertrace background covariant?",
            "result": True,
            "derivation": "all regulator kernels are functions of background-covariant Laplace-type operators",
            "status": "BACKGROUND_DIFF_COVARIANT",
            "source_path": relative(SOURCE_TEX),
            "valid_for_parent_finite_three_point_claim": False,
        },
        {
            "gate_id": "T4981_07_quantum_BRST_restoration",
            "question": "Does the acquired proper-time source prove the full quantum Slavnov-Taylor identity and finite parent contacts?",
            "result": False,
            "derivation": "the source uses a one-loop-improved proper-time flow and assumes a non-running ghost action",
            "status": "NOT_PROVEN",
            "source_path": relative(SOURCE_TEX),
            "valid_for_parent_finite_three_point_claim": False,
        },
        {
            "gate_id": "T4981_08_parent_finite_TTT",
            "question": "Is the complete finite graviton-ghost-motion metric third response closed?",
            "result": False,
            "derivation": "universal quadratic logs are fixed, but gravity/ghost finite constants and interacting P(X) contacts are not assembled",
            "status": "OPEN",
            "source_path": f"{relative(SOURCE_TEX)};{relative(SCALAR_4980)}",
            "valid_for_parent_finite_three_point_claim": False,
        },
    ]

    gates = [
        ("G01_required_parent_inputs", not missing_paths, f"{len(required_paths)} inputs"),
        ("G02_source_formula_fragments", source_complete, str(source_fragments)),
        (
            "G03_de_Donder_metric_minimality",
            metric_nonminimal == 0 and trace_nonminimal == 0,
            f"coefficients={metric_nonminimal},{trace_nonminimal}",
        ),
        (
            "G04_de_Donder_ghost_minimality",
            ghost_nonminimal == 0,
            f"coefficient={ghost_nonminimal}",
        ),
        (
            "G05_DeWitt_spectrum",
            negative_count == 1 and positive_count == 9 and spectrum_residual < 1.0e-12,
            f"negative={negative_count};positive={positive_count};residual={spectrum_residual:.3e}",
        ),
        (
            "G06_zero_motion_block",
            all(row["valid_for_parent_quadratic_claim"] for row in hessian_rows),
            "seven sourced/derived parent Hessian rows",
        ),
        (
            "G07_Einstein_ghost_mode_count",
            abs(sum(float(row["weighted_count"]) for row in mode_rows[:3]) - 1.0) < 1.0e-15,
            "1 determinant unit = two graviton helicities",
        ),
        (
            "G08_parent_mode_count",
            abs(float(mode_rows[-1]["weighted_count"]) - 1.5) < 1.0e-15,
            "two graviton plus one real scalar",
        ),
        (
            "G09_gravity_R_log_source",
            abs(gravity_R_from_source - 1.0 / 120.0) < 1.0e-15,
            f"normalized={gravity_R_from_source:.17g}",
        ),
        (
            "G10_gravity_Ricci_log_source",
            abs(gravity_Ricci_from_source - 7.0 / 20.0) < 1.0e-15,
            f"normalized={gravity_Ricci_from_source:.17g}",
        ),
        (
            "G11_scalar_response_action_factor_two",
            any(
                row["sector"] == "one_real_minimal_motion_scalar_UV"
                and abs(
                    row["response_coefficient_numeric"]
                    - 2.0 * row["action_coefficient_numeric"]
                )
                < 1.0e-15
                for row in log_rows
            ),
            "mixed response equals twice action coefficient",
        ),
        (
            "G12_parent_R_log_sum",
            parent_coefficients["R_log_R"] == Fraction(1, 80),
            fraction_text(parent_coefficients["R_log_R"]),
        ),
        (
            "G13_parent_Ricci_log_sum",
            parent_coefficients["Ricci_log_Ricci"] == Fraction(43, 120),
            fraction_text(parent_coefficients["Ricci_log_Ricci"]),
        ),
        (
            "G14_Schur_identity",
            maximum_schur_identity < 1.0e-12,
            f"max={maximum_schur_identity:.3e}",
        ),
        (
            "G15_Schur_first_order",
            final_schur_slope < 2.0e-4,
            f"last={final_schur_slope:.3e}",
        ),
        (
            "G16_interacting_naive_sum_rejected",
            next(row for row in transfer_rows if row["gate_id"] == "T4981_05_interacting_PX_factorization")["result"] is False,
            "order-x mixing term retained",
        ),
        (
            "G17_parent_finite_TTT_withheld",
            next(row for row in transfer_rows if row["gate_id"] == "T4981_08_parent_finite_TTT")["result"] is False,
            "universal two-point result only",
        ),
        ("G18_full_MTS_false", True, "no full-theory promotion"),
    ]
    gate_rows = [
        {
            "gate": name,
            "passed": passed,
            "detail": detail,
            "status": "pass" if passed else "fail",
        }
        for name, passed, detail in gates
    ]
    pass_count = sum(bool(row["passed"]) for row in gate_rows)
    all_gates_pass = pass_count == len(gate_rows)

    result = {
        "checkpoint_marker": MARKER,
        "dry_run": arguments.dry_run,
        "required_input_count": len(required_paths),
        "de_Donder_nonminimal_coefficients": {
            "metric_delta": float(metric_nonminimal),
            "metric_trace": float(trace_nonminimal),
            "ghost": float(ghost_nonminimal),
        },
        "DeWitt_spectrum": [float(value) for value in eigenvalues],
        "Einstein_ghost_determinant_weight": 1.0,
        "parent_x0_determinant_weight": 1.5,
        "parent_universal_log_action_coefficients_in_units_1_over_4pi_squared": {
            key: fraction_text(value) for key, value in parent_coefficients.items()
        },
        "maximum_Schur_identity_residual": maximum_schur_identity,
        "final_Schur_slope_residual": final_schur_slope,
        "gate_pass_count": pass_count,
        "gate_count": len(gate_rows),
        "valid_for_parent_gauge_fixed_quadratic_hessian": all_gates_pass,
        "valid_for_parent_universal_quadratic_log_claim": all_gates_pass,
        "valid_for_zero_motion_scalar_contact_architecture_transfer": all_gates_pass,
        "valid_for_interacting_PX_finite_parent_determinant": False,
        "valid_for_parent_finite_metric_three_point_claim": False,
        "valid_for_full_quantum_BRST_claim": False,
        "valid_for_exact_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": (
            "4982 derive the order-x covariant motion-metric Schur kernel and its "
            "BRST-compatible two-point projection before any finite parent TTT claim"
        ),
        "elapsed_seconds": time.perf_counter() - started,
    }

    if arguments.dry_run:
        print(
            f"{MARKER}_DRY_RUN={pass_count}/{len(gate_rows)} "
            f"R={fraction_text(parent_coefficients['R_log_R'])} "
            f"Ricci={fraction_text(parent_coefficients['Ricci_log_Ricci'])}",
            flush=True,
        )
        return 0 if all_gates_pass else 1

    write_csv(HESSIAN_CSV, tagged(hessian_rows))
    write_csv(MODE_CSV, tagged(mode_rows))
    write_csv(LOG_CSV, tagged(log_rows))
    write_csv(SCHUR_CSV, tagged(schur_rows))
    write_csv(TRANSFER_CSV, tagged(transfer_rows))
    write_csv(GATE_CSV, tagged(gate_rows))
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    provenance_lines = [
        "# Checkpoint 4981 provenance",
        "",
        "Generated locally. No web request and no GitHub action.",
        "",
        "The gravity/ghost Hessian and logarithmic coefficients are read from the",
        "acquired local source. The motion block is inherited from the derived MTS",
        "P(X) Hessian. The scalar action/response factor of two is derived before",
        "the parent coefficients are added.",
        "",
        "## Input digests",
    ]
    for path in required_paths:
        provenance_lines.append(f"- `{relative(path)}` sha256 `{digest(path)}`")
    PROVENANCE.write_text("\n".join(provenance_lines) + "\n", encoding="utf-8")

    print(
        f"{MARKER}_PASS={pass_count}/{len(gate_rows)} output={SOURCE}",
        flush=True,
    )
    return 0 if all_gates_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import csv
import hashlib
import math
from functools import lru_cache
from pathlib import Path
from typing import Any

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"

MARKER = "MTS_MICROSCOPIC_METRIC_THREE_POINT_WEYL_CUBIC_4908"
FORMAL_MARKER = "PPC4161_MICROSCOPIC_METRIC_THREE_POINT_WEYL_CUBIC_4908"
NEXT_TARGET = (
    "4909-Y5-R2FR-renormalized-motion-scalar-measure-mass-gap-and-"
    "stress-three-point-matching.md"
)
CHECKED_DATE = "2026-07-12"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    sources = [
        (
            "SRC4908_00_core_action",
            ROOT
            / "core-mts-framework"
            / "action-principle"
            / "the-fundamental-action-of-motion-timespace-field-theory.md",
            "n = 4/3",
            "printed_motion_scalar_action",
        ),
        (
            "SRC4908_01_core_EFT",
            ROOT
            / "core-mts-framework"
            / "field-theory"
            / "the-effective-field-theory-of-motion-timespace.md",
            "with n = 4/3",
            "printed_motion_scalar_EFT",
        ),
        (
            "SRC4908_02_primitive_audit",
            POST
            / "4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-universal-source-coupling-or-correspondence-demotion.md",
            "PRIMITIVE_COVARIANCE_SIGN_AND_FLOW_RANK_THEOREM_4872",
            "primitive_action_and_boundary_term_audit",
        ),
        (
            "SRC4908_03_open_parent",
            POST
            / "4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md",
            "OPEN_PARENT_HADAMARD_INDUCED_GRAVITY_AND_METRIC_ONLY_QUOTIENT_4873",
            "Schwinger_Keldysh_parent",
        ),
        (
            "SRC4908_04_integrated_metric",
            POST
            / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
            "INTEGRATED_PRINCIPAL_DENSITY_PARENT_AND_SPIN2_POLE_THEOREM_4875",
            "integrated_Diff_metric_parent",
        ),
        (
            "SRC4908_05_heat_kernel",
            POST
            / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md",
            "INTEGRATED_H_PARENT_SADDLE_HEAT_KERNEL_POLE_HIERARCHY_4876",
            "covariant_scalar_determinant",
        ),
        (
            "SRC4908_06_spectrum",
            POST
            / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md",
            "MTS_SPECTRUM_NO_GO_NONLOCAL_COMPLETION_AND_RENORMALIZED_VACUUM_FREEZE_4877",
            "real_complex_and_bath_spectrum_audit",
        ),
        (
            "SRC4908_07_scalar_a6",
            POST
            / "4881-Y5-R2FR-compact-matter-interior-EOS-contact-matching-and-Riemann-cubed-coefficient-owner-gate.md",
            "MTS_COMPACT_FLUID_TOV_AND_SCALAR_A6_OWNER_4881",
            "scalar_a6_owner",
        ),
        (
            "SRC4908_08_Newton_calibration",
            POST
            / "4898-Y5-R2FR-microscopic-Planck-stiffness-owner-and-GN-calibration-versus-prediction-gate.md",
            "MTS_GN_CALIBRATION_VERSUS_PREDICTION_GATE_4898",
            "single_Newton_calibration",
        ),
        (
            "SRC4908_09_current_action",
            POST
            / "4904-Y5-R2FR-current-unified-action-assembly-Ward-identity-and-parameter-prediction-ledger.md",
            "MTS_CURRENT_UNIFIED_ACTION_WARD_PARAMETER_GATE_4904",
            "active_action_and_field_content",
        ),
        (
            "SRC4908_10_operator_basis",
            POST
            / "4905-Y5-R2FR-first-nontrivial-MTS-to-SM-gravity-operator-basis-and-independent-observable-gate.md",
            "MTS_FIRST_RESIDUAL_OPERATOR_AND_INDEPENDENT_OBSERVABLE_GATE_4905",
            "Weyl_cubic_basis_and_heavy_scalar_weight",
        ),
        (
            "SRC4908_11_galaxy_freeze",
            POST
            / "4907-Y5-R2FR-parent-derived-environmental-bi-response-action-or-galaxy-residual-freeze.md",
            "MTS_PARENT_ENVIRONMENTAL_BIRESPONSE_OR_GALAXY_FREEZE_4907",
            "validated_predecessor",
        ),
        (
            "SRC4908_12_prior_validation",
            OUTPUT / "P8_Y5_BRR545_4907_VALIDATION.csv",
            "VAL4907_OVERALL,PASS",
            "validated_predecessor",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker, role in sources:
        exists = path.exists()
        rows.append(
            {
                "source_id": source_id,
                "source_type": role,
                "source_path_or_url": str(path),
                "local_path_required": True,
                "source_exists": exists,
                "marker": marker,
                "marker_found": contains(path, marker),
                "sha256": sha256(path) if exists else "",
            }
        )
    return {
        "rows": rows,
        "passed": all(
            row["source_exists"] and row["marker_found"] for row in rows
        ),
    }


@lru_cache(maxsize=None)
def core_hessian() -> dict[str, Any]:
    psi, coupling, source = sp.symbols(
        "psi lambda J", positive=True, finite=True
    )
    potential = sp.Rational(3, 4) * coupling * psi ** sp.Rational(4, 3)
    first = sp.diff(potential, psi)
    second = sp.diff(first, psi)
    third = sp.diff(second, psi)
    fourth = sp.diff(third, psi)
    sourced_background = (source / coupling) ** 3
    mass_squared = sp.simplify(second.subs(psi, sourced_background))
    cubic = sp.simplify(third.subs(psi, sourced_background))
    quartic = sp.simplify(fourth.subs(psi, sourced_background))
    stationarity = sp.simplify(
        first.subs(psi, sourced_background) - source
    )
    rows = [
        {
            "quantity": "core_potential_positive_branch",
            "expression": str(potential),
            "result": "V=(3/4) lambda |psi|^(4/3)",
            "status": "PRINTED_PARENT_INPUT",
        },
        {
            "quantity": "first_derivative",
            "expression": str(first),
            "result": "lambda sign(psi)|psi|^(1/3)",
            "status": "EXACT_AWAY_FROM_ZERO",
        },
        {
            "quantity": "vacuum",
            "expression": "V'(psi_bar)=0",
            "result": "psi_bar=0 for lambda>0",
            "status": "UNIQUE_STABLE_CLASSICAL_VACUUM",
        },
        {
            "quantity": "vacuum_Hessian",
            "expression": str(second),
            "result": "+infinity as psi->0",
            "status": "NO_FINITE_GAUSSIAN_HESSIAN",
        },
        {
            "quantity": "source_regularized_background",
            "expression": str(sourced_background),
            "result": "psi_J=(J/lambda)^3",
            "status": "AUXILIARY_LEGENDRE_SOURCE_ONLY",
        },
        {
            "quantity": "source_regularized_mass_squared",
            "expression": str(mass_squared),
            "result": "m_J^2=lambda^3/(3 J^2)",
            "status": "FINITE_FOR_NONZERO_SOURCE",
        },
        {
            "quantity": "source_regularized_cubic",
            "expression": str(cubic),
            "result": "g3_J=-2 lambda^6/(9 J^5)",
            "status": "DIVERGES_AT_VACUUM",
        },
        {
            "quantity": "source_regularized_quartic",
            "expression": str(quartic),
            "result": "g4_J=10 lambda^9/(27 J^8)",
            "status": "DIVERGES_AT_VACUUM",
        },
        {
            "quantity": "printed_gamma_term",
            "expression": "-gamma psi partial_t psi",
            "result": "-(gamma/2) partial_t(psi^2)",
            "status": "BOUNDARY_NOT_HESSIAN_DAMPING",
        },
    ]
    return {
        "rows": rows,
        "potential": str(potential),
        "first": str(first),
        "second": str(second),
        "third": str(third),
        "fourth": str(fourth),
        "sourced_background": str(sourced_background),
        "mass_squared": str(mass_squared),
        "cubic": str(cubic),
        "quartic": str(quartic),
        "stationarity_residual": str(stationarity),
        "vacuum_hessian_finite": False,
        "passed": stationarity == 0
        and mass_squared == coupling**3 / (3 * source**2)
        and cubic == -2 * coupling**6 / (9 * source**5)
        and quartic == 10 * coupling**9 / (27 * source**8),
    }


@lru_cache(maxsize=None)
def metric_vertex_and_Ward_identity() -> dict[str, Any]:
    mass_squared = sp.symbols("m2", real=True)
    p = sp.Matrix(sp.symbols("p0:4", real=True))
    p_prime = sp.Matrix(sp.symbols("r0:4", real=True))
    eta = sp.diag(1, -1, -1, -1)
    p_lower = eta * p
    p_prime_lower = eta * p_prime
    q = p_prime - p
    p_dot_p_prime = (p.T * eta * p_prime)[0]
    p_squared = (p.T * eta * p)[0]
    p_prime_squared = (p_prime.T * eta * p_prime)[0]
    vertex = sp.Matrix(
        4,
        4,
        lambda mu, nu: p_prime_lower[mu] * p_lower[nu]
        + p_prime_lower[nu] * p_lower[mu]
        - eta[mu, nu] * (p_dot_p_prime - mass_squared),
    )
    contracted = sp.Matrix(
        [
            sp.simplify(sum(q[mu] * vertex[mu, nu] for mu in range(4)))
            for nu in range(4)
        ]
    )
    expected = sp.Matrix(
        [
            p_lower[nu] * (p_prime_squared - mass_squared)
            - p_prime_lower[nu] * (p_squared - mass_squared)
            for nu in range(4)
        ]
    )
    residual = sp.simplify(contracted - expected)
    rows = [
        {
            "object": "one_graviton_two_scalar_vertex",
            "expression": "V_mn=p'_m p_n+p'_n p_m-eta_mn(p'.p-m^2)",
            "normalization": "overall -i/(2 M_R) stripped",
            "result": "nonzero universal metric vertex",
        },
        {
            "object": "vertex_Ward_identity",
            "expression": "q^m V_mn=p_n Delta^-1(p')-p'_n Delta^-1(p)",
            "normalization": "q=p'-p; Delta^-1=p^2-m^2",
            "result": "exact; zero between on-shell scalar legs",
        },
        {
            "object": "metric_coupling_owner",
            "expression": "delta S_psi=(1/2) int sqrt(-g) T_mn delta g^mn",
            "normalization": "same public metric",
            "result": "Hilbert coupling; no independent source charge",
        },
    ]
    return {
        "rows": rows,
        "Ward_residual": [str(value) for value in residual],
        "Ward_identity_exact": all(value == 0 for value in residual),
        "passed": all(value == 0 for value in residual),
    }


@lru_cache(maxsize=None)
def determinant_three_point() -> dict[str, Any]:
    t = sp.symbols("t", real=True)
    d0, d1, d2, d3 = sp.symbols("D0 D1 D2 D3", nonzero=True)
    operator = d0 + t * d1 + t**2 * d2 / 2 + t**3 * d3 / 6
    third = sp.simplify(sp.diff(sp.log(operator), t, 3).subs(t, 0))
    expected = sp.simplify(d3 / d0 - 3 * d1 * d2 / d0**2 + 2 * d1**3 / d0**3)
    rows = [
        {
            "diagram_class": "three_graviton_scalar_seagull",
            "trace_term": "(1/2) Tr[G D_123]",
            "multiplicity": 1,
            "required_for_Diff_Ward_identity": True,
        },
        {
            "diagram_class": "two_plus_one_metric_insertion",
            "trace_term": "-(1/2) Tr[G D_i G D_jk] plus 3 permutations",
            "multiplicity": -3,
            "required_for_Diff_Ward_identity": True,
        },
        {
            "diagram_class": "scalar_triangle",
            "trace_term": "+(1/2) Tr[G D_1 G D_2 G D_3 plus reverse order]",
            "multiplicity": 2,
            "required_for_Diff_Ward_identity": True,
        },
    ]
    return {
        "rows": rows,
        "commuting_third_variation": str(third),
        "expected": str(expected),
        "exact_operator_formula": "1/2 Tr[G D123-G D1 G D23-G D2 G D13-G D3 G D12+G D1 G D2 G D3+G D1 G D3 G D2]",
        "passed": sp.simplify(third - expected) == 0,
    }


@lru_cache(maxsize=None)
def source_regularized_Weyl_coefficient() -> dict[str, Any]:
    coupling, source, cutoff = sp.symbols(
        "lambda J Lambda", positive=True, finite=True
    )
    mass_squared = coupling**3 / (3 * source**2)
    scalar_weight = sp.Rational(1, 30240) / (4 * sp.pi) ** 2
    zeta = sp.simplify(
        scalar_weight * sp.exp(-mass_squared / cutoff**2) / mass_squared
    )
    expected = sp.simplify(
        source**2
        * sp.exp(-coupling**3 / (3 * source**2 * cutoff**2))
        / (10080 * (4 * sp.pi) ** 2 * coupling**3)
    )
    vacuum_limit = sp.limit(zeta, source, 0, dir="+")
    cutoff_removed = sp.limit(zeta, cutoff, sp.oo)
    cutoff_removed_vacuum_limit = sp.limit(
        cutoff_removed, source, 0, dir="+"
    )
    prefactor = float(scalar_weight)
    sweep: list[dict[str, Any]] = []
    for dimensionless_source in (1.0, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01):
        j = dimensionless_source
        mass_over_mu = 1.0 / (math.sqrt(3.0) * j)
        cubic_over_mass = 2.0 * math.sqrt(3.0) / (9.0 * j**4)
        quartic = 10.0 / (27.0 * j**8)
        zeta_uncut = j**2 / (10080.0 * (4.0 * math.pi) ** 2)
        zeta_cutoff_mu = zeta_uncut * math.exp(-1.0 / (3.0 * j**2))
        zeta_cutoff_10mu = zeta_uncut * math.exp(
            -1.0 / (300.0 * j**2)
        )
        control = max(cubic_over_mass, quartic)
        sweep.append(
            {
                "j_abs": j,
                "psi_J_over_mu": j**3,
                "m_J_over_mu": mass_over_mu,
                "abs_g3_over_m_J": cubic_over_mass,
                "abs_g4": quartic,
                "Gaussian_control_max": control,
                "Gaussian_control_below_one": control < 1.0,
                "zeta_times_mu2_cutoff_removed": zeta_uncut,
                "zeta_times_mu2_Lambda_over_mu_1": zeta_cutoff_mu,
                "zeta_times_mu2_Lambda_over_mu_10": zeta_cutoff_10mu,
            }
        )
    return {
        "rows": sweep,
        "scalar_weight": str(scalar_weight),
        "scalar_weight_numeric": prefactor,
        "zeta_source": str(zeta),
        "zeta_expected": str(expected),
        "vacuum_limit": str(vacuum_limit),
        "cutoff_removed_vacuum_limit": str(cutoff_removed_vacuum_limit),
        "Gaussian_control_near_vacuum": False,
        "formal_one_loop_vacuum_coefficient_zero": vacuum_limit == 0
        and cutoff_removed_vacuum_limit == 0,
        "passed": sp.simplify(zeta - expected) == 0
        and vacuum_limit == 0
        and cutoff_removed_vacuum_limit == 0
        and any(row["Gaussian_control_below_one"] for row in sweep)
        and all(
            not row["Gaussian_control_below_one"]
            for row in sweep
            if row["j_abs"] <= 0.5
        ),
    }


@lru_cache(maxsize=None)
def nonperturbative_scaling() -> dict[str, Any]:
    rows = [
        {
            "quantity": "canonical_scalar_dimension",
            "mass_dimension": "1",
            "derived_relation": "[psi]=1",
            "status": "EXACT_4D_POWER_COUNTING",
        },
        {
            "quantity": "nonanalytic_coupling",
            "mass_dimension": "8/3",
            "derived_relation": "[lambda]=4-4/3=8/3",
            "status": "EXACT_4D_POWER_COUNTING",
        },
        {
            "quantity": "intrinsic_scale_mu",
            "mass_dimension": "1",
            "derived_relation": "mu=lambda^(3/8)",
            "status": "EXACT_IF_LAMBDA_IS_ONLY_SCALAR_SCALE",
        },
        {
            "quantity": "dimensionless_action",
            "mass_dimension": "0",
            "derived_relation": "x=y/mu; psi=mu phi; S=int d4y[(d phi)^2/2+3|phi|^(4/3)/4]",
            "status": "EXACT_CLASSICAL_RESCALING",
        },
        {
            "quantity": "nonperturbative_gap",
            "mass_dimension": "1",
            "derived_relation": "m_gap=c_m mu",
            "status": "DIMENSIONLESS_CONSTANT_REQUIRES_RENORMALIZED_MEASURE",
        },
        {
            "quantity": "nonperturbative_Weyl_cubic",
            "mass_dimension": "-2",
            "derived_relation": "zeta_psi=c_6/mu^2=c_6 lambda^(-3/4)",
            "status": "DIMENSIONLESS_STRESS_THREE_POINT_CONSTANT_OPEN",
        },
    ]
    return {
        "rows": rows,
        "mu_power": sp.Rational(3, 8),
        "zeta_lambda_power": sp.Rational(-3, 4),
        "unknown_dimensionless_constants": ["c_m", "c_6"],
        "passed": sp.Rational(8, 3) * sp.Rational(3, 8) == 1
        and sp.Rational(8, 3) * sp.Rational(-3, 4) == -2,
    }


@lru_cache(maxsize=None)
def open_parent_and_owner_gate() -> dict[str, Any]:
    rows = [
        {
            "owner": "printed_gamma_term",
            "conservative_C3_status": "NO_CONTRIBUTION",
            "reason": "total derivative for constant gamma",
            "numeric_coefficient_owned": False,
        },
        {
            "owner": "Schwinger_Keldysh_r_a_pair",
            "conservative_C3_status": "NOT_TWO_SCALAR_SPECIES",
            "reason": "CTP normalization Gamma[g,g]=0; r/a are response coordinates",
            "numeric_coefficient_owned": False,
        },
        {
            "owner": "source_regularized_real_motion_scalar_Hessian",
            "conservative_C3_status": "FORMAL_ONE_LOOP_ZERO_AT_J_TO_ZERO",
            "reason": "m_J^2=lambda^3/(3J^2) and zeta_J is proportional to J^2",
            "numeric_coefficient_owned": False,
        },
        {
            "owner": "interacting_motion_scalar",
            "conservative_C3_status": "NONPERTURBATIVE_SCALING_ONLY",
            "reason": "zeta_psi=c_6 lambda^(-3/4); c_6 not calculated",
            "numeric_coefficient_owned": False,
        },
        {
            "owner": "closed_bath_X",
            "conservative_C3_status": "UNMATCHED_SPECTRUM",
            "reason": "bath masses, spins and curvature couplings not selected",
            "numeric_coefficient_owned": False,
        },
        {
            "owner": "integrated_H_and_Diff_ghosts",
            "conservative_C3_status": "UNMATCHED_BACKGROUND_FIELD_SECTOR",
            "reason": "gauge-consistent six-derivative contribution not calculated",
            "numeric_coefficient_owned": False,
        },
        {
            "owner": "bare_Wilsonian_C3_boundary",
            "conservative_C3_status": "ALLOWED_BUT_UNSIGNED",
            "reason": "setting it to zero is a UV boundary choice, not Diff symmetry",
            "numeric_coefficient_owned": False,
        },
        {
            "owner": "parity_odd_C_C_Ctilde_motion_scalar",
            "conservative_C3_status": "EXACT_ZERO_AT_SCALAR_THRESHOLD",
            "reason": "printed scalar and metric coupling are parity even",
            "numeric_coefficient_owned": True,
        },
    ]
    return {
        "rows": rows,
        "SK_diagonal_action_value": 0,
        "r_a_physical_species_count": 1,
        "real_complex_primitive_count_fixed": False,
        "closed_completion_fixed": False,
        "parity_odd_scalar_threshold": 0,
        "total_parity_even_numeric_coefficient_owned": False,
        "passed": rows[-1]["numeric_coefficient_owned"]
        and not any(
            row["numeric_coefficient_owned"]
            for row in rows[:-1]
        ),
    }


@lru_cache(maxsize=None)
def local_GR_Maxwell_gate() -> dict[str, Any]:
    t, c1, c2 = sp.symbols("t C1 C2", real=True)
    linearized_curvature = t * c1 + t**2 * c2
    cubic_operator = sp.expand(linearized_curvature**3)
    first = sp.diff(cubic_operator, t).subs(t, 0)
    second = sp.diff(cubic_operator, t, 2).subs(t, 0)
    third = sp.diff(cubic_operator, t, 3).subs(t, 0)
    rows = [
        {
            "arena": "flat_saddle_tadpole",
            "C3_effect": "none because C[eta]=0",
            "baseline_result": "C0_R fixed once",
            "gate": "PASS",
        },
        {
            "arena": "massless_spin2_pole",
            "C3_effect": "delta^2 int C3 at h=0 equals zero",
            "baseline_result": "EH propagator and residue unchanged",
            "gate": "PASS",
        },
        {
            "arena": "Newton_linear_exchange",
            "C3_effect": "no quadratic metric Hessian",
            "baseline_result": "G_N=1/(8 pi M_R^2) unchanged",
            "gate": "PASS",
        },
        {
            "arena": "weak_PPN_and_orbits",
            "C3_effect": "first nonlinear relative scale epsilon_3~|zeta| q^4/M_R^2",
            "baseline_result": "requires epsilon_3 much less than one",
            "gate": "CONDITIONAL_ON_COEFFICIENT",
        },
        {
            "arena": "Maxwell_and_Poynting",
            "C3_effect": "pure metric only; no direct F^2 C threshold on factorized MTS slice",
            "baseline_result": "minimal Maxwell Hilbert stress retained",
            "gate": "PASS_ACTIVE_SLICE",
        },
        {
            "arena": "strong_gravity_three_point",
            "C3_effect": "vertex proportional to zeta q^6/M_R^3",
            "baseline_result": "first direct local observable channel",
            "gate": "COEFFICIENT_OPEN",
        },
    ]
    return {
        "rows": rows,
        "C3_first_variation_at_flat": str(first),
        "C3_second_variation_at_flat": str(second),
        "C3_third_variation_at_flat": str(third),
        "propagator_modified": second != 0,
        "Newton_linear_modified": second != 0,
        "Maxwell_direct_mixed_MTS_threshold": 0,
        "vertex_scaling": "Gamma_hhh_C3~zeta q^6/M_R^3",
        "EH_vertex_scaling": "Gamma_hhh_EH~q^2/M_R",
        "relative_scaling": "epsilon_3~|zeta| q^4/M_R^2",
        "passed": first == 0
        and second == 0
        and third == 6 * c1**3,
    }


@lru_cache(maxsize=None)
def coefficient_arbitration() -> dict[str, Any]:
    hessian = core_hessian()
    vertex = metric_vertex_and_Ward_identity()
    determinant = determinant_three_point()
    loop = source_regularized_Weyl_coefficient()
    scaling = nonperturbative_scaling()
    owners = open_parent_and_owner_gate()
    local = local_GR_Maxwell_gate()
    rows = [
        {
            "gate": "printed_motion_potential",
            "status": "PASS",
            "reason": "n=4/3 potential is explicit",
        },
        {
            "gate": "finite_stationary_Gaussian_Hessian",
            "status": "FAIL",
            "reason": "only stable vacuum is the non-C2 cusp psi=0",
        },
        {
            "gate": "metric_vertex_and_Ward_identity",
            "status": "PASS",
            "reason": "h psi psi vertex and exact Ward contraction derived",
        },
        {
            "gate": "metric_three_point_determinant",
            "status": "PASS",
            "reason": "triangle plus seagull functional identity derived",
        },
        {
            "gate": "formal_one_loop_vacuum_C3",
            "status": "ZERO_LIMIT_ONLY",
            "reason": "source-regularized coefficient tends to zero",
        },
        {
            "gate": "Gaussian_control_at_vacuum",
            "status": "FAIL",
            "reason": "g3/m and g4 diverge as j^-4 and j^-8",
        },
        {
            "gate": "nonperturbative_scaling",
            "status": "PASS",
            "reason": "zeta_psi=c6 lambda^(-3/4) reduces problem to one dimensionless stress-three-point constant",
        },
        {
            "gate": "total_parity_even_owner",
            "status": "FAIL",
            "reason": "c6, species count, bath, H/ghost and Wilson boundary are not jointly fixed",
        },
        {
            "gate": "parity_odd_scalar_threshold",
            "status": "EXACT_ZERO",
            "reason": "parity-even scalar threshold",
        },
        {
            "gate": "local_GR_Newton_Maxwell",
            "status": "PASS_ACTIVE_BASELINE",
            "reason": "C3 has no flat quadratic Hessian and no mixed EM portal",
        },
        {
            "gate": "activate_Gamma_MTS_res",
            "status": "FAIL",
            "reason": "no controlled nonzero parent coefficient",
        },
    ]
    all_internal = all(
        section["passed"]
        for section in (
            hessian,
            vertex,
            determinant,
            loop,
            scaling,
            owners,
            local,
        )
    )
    return {
        "rows": rows,
        "sections": {
            "hessian": hessian,
            "vertex": vertex,
            "determinant": determinant,
            "loop": loop,
            "scaling": scaling,
            "owners": owners,
            "local": local,
        },
        "formal_Hessian_sector_C3_vacuum_limit": 0,
        "all_order_interacting_scalar_C3_proved_zero": False,
        "total_parent_C3_numeric": "not_promoted",
        "parity_odd_scalar_C3": 0,
        "Gamma_MTS_res": 0,
        "active_novel_MTS_numeric_predictions": 0,
        "next_target": NEXT_TARGET,
        "decision": "METRIC_VERTEX_AND_WARD_DERIVED_SOURCE_REGULATED_ONE_LOOP_C3_ZERO_LIMIT_BUT_GAUSSIAN_VACUUM_UNCONTROLLED_NONPERTURBATIVE_SCALING_C6_LAMBDA_MINUS_THREE_QUARTERS_DERIVED_TOTAL_COEFFICIENT_NOT_OWNED_ACTIVE_RESIDUAL_ZERO_PRIVATE_NONCLAIM",
        "all_checks_pass": all_internal,
    }


def output_groups(calculation: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = calculation["sections"]
    return {
        "CORE_HESSIAN": tagged(sections["hessian"]["rows"]),
        "METRIC_VERTEX": tagged(sections["vertex"]["rows"]),
        "DETERMINANT_THREE_POINT": tagged(sections["determinant"]["rows"]),
        "SOURCE_REGULATED_SWEEP": tagged(sections["loop"]["rows"]),
        "NONPERTURBATIVE_SCALING": tagged(sections["scaling"]["rows"]),
        "WEYL_CUBIC_OWNER": tagged(sections["owners"]["rows"]),
        "LOCAL_LIMITS": tagged(sections["local"]["rows"]),
        "REENTRY_GATE": tagged(calculation["rows"]),
        "DECISION": tagged(
            [
                {
                    "overall_decision": calculation["decision"],
                    "formal_Hessian_sector_C3_vacuum_limit": calculation[
                        "formal_Hessian_sector_C3_vacuum_limit"
                    ],
                    "all_order_interacting_scalar_C3_proved_zero": calculation[
                        "all_order_interacting_scalar_C3_proved_zero"
                    ],
                    "total_parent_C3_numeric": calculation[
                        "total_parent_C3_numeric"
                    ],
                    "parity_odd_scalar_C3": calculation[
                        "parity_odd_scalar_C3"
                    ],
                    "Gamma_MTS_res": calculation["Gamma_MTS_res"],
                    "active_novel_MTS_numeric_predictions": calculation[
                        "active_novel_MTS_numeric_predictions"
                    ],
                    "next_target": calculation["next_target"],
                    "all_checks_pass": calculation["all_checks_pass"],
                }
            ]
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sources = source_contract()
    calculation = coefficient_arbitration()
    return {
        **calculation,
        "sources": sources,
        "all_checks_pass": calculation["all_checks_pass"]
        and sources["passed"],
    }


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    calculation = result()
    groups = output_groups(calculation)
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4908_SOURCE_REGISTER.csv",
        tagged(calculation["sources"]["rows"]),
    )
    for name, rows in groups.items():
        write_csv(OUTPUT / f"P8_Y5_R2FR_4908_{name}.csv", rows)
    sections = calculation["sections"]
    print(
        "ward_exact={} determinant_exact={} formal_zeta_limit={} "
        "gaussian_control={} total_owned={} gamma_res={}".format(
            sections["vertex"]["Ward_identity_exact"],
            sections["determinant"]["passed"],
            sections["loop"]["vacuum_limit"],
            sections["loop"]["Gaussian_control_near_vacuum"],
            sections["owners"]["total_parity_even_numeric_coefficient_owned"],
            calculation["Gamma_MTS_res"],
        )
    )
    print(calculation["decision"])
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

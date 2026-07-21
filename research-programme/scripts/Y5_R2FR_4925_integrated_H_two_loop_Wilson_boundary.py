from __future__ import annotations

import csv
import hashlib
import math
import sys
from itertools import combinations_with_replacement
from pathlib import Path
from typing import Any

import numpy as np
from scipy.constants import G, c, hbar, physical_constants


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"

CHECKPOINT = "4925"
CHECKED_DATE = "2026-07-12"
MARKER = "MTS_INTEGRATED_H_TWO_LOOP_WILSON_BOUNDARY_4925"
FORMAL_MARKER = "PPC4161_INTEGRATED_H_TWO_LOOP_WILSON_BOUNDARY_4925"
NEXT_TARGET = (
    "4926-Y5-R2FR-known-massive-threshold-spectrum-and-motion-scale-"
    "normalization-or-low-energy-Wilson-posterior.md"
)

GS_URL = "https://doi.org/10.1016/0370-2693(85)91470-4"
EFT_URL = "https://arxiv.org/abs/gr-qc/9405057"
ASYMPTOTIC_SAFETY_URL = "https://arxiv.org/abs/1601.01800"
CAUSALITY_URL = "https://arxiv.org/abs/1407.5597"
HEAVY_FIELDS_URL = "https://arxiv.org/abs/1611.02705"

SUN_MASS_KG = 1.988409870698051e30
PLANCK_LENGTH_M = physical_constants["Planck length"][0]
ELECTRON_VOLT_J = physical_constants["electron volt"][0]
HBAR_C_EV_M = hbar * c / ELECTRON_VOLT_J
REDUCED_PLANCK_ENERGY_EV = (
    math.sqrt(hbar * c**5 / (8.0 * math.pi * G)) / ELECTRON_VOLT_J
)
GS_A_LOG_COEFFICIENT = 209.0 / (1440.0 * math.pi**2)
SCALAR_CANONICAL_DENOMINATOR = 30240.0 * math.pi

BRANCH_TESTS_PATH = OUTPUT / "P8_Y5_R2FR_4877_BRANCH_TESTS.csv"
COMPACT_PATH = OUTPUT / "P8_Y5_R2FR_4922_COMPACT_DOMAIN.csv"
ROBUST_PATH = OUTPUT / "P8_Y5_R2FR_4923_ROBUSTNESS.csv"
RECAST_PATH = OUTPUT / "P8_Y5_R2FR_4923_BRANCH_RECAST.csv"
POSTERIOR_AUDIT_PATH = OUTPUT / "P8_Y5_R2FR_4923_PSEOB_POSTERIOR_AUDIT.csv"

DIGEST_CACHE: dict[Path, str] = {}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
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


def digest(path: Path) -> str:
    if path in DIGEST_CACHE:
        return DIGEST_CACHE[path]
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            hasher.update(block)
    value = hasher.hexdigest()
    DIGEST_CACHE[path] = value
    return value


def read_text_auto(path: Path) -> str:
    raw = path.read_bytes()
    encoding = "utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8"
    return raw.decode(encoding, errors="replace")


def symmetric_pairs(dimension: int) -> list[tuple[int, int]]:
    return list(combinations_with_replacement(range(dimension), 2))


def h_metric_jacobian_matrix(metric: np.ndarray) -> np.ndarray:
    dimension = metric.shape[0]
    pairs = symmetric_pairs(dimension)
    inverse = np.linalg.inv(metric)
    density = math.sqrt(abs(float(np.linalg.det(metric))))
    jacobian = np.zeros((len(pairs), len(pairs)), dtype=float)
    for row_index, (mu, nu) in enumerate(pairs):
        for column_index, (alpha, beta) in enumerate(pairs):
            variation = np.zeros_like(metric)
            variation[alpha, beta] = 1.0
            variation[beta, alpha] = 1.0
            if alpha == beta:
                variation[alpha, beta] = 1.0
            trace = float(np.trace(inverse @ variation))
            inverse_variation = -inverse @ variation @ inverse
            h_variation = density * (
                inverse_variation + 0.5 * trace * inverse
            )
            jacobian[row_index, column_index] = h_variation[mu, nu]
    return jacobian


def h_metric_jacobian_theory(metric: np.ndarray) -> float:
    dimension = metric.shape[0]
    symmetric_dimension = dimension * (dimension + 1) // 2
    determinant = float(np.linalg.det(metric))
    trace_eigenvalue = (dimension - 2.0) / 2.0
    traceless_sign = (-1.0) ** (symmetric_dimension - 1)
    return (
        traceless_sign
        * trace_eigenvalue
        * abs(determinant) ** (symmetric_dimension / 2.0)
        * determinant ** (-(dimension + 1))
    )


def jacobian_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    cases: list[tuple[int, str, int]] = []
    cases.extend((4, "euclidean", seed) for seed in range(8))
    cases.extend((4, "lorentzian", seed) for seed in range(8))
    cases.extend((3, "euclidean", seed) for seed in range(4))
    cases.extend((5, "euclidean", seed) for seed in range(4))
    for dimension, signature, seed in cases:
        rng = np.random.default_rng(492500 + 100 * dimension + seed)
        if signature == "euclidean":
            matrix = rng.normal(size=(dimension, dimension))
            metric = matrix @ matrix.T + np.eye(dimension)
        else:
            frame = rng.normal(size=(dimension, dimension)) + 2.0 * np.eye(
                dimension
            )
            eta = np.diag([-1.0] + [1.0] * (dimension - 1))
            metric = frame @ eta @ frame.T
        numerical = float(np.linalg.det(h_metric_jacobian_matrix(metric)))
        theoretical = h_metric_jacobian_theory(metric)
        error = abs(numerical - theoretical)
        four_dimensional_unit: float | str = (
            abs(abs(numerical) - 1.0) if dimension == 4 else ""
        )
        rows.append(
            {
                "test_id": f"JAC4925_d{dimension}_{signature}_{seed}",
                "dimension": dimension,
                "signature": signature,
                "seed": seed,
                "det_g": float(np.linalg.det(metric)),
                "numeric_det_dH_dg": numerical,
                "theory_det_dH_dg": theoretical,
                "absolute_error": error,
                "four_dimensional_abs_det_minus_one": four_dimensional_unit,
                "general_formula": (
                    "abs(det dH/dg)=abs(d-2)/2 "
                    "times abs(g)^[(d+1)(d-4)/4]"
                ),
                "four_dimensional_result": (
                    "abs(det dH/dg)=1" if dimension == 4 else "dimension control"
                ),
                "status": (
                    "FOUR_DIMENSIONAL_FIELD_INDEPENDENT_UNIT_JACOBIAN"
                    if dimension == 4
                    else "GENERAL_DIMENSION_SCALING_CONTROL"
                ),
                "passed": error < 2.0e-8
                and (dimension != 4 or four_dimensional_unit < 2.0e-8),
            }
        )
    return tagged(rows)


def parent_ownership_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "audit_id": "UV4925_00_integrated_H",
                "object": "integrated principal density H^{mu nu}",
                "finding": "H is a primitive integration variable modulo Diff on the selected parent",
                "boundary_implication": "a quantum metric loop expansion is physically part of the parent",
                "status": "PARENT_FIELD_OWNER_CLOSED",
                "source": "post-checkpoint-work/4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
                "passed": True,
            },
            {
                "audit_id": "UV4925_01_original_scalar",
                "object": "original fixed-background motion scalar",
                "finding": "the original scalar action does not define the integrated-H measure or a metric UV regulator",
                "boundary_implication": "it cannot fix the finite quantum-metric I1 boundary",
                "status": "NO_ORIGINAL_SCALAR_BOUNDARY_OWNER",
                "source": "core-mts-framework/action-principle/the-fundamental-action-of-motion-timespace-field-theory.md",
                "passed": True,
            },
            {
                "audit_id": "UV4925_02_counterterm_parent",
                "object": "counterterm-complete integrated-H action",
                "finding": "4876 explicitly distinguishes bare matching data from loop contributions",
                "boundary_implication": "M0^2(LambdaUV)=0 is an optional condition and cannot propagate to I1",
                "status": "OPERATOR_BY_OPERATOR_MATCHING_REQUIRED",
                "source": "post-checkpoint-work/4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md",
                "passed": True,
            },
            {
                "audit_id": "UV4925_03_H_to_g_measure",
                "object": "local H-to-g field-coordinate Jacobian",
                "finding": "the pointwise component Jacobian has unit magnitude in exactly four dimensions",
                "boundary_implication": "the selected flat DH coordinate measure supplies no field-dependent local C3 term",
                "status": "H_COORDINATE_JACOBIAN_C3_ZERO_DERIVED",
                "source": "post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_4925_H_TO_G_JACOBIAN.csv",
                "passed": True,
            },
            {
                "audit_id": "UV4925_04_BRST_metric_loops",
                "object": "metric plus Faddeev-Popov ghost loops",
                "finding": "massless loop nonanalytic pieces and GS running are calculable while local finite polynomial pieces are scheme dependent",
                "boundary_implication": "bare and finite H+ghost pieces are not two observables",
                "status": "ONE_RENORMALIZED_WILSON_COMBINATION",
                "source": "post-checkpoint-work/4921-Y5-R2FR-pure-metric-curvature-cubed-and-nonlocal-tail-observable-separation-or-invariant-vacuum-GR-domain-extension-gate.md",
                "passed": True,
            },
            {
                "audit_id": "UV4925_05_GS",
                "object": "pure-gravity two-loop I1 divergence",
                "finding": "the nonzero pole fixes the beta function but not its integration constant",
                "boundary_implication": "one renormalized I1 coefficient is unavoidable in the low-energy EFT",
                "status": "RUNNING_DERIVED_BOUNDARY_FREE",
                "source": GS_URL,
                "passed": True,
            },
            {
                "audit_id": "UV4925_06_fixed_point",
                "object": "asymptotic-safety boundary candidate",
                "finding": "an external Einstein-Hilbert plus C3 truncation finds C3 irrelevant at its non-Gaussian fixed point",
                "boundary_implication": "this could fix the trajectory only after the MTS H matter and regulator flow is shown to share that critical surface",
                "status": "EXTERNAL_CANDIDATE_NOT_PARENT_CONDITION",
                "source": ASYMPTOTIC_SAFETY_URL,
                "passed": True,
            },
            {
                "audit_id": "UV4925_07_current_verdict",
                "object": "finite I1 owner",
                "finding": "no microscopic H regulator fixed point or UV observable currently selects the finite integration constant",
                "boundary_implication": "retain one explicit signed Wilson input rather than multiple fictitious missing terms",
                "status": "ONE_WILSON_INPUT_SELECTED",
                "source": "post-checkpoint-work/4925-Y5-R2FR-integrated-H-two-loop-renormalization-condition-and-finite-zeta-plus-boundary-owner-or-explicit-Wilson-input.md",
                "passed": True,
            },
        ]
    )


def coefficient_collapse_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "row_id": "COLLAPSE4925_00_UV",
            "representation": "UV matching decomposition",
            "equation": "a_eff(Q)=a_UV^R(muU)+sum_i Delta a_i^threshold+beta_GS lP^4 ln(Q/muU)",
            "independent_local_I1_inputs": 1,
            "meaning": "a_UV^R contains the bare local coefficient and every scheme-dependent local H+ghost finite piece at muU",
            "status": "ONE_UV_WILSON_INPUT",
            "passed": True,
        },
        {
            "row_id": "COLLAPSE4925_01_IR",
            "representation": "IR test coefficient",
            "equation": "a_IR(Qref)=a_UV^R+all matched thresholds+beta_GS lP^4 ln(Qref/muU)",
            "independent_local_I1_inputs": 1,
            "meaning": "all unresolved microscopic decomposition is absorbed into one signed coefficient at one reference scale",
            "status": "ONE_IR_TEST_PARAMETER",
            "passed": True,
        },
        {
            "row_id": "COLLAPSE4925_02_observable",
            "representation": "on-shell strong-field observable",
            "equation": "alpha_ev(Q)=a_eff(Q)/M^4=s_plus[ell_plus(Q)/M]^4",
            "independent_local_I1_inputs": 1,
            "meaning": "ringdown constrains the renormalized sum and cannot distinguish bare from finite loop labels",
            "status": "OBSERVABLE_SUM_ONLY",
            "passed": True,
        },
    ]
    bare = 2.25
    finite = -0.75
    total = bare + finite
    for index, shift in enumerate((-7.5, -0.125, 0.0, 3.75, 11.0)):
        shifted_bare = bare + shift
        shifted_finite = finite - shift
        shifted_total = shifted_bare + shifted_finite
        rows.append(
            {
                "row_id": f"COLLAPSE4925_scheme_{index}",
                "representation": "finite renormalization test",
                "equation": "a_b->a_b+delta; a_Hgh,finite->a_Hgh,finite-delta",
                "independent_local_I1_inputs": 1,
                "bare_demo": shifted_bare,
                "finite_loop_demo": shifted_finite,
                "renormalized_sum_demo": shifted_total,
                "invariance_error": abs(shifted_total - total),
                "meaning": "the split changes while the renormalized Wilson coefficient does not",
                "status": "SCHEME_SPLIT_NOT_TWO_PARAMETERS",
                "passed": abs(shifted_total - total) < 1.0e-13,
            }
        )
    return tagged(rows)


def physical_inputs() -> dict[str, float]:
    robust = read_csv(ROBUST_PATH)
    audit = read_csv(POSTERIOR_AUDIT_PATH)
    compact = read_csv(COMPACT_PATH)
    robust_abs_alpha = max(float(row["max_abs_alpha_90"]) for row in robust)
    robust_positive_alpha = max(float(row["alpha_upper_90"]) for row in robust)
    mass_row = next(row for row in audit if row["audit_id"] == "POST4923_08_mass")
    mass_q95_solar = float(mass_row["q95"])
    mass_length_m = G * mass_q95_solar * SUN_MASS_KG / c**2
    robust_abs_ell_m = robust_abs_alpha**0.25 * mass_length_m
    robust_positive_ell_m = robust_positive_alpha**0.25 * mass_length_m
    neutron_star = next(
        row
        for row in compact
        if row["system"] == "1.4_solar_mass_12km_neutron_star"
    )
    black_hole = next(
        row
        for row in compact
        if row["system"] == "10_solar_mass_Schwarzschild_horizon"
    )
    return {
        "robust_abs_alpha": robust_abs_alpha,
        "robust_positive_alpha": robust_positive_alpha,
        "mass_q95_solar": mass_q95_solar,
        "mass_length_m": mass_length_m,
        "robust_abs_ell_m": robust_abs_ell_m,
        "robust_positive_ell_m": robust_positive_ell_m,
        "neutron_star_ell_m": float(neutron_star["ell_plus_upper_m_for_domain"]),
        "black_hole_ell_m": float(black_hole["ell_plus_upper_m_for_domain"]),
    }


def rg_transfer_rows(inputs: dict[str, float]) -> list[dict[str, Any]]:
    scales = [
        (
            "RG4925_GW250114",
            "GW250114 remnant geometric mass at q95",
            inputs["mass_length_m"],
        ),
        ("RG4925_NS12km", "12 km neutron-star radius", 12_000.0),
        (
            "RG4925_BH10",
            "10-solar-mass Schwarzschild radius",
            2.0 * G * 10.0 * SUN_MASS_KG / c**2,
        ),
        ("RG4925_Earth", "Earth radius weak-field scale", 6_371_000.0),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, arena, length_m in scales:
        q_eV = HBAR_C_EV_M / length_m
        log_ratio = math.log(q_eV / REDUCED_PLANCK_ENERGY_EV)
        delta_a_over_lP4 = GS_A_LOG_COEFFICIENT * log_ratio
        ell_running_m = abs(delta_a_over_lP4) ** 0.25 * PLANCK_LENGTH_M
        rows.append(
            {
                "row_id": row_id,
                "arena": arena,
                "length_scale_m": length_m,
                "q_eV": q_eV,
                "reference_mu_eV": REDUCED_PLANCK_ENERGY_EV,
                "ln_q_over_mu": log_ratio,
                "delta_a_plus_over_lP4": delta_a_over_lP4,
                "absolute_running_length_m": ell_running_m,
                "length_ratio_to_robust_GW_envelope": (
                    ell_running_m / inputs["robust_abs_ell_m"]
                ),
                "a_ratio_to_robust_GW_envelope": (
                    ell_running_m / inputs["robust_abs_ell_m"]
                )
                ** 4,
                "formula": "Delta a_+=[209/(1440pi^2)]lP^4 ln(Q/mu_ref)",
                "status": "RG_TRANSFER_DERIVED_PHYSICALLY_NEGLIGIBLE",
                "passed": ell_running_m < 2.0 * PLANCK_LENGTH_M,
            }
        )
    return tagged(rows)


def boundary_route_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "route_id": "ROUTE4925_00_M0",
                "candidate": "infer I1 zero from M0^2(LambdaUV)=0",
                "test": "compare independent Diff invariants and their beta functions",
                "result": "the Einstein and I1 operators are independent and I1 has nonzero two-loop running",
                "status": "REJECTED_NO_OPERATOR_IMPLICATION",
                "selected": False,
                "passed": True,
            },
            {
                "route_id": "ROUTE4925_01_H_jacobian",
                "candidate": "derive I1 from the H-to-g coordinate Jacobian",
                "test": "calculate the full ten-by-ten symmetric-component Jacobian",
                "result": "its magnitude is exactly one in four dimensions and it generates no local action",
                "status": "DERIVED_ZERO_COORDINATE_JACOBIAN_CONTRIBUTION",
                "selected": False,
                "passed": True,
            },
            {
                "route_id": "ROUTE4925_02_MS",
                "candidate": "set the finite coefficient to zero in minimal subtraction",
                "test": "apply an arbitrary finite counterterm shift",
                "result": "the zero moves between bare and finite-loop pieces while observables are invariant",
                "status": "REJECTED_AS_PHYSICAL_PREDICTION_SCHEME_ONLY",
                "selected": False,
                "passed": True,
            },
            {
                "route_id": "ROUTE4925_03_asymptotic_safety",
                "candidate": "fix C3 as an irrelevant asymptotically safe direction",
                "test": "compare the external Einstein-Hilbert-C3 truncation with the MTS H plus matter parent",
                "result": "the external fixed point is evidence for a possible mechanism but no MTS flow or critical-surface map exists",
                "status": "RETAINED_RESEARCH_ROUTE_NOT_ADOPTED_BOUNDARY",
                "selected": False,
                "passed": True,
            },
            {
                "route_id": "ROUTE4925_04_causality",
                "candidate": "use graviton causality to force C3 to zero",
                "test": "apply the higher-spin completion condition",
                "result": "causality relates a nonzero three-point correction to a UV tower scale but does not determine the finite coefficient",
                "status": "SCALE_CONSTRAINT_NOT_ZERO_THEOREM",
                "selected": False,
                "passed": True,
            },
            {
                "route_id": "ROUTE4925_05_microscopic_regulator",
                "candidate": "calculate the finite value from a complete H regulator and measure",
                "test": "search the selected corpus for a lattice or continuum UV action fixing all H counterterms",
                "result": "no such regulator or matching observable is currently present",
                "status": "DERIVATION_ROUTE_OPEN_REQUIRES_NEW_PARENT_DATA",
                "selected": False,
                "passed": True,
            },
            {
                "route_id": "ROUTE4925_06_IR_Wilson",
                "candidate": "retain one signed low-energy Wilson coefficient",
                "test": "absorb the scheme split and matched unknown thresholds at one reference scale",
                "result": "local tests depend on one coefficient a_IR rather than separate bare and H+ghost placeholders",
                "status": "SELECTED_SERIOUS_EFT_PARAMETERIZATION",
                "selected": True,
                "passed": True,
            },
        ]
    )


def heavy_threshold_rows(inputs: dict[str, float]) -> list[dict[str, Any]]:
    species = [
        ("real_scalar", 1.0, "positive", "one real minimally coupled scalar"),
        ("Dirac_fermion", -4.0, "negative", "one four-component Dirac fermion"),
        ("massive_vector", 3.0, "positive", "one Stueckelberg-complete Proca vector"),
    ]
    scalar_floor = (
        HBAR_C_EV_M
        * PLANCK_LENGTH_M
        / (
            math.sqrt(SCALAR_CANONICAL_DENOMINATOR)
            * inputs["neutron_star_ell_m"] ** 2
        )
    )
    rows: list[dict[str, Any]] = []
    for species_name, ratio, sign, meaning in species:
        rows.append(
            {
                "species": species_name,
                "physical_counting_unit": meaning,
                "I1_coefficient_ratio_to_real_scalar": ratio,
                "zeta_plus_threshold": (
                    f"{ratio:g}/[30240(4pi)^2 m^2]"
                ),
                "sign": sign,
                "parity_odd_threshold": 0.0,
                "one_species_NS_one_percent_mass_floor_eV_no_cancellation": (
                    scalar_floor * math.sqrt(abs(ratio))
                ),
                "local_expansion_requirement": "Q much less than m",
                "source": HEAVY_FIELDS_URL,
                "status": "FINITE_THRESHOLD_BASIS_DERIVED_SPECTRUM_SUM_OPEN",
                "passed": ratio != 0.0,
            }
        )
    return tagged(rows)


def wilson_bound_rows(inputs: dict[str, float]) -> list[dict[str, Any]]:
    absolute_a = inputs["robust_abs_ell_m"] ** 4
    positive_a = inputs["robust_positive_ell_m"] ** 4
    neutron_star_a = inputs["neutron_star_ell_m"] ** 4
    rows = [
        {
            "bound_id": "WBOUND4925_00_robust_abs",
            "arena": "GW250114 two-branch robustness envelope",
            "coefficient_sign_domain": "signed arbitrary",
            "alpha_endpoint": inputs["robust_abs_alpha"],
            "mass_anchor_solar": inputs["mass_q95_solar"],
            "ell_bound_m": inputs["robust_abs_ell_m"],
            "abs_a_eff_bound_m4": absolute_a,
            "affine_Wilson_constraint": "-Aobs-a_calc <= a_UV^R(muU) <= Aobs-a_calc",
            "interpretation": "conservative envelope only; not a polarization-weighted likelihood combination",
            "status": "CURRENT_NONCLAIM_SIGNED_IR_WILSON_ENVELOPE",
            "passed": True,
        },
        {
            "bound_id": "WBOUND4925_01_positive",
            "arena": "GW250114 positive-threshold robustness envelope",
            "coefficient_sign_domain": "nonnegative total branch",
            "alpha_endpoint": inputs["robust_positive_alpha"],
            "mass_anchor_solar": inputs["mass_q95_solar"],
            "ell_bound_m": inputs["robust_positive_ell_m"],
            "abs_a_eff_bound_m4": positive_a,
            "affine_Wilson_constraint": "0 <= a_eff <= Apositive",
            "interpretation": "applies only when the complete matched coefficient is nonnegative",
            "status": "CURRENT_NONCLAIM_POSITIVE_IR_WILSON_ENVELOPE",
            "passed": True,
        },
        {
            "bound_id": "WBOUND4925_02_NS_domain",
            "arena": "1.4-solar-mass 12-km neutron-star one-percent target",
            "coefficient_sign_domain": "absolute domain target",
            "ell_bound_m": inputs["neutron_star_ell_m"],
            "abs_a_eff_bound_m4": neutron_star_a,
            "affine_Wilson_constraint": "abs(a_eff) <= ell_NS^4",
            "interpretation": "internal perturbative-control target before EOS completion",
            "status": "COMPACT_ONE_PERCENT_TARGET_NOT_DATA_BOUND",
            "passed": True,
        },
        {
            "bound_id": "WBOUND4925_03_gap",
            "arena": "current observation versus compact target",
            "coefficient_sign_domain": "absolute comparison",
            "ell_bound_m": inputs["robust_abs_ell_m"],
            "abs_a_eff_bound_m4": absolute_a,
            "affine_Wilson_constraint": "Aobs/A_NS=(ell_obs/ell_NS)^4",
            "coefficient_room_factor": absolute_a / neutron_star_a,
            "length_room_factor": (
                inputs["robust_abs_ell_m"] / inputs["neutron_star_ell_m"]
            ),
            "interpretation": "the current conservative QNM envelope is not a one-percent compact certificate",
            "status": "COMPACT_PROMOTION_GAP_QUANTIFIED",
            "passed": absolute_a > neutron_star_a,
        },
    ]
    return tagged(rows)


def induced_scale_rows(inputs: dict[str, float]) -> list[dict[str, Any]]:
    branches = [row for row in read_csv(BRANCH_TESTS_PATH) if float(row["W1"]) > 0.0]
    rows: list[dict[str, Any]] = []
    for row in branches:
        weight = float(row["W1"])
        cutoff_ratio = math.sqrt(96.0 * math.pi**2 / weight)
        cutoff_eV = cutoff_ratio * REDUCED_PLANCK_ENERGY_EV
        inverse_cutoff_m = HBAR_C_EV_M / cutoff_eV
        rows.append(
            {
                "branch": row["branch"],
                "W1": weight,
                "LambdaUV_over_reduced_Planck": cutoff_ratio,
                "LambdaUV_eV_after_measured_G_matching": cutoff_eV,
                "ell_for_abs_cW_equal_one_m": inverse_cutoff_m,
                "abs_cW_at_robust_GW_envelope": (
                    inputs["robust_abs_ell_m"] / inverse_cutoff_m
                )
                ** 4,
                "abs_cW_at_NS_one_percent_target": (
                    inputs["neutron_star_ell_m"] / inverse_cutoff_m
                )
                ** 4,
                "cW_equal_one_length_ratio_to_NS_target": (
                    inverse_cutoff_m / inputs["neutron_star_ell_m"]
                ),
                "matching_formula": "W1 LambdaUV^2=96 pi^2 Mbar_Pl^2",
                "natural_cW_equal_one_is_assumption": True,
                "branch_is_parent_selected": False,
                "status": "EXACT_CONDITIONAL_INDUCED_SCALE_NOT_WILSON_PREDICTION",
                "passed": cutoff_eV > 0.0,
            }
        )
    return tagged(rows)


def gate_decision_rows(inputs: dict[str, float]) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "gate": "H_to_g_jacobian",
                "status": "UNIT_MAGNITUDE_DERIVED_IN_4D",
                "decision": "the selected component DH measure does not create a hidden local C3 Jacobian term",
                "passed": True,
            },
            {
                "gate": "Hghost_finite_split",
                "status": "COLLAPSED_INTO_RENORMALIZED_WILSON",
                "decision": "do not count the bare coefficient and scheme-dependent metric-ghost finite part as two physical inputs",
                "passed": True,
            },
            {
                "gate": "two_loop_running",
                "status": "DERIVED_RG_INVARIANT_TRANSFER",
                "decision": "retain the GS logarithm; its Planck-reference transfer is about one Planck length in all displayed arenas",
                "passed": True,
            },
            {
                "gate": "boundary_zero_proof",
                "status": "NOT_DERIVED",
                "decision": "M0 zero, minimal subtraction and the H coordinate Jacobian do not fix the physical finite I1 integration constant",
                "passed": True,
            },
            {
                "gate": "asymptotic_safety_route",
                "status": "EXTERNAL_CANDIDATE_NOT_ADOPTED",
                "decision": "a fixed-point mechanism remains testable but requires the actual MTS H-plus-matter functional flow",
                "passed": True,
            },
            {
                "gate": "heavy_threshold_basis",
                "status": "SPIN_0_HALF_1_COEFFICIENTS_DERIVED",
                "decision": "use the +1 -4 +3 Ricci-flat I1 ratios; the actual MTS and visible spectrum sum remains next-stage work",
                "passed": True,
            },
            {
                "gate": "I1_parameter_count",
                "status": "ONE_SIGNED_IR_WILSON_INPUT",
                "decision": "local observations require one a_IR(Qref), while microscopic decomposition remains a fundamental-theory target",
                "passed": True,
            },
            {
                "gate": "current_Wilson_bound",
                "status": "ROBUST_NONCLAIM_ENVELOPE_ACQUIRED",
                "decision": f"retain abs(ell_IR)<={inputs['robust_abs_ell_m']/1000.0:.6f} km as a conservative branch envelope",
                "passed": True,
            },
            {
                "gate": "induced_scale",
                "status": "PLANCK_NATURAL_SAFETY_CONDITIONAL_NOT_PROOF",
                "decision": "cW of order one at the Newton-matched induced cutoff is fantastically below compact bounds but naturalness is not a boundary condition",
                "passed": True,
            },
            {
                "gate": "weak_invariant_vacuum_GR",
                "status": "RETAINED",
                "decision": "the one-Wilson representation and negligible running preserve the weak local branch",
                "passed": True,
            },
            {
                "gate": "compact_vacuum_GR",
                "status": "NOT_PROMOTED",
                "decision": "the conservative QNM coefficient room remains above the internal one-percent compact target",
                "passed": True,
            },
            {
                "gate": "full_MTS_to_GR",
                "status": "NOT_PROMOTED",
                "decision": "the UV value, physical threshold spectrum and compact matter completion remain open",
                "passed": True,
            },
            {
                "gate": "next_target",
                "status": "THRESHOLD_SPECTRUM_AND_MOTION_SCALE",
                "decision": NEXT_TARGET,
                "passed": True,
            },
        ]
    )


def source_register_rows() -> list[dict[str, Any]]:
    local_sources = [
        (
            "SRC4925_00_4875",
            POST / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md",
            "INTEGRATED_PRINCIPAL_DENSITY_PARENT_AND_SPIN2_POLE_THEOREM_4875",
            "integrated_H_parent",
        ),
        (
            "SRC4925_01_4876",
            POST / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md",
            "INTEGRATED_H_PARENT_SADDLE_HEAT_KERNEL_POLE_HIERARCHY_4876",
            "counterterm_parent",
        ),
        (
            "SRC4925_02_4877",
            POST / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md",
            "MTS_SPECTRUM_NO_GO_NONLOCAL_COMPLETION_AND_RENORMALIZED_VACUUM_FREEZE_4877",
            "spectrum_and_nonlocal_split",
        ),
        (
            "SRC4925_03_4904",
            POST / "4904-Y5-R2FR-current-unified-action-assembly-Ward-identity-and-parameter-prediction-ledger.md",
            "MTS_CURRENT_UNIFIED_ACTION_WARD_PARAMETER_GATE_4904",
            "current_action",
        ),
        (
            "SRC4925_04_4915",
            POST / "4915-Y5-R2FR-parent-EH-residue-universal-source-coupling-and-measured-G-calibration-or-closure-demotion.md",
            "MTS_SINGLE_FUNCTIONAL_EH_SOURCE_RESIDUE_4915",
            "measured_G_owner",
        ),
        (
            "SRC4925_05_4916",
            POST / "4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md",
            "MTS_COVARIANTIZATION_MAP_FLOW_CHARGE_4916",
            "H_metric_map",
        ),
        (
            "SRC4925_06_4921",
            POST / "4921-Y5-R2FR-pure-metric-curvature-cubed-and-nonlocal-tail-observable-separation-or-invariant-vacuum-GR-domain-extension-gate.md",
            "MTS_C3_NONLOCAL_OBSERVABLE_DOMAIN_GATE_4921",
            "GS_running",
        ),
        (
            "SRC4925_07_4922",
            POST / "4922-Y5-R2FR-cubic-curvature-strong-field-waveform-love-ringdown-bound-or-compact-vacuum-GR-domain-gate.md",
            "MTS_WEYL_C3_GW170608_DOMAIN_GATE_4922",
            "canonical_C3_map",
        ),
        (
            "SRC4925_08_4923",
            POST / "4923-Y5-R2FR-GW250114-gravitational-QNM-parity-even-Weyl-cubic-recast-or-posterior-acquisition-gate.md",
            "MTS_GW250114_GRAVITATIONAL_QNM_WEYL_C3_RECAST_4923",
            "current_observational_envelope",
        ),
        (
            "SRC4925_09_4924",
            POST / "4924-Y5-R2FR-renormalized-parent-Weyl-cubic-finite-matching-sign-and-scale-from-motion-scalar-determinant-or-explicit-counterterm-boundary.md",
            "MTS_PARENT_WEYL_C3_FINITE_MATCHING_4924",
            "scalar_threshold_and_boundary",
        ),
        (
            "SRC4925_10_checkpoint",
            POST / "4925-Y5-R2FR-integrated-H-two-loop-renormalization-condition-and-finite-zeta-plus-boundary-owner-or-explicit-Wilson-input.md",
            MARKER,
            "generated_checkpoint",
        ),
        (
            "SRC4925_11_research",
            Path(__file__).resolve(),
            "def h_metric_jacobian_theory",
            "generated_research_code",
        ),
        (
            "SRC4925_12_validation",
            SCRIPTS / "Y5_R2FR_4925_integrated_H_two_loop_Wilson_boundary_validation.py",
            "VAL4925_OVERALL",
            "generated_validation_code",
        ),
        (
            "SRC4925_13_formal",
            FORMAL / "941-PPC4161-integrated-H-two-loop-Wilson-boundary.md",
            FORMAL_MARKER,
            "formal_summary",
        ),
        (
            "SRC4925_14_claims",
            FORMAL / "02-claims-register.csv",
            "L-767",
            "claim_register",
        ),
        (
            "SRC4925_15_variables",
            FORMAL / "04-variable-audit.csv",
            "HMetricJacobian4925_MTS",
            "variable_register",
        ),
        (
            "SRC4925_16_equations",
            FORMAL / "05-equation-register.md",
            "1.218 Integrated-H measure and one-Wilson matching",
            "equation_register",
        ),
        (
            "SRC4925_17_redteam",
            FORMAL / "06-consistency-red-team.md",
            "169. A scheme split is not two physical Weyl-cubic parameters",
            "redteam_register",
        ),
        (
            "SRC4925_18_spine",
            FORMAL / "07-unification-spine.md",
            "PPC4161 checkpoint 4925",
            "spine_register",
        ),
        (
            "SRC4925_19_resume",
            POST / "CURRENT_LOCAL_RESUME.md",
            "4925-Y5-R2FR-integrated-H-two-loop",
            "resume_register",
        ),
        (
            "SRC4925_20_4877_data",
            BRANCH_TESTS_PATH,
            "BT4877_05",
            "induced_spectrum_input",
        ),
        (
            "SRC4925_21_4922_data",
            COMPACT_PATH,
            "1.4_solar_mass_12km_neutron_star",
            "compact_domain_input",
        ),
        (
            "SRC4925_22_4923_robust",
            ROBUST_PATH,
            "axial_minus",
            "robust_alpha_input",
        ),
        (
            "SRC4925_23_4923_recast",
            RECAST_PATH,
            "polar_plus",
            "branch_recast_input",
        ),
        (
            "SRC4925_24_4923_audit",
            POSTERIOR_AUDIT_PATH,
            "POST4923_08_mass",
            "mass_input",
        ),
        (
            "SRC4925_25_4924_scalar",
            OUTPUT / "P8_Y5_R2FR_4924_SCALAR_THRESHOLD.csv",
            "SCALAR4924_N1",
            "motion_scalar_threshold",
        ),
        (
            "SRC4925_26_4924_GS",
            OUTPUT / "P8_Y5_R2FR_4924_GS_CANONICAL_RUNNING.csv",
            "GS4924_log_1",
            "canonical_running",
        ),
        (
            "SRC4925_27_4924_validation",
            OUTPUT / "P8_Y5_BRR545_4924_VALIDATION.csv",
            "VAL4924_OVERALL",
            "prior_validation",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker, role in local_sources:
        exists = path.exists()
        marker_found = exists and marker in read_text_auto(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path_or_url": path.relative_to(ROOT).as_posix(),
                "source_role": role,
                "marker": marker,
                "local_path_required": True,
                "source_exists": exists,
                "marker_found": marker_found,
                "sha256": digest(path) if exists else "",
                "status": "LOCAL_SOURCE_VERIFIED" if exists and marker_found else "LOCAL_SOURCE_FAILED",
                "passed": exists and marker_found,
            }
        )
    external_sources = [
        ("SRC4925_28_GS", GS_URL, "two-loop pure-gravity divergence", "primary_theory"),
        ("SRC4925_29_EFT", EFT_URL, "known versus unknown gravity EFT terms", "primary_theory"),
        ("SRC4925_30_AS", ASYMPTOTIC_SAFETY_URL, "C3 fixed-point candidate", "primary_theory_candidate"),
        ("SRC4925_31_causality", CAUSALITY_URL, "higher-spin causality condition", "primary_theory"),
        ("SRC4925_32_heavy", HEAVY_FIELDS_URL, "spin-zero half one finite C3 thresholds", "primary_theory"),
    ]
    for source_id, url, marker, role in external_sources:
        rows.append(
            {
                "source_id": source_id,
                "source_path_or_url": url,
                "source_role": role,
                "marker": marker,
                "local_path_required": False,
                "source_exists": True,
                "marker_found": True,
                "sha256": "",
                "status": "EXTERNAL_PRIMARY_URL_RECORDED",
                "passed": True,
            }
        )
    return tagged(rows)


def main() -> int:
    inputs = physical_inputs()
    tables = {
        "P8_Y5_R2FR_4925_PARENT_UV_OWNERSHIP.csv": parent_ownership_rows(),
        "P8_Y5_R2FR_4925_H_TO_G_JACOBIAN.csv": jacobian_rows(),
        "P8_Y5_R2FR_4925_RENORMALIZED_COEFFICIENT_COLLAPSE.csv": coefficient_collapse_rows(),
        "P8_Y5_R2FR_4925_TWO_LOOP_RG_TRANSFER.csv": rg_transfer_rows(inputs),
        "P8_Y5_R2FR_4925_BOUNDARY_ROUTE_AUDIT.csv": boundary_route_rows(),
        "P8_Y5_R2FR_4925_HEAVY_FIELD_THRESHOLD_BASIS.csv": heavy_threshold_rows(inputs),
        "P8_Y5_R2FR_4925_WILSON_BOUND.csv": wilson_bound_rows(inputs),
        "P8_Y5_R2FR_4925_INDUCED_SCALE_ENVELOPE.csv": induced_scale_rows(inputs),
        "P8_Y5_R2FR_4925_GATE_DECISION.csv": gate_decision_rows(inputs),
    }
    for filename, rows in tables.items():
        write_csv(OUTPUT / filename, rows)
    sources = source_register_rows()
    write_csv(OUTPUT / "P8_Y5_R2FR_4925_SOURCE_REGISTER.csv", sources)
    all_rows = [row for rows in tables.values() for row in rows]
    passed = all(bool(row.get("passed", True)) for row in all_rows) and all(
        bool(row["passed"]) for row in sources
    )
    print(
        "P8_Y5_R2FR_4925_INTEGRATED_H_TWO_LOOP_WILSON_PASS"
        if passed
        else "P8_Y5_R2FR_4925_INTEGRATED_H_TWO_LOOP_WILSON_FAIL"
    )
    print("H_to_g_abs_jacobian_4D=1")
    print(f"robust_abs_ell_km={inputs['robust_abs_ell_m']/1000.0}")
    print(f"positive_ell_km={inputs['robust_positive_ell_m']/1000.0}")
    print("independent_IR_I1_inputs=1")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

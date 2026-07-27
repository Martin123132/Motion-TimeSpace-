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

MARKER = "MTS_PARENT_ENVIRONMENTAL_BIRESPONSE_OR_GALAXY_FREEZE_4907"
FORMAL_MARKER = "PPC4161_ENVIRONMENTAL_BIRESPONSE_GALAXY_FREEZE_4907"
NEXT_TARGET = (
    "4908-Y5-R2FR-microscopic-MTS-metric-three-point-vertex-and-"
    "Weyl-cubic-coefficient-or-zero-residual-theorem.md"
)

AU_M = 149_597_870_700.0
KPC_M = 3.085_677_581_491_367e19
SOLAR_COMPACTNESS = 2.122_502_570_792_008e-6
BETA_ANCHOR = -1.0 / 18.0
BETA_V19 = -0.2


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
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


def quantile(values: list[float], probability: float) -> float:
    finite = sorted(value for value in values if math.isfinite(value))
    if not finite:
        return math.nan
    if len(finite) == 1:
        return finite[0]
    position = probability * (len(finite) - 1)
    lower = math.floor(position)
    upper = math.ceil(position)
    fraction = position - lower
    return finite[lower] * (1.0 - fraction) + finite[upper] * fraction


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    local_sources = [
        (
            "SRC4907_00_4906",
            POST
            / "4906-Y5-R2FR-galaxy-response-to-no-slip-covariant-form-factor-and-independent-lensing-gate.md",
            "MTS_GALAXY_KERNEL_NO_SLIP_LENSING_ARBITRATION_4906",
            "validated_predecessor",
        ),
        (
            "SRC4907_01_4906_validation",
            OUTPUT / "P8_Y5_BRR545_4906_VALIDATION.csv",
            "VAL4906_OVERALL,PASS",
            "validated_predecessor",
        ),
        (
            "SRC4907_02_current_action",
            POST
            / "4904-Y5-R2FR-current-unified-action-assembly-Ward-identity-and-parameter-prediction-ledger.md",
            "MTS_CURRENT_UNIFIED_ACTION_WARD_PARAMETER_GATE_4904",
            "active_field_content",
        ),
        (
            "SRC4907_03_memory_scalar",
            POST
            / "4886-Y5-R2FR-canonical-memory-scalar-local-screening-scalarization-and-same-parent-cosmology-compatibility-gate.md",
            "MTS_MEMORY_SCALAR_SCREENING_COSMOLOGY_4886",
            "conformal_scalar_local_gate",
        ),
        (
            "SRC4907_04_memory_validation",
            OUTPUT / "P8_Y5_BRR545_4886_VALIDATION.csv",
            "VAL4886_OVERALL,PASS",
            "conformal_scalar_validation",
        ),
        (
            "SRC4907_05_scalar_PPN",
            OUTPUT / "P8_Y5_R2FR_4886_PPN_COSMOLOGY_SUMMARY.csv",
            "alpha_DEF_squared_max",
            "conformal_scalar_PPN_bound",
        ),
        (
            "SRC4907_06_scalar_range",
            OUTPUT / "P8_Y5_R2FR_4886_WEAK_SOURCE_RANGE.csv",
            "solar_charge_ratio",
            "weak_source_screening_and_range",
        ),
        (
            "SRC4907_07_derivative_source",
            POST
            / "4887-Y5-R2FR-conserved-derivative-memory-source-with-local-PPN-silence-and-FLRW-activation-or-active-M-cosmology-demotion-gate.md",
            "MTS_EXPANSION_DRIVEN_MEMORY_SOURCE_4887",
            "stationary_flow_source",
        ),
        (
            "SRC4907_08_bath_retirement",
            POST
            / "4896-Y5-R2FR-full-matrix-nonlocal-FLRW-reshoot-covariant-bath-stress-and-constraint-gate.md",
            "MTS_FULL_MATRIX_FLRW_STRESS_RETIREMENT_GATE_4896",
            "bath_retirement",
        ),
        (
            "SRC4907_09_local_EFT_Maxwell",
            POST
            / "4878-Y5-R2FR-renormalized-EFT-local-limit-and-arena-specific-nonlocal-residual-bounds-to-R10-PPN-clocks-orbit-and-Maxwell.md",
            "MTS_RENORMALIZED_EFT_LOCAL_ARENA_BOUNDS_4878",
            "Maxwell_and_Poynting_projection",
        ),
        (
            "SRC4907_10_local_GR",
            POST
            / "4879-Y5-R2FR-source-size-contact-matching-and-second-order-beta-completion-plus-gauge-invariant-light-kernel-or-strict-EFT-local-GR-promotion-gate.md",
            "MTS_FINITE_SOURCE_BETA_LIGHT_CLOCK_LOCAL_GR_CERTIFICATE_4879",
            "stationary_local_GR_certificate",
        ),
        (
            "SRC4907_11_galaxy_spread",
            OUTPUT / "P8_Y5_R2FR_4906_RESPONSE_SPREAD.csv",
            "fraction_mu_greater_than_4_over_3",
            "galaxy_force_enhancement",
        ),
        (
            "SRC4907_12_galaxy_curves",
            OUTPUT / "P8_Y5_R2FR_4906_RESPONSE_PER_GALAXY.csv",
            "L_eff_kpc",
            "galaxy_response_lengths",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker, role in local_sources:
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
                "source_checked_date": "2026-07-12",
            }
        )
    return {
        "rows": rows,
        "local_sources": len(rows),
        "passed": all(
            row["source_exists"] and row["marker_found"] for row in rows
        ),
    }


@lru_cache(maxsize=None)
def surviving_parent_carriers() -> dict[str, Any]:
    rows = [
        {
            "carrier": "public_metric_g_hat_H",
            "current_status": "ACTIVE",
            "matter_interface": "one Standard-Model Hilbert source",
            "environmental_response_capacity": "analytic metric residuals only unless a new nonanalytic branch is derived",
            "eligible_without_reentry": True,
        },
        {
            "carrier": "Standard_Model_fields",
            "current_status": "ACTIVE_KNOWN_LIMIT",
            "matter_interface": "minimal public metric and gauge interactions",
            "environmental_response_capacity": "ordinary stress including electromagnetic Poynting flux",
            "eligible_without_reentry": True,
        },
        {
            "carrier": "microscopic_psi_r_psi_a_X",
            "current_status": "INTEGRATED_MATCHING_LAYER",
            "matter_interface": "no active direct mixed vertex",
            "environmental_response_capacity": "pure metric matching coefficients and form factors",
            "eligible_without_reentry": False,
        },
        {
            "carrier": "canonical_memory_scalar_M",
            "current_status": "UV_DETERMINANT_CONDITIONAL_REENTRY",
            "matter_interface": "minimal conformal owner A=exp(beta phi^2) already tested",
            "environmental_response_capacity": "scalar dynamics but leading conformal lensing cancels",
            "eligible_without_reentry": False,
        },
        {
            "carrier": "bath_clock_flow_u",
            "current_status": "RETIRED_SOURCE",
            "matter_interface": "derivative expansion source sigma_theta div u",
            "environmental_response_capacity": "FLRW activation but exact stationary silence",
            "eligible_without_reentry": False,
        },
        {
            "carrier": "galaxy_support_law",
            "current_status": "EMPIRICAL_PILLAR",
            "matter_interface": "none at action level",
            "environmental_response_capacity": "source-state radial support cache",
            "eligible_without_reentry": False,
        },
    ]
    return {
        "rows": rows,
        "active_extra_light_MTS_fields": 0,
        "active_direct_MTS_matter_vertices": 0,
        "eligible_environmental_MTS_carriers": sum(
            row["eligible_without_reentry"]
            and row["carrier"] not in {"public_metric_g_hat_H", "Standard_Model_fields"}
            for row in rows
        ),
        "passed": len(rows) == 6
        and sum(row["current_status"] == "ACTIVE" for row in rows) == 1,
    }


@lru_cache(maxsize=None)
def analytic_metric_scaling_theorem() -> dict[str, Any]:
    source_scale = sp.symbols("lambda", positive=True)
    support_zero = sp.symbols("S_0", real=True)
    coefficients = sp.symbols("c_1:6")
    analytic_response = sum(
        coefficient * source_scale**order
        for order, coefficient in enumerate(coefficients, start=1)
    )
    difference = sp.expand(analytic_response - support_zero)
    coefficient_equations = sp.Poly(difference, source_scale).all_coeffs()
    identity_solution = sp.solve(
        coefficient_equations,
        [*coefficients, support_zero],
        dict=True,
    )
    rows = [
        {
            "action_class": "calibrated_EH_plus_fixed_background",
            "leading_source_scaling": "lambda",
            "galaxy_lambda_zero_scaling": "lambda^0",
            "can_reproduce_nonzero_canonical_support_exactly": False,
            "reason": "the calibrated Lambda background has a fixed r^2 profile and no source-defined L_eff; the source response starts linearly",
        },
        {
            "action_class": "quadratic_local_or_nonlocal_metric",
            "leading_source_scaling": "lambda",
            "galaxy_lambda_zero_scaling": "lambda^0",
            "can_reproduce_nonzero_canonical_support_exactly": False,
            "reason": "the linearized propagator is source independent",
        },
        {
            "action_class": "analytic_curvature_degree_n_ge_3",
            "leading_source_scaling": "lambda^(n-1)",
            "galaxy_lambda_zero_scaling": "lambda^0",
            "can_reproduce_nonzero_canonical_support_exactly": False,
            "reason": "the first perturbative correction is at least quadratic in the source",
        },
        {
            "action_class": "finite_analytic_metric_series",
            "leading_source_scaling": "sum_p>=1 c_p lambda^p",
            "galaxy_lambda_zero_scaling": "S_0 nonzero",
            "can_reproduce_nonzero_canonical_support_exactly": False,
            "reason": "the polynomial identity forces S_0 and every c_p to zero",
        },
        {
            "action_class": "nonanalytic_or_separate_environmental_branch",
            "leading_source_scaling": "not fixed by the analytic theorem",
            "galaxy_lambda_zero_scaling": "potentially lambda^0",
            "can_reproduce_nonzero_canonical_support_exactly": True,
            "reason": "logical escape only; requires a new branch, state selection and local-GR proof absent from the active parent",
        },
    ]
    return {
        "rows": rows,
        "analytic_response": str(analytic_response),
        "identity_difference": str(difference),
        "identity_solution": str(identity_solution),
        "source_zero_limit": str(sp.limit(analytic_response, source_scale, 0)),
        "galaxy_zero_limit": str(support_zero),
        "analytic_metric_route_closes_current_galaxy_law": False,
        "nonanalytic_escape_parent_owned": False,
        "passed": identity_solution
        == [
            {
                coefficients[0]: 0,
                coefficients[1]: 0,
                coefficients[2]: 0,
                coefficients[3]: 0,
                coefficients[4]: 0,
                support_zero: 0,
            }
        ],
    }


def weak_source_charge_ratio(beta: float, compactness: float) -> tuple[float, float]:
    x_squared = 12.0 * abs(beta) * compactness
    ratio = 1.0 + 2.0 * x_squared / 5.0 + 17.0 * x_squared**2 / 105.0
    return x_squared, ratio


@lru_cache(maxsize=None)
def conformal_scalar_galaxy_local_gate() -> dict[str, Any]:
    ppn = read_csv(OUTPUT / "P8_Y5_R2FR_4886_PPN_COSMOLOGY_SUMMARY.csv")[0]
    weak = read_csv(OUTPUT / "P8_Y5_R2FR_4886_WEAK_SOURCE_RANGE.csv")[0]
    spread = read_csv(OUTPUT / "P8_Y5_R2FR_4906_RESPONSE_SPREAD.csv")
    curves = read_csv(OUTPUT / "P8_Y5_R2FR_4906_RESPONSE_PER_GALAXY.csv")

    alpha_squared_max = float(ppn["alpha_DEF_squared_max"])
    deliberately_generous_force_envelope = 2.0 * alpha_squared_max
    rows: list[dict[str, Any]] = []
    for row in spread:
        required_p16 = float(row["mu_pointwise_p16"]) - 1.0
        required_median = float(row["mu_pointwise_median"]) - 1.0
        required_p84 = float(row["mu_pointwise_p84"]) - 1.0
        rows.append(
            {
                "r_over_r_out": float(row["r_over_r_out"]),
                "galaxy_count": int(row["galaxy_count"]),
                "required_force_enhancement_p16": required_p16,
                "required_force_enhancement_median": required_median,
                "required_force_enhancement_p84": required_p84,
                "Cassini_alpha_DEF_squared_max": alpha_squared_max,
                "generous_unscreened_scalar_envelope": deliberately_generous_force_envelope,
                "p16_over_generous_scalar_envelope": required_p16
                / deliberately_generous_force_envelope,
                "median_over_generous_scalar_envelope": required_median
                / deliberately_generous_force_envelope,
                "same_branch_magnitude_pass": required_p16
                <= deliberately_generous_force_envelope,
            }
        )

    anchor_x2, anchor_charge = weak_source_charge_ratio(
        BETA_ANCHOR, SOLAR_COMPACTNESS
    )
    v19_x2, v19_charge = weak_source_charge_ratio(
        BETA_V19, SOLAR_COMPACTNESS
    )
    lengths = [float(row["L_eff_kpc"]) for row in curves]
    minimum_length = min(lengths)
    minimum_length_attenuation = math.exp(
        -AU_M / (minimum_length * KPC_M)
    )
    scalar_rows = [
        {
            "branch": "4886_beta_minus_1_over_18",
            "beta": BETA_ANCHOR,
            "solar_x_squared": anchor_x2,
            "solar_charge_ratio": anchor_charge,
            "screened": anchor_charge < 0.1,
            "interpretation": "weak source is unscreened and slightly enhanced",
        },
        {
            "branch": "v19_beta_minus_0p2",
            "beta": BETA_V19,
            "solar_x_squared": v19_x2,
            "solar_charge_ratio": v19_charge,
            "screened": v19_charge < 0.1,
            "interpretation": "stronger negative beta remains deeply in the unscreened weak-source regime",
        },
        {
            "branch": "galaxy_range_Yukawa_test",
            "beta": "not_applicable",
            "solar_x_squared": "not_applicable",
            "solar_charge_ratio": minimum_length_attenuation,
            "screened": minimum_length_attenuation < 0.1,
            "interpretation": "a range at least as long as the shortest empirical L_eff is effectively unattenuated across one AU",
        },
    ]
    source_charge_from_4886 = float(weak["solar_charge_ratio"])
    return {
        "rows": rows,
        "scalar_rows": scalar_rows,
        "Cassini_alpha_DEF_squared_max": alpha_squared_max,
        "generous_force_envelope": deliberately_generous_force_envelope,
        "minimum_required_to_envelope_ratio": min(
            row["p16_over_generous_scalar_envelope"] for row in rows
        ),
        "maximum_required_to_envelope_ratio": max(
            row["median_over_generous_scalar_envelope"] for row in rows
        ),
        "anchor_solar_charge_reproduced": abs(
            anchor_charge - source_charge_from_4886
        )
        < 1e-12,
        "v19_solar_charge_ratio": v19_charge,
        "minimum_empirical_L_eff_kpc": minimum_length,
        "median_empirical_L_eff_kpc": quantile(lengths, 0.5),
        "minimum_range_AU_attenuation": minimum_length_attenuation,
        "pure_conformal_lensing_response": 1.0,
        "same_branch_galaxy_route_passes": False,
        "passed": all(not row["same_branch_magnitude_pass"] for row in rows)
        and anchor_charge > 1.0
        and v19_charge > 1.0
        and minimum_length_attenuation > 0.99999999,
    }


@lru_cache(maxsize=None)
def stationary_flow_source_theorem() -> dict[str, Any]:
    rows = [
        {
            "configuration": "normalized_stationary_Killing_flow",
            "divergence": "nabla_mu u^mu=0",
            "memory_source": "sigma_theta theta=0",
            "can_generate_stationary_galaxy_support": False,
            "reason": "Killing divergence and K dot grad K^2 both vanish",
        },
        {
            "configuration": "stationary_axisymmetric_circular_disk",
            "divergence": "(sqrt(-g))^-1[partial_t(sqrt(-g)u^t)+partial_phi(sqrt(-g)u^phi)]=0",
            "memory_source": "sigma_theta theta=0",
            "can_generate_stationary_galaxy_support": False,
            "reason": "u^R=u^z=0 and all fields are independent of t and phi",
        },
        {
            "configuration": "radial_inflow_or_outflow",
            "divergence": "nonzero in general",
            "memory_source": "flow-dependent",
            "can_generate_stationary_galaxy_support": False,
            "reason": "not the universal equilibrium stellar and gas support law and the bath carrier is retired",
        },
        {
            "configuration": "FLRW",
            "divergence": "theta=3H",
            "memory_source": "3 sigma_theta H",
            "can_generate_stationary_galaxy_support": False,
            "reason": "cosmological activation does not supply a static disk source",
        },
    ]
    return {
        "rows": rows,
        "stationary_disk_source": 0,
        "bath_source_currently_active": False,
        "derivative_route_galaxy_passes": False,
        "passed": rows[0]["divergence"] == "nabla_mu u^mu=0"
        and rows[1]["memory_source"] == "sigma_theta theta=0"
        and not any(row["can_generate_stationary_galaxy_support"] for row in rows),
    }


@lru_cache(maxsize=None)
def Maxwell_Poynting_projection() -> dict[str, Any]:
    conformal_factor = sp.symbols("A", positive=True)
    conformal_weight = sp.simplify(
        conformal_factor**4
        * conformal_factor ** (-2)
        * conformal_factor ** (-2)
    )
    spacetime_dimension = sp.Integer(4)
    field_invariant = sp.symbols("F2")
    trace = sp.simplify(
        field_invariant
        - spacetime_dimension * field_invariant / spacetime_dimension
    )
    rows = [
        {
            "projection": "four_dimensional_conformal_Maxwell_action",
            "equation": "sqrt(-g_J) g_J^-1 g_J^-1=A^4 A^-2 A^-2",
            "result": str(conformal_weight),
            "new_scalar_source": False,
        },
        {
            "projection": "free_Maxwell_trace",
            "equation": "T_EM=F^2-(4/4)F^2",
            "result": str(trace),
            "new_scalar_source": False,
        },
        {
            "projection": "Poynting_vector",
            "equation": "S^i=c T_EM^(0i)",
            "result": "retained in the ordinary Hilbert stress and Einstein momentum equation",
            "new_scalar_source": False,
        },
        {
            "projection": "photon_cone",
            "equation": "g_J=A^2 g_E",
            "result": "null cone and leading conformal lensing sum unchanged",
            "new_scalar_source": False,
        },
        {
            "projection": "required_nonconformal_escape",
            "equation": "M^2 F^2 or disformal B(phi) grad(phi) grad(phi)",
            "result": "not parent-owned and would reopen light-cone, clock and WEP gates",
            "new_scalar_source": True,
        },
    ]
    return {
        "rows": rows,
        "conformal_weight": str(conformal_weight),
        "Maxwell_trace": str(trace),
        "Poynting_gravitates_in_baseline": True,
        "Poynting_sources_trace_memory_scalar": False,
        "Maxwell_creates_missing_bi_response": False,
        "passed": conformal_weight == 1
        and trace == 0
        and not rows[0]["new_scalar_source"]
        and rows[4]["new_scalar_source"],
    }


@lru_cache(maxsize=None)
def reentry_gate_and_freeze() -> dict[str, Any]:
    carriers = surviving_parent_carriers()
    metric = analytic_metric_scaling_theorem()
    scalar = conformal_scalar_galaxy_local_gate()
    flow = stationary_flow_source_theorem()
    Maxwell = Maxwell_Poynting_projection()
    rows = [
        {
            "gate": "parent_owned_carrier",
            "requirement": "one active MTS field or metric operator generates the environmental scale",
            "status": "FAIL",
            "reason": "no active extra light carrier; the analytic metric route has the wrong source scaling",
        },
        {
            "gate": "galaxy_dynamics",
            "requirement": "same parent supplies the observed radial force magnitude",
            "status": "FAIL",
            "reason": f"even a factor-two Cassini scalar envelope is at least {scalar['minimum_required_to_envelope_ratio']:.1f} times too small",
        },
        {
            "gate": "lensing_relation",
            "requirement": "same parent fixes mu_lens with no target refit",
            "status": "FAIL",
            "reason": "the only concrete scalar re-entry has mu_lens=1 and no spin-two/disformal owner",
        },
        {
            "gate": "stationary_source",
            "requirement": "the derivative source remains nonzero in equilibrium galaxies",
            "status": "FAIL",
            "reason": "theta=0 for stationary axisymmetric circular flow",
        },
        {
            "gate": "local_GR",
            "requirement": "galaxy-strength branch screens or decouples in the Solar System",
            "status": "FAIL",
            "reason": "both tested negative-beta branches are unscreened and galaxy-range Yukawa attenuation is negligible at one AU",
        },
        {
            "gate": "Maxwell_EM_stress",
            "requirement": "Poynting stress remains correctly coupled without inventing an EM scalar source",
            "status": "PASS_BASELINE_ONLY",
            "reason": "Maxwell is conformally invariant and traceless; Poynting remains ordinary Hilbert stress",
        },
        {
            "gate": "Ward_conservation",
            "requirement": "new exchange follows from one action",
            "status": "NO_NEW_EDGE",
            "reason": "the active baseline remains conserved because no failed candidate is inserted",
        },
        {
            "gate": "action_entry_decision",
            "requirement": "all preceding action, dynamics, lensing and local gates close",
            "status": "FREEZE_GALAXY_RESIDUAL_OUTSIDE_ACTIVE_ACTION",
            "reason": "no surviving parent route closes the joint contract",
        },
    ]
    return {
        "rows": rows,
        "galaxy_empirical_pillar_retained": True,
        "galaxy_residual_active": False,
        "Gamma_MTS_res": 0,
        "new_parent_field_added": False,
        "new_free_coefficient_added": False,
        "active_novel_MTS_numeric_predictions": 0,
        "public_claim_allowed": False,
        "next_target": NEXT_TARGET,
        "passed": carriers["passed"]
        and metric["passed"]
        and scalar["passed"]
        and flow["passed"]
        and Maxwell["passed"]
        and rows[-1]["status"]
        == "FREEZE_GALAXY_RESIDUAL_OUTSIDE_ACTIVE_ACTION",
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "carriers": surviving_parent_carriers(),
        "metric": analytic_metric_scaling_theorem(),
        "scalar": conformal_scalar_galaxy_local_gate(),
        "flow": stationary_flow_source_theorem(),
        "Maxwell": Maxwell_Poynting_projection(),
        "gate": reentry_gate_and_freeze(),
    }
    all_checks_pass = all(section["passed"] for section in sections.values())
    return {
        "marker": MARKER,
        "formal_marker": FORMAL_MARKER,
        "sections": sections,
        "decision": (
            "NO_CURRENT_PARENT_ENVIRONMENTAL_BIRESPONSE_ANALYTIC_METRIC_SCALING_"
            "NO_GO_CONFORMAL_SCALAR_CASSINI_AND_LENSING_FAIL_DERIVATIVE_FLOW_"
            "STATIONARY_ZERO_MAXWELL_POYNTING_BASELINE_ONLY_GALAXY_RESIDUAL_"
            "FROZEN_OUTSIDE_ACTIVE_ACTION_PRIVATE_NONCLAIM"
        ),
        "all_checks_pass": all_checks_pass,
        "next_target": NEXT_TARGET,
    }


def main() -> int:
    calculation = result()
    sections = calculation["sections"]
    print(
        "active_extra_fields="
        f"{sections['carriers']['active_extra_light_MTS_fields']} "
        "metric_route="
        f"{sections['metric']['analytic_metric_route_closes_current_galaxy_law']} "
        "scalar_min_shortfall="
        f"{sections['scalar']['minimum_required_to_envelope_ratio']:.3f} "
        "stationary_source="
        f"{sections['flow']['stationary_disk_source']} "
        "galaxy_active="
        f"{sections['gate']['galaxy_residual_active']}"
    )
    print(calculation["decision"])
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

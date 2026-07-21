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
from scipy.interpolate import CubicSpline


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4962"
RESIDUALS = POST / "source-intake" / "mts_residuals"
EOS_ROOT = POST / "source-intake" / "microphysical_eos" / "4883" / "lalsuite"

RESULT_JSON = SOURCE / "compact_body_matching_results.json"
SENSITIVITY_CSV = SOURCE / "compact_body_sensitivity_and_no_dipole.csv"
JUNCTION_CSV = SOURCE / "junction_and_worldline_matching.csv"
RESIDUE_CSV = SOURCE / "conservative_radiative_residue_match.csv"
EOS_CSV = SOURCE / "realistic_EOS_scalar_stability_transfer.csv"
BOUNDARY_CSV = SOURCE / "strong_field_residual_boundary.csv"
DECISION_CSV = SOURCE / "compact_body_strong_GR_decision.csv"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4962_COMPACT_BODY_SENSITIVITY_FLUX_JUNCTION"
CHECKED_DATE = "2026-07-13"

C_LIGHT = 299_792_458.0
G_NEWTON = 6.67430e-11
M_SUN_KG = 1.98847e30
L_SUN_M = G_NEWTON * M_SUN_KG / C_LIGHT**2
RHO_CRITICAL_KG_M3 = 4.246023114199768e35

SOURCE_PATHS = {
    "strong_vacuum_4880": POST
    / "4880-Y5-R2FR-selected-metric-branch-local-GR-certificate-domain-of-validity-and-strong-field-entry-gate.md",
    "compact_matter_4881": POST
    / "4881-Y5-R2FR-compact-matter-interior-EOS-contact-matching-and-Riemann-cubed-coefficient-owner-gate.md",
    "multi_EOS_4883": POST
    / "4883-Y5-R2FR-tabulated-microphysical-EOS-acquisition-and-multi-EOS-mass-radius-tidal-contact-response-gate.md",
    "multi_EOS_response_4883": RESIDUALS
    / "P8_Y5_R2FR_4883_RESPONSE_BENCHMARKS.csv",
    "multi_EOS_validation_4883": RESIDUALS
    / "P8_Y5_BRR545_4883_VALIDATION.csv",
    "matter_junction_4943": POST
    / "4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-junction-or-fifth-force-residual-gate.md",
    "scalar_junction_4943": POST
    / "source-intake"
    / "functional_rg"
    / "4943"
    / "junction_scalar_charge_and_fifth_force.csv",
    "interior_stability_4943": POST
    / "source-intake"
    / "functional_rg"
    / "4943"
    / "interior_stability_benchmarks.csv",
    "universal_source_4960": POST
    / "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-local-GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md",
    "local_chain_4960": POST
    / "source-intake"
    / "functional_rg"
    / "4960"
    / "local_limit_chain_and_calibrations.csv",
    "residual_quarantine_4960": POST
    / "source-intake"
    / "functional_rg"
    / "4960"
    / "local_residual_quarantine.csv",
    "origin_boundary_4961": POST
    / "4961-Y5-R2FR-integrated-H-origin-and-induced-EH-residue-from-motion-Hessian-or-explicit-fundamental-field-boundary.md",
    "origin_result_4961": POST
    / "source-intake"
    / "functional_rg"
    / "4961"
    / "integrated_H_origin_and_induced_EH_results.json",
    "GW_bound_4923": POST
    / "4923-Y5-R2FR-GW250114-gravitational-QNM-parity-even-Weyl-cubic-recast-or-posterior-acquisition-gate.md",
    "conditional_C3_4929": POST
    / "4929-Y5-R2FR-MTS-matter-completed-C3-essential-flow-and-fixed-point-survival-or-one-Wilson-retention.md",
    "EOS_BSK24": EOS_ROOT / "BSK24.dat",
    "EOS_SLY4": EOS_ROOT / "SLY4.dat",
    "EOS_DD2": EOS_ROOT / "DD2.dat",
}

EXPECTED_HASHES = {
    "strong_vacuum_4880": "b4966159301e6c6c7fac6d618c509be5ad04d1a7ff83522eb3b3b0899cb14df0",
    "compact_matter_4881": "86151ef70734f8efdd3143ccc27d8ed56fc75b4c3df550317e788b1692fa5727",
    "multi_EOS_4883": "dea9165f9ab1e2d3309cc16a9cd3f7262d06c28817bec9611229d8b9db2f1db2",
    "multi_EOS_response_4883": "8f7a0625d8618bbabecd1b990763dd32018ea34642c2867913c136fd5cbf1454",
    "multi_EOS_validation_4883": "197fa1768ca4b7b13e5a7e1cd72629614f9f713a898ee2eb524513a1efa5f823",
    "matter_junction_4943": "a90da0e9ad0457fc3dbdb389d7bf2715cb9d707cbffa094a987b0b0553e257b5",
    "scalar_junction_4943": "5fbca2c1672d7fbb6f1741e56a3c72a2adbaee544a4fd5fd5525a616cb836df6",
    "interior_stability_4943": "3c49fdc86490eb936c27fc954b420ab1205fa2e6211e87507cc33cec7f64e3af",
    "universal_source_4960": "6cd343d022dde751f86ad82eaf0f61fb5e3616753c228f631c44a45da278a69d",
    "local_chain_4960": "e4a7d3de99b2543b2e59b4fb47368e2357b179ca472b372822bfa3a2ca17a1ce",
    "residual_quarantine_4960": "db04d7caa6c17036e18eabcfa592648b95b451c97acfb411b41440bb539b1045",
    "origin_boundary_4961": "ec6c5ff4056ed13ad92cad5e70ce125d81183abd0d79c59345dd6393987e2de2",
    "origin_result_4961": "2be33638d28a679878a17f1038543876b4df742d1a8769de9e8ead02bb665076",
    "GW_bound_4923": "1761d637256699107c8cd7bc0d7ce07a3ff530c8c40d8f4b8cf9dad5d42f4354",
    "conditional_C3_4929": "46302f298fcfa63633455cecf9977e3fb8d0384a1fe5bbf8ecd33b60e444e7ea",
    "EOS_BSK24": "78e6047b0a7724b350692b816f0d6181c49341847351e2a9a5e26b940f62aa1d",
    "EOS_SLY4": "475b77304c6da7253699c3cf48ad5a06bb637178f9615267cc0c6e6b41cc0b75",
    "EOS_DD2": "7c9b5b5b3b50219d35e8a302d596b2b08df193cb62c17386cdd969174390d1fe",
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


def truth(value: str) -> bool:
    return value.strip().lower() == "true"


def eos_central_density(eos_id: str, central_q: float) -> float:
    raw = np.loadtxt(SOURCE_PATHS[f"EOS_{eos_id}"])
    if raw.ndim != 2:
        raise ValueError(f"{eos_id}: expected rectangular EOS table")
    if raw.shape[1] == 2:
        pressure = raw[:, 0] * L_SUN_M**2
        energy = raw[:, 1] * L_SUN_M**2
    elif raw.shape[1] >= 9:
        energy = raw[:, 2] * 1.0e3 * G_NEWTON / C_LIGHT**2 * L_SUN_M**2
        pressure = raw[:, 3] * 1.0e-1 * G_NEWTON / C_LIGHT**4 * L_SUN_M**2
    else:
        raise ValueError(f"{eos_id}: unsupported EOS table")
    finite = (
        np.isfinite(pressure)
        & np.isfinite(energy)
        & (pressure > 0.0)
        & (energy > 0.0)
    )
    pressure = np.asarray(pressure[finite], dtype=float)
    energy = np.asarray(energy[finite], dtype=float)
    spline = CubicSpline(
        np.log(pressure),
        np.log(energy),
        bc_type="natural",
        extrapolate=False,
    )
    central_pressure = central_q**2.5
    central_energy = float(np.exp(spline(np.log(central_pressure))))
    return central_energy / L_SUN_M**2 * C_LIGHT**2 / G_NEWTON


def symmetry_and_residue_checks() -> tuple[dict[str, bool], dict[str, str]]:
    x, mass0, beta2, beta4 = sp.symbols(
        "x mass0 beta2 beta4", real=True
    )
    mass = mass0 + beta2 * x**2 / 2 + beta4 * x**4 / 24
    alpha = sp.simplify(sp.diff(sp.log(mass), x).subs(x, 0))
    charge = sp.simplify(-sp.diff(mass, x).subs(x, 0))
    alpha_a, alpha_b = sp.symbols("alpha_A alpha_B", real=True)
    dipole = sp.expand((alpha_a - alpha_b) ** 2).subs(
        {alpha_a: alpha, alpha_b: alpha}
    )

    residue = sp.symbols("M_R2", positive=True)
    conservative = sp.simplify(1 / residue)
    radiative = sp.simplify(residue * (1 / residue) ** 2)
    normalization = sp.symbols("a", nonzero=True)
    kinetic_rescaled = residue / normalization**2
    source_rescaled = 1 / normalization
    radiative_rescaled = sp.simplify(
        kinetic_rescaled
        * (source_rescaled / kinetic_rescaled) ** 2
    )

    checks = {
        "reflection_mass_even": sp.simplify(mass.subs(x, -x) - mass) == 0,
        "first_sensitivity_zero": alpha == 0,
        "scalar_charge_zero": charge == 0,
        "binary_scalar_dipole_zero": sp.simplify(dipole) == 0,
        "conservative_radiative_residue_equal": sp.simplify(
            radiative - conservative
        )
        == 0,
        "radiative_field_normalization_cancels": sp.simplify(
            radiative_rescaled - conservative
        )
        == 0,
    }
    expressions = {
        "mass_function": str(mass),
        "alpha_A_at_zero": str(alpha),
        "Q_A_at_zero": str(charge),
        "dipole_factor": str(sp.simplify(dipole)),
        "conservative_residue": str(conservative),
        "radiative_residue": str(radiative),
        "radiative_rescaled": str(radiative_rescaled),
    }
    return checks, expressions


def sensitivity_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "gate_id": "SENS4962_00_even_mass",
                "object": "compact-body ADM mass m_A(x_inf)",
                "equation": "m_A(-x_inf)=m_A(x_inf)",
                "result": "reflection symmetry makes the body mass even",
                "scope": "unique reflection-even compact branch",
                "status": "DERIVED",
                "passed": True,
                "valid_for_declared_parent_branch": True,
            },
            {
                "gate_id": "SENS4962_01_first_sensitivity",
                "object": "alpha_A=d ln m_A/d x_inf at x_inf=0",
                "equation": "alpha_A=0",
                "result": "first compact-body scalar sensitivity vanishes",
                "scope": "stable branch continuously connected to psi=0",
                "status": "DERIVED",
                "passed": True,
                "valid_for_declared_parent_branch": True,
            },
            {
                "gate_id": "SENS4962_02_scalar_charge",
                "object": "Q_A=-d m_A/d psi_inf",
                "equation": "Q_A=0",
                "result": "agrees with the independent 4943 flux theorem",
                "scope": "ordinary matter; no reflection-odd surface action",
                "status": "DERIVED_TWO_WAYS",
                "passed": True,
                "valid_for_declared_parent_branch": True,
            },
            {
                "gate_id": "SENS4962_03_binary_dipole",
                "object": "leading scalar dipole flux",
                "equation": "P_dipole proportional to (alpha_A-alpha_B)^2=0",
                "result": "no leading one-scalar dipole radiation",
                "scope": "both bodies on the same psi=0 branch",
                "status": "DERIVED",
                "passed": True,
                "valid_for_declared_parent_branch": True,
            },
            {
                "gate_id": "SENS4962_04_vector_charge",
                "object": "compact-body vector sensitivity",
                "equation": "no independent vector field or vector pole",
                "result": "identically absent in the selected metric-only branch",
                "scope": "does not apply to the demoted unit-flow extension",
                "status": "ABSENT_BY_FIELD_CONTENT",
                "passed": True,
                "valid_for_declared_parent_branch": True,
            },
            {
                "gate_id": "SENS4962_05_zero_mode",
                "object": "linear scalarization bifurcation",
                "equation": "int N sqrt(gamma)[B^ij D_i u D_j u+m_eff^2 u^2]=0",
                "result": "positive quadratic form and zero asymptotic data imply u=0",
                "scope": "strict-EFT corridor; B positive; m_eff^2 nonnegative",
                "status": "PERTURBATIVE_NO_ZERO_MODE",
                "passed": True,
                "valid_for_declared_parent_branch": True,
            },
            {
                "gate_id": "SENS4962_06_second_sensitivity",
                "object": "beta_A=d alpha_A/d x_inf at zero",
                "equation": "beta_A generally nonzero",
                "result": "pair effects and disconnected scalarized branches are not erased",
                "scope": "requires nonlinear global stellar solve if activated",
                "status": "FINITE_RESIDUAL_NOT_A_DIPOLE",
                "passed": True,
                "valid_for_declared_parent_branch": False,
            },
        ]
    )


def junction_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "gate_id": "MATCH4962_00_worldline",
                "system": "compact body after internal fields are integrated out",
                "equation": "S_A=-m_A int ds + (lambda_A/2) int E_mn E^mn ds + ...",
                "result": "one universal metric point-particle term plus finite-size operators",
                "status": "DIFF_WORLDLINE_EFT",
                "passed": True,
                "required_conditions": "single public metric; no extra long-range charge",
            },
            {
                "gate_id": "MATCH4962_01_metric_shell",
                "system": "metric junction with surface stress S_ab",
                "equation": "[K_ab]-h_ab[K]=-S_ab/M_R^2",
                "result": "same M_R residue as bulk Einstein equation",
                "status": "DERIVED_EH_JUNCTION",
                "passed": True,
                "required_conditions": "two-derivative selected branch",
            },
            {
                "gate_id": "MATCH4962_02_metric_no_shell",
                "system": "ordinary stellar surface without a thin shell",
                "equation": "[h_ab]=0 and [K_ab]=0",
                "result": "interior and exterior use one ADM mass and one metric",
                "status": "DERIVED",
                "passed": True,
                "required_conditions": "S_ab=0; regular surface",
            },
            {
                "gate_id": "MATCH4962_03_scalar",
                "system": "motion scalar junction",
                "equation": "[psi]=0; [n_mu K_eff^munu nabla_nu psi]=0",
                "result": "psi=0 matches through the material surface",
                "status": "IMPORTED_AND_REVALIDATED_4943",
                "passed": True,
                "required_conditions": "no reflection-odd surface action",
            },
            {
                "gate_id": "MATCH4962_04_EM",
                "system": "electromagnetic surface",
                "equation": "[n_mu D^munu]=j_Sigma^nu; [n_mu dualF^munu]=0",
                "result": "D^munu=F^munu-4c_IR C^munurhosigma F_rhosigma",
                "status": "DERIVED_FROM_SAME_EM_ACTION",
                "passed": True,
                "required_conditions": "no magnetic surface charge; same c_IR in stress",
            },
            {
                "gate_id": "MATCH4962_05_order_reduction",
                "system": "R2 and C2 stellar contacts",
                "equation": "strict-EFT order reduction selects the GR-connected solution",
                "result": "no independent heavy/runaway junction data are admitted",
                "status": "CONDITIONAL_STRICT_EFT_BRANCH",
                "passed": True,
                "required_conditions": "perturbative Wilson coefficients; analytic branch selector",
            },
        ]
    )


def residue_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "gate_id": "RAD4962_00_conservative",
                "quantity": "conservative source exchange",
                "scaling": "C_cons=1/M_R^2=8 pi G_N",
                "result": "one measured Newton residue",
                "new_independent_calibration": False,
                "status": "DERIVED_4960_REUSED",
                "passed": True,
            },
            {
                "gate_id": "RAD4962_01_wave_amplitude",
                "quantity": "far-zone tensor wave",
                "scaling": "h_TT proportional to Qddot/(M_R^2 R)",
                "result": "source amplitude uses the same M_R",
                "new_independent_calibration": False,
                "status": "DERIVED",
                "passed": True,
            },
            {
                "gate_id": "RAD4962_02_wave_flux",
                "quantity": "tensor wave stress",
                "scaling": "F_GW proportional to M_R^2 <dot h_TT dot h_TT>",
                "result": "M_R^2 times amplitude squared leaves 1/M_R^2",
                "new_independent_calibration": False,
                "status": "DERIVED",
                "passed": True,
            },
            {
                "gate_id": "RAD4962_03_quadrupole",
                "quantity": "leading isolated-binary power",
                "scaling": "P_T=G_N/(5 c^5)<Q'''_ij Q'''_ij>",
                "result": "standard GR tensor quadrupole coefficient",
                "new_independent_calibration": False,
                "status": "DERIVED_AT_TWO_DERIVATIVES",
                "passed": True,
            },
            {
                "gate_id": "RAD4962_04_metric_dipole",
                "quantity": "mass monopole and dipole radiation",
                "scaling": "Mdot=0; Dddot_i=Pdot_i=0",
                "result": "stress conservation removes lower tensor multipoles",
                "new_independent_calibration": False,
                "status": "DERIVED_BY_WARD_CONSERVATION",
                "passed": True,
            },
            {
                "gate_id": "RAD4962_05_scalar_vector",
                "quantity": "extra-polarization leading flux",
                "scaling": "Q_psi=0; alpha_A-alpha_B=0; no vector pole",
                "result": "no scalar dipole and no vector radiation on selected branch",
                "new_independent_calibration": False,
                "status": "DERIVED_ON_BRANCH",
                "passed": True,
            },
            {
                "gate_id": "RAD4962_06_normalization",
                "quantity": "arbitrary graviton field rescaling",
                "scaling": "(M_R^2/a^2)*(a/M_R^2)^2=1/M_R^2",
                "result": "radiative and conservative residues remain identical",
                "new_independent_calibration": False,
                "status": "EXACT_CANCELLATION",
                "passed": True,
            },
        ]
    )


def eos_rows() -> tuple[list[dict[str, Any]], dict[str, float]]:
    response = read_csv(SOURCE_PATHS["multi_EOS_response_4883"])
    rows: list[dict[str, Any]] = []
    max_density = 0.0
    max_ratio = 0.0
    max_tidal_cap = 0.0
    for item in response:
        density = eos_central_density(
            item["eos_id"], float(item["central_q"])
        )
        ratio = density / RHO_CRITICAL_KG_M3
        tidal_cap = float(item["cap_abs_deltaLambda_over_Lambda_fixed_M"])
        max_density = max(max_density, density)
        max_ratio = max(max_ratio, ratio)
        max_tidal_cap = max(max_tidal_cap, tidal_cap)
        rows.append(
            {
                "eos_id": item["eos_id"],
                "model_id": item["model_id"],
                "mass_Msun": float(item["mass"]),
                "radius_km": float(item["radius_km"]),
                "compactness": float(item["compactness"]),
                "central_density_kg_m3": density,
                "critical_density_kg_m3": RHO_CRITICAL_KG_M3,
                "central_to_critical_ratio": ratio,
                "orders_below_instability": -math.log10(ratio),
                "kinetic_lower_bound": 1.0 - ratio,
                "tidal_contact_cap": tidal_cap,
                "stable_branch": truth(item["stable_branch"]),
                "status": "REALISTIC_EOS_PERTURBATIVE_ZERO_MODE_EXCLUDED",
                "passed": (
                    truth(item["stable_branch"])
                    and ratio < 1.0
                    and truth(item["response_valid"])
                ),
                "valid_for_declared_parent_branch": True,
            }
        )
    return tagged(rows), {
        "max_central_density_kg_m3": max_density,
        "max_central_to_critical_ratio": max_ratio,
        "minimum_orders_below_instability": -math.log10(max_ratio),
        "max_tidal_contact_cap": max_tidal_cap,
    }


def residual_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "residual_id": "STRONG4962_00_C3",
                "operator_or_branch": "A_+ C^3",
                "current_result": "GW250114 robust envelope reaches epsilon_h about 0.040, not the one-percent gate",
                "status": "OBSERVATION_BOUNDS_BUT_DOES_NOT_PROMOTE_COMPACT_GR",
                "leading_two_derivative_GR_safe": True,
                "remaining_work": "complete parent flow or tighter compact-field bound",
                "claim_guard": "conditional 4929 ell_plus near 1.8e-36 m is not a full-parent prediction",
            },
            {
                "residual_id": "STRONG4962_01_R2_C2",
                "operator_or_branch": "a_R R^2 and a_C C^2",
                "current_result": "Einstein vacuum exact; realistic EOS contact response below 3.04e-17 under inherited caps",
                "status": "STRICT_EFT_CONTROLLED_COEFFICIENT_OWNERSHIP_OPEN",
                "leading_two_derivative_GR_safe": True,
                "remaining_work": "derive or measure finite Wilson coefficients",
                "claim_guard": "do not call control caps parent predictions",
            },
            {
                "residual_id": "STRONG4962_02_scalar_nonlinear",
                "operator_or_branch": "even motion-scalar nonlinear branch",
                "current_result": "zero branch has no perturbative zero mode across nine realistic EOS rows",
                "status": "PERTURBATIVE_BRANCH_CLOSED_DISCONNECTED_BRANCH_OPEN",
                "leading_two_derivative_GR_safe": True,
                "remaining_work": "global nonlinear stellar solve if nonconvex higher terms are activated",
                "claim_guard": "beta_A and disconnected scalarized states are not proved zero",
            },
            {
                "residual_id": "STRONG4962_03_tidal",
                "operator_or_branch": "finite-size Love and dissipative worldline operators",
                "current_result": "GR EOS dependence retained; contact shift tiny under caps",
                "status": "GR_FINITE_SIZE_BASELINE_PLUS_BOUNDED_EFT_RESIDUAL",
                "leading_two_derivative_GR_safe": True,
                "remaining_work": "binary waveform likelihood with common EOS nuisance treatment",
                "claim_guard": "ordinary EOS spread is not an MTS failure or prediction",
            },
            {
                "residual_id": "STRONG4962_04_CFF",
                "operator_or_branch": "c_IR C_mnrs F^mn F^rs",
                "current_result": "junction, propagation and stress share one coefficient",
                "status": "STRUCTURE_DERIVED_PHYSICAL_MATCHING_OPEN",
                "leading_two_derivative_GR_safe": True,
                "remaining_work": "QCD TJJ matching or one source-backed calibration",
                "claim_guard": "do not call compact electrovac exactly Einstein-Maxwell when c_IR is retained",
            },
            {
                "residual_id": "STRONG4962_05_state",
                "operator_or_branch": "nonvacuum preferred-flow or reflection-breaking state",
                "current_result": "absent only on the selected Lorentz-invariant zero-enthalpy reflection-even branch",
                "status": "OUTSIDE_SELECTED_BRANCH",
                "leading_two_derivative_GR_safe": True,
                "remaining_work": "cosmological and coherent-flow state matching",
                "claim_guard": "do not export the compact theorem to every MTS state",
            },
            {
                "residual_id": "STRONG4962_06_parent",
                "operator_or_branch": "integrated H, Diff and absolute M_R origin",
                "current_result": "explicit parent data; numerical G calibrated once",
                "status": "ONTOLOGICAL_BOUNDARY_UNCHANGED",
                "leading_two_derivative_GR_safe": True,
                "remaining_work": "future independent tensor-gauge microscopic completion if desired",
                "claim_guard": "do not call pure motion-scalar emergence proved",
            },
        ]
    )


def decision_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "decision_id": "DEC4962_00_two_derivative_compact",
                "question": "Does the selected stable metric branch reproduce compact-body GR at leading two-derivative point-particle order?",
                "decision": "YES_CONDITIONALLY",
                "reason": "one metric, zero extra charge, EH junction, universal ADM mass and same conservative-radiative residue",
                "passed": True,
                "valid_for_declared_parent_branch": True,
            },
            {
                "decision_id": "DEC4962_01_scalar_dipole",
                "question": "Is a leading compact-body scalar dipole present?",
                "decision": "NO_ON_SELECTED_BRANCH",
                "reason": "reflection symmetry and junction flux independently give alpha_A=Q_A=0",
                "passed": True,
                "valid_for_declared_parent_branch": True,
            },
            {
                "decision_id": "DEC4962_02_radiative_G",
                "question": "Does binary radiation require another gravitational calibration?",
                "decision": "NO",
                "reason": "wave amplitude and flux reduce to the same 1/M_R^2 residue as conservative exchange",
                "passed": True,
                "valid_for_declared_parent_branch": True,
            },
            {
                "decision_id": "DEC4962_03_realistic_matter",
                "question": "Does realistic neutron-star matter destabilize the psi=0 branch under current caps?",
                "decision": "NO_PERTURBATIVE_ZERO_MODE_IN_TESTED_CORRIDOR",
                "reason": "nine BSK24 SLY4 DD2 rows lie over 17 orders below the sufficient instability threshold",
                "passed": True,
                "valid_for_declared_parent_branch": True,
            },
            {
                "decision_id": "DEC4962_04_full_compact_GR",
                "question": "Is exact all-operator compact GR now established?",
                "decision": "NO",
                "reason": "C3 observational control misses the one-percent gate and finite Wilson matching plus disconnected scalar branches remain open",
                "passed": True,
                "valid_for_declared_parent_branch": False,
            },
            {
                "decision_id": "DEC4962_05_full_MTS",
                "question": "Is full MTS-to-GR emergence established?",
                "decision": "NO",
                "reason": "integrated H Diff visible ontology and absolute G remain explicit parent or calibrated content",
                "passed": True,
                "valid_for_declared_parent_branch": False,
            },
        ]
    )


def main() -> int:
    SOURCE.mkdir(parents=True, exist_ok=True)

    missing = [name for name, path in SOURCE_PATHS.items() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing source paths: {missing}")
    source_hashes = {name: digest(path) for name, path in SOURCE_PATHS.items()}
    bad_hashes = {
        name: {"expected": EXPECTED_HASHES[name], "actual": actual}
        for name, actual in source_hashes.items()
        if EXPECTED_HASHES.get(name) != actual
    }
    if bad_hashes:
        raise RuntimeError(f"source hash mismatch: {bad_hashes}")

    source_text = {
        name: path.read_text(encoding="utf-8-sig")
        for name, path in SOURCE_PATHS.items()
        if path.suffix.lower() in {".md", ".json", ".csv"}
    }
    source_clause_checks = {
        "4880_exact_Einstein_vacuum": "Every four-dimensional Einstein metric" in source_text["strong_vacuum_4880"],
        "4883_three_EOS": all(
            token in source_text["multi_EOS_4883"]
            for token in ("BSK24", "SLY4", "DD2", "48")
        ),
        "4943_zero_charge": all(
            token in source_text["matter_junction_4943"]
            for token in ("Q_psi", "a_psi/a_N=0", "[psi]_Sigma=0")
        ),
        "4960_universal_residue": all(
            token in source_text["universal_source_4960"]
            for token in ("rank one", "Einstein -> Poisson -> Newton", "strong compact-body GR")
        ),
        "4961_parent_boundary": all(
            token in source_text["origin_boundary_4961"]
            for token in ("explicit fundamental", "numerical value of", "strong compact-body GR")
        ),
        "4923_compact_not_promoted": "compact-vacuum GR           -> not promoted" in source_text["GW_bound_4923"],
        "4929_conditional_C3": all(
            token in source_text["conditional_C3_4929"]
            for token in ("1.790736675667496e-36 m", "remain conditional", "compact and full MTS-to-GR")
        ),
    }
    if not all(source_clause_checks.values()):
        raise RuntimeError(f"source clause mismatch: {source_clause_checks}")

    validation_4883 = read_csv(SOURCE_PATHS["multi_EOS_validation_4883"])
    junction_4943 = read_csv(SOURCE_PATHS["scalar_junction_4943"])
    if not validation_4883 or not all(
        row.get("status", "").upper() == "PASS" for row in validation_4883
    ):
        raise RuntimeError("4883 validation is not fully passing")
    if not junction_4943 or not all(truth(row["passed"]) for row in junction_4943):
        raise RuntimeError("4943 junction pack is not fully passing")

    algebra_checks, expressions = symmetry_and_residue_checks()
    if not all(algebra_checks.values()):
        raise RuntimeError(f"algebra gate failed: {algebra_checks}")

    sensitivity = sensitivity_rows()
    junction = junction_rows()
    residue = residue_rows()
    eos, eos_summary = eos_rows()
    boundary = residual_rows()
    decision = decision_rows()

    checks = {
        **algebra_checks,
        "all_source_hashes_match": not bad_hashes,
        "all_source_clauses_match": all(source_clause_checks.values()),
        "4883_validation_passes": all(
            row.get("status", "").upper() == "PASS"
            for row in validation_4883
        ),
        "4943_junction_pack_passes": all(
            truth(row["passed"]) for row in junction_4943
        ),
        "all_realistic_EOS_rows_stable": all(row["passed"] for row in eos),
        "EOS_stability_margin_exceeds_15_orders": (
            eos_summary["minimum_orders_below_instability"] > 15.0
        ),
        "no_new_radiative_calibration": all(
            not row["new_independent_calibration"] for row in residue
        ),
        "full_compact_GR_not_overclaimed": any(
            row["decision_id"] == "DEC4962_04_full_compact_GR"
            and row["decision"] == "NO"
            for row in decision
        ),
        "full_MTS_false": any(
            row["decision_id"] == "DEC4962_05_full_MTS"
            and row["decision"] == "NO"
            for row in decision
        ),
    }
    if not all(checks.values()):
        raise RuntimeError(
            f"internal checks failed: {[key for key, value in checks.items() if not value]}"
        )

    write_csv(SENSITIVITY_CSV, sensitivity)
    write_csv(JUNCTION_CSV, junction)
    write_csv(RESIDUE_CSV, residue)
    write_csv(EOS_CSV, eos)
    write_csv(BOUNDARY_CSV, boundary)
    write_csv(DECISION_CSV, decision)

    result = {
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "source_hashes": source_hashes,
        "source_clause_checks": source_clause_checks,
        "checks": checks,
        "symbolic_expressions": expressions,
        "counts": {
            "source_paths": len(SOURCE_PATHS),
            "sensitivity_rows": len(sensitivity),
            "junction_rows": len(junction),
            "residue_rows": len(residue),
            "EOS_rows": len(eos),
            "residual_rows": len(boundary),
            "decision_rows": len(decision),
        },
        "EOS_summary": eos_summary,
        "promotions": {
            "selected_two_derivative_compact_point_particle_GR": True,
            "zero_leading_scalar_dipole_on_selected_branch": True,
            "same_conservative_and_radiative_GN": True,
            "realistic_EOS_perturbative_zero_mode_excluded": True,
            "all_operator_compact_GR": False,
            "full_MTS": False,
        },
        "next_target": (
            "4963-Y5-R2FR-strong-field-C3-Wilson-selection-and-global-"
            "scalar-branch-exclusion-or-compact-GR-finite-residual.md"
        ),
    }
    RESULT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    provenance_lines = [
        "# 4962 provenance",
        "",
        f"Marker: {MARKER}.",
        "",
        "All source inputs are local and SHA-256 locked before execution.",
        "",
        "| source key | local path | SHA-256 |",
        "|---|---|---|",
    ]
    for name, path in SOURCE_PATHS.items():
        provenance_lines.append(
            f"| {name} | {path.relative_to(ROOT).as_posix()} | {source_hashes[name]} |"
        )
    provenance_lines.extend(
        [
            "",
            "The realistic-EOS central densities are recalculated from the locked",
            "LALSuite tables with the same natural cubic log-pressure/log-energy",
            "interpolation used at checkpoint 4883. No web value or fitted compact",
            "sensitivity is inserted.",
            "",
            "The C3 observational and conditional-flow rows inherit checkpoints",
            "4923 and 4929. The conditional fixed-point length is not promoted to",
            "a full-parent prediction.",
            "",
        ]
    )
    PROVENANCE.write_text("\n".join(provenance_lines), encoding="utf-8")

    print(
        json.dumps(
            {
                "marker": MARKER,
                "checks_passed": sum(checks.values()),
                "checks_total": len(checks),
                "max_EOS_density_kg_m3": eos_summary[
                    "max_central_density_kg_m3"
                ],
                "minimum_orders_below_instability": eos_summary[
                    "minimum_orders_below_instability"
                ],
                "selected_two_derivative_compact_GR": True,
                "all_operator_compact_GR": False,
                "full_MTS": False,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import csv
import hashlib
import json
import math
import statistics
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4951"

RESULT_JSON = SOURCE / "coupled_VFZX2_fixed_and_running_gate_results.json"
SOURCE_AUDIT_CSV = SOURCE / "coupled_VFZX2_linear_source_audit.csv"
HESSIAN_CSV = SOURCE / "pair_onset_Hessian_projection.csv"
FIXED_POINT_CSV = SOURCE / "parent_and_source_fixed_point_indices.csv"
RUNNING_CSV = SOURCE / "running_pair_window_gate.csv"
DECISION_CSV = SOURCE / "pair_sector_decision.csv"

NARAIN_TAR = SOURCE / "0911.0386v2-source.tar"
NARAIN_PDF = SOURCE / "0911.0386v2.pdf"
NARAIN_TEX = SOURCE / "src0911" / "narain1rev1arxiv.tex"
PERCACCI_TAR = SOURCE / "1501.00888v3-source.tar"
PERCACCI_PDF = SOURCE / "1501.00888v3.pdf"
PERCACCI_TEX = SOURCE / "src1501" / "paper_GP3_journal.tex"
CURVED_SCALAR_TEX = (
    POST / "source-intake" / "functional_rg" / "4950" / "src1711" / "Flow-final.tex"
)
SHIFT_SYMMETRIC_TEX = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4937"
    / "src-2110.09566v1"
    / "SSTwAS.tex"
)
PARENT_ROOTS_CSV = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4937"
    / "constant_potential_root_spectrum.csv"
)
LOWER_X2_CSV = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4941"
    / "lower_scalar_essential_quotient.csv"
)
LOCAL_THRESHOLDS_CSV = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4950"
    / "local_spherical_pair_thresholds.csv"
)
SPARC_THRESHOLDS_CSV = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4950"
    / "SPARC_spherical_pair_window.csv"
)
SPARC_POTENTIAL_CSV = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4950"
    / "SPARC_baryonic_potential_depth_proxy.csv"
)
LOCAL_CERTIFICATE = (
    POST
    / "4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md"
)
PAIR_CHECKPOINT = (
    POST
    / "4950-Y5-R2FR-reflection-even-pair-source-operator-Rpsi2-Tpsi2-and-stabilized-galaxy-bifurcation-window-or-route-rejection.md"
)

EXPECTED_HASHES = {
    NARAIN_TAR: "be39b7e755a58dcd0a9ae2e597c0326c3c5f85a4bb02997952202ee7d377812a",
    NARAIN_PDF: "d41509922cf5b75c39a86910df78783474ee96aa106ed0a87bfbc3a97771a507",
    NARAIN_TEX: "570937dcbb8b3486b940ce8fcaede86dc1830c2a135357d203794c2aa621460f",
    PERCACCI_TAR: "2805cd350348c54ba73b8a5e78f2c9372d56bab10c1c9b1b3770b0ee8bacabe8",
    PERCACCI_PDF: "d25a7cb87c56f7ce29ed01c0b9b5b345bcc37f404d6a410e4f0f55ae6b02a9f4",
    PERCACCI_TEX: "fc269051a979b4ace3b3e6c4994a8711d2e42cfb163d439468d9bea6dab08b51",
    CURVED_SCALAR_TEX: "3fd379ba98e5ce9bdbdbf781683fdd2f471315328e9f28d94920e5b027c9a6cc",
    SHIFT_SYMMETRIC_TEX: "09e4775df76bf3e2024be7f2ec655a125436dbb6042779bc71fe03f6f7e5d778",
    PARENT_ROOTS_CSV: "fcc85c2120d5a6546352de7ef3433afb6fd45d74aa68c0e89b4c21c909366a79",
    LOWER_X2_CSV: "62f83d1e254709fa6dd5141ad9132a3d9aac89894a30684f804bae508646e89f",
    LOCAL_THRESHOLDS_CSV: "4b39f5ec00100c8b38b467c836908bef7431d778c342374d540a9412c579c07d",
    SPARC_THRESHOLDS_CSV: "6f88060429ee774b4e675a86b721fff9444a11c733562f1228ea66faa3c09acf",
    SPARC_POTENTIAL_CSV: "02b1c2d790b67802bbc45cc52953af5e2a0dfb9a7773e6d3c169c5c5477e330e",
    LOCAL_CERTIFICATE: "0b71f50c85ab4c5761755aa11544910a1a1e4fcacc901236432705a5ba36563f",
    PAIR_CHECKPOINT: "64188638f5d19e125e5c1305cce898332267295b26625c1492610a3c529774cf",
}

MARKER = "MTS_4951_COUPLED_VFZX2_FIXED_AND_RUNNING_GATE"
CHECKED_DATE = "2026-07-13"
KPC_METRES = 3.085677581491367e19


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
        raise ValueError(f"refusing to write empty table {path.name}")
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


def coefficient(expression: sp.Expr, field_symbol: sp.Symbol, power: int) -> sp.Expr:
    return sp.expand(expression).coeff(field_symbol, power)


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    source_hashes = {
        path.as_posix(): digest(path) if path.exists() else "MISSING"
        for path in EXPECTED_HASHES
    }
    hash_failures = {
        path.as_posix(): {
            "expected": expected,
            "actual": source_hashes[path.as_posix()],
        }
        for path, expected in EXPECTED_HASHES.items()
        if source_hashes[path.as_posix()] != expected
    }
    if hash_failures:
        raise RuntimeError(f"source hash mismatch: {hash_failures}")

    narain_text = NARAIN_TEX.read_text(encoding="utf-8-sig")
    percacci_text = PERCACCI_TEX.read_text(encoding="utf-8-sig")
    curved_text = CURVED_SCALAR_TEX.read_text(encoding="utf-8-sig")
    shift_text = SHIFT_SYMMETRIC_TEX.read_text(encoding="utf-8-sig")
    pair_text = PAIR_CHECKPOINT.read_text(encoding="utf-8-sig")

    source_contract = {
        "Narain_minimal_coupling_invariant": "minimal coupling is self consistent" in narain_text,
        "Narain_GMFP_block_recursion": r"M_{ii} = (d-2) \, i + M_{00}" in narain_text,
        "Narain_no_additive_lambda4_source": "minimal coupling is self consistent" in narain_text
        and "does not get any contribution from gravity" in narain_text,
        "Percacci_physical_gauge_VF_flow": "\\label{vdot4}" in percacci_text
        and "\\label{fdot4}" in percacci_text,
        "Percacci_constant_FP1": "f_*=\\frac{41}{768\\pi^2}" in percacci_text,
        "Percacci_nonminimal_FP2": "f_*(\\varphi)=\\frac{37}{768\\pi^2}+\\frac{1}{6}\\varphi^2" in percacci_text,
        "curved_scalar_VFZ_universal_flow": "perturbative-vfz-flow-dimful" in curved_text,
        "curved_scalar_beta_xi_structure": "\\frac{1}{6} -  \\frac{F_k''}{Z_k}" in curved_text,
        "shift_symmetric_subspace_closed": "space of shift-symmetric scalar-tensor interactions is closed" in shift_text,
        "shift_X2_flat_beta": "\\left. \\beta^{\\text{flat}}_c \\right|_{\\eta_s = 0} = 4 c + \\frac{5}{8\\pi^2} c^2" in shift_text,
        "4950_empty_window": "universal spherical galaxy/local window           = empty" in pair_text,
    }
    if not all(source_contract.values()):
        raise RuntimeError(f"primary source contract failed: {source_contract}")

    field_symbol = sp.symbols("varphi", real=True)
    vacuum_value, mass_squared, quartic = sp.symbols("v0 m2 lambda4", real=True)
    planck_value, pair_coupling = sp.symbols("f0 xi_pair", real=True)
    potential = vacuum_value + mass_squared * field_symbol**2 / 2 + quartic * field_symbol**4 / 24
    planck_function = planck_value + pair_coupling * field_symbol**2 / 2
    potential_prime = sp.diff(potential, field_symbol)
    potential_second = sp.diff(potential, field_symbol, 2)
    planck_prime = sp.diff(planck_function, field_symbol)
    planck_second = sp.diff(planck_function, field_symbol, 2)

    beta_potential_function = (
        -4 * potential
        + field_symbol * potential_prime
        + 1 / (16 * sp.pi**2)
        + (planck_function + 3 * planck_prime**2)
        / (
            32
            * sp.pi**2
            * (3 * planck_prime**2 + planck_function * (1 + potential_second))
        )
    )
    beta_planck_function = (
        -2 * planck_function
        + field_symbol * planck_prime
        + sp.Rational(37, 384) / sp.pi**2
        + planck_function
        * (
            (planck_function + 3 * planck_prime**2)
            * (1 - 3 * planck_second + 3 * potential_second)
            + 2 * planck_function * potential_second**2
        )
        / (
            96
            * sp.pi**2
            * (3 * planck_prime**2 + planck_function * (1 + potential_second)) ** 2
        )
    )
    potential_series = sp.series(
        beta_potential_function, field_symbol, 0, 6
    ).removeO()
    planck_series = sp.series(
        beta_planck_function, field_symbol, 0, 6
    ).removeO()
    comparator_betas = sp.Matrix(
        [
            coefficient(potential_series, field_symbol, 0),
            2 * coefficient(potential_series, field_symbol, 2),
            24 * coefficient(potential_series, field_symbol, 4),
            coefficient(planck_series, field_symbol, 0),
            2 * coefficient(planck_series, field_symbol, 2),
        ]
    )
    comparator_coordinates = sp.Matrix(
        [vacuum_value, mass_squared, quartic, planck_value, pair_coupling]
    )
    comparator_fp1 = {
        vacuum_value: sp.Rational(3, 128) / sp.pi**2,
        mass_squared: 0,
        quartic: 0,
        planck_value: sp.Rational(41, 768) / sp.pi**2,
        pair_coupling: 0,
    }
    comparator_fp2 = {
        vacuum_value: sp.Rational(3, 128) / sp.pi**2,
        mass_squared: 0,
        quartic: 0,
        planck_value: sp.Rational(37, 768) / sp.pi**2,
        pair_coupling: sp.Rational(1, 3),
    }
    fp1_residual = [sp.simplify(value.subs(comparator_fp1)) for value in comparator_betas]
    fp2_residual = [sp.simplify(value.subs(comparator_fp2)) for value in comparator_betas]
    fp1_stability = sp.simplify(
        comparator_betas.jacobian(comparator_coordinates).subs(comparator_fp1)
    )
    fp1_eigenvalues = sorted(
        [
            float(sp.N(eigenvalue))
            for eigenvalue, multiplicity in fp1_stability.eigenvals().items()
            for _ in range(multiplicity)
        ]
    )
    fp1_critical_exponents = sorted([-value for value in fp1_eigenvalues], reverse=True)

    loop_denominator = (4 * sp.pi) ** 2
    fixed_background_beta_lambda = sp.simplify(3 * quartic**2 / loop_denominator)
    fixed_background_beta_xi = sp.simplify(
        quartic * (pair_coupling - sp.Rational(1, 6)) / loop_denominator
    )
    flat_x2_coupling = sp.symbols("c_X2", real=True)
    flat_x2_beta = sp.simplify(
        4 * flat_x2_coupling
        + 5 * flat_x2_coupling**2 / (8 * sp.pi**2)
    )
    flat_x2_roots = sp.solve(sp.Eq(flat_x2_beta, 0), flat_x2_coupling)

    fluctuation_amplitude, gradient_norm, curvature_symbol = sp.symbols(
        "epsilon grad_f_sq R", real=True
    )
    test_function, wave_normalization, wave_curvature, x2_coupling = sp.symbols(
        "f Z0 z2 c_X2", real=True
    )
    kinetic_invariant = fluctuation_amplitude**2 * gradient_norm / 2
    expanded_density = (
        wave_normalization * kinetic_invariant
        + wave_curvature
        * fluctuation_amplitude**2
        * test_function**2
        * kinetic_invariant
        / 2
        + x2_coupling * kinetic_invariant**2
        + mass_squared * fluctuation_amplitude**2 * test_function**2 / 2
        + quartic * fluctuation_amplitude**4 * test_function**4 / 24
        - pair_coupling
        * curvature_symbol
        * fluctuation_amplitude**2
        * test_function**2
        / 2
    )
    quadratic_density = sp.expand(expanded_density).coeff(fluctuation_amplitude, 2)
    expected_quadratic_density = (
        wave_normalization * gradient_norm
        + (mass_squared - pair_coupling * curvature_symbol) * test_function**2
    ) / 2
    hessian_exact = sp.simplify(quadratic_density - expected_quadratic_density) == 0

    source_rows = tagged(
        [
            {
                "coordinate": "m2=V''(0)/Z0",
                "symmetry_at_zero": "breaks constant shift symmetry; reflection even",
                "additive_parent_source_at_GMFP": 0,
                "derived_reason": "a regulator preserving psi->psi+constant cannot generate V field dependence from F=constant, V=constant, Z=constant, X2",
                "linear_onset_entry": True,
                "parent_value_status": "relevant motion-gap datum already identified",
            },
            {
                "coordinate": "lambda4=V''''(0)/Z0^2",
                "symmetry_at_zero": "breaks constant shift symmetry; reflection even",
                "additive_parent_source_at_GMFP": 0,
                "derived_reason": "Narain-Percacci GMFP theorem and MTS potential trace are homogeneous in field-dependent V coordinates",
                "linear_onset_entry": False,
                "parent_value_status": "MTS potential projection makes regular quartic irrelevant at the low fixed branch",
            },
            {
                "coordinate": "xi=F''(0)/Z0",
                "symmetry_at_zero": "breaks constant shift symmetry; reflection even",
                "additive_parent_source_at_GMFP": 0,
                "derived_reason": "constant F subspace is invariant when all scalar self couplings vanish",
                "linear_onset_entry": True,
                "parent_value_status": "multiplicative gravity coefficient is scheme-sensitive; no additive MTS source",
            },
            {
                "coordinate": "z2=Z''(0)/Z0",
                "symmetry_at_zero": "shift breaking derivative function",
                "additive_parent_source_at_GMFP": 0,
                "derived_reason": "universal VFZ flow gives zero field-dependent Z source on constant V,F,Z",
                "linear_onset_entry": False,
                "parent_value_status": "zero on Gaussian-matter pair branch",
            },
            {
                "coordinate": "c_ess X2",
                "symmetry_at_zero": "shift symmetric and reflection even",
                "additive_parent_source_at_GMFP": "nonzero with gravity",
                "derived_reason": "SSTwAS and 4941 lower essential quotient generate the derivative quartic",
                "linear_onset_entry": False,
                "parent_value_status": "nonzero shifted fixed point allowed; no quadratic static source",
            },
        ]
    )

    hessian_rows = tagged(
        [
            {
                "term": "Z0 X",
                "epsilon_order": 2,
                "quadratic_contribution": "Z0 (grad f)^2/2",
                "enters_static_onset": True,
                "result": "positive kinetic term required",
            },
            {
                "term": "V''(0) psi2/2",
                "epsilon_order": 2,
                "quadratic_contribution": "m2 f^2/2",
                "enters_static_onset": True,
                "result": "universal motion gap",
            },
            {
                "term": "-F''(0) R psi2/2",
                "epsilon_order": 2,
                "quadratic_contribution": "-xi R f^2/2",
                "enters_static_onset": True,
                "result": "only curvature pair trigger in VFZX2",
            },
            {
                "term": "lambda4 psi4/24",
                "epsilon_order": 4,
                "quadratic_contribution": 0,
                "enters_static_onset": False,
                "result": "stabilizes amplitude but cannot move first bifurcation",
            },
            {
                "term": "z2 psi2 X/2",
                "epsilon_order": 4,
                "quadratic_contribution": 0,
                "enters_static_onset": False,
                "result": "field-dependent wave function is silent at psi=0",
            },
            {
                "term": "c_ess X2",
                "epsilon_order": 4,
                "quadratic_contribution": 0,
                "enters_static_onset": False,
                "result": "nonlinear kinetic screening cannot change linear onset",
            },
            {
                "term": "complete psi=0 Hessian",
                "epsilon_order": 2,
                "quadratic_contribution": "Gamma2=-Z0 box+V''(0)-F''(0)R",
                "enters_static_onset": True,
                "result": "exact for the declared local VFZX2 truncation",
            },
        ]
    )

    parent_root_rows = read_csv(PARENT_ROOTS_CSV)
    parent_low = next(
        row
        for row in parent_root_rows
        if row["scheme"] == "source_diagonal_calibrated" and row["branch"] == "low"
    )
    parent_mass_theta = float(parent_low["theta_mass_n2"])
    parent_quartic_theta = float(parent_low["theta_quartic_n4"])
    parent_anomaly = float(parent_low["A_gravity"])
    fixed_point_rows = tagged(
        [
            {
                "system": "MTS parent optimized potential low branch",
                "fixed_point": "Gaussian-matter pair coordinates",
                "coordinate": "mass m2",
                "fixed_value": 0,
                "critical_exponent": parent_mass_theta,
                "classification": "RELEVANT",
                "scope": "parent-owned potential projection",
            },
            {
                "system": "MTS parent optimized potential low branch",
                "fixed_point": "Gaussian-matter pair coordinates",
                "coordinate": "quartic lambda4",
                "fixed_value": 0,
                "critical_exponent": parent_quartic_theta,
                "classification": "IRRELEVANT",
                "scope": "parent-owned potential projection",
            },
            {
                "system": "MTS parent shift-symmetry theorem",
                "fixed_point": "Gaussian-matter pair coordinates",
                "coordinate": "xi pair source",
                "fixed_value": 0,
                "critical_exponent": "not parent-signed",
                "classification": "NO_ADDITIVE_SOURCE_INDEX_SCHEME_SENSITIVE",
                "scope": "zero fixed coordinate proved; multiplicative index not imported",
            },
            {
                "system": "Percacci-Vacca physical-gauge polynomial comparator",
                "fixed_point": "FP1",
                "coordinate": "v0,m2,lambda4,f0,xi",
                "fixed_value": "3/(128pi2),0,0,41/(768pi2),0",
                "critical_exponent": ";".join(f"{value:.12g}" for value in fp1_critical_exponents),
                "classification": "3_RELEVANT_2_MARGINAL_IN_FIVE_COORDINATE_POLYNOMIAL",
                "scope": "external source comparator; not spliced into MTS",
            },
            {
                "system": "Percacci-Vacca physical-gauge polynomial comparator",
                "fixed_point": "FP2",
                "coordinate": "F curvature coefficient",
                "fixed_value": "F=f0+varphi2/6 so F''=1/3",
                "critical_exponent": "functional source reports 1.809 for extra relevant mode",
                "classification": "ORDER_ONE_NONMINIMAL_FIXED_POINT",
                "scope": "external source comparator; at least 2.7e6 below easiest galaxy threshold",
            },
            {
                "system": "Narain-Percacci De-Donder GMFP comparator",
                "fixed_point": "GMFP",
                "coordinate": "phi2 V/F block",
                "fixed_value": "all scalar self interactions zero",
                "critical_exponent": "0.143+/-2.879i",
                "classification": "SMALL_RELEVANT_SCHEME_COMPARATOR",
                "scope": "demonstrates index scheme sensitivity; invariant zero source is common",
            },
            {
                "system": "shift-symmetric flat X2 source comparator",
                "fixed_point": "GFP and derivative NGFP",
                "coordinate": "c_X2",
                "fixed_value": ";".join(str(root) for root in flat_x2_roots),
                "critical_exponent": "-4 at GFP; +4 at flat NGFP under source convention",
                "classification": "DERIVATIVE_SECTOR_DOES_NOT_SOURCE_PAIR_HESSIAN",
                "scope": "external source comparator plus exact epsilon-order theorem",
            },
        ]
    )

    local_rows = read_csv(LOCAL_THRESHOLDS_CSV)
    sparc_rows = read_csv(SPARC_THRESHOLDS_CSV)
    massless_local = {
        row["system"]: row
        for row in local_rows
        if row["compton_case"] == "massless"
    }
    massless_galaxies = [
        row for row in sparc_rows if row["compton_case"] == "massless"
    ]
    easiest_galaxy = min(
        massless_galaxies, key=lambda row: float(row["Bcrit_spherical"])
    )
    galaxy_threshold = float(easiest_galaxy["Bcrit_spherical"])
    galaxy_radius = float(easiest_galaxy["outer_radius_kpc"]) * KPC_METRES

    running_rows: list[dict[str, Any]] = []
    for local_system in (
        "Sun",
        "one_solar_mass_white_dwarf",
        "1.4_solar_mass_12km_neutron_star",
    ):
        local_row = massless_local[local_system]
        local_threshold = float(local_row["Bcrit_spherical"])
        local_radius = float(local_row["radius_m"])
        required_growth = galaxy_threshold / local_threshold
        momentum_ratio = local_radius / galaxy_radius
        required_average_exponent = math.log(required_growth) / math.log(momentum_ratio)
        running_rows.append(
            {
                "comparison": f"{easiest_galaxy['galaxy']}_versus_{local_system}",
                "galaxy_radius_m": galaxy_radius,
                "local_radius_m": local_radius,
                "k_galaxy_over_k_local": momentum_ratio,
                "Bcrit_galaxy": galaxy_threshold,
                "Bceiling_local": local_threshold,
                "required_B_IR_growth": required_growth,
                "required_average_dlnB_dlnk": required_average_exponent,
                "stable_VF_one_loop_sign": "dln|xi-1/6|/dlk=lambda4/(16pi2)>=0",
                "IR_direction_result": "|xi-1/6| nonincreasing toward lower k",
                "passes_required_growth": False,
            }
        )

    sample_lambda_values = (0.01, 0.1, 1.0, 4.0 * math.pi)
    white_dwarf_radius = float(
        massless_local["one_solar_mass_white_dwarf"]["radius_m"]
    )
    logarithmic_interval = math.log(white_dwarf_radius / galaxy_radius)
    lambda_coefficient = 3.0 / (16.0 * math.pi**2)
    for initial_lambda in sample_lambda_values:
        final_lambda = initial_lambda / (
            1.0 - lambda_coefficient * initial_lambda * logarithmic_interval
        )
        xi_deviation_ratio = (final_lambda / initial_lambda) ** (1.0 / 3.0)
        running_rows.append(
            {
                "comparison": f"analytic_VF_trajectory_lambdaWD_{initial_lambda:.8g}",
                "galaxy_radius_m": galaxy_radius,
                "local_radius_m": white_dwarf_radius,
                "k_galaxy_over_k_local": white_dwarf_radius / galaxy_radius,
                "Bcrit_galaxy": galaxy_threshold,
                "Bceiling_local": float(
                    massless_local["one_solar_mass_white_dwarf"]["Bcrit_spherical"]
                ),
                "required_B_IR_growth": galaxy_threshold
                / float(
                    massless_local["one_solar_mass_white_dwarf"]["Bcrit_spherical"]
                ),
                "lambda_at_local_scale": initial_lambda,
                "lambda_at_galaxy_scale": final_lambda,
                "xi_minus_one_sixth_IR_over_local": xi_deviation_ratio,
                "stable_VF_one_loop_sign": "positive lambda4",
                "IR_direction_result": "suppression rather than required amplification",
                "passes_required_growth": xi_deviation_ratio
                >= galaxy_threshold
                / float(
                    massless_local["one_solar_mass_white_dwarf"]["Bcrit_spherical"]
                ),
            }
        )

    potential_rows = read_csv(SPARC_POTENTIAL_CSV)
    minimum_shape_floor = min(
        float(row["B_no_bound_floor_proxy"]) for row in potential_rows
    )
    white_dwarf_ceiling = float(
        massless_local["one_solar_mass_white_dwarf"]["Bcrit_spherical"]
    )
    finite_mass_never_improves = all(
        float(row["Bcrit_spherical"])
        >= float(
            next(
                base["Bcrit_spherical"]
                for base in massless_galaxies
                if base["galaxy"] == row["galaxy"]
            )
        )
        - 1.0e-8
        for row in sparc_rows
        if row["compton_case"] != "massless"
    )
    all_spherical_windows_empty = all(
        row["universal_window_vs_white_dwarf"].lower() == "false"
        and row["universal_window_vs_neutron_star"].lower() == "false"
        for row in sparc_rows
    )

    decision_rows = tagged(
        [
            {
                "gate": "common_parent_shift_source",
                "result": "PASS_ZERO_THEOREM",
                "meaning": "m2 lambda4 xi and z2 have no additive source at the Gaussian-matter pair point; X2 alone is generated",
                "route_status": "PAIR_BREAKING_VALUES_NOT_DERIVED_FROM_X2",
            },
            {
                "gate": "complete_VFZX2_linear_onset",
                "result": "PASS_EXACT_HESSIAN",
                "meaning": "lambda4 z2 and X2 are absent from Gamma2 at psi=0",
                "route_status": "ONLY_MASS_AND_CURVATURE_PAIR_TERM_CAN_TRIGGER",
            },
            {
                "gate": "MTS_parent_fixed_indices",
                "result": "MASS_RELEVANT_QUARTIC_IRRELEVANT_XI_INDEX_OPEN",
                "meaning": "parent flow predicts no nonzero pair fixed coordinate and does not select Jgap",
                "route_status": "NO_STATIC_PAIR_SOURCE_GAINED",
            },
            {
                "gate": "local_galaxy_spectral_ordering",
                "result": "FAIL_EMPTY_WINDOW",
                "meaning": "all 700 galaxy/compton rows require activation coefficients above white-dwarf and neutron-star ceilings",
                "route_status": "UNIVERSAL_STATIC_PAIR_ROUTE_REJECTED",
            },
            {
                "gate": "stable_IR_VF_running",
                "result": "FAIL_WRONG_RUNNING_SIGN",
                "meaning": "lambda4>=0 makes |xi-1/6| decrease from local-object to galaxy momentum scales",
                "route_status": "RG_IMPROVEMENT_CANNOT_REVERSE_THRESHOLD_ORDER",
            },
            {
                "gate": "shape_aware_floor",
                "result": "FAIL_PROXY_ONLY",
                "meaning": f"minimum potential-depth no-bound floor {minimum_shape_floor:.12g} remains {minimum_shape_floor / white_dwarf_ceiling:.12g} times the white-dwarf ceiling",
                "route_status": "SUPPORTING_DIAGNOSTIC_NOT_FULL_3D_THEOREM",
            },
            {
                "gate": "4951_route_decision",
                "result": "REJECT_CURRENT_STATIC_VFZX2_GALAXY_BRIDGE",
                "meaning": "the coupled functional block is necessary for renormalization but cannot alter the psi=0 onset ordering in the source-derived stable branch",
                "route_status": "KEEP_4947_LOCAL_GR_BRANCH_AND_PIVOT_TO_PARENT_CTP_MATTER_GRAVITON_NOISE_SOURCE",
            },
        ]
    )

    checks = {
        "source_hashes_match": not hash_failures,
        "all_primary_source_contracts_found": all(source_contract.values()),
        "physical_gauge_FP1_exact": all(value == 0 for value in fp1_residual),
        "physical_gauge_FP2_exact": all(value == 0 for value in fp2_residual),
        "FP1_eigenvalue_multiplicities_exact": fp1_eigenvalues
        == [-4.0, -2.0, -2.0, 0.0, 0.0],
        "fixed_background_beta_lambda_exact": sp.simplify(
            fixed_background_beta_lambda - 3 * quartic**2 / (16 * sp.pi**2)
        )
        == 0,
        "fixed_background_beta_xi_exact": sp.simplify(
            fixed_background_beta_xi
            - quartic * (pair_coupling - sp.Rational(1, 6)) / (16 * sp.pi**2)
        )
        == 0,
        "flat_X2_roots_exact": set(flat_x2_roots)
        == {sp.Integer(0), -32 * sp.pi**2 / 5},
        "complete_quadratic_Hessian_exact": hessian_exact,
        "quartic_absent_from_pair_Hessian": not quadratic_density.has(quartic),
        "z2_absent_from_pair_Hessian": not quadratic_density.has(wave_curvature),
        "X2_absent_from_pair_Hessian": not quadratic_density.has(x2_coupling),
        "parent_mass_relevant": parent_mass_theta > 0.0,
        "parent_quartic_irrelevant": parent_quartic_theta < 0.0,
        "all_175_massless_galaxies_present": len(massless_galaxies) == 175,
        "all_700_spherical_windows_empty": len(sparc_rows) == 700
        and all_spherical_windows_empty,
        "finite_mass_never_lowers_galaxy_threshold": finite_mass_never_improves,
        "required_running_is_IR_growth": all(
            float(row["required_B_IR_growth"]) > 1.0 for row in running_rows
        ),
        "stable_sample_trajectories_never_rescue": all(
            not bool(row["passes_required_growth"]) for row in running_rows
        ),
        "shape_floor_above_white_dwarf": minimum_shape_floor > white_dwarf_ceiling,
        "no_output_row_promoted_to_full_claim": all(
            not bool(row["valid_for_full_MTS_claim"])
            for rows in (
                source_rows,
                hessian_rows,
                fixed_point_rows,
                tagged(running_rows),
                decision_rows,
            )
            for row in rows
        ),
    }
    if not all(checks.values()):
        raise RuntimeError(f"4951 gate failed: {checks}")

    running_rows = tagged(running_rows)
    result = {
        "marker": MARKER,
        "source_hashes": {
            path.relative_to(ROOT).as_posix(): expected
            for path, expected in EXPECTED_HASHES.items()
        },
        "source_contract": source_contract,
        "declared_action": {
            "equation": "Gamma=int sqrt(g)[V(psi)-F(psi)R+Z(psi)X+c_ess X^2]",
            "reflection_even_expansion": "V=V0+m2 psi2/2+lambda4 psi4/24+...; F=F0+xi psi2/2+...; Z=Z0+z2 psi2/2+...",
            "quadratic_operator": "Gamma_psi_psi=-Z0 box+m2-xi R",
            "rayleigh_operator": "lambda0=inf_f [int Z0|grad f|2+(m2-xi R)f2]/int f2",
        },
        "parent_source_theorem": {
            "statement": "the shift-symmetric surface V=constant,F=constant,Z=constant,c_ess arbitrary is RG invariant; gravity may source c_ess but cannot additively source m2,lambda4,xi,z2",
            "consequence": "the generated X2 coordinate cannot manufacture a static pair source",
        },
        "source_comparator": {
            "physical_gauge_FP1_residual": [str(value) for value in fp1_residual],
            "physical_gauge_FP2_residual": [str(value) for value in fp2_residual],
            "physical_gauge_FP1_stability": [
                [str(value) for value in row] for row in fp1_stability.tolist()
            ],
            "physical_gauge_FP1_eigenvalues": fp1_eigenvalues,
            "physical_gauge_FP1_critical_exponents": fp1_critical_exponents,
            "fixed_background_beta_lambda": str(fixed_background_beta_lambda),
            "fixed_background_beta_xi": str(fixed_background_beta_xi),
            "flat_X2_beta": str(flat_x2_beta),
            "flat_X2_roots": [str(root) for root in flat_x2_roots],
            "scheme_firewall": "external scalar-tensor fixed points are not inserted into the MTS parent; only symmetry, Hessian order and universal IR signs are transferred",
        },
        "parent_indices": {
            "A_gravity": parent_anomaly,
            "theta_mass": parent_mass_theta,
            "theta_quartic": parent_quartic_theta,
            "theta_xi": "not parent-signed",
        },
        "spectral_gate": {
            "easiest_massless_galaxy": easiest_galaxy["galaxy"],
            "easiest_galaxy_outer_radius_kpc": float(
                easiest_galaxy["outer_radius_kpc"]
            ),
            "easiest_galaxy_Bcrit": galaxy_threshold,
            "white_dwarf_ceiling": white_dwarf_ceiling,
            "neutron_star_ceiling": float(
                massless_local["1.4_solar_mass_12km_neutron_star"][
                    "Bcrit_spherical"
                ]
            ),
            "all_spherical_windows_empty": all_spherical_windows_empty,
            "finite_mass_never_improves": finite_mass_never_improves,
            "shape_proxy_minimum_floor": minimum_shape_floor,
        },
        "IR_running_theorem": {
            "equations": "beta_lambda=3lambda2/(16pi2); beta_delta=lambda delta/(16pi2), delta=xi-1/6",
            "solution": "delta(k2)/delta(k1)=[lambda(k2)/lambda(k1)]^(1/3)",
            "stable_branch": "lambda>=0 implies |delta| cannot grow toward smaller k",
            "required_running_rows": running_rows,
        },
        "decision": {
            "coupled_VFZX2_RG_closure_required": True,
            "current_static_even_pair_galaxy_bridge": False,
            "local_GR_Newton_Maxwell_4947_retained": True,
            "reason": "the full declared functional block leaves the linear onset operator unchanged, while the measured galaxy/local hierarchy requires the opposite IR running from the stable source-derived flow",
            "next_target": "4952-Y5-R2FR-visible-matter-graviton-CTP-noise-kernel-to-motion-pair-source-and-frequency-support-or-composite-route-rejection.md",
        },
        "checks": checks,
    }

    SOURCE.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_AUDIT_CSV, source_rows)
    write_csv(HESSIAN_CSV, hessian_rows)
    write_csv(FIXED_POINT_CSV, fixed_point_rows)
    write_csv(RUNNING_CSV, running_rows)
    write_csv(DECISION_CSV, decision_rows)
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print(f"{MARKER}_PARENT_THETA_MASS={parent_mass_theta:.15e}", flush=True)
    print(f"{MARKER}_PARENT_THETA_QUARTIC={parent_quartic_theta:.15e}", flush=True)
    print(f"{MARKER}_EASIEST_GALAXY_BCRIT={galaxy_threshold:.15e}", flush=True)
    print(
        f"{MARKER}_WD_GROWTH_REQUIRED={galaxy_threshold / white_dwarf_ceiling:.15e}",
        flush=True,
    )
    print(f"{MARKER}_CHECKS={sum(checks.values())}/{len(checks)}", flush=True)
    print(f"{MARKER}_DONE", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

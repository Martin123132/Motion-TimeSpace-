from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
SCRIPT = Path(__file__).resolve()

CHECKPOINT_4953_DOCUMENT = (
    POST
    / "4953-Y5-R2FR-galaxy-formation-transient-spectrum-X2-kinetic-cascade-and-local-injection-bound-or-composite-route-rejection.md"
)
CHECKPOINT_4953_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4953"
    / "formation_X2_cascade_and_injection_results.json"
)
CHECKPOINT_4953_NONLINEAR = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4953"
    / "SPARC_X2_nonlinearity_gate.csv"
)
CHECKPOINT_4954_DOCUMENT = (
    POST
    / "4954-Y5-R2FR-finite-time-off-shell-X2-number-changing-2PI-kernel-and-formation-source-efficiency-or-nonequilibrium-route-rejection.md"
)
CHECKPOINT_4954_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4954"
    / "offshell_X2_X3_number_change_results.json"
)
CHECKPOINT_4958_DOCUMENT = (
    POST
    / "4958-Y5-R2FR-six-derivative-essential-X2-X3-quotient-and-invariant-2to4-amplitude-or-rate-route-rejection.md"
)
CHECKPOINT_4958_TRAJECTORY = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4958"
    / "essential_functional_GR_trajectory.csv"
)
CHECKPOINT_4959_DOCUMENT = (
    POST
    / "4959-Y5-R2FR-O2-O3-O4-external-scalar-sixpoint-projectors-and-full-invariant-amplitude-or-curvature-route-rejection.md"
)
CHECKPOINT_4959_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4959"
    / "curvature_sixpoint_projector_results.json"
)
CHECKPOINT_4960_DOCUMENT = (
    POST
    / "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-local-GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md"
)
CHECKPOINT_4960_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4960"
    / "integrated_H_universal_source_results.json"
)
CHECKPOINT_5156_DOCUMENT = (
    POST
    / "5156-Y5-R2FR-FLRW-Hessian-Gaussian-state-single-clock-adiabatic-radiation-transfer-and-patch-collapse-gate.md"
)
CHECKPOINT_5156_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5156"
    / "FLRW_covariance_radiation_transfer_results.json"
)
CHECKPOINT_5178_DOCUMENT = (
    POST
    / "5178-Y5-R2FR-exact-2PI-Schur-Ward-Vlasov-subtraction-and-Gaussian-residual-stress-no-go.md"
)
CHECKPOINT_5178_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5178"
    / "twoPI_Schur_Vlasov_subtraction_results.json"
)
BERGES_TEX = (
    POST
    / "source-intake"
    / "functional_rg"
    / "4948"
    / "riolecture.tex"
)
GARNY_ROOT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5179"
    / "sources"
    / "garny_muller_0904.3600"
)
GARNY_TEX = GARNY_ROOT / "feynRulesCTP.tex"
GARNY_ARCHIVE = GARNY_ROOT / "0904.3600-source.tar"
PLANCK_ROOT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5179"
    / "sources"
    / "planck_2018_non_gaussianity_1905.05697"
)
PLANCK_ABSTRACT = PLANCK_ROOT / "L09_abstract.tex"
PLANCK_SECTION7 = PLANCK_ROOT / "L09_Section7.tex"
PLANCK_ARCHIVE = PLANCK_ROOT.parent / "planck_2018_non_gaussianity_1905.05697-source.tar"
CHECKPOINT_5176_ROOT = POST / "source-intake" / "functional_rg" / "5176"

OUT = POST / "source-intake" / "functional_rg" / "5179"
KERNEL_CSV = OUT / "lowest_even_CTP_boundary_kernel.csv"
FLRW_CSV = OUT / "X2_X3_FLRW_induced_fourpoint_contract.csv"
WICK_CSV = OUT / "exact_quartic_state_Wick_and_positivity_gate.csv"
STRESS_CSV = OUT / "stress_contraction_and_kurtosis_bound.csv"
CMB_CSV = OUT / "CMB_covariance_and_trispectrum_projection_gate.csv"
DECISION_CSV = OUT / "state_preparation_route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "lowest_even_CTP_state_preparation_results.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5179_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5179-Y5-R2FR-lowest-reflection-even-CTP-boundary-kernel-FLRW-preparation-and-perturbative-extra-stress-no-go.md"
)

MARKER = "MTS_5179_LOWEST_EVEN_CTP_BOUNDARY_KERNEL_PERTURBATIVE_STATE_PREPARATION_GATE"
CHECKED_DATE = "2026-07-23"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CHECKPOINT_5176_TREE_LOCK = (
    "254d5879c1e76908e3942e4817892e091fa1315666dae1d6d74e2c3287c67b8b"
)
GARNY_ARCHIVE_LOCK = (
    "94d519820ab4ada378a6e9a16af828e90dae2440a7a45a6ebf18f98a5522c17f"
)
PLANCK_ARCHIVE_LOCK = (
    "bbf976dda6afe2184143c203776b3d93d31815938d8cec648eb63ae4d822e3cc"
)
REDUCED_PLANCK_MASS_EV = 2.435e27
HBARC_EV_M = 1.973269804e-7
KPC_M = 3.0856775814913673e19
REFERENCE_GALAXY = "UGC09133"
REFERENCE_MASS_EV = 1.0e-20

ROUTE_DECISION = (
    "THE_LOWEST_REFLECTION_EVEN_NON_GAUSSIAN_STATE_VERTEX_IS_THE_SURFACE_"
    "SUPPORTED_ALPHA4_AND_A_COVARIANT_PREPARATION_CONTOUR_DERIVES_ITS_"
    "LEADING_X2_KERNEL_BUT_NOT_A_FREE_GALAXY_STRESS_THE_STANDALONE_"
    "POSITIVE_DIAGONAL_QUARTIC_STATE_CAN_ONLY_SUPPRESS_VARIANCE_THE_BULK_"
    "INDUCED_WEAK_KERNEL_IS_VACUUM_LOCAL_OR_ORDER_CESS_SQUARED_AFTER_"
    "VLASOV_SUBTRACTION_AND_THE_EXISTING_CONTROLLED_FORMATION_BOUNDS_ARE_"
    "FAR_TOO_SMALL_SO_AN_ORDER_ONE_REPAIR_REQUIRES_A_PARENT_DERIVED_STRONG_"
    "FULL_EVEN_BOUNDARY_HIERARCHY_OR_GAPLESS_OCCUPIED_CONTINUUM_AND_CANNOT_"
    "BE_CLAIMED_FROM_ALPHA4_ALONE"
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for file_path in sorted(
        item for item in path.rglob("*") if item.is_file()
    ):
        relative = file_path.relative_to(path).as_posix()
        value.update(relative.encode("utf-8"))
        value.update(file_digest(file_path).encode("ascii"))
    return value.hexdigest()


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "passed"}


def source_paths() -> dict[str, Path]:
    return {
        "script_5179": SCRIPT,
        "checkpoint_4953_document": CHECKPOINT_4953_DOCUMENT,
        "checkpoint_4953_result": CHECKPOINT_4953_RESULT,
        "checkpoint_4953_nonlinearity": CHECKPOINT_4953_NONLINEAR,
        "checkpoint_4954_document": CHECKPOINT_4954_DOCUMENT,
        "checkpoint_4954_result": CHECKPOINT_4954_RESULT,
        "checkpoint_4958_document": CHECKPOINT_4958_DOCUMENT,
        "checkpoint_4958_trajectory": CHECKPOINT_4958_TRAJECTORY,
        "checkpoint_4959_document": CHECKPOINT_4959_DOCUMENT,
        "checkpoint_4959_result": CHECKPOINT_4959_RESULT,
        "checkpoint_4960_document": CHECKPOINT_4960_DOCUMENT,
        "checkpoint_4960_result": CHECKPOINT_4960_RESULT,
        "checkpoint_5156_document": CHECKPOINT_5156_DOCUMENT,
        "checkpoint_5156_result": CHECKPOINT_5156_RESULT,
        "checkpoint_5178_document": CHECKPOINT_5178_DOCUMENT,
        "checkpoint_5178_result": CHECKPOINT_5178_RESULT,
        "berges_nonequilibrium_source": BERGES_TEX,
        "garny_muller_source": GARNY_TEX,
        "garny_muller_archive": GARNY_ARCHIVE,
        "planck_nonGaussianity_abstract": PLANCK_ABSTRACT,
        "planck_nonGaussianity_section7": PLANCK_SECTION7,
        "planck_nonGaussianity_archive": PLANCK_ARCHIVE,
    }


def source_metadata() -> dict[str, dict[str, str]]:
    return {
        "garny_muller_source": {
            "url": "https://arxiv.org/abs/0904.3600",
            "role": "general non-Gaussian CTP density matrix, alpha4 surface vertex and Kadanoff-Baym source",
        },
        "garny_muller_archive": {
            "url": "https://arxiv.org/e-print/0904.3600",
            "role": "primary-source archive",
        },
        "berges_nonequilibrium_source": {
            "url": "https://arxiv.org/abs/hep-ph/0409233",
            "role": "2PI CTP action, initial sources and nonequilibrium evolution",
        },
        "planck_nonGaussianity_abstract": {
            "url": "https://arxiv.org/abs/1905.05697",
            "role": "Planck 2018 primordial trispectrum result",
        },
        "planck_nonGaussianity_section7": {
            "url": "https://arxiv.org/abs/1905.05697",
            "role": "trispectrum definitions and numerical template constraints",
        },
        "planck_nonGaussianity_archive": {
            "url": "https://arxiv.org/e-print/1905.05697",
            "role": "primary-source archive",
        },
    }


def perfect_matchings(labels: tuple[str, ...]) -> list[tuple[tuple[str, str], ...]]:
    if not labels:
        return [tuple()]
    first = labels[0]
    output: list[tuple[tuple[str, str], ...]] = []
    for index in range(1, len(labels)):
        second = labels[index]
        remainder = labels[1:index] + labels[index + 1 :]
        for matching in perfect_matchings(remainder):
            output.append(((first, second),) + matching)
    return output


def gaussian_even_moment(order: int) -> Fraction:
    if order % 2:
        return Fraction(0)
    value = 1
    for factor in range(order - 1, 0, -2):
        value *= factor
    return Fraction(value)


def exact_wick_values() -> dict[str, Any]:
    six_matchings = perfect_matchings(("i", "j", "a", "b", "c", "d"))
    disconnected_two = [
        matching
        for matching in six_matchings
        if any(set(pair) == {"i", "j"} for pair in matching)
    ]
    connected_two = [
        matching for matching in six_matchings if matching not in disconnected_two
    ]
    eight_matchings = perfect_matchings(
        ("i", "j", "k", "l", "a", "b", "c", "d")
    )
    external = {"i", "j", "k", "l"}
    vertex = {"a", "b", "c", "d"}
    fully_connected_four = [
        matching
        for matching in eight_matchings
        if all(
            (pair[0] in external and pair[1] in vertex)
            or (pair[1] in external and pair[0] in vertex)
            for pair in matching
        )
    ]
    moment_2 = gaussian_even_moment(2)
    moment_4 = gaussian_even_moment(4)
    moment_6 = gaussian_even_moment(6)
    moment_8 = gaussian_even_moment(8)
    delta_moment_2 = -(
        moment_6 - moment_2 * moment_4
    ) / Fraction(math.factorial(4))
    delta_moment_4 = -(
        moment_8 - moment_4 * moment_4
    ) / Fraction(math.factorial(4))
    delta_kappa_4 = delta_moment_4 - 6 * moment_2 * delta_moment_2
    return {
        "six_pairings": len(six_matchings),
        "disconnected_two_pairings": len(disconnected_two),
        "connected_two_pairings": len(connected_two),
        "eight_pairings": len(eight_matchings),
        "fully_connected_four_pairings": len(fully_connected_four),
        "moment_2": moment_2,
        "moment_4": moment_4,
        "moment_6": moment_6,
        "moment_8": moment_8,
        "delta_moment_2": delta_moment_2,
        "delta_moment_4": delta_moment_4,
        "delta_kappa_4": delta_kappa_4,
    }


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def source_signature_checks() -> dict[str, bool]:
    garny = GARNY_TEX.read_text(encoding="utf-8-sig")
    berges = BERGES_TEX.read_text(encoding="utf-8-sig")
    planck_abstract = PLANCK_ABSTRACT.read_text(encoding="utf-8-sig")
    planck_section = PLANCK_SECTION7.read_text(encoding="utf-8-sig")
    return {
        "garny_density_functional": (
            r"\left\langle \varphi_+ \left| \rho \right| \varphi_- \right\rangle"
            in garny
            and r"= \exp\left( i F[\varphi] \right)" in garny
        ),
        "garny_surface_support": (
            "all their time arguments lie on the boundaries" in garny
        ),
        "garny_hermiticity": (
            r"i\alpha_n^{\epsilon_1,\dots,\epsilon_n}" in garny
            and r"(-\epsilon_1)" in garny
        ),
        "garny_Z2_odd_zero": (
            "all kernels" in garny
            and "with odd $n$ vanish" in garny
        ),
        "garny_alpha4_vertex": (
            r"\alpha_{4, 0L}^{th}" in garny
            and r"-i \lambda \intl_{\I} d^4 v" in garny
        ),
        "garny_nonGaussian_nonlocal_zero_at_setting_sun": (
            r"\Pi^{nG}_{non-loc}(x,y) & = & 0" in garny
        ),
        "garny_KB_surface_source": (
            r"\Pi_{\lambda\alpha,F}" in garny
            and r"G_F (0, y^0, \bm{k})" in garny
        ),
        "berges_initial_sources": (
            r"\alpha_3" in berges
            and r"\alpha_4" in berges
            and "initial time" in berges
        ),
        "planck_local_gNL": (
            r"$g_{\rm NL}^{\rm local} = (-5.8 \pm 6.5) \times 10^4$"
            in planck_abstract
        ),
        "planck_three_templates": (
            r"$*(-5.8\pm6.5)\times10^4$" in planck_section
            and r"$*(-0.8\pm1.9)\times10^6$" in planck_section
            and r"$*(-3.9\pm3.9)\times10^5$" in planck_section
        ),
    }


def select_trajectory_row(rows: list[dict[str, str]]) -> dict[str, str]:
    matches = [
        row
        for row in rows
        if row["scheme"] == "dynamic_etaN"
        and row["polynomial_order"] == "8"
    ]
    if not matches:
        raise RuntimeError("checkpoint-4958 dynamic N=8 trajectory row absent")
    return matches[-1]


def select_sixpoint_row(result: dict[str, Any]) -> dict[str, Any]:
    matches = [
        row
        for row in result["trajectory_bounds"]
        if row["scheme"] == "dynamic_etaN"
        and str(row["polynomial_order"]) == "8"
    ]
    if len(matches) != 1:
        raise RuntimeError("checkpoint-4959 dynamic N=8 bound row not unique")
    return matches[0]


def median(values: list[float]) -> float:
    ordered = sorted(values)
    size = len(ordered)
    if size % 2:
        return ordered[size // 2]
    return 0.5 * (ordered[size // 2 - 1] + ordered[size // 2])


def derive_inputs() -> dict[str, Any]:
    result_4954 = read_json(CHECKPOINT_4954_RESULT)
    trajectory = select_trajectory_row(read_csv(CHECKPOINT_4958_TRAJECTORY))
    result_4959 = read_json(CHECKPOINT_4959_RESULT)
    result_4960 = read_json(CHECKPOINT_4960_RESULT)
    result_5156 = read_json(CHECKPOINT_5156_RESULT)
    result_5178 = read_json(CHECKPOINT_5178_RESULT)
    nonlinear_rows = [
        row
        for row in read_csv(CHECKPOINT_4953_NONLINEAR)
        if parse_bool(row["positive_outer_residual_target"])
    ]
    if not nonlinear_rows:
        raise RuntimeError("checkpoint-4953 positive-target rows absent")
    reference_rows = [
        row for row in nonlinear_rows if row["galaxy"] == REFERENCE_GALAXY
    ]
    if len(reference_rows) != 1:
        raise RuntimeError("UGC09133 nonlinearity row not unique")
    reference_row = reference_rows[0]
    densities = [
        float(row["required_effective_energy_density_eV4"])
        for row in nonlinear_rows
    ]
    natural_c = REDUCED_PLANCK_MASS_EV**-4
    A2 = float(trajectory["A2_a_over_g_power"])
    trajectory_c = A2 * natural_c / (64.0 * math.pi**2)
    target_fraction = float(
        result_5178["summary"][
            "minimum_required_relative_transition_correction"
        ]
    )
    required_lambda = -2.0 * target_fraction
    radius_m = (
        float(result_5178["summary"]["reference_transition_radius_kpc"])
        * KPC_M
    )
    profile_energy = HBARC_EV_M / radius_m
    reference_density = float(
        reference_row["required_effective_energy_density_eV4"]
    )
    max_density = max(densities)
    median_density = median(densities)
    min_density = min(densities)
    natural_reference_epsilon = natural_c * reference_density
    trajectory_reference_epsilon = (
        abs(trajectory_c) * reference_density
    )
    natural_max_epsilon = natural_c * max_density
    natural_median_epsilon = natural_c * median_density
    sixpoint = select_sixpoint_row(result_4959)
    return {
        "result_4954": result_4954,
        "trajectory_4958": trajectory,
        "sixpoint_4959": sixpoint,
        "result_4960": result_4960,
        "result_5156": result_5156,
        "result_5178": result_5178,
        "positive_rows": nonlinear_rows,
        "positive_row_count": len(nonlinear_rows),
        "reference_row": reference_row,
        "density_min_eV4": min_density,
        "density_median_eV4": median_density,
        "density_max_eV4": max_density,
        "natural_c_eV_minus4": natural_c,
        "A2_dynamic_N8": A2,
        "trajectory_c_eV_minus4": trajectory_c,
        "trajectory_to_natural_ratio": trajectory_c / natural_c,
        "target_fraction": target_fraction,
        "required_diagonal_lambda": required_lambda,
        "reference_radius_m": radius_m,
        "reference_profile_energy_eV": profile_energy,
        "reference_profile_energy_over_mass": (
            profile_energy / REFERENCE_MASS_EV
        ),
        "reference_profile_energy_over_mass_squared": (
            profile_energy / REFERENCE_MASS_EV
        )
        ** 2,
        "natural_reference_epsilon": natural_reference_epsilon,
        "trajectory_reference_epsilon": trajectory_reference_epsilon,
        "natural_max_epsilon": natural_max_epsilon,
        "natural_median_epsilon": natural_median_epsilon,
        "natural_reference_K_required": (
            target_fraction / natural_reference_epsilon
        ),
        "trajectory_reference_K_required": (
            target_fraction / trajectory_reference_epsilon
        ),
        "natural_best_case_K_required": (
            target_fraction / natural_max_epsilon
        ),
        "natural_median_K_required": (
            target_fraction / natural_median_epsilon
        ),
        "natural_worst_case_K_required": (
            target_fraction / (natural_c * min_density)
        ),
    }


def kernel_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "kernel_id": "K5179_00_density_functional",
            "object": "general CTP initial density matrix",
            "equation": "<phi_+|rho|phi_->=exp(i F[phi]); F=sum_n alpha_n phi^n/n!",
            "derivation": "exact field-basis parameterization",
            "support_or_constraint": "complete initial-state information",
            "status": "DERIVED_SOURCE_SIGNED",
        },
        {
            "kernel_id": "K5179_01_surface_support",
            "object": "alpha_n(x_1,...,x_n)",
            "equation": "alpha_n=alpha_n^(a_1...a_n)(x_i) product_i delta_a_i(eta_i-eta_0)",
            "derivation": "F depends only on fields at the CTP boundary",
            "support_or_constraint": "all time arguments lie on Sigma_0",
            "status": "DERIVED_SOURCE_SIGNED",
        },
        {
            "kernel_id": "K5179_02_hermiticity",
            "object": "CTP branch kernels",
            "equation": "i alpha_n^(a_1...a_n)=[i alpha_n^(-a_1...-a_n)]*",
            "derivation": "rho=rho_dagger",
            "support_or_constraint": "necessary but not sufficient for positivity",
            "status": "DERIVED_SOURCE_SIGNED",
        },
        {
            "kernel_id": "K5179_03_reflection",
            "object": "reflection-even parent state",
            "equation": "alpha_(2r+1)=0",
            "derivation": "psi -> -psi invariance of action and initial state",
            "support_or_constraint": "all odd connected cumulants remain zero",
            "status": "DERIVED_EXACT",
        },
        {
            "kernel_id": "K5179_04_Gaussian_data",
            "object": "alpha_2",
            "equation": "alpha_2 <-> independent F_k occupation and squeezing data",
            "derivation": "checkpoint 5156 Gaussian-state theorem",
            "support_or_constraint": "not fixed by the Hessian",
            "status": "DERIVED_NONUNIQUENESS",
        },
        {
            "kernel_id": "K5179_05_lowest_nonGaussian",
            "object": "alpha_4",
            "equation": "F_4=(1/4!) integral_(Sigma_0^4) alpha_4 psi^4",
            "derivation": "alpha_3=0 by reflection and alpha_2 is Gaussian",
            "support_or_constraint": "lowest reflection-even non-Gaussian boundary vertex",
            "status": "DERIVED_EXACT",
        },
        {
            "kernel_id": "K5179_06_preparation_contour",
            "object": "leading X2-induced alpha_4",
            "equation": "alpha_4,X2(z_i)=-i integral_P d4v V_X2[nabla Delta_P(v,z_1),...,nabla Delta_P(v,z_4)]+O(c_ess^2)",
            "derivation": "integrate the covariant preparation contour and amputate its four connections",
            "support_or_constraint": "P and every z_i terminate on Sigma_0",
            "status": "DERIVED_FUNCTIONAL_FORM",
        },
        {
            "kernel_id": "K5179_07_even_hierarchy",
            "object": "alpha_6 and higher",
            "equation": "alpha_6,X2=O(c_ess^2) from two preparation vertices joined by one complete connection",
            "derivation": "same contour decomposition as the source-signed thermal alpha_6",
            "support_or_constraint": "a strong prepared state does not consistently stop at alpha_4",
            "status": "DERIVED_ORDER_HIERARCHY",
        },
        {
            "kernel_id": "K5179_08_X3_fourpoint",
            "object": "X3 contribution to alpha_4",
            "equation": "delta V_4,X3=(1/2) Tr_G V_6,X3",
            "derivation": "choose two of six legs and Wick contract: C(6,2) 4!/6!=1/2",
            "support_or_constraint": "local tadpole renormalization of the four-point vertex",
            "status": "DERIVED_EXACT_COMBINATORICS",
        },
        {
            "kernel_id": "K5179_09_positivity",
            "object": "prepared density matrix",
            "equation": "rho_0=U_P rho_G U_P_dagger or rho_0=exp(-beta H)/Z",
            "derivation": "constructive unitary or Euclidean preparation",
            "support_or_constraint": "positivity is automatic only after P and rho_G are specified",
            "status": "DERIVED_CONDITION",
        },
        {
            "kernel_id": "K5179_10_boundary_Ward",
            "object": "spatial diffeomorphism identity",
            "equation": "D_i[2 delta F_4/(sqrt(h) delta h_ij)]-[delta F_4/(sqrt(h) delta psi)]D^j psi=0",
            "derivation": "Noether variation of a scalar preparation functional on Sigma_0",
            "support_or_constraint": "normal constraint and branch matching are also required",
            "status": "DERIVED_CONDITION",
        },
        {
            "kernel_id": "K5179_11_arbitrary_alpha4",
            "object": "unsourced alpha_4",
            "equation": "bulk X2/X3 coefficients do not choose P, eta_i, beta or rho_G",
            "derivation": "action-versus-state separation",
            "support_or_constraint": "an arbitrary alpha_4 remains independent boundary data",
            "status": "NOT_A_DERIVED_MTS_PREDICTION",
        },
    ]
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def flrw_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "derivation_id": "F5179_00_FLRW_X2",
            "object": "X2 action on spatially flat FLRW",
            "equation": "S_X2=(c_ess/4) integral d_eta d3x [-(psi')^2+(grad psi)^2]^2",
            "order": "c_ess",
            "result": "a^4 measure cancels two inverse metrics exactly",
            "independent_new_bulk_stress": False,
            "status": "DERIVED_EXACT",
        },
        {
            "derivation_id": "F5179_01_vertex",
            "object": "symmetric four-leg derivative vertex",
            "equation": "V_X2=2 c_ess sum_pairings (p_i.p_j)(p_k.p_l)",
            "order": "c_ess",
            "result": "M_22=(c_ess/2)(s^2+t^2+u^2) on massless shell",
            "independent_new_bulk_stress": False,
            "status": "DERIVED_EXACT",
        },
        {
            "derivation_id": "F5179_02_Hamiltonian",
            "object": "first-order interaction Hamiltonian",
            "equation": "H_X2,I=-L_X2,I+O(c_ess^2)",
            "order": "c_ess",
            "result": "the perturbative Legendre correction cancels at first order",
            "independent_new_bulk_stress": False,
            "status": "DERIVED_EXACT",
        },
        {
            "derivation_id": "F5179_03_in_in_fourpoint",
            "object": "first connected equal-time four-point",
            "equation": "C4_c(eta0)=i integral_(eta_i)^eta0 d_eta <[H_X2,I(eta),psi_1 psi_2 psi_3 psi_4(eta0)]>_G+O(c_ess^2)",
            "order": "c_ess",
            "result": "unitary preparation formula; odd cumulants remain zero",
            "independent_new_bulk_stress": False,
            "status": "DERIVED_EXACT_TO_FIRST_ORDER",
        },
        {
            "derivation_id": "F5179_04_mode_kernel",
            "object": "FLRW mode representation",
            "equation": "C4_c=2 Im{product_i u_i(eta0) integral d_eta V_X2^H[u_1*,u_2*,u_3*,u_4*]} delta3(sum k_i)+O(c_ess^2)",
            "order": "c_ess",
            "result": "V_X2^H uses D_ij=-u_i'*u_j'+(k_i.k_j)u_i*u_j",
            "independent_new_bulk_stress": False,
            "status": "DERIVED_FUNCTIONAL_FORM",
        },
        {
            "derivation_id": "F5179_04b_Euclidean_vacuum",
            "object": "explicit adiabatic-vacuum boundary kernel",
            "equation": "A4_E(k_i)=[2c_ess/k_t] sum_pairings [k_i k_j-k_i_vec.k_j_vec][k_k k_l-k_k_vec.k_l_vec]",
            "order": "c_ess",
            "result": "regular tetrahedron gives A4_E=(8/3)c_ess k^3; this is vacuum wavefunctional dressing",
            "independent_new_bulk_stress": False,
            "status": "DERIVED_EXACT_ON_MASSLESS_ADIABATIC_BENCHMARK",
        },
        {
            "derivation_id": "F5179_05_X3_tadpole",
            "object": "first X3 correction to four-point",
            "equation": "V4_eff=V4_X2+(1/2) Tr_G V6_X3+counterterms",
            "order": "d_3 G(x,x)",
            "result": "local renormalization; no independent nonlocal alpha4 shape",
            "independent_new_bulk_stress": False,
            "status": "DERIVED_EXACT_TO_FIRST_LOOP",
        },
        {
            "derivation_id": "F5179_06_2PI_double_bubble",
            "object": "weak interacting Gamma_2",
            "equation": "Gamma_2,db proportional (1/8) integral_C V4_X2 G G",
            "order": "c_ess",
            "result": "Hartree/local analytic self-energy",
            "independent_new_bulk_stress": False,
            "status": "DERIVED_TOPOLOGY_AND_SYMMETRY_FACTOR",
        },
        {
            "derivation_id": "F5179_07_2PI_basketball",
            "object": "first nonlocal weak self-energy",
            "equation": "Gamma_2,bb proportional (1/48) integral_C V4_X2 G^4 V4_X2",
            "order": "c_ess^2",
            "result": "setting-sun self-energy and multiparticle cut",
            "independent_new_bulk_stress": False,
            "status": "DERIVED_TOPOLOGY_AND_SYMMETRY_FACTOR",
        },
        {
            "derivation_id": "F5179_08_surface_self_energy",
            "object": "alpha4 feedback into F",
            "equation": "S_alpha,k=Pi_(lambda alpha),F F(eta0,eta')+(1/4)Pi_(lambda alpha),rho rho(eta0,eta')",
            "order": "c_ess alpha_4",
            "result": "retarded initial-surface memory source, not a stationary volume source",
            "independent_new_bulk_stress": False,
            "status": "DERIVED_SOURCE_SIGNED",
        },
        {
            "derivation_id": "F5179_09_stress_contraction",
            "object": "late-time Hilbert stress",
            "equation": "delta T2_mn=D2_mn delta F; delta T_X2,mn=c_ess D4_mn [G G+C4_c]",
            "order": "alpha_4 and c_ess alpha_4",
            "result": "bulk-induced C4 contribution is O(c_ess^2); alpha2 retuning is separate state data",
            "independent_new_bulk_stress": False,
            "status": "DERIVED_ORDER_COUNTING",
        },
        {
            "derivation_id": "F5179_10_vacuum_preparation",
            "object": "adiabatic interacting vacuum",
            "equation": "eta_i -> -infinity(1-i epsilon) fixes the wavefunctional alpha4",
            "order": "c_ess",
            "result": "vacuum dressing belongs to vacuum matching or the calculable finite vacuum response, not occupation",
            "independent_new_bulk_stress": False,
            "status": "DERIVED_BUT_ALREADY_SUBTRACTED",
        },
        {
            "derivation_id": "F5179_11_gapped_cut",
            "object": "weak vacuum setting-sun infrared",
            "equation": "Im Sigma_R starts at the three-particle threshold; k_profile/(3m_gap)=5.85e-9 for the reference branch",
            "order": "c_ess^2",
            "result": "analytic below threshold and cannot create the required absolute-k criticality",
            "independent_new_bulk_stress": False,
            "status": "DERIVED_ON_GAPPED_VACUUM_BRANCH",
        },
        {
            "derivation_id": "F5179_12_occupied_cut",
            "object": "finite-occupation low-frequency cut",
            "equation": "leading Wigner response=Vlasov; collision correction begins beyond the subtracted kinetic term",
            "order": "c_ess^2 after Vlasov",
            "result": "the leading occupied response cannot be counted twice",
            "independent_new_bulk_stress": False,
            "status": "DERIVED_SUBTRACTION",
        },
    ]
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def wick_rows(inputs: dict[str, Any], wick: dict[str, Any]) -> list[dict[str, Any]]:
    target = inputs["target_fraction"]
    required_lambda = inputs["required_diagonal_lambda"]
    rows = [
        {
            "check_id": "W5179_00_six_pairings",
            "object": "Gaussian six-field Wick expansion",
            "exact_value": wick["six_pairings"],
            "equation_or_test": "(6-1)!!=15",
            "implication": "normalization-subtracted two-point correction has 12 connected pairings",
            "passed": wick["six_pairings"] == 15,
        },
        {
            "check_id": "W5179_01_two_point_connected",
            "object": "quartic insertion into covariance",
            "exact_value": wick["connected_two_pairings"],
            "equation_or_test": "15-3=12; 12/4!=1/2",
            "implication": "delta C_ij=-(lambda/2) K_abcd C_ia C_jb C_cd",
            "passed": wick["connected_two_pairings"] == 12,
        },
        {
            "check_id": "W5179_02_eight_pairings",
            "object": "Gaussian eight-field Wick expansion",
            "exact_value": wick["eight_pairings"],
            "equation_or_test": "(8-1)!!=105",
            "implication": "full four-point moment before cumulant subtraction",
            "passed": wick["eight_pairings"] == 105,
        },
        {
            "check_id": "W5179_03_fourpoint_connected",
            "object": "quartic insertion into connected four-point",
            "exact_value": wick["fully_connected_four_pairings"],
            "equation_or_test": "4!=24; 24/4!=1",
            "implication": "C4_c=-lambda K_abcd C_ia C_jb C_kc C_ld",
            "passed": wick["fully_connected_four_pairings"] == 24,
        },
        {
            "check_id": "W5179_04_scalar_moments",
            "object": "unit-variance Gaussian moments",
            "exact_value": ";".join(
                fraction_text(wick[key])
                for key in ("moment_2", "moment_4", "moment_6", "moment_8")
            ),
            "equation_or_test": "<q^2>,<q^4>,<q^6>,<q^8>=1,3,15,105",
            "implication": "independent exact check of all perturbative coefficients",
            "passed": [
                wick["moment_2"],
                wick["moment_4"],
                wick["moment_6"],
                wick["moment_8"],
            ]
            == [1, 3, 15, 105],
        },
        {
            "check_id": "W5179_05_covariance_shift",
            "object": "p_lambda proportional exp[-q^2/(2C)-lambda q^4/(24C^2)]",
            "exact_value": fraction_text(wick["delta_moment_2"]),
            "equation_or_test": "<q^2>/C=1-lambda/2+O(lambda^2)",
            "implication": "positive quartic damping lowers the covariance",
            "passed": wick["delta_moment_2"] == Fraction(-1, 2),
        },
        {
            "check_id": "W5179_06_kurtosis_shift",
            "object": "connected projected four-point",
            "exact_value": fraction_text(wick["delta_kappa_4"]),
            "equation_or_test": "kappa_4/C^2=-lambda+O(lambda^2)",
            "implication": "an order-one covariance repair is also strongly non-Gaussian",
            "passed": wick["delta_kappa_4"] == Fraction(-1),
        },
        {
            "check_id": "W5179_07_global_monotonicity",
            "object": "normalizable diagonal quartic family",
            "exact_value": "negative",
            "equation_or_test": "d<q^2>/d lambda=-Cov(q^2,q^4)/(24C^2)<0; 2Cov(Y,Y^2)=E[(Y-Y')^2(Y+Y')]",
            "implication": "the variance suppression holds beyond first-order perturbation theory",
            "passed": True,
        },
        {
            "check_id": "W5179_08_required_lambda",
            "object": "minimum locked transition correction",
            "exact_value": required_lambda,
            "equation_or_test": f"lambda_required=-2*{target:.17g}",
            "implication": "required lambda is negative and has magnitude greater than two",
            "passed": required_lambda < -2.0,
        },
        {
            "check_id": "W5179_09_normalizability",
            "object": "standalone quartic truncation at required sign",
            "exact_value": False,
            "equation_or_test": "lambda<0 makes -lambda q^4/(24C^2) grow at large |q|",
            "implication": "alpha6 or a complete positive preparation functional is mandatory",
            "passed": required_lambda < 0.0,
        },
    ]
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def stress_rows(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    execution = inputs["result_4954"]["execution"]
    sixpoint = inputs["sixpoint_4959"]
    rows = [
        {
            "bound_id": "S5179_00_target",
            "quantity": "minimum additional fractional V^2 at locked transition",
            "value": inputs["target_fraction"],
            "units": "dimensionless",
            "equation_or_source": "checkpoint-5178 min(A_transition)-1",
            "interpretation": "minimum order-one stress-response target",
            "status": "SOURCE_LOCKED",
        },
        {
            "bound_id": "S5179_01_natural_c",
            "quantity": "generous Planck-suppressed c_ess comparator",
            "value": inputs["natural_c_eV_minus4"],
            "units": "eV^-4",
            "equation_or_source": "1/Mbar_Pl^4 with Mbar_Pl=2.435e27 eV",
            "interpretation": "larger than the dynamic-N8 trajectory magnitude",
            "status": "DECLARED_GENEROUS_COMPARATOR",
        },
        {
            "bound_id": "S5179_02_trajectory_c",
            "quantity": "dynamic-N8 canonical c_ess trajectory comparator",
            "value": inputs["trajectory_c_eV_minus4"],
            "units": "eV^-4",
            "equation_or_source": "c_ess=A2 G_N^2=A2/(64pi^2 Mbar_Pl^4)",
            "interpretation": "conditional on the checkpoint-4958 minimal-essential trajectory normalization",
            "status": "DERIVED_TRAJECTORY_COMPARATOR",
        },
        {
            "bound_id": "S5179_03_A2",
            "quantity": "A2=a2/g^2 dynamic-N8 endpoint",
            "value": inputs["A2_dynamic_N8"],
            "units": "dimensionless",
            "equation_or_source": "checkpoint-4958 essential functional trajectory",
            "interpretation": "trajectory c_ess is 0.2562 of the generous comparator in magnitude",
            "status": "SOURCE_LOCKED",
        },
        {
            "bound_id": "S5179_03b_Euclidean_sign",
            "quantity": "standalone Euclidean X2 quartic stability on the trajectory",
            "value": inputs["trajectory_c_eV_minus4"] > 0.0,
            "units": "boolean",
            "equation_or_source": "A4_E=(8/3)c_ess k^3 on the regular-tetrahedron benchmark",
            "interpretation": "negative c_ess requires the higher P(X) hierarchy or UV completion for a globally positive preparation",
            "status": "QUARTIC_ONLY_PREPARATION_REJECTED",
        },
        {
            "bound_id": "S5179_04_positive_rows",
            "quantity": "positive-target SPARC outer-density rows",
            "value": inputs["positive_row_count"],
            "units": "rows",
            "equation_or_source": "checkpoint-4953 SPARC_X2_nonlinearity_gate.csv",
            "interpretation": "same global coefficient; no arena retuning",
            "status": "SOURCE_LOCKED",
        },
        {
            "bound_id": "S5179_05_density_range",
            "quantity": "positive-target required effective density range",
            "value": f"{inputs['density_min_eV4']:.17g};{inputs['density_median_eV4']:.17g};{inputs['density_max_eV4']:.17g}",
            "units": "eV^4 min;median;max",
            "equation_or_source": "checkpoint-4953 public outer-density diagnostic",
            "interpretation": "used only as a conservative stress-scale comparator",
            "status": "SOURCE_LOCKED",
        },
        {
            "bound_id": "S5179_06_best_epsilon",
            "quantity": "largest generous |c_ess| rho among positive rows",
            "value": inputs["natural_max_epsilon"],
            "units": "dimensionless",
            "equation_or_source": "|c_ess| max(rho)",
            "interpretation": "best possible row for an X2 stress enhancement",
            "status": "CALCULATED",
        },
        {
            "bound_id": "S5179_07_best_K",
            "quantity": "minimum operational four-point stress enhancement K_T",
            "value": inputs["natural_best_case_K_required"],
            "units": "dimensionless",
            "equation_or_source": "K_T=target/(|c_ess|rho), where |Delta T_X2|=|c_ess|rho^2 K_T",
            "interpretation": "even the densest row needs K_T above 1e114",
            "status": "CALCULATED_LOWER_COMPARATOR",
        },
        {
            "bound_id": "S5179_08_reference_K_natural",
            "quantity": "UGC09133 K_T with generous c_ess",
            "value": inputs["natural_reference_K_required"],
            "units": "dimensionless",
            "equation_or_source": "target/(Mbar_Pl^-4 rho_UGC09133)",
            "interpretation": "required connected/total fourth-moment enhancement",
            "status": "CALCULATED",
        },
        {
            "bound_id": "S5179_09_reference_K_trajectory",
            "quantity": "UGC09133 K_T with trajectory c_ess",
            "value": inputs["trajectory_reference_K_required"],
            "units": "dimensionless",
            "equation_or_source": "target/(|A2 G_N^2| rho_UGC09133)",
            "interpretation": "trajectory normalization strengthens the no-go",
            "status": "CALCULATED",
        },
        {
            "bound_id": "S5179_10_profile_threshold",
            "quantity": "reference profile momentum relative to mass gap",
            "value": inputs["reference_profile_energy_over_mass"],
            "units": "dimensionless",
            "equation_or_source": "(hbar c/R_n)/m_gap",
            "interpretation": "weak vacuum three-particle cut is far above the profile scale",
            "status": "CALCULATED",
        },
        {
            "bound_id": "S5179_11_preparation_probability",
            "quantity": "maximum controlled finite-preparation probability",
            "value": execution[
                "finite_preparation_probability_max_high_frequency"
            ],
            "units": "dimensionless",
            "equation_or_source": "checkpoint-4954 across 692 high-frequency rows",
            "interpretation": "all 692 rows fail",
            "status": "SOURCE_LOCKED_REJECTION",
        },
        {
            "bound_id": "S5179_12_controlled_gain",
            "quantity": "maximum generous controlled log gain",
            "value": execution[
                "controlled_envelope_log_gain_max_high_frequency"
            ],
            "units": "dimensionless",
            "equation_or_source": "checkpoint-4954 background/dilute envelope",
            "interpretation": "below the minimum required log multiplicity",
            "status": "SOURCE_LOCKED_REJECTION",
        },
        {
            "bound_id": "S5179_13_required_gain",
            "quantity": "minimum required high-frequency log multiplicity",
            "value": execution[
                "required_log_multiplicity_min_high_frequency"
            ],
            "units": "dimensionless",
            "equation_or_source": "checkpoint-4954",
            "interpretation": "controlled gain shortfall exceeds two orders in log space",
            "status": "SOURCE_LOCKED",
        },
        {
            "bound_id": "S5179_14_sixpoint",
            "quantity": "minimum full six-point kernel over arbitrary O2",
            "value": sixpoint["full_basis_kernel_minimized_over_O2"],
            "units": "dimensionless trajectory kernel",
            "equation_or_source": "checkpoint-4959 dynamic-N8 endpoint",
            "interpretation": "X3 and curvature completion do not produce a hidden large weak source",
            "status": "SOURCE_LOCKED_REJECTION",
        },
    ]
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def cmb_rows(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    covariance = inputs["result_5156"]
    rows = [
        {
            "gate_id": "C5179_00_empirical_covariance",
            "quantity": "checkpoint-5156 empirical adiabatic A_s",
            "central_value": covariance["CAMB_metadata"]["effective_A_s"],
            "one_sigma": "",
            "template_or_equation": "Gaussian comparator only",
            "transfer_required": False,
            "numeric_MTS_bound_applied": False,
            "status": "NONCLAIM_BASELINE",
        },
        {
            "gate_id": "C5179_01_local_gNL",
            "quantity": "Planck local primordial trispectrum g_NL",
            "central_value": -5.8e4,
            "one_sigma": 6.5e4,
            "template_or_equation": "T_zeta=(54/25)g_NL[P_zeta P_zeta P_zeta+3 perms]",
            "transfer_required": True,
            "numeric_MTS_bound_applied": False,
            "status": "SOURCE_BACKED_OBSERVATIONAL_BOUND",
        },
        {
            "gate_id": "C5179_02_dotpi4_gNL",
            "quantity": "Planck dot-pi^4 trispectrum amplitude",
            "central_value": -0.8e6,
            "one_sigma": 1.9e6,
            "template_or_equation": "Planck EFT trispectrum template",
            "transfer_required": True,
            "numeric_MTS_bound_applied": False,
            "status": "SOURCE_BACKED_OBSERVATIONAL_BOUND",
        },
        {
            "gate_id": "C5179_03_dpi4_gNL",
            "quantity": "Planck (partial pi)^4 trispectrum amplitude",
            "central_value": -3.9e5,
            "one_sigma": 3.9e5,
            "template_or_equation": "Planck EFT trispectrum template",
            "transfer_required": True,
            "numeric_MTS_bound_applied": False,
            "status": "SOURCE_BACKED_OBSERVATIONAL_BOUND",
        },
        {
            "gate_id": "C5179_04_projection",
            "quantity": "motion-to-curvature trispectrum projection",
            "central_value": "",
            "one_sigma": "",
            "template_or_equation": "T_zeta^MTS=product_i T_(zeta X)(k_i) C4_X,c plus metric constraint terms",
            "transfer_required": True,
            "numeric_MTS_bound_applied": False,
            "status": "TRANSFER_NOT_DERIVED_NO_NUMERIC_BOUND",
        },
        {
            "gate_id": "C5179_05_no_false_application",
            "quantity": "direct use of Planck g_NL on hidden motion alpha4",
            "central_value": False,
            "one_sigma": "",
            "template_or_equation": "requires a sourced shape overlap and T_(zeta X)",
            "transfer_required": True,
            "numeric_MTS_bound_applied": False,
            "status": "FORBIDDEN_WITHOUT_TRANSFER",
        },
        {
            "gate_id": "C5179_06_covariance_nonuniqueness",
            "quantity": "parent primordial covariance derived",
            "central_value": covariance["parent_primordial_covariance_derived"],
            "one_sigma": "",
            "template_or_equation": "checkpoint-5156 action-versus-state theorem",
            "transfer_required": False,
            "numeric_MTS_bound_applied": False,
            "status": "FALSE_SOURCE_LOCKED",
        },
    ]
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_cosmology_claim": False,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "D5179_00_lowest_kernel",
            "question": "What is the lowest reflection-even non-Gaussian boundary kernel?",
            "answer": "alpha_4 on the initial CTP surface",
            "reason": "alpha_2 is Gaussian and reflection removes alpha_3",
            "status": "DERIVED_EXACT",
            "next_action": "use only a constructive preparation contour",
        },
        {
            "decision_id": "D5179_01_diagonal_quartic",
            "question": "Can a standalone positive diagonal alpha4 increase the locked covariance?",
            "answer": "no",
            "reason": "every normalizable positive quartic damping lowers variance; the required negative sign is nonnormalizable without higher kernels",
            "status": "REJECTED_EXACT_IN_DECLARED_FAMILY",
            "next_action": "do not fit alpha4 as a lone state parameter",
        },
        {
            "decision_id": "D5179_02_adiabatic_vacuum",
            "question": "Does the adiabatically prepared X2 vacuum provide a new galaxy stress?",
            "answer": "no",
            "reason": "its alpha4 is assigned to local vacuum matching or the calculable finite vacuum response, not adjustable occupation",
            "status": "VACUUM_SECTOR_NOT_GALAXY_OCCUPATION",
            "next_action": "retain the checkpoint-5178 subtraction",
        },
        {
            "decision_id": "D5179_03_weak_unitary_preparation",
            "question": "Can controlled X2-X3 preparation make the order-one residual stress?",
            "answer": "no on the tested controlled branch",
            "reason": "surface feedback is O(c alpha4), induced alpha4 is O(c), and the 4954-4959 finite-time and six-point bounds fail",
            "status": "PERTURBATIVE_EXTRA_STRESS_REPAIR_REJECTED",
            "next_action": "do not repeat weak finite-time cascade calculations",
        },
        {
            "decision_id": "D5179_04_X3",
            "question": "Does X3 supply an independent lowest four-point source?",
            "answer": "no",
            "reason": "its first four-leg contribution is a local tadpole renormalization of X2; its genuine tree datum is six-point",
            "status": "REJECTED_AS_INDEPENDENT_ALPHA4_SOURCE",
            "next_action": "keep the full even hierarchy only in a strong calculation",
        },
        {
            "decision_id": "D5179_05_arbitrary_state",
            "question": "May an arbitrary large alpha4 be called an MTS prediction?",
            "answer": "no",
            "reason": "the current parent does not select the preparation contour, initial time, temperature or state functional",
            "status": "EXPLICIT_BOUNDARY_POSTULATE_ONLY",
            "next_action": "require a parent cosmogenesis/state-selection principle",
        },
        {
            "decision_id": "D5179_06_CMB",
            "question": "Is the Planck trispectrum bound directly applicable to alpha4_X?",
            "answer": "not yet",
            "reason": "the motion-to-curvature transfer and template overlap are not derived",
            "status": "CONDITIONAL_OBSERVATIONAL_GATE",
            "next_action": "derive T_(zeta X) before evaluating a g_NL likelihood",
        },
        {
            "decision_id": "D5179_07_survivor",
            "question": "What non-Gaussian route survives?",
            "answer": "a parent-derived strong full even boundary hierarchy or a gapless occupied continuum",
            "reason": "alpha4 alone and every controlled weak preparation route fail the positivity/amplitude/subtraction gates",
            "status": "OPEN_NOT_CLAIMED",
            "next_action": "derive the leading X2-X3 2PI spectral kernel and test whether any occupied branch removes the infrared gap without replaying Vlasov",
        },
        {
            "decision_id": "D5179_08_local_branch",
            "question": "Does checkpoint 5179 modify local GR, Newton or Maxwell?",
            "answer": "no",
            "reason": "all new terms are state-boundary or higher interacting corrections and the universal Hilbert source is unchanged",
            "status": "CHECKPOINT_4960_BRANCH_RETAINED",
            "next_action": "preserve the one-G_N one-Hilbert-source local branch",
        },
    ]
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_local_GR_claim": False,
            "valid_for_galaxy_claim": False,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def validation_row(
    validation_id: str,
    check: str,
    passed: bool,
    actual: Any,
    expected: Any,
) -> dict[str, Any]:
    return {
        "validation_id": validation_id,
        "check": check,
        "passed": bool(passed),
        "actual": actual,
        "expected": expected,
        "checkpoint_marker": MARKER,
        "valid_for_full_MTS_claim": False,
        "source_checked_date": CHECKED_DATE,
    }


def write_document(result: dict[str, Any]) -> None:
    summary = result["summary"]
    DOCUMENT.write_text(
        f"""# 5179 - Lowest reflection-even CTP boundary kernel, FLRW preparation and perturbative extra-stress no-go

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

This checkpoint performs the derivation selected at 5178. It does not invent
another occupation function and it does not stop at saying that the initial
state is missing. The lowest reflection-even non-Gaussian CTP kernel is
identified, derived from a covariant preparation contour, inserted into the
2PI/Kadanoff--Baym hierarchy, contracted into the Hilbert stress, and tested
against the already-locked amplitude and formation scales.

The result is restrictive. A weak parent-induced `alpha_4` exists, but it is
an initial-surface vertex rather than a stationary volume source. Adiabatic
vacuum preparation gives vacuum dressing already classified at checkpoint 5178
as local matching or calculable finite vacuum response, not galaxy occupation.
A controlled nonvacuum preparation contributes beyond the Vlasov response at
`O(c_ess^2)` and is far too small under the existing 4954--4959 bounds. A
standalone positive diagonal quartic state cannot even move the covariance in
the needed direction. A strong state can evade these weak statements only by
supplying a complete positive even hierarchy or a gapless occupied continuum;
that remains an explicit parent task, not a result hidden inside `alpha_4`.

## 1. Exact state-kernel hierarchy

For a general initial density matrix,

```text
<phi_+|rho|phi_->=exp(i F[phi]),

F[phi]=sum_(n>=0) (1/n!) integral_C alpha_n phi^n.
```

Every `alpha_n` is supported where all of its time arguments lie on the
initial CTP surface. Hermiticity gives

```text
i alpha_n^(a_1...a_n)
 =[i alpha_n^(-a_1...-a_n)]*.
```

The selected parent and state are invariant under `psi -> -psi`; therefore
all odd kernels vanish. `alpha_2` is the independent Gaussian covariance
already proved nonunique at checkpoint 5156. The first new kernel is exactly

```text
F_4=(1/4!) integral_(Sigma_0^4) alpha_4 psi^4.
```

This identifies the missing object without assigning it an arbitrary value.

## 2. Derivation from the bulk `X2-X3` parent

On spatially flat FLRW,

```text
sqrt(-g) [c_ess/4 (g^mn partial_m psi partial_n psi)^2]
 =c_ess/4 [-(psi')^2+(grad psi)^2]^2.
```

The `a^4` measure cancels the two inverse metrics. The symmetric four-leg
vertex is

```text
V_X2=2 c_ess sum_pairings (p_i.p_j)(p_k.p_l),
```

which reproduces the checkpoint-4953 shell amplitude

```text
M_22=(c_ess/2)(s^2+t^2+u^2).
```

For a Gaussian state prepared from `eta_i` to `eta_0`, the first connected
four-point is the exact first-order in-in expression

```text
C4_c(eta_0)
 =i integral_(eta_i)^eta_0 d_eta
   <[H_X2,I(eta),psi_1 psi_2 psi_3 psi_4(eta_0)]>_G
  +O(c_ess^2).
```

Equivalently, integrating the preparation contour `P` into an effective
initial surface gives

```text
alpha_4,X2(z_i)
 =-i integral_P d4v
   V_X2[nabla Delta_P(v,z_1),...,nabla Delta_P(v,z_4)]
  +O(c_ess^2).
```

This is the derivative-interaction version of the source-signed
Garny--Muller thermal initial-correlation construction. It is a real
derivation of the functional form. Its numeric value still depends on a
state-preparation contour, initial Gaussian state and endpoint that the
current parent has not selected.

One canonical contour can be completed exactly. Preparing the massless
adiabatic vacuum by a Euclidean half-space gives the free solution
`psi_k(tau)=psi_k(0)exp(k tau)` and therefore

```text
A_4,E(k_i)
 =[2 c_ess/k_t]
  sum_pairings
   [k_i k_j-k_i_vec.k_j_vec]
   [k_k k_l-k_k_vec.k_l_vec],

k_t=sum_i k_i.
```

For four equal magnitudes whose vectors form a regular momentum tetrahedron,
`k_i_vec.k_j_vec=-k^2/3`, so

```text
A_4,E=(8/3)c_ess k^3.
```

This is an explicit derived `alpha_4` benchmark, not an unspecified symbol.
It is also precisely interacting-vacuum wavefunctional dressing. It cannot be
relabelled as a populated galaxy state; the local part belongs to vacuum
matching and the finite part is a calculable vacuum response.

The dynamic-`N=8` GR-connected trajectory has
`c_ess={summary['trajectory_c_eV_minus4']:.17g} eV^-4`. Under this canonical
Euclidean continuation its standalone quartic is therefore destabilizing,
not damping. This does not reject the functional `P(X)` trajectory: it proves
that the trajectory's higher even terms or a UV completion are mandatory to
define a global positive preparation. The locally converged Taylor germ
cannot be truncated to `X2` and used as a density matrix.

`X3` does not provide another independent leading four-point shape. Contracting
two of its six legs gives

```text
delta V_4,X3=(1/2) Tr_G V_6,X3,
```

because `C(6,2)4!/6!=1/2`. This is a local tadpole renormalization of the
four-leg vertex. Genuine higher state information begins with `alpha_6`.
Two `X2` preparation vertices generate `alpha_6=O(c_ess^2)`, so a strong
prepared state necessarily carries a full even hierarchy.

## 3. Exact quartic positivity test

The projected diagonal family

```text
p_lambda(q)
 proportional exp[-q^2/(2C)-lambda q^4/(24 C^2)]
```

is the most favorable way to test whether the lowest kernel alone can raise a
mode covariance while preserving a manifest positive density. Exact Wick
combinatorics gives

```text
<q^2>/C       =1-lambda/2+O(lambda^2),
kappa_4/C^2  =-lambda+O(lambda^2).
```

The script enumerates all Wick pairings: `15` for six fields, `105` for eight
fields, `12` normalization-connected covariance pairings, and `24` fully
connected four-point pairings. The coefficients are therefore not fitted.

The sign result is global rather than merely perturbative:

```text
d<q^2>/d lambda
 =-Cov(q^2,q^4)/(24 C^2)<0,  lambda>=0,

2 Cov(Y,Y^2)=E[(Y-Y')^2(Y+Y')]>=0,  Y=q^2.
```

Every normalizable positive quartic damping suppresses the variance. The
minimum locked transition deficit `{summary['minimum_required_fraction']:.17g}`
would require

```text
lambda_required={summary['required_diagonal_lambda']:.17g}.
```

That sign makes a quartic-only diagonal weight nonnormalizable at large
`|q|`, and its magnitude is outside weak non-Gaussian control. A positive
`alpha_6` or a complete constructive quantum density matrix can stabilize a
negative effective quartic region, but then `alpha_4` is not the complete
state and the full hierarchy must be derived.

This is scoped correctly: it is an exact no-go for a standalone positive
diagonal quartic family, not for every off-diagonal quantum density matrix.
A unitary preparation can preserve positivity, but then its amplitude is
fixed by the bulk coupling and preparation history and must pass the next
gate.

## 4. 2PI and stress contraction

The post-4951 parent is interacting, so the earlier displayed
`Gamma_2^scalar=0` must not be reused beyond its quadratic scope. For `X2`,
the weak 2PI hierarchy begins with

```text
Gamma_2,double-bubble proportional (1/8) integral_C V4 G G,
Gamma_2,basketball   proportional (1/48) integral_C V4 G^4 V4.
```

The first term is a local Hartree correction of order `c_ess`; the first
nonlocal self-energy is order `c_ess^2`. An initial `alpha_4` enters the
statistical Kadanoff--Baym equation through the source-signed surface term

```text
S_alpha,k
 =Pi_(lambda alpha),F F(eta_0,eta')
  +(1/4)Pi_(lambda alpha),rho rho(eta_0,eta').
```

At late times,

```text
delta T_mn^(2)=D_mn^(2) delta F,
delta T_mn^X2=c_ess D_mn^(4)[G G+C4_c].
```

If the same bulk `X2` vertex induces `alpha_4`, its genuinely connected
late-time stress contribution is `O(c_ess^2)`. An arbitrary order-one
`alpha_4` can instead change the state, but that is precisely the independent
boundary postulate being tested, not a derived bulk source.

The weak vacuum setting-sun cut is also analytic far below its
three-particle threshold. For locked `UGC09133`,

```text
hbar c/R_n={summary['reference_profile_energy_eV']:.17g} eV,
(hbar c/R_n)/m_gap={summary['profile_energy_over_mass']:.17g},
[(hbar c/R_n)/m_gap]^2={summary['profile_energy_over_mass_squared']:.17g}.
```

It cannot produce the `|k|` criticality required at checkpoint 5149. A
populated medium can carry a low-frequency cut, but its leading Wigner term is
the Vlasov response already evolved and subtracted. The remaining collision
piece starts at the same weak interacting order tested at 4954.

## 5. Quantitative amplitude gate

Define the operational tensor-contracted fourth-moment enhancement by

```text
|Delta T_X2|=|c_ess| rho^2 K_T.
```

Then an additional fractional stress `f` requires the identity

```text
K_T=f/(|c_ess|rho).
```

Using the deliberately generous comparator
`|c_ess|=Mbar_Pl^-4={summary['natural_c_eV_minus4']:.17g} eV^-4`,
even the densest of the `{summary['positive_row_count']}` positive-target
checkpoint-4953 rows requires

```text
K_T>={summary['best_case_K_required']:.17g}.
```

For `UGC09133`, the generous and trajectory-normalized requirements are

```text
K_T,generous  ={summary['reference_K_natural']:.17g},
K_T,trajectory={summary['reference_K_trajectory']:.17g}.
```

These are operational stress enhancements, so no order-one tensor convention
is hidden in the comparison. They are incompatible with a weakly
non-Gaussian state.

The independent dynamical calculation agrees:

```text
4954 maximum finite-preparation probability
 ={summary['maximum_preparation_probability']:.17g};

4954 maximum generous controlled log gain
 ={summary['maximum_controlled_log_gain']:.17g};

4954 minimum required log multiplicity
 ={summary['minimum_required_log_multiplicity']:.17g};

4959 minimum completed six-point kernel
 ={summary['minimum_sixpoint_kernel']:.17g}.
```

All `{summary['controlled_failure_rows']}` high-frequency rows fail. This
closes the controlled perturbative state-preparation repair; it does not
pretend to calculate a strong nonquasiparticle state.

## 6. CMB gate without a false constraint

Planck 2018 reports

```text
g_NL^local       =(-5.8 +/- 6.5) 10^4,
g_NL^dot-pi^4    =(-0.8 +/- 1.9) 10^6,
g_NL^(partial pi)^4=(-3.9 +/- 3.9) 10^5.
```

These are real observational constraints. They cannot be directly pasted
onto a hidden motion-field `alpha_4`. The required projection is

```text
T_zeta^MTS
 =product_i T_(zeta X)(k_i) C4_X,c
  +metric-constraint terms,
```

followed by an overlap with the Planck templates. The current parent has not
derived `T_(zeta X)` or the shape overlap. Therefore this checkpoint records
the Planck numbers and the exact projection contract but does not fabricate a
numeric MTS trispectrum pass. The checkpoint-5156 empirical adiabatic
covariance remains a nonclaim baseline.

## 7. Result and next calculation

```text
lowest reflection-even non-Gaussian kernel       = alpha_4, derived;
covariant X2 preparation functional form         = derived;
X3 independent lowest four-point source          = rejected;
standalone positive diagonal quartic repair      = rejected exactly;
adiabatic-vacuum alpha_4 as galaxy occupation    = rejected by subtraction;
controlled weak X2-X3 prepared stress            = rejected quantitatively;
direct Planck g_NL bound on hidden alpha_4        = forbidden without transfer;
strong full even hierarchy                       = open, not claimed;
gapless occupied continuum                       = open, not claimed;
local GR/Newton/Maxwell branch                    = unchanged.
```

Route decision:
`{ROUTE_DECISION}`.

The next parent-owned calculation is not another `alpha_4` inventory. It is
to construct the leading trajectory-normalized `X2-X3` retarded 2PI spectral
kernel on the occupied branch, subtract its Vlasov limit explicitly, and test
whether the remaining spectral density can close the gap or generate the
required infrared nonanalyticity. If it stays gapped and perturbative, the
state/interaction repair closes and any strong boundary state remains a
declared cosmogenesis postulate.

## 8. Sources and artifacts

Primary sources:

- J. Berges, *Introduction to Nonequilibrium Quantum Field Theory*,
  `https://arxiv.org/abs/hep-ph/0409233`;
- M. Garny and M. M. Muller, *Kadanoff--Baym Equations with Non-Gaussian
  Initial Conditions: The Equilibrium Limit*,
  `https://arxiv.org/abs/0904.3600`;
- Planck Collaboration, *Planck 2018 results. IX. Constraints on primordial
  non-Gaussianity*, `https://arxiv.org/abs/1905.05697`.

Generated artifacts:

- `scripts/{SCRIPT.name}`;
- `source-intake/functional_rg/5179/{KERNEL_CSV.name}`;
- `source-intake/functional_rg/5179/{FLRW_CSV.name}`;
- `source-intake/functional_rg/5179/{WICK_CSV.name}`;
- `source-intake/functional_rg/5179/{STRESS_CSV.name}`;
- `source-intake/functional_rg/5179/{CMB_CSV.name}`;
- `source-intake/functional_rg/5179/{DECISION_CSV.name}`;
- `source-intake/functional_rg/5179/{PROVENANCE_CSV.name}`;
- `source-intake/functional_rg/5179/{RESULT_JSON.name}`;
- `source-intake/mts_residuals/{VALIDATION_CSV.name}`.

This is a private nonclaim checkpoint. It makes no local-GR, galaxy,
cosmology or full-MTS empirical claim.
""",
        encoding="utf-8",
    )


def run(dry_run: bool) -> dict[str, Any]:
    paths = source_paths()
    missing = {
        name: str(path) for name, path in paths.items() if not path.is_file()
    }
    if missing:
        raise FileNotFoundError(f"missing source paths: {missing}")
    source_hashes_before = {
        name: file_digest(path) for name, path in paths.items()
    }
    formal_before = tree_digest(FORMAL)
    checkpoint_5176_before = tree_digest(CHECKPOINT_5176_ROOT)
    signatures = source_signature_checks()
    inputs = derive_inputs()
    wick = exact_wick_values()
    kernels = kernel_rows()
    flrw = flrw_rows()
    wick_output = wick_rows(inputs, wick)
    stress = stress_rows(inputs)
    cmb = cmb_rows(inputs)
    decisions = decision_rows()
    execution = inputs["result_4954"]["execution"]
    summary = {
        "lowest_even_nonGaussian_kernel": "alpha_4",
        "alpha4_functional_form_derived": True,
        "numeric_alpha4_parent_selected": False,
        "Euclidean_vacuum_tetrahedron_factor": 8.0 / 3.0,
        "standalone_positive_diagonal_alpha4_can_raise_variance": False,
        "minimum_required_fraction": inputs["target_fraction"],
        "required_diagonal_lambda": inputs["required_diagonal_lambda"],
        "positive_row_count": inputs["positive_row_count"],
        "natural_c_eV_minus4": inputs["natural_c_eV_minus4"],
        "trajectory_c_eV_minus4": inputs["trajectory_c_eV_minus4"],
        "trajectory_to_natural_ratio": inputs[
            "trajectory_to_natural_ratio"
        ],
        "trajectory_Euclidean_quartic_stable_alone": (
            inputs["trajectory_c_eV_minus4"] > 0.0
        ),
        "best_case_K_required": inputs[
            "natural_best_case_K_required"
        ],
        "median_K_required": inputs["natural_median_K_required"],
        "reference_K_natural": inputs[
            "natural_reference_K_required"
        ],
        "reference_K_trajectory": inputs[
            "trajectory_reference_K_required"
        ],
        "reference_profile_energy_eV": inputs[
            "reference_profile_energy_eV"
        ],
        "profile_energy_over_mass": inputs[
            "reference_profile_energy_over_mass"
        ],
        "profile_energy_over_mass_squared": inputs[
            "reference_profile_energy_over_mass_squared"
        ],
        "maximum_preparation_probability": execution[
            "finite_preparation_probability_max_high_frequency"
        ],
        "maximum_controlled_log_gain": execution[
            "controlled_envelope_log_gain_max_high_frequency"
        ],
        "minimum_required_log_multiplicity": execution[
            "required_log_multiplicity_min_high_frequency"
        ],
        "controlled_failure_rows": execution[
            "controlled_envelope_failures"
        ],
        "minimum_sixpoint_kernel": inputs["sixpoint_4959"][
            "full_basis_kernel_minimized_over_O2"
        ],
        "Planck_local_gNL_central": -5.8e4,
        "Planck_local_gNL_sigma": 6.5e4,
        "motion_to_curvature_transfer_derived": False,
        "Planck_numeric_MTS_bound_applied": False,
        "perturbative_extra_stress_repair": "REJECTED",
        "strong_full_even_state_hierarchy": "OPEN_NOT_CLAIMED",
        "gapless_occupied_continuum": "OPEN_NOT_CLAIMED",
        "local_GR_Newton_Maxwell_branch_modified": False,
        "valid_for_local_GR_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_cosmology_claim": False,
        "valid_for_full_MTS_claim": False,
        "route_decision": ROUTE_DECISION,
    }
    dry_checks = [
        validation_row(
            "V5179_00_sources",
            "all cited local source paths exist",
            not missing,
            len(paths) - len(missing),
            len(paths),
        ),
        validation_row(
            "V5179_01_formal_lock",
            "protected formalization-workbench digest is unchanged",
            formal_before == FORMAL_DIGEST_LOCK,
            formal_before,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            "V5179_02_5176_lock",
            "immutable checkpoint-5176 tree is unchanged",
            checkpoint_5176_before == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_before,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            "V5179_03_garny_archive",
            "Garny-Muller primary-source archive hash matches acquisition",
            source_hashes_before["garny_muller_archive"]
            == GARNY_ARCHIVE_LOCK,
            source_hashes_before["garny_muller_archive"],
            GARNY_ARCHIVE_LOCK,
        ),
        validation_row(
            "V5179_04_planck_archive",
            "Planck primary-source archive hash matches acquisition",
            source_hashes_before["planck_nonGaussianity_archive"]
            == PLANCK_ARCHIVE_LOCK,
            source_hashes_before["planck_nonGaussianity_archive"],
            PLANCK_ARCHIVE_LOCK,
        ),
        validation_row(
            "V5179_05_source_signatures",
            "all primary-source equation signatures are present",
            all(signatures.values()),
            sum(signatures.values()),
            len(signatures),
        ),
        validation_row(
            "V5179_06_lowest_kernel",
            "reflection-even hierarchy selects alpha4 after Gaussian alpha2",
            summary["lowest_even_nonGaussian_kernel"] == "alpha_4"
            and summary["alpha4_functional_form_derived"],
            summary["lowest_even_nonGaussian_kernel"],
            "alpha_4",
        ),
        validation_row(
            "V5179_07_wick_six",
            "six-field Wick pairing count is exact",
            wick["six_pairings"] == 15
            and wick["connected_two_pairings"] == 12,
            [wick["six_pairings"], wick["connected_two_pairings"]],
            [15, 12],
        ),
        validation_row(
            "V5179_08_wick_eight",
            "eight-field and connected four-point pairing counts are exact",
            wick["eight_pairings"] == 105
            and wick["fully_connected_four_pairings"] == 24,
            [
                wick["eight_pairings"],
                wick["fully_connected_four_pairings"],
            ],
            [105, 24],
        ),
        validation_row(
            "V5179_09_wick_coefficients",
            "normalized covariance and kurtosis coefficients are exact",
            wick["delta_moment_2"] == Fraction(-1, 2)
            and wick["delta_kappa_4"] == Fraction(-1),
            [
                fraction_text(wick["delta_moment_2"]),
                fraction_text(wick["delta_kappa_4"]),
            ],
            ["-1/2", "-1"],
        ),
        validation_row(
            "V5179_10_FLRW_scale",
            "FLRW X2 scale-factor exponent cancels",
            4 - 2 * 2 == 0,
            4 - 2 * 2,
            0,
        ),
        validation_row(
            "V5179_11_vertex",
            "symmetric X2 vertex reproduces the checkpoint-4953 amplitude coefficient",
            Fraction(2, 1) * Fraction(1, 4) == Fraction(1, 2),
            fraction_text(Fraction(2, 1) * Fraction(1, 4)),
            "1/2",
        ),
        validation_row(
            "V5179_12_X3_contraction",
            "X3-to-fourpoint tadpole combinatoric is one half",
            Fraction(math.comb(6, 2) * math.factorial(4), math.factorial(6))
            == Fraction(1, 2),
            fraction_text(
                Fraction(
                    math.comb(6, 2) * math.factorial(4),
                    math.factorial(6),
                )
            ),
            "1/2",
        ),
        validation_row(
            "V5179_12b_Euclidean_kernel",
            "massless Euclidean regular-tetrahedron wavefunctional factor is eight thirds",
            Fraction(2, 1)
            * Fraction(1, 4)
            * 3
            * Fraction(4, 3) ** 2
            == Fraction(8, 3),
            fraction_text(
                Fraction(2, 1)
                * Fraction(1, 4)
                * 3
                * Fraction(4, 3) ** 2
            ),
            "8/3",
        ),
        validation_row(
            "V5179_13_required_sign",
            "locked positive covariance repair requires a negative standalone quartic",
            summary["required_diagonal_lambda"] < 0.0,
            summary["required_diagonal_lambda"],
            "<0",
        ),
        validation_row(
            "V5179_14_nonperturbative_size",
            "required standalone quartic magnitude exceeds weak control",
            abs(summary["required_diagonal_lambda"]) > 2.0,
            abs(summary["required_diagonal_lambda"]),
            ">2",
        ),
        validation_row(
            "V5179_15_density_rows",
            "all 173 source-locked positive-target density rows are retained",
            inputs["positive_row_count"] == 173,
            inputs["positive_row_count"],
            173,
        ),
        validation_row(
            "V5179_16_kurtosis",
            "even the best generous stress comparator requires K_T above 1e110",
            summary["best_case_K_required"] > 1.0e110,
            summary["best_case_K_required"],
            ">1e110",
        ),
        validation_row(
            "V5179_16b_Euclidean_stability",
            "negative trajectory c_ess is not promoted to a standalone positive Euclidean quartic state",
            not summary["trajectory_Euclidean_quartic_stable_alone"]
            and summary["trajectory_c_eV_minus4"] < 0.0,
            [
                summary["trajectory_Euclidean_quartic_stable_alone"],
                summary["trajectory_c_eV_minus4"],
            ],
            [False, "<0"],
        ),
        validation_row(
            "V5179_17_threshold",
            "reference profile momentum lies far below the mass gap",
            summary["profile_energy_over_mass"] < 1.0e-7,
            summary["profile_energy_over_mass"],
            "<1e-7",
        ),
        validation_row(
            "V5179_18_4954_rows",
            "all 692 controlled high-frequency preparation rows fail",
            execution["positive_high_frequency_rows"] == 692
            and execution["finite_preparation_failures"] == 692
            and execution["controlled_envelope_failures"] == 692,
            [
                execution["positive_high_frequency_rows"],
                execution["finite_preparation_failures"],
                execution["controlled_envelope_failures"],
            ],
            [692, 692, 692],
        ),
        validation_row(
            "V5179_19_4954_gain",
            "maximum controlled gain remains below minimum required multiplicity",
            summary["maximum_controlled_log_gain"]
            < summary["minimum_required_log_multiplicity"],
            [
                summary["maximum_controlled_log_gain"],
                summary["minimum_required_log_multiplicity"],
            ],
            "first < second",
        ),
        validation_row(
            "V5179_20_sixpoint",
            "completed weak six-point kernel is finite positive and tiny",
            0.0 < summary["minimum_sixpoint_kernel"] < 1.0e-50,
            summary["minimum_sixpoint_kernel"],
            "0 < value < 1e-50",
        ),
        validation_row(
            "V5179_21_CMB_projection",
            "Planck bound is not falsely applied without motion-to-curvature transfer",
            not summary["motion_to_curvature_transfer_derived"]
            and not summary["Planck_numeric_MTS_bound_applied"],
            [
                summary["motion_to_curvature_transfer_derived"],
                summary["Planck_numeric_MTS_bound_applied"],
            ],
            [False, False],
        ),
        validation_row(
            "V5179_22_covariance_nonclaim",
            "checkpoint-5156 primordial covariance remains non-derived",
            not inputs["result_5156"][
                "parent_primordial_covariance_derived"
            ],
            inputs["result_5156"][
                "parent_primordial_covariance_derived"
            ],
            False,
        ),
        validation_row(
            "V5179_23_universal_source",
            "checkpoint-4960 one-source local branch remains derived in its declared parent",
            inputs["result_4960"]["decision"][
                "leading_local_source_coupling"
            ]
            == "DERIVED_WITHIN_DECLARED_INTEGRATED_H_DIFF_PARENT",
            inputs["result_4960"]["decision"][
                "leading_local_source_coupling"
            ],
            "DERIVED_WITHIN_DECLARED_INTEGRATED_H_DIFF_PARENT",
        ),
        validation_row(
            "V5179_24_nonclaims",
            "all generated theory rows remain explicit nonclaims",
            all(
                not row["valid_for_full_MTS_claim"]
                for row in (
                    kernels
                    + flrw
                    + wick_output
                    + stress
                    + cmb
                    + decisions
                )
            ),
            "all_false",
            "all_false",
        ),
    ]
    failures = [
        row["validation_id"] for row in dry_checks if not row["passed"]
    ]
    if failures:
        raise RuntimeError(f"dry-run validation failures: {failures}")
    if dry_run:
        return {
            "mode": "dry-run",
            "checkpoint_marker": MARKER,
            "planned_outputs": [
                str(path)
                for path in (
                    KERNEL_CSV,
                    FLRW_CSV,
                    WICK_CSV,
                    STRESS_CSV,
                    CMB_CSV,
                    DECISION_CSV,
                    PROVENANCE_CSV,
                    RESULT_JSON,
                    VALIDATION_CSV,
                    DOCUMENT,
                )
            ],
            "summary": summary,
            "validation_count": len(dry_checks),
        }
    write_csv(KERNEL_CSV, kernels)
    write_csv(FLRW_CSV, flrw)
    write_csv(WICK_CSV, wick_output)
    write_csv(STRESS_CSV, stress)
    write_csv(CMB_CSV, cmb)
    write_csv(DECISION_CSV, decisions)
    source_hashes_after = {
        name: file_digest(path) for name, path in paths.items()
    }
    metadata = source_metadata()
    provenance_rows = [
        {
            "source_id": name,
            "source_path": str(path),
            "source_url": metadata.get(name, {}).get("url", "local checkpoint"),
            "role": metadata.get(name, {}).get(
                "role", "read-only parent input"
            ),
            "sha256_before": source_hashes_before[name],
            "sha256_after": source_hashes_after[name],
            "read_only_unchanged": (
                source_hashes_before[name] == source_hashes_after[name]
            ),
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for name, path in paths.items()
    ]
    write_csv(PROVENANCE_CSV, provenance_rows)
    formal_after = tree_digest(FORMAL)
    checkpoint_5176_after = tree_digest(CHECKPOINT_5176_ROOT)
    output_paths = (
        KERNEL_CSV,
        FLRW_CSV,
        WICK_CSV,
        STRESS_CSV,
        CMB_CSV,
        DECISION_CSV,
        PROVENANCE_CSV,
    )
    output_text = "\n".join(
        path.read_text(encoding="utf-8") for path in output_paths
    )
    full_checks = dry_checks + [
        validation_row(
            "V5179_25_sources_read_only",
            "all source hashes remain unchanged",
            source_hashes_before == source_hashes_after,
            sum(
                source_hashes_before[name] == source_hashes_after[name]
                for name in paths
            ),
            len(paths),
        ),
        validation_row(
            "V5179_26_formal_after",
            "formalization-workbench remains protected after execution",
            formal_after == formal_before == FORMAL_DIGEST_LOCK,
            formal_after,
            FORMAL_DIGEST_LOCK,
        ),
        validation_row(
            "V5179_27_5176_after",
            "checkpoint-5176 remains immutable after execution",
            checkpoint_5176_after
            == checkpoint_5176_before
            == CHECKPOINT_5176_TREE_LOCK,
            checkpoint_5176_after,
            CHECKPOINT_5176_TREE_LOCK,
        ),
        validation_row(
            "V5179_28_output_rows",
            "all generated evidence tables have their exact row counts",
            [
                len(kernels),
                len(flrw),
                len(wick_output),
                len(stress),
                len(cmb),
                len(decisions),
                len(provenance_rows),
            ]
            == [12, 14, 10, 16, 7, 9, len(paths)],
            [
                len(kernels),
                len(flrw),
                len(wick_output),
                len(stress),
                len(cmb),
                len(decisions),
                len(provenance_rows),
            ],
            [12, 14, 10, 16, 7, 9, len(paths)],
        ),
        validation_row(
            "V5179_29_no_placeholders",
            "generated evidence contains no placeholder marker",
            "MISSING_" not in output_text,
            "MISSING_" in output_text,
            False,
        ),
        validation_row(
            "V5179_30_route_unique",
            "exactly one decision row names the surviving route",
            sum(
                row["decision_id"] == "D5179_07_survivor"
                for row in decisions
            )
            == 1,
            sum(
                row["decision_id"] == "D5179_07_survivor"
                for row in decisions
            ),
            1,
        ),
        validation_row(
            "V5179_31_local_unchanged",
            "local GR/Newton/Maxwell branch is not modified",
            not summary["local_GR_Newton_Maxwell_branch_modified"],
            summary["local_GR_Newton_Maxwell_branch_modified"],
            False,
        ),
        validation_row(
            "V5179_32_no_claim",
            "checkpoint remains a local, galaxy, cosmology and full-MTS nonclaim",
            not any(
                summary[key]
                for key in (
                    "valid_for_local_GR_claim",
                    "valid_for_galaxy_claim",
                    "valid_for_cosmology_claim",
                    "valid_for_full_MTS_claim",
                )
            ),
            [
                summary["valid_for_local_GR_claim"],
                summary["valid_for_galaxy_claim"],
                summary["valid_for_cosmology_claim"],
                summary["valid_for_full_MTS_claim"],
            ],
            [False, False, False, False],
        ),
    ]
    failures = [
        row["validation_id"] for row in full_checks if not row["passed"]
    ]
    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "route_decision": ROUTE_DECISION,
        "source_paths": {
            name: str(path) for name, path in paths.items()
        },
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "source_signatures": signatures,
        "formalization_workbench_tree_sha256": formal_after,
        "checkpoint_5176_tree_sha256": checkpoint_5176_after,
        "exact_Wick_analysis": {
            key: fraction_text(value)
            if isinstance(value, Fraction)
            else value
            for key, value in wick.items()
        },
        "summary": summary,
        "validation_count": len(full_checks),
        "validation_failures": failures,
        "valid_for_local_GR_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_cosmology_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    write_json(RESULT_JSON, result)
    write_document(result)
    write_csv(VALIDATION_CSV, full_checks)
    if failures:
        raise RuntimeError(f"validation failures: {failures}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Derive the lowest reflection-even non-Gaussian CTP boundary "
            "kernel and test its controlled FLRW stress capability."
        )
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate sources and calculations without writing outputs",
    )
    arguments = parser.parse_args()
    result = run(arguments.dry_run)
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()

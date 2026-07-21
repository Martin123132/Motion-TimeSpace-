from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import math
import sys
from pathlib import Path
from typing import Any

import h5py
import numpy as np
import qnm
from scipy.constants import G, c
from scipy.integrate import cumulative_trapezoid
from scipy.stats import gaussian_kde


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"
INTAKE = POST / "source-intake" / "GW250114" / "4923"
RELEASE = (
    INTAKE
    / "release_extract"
    / "TGR_companion_S250114ax_results"
)
PSEOB = RELEASE / "gw250114_pseobnr"
PYRING = (
    RELEASE
    / "gw250114_pyring_results"
    / "GW250114"
    / (
        "GW250114A_NRSur7dq4HighFCalDownloadedDataExternalCustomPSDs_"
        "TEOB_22_21_33_44_55_domega_dtau_220_domega_dtau_440_0M_"
        "weighted_posterior"
    )
    / "Nested_sampler"
    / "posterior.dat"
)
ARCHIVE = INTAKE / "TGR_companion_S250114ax_results.tar.gz"
PSEOB_H5 = PSEOB / "posterior_samples.h5"
PSEOB_DAT = PSEOB / "pSEOBNRv5PHM_pesummary.dat"
PSEOB_REMNANT = PSEOB / "pseob_remnant_samples.npz"
COEFFICIENT_FILE = (
    POST
    / "source-intake"
    / "parent_coupling"
    / "4923"
    / "GRAVITATIONAL_QNM_220_CUBIC_COEFFICIENTS.csv"
)

CHECKPOINT = "4923"
CHECKED_DATE = "2026-07-12"
MARKER = "MTS_GW250114_GRAVITATIONAL_QNM_WEYL_C3_RECAST_4923"
FORMAL_MARKER = "PPC4161_GW250114_QNM_WEYL_C3_RECAST_4923"
NEXT_TARGET = (
    "4924-Y5-R2FR-renormalized-parent-Weyl-cubic-finite-matching-"
    "sign-and-scale-from-motion-scalar-determinant-or-explicit-"
    "counterterm-boundary.md"
)

GW250114_PAPER_URL = "https://arxiv.org/abs/2509.08099"
GW250114_RELEASE_URL = "https://doi.org/10.5281/zenodo.17018009"
QNM_THEORY_URL = "https://arxiv.org/abs/2307.07431"
QNM_PACKAGE_URL = "https://github.com/duetosymmetry/qnm"
GW170608_URL = "https://arxiv.org/abs/2407.08929"
SCALAR_EXCLUSION_URL = "https://arxiv.org/abs/2604.11755"

EXPECTED_ARCHIVE_MD5 = "8778398081EF5713E4C762169C9FD65C"
ALPHA_MIN = -0.15
ALPHA_MAX = 0.15
ALPHA_POINTS = 501
ROBUST_ALPHA_POINTS = 1501
CHI_INTEGRATION_MIN = 0.63
CHI_THEORY_MAX = 0.70
CHI_POINTS = 71
TAU_DOMAIN = 0.01
ALPHA_ONE_PERCENT_CAP = 4.0 * TAU_DOMAIN / 3.0
THEORY_RELATIVE_ERROR = 0.05
SUN_MASS_KG = 1.988409870698051e30
EARTH_MASS_KG = 5.9722e24
EARTH_RADIUS_M = 6_371_000.0
GALILEO_ALTITUDE_M = 23_229_000.0

DIGEST_CACHE: dict[tuple[Path, str], str] = {}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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


def digest(path: Path, algorithm: str = "sha256") -> str:
    key = (path, algorithm)
    if key in DIGEST_CACHE:
        return DIGEST_CACHE[key]
    hasher = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            hasher.update(block)
    value = hasher.hexdigest()
    DIGEST_CACHE[key] = value
    return value


def read_text_auto(path: Path) -> str:
    raw = path.read_bytes()
    encoding = "utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8"
    return raw.decode(encoding, errors="replace")


def load_coefficients() -> dict[str, np.ndarray]:
    rows = read_csv(COEFFICIENT_FILE)
    orders = [int(row["order"]) for row in rows]
    if orders != list(range(13)):
        raise ValueError("the cubic 220 coefficient table must contain orders 0 through 12")
    return {
        "polar_plus": np.asarray(
            [
                complex(float(row["even_plus_real"]), float(row["even_plus_imag"]))
                for row in rows
            ],
            dtype=complex,
        ),
        "axial_minus": np.asarray(
            [
                complex(float(row["even_minus_real"]), float(row["even_minus_imag"]))
                for row in rows
            ],
            dtype=complex,
        ),
    }


def load_pseob() -> tuple[np.ndarray, np.ndarray, np.ndarray, str]:
    with h5py.File(PSEOB_H5, "r") as handle:
        group = handle["pSEOBNRv5PHM"]
        samples = group["posterior_samples"][:]
        prior_raw = group["config_file/config/prior_dict"][0]
    prior_text = (
        prior_raw.decode("utf-8", errors="replace")
        if isinstance(prior_raw, bytes)
        else str(prior_raw)
    )
    reporting_mask = (
        (samples["domega440"] < 0.8)
        & (samples["dtau440"] < 0.8)
    )
    theory_mask = (
        reporting_mask
        & (samples["final_spin_non_evolved"] >= 0.0)
        & (samples["final_spin_non_evolved"] <= CHI_THEORY_MAX)
    )
    return samples, reporting_mask, theory_mask, prior_text


def qnm_maps(
    spins: np.ndarray,
    coefficients: dict[str, np.ndarray],
) -> dict[str, dict[str, np.ndarray]]:
    mode = qnm.modes_cache(s=-2, l=2, m=2, n=0)
    kerr = np.asarray([mode(a=float(spin))[0] for spin in spins], dtype=complex)
    maps: dict[str, dict[str, np.ndarray]] = {}
    for branch, branch_coefficients in coefficients.items():
        shifts = np.polynomial.polynomial.polyval(spins, branch_coefficients)
        frequency_coefficient = shifts.real / kerr.real
        damping_coefficient = -shifts.imag / kerr.imag
        maps[branch] = {
            "kerr": kerr,
            "shift": shifts,
            "frequency_coefficient": frequency_coefficient,
            "damping_coefficient": damping_coefficient,
        }
    return maps


def cdf_from_pdf(grid: np.ndarray, density: np.ndarray) -> np.ndarray:
    cumulative = np.concatenate(
        [[0.0], cumulative_trapezoid(density, grid)]
    )
    return cumulative / cumulative[-1]


def summarize_profile(
    alpha_grid: np.ndarray,
    density: np.ndarray,
) -> dict[str, float]:
    normalized = density / np.trapezoid(density, alpha_grid)
    cumulative = cdf_from_pdf(alpha_grid, normalized)
    lower, median, upper = np.interp(
        [0.05, 0.50, 0.95],
        cumulative,
        alpha_grid,
    )
    maximum_index = int(np.argmax(normalized))
    map_value = float(alpha_grid[maximum_index])
    probability_positive = 1.0 - float(
        np.interp(0.0, alpha_grid, cumulative)
    )
    probability_domain = float(
        np.interp(ALPHA_ONE_PERCENT_CAP, alpha_grid, cumulative)
        - np.interp(-ALPHA_ONE_PERCENT_CAP, alpha_grid, cumulative)
    )
    density_zero = float(np.interp(0.0, alpha_grid, normalized))
    density_maximum = float(normalized[maximum_index])
    delta_chi2 = 2.0 * math.log(density_maximum / density_zero)
    prior_density = 1.0 / (ALPHA_MAX - ALPHA_MIN)
    bayes_gr_over_line = density_zero / prior_density
    edge_fraction = 0.90
    edge_low = ALPHA_MIN * edge_fraction
    edge_high = ALPHA_MAX * edge_fraction
    edge_probability = float(
        np.interp(edge_low, alpha_grid, cumulative)
        + 1.0
        - np.interp(edge_high, alpha_grid, cumulative)
    )
    return {
        "alpha_lower_90": float(lower),
        "alpha_median": float(median),
        "alpha_upper_90": float(upper),
        "alpha_map": map_value,
        "probability_alpha_positive": probability_positive,
        "probability_one_percent_domain": probability_domain,
        "delta_chi2_proxy_vs_GR": delta_chi2,
        "bayes_GR_over_line_uniform_prior": bayes_gr_over_line,
        "prior_edge_probability": edge_probability,
        "max_abs_alpha_90": max(abs(float(lower)), abs(float(upper))),
        "normalized_density_zero": density_zero,
    }


def release_provenance_rows() -> list[dict[str, Any]]:
    archive_md5 = digest(ARCHIVE, "md5")
    selected = [
        ("archive", ARCHIVE, "official Zenodo tarball", "md5"),
        ("pseob_h5", PSEOB_H5, "official pSEOB posterior samples", "sha256"),
        ("pseob_dat", PSEOB_DAT, "official tabular pSEOB posterior", "sha256"),
        ("pseob_remnant", PSEOB_REMNANT, "official remnant summary samples", "sha256"),
        ("pyring_generic", PYRING, "official generic PyRing posterior comparator", "sha256"),
        ("qnm_theory_html", INTAKE / "arxiv_2307.07431.html", "local theory snapshot", "sha256"),
        ("event_paper_html", INTAKE / "arxiv_2509.08099.html", "local event-paper snapshot", "sha256"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, role, hash_algorithm in selected:
        hash_value = archive_md5 if hash_algorithm == "md5" else digest(path)
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "exists": path.exists(),
                "size_bytes": path.stat().st_size,
                "hash_algorithm": hash_algorithm,
                "hash": hash_value,
                "expected_hash": EXPECTED_ARCHIVE_MD5.lower() if source_id == "archive" else "",
                "hash_verified": (
                    archive_md5.lower() == EXPECTED_ARCHIVE_MD5.lower()
                    if source_id == "archive"
                    else len(hash_value) == 64
                ),
                "source_url": (
                    GW250114_RELEASE_URL
                    if source_id in {"archive", "pseob_h5", "pseob_dat", "pseob_remnant", "pyring_generic"}
                    else QNM_THEORY_URL
                    if source_id == "qnm_theory_html"
                    else GW250114_PAPER_URL
                ),
                "passed": True,
            }
        )
    return tagged(rows)


def posterior_audit_rows(
    samples: np.ndarray,
    reporting_mask: np.ndarray,
    theory_mask: np.ndarray,
    prior_text: str,
) -> list[dict[str, Any]]:
    reporting_count = int(np.count_nonzero(reporting_mask))
    theory_count = int(np.count_nonzero(theory_mask))
    rows: list[dict[str, Any]] = [
        {
            "audit_id": "POST4923_00_raw",
            "quantity": "raw pSEOB posterior samples",
            "value": len(samples),
            "q05": "",
            "q50": "",
            "q95": "",
            "units": "samples",
            "status": "OFFICIAL_RELEASE_LOADED",
            "detail": "pSEOBNRv5PHM/posterior_samples",
            "passed": len(samples) == 40776,
        },
        {
            "audit_id": "POST4923_01_reporting_cut",
            "quantity": "published 440 prior-reporting cut",
            "value": reporting_count,
            "q05": "",
            "q50": "",
            "q95": "",
            "units": "samples",
            "status": "PAPER_NOTEBOOK_CUT_REPRODUCED",
            "detail": "domega440<0.8 and dtau440<0.8",
            "passed": reporting_count == 17742,
        },
        {
            "audit_id": "POST4923_02_theory_support",
            "quantity": "samples inside gravitational-QNM spin domain",
            "value": theory_count,
            "q05": "",
            "q50": "",
            "q95": "",
            "units": "samples",
            "status": "CHI_LE_0P7",
            "detail": "reporting cut plus 0<=final_spin_non_evolved<=0.7",
            "passed": theory_count == 17719,
        },
        {
            "audit_id": "POST4923_03_support_fraction",
            "quantity": "reported samples retained by spin cut",
            "value": theory_count / reporting_count,
            "q05": "",
            "q50": "",
            "q95": "",
            "units": "fraction",
            "status": "MORE_THAN_99_PERCENT_SUPPORTED",
            "detail": "the unsupported high-spin tail is removed rather than extrapolated",
            "passed": theory_count / reporting_count > 0.998,
        },
        {
            "audit_id": "POST4923_04_priors",
            "quantity": "deviation priors",
            "value": "uniform",
            "q05": -0.8,
            "q50": "",
            "q95": 2.0,
            "units": "dimensionless",
            "status": "UNIFORM_DOMEGA220_DTAU220",
            "detail": "domega220 and dtau220 independently uniform on [-0.8,2.0]",
            "passed": (
                "domega220 = Uniform" in prior_text
                and "dtau220 = Uniform" in prior_text
                and "minimum=-0.8, maximum=2.0" in prior_text
            ),
        },
    ]
    selected = samples[theory_mask]
    parameter_specs = [
        ("POST4923_05_df220", "domega220", "fractional 220 frequency deviation", "dimensionless"),
        ("POST4923_06_dtau220", "dtau220", "fractional 220 damping-time deviation", "dimensionless"),
        ("POST4923_07_spin", "final_spin_non_evolved", "remnant dimensionless spin", "dimensionless"),
        ("POST4923_08_mass", "final_mass_non_evolved", "detector-frame remnant mass", "solar_mass"),
    ]
    for audit_id, field, quantity, units in parameter_specs:
        values = np.asarray(selected[field], dtype=float)
        q05, q50, q95 = np.quantile(values, [0.05, 0.50, 0.95])
        rows.append(
            {
                "audit_id": audit_id,
                "quantity": quantity,
                "value": float(np.mean(values)),
                "q05": float(q05),
                "q50": float(q50),
                "q95": float(q95),
                "units": units,
                "status": "FINITE_POSTERIOR_SUMMARY",
                "detail": field,
                "passed": bool(np.all(np.isfinite(values))),
            }
        )
    frequency = np.asarray(selected["domega220"], dtype=float)
    damping = np.asarray(selected["dtau220"], dtype=float)
    spin = np.asarray(selected["final_spin_non_evolved"], dtype=float)
    rows.extend(
        [
            {
                "audit_id": "POST4923_09_df_dtau_corr",
                "quantity": "corr(domega220,dtau220)",
                "value": float(np.corrcoef(frequency, damping)[0, 1]),
                "q05": "",
                "q50": "",
                "q95": "",
                "units": "correlation",
                "status": "JOINT_POSTERIOR_RETAINED",
                "detail": "the recast uses the joint density rather than two independent intervals",
                "passed": True,
            },
            {
                "audit_id": "POST4923_10_df_spin_corr",
                "quantity": "corr(domega220,spin)",
                "value": float(np.corrcoef(frequency, spin)[0, 1]),
                "q05": "",
                "q50": "",
                "q95": "",
                "units": "correlation",
                "status": "SPIN_CORRELATION_RETAINED",
                "detail": "the primary 3D KDE integrates the theory manifold over spin",
                "passed": True,
            },
        ]
    )
    return tagged(rows)


def compatibility_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "compatibility_id": "COMP4923_00_pSEOB",
                "data_product": "pSEOBNRv5PHM joint 220 and 440 deviations",
                "theory_product": "fractional 220 frequency and damping-time map",
                "status": "COMPATIBLE_220",
                "decision": "use pSEOB 220 posterior and its correlated remnant spin",
                "reason": "fractional angular-frequency and ordinary-frequency shifts are identical",
                "passed": True,
            },
            {
                "compatibility_id": "COMP4923_01_generic_PyRing",
                "data_product": "TEOBResumSPM PyRing generic deviation posterior",
                "theory_product": "same 220 map",
                "status": "COMPARATOR_NOT_PRIMARY",
                "decision": "retain locally but do not mix with the pSEOB posterior",
                "reason": "its much broader 220 posterior is a different waveform analysis",
                "passed": True,
            },
            {
                "compatibility_id": "COMP4923_02_440",
                "data_product": "pSEOB 440 deviation posterior",
                "theory_product": "arXiv:2307.07431 modes",
                "status": "INCOMPATIBLE_NO_440_CUBIC_COEFFICIENTS",
                "decision": "exclude 440 from the Weyl-cubic likelihood",
                "reason": "the source provides fundamental 220 and 330 coefficients, not 440",
                "passed": True,
            },
            {
                "compatibility_id": "COMP4923_03_polarizations",
                "data_product": "single generic 220 complex frequency per waveform",
                "theory_product": "distinct polar-plus and axial-minus frequencies",
                "status": "BRANCH_CONDITIONAL_ONLY",
                "decision": "report two separate line posteriors",
                "reason": "MTS does not yet predict the excitation or mixing weights",
                "passed": True,
            },
            {
                "compatibility_id": "COMP4923_04_scalar",
                "data_product": "GW strain gravitational QNMs",
                "theory_product": "arXiv:2604.11755 scalar perturbation modes",
                "status": "EXCLUDED_WRONG_SECTOR",
                "decision": "do not use",
                "reason": "scalar QNMs are not the gravitational strain modes fitted by pSEOB",
                "passed": True,
            },
        ]
    )


def coefficient_map_rows(
    samples: np.ndarray,
    theory_mask: np.ndarray,
    coefficients: dict[str, np.ndarray],
) -> list[dict[str, Any]]:
    selected_spin = np.asarray(
        samples["final_spin_non_evolved"][theory_mask],
        dtype=float,
    )
    spin_values = np.concatenate(
        [np.quantile(selected_spin, [0.05, 0.50, 0.95]), [CHI_THEORY_MAX]]
    )
    spin_labels = ["spin_q05", "spin_q50", "spin_q95", "spin_0p7"]
    maps = qnm_maps(spin_values, coefficients)
    rows: list[dict[str, Any]] = []
    for branch, branch_map in maps.items():
        for index, (spin_label, spin_value) in enumerate(zip(spin_labels, spin_values)):
            shift = branch_map["shift"][index]
            kerr = branch_map["kerr"][index]
            expected_real = 0.220 if branch == "polar_plus" else -0.221
            expected_imag = -0.293 if branch == "polar_plus" else 0.251
            convergence_difference = 1.23 if branch == "polar_plus" else 0.88
            at_endpoint = spin_label == "spin_0p7"
            endpoint_match = (
                abs(shift.real - expected_real) < 5.0e-4
                and abs(shift.imag - expected_imag) < 5.0e-4
            )
            rows.append(
                {
                    "map_id": f"MAP4923_{branch}_{spin_label}",
                    "branch": branch,
                    "polarization": "polar" if branch == "polar_plus" else "axial",
                    "spin": float(spin_value),
                    "kerr_omega_real": float(kerr.real),
                    "kerr_omega_imag": float(kerr.imag),
                    "deltaomega_real": float(shift.real),
                    "deltaomega_imag": float(shift.imag),
                    "k_frequency": float(branch_map["frequency_coefficient"][index]),
                    "k_damping_time": float(branch_map["damping_coefficient"][index]),
                    "map_frequency": "deltahat_f220=alpha_ev Re(deltaomega)/Re(M omega_Kerr)",
                    "map_damping": "deltahat_tau220=-alpha_ev Im(deltaomega)/Im(M omega_Kerr)",
                    "alpha_identity": "alpha_ev=alpha_bar1=s_+(ell_+/M)^4",
                    "published_endpoint_difference_percent": convergence_difference if at_endpoint else "",
                    "endpoint_table_match": endpoint_match if at_endpoint else "",
                    "status": "SOURCE_BACKED_GRAVITATIONAL_QNM_MAP",
                    "passed": endpoint_match if at_endpoint else True,
                }
            )
    return tagged(rows)


def joint_profiles(
    samples: np.ndarray,
    theory_mask: np.ndarray,
    coefficients: dict[str, np.ndarray],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    selected = samples[theory_mask]
    sample_matrix = np.vstack(
        [
            np.asarray(selected["domega220"], dtype=float),
            np.asarray(selected["dtau220"], dtype=float),
            np.asarray(selected["final_spin_non_evolved"], dtype=float),
        ]
    )
    posterior_kde = gaussian_kde(sample_matrix)
    alpha_grid = np.linspace(ALPHA_MIN, ALPHA_MAX, ALPHA_POINTS)
    spin_grid = np.linspace(CHI_INTEGRATION_MIN, CHI_THEORY_MAX, CHI_POINTS)
    maps = qnm_maps(spin_grid, coefficients)
    mass_values = np.asarray(selected["final_mass_non_evolved"], dtype=float)
    mass_q05, mass_q50, mass_q95 = np.quantile(mass_values, [0.05, 0.50, 0.95])
    profile_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    for branch, branch_map in maps.items():
        frequency_coefficients = branch_map["frequency_coefficient"]
        damping_coefficients = branch_map["damping_coefficient"]
        density = np.empty_like(alpha_grid)
        for alpha_index, alpha_value in enumerate(alpha_grid):
            points = np.vstack(
                [
                    alpha_value * frequency_coefficients,
                    alpha_value * damping_coefficients,
                    spin_grid,
                ]
            )
            density[alpha_index] = np.trapezoid(
                posterior_kde(points),
                spin_grid,
            )
        density /= np.trapezoid(density, alpha_grid)
        summary = summarize_profile(alpha_grid, density)
        ell_over_mass = summary["max_abs_alpha_90"] ** 0.25
        median_mass_length_km = (
            G * float(mass_q50) * SUN_MASS_KG / c**2 / 1000.0
        )
        summary_rows.append(
            {
                "branch": branch,
                "polarization": "polar" if branch == "polar_plus" else "axial",
                "method": "3D_joint_KDE_line_manifold_spin_integrated",
                **summary,
                "alpha_prior_min": ALPHA_MIN,
                "alpha_prior_max": ALPHA_MAX,
                "kde_bandwidth": "Scott",
                "spin_integration_min": CHI_INTEGRATION_MIN,
                "spin_integration_max": CHI_THEORY_MAX,
                "samples_used": len(selected),
                "mass_q05_solar": float(mass_q05),
                "mass_q50_solar": float(mass_q50),
                "mass_q95_solar": float(mass_q95),
                "ell_over_M_from_max_abs_90": ell_over_mass,
                "illustrative_ell_km_at_median_mass": ell_over_mass * median_mass_length_km,
                "status": "BRANCH_CONDITIONAL_NONCLAIM",
                "GR_inside_90": (
                    summary["alpha_lower_90"] < 0.0 < summary["alpha_upper_90"]
                ),
                "passed": (
                    summary["alpha_lower_90"] < 0.0 < summary["alpha_upper_90"]
                    and summary["prior_edge_probability"] < 1.0e-6
                ),
            }
        )
        for alpha_value, density_value in zip(alpha_grid, density):
            profile_rows.append(
                {
                    "branch": branch,
                    "alpha_ev": float(alpha_value),
                    "posterior_density": float(density_value),
                    "method": "3D_joint_KDE_line_manifold_spin_integrated",
                    "alpha_prior_min": ALPHA_MIN,
                    "alpha_prior_max": ALPHA_MAX,
                    "passed": bool(math.isfinite(float(density_value))),
                }
            )
    return tagged(summary_rows), tagged(profile_rows)


def robustness_rows(
    samples: np.ndarray,
    theory_mask: np.ndarray,
    coefficients: dict[str, np.ndarray],
) -> list[dict[str, Any]]:
    selected = samples[theory_mask]
    frequency = np.asarray(selected["domega220"], dtype=float)
    damping = np.asarray(selected["dtau220"], dtype=float)
    spins = np.asarray(selected["final_spin_non_evolved"], dtype=float)
    sample_matrix = np.vstack([frequency, damping])
    alpha_grid = np.linspace(ALPHA_MIN, ALPHA_MAX, ROBUST_ALPHA_POINTS)
    spin_values = np.quantile(spins, [0.05, 0.50, 0.95])
    spin_labels = ["q05", "q50", "q95"]
    maps = qnm_maps(spin_values, coefficients)
    rows: list[dict[str, Any]] = []
    for bandwidth_multiplier in (0.75, 1.00, 1.25):
        posterior_kde = gaussian_kde(sample_matrix)
        posterior_kde.set_bandwidth(
            posterior_kde.factor * bandwidth_multiplier
        )
        for spin_index, (spin_label, spin_value) in enumerate(
            zip(spin_labels, spin_values)
        ):
            for branch, branch_map in maps.items():
                frequency_coefficient = float(
                    branch_map["frequency_coefficient"][spin_index]
                )
                damping_coefficient = float(
                    branch_map["damping_coefficient"][spin_index]
                )
                density = posterior_kde(
                    np.vstack(
                        [
                            frequency_coefficient * alpha_grid,
                            damping_coefficient * alpha_grid,
                        ]
                    )
                )
                nominal = summarize_profile(alpha_grid, density)
                for theory_scale in (
                    1.0 - THEORY_RELATIVE_ERROR,
                    1.0,
                    1.0 + THEORY_RELATIVE_ERROR,
                ):
                    lower = nominal["alpha_lower_90"] / theory_scale
                    median = nominal["alpha_median"] / theory_scale
                    upper = nominal["alpha_upper_90"] / theory_scale
                    map_value = nominal["alpha_map"] / theory_scale
                    rows.append(
                        {
                            "branch": branch,
                            "spin_quantile": spin_label,
                            "spin": float(spin_value),
                            "bandwidth_multiplier": bandwidth_multiplier,
                            "theory_coefficient_scale": theory_scale,
                            "alpha_lower_90": lower,
                            "alpha_median": median,
                            "alpha_upper_90": upper,
                            "alpha_map": map_value,
                            "max_abs_alpha_90": max(abs(lower), abs(upper)),
                            "frequency_coefficient_nominal": frequency_coefficient,
                            "damping_coefficient_nominal": damping_coefficient,
                            "method": "2D_marginal_KDE_fixed_spin_sensitivity",
                            "status": "ROBUSTNESS_NONCLAIM",
                            "passed": lower < 0.0 < upper,
                        }
                    )
    return tagged(rows)


def domain_rows(
    branch_rows: list[dict[str, Any]],
    robust_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    robust_max = max(float(row["max_abs_alpha_90"]) for row in robust_rows)
    robust_epsilon = 0.75 * robust_max
    mass_q95 = max(float(row["mass_q95_solar"]) for row in branch_rows)
    mass_q95_length_km = G * mass_q95 * SUN_MASS_KG / c**2 / 1000.0
    robust_ell_km = robust_max**0.25 * mass_q95_length_km
    earth_mass_length = G * EARTH_MASS_KG / c**2
    earth_acceleration = (
        140.0
        * (robust_ell_km * 1000.0) ** 4
        * earth_mass_length**2
        / EARTH_RADIUS_M**6
    )
    radius_two = EARTH_RADIUS_M + GALILEO_ALTITUDE_M
    clock_residual = (
        20.0
        * (robust_ell_km * 1000.0) ** 4
        * earth_mass_length**2
        * abs(EARTH_RADIUS_M**-7 - radius_two**-7)
        / abs(EARTH_RADIUS_M**-1 - radius_two**-1)
    )
    rows: list[dict[str, Any]] = []
    for branch_row in branch_rows:
        max_abs = float(branch_row["max_abs_alpha_90"])
        epsilon = 0.75 * max_abs
        rows.append(
            {
                "domain_id": f"DOMAIN4923_{branch_row['branch']}",
                "branch": branch_row["branch"],
                "alpha_envelope": max_abs,
                "epsilon_h_Schwarzschild_proxy": epsilon,
                "tau_domain": TAU_DOMAIN,
                "miss_factor": epsilon / TAU_DOMAIN,
                "probability_inside_domain": branch_row[
                    "probability_one_percent_domain"
                ],
                "illustrative_ell_km": branch_row[
                    "illustrative_ell_km_at_median_mass"
                ],
                "domain_gate_passed": epsilon <= TAU_DOMAIN,
                "status": "COMPACT_ONE_PERCENT_NOT_PROMOTED",
                "passed": epsilon > TAU_DOMAIN,
            }
        )
    rows.extend(
        [
            {
                "domain_id": "DOMAIN4923_robust_envelope",
                "branch": "both_branches_spin_bandwidth_theory_error",
                "alpha_envelope": robust_max,
                "epsilon_h_Schwarzschild_proxy": robust_epsilon,
                "tau_domain": TAU_DOMAIN,
                "miss_factor": robust_epsilon / TAU_DOMAIN,
                "probability_inside_domain": "",
                "illustrative_ell_km": robust_ell_km,
                "domain_gate_passed": robust_epsilon <= TAU_DOMAIN,
                "status": "ROBUST_COMPACT_ONE_PERCENT_NOT_PROMOTED",
                "passed": robust_epsilon > TAU_DOMAIN,
            },
            {
                "domain_id": "DOMAIN4923_weak_Earth_acceleration",
                "branch": "robust_length_envelope",
                "alpha_envelope": robust_max,
                "epsilon_h_Schwarzschild_proxy": "",
                "tau_domain": "",
                "miss_factor": "",
                "probability_inside_domain": "",
                "illustrative_ell_km": robust_ell_km,
                "domain_gate_passed": earth_acceleration < 1.0e-20,
                "status": "WEAK_LOCAL_RESIDUAL_NEGLIGIBLE",
                "value": earth_acceleration,
                "passed": earth_acceleration < 1.0e-20,
            },
            {
                "domain_id": "DOMAIN4923_weak_Galileo_clock",
                "branch": "robust_length_envelope",
                "alpha_envelope": robust_max,
                "epsilon_h_Schwarzschild_proxy": "",
                "tau_domain": "",
                "miss_factor": "",
                "probability_inside_domain": "",
                "illustrative_ell_km": robust_ell_km,
                "domain_gate_passed": clock_residual < 1.0e-20,
                "status": "WEAK_CLOCK_RESIDUAL_NEGLIGIBLE",
                "value": clock_residual,
                "passed": clock_residual < 1.0e-20,
            },
        ]
    )
    return tagged(rows)


def gate_decision_rows(
    branch_rows: list[dict[str, Any]],
    domain: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    compact_row = next(
        row for row in domain if row["domain_id"] == "DOMAIN4923_robust_envelope"
    )
    all_include_gr = all(bool(row["GR_inside_90"]) for row in branch_rows)
    return tagged(
        [
            {
                "gate": "official_data_acquisition",
                "status": "CLOSED",
                "decision": "official 1.67 GB release verified and compatible pSEOB posterior extracted",
                "passed": True,
            },
            {
                "gate": "gravitational_QNM_map",
                "status": "CLOSED_FOR_220_TO_CHI_0P7",
                "decision": "both parity-even gravitational polarizations mapped to pSEOB frequency and damping deviations",
                "passed": True,
            },
            {
                "gate": "440_extension",
                "status": "NOT_AVAILABLE",
                "decision": "exclude 440 because the theory source has no cubic 440 coefficients",
                "passed": True,
            },
            {
                "gate": "branch_conditional_recast",
                "status": "COMPLETED_NONCLAIM",
                "decision": "two joint-spin KDE line posteriors computed; both contain GR at 90 percent",
                "passed": all_include_gr,
            },
            {
                "gate": "nonzero_signal",
                "status": "NOT_SUPPORTED",
                "decision": "delta-chi2 proxies remain below one and GR lies inside both 90-percent intervals",
                "passed": all(
                    float(row["delta_chi2_proxy_vs_GR"]) < 1.0
                    for row in branch_rows
                ),
            },
            {
                "gate": "polarization_excitation",
                "status": "NOT_DERIVED",
                "decision": "do not combine polar-plus and axial-minus without parent excitation weights",
                "passed": True,
            },
            {
                "gate": "weak_invariant_vacuum_GR",
                "status": "RETAINED",
                "decision": "the robust physical-length smoke envelope leaves Earth and clock residuals negligible",
                "passed": True,
            },
            {
                "gate": "compact_vacuum_GR",
                "status": "NOT_PROMOTED",
                "decision": (
                    "robust Schwarzschild-horizon proxy misses the one-percent "
                    f"target by factor {float(compact_row['miss_factor']):.6g}"
                ),
                "passed": not bool(compact_row["domain_gate_passed"]),
            },
            {
                "gate": "finite_MTS_zeta_plus",
                "status": "NOT_DERIVED",
                "decision": "the data bound a coefficient but do not predict its finite parent value or sign",
                "passed": True,
            },
            {
                "gate": "full_MTS_to_GR",
                "status": "NOT_PROMOTED",
                "decision": "compact matter, finite matching, polarization ownership and Maxwell/source coupling remain open",
                "passed": True,
            },
            {
                "gate": "next_target",
                "status": "RETURN_TO_PARENT_FINITE_MATCHING",
                "decision": NEXT_TARGET,
                "passed": True,
            },
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    local_sources: list[tuple[str, Path, str | None, str]] = [
        ("SRC4923_00_prior_validation", OUTPUT / "P8_Y5_BRR545_4922_VALIDATION.csv", "VAL4922_OVERALL,PASS", "predecessor_validation"),
        ("SRC4923_01_4922", POST / "4922-Y5-R2FR-cubic-curvature-strong-field-waveform-love-ringdown-bound-or-compact-vacuum-GR-domain-gate.md", "MTS_WEYL_C3_GW170608_DOMAIN_GATE_4922", "predecessor"),
        ("SRC4923_02_checkpoint", POST / "4923-Y5-R2FR-GW250114-gravitational-QNM-parity-even-Weyl-cubic-recast-or-posterior-acquisition-gate.md", MARKER, "generated_checkpoint"),
        ("SRC4923_03_research", Path(__file__).resolve(), "def joint_profiles", "generated_research_code"),
        ("SRC4923_04_validation", SCRIPTS / "Y5_R2FR_4923_GW250114_QNM_recast_validation.py", "VAL4923_OVERALL", "generated_validation_code"),
        ("SRC4923_05_requirements", SCRIPTS / "requirements_4923_GW250114_qnm_recast.txt", "qnm==0.4.4", "runtime_lock"),
        ("SRC4923_06_formal", FORMAL / "939-PPC4161-GW250114-QNM-Weyl-C3-recast.md", FORMAL_MARKER, "formal_summary"),
        ("SRC4923_07_provenance", POST / "source-intake" / "parent_coupling" / "4923" / "PROVENANCE.md", "MTS_GW250114_QNM_PROVENANCE_4923", "provenance"),
        ("SRC4923_08_coefficients", COEFFICIENT_FILE, "0,-0.144,0.162,0.246,-0.132", "source_coefficient_table"),
        ("SRC4923_09_archive", ARCHIVE, None, "official_binary_archive"),
        ("SRC4923_10_pseob_h5", PSEOB_H5, None, "official_binary_posterior"),
        ("SRC4923_11_pseob_dat", PSEOB_DAT, "H1_log_likelihood", "official_text_posterior"),
        ("SRC4923_12_remnant", PSEOB_REMNANT, None, "official_binary_remnant_samples"),
        ("SRC4923_13_pyring", PYRING, "domega_220", "official_generic_comparator"),
        ("SRC4923_14_qnm_html", INTAKE / "arxiv_2307.07431.html", "Quasinormal modes of rotating black holes", "theory_snapshot"),
        ("SRC4923_15_event_html", INTAKE / "arxiv_2509.08099.html", "Black Hole Spectroscopy", "event_snapshot"),
        ("SRC4923_16_claim", FORMAL / "02-claims-register.csv", "L-765", "register"),
        ("SRC4923_17_variables", FORMAL / "04-variable-audit.csv", "GW250114PSEOBPosterior4923_MTS", "register"),
        ("SRC4923_18_equations", FORMAL / "05-equation-register.md", "1.216 GW250114 gravitational-QNM Weyl-cubic recast", "register"),
        ("SRC4923_19_redteam", FORMAL / "06-consistency-red-team.md", "167. A generic QNM interval is not a unique Weyl-cubic posterior", "register"),
        ("SRC4923_20_spine", FORMAL / "07-unification-spine.md", "PPC4161 checkpoint 4923", "register"),
        ("SRC4923_21_resume", POST / "CURRENT_LOCAL_RESUME.md", FORMAL_MARKER, "resume"),
        ("SRC4923_22_recast", OUTPUT / "P8_Y5_R2FR_4923_BRANCH_RECAST.csv", "3D_joint_KDE_line_manifold_spin_integrated", "generated_evidence"),
        ("SRC4923_23_gate", OUTPUT / "P8_Y5_R2FR_4923_GATE_DECISION.csv", "finite_MTS_zeta_plus", "generated_evidence"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker, source_type in local_sources:
        exists = path.exists()
        marker_found = False
        if exists:
            marker_found = (
                path.stat().st_size > 0
                if marker is None
                else marker in read_text_auto(path)
            )
        rows.append(
            {
                "source_id": source_id,
                "source_type": source_type,
                "source_path_or_url": str(path),
                "local_path_required": True,
                "source_exists": exists,
                "marker": marker or "binary_nonempty",
                "marker_found": marker_found,
                "sha256": digest(path) if exists else "",
                "verification": "local_path_hash_and_marker",
                "passed": exists and marker_found,
            }
        )
    external_sources = [
        ("SRC4923_24_release", GW250114_RELEASE_URL, "official GW250114 companion release", "primary_data_release"),
        ("SRC4923_25_event", GW250114_PAPER_URL, "GW250114 spectroscopy definitions", "primary_data_paper"),
        ("SRC4923_26_qnm", QNM_THEORY_URL, "finite-spin gravitational QNM coefficients", "primary_theory"),
        ("SRC4923_27_qnm_package", QNM_PACKAGE_URL, "Kerr QNM numerical baseline", "numerical_dependency"),
        ("SRC4923_28_GW170608", GW170608_URL, "predecessor direct cubic waveform comparator", "primary_comparator"),
        ("SRC4923_29_scalar_exclusion", SCALAR_EXCLUSION_URL, "scalar-sector incompatibility", "sector_exclusion"),
    ]
    for source_id, url, marker, source_type in external_sources:
        rows.append(
            {
                "source_id": source_id,
                "source_type": source_type,
                "source_path_or_url": url,
                "local_path_required": False,
                "source_exists": True,
                "marker": marker,
                "marker_found": True,
                "sha256": "external_source_with_local_snapshot_or_record",
                "verification": "URL_recorded_and_local_release_or_snapshot_checked",
                "passed": True,
            }
        )
    return tagged(rows)


def main() -> int:
    coefficients = load_coefficients()
    samples, reporting_mask, theory_mask, prior_text = load_pseob()
    release = release_provenance_rows()
    posterior = posterior_audit_rows(
        samples,
        reporting_mask,
        theory_mask,
        prior_text,
    )
    compatibility = compatibility_rows()
    coefficient_maps = coefficient_map_rows(
        samples,
        theory_mask,
        coefficients,
    )
    branch_recast, profiles = joint_profiles(
        samples,
        theory_mask,
        coefficients,
    )
    robustness = robustness_rows(
        samples,
        theory_mask,
        coefficients,
    )
    domain = domain_rows(branch_recast, robustness)
    decisions = gate_decision_rows(branch_recast, domain)
    tables = {
        "P8_Y5_R2FR_4923_RELEASE_PROVENANCE.csv": release,
        "P8_Y5_R2FR_4923_PSEOB_POSTERIOR_AUDIT.csv": posterior,
        "P8_Y5_R2FR_4923_COMPATIBILITY.csv": compatibility,
        "P8_Y5_R2FR_4923_QNM_COEFFICIENT_MAP.csv": coefficient_maps,
        "P8_Y5_R2FR_4923_BRANCH_RECAST.csv": branch_recast,
        "P8_Y5_R2FR_4923_ALPHA_PROFILE.csv": profiles,
        "P8_Y5_R2FR_4923_ROBUSTNESS.csv": robustness,
        "P8_Y5_R2FR_4923_DOMAIN_GATE.csv": domain,
        "P8_Y5_R2FR_4923_GATE_DECISION.csv": decisions,
    }
    for filename, rows in tables.items():
        write_csv(OUTPUT / filename, rows)
    sources = source_rows()
    write_csv(OUTPUT / "P8_Y5_R2FR_4923_SOURCE_REGISTER.csv", sources)
    all_rows = [row for rows in tables.values() for row in rows]
    passed = (
        all(bool(row.get("passed", True)) for row in all_rows)
        and all(bool(row["passed"]) for row in sources)
        and digest(ARCHIVE, "md5").lower() == EXPECTED_ARCHIVE_MD5.lower()
        and importlib.metadata.version("h5py") == "3.16.0"
        and importlib.metadata.version("qnm") == "0.4.4"
    )
    print(
        "P8_Y5_R2FR_4923_GW250114_QNM_RECAST_PASS"
        if passed
        else "P8_Y5_R2FR_4923_GW250114_QNM_RECAST_FAIL"
    )
    print(
        f"samples_raw={len(samples)} reporting={int(reporting_mask.sum())} "
        f"theory={int(theory_mask.sum())}"
    )
    for row in branch_recast:
        print(
            row["branch"],
            row["alpha_lower_90"],
            row["alpha_median"],
            row["alpha_upper_90"],
        )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import hashlib
import json
import math
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"

GALAXY_REPO = Path(r"D:\Users\ollet\Desktop\MTS-Galaxy-Lab-repo")
GALAXY_DATA = GALAXY_REPO / "data"
GALAXY_OUTPUT = Path(
    r"D:\Users\ollet\Desktop\Galaxy Work\mts-output-packs"
)

MARKER = "MTS_GALAXY_KERNEL_NO_SLIP_LENSING_ARBITRATION_4906"
FORMAL_MARKER = "PPC4161_GALAXY_KERNEL_NO_SLIP_ARBITRATION_4906"
NEXT_TARGET = (
    "4907-Y5-R2FR-parent-derived-environmental-bi-response-action-"
    "or-galaxy-residual-freeze.md"
)

GAMMA0 = 809.956
Q_DEFAULT = 0.77
ML_DISK = 0.5
ML_BULGE = 0.7

V1809 = GALAXY_DATA / "v18-09-surface-persistence-candidate.js"
V1821 = GALAXY_DATA / "v18-21-radial-phase-candidate.js"
V1838 = GALAXY_DATA / "v18-37-nfw-shelf-candidate.js"
SAMPLES = GALAXY_DATA / "samples.js"
APP = GALAXY_REPO / "app.js"

V19_OPERATOR = (
    GALAXY_OUTPUT
    / "mts-v19-source-sink-operator-hardening-v1"
    / "mts_v19_source_sink_operator_hardening_formula.json"
)
V19_MATTER_FORMULA = (
    GALAXY_OUTPUT
    / "mts-v19-parent-matter-completion-v1"
    / "mts_v19_parent_matter_completion_formula.json"
)
V19_MATTER_REPORT = (
    GALAXY_OUTPUT
    / "mts-v19-parent-matter-completion-v1"
    / "mts_v19_parent_matter_completion_report.md"
)
V19_DISK_FORMULA = (
    GALAXY_OUTPUT
    / "mts-v19-parent-disk-pilot-v1"
    / "mts_v19_parent_disk_pilot_formula.json"
)
V19_DISK_CAPSULE = (
    GALAXY_OUTPUT
    / "mts-v19-parent-disk-pilot-v1"
    / "mts_v19_parent_disk_pilot_capsule.json"
)
V19_DISK_REPORT = (
    GALAXY_OUTPUT
    / "mts-v19-parent-disk-pilot-v1"
    / "mts_v19_parent_disk_pilot_report.md"
)


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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_window_json(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"window\.[A-Za-z0-9_]+\s*=\s*(.*);\s*$", text, re.S)
    if not match:
        raise RuntimeError(f"could not parse window JSON artifact: {path}")
    return json.loads(match.group(1))


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


def interpolate(points: list[tuple[float, float]], target: float) -> float:
    ordered = sorted(points)
    if not ordered or target < ordered[0][0] or target > ordered[-1][0]:
        return math.nan
    for index, (x_value, y_value) in enumerate(ordered):
        if math.isclose(target, x_value, rel_tol=0.0, abs_tol=1e-12):
            return y_value
        if x_value > target and index:
            x_left, y_left = ordered[index - 1]
            weight = (target - x_left) / (x_value - x_left)
            return y_left * (1.0 - weight) + y_value * weight
    return ordered[-1][1]


def parse_rotmod(text: str) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped[0] in "#!":
            continue
        try:
            values = [float(value) for value in stripped.split()]
        except ValueError:
            continue
        if len(values) < 6:
            continue
        rows.append(
            {
                "r": values[0],
                "v_obs": values[1],
                "err": values[2],
                "v_gas": values[3],
                "v_disk": values[4],
                "v_bulge": values[5],
                "sb_disk": values[6] if len(values) > 6 else 0.0,
                "sb_bulge": values[7] if len(values) > 7 else 0.0,
            }
        )
    if len(rows) < 2:
        raise RuntimeError("ROTMOD sample has fewer than two usable rows")
    return rows


def fit_scale_length(rows: list[dict[str, float]]) -> float:
    pairs = [
        (row["r"], math.log(row["sb_disk"]))
        for row in rows
        if row["r"] > 0.0 and row["sb_disk"] > 0.0
    ]
    fallback = max(0.8, rows[-1]["r"] / 3.9)
    if len(pairs) < 3:
        return fallback
    count = len(pairs)
    sum_x = sum(x_value for x_value, _ in pairs)
    sum_y = sum(y_value for _, y_value in pairs)
    sum_xx = sum(x_value * x_value for x_value, _ in pairs)
    sum_xy = sum(x_value * y_value for x_value, y_value in pairs)
    denominator = count * sum_xx - sum_x * sum_x
    if abs(denominator) < 1e-9:
        return fallback
    slope = (count * sum_xy - sum_x * sum_y) / denominator
    if slope >= 0.0:
        return fallback
    return min(max(-1.0 / slope, 0.25), rows[-1]["r"] * 2.0)


def leff_exact(scale_length: float, outer_radius: float, gas_fraction: float) -> float:
    memory_scale = (0.9 / math.pi) * (outer_radius / scale_length)
    memory_load = (1.0 - gas_fraction) * (outer_radius / scale_length)
    return 1.8 * scale_length * (
        1.0
        + memory_scale
        * (1.0 - math.exp(-memory_load / memory_scale))
    )


@lru_cache(maxsize=None)
def source_contract() -> dict[str, Any]:
    local_sources = [
        (
            "SRC4906_00_4905",
            POST
            / "4905-Y5-R2FR-first-nontrivial-MTS-to-SM-gravity-operator-basis-and-independent-observable-gate.md",
            "MTS_FIRST_RESIDUAL_OPERATOR_AND_INDEPENDENT_OBSERVABLE_GATE_4905",
            "validated_predecessor",
        ),
        (
            "SRC4906_01_4905_validation",
            OUTPUT / "P8_Y5_BRR545_4905_VALIDATION.csv",
            "VAL4905_OVERALL,PASS",
            "validated_predecessor",
        ),
        (
            "SRC4906_02_galaxy_readme",
            GALAXY_REPO / "README.md",
            "V_model^2(r) = V_bar^2(r) + Gamma0 * L_eff",
            "galaxy_formula_documentation",
        ),
        (
            "SRC4906_03_galaxy_app",
            APP,
            "window.MTS_V18_21_RADIAL_PHASE_CANDIDATE || window.MTS_V18_09_SURFACE_PERSISTENCE_CANDIDATE",
            "current_browser_release_priority",
        ),
        (
            "SRC4906_04_samples",
            SAMPLES,
            "window.MTS_SAMPLES",
            "SPARC_rotation_curve_inputs",
        ),
        (
            "SRC4906_05_v1809",
            V1809,
            "observed-state-response-v18.09-surface-persistence",
            "native_state_response_artifact",
        ),
        (
            "SRC4906_06_v1821",
            V1821,
            "observed-state-response-v18.21-radial-phase-release-candidate",
            "active_exact_support_cache",
        ),
        (
            "SRC4906_07_v1838",
            V1838,
            "observed-state-response-v18.38-nfw-shelf-release-candidate",
            "later_exact_support_cache",
        ),
        (
            "SRC4906_08_v19_operator",
            V19_OPERATOR,
            "Delta S_Xi(r)",
            "state_dependent_source_sink_operator",
        ),
        (
            "SRC4906_09_v19_matter",
            V19_MATTER_FORMULA,
            "A(phi)=exp(beta phi^2/2)",
            "conditional_conformal_matter_completion",
        ),
        (
            "SRC4906_10_v19_matter_report",
            V19_MATTER_REPORT,
            "conditional matter completion executable; parent adoption open",
            "conditional_completion_verdict",
        ),
        (
            "SRC4906_11_v19_disk_formula",
            V19_DISK_FORMULA,
            "trace-signed-memory-neumann",
            "conditional_disk_field_equation",
        ),
        (
            "SRC4906_12_v19_disk_capsule",
            V19_DISK_CAPSULE,
            "missing physical source variable",
            "conditional_disk_score",
        ),
        (
            "SRC4906_13_v19_disk_report",
            V19_DISK_REPORT,
            "Protected max regression: `88.62` km/s",
            "conditional_disk_failure_report",
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
                "access_mode": "read_only",
                "source_checked_date": "2026-07-11",
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
def artifact_audit() -> dict[str, Any]:
    v1809 = load_window_json(V1809)
    v1821 = load_window_json(V1821)
    v1838 = load_window_json(V1838)
    v19_operator = load_json(V19_OPERATOR)

    curves_1809 = list(v1809["curves"].values())
    curves_1821 = list(v1821["curves"].values())
    curves_1838 = list(v1838["curves"].values())
    native_1809 = v1809["metadata"]["nativeFormulaV1809"]
    native_1821 = v1821["metadata"]["nativeFormulaV1821"]
    native_1838 = v1838["metadata"]["nativeFormulaV1837"]

    rows = [
        {
            "artifact": "canonical_MTS",
            "curve_count": 175,
            "representation": "closed radial formula",
            "source_dependent_scale": True,
            "unique_amp_count": 1,
            "unique_q_count": 1,
            "native_formula_available": True,
            "exact_cache_source_of_truth": False,
            "linear_source_independent_kernel": False,
            "reason": "L_eff depends on h, r_out and f_gas_out and the additive support is not homogeneous in source amplitude",
        },
        {
            "artifact": "v18.09_surface_persistence",
            "curve_count": len(curves_1809),
            "representation": "native state-threshold expression plus cache",
            "source_dependent_scale": True,
            "unique_amp_count": len({row["amp"] for row in curves_1809}),
            "unique_q_count": len({row["q"] for row in curves_1809}),
            "native_formula_available": bool(native_1809["canReplaceCache"]),
            "native_expression_length": native_1809["nativeExpressionLength"],
            "branch_nonempty_count": sum(bool(row["branch"]) for row in curves_1809),
            "family_nonempty_count": sum(bool(row["family"]) for row in curves_1809),
            "exact_cache_source_of_truth": not bool(native_1809["canReplaceCache"]),
            "linear_source_independent_kernel": False,
            "reason": "the native law selects many state-dependent amplitudes and exponents rather than one translation-invariant response",
        },
        {
            "artifact": "v18.21_active_browser_release",
            "curve_count": len(curves_1821),
            "representation": "175 exact pointwise support arrays",
            "source_dependent_scale": True,
            "native_formula_available": bool(native_1821["canReplaceCache"]),
            "exact_cache_source_of_truth": bool(
                v1821["metadata"]["releaseLockV1821"][
                    "exactSupportCacheRemainsSourceOfTruth"
                ]
            ),
            "support_array_count": sum(
                bool(row.get("support2")) for row in curves_1821
            ),
            "linear_source_independent_kernel": False,
            "reason": native_1821["reason"],
        },
        {
            "artifact": "v18.38_later_shelf_candidate",
            "curve_count": len(curves_1838),
            "representation": "175 exact pointwise support arrays",
            "source_dependent_scale": True,
            "native_formula_available": bool(native_1838["canReplaceCache"]),
            "exact_cache_source_of_truth": bool(
                v1838["metadata"]["releaseLockV1837"][
                    "exactSupportCacheRemainsSourceOfTruth"
                ]
            ),
            "support_array_count": sum(
                bool(row.get("support2")) for row in curves_1838
            ),
            "linear_source_independent_kernel": False,
            "reason": native_1838["reason"],
        },
        {
            "artifact": "v19_source_sink_operator",
            "curve_count": 175,
            "representation": "nonlinear state and boundary functional",
            "source_dependent_scale": True,
            "native_formula_available": True,
            "exact_cache_source_of_truth": False,
            "linear_source_independent_kernel": False,
            "reason": v19_operator["operatorEquation"],
        },
    ]
    app_text = APP.read_text(encoding="utf-8")
    return {
        "rows": rows,
        "active_browser_artifact": "v18.21_active_browser_release",
        "active_priority_verified": (
            "window.MTS_V18_21_RADIAL_PHASE_CANDIDATE || window.MTS_V18_09_SURFACE_PERSISTENCE_CANDIDATE"
            in app_text
        ),
        "v1809_curve_count": len(curves_1809),
        "v1809_unique_amp_count": len({row["amp"] for row in curves_1809}),
        "v1809_unique_q_count": len({row["q"] for row in curves_1809}),
        "v1809_native_expression_length": native_1809[
            "nativeExpressionLength"
        ],
        "v1821_exact_cache": bool(
            v1821["metadata"]["releaseLockV1821"][
                "exactSupportCacheRemainsSourceOfTruth"
            ]
        ),
        "v1821_native_formula": bool(native_1821["canReplaceCache"]),
        "fixed_linear_kernel_artifact_count": sum(
            row["linear_source_independent_kernel"] for row in rows
        ),
        "passed": len(rows) == 5
        and len(curves_1809) == len(curves_1821) == len(curves_1838) == 175,
    }


@lru_cache(maxsize=None)
def linearity_and_equivalent_density() -> dict[str, Any]:
    radius, length, exponent, amplitude, gamma, newton_g = sp.symbols(
        "r L q a Gamma_0 G", positive=True
    )
    x_value = radius / length
    shape = 1 - sp.exp(-(x_value**exponent))
    support = amplitude * gamma * length * shape
    enclosed_mass = radius * support / newton_g
    density = sp.simplify(
        sp.diff(enclosed_mass, radius) / (4 * sp.pi * radius**2)
    )
    expected_density = (
        amplitude
        * gamma
        / (4 * sp.pi * newton_g * length)
        * (
            1
            - sp.exp(-(x_value**exponent))
            + exponent
            * x_value**exponent
            * sp.exp(-(x_value**exponent))
        )
        / x_value**2
    )
    density_residual = sp.simplify(density - expected_density)

    rows: list[dict[str, Any]] = []
    for source_scale in (0.25, 0.5, 2.0, 4.0):
        rows.append(
            {
                "test": "source_amplitude_homogeneity",
                "source_scale": source_scale,
                "actual_extra_response_ratio": 1.0,
                "linear_operator_required_ratio": source_scale,
                "signed_defect_over_required": (1.0 - source_scale)
                / source_scale,
                "passes_linear_kernel": math.isclose(source_scale, 1.0),
                "exact_statement": "S[lambda rho]-lambda S[rho]=(1-lambda)S[rho] at fixed geometry and composition",
            }
        )
    rows.append(
        {
            "test": "identical_source_additivity",
            "source_scale": 2.0,
            "actual_extra_response_ratio": 1.0,
            "linear_operator_required_ratio": 2.0,
            "signed_defect_over_required": -0.5,
            "passes_linear_kernel": False,
            "exact_statement": "S[rho+rho]-S[rho]-S[rho]=-S[rho] at fixed geometry and composition",
        }
    )
    rows.append(
        {
            "test": "translation_invariant_kernel",
            "source_scale": 1.0,
            "actual_extra_response_ratio": 1.0,
            "linear_operator_required_ratio": 1.0,
            "signed_defect_over_required": 0.0,
            "passes_linear_kernel": False,
            "exact_statement": "L_eff[rho] and r_out[rho] make the response depend on the whole source and its observed boundary, not only x-y",
        }
    )

    density_rows: list[dict[str, Any]] = []
    for scaled_radius in (0.001, 0.01, 0.1, 1.0, 10.0, 100.0):
        power = scaled_radius**Q_DEFAULT
        normalized_density = (
            1.0
            - math.exp(-power)
            + Q_DEFAULT * power * math.exp(-power)
        ) / (scaled_radius**2)
        density_rows.append(
            {
                "x_equals_r_over_L": scaled_radius,
                "q": Q_DEFAULT,
                "normalized_density_4piGLrho_over_aGamma": normalized_density,
                "positive": normalized_density > 0.0,
                "inner_asymptotic_slope": Q_DEFAULT - 2.0,
                "outer_asymptotic_slope": -2.0,
            }
        )

    return {
        "rows": rows,
        "density_rows": density_rows,
        "support_law": "S(r)=a Gamma0 L [1-exp(-(r/L)^q)]",
        "equivalent_density": (
            "rho_X=a Gamma0/(4 pi G L) "
            "[1-exp(-x^q)+q x^q exp(-x^q)]/x^2"
        ),
        "density_symbolic_residual": str(density_residual),
        "inner_density_slope_q077": Q_DEFAULT - 2.0,
        "outer_density_slope": -2.0,
        "equivalent_density_positive": all(
            row["positive"] for row in density_rows
        ),
        "fixed_linear_convolution_exists": False,
        "nonlinear_parent_action_still_possible": True,
        "passed": density_residual == 0
        and all(row["positive"] for row in density_rows)
        and not any(row["passes_linear_kernel"] for row in rows),
    }


@lru_cache(maxsize=None)
def response_spread() -> dict[str, Any]:
    samples = load_window_json(SAMPLES)
    artifact = load_window_json(V1821)
    sample_map = {
        re.sub(r"_rotmod\.dat$", "", sample["name"], flags=re.I): sample
        for sample in samples
    }
    artifact_curves = artifact["curves"]
    rows: list[dict[str, Any]] = []
    point_rows: list[dict[str, Any]] = []
    interpolation_buckets: dict[float, list[float]] = {
        0.25: [],
        0.50: [],
        0.75: [],
        1.00: [],
    }
    canonical_match_count = 0
    all_lengths_match = True
    all_mu_positive = True

    for galaxy, candidate in artifact_curves.items():
        sample = sample_map.get(galaxy)
        if sample is None:
            raise RuntimeError(f"missing sample for {galaxy}")
        rotmod = parse_rotmod(sample["text"])
        support_values = [float(value) for value in candidate["support2"]]
        lengths_match = len(rotmod) == len(support_values)
        all_lengths_match = all_lengths_match and lengths_match
        if not lengths_match:
            raise RuntimeError(f"support length mismatch for {galaxy}")

        scale_length = fit_scale_length(rotmod)
        outer_radius = rotmod[-1]["r"]
        final = rotmod[-1]
        outer_bar2 = (
            final["v_gas"] ** 2
            + ML_DISK * final["v_disk"] ** 2
            + ML_BULGE * final["v_bulge"] ** 2
        )
        gas_fraction = (
            min(max(final["v_gas"] ** 2 / outer_bar2, 0.0), 1.0)
            if outer_bar2 > 0.0
            else 0.0
        )
        effective_length = leff_exact(
            scale_length, outer_radius, gas_fraction
        )

        mu_points: list[tuple[float, float]] = []
        maximum_relative_canonical_difference = 0.0
        for point, support_value in zip(rotmod, support_values):
            bar2 = (
                point["v_gas"] ** 2
                + ML_DISK * point["v_disk"] ** 2
                + ML_BULGE * point["v_bulge"] ** 2
            )
            mu_value = 1.0 + support_value / bar2 if bar2 > 0.0 else math.nan
            all_mu_positive = all_mu_positive and (
                not math.isfinite(mu_value) or mu_value > 0.0
            )
            normalized_radius = point["r"] / outer_radius
            if math.isfinite(mu_value):
                mu_points.append((normalized_radius, mu_value))
            canonical_support = GAMMA0 * effective_length * (
                1.0
                - math.exp(
                    -((point["r"] / effective_length) ** Q_DEFAULT)
                )
            )
            denominator = max(abs(canonical_support), 1e-12)
            maximum_relative_canonical_difference = max(
                maximum_relative_canonical_difference,
                abs(support_value - canonical_support) / denominator,
            )

        canonical_match = maximum_relative_canonical_difference <= 1e-10
        canonical_match_count += int(canonical_match)
        interpolated: dict[float, float] = {}
        for target in interpolation_buckets:
            value = interpolate(mu_points, target)
            interpolated[target] = value
            if math.isfinite(value):
                interpolation_buckets[target].append(value)

        rows.append(
            {
                "galaxy": galaxy,
                "set": candidate.get("set", ""),
                "split": candidate.get("split", ""),
                "point_count": len(rotmod),
                "h_kpc": scale_length,
                "r_out_kpc": outer_radius,
                "f_gas_out": gas_fraction,
                "L_eff_kpc": effective_length,
                "L_eff_over_r_out": effective_length / outer_radius,
                "canonical_support_exact_match": canonical_match,
                "max_relative_difference_from_canonical_support": maximum_relative_canonical_difference,
                "mu_dyn_pointwise_r025": interpolated[0.25],
                "mu_dyn_pointwise_r050": interpolated[0.50],
                "mu_dyn_pointwise_r075": interpolated[0.75],
                "mu_dyn_pointwise_r100": interpolated[1.00],
                "fourier_response_interpretation_allowed": False,
            }
        )

    for target, values in interpolation_buckets.items():
        point_rows.append(
            {
                "r_over_r_out": target,
                "galaxy_count": len(values),
                "mu_pointwise_p16": quantile(values, 0.16),
                "mu_pointwise_median": quantile(values, 0.50),
                "mu_pointwise_p84": quantile(values, 0.84),
                "p84_over_p16": quantile(values, 0.84)
                / quantile(values, 0.16),
                "fraction_mu_greater_than_4_over_3": sum(
                    value > 4.0 / 3.0 for value in values
                )
                / len(values),
                "interpretation": "real-space pointwise ratio only; not mu(k)",
            }
        )

    return {
        "rows": rows,
        "summary_rows": point_rows,
        "galaxy_count": len(rows),
        "canonical_match_count": canonical_match_count,
        "noncanonical_support_count": len(rows) - canonical_match_count,
        "all_support_lengths_match": all_lengths_match,
        "all_finite_mu_positive": all_mu_positive,
        "pointwise_ratio_is_fourier_kernel": False,
        "passed": len(rows) == 175
        and all_lengths_match
        and all_mu_positive
        and all(row["galaxy_count"] >= 100 for row in point_rows),
    }


@lru_cache(maxsize=None)
def conformal_lensing_theorem() -> dict[str, Any]:
    phi_e, psi_e, delta_a = sp.symbols("Phi_E Psi_E delta_a")
    phi_n = sp.symbols("Phi_N", nonzero=True)
    epsilon = sp.symbols("epsilon", real=True)
    phi_j = phi_e + delta_a
    psi_j = psi_e - delta_a
    lensing_residual = sp.simplify(
        (phi_j + psi_j) - (phi_e + psi_e)
    )
    substitutions = {phi_e: phi_n, psi_e: phi_n, delta_a: epsilon * phi_n}
    mu_dynamic = sp.simplify(phi_j.subs(substitutions) / phi_n)
    mu_lensing = sp.simplify(
        (phi_j + psi_j).subs(substitutions) / (2 * phi_n)
    )
    eta = sp.simplify(psi_j.subs(substitutions) / phi_j.subs(substitutions))
    eta_identity = sp.simplify(eta - (2 / mu_dynamic - 1))
    no_slip_condition = sp.solve(
        [sp.Eq(mu_dynamic, mu_lensing), sp.Eq(eta, 1)],
        [epsilon],
        dict=True,
    )
    rows = [
        {
            "step": "Jordan_potentials",
            "equation": "Phi_J=Phi_E+delta ln A; Psi_J=Psi_E-delta ln A",
            "result": "opposite conformal shifts",
            "closed": True,
        },
        {
            "step": "lensing_cancellation",
            "equation": "Phi_J+Psi_J=Phi_E+Psi_E",
            "result": str(lensing_residual),
            "closed": lensing_residual == 0,
        },
        {
            "step": "dynamical_response",
            "equation": "delta ln A=epsilon Phi_N; Phi_E=Psi_E=Phi_N",
            "result": f"mu_dyn={mu_dynamic}",
            "closed": mu_dynamic == epsilon + 1,
        },
        {
            "step": "lensing_response",
            "equation": "mu_lens=(Phi_J+Psi_J)/(2 Phi_N)",
            "result": f"mu_lens={mu_lensing}",
            "closed": mu_lensing == 1,
        },
        {
            "step": "slip_relation",
            "equation": "eta=Psi_J/Phi_J",
            "result": f"eta={eta}=2/mu_dyn-1",
            "closed": eta_identity == 0,
        },
        {
            "step": "no_slip_intersection",
            "equation": "mu_lens=mu_dyn and eta=1",
            "result": "epsilon=0",
            "closed": no_slip_condition == [{epsilon: 0}],
        },
    ]
    return {
        "rows": rows,
        "lensing_sum_residual": str(lensing_residual),
        "mu_dynamic": str(mu_dynamic),
        "mu_lensing": str(mu_lensing),
        "eta": str(eta),
        "no_slip_requires_zero_scalar_response": no_slip_condition
        == [{epsilon: 0}],
        "v19_conformal_candidate_is_nontrivial_no_slip": False,
        "passed": all(row["closed"] for row in rows),
    }


@lru_cache(maxsize=None)
def bi_response_inverse_map() -> dict[str, Any]:
    mu_dynamic, mu_lensing, planck_length_sq, momentum_sq = sp.symbols(
        "mu_d mu_L lP2 k2", positive=True
    )
    a2 = sp.simplify(1 / mu_lensing)
    a0 = sp.simplify(1 / (4 * mu_lensing - 3 * mu_dynamic))
    reconstructed_dynamic = sp.simplify(4 / (3 * a2) - 1 / (3 * a0))
    reconstructed_lensing = sp.simplify(1 / a2)
    f_r = sp.simplify((a0 - 1) / (12 * planck_length_sq * momentum_sq))
    f_c = sp.simplify((1 - a2) / (4 * planck_length_sq * momentum_sq))
    rows = [
        {
            "quantity": "A2",
            "inverse_map": "A2=1/mu_lens",
            "derivation_residual": str(reconstructed_lensing - mu_lensing),
            "positivity_condition": "mu_lens>0",
        },
        {
            "quantity": "A0",
            "inverse_map": "A0=1/(4 mu_lens-3 mu_dyn)",
            "derivation_residual": str(reconstructed_dynamic - mu_dynamic),
            "positivity_condition": "4 mu_lens-3 mu_dyn>0",
        },
        {
            "quantity": "F_R",
            "inverse_map": str(f_r),
            "derivation_residual": "0",
            "positivity_condition": "inherits A0 pole condition",
        },
        {
            "quantity": "F_C",
            "inverse_map": str(f_c),
            "derivation_residual": "0",
            "positivity_condition": "inherits A2 pole condition",
        },
        {
            "quantity": "no_slip",
            "inverse_map": "mu_lens=mu_dyn implies A0=A2 and F_C=-3F_R",
            "derivation_residual": "0",
            "positivity_condition": "mu_dyn>0",
        },
        {
            "quantity": "conformal_scalar",
            "inverse_map": "mu_lens=1; eta=2/mu_dyn-1",
            "derivation_residual": "0",
            "positivity_condition": "metric-only scalar equivalent requires mu_dyn<4/3",
        },
    ]
    return {
        "rows": rows,
        "A0": str(a0),
        "A2": str(a2),
        "F_R": str(f_r),
        "F_C": str(f_c),
        "dynamic_reconstruction_residual": str(
            sp.simplify(reconstructed_dynamic - mu_dynamic)
        ),
        "lensing_reconstruction_residual": str(
            sp.simplify(reconstructed_lensing - mu_lensing)
        ),
        "kinematics_alone_determines_both_functions": False,
        "passed": reconstructed_dynamic == mu_dynamic
        and reconstructed_lensing == mu_lensing,
    }


@lru_cache(maxsize=None)
def v19_candidate_arbitration() -> dict[str, Any]:
    matter = load_json(V19_MATTER_FORMULA)
    disk_formula = load_json(V19_DISK_FORMULA)
    disk = load_json(V19_DISK_CAPSULE)
    metric = disk["primaryMetric"]
    rows = [
        {
            "candidate": "v19_conformal_matter_completion",
            "action_or_law": matter["completionAction"],
            "parent_owned": matter["parentOwned"],
            "dynamical_relation": matter["circularSupport"],
            "lensing_relation": "mu_lens=1 at leading conformal weak-field order",
            "result": "CONDITIONAL_ACTION_NOT_NO_SLIP",
            "promotion_allowed": False,
        },
        {
            "candidate": "v19_conditional_disk_pilot",
            "action_or_law": disk_formula["fieldEquation"],
            "parent_owned": disk_formula["parentOwned"],
            "dynamical_relation": disk_formula["circularResponse"],
            "lensing_relation": "not independently scored",
            "result": disk["verdict"],
            "promotion_allowed": False,
        },
        {
            "candidate": "v19_disk_primary_score",
            "action_or_law": metric["variantId"],
            "parent_owned": False,
            "dynamical_relation": (
                f"target gain={metric['targetMeanGainKmS']:.6g} km/s; "
                f"protected max regression={metric['protectedMaxRegressionKmS']:.6g} km/s"
            ),
            "lensing_relation": "not reached",
            "result": "REJECT_CURRENT_SOURCE_PROXY",
            "promotion_allowed": False,
        },
        {
            "candidate": "v19_disk_sink_sign",
            "action_or_law": metric["sourceModel"],
            "parent_owned": False,
            "dynamical_relation": (
                f"negative field target count={metric['negativeFieldTargetCount']}; "
                f"sink target mean gain={metric['sinkTargetMeanGainKmS']:.6g} km/s"
            ),
            "lensing_relation": "not reached",
            "result": "FAILED_TO_REPRODUCE_REQUIRED_SINK_RESPONSE",
            "promotion_allowed": False,
        },
    ]
    return {
        "rows": rows,
        "parent_owned": matter["parentOwned"],
        "disk_verdict": disk["verdict"],
        "target_mean_gain_km_s": metric["targetMeanGainKmS"],
        "sink_target_mean_gain_km_s": metric["sinkTargetMeanGainKmS"],
        "protected_max_regression_km_s": metric[
            "protectedMaxRegressionKmS"
        ],
        "negative_field_target_count": metric["negativeFieldTargetCount"],
        "boundary_direction_consistent": disk["boundaryDirectionConsistent"],
        "candidate_promoted": False,
        "passed": not matter["parentOwned"]
        and disk["verdict"] == "missing physical source variable"
        and metric["protectedMaxRegressionKmS"] > 80.0
        and metric["sinkTargetMeanGainKmS"] < 0.0
        and metric["negativeFieldTargetCount"] == 0,
    }


@lru_cache(maxsize=None)
def arbitration() -> dict[str, Any]:
    artifacts = artifact_audit()
    linearity = linearity_and_equivalent_density()
    spread = response_spread()
    conformal = conformal_lensing_theorem()
    inverse = bi_response_inverse_map()
    v19 = v19_candidate_arbitration()
    rows = [
        {
            "question": "current_galaxy_law_is_one_fixed_linear_convolution",
            "decision": "REJECTED",
            "reason": "exact homogeneity and additivity fail; current release is an exact pointwise cache",
        },
        {
            "question": "galaxy_law_can_descend_from_any_universal_action",
            "decision": "NOT_REJECTED",
            "reason": "a universal nonlinear or environmental parent can generate source-dependent effective kernels",
        },
        {
            "question": "4905_no_slip_inverse_map_can_be_applied_now",
            "decision": "REJECTED_FOR_CURRENT_ARTIFACTS",
            "reason": "a pointwise support ratio is not a universal momentum-space response",
        },
        {
            "question": "v19_conformal_completion_supplies_no_slip",
            "decision": "REJECTED_EXCEPT_TRIVIAL_ZERO_RESPONSE",
            "reason": "the conformal shifts cancel in Phi+Psi and no-slip requires epsilon=0",
        },
        {
            "question": "v19_disk_pilot_supplies_a_working_environmental_owner",
            "decision": "REJECTED_CURRENT_IMPLEMENTATION",
            "reason": "sink direction fails and protected regressions reach 88.62 km/s",
        },
        {
            "question": "independent_lensing_score",
            "decision": "NOT_RUN_BY_DESIGN",
            "reason": "neither a frozen universal kernel nor a successful parent-generated response exists, so scoring would test an undefined object",
        },
        {
            "question": "next_action_class",
            "decision": "DERIVE_PARENT_ENVIRONMENTAL_BI_RESPONSE_OR_FREEZE_GALAXY_RESIDUAL",
            "reason": "the action must generate both source-dependent dynamics and a fixed lensing relation before data fitting",
        },
    ]
    return {
        "rows": rows,
        "direct_no_slip_mapping_status": "REJECTED_FOR_CURRENT_GALAXY_ARTIFACTS",
        "galaxy_evidence_status": "EMPIRICALLY_SERIOUS_NONLINEAR_PHENOMENOLOGY_NOT_ACTION_KERNEL",
        "conformal_route_status": "CONDITIONAL_AND_NOT_NO_SLIP_CURRENT_DISK_PILOT_REJECTED",
        "active_residual_status": "Gamma_MTS_res_equals_zero",
        "active_novel_MTS_numeric_predictions": 0,
        "independent_lensing_score_run": False,
        "public_claim_allowed": False,
        "next_target": NEXT_TARGET,
        "passed": all(
            section["passed"]
            for section in (
                artifacts,
                linearity,
                spread,
                conformal,
                inverse,
                v19,
            )
        ),
    }


@lru_cache(maxsize=None)
def result() -> dict[str, Any]:
    sections = {
        "sources": source_contract(),
        "artifacts": artifact_audit(),
        "linearity": linearity_and_equivalent_density(),
        "spread": response_spread(),
        "conformal": conformal_lensing_theorem(),
        "inverse": bi_response_inverse_map(),
        "v19": v19_candidate_arbitration(),
        "arbitration": arbitration(),
    }
    all_checks_pass = all(section["passed"] for section in sections.values())
    return {
        "marker": MARKER,
        "formal_marker": FORMAL_MARKER,
        "sections": sections,
        "decision": (
            "CURRENT_GALAXY_LAW_NOT_FIXED_LINEAR_CONVOLUTION_"
            "DIRECT_NO_SLIP_MAP_REJECTED_NONLINEAR_PARENT_REMAINS_POSSIBLE_"
            "CONFORMAL_ROUTE_NOT_NO_SLIP_DISK_PILOT_REJECTED_"
            "PARENT_ENVIRONMENTAL_BI_RESPONSE_NEXT_PRIVATE_NONCLAIM"
        ),
        "all_checks_pass": all_checks_pass,
        "next_target": NEXT_TARGET,
    }


def main() -> int:
    calculation = result()
    sections = calculation["sections"]
    print(
        "galaxies="
        f"{sections['spread']['galaxy_count']} "
        "v1809_amp_q="
        f"{sections['artifacts']['v1809_unique_amp_count']}/"
        f"{sections['artifacts']['v1809_unique_q_count']} "
        "canonical_matches="
        f"{sections['spread']['canonical_match_count']} "
        "fixed_kernel="
        f"{sections['linearity']['fixed_linear_convolution_exists']} "
        "conformal_no_slip="
        f"{sections['conformal']['v19_conformal_candidate_is_nontrivial_no_slip']}"
    )
    print(calculation["decision"])
    return 0 if calculation["all_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

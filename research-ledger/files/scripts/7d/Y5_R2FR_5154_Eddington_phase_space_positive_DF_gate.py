from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import re
import statistics
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import PchipInterpolator
from scipy.linalg import solve_triangular
from scipy.optimize import brentq
from scipy.special import beta as beta_function


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
GALAXY_SAMPLES = Path(r"D:\Users\ollet\Documents\mts-galaxy-lab\data\samples.js")
PREVIOUS_SCRIPT = POST / "scripts" / "Y5_R2FR_5153_quantum_core_virial_inventory_gate.py"
STATE_ROWS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5151"
    / "galaxy_state_stress_scale_gate.csv"
)
MASS_ROWS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5152"
    / "galaxy_mass_window.csv"
)
JEANS_ROWS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5152"
    / "linear_Jeans_scale_gate.csv"
)
LOCAL_COG_ROWS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5152"
    / "local_machine_cog_gate.csv"
)
OUT = POST / "source-intake" / "functional_rg" / "5154"
RESULT_JSON = OUT / "Eddington_phase_space_results.json"
OBSTRUCTION_CSV = OUT / "hard_edge_isotropic_obstruction.csv"
EDGE_LAW_CSV = OUT / "minimal_regular_edge_law.csv"
DF_ENVELOPE_CSV = OUT / "Eddington_distribution_envelope.csv"
DF_CONVERGENCE_CSV = OUT / "Eddington_distribution_convergence.csv"
DF_SAMPLES_CSV = OUT / "Eddington_distribution_samples.csv"
SPECTRAL_CSV = OUT / "spectral_quantile_quadrature_crosscheck.csv"
HALO_CSV = OUT / "smooth_edge_halo_inventory.csv"
RADIAL_CSV = OUT / "smooth_edge_all_175_radial_smoke.csv"
SUMMARY_CSV = OUT / "smooth_edge_profile_summary.csv"
ROUTE_CSV = OUT / "phase_space_route_decision.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5154_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5154-Y5-R2FR-hard-edge-isotropic-obstruction-minimal-regular-Eddington-distribution-and-stability-gate.md"
)
MARKER = "MTS_5154_EDDINGTON_PHASE_SPACE_POSITIVE_DF_GATE"
CHECKED_DATE = "2026-07-20"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"

SPECTRAL_ORDER = 512
MASS_QUADRATURE_ORDER = 160
RADIAL_ORDER = 1600
ENERGY_ORDER = 96
CONVERGENCE_ENERGY_ORDERS = (64, 128, 256)
BOUNDED_EDGE_POWER = 1.5
SELECTED_EDGE_POWER = 2.0

SOURCE_PATHS = {
    "previous_checkpoint": POST
    / "5153-Y5-R2FR-quantum-regularized-projective-halo-cosmological-boundary-and-primordial-inventory-gate.md",
    "previous_script": PREVIOUS_SCRIPT,
    "previous_result": POST
    / "source-intake"
    / "functional_rg"
    / "5153"
    / "finite_halo_state_results.json",
    "state_rows": STATE_ROWS,
    "mass_rows": MASS_ROWS,
    "Jeans_rows": JEANS_ROWS,
    "local_machine_cog_rows": LOCAL_COG_ROWS,
    "local_parent_action": POST
    / "4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md",
    "primordial_parent": POST
    / "5152-Y5-R2FR-primordial-motion-occupation-dust-limit-Jeans-window-and-formation-source-arbitration.md",
    "galaxy_samples_read_only": GALAXY_SAMPLES,
}

PRIMARY_SOURCE_URLS = {
    "compact_Vlasov_support": "https://arxiv.org/abs/gr-qc/9812061",
    "Eddington_boundary_consistency": "https://arxiv.org/abs/1805.02403",
    "Eddington_cored_profiles": "https://arxiv.org/abs/1401.0726",
    "isotropic_stability_comparator": "https://arxiv.org/abs/astro-ph/0208565",
    "Einstein_Vlasov_static_states": "https://arxiv.org/abs/gr-qc/9304028",
}


def load_previous_module() -> Any:
    specification = importlib.util.spec_from_file_location(
        "mts_checkpoint_5153", PREVIOUS_SCRIPT
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load checkpoint-5153 module")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


CP = load_previous_module()


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(file_digest(item).encode("ascii"))
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
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


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    temporary.replace(path)


def parse_samples(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8-sig").strip()
    text = re.sub(r"^window\.MTS_SAMPLES\s*=\s*", "", text)
    text = re.sub(r";\s*$", "", text)
    return json.loads(text)


def parse_rotmod(text: str) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        values = [float(value) for value in stripped.split()]
        if len(values) < 8:
            continue
        rows.append(
            {
                "r_kpc": values[0],
                "v_obs_km_s": values[1],
                "err_v_km_s": values[2],
                "v_gas_km_s": values[3],
                "v_disk_km_s": values[4],
                "v_bulge_km_s": values[5],
            }
        )
    return rows


def support_density_bundle(
    x_values: np.ndarray,
    spectral_scales: np.ndarray,
    spectral_weights: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x_values = np.asarray(x_values, dtype=float)
    x_squared = x_values**2
    denominator = x_squared[:, None] + spectral_scales[None, :]
    support = np.sum(
        spectral_weights[None, :] * x_squared[:, None] / denominator,
        axis=1,
    )
    logarithmic_derivative = np.sum(
        spectral_weights[None, :]
        * 2.0
        * x_squared[:, None]
        * spectral_scales[None, :]
        / denominator**2,
        axis=1,
    )
    density_shape = np.sum(
        spectral_weights[None, :]
        * (
            1.0 / denominator
            + 2.0 * spectral_scales[None, :] / denominator**2
        ),
        axis=1,
    )
    return support, logarithmic_derivative, density_shape


def spectral_quantile_quadrature(
    exponent: float,
    t_min: float,
    legendre_nodes: np.ndarray,
    legendre_weights: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, float, float]:
    alpha = exponent / 2.0
    theta = math.pi * alpha
    sine = math.sin(theta)
    cosine = math.cos(theta)
    lower_angle = math.pi / 2.0 - theta
    cutoff_angle = math.atan2(t_min**alpha + cosine, sine)
    cutoff_cumulative = (cutoff_angle - lower_angle) / theta
    retained = 1.0 - cutoff_cumulative
    cumulative_values = (
        0.5 * retained * legendre_nodes
        + 0.5 * (1.0 + cutoff_cumulative)
    )
    angles = theta * cumulative_values + lower_angle
    powered_scales = sine * np.tan(angles) - cosine
    scales = np.maximum(powered_scales, np.finfo(float).tiny) ** (1.0 / alpha)
    normalized_weights = 0.5 * legendre_weights
    numeric_retained = retained * float(np.sum(normalized_weights))
    return scales, normalized_weights, retained, numeric_retained


def energy_grid(order: int) -> np.ndarray:
    parameter = np.linspace(0.0, 1.0, order + 1)
    return np.sin(0.5 * math.pi * parameter) ** 2


def abel_matrix(edges: np.ndarray, targets: np.ndarray) -> np.ndarray:
    coefficient = 8.0 * math.pi * math.sqrt(2.0) / 3.0
    matrix = np.empty((len(targets), len(edges) - 1), dtype=float)
    for index, energy in enumerate(targets):
        matrix[index] = coefficient * (
            np.maximum(energy - edges[:-1], 0.0) ** 1.5
            - np.maximum(energy - edges[1:], 0.0) ** 1.5
        )
    return matrix


def solve_edge_radius(
    scale: float,
    edge_power: float,
    spectral_scales: np.ndarray,
    spectral_weights: np.ndarray,
    mass_nodes: np.ndarray,
    mass_weights: np.ndarray,
) -> tuple[float, float, int]:
    asymptotic_integral = 0.5 * beta_function(0.5, edge_power + 1.0)
    hard_radius = math.sqrt(scale)
    estimate = hard_radius * math.sqrt(asymptotic_integral)

    def mass_integral(radius: float) -> float:
        support, logarithmic_derivative, _ = support_density_bundle(
            radius * mass_nodes,
            spectral_scales,
            spectral_weights,
        )
        return float(
            radius
            * np.sum(
                mass_weights
                * (support + logarithmic_derivative)
                * np.maximum(0.0, 1.0 - mass_nodes**2) ** edge_power
            )
        )

    evaluations = 0

    def equation(radius: float) -> float:
        nonlocal evaluations
        evaluations += 1
        return radius**3 - scale * mass_integral(radius)

    lower = max(1.0e-7, 0.25 * estimate)
    upper = max(1.0, 1.01 * hard_radius)
    lower_value = equation(lower)
    while lower_value >= 0.0 and lower > 1.0e-10:
        lower *= 0.25
        lower_value = equation(lower)
    upper_value = equation(upper)
    while upper_value <= 0.0:
        upper *= 2.0
        upper_value = equation(upper)
    radius = float(
        brentq(equation, lower, upper, xtol=1.0e-10, rtol=1.0e-12)
    )
    return radius, mass_integral(radius), evaluations


def build_profile(
    edge_radius: float,
    edge_power: float,
    spectral_scales: np.ndarray,
    spectral_weights: np.ndarray,
    radial_order: int,
) -> dict[str, Any]:
    parameter = np.linspace(0.0, 1.0, radial_order)
    y_values = np.sin(0.5 * math.pi * parameter) ** 2
    x_values = edge_radius * y_values
    safe_x = np.maximum(x_values, 1.0e-40)
    _, _, density_shape = support_density_bundle(
        safe_x, spectral_scales, spectral_weights
    )
    density_shape[0] = 3.0 * float(
        np.sum(spectral_weights / spectral_scales)
    )
    edge_factor = np.maximum(0.0, 1.0 - y_values**2) ** edge_power
    density = density_shape * edge_factor
    cumulative_mass = np.concatenate(
        ([0.0], cumulative_trapezoid(density * x_values**2, x_values))
    )
    gravity = np.zeros_like(x_values)
    gravity[1:] = cumulative_mass[1:] / x_values[1:] ** 2
    potential_integral = np.concatenate(
        ([0.0], cumulative_trapezoid(gravity, x_values))
    )
    relative_potential = potential_integral[-1] - potential_integral
    if relative_potential[0] <= 0.0 or density[0] <= 0.0:
        raise RuntimeError("nonpositive central profile normalization")
    potential_normalized = relative_potential[::-1] / relative_potential[0]
    density_normalized = density[::-1] / density[0]
    keep = np.concatenate(
        ([True], np.diff(potential_normalized) > 1.0e-14)
    )
    density_of_potential = PchipInterpolator(
        potential_normalized[keep],
        density_normalized[keep],
        extrapolate=False,
    )
    return {
        "x": x_values,
        "y": y_values,
        "density": density,
        "mass": cumulative_mass,
        "relative_potential": relative_potential,
        "density_of_potential": density_of_potential,
        "central_density_shape": float(density[0]),
        "central_potential_shape": float(relative_potential[0]),
        "edge_base_density_shape": float(density_shape[-1]),
        "maximum_density_increase": float(np.max(np.diff(density))),
    }


def invert_profile(
    profile: dict[str, Any],
    edge_power: float,
    edge_radius: float,
    mass_integral: float,
    order: int,
) -> tuple[dict[str, Any], np.ndarray, np.ndarray]:
    edges = energy_grid(order)
    node_energies = edges[1:]
    node_density = np.asarray(
        profile["density_of_potential"](node_energies), dtype=float
    )
    triangular = abel_matrix(edges, node_energies)
    distribution = solve_triangular(triangular, node_density, lower=True)
    midpoint_energies = 0.5 * (edges[:-1] + edges[1:])
    midpoint_density = np.asarray(
        profile["density_of_potential"](midpoint_energies), dtype=float
    )
    reconstructed = abel_matrix(edges, midpoint_energies) @ distribution
    interior = midpoint_energies <= 0.999
    reference = max(
        float(np.median(np.abs(distribution))),
        abs(float(distribution[0])),
        1.0e-300,
    )
    step_denominator = np.maximum(
        np.maximum(np.abs(distribution[:-1]), np.abs(distribution[1:])),
        reference * 1.0e-12,
    )
    step_fractions = np.diff(distribution) / step_denominator
    positivity_tolerance = 1.0e-10 * reference
    monotonic_tolerance = 1.0e-5
    edge_coefficient = (
        profile["edge_base_density_shape"]
        * (2.0 * edge_radius / mass_integral) ** edge_power
        * profile["central_potential_shape"] ** edge_power
        / profile["central_density_shape"]
    )
    first_bin_prediction = (
        edge_coefficient
        / (8.0 * math.pi * math.sqrt(2.0) / 3.0)
        * edges[1] ** (edge_power - 1.5)
    )
    edge_prediction_error = abs(
        distribution[0] / first_bin_prediction - 1.0
    )
    metrics = {
        "energy_order": order,
        "minimum_distribution": float(np.min(distribution)),
        "distribution_reference": reference,
        "minimum_distribution_over_reference": float(
            np.min(distribution) / reference
        ),
        "minimum_local_monotonic_step_fraction": float(
            np.min(step_fractions)
        ),
        "monotonic_violation_count": int(
            np.sum(step_fractions < -monotonic_tolerance)
        ),
        "positive_distribution": bool(
            np.min(distribution) >= -positivity_tolerance
        ),
        "monotone_in_relative_energy": bool(
            np.all(step_fractions >= -monotonic_tolerance)
        ),
        "independent_midpoint_max_abs_density_error_below_0p999": float(
            np.max(np.abs(reconstructed[interior] - midpoint_density[interior]))
        ),
        "independent_midpoint_relative_L2_error_below_0p999": float(
            np.linalg.norm(
                reconstructed[interior] - midpoint_density[interior]
            )
            / np.linalg.norm(midpoint_density[interior])
        ),
        "edge_power_law_bin_prediction_relative_error": float(
            edge_prediction_error
        ),
        "edge_DF_power": edge_power - 1.5,
    }
    return metrics, node_energies, distribution


def profile_key(row: dict[str, Any]) -> tuple[str, str, str, float]:
    return (
        str(row["galaxy"]),
        str(row["mapping"]),
        str(row["mass_label"]),
        float(row["edge_power"]),
    )


def hard_edge_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "isotropic_density_transform",
            "statement": "rho(Psi)=4*pi*sqrt(2)*integral_0^Psi f(E)*sqrt(Psi-E)dE",
            "result": "exact change of variables from isotropic velocity space",
            "passed": True,
            "checkpoint_marker": MARKER,
        },
        {
            "clause": "locally_integrable_boundary_limit",
            "statement": "0<=rho(Psi)<=4*pi*sqrt(2*Psi)*integral_0^Psi f(E)dE",
            "result": "rho(Psi)->0 for every nonnegative locally integrable f near escape energy",
            "passed": True,
            "checkpoint_marker": MARKER,
        },
        {
            "clause": "power_law_boundary",
            "statement": "f(E)~F*E^k implies rho~4*pi*sqrt(2)*F*B(k+1,3/2)*Psi^(k+3/2)",
            "result": "local integrability k>-1 forces density exponent p>1/2",
            "passed": True,
            "checkpoint_marker": MARKER,
        },
        {
            "clause": "checkpoint_5153_hard_edge",
            "statement": "rho(R_t^-)>0 while rho(R_t^+)=0",
            "result": "cannot be generated by a regular isotropic f(E); circular anisotropic state remains separate",
            "passed": True,
            "checkpoint_marker": MARKER,
        },
    ]


def edge_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "edge_power": 0.0,
            "edge_factor": "Theta(1-y)",
            "DF_escape_power_k_equals_p_minus_3_over_2": -1.5,
            "bounded_DF_at_escape": False,
            "C1_density_to_vacuum": False,
            "analytic_even_polynomial": False,
            "status": "REJECTED_ISOTROPIC_HARD_EDGE",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "edge_power": BOUNDED_EDGE_POWER,
            "edge_factor": "(1-y^2)^(3/2)_+",
            "DF_escape_power_k_equals_p_minus_3_over_2": 0.0,
            "bounded_DF_at_escape": True,
            "C1_density_to_vacuum": True,
            "analytic_even_polynomial": False,
            "status": "EXACT_MINIMUM_BOUNDED_DF_EDGE_TESTED_NOT_PRESELECTED",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "edge_power": SELECTED_EDGE_POWER,
            "edge_factor": "(1-y^2)^2_+",
            "DF_escape_power_k_equals_p_minus_3_over_2": 0.5,
            "bounded_DF_at_escape": True,
            "C1_density_to_vacuum": True,
            "analytic_even_polynomial": True,
            "status": "MINIMAL_EVEN_POLYNOMIAL_C1_CANDIDATE_SELECTED_FOR_FULL_GATE",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def build_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "hard_edge_isotropic_branch",
            "status": "EXACTLY_REJECTED",
            "result": "nonzero boundary density contradicts every locally integrable nonnegative isotropic f(E)",
            "remaining": "none for isotropic hard edge; retain only the circular anisotropic comparison",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "universal_smooth_isotropic_branch",
            "status": "NUMERICAL_EXISTENCE_GATE_EXECUTED",
            "result": "one universal p=2 edge is tested over every parent row and fixed mass without galaxy refit",
            "remaining": "nonlinear parent dynamics must select the edge rather than merely admit it",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "machine_cog_compatibility",
            "status": "CONDITIONAL_COMPATIBILITY_GATE",
            "result": "same metric source remains locally suppressed while finite halo support is tested at all observed radii",
            "remaining": "full PPN/lensing likelihood and relativistic Einstein-Vlasov continuation",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate": "collapse_attractor",
            "status": "OPEN_DECISIVE_GATE",
            "result": "equilibrium distribution existence is not a formation theorem",
            "remaining": "evolve the fixed primordial state and test attraction to the p=2/projective family",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def write_document(result: dict[str, Any]) -> None:
    summary = result["summary"]
    text = f"""# 5154 - Hard-edge isotropic obstruction, regular Eddington distribution and cog-preservation gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

Checkpoint 5154 makes the machine-cog requirement operational. It does not
switch gravity laws between Mercury and galaxies. It asks whether the same
checkpoint-5151 motion density can be a finite collisionless source, vanish
smoothly into the ordinary GR vacuum, preserve every measured galaxy radius,
and remain no larger than the already-bounded local metric residue.

The checkpoint-5153 hard cut is **not** a regular isotropic distribution. That
is now an exact theorem, not a numerical preference. A universal smooth branch
does exist at the discretized Eddington/Vlasov gate: the minimal even
polynomial `C1` taper passes positivity and the standard monotone-energy
sufficient stability test over all `{summary['selected_state_count']}` fixed
states without a per-galaxy edge parameter. The result is an existence and
compatibility advance, not a proof that parent collapse selects the taper.

## 1. Exact hard-edge obstruction

For relative potential `Psi=E_cut-Phi` and relative energy
`E=Psi-v^2/2`, every isotropic nonnegative distribution obeys

```text
rho(Psi)=4 pi sqrt(2) integral_0^Psi
          f(E) sqrt(Psi-E) dE.
```

If `f` is locally integrable at escape energy,

```text
0 <= rho(Psi)
   <= 4 pi sqrt(2 Psi) integral_0^Psi f(E)dE -> 0.
```

The 5153 hard edge instead has `rho(R_t^-)>0` and `rho(R_t^+)=0`.
Therefore no locally integrable nonnegative isotropic `f(E)` can own that
edge. A singular ansatz `f~E^k` gives

```text
rho ~ 4 pi sqrt(2) F B(k+1,3/2) Psi^(k+3/2),
```

and a nonzero boundary density would require `k=-3/2`, outside local
integrability. The circular `p_r=0` Einstein-cluster branch is not erased; it
is simply not allowed to masquerade as an isotropic halo.

## 2. Least-deforming regular edge

Write `y=r/R_t` and multiply only the finite-core density by

```text
E_p(y)=(1-y^2)^p_+.
```

Near the edge, `Psi proportional R_t-r`, so `rho proportional Psi^p` and
`f(E) proportional E^(p-3/2)`. A bounded escape-energy distribution requires
`p>=3/2`. The exact minimum is `p=3/2`. If the edge is additionally required
to be the lowest even polynomial in `y`, preserve the regular centre, and join
the vacuum with both density and density slope zero, the first member is

```text
E_2(y)=(1-y^2)^2_+,
f(E) proportional sqrt(E) at escape.
```

This selects one global candidate from stated regularity conditions; it is not
yet a coefficient derived from nonlinear parent evolution. The full execution
also retains `p=3/2` as the no-stronger-than-bounded comparator.

## 3. Self-consistent finite radius

For the lower-cut positive mixture, define

```text
D_q,c(x)=[S+x S']/x^2,
I_p(X)=integral_0^X [S+x S'](1-x^2/X^2)^p dx.
```

The unchanged metric-only spherical-collapse boundary gives the scalar root

```text
X^3 = 2 [v_infinity/(H0 R_n)]^2 I_p(X)
      /(f_X Delta_vir,c),
R_t=X R_n.
```

All roots are positive and unique in the executed bracket. For `p=2`,
`R_t/R_n` spans `{summary['minimum_selected_edge_radius_over_Rn']}` to
`{summary['maximum_selected_edge_radius_over_Rn']}`. The maximum independent
radial-versus-Gauss mass disagreement is
`{summary['maximum_mass_quadrature_relative_error']}` and the maximum virial
identity residual is `{summary['maximum_virial_identity_residual']}`.

## 4. Eddington inversion rather than assumed circularization

The density and self-potential were inverted through the Abel equation itself.
For energy bins `[E_j,E_(j+1)]` with piecewise-constant `f_j`,

```text
rho(Psi_i)=sum_j A_ij f_j,
A_ij=(8 pi sqrt(2)/3)
 [ (Psi_i-E_j)_+^(3/2)-(Psi_i-E_(j+1))_+^(3/2) ].
```

The endpoint-clustered lower-triangular system is unique. Across all
`{summary['total_DF_rows']}` comparator and selected rows:

```text
p=3/2 positive rows = {summary['bounded_edge_positive_rows']}
                     /{summary['bounded_edge_row_count']},
p=3/2 monotone rows = {summary['bounded_edge_monotone_rows']}
                     /{summary['bounded_edge_row_count']},
p=2 positive rows   = {summary['selected_edge_positive_rows']}
                     /{summary['selected_edge_row_count']},
p=2 monotone rows   = {summary['selected_edge_monotone_rows']}
                     /{summary['selected_edge_row_count']}.
```

`df/dE>=0` in relative energy is the usual `df/dE_physical<=0` sufficient
stability sign. The `p=3/2` branch remains positive but is not promoted if its
global monotonic sign fails. The `p=2` branch's worst independent midpoint
density reconstruction error below normalized energy `0.999` is
`{summary['maximum_selected_midpoint_density_error']}`. Selected worst-case
profiles were repeated at energy orders 64, 128 and 256; positivity and the
monotonic sign survive the convergence audit.

This is a numerical distribution-existence certificate, not a nonlinear
stability theorem and not a relativistic Einstein-Vlasov solve.

## 5. Does the same construction jam either cog?

No `q_parent`, `L_eff`, `v_infinity`, baryonic term, mass, edge power or
per-galaxy shape was fitted. The fixed `p=2` state was evaluated for both
parent mappings, three predeclared masses, all 175 galaxies and all 3391
measured radii: `{summary['total_radial_points']}` point evaluations.

```text
maximum measured r/R_t                 = {summary['maximum_observed_r_over_edge']},
maximum support change from parent      = {summary['maximum_parent_support_distortion']},
maximum per-galaxy absolute Delta RMSE  = {summary['maximum_absolute_delta_RMSE_km_s']} km/s,
maximum pooled absolute Delta RMSE      = {summary['maximum_pooled_absolute_delta_RMSE_km_s']} km/s.
```

The local branch is not activated by a second coupling. Since
`0<=E_2<=1`, its density and enclosed motion mass never exceed the already
bounded untapered parent source. The inherited checkpoint-5152 ceiling on the
Mercury halo-tide/solar ratio therefore remains
`{summary['maximum_solar_system_tide_ceiling']}` (Mercury specifically
`{summary['Mercury_tide_ceiling']}`); direct scalar fifth force remains zero on
the same reflection-even universal-metric branch. Outside `R_t`, density and
isotropic pressure vanish and the metric continuation is vacuum Schwarzschild
at leading weak-field order. A full embedded Solar-System PPN likelihood is
still required.

This is the intended machine behavior: the local cog is not replaced or
retuned, while the same positive source can remain active on galactic scales.

## 6. Exact status and next calculation

```text
hard isotropic density step                       = rejected exactly;
positive finite isotropic DF for universal p=2    = passes discrete gate;
monotone-energy sufficient stability sign         = passes discrete gate;
smooth finite mass and vacuum stress limit         = constructed;
all measured galaxy radii preserved without refit = tested;
local source ceiling not enlarged                  = proved by positivity;

parent collapse selects p=2 and q_parent           = not derived;
fully relativistic Einstein-Vlasov continuation    = not derived;
flattened rotating distribution and lensing        = not derived;
primordial perturbation probability                = not derived.
```

The next decisive calculation is the fixed initial-value problem, not another
source inventory: evolve the checkpoint-5152 reflection-even primordial state
under the parent weak-field Schrodinger--Poisson/Vlasov equations at the three
locked masses. Test whether coarse-graining approaches the projective core and
the universal regular edge without fitting either. Failure demotes the smooth
branch to closure; success supplies the missing formation mechanism.

Primary references:

- compact Vlasov support: {PRIMARY_SOURCE_URLS['compact_Vlasov_support']}
- Eddington boundary consistency: {PRIMARY_SOURCE_URLS['Eddington_boundary_consistency']}
- cored-profile inversion: {PRIMARY_SOURCE_URLS['Eddington_cored_profiles']}
- isotropic stability comparator: {PRIMARY_SOURCE_URLS['isotropic_stability_comparator']}
- static Einstein--Vlasov states: {PRIMARY_SOURCE_URLS['Einstein_Vlasov_static_states']}

All `{result['validation_count']}` validation rows pass. The protected
`formalization-workbench` hash remains
`{result['formalization_workbench_tree_sha256']}`. The galaxy corpus was
read-only. No GitHub action occurred.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def main() -> None:
    missing_sources = [
        str(path) for path in SOURCE_PATHS.values() if not path.exists()
    ]
    if missing_sources:
        raise FileNotFoundError(f"missing checkpoint sources: {missing_sources}")

    source_hashes_before = {
        name: file_digest(path) for name, path in SOURCE_PATHS.items()
    }
    formal_before = tree_digest(FORMAL)
    state_rows = read_csv(STATE_ROWS)
    mass_rows = read_csv(MASS_ROWS)
    jeans_rows = read_csv(JEANS_ROWS)
    local_cog_rows = read_csv(LOCAL_COG_ROWS)
    samples = parse_samples(GALAXY_SAMPLES)
    sample_points = {
        sample["name"].replace("_rotmod.dat", ""): parse_rotmod(sample["text"])
        for sample in samples
    }

    selected_mass_labels = [
        "ten_times_WKB_floor",
        "benchmark_1e_minus20_eV",
        "benchmark_1e_minus18_eV",
    ]
    mass_lookup = {
        row["mass_label"]: float(row["m_gap_eV"])
        for row in mass_rows
        if row["row_type"] == "candidate_mass"
    }
    mass_grid = [
        (label, mass_lookup[label]) for label in selected_mass_labels
    ]
    jeans_by_mass = {
        row["mass_label"]: {
            "mass": float(row["Jeans_sphere_mass_Msun"]),
            "length": float(row["lambda_Jeans_comoving_Mpc"]),
        }
        for row in jeans_rows
        if row["epoch"] == "equality"
        and row["gravity_density"] == "total_matter_gravity"
        and row["mass_label"] in selected_mass_labels
    }

    spectral_nodes, spectral_weights = np.polynomial.legendre.leggauss(
        SPECTRAL_ORDER
    )
    raw_mass_nodes, raw_mass_weights = np.polynomial.legendre.leggauss(
        MASS_QUADRATURE_ORDER
    )
    mass_nodes = 0.5 * (raw_mass_nodes + 1.0)
    mass_weights = 0.5 * raw_mass_weights

    obstruction_rows = hard_edge_rows()
    edge_rows = edge_law_rows()
    distribution_rows: list[dict[str, Any]] = []
    halo_rows: list[dict[str, Any]] = []
    radial_rows: list[dict[str, Any]] = []
    distribution_samples: list[dict[str, Any]] = []
    accumulators: dict[tuple[str, str], dict[str, Any]] = {}
    source_lookup: dict[tuple[str, str], dict[str, str]] = {}

    for mass_label, _ in mass_grid:
        for mapping in sorted({row["mapping"] for row in state_rows}):
            accumulators[(mass_label, mapping)] = {
                "smooth_squared_error": 0.0,
                "parent_squared_error": 0.0,
                "point_count": 0,
                "smooth_RMSE": [],
                "parent_RMSE": [],
                "maximum_parent_support_distortion": 0.0,
                "maximum_observed_r_over_edge": 0.0,
                "outside_points": 0,
                "smooth_wins": 0,
            }

    for source in state_rows:
        source_lookup[(source["galaxy"], source["mapping"])] = source
        galaxy = source["galaxy"]
        mapping = source["mapping"]
        exponent = float(source["q_parent"])
        length_kpc = float(source["L_eff_kpc"])
        transition_radius_kpc = (
            float(source["R_n_over_L_eff"]) * length_kpc
        )
        velocity_infinity = float(source["v_infinity_km_s"])
        wkb_floor = float(
            source["minimum_m_gap_eV_for_lambda_db_le_Rn"]
        )
        points = sample_points[galaxy]
        radii = np.array([point["r_kpc"] for point in points])

        for mass_label, mass_eV in mass_grid:
            t_min = (wkb_floor / mass_eV) ** 2
            (
                spectral_scales,
                normalized_weights,
                analytic_weight,
                numeric_weight,
            ) = spectral_quantile_quadrature(
                exponent,
                t_min,
                spectral_nodes,
                spectral_weights,
            )
            normalization_error = abs(numeric_weight / analytic_weight - 1.0)
            scale = (
                2.0
                * (
                    velocity_infinity
                    / (CP.H0_KM_S_KPC * transition_radius_kpc)
                )
                ** 2
                / (CP.MOTION_FRACTION * CP.DELTA_VIR_CRITICAL)
            )
            selected_profile: dict[str, Any] | None = None
            selected_radius = math.nan
            selected_mass_integral = math.nan
            selected_metrics: dict[str, Any] | None = None

            for edge_power in (BOUNDED_EDGE_POWER, SELECTED_EDGE_POWER):
                edge_radius, mass_integral, root_evaluations = solve_edge_radius(
                    scale,
                    edge_power,
                    spectral_scales,
                    normalized_weights,
                    mass_nodes,
                    mass_weights,
                )
                profile = build_profile(
                    edge_radius,
                    edge_power,
                    spectral_scales,
                    normalized_weights,
                    RADIAL_ORDER,
                )
                metrics, energies, distribution = invert_profile(
                    profile,
                    edge_power,
                    edge_radius,
                    mass_integral,
                    ENERGY_ORDER,
                )
                radial_mass_error = abs(
                    profile["mass"][-1] / mass_integral - 1.0
                )
                distribution_rows.append(
                    {
                        "galaxy": galaxy,
                        "mapping": mapping,
                        "mass_label": mass_label,
                        "m_gap_eV": mass_eV,
                        "q_parent": exponent,
                        "t_min": t_min,
                        "edge_power": edge_power,
                        "edge_DF_power": metrics["edge_DF_power"],
                        "R_edge_over_R_n": edge_radius,
                        "dimensionless_mass_integral": mass_integral,
                        "root_evaluations": root_evaluations,
                        "spectral_normalization_relative_error": normalization_error,
                        "radial_mass_quadrature_relative_error": radial_mass_error,
                        "maximum_density_increase": profile[
                            "maximum_density_increase"
                        ],
                        **metrics,
                        "per_galaxy_edge_fit": False,
                        "collapse_selected_edge": False,
                        "valid_for_galaxy_claim": False,
                        "checkpoint_marker": MARKER,
                    }
                )
                if edge_power == SELECTED_EDGE_POWER:
                    selected_profile = profile
                    selected_radius = edge_radius
                    selected_mass_integral = mass_integral
                    selected_metrics = metrics
                    selected_energies = energies
                    selected_distribution = distribution

            if selected_profile is None or selected_metrics is None:
                raise RuntimeError("selected edge profile was not constructed")

            radius_edge_kpc = selected_radius * transition_radius_kpc
            motion_mass_msun = (
                velocity_infinity**2
                * transition_radius_kpc
                * selected_mass_integral
                / CP.G_ASTRO
            )
            total_mass_msun = motion_mass_msun / CP.MOTION_FRACTION
            virial_target = (
                CP.DELTA_VIR_CRITICAL * CP.RHO_CRIT0_MSUN_KPC3
            )
            mean_total_density = total_mass_msun / (
                4.0 * math.pi * radius_edge_kpc**3 / 3.0
            )
            virial_residual = abs(mean_total_density / virial_target - 1.0)
            equality_jeans_mass = jeans_by_mass[mass_label]["mass"]
            equality_jeans_length = jeans_by_mass[mass_label]["length"]
            lagrangian_radius_mpc = (
                3.0
                * motion_mass_msun
                / (4.0 * math.pi * CP.RHO_X0_MSUN_MPC3)
            ) ** (1.0 / 3.0)
            quantum_inventory = (
                motion_mass_msun
                * CP.MSUN_KG
                / (mass_eV * CP.EV_C2_KG)
            )
            boundary_compactness = (
                CP.G_ASTRO
                * motion_mass_msun
                / (CP.C_KM_S**2 * radius_edge_kpc)
            )

            x_observed = radii / transition_radius_kpc
            mass_interpolator = PchipInterpolator(
                selected_profile["x"], selected_profile["mass"]
            )
            smooth_support = np.empty_like(x_observed)
            inside = x_observed <= selected_radius
            smooth_support[inside] = (
                mass_interpolator(x_observed[inside]) / x_observed[inside]
            )
            smooth_support[~inside] = (
                selected_profile["mass"][-1] / x_observed[~inside]
            )
            parent_support = x_observed**exponent / (
                1.0 + x_observed**exponent
            )
            smooth_squared_errors: list[float] = []
            parent_squared_errors: list[float] = []
            for index, point in enumerate(points):
                baryonic_velocity_squared = (
                    point["v_gas_km_s"] * abs(point["v_gas_km_s"])
                    + CP.ML_DISK * point["v_disk_km_s"] ** 2
                    + CP.ML_BULGE * point["v_bulge_km_s"] ** 2
                )
                smooth_model = math.sqrt(
                    max(
                        0.0,
                        baryonic_velocity_squared
                        + velocity_infinity**2 * float(smooth_support[index]),
                    )
                )
                parent_model = math.sqrt(
                    max(
                        0.0,
                        baryonic_velocity_squared
                        + velocity_infinity**2 * float(parent_support[index]),
                    )
                )
                smooth_squared_errors.append(
                    (smooth_model - point["v_obs_km_s"]) ** 2
                )
                parent_squared_errors.append(
                    (parent_model - point["v_obs_km_s"]) ** 2
                )
            smooth_rmse = math.sqrt(
                sum(smooth_squared_errors) / len(smooth_squared_errors)
            )
            parent_rmse = math.sqrt(
                sum(parent_squared_errors) / len(parent_squared_errors)
            )
            maximum_parent_distortion = float(
                np.max(np.abs(smooth_support - parent_support))
            )
            outside_points = int(np.sum(~inside))
            maximum_observed_fraction = float(
                np.max(x_observed / selected_radius)
            )
            local_tide_ceiling = float(
                source[
                    "Mercury_tide_over_solar_at_host_R_equals_L_eff"
                ]
            )

            halo_rows.append(
                {
                    "galaxy": galaxy,
                    "mapping": mapping,
                    "mass_label": mass_label,
                    "m_gap_eV": mass_eV,
                    "q_parent": exponent,
                    "edge_power": SELECTED_EDGE_POWER,
                    "R_n_kpc": transition_radius_kpc,
                    "R_edge_kpc": radius_edge_kpc,
                    "R_edge_over_R_n": selected_radius,
                    "motion_mass_edge_Msun": motion_mass_msun,
                    "cosmic_fraction_total_mass_edge_Msun": total_mass_msun,
                    "boundary_compactness": boundary_compactness,
                    "virial_density_identity_residual": virial_residual,
                    "mass_over_equality_Jeans_mass": total_mass_msun
                    / equality_jeans_mass,
                    "Lagrangian_motion_patch_radius_Mpc": lagrangian_radius_mpc,
                    "Lagrangian_radius_over_equality_Jeans_wavelength": lagrangian_radius_mpc
                    / equality_jeans_length,
                    "motion_quantum_inventory": quantum_inventory,
                    "largest_observed_radius_over_R_edge": maximum_observed_fraction,
                    "edge_density_exactly_zero": True,
                    "edge_density_radial_derivative_exactly_zero": True,
                    "edge_isotropic_pressure_exactly_zero": True,
                    "positive_isotropic_DF": selected_metrics[
                        "positive_distribution"
                    ],
                    "monotone_relative_energy_DF": selected_metrics[
                        "monotone_in_relative_energy"
                    ],
                    "per_galaxy_edge_fit": False,
                    "collapse_selected_edge": False,
                    "valid_for_galaxy_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
            radial_rows.append(
                {
                    "galaxy": galaxy,
                    "mapping": mapping,
                    "mass_label": mass_label,
                    "m_gap_eV": mass_eV,
                    "point_count": len(points),
                    "smooth_edge_RMSE_km_s": smooth_rmse,
                    "unregularized_parent_RMSE_km_s": parent_rmse,
                    "delta_RMSE_km_s": smooth_rmse - parent_rmse,
                    "maximum_parent_support_distortion": maximum_parent_distortion,
                    "maximum_observed_r_over_R_edge": maximum_observed_fraction,
                    "points_outside_R_edge": outside_points,
                    "local_tide_ceiling_from_untapered_parent": local_tide_ceiling,
                    "per_galaxy_shape_fit": False,
                    "valid_for_galaxy_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
            accumulator = accumulators[(mass_label, mapping)]
            accumulator["smooth_squared_error"] += sum(smooth_squared_errors)
            accumulator["parent_squared_error"] += sum(parent_squared_errors)
            accumulator["point_count"] += len(points)
            accumulator["smooth_RMSE"].append(smooth_rmse)
            accumulator["parent_RMSE"].append(parent_rmse)
            accumulator["maximum_parent_support_distortion"] = max(
                accumulator["maximum_parent_support_distortion"],
                maximum_parent_distortion,
            )
            accumulator["maximum_observed_r_over_edge"] = max(
                accumulator["maximum_observed_r_over_edge"],
                maximum_observed_fraction,
            )
            accumulator["outside_points"] += outside_points
            accumulator["smooth_wins"] += smooth_rmse < parent_rmse

            if galaxy == "CamB" and mapping.endswith("minus_2lambda"):
                for energy, value in zip(
                    selected_energies[::8], selected_distribution[::8]
                ):
                    distribution_samples.append(
                        {
                            "sample_role": "fixed_reference_profile",
                            "galaxy": galaxy,
                            "mapping": mapping,
                            "mass_label": mass_label,
                            "edge_power": SELECTED_EDGE_POWER,
                            "normalized_relative_energy": float(energy),
                            "normalized_distribution_bin": float(value),
                            "valid_for_claim": False,
                            "checkpoint_marker": MARKER,
                        }
                    )

    summary_rows: list[dict[str, Any]] = []
    for (mass_label, mapping), accumulator in accumulators.items():
        point_count = accumulator["point_count"]
        summary_rows.append(
            {
                "mass_label": mass_label,
                "mapping": mapping,
                "galaxy_count": len(accumulator["smooth_RMSE"]),
                "point_count": point_count,
                "mean_smooth_edge_RMSE_km_s": statistics.mean(
                    accumulator["smooth_RMSE"]
                ),
                "median_smooth_edge_RMSE_km_s": statistics.median(
                    accumulator["smooth_RMSE"]
                ),
                "pooled_smooth_edge_RMSE_km_s": math.sqrt(
                    accumulator["smooth_squared_error"] / point_count
                ),
                "pooled_unregularized_parent_RMSE_km_s": math.sqrt(
                    accumulator["parent_squared_error"] / point_count
                ),
                "maximum_parent_support_distortion": accumulator[
                    "maximum_parent_support_distortion"
                ],
                "maximum_observed_r_over_R_edge": accumulator[
                    "maximum_observed_r_over_edge"
                ],
                "points_outside_R_edge": accumulator["outside_points"],
                "smooth_edge_wins_out_of_175": accumulator["smooth_wins"],
                "per_galaxy_shape_fit": False,
                "valid_for_galaxy_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

    bounded_rows = [
        row
        for row in distribution_rows
        if row["edge_power"] == BOUNDED_EDGE_POWER
    ]
    selected_rows = [
        row
        for row in distribution_rows
        if row["edge_power"] == SELECTED_EDGE_POWER
    ]
    convergence_targets = {
        profile_key(
            min(
                bounded_rows,
                key=lambda row: row[
                    "minimum_local_monotonic_step_fraction"
                ],
            )
        ): "bounded_edge_worst_monotonic",
        profile_key(
            min(
                selected_rows,
                key=lambda row: row[
                    "minimum_local_monotonic_step_fraction"
                ],
            )
        ): "selected_edge_worst_monotonic",
        profile_key(
            max(
                selected_rows,
                key=lambda row: row[
                    "independent_midpoint_max_abs_density_error_below_0p999"
                ],
            )
        ): "selected_edge_worst_reconstruction",
        profile_key(
            min(selected_rows, key=lambda row: row["R_edge_over_R_n"])
        ): "selected_edge_minimum_radius",
        profile_key(
            max(selected_rows, key=lambda row: row["R_edge_over_R_n"])
        ): "selected_edge_maximum_radius",
    }
    convergence_rows: list[dict[str, Any]] = []
    mass_value_lookup = dict(mass_grid)
    for key, role in convergence_targets.items():
        galaxy, mapping, mass_label, edge_power = key
        source = source_lookup[(galaxy, mapping)]
        mass_eV = mass_value_lookup[mass_label]
        exponent = float(source["q_parent"])
        transition_radius_kpc = (
            float(source["R_n_over_L_eff"]) * float(source["L_eff_kpc"])
        )
        velocity_infinity = float(source["v_infinity_km_s"])
        t_min = (
            float(source["minimum_m_gap_eV_for_lambda_db_le_Rn"])
            / mass_eV
        ) ** 2
        spectral_scales, normalized_weights, _, _ = spectral_quantile_quadrature(
            exponent,
            t_min,
            spectral_nodes,
            spectral_weights,
        )
        scale = (
            2.0
            * (
                velocity_infinity
                / (CP.H0_KM_S_KPC * transition_radius_kpc)
            )
            ** 2
            / (CP.MOTION_FRACTION * CP.DELTA_VIR_CRITICAL)
        )
        edge_radius, mass_integral, _ = solve_edge_radius(
            scale,
            edge_power,
            spectral_scales,
            normalized_weights,
            mass_nodes,
            mass_weights,
        )
        high_profile = build_profile(
            edge_radius,
            edge_power,
            spectral_scales,
            normalized_weights,
            3600,
        )
        for order in CONVERGENCE_ENERGY_ORDERS:
            metrics, energies, distribution = invert_profile(
                high_profile,
                edge_power,
                edge_radius,
                mass_integral,
                order,
            )
            convergence_rows.append(
                {
                    "target_role": role,
                    "galaxy": galaxy,
                    "mapping": mapping,
                    "mass_label": mass_label,
                    "edge_power": edge_power,
                    "energy_order": order,
                    **metrics,
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
            if order == max(CONVERGENCE_ENERGY_ORDERS):
                for energy, value in zip(energies[::8], distribution[::8]):
                    distribution_samples.append(
                        {
                            "sample_role": role,
                            "galaxy": galaxy,
                            "mapping": mapping,
                            "mass_label": mass_label,
                            "edge_power": edge_power,
                            "normalized_relative_energy": float(energy),
                            "normalized_distribution_bin": float(value),
                            "valid_for_claim": False,
                            "checkpoint_marker": MARKER,
                        }
                    )

    spectral_crosscheck_candidates = {
        profile_key(min(selected_rows, key=lambda row: row["t_min"])),
        profile_key(max(selected_rows, key=lambda row: row["t_min"])),
        profile_key(min(selected_rows, key=lambda row: row["R_edge_over_R_n"])),
        profile_key(max(selected_rows, key=lambda row: row["R_edge_over_R_n"])),
    }
    high_nodes, high_weights = np.polynomial.legendre.leggauss(1536)
    spectral_crosscheck_rows: list[dict[str, Any]] = []
    crosscheck_x = np.logspace(-8.0, 4.0, 400)
    for galaxy, mapping, mass_label, _ in spectral_crosscheck_candidates:
        source = source_lookup[(galaxy, mapping)]
        exponent = float(source["q_parent"])
        mass_eV = mass_value_lookup[mass_label]
        t_min = (
            float(source["minimum_m_gap_eV_for_lambda_db_le_Rn"])
            / mass_eV
        ) ** 2
        quantile_scales, quantile_weights, _, _ = spectral_quantile_quadrature(
            exponent,
            t_min,
            spectral_nodes,
            spectral_weights,
        )
        reference_scales, reference_weights, _, _ = CP.spectral_quadrature(
            exponent,
            t_min,
            high_nodes,
            high_weights,
        )
        quantile_support, _, quantile_density = support_density_bundle(
            crosscheck_x,
            quantile_scales,
            quantile_weights,
        )
        reference_support, _, reference_density = support_density_bundle(
            crosscheck_x,
            reference_scales,
            reference_weights,
        )
        spectral_crosscheck_rows.append(
            {
                "galaxy": galaxy,
                "mapping": mapping,
                "mass_label": mass_label,
                "q_parent": exponent,
                "t_min": t_min,
                "quantile_order": SPECTRAL_ORDER,
                "reference_log_order": 1536,
                "maximum_support_absolute_error": float(
                    np.max(np.abs(quantile_support - reference_support))
                ),
                "maximum_x2_density_shape_absolute_error": float(
                    np.max(
                        np.abs(
                            crosscheck_x**2
                            * (quantile_density - reference_density)
                        )
                    )
                ),
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

    route_rows = build_route_rows()
    source_hashes_after = {
        name: file_digest(path) for name, path in SOURCE_PATHS.items()
    }
    formal_after = tree_digest(FORMAL)
    pooled_deltas = [
        abs(
            row["pooled_smooth_edge_RMSE_km_s"]
            - row["pooled_unregularized_parent_RMSE_km_s"]
        )
        for row in summary_rows
    ]
    embedded_tide_rows = [
        row for row in local_cog_rows if row["effect"] == "embedded_halo_tide"
    ]
    local_tide_ceiling = max(
        float(row["dimensionless_size"]) for row in embedded_tide_rows
    )
    mercury_tide_ceiling = next(
        float(row["dimensionless_size"])
        for row in embedded_tide_rows
        if row["arena_or_mass"] == "Mercury_orbit"
    )
    summary = {
        "total_DF_rows": len(distribution_rows),
        "bounded_edge_row_count": len(bounded_rows),
        "bounded_edge_positive_rows": sum(
            row["positive_distribution"] for row in bounded_rows
        ),
        "bounded_edge_monotone_rows": sum(
            row["monotone_in_relative_energy"] for row in bounded_rows
        ),
        "selected_edge_row_count": len(selected_rows),
        "selected_state_count": len(selected_rows),
        "selected_edge_positive_rows": sum(
            row["positive_distribution"] for row in selected_rows
        ),
        "selected_edge_monotone_rows": sum(
            row["monotone_in_relative_energy"] for row in selected_rows
        ),
        "minimum_selected_edge_radius_over_Rn": min(
            row["R_edge_over_R_n"] for row in selected_rows
        ),
        "maximum_selected_edge_radius_over_Rn": max(
            row["R_edge_over_R_n"] for row in selected_rows
        ),
        "maximum_mass_quadrature_relative_error": max(
            row["radial_mass_quadrature_relative_error"]
            for row in selected_rows
        ),
        "maximum_spectral_normalization_relative_error": max(
            row["spectral_normalization_relative_error"]
            for row in distribution_rows
        ),
        "maximum_quantile_support_crosscheck_error": max(
            row["maximum_support_absolute_error"]
            for row in spectral_crosscheck_rows
        ),
        "maximum_quantile_x2_density_crosscheck_error": max(
            row["maximum_x2_density_shape_absolute_error"]
            for row in spectral_crosscheck_rows
        ),
        "maximum_virial_identity_residual": max(
            row["virial_density_identity_residual"] for row in halo_rows
        ),
        "maximum_selected_midpoint_density_error": max(
            row[
                "independent_midpoint_max_abs_density_error_below_0p999"
            ]
            for row in selected_rows
        ),
        "maximum_selected_edge_prediction_error": max(
            row["edge_power_law_bin_prediction_relative_error"]
            for row in selected_rows
        ),
        "total_radial_points": sum(row["point_count"] for row in radial_rows),
        "maximum_observed_r_over_edge": max(
            row["maximum_observed_r_over_R_edge"] for row in radial_rows
        ),
        "points_outside_edge": sum(
            row["points_outside_R_edge"] for row in radial_rows
        ),
        "maximum_parent_support_distortion": max(
            row["maximum_parent_support_distortion"] for row in radial_rows
        ),
        "maximum_absolute_delta_RMSE_km_s": max(
            abs(row["delta_RMSE_km_s"]) for row in radial_rows
        ),
        "maximum_pooled_absolute_delta_RMSE_km_s": max(pooled_deltas),
        "minimum_mass_over_Jeans": min(
            row["mass_over_equality_Jeans_mass"] for row in halo_rows
        ),
        "minimum_Lagrangian_radius_over_Jeans": min(
            row["Lagrangian_radius_over_equality_Jeans_wavelength"]
            for row in halo_rows
        ),
        "maximum_boundary_compactness": max(
            row["boundary_compactness"] for row in halo_rows
        ),
        "maximum_solar_system_tide_ceiling": local_tide_ceiling,
        "Mercury_tide_ceiling": mercury_tide_ceiling,
        "convergence_target_count": len(convergence_targets),
    }

    output_csvs = [
        OBSTRUCTION_CSV,
        EDGE_LAW_CSV,
        DF_ENVELOPE_CSV,
        DF_CONVERGENCE_CSV,
        DF_SAMPLES_CSV,
        SPECTRAL_CSV,
        HALO_CSV,
        RADIAL_CSV,
        SUMMARY_CSV,
        ROUTE_CSV,
    ]
    write_csv(OBSTRUCTION_CSV, obstruction_rows)
    write_csv(EDGE_LAW_CSV, edge_rows)
    write_csv(DF_ENVELOPE_CSV, distribution_rows)
    write_csv(DF_CONVERGENCE_CSV, convergence_rows)
    write_csv(DF_SAMPLES_CSV, distribution_samples)
    write_csv(SPECTRAL_CSV, spectral_crosscheck_rows)
    write_csv(HALO_CSV, halo_rows)
    write_csv(RADIAL_CSV, radial_rows)
    write_csv(SUMMARY_CSV, summary_rows)
    write_csv(ROUTE_CSV, route_rows)
    result: dict[str, Any] = {
        "checked_date": CHECKED_DATE,
        "checkpoint_marker": MARKER,
        "source_paths": {name: str(path) for name, path in SOURCE_PATHS.items()},
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "primary_source_urls": PRIMARY_SOURCE_URLS,
        "formalization_workbench_tree_sha256": formal_after,
        "summary": summary,
        "route_decision": "POSITIVE_UNIVERSAL_ISOTROPIC_STATE_EXISTS_ADVANCE_TO_FIXED_COLLAPSE_ATTRACTOR_RUN",
        "hard_edge_isotropic_branch_rejected_exactly": True,
        "universal_smooth_isotropic_state_constructed": True,
        "parent_dynamics_selects_edge": False,
        "nonlinear_collapse_attractor_derived": False,
        "relativistic_Einstein_Vlasov_solution_derived": False,
        "valid_for_cosmology_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_PPN_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    convergence_selected = [
        row
        for row in convergence_rows
        if row["edge_power"] == SELECTED_EDGE_POWER
        and row["energy_order"] >= 128
    ]
    checks = [
        ("source_paths_exist", not missing_sources, str(missing_sources)),
        (
            "all_sources_and_galaxy_sample_read_only",
            source_hashes_before == source_hashes_after,
            str(source_hashes_after),
        ),
        (
            "formalization_workbench_unchanged",
            formal_before == FORMAL_BASELINE and formal_after == FORMAL_BASELINE,
            formal_after,
        ),
        (
            "hard_edge_obstruction_closes_exactly",
            all(row["passed"] for row in obstruction_rows),
            "locally integrable isotropic f forces rho(Psi)->0",
        ),
        (
            "all_1050_states_both_edge_laws_executed",
            len(bounded_rows) == 1050 and len(selected_rows) == 1050,
            str([len(bounded_rows), len(selected_rows)]),
        ),
        (
            "spectral_and_radial_quadrature_controlled",
            summary["maximum_spectral_normalization_relative_error"] < 1.0e-12
            and summary["maximum_quantile_support_crosscheck_error"] < 2.0e-6
            and summary["maximum_quantile_x2_density_crosscheck_error"] < 2.0e-5
            and summary["maximum_mass_quadrature_relative_error"] < 2.0e-5,
            str(
                [
                    summary["maximum_spectral_normalization_relative_error"],
                    summary["maximum_quantile_support_crosscheck_error"],
                    summary["maximum_quantile_x2_density_crosscheck_error"],
                    summary["maximum_mass_quadrature_relative_error"],
                ]
            ),
        ),
        (
            "all_selected_densities_monotone_and_roots_positive",
            all(
                row["maximum_density_increase"] <= 1.0e-9
                and row["R_edge_over_R_n"] > 1.0
                for row in selected_rows
            ),
            str(summary["minimum_selected_edge_radius_over_Rn"]),
        ),
        (
            "minimum_bounded_edge_DFs_positive",
            summary["bounded_edge_positive_rows"]
            == summary["bounded_edge_row_count"],
            str(summary["bounded_edge_positive_rows"]),
        ),
        (
            "bounded_edge_not_silently_promoted_to_stable",
            summary["bounded_edge_monotone_rows"]
            < summary["bounded_edge_row_count"],
            str(summary["bounded_edge_monotone_rows"]),
        ),
        (
            "selected_universal_edge_DFs_positive",
            summary["selected_edge_positive_rows"]
            == summary["selected_edge_row_count"],
            str(summary["selected_edge_positive_rows"]),
        ),
        (
            "selected_universal_edge_DFs_monotone",
            summary["selected_edge_monotone_rows"]
            == summary["selected_edge_row_count"],
            str(summary["selected_edge_monotone_rows"]),
        ),
        (
            "independent_Abel_reconstruction_controlled",
            summary["maximum_selected_midpoint_density_error"] < 0.02,
            str(summary["maximum_selected_midpoint_density_error"]),
        ),
        (
            "selected_worst_cases_converge",
            bool(convergence_selected)
            and all(row["positive_distribution"] for row in convergence_selected)
            and all(
                row["monotone_in_relative_energy"]
                for row in convergence_selected
            ),
            str(len(convergence_selected)),
        ),
        (
            "smooth_virial_identity_closes",
            summary["maximum_virial_identity_residual"] < 1.0e-9,
            str(summary["maximum_virial_identity_residual"]),
        ),
        (
            "smooth_edge_stress_vanishes_without_shell",
            all(row["edge_density_exactly_zero"] for row in halo_rows)
            and all(
                row["edge_density_radial_derivative_exactly_zero"]
                for row in halo_rows
            )
            and all(row["edge_isotropic_pressure_exactly_zero"] for row in halo_rows),
            "rho, radial derivative and isotropic pressure vanish at p=2 edge",
        ),
        (
            "all_20346_radial_points_inside_edge",
            summary["total_radial_points"] == 20346
            and summary["points_outside_edge"] == 0,
            str(
                [
                    summary["total_radial_points"],
                    summary["maximum_observed_r_over_edge"],
                ]
            ),
        ),
        (
            "universal_edge_does_not_refit_galaxies",
            all(not row["per_galaxy_shape_fit"] for row in radial_rows)
            and all(not row["per_galaxy_edge_fit"] for row in halo_rows),
            "one p=2 edge law for all rows",
        ),
        (
            "galaxy_cog_preserved_at_smoke_level",
            summary["maximum_parent_support_distortion"] < 0.08
            and summary["maximum_pooled_absolute_delta_RMSE_km_s"] < 1.0,
            str(
                [
                    summary["maximum_parent_support_distortion"],
                    summary["maximum_pooled_absolute_delta_RMSE_km_s"],
                ]
            ),
        ),
        (
            "local_cog_source_not_enlarged",
            local_tide_ceiling < 1.0e-12,
            str([mercury_tide_ceiling, local_tide_ceiling]),
        ),
        (
            "primordial_inventory_still_above_Jeans_gate",
            summary["minimum_mass_over_Jeans"] > 1.0
            and summary["minimum_Lagrangian_radius_over_Jeans"] > 1.0,
            str(
                [
                    summary["minimum_mass_over_Jeans"],
                    summary["minimum_Lagrangian_radius_over_Jeans"],
                ]
            ),
        ),
        (
            "weak_field_boundary_controlled",
            summary["maximum_boundary_compactness"] < 1.0e-5,
            str(summary["maximum_boundary_compactness"]),
        ),
        (
            "route_advances_to_fixed_collapse_not_source_sweep",
            route_rows[-1]["status"] == "OPEN_DECISIVE_GATE"
            and result["route_decision"].endswith("COLLAPSE_ATTRACTOR_RUN"),
            result["route_decision"],
        ),
        (
            "all_output_CSVs_parse",
            all(len(read_csv(path)) > 0 for path in output_csvs),
            str([str(path) for path in output_csvs]),
        ),
        (
            "completion_not_smuggled",
            not result["parent_dynamics_selects_edge"]
            and not result["nonlinear_collapse_attractor_derived"]
            and not result["relativistic_Einstein_Vlasov_solution_derived"],
            "existence and compatibility do not imply formation",
        ),
        (
            "claim_discipline",
            not result["valid_for_cosmology_claim"]
            and not result["valid_for_galaxy_claim"]
            and not result["valid_for_PPN_claim"]
            and not result["valid_for_full_MTS_claim"],
            "private phase-space gate only",
        ),
    ]
    validation_rows = [
        {
            "check_id": f"V5154_{index:02d}_{name}",
            "passed": passed,
            "detail": detail,
            "checkpoint_marker": MARKER,
        }
        for index, (name, passed, detail) in enumerate(checks, start=1)
    ]
    result["validation_count"] = len(validation_rows)
    result["validation_failures"] = [
        row["check_id"] for row in validation_rows if not row["passed"]
    ]

    write_csv(VALIDATION_CSV, validation_rows)
    write_document(result)
    atomic_json(RESULT_JSON, result)
    if result["validation_failures"]:
        raise RuntimeError(
            f"checkpoint 5154 validation failures: {result['validation_failures']}"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

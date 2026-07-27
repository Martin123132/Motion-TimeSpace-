from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import statistics
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import quad
from scipy.interpolate import PchipInterpolator
from scipy.optimize import minimize_scalar
from scipy.special import gamma


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
GALAXY = Path(r"D:\Users\ollet\Documents\mts-galaxy-lab")
OUT = POST / "source-intake" / "functional_rg" / "5148"
RESULT_JSON = OUT / "regime_selective_motion_response_results.json"
KERNEL_CSV = OUT / "spectral_response_kernel.csv"
GALAXY_CSV = OUT / "galaxy_kernel_interface_smoke.csv"
LOCAL_CSV = OUT / "local_cog_suppression.csv"
CONTRACT_CSV = OUT / "parent_schur_complement_contract.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5148_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5148-Y5-R2FR-one-parent-local-GR-galaxy-spectral-response-cog-theorem.md"
)
MARKER = "MTS_5148_ONE_PARENT_LOCAL_GR_GALAXY_SPECTRAL_RESPONSE_COG_THEOREM"
CHECKED_DATE = "2026-07-20"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
KPC_IN_AU = 206264806.24709636
INTEGRATION_LIMIT = 400.0


SOURCE_PATHS = {
    "local_vacuum_branch": POST
    / "4942-Y5-R2FR-O4-completed-endpoint-local-vacuum-homogeneous-motion-branch-and-C3-CFF-PPN-residual-gate.md",
    "matter_continuation": POST
    / "4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-junction-or-fifth-force-residual-gate.md",
    "local_source_residue": POST
    / "4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md",
    "projective_phase": POST
    / "4948-Y5-R2FR-single-parent-motion-Hessian-to-galaxy-phase-flow-and-universal-Jgap-interface.md",
    "static_occupation_gate": POST
    / "4949-Y5-R2FR-covariant-2PI-motion-occupation-Dyson-source-and-conserved-galaxy-stress-or-composite-route-rejection.md",
    "poynting_pair_gate": POST
    / "4952-Y5-R2FR-visible-matter-graviton-CTP-noise-kernel-to-motion-pair-source-and-frequency-support-or-composite-route-rejection.md",
    "functional_motion_hessian": POST
    / "4956-Y5-R2FR-functional-PX-motion-flow-gravity-source-and-convergence-or-derivative-hierarchy-rejection.md",
    "universal_source_theorem": POST
    / "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-local-GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md",
    "explicit_parent_boundary": POST
    / "4961-Y5-R2FR-integrated-H-origin-and-induced-EH-residue-from-motion-Hessian-or-explicit-fundamental-field-boundary.md",
    "galaxy_readme": GALAXY / "README.md",
    "galaxy_app": GALAXY / "app.js",
    "galaxy_samples": GALAXY / "data" / "samples.js",
}


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


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    temporary.replace(path)


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


def parse_locked_constants(app_text: str) -> dict[str, float]:
    keys = {
        "gamma0": "gamma0",
        "q": "qDefault",
        "ml_disk": "mlDisk",
        "ml_bulge": "mlBulge",
    }
    values: dict[str, float] = {}
    for output_key, source_key in keys.items():
        match = re.search(
            rf"\b{re.escape(source_key)}\s*:\s*([-+0-9.eE]+)", app_text
        )
        if match is None:
            raise RuntimeError(f"missing galaxy constant {source_key}")
        values[output_key] = float(match.group(1))
    return values


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
                "r": values[0],
                "v_obs": values[1],
                "err_v": values[2],
                "v_gas": values[3],
                "v_disk": values[4],
                "v_bulge": values[5],
                "sb_disk": values[6],
                "sb_bulge": values[7],
            }
        )
    return rows


def fit_scale_length(rows: list[dict[str, float]]) -> float:
    points = [row for row in rows if row["sb_disk"] > 0.0 and row["r"] > 0.0]
    radius_out = rows[-1]["r"]
    if len(points) < 3:
        return max(0.8, radius_out / 3.9)
    xs = [row["r"] for row in points]
    ys = [math.log(row["sb_disk"]) for row in points]
    count = len(xs)
    sum_x = sum(xs)
    sum_y = sum(ys)
    denominator = count * sum(value * value for value in xs) - sum_x * sum_x
    if abs(denominator) < 1.0e-9:
        return max(0.8, radius_out / 3.9)
    slope = (
        count * sum(x_value * y_value for x_value, y_value in zip(xs, ys))
        - sum_x * sum_y
    ) / denominator
    if slope >= 0.0:
        return max(0.8, radius_out / 3.9)
    return min(max(-1.0 / slope, 0.25), radius_out * 2.0)


def response_support(q_value: float, x_value: float, limit: float) -> float:
    def integrand(u_value: float) -> float:
        if u_value == 0.0:
            return 0.0
        y_value = x_value / u_value
        return (
            math.sin(u_value)
            / u_value
            * y_value ** (1.0 + q_value)
            / (1.0 + y_value**q_value) ** 2
        )

    integral = quad(
        integrand, 0.0, 1.0, epsabs=3.0e-10, epsrel=3.0e-9, limit=400
    )[0]
    left = 1.0
    while left < limit:
        right = min(left + math.pi, limit)
        integral += quad(
            integrand,
            left,
            right,
            epsabs=2.0e-10,
            epsrel=2.0e-8,
            limit=80,
        )[0]
        left = right
    return 1.0 - q_value * integral / x_value


def build_kernel(q_value: float) -> tuple[list[dict[str, Any]], dict[str, Any], Any]:
    grid_x = np.logspace(-4.0, math.log10(200.0), 120)
    grid_support = np.array(
        [response_support(q_value, float(value), INTEGRATION_LIMIT) for value in grid_x]
    )
    interpolation = PchipInterpolator(np.log(grid_x), grid_support)
    comparison_x = np.logspace(-3.0, 1.5, 80)
    canonical = 1.0 - np.exp(-(comparison_x**q_value))

    def loss(log_scale: float) -> float:
        predicted = interpolation(np.log(comparison_x) + log_scale)
        return float(np.mean((predicted - canonical) ** 2))

    optimization = minimize_scalar(
        loss,
        bounds=(math.log(0.5), math.log(5.0)),
        method="bounded",
        options={"xatol": 1.0e-9},
    )
    scale = math.exp(float(optimization.x))
    predicted = interpolation(np.log(comparison_x * scale))
    differences = predicted - canonical
    coefficient = (
        -2.0
        * math.pi**2
        * q_value
        * gamma(-q_value / 2.0)
        / (
            4.0 ** ((3.0 + q_value) / 2.0)
            * math.pi**1.5
            * gamma((3.0 + q_value) / 2.0)
        )
    )
    convergence_points = [0.01, 1.0, 100.0]
    convergence = [
        {
            "x": value,
            "support_limit_400": response_support(q_value, value, 400.0),
            "support_limit_800": response_support(q_value, value, 800.0),
        }
        for value in convergence_points
    ]
    for row in convergence:
        row["absolute_difference"] = abs(
            row["support_limit_400"] - row["support_limit_800"]
        )
    rows = [
        {
            "x": float(x_value),
            "support": float(support),
            "canonical_support": float(1.0 - math.exp(-(x_value**q_value))),
            "phase_occupation": float(x_value**q_value / (1.0 + x_value**q_value)),
            "checkpoint_marker": MARKER,
        }
        for x_value, support in zip(grid_x, grid_support)
    ]
    summary = {
        "q": q_value,
        "small_x_coefficient": float(coefficient),
        "small_x_numeric_ratio": float(
            grid_support[0] / grid_x[0] ** q_value
        ),
        "support_at_x_1": float(interpolation(0.0)),
        "support_at_x_100": float(interpolation(math.log(100.0))),
        "monotonic": bool(np.all(np.diff(grid_support) >= -2.0e-7)),
        "minimum_support": float(np.min(grid_support)),
        "maximum_support": float(np.max(grid_support)),
        "best_mu_times_L_eff": scale,
        "shape_rmse": float(math.sqrt(np.mean(differences**2))),
        "shape_mean_absolute_error": float(np.mean(np.abs(differences))),
        "shape_maximum_absolute_error": float(np.max(np.abs(differences))),
        "integration_convergence": convergence,
        "maximum_integration_difference": max(
            row["absolute_difference"] for row in convergence
        ),
    }
    return rows, summary, interpolation


def galaxy_smoke(
    samples: list[dict[str, Any]], constants: dict[str, float], scale: float
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for sample in samples:
        points = parse_rotmod(sample["text"])
        if len(points) < 2:
            raise RuntimeError(f"insufficient rows for {sample['name']}")
        points.sort(key=lambda row: row["r"])
        radius_out = points[-1]["r"]
        scale_length = fit_scale_length(points)
        outer = points[-1]
        baryonic_velocity_squared = (
            outer["v_gas"] ** 2
            + constants["ml_disk"] * outer["v_disk"] ** 2
            + constants["ml_bulge"] * outer["v_bulge"] ** 2
        )
        gas_fraction = (
            min(max(outer["v_gas"] ** 2 / baryonic_velocity_squared, 0.0), 1.0)
            if baryonic_velocity_squared > 0.0
            else 0.0
        )
        memory_scale = (0.9 / math.pi) * (radius_out / scale_length)
        memory_load = (1.0 - gas_fraction) * (radius_out / scale_length)
        effective_length = 1.8 * scale_length * (
            1.0
            + memory_scale
            * (1.0 - math.exp(-memory_load / memory_scale))
        )
        gm_proxy = baryonic_velocity_squared * radius_out
        amplitude = (
            math.pi
            * constants["gamma0"]
            * effective_length**2
            / (2.0 * scale * gm_proxy)
        )
        rows.append(
            {
                "galaxy": sample["name"].replace("_rotmod.dat", ""),
                "point_count": len(points),
                "r_out_kpc": radius_out,
                "h_kpc": scale_length,
                "f_gas_out": gas_fraction,
                "memory_load": memory_load,
                "L_eff_kpc": effective_length,
                "vbar_out_squared_km2_s2": baryonic_velocity_squared,
                "GM_proxy_km2_s2_kpc": gm_proxy,
                "kernel_amplitude_A": amplitude,
                "within_factor_two_of_A_one": 0.5 <= amplitude <= 2.0,
                "mass_proxy_is_spherical_smoke_only": True,
                "valid_for_galaxy_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    amplitudes = np.array([row["kernel_amplitude_A"] for row in rows])
    log_gm = np.log([row["GM_proxy_km2_s2_kpc"] for row in rows])
    log_scale_side = np.log(
        [constants["gamma0"] * row["L_eff_kpc"] ** 2 for row in rows]
    )
    mean_x = float(np.mean(log_gm))
    mean_y = float(np.mean(log_scale_side))
    centered_x = log_gm - mean_x
    centered_y = log_scale_side - mean_y
    slope = float(np.dot(centered_x, centered_y) / np.dot(centered_x, centered_x))
    intercept = mean_y - slope * mean_x
    residuals = log_scale_side - (intercept + slope * log_gm)
    slope_standard_error = math.sqrt(
        float(np.dot(residuals, residuals))
        / (len(rows) - 2)
        / float(np.dot(centered_x, centered_x))
    )
    correlation = float(
        np.dot(centered_x, centered_y)
        / math.sqrt(float(np.dot(centered_x, centered_x) * np.dot(centered_y, centered_y)))
    )
    summary = {
        "sample_count": len(rows),
        "amplitude_geometric_mean": float(
            math.exp(statistics.mean(math.log(value) for value in amplitudes))
        ),
        "amplitude_median": float(np.median(amplitudes)),
        "amplitude_p16": float(np.quantile(amplitudes, 0.16)),
        "amplitude_p84": float(np.quantile(amplitudes, 0.84)),
        "amplitude_minimum": float(np.min(amplitudes)),
        "amplitude_maximum": float(np.max(amplitudes)),
        "within_factor_two_of_unity": int(np.sum((amplitudes >= 0.5) & (amplitudes <= 2.0))),
        "log_relation_slope": slope,
        "log_relation_slope_standard_error": slope_standard_error,
        "log_relation_intercept": intercept,
        "log_relation_pearson_r": correlation,
        "log_relation_residual_standard_deviation": float(
            np.std(residuals, ddof=1)
        ),
        "minimum_L_eff_kpc": min(row["L_eff_kpc"] for row in rows),
        "maximum_L_eff_kpc": max(row["L_eff_kpc"] for row in rows),
    }
    return rows, summary


def local_suppression(
    q_value: float,
    small_x_coefficient: float,
    scale: float,
    amplitude_maximum: float,
    minimum_length_kpc: float,
) -> list[dict[str, Any]]:
    arenas = {
        "Earth_surface": 4.2635e-5,
        "Cassini_solar_limb": 0.00465047,
        "Mercury_orbit": 0.387098,
        "Earth_orbit": 1.0,
        "Neptune_orbit": 30.07,
    }
    rows: list[dict[str, Any]] = []
    for arena, radius_au in arenas.items():
        x_value = scale * radius_au / (minimum_length_kpc * KPC_IN_AU)
        support = small_x_coefficient * x_value**q_value
        relative_force = (
            2.0 * amplitude_maximum / math.pi * x_value * support
        )
        rows.append(
            {
                "arena": arena,
                "radius_AU": radius_au,
                "conservative_L_eff_kpc": minimum_length_kpc,
                "conservative_A": amplitude_maximum,
                "mu_r": x_value,
                "small_x_support": support,
                "relative_force_correction": relative_force,
                "comparison_ceiling": 1.0e-5,
                "passes_static_kernel_ceiling": relative_force < 1.0e-5,
                "valid_for_PPN_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows


def contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "single_public_metric_source",
            "equation_or_rule": "delta S_m/delta H = -(T_mn-g_mn T/2)/2",
            "status": "DERIVED_4960",
            "manual_arena_switch": False,
        },
        {
            "clause": "local_motion_mixing",
            "equation_or_rule": "B_hpsi[psi=0]=0 by reflection and homogeneous local branch",
            "status": "DERIVED_4942_4943",
            "manual_arena_switch": False,
        },
        {
            "clause": "phase_occupation",
            "equation_or_rule": "n_q(y)=y^q/(1+y^q); d n_q/d ln y=q n_q(1-n_q)",
            "status": "DERIVED_EXACT",
            "manual_arena_switch": False,
        },
        {
            "clause": "minimal_cog_response",
            "equation_or_rule": "C_q(y)=y n_q(y)=y^(1+q)/(1+y^q)",
            "status": "DERIVED_FROM_UV_INNER_POWER_AND_IR_PLATEAU_REQUIREMENTS",
            "manual_arena_switch": False,
        },
        {
            "clause": "required_motion_self_energy",
            "equation_or_rule": "Sigma/K_h=A C_q/(1+A C_q)",
            "status": "DERIVED_SCHUR_COMPLEMENT_TARGET",
            "manual_arena_switch": False,
        },
        {
            "clause": "static_kernel_positivity",
            "equation_or_rule": "K_eff=K_h/(1+A C_q)>0 for A>=0 and Euclidean k>0",
            "status": "DERIVED_CONDITIONAL",
            "manual_arena_switch": False,
        },
        {
            "clause": "Poynting_interface",
            "equation_or_rule": "T_EM^0i enters H universally; stationary/DC flux does not populate motion pairs",
            "status": "DERIVED_4960_AND_4952",
            "manual_arena_switch": False,
        },
        {
            "clause": "retarded_parent_realization",
            "equation_or_rule": "B K_ret^-1 B_dagger must reproduce Sigma without acausal or negative-spectral modes",
            "status": "NEXT_DERIVATION",
            "manual_arena_switch": False,
        },
        {
            "clause": "state_amplitude_and_scale",
            "equation_or_rule": "A[g,state] and mu[g,state] must follow from one CTP motion state, not per-galaxy fitting",
            "status": "NEXT_DERIVATION",
            "manual_arena_switch": False,
        },
        {
            "clause": "parent_numeric_q",
            "equation_or_rule": "q=0.77 is galaxy-locked; the direct 4948 one-point Hessian exponent did not match it",
            "status": "OPEN_NOT_SILENTLY_IDENTIFIED",
            "manual_arena_switch": False,
        },
    ]


def write_document(result: dict[str, Any]) -> None:
    kernel = result["kernel"]
    galaxy = result["galaxy_smoke"]
    mercury = next(
        row for row in result["local_suppression"] if row["arena"] == "Mercury_orbit"
    )
    DOCUMENT.write_text(
        f"""# 5148 - One-parent local-GR/galaxy spectral-response cog theorem

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

This checkpoint constructs a concrete bridge instead of recording another
missing coefficient. The already selected parent has one universal metric
source and an exact reflection-even `psi=0` local branch. Its physical Hessian
can therefore have a state-dependent block form

```text
Gamma2 = 1/2 (h,chi) [[K_h,B],[B_dagger,K_chi]] (h,chi)^T + h.T/2.
```

Eliminating the motion response gives the exact Schur complement

```text
K_eff = K_h - B K_chi^-1 B_dagger.
```

On the certified local branch `B=0`, so the Einstein/Newton/Mercury cog is
unchanged. A nonzero motion state may instead give `B!=0`; this is a branch of
the same action, not a second gravitational coupling.

## Spectral response derived from the two required cogs

Let `y=mu/k` and define

```text
n_q(y) = y^q/(1+y^q),
d n_q/d ln y = q n_q(1-n_q).
```

Flat outer rotation requires a static `1/k^3` response, while the locked MTS
inner support requires the extra circular-speed term to start as `r^q`.
Within the no-new-scale monomial class `C=y^a n_q^b`, the low-frequency
plateau fixes `a=1` and the inner `r^q` power then fixes `b=1`. The unique
minimal member of that declared class is therefore

```text
C_q(y) = y n_q(y) = y^(1+q)/(1+y^q),
D_h(k) = D_GR(k)[1+A C_q(mu/k)].
```

Thus `C_q~(mu/k)^(1+q)` at high frequency and `C_q~mu/k` at low
frequency. The corresponding required Schur complement is

```text
Sigma/K_h = A C_q/(1+A C_q),
K_eff = K_h/(1+A C_q).
```

For `A>=0` the Euclidean static kernel has no new zero. A causal retarded CTP
realization is still required before this becomes a parent-derived physical
law.

## Real-space theorem

For a point-source Green function the extra circular speed is

```text
Delta V^2(r) = [2 A G M mu/pi] S_q(mu r),
S_q(x) = 1-(q/x) integral_0^infinity du (sin u/u)
         (x/u)^(1+q)/[1+(x/u)^q]^2.
```

It obeys `S_q(x)->1` at large `x` and
`S_q(x)={kernel['small_x_coefficient']} x^q+...` for the locked
`q={kernel['q']}`. Hence the same response is negligible relative to Newton
at short distance but gives a flat plateau at long distance.

After one global spectral-to-real scale conversion
`mu L_eff={kernel['best_mu_times_L_eff']}`, this support approximates the
galaxy lab's `1-exp[-(r/L_eff)^q]` with RMSE
`{kernel['shape_rmse']}` over `10^-3 <= r/L_eff <= 10^1.5`.

## Read-only 175-galaxy smoke

Using the galaxy lab's own locked constants and exact `L_eff` construction,
the outer baryonic proxy `GM_proxy=Vbar_out^2 r_out` implies

```text
A_i = pi Gamma0 L_eff^2/(2 mu L_eff GM_proxy).
```

Across all `{galaxy['sample_count']}` LTGs, `A` has geometric mean
`{galaxy['amplitude_geometric_mean']}`, median
`{galaxy['amplitude_median']}`, and 16--84 percent range
`[{galaxy['amplitude_p16']},{galaxy['amplitude_p84']}]`;
`{galaxy['within_factor_two_of_unity']}/175` rows lie within a factor two of
unity. The log relation has Pearson `r={galaxy['log_relation_pearson_r']}` and
slope `{galaxy['log_relation_slope']} +/- {galaxy['log_relation_slope_standard_error']}`.

This is promising interface evidence, not a galaxy claim. `Vbar_out^2 r_out`
is only a spherical mass proxy for disk data, the scatter is material, and
`A` and `mu` have not yet been calculated from the parent CTP state.

## Local suppression and Poynting

Combining the largest inferred `A` with the smallest `L_eff` gives a deliberately
conservative Mercury static-kernel correction of
`{mercury['relative_force_correction']}`, far below the checkpoint's `1e-5`
smoke ceiling. This does not replace a covariant PPN calculation, but it proves
that the candidate response has the required UV suppression rather than
breaking Mercury to repair galaxies.

The Poynting vector remains part of the one Hilbert source. Checkpoint 4952
already proves that stationary/DC flux does not create motion pairs, so it is
not smuggled in as an activation source. Time-dependent electromagnetic or
gravitational flux can matter only if the next retarded CTP self-energy
calculation derives it.

## Claim boundary and next derivation

Derived here:

- the unique minimal spectral factor within the declared `y^a n_q^b` class
  satisfying the selected inner and outer power requirements;
- exact logistic phase flow;
- exact static Schur-complement target and Euclidean positivity;
- the real-space support transform and short/long-distance limits;
- a read-only 175-galaxy amplitude/shape smoke and conservative local bound.

Not yet derived:

- `B K_ret^-1 B_dagger` from the actual occupied motion CTP Hessian;
- the state law fixing `A` and `mu` from source history without per-galaxy
  fitting;
- the locked numeric `q=0.77` from the parent, since the direct 4948
  one-point exponent failed;
- causal spectral positivity, full lensing/slip and PPN projections.

The next target is therefore one calculation: evaluate the retarded
state-dependent motion polarization and test whether its transverse metric
self-energy has the required `A C_q/(1+A C_q)` form. If it does not, this
route is rejected rather than retained as closure.

The protected `formalization-workbench` hash remains
`{result['formalization_workbench_tree_sha256']}`. No GitHub or galaxy-repo
write occurred.
""",
        encoding="utf-8",
    )


def main() -> None:
    missing = [str(path) for path in SOURCE_PATHS.values() if not path.exists()]
    if missing:
        raise RuntimeError(f"missing source paths: {missing}")
    source_hashes_before = {
        name: file_digest(path) for name, path in SOURCE_PATHS.items()
    }
    formal_before = tree_digest(FORMAL)
    app_text = SOURCE_PATHS["galaxy_app"].read_text(encoding="utf-8-sig")
    constants = parse_locked_constants(app_text)
    samples = parse_samples(SOURCE_PATHS["galaxy_samples"])
    kernel_rows, kernel_summary, _ = build_kernel(constants["q"])
    galaxy_rows, galaxy_summary = galaxy_smoke(
        samples, constants, kernel_summary["best_mu_times_L_eff"]
    )
    local_rows = local_suppression(
        constants["q"],
        kernel_summary["small_x_coefficient"],
        kernel_summary["best_mu_times_L_eff"],
        galaxy_summary["amplitude_maximum"],
        galaxy_summary["minimum_L_eff_kpc"],
    )
    contracts = contract_rows()
    write_csv(KERNEL_CSV, kernel_rows)
    write_csv(GALAXY_CSV, galaxy_rows)
    write_csv(LOCAL_CSV, local_rows)
    write_csv(CONTRACT_CSV, contracts)
    source_hashes_after = {
        name: file_digest(path) for name, path in SOURCE_PATHS.items()
    }
    formal_after = tree_digest(FORMAL)
    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "source_paths": {name: str(path) for name, path in SOURCE_PATHS.items()},
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "locked_constants": constants,
        "kernel": kernel_summary,
        "galaxy_smoke": galaxy_summary,
        "local_suppression": local_rows,
        "formalization_workbench_tree_sha256": formal_after,
        "valid_for_new_local_GR_claim": False,
        "valid_for_PPN_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    checks = [
        ("source_paths_exist", not missing, str(missing)),
        (
            "source_files_read_only",
            source_hashes_before == source_hashes_after,
            str(source_hashes_after),
        ),
        (
            "formal_tree_unchanged",
            formal_before == FORMAL_BASELINE and formal_after == FORMAL_BASELINE,
            formal_after,
        ),
        (
            "locked_constants_parsed",
            constants
            == {"gamma0": 809.956, "q": 0.77, "ml_disk": 0.5, "ml_bulge": 0.7},
            str(constants),
        ),
        ("all_175_galaxies_parsed", len(galaxy_rows) == 175, str(len(galaxy_rows))),
        (
            "kernel_support_monotonic",
            kernel_summary["monotonic"]
            and kernel_summary["minimum_support"] >= -1.0e-6
            and kernel_summary["maximum_support"] <= 1.01,
            str(
                (
                    kernel_summary["minimum_support"],
                    kernel_summary["maximum_support"],
                )
            ),
        ),
        (
            "small_x_asymptotic",
            abs(
                kernel_summary["small_x_numeric_ratio"]
                / kernel_summary["small_x_coefficient"]
                - 1.0
            )
            < 0.01,
            str(
                (
                    kernel_summary["small_x_numeric_ratio"],
                    kernel_summary["small_x_coefficient"],
                )
            ),
        ),
        (
            "flat_outer_plateau",
            kernel_summary["support_at_x_100"] > 0.95,
            str(kernel_summary["support_at_x_100"]),
        ),
        (
            "integral_convergence",
            kernel_summary["maximum_integration_difference"] < 5.0e-4,
            str(kernel_summary["maximum_integration_difference"]),
        ),
        (
            "canonical_shape_smoke",
            kernel_summary["shape_rmse"] < 0.07,
            str(kernel_summary["shape_rmse"]),
        ),
        (
            "amplitude_order_unity_smoke",
            0.5 <= galaxy_summary["amplitude_geometric_mean"] <= 2.0
            and galaxy_summary["within_factor_two_of_unity"] >= 100,
            str(
                (
                    galaxy_summary["amplitude_geometric_mean"],
                    galaxy_summary["within_factor_two_of_unity"],
                )
            ),
        ),
        (
            "source_scale_correlation_smoke",
            galaxy_summary["log_relation_pearson_r"] > 0.9,
            str(galaxy_summary["log_relation_pearson_r"]),
        ),
        (
            "local_static_kernel_suppressed",
            all(row["passes_static_kernel_ceiling"] for row in local_rows),
            str(max(row["relative_force_correction"] for row in local_rows)),
        ),
        (
            "no_manual_arena_switch",
            all(not row["manual_arena_switch"] for row in contracts),
            "single parent Hessian and state-dependent Schur complement",
        ),
        (
            "claim_discipline",
            not result["valid_for_new_local_GR_claim"]
            and not result["valid_for_PPN_claim"]
            and not result["valid_for_galaxy_claim"]
            and not result["valid_for_full_MTS_claim"],
            "constructive kernel target and smoke only",
        ),
    ]
    validation_rows = [
        {
            "check_id": f"V5148_{index:02d}_{name}",
            "passed": passed,
            "detail": detail,
            "checkpoint_marker": MARKER,
        }
        for index, (name, passed, detail) in enumerate(checks, start=1)
    ]
    result["validation_failures"] = [
        row["check_id"] for row in validation_rows if not row["passed"]
    ]
    atomic_json(RESULT_JSON, result)
    write_csv(VALIDATION_CSV, validation_rows)
    write_document(result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["validation_failures"]:
        raise RuntimeError(
            f"checkpoint 5148 validation failures: {result['validation_failures']}"
        )


if __name__ == "__main__":
    main()

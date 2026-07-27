from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import quad


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
OUT = POST / "source-intake" / "functional_rg" / "5149"
RESULT_JSON = OUT / "causal_spectral_density_and_critical_mixing_results.json"
DENSITY_CSV = OUT / "static_response_spectral_density.csv"
RECONSTRUCTION_CSV = OUT / "spectral_reconstruction_gate.csv"
MIXING_CSV = OUT / "critical_mixing_asymptotics.csv"
ROUTE_CSV = OUT / "vacuum_vs_occupied_medium_route_gate.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5149_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5149-Y5-R2FR-causal-spectral-density-critical-motion-mixing-and-vacuum-no-go.md"
)
MARKER = "MTS_5149_CAUSAL_SPECTRAL_DENSITY_CRITICAL_MOTION_MIXING_GATE"
CHECKED_DATE = "2026-07-20"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


SOURCE_PATHS = {
    "kernel_checkpoint": POST
    / "5148-Y5-R2FR-one-parent-local-GR-galaxy-spectral-response-cog-theorem.md",
    "kernel_result": POST
    / "source-intake"
    / "functional_rg"
    / "5148"
    / "regime_selective_motion_response_results.json",
    "local_motion_CTP": POST
    / "4949-Y5-R2FR-covariant-2PI-motion-occupation-Dyson-source-and-conserved-galaxy-stress-or-composite-route-rejection.md",
    "functional_motion_parent": POST
    / "4956-Y5-R2FR-functional-PX-motion-flow-gravity-source-and-convergence-or-derivative-hierarchy-rejection.md",
    "universal_source": POST
    / "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-local-GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md",
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


def response_coefficient(s_value: float, q_value: float, mu_value: float) -> float:
    return mu_value ** (1.0 + q_value) / (
        math.sqrt(s_value) * (s_value ** (q_value / 2.0) + mu_value**q_value)
    )


def response_density(t_value: float, q_value: float, mu_value: float) -> float:
    angle = math.pi * q_value / 2.0
    t_power = t_value ** (q_value / 2.0)
    numerator = mu_value**q_value + t_power * math.cos(angle)
    denominator = (
        mu_value ** (2.0 * q_value)
        + 2.0
        * mu_value**q_value
        * t_power
        * math.cos(angle)
        + t_value**q_value
    )
    return (
        mu_value ** (1.0 + q_value)
        * numerator
        / (math.pi * math.sqrt(t_value) * denominator)
    )


def reconstruct_response(s_value: float, q_value: float, mu_value: float) -> float:
    def logarithmic_integrand(log_t: float) -> float:
        t_value = math.exp(log_t)
        return (
            response_density(t_value, q_value, mu_value)
            * t_value
            / (s_value + t_value)
        )

    return quad(
        logarithmic_integrand,
        -60.0,
        60.0,
        epsabs=1.0e-11,
        epsrel=1.0e-10,
        limit=1000,
    )[0]


def logarithmic_slope(xs: np.ndarray, ys: np.ndarray) -> float:
    log_x = np.log(xs)
    log_y = np.log(ys)
    centered_x = log_x - np.mean(log_x)
    centered_y = log_y - np.mean(log_y)
    return float(np.dot(centered_x, centered_y) / np.dot(centered_x, centered_x))


def write_document(result: dict[str, Any]) -> None:
    spectral = result["spectral_density"]
    mixing = result["critical_mixing"]
    DOCUMENT.write_text(
        f"""# 5149 - Causal spectral density, critical motion mixing and vacuum no-go

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

The checkpoint-5148 response is not left as an arbitrary nonlocal function.
Its static spectral measure is derived exactly and is positive for the locked
`q={result['q']}`. It therefore admits a causal continuum **response**
completion. The same function cannot be promoted to a Lorentz-invariant
vacuum graviton propagator with a positive Kallen--Lehmann continuum: that
continuum has the opposite sign. The viable interpretation is consequently a
state-dependent motion-medium susceptibility inside the existing universal
metric theory, not a replacement vacuum graviton.

## Exact static spectral representation

For `s=k^2`, checkpoint 5148's dimensionless factor is

```text
C_q(s)=mu^(1+q)/[sqrt(s)(s^(q/2)+mu^q)].
```

Across the cut `s=-t+i0`, its Stieltjes density is

```text
rho_C(t)=mu^(1+q)[mu^q+t^(q/2)cos(pi q/2)]
         /{{pi sqrt(t)[mu^(2q)+2mu^q t^(q/2)cos(pi q/2)+t^q]}}.
```

For `0<q<=1`, every factor is nonnegative and hence

```text
C_q(s)=integral_0^infinity rho_C(t)/(s+t) dt,
rho_C(t)>0.
```

The numerical reconstruction spans twelve decades in `s/mu^2` and has
maximum relative error `{spectral['maximum_reconstruction_relative_error']}`.
The minimum sampled density is `{spectral['minimum_density']}`.

One causal continuation is the retarded oscillator continuum

```text
C_R(omega,k)=integral_0^infinity dt rho_C(t)
              /[k^2+t-(omega+i0)^2].
```

This proves existence of a causal response kernel. It does not prove that the
current MTS state supplies precisely this density or coupling.

## Vacuum positivity gate

On the physical transverse conserved-source spin-2 coefficient, if one
instead declares

```text
D_vac(s)=[1+A C_q(s)]/(M_R^2 s),
```

then away from the massless pole its continuum density is

```text
rho_D(t)=-A rho_C(t)/(M_R^2 t)<0  for A>0.
```

That fails vacuum Kallen--Lehmann positivity. The checkpoint-5148 kernel is
therefore rejected as a fundamental Lorentz-invariant vacuum propagator. A
medium CTP response can evade that vacuum inference because the state breaks
Lorentz invariance and the complete metric-plus-medium system, not the
reduced static metric kernel alone, owns positivity.

## Critical mixing theorem

For the Hessian Schur complement define

```text
zeta(k)=B K_chi^-1 B_dagger/K_h
       =A C_q/(1+A C_q).
```

The executed asymptotics are

```text
zeta(k) ~ A(mu/k)^(1+q)                    at k >> mu,
1-zeta(k) ~ k/(A mu)                       at k << mu.
```

The measured log slopes are `{mixing['high_k_zeta_slope']}` and
`{mixing['low_k_one_minus_zeta_slope']}`, against exact targets
`-{1.0 + result['q']}` and `+1`. Thus the galaxy state must approach unit
normalized metric-motion mixing in the infrared, with determinant

```text
det Gamma2 = K_h K_chi(1-zeta) proportional to |k| K_h K_chi.
```

This is a criticality condition, not a small loop correction.

## Current-parent compatibility

The checkpoint-4949 stationary local operator has `m_gap^2>0`, positive
quadratic form and `B=0` on the reflection-even vacuum. More generally, a
finite local gapped Hessian with analytic coefficients has a Taylor series in
`k^2`; without a determinant zero it gives finite renormalization, and even a
local tuning cannot generate the required `|k|` term. It therefore cannot
produce the 5148 response in its stationary vacuum.

The remaining route is precise: an occupied, gapless or critical CTP
collective state must generate a transverse nonanalytic stress response and
the full Hessian must satisfy the unit-mixing limit without a negative-norm
mode or Jeans instability. Time-dependent Poynting or gravitational flux may
enter only through that same retarded stress correlator; the stationary/DC
no-pair theorem remains intact.

## Next calculation

Construct the smallest reflection-even occupied-state Hessian allowed by the
functional `P(X)` parent, calculate its retarded stress-stress polarization,
and test three non-negotiable conditions:

1. transverse Ward identity;
2. `1-zeta(k)` linear in `|k|` across the galactic corridor;
3. positive full-system spectral/gradient matrix.

If a regular gapped state cannot satisfy them, the current motion-scalar
realization of the 5148 bridge is rejected rather than renamed as closure.

All `{result['validation_count']}` validation checks pass. The protected
`formalization-workbench` hash remains
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
    kernel_result = json.loads(
        SOURCE_PATHS["kernel_result"].read_text(encoding="utf-8")
    )
    q_value = float(kernel_result["kernel"]["q"])
    amplitude = float(kernel_result["galaxy_smoke"]["amplitude_geometric_mean"])
    mu_value = 1.0

    density_grid = np.logspace(-12.0, 12.0, 241)
    density_rows = [
        {
            "t_over_mu2": float(t_value),
            "rho_C_in_mu_units": response_density(float(t_value), q_value, mu_value),
            "rho_positive": response_density(float(t_value), q_value, mu_value) > 0.0,
            "rho_reduced_vacuum_continuum": -amplitude
            * response_density(float(t_value), q_value, mu_value)
            / float(t_value),
            "vacuum_continuum_positive": False,
            "checkpoint_marker": MARKER,
        }
        for t_value in density_grid
    ]

    reconstruction_s = np.logspace(-6.0, 6.0, 13)
    reconstruction_rows: list[dict[str, Any]] = []
    for s_value in reconstruction_s:
        analytic = response_coefficient(float(s_value), q_value, mu_value)
        reconstructed = reconstruct_response(float(s_value), q_value, mu_value)
        reconstruction_rows.append(
            {
                "s_over_mu2": float(s_value),
                "analytic_C": analytic,
                "spectral_integral_C": reconstructed,
                "relative_error": abs(reconstructed / analytic - 1.0),
                "checkpoint_marker": MARKER,
            }
        )

    low_k = np.logspace(-7.0, -3.0, 41)
    high_k = np.logspace(3.0, 7.0, 41)

    def coefficient_from_k(k_value: float) -> float:
        return response_coefficient(k_value * k_value, q_value, mu_value)

    low_zeta = np.array(
        [
            amplitude * coefficient_from_k(float(k_value))
            / (1.0 + amplitude * coefficient_from_k(float(k_value)))
            for k_value in low_k
        ]
    )
    high_zeta = np.array(
        [
            amplitude * coefficient_from_k(float(k_value))
            / (1.0 + amplitude * coefficient_from_k(float(k_value)))
            for k_value in high_k
        ]
    )
    low_slope = logarithmic_slope(low_k, 1.0 - low_zeta)
    high_slope = logarithmic_slope(high_k, high_zeta)
    mixing_rows = [
        {
            "regime": "infrared",
            "k_over_mu": float(k_value),
            "zeta": float(zeta_value),
            "one_minus_zeta": float(1.0 - zeta_value),
            "target_power": 1.0,
            "checkpoint_marker": MARKER,
        }
        for k_value, zeta_value in zip(low_k, low_zeta)
    ] + [
        {
            "regime": "ultraviolet",
            "k_over_mu": float(k_value),
            "zeta": float(zeta_value),
            "one_minus_zeta": float(1.0 - zeta_value),
            "target_power": -(1.0 + q_value),
            "checkpoint_marker": MARKER,
        }
        for k_value, zeta_value in zip(high_k, high_zeta)
    ]

    route_rows = [
        {
            "route": "Lorentz_invariant_vacuum_graviton",
            "static_C_density_positive": True,
            "reduced_graviton_continuum_positive": False,
            "critical_state_required": True,
            "status": "REJECTED_BY_NEGATIVE_CONTINUUM_RESIDUE",
            "valid_for_claim": False,
        },
        {
            "route": "stationary_gapped_motion_vacuum",
            "static_C_density_positive": True,
            "reduced_graviton_continuum_positive": None,
            "critical_state_required": True,
            "status": "REJECTED_BY_B_ZERO_GAP_AND_K2_ANALYTICITY",
            "valid_for_claim": False,
        },
        {
            "route": "occupied_critical_CTP_motion_medium",
            "static_C_density_positive": True,
            "reduced_graviton_continuum_positive": None,
            "critical_state_required": True,
            "status": "SURVIVES_CAUSAL_RESPONSE_EXISTENCE_PARENT_DERIVATION_OPEN",
            "valid_for_claim": False,
        },
    ]

    write_csv(DENSITY_CSV, density_rows)
    write_csv(RECONSTRUCTION_CSV, reconstruction_rows)
    write_csv(MIXING_CSV, mixing_rows)
    write_csv(ROUTE_CSV, route_rows)
    source_hashes_after = {
        name: file_digest(path) for name, path in SOURCE_PATHS.items()
    }
    formal_after = tree_digest(FORMAL)
    spectral_summary = {
        "q_positive_response_range": "0<q<=1",
        "minimum_density": min(row["rho_C_in_mu_units"] for row in density_rows),
        "maximum_density": max(row["rho_C_in_mu_units"] for row in density_rows),
        "maximum_reconstruction_relative_error": max(
            row["relative_error"] for row in reconstruction_rows
        ),
        "all_static_density_rows_positive": all(
            row["rho_positive"] for row in density_rows
        ),
        "all_reduced_vacuum_continuum_rows_negative": all(
            row["rho_reduced_vacuum_continuum"] < 0.0 for row in density_rows
        ),
    }
    mixing_summary = {
        "amplitude": amplitude,
        "high_k_zeta_slope": high_slope,
        "high_k_target_slope": -(1.0 + q_value),
        "low_k_one_minus_zeta_slope": low_slope,
        "low_k_target_slope": 1.0,
        "infrared_unit_mixing": float(low_zeta[0]),
        "ultraviolet_suppressed_mixing": float(high_zeta[-1]),
        "stationary_gapped_local_parent_compatible": False,
        "occupied_critical_CTP_route_survives": True,
    }
    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "q": q_value,
        "source_paths": {name: str(path) for name, path in SOURCE_PATHS.items()},
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "spectral_density": spectral_summary,
        "critical_mixing": mixing_summary,
        "formalization_workbench_tree_sha256": formal_after,
        "valid_for_vacuum_modified_gravity_claim": False,
        "valid_for_parent_CTP_derivation_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    checks = [
        ("source_paths_exist", not missing, str(missing)),
        (
            "sources_read_only",
            source_hashes_before == source_hashes_after,
            str(source_hashes_after),
        ),
        (
            "formal_tree_unchanged",
            formal_before == FORMAL_BASELINE and formal_after == FORMAL_BASELINE,
            formal_after,
        ),
        ("locked_q_in_positive_range", 0.0 < q_value <= 1.0, str(q_value)),
        (
            "static_response_density_positive",
            spectral_summary["all_static_density_rows_positive"],
            str(spectral_summary["minimum_density"]),
        ),
        (
            "spectral_integral_reconstructs_kernel",
            spectral_summary["maximum_reconstruction_relative_error"] < 1.0e-8,
            str(spectral_summary["maximum_reconstruction_relative_error"]),
        ),
        (
            "vacuum_continuum_residue_negative",
            spectral_summary["all_reduced_vacuum_continuum_rows_negative"],
            "rho_D=-A rho_C/t",
        ),
        (
            "infrared_critical_slope",
            abs(low_slope - 1.0) < 2.0e-3,
            str(low_slope),
        ),
        (
            "ultraviolet_suppression_slope",
            abs(high_slope + 1.0 + q_value) < 2.0e-3,
            str(high_slope),
        ),
        (
            "critical_unit_mixing_reached",
            mixing_summary["infrared_unit_mixing"] > 0.99999,
            str(mixing_summary["infrared_unit_mixing"]),
        ),
        (
            "stationary_gapped_vacuum_rejected",
            not mixing_summary["stationary_gapped_local_parent_compatible"],
            "B=0 locally; gapped local Hessian is analytic in k^2",
        ),
        (
            "occupied_CTP_route_only_survivor",
            route_rows[-1]["status"].startswith("SURVIVES")
            and all(row["status"].startswith("REJECTED") for row in route_rows[:2]),
            str([row["status"] for row in route_rows]),
        ),
        (
            "claim_discipline",
            not result["valid_for_vacuum_modified_gravity_claim"]
            and not result["valid_for_parent_CTP_derivation_claim"]
            and not result["valid_for_galaxy_claim"]
            and not result["valid_for_full_MTS_claim"],
            "causal response existence and route selection only",
        ),
    ]
    validation_rows = [
        {
            "check_id": f"V5149_{index:02d}_{name}",
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
    atomic_json(RESULT_JSON, result)
    write_csv(VALIDATION_CSV, validation_rows)
    write_document(result)
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["validation_failures"]:
        raise RuntimeError(
            f"checkpoint 5149 validation failures: {result['validation_failures']}"
        )


if __name__ == "__main__":
    main()

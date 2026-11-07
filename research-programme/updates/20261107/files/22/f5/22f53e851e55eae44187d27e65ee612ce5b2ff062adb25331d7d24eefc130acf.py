import os

import sympy as sp
from common import ROOT, modest, require, write, digest


def main():
    modest()
    mu, omega, scale = sp.symbols("mu omega a", positive=True)
    hubble, potential, position, velocity, source = sp.symbols("H U X V J", real=True)
    frequency_rate = sp.symbols("frequency_rate", real=True)
    coordinate = (mu * position + sp.I * velocity) / sp.sqrt(2 * mu)
    conjugate = sp.conjugate(coordinate)
    exact_derivative = sp.diff(coordinate, position) * velocity + sp.diff(coordinate, velocity) * (-mu**2 * position + potential * position + source) + sp.diff(coordinate, mu) * frequency_rate
    predicted = -sp.I * mu * coordinate + frequency_rate / (2 * mu) * conjugate + sp.I * (potential * position + source) / sp.sqrt(2 * mu)
    checks = {"oscillator_coordinate_evolution": sp.simplify(exact_derivative - predicted)}
    action = sp.simplify(coordinate * conjugate)
    action_rate = sp.diff(action, position) * velocity + sp.diff(action, velocity) * (-mu**2 * position + potential * position) + sp.diff(action, mu) * hubble * mu
    checks["background_action_rate"] = sp.simplify(action_rate - hubble * sp.re(coordinate**2) - potential / mu * sp.im(coordinate**2))
    comoving_energy_mass = ((velocity - hubble * position)**2 + mu**2 * position**2) / (2 * mu)
    checks["comoving_energy_action_difference"] = sp.simplify(comoving_energy_mass - action + hubble * position * velocity / mu - hubble**2 * position**2 / (2 * mu))
    real_part, imaginary_part, lapse = sp.symbols("Xpart Ypart Lapse", real=True)
    denominator = scale**2 * sp.sqrt(mu * omega)
    density_coefficient = mu * (omega + mu) + hubble**2
    quadrature_coefficient = hubble * (omega - mu)
    density = (density_coefficient * real_part + quadrature_coefficient * imaginary_part) / denominator
    pressure = ((density_coefficient - 2 * mu**2) * real_part + quadrature_coefficient * imaginary_part) / denominator
    current_over_k = (-hubble * real_part + mu * imaginary_part) / denominator
    regular_denominator = density_coefficient + quadrature_coefficient * hubble / mu
    pressure_density = 1 - 2 * mu**2 / regular_denominator
    pressure_current = 2 * mu * quadrature_coefficient / regular_denominator
    checks["regular_projected_pressure"] = sp.simplify(pressure + lapse - pressure_density * (density + lapse) - pressure_current * current_over_k - (1 - pressure_density) * lapse)
    checks["positive_regular_denominator"] = sp.simplify(regular_denominator - mu * (omega + mu) - hubble**2 * omega / mu)
    beat = (omega - mu) / (omega + mu)
    checks["frozen_background_pressure"] = sp.simplify(pressure_density.subs(hubble, 0) - beat)
    checks["frozen_background_current_coefficient"] = sp.simplify(pressure_current.subs(hubble, 0))
    wave = sp.symbols("k", positive=True)
    checks["beat_dispersion"] = sp.factor(((omega - mu)**2 - wave**2 * beat).subs(wave**2, omega**2 - mu**2))
    checks["nonrelativistic_pressure_limit"] = sp.limit(((sp.sqrt(wave**2 + mu**2) - mu) / (sp.sqrt(wave**2 + mu**2) + mu)) / wave**2, wave, 0) - 1 / (4 * mu**2)
    phase, amplitude, amplitude_rate, frequency = sp.symbols("phase amplitude amplitude_rate frequency", real=True)
    exponential = sp.exp(-sp.I * phase)
    checks["fast_integration_by_parts"] = sp.simplify(sp.I * (amplitude_rate * exponential - sp.I * frequency * amplitude * exponential) - sp.I * amplitude_rate * exponential - frequency * amplitude * exponential)
    rows = [dict(name=name, residual=str(sp.simplify(value)), passed=sp.simplify(value) == 0) for name, value in checks.items()]
    result = dict(passed=all(row["passed"] for row in rows), pid=os.getpid(), checks=rows,
        pressure_density=str(sp.factor(pressure_density)), pressure_current=str(sp.factor(pressure_current)),
        regular_denominator=str(sp.factor(regular_denominator)), source_sha256=digest(__file__),
        assumptions=["retained canonical quadratic real field", "flat FLRW reference background", "mu=am positive", "omega^2=k^2+mu^2", "metric driving retained", "phase projection is not automatically a time average"])
    write(ROOT / "derivation-result.json", result)
    print(dict(passed=result["passed"], identities=len(rows), pressure_density=result["pressure_density"], pressure_current=result["pressure_current"]), flush=True)
    require(result["passed"], "symbolic derivation failed")


if __name__ == "__main__":
    main()

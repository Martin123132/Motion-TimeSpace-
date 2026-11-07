from __future__ import annotations

from datetime import datetime, timezone
import sympy as sp

from sidebands import ROOT, BRANCH, digest, read_json, write_json, modest_process


def main():
    modest_process()
    tidal_ratio, anomaly = sp.symbols('k tau', real=True)
    checks = []

    def exact(name, expression):
        residual = sp.factor(expression)
        assert residual == 0, (name, residual)
        checks.append({'name': name, 'passed': True, 'residual': str(residual)})

    linear_m2 = (-2+3*tidal_ratio)*sp.cos(anomaly)-4*sp.I*(1+tidal_ratio)*sp.sin(anomaly)
    linear_m0 = (-2+3*tidal_ratio)*sp.cos(anomaly)
    amplitudes = {}
    for azimuth, harmonic, expression, expected in [(2, 1, linear_m2, 1+sp.Rational(7, 2)*tidal_ratio),
                 (2, -1, linear_m2, -3-tidal_ratio/2), (0, 1, linear_m0, -1+sp.Rational(3, 2)*tidal_ratio)]:
        projected = sp.integrate(sp.expand_complex(expression*sp.exp(sp.I*harmonic*anomaly)), (anomaly, 0, 2*sp.pi))/(2*sp.pi)
        exact('trace-free quadrupole sideband '+str((azimuth, harmonic)), projected-expected)
        amplitudes[(azimuth, harmonic)] = projected
    powers = {(2, 1): sp.Rational(3, 2)**6*amplitudes[(2, 1)]**2,
              (2, -1): sp.Rational(1, 2)**6*amplitudes[(2, -1)]**2,
              (0, 1): sp.Rational(2, 3)*sp.Rational(1, 2)**6*amplitudes[(0, 1)]**2}
    radial_loss_factor = powers[(2, 1)]/3-powers[(2, -1)]+powers[(0, 1)]
    exact('Kepler radial action loss at zero tide', radial_loss_factor.subs(tidal_ratio, 0)-sp.Rational(11, 3))
    exact('linear tide radial action loss coefficient', sp.diff(radial_loss_factor, tidal_ratio).subs(tidal_ratio, 0)-sp.Rational(53, 2))
    damping_factor = sp.expand(radial_loss_factor-sp.Rational(1, 2)*(1+tidal_ratio)**2)
    damping_ratio = sp.factor(damping_factor/sp.Rational(19, 6))
    exact('zero-tide circularisation normalization', damping_ratio.subs(tidal_ratio, 0)-1)
    coefficient = 3*sp.diff(damping_ratio, tidal_ratio).subs(tidal_ratio, 0)
    exact('tidal circularisation coefficient', coefficient-sp.Rational(459, 19))
    analysis_path = ROOT/'results/analysis/status.json'
    analysis = read_json(analysis_path)
    static_path = BRANCH/'eccentric-polar-radiation-20261005/results/pilot/status.json'
    static = read_json(static_path)
    tidal_lambda = static['static_rows'][0]['tidal_lambda']
    radius = static['orbits'][0]['radius']
    predictions = []
    for row in analysis['weak_field_baseline']:
        orbital_radius = row['separation_over_radius']*radius
        predicted_fraction = float(coefficient)*tidal_lambda/orbital_radius**5
        predictions.append({'separation_over_radius': row['separation_over_radius'], 'tidal_lambda': tidal_lambda,
                            'predicted_fractional_extra_damping': predicted_fraction,
                            'relativistic_fractional_extra_damping': row['fractional_body_extra_damping'],
                            'observed_scaled_coefficient': row['fractional_body_extra_damping']*orbital_radius**5/tidal_lambda,
                            'exact_leading_coefficient': float(coefficient),
                            'relative_finite_radius_correction': row['fractional_body_extra_damping']/predicted_fraction-1})
    source_path = BRANCH/'orbital-backreaction-20261004/20-reciprocal-tidal-orbit-and-consistent-leading-inspiral.md'
    directory = ROOT/'results/tidal-limit'
    directory.mkdir(parents=True, exist_ok=False)
    result = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(), 'script_sha256': digest(__file__),
              'input_hashes': {str(path): digest(path) for path in [analysis_path, static_path, source_path]},
              'checks': checks, 'linear_tidal_coefficient': str(coefficient),
              'fixed_geodesic_quadrupole_damping_ratio_polynomial_in_k': str(damping_ratio),
              'definition_k': '3 lambda_static/r0^5', 'predictions': predictions,
              'scope': 'Leading test mass, near-circular, weak-field, adiabatic electric quadrupole response; linear-in-lambda leading comparison, not a finite-radius exact formula.'}
    write_json(directory/'status.json', result, exclusive=True)
    print({'checks': len(checks), 'coefficient': str(coefficient), 'predictions': predictions}, flush=True)


if __name__ == '__main__':
    main()

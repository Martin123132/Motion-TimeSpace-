from __future__ import annotations

from datetime import datetime, timezone
import math
import sympy as sp

from sidebands import ROOT, BRANCH, digest, read_json, write_json, modest_process
from analyze_limit import damping


def projected_gamma(rows, key):
    projected = [{**row, 'BH_infinity_energy': row[key], 'BH_horizon_energy': 0.} for row in rows]
    return damping(projected, 'combined_ell2', 'BH')['Gamma_z_per_mu']


def main():
    modest_process()
    checks = []

    def exact(name, expression):
        residual = sp.trigsimp(sp.expand(expression))
        assert residual == 0, (name, residual)
        checks.append({'name': name, 'passed': True, 'residual': str(residual)})

    anomaly = sp.symbols('tau', real=True)
    cosine, sine = sp.cos(anomaly), sp.sin(anomaly)
    tensor = sp.Matrix([[cosine**2-sp.Rational(1, 3), cosine*sine, 0],
                        [cosine*sine, sine**2-sp.Rational(1, 3), 0], [0, 0, -sp.Rational(1, 3)]])
    derivative = -3*sp.diff(tensor, anomaly)
    exact('electric tidal tensor circular derivative norm', sum(value**2 for value in derivative)-18)
    exact('leading circular absorption normalization', sp.Rational(16, 45)*18-sp.Rational(32, 5))
    for azimuth, harmonic, expression, expected in [(2, 1, 3*cosine-4*sp.I*sine, sp.Rational(7, 2)),
                 (2, -1, 3*cosine-4*sp.I*sine, -sp.Rational(1, 2)), (0, 1, 3*cosine, sp.Rational(3, 2))]:
        projected = sp.integrate(sp.expand_complex(expression*sp.exp(sp.I*harmonic*anomaly)), (anomaly, 0, 2*sp.pi))/(2*sp.pi)
        exact('electric horizon sideband '+str((azimuth, harmonic)), projected-expected)
    power_plus = sp.Rational(3, 2)**2*sp.Rational(7, 2)**2
    power_minus = sp.Rational(1, 2)**2*sp.Rational(1, 2)**2
    power_zero = sp.Rational(2, 3)*sp.Rational(1, 2)**2*sp.Rational(3, 2)**2
    radial_factor = power_plus/3-power_minus+power_zero
    exact('horizon radial action coefficient', radial_factor-sp.Rational(19, 2))
    horizon_coefficient = (radial_factor-sp.Rational(1, 2))/sp.Rational(19, 6)
    exact('horizon circularisation coefficient', horizon_coefficient-sp.Rational(54, 19))
    analytic_path = ROOT/'results/analytic-fine/status.json'
    analysis_path = ROOT/'results/analysis/status.json'
    tidal_path = ROOT/'results/tidal-limit/status.json'
    analytic, analysis, tidal = map(read_json, [analytic_path, analysis_path, tidal_path])
    rows = []
    for baseline in analysis['weak_field_baseline']:
        separation = baseline['separation_over_radius']
        selected = [row for row in analytic['rows'] if abs(row['separation_over_radius']-separation) < 1e-10]
        mass, radius = selected[0]['mass'], selected[0]['radius']*separation
        horizon_gamma = projected_gamma(selected, 'BH_horizon_energy')
        infinity_difference = projected_gamma(selected, 'difference_infinity_energy')
        predicted_horizon_fraction = float(horizon_coefficient)*(mass/radius)**4
        electric = next(row for row in tidal['predictions'] if row['separation_over_radius'] == separation)
        lambda_static = electric['tidal_lambda']
        normalization = baseline['Newtonian_Gamma']
        rows.append({'separation_over_radius': separation, 'horizon_Gamma': horizon_gamma,
            'infinity_difference_Gamma': infinity_difference,
            'total_difference_Gamma': baseline['difference_Gamma'],
            'exact_split_relative_error': abs(infinity_difference-horizon_gamma-baseline['difference_Gamma'])/abs(baseline['difference_Gamma']),
            'horizon_over_Newtonian_Gamma': horizon_gamma/normalization,
            'predicted_horizon_over_Newtonian_Gamma': predicted_horizon_fraction,
            'horizon_leading_relative_correction': horizon_gamma/(normalization*predicted_horizon_fraction)-1,
            'outgoing_tidal_scaled_coefficient': infinity_difference/normalization*radius**5/lambda_static,
            'electric_coefficient': float(sp.Rational(459, 19)),
            'outgoing_leading_relative_correction': (infinity_difference/normalization)/(float(sp.Rational(459, 19))*lambda_static/radius**5)-1,
            'horizon_fraction_of_total_difference_magnitude': abs(horizon_gamma/baseline['difference_Gamma'])})
    directory = ROOT/'results/horizon-limit'
    directory.mkdir(parents=True, exist_ok=False)
    result = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(), 'script_sha256': digest(__file__),
              'input_hashes': {str(path): digest(path) for path in [analytic_path, analysis_path, tidal_path]},
              'checks': checks, 'leading_horizon_coefficient': str(horizon_coefficient), 'rows': rows,
              'source_url': 'https://arxiv.org/pdf/gr-qc/0407050', 'source_doi': '10.1103/PhysRevD.70.084044',
              'source_equation': '8.38, PDF page25: 16 M^6/45 times averaged squared derivatives of electric and magnetic tides',
              'source_access': 'Primary PDF text checked by web tool on2026-10-05; no new local PDF archive.',
              'scope': 'Leading slow-motion electric absorption; magnetic and relativistic corrections are subleading here.',
              'leading_separate_contributions': 'DeltaGamma_inf/Gamma_N=(459/19)lambda/r0^5; Gamma_H/Gamma_N=(54/19)(M/r0)^4; total difference is infinity difference minus horizon.',
              'warning': 'The tidal r^-5 term is not the strict leading large-radius body-minus-BH-total term at fixed parameters: removed horizon absorption scales r^-4.'}
    write_json(directory/'status.json', result, exclusive=True)
    print({'checks': len(checks), 'horizon_coefficient': str(horizon_coefficient), 'rows': rows}, flush=True)


if __name__ == '__main__':
    main()

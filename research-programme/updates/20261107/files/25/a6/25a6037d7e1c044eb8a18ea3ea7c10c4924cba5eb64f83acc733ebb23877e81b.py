from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

from common import ROOT, BRANCH, PARENT, digest, read_json, write_json, modest_process, polar_settings, imported_hashes
from analyze_inspiral import Curve, kernels


def main():
    modest_process()
    checks, inputs = [], {}

    def check(name, passed, value=None, tolerance=None):
        checks.append(dict(name=name, passed=bool(passed), value=value, tolerance=tolerance))

    def below(name, value, tolerance):
        check(name, bool(np.isfinite(value)) and value <= tolerance, float(value), tolerance)

    def load(path, script):
        report = read_json(path)
        inputs[str(path)] = digest(path)
        check(str(path)+'complete', report['state'] == 'complete')
        check(str(path)+'current producer', report['script_sha256'] == digest(ROOT/script))
        for source, expected in report.get('input_hashes', {}).items():
            check(str(path)+'input '+source, Path(source).is_file() and digest(source) == expected)
        return report

    analysis = load(ROOT/'results/analysis/status.json', 'analyze_inspiral.py')
    derivation = load(ROOT/'results/derivation/status.json', 'derive_evolution.py')
    check('13 exact checks including one phase bookkeeping identity', len(derivation['checks']) == 13 and
          all(row['passed'] and row['residual'] == '0' for row in derivation['checks']))
    mode_count = 0
    for label, expected in [('nodes-fine', 105), ('nodes-coarse', 105), ('gauss-fine', 56)]:
        directory = ROOT/'results'/label
        report = load(directory/'status.json', 'run_nodes.py')
        mode_count += len(report['rows'])
        check(label+'completion marker', (directory/'COMPLETE').is_file())
        check(label+'new modes', len(report['rows']) == expected)
        check(label+'reused endpoint count', len(report['reused']) == (14 if label.startswith('nodes') else 0))
        check(label+'unique solved modes', len({(row['node_index'], row['sector'], row['azimuth'], row['harmonic']) for row in report['rows']}) == expected)
        for row in report['rows']+report['reused']:
            path = Path(row['archive'])
            if not path.is_absolute():
                path = directory/path
            prefix = label+':'+str((row['separation_over_radius'], row['sector'], row['azimuth'], row['harmonic']))+':'
            with np.load(path, allow_pickle=False) as archive:
                check(prefix+'finite solution arrays', all(np.isfinite(archive[key]).all() for key in archive.files))
                below(prefix+'saved frequency', abs(float(archive['frequency'])/row['frequency']-1), 1e-14)
                check(prefix+'actual interior archived', ('spline_coefficients' if row['sector'] == 'polar' else 'interior_values') in archive.files)
            for key, tolerance in [('Wronskian_error', 1e-7), ('optical_error_over_component_sum', 1e-11),
                                   ('direct_body_amplitude_relative_error', 1e-7)]:
                below(prefix+key, row[key], tolerance)
            below(prefix+'outgoing unit current', row['outgoing_diagnostic']['infinity_flux_normalization_error'], 1e-11)
            below(prefix+'horizon unit current', row['horizon_diagnostic']['horizon_flux_normalization_error'], 1e-11)
            check(prefix+'positive primitive powers', all(row[key] >= 0 for key in ['BH_infinity_energy', 'BH_horizon_energy', 'body_infinity_energy']))
            if row['sector'] == 'polar':
                below(prefix+'coupled interior residual', row['interior_maximum_residual'], 1.001*polar_settings(report['arguments']['settings'])['interior_tolerance'])
                below(prefix+'boundary residual', row['interior_boundary_residual'], 1e-8)
    for comparison in analysis['comparisons']:
        if comparison['label'] != 'nested5-fine':
            below(comparison['label']+'endpoint integral control', max(comparison['relative_component_errors']), 1e-6)
    nested5 = next(row for row in analysis['comparisons'] if row['label'] == 'nested5-fine')
    nested9 = next(row for row in analysis['comparisons'] if row['label'] == 'nested9-fine')
    check('five-node diagnostic is refined rather than silently accepted', max(nested5['relative_component_errors']) > 1e-6 and
          max(nested9['relative_component_errors']) < 1e-7)
    for row in analysis['independent_gauss_point_controls']:
        below('held-out wave-node interpolation '+str(row['separation']), max(value for key, value in row.items() if key != 'separation'), 1e-8)
    below('independent integration ODE', max(analysis['ode_control']['relative_errors']), 1e-9)

    summary = analysis['summary']
    mass, radius, tidal_lambda = summary['central_mass'], summary['central_radius'], summary['tidal_lambda']
    curve = Curve(analysis['raw_nodes']['nodes-fine'], mass, radius, tidal_lambda)
    trajectory = analysis['trajectory']
    for before, after in zip(trajectory, trajectory[1:]):
        check('monotone physical flow '+str(after['separation_over_radius']),
              after['separation_over_radius'] < before['separation_over_radius'] and
              after['scaled_time_body'] > before['scaled_time_body'] and after['scaled_time_BH'] > before['scaled_time_BH'] and
              after['scaled_phase_body'] > before['scaled_phase_body'] and after['scaled_phase_BH'] > before['scaled_phase_BH'] and
              0 < after['e_over_initial_body'] < before['e_over_initial_body'] and
              0 < after['e_over_initial_BH'] < before['e_over_initial_BH'])
    check('same initial data', trajectory[0]['scaled_time_body'] == trajectory[0]['scaled_time_BH'] ==
          trajectory[0]['scaled_phase_body'] == trajectory[0]['scaled_phase_BH'] == 0 and
          trajectory[0]['e_over_initial_body'] == trajectory[0]['e_over_initial_BH'] == 1)
    for separation in np.linspace(5., 10., 51):
        semilatus = separation*radius/mass
        values = curve.rates(separation)
        check('both local flows shrink and damp '+str(separation), values['P_BH'] < 0 and values['G_BH'] < 0 and
              values['P_BH']+values['P_out']-values['P_H'] < 0 and values['G_BH']+values['G_out']-values['G_H'] < 0)
        null = {**values, 'P_out': values['P_H'], 'G_out': values['G_H']}
        check('identical response null comparison '+str(separation), np.array_equal(kernels(null, semilatus, mass)[3:], np.zeros(3)))
        check('source orbit exterior and stable '+str(separation), semilatus > 6 and separation > 1)
    for row in analysis['raw_nodes']['nodes-fine']:
        reconstructed = curve.rates(row['separation'])
        below('interpolation reproduces nodes '+str(row['separation']), max(abs(reconstructed[key]/row[key]-1) for key in reconstructed), 1e-10)

    for separation in [9., 7.5, 6.]:
        semilatus = separation*radius/mass
        values = curve.rates(separation)
        step = 2e-4
        before, after = curve.integral(separation-step), curve.integral(separation+step)
        derivative = (after-before)/(2*step)
        exact = curve.integrand(separation)
        below('trajectory differentiates to all six rates '+str(separation), max(abs((derivative-exact)/exact)), 1e-7)
        omega = 1/(mass*semilatus**1.5)
        below('geodesic orbital clock '+str(separation), abs(exact[1]/exact[0]/(mass*omega)-1), 1e-13)
        below('body eccentricity equation '+str(separation), abs((exact[2]+exact[5])/(radius/mass) /
              ((values['G_BH']+values['G_out']-values['G_H'])/(values['P_BH']+values['P_out']-values['P_H']))-1), 1e-13)

    endpoint = trajectory[-1]
    equal = summary['equal_time']
    residual_time = curve.integral(equal['BH_separation'])[0]-equal['scaled_time']
    below('equal-time radius inversion scaled by differential time', abs(residual_time)/abs(endpoint['scaled_time_difference']), 1e-8)
    check('equal-time reference radius still outside endpoint', 5 < equal['BH_separation'] < 10)
    check('phase comparison surfaces kept distinct', endpoint['scaled_phase_difference'] < 0 < equal['scaled_orbital_phase_difference'])
    equal_time_scaling = []
    for strength in [.5, 1.]:
        target_time = endpoint['scaled_time_BH']+strength*endpoint['scaled_time_difference']
        hole_radius = brentq(lambda separation: curve.integral(separation)[0]-target_time, 5., 10., xtol=1e-12)
        phase_remaining = quad(lambda separation: curve.integrand(separation)[1], hole_radius, 5., epsabs=1e-11, epsrel=2e-12)[0]
        actual = strength*endpoint['scaled_phase_difference']+phase_remaining
        linear = strength*equal['first_order_scaled_phase_difference']
        equal_time_scaling.append(dict(strength=strength, exact=actual, linear=linear, remainder=actual-linear))
    below('equal-time conversion quadratic remainder', abs(equal_time_scaling[1]['remainder']/equal_time_scaling[0]['remainder']/4-1), .005)
    below('weak-field difference plausibility, not precision validation', max(abs(np.array(summary['finite_radius_corrections_to_weak_difference']))), .03)
    below('known-pole linewidth-sweep diagnostic', summary['adiabat_maxima']['frequency_sweep_over_pole_linewidth'], .01)
    below('leading tide envelope diagnostic', summary['adiabat_maxima']['leading_electric_envelope_memory_indicator'], .01)
    below('orbital drift diagnostic', summary['adiabat_maxima']['orbit_drift_per_radian'], .01)
    check('fast imposed-drive negative control rejected', 1e5*summary['adiabat_maxima']['frequency_sweep_over_pole_linewidth'] > 1)
    check('mass ratio is an illustrative test-source choice', summary['mass_ratio_example'] == 1e-5)
    check('full-response memory bound is not asserted', 'not a full-response memory error bound' in summary['memory_scope'])

    for path in sorted((ROOT/'results/analysis').glob('*.csv')):
        with path.open(newline='', encoding='utf-8') as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            check(path.name+'well-formed table', bool(rows) and len(reader.fieldnames) == len(set(reader.fieldnames)) and
                  all(None not in row and all(value is not None for value in row.values()) for row in rows))
        inputs[str(path)] = digest(path)
    prior_path = PARENT/'results/validation/status.json'
    prior = read_json(prior_path)
    inputs[str(prior_path)] = digest(prior_path)
    for source in prior['primary_pdfs']:
        check('primary archived source '+source['path'], Path(source['path']).is_file() and digest(source['path']) == source['sha256'])
    failed = [row for row in checks if not row['passed']]
    directory = ROOT/'results/validation'
    directory.mkdir(parents=True, exist_ok=False)
    result = dict(state='failed' if failed else 'complete', script_sha256=digest(__file__),
                  time_utc=datetime.now(timezone.utc).isoformat(), input_hashes={**inputs, **imported_hashes()},
                  checks=checks, new_wave_mode_evaluations=mode_count, reused_endpoint_rows=28,
                  exact_checks=13, phase_bookkeeping_checks_in_exact_count=1,
                  primary_pdfs=prior['primary_pdfs'], source_urls=prior['source_urls'],
                  equal_time_scaling=equal_time_scaling,
                  maximum_resolution_endpoint_error=max(next(row for row in analysis['comparisons'] if row['label'] == 'nodes-coarse')['relative_component_errors']),
                  maximum_nested9_endpoint_error=max(nested9['relative_component_errors']),
                  maximum_independent_gauss8_endpoint_error=max(next(row for row in analysis['comparisons'] if row['label'] == 'independent-gauss8-fine')['relative_component_errors']),
                  note='These are correlated numerical and provenance checks, not independent physical tests.')
    write_json(directory/'status.json', result, exclusive=True)
    print(dict(checks=len(checks), failed=failed[:12], new_modes=mode_count, equal_time_scaling=equal_time_scaling), flush=True)
    assert not failed, str(len(failed))+' checks failed'


if __name__ == '__main__':
    main()


from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import psutil
from scipy.interpolate import PPoly

from companion_system import ROOT, BRANCH, ResponseProblem, reference_wave, source_jumps, determinant, encode
from response_system_v2 import DynamicProblem


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def strict_json(path):
    def pairs(values):
        result = {}
        for key, value in values:
            assert key not in result, (path, key)
            result[key] = value
        return result

    return json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def decode(value):
    return complex(value['real'], value['imaginary'])


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/validation'
    output.mkdir(exist_ok=False)
    labels = ['derivation', 'far-orbit-derivation-v2', 'main', 'fine', 'wide', 'wide-control', 'reference', 'reference-fine', 'controls', 'reduction']
    reports = {label: strict_json(ROOT/f'results/{label}/status.json') for label in labels}
    checks = []

    def check(name, passed):
        assert passed, name
        checks.append({'name': name, 'passed': True})

    script_hashes = {digest(path) for path in ROOT.glob('*.py')}
    for label, report in reports.items():
        check('complete_script_owned_'+label, report['state'] == 'complete' and report['script_sha256'] in script_hashes)
        if 'system_sha256' in report:
            check('current_system_'+label, report['system_sha256'] == digest(ROOT/'companion_system.py'))
    for label in ['derivation', 'far-orbit-derivation-v2']:
        check('all_symbolic_'+label, all(row['passed'] for row in reports[label]['checks']))
    check('symbolic_total', sum(len(reports[label]['checks']) for label in ['derivation', 'far-orbit-derivation-v2']) == 21)
    for label, expected in reports['reduction']['source_hashes'].items():
        check('reduction_input_'+label, digest(ROOT/f'results/{label}/status.json') == expected)
    provenance = strict_json(ROOT/'sources/provenance.json')
    check('source_acquisition_complete', provenance['state'] == 'complete' and provenance['script_sha256'] == digest(ROOT/'acquire_sources.py'))
    for index, source in enumerate(provenance['sources']):
        check('primary_source_'+str(index), Path(source['path']).is_file() and digest(source['path']) == source['sha256'] and source['url'].startswith('https://arxiv.org/pdf/'))
    for label in ['reference', 'reference-fine']:
        for index, row in enumerate(reports[label]['rows']):
            check('positive_reference_flux_'+label+str(index), row['pair_power_infinity_per_geometric_particle_mass_squared'] > 0 and row['pair_power_horizon_per_geometric_particle_mass_squared'] > 0)
            check('reference_jumps_'+label+str(index), max(row['jump_value_error'], row['jump_slope_error']) < 1e-9)
            if row['published_pair_flux'] is not None:
                check('published_GR_benchmark_'+label+str(index), row['published_relative_difference'] < 1e-4)
        check('quadrupole_limit_'+label, abs(reports[label]['rows'][-1]['quadrupole_ratio']-1) < .002)
        check('quadrupole_limit_convergence_'+label, abs(reports[label]['rows'][-1]['quadrupole_ratio']-1) < abs(reports[label]['rows'][-2]['quadrupole_ratio']-1))
    reference_precision = [abs(first['pair_power_infinity_per_geometric_particle_mass_squared']/second['pair_power_infinity_per_geometric_particle_mass_squared']-1)
                           for first, second in zip(reports['reference']['rows'], reports['reference-fine']['rows'])]
    check('GR_boundary_precision', max(reference_precision) < 1e-9)
    controls = reports['controls']
    check('horizon_recursion_residuals', max(row['first_eight_residuals_maximum'] for row in controls['horizon_series_controls']) < 1e-10)
    check('static_horizon_growing_solution', max(row['static_regular_shape_error'] for row in controls['static_horizon_controls']) < 1e-11)
    check('static_horizon_no_decaying_solution', max(abs(decode(row['static_decaying_over_growing_scaled'])) for row in controls['static_horizon_controls']) < 1e-11)
    check('extraction_independence', max(row['relative_excess_difference'] for row in controls['fixed_source_extraction_controls']) < 1e-11)
    check('matching_convention_independence', max(row['relative_excess_difference'] for row in controls['matching_convention_controls']) < 1e-11)
    reference_power = reports['reference']['rows'][0]['pair_power_infinity_per_geometric_particle_mass_squared']
    check('geometric_unit_scaling', max(abs(row['mass_squared_times_reference_flux']/reference_power-1) for row in controls['unit_scaling_controls']) < 1e-9)
    check('selected_circular_resonance_inaccessible', controls['circular_resonance']['formal_resonance_radius_over_body_radius'] < 1 and not controls['circular_resonance']['external_circular_resonance_accessible'])
    profile = ResponseProblem().profile
    replay_errors = []
    for label in ['main', 'fine', 'wide', 'wide-control']:
        report = reports[label]
        arguments = report['arguments']
        for index, row in enumerate(report['rows']):
            name = label+'_'+str(index)
            archive = ROOT/f'results/{label}'/row['archive']
            with np.load(archive, allow_pickle=False) as arrays:
                check('finite_archive_'+name, all(np.all(np.isfinite(arrays[key])) for key in arrays.files))
                spline = PPoly(arrays['spline_coefficients'], arrays['spline_knots'])
                solution = SimpleNamespace(sol=spline, p=arrays['parameters'].copy())
            problem = DynamicProblem(profile, complex(row['sigma']), arguments['distance'], arguments['interior_tolerance'])
            boundary = problem.boundary(spline(spline.x[0]), spline(spline.x[-1]), solution.p)
            check('interior_converged_'+name, max(abs(boundary)) < 1e-7 and row['interior_maximum_residual'] < 1.01*arguments['interior_tolerance'])
            check('physical_source_jumps_'+name, max(row['value_jump_error'], row['slope_jump_error'], row['reference_value_jump_error'], row['reference_slope_jump_error']) < 1e-9)
            check('direct_total_wave_control_'+name, row['direct_to_stable_amplitude_relative_error'] < 1e-10)
            check('positive_body_flux_'+name, row['body_pair_power_infinity'] > 0)
            amplitude = decode(row['amplitude_ratio_minus_one'])
            check('amplitude_power_consistency_'+name, abs(row['pair_flux_ratio_minus_one']-(2*amplitude.real+abs(amplitude)**2)) < 1e-15)
            _, _, master, derivative = problem.surface(solution)
            inside = np.array([1., derivative/master])
            reference = reference_wave(row['orbit'], row['mass'], row['radius'], arguments['far_phase'], arguments['outer_order'], arguments['horizon_epsilon'], arguments['horizon_order'], arguments['tolerance'])
            jump_a, jump_b = source_jumps(row['orbit'], row['mass'])
            outgoing = reference['outgoing']
            horizon = reference['horizon']
            source_outgoing = jump_b*outgoing[row['orbit']][0]-jump_a*outgoing[row['orbit']][1]
            source_horizon = jump_b*horizon[row['orbit']][0]-jump_a*horizon[row['orbit']][1]
            replay = -determinant(inside, horizon[row['radius']])/determinant(inside, outgoing[row['radius']])*source_outgoing/source_horizon
            replay_errors.append(abs(replay/amplitude-1))
    check('saved_body_response_replay', max(replay_errors) < 1e-11)
    reduction = reports['reduction']
    check('relative_excess_precision', max(row['complex_excess_relative_difference'] for row in reduction['precision_controls']) < 2e-7)
    check('relative_excess_phase_precision', max(row['imaginary_excess_relative_difference'] for row in reduction['precision_controls']) < 3e-6)
    check('shared_reference_precision', max(row['reference_power_relative_difference'] for row in reduction['precision_controls']) < 1e-9)
    far = [row for row in reduction['wide_orbit_predictions'] if row['separation_over_radius'] >= 10]
    check('unfitted_PN_improves_each_wide_prediction', all(row['relative_error_first_PN'] < row['relative_error_leading'] for row in far))
    check('unfitted_PN_error_decreases', all(first['relative_error_first_PN'] > second['relative_error_first_PN'] for first, second in zip(far, far[1:])))
    check('wide_PN_coefficient_approaches_derived_value', abs(far[-1]['inferred_first_PN_coefficient']/(85/21)-1) < .001)
    check('widest_PN_prediction_accuracy', far[-1]['relative_error_first_PN'] < 1e-6)
    check('failed_symbolic_attempt_preserved', (ROOT/'results/far-orbit-derivation/FAILED.md').is_file() and (ROOT/'far-orbit-console.txt').is_file())
    inputs = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*'))
              if path.is_file() and path.suffix in ['.py', '.json', '.npz', '.pdf'] and output not in path.parents}
    report = {'state': 'complete', 'script_sha256': digest(__file__), 'checks': checks, 'input_hashes': inputs,
              'symbolic_checks': 21, 'interior_evaluations': 25, 'saved_orbital_interiors_replayed': 20,
              'archive_replay_relative_errors': replay_errors, 'reference_precision_relative_errors': reference_precision,
              'maximum_body_excess_precision_difference': max(row['complex_excess_relative_difference'] for row in reduction['precision_controls']),
              'widest_unfitted_first_PN_prediction_relative_error': far[-1]['relative_error_first_PN'],
              'circular_resonance': controls['circular_resonance'],
              'scope': 'First-order circular test-companion polar quadrupole waves; comparison changes central object, not gravity law. Finite-grid controls are not a continuum or complete inspiral error certificate.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'symbolic_checks': 21, 'interiors': 25,
                      'replay_maximum': max(replay_errors), 'reference_precision': reference_precision,
                      'body_excess_precision': report['maximum_body_excess_precision_difference'],
                      'PN_prediction': far[-1]['relative_error_first_PN']}))


if __name__ == '__main__':
    main()

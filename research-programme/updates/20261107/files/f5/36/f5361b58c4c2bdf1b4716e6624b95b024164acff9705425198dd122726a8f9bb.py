from __future__ import annotations

from datetime import datetime, timezone
import math

import numpy as np

from polar_radiation import ROOT, BRANCH, digest, read_json, write_json, modest_process
from analyze_waves import losses, power_for


def main():
    modest_process()
    directory = ROOT/'results/validation'
    directory.mkdir(parents=True, exist_ok=False)
    checks, inputs = [], {}

    def check(name, passed, value=None, tolerance=None):
        checks.append({'name': name, 'passed': bool(passed), 'value': value, 'tolerance': tolerance})

    def below(name, value, tolerance):
        check(name, math.isfinite(value) and value <= tolerance, float(value), tolerance)

    analysis_path = ROOT/'results/analysis/status.json'
    analysis = read_json(analysis_path)
    inputs[str(analysis_path)] = digest(analysis_path)
    check('analysis complete and current', analysis['state'] == 'complete' and analysis['script_sha256'] == digest(ROOT/'analyze_waves.py'))
    for path, expected in analysis['input_hashes'].items():
        check('analysis input '+path, digest(path) == expected)
    labels = ['pilot', 'fine-e03', 'fine-e06', 'resolved-coarse-e03', 'resolved-coarse-e06',
              'fine-tail03', 'fine-tail06', 'resolved-coarse-tail03', 'resolved-coarse-tail06',
              'quadrature-e03', 'quadrature-e06', 'quadrature-pole03', 'quadrature-pole06']
    groups = {}
    mode_count = 0
    for label in labels:
        path = ROOT/'results'/label/'status.json'
        groups[label] = report = read_json(path)
        inputs[str(path)] = digest(path)
        check(label+' complete', report['state'] == 'complete')
        check(label+' runner current', report['script_sha256'] == digest(ROOT/'polar_radiation.py'))
        for source, expected in report['input_hashes'].items():
            check(label+' imported source '+source, digest(source) == expected)
        modes = report['rows']
        mode_count += len(modes)
        check(label+' unique independent reality pairs', len({(row['eccentricity'], row['azimuth'], row['harmonic']) for row in modes}) == len(modes))
        maximum = report['arguments']['maximum']
        expected_count = 10 if label == 'pilot' else 3*maximum+1 if report['arguments']['plan'] == 'spectrum' else 3*(maximum-report['arguments']['minimum']+1)
        check(label+' all requested solves present', len(modes) == expected_count)
        for row in modes:
            prefix = f'{label}:e{row["eccentricity"]}:m{row["azimuth"]}:n{row["harmonic"]}:'
            archive_path = path.parent/row['archive']
            check(prefix+'archive exists', archive_path.is_file())
            with np.load(archive_path, allow_pickle=False) as archive:
                check(prefix+'finite saved coupled solution', all(np.isfinite(archive[key]).all() for key in archive.files))
                below(prefix+'archived solved frequency', abs(float(archive['frequency'])-abs(row['frequency'])), 1e-15)
            below(prefix+'nonabsorbing body verified', row['body_slope_imaginary_error'], 1e-12)
            below(prefix+'coupled collocation residual', row['interior_maximum_residual'], 1.001*report['settings']['interior_tolerance'])
            below(prefix+'boundary residual', row['interior_boundary_residual'], 1e-8)
            for key, tolerance in [('Wronskian_error', 1e-7), ('BH_reconstruction_relative_error', 1e-8),
                    ('optical_error_over_component_sum', 1e-11), ('metric_reciprocity_error_over_absolute_scale', 1e-8),
                    ('full_vs_half_error_over_absolute_scale', 1e-8), ('direct_body_amplitude_error_over_source_scale', 1e-7)]:
                below(prefix+key, row[key], tolerance)
            below(prefix+'outgoing unit current', row['outgoing_diagnostic']['infinity_flux_normalization_error'], 1e-11)
            below(prefix+'horizon unit current', row['horizon_diagnostic']['horizon_flux_normalization_error'], 1e-11)
            check(prefix+'same boundary null control', row['BH_boundary_control'] == 0)
            check(prefix+'nonnegative outgoing powers', row['BH_infinity_energy'] >= 0 and row['BH_horizon_energy'] >= 0 and row['body_infinity_energy'] >= 0)
            check(prefix+'m0 angular zero', row['azimuth'] != 0 or all(row[channel+'_angular'] == 0 for channel in ['BH_infinity', 'BH_horizon', 'body_infinity', 'difference_total']))
        for zero in report['static_rows']:
            check(label+' static flux excluded '+str(zero['eccentricity']), zero['energy_flux'] == 0 and zero['angular_flux'] == 0)
            below(label+' static metric reciprocity', zero['metric_reciprocity_error_over_absolute_scale'], 1e-8)
    for key, value in analysis['circular_regression'].items():
        below('circular regression '+key, value, 1e-8)
    pilot = groups['pilot']['rows']
    carrier = pilot[0]['body_infinity_energy']
    for row in pilot[1:3]:
        below('circular noncarrier power '+str(row['azimuth']), row['body_infinity_energy']/carrier, 1e-22)
    below('static circular action', analysis['static_controls'][0]['circular_static_regression'], 1e-10)
    for row in analysis['refinement']:
        below('radial/source refinement '+str((row['eccentricity'], row['channel'], row['quantity'])), row['difference_over_absolute_sum'], 1e-6)
    for row in analysis['secular']:
        prefix = str((row['eccentricity'], row['component'], row['channel']))
        below(prefix+' action first law', row['first_law_relative_error'], 1e-10)
        below(prefix+' independent p inverse', abs(row['semilatus_rate_per_mu']-row['direct_energy_angular_semilatus_rate'])/max(abs(row['semilatus_rate_per_mu']), 1e-300), 1e-9)
        if row['eccentricity']:
            below(prefix+' independent z inverse', abs(row['squared_eccentricity_rate_per_mu']-row['direct_energy_angular_squared_rate'])/max(abs(row['squared_eccentricity_rate_per_mu']), 1e-300), 1e-9)
        else:
            check(prefix+' exactly circular stays circular', row['squared_eccentricity_rate_per_mu'] == 0.)
        if row['channel'] == 'difference':
            for quantity in ['radial', 'angular']:
                rate_key = 'radial_action_rate_per_mu' if quantity == 'radial' else 'angular_rate_per_mu'
                below(prefix+' optical '+quantity, abs(row[rate_key]-row['optical_'+quantity+'_difference'])/max(abs(row[rate_key]), 1e-300), 1e-10)
    for row in analysis['Newtonian_baselines']:
        for key in ['power_closed_form_relative_error', 'angular_closed_form_relative_error', 'average_constant_error']:
            below('independent Newtonian tensor '+str(row['eccentricity'])+key, row[key], 1e-11)
        for quantity in ['energy', 'angular']:
            below('weak-field magnitude only '+str(row['eccentricity'])+quantity, abs(row['BH_'+quantity+'_over_Newtonian']-1), .1)
    quadrature = []
    for suffix in ['03', '06']:
        reference = groups['fine-e'+suffix]['rows']+groups['fine-tail'+suffix]['rows']
        lookup = {(row['azimuth'], row['harmonic']): row for row in reference}
        for part in ['e', 'pole']:
            label = 'quadrature-'+part+suffix
            refined = groups[label]['rows']
            original = [lookup[(row['azimuth'], row['harmonic'])] for row in refined]
            for channel in ['BH', 'body', 'difference']:
                original_loss, refined_loss = losses(original, channel), losses(refined, channel)
                for quantity, weight in [('energy', lambda row: 1.), ('angular', lambda row: row['azimuth']/row['frequency']),
                                          ('radial', lambda row: row['harmonic']/row['frequency'])]:
                    scale = math.fsum(abs(weight(row)*power_for(row, channel)) for row in reference)
                    value = abs(refined_loss[quantity]-original_loss[quantity])/max(scale, 1e-300)
                    quadrature.append({'label': label, 'channel': channel, 'quantity': quantity,
                                       'difference_over_full_absolute_sum': value})
                    below(label+' '+channel+' '+quantity+' independent quadrature', value, 1e-7)
    symbolic_path = ROOT/'results/derivation/status.json'
    symbolic = read_json(symbolic_path)
    inputs[str(symbolic_path)] = digest(symbolic_path)
    check('five exact identities', len(symbolic['checks']) == 5 and all(row['passed'] for row in symbolic['checks']) and symbolic['script_sha256'] == digest(ROOT/'derive_work.py'))
    prior = read_json(BRANCH/'eccentric-polar-source-20261005/results/validation/status.json')
    for primary in prior['primary_pdfs']:
        check('primary PDF '+primary['path'], digest(primary['path']) == primary['sha256'])
    source_urls = prior['source_urls']+['https://journals.aps.org/pr/abstract/10.1103/PhysRev.131.435',
                  'https://journals.aps.org/pr/abstract/10.1103/PhysRev.136.B1224']
    diagnostics = []
    for label in ['coarse-e03', 'coarse-e06', 'coarse-tail03', 'coarse-tail06']:
        path = ROOT/'results'/label/'status.json'
        diagnostic = read_json(path)
        inputs[str(path)] = digest(path)
        check(label+' diagnostic execution complete', diagnostic['state'] == 'complete')
        check(label+' diagnostic runner unchanged', diagnostic['script_sha256'] == digest(ROOT/'polar_radiation.py'))
        diagnostics.append({'label': label, 'mode_count': len(diagnostic['rows']), 'accepted_for_radial_refinement': False,
             'maximum_metric_source_error': max(row['metric_reciprocity_error_over_absolute_scale'] for row in diagnostic['rows']),
             'modes_exceeding_source_control_1e8': sum(row['metric_reciprocity_error_over_absolute_scale'] > 1e-8 for row in diagnostic['rows'])})
    check('underresolved source control is detected, not promoted', any(row['modes_exceeding_source_control_1e8'] for row in diagnostics))
    failed = [row for row in checks if not row['passed']]
    result = {'state': 'failed' if failed else 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'input_hashes': inputs, 'checks': checks,
              'wave_mode_evaluations': mode_count, 'static_solves': sum(len(group['static_rows']) for group in groups.values()),
              'exact_checks': len(symbolic['checks']), 'quadrature_controls': quadrature, 'excluded_source_grid_diagnostics': diagnostics,
              'primary_pdfs': prior['primary_pdfs'], 'source_urls': source_urls,
              'maximum_component_refinement': max(row['difference_over_absolute_sum'] for row in analysis['refinement']),
              'maximum_quadrature_refinement': max(row['difference_over_full_absolute_sum'] for row in quadrature)}
    write_json(directory/'status.json', result, exclusive=True)
    print({'checks': len(checks), 'failed': failed[:20], 'wave_mode_evaluations': mode_count,
           'maximum_component_refinement': result['maximum_component_refinement'],
           'maximum_quadrature_refinement': result['maximum_quadrature_refinement']})
    assert not failed, f'{len(failed)} checks failed'


if __name__ == '__main__':
    main()

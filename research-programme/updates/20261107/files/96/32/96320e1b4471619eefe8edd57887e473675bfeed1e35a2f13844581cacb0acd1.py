from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime
from time import perf_counter
import contextlib
import csv
import hashlib
import json
import numpy as np


LEVELS = {
    'parent': {
        'reference-reference': ('annular-resampled-parent-current-attempt01', 'reference-reference'),
        'MTS-primary': ('annular-resampled-parent-current-attempt01', 'MTS-primary')},
    'fine': {
        'reference-reference': ('annular-reference-matched-current-attempt01', 'resampled'),
        'MTS-primary': ('annular-MTS-primary-matched-current-attempt01', 'resampled')},
    'third': {
        'reference-reference': ('annular-reference-third-current-attempt02', 'reference-reference'),
        'MTS-primary': ('annular-MTS-primary-third-current-attempt02', 'MTS-primary')}}
VALIDATIONS = [
    'annular-resampled-parent-current-validation-attempt01',
    'annular-reference-matched-current-validation-attempt01',
    'annular-MTS-primary-matched-current-validation-attempt02',
    'annular-reference-third-current-validation-attempt02',
    'annular-MTS-primary-third-current-validation-attempt02']
COMPONENTS = [
    'cell_source', 'face_source', 'endpoint_source', 'dust_euler', 'gram_space',
    'current_interpolation', 'current_endpoint', 'current_gram_bond',
    'current_gram_geometry', 'current_gram_advection', 'transport_smooth_cell',
    'transport_trace_lift', 'transport_material_cell', 'transport_material_face',
    'transport_gram_work', 'transport_negative_boundary', 'transport_full_Euler_work',
    'transport_mode_reaction', 'transport_material_quadrature', 'transport_weak_assembly_defect']
GROUPS = {'source_and_space': slice(0, 5), 'current_correction_rate': slice(5, 10),
          'transport_rate': slice(10, 20)}


def main():
    evidence = EvidenceRun('annular-primary-reference-third-component-comparison-attempt01', __file__)
    started = perf_counter()
    try:
        folders = list(dict.fromkeys([entry[0] for level in LEVELS.values() for entry in level.values()]
                                    + VALIDATIONS))
        authorities, digests = {}, {}
        for folder in folders:
            path = evidence.output.parent / folder / 'status.json'
            data = json.loads(path.read_text(encoding='utf-8'))
            evidence.check(folder + ':complete', data['state'] == 'complete'
                           and bool(data['checks']) and all(row['passed'] for row in data['checks']))
            evidence.own(path)
            authorities[folder] = data
            for table in ['inputs', 'outputs']:
                for relative, digest in data[table].items():
                    if relative in digests and digests[relative] != digest:
                        raise RuntimeError('Conflicting source digest: ' + relative)
                    digests[relative] = digest
        for relative, digest in digests.items():
            path = evidence.root / relative
            evidence.check('source_hash:' + relative,
                           path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest)
            evidence.own(path)
        for branch, (folder, unused) in LEVELS['third'].items():
            validation_folder = folder.replace('current-attempt', 'current-validation-attempt')
            data, validation = authorities[folder], authorities[validation_folder]
            for name, status in [('run', data), ('validation', validation)]:
                evidence.check(branch + ':' + name + ':all_seven_states',
                               status['full_radial_comparison_completed'] and not status['pending_cases']
                               and len(status['cases']) == 7)
            evidence.check(branch + ':matching_validation', validation['source_run'] == folder)
            evidence.check(branch + ':three_comparisons',
                           len(data['comparison']) == len(validation['comparison']) == 3)
            for row, replay in zip(data['comparison'], validation['comparison']):
                evidence.check(branch + ':validated_comparison:' + str(row['test']),
                               row['branch'] == replay['branch'] and row['test'] == replay['test']
                               and all(abs(row[level] - replay[level]) <= 2e-14 for level in LEVELS))
        arrays, component_rows, group_rows, difference_rows, level_rows = {}, [], [], [], []
        for level, entries in LEVELS.items():
            arrays[level] = {}
            for branch, (folder, route) in entries.items():
                selected = [row for row in authorities[folder]['summaries'] if row['route'] == route]
                evidence.check(level + ':' + branch + ':unique_summary', len(selected) == 1)
                summary = selected[0]
                path = evidence.root / summary['component_path']
                relative = str(path.relative_to(evidence.root))
                evidence.check(level + ':' + branch + ':owned_component_archive', relative in digests)
                with np.load(path, allow_pickle=False) as archive:
                    names = archive['component_names'].tolist()
                    components, radial = archive['components'].copy(), archive['radial'].copy()
                evidence.check(level + ':' + branch + ':component_basis', names == COMPONENTS)
                evidence.check(level + ':' + branch + ':finite_shapes',
                               components.shape == (2, 20, 3) and radial.shape == (2, 2, 3)
                               and np.isfinite(components).all() and np.isfinite(radial).all())
                final = radial[1, -1]
                third_folder = LEVELS['third'][branch][0]
                comparison = authorities[third_folder]['comparison']
                evidence.check(level + ':' + branch + ':signed_summary',
                               np.allclose(final, summary['signed_radial'], atol=2e-24, rtol=0)
                               and np.allclose(final, [row[level] for row in comparison], atol=2e-24, rtol=0))
                arrays[level][branch] = (components, radial)
                for test in range(3):
                    level_rows.append(dict(branch=branch, level=level, test=test, direct=final[test],
                        component_sum=components[-1, :, test].sum(),
                        direct_minus_component_sum=final[test] - components[-1, :, test].sum(),
                        outer_change=abs(radial[1, 1, test] - radial[1, 0, test]),
                        quadrature_change=abs(radial[1, 1, test] - radial[0, 1, test]),
                        direct_minus_source_decomposition=comparison[test][level + '_decomposition_gap']))
            reference, reference_radial = arrays[level]['reference-reference']
            primary, primary_radial = arrays[level]['MTS-primary']
            difference = primary - reference
            direct_difference = primary_radial - reference_radial
            for index, component in enumerate(COMPONENTS):
                for test in range(3):
                    component_rows.append(dict(level=level, test=test, component=component,
                        reference=reference[-1, index, test], primary=primary[-1, index, test],
                        primary_minus_reference=difference[-1, index, test],
                        difference_outer_change=abs(difference[1, index, test] - difference[0, index, test])))
            for group, selection in GROUPS.items():
                for test in range(3):
                    group_rows.append(dict(level=level, test=test, group=group,
                        reference=reference[-1, selection, test].sum(), primary=primary[-1, selection, test].sum(),
                        primary_minus_reference=difference[-1, selection, test].sum()))
            for test in range(3):
                total = difference[-1, :, test].sum()
                grouped = sum(row['primary_minus_reference'] for row in group_rows
                              if row['level'] == level and row['test'] == test)
                evidence.check(level + ':groups_exhaust_components:' + str(test), abs(total - grouped) < 1e-24)
                difference_rows.append(dict(level=level, test=test,
                    primary_minus_reference=direct_difference[1, -1, test], component_difference_sum=total,
                    direct_minus_component_difference=direct_difference[1, -1, test] - total,
                    difference_outer_change=abs(direct_difference[1, 1, test] - direct_difference[1, 0, test]),
                    difference_quadrature_change=abs(direct_difference[1, 1, test] - direct_difference[0, 1, test])))
        exports = [('component-differences.csv', component_rows, 180), ('group-differences.csv', group_rows, 27),
                   ('current-differences.csv', difference_rows, 9), ('signed-levels.csv', level_rows, 18)]
        for filename, rows, expected in exports:
            path = evidence.output / filename
            with path.open('w', newline='', encoding='utf-8') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path, 'outputs')
            with path.open(newline='', encoding='utf-8') as stream:
                parsed = list(csv.DictReader(stream))
            evidence.check(filename + ':roundtrip', len(parsed) == expected
                           and all(None not in row and None not in row.values() for row in parsed))
        threshold = datetime.fromisoformat('2026-09-27T18:09:26+00:00').timestamp()
        changed = [str(path) for path in (evidence.root.parent / 'formalization-workbench').rglob('*')
                   if path.is_file() and path.stat().st_mtime >= threshold]
        evidence.check('protected_workbench_unchanged', not changed, changed)
        evidence.check('no_scripts_bytecode_cache', not (evidence.root / 'scripts/__pycache__').exists())
        third = authorities[LEVELS['third']['MTS-primary'][0]]
        ratios = [row['fine_to_third_absolute_ratio'] for row in third['comparison']]
        evidence.report.update(seconds=perf_counter() - started, difference_rows=difference_rows,
            primary_fine_to_third_absolute_ratios=ratios,
            primary_all_three_shrink=all(value < 1 for value in ratios),
            no_numerical_solve_performed=True, asymptotic_order_established=False,
            historical_scientific_flags={folder: dict(passed=authorities[folder]['science_passed'],
                total=authorities[folder]['science_total']) for folder in VALIDATIONS},
            protected_workbench_changed_count=len(changed), github_action=False, subagents_used=False,
            scope='Read-only attribution of three-grid MTS-primary minus reference radial-current residuals; '
                  'not a new field equation or observational comparison.')
        with (evidence.output / 'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output / 'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=evidence.report['seconds'],
                              primary_fine_to_third_absolute_ratios=ratios, difference_rows=difference_rows)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

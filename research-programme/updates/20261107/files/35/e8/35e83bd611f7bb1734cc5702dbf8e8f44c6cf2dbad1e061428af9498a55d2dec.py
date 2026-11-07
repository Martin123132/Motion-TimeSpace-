from common import *
from stress_math import SPECIES, GROUPS
from scipy.interpolate import make_interp_spline
import numpy as np
import csv
import math
import ast


def main():
    modest()
    check_parent()
    checks, evidence, rows, reports = [], {}, [], []
    def check(name, condition, value=None):
        checks.append(dict(name=name, passed=bool(condition), value=value))
        require(condition, name)
    def source(path):
        evidence[str(path)] = digest(path)
    for path in STAGE.glob('*.py'):
        ast.parse(path.read_text())
        check('parse ' + path.name, True)
        source(path)
    for family in ('half', 'balanced', 'double'):
        directory = STAGE / family
        manifest = read(directory / 'inputs.json')
        for path, expected in manifest['sources'].items():
            check('frozen ' + family + ' ' + Path(path).name, digest(path) == expected)
            source(path)
        combined = read(directory / 'result.json')
        check('complete family ' + family, combined['passed'])
        source(directory / 'result.json')
        source(directory / 'inputs.json')
        for report in combined['reports']:
            guard()
            model = report['model']
            tag = family + '/' + model
            check(tag + ' input hash', digest(report['original_input']) == report['original_sha256'])
            check(tag + ' output hash', digest(report['output']) == report['output_sha256'])
            source(report['original_input'])
            source(report['output'])
            for name in ('qualification', 'result'):
                source(directory / (model + '-' + name + '.json'))
            packet = load(report['output'])
            reference = load(report['original_input'])
            context_path = directory / 'contexts' / (model + '-' + family) / 'initial-context.npz'
            context = load(context_path)
            source(context_path)
            alpha_slot = int(np.flatnonzero(context['core'] == np.flatnonzero(context['mapping'] == 1)[0])[0])
            alpha = reference['evolved_state'][:, alpha_slot]
            hubble, grid, wave = reference['H'], reference['efold'], float(reference['wave'])
            values = {name: reference['values'][:, index] for index, name in enumerate(reference['value_names'])}
            terms = reference['terms']
            current = terms[:, :, 1] + wave * alpha[:, None] * terms[:, :, 5]
            shear = terms[:, :, 6]
            check(tag + ' exact grid', np.array_equal(grid, packet['efold']))
            check(tag + ' finite packet', all(np.isfinite(value).all() for value in packet.values()))
            for name, expected in (('current', current), ('shear', shear), ('density', terms[:, :, 0] - 3 * (hubble * alpha)[:, None] * terms[:, :, 5])):
                error = float(np.max(abs(expected - packet[name])) / max(np.max(abs(expected)), 1e-80))
                check(tag + ' independent ' + name, error < ALGEBRA, error)
            check(tag + ' scalar zero', np.count_nonzero(shear[:, [5, 6]]) == 0)
            cdm = float(np.max(abs(values['delta_c'])))
            check(tag + ' original normalization', cdm == report['cdm_envelope'] == float(packet['cdm_envelope']))
            csv_path = directory / (model + '-species.csv')
            source(csv_path)
            with csv_path.open(newline='', encoding='utf-8') as stream:
                species_rows = list(csv.DictReader(stream))
            check(tag + ' species order', [row['species'] for row in species_rows] == list(SPECIES))
            for index, row in enumerate(species_rows):
                for name, array in (('Q', current), ('Pi', shear)):
                    metrics = dict(raw_sup=float(np.max(abs(array[:, index]))),
                                   raw_rms_N=float(np.sqrt(np.trapezoid(array[:, index]**2, grid) / (grid[-1] - grid[0]))),
                                   normalized_sup=float(np.max(abs(array[:, index] / (hubble**2 * cdm)))),
                                   raw_final=float(array[-1, index]))
                    for suffix, expected in metrics.items():
                        check(tag + ' csv ' + row['species'] + ' ' + name + suffix, abs(float(row[name + '_' + suffix]) - expected) <= ALGEBRA * max(abs(expected), 1e-80))
                rows.append(row)
            norms, upper = packet['norms'], packet['energy_upper']
            replay = norms[0].copy()
            max_replay = 0.
            for index, width in enumerate(np.diff(grid)):
                decay = math.exp(-float(width) / 2)
                increment = -math.expm1(-float(width) / 2)
                for half in range(2):
                    replay = decay * replay + increment * packet['forcing'][index]
                max_replay = max(max_replay, float(np.max(abs(replay - upper[index + 1])) / max(np.max(abs(upper[index + 1])), 1e-80)))
            check(tag + ' independent two-half comparison', max_replay < ALGEBRA, max_replay)
            check(tag + ' energy containment', np.max(norms - upper) <= GATE * max(np.max(upper), 1e-80))
            direct = packet['factors'] * norms + packet['endpoints']
            restored = packet['factors'] * upper + packet['endpoints']
            check(tag + ' projection', np.max(abs(shear[:, [2, 3, 4]]) - direct) <= ALGEBRA * max(np.max(direct), 1e-80))
            check(tag + ' bound restoration', np.max(abs(restored - packet['shear_upper'])) <= ALGEBRA * max(np.max(restored), 1e-80))
            check(tag + ' shear containment', np.max(abs(shear[:, [2, 3, 4]]) - restored) <= GATE * max(np.max(restored), 1e-80))
            source_curve = make_interp_spline(grid, packet['source'], k=5, axis=0)
            max_force_excess = 0.
            for first in range(0, len(grid) - 1, 256):
                guard()
                last = min(first + 256, len(grid) - 1)
                locations = grid[first:last, None] + (grid[first + 1:last + 1] - grid[first:last])[:, None] * np.linspace(0, 1, 11)
                sampled = np.linalg.norm(source_curve(locations), axis=-1).max(axis=1)
                max_force_excess = max(max_force_excess, float(np.max(sampled - packet['forcing'][first:last])))
            check(tag + ' force control sample', max_force_excess <= ALGEBRA * max(np.max(packet['forcing']), 1e-80), max_force_excess)
            density_b = terms[:, 1, 5]
            density_gamma, density_r = packet['radiative_density'].T
            defect = 4 / 3 * np.sum(packet['massive'], axis=1) - terms[:, 4, 5]
            current_bounds = (np.sqrt(density_b + 4 * density_gamma / 3) * norms[:, 0],
                              np.sqrt(4 * density_r / 3) * norms[:, 1],
                              np.sqrt(4 / 3 * np.sum(packet['massive'], axis=1)) * norms[:, 2] + wave * abs(defect * alpha))
            for name, actual, bound in zip(GROUPS, (abs(current[:, 1] + current[:, 2]), abs(current[:, 3]), abs(current[:, 4])), current_bounds):
                excess = float(np.max(np.maximum(actual - bound, 0)) / max(np.max(bound), 1e-80))
                check(tag + ' current projection ' + name, excess < ALGEBRA, excess)
            qualification = read(directory / (model + '-qualification.json'))
            check(tag + ' 104 native tests', len(qualification['samples']) == 104)
            for sample in qualification['samples']:
                for name in ('photon_equation', 'massless_equation', 'massive_equation'):
                    check(tag + ' native ' + str(sample['index']) + ' ' + str(sample['perturbed']) + ' ' + name, sample[name] < GATE, sample[name])
            reports.append(dict(family=family, **report))
            del packet, reference, context, source_curve
    with (ROOT / 'species.csv').open('x', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    comparisons = []
    for family in ('half', 'balanced', 'double'):
        heavy = next(report for report in reports if report['family'] == family and report['model'] == 'heavy')
        cold = next(report for report in reports if report['family'] == family and report['model'] == 'cold')
        comparisons.append(dict(family=family, raw_shear_sup_ratio=heavy['total_shear_raw_sup'] / cold['total_shear_raw_sup'],
                                normalized_shear_sup_ratio=heavy['total_shear_normalized_sup'] / cold['total_shear_normalized_sup'],
                                cdm_reference_ratio=heavy['cdm_envelope'] / cold['cdm_envelope']))
    check_parent()
    write(ROOT / 'summary.json', dict(passed=True, reports=reports, comparisons=comparisons, evidence_hashes=evidence,
                                     native_states=sum(report['qualification_count'] for report in reports),
                                     saved_epochs=sum(report['original_nodes'] for report in reports), new_physical_ode_solves=0))
    write(ROOT / 'validation.json', dict(passed=True, count=len(checks), checks=checks))
    print('all', len(checks), 'checks passed', flush=True)
    print(json.dumps(comparisons, indent=2), flush=True)


if __name__ == '__main__':
    main()

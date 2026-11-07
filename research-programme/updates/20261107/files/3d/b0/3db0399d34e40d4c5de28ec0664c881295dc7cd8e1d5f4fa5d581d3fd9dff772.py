from derive_annular_source_gravity_20260914 import EvidenceRun
from decimal import Decimal, localcontext
from time import perf_counter
import contextlib
import csv
import hashlib
import json
import numpy as np


def archive(path):
    with np.load(path, allow_pickle=False) as saved:
        return {key: saved[key].copy() for key in saved.files}


def central_euler(raw):
    keys = ['measure', 'alpha', 'beta', 'alpha_r', 'beta_r', 'alpha_t', 'gradient', 'rate', 'rate_r',
            'acceleration', 'speed', 'speed_r', 'speed_rate', 'eta', 'eta_r', 'field', 'field_r']
    data = {key: np.array([Decimal.from_float(float(value)) for value in raw[key]], dtype=object) for key in keys}
    one, half, zero = Decimal(1), Decimal('.5'), Decimal(0)
    estimates = []
    for step in [Decimal('.0001'), Decimal('.00005'), Decimal('.000025')]:
        pairs = []
        for sign in [-1, 1]:
            amount = sign * step
            width = one + amount * data['eta_r']
            gradient = (data['gradient'] + amount * data['field_r']) / width
            alpha = data['alpha'] + amount * data['alpha_r'] * data['eta']
            beta = data['beta'] + amount * data['beta_r'] * data['eta']
            temporal = data['rate'] - data['speed'] * gradient
            action = sum(data['measure'] * width * (alpha * temporal**2 - beta * gradient**2) * half, zero)
            width = one + amount * data['speed_r']
            gradient = (data['gradient'] + amount * data['rate_r']) / width
            alpha = data['alpha'] + amount * (data['alpha_t'] + data['speed'] * data['alpha_r'])
            temporal = data['rate'] + amount * data['acceleration'] - (data['speed'] + amount * data['speed_rate']) * gradient
            momentum = sum(data['measure'] * width * alpha * temporal * (data['field'] - data['eta'] * gradient), zero)
            pairs.append((action, momentum))
        derivatives = [(pairs[1][index] - pairs[0][index]) / (2 * step) for index in range(2)]
        estimates.append(derivatives[1] - derivatives[0])
    coarse = (4 * estimates[1] - estimates[0]) / 3
    fine = (4 * estimates[2] - estimates[1]) / 3
    return estimates, coarse, fine


def main():
    evidence = EvidenceRun('annular-directional-coupled-Euler-validation-attempt01', __file__)
    started = perf_counter()
    try:
        parent_path = evidence.output.parent / 'annular-directional-coupled-Euler-attempt02/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        evidence.check('main_complete', parent['state'] == 'complete' and all(row['passed'] for row in parent['checks']))
        bad = []
        for table in ['inputs', 'outputs']:
            for relative, digest in parent[table].items():
                path = evidence.root / relative
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                    bad.append(relative)
                else:
                    evidence.own(path)
        evidence.check('all_main_inputs_and_outputs_rehashed', not bad, bad)
        rows = []
        with localcontext() as context:
            context.prec = 60
            for case in parent['cases']:
                name = case['branch'] + '-' + case['level']
                print(json.dumps(dict(stage=name, seconds=perf_counter() - started)), flush=True)
                for relative in case['material_paths']:
                    values = archive(evidence.root / relative)
                    channels = list(values['channels'])
                    table = dict(zip(channels, values['values'].T))
                    evidence.check(relative + ':finite', np.isfinite(values['values']).all())
                    evidence.check(relative + ':positive_measure', np.min(values['weights']) > 0 and abs(sum(values['weights']) - 1) < 2e-14)
                    evidence.check(relative + ':positive_kinetic_defect', np.min(table['kinetic_defect']) >= 0)
                    evidence.check(relative + ':recomputed_average', np.max(abs(values['weights'] @ values['values'] - values['average'])) <= 2e-20)
                    evidence.check(relative + ':direct_mesh_field_partition', np.max(abs(table['coupled_direct'] - table['solved_field_work'] - table['mesh_equation'])) <= 2e-16)
                    evidence.check(relative + ':independent_defect_sum', np.max(abs(table['coupled_direct'] - table['wave_label_defect'] - table['wave_spatial_defect'] - table['wave_faces'] - table['gram_field'] - table['gram_mesh'] - table['gram_coefficient'])) <= 2e-16)
                relative = case['probe_paths'][1]
                raw = archive(evidence.root / relative)
                estimates, coarse, fine = central_euler(raw)
                expected = Decimal.from_float(float(raw['values'][channels.index('wave_direct')]))
                error = abs(fine - expected)
                evidence.check(name + ':real_signed_action_and_momentum', error <= Decimal('2e-16'), dict(error=str(error), coarse_to_fine=str(abs(fine - coarse))))
                evidence.check(name + ':real_signed_derivative_converged', abs(fine - coarse) <= Decimal('2e-16'))
                rows.append(dict(branch=case['branch'], level=case['level'], material_label=float(raw['label']),
                    central_1=str(estimates[0]), central_2=str(estimates[1]), central_3=str(estimates[2]),
                    richardson_coarse=str(coarse), richardson_fine=str(fine), direct_analytic=str(expected), difference=str(fine - expected)))
        path = evidence.output / 'independent-real-derivatives.csv'
        with path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(path, 'outputs')
        for relative in parent['outputs']:
            if relative.endswith('.csv'):
                with (evidence.root / relative).open(newline='', encoding='utf-8') as stream:
                    parsed = list(csv.DictReader(stream))
                evidence.check(relative + ':rectangular_csv', bool(parsed) and all(None not in row and all(value is not None for value in row.values()) for row in parsed))
        evidence.report.update(seconds=perf_counter() - started, independent_real_derivative_cases=len(rows),
            numerical_precision=60, signed_time_jets_only=True, new_nonlinear_solves=0, github_action=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    with contextlib.redirect_stderr(__import__('sys').stdout):
        main()

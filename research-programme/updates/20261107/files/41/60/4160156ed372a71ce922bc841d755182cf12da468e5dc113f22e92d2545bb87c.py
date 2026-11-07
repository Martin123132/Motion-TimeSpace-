from common import *
from adjoint_operator import open_owned, relative, sup
from compact_adjoint import CompactAdjoint
from physical_energy_map import PhysicalEnergyMap
from forcing_math import explicit
from cold_math import adapt, pressure_and_current, comparison, symbolic, coefficients
import numpy as np


def algebra_cases():
    records = []
    for epsilon in (1e-12, 1e-8, 1e-4, .01, .05, .5):
        for speed in (0., 1e-15, 1e-10, 1e-6, .01, .2, .8, 1.):
            for eta in (-2., -1., 0., 1., 3.):
                width, width_rate, diagonal0, diagonal1, cross, logarithmic, upper = coefficients(epsilon, speed, eta)
                symmetric = np.array([[diagonal0, cross], [cross, diagonal1]], dtype=float)
                actual = float(np.linalg.eigvalsh(symmetric)[-1])
                values = dict(density_over_k=2 * epsilon / width,
                              free_density0_over_k=2 * (1 + speed**2) * epsilon / width,
                              free_density1_over_k=2 / np.sqrt(3),
                              psi_drive_over_k=2 / np.sqrt(3), phi_drive_over_H=2 * width,
                              current_over_H=2 / np.sqrt(3), shear_over_H=2 * speed / np.sqrt(5))
                passed = (abs(actual - logarithmic) < ALGEBRA and actual <= upper + ALGEBRA
                          and abs(cross) <= 1 / np.sqrt(3) + ALGEBRA
                          and values['density_over_k'] <= 1 + ALGEBRA
                          and values['free_density0_over_k'] <= 2 + ALGEBRA
                          and values['phi_drive_over_H'] <= 2 * np.sqrt(2) + ALGEBRA)
                require(passed and all(np.isfinite(value) for value in values.values()), 'cold coefficient limit')
                records.append(dict(epsilon=epsilon, speed=speed, eta=eta, width=float(width), weight_rate=float(width_rate),
                                    actual_log_norm=actual, formula=float(logarithmic), upper=float(upper), passed=bool(passed), **values))
    return dict(passed=True, scope='Dimensionless coefficient stress tests, NOT background solutions or new cosmological fits', rows=records)


def main():
    modest()
    check_parent()
    (ROOT / 'contexts').mkdir(exist_ok=False)
    write(ROOT / 'inputs.json', dict(sources=frozen_sources(), parent_seal=PARENT_SEAL, numerical=GATE, algebra=ALGEBRA))
    write(ROOT / 'symbolic.json', symbolic())
    write(ROOT / 'coefficient-limits.json', algebra_cases())
    reports = []
    for model in ('heavy', 'cold'):
        record = read(CHANNELS / LABEL / (model + '-channels.json'))['coefficient_input']
        require(digest(record['path']) == record['sha256'], 'unchanged coefficient packet')
        packet = load(record['path'])
        operator = CompactAdjoint(packet)
        system = open_owned(model, 'contexts')
        energy = PhysicalEnergyMap(system)
        errors, algebra, bounds, rows = {}, {}, [], []
        def check(name, value, exact=False):
            target = algebra if exact else errors
            target[name] = max(target.get(name, 0.), float(value))
        grid = packet['efold']
        for count, index in enumerate(np.unique(np.linspace(3, len(grid) - 5, 97, dtype=int))):
            guard()
            efold = float(grid[index] + .43 * (grid[index + 1] - grid[index]))
            adapted = adapt(system, energy, efold)
            physical = pressure_and_current(system, energy, efold, adapted)
            new, old = adapted['rows'], adapted['old']
            transform, inverse, derivative = new['transform'], new['inverse'], new['derivative']
            core, into_core, into_tail, speed, _, _ = operator.blocks(efold, 0)
            matrix = transform @ core @ inverse + derivative
            metric = np.outer(new['psi_injection'], new['psi']) + np.outer(new['phi_injection'], new['phi_rate'])
            free = matrix - metric
            check('coordinate_inverse', relative(transform @ inverse - np.eye(energy.size), np.eye(energy.size)), True)
            for values in adapted['direct_massive']:
                monopole, dipole, quad = values['slots']
                for name, slot, expected in (('density', monopole, values['density0']), ('density_rate', monopole, values['density0_rate']),
                                            ('free_density', monopole, values['free0']), ('free_density', dipole, values['free1']),
                                            ('current', dipole, values['current1']), ('shear', quad, values['shear2']),
                                            ('psi_injection', dipole, values['psi1']), ('phi_injection', monopole, values['phi0'])):
                    check('explicit_massive_' + name, abs(new[name][slot] - expected) / max(abs(expected), 1e-80), True)
            check('free_density', relative(new['density_rate'] + new['density'] @ free - new['free_density'], new['free_density']))
            check('free_current', relative(physical['current_rate'] + new['current'] @ free - physical['free_current'], physical['free_current']))
            for label, row, injection, expected in (
                    ('density_psi', new['density'], new['psi_injection'], 3 * old['defect']),
                    ('density_phi', new['density'], new['phi_injection'], 3 * old['quadrature']),
                    ('current_psi', new['current'], new['psi_injection'], (old['quadrature'] - old['defect']) * system.wave / old['hubble']),
                    ('current_phi', new['current'], new['phi_injection'], 0.)):
                check(label, abs(row @ injection - expected) / max(np.linalg.norm(row) * np.linalg.norm(injection), abs(expected), 1e-80), True)
            gr_matrix = free + np.outer(new['psi_injection'], physical['gr_psi']) + np.outer(new['phi_injection'], physical['gr_phi_rate'])
            pressure_matrix = np.zeros_like(matrix)
            pressure_matrix[energy.slot(4)] = physical['native_pressure']
            ufa_matrix = np.zeros_like(matrix)
            signatures = system.context['signature_values']
            comparison_rows = {}
            for branch, branch_matrix in (('poisson-spatial', matrix), ('gr', gr_matrix)):
                result = comparison(system, energy, adapted, physical, branch_matrix, branch)
                scale = max(1., np.linalg.norm(branch_matrix, ord='fro'))
                excess = float(np.max(result['actual'] - result['upper']) / scale)
                check(branch + '_comparison_excess', max(0., excess), True)
                if signatures[12]:
                    ufa_matrix[energy.slot(int(signatures[4]) + 2), system.alpha_slot] = result['ufa']
                comparison_rows[branch] = dict(actual=result['actual'].tolist(), upper=result['upper'].tolist(),
                                               maximum_row_sum=float(np.max(result['upper'].sum(axis=1))))
            base_rest = (free - pressure_matrix - ufa_matrix)[np.ix_(energy.rest, energy.rest)]
            actual_base = max(float(np.max(adapted['tail_rate'])), float(np.linalg.eigvalsh((base_rest + base_rest.T) / 2)[-1]))
            check('base_log_norm', max(0., actual_base - result['base']) / max(1., np.linalg.norm(base_rest)), True)
            for node in range(5):
                slots = [energy.moment_slot(degree, node) for degree in range(3)]
                epsilon, velocity, width = adapted['epsilon'], adapted['speeds'][node], adapted['width'][node]
                block = free[np.ix_(slots[:2], slots[:2])]
                expected = np.array([[adapted['diagonal0'][node], -width / (np.sqrt(3) * epsilon)],
                                     [velocity**2 / (np.sqrt(3) * epsilon * width), adapted['diagonal1'][node]]])
                check('cold_stream_block', relative(block - expected, expected))
            weights = np.diag(transform)[energy.quadrupoles]
            tail_weights = adapted['tail_weights']
            boundary = into_core * weights / tail_weights[0] + into_tail * tail_weights[0] / weights
            lower = operator.lower[1:, None] * speed * tail_weights[1:] / tail_weights[:-1]
            upper = operator.upper[:-1, None] * speed * tail_weights[:-1] / tail_weights[1:]
            check('tail_skew', max(sup(boundary), sup(lower + upper)) / max(sup(lower), sup(upper), 1e-80), True)
            for seed in range(3):
                vector = np.sin(np.arange(len(system.units)) * (.7 + seed) + count + .17)
                state = np.empty(len(vector))
                state[:energy.size] = (inverse @ vector[:energy.size]) * system.units[:energy.size]
                state[energy.size:] = (vector[energy.size:].reshape(190, 5) / tail_weights).reshape(-1) * system.units[energy.size:]
                for branch, branch_matrix, psi_row, phi_rate_row in (
                        ('poisson-spatial', matrix, new['psi'], new['phi_rate']),
                        ('gr', gr_matrix, physical['gr_psi'], physical['gr_phi_rate'])):
                    rate, values, rates, info, _, _ = system.evaluate(efold, state, branch)
                    calculated = transform @ (rate[:energy.size] / system.units[:energy.size]) + derivative @ vector[:energy.size]
                    expected = branch_matrix @ vector[:energy.size]
                    expected[energy.quadrupoles] += into_core * weights / tail_weights[0] * vector[energy.size:].reshape(190, 5)[0]
                    check(branch + '_native_generator', relative(calculated - expected, calculated))
                    for label, key, physical_row in (('density', 'D', new['density']), ('current', 'Q', new['current']),
                                                     ('shear', 'Pi', new['shear']), ('psi', 'Psi', psi_row)):
                        value = physical_row @ vector[:energy.size]
                        scale = max(np.linalg.norm(physical_row) * np.linalg.norm(vector[:energy.size]), abs(values[key]), 1e-80)
                        check(branch + '_native_' + label, abs(value - values[key]) / scale)
                    value = phi_rate_row @ vector[:energy.size]
                    check(branch + '_native_phi_rate', abs(value - rates['Phi'] / old['hubble']) / max(np.linalg.norm(phi_rate_row) * np.linalg.norm(vector[:energy.size]), abs(value), 1e-80))
                    if branch == 'gr':
                        check('gr_phi_constraint', abs(physical['gr_phi'] @ vector[:energy.size] - values['Phi']) / max(np.linalg.norm(physical['gr_phi']) * np.linalg.norm(vector[:energy.size]), 1e-80))
                tail_vector = vector[energy.size:].reshape(190, 5)
                actual_tail = tail_weights * (rate[energy.size:] / system.units[energy.size:]).reshape(190, 5) + adapted['tail_rate'] * tail_vector
                expected_tail = adapted['tail_rate'] * tail_vector
                expected_tail[1:] += lower * tail_vector[:-1]
                expected_tail[:-1] += upper * tail_vector[1:]
                expected_tail[0] += into_tail * tail_weights[0] / weights * vector[energy.quadrupoles]
                check('native_tail', relative(actual_tail - expected_tail, actual_tail))
            forcing = explicit(system, energy, efold)
            scaling, scaling_rate = adapted['scaling'], adapted['scaling_rate']
            primitive = scaling * forcing['primitive']
            primitive_rate = scaling * forcing['primitive_rate'] + scaling_rate * primitive
            current_force, shear_force = scaling * forcing['current'], scaling * forcing['shear']
            check('primitive_current_covariance', relative(shear_force + matrix @ primitive - primitive_rate - current_force, current_force))
            commutator = free @ new['phi_injection'] - (scaling * forcing['phi_rate'] + scaling_rate * new['phi_injection'])
            check('commutator_covariance', relative(commutator - scaling * forcing['commutator'], scaling * forcing['commutator']))
            rescaling = result['rescaling']
            dual_c = np.zeros(energy.size)
            dual_c[system.cdm_slot] = 1 / (np.sqrt(physical['density_weights'][0]) * old['hubble'] / system.wave)
            k_c = old['hubble']**2 / system.wave * np.linalg.norm(dual_c / rescaling)
            expected_k_c = old['hubble'] / np.sqrt(physical['density_weights'][0])
            check('cdm_dual_constant', abs(k_c - expected_k_c) / expected_k_c, True)
            row = dict(efold=efold, epsilon=adapted['epsilon'], minimum_speed=float(np.min(adapted['speeds'])),
                       maximum_kv_over_H=float(np.max(adapted['speeds']) / adapted['epsilon']),
                       massive_log_norm_max=float(np.max(adapted['massive_logarithmic'])), simple_massive_bound=adapted['simple_bound'],
                       actual_free_rest=actual_base, free_rest_upper=result['base'], pressure_norm=float(np.linalg.norm(physical['native_pressure'][energy.rest])),
                       comparisons=comparison_rows, current_row_over_H=float(np.linalg.norm(new['current'] / rescaling) / old['hubble']),
                       density_row_over_k=float(np.linalg.norm(new['density'] / rescaling) / system.wave),
                       shear_row_over_H=float(np.linalg.norm(new['shear'] / rescaling) / old['hubble']),
                       cdm_dual_K=k_c, density_dual_K=float(np.linalg.norm(new['density'] / rescaling) / system.wave),
                       balanced_current_force_over_k=float(np.linalg.norm(rescaling * current_force) / system.wave),
                       balanced_shear_force_over_k=float(np.linalg.norm(rescaling * shear_force) / system.wave),
                       balanced_primitive_over_H=float(np.linalg.norm(rescaling * primitive) / old['hubble']))
            rows.append(row)
            if count % 32 == 0:
                print(LABEL, model, 'cold/GR sample', count + 1, flush=True)
        passed = max(errors.values()) < GATE and max(algebra.values()) < ALGEBRA
        report = dict(model=model, passed=passed, errors=errors, algebra=algebra, rows=rows, coefficient_input=record,
                      new_physical_ode_solves=0, native_vectors=97 * 3 * 2, scope='Equation-derived inequalities; off-node qualification, not sampled continuum supremum certification')
        write(ROOT / (model + '-result.json'), report)
        print(LABEL, model, 'passed', passed, errors, algebra, flush=True)
        require(passed, 'preserve cold/GR qualification discrepancy')
        reports.append(report)
        del system, energy, packet, operator
    for path, expected in read(ROOT / 'inputs.json')['sources'].items():
        require(digest(path) == expected, 'frozen source')
    check_parent()
    write(ROOT / 'result.json', dict(passed=True, reports=reports))


if __name__ == '__main__':
    main()

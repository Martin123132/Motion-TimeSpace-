from common241 import *
import ports241 as original
import argparse
import types
from scipy import linalg
CANDIDATE = ROOT / 'precision'
EPSILON = np.finfo(float).eps


def setup_repair():
    config = protocol()
    frozen = read(ROOT / 'precision-configuration.json')
    for name, expected in frozen['code'].items():
        assert digest(ROOT / name) == expected, name
    for path, expected in frozen['inputs'].items():
        assert digest(path) == expected, path
    return config


def product_pair(values, factor):
    upper, lower = precise.split(values)
    factor_upper, factor_lower = precise.split(np.asarray(factor))
    product = values * factor
    residual = ((upper * factor_upper - product) + upper * factor_lower + lower * factor_upper) + lower * factor_lower
    return product, residual


def solve_pair(matrix, degree, basis, context):
    mass = np.triu(basis['mass']) + np.triu(basis['mass'], 1).T
    delta = mass - np.eye(len(mass))
    norm = np.linalg.norm(delta, ord=np.inf)
    assert norm < 1e-12
    weak = matrix[1:-1]
    first = delta @ weak
    correction = -first + delta @ first
    with mp.workdps(80):
        exact_factor = (2 * degree + 1) * scalar(context['opacity'])
        factor_high = float(exact_factor)
        factor_low = float(exact_factor - scalar(factor_high))
    high, residual = product_pair(weak, factor_high)
    low = residual + weak * factor_low + correction * factor_high + correction * factor_low
    gamma = len(mass) * EPSILON / (1 - len(mass) * EPSILON)
    error_bound = norm**3 / (1 - norm) + 4 * gamma * norm + 4 * gamma * norm**2 + 64 * EPSILON**2
    return high, low, dict(delta_norm=float(norm), exact_neumann_remainder=float(norm**3 / (1 - norm)),
        relative_infinity_solver_bound=float(error_bound))


def physical_port(matrix, degree, basis, moment, context):
    high, low, estimate = solve_pair(matrix, degree, basis, context)
    local = context['local']
    direct = context['opacity'] * matrix[0]
    gas = context['opacity'] * matrix[-1]
    divisor = local['chi'] * local['C'] if degree == 0 else local['B'] if degree == 1 else 1.
    upper, ordinary_upper, defect_upper = moment.contract(high, degree)
    lower, ordinary_lower, defect_lower = moment.contract(low, degree)
    port = dict(photon=high, photon_low=low, photon_moment=upper + lower, direct_moment=direct,
        gas_moment=gas, gas_rate=gas / divisor, angular_mass_factor=2 * degree + 1,
        ordinary_photon_moment=ordinary_upper + ordinary_lower, readout_defect=defect_upper + defect_lower)
    port.update(coupling.metric_response(port, degree, context['reference'], context['scale'], local['C']))
    port['metric_T_cubic'] = port['sigma_transverse_second'] / 3
    port['metric_L_cubic'] = port['sigma_longitudinal_second'] / 3
    return port


def verify_port(label, port, matrix, degree, context, native_rows, checks):
    direct, gas = port['direct_moment'], port['gas_moment']
    transfer_scale = max(np.linalg.norm(direct) + np.linalg.norm(gas), 1e-300)
    check(checks, label + ':same-mass direct photon moment', original.scaled_error(port['photon_moment'], direct))
    if degree < 2:
        check(checks, label + ':independent gas exchange', np.linalg.norm(port['photon_moment'] + gas) / transfer_scale)
        divisor = context['local']['chi'] * context['local']['C'] if degree == 0 else context['local']['B']
        check(checks, label + ':gas primitive to stress', original.scaled_error(port['gas_rate'] * divisor, gas))
        check(checks, label + ':omitted gas rejected', int(np.linalg.norm(port['photon_moment']) / transfer_scale <= 1e-7), 0)
        if degree == 1:
            check(checks, label + ':omitted dipole inverse mass rejected', int(np.linalg.norm(port['photon_moment'] / 3 + gas) / transfer_scale <= 1e-7), 0)
    source_high = np.vstack([port['photon'], port['gas_rate'] if degree < 2 else np.zeros(matrix.shape[1])])
    source_low = np.vstack([port['photon_low'], np.zeros(matrix.shape[1])])
    high, low = native_rows
    rates = context['reference'] * (precise.stable_dot(source_high.T, high, low) + precise.stable_dot(source_low.T, high, low)).T
    stress_scale = context['reference'] * transfer_scale
    for index, name in enumerate(('energy', 'current', 'stress_transverse', 'stress_longitudinal')):
        check(checks, label + ':native stress rate:' + name, original.scaled_error(rates[index], port[name], stress_scale))
    native_T = context['scale']**2 * (rates[0] - rates[3]) / 6
    native_L = context['scale']**2 * (rates[0] + rates[3] - 2 * rates[2]) / 6
    metric_scale = context['scale']**2 * stress_scale
    check(checks, label + ':native transverse cubic metric coefficient', original.scaled_error(native_T, port['metric_T_cubic'], metric_scale))
    check(checks, label + ':native longitudinal cubic metric coefficient', original.scaled_error(native_L, port['metric_L_cubic'], metric_scale))
    native_constraint = np.vstack([-2 * context['scale']**2 * rates[0], -context['scale']**2 * rates[1]])
    check(checks, label + ':native constraint-rate forcing', original.scaled_error(native_constraint, port['constraint_forcing'], metric_scale))
    if degree < 2:
        check(checks, label + ':balanced direct constraint injection', np.linalg.norm(port['constraint_forcing']) / metric_scale)
    if degree == 0:
        expected = -context['scale']**2 * context['reference'] * direct * (context['local']['C'] - 2) / (18 * context['local']['C'])
        check(checks, label + ':derived pressure-mediated cubic coefficient', original.scaled_error(port['metric_T_cubic'], expected))
        check(checks, label + ':isotropic metric response', original.scaled_error(port['metric_T_cubic'], port['metric_L_cubic']))
        wrong = rates[0] + context['reference'] * context['local']['chi'] * (1 - context['local']['C']) * port['gas_rate']
        check(checks, label + ':uncorrected NR heat capacity rejected', int(original.scaled_error(wrong, rates[0], stress_scale) <= 1e-7), 0)
    if degree == 2:
        check(checks, label + ':trace-free leading metric response', np.linalg.norm(2 * port['metric_T_cubic'] + port['metric_L_cubic']) /
            max(np.linalg.norm(port['metric_T_cubic']) + np.linalg.norm(port['metric_L_cubic']), 1e-300))
    return dict(exchange=np.linalg.norm(port['photon_moment'] + gas) / transfer_scale if degree < 2 else 0.,
        direct_readout_error=original.scaled_error(port['photon_moment'], direct),
        cubic_metric_norm=float(np.linalg.norm(np.vstack([native_T, native_L]))),
        native_frame_error=max(original.scaled_error(rates[index], port[name], stress_scale) for index, name in
            enumerate(('energy', 'current', 'stress_transverse', 'stress_longitudinal'))))


def freeze():
    protocol()
    assert not (ROOT / 'precision-configuration.json').exists()
    inputs = {}
    for name in ('results/precision-diagnosis.json', 'results/warm.json', 'results/middle.json', 'results/cold.json',
            'results/control.json', 'results/algebra.json'):
        register(inputs, ROOT / name)
    write(ROOT / 'precision-configuration.json', dict(frozen_at=now(), inputs=inputs,
        code={name: digest(ROOT / name) for name in ('repair241.py', 'PRECISION-REPAIR.md', 'ports241.py')},
        identity_tolerance=1e-10, response_tolerance=.002, original_failed_checks=146,
        change='High/low near-identity mass inverse and its native stress readout; no source, gas or gate change'))
    write(CANDIDATE / 'inputs.json', read(ROOT / 'inputs.json'))
    for name in ('control', 'algebra'):
        write(CANDIDATE / 'results' / f'{name}.json', read(ROOT / 'results' / f'{name}.json'))


def pilot():
    modest()
    setup_repair()
    assert not (ROOT / 'results/precision-pilot.json').exists()
    basis = packet(PORTS / 'frozen/basis.npz')
    moment = repair.SameMassMoment(basis)
    matrices = packet(PARENT / 'results/warm-three-hard-angle-sum.npz')
    context = read(PORTS / 'results/warm-contexts.json')[0]
    checks, records = [], []
    with mp.workdps(80):
        mass = mp.matrix([[scalar(value) for value in row] for row in moment.mass])
        inverse = mass**-1
        exact_energy = mp.matrix([moment.exact]).T
        for degree in (0, 1, 2):
            for component in ('leading_control', 'real_correction', 'virtual', 'combined'):
                key = f'angular6:join1:heavy:original:l{degree}:{component}'
                matrix = matrices[key]
                high, low, bound = solve_pair(matrix, degree, basis, context)
                measured = physical_port(matrix, degree, basis, moment, context)['photon_moment']
                for column in (0, 1, 96, 97, 98):
                    weak = mp.matrix([scalar(value) for value in matrix[1:-1, column]])
                    scale = (2 * degree + 1) * scalar(context['opacity'])
                    expected = scale * inverse * weak
                    represented = mp.matrix([scalar(upper) + scalar(lower) for upper, lower in zip(high[:, column], low[:, column])])
                    error = max(abs(value) for value in represented - expected)
                    reference = max(max(abs(value) for value in expected), mp.mpf('1e-300'))
                    check(checks, key + f':column{column}:independent80digit mass solve', error / reference)
                    denominator = abs(scale) * max(abs(value) for value in weak) * bound['relative_infinity_solver_bound']
                    check(checks, key + f':column{column}:Neumann plus rounding bound', error / max(denominator, mp.mpf('1e-300')), 1.)
                    expected_moment = (exact_energy.T * expected)[0] / (2 * degree + 1)
                    moment_error = abs(scalar(measured[column]) - expected_moment) / max(abs(expected_moment), mp.mpf('1e-300'))
                    check(checks, key + f':column{column}:independent80digit energy readout', moment_error)
                    records.append(dict(key=key, column=column, mass_relative_error=float(error / reference), moment_relative_error=float(moment_error)))
    failures = [row for row in checks if not row['passed']]
    report = dict(stage=241, qualified=not failures, checks=checks, failed=failures, records=records,
        maximum_mass_error=max(row['mass_relative_error'] for row in records),
        maximum_moment_error=max(row['moment_relative_error'] for row in records), solver_bound=bound,
        script_sha256=digest(__file__), finished_at=now())
    write(ROOT / 'results/precision-pilot.json', report)
    print(json.dumps({key: value for key, value in report.items() if key not in ('checks', 'records')}, indent=2), flush=True)


def run(anchor):
    setup_repair()
    assert read(ROOT / 'results/precision-pilot.json')['qualified']
    namespace = dict(original.run.__globals__)
    namespace.update(ROOT=CANDIDATE, physical_port=physical_port, verify_port=verify_port, __file__=__file__)
    runner = types.FunctionType(original.run.__code__, namespace, 'precision_carried_original_assessment')
    runner(anchor)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['freeze', 'pilot', 'warm', 'middle', 'cold'])
    mode = parser.parse_args().mode
    freeze() if mode == 'freeze' else pilot() if mode == 'pilot' else run(mode)

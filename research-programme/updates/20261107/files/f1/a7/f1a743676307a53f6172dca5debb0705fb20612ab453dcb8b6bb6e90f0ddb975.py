from common241 import *
from types import SimpleNamespace
import argparse


def environment(config, inputs):
    basis = packet(PORTS / 'frozen/basis.npz')
    moment = repair.SameMassMoment(basis)
    systems = {model: retained.gravity.prior.System(model, 6400, inputs) for model in ('heavy', 'cold')}
    histories = {model: packet(BRANCH / 'two-way-thermal-gravity-20261026' / 'runs' / f'{model}-6400/history.npz') for model in systems}
    return basis, moment, systems, histories


def physical_port(matrix, degree, basis, moment, context):
    local = context['local']
    port = coupling.lift(matrix, degree, SimpleNamespace(mass=basis['mass'], energy=basis['energy']),
        context['opacity'], local['chi'], local['C'], local['B'])
    protected, original, defect = moment.contract(port['photon'], degree)
    port.update(photon_moment=protected, ordinary_photon_moment=original, readout_defect=defect)
    port.update(coupling.metric_response(port, degree, context['reference'], context['scale'], local['C']))
    port['metric_T_cubic'] = port['sigma_transverse_second'] / 3
    port['metric_L_cubic'] = port['sigma_longitudinal_second'] / 3
    return port


def scaled_error(first, second, scale=None):
    return coupling.normalization_error(first, second, scale)


def verify_port(label, port, matrix, degree, context, native_rows, checks):
    direct, gas = port['direct_moment'], port['gas_moment']
    transfer_scale = max(np.linalg.norm(direct) + np.linalg.norm(gas), 1e-300)
    check(checks, label + ':same-mass direct photon moment', scaled_error(port['photon_moment'], direct))
    if degree < 2:
        check(checks, label + ':independent gas exchange', np.linalg.norm(port['photon_moment'] + gas) / transfer_scale)
        divisor = context['local']['chi'] * context['local']['C'] if degree == 0 else context['local']['B']
        check(checks, label + ':gas primitive to stress', scaled_error(port['gas_rate'] * divisor, gas))
        check(checks, label + ':omitted gas rejected', int(np.linalg.norm(port['photon_moment']) / transfer_scale <= 1e-7), 0)
        if degree == 1:
            check(checks, label + ':omitted dipole inverse mass rejected', int(np.linalg.norm(port['photon_moment'] / 3 + gas) / transfer_scale <= 1e-7), 0)
    source = np.vstack([port['photon'], port['gas_rate'] if degree < 2 else np.zeros(matrix.shape[1])])
    high, low = native_rows
    rates = context['reference'] * precise.stable_dot(source.T, high, low).T
    stress_scale = context['reference'] * transfer_scale
    for index, name in enumerate(('energy', 'current', 'stress_transverse', 'stress_longitudinal')):
        check(checks, label + ':native stress rate:' + name, scaled_error(rates[index], port[name], stress_scale))
    native_T = context['scale']**2 * (rates[0] - rates[3]) / 6
    native_L = context['scale']**2 * (rates[0] + rates[3] - 2 * rates[2]) / 6
    metric_scale = context['scale']**2 * stress_scale
    check(checks, label + ':native transverse cubic metric coefficient', scaled_error(native_T, port['metric_T_cubic'], metric_scale))
    check(checks, label + ':native longitudinal cubic metric coefficient', scaled_error(native_L, port['metric_L_cubic'], metric_scale))
    native_constraint = np.vstack([-2 * context['scale']**2 * rates[0], -context['scale']**2 * rates[1]])
    check(checks, label + ':native constraint-rate forcing', scaled_error(native_constraint, port['constraint_forcing'], metric_scale))
    if degree < 2:
        check(checks, label + ':balanced direct constraint injection', np.linalg.norm(port['constraint_forcing']) / metric_scale)
    if degree == 0:
        expected = -context['scale']**2 * context['reference'] * direct * (context['local']['C'] - 2) / (18 * context['local']['C'])
        check(checks, label + ':derived pressure-mediated cubic coefficient', scaled_error(port['metric_T_cubic'], expected))
        check(checks, label + ':isotropic metric response', scaled_error(port['metric_T_cubic'], port['metric_L_cubic']))
        wrong = rates[0] + context['reference'] * context['local']['chi'] * (1 - context['local']['C']) * port['gas_rate']
        wrong_error = scaled_error(wrong, rates[0], stress_scale)
        check(checks, label + ':uncorrected NR heat capacity rejected', int(wrong_error <= 1e-7), 0)
    if degree == 2:
        check(checks, label + ':trace-free leading metric response', np.linalg.norm(2 * port['metric_T_cubic'] + port['metric_L_cubic']) /
            max(np.linalg.norm(port['metric_T_cubic']) + np.linalg.norm(port['metric_L_cubic']), 1e-300))
    return dict(exchange=np.linalg.norm(port['photon_moment'] + gas) / transfer_scale if degree < 2 else 0.,
        direct_readout_error=scaled_error(port['photon_moment'], direct),
        cubic_metric_norm=float(np.linalg.norm(np.vstack([native_T, native_L]))),
        native_frame_error=max(scaled_error(rates[index], port[name], stress_scale) for index, name in
            enumerate(('energy', 'current', 'stress_transverse', 'stress_longitudinal'))))


def control():
    modest()
    config = protocol()
    assert not (ROOT / 'results/control.json').exists()
    inputs = read(ROOT / 'inputs.json')
    basis, moment, systems, histories = environment(config, inputs)
    checks = []
    for anchor in ('warm', 'middle', 'cold'):
        contexts = read(PORTS / 'results' / f'{anchor}-contexts.json')
        matrices = packet(REFERENCE / 'results' / f'{anchor}-assessment.npz')
        raw = packet(PORTS / 'results' / f'{anchor}-ports.npz')
        protected = packet(PORTS / 'results' / f'{anchor}-protected-ports.npz')
        for state, context in zip(config['states'], contexts):
            assert (context['model'], context['history']) == (state['model'], state['history'])
            for join in config['joins']:
                for degree in config['multipoles']:
                    for component in ('leading_control', 'MTS_correction', 'combined'):
                        key = f'angular6:join{join}:{state["model"]}:{state["history"]}:l{degree}:{component}'
                        port = physical_port(matrices[key], degree, basis, moment, context)
                        for name in ('photon', 'gas_rate', 'gas_moment'):
                            check(checks, anchor + ':' + key + ':saved raw ' + name, relative(port[name], raw[key + ':' + name]))
                        for name in ('photon_moment', 'pressure', 'shear', 'energy', 'current', 'sigma_transverse_second', 'sigma_longitudinal_second'):
                            check(checks, anchor + ':' + key + ':saved protected ' + name, relative(port[name], protected[key + ':' + name]))
    modules(inputs)
    failures = [row for row in checks if not row['passed']]
    write(ROOT / 'results/control-inputs.json', inputs)
    write(ROOT / 'results/control.json', dict(stage=241, qualified=not failures, checks=checks, failed=failures,
        maximum_error=max(row['value'] for row in checks), finished_at=now(), script_sha256=digest(__file__),
        scope='Reproduce Stage238 angular6 event0 physical ports before new support'))
    print(json.dumps(dict(controls=len(checks), failures=failures[:8])), flush=True)


def run(anchor):
    modest()
    config = protocol()
    assert read(ROOT / 'results/control.json')['qualified']
    assert read(ROOT / 'results/algebra.json')['qualified']
    assert not (ROOT / 'results' / f'{anchor}.json').exists()
    inputs = read(ROOT / 'inputs.json')
    basis, moment, systems, histories = environment(config, inputs)
    contexts = read(PORTS / 'results' / f'{anchor}-contexts.json')
    matrices = packet(PARENT / 'results' / f'{anchor}-three-hard-angle-sum.npz')
    individual = [packet(REFERENCE / 'results' / f'{anchor}-assessment.npz')]
    individual.extend(packet(PARENT / 'results' / f'{anchor}-e{event}-components.npz') for event in (1, 2))
    checks, records, refinements, density_records, output = [], [], [], [], {}
    for state_index, (state, context) in enumerate(zip(config['states'], contexts)):
        assert (context['model'], context['history']) == (state['model'], state['history'])
        native = frame_owner.SavedFrame(systems[state['model']], histories[state['model']], context, basis)
        native_rows = {degree: frame_owner.stable_rows(native, degree, moment, checks,
            f'{anchor}:{state["model"]}:{state["history"]}:l{degree}') for degree in config['multipoles']}
        local = context['local']
        for join in config['joins']:
            for order in config['angular_orders']:
                prefix = f'angular{order}:join{join}:{state["model"]}:{state["history"]}'
                for degree in config['multipoles']:
                    components = {}
                    for component in config['components']:
                        key = prefix + f':l{degree}:' + component
                        matrix = matrices[key]
                        reconstructed = sum(event[key] for event in individual)
                        check(checks, anchor + ':' + key + ':coverage sum exactly once', relative(matrix, reconstructed))
                        port = physical_port(matrix, degree, basis, moment, context)
                        record = verify_port(anchor + ':' + key, port, matrix, degree, context, native_rows[degree], checks)
                        records.append(dict(anchor=anchor, key=key, component=component, degree=degree, **record))
                        components[component] = port
                        for name, value in port.items():
                            output[key + ':' + name] = np.asarray(value)
                    for name in ('photon', 'gas_rate', 'pressure', 'shear', 'metric_T_cubic', 'metric_L_cubic'):
                        matched = sum(components[part][name] for part in ('real_correction', 'virtual', 'state'))
                        check(checks, anchor + ':' + prefix + f':l{degree}:{name}:matched component additivity',
                            scaled_error(matched, components['MTS_correction'][name]))
                        combined = components['leading_control'][name] + components['MTS_correction'][name]
                        check(checks, anchor + ':' + prefix + f':l{degree}:{name}:equal-support baseline additivity',
                            scaled_error(combined, components['combined'][name]))
                for component in config['components']:
                    quadratic = matrices[prefix + ':C2:' + component]
                    density = physical_port(quadratic[:, None], 0, basis, moment, context)
                    transfer = context['opacity'] * quadratic[0]
                    gas_transfer = context['opacity'] * quadratic[-1]
                    density_rate = density['gas_rate'][0] + transfer / (local['chi'] * local['C'])
                    transfer_scale = max(abs(transfer) + abs(gas_transfer), 1e-300)
                    check(checks, anchor + ':' + prefix + ':' + component + ':derived density temperature cancellation',
                        abs(density_rate * local['chi'] * local['C']) / transfer_scale)
                    coefficients = coupling.background_transfer_tangent(local, transfer, 0., 0., 1., 1., 1.)
                    temperature_self = local['C_R'] * transfer / (local['chi'] * local['C']**2)
                    velocity_self = (1 + 2 / (3 * local['C'])) * transfer / local['B']
                    check(checks, anchor + ':' + prefix + ':' + component + ':derived background capacity column',
                        scaled_error(coefficients['temperature_rate'], transfer / (local['chi'] * local['C']) + temperature_self))
                    check(checks, anchor + ':' + prefix + ':' + component + ':derived background enthalpy column',
                        scaled_error(coefficients['velocity_rate'], velocity_self))
                    for name, value in [('density_photon', density['photon'][:, 0]), ('density_gas_temperature', density_rate),
                            ('temperature_self_feedback', temperature_self), ('velocity_self_feedback', velocity_self),
                            ('background_transfer', transfer), ('off_shell_energy', coefficients['energy_defect']),
                            ('off_shell_current', coefficients['current_defect'])]:
                        output[prefix + ':' + component + ':' + name] = np.asarray(value)
                    density_records.append(dict(anchor=anchor, key=prefix + ':' + component, background_transfer=float(transfer),
                        independent_gas_transfer=float(gas_transfer), temperature_density_rate=float(density_rate),
                        capacity_feedback=float(temperature_self), enthalpy_feedback=float(velocity_self)))
            for degree in config['multipoles']:
                for component in config['components']:
                    for name in ('photon', 'gas_rate', 'pressure', 'shear', 'metric_T_cubic', 'metric_L_cubic'):
                        tail = f'join{join}:{state["model"]}:{state["history"]}:l{degree}:{component}:{name}'
                        first, last = output['angular4:' + tail], output['angular6:' + tail]
                        error = relative(first, last)
                        check(checks, anchor + ':' + tail + ':angular4-to6 physical response', error, config['response_tolerance'])
                        refinements.append(dict(anchor=anchor, key=tail, relative_error=error,
                            reference_norm=float(np.linalg.norm(last)), absolute_difference=float(np.linalg.norm(first - last))))
    assert all(np.all(np.isfinite(value)) for value in output.values())
    target = ROOT / 'results' / f'{anchor}-ports-and-jets.npz'
    save(target, **output)
    modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    failures = [row for row in checks if not row['passed']]
    write(ROOT / 'results' / f'{anchor}-inputs.json', inputs)
    result = dict(stage=241, anchor=anchor, qualified=not failures, checks=checks, failed=failures,
        records=records, refinements=refinements, density_records=density_records,
        maximum_port_refinement=max(row['relative_error'] for row in refinements),
        maximum_readout_error=max(row['direct_readout_error'] for row in records),
        maximum_exchange_error=max(row['exchange'] for row in records),
        maximum_native_frame_error=max(row['native_frame_error'] for row in records),
        output_sha256=digest(target), script_sha256=digest(__file__), finished_at=now(),
        finite_interval_propagated=False, incoming_history_changed=False, tail_closure_added=False,
        scope='Three-hard-angle source to native EOS/stress and first nonzero local metric coefficient, with density and background-transfer columns')
    write(ROOT / 'results' / f'{anchor}.json', result)
    print(json.dumps(dict(anchor=anchor, checks=len(checks), failures=len(failures), first_failures=failures[:12],
        maximum_port_refinement=result['maximum_port_refinement'], maximum_readout_error=result['maximum_readout_error'])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['control', 'warm', 'middle', 'cold'])
    arguments = parser.parse_args()
    control() if arguments.mode == 'control' else run(arguments.mode)

from common240 import *
sys.path.insert(0, str(REFERENCE))
import virtual237 as retained_virtual
import common234
import radial234
import state235
import argparse
GRID_CACHE = {}


def tree_at(parameters):
    energy, cosine = mp.mpf(str(parameters['energy'])), mp.mpf(str(parameters['cosine']))
    return angular.inherited.source.exact.single_tensor(energy, mp.matrix([mp.sqrt(1 - cosine**2), 0, cosine]))[0]


def tensors(row, order, checks):
    target = ROOT / 'virtual' / event_key(row) / f'angular{order}-tensors.json'
    if target.exists():
        report = read(target)
        assert report['script_sha256'] == digest(__file__)
        checks.extend(report['tensor_checks'])
        return report
    parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
    owner, exact = angular.inherited.source.dressed, angular.inherited.source.exact
    with mp.workdps(80):
        energy, cosine, temperature = [mp.mpf(str(value)) for value in (parameters['energy'], parameters['cosine'], row['theta'])]
        initial = mp.matrix([1, 0, 0, 0])
        incoming_direction = mp.matrix([0, 0, 1])
        outgoing_direction = mp.matrix([mp.sqrt(1 - cosine**2), 0, cosine])
        incoming = exact.photon(energy, incoming_direction)
        outgoing = exact.photon(energy / (1 + energy * (1 - cosine)), outgoing_direction)
        final = initial + incoming - outgoing
        left = exact.spinors(final).transpose_conj() * exact.gamma_matrices()[0]
        right = exact.spinors(initial)
        frames = (exact.frame(incoming_direction), exact.frame(outgoing_direction))
        bath = mp.matrix([mp.mpf(str(value)) for value in parameters['bath']])
        rays = []
        for index, (raw_direction, angular_weight) in enumerate(angular.inherited.source.angular_nodes(order)):
            direction = exact.unit(raw_direction)
            null = exact.photon(mp.mpf(1), direction)
            doppler = exact.dot(bath, null)
            local_temperature = temperature / doppler
            lab = np.asarray(parameters['transform']) @ np.array(list(null), dtype=float)
            lab_direction = lab[1:] / np.linalg.norm(lab[1:])
            entries = []
            for incoming_index in range(2):
                for outgoing_index in range(2):
                    first_pol, second_pol = frames[0][incoming_index], frames[1][outgoing_index]
                    raw = owner.radial_decomposition(initial, incoming, outgoing, first_pol, second_pol, direction)
                    constant = left * raw['constant'] * right + owner.external_finite_constant(initial, incoming, outgoing, first_pol, second_pol, null)
                    poles = [dict(location=mp.nstr(pole['location'], 85), sign=int(pole['denominator_slope_sign']),
                        coefficient=common234.matrix_text(left * pole['coefficient'] * right)) for pole in raw['poles']]
                    if index == 0:
                        value = constant * local_temperature**2 * mp.pi**2 / 6
                        for pole in poles:
                            scaled = mp.mpf(pole['location']) / local_temperature
                            kernel = (mp.log(scaled / (2 * mp.pi)) - mp.re(mp.digamma(mp.j * scaled / (2 * mp.pi)))) / 2
                            kernel -= mp.j * mp.pi * pole['sign'] / (2 * mp.expm1(scaled))
                            value += common234.matrix_value(pole['coefficient']) * kernel
                        independent = owner.finite_dressed(initial, incoming, outgoing, first_pol, second_pol, direction, local_temperature)
                        check(checks, f'{event_key(row)}:a{order}:pol{incoming_index}{outgoing_index}:dressed replay',
                            mp.norm(value - independent) / max(mp.norm(independent), mp.mpf('1e-300')))
                    entries.append(dict(incoming_polarization=incoming_index, outgoing_polarization=outgoing_index,
                        constant=common234.matrix_text(constant), poles=poles))
            rays.append(dict(index=index, rest_direction=[mp.nstr(value, 85) for value in direction],
                lab_direction=lab_direction.tolist(), doppler=mp.nstr(doppler, 85), weight=angular_weight, polarizations=entries))
        prefactor = 4 * mp.pi * mp.mpf(str(angular.inherited.source.ALPHA)) / (2 * (2 * mp.pi)**3)
    result = dict(event=event_key(row), angular_order=order, rays=rays, prefactor=mp.nstr(prefactor, 85),
        script_sha256=digest(__file__), tensor_checks=checks.copy(), finished_at=now())
    write(target, result)
    return result


def scalar_maps(config, row, report, features, join, checks):
    parameters, unused = source.physics.parameters_and_weight(row['theta'], row['node'])
    with mp.workdps(80):
        tree = tree_at(parameters)
    cache_key = id(features), join, config['virtual_radial_order']
    if cache_key not in GRID_CACHE:
        GRID_CACHE[cache_key] = radial234.grid(features, join, config['virtual_radial_order'])
    frequency, weights, numerator = GRID_CACHE[cache_key]
    constant = weights @ numerator
    inherited_constant = packet(retained_virtual.VIRTUAL / 'radial' / f'join{join}-order6.npz')['constant']
    check(checks, f'{event_key(row)}:join{join}:unchanged constant radial moment', relative(constant, inherited_constant))
    constant = inherited_constant
    full, compensation = np.zeros((99, 13)), np.zeros((99, 13))
    thermal_terms, exterior_poles = [], 0
    with mp.workdps(80):
        for ray in report['rays']:
            entries = ray['polarizations']
            descriptors = entries[0]['poles']
            assert all([(pole['location'], pole['sign']) for pole in entry['poles']] ==
                [(pole['location'], pole['sign']) for pole in descriptors] for entry in entries)
            constant_tensor = [value for entry in entries for value in common234.matrix_value(entry['constant'])]
            coefficient = retained_virtual.contract(tree, constant_tensor)
            pole_coefficients = [retained_virtual.contract(tree, [value for entry in entries for value in
                common234.matrix_value(entry['poles'][index]['coefficient'])]) for index in range(2)]
            temperature = mp.mpf(str(row['theta'])) / mp.mpf(ray['doppler'])
            factor = mp.mpf(report['prefactor']) * scalar(ray['weight'])
            spectral = complex(coefficient * temperature**2) * constant.astype(complex)
            thermal = coefficient * temperature**2 * mp.pi**2 / 6
            for pole_index, pole in enumerate(descriptors):
                location = float(mp.mpf(pole['location']) * mp.mpf(ray['doppler']) / scalar(row['theta']))
                if config['spectral_domain'][0] < location < config['spectral_domain'][1]:
                    integral, unused = radial234.pole_integral(features.splines[join], frequency, weights, numerator, location, pole['sign'])
                else:
                    assert location not in config['spectral_domain']
                    integral = (weights @ (numerator / (frequency**2 - location**2)[:, None])).astype(complex)
                    exterior_poles += 1
                spectral += complex(pole_coefficients[pole_index]) * integral
                scaled = mp.mpf(pole['location']) / temperature
                kernel = (mp.log(scaled / (2 * mp.pi)) - mp.re(mp.digamma(mp.j * scaled / (2 * mp.pi)))) / 2
                kernel -= mp.j * mp.pi * pole['sign'] / (2 * mp.expm1(scaled))
                thermal += pole_coefficients[pole_index] * kernel
            direction = np.array(ray['lab_direction'])[None, :]
            harmonic = np.concatenate([[1.], direction[0], angular.angular_feature(direction, 2)[0]])
            term = (float(factor) * spectral.real)[:, None] * harmonic[None, :]
            change = term - compensation
            updated = full + change
            compensation = (updated - full) - change
            full = updated
            thermal_terms.append(factor * mp.re(thermal))
        thermal = float(mp.fsum(thermal_terms))
    return dict(scalar_map=full, thermal_scalar=np.array(thermal), outside_poles=np.array(exterior_poles))


def blocks(config, row, join, mapped, features, models, checks):
    parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
    event = geometry(parameters)
    tests = models[0]['difference'].tests.evaluate(np.array(event['frequencies']))
    basis = features.evaluate(np.array(event['frequencies']), join)
    scalar_map = mapped['scalar_map'][:98]
    output = {}
    with mp.workdps(80):
        vacuum = angular.inherited.vacuum.finite_virtual_ratio(mp.mpf(str(parameters['energy'])), mp.mpf(str(parameters['cosine'])))
        vacuum += angular.inherited.vacuum.soft_constant(mp.mpf(str(parameters['energy'])), mp.mpf(str(parameters['cosine'])))
        factor = float((vacuum + scalar(float(mapped['thermal_scalar']))) / 2)
        for state_index, state in enumerate(config['states']):
            physical = [scalar(config['heat']) * mp.mpf(value) for value in state['coefficients']]
            potential = [mp.fsum(scalar(value) * coefficient for value, coefficient in zip(line, physical[:98])) for line in basis]
            stats = statistics(event, potential, physical[-1])
            for degree, section in [(0, slice(0, 1)), (1, slice(1, 4)), (2, slice(4, 13))]:
                equilibrium, unused, left, unused = projected(event, tests, basis, stats['equilibrium'], degree)
                mixed, unused, unused, unused = projected(event, tests, basis, stats['mixed'], degree)
                statistical = weight * factor * mixed
                background = float(mp.fsum(scalar(value) * coefficient for value, coefficient in zip(scalar_map[:, 0], physical[:98])))
                wave = np.vstack([scalar_map[:, section], np.zeros((1, scalar_map[:, section].shape[-1]))])
                first = .5 * weight * background * equilibrium
                second = .5 * weight * float(stats['linear_source']) * (left @ wave.T) / (2 * degree + 1)
                total = statistical + first + second
                prefix = f'state{state_index}:l{degree}'
                for name, value in [('statistical', statistical), ('background', first), ('wave', second), ('total', total)]:
                    output[prefix + ':' + name] = value
                    if degree < 2:
                        check(checks, f'{event_key(row)}:join{join}:{prefix}:{name}:independent gas force',
                            np.linalg.norm(value[0] + value[-1]) / max(np.linalg.norm(value[0]) + np.linalg.norm(value[-1]), 1e-300))
    return output


def run(hard_event, control=False):
    modest()
    config = secondary_protocol()
    original, features, models = setup(config)
    rows = config['reused_event_zero'] if control else [row for row in config['events'] if row['event'] == hard_event]
    for row in rows:
        for order in config['angular_orders']:
            checks = []
            if control:
                report = read(REFERENCE / 'virtual' / f'angular{order}' / (row['label'] + '-tensors.json'))
            else:
                assert read(ROOT / 'results/secondary-control.json')['qualified']
                report = tensors(row, order, checks)
            for join in config['joins']:
                target = ROOT / ('control' if control else 'virtual') / event_key(row) / f'angular{order}-join{join}.npz'
                if target.exists():
                    metadata = read(target.with_suffix('.json'))
                    assert metadata['qualified'] and digest(target) == metadata['sha256']
                    continue
                began = time.monotonic()
                mapped = scalar_maps(config, row, report, features, join, checks)
                values = blocks(config, row, join, mapped, features, models, checks)
                if control:
                    reference = packet(REFERENCE / 'virtual' / f'angular{order}' / f'{row["label"]}-join{join}.npz')
                    for name in ('scalar_map', 'thermal_scalar'):
                        check(checks, f'{event_key(row)}:a{order}:join{join}:saved ' + name, relative(mapped[name], reference[name]))
                    for name in values:
                        check(checks, f'{event_key(row)}:a{order}:join{join}:saved ' + name, relative(values[name], reference[name]))
                save(target, **mapped, **values)
                failures = [entry for entry in checks if not entry['passed']]
                write(target.with_suffix('.json'), dict(qualified=not failures, checks=checks, failed=failures,
                    sha256=digest(target), event=event_key(row), order=order, join=join, script_sha256=digest(__file__),
                    configuration_sha256=digest(ROOT / 'secondary-configuration.json'), seconds=time.monotonic() - began, finished_at=now()))
                print(json.dumps(dict(virtual=event_key(row), order=order, join=join, failures=len(failures))), flush=True)
                assert not failures, failures[:3]


def secondary_protocol():
    config = protocol()
    frozen = read(ROOT / 'secondary-configuration.json')
    for name, expected in frozen['code'].items():
        assert digest(ROOT / name) == expected, name
    for path, expected in frozen['inputs'].items():
        assert digest(path) == expected, path
    return config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('event', type=int, choices=[0, 1, 2])
    arguments = parser.parse_args()
    run(arguments.event, control=arguments.event == 0)

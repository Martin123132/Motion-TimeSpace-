from common237 import *
import argparse


def freeze():
    config = protocol()
    target = ROOT / 'virtual-configuration.json'
    assert not target.exists()
    write(target, dict(frozen_at=now(), script_sha256=digest(__file__),
        configuration_sha256=digest(ROOT / 'configuration.json'), angular_orders=[2, 4, 6, 8],
        scalar_contraction='2 Re <tree,amplitude> / <tree,tree>; complex pole coefficients retained',
        spectral_domain=config['spectral_domain'], radial_order=6,
        outside_poles='Ordinary finite-domain integral, no imaginary residue outside domain; no history exterior assumed'))


def contract(tree, tensor):
    normalization = mp.fsum(mp.mpc(value).conjugate() * mp.mpc(value) for value in tree.ravel())
    return 2 * mp.fsum(mp.mpc(value).conjugate() * coefficient
                      for value, coefficient in zip(tree.ravel(), tensor)) / normalization


def tensors(row, order, checks):
    target = ROOT / 'virtual' / f'angular{order}' / (row['label'] + '-tensors.json')
    if target.exists():
        saved = read(target)
        assert saved['script_sha256'] == digest(__file__)
        return saved
    parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
    old = packet(VIRTUAL / 'tensors' / (row['label'] + '.npz'))
    if order == 2:
        result = read(VIRTUAL / 'tensors' / (row['label'] + '.json'))
        return dict(result, tree=old['tree'])
    owner, exact = angular.inherited.source.dressed, angular.inherited.source.exact
    with mp.workdps(80):
        energy, cosine, temperature = [mp.mpf(str(value)) for value in
                                       (parameters['energy'], parameters['cosine'], row['theta'])]
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
                    constant = left * raw['constant'] * right + owner.external_finite_constant(
                        initial, incoming, outgoing, first_pol, second_pol, null)
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
                        check(checks, f'{row["label"]}:angular{order}:pol{incoming_index}{outgoing_index}:dressed replay',
                            mp.norm(value - independent) / max(mp.norm(independent), mp.mpf('1e-300')))
                    entries.append(dict(incoming_polarization=incoming_index, outgoing_polarization=outgoing_index,
                        constant=common234.matrix_text(constant), poles=poles))
            rays.append(dict(index=index, rest_direction=[mp.nstr(value, 85) for value in direction],
                lab_direction=lab_direction.tolist(), doppler=mp.nstr(doppler, 85), weight=angular_weight, polarizations=entries))
        prefactor = 4 * mp.pi * mp.mpf(str(angular.inherited.source.ALPHA)) / (2 * (2 * mp.pi)**3)
    result = dict(label=row['label'], angular_order=order, rays=rays, prefactor=mp.nstr(prefactor, 85),
        script_sha256=digest(__file__), tensor_checks=checks.copy(), finished_at=now())
    write(target, result)
    return result


def scalar_maps(config, row, order, report, features, join, checks):
    anchor = next(index for index, entry in enumerate(config['events']) if entry['label'] == row['label'])
    old = packet(VIRTUAL / 'tensors' / (row['label'] + '.npz'))
    tree = old['tree']
    radial = packet(VIRTUAL / 'radial' / f'join{join}-order6.npz')
    constant = radial['constant']
    if order != 2:
        frequency, weights, numerator = radial234.grid(features, join, 6)
        check(checks, f'{row["label"]}:angular{order}:join{join}:fixed constant moment', relative(weights @ numerator, constant))
    full = np.zeros((99, 13))
    compensation = np.zeros_like(full)
    thermal_terms, exterior_poles = [], 0
    radial_values, radial_locations = [], []
    with mp.workdps(80):
        for ray_index, ray in enumerate(report['rays']):
            entries = ray['polarizations']
            pole_descriptors = entries[0]['poles']
            assert all([(pole['location'], pole['sign']) for pole in entry['poles']] ==
                       [(pole['location'], pole['sign']) for pole in pole_descriptors] for entry in entries)
            constant_tensor = [value for entry in entries for value in common234.matrix_value(entry['constant'])]
            constant_coefficient = contract(tree, constant_tensor)
            pole_coefficients = [contract(tree, [value for entry in entries for value in
                common234.matrix_value(entry['poles'][pole_index]['coefficient'])]) for pole_index in range(2)]
            local_temperature = mp.mpf(str(row['theta'])) / mp.mpf(ray['doppler'])
            factor = mp.mpf(report['prefactor']) * scalar(ray['weight'])
            spectral = complex(constant_coefficient * local_temperature**2) * constant.astype(complex)
            thermal = constant_coefficient * local_temperature**2 * mp.pi**2 / 6
            values, locations = [], []
            for pole_index, pole in enumerate(pole_descriptors):
                location = float(mp.mpf(pole['location']) * mp.mpf(ray['doppler']) / scalar(row['theta']))
                locations.append(location)
                if order == 2:
                    integral = radial['poles'][anchor, ray_index, pole_index]
                elif config['spectral_domain'][0] < location < config['spectral_domain'][1]:
                    integral, unused = radial234.pole_integral(features.splines[join], frequency, weights, numerator, location, pole['sign'])
                else:
                    assert location != config['spectral_domain'][0] and location != config['spectral_domain'][1]
                    integral = (weights @ (numerator / (frequency**2 - location**2)[:, None])).astype(complex)
                    exterior_poles += 1
                values.append(integral)
                spectral += complex(pole_coefficients[pole_index]) * integral
                scaled = mp.mpf(pole['location']) / local_temperature
                kernel = (mp.log(scaled / (2 * mp.pi)) - mp.re(mp.digamma(mp.j * scaled / (2 * mp.pi)))) / 2
                kernel -= mp.j * mp.pi * pole['sign'] / (2 * mp.expm1(scaled))
                thermal += pole_coefficients[pole_index] * kernel
            direction = np.array(ray['lab_direction'])[None, :]
            angular_features = np.concatenate([[1.], direction[0], angular.angular_feature(direction, 2)[0]])
            term = (float(factor) * spectral.real)[:, None] * angular_features[None, :]
            change = term - compensation
            updated = full + change
            compensation = (updated - full) - change
            full = updated
            thermal_terms.append(factor * mp.re(thermal))
            radial_values.append(values)
            radial_locations.append(locations)
        thermal = float(mp.fsum(thermal_terms))
    if order == 2:
        reference = packet(VIRTUAL / 'response' / f'{row["label"]}-join{join}-order6.npz')['mueller'][:, :, 0, 0]
        for degree, section in [(0, slice(0, 1)), (1, slice(1, 4)), (2, slice(4, 13))]:
            check(checks, f'{row["label"]}:join{join}:l{degree}:scalar versus full tensor replay', relative(full[:, section], reference[:, section]))
        check(checks, f'{row["label"]}:join{join}:original Planck scalar replay', abs(thermal / read(row['loop_path'])['scalar'] - 1))
    return dict(scalar_map=full, thermal_scalar=np.array(thermal), poles=np.array(radial_values),
        pole_locations=np.array(radial_locations), outside_poles=np.array(exterior_poles))


def blocks(config, row, join, mapped, features, models, checks, order):
    parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
    event = geometry(parameters)
    tests = models[0]['difference'].tests.evaluate(np.array(event['frequencies']))
    basis = features.evaluate(np.array(event['frequencies']), join)
    old = packet(common234.PARENT / 'runs' / row['label'] / 'vertices.npz')
    reference = packet(VIRTUAL / 'results/virtual-mixed-blocks.npz') if order == 2 else None
    thermal_old = read(row['loop_path'])['scalar']
    scalar_map = mapped['scalar_map'][:98]
    output = {}
    with mp.workdps(80):
        for state_index, state in enumerate(config['states']):
            physical = [scalar(config['heat']) * mp.mpf(value) for value in state['coefficients']]
            potential = [mp.fsum(scalar(value) * coefficient for value, coefficient in zip(line, physical[:98])) for line in basis]
            stats = statistics(event, potential, physical[-1])
            for degree, section in [(0, slice(0, 1)), (1, slice(1, 4)), (2, slice(4, 13))]:
                equilibrium, unused, left, unused = projected(event, tests, basis, stats['equilibrium'], degree)
                mixed, unused, unused, unused = projected(event, tests, basis, stats['mixed'], degree)
                statistical = old[f'join{join}-state{state_index}-l{degree}-virtual-statistical-mixed']
                statistical = statistical + .5 * weight * (float(mapped['thermal_scalar']) - thermal_old) * mixed
                background = float(mp.fsum(scalar(value) * coefficient for value, coefficient in zip(scalar_map[:, 0], physical[:98])))
                wave = np.vstack([scalar_map[:, section], np.zeros((1, scalar_map[:, section].shape[-1]))])
                first = .5 * weight * background * equilibrium
                second = .5 * weight * float(stats['linear_source']) * (left @ wave.T) / (2 * degree + 1)
                total = statistical + first + second
                prefix = f'state{state_index}:l{degree}'
                for name, value in [('statistical', statistical), ('background', first), ('wave', second), ('total', total)]:
                    output[prefix + ':' + name] = value
                if degree < 2:
                    check(checks, f'{row["label"]}:angular{order}:join{join}:{prefix}:independent gas force',
                        np.linalg.norm(total[0] + total[-1]) / max(np.linalg.norm(total[0]) + np.linalg.norm(total[-1]), 1e-300))
                if order == 2:
                    name = f'{row["label"]}:join{join}:{state["model"]}:{state["history"]}:l{degree}:order6:total'
                    check(checks, f'{row["label"]}:join{join}:{prefix}:saved virtual block replay', relative(total, reference[name]))
    return output


def run():
    modest()
    config = protocol()
    frozen = read(ROOT / 'virtual-configuration.json')
    assert frozen['script_sha256'] == digest(__file__)
    assert frozen['configuration_sha256'] == digest(ROOT / 'configuration.json')
    original, features, models = setup(config)
    for order in frozen['angular_orders']:
        for row in config['events']:
            checks = []
            report = tensors(row, order, checks)
            for join in config['joins']:
                target = ROOT / 'virtual' / f'angular{order}' / f'{row["label"]}-join{join}.npz'
                if target.exists():
                    previous = read(target.with_suffix('.json'))
                    assert previous['qualified'] and digest(target) == previous['sha256']
                    assert previous['script_sha256'] == digest(__file__)
                    continue
                began = time.monotonic()
                mapped = scalar_maps(config, row, order, report, features, join, checks)
                values = blocks(config, row, join, mapped, features, models, checks, order)
                assert all(np.all(np.isfinite(value)) for value in list(mapped.values()) + list(values.values()))
                save(target, **mapped, **values)
                failed = [entry for entry in checks if not entry['passed']]
                result = dict(state='complete', qualified=not failed, checks=checks, failed=failed, sha256=digest(target),
                    script_sha256=digest(__file__), angular_order=order, radial_order=6, anchor=row['label'], join=join,
                    seconds=time.monotonic() - began, thermal_scalar=float(mapped['thermal_scalar']),
                    outside_poles=int(mapped['outside_poles']), actual_history_exterior_supplied=False, finished_at=now())
                write(target.with_suffix('.json'), result)
                print(json.dumps({name: value for name, value in result.items() if name not in ('checks', 'sha256', 'script_sha256')}), flush=True)
                assert not failed, failed


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['freeze', 'run'])
    {'freeze': freeze, 'run': run}[parser.parse_args().mode]()

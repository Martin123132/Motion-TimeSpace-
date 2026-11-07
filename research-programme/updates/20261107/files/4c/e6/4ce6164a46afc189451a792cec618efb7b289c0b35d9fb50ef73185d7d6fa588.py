from common234 import *
import argparse


def main(label):
    modest()
    config = protocol()
    output = ROOT / 'tensors' / (label + '.json')
    assert not output.exists()
    began = time.monotonic()
    row = next(row for row in config['events'] if row['label'] == label)
    parameters, event_weight = source.physics.parameters_and_weight(row['theta'], row['node'])
    loop = read(row['loop_path'])
    assert loop['identity'] == source.physics.event_owner.inherited.virtual_identity(parameters)
    owner = angular.inherited.source.dressed
    exact = angular.inherited.source.exact
    checks, rays = [], []
    with mp.workdps(config['tensor_digits']):
        energy, cosine, temperature = [mp.mpf(str(value)) for value in (parameters['energy'], parameters['cosine'], row['theta'])]
        initial = mp.matrix([1, 0, 0, 0])
        direction_in = mp.matrix([0, 0, 1])
        direction_out = mp.matrix([mp.sqrt(1 - cosine**2), 0, cosine])
        incoming = exact.photon(energy, direction_in)
        outgoing = exact.photon(energy / (1 + energy * (1 - cosine)), direction_out)
        final = initial + incoming - outgoing
        left = exact.spinors(final).transpose_conj() * exact.gamma_matrices()[0]
        right = exact.spinors(initial)
        frames = [exact.frame(direction_in), exact.frame(direction_out)]
        bath = mp.matrix([mp.mpf(str(value)) for value in parameters['bath']])
        accumulated = [[mp.zeros(2) for outgoing_index in range(2)] for incoming_index in range(2)]
        derivative_accumulated = [[mp.zeros(2) for outgoing_index in range(2)] for incoming_index in range(2)]
        for ray_index, (raw_direction, weight) in enumerate(angular.inherited.source.angular_nodes(2)):
            direction = exact.unit(raw_direction)
            null = exact.photon(mp.mpf(1), direction)
            doppler = exact.dot(bath, null)
            local_temperature = temperature / doppler
            lab_null = np.asarray(parameters['transform']) @ np.array(list(null), dtype=float)
            lab_direction = lab_null[1:] / np.linalg.norm(lab_null[1:])
            entries = []
            for incoming_index in range(2):
                for outgoing_index in range(2):
                    first_pol, second_pol = frames[0][incoming_index], frames[1][outgoing_index]
                    raw = owner.radial_decomposition(initial, incoming, outgoing, first_pol, second_pol, direction)
                    constant = left * raw['constant'] * right + owner.external_finite_constant(initial, incoming, outgoing, first_pol, second_pol, null)
                    poles = [dict(location=mp.nstr(pole['location'], 85), sign=int(pole['denominator_slope_sign']),
                        coefficient=matrix_text(left * pole['coefficient'] * right)) for pole in raw['poles']]
                    value = constant * local_temperature**2 * mp.pi**2 / 6
                    thermal_derivative = 2 * value
                    for pole in poles:
                        location = mp.mpf(pole['location']) / local_temperature
                        kernel = (mp.log(location / (2 * mp.pi)) - mp.re(mp.digamma(mp.j * location / (2 * mp.pi)))) / 2
                        kernel -= mp.j * mp.pi * pole['sign'] / (2 * mp.expm1(location))
                        derivative = -mp.mpf('.5') + mp.re(mp.j * location * mp.polygamma(1, mp.j * location / (2 * mp.pi)) / (4 * mp.pi))
                        derivative -= mp.j * mp.pi * pole['sign'] * location * mp.exp(location) / (2 * mp.expm1(location)**2)
                        value += matrix_value(pole['coefficient']) * kernel
                        thermal_derivative += matrix_value(pole['coefficient']) * derivative
                    if ray_index == 0:
                        independent = owner.finite_dressed(initial, incoming, outgoing, first_pol, second_pol, direction, local_temperature)
                        check(checks, f'{label}:pol{incoming_index}{outgoing_index}:original dressed amplitude', mp.norm(value - independent) / max(mp.norm(independent), mp.mpf('1e-300')))
                    accumulated[incoming_index][outgoing_index] += scalar(weight) * value
                    derivative_accumulated[incoming_index][outgoing_index] += scalar(weight) * thermal_derivative
                    entries.append(dict(incoming_polarization=incoming_index, outgoing_polarization=outgoing_index,
                        constant=matrix_text(constant), poles=poles))
            rays.append(dict(index=ray_index, rest_direction=[mp.nstr(value, 85) for value in direction],
                lab_direction=lab_direction.tolist(), doppler=mp.nstr(doppler, 85), weight=weight, polarizations=entries))
        prefactor = 4 * mp.pi * mp.mpf(str(angular.inherited.source.ALPHA)) / (2 * (2 * mp.pi)**3)
        result = np.array([[[[complex(prefactor * accumulated[incident][outgoing][last, first]) for first in range(2)]
                            for last in range(2)] for outgoing in range(2)] for incident in range(2)])
        derivative_result = np.array([[[[complex(prefactor * derivative_accumulated[incident][outgoing][last, first]) for first in range(2)]
                            for last in range(2)] for outgoing in range(2)] for incident in range(2)])
        tree, unused = exact.single_tensor(energy, direction_out)
        mueller = angular.inherited.source.mueller(tree)
        replay = angular.inherited.source.interference(tree, result) / mueller[0, 0]
        check(checks, label + ':cached scalar loop replay', abs(replay[0, 0] / loop['scalar'] - 1))
        saved = ROOT / 'tensors' / (label + '.npz')
        save(saved, tree=tree, planck=result, planck_temperature_derivative=derivative_result,
            replay_mueller=replay, temperature=row['theta'], event_weight=event_weight,
            incoming_stokes=parameters['incoming_stokes'], outgoing_stokes=parameters['outgoing_stokes'])
    failed = [entry for entry in checks if not entry['passed']]
    report = dict(stage=234, label=label, state='complete', qualified=not failed, checks=checks, failed=failed,
        rays=rays, prefactor=mp.nstr(prefactor, 85), sha256=digest(saved), event_identity=loop['identity'],
        cached_scalar=loop['scalar'], replay_scalar=float(replay[0, 0]), seconds=time.monotonic() - began,
        tensor_precision=config['tensor_digits'], directional_decompositions=32, planck_amplitude_replays=1,
        new_virtual_cache_entries=0, finished_at=now())
    write(output, report)
    print(json.dumps(dict(label=label, checks=len(checks), failed=failed, seconds=report['seconds'], scalar=float(replay[0, 0]))), flush=True)
    assert not failed, failed


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('label', choices=['warm', 'middle', 'cold'])
    main(parser.parse_args().label)

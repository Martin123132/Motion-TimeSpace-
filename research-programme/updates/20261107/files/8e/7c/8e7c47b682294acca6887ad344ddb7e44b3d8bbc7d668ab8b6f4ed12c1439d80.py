import argparse
from emission_angular_common import *
from leading_pair import leading_coefficients
from reaction_geometry import ReactionGeometry
from build_spectral_kernel import physical_block


def blocks_at(basis, theta, events, angular, profiles, gas_temperatures):
    count = basis.count
    maximum = len(angular) - 1
    names = [['I'] if degree < 2 else ['I', 'E'] for degree in range(maximum + 1)]
    baseline = [np.zeros((len(channels) * count, len(channels) * count)) for channels in names]
    mixed = [np.zeros((2, len(channels) * count, len(channels) * count)) for channels in names]
    temperature = np.zeros((2, count))
    base = np.zeros_like(basis.mass)
    mixed_base = np.zeros((2, count, count))
    speeds, _ = thermal_wave.prior.prior.juttner_rule(theta, 6)
    gamma = np.repeat(1 / np.sqrt(1 - speeds ** 2), 2 * 6 ** 3)
    pairs = [[(left, right) for left in range(len(channels)) for right in range(len(channels))
              if not (degree == 0 and left == right == 0)] for degree, channels in enumerate(names)]
    discarded, total = 0., 0.
    for frequency, measure, initial in zip(basis.nodes, basis.measure / 2, basis.values):
        recoil = 1 / (1 + theta * frequency * events['incident'] * (1 - events['cosine']))
        extra = (1 - recoil) ** 2 / recoil
        final = frequency * events['incident'] * recoil * events['outgoing']
        bose = (1 + 1 / np.expm1(final)) / (1 + 1 / np.expm1(frequency))
        probability = measure * events['weight'] * 1.5 * recoil ** 2 * bose
        trace = 1 + events['cosine'] ** 2 + extra
        inside = (final >= basis.minimum) & (final <= basis.maximum)
        discarded += float(np.sum((probability * trace)[~inside]))
        total += float(np.sum(probability * trace))
        target = basis.evaluate(final[inside])
        probability, trace, extra = probability[inside], trace[inside], extra[inside]
        conductance = probability * trace
        difference = initial[None, :] - target
        base -= .5 * (np.sum(conductance) * np.outer(initial, initial) + (target.T * conductance) @ target)
        baseline[0] -= .5 * (difference.T * conductance) @ difference
        coefficients = []
        for model in range(2):
            left, right, thermal = leading_coefficients(frequency, final[inside], initial @ profiles[model],
                target @ profiles[model], gas_temperatures[model], theta, gamma[inside])
            coefficients.append((left, right))
            mixed_base[model] -= .5 * (np.sum(conductance * left) * np.outer(initial, initial) + (target.T * (conductance * right)) @ target)
            mixed[0][model] -= .5 * (difference.T * conductance) @ (left[:, None] * initial - right[:, None] * target)
            temperature[model] -= .5 * difference.T @ (conductance * thermal)
        for degree, (first, second) in enumerate(angular):
            for source, destination in pairs[degree]:
                weight = .5 * probability * (first[source, destination, inside] + extra * second[source, destination, inside])
                source_slice = slice(source * count, (source + 1) * count)
                destination_slice = slice(destination * count, (destination + 1) * count)
                cross = np.outer(initial, weight @ target)
                baseline[degree][source_slice, destination_slice] += cross
                baseline[degree][destination_slice, source_slice] += cross.T
                for model, (left, right) in enumerate(coefficients):
                    mixed[degree][model, source_slice, destination_slice] += np.outer(initial, (weight * right) @ target)
                    mixed[degree][model, destination_slice, source_slice] += np.outer((weight * left) @ target, initial)
    for degree, channels in enumerate(names):
        if degree == 0:
            continue
        for mode in range(len(channels)):
            section = slice(mode * count, (mode + 1) * count)
            baseline[degree][section, section] += base / (2 * degree + 1)
            mixed[degree][:, section, section] += mixed_base / (2 * degree + 1)
    return baseline, mixed, temperature, discarded / total


def main(arguments):
    modest()
    folder = ROOT / 'banks' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    geometries = [ReactionGeometry(model, model + '-reaction104-6400') for model in ['heavy', 'cold']]
    basis = geometries[0].basis
    temperatures = np.array(json.loads((PARENT / 'banks/infrared104-q700/status.json').read_text())['temperatures'])
    end = geometries[0].thermal.end
    theta_start = geometries[0].at(0.)['theta']
    primary_knots = np.log(theta_start / temperatures)
    step = end / 6400
    knots = np.unique(np.r_[np.clip(primary_knots, 0., end), step * np.array([1, 4, 16, 64])])
    if arguments.point is not None:
        knots = np.array([arguments.point])
    checks, rows = [], []
    started = time.perf_counter()
    for index, expansion in enumerate(knots):
        theta = geometries[0].at(expansion)['theta']
        events = thermal_wave.prior.event_geometry(theta, 6)
        angular = []
        for degree in range(arguments.maximum + 1):
            first, second, names = thermal_wave.prior.angular_correlations(events, degree)
            retained = [names.index(name) for name in (['I'] if degree < 2 else ['I', 'E'])]
            excluded = [mode for mode in range(len(names)) if mode not in retained]
            error = max(float(np.max(abs(first[np.ix_(retained, excluded)]))), float(np.max(abs(second[np.ix_(retained, excluded)]))))
            checks.append(check('Scalar I/E parity closure knot=' + str(index) + ' degree=' + str(degree), error, 1e-12))
            angular.append((first[np.ix_(retained, retained)], second[np.ix_(retained, retained)]))
        profiles = [geometry.profiles(expansion) for geometry in geometries]
        gas_temperatures = [float(geometry.temperature(expansion)) for geometry in geometries]
        baseline, mixed, thermal, discarded = blocks_at(basis, theta, events, angular, profiles, gas_temperatures)
        payload = dict(expansion=expansion, theta=theta, temperature=thermal,
                       background_profiles=profiles, background_gas=gas_temperatures)
        for degree in range(arguments.maximum + 1):
            payload['base_' + str(degree)] = baseline[degree]
            payload['mixed_' + str(degree)] = mixed[degree]
            full_mass = linalg.block_diag(*([basis.mass / (2 * degree + 1)] * (1 if degree < 2 else 2)))
            eigenvalues = linalg.eigh(baseline[degree], full_mass, eigvals_only=True)
            checks.append(check('Physical Planck Compton dissipation knot=' + str(index) + ' degree=' + str(degree), max(0., eigenvalues.max()), 1e-9))
        for model in range(2):
            error = linalg.norm(basis.chemical @ mixed[0][model]) / max(linalg.norm(mixed[0][model]), 1e-30)
            checks.append(check('Mixed Compton photon-number left null knot=' + str(index) + ' model=' + str(model), error, 1e-10))
            error = abs(basis.chemical @ thermal[model]) / max(linalg.norm(thermal[model]), 1e-30)
            checks.append(check('Compton temperature photon-number null knot=' + str(index) + ' model=' + str(model), error, 1e-10))
        if index == 0:
            original, names, _ = physical_block(basis, theta, events, min(2, arguments.maximum))
            retained = np.r_[np.arange(basis.count), basis.count + np.arange(basis.count)] if arguments.maximum >= 2 else np.arange(basis.count)
            error = linalg.norm(original[np.ix_(retained, retained)] - baseline[min(2, arguments.maximum)]) / linalg.norm(baseline[min(2, arguments.maximum)])
            checks.append(check('Reduced assembly equals inherited full polarized operator', error, 1e-12))
        np.savez_compressed(folder / ('knot-' + str(index) + '.npz'), **payload)
        rows.append(dict(expansion=float(expansion), discarded_pair_weight=discarded))
        write_json(folder / 'progress.json', dict(state='running', knots_done=index + 1, knots_total=len(knots), elapsed=time.perf_counter() - started))
        print(json.dumps(dict(knot=index, knots=len(knots), elapsed=time.perf_counter() - started)), flush=True)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
        basis_spec=dict(count=104, quadrature=700, minimum=1e-5, maximum=60., pivot=.1),
        knots=knots.tolist(), original_temperature_knots=temperatures.tolist(), maximum_degree=arguments.maximum,
        matrices_scaled_by_heat=True, backgrounds='Stage81 matched three-photon Gould + finite-shift Compton + H/He BR histories.',
        no_number_projection=True, no_diffusion_substitution=True, elapsed=time.perf_counter() - started,
        full_finite_k_wave_evolution=False), __file__,
        [ROOT / 'reaction_geometry.py', PARENT / 'leading_pair.py', *[geometry.source for geometry in geometries],
         PARENT / 'banks/infrared104-q700/status.json', THERMAL_STAGE / 'build_spectral_kernel.py',
         BRANCH / 'polarized-heat-momentum-grid-20261007/grid_common.py'])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--maximum', type=int, default=4)
    parser.add_argument('--point', type=float)
    main(parser.parse_args())

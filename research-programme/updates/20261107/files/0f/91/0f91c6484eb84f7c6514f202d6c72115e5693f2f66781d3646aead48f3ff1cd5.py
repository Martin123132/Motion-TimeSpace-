from integrate236 import *


def moments(features, join, order, profile, config):
    floor, ceiling = config['spectral_domain']
    count = math.ceil(math.log(ceiling / floor) / config['maximum_log_width'])
    edges = np.linspace(math.log(floor), math.log(ceiling), count + 1)
    nodes, weights = np.polynomial.legendre.leggauss(order)
    middle, half = .5 * (edges[1:] + edges[:-1]), .5 * np.diff(edges)
    frequency = np.exp(middle[:, None] + half[:, None] * nodes).ravel()
    measure = (half[:, None] * weights * frequency.reshape(-1, order)).ravel()
    occupation = 1 / np.expm1(frequency)
    removed = -np.expm1(-(frequency / profile)**2)
    scalar_moment = np.dot(measure, removed * occupation / frequency)
    coordinate = (measure * removed * occupation * (1 + occupation) / frequency) @ features.evaluate(frequency, join)
    return scalar_moment, coordinate


def main():
    modest()
    config, frozen = run_protocol()
    original, features, models = setup(config)
    checks, records = [], []
    original_maps = packet(PARENT / 'results/soft-profile-maps.npz')
    moment_data = {(join, order, profile): moments(features, join, order, profile, config)
        for join in (0, 1) for order in frozen['orders'] for profile in (.2, .5)}
    with mp.workdps(80):
        for row in config['events']:
            parameters, event_weight = source.physics.parameters_and_weight(row['theta'], row['node'])
            totals = {(join, degree, order, profile): np.zeros((7, 98, 99))
                for join in (0, 1) for degree in (0, 1, 2) for order in frozen['orders'] for profile in (.2, .5)}
            for ray_index, (direction, angular_weight) in enumerate(angular.inherited.source.angular_nodes(4)):
                owner = Direction(precise_context(parameters), direction)
                factors = Factors(owner, features, models[0]['difference'].tests, config['states'], config['heat'])
                old_gram = models[0]['control'].gram(np.array(list(map(float, owner.hard_direction))), np.array(list(map(float, owner.direction))))
                check(checks, f'{row["label"]}:ray{ray_index}:original leading rational Gram', relative(np.array(owner.gram.tolist(), dtype=float), old_gram))
                for mode in ('control', 'difference'):
                    check(checks, f'{row["label"]}:ray{ray_index}:{mode}:original pole',
                        abs(float(owner.pole[mode]) - models[0][mode].poles(parameters, direction)) / max(abs(float(owner.pole[mode])), 1e-300), 1e-7)
                emission, unused, local_temperature = upper_limits(owner)
                gauss, weights = np.polynomial.legendre.leggauss(18)
                for fraction in frozen['separator_fractions']:
                    interval = -mp.log(scalar(fraction))
                    quadrature = float(interval) * np.sum(weights) / 2
                    check(checks, f'{row["label"]}:ray{ray_index}:separator{fraction}:subtraction plus logarithm', abs(quadrature + float(mp.log(scalar(fraction)))))
                for join in (0, 1):
                    for degree in (0, 1, 2):
                        left = factors.left[degree]
                        right = np.array(factors.right[join, degree])
                        for order in frozen['orders']:
                            for profile in (.2, .5):
                                moment, coordinate = moment_data[join, order, profile]
                                projected_moment = np.vstack([coordinate[:, None] * factors.harmonics[degree][2], np.zeros((1, left.shape[-1]))])
                                correction = moment * right
                                for state in range(1, 7):
                                    background = float(state235.contraction(coordinate, factors.physical[state - 1][:98]))
                                    correction[state] += background * right[0] + float(factors.coefficients[join][state]['density']) * projected_moment
                                scale = event_weight * angular_weight * float(owner.pole['full']) / (2 * degree + 1)
                                totals[join, degree, order, profile] += scale * np.einsum('ai,vbi->vab', left, correction, optimize=True)
            for join in (0, 1):
                for degree in (0, 1, 2):
                    for profile in (.2, .5):
                        for state_index, history in enumerate(config['states']):
                            prefix = f'{row["label"]}:join{join}:state{state_index}:l{degree}:profile{profile}'
                            reference = -original_maps[prefix + ':profile_conversion_change']
                            before = totals[join, degree, 18, profile][state_index + 1]
                            after = totals[join, degree, 26, profile][state_index + 1]
                            error = relative(after, reference)
                            check(checks, prefix + ':independent subtraction/profile cancellation', error, config['refinement_tolerance'])
                            check(checks, prefix + ':log-panel profile refinement', relative(before, after), config['refinement_tolerance'])
                            records.append(dict(anchor=row['label'], join=join, degree=degree, profile=profile,
                                model=history['model'], history=history['history'], cancellation=error, refinement=relative(before, after)))
            print(json.dumps(dict(anchor=row['label'], checks=len(checks), failed=sum(not value['passed'] for value in checks))), flush=True)
    failures = [row for row in checks if not row['passed']]
    write(ROOT / 'results/matching.json', dict(qualified=not failures, checks=checks, failed=failures, records=records,
        script_sha256=digest(Path(__file__)), saved_profile_reference_sha256=digest(PARENT / 'results/soft-profile-maps.npz'),
        finished_at=now(), scope='Original leading control and poles; independent full-basis finite-domain profile and separator shifts'))
    print(json.dumps(dict(checks=len(checks), failed=len(failures), examples=failures[:5], maximum_cancellation=max(row['cancellation'] for row in records))), flush=True)
    assert not failures


if __name__ == '__main__':
    main()

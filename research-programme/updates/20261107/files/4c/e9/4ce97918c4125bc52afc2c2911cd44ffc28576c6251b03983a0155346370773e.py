import argparse
from mixed_common import *
from stable_pair import coefficients


def background_profile(system, expansion):
    local = system.background(expansion)
    profile = system.geometry.profiles(expansion).copy()
    vectors = np.column_stack([system.basis.chemical, system.basis.temperature])
    moments = np.vstack([system.basis.number, system.basis.energy])
    profile += vectors @ linalg.solve(moments @ vectors,
                                     [-system.basis.number @ profile,
                                      local['photon_energy_scaled'] - system.basis.energy @ profile])
    shift = local['physical_heat'] * float(system.geometry.temperature(expansion))
    return profile, shift, local['physical_heat']


def physical_mixed(basis, theta, events, gamma, angular, degree, backgrounds):
    first, second, names = angular
    count, modes = basis.count, len(names)
    blocks = np.zeros((len(backgrounds), modes * count, modes * count))
    base = np.zeros((len(backgrounds), count, count))
    temperature = np.zeros((len(backgrounds), count))
    residual = np.zeros_like(temperature)
    total, discarded = 0., 0.
    pairs = [(left, right) for left in range(modes) for right in range(modes)
             if max(np.max(abs(first[left, right])), np.max(abs(second[left, right]))) > 1e-14
             and not (degree == 0 and left == right == 0)]
    for frequency, measure, initial in zip(basis.nodes, basis.measure / 2, basis.values):
        recoil = 1 / (1 + theta * frequency * events['incident'] * (1 - events['cosine']))
        extra = (1 - recoil) ** 2 / recoil
        final = frequency * events['incident'] * recoil * events['outgoing']
        bose = (1 + 1 / np.expm1(final)) / (1 + 1 / np.expm1(frequency))
        probability = measure * events['weight'] * 1.5 * recoil ** 2 * bose
        trace = (1 + events['cosine'] ** 2 + extra) / (2 * degree + 1)
        inside = (final >= basis.minimum) & (final <= basis.maximum)
        discarded += float(np.sum((probability * trace)[~inside]))
        total += float(np.sum(probability * trace))
        target = basis.evaluate(final[inside])
        probability, trace, extra = probability[inside], trace[inside], extra[inside]
        conductance = probability * trace
        difference = initial[None, :] - target
        for model, (profile, shift, heat) in enumerate(backgrounds):
            left, right, thermal, defect = coefficients(frequency, final[inside], initial @ profile,
                                                       target @ profile, heat, shift, theta, gamma[inside])
            left, right, thermal, defect = left / heat, right / heat, thermal / heat, defect / heat ** 2
            base[model] -= .5 * (np.sum(conductance * left) * np.outer(initial, initial)
                                + (target.T * (conductance * right)) @ target)
            if degree == 0:
                blocks[model, :count, :count] -= .5 * (difference.T * conductance) @ (
                    left[:, None] * initial - right[:, None] * target)
                temperature[model] -= .5 * difference.T @ (conductance * thermal)
                residual[model] -= .5 * difference.T @ (conductance * defect)
            for source, destination in pairs:
                weight = .5 * probability * (first[source, destination, inside] + extra * second[source, destination, inside])
                source_slice = slice(source * count, (source + 1) * count)
                destination_slice = slice(destination * count, (destination + 1) * count)
                blocks[model, source_slice, destination_slice] += np.outer(initial, (weight * right) @ target)
                blocks[model, destination_slice, source_slice] += np.outer((weight * left) @ target, initial)
    for model in range(len(backgrounds)):
        for mode in range(modes):
            if degree == 0 and mode == 0:
                continue
            section = slice(mode * count, (mode + 1) * count)
            blocks[model, section, section] += base[model]
    return blocks, temperature, residual, discarded / total


def main(arguments):
    modest()
    folder = ROOT / 'banks' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    systems = [RefinedSystem(model, 24, 8) for model in ['heavy', 'cold']]
    basis = systems[0].basis
    end = systems[0].geometry.thermal.end
    step = end / 3200
    knots = np.unique(np.r_[np.linspace(0., end, arguments.intervals + 1), step * np.array([1, 4, 16, 64])])
    if arguments.point is not None:
        knots = np.array([arguments.point])
    checks, rows = [], []
    started = time.perf_counter()
    for index, expansion in enumerate(knots):
        theta = systems[0].background(expansion)['theta']
        backgrounds = [background_profile(system, expansion) for system in systems]
        contents = dict(expansion=expansion, theta=theta, heat=backgrounds[0][2])
        for order in sorted(set([arguments.event_order, max(8, arguments.event_order)])):
            events = grid.event_geometry(theta, order)
            speeds, _ = grid.prior.juttner_rule(theta, order)
            gamma = np.repeat(1 / np.sqrt(1 - speeds ** 2), 2 * order ** 3)
            assert len(gamma) == len(events['weight'])
            for degree in range(9):
                if order != (max(8, arguments.event_order) if degree == 8 else arguments.event_order):
                    continue
                angular = grid.angular_correlations(events, degree)
                blocks, thermal, residual, discarded = physical_mixed(basis, theta, events, gamma, angular, degree, backgrounds)
                contents['block_' + str(degree)] = blocks
                if degree == 0:
                    contents.update(temperature=thermal, residual=residual)
                    error = max(float(np.linalg.norm(basis.chemical @ block[:24]) / max(np.linalg.norm(block), 1e-100)) for block in blocks)
                    checks.append(dict(name='Left photon-number null at knot' + str(index), passed=error < 1e-10, value=error))
                    for name, values in [('temperature', thermal), ('residual', residual)]:
                        error = max(float(abs(basis.chemical @ value) / max(np.linalg.norm(value), 1e-100)) for value in values)
                        checks.append(dict(name=name + ' conserves photon number knot' + str(index), passed=error < 1e-10, value=error))
                checks.append(dict(name='Finite mixed block knot' + str(index) + ' degree' + str(degree), passed=bool(np.isfinite(blocks).all())))
                rows.append(dict(knot=index, degree=degree, event_order=order, discarded_reference_weight=discarded))
        np.savez_compressed(folder / ('knot-' + str(index) + '.npz'), **contents)
        print(json.dumps(dict(knot=index, knots=len(knots), elapsed=time.perf_counter() - started)), flush=True)
        write_json(folder / 'progress.json', dict(state='running', completed=index + 1, knots=len(knots), elapsed=time.perf_counter() - started))
    finish(folder, dict(checks=checks, all_checks_passed=all(row['passed'] for row in checks), count=len(checks),
                        knots=knots.tolist(), basis_count=24, quadrature_count=len(basis.nodes), event_order=arguments.event_order,
                        blocks_scaled_by_heat=True, residual_scaled_by_heat_squared=True, rows=rows,
                        backgrounds='Both Stage75 24-function conservative trajectories; exact finite-heat coefficients.',
                        elapsed=time.perf_counter() - started), __file__,
           [ROOT / 'stable_pair.py', PARENT / 'stable_spectral_basis.py', GRID / 'grid_common.py',
            *[system.geometry.source for system in systems]])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--intervals', type=int, default=16)
    parser.add_argument('--event-order', type=int, default=6)
    parser.add_argument('--point', type=float)
    main(parser.parse_args())

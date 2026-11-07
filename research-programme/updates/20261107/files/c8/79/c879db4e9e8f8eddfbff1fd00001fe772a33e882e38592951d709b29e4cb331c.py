import argparse
from inclusive_soft import *
from polarized_soft_pole import weighted_angular


def cusp_array(invariant):
    speed2 = invariant * (2 + invariant) / (1 + invariant) ** 2
    small = speed2 < .0025
    result = np.empty_like(speed2)
    result[small] = sum(speed2[small] ** power / (2 * power + 1) for power in range(1, 10))
    speed = np.sqrt(speed2[~small])
    result[~small] = np.arctanh(speed) / speed - 1
    return 2 * ALPHA / math.pi * result


def all_blocks(basis, theta, maximum):
    events = thermal_wave.prior.event_geometry(theta, 6)
    angular = [thermal_wave.prior.angular_correlations(events, degree) for degree in range(maximum + 1)]
    blocks = [np.zeros((len(names) * basis.count, len(names) * basis.count)) for first, second, names in angular]
    names_by_degree = [names for first, second, names in angular]
    pairs = [[(left, right) for left in range(len(names)) for right in range(len(names))
        if max(np.max(abs(first[left, right])), np.max(abs(second[left, right]))) > 1e-14 and not (degree == 0 and left == right == 0)]
        for degree, (first, second, names) in enumerate(angular)]
    base = np.zeros_like(basis.mass)
    pole_factor = 4 * ALPHA / (3 * math.pi) * theta ** 2
    discarded, total = 0., 0.
    for frequency, measure, initial in zip(basis.nodes, basis.measure / 2, basis.values):
        rest_energy = theta * frequency * events['incident']
        ratio = 1 / (1 + rest_energy * (1 - events['cosine']))
        extra = (1 - ratio) ** 2 / ratio
        final = frequency * events['incident'] * ratio * events['outgoing']
        invariant = rest_energy ** 2 * (1 - events['cosine']) * ratio
        current_weight = 2 * cusp_array(invariant) / pole_factor
        bose = (1 + 1 / np.expm1(final)) / (1 + 1 / np.expm1(frequency))
        probability = measure * events['weight'] * 1.5 * ratio ** 2 * bose * current_weight
        trace = 1 + events['cosine'] ** 2 + extra
        inside = (final >= basis.minimum) & (final <= basis.maximum)
        discarded += float(np.sum((probability * trace)[~inside]))
        total += float(np.sum(probability * trace))
        target = basis.evaluate(final[inside])
        probability, trace, extra = probability[inside], trace[inside], extra[inside]
        conductance = probability * trace
        difference = initial[None, :] - target
        base -= .5 * (np.sum(conductance) * np.outer(initial, initial) + (target.T * conductance) @ target)
        blocks[0][:basis.count, :basis.count] -= .5 * (difference.T * conductance) @ difference
        for degree, (first, second, names) in enumerate(angular):
            for left, right in pairs[degree]:
                weight = .5 * probability * (first[left, right, inside] + extra * second[left, right, inside])
                cross = np.outer(initial, weight @ target)
                source, destination = slice(left * basis.count, (left + 1) * basis.count), slice(right * basis.count, (right + 1) * basis.count)
                blocks[degree][source, destination] += cross
                blocks[degree][destination, source] += cross.T
    for degree, names in enumerate(names_by_degree):
        for mode in range(len(names)):
            if degree == 0 and mode == 0:
                continue
            section = slice(mode * basis.count, (mode + 1) * basis.count)
            blocks[degree][section, section] += base / (2 * degree + 1)
    return blocks, names_by_degree, discarded / total


def main(arguments):
    modest()
    folder = ROOT / 'banks' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    specification = dict(count=104, quadrature=700, minimum=1e-5, maximum=60., pivot=.1)
    basis = ConsistentBasis(**specification)
    background = thermal_wave.thermal.ThermalBackground('heavy')
    checks, rows = [], []
    started = time.perf_counter()
    for index, expansion in enumerate([0., math.log(10) / 2, math.log(10)]):
        theta = background.theta0 / (background.start_scale * math.exp(expansion))
        blocks, names, discarded = all_blocks(basis, theta, arguments.maximum)
        rayleighs = []
        payload = dict(theta=theta, expansion=expansion)
        for degree, block in enumerate(blocks):
            mass = linalg.block_diag(*([basis.mass / (2 * degree + 1)] * len(names[degree])))
            eigenvalues = linalg.eigh(block, mass, eigvals_only=True)
            checks.append(check('Exact-event soft pole dissipation theta=' + str(theta) + ' l=' + str(degree), max(0., max(eigenvalues)) / max(abs(eigenvalues)), 1e-11))
            if degree == 0:
                chemical = np.r_[basis.chemical, np.zeros((len(names[degree]) - 1) * basis.count)]
                checks.append(check('Hard-process photon number null theta=' + str(theta), linalg.norm(block @ chemical) / linalg.norm(block), 1e-11))
            template = np.r_[basis.temperature, np.zeros((len(names[degree]) - 1) * basis.count)]
            rayleighs.append(float(-template @ block @ template / (template @ mass @ template)))
            payload['real_' + str(degree)] = block
            payload['virtual_' + str(degree)] = -block
        np.savez_compressed(folder / ('knot-' + str(index) + '.npz'), **payload)
        rows.append(dict(expansion=expansion, theta=theta, temperature_rayleighs=rayleighs, discarded_pair_weight=discarded))
        print(json.dumps(dict(knot=index, elapsed=time.perf_counter() - started, row=rows[-1])), flush=True)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
        basis_spec=specification, event_order=6, maximum_degree=arguments.maximum,
        pole_scope='Inclusive unresolved hard-process pole only; NOT the physical resolved soft-photon creation/loss operator.',
        scalar_14_16_correction_used=False, finite_shift_compton_event_weights_used=True,
        normalization='Multiply stored real/virtual matrices by [4alpha/(3pi)] theta_star^2/xmin. Same-event virtual sign follows sourced soft unitarity.',
        complete_finite_loop=False, thermal_soft_bath=True, arbitrary_nonthermal_soft_slope_not_assumed=True,
        elapsed=time.perf_counter() - started), __file__,
        [ROOT / 'inclusive_soft.py', ROOT / 'polarized_soft_pole.py', ROOT / 'sources/hep-ph-9308249.html',
         BRANCH / 'polarized-heat-momentum-grid-20261007/grid_common.py',
         BRANCH / 'expanding-thermal-gravity-20261007/build_spectral_kernel.py',
         PARENT / 'banks/matched104-l4/status.json', PARENT / 'results/matched-integrated-parity/status.json',
         background.parent.source, background.native_constants])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', default='finite-shift-soft104-l4')
    parser.add_argument('--maximum', type=int, default=4)
    main(parser.parse_args())

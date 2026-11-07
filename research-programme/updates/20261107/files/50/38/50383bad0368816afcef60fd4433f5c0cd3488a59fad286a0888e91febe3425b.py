from weak_common import *


def directional_split(initial, incoming, outgoing, first_pol, second_pol, direction, temperature):
    dressed = source.dressed
    exact = source.exact
    coefficients = dressed.radial_decomposition(initial, incoming, outgoing, first_pol, second_pol, direction)
    final = initial + incoming - outgoing
    null = exact.photon(exact.mp.mpf(1), direction)
    principal = coefficients['constant'] * temperature**2 * exact.mp.pi**2 / 6
    absorptive = exact.mp.zeros(4)
    for pole in coefficients['poles']:
        scaled = pole['location'] / temperature
        hilbert = (exact.mp.log(scaled / (2 * exact.mp.pi))
                   - exact.mp.re(exact.mp.digamma(exact.mp.j * scaled / (2 * exact.mp.pi)))) / 2
        principal += pole['coefficient'] * hilbert
        absorptive += pole['coefficient'] * (-exact.mp.j * exact.mp.pi
                       * pole['denominator_slope_sign'] / (2 * exact.mp.expm1(scaled)))
    left = exact.spinors(final).transpose_conj() * exact.gamma_matrices()[0]
    right = exact.spinors(initial)
    principal = left * principal * right
    principal += dressed.external_finite_constant(initial, incoming, outgoing,
                    first_pol, second_pol, null) * temperature**2 * exact.mp.pi**2 / 6
    return principal, left * absorptive * right


def evaluate(parameters, directions):
    exact = source.exact
    exact.mp.mp.dps = 60
    energy = exact.mp.mpf(str(parameters['energy']))
    cosine = exact.mp.mpf(str(parameters['cosine']))
    initial = exact.mp.matrix([1, 0, 0, 0])
    incoming = exact.photon(energy, exact.mp.matrix([0, 0, 1]))
    hard_direction = exact.mp.matrix([exact.mp.sqrt(1 - cosine**2), 0, cosine])
    outgoing = exact.photon(energy / (1 + energy * (1 - cosine)), hard_direction)
    frames = [exact.frame(exact.mp.matrix([0, 0, 1])), exact.frame(hard_direction)]
    bath = exact.mp.matrix([exact.mp.mpf(str(value)) for value in parameters['bath']])
    temperature = exact.mp.mpf(str(parameters['temperature']))
    tree, response, normalized = source.tree_map(parameters)
    principal_total = np.zeros_like(tree, dtype=complex)
    absorptive_total = np.zeros_like(tree, dtype=complex)
    rows = []
    prefactor = 4 * exact.mp.pi * exact.mp.mpf(str(source.ALPHA)) / (2 * (2 * exact.mp.pi)**3)
    for index, (direction, measure) in enumerate(directions):
        unit = exact.unit(direction)
        local_temperature = temperature / exact.dot(bath, exact.photon(exact.mp.mpf(1), unit))
        principal_tensor = np.zeros_like(tree, dtype=complex)
        absorptive_tensor = np.zeros_like(tree, dtype=complex)
        reconstruction_error = exact.mp.mpf(0)
        scalar_absorptive = exact.mp.mpf(0)
        scalar_norm = exact.mp.mpf(0)
        for first, second in source.itertools.product([0, 1], repeat=2):
            principal, absorptive = directional_split(initial, incoming, outgoing,
                            frames[0][first], frames[1][second], unit, local_temperature)
            original = source.dressed.finite_dressed(initial, incoming, outgoing,
                            frames[0][first], frames[1][second], unit, local_temperature)
            reconstruction_error = max(reconstruction_error, exact.mp.norm(original - principal - absorptive)
                                       / max(exact.mp.norm(original), exact.mp.mpf('1e-80')))
            amplitude = (exact.spinors(initial + incoming - outgoing).transpose_conj()
                         * exact.gamma_matrices()[0]
                         * source.dressed.compton(initial, incoming, outgoing, frames[0][first], frames[1][second])
                         * exact.spinors(initial))
            scalar_absorptive += 2 * exact.mp.re(sum(exact.mp.conj(amplitude[row, column]) * absorptive[row, column]
                                                   for row in range(2) for column in range(2)))
            scalar_norm += exact.mp.norm(amplitude) * exact.mp.norm(absorptive)
            for final_spin, initial_spin in source.itertools.product([0, 1], repeat=2):
                principal_tensor[first, second, final_spin, initial_spin] = complex(prefactor * principal[final_spin, initial_spin])
                absorptive_tensor[first, second, final_spin, initial_spin] = complex(prefactor * absorptive[final_spin, initial_spin])
        principal_total += measure * principal_tensor
        absorptive_total += measure * absorptive_tensor
        rows.append(dict(direction=list(map(float, direction)),
                         reconstruction_error=float(reconstruction_error),
                         scalar_absorptive_fraction=float(abs(scalar_absorptive) / max(scalar_norm, exact.mp.mpf('1e-80')))))
    return dict(principal_tensor=principal_total, absorptive_tensor=absorptive_total,
                principal_map=source.interference(tree, principal_total) / response[0, 0],
                absorptive_map=source.interference(tree, absorptive_total) / response[0, 0],
                rows=rows)


def main():
    modest()
    folder = ROOT / 'results/absorptive-scalar-projection'
    folder.mkdir(parents=True, exist_ok=False)
    temperature = .00045962015785263325
    parameters = source.context(temperature, .1, [.02, .005, -.01], temperature)
    started = time.monotonic()
    result = evaluate(parameters, list(source.angular_nodes(4)))
    parent_file = BRANCH / 'moving-polarized-thermal-20261008/results/moving-a6-r40-v8/source.npz'
    with np.load(parent_file) as saved:
        expected = saved['virtual'].copy()
    checks = [
        check('PV plus absorptive pole split reconstructs original directional amplitude',
              max(row['reconstruction_error'] for row in result['rows']), 1e-45),
        check('Absorptive scalar trace vanishes before thermal angular averaging',
              max(row['scalar_absorptive_fraction'] for row in result['rows']), 1e-45),
        check('Split angular4 map reproduces inherited angular8 map',
              relative(result['principal_map'] + result['absorptive_map'], expected), 1e-6),
        check('PV scalar equals full inherited intensity interference',
              abs(result['principal_map'][0, 0] / expected[0, 0] - 1), 1e-6),
        dict(name='Absorptive polarization response is retained rather than declared zero',
             passed=bool(np.linalg.norm(result['absorptive_map']) > abs(expected[0, 0]) * .01))]
    np.savez(folder / 'split.npz', **{key: value for key, value in result.items() if key != 'rows'})
    finish(folder, dict(checks=checks, count=len(checks),
           all_checks_passed=all(row['passed'] for row in checks), rows=result['rows'],
           elapsed_seconds=time.monotonic() - started,
           principal_map=result['principal_map'].tolist(), absorptive_map=result['absorptive_map'].tolist(),
           scope='Scalar unpolarized one-loop rate: absorptive interference vanishes; full polarized kinetic generator not inferred.'),
           __file__, [parent_file, parent_file.parent / 'status.json'])
    print(json.dumps(dict(seconds=time.monotonic() - started,
                         failed=[row for row in checks if not row['passed']],
                         principal_scalar=float(result['principal_map'][0, 0]),
                         absorptive_norm=float(np.linalg.norm(result['absorptive_map'])))), flush=True)


if __name__ == '__main__':
    main()

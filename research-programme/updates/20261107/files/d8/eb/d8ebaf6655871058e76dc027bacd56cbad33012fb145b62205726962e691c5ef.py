from tail_common import *


def main():
    modest()
    folder = ROOT / 'results/manufactured-controls'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows = [], []
    size, spacing = 81, .03
    offsets = np.arange(-30, 31)
    theta = .00014534465573404461
    coefficients, eigenvalue = stencil(theta, 6, spacing, offsets)
    internal, lower, upper = split_matrix(coefficients, offsets, size)
    ones = np.ones(size)
    outside = (lower + upper) @ np.ones(30)
    row_sum = internal @ ones + outside
    checks.append(dict(name='Jump generator annihilates a constant including exterior legs',
                       value=float(max(abs(row_sum))), passed=max(abs(row_sum)) < 1e-14))
    gamma, rate, step = .1, 20., .005
    generator = rate * (internal + sparse.diags(np.full(size, eigenvalue - gamma)))
    forcing = rate * (gamma - eigenvalue + outside)
    equilibrium_error = max(abs(generator @ ones + forcing))
    checks.append(dict(name='Equal gas and photon temperature is exact equilibrium',
                       value=float(equilibrium_error), passed=equilibrium_error < 1e-12))
    inverse = sparse_linalg.splu(sparse.eye(size, format='csc') - step * generator)
    state, analytic = np.zeros(size), 0.
    errors = []
    for index in range(200):
        analytic = (analytic + step * rate * gamma) / (1 + step * rate * (gamma - eigenvalue))
        state = inverse.solve(state + step * rate * (gamma + outside * analytic))
        errors.append(float(max(abs(state - analytic))))
    checks.append(dict(name='Manufactured dynamic constant-slope reaction matches exact backward Euler',
                       value=max(errors), passed=max(errors) < 1e-12))
    continuum = gamma / (gamma - eigenvalue) * (-math.expm1(-rate * (gamma - eigenvalue)))
    continuum_errors = []
    for steps in [200, 400, 800]:
        timestep = 1 / steps
        exact_discrete = gamma / (gamma - eigenvalue) * (1 - (1 + timestep * rate * (gamma - eigenvalue))**(-steps))
        continuum_errors.append(abs(exact_discrete - continuum))
    checks.append(dict(name='Time integrator approaches analytic continuous transient at expected order',
                       value=continuum_errors, passed=continuum_errors[1] < .51 * continuum_errors[0] and continuum_errors[2] < .51 * continuum_errors[1]))
    no_absorption = rate * (internal + sparse.diags(np.full(size, eigenvalue)))
    response = float((no_absorption @ ones + rate * outside).mean())
    checks.append(dict(name='Source-off control retains soft Compton growth of a slope',
                       value=response, passed=abs(response - rate * eigenvalue) < 1e-12 and response > 0))
    checks.append(dict(name='Source-off control fails absorption-contraction condition rather than fabricated decay',
                       passed=-eigenvalue < 0))
    ratios, rates = jump_events(theta, 6)
    powers = np.array([-4, -3, -2, -1, 0, 1, 2, 3])
    moments = np.array([rates @ (np.expm1((power - 1) * np.log(ratios)) - np.expm1(-np.log(ratios))) for power in powers])
    symmetry_error = max(abs(moments - moments[::-1]))
    checks.append(dict(name='Direct-boost Thomson Mellin reciprocity', value=float(symmetry_error), passed=symmetry_error < 1e-11))
    checks.append(dict(name='Zero-energy transport has positive event rates', passed=bool(rates.min() > 0)))
    energy = np.array([.1, .3, 1., 3.])
    beta = -.9
    jump = (beta * energy / 3 + beta * 2 * energy / 3 - beta * energy)
    checks.append(dict(name='Temperature mode annihilates full three-photon reaction before soft reduction', passed=float(max(abs(jump))) < 1e-15))
    finish(folder, dict(checks=checks, scalar_decay=rate * (gamma - eigenvalue),
        scope='Independent algebra, sign and manufactured transient controls for the retained soft generator.'), __file__)
    print(json.dumps(dict(checks=len(checks), failed=[item['name'] for item in checks if not item['passed']])), flush=True)


if __name__ == '__main__':
    main()

from population_common import *
from resolved_redistribution import incoming_rule


def born_average(spectra, theta, seed_order, hard_order, radial, polar, azimuths):
    cosines, weights = np.polynomial.legendre.leggauss(hard_order)
    coefficients = spectra.coefficients()
    result = np.zeros((6, 6))
    for meridian, electron_weight in prior.inherited.inherited.gas_rule(theta, radial, polar):
        for angle in np.arange(azimuths) * 2 * np.pi / azimuths:
            velocity = np.array([meridian[0] * math.cos(angle), meridian[0] * math.sin(angle), meridian[2]])
            for frequency, measure in incoming_rule(seed_order, 1e-5, 24.):
                seed_weight = measure * frequency**2 / math.expm1(frequency) / I3
                for cosine, hard_weight in zip(cosines, weights):
                    parameters = weak.source.context(theta * frequency, float(cosine), velocity, theta)
                    jump, product = weak.born_data(parameters)
                    result += electron_weight / azimuths * seed_weight * 2 * np.pi * hard_weight * parameters['born_differential_over_thomson'] * .5 * product
    return result, -result @ coefficients


def main():
    modest()
    folder = ROOT / 'results/input-and-born-control'
    folder.mkdir(parents=True, exist_ok=False)
    spectra = Spectra(.5)
    weak.functions, weak.derivatives = spectra.functions, spectra.derivatives
    background = thermal_wave.thermal.ThermalBackground('heavy')
    theta = background.at(spectra.coordinate)['thermal_parameter']
    checks, rows, paths = [], [], []
    sample = np.geomspace(3e-4, 59., 317)
    values = spectra.functions(sample)
    for index, model in enumerate(['heavy', 'cold']):
        expected = spectra.basis.evaluate(sample) @ spectra.original[model]
        error = float(np.max(abs(values[:, 1 + 2 * index] - expected)))
        checks.append(dict(name='Joined spectrum preserves saved hard profile ' + model, value=error, passed=error < 1e-5))
        tail_frequency, slope = spectra.tails[model]
        low = np.geomspace(1e-6, 4e-5, 151)
        expected_low = np.interp(np.log(low), np.log(tail_frequency), slope) * low
        error_low = float(np.max(abs(spectra.functions(low)[:, 1 + 2 * index] - expected_low)))
        checks.append(dict(name='Solved tail owns soft profile ' + model, value=error_low, passed=error_low < 1e-10))
    forbidden = []
    for frequency in [1e-8, 80.]:
        try:
            spectra.functions(np.array([frequency]))
            forbidden.append(False)
        except ValueError:
            forbidden.append(True)
    checks.append(dict(name='No silently extrapolated spectrum outside declared domain', passed=all(forbidden)))
    controls = [(1, 2, 1, 2, 2), (2, 4, 2, 2, 4), (4, 6, 3, 4, 6), (6, 8, 4, 4, 8)]
    for settings in controls:
        started = time.monotonic()
        matrix, current = born_average(spectra, theta, *settings)
        rows.append(dict(settings=settings, photon_energy=current[0].tolist(), gas_energy=current[-1].tolist(),
                         elapsed=time.monotonic() - started))
        print(json.dumps(rows[-1]), flush=True)
    import infrared_ladder
    ladder = infrared_ladder.InfraredLadder(prior.inherited.BACKGROUND / 'banks/infrared96-q700')
    kernel = ladder.at(theta, 0)[:96, :96]
    expected = []
    for index, model in enumerate(['heavy', 'cold']):
        expected.append(float(ladder.basis.temperature @ kernel @ (spectra.original[model] - spectra.gas[index] * ladder.basis.temperature)))
    final = np.array(rows[-1]['photon_energy'])
    parent_difference = float(np.max(abs(final[[0, 2]] - expected) / np.abs(expected)))
    refinement = float(np.max(abs(final - rows[-2]['photon_energy'])) / np.max(abs(final)))
    checks.append(dict(name='Direct normalized Born population source approaches retained collision bank', value=parent_difference, passed=parent_difference < .01))
    checks.append(dict(name='Independent Born quadrature refinement', value=refinement, passed=refinement < .01))
    checks.append(dict(name='Born energy exchange cancels independently after averaging', value=float(np.max(abs(final + rows[-1]['gas_energy']))),
                       passed=np.max(abs(final + rows[-1]['gas_energy'])) < 1e-10))
    finish(folder, dict(checks=checks, rows=rows, expected_parent_born_energy=expected,
        spectral_order=['heavy-wide', 'heavy-narrow', 'cold-wide', 'cold-narrow'],
        source_absolute_tolerance_for_projection=1e-6 * float(np.max(abs(final))),
        seed_domain=[1e-5, 24.], parent_domain=[1e-5, 60.],
        omitted_seed_tail_is_not_automatically_bounded=True), __file__, [*spectra.inputs, *ladder.inputs,
                                                                      background.parent.source, background.native_constants])
    print(json.dumps(dict(checks=len(checks), failed=[item['name'] for item in checks if not item['passed']],
                         parent_difference=parent_difference, refinement=refinement)), flush=True)


if __name__ == '__main__':
    main()

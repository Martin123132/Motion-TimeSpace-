from observer_common import *
from spectral_readout import SpectralReadout, spectral_norm


def main():
    modest()
    folder = ROOT / 'results/projection-identities'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows, inputs = [], [], []
    random = np.random.default_rng(771307)
    for model in ['heavy', 'cold']:
        system = MixedSystem(model, 24, 8, 'event8')
        readout = SpectralReadout(system)
        basis = system.basis
        inputs.extend(readout.inputs)
        for expansion in [0., .1, 1., system.geometry.thermal.end]:
            background = readout.background(expansion)
            dilation, age = background['dilation'], background['age']
            state = random.normal(size=system.size) * 1e-3 + 1j * random.normal(size=system.size) * 1e-3
            result = readout.apply(expansion, state)
            changed = readout.apply(expansion, readout.transform(expansion, state, 2e-3 + 1e-3j, -3e-3))
            gauge_error = float(max(np.max(abs(result[key] - changed[key])) for key in ['temperatures', 'shapes', 'relational']))
            original = np.asarray([state[system.mode_slice(degree, name)] for degree, names in enumerate(system.names) for name in names])
            inversion_error = float(np.max(abs(readout.reconstruct(result) - original)))
            moment_error = float(np.max(abs(result['shapes'] @ basis.number)))
            boundary_error = float(linalg.norm(background['weak_change'] - background['dilation_change']
                                                - system.mass_inverse @ background['boundary'])
                                   / max(linalg.norm(background['dilation_change']), 1e-30))
            thermal_state = np.zeros(system.size, complex)
            thermal_state[system.mode_slice(0)] = .003 * dilation
            thermal_state[system.mode_slice(1)] = -.004 * dilation
            thermal_state[9] = -.004
            pure = readout.apply(expansion, thermal_state)
            checks.extend([
                dict(name=model + ':' + str(expansion) + ': passive time/frame transformations leave readout invariant', passed=gauge_error < 1e-12, value=gauge_error),
                dict(name=model + ':' + str(expansion) + ': exact reconstruction keeps clock velocity and all modes', passed=inversion_error < 1e-12, value=inversion_error),
                dict(name=model + ':' + str(expansion) + ': shape has zero number moment without erasing energy', passed=moment_error < 1e-12, value=moment_error),
                dict(name=model + ':' + str(expansion) + ': physical strong dilation equals weak dilation minus finite-band flux', passed=boundary_error < 1e-7, value=boundary_error),
                dict(name=model + ':' + str(expansion) + ': pure dilation and comoving dipole produce zero distortion', passed=float(np.max(abs(pure['shapes']))) < 1e-12)])
            if expansion:
                wrong = state[system.mode_slice(0)] - basis.temperature * (basis.number @ state[system.mode_slice(0)]) / (basis.number @ basis.temperature)
                shifted = readout.transform(expansion, state, .02, 0.)
                wrong_shifted = shifted[system.mode_slice(0)] - basis.temperature * (basis.number @ shifted[system.mode_slice(0)]) / (basis.number @ basis.temperature)
                omitted_age = float(linalg.norm(wrong_shifted - wrong))
                negative = readout.apply(expansion, thermal_state)
                planck_only = thermal_state[system.mode_slice(0)] - .003 * basis.temperature
                fake_shape = float(linalg.norm(planck_only))
                rows.append(dict(model=model, expansion=expansion, clock_omission_change=omitted_age,
                                 planck_tangent_only_fake_shape=fake_shape,
                                 finite_band_boundary_fraction=float(linalg.norm(background['boundary']) / max(linalg.norm(background['dilation_change']), 1e-30))))
                checks.append(dict(name=model + ':' + str(expansion) + ': wrong Planck-only coordinate projection fails omission control',
                                   passed=omitted_age > 1e-13 and fake_shape > 1e-13))
        beta = float((basis.number @ basis.temperature) / (basis.number @ basis.chemical))
        chemical_distortion = basis.temperature / beta - basis.chemical
        temperature, kept = readout.split(chemical_distortion, basis.temperature)
        old_vectors = np.column_stack([basis.chemical, basis.temperature])
        old_moments = np.vstack([basis.number, basis.energy])
        old_erasure = chemical_distortion - old_vectors @ linalg.solve(old_moments @ old_vectors, old_moments @ chemical_distortion)
        checks.append(dict(name=model + ': number-temperature projection retains physical chemical-potential distortion and its energy',
                           passed=abs(temperature) < 1e-12 and linalg.norm(kept - chemical_distortion) < 1e-12
                           and abs(basis.energy @ kept) > .1))
        checks.append(dict(name=model + ': old two-moment complement is not a general distortion observable',
                           passed=linalg.norm(old_erasure) < 1e-12 and linalg.norm(kept) > .1))
        rows.append(dict(model=model, finite_band_beta_mu=beta, chemical_distortion_energy=float(basis.energy @ kept)))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        observer='Baryon rest tetrad', clock='Fixed proper baryon number density',
                        spectral_template='Number-defined dilation of the actual background, not a fitted blackbody alone',
                        transformation_test_is_readout_test_not_a_second_gauge_evolution=True), __file__,
           [ROOT / 'spectral_readout.py', *sorted(set(inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()

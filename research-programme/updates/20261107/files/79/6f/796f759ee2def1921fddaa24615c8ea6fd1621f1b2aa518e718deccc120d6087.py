from observer_common import *
from spectral_readout import SpectralReadout, spectral_norm


def main():
    modest()
    folder = ROOT / 'results/projected-waves'
    folder.mkdir(parents=True, exist_ok=False)
    inputs, checks, rows = [], [], []
    for model in ['heavy', 'cold']:
        system = MixedSystem(model, 24, 8, 'event8')
        readout = SpectralReadout(system)
        inputs.extend(readout.inputs)
        source = PARENT / 'waves' / (model + '24-event8-3200') / 'evolution.npz'
        earlier = THERMAL_PARENT / 'paired' / (model + '24-high8-3200') / 'evolution.npz'
        inputs.extend([source, source.parent / 'status.json', earlier, earlier.parent / 'status.json'])
        with np.load(source) as saved:
            expansion, baseline, difference = saved['expansion'].copy(), saved['baseline_states'].copy(), saved['scaled_differences'].copy()
            heat = float(saved['heat'])
        with np.load(earlier) as saved:
            earlier_difference = saved['differences'].copy()
        mixed_shapes, mixed_temperatures, old_shapes, baseline_shapes = [], [], [], []
        band_centres = np.array([.03, .1, .3, 1., 3., 8.])
        frequencies, weights = np.polynomial.legendre.leggauss(20)
        bands = []
        for centre in band_centres:
            nodes = centre * np.exp(.08 * frequencies)
            planck = 1 / np.expm1(nodes)
            brightness = nodes ** 3 * planck * (1 + planck)
            bands.append((weights / 2 * brightness) @ system.basis.evaluate(nodes))
        bands = np.asarray(bands)
        gauge_errors, reconstruction_errors, temperature_errors = [], [], []
        for point, state, delta, previous_state in zip(expansion, baseline, difference, earlier_difference):
            mixed = readout.apply(point, delta)
            old = readout.apply(point, previous_state)
            normal = readout.apply(point, state)
            physical = heat * delta
            changed = readout.apply(point, readout.transform(point, physical, .001, -.001))
            physical_readout = readout.apply(point, physical)
            scale = max(float(np.max(spectral_norm(physical_readout['shapes'], system.basis.mass))), 1e-30)
            if point:
                gauge_errors.append(float(np.max(spectral_norm(changed['shapes'] - physical_readout['shapes'], system.basis.mass))) / scale)
            target = np.asarray([physical[system.mode_slice(degree, name)] for degree, names in enumerate(system.names) for name in names])
            reconstruction_errors.append(float(np.max(abs(readout.reconstruct(physical_readout) - target))))
            mixed_shapes.append(mixed['shapes'])
            mixed_temperatures.append(mixed['temperatures'])
            old_shapes.append(old['shapes'])
            baseline_shapes.append(normal['shapes'])
        mixed_shapes, old_shapes, baseline_shapes = map(np.asarray, [mixed_shapes, old_shapes, baseline_shapes])
        index = 0
        for degree, names in enumerate(system.names):
            for name in names:
                mixed_norm = heat * float(np.max(spectral_norm(mixed_shapes[:, index], system.basis.mass)))
                old_norm = float(np.max(spectral_norm(old_shapes[:, index], system.basis.mass)))
                base_norm = float(np.max(spectral_norm(baseline_shapes[:, index], system.basis.mass)))
                rows.append(dict(model=model, mode=str(degree) + name, mixed_shape=mixed_norm,
                                 previous_angular_shape=old_norm, baseline_shape=base_norm,
                                 mixed_to_previous=mixed_norm / old_norm if old_norm > 1e-25 else None))
                index += 1
        np.savez_compressed(folder / (model + '.npz'), expansion=expansion, heat=heat,
                            scaled_mixed_shapes=mixed_shapes, scaled_mixed_temperatures=mixed_temperatures,
                            previous_angular_shapes=old_shapes, baseline_shapes=baseline_shapes,
                            ideal_band_x=band_centres, ideal_band_rows=bands,
                            scaled_mixed_band_shape=np.einsum('bf,tmf->tmb', bands, mixed_shapes))
        checks.extend([
            dict(name=model + ': coordinate/frame invariance at tiny mixed-signal scale', passed=max(gauge_errors) < .002, value=max(gauge_errors)),
            dict(name=model + ': all physical spectral modes reconstruct', passed=max(reconstruction_errors) < 1e-24, value=max(reconstruction_errors)),
            dict(name=model + ': photon-number-free shape at all times', passed=float(np.max(abs(mixed_shapes @ system.basis.number))) < 1e-10),
            dict(name=model + ': finite projected spectra and bands', passed=bool(np.isfinite(mixed_shapes).all()))])
        control = THERMAL_PARENT / 'runs' / (model + '16-dust-3200') / 'evolution.npz'
        inputs.extend([control, control.parent / 'status.json'])
        with np.load(control) as saved:
            control_times, states = saved['expansion'].copy(), saved['states'].copy()
        residual, amplitude = 0., 0.
        for point, reduced in zip(control_times, states):
            expanded = np.zeros(system.size, complex)
            expanded[:11] = reduced[:11]
            start = 11
            for degree, names in enumerate(system.names):
                for mode, name in enumerate(names):
                    section = system.mode_slice(degree, name)
                    expanded[section.start:section.start + 16] = reduced[start + mode * 16:start + (mode + 1) * 16]
                start += 16 * len(names)
            projection = readout.apply(point, expanded, planck=True)
            residual = max(residual, float(np.max(abs(projection['shapes']))))
            amplitude = max(amplitude, float(np.max(abs(expanded))))
        checks.append(dict(name=model + ': matched established Planck/dust control remains distortion-free',
                           passed=residual < 1e-10 * amplitude, relative=residual / amplitude))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        no_new_wave_evolution=True, same_projection_both_parents=True,
                        bands_are_ideal_local_log_frequency_probes_not_instrument_bandpasses=True,
                        no_observed_sky_or_homogeneous_monopole_claim=True), __file__,
           [ROOT / 'spectral_readout.py', *sorted(set(inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
                          monopoles=[row for row in rows if row['mode'] == '0I'])), flush=True)


if __name__ == '__main__':
    main()

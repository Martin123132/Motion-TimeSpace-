from thermal_wave_common import *
from stable_spectral_basis import load_basis


def main():
    modest()
    folder = ROOT / 'results/expanding-refinements'
    assert not folder.exists()
    checks, rows, inputs = [], [], []
    def load(relative):
        source = ROOT / relative / 'evolution.npz'
        metadata = json.loads((source.parent / 'status.json').read_text())
        assert metadata['all_checks_passed'], relative
        inputs.extend([source, source.parent / 'status.json'])
        with np.load(source) as saved:
            return {key: saved[key].copy() for key in saved.files}
    labels = ['cold_density', 'baryon_density', 'photon_energy', 'neutrino_energy', 'photon_flux', 'neutrino_flux',
              'baryon_velocity', 'temperature', 'field1', 'field2', 'prime1', 'prime2']
    for model in ['heavy', 'cold']:
        pairs = [
            ('time1600-3200', model + '16-1600', model + '16-3200'),
            ('basis16-24', model + '16-3200', model + '24-3200'),
            ('angular6-8', model + '16-l6-3200', model + '16-3200'),
        ]
        for name, coarse_name, fine_name in pairs:
            coarse, fine = load('paired/' + coarse_name), load('paired/' + fine_name)
            assert np.max(abs(coarse['expansion'] - fine['expansion'])) < 1e-13
            for column, label in enumerate(labels):
                scale = float(np.max(abs(fine['features'][:, column])))
                error = float(np.max(abs(coarse['features'][:, column] - fine['features'][:, column])))
                baseline = float(np.max(abs(fine['baselines'][:, column])))
                floor = 1e-14 * max(baseline, 1e-30)
                resolved = scale > 100 * floor
                relative = error / scale if resolved else None
                passed = relative < .002 if resolved else error < floor
                rows.append(dict(model=model, comparison=name, feature=label, response=scale, difference=error,
                                 relative=relative, resolved=resolved, absolute_floor=floor))
                checks.append(dict(name=model + ':' + name + ':' + label + ': small response refinement',
                                   passed=passed, value=relative, resolved=resolved))
        for control in ['dust', 'physical', 'matched-elastic']:
            errors = []
            for steps in [800, 1600, 3200]:
                saved = load('runs/' + model + '16-' + control + '-' + str(steps))
                errors.append(float(np.max(saved['constraints'])))
            checks.append(dict(name=model + ':' + control + ': unprojected constraints converge with time resolution',
                               passed=errors[2] < errors[1] < errors[0] and errors[2] < .002, values=errors))
        paired = load('paired/' + model + '16-3200')
        direct = load('runs/' + model + '16-physical-3200')
        elastic = load('runs/' + model + '16-matched-elastic-3200')
        residual = float(np.max(abs(direct['features'] - elastic['features'] - paired['features'])))
        checks.append(dict(name=model + ': paired equation reconstructs independently evolved physical solution',
                           passed=residual < 1e-11, absolute_error=residual))
        basis = load_basis(ROOT / 'banks/stable24-late')
        source = ROOT / 'backgrounds' / (model + '24-3200') / 'history.npz'
        inputs.extend([source, source.parent / 'status.json'])
        with np.load(source) as background:
            rows.append(dict(model=model, background_final_energy=float(background['energy_scaled'][-1] * background['heat']),
                             background_final_temperature=float(background['temperature_scaled'][-1] * background['heat'])))
    folder.mkdir(parents=True, exist_ok=False)
    passed = all(row['passed'] for row in checks)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=passed, rows=rows,
                        gate=.002, small_response_directly_evolved=True, same_tests_both_retained_parents=True,
                        no_new_empirical_fit=True), __file__, sorted(set(inputs)))
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
                          worst_resolved=max(row['relative'] for row in rows if row.get('relative') is not None))), flush=True)


if __name__ == '__main__':
    main()

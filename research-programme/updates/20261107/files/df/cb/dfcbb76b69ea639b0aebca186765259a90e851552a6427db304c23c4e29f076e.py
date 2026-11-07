import argparse
from mixed_common import *
from mixed_wave_system import MixedSystem


def main(arguments):
    modest()
    folder = ROOT / 'results' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    inputs, rows, checks = [], [], []
    def load(name):
        path = ROOT / 'waves' / name / 'evolution.npz'
        packet = json.loads((path.parent / 'status.json').read_text())
        assert packet['all_checks_passed'], name
        inputs.extend([path, path.parent / 'status.json'])
        with np.load(path) as saved:
            return {key: saved[key].copy() for key in saved.files}
    labels = ['cold_density', 'baryon_density', 'photon_energy', 'neutrino_energy', 'photon_flux', 'neutrino_flux',
              'baryon_velocity', 'temperature', 'field1', 'field2', 'prime1', 'prime2']
    for model in ['heavy', 'cold']:
        fine_name = model + arguments.fine
        fine = load(fine_name)
        heat = float(fine['heat'])
        system = MixedSystem(model, int(fine['basis_count']), int(fine['maximum']), arguments.bank)
        for coarse_suffix in arguments.coarse:
            coarse = load(model + coarse_suffix)
            assert np.max(abs(coarse['expansion'] - fine['expansion'])) < 1e-12
            for column, label in enumerate(labels):
                amplitude = float(np.max(abs(fine['scaled_features'][:, column])))
                error = float(np.max(abs(coarse['scaled_features'][:, column] - fine['scaled_features'][:, column])))
                floor = 1e-12 * max(float(np.max(abs(fine['baseline_features'][:, column]))), 1e-30)
                resolved = amplitude > 100 * floor
                relative = error / amplitude if resolved else None
                passed = relative < .002 if resolved else error < floor
                rows.append(dict(model=model, comparison=coarse_suffix + ':' + arguments.fine, feature=label,
                                 relative=relative, amplitude=heat * amplitude, absolute_error=heat * error,
                                 resolved=resolved, scaled_floor=floor))
                checks.append(dict(name=model + ':' + coarse_suffix + ':' + label, passed=bool(passed), value=relative))
            coarse_count = int(coarse['basis_count'])
            fine_count = int(fine['basis_count'])
            coarse_start, fine_start = 11, 11
            for degree in range(int(fine['maximum']) + 1):
                names = ['I', 'V'] if degree < 2 else ['I', 'E', 'B', 'V']
                for mode, name in enumerate(names):
                    fine_slice = slice(fine_start + mode * fine_count, fine_start + (mode + 1) * fine_count)
                    coarse_slice = slice(coarse_start + mode * coarse_count, coarse_start + (mode + 1) * coarse_count)
                    target = fine['scaled_differences'][:, fine_slice]
                    candidate = np.zeros_like(target)
                    candidate[:, :coarse_count] = coarse['scaled_differences'][:, coarse_slice]
                    norm = float(np.max(linalg.norm(target, axis=1)))
                    error = float(np.max(linalg.norm(candidate - target, axis=1)))
                    active = norm > 1e-18
                    ratio = error / norm if active else None
                    checks.append(dict(name=model + ':' + coarse_suffix + ': spectrum ' + str(degree) + name,
                                       passed=bool(ratio < .002 if active else error < 1e-18), value=ratio))
                    rows.append(dict(model=model, comparison=coarse_suffix + ':' + arguments.fine,
                                     spectral_mode=str(degree) + name, relative=ratio, physical_norm=heat * norm))
                coarse_start += coarse_count * len(names)
                fine_start += fine_count * len(names)
        source = PARENT / 'paired' / (model + '24-high8-3200') / 'evolution.npz'
        inputs.extend([source, source.parent / 'status.json'])
        with np.load(source) as parent:
            assert np.max(abs(parent['expansion'] - fine['expansion'])) < 1e-12
            feature_ratios = []
            for column, label in enumerate(labels):
                parent_amplitude = float(np.max(abs(parent['features'][:, column])))
                mixed_amplitude = float(np.max(abs(fine['scaled_features'][:, column]))) * heat
                ratio = mixed_amplitude / parent_amplitude if parent_amplitude > 1e-35 else None
                feature_ratios.append(ratio)
                rows.append(dict(model=model, feature=label, mixed_physical_amplitude=mixed_amplitude,
                                 parent_angular_thermal_amplitude=parent_amplitude, mixed_to_parent_ratio=ratio))
            baseline_error = float(np.max(abs(fine['baseline_states'] - parent['baseline_states'] - parent['differences'])))
            checks.append(dict(name=model + ': baseline reconstructs saved Stage75 physical wave',
                               passed=baseline_error < 1e-10, absolute=baseline_error))
        norms = []
        for expansion, response in zip(fine['expansion'][1:], fine['background_corrections'][1:]):
            profile = system.geometry.profiles(expansion)
            norms.append(heat * float(linalg.norm(response[:-1])) / max(float(linalg.norm(profile)), 1e-100))
        rows.append(dict(model=model, forced_nonlinear_background_fraction=max(norms),
                         final_physical_temperature_correction=heat ** 2 * float(fine['background_corrections'][-1, -1])))
    passed = all(row['passed'] for row in checks)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=passed, rows=rows,
                        gate=.002, both_parents_same_tests=True, source_complete_matrix_derivative=True,
                        propagated_not_sampled_coefficient_comparison=True, no_observational_fit=True), __file__,
           [ROOT / 'mixed_wave_system.py', *sorted(set(inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--fine', required=True)
    parser.add_argument('--coarse', nargs='+', required=True)
    parser.add_argument('--bank', default='fine16')
    main(parser.parse_args())

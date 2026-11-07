from scaled_common import *
from scaled_system import ScaledSystem
from compare_scaled_waves import load_wave


def main():
    modest()
    folder = ROOT / 'results/parent-equivalence'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows, inputs = [], [], []
    for model in ['heavy', 'cold']:
        system = ScaledSystem(model)
        new, source = load_wave(model, 36, 3200)
        inputs.extend(source)
        old_path = PARENT / 'waves' / (model + '36-3200') / 'evolution.npz'
        inputs.extend([old_path, old_path.parent / 'status.json'])
        with np.load(old_path) as saved:
            assert np.max(abs(saved['expansion'] - new['expansion'])) < 1e-12
            original_features = saved['baseline_features'] + float(saved['heat']) * saved['scaled_features']
            original_baseline = saved['baseline_states'].copy()
            original_correction = float(saved['heat']) * saved['scaled_differences']
        for index in range(original_features.shape[1]):
            amplitude = float(np.max(abs(original_features[:, index])))
            error = float(np.max(abs(new['full_features'][:, index] - original_features[:, index])))
            relative = error / max(amplitude, 1e-25)
            checks.append(dict(name=model + ': retained physical feature ' + str(index), passed=relative < .002, value=relative, absolute=error))
        physical_baseline = np.array([system.physical_state(state) for state in new['baseline_coordinates']])
        physical_difference = np.array([system.physical_state(state) for state in new['coordinate_differences']])
        baseline_error = float(np.max(abs(physical_baseline - original_baseline)))
        correction_error = float(np.max(abs(physical_difference - original_correction)))
        correction_scale = float(np.max(abs(original_correction)))
        checks.append(dict(name=model + ': separately evolved mixed correction retains physical normalization', passed=correction_error / correction_scale < .002, value=correction_error / correction_scale))
        rows.append(dict(model=model, baseline_max_absolute_difference=baseline_error,
                         mixed_correction_relative_difference=correction_error / correction_scale))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        reference_scope='Same physical model at3200 steps. Agreement of large features does not alone certify the tiny spectral shape.'), __file__,
           [ROOT / 'scaled_system.py', ROOT / 'compare_scaled_waves.py', *sorted(set(inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()

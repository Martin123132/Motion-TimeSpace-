from thermal_wave_common import *
from thermal_wave_system import ThermalWaveSystem


def main():
    modest()
    folder = ROOT / 'results/paired-constraint-response'
    assert not folder.exists()
    checks, rows, inputs = [], [], []
    for model in ['heavy', 'cold']:
        system = ThermalWaveSystem(model, 16, 8, 'physical')
        errors = []
        for steps in [1600, 3200]:
            source = ROOT / 'paired' / (model + '16-' + str(steps)) / 'evolution.npz'
            inputs.extend([source, source.parent / 'status.json'])
            assert json.loads((source.parent / 'status.json').read_text())['all_checks_passed']
            residuals, scales = [], []
            with np.load(source) as saved:
                for expansion, difference in zip(saved['expansion'], saved['differences']):
                    residual, scale = system.constraints(float(expansion), difference)
                    residuals.append(residual)
                    scales.append(scale)
            peak_scale = max(scales)
            relative = float(np.max(abs(np.array(residuals))) / peak_scale)
            errors.append(relative)
            checks.append(dict(name=model + ': constraints measured at small paired response scale, steps' + str(steps),
                               passed=relative < .002, value=relative, peak_response_constraint_scale=peak_scale))
            rows.append(dict(model=model, steps=steps, relative=relative, peak_response_constraint_scale=peak_scale,
                             peak_absolute_residual=float(np.max(abs(np.array(residuals))))))
        checks.append(dict(name=model + ': small-response constraint residual decreases on time refinement',
                           passed=errors[1] < errors[0], values=errors))
        inputs.extend([system.geometry.source, system.geometry.parent.source, *system.ladder.inputs])
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        constraints_normalized_to_small_correction_not_common_baseline=True,
                        no_constraint_projection_used=True), __file__,
           [ROOT / 'thermal_wave_system.py', ROOT / 'background_geometry.py', ROOT / 'kernel_ladder.py', *sorted(set(inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']], rows=rows)), flush=True)


if __name__ == '__main__':
    main()

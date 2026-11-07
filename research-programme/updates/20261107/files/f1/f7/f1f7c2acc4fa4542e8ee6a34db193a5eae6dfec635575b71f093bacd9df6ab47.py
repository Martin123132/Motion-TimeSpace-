from step_common import *
from compare_response import sampled, norms


def main():
    modest()
    folder = ROOT / 'results/synthetic-refinements'
    assert not folder.exists()
    inputs, packets, checks = [], {}, []
    for label in ['base', 'time', 'fine']:
        path = ROOT / 'runs' / ('synthetic-' + label)
        with np.load(path / 'evolution.npz', allow_pickle=False) as packet:
            report = json.loads((path / 'status.json').read_text())
            packets[label] = dict(values=sampled(packet), times=packet['optical_depth'].copy(),
                                  temperature=np.array([row['temperature_defect_real'] for row in report['history']]),
                                  velocity=np.array([row['velocity_defect_real'] for row in report['history']]),
                                  entropy_ratio=report['final_to_initial_entropy_defect'])
        inputs.extend([path / 'evolution.npz', path / 'status.json'])
    rows = []
    for initial, final, label in [('base', 'time', 'time'), ('time', 'fine', 'frequency')]:
        coarse, fine = packets[initial], packets[final]
        assert np.max(abs(coarse['times'] - fine['times'])) < 1e-10
        spectrum = float(max(norms(coarse['values'] - fine['values'])) / max(norms(fine['values'])))
        temperature = float(max(abs(coarse['temperature'] - fine['temperature'])) / max(abs(fine['temperature'])))
        velocity = float(max(abs(coarse['velocity'] - fine['velocity'])) / max(abs(fine['velocity'])))
        for name, error in [('spectral defect', spectrum), ('temperature defect', temperature), ('velocity defect', velocity)]:
            checks.append(dict(name=label + ': independent nonthermal ' + name + ' refinement',
                               passed=error < .002, value=error, gate=.002))
        rows.append(dict(refinement=label, spectrum_error=spectrum, temperature_error=temperature,
                         velocity_error=velocity, coarse_entropy_ratio=coarse['entropy_ratio'],
                         fine_entropy_ratio=fine['entropy_ratio']))
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        rows=rows, independent_static_plasma_fixture_not_cosmological_prediction=True,
                        fine_compton_parameter=4., finite_positive_heat_capacity_evolved=True), __file__,
           inputs + [ROOT / 'compare_response.py'])
    print(json.dumps(dict(checks=checks, rows=rows)), flush=True)


if __name__ == '__main__':
    main()

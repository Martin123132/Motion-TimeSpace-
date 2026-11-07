from observer_common import *
from spectral_readout import SpectralReadout, spectral_norm
from extended_system import ExtendedSystem
from verify_total_response import embed


def load_projection(system, path):
    packet = json.loads((path.parent / 'status.json').read_text())
    assert packet['all_checks_passed']
    with np.load(path) as saved:
        times = saved['expansion'].copy()
        baseline = embed(system, saved['baseline_states'], int(saved['basis_count']))
        differences = embed(system, saved['scaled_differences'], int(saved['basis_count']))
        heat = float(saved['heat'])
    readout = SpectralReadout(system)
    base, correction = [], []
    for point, state, delta in zip(times, baseline, differences):
        base.append(readout.apply(point, state)['shapes'])
        correction.append(heat * readout.apply(point, delta)['shapes'])
    return times, np.asarray(base), np.asarray(correction), [path, path.parent / 'status.json', *readout.inputs]


def main():
    modest()
    folder = ROOT / 'results/extended-total-response'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows, inputs = [], [], []
    for model in ['heavy', 'cold']:
        system = ExtendedSystem(model)
        times, baseline, correction, source = load_projection(system, ROOT / 'waves' / (model + '28-3200') / 'evolution.npz')
        inputs.extend(source)
        total = baseline + correction
        baseline_norm = float(np.max(spectral_norm(baseline[:, 0], system.basis.mass)))
        total_norm = float(np.max(spectral_norm(total[:, 0], system.basis.mass)))
        inner = np.einsum('ti,ij,tj->', baseline[:, 0].conj(), system.basis.mass, correction[:, 0]).real
        base_power = np.einsum('ti,ij,tj->', baseline[:, 0].conj(), system.basis.mass, baseline[:, 0]).real
        correction_power = np.einsum('ti,ij,tj->', correction[:, 0].conj(), system.basis.mass, correction[:, 0]).real
        rows.append(dict(model=model, baseline_shape_norm=baseline_norm, total_shape_norm=total_norm,
                         remaining_fraction=total_norm / baseline_norm, spectral_mass_weighted_overlap=float(inner / np.sqrt(base_power * correction_power))))
        np.savez_compressed(folder / (model + '-total.npz'), expansion=times, baseline=baseline,
                            correction=correction, total=total)
        for suffix in ['24-3200', '24-event8-3200']:
            coarse_times, coarse_base, coarse_correction, source = load_projection(system, PARENT / 'waves' / (model + suffix) / 'evolution.npz')
            inputs.extend(source)
            assert np.max(abs(coarse_times - times)) < 1e-12
            coarse = coarse_base + coarse_correction
            for mode, label in [(0, '0I'), (2, '1I'), (4, '2I'), (5, '2E')]:
                norm = float(np.max(spectral_norm(total[:, mode], system.basis.mass)))
                error = float(np.max(spectral_norm(coarse[:, mode] - total[:, mode], system.basis.mass)))
                relative = error / norm
                checks.append(dict(name=model + ':' + suffix + ': common-basis total physical shape ' + label,
                                   passed=relative < .002, value=relative))
                rows.append(dict(model=model, comparison=suffix, mode=label, relative=relative, absolute_error=error))
        for mode, label in [(0, '0I'), (2, '1I'), (4, '2I'), (5, '2E')]:
            number_error = float(np.max(abs(total[:, mode] @ system.basis.number)))
            norm = float(np.max(spectral_norm(total[:, mode], system.basis.mass)))
            checks.append(dict(name=model + ': total physical shape number-free ' + label,
                               passed=number_error < 1e-8 * norm, value=number_error / norm))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        gate=.002, common_readout_basis=28, physical_background_basis=24,
                        refinement_changes_no_physical_parameters=True,
                        failed16_to24_total_comparison_retained=True,
                        scope='Resolution of the coherent local early-time spectral readout; not a sky prediction.'), __file__,
           [ROOT / 'spectral_readout.py', ROOT / 'extended_system.py', ROOT / 'verify_total_response.py', *sorted(set(inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
                          cancellation=[row for row in rows if 'remaining_fraction' in row])), flush=True)


if __name__ == '__main__':
    main()

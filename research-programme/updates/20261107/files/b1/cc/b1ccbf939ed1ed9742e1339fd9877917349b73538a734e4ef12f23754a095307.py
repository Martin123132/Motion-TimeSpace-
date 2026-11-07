from observer_common import *
from spectral_readout import SpectralReadout, spectral_norm


def embed(system, states, count):
    if count == system.count:
        return states.copy()
    result = np.zeros((len(states), system.size), complex)
    result[:, :11] = states[:, :11]
    offset = 11
    for degree, names in enumerate(system.names):
        for mode, name in enumerate(names):
            target = system.mode_slice(degree, name)
            result[:, target.start:target.start + count] = states[:, offset + mode * count:offset + (mode + 1) * count]
        offset += count * len(names)
    result[:, system.neutrino] = states[:, offset:]
    return result


def project_run(system, suffix):
    path = PARENT / 'waves' / (system.model + suffix) / 'evolution.npz'
    packet = json.loads((path.parent / 'status.json').read_text())
    assert packet['all_checks_passed']
    with np.load(path) as saved:
        times = saved['expansion'].copy()
        baseline = embed(system, saved['baseline_states'], int(saved['basis_count']))
        correction = embed(system, saved['scaled_differences'], int(saved['basis_count']))
        heat = float(saved['heat'])
    readout = SpectralReadout(system)
    base, changes = [], []
    for point, state, delta in zip(times, baseline, correction):
        base.append(readout.apply(point, state)['shapes'])
        changes.append(heat * readout.apply(point, delta)['shapes'])
    base, changes = np.asarray(base), np.asarray(changes)
    return times, base, changes, [path, path.parent / 'status.json']


def main():
    modest()
    folder = ROOT / 'results/total-response-refinement'
    folder.mkdir(parents=True, exist_ok=False)
    checks, rows, inputs = [], [], []
    for model in ['heavy', 'cold']:
        system = MixedSystem(model, 24, 8, 'event8')
        times, baseline, correction, source = project_run(system, '24-event8-3200')
        inputs.extend(source)
        total = baseline + correction
        baseline_norm = float(np.max(spectral_norm(baseline[:, 0], system.basis.mass)))
        total_norm = float(np.max(spectral_norm(total[:, 0], system.basis.mass)))
        overlap = float(np.vdot(baseline[:, 0], correction[:, 0]).real / (linalg.norm(baseline[:, 0]) * linalg.norm(correction[:, 0])))
        rows.append(dict(model=model, baseline_shape_norm=baseline_norm, total_shape_norm=total_norm,
                         remaining_fraction=total_norm / baseline_norm, history_overlap=overlap))
        np.savez_compressed(folder / (model + '-total.npz'), expansion=times, baseline=baseline,
                            correction=correction, total=total)
        for suffix in ['24-1600', '16-3200', '24-coarse-3200', '24-3200']:
            coarse_times, coarse_base, coarse_correction, sources = project_run(system, suffix)
            inputs.extend(sources)
            assert np.max(abs(coarse_times - times)) < 1e-12
            coarse = coarse_base + coarse_correction
            for mode, label in [(0, '0I'), (2, '1I'), (4, '2I'), (5, '2E')]:
                norm = float(np.max(spectral_norm(total[:, mode], system.basis.mass)))
                error = float(np.max(spectral_norm(coarse[:, mode] - total[:, mode], system.basis.mass)))
                relative = error / norm
                checks.append(dict(name=model + ':' + suffix + ': total physical shape ' + label,
                                   passed=relative < .002, value=relative))
                rows.append(dict(model=model, comparison=suffix, mode=label, relative=relative, absolute_error=error))
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks), rows=rows,
                        coherent_sum_not_sum_of_norms=True, gate=.002,
                        baseline_plus_correction_projected_separately_to_limit_subtraction_error=True), __file__,
           [ROOT / 'spectral_readout.py', *sorted(set(inputs))])
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
                          cancellation=[row for row in rows if 'remaining_fraction' in row])), flush=True)


if __name__ == '__main__':
    main()

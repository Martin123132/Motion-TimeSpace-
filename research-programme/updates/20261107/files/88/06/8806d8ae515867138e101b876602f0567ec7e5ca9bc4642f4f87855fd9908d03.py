from stage171_direction_common import *


def moment_checks(pair, label, basis, rows):
    high, low = pair
    with mp.workdps(80):
        norm0, norm1 = [mp.mpf(float(value)) for value in basis['norms'][:2]]
        mean = mp.mpf(float(basis['mean']))
        for branch, component, history in np.ndindex(2, 6, 4):
            def value(index):
                return mp.mpf(float(high[branch, component, index, history])) + mp.mpf(float(low[branch, component, index, history]))
            energy, gas = value(0), value(97)
            represented = mean*norm0*value(1)+norm1*value(2)
            scale = max(abs(energy), abs(gas), mp.mpf('1e-300'))
            key = f'{label}:{branch}:{source.COMPONENTS[component]}:{history}'
            check(rows, key+':energy-coordinate', abs(energy-represented)/scale, 1e-10)
            check(rows, key+':independent-gas-exchange', abs(energy+gas)/scale, 1e-10)
    for component, indices in [(4, [1, 2, 3]), (5, [0, 1, 2, 3])]:
        combined = combine([(high[:, index], low[:, index]) for index in indices], [1]*len(indices))
        error = combine([combined, (high[:, component], low[:, component])], [1, -1])
        relative = norm(error[0]+error[1], basis['mass']) / np.maximum(norm(high[:, component]+low[:, component], basis['mass']), 1e-300)
        check(rows, label+':component-closure:'+str(component), np.max(relative), 1e-10)


def main():
    source.modest()
    folder = ROOT / 'results/assessment'
    assert not (folder / 'COMPLETE').exists()
    frozen = verify(ROOT / 'results/frozen')
    assert verify(ROOT / 'events/target')['all_checks_passed']
    frozen_time = datetime.fromisoformat(frozen['finished_utc'])
    config = json.loads((ROOT / 'configuration.json').read_text())
    basis_path = PARENT / 'results/preparation/basis.npz'
    basis = np.load(basis_path)
    prediction = np.load(ROOT / 'results/frozen/predictions.npz')
    labels = list(prediction['groups'])
    paths = [ROOT / 'results/frozen/status.json', ROOT / 'results/frozen/predictions.npz', basis_path, ROOT / 'configuration.json']
    checks, moments, records, stencil_records = [], [], [], []
    actual = {}
    for tag in [*source.OFFSETS, 'target']:
        for electron in ELECTRONS:
            path = event_path(tag, electron)
            pair = read_pair(path)
            paths.append(path)
            moment_checks(pair, f'{tag}:electron{electron:02d}', basis, moments)
            if tag == 'anchor':
                assert np.array_equal(pair[0][0], pair[0][1]) and np.array_equal(pair[1][0], pair[1][1])
            if tag == 'target':
                with np.load(path) as data:
                    if electron not in REUSED:
                        assert datetime.fromisoformat(str(data['finished_utc'])) > frozen_time
                    node = json.loads(str(data['node']))
                    assert node['electron_index'] == electron and node['frequency'] == 14. and node['cosine'] == 0.
                actual[electron] = pair
    all_actuals, all_lows = [], []
    for index, label in enumerate(labels):
        if label.startswith('electron'):
            electrons = [int(label.replace('electron', ''))]
        else:
            electrons = {'reused_subtotal': list(REUSED), 'new_subtotal': config['new_electron_indices'], 'complete_sum': ELECTRONS}[label]
        target = combine([actual[electron] for electron in electrons], [1]*len(electrons))
        all_actuals.append(target[0])
        all_lows.append(target[1])
        target_norm = norm(target[0]+target[1], basis['mass'])
        moment_checks(target, label+':summed-target', basis, moments)
        for order_index, order_name in enumerate(['linear_fine', 'quadratic_fine', 'quadratic_coarse']):
            proposed = (prediction['high'][index, order_index], prediction['low'][index, order_index])
            error = combine([proposed, target], [1, -1])
            relative = norm(error[0]+error[1], basis['mass']) / np.maximum(target_norm, 1e-300)
            for branch, component, history in np.ndindex(relative.shape):
                check(checks, f'{label}:{order_name}:{BRANCHES[branch]}:{source.COMPONENTS[component]}:{history}', relative[branch, component, history], .01)
                records.append(dict(group=str(label), prediction=order_name, branch=BRANCHES[branch],
                                    component=source.COMPONENTS[component], history=history,
                                    relative=float(relative[branch, component, history]), target_norm=float(target_norm[branch, component, history])))
        fine = (prediction['high'][index, 1], prediction['low'][index, 1])
        coarse = (prediction['high'][index, 2], prediction['low'][index, 2])
        change = combine([fine, coarse], [1, -1])
        relative = norm(change[0]+change[1], basis['mass'])/np.maximum(target_norm, 1e-300)
        for branch, component, history in np.ndindex(relative.shape):
            stencil_records.append(dict(group=str(label), branch=BRANCHES[branch], component=source.COMPONENTS[component],
                                        history=history, relative=float(relative[branch, component, history])))
    summary = {}
    for label in ['reused_subtotal', 'new_subtotal', 'complete_sum']:
        for order_name in ['linear_fine', 'quadratic_fine', 'quadratic_coarse']:
            for branch in BRANCHES:
                for component in source.COMPONENTS:
                    values = [row['relative'] for row in records if (row['group'], row['prediction'], row['branch'], row['component']) == (label, order_name, branch, component)]
                    summary[f'{label}/{order_name}/{branch}/{component}'] = dict(maximum=max(values), passed=sum(value < .01 for value in values), count=len(values))
    folder.mkdir(parents=True, exist_ok=True)
    write_json(folder / 'prediction-checks.json', records)
    write_json(folder / 'moment-checks.json', moments)
    write_json(folder / 'stencil-impact.json', stencil_records)
    np.savez_compressed(folder / 'actuals.npz', high=np.array(all_actuals), low=np.array(all_lows), groups=np.array(labels))
    paths += [folder / name for name in ['prediction-checks.json', 'moment-checks.json', 'stencil-impact.json', 'actuals.npz']]
    packet = finish(folder, checks, paths, summary=summary, moment_checks=len(moments), moment_failures=sum(not row['passed'] for row in moments),
                    target_predictions_preceded_new_evaluations=True, previously_seen_target_directions=4, source_adopted=False,
                    tolerances_changed=False, full_population_integral=False)
    print(json.dumps(dict(prediction_checks=len(checks), prediction_failures=sum(not row['passed'] for row in checks),
                         moment_failures=packet['moment_failures'], complete_sum={key:value for key,value in summary.items() if key.startswith('complete_sum/')})), flush=True)


if __name__ == '__main__':
    main()

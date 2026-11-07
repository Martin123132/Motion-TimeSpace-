from stage172_angle_common import *
from assess_stage171 import moment_checks


def main():
    source.modest()
    folder = ROOT / 'results/assessment'
    assert not (folder / 'COMPLETE').exists()
    frozen = verify(ROOT / 'results/frozen')
    assert verify(ROOT / 'events/target')['all_checks_passed']
    freeze_time = datetime.fromisoformat(frozen['finished_utc'])
    config = json.loads((ROOT / 'configuration.json').read_text())
    basis_path = source.ROOT / 'results/preparation/basis.npz'
    basis = np.load(basis_path)
    prediction = np.load(ROOT / 'results/frozen/predictions.npz')
    assert list(prediction['groups']) == list(config['groups'])
    paths = [ROOT / 'results/frozen/status.json', ROOT / 'results/frozen/predictions.npz', basis_path, ROOT / 'configuration.json']
    checks, moments, records, stencil_records = [], [], [], []
    actual = {}
    for tag in [*source.OFFSETS, 'target']:
        for node in config['selected']:
            key = event_key(node)
            path = event_path(tag, key)
            pair = read_pair(path)
            paths.append(path)
            moment_checks(pair, tag+':'+key, basis, moments)
            if tag == 'anchor':
                assert np.array_equal(pair[0][0], pair[0][1]) and np.array_equal(pair[1][0], pair[1][1])
            if tag == 'target':
                with np.load(path) as data:
                    if node['cosine'] != 0.:
                        assert datetime.fromisoformat(str(data['finished_utc'])) > freeze_time
                    target_node = json.loads(str(data['node']))
                    assert event_key(target_node) == key and target_node['frequency'] == 14.
                actual[key] = pair
    all_actuals, all_lows = [], []
    for index, (label, members) in enumerate(config['groups'].items()):
        target = combine([actual[key] for key in members], [1]*len(members))
        all_actuals.append(target[0])
        all_lows.append(target[1])
        target_norm = norm(target[0]+target[1], basis['mass'])
        moment_checks(target, label+':summed-target', basis, moments)
        for order_index, order_name in enumerate(['linear_fine', 'quadratic_fine', 'quadratic_coarse']):
            proposed = (prediction['high'][index, order_index], prediction['low'][index, order_index])
            error = combine([proposed, target], [1, -1])
            relative = norm(error[0]+error[1], basis['mass'])/np.maximum(target_norm, 1e-300)
            for branch, component, history in np.ndindex(relative.shape):
                check(checks, f'{label}:{order_name}:{BRANCHES[branch]}:{source.COMPONENTS[component]}:{history}', relative[branch, component, history], .01)
                records.append(dict(group=label, prediction=order_name, branch=BRANCHES[branch],
                                    component=source.COMPONENTS[component], history=history,
                                    relative=float(relative[branch, component, history]), target_norm=float(target_norm[branch, component, history])))
        fine = (prediction['high'][index, 1], prediction['low'][index, 1])
        coarse = (prediction['high'][index, 2], prediction['low'][index, 2])
        change = combine([fine, coarse], [1, -1])
        relative = norm(change[0]+change[1], basis['mass'])/np.maximum(target_norm, 1e-300)
        for branch, component, history in np.ndindex(relative.shape):
            stencil_records.append(dict(group=label, branch=BRANCHES[branch], component=source.COMPONENTS[component],
                                        history=history, relative=float(relative[branch, component, history])))
    summary = {}
    for label in ['angle_negative', 'angle_central', 'angle_positive', 'new_angles_sum', 'complete_sum']:
        for order_name in ['linear_fine', 'quadratic_fine', 'quadratic_coarse']:
            for branch in BRANCHES:
                for component in source.COMPONENTS:
                    values = [row['relative'] for row in records if (row['group'],row['prediction'],row['branch'],row['component']) == (label,order_name,branch,component)]
                    summary[f'{label}/{order_name}/{branch}/{component}'] = dict(maximum=max(values), passed=sum(value < .01 for value in values), count=len(values))
    folder.mkdir(parents=True, exist_ok=True)
    write_json(folder / 'prediction-checks.json', records)
    write_json(folder / 'moment-checks.json', moments)
    write_json(folder / 'stencil-impact.json', stencil_records)
    np.savez_compressed(folder / 'actuals.npz', high=np.array(all_actuals), low=np.array(all_lows), groups=np.array(list(config['groups'])))
    paths += [folder / name for name in ['prediction-checks.json', 'moment-checks.json', 'stencil-impact.json', 'actuals.npz']]
    report = finish(folder, checks, paths, summary=summary, moment_checks=len(moments), moment_failures=sum(not row['passed'] for row in moments),
                    target_predictions_preceded_new_evaluations=True, previously_seen_target_combinations=12,
                    source_adopted=False, tolerances_changed=False, full_population_integral=False)
    print(json.dumps(dict(prediction_checks=len(checks), prediction_failures=sum(not row['passed'] for row in checks),
                         moment_failures=report['moment_failures'], complete_sum={key:value for key,value in summary.items() if key.startswith('complete_sum/')})), flush=True)


if __name__ == '__main__':
    main()

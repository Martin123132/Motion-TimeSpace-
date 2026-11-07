from stage172_angle_common import *
import argparse


def prepare():
    assert not (ROOT / 'configuration.json').exists()
    assert digest(PARENT / 'results/stage-integrity.json') == PARENT_SHA
    parent = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    for filename, checksum in parent['file_hashes'].items():
        assert digest(PARENT / filename) == checksum, filename
    for filename, checksum in parent['consumed_and_immediate_rehashed'].items():
        assert digest(filename) == checksum, filename
    config = json.loads((PARENT / 'configuration.json').read_text())
    for name in ['hard_cosine', 'reused_electron_indices', 'new_electron_indices', 'prior_bookmark_normalized_sha256']:
        config.pop(name, None)
    anchor, theta = source.context(source.START)
    selected = nodes(theta)
    groups = {event_key(node): [event_key(node)] for node in selected}
    groups.update({'angle_'+angle: [event_key(node) for node in selected if angle_label(node['cosine']) == angle] for angle in ANGLES})
    groups['new_angles_sum'] = [event_key(node) for node in selected if node['cosine'] != 0.]
    groups['complete_sum'] = [event_key(node) for node in selected]
    config.update(stage=172, hard_cosines=sorted({node['cosine'] for node in selected}), selected=selected, groups=groups,
                  reused_angle='central', new_angles=['negative', 'positive'], new_target_combinations=24,
                  known_target_combinations=12, partial_prospective_test=True, complete_finite_hard_angle_sum=True,
                  full_population_integral=False, started_utc=STARTED, deadline_utc=DEADLINE)
    checks, paths = [], [PARENT / 'configuration.json', *anchor.inputs]
    for tag, offset in {**source.OFFSETS, 'target': config['delta_log_temperature']}.items():
        unused, temperature = source.context(source.START-offset/config['expansion_span'])
        selected_at_temperature = nodes(temperature)
        hard = [node for node in selected_at_temperature if node['electron_index'] == 0]
        for power in range(6):
            expected = 2/(power+1) if power % 2 == 0 else 0.
            check(checks, f'{tag}:Gauss moment degree{power}', abs(sum(node['hard_weight']*node['cosine']**power for node in hard)-expected), 1e-14)
        if tag != 'target':
            paths.extend(event_path(tag, event_key(node)) for node in selected_at_temperature if node['cosine'] == 0.)
    config['prior_bookmark_normalized_sha256'] = {
        str(path): hashlib.sha256(path.read_text(encoding='utf-8').encode('utf-8')).hexdigest()
        for path in [BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md']}
    write_json(ROOT / 'configuration.json', config)
    report = finish(ROOT / 'results/preparation', checks, [*paths, ROOT / 'configuration.json'],
                    parent_payloads_rehashed=len(parent['file_hashes']), target_source_read=False,
                    new_target_source_evaluated=False, target_kinematics_only=True)
    assert report['all_checks_passed']
    print(json.dumps(dict(prepared=True, checks=len(checks), new_events=144, reused_events=72, groups=len(groups))), flush=True)


def evaluate_phase(phase, deadline):
    config = json.loads((ROOT / 'configuration.json').read_text())
    assert verify(ROOT / 'results/preparation')['all_checks_passed']
    if phase == 'target':
        frozen = verify(ROOT / 'results/frozen')
        assert frozen['new_target_source_evaluated'] is False
        offsets = {'target': config['delta_log_temperature']}
    else:
        offsets = source.OFFSETS
    anchor, unused = source.context(source.START)
    for tag, offset in offsets.items():
        folder = ROOT / 'events' / tag
        if (folder / 'COMPLETE').exists():
            verify(folder)
            continue
        folder.mkdir(parents=True, exist_ok=True)
        bundle, theta = source.context(source.START-offset/config['expansion_span'])
        paired = source.PairedHistory(bundle, anchor)
        evaluators = source.models(paired)
        checks, paths = [], [ROOT / 'configuration.json', *bundle.inputs, *anchor.inputs]
        if phase == 'target':
            paths.append(ROOT / 'results/frozen/status.json')
        for node in nodes(theta):
            if node['cosine'] == 0.:
                continue
            key = event_key(node)
            path = event_path(tag, key)
            if not path.exists():
                if datetime.now(timezone.utc) >= datetime.fromisoformat(deadline):
                    write_json(ROOT / 'progress.json', dict(state='paused_at_safe_event', phase=tag, next_key=key))
                    return False
                began = time.monotonic()
                path.parent.mkdir(parents=True, exist_ok=True)
                parameters, weight = source.physics.parameters_and_weight(theta, node)
                scalar, cache_path, reused = virtual(parameters)
                mp.mp.dps = 60
                high, low, diagnostics = source.evaluate(parameters, paired, evaluators, scalar)
                pair = (np.stack([high[..., :4], high[..., 4:]]), np.stack([low[..., :4], low[..., 4:]]))
                high, low = combine([pair], [-weight])
                temporary = path.with_suffix('.tmp')
                with temporary.open('wb') as handle:
                    np.savez_compressed(handle, high=high, low=low, theta=theta, offset=offset, weight=weight,
                                        node=json.dumps(node, sort_keys=True), diagnostics=json.dumps(diagnostics),
                                        loop_path=str(cache_path), loop_reused=reused, explicit_mp_precision=60,
                                        finished_utc=datetime.now(timezone.utc).isoformat())
                temporary.replace(path)
                print(json.dumps(dict(phase=tag, key=key, seconds=time.monotonic()-began)), flush=True)
            with np.load(path) as data:
                assert float(data['theta']) == theta and float(data['offset']) == offset
                assert data['high'].shape == data['low'].shape == (2, 6, 98, 4)
                assert np.isfinite(data['high']).all() and np.isfinite(data['low']).all()
                assert json.loads(str(data['node'])) == node
                assert int(data['explicit_mp_precision']) == 60
                for name, value in json.loads(str(data['diagnostics'])).items():
                    check(checks, key+':'+name, value, 1e-10)
                paths.extend([path, Path(str(data['loop_path']))])
            write_json(ROOT / 'progress.json', dict(state='running', phase=tag, last_key=key,
                       saved_new_events=len(list((ROOT / 'events').rglob('electron-*.npz'))), expected_new_events=144, pid=os.getpid()))
        report = finish(folder, checks, paths, theta=theta, phase=tag, new_combinations=24)
        assert report['all_checks_passed'], 'Event identities failed; retain bank and investigate before proceeding'
    return True


def freeze():
    assert not (ROOT / 'events/target').exists()
    folder = ROOT / 'results/frozen'
    assert not (folder / 'COMPLETE').exists()
    config = json.loads((ROOT / 'configuration.json').read_text())
    for tag in source.OFFSETS:
        assert verify(ROOT / 'events' / tag)['all_checks_passed']
    basis_path = source.ROOT / 'results/preparation/basis.npz'
    mass = np.load(basis_path)['mass']
    paths = [ROOT / 'configuration.json', basis_path]
    all_pairs = {event_key(node): {tag: read_pair(event_path(tag, event_key(node))) for tag in source.OFFSETS} for node in config['selected']}
    paths.extend(event_path(tag, key) for key in all_pairs for tag in source.OFFSETS)
    high, low, derivative_high, derivative_low, checks = [], [], [], [], []
    for label, members in config['groups'].items():
        summed = {tag: combine([all_pairs[key][tag] for key in members], [1]*len(members)) for tag in source.OFFSETS}
        predictions, derivatives = predictors(summed, config['delta_log_temperature'])
        high.append(np.array([pair[0] for pair in predictions]))
        low.append(np.array([pair[1] for pair in predictions]))
        derivative_high.append(np.array([pair[0] for pair in derivatives]))
        derivative_low.append(np.array([pair[1] for pair in derivatives]))
        for derivative, indices in [('tangent', [0, 1]), ('curvature', [2, 3])]:
            coarse, fine = [derivatives[index] for index in indices]
            difference = combine([coarse, fine], [1, -1])
            relative = norm(difference[0]+difference[1], mass)/np.maximum(norm(fine[0]+fine[1], mass), 1e-300)
            for branch, component, history in np.ndindex(relative.shape):
                check(checks, f'{label}:{BRANCHES[branch]}:{source.COMPONENTS[component]}:{history}:{derivative}', relative[branch, component, history], .01)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / 'predictions.npz'
    np.savez_compressed(path, high=np.array(high), low=np.array(low), derivative_high=np.array(derivative_high),
                        derivative_low=np.array(derivative_low), groups=np.array(list(config['groups'])),
                        delta=config['delta_log_temperature'], orders=np.array([1, 2, 2]))
    finish(folder, checks, [*paths, path], new_target_source_evaluated=False, new_target_source_read=False,
           known_target_combinations=12, missing_target_combinations=24, partially_prospective=True,
           prediction_sha256=digest(path), source_curve_changed=False,
           finite_derivative_failures=sum(not row['passed'] for row in checks))
    print(json.dumps(dict(frozen=True, prediction_sha256=digest(path), derivative_failures=sum(not row['passed'] for row in checks))), flush=True)


def main():
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['prepare', 'stencil', 'freeze', 'target', 'production'])
    parser.add_argument('--deadline', default=DEADLINE)
    args = parser.parse_args()
    if args.phase == 'prepare':
        prepare()
    elif args.phase == 'freeze':
        freeze()
    elif args.phase == 'production':
        if not evaluate_phase('stencil', args.deadline):
            return
        if not (ROOT / 'results/frozen/COMPLETE').exists():
            freeze()
        if not evaluate_phase('target', args.deadline):
            return
        write_json(ROOT / 'progress.json', dict(state='production_complete', saved_new_events=144, pid=os.getpid()))
    else:
        evaluate_phase(args.phase, args.deadline)


if __name__ == '__main__':
    main()

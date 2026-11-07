from stage171_direction_common import *
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
    config.update(stage=171, incoming_frequency=14., hard_cosine=0., electron_indices=ELECTRONS,
                  reused_electron_indices=list(REUSED), new_electron_indices=[value for value in ELECTRONS if value not in REUSED],
                  partial_prospective_test=True, complete_finite_electron_sum=True,
                  full_population_integral=False, started_utc=STARTED, deadline_utc=DEADLINE)
    config.pop('selected')
    anchor, theta = source.context(source.START)
    checks = []
    paths = [PARENT / 'configuration.json', *anchor.inputs]
    for tag, offset in {**source.OFFSETS, 'target': config['delta_log_temperature']}.items():
        unused, temperature = source.context(source.START-offset/config['expansion_span'])
        selected = nodes(temperature)
        weights, velocities = [], []
        for node in selected:
            for reflected in range(node['reflection_multiplicity']):
                velocity = np.array(node['velocity'])
                if reflected:
                    velocity[1] *= -1
                velocities.append(velocity)
                weights.append(node['electron_weight'])
        weights, velocities = np.array(weights), np.array(velocities)
        assert len(weights) == 16
        check(checks, tag+':electron normalization', abs(weights.sum()-1), 1e-14)
        check(checks, tag+':odd velocity moment', np.max(abs(weights @ velocities)), 1e-14)
        tensor = np.einsum('a,ai,aj->ij', weights, velocities, velocities)
        check(checks, tag+':isotropic second moment', np.max(abs(tensor-np.eye(3)*np.trace(tensor)/3)), 1e-14)
        if tag != 'target':
            paths.extend(event_path(tag, electron) for electron in REUSED)
    bookmarks = {}
    for path in [BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md']:
        body = path.read_text(encoding='utf-8')
        bookmarks[str(path)] = hashlib.sha256(body.encode('utf-8')).hexdigest()
    config['prior_bookmark_normalized_sha256'] = bookmarks
    write_json(ROOT / 'configuration.json', config)
    packet = finish(ROOT / 'results/preparation', checks, [*paths, ROOT / 'configuration.json'],
                    parent_payloads_rehashed=len(parent['file_hashes']), inherited_dependencies_rehashed=len(parent['consumed_and_immediate_rehashed']),
                    target_source_read=False, target_kinematics_only=True)
    assert packet['all_checks_passed']
    print(json.dumps(dict(prepared=True, checks=len(checks), new_events=48, reused_events=24)), flush=True)


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
            electron = node['electron_index']
            if electron in REUSED:
                continue
            path = event_path(tag, electron)
            if not path.exists():
                if datetime.now(timezone.utc) >= datetime.fromisoformat(deadline):
                    write_json(ROOT / 'progress.json', dict(state='paused_at_safe_event', phase=tag, next_electron=electron))
                    return False
                began = time.monotonic()
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
                print(json.dumps(dict(phase=tag, electron=electron, seconds=time.monotonic()-began)), flush=True)
            with np.load(path) as data:
                assert float(data['theta']) == theta and float(data['offset']) == offset
                assert data['high'].shape == data['low'].shape == (2, 6, 98, 4)
                assert np.isfinite(data['high']).all() and np.isfinite(data['low']).all()
                assert int(data['explicit_mp_precision']) == 60
                for name, value in json.loads(str(data['diagnostics'])).items():
                    check(checks, f'{electron}:{name}', value, 1e-10)
                paths.extend([path, Path(str(data['loop_path']))])
            write_json(ROOT / 'progress.json', dict(state='running', phase=tag, last_electron=electron,
                       saved_new_events=len(list((ROOT / 'events').rglob('electron-*.npz'))), expected_new_events=48, pid=os.getpid()))
        finish(folder, checks, paths, theta=theta, phase=tag, newly_evaluated_electrons=config['new_electron_indices'])
    return True


def freeze():
    assert not (ROOT / 'events/target').exists()
    folder = ROOT / 'results/frozen'
    assert not (folder / 'COMPLETE').exists()
    config = json.loads((ROOT / 'configuration.json').read_text())
    for tag in source.OFFSETS:
        assert verify(ROOT / 'events' / tag)['all_checks_passed']
    mass = np.load(PARENT / 'results/preparation/basis.npz')['mass']
    paths = [ROOT / 'configuration.json', PARENT / 'results/preparation/basis.npz']
    all_pairs = {}
    for electron in ELECTRONS:
        all_pairs[electron] = {tag: read_pair(event_path(tag, electron)) for tag in source.OFFSETS}
        paths.extend(event_path(tag, electron) for tag in source.OFFSETS)
    groups = [(f'electron{electron:02d}', [electron]) for electron in ELECTRONS]
    groups += [('reused_subtotal', list(REUSED)), ('new_subtotal', config['new_electron_indices']), ('complete_sum', ELECTRONS)]
    high, low, derivative_high, derivative_low, checks = [], [], [], [], []
    for label, electrons in groups:
        summed = {tag: combine([all_pairs[electron][tag] for electron in electrons], [1]*len(electrons)) for tag in source.OFFSETS}
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
                check(checks, f'{label}:{BRANCHES[branch]}:{source.COMPONENTS[component]}:{history}:{derivative}',
                      relative[branch, component, history], .01)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / 'predictions.npz'
    np.savez_compressed(path, high=np.array(high), low=np.array(low), derivative_high=np.array(derivative_high),
                        derivative_low=np.array(derivative_low), groups=np.array([label for label, unused in groups]),
                        delta=config['delta_log_temperature'], orders=np.array([1, 2, 2]))
    finish(folder, checks, [*paths, path], new_target_source_evaluated=False, new_target_source_read=False,
           known_target_directions=4, missing_target_directions=8, partially_prospective=True,
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
        write_json(ROOT / 'progress.json', dict(state='production_complete', saved_new_events=48, pid=os.getpid()))
    else:
        evaluate_phase(args.phase, args.deadline)


if __name__ == '__main__':
    main()

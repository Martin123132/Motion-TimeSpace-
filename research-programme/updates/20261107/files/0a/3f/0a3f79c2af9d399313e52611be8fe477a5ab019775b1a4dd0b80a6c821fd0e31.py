from stage172_angle_common import *
sys.path.insert(0, str(BRANCH / 'heldout-final-spectrum-20261019'))
import stage168_common as ancestry


def main():
    source.modest()
    folder = ROOT / 'results/validation'
    assert not (folder / 'COMPLETE').exists()
    checks, retained, hashes, packets = [], [], {}, {}
    required = ['results/preparation', 'results/frozen', 'results/assessment', *['events/'+tag for tag in [*source.OFFSETS, 'target']]]
    for label in required:
        packet = verify(ROOT / label)
        packets[label] = packet
        for filename, checksum in packet['input_hashes'].items():
            assert filename not in hashes or hashes[filename] == checksum, filename
            hashes[filename] = checksum
        retained.extend(dict(row, packet=label) for row in packet['checks'] if not row['passed'])
    moments = json.loads((ROOT / 'results/assessment/moment-checks.json').read_text())
    retained.extend(dict(row, packet='independent_moments') for row in moments if not row['passed'])
    assert packets['results/preparation']['all_checks_passed']
    assert all(packets['events/'+tag]['all_checks_passed'] for tag in [*source.OFFSETS, 'target'])
    checks.append(dict(name='All preparation and production identities pass', passed=True))
    check(checks, 'Current source moment failures', sum(not row['passed'] for row in moments), .5)
    config = json.loads((ROOT / 'configuration.json').read_text())
    basis_path = source.ROOT / 'results/preparation/basis.npz'
    basis = np.load(basis_path)
    mass = basis['mass']
    frozen = np.load(ROOT / 'results/frozen/predictions.npz')
    labels = list(frozen['groups'])
    total_index = labels.index('complete_sum')
    central_index = labels.index('angle_central')
    old_frozen_path = PARENT / 'results/frozen/predictions.npz'
    old_frozen = np.load(old_frozen_path)
    old_index = list(old_frozen['groups']).index('complete_sum')
    for order in range(3):
        direct = (frozen['high'][total_index, order], frozen['low'][total_index, order])
        for label, members in [('36 individual', list(config['groups'])[:36]), ('3 angle subtotals', ['angle_'+angle for angle in ANGLES])]:
            indices = [labels.index(member) for member in members]
            summed = combine([(frozen['high'][index, order], frozen['low'][index, order]) for index in indices], [1]*len(indices))
            error = combine([summed, direct], [1, -1])
            relative = norm(error[0]+error[1], mass)/np.maximum(norm(direct[0]+direct[1], mass), 1e-300)
            check(checks, f'{label}:sum/prediction commutation:{order}', np.max(relative), 1e-10)
        central = (frozen['high'][central_index, order], frozen['low'][central_index, order])
        old_central = (old_frozen['high'][old_index, order], old_frozen['low'][old_index, order])
        error = combine([central, old_central], [1, -1])
        relative = norm(error[0]+error[1], mass)/np.maximum(norm(old_central[0]+old_central[1], mass), 1e-300)
        check(checks, 'Unchanged Stage171 central prediction:'+str(order), np.max(relative), 1e-10)
    anchor, unused = source.context(source.START)
    precision = []
    for tag, offset in [('anchor', 0.), ('target', config['delta_log_temperature'])]:
        bundle, theta = source.context(source.START-offset/config['expansion_span'])
        paired = source.PairedHistory(bundle, anchor)
        model = source.models(paired)[0]['difference']
        for node in nodes(theta):
            if node['cosine'] == 0. or node['electron_index'] not in [1, 14]:
                continue
            parameters, unused = source.physics.parameters_and_weight(theta, node)
            with mp.workdps(60):
                lower = model.state_correction(parameters)['total']
            with mp.workdps(80):
                higher = model.state_correction(parameters)['total']
            values = norm(lower-higher, mass)/np.maximum(norm(higher, mass), 1e-300)
            for column, value in enumerate(values):
                check(precision, f'{tag}:{event_key(node)}:state60-vs80:{column}', value, 1e-10)
    checks += precision
    parent_path = PARENT / 'results/stage-integrity.json'
    assert digest(parent_path) == PARENT_SHA
    parent = json.loads(parent_path.read_text())
    chain = {parent_path: parent}
    current = parent
    for name in ['microscopic-temperature-tangent-20261019', 'low-frequency-temperature-law-20261019', 'heldout-final-spectrum-20261019']:
        path = BRANCH / name / 'results/stage-integrity.json'
        assert digest(path) == current['parent_seal_sha256']
        current = json.loads(path.read_text())
        chain[path] = current
    chain.update(ancestry.ancestors())
    prior = {PARENT / name for name in parent['file_hashes']}
    prior.update(Path(filename) for filename in hashes if not Path(filename).is_relative_to(ROOT))
    prior.update(path for path in inputs() if not path.is_relative_to(ROOT))
    prior.add(old_frozen_path)
    authenticated = ancestry.authenticate(prior, chain)
    checks.append(dict(name='Immediate parent and consumed ancestor files authenticated', count=len(authenticated), passed=True))
    for filename, checksum in hashes.items():
        assert digest(filename) == checksum, filename
    scripts = list(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_text(encoding='utf-8'), str(path), 'exec')
    assert not list(ROOT.rglob('__pycache__'))
    checks.append(dict(name='Scripts compile without caches', count=len(scripts), passed=True))
    protected = BRANCH.parent.parent / 'formalization-workbench'
    modified = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > datetime.fromisoformat(STARTED).timestamp()]
    checks.append(dict(name='Protected workbench mtime guard', passed=not modified, count=len(modified)))
    assert len(list((ROOT / 'events').rglob('electron-*.npz'))) == 144
    freeze_time = datetime.fromisoformat(packets['results/frozen']['finished_utc'])
    targets = list((ROOT / 'events/target').rglob('electron-*.npz'))
    assert len(targets) == 24
    for path in targets:
        with np.load(path) as data:
            assert datetime.fromisoformat(str(data['finished_utc'])) > freeze_time
    assert packets['results/frozen']['known_target_combinations'] == 12
    checks.append(dict(name='All24 new targets follow freeze;12 known central targets disclosed', passed=True))
    primary = [row for row in packets['results/frozen']['checks'] if row['name'].startswith('complete_sum:') and
               any(':'+component+':' in row['name'] for component in ['control', 'remainder', 'total'])]
    folder.mkdir(parents=True, exist_ok=True)
    write_json(folder / 'retained-failures.json', retained)
    write_json(folder / 'state-precision-checks.json', precision)
    report = finish(folder, checks, [*map(Path, hashes), old_frozen_path, *[ROOT / label / 'status.json' for label in required],
                                    folder / 'retained-failures.json', folder / 'state-precision-checks.json'],
                    protocol_validation_only=True, retained_failed_check_count=len(retained),
                    primary_summed_derivative_stability_pass=all(row['passed'] for row in primary),
                    consumed_and_immediate_rehashed=authenticated, rehashed_prior_files=len(authenticated),
                    compiled_scripts=len(scripts), source_curve_changed=False, current_history_replaced=False,
                    full_population_integral=False, native_incident_histories_are_inputs=True,
                    partial_prospective_test=True, tolerances_changed=False, protected_modified_file_count=len(modified),
                    protected_check_scope='Mtime guard since '+STARTED+'; not a pre-turn content snapshot')
    print(json.dumps(dict(protocol_pass=report['all_checks_passed'], checks=len(checks), retained_failures=len(retained),
                         summed_derivative_pass=report['primary_summed_derivative_stability_pass'], authenticated=len(authenticated))), flush=True)


if __name__ == '__main__':
    main()

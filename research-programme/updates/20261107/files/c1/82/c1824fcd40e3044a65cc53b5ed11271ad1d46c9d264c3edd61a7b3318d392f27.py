from stage173_frequency_common import *
sys.path.insert(0, str(BRANCH / 'heldout-final-spectrum-20261019'))
import stage168_common as ancestry


def main():
    source.modest()
    folder = ROOT / 'results/validation'
    assert not (folder / 'COMPLETE').exists()
    checks, retained, hashes, packets = [], [], {}, {}
    tags = [*source.OFFSETS, 'target']
    required = ['results/preparation', 'results/frozen', 'results/assessment', *['events/'+tag for tag in tags]]
    batches = [f'runs/{tag}-batch-{batch:02d}' for tag in tags for batch in range(1, 7)]
    for label in [*required, *batches]:
        packet = verify(ROOT / label)
        packets[label] = packet
        for filename, checksum in packet['input_hashes'].items():
            assert filename not in hashes or hashes[filename] == checksum, filename
            hashes[filename] = checksum
        if label not in batches:
            retained.extend(dict(row, packet=label) for row in packet['checks'] if not row['passed'])
    for tag in tags:
        ordinals = []
        for batch in range(1, 7):
            packet = packets[f'runs/{tag}-batch-{batch:02d}']
            assert packet['all_checks_passed'] and packet['batch_size'] == 6 and packet['count'] == 30
            ordinals.extend(range(packet['first_ordinal'], packet['last_ordinal']+1))
        assert ordinals == list(range(36))
    checks.append(dict(name='36 six-event batches cover all216 events without gaps or overlap', passed=True))
    moments = json.loads((ROOT / 'results/assessment/moment-checks.json').read_text())
    retained.extend(dict(row, packet='independent_moments') for row in moments if not row['passed'])
    assert packets['results/preparation']['all_checks_passed']
    assert all(packets['events/'+tag]['all_checks_passed'] for tag in tags)
    checks.append(dict(name='All preparation and production identities pass', passed=True))
    check(checks, 'Current source moment failures', sum(not row['passed'] for row in moments), .5)
    config = json.loads((ROOT / 'configuration.json').read_text())
    mass = np.load(source.ROOT / 'results/preparation/basis.npz')['mass']
    frozen = np.load(ROOT / 'results/frozen/predictions.npz')
    labels = list(frozen['groups'])
    complete_index = labels.index('complete_sum')
    reference_index = labels.index('reference_x14')
    partial_index = labels.index('two_frequency_partial')
    reference, reference_derivatives, reference_path = reference_prediction()
    for order in range(3):
        direct = (frozen['high'][complete_index, order], frozen['low'][complete_index, order])
        for label, members in [('36 individual', list(config['groups'])[:36]), ('3 angle subtotals', ['angle_'+angle for angle in ANGLES])]:
            indices = [labels.index(member) for member in members]
            summed = combine([(frozen['high'][index, order], frozen['low'][index, order]) for index in indices], [1]*len(indices))
            error = combine([summed, direct], [1, -1])
            relative = norm(error[0]+error[1], mass)/np.maximum(norm(direct[0]+direct[1], mass), 1e-300)
            check(checks, f'{label}:sum/prediction commutation:{order}', np.max(relative), 1e-10)
        assert np.array_equal(frozen['high'][reference_index, order], reference[order][0])
        assert np.array_equal(frozen['low'][reference_index, order], reference[order][1])
        partial = combine([direct, reference[order]], [1, 1])
        assert np.array_equal(frozen['high'][partial_index, order], partial[0])
        assert np.array_equal(frozen['low'][partial_index, order], partial[1])
    checks.append(dict(name='Saved x=14 predictors unchanged; partial sum not reweighted', passed=True))
    anchor, unused = source.context(source.START)
    precision = []
    for tag, offset in [('anchor', 0.), ('target', config['delta_log_temperature'])]:
        bundle, theta = source.context(source.START-offset/config['expansion_span'])
        paired = source.PairedHistory(bundle, anchor)
        model = source.models(paired)[0]['difference']
        for node in nodes(theta, config['incoming_frequency']):
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
    for name in ['electron-direction-temperature-average-20261020', 'microscopic-temperature-tangent-20261019', 'low-frequency-temperature-law-20261019', 'heldout-final-spectrum-20261019']:
        path = BRANCH / name / 'results/stage-integrity.json'
        assert digest(path) == current['parent_seal_sha256']
        current = json.loads(path.read_text())
        chain[path] = current
    chain.update(ancestry.ancestors())
    prior = {PARENT / name for name in parent['file_hashes']}
    prior.update(Path(filename) for filename in hashes if not Path(filename).is_relative_to(ROOT))
    prior.update(path for path in inputs() if not path.is_relative_to(ROOT))
    prior.add(reference_path)
    authenticated = ancestry.authenticate(prior, chain)
    checks.append(dict(name='Immediate parent and consumed ancestors authenticated', count=len(authenticated), passed=True))
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
    assert len(list((ROOT / 'events').rglob('electron-*.npz'))) == 216
    freeze_time = datetime.fromisoformat(packets['results/frozen']['finished_utc'])
    targets = list((ROOT / 'events/target').rglob('electron-*.npz'))
    assert len(targets) == 36
    for path in targets:
        with np.load(path) as data:
            assert datetime.fromisoformat(str(data['finished_utc'])) > freeze_time
    assert packets['results/frozen']['known_reference_target_combinations'] == 36
    checks.append(dict(name='All36 new-frequency targets follow freeze; known x=14 targets disclosed', passed=True))
    stability = {}
    for group in ['complete_sum', 'two_frequency_partial']:
        primary = [row for row in packets['results/frozen']['checks'] if row['name'].startswith(group+':') and
                   any(':'+component+':' in row['name'] for component in ['control', 'remainder', 'total'])]
        stability[group] = all(row['passed'] for row in primary)
    folder.mkdir(parents=True, exist_ok=True)
    write_json(folder / 'retained-failures.json', retained)
    write_json(folder / 'state-precision-checks.json', precision)
    report = finish(folder, checks, [*map(Path, hashes), reference_path, *[ROOT / label / 'status.json' for label in [*required, *batches]],
                                    folder / 'retained-failures.json', folder / 'state-precision-checks.json'],
                    protocol_validation_only=True, retained_failed_check_count=len(retained),
                    primary_summed_derivative_stability=stability, consumed_and_immediate_rehashed=authenticated,
                    rehashed_prior_files=len(authenticated), compiled_scripts=len(scripts), verified_batches=36,
                    source_curve_changed=False, current_history_replaced=False, full_population_integral=False,
                    native_incident_histories_are_inputs=True, partial_sum_partly_prospective=True,
                    tolerances_changed=False, protected_modified_file_count=len(modified),
                    protected_check_scope='Mtime guard since '+STARTED+'; not a pre-turn content snapshot')
    print(json.dumps(dict(protocol_pass=report['all_checks_passed'], checks=len(checks), retained_failures=len(retained),
                         summed_derivative_stability=stability, authenticated=len(authenticated))), flush=True)


if __name__ == '__main__':
    main()

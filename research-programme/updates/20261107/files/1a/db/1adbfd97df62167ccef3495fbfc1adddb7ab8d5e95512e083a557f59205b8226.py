from stage171_direction_common import *
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
    checks.append(dict(name='All preparation and production event identities pass', passed=True))
    check(checks, 'Current source moment failures', sum(not row['passed'] for row in moments), .5)
    config = json.loads((ROOT / 'configuration.json').read_text())
    basis_path = PARENT / 'results/preparation/basis.npz'
    basis = np.load(basis_path)
    mass = basis['mass']
    frozen = np.load(ROOT / 'results/frozen/predictions.npz')
    index = list(frozen['groups']).index('complete_sum')
    for order in range(3):
        summed = combine([(frozen['high'][ordinal, order], frozen['low'][ordinal, order]) for ordinal in range(12)], [1]*12)
        direct = (frozen['high'][index, order], frozen['low'][index, order])
        error = combine([summed, direct], [1, -1])
        relative = norm(error[0]+error[1], mass)/np.maximum(norm(direct[0]+direct[1], mass), 1e-300)
        check(checks, 'Sum/prediction commutation order'+str(order), np.max(relative), 1e-10)
    anchor, unused = source.context(source.START)
    precision = []
    for tag, offset in [('anchor', 0.), ('target', config['delta_log_temperature'])]:
        bundle, theta = source.context(source.START-offset/config['expansion_span'])
        paired = source.PairedHistory(bundle, anchor)
        model = source.models(paired)[0]['difference']
        for node in nodes(theta):
            if node['electron_index'] not in [1, 14]:
                continue
            parameters, weight = source.physics.parameters_and_weight(theta, node)
            with mp.workdps(60):
                low_precision = model.state_correction(parameters)['total']
            with mp.workdps(80):
                high_precision = model.state_correction(parameters)['total']
            values = norm(low_precision-high_precision, mass)/np.maximum(norm(high_precision, mass), 1e-300)
            for column, value in enumerate(values):
                check(precision, f'{tag}:{node["electron_index"]}:state60-vs80:{column}', value, 1e-10)
    checks += precision
    parent_path = PARENT / 'results/stage-integrity.json'
    assert digest(parent_path) == PARENT_SHA
    parent = json.loads(parent_path.read_text())
    stage169 = BRANCH / 'low-frequency-temperature-law-20261019/results/stage-integrity.json'
    assert digest(stage169) == parent['parent_seal_sha256']
    parent169 = json.loads(stage169.read_text())
    stage168 = BRANCH / 'heldout-final-spectrum-20261019/results/stage-integrity.json'
    assert digest(stage168) == parent169['parent_seal_sha256']
    chain = {parent_path: parent, stage169: parent169, stage168: json.loads(stage168.read_text()), **ancestry.ancestors()}
    prior = {PARENT / name for name in parent['file_hashes']}
    prior.update(Path(filename) for filename in hashes if not Path(filename).is_relative_to(ROOT))
    prior.update(path for path in inputs() if not path.is_relative_to(ROOT))
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
    new_events = sorted((ROOT / 'events').rglob('electron-*.npz'))
    assert len(new_events) == 48
    freeze_time = datetime.fromisoformat(packets['results/frozen']['finished_utc'])
    for path in (ROOT / 'events/target').glob('*.npz'):
        with np.load(path) as data:
            assert datetime.fromisoformat(str(data['finished_utc'])) > freeze_time
    assert packets['results/frozen']['known_target_directions'] == 4
    checks.append(dict(name='New target events follow the frozen prediction; four prior directions disclosed', passed=True))
    primary = [row for row in packets['results/frozen']['checks'] if row['name'].startswith('complete_sum:') and
               any(':'+component+':' in row['name'] for component in ['control', 'remainder', 'total'])]
    folder.mkdir(parents=True, exist_ok=True)
    write_json(folder / 'retained-failures.json', retained)
    write_json(folder / 'state-precision-checks.json', precision)
    report = finish(folder, checks, [*map(Path, hashes), *[ROOT / label / 'status.json' for label in required],
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

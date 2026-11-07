from replay239 import *


def freeze_resume():
    config, frozen = replay_protocol()
    assert not (ROOT / 'replay-resume-configuration.json').exists()
    unsealed = ROOT / 'replay/warm-a6-r000.npz'
    assert unsealed.exists() and not unsealed.with_suffix('.json').exists()
    write(ROOT / 'replay-resume-configuration.json', dict(frozen_at=now(), script_sha256=digest(__file__),
        original_replay_configuration=digest(ROOT / 'replay-configuration.json'),
        recovered_array=str(unsealed), recovered_sha256=digest(unsealed),
        repair='Merge case metadata as positional dict argument, avoiding duplicate evaluated_events keyword',
        scientific_code_changed=False, incomplete_report_preserved=True,
        repeat_reason='Confirm the saved unsealed first packet and record its missing metadata; do not overwrite it'))


def resume_protocol():
    config, frozen = replay_protocol()
    resumed = read(ROOT / 'replay-resume-configuration.json')
    assert digest(__file__) == resumed['script_sha256']
    assert digest(ROOT / 'replay-configuration.json') == resumed['original_replay_configuration']
    assert digest(resumed['recovered_array']) == resumed['recovered_sha256']
    return config, frozen, resumed


def run_confirmed(order):
    modest()
    config, frozen, resumed = resume_protocol()
    retained_config = read(REFERENCE / 'configuration.json')
    original, features, models = integration.setup(retained_config)
    candidate_globals = dict(integration.ray_integral.__globals__)
    candidate_globals['Direction'] = RationalDirection
    candidate = types.FunctionType(integration.ray_integral.__code__, candidate_globals, 'exact_rational_ray_integral',
        integration.ray_integral.__defaults__, integration.ray_integral.__closure__)
    assert integration.ray_integral.__globals__['Direction'] is Direction
    inputs = read(ROOT / 'replay-inputs.json')
    modules(inputs)
    for case in frozen['cases']:
        if case['angular_order'] != order:
            continue
        stem = ROOT / 'confirmed-replay' / case_label(case)
        if stem.with_suffix('.json').exists():
            result = read(stem.with_suffix('.json'))
            assert result['configuration_sha256'] == digest(ROOT / 'replay-configuration.json')
            assert result['resume_sha256'] == digest(ROOT / 'replay-resume-configuration.json')
            assert result['sha256'] == digest(stem.with_suffix('.npz'))
            continue
        assert not stem.with_suffix('.npz').exists()
        if time.time() > datetime.fromisoformat(START).timestamp() + 3.7 * 3600:
            print(json.dumps(dict(safe_stop=True, next_case=case_label(case))), flush=True)
            return
        event = next(row for row in config['events'] if row['label'] == case['anchor'])
        local = dict(retained_config, angular_order=order)
        with mp.workdps(frozen['digits']):
            arrays, metadata = candidate(local, event, case['radial_order'], case['ray'], original, features, models)
        assert integration.ray_integral.__globals__['Direction'] is Direction
        assert all(np.all(np.isfinite(value)) for value in arrays.values())
        reference = packet(Path(case['reference_stem']).with_suffix('.npz'))
        checks, records = compare(case, arrays, reference, frozen['replay_tolerance'])
        check(checks, case_label(case) + ':same event count', abs(metadata['evaluated_events'] - case['evaluated_events']), 0)
        if case_label(case) == 'warm-a6-r000':
            recovered = packet(resumed['recovered_array'])
            for name in arrays:
                check(checks, 'saved unsealed calculation identical:' + name, int(not np.array_equal(arrays[name], recovered[name])), 0)
        failed = [entry for entry in checks if not entry['passed']]
        save(stem.with_suffix('.npz'), **arrays)
        write(stem.with_suffix('.json'), dict(case, **metadata, checks=checks, failed=failed, qualified=not failed,
            records=records, sha256=digest(stem.with_suffix('.npz')), configuration_sha256=digest(ROOT / 'replay-configuration.json'),
            resume_sha256=digest(ROOT / 'replay-resume-configuration.json'),
            old_walltime_over_new=case['old_seconds'] / metadata['seconds'],
            timing_note='Historical reference wall time, not a simultaneous controlled full-ray benchmark', finished_at=now()))
        print(json.dumps(dict(case=case_label(case), seconds=metadata['seconds'], checks=len(checks), failures=len(failed),
            maximum_matrix=max(row['matrix'] for row in records), maximum_gas=max(row['gas'] for row in records))), flush=True)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    write(ROOT / 'confirmed-replay' / f'inputs-angular{order}.json', inputs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['freeze', 'run'])
    parser.add_argument('--order', type=int, choices=[6, 8], default=6)
    arguments = parser.parse_args()
    freeze_resume() if arguments.mode == 'freeze' else run_confirmed(arguments.order)

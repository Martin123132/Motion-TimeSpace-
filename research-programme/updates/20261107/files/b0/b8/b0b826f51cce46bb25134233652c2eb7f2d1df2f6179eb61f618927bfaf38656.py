from integrate236 import *
import psutil


def prepare():
    modest()
    for worker in psutil.process_iter(['pid', 'cmdline']):
        command = worker.info.get('cmdline') or []
        assert not any(Path(argument).name == 'integrate236.py' for argument in command), worker.info
    pause = read(ROOT / 'PAUSE-MANIFEST.json')
    assert digest(ROOT / 'integration-configuration.json') == pause['configuration_sha256']
    assert digest(ROOT / 'PAUSED.md') == pause['pause_note_sha256']
    for name, expected in pause['file_hashes'].items():
        assert digest(ROOT / name) == expected, name
    for name, expected in pause['implementation'].items():
        assert digest(ROOT / name) == expected, name
    config, frozen = run_protocol()
    inputs = read(ROOT / 'inputs.json')
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    assert not list(ROOT.rglob('*.partial'))
    target = ROOT / 'resume-configuration.json'
    assert not target.exists()
    write(target, dict(started_at=now(), safe_stop_timestamp=time.time() + 3.75 * 3600,
        previous_turn='progress; user-requested safe pause', restart_sha256=digest(ROOT / 'PAUSE-MANIFEST.json'),
        configuration_sha256=pause['configuration_sha256'], saved_rays=30, consumed_inputs_verified=len(inputs),
        implementation_sha256=digest(Path(__file__)), no_prior_stage_worker=True,
        max_workers=2, threads_per_worker=1, original_bank_changed=False, original_tolerances_changed=False))
    print(json.dumps(dict(restart_verified=True, saved_rays=30, unchanged_inputs=len(inputs))), flush=True)


def resume(order):
    modest()
    frozen = read(ROOT / 'resume-configuration.json')
    assert frozen['implementation_sha256'] == digest(Path(__file__))
    assert frozen['restart_sha256'] == digest(ROOT / 'PAUSE-MANIFEST.json')
    assert frozen['configuration_sha256'] == digest(ROOT / 'integration-configuration.json')
    deadline = frozen['safe_stop_timestamp']
    for anchor in ('warm', 'middle', 'cold'):
        if time.time() >= deadline:
            print(json.dumps(dict(safe_stop=True, order=order, next_anchor=anchor)), flush=True)
            return
        run(anchor, order, 0, 32, deadline)
        completed = len(list((ROOT / 'rays' / anchor / f'order{order}').glob('ray-*.json')))
        if completed != 32:
            print(json.dumps(dict(safe_stop=True, order=order, anchor=anchor, saved_rays=completed)), flush=True)
            return
    print(json.dumps(dict(order=order, all_three_anchors_complete=True, finished_at=now())), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['prepare', 'run'])
    parser.add_argument('--order', type=int, choices=[18, 26], default=18)
    arguments = parser.parse_args()
    prepare() if arguments.mode == 'prepare' else resume(arguments.order)

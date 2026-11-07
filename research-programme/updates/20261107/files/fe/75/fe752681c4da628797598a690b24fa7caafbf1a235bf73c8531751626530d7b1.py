from common236 import *
import psutil

modest()
for worker in psutil.process_iter(['pid', 'name', 'cmdline']):
    command = worker.info.get('cmdline') or []
    assert not any(Path(argument).name == 'integrate236.py' for argument in command), worker.info
assert not list((ROOT / 'rays').rglob('*.partial'))
configuration_hash = digest(ROOT / 'integration-configuration.json')
payloads = {}
counts = {}
for report_path in sorted((ROOT / 'rays').rglob('ray-*.json')):
    report = read(report_path)
    assert report['configuration_sha256'] == configuration_hash
    assert digest(report_path.with_suffix('.npz')) == report['sha256']
    payloads[str(report_path.relative_to(ROOT))] = digest(report_path)
    payloads[str(report_path.with_suffix('.npz').relative_to(ROOT))] = report['sha256']
    key = report['anchor'] + ':order' + str(report['order'])
    counts.setdefault(key, []).append(report['ray'])
for values in counts.values():
    assert values == list(range(len(values)))
assert counts == {'warm:order18': list(range(21)), 'warm:order26': list(range(9))}
write(ROOT / 'PAUSE-MANIFEST.json', dict(state='paused_at_user_request', created_at=now(),
    file_hashes=payloads, configuration_sha256=configuration_hash,
    implementation={path.name: digest(path) for path in ROOT.glob('*.py')},
    counts={key: len(values) for key, values in counts.items()}, next_rays={key: len(values) for key, values in counts.items()},
    active_stage_workers=0, partial_packets=0, complete_stage=False,
    pause_note_sha256=digest(ROOT / 'PAUSED.md')))
print(json.dumps(dict(paused_restart_verified=True, saved_rays=sum(map(len, counts.values())), active_stage_workers=0)), flush=True)

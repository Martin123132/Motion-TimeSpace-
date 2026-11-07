from thermal_wave_common import *


def main():
    modest()
    path = PARENT / 'results/stage-integrity.json'
    parent = json.loads(path.read_text())
    assert parent['state'] == 'complete' and parent['all_current_acceptance_checks_passed']
    assert len(parent['file_hashes']) == 815
    for name, expected in parent['file_hashes'].items():
        assert digest(PARENT / name) == expected, name
    folder = ROOT / 'results/start-guard'
    folder.mkdir(parents=True, exist_ok=False)
    checks = [dict(name='All815 latest-parent payloads rehashed unchanged', passed=True)]
    finish(folder, dict(checks=checks, count=1, all_checks_passed=True, previous_goal_turn='progress',
                        cumulative_prior_entries=8536), __file__)
    print(json.dumps(dict(rehashed=815, previous_goal_turn='progress')), flush=True)


if __name__ == '__main__':
    main()

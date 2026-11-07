from mixed_common import *


def main():
    modest()
    seal = PARENT / 'results/stage-integrity.json'
    packet = json.loads(seal.read_text())
    assert packet['state'] == 'complete' and packet['all_current_acceptance_checks_passed']
    assert len(packet['file_hashes']) == 622
    for name, expected in packet['file_hashes'].items():
        assert digest(PARENT / name) == expected, name
    folder = ROOT / 'results/start-guard'
    folder.mkdir(parents=True, exist_ok=False)
    checks = [dict(name='All622 immediate-parent payloads rehashed unchanged', passed=True)]
    finish(folder, dict(checks=checks, count=1, all_checks_passed=True,
                        previous_goal_turn='progress', cumulative_prior_entries=9158), __file__)
    print(json.dumps(dict(rehashed=622, previous_goal_turn='progress')), flush=True)


if __name__ == '__main__':
    main()

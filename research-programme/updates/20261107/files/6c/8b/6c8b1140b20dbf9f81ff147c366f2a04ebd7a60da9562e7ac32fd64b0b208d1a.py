from scaled_common import *


def main():
    modest()
    packet = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    assert packet['state'] == 'complete' and packet['current_goal_turn'] == 'progress'
    assert not packet['all_requested_numerical_gates_closed']
    assert len(packet['file_hashes']) == 264
    for name, expected in packet['file_hashes'].items():
        assert digest(PARENT / name) == expected, name
    folder = ROOT / 'results/start-guard'
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=[dict(name='All264 parent payloads unchanged and the unresolved band gate retained', passed=True)],
                        count=1, all_checks_passed=True, previous_goal_turn='progress', cumulative_prior_entries=9617), __file__)
    print('Verified264 parent payloads; previous turn made progress; band time gate remains open.', flush=True)


if __name__ == '__main__':
    main()

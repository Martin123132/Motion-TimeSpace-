from observer_common import *


def main():
    modest()
    seal = PARENT / 'results/stage-integrity.json'
    packet = json.loads(seal.read_text())
    assert packet['all_current_acceptance_checks_passed'] and packet['current_goal_turn'] == 'progress'
    assert len(packet['file_hashes']) == 195
    for name, expected in packet['file_hashes'].items():
        assert digest(PARENT / name) == expected, name
    folder = ROOT / 'results/start-guard'
    folder.mkdir(parents=True, exist_ok=False)
    checks = [dict(name='All195 immediate-parent payloads unchanged', passed=True)]
    finish(folder, dict(checks=checks, all_checks_passed=True, count=1,
                        previous_goal_turn='progress', cumulative_prior_entries=9353), __file__)
    print('Parent195 payloads verified; previous goal turn made progress.', flush=True)


if __name__ == '__main__':
    main()

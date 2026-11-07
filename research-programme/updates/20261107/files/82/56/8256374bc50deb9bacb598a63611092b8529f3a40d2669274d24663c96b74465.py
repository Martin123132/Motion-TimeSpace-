from wave_common import *


def main():
    modest()
    folder = ROOT / 'results/start-guard'
    folder.mkdir(parents=True, exist_ok=False)
    seal = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    assert seal['state'] == 'complete' and seal['all_requested_numerical_gates_closed']
    for relative, expected in seal['file_hashes'].items():
        assert digest(PARENT / relative) == expected, relative
    assert len(seal['file_hashes']) == 540 and seal['prior_sealed_entries_unchanged'] == 9725
    checks = [dict(name='Stage79 all540 payloads unchanged', passed=True)]
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=True,
                        parent_chain_expected_entries=10265, previous_goal_turn='progress'), __file__)
    print(json.dumps(dict(checks=len(checks), failed=[])), flush=True)


if __name__ == '__main__':
    main()

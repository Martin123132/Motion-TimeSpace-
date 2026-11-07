from emission_common import *


def main():
    modest()
    folder = ROOT / 'results/start-guard'
    folder.mkdir(parents=True, exist_ok=False)
    path = PARENT / 'results/stage-integrity.json'
    seal = json.loads(path.read_text())
    assert seal['state'] == 'complete' and seal['all_requested_numerical_gates_closed']
    for relative, expected in seal['file_hashes'].items():
        assert digest(PARENT / relative) == expected, relative
    assert len(seal['file_hashes']) == 108
    assert seal['prior_sealed_entries_unchanged'] == 9617
    checks = [dict(name='Stage78 complete and all108 sealed payloads unchanged', passed=True)]
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=True,
        previous_goal_turn='progress', parent_chain_expected_entries=9725), __file__)
    print(json.dumps(dict(checks=len(checks), failed=[])), flush=True)


if __name__ == '__main__':
    main()

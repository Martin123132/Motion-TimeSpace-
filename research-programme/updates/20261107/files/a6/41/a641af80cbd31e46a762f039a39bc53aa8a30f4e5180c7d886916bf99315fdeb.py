from soft_matching_common import *


def main():
    modest()
    folder = ROOT / 'results/start-guard'
    folder.mkdir(parents=True, exist_ok=False)
    seal = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    assert seal['state'] == 'complete'
    for relative, expected in seal['file_hashes'].items():
        assert digest(PARENT / relative) == expected, relative
    assert len(seal['file_hashes']) == 157 and seal['prior_sealed_entries_unchanged'] == 10378
    checks = [dict(name='Stage81 all157 payloads unchanged', passed=True)]
    finish(folder, dict(checks=checks, count=1, all_checks_passed=True,
        parent_chain_expected_entries=10535, previous_goal_turn='progress'), __file__)
    print(json.dumps(dict(checks=1, failed=[])), flush=True)


if __name__ == '__main__':
    main()

from direction_common import *


def main():
    modest()
    folder = ROOT / 'results/preflight'
    folder.mkdir(parents=True, exist_ok=False)
    assert digest(PARENT / 'results/stage-integrity.json') == PARENT_SEAL
    checks = []
    for owner, count in [(PARENT, 13900), (OUTER, 7743)]:
        seal = json.loads((owner / 'results/stage-integrity.json').read_text())
        assert seal['state'] == 'complete' and len(seal['file_hashes']) == count
        for name, expected in seal['file_hashes'].items():
            assert digest(owner / name) == expected, name
        checks.append(dict(name=f'All{count} sealed payloads checked: {owner.name}', passed=True))
    finish(folder, dict(checks=checks, previous_goal_turn='progress', ancestor_failures_preserved=True), __file__,
        [OUTER / 'results/stage-integrity.json'])
    print(json.dumps(dict(state='complete', checked_payloads=21643)), flush=True)


if __name__ == '__main__':
    main()

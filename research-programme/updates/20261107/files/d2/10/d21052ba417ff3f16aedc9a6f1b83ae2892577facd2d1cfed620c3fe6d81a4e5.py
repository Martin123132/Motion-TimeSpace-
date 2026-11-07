from aligned_common import *


def main():
    modest()
    folder = ROOT / 'results/preflight'
    folder.mkdir(parents=True, exist_ok=False)
    seal_path = PARENT / 'results/stage-integrity.json'
    assert digest(seal_path) == PARENT_SEAL
    seal = json.loads(seal_path.read_text())
    assert seal['state'] == 'complete' and len(seal['file_hashes']) == 7743
    for name, expected in seal['file_hashes'].items():
        assert digest(PARENT / name) == expected, name
    baseline = json.loads((PARENT / 'results/node-audit/status.json').read_text())
    assert baseline['all_checks_passed'] and baseline['every_node_loop_identity_verified']
    checks = [dict(name='All7743 sealed Stage95 payloads verified before use', passed=True),
        dict(name='Reused expensive terms retain verified actual-node loop ownership', passed=True)]
    finish(folder, dict(checks=checks, previous_goal_turn='progress', previous_failures_preserved=True),
        __file__, [PARENT / 'results/node-audit/status.json'])
    print(json.dumps(dict(state='complete', parent_payloads=7743)), flush=True)


if __name__ == '__main__':
    main()

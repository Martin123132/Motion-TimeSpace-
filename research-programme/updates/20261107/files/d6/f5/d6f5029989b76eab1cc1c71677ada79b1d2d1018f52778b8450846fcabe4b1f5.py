from thermal_source_common import *


def main():
    modest()
    folder=ROOT/'results/start-guard'
    folder.mkdir(parents=True,exist_ok=False)
    parent=json.loads((PARENT/'results/stage-integrity.json').read_text())
    for relative,expected in parent['file_hashes'].items():
        assert digest(PARENT/relative)==expected,relative
    assert len(parent['file_hashes'])==62
    checks=[dict(name='Stage84 payloads unchanged at continuation',passed=True)]
    finish(folder,dict(checks=checks,count=1,all_checks_passed=True,parent_files=62,
                       previous_goal_turn='progress'),__file__)
    print(json.dumps(dict(parent_files=62,checks=1)),flush=True)


if __name__=='__main__':
    main()

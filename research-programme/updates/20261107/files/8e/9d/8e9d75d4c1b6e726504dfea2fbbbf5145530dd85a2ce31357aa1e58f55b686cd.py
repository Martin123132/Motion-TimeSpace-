from polar_common import *


def main():
    modest()
    locations=[ROOT/'runs'/f'{part}-p3-shard{shard}' for part in ['expensive','control'] for shard in [0,1]]
    assert all((location/'COMPLETE').exists() for location in locations)
    assert json.loads((ROOT/'results/node-audit/status.json').read_text())['all_checks_passed']
    folder=ROOT/'results/combined-source'
    folder.mkdir(parents=True,exist_ok=False)
    totals={key:np.zeros((98,4)) for key in ['difference','virtual','state','control']}
    for location in locations:
        report=json.loads((location/'status.json').read_text())
        assert report['all_checks_passed']
        source=dict(np.load(location/'source.npz'))
        for key in totals:
            if key in source:
                totals[key]+=source[key]
    reference_path=PARENT/'results/combined-source/source.npz'
    reference=dict(np.load(reference_path))
    totals.update({key:reference[key] for key in ['sampled_leading','accurate_leading','mass','temperature','chemical']})
    totals['kinematic_remainder']=totals['control']-totals['sampled_leading']
    totals['remainder']=sum(totals[key] for key in ['kinematic_remainder','difference','virtual','state'])
    totals['total']=totals['accurate_leading']+totals['remainder']
    pair=float(np.max(abs(totals['total'][0]+totals['total'][-1])))
    energy=float(np.max(abs(totals['temperature']@totals['total'][1:-1]-totals['total'][0])))
    scale=max(float(np.max(abs(totals['total'][0]))),1e-30)
    checks=[dict(name='Whole96-mode four-profile source assembled, all pieces retained',passed=bool(np.isfinite(totals['total']).all())),
        dict(name='Independent photon/gas exchange retained',value=pair,passed=pair<1e-6*scale),
        dict(name='Original temperature test matches energy row',value=energy,passed=energy<1e-6*scale)]
    np.savez(folder/'source.npz',**totals)
    finish(folder,dict(checks=checks,physical_electrons=48,scalar_representatives=30,electron_polar=3,
        new_parent_history=False,full_parent_feedback_applied=False),__file__,
        [reference_path,ROOT/'results/node-audit/status.json',*[location/name for location in locations for name in ['status.json','source.npz']]])
    print(json.dumps(dict(checks=checks)),flush=True)


if __name__=='__main__':
    main()

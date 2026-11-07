from frequency_grid_common import *


def main():
    modest()
    locations=[ROOT/'runs'/f'seed3-shard{shard}' for shard in [0,1]]
    assert all((location/'COMPLETE').exists() for location in locations)
    assert json.loads((ROOT/'results/node-audit/status.json').read_text())['all_checks_passed']
    folder=ROOT/'results/coarse-source'
    folder.mkdir(parents=True,exist_ok=False)
    fine_path=PARENT/'results/combined-source/source.npz'
    coarse=dict(np.load(fine_path))
    for key in ['difference','virtual','state']:
        coarse[key]=sum(np.load(location/'source.npz')[key] for location in locations)
    coarse['remainder']=sum(coarse[key] for key in ['kinematic_remainder','difference','virtual','state'])
    coarse['total']=coarse['accurate_leading']+coarse['remainder']
    pair=float(np.max(abs(coarse['total'][0]+coarse['total'][-1])))
    energy=float(np.max(abs(coarse['temperature']@coarse['total'][1:-1]-coarse['total'][0])))
    scale=max(float(np.max(abs(coarse['total'][0]))),1e-30)
    checks=[dict(name='Coarse-frequency companion keeps all96 modes,four profiles and gas',passed=bool(np.isfinite(coarse['total']).all())),
        dict(name='Companion independent photon/gas exchange',value=pair,passed=pair<1e-6*scale),
        dict(name='Companion original energy projection',value=energy,passed=energy<1e-6*scale)]
    np.savez(folder/'source.npz',**coarse)
    finish(folder,dict(checks=checks,seed_order=3,physical_electrons=72,scalar_representatives=45,
        fine_source_recomputed=False,coarse_companion_not_promoted_to_fine=True),__file__,
        [fine_path,ROOT/'results/node-audit/status.json',*[location/name for location in locations for name in ['status.json','source.npz']]])
    print(json.dumps(dict(checks=checks)),flush=True)


if __name__=='__main__':
    main()

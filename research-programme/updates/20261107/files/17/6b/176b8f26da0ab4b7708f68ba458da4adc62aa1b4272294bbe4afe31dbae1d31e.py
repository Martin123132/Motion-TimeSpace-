from residual_kinetic_common import *


def main():
    modest()
    folder=ROOT/'results/baseline-refinement'
    folder.mkdir(parents=True,exist_ok=False)
    specification=json.loads((BRANCH/'temperature-distortion-projection-20261012/results/projection/status.json').read_text())['basis_specification']
    basis=infrared_ladder.ConsistentBasis(**specification)
    readout=ResidualMap(basis)
    checks,inputs,summaries=[],[],{}
    for model in ['heavy','cold']:
        histories={}
        packets={}
        for label,steps,bank in [('leading',3200,'s700-i160'),('leading',6400,'s700-i160'),('refined',6400,'s960-i256')]:
            path=BASELINE/f'{model}-nonlocal-{label}-{steps}/history.npz'
            status=path.parent/'status.json'
            inputs.extend([path,status])
            packet=json.loads(status.read_text())
            assert packet['all_checks_passed'] and packet['bank']==bank and packet['mode']=='nonlocal-leading'
            assert packet['basis_spec']==specification
            with np.load(path) as saved:
                indices=np.arange(steps//2,steps+1,steps//128)
                assert len(indices)==65
                histories[(label,steps)]=dict(coordinate=saved['expansion'][indices],photon=saved['profiles'][indices],
                    residual=np.einsum('ij,nj->ni',readout.mapping,saved['profiles'][indices]))
            packets[(label,steps)]=packet
        comparisons={}
        for name,reference_key,other_key in [('matched_lower_bank_timestep',('leading',6400),('leading',3200)),
                                            ('matched6400_bank_refinement',('refined',6400),('leading',6400))]:
            reference,other=histories[reference_key],histories[other_key]
            assert np.max(abs(reference['coordinate']-other['coordinate']))<1e-13
            norm_history=np.sqrt(np.sum(basis.measure*reference['residual']**2,axis=1))
            differences=np.sqrt(np.sum(basis.measure*(reference['residual']-other['residual'])**2,axis=1))
            relative=differences/np.maximum(norm_history,1e-300)
            comparisons[name]=dict(maximum_relative=float(relative.max()),endpoint_relative=float(relative[-1]),
                identical_frequency_and_template_projection=True)
            checks.append(dict(name=name+':'+model,value=float(relative.max()),limit=.01,
                passed=bool(relative.max()<.01)))
        with np.load(ROOT/'results/kinetic-drive'/f'{model}-1024.npz') as current:
            difference=histories[('refined',6400)]['residual']-current['primary_residual'][:,:,0]
            value=float(np.max(abs(difference))/max(np.max(abs(current['primary_residual'][:,:,0])),1e-300))
            checks.append(dict(name='Primary baseline replay:'+model,value=value,limit=1e-12,passed=value<1e-12))
        inputs.append(ROOT/'results/kinetic-drive'/f'{model}-1024.npz')
        summaries[model]=comparisons
    finish(folder,dict(checks=checks,models=summaries,
        same_s960_bank_baseline_timestep_control_available=False,
        same_s700_bank_baseline_timestep_control_available=True,
        new_history_run=False,source_sweep=False,unchanged_saved_rules=True),__file__,inputs)
    print(json.dumps(dict(checks=checks,models=summaries)),flush=True)


if __name__=='__main__':
    main()

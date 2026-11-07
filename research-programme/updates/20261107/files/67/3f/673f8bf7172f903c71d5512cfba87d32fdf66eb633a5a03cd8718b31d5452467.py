from carry_common import *


def main():
    modest()
    folder=ROOT/'results/memory-contract'
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows,inputs=[],{},[]
    for model in ['heavy','cold']:
        carry_folder=ROOT/'results'/f'evolution-{model}-carry'
        reset_folder=ROOT/'results'/f'evolution-{model}-reset'
        carry=read_npz(carry_folder/'prediction.npz')
        reset=read_npz(reset_folder/'prediction.npz')
        measure=(carry['frequency']/carry['frequency'][-1])**3
        archives_carry=[PARENT/'results'/f'replay-{model}-cubic/checkpoints/restart-00640.npz']
        archives_reset=[P129/'results'/f'replay-{model}-control/checkpoints/restart-00640.npz']
        archives_carry.extend(carry_folder/'checkpoints'/f'restart-{step:05d}.npz' for step in range(720,1281,80))
        archives_reset.extend(reset_folder/'checkpoints'/f'restart-{step:05d}.npz' for step in range(720,1281,80))
        energies=[]
        for left_path,right_path in zip(archives_carry,archives_reset):
            left,right=map(read_npz,[left_path,right_path])
            for key in ['old_outer','older_outer']:
                assert np.array_equal(left[key],right[key])
            delta=left['error']-right['error']
            previous_delta=left['previous_error']-right['previous_error']
            energy=np.sum(measure[:,None]*(delta**2+(2*delta-previous_delta)**2),axis=0)/4
            energies.append(energy)
            inputs.extend([left_path,left_path.with_suffix('.json'),right_path,right_path.with_suffix('.json')])
        energies=np.array(energies)
        ratios=energies[1:]/np.maximum(energies[:-1],1e-300)
        endpoint_relative=np.max(abs(carry['defect'][-1]-reset['defect'][-1]),axis=0)/np.maximum(np.max(abs(carry['defect'][-1]),axis=0),1e-300)
        checks.append(dict(name='Identical carry/reset external histories:'+model,passed=True))
        checks.append(dict(name='Nonzero inherited corrected memory:'+model,passed=bool(np.all(energies[0]>0))))
        for column,values in zip(['baseline','join1','join2'],ratios.T):
            checks.append(check('Memory G-norm contraction:'+model+':'+column,float(np.max(values)),1+1e-8))
        rows[model]=dict(energy=energies.tolist(),interval_ratios=ratios.tolist(),initial_to_final_ratio=(energies[-1]/energies[0]).tolist(),
            endpoint_memory_relative=endpoint_relative.tolist(),memory_norm_is_physical_energy=False)
        np.savez_compressed(folder/(model+'-memory.npz'),steps=np.arange(640,1281,80),energy=energies,
            endpoint_difference=carry['defect'][-1]-reset['defect'][-1])
        inputs.extend([carry_folder/'prediction.npz',reset_folder/'prediction.npz',carry_folder/'status.json',reset_folder/'status.json'])
    assert all(row['passed'] for row in checks),[row for row in checks if not row['passed']]
    chain=ancestors()
    for path in inputs:
        if not Path(path).is_relative_to(ROOT):
            verify_source(path,chain)
    finish(folder,dict(checks=checks,models=rows),__file__,inputs)
    print(json.dumps(rows),flush=True)


if __name__=='__main__':
    main()

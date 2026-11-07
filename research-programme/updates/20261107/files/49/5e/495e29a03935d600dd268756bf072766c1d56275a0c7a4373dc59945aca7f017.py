import argparse
from resolved_redistribution import *


def main():
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--name',required=True)
    parser.add_argument('--electron',type=int,default=2)
    parser.add_argument('--angular',type=int,default=2)
    parser.add_argument('--frequency',type=int,default=4)
    parser.add_argument('--soft',type=int,default=12)
    parser.add_argument('--minimum',type=float,default=1e-5)
    arguments=parser.parse_args()
    folder=ROOT/'results'/arguments.name
    folder.mkdir(parents=True,exist_ok=False)
    metadata,saved,spectrum=snapshot()
    theta=metadata['reference_temperature']
    started=time.perf_counter()
    def progress(done,total,count,matrix,current):
        write_json(folder/'progress.json',dict(state='running',electron_nodes_done=done,electron_nodes_total=total,
                                             events=count,elapsed=time.perf_counter()-started))
        np.savez_compressed(folder/'partial.npz',matrix=matrix,source_scaled=current)
        print(arguments.name+' '+str(done)+'/'+str(total)+' '+str(round(time.perf_counter()-started,1))+'s',flush=True)
    matrix,current,details=integrate_resolved(theta,metadata['gas_temperature_scaled'],spectrum,
        arguments.electron,arguments.electron,arguments.angular,arguments.frequency,arguments.soft,
        arguments.minimum,metadata['basis_spec']['maximum'],progress)
    heat=np.array([0.,1,0,0,1])
    scale=max(np.linalg.norm(matrix),1e-30)
    checks=[check('Resolved DC weak block is symmetric',np.linalg.norm(matrix-matrix.T)/scale,1e-12),
            check('Resolved DC entropy is nonincreasing',max(0.,np.linalg.eigvalsh(matrix).max())/scale,1e-12),
            check('Common-temperature mode follows event kinematics',np.linalg.norm(matrix@heat)/scale,1e-12),
            check('Saved-spectrum photon plus gas heating closes',abs(current[1]+current[4])/max(np.linalg.norm(current),1e-30),1e-10),
            dict(name='Resolved photon production is retained',passed=bool(matrix[0,0]<0 and current[0]!=0))]
    np.savez_compressed(folder/'operator.npz',matrix=matrix,source_scaled=current,source_physical=metadata['heat']*current,
                        common_temperature=heat)
    report=dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),arguments=vars(arguments),
                elapsed=time.perf_counter()-started,details=details,matrix=matrix.tolist(),source_scaled=current.tolist(),
                source_physical=(metadata['heat']*current).tolist(),basis=['photon number','photon energy','x^2/(1+x)','x^3/(1+x)^2','gas heat'],
                time_unit='Thomson optical time d_tau=n_e sigma_T c dt',moment_unit='Reference photon energy density with dimensionless frequency x=E/T',
                real_forward_and_inverse_both_included=True,virtual_matched=False,infrared_below_minimum_included=False,
                saved_spectrum_evaluated=True,new_time_evolution=False)
    finish(folder,report,__file__,[ROOT/'resolved_redistribution.py',ROOT/'batched_real.py',ROOT/'results/saved-state/status.json',
           ROOT/'results/saved-state/state.npz',PARENT/'reduced_amplitude.py',PARENT/'polarized_source.py',
           folder/'operator.npz',folder/'partial.npz',folder/'progress.json'])
    print(json.dumps(dict(name=arguments.name,elapsed=report['elapsed'],failed=[row for row in checks if not row['passed']],source=current.tolist())),flush=True)


if __name__=='__main__':
    main()

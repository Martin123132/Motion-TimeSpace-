from __future__ import annotations

from collision_common import *
from compare_photon_baryon import solve


def main():
    modest()
    folder=ROOT/'results/photon-reference-refined'
    folder.mkdir(parents=True,exist_ok=False)
    inputs=[ROOT/'compare_photon_baryon.py',NATIVE/'fortran/equations.f90',NATIVE/'camb/cambdll.dll']
    rows=[]
    checks=[]
    columns=['delta_photon','v_photon','pi_photon','v_baryon_cdm','delta_baryon']
    report=dict(state='running',pid=os.getpid(),completed=0,total=4)
    write_json(folder/'status.json',report)
    for label,source_name in [('heavy','unmatched-base.npz'),('cold','cold-base.npz')]:
        original=ROOT/'runs/backgrounds'/(label+'.npz')
        source=HISTORY/'runs/sources'/source_name
        inputs.extend([original,source])
        with np.load(original) as saved:
            packet={name:saved[name].copy() for name in saved.files}
        times=packet['times']
        names=list(packet['names'])
        for boost in [5.,10.]:
            started=time.monotonic()
            params=inherited.inherited.inherited.inherited.inherited.params_for(source)
            original_boost=float(params.Accuracy.AccuracyBoost)
            params.Accuracy.AccuracyBoost=boost
            params.Accuracy.IntTolBoost=6
            native=camb.get_background(params)
            packet['values']=native.get_time_evolution([.1],times,vars=names,lAccuracyBoost=4)[0]
            thermal=native.get_background_time_evolution(times,vars=['opacity','cs2b','T_b','x_e'])
            packet.update(thermal)
            packet['scales']=np.ascontiguousarray(packet['values'][:,names.index('a')])
            densities=native.get_background_densities(packet['scales'],vars=['baryon','photon'])
            packet['ratio']=.75*densities['baryon']/densities['photon']
            sample_times,independent,steps=solve(packet,.025,24)
            reference=interpolate.CubicSpline(times,packet['values'][:,[names.index(name) for name in columns]])(sample_times)
            envelopes=np.maximum(np.max(abs(reference),axis=0),1e-10)
            errors=np.max(abs(independent-reference),axis=0)/envelopes
            row=dict(model=label,accuracy_boost=boost,original_accuracy_boost=original_boost,
                native_errors=errors.tolist(),steps=steps,seconds=time.monotonic()-started)
            rows.append(row)
            np.savez_compressed(folder/(label+'-boost'+str(int(boost))+'.npz'),times=sample_times,
                independent=independent,native=reference,envelopes=envelopes,errors=errors,columns=columns,
                native_times=times,native_values=packet['values'],names=names,opacity=packet['opacity'])
            checks.append(dict(name=label+' accuracy'+str(boost)+': finite values and unchanged gates',
                passed=bool(np.isfinite(independent).all() and np.max(errors[[0,1,3,4]])<.002 and errors[2]<.005),errors=errors.tolist()))
            report.update(completed=report['completed']+1,last=row)
            write_json(folder/'status.json',report)
            print(json.dumps(row),flush=True)
    passed=all(row['passed'] for row in checks)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=passed,rows=rows,
        original_results_unchanged=True,accuracy_boost_changes_several_native_approximations=True,
        isolated_tight_coupling_toggle=False,no_new_fitted_parameter=True),__file__,inputs)
    assert passed,checks


if __name__=='__main__':
    main()


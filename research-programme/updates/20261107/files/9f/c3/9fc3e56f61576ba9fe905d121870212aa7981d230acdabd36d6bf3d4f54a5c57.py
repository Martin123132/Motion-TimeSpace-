from __future__ import annotations

from constraint_common import *
from reconstruct_neutrinos import response


def main():
    modest()
    folder=ROOT/'results/neutrino-refined'
    folder.mkdir(parents=True,exist_ok=False)
    inputs=[ROOT/'reconstruct_neutrinos.py',NATIVE/'fortran/equations.f90',NATIVE/'camb/cambdll.dll']
    checks=[]
    rows=[]
    for label,source_name in [('heavy','unmatched-base.npz'),('cold','cold-base.npz')]:
        original=ROOT/'runs/native'/(label+'.npz')
        inputs.append(original)
        old=np.load(original)
        times=old['conformal_time']
        names=list(old['names'])
        source=HISTORY/'runs/sources'/source_name
        inputs.append(source)
        params=inherited.inherited.inherited.inherited.params_for(source)
        native=camb.get_background(params)
        native.Params.Accuracy.IntTolBoost=6
        field_values=[]
        for boost in [8,12]:
            values=native.get_time_evolution([1.],times,vars=names,lAccuracyBoost=boost)[0]
            field_values.append(values)
            _,volume_rate,_,_=inherited.metric(1.,np.array([1.,0.,0.]),names,values,float(old['baryon_fraction']))
            shear_rate=-values[:,names.index('H')]*values[:,names.index('v_newtonian_cdm')]
            ratio=(7/8)*(4/11)**(4/3)*float(old['effective_neutrino_number'])
            fraction=ratio/(1+ratio)
            eta=values[0,names.index('etak')]
            initial=[values[0,names.index('delta_neutrino')],values[0,names.index('v_neutrino')],
                eta*(4/3)*times[0]**2/(15+4*fraction),eta*(4/21)*times[0]**3/(15+4*fraction)]
            independent,nfev=response(1.,times,volume_rate,shear_rate,initial,160)
            reference=values[:,[names.index('delta_neutrino'),names.index('v_neutrino')]]
            envelope=np.maximum(np.max(abs(reference),axis=0),1e-10)
            errors=np.max(abs(independent[:,:2]-reference),axis=0)/envelope
            row=dict(model=label,boost=boost,native_errors=errors.tolist(),expected_ufa_switch_tau=14*boost-4,
                end_tau=float(times[-1]),nfev=nfev)
            rows.append(row)
            checks.append(dict(name=label+' hierarchy'+str(boost)+': native kinetic response agreement',passed=bool(np.max(errors)<.0015),errors=errors.tolist()))
            np.savez_compressed(folder/(label+'-boost'+str(boost)+'.npz'),times=times,names=names,values=values,
                independent_moments=independent,native_density_momentum=reference,errors=errors,initial_moments=initial)
            print(json.dumps(row),flush=True)
        fine=field_values[-1]
        previous=field_values[0]
        native_error=[]
        for name in ['delta_neutrino','v_neutrino','delta_cdm','delta_baryon','etak','mts_dphi_s','mts_dphidot_s','mts_dphi_h','mts_dphidot_h']:
            column=names.index(name)
            envelope=max(float(np.max(abs(fine[:,column]))),1e-300)
            original_error=float(np.max(abs(fine[:,column]-old['values'][2,:,column])))/envelope
            refined_error=float(np.max(abs(fine[:,column]-previous[:,column])))/envelope
            native_error.append(dict(column=name,old4_to12_envelope_error=original_error,new8_to12_envelope_error=refined_error))
        checks.append(dict(name=label+': hierarchy12 does not enter high-ktau approximation',passed=bool(times[-1]<164)))
        checks.append(dict(name=label+': density and metric8/12 agreement',passed=all(row['new8_to12_envelope_error']<.0015 for row in native_error)))
        write_json(folder/(label+'-history-comparison.json'),native_error)
    old_report=json.loads((ROOT/'results/neutrino-response/status.json').read_text())
    rejected=[row for row in old_report['checks'] if not row['passed']]
    checks.append(dict(name='Original failed tests retained as common native approximation evidence',passed=len(rejected)==2))
    assert all(row['passed'] for row in checks),checks
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,rows=rows,
        superseded_failures=rejected,original_failures_not_relabelled_passes=True,
        root_cause='Native switches to high_ktau_neutrino_approx at k*tau=max(20,lmaxnr-4); lmaxnr=14*lAccuracyBoost here. Boost4 switches at52; boost12 stays unswitched across this history.',
        acceptance_thresholds_unchanged=True,original_sealed_histories_not_modified=True),__file__,[*inputs,ROOT/'results/neutrino-response/status.json'])


if __name__=='__main__':
    main()

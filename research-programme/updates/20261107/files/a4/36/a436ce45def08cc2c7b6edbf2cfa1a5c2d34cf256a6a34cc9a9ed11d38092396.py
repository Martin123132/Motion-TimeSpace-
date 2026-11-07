from matched_feedback_common import *


def main():
    modest()
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    for profile_variant,transport_variant in [('fine','space'),('space','fine')]:
        label=profile_variant+'-'+transport_variant+'-transport'
        folder=ROOT/'results'/('sources-'+label)
        folder.mkdir(parents=True,exist_ok=False)
        checks,inputs,summaries=[],[*ladder.inputs],{}
        for model in ['heavy','cold']:
            source_path=ROOT/'results'/f'sources-{profile_variant}-q32-m40'/(model+'.npz')
            inputs.extend([source_path,source_path.parent/'status.json'])
            with np.load(source_path) as archive:
                data={key:archive[key].copy() for key in archive.files}
            profile,profiles,gas,paths=read_prediction(model,profile_variant)
            transport,unused_photon,unused_gas,transport_paths=read_prediction(model,transport_variant)
            inputs.extend([*paths,*transport_paths])
            frequency,weights=log_rule([2e-5,4e-5,.0003,.001,.003,.01,.04],32)
            values=basis.evaluate(frequency)
            spacing=math.log(transport['frequency'][1]/transport['frequency'][0])
            ratios=np.exp(transport['offsets']*spacing)
            adjoints=[]
            for ratio in ratios:
                local=(basis.evaluate(frequency*ratio)-values+(basis.evaluate(frequency/ratio)-values)/ratio).T*weights/(2*I3)
                local[0]=0
                local[1]=frequency*(ratio-1+(1/ratio-1)/ratio)*weights/(2*I3*basis.norms[1])
                adjoints.append(local)
            adjoints=np.array(adjoints)
            correction=CompactCorrection(basis,profile['frequency'],.04)
            correction.register('quadrature',frequency)
            count=len(transport['offsets'])
            bank_at=interpolate.interp1d(transport['coefficient_knots'],transport['coefficient_bank'],axis=0,bounds_error=True)
            for epoch,position in enumerate(profile['coordinate']):
                spline=interpolate.CubicSpline(np.log(profile['frequency']),profile['slope'][epoch],axis=0,extrapolate=False)
                replacement=correction.at('quadrature',spline,profiles[epoch])
                if epoch==0:
                    replacement*=0
                kernel=bank_at(position)[:count]/ratios
                data['raw_source'][epoch,0]=np.einsum('j,jif->if',kernel,adjoints)@replacement
            data['source']=data['raw_source']-data['overlap_source']
            data['number_source']=np.einsum('i,ntik->ntk',basis.chemical,data['source'])
            data['energy_source']=np.einsum('i,ntik->ntk',basis.temperature,data['source'])
            assert all(np.isfinite(value).all() for value in data.values() if value.dtype.kind not in ['U','S'])
            value=float(np.max(abs(np.einsum('i,nik->nk',basis.chemical,data['raw_source'][:,0]))))
            checks.append(dict(name='Compton number invariant under transport-only swap:'+model,value=value,passed=value==0.))
            with np.load(source_path) as original:
                checks.append(dict(name='DC,BR and projected moments unchanged by transport swap:'+model,
                    passed=bool(np.array_equal(data['source'][:,1:],original['source'][:,1:]) and np.array_equal(data['projected_replacement'],original['projected_replacement']))))
            np.savez_compressed(folder/(model+'.npz'),**data)
            summaries[model]=dict(profile_variant=profile_variant,transport_variant=transport_variant)
        finish(folder,dict(checks=checks,models=summaries,variant=profile_variant,quadrature_order=32,
            match_upper=.04,columns=['baseline','join1','join2'],
            transport_variant=transport_variant,diagnostic_swap=True,new_parent_history=False,
            overlap_subtracted=True,stored_moment_derivative_accounted=True,soft_compton_extension=True,
            full_finite_frequency_compton_extension=False,matched_dc_all_legs=True,fitted_cutoff=False),__file__,inputs)
        print(json.dumps(dict(case=label,checks=checks)),flush=True)


if __name__=='__main__':
    main()

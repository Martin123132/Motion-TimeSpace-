from direct_common import *


def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--bank',required=True)
    parser.add_argument('--variant',choices=['fine','space','time'],default='fine')
    args=parser.parse_args()
    modest()
    bank_folder=ROOT/'results'/args.bank
    metadata=json.loads((bank_folder/'status.json').read_text())
    assert metadata['all_checks_passed']
    bank=read_npz(bank_folder/'bank.npz')
    upper=metadata['match_upper']
    label=args.variant+'-'+args.bank.removeprefix('bank-')
    folder=ROOT/'results'/('sources-'+label)
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    inputs=[*ladder.inputs,bank_folder/'bank.npz',bank_folder/'status.json']
    checks,models=[],{}
    for model in ['heavy','cold']:
        prediction,profiles,gas,dependencies=read_prediction(model,args.variant)
        inputs.extend(dependencies)
        path=PARENT/'results'/f'sources-{args.variant}-q32-m{int(upper*1000)}'/(model+'.npz')
        verify_source(path,chain)
        original=read_npz(path)
        inputs.extend([path,path.parent/'status.json'])
        assert np.array_equal(original['coordinate'],bank['coordinate'])
        assert np.array_equal(original['profiles'],profiles)
        correction=CompactCorrection(basis,prediction['frequency'],upper)
        correction.register('source',bank['frequency'])
        replacements=[]
        for epoch in range(len(bank['coordinate'])):
            spline=interpolate.CubicSpline(np.log(prediction['frequency']),prediction['slope'][epoch],axis=0,extrapolate=False)
            value=correction.at('source',spline,profiles[epoch])
            if epoch==0:
                value=np.zeros_like(value)
            replacements.append(bank['adjoint'][epoch]@value)
        data={key:value.copy() for key,value in original.items()}
        data['raw_source'][:,0]=np.array(replacements)
        data['source']=data['raw_source']-data['overlap_source']
        data['number_source']=np.einsum('i,ntik->ntk',basis.chemical,data['source'])
        data['energy_source']=np.einsum('i,ntik->ntk',basis.temperature,data['source'])
        data['compton_event_order']=np.array(metadata['event_order'])
        data['compton_panel_order']=np.array(metadata['quadrature_order'])
        data['physical_doppler_shifts']=np.array(True)
        for key in ['overlap_source','projected_replacement','replacement_moments','replacement_norm','unresolved_norm',
                    'projection_quadrature_difference','profiles','gas']:
            assert np.array_equal(data[key],original[key]),key
        assert np.array_equal(data['raw_source'][:,1:],original['raw_source'][:,1:])
        assert np.count_nonzero(data['source'][0])==0
        assert np.isfinite(data['source']).all()
        number=np.einsum('i,nik->nk',basis.chemical,data['raw_source'][:,0])
        checks.extend([check('Compton number invariant:'+model,np.max(abs(number)),1e-14),
            dict(name='Only raw Compton changed;stored moments,DC,BR,overlap and histories identical:'+model,passed=True),
            dict(name='Analytic zero initial replacement:'+model,passed=True)])
        np.savez_compressed(folder/(model+'.npz'),**data)
        norms=dual_norm(data['raw_source'][:,0],basis)
        changes=dual_norm(data['raw_source'][:,0]-original['raw_source'][:,0],basis)
        models[model]=dict(maximum_direct_raw_compton_dual_norm=norms.max(axis=0).tolist(),
            maximum_change_over_direct_scale=(changes.max(axis=0)/np.maximum(norms.max(axis=0),1e-300)).tolist())
    finish(folder,dict(checks=checks,models=models,variant=args.variant,match_upper=upper,
        event_order=metadata['event_order'],compton_panel_order=metadata['quadrature_order'],
        dcbr_panel_order_unchanged=32,columns=['baseline','join1','join2'],parent_history_rerun=False,
        physical_shift_grid_deposition=False,source_bank=args.bank),__file__,inputs)


if __name__=='__main__':
    main()


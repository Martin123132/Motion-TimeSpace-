from turnover_common import *


def main():
    modest()
    folder=ROOT/'results/invariant-banks'
    folder.mkdir(parents=True,exist_ok=False)
    inputs=[ROOT/'INVARIANT-INTERPOLATION.md']
    clock_banks={}
    for model in ['heavy','cold']:
        path=TAIL/'runs'/(model+'-production')/'tail.npz'
        inputs.append(path)
        with np.load(path) as saved:
            selected=saved['coefficient_knots']>=math.log(10)/2-1e-12
            times=saved['coefficient_knots'][selected].copy()
            count=len(saved['offsets'])
            clock_banks[model]=saved['coefficient_bank'][selected,count:count+3].copy()
            original_spacing=float(np.log(saved['frequency'][1]/saved['frequency'][0]))
    assert len(times)==65
    background=thermal_wave.thermal.ThermalBackground('heavy')
    inputs.extend([background.parent.source,background.native_constants])
    events=[]
    for coordinate in times:
        theta=background.at(float(coordinate))['thermal_parameter']
        ratios,conductance=tail.jump_events(theta,6)
        events.append((np.log(ratios),conductance))
    checks,metadata,files=[],{},{}
    for label,factor in [('invariant',1),('invariant-half',2)]:
        spacing=original_spacing/factor
        margin=int(math.ceil(max(float(np.max(abs(shifts))) for shifts,weights in events)/spacing))+2
        offsets=np.arange(-margin,margin+1)
        banks=[]
        largest_mode_error,largest_weight_error,minimum_weight=0.,0.,1.
        for shifts,conductance in events:
            lower=np.floor(shifts/spacing).astype(int)
            upper_weight=(-np.expm1(-(shifts-lower*spacing)))/(-np.expm1(-spacing))
            lower_weight=1-upper_weight
            assert lower.min()>=offsets[0] and (lower+1).max()<=offsets[-1]
            minimum_weight=min(minimum_weight,float(min(upper_weight.min(),lower_weight.min())))
            stencil=np.zeros(len(offsets))
            np.add.at(stencil,lower-offsets[0],conductance*lower_weight)
            np.add.at(stencil,lower+1-offsets[0],conductance*upper_weight)
            stencil[-offsets[0]]-=conductance.sum()
            eigenvalue=float(conductance@(-np.expm1(-shifts)))
            chemical=float(stencil@np.exp(-offsets*spacing)+eigenvalue)
            largest_mode_error=max(largest_mode_error,abs(chemical)/max(abs(eigenvalue),1e-300))
            reconstructed=lower_weight*np.exp(-lower*spacing)+upper_weight*np.exp(-(lower+1)*spacing)
            largest_weight_error=max(largest_weight_error,float(np.max(abs(reconstructed-np.exp(-shifts)))))
            banks.append(np.r_[stencil,eigenvalue])
        banks=np.array(banks)
        checks.extend([
            dict(name='Positive interpolation weights:'+label,value=minimum_weight,passed=minimum_weight>=-1e-14),
            dict(name='Constant chemical potential preserved:'+label,value=largest_mode_error,limit=1e-10,passed=largest_mode_error<=1e-10),
            dict(name='Exponential interpolation identity:'+label,value=largest_weight_error,limit=1e-14,passed=largest_weight_error<=1e-14),
            dict(name='Constant slope jump row sum:'+label,value=float(abs(banks[:,:len(offsets)].sum(axis=1)).max()),
                 passed=bool(abs(banks[:,:len(offsets)].sum(axis=1)).max()<1e-14))])
        for model in ['heavy','cold']:
            target=ROOT/(label+'-banks')/'runs'/(model+'-production')
            target.mkdir(parents=True,exist_ok=False)
            coefficient_bank=np.column_stack([banks,clock_banks[model][:,1:]])
            path=target/'tail.npz'
            np.savez(path,frequency=1e-6*np.exp(spacing*np.arange(2)),
                coefficient_knots=times,coefficient_bank=coefficient_bank,offsets=offsets)
            files[str(path)]=digest(path)
            checks.append(dict(name='Same physical lambda1 as cached events:'+label+':'+model,
                value=float(np.max(abs(banks[:,-1]-clock_banks[model][:,0])/abs(clock_banks[model][:,0]))),
                passed=bool(np.max(abs(banks[:,-1]-clock_banks[model][:,0])/abs(clock_banks[model][:,0]))<1e-10)))
        metadata[label]=dict(spacing=spacing,offset_count=len(offsets),maximum_chemical_mode_relative_error=largest_mode_error)
    finish(folder,dict(checks=checks,files=files,banks=metadata,soft_velocity_temperature_nodes=65,
        event_order=6,finite_frequency_source_evaluations=0,physical_coefficients_fitted=False,
        parent_history_rerun=False,old_predictions_unchanged=True),__file__,inputs)
    print(json.dumps(dict(checks=checks,metadata=metadata)),flush=True)


if __name__=='__main__':
    main()

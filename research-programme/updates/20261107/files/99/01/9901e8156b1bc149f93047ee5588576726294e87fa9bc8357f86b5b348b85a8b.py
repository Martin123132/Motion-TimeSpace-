from history_source_common import *


def main():
    modest()
    folder=ROOT/'results/energy-defect-audit'
    folder.mkdir(parents=True,exist_ok=False)
    anchor_path=ROOT/'results/anchor-source/source.npz'
    anchor=dict(np.load(anchor_path))
    bundle=EpochBundle()
    basis=bundle.basis
    checks,inputs,rows=[],[anchor_path,*bundle.inputs],[]
    for model in ['heavy','cold']:
        background=thermal_wave.thermal.ThermalBackground(model)
        path=ROOT/'results/history-response'/f'{model}-512.npz'
        raw=dict(np.load(path))
        counts=len(raw['coordinate'])-1
        step=float(raw['coordinate'][1]-raw['coordinate'][0])
        selection=slice(0,2) if model=='heavy' else slice(2,4)
        integrated,old_integrated=np.zeros((2,6)),np.zeros((2,6))
        histories=[integrated.copy()]
        for index,coordinate in enumerate(raw['coordinate'][1:],1):
            phase=index/counts
            midpoint=anchor['midpoint'][:,selection]
            source=np.column_stack([(1-phase)*anchor[key][:,selection]+phase*midpoint
                for key in ['quarter','temperature_only']]+[midpoint])
            local=background.at(float(coordinate))
            rate=local['coefficient']/local['thermal_parameter']
            projection=basis.temperature@source[1:-1]-source[0]
            pairing=source[0]+source[-1]
            forcing=rate*np.vstack([projection,pairing])
            if index==1:
                alpha=1/step
                history=integrated/step
            else:
                alpha=1.5/step
                history=(2*integrated-.5*old_integrated)/step
            updated=(history+forcing)/alpha
            old_integrated,integrated=integrated,updated
            histories.append(integrated.copy())
        histories=np.asarray(histories)
        expected=histories.sum(axis=1)
        observed=raw['energy']+background.chi*raw['gas']+raw['work']
        residual=observed-expected
        observed_scale=np.maximum(np.max(abs(observed),axis=0),1e-300)
        physical_scale=np.maximum(np.max(abs(raw['energy'])+abs(background.chi*raw['gas'])+abs(raw['work']),axis=0),1e-300)
        rows.append(dict(model=model,relative_unexplained_to_raw_imbalance=(np.max(abs(residual),axis=0)/observed_scale).tolist(),
            relative_unexplained_to_energy_scale=(np.max(abs(residual),axis=0)/physical_scale).tolist(),
            final_observed=observed[-1].tolist(),final_integrated_source_defect=expected[-1].tolist(),
            final_projection_defect=histories[-1,0].tolist(),final_pair_defect=histories[-1,1].tolist()))
        checks.append(dict(name='All raw energy-defect contributions retained and finite:'+model,
            passed=bool(np.isfinite(histories).all() and np.isfinite(residual).all())))
        np.savez(folder/f'{model}.npz',coordinate=raw['coordinate'],raw_imbalance=observed,
            integrated_projection=histories[:,0],integrated_event_pair=histories[:,1],unexplained=residual)
        inputs.extend([path,path.parent/'status.json',background.parent.source,background.native_constants])
    finish(folder,dict(checks=checks,rows=rows,scope='Diagnostic accounting,not a conservation pass or a bound on continuum error.'),__file__,inputs)
    print(json.dumps(dict(rows=rows)),flush=True)


if __name__=='__main__':
    main()

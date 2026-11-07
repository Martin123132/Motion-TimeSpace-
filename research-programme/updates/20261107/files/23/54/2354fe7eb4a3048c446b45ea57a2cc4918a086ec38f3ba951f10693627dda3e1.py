from decimal import Decimal,localcontext
from projection_common import *


def exact_readout(basis,frequency,photon,energy,precision):
    with localcontext() as context:
        context.prec=precision
        convert=lambda value:Decimal(float(value))
        capacity=convert(float(basis.energy@basis.temperature))
        norms=[convert(value) for value in basis.norms]
        mean,pivot=convert(basis.mean),convert(basis.pivot)
        coefficients=[[convert(value) for value in column] for column in photon.T]
        eta=[convert(value)/capacity for value in energy]
        template=[convert(value) for value in basis.temperature]
        residuals=[[value-mode*amplitude for value,mode in zip(column,template)]
                   for column,amplitude in zip(coefficients,eta)]
        outputs={key:[] for key in ['potential','distortion','temperature','coefficient_residual','template_from_coefficients','template_allowance']}
        for sampled in frequency:
            point=convert(sampled)
            compact=(point-pivot)/(point+pivot)
            values=[Decimal(1)/norms[0],(point-mean)/norms[1]]
            for degree in range(2,basis.count):
                value=compact*values[-1]
                for repeat in range(2):
                    value-=sum((values[index]*convert(basis.projections[degree,repeat,index]) for index in range(degree)),Decimal(0))
                values.append(value/norms[degree])
            template_value=sum((value*mode for value,mode in zip(values,template)),Decimal(0))
            allowance=Decimal(256)*convert(np.finfo(float).eps)*sum((abs(value*mode) for value,mode in zip(values,template)),Decimal(0))
            totals=[sum((value*coefficient for value,coefficient in zip(values,column)),Decimal(0)) for column in coefficients]
            independent=[sum((value*coefficient for value,coefficient in zip(values,column)),Decimal(0)) for column in residuals]
            temperatures=[point*amplitude for amplitude in eta]
            outputs['potential'].append([float(value) for value in totals])
            outputs['temperature'].append([float(value) for value in temperatures])
            outputs['distortion'].append([float(total-temp) for total,temp in zip(totals,temperatures)])
            outputs['coefficient_residual'].append([float(value) for value in independent])
            outputs['template_from_coefficients'].append(float(template_value))
            outputs['template_allowance'].append(float(allowance))
    return {key:np.asarray(value) for key,value in outputs.items()}


def main():
    modest()
    folder=ROOT/'results/stable-readout'
    folder.mkdir(parents=True,exist_ok=False)
    raw_path=ROOT/'results/projection/status.json'
    report=json.loads(raw_path.read_text())
    for path,expected in report['input_hashes'].items():
        assert digest(path)==expected,path
    failures=[row for row in report['checks'] if not row['passed']]
    assert len(failures)==3
    assert {row['name'] for row in failures}=={
        'Temperature basis is x at independent sample frequencies',
        'Pointwise occupation reconstructs on represented band:heavy',
        'Pointwise occupation reconstructs on represented band:cold'}
    basis=infrared_ladder.ConsistentBasis(**report['basis_specification'])
    frequency=np.geomspace(basis.minimum,basis.maximum,241)
    occupation=1/np.expm1(frequency)
    weight=occupation*(1+occupation)
    checks,inputs,models=[],[raw_path,ROOT/'STABLE-READOUT.md'],{}
    def test(name,value,limit=1e-11):
        checks.append(dict(name=name,value=float(value),limit=limit,passed=bool(np.isfinite(value) and value<limit)))
    for model in ['heavy','cold']:
        state,path=read_final(model,'main-1024')
        inputs.append(path)
        coarse=exact_readout(basis,frequency,state['photon'],state['energy'],40)
        fine=exact_readout(basis,frequency,state['photon'],state['energy'],65)
        metadata=report['models'][model]['metadata']
        heat=metadata['heat']
        scale=np.maximum(np.max(abs(weight[:,None]*fine['potential']),axis=0),1e-300)
        for key in ['potential','distortion','temperature','coefficient_residual']:
            test('40 to65 decimal digit readout agreement:'+model+':'+key,
                np.max(abs(weight[:,None]*(fine[key]-coarse[key]))/scale))
        test('Rounded coefficient temperature tangent within explicit256eps allowance:'+model,
            np.max(abs(fine['template_from_coefficients']-frequency)/fine['template_allowance']),1.)
        test('Analytic temperature plus high precision distortion reconstructs:'+model,
            np.max(abs(weight[:,None]*(fine['potential']-fine['temperature']-fine['distortion']))/scale))
        test('Independent unrounded coefficient residual agrees with physical tangent split:'+model,
            np.max(abs(weight[:,None]*(fine['coefficient_residual']-fine['distortion']))/scale))
        delta_full=heat*weight[:,None]*fine['potential']
        delta_dist=heat*weight[:,None]*fine['distortion']
        delta_temp=heat*weight[:,None]*fine['temperature']
        frequency_hz=frequency*metadata['k_B']*metadata['reference_temperature_K']/metadata['h_P']
        factor=2*metadata['h_P']*frequency_hz**3/metadata['c']**2
        intensity_full=factor[:,None]*delta_full
        intensity_dist=factor[:,None]*delta_dist
        intensity_temp=factor[:,None]*delta_temp
        delta_scale=np.maximum(np.max(abs(delta_full),axis=0),1e-300)
        intensity_scale=np.maximum(np.max(abs(intensity_full),axis=0),1e-300)
        test('Physical occupation reconstruction same1e-11 gate:'+model,
            np.max(abs(delta_full-delta_temp-delta_dist)/delta_scale))
        test('Physical specific intensity reconstruction same1e-11 gate:'+model,
            np.max(abs(intensity_full-intensity_temp-intensity_dist)/intensity_scale))
        test('Physical fractional radiance equals fractional occupation:'+model,
            np.max(abs(intensity_dist/(factor*occupation)[:,None]-delta_dist/occupation[:,None]))/
            max(float(np.max(abs(delta_dist/occupation[:,None]))),1e-300))
        raw_spectrum_path=ROOT/'results/projection'/f'{model}-band-spectrum.npz'
        inputs.append(raw_spectrum_path)
        with np.load(raw_spectrum_path) as raw:
            change=np.max(abs(raw['delta_occupation_distortion']-delta_dist)/delta_scale,axis=0)
        np.savez(folder/f'{model}-physical-band-spectrum.npz',x=frequency,frequency_Hz=frequency_hz,
            delta_occupation=delta_full,delta_occupation_temperature=delta_temp,
            delta_occupation_distortion=delta_dist,delta_intensity_SI=intensity_full,
            delta_intensity_temperature_SI=intensity_temp,delta_intensity_distortion_SI=intensity_dist,
            distortion_fractional_intensity=delta_dist/occupation[:,None],
            potential=fine['potential'],distortion_potential=fine['distortion'],
            temperature_potential=fine['temperature'],reference_temperature_K=metadata['reference_temperature_K'])
        models[model]=dict(raw_to_stable_band_distortion_relative_to_full_peak=change.tolist(),
            central_band_fractional_distortion_max=np.max(abs(delta_dist[:,:2]/occupation[:,None]),axis=0).tolist(),
            template_floating_coefficient_defect_relative=float(np.max(abs(fine['template_from_coefficients']/frequency-1))),
            high_precision_digits=65)
    finish(folder,dict(checks=checks,models=models,retained_raw_failures=failures,
        coefficient_projection_recomputed=False,source_evaluations=0,
        thresholds_relaxed=False,stable_pointwise_readout_authoritative=True,
        old_float64_pointwise_readout_retained=True,exact_temperature_tangent_used=True,
        basis_parameters_unchanged=True,independent_energy_unchanged=True,
        no_new_continuum_or_infrared_error_bound=True),__file__,inputs)
    print(json.dumps(dict(count=len(checks),failures=[row for row in checks if not row['passed']],models=models)),flush=True)
    if not all(row['passed'] for row in checks):
        raise SystemExit(1)


if __name__=='__main__':
    main()


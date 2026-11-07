from common225 import *

def probe(name,coordinate,first,last):
    fraction=(coordinate-first)/(last-first)
    if name=='constant':
        return 1.,0.
    if name=='ramp':
        return fraction,1/(last-first)
    return 4*fraction*(1-fraction),(4-8*fraction)/(last-first)

def forward(background,name,first,last):
    def rhs(coordinate,values):
        parts=model_parts(background,coordinate)
        supplied=probe(name,coordinate,first,last)[0]
        return parts['operator']@values+parts['forcing']*supplied
    solved=integrate.solve_ivp(rhs,(first,last),np.zeros(4),method='DOP853',rtol=3e-11,atol=1e-40,
        max_step=.005,dense_output=True)
    assert solved.success
    return solved,rhs

def nonlinear(background,name,first,last,amplitude):
    initial=model_parts(background,first)['state']
    mass2=background.parent.masses**2
    def rate(coordinate,values):
        scale=background.start_scale*math.exp(coordinate)
        external=amplitude*background.parent.photons/scale**4*probe(name,coordinate,first,last)[0]
        density=background.parent.radiation/scale**4+(background.parent.baryons+background.parent.cold)/scale**3
        density+=np.sum(values[2:]**2/scale**2+mass2*values[:2]**2)/2+external
        assert density>0
        return scale*math.sqrt(density/3)
    def rhs(coordinate,values):
        scale=background.start_scale*math.exp(coordinate)
        hubble=rate(coordinate,values)
        return np.r_[values[2:]/hubble,-2*values[2:]-scale**2*mass2*values[:2]/hubble]
    solved=integrate.solve_ivp(rhs,(first,last),np.r_[initial['fields'],initial['prime']],method='DOP853',
        rtol=3e-12,atol=1e-28,max_step=.005,dense_output=True)
    assert solved.success
    return solved,rate

def run():
    config=protocol()
    inputs=read(ROOT/'inputs.json');rows=[];records=[]
    for model in config['models']:
        background=gravity.ThermalBackground(model)
        register(inputs,background.parent.source)
        register(inputs,background.native_constants)
        for span,limits in config['spans'].items():
            first,last=np.array(limits)*math.log(10)
            bound=analytic_bound(background,first,last)
            samples=np.linspace(first,last,65)
            for coordinate in samples:
                parts=model_parts(background,coordinate)
                field_energy=(parts['field'][:2]**2+parts['field'][2:]**2)/2
                check(rows,f'{model}:{span}:{coordinate}:field-energy majorant',np.max(field_energy/np.maximum(bound['field_energy_initial'],1e-300)),1+1e-10,'bound')
                check(rows,f'{model}:{span}:{coordinate}:density lower bound',bound['density_min']/parts['energy'],1+1e-10,'bound')
                check(rows,f'{model}:{span}:{coordinate}:scalar drive majorant',np.linalg.norm(parts['drive'])/max(bound['Bstar'],1e-300),1+1e-10,'bound')
                check(rows,f'{model}:{span}:{coordinate}:density row majorant',np.linalg.norm(parts['row'])/max(bound['Cstar'],1e-300),1+1e-10,'bound')
                check(rows,f'{model}:{span}:{coordinate}:photon fraction majorant',parts['direct']/bound['Dstar'],1+1e-10,'bound')
            endpoint=model_parts(background,last)
            adjoint=integrate.solve_ivp(lambda coordinate,values:-model_parts(background,coordinate)['operator'].T@values,
                (last,first),endpoint['row'],method='DOP853',rtol=3e-11,atol=1e-45,max_step=.005,dense_output=True)
            assert adjoint.success
            quadratures={}
            for order in config['quadrature_orders']:
                nodes,weights=np.polynomial.legendre.leggauss(order)
                coordinates=(first+last)/2+(last-first)*nodes/2
                weighted=(last-first)*weights/2
                kernel=np.array([adjoint.sol(coordinate)@model_parts(background,coordinate)['forcing'] for coordinate in coordinates])
                quadratures[order]=(coordinates,weighted,kernel)
            low=quadratures[config['quadrature_orders'][0]]
            high=quadratures[config['quadrature_orders'][1]]
            lower_gain=endpoint['direct']+low[1]@abs(low[2])
            numeric_gain=endpoint['direct']+high[1]@abs(high[2])
            check(rows,f'{model}:{span}:kernel absolute-integral refinement',abs(lower_gain-numeric_gain)/max(abs(numeric_gain),1e-300),1e-6,'quadrature')
            check(rows,f'{model}:{span}:adjoint gain below analytic majorant',numeric_gain/bound['source_gain'],1+1e-10,'bound')
            incoming=adjoint.sol(first)
            check(rows,f'{model}:{span}:incoming row below analytic majorant',np.linalg.norm(incoming)/bound['incoming_gain'],1+1e-10,'bound')
            tests=[]
            for name in config['probes']:
                solved,rhs=forward(background,name,first,last)
                values=solved.sol(samples).T
                predictions=[]
                for coordinate,state in zip(samples,values):
                    parts=model_parts(background,coordinate)
                    source,source_prime=probe(name,coordinate,first,last)
                    prediction=parts['row']@state+parts['direct']*source
                    predictions.append(prediction)
                    field_pressure=parts['field'][2:]@state[2:]-parts['field'][:2]@state[:2]
                    pressure=parts['state']['photon']*(source-source_prime)/3+field_pressure
                    density=2*parts['energy']*prediction
                    baseline_pressure=(parts['state']['photon']+parts['state']['neutrino'])/3
                    baseline_pressure+=(np.sum(parts['field'][2:]**2)-np.sum(parts['field'][:2]**2))/2
                    equation_of_state=baseline_pressure/parts['energy']
                    row_prime=parts['free']@parts['field']/(2*parts['energy'])+3*(1+equation_of_state)*parts['row']
                    direct_prime=(-1+3*equation_of_state)*parts['direct']
                    tangent_prime=row_prime@state+parts['row']@rhs(coordinate,state)+direct_prime*source+parts['direct']*source_prime
                    raychaudhuri=-1.5*(pressure-equation_of_state*density)/parts['energy']
                    check(rows,f'{model}:{span}:{name}:{coordinate}:Raychaudhuri',abs(tangent_prime-raychaudhuri)/max(abs(tangent_prime)+abs(raychaudhuri),1e-300),1e-8,'identity')
                predictions=np.array(predictions)
                estimates=[]
                for order in config['quadrature_orders']:
                    coordinates,weights,kernel=quadratures[order]
                    drive=np.array([probe(name,coordinate,first,last)[0] for coordinate in coordinates])
                    estimates.append(float(endpoint['direct']*probe(name,last,first,last)[0]+weights@(kernel*drive)))
                check(rows,f'{model}:{span}:{name}:forward adjoint',abs(estimates[-1]-predictions[-1])/max(abs(predictions[-1]),1e-300),1e-6,'independent_evolution')
                check(rows,f'{model}:{span}:{name}:quadrature refinement',abs(estimates[-1]-estimates[0])/max(abs(estimates[-1]),1e-300),1e-6,'quadrature')
                check(rows,f'{model}:{span}:{name}:whole probe below analytic bound',np.max(abs(predictions))/bound['source_gain'],1+1e-10,'bound')
                variations=[]
                for amplitude in config['probe_amplitudes']:
                    positive,positive_rate=nonlinear(background,name,first,last,amplitude)
                    negative,negative_rate=nonlinear(background,name,first,last,-amplitude)
                    rates=np.array([(positive_rate(coordinate,positive.sol(coordinate))-negative_rate(coordinate,negative.sol(coordinate)))
                        /(2*amplitude*model_parts(background,coordinate)['state']['hubble']) for coordinate in samples])
                    error=float(np.max(abs(rates-predictions))/max(float(np.max(abs(predictions))),1e-300))
                    check(rows,f'{model}:{span}:{name}:{amplitude}:nonlinear Friedmann variation',error,5e-5,'independent_evolution')
                    field_error=None
                    if model=='heavy':
                        displacement=(positive.sol(samples)-negative.sol(samples)).T/(2*amplitude)
                        transformed=np.column_stack([displacement[:,:2]*background.parent.masses,
                            displacement[:,2:]/(background.start_scale*np.exp(samples))[:,None]])
                        field_error=float(np.max(abs(transformed[:,[1,3]]-values[:,[1,3]]))/max(float(np.max(abs(values[:,[1,3]]))),1e-300))
                        check(rows,f'{model}:{span}:{name}:{amplitude}:nonlinear heavy-field variation',field_error,5e-5,'independent_evolution')
                    variations.append(dict(amplitude=amplitude,H_envelope_relative_error=error,heavy_field_relative_error=field_error))
                tests.append(dict(probe=name,endpoint_response=float(predictions[-1]),adjoint_endpoint=estimates[-1],
                    maximum_response=float(np.max(abs(predictions))),nonlinear_variations=variations))
                save(ROOT/f'gravity/{model}-{span}-{name}.npz',log_expansion=samples,field_energy_frame=values,H_fraction=predictions)
            save(ROOT/f'gravity/{model}-{span}-kernel.npz',coordinate=high[0],weights=high[1],kernel=high[2],
                incoming_row=incoming,direct_endpoint=endpoint['direct'])
            records.append(dict(model=model,span=span,first_fraction=limits[0],last_fraction=limits[1],
                analytic=bound,numerical_adjoint_gain=float(numeric_gain),incoming_row=incoming.tolist(),
                probe_results=tests,zero_incoming_only_for_probes=True))
            print(json.dumps(dict(model=model,span=span,analytic_gain=bound['source_gain'],adjoint_gain=numeric_gain,
                failed=sum(not row['passed'] for row in rows))),flush=True)
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'inputs-gravity.json',inputs)
    write(ROOT/'results/gravity.json',dict(checks=rows,failed_checks=failed,qualified=not failed,records=records,finished_at=now(),
        calibrated_G_unchanged=True,field_feedback_included=True,actual_full_source_history_not_assumed=True,
        analytical_bound_scope='conditional on retained positive canonical parent and source sup bound; no numerical calibration interval certification'))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),failures=failed[:12])),flush=True)

if __name__=='__main__':
    parent.old.source.modest()
    run()

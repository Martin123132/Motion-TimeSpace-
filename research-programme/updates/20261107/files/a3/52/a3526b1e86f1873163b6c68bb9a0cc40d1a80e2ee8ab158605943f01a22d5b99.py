from common225 import *

def run():
    config=protocol()
    inputs=read(ROOT/'inputs.json');rows=[];records=[];bounds=[];matrix_diagnostics=[]
    with mp.workdps(80):
        for model in config['models']:
            for count in config['counts']:
                system=parent.old.matched.System(model,count,inputs)
                basis=system.basis
                heat=mp.mpf(float(system.background.chi))
                mass=parent.matrix(basis.mass)
                mass=(mass+mass.T)/2
                energy_row=parent.matrix(basis.energy[None,:])
                dual=mp.lu_solve(mass,energy_row.T)
                density_dual=heat*mp.sqrt((energy_row*dual)[0]+heat)
                tail_bound=analytic_bound(system.background,parent.TARGET_FRACTION*math.log(10),math.log(10))
                reference_norm=None
                folders=[('window',path) for path in sorted((KINETIC/f'window/{model}-{count}').glob('step-*.npz'))]
                folders += [('tail',path) for path in sorted((KINETIC/f'tail/{model}-{count}').glob('step-*.npz'))]
                for scope,path in folders:
                    stored=load(inputs,path)
                    index=int(stored['index'])
                    values=parent.matrix(stored['high'])+parent.matrix(stored['low'])
                    if scope=='window':
                        values=values[:,2*parent.WIDTH:]
                    coordinate=(.75+.25*index/count)*math.log(10)
                    first,last,target=parent.indices(count)
                    solver=parent.Physical(system,system.make_step(index),mp.mpf('1.5')/mp.mpf(float(system.step)))
                    supplied=parent.source_at(model,count,index,system,rows) if first<=index<=last else parent.zero_source(parent.WIDTH)
                    derivative=solver.derivative(values)+previous.source_vector(solver,supplied)
                    photon=solver.transform*values[:96,:]
                    energy_norm=[];normalized_density=[];normalized_pressure=[]
                    physical_scale=mp.mpf(float(system.background.photon_energy0))/mp.mpf(float(system.background.start_scale*math.exp(coordinate)))**4
                    for column,label in enumerate(parent.LABELS):
                        energy,gas=values[0,column],values[96,column]
                        density=heat*(energy+heat*gas)
                        pressure=heat*(energy+2*heat*gas)/3
                        density_derivative=heat*(derivative[0,column]+heat*derivative[96,column])-4*density
                        injected=heat*supplied['pair'][column]
                        continuity=density_derivative+3*(density+pressure)-injected
                        denominator=max(abs(density_derivative)+3*abs(density+pressure)+abs(injected),mp.mpf('1e-300'))
                        check(rows,f'{model}:{count}:{scope}:{index}:{column}:calibrated continuity',abs(continuity)/denominator,1e-8,'identity')
                        omitted=density_derivative+3*(density+heat*energy/3)-injected
                        expected=-2*heat**2*gas
                        check(rows,f'{model}:{count}:{scope}:{index}:{column}:omitted-pressure residual',abs(omitted-expected)/max(abs(expected),mp.mpf('1e-300')),1e-10,'negative_control_identity')
                        spectral_energy=(energy_row*photon[:,column])[0]
                        kinetic_squared=(photon[:,column].T*mass*photon[:,column])[0]+heat*gas**2
                        assert kinetic_squared>=0
                        kinetic=mp.sqrt(kinetic_squared)
                        cauchy=density_dual*kinetic
                        physical_density=heat*(spectral_energy+heat*gas)
                        check(rows,f'{model}:{count}:{scope}:{index}:{column}:energy-moment representation',abs(density-physical_density)/max(cauchy,mp.mpf('1e-300')),1e-10,'representation')
                        check(rows,f'{model}:{count}:{scope}:{index}:{column}:physical density dual bound',abs(physical_density)/max(cauchy,mp.mpf('1e-300')),1+1e-10,'bound')
                        energy_norm.append(float(kinetic));normalized_density.append(float(density));normalized_pressure.append(float(pressure))
                        if label['component']!='zero':
                            records.append(dict(model=model,count=count,scope=scope,index=index,fraction=.75+.25*index/count,**label,
                                q_density=float(density),q_pressure=float(pressure),q_injection=float(injected),
                                density_J_m3=float(physical_scale*density),pressure_Pa=float(physical_scale*pressure),
                                density_moment_representation_difference=float(density-physical_density),
                                omitted_pressure_whole_balance_ratio=float(abs(omitted)/denominator),
                                energy_norm=float(kinetic),pointwise_density_bound=float(cauchy)))
                    if scope=='window' and index==target:
                        reference_norm=np.array(energy_norm)
                        for column,label in enumerate(parent.LABELS):
                            if label['component']=='zero':
                                continue
                            maximum_density=float(density_dual)*energy_norm[column]
                            bounds.append(dict(model=model,count=count,**label,physical_tail_start=parent.TARGET_FRACTION,
                                Q_tail=maximum_density,H_tail_zero_incoming_bound=tail_bound['source_gain']*maximum_density,
                                incoming_field_coefficient=tail_bound['incoming_gain'],
                                incoming_field_norm_units='sqrt(parent scalar energy density); explicit not zeroed',
                                scope='post-restart attributed source-free physical tail, not full earlier response'))
                    if scope=='tail':
                        assert reference_norm is not None
                        for column,value in enumerate(energy_norm):
                            check(rows,f'{model}:{count}:{index}:{column}:saved tail norm not increased',value/max(reference_norm[column],1e-300),1+1e-10,'comparison')
                    save(ROOT/f'stress/{model}-{count}-{scope}-{index}.npz',q_density=np.array(normalized_density),q_pressure=np.array(normalized_pressure),
                        energy_norm=np.array(energy_norm),fraction=.75+.25*index/count,chi=float(heat),rho_star_J_m3=float(physical_scale))
                if count==4096:
                    for temperature in system.ladder.temperatures:
                        stiffness=system.ladder.at(float(temperature),0)[:96,:96]-system.emission.at(float(temperature),'dcbr')
                        symmetric=(stiffness+stiffness.T)/2
                        eigenvalues=linalg.eigvalsh(symmetric,basis.mass)
                        radius=max(float(np.max(abs(eigenvalues))),1e-300)
                        maximum=float(max(eigenvalues[-1],0.))/radius
                        asymmetry=float(np.linalg.norm(stiffness-stiffness.T)/max(np.linalg.norm(stiffness),1e-300))
                        check(rows,f'{model}:{temperature}:stored dissipation diagnostic',maximum,1e-10,'representation')
                        check(rows,f'{model}:{temperature}:stored symmetry diagnostic',asymmetry,1e-10,'representation')
                        matrix_diagnostics.append(dict(model=model,temperature=float(temperature),largest_generalized_eigenvalue=float(eigenvalues[-1]),
                            normalized_positive_part=maximum,scope='floating diagnostic; analytic sign comes from positive physical Gram construction'))
                print(json.dumps(dict(model=model,count=count,stress_packets=len(folders),failed=sum(not row['passed'] for row in rows))),flush=True)
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'inputs-stress.json',inputs)
    write(ROOT/'results/stress.json',dict(checks=rows,failed_checks=failed,qualified=not failed,records=records,tail_bounds=bounds,
        stored_matrix_diagnostics=matrix_diagnostics,finished_at=now(),source_free_model_scope=config['kinetic_tail_scope']))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),failures=failed[:10])),flush=True)

if __name__=='__main__':
    parent.old.source.modest()
    run()

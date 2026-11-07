from common226 import *
import time

def solve_factor(factor,permutation,values):
    return mp.mp.U_solve(factor,mp.mp.L_solve(factor,values,permutation))

def run(model):
    config=protocol()
    inputs=read(ROOT/'inputs.json');rows=[];records=[]
    began=time.monotonic()
    with mp.workdps(80):
        system=parent.old.matched.System(model,4096,inputs)
        heat=mp.mpf(float(system.background.chi))
        mass=parent.matrix(system.basis.mass)
        mass=(mass+mass.T)/2
        factor,permutation=mp.mp.LU_decomp(mass)
        temperature=parent.matrix(system.basis.temperature[:,None])
        energy=parent.matrix(system.basis.energy[None,:])
        defect_row=energy-temperature.T*mass
        defect=mp.sqrt((defect_row*solve_factor(factor,permutation,defect_row.T))[0])
        energy_dual=mp.sqrt((energy*solve_factor(factor,permutation,energy.T))[0]+heat)
        first,last,target=parent.indices(4096)
        coordinates=[]
        forces=[];injections=[];recorded_injections=[];sample_norms=[]
        for index in range(first,last+1):
            source=parent.source_at(model,4096,index,system,rows)
            raw=source['raw']
            coordinates.append(mp.mpf(float((.75+.25*index/4096)*math.log(10))))
            norms=[];pair=[];old_pair=[]
            for column,label in enumerate(LABELS):
                photon_force=raw[1:97,column]
                gas_force=raw[97,column]
                solved=solve_factor(factor,permutation,photon_force)
                squared=(photon_force.T*solved)[0]+gas_force**2/heat
                assert squared>=0
                norms.append(mp.sqrt(squared))
                physical_pair=(temperature.T*photon_force)[0]+gas_force
                pair.append(physical_pair)
                old_pair.append(source['pair'][column])
                exchange_scale=max(abs((temperature.T*photon_force)[0])+abs(gas_force),mp.mpf('1e-300'))
                check(rows,f'{index}:{column}:physical/recorded pair representation',
                    abs(physical_pair-source['pair'][column])/exchange_scale,1e-10,'representation')
                if label['component']=='zero':
                    check(rows,f'{index}:zero forcing',norms[-1]+abs(physical_pair),0,'identity')
            forces.append(norms);injections.append(pair);recorded_injections.append(old_pair)
            if (index-first)%8==0:
                print(json.dumps(dict(model=model,source=index-first+1,total=last-first+1,seconds=time.monotonic()-began)),flush=True)
        global_end=mp.mpf(float(math.log(10)))
        short_end=mp.mpf(float(parent.TARGET_FRACTION*math.log(10)))
        global_metric=inherited.analytic_bound(system.background,float(coordinates[0]),float(global_end))
        short_metric=inherited.analytic_bound(system.background,float(coordinates[0]),float(short_end))
        tail_metric=inherited.analytic_bound(system.background,float(short_end),float(global_end))
        metrics=dict(global_interval=global_metric,forced_to_restart=short_metric,restart_tail=tail_metric)
        for count in parent.COUNTS:
            stride=4096//count
            used_coordinates=coordinates[::stride]
            start_index,stop_index,target_index=parent.indices(count)
            spacing=mp.mpf(float(.25*math.log(10)/count))
            window_bounds=[]
            for column,label in enumerate(LABELS):
                norms=[values[column] for values in forces[::stride]]
                pair=[values[column] for values in injections[::stride]]
                original_pair=[values[column] for values in recorded_injections[::stride]]
                area,moment,energy_area=integrals(used_coordinates,norms,pair,global_end)
                global_q=forced_q(heat,defect,used_coordinates,norms,pair,global_end)
                short_q=forced_q(heat,defect,used_coordinates,norms,pair,short_end)
                discarded_pair_q=forced_q(heat,defect,used_coordinates,norms,original_pair,global_end)
                bounds,densities=discrete_bounds(heat,spacing,norms,pair,defect)
                window_bounds.append((bounds,densities))
                duration=short_end-used_coordinates[0]
                beta=mp.mpf(float(short_metric['beta']))
                growth=mp.expm1(beta*duration)/beta if beta else duration
                field_bound=mp.mpf(float(short_metric['Bstar']*short_metric['Dstar']))*short_q*growth
                split_bound=mp.mpf(float(tail_metric['source_gain']))*global_q+mp.mpf(float(tail_metric['incoming_gain']))*field_bound
                whole_bound=mp.mpf(float(global_metric['source_gain']))*global_q
                if label['component']=='zero':
                    check(rows,f'{count}:zero bounds',whole_bound+field_bound,0,'identity')
                    continue
                records.append(dict(model=model,count=count,**label,force_integral=float(area),force_first_moment=float(moment),
                    absolute_pair_integral=float(energy_area),moment_representation_dual=float(defect),
                    Q_global=float(global_q),Q_at_restart=float(short_q),field_norm_at_restart_bound=float(field_bound),
                    H_whole_attributed_bound=float(whole_bound),H_split_attributed_bound=float(split_bound),
                    H_incoming_piece_bound=float(mp.mpf(float(tail_metric['incoming_gain']))*field_bound),
                    source_pair_representation_change=float(global_q-discarded_pair_q),
                    physical_window_complete=True,whole_cosmic_history_claimed=False))
            for path in sorted((KINETIC/f'window/{model}-{count}').glob('step-*.npz')):
                stored=load(inputs,path)
                index=int(stored['index'])
                if index>stop_index:
                    continue
                values=(parent.matrix(stored['high'])+parent.matrix(stored['low']))[:,2*parent.WIDTH:]
                previous=(parent.matrix(stored['previous_high'])+parent.matrix(stored['previous_low']))[:,2*parent.WIDTH:]
                transform=parent.matrix(system.coordinates.transform)
                state=transform*values[:96,:];older=transform*previous[:96,:]
                for column,label in enumerate(LABELS):
                    kinetic=(state[:,column].T*mass*state[:,column])[0]+heat*values[96,column]**2
                    previous_combination=2*state[:,column]-older[:,column]
                    two_state=mp.sqrt(kinetic+(previous_combination.T*mass*previous_combination)[0]+heat*(2*values[96,column]-previous[96,column])**2)
                    physical_density=heat*((energy*state[:,column])[0]+heat*values[96,column])
                    upper,density=window_bounds[column]
                    ordinal=index-start_index
                    check(rows,f'{count}:{index}:{column}:saved two-state norm below G-bound',
                        two_state/max(upper[ordinal],mp.mpf('1e-300')),1+1e-10,'discrete_bound')
                    check(rows,f'{count}:{index}:{column}:saved density below discrete work-bound',
                        abs(physical_density)/max(density[ordinal],mp.mpf('1e-300')),1+1e-10,'discrete_bound')
        for label in LABELS[:-1]:
            paired=[next(record for record in records if record['count']==count and all(record[key]==value for key,value in label.items())) for count in parent.COUNTS]
            for key in ('force_integral','Q_global','H_whole_attributed_bound','field_norm_at_restart_bound'):
                error=abs(paired[0][key]-paired[1][key])/max(abs(paired[1][key]),1e-300)
                check(rows,f'{label}:{key}:32/64-cell refinement',error,.01,'refinement')
        high,low=parent.split(mp.matrix(forces))
        injection_high,injection_low=parent.split(mp.matrix(injections))
        save(ROOT/f'sources/{model}.npz',coordinates=np.array([float(value) for value in coordinates]),
            force_norm_high=high,force_norm_low=low,injection_high=injection_high,injection_low=injection_low,
            heat=float(heat),energy_moment_defect=float(defect))
    failed=[row for row in rows if not row['passed']]
    write(ROOT/f'inputs-{model}.json',inputs)
    write(ROOT/f'results/{model}.json',dict(checks=rows,failed_checks=failed,qualified=not failed,
        records=records,metric_bounds=metrics,seconds=time.monotonic()-began,finished_at=now(),
        exact_continuum_source_curve_claimed=False,feedback_included=False,
        scope='Retained dissipative weak law with named linear numerical forcing reconstruction; separate discrete source-window energy bounds'))
    print(json.dumps(dict(model=model,checks=len(rows),failed=len(failed),failures=failed[:10],seconds=time.monotonic()-began)),flush=True)

if __name__=='__main__':
    parent.old.source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--model',choices=parent.MODELS,required=True)
    run(parser.parse_args().model)


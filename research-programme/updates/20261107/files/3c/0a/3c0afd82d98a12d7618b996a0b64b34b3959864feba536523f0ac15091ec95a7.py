from common225 import *

def prepare():
    protocol()
    assert not (ROOT/'sharp-configuration.json').exists()
    write(ROOT/'sharp-configuration.json',dict(frozen_at=now(),
        hashes={name:digest(ROOT/name) for name in ('sharpen225.py','completion225.py','ENERGY-WORK-BOUND.md',
            'results/stress.json','results/gravity.json','coordinate-repair.json')},
        identity_tolerance=1e-10,scope='Source-free restart tail; initial field response remains explicit'))

def sharp_protocol():
    protocol()
    config=read(ROOT/'sharp-configuration.json')
    for name,value in config['hashes'].items():
        assert digest(ROOT/name)==value,name
    return config

def run():
    sharp_protocol()
    stress=read(ROOT/'results/stress.json')
    gravity_report=read(ROOT/'results/gravity.json')
    assert stress['qualified'] and gravity_report['qualified']
    rows=[];records=[];inputs=read(ROOT/'inputs-stress.json')
    with mp.workdps(80):
        duration=mp.mpf(float((1-parent.TARGET_FRACTION)*math.log(10)))
        work_factor=min(duration,mp.sqrt(duration/2))
        for model in parent.MODELS:
            metric=next(record for record in gravity_report['records'] if record['model']==model and record['span']=='source_free_tail')
            for count in parent.COUNTS:
                system=parent.old.matched.System(model,count,inputs)
                heat=mp.mpf(float(system.background.chi))
                target=parent.indices(count)[2]
                mass=parent.matrix(system.basis.mass)
                mass=(mass+mass.T)/2
                transform=parent.matrix(system.coordinates.transform)
                energy_row=parent.matrix(system.basis.energy[None,:])
                dual_norm=heat*mp.sqrt((energy_row*mp.lu_solve(mass,energy_row.T))[0]+heat)
                saved=load(inputs,KINETIC/f'window/{model}-{count}/step-{target}.npz')
                values=(parent.matrix(saved['high'])+parent.matrix(saved['low']))[:,2*parent.WIDTH:]
                bounds=[]
                for column,label in enumerate(parent.LABELS):
                    photon=transform*values[:96,column]
                    gas=values[96,column]
                    kinetic=mp.sqrt((photon.T*mass*photon)[0]+heat*gas**2)
                    initial_density=heat*((energy_row*photon)[0]+heat*gas)
                    dual=dual_norm*kinetic
                    work=abs(initial_density)+heat**mp.mpf('1.5')*kinetic*work_factor
                    sharp=min(dual,work)
                    bounds.append(sharp)
                    check(rows,f'{model}:{count}:{column}:sharp no worse than dual',sharp/max(dual,mp.mpf('1e-300')),1+1e-10,'bound')
                    if label['component']=='zero':
                        check(rows,f'{model}:{count}:zero bound',sharp,0,'identity')
                        continue
                    inherited=next(record for record in stress['tail_bounds'] if record['model']==model and record['count']==count
                        and all(record[key]==value for key,value in label.items()))
                    check(rows,f'{model}:{count}:{column}:dual replay',abs(dual-mp.mpf(inherited['Q_tail']))/max(dual,mp.mpf('1e-300')),1e-10,'identity')
                    records.append(dict(model=model,count=count,**label,q_initial_physical=float(initial_density),V_initial=float(kinetic),
                        Q_dual=float(dual),Q_work=float(work),Q_sharp=float(sharp),
                        H_tail_zero_incoming_bound=metric['analytic']['source_gain']*float(sharp),
                        incoming_field_coefficient=metric['analytic']['incoming_gain'],
                        improvement_over_dual=float(dual/max(sharp,mp.mpf('1e-300')))))
                for path in sorted((KINETIC/f'tail/{model}-{count}').glob('step-*.npz')):
                    later=load(inputs,path)
                    state=parent.matrix(later['high'])+parent.matrix(later['low'])
                    for column in range(parent.WIDTH):
                        density=heat*((energy_row*transform*state[:96,column])[0]+heat*state[96,column])
                        check(rows,f'{model}:{count}:{path.stem}:{column}:saved density within analytic tail bound',abs(density)/max(bounds[column],mp.mpf('1e-300')),1+1e-10,'comparison')
    failed=[row for row in rows if not row['passed']]
    for path in (ROOT/'sharp-configuration.json',ROOT/'sharpen225.py',ROOT/'ENERGY-WORK-BOUND.md'):
        register(inputs,path)
    write(ROOT/'inputs-sharp.json',inputs)
    write(ROOT/'results/sharp-bound.json',dict(checks=rows,failed_checks=failed,qualified=not failed,records=records,
        finished_at=now(),duration=float(duration),work_factor=float(work_factor),
        unknown_incoming_state_kept=True,global_source_history_bound_claimed=False,
        scope='Analytic energy/work and coupled-field majorants for the retained source-free physical restart model'))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),failures=failed[:10])),flush=True)

if __name__=='__main__':
    parent.old.source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','run'])
    globals()[parser.parse_args().phase]()

from common223 import *

def columns_for(profile,grid,component):
    return [index for index,label in enumerate(LABELS) if label['profile']==profile and label['grid']==grid and label['component']==component]

def compare_readouts(rows,records,scope,first,second,columns_first,columns_second,model,component):
    for field in ('residual','gas','energy','work','number'):
        left=first[field][...,columns_first];right=second[field][...,columns_second]
        if field=='residual':
            numerator=old.matched.saved.response.norm(left-right,second['measure'])
            denominator=old.matched.saved.response.norm(right,second['measure'])
        else:
            numerator=abs(left-right);denominator=abs(right)
        ratios=numerator/np.maximum(denominator,1e-300)
        for join,value in enumerate(np.asarray(ratios).reshape(-1)):
            record=dict(scope=scope,model=model,component=component,field=field,join=join,relative=float(value))
            records.append(record)
            check(rows,f'{scope}:{model}:{component}:{field}:{join}',value,.01,'comparison')

def exact_saved(path):
    stored=packet(path)
    return matrix(stored['high'])+matrix(stored['low'])

def physical_state_checks(values,rows,label):
    for profile,grid,join in [(profile,grid,join) for profile in old.PROFILES for grid in ('quarter','eighth') for join in (0,1)]:
        indices={component:next(index for index,item in enumerate(LABELS) if item==dict(profile=profile,grid=grid,component=component,join=join))
                 for component in ('baseline','MTS','total')}
        baseline=values[:,indices['baseline']]
        correction=values[:,indices['MTS']]
        total=values[:,indices['total']]
        check(rows,f'{label}:{profile}:{grid}:{join}:component vector',relative(total,baseline+correction),1e-10,'identity')
        for field,row in (('energy',0),('gas',96),('work',97),('number',98)):
            expected=baseline[row]+correction[row]
            check(rows,f'{label}:{profile}:{grid}:{join}:component {field}',abs(total[row]-expected)/max(abs(expected),mp.mpf('1e-300')),1e-10,'identity')

def assess(phase):
    config=protocol()
    rows=[];records=[]
    if phase=='window':
        rows.extend(read(ROOT/'results/preparation.json')['checks'])
    for model in MODELS:
        for count in COUNTS:
            folder=ROOT/f'{phase}/{model}-{count}'
            report=read(folder/'complete.json')
            for name,value in report['file_hashes'].items():
                assert digest(folder/name)==value,name
            rows.extend(dict(row,name=f'{model}:{count}:'+row['name']) for row in report['checks'])
            system=old.matched.System(model,count,{})
            if phase=='window':
                for path in folder.glob('step-*.npz'):
                    with mp.workdps(80):
                        values=exact_saved(path)
                        expected=values[:,:WIDTH]+values[:,2*WIDTH:]
                        actual=values[:,WIDTH:2*WIDTH]
                        transform=matrix(system.coordinates.transform)
                        for column in range(WIDTH):
                            check(rows,f'{model}:{count}:{path.stem}:photon matching column{column}',
                                  relative(transform*actual[:96,column],transform*expected[:96,column]),1e-10,'identity')
                        physical_state_checks(values[:,2*WIDTH:],rows,f'{model}:{count}:{path.stem}')
                stop=indices(count)[1]
                prior=packet(PARENT/f'responses/{model}-{count}/step-{stop}.npz')
                selected_columns=COLUMNS+[column+old.WIDTH for column in COLUMNS]
                with mp.workdps(80):
                    values=exact_saved(folder/f'step-{stop}.npz')[:,2*WIDTH:]
                    before=exact_pair(prior['current'][:,selected_columns])
                    for field,row in (('energy',0),('gas',96),('work',97),('number',98)):
                        errors=[abs(values[row,column]-before[row,column])/max(abs(before[row,column]),mp.mpf('1e-300')) for column in range(WIDTH)]
                        check(rows,f'{model}:{count}:Stage222 endpoint {field} replay',max(errors),1e-10,'identity')
            else:
                with mp.workdps(80):
                    physical_state_checks(exact_saved(folder/f'step-{count}.npz'),rows,f'{model}:{count}:final')
        coarse=packet(ROOT/f'{phase}/{model}-2048/increment-readout.npz')
        fine=packet(ROOT/f'{phase}/{model}-4096/increment-readout.npz')
        for component in ('baseline','MTS','total'):
            for profile in old.PROFILES:
                eighth=columns_for(profile,'eighth',component)
                quarter=columns_for(profile,'quarter',component)
                compare_readouts(rows,records,'response_step:'+profile,coarse,fine,eighth,eighth,model,component)
                compare_readouts(rows,records,'history_step:'+profile,fine,fine,quarter,eighth,model,component)
            quadratic=columns_for('quadratic','eighth',component)
            secant=columns_for('endpoint_secant','eighth',component)
            compare_readouts(rows,records,'operator_sensitivity',fine,fine,secant,quadratic,model,component)
    failed=[row for row in rows if not row['passed']]
    write(ROOT/f'results/{phase}-assessment.json',dict(phase=phase,checks=rows,failed_checks=failed,records=records,qualified=not failed,
        scope='isolated source-window contribution, not all-frequency or complete cosmological history',
        prediction_is_incoming_plus_interval_plus_other_sources=True))
    print(json.dumps(dict(phase=phase,checks=len(rows),failed=len(failed),
        maxima={scope:max(row['relative'] for row in records if row['scope']==scope) for scope in sorted({row['scope'] for row in records})},
        failures=[dict(name=row['name'],value=row['value'],limit=row['limit']) for row in failed[:24]])),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['window','tail'])
    args=parser.parse_args()
    assess(args.phase)


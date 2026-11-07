from common223 import *
from assess223 import columns_for

def prepare():
    protocol()
    assert not (ROOT/'spectrum-configuration.json').exists()
    write(ROOT/'spectrum-configuration.json',dict(frozen_at=now(),script_sha256=digest(__file__),
        metric_owner=str(Path(old.matched.saved.response.__file__)),
        metric_owner_sha256=digest(old.matched.saved.response.__file__),
        metrics=list(old.matched.saved.response.METRICS),comparison_tolerance=.01,identity_tolerance=1e-10,
        scope='Existing heat-scaled temperature/mu/y/shape readout of this isolated interval contribution',
        new_data_used=False,parameters_fitted=False))

def run():
    protocol()
    config=read(ROOT/'spectrum-configuration.json')
    assert digest(__file__)==config['script_sha256']
    assert digest(config['metric_owner'])==config['metric_owner_sha256']
    rows=[];records=[];comparisons=[]
    for model in MODELS:
        values={}
        for count in COUNTS:
            folder=ROOT/f'tail/{model}-{count}'
            report=read(folder/'complete.json')
            assert digest(folder/'increment-readout.npz')==report['file_hashes']['increment-readout.npz']
            data=packet(folder/'increment-readout.npz')
            metrics=old.matched.saved.response.metrics(data,float(data['heat']),data['measure'])
            assert metrics.shape==(6,WIDTH)
            values[count]=metrics
            for column,label in enumerate(LABELS):
                records.append(dict(model=model,count=count,**label,values={name:float(metrics[index,column]) for index,name in enumerate(config['metrics'])}))
            for profile in old.PROFILES:
                for grid in ('quarter','eighth'):
                    for join in (0,1):
                        selected_columns={component:columns_for(profile,grid,component)[join] for component in ('baseline','MTS','total')}
                        for metric_index,name in enumerate(config['metrics'][:3]):
                            actual=metrics[metric_index,selected_columns['total']]
                            expected=math.fsum((float(metrics[metric_index,selected_columns['baseline']]),float(metrics[metric_index,selected_columns['MTS']])))
                            check(rows,f'{model}:{count}:{profile}:{grid}:{join}:{name}:linear components',
                                abs(actual-expected)/max(abs(expected),1e-300),1e-10,'identity')
        for component in ('baseline','MTS','total'):
            for profile in old.PROFILES:
                eighth=columns_for(profile,'eighth',component)
                quarter=columns_for(profile,'quarter',component)
                for scope,left,right in (
                    ('response_step',values[2048][:,eighth],values[4096][:,eighth]),
                    ('history_step',values[4096][:,quarter],values[4096][:,eighth])):
                    for metric_index,name in enumerate(config['metrics']):
                        for join in (0,1):
                            difference=float(abs(left[metric_index,join]-right[metric_index,join]))
                            relative_value=difference/max(abs(float(right[metric_index,join])),1e-300)
                            comparisons.append(dict(model=model,component=component,profile=profile,scope=scope,metric=name,join=join,
                                absolute_difference=difference,relative=relative_value))
                            check(rows,f'{model}:{component}:{profile}:{scope}:{name}:{join}',relative_value,.01,'comparison')
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'results/final-spectrum-reference.json',dict(configuration=config,records=records,comparisons=comparisons,
        checks=rows,failed_checks=failed,qualified=not failed,full_cosmological_spectrum=False))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),
        maxima={scope:max(row['relative'] for row in comparisons if row['scope']==scope) for scope in ('response_step','history_step')},
        failures=[dict(name=row['name'],value=row['value'],limit=row['limit']) for row in failed[:20]])),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','run'])
    args=parser.parse_args()
    globals()[args.phase]()


from stage163_common import *


def read_exact(path):
    data=json.loads(path.read_text())
    return np.array([Decimal(value) for value in data['values']],dtype=object).reshape(data['shape'])


def main():
    modest()
    folder=ROOT/'results/precision-diagnosis'
    folder.mkdir(parents=True,exist_ok=False)
    source=verify_packet(ROOT/'results/sources')
    records=source['summary']['precision']
    old=verify_packet(PARENT/'results/moment-repair')
    checks=[]
    comparison={}
    inputs=[ROOT/'results/sources/status.json',PARENT/'results/moment-repair/status.json']
    with localcontext() as context:
        context.prec=60
        component_records={}
        for endpoint in ENDPOINTS:
            moments={}
            for order in [4,5,6]:
                path=ROOT/'results/sources'/f'{endpoint}-order{order}-moments.json'
                moments[order]=read_exact(path)
                inputs.append(path)
            for step,high,low in [('54',5,4),('65',6,5),('64',6,4)]:
                delta=moments[high]-moments[low]
                total=delta.sum(axis=(0,1))
                components=delta.sum(axis=0)
                for column in range(4):
                    key=f'{endpoint}:{step}:{column}'
                    prior=old['records'][endpoint+'-'+step+'-'+str(column)]
                    current=records[f'{endpoint}:step{step}:{column}']
                    comparison[key]=dict(old_pair=prior['pair'],new_pair=current['pair'],
                        old_moment=prior['moment'],new_moment=current['moment'],
                        pair_improvement=prior['pair']/max(current['pair'],1e-300),
                        moment_improvement=prior['moment']/max(current['moment'],1e-300),
                        passes=current['pair']<1e-10 and current['moment']<1e-10)
                    scale=max(abs(total[0,column]),Decimal('1e-300'))
                    component_records[key]={component:dict(
                        pair_defect_over_total_energy=float((components[index,0,column]+components[index,-1,column])/scale),
                        photon=str(components[index,0,column]),gas=str(components[index,-1,column]))
                        for index,component in enumerate(COMPONENTS)}
                    assert abs(float((total[0,column]+total[-1,column])/scale))==current['pair']
        checks.append(dict(name='Independent comparison with saved pre-repair atomic gate',passed=True))
    fixed=[key for key,value in comparison.items() if value['passes']]
    failed=[key for key,value in comparison.items() if not value['passes']]
    write_json(ROOT/'PRECISION-DIAGNOSIS.json',dict(comparison=comparison,component_defects=component_records,
        paired_step_columns_pass=len(fixed),paired_step_columns_fail=len(failed),failed_columns=failed,
        source_readiness_passed=source['all_checks_passed'],tolerance=1e-10))
    finish(folder,dict(checks=checks,comparison=comparison,component_defects=component_records,
        paired_step_columns_pass=len(fixed),paired_step_columns_fail=len(failed)),__file__,
        [*inputs,ROOT/'PRECISION-DIAGNOSIS.json'])
    print(json.dumps(dict(paired_step_columns_pass=len(fixed),failed_columns=failed,
        max_pair=max(value['new_pair'] for value in comparison.values()),
        max_moment=max(value['new_moment'] for value in comparison.values()))),flush=True)


if __name__=='__main__':
    main()

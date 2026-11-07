from source201 import *
COMPONENTS=['baseline','real_difference','virtual','state','MTS','total']


def norms(values,factor):
    shape=values.shape
    photon=np.moveaxis(values[...,1:97,:],-2,0).reshape(96,-1)
    solved=linear.solve_triangular(factor,photon,lower=True)
    return np.linalg.norm(solved,axis=0).reshape(shape[:-2]+(shape[-1],))


def subtract(left,right):
    return combine([left,(-right[0],-right[1])])


def primitives(pairs):
    total=combine([(high[:,:4],low[:,:4]) for high,low in pairs])
    outputs=[]
    for group in range(total[0].shape[0]):
        pieces=[(total[0][group,index],total[1][group,index]) for index in range(4)]
        pieces.extend([combine(pieces[1:4]),combine(pieces[:4])])
        outputs.append((np.stack([value[0] for value in pieces]),np.stack([value[1] for value in pieces])))
    return np.stack([pair[0] for pair in outputs]),np.stack([pair[1] for pair in outputs])


def analysis_protocol():
    record=read(ROOT/'frozen/analysis-protocol.json')
    for name,value in record['hashes'].items():
        assert digest(ROOT/name)==value,name


def freeze_analysis():
    assert not (ROOT/'actual').exists()
    assert not (ROOT/'frozen/analysis-protocol.json').exists()
    write(ROOT/'frozen/analysis-protocol.json',dict(frozen_utc=datetime.now(timezone.utc).isoformat(),
        hashes={name:digest(ROOT/name) for name in ('assess201.py','ANALYSIS-CONTRACT.md')}))
    print('Assessment protocol frozen before absolute evaluations.',flush=True)


def main():
    config=protocol();analysis_protocol()
    frozen=read(ROOT/'frozen/prediction-manifest.json')
    for name,value in frozen['files'].items():
        assert digest(ROOT/name)==value,name
    original,theta=source.context(config['target_fraction'])
    factor=linear.cholesky(original.basis.mass,lower=True)
    photon_norm=lambda values:norms(values,factor)
    rows=list(read(ROOT/'results/representation.json')['checks'])
    predictions=[];actuals=[];increment_parts=[];event_records=[]
    for index in range(36):
        for kind in ('prediction','actual'):
            path=ROOT/f'{kind}/event-{index:02d}.npz'
            record=read(path.with_suffix('.json'))
            assert digest(path)==record['sha256'] and not record['failed_checks']
            assert digest(record['loop_path'])==record['loop_sha256']
            rows.extend(dict(row,name=f'{kind}:{index}:'+row['name']) for row in record['checks'])
        prediction=packet(ROOT/f'frozen/event-{index:02d}-prediction.npz')
        actual=packet(ROOT/f'actual/event-{index:02d}.npz')
        part=packet(ROOT/f'prediction/event-{index:02d}.npz')
        predictions.append((prediction['high'],prediction['low']))
        actuals.append((actual['high'],actual['low']))
        increment_parts.append((part['high'][:4],part['low'][:4]))
        observed=tuple(np.stack([combine([(actual['high'][group],actual['low'][group]),
                    (-actual['high'][0],-actual['low'][0])])[part_index] for group in (1,2)]) for part_index in (0,1))
        error=subtract((prediction['high'],prediction['low']),observed)
        photon_error=photon_norm(error[0]+error[1])/np.maximum(photon_norm(observed[0]+observed[1]),1e-300)
        gas_error=abs(error[0][...,-1,:]+error[1][...,-1,:])/np.maximum(abs(observed[0][...,-1,:]+observed[1][...,-1,:]),1e-300)
        event_records.append(dict(event=index,maximum_photon_relative=float(photon_error.max()),
            maximum_gas_relative=float(gas_error.max()),aggregate_gate_applied_here=False))
        absolute_scale=np.maximum(photon_norm(actual['high'][1:]+actual['low'][1:]),photon_norm(actual['high'][0]+actual['low'][0]))
        for grid,component,column in np.ndindex(absolute_scale.shape):
            check(rows,f'event{index}:{grid}:{component}:{column}:absolute reconstruction',
                photon_norm(error[0]+error[1])[grid,component,column]/max(absolute_scale[grid,component,column],1e-300),1e-10,'identity')
    predicted=primitives(predictions)
    absolute=primitives(actuals)
    parts=primitives(increment_parts)
    observed=tuple(np.stack([combine([(absolute[0][group],absolute[1][group]),
                (-absolute[0][0],-absolute[1][0])])[part_index] for group in (1,2)]) for part_index in (0,1))
    discrepancy=subtract(predicted,observed)
    records=[]
    for label,measure in [('photon',photon_norm),('gas',lambda value:abs(value[...,-1,:]))]:
        denominator=measure(observed[0]+observed[1])
        relative=measure(discrepancy[0]+discrepancy[1])/np.maximum(denominator,1e-300)
        absolute_denominator=np.maximum(measure(absolute[0][1:]+absolute[1][1:]),measure(absolute[0][0]+absolute[1][0]))
        reconstruction=measure(discrepancy[0]+discrepancy[1])/np.maximum(absolute_denominator,1e-300)
        for grid,component,column in np.ndindex(relative.shape):
            name=f'{GRIDS[grid]}:{COMPONENTS[component]}:{column}:{label}'
            check(rows,name+':frozen full increment',relative[grid,component,column],.01,'prediction')
            check(rows,name+':absolute reconstruction',reconstruction[grid,component,column],1e-10,'identity')
            records.append(dict(grid=GRIDS[grid],component=COMPONENTS[component],model=('heavy','cold')[column//2],
                join=column%2,measure=label,relative=float(relative[grid,component,column]),
                actual_size=float(denominator[grid,component,column]),predicted_size=float(measure(predicted[0]+predicted[1])[grid,component,column])))
    mesh=subtract((predicted[0][0],predicted[1][0]),(predicted[0][1],predicted[1][1]))
    direct_mesh=subtract((absolute[0][1],absolute[1][1]),(absolute[0][2],absolute[1][2]))
    mesh_records=[]
    for label,measure in [('photon',photon_norm),('gas',lambda value:abs(value[...,-1,:]))]:
        for method,difference,denominator in [('increment',mesh,predicted[0][1]+predicted[1][1]),
                ('absolute_difference',direct_mesh,observed[0][1]+observed[1][1]),
                ('absolute_scale',direct_mesh,absolute[0][2]+absolute[1][2])]:
            relative=measure(difference[0]+difference[1])/np.maximum(measure(denominator),1e-300)
            for component,column in np.ndindex(relative.shape):
                check(rows,f'{COMPONENTS[component]}:{column}:{label}:{method}:mesh',relative[component,column],.01,'mesh')
                mesh_records.append(dict(component=COMPONENTS[component],model=('heavy','cold')[column//2],join=column%2,
                    measure=label,method=method,relative=float(relative[component,column])))
    decompositions=[]
    for grid_index,grid in enumerate(GRIDS):
        photon=(parts[0][2*grid_index],parts[1][2*grid_index])
        gas=(parts[0][2*grid_index+1],parts[1][2*grid_index+1])
        sum_pair=combine([photon,gas])
        reconstruction=subtract(sum_pair,(predicted[0][grid_index],predicted[1][grid_index]))
        for label,measure in [('photon',photon_norm),('gas',lambda value:abs(value[...,-1,:]))]:
            denominator=np.maximum(measure(sum_pair[0]+sum_pair[1]),1e-300)
            first=measure(photon[0]+photon[1])/denominator
            second=measure(gas[0]+gas[1])/denominator
            closure=measure(reconstruction[0]+reconstruction[1])/denominator
            for component,column in np.ndindex(denominator.shape):
                check(rows,f'{grid}:{component}:{column}:{label}:photon-gas closure',closure[component,column],1e-10,'identity')
                decompositions.append(dict(grid=grid,component=COMPONENTS[component],model=('heavy','cold')[column//2],join=column%2,
                    measure=label,omit_photon_error=float(first[component,column]),omit_gas_error=float(second[component,column]),
                    cancellation_factor=float(first[component,column]+second[component,column])))
    for name,pair in [('absolute',absolute),('predicted_delta',predicted),('observed_delta',observed),('split_parts',parts)]:
        values=pair[0]+pair[1]
        exchange=values[...,0,:]+values[...,-1,:]
        scale=np.maximum(np.maximum(abs(values[...,0,:]),abs(values[...,-1,:])),1e-300)
        for index in np.ndindex(scale.shape):
            check(rows,f'{name}:{index}:energy exchange',exchange[index]/scale[index],1e-10,'identity')
    nonzero=(photon_norm(observed[0]+observed[1])>0)&(abs(observed[0][...,-1,:]+observed[1][...,-1,:])>0)
    check(rows,'zero-correction forecast rejected for all nonzero components',int(not nonzero.all()),0,'negative_control')
    save(ROOT/'results/x14-source.npz',prediction_high=predicted[0],prediction_low=predicted[1],
        absolute_high=absolute[0],absolute_low=absolute[1],delta_high=observed[0],delta_low=observed[1],
        discrepancy_high=discrepancy[0],discrepancy_low=discrepancy[1],
        split_high=parts[0],split_low=parts[1],theta=theta,frequency=14.,components=np.array(COMPONENTS))
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'results/source-assessment.json',dict(state='qualified' if not failed else 'checks_failed',
        checks=rows,failed_checks=failed,records=records,mesh_records=mesh_records,decompositions=decompositions,
        event_diagnostics=event_records,events=36,new_virtual_integrals=0,full_frequency_panel_qualified=False,
        x14_qualified=not failed,shared_evaluator=True,observational_prediction=False,
        result_sha256=digest(ROOT/'results/x14-source.npz')))
    write(ROOT/'progress.json',dict(state='x14_qualified' if not failed else 'x14_checks_failed',failed_checks=len(failed)))
    print(json.dumps(dict(checks=len(rows),failed=failed,worst_prediction=max(row['relative'] for row in records),
        worst_mesh=max(row['relative'] for row in mesh_records),event_worst=max(row['maximum_photon_relative'] for row in event_records))),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['freeze','assess'])
    args=parser.parse_args()
    if args.phase=='freeze':freeze_analysis()
    else:main()

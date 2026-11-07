from stage153_separation_common import *
from decimal import Decimal,localcontext


def precise_readout(saved,reader):
    def decimal(value):
        return Decimal.from_float(float(value))
    with localcontext() as context:
        context.prec=60
        frequency=[decimal(value) for value in reader.frequency]
        measure=[decimal(value) for value in reader.measure]
        templates=[[decimal(value) for value in row] for row in reader.templates]
        capacity=sum(weight*value*value for weight,value in zip(measure,frequency))
        gram=[[sum(weight*row[left]*row[right] for weight,row in zip(measure,templates))
            for right in range(2)] for left in range(2)]
        determinant=gram[0][0]*gram[1][1]-gram[0][1]*gram[1][0]
        def columns(values):
            base,first,second,delta_first,delta_second=[decimal(values[index]) for index in [0,1,2,9,10]]
            return [base,first,second,delta_first,delta_second,
                first+delta_first,second+delta_second,base+first,base+second,
                base+first+delta_first,base+second+delta_second]
        energy=columns(saved['energy'])
        potentials=[columns(row) for row in saved['potential']]
        distortion=[[value-node*amount/capacity for value,amount in zip(row,energy)]
            for node,row in zip(frequency,potentials)]
        amplitudes=[]
        for column in range(11):
            rhs=[sum(weight*row[index]*values[column] for weight,row,values in zip(measure,templates,distortion)) for index in range(2)]
            amplitudes.append([(rhs[0]*gram[1][1]-rhs[1]*gram[0][1])/determinant,
                (gram[0][0]*rhs[1]-gram[1][0]*rhs[0])/determinant])
        residual=[[value-sum(template*amount for template,amount in zip(row,amplitudes[column]))
            for column,value in enumerate(values)] for row,values in zip(templates,distortion)]
        maximum=Decimal(0)
        for values in [potentials,distortion,residual,[[column[row] for column in amplitudes] for row in range(2)]]:
            for source_index,frozen_index,resolved_index in [(3,7,9),(4,8,10),(3,1,5),(4,2,6)]:
                denominator=max(abs(row[source_index]) for row in values)
                error=max(abs(row[resolved_index]-row[frozen_index]-row[source_index]) for row in values)
                maximum=max(maximum,error/max(denominator,Decimal('1e-300')))
        return dict(amplitudes=np.asarray([[float(row[index]) for row in amplitudes] for index in range(2)]),
            residual=np.asarray([[float(value) for value in row] for row in residual]),
            same_baseline_cancellation=float(maximum))


def main():
    modest()
    folder=ROOT/'results/precision'
    folder.mkdir(parents=True,exist_ok=False)
    analysis=verify_packet(ROOT/'results/analysis')
    failures=[row for row in analysis['checks'] if not row['passed']]
    assert failures and all(row['name'].startswith(('FROZEN_FORECAST:','Same baseline cancellation:','CONVERGENCE:')) for row in failures)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    checks,records,inputs=[],{},[ROOT/'results/analysis/status.json',ROOT/'PRECISION-NOTES.md',*ladder.inputs]
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for count in COUNTS:
                for match in [20,40]:
                    label=f'{model}-{route}-{count}-m{match}'
                    path=ROOT/'results/analysis'/(label+'-readout.npz')
                    saved=read_npz(path)
                    result=precise_readout(saved,reader)
                    test(checks,'60digit baseline/MTS cancellation:'+label,result['same_baseline_cancellation'],1e-8)
                    for position,name in enumerate(['mu','y']):
                        close(checks,'Independent60digit direct '+name+':'+label,
                            result['amplitudes'][position,3:5],saved['amplitudes'][position,9:11],1e-8)
                        close(checks,'Independent60digit baseline '+name+':'+label,
                            result['amplitudes'][position,:1],saved['amplitudes'][position,:1],1e-10)
                    close(checks,'Independent60digit direct residual:'+label,
                        result['residual'][:,3:5],saved['residual'][:,9:11],1e-10)
                    records[label]=dict(cancellation=result['same_baseline_cancellation'],
                        mu_relative=float(max(abs(result['amplitudes'][0,3:5]/saved['amplitudes'][0,9:11]-1))),
                        y_relative=float(max(abs(result['amplitudes'][1,3:5]/saved['amplitudes'][1,9:11]-1))))
                    np.savez_compressed(folder/(label+'.npz'),**result)
                    inputs.extend([path,folder/(label+'.npz')])
    report=dict(precision=60,records=records,raw_failures_retained=failures,
        repaired_construction='Baseline and frozen MTS plus independently saved small defect; sum/project/subtract in60digit arithmetic.',
        raw_saved_large_trajectory_subtractions_preserved=True,no_tolerance_changed=True,
        input_sources_or_history_changed=False,new_events=0,new_trajectories=0)
    write_json(ROOT/'PRECISION-SUMMARY.json',report)
    finish(folder,dict(checks=checks,raw_failure_count=len(failures),
        raw_cancellation_failures=sum(row['name'].startswith('Same baseline cancellation:') for row in failures),
        records=records,all_repaired=all(row['passed'] for row in checks)),__file__,
        [*inputs,ROOT/'PRECISION-SUMMARY.json'])
    print(json.dumps(dict(checks=len(checks),passed=all(row['passed'] for row in checks),
        raw_cancellation_failures=sum(row['name'].startswith('Same baseline cancellation:') for row in failures),
        maximum_cancellation=max(row['cancellation'] for row in records.values()),
        maximum_mu=max(row['mu_relative'] for row in records.values()),
        maximum_y=max(row['y_relative'] for row in records.values()))),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()

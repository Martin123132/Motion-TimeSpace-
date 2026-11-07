from reconcile224 import *
from decimal import Decimal,localcontext

def validate():
    protocol()
    report=read(ROOT/'results/status.json')
    rows=[]
    assert report['qualified']
    inputs=read(ROOT/'inputs-final.json')
    for record in report['summaries']:
        saved=packet(ROOT/f"spectra/{record['label']}.npz")
        for column in range(6):
            exact_error=Fraction()
            scale=Fraction()
            duplicate_norm=0.
            for index in range(len(saved['frequency'])):
                original=Fraction.from_float(float(saved['saved_potential'][index,column]))
                warm=Fraction.from_float(float(saved['warm_delta'][index,column]))
                cold=Fraction.from_float(float(saved['cold_delta'][index,column]))
                conditional=Fraction.from_float(float(saved['conditional_high'][index,column]))+Fraction.from_float(float(saved['conditional_low'][index,column]))
                exact_error=max(exact_error,abs(conditional-original-warm-cold))
                scale=max(scale,abs(cold))
                duplicate=(original+warm+cold+cold)-(original+warm+cold)
                assert duplicate==cold
                duplicate_norm+=float(saved['measure'][index])*float(duplicate)**2
            check(rows,record['label']+f':{column}:exact-rational cold increment preserved',float(exact_error/max(scale,Fraction(1,10**300))),1e-10,'identity')
            check(rows,record['label']+f':{column}:duplicate changes saved vector',int(duplicate_norm==0.),0,'negative_control')
        reference=load(inputs,REFERENCE/f"results/comparison/{record['model']}-{record['route']}-4096-m{record['matching']}.npz")
        columns=[0,0,3,4,7,8]
        original=reference['residual'][:,columns]
        with localcontext() as context:
            context.prec=80
            weights=[Decimal.from_float(float(value)) for value in saved['measure']]
            heat=Decimal.from_float(float(saved['heat']))
            for column in range(6):
                before=[Decimal.from_float(float(value)) for value in original[:,column]]
                delta=[Decimal.from_float(float(value)) for value in saved['delta_residual'][:,column]]
                before_squared=sum(weight*value*value for weight,value in zip(weights,before))
                after_squared=sum(weight*(value+change)**2 for weight,value,change in zip(weights,before,delta))
                direct=heat*(after_squared.sqrt()-before_squared.sqrt())
                expected=Decimal.from_float(record['residual_changes'][column]['signed_change'])
                error=abs(direct-expected)/max(abs(expected),Decimal('1e-300'))
                check(rows,record['label']+f':{column}:independent Decimal norm change',float(error),1e-10,'identity')
    for model in parent.MODELS:
        fine=load(inputs,PARENT/f'tail/{model}-4096/increment-readout.npz')
        heat=Fraction.from_float(float(fine['heat']))
        for count in parent.COUNTS:
            for side in ('left','right'):
                saved=packet(ROOT/f'boundaries/{model}-{count}-{side}.npz')
                for column in range(parent.WIDTH):
                    values=[Fraction.from_float(float(saved['high'][row,column]))+Fraction.from_float(float(saved['low'][row,column])) for row in (0,96,97,99)]
                    terms=[values[0],heat*values[1],values[2],-values[3]]
                    numerator=abs(sum(terms,Fraction()))
                    denominator=max(sum(map(abs,terms),Fraction()),Fraction(1,10**300))
                    check(rows,f'{model}:{count}:{side}:{column}:boundary energy/work/input ledger',float(numerator/denominator),1e-10,'identity')
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'results/independent-validation.json',dict(checks=rows,failed_checks=failed,qualified=not failed,
        finished_at=now(),script_sha256=digest(__file__),
        no_new_integrals=True,no_new_time_evolutions=True,
        scope='Exact stored-input sums, independent Decimal norm differences and boundary forcing conservation'))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),failures=failed[:12])),flush=True)

if __name__=='__main__':
    parent.old.source.modest()
    validate()

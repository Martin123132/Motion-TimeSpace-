from response221 import *


def diagnose():
    protocol();records=[];rows=[]
    for model in MODELS:
        for count in (2048,4096):
            folder=ROOT/f'responses/{model}-{count}'
            inputs=read(ROOT/f'inputs-response-{model}-{count}.json')
            system=matched.System(model,count,inputs)
            stored=packet(folder/'incoming.npz')
            homogeneous=stored['current'].copy();hprev=stored['previous'].copy()
            joint=homogeneous.copy();jprev=hprev.copy()
            increment=np.zeros_like(joint);iprev=increment.copy()
            start=round((START-.75)*count/.25);stop=round((STOP-.75)*count/.25)
            for index in range(start+1,stop+1):
                step=system.make_step(index)
                supplied=pair_source(verify_point(model,index*(FINE//count))[0],system,rows,'diagnostic')
                new_inc,unused=system.advance(increment,iprev,step,supplied)
                new_joint,unused=system.advance(joint,jprev,step,supplied)
                new_hom,unused=system.advance(homogeneous,hprev,step)
                iprev,increment=increment,new_inc;jprev,joint=joint,new_joint;hprev,homogeneous=homogeneous,new_hom
                actual=matched.collapsed(joint);expected=matched.collapsed(homogeneous+increment)
                for field,row in [('energy',0),('gas',96)]:
                    ratios=abs(actual[row]-expected[row])/np.maximum(abs(expected[row]),1e-300)
                    for column in np.where(ratios>1e-10)[0]:
                        with mp.workdps(100):
                            exact=lambda state:mp.mpf(float(state[row,column]))+mp.mpf(float(state[row,column+WIDTH]))
                            actual_mp=exact(joint);h_mp=exact(homogeneous);inc_mp=exact(increment);expected_mp=h_mp+inc_mp
                            scale=abs(h_mp)+abs(inc_mp)
                            profile,grid,component,join=np.unravel_index(column,(2,3,6,2))
                            records.append(dict(model=model,count=count,index=index,fraction=step['fraction'],field=field,column=int(column),
                                profile=PROFILES[profile],grid=GRIDS[grid],component=COMPONENTS[component],join=int(join),
                                actual=str(actual_mp),expected=str(expected_mp),absolute_error=str(abs(actual_mp-expected_mp)),
                                relative_to_net=float(abs(actual_mp-expected_mp)/max(abs(expected_mp),mp.mpf('1e-300'))),
                                relative_to_branch_sum=float(abs(actual_mp-expected_mp)/max(scale,mp.mpf('1e-300'))),
                                cancellation_factor=float(scale/max(abs(expected_mp),mp.mpf('1e-300')))))
            terminal=packet(folder/f'step-{stop}.npz')
            check(rows,f'{model}:{count}:joint replay',np.max(abs(joint-terminal['joint'])),0,'integrity')
            check(rows,f'{model}:{count}:increment replay',np.max(abs(increment-terminal['current'])),0,'integrity')
    write(ROOT/'results/matching-roundoff-diagnosis.json',dict(checks=rows,failed_checks=[row for row in rows if not row['passed']],records=records,
        interpretation='Raw twofold state sums evaluated at100digits; no changed tolerance or numerical trajectory. Branch cancellation diagnoses conditioning, not by itself a proof of all rounding error.'))
    print(json.dumps(dict(records=records,checks=len(rows),failed=sum(not row['passed'] for row in rows))),flush=True)


if __name__=='__main__':
    source.modest()
    diagnose()

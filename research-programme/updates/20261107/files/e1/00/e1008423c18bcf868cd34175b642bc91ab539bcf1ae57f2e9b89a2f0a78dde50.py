from common227 import *
import time

def solve_columns(matrix,values):
    factor,permutation=mp.mp.LU_decomp(matrix)
    result=mp.matrix(values.rows,values.cols)
    for column in range(values.cols):
        result[:,column]=mp.mp.U_solve(factor,mp.mp.L_solve(factor,values[:,column],permutation))
    return result

def run():
    config=protocol()
    inputs=read(ROOT/'inputs.json');rows=[];records=[]
    began=now()
    with mp.workdps(80):
        for model in parent.MODELS:
            reference=Reference(model,inputs)
            for fraction in config['coupled_probes']:
                coordinate=fraction*math.log(10)
                actual=reference.actual(coordinate)
                force=actual['force']
                returned=mp.matrix(97,1)
                returned[:96,:]=force
                returned[96]=actual['gas']
                for epsilon in (mp.mpf('.001'),mp.mpf('.0001')):
                    quotient=(returned/(1+epsilon)-returned/(1-epsilon))/(2*epsilon)
                    expected=-returned/(1-epsilon**2)
                    check(rows,f'{model}:{fraction}:{epsilon}:rate derivative',
                        parent.relative(quotient,expected),1e-10,'identity')
                check(rows,f'{model}:{fraction}:computed return moment',
                    abs((reference.temperature.T*force)[0]+actual['gas']-((reference.temperature.T-reference.beta)*force)[0])/
                    max(abs(actual['gas'])+abs((reference.temperature.T*force)[0]),mp.mpf('1e-300')),1e-10,'identity')
                for count in config['counts']:
                    alpha=mp.mpf('1.5')/mp.mpf(float(.25*math.log(10)/count))
                    rate=actual['rate'];stiffness=(actual['stiffness']+actual['stiffness'].T)/2
                    thermal=mp.matrix(97)
                    thermal[:96,:96]=alpha*reference.mass-rate*stiffness
                    thermal[:96,96:97]=rate*stiffness*reference.temperature
                    thermal[96:97,:96]=rate*reference.temperature.T*stiffness
                    thermal[96,96]=reference.heat*(alpha+1)-(rate*reference.temperature.T*stiffness*reference.temperature)[0]
                    thermal_density=mp.matrix(1,97)
                    thermal_density[:,:96]=reference.heat*reference.energy
                    thermal_density[96]=reference.heat**2
                    metric=inherited.model_parts(reference.background,coordinate)
                    operator=parent.matrix(metric['operator'])
                    scalar=alpha*mp.eye(4)-operator
                    drive=parent.matrix(metric['forcing'][:,None])
                    readout=parent.matrix(metric['row'][None,:])
                    direct=mp.mpf(float(metric['direct']))
                    scalar_response=solve_columns(scalar,drive)
                    effective=direct+(readout*scalar_response)[0]
                    index=round((fraction-.75)*4096/.25)
                    sources=parent.source_at(model,4096,index,reference.system,rows)
                    columns=[next(position for position,label in enumerate(parent.LABELS) if label==dict(
                        profile='quadratic',grid='eighth',component=component,join=0)) for component in ('baseline','MTS','total')]
                    forcing=mp.matrix(97,3)
                    for target,column in enumerate(columns):
                        forcing[:96,target]=sources['raw'][1:97,column]
                        forcing[96,target]=sources['raw'][97,column]
                    free=solve_columns(thermal,forcing)
                    response=solve_columns(thermal,returned)
                    free_density=thermal_density*free
                    loop=effective*(thermal_density*response)[0]
                    for sign in (1,-1,0):
                        denominator=1+sign*loop
                        assert denominator!=0
                        prediction=effective*free_density/denominator
                        state=free-sign*response*prediction
                        metric_state=scalar_response*(thermal_density*state)
                        block=mp.matrix(101)
                        block[:97,:97]=thermal+sign*returned*direct*thermal_density
                        block[:97,97:]=sign*returned*readout
                        block[97:,:97]=-drive*thermal_density
                        block[97:,97:]=scalar
                        rhs=mp.matrix(101,3);rhs[:97,:]=forcing
                        solved=solve_columns(block,rhs)
                        measured=direct*thermal_density*solved[:97,:]+readout*solved[97:,:]
                        check(rows,f'{model}:{fraction}:{count}:{sign}:independent block thermal',
                            parent.relative(solved[:97,:],state),1e-10,'independent_solve')
                        check(rows,f'{model}:{fraction}:{count}:{sign}:independent block metric',
                            parent.relative(solved[97:,:],metric_state),1e-10,'independent_solve')
                        check(rows,f'{model}:{fraction}:{count}:{sign}:independent H readout',
                            parent.relative(measured,prediction),1e-10,'independent_solve')
                    check(rows,f'{model}:{fraction}:{count}:baseline plus MTS equals total',
                        parent.relative(free[:,0]+free[:,1],free[:,2]),1e-10,'identity')
                    records.append(dict(model=model,fraction=fraction,count=count,implicit_loop=float(loop),
                        denominator=float(1+loop),relative_return=float(-loop/(1+loop)),
                        prescribed_H=[float(value) for value in effective*free_density],
                        scope='Single-step physical operator probe with real source; not a replacement time evolution'))
                print(json.dumps(dict(model=model,fraction=fraction,checks=len(rows),failed=sum(not row['passed'] for row in rows))),flush=True)
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'inputs-probes.json',inputs)
    write(ROOT/'results/probes.json',dict(checks=rows,failed_checks=failed,qualified=not failed,records=records,started_at=began,finished_at=now()))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),failures=failed[:8])),flush=True)

if __name__=='__main__':
    parent.old.source.modest()
    run()


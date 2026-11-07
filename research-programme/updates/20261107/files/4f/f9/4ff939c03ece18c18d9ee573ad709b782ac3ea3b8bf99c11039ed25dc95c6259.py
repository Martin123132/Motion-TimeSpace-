from common227 import *
from probes227 import solve_columns

def prepare():
    protocol()
    path=ROOT/'increment-configuration.json'
    assert not path.exists()
    write(path,dict(frozen_at=now(),hashes={name:digest(ROOT/name) for name in
        ('increment227.py','complete227.py','INCREMENT-VALIDATION.md')},
        source_probe_hash=digest(ROOT/'results/probes.json'),relative_tolerance=1e-10,
        purpose='Resolve the small physical feedback increment, not just the common solution'))

def verify():
    protocol()
    config=read(ROOT/'increment-configuration.json')
    for name,value in config['hashes'].items():
        assert digest(ROOT/name)==value,name
    assert digest(ROOT/'results/probes.json')==config['source_probe_hash']

def run():
    verify()
    inputs=read(ROOT/'inputs.json');rows=[];records=[]
    with mp.workdps(80):
        for model in parent.MODELS:
            reference=Reference(model,inputs)
            for fraction in read(ROOT/'configuration.json')['coupled_probes']:
                coordinate=fraction*math.log(10)
                actual=reference.actual(coordinate)
                returned=mp.matrix(97,1)
                returned[:96,:]=actual['force'];returned[96]=actual['gas']
                for count in (2048,4096):
                    alpha=mp.mpf('1.5')/mp.mpf(float(.25*math.log(10)/count))
                    rate=actual['rate'];stiffness=(actual['stiffness']+actual['stiffness'].T)/2
                    thermal=mp.matrix(97)
                    thermal[:96,:96]=alpha*reference.mass-rate*stiffness
                    thermal[:96,96:97]=rate*stiffness*reference.temperature
                    thermal[96:97,:96]=rate*reference.temperature.T*stiffness
                    thermal[96,96]=reference.heat*(alpha+1)-(rate*reference.temperature.T*stiffness*reference.temperature)[0]
                    density=mp.matrix(1,97)
                    density[:,:96]=reference.heat*reference.energy;density[96]=reference.heat**2
                    metric=inherited.model_parts(reference.background,coordinate)
                    scalar=alpha*mp.eye(4)-parent.matrix(metric['operator'])
                    drive=parent.matrix(metric['forcing'][:,None])
                    readout=parent.matrix(metric['row'][None,:]);direct=mp.mpf(float(metric['direct']))
                    scalar_response=solve_columns(scalar,drive)
                    effective=direct+(readout*scalar_response)[0]
                    index=round((fraction-.75)*4096/.25)
                    sources=parent.source_at(model,4096,index,reference.system,rows)
                    forcing=mp.matrix(97,3)
                    components=('baseline','MTS','total')
                    for target,component in enumerate(components):
                        column=next(position for position,label in enumerate(parent.LABELS) if label==dict(
                            profile='quadratic',grid='eighth',component=component,join=0))
                        forcing[:96,target]=sources['raw'][1:97,column]
                        forcing[96,target]=sources['raw'][97,column]
                    free=solve_columns(thermal,forcing)
                    response=solve_columns(thermal,returned)
                    free_density=density*free
                    free_H=effective*free_density
                    free_scalar=scalar_response*free_density
                    loop=effective*(density*response)[0]
                    for sign in (1,-1):
                        factor=-sign*loop/(1+sign*loop)
                        expected_H=factor*free_H
                        expected_thermal=-sign*response*(free_H/(1+sign*loop))
                        expected_scalar=scalar_response*(density*expected_thermal)
                        block=mp.matrix(101)
                        block[:97,:97]=thermal+sign*returned*direct*density
                        block[:97,97:]=sign*returned*readout
                        block[97:,:97]=-drive*density;block[97:,97:]=scalar
                        rhs=mp.matrix(101,3);rhs[:97,:]=forcing
                        solved=solve_columns(block,rhs)
                        measured_H=direct*density*solved[:97,:]+readout*solved[97:,:]-free_H
                        measured_thermal=solved[:97,:]-free
                        measured_scalar=solved[97:,:]-free_scalar
                        for column,component in enumerate(components):
                            label=f'{model}:{fraction}:{count}:{sign}:{component}'
                            errors=dict(H=parent.relative(measured_H[:,column],expected_H[:,column]),
                                thermal=parent.relative(measured_thermal[:,column],expected_thermal[:,column]),
                                scalar=parent.relative(measured_scalar[:,column],expected_scalar[:,column]))
                            for key,value in errors.items():
                                check(rows,label+':increment '+key,value,1e-10,'increment')
                            omission=parent.relative(mp.matrix(1,1),expected_H[:,column])
                            check(rows,label+':omitted-return negative control',int(omission<=mp.mpf('1e-10')),0,'negative_control')
                            records.append(dict(model=model,fraction=fraction,count=count,sign=sign,component=component,
                                loop=float(loop),relative_return=float(factor),expected_H_increment=float(expected_H[column]),
                                measured_H_increment=float(measured_H[column]),errors={key:float(value) for key,value in errors.items()}))
                    print(json.dumps(dict(model=model,fraction=fraction,count=count,checks=len(rows),failed=sum(not row['passed'] for row in rows))),flush=True)
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'inputs-increment.json',inputs)
    write(ROOT/'results/increment.json',dict(checks=rows,failed_checks=failed,qualified=not failed,
        records=records,finished_at=now(),digits=80,normalization='Each component feedback increment itself'))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),failures=failed[:8])),flush=True)

if __name__=='__main__':
    parent.old.source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','run'])
    globals()[parser.parse_args().phase]()


from common226 import *
from scipy.integrate import solve_ivp

def prepare():
    protocol()
    path=ROOT/'feedback-configuration.json'
    assert not path.exists()
    write(path,dict(frozen_at=now(),hashes={name:digest(ROOT/name) for name in
        ('feedback226.py','complete226.py','FINITE-TIME-FEEDBACK.md')},tolerance=1e-10,
        scope='Independent constant-coefficient controls for the causal return-bound derivation; no MTS calibration'))

def verify():
    protocol()
    config=read(ROOT/'feedback-configuration.json')
    for name,value in config['hashes'].items():
        assert digest(ROOT/name)==value,name

def run():
    verify()
    heat=.2
    duration=.7
    metric=np.diag([1.,heat])
    inverse=np.diag([1.,1/heat])
    thermal=np.array([[-1.4,1.4],[1.4/heat,-1-1.4/heat]])
    density_row=heat*np.array([1.,heat])
    scalar_free=-.3
    scalar_drive=.4
    scalar_readout=.6
    direct=.25
    scalar_operator=scalar_free+scalar_drive*scalar_readout
    beta=abs(scalar_drive*scalar_readout)
    gain=direct*math.exp(beta*duration)
    external=np.array([.3,-.3])
    norm_external=math.sqrt(external@inverse@external)
    q_external=heat**1.5*norm_external*duration**2/2
    unreturned_bound=gain*q_external
    rows=[];records=[]
    for strength in (0.,.1,1.,3.):
        for kind,exchange in (('balanced',np.array([.4,-.4])),('injected',np.array([.4,-.2]))):
            returned=strength*exchange
            norm_return=math.sqrt(returned@inverse@returned)
            injection_return=abs(returned.sum())
            exponent=gain*(heat*injection_return*duration+heat**1.5*norm_return*duration**2/2)
            bound=unreturned_bound*math.exp(exponent)
            full=np.zeros((3,3))
            full[:2,:2]=thermal-np.outer(inverse@returned,direct*density_row)
            full[:2,2]=-inverse@returned*scalar_readout
            full[2,:2]=scalar_drive*direct*density_row
            full[2,2]=scalar_operator
            forcing=np.r_[inverse@external,0.]
            solved=solve_ivp(lambda coordinate,state:full@state+forcing,(0,duration),np.zeros(3),
                method='DOP853',rtol=3e-12,atol=1e-14,dense_output=True)
            assert solved.success
            states=solved.sol(np.linspace(0,duration,65))
            output=direct*density_row@states[:2]+scalar_readout*states[2]
            check(rows,f'{strength}:{kind}:closed response below causal bound',
                np.max(abs(output))/bound,1+1e-10,'feedback_bound')
            test=np.array([.27,-.18,.04])
            xi=direct*density_row@test[:2]+scalar_readout*test[2]
            derivative=full@test+forcing
            actual_density_prime=density_row@derivative[:2]
            expected_density_prime=-heat**2*test[1]+heat*(external.sum()-returned.sum()*xi)
            check(rows,f'{strength}:{kind}:return energy identity',abs(actual_density_prime-expected_density_prime),1e-10,'identity')
            for epsilon in (1e-4,1e-5):
                rate1=1/(1+epsilon*xi)
                rate2=1/(1-epsilon*xi)
                difference=(rate1-rate2)/(2*epsilon)
                check(rows,f'{strength}:{kind}:{epsilon}:Hubble rate variation',
                    abs(difference+xi)/max(abs(xi),1e-300),1e-8,'independent_evolution')
            records.append(dict(strength=strength,kind=kind,peak=float(np.max(abs(output))),
                bound=bound,causal_exponent=exponent))
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'results/feedback-controls.json',dict(checks=rows,failed_checks=failed,qualified=not failed,
        records=records,finished_at=now(),numerical_MTS_feedback_gain_claimed=False))
    print(json.dumps(dict(checks=len(rows),failed=len(failed),failures=failed[:8])),flush=True)

if __name__=='__main__':
    parent.old.source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','run'])
    globals()[parser.parse_args().phase]()


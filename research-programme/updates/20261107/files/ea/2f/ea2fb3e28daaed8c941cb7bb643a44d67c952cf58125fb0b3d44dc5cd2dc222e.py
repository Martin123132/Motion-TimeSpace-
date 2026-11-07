from flrw_thermal_response import *


def main():
    modest()
    folder=ROOT/'results/flrw-conservation-refined'
    folder.mkdir(parents=True,exist_ok=False)
    previous_path=ROOT/'results/flrw-response/status.json'
    previous=json.loads(previous_path.read_text())
    checks=[]
    reports=[]
    for label in ['heavy','cold']:
        background=ThermalBackground(label)
        solution,rhs=solve_response(background)
        samples=np.linspace(0,background.end,101)[1:-1]
        analytic=[]
        finite={str(step):[] for step in [1e-5,5e-6,2.5e-6]}
        for point in samples:
            center=solution.sol(point)
            derivative=rhs(point,center)
            state,density,pressure,_=stress_response(background,point,center)
            scale=state['scale']
            mass2=background.parent.masses**2
            background_field_prime=state['prime']/state['hubble']
            background_prime_prime=-2*state['prime']-scale**2*mass2*state['fields']/state['hubble']
            kinetic_prime=np.sum(background_prime_prime*center[2:4]+state['prime']*derivative[2:4]-2*state['prime']*center[2:4])/scale**2
            potential_prime=np.sum(mass2*(background_field_prime*center[:2]+state['fields']*derivative[:2]))
            exact_derivative=state['photon']*(4*point-5)+kinetic_prime+potential_prime
            normalization=abs(exact_derivative)+3*abs(density+pressure)
            analytic.append(float(abs(exact_derivative+3*(density+pressure))/max(normalization,1e-100)))
            for step in [1e-5,5e-6,2.5e-6]:
                plus=stress_response(background,point+step,center+step*derivative)
                minus=stress_response(background,point-step,center-step*derivative)
                numerical=(plus[1]-minus[1])/(2*step)
                finite[str(step)].append(float(abs(numerical+3*(density+pressure))/max(normalization,1e-100)))
        maximum={step:max(values) for step,values in finite.items()}
        checks.append(dict(name=label+': analytic directional stress derivative conserves energy',passed=max(analytic)<1e-8,value=max(analytic),gate=1e-8))
        checks.append(dict(name=label+': refined independent difference clears unchanged gate',passed=maximum['2.5e-06']<1e-8,value=maximum['2.5e-06'],gate=1e-8))
        checks.append(dict(name=label+': coarse residual decreases with probe spacing',passed=maximum['2.5e-06']<maximum['5e-06']<maximum['1e-05'],values=maximum))
        reports.append(dict(model=label,analytic_ward_max=max(analytic),finite_difference_ward_max=maximum))
    failures=[row for row in previous['checks'] if not row['passed']]
    checks.append(dict(name='Original two finite-difference failures preserved',passed=len(failures)==2 and all(row['gate']==1e-8 for row in failures)))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),models=reports,
        retained_probe_failures=failures,physical_equations_and_acceptance_gate_unchanged=True),__file__,[ROOT/'flrw_thermal_response.py',previous_path])
    print(json.dumps(dict(checks=checks,models=reports)),flush=True)


if __name__=='__main__':
    main()

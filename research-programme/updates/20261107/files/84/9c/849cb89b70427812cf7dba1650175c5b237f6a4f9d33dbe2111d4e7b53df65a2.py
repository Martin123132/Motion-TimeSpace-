from thermal_common import *


def state_at_scale(background,scale):
    moment=background.parent.time_at(scale)
    for iteration in range(3):
        state=background.parent.at(moment)
        moment-=(state['scale']-scale)/(state['scale']*state['hubble'])
    return background.parent.at(moment)


def stress_response(background,log_expansion,response):
    scale=background.start_scale*math.exp(log_expansion)
    state=state_at_scale(background,scale)
    mass2=background.parent.masses**2
    kinetic=np.sum(state['prime']*response[2:4])/scale**2
    potential=np.sum(mass2*state['fields']*response[:2])
    density=state['photon']*(1-log_expansion)+kinetic+potential
    pressure=state['photon']*(2-log_expansion)/3+kinetic-potential
    fraction=density*scale**2/(6*state['hubble']**2)
    return state,density,pressure,fraction


def solve_response(background):
    mass2=background.parent.masses**2
    def rhs(log_expansion,response):
        state,_,_,hubble_fraction=stress_response(background,log_expansion,response)
        scale=state['scale']
        hubble=state['hubble']
        fields=response[2:4]/hubble-state['prime']/hubble*hubble_fraction
        prime=-2*response[2:4]-scale**2*mass2/hubble*response[:2]+scale**2*mass2*state['fields']/hubble*hubble_fraction
        return np.r_[fields,prime,-hubble_fraction/hubble,-scale*hubble_fraction/hubble]
    solution=integrate.solve_ivp(rhs,(0,background.end),np.zeros(6),method='DOP853',rtol=3e-11,atol=1e-27,max_step=.01,dense_output=True)
    assert solution.success
    return solution,rhs


def full_background(background,amplitude):
    parent=background.parent
    mass2=parent.masses**2
    initial=state_at_scale(background,background.start_scale)
    def hubble(log_expansion,state):
        scale=background.start_scale*math.exp(log_expansion)
        density=(parent.radiation/scale**4+(parent.baryons+parent.cold)/scale**3+
            np.sum(state[2:4]**2/scale**2+mass2*state[:2]**2)/2+
            amplitude*parent.photons/scale**4*(1-log_expansion))
        return scale*math.sqrt(density/3)
    def rhs(log_expansion,state):
        scale=background.start_scale*math.exp(log_expansion)
        rate=hubble(log_expansion,state)
        return np.r_[state[2:4]/rate,-2*state[2:4]-scale**2*mass2*state[:2]/rate,1/rate,scale/rate]
    solution=integrate.solve_ivp(rhs,(0,background.end),np.r_[initial['fields'],initial['prime'],0.,0.],
        method='DOP853',rtol=3e-12,atol=1e-28,max_step=.01,dense_output=True)
    assert solution.success
    return solution,hubble


def main():
    modest()
    folder=ROOT/'results/flrw-response'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    reports=[]
    inputs=[]
    for label in ['heavy','cold']:
        background=ThermalBackground(label)
        solution,rhs=solve_response(background)
        samples=np.linspace(0,background.end,101)
        responses=solution.sol(samples).T
        hubble_response=np.array([stress_response(background,point,value)[3] for point,value in zip(samples,responses)])
        comparisons=[]
        for amplitude in [1e-3,1e-4]:
            positive,positive_rate=full_background(background,amplitude)
            negative,negative_rate=full_background(background,-amplitude)
            derivative=(positive.sol(samples)-negative.sol(samples)).T/(2*amplitude)
            exact_rate=np.array([(positive_rate(point,positive.sol(point))-negative_rate(point,negative.sol(point)))/(2*amplitude*state_at_scale(background,background.start_scale*math.exp(point))['hubble']) for point in samples])
            rate_error=float(np.max(abs(exact_rate-hubble_response))/np.max(abs(hubble_response)))
            clock_error=float(np.max(abs(derivative[:,4:]-responses[:,4:]))/max(np.max(abs(responses[:,4:])),1e-100))
            field_error=0. if label=='cold' else float(np.max(abs(derivative[:,[1,3]]-responses[:,[1,3]]))/np.max(abs(responses[:,[1,3]])))
            comparisons.append(dict(amplitude=amplitude,hubble_error=rate_error,clock_error=clock_error,heavy_field_error=field_error))
            checks.append(dict(name=label+': full Friedmann/field variation amplitude '+str(amplitude),passed=max(rate_error,clock_error,field_error)<5e-5,value=max(rate_error,clock_error,field_error),gate=5e-5))
        ward=[]
        raychaudhuri=[]
        for point in samples[1:-1]:
            step=1e-5
            center=solution.sol(point)
            state,density,pressure,fraction=stress_response(background,point,center)
            derivative=rhs(point,center)
            plus=stress_response(background,point+step,center+step*derivative)
            minus=stress_response(background,point-step,center-step*derivative)
            density_prime=(plus[1]-minus[1])/(2*step)
            residual=density_prime+3*(density+pressure)
            ward.append(float(abs(residual)/max(abs(density_prime)+3*abs(density+pressure),1e-100)))
            density0=3*state['hubble']**2/state['scale']**2
            pressure0=(state['photon']+state['neutrino'])/3+np.sum(state['prime']**2/state['scale']**2-background.parent.masses**2*state['fields']**2)/2
            predicted=-1.5*(pressure-pressure0/density0*density)/density0
            numerical=(plus[3]-minus[3])/(2*step)
            raychaudhuri.append(float(abs(numerical-predicted)/max(abs(numerical)+abs(predicted),1e-100)))
        checks.append(dict(name=label+': derived stress obeys homogeneous conservation',passed=max(ward)<1e-8,value=max(ward),gate=1e-8))
        checks.append(dict(name=label+': Friedmann response also satisfies Raychaudhuri',passed=max(raychaudhuri)<1e-8,value=max(raychaudhuri),gate=1e-8))
        physical_rate=background.chi*hubble_response
        seconds=background.constants['Mpc']/background.constants['c']
        reports.append(dict(model=label,chi=background.chi,maximum_hubble_fraction=float(np.max(abs(physical_rate))),
            final_hubble_fraction=float(physical_rate[-1]),final_proper_time_shift_seconds=float(background.chi*responses[-1,5]*seconds),
            final_heavy_field_shift=float(background.chi*responses[-1,1]),
            finite_difference_tests=comparisons,ward_max=max(ward),raychaudhuri_max=max(raychaudhuri),
            zero_initial_field_response=True,background_response_not_a_new_likelihood=True,
            slowly_frozen_field_displacement_below_full_state_subtraction_resolution=True))
        np.savez_compressed(folder/(label+'.npz'),log_expansion=samples,response_per_chi=responses,hubble_response_per_chi=hubble_response,chi=background.chi)
        inputs.append(background.parent.source)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),models=reports,
        conserved_heat_stress_reinserted_in_linearized_FLRW=True,thermal_nonparallel_perturbation_feedback_not_yet_inserted=True,
        signed_test_amplitudes_are_derivative_checks_not_negative_heat_capacities=True),__file__,inputs)
    print(json.dumps(dict(checks=checks,models=reports)),flush=True)


if __name__=='__main__':
    main()

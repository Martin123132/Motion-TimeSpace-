from polarized_source import *


def main():
    modest()
    folder=ROOT/'results/moving-geometry'
    folder.mkdir(parents=True,exist_ok=False)
    checks,rows=[],[]
    metric=np.diag([1.,-1.,-1.,-1.])
    energy=.00045962015785263325
    for velocity in [[0,0,0],[.02,.005,-.01],[.2,-.1,.3]]:
        parameters=context(energy,.1,velocity,energy)
        label=' velocity='+str(velocity)
        transform=parameters['transform']
        checks.append(check('Lorentz metric preserved'+label,np.linalg.norm(transform.T@metric@transform-metric),3e-14))
        checks.append(check('Bath unit future timelike'+label,abs(dot(parameters['bath'],parameters['bath'])-1),3e-14))
        for name in ['incoming','outgoing']:
            jones=parameters[name+'_jones']
            stokes=parameters[name+'_stokes']
            checks.append(check('Gauge-corrected transverse Jones orthogonal '+name+label,np.linalg.norm(jones.T@jones-np.eye(2)),3e-14))
            checks.append(check('Stokes rotation orthogonal '+name+label,np.linalg.norm(stokes.T@stokes-np.eye(4)),3e-14))
            checks.append(check('Stokes intensity is invariant '+name+label,np.linalg.norm(stokes[0]-np.eye(4)[0]),3e-14))
        incoming=transform@np.array([parameters['energy'],0,0,parameters['energy']])
        outgoing=transform@np.r_[parameters['hard'],parameters['hard']*parameters['hard_direction']]
        checks.append(check('Incident ray returns to lab input'+label,np.linalg.norm(incoming-np.array([energy,0,0,energy]))/energy,3e-14))
        checks.append(check('Scattered ray returns to lab direction'+label,np.linalg.norm(outgoing[1:]/outgoing[0]-np.array([math.sqrt(.99),0,.1])),3e-14))
        mass_integral=0.
        for direction,weight in angular_nodes(12):
            doppler=dot(parameters['bath'],np.r_[1.,direction])
            mass_integral+=weight/doppler**2
        checks.append(check('Anisotropic bath gives scalar thermal mass'+label,abs(mass_integral/(4*np.pi)-1),1e-10))
        for direction in [np.array([0.,.8,.6]),np.array([1.,0.,0.]),np.array([0.,0.,-1.])]:
            upper=bath_ordered_upper(parameters,direction)
            sample=event(parameters['energy'],upper,parameters['hard_direction'],direction)
            hard_lab=transform@sample['photons'][1]
            soft_lab=transform@sample['photons'][2]
            checks.append(check('Hard/soft lab ordering boundary'+label,abs(hard_lab[0]/soft_lab[0]-1),3e-14))
            null=np.r_[1.,direction]
            checks.append(check('Bose occupation scalar'+label,abs((transform@null)[0]/dot(parameters['bath'],null)-1),3e-14))
        step=1e-5
        def aberration(cosine,azimuth):
            ray=np.r_[1.,math.sqrt(1-cosine**2)*math.cos(azimuth),math.sqrt(1-cosine**2)*math.sin(azimuth),cosine]
            transformed=np.linalg.inv(transform)@ray
            return transformed[1:]/transformed[0]
        derivative_cosine=(aberration(.1+step,0)-aberration(.1-step,0))/(2*step)
        derivative_azimuth=(aberration(.1,step)-aberration(.1,-step))/(2*step)
        jacobian=np.linalg.norm(np.cross(derivative_cosine,derivative_azimuth))
        checks.append(check('Solid-angle Jacobian independent differential check'+label,abs(jacobian/parameters['angular_jacobian']-1),2e-9))
        velocity=np.asarray(velocity)
        gamma=1/math.sqrt(1-velocity@velocity)
        momentum=gamma*velocity
        velocity_derivative=-velocity/(2*gamma**2)
        def born_at(delta,hold_momentum):
            mass=math.sqrt(1+delta)
            chosen=momentum/math.sqrt(momentum@momentum+mass**2) if hold_momentum else velocity
            return born_lab_source(energy,.1,chosen,energy,mass)
        delta=1e-3
        def derivative(function):
            return (-function(2*delta)+8*function(delta)-8*function(-delta)+function(-2*delta))/(12*delta)
        fixed_momentum=derivative(lambda shift:born_at(shift,True))
        fixed_velocity=derivative(lambda shift:born_at(shift,False))
        velocity_shift=derivative(lambda shift:born_lab_source(energy,.1,velocity+shift*velocity_derivative,energy))
        error=np.linalg.norm(fixed_momentum-fixed_velocity-velocity_shift)/np.linalg.norm(fixed_momentum)
        checks.append(check('Independent massive Born family obeys fixed-momentum chain rule'+label,error,2e-9))
        correction=canonical_momentum_correction(parameters)
        refined=canonical_momentum_correction(parameters,5e-4)
        checks.append(check('Canonical momentum derivative step refinement'+label,np.linalg.norm(correction-refined)/max(np.linalg.norm(correction),1e-25),2e-8))
        rows.append(dict(velocity=velocity.tolist(),mass_family_chain_rule_error=float(error),
                         canonical_event_matrix=correction[0].tolist()))
    checks.append(dict(name='Reject collinear basis singularity explicitly',passed=False))
    try:
        context(energy,1,[0,0,0],energy)
    except ValueError:
        checks[-1]['passed']=True
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=all(row['passed'] for row in checks),rows=rows),
           __file__,[ROOT/'moving_frame.py',ROOT/'polarized_source.py',ROOT/'reduced_amplitude.py'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()

from resolved_redistribution import *


def integrate_paired(theta,gas_temperature_scaled,spectrum,electron_radial,electron_polar,angular_order,
                     frequency_order,soft_order,minimum,maximum,progress=None):
    matrix=np.zeros((5,5))
    current=np.zeros(5)
    counts=0
    null_error=0.
    directions=list(source.angular_nodes(angular_order))
    nodes,quadrature=np.polynomial.legendre.leggauss(soft_order)
    electron_nodes=list(gas_rule(theta,electron_radial,electron_polar))
    prefactor=3*source.ALPHA/(128*np.pi**3)
    for electron_index,(velocity,electron_weight) in enumerate(electron_nodes):
        transform,bath,incident_doppler=incoming_transform(velocity)
        relative_flux=1-velocity[2]
        for frequency,frequency_weight in incoming_rule(frequency_order,minimum,maximum):
            energy=theta*frequency*incident_doppler
            input_basis=scalar_functions(frequency)
            input_potential=float(spectrum(math.log(frequency)))
            seed_weight=frequency_weight*frequency**2/np.expm1(frequency)/I3
            for hard_direction,hard_measure in directions:
                angle01=1-hard_direction[2]
                hard_doppler=source.dot(bath,np.r_[1.,hard_direction])
                for soft_direction,soft_measure in directions:
                    angle02=1-soft_direction[2]
                    angle12=1-hard_direction@soft_direction
                    soft_doppler=source.dot(bath,np.r_[1.,soft_direction])
                    ratio=soft_doppler/hard_doppler
                    middle=1+energy*angle02+ratio*(1+energy*angle01)
                    emission_upper=2*energy/(middle+math.sqrt(middle**2-4*ratio*angle12*energy))
                    absorption_upper=theta*frequency/soft_doppler
                    lower=minimum*theta/soft_doppler
                    signed,measures=[],[]
                    for sign,upper in [(1,emission_upper),(-1,absorption_upper)]:
                        if upper<=lower:
                            continue
                        halfwidth=(math.log(upper)-math.log(lower))/2
                        midpoint=(math.log(upper)+math.log(lower))/2
                        values=np.exp(midpoint+halfwidth*nodes)
                        signed.extend(sign*values)
                        measures.extend(halfwidth*quadrature*values)
                    if not signed:
                        continue
                    signed=np.asarray(signed)
                    measures=np.asarray(measures)
                    signs=np.sign(signed)
                    intensity,photons,final,hard,denominator=intensity_batch(energy,signed,hard_direction,soft_direction)
                    hard_frequency=hard*hard_doppler/theta
                    soft_frequency=abs(signed)*soft_doppler/theta
                    inside=(hard_frequency>=minimum)&(hard_frequency<=maximum)&(soft_frequency<=maximum)
                    photon_jump=scalar_functions(hard_frequency)+signs[:,None]*scalar_functions(soft_frequency)-input_basis
                    recoil=final[:,1:]
                    rest_energy=np.sum(recoil**2,axis=1)/(final[:,0]+1)
                    electron_jump=(transform[0,0]*rest_energy+recoil@transform[0,1:])/theta
                    jump=np.column_stack([photon_jump,electron_jump])
                    null_error=max(null_error,float(np.max(abs(jump[:,1]+jump[:,4]))))
                    stimulated=(1+1/np.expm1(hard_frequency))*((signs+1)/2+1/np.expm1(soft_frequency))
                    density=prefactor*hard*abs(signed)/(energy*denominator)*intensity
                    weights=.5*electron_weight*relative_flux*seed_weight*hard_measure*soft_measure*measures*density*stimulated*inside
                    departure=spectrum(np.log(hard_frequency))+signs*spectrum(np.log(soft_frequency))-input_potential+gas_temperature_scaled*electron_jump
                    matrix-=(jump.T*weights)@jump
                    current-=jump.T@(weights*departure)
                    counts+=len(signed)
        if progress:
            progress(electron_index+1,len(electron_nodes),counts,matrix,current)
    return matrix,current,dict(real_events=counts,maximum_common_temperature_event_residual=null_error,
                               electron_nodes=len(electron_nodes),hard_lab_ordered=True,
                               inverse_hard_seed_ordered=True,forward_inverse_symmetry_factor=.5)

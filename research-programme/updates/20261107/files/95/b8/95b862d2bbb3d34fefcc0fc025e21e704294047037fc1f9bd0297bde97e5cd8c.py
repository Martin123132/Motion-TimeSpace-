from resolved_redistribution import *


def angular_soft_pole(recoil_squared):
    beta_squared=recoil_squared/(1+recoil_squared)
    series=sum(beta_squared**power/(2*power+1) for power in range(1,13))
    return 2*source.ALPHA/np.pi*series


def coefficient(theta,electron_order=6,angular_order=6,frequency_order=12):
    result=0.
    angular=list(source.angular_nodes(angular_order))
    directions=np.array([item[0] for item in angular])
    angular_weights=np.array([item[1] for item in angular])
    frequency_rule=list(incoming_rule(frequency_order,1e-5,60.))
    frequencies=np.array([item[0] for item in frequency_rule])
    frequency_weights=np.array([item[1] for item in frequency_rule])
    seed=frequency_weights*frequencies**2/np.expm1(frequencies)/I3
    cosine=directions[:,2]
    for velocity,electron_weight in gas_rule(theta,electron_order,electron_order):
        transform,bath,incident_doppler=incoming_transform(velocity)
        energy=theta*frequencies[:,None]*incident_doppler
        hard=energy/(1+energy*(1-cosine))
        doppler=bath[0]-directions@bath[1:]
        hard_frequency=hard*doppler/theta
        recoil_squared=(energy-hard)**2+2*energy*hard*(1-cosine)
        pole=angular_soft_pole(recoil_squared)
        intensity=1+cosine**2+energy**2*(1-cosine)**2/(1+energy*(1-cosine))
        born=3/(16*np.pi)*(hard/energy)**2*intensity*(1+1/np.expm1(hard_frequency))
        result+=electron_weight*(1-velocity[2])*np.sum(seed[:,None]*angular_weights*born*pole)
    leading=16*source.ALPHA/(3*np.pi)*theta**2
    return float(result),float(result/leading)

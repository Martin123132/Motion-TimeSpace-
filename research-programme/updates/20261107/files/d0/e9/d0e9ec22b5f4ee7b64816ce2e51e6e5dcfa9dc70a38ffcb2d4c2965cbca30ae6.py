from coupled_system import *


def ward_identity(system,moment,states,relative_step=1e-5):
    background=system.background.at(moment)
    scale,hubble=background['scale'],background['hubble']
    pressure0=(background['photon']+background['neutrino'])/3+np.sum(background['prime']**2/scale**2-system.mass2*background['fields']**2)/2
    energy0=3*hubble**2/scale**2
    derivative=system.slow_rhs(moment,states)+system.collision_rhs(moment,states)
    step=relative_step*moment
    plus=system.stress(moment+step,states+step*derivative)
    minus=system.stress(moment-step,states-step*derivative)
    stresses=system.stress(moment,states)
    parts=[system.unpack(state) for state in states]
    residuals=[]
    scales=[]
    for index,(energy,current,stress) in enumerate(stresses):
        energy_prime=(plus[index][0]-minus[index][0])/(2*step)
        current_prime=(plus[index][1]-minus[index][1])/(2*step)
        theta=np.trace(parts[index]['rate'])
        momentum=system.momenta[index]
        energy_residual=energy_prime+3*hubble*energy+hubble*np.trace(stress)+theta*(energy0+pressure0)+1j*momentum@current/scale
        current_residual=current_prime+3*hubble*current+1j*scale*momentum@stress
        energy_scale=abs(energy_prime)+abs(3*hubble*energy)+abs(hubble*np.trace(stress))+abs(theta*(energy0+pressure0))+abs(momentum@current/scale)
        current_scale=np.linalg.norm(current_prime)+3*hubble*np.linalg.norm(current)+scale*np.linalg.norm(momentum@stress)
        if index==3:
            for own,partner,own_momentum,partner_stress in [(parts[0],parts[1],system.momenta[0],stresses[1]),(parts[1],parts[0],system.momenta[1],stresses[0])]:
                partner_energy,partner_current,partner_tensor=partner_stress
                theta=np.trace(own['rate'])
                volume=np.trace(own['metric'])/2
                product=(theta*partner_energy+np.trace(own['rate']@partner_tensor)-
                    1j*momentum@own['metric']@partner_current/scale+1j*(own_momentum@partner_current)*volume/scale)/2
                energy_residual+=product
                energy_scale+=abs(product)
                connection=geometry.christoffel_linear(1j*np.einsum('a,ij->aij',own_momentum,own['metric']))
                product=theta*partner_current/2
                for component in range(3):
                    product[component]+=scale*sum(connection[upper,upper,middle]*partner_tensor[middle,component]-connection[middle,upper,component]*partner_tensor[upper,middle] for upper in range(3) for middle in range(3))/2
                current_residual+=product
                current_scale+=np.linalg.norm(product)
        residuals.append([float(abs(energy_residual)/max(energy_scale,1e-30)),float(np.linalg.norm(current_residual)/max(current_scale,1e-30))])
        scales.append([float(energy_scale),float(current_scale)])
    return dict(residuals=residuals,normalizers=scales)


def observe(system,moment,states):
    background=system.background.at(moment)
    residuals=system.constraints(moment,states)
    features=[]
    normalized=[]
    screens=[]
    for index,state in enumerate(states):
        parts=system.unpack(state)
        photon,neutrino=system.moments(state)
        theta=np.trace(parts['metric'])/2
        cold=system.cold_numbers[index]-theta
        baryon=parts['number']-theta
        if index==3:
            left,right=[system.unpack(value) for value in states[:2]]
            volume_product=np.trace(left['metric'])*np.trace(right['metric'])/8+np.trace(left['metric']@right['metric'])/4
            cold+=volume_product
            baryon+=volume_product-(np.trace(left['metric'])*right['number']+np.trace(right['metric'])*left['number'])/4-left['velocity']@right['velocity']/2
        features.append(np.r_[cold,baryon,photon[0],neutrino[0],photon[1],neutrino[1],parts['velocity'],parts['field'],parts['prime'],np.trace(parts['rate']),parts['metric'].ravel()])
        momentum=system.momenta[index]
        curvature_scale=(momentum@momentum)*max(1.,np.linalg.norm(parts['metric']))
        normalized.append([float(abs(residuals[index,0])/curvature_scale),float(np.linalg.norm(residuals[index,1:])/(curvature_scale*max(1.,moment)))])
        screens.append(float(np.max(abs(np.einsum('ni,nij->nj',system.directions,parts['photon'])))))
    left,right=[system.unpack(value) for value in states[:2]]
    second=system.unpack(states[3])
    metric_rate=second['rate']+(left['metric']@right['rate']+right['metric']@left['rate'])/2
    return dict(features=np.array(features),constraint_normalized=normalized,screen_error=screens,
        second_metric_symmetry=float(np.max(abs(second['metric']-second['metric'].T))),
        second_metric_rate_symmetry=float(np.max(abs(metric_rate-metric_rate.T))))

from coupled_system import *


def initial_state(system,scale):
    background=system.background
    moment=background.time_at(scale)
    coefficients=boundary_coefficients(background.fraction,background.baryon_share)
    matter=background.mu
    inverse_opacity=1/background.kappa0
    shear0=coefficients['shear0']
    correction=matter*coefficients['shear_matter']+inverse_opacity*coefficients['shear_collision']
    photon_flow=moment**3*coefficients['photon0']+moment**4*(matter*coefficients['photon_matter']+inverse_opacity*coefficients['photon_collision'])
    neutrino_stress=-4*shear0*moment**2/15-8*correction*moment**3/45
    identity=np.eye(3)
    direction=system.directions
    screen=system.screen
    def trace_free(matrix):
        return matrix-identity*np.trace(matrix)/3
    def corrections(curvature):
        return correction*trace_free(curvature)+identity*matter*np.trace(curvature)/80
    def densities(curvature):
        return np.trace(curvature)*moment**2/16*(1-matter*moment/5)
    def fields(curvature):
        strength=background.beta**2*background.masses**2*background.frozen*np.trace(curvature)
        return -strength*moment**6/1680*(1-matter*moment/35),-strength*6*moment**5/1680*(1-matter*moment/30)
    def polarization(shear):
        return (-2*np.einsum('ni,ij,nj->n',direction,shear,direction)[:,None,None]*screen+
            (4/3)*screen@shear@screen)/background.at(moment)['opacity']
    scalar_odd=moment**3/36-matter*moment**4/240
    tensor_odd=10*moment**3/(3*(15+4*background.fraction))-correction*moment**4/3
    states=[]
    curvatures=[]
    seeds=[]
    for momentum in system.momenta[:3]:
        seed=inherited.seed_linear(momentum)
        curvature=inherited.linear_ricci(seed,momentum)
        scalar=np.trace(curvature)
        traceless=trace_free(curvature)
        leading=shear0*traceless-identity*scalar/24
        next_order=corrections(curvature)
        metric=seed+moment**2*leading+(2/3)*moment**3*next_order
        rate=moment*leading+moment**2*next_order
        density=densities(curvature)
        velocity=1j*momentum*photon_flow*scalar
        photon=4*density/3*screen/2+2*(direction@velocity)[:,None,None]*screen+polarization(trace_free(rate))
        neutrino=(4*density/3+(15/2)*neutrino_stress*np.einsum('ni,ij,nj->n',direction,traceless,direction)-
            1j*(direction@momentum)*(scalar_odd*scalar+tensor_odd*np.einsum('ni,ij,nj->n',direction,traceless,direction)))
        field,prime=fields(curvature)
        states.append(system.pack(metric,rate,field,prime,density+np.trace(metric)/2,velocity,photon,neutrino))
        curvatures.append(curvature)
        seeds.append(seed)
    pair=inherited.seed_geometry(*system.momenta[:2],background.fraction)
    curvature=pair['ricci2']
    next_order=corrections(curvature)+(seeds[0]@corrections(curvatures[1])+seeds[1]@corrections(curvatures[0]))/2
    metric=pair['seed2']+moment**2*pair['metric2_time_coefficient']+(2/3)*moment**3*next_order
    rate=moment*pair['rate2']+moment**2*corrections(curvature)
    left,right=[system.unpack(state) for state in states[:2]]
    hleft,hright=left['metric'],right['metric']
    commutator=(hleft@right['rate']-right['rate']@hleft+hright@left['rate']-left['rate']@hright)/2
    physical_shear=trace_free(rate+commutator/2)
    density=densities(curvature)
    velocity=1j*system.momenta[3]*photon_flow*np.trace(curvature)
    local_velocity=velocity-(hleft@right['velocity']+hright@left['velocity'])/4
    photon=4*density/3*screen/2+2*(direction@local_velocity)[:,None,None]*screen+polarization(physical_shear)
    tensor_p,tensor_q=[trace_free(value) for value in curvatures[:2]]
    tensor2=trace_free(curvature)+(hleft@tensor_q-tensor_q@hleft+hright@tensor_p-tensor_p@hright)/4
    scalar_gradient=1j*(direction@system.momenta[3])*np.trace(curvature)
    for own,partner,partner_momentum in [(seeds[0],curvatures[1],system.momenta[1]),(seeds[1],curvatures[0],system.momenta[0])]:
        scalar_gradient-=.25j*(direction@own@partner_momentum)*np.trace(partner)
    covariant_tensor2=trace_free(curvature)+(seeds[0]@tensor_q+seeds[1]@tensor_p)/2
    tensor_gradient=1j*np.einsum('i,jk->ijk',system.momenta[3],covariant_tensor2)
    frame_correction=np.zeros(len(direction),complex)
    for own,partner,own_momentum,partner_momentum in [(seeds[0],tensor_q,system.momenta[0],system.momenta[1]),(seeds[1],tensor_p,system.momenta[1],system.momenta[0])]:
        connection=geometry.christoffel_linear(1j*np.einsum('a,ij->aij',own_momentum,own))
        tensor_gradient-=(np.einsum('lij,lk->ijk',connection,partner)+np.einsum('lik,jl->ijk',connection,partner))/2
        partner_gradient=1j*np.einsum('i,jk->ijk',partner_momentum,partner)
        shifted=direction@own.T
        frame_correction-=.25*(np.einsum('ni,nj,nk,ijk->n',shifted,direction,direction,partner_gradient)+
            np.einsum('ni,nj,nk,ijk->n',direction,shifted,direction,partner_gradient)+
            np.einsum('ni,nj,nk,ijk->n',direction,direction,shifted,partner_gradient))
    tensor_gradient=np.einsum('ni,nj,nk,ijk->n',direction,direction,direction,tensor_gradient)+frame_correction
    neutrino=(4*density/3+(15/2)*neutrino_stress*np.einsum('ni,ij,nj->n',direction,tensor2,direction)-
        scalar_odd*scalar_gradient-tensor_odd*tensor_gradient)
    volume_left,volume_right=np.trace(hleft)/2,np.trace(hright)/2
    volume2=np.trace(metric)/2-np.trace(hleft@hright)/4
    number=density+volume2+volume_left*volume_right/2+(volume_left*densities(curvatures[1])+volume_right*densities(curvatures[0]))/2+left['velocity']@right['velocity']/2
    field,prime=fields(curvature)
    states.append(system.pack(metric,rate,field,prime,number,velocity,photon,neutrino))
    system.cold_numbers[3]=np.trace(pair['seed2'])/2-np.trace(seeds[0]@seeds[1])/4+np.trace(seeds[0])*np.trace(seeds[1])/8
    states=np.array(states,dtype=complex)
    before=system.constraints(moment,states)
    projected,changes=system.project_constraints(moment,states)
    return moment,projected,dict(projection_relative_changes=changes,
        maximum_constraint_before=float(np.max(abs(before))),maximum_constraint_after=float(np.max(abs(system.constraints(moment,projected)))))

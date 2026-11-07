from reduced_amplitude import *


def boost_matrix(velocity):
    velocity=np.asarray(velocity,dtype=float)
    squared=float(velocity@velocity)
    if squared>=1:
        raise ValueError('Electron velocity must be subluminal')
    gamma=1/math.sqrt(1-squared)
    output=np.eye(4)
    output[0,0]=gamma
    output[0,1:]=gamma*velocity
    output[1:,0]=gamma*velocity
    output[1:,1:]+=gamma**2/(gamma+1)*np.outer(velocity,velocity)
    return output


def jones_rotation(transform,rest_photon,rest_frame,lab_direction):
    transformed_photon=transform@rest_photon
    transported=np.array([transform@polarization for polarization in rest_frame])
    transported-=transported[:,0,None]/transformed_photon[0]*transformed_photon
    chosen=frame(lab_direction)
    return chosen[:,1:]@transported[:,1:].T


def stokes_rotation(jones):
    return np.einsum('uab,bc,vcd,ad->uv',PAULI,jones,PAULI,jones.conj()).real/2


def context(lab_energy,lab_cosine,velocity,temperature):
    velocity=np.asarray(velocity,dtype=float)
    if velocity.shape!=(3,) or not np.all(np.isfinite(velocity)):
        raise ValueError('A finite three-component velocity is required')
    if not (np.isfinite(lab_energy) and lab_energy>0 and np.isfinite(temperature) and temperature>0):
        raise ValueError('Energy and temperature must be positive and finite')
    if not (-1<lab_cosine<1):
        raise ValueError('The scattering-plane basis excludes exactly collinear rays')
    incoming_lab=np.array([0.,0.,1.])
    outgoing_lab=np.array([math.sqrt(1-lab_cosine**2),0.,lab_cosine])
    inverse_boost=boost_matrix(-velocity)
    incoming_rest=inverse_boost@np.r_[lab_energy,lab_energy*incoming_lab]
    outgoing_rest=inverse_boost@np.r_[1.,outgoing_lab]
    incoming_direction=incoming_rest[1:]/incoming_rest[0]
    outgoing_direction=outgoing_rest[1:]/outgoing_rest[0]
    cosine=float(incoming_direction@outgoing_direction)
    first=outgoing_direction-cosine*incoming_direction
    first/=np.linalg.norm(first)
    second=np.cross(incoming_direction,first)
    orientation=np.column_stack([first,second,incoming_direction])
    rotation=np.eye(4)
    rotation[1:,1:]=orientation
    transform=boost_matrix(velocity)@rotation
    bath=np.linalg.inv(transform)@np.array([1.,0.,0.,0.])
    energy=float(incoming_rest[0])
    hard=energy/(1+energy*(1-cosine))
    hard_direction=np.array([math.sqrt(1-cosine**2),0.,cosine])
    photons=[np.array([energy,0,0,energy]),np.r_[hard,hard*hard_direction]]
    incoming_jones=jones_rotation(transform,photons[0],frame(np.array([0.,0.,1.])),incoming_lab)
    outgoing_jones=jones_rotation(transform,photons[1],frame(hard_direction),outgoing_lab)
    hard_doppler=dot(bath,np.r_[1.,hard_direction])
    hard_lab_energy=hard*hard_doppler
    hard_bose=1+1/np.expm1(hard_lab_energy/temperature)
    gamma=boost_matrix(velocity)[0,0]
    angular_jacobian=1/(gamma**2*(1-velocity@outgoing_lab)**2)
    relative_flux=1-velocity@incoming_lab
    tree_intensity=1+cosine**2+energy**2*(1-cosine)**2/(1+energy*(1-cosine))
    reference=3/(16*np.pi)*(hard/energy)**2*tree_intensity*hard_bose*relative_flux*angular_jacobian
    return dict(lab_energy=lab_energy,lab_cosine=lab_cosine,velocity=velocity,temperature=temperature,
                energy=energy,cosine=cosine,hard=hard,hard_direction=hard_direction,bath=bath,
                transform=transform,incoming_jones=incoming_jones,outgoing_jones=outgoing_jones,
                incoming_stokes=stokes_rotation(incoming_jones),outgoing_stokes=stokes_rotation(outgoing_jones),
                hard_doppler=hard_doppler,hard_bose=hard_bose,relative_flux=relative_flux,
                angular_jacobian=angular_jacobian,born_differential_over_thomson=reference)


def lab_moments(rest,parameters):
    output=np.empty_like(rest)
    output[0]=rest[0]
    output[1:5]=np.einsum('ab,bij->aij',parameters['transform'],rest[1:5])
    output[5:9]=np.einsum('ab,bij->aij',parameters['transform'],rest[5:9])
    return np.einsum('ab,kbc,dc->kad',parameters['outgoing_stokes'],output,parameters['incoming_stokes'])


def bath_ordered_upper(parameters,direction):
    energy=parameters['energy']
    angle01=1-parameters['cosine']
    angle02=1-direction[2]
    angle12=1-parameters['hard_direction']@direction
    soft_doppler=dot(parameters['bath'],np.r_[1.,direction])
    ratio=soft_doppler/parameters['hard_doppler']
    middle=1+energy*angle02+ratio*(1+energy*angle01)
    return 2*energy/(middle+math.sqrt(middle**2-4*ratio*angle12*energy))

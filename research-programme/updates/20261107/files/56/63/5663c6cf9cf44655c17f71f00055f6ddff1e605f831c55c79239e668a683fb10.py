from thermal_radial import *
from emission_rates import ALPHA


def kinematic_spinor_shift(momentum,spatial_shift):
    energy_shift=sum(momentum[index+1]*spatial_shift[index] for index in range(3))/momentum[0]
    states=spin.spinors(momentum)
    first,second,third=spatial_shift
    pauli=mp.matrix([[third,first-mp.j*second],[first+mp.j*second,-third]])
    output=mp.zeros(4,2)
    for row in range(2):
        for column in range(2):
            output[row,column]=energy_shift/(2*(momentum[0]+1))*states[row,column]
            output[row+2,column]=pauli[row,column]/mp.sqrt(momentum[0]+1)-energy_shift/(2*(momentum[0]+1))*states[row+2,column]
    return output


def external_finite_constant(initial,incoming,outgoing,first_pol,second_pol,null):
    final=initial+incoming-outgoing
    direction=mp.matrix(list(outgoing)[1:])/outgoing[0]
    initial_energy,initial_spin=external_shift(initial,null)
    final_energy,final_spin=external_shift(final,null)
    hard_shift=(initial_energy-final_energy)/(1-sum(final[index+1]*direction[index] for index in range(3))/final[0])
    initial_delta=mp.matrix([initial_energy,0,0,0])
    hard_delta=spin.photon(hard_shift,direction)
    final_spin+=kinematic_spinor_shift(final,-hard_shift*direction)
    direct,crossed=spin.propagator(initial+incoming),spin.propagator(initial-outgoing)
    first_vertex,second_vertex=spin.slash(first_pol),spin.slash(second_pol)
    variation=(-second_vertex*direct*spin.slash(initial_delta)*direct*first_vertex
               -first_vertex*crossed*spin.slash(initial_delta-hard_delta)*crossed*second_vertex)
    tree=compton(initial,incoming,outgoing,first_pol,second_pol)
    left,right=spin.spinors(final).transpose_conj()*spin.gamma_matrices()[0],spin.spinors(initial)
    residue_finite=-1/(initial[0]*spin.dot(initial,null))-1/(final[0]*spin.dot(final,null))
    return (final_spin.transpose_conj()*spin.gamma_matrices()[0]*tree*right
            +left*tree*initial_spin+left*variation*right+residue_finite*left*tree*right)


def finite_dressed(initial,incoming,outgoing,first_pol,second_pol,direction,temperature):
    if mp.norm(mp.matrix(list(initial)[1:]))>mp.mpf('1e-40'):
        raise ValueError('This fixed-direction kinematic update is for the resting incoming electron')
    coefficients=radial_decomposition(initial,incoming,outgoing,first_pol,second_pol,direction)
    final=initial+incoming-outgoing
    null=spin.photon(mp.mpf(1),direction)
    radial=coefficients['constant']*temperature**2*mp.pi**2/6
    for pole in coefficients['poles']:
        scaled=pole['location']/temperature
        principal_value=(mp.log(scaled/(2*mp.pi))-mp.re(mp.digamma(mp.j*scaled/(2*mp.pi))))/2
        kernel=principal_value-mp.j*mp.pi*pole['denominator_slope_sign']/(2*mp.expm1(scaled))
        radial+=pole['coefficient']*kernel
    result=spin.spinors(final).transpose_conj()*spin.gamma_matrices()[0]*radial*spin.spinors(initial)
    result+=external_finite_constant(initial,incoming,outgoing,first_pol,second_pol,null)*temperature**2*mp.pi**2/6
    return result


def integrate_dressed(energy,hard_cosine,temperature,order):
    initial=mp.matrix([1,0,0,0])
    incoming_direction=mp.matrix([0,0,1])
    hard_direction=mp.matrix([mp.sqrt(1-hard_cosine**2),0,hard_cosine])
    incoming=spin.photon(energy,incoming_direction)
    outgoing=spin.photon(energy/(1+energy*(1-hard_cosine)),hard_direction)
    frames=[spin.frame(incoming_direction),spin.frame(hard_direction)]
    tensors=[[mp.zeros(2) for second in range(2)] for first in range(2)]
    nodes,weights=np.polynomial.legendre.leggauss(order)
    for cosine,weight in zip(nodes,weights):
        cosine=mp.mpf(float(cosine))
        for azimuth_index in range(2*order):
            azimuth=mp.pi*(mp.mpf(azimuth_index)+mp.mpf('.5'))/order
            direction=mp.matrix([mp.sqrt(1-cosine**2)*mp.cos(azimuth),mp.sqrt(1-cosine**2)*mp.sin(azimuth),cosine])
            measure=mp.mpf(float(weight))*mp.pi/order
            for first,second in itertools.product([0,1],repeat=2):
                tensors[first][second]+=measure*finite_dressed(initial,incoming,outgoing,frames[0][first],frames[1][second],direction,temperature)
    prefactor=4*mp.pi*mp.mpf(str(ALPHA))/(2*(2*mp.pi)**3)
    array=np.array([[[[complex(prefactor*tensors[first][second][final_spin,initial_spin])
                       for initial_spin in range(2)] for final_spin in range(2)]
                     for second in range(2)] for first in range(2)])
    tree,final=spin.single_tensor(energy,hard_direction)
    interference=2*float(np.vdot(tree,array).real)/float(np.vdot(tree,tree).real)
    return array,dict(energy=float(energy),hard_cosine=float(hard_cosine),temperature=float(temperature),
                      angular_order=order,amplitude_interference_over_bare=float(interference),
                      amplitude_norm=float(np.linalg.norm(array)),
                      scope='Soft-pole-subtracted dressed amplitude; not a complete differential or inclusive rate')

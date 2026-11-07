import itertools
import mpmath as mp
from thermal_vertex_common import *
import dirac_amplitude as spin


def inverse(momentum):
    return spin.slash(momentum)-mp.eye(4)


def contracted_chain(matrices):
    gamma=spin.gamma_matrices()
    return sum(((-1 if index==0 else 1)*gamma[index]*matrices*gamma[index]
                for index in range(4)),mp.zeros(4))


def self_energy(momentum, bath):
    return sum((contracted_chain(spin.propagator(momentum-sign*bath))
                for sign in [-1,1]),mp.zeros(4))


def vertex(outgoing, incoming, polarization, bath):
    return sum((contracted_chain(spin.propagator(outgoing-sign*bath)*spin.slash(polarization)
                                *spin.propagator(incoming-sign*bath))
                for sign in [-1,1]),mp.zeros(4))


def ordered_blocks(initial, first, second, first_pol, second_pol, bath):
    middle=initial+first
    final=middle+second
    propagator=spin.propagator(middle)
    first_vertex,second_vertex=spin.slash(first_pol),spin.slash(second_pol)
    box=sum((contracted_chain(spin.propagator(final-sign*bath)*second_vertex
                             *spin.propagator(middle-sign*bath)*first_vertex
                             *spin.propagator(initial-sign*bath))
             for sign in [-1,1]),mp.zeros(4))
    return dict(self_energy=second_vertex*propagator*self_energy(middle,bath)*propagator*first_vertex,
                incoming_vertex=second_vertex*propagator*vertex(middle,initial,first_pol,bath),
                outgoing_vertex=vertex(final,middle,second_pol,bath)*propagator*first_vertex,
                box=box)


def compton(initial, incoming, outgoing, incoming_pol, outgoing_pol, bath=None, omit=None):
    transfers=[incoming,-outgoing]
    polarizations=[incoming_pol,outgoing_pol]
    total=mp.zeros(4)
    for first,second in [(0,1),(1,0)]:
        if bath is None:
            total+=spin.slash(polarizations[second])*spin.propagator(initial+transfers[first])*spin.slash(polarizations[first])
        else:
            blocks=ordered_blocks(initial,transfers[first],transfers[second],polarizations[first],polarizations[second],bath)
            total+=sum((value for name,value in blocks.items() if name!=omit),mp.zeros(4))
    return total


def incoming_ward_rhs(initial, incoming, outgoing, outgoing_pol, bath):
    final=initial+incoming-outgoing
    direct,crossed=initial+incoming,initial-outgoing
    direct_prop,crossed_prop=spin.propagator(direct),spin.propagator(crossed)
    hard=spin.slash(outgoing_pol)
    return (-self_energy(final,bath)*crossed_prop*hard
            +inverse(final)*crossed_prop*self_energy(crossed,bath)*crossed_prop*hard
            +inverse(final)*crossed_prop*vertex(crossed,initial,outgoing_pol,bath)
            -vertex(final,direct,outgoing_pol,bath)*direct_prop*inverse(initial)
            -hard*direct_prop*self_energy(direct,bath)*direct_prop*inverse(initial)
            +hard*direct_prop*self_energy(initial,bath))


def on_shell(spatial):
    return mp.matrix([mp.sqrt(1+sum(value**2 for value in spatial)),*spatial])


def external_shift(momentum,bath):
    gamma0=spin.gamma_matrices()[0]
    hamiltonian=momentum[0]*mp.eye(4)-gamma0*inverse(momentum)
    perturbation=gamma0*self_energy(momentum,bath)
    states=spin.spinors(momentum)
    energy_shift=(states.transpose_conj()*perturbation*states)[0,0]/(2*momentum[0])
    negative=(mp.eye(4)-hamiltonian/momentum[0])/2
    correction=negative*perturbation*states/(2*momentum[0])
    return mp.re(energy_shift),correction


def dressed_event(energy,hard_direction,bath,epsilon):
    initial=mp.matrix([1,0,0,0])
    incoming=spin.photon(energy,mp.matrix([0,0,1]))
    hard_energy=energy/(1+energy*(1-hard_direction[2]))
    outgoing=spin.photon(hard_energy,hard_direction)
    final=initial+incoming-outgoing
    initial_shift,initial_spin_shift=external_shift(initial,bath)
    final_shift,final_spin_shift=external_shift(final,bath)
    hard_shift=(initial_shift-final_shift)/(1-sum(final[index+1]*hard_direction[index] for index in range(3))/final[0])
    outgoing_new=spin.photon(hard_energy+epsilon*hard_shift,hard_direction)
    initial_new=initial+mp.matrix([epsilon*initial_shift,0,0,0])
    final_new=initial_new+incoming-outgoing_new
    initial_states=spin.spinors(initial)+epsilon*initial_spin_shift
    final_states=spin.spinors(on_shell(list(final_new)[1:]))+epsilon*final_spin_shift
    return dict(initial=initial_new,incoming=incoming,outgoing=outgoing_new,final=final_new,
                initial_states=initial_states,final_states=final_states,
                initial_shift=initial_shift,final_shift=final_shift,hard_shift=hard_shift)

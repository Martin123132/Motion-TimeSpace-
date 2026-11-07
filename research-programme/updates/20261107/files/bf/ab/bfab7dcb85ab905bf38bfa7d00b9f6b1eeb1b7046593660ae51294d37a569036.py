from batched_real import *


def channels(amplitudes):
    return amplitudes.transpose(3,4,1,2,0).reshape(4,4,2)


def difference(amplitudes,photon_observables,electron_initial=0.,electron_final=0.):
    kraus=channels(amplitudes)
    incoming=photon_observables[0]+electron_initial*np.eye(2)
    outgoing=np.kron(photon_observables[1],np.eye(2))+np.kron(np.eye(2),photon_observables[2])+electron_final*np.eye(4)
    return outgoing@kraus-kraus@incoming


def linear_pair(amplitudes,observables,perturbations,electron_observables=(0.,0.),electron_perturbations=(0.,0.)):
    first=difference(amplitudes,observables,*electron_observables)
    second=difference(amplitudes,perturbations,*electron_perturbations)
    return -float(np.vdot(second,first).real)/4


def nonlinear_weak(amplitudes,observables,occupations,electron_weights,electron_observables=(0.,0.)):
    kraus=channels(amplitudes)
    delta=difference(amplitudes,observables,*electron_observables)
    incoming,first,second=occupations
    gain=np.kron(np.eye(2)+first,np.eye(2)+second)
    loss=np.kron(first,second)
    forward=np.einsum('sai,ij,sbj,ba->',delta,incoming,kraus.conj(),gain).real
    reverse=np.einsum('sai,ij,sbj,ba->',delta,np.eye(2)+incoming,kraus.conj(),loss).real
    return (electron_weights[0]*forward-electron_weights[1]*reverse)/4


def matrix_occupation(frequency,potential,amplitude):
    values,vectors=np.linalg.eigh(potential)
    return (vectors/np.expm1(frequency-amplitude*values))@vectors.conj().T

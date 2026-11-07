from kinetic_common import *
import reduced_amplitude as reduced
import itertools


def tensor_batch(energy,soft,hard_direction,soft_direction):
    soft=np.asarray(soft,dtype=float)
    angle01=1-hard_direction[2]
    angle02=1-soft_direction[2]
    angle12=1-hard_direction@soft_direction
    denominator=1+energy*angle01-soft*angle12
    hard=(energy-soft-energy*soft*angle02)/denominator
    if np.any(hard<=0) or np.any(denominator<=0):
        raise ValueError('Unphysical real batch')
    count=len(soft)
    photons=np.empty((count,3,4))
    photons[:,0]=np.array([energy,0,0,energy])
    photons[:,1]=hard[:,None]*np.r_[1.,hard_direction]
    photons[:,2]=soft[:,None]*np.r_[1.,soft_direction]
    recoil=photons[:,0,1:]-photons[:,1,1:]-photons[:,2,1:]
    final=np.column_stack([np.sqrt(1+np.sum(recoil**2,axis=1)),recoil])
    frames=np.array([reduced.frame(np.array([0.,0.,1.])),reduced.frame(hard_direction),reduced.frame(soft_direction)])
    vertices=np.array([[reduced.slash(polarization) for polarization in frame] for frame in frames])
    transfers=photons*np.array([1,-1,-1])[None,:,None]
    slashes=np.einsum('nla,aij->nlij',transfers*np.array([1,-1,-1,-1]),reduced.GAMMA)
    initial_states=reduced.spinors(np.array([1.,0,0,0]))
    pauli=np.einsum('na,aij->nij',recoil,reduced.PAULI[[2,3,1]])
    final_states=np.concatenate([np.broadcast_to(np.eye(2),(count,2,2)),pauli/(final[:,0,None,None]+1)],axis=1)
    final_states*=np.sqrt(final[:,0,None,None]+1)
    final_left=final_states.conj().transpose(0,2,1)@reduced.GAMMA[0]
    left,right=[],[]
    for leg in range(3):
        right.append((slashes[:,leg,None]@vertices[leg][None]@initial_states)/(2*transfers[:,leg,0,None,None,None]))
        dot_pol=final@((frames[leg]*np.array([1,-1,-1,-1])).T)
        dot_transfer=np.sum(final*transfers[:,leg]*np.array([1,-1,-1,-1]),axis=1)
        numerator=2*dot_pol[:,:,None,None]*reduced.IDENTITY-vertices[leg][None]@slashes[:,leg,None]
        left.append((final_left[:,None]@numerator)/(-2*dot_transfer[:,None,None,None]))
    result=np.zeros((count,2,2,2,2,2),complex)
    for first,middle,last in itertools.permutations(range(3)):
        term=np.einsum('nafd,bde,ncei->nabcfi',left[last],vertices[middle],right[first])
        ordering=[last,middle,first]
        result+=term.transpose([0]+[ordering.index(leg)+1 for leg in range(3)]+[4,5])
    return result,photons,final,hard,denominator


def intensity_batch(energy,soft,hard_direction,soft_direction):
    amplitudes,photons,final,hard,denominator=tensor_batch(energy,soft,hard_direction,soft_direction)
    return np.sum(abs(amplitudes)**2,axis=(1,2,3,4,5))/4,photons,final,hard,denominator

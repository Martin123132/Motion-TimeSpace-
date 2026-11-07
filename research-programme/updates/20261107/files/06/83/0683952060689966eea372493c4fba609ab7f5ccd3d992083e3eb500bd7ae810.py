import itertools
from polarized_thermal_common import *
import dirac_amplitude as exact


GAMMA=np.array([np.array(matrix.tolist(),dtype=complex) for matrix in exact.gamma_matrices()])
IDENTITY=np.eye(4,dtype=complex)
PAULI=np.array([np.eye(2),[[1,0],[0,-1]],[[0,1],[1,0]],[[0,-1j],[1j,0]]],dtype=complex)


def dot(left,right):
    return left[0]*right[0]-np.dot(left[1:],right[1:])


def slash(vector):
    return np.einsum('a,aij->ij',vector*np.array([1,-1,-1,-1]),GAMMA)


def frame(direction):
    reference=np.array([0.,0.,1.]) if abs(direction[2])<.8 else np.array([1.,0.,0.])
    first=np.cross(direction,reference)
    first/=np.linalg.norm(first)
    second=np.cross(direction,first)
    return np.column_stack([np.zeros(2),np.array([first,second])])


def spinors(momentum):
    energy,first,second,third=momentum
    pauli=np.array([[third,first-1j*second],[first+1j*second,-third]],dtype=complex)
    return np.vstack([np.eye(2),pauli/(energy+1)])*math.sqrt(energy+1)


def event(energy,signed_soft,hard_direction,soft_direction):
    incoming_direction=np.array([0.,0.,1.])
    angles=[1-np.dot(left,right) for left,right in [(incoming_direction,hard_direction),
                                                   (incoming_direction,soft_direction),(hard_direction,soft_direction)]]
    denominator=1+energy*angles[0]-signed_soft*angles[2]
    hard=(energy-signed_soft-energy*signed_soft*angles[1])/denominator
    if hard<=0 or denominator<=0:
        raise ValueError('Unphysical crossed real event')
    photons=np.array([np.r_[value,value*direction] for value,direction in
                      [(energy,incoming_direction),(hard,hard_direction),(signed_soft,soft_direction)]])
    initial=np.array([1.,0.,0.,0.])
    final=initial+photons[0]-photons[1]-photons[2]
    final[0]=math.sqrt(1+np.dot(final[1:],final[1:]))
    return dict(initial=initial,final=final,photons=photons,hard=hard,denominator=denominator,angles=angles,
                frames=np.array([frame(direction) for direction in [incoming_direction,hard_direction,soft_direction]]))


def tensor(sample,ward=None,omit=None):
    initial,final=sample['initial'],sample['final']
    transfers=sample['photons']*np.array([1,-1,-1])[:,None]
    frames=sample['frames'].copy()
    if ward is not None:
        frames[ward]=sample['photons'][ward]/sample['photons'][ward][0]
    vertices=np.array([[slash(polarization) for polarization in basis] for basis in frames])
    transfer_slash=np.array([slash(momentum) for momentum in transfers])
    initial_states=spinors(initial)
    final_states=spinors(final).conj().T@GAMMA[0]
    left,right=[],[]
    for leg in range(3):
        right.append(np.array([(2*dot(initial,frames[leg,state])*IDENTITY+transfer_slash[leg]@vertices[leg,state])
                               @initial_states/(2*dot(initial,transfers[leg])) for state in range(2)]))
        left.append(np.array([final_states@(2*dot(final,frames[leg,state])*IDENTITY-vertices[leg,state]@transfer_slash[leg])
                              /(-2*dot(final,transfers[leg])) for state in range(2)]))
    result=np.zeros((2,2,2,2,2),dtype=complex)
    for first,middle,last in itertools.permutations(range(3)):
        if (first,middle,last)==omit:
            continue
        term=np.einsum('afd,bde,cei->abcfi',left[last],vertices[middle],right[first])
        ordering=[last,middle,first]
        result+=term.transpose([ordering.index(leg) for leg in range(3)]+[3,4])
    return result


def mueller(tensor):
    if tensor.ndim==5:
        kraus=tensor.transpose(2,3,4,1,0).reshape(8,2,2)
    else:
        kraus=tensor.transpose(2,3,1,0).reshape(4,2,2)
    matrix=np.einsum('uab,kbc,vcd,kad->uv',PAULI,kraus,PAULI,kraus.conj())/4
    if np.max(abs(matrix.imag))>1e-10*max(np.max(abs(matrix.real)),1):
        raise ArithmeticError('Hermitian polarization map acquired an imaginary Mueller entry')
    return matrix.real


def interference(tree,correction):
    bare=tree.transpose(2,3,1,0).reshape(4,2,2)
    changed=correction.transpose(2,3,1,0).reshape(4,2,2)
    return np.einsum('uab,kbc,vcd,kad->uv',PAULI,changed,PAULI,bare.conj()).real/2

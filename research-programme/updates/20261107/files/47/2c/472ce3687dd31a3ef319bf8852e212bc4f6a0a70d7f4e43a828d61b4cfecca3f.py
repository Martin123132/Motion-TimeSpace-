from moving_frame import *
import thermal_dressed as dressed
import thermal_event_source as previous
from emission_rates import ALPHA


def angular_nodes(order):
    cosines,weights=np.polynomial.legendre.leggauss(order)
    for cosine,weight in zip(cosines,weights):
        for index in range(2*order):
            azimuth=np.pi*(index+.5)/order
            yield np.array([math.sqrt(1-cosine**2)*math.cos(azimuth),math.sqrt(1-cosine**2)*math.sin(azimuth),cosine]),weight*np.pi/order


def tree_map(parameters):
    exact.mp.mp.dps=60
    direction=exact.mp.matrix([exact.mp.sqrt(1-exact.mp.mpf(str(parameters['cosine']))**2),0,exact.mp.mpf(str(parameters['cosine']))])
    tree,final=exact.single_tensor(exact.mp.mpf(str(parameters['energy'])),direction)
    response=mueller(tree)
    return tree,response,response/response[0,0]


def virtual_map(parameters,order):
    exact.mp.mp.dps=60
    energy=exact.mp.mpf(str(parameters['energy']))
    cosine=exact.mp.mpf(str(parameters['cosine']))
    temperature=exact.mp.mpf(str(parameters['temperature']))
    initial=exact.mp.matrix([1,0,0,0])
    incoming=exact.photon(energy,exact.mp.matrix([0,0,1]))
    hard_direction=exact.mp.matrix([exact.mp.sqrt(1-cosine**2),0,cosine])
    outgoing=exact.photon(energy/(1+energy*(1-cosine)),hard_direction)
    bath=exact.mp.matrix([exact.mp.mpf(str(value)) for value in parameters['bath']])
    frames=[exact.frame(exact.mp.matrix([0,0,1])),exact.frame(hard_direction)]
    tensors=[[exact.mp.zeros(2) for second in range(2)] for first in range(2)]
    for direction,measure in angular_nodes(order):
        direction=exact.unit(direction)
        local_temperature=temperature/exact.dot(bath,exact.photon(exact.mp.mpf(1),direction))
        for first,second in itertools.product([0,1],repeat=2):
            tensors[first][second]+=exact.mp.mpf(float(measure))*dressed.finite_dressed(initial,incoming,outgoing,
                                      frames[0][first],frames[1][second],direction,local_temperature)
    prefactor=4*exact.mp.pi*exact.mp.mpf(str(ALPHA))/(2*(2*exact.mp.pi)**3)
    array=np.array([[[[complex(prefactor*tensors[first][second][final_spin,initial_spin]) for initial_spin in range(2)]
                      for final_spin in range(2)] for second in range(2)] for first in range(2)])
    tree,tree_mueller,normalized=tree_map(parameters)
    return array,interference(tree,array)/tree_mueller[0,0]


def moment_vector(sample,energy,signed_soft):
    angles=sample['angles']
    energy_transfer=-(energy**2*angles[0]+signed_soft**2*angles[2]
                      +energy*signed_soft*(angles[1]-angles[0]-angles[2]))/sample['denominator']
    photons=sample['photons'][1]+sample['photons'][2]-sample['photons'][0]
    photons[0]=energy_transfer
    spatial=-photons[1:]
    squared=spatial@spatial
    electron=np.r_[squared/(math.sqrt(1+squared)+1),spatial]
    return np.r_[1.,photons,electron]


def real_map(parameters,signed_soft,direction,tree_intensity):
    energy=parameters['energy']
    sample=event(energy,signed_soft,parameters['hard_direction'],direction)
    response=mueller(tensor(sample))
    ratio=parameters['hard']/energy
    coefficient=ALPHA/(4*np.pi**2)*sample['hard']*signed_soft/(energy*sample['denominator']*ratio**2*tree_intensity)
    bath_energy=sample['hard']*parameters['hard_doppler']
    enhancement=(1+1/np.expm1(bath_energy/parameters['temperature']))/parameters['hard_bose']
    return coefficient*response,enhancement,moment_vector(sample,energy,signed_soft)


def real_moments(parameters,angular_order,radial_order,profile_ratio=None):
    energy,cosine,temperature=parameters['energy'],parameters['cosine'],parameters['temperature']
    tree,tree_mueller,normalized=tree_map(parameters)
    hard_direction=parameters['hard_direction']
    recoil=np.array([0.,0.,energy])-parameters['hard']*hard_direction
    final_energy=math.sqrt(1+recoil@recoil)
    born=np.r_[1.,-recoil@recoil/(final_energy+1),-recoil,recoil@recoil/(final_energy+1),recoil]
    total=np.zeros((9,4,4))
    conversion=np.zeros((9,4,4))
    profile_integral=0. if profile_ratio is None else float(previous.profile_conversion(
        previous.mp.mpf(1),previous.mp.mpf(1),previous.mp.mpf(str(profile_ratio))))
    nodes,weights=np.polynomial.legendre.leggauss(radial_order)
    def interval(left,right):
        return zip((left+right)/2+(right-left)*nodes/2,(right-left)*weights/2)
    for direction,angular_weight in angular_nodes(angular_order):
        soft_doppler=dot(parameters['bath'],np.r_[1.,direction])
        upper=bath_ordered_upper(parameters,direction)
        local_temperature=temperature/soft_doppler
        upper_absorption=max(60*local_temperature,2*upper)
        pole=ALPHA/(4*np.pi**2)*(np.cross(recoil,direction)@np.cross(recoil,direction))/(final_energy-recoil@direction)**2
        base=pole*born[:,None,None]*normalized
        profile_scale=None if profile_ratio is None else profile_ratio*local_temperature
        for soft,measure in interval(0,upper):
            positive,positive_bose,positive_weight=real_map(parameters,soft,direction,tree_mueller[0,0])
            negative,negative_bose,negative_weight=real_map(parameters,-soft,direction,tree_mueller[0,0])
            profile=1. if profile_scale is None else math.exp(-(soft/profile_scale)**2)
            positive_moment=positive_weight[:,None,None]*positive
            negative_moment=negative_weight[:,None,None]*negative
            paired=(positive_bose*positive_moment-negative_bose*negative_moment-2/soft*base*profile)/np.expm1(soft/local_temperature)
            total+=angular_weight*measure*(paired+(positive_bose-1)*positive_moment)
        boundaries=[upper]+[value*local_temperature for value in [1,2,5,10,20,40] if upper<value*local_temperature<upper_absorption]+[upper_absorption]
        for left,right in zip(boundaries[:-1],boundaries[1:]):
            for soft,measure in interval(left,right):
                negative,negative_bose,negative_weight=real_map(parameters,-soft,direction,tree_mueller[0,0])
                profile=1. if profile_scale is None else math.exp(-(soft/profile_scale)**2)
                total+=angular_weight*measure*(-negative_bose*negative_weight[:,None,None]*negative-2/soft*base*profile)/np.expm1(soft/local_temperature)
        if profile_scale is not None:
            conversion+=angular_weight*profile_integral*base
    return total,conversion,born,normalized


def matched_moments(parameters,virtual,angular_order,radial_order,profile_ratio=None):
    real,conversion,born,normalized=real_moments(parameters,angular_order,radial_order,profile_ratio)
    response=previous.phase_response(previous.mp.mpf(str(parameters['energy'])),previous.mp.mpf(str(parameters['cosine'])),
                                     previous.mp.mpf(str(parameters['temperature'])))
    hard_bose_delta=-(parameters['hard_bose']-1)*parameters['hard_doppler']*float(response['hard_delta'])/parameters['temperature']
    rate=virtual+(float(response['phase_delta'])+hard_bose_delta)*normalized
    shifted=np.array([0,*[float(value) for value in response['photon_delta']],*[float(value) for value in response['electron_delta']]])
    rest=real+conversion+born[:,None,None]*rate+shifted[:,None,None]*normalized
    return rest,lab_moments(rest,parameters),dict(real=real,profile_conversion=conversion,born=born,
                                               normalized_tree=normalized,hard_bose_delta=hard_bose_delta)


def born_lab_source(lab_energy,lab_cosine,velocity,temperature,mass=1.):
    parameters=context(lab_energy/mass,lab_cosine,velocity,temperature/mass)
    tree,response,normalized=tree_map(parameters)
    recoil=np.array([0.,0.,parameters['energy']])-parameters['hard']*parameters['hard_direction']
    recoil_energy=recoil@recoil/(math.sqrt(1+recoil@recoil)+1)
    born=np.r_[1.,-recoil_energy,-recoil,recoil_energy,recoil]
    born[1:]*=mass
    return parameters['born_differential_over_thomson']/mass**2*lab_moments(born[:,None,None]*normalized,parameters)


def canonical_momentum_correction(parameters,step=1e-3):
    velocity=parameters['velocity']
    if not np.any(velocity):
        return np.zeros((9,4,4))
    gamma_squared=1/(1-velocity@velocity)
    velocity_derivative=-velocity/(2*gamma_squared)
    delta_mass_squared=2*np.pi*ALPHA*parameters['temperature']**2/3
    def evaluate(offset):
        return born_lab_source(parameters['lab_energy'],parameters['lab_cosine'],
                               velocity+offset*velocity_derivative,parameters['temperature'])
    derivative=(-evaluate(2*step)+8*evaluate(step)-8*evaluate(-step)+evaluate(-2*step))/(12*step)
    return delta_mass_squared*derivative/parameters['born_differential_over_thomson']

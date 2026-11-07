import mpmath as mp
from thermal_source_common import *
import ordered_real_kernel as real
import source_four_force as forces
from emission_rates import ALPHA


def occupation(energy,temperature):
    return 1/mp.expm1(energy/temperature)


def dressed_phase(energy,cosine,mass_squared_shift):
    mass=mp.sqrt(1+mass_squared_shift)
    hard=energy/(1+energy*(1-cosine)/mass)
    spatial_squared=energy**2+hard**2-2*energy*hard*cosine
    bare_final=mp.sqrt(1+spatial_squared)
    dressed_final=mp.sqrt(1+mass_squared_shift+spatial_squared)
    velocity_projection=(energy*cosine-hard)/dressed_final
    measure=hard/(bare_final*(1-velocity_projection))
    return measure,hard,dressed_final-mass


def phase_response(energy,cosine,temperature):
    hard=energy/(1+energy*(1-cosine))
    final=1+energy-hard
    projection=(energy*cosine-hard)/final
    mass_squared=2*mp.pi*mp.mpf(str(ALPHA))*temperature**2/3
    hard_delta=mass_squared/2*(1-1/final)/(1-projection)
    final_bare_delta=-hard_delta*projection
    velocity_delta=-hard_delta/final-projection*final_bare_delta/final-projection*mass_squared/(2*final**2)
    phase_delta=hard_delta/hard-final_bare_delta/final+velocity_delta/(1-projection)
    bose_delta=-occupation(hard,temperature)*hard_delta/temperature
    photon_delta=mp.matrix([hard_delta,hard_delta*mp.sqrt(1-cosine**2),0,hard_delta*cosine])
    electron_energy_delta=final_bare_delta+mass_squared/(2*final)-mass_squared/2
    electron_delta=mp.matrix([electron_energy_delta,-photon_delta[1],0,-photon_delta[3]])
    return dict(mass_squared=mass_squared,hard_delta=hard_delta,phase_delta=phase_delta,
                bose_delta=bose_delta,photon_delta=photon_delta,electron_delta=electron_delta)


def weight_vector(energy,hard,signed_soft,cosine,soft_cosine,azimuth):
    photons,electron,soft,hard_transfer=forces.four_transfers(energy,hard,signed_soft,cosine,soft_cosine,azimuth)
    return mp.matrix([1,*photons,*electron])


def signed_event(energy,signed_soft,cosine,soft_cosine,azimuth,temperature):
    values=real.geometry(energy,cosine,soft_cosine,azimuth)
    squared,hard,denominator=real.amplitude_squared(energy,signed_soft,*values[1:])
    born=energy/(1+energy*(1-cosine))
    hard_bose=(1+occupation(hard,temperature))/(1+occupation(born,temperature))
    density=real.real_density(energy,signed_soft,*values[1:])
    return density,hard_bose,weight_vector(energy,hard,signed_soft,cosine,soft_cosine,azimuth)


def gauss_interval(count,lower,upper):
    nodes,weights=np.polynomial.legendre.leggauss(count)
    for node,weight in zip(nodes,weights):
        yield (lower+upper)/2+(upper-lower)*mp.mpf(float(node))/2,(upper-lower)*mp.mpf(float(weight))/2


def matching_profile(energy,scale):
    return mp.mpf(1) if scale is None else mp.exp(-(energy/scale)**2)


def real_thermal_source(energy,cosine,temperature,angular_order,radial_order,cutoff_factor=60,profile_scale=None,lower_fraction=0):
    energy,cosine,temperature=map(mp.mpf,[energy,cosine,temperature])
    upper_absorption=cutoff_factor*temperature
    lower=mp.mpf(lower_fraction)*temperature
    born_energy=energy/(1+energy*(1-cosine))
    born=weight_vector(energy,born_energy,mp.mpf(0),cosine,mp.mpf(0),mp.mpf(0))
    paired,tail,hard_stimulation=mp.zeros(9,1),mp.zeros(9,1),mp.zeros(9,1)
    pole_total=mp.mpf(0)
    for soft_cosine,azimuth,angular_weight in real.angular_nodes(angular_order):
        geometry=real.geometry(energy,cosine,soft_cosine,azimuth)
        upper=real.ordered_upper(*geometry)
        assert lower<upper<upper_absorption
        pole=real.pole_density(*geometry)
        pole_total+=angular_weight*pole
        for soft,measure in gauss_interval(radial_order,lower,upper):
            emission,bose_emission,emission_weight=signed_event(energy,soft,cosine,soft_cosine,azimuth,temperature)
            crossed,bose_absorption,absorption_weight=signed_event(energy,-soft,cosine,soft_cosine,azimuth,temperature)
            subtraction=2*pole/soft*born*matching_profile(soft,profile_scale)
            paired+=angular_weight*measure*occupation(soft,temperature)*(emission*bose_emission*emission_weight-crossed*bose_absorption*absorption_weight-subtraction)
        for soft,measure in gauss_interval(radial_order,mp.mpf(0),upper):
            emission,bose_emission,emission_weight=signed_event(energy,soft,cosine,soft_cosine,azimuth,temperature)
            hard_stimulation+=angular_weight*measure*emission*(bose_emission-1)*emission_weight
        partitions=[upper]
        partitions.extend(value*temperature for value in [1,2,5,10,20,40] if upper<value*temperature<upper_absorption)
        partitions.append(upper_absorption)
        for left,right in zip(partitions[:-1],partitions[1:]):
            for soft,measure in gauss_interval(radial_order,left,right):
                crossed,bose_absorption,absorption_weight=signed_event(energy,-soft,cosine,soft_cosine,azimuth,temperature)
                subtraction=2*pole/soft*born*matching_profile(soft,profile_scale)
                tail+=angular_weight*measure*occupation(soft,temperature)*(-crossed*bose_absorption*absorption_weight-subtraction)
    total=paired+tail+hard_stimulation
    return dict(total=total,paired=paired,absorption_tail=tail,hard_stimulation=hard_stimulation,
                integrated_pole=pole_total,born=born)


def profile_conversion(pole,temperature,scale):
    if scale is None:
        return mp.mpf(0)
    return -2*pole*mp.quad(lambda energy:occupation(energy,temperature)*(-mp.expm1(-(energy/scale)**2))/energy,
                           [0,scale,temperature,mp.inf] if scale<temperature else [0,temperature,scale,mp.inf])


def matched_event_source(energy,cosine,temperature,angular_order,radial_order,virtual_interference,
                         cutoff_factor=60,profile_scale=None,lower_fraction=0):
    response=phase_response(energy,cosine,temperature)
    pieces=real_thermal_source(energy,cosine,temperature,angular_order,radial_order,cutoff_factor,profile_scale,lower_fraction)
    conversion=profile_conversion(pieces['integrated_pole'],temperature,profile_scale)
    virtual=mp.mpf(virtual_interference)+response['phase_delta']+response['bose_delta']+conversion
    shifted=mp.matrix([0,*response['photon_delta'],*response['electron_delta']])
    total=pieces['total']+virtual*pieces['born']+shifted
    return dict(total=total,virtual=virtual,profile_conversion=conversion,response=response,pieces=pieces)

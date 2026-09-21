from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_compensated_momentum_rate_20260919 import compensated_acceleration,inverse_residual
from annular_wave_error_energy_20260919 import stiffness_weights,stiffness_terms,source_kinetic_force
from annular_P2_weighted_projection_bounds_20260919 import band_action
from scipy.linalg import solve_banded,cho_solve
import numpy as np


def forced_linear_step(frequency,position,velocity,first_force,last_force,step):
    angle = frequency*step
    sine_over_frequency = step*np.sinc(angle/np.pi)
    second = .5*step**2*np.sinc(angle/(2*np.pi))**2
    small = abs(angle) < 1e-3
    third_factor = np.empty_like(angle)
    third_factor[small] = 1/6-angle[small]**2/120+angle[small]**4/5040
    third_factor[~small] = (1-np.sinc(angle[~small]/np.pi))/angle[~small]**2
    third = step**3*third_factor
    slope = (last_force-first_force)/step
    cosine = np.cos(angle)
    return (cosine*position+sine_over_frequency*velocity+second*first_force+third*slope,
        -frequency*np.sin(angle)*position+cosine*velocity+sine_over_frequency*first_force+second*slope)


def live_item(system,state,center):
    rates,geometry = system.solve(*state)
    layer = system.layer(system.labels[center],geometry)
    values = state[0,center]
    data = layer.evaluate(0.,values,rates[center])
    return dict(layer=layer,data=data,values=values,rates=rates[center],all_rates=rates,geometry=geometry,
        weights=stiffness_weights(layer,values[-1]),
        inverse_residual=inverse_residual(data,rates[center],state[1,center,:-1]))


def live_acceleration(system,state,center,base,step):
    flow = base['flow']
    before = live_item(system,state-step*flow,center)
    after = live_item(system,state+step*flow,center)
    mass_rate = (after['data']['mass_bands']-before['data']['mass_bands'])/(2*step)
    cross_rate = (after['data']['cross']-before['data']['cross'])/(2*step)
    residual_rate = (after['inverse_residual']-before['inverse_residual'])/(2*step)
    direct = (after['rates']-before['rates'])/(2*step)
    result = compensated_acceleration(base['data'],base['rates'],flow[1,center,:-1],mass_rate,cross_rate,
        direct[-1],residual_rate)
    return dict(**result,mass_rate=mass_rate,cross_rate=cross_rate,inverse_residual_rate=residual_rate,
        source_acceleration=direct[-1],direct_acceleration=direct[:-1])


def moving_forcing(base,acceleration,frozen_mass_lower,frozen_stiffness):
    values = base['values'][:-1]
    frozen_load = frozen_stiffness @ values
    frozen_acceleration_operator = cho_solve((frozen_mass_lower,True),frozen_load,check_finite=False)
    action_load = stiffness_terms(base['layer'],base['weights'],values)['load']
    kinetic = source_kinetic_force(base['layer'],base['values'],base['rates'],base['data'])
    force = base['flow'][1,base['center'],:-1]
    loads = dict(geometry_stiffness_drift=band_action(base['data']['mass_bands'],frozen_acceleration_operator)-action_load,
        source_kinetic=kinetic,canonical_action_reconstruction_defect=force+action_load-kinetic,
        cross_transport=-acceleration['cross_rate']*base['rates'][-1],
        source_acceleration=-base['data']['cross']*acceleration['source_acceleration'],
        mass_transport=-band_action(acceleration['mass_rate'],base['rates'][:-1]),
        inverse_residual=-acceleration['inverse_residual_rate'])
    names = list(loads)
    solved = solve_banded((2,2),base['data']['mass_bands'],np.column_stack(list(loads.values())),check_finite=False)
    return dict(forcing=sum(solved.T),direct=acceleration['acceleration']+frozen_acceleration_operator,
        channels=dict(zip(names,solved.T)))


def fixed_basis_remainder(mass,stiffness,mass_rate,stiffness_rate,reference_mass,reference_stiffness,
                          displacement,velocity,acceleration,residual_rate):
    current_rhs = residual_rate-stiffness_rate @ displacement-mass_rate @ acceleration-stiffness @ velocity
    jerk = np.linalg.solve(mass,current_rhs)
    frozen_rhs = reference_mass @ jerk+reference_stiffness @ velocity
    return frozen_rhs,jerk

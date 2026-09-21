import numpy as np

from annular_constrained_mass_relative_energy_20260914 import uniform_constants, quadrature, density_energy
from annular_reference_wave_decoupling_20260914 import reference_acceleration


def locking_constants():
    values = uniform_constants()
    radius,ceiling = values['radius_lower'],values['radius_upper']
    floor,mass,energy = values['chosen_F_floor'],values['actual_mass_ceiling'],values['energy_ceiling']
    lower,upper = values['weight_lower'],values['outer_clock_upper']
    coupling,source = values['coupling'],values['reservoir_L1']
    length = ceiling-radius
    a_min,a_max = lower/ceiling**2,upper/radius**2
    c_min,c_max = radius**2*lower,ceiling**2*upper
    spatial_log = 2/radius+2*mass/(radius**2*floor)
    mass_rate_multiplier = 2*coupling*np.sqrt(energy)
    time_log = mass_rate_multiplier*(2/(radius*floor)+2*length/(radius**2*floor**2)+
                                    coupling*source/(radius**2*floor**1.5))
    time_log_gradient = 2*mass_rate_multiplier/(radius**2*floor**2)
    delta_a = a_max*spatial_log/2
    delta_c = c_max*spatial_log/2
    delta_b = time_log_gradient/2
    delta_d = (time_log_gradient+2*time_log*spatial_log)/2
    forcing_v = 4*(delta_a**2*ceiling**2/a_min+delta_c**2/(radius**2*c_min))
    forcing_vsquare = 4*(delta_b**2/(radius**2*a_min)+delta_d**2*ceiling**2/c_min)
    forcing_a = 32*c_max**2*ceiling**2/c_min**3
    forcing_boundary_vsquare = time_log**2*(forcing_a+16*ceiling**2/c_min)
    return dict(values,a_min=a_min,a_max=a_max,c_min=c_min,c_max=c_max,
                spatial_log_bound=spatial_log,mass_rate_multiplier=mass_rate_multiplier,
                time_log_multiplier=time_log,time_log_gradient_multiplier=time_log_gradient,
                delta_a_multiplier=delta_a,delta_c_multiplier=delta_c,
                delta_b_multiplier=delta_b,delta_d_multiplier=delta_d,
                forcing_h2_EV=forcing_v,forcing_h2_EV2=forcing_vsquare,
                forcing_h_EA=forcing_a,forcing_h_EV2=forcing_boundary_vsquare)


def pair_diagnostics(system,time,state,order=12):
    constants = locking_constants()
    offsets,weights = quadrature(order)
    velocity,acceleration = reference_acceleration(system,time,state)
    geometry = system.geometry(time,state)
    data = geometry.layer(offsets)
    moved = system.geometry(time,state+1j*1e-20*velocity).layer(offsets)
    coefficient = data['N']*data['U']/data['R']**2
    coefficient_rate = (moved['N']*moved['U']/moved['R']**2).imag/1e-20
    kinetic = coefficient[:,:-1]
    log_kinetic_rate = coefficient_rate[:,:-1]/kinetic
    edge = (data['C'][:,:-1]+data['C'][:,1:])/2
    edge_rate = (moved['C'][:,:-1]+moved['C'][:,1:]).imag/(2e-20)
    log_edge_rate = edge_rate/edge
    gradient = np.diff(data['chi'],axis=1)/system.spacing
    force = edge*gradient
    wave_velocity = data['q'][:,:-1]
    momentum_rate = np.diff(np.column_stack([np.zeros(len(offsets)),force]),axis=1)/system.node_weights[:-1]
    velocity_gradient = np.diff(data['q'],axis=1)/system.spacing
    velocity_rate = kinetic*momentum_rate+log_kinetic_rate*wave_velocity
    force_rate = edge*velocity_gradient+log_edge_rate*force
    difference_q = wave_velocity[:,None,:]-wave_velocity[None,:,:]
    difference_force = force[:,None,:]-force[None,:,:]
    difference_a = kinetic[:,None,:]-kinetic[None,:,:]
    difference_c = edge[:,None,:]-edge[None,:,:]
    difference_b = log_kinetic_rate[:,None,:]-log_kinetic_rate[None,:,:]
    difference_d = log_edge_rate[:,None,:]-log_edge_rate[None,:,:]
    residual_q = difference_a*momentum_rate[None,:,:]+difference_b*wave_velocity[None,:,:]
    residual_force = difference_c*velocity_gradient[None,:,:]+difference_d*force[None,:,:]
    kinetic_measure = system.node_weights[None,None,:-1]/kinetic[:,None,:]
    edge_measure = system.spacing/edge[:,None,:]
    pair_weights = weights[:,None]*weights[None,:]
    def average(values):
        return float(np.sum(pair_weights*np.sum(values,axis=2)))
    pair_energy = .5*average(kinetic_measure*difference_q**2+edge_measure*difference_force**2)
    direct_rate = average(kinetic_measure*difference_q*(velocity_rate[:,None,:]-velocity_rate[None,:,:])+
                          edge_measure*difference_force*(force_rate[:,None,:]-force_rate[None,:,:])-
                          .5*kinetic_measure*log_kinetic_rate[:,None,:]*difference_q**2-
                          .5*edge_measure*log_edge_rate[:,None,:]*difference_force**2)
    metric_rate = .5*average(kinetic_measure*log_kinetic_rate[:,None,:]*difference_q**2+
                              edge_measure*log_edge_rate[:,None,:]*difference_force**2)
    forcing_pairing = average(kinetic_measure*difference_q*residual_q+
                              edge_measure*difference_force*residual_force)
    forcing_square = average(kinetic_measure*residual_q**2+edge_measure*residual_force**2)
    forcing_bulk = float(np.sum(pair_weights*np.sum((edge_measure*residual_force**2)[:,:,:-1],axis=2)))
    forcing_boundary = float(np.sum(pair_weights*(edge_measure*residual_force**2)[:,:,-1]))
    energy_v = float(density_energy(system,velocity))
    energy_a = float(density_energy(system,acceleration))
    step = system.spacing
    analytic_forcing = step**2*(constants['forcing_h2_EV']*energy_v+constants['forcing_h2_EV2']*energy_v**2)
    analytic_forcing += step*(constants['forcing_h_EA']*energy_a+constants['forcing_h_EV2']*energy_v**2)
    phase_variance = average(system.node_weights[None,None,:-1]*
                               (data['p'][:,:-1,None].transpose(0,2,1)-data['p'][None,:,:-1])**2+
                            step*(gradient[:,None,:]-gradient[None,:,:])**2)
    mean_q = weights @ wave_velocity
    direct_q_variance = float(weights @ np.sum(system.node_weights[:-1]*(wave_velocity-mean_q)**2,axis=1))
    pair_q_variance = average(system.node_weights[None,None,:-1]*difference_q**2)/2
    raw = dict(weights=weights,kinetic=kinetic,edge=edge,b=log_kinetic_rate,d=log_edge_rate,
               q=wave_velocity,force=force,q_rate=velocity_rate,force_rate=force_rate,
               residual_q=residual_q,residual_force=residual_force,gradient=gradient)
    result = dict(count=len(system.radii),time=float(time),h=step,degree=system.grid.degree,
                  pair_energy=pair_energy,phase_variance=phase_variance,direct_rate=direct_rate,
                  metric_rate=metric_rate,forcing_pairing=forcing_pairing,
                  balance_error=abs(direct_rate-metric_rate-forcing_pairing),
                  forcing_square=forcing_square,analytic_forcing_square_bound=float(analytic_forcing),
                  force_bulk_residual_square=forcing_bulk,force_boundary_residual_square=forcing_boundary,
                  velocity_energy=energy_v,acceleration_energy=energy_a,
                  max_a_difference=float(abs(difference_a).max()),
                  max_bulk_c_difference=float(abs(difference_c[:,:,:-1]).max()),
                  max_source_c_difference=float(abs(difference_c[:,:,-1]).max()),
                  max_b_difference=float(abs(difference_b).max()),
                  max_bulk_d_difference=float(abs(difference_d[:,:,:-1]).max()),
                  max_log_rate=float(max(abs(log_kinetic_rate).max(),abs(log_edge_rate).max())),
                  variance_identity_error=abs(direct_q_variance-pair_q_variance),
                  omitted_live_coefficients_error=abs(direct_rate-forcing_pairing))
    return result,raw


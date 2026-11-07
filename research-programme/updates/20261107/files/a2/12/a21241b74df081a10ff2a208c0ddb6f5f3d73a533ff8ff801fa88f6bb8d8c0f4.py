from annular_C0_boundary_integral_20260930 import quadratic
from annular_C0_decimal_transport_20260930 import precise_exp,precise_sqrt
from annular_weighted_current_polynomial_20261001 import weighted_polynomial
import numpy as np


def metric_data(radius,values,radial,time,precise=False):
    geometry = 1-2*values[0]/radius
    geometry_r = -2*radial[0]/radius+2*values[0]/radius**2
    lapse = precise_exp(values[1]) if precise else np.exp(values[1])
    root = precise_sqrt(geometry) if precise else np.sqrt(geometry)
    alpha,beta = radius**2/(lapse*root),radius**2*lapse*root
    alpha_r = alpha*(2/radius-radial[1]-geometry_r/(2*geometry))
    beta_r = beta*(2/radius+radial[1]+geometry_r/(2*geometry))
    clock_time = time[1]-time[0]/(radius*geometry)
    return dict(alpha=alpha,beta=beta,alpha_r=alpha_r,beta_r=beta_r,alpha_t=-alpha*clock_time,
        geometry=geometry,geometry_r=geometry_r,clock_time=clock_time)


def metric_derivative(radius,base,time,change,change_r,change_t):
    geometry = base['geometry']
    logarithm = change[1]-change[0]/(radius*geometry)
    logarithm_r = change_r[1]-change_r[0]/(radius*geometry)
    logarithm_r += change[0]*(geometry+radius*base['geometry_r'])/(radius*geometry)**2
    alpha,beta = -base['alpha']*logarithm,base['beta']*logarithm
    clock_change = change_t[1]-change_t[0]/(radius*geometry)-2*time[0]*change[0]/(radius**2*geometry**2)
    return dict(alpha=alpha,beta=beta,alpha_r=-base['alpha_r']*logarithm-base['alpha']*logarithm_r,
        beta_r=base['beta_r']*logarithm+base['beta']*logarithm_r,
        alpha_t=-alpha*base['clock_time']-base['alpha']*clock_change)


def kinematics(data,amount=0):
    local,width = data['local'],data['width']
    rate_coefficients = data['rate']+amount*data['field_change']
    rate,rate_r = quadratic(rate_coefficients,local,width)
    gradient = quadratic(data['field'],local,width)[1]
    acceleration = quadratic(data['acceleration']+amount*data['acceleration_change'],local,width)[0]
    displacement = data['displacement_left']+(data['displacement_right']-data['displacement_left'])*local
    speed = displacement*data['source_velocity']+amount*(data['movement_left']+(data['movement_right']-data['movement_left'])*local)
    speed_r = ((data['displacement_right']-data['displacement_left'])*data['source_velocity']
        +amount*(data['movement_right']-data['movement_left']))/width
    speed_time = displacement*(data['source_acceleration']+amount*data['source_acceleration_change'])
    temporal = rate-speed*gradient
    gradient_time = rate_r-speed_r*gradient
    temporal_time = acceleration-speed_time*gradient-speed*gradient_time
    return dict(rate=rate,rate_r=rate_r,rate_coefficients=rate_coefficients,gradient=gradient,
        acceleration=acceleration,speed=speed,speed_r=speed_r,speed_time=speed_time,
        temporal=temporal,gradient_time=gradient_time,temporal_time=temporal_time)


def current_values(data,radius,values,radial,time,change,change_r,change_t,amount=0,precise=False,original=False):
    coefficients = metric_data(radius,values+amount*change,radial+amount*change_r,time+amount*change_t,precise)
    state = kinematics(data,amount)
    alpha,beta,alpha_r,beta_r,alpha_t = [coefficients[key] for key in ['alpha','beta','alpha_r','beta_r','alpha_t']]
    rate,rate_r,gradient,speed,speed_r,temporal,gradient_time,temporal_time = [state[key] for key in
        ['rate','rate_r','gradient','speed','speed_r','temporal','gradient_time','temporal_time']]
    alpha_dot,beta_dot = alpha_t+speed*alpha_r,-beta*alpha_t/alpha+speed*beta_r
    momentum_rate = (alpha_dot+speed_r*alpha)*temporal+alpha*temporal_time
    flux = alpha*speed*temporal+beta*gradient
    energy = (alpha*temporal**2+beta*gradient**2)/2
    test,test_r = quadratic(data['test'],data['local'],data['width'])
    eta = data['eta_left']+(data['eta_right']-data['eta_left'])*data['local']
    eta_r = (data['eta_right']-data['eta_left'])/data['width']
    force = momentum_rate*(test-gradient*eta)+flux*test_r-alpha*temporal*gradient_time*eta
    force -= (alpha_r*temporal**2-beta_r*gradient**2)*eta/2+(energy+alpha*speed*temporal*gradient)*eta_r
    rows = [force]
    packet = dict(data,rate=state['rate_coefficients'])
    for power in range(3):
        if original:
            integral = ((radius-6)**(power+1)-(data['source']-6)**(power+1))/(power+1)
            nodes = []
            for fraction in [0.,.5,1.]:
                node_radius = data['node_left']+(data['node_right']-data['node_left'])*fraction
                node_rate = quadratic(state['rate_coefficients'],fraction,data['width'])[0]
                nodes.append(node_rate*((node_radius-6)**(power+1)-(data['source']-6)**(power+1))/(power+1))
            left,middle,right = nodes
            local = data['local']
            weighted = left*(1-local)*(1-2*local)+4*middle*local*(1-local)+right*local*(2*local-1)
            weighted_r = (left*(4*local-3)+middle*(4-8*local)+right*(4*local-1))/data['width']
            energy_time = (alpha_dot*temporal**2+beta_dot*gradient**2)/2
            energy_time += alpha*temporal*temporal_time+beta*gradient*gradient_time
            rows.append(-momentum_rate*weighted-flux*weighted_r+(energy_time+(speed_r+alpha_t/alpha)*energy)*integral+energy*speed*(radius-6)**power)
        else:
            integral,weighted_r,factor = weighted_polynomial(packet,radius,rate,speed,gradient,power)
            compact = speed*(beta_r*gradient**2-alpha_r*temporal**2)/2+beta*gradient*rate_r-speed_r*energy
            rows.append(momentum_rate*factor-flux*weighted_r+compact*integral+energy*speed*(radius-6)**power)
    return np.array(rows)


def analytic_response(data,radius,values,radial,time,change,change_r,change_t,precise=False):
    base = metric_data(radius,values,radial,time,precise)
    delta = metric_derivative(radius,base,time,change,change_r,change_t)
    state = kinematics(data)
    alpha,beta,alpha_r,beta_r,alpha_t = [base[key] for key in ['alpha','beta','alpha_r','beta_r','alpha_t']]
    da,db,da_r,db_r,da_t = [delta[key] for key in ['alpha','beta','alpha_r','beta_r','alpha_t']]
    rate,rate_r,gradient,speed,speed_r,temporal,gradient_time,temporal_time = [state[key] for key in
        ['rate','rate_r','gradient','speed','speed_r','temporal','gradient_time','temporal_time']]
    direction,direction_r = quadratic(data['field_change'],data['local'],data['width'])
    speed_change = data['movement_left']+(data['movement_right']-data['movement_left'])*data['local']
    speed_r_change = (data['movement_right']-data['movement_left'])/data['width']
    displacement = data['displacement_left']+(data['displacement_right']-data['displacement_left'])*data['local']
    acceleration_change = quadratic(data['acceleration_change'],data['local'],data['width'])[0]
    speed_time_change = displacement*data['source_acceleration_change']
    temporal_change = direction-speed_change*gradient
    gradient_time_change = direction_r-speed_r_change*gradient
    temporal_time_change = acceleration_change-speed_time_change*gradient-speed_change*gradient_time-speed*gradient_time_change
    logarithm = alpha_t+speed*alpha_r+speed_r*alpha
    logarithm_change = da_t+speed_change*alpha_r+speed*da_r+speed_r_change*alpha+speed_r*da
    momentum = logarithm*temporal+alpha*temporal_time
    momentum_change = logarithm_change*temporal+logarithm*temporal_change+da*temporal_time+alpha*temporal_time_change
    flux = alpha*speed*temporal+beta*gradient
    flux_change = da*speed*temporal+alpha*speed_change*temporal+alpha*speed*temporal_change+db*gradient
    energy = (alpha*temporal**2+beta*gradient**2)/2
    energy_change = (da*temporal**2+db*gradient**2)/2+alpha*temporal*temporal_change
    compact_change = speed_change*(beta_r*gradient**2-alpha_r*temporal**2)/2
    compact_change += speed*(db_r*gradient**2-da_r*temporal**2-2*alpha_r*temporal*temporal_change)/2
    compact_change += db*gradient*rate_r+beta*gradient*direction_r-speed_r_change*energy-speed_r*energy_change
    test,test_r = quadratic(data['test'],data['local'],data['width'])
    eta = data['eta_left']+(data['eta_right']-data['eta_left'])*data['local']
    eta_r = (data['eta_right']-data['eta_left'])/data['width']
    force = momentum_change*(test-gradient*eta)+flux_change*test_r
    force -= (da*temporal*gradient_time+alpha*temporal_change*gradient_time+alpha*temporal*gradient_time_change)*eta
    force -= (da_r*temporal**2+2*alpha_r*temporal*temporal_change-db_r*gradient**2)*eta/2
    force -= (energy_change+(da*speed*temporal+alpha*speed_change*temporal+alpha*speed*temporal_change)*gradient)*eta_r
    rows = [force]
    direction_packet = dict(data,rate=data['field_change'])
    for power in range(3):
        integral,weighted_r,factor = weighted_polynomial(data,radius,rate,speed,gradient,power)
        unused,weighted_r_change,factor_change = weighted_polynomial(direction_packet,radius,direction,speed_change,gradient,power)
        rows.append(momentum_change*factor+momentum*factor_change-flux_change*weighted_r-flux*weighted_r_change
            +compact_change*integral+(energy_change*speed+energy*speed_change)*(radius-6)**power)
    return np.array(rows)


def matter_gravity_response(radius,values,time_mass,change,change_time_mass,source_speed,speed_change,density,mass,coupling,precise=False):
    geometry = 1-2*values[0]/radius
    lapse = precise_exp(values[1]) if precise else np.exp(values[1])
    root = precise_sqrt(geometry) if precise else np.sqrt(geometry)
    clock_squared = lapse*lapse-source_speed**2/geometry
    clock = precise_sqrt(clock_squared) if precise else np.sqrt(clock_squared)
    coefficient = lapse/(coupling*root)
    loading = coupling*mass*density*root*lapse/clock
    logarithm = -change[0]/(radius*geometry)+change[1]
    logarithm -= (lapse*lapse*change[1]-source_speed*speed_change/geometry
        -source_speed**2*change[0]/(radius*geometry**2))/clock_squared
    loading_change = loading*logarithm
    remainder = time_mass+source_speed*loading
    return coefficient*(change_time_mass+speed_change*loading+source_speed*loading_change
        +(change[1]+change[0]/(radius*geometry))*remainder)

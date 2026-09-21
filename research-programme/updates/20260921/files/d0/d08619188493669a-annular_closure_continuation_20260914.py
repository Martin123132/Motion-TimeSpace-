import numpy as np

from annular_live_exterior_response_20260913 import LiveExteriorResponse, TimeFit


class PolynomialHistory:
    def __init__(self, times, states):
        self.duration = float(times[-1])
        self.fit = TimeFit(states,self.duration)

    def sol(self, time):
        if np.ndim(time)==0:
            return self.fit(time)
        return np.stack([self.fit(value) for value in time],axis=1)


def common_profiles(system, states, offsets):
    return np.stack([system.grid.evaluate(system.grid.coefficients(system.unpack(state)[0]),offsets) for state in states])


def trajectory_diagnostics(system, history, parameter, duration=.032):
    response = LiveExteriorResponse(system,duration)
    times = np.unique(np.concatenate([np.linspace(0.,duration,33),[.004,.008,.016,duration]]))
    offsets = np.linspace(-.5,.5,65)
    states = history.sol(times).T
    outputs = []
    mass_law_errors = []
    minimum_f = float('inf')
    minimum_n = float('inf')
    minimum_energy = float('inf')
    maximum_constraint_defect = 0.
    for index,(time,state) in enumerate(zip(times,states)):
        evaluation = system.evaluate_protocol(time,state,parameter)
        outputs.append(response.outputs(evaluation))
        geometry = evaluation['geometry']
        minimum_f = min(minimum_f,geometry.minimum_F)
        minimum_n = min(minimum_n,float(geometry.metric(geometry.edges)['N'].min()))
        minimum_energy = min(minimum_energy,float(geometry.scalar(offsets)['energy'].min()))
        maximum_constraint_defect = max(maximum_constraint_defect,geometry.collocation_defect)
        if index%4==0 or index==len(times)-1:
            step = 1e-20
            varied = system.evaluate_protocol(time+1j*step,state+1j*step*evaluation['rhs'],parameter)
            derivative = varied['geometry'].metric(system.radii)['mu'].imag/step
            mass_law_errors.append(float(abs(derivative-system.mass_flux(evaluation,system.radii)).max()))
    outputs = np.stack(outputs)
    points,weights = np.polynomial.legendre.leggauss(24)
    integrated = np.zeros(2)
    for time,weight in zip(duration*(points+1)/2,duration*weights/2):
        output = response.outputs(system.evaluate_protocol(time,history.sol(time),parameter))
        integrated += weight*output[[3,5]]
    initial_evaluation = system.evaluate_protocol(0.,system.initial_state,parameter)
    initial_n = initial_evaluation['geometry'].metric(np.array([system.radii[0]]))['N'][0]
    gamma = outputs[0,3]/initial_n
    affine_defect = outputs[:,1]-outputs[0,1]-gamma*states[:,-1]
    checkpoints = []
    for end in [.004,.008,.016,duration]:
        index = int(np.flatnonzero(times==end)[0])
        checkpoints.append({'time':end,'inner_mass_change':float(outputs[index,1]-outputs[0,1]),
                            'inner_affine_history_defect':float(affine_defect[index]),
                            'source_energy_change':float(outputs[index,4]-outputs[0,4]),
                            'inner_current':float(outputs[index,0])})
    diagnostics = {'duration':duration,'minimum_F_sampled':minimum_f,'minimum_N_sampled':minimum_n,
                   'minimum_source_energy_sampled':minimum_energy,'radial_constraint_defect':maximum_constraint_defect,
                   'live_mass_law_error':max(mass_law_errors),
                   'total_mass_drift':float(abs(outputs[:,6]-outputs[0,6]).max()),
                   'inner_mass_balance_error':float(abs(outputs[-1,1]-outputs[0,1]-integrated[0])),
                   'source_energy_balance_error':float(abs(outputs[-1,4]-outputs[0,4]-integrated[1])),
                   'initial_to_final_source_energy_fraction':float(outputs[-1,4]/outputs[0,4]),
                   'checkpoints':checkpoints}
    arrays = {'times':times,'states':states,'outputs':outputs,'offsets':offsets,
              'profiles':common_profiles(system,states,offsets),'inner_affine_defect':affine_defect,
              'initial_state':system.initial_state}
    return diagnostics,arrays


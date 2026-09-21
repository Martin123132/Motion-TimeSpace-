import numpy as np


def smooth_preparation(system):
    state=system.initial_state.copy()
    values=system.values(state)
    values[:,2*system.count+1]=-.00008*(1+.03*system.offsets)
    displacement=system.radii-6.03
    distance=abs(displacement)
    envelope=np.ones(system.count)
    envelope_gradient=np.zeros(system.count)
    outside=distance>=.55
    transition=(distance>.20)&(~outside)
    fraction=(distance[transition]-.20)/.35
    envelope[transition]=1-(6*fraction**5-15*fraction**4+10*fraction**3)
    envelope[outside]=0.
    envelope_gradient[transition]=-30*fraction**2*(fraction-1)**2*np.sign(displacement[transition])/.35
    plateau=(distance>.01)&(distance<.19)
    amplitude=float(np.mean(values[0,:system.count][plateau]/displacement[plateau]))
    gradient=amplitude*(envelope+displacement*envelope_gradient)
    for iteration in range(10):
        prepared=system.preparation(state)
        data=prepared['data']
        kinetic=system.node_weights*data['R'][:,:system.count]**2/(data['N'][:,:system.count]*data['U'][:,:system.count])
        desired=-data['V'][:,None]*gradient
        values[:,system.count:2*system.count]=kinetic*desired
    final=system.preparation(state)
    velocity_error=np.max(abs(final['qdot']+final['data']['V'][:,None]*gradient))
    if max(np.max(abs(final['trace'])),np.max(abs(final['trace_rate'])),velocity_error)>2e-12:
        raise ValueError('Smooth common velocity preparation did not close.')
    return state


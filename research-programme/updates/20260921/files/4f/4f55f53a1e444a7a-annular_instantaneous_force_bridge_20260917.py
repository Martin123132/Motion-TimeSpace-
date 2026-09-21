import numpy as np
from scipy.linalg import solve_banded
from annular_flat_preassembled_flow_20260916 import band_product
from derive_annular_characteristic_source_20260917 import rhs


def reference_force_rate(instant, state, initial):
    position, speed = state[:2]
    signs = np.array([1., -1.])
    feet = position-signs*instant
    scalar = initial.profile(feet)
    gradient = initial.profile(feet, 1)
    curvature = initial.profile(feet, 2)
    numerator = scalar+(1+.06*signs)*feet*gradient
    radial_numerator = (2+.06*signs)*gradient+(1+.06*signs)*feet*curvature
    traces = numerator/(position*(1+signs*speed))
    acceleration = rhs(instant, state)[1]
    trace_rates = radial_numerator*(speed-signs)/(position*(1+signs*speed))
    trace_rates -= traces*(speed/position+signs*acceleration/(1+signs*speed))
    difference = traces[0]**2-traces[1]**2
    rate = position*speed*(1-speed**2)*difference-position**2*speed*acceleration*difference
    rate += position**2*(1-speed**2)*(traces[0]*trace_rates[0]-traces[1]*trace_rates[1])
    return dict(force=position**2*(1-speed**2)*difference/2, rate=rate, traces=traces, trace_rates=trace_rates)


def canonical_momentum(model, state):
    count = model.count
    field, position, velocity, speed = state[:count], state[count], state[count+1:-2], state[-2]
    matrices = model.matrices(position)
    cross = band_product(matrices['transport'], field)
    field_momentum = band_product(matrices['mass'], velocity)+speed*cross
    source_momentum = model.system.source_mass*speed/np.sqrt(1-speed**2)
    source_momentum += velocity @ cross+speed*field @ band_product(matrices['square'], field)
    return np.append(field_momentum, source_momentum)


def force_diagnostics(adjoint, state):
    model, count = adjoint.model, adjoint.count
    context = adjoint.context(state)
    matrices = context['matrices']
    field, velocity, speed = context['field'], context['velocity'], context['speed']
    flow = context['value']['flow']
    gradient = adjoint.force_gradient(state, context)
    canonical = adjoint.canonical_covector(state, gradient, context)
    force_rate = gradient @ flow
    complex_rate = model.evaluate(state.astype(complex)+1e-25j*flow)['force'].imag/1e-25
    field_gradient = speed*band_product(matrices['transport'], velocity, True)
    field_gradient += speed**2*band_product(matrices['square'], field)-adjoint.stiffness(matrices, field)
    source_gradient = velocity @ band_product(matrices['mass_b'], velocity)/2
    source_gradient += speed*velocity @ band_product(matrices['transport_b'], field)
    source_gradient += speed**2*field @ band_product(matrices['square_b'], field)/2
    source_gradient -= field @ adjoint.stiffness(matrices, field, '_b')/2
    momentum_rate = np.append(field_gradient, source_gradient)
    pushforward = canonical_momentum(model, state.astype(complex)+1e-25j*flow).imag/1e-25
    canonical_flow = np.concatenate([velocity, [speed], momentum_rate])
    canonical_rate = canonical @ canonical_flow
    field_position, source_position = canonical[:count], canonical[count]
    field_momentum, source_momentum = canonical[count+1:-1], canonical[-1]
    dual_square = field_position @ solve_banded((2, 2), matrices['bulk'], field_position, check_finite=False)
    dual_square += source_position**2+field_momentum @ band_product(matrices['mass'], field_momentum)+source_momentum**2
    flow_square = velocity @ band_product(matrices['bulk'], velocity)+speed**2
    flow_square += field_gradient @ solve_banded((2, 2), matrices['mass'], field_gradient, check_finite=False)+source_gradient**2
    if min(dual_square, flow_square) <= 0.:
        raise ValueError('Positive energy norms required.')
    return dict(force=float(context['value']['force']), rate=float(force_rate), complex_rate=float(complex_rate),
        canonical_rate=float(canonical_rate), canonical_pushforward_error=float(max(abs(momentum_rate-pushforward))),
        energy_dual_sensitivity=float(np.sqrt(dual_square)), canonical_flow_energy_norm=float(np.sqrt(flow_square)),
        pointwise_cauchy_bound=float(np.sqrt(dual_square*flow_square)))

from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_midpoint_20260921 import CommonLoads, CommonCoordinateAction
from annular_candidate_radial_constraint_20260920 import CandidateRadialSolve
from annular_candidate_hamiltonian_20260921 import decimals
from fractions import Fraction
import numpy as np


def symbolic_balance(evidence):
    import sympy as sp
    jacobian, alpha, beta = sp.symbols('J alpha beta', positive=True)
    displacement, jacobian_source, velocity, gradient, rate = sp.symbols('d J_b V G U', real=True)
    rate_gradient, second_gradient, acceleration, source_acceleration, alpha_dot = sp.symbols('U_x G_x A A_b alpha_dot')
    alpha_radial, beta_radial = sp.symbols('alpha_r beta_r')
    physical_gradient = gradient/jacobian
    temporal = rate-velocity*displacement*physical_gradient
    density = jacobian*(alpha*temporal**2-beta*physical_gradient**2)/2
    momentum = sp.diff(density, rate)
    flux = sp.diff(density, gradient)
    source_momentum = sp.diff(density, velocity)
    source_force = sp.diff(density,jacobian)*jacobian_source+displacement*(
        sp.diff(density,alpha)*alpha_radial+sp.diff(density,beta)*beta_radial)
    time_jets = {jacobian:jacobian_source*velocity,gradient:rate_gradient,rate:acceleration,
        velocity:source_acceleration,alpha:alpha_dot}
    space_jets = {displacement:jacobian_source,gradient:second_gradient,rate:rate_gradient,
        alpha:jacobian*alpha_radial,beta:jacobian*beta_radial}
    time_derivative = lambda expression: sum(sp.diff(expression,key)*value for key,value in time_jets.items())
    space_derivative = lambda expression: sum(sp.diff(expression,key)*value for key,value in space_jets.items())
    eta = -displacement*physical_gradient
    boundary = displacement*(density/jacobian-physical_gradient*flux)
    euler = -time_derivative(momentum)-space_derivative(flux)
    evidence.check('exact_moving_map_source_EL_equals_cell_boundary_plus_field_EL',sp.simplify(
        source_force-time_derivative(source_momentum)-space_derivative(boundary)-eta*euler) == 0)
    simplified = displacement*(alpha*rate**2+(beta-alpha*(displacement*velocity)**2)*physical_gradient**2)/2
    evidence.check('boundary_flux_simplifies_without_cross_terms',sp.simplify(boundary-simplified) == 0)
    evidence.check('pinned_moving_anchor_has_wave_traction',sp.simplify(boundary.subs({displacement:1,rate:0})
        -(beta-alpha*velocity**2)*physical_gradient**2/2) == 0)
    evidence.report['symbolic_identity'] = dict(source_EL='B_x + eta E_u',eta='-d u_x/J',
        field_EL='-pi_t-H_x',momentum='pi=J alpha (u_t-d V u_x/J)',
        flux='H=-alpha (u_t-d V u_x/J) d V-beta u_x/J',
        boundary='d [alpha u_t^2+(beta-alpha d^2 V^2)(u_x/J)^2]/2',
        gram_source='-1/2 sum (sampling gradient_source)_k (factor u)_k^2',valid_for_claim=False)


def replay(owner, mesh, packet, extension, saved, deadline):
    coordinates = decimals(saved['coordinates'])
    loads = CommonLoads(owner,coordinates,saved['rates'],mesh,packet,extension,64,deadline)
    solver = CandidateRadialSolve(loads,22,28,[extension])
    if not np.array_equal(solver.edges,saved['radial_edges']):
        raise ValueError('Saved radial grid changed during replay.')
    state = saved['radial_state']
    rhs = solver.rhs(state,extension).reshape(2,*solver.nodes.shape)
    coefficients = rhs @ solver.rule.inverse.T
    primitives = np.stack([np.polynomial.chebyshev.chebint(values.T).T*solver.lengths[:,None]/2 for values in coefficients])
    for component in range(2):
        primitives[component,:,0] -= np.polynomial.chebyshev.chebval(-1.,primitives[component].T)
    increments = np.array([np.polynomial.chebyshev.chebval(1.,values.T) for values in primitives])
    left = np.c_[owner.central_mass+np.r_[0.,np.cumsum(increments[0,:-1])],
        .5*np.log(1-2*(owner.central_mass+sum(increments[0]))/solver.edges[-1])
        -sum(increments[1])+np.r_[0.,np.cumsum(increments[1,:-1])]].T
    solution = dict(state=state,rhs_coefficients=coefficients,primitives=primitives,left=left)
    action = CommonCoordinateAction(owner,coordinates,saved['rates'],mesh,loads,solver,solution,64)
    return action,float(np.max(abs(solver.residual(state,extension))))


def sampled(action, reference, cells, local, label):
    cardinal = np.asarray(action.cardinal(label)).ravel()
    source, velocity = cardinal @ action.source,cardinal @ action.velocity
    geometry = action.geometry(reference,source,label)
    jacobian, displacement, jacobian_source = [geometry[key].copy() for key in ['jacobian','displacement','jacobian_source']]
    edges = np.array([float(value) for value in action.edges])
    left_cells = edges[cells+1] <= action.owner.model.anchor
    at_left_anchor = left_cells & (reference == action.owner.model.anchor)
    left_span = action.owner.model.anchor-action.owner.model.radii[0]
    jacobian[at_left_anchor] = (source-action.owner.model.radii[0]-action.owner.width*label)/left_span
    jacobian_source[at_left_anchor] = 1/left_span
    coefficients = np.einsum('cpl,l->cp',action.gradient,cardinal)[cells]
    gradient = coefficients[:,0]+coefficients[:,1]*local
    second = coefficients[:,1]/(edges[cells+1]-edges[cells])
    coefficients = np.einsum('cpl,l->cp',action.rate_polynomial,cardinal)[cells]
    rate = coefficients[:,0]+local*(coefficients[:,1]+local*coefficients[:,2])
    rate_gradient = (coefficients[:,1]+2*coefficients[:,2]*local)/(edges[cells+1]-edges[cells])
    physical_gradient = gradient/jacobian
    physical_gradient_x = second/jacobian
    radius,metric,lapse = [geometry[key] for key in ['radius','metric','lapse']]
    alpha = radius**2/(lapse*np.sqrt(metric))
    beta = radius**2*lapse*np.sqrt(metric)
    alpha_x = jacobian*alpha*(2/radius-geometry['lapse_log_radial']-geometry['metric_radial']/(2*metric))
    beta_x = jacobian*beta*(2/radius+geometry['lapse_log_radial']+geometry['metric_radial']/(2*metric))
    mesh_velocity, mesh_velocity_x = displacement*velocity,jacobian_source*velocity
    temporal = rate-mesh_velocity*physical_gradient
    temporal_x = rate_gradient-mesh_velocity_x*physical_gradient-mesh_velocity*physical_gradient_x
    momentum = jacobian*alpha*temporal
    eta = -displacement*physical_gradient
    eta_dot = -displacement*(rate_gradient/jacobian-physical_gradient*jacobian_source*velocity/jacobian)
    flux_x = -(alpha_x*temporal*mesh_velocity+alpha*temporal_x*mesh_velocity
        +alpha*temporal*mesh_velocity_x+beta_x*physical_gradient+beta*physical_gradient_x)
    boundary = displacement*(alpha*rate**2+(beta-alpha*mesh_velocity**2)*physical_gradient**2)/2
    boundary_x = jacobian_source*(alpha*rate**2+(beta-alpha*mesh_velocity**2)*physical_gradient**2)/2
    boundary_x += displacement*(alpha_x*rate**2/2+alpha*rate*rate_gradient
        +(beta_x-alpha_x*mesh_velocity**2-2*alpha*mesh_velocity*mesh_velocity_x)*physical_gradient**2/2
        +(beta-alpha*mesh_velocity**2)*physical_gradient*physical_gradient_x)
    force_density = geometry['kinetic_source']*temporal**2/2-geometry['kinetic']*temporal*velocity*eta*jacobian_source/jacobian
    force_density -= geometry['gradient_source']*gradient**2/2
    return dict(momentum=momentum,source_momentum=eta*momentum,eta=eta,eta_dot=eta_dot,
        flux_x=flux_x,boundary=boundary,boundary_x=boundary_x,force=force_density)


def centered_extended(positive, negative, step):
    return (np.asarray(positive,np.longdouble)-np.asarray(negative,np.longdouble))/(2*np.longdouble(step))


def integrate(measure, values):
    return float(np.sum(np.asarray(measure,np.longdouble)*np.asarray(values,np.longdouble),dtype=np.longdouble))


def label_balance(base, probes, steps, label, order):
    source = np.asarray(base.cardinal(label)).ravel() @ base.source
    quadrature = base.quadrature(label,source,order)
    reference,cells,local,measure = [quadrature[key] for key in ['reference','cells','local','measure']]
    values = sampled(base,reference,cells,local,label)
    direct_momentum,direct_source,probe_momentum,probe_source = [],[],[],[]
    for index,step in enumerate(steps):
        positive,negative = [sampled(probes[index,sign],reference,cells,local,label) for sign in [1,-1]]
        direct_momentum.append(centered_extended(positive['momentum'],negative['momentum'],step))
        direct_source.append(centered_extended(positive['source_momentum'],negative['source_momentum'],step))
        probe_momentum.extend([positive['momentum'],negative['momentum']])
        probe_source.extend([positive['source_momentum'],negative['source_momentum']])
    momentum_rates = [(4*direct_momentum[index+1]-direct_momentum[index])/3 for index in range(2)]
    source_rates = [(4*direct_source[index+1]-direct_source[index])/3 for index in range(2)]
    fields = []
    for momentum_rate,source_rate in zip(momentum_rates,source_rates):
        volume = -values['eta']*(momentum_rate+values['flux_x'])
        direct = values['force']-values['eta_dot']*values['momentum']-values['eta']*momentum_rate
        fields.append(dict(volume=integrate(measure,volume),direct_product=integrate(measure,direct),
            direct_difference=integrate(measure,values['force']-source_rate),
            pointwise_identity_error=float(np.max(abs(direct-volume-values['boundary_x']))),
            source_momentum_rate=integrate(measure,source_rate)))
    edges = np.array([float(value) for value in base.edges])
    edge_cells = np.arange(len(edges)-1)
    left = sampled(base,edges[:-1],edge_cells,np.zeros(len(edge_cells)),label)['boundary']
    right = sampled(base,edges[1:],edge_cells,np.ones(len(edge_cells)),label)['boundary']
    jumps = right[:-1]-left[1:]
    hinge = list(base.edges).index(Fraction.from_float(float(base.owner.model.anchor)))-1
    anchor = float(jumps[hinge])
    internal = float(np.sum(np.delete(jumps,hinge),dtype=np.longdouble))
    exterior = float(right[-1]-left[0])
    boundary_integral = integrate(measure,values['boundary_x'])
    cardinal = np.asarray(base.cardinal(label)).ravel()
    factors = base.factor_values @ cardinal
    geometry = base.geometry(base.knots,source,label)
    gram = -float((base.sampling @ geometry['gradient_source']) @ factors**2)/2
    channels = dict(anchor=anchor,internal=internal,exterior=exterior,gram=gram,
        boundary_integral=boundary_integral,bulk_force=integrate(measure,values['force']))
    for index,result in enumerate(fields):
        channels.update({key+'_'+str(index):value for key,value in result.items()})
    raw = dict(reference=reference,cells=cells,local=local,measure=measure,
        probe_momentum=np.asarray(probe_momentum),probe_source_momentum=np.asarray(probe_source),
        jump_density=jumps,edge_left=left,edge_right=right,**values)
    return channels,raw

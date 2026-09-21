from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_energy_current_20260921 import reconstructed_solver, richardson
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_candidate_hamiltonian_20260921 import decimals
from annular_decimal_transport_v2_20260919 import decimal_array
from copy import copy
from decimal import localcontext
import numpy as np


def symbolic_controls(evidence):
    import sympy as sp
    alpha,beta,speed,left_gradient,right_gradient,reference_rate = sp.symbols('alpha beta W gL gR U')
    left_time,right_time = reference_rate-speed*left_gradient,reference_rate-speed*right_gradient
    left_energy = (alpha*left_time**2+beta*left_gradient**2)/2
    right_energy = (alpha*right_time**2+beta*right_gradient**2)/2
    left_flux,right_flux = -beta*left_time*left_gradient,-beta*right_time*right_gradient
    face = -(right_flux-left_flux)+speed*(right_energy-left_energy)
    expected = (left_time+right_time)*(beta-alpha*speed**2)*(right_gradient-left_gradient)/2
    evidence.check('moving_face_power_uses_average_time_trace',sp.expand(face-expected)==0)
    traction = (beta-alpha*speed**2)*(left_gradient**2-right_gradient**2)/2
    evidence.check('pinned_anchor_face_power_matches_traction',sp.expand(face.subs(reference_rate,0)-speed*traction)==0)
    gamma,load,source_gamma,velocity,metric_rate,field_power = sp.symbols('gamma load gamma_b V M power')
    gamma_rate = source_gamma*velocity+gamma*metric_rate
    energy_divergence = -field_power+gamma_rate*load
    gram_divergence = -energy_divergence+gamma*load*metric_rate
    evidence.check('Gram_temporal_Ward_source_reduces_to_action_work',sp.expand(gram_divergence-field_power+velocity*source_gamma*load)==0)
    density,density_t,lapse_t,metric_t,lapse,metric,flux_r,pressure = sp.symbols('h h_t N_t F_t N F j_r p')
    integral_factor_log_t = lapse_t/lapse-metric_t/(2*metric)
    reduced = -density_t+density*integral_factor_log_t-flux_r+(density+pressure)*metric_t/(2*metric)
    evidence.check('weighted_stress_divergence_energy_exchange',sp.simplify(reduced
        -(-density_t-flux_r+density*lapse_t/lapse+pressure*metric_t/(2*metric)))==0)
    source_rate,source_EL,explicit_time = sp.symbols('V E_d L_t')
    hamiltonian_rate = -source_rate*source_EL-explicit_time
    evidence.check('dust_temporal_Ward_source_is_velocity_times_EL',sp.expand(-hamiltonian_rate-explicit_time-source_rate*source_EL)==0)


def probe_action(base,saved,archive):
    action = copy(base)
    action.solver,action.solution = reconstructed_solver(archive)
    action.source = np.asarray(saved['coordinates'][:,-1],float)
    action.velocity = saved['rates'][:,-1]
    with localcontext() as context:
        context.prec = 64
        action.polynomial,action.gradient = local_polynomials(action.mesh,decimals(saved['coordinates'][:,:-1]).T)
        action.rate_polynomial,unused = local_polynomials(action.mesh,decimal_array(saved['rates'][:,:-1].T))
    return action


def fields(action,reference,cells,local,label):
    cardinal = np.asarray(action.cardinal(label)).ravel()
    source,velocity = cardinal @ action.source,cardinal @ action.velocity
    geometry = action.geometry(reference,source,label)
    jacobian,displacement,jacobian_source = [geometry[key].copy() for key in ['jacobian','displacement','jacobian_source']]
    edges = np.array([float(value) for value in action.edges])
    left_anchor = (edges[cells+1]<=action.owner.model.anchor)&(reference==action.owner.model.anchor)
    span = action.owner.model.anchor-action.owner.model.radii[0]
    jacobian[left_anchor] = (source-action.owner.model.radii[0]-action.owner.width*label)/span
    jacobian_source[left_anchor] = 1/span
    coefficients = np.einsum('cpl,l->cp',action.gradient,cardinal)[cells]
    gradient = (coefficients[:,0]+coefficients[:,1]*local)/jacobian
    gradient_x = coefficients[:,1]/((edges[cells+1]-edges[cells])*jacobian)
    rates = np.einsum('cpl,l->cp',action.rate_polynomial,cardinal)[cells]
    reference_rate = rates[:,0]+local*(rates[:,1]+local*rates[:,2])
    rate_x = (rates[:,1]+2*local*rates[:,2])/(edges[cells+1]-edges[cells])
    radius,metric,lapse = [geometry[key] for key in ['radius','metric','lapse']]
    alpha = radius**2/(lapse*np.sqrt(metric))
    beta = radius**2*lapse*np.sqrt(metric)
    alpha_x = jacobian*alpha*(2/radius-geometry['lapse_log_radial']-geometry['metric_radial']/(2*metric))
    beta_x = jacobian*beta*(2/radius+geometry['lapse_log_radial']+geometry['metric_radial']/(2*metric))
    speed,speed_x = displacement*velocity,jacobian_source*velocity
    temporal = reference_rate-speed*gradient
    temporal_x = rate_x-speed_x*gradient-speed*gradient_x
    momentum = jacobian*alpha*temporal
    flux_x = -(alpha_x*temporal*speed+alpha*temporal_x*speed+alpha*temporal*speed_x
        +beta_x*gradient+beta*gradient_x)
    energy = (alpha*temporal**2+beta*gradient**2)/2
    flux = -beta*temporal*gradient
    return dict(radius=radius,temporal=temporal,momentum=momentum,flux_x=flux_x,energy=energy,
        physical_flux=flux,speed=speed,gradient=gradient,alpha=alpha,beta=beta,reference_rate=reference_rate)


def material_quadrature(loads,radius,order):
    references = np.unique(np.r_[loads.knots,loads.owner.model.edges])
    endpoints = np.array([loads.material.node_geometry(references,label)[0] for label in [-.5,.5]])
    cuts = [-.5,.5]
    for target in radius:
        selected = (target>endpoints[0])&(target<endpoints[1])
        if np.any(selected):
            cuts.extend(loads.material.inverse_node(np.full(sum(selected),target),references[selected]))
    cuts = np.unique(cuts)
    cuts = cuts[np.r_[True,np.diff(cuts)>1e-13]]
    points,weights = np.polynomial.legendre.leggauss(order)
    labels = ((cuts[:-1,None]+cuts[1:,None])/2+np.diff(cuts)[:,None]*points/2).ravel()
    measure = (np.diff(cuts)[:,None]*weights/2).ravel()*6*(labels+.5)*(.5-labels)
    return labels,measure,cuts


def label_source(base,loads,probes,steps,radius,label,order):
    cardinal = np.asarray(base.cardinal(label)).ravel()
    source,velocity = cardinal @ base.source,cardinal @ base.velocity
    quadrature_action = copy(base)
    quadrature_action.solver = copy(base.solver)
    quadrature_action.solver.edges = np.unique(np.r_[base.solver.edges,radius])
    quadrature = quadrature_action.quadrature(label,source,order)
    reference,cells,local,measure = [quadrature[key] for key in ['reference','cells','local','measure']]
    values = fields(base,reference,cells,local,label)
    probe_momentum = np.array([[fields(probes[index,sign],reference,cells,local,label)['momentum']
        for sign in [-1,1]] for index in range(3)])
    unused,momentum_rate = richardson(probe_momentum,steps)
    selections = values['radius'][:,None]<radius[None,:]
    measures = measure[:,None]*selections
    space_work = (values['temporal']*values['flux_x']) @ measures
    time_work = np.array([(values['temporal']*rate) @ measures for rate in momentum_rate])
    probe_work = np.einsum('abq,q,qk->abk',probe_momentum,values['temporal'],measures,optimize=True)
    volume = -time_work-space_work
    edges = np.array([float(value) for value in base.edges])
    cell_indices = np.arange(len(edges)-1)
    left = fields(base,edges[:-1],cell_indices,np.zeros(len(cell_indices)),label)
    right = fields(base,edges[1:],cell_indices,np.ones(len(cell_indices)),label)
    face_radius = right['radius'][:-1]
    face_speed = (left['speed'][1:]+right['speed'][:-1])/2
    face_power = -(left['physical_flux'][1:]-right['physical_flux'][:-1])
    face_power += face_speed*(left['energy'][1:]-right['energy'][:-1])
    face_average = (left['temporal'][1:]+right['temporal'][:-1])/2
    face_EL = (left['beta'][1:]-left['alpha'][1:]*face_speed**2)*(left['gradient'][1:]-right['gradient'][:-1])
    hinge = np.flatnonzero(edges[1:-1]==base.owner.model.anchor)
    ordinary = np.ones(len(face_radius),dtype=bool)
    ordinary[hinge] = False
    face_masks = face_radius[:,None]<radius
    internal = (face_power*ordinary) @ face_masks
    anchor = (face_power*~ordinary) @ face_masks
    exterior_power = np.array([-(left['physical_flux'][0]-left['speed'][0]*left['energy'][0]),
        right['physical_flux'][-1]-right['speed'][-1]*right['energy'][-1]])
    exterior_radius = np.array([left['radius'][0],right['radius'][-1]])
    exterior = exterior_power @ (exterior_radius[:,None]<radius)
    def dust_momentum(action):
        position,speed = cardinal @ action.source,cardinal @ action.velocity
        metric_values,unused = action.solver.values(action.solution,np.array([position]))
        metric = 1-2*metric_values[0,0]/position
        lapse = np.exp(metric_values[1,0])
        return action.owner.source_mass*speed/(metric*np.sqrt(lapse**2-speed**2/metric))
    dust_probe = np.array([[dust_momentum(probes[index,sign]) for sign in [-1,1]] for index in range(3)])
    unused,dust_rate = richardson(dust_probe,steps)
    dust_force = base.dust(source,velocity)[1]
    dust = velocity*(dust_force-dust_rate[:,None])*(source<radius)
    geometry = base.geometry(base.knots,source,label)
    image = base.factor_values @ cardinal
    sampled = loads.sampling @ geometry['gradient']
    with localcontext() as context:
        context.prec = 64
        gram_force = -np.asarray(loads.factor.apply(decimal_array((sampled*image)[:,None]),transpose=True)[:,0],float)
    node_load = np.asarray(loads.sampling.T @ (image**2/2))
    field_power = (cardinal @ loads.rates[:,:-1])*gram_force
    source_power = -velocity*geometry['gradient_source']*node_load
    node_mask = geometry['radius'][:,None]<radius
    gram_field = field_power @ node_mask
    gram_source = source_power @ node_mask
    total = volume+internal+anchor+exterior+dust+gram_field+gram_source
    raw = dict(probe_temporal_momentum=probe_work,time_work=time_work,space_work=space_work,volume=volume,
        internal=internal,anchor=anchor,exterior=exterior,dust=dust,gram_field=gram_field,gram_source=gram_source,total=total,
        face_radius=face_radius,face_power=face_power,face_average=face_average,face_EL=face_EL,ordinary_mask=ordinary,
        exterior_radius=exterior_radius,exterior_power=exterior_power,dust_probe=dust_probe,dust_force=dust_force,
        source=source,velocity=velocity,node_radius=geometry['radius'],node_field_power=field_power,node_source_power=source_power,
        quadrature_points=len(reference))
    spot = dict(reference=reference,cells=cells,local=local,measure=measure,probe_momentum=probe_momentum,
        temporal=values['temporal'],flux_x=values['flux_x'],physical_radius=values['radius'])
    return raw,spot

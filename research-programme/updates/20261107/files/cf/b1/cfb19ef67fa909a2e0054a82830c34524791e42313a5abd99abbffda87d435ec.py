from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_radial_constraint_20260920 import CandidateRadialSolve
from annular_candidate_midpoint_20260921 import CommonLoads, CommonCoordinateAction
from annular_candidate_canonical_response_20260920 import temporal_values
from annular_P2_indexed_live_geometry_20260919 import IndexedP2Density
from annular_candidate_hamiltonian_20260921 import decimals
from annular_decimal_transport_v2_20260919 import decimal_array
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
from decimal import localcontext
from copy import copy
from math import fsum
from time import perf_counter
import numpy as np


def symbolic_checks(evidence):
    import sympy as sp
    factor = sp.Matrix([[1,-2,1],[2,1,-3]])
    sampling = sp.Matrix([[sp.Rational(1,3),sp.Rational(2,3),0],[0,sp.Rational(1,4),sp.Rational(3,4)]])
    field = sp.Matrix(sp.symbols('u0:3'))
    rate = sp.Matrix(sp.symbols('v0:3'))
    gamma = sp.Matrix(sp.symbols('g0:3',positive=True))
    gamma_dot = sp.Matrix(sp.symbols('gd0:3'))
    image, image_rate = factor*field,factor*rate
    sampled = sampling*gamma
    force = -factor.T*sp.diag(*sampled)*image
    transfer = sp.diag(*gamma)*sampling.T*sp.diag(*image)*factor*sp.diag(*rate)
    outgoing = transfer.T-transfer
    energy_rate = sp.diag(*gamma)*sampling.T*sp.diag(*image)*image_rate
    exchange = sp.diag(*gamma_dot)*sampling.T*sp.Matrix([value**2/2 for value in image])
    residual = energy_rate+exchange+sp.diag(*rate)*force+outgoing*sp.ones(3,1)-exchange
    evidence.check('symbolic_actual_Gram_node_power_identity',all(sp.expand(value)==0 for value in residual))
    evidence.check('symbolic_Gram_bond_current_antisymmetric',outgoing+outgoing.T==sp.zeros(3))
    for cut in [0,1,2,3]:
        mask = sp.diag(*([1]*cut+[0]*(3-cut)))
        cut_formula = (image.T*(sp.diag(*sampled)*factor*mask*rate-sp.diag(*(sampling*mask*gamma))*image_rate))[0]
        crossing = sum(outgoing[first,last] for first in range(cut) for last in range(cut,3))
        evidence.check('symbolic_cut_current_'+str(cut),sp.expand(cut_formula-crossing)==0)
    time,radius,angle,azimuth = sp.symbols('t r theta phi',real=True)
    lapse,metric = sp.Function('N')(time,radius),sp.Function('F')(time,radius)
    coordinates = [time,radius,angle,azimuth]
    tensor = sp.diag(-lapse**2,1/metric,radius**2,radius**2*sp.sin(angle)**2)
    inverse = tensor.inv()
    christoffel = [[[sp.simplify(sum(inverse[upper,index]*(sp.diff(tensor[index,last],coordinates[first])
        +sp.diff(tensor[index,first],coordinates[last])-sp.diff(tensor[first,last],coordinates[index]))/2
        for index in range(4))) for last in range(4)] for first in range(4)] for upper in range(4)]
    ricci = sum(sp.diff(christoffel[index][0][1],coordinates[index])-sp.diff(christoffel[index][0][index],radius)
        +sum(christoffel[index][0][1]*christoffel[other][index][other]
        -christoffel[other][0][index]*christoffel[index][1][other] for other in range(4)) for index in range(4))
    evidence.check('derived_mixed_Einstein_tensor_G_r_t',sp.simplify(metric*ricci+sp.diff(metric,time)/radius)==0)


def reconstructed_solver(archive):
    solver = CandidateRadialSolve.__new__(CandidateRadialSolve)
    solver.edges = archive['edges']
    solver.lengths = np.diff(solver.edges)
    solver.centers = (solver.edges[:-1]+solver.edges[1:])/2
    solution = {key:archive[key] for key in ['state','rhs_coefficients','primitives','left']}
    return solver,solution


def excess_mass(solver,solution,radius):
    increments = np.polynomial.chebyshev.chebval(1.,solution['primitives'][0].T)
    prefix = np.array([fsum(increments[:index]) for index in range(len(increments))])
    selected = np.clip(np.searchsorted(solver.edges,radius,side='right')-1,0,len(solver.edges)-2)
    mapped = 2*(radius-solver.centers[selected])/solver.lengths[selected]
    return prefix[selected]+np.polynomial.chebyshev.chebval(mapped,solution['primitives'][0,selected].T,tensor=False)


def richardson(values,steps):
    differences = (values[:,1]-values[:,0])/(2*np.asarray(steps).reshape((-1,)+(1,)*(values.ndim-2)))
    extrapolated = (4*differences[1:]-differences[:-1])/3
    return differences,extrapolated


def build_base(owner,mesh,packet,extension,saved,archive,deadline):
    coordinates = decimals(saved['coordinates'])
    loads = CommonLoads(owner,coordinates,saved['rates'],mesh,packet,extension,64,deadline)
    solver,solution = reconstructed_solver(archive)
    action = CommonCoordinateAction(owner,coordinates,saved['rates'],mesh,loads,solver,solution,64)
    return loads,action


def wave_dust_current(loads,action,radius,order):
    owner = loads.owner
    owner.label_order = order
    channels = {key:np.zeros(len(radius)) for key in ['cross_moment','source_density','velocity','temporal_square','gradient_square']}
    for start in range(0,len(radius),32):
        if perf_counter()>loads.deadline:
            raise RuntimeError('Saved-work boundary during wave current quadrature.')
        section = slice(start,start+32)
        density = IndexedP2Density(loads.material,radius[section])
        density.update(loads.rates)
        temporal = temporal_values(density,loads.rates)
        gradient = loads.material.samples(density.radius[density.indices],density.offsets)[3]
        channels['cross_moment'][section] = np.bincount(density.indices,
            weights=density.label_weights*temporal*gradient,minlength=len(density.radius))
        for key in ['source_density','velocity','temporal_square','gradient_square']:
            channels[key][section] = getattr(density,key)
    values,derivatives = action.solver.values(action.solution,radius)
    mass,lapse = values[0],np.exp(values[1])
    metric = 1-2*mass/radius
    velocity = channels['velocity']
    clock = np.sqrt(lapse**2-velocity**2/metric)
    conversion = owner.coupling*np.sqrt(metric)/lapse
    wave_energy = -radius**2*lapse*np.sqrt(metric)*channels['cross_moment']
    dust_mass_density = owner.coupling*owner.source_mass*channels['source_density']*np.sqrt(metric)*lapse/clock
    channels.update(mass=mass,lapse=lapse,metric=metric,conversion=conversion,
        wave_energy_current=wave_energy,wave_mass_current=conversion*wave_energy,
        dust_mass_density=dust_mass_density,dust_mass_current=velocity*dust_mass_density,
        mass_radial=derivatives[0])
    return channels


def gram_nodes(loads,action,labels):
    cardinal = loads.material.interpolation(labels)
    source = cardinal @ action.source
    geometry = [action.geometry(action.knots,position,label) for position,label in zip(source,labels)]
    gamma = np.array([row['gradient'] for row in geometry])
    gamma_source = np.array([row['gradient_source'] for row in geometry])
    with localcontext() as context:
        context.prec = 64
        image_rate_vertices = np.asarray(loads.factor.apply(decimal_array(loads.rates[:,:-1].T)),float)
    image = cardinal @ np.asarray(loads.exact_factors.T,float)
    image_rate = cardinal @ image_rate_vertices.T
    velocity = cardinal @ loads.rates[:,:-1]
    source_velocity = cardinal @ loads.rates[:,-1]
    sampled = (loads.sampling @ gamma.T).T
    with localcontext() as context:
        context.prec = 64
        force = -np.asarray(loads.factor.apply(decimal_array((sampled*image).T),transpose=True).T,float)
    node_load = np.asarray(loads.sampling.T @ (image**2/2).T).T
    internal_rate = gamma*np.asarray(loads.sampling.T @ (image*image_rate).T).T
    field_power = velocity*force
    outward_increment = -field_power-internal_rate
    source_power = -source_velocity*np.sum(gamma_source*node_load,axis=1)
    return dict(labels=labels,cardinal=cardinal,gamma=gamma,gamma_source=gamma_source,
        image=image,image_rate=image_rate,sampled=sampled,velocity=velocity,source_velocity=source_velocity,
        force=force,node_load=node_load,energy=gamma*node_load,internal_rate=internal_rate,
        field_power=field_power,outward_increment=outward_increment,source_power=source_power,
        radius=np.array([row['radius'] for row in geometry]),
        mesh_velocity=np.array([row['displacement'] for row in geometry])*source_velocity[:,None])


def gram_cut_current(loads,action,radius,degree):
    rule = ChebyshevRule(degree)
    nodes = gram_nodes(loads,action,rule.points/2)
    weight = 6*(nodes['labels']+.5)*(.5-nodes['labels'])
    coefficients = rule.inverse @ (weight[:,None]*nodes['outward_increment'])
    primitive = np.polynomial.chebyshev.chebint(coefficients,axis=0)/2
    lower = np.polynomial.chebyshev.chebval(-1.,primitive)
    graph = np.zeros(len(radius))
    advection = np.zeros(len(radius))
    for index,reference in enumerate(loads.knots):
        endpoints = loads.material.node_geometry(reference,np.array([-.5,.5]))[0]
        labels = loads.material.inverse_node(np.clip(radius,*endpoints),reference)
        labels[radius<=endpoints[0]] = -.5
        labels[radius>=endpoints[1]] = .5
        graph += np.polynomial.chebyshev.chebval(2*labels,primitive[:,index])-lower[index]
        selected = (radius>endpoints[0]) & (radius<endpoints[1])
        if np.any(selected):
            label = labels[selected]
            cardinal = loads.material.interpolation(label)
            source = cardinal @ action.source
            velocity = cardinal @ action.velocity
            unused,spatial,label_jacobian = loads.material.node_geometry(reference,label)
            unused,unused2,displacement = action.owner.model.mapping(np.full(len(label),reference),action.owner.model.anchor)
            values,unused = action.solver.values(action.solution,radius[selected])
            gamma = radius[selected]**2*np.exp(values[1])*np.sqrt(1-2*values[0]/radius[selected])/spatial
            advection[selected] += 6*(label+.5)*(.5-label)*displacement*velocity*gamma*loads.node_load(label,index,
                next(iter(loads.factor_coefficients)))/label_jacobian
    return dict(graph=graph,advection=advection,total=graph+advection),nodes


def gram_power_probes(loads,action,nodes,states,archives,steps):
    gammas,images,metric_logs = [],[],[]
    labels,cardinal = nodes['labels'],nodes['cardinal']
    for index in range(3):
        gamma_pair,image_pair,log_pair = [],[],[]
        for sign in [-1,1]:
            state,archive = states[index,sign],archives[index,sign]
            probe = copy(action)
            probe.solver,probe.solution = reconstructed_solver(archive)
            probe.source = np.asarray(state['coordinates'][:,-1],float)
            geometries = [probe.geometry(probe.knots,cardinal[position] @ probe.source,label)
                for position,label in enumerate(labels)]
            gamma_pair.append(np.array([row['gradient'] for row in geometries]))
            with localcontext() as context:
                context.prec = 64
                image_pair.append(cardinal @ np.asarray(loads.factor.apply(decimals(state['coordinates'][:,:-1]).T).T,float))
            values,unused = probe.solver.values(probe.solution,nodes['radius'].ravel())
            logs = values[1]+np.log(1-2*values[0]/nodes['radius'].ravel())/2
            log_pair.append(logs.reshape(nodes['radius'].shape))
        gammas.append(gamma_pair)
        images.append(image_pair)
        metric_logs.append(log_pair)
    gammas,images,metric_logs = map(np.asarray,[gammas,images,metric_logs])
    unused,gamma_rate = richardson(gammas,steps)
    unused,metric_rate = richardson(metric_logs,steps)
    energies = np.array([[np.sum(pair_gamma*np.asarray(loads.sampling.T @ (pair_image**2/2).T).T,axis=1)
        for pair_gamma,pair_image in zip(gamma_pair,image_pair)] for gamma_pair,image_pair in zip(gammas,images)])
    unused,energy_rate = richardson(energies,steps)
    exchange = np.sum(nodes['gamma']*metric_rate*nodes['node_load'],axis=2)
    analytic_rate = np.sum(nodes['internal_rate'],axis=1)+np.sum(gamma_rate*nodes['node_load'],axis=2)
    field_power = np.sum(nodes['field_power'],axis=1)
    balance = analytic_rate+field_power+nodes['source_power']-exchange
    return dict(probe_gamma=gammas,probe_image=images,probe_metric_log=metric_logs,probe_energy=energies,
        gamma_rate=gamma_rate,metric_rate=metric_rate,energy_rate=energy_rate,metric_exchange=exchange,
        analytic_energy_rate=analytic_rate,energy_balance=balance,
        coefficient_chain_residual=gamma_rate-nodes['gamma_source']*nodes['source_velocity'][:,None]-nodes['gamma']*metric_rate)

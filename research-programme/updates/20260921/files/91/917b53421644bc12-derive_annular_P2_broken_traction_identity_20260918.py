from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_primitive_geometry_20260918 import PrimitiveP2System
from annular_live_P2_current_20260918 import LiveP2Tangent, physical_sample
from diagnose_annular_P2_traction_gap_20260918 import trace_pressure
from run_annular_P2_continuum_bridge_20260918 import checked_load
import argparse
import numpy as np
import sympy as symbolic


def broken_traction(tangent, order=32):
    current = tangent.layer_data(0.)
    layer, values, rates = current.layer, current.coordinates, current.rates
    geometry = tangent.geometry
    boundaries, unused, unused2 = layer.mapping(layer.edges, values[-1])
    interior = geometry.edges[(geometry.edges > boundaries[0]) & (geometry.edges < boundaries[-1])]
    endpoints = np.unique(np.concatenate([boundaries, interior]))
    points, weights = np.polynomial.legendre.leggauss(order)
    lengths = np.diff(endpoints)
    radius = ((endpoints[:-1,None]+endpoints[1:,None])/2+lengths[:,None]*points/2).ravel()
    quadrature = (lengths[:,None]*weights/2).ravel()
    temporal, gradient = physical_sample(layer,values,rates,radius)
    temporal_changed, unused = physical_sample(current.tangent_layer,current.changed_coordinates,current.changed_rates,radius)
    time_derivative = (radius**4/current.tangent_layer.coefficient(0.,radius)*temporal_changed).imag/current.step
    unused, spatial_changed = physical_sample(layer,values,rates,radius.astype(complex)+1j*current.step)
    spatial_derivative = (layer.coefficient(0.,radius.astype(complex)+1j*current.step)*spatial_changed).imag/current.step
    residual = time_derivative-spatial_derivative
    motion = np.where(radius < values[-1], (radius-boundaries[0])/(values[-1]-boundaries[0]),
        (boundaries[-1]-radius)/(boundaries[-1]-values[-1]))
    integrand = residual*motion*gradient
    bulk = float(quadrature @ integrand)
    bulk_absolute = float(quadrature @ abs(integrand))
    midpoint = (layer.edges[:-1]+layer.edges[1:])/2
    unused, jacobian, unused2 = layer.mapping(midpoint,values[-1])
    indices = layer.element_indices
    valid = indices >= 0
    local_values = values[:-1][np.maximum(indices,0)]*valid
    reference_lengths = np.diff(layer.edges)
    gradient_lower = (local_values @ np.array([-3.,4.,-1.]))/(reference_lengths*jacobian)
    gradient_upper = (local_values @ np.array([1.,-4.,3.]))/(reference_lengths*jacobian)
    internal = np.arange(1,len(layer.edges)-1)
    source_edge = np.searchsorted(layer.edges,layer.anchor)
    internal = internal[internal != source_edge]
    radius_edge, unused, motion_edge = layer.mapping(layer.edges[internal],values[-1])
    coefficient = layer.coefficient(0.,radius_edge)
    kinetic = radius_edge**4/coefficient
    speed_edge = motion_edge*rates[-1]
    jumps = motion_edge*(coefficient-kinetic*speed_edge**2)*(gradient_upper[internal-1]**2-gradient_lower[internal]**2)/2
    nodes, jacobian_nodes, motion_nodes = layer.mapping(layer.radii,values[-1])
    coefficient_nodes = layer.coefficient(0.,nodes)
    coefficient_radial = layer.coefficient(0.,nodes.astype(complex)+1j*current.step).imag/current.step
    jacobian_source = np.where(layer.radii < layer.anchor, 1/(layer.anchor-layer.radii[0]), -1/(layer.radii[-1]-layer.anchor))
    factor = layer.lifted @ values[:-1]
    atom_weights = np.asarray(layer.sampling.T @ factor**2)/(2*layer.gram_spacing)
    gram = float(-atom_weights @ (coefficient_radial*motion_nodes/jacobian_nodes
        -coefficient_nodes*jacobian_source/jacobian_nodes**2))
    pressure = trace_pressure(tangent.system,tangent.coordinates,tangent.rates,geometry)['finite_trace_pressure']
    force = float(-current.wave_source_euler)
    interior_sum = float(sum(jumps))
    return dict(force=force, trace_pressure=pressure, bulk_Euler_work=bulk,
        internal_moving_edge_work=interior_sum, explicit_Gram_shape_force=gram,
        actual_defect=force-pressure, derived_defect=bulk+interior_sum+gram,
        identity_error=abs(force-pressure-bulk-interior_sum-gram),
        absolute_term_bound=bulk_absolute+float(sum(abs(jumps)))+abs(gram),
        maximum_regular_Euler_residual=float(max(abs(residual))))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--counts', nargs='+', type=int, default=[17,33])
    args = parser.parse_args()
    tag = '-'.join(map(str,args.counts))
    evidence = EvidenceRun('annular-P2-broken-traction-'+tag+'-attempt01',__file__)
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_forward_evolution=True,
            finite_Gram_retained=True, no_force_correction_applied=True,
            full_live_P2_force_convergence_proven=False, boundary_virtual_work_identity_not_convergence=True,
            continuous_piecewise_integral_identity_with_measured_quadrature_error=True)
        kinetic, coefficient, temporal, gradient, speed = symbolic.symbols('A C W H v', real=True)
        endpoint = kinetic*temporal**2/2-coefficient*gradient**2/2+(coefficient*gradient+speed*kinetic*temporal)*gradient
        factored = kinetic*(temporal+speed*gradient)**2/2+(coefficient-kinetic*speed**2)*gradient**2/2
        evidence.check('moving_spacetime_endpoint_identity',symbolic.expand(endpoint-factored) == 0)
        for count in args.counts:
            for branch in ['reference','MTS']:
                if count == 17:
                    data = checked_load(evidence,'annular-P2-tight-budget-'+branch+'-attempt01','principal.npz')
                else:
                    data = checked_load(evidence,'annular-P2-continuum-bridge-'+branch+'-'+str(count)+'-attempt01','trajectory.npz')
                system = PrimitiveP2System(count,branch == 'MTS',layer_degree=14,radial_degree=18,action_order=32,label_order=20)
                states = data['states'].reshape(5,2,len(system.labels),system.count+1)
                for index in [0,4]:
                    coordinates,momenta = states[index]
                    tangent = LiveP2Tangent(system,coordinates,momenta)
                    row = broken_traction(tangent)
                    controlled = broken_traction(tangent,order=48)
                    row.update(branch=branch,base_count=count,time=float(data['times'][index]),
                        quadrature_change=abs(controlled['derived_defect']-row['derived_defect']))
                    evidence.report['cases'].append(row)
                    evidence.save()
                    print(row,flush=True)
                    evidence.check(branch+str(count)+'_'+str(index)+'_derived_force_identity',row['identity_error'] < 2e-9,row)
                    evidence.check(branch+str(count)+'_'+str(index)+'_quadrature_control',row['quadrature_change'] < 2e-9,row['quadrature_change'])
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

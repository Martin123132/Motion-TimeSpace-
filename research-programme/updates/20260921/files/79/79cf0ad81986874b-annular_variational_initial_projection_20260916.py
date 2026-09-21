import numpy as np
from scipy.linalg import solve_banded
from scipy.sparse import coo_matrix, diags
from scipy.sparse.linalg import spsolve
from run_annular_source_fitted_crossing_20260915 import profile, initial


def projection_features(system, reference):
    if hasattr(system,'features_quadratic'):
        return system.features_quadratic(reference)
    cells, shape, radial, unused = system.features(reference,system.anchor)
    return np.column_stack([cells,cells+1]),shape,radial


def assemble_vector(system, indices, values):
    result = np.zeros(system.count,dtype=values.dtype)
    np.add.at(result,indices.ravel(),values.ravel())
    return result


def assemble_matrix(system, indices, basis, weights):
    rows, columns, values = [],[],[]
    for first in range(indices.shape[1]):
        for second in range(indices.shape[1]):
            rows.append(indices[:,first])
            columns.append(indices[:,second])
            values.append(weights*basis[:,first]*basis[:,second])
    return coo_matrix((np.concatenate(values),(np.concatenate(rows),np.concatenate(columns))),shape=(system.count,system.count)).tocsr()


def projection_quadrature(system, order=12):
    edges = np.unique(np.concatenate([system.radii,[system.anchor],6.03+np.array([-.55,-.2,.2,.55])]))
    points, weights = np.polynomial.legendre.leggauss(order)
    radius = ((edges[:-1,None]+edges[1:,None])/2+np.diff(edges)[:,None]*points/2).ravel()
    measure = (np.diff(edges)[:,None]*weights/2).ravel()
    return radius,measure


def variational_initial(system, project_configuration=True, project_velocity=True, order=12):
    state = initial(system)
    coordinates,rates = np.split(state[:-1],2)
    reference,weights = projection_quadrature(system,order)
    indices,shape,radial = projection_features(system,reference)
    radius,jacobian,displacement = system.mapping(reference,coordinates[-1])
    coefficient = system.coefficient(0.,radius)
    unused,exact_gradient = profile(radius)
    exact_temporal = -.06*exact_gradient
    derivative = radial/jacobian[:,None]
    measure = weights*jacobian
    original_data = system.evaluate(0.,coordinates,rates)
    original_factor,hinge,jump = system.gram_data(system.anchor,coordinates[:-1])
    if hasattr(system,'lifted'):
        lifted = system.lifted
    else:
        from scipy.sparse import csr_matrix
        lifted = system.original-csr_matrix(hinge[:,None]) @ csr_matrix(jump[None,:])
    gram_spacing = getattr(system,'gram_spacing',system.spacing)
    node_radius,node_jacobian,unused = system.mapping(system.radii,coordinates[-1])
    gram_coefficient = np.asarray(system.sampling @ (system.coefficient(0.,node_radius)/node_jacobian))/gram_spacing
    exact_nodal,unused = profile(node_radius)
    exact_factor = system.original @ exact_nodal
    stiffness = assemble_matrix(system,indices,derivative,measure*coefficient)+lifted.T @ diags(gram_coefficient) @ lifted
    configuration_right = assemble_vector(system,indices,derivative*(measure*coefficient*exact_gradient)[:,None])+lifted.T @ (gram_coefficient*exact_factor)
    if project_configuration:
        coordinates[:-1] = spsolve(stiffness.tocsc(),configuration_right)
    gradient = np.sum(derivative*coordinates[:-1][indices],axis=1)
    temporal_weight = measure*radius**4/coefficient
    desired_pulled_rate = exact_temporal+displacement*rates[-1]*gradient
    velocity_right = assemble_vector(system,indices,shape*(temporal_weight*desired_pulled_rate)[:,None])
    updated_data = system.evaluate(0.,coordinates,rates)
    bands = updated_data['mass_bands']
    bandwidth = (len(bands)-1)//2
    if project_velocity:
        rates[:-1] = solve_banded((bandwidth,bandwidth),bands,velocity_right)
    mass = assemble_matrix(system,indices,shape,temporal_weight)
    configuration_residual = stiffness @ coordinates[:-1]-configuration_right
    velocity_residual = mass @ rates[:-1]-velocity_right
    temporal = np.sum(shape*rates[:-1][indices],axis=1)-displacement*rates[-1]*gradient
    old_gradient = original_data['field_radial']
    old_factor = lifted @ initial(system)[:system.count]
    projected_factor = lifted @ coordinates[:-1]
    gradient_error = np.dot(measure*coefficient,(gradient-exact_gradient)**2)
    gram_error = np.dot(gram_coefficient,(projected_factor-exact_factor)**2)
    diagnostic = dict(configuration_normal_residual=float(np.max(abs(configuration_residual))),
        velocity_normal_residual=float(np.max(abs(velocity_residual))),
        gradient_error_squared=float(gradient_error),Gram_projection_error_squared=float(gram_error),
        velocity_error_squared=float(np.dot(temporal_weight,(temporal-exact_temporal)**2)),
        coordinate_change=float(np.max(abs(coordinates[:-1]-initial(system)[:system.count]))),
        project_configuration=project_configuration,project_velocity=project_velocity,
        exact_profile_Gram_target_not_zeroed=True,force_not_used_to_choose_projection=True)
    return np.concatenate([coordinates,rates,[0.]]),diagnostic

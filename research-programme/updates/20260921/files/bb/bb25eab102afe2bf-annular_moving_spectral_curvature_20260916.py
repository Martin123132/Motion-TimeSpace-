import numpy as np
from scipy.sparse import diags
from annular_boundary_response_20260916 import basis_matrix
from annular_moving_spectral_frame_20260916 import system_frame


def analytic_matrix_derivatives(system, position):
    if system.background_mass is None:
        raise ValueError('Closed derivatives apply only to the prescribed constant-mass metric.')
    radius, jacobian, displacement = system.mapping(system.reference_radius, position)
    inner, outer = system.radii[[0,-1]]
    jacobian_b = np.where(system.reference_radius<system.anchor,1/(system.anchor-inner),-1/(outer-system.anchor))
    parameter = 2*system.background_mass
    if not np.allclose(system.coefficient(0.,radius),radius*(radius-parameter),rtol=2e-13,atol=2e-13):
        raise ValueError('Metric coefficient is not the qualified prescribed expression.')
    function = radius**3/(radius-parameter)
    first = 2*radius+parameter-parameter**3/(radius-parameter)**2
    second = 2+2*parameter**3/(radius-parameter)**3
    temporal_b = system.reference_weight*(jacobian_b*function+jacobian*displacement*first)
    temporal_bb = system.reference_weight*(2*jacobian_b*displacement*first+jacobian*displacement**2*second)
    transport_b = -system.reference_weight*displacement**2*first
    transport_bb = -system.reference_weight*displacement**3*second
    square_b = system.reference_weight*displacement**2*(displacement*first/jacobian-function*jacobian_b/jacobian**2)
    square_bb = system.reference_weight*displacement**2*(displacement**2*second/jacobian
        -2*displacement*first*jacobian_b/jacobian**2+2*function*jacobian_b**2/jacobian**3)
    coefficient = radius*(radius-parameter)
    coefficient_b = displacement*(2*radius-parameter)
    spatial_b = system.reference_weight*(coefficient_b/jacobian-coefficient*jacobian_b/jacobian**2)
    spatial_bb = system.reference_weight*(2*displacement**2/jacobian-2*coefficient_b*jacobian_b/jacobian**2
        +2*coefficient*jacobian_b**2/jacobian**3)
    nodal_radius,nodal_jacobian,nodal_displacement = system.mapping(system.radii,position)
    nodal_jacobian_b = np.where(system.radii<system.anchor,1/(system.anchor-inner),-1/(outer-system.anchor))
    nodal = nodal_radius*(nodal_radius-parameter)
    nodal_b = nodal_displacement*(2*nodal_radius-parameter)
    nodal_first = nodal_b/nodal_jacobian-nodal*nodal_jacobian_b/nodal_jacobian**2
    nodal_second = 2*nodal_displacement**2/nodal_jacobian-2*nodal_b*nodal_jacobian_b/nodal_jacobian**2
    nodal_second += 2*nodal*nodal_jacobian_b**2/nodal_jacobian**3
    gram_b = np.asarray(system.sampling @ nodal_first)/system.gram_spacing
    gram_bb = np.asarray(system.sampling @ nodal_second)/system.gram_spacing
    shape = basis_matrix(system,system.reference_shape)
    radial = basis_matrix(system,system.reference_radial)
    derivatives = []
    for temporal,transport,square,spatial,gram in [(temporal_b,transport_b,square_b,spatial_b,gram_b),
        (temporal_bb,transport_bb,square_bb,spatial_bb,gram_bb)]:
        derivatives.append(dict(mass=(shape.T @ diags(temporal) @ shape).toarray(),
            transport=(shape.T @ diags(transport) @ radial).toarray(),
            transport_square=(radial.T @ diags(square) @ radial).toarray(),
            stiffness=(radial.T @ diags(spatial) @ radial+system.lifted.T @ diags(gram) @ system.lifted).toarray()))
    return derivatives


def second_frame(frame, mass_bb, stiffness_bb):
    vectors,connection = frame['vectors'],frame['connection']
    values,within = frame['values'],frame['within']
    mass_b = frame['mass_b_modal']
    stiffness_b = frame['stiffness_b_modal']
    mass_second = vectors.T @ mass_bb @ vectors
    stiffness_second = vectors.T @ stiffness_bb @ vectors
    block_b = frame['block_stiffness_b']
    forcing = stiffness_second+2*stiffness_b @ connection-mass_second*values[None,:]
    forcing -= 2*(mass_b @ connection)*values[None,:]+2*(mass_b+connection) @ block_b
    normalization_second = -2*connection.T @ connection-2*connection.T @ mass_b-2*mass_b @ connection-mass_second
    second_connection = normalization_second/2
    gaps = values[None,:]-values[:,None]
    second_connection[~within] = forcing[~within]/gaps[~within]
    block_second = forcing+values[:,None]*second_connection-second_connection*values[None,:]
    return dict(vectors_bb=vectors @ second_connection,second_connection=second_connection,
        block_stiffness_bb=block_second,normalization_second=normalization_second)


def curved_system_frame(system, position, relative_gap=1e-6):
    frame = system_frame(system,position,relative_gap)
    first,second = analytic_matrix_derivatives(system,position)
    frame.update(second_frame(frame,second['mass'],second['stiffness']))
    vectors,vectors_b,vectors_bb = frame['vectors'],frame['vectors_b'],frame['vectors_bb']
    mass,transport = frame['matrices']['mass'],frame['matrices']['transport']
    transport_b = vectors_b.T @ mass @ vectors_b+vectors.T @ first['mass'] @ vectors_b+vectors.T @ mass @ vectors_bb
    transport_b += vectors_b.T @ transport @ vectors+vectors.T @ first['transport'] @ vectors+vectors.T @ transport @ vectors_b
    frame.update(analytic_first=first,analytic_second=second,modal_transport_b=transport_b)
    return frame

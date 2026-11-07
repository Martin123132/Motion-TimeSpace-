from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_moving_Legendre_current_20260921 import samples,wave_data,dust_data
from annular_joint_first_tangent_20260922 import ZeroTangent
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from scipy.sparse import coo_matrix
from time import perf_counter
import numpy as np


def zero_rate_system(action, spatial_order, material_order, deadline, progress):
    if np.any(action.velocity) or np.any(action.rate_polynomial):
        raise ValueError('Time-symmetric slice required')
    tangent = ZeroTangent()
    node_count, label_count = len(action.knots), len(action.source)
    component_count = node_count+1
    cell_count = len(action.mesh['elements'])
    field_blocks = np.zeros((cell_count, 3, 3, label_count, label_count))
    cross_blocks = np.zeros((node_count, label_count, label_count))
    source_block = np.zeros((label_count, label_count))
    dust_block = np.zeros_like(source_block)
    momentum = np.zeros((label_count, component_count))
    convection = np.zeros((2, label_count, component_count))
    points, weights = np.polynomial.legendre.leggauss(material_order)
    points, weights = points/2, weights/2
    weights *= 6*(points+.5)*(.5-points)
    for index, (label, weight) in enumerate(zip(points, weights)):
        if perf_counter() > deadline:
            raise RuntimeError('Saved boundary during exact-clock Hessian assembly.')
        row = samples(action, label, spatial_order)
        wave = wave_data(row, tangent)
        dust = dust_data(action, row['source'], row['velocity'], tangent)
        quadrature, geometry = row['quadrature'], row['geometry']
        measure, indices, shape = quadrature['measure'], quadrature['indices'], row['shape']
        kinetic, motion, temporal = geometry['kinetic'], row['motion'], row['temporal']
        cardinal = row['cardinal']
        outer = weight*np.outer(cardinal, cardinal)
        for first in range(3):
            for second in range(3):
                cell_values = np.bincount(quadrature['cells'],
                    weights=measure*kinetic*shape[:, first]*shape[:, second], minlength=cell_count)
                field_blocks[:, first, second] += cell_values[:, None, None]*outer
        cross_values = np.zeros(node_count)
        np.add.at(cross_values, indices.ravel(), (measure[:, None]*kinetic[:, None]*motion[:, None]*shape).ravel())
        cross_blocks += cross_values[:, None, None]*outer
        source_block += (measure @ (kinetic*motion**2)+dust['inertia'])*outer
        dust_block += dust['inertia']*outer
        field_values = np.zeros(node_count)
        np.add.at(field_values, indices.ravel(), (measure[:, None]*kinetic[:, None]*temporal[:, None]*shape).ravel())
        source_value = measure @ (kinetic*temporal*motion)+dust['momentum']
        momentum += weight*np.outer(cardinal, np.r_[field_values, source_value])
        for estimate in range(2):
            field_values = np.zeros(node_count)
            np.add.at(field_values, indices.ravel(),
                (measure[:, None]*wave['momentum_rate'][estimate, :, None]*shape).ravel())
            source_value = measure @ (wave['momentum_rate'][estimate]*motion+kinetic*temporal*row['motion_rate'])
            source_value += dust['momentum_rate'][estimate]
            convection[estimate] += weight*np.outer(cardinal, np.r_[field_values, source_value])
        if index%8 == 7:
            progress('Hessian-label-'+str(index+1))
    elements = np.asarray(action.mesh['elements'])
    row_nodes = np.broadcast_to(elements[:, :, None, None, None], field_blocks.shape)
    column_nodes = np.broadcast_to(elements[:, None, :, None, None], field_blocks.shape)
    label_rows = np.arange(label_count)[None, None, None, :, None]
    label_columns = np.arange(label_count)[None, None, None, None, :]
    field_rows = np.broadcast_to(row_nodes+component_count*label_rows, field_blocks.shape)
    field_columns = np.broadcast_to(column_nodes+component_count*label_columns, field_blocks.shape)
    selected = (row_nodes>=0)&(column_nodes>=0)
    cross_rows = np.broadcast_to(np.arange(node_count)[:, None, None]+component_count*np.arange(label_count)[None, :, None], cross_blocks.shape)
    cross_columns = np.broadcast_to(node_count+component_count*np.arange(label_count)[None, None, :], cross_blocks.shape)
    source_indices = node_count+component_count*np.arange(label_count)
    rows = np.r_[field_rows[selected], cross_rows.ravel(), cross_columns.ravel(), np.repeat(source_indices, label_count)]
    columns = np.r_[field_columns[selected], cross_columns.ravel(), cross_rows.ravel(), np.tile(source_indices, label_count)]
    values = np.r_[field_blocks[selected], cross_blocks.ravel(), cross_blocks.ravel(), source_block.ravel()]
    matrix = coo_matrix((values, (rows, columns)), shape=(label_count*component_count,)*2).tocsr()
    matrix.eliminate_zeros()
    inverse = BandedSourceInverse(matrix, (label_count, component_count))
    action_result = action.momentum_and_force(spatial_order, material_order, deadline)
    native_force = action_result['bulk']+action_result['dust']
    forcing = native_force[None]-convection
    acceleration = inverse.solve(forcing.reshape(2, -1).T).T.reshape(forcing.shape)
    return dict(matrix=matrix, inverse=inverse, momentum=momentum, convection=convection,
        force=native_force, fixed_reference_gram=action_result['gram'], forcing=forcing, acceleration=acceleration, dust_block=dust_block,
        action_momentum=action_result['momentum'])


def endpoint_traction(action,order):
    result = np.zeros((len(action.source),len(action.knots)+1))
    points,weights = np.polynomial.legendre.leggauss(order)
    points,weights = points/2,weights/2
    weights *= 6*(points+.5)*(.5-points)
    endpoints = np.array([float(action.edges[0]),float(action.edges[-1])])
    nodes = np.array([int(np.argmin(action.knots)),int(np.argmax(action.knots))])
    for label,weight in zip(points,weights):
        cardinal = np.asarray(action.cardinal(label)).ravel()
        source = float(cardinal@action.source)
        geometry = action.geometry(endpoints,source,label)
        gradient = np.einsum('cpl,l->cp',action.gradient[[0,-1]],cardinal)
        slope = np.array([gradient[0,0],gradient[1].sum()])
        load = geometry['gradient']*slope*np.array([1,-1])
        result[:,nodes] += weight*cardinal[:,None]*load[None,:]
    return result


def direct_momentum_jacobian(action,direction,spatial_order,material_order,deadline):
    result = np.zeros_like(direction,dtype=complex)
    step = 1e-20j
    points,weights = np.polynomial.legendre.leggauss(material_order)
    points,weights = points/2,weights/2
    weights *= 6*(points+.5)*(.5-points)
    for label,weight in zip(points,weights):
        if perf_counter()>deadline:
            raise RuntimeError('Safe momentum-oracle boundary')
        row = samples(action,label,spatial_order)
        quadrature,geometry,cardinal = row['quadrature'],row['geometry'],row['cardinal']
        velocity = step*(cardinal@direction[:,-1])
        nodal_rate = step*(cardinal@direction[:,:-1])
        field_rate = np.sum(row['shape']*nodal_rate[quadrature['indices']],axis=1)
        temporal = field_rate+velocity*row['motion']
        integrand = quadrature['measure']*geometry['kinetic']*temporal
        field = np.zeros(len(action.knots),dtype=complex)
        np.add.at(field,quadrature['indices'].ravel(),(integrand[:,None]*row['shape']).ravel())
        metric_value = action.solver.values(action.solution,np.array([row['source']]))[0][:,0]
        lapse,metric = np.exp(metric_value[1]),1-2*metric_value[0]/row['source']
        source = integrand@row['motion']+action.owner.source_mass*velocity/(metric*np.sqrt(lapse**2-velocity**2/metric))
        result += weight*np.outer(cardinal,np.r_[field,source])
    return result.imag/step.imag


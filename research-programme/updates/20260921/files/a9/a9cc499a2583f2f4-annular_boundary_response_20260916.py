import numpy as np
from fractions import Fraction
from scipy.sparse import coo_matrix, diags


def basis_matrix(system, values):
    indices = system.reference_indices
    rows = np.repeat(np.arange(len(indices)), indices.shape[1])
    return coo_matrix((values.ravel(), (rows, indices.ravel())),
                     shape=(len(indices), system.count)).tocsr()


def field_matrices(system, position):
    radius, jacobian, displacement = system.mapping(system.reference_radius, position)
    shape = basis_matrix(system, system.reference_shape)
    radial = basis_matrix(system, system.reference_radial)
    motion = diags(-displacement/jacobian) @ radial
    coefficient = system.coefficient(0., radius)
    temporal = system.reference_weight*jacobian*radius**4/coefficient
    spatial = system.reference_weight*coefficient/jacobian
    nodal_radius, nodal_jacobian, unused = system.mapping(system.radii, position)
    gram_weights = np.asarray(system.sampling @ (system.coefficient(0., nodal_radius)/nodal_jacobian))/system.gram_spacing
    mass = shape.T @ diags(temporal) @ shape
    transport = shape.T @ diags(temporal) @ motion
    transport_square = motion.T @ diags(temporal) @ motion
    bulk = radial.T @ diags(spatial) @ radial
    gram = system.lifted.T @ diags(gram_weights) @ system.lifted
    return dict(mass=mass.tocsr(), transport=transport.tocsr(), transport_square=transport_square.tocsr(),
                stiffness=(bulk+gram).tocsr(), bulk=bulk.tocsr(), gram=gram.tocsr(), gram_weights=gram_weights)


def matrix_derivatives(system, position):
    step = 1e-24
    moved = field_matrices(system, position+1j*step)
    return {name: moved[name].imag/step for name in ['mass', 'transport', 'transport_square', 'stiffness']}


def nested_coordinates(coarse, fine):
    ideal_nodes = [Fraction(float(value)) for value in fine.radii]
    for element, free_index in enumerate(fine.element_indices[:, 1]):
        ideal_nodes[free_index] = (Fraction(float(fine.edges[element]))+Fraction(float(fine.edges[element+1])))/2
    rows, columns, values = [], [], []
    for free_index, node in enumerate(ideal_nodes):
        element = min(max(np.searchsorted(coarse.edges, float(node), side='right')-1, 0), len(coarse.edges)-2)
        left, right = Fraction(float(coarse.edges[element])), Fraction(float(coarse.edges[element+1]))
        fraction = (node-left)/(right-left)
        shapes = [(1-fraction)*(1-2*fraction), 4*fraction*(1-fraction), fraction*(2*fraction-1)]
        for column, value in zip(coarse.element_indices[element], shapes):
            if column >= 0:
                rows.append(free_index)
                columns.append(column)
                values.append(float(value))
    embedding = coo_matrix((values, (rows, columns)), shape=(fine.count, coarse.count)).tocsr()
    retained = np.array([int(np.argmin(abs(fine.radii-node))) for node in coarse.radii])
    if len(np.unique(retained)) != coarse.count or np.max(abs(fine.radii[retained]-coarse.radii)) > 2e-14:
        raise ValueError('The proposed hierarchical split does not retain the original nodes.')
    new = np.setdiff1d(np.arange(fine.count), retained)
    bubbles = coo_matrix((np.ones(len(new)), (new, np.arange(len(new)))), shape=(fine.count, len(new))).tocsr()
    return embedding, bubbles, retained, new


def split_vector(vector, embedding, retained, new):
    coarse = vector[retained]
    detail = (vector-embedding @ coarse)[new]
    return coarse, detail


def blocks(matrix, embedding, bubbles):
    return dict(coarse=(embedding.T @ matrix @ embedding).tocsr(),
                coupling=(bubbles.T @ matrix @ embedding).toarray(),
                local=(bubbles.T @ matrix @ bubbles).toarray())

from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_primitive_geometry_20260918 import PrimitiveP2System
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_source_fitted_action_20260915 import SourceFittedAction
from scipy.sparse import coo_matrix, csr_matrix
from scipy.linalg import eigvalsh, solve_banded
import numpy as np


class GradedSourceAction(LocallyRefinedSourceAction):
    def __init__(self, base_count, gram, order=32, source_cap=4e-5):
        if not np.isfinite(source_cap) or source_cap <= 0:
            raise ValueError('The source-cell cap must be finite and positive.')
        super().__init__(base_count, gram, order=order, background_mass=.7, source_splits=8)
        linear = SourceFittedAction(base_count, gram, order, .7, self.anchor)
        self.source_cap = source_cap
        self.source_bisections = [0, 0]
        for side in [0, 1]:
            for unused in range(30):
                source = int(np.searchsorted(self.edges, self.anchor))
                element = source-1 if side == 0 else source
                lower, upper = self.edges[element:element+2]
                if upper-lower <= source_cap:
                    break
                self.edges = np.sort(np.append(self.edges, (lower+upper)/2))
                self.source_bisections[side] += 1
            else:
                raise RuntimeError('Source grading exceeded thirty bisections.')
        full_nodes = np.sort(np.concatenate([self.edges, (self.edges[:-1]+self.edges[1:])/2]))
        free = full_nodes != self.anchor
        self.radii, self.count = full_nodes[free], int(np.sum(free))
        full_to_free = np.full(len(full_nodes), -1, dtype=int)
        full_to_free[free] = np.arange(self.count)
        element_nodes = np.column_stack([np.arange(0, len(full_nodes)-2, 2),
            np.arange(1, len(full_nodes)-1, 2), np.arange(2, len(full_nodes), 2)])
        self.element_indices = full_to_free[element_nodes]
        lengths = np.diff(self.edges)
        self.reference_radius = (self.edges[:-1, None]+lengths[:, None]*self.fractions).ravel()
        self.reference_weight = (lengths[:, None]*self.weights).ravel()
        self.reference_indices, self.reference_shape, self.reference_radial = self.features_quadratic(self.reference_radius)
        vertices = np.searchsorted(self.radii, self.base_radii)
        original, sampling = linear.original.tocoo(), linear.sampling.tocoo()
        self.original = coo_matrix((original.data, (original.row, vertices[original.col])),
            shape=(original.shape[0], self.count)).tocsr()
        self.sampling = coo_matrix((sampling.data, (sampling.row, vertices[sampling.col])),
            shape=(sampling.shape[0], self.count)).tocsr()
        self.jump = np.zeros(self.count)
        source = int(np.searchsorted(self.edges, self.anchor))
        for element, local, sign in [(source-1, np.array([1., -4., 3.]), -1.),
                (source, np.array([-3., 4., -1.]), 1.)]:
            indices = self.element_indices[element]
            selected = indices >= 0
            np.add.at(self.jump, indices[selected], sign*local[selected]/lengths[element])
        hinge = np.maximum(self.radii-self.anchor, 0.)
        self.lifted_hinge = self.original @ hinge
        self.lifted = self.original-csr_matrix(self.lifted_hinge[:, None]) @ csr_matrix(self.jump[None, :])
        cells, shapes, unused, unused2 = linear.features(self.radii, self.anchor)
        self.linear_embedding = coo_matrix((shapes.ravel(), (np.repeat(np.arange(self.count), 2),
            np.column_stack([cells, cells+1]).ravel())), shape=(self.count, base_count)).tocsr()


class GradedP2System(PrimitiveP2System):
    def __init__(self, base_count, gram, source_cap=4e-5, action_order=32):
        super().__init__(base_count, gram, layer_degree=14, radial_degree=18,
            action_order=action_order, label_order=20)
        self.model = GradedSourceAction(base_count, gram, order=action_order, source_cap=source_cap)
        self.count = self.model.count


def nested_embedding(coarse, fine):
    indices, shape, unused = coarse.features_quadratic(fine.radii)
    return coo_matrix((shape.ravel(), (np.repeat(np.arange(fine.count), 3), indices.ravel())),
        shape=(fine.count, coarse.count)).tocsr()


def scalar_pencil(layer, values):
    data = layer.evaluate(0., values, np.zeros_like(values))
    indices, radial = layer.reference_indices, layer.reference_radial
    radius, jacobian, unused = layer.mapping(layer.reference_radius, values[-1])
    weights = layer.reference_weight*layer.coefficient(0., radius)/jacobian
    stiffness = np.zeros((layer.count, layer.count))
    for first in range(3):
        for second in range(3):
            np.add.at(stiffness, (indices[:, first], indices[:, second]), weights*radial[:, first]*radial[:, second])
    nodes, jacobian, unused = layer.mapping(layer.radii, values[-1])
    factor_weights = np.asarray(layer.sampling @ (layer.coefficient(0., nodes)/jacobian))/layer.gram_spacing
    lifted = layer.lifted.toarray()
    stiffness += lifted.T @ (factor_weights[:, None]*lifted)
    mass = np.zeros_like(stiffness)
    for column in range(layer.count):
        for row in range(max(0, column-2), min(layer.count, column+3)):
            mass[row, column] = data['mass_bands'][2+row-column, column]
    return mass, stiffness


def frequency_diagnostic(layer, values):
    mass, stiffness = scalar_pencil(layer, values)
    eigenvalues = eigvalsh(stiffness, mass, check_finite=False)
    probe = .001*np.sin(np.arange(layer.count)+.3)
    tested = np.append(probe, values[-1])
    covector = layer.evaluate(0., tested, np.zeros_like(tested))['scalar_covector']
    frequency = float(np.sqrt(eigenvalues[-1]))
    return dict(minimum_eigenvalue=float(eigenvalues[0]), maximum_angular_frequency=frequency,
        shortest_period=float(2*np.pi/frequency),
        stiffness_action_error=float(max(abs(covector+stiffness @ probe))),
        mode_count=len(eigenvalues))


def force_schur_identity(current):
    layer, values, rates = current.layer, current.coordinates, current.rates
    data = current.data
    moved = current.tangent_layer.evaluate(0., current.changed_coordinates, rates)
    transport = moved['field_momenta'].imag/current.step
    dust_transport = float(moved['material_momentum'].imag/current.step)
    raw_wave = float(layer.source_covector(0., values, rates, wave=True))
    raw_total = float(layer.source_covector(0., values, rates))
    solved = solve_banded((2, 2), data['mass_bands'],
        np.column_stack([data['scalar_covector']-transport[:-1], data['cross']]), check_finite=False)
    radius, jacobian, motion = layer.mapping(layer.reference_radius, values[-1])
    field_motion = -motion*data['field_radial']
    projected = np.sum(layer.reference_shape*solved[:, 1][layer.reference_indices], axis=1)
    weights = layer.reference_weight*jacobian*radius**4/layer.coefficient(0., radius)
    complement = float(weights @ (field_motion-projected)**2)
    raw_complement = float(weights @ field_motion**2-data['cross'] @ solved[:, 1])
    lapse, root = layer.metric(0., values[-1])
    inertia = float(layer.source_mass*lapse**2/(root**2*data['clock']**3))
    free_wave_drive = float(raw_wave-transport[-1]-data['cross'] @ solved[:, 0])
    dust_drive = float(raw_total-raw_wave-dust_transport)
    predicted_acceleration = (dust_drive+free_wave_drive)/(inertia+complement)
    predicted_force = (inertia*free_wave_drive-complement*dust_drive)/(inertia+complement)
    return dict(field_projection_inertia=complement, inertia_subtraction_error=abs(complement-raw_complement),
        dust_inertia=inertia, free_wave_drive=free_wave_drive, dust_drive=dust_drive,
        predicted_source_acceleration=predicted_acceleration,
        predicted_reduced_force=predicted_force, force_identity_error=abs(predicted_force+current.wave_source_euler),
        prescribed_geometry_tangent_already_from_live_canonical_flow=True)

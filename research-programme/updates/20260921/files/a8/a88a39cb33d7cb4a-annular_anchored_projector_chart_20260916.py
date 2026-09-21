import numpy as np
from scipy.linalg import cholesky, eigh, solve_triangular
from annular_boundary_response_20260916 import field_matrices
from annular_moving_spectral_curvature_20260916 import analytic_matrix_derivatives, second_frame
from annular_moving_spectral_frame_20260916 import spectral_clusters, close_selection_under_clusters


def split_frame(mass, stiffness, first, second, retained, gap_floor):
    values, vectors = eigh(stiffness, mass)
    if values[0] <= 0:
        raise ValueError('Positive original field spectrum required.')
    selected = np.zeros(len(values), dtype=bool)
    selected[retained] = True
    within = selected[:, None] == selected[None, :]
    gaps = values[None, :] - values[:, None]
    scale = np.maximum(1., np.maximum(abs(values[:, None]), abs(values[None, :])))
    separation = float(np.min(abs(gaps[~within])/scale[~within])) if np.any(~within) else 1.
    if separation <= gap_floor:
        raise ValueError('Retained/omitted spectral gap closed: stop, do not relabel or discard a cluster.')
    mass_b = vectors.T @ first['mass'] @ vectors
    stiffness_b = vectors.T @ first['stiffness'] @ vectors
    connection = -mass_b/2
    forcing = stiffness_b-mass_b*values[None, :]
    connection[~within] = forcing[~within]/gaps[~within]
    block_b = stiffness_b+connection.T*values[None, :]+values[:, None]*connection
    frame = dict(values=values, vectors=vectors, connection=connection, within=within,
        mass_b_modal=mass_b, stiffness_b_modal=stiffness_b, block_stiffness_b=block_b,
        vectors_b=vectors @ connection, relative_external_gap=separation)
    frame.update(second_frame(frame, second['mass'], second['stiffness']))
    return frame


def lower_half(matrix):
    result = np.tril(matrix)
    result[np.diag_indices_from(result)] *= .5
    return result


def normalized_jet(raw, raw_b, raw_bb, mass, mass_b, mass_bb):
    gram = raw.T @ mass @ raw
    gram_b = raw_b.T @ mass @ raw+raw.T @ mass_b @ raw+raw.T @ mass @ raw_b
    gram_bb = raw_bb.T @ mass @ raw+raw.T @ mass @ raw_bb+2*raw_b.T @ mass @ raw_b
    gram_bb += 2*raw_b.T @ mass_b @ raw+2*raw.T @ mass_b @ raw_b+raw.T @ mass_bb @ raw
    gram = (gram+gram.T)/2
    eigenvalues = eigh(gram, eigvals_only=True)
    if eigenvalues[0] < .25 or eigenvalues[-1]/eigenvalues[0] > 100.:
        raise ValueError('Anchored chart lost overlap; stop for an explicit chart transition.')
    lower = cholesky(gram, lower=True)
    inverse = solve_triangular(lower, np.eye(len(lower)), lower=True)
    lower_b = lower @ lower_half(inverse @ gram_b @ inverse.T)
    lower_bb = lower @ lower_half(inverse @ (gram_bb-2*lower_b @ lower_b.T) @ inverse.T)
    factor = inverse.T
    factor_b = -factor @ lower_b.T @ factor
    factor_bb = 2*factor @ lower_b.T @ factor @ lower_b.T @ factor-factor @ lower_bb.T @ factor
    return dict(basis=raw @ factor, basis_b=raw_b @ factor+raw @ factor_b,
        basis_bb=raw_bb @ factor+2*raw_b @ factor_b+raw @ factor_bb,
        overlap_min=float(eigenvalues[0]), overlap_max=float(eigenvalues[-1]))


def material_terms(system, position, speed):
    geometry = 1-2*system.background_mass/position
    geometry_b = 2*system.background_mass/position**2
    clock_square = geometry-speed**2/geometry
    if np.real(clock_square) <= 0:
        raise ValueError('Source is no longer timelike.')
    clock = np.sqrt(clock_square)
    clock_b = geometry_b*(1+speed**2/geometry**2)/(2*clock)
    momentum_b = -system.source_mass*speed*(geometry_b/(geometry**2*clock)+clock_b/(geometry*clock**2))
    return dict(clock=clock, action=-system.source_mass*clock,
        momentum=system.source_mass*speed/(geometry*clock), inertia=system.source_mass/clock**3,
        covector=-system.source_mass*clock_b, momentum_b=momentum_b)


class AnchoredProjectorChart:
    def __init__(self, system, retained, cluster_gap=1e-3, gap_floor=1e-4):
        self.system = system
        self.anchor = system.anchor
        self.gap_floor = gap_floor
        matrices = field_matrices(system, self.anchor)
        values, vectors = eigh(matrices['stiffness'].toarray(), matrices['mass'].toarray())
        self.retained = close_selection_under_clusters(retained, spectral_clusters(values, cluster_gap))
        self.omitted = np.setdiff1d(np.arange(system.count), self.retained)
        self.anchor_basis = vectors[:, self.retained]
        self.count = len(self.retained)
        self.last_position = None
        self.last_data = None
        self.evaluations = 0
        self.minimum_gap = 1.
        self.minimum_overlap = 1.

    def at(self, position):
        if np.iscomplexobj(position):
            raise ValueError('Use the qualified local jet for complex-step tests, not Hermitian eigensolvers.')
        position = float(position)
        if position == self.last_position:
            return self.last_data
        sparse = field_matrices(self.system, position)
        matrices = {name: sparse[name].toarray() for name in ['mass', 'stiffness', 'transport', 'transport_square']}
        first, second = analytic_matrix_derivatives(self.system, position)
        mass, stiffness = matrices['mass'], matrices['stiffness']
        frame = split_frame(mass, stiffness, first, second, self.retained, self.gap_floor)
        selected = frame['vectors'][:, self.retained]
        selected_b = frame['vectors_b'][:, self.retained]
        selected_bb = frame['vectors_bb'][:, self.retained]
        symmetric = selected @ selected.T
        symmetric_b = selected_b @ selected.T+selected @ selected_b.T
        symmetric_bb = selected_bb @ selected.T+2*selected_b @ selected_b.T+selected @ selected_bb.T
        projector = symmetric @ mass
        projector_b = symmetric_b @ mass+symmetric @ first['mass']
        projector_bb = symmetric_bb @ mass+2*symmetric_b @ first['mass']+symmetric @ second['mass']
        normalized = normalized_jet(projector @ self.anchor_basis, projector_b @ self.anchor_basis,
            projector_bb @ self.anchor_basis, mass, first['mass'], second['mass'])
        basis, basis_b, basis_bb = [normalized[name] for name in ['basis', 'basis_b', 'basis_bb']]
        transport, square = matrices['transport'], matrices['transport_square']
        effective_transport = basis.T @ mass @ basis_b+basis.T @ transport @ basis
        effective_square = basis_b.T @ mass @ basis_b+basis_b.T @ transport @ basis
        effective_square += basis.T @ transport.T @ basis_b+basis.T @ square @ basis
        effective_stiffness = basis.T @ stiffness @ basis
        transport_b = basis_b.T @ mass @ basis_b+basis.T @ first['mass'] @ basis_b+basis.T @ mass @ basis_bb
        transport_b += basis_b.T @ transport @ basis+basis.T @ first['transport'] @ basis+basis.T @ transport @ basis_b
        square_b = basis_bb.T @ mass @ basis_b+basis_b.T @ first['mass'] @ basis_b+basis_b.T @ mass @ basis_bb
        mixed_b = basis_bb.T @ transport @ basis+basis_b.T @ first['transport'] @ basis+basis_b.T @ transport @ basis_b
        square_b += mixed_b+mixed_b.T+basis_b.T @ square @ basis+basis.T @ first['transport_square'] @ basis+basis.T @ square @ basis_b
        stiffness_b = basis_b.T @ stiffness @ basis+basis.T @ first['stiffness'] @ basis+basis.T @ stiffness @ basis_b
        data = dict(**normalized, matrices=matrices, first=first, second=second,
            transport=effective_transport, square=effective_square, stiffness=effective_stiffness,
            transport_b=transport_b, square_b=square_b, stiffness_b=stiffness_b,
            projector=projector, projector_b=projector_b, projector_bb=projector_bb,
            complement=frame['vectors'][:, self.omitted], values=frame['values'],
            relative_external_gap=frame['relative_external_gap'])
        self.last_position, self.last_data = position, data
        self.evaluations += 1
        self.minimum_gap = min(self.minimum_gap, data['relative_external_gap'])
        self.minimum_overlap = min(self.minimum_overlap, data['overlap_min'])
        return data

    def dynamics(self, coordinates, rates):
        modal, position = coordinates[:-1], coordinates[-1]
        velocity, speed = rates[:-1], rates[-1]
        data = self.at(position)
        transport, square, stiffness = data['transport'], data['square'], data['stiffness']
        material = material_terms(self.system, position, speed)
        field_rhs = -speed*(transport-transport.T) @ velocity-stiffness @ modal
        field_rhs -= speed**2*(data['transport_b']-square) @ modal
        source_rhs = -velocity @ transport @ velocity-2*speed*velocity @ square @ modal
        source_rhs -= speed**2*(modal @ data['square_b'] @ modal)/2+modal @ data['stiffness_b'] @ modal/2
        source_rhs += material['covector']-speed*material['momentum_b']
        cross = transport @ modal
        inertia = material['inertia']+modal @ square @ modal
        schur = inertia-cross @ cross
        if schur <= 0:
            raise ValueError('Reduced kinetic Schur complement nonpositive.')
        acceleration = (source_rhs-cross @ field_rhs)/schur
        return dict(acceleration=np.append(field_rhs-cross*acceleration, acceleration),
            field_rhs=field_rhs, source_rhs=source_rhs, cross=cross, inertia=inertia, schur=schur,
            material=material, chart=data)

    def rhs(self, instant, state):
        coordinates, rates = np.split(state[:-1], 2)
        data = self.dynamics(coordinates, rates)
        return np.concatenate([rates, data['acceleration'], [data['material']['clock']]])

    def lift(self, coordinates, rates, acceleration=None):
        data = self.at(coordinates[-1])
        modal, velocity, speed = coordinates[:-1], rates[:-1], rates[-1]
        basis, basis_b, basis_bb = data['basis'], data['basis_b'], data['basis_bb']
        physical_coordinates = np.append(basis @ modal, coordinates[-1])
        physical_rates = np.append(basis @ velocity+speed*basis_b @ modal, speed)
        if acceleration is None:
            return physical_coordinates, physical_rates
        physical_acceleration = basis @ acceleration[:-1]+2*speed*basis_b @ velocity
        physical_acceleration += speed**2*basis_bb @ modal+basis_b @ modal*acceleration[-1]
        return physical_coordinates, physical_rates, np.append(physical_acceleration, acceleration[-1])

    def prepare(self, original_state):
        coordinates, rates = np.split(original_state[:-1], 2)
        data = self.at(coordinates[-1])
        original = self.system.evaluate(0., coordinates, rates)
        modal = data['basis'].T @ data['matrices']['mass'] @ coordinates[:-1]
        momentum = data['basis'].T @ original['momenta'][:-1]
        velocity = momentum-rates[-1]*data['transport'] @ modal
        return np.concatenate([modal, [coordinates[-1]], velocity, [rates[-1], original_state[-1]]])


def jet_pullback(chart, base_position, coordinates, rates):
    data = chart.at(base_position)
    displacement = coordinates[-1]-base_position
    basis = data['basis']+displacement*data['basis_b']+displacement**2*data['basis_bb']/2
    basis_b = data['basis_b']+displacement*data['basis_bb']
    physical_coordinates = np.append(basis @ coordinates[:-1], coordinates[-1])
    physical_rates = np.append(basis @ rates[:-1]+rates[-1]*basis_b @ coordinates[:-1], rates[-1])
    original = chart.system.evaluate(0., physical_coordinates, physical_rates)
    momentum = np.append(basis.T @ original['momenta'][:-1],
        original['momenta'][-1]+original['momenta'][:-1] @ basis_b @ coordinates[:-1])
    return dict(action=original['action'], momenta=momentum, original=original,
        physical_coordinates=physical_coordinates, physical_rates=physical_rates)


def omission_diagnostic(chart, coordinates, rates):
    dynamics = chart.dynamics(coordinates, rates)
    data, material = dynamics['chart'], dynamics['material']
    physical, physical_rate, lifted_acceleration = chart.lift(coordinates, rates, dynamics['acceleration'])
    original = chart.system.evaluate(0., physical, physical_rate)
    original_acceleration = chart.system.acceleration(0., physical, physical_rate)
    difference = original_acceleration-lifted_acceleration
    mass = data['matrices']['mass']
    field_residual = -mass @ difference[:-1]-original['cross']*difference[-1]
    omitted_drive = -data['complement'].T @ field_residual
    omitted_cross = data['complement'].T @ (mass @ data['basis_b'] @ coordinates[:-1]+original['cross'])
    full_schur = dynamics['schur']-omitted_cross @ omitted_cross
    if full_schur <= 0:
        raise ValueError('Full kinetic Schur complement nonpositive.')
    predicted_force = -material['inertia']*(omitted_cross @ omitted_drive)/full_schur
    actual_force = material['inertia']*difference[-1]
    bound = material['inertia']*np.linalg.norm(omitted_cross)*np.linalg.norm(omitted_drive)/full_schur
    defect_square = difference[:-1] @ mass @ difference[:-1]
    defect_square += 2*difference[-1]*original['cross'] @ difference[:-1]+original['source_inertia']*difference[-1]**2
    predicted_defect_square = omitted_drive @ omitted_drive+(omitted_cross @ omitted_drive)**2/full_schur
    return dict(same_state_force=float(actual_force), same_state_force_predicted=float(predicted_force),
        same_state_force_bound=float(bound), omitted_drive_norm=float(np.linalg.norm(omitted_drive)),
        kinetic_defect_norm=float(np.sqrt(max(0., defect_square))), kinetic_defect_square=float(defect_square),
        predicted_defect_square=float(predicted_defect_square), full_schur=float(full_schur),
        retained_EL_residual=float(np.linalg.norm(data['basis'].T @ field_residual)),
        original_acceleration=original_acceleration, reduced_acceleration=dynamics['acceleration'],
        source_connection_momentum=float(original['momenta'][:-1] @ data['basis_b'] @ coordinates[:-1]))

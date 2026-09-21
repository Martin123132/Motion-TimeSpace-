import numpy as np
from annular_live_continuum_characteristics_20260915 import ContinuumMaterial, ContinuumGeometry, LiveContinuumCharacteristics
from annular_live_continuum_fast_20260915 import FactoredContinuumDensity


class BarycentricDensity(FactoredContinuumDensity):
    def __init__(self, material, radius, order=None):
        super().__init__(material, radius, order)
        owner = material.owner
        barycentric = (-1.)**np.arange(owner.count)
        barycentric[[0, -1]] *= .5
        self.spatial_interpolation, self.label_interpolation = [], []
        for side in [0, 1]:
            separation = self.mapped[side][:, None]-owner.spatial_rule.points[None, :]
            exact = separation == 0
            separation[exact] = 1.
            interpolation = barycentric[None, :]/separation
            interpolation /= interpolation.sum(axis=1)[:, None]
            rows = np.any(exact, axis=1)
            interpolation[rows] = exact[rows]
            self.spatial_interpolation.append(interpolation)
            label_interpolation = material.interpolation(self.labels[self.selected[side]])
            self.label_interpolation.append(label_interpolation)
            endpoint = -1 if side == 0 else 0
            self.boundary_operators[side] = label_interpolation*interpolation[:, endpoint, None]

    def update(self, fields):
        if self.baseline is None:
            self.baseline = np.zeros((2, len(self.labels)))
            for side in [0, 1]:
                for sign in [0, 1]:
                    interpolated = self.label_interpolation[side] @ fields[:, side, sign]
                    self.baseline[sign, self.selected[side]] = np.sum(interpolated*self.spatial_interpolation[side], axis=1)
            self.initial_boundary = [fields[:, 0, 0, -1].copy(), fields[:, 1, 1, 0].copy()]
        super().update(fields)


class BarycentricGeometry(ContinuumGeometry):
    def __init__(self, owner, material, free_fields):
        self.owner, self.material, self.rule = owner, material, owner.radial_rule
        outer_edges = np.array([owner.inner-owner.width/2, owner.inner+owner.width/2, owner.outer-owner.width/2, owner.outer+owner.width/2])
        fixed = np.arange(owner.inner+.05, owner.outer, owner.radial_spacing)
        self.edges = np.unique(np.concatenate([outer_edges, fixed, material.source[[0, -1], 0]]))
        self.lengths, self.centers = np.diff(self.edges), (self.edges[:-1]+self.edges[1:])/2
        self.nodes = self.centers[:, None]+self.lengths[:, None]*self.rule.points/2
        self.density = BarycentricDensity(material, self.nodes)
        mass = owner.central_mass+np.zeros_like(self.nodes)
        self.assign_mass(mass)
        for iteration in range(40):
            source_mass = self.evaluate(material.source[:, 0], self.mass_coefficients)
            fields = owner.boundaries(free_fields, material.source, source_mass)
            self.density.update(fields)
            mass_radial, unused = self.density.radial(mass.ravel())
            updated = owner.central_mass+self.integrated(mass_radial)
            error = float(np.max(abs(updated-mass)))
            mass = updated
            self.assign_mass(mass)
            if error < 2e-14:
                break
        else:
            raise RuntimeError('Barycentric continuum radial mass fixed point did not converge.')
        self.fields, self.iterations, self.fixed_point_error = fields, iteration+1, error
        unused, log_lapse_radial = self.density.radial(mass.ravel())
        primitive = self.integrated(log_lapse_radial)
        self.log_lapse_nodes = .5*np.log(1-2*mass[-1, -1]/self.edges[-1])+primitive-primitive[-1, -1]
        self.lapse_coefficients = self.log_lapse_nodes @ self.rule.inverse.T


class BarycentricLiveContinuum(LiveContinuumCharacteristics):
    def solve(self, state):
        fields, source = self.unpack(state)
        return BarycentricGeometry(self, ContinuumMaterial(self, source), fields)

import numpy as np
from annular_live_continuum_characteristics_20260915 import LiveContinuumCharacteristics, ContinuumGeometry, ContinuumMaterial, ContinuumDensity, weight


class FactoredContinuumDensity(ContinuumDensity):
    def __init__(self, material, radius, order=None):
        self.material, self.radius = material, np.asarray(radius).reshape(-1)
        owner = material.owner
        points, weights = np.polynomial.legendre.leggauss(order or owner.label_order)
        labels, label_weights, indices = [], [], []
        source_low, source_high = material.source[[0, -1], 0]
        for index, target in enumerate(self.radius):
            cuts = np.array([(target-owner.inner)/owner.width, (target-owner.outer)/owner.width])
            cuts = cuts[(cuts > -.5) & (cuts < .5)]
            if source_low < target < source_high:
                cuts = np.append(cuts, material.inverse(target))
            cuts = np.unique(np.concatenate([[-.5], cuts, [.5]]))
            for lower, upper in zip(cuts[:-1], cuts[1:]):
                local = (lower+upper)/2+(upper-lower)*points/2
                labels.extend(local)
                label_weights.extend((upper-lower)*weights*weight(local)/2)
                indices.extend([index]*len(points))
        self.labels = np.asarray(labels)
        self.weights, self.indices = np.asarray(label_weights), np.asarray(indices)
        targets = self.radius[self.indices]
        sources = material.values(self.labels)[:, 0]
        inner, outer = owner.inner+owner.width*self.labels, owner.outer+owner.width*self.labels
        self.boundary_operators, self.selected, self.mapped = [], [], []
        for side in [0, 1]:
            selected = (targets >= inner) & (targets <= outer) & ((targets < sources) if side == 0 else (targets >= sources))
            lower, upper = (inner, sources) if side == 0 else (sources, outer)
            mapped = 2*(targets[selected]-lower[selected])/(upper[selected]-lower[selected])-1
            endpoint = -1 if side == 0 else 0
            endpoint_basis = np.polynomial.chebyshev.chebval(mapped, owner.spatial_rule.inverse[:, endpoint])
            self.boundary_operators.append(material.interpolation(self.labels[selected])*endpoint_basis[:, None])
            self.selected.append(selected)
            self.mapped.append(mapped)
        self.source_density, self.source_momentum = np.zeros(len(self.radius)), np.zeros(len(self.radius))
        selected = (self.radius >= source_low) & (self.radius <= source_high)
        source_labels = material.inverse(self.radius[selected])
        self.source_density[selected] = weight(source_labels)/material.jacobian(source_labels)
        self.source_momentum[selected] = material.values(source_labels)[:, 1]
        self.baseline = None

    def update(self, fields):
        owner = self.material.owner
        if self.baseline is None:
            self.baseline = np.zeros((2, len(self.labels)))
            for side in [0, 1]:
                selected = self.selected[side]
                for sign in [0, 1]:
                    coefficients = owner.layer_rule.inverse @ fields[:, side, sign] @ owner.spatial_rule.inverse.T
                    self.baseline[sign, selected] = np.polynomial.chebyshev.chebval2d(2*self.labels[selected], self.mapped[side], coefficients)
            self.initial_boundary = [fields[:, 0, 0, -1].copy(), fields[:, 1, 1, 0].copy()]
        plus, minus = self.baseline.copy()
        plus[self.selected[0]] += self.boundary_operators[0] @ (fields[:, 0, 0, -1]-self.initial_boundary[0])
        minus[self.selected[1]] += self.boundary_operators[1] @ (fields[:, 1, 1, 0]-self.initial_boundary[1])
        self.square = np.bincount(self.indices, weights=self.weights*(plus**2+minus**2)/2, minlength=len(self.radius))
        self.cross = np.bincount(self.indices, weights=self.weights*(plus**2-minus**2)/4, minlength=len(self.radius))


class FactoredContinuumGeometry(ContinuumGeometry):
    def __init__(self, owner, material, free_fields):
        self.owner, self.material, self.rule = owner, material, owner.radial_rule
        outer_edges = np.array([owner.inner-owner.width/2, owner.inner+owner.width/2, owner.outer-owner.width/2, owner.outer+owner.width/2])
        fixed = np.arange(owner.inner+.05, owner.outer, owner.radial_spacing)
        self.edges = np.unique(np.concatenate([outer_edges, fixed, material.source[[0, -1], 0]]))
        self.lengths, self.centers = np.diff(self.edges), (self.edges[:-1]+self.edges[1:])/2
        self.nodes = self.centers[:, None]+self.lengths[:, None]*self.rule.points/2
        self.density = FactoredContinuumDensity(material, self.nodes)
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
            raise RuntimeError('Factored continuum radial mass fixed point did not converge.')
        self.fields, self.iterations, self.fixed_point_error = fields, iteration+1, error
        unused, log_lapse_radial = self.density.radial(mass.ravel())
        primitive = self.integrated(log_lapse_radial)
        self.log_lapse_nodes = .5*np.log(1-2*mass[-1, -1]/self.edges[-1])+primitive-primitive[-1, -1]
        self.lapse_coefficients = self.log_lapse_nodes @ self.rule.inverse.T


class FastLiveContinuum(LiveContinuumCharacteristics):
    def solve(self, state):
        fields, source = self.unpack(state)
        material = ContinuumMaterial(self, source)
        return FactoredContinuumGeometry(self, material, fields)

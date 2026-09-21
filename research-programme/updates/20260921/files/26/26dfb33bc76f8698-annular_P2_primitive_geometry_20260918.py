from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_P2_canonical_v2_20260918 import LiveP2Geometry, P2Material, inverse_momenta
from annular_live_P2_current_20260918 import EvolvingP2System
import numpy as np


class PrimitiveP2Geometry(LiveP2Geometry):
    def solve(self):
        super().solve()
        mass_rhs, lapse_rhs = self.density.rhs(self.mass_nodes.ravel(), self.log_lapse_nodes.ravel())
        self.mass_rhs_coefficients = mass_rhs.reshape(self.nodes.shape) @ self.rule.inverse.T
        self.lapse_rhs_coefficients = lapse_rhs.reshape(self.nodes.shape) @ self.rule.inverse.T
        self.mass_primitive = np.polynomial.chebyshev.chebint(self.mass_rhs_coefficients.T).T*self.lengths[:, None]/2
        self.lapse_primitive = np.polynomial.chebyshev.chebint(self.lapse_rhs_coefficients.T).T*self.lengths[:, None]/2
        self.mass_primitive[:, 0] -= np.polynomial.chebyshev.chebval(-1., self.mass_primitive.T)
        self.lapse_primitive[:, 0] -= np.polynomial.chebyshev.chebval(-1., self.lapse_primitive.T)
        mass_increments = np.polynomial.chebyshev.chebval(1., self.mass_primitive.T)
        lapse_increments = np.polynomial.chebyshev.chebval(1., self.lapse_primitive.T)
        self.mass_left = self.owner.central_mass+np.concatenate([[0.], np.cumsum(mass_increments[:-1])])
        outer_mass = self.owner.central_mass+sum(mass_increments)
        outer_lapse = .5*np.log(1-2*outer_mass/self.edges[-1])
        self.lapse_left = outer_lapse-sum(lapse_increments)+np.concatenate([[0.], np.cumsum(lapse_increments[:-1])])
        represented_mass, represented_lapse, unused, unused2 = self.values(self.nodes.ravel())
        self.dense_output_node_change = float(max(np.max(abs(represented_mass-self.mass_nodes.ravel())),
            np.max(abs(represented_lapse-self.log_lapse_nodes.ravel()))))
        self.mass_nodes = represented_mass.reshape(self.nodes.shape)
        self.log_lapse_nodes = represented_lapse.reshape(self.nodes.shape)
        self.mass_coefficients = self.mass_primitive.copy()
        self.mass_coefficients[:, 0] += self.mass_left
        self.lapse_coefficients = self.lapse_primitive.copy()
        self.lapse_coefficients[:, 0] += self.lapse_left
        self.mass_derivative = self.mass_rhs_coefficients*self.lengths[:, None]/2
        self.lapse_derivative = self.lapse_rhs_coefficients*self.lengths[:, None]/2

    def values(self, radius):
        radius = np.asarray(radius)
        indices = np.clip(np.searchsorted(self.edges, radius.real, side='right')-1, 0, len(self.lengths)-1)
        mapped = 2*(radius-self.centers[indices])/self.lengths[indices]
        mass = self.mass_left[indices]+np.polynomial.chebyshev.chebval(mapped, self.mass_primitive[indices].T, tensor=False)
        log_lapse = self.lapse_left[indices]+np.polynomial.chebyshev.chebval(mapped, self.lapse_primitive[indices].T, tensor=False)
        mass_radial = np.polynomial.chebyshev.chebval(mapped, self.mass_rhs_coefficients[indices].T, tensor=False)
        lapse_radial = np.polynomial.chebyshev.chebval(mapped, self.lapse_rhs_coefficients[indices].T, tensor=False)
        return mass, log_lapse, mass_radial, lapse_radial


class PrimitiveP2System(EvolvingP2System):
    def initial(self, wave=True, deformed=False):
        coordinates, unused, rates, unused2 = super().initial(wave, deformed)
        geometry = PrimitiveP2Geometry(self, P2Material(self, coordinates), rates)
        momenta = np.array([self.layer(label, geometry).evaluate(0., position, velocity)['momenta']
            for label, position, velocity in zip(self.labels, coordinates, rates)])
        return coordinates, momenta, rates, geometry

    def solve(self, coordinates, momenta):
        material = P2Material(self, coordinates)
        rates = np.zeros_like(coordinates)
        geometry = PrimitiveP2Geometry(self, material, rates)
        history = []
        for iteration in range(32):
            updated = np.array([inverse_momenta(self.layer(label, geometry), position, momentum)[0]
                for label, position, momentum in zip(self.labels, coordinates, momenta)])
            error = float(max(abs(updated-rates).ravel()))
            rates = updated
            geometry.density.update(rates)
            geometry.solve()
            history.append(error)
            if error < self.canonical_tolerance:
                break
        else:
            raise RuntimeError('Primitive P2 canonical/radial iteration failed to converge.')
        geometry.canonical_history = history
        return rates, geometry

import numpy as numerical

from annular_canonical_initial_data_20260911 import CanonicalInitialData


class CanonicalInitialNodalData(CanonicalInitialData):
    def seed(self, reactions):
        return numerical.concatenate([self.mass_coeff_seed[1:self.face_count], self.pi_coeff_seed[:self.count], reactions])

    def set_state(self, data):
        mass_coeff = numerical.concatenate([self.mass_coeff_seed[:1], data[:self.face_count - 1], numerical.zeros(self.count - 2)])
        pi_coeff = self.pi_coeff_seed.astype(numerical.result_type(data)).copy()
        pi_coeff[:self.count] = data[self.face_count - 1:self.face_count - 1 + self.count]
        self.mass = mass_coeff[:self.face_count]
        self.mass_q = self.maps['mass_map'] @ mass_coeff
        self.mass_r = self.maps['mass_gradient'] @ mass_coeff
        self.spatial_f = 1 - 2 * self.mass_q / self.radius
        self.node_f = 1 - 2 * (self.basis.face_to_node @ self.mass) / self.basis.radii
        self.link_f = 1 - 2 * (self.link_mass_map @ mass_coeff) / self.links.points
        self.pi = self.pi_map @ pi_coeff
        return mass_coeff, pi_coeff, data[-3:]

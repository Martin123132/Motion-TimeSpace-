import numpy as np
from annular_repaired_live_current_20260915 import LiveTangent


class SparseLiveTangent(LiveTangent):
    def regular_dual_dot(self, layer, coordinates, rates, acceleration, radius):
        def fields(position, velocity):
            cell, shape, radial, motion = layer.features(radius, position[-1])
            scalar = np.column_stack([position[cell], position[cell+1]])
            scalar_rate = np.column_stack([velocity[cell], velocity[cell+1]])
            temporal = np.sum(shape*scalar_rate, axis=1)+np.sum(motion*scalar, axis=1)*velocity[-1]
            return temporal, np.sum(radial*scalar, axis=1)

        temporal, gradient = fields(coordinates, rates)
        step = 1e-24
        moved_temporal, moved_gradient = fields(coordinates.astype(complex)+1j*step*rates,
                                                rates.astype(complex)+1j*step*acceleration)
        temporal_dot, gradient_dot = moved_temporal.imag/step, moved_gradient.imag/step
        lapse, root = self.geometry.metric(radius)
        lapse_dot, root_dot = self.tangent_geometry.derivative(radius)
        coefficient = radius**2*lapse*root
        coefficient_dot = radius**2*(lapse_dot*root+lapse*root_dot)
        dual_dot = -radius**4*temporal*temporal_dot/coefficient**2
        dual_dot += radius**4*temporal**2*coefficient_dot/coefficient**3-gradient*gradient_dot
        return coefficient*dual_dot

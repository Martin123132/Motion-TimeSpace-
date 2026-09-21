import numpy as np

from annular_covariant_joint_preparation_20260912 import JointPreparation


class CanonicalPortPreparation(JointPreparation):
    def evaluate(self, coefficients, surface='quad', inferred_ports=False):
        result = super().evaluate(coefficients, surface, inferred_ports=False)
        nodes = result['fields']['nodes']
        velocity = result['current']['q']
        outward = np.array([-1., 1.])
        rho = np.zeros_like(result['momentum'])
        multiplier = nodes['N'][[0, -1]] / (.1 * np.sqrt(nodes['F'][[0, -1]]))
        rho[[0, -1]] = outward * multiplier * result['mu_nodes'][[0, -1]] / velocity[[0, -1]]
        source_work = -nodes['eta'].T @ (rho * velocity / nodes['N'])
        rate = result['C1_no_ports'] + source_work
        boundary_work = -nodes['eta'][[0, -1]].T @ (outward * result['current']['K']['nodes'][[0, -1]] / nodes['N'][[0, -1]])
        endpoint_defect = result['mu_nodes'][[0, -1]] - result['raw_nodes'][[0, -1]]
        boundary_projection = nodes['eta'][[0, -1]].T @ (outward * endpoint_defect / (.1 * np.sqrt(nodes['F'][[0, -1]])))
        residual = result['residual'].copy()
        residual[-2] = (result['mu_nodes'][0] - self.saved['boundary_velocity'][0]) / .02
        result.update({'rho': rho, 'p_first': (result['current']['Gchi'] + rho) / self.node_weights, 'C1': rate, 'residual': residual, 'source_work': source_work, 'boundary_work': boundary_work, 'boundary_projection': boundary_projection, 'bulk_nodal_projection_work': result['projection_work'] - boundary_projection, 'Ward_error': rate - result['projection_work'] - result['metric_work'] - boundary_work - source_work})
        return result

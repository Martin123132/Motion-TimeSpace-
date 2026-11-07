from __future__ import annotations

import numpy as np
import sympy as sp

from interior_common import ROOT, Background, read_json


class LocalSystem:
    def __init__(self):
        self.background = Background()
        self.report = read_json(ROOT/'results/energy-v2/status.json')
        self.symbols = sp.symbols(' '.join(self.report['symbols']), positive=True)
        self.environment = dict(zip(self.report['symbols'], self.symbols))
        self.coefficient_names = list(self.report['coefficients'])
        self.derivative_names = list(self.report['derivatives'])
        expressions = [self.report['coefficients'][name] for name in self.coefficient_names]
        expressions += [self.report['derivatives'][name] for name in self.derivative_names]
        expressions += [value for row in self.report['base_hessian'] for value in row]
        expressions += self.report['contact_coefficients']
        self.evaluate = sp.lambdify(self.symbols, [sp.sympify(value, locals=self.environment) for value in expressions], 'numpy', cse=True)

    def values(self, position):
        data = self.background.values(position)
        arguments = [position, self.background.alpha, data['metric'], data['field'], data['gradient'],
                     self.background.frequency/data['lapse'], data['energy'], data['force'], data['second']]
        result = np.array([np.broadcast_to(value, position.shape) for value in self.evaluate(*arguments)])
        split = len(self.coefficient_names)
        coefficients = dict(zip(self.coefficient_names, result[:split]))
        derivative_end = split+len(self.derivative_names)
        derivatives = dict(zip(self.derivative_names, result[split:derivative_end]))
        base = np.moveaxis(result[derivative_end:derivative_end+36].reshape(6, 6, len(position)), -1, 0)
        contact = result[derivative_end+36:]
        mapping = np.zeros((len(position), 6, 5))
        mapping[:, :5, :] = np.eye(5)
        mapping[:, 5, :] = np.array([coefficients[name] for name in ['k_Zprime', 'k_Z', 'k_wprime', 'k_w', 'k_pibar']]).T
        local = np.einsum('qai,qab,qbj->qij', mapping, base, mapping)
        return data, coefficients, derivatives, local, contact


def scalar_schur(local):
    phase_coefficient = local[:, 4, 4]
    spatial = local[:, :4, :4]-np.einsum('qi,qj->qij', local[:, :4, 4], local[:, :4, 4])/phase_coefficient[:, None, None]
    gradient_indices, value_indices = [0, 2], [1, 3]
    gradient = spatial[:, gradient_indices][:, :, gradient_indices]
    mixed = spatial[:, gradient_indices][:, :, value_indices]
    potential = spatial[:, value_indices][:, :, value_indices]
    return phase_coefficient, gradient, mixed, potential

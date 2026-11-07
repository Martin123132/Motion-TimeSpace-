from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

from response_system_v2 import ResponseProblem as BaseProblem
from response_system_v2 import ROOT, PARENT, BRANCH, asymptotic_coefficients, potential, static_master_basis, encode


def outward_amplitude_ratios(radius, mass, sigma, shell_fractions, far_phase=40., order=10, tolerance=2e-12):
    positions = radius*np.array(sorted(set([1., *shell_fractions]), reverse=True))
    if sigma == 0:
        surface = static_master_basis(radius, mass, 1.)[0, 1]
        return {float(position/radius): static_master_basis(position, mass, 1.)[0, 1]/surface for position in positions}
    outer = max(1.1*positions[0], far_phase/sigma.real)
    coefficients = asymptotic_coefficients(mass*sigma, order)
    argument = sigma*outer
    indices = np.arange(order+1)
    series = np.sum(coefficients*argument**(-indices))
    derivative = np.sum(-indices*coefficients*argument**(-indices-1))
    initial = np.array([1.+0j, 1j*sigma+(1-2*mass/outer)*sigma*derivative/series])

    def equation(position, state):
        return np.array([state[1], (potential(position, mass)-sigma**2)*state[0]])/(1-2*mass/position)

    solution = solve_ivp(equation, (outer, radius), initial, t_eval=positions, method='DOP853', rtol=tolerance, atol=tolerance/100)
    assert solution.success, solution.message
    return {float(position/radius): value/solution.y[0, -1] for position, value in zip(solution.t, solution.y[0])}


class ResponseProblem(BaseProblem):
    def evaluate(self, sigma, buffers=(2., 3., 4.), shells=(10., 20., 40.)):
        report, solution = super().evaluate(sigma, buffers, shells)
        ratios = outward_amplitude_ratios(self.radius, self.mass, complex(sigma), shells, self.far_phase, self.order)
        surface_green = report['rows'][0]['total_green_surface_surface']
        for row in report['shell_rows']:
            fraction = row['source_radius_over_body_radius']
            corrected = surface_green*ratios[min(ratios, key=lambda key: abs(key-fraction))]
            row['outward_propagation_relative_control_difference'] = abs(row['master_surface_per_unit_source_jump']/corrected-1)
            row['master_surface_per_unit_source_jump'] = corrected
        report['source_propagation_method'] = 'All outgoing amplitudes sampled during inward integration, avoiding growing contamination from an outward near-static decaying solution.'
        return report, solution

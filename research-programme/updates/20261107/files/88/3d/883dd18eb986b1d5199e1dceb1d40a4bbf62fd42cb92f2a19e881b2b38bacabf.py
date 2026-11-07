from __future__ import annotations

import numpy as np
from scipy.integrate import solve_bvp

from dynamic_system import DynamicProblem as BaseProblem


class DynamicProblem(BaseProblem):
    def solve(self, previous=None):
        mesh = np.unique(np.r_[np.linspace(self.lower, self.upper, 400), np.linspace(max(self.lower, 1-12/self.radius), self.upper, 500)])
        dtype = complex if np.iscomplexobj(self.sigma) else float
        if previous is None:
            guess = np.vstack([-2*mesh**2, -4*mesh**3/3, -.04*mesh**2*(1-mesh)**2, -.08*mesh*(1-mesh)*(1-2*mesh), -.004*mesh**2, -.008*mesh]).astype(dtype)
            parameters = np.array([-.04, -.004, -2., -4/3], dtype=dtype)
        else:
            guess, parameters = previous.sol(mesh).astype(dtype), previous.p.astype(dtype)

        def jacobian(coordinate, state, parameters):
            result = np.empty((6, 6, len(coordinate)), dtype=dtype)
            for index in range(6):
                basis = np.zeros((6, len(coordinate)), dtype=dtype)
                basis[index] = 1
                result[:, index] = self.equation(coordinate, basis, parameters)
            return result, np.zeros((6, 4, len(coordinate)), dtype=dtype)

        zeros, zero_parameters = np.zeros(6, dtype=dtype), np.zeros(4, dtype=dtype)
        constant = self.boundary(zeros, zeros, zero_parameters)
        left_jacobian, right_jacobian, parameter_jacobian = np.empty((10, 6), dtype=dtype), np.empty((10, 6), dtype=dtype), np.empty((10, 4), dtype=dtype)
        for index in range(6):
            basis = np.eye(6, dtype=dtype)[index]
            left_jacobian[:, index] = self.boundary(basis, zeros, zero_parameters)-constant
            right_jacobian[:, index] = self.boundary(zeros, basis, zero_parameters)-constant
        for index in range(4):
            parameter_jacobian[:, index] = self.boundary(zeros, zeros, np.eye(4, dtype=dtype)[index])-constant

        def boundary_jacobian(left, right, parameters):
            return left_jacobian, right_jacobian, parameter_jacobian

        return solve_bvp(self.equation, self.boundary, mesh, guess, p=parameters, fun_jac=jacobian, bc_jac=boundary_jacobian,
                         tol=self.tolerance, bc_tol=self.tolerance/10, max_nodes=18000)

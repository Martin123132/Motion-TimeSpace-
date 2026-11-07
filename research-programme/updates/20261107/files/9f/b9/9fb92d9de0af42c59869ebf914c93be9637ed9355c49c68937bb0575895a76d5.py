from __future__ import annotations

from types import SimpleNamespace

import numpy as np
from scipy.integrate import solve_bvp
from scipy.interpolate import PPoly

from dynamic_system import DynamicProblem as BaseProblem


class DynamicProblem(BaseProblem):
    def solve(self, previous=None):
        mesh = np.unique(np.r_[np.linspace(self.lower, self.upper, 400), np.linspace(max(self.lower, 1-12/self.radius), self.upper, 500)])
        if previous is None:
            guess = np.vstack([-2*mesh**2, -4*mesh**3/3, -.04*mesh**2*(1-mesh)**2, -.08*mesh*(1-mesh)*(1-2*mesh), -.004*mesh**2, -.008*mesh]).astype(complex)
            parameters = np.array([-.04, -.004, -2., -4/3], dtype=complex)
        else:
            guess, parameters = previous.sol(mesh).astype(complex), previous.p.astype(complex)

        def equation(coordinate, state, parameters):
            answer = self.equation(coordinate, state[:6]+1j*state[6:], parameters[:4]+1j*parameters[4:])
            return np.vstack([answer.real, answer.imag])

        def boundary(left, right, parameters):
            answer = self.boundary(left[:6]+1j*left[6:], right[:6]+1j*right[6:], parameters[:4]+1j*parameters[4:])
            return np.r_[answer.real, answer.imag]

        def jacobian(coordinate, state, parameters):
            matrix = np.empty((6, 6, len(coordinate)), dtype=complex)
            for index in range(6):
                basis = np.zeros((6, len(coordinate)), dtype=complex)
                basis[index] = 1
                matrix[:, index] = self.equation(coordinate, basis, np.zeros(4))
            result = np.concatenate([np.concatenate([matrix.real, -matrix.imag], axis=1), np.concatenate([matrix.imag, matrix.real], axis=1)], axis=0)
            return result, np.zeros((12, 8, len(coordinate)))

        zeros, zero_parameters = np.zeros(12), np.zeros(8)
        constant = boundary(zeros, zeros, zero_parameters)
        left_jacobian, right_jacobian, parameter_jacobian = np.empty((20, 12)), np.empty((20, 12)), np.empty((20, 8))
        for index in range(12):
            basis = np.eye(12)[index]
            left_jacobian[:, index] = boundary(basis, zeros, zero_parameters)-constant
            right_jacobian[:, index] = boundary(zeros, basis, zero_parameters)-constant
        for index in range(8):
            parameter_jacobian[:, index] = boundary(zeros, zeros, np.eye(8)[index])-constant

        def boundary_jacobian(left, right, parameters):
            return left_jacobian, right_jacobian, parameter_jacobian

        solution = solve_bvp(equation, boundary, mesh, np.vstack([guess.real, guess.imag]), p=np.r_[parameters.real, parameters.imag],
                             fun_jac=jacobian, bc_jac=boundary_jacobian, tol=self.tolerance, bc_tol=self.tolerance/10, max_nodes=18000)
        spline = PPoly.construct_fast(solution.sol.c[:, :, :6]+1j*solution.sol.c[:, :, 6:], solution.sol.x, axis=1)
        return SimpleNamespace(sol=spline, p=solution.p[:4]+1j*solution.p[4:], y=solution.y[:6]+1j*solution.y[6:],
                               x=solution.x, rms_residuals=solution.rms_residuals, success=solution.success, message=solution.message, niter=solution.niter)

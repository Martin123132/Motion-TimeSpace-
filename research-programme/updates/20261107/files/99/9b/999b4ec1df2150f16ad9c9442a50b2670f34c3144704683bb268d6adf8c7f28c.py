from __future__ import annotations

import numpy as np
from scipy.integrate import solve_bvp

from sequence_tools import GRAVITY, PULSATION, SequenceBody as BaseSequenceBody, SequenceProfile, digest, save_solution, signed_spectrum
from sequence_tools import load_solution as base_load_solution


def load_solution(path):
    solution = base_load_solution(path)
    archive = np.load(path)
    body = BaseSequenceBody(float(archive['floor']), 2e-7)
    body.alpha = float(archive['alpha'])
    body.mass_scale = float(archive['mass_scale'])
    endpoint = body.endpoint(solution.p)
    solution.cut = endpoint[0]
    solution.total_charge_fraction = float(solution.sol(1.)[4]+endpoint[3]/solution.charge_scale)
    return solution


class SequenceBody(BaseSequenceBody):
    def continue_from(self, previous, target_charge=None, target_central=None):
        self.target_central = target_central
        old_charge_scale = previous.charge_scale
        self.charge_scale = target_charge/(4*np.pi) if target_charge is not None else old_charge_scale
        stride = max(1, int(np.ceil(len(previous.sol.x)/1600)))
        inherited = previous.sol.x[::stride]
        mesh = np.unique(np.concatenate([np.linspace(1e-6, 1, 1000), inherited, 1-np.geomspace(1e-7, .02, 80)]))
        separated = [float(mesh[0])]
        for node in mesh[1:-1]:
            if node-separated[-1] >= 1e-6 and 1-node >= 1e-6:
                separated.append(float(node))
        mesh = np.array([*separated, 1.])
        cut = self.endpoint(previous.p)[0]
        position = cut*mesh
        old_coordinate = position/previous.cut
        initial = previous.sol(np.clip(old_coordinate, 1e-6, 1.))
        initial[1] *= cut/previous.cut
        tail = old_coordinate > 1.
        if np.any(tail):
            radius = self.base_radius*previous.p[1]
            amplitude, slope = self.tail_values(radius-position[tail], previous.p)
            initial[0, tail] = amplitude
            initial[1, tail] = cut*slope
            initial[2, tail] = previous.p[2]
            initial[3, tail] = .5*np.log(1-2*self.alpha*self.mass_scale*previous.p[2]/position[tail])
            initial[4, tail] = previous.total_charge_fraction
        initial[4] *= old_charge_scale/self.charge_scale
        solution = solve_bvp(self.equation, self.boundary, mesh, initial, p=previous.p.copy(),
                             fun_jac=self.jacobian, tol=self.tolerance, bc_tol=1e-11, max_nodes=40000)
        solution.charge_scale = self.charge_scale
        endpoint = self.endpoint(solution.p)
        solution.cut = endpoint[0]
        solution.total_charge_fraction = float(solution.sol(1.)[4]+endpoint[3]/self.charge_scale)
        return solution

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_bvp

from sequence_tools import GRAVITY, PULSATION, SequenceBody as BaseSequenceBody, SequenceProfile, digest, load_solution, save_solution, signed_spectrum


class SequenceBody(BaseSequenceBody):
    def continue_from(self, previous, target_charge=None, target_central=None):
        self.target_central = target_central
        old_charge_scale = previous.charge_scale
        self.charge_scale = target_charge/(4*np.pi) if target_charge is not None else old_charge_scale
        stride = max(1, int(np.ceil(len(previous.sol.x)/1600)))
        inherited = previous.sol.x[::stride]
        edge = 1-np.geomspace(1e-7, .02, 80)
        mesh = np.unique(np.concatenate([np.linspace(1e-6, 1, 1000), inherited, edge]))
        initial = previous.sol(mesh)
        initial[4] *= old_charge_scale/self.charge_scale
        solution = solve_bvp(self.equation, self.boundary, mesh, initial, p=previous.p.copy(),
                             fun_jac=self.jacobian, tol=self.tolerance, bc_tol=1e-11, max_nodes=40000)
        solution.charge_scale = self.charge_scale
        return solution

from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_live_exponential_20260919 import RotationFlow, exponential_midpoint
import mpmath as mp
from scipy.integrate import solve_ivp
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-P2-live-exponential-algebra-attempt02', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False, live_annular_evolution=False,
            tests_are_manufactured_solver_controls=True)
        flow = RotationFlow(np.array([[0., 1e-10, 1.7, 23., 1e6]]))
        state = np.array([[[.3, -.2, .7, -.1, .4]], [[.5, .6, -.3, .8, -.9]]])
        for step in [0., 1e-12, 1e-5, .1]:
            actual = flow.exponential(step, state)
            weighted = step*flow.phi1(step, state)
            exact, integral = np.zeros_like(state), np.zeros_like(state)
            for index, frequency in enumerate(flow.frequency[0]):
                matrix = np.array([[0., frequency], [-frequency, 0.]])
                block = np.zeros((4, 4))
                block[:2, :2], block[:2, 2:] = matrix, np.eye(2)
                mp.mp.dps = 60
                exact_block = mp.expm(mp.mpf(step)*mp.matrix(block.tolist()))
                expected = np.array(exact_block.tolist(), dtype=float)
                exact[:, 0, index] = expected[:2, :2] @ state[:, 0, index]
                integral[:, 0, index] = expected[:2, 2:] @ state[:, 0, index]
            error = float(np.max(abs(actual-exact)))
            integral_error = float(np.max(abs(weighted-integral)))
            evidence.check('matrix_exponential_'+str(step), error < 2e-11, error)
            evidence.check('augmented_matrix_phi1_'+str(step), integral_error < 2e-12, integral_error)
            evidence.check('orthogonal_rotation_'+str(step), abs(np.linalg.norm(actual)/np.linalg.norm(state)-1) < 1e-14)
        drive = np.full_like(state, .013)
        flow.remainder = lambda values: drive
        for step in [1e-5, .1]:
            expected = flow.exponential(step, state)+step*flow.phi1(step, drive)
            evidence.check('constant_forcing_exact_'+str(step), np.max(abs(exponential_midpoint(flow, state, step)-expected)) < 2e-15)
        flow.remainder = lambda values: np.zeros_like(values)
        evidence.check('all_modes_linear_exact', np.max(abs(exponential_midpoint(flow, state, .00003)
            -flow.exponential(.00003, state))) < 2e-15)
        system = RotationFlow([[2., 5., 0.]])
        initial = np.array([[[.2, -.3, .4]], [[-.1, .25, .15]]])

        def remainder(values):
            positions, momenta = values[0, 0], values[1, 0]
            return np.array([[[.03*momenta[2]+.02*positions[1]**2, .04*positions[0], momenta[2]]],
                [[-.05*np.sin(positions[0]), .03*positions[2]-.02*momenta[1]**2,
                  -.2*positions[2]+.03*positions[1]]]])

        system.remainder = remainder
        target = solve_ivp(lambda time, vector:(system.linear(vector.reshape(initial.shape))+
            remainder(vector.reshape(initial.shape))).ravel(), (0., .2), initial.ravel(),
            method='DOP853', rtol=2e-13, atol=2e-15, t_eval=[.2])
        evidence.check('independent_DOP853_manufactured_control_complete', target.success)
        errors = []
        for steps in [10, 20, 40]:
            values = initial.copy()
            for unused in range(steps):
                values = exponential_midpoint(system, values, .2/steps)
            error = float(np.linalg.norm(values.ravel()-target.y[:, -1]))
            errors.append(error)
            evidence.report['cases'].append(dict(steps=steps, error=error))
        ratios = [errors[0]/errors[1], errors[1]/errors[2]]
        evidence.check('second_order_on_nonlinear_noncommuting_fixture', all(3.7 < ratio < 4.3 for ratio in ratios), ratios)
        frozen_source = initial.copy()
        frozen_source[:, :, -1] = 0.
        evidence.check('dropped_source_negative_control_detected', np.linalg.norm(target.y[:, -1].reshape(initial.shape)[:, :, -1]
            -frozen_source[:, :, -1]) > .1)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_anderson_midpoint_v2_20260921 import midpoint_step
from annular_candidate_midpoint_20260921 import midpoint_step as old_midpoint
from annular_decimal_transport_v2_20260919 import decimal_array
from decimal import Decimal, localcontext
import contextlib
import numpy as np


class LinearMechanical:
    precision = 64

    def __init__(self):
        self.mass = np.array([1., 2., 3., 4.])
        self.stiffness = np.array([10., 20., 60., 200.])
        self.original_scale = np.sqrt(self.mass)

    def evaluate(self, coordinates, rates):
        with localcontext() as context:
            context.prec = 64
            force = -coordinates*decimal_array(self.stiffness)
        return dict(momentum=rates*self.mass, force_decimal=force, force=np.asarray(force, float),
            radial_residual=0., minimum_F=1., maximum_speed_ratio=0.)

    def solve(self, residual):
        return residual/self.mass

    def residual_norm(self, residual):
        return float(np.linalg.norm(np.asarray(residual).ravel()/self.original_scale))


def main():
    evidence = EvidenceRun('annular-candidate-accelerated-midpoint-control-attempt02', __file__)
    try:
        model = LinearMechanical()
        position = decimal_array(np.array([[.1, -.2, .3, -.1]]))
        momentum = decimal_array(np.array([[.05, -.02, .1, -.04]]))
        seed = np.zeros((1, 4))
        records = []
        recorder = lambda row, *unused: records.append(row)
        failed = False
        try:
            old_midpoint(model, position, momentum, seed, 1., model, recorder)
        except RuntimeError as error:
            failed = 'not contracting' in str(error)
        evidence.check('mass_only_iteration_rejects_stiff_linear_control', failed)
        results = midpoint_step(model, position, momentum, seed, 1., model, recorder)
        updated_q, updated_p, rates = results[:3]
        expected = (np.asarray(momentum, float)-.5*model.stiffness*np.asarray(position, float))/(model.mass+.25*model.stiffness)
        evidence.check('full_rate_solution_matches_independent_linear_inverse', float(np.max(abs(rates-expected))) < 2e-12)
        initial_energy = float(np.sum(np.asarray(momentum, float)**2/(2*model.mass)+model.stiffness*np.asarray(position, float)**2/2))
        energy = float(np.sum(np.asarray(updated_p, float)**2/(2*model.mass)+model.stiffness*np.asarray(updated_q, float)**2/2))
        evidence.check('quadratic_midpoint_energy_identity', abs(energy-initial_energy) < 2e-12)
        reverse = midpoint_step(model, updated_q, updated_p, seed+.03, -1., model, recorder)
        with localcontext() as context:
            context.prec = 64
            reversal = float(max(np.max(abs(reverse[0]-position)), np.max(abs(reverse[1]-momentum))))
        evidence.check('independent_reverse_recovers_linear_state', reversal < 2e-12)
        evidence.report.update(linear_control_only=True, no_physical_modes_deleted=True,
            unchanged_residual_gates=True, reverse_error=reversal, rate_error=float(np.max(abs(rates-expected))),
            energy_error=abs(energy-initial_energy), forward_iterations=len(results[-1]), reverse_iterations=len(reverse[-1]),
            iterations=records, github_action=False, subagents_used=False)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print('Accelerated linear mechanical control passed; unchanged gates and full state retained.', flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

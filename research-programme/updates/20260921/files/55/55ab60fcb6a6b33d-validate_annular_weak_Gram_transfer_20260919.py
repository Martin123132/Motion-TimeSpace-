from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_weak_Gram_transfer_20260919 import adjoint_test, TEMPLATE_BOUND
from validate_annular_canonical_driver_residual_20260919 import banded
from fractions import Fraction
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-weak-Gram-algebra-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            nonnested_nonsymmetric_transfer_controls=True, wrong_adjoint_negative_controls=True)
        generator = np.random.default_rng(202609191439)
        for case in range(4):
            coarse_count, fine_count = 5, 9
            coarse_mass = np.diag(generator.uniform(.6, 1.4, coarse_count))
            fine_mass = np.diag(generator.uniform(.7, 1.5, fine_count))
            transfer = generator.normal(size=(fine_count, coarse_count))
            values, test = generator.normal(size=coarse_count), generator.normal(size=fine_count)
            indices = np.tile(np.arange(coarse_count), (fine_count, 1))
            adjoint, unused = adjoint_test(banded(coarse_mass), banded(fine_mass), test, indices, transfer, coarse_count)
            coarse_original, fine_original = generator.normal(size=(6, coarse_count)), generator.normal(size=(7, fine_count))
            coarse_hinge, fine_hinge = generator.normal(size=6), generator.normal(size=7)
            coarse_jump, fine_jump = generator.normal(size=coarse_count), generator.normal(size=fine_count)
            coarse_lifted = coarse_original-np.outer(coarse_hinge, coarse_jump)
            fine_lifted = fine_original-np.outer(fine_hinge, fine_jump)
            coarse_weights, fine_weights = generator.uniform(.5, 1.5, 6), generator.uniform(.5, 1.5, 7)
            coarse_stiffness = coarse_lifted.T @ (coarse_weights[:, None]*coarse_lifted)
            fine_stiffness = fine_lifted.T @ (fine_weights[:, None]*fine_lifted)
            covector_map = fine_mass @ transfer @ np.linalg.inv(coarse_mass)
            direct = float(test @ (covector_map @ coarse_stiffness @ values-fine_stiffness @ transfer @ values))
            weak = float((coarse_lifted @ adjoint) @ (coarse_weights*(coarse_lifted @ values))
                -(fine_lifted @ test) @ (fine_weights*(fine_lifted @ transfer @ values)))
            wrong = float((coarse_lifted @ (transfer.T @ test)) @ (coarse_weights*(coarse_lifted @ values))
                -(fine_lifted @ test) @ (fine_weights*(fine_lifted @ transfer @ values)))
            extended_trial = fine_original @ transfer @ values-fine_hinge*(coarse_jump @ values)
            extended_test = fine_original @ transfer @ adjoint-fine_hinge*(coarse_jump @ adjoint)
            coarse_work = float((coarse_lifted @ adjoint) @ (coarse_weights*(coarse_lifted @ values)))
            channels = dict(operator_weight=coarse_work-float(extended_test @ (fine_weights*extended_trial)),
                test_range=float((fine_lifted @ (transfer @ adjoint-test)) @ (fine_weights*extended_trial)),
                test_jump=-float((coarse_jump @ adjoint-fine_jump @ transfer @ adjoint)*(fine_hinge @ (fine_weights*extended_trial))),
                trial_jump=-float((coarse_jump @ values-fine_jump @ transfer @ values)*((fine_lifted @ test) @ (fine_weights*fine_hinge))))
            evidence.check(str(case)+'_mass_adjoint_weak_identity', abs(direct-weak) < 3e-10)
            evidence.check(str(case)+'_four_channel_nonnested_telescope', abs(sum(channels.values())-weak) < 3e-10)
            evidence.check(str(case)+'_raw_transpose_is_wrong', abs(wrong-weak) > 1e-3)
            evidence.check(str(case)+'_dropped_jump_controls_fail', abs(channels['test_jump']) > 1e-3 and abs(channels['trial_jump']) > 1e-3)
            evidence.report['cases'].append(dict(fixture=case, weak_identity_error=abs(direct-weak),
                telescope_error=abs(sum(channels.values())-weak), wrong_adjoint_error=abs(wrong-weak), **channels, valid_for_claim=False))
        maximum_diagonal = Fraction(59097, 573104)
        maximum_adjacent = Fraction(3, 392)
        maximum_extra = Fraction(1, 392)
        evidence.check('exact_uniform_template_bound', float(maximum_diagonal+2*maximum_adjacent+maximum_extra) == TEMPLATE_BOUND)
        evidence.check('all_diagonal_types_bounded', all(value <= maximum_diagonal for value in [Fraction(5,72), Fraction(1825,25284), Fraction(491,7056)]))
        evidence.check('all_adjacent_types_bounded', all(value <= maximum_adjacent for value in [Fraction(1,144), Fraction(253,50568)]))
        evidence.check('third_difference_first_difference_convolution_l1_constant', sum(abs(value) for value in [1,-2,1]) == 4)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']))), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

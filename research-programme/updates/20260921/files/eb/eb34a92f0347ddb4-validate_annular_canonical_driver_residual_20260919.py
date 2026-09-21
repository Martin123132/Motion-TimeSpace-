from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_canonical_driver_residual_20260919 import canonical_residual_split, driver_pairing
import contextlib
import json
import numpy as np


def banded(dense):
    count = len(dense)
    result = np.zeros((5, count))
    for column in range(count):
        for row in range(max(0, column-2), min(count, column+3)):
            result[2+row-column, column] = dense[row, column]
    return result


def main():
    evidence = EvidenceRun('annular-canonical-driver-algebra-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            independent_dense_controls=True, nonzero_inverse_residual_controls=True,
            transfer_jump_negative_control=True, raw_covector_interpolation_not_used=True)
        generator = np.random.default_rng(20260919)
        for case in range(4):
            coarse_count, fine_count = 5, 9
            coarse_lower = np.diag(generator.uniform(.7, 1.4, coarse_count))+np.diag(generator.normal(0., .1, coarse_count-1), -1)
            fine_lower = np.diag(generator.uniform(.7, 1.4, fine_count))+np.diag(generator.normal(0., .1, fine_count-1), -1)
            coarse_mass, fine_mass = coarse_lower @ coarse_lower.T, fine_lower @ fine_lower.T
            coarse_cross, fine_cross = generator.normal(size=coarse_count), generator.normal(size=fine_count)
            coarse_rate, fine_rate = generator.normal(size=coarse_count+1), generator.normal(size=fine_count+1)
            coarse_error, fine_error = .1*generator.normal(size=coarse_count), .1*generator.normal(size=fine_count)
            if case == 1:
                coarse_error *= 0.
                fine_error *= 0.
            if case == 2:
                coarse_rate[-1], fine_rate[-1] = 0., 0.
            prolongation = generator.normal(size=(fine_count, coarse_count))
            coarse_momenta = coarse_mass @ coarse_rate[:-1]+coarse_cross*coarse_rate[-1]+coarse_error
            fine_momenta = fine_mass @ fine_rate[:-1]+fine_cross*fine_rate[-1]+fine_error
            coarse = dict(mass_bands=banded(coarse_mass), cross=coarse_cross)
            fine = dict(mass_bands=banded(fine_mass), cross=fine_cross)
            split = canonical_residual_split(coarse, fine, coarse_momenta, fine_momenta, coarse_rate, fine_rate,
                lambda values:prolongation @ values)
            original = generator.normal(size=(6, fine_count))
            hinge = generator.normal(size=6)
            fine_jump = generator.normal(size=fine_count)
            coarse_jump = generator.normal(size=coarse_count)
            lifted = original-np.outer(hinge, fine_jump)
            row_covector = generator.normal(size=6)
            covector = lifted.T @ row_covector
            result, unused = driver_pairing(fine['mass_bands'], split, covector)
            jump_correction = float((row_covector @ hinge)*(coarse_jump @ coarse_rate[:-1]-fine_jump @ prolongation @ coarse_rate[:-1]))
            direct = float(row_covector @ (lifted @ fine_rate[:-1]-original @ prolongation @ coarse_rate[:-1]
                +hinge*(coarse_jump @ coarse_rate[:-1])))
            components = sum(result[key] for key in ['momentum_channel', 'source_cross_channel', 'coarse_inverse_channel', 'fine_inverse_channel'])
            evidence.check(str(case)+'_momentum_residual_recovers_actual_velocity', split['velocity_reconstruction_error'] < 3e-13
                and split['load_split_error'] < 3e-13)
            evidence.check(str(case)+'_complete_driver_identity', abs(direct-result['residual_pairing']-jump_correction) < 3e-12
                and abs(direct-components-jump_correction) < 3e-12)
            evidence.check(str(case)+'_localized_and_mass_bounds', abs(direct) <= result['corrected_residual_localized_bound']+abs(jump_correction)+3e-12
                and abs(direct) <= result['corrected_residual_mass_bound']+abs(jump_correction)+3e-12)
            evidence.check(str(case)+'_omitted_transfer_jump_negative_control', abs(jump_correction) > 1e-3)
            if case != 1:
                evidence.check(str(case)+'_omitted_inverse_residual_negative_control',
                    abs(result['coarse_inverse_channel']+result['fine_inverse_channel']) > 1e-3)
            if case == 2:
                evidence.check('zero_source_velocity_removes_cross_channel', abs(result['source_cross_channel']) < 3e-13)
            evidence.report['cases'].append(dict(fixture=case, **result, interpolation_jump_channel=jump_correction,
                actual_driver=direct, total_reconstruction_error=abs(direct-components-jump_correction)))
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

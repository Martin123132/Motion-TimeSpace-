from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_Gram_projection_commutator_20260919 import mass_pairing, band_action
from scipy.linalg import cholesky_banded
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-projection-commutator-algebra-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            independent_dense_mass_control=True, includes_nonzero_and_zero_controls=True)
        generator = np.random.default_rng(20260919)
        for count in [7, 23]:
            lower = np.diag(np.linspace(.7, 1.4, count))
            lower += np.diag(generator.normal(0., .1, count-1), -1)
            lower += np.diag(generator.normal(0., .1, count-2), -2)
            dense = lower @ lower.T
            bands = np.zeros((5, count))
            for column in range(count):
                for row in range(max(0, column-2), min(count, column+3)):
                    bands[2+row-column, column] = dense[row, column]
            covector = generator.normal(size=count)
            delta = generator.normal(size=count)
            base = generator.normal(size=count)
            residual = dense @ (base+delta)-dense @ base
            evidence.check(str(count)+'_band_action_matches_independent_dense',
                np.max(abs(band_action(bands, base)-dense @ base)) < 2e-14)
            evidence.check(str(count)+'_positive_mass_factorization', np.all(cholesky_banded(bands[:3])[-1] > 0))
            cases = [('general', residual, covector), ('saturating_positive', covector, covector),
                ('saturating_negative', -covector, covector), ('zero_residual', residual*0., covector),
                ('zero_covector', residual, covector*0.)]
            for name, load, functional in cases:
                result, arrays = mass_pairing(bands, load, functional)
                expected = float(functional @ np.linalg.solve(dense, load))
                tag = str(count)+'_'+name
                evidence.check(tag+'_dense_and_dual_pairings', abs(result['projection_force']-expected) < 3e-13
                    and abs(result['dual_residual_pairing']-expected) < 3e-13)
                evidence.check(tag+'_both_bounds', abs(expected) <= result['dual_mass_bound']+3e-13
                    and abs(expected) <= result['dual_residual_absolute_bound']+3e-13)
                if name.startswith('saturating'):
                    evidence.check(tag+'_bound_is_sharp', abs(abs(expected)-result['dual_mass_bound']) < 3e-13)
                if name == 'general':
                    evidence.check(tag+'_actual_projection_correction_recovered', np.max(abs(arrays['correction']-delta)) < 3e-14)
                    evidence.check(tag+'_omitted_residual_negative_control', abs(expected) > 1e-3)
                evidence.report['cases'].append(dict(count=count, fixture=name, **result))
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

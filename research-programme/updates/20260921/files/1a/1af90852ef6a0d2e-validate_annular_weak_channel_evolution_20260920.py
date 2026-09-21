from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_decimal_transport_20260919 import DecimalAction, decimal_array, dot
from annular_mixed_weak_maps_20260920 import MixedMap
from annular_weak_channel_evolution_20260920 import evolve_channels
from validate_annular_mixed_force_cascade_v2_20260920 import action_data, oscillator
from decimal import Decimal, localcontext
import contextlib
import json
import mpmath as mp


def main():
    evidence = EvidenceRun('annular-weak-channel-controls-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
            fixture_only=True, physical_force_mismatch_fixed=False)
        with localcontext() as ctx, mp.workdps(80):
            ctx.prec = 48
            coarse_mass = [[2., .125], [.125, 1.5]]
            fine_mass = [[3., .25, .0625], [.25, 2., .125], [.0625, .125, 1.]]
            coarse_factor = [[1., -.5], [.25, 2.]]
            fine_factor = [[1., -.5, 0.], [0., 2., .25], [.125, 0., 1.5]]
            actions = [DecimalAction(action_data(mass, factor)) for mass, factor in
                [(coarse_mass, coarse_factor), (fine_mass, fine_factor)]]
            raw_mass = [[1., .125], [.25, 1.5], [-.125, .25]]
            raw_stiffness = [[2., -.25], [-.5, 3.], [.125, 1.]]
            coefficients = [(1., .125), (.5, -.25), (-.125, .375), (0., .25), (0., 0.)]
            pairs = []
            for mass_coefficient, stiffness_coefficient in coefficients:
                pair = []
                for coefficient, values in [(mass_coefficient, raw_mass), (stiffness_coefficient, raw_stiffness)]:
                    pair.append(MixedMap([{column:Decimal.from_float(coefficient*value)
                        for column, value in enumerate(row)} for row in values], 2))
                pairs.append(pair)
            initial = decimal_array([[.125, -.25], [.75, .0625]])[:, :, None]
            covector = decimal_array([[1., -.5, .25], [.125, .0625, -.25]])[:, :, None]
            forward, unused, controls = evolve_channels(*actions, pairs, initial, Decimal('.375'), 64)
            backward, unused, controls = evolve_channels(*actions, pairs, covector, Decimal('.375'), 64, transpose=True)
            coarse_mass, fine_mass = mp.matrix(coarse_mass), mp.matrix(fine_mass)
            coarse_factor, fine_factor = mp.matrix(coarse_factor), mp.matrix(fine_factor)
            coarse_acceleration = coarse_mass**-1*coarse_factor.T*coarse_factor
            fine_acceleration = fine_mass**-1*fine_factor.T*fine_factor
            for column, (mass_coefficient, stiffness_coefficient) in enumerate(coefficients):
                generator = mp.matrix(10)
                generator[:4, :4] = oscillator(coarse_acceleration)
                generator[4:, 4:] = oscillator(fine_acceleration)
                defect = mass_coefficient*mp.matrix(raw_mass)*coarse_acceleration-stiffness_coefficient*mp.matrix(raw_stiffness)
                generator[7:, :2] = fine_mass**-1*defect
                exact = mp.expm(mp.mpf('.375')*generator)*mp.matrix([float(value) for value in initial.flat]+[0.]*6)
                expected = sum(mp.mpf(float(value))*exact[index+4] for index, value in enumerate(covector.flat))
                actual = dot(covector[:, :, 0], forward[:, :, column])
                dual = dot(initial[:, :, 0], backward[:, :, column])
                evidence.check('channel_'+str(column)+'_dense_exponential', abs(mp.mpf(str(actual))-expected) < mp.mpf('1e-38'))
                evidence.check('channel_'+str(column)+'_adjoint', abs(actual-dual) < Decimal('1e-38'))
                evidence.report['cases'].append(dict(channel=column, forward=str(actual), adjoint=str(dual), exact=str(expected), valid_for_claim=False))
            evidence.check('only_identically_zero_channel_skipped', controls['exactly_zero_channels'] == [4]
                and all(value == 0 for value in forward[:, :, 4].flat))
            evidence.check('negative_channel_sign_detectable', abs(Decimal(evidence.report['cases'][3]['forward'])) > Decimal('1e-6'))
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

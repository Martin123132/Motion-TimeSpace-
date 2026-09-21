from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_decimal_transport_20260919 import DecimalAction, DecimalMap, decimal_array, dot
from annular_mixed_weak_maps_20260920 import MixedMap
from annular_mixed_force_cascade_20260920 import integrate_channels
from decimal import Decimal, localcontext
from scipy.sparse import csr_matrix
import contextlib
import json
import mpmath as mp
import numpy as np


def action_data(mass, factor):
    count = len(mass)
    bands = np.zeros((5, count))
    for row in range(count):
        for column in range(count):
            if abs(row-column) <= 2:
                bands[2+row-column, column] = mass[row][column]
    data = dict(mass_bands=bands, gradient_weights=np.ones(count), gram_weights=np.zeros(0))
    for name, matrix in [('gradient', csr_matrix(factor)), ('gram', csr_matrix((0, count)))]:
        for field in ['data', 'indices', 'indptr', 'shape']:
            data[name+'_'+field] = np.asarray(getattr(matrix, field))
    return data


def oscillator(acceleration):
    count = acceleration.rows
    generator = mp.matrix(2*count)
    for row in range(count):
        generator[row, row+count] = 1
        for column in range(count):
            generator[row+count, column] = -acceleration[row, column]
    return generator


def main():
    evidence = EvidenceRun('annular-mixed-force-controls-attempt02', __file__)
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
            transfer_array = [[1., 0.], [.5, 0.], [-.25, 0.]]
            mass_array = [[1., .125], [.25, 1.5], [-.125, .25]]
            stiffness_array = [[2., -.25], [-.5, 3.], [.125, 1.]]
            transfer = DecimalMap(csr_matrix(transfer_array))
            maps = {name: MixedMap([{column: str(value) for column, value in enumerate(row)} for row in values], 2)
                for name, values in [('mass', mass_array), ('gradient', stiffness_array), ('gram', [[0., 0.]]*3)]}
            initial = decimal_array([[.125, -.25], [.75, .0625]])[:, :, None]
            covector = decimal_array([[1., -.5, .25], [.125, .0625, -.25]])[:, :, None]
            duration = Decimal('.375')
            forward, unused, diagnostics = integrate_channels(*actions, transfer, maps, initial, duration, 64)
            backward, unused, diagnostics = integrate_channels(*actions, transfer, maps, covector, duration, 64, transpose=True)
            coarse_mass, fine_mass = mp.matrix(coarse_mass), mp.matrix(fine_mass)
            coarse_factor, fine_factor = mp.matrix(coarse_factor), mp.matrix(fine_factor)
            coarse_stiffness, fine_stiffness = coarse_factor.T*coarse_factor, fine_factor.T*fine_factor
            coarse_acceleration, fine_acceleration = coarse_mass**-1*coarse_stiffness, fine_mass**-1*fine_stiffness
            transfer_exact, mixed_mass, mixed_stiffness = mp.matrix(transfer_array), mp.matrix(mass_array), mp.matrix(stiffness_array)
            defects = [(fine_mass*transfer_exact-mixed_mass)*coarse_acceleration,
                mixed_stiffness-fine_stiffness*transfer_exact, mixed_mass*coarse_acceleration-mixed_stiffness]
            channels = []
            for column, defect in enumerate(defects):
                generator = mp.matrix(10)
                generator[:4, :4] = oscillator(coarse_acceleration)
                generator[4:, 4:] = oscillator(fine_acceleration)
                generator[7:, :2] = fine_mass**-1*defect
                start = mp.matrix([float(value) for value in initial.flat]+[0.]*6)
                exact = mp.expm(mp.mpf(str(duration))*generator)*start
                expected = sum(mp.mpf(float(value))*exact[index+4] for index, value in enumerate(covector.flat))
                actual = dot(covector[:, :, 0], forward[:, :, column])
                dual = dot(initial[:, :, 0], backward[:, :, column])
                evidence.check('channel_'+str(column)+'_independent_dense_exponential', abs(mp.mpf(str(actual))-expected) < mp.mpf('1e-38'))
                evidence.check('channel_'+str(column)+'_independent_adjoint', abs(actual-dual) < Decimal('1e-38'))
                channels.append(actual)
                evidence.report['cases'].append(dict(channel=column, actual=str(actual), adjoint=str(dual), exact=str(expected), valid_for_claim=False))
            evidence.check('singular_transfer_is_not_inverted', np.linalg.matrix_rank(transfer_array) == 1)
            evidence.check('negative_sign_control_detected', abs(2*channels[1]) > Decimal('1e-6'))
            evidence.check('channels_do_not_vanish_trivially', all(abs(value) > Decimal('1e-8') for value in channels))
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

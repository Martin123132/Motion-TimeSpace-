from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_decimal_transport_20260919 import DecimalAction, DecimalMap, decimal_array, zero_array, dot, propagate
from run_annular_P2_continuum_bridge_20260918 import checked_load
from decimal import Decimal, localcontext
from scipy.sparse import csr_matrix
from time import perf_counter
import contextlib
import json
import mpmath as mp
import numpy as np


def fixture(evidence):
    mass = np.array([[3., .125, -.03125], [.125, 2., .0625], [-.03125, .0625, 1.]])
    factor = csr_matrix([[2., -.5, 0.], [0., 1., -.25], [.125, 0., 3.]])
    bands = np.zeros((5, 3))
    for row in range(3):
        for column in range(3):
            bands[2+row-column, column] = mass[row, column]
    empty = csr_matrix((0, 3))
    data = dict(mass_bands=bands, gradient_weights=np.array([1., 2., 3.]), gram_weights=np.zeros(0))
    for name, matrix in [('gradient', factor), ('gram', empty)]:
        for field in ['data', 'indices', 'indptr']:
            data[name+'_'+field] = getattr(matrix, field)
    with localcontext() as ctx, mp.workdps(80):
        ctx.prec = 48
        action = DecimalAction(data)
        exact_mass = mp.matrix(mass.tolist())
        exact_factor = mp.matrix(factor.toarray().tolist())
        exact_stiffness = exact_factor.T*mp.diag([1, 2, 3])*exact_factor
        exact_acceleration = exact_mass**-1*exact_stiffness
        generator = mp.matrix(6)
        for row in range(3):
            generator[row, row+3] = 1
            for column in range(3):
                generator[row+3, column] = -exact_acceleration[row, column]
        phase = decimal_array(np.array([[.125, -.25, .5], [.75, -.125, .0625]]))[:, :, None]
        for transpose in [False, True]:
            source = np.asarray(phase, dtype=float).reshape(6)
            expected = mp.expm(mp.mpf('0.375')*(generator.T if transpose else generator))*mp.matrix(source.tolist())
            result, unused = propagate(action, phase, Decimal('.375'), 64, transpose=transpose)
            error = max(abs(mp.mpf(str(value))-expected[index]) for index, value in enumerate(result.flat))
            evidence.check('independent_dense_mpmath_'+str(transpose), error < mp.mpf('1e-38'), str(error))
        direct, unused = propagate(action, phase, Decimal('.375'), 64)
        increment, unused = propagate(action, phase, Decimal('.375'), 64, increment=True)
        error = max(map(abs, (direct-phase-increment).flat))
        evidence.check('independent_affine_increment_fixture', error < Decimal('1e-38'), str(error))
        sample = decimal_array(np.array([[1.], [2.], [-.5]]))
        actual = action.acceleration(sample)
        expected = exact_acceleration*mp.matrix([1, 2, -.5])
        error = max(abs(mp.mpf(str(actual[index, 0]))-expected[index]) for index in range(3))
        evidence.check('factor_assembly_and_LDL_dense_oracle', error < mp.mpf('1e-38'), str(error))


def main():
    evidence = EvidenceRun('annular-decimal-duality-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            original_action_unchanged=True, genuine_decimal_precision=True,
            fixed_saved_binary64_inputs_not_new_parent_precision=True, original_strict_dual_gate_pass=False,
            full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
            interval_roundoff_certificate=False, maximum_wall_seconds=7200)
        fixture(evidence)
        previous_path = evidence.output.parent/'annular-full-force-transport-attempt02/status.json'
        previous = json.loads(previous_path.read_text())
        evidence.own(previous_path)
        evidence.check('old_failed_strict_qualification_preserved', previous['state'] == 'complete'
            and not previous['original_strict_dual_gate_pass'])
        evidence.report['controls'] = []
        for branch in ['reference', 'MTS']:
            data = [checked_load(evidence, 'annular-action-exponential-response-attempt01', branch+'-'+level+'-action.npz')
                for level in ['coarse', 'fine']]
            initial = checked_load(evidence, 'annular-moving-duhamel-trajectory-attempt01', branch+'-point032.npz')
            endpoint = [checked_load(evidence, 'annular-full-force-endpoints-attempt01', branch+'-'+comparison+'-force-covector.npz')
                for comparison in ['spatial32', 'spatial64']]
            evidence.check(branch+'_same_spatial_transfer', np.array_equal(endpoint[0]['transfer'], endpoint[1]['transfer']))
            saved_rows = []
            for digits, degree in [(32, 48), (48, 64)]:
                with localcontext() as ctx:
                    ctx.prec = digits
                    actions = [DecimalAction(item) for item in data]
                    transfer = DecimalMap(csr_matrix(endpoint[0]['transfer']))
                    coarse = decimal_array(np.stack([initial['0_position'], -initial['0_reverse_velocity']]))[:, :, None]
                    fine = decimal_array(np.stack([initial['1_position'], -initial['1_reverse_velocity']]))[:, :, None]
                    embedded = np.stack([transfer.apply(component) for component in coarse])
                    initial_difference = fine-embedded
                    covector = decimal_array(np.stack([item['covector'] for item in endpoint], axis=-1))
                    coarse_covector = np.stack([transfer.apply(component, transpose=True) for component in covector])
                    duration = Decimal.from_float(4e-5)

                    def run(label, action, phase, transpose=False, increment=False):
                        def progress(done, total):
                            evidence.report['progress'] = dict(branch=branch, digits=digits, part=label,
                                done=done, total=total, seconds=perf_counter()-started)
                            evidence.save()
                            print(json.dumps(evidence.report['progress']), flush=True)
                        result, diagnostics = propagate(action, phase, duration, degree, transpose=transpose,
                            increment=increment, progress=progress, deadline=started+7200)
                        diagnostics.update(branch=branch, part=label, valid_for_claim=False)
                        evidence.report['controls'].append(diagnostics)
                        return result

                    representation = run('small_initial_difference', actions[1], initial_difference)
                    fine_increment = run('fine_operator_increment', actions[1], embedded, increment=True)
                    coarse_increment = run('coarse_operator_increment', actions[0], coarse, increment=True)
                    commutator = fine_increment-np.stack([transfer.apply(component) for component in coarse_increment])
                    backward_fine = run('independent_fine_adjoint', actions[1], covector, transpose=True)
                    backward_coarse = run('independent_coarse_adjoint', actions[0], coarse_covector, transpose=True)
                    branch_rows = []
                    for column, comparison in enumerate(['spatial32', 'spatial64']):
                        initial_pairing = dot(covector[:, :, column], representation[:, :, 0])
                        operator_pairing = dot(covector[:, :, column], commutator[:, :, 0])
                        forward = initial_pairing+operator_pairing
                        backward = dot(backward_fine[:, :, column], fine[:, :, 0])-dot(backward_coarse[:, :, column], coarse[:, :, 0])
                        error = abs(forward-backward)
                        tolerance = Decimal('2e-10')*max(abs(forward), abs(backward), Decimal('1e-9'))+Decimal('3e-16')
                        old = next(row for row in previous['duals'] if row['branch'] == branch and row['comparison'] == comparison)
                        row = dict(branch=branch, comparison=comparison, digits=digits, degree=degree,
                            initial_representation=str(initial_pairing), frozen_operator_commutator=str(operator_pairing),
                            forward_pairing=str(forward), backward_pairing=str(backward), dual_error=str(error),
                            unchanged_numerical_tolerance=str(tolerance), original_strict_gate_pass=bool(error <= tolerance),
                            old_forward_pairing=old['forward_pairing'], old_backward_pairing=old['backward_pairing'],
                            old_dual_error=old['error'], forward_change=str(forward-Decimal.from_float(old['forward_pairing'])),
                            backward_change=str(backward-Decimal.from_float(old['backward_pairing'])), valid_for_claim=False)
                        evidence.report['cases'].append(row)
                        branch_rows.append(row)
                        evidence.check(branch+'_'+comparison+'_'+str(digits)+'_unchanged_strict_duality_gate', error <= tolerance, row)
                    payload = dict(branch=branch, digits=digits, representation=representation[:, :, 0].tolist(),
                        operator_commutator=commutator[:, :, 0].tolist(), backward_fine=backward_fine.tolist(),
                        backward_coarse=backward_coarse.tolist())
                    output = evidence.output/(branch+'-'+str(digits)+'-transport.json')
                    output.write_text(json.dumps(payload, default=str)+'\n', encoding='utf-8')
                    evidence.own(output, 'outputs')
                    if saved_rows:
                        for earlier, later in zip(saved_rows, branch_rows):
                            error = max(abs(Decimal(earlier[key])-Decimal(later[key])) for key in
                                ['initial_representation', 'frozen_operator_commutator', 'forward_pairing', 'backward_pairing'])
                            evidence.check(branch+'_'+later['comparison']+'_precision_and_order_refinement',
                                error < Decimal('1e-22'), str(error))
                    saved_rows = branch_rows
                    evidence.save()
        evidence.report['original_strict_dual_gate_pass'] = all(row['original_strict_gate_pass'] for row in evidence.report['cases'])
        evidence.report['seconds'] = perf_counter()-started
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

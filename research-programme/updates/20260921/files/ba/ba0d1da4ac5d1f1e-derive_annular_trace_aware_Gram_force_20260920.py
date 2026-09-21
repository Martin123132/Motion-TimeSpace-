from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_decimal_transport_v2_20260919 import DecimalAction, decimal_array, dot
from annular_mixed_weak_maps_20260920 import MixedMap
from annular_weak_channel_evolution_20260920 import evolve_channels
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from derive_annular_common_weak_action_20260920 import dec_saved
from run_annular_P2_continuum_bridge_20260918 import checked_load
from decimal import Decimal, localcontext
from time import perf_counter
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-trace-aware-Gram-force-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            original_action_unchanged=True, full_live_P2_force_convergence_proven=False,
            certified_continuous_time_bound=False, physical_force_mismatch_fixed=False,
            full_moving_force_decomposition_done=False, parent_coefficient_precision='binary64',
            trace_aware_Gram_force_qualified=False, no_singular_inverse=True, maximum_wall_seconds=10000)
        evidence.report['controls'], evidence.report['refinement'], evidence.report['regrouped'] = [], [], []
        previous_path = evidence.output.parent/'annular-weak-residual-force-attempt01/status.json'
        previous = json.loads(previous_path.read_text())
        evidence.own(previous_path)
        evidence.check('previous_weak_channels_complete', previous['state'] == 'complete'
            and previous['weak_residual_channels_qualified'] and all(row['passed'] for row in previous['checks']))
        fixture_path = evidence.output.parent/'annular-weak-channel-controls-attempt01/status.json'
        fixture = json.loads(fixture_path.read_text())
        evidence.own(fixture_path)
        evidence.check('independent_dense_controls_complete', fixture['state'] == 'complete'
            and all(row['passed'] for row in fixture['checks']))
        for branch in ['reference', 'MTS']:
            packet = owned_json(evidence, 'annular-trace-aware-Gram-matrices-attempt01', branch+'-trace-Gram-matrices.json')
            labels = list(packet['channels'])
            pairs = [[MixedMap(item[name]['rows'], item[name]['columns']) for name in ['mass', 'stiffness']]
                for item in packet['channels'].values()]
            old_rows = {row['channel']:row for row in previous['cases']
                if row['branch'] == branch and row['digits'] == 48 and row['moment_order'] == 64}
            old = old_rows['Gram_same_geometry_stencil']
            expected, gate = Decimal(old['integral']), Decimal(old['literal_predecessor_gate'])
            if branch == 'reference':
                evidence.check('reference_all_channel_operators_exactly_zero',
                    all(len(mapping.values) == 0 for pair in pairs for mapping in pair))
                evidence.check('reference_previous_Gram_zero', expected == 0)
                values = [Decimal(0)]*len(labels)
                for label in labels:
                    evidence.report['cases'].append(dict(branch=branch, digits=0, degree=0, channel=label,
                        integral='0', adjoint_integral='0', total='0', prior_Gram_integral=str(expected),
                        literal_predecessor_gate=str(gate), evaluation_method='analytic_zero_operator',
                        valid_for_claim=False))
                evidence.report['controls'].append(dict(branch=branch, direction='both',
                    evaluation_method='analytic_zero_operator', explanation='Zero forcing and zero initial response imply zero response by uniqueness of the original finite-dimensional linear ODE.',
                    valid_for_claim=False))
            else:
                data = [checked_load(evidence, 'annular-action-exponential-response-attempt01', branch+'-'+level+'-action.npz')
                    for level in ['coarse', 'fine']]
                initial = checked_load(evidence, 'annular-moving-duhamel-trajectory-attempt01', branch+'-point032.npz')
                endpoint = checked_load(evidence, 'annular-full-force-endpoints-attempt01', branch+'-spatial64-force-covector.npz')
                comparisons = None
                for digits, degree, directions in [(32, 48, ['forward']), (48, 64, ['forward', 'adjoint'])]:
                    with localcontext() as ctx:
                        ctx.prec = digits
                        actions = [DecimalAction(item) for item in data]
                        source = decimal_array(np.stack([initial['0_position'], -initial['0_reverse_velocity']]))[:, :, None]
                        covector = decimal_array(endpoint['covector'])[:, :, None]
                        directional = {}
                        for direction in directions:
                            def progress(done, total):
                                evidence.report['progress'] = dict(branch=branch, digits=digits, degree=degree,
                                    direction=direction, done=done, total=total, seconds=perf_counter()-started)
                                evidence.save()
                                print(json.dumps(evidence.report['progress']), flush=True)
                            response, terminal, diagnostics = evolve_channels(*actions, pairs,
                                covector if direction == 'adjoint' else source, Decimal.from_float(4e-5), degree,
                                transpose=direction == 'adjoint', progress=progress, deadline=started+10000)
                            pairing = source if direction == 'adjoint' else covector
                            values = [dot(pairing[:, :, 0], response[:, :, column]) for column in range(len(labels))]
                            directional[direction] = values
                            evidence.report['controls'].append(dict(branch=branch, direction=direction,
                                evaluation_method='original_frozen_channel_evolution', **diagnostics, valid_for_claim=False))
                            output = evidence.output/(branch+'-'+str(digits)+'-'+direction+'.json')
                            output.write_text(json.dumps(dict(labels=labels, integrals=list(map(str, values)),
                                response=response.tolist(), source_terminal=terminal.tolist()), default=str)+'\n', encoding='utf-8')
                            evidence.own(output, 'outputs')
                            error = abs(sum(values, Decimal(0))-expected)
                            evidence.check(str(digits)+'_'+direction+'_previous_Gram_force_recovered', error <= gate,
                                dict(error=str(error), literal_gate=str(gate)))
                        forward, dual = directional['forward'], directional.get('adjoint')
                        if dual is not None:
                            for label, first, last in zip(labels, forward, dual):
                                evidence.check(label+'_independent_adjoint', abs(first-last) <= gate,
                                    dict(error=str(abs(first-last)), literal_gate=str(gate)))
                            old_adjoint = owned_json(evidence, 'annular-weak-residual-force-attempt01', branch+'-48-order64-adjoint.json')
                            error = max(map(abs, (terminal-dec_saved(old_adjoint['source_terminal'])).flat))
                            evidence.check('same_original_fine_adjoint', error < Decimal('1e-32'), str(error))
                        for label, value, backward in zip(labels, forward, dual if dual is not None else [None]*len(labels)):
                            evidence.report['cases'].append(dict(branch=branch, digits=digits, degree=degree, channel=label,
                                integral=str(value), adjoint_integral=str(backward) if backward is not None else '',
                                total=str(sum(forward, Decimal(0))), prior_Gram_integral=str(expected),
                                literal_predecessor_gate=str(gate), evaluation_method='original_frozen_channel_evolution',
                                valid_for_claim=False))
                        if comparisons is not None:
                            for label, first, last in zip(labels, forward, comparisons):
                                error = abs(first-last)
                                evidence.report['refinement'].append(dict(branch=branch, channel=label,
                                    comparison='arithmetic_and_time_order_fixed_matrices', absolute_change=str(error),
                                    literal_predecessor_gate=str(gate), passed=bool(error <= gate), valid_for_claim=False))
                                evidence.check(label+'_refinement', error <= gate, str(error))
                        comparisons, values = forward, forward
                        evidence.save()
            with localcontext() as ctx:
                ctx.prec = 64
                regrouped_finer = Decimal(old_rows['unresolved_finer_test']['integral'])+values[0]
                remaining = sum((Decimal(old_rows[label]['integral']) for label in
                    ['coarse_native_closure', 'mass_gradient_geometry', 'Gram_geometry_weight']), Decimal(0))
                total = remaining+regrouped_finer+values[1]
                expected_weak = Decimal(old['total'])
                evidence.check(branch+'_regrouping_preserves_old_weak_sum', abs(total-expected_weak) <= gate,
                    dict(error=str(abs(total-expected_weak)), literal_gate=str(gate)))
                evidence.report['regrouped'].append(dict(branch=branch, old_unresolved_finer_test=old_rows['unresolved_finer_test']['integral'],
                    lost_test_trace=str(values[0]), trace_complete_finer_test=str(regrouped_finer),
                    trace_aware_Gram_remainder=str(values[1]), unchanged_other_channels=str(remaining),
                    weak_total=str(total), prior_weak_total=str(expected_weak), literal_predecessor_gate=str(gate),
                    valid_for_claim=False))
            evidence.save()
        evidence.report.update(trace_aware_Gram_force_qualified=True, seconds=perf_counter()-started)
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


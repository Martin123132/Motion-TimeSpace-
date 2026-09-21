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
    evidence = EvidenceRun('annular-weak-residual-force-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            original_action_unchanged=True, full_live_P2_force_convergence_proven=False,
            certified_continuous_time_bound=False, physical_force_mismatch_fixed=False,
            full_moving_force_decomposition_done=False, parent_coefficient_precision='binary64',
            weak_residual_channels_qualified=False, no_singular_inverse=True, maximum_wall_seconds=11000)
        evidence.report['controls'], evidence.report['refinement'] = [], []
        controls_path = evidence.output.parent/'annular-weak-channel-controls-attempt01/status.json'
        controls = json.loads(controls_path.read_text())
        evidence.own(controls_path)
        evidence.check('independent_dense_channel_controls', controls['state'] == 'complete' and all(row['passed'] for row in controls['checks']))
        previous_path = evidence.output.parent/'annular-mixed-force-integrals-attempt01/status.json'
        previous = json.loads(previous_path.read_text())
        evidence.own(previous_path)
        evidence.check('previous_frozen_channels_complete', previous['state'] == 'complete' and previous['frozen_operator_force_integrals_qualified'])
        for branch in ['reference', 'MTS']:
            data = [checked_load(evidence, 'annular-action-exponential-response-attempt01', branch+'-'+level+'-action.npz')
                for level in ['coarse', 'fine']]
            initial = checked_load(evidence, 'annular-moving-duhamel-trajectory-attempt01', branch+'-point032.npz')
            endpoint = checked_load(evidence, 'annular-full-force-endpoints-attempt01', branch+'-spatial64-force-covector.npz')
            previous_row = next(row for row in previous['cases'] if row['branch'] == branch and row['digits'] == 48 and row['channel'] == 'mixed_weak_remainder')
            expected = Decimal(previous_row['forward_integral'])
            gate = Decimal(previous_row['literal_predecessor_gate'])
            comparisons = {}
            for digits, degree, order, directions in [(32, 48, 32, ['forward']),
                    (48, 64, 32, ['forward']), (48, 64, 64, ['forward', 'adjoint'])]:
                with localcontext() as ctx:
                    ctx.prec = digits
                    actions = [DecimalAction(item) for item in data]
                    packet = owned_json(evidence, 'annular-weak-residual-matrices-attempt01', branch+'-order'+str(order)+'-residual-matrices.json')
                    labels = list(packet)
                    pairs = [[MixedMap(item[name]['rows'], item[name]['columns']) for name in ['mass', 'stiffness']]
                        for item in packet.values()]
                    source = decimal_array(np.stack([initial['0_position'], -initial['0_reverse_velocity']]))[:, :, None]
                    covector = decimal_array(endpoint['covector'])[:, :, None]
                    directional = {}
                    for direction in directions:
                        def progress(done, total):
                            evidence.report['progress'] = dict(branch=branch, digits=digits, order=order,
                                direction=direction, done=done, total=total, seconds=perf_counter()-started)
                            evidence.save()
                            print(json.dumps(evidence.report['progress']), flush=True)
                        response, terminal, diagnostics = evolve_channels(*actions, pairs,
                            covector if direction == 'adjoint' else source, Decimal.from_float(4e-5), degree,
                            transpose=direction == 'adjoint', progress=progress, deadline=started+11000)
                        pairing = source if direction == 'adjoint' else covector
                        values = [dot(pairing[:, :, 0], response[:, :, column]) for column in range(len(labels))]
                        directional[direction] = values
                        evidence.report['controls'].append(dict(branch=branch, direction=direction, moment_order=order,
                            **diagnostics, valid_for_claim=False))
                        output = evidence.output/(branch+'-'+str(digits)+'-order'+str(order)+'-'+direction+'.json')
                        output.write_text(json.dumps(dict(labels=labels, integrals=list(map(str, values)),
                            response=response.tolist(), source_terminal=terminal.tolist()), default=str)+'\n', encoding='utf-8')
                        evidence.own(output, 'outputs')
                        error = abs(sum(values, Decimal(0))-expected)
                        evidence.check(branch+'_'+str(digits)+'_'+str(order)+'_'+direction+'_old_weak_remainder_recovered', error <= gate,
                            dict(error=str(error), literal_gate=str(gate)))
                        if branch == 'reference':
                            evidence.check('reference_'+str(digits)+'_'+str(order)+'_'+direction+'_Gram_channels_exact_zero', values[3] == 0 and values[4] == 0)
                        evidence.save()
                    forward = directional['forward']
                    dual = directional.get('adjoint')
                    if dual is not None:
                        for label, first, last in zip(labels, forward, dual):
                            evidence.check(branch+'_'+label+'_independent_adjoint', abs(first-last) <= gate,
                                dict(error=str(abs(first-last)), literal_gate=str(gate)))
                        old_path = owned_json(evidence, 'annular-mixed-force-integrals-attempt01', branch+'-48-adjoint-channels.json')
                        error = max(map(abs, (terminal-dec_saved(old_path['source_terminal'])).flat))
                        evidence.check(branch+'_same_original_fine_adjoint', error < Decimal('1e-32'), str(error))
                    for label, value, backward in zip(labels, forward, dual if dual is not None else [None]*len(labels)):
                        evidence.report['cases'].append(dict(branch=branch, digits=digits, degree=degree, moment_order=order,
                            channel=label, integral=str(value), adjoint_integral=str(backward) if backward is not None else '',
                            prior_weak_remainder=str(expected), total=str(sum(forward, Decimal(0))),
                            literal_predecessor_gate=str(gate), valid_for_claim=False))
                    if comparisons:
                        compare_key = (32, 32) if order == 32 else (48, 32)
                        kind = 'time_precision_order_only' if order == 32 else 'spatial_moments_only'
                        for label, value, before in zip(labels, forward, comparisons[compare_key]):
                            error = abs(value-before)
                            evidence.report['refinement'].append(dict(branch=branch, channel=label, comparison=kind,
                                absolute_change=str(error), literal_predecessor_gate=str(gate), passed=bool(error <= gate), valid_for_claim=False))
                            evidence.check(branch+'_'+label+'_'+kind, error <= gate, str(error))
                    comparisons[(digits, order)] = forward
                    evidence.save()
        evidence.report['weak_residual_channels_qualified'] = True
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

from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_decimal_transport_v2_20260919 import DecimalAction, DecimalMap, decimal_array, dot
from annular_mixed_weak_maps_20260920 import MixedMap
from annular_mixed_force_cascade_20260920 import integrate_channels
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from run_annular_P2_continuum_bridge_20260918 import checked_load
from decimal import Decimal, localcontext
from scipy.sparse import csr_matrix
from time import perf_counter
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-mixed-force-integrals-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            original_action_unchanged=True, original_physical_force_mismatch_unchanged=True,
            full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
            parent_coefficient_precision='binary64', no_singular_inverse=True,
            physical_force_mismatch_fixed=False, frozen_operator_force_integrals_qualified=False,
            full_moving_force_decomposition_done=False, maximum_wall_seconds=10000)
        evidence.report['controls'], evidence.report['refinement'] = [], []
        fixture_path = evidence.output.parent/'annular-mixed-force-controls-attempt02/status.json'
        fixture = json.loads(fixture_path.read_text())
        evidence.own(fixture_path)
        evidence.check('independent_dense_and_dual_fixture_passed', fixture['state'] == 'complete' and all(row['passed'] for row in fixture['checks']))
        prior_path = evidence.output.parent/'annular-decimal-duality-attempt02/status.json'
        prior = json.loads(prior_path.read_text())
        evidence.own(prior_path)
        evidence.check('original_strict_duality_complete', prior['state'] == 'complete' and prior['original_strict_dual_gate_pass'])
        labels = ['mass_transfer_and_assembly', 'stiffness_transfer_and_assembly', 'mixed_weak_remainder']
        for branch in ['reference', 'MTS']:
            data = [checked_load(evidence, 'annular-action-exponential-response-attempt01', branch+'-'+level+'-action.npz')
                for level in ['coarse', 'fine']]
            initial = checked_load(evidence, 'annular-moving-duhamel-trajectory-attempt01', branch+'-point032.npz')
            endpoint = checked_load(evidence, 'annular-full-force-endpoints-attempt01', branch+'-spatial64-force-covector.npz')
            earlier = next(row for row in prior['cases'] if row['branch'] == branch and row['comparison'] == 'spatial64' and row['digits'] == 48)
            gate, expected = Decimal(earlier['unchanged_numerical_tolerance']), Decimal(earlier['frozen_operator_commutator'])
            previous = None
            for digits, degree, order in [(32, 48, 32), (48, 64, 64)]:
                with localcontext() as ctx:
                    ctx.prec = digits
                    actions = [DecimalAction(item) for item in data]
                    packet = owned_json(evidence, 'annular-mixed-weak-matrices-attempt01', branch+'-order'+str(order)+'-mixed-matrices.json')
                    maps = {name: MixedMap(item['rows'], item['columns']) for name, item in packet.items()}
                    transfer = DecimalMap(csr_matrix(endpoint['transfer']))
                    source = decimal_array(np.stack([initial['0_position'], -initial['0_reverse_velocity']]))[:, :, None]
                    covector = decimal_array(endpoint['covector'])[:, :, None]
                    duration = Decimal.from_float(4e-5)

                    def run(direction):
                        def progress(done, total):
                            evidence.report['progress'] = dict(branch=branch, digits=digits, order=order,
                                direction=direction, done=done, total=total, seconds=perf_counter()-started)
                            evidence.save()
                            print(json.dumps(evidence.report['progress']), flush=True)
                        result, terminal, diagnostics = integrate_channels(*actions, transfer, maps,
                            covector if direction == 'adjoint' else source, duration, degree,
                            transpose=direction == 'adjoint', progress=progress, deadline=started+10000)
                        evidence.report['controls'].append(dict(branch=branch, direction=direction, order=order,
                            **diagnostics, valid_for_claim=False))
                        output = evidence.output/(branch+'-'+str(digits)+'-'+direction+'-channels.json')
                        output.write_text(json.dumps(dict(response=result.tolist(), source_terminal=terminal.tolist()), default=str)+'\n', encoding='utf-8')
                        evidence.own(output, 'outputs')
                        evidence.save()
                        return result

                    forward = run('forward')
                    values = [dot(covector[:, :, 0], forward[:, :, column]) for column in range(3)]
                    error = abs(sum(values, Decimal(0))-expected)
                    evidence.check(branch+'_'+str(digits)+'_unchanged_prior_force_telescope', error <= gate,
                        dict(error=str(error), literal_gate=str(gate)))
                    if previous is not None:
                        for label, before, after in zip(labels, previous, values):
                            error = abs(after-before)
                            evidence.report['refinement'].append(dict(branch=branch, channel=label,
                                combined_precision_time_order_and_spatial_quadrature_change=str(error),
                                literal_predecessor_gate=str(gate), passed=bool(error <= gate), valid_for_claim=False))
                            evidence.check(branch+'_'+label+'_combined_refinement', error <= gate, str(error))
                    dual_values = [None]*3
                    if digits == 48:
                        adjoint = run('adjoint')
                        dual_values = [dot(source[:, :, 0], adjoint[:, :, column]) for column in range(3)]
                        for label, value, dual in zip(labels, values, dual_values):
                            evidence.check(branch+'_'+label+'_independent_forward_adjoint', abs(value-dual) <= gate,
                                dict(error=str(abs(value-dual)), literal_gate=str(gate)))
                    for label, value, dual in zip(labels, values, dual_values):
                        evidence.report['cases'].append(dict(branch=branch, digits=digits, degree=degree, moment_order=order,
                            channel=label, forward_integral=str(value), adjoint_integral=str(dual) if dual is not None else '',
                            prior_frozen_commutator=str(expected), total=str(sum(values, Decimal(0))),
                            literal_predecessor_gate=str(gate), full_physical_force_repair=False, valid_for_claim=False))
                    previous = values
                    evidence.save()
        evidence.report['frozen_operator_force_integrals_qualified'] = True
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

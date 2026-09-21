from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_decimal_transport_v2_20260919 import DecimalAction, DecimalMap, decimal_array, dot
from annular_mixed_weak_maps_20260920 import MixedMap
from annular_mixed_force_cascade_20260920 import integrate_channels
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from derive_annular_common_weak_action_20260920 import dec_saved
from run_annular_P2_continuum_bridge_20260918 import checked_load
from decimal import Decimal, localcontext
from scipy.sparse import csr_matrix
from time import perf_counter
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-mixed-force-refinement-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            original_action_unchanged=True, full_live_P2_force_convergence_proven=False,
            certified_continuous_time_bound=False, physical_force_mismatch_fixed=False,
            isolated_quadrature_and_time_precision_checked=False)
        status_path = evidence.output.parent/'annular-mixed-force-integrals-attempt01/status.json'
        prior = json.loads(status_path.read_text())
        evidence.own(status_path)
        evidence.check('completed_primal_and_dual_integrals', prior['state'] == 'complete'
            and prior['frozen_operator_force_integrals_qualified'] and all(row['passed'] for row in prior['checks']))
        with localcontext() as ctx:
            ctx.prec = 48
            for branch in ['reference', 'MTS']:
                data = [checked_load(evidence, 'annular-action-exponential-response-attempt01', branch+'-'+level+'-action.npz')
                    for level in ['coarse', 'fine']]
                initial = checked_load(evidence, 'annular-moving-duhamel-trajectory-attempt01', branch+'-point032.npz')
                endpoint = checked_load(evidence, 'annular-full-force-endpoints-attempt01', branch+'-spatial64-force-covector.npz')
                actions = [DecimalAction(item) for item in data]
                packet = owned_json(evidence, 'annular-mixed-weak-matrices-attempt01', branch+'-order32-mixed-matrices.json')
                maps = {name: MixedMap(item['rows'], item['columns']) for name, item in packet.items()}
                transfer = DecimalMap(csr_matrix(endpoint['transfer']))
                source = decimal_array(np.stack([initial['0_position'], -initial['0_reverse_velocity']]))[:, :, None]
                covector = decimal_array(endpoint['covector'])[:, :, None]

                def progress(done, total):
                    evidence.report['progress'] = dict(branch=branch, done=done, total=total, seconds=perf_counter()-started)
                    evidence.save()
                    print(json.dumps(evidence.report['progress']), flush=True)

                response, unused, diagnostics = integrate_channels(*actions, transfer, maps, source,
                    Decimal.from_float(4e-5), 64, progress=progress, deadline=started+3600)
                values = [dot(covector[:, :, 0], response[:, :, column]) for column in range(3)]
                labels = ['mass_transfer_and_assembly', 'stiffness_transfer_and_assembly', 'mixed_weak_remainder']
                for label, value in zip(labels, values):
                    low = next(row for row in prior['cases'] if row['branch'] == branch and row['digits'] == 32 and row['channel'] == label)
                    high = next(row for row in prior['cases'] if row['branch'] == branch and row['digits'] == 48 and row['channel'] == label)
                    gate = Decimal(high['literal_predecessor_gate'])
                    precision_error = abs(value-Decimal(low['forward_integral']))
                    quadrature_error = abs(value-Decimal(high['forward_integral']))
                    evidence.check(branch+'_'+label+'_time_order_and_precision_only', precision_error <= gate, str(precision_error))
                    evidence.check(branch+'_'+label+'_spatial_moment_order_only', quadrature_error <= gate, str(quadrature_error))
                    evidence.report['cases'].append(dict(branch=branch, channel=label, digits=48, degree=64, moment_order=32,
                        integral=str(value), time_order_and_precision_change=str(precision_error),
                        spatial_moment_order_change=str(quadrature_error), literal_predecessor_gate=str(gate), valid_for_claim=False))
                current = owned_json(evidence, 'annular-mixed-force-integrals-attempt01', branch+'-48-adjoint-channels.json')
                previous = owned_json(evidence, 'annular-decimal-duality-attempt02', branch+'-48-transport.json')
                error = max(map(abs, (dec_saved(current['source_terminal'])[:, :, 0]
                    -dec_saved(previous['backward_fine'])[:, :, 1]).flat))
                evidence.check(branch+'_original_full_force_adjoint_path_endpoint_retained', error < Decimal('1e-32'), str(error))
                output = evidence.output/(branch+'-48-order32-forward-channels.json')
                output.write_text(json.dumps(dict(response=response.tolist(), integrals=list(map(str, values))), default=str)+'\n', encoding='utf-8')
                evidence.own(output, 'outputs')
                evidence.save()
        evidence.report['isolated_quadrature_and_time_precision_checked'] = True
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

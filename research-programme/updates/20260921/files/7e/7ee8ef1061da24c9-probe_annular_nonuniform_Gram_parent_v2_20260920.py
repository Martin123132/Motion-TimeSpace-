from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_nonuniform_Gram_candidate_20260920 import gram_action, template_rows
from annular_common_P2_overlay_20260919 import evaluation_rows, compose_rows
from derive_annular_exact_source_trace_comparison_20260920 import jump_row, rational_rows
from derive_annular_common_weak_action_20260920 import dec_saved
from annular_decimal_transport_v2_20260919 import DecimalAction, decimal_array
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from derive_annular_moving_Gram_profile_20260919 import evaluate_pair
from acquire_annular_common_action_weights_20260920 import densities
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from run_annular_P2_continuum_bridge_20260918 import checked_load
from decimal import Decimal, localcontext
from fractions import Fraction
from scipy.sparse import diags
from time import perf_counter
import contextlib
import json
import numpy as np


def mesh_from_packet(packet):
    return dict(packet, nodes=list(map(Fraction, packet['nodes'])),
        edges=list(map(Fraction, packet['edges'])), anchor=Fraction(packet['anchor']))


def sample_field(mesh, values, knots):
    rows = evaluation_rows(mesh, knots)
    result = []
    for row in rows:
        result.append(sum((np.longdouble(coefficient.numerator)/np.longdouble(coefficient.denominator)*np.longdouble(values[column])
            for column, coefficient in row.items()), np.longdouble(0)))
    return np.asarray(result, dtype=np.longdouble)


def field_jump(mesh, values):
    row = jump_row(mesh)
    return sum((np.longdouble(coefficient.numerator)/np.longdouble(coefficient.denominator)*np.longdouble(values[column])
        for column, coefficient in row.items()), np.longdouble(0))


def main():
    evidence = EvidenceRun('annular-nonuniform-Gram-parent-probes-attempt02', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            original_live_action_unchanged=True, candidate_only=True, nonuniform_parent_uniqueness_proven=False,
            physical_force_mismatch_fixed=False, full_live_P2_force_convergence_proven=False,
            certified_continuous_time_bound=False, actual_time_integrated_force_test=False,
            evolving_front_resolution_proven=False, saved_profile_knots_retained=True,
            evaluation_scope='fixed saved primal/adjoint profiles and original frozen coarse geometry')
        control_path = evidence.output.parent/'annular-nonuniform-Gram-controls-attempt01/status.json'
        controls = json.loads(control_path.read_text())
        evidence.own(control_path)
        evidence.check('candidate_controls_qualified', controls['state'] == 'complete'
            and controls['uniform_recovery_qualified'] and controls['variation_qualified']
            and all(row['passed'] for row in controls['checks']))
        evidence.report['meshes'], evidence.report['sources'] = [], []
        for branch in ['reference', 'MTS']:
            packet = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
            coarse_mesh, fine_mesh = [mesh_from_packet(item) for item in packet['native']]
            anchor = Fraction(packet['overlay']['anchor'])
            source_reference = np.longdouble(anchor.numerator)/np.longdouble(anchor.denominator)
            for level in range(2):
                identity = compose_rows(rational_rows(packet['left_inverses'][level]), rational_rows(packet['embeddings'][level]))
                evidence.check(branch+'_'+str(level)+'_exact_native_recovery_from_common_field',
                    all(row == {index:Fraction(1)} for index, row in enumerate(identity)))
            native = checked_load(evidence, 'annular-action-exponential-response-attempt01', branch+'-fine-action.npz')
            initial = checked_load(evidence, 'annular-moving-duhamel-trajectory-attempt01', branch+'-point032.npz')
            force = checked_load(evidence, 'annular-full-force-endpoints-attempt01', branch+'-spatial64-force-covector.npz')
            forward = owned_json(evidence, 'annular-weak-residual-force-attempt01', branch+'-48-order64-forward.json')
            adjoint = owned_json(evidence, 'annular-weak-residual-force-attempt01', branch+'-48-order64-adjoint.json')
            saved = checked_load(evidence, 'annular-live-compensated-rate-attempt01', branch+'-1e-07-compensated-rate.npz')
            with localcontext() as ctx:
                ctx.prec = 48
                action = DecimalAction(native)
                adjoint_initial = action.solve(dec_saved(adjoint['source_terminal'])[1])[:, 0]
                adjoint_final = action.solve(decimal_array(force['covector'])[1, :, None])[:, 0]
                profiles = [('initial', np.asarray(initial['0_position'], dtype=np.longdouble),
                        np.array([np.longdouble(str(value)) for value in adjoint_initial])),
                    ('final', np.array([np.longdouble(str(value)) for value in dec_saved(forward['source_terminal'])[0, :, 0]]),
                        np.array([np.longdouble(str(value)) for value in adjoint_final]))]
            systems = [IndexedGradedP2System(257, branch == 'MTS', 2e-5), IndexedGradedP2System(513, branch == 'MTS', 1e-5)]
            pair = evaluate_pair(systems, [saved[str(level)+'_state'] for level in range(2)])
            layer, position = pair[0]['layer'], pair[0]['values'][-1]
            coefficient_source = checked_load(evidence, 'annular-common-action-weights-attempt01', branch+'-native-and-cuts.npz')
            unused, gradient = densities(layer, position, pair[1]['layer'].radii)
            reproduced = pair[1]['layer'].sampling @ gradient/pair[1]['layer'].gram_spacing
            expected = coefficient_source['fine_gram_weights_at_coarse_geometry']
            coefficient_error = float(np.max(abs(reproduced-expected), initial=0.)/max(1., np.max(abs(expected), initial=0.)))
            evidence.check(branch+'_original_frozen_geometry_reproduced', coefficient_error < 3e-12, coefficient_error)
            meshes = [('uniform513', list(map(Fraction, systems[1].model.base_radii)))]
            knots = sorted(map(Fraction, packet['overlay']['nodes']))
            for level in range(3):
                if level:
                    refined = sorted(set(knots+[(first+last)/2 for first, last in zip(knots, knots[1:])])-{anchor})
                    evidence.check(branch+'_'+str(level)+'_nested_knots', set(knots) <= set(refined))
                    knots = refined
                evidence.check(branch+'_'+str(level)+'_all_common_P2_nodes_retained',
                    set(map(Fraction, packet['overlay']['nodes'])) <= set(knots))
                meshes.append(('profile'+str(level), knots))
            for mesh_label, knots in meshes:
                coordinate = np.array([np.longdouble(value.numerator)/np.longdouble(value.denominator) for value in knots])
                unused, coefficient = densities(layer, position, np.asarray(coordinate, dtype=float))
                evidence.check(branch+'_'+mesh_label+'_positive_parent_weight', np.all(np.isfinite(coefficient)) and np.all(coefficient > 0))
                gaps = np.diff(coordinate)
                windows = np.stack([gaps[offset:len(coordinate)-3+offset] for offset in range(3)], axis=1)
                width = np.mean(windows, axis=1)
                variation = np.sum((windows-width[:, None])**2, axis=1)/np.sum(windows**2, axis=1)
                template, unused = template_rows(len(coordinate))
                evidence.report['meshes'].append(dict(branch=branch, label=mesh_label, count=len(knots),
                    minimum_gap=float(min(gaps)), maximum_gap=float(max(gaps)),
                    maximum_local_ratio=float(np.max(np.max(windows, axis=1)/np.min(windows, axis=1))),
                    native_fields_representable_without_mode_loss=mesh_label != 'uniform513', valid_for_claim=False))
                for endpoint, trial, test in profiles:
                    trial_values, test_values = sample_field(coarse_mesh, trial, knots), sample_field(fine_mesh, test, knots)
                    trial_jump, test_jump = field_jump(coarse_mesh, trial), field_jump(fine_mesh, test)
                    trial_action = gram_action(coordinate, trial_values, trial_jump, source_reference,
                        coefficient, include_gram=branch == 'MTS')
                    test_action = gram_action(coordinate, test_values, test_jump, source_reference,
                        coefficient, include_gram=branch == 'MTS')
                    for extension in ['primary', 'nonunique_control']:
                        trial_factor, test_factor = trial_action['factor'], test_action['factor']
                        if extension == 'nonunique_control' and branch == 'MTS':
                            operator = template @ diags(1+variation) @ trial_action['kernel']
                            hinge = np.maximum(coordinate-source_reference, 0.)
                            trial_factor = operator @ (trial_values-trial_jump*hinge)
                            test_factor = operator @ (test_values-test_jump*hinge)
                        weight = trial_action['row_weight']
                        trial_energy = np.dot(weight, trial_factor**2)/2
                        test_energy = np.dot(weight, test_factor**2)/2
                        bilinear = np.dot(weight*trial_factor, test_factor)
                        bound = 2*np.sqrt(trial_energy*test_energy)
                        evidence.check(branch+'_'+mesh_label+'_'+endpoint+'_'+extension+'_positive_Cauchy_pair',
                            trial_energy >= 0 and test_energy >= 0 and abs(bilinear) <= bound*(1+1e-12)+1e-28)
                        if branch == 'reference':
                            evidence.check(mesh_label+'_'+endpoint+'_'+extension+'_reference_exact_zero',
                                trial_energy == 0 and test_energy == 0 and bilinear == 0)
                        evidence.report['cases'].append(dict(branch=branch, mesh=mesh_label, endpoint=endpoint,
                            extension=extension, knot_count=len(knots), trial_jump=str(trial_jump), test_jump=str(test_jump),
                            trial_energy=str(trial_energy), test_energy=str(test_energy), bilinear=str(bilinear),
                            Cauchy_bound=str(bound), actual_time_integrated_force=False, valid_for_claim=False))
                    output = evidence.output/(branch+'-'+mesh_label+'-'+endpoint+'-profile.npz')
                    np.savez_compressed(output, knots=coordinate, trial=trial_values, test=test_values,
                        coefficient=coefficient, trial_jump=trial_jump, test_jump=test_jump,
                        primary_trial_factor=trial_action['factor'], primary_test_factor=test_action['factor'])
                    evidence.own(output, 'outputs')
                evidence.report['progress'] = dict(branch=branch, mesh=mesh_label, seconds=perf_counter()-started)
                evidence.save()
                print(json.dumps(evidence.report['progress']), flush=True)
            evidence.report['sources'].append(dict(branch=branch, coefficient_reproduction_error=coefficient_error,
                frozen_source_position=float(position), parent_inputs='binary64 with saved 48-digit propagation',
                profile_arithmetic='platform numpy.longdouble; no extra physical precision', valid_for_claim=False))
        evidence.report.update(seconds=perf_counter()-started, fixed_saved_profile_probe_complete=True)
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

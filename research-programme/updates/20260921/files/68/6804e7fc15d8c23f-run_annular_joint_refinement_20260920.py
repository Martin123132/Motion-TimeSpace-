from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_common_frozen_candidate_20260920 import FrozenCandidate
from annular_decimal_transport_v2_20260919 import propagate
from annular_common_weighted_moments_20260920 import apply_rational_rows
from annular_common_P2_overlay_20260919 import evaluation_rows, compose_rows
from derive_annular_common_weak_action_20260920 import dec_saved
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from run_annular_common_frozen_candidate_20260920 import energy, relative_phase_error, force_at
from build_annular_joint_refinement_20260920 import rational_mesh
from decimal import Decimal, localcontext
from fractions import Fraction
from time import perf_counter
from datetime import datetime, timezone
import contextlib
import json
import numpy as np


BUILD = 'annular-joint-candidate-refinement-build-attempt01'
CASES = [('reference', 'reference'), ('MTS', 'primary'), ('MTS', 'alternative')]


def main():
    evidence = EvidenceRun('annular-joint-candidate-refinement-response-attempt01', __file__)
    started = perf_counter()
    deadline = started+min(10800, (datetime(2026, 9, 20, 21, 50, tzinfo=timezone.utc)-datetime.now(timezone.utc)).total_seconds())
    try:
        evidence.report.update(github_action=False, subagents_used=False, candidate_only=True,
            original_live_action_unchanged=True, no_new_live_evolution=True, frozen_background_only=True,
            homogeneous_scalar_block_only=True, moving_source_evolved=False, source_force_diagnostic_only=True,
            physical_force_mismatch_fixed=False, self_consistent_candidate_metric_solved=False,
            full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
            actual_time_integrated_force_test=False, nonuniform_parent_uniqueness_proven=False,
            refined_pilot_arithmetic_qualified=False, spatial_convergence_proven=False,
            maximum_wall_seconds=max(0, deadline-started),
            arithmetic_gates=dict(energy32='1e-20', energy48='1e-34', phase_refinement='1e-20',
                source_diagnostic_refinement='1e-19', reverse_phase='1e-32'))
        for key in ['forces', 'refinement', 'reversal', 'spatial', 'extension_sensitivity']:
            evidence.report[key] = []
        build_path = evidence.output.parent/BUILD/'status.json'
        build = json.loads(build_path.read_text())
        evidence.own(build_path)
        evidence.check('both_refinement_levels_qualified', build['state'] == 'complete'
            and build['joint_refinement_assembly_qualified'] and all(row['passed'] for row in build['checks'])
            and len(build['cases']) == 6 and max(row['steps_at_4e_5'] for row in build['cases']) <= 512)
        old_path = evidence.output.parent/'annular-common-candidate-response-attempt01/status.json'
        old = json.loads(old_path.read_text())
        evidence.own(old_path)
        evidence.check('base_pilot_complete', old['state'] == 'complete'
            and old['frozen_scalar_response_arithmetic_qualified'] and all(row['passed'] for row in old['checks']))
        results, meshes = {}, {}
        for branch, extension in CASES:
            label = branch+'-'+extension
            results[(label, 0, 48)] = owned_json(evidence, 'annular-common-candidate-response-attempt01', label+'-48-endpoint.json')
            if (branch, 0) not in meshes:
                packet = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
                meshes[(branch, 0)] = rational_mesh(packet['overlay'])
        base_sensitivity = dict(old['extension_sensitivity'][0])
        base_sensitivity.update(level=0, count=1094)
        evidence.report['extension_sensitivity'].append(base_sensitivity)
        duration = Decimal.from_float(4e-5)
        evidence.report['duration_original_binary64_exact'] = str(duration)
        for level in [1, 2]:
            for branch, extension in CASES:
                label = branch+'-'+extension
                packet = owned_json(evidence, BUILD, label+'-L'+str(level)+'-action.json')
                mesh_packet = owned_json(evidence, BUILD, branch+'-L'+str(level)+'-mesh.json')
                mesh = rational_mesh(mesh_packet['mesh'])
                meshes[(branch, level)] = mesh
                preceding = meshes[(branch, level-1)]
                embedding = evaluation_rows(preceding, mesh['nodes'])
                restriction = evaluation_rows(mesh, preceding['nodes'])
                evidence.check(label+'_L'+str(level)+'_adjacent_exact_recovery', all(row == {index:Fraction(1)}
                    for index, row in enumerate(compose_rows(restriction, embedding))))
                for digits, degree, energy_gate in [(32, 48, Decimal('1e-20')), (48, 64, Decimal('1e-34'))]:
                    with localcontext() as ctx:
                        ctx.prec = digits
                        action = FrozenCandidate(packet)
                        initial = dec_saved(packet['phase'])[:, :, None]
                        initial_energy = energy(action, initial)

                        def progress(done, total):
                            evidence.report['progress'] = dict(case=label, level=level, digits=digits,
                                operation='forward', completed_substeps=done, total_substeps=total,
                                seconds=perf_counter()-started)
                            evidence.save()
                            print(json.dumps(evidence.report['progress']), flush=True)

                        endpoint, diagnostics = propagate(action, initial, duration, degree, progress=progress, deadline=deadline)
                        final_energy = energy(action, endpoint)
                        drift = abs(final_energy-initial_energy)/initial_energy
                        check_prefix = label+'_L'+str(level)+'_'+str(digits)
                        evidence.check(check_prefix+'_energy', drift < energy_gate, str(drift))
                        forces = {point:force_at(action, phase, packet['dust'])
                            for point, phase in [('initial', initial), ('final', endpoint)]}
                        evidence.check(check_prefix+'_field_inertia_nonnegative',
                            all(item['field_inertia_complement'] >= 0 for item in forces.values()))
                        for point, force in forces.items():
                            evidence.report['forces'].append(dict(branch=branch, extension=extension, level=level,
                                count=action.count, digits=digits, endpoint=point,
                                **{name:str(value) for name, value in force.items()},
                                diagnostic_not_coupled=True, valid_for_claim=False))
                        result = dict(branch=branch, extension=extension, level=level, count=action.count,
                            digits=digits, phase=endpoint.tolist(), force={name:str(value) for name, value in forces['final'].items()},
                            homogeneous_scalar_block_only=True, valid_for_claim=False)
                        output = evidence.output/(label+'-L'+str(level)+'-'+str(digits)+'-endpoint.json')
                        output.write_text(json.dumps(result, default=str)+'\n', encoding='utf-8')
                        evidence.own(output, 'outputs')
                        results[(label, level, digits)] = result
                        evidence.report['cases'].append(dict(branch=branch, extension=extension, level=level,
                            count=action.count, initial_energy=str(initial_energy), final_energy=str(final_energy),
                            relative_energy_drift=str(drift), energy_gate=str(energy_gate),
                            frequency_bound=str(action.frequency_bound), **diagnostics, valid_for_claim=False))
                        evidence.save()
                        if digits == 48:
                            low = results[(label, level, 32)]
                            error = relative_phase_error(action, endpoint-dec_saved(low['phase']), endpoint)
                            force_error = abs(forces['final']['reduced_wave_force']-Decimal(low['force']['reduced_wave_force']))
                            force_scale = max(abs(forces['final']['reduced_wave_force']), Decimal('1e-40'))
                            evidence.check(check_prefix+'_precision_order_phase', error < Decimal('1e-20'), str(error))
                            evidence.check(check_prefix+'_precision_order_source', force_error/force_scale < Decimal('1e-19'), str(force_error/force_scale))
                            evidence.report['refinement'].append(dict(branch=branch, extension=extension, level=level,
                                relative_phase_energy_error=str(error), absolute_source_diagnostic_change=str(force_error),
                                relative_source_diagnostic_change=str(force_error/force_scale),
                                not_a_physical_force_gate=True, valid_for_claim=False))
                            before = results[(label, level-1, 48)]
                            embedded = np.stack([apply_rational_rows(embedding, values) for values in dec_saved(before['phase'])])
                            spatial_phase = relative_phase_error(action, endpoint-embedded, endpoint)
                            spatial_force = forces['final']['reduced_wave_force']-Decimal(before['force']['reduced_wave_force'])
                            evidence.report['spatial'].append(dict(branch=branch, extension=extension, level=level,
                                count=action.count, previous_count=preceding['count'], relative_phase_difference=str(spatial_phase),
                                signed_source_diagnostic_change=str(spatial_force),
                                relative_source_diagnostic_change=str(abs(spatial_force)/force_scale),
                                final_source_diagnostic=str(forces['final']['reduced_wave_force']),
                                not_a_continuum_error_bound=True, valid_for_claim=False))

                            def reverse_progress(done, total):
                                evidence.report['progress'] = dict(case=label, level=level, digits=digits,
                                    operation='reverse', completed_substeps=done, total_substeps=total,
                                    seconds=perf_counter()-started)
                                evidence.save()
                                print(json.dumps(evidence.report['progress']), flush=True)

                            recovered, reverse_diagnostics = propagate(action, endpoint, -duration, degree,
                                progress=reverse_progress, deadline=deadline)
                            error = relative_phase_error(action, recovered-initial, initial)
                            evidence.check(check_prefix+'_all_mode_reversal', error < Decimal('1e-32'), str(error))
                            evidence.report['reversal'].append(dict(branch=branch, extension=extension, level=level,
                                relative_phase_energy_error=str(error), **reverse_diagnostics, valid_for_claim=False))
                            reverse_path = evidence.output/(label+'-L'+str(level)+'-48-reversed.json')
                            reverse_path.write_text(json.dumps(dict(phase=recovered.tolist(), diagnostics=reverse_diagnostics,
                                valid_for_claim=False), default=str)+'\n', encoding='utf-8')
                            evidence.own(reverse_path, 'outputs')
                            evidence.save()
            with localcontext() as ctx:
                ctx.prec = 48
                primary = owned_json(evidence, BUILD, 'MTS-primary-L'+str(level)+'-action.json')
                alternative = owned_json(evidence, BUILD, 'MTS-alternative-L'+str(level)+'-action.json')
                evidence.check('L'+str(level)+'_extensions_share_non_Gram_inputs', primary['phase'] == alternative['phase']
                    and primary['dust'] == alternative['dust'] and all(primary['maps'][name] == alternative['maps'][name]
                        for name in primary['maps'] if name not in ['stiffness', 'stiffness_X']))
                action = FrozenCandidate(primary)
                first, last = [results[('MTS-'+name, level, 48)] for name in ['primary', 'alternative']]
                difference = relative_phase_error(action, dec_saved(last['phase'])-dec_saved(first['phase']), dec_saved(first['phase']))
                force_difference = Decimal(last['force']['reduced_wave_force'])-Decimal(first['force']['reduced_wave_force'])
                evidence.report['extension_sensitivity'].append(dict(level=level, count=action.count,
                    comparison='alternative minus primary, same MTS background and initial field',
                    relative_phase_difference_in_primary_energy_norm=str(difference),
                    reduced_source_diagnostic_difference=str(force_difference),
                    relative_source_diagnostic_difference=str(abs(force_difference/Decimal(first['force']['reduced_wave_force']))),
                    a_selection_or_rejection_criterion=False, valid_for_claim=False))
                evidence.save()
                print(json.dumps(dict(level_complete=level, sensitivity=evidence.report['extension_sensitivity'][-1],
                    seconds=perf_counter()-started)), flush=True)
        sensitivity = evidence.report['extension_sensitivity']
        evidence.report['decision'] = dict(
            absolute_extension_difference_shrinks_on_both_refinements=all(
                abs(Decimal(last['reduced_source_diagnostic_difference'])) < abs(Decimal(first['reduced_source_diagnostic_difference']))
                for first, last in zip(sensitivity, sensitivity[1:])),
            relative_extension_difference_shrinks_on_both_refinements=all(
                Decimal(last['relative_source_diagnostic_difference']) < Decimal(first['relative_source_diagnostic_difference'])
                for first, last in zip(sensitivity, sensitivity[1:])),
            physical_winner_selected=False, continuum_limit_proven=False, valid_for_claim=False)
        evidence.report.update(refined_pilot_arithmetic_qualified=True, seconds=perf_counter()-started)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=evidence.report['seconds'],
            sensitivity=sensitivity, decision=evidence.report['decision'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

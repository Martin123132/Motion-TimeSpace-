from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_common_frozen_candidate_20260920 import FrozenCandidate, source_force
from annular_decimal_transport_v2_20260919 import propagate, dot
from derive_annular_common_weak_action_20260920 import dec_saved
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from decimal import Decimal, localcontext
from time import perf_counter
import contextlib
import json
import numpy as np


ZERO = Decimal(0)


def energy(action, phase):
    position, velocity = phase[0], phase[1]
    return (dot(velocity, action.maps['mass'].apply(velocity))
        +dot(position, action.stiffness(position)))/2


def relative_phase_error(action, difference, reference):
    numerator, denominator = energy(action, difference), energy(action, reference)
    if numerator < 0 or denominator <= 0:
        raise ValueError('Nonpositive phase energy metric.')
    return (numerator/denominator).sqrt()


def force_at(action, phase, dust):
    return source_force(action, phase[0, :, 0], phase[1, :, 0],
        Decimal.from_float(dust['source_velocity']), Decimal.from_float(dust['dust_inertia']),
        Decimal.from_float(dust['dust_drive']))


def main():
    evidence = EvidenceRun('annular-common-candidate-response-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False,
            no_new_evolution=False, no_new_live_evolution=True, original_live_action_unchanged=True,
            candidate_only=True, frozen_background_only=True, homogeneous_scalar_block_only=True,
            moving_source_evolved=False, source_force_diagnostic_only=True,
            physical_force_mismatch_fixed=False, full_live_P2_force_convergence_proven=False,
            certified_continuous_time_bound=False, self_consistent_candidate_metric_solved=False,
            actual_time_integrated_force_test=False, nonuniform_parent_uniqueness_proven=False,
            frozen_scalar_response_arithmetic_qualified=False, maximum_wall_seconds=7200,
            propagator='u_dot=v, v_dot=-M_inverse K u; V and geometry do not evolve',
            force_scope='Full prescribed-background source Schur diagnostic at homogeneous scalar endpoints, not coupled evolution or a force convergence test.',
            arithmetic_gates=dict(energy32='1e-20', energy48='1e-34', phase_refinement='1e-20',
                source_diagnostic_refinement='1e-19', reverse_phase='1e-32'),
            original_physical_mismatch_percentages_unchanged=True)
        controls_path = evidence.output.parent/'annular-complete-candidate-controls-attempt01/status.json'
        controls = json.loads(controls_path.read_text())
        evidence.own(controls_path)
        evidence.check('independent_controls_complete', controls['state'] == 'complete'
            and all(item['passed'] for item in controls['checks'])
            and controls['full_source_Euler_controls_qualified'] and controls['frozen_scalar_propagator_qualified'])
        evidence.report['refinement'], evidence.report['reversal'], evidence.report['forces'] = [], [], []
        results, packets = {}, {}
        duration = Decimal.from_float(4e-5)
        evidence.report['duration_original_binary64_exact'] = str(duration)
        cases = [('reference', 'reference'), ('MTS', 'primary'), ('MTS', 'alternative')]
        for branch, extension in cases:
            label = branch+'-'+extension
            packet = owned_json(evidence, 'annular-complete-frozen-candidate-attempt01', label+'-action.json')
            packets[label] = packet
            evidence.check(label+'_all_common_dofs_retained', packet['count'] == 1094)
            for digits, degree, energy_gate in [(32, 48, Decimal('1e-20')), (48, 64, Decimal('1e-34'))]:
                with localcontext() as ctx:
                    ctx.prec = digits
                    action = FrozenCandidate(packet)
                    initial = dec_saved(packet['phase'])[:, :, None]
                    initial_energy = energy(action, initial)

                    def progress(done, total):
                        evidence.report['progress'] = dict(case=label, digits=digits, operation='forward',
                            completed_substeps=done, total_substeps=total, seconds=perf_counter()-started)
                        evidence.save()
                        print(json.dumps(evidence.report['progress']), flush=True)

                    endpoint, diagnostics = propagate(action, initial, duration, degree,
                        progress=progress, deadline=started+7200)
                    final_energy = energy(action, endpoint)
                    drift = abs(final_energy-initial_energy)/initial_energy
                    evidence.check(label+'_'+str(digits)+'_energy_conservation', drift < energy_gate, str(drift))
                    forces = {name:force_at(action, phase, packet['dust'])
                        for name, phase in [('initial', initial), ('final', endpoint)]}
                    evidence.check(label+'_'+str(digits)+'_nonnegative_field_inertia',
                        all(item['field_inertia_complement'] >= ZERO for item in forces.values()))
                    for point, force in forces.items():
                        evidence.report['forces'].append(dict(branch=branch, extension=extension, digits=digits,
                            endpoint=point, **{name:str(value) for name, value in force.items()},
                            diagnostic_not_coupled=True, valid_for_claim=False))
                    results[(label, digits)] = dict(phase=endpoint.copy(), force=forces['final'])
                    output = evidence.output/(label+'-'+str(digits)+'-endpoint.json')
                    output.write_text(json.dumps(dict(branch=branch, extension=extension, digits=digits,
                        degree=degree, duration=str(duration), phase=endpoint.tolist(), diagnostics=diagnostics,
                        force={name:str(value) for name, value in forces['final'].items()},
                        homogeneous_scalar_block_only=True, valid_for_claim=False), default=str)+'\n', encoding='utf-8')
                    evidence.own(output, 'outputs')
                    evidence.report['cases'].append(dict(branch=branch, extension=extension,
                        count=action.count, initial_energy=str(initial_energy), final_energy=str(final_energy),
                        relative_energy_drift=str(drift), energy_arithmetic_gate=str(energy_gate),
                        frequency_bound=str(action.frequency_bound), **diagnostics, valid_for_claim=False))
                    evidence.save()
                    if digits == 48:
                        coarse = results[(label, 32)]
                        error = relative_phase_error(action, endpoint-coarse['phase'], endpoint)
                        force_error = abs(forces['final']['reduced_wave_force']-coarse['force']['reduced_wave_force'])
                        force_scale = max(abs(forces['final']['reduced_wave_force']), Decimal('1e-40'))
                        evidence.check(label+'_phase_precision_order_refinement', error < Decimal('1e-20'), str(error))
                        evidence.check(label+'_source_diagnostic_precision_order_refinement',
                            force_error/force_scale < Decimal('1e-19'), str(force_error/force_scale))
                        evidence.report['refinement'].append(dict(branch=branch, extension=extension,
                            relative_phase_energy_error=str(error), absolute_source_diagnostic_change=str(force_error),
                            relative_source_diagnostic_change=str(force_error/force_scale), phase_gate='1e-20', force_gate='1e-19',
                            not_a_physical_force_gate=True, valid_for_claim=False))

                        def reverse_progress(done, total):
                            evidence.report['progress'] = dict(case=label, digits=digits, operation='reverse',
                                completed_substeps=done, total_substeps=total, seconds=perf_counter()-started)
                            evidence.save()
                            print(json.dumps(evidence.report['progress']), flush=True)

                        recovered, reverse_diagnostics = propagate(action, endpoint, -duration, degree,
                            progress=reverse_progress, deadline=started+7200)
                        error = relative_phase_error(action, recovered-initial, initial)
                        evidence.check(label+'_all_mode_reversal', error < Decimal('1e-32'), str(error))
                        evidence.report['reversal'].append(dict(branch=branch, extension=extension,
                            relative_phase_energy_error=str(error), arithmetic_gate='1e-32',
                            **reverse_diagnostics, valid_for_claim=False))
                        reverse_path = evidence.output/(label+'-48-reversed.json')
                        reverse_path.write_text(json.dumps(dict(phase=recovered.tolist(), diagnostics=reverse_diagnostics,
                            valid_for_claim=False), default=str)+'\n', encoding='utf-8')
                        evidence.own(reverse_path, 'outputs')
                        evidence.save()
        with localcontext() as ctx:
            ctx.prec = 48
            primary, alternative = [packets['MTS-'+name] for name in ['primary', 'alternative']]
            evidence.check('extensions_share_all_non_Gram_inputs', primary['phase'] == alternative['phase']
                and primary['dust'] == alternative['dust'] and all(primary['maps'][name] == alternative['maps'][name]
                    for name in primary['maps'] if name not in ['stiffness', 'stiffness_X']))
            action = FrozenCandidate(primary)
            first, last = [results[('MTS-'+name, 48)] for name in ['primary', 'alternative']]
            difference = relative_phase_error(action, last['phase']-first['phase'], first['phase'])
            force_difference = last['force']['reduced_wave_force']-first['force']['reduced_wave_force']
            evidence.report['extension_sensitivity'] = [dict(
                comparison='alternative minus primary, same MTS background and initial state',
                relative_phase_difference_in_primary_energy_norm=str(difference),
                reduced_source_diagnostic_difference=str(force_difference),
                relative_source_diagnostic_difference=str(abs(force_difference/first['force']['reduced_wave_force'])),
                a_selection_or_rejection_criterion=False, valid_for_claim=False)]
        evidence.report.update(frozen_scalar_response_arithmetic_qualified=True, seconds=perf_counter()-started)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', seconds=evidence.report['seconds'], checks=len(evidence.report['checks']),
            refinement=evidence.report['refinement'], sensitivity=evidence.report['extension_sensitivity'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

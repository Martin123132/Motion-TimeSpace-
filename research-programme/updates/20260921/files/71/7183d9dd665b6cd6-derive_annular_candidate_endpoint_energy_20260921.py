from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_hamiltonian_20260921 import symbolic_energy_checks, decimals, energy_channels
from annular_candidate_midpoint_20260921 import LiveCommonEvaluation, midpoint_step
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from annular_candidate_canonical_response_20260920 import common_material
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from derive_annular_candidate_midpoint_20260921 import saved_matrix
from run_annular_P2_continuum_bridge_20260918 import checked_load
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from decimal import Decimal, localcontext
from time import perf_counter
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-candidate-endpoint-energy-attempt01', __file__)
    started = perf_counter()
    deadline = started+9000
    try:
        prior_path = evidence.output.parent/'annular-candidate-coupled-midpoint-final-integrity.json'
        prior = json.loads(prior_path.read_text())
        evidence.own(prior_path)
        evidence.check('coupled_midpoint_sources_complete', prior['state'] == 'complete' and prior['trajectories_qualified']
            and prior['independent_quadrature_qualified'] and prior['independent_reverse_qualified']
            and all(row['passed'] for row in prior['checks']))
        evidence.report.update(github_action=False, subagents_used=False, candidate_only=True, polar_zero_shift_only=True,
            original_live_action_unchanged=True, new_coupled_evolution=False, modes_deleted=False,
            physical_force_mismatch_fixed=False, spatial_convergence_proven=False, full_live_P2_force_convergence_proven=False,
            general_nonzero_shift_or_temporal_current_derived=False, exact_finite_label_Galerkin_evolution_qualified=False,
            global_stability_proven=False, endpoint_velocities_recovered=False, full_hamiltonian_computed=False,
            total_energy_conservation_proven=False, energy_time_order_resolved=False,
            boundary_energy_identity_symbolically_derived=False, weak_field_dust_energy_form_derived=False,
            no_Newton_constant_derivation=True, initial_to_final_interval=1e-7, interval_not_assigned_seconds=True,
            iterations=[], drifts=[], refinement=[], quadrature=[], energy_smoke_relative_tolerance=1e-9,
            Legendre_boundary_relative_tolerance=2e-9, long_run_not_started=True)
        symbolic_energy_checks(evidence)
        evidence.report.update(boundary_energy_identity_symbolically_derived=True, weak_field_dust_energy_form_derived=True)
        for branch, extension in [('reference', 'reference'), ('MTS', 'primary'), ('MTS', 'alternative')]:
            case = branch+'-'+extension
            native = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            saved = checked_load(evidence, 'annular-candidate-initial-metric-attempt02', branch+'-velocity-owned-inputs.npz')
            packet = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
            owner, unused, unused_rates = common_material(native, saved, packet)
            action = owned_json(evidence, 'annular-complete-frozen-candidate-attempt01', case+'-action.json')
            preconditioner = BandedSourceInverse(saved_matrix(evidence, case+'-22-fixed-metric-mass.npz'), (15, 1095))
            rows = {}
            specifications = [('initial', 'annular-candidate-coupled-midpoint-attempt01', 'initial', 10, 32),
                ('one_step', 'annular-candidate-coupled-midpoint-attempt01', 'forward1-step1', 10, 32),
                ('two_steps', 'annular-candidate-coupled-midpoint-attempt01', 'forward2-step2', 10, 32),
                ('four_steps', 'annular-candidate-coupled-midpoint-attempt01', 'forward4-step4', 10, 32),
                ('fine_initial', 'annular-candidate-midpoint-quadrature-attempt01', 'initial', 16, 48),
                ('fine_step', 'annular-candidate-midpoint-quadrature-attempt01', 'fine-step', 16, 48)]
            for label, folder, suffix, reference_order, material_order in specifications:
                name = case+'-'+label
                source_name = case+'-'+suffix+'.npz'
                source = checked_load(evidence, folder, source_name)
                coordinates, momenta = decimals(source['coordinates']), decimals(source['momenta'])
                seed = source['midpoint_rates'].copy()
                evaluator = LiveCommonEvaluation(owner, packet['overlay'], action, extension, deadline,
                    reference_order=reference_order, material_order=material_order)
                print(json.dumps(dict(case=name, operation='recover_endpoint_velocity', seconds=perf_counter()-started)), flush=True)
                def record(row, midpoint, rates, current, residual):
                    evidence.report['iterations'].append(dict(case=name, **row, valid_for_claim=False))
                    evidence.report['progress'] = dict(case=name, iteration=row['iteration'],
                        relative_residual=row['relative_residual'], maximum_correction=row['maximum_correction'],
                        seconds=perf_counter()-started)
                    evidence.save()
                    print(json.dumps(evidence.report['progress']), flush=True)
                    np.savez_compressed(evidence.output/'latest-endpoint-recovery.npz', coordinates=np.array(coordinates, dtype=str),
                        momenta=np.array(momenta, dtype=str), rates=rates, residual=residual, metric=current['solution']['state'])
                recovered_coordinates, recovered_momenta, rates, current, history = midpoint_step(evaluator,
                    coordinates, momenta, seed, 0., preconditioner, record)
                final = history[-1]
                evidence.check(name+'_endpoint_state_unchanged', np.array_equal(recovered_coordinates, coordinates)
                    and np.array_equal(recovered_momenta, momenta))
                evidence.check(name+'_full_inverse_and_radial_gates', final['relative_residual'] < 5e-12
                    and final['maximum_correction'] < 2e-12 and final['radial_residual'] < 2e-12
                    and final['minimum_F'] > 0 and final['maximum_speed_ratio'] < 1)
                changed = float(np.max(abs(rates-seed)))
                if label.endswith('initial'):
                    evidence.check(name+'_known_initial_rates_recovered', changed < 2e-12, changed)
                else:
                    evidence.check(name+'_midpoint_velocity_not_misused_as_endpoint', history[0]['relative_residual'] > 1e-8
                        and changed > 1e-11, dict(initial_residual=history[0]['relative_residual'], velocity_change=changed))
                energy, numerical, raw = energy_channels(current, momenta, rates, preconditioner)
                path = evidence.output/(name+'-energy-inputs.npz')
                np.savez_compressed(path, **raw, coordinates=np.array(coordinates, dtype=str), seed_rates=seed,
                    metric=current['solution']['state'], edges=current['solver'].edges, nodes=current['solver'].nodes)
                evidence.own(path, 'outputs')
                with localcontext() as context:
                    context.prec = 64
                    boundary = Decimal(energy['boundary_integral'])
                    full = Decimal(energy['full_shifted_hamiltonian'])
                    relative_identity = float(abs(full-boundary)/abs(boundary))
                    gravity = Decimal(energy['gravity_bulk'])
                evidence.check(name+'_positive_boundary_energy_and_full_Legendre_identity', boundary > 0
                    and relative_identity < 2e-9, relative_identity)
                evidence.check(name+'_independent_radial_density_identity', numerical['pointwise_radial_Legendre_relative_defect'] < 2e-12,
                    numerical['pointwise_radial_Legendre_relative_defect'])
                evidence.check(name+'_inverse_energy_error_respects_Cauchy_bound', abs(float(energy['inverse_energy_error'])) <=
                    numerical['inverse_energy_Cauchy_bound']*(1+1e-10)+1e-30)
                evidence.check(name+'_omitted_gravity_and_boundary_terms_detected', abs(float(boundary/full)) > .1
                    and abs(float(gravity/full)) > .1)
                row = dict(branch=branch, extension=extension, label=label, full_components=16425,
                    reference_order=reference_order, material_order=material_order, iterations=len(history),
                    endpoint_velocity_change_from_seed=changed, relative_Legendre_boundary_difference=relative_identity,
                    **{key:final[key] for key in ['relative_residual', 'maximum_correction', 'radial_residual', 'minimum_F', 'maximum_speed_ratio']},
                    **numerical, energy=energy, source_state=str((evidence.output.parent/folder/source_name).relative_to(evidence.root)),
                    valid_for_claim=False)
                evidence.report['cases'].append(row)
                rows[label] = row
                evidence.save()
            for label in ['one_step', 'two_steps', 'four_steps', 'fine_step']:
                baseline = rows['fine_initial'] if label == 'fine_step' else rows['initial']
                current = rows[label]
                with localcontext() as context:
                    context.prec = 64
                    initial_energy = Decimal(baseline['energy']['full_shifted_hamiltonian'])
                    drift = Decimal(current['energy']['full_shifted_hamiltonian'])-initial_energy
                    boundary_drift = Decimal(current['energy']['boundary_integral'])-Decimal(baseline['energy']['boundary_integral'])
                resolution = current['diagnostic_resolution_scale']+baseline['diagnostic_resolution_scale']
                row = dict(branch=branch, extension=extension, label=label, energy_drift=str(drift), boundary_energy_drift=str(boundary_drift),
                    relative_energy_drift=float(abs(drift)/abs(initial_energy)), diagnostic_resolution_scale=resolution,
                    drift_over_resolution=float(abs(drift))/resolution, drift_resolved=abs(float(drift)) > 4*resolution,
                    smoke_passed=abs(drift) < Decimal('1e-9')*abs(initial_energy), resolution_scale_not_certified=True,
                    conservation_proven=False, valid_for_claim=False)
                evidence.report['drifts'].append(row)
            branch_drifts = {row['label']:row for row in evidence.report['drifts'] if row['branch'] == branch and row['extension'] == extension}
            first, second, third = [Decimal(branch_drifts[label]['energy_drift']) for label in ['one_step', 'two_steps', 'four_steps']]
            floor = max(branch_drifts[label]['diagnostic_resolution_scale'] for label in ['one_step', 'two_steps', 'four_steps'])
            first_difference, second_difference = abs(first-second), abs(second-third)
            resolved = float(first_difference) > 4*floor and float(second_difference) > 4*floor
            ratio = float(second_difference/max(first_difference, Decimal('1e-90')))
            evidence.report['refinement'].append(dict(branch=branch, extension=extension, first_difference=str(first_difference),
                second_difference=str(second_difference), diagnostic_resolution_scale=floor, ratio=ratio,
                resolved_energy_time_order=resolved and ratio < .4, differences_resolved=resolved,
                floor_limited=not resolved, valid_for_claim=False))
            with localcontext() as context:
                context.prec = 64
                drift_difference = Decimal(branch_drifts['fine_step']['energy_drift'])-first
                initial_offset = Decimal(rows['fine_initial']['energy']['full_shifted_hamiltonian'])-Decimal(rows['initial']['energy']['full_shifted_hamiltonian'])
            evidence.report['quadrature'].append(dict(branch=branch, extension=extension,
                energy_drift_difference=str(drift_difference), initial_energy_offset=str(initial_offset),
                matched_physical_initial_state=True, spatial_convergence_claim=False, valid_for_claim=False))
            evidence.save()
        evidence.own(evidence.output/'latest-endpoint-recovery.npz', 'outputs')
        evidence.check('all_endpoint_and_refinement_cases_retained', len(evidence.report['cases']) == 18
            and len(evidence.report['drifts']) == 12 and len(evidence.report['refinement']) == 3
            and len(evidence.report['quadrature']) == 3)
        evidence.report.update(endpoint_velocities_recovered=True, full_hamiltonian_computed=True,
            energy_drift_smoke_passed=all(row['smoke_passed'] for row in evidence.report['drifts']),
            energy_time_order_resolved=all(row['resolved_energy_time_order'] for row in evidence.report['refinement']),
            seconds=perf_counter()-started)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']),
            energy_smoke_passed=evidence.report['energy_drift_smoke_passed'],
            energy_time_order_resolved=evidence.report['energy_time_order_resolved'], seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        recovery = evidence.output/'latest-endpoint-recovery.npz'
        if recovery.exists():
            evidence.own(recovery, 'outputs')
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

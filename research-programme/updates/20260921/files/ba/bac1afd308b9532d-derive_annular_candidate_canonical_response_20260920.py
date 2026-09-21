from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_canonical_response_20260920 import (
    common_material, probe_directions, density_response, restored_solver, velocity_forcing,
    solve_tangent, solve_changed_velocity, radial_weights, total_action, momentum_response,
    center_momentum, transpose_embedding)
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from run_annular_P2_continuum_bridge_20260918 import checked_load
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from time import perf_counter
import contextlib
import json
import numpy as np
import sympy as sp


def main():
    evidence = EvidenceRun('annular-candidate-live-momenta-attempt01', __file__)
    started = perf_counter()
    deadline = started+10800
    try:
        evidence.report.update(github_action=False, subagents_used=False, candidate_only=True,
            polar_zero_shift_only=True, original_live_action_unchanged=True, no_new_evolution=True,
            self_consistent_candidate_metric_solved=True, fixed_physical_fields_and_velocities=True,
            old_canonical_momenta_preserved=False, physical_force_mismatch_fixed=False,
            full_live_P2_force_convergence_proven=False, spatial_convergence_proven=False,
            general_nonzero_shift_or_temporal_current_derived=False, initial_physical_time=0.,
            continuous_material_action_momenta_computed=False, full_canonical_inverse_qualified=False,
            all_mode_reduced_inertia_positive_proven=False, directional_response_only=True,
            exact_finite_label_Galerkin_evolution_qualified=False, new_coupled_evolution=False,
            derivative_checks=[], inertia_entries=[], refinement=[])
        source = evidence.output.parent/'annular-candidate-radial-metric-final-integrity.json'
        prior = json.loads(source.read_text())
        evidence.own(source)
        evidence.check('preceding_stage_complete_nonclaim', prior['state'] == 'complete'
            and prior['candidate_initial_metric_qualified'] and not prior['full_GR_limit_proven'])
        radius, mass, lapse, speed, source_mass = sp.symbols('radius mass lapse speed source_mass', positive=True)
        metric = 1-2*mass/radius
        clock = sp.sqrt(lapse**2-speed**2/metric)
        momentum = source_mass*speed/(metric*clock)
        expected = [momentum*(2/(radius*metric)+speed**2/(radius*metric**2*clock**2)),
            -momentum*lapse**2/clock**2, source_mass*lapse**2/(metric*clock**3)]
        actual = [sp.diff(momentum, mass), lapse*sp.diff(momentum, lapse), sp.diff(momentum, speed)]
        for label, first, last in zip(['mass', 'log_lapse', 'velocity'], actual, expected):
            evidence.check('symbolic_dust_momentum_'+label, sp.factor(sp.together(first-last)) == 0)
        for branch in ['reference', 'MTS']:
            native = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            saved = checked_load(evidence, 'annular-candidate-initial-metric-attempt02', branch+'-velocity-owned-inputs.npz')
            mesh = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
            owner, coordinates, rates = common_material(native, saved, mesh)
            directions = probe_directions(owner, coordinates)
            snapshot = evidence.output/(branch+'-common-inputs.npz')
            np.savez_compressed(snapshot, coordinates=coordinates, rates=rates, directions=directions, labels=owner.labels)
            evidence.own(snapshot, 'outputs')
            extensions = ['reference'] if branch == 'reference' else ['primary', 'alternative']
            previous = {}
            for degree, label_order in [(18, 20), (22, 28)]:
                density = checked_load(evidence, 'annular-candidate-initial-metric-attempt02',
                    branch+'-radial'+str(degree)+'-density.npz')
                solver = restored_solver(owner, density, degree)
                solver.label_order = label_order
                label = branch+'-'+str(degree)
                evidence.report['progress'] = dict(branch=branch, radial_degree=degree, operation='density_velocity_response',
                    seconds=perf_counter()-started)
                evidence.save()
                print(json.dumps(evidence.report['progress']), flush=True)
                response = density_response(owner, coordinates, rates, directions, solver.nodes.ravel(), label_order, deadline)
                errors = {name:float(np.max(abs(response[name]-solver.fields[name])))
                    for name in ['temporal_square', 'gradient_square', 'source_density', 'velocity']}
                evidence.check(label+'_common_representation_of_same_initial_fields', max(errors.values()) < 2e-9, errors)
                for name in errors:
                    solver.fields[name] = response[name]
                path = evidence.output/(label+'-density-response.npz')
                np.savez_compressed(path, **response, nodes=solver.nodes, edges=solver.edges)
                evidence.own(path, 'outputs')
                for extension in extensions:
                    case = branch+'-'+extension+'-'+str(degree)
                    solution = solver.solve(extension)
                    state = solution['state']
                    previous_metric = checked_load(evidence, 'annular-candidate-initial-metric-attempt02',
                        case+'-metric.npz')
                    metric_change = float(np.max(abs(state-previous_metric['state'])))
                    evidence.check(case+'_coherent_metric_recovered', metric_change < 2e-9, metric_change)
                    tangents, complex_states, changed_solvers, tangent_rows = [], [], [], []
                    for direction in range(len(directions)):
                        forcing = velocity_forcing(solver, state, response['delta_temporal'][direction],
                            response['delta_velocity'][direction])
                        tangent, residual, history = solve_tangent(solver, state, extension, forcing)
                        altered, changed = solve_changed_velocity(solver, state, extension, response, direction, 1e-25j)
                        independent = changed.imag/1e-25
                        relative = float(np.max(abs(independent-tangent))/max(np.max(abs(tangent)), 1e-30))
                        forcing_error = float(np.max(abs(altered.rhs(state.astype(complex), extension).imag/1e-25-forcing)))
                        evidence.check(case+'_radial_velocity_forcing_'+str(direction), forcing_error < 2e-11, forcing_error)
                        evidence.check(case+'_live_metric_direction_'+str(direction),
                            relative < 2e-8 and residual < 2e-11, dict(relative=relative, residual=residual))
                        tangents.append(tangent)
                        complex_states.append(changed)
                        changed_solvers.append(altered)
                        tangent_rows.append(dict(branch=branch, extension=extension, radial_degree=degree,
                            direction=direction, forcing_error=forcing_error, metric_relative_error=relative,
                            linear_residual=residual, tangent_iterations=len(history), valid_for_claim=False))
                    tangents = np.array(tangents)
                    evidence.report['progress'] = dict(case=case, operation='full_momenta_and_directional_inertia',
                        seconds=perf_counter()-started)
                    evidence.save()
                    print(json.dumps(evidence.report['progress']), flush=True)
                    canonical = momentum_response(owner, coordinates, rates, directions, solver, state,
                        tangents, complex_states, deadline)
                    projection = directions.reshape(len(directions), -1)
                    fixed_matrix = projection @ canonical['fixed_derivatives'].reshape(len(directions), -1).T
                    live_matrix = projection @ canonical['live_derivatives'].reshape(len(directions), -1).T
                    symmetry = float(np.max(abs(live_matrix-live_matrix.T))/max(np.max(abs(live_matrix)), 1e-30))
                    evidence.check(case+'_reduced_directional_reciprocity', symmetry < 2e-7, symmetry)
                    relative_momenta = float(np.max(abs(canonical['live_derivatives']-canonical['complex_derivatives']))
                        /max(np.max(abs(canonical['live_derivatives'])), 1e-30))
                    evidence.check(case+'_full_momentum_directional_derivatives', relative_momenta < 2e-8, relative_momenta)
                    fixed_eigenvalues = np.linalg.eigvalsh((fixed_matrix+fixed_matrix.T)/2)
                    live_eigenvalues = np.linalg.eigvalsh((live_matrix+live_matrix.T)/2)
                    evidence.check(case+'_fixed_metric_four_probe_inertia_positive', min(fixed_eigenvalues) > 0)
                    evidence.check(case+'_finite_live_probe_matrix', np.all(np.isfinite(live_matrix)))
                    coefficient = solver.nodes.ravel()**2/(np.exp(state[1].ravel())*
                        np.sqrt(1-2*state[0].ravel()/solver.nodes.ravel()))
                    metric = 1-2*state[0].ravel()/solver.nodes.ravel()
                    lapse = np.exp(state[1].ravel())
                    clock = np.sqrt(lapse**2-response['velocity']**2/metric)
                    for direction, row in enumerate(tangent_rows):
                        contraction = float(projection[direction] @ canonical['momentum'].ravel())
                        direct = float(radial_weights(solver) @ (coefficient*response['delta_temporal'][direction]/2
                            +owner.source_mass*response['source_density']*response['velocity']
                            *response['delta_velocity'][direction]/(metric*clock)))
                        envelope = float(total_action(changed_solvers[direction], complex_states[direction], extension).imag/1e-25)
                        scale = max(abs(contraction), abs(direct), 1e-12)
                        fixed_error, envelope_error = abs(contraction-direct)/scale, abs(contraction-envelope)/scale
                        evidence.check(case+'_weighted_action_momentum_'+str(direction), fixed_error < 2e-8, fixed_error)
                        evidence.check(case+'_stationary_action_envelope_'+str(direction), envelope_error < 2e-6, envelope_error)
                        row.update(momentum_contraction=contraction, fixed_action_derivative=direct,
                            on_shell_action_derivative=envelope, fixed_action_relative_error=fixed_error,
                            envelope_relative_error=envelope_error)
                    evidence.report['derivative_checks'].extend(tangent_rows)
                    for first in range(len(directions)):
                        for last in range(len(directions)):
                            evidence.report['inertia_entries'].append(dict(branch=branch, extension=extension,
                                radial_degree=degree, first=first, last=last,
                                fixed=float(fixed_matrix[first, last]), live=float(live_matrix[first, last]),
                                gravity_response=float(live_matrix[first, last]-fixed_matrix[first, last]),
                                four_probe_not_all_mode_certificate=True, valid_for_claim=False))
                    center = int(np.argmin(abs(owner.labels)))
                    pointwise = center_momentum(owner, coordinates, rates, solver, solution)
                    pullback = np.r_[transpose_embedding(mesh['embeddings'][0], pointwise[:-1], native.count), pointwise[-1]]
                    center_error = float(np.max(abs(pullback-saved['original_momenta'][center])))
                    if branch == 'reference':
                        evidence.check(case+'_independent_pointwise_reference_momentum_recovery', center_error < 2e-9, center_error)
                    row = dict(branch=branch, extension=extension, radial_degree=degree, label_order=label_order,
                        field_dofs=owner.count, material_labels=len(owner.labels), momentum_components=coordinates.size,
                        metric_change_from_preceding=metric_change, integral_residual=solution['maximum_residual'],
                        maximum_momentum=float(np.max(abs(canonical['momentum']))),
                        center_pullback_change_from_old=center_error, directional_reciprocity_error=symmetry,
                        full_momentum_directional_relative_error=relative_momenta,
                        minimum_fixed_probe_eigenvalue=float(min(fixed_eigenvalues)),
                        minimum_live_probe_eigenvalue=float(min(live_eigenvalues)),
                        live_probe_positive=bool(min(live_eigenvalues) > 0),
                        relative_gravity_inertia_correction=float(np.linalg.norm(live_matrix-fixed_matrix)/np.linalg.norm(fixed_matrix)),
                        four_probe_not_all_mode_certificate=True, old_momenta_not_preserved=True, valid_for_claim=False)
                    if degree == 22:
                        prior_case = previous[extension]
                        momentum_change = float(np.linalg.norm(canonical['momentum']-prior_case['momentum'])
                            /max(np.linalg.norm(canonical['momentum']), 1e-30))
                        inertia_change = float(np.linalg.norm(live_matrix-prior_case['live_matrix'])/np.linalg.norm(live_matrix))
                        evidence.check(case+'_joint_quadrature_refinement', max(momentum_change, inertia_change) < 2e-6,
                            dict(momentum=momentum_change, inertia=inertia_change))
                        evidence.report['refinement'].append(dict(branch=branch, extension=extension,
                            momentum_relative_change=momentum_change, live_inertia_relative_change=inertia_change,
                            not_field_spatial_or_evolution_convergence=True, valid_for_claim=False))
                    previous[extension] = dict(momentum=canonical['momentum'], live_matrix=live_matrix)
                    output = evidence.output/(case+'-canonical.npz')
                    np.savez_compressed(output, **canonical, state=state, tangents=tangents,
                        complex_states=np.array(complex_states), fixed_matrix=fixed_matrix, live_matrix=live_matrix,
                        pointwise_center_momentum=pointwise, native_pullback_center_momentum=pullback)
                    evidence.own(output, 'outputs')
                    evidence.report['cases'].append(row)
                    evidence.report['progress'] = dict(case=case, operation='case_complete', seconds=perf_counter()-started)
                    evidence.save()
                    print(json.dumps(dict(**evidence.report['progress'], reciprocity=symmetry,
                        live_eigenvalue=row['minimum_live_probe_eigenvalue'])), flush=True)
        evidence.report.update(continuous_material_action_momenta_computed=True,
            directional_live_velocity_response_qualified=True, stationary_action_envelope_numerically_checked=True,
            candidate_momenta_computed=True, seconds=perf_counter()-started)
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


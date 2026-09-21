from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_radial_constraint_20260920 import CandidateLoads, CandidateRadialSolve, radial_rhs
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_mixed_weak_maps_20260920 import MixedMap
from derive_annular_common_weak_action_20260920 import dec_saved
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from run_annular_P2_continuum_bridge_20260918 import checked_load
from decimal import localcontext
from time import perf_counter
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-candidate-initial-metric-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            original_live_action_unchanged=True, candidate_only=True, polar_zero_shift_only=True,
            self_consistent_candidate_metric_solved=False, fixed_physical_fields_and_velocities=True,
            old_canonical_momenta_preserved=False, no_new_canonical_evolution=True,
            physical_force_mismatch_fixed=False, full_live_P2_force_convergence_proven=False,
            certified_continuous_time_bound=False, spatial_convergence_proven=False,
            candidate_initial_metric_qualified=False)
        control_path = evidence.output.parent/'annular-candidate-radial-derivation-attempt03/status.json'
        control = json.loads(control_path.read_text())
        evidence.own(control_path)
        evidence.check('independent_derivation_controls_complete', control['state'] == 'complete'
            and control['radial_constraint_derived'] and control['radial_jacobian_qualified']
            and all(row['passed'] for row in control['checks']))
        evidence.report['refinement'], evidence.report['factor_checks'], evidence.report['extension_differences'] = [], [], []
        for branch in ['reference', 'MTS']:
            saved = checked_load(evidence, 'annular-live-compensated-rate-attempt01', branch+'-1e-07-compensated-rate.npz')
            mesh = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
            owner = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            coordinates, original_momenta = saved['0_state']
            rates, old_geometry = owner.solve(coordinates, original_momenta)
            extensions = ['reference'] if branch == 'reference' else ['primary', 'alternative']
            packets = {extension:owned_json(evidence, 'annular-complete-frozen-candidate-attempt01',
                branch+'-'+extension+'-action.json') for extension in extensions}
            loads = CandidateLoads(owner, coordinates, rates, mesh, packets)
            loads.deadline = started+9000
            evidence.check(branch+'_source_and_spatial_maps_ordered', loads.material.minimum_jacobian > 0
                and loads.material.minimum_spatial_jacobian > 0)
            center = int(np.argmin(abs(owner.labels)))
            with localcontext() as context:
                context.prec = 64
                for extension in extensions:
                    packet = packets[extension]
                    if extension != 'reference':
                        expected = np.asarray(MixedMap(packet['gram_factor']['rows'], packet['count']).apply(
                            dec_saved(packet['phase'])[0, :, None])[:, 0], dtype=float)
                        actual = loads.factor_vertices[extension][center]
                        error = float(np.max(abs(actual-expected)))
                        evidence.check(extension+'_saved_center_Gram_factor_preserved',
                            error <= 1e-24+1e-10*float(np.max(abs(expected))), error)
                        reconstructed = np.polynomial.chebyshev.chebval(2*owner.labels, loads.factor_coefficients[extension]).T
                        relative = float(np.max(abs(reconstructed-loads.factor_vertices[extension]))
                            /max(np.max(abs(loads.factor_vertices[extension])), 1e-30))
                        evidence.check(extension+'_label_factor_interpolation', relative < 1e-11, relative)
                        evidence.report['factor_checks'].append(dict(extension=extension, center_factor_error=error,
                            label_factor_relative_error=relative, high_precision_atom_preparation_digits=64, valid_for_claim=False))
            snapshot = evidence.output/(branch+'-velocity-owned-inputs.npz')
            np.savez_compressed(snapshot, coordinates=coordinates, original_momenta=original_momenta,
                fixed_rates=rates, labels=owner.labels, candidate_reference_knots=loads.knots)
            evidence.own(snapshot, 'outputs')
            probes = np.linspace(owner.model.radii[0]-owner.width/2, owner.model.radii[-1]+owner.width/2, 513)
            probes = np.unique(np.r_[probes, coordinates[:, -1]])
            old_mass, old_lapse, unused, unused2 = old_geometry.values(probes)
            previous_values = {}
            for degree, label_order in [(18, 20), (22, 28)]:
                evidence.report['progress'] = dict(branch=branch, radial_degree=degree, label_order=label_order,
                    operation='prepare_candidate_density', seconds=perf_counter()-started)
                evidence.save()
                print(json.dumps(evidence.report['progress']), flush=True)
                solver = CandidateRadialSolve(loads, degree, label_order, extensions)
                evidence.check(branch+'_'+str(degree)+'_all_Gram_density_nonnegative',
                    all(np.min(values) >= 0 for values in solver.fields['gram'].values()))
                evidence.check(branch+'_'+str(degree)+'_positive_radial_segments', np.min(solver.lengths) > 0)
                fields_path = evidence.output/(branch+'-radial'+str(degree)+'-density.npz')
                np.savez_compressed(fields_path, edges=solver.edges, nodes=solver.nodes,
                    **{name:value for name, value in solver.fields.items() if name != 'gram'},
                    **{'gram_'+name:value for name, value in solver.fields['gram'].items()})
                evidence.own(fields_path, 'outputs')
                off_points = np.polynomial.legendre.leggauss(2)[0]
                off_radius = (solver.centers[:, None]+solver.lengths[:, None]*off_points/2).ravel()
                off_fields = loads.sample(off_radius, 32, extensions)
                current_values = {}
                for extension in extensions:
                    label = branch+'-'+extension+'-'+str(degree)
                    solution = solver.solve(extension)
                    state = solution['state']
                    residual = solution['maximum_residual']
                    evidence.check(label+'_integral_constraint_residual', residual < 2e-12, residual)
                    direction = np.array([.02*(1+.1*np.sin(solver.nodes)), .015*np.cos(solver.nodes)])
                    derived = solver.jacobian_product(state, direction, extension)
                    independent = solver.residual(state.astype(complex)+1e-24j*direction, extension).imag/1e-24
                    error = float(np.max(abs(derived-independent)))
                    evidence.check(label+'_full_integral_Jacobian', error < 3e-11, error)
                    boundary_term = direction[0, -1, -1]/(solver.edges[-1]*(1-2*state[0, -1, -1]/solver.edges[-1]))
                    evidence.check(label+'_omitted_outer_clock_Jacobian_detected', abs(boundary_term) > 1e-6)
                    values, derivatives = solver.values(solution, off_radius)
                    expected = radial_rhs(off_radius, *values, off_fields['temporal_square'], off_fields['gradient_square'],
                        off_fields['gram'][extension], off_fields['source_density'], off_fields['velocity'],
                        owner.coupling, owner.source_mass)
                    off_error = np.max(abs(derivatives-expected), axis=1)
                    evidence.check(label+'_off_grid_radial_constraints', max(off_error) < 1e-8, list(map(float, off_error)))
                    values_at_probes, unused = solver.values(solution, probes)
                    current_values[extension] = values_at_probes
                    changes = np.max(abs(values_at_probes-np.array([old_mass, old_lapse])), axis=1)
                    if branch == 'reference':
                        evidence.check(label+'_reference_original_metric_recovered', max(changes) < 2e-9, list(map(float, changes)))
                    boundary, unused = solver.values(solution, solver.edges[[0, -1]])
                    boundary_error = max(abs(boundary[0, 0]-owner.central_mass),
                        abs(boundary[1, -1]-.5*np.log(1-2*boundary[0, -1]/solver.edges[-1])))
                    evidence.check(label+'_both_sourced_boundaries', boundary_error < 2e-12, float(boundary_error))
                    row = dict(branch=branch, extension=extension, radial_degree=degree, label_order=label_order,
                        field_dofs=mesh['overlay']['count'], radial_segments=len(solver.lengths), radial_nodes=solver.nodes.size,
                        iterations=len(solution['history']), integral_residual=residual, global_Jacobian_error=error,
                        off_grid_mass_residual=float(off_error[0]), off_grid_log_lapse_residual=float(off_error[1]),
                        boundary_error=float(boundary_error), maximum_mass_change_from_old=float(changes[0]),
                        maximum_log_lapse_change_from_old=float(changes[1]), outer_mass=float(boundary[0, -1]),
                        minimum_F=float(np.min(1-2*state[0]/solver.nodes)),
                        maximum_source_speed_ratio=float(np.max(abs(solver.fields['velocity'])/
                            (np.exp(state[1].ravel())*np.sqrt(1-2*state[0].ravel()/solver.nodes.ravel())))),
                        velocity_owned_not_old_canonical_state=True, valid_for_claim=False)
                    evidence.report['cases'].append(row)
                    if degree == 22:
                        difference = np.max(abs(values_at_probes-previous_values[extension]), axis=1)
                        evidence.check(label+'_joint_radial_label_refinement', max(difference) < 2e-9, list(map(float, difference)))
                        evidence.report['refinement'].append(dict(branch=branch, extension=extension,
                            radial_degrees='18 -> 22', label_orders='20 -> 28',
                            maximum_mass_change=float(difference[0]), maximum_log_lapse_change=float(difference[1]),
                            numerical_gate=2e-9, not_a_spatial_force_convergence_gate=True, valid_for_claim=False))
                    output = evidence.output/(label+'-metric.npz')
                    np.savez_compressed(output, edges=solver.edges, nodes=solver.nodes, state=state,
                        rhs_coefficients=solution['rhs_coefficients'], primitives=solution['primitives'], left=solution['left'],
                        history=solution['history'], probes=probes, probe_values=values_at_probes,
                        off_radius=off_radius, off_values=values, off_derivatives=derivatives, off_expected=expected)
                    evidence.own(output, 'outputs')
                    evidence.report['progress'] = dict(case=label, operation='metric_solved', seconds=perf_counter()-started)
                    evidence.save()
                    print(json.dumps(dict(**evidence.report['progress'], integral_residual=residual, off_grid=max(off_error))), flush=True)
                if branch == 'MTS':
                    differences = np.max(abs(current_values['primary']-current_values['alternative']), axis=1)
                    evidence.report['extension_differences'].append(dict(radial_degree=degree, label_order=label_order,
                        maximum_mass_difference=float(differences[0]), maximum_log_lapse_difference=float(differences[1]),
                        not_a_uniqueness_certificate=True, valid_for_claim=False))
                previous_values = current_values
        evidence.report.update(self_consistent_candidate_metric_solved=True, candidate_initial_metric_qualified=True,
            general_nonzero_shift_or_temporal_current_derived=False, new_candidate_canonical_momenta_computed=False,
            seconds=perf_counter()-started)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=evidence.report['seconds'],
            cases=evidence.report['cases'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

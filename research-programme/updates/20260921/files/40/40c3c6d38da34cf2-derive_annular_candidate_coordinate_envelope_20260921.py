from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_radial_constraint_20260920 import CandidateLoads, CandidateRadialSolve
from annular_candidate_canonical_response_20260920 import radial_weights
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_common_weighted_moments_20260920 import apply_rational_rows
from annular_decimal_transport_v2_20260919 import decimal_array
from run_annular_P2_continuum_bridge_20260918 import checked_load
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from decimal import Decimal, localcontext
from time import perf_counter
import contextlib
import json
import numpy as np


def action_channels(solver, solution, extension):
    radius = solver.nodes.ravel()
    mass, log_lapse = solution['state'].reshape(2, -1)
    lapse, metric = np.exp(log_lapse), 1-2*mass/radius
    root = np.sqrt(metric)
    clock = np.sqrt(lapse**2-solver.fields['velocity']**2/metric)
    wave = radius**2*solver.fields['temporal_square']/(2*lapse*root)
    wave -= lapse*root*radius**2*(solver.fields['gradient_square']/2+solver.fields['gram'][extension])
    dust = -solver.owner.source_mass*solver.fields['source_density']*clock
    gravity = lapse*solver.rhs(solution['state'], extension)[0]/(solver.owner.coupling*root)
    weights = radial_weights(solver).astype(np.longdouble)
    channels = {name:np.sum(weights*values.astype(np.longdouble))
        for name, values in [('wave', wave), ('dust', dust), ('gravity_bulk', gravity)]}
    channels['gravity_boundary_shifted'] = -(np.longdouble(mass[-1])-solver.owner.central_mass)/solver.owner.coupling
    channels['total_shifted'] = sum(channels.values())
    return channels


def native_directions(owner, coordinates):
    directions = np.zeros((3, *coordinates.shape))
    directions[0, :, :-1] = coordinates[:, :-1]
    directions[1, :, -1] = 1+.1*owner.labels
    fraction = (owner.model.radii-owner.model.radii[0])/(owner.model.radii[-1]-owner.model.radii[0])
    offset = (owner.model.radii-owner.model.anchor)/(owner.model.radii[-1]-owner.model.radii[0])
    directions[2, :, :-1] = .01*(1+owner.labels[:, None])*np.sin(3*np.pi*fraction)*offset
    directions[2, :, -1] = .2*(owner.labels**2-1/12)
    return directions


def main():
    evidence = EvidenceRun('annular-candidate-coordinate-envelope-attempt01', __file__)
    started = perf_counter()
    deadline = started+7500
    try:
        source = evidence.output.parent/'annular-candidate-coordinate-covectors-attempt01/status.json'
        previous = json.loads(source.read_text())
        evidence.own(source)
        evidence.check('full_covectors_and_independent_derivatives_qualified', previous['state'] == 'complete'
            and previous['full_coordinate_covectors_computed'] and previous['independent_coordinate_derivatives_qualified']
            and previous['quadrature_qualified'] and all(row['passed'] for row in previous['checks']))
        evidence.report.update(github_action=False, subagents_used=False, candidate_only=True,
            polar_zero_shift_only=True, no_new_evolution=True, new_coupled_evolution=False,
            original_live_action_unchanged=True, physical_force_mismatch_fixed=False,
            full_live_P2_force_convergence_proven=False, spatial_convergence_proven=False,
            general_nonzero_shift_or_temporal_current_derived=False, modes_deleted=False,
            on_shell_coordinate_envelope_numerically_tested=True, coordinate_envelope_qualified=False,
            exact_finite_label_Galerkin_evolution_qualified=False, initial_physical_time=0.,
            cases=[], finite_differences=[], comparisons=[], radial_degree=22, material_order=28,
            independent_material_covector_orders=[16, 48], direction_names=['native_amplitude', 'source_motion', 'mixed'],
            fixed_rates_under_coordinate_variation=True, source_support_and_radial_edges_rebuilt=True,
            derivative_absolute_tolerance=2e-10, derivative_relative_tolerance=2e-5)
        for branch in ['reference', 'MTS']:
            owner = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            saved = checked_load(evidence, 'annular-candidate-initial-metric-attempt02', branch+'-velocity-owned-inputs.npz')
            mesh = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-exact-common-overlay.json')
            extensions = ['reference'] if branch == 'reference' else ['primary', 'alternative']
            packets = {extension:owned_json(evidence, 'annular-complete-frozen-candidate-attempt01',
                branch+'-'+extension+'-action.json') for extension in extensions}
            directions = native_directions(owner, saved['coordinates'])
            with localcontext() as context:
                context.prec = 64
                embedded = [np.vstack([apply_rational_rows(mesh['embeddings'][0], decimal_array(direction[:, :-1].T)),
                    decimal_array(direction[:, -1])[None, :]]) for direction in directions]
            contractions = {}
            for extension in extensions:
                forces = checked_load(evidence, 'annular-candidate-coordinate-covectors-attempt01',
                    branch+'-'+extension+'-16-48-covectors.npz')
                with localcontext() as context:
                    context.prec = 64
                    total = decimal_array(forces['bulk'])+decimal_array(forces['dust'])
                    total += np.array([[Decimal(value) for value in row] for row in forces['gram_decimal']])
                    contractions[extension] = [float(np.sum(total*direction)) for direction in embedded]
            path = evidence.output/(branch+'-native-coordinate-variations.npz')
            np.savez_compressed(path, directions=directions, embedded=np.array(embedded, dtype=str),
                coordinates=saved['coordinates'], fixed_rates=saved['fixed_rates'])
            evidence.own(path, 'outputs')
            for direction in range(len(directions)):
                series = {extension:[] for extension in extensions}
                for step in [1e-3, 5e-4, 2.5e-4]:
                    signs = {}
                    for sign in [-1, 1]:
                        if perf_counter() > deadline:
                            raise RuntimeError('Safe wall boundary with all completed variations retained.')
                        label = branch+'-d'+str(direction)+'-h'+format(step, '.1e')+'-sign'+str(sign)
                        evidence.report['progress'] = dict(case=label, operation='rebuild_support_and_resolve_gravity',
                            seconds=perf_counter()-started)
                        evidence.save()
                        print(json.dumps(evidence.report['progress']), flush=True)
                        coordinates = saved['coordinates']+sign*step*directions[direction]
                        loads = CandidateLoads(owner, coordinates, saved['fixed_rates'], mesh, packets)
                        loads.deadline = deadline
                        evidence.check(label+'_ordered_source_and_spatial_maps', loads.material.minimum_jacobian > 0
                            and loads.material.minimum_spatial_jacobian > 0)
                        solver = CandidateRadialSolve(loads, 22, 28, extensions)
                        density_path = evidence.output/(label+'-density.npz')
                        np.savez_compressed(density_path, coordinates=coordinates, nodes=solver.nodes, edges=solver.edges,
                            **{name:values for name, values in solver.fields.items() if name != 'gram'},
                            **{'gram_'+name:values for name, values in solver.fields['gram'].items()})
                        evidence.own(density_path, 'outputs')
                        signs[sign] = {}
                        for extension in extensions:
                            solution = solver.solve(extension)
                            evidence.check(label+'-'+extension+'_radial_constraint_resolved', solution['maximum_residual'] < 2e-12,
                                solution['maximum_residual'])
                            channels = action_channels(solver, solution, extension)
                            signs[sign][extension] = channels
                            solution_path = evidence.output/(label+'-'+extension+'-metric.npz')
                            np.savez_compressed(solution_path, **solution)
                            evidence.own(solution_path, 'outputs')
                            evidence.report['cases'].append(dict(branch=branch, extension=extension, direction=direction,
                                step=step, sign=sign, residual=solution['maximum_residual'], iterations=len(solution['history']),
                                radial_segments=len(solver.lengths), action_channels={name:float(value) for name, value in channels.items()},
                                valid_for_claim=False))
                        evidence.save()
                    for extension in extensions:
                        differences = {name:float((signs[1][extension][name]-signs[-1][extension][name])/(2*step))
                            for name in signs[1][extension]}
                        expected = contractions[extension][direction]
                        observed = differences['total_shifted']
                        series[extension].append(observed)
                        evidence.report['finite_differences'].append(dict(branch=branch, extension=extension,
                            direction=direction, step=step, canonical_covector=expected, full_action_derivative=observed,
                            absolute_difference=abs(observed-expected), relative_difference=abs(observed-expected)/max(abs(expected), 1e-30),
                            channel_derivatives=differences, valid_for_claim=False))
                for extension in extensions:
                    coarse, middle, fine = series[extension]
                    first, last = (4*middle-coarse)/3, (4*fine-middle)/3
                    expected = contractions[extension][direction]
                    tolerance = 2e-10+2e-5*abs(expected)
                    row = dict(branch=branch, extension=extension, direction=direction, canonical_covector=expected,
                        extrapolated_full_action_derivative=last, absolute_difference=abs(last-expected),
                        relative_difference=abs(last-expected)/max(abs(expected), 1e-30), extrapolation_difference=abs(last-first),
                        tolerance=tolerance, passed=abs(last-expected) < tolerance and abs(last-first) < tolerance,
                        directional_test_not_global_stationarity_theorem=True, valid_for_claim=False)
                    evidence.report['comparisons'].append(row)
                    evidence.save()
                    print(json.dumps(dict(operation='envelope_comparison', **row)), flush=True)
        evidence.report.update(coordinate_envelope_qualified=all(row['passed'] for row in evidence.report['comparisons']),
            seconds=perf_counter()-started)
        evidence.check('all_expected_coordinate_envelope_comparisons_recorded', len(evidence.report['comparisons']) == 9
            and len(evidence.report['cases']) == 54 and len(evidence.report['finite_differences']) == 27)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']),
            envelope_qualified=evidence.report['coordinate_envelope_qualified'], seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

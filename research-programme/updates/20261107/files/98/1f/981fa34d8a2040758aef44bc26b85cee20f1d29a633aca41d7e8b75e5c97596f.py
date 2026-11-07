from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_nested_physical_refinement_v3_20260922 import bisected_mesh, adapt_owner, prolong_state, all_prolongation
from annular_quadratic_core_20261002 import live_core, physical_edges
from annular_live_transmission_system_20261002 import coupled_system
from annular_physical_native_kernel_20260928 import NativeKernel, decimals, maximum
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from analyze_annular_source_flat_state_20261002 import read_archive
from decimal import Decimal, localcontext
from fractions import Fraction
from scipy.sparse import load_npz
from time import perf_counter
import argparse
import ctypes
import gc
import json
import numpy as np


def fixed_support_packet(parent, mesh, restriction):
    def moved(rows):
        return [{str(restriction[int(column)]): value for column, value in row.items()} for row in rows]
    return dict(count=mesh['count'], mesh=mesh, extension='primary', gram_support=parent['gram_support'],
        gram_factor=dict(rows=moved(parent['gram_factor']['rows']), columns=mesh['count']),
        gram_sampling=moved(parent['gram_sampling']), fixed_interaction_support=True,
        route='exact_prolongation_of_saved_P2', valid_for_claim=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--branch', choices=['primary', 'reference'], required=True)
    parser.add_argument('--cpu', type=int, default=2)
    args = parser.parse_args()
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << args.cpu):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-live-native-transmission-fourth-' + args.branch + '-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 7200
    try:
        evidence.own(evidence.root / 'DERIVATION-20261002-fixed-profile-native-refinement.md')
        base = 'source-intake/navier-stokes/20260914/'
        parent = verify_report(evidence, base + 'annular-live-native-transmission-third-attempt02/status.json')
        evidence.check('complete_parent', parent['state'] == 'complete')
        seal_path = evidence.output.parent / 'annular-quadratic-transmission-integrity-20261002.json'
        evidence.own(seal_path)
        digests = json.loads(seal_path.read_text())['hashes']
        state_path = next(row['path'] for row in parent['states'] if row['name'] == 'iteration0')
        state = read_archive(evidence.root / state_path)
        packet = json.loads((evidence.root / parent['packet_path']).read_text())
        mesh, prolongation, restriction = bisected_mesh(packet['mesh'])
        fine_packet = fixed_support_packet(packet, mesh, restriction)
        fine_packet.update(prolongation=prolongation, restriction=restriction, parent_state=state_path, parent_packet=parent['packet_path'])
        evidence.check('fixed_native_support', fine_packet['gram_support'] == packet['gram_support'] and len(packet['gram_support']) == 1094)
        evidence.check('doubled_field_space', mesh['count'] == 2 * packet['count'] == 8752)
        evidence.check('exact_retained_nodes', all(mesh['nodes'][chosen] == packet['mesh']['nodes'][index] for index, chosen in enumerate(restriction)))
        evidence.check('retained_operator_rows', len(fine_packet['gram_factor']['rows']) == len(packet['gram_factor']['rows']))
        reverse = {str(value): str(index) for index, value in enumerate(restriction)}
        for name, old_rows, new_rows in [('factor', packet['gram_factor']['rows'], fine_packet['gram_factor']['rows']),
                                        ('sampling', packet['gram_sampling'], fine_packet['gram_sampling'])]:
            evidence.check(name + ':exact_column_embedding', [{reverse[key]: value for key, value in row.items()} for row in new_rows] == old_rows)
        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe refinement boundary')
        with localcontext() as context:
            context.prec = 64
            coordinates, rates = prolong_state(state, prolongation)
            evidence.check('same_old_field_and_source', np.array_equal(coordinates[:, restriction], decimals(state['coordinates'][:, :-1]))
                and np.array_equal(coordinates[:, -1], decimals(state['coordinates'][:, -1])))
            evidence.check('zero_rates_retained', not np.any(rates) and not np.any(state['rates']))
            coarse_engine, fine_engine = NativeKernel(packet['mesh'], packet['gram_support'], True), NativeKernel(mesh, packet['gram_support'], True)
            unused, old_action, sources = restore_case(evidence, digests, 'MTS-primary', 'third', deadline)
            owner = adapt_owner(old_action.owner, mesh)
            maximum_value_error, maximum_jet_error, maximum_curvature_error = Decimal(0), Decimal(0), Decimal(0)
            coarse_field = decimals(state['coordinates'])
            for index, label in enumerate(owner.layer_rule.points / 2):
                coarse_edges = physical_edges(coarse_engine, coordinates[index, -1], label, owner.width)
                fine_edges = physical_edges(fine_engine, coordinates[index, -1], label, owner.width)
                old_atoms = coarse_engine.atoms(coarse_edges, coarse_field[index, :-1])
                new_atoms = fine_engine.atoms(fine_edges, coordinates[index, :-1])
                maximum_jet_error = max(maximum_jet_error, maximum(new_atoms['slope_left'][::2] - old_atoms['slope_left']),
                    maximum(new_atoms['slope_right'][1::2] - old_atoms['slope_right']))
                maximum_curvature_error = max(maximum_curvature_error, maximum(new_atoms['second'] - np.repeat(old_atoms['second'], 2)))
                for fine_index, row in enumerate(prolongation):
                    expected = sum((Decimal(Fraction(value).numerator) / Decimal(Fraction(value).denominator)) * coarse_field[index, int(column)]
                        for column, value in row.items())
                    maximum_value_error = max(maximum_value_error, abs(coordinates[index, fine_index] - expected))
            evidence.check('P2_all_nodes', maximum_value_error < Decimal('1e-45'), str(maximum_value_error))
            evidence.check('P2_all_one_sided_jets', maximum_jet_error < Decimal('1e-40'), str(maximum_jet_error))
            evidence.check('P2_all_cell_curvatures', maximum_curvature_error < Decimal('1e-35'), str(maximum_curvature_error))
        packet_path = evidence.output / 'fourth-action.json'
        packet_path.write_text(json.dumps(fine_packet) + '\n')
        evidence.own(packet_path, 'outputs')
        evidence.report.update(branch=args.branch, packet_path=str(packet_path.relative_to(evidence.root)), results=[], comparisons=[],
            fixed_profile=True, curvature_refitted=False, carrier_retuned=False, physical_interaction_refined=False,
            physical_trajectory_computed=False, second_order_preservation_done=False, github_action=False, subagents_used=False)
        progress('fresh native radial solve')
        loads, action = live_core(owner, coordinates, rates, mesh, fine_packet, args.branch, deadline)
        radial_error = float(np.max(abs(action.solver.residual(action.solution['state'], args.branch))))
        evidence.check('fresh_radial_equations', radial_error < 8e-14, radial_error)
        saved_state = evidence.output / 'fourth-state.npz'
        np.savez_compressed(saved_state, coordinates=np.asarray(coordinates, str), rates=rates, edges=action.solver.edges, **action.solution)
        evidence.own(saved_state, 'outputs')
        evidence.report['state_path'] = str(saved_state.relative_to(evidence.root))
        transfer = all_prolongation(prolongation, packet['count'], len(owner.layer_rule.points))
        for spatial, material in [(12, 48), (16, 64)]:
            name = args.branch + '-' + str(spatial) + '-' + str(material)
            arrays, matrix, item = coupled_system(evidence, loads, action, fine_packet, args.branch, name, spatial, material, deadline, progress)
            old_name = ('iteration0' if material == 48 else 'primary-16-64') if args.branch == 'primary' else name
            old_item = next(row for row in parent['results'] if row['name'] == old_name)
            old = read_archive(evidence.root / old_item['path'])
            old_matrix = load_npz(evidence.root / old_item['matrix_path'])
            prolonged = transfer @ old['acceleration'].ravel()
            difference = arrays['acceleration'].ravel() - prolonged
            mass_difference = transfer.T @ matrix @ transfer - old_matrix
            force_difference = transfer.T @ arrays['force'].ravel() - old['force'].ravel()
            record = dict(branch=args.branch, material=material, spatial=spatial,
                mass_pullback_max=float(np.max(abs(mass_difference.data))) if mass_difference.nnz else 0.,
                force_pullback_max=float(np.max(abs(force_difference))),
                common_node_acceleration_difference=float(np.max(abs(arrays['acceleration'][:, restriction] - old['acceleration'][:, :-1]))),
                source_acceleration_difference=float(np.max(abs(arrays['acceleration'][:, -1] - old['acceleration'][:, -1]))),
                acceleration_kinetic_norm=float(np.sqrt(arrays['acceleration'].ravel() @ (matrix @ arrays['acceleration'].ravel()))),
                prolongation_defect_kinetic_norm=float(np.sqrt(max(0., difference @ (matrix @ difference)))),
                old_maximum_acceleration=old_item['maximum_acceleration'], new_maximum_acceleration=item['maximum_acceleration'],
                native_energy_change=item['native_energy'] - old_item['native_energy'], valid_for_claim=False)
            evidence.check(name + ':finite_refinement_comparison', all(np.isfinite(value) for value in record.values() if isinstance(value, float)))
            evidence.check(name + ':Galerkin_mass_pullback', record['mass_pullback_max'] < 2e-11, record['mass_pullback_max'])
            evidence.check(name + ':Galerkin_force_pullback', record['force_pullback_max'] < 2e-11, record['force_pullback_max'])
            item['initial_data_gates_pass'] = bool(item['maximum_trace_residual'] < 1e-9 and (args.branch == 'reference' or
                item['relative_point_residual'] < 1e-8 and item['relative_jump_residual'] < 1e-7))
            evidence.report['results'].append(item)
            evidence.report['comparisons'].append(record)
            evidence.save()
            del arrays, matrix, old_matrix, mass_difference
            gc.collect()
        evidence.report.update(seconds=perf_counter() - started, radial_residual=radial_error, spatial_refinement_done_for_this_state=True,
            asymptotic_convergence_proven=False, continuous_material_bound_proven=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

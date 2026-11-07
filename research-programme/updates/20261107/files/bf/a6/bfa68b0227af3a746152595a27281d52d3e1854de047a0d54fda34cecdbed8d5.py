from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_nested_physical_refinement_v3_20260922 import adapt_owner
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_candidate_hamiltonian_20260921 import decimals
from annular_physical_native_kernel_20260928 import NativeKernel, maximum
from derive_annular_native_shape_stress_20260928 import physical_data
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from analyze_annular_source_flat_state_20261002 import read_archive
from annular_high_order_native_v2_20261003 import PolynomialBasis, HighKernel, HighLoads, HighAction, zero_system
from decimal import Decimal, localcontext
from fractions import Fraction
from scipy.sparse import load_npz
from time import perf_counter
import ctypes
import json
import numpy as np


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << 2):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-high-order-adapter-validation-attempt02', __file__)
    started, deadline = perf_counter(), perf_counter() + 3600
    try:
        evidence.own(evidence.root / 'DERIVATION-20261003-live-higher-order-curvature-repair.md')
        with localcontext() as context:
            context.prec = 64
            for degree in [2, 6]:
                basis = PolynomialBasis(degree)
                vandermonde = np.array([[point**power for power in range(degree + 1)] for point in basis.nodes], dtype=object)
                evidence.check('degree' + str(degree) + ':exact_nodal_basis', np.array_equal(vandermonde @ basis.rational, np.eye(degree + 1, dtype=int)))
                evidence.check('degree' + str(degree) + ':partition_unity', list(np.sum(basis.rational, axis=1)) == [Fraction(1)] + [Fraction(0)] * degree)
                for power in range(degree + 1):
                    coefficients = basis.rational @ np.array([point**power for point in basis.nodes], dtype=object)
                    evidence.check('degree' + str(degree) + ':monomial' + str(power), all(value == (1 if index == power else 0) for index, value in enumerate(coefficients)))
        parent = verify_report(evidence, 'source-intake/navier-stokes/20260914/annular-live-native-transmission-third-attempt02/status.json')
        seal = evidence.output.parent / 'annular-live-refinement-time-jet-integrity-20261002.json'
        evidence.own(seal)
        digests = json.loads(seal.read_text())['hashes']
        packet = json.loads((evidence.root / parent['packet_path']).read_text())
        state = read_archive(evidence.root / next(row['path'] for row in parent['states'] if row['name'] == 'iteration0'))
        mesh = dict(packet['mesh'], degree=2, gram_support=packet['gram_support'])
        with localcontext() as context:
            context.prec = 64
            unused, old_action, sources = restore_case(evidence, digests, 'MTS-primary', 'third', deadline)
            owner = adapt_owner(old_action.owner, mesh)
            loads = HighLoads(owner, decimals(state['coordinates']), state['rates'], mesh, 'primary', deadline)
            solver, solution = reconstructed_solver(state)
            action = HighAction(loads, mesh, solver, solution)
            old_engine = NativeKernel(mesh, packet['gram_support'], True)
            engine = loads.native_engine
            for label in [-.37, 0., .41]:
                data = physical_data(engine, loads, action, label)
                for variant in ['actual', 'source_jump_control']:
                    field = data['field'].copy()
                    if variant == 'source_jump_control':
                        field[engine.indices[engine.anchor, 1]] += Decimal('1e-13')
                    old = old_engine.evaluate(data['edges'], field, data['beta'])
                    current = engine.evaluate(data['edges'], field, data['beta'], data['beta_radial'])
                    edge = old['edge_gradient'].copy()
                    edge[engine.native_edges] += old['load'] * data['beta_radial']
                    for name, first, second in [('image', current['image'], old['image']),
                        ('field', current['field_gradient'], old['field_gradient']), ('edge', current['edge_gradient'], edge)]:
                        error = float(maximum(first - second) / max(maximum(second), Decimal('1e-40')))
                        evidence.check(str(label) + ':' + variant + ':' + name, error < 2e-20, error)
                native = data['edges'][engine.native_edges]
                beta = 1 + native**2
                current = engine.evaluate(data['edges'], data['field'], beta, 2 * native)
                edge_direction = (data['edges'] - data['edges'][0]) * (data['edges'][-1] - data['edges']) / 100
                field_direction = data['field'] / 7
                expected = sum(current['field_gradient'] * field_direction, Decimal(0)) + sum(current['edge_gradient'] * edge_direction, Decimal(0))
                approximations = []
                for step in [Decimal('1e-5'), Decimal('5e-6')]:
                    energies = []
                    for sign in [-1, 1]:
                        changed_edges = data['edges'] + sign * step * edge_direction
                        changed = engine.evaluate(changed_edges, data['field'] + sign * step * field_direction,
                            1 + changed_edges[engine.native_edges]**2)
                        energies.append(changed['energy'])
                    approximations.append((energies[1] - energies[0]) / (2 * step))
                corrected = (4 * approximations[1] - approximations[0]) / 3
                error = float(abs(corrected - expected) / max(abs(expected), Decimal('1e-40')))
                evidence.check(str(label) + ':native_action_directional_derivative', error < 1e-14, error)
        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
        system = zero_system(action, 12, 48, deadline, progress)
        old_row = next(row for row in parent['results'] if row['name'] == 'iteration0')
        old = read_archive(evidence.root / old_row['path'])
        old_matrix = load_npz(evidence.root / old_row['matrix_path'])
        difference = system['matrix'] - old_matrix
        matrix_error = float(max(abs(difference.data), default=0.))
        force_error = float(np.max(abs(system['force'] - old['wave_source_force'])))
        diagnostic = evidence.output / 'P2-replay.npz'
        np.savez_compressed(diagnostic, force=system['force'], old_force=old['wave_source_force'],
            wave=system['wave_force'], dust=system['dust_force'], gradient=action.gradient)
        evidence.own(diagnostic, 'outputs')
        evidence.report['force_components'] = dict(field=float(np.max(abs(system['force'][:, :-1] - old['wave_source_force'][:, :-1]))),
            source=float(np.max(abs(system['force'][:, -1] - old['wave_source_force'][:, -1]))))
        evidence.check('P2_full_mass_replay', matrix_error < 2e-13, matrix_error)
        evidence.check('P2_wave_source_force_replay', force_error < 2e-13, force_error)
        solved = system['inverse'].solve(old['force'].ravel()).reshape(old['force'].shape)
        solve_error = float(np.max(abs(solved - old['acceleration'])))
        evidence.check('P2_complete_acceleration_replay', solve_error < 2e-8, solve_error)
        evidence.report.update(seconds=perf_counter() - started, adapter_qualified=True, degree_six_live_state_solved=False,
            matrix_error=matrix_error, wave_source_force_error=force_error, acceleration_error=solve_error,
            github_action=False, subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

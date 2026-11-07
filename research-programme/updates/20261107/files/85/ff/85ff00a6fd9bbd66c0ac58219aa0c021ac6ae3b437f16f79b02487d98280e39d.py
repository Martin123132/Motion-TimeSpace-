from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_position_reaction_20260929 import ResponseSum, second_radial, native_position_force
from annular_old_field_reaction_20260929 import coefficient_data
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_physical_native_kernel_20260928 import NativeKernel, decimals
from derive_annular_native_shape_stress_20260928 import physical_data
from decimal import Decimal, localcontext
from time import perf_counter
import hashlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-position-native-force-validation-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 1800
    try:
        seal_path = evidence.output.parent / 'annular-position-time-final-integrity-20260929.json'
        seal = json.loads(seal_path.read_text())
        evidence.own(seal_path)
        digests = {key: value for key, value in seal['hashes'].items() if key != 'CURRENT_LOCAL_RESUME.md'}

        def read(relative):
            path = evidence.root / relative
            if hashlib.sha256(path.read_bytes()).hexdigest() != digests[relative]:
                raise RuntimeError('Changed native validator input: ' + relative)
            evidence.own(path)
            return load_owned(evidence, digests, path)

        status = lambda name: read(str((evidence.output.parent / name / 'status.json').relative_to(evidence.root)))
        live, jets, positions = [status(name) for name in ['annular-live-support-acceleration-attempt01',
            'annular-position-metric-jet-validation-attempt01', 'annular-compensated-position-attempt04']]
        evidence.report.update(scope='Independent original native-energy mixed derivative against position-force covector',
            github_action=False, subagents_used=False, original_workbench_write=False, new_trajectories=0,
            supports_k0_native_term_only=True, C0_force_current_column_computed=False)
        with localcontext() as context:
            context.prec = 70
            for level in ['fine', 'third']:
                branch = 'MTS-primary'
                loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                for relative in sources.values():
                    read(relative)
                match = lambda report: next(row for row in report['cases'] if row['branch'] == branch and row['level'] == level)
                previous, jet, positioned = map(match, [live, jets, positions])
                directions = read(previous['direction_path'])
                correction = read(previous['paths']['projection'])['correction']
                field_direction, source_direction = directions['field_vertices'] - correction[:, :-1], -correction[:, -1]
                restore = lambda archive: MetricResponse(*reconstructed_solver(archive), None, 0., [])
                position = ResponseSum(restore(read(positioned['paths']['response'])), restore(read(jet['paths']['transported_old_metric'])))
                packet = read(sources['packet'])
                native = NativeKernel(action.mesh, packet['gram_support'], True)
                tests = []
                for label in [-.31, 0., .287]:
                    data = physical_data(native, loads, action, label)
                    cardinal = data['cardinal']
                    field_change = decimals(cardinal @ field_direction)
                    edge_change = decimals(cardinal @ directions['edge_vertices']) + data['displacement'] * Decimal.from_float(float(cardinal @ source_direction))
                    radius = np.asarray(data['edges'][native.native_edges], float)
                    movement = np.asarray(edge_change[native.native_edges], float)
                    values, radial = action.solver.values(action.solution, radius)
                    second = second_radial(action.solver, action.solution, radius)
                    pos, pos_r = position.at(radius)
                    unused, beta, unused2, beta_r = coefficient_data(radius + 1e-25j * movement,
                        values + 1e-25j * (pos + radial * movement), radial + 1e-25j * (pos_r + second * movement))
                    beta_change, beta_r_change = decimals(beta.imag / 1e-25), decimals(beta_r.imag / 1e-25)
                    force, unused, unused2 = native_position_force(native, loads, action, label,
                        field_direction, source_direction, directions['edge_vertices'], position)
                    field_test = decimals(np.sin(np.arange(native.count) * .37) / max(native.count, 1))
                    source_test = Decimal('.17')
                    predicted = -sum(decimals(force[:-1]) * field_test, Decimal(0)) - Decimal.from_float(float(force[-1])) * source_test
                    step = Decimal('1e-10')
                    total = Decimal(0)
                    for first in [-1, 1]:
                        for second_sign in [-1, 1]:
                            shifted_edges = data['edges'] + first * step * edge_change + second_sign * step * source_test * data['displacement']
                            shifted_field = data['field'] + first * step * field_change + second_sign * step * field_test
                            shifted_beta = data['beta'] + first * step * beta_change
                            shifted_beta += second_sign * step * source_test * data['displacement'][native.native_edges] * data['beta_radial']
                            shifted_beta += first * second_sign * step**2 * source_test * data['displacement'][native.native_edges] * beta_r_change
                            total += first * second_sign * native.evaluate(shifted_edges, shifted_field, shifted_beta, adjoint=False)['energy']
                    measured = total / (4 * step**2)
                    error = abs(measured - predicted)
                    tolerance = Decimal('1e-25') + Decimal('2e-7') * abs(predicted)
                    result = dict(label=label, predicted=float(predicted), original_energy_mixed=float(measured),
                        error=float(error), tolerance=float(tolerance))
                    evidence.check(level + ':native_energy_mixed:' + str(label), error <= tolerance, result)
                    tests.append(result)
                evidence.report['cases'].append(dict(branch=branch, level=level, tests=tests))
                evidence.save()
                print(json.dumps(evidence.report['cases'][-1]), flush=True)
        evidence.report['seconds'] = perf_counter() - started
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

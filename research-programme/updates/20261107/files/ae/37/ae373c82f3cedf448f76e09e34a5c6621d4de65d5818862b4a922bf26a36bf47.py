from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_position_reaction_20260929 import ResponseSum
from annular_old_field_reaction_20260929 import coefficient_data
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from annular_moving_Legendre_current_20260921 import samples
from annular_directional_coupled_Euler_20260928 import interpolate_nodal
from scipy.sparse import load_npz
from time import perf_counter
from decimal import localcontext
import json
import numpy as np


def field_force(loads, action, directions, correction, mode_rate, position, order, spatial_order):
    names = ['metric', 'transport', 'gradient', 'total']
    result = {name: np.zeros_like(loads.rates) for name in names}
    labels, weights = np.polynomial.legendre.leggauss(order)
    labels, weights = labels / 2, weights / 2
    weights *= 6 * (labels + .5) * (.5 - labels)
    edges = np.asarray([float(value) for value in action.edges])
    field_direction = directions['field_vertices'] - correction[:, :-1]
    for label, weight in zip(labels, weights):
        row = samples(action, label, spatial_order)
        geometry, quad, cardinal = row['geometry'], row['quadrature'], row['cardinal']
        radius, jacobian = geometry['radius'], geometry['jacobian']
        indices = np.asarray(action.mesh['elements'])[quad['cells']]
        selected = indices >= 0
        widths = np.diff(edges)[quad['cells']] * jacobian
        interpolate = lambda array: interpolate_nodal(cardinal @ array, indices, quad['local'], widths)
        unused, field_r = interpolate(field_direction)
        transported = interpolate(mode_rate[:, :-1])[0]
        source_mode = -float(cardinal @ correction[:, -1])
        source_rate = float(cardinal @ mode_rate[:, -1])
        edge = cardinal @ directions['edge_vertices']
        cells, local = quad['cells'], quad['local']
        eta = (1 - local) * edge[cells] + local * edge[cells + 1]
        eta_r = (edge[cells + 1] - edge[cells]) / widths
        displacement = geometry['displacement']
        displacement_r = geometry['jacobian_source'] / jacobian
        movement = eta + displacement * source_mode
        movement_r = eta_r + displacement_r * source_mode
        speed = displacement * row['velocity']
        movement_rate = displacement * source_rate
        gradient = row['gradient'] / jacobian
        gradient_change = field_r - gradient * movement_r
        temporal = row['rate'] - speed * gradient
        temporal_change = transported - movement_rate * gradient - speed * gradient_change
        values, radial = action.solver.values(action.solution, radius)
        alpha, beta, unused, unused2 = coefficient_data(radius, values, radial)
        alpha_changed, beta_changed, unused, unused2 = coefficient_data(radius + 1e-25j * movement,
            values + 1e-25j * (position.values(radius) + radial * movement), radial)
        density = dict(metric=-(alpha_changed.imag / 1e-25 * temporal * speed + beta_changed.imag / 1e-25 * gradient),
            transport=-alpha * (temporal_change * speed + temporal * movement_rate), gradient=-beta * gradient_change)
        density['total'] = sum(density.values())
        for name, value in density.items():
            local_force = quad['measure'][:, None] * value[:, None] * quad['radial']
            vector = np.zeros(loads.rates.shape[1])
            np.add.at(vector, indices[selected], local_force[selected])
            result[name] += weight * np.outer(cardinal, vector)
    return result


def main():
    evidence = EvidenceRun('annular-position-force-diagnostic-attempt01', __file__)
    start, deadline = perf_counter(), perf_counter() + 1800
    try:
        parent_path = evidence.output.parent / 'annular-position-reaction-attempt01/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        digests = dict(parent['inputs'], **parent['outputs'])
        read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
        status = lambda name: read(str((evidence.output.parent / name / 'status.json').relative_to(evidence.root)))
        live, jets, positions = [status(name) for name in ['annular-live-support-acceleration-attempt01',
            'annular-position-metric-jet-validation-attempt01', 'annular-compensated-position-attempt04']]
        branch, level = 'reference-reference', 'fine'
        loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
        match = lambda report: next(row for row in report['cases'] if row['branch'] == branch and row['level'] == level)
        previous, jet, positioned = map(match, [live, jets, positions])
        directions = read(previous['direction_path'])
        correction = read(previous['paths']['projection'])['correction']
        mode_rate = read(jet['paths']['completed_metric_time'])['mode_rate']
        restore = lambda archive: MetricResponse(*reconstructed_solver(archive), None, 0., [])
        position = ResponseSum(restore(read(positioned['paths']['response'])), restore(read(jet['paths']['transported_old_metric'])))
        owner = read(sources['parent'])
        centre = next(row for row in owner['centres'] if row.get('route') == 'resampled')
        inverse = BandedSourceInverse(load_npz(evidence.root / centre['matrix_path']), loads.rates.shape)
        outputs = {}
        with localcontext() as context:
            context.prec = 70
            for order, spatial in [(48, 12), (64, 12), (96, 12), (128, 12), (48, 20), (64, 20)]:
                result = field_force(loads, action, directions, correction, mode_rate, position, order, spatial)
                path = evidence.output / ('force-' + str(order) + '-' + str(spatial) + '.npz')
                np.savez_compressed(path, **result)
                evidence.own(path, 'outputs')
                baseline = outputs.get((48, 12), result)
                comparisons = {key: dict(raw=float(np.max(abs(result[key] - baseline[key]))),
                    inverse=float(np.max(abs(inverse.solve((result[key] - baseline[key]).ravel()))))) for key in result}
                summary = dict(order=order, spatial=spatial, comparisons_to_48_12=comparisons, seconds=perf_counter() - start)
                evidence.report['cases'].append(summary)
                evidence.save()
                print(json.dumps(summary), flush=True)
                outputs[order, spatial] = result
        evidence.report['seconds'] = perf_counter() - start
        evidence.report['scope'] = 'Diagnostic only; previous quadrature failure retained, no acceptance gate changed'
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

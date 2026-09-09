import hashlib
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_local_ward_identity_20260909 import LocalWardIdentity
    from annular_metric_link_quadratic_20260909 import CachedMetricLinkRouthian, MetricLinkQuadrature

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-metric-evolution-independent-controls'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'scope': 'Independently recompute the final full Ward remainder and all shift components, verify identical external histories and non-projected constraint drift, and distinguish discretization residuals from full coupled evolution.'}
    (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def own(path):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        report['inputs'][str(path.relative_to(root))] = digest
        return digest

    def maximum(value):
        return float(numerical.max(numerical.abs(value)))

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        print(name + ': ' + str(bool(passed)), flush=True)

    class CachedWard(LocalWardIdentity):
        def connection_transport(self):
            packed, system = self.arrays['corrected'], self.system
            return system.links.matrix(packed[system.slices[0]], packed[system.slices[1]], system.constants)

    save()
    try:
        own(Path(__file__))
        for name in ['annular-metric-quadratic-derived', 'annular-metric-evolution-smoke']:
            owner_path = intake / name / 'status.json'
            own(owner_path)
            owner = json.loads(owner_path.read_text())
            check(name + '_complete', owner['state'] == 'complete' and owner['passed'] == owner['total'])
            check(name + '_hashes_unchanged', all(own(root / path) == digest for path, digest in {**owner['inputs'], **owner['outputs']}.items()))
        for case_name in ['canonical', 'nonlinear_modulated']:
            case_path = intake / 'annular-constraint-correction-initial' / (case_name + '.json')
            own(case_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            kappa = float(symbolic.sympify(case['normalization_kappa']))
            for intervals in [16, 32]:
                tag = case_name + '_N' + str(intervals)
                initial = {}
                for branch, label in [('GR', 'GR'), ('metric_Gram', 'Gram')]:
                    path = intake / 'annular-constraint-routhian-derived' / (tag + '_' + label + '.npz')
                    own(path)
                    with numerical.load(path) as loaded:
                        initial[branch] = {name: loaded[name].copy() for name in loaded.files}
                shared = ['radius', 'faces', 'scalar', 'momentum', 'defect', 'defect_time', 'defect_acceleration', 'endpoint_acceleration', 'outer_clock']
                check(tag + '_phase_and_external_inputs_identical', all(numerical.array_equal(initial['GR'][name], initial['metric_Gram'][name]) for name in shared), {'fields': shared})
                check(tag + '_same_initial_inner_mass', initial['GR']['corrected'][0] == initial['metric_Gram']['corrected'][0])
                for branch in ['GR', 'metric_Gram']:
                    source = initial[branch]
                    basis = MixedActionBasis(source['radius'])
                    links = MetricLinkQuadrature(basis)
                    node_count, face_count = basis.radii.size, basis.faces.size
                    trajectory_path = intake / 'annular-metric-evolution-smoke' / (tag + '_' + branch + '_steps16.npz')
                    own(trajectory_path)
                    with numerical.load(trajectory_path) as loaded:
                        trajectory = {name: loaded[name].copy() for name in loaded.files}
                    check(tag + '_' + branch + '_nonzero_actual_evolution', maximum(trajectory['state'][-1] - trajectory['state'][0]) > 1e-5)
                    for index in [0, 8, 16]:
                        time, state = trajectory['time'][index], trajectory['state'][index]
                        scalar, momentum, packed = state[:node_count], state[node_count:2 * node_count], state[2 * node_count:]
                        defect = source['defect'] + time * source['defect_time'] + time**2 * source['defect_acceleration'] / 2
                        defect_time = source['defect_time'] + time * source['defect_acceleration']
                        outer_clock = source['outer_clock'][0] + time * source['outer_clock'][1]
                        system = CachedMetricLinkRouthian(basis, scalar, defect, defect_time, constants, kappa, momentum, outer_clock, links=links)
                        include_gram = branch != 'GR'
                        tangent = system.constraint_tangent(packed, include_gram, source['defect_acceleration'], source['endpoint_acceleration'], source['outer_clock'][1])
                        unused_value, gradient, hessian = system.evaluate(packed, include_gram)
                        arrays = dict(source, corrected=packed, scalar=scalar, momentum=momentum, defect=defect, defect_time=defect_time, gradient_final=gradient, Hessian_final=hessian, **tangent)
                        identity = CachedWard(system, arrays)
                        ward = identity.evaluate(include_gram)
                        sample_name = tag + '_' + branch + '_sample' + str(index)
                        check(sample_name + '_recomputed_full_shift_and_constraint_vectors', maximum(tangent['shift_residual'] - trajectory['shifts'][index]) < 1e-13 and maximum(gradient[system.free] - trajectory['constraints'][index]) < 1e-13)
                        check(sample_name + '_full_Ward_identity', maximum(ward['identity_error']) < 2e-11, maximum(ward['identity_error']))
                        mass, lapse = packed[system.slices[0]], packed[system.slices[1]]
                        gamma = (basis.node_to_face @ lapse)**2 * (1 - 2 * mass / basis.faces - constants['Lambda'] * basis.faces**2 / 3)
                        desired = -numerical.eye(face_count) / gamma[:, None]
                        values, slopes = numerical.zeros((node_count, face_count)), numerical.zeros((node_count, face_count))
                        slopes[0], slopes[-1] = desired[0], desired[-1]
                        fractions = (basis.faces[1:-1] - basis.radii[:-1]) / basis.spacing
                        for cell, fraction in enumerate(fractions):
                            left = 3 * fraction**2 - 4 * fraction + 1
                            right = 3 * fraction**2 - 2 * fraction
                            values[cell + 1] = values[cell] + basis.spacing * (desired[cell + 1] - left * slopes[cell] - right * slopes[cell + 1]) / (6 * fraction * (1 - fraction))
                        inverse = numerical.concatenate([values, basis.spacing * slopes], axis=0)
                        check(sample_name + '_constructive_all_face_right_inverse', maximum(ward['shift_generator'] @ inverse - numerical.eye(face_count)) < 1e-12)
                        terms = {name: sign * inverse.T @ ward[name] for name, sign in [('bulk_remainder', 1), ('Gram_coefficient_remainder', -1), ('Gram_link_remainder', -1), ('lifting_work', -1), ('scalar_endpoint_and_bulk_work', -1), ('mass_boundary_and_bulk_work', -1), ('lapse_constraint_derivative_work', -1)]}
                        reconstructed = sum(terms.values())
                        check(sample_name + '_independently_reconstructed_all_shift_rows', maximum(reconstructed - tangent['shift_residual']) < 2e-11)
                        check(sample_name + '_unsolved_shift_not_hidden_by_small_constraint_drift', maximum(tangent['shift_residual']) > 100 * max(maximum(gradient[system.free]), 1e-15))
                        target = destination / (sample_name + '.npz')
                        numerical.savez_compressed(target, right_inverse=inverse, full_shift_residual=tangent['shift_residual'], reconstructed_shift_residual=reconstructed, free_constraint=gradient[system.free], **{'Ward_' + name: value for name, value in ward.items()}, **{'shift_part_' + name: value for name, value in terms.items()})
                        report['outputs'][str(target.relative_to(root))] = hashlib.sha256(target.read_bytes()).hexdigest()
                        report['samples'].append({'case': case_name, 'intervals': intervals, 'branch': branch, 'time': float(time), 'shift_residual_max': maximum(tangent['shift_residual']), 'Ward_error': maximum(ward['identity_error']), 'full_residual_reconstruction_error': maximum(reconstructed - tangent['shift_residual']), 'contributions_max_norm': {name: maximum(value) for name, value in terms.items()}, 'raw_lifting_Euler_max': maximum(ward['lifting_euler']), 'basis_dependent_split_not_a_unique_physical_attribution': True})
                        save()
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('all_owned_sources_unchanged', all(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest for name, digest in report['inputs'].items()))
        check('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
        report.update(passed=sum(row['passed'] for row in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
        report['state'] = 'complete' if report['passed'] == report['total'] else 'failed'
        save()
        if report['state'] == 'complete':
            (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')
        print(json.dumps({key: report[key] for key in ['state', 'passed', 'total', 'completed_utc']}), flush=True)
        if report['state'] != 'complete':
            raise SystemExit(1)
    except Exception as error:
        report.update(state='failed', failure=repr(error), traceback=traceback.format_exc(), completed_utc=datetime.now(timezone.utc).isoformat())
        save()
        raise


if __name__ == '__main__':
    run()

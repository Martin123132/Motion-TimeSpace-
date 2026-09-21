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
    from scipy.linalg import cholesky, solve_triangular, svd
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_frozen_second_jet_20260912 import FrozenSecondJet

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    destination = intake / 'annular-frozen-second-jet-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'checks': [], 'inputs': {}, 'outputs': {}, 'cases': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'formal_interior_time_germ_only': True, 'boundary_accelerations_parent_owned': False, 'protocol': 'N16 frozen accepted initial fields and full phase maps. Full nonlinear-history second jet, not differentiation of the P=0-only operator. All 19 Cddot rows, two free-P trace accelerations and outer clock rate. Derived drive accelerations reported; zero-acceleration drive continuation is a separately labelled smoke assumption. One BelowNormal single-core worker.'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    def archive(name, arrays):
        path = destination / (name + '.npz')
        numerical.savez_compressed(path, **arrays)
        with numerical.load(path, allow_pickle=False) as saved:
            check(name + '_finite_roundtrip', set(saved.files) == set(arrays) and all(numerical.isfinite(value).all() and numerical.array_equal(value, saved[key]) for key, value in arrays.items()))
        own(path, 'outputs')

    def describe(result):
        return {'Cddot_max': float(abs(result['constraint_second']).max()), 'Cddot_original_rows_max': float(abs(result['constraint_second'][:17]).max()), 'Cddot_extra_rows': result['constraint_second'][-2:].tolist(), 'Pddot_endpoints': result['nodes']['P'][[0, -1]].tolist(), 'clock_rate_error': float(result['clock_first']), 'inferred_drive_accelerations': result['inferred_drive_accelerations'].tolist(), 'full_compatibility_max': float(abs(result['compatibility']).max()), 'finite_second_jet_gate': bool(abs(result['compatibility']).max() < 1e-10), 'weighted_current_first_error': float(abs(result['weighted_current_first_identity']).max())}

    def result_arrays(result):
        output = {key: value for key, value in result.items() if isinstance(value, numerical.ndarray)}
        output.update({key + '_second_coefficients': value for key, value in result['second'].items()})
        output.update({key + '_second_nodes': value for key, value in result['nodes'].items()})
        return output

    save()
    try:
        prior_path = intake / 'annular-cubic-boundary-final-integrity.json'
        prior = json.loads(prior_path.read_text())
        own(prior_path)
        check('previous_finite_first_jet_sealed', prior['state'] == 'complete' and prior['finite_initial_boundary_first_jet_pass'])
        known = {}
        for table in ['inputs', 'outputs']:
            for name, expected in prior[table].items():
                if name not in known:
                    known[name] = digest(root / name)
                if known[name] != expected:
                    raise RuntimeError('Changed source: ' + name)
                report['inputs'][name] = expected
        for name in ['annular_frozen_second_jet_20260912.py', Path(__file__).name]:
            path = root / 'scripts' / name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            snapshot = destination / ('executed-' + name)
            snapshot.write_bytes(path.read_bytes())
            own(snapshot, 'outputs')
        common = CommonProfile(root)
        for branch in ['GR', 'metric_Gram']:
            print('Assembling full second jet: ' + branch, flush=True)
            model = FrozenSecondJet(common, branch)
            higher = FrozenSecondJet(common, branch, higher=True)
            candidate = model.candidate()
            base = model.evaluate(candidate)
            check(branch + '_all_nineteen_C_and_Cdot_replayed', abs(base['constraint'] - model.first['constraint']).max() < 1e-12 and base['Cdot_replay_error'] < 1e-12)
            check(branch + '_weighted_current_time_identity', abs(base['weighted_current_first_identity']).max() < 1e-10)
            transform = solve_triangular(cholesky(model.data[model.surface]['eta'].T @ (model.weights[:, None] * model.data[model.surface]['eta']), lower=True).T, numerical.eye(19), lower=False)
            columns = []
            drive_columns = []
            for column in range(19):
                evaluated = model.evaluate(candidate.astype(complex) + 1e-25j * transform[:, column])
                columns.append(evaluated['compatibility'].imag / 1e-25)
                drive_columns.append(evaluated['inferred_drive_accelerations'].imag / 1e-25)
            matrix = numerical.column_stack(columns)
            drive_matrix = numerical.column_stack(drive_columns)
            direction = numerical.cos(numerical.arange(19) + .71) * .001
            moved = model.evaluate(candidate + transform @ direction)
            affine_error = float(abs(moved['compatibility'] - base['compatibility'] - matrix @ direction).max())
            check(branch + '_second_jet_is_affine_in_lapse_rate', affine_error < 1e-8, affine_error)
            record = {'branch': branch, 'candidate': describe(base), 'solutions': [], 'first_data_and_frames_unchanged': True}
            report['cases'].append(record)
            archive(branch + '_candidate_second_jet', result_arrays(base))
            for smoke in [False, True]:
                selected_matrix = numerical.concatenate([matrix, drive_matrix]) if smoke else matrix
                selected_rhs = numerical.concatenate([base['compatibility'], base['inferred_drive_accelerations']]) if smoke else base['compatibility']
                left, singular, right = svd(selected_matrix, full_matrices=False)
                for cutoff in [1e-8, 1e-10, 1e-12]:
                    active = singular > cutoff * singular[0]
                    update = -(right[active].T / singular[active]) @ (left[:, active].T @ selected_rhs)
                    selected = candidate + transform @ update
                    evaluated = model.evaluate(selected)
                    fine = higher.evaluate(selected)
                    linear_residual = selected_matrix @ update + selected_rhs
                    replay_residual = numerical.concatenate([evaluated['compatibility'], evaluated['inferred_drive_accelerations']]) if smoke else evaluated['compatibility']
                    label = ('affine_drive_smoke' if smoke else 'free_drive_compatibility') + '_' + str(cutoff)
                    row = {'label': label, 'zero_acceleration_drive_assumed': smoke, 'relative_SVD_cutoff': cutoff, 'retained_rank': int(active.sum()), 'singular_values': singular.tolist(), 'lapse_rate_L2_update': float(numerical.linalg.norm(update)), 'lapse_rate_max': float(abs(model.data[model.surface]['eta'] @ selected).max()), 'linear_replay_error': float(abs(linear_residual - replay_residual).max()), 'primary': describe(evaluated), 'higher': describe(fine), 'zero_acceleration_smoke_gate': bool(smoke and abs(replay_residual).max() < 1e-10)}
                    record['solutions'].append(row)
                    archive(branch + '_' + label, result_arrays(evaluated))
                    print(json.dumps({'branch': branch, 'label': label, 'rank': row['retained_rank'], 'residual': row['primary']['full_compatibility_max'], 'higher': row['higher']['full_compatibility_max'], 'lapse_rate_max': row['lapse_rate_max']}), flush=True)
            archive(branch + '_affine_compatibility_operator', {'matrix': matrix, 'drive_matrix': drive_matrix, 'base': base['compatibility'], 'base_drives': base['inferred_drive_accelerations'], 'lapse_metric_transform': transform, 'candidate': candidate})
            save()
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        report['completed_utc'] = datetime.now(timezone.utc).isoformat()
        save()
        print(json.dumps({'state': report['state'], 'checks': len(report['checks']), 'finite_second_jet_any_pass': any(row['primary']['finite_second_jet_gate'] and row['higher']['finite_second_jet_gate'] for case in report['cases'] for row in case['solutions']), 'new_evolution': False}), flush=True)
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()

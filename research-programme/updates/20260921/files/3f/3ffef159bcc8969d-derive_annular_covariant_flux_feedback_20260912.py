import hashlib
import json
import sys
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from scipy.linalg import solve
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_canonical_trace_context_20260911 import load_archive
    from annular_covariant_joint_preparation_20260912 import JointPreparation
    from annular_covariant_flux_moments_20260912 import complete_flux_moments, install, energy_balanced, carrier_family, functionals

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    source = intake / 'annular-covariant-flux-moments-attempt01'
    destination = intake / 'annular-covariant-flux-feedback-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'cases': [], 'inputs': {}, 'outputs': {}, 'maximum_additional_feedback_iterations': 4, 'valid_for_physics_claim': False, 'new_evolution': False, 'full_first_jet_closed': False, 'full_second_jet_closed': False, 'interval_certificate': False, 'old_working_branch_unchanged': True, 'basis_rebuilt_from_original79_not_cumulatively_enlarged': True}

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    save()
    try:
        previous_path = source / 'status.json'
        previous = json.loads(previous_path.read_text())
        check('frozen_trial_complete_not_a_first_jet_pass', previous['state'] == 'complete' and all(not item['full_first_jet_gate'] for case in previous['cases'] for item in case['results']))
        for table in ['inputs', 'outputs']:
            for name, expected in previous[table].items():
                if name in report['inputs']:
                    continue
                if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Changed evidence: ' + name)
                report['inputs'][name] = expected
        own(previous_path)
        snapshot = destination / ('executed-' + Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        common = CommonProfile(root)
        for branch in ['GR', 'metric_Gram']:
            model = JointPreparation(common, branch)
            old_frames = model.frame
            raw_frames = load_archive(source / (branch + '_frozen_extended_frames.npz'))
            frames = {surface: {kind: raw_frames[surface + '__' + kind] for kind in ['q', 'qr', 'p']} for surface in old_frames}
            install(model, frames)
            coefficients = load_archive(source / (branch + '_moment_candidate.npz'))['coefficients']
            target = model.evaluate(coefficients)
            case = {'branch': branch, 'iterations': []}
            report['cases'].append(case)
            previous_generator = target['current']['generator']
            for iteration in range(1, 5):
                install(model, old_frames)
                frames, unused_family, construction, diagnostics = complete_flux_moments(model, target)
                install(model, frames)
                coefficients, target, history = model.solve()
                higher = model.evaluate(coefficients, 'check')
                record = {'iteration': iteration, 'construction': diagnostics, 'Newton_history': history, 'surfaces': []}
                case['iterations'].append(record)
                archive = dict(construction, coefficients=coefficients)
                for surface, result, weights in [('quad', target, model.context.weights), ('check', higher, model.context.check_weights)]:
                    energy = energy_balanced(model, result)
                    family = carrier_family(model, result)
                    projected_coefficients = solve(model.pairings[surface], frames[surface]['p'].T @ (weights[:, None] * family[surface]))
                    projected = {name: frames[name]['q'] @ projected_coefficients for name in frames}
                    defect = functionals(model, result['fields'], result['energy'], projected, surface) - functionals(model, result['fields'], result['energy'], family, surface)
                    row = {'surface': surface, 'C0': float(abs(result['residual'][:19]).max()), 'C1': float(abs(energy['C1']).max()), 'metric_work': float(abs(result['metric_work']).max()), 'flux_work': float(abs(result['projection_work']).max()), 'mass_endpoint_error': float(abs(result['mu_nodes'][[0, -1]] - result['raw_nodes'][[0, -1]]).max()), 'P1_endpoint': float(abs(result['P_nodes'][[0, -1]]).max()), 'full16_moment_defect': float(abs(defect[:19]).max()), 'full16_endpoint_defect': float(abs(defect[19:]).max()), 'Ward_error': float(abs(energy['Ward_error']).max())}
                    row['full_first_jet_gate'] = max(row['C0'], row['C1'], row['mass_endpoint_error'], row['P1_endpoint']) < 1e-10
                    record['surfaces'].append(row)
                    for key in ['C1', 'rho', 'p_first', 'Ward_error']:
                        archive[surface + '__' + key] = energy[key]
                    for key in ['mu_coeff', 'P_coeff', 'mu_nodes', 'P_nodes', 'raw_nodes', 'projection_work', 'metric_work', 'residual']:
                        archive[surface + '__' + key] = result[key]
                    archive[surface + '__generator'] = result['current']['generator']
                    check(branch + '_' + str(iteration) + '_' + surface + '_initial_data_and_Ward_validated', row['C0'] < 1e-10 and row['Ward_error'] < 1e-10, row)
                record['generator_change_max'] = float(abs(target['current']['generator'] - previous_generator).max())
                record['current_frozen_mass_dimension'] = frames['quad']['q'].shape[1]
                previous_generator = target['current']['generator']
                path = destination / (branch + '_iteration' + str(iteration) + '.npz')
                np.savez_compressed(path, **archive)
                own(path, 'outputs')
                path = destination / (branch + '_iteration' + str(iteration) + '_frames.npz')
                np.savez_compressed(path, **{surface + '__' + kind: values for surface, maps in frames.items() for kind, values in maps.items()})
                own(path, 'outputs')
                save()
                print(json.dumps({'branch': branch, 'iteration': iteration, 'generator_change': record['generator_change_max'], 'surfaces': record['surfaces']}), flush=True)
                if all(row['full_first_jet_gate'] for row in record['surfaces']):
                    break
            case['completed_fixed_budget_not_a_contraction_proof'] = True
            save()
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        save()
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()

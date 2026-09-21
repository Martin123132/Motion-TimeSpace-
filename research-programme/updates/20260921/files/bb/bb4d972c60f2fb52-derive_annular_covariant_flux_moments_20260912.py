import hashlib
import json
import sys
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_canonical_trace_context_20260911 import load_archive
    from annular_covariant_joint_preparation_20260912 import JointPreparation
    from annular_covariant_flux_moments_20260912 import complete_flux_moments, install, energy_balanced, carrier_family, functionals
    from scipy.linalg import solve

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    destination = intake / 'annular-covariant-flux-moments-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'cases': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'full_first_jet_closed': False, 'full_second_jet_closed': False, 'interval_certificate': False, 'no_publication': True, 'previous_working_branch_unchanged': True}

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
        previous_path = intake / 'annular-covariant-joint-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_seal_complete_and_no_full_first_jet_claim', previous['state'] == 'complete' and not previous['full_first_jet_closed'])
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
            print('Continuous-coordinate/full-family moment construction: ' + branch, flush=True)
            model = JointPreparation(common, branch)
            old_frame = model.frame
            original = load_archive(intake / 'annular-covariant-joint-preparation-attempt01' / (branch + '_joint_candidate.npz'))
            baseline = model.evaluate(original['coefficients'])
            base_energy = energy_balanced(model, baseline)
            frames, family, construction, diagnostics = complete_flux_moments(model, baseline)
            report['cases'].append({'branch': branch, 'construction': diagnostics, 'baseline_C1': float(abs(base_energy['C1']).max())})
            save()
            print(json.dumps(diagnostics), flush=True)
            check(branch + '_all_old_columns_retained_exactly', all(np.array_equal(frames[surface][kind][:, :old_frame[surface][kind].shape[1]], old_frame[surface][kind]) for surface in frames for kind in ['q', 'qr', 'p']))
            check(branch + '_all16_source_family_not_just_actual_amplitude', diagnostics['family_dimension'] == 16 and diagnostics['source_moment_error'] < 1e-8 and diagnostics['endpoint_trace_error'] < 1e-9, diagnostics)
            check(branch + '_canonical_pair_well_conditioned', diagnostics['new_pairing_condition'] < 100 and diagnostics['block_pairing_error'] < 1e-8)
            install(model, frames)
            coefficients, candidate, history = model.solve()
            higher = model.evaluate(coefficients, 'check')
            summaries = []
            archive = dict(construction, coefficients=coefficients)
            for surface, result, weights in [('quad', candidate, model.context.weights), ('check', higher, model.context.check_weights)]:
                energy = energy_balanced(model, result)
                regenerated = carrier_family(model, result)
                projected_coefficients = solve(model.pairings[surface], model.frame[surface]['p'].T @ (weights[:, None] * regenerated[surface]))
                projected = {name: model.frame[name]['q'] @ projected_coefficients for name in frames}
                defect = functionals(model, result['fields'], result['energy'], projected, surface) - functionals(model, result['fields'], result['energy'], regenerated, surface)
                row = {'surface': surface, 'C0': float(abs(result['residual'][:19]).max()), 'C1': float(abs(energy['C1']).max()), 'metric_work': float(abs(result['metric_work']).max()), 'flux_projection_work': float(abs(result['projection_work']).max()), 'C1_interior': float(abs(energy['C1'][1:16]).max()), 'mass_drive_error': float(result['mu_nodes'][0] - model.saved['boundary_velocity'][0]), 'raw_mass_drive_error': float(result['raw_nodes'][0] - model.saved['boundary_velocity'][0]), 'mass_endpoint_projection_error': float(abs(result['mu_nodes'][[0, -1]] - result['raw_nodes'][[0, -1]]).max()), 'P1_endpoint': float(abs(result['P_nodes'][[0, -1]]).max()), 'regenerated_all16_moment_error': float(abs(defect[:19]).max()), 'regenerated_all16_endpoint_error': float(abs(defect[19:]).max()), 'Ward_reconstruction': float(abs(energy['Ward_error']).max()), 'F_min': min(float(data['F'].min()) for data in result['fields'].values()), 'N_min': min(float(data['N'].min()) for data in result['fields'].values()), 'J_min': float(result['current']['J'].min()), 'J_max': float(result['current']['J'].max())}
                row['full_first_jet_gate'] = max(row['C0'], row['C1'], abs(row['mass_drive_error']), row['mass_endpoint_projection_error'], row['P1_endpoint']) < 1e-10
                summaries.append(row)
                check(branch + '_' + surface + '_joint_data_prepared', max(row['C0'], abs(row['raw_mass_drive_error']), abs(result['residual'][-1])) < 1e-10, row)
                for key in ['C1', 'rho', 'p_first', 'Ward_error', 'boundary_work', 'source_work']:
                    archive[surface + '__' + key] = energy[key]
                for key in ['P_coeff', 'mu_coeff', 'P_nodes', 'mu_nodes', 'raw_nodes', 'projection_work', 'metric_work', 'residual']:
                    archive[surface + '__' + key] = result[key]
                archive[surface + '__' + 'regenerated_family_defect'] = defect
            record = report['cases'][-1]
            record.update({'Newton_history': history, 'results': summaries, 'state_changed_and_all_four_rates_regenerated': True, 'momentum_change_from_previous': float(abs(candidate['momentum'] - baseline['momentum']).max())})
            path = destination / (branch + '_moment_candidate.npz')
            np.savez_compressed(path, **archive)
            own(path, 'outputs')
            path = destination / (branch + '_frozen_extended_frames.npz')
            np.savez_compressed(path, **{surface + '__' + kind: array for surface, maps in frames.items() for kind, array in maps.items()})
            own(path, 'outputs')
            save()
            print(json.dumps(record), flush=True)
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

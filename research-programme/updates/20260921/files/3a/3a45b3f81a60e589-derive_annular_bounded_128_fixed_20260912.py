import argparse
import gc
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
    from scipy.linalg import solve
    from annular_canonical_bounded_128_20260912 import CommonProfile, RefinedContext, RefinedPreparation, RefinedFields
    from annular_canonical_rate_completion_20260911 import evaluate_initial
    from annular_canonical_trace_projection_stable_20260911 import kernel_family, gram_density_control

    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', required=True)
    arguments = parser.parse_args()
    if not arguments.attempt.isalnum():
        raise ValueError('Fresh alphanumeric attempt required.')
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    destination = intake / ('annular-bounded-N128-' + arguments.attempt)
    destination.mkdir(parents=True, exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'cases': [], 'comparisons': [], 'matched_branch_comparisons': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'protocol': 'Bounded N128 only, compared with sealed N64; shared prepared N16 MTS chi and auxiliary momentum profile, shared original coarse kinetic map at every mesh, shared inner mass/drives/clock/lapse shape. Each GR or Gram branch solves dependent mass and exactly two global cubic boundary amplitudes. No separately fitted fine archive; zeros for unused construction-only legacy momentum covectors. This matched-profile GR branch is not the earlier smooth manufactured GR reference.'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None, fatal=True):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if fatal and not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    def archive(name, arrays):
        path = destination / (name + '.npz')
        if path.exists():
            raise FileExistsError(path)
        numerical.savez_compressed(path, **arrays)
        with numerical.load(path, allow_pickle=False) as saved:
            check(name + '_finite_roundtrip', set(saved.files) == set(arrays) and all(numerical.isfinite(value).all() and numerical.array_equal(value, saved[key]) for key, value in arrays.items()))
        own(path, 'outputs')

    save()
    try:
        prior_path = intake / 'annular-common-profile-refinement-final-integrity.json'
        own(prior_path)
        previous = json.loads(prior_path.read_text())
        check('prior_seal_complete', previous['state'] == 'complete')
        for table in ['inputs', 'outputs']:
            for name, expected in previous[table].items():
                if digest(root / name) != expected:
                    raise RuntimeError('Prior evidence changed: ' + name)
                report['inputs'][name] = expected
        for name in ['annular_canonical_bounded_128_20260912.py', 'annular_inherited_knot_link_quadrature_20260912.py', Path(__file__).name]:
            path = root / 'scripts' / name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            snapshot = destination / ('executed-' + name)
            snapshot.write_bytes(path.read_bytes())
            own(snapshot, 'outputs')
        common = CommonProfile(root)
        own(common.prepared_path)
        surveys, last_success = {}, {'metric_Gram': 64, 'GR': 64}
        for branch in ['metric_Gram', 'GR']:
            path = intake / 'annular-common-profile-refinement-attempt02' / ('N64_' + branch + '_survey.npz')
            own(path)
            with numerical.load(path, allow_pickle=False) as saved_lower:
                surveys[(64, branch)] = {key: saved_lower[key].copy() for key in saved_lower.files}
        for intervals in [128]:
            for branch in ['metric_Gram', 'GR']:
                label = 'N' + str(intervals) + '_' + branch
                record = {'label': label, 'intervals': intervals, 'branch': branch, 'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat()}
                report['cases'].append(record)
                if intervals > 16 and last_success.get(branch) != intervals // 2:
                    record.update({'state': 'not_run', 'reason': 'Previous spatial construction for this branch did not complete; no blind refinement.'})
                    save()
                    continue
                print('Starting ' + label + ' at ' + record['started_utc'], flush=True)
                save()
                try:
                    context = RefinedContext(common, intervals, branch)
                    survey_points = context.surfaces['survey']
                    sampled = RefinedFields(context, context.saved).evaluate(survey_points)
                    original = common.physical_free(survey_points)
                    transfer_errors = {key: float(abs(sampled[key] - original[key]).max()) for key in ['chi', 'w', 'w_r', 'pi', 'pi_r']}
                    shape = context.old_frames['mass']['quad']['q'].shape[1]
                    record['transfer_errors_before_boundary_preparation'] = transfer_errors
                    record['original_mass_phase_dimension'] = shape
                    check(label + '_same_physical_free_profiles', max(transfer_errors.values()) < 1e-8, transfer_errors)
                    check(label + '_same_external_boundary_data', numerical.array_equal(context.saved['boundary_velocity'], common.prepared['boundary_velocity']) and context.saved['mass_coefficients'][0] == common.prepared['mass_coefficients'][0])
                    prep = RefinedPreparation(context)
                    amplitudes, prepared, history = prep.solve()
                    actual, frames, data = prepared['actual'], prepared['frames'], prepared['data']
                    higher = evaluate_initial(frames['mass'], frames['scalar'], data, context.basis, context.check_weights, context.check_links, context.include_gram, context.system.outer_clock, surface='check', link_surface='links_check')
                    family, primitive, unused_carrier = kernel_family(context, data, frames['mass'], actual['P_rate_coeff'])
                    record.update({'amplitudes': amplitudes.tolist(), 'history': history, 'function_calls': prep.calls, 'completion': prepared['completion'], 'trace_extension': prepared['extension'], 'outcomes': {}})
                    for variant, result in [('primary', actual), ('higher', higher)]:
                        surface = 'check' if variant == 'higher' else 'quad'
                        weights = context.check_weights if variant == 'higher' else context.weights
                        eta_mass = data[surface]['eta'].T @ (weights[:, None] * data[surface]['eta'])
                        nodes = data['nodes']
                        parent_flux = .1 * nodes['N'][[0, -1]] * nodes['F'][[0, -1]]**1.5 * nodes['pi'][[0, -1]] * nodes['w'][[0, -1]]
                        parent_flux += numerical.array([1., -1.]) * .1 * numerical.sqrt(nodes['F'][[0, -1]]) * result['q_nodes'][[0, -1]] * result['gram_scalar'][[0, -1]] / nodes['N'][[0, -1]]
                        record['outcomes'][variant] = {'C_max': float(abs(result['constraint']).max()), 'Cdot_max': float(abs(result['constraint_rate']).max()), 'C_dual_L2': float(numerical.sqrt(max(0., result['constraint'] @ solve(eta_mass, result['constraint'])))), 'Cdot_dual_L2': float(numerical.sqrt(max(0., result['constraint_rate'] @ solve(eta_mass, result['constraint_rate'])))), 'mass_trace_gaps': (result['mu_t_nodes'][[0, -1]] - parent_flux).tolist(), 'mass_drive_gap': float(result['mu_t_nodes'][0] - context.saved['boundary_velocity'][0]), 'outer_scalar_drive_gap': float(result['q_nodes'][-1] - context.saved['boundary_velocity'][2]), 'clock_gap': float(nodes['N'][-1] / numerical.sqrt(nodes['F'][-1]) - context.system.outer_clock), 'minimum_sampled_F': float(min(values['F'].min() for values in data.values())), 'minimum_sampled_N': float(min(values['N'].min() for values in data.values())), 'time_link_log_max': float(abs(result['endpoint_log']).max())}
                        archive(label + '_' + variant, {key: value for key, value in result.items() if isinstance(value, numerical.ndarray)})
                    if context.include_gram:
                        unused_coefficients, unused_density, controls = gram_density_control(context, data, actual, family, primitive)
                        record['kernel_controls'] = controls
                    survey = {key: value.copy() for key, value in data['survey'].items() if key not in ['eta', 'eta_r']}
                    survey.update({'mu_t': frames['mass']['survey']['q'] @ actual['mass_rate_coeff'], 'mu_tr': frames['mass']['survey']['qr'] @ actual['mass_rate_coeff'], 'P_t': frames['mass']['survey']['p'] @ actual['P_rate_coeff'], 'q': frames['scalar']['survey']['q'] @ actual['q_coeff'], 'q_r': frames['scalar']['survey']['qr'] @ actual['q_coeff'], 'pi_t': frames['scalar']['survey']['p'] @ actual['pi_rate_coeff'], 'weights': context.survey_weights})
                    record['survey_norms'] = {key + '_L2': float(numerical.sqrt(survey['weights'] @ survey[key]**2)) for key in ['mu', 'mu_r', 'pi', 'pi_r', 'N', 'mu_t', 'mu_tr', 'P_t', 'q', 'q_r', 'pi_t']}
                    record['survey_pi_total_variation'] = float(abs(numerical.diff(survey['pi'])).sum())
                    record['Gram_base_quadratic_form'] = float(numerical.sum(context.basis.radii**2 * data['nodes']['N'] * numerical.sqrt(data['nodes']['F']) * prep.gram_density))
                    archive(label + '_survey', survey)
                    archive(label + '_initial_data', {**prepared['saved'], 'amplitudes': amplitudes, 'radii': context.basis.radii, 'faces': context.basis.faces, 'frozen_seed_packed': context.model.packed, 'canonical_common_weight_owner': numerical.array(16)})
                    if (intervals // 2, branch) in surveys:
                        lower = surveys[(intervals // 2, branch)]
                        differences = {key: float(numerical.sqrt(survey['weights'] @ (survey[key] - lower[key])**2)) for key in ['mu', 'mu_r', 'pi', 'pi_r', 'N', 'mu_t', 'mu_tr', 'P_t', 'q', 'q_r', 'pi_t']}
                        report['comparisons'].append({'branch': branch, 'coarse': intervals // 2, 'fine': intervals, 'physical_L2_differences': differences})
                    surveys[(intervals, branch)] = survey
                    diagnostic = prepared['extension']
                    numerical_gate = all(max(outcome['C_max'], outcome['Cdot_max'], abs(outcome['mass_drive_gap']), abs(outcome['outer_scalar_drive_gap']), abs(outcome['clock_gap'])) < 1e-10 for outcome in record['outcomes'].values())
                    record['finite_initial_identity_gate'] = numerical_gate
                    check(label + '_full_rows_and_boundary_gates', numerical_gate, record['outcomes'], fatal=False)
                    check(label + '_canonical_full_kernel_family', diagnostic['parent_family_dimension'] == intervals and diagnostic['no_parent_family_modes_discarded'] and diagnostic['all_kernel_family_trace_error'] < 1e-10 and diagnostic['block_pairing_error'] < 1e-8, diagnostic, fatal=False)
                    if intervals == 16 and branch == 'metric_Gram':
                        baseline_path = root / 'source-intake/navier-stokes/20260911/annular-canonical-trace-boundary-control-attempt01/MTS_prepared_first_jet.npz'
                        with numerical.load(baseline_path, allow_pickle=False) as old:
                            replay = {key: float(abs(actual[key] - old[key]).max()) for key in ['constraint', 'constraint_rate', 'mu_t_nodes', 'q_nodes']}
                        record['prior_N16_prepared_replay'] = replay
                        check('N16_reproduces_prior_prepared_physics', max(replay.values()) < 1e-10, replay)
                    record.update({'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat()})
                    last_success[branch] = intervals
                    print(json.dumps({'label': label, 'gate': numerical_gate, 'amplitudes': amplitudes.tolist(), 'outcomes': record['outcomes'], 'norms': record['survey_norms']}), flush=True)
                    del prepared, frames, data, context, prep, actual, higher
                    gc.collect()
                except Exception as error:
                    record.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
                    print(label + ' FAILED: ' + repr(error), flush=True)
                save()
            if (intervals, 'GR') in surveys and (intervals, 'metric_Gram') in surveys:
                reference, mts = surveys[(intervals, 'GR')], surveys[(intervals, 'metric_Gram')]
                report['matched_branch_comparisons'].append({'intervals': intervals, 'MTS_minus_matched_GR_L2': {key: float(numerical.sqrt(mts['weights'] @ (mts[key] - reference[key])**2)) for key in ['mu', 'pi', 'N', 'mu_t', 'P_t', 'q', 'pi_t']}})
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete' if all(row['state'] == 'complete' for row in report['cases']) and all(row['passed'] for row in report['checks']) else 'complete_with_failures'
        report['completed_utc'] = datetime.now(timezone.utc).isoformat()
        save()
        print(json.dumps({'state': report['state'], 'cases': [{key: value for key, value in row.items() if key in ['label', 'state', 'error', 'finite_initial_identity_gate']} for row in report['cases']], 'comparisons': report['comparisons'], 'matched_branch_comparisons': report['matched_branch_comparisons']}), flush=True)
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        save()
        raise


if __name__ == '__main__':
    run()

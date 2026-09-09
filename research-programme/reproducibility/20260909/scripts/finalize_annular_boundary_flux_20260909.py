import argparse
import hashlib
import json
import re
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis, linear_value_gradient, real_linear
    from annular_action_boundary_current_20260909 import boundary_balance, gram_current
    from annular_boundary_ramp_bound_20260909 import affine_link_bound
    from annular_local_ward_identity_20260909 import LocalWardIdentity
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['analyze', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-boundary-affine-ramp-analysis'
    target = intake / 'annular-boundary-current-final-integrity.json'
    inputs, outputs, owners = {}, {}, []

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path):
        inputs[str(path.relative_to(root))] = digest(path)

    def artifact(path):
        outputs[str(path.relative_to(root))] = digest(path)

    def inherit(table, inherited):
        for relative, expected in inherited.items():
            actual = digest(root / relative)
            if actual != expected or relative in table and table[relative] != actual:
                raise RuntimeError('Changed source/result: ' + relative)
            table[relative] = actual

    def loaded(path):
        own(path)
        with numerical.load(path) as handle:
            return {name: handle[name].copy() for name in handle.files}

    def maximum(value):
        return float(numerical.max(numerical.abs(value)))

    for name in ['annular-action-boundary-current-derived', 'annular-boundary-N64-evolution-smoke']:
        path = intake / name / 'status.json'
        owner = json.loads(path.read_text())
        if owner['state'] != 'complete' or owner['passed'] != owner['total'] or not (path.parent / 'COMPLETE').exists():
            raise RuntimeError('Incomplete owner: ' + name)
        owners.append({'owner': name, **{key: owner[key] for key in ['state', 'passed', 'total', 'completed_utc']}})
        inherit(inputs, owner['inputs'])
        inherit(outputs, owner['outputs'])
        for extra in [path, path.parent / 'COMPLETE', path.parent / 'executed-script.py']:
            own(extra)
    scripts = ['annular_action_boundary_current_20260909.py', 'derive_annular_action_boundary_current_20260909.py', 'evolve_annular_boundary_N64_20260909.py', 'annular_boundary_ramp_bound_20260909.py', 'finalize_annular_boundary_flux_20260909.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if arguments.phase == 'analyze':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'trajectories': [], 'ramp_samples': [], 'valid_for_physics_claim': False, 'scope': 'Postprocess immutable released-slope trajectories; derive affine Ward endpoint balance and a positive-chart piecewise-smooth interpolation bound. No integration, refit, boundary subtraction or physical-claim promotion.'}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                save()
                raise RuntimeError('Validation failed: ' + name + ' ' + repr(detail))

        class CurrentWard(LocalWardIdentity):
            def connection_transport(self):
                system, packed = self.system, self.arrays['corrected']
                return system.links.matrix(packed[system.slices[0]], packed[system.slices[1]], system.constants)

        def check_interpolation(system, packed, pair_current, label):
            bound = affine_link_bound(system, packed, pair_current)
            basis, links = system.basis, system.links
            mass, lapse = packed[system.slices[0]], packed[system.slices[1]]
            gamma = 1 / links.inverse_clock(mass, lapse, system.constants)[0]
            gamma_face = -bound['affine_shift_generator'] * (basis.radii[-1] - basis.radii[0])
            interpolated = real_linear(links.face_value, gamma_face)
            cell = numerical.clip(numerical.searchsorted(basis.faces, links.points, side='right') - 1, 0, basis.faces.size - 2)
            direct_error = links.integrate(1 - interpolated / gamma) / (basis.radii[-1] - basis.radii[0])
            check(label + '_independent_affine_link_integrand', maximum(direct_error - bound['link_error']) < 1e-13)
            check(label + '_positive_gamma_lower_bound', numerical.all(gamma + 1e-13 >= bound['cell_gamma_lower_bound'][cell]))
            check(label + '_pointwise_interpolation_bound', numerical.all(numerical.abs(gamma - interpolated) <= bound['cell_gamma_interpolation_bound'][cell] + 1e-13))
            check(label + '_all_link_integrals_bounded', numerical.all(numerical.abs(bound['link_error']) <= bound['link_error_bound'] + 1e-13))
            check(label + '_weighted_current_remainder_bounded', abs(float(bound['Gram_affine_link_remainder'])) <= float(bound['Gram_affine_link_remainder_bound']) + 1e-13 * numerical.sum(numerical.abs(pair_current)))
            return bound

        save()
        try:
            for case_name in ['canonical', 'nonlinear_modulated']:
                case_path = intake / 'annular-constraint-correction-initial' / (case_name + '.json')
                own(case_path)
                case = json.loads(case_path.read_text())
                constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
                kappa = float(symbolic.sympify(case['normalization_kappa']))
                for intervals in [16, 32, 64]:
                    for branch in ['GR', 'metric_Gram']:
                        tag = case_name + '_N' + str(intervals) + '_' + branch
                        report['active_job'] = tag
                        save()
                        source = loaded(intake / 'annular-released-Hermite-initial-derived' / (tag + '.npz'))
                        folder = intake / ('annular-boundary-N64-evolution-smoke' if intervals == 64 else 'annular-released-Hermite-evolution-smoke')
                        steps = 64 if intervals == 64 else 32
                        trajectory = loaded(folder / (tag + '_steps' + str(steps) + '.npz'))
                        basis = MixedActionBasis(source['radius'])
                        links = MetricLinkQuadrature(basis)
                        node_count = basis.radii.size
                        length = basis.radii[-1] - basis.radii[0]
                        affine_node = (basis.radii - basis.radii[0]) / length
                        affine_face = (basis.faces - basis.radii[0]) / length
                        parameters = numerical.concatenate([affine_node, numerical.full(node_count, basis.spacing / length)])
                        include_gram = branch != 'GR'
                        records = {name: [] for name in ['time', 'offset', 'flux', 'clocks', 'identity_error']}
                        indices = range(0, steps + 1, steps // 32)
                        for index in indices:
                            time, state = trajectory['time'][index], trajectory['state'][index]
                            scalar, slope, momentum, slope_momentum = [state[part * node_count:(part + 1) * node_count] for part in range(4)]
                            packed = state[4 * node_count:]
                            system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, momentum, slope_momentum, source['outer_clock'][0] + time * source['outer_clock'][1], links)
                            tangent = system.constraint_tangent(packed, include_gram, source['endpoint_acceleration'], source['outer_clock'][1])
                            balance = boundary_balance(system, packed, tangent, include_gram, source['outer_clock'][1])
                            check(tag + '_sample' + str(index) + '_same_unmodified_shift_residual', maximum(tangent['shift_residual'] - trajectory['shifts'][index]) < 2e-12)
                            for name, value in [('time', time), ('offset', balance['local_boundary_balance']), ('flux', balance['reaction_flux_positive_R']), ('clocks', balance['variational_boundary_clocks']), ('identity_error', balance['global_boundary_identity_error'])]:
                                records[name].append(value)
                            if intervals == 64:
                                check(tag + '_sample' + str(index) + '_same_saved_boundary_offset', maximum(balance['local_boundary_balance'] - trajectory['boundary_offset'][index]) < 1e-13)
                            if index not in [0, steps // 2, steps]:
                                continue
                            unused_value, gradient, hessian = system.evaluate(packed, include_gram)
                            arrays = dict(source, scalar=scalar, corrected=packed, defect=slope / basis.spacing, defect_time=packed[system.slope_slice] / basis.spacing, defect_acceleration=tangent['packed_speed'][system.slope_slice] / basis.spacing, gradient_final=gradient, Hessian_final=hessian, **tangent)
                            ward = CurrentWard(system, arrays).evaluate(include_gram)
                            saved_path = folder / (tag + ('_sample' if intervals == 64 else '_Ward') + str(index) + '.npz')
                            saved = loaded(saved_path)
                            prefix = 'Ward_' if intervals == 64 else ''
                            check(tag + '_ramp' + str(index) + '_same_independent_saved_Ward', maximum(ward['predicted_shift_work'] - saved[prefix + 'predicted_shift_work']) < 2e-12)
                            shift_generator = real_linear(ward['shift_generator'], parameters)
                            velocity = packed[system.slices[2]]
                            free_remainder = numerical.dot(affine_node[1:-1] * velocity[1:-1], balance['scalar_Euler'][1:-1])
                            free_remainder += numerical.dot(affine_face[1:] * tangent['packed_speed'][system.slices[0]][1:], gradient[system.slices[0]][1:])
                            terms = {name: float(sign * numerical.dot(parameters, ward[name])) for name, sign in [('bulk_remainder', 1), ('Gram_coefficient_remainder', -1), ('Gram_link_remainder', -1), ('lifting_work', -1), ('lapse_constraint_derivative_work', -1)]}
                            terms['shift_work'] = float(-numerical.dot(shift_generator, tangent['shift_residual']))
                            terms['free_scalar_mass_work'] = float(-free_remainder)
                            reconstructed = sum(terms.values())
                            error = abs(reconstructed - balance['local_boundary_balance'][-1])
                            check(tag + '_ramp' + str(index) + '_exact_outer_offset_without_fitting', error < 2e-12, float(error))
                            bound_arrays = {}
                            if include_gram:
                                current = gram_current(system, packed, tangent)
                                bound = check_interpolation(system, packed, current['pair_current'], tag + '_ramp' + str(index))
                                check(tag + '_ramp' + str(index) + '_same_affine_Gram_Ward_term', abs(float(bound['Gram_affine_link_remainder']) + terms['Gram_link_remainder']) < 1e-13)
                                check(tag + '_ramp' + str(index) + '_same_shift_generator', maximum(shift_generator - bound['affine_shift_generator']) < 1e-12)
                                bound_arrays = {'bound_' + name: value for name, value in bound.items()}
                            triangle = sum(abs(value) for value in terms.values())
                            separated = triangle - abs(terms['shift_work']) + numerical.dot(numerical.abs(shift_generator), numerical.abs(tangent['shift_residual']))
                            if include_gram:
                                separated += float(bound['Gram_affine_link_remainder_bound']) - abs(terms['Gram_link_remainder'])
                            check(tag + '_ramp' + str(index) + '_finite_outer_offset_triangle_bound', abs(balance['local_boundary_balance'][-1]) <= separated + 2e-12)
                            path = destination / (tag + '_sample' + str(index) + '.npz')
                            numerical.savez_compressed(path, ramp_parameters=parameters, shift_generator=shift_generator, local_boundary_balance=balance['local_boundary_balance'], independent_free_remainder=free_remainder, reconstructed_outer_offset=reconstructed, **{'term_' + name: value for name, value in terms.items()}, **bound_arrays)
                            artifact(path)
                            report['ramp_samples'].append({'case': case_name, 'intervals': intervals, 'branch': branch, 'time': float(time), 'offset': balance['local_boundary_balance'].tolist(), 'reconstruction_error': float(error), 'signed_terms': terms, 'triangle_bound': float(triangle), 'absolute_shift_and_link_bound': float(separated), 'Gram_affine_link_remainder_bound': float(bound['Gram_affine_link_remainder_bound']) if include_gram else 0.0, 'maximum_link_error': maximum(bound['link_error']) if include_gram else 0.0, 'maximum_link_error_bound': maximum(bound['link_error_bound']) if include_gram else 0.0})
                            if case_name == 'canonical' and intervals == 16 and branch == 'metric_Gram' and index == 0:
                                manufactured = packed.copy()
                                manufactured[system.slices[0]] = 0
                                manufactured[system.slices[1]] = 1 + 0.1 * numerical.abs(basis.radii - basis.radii[node_count // 2])
                                manufactured_bound = check_interpolation(system, manufactured, numerical.ones(links.node.size), tag + '_manufactured_lapse_kink')
                                check(tag + '_manufactured_kink_is_nontrivial', maximum(manufactured_bound['link_error']) > 1e-8)
                                path = destination / 'manufactured-positive-lapse-kink.npz'
                                numerical.savez_compressed(path, packed=manufactured, **manufactured_bound)
                                artifact(path)
                                invalid = packed.copy()
                                invalid[system.slices[1]] = 0
                                rejected = False
                                try:
                                    affine_link_bound(system, invalid, numerical.ones(links.node.size))
                                except ValueError:
                                    rejected = True
                                check(tag + '_zero_lapse_chart_rejected', rejected)
                        values = {name: numerical.asarray(value) for name, value in records.items()}
                        check(tag + '_33_common_times_and_two_unsubtracted_endpoints', values['offset'].shape == (33, 2) and numerical.allclose(values['time'], numerical.linspace(0, .01, 33), atol=1e-16, rtol=0))
                        check(tag + '_global_boundary_identity_all_common_times', maximum(values['identity_error']) < 2e-12)
                        path = destination / (tag + '_boundary_timeseries.npz')
                        numerical.savez_compressed(path, **values)
                        artifact(path)
                        row = {'case': case_name, 'intervals': intervals, 'branch': branch, 'maximum_boundary_offset': maximum(values['offset']), 'final_boundary_offset': values['offset'][-1].tolist(), 'maximum_global_boundary_identity_error': maximum(values['identity_error'])}
                        report['trajectories'].append(row)
                        save()
                        print(json.dumps(row), flush=True)
            for module in tuple(sys.modules.values()):
                filename = getattr(module, '__file__', None)
                if filename:
                    path = Path(filename).resolve()
                    if path.parent == root / 'scripts' and path.suffix == '.py':
                        own(path)
            check('all_owned_sources_unchanged_at_analysis_end', all(digest(root / name) == expected for name, expected in inputs.items()))
            check('all_owned_outputs_unchanged_at_analysis_end', all(digest(root / name) == expected for name, expected in outputs.items()))
            check('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
            report.update(state='complete', passed=sum(row['passed'] for row in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
            save()
            (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')
            print(json.dumps({key: report[key] for key in ['state', 'passed', 'total', 'completed_utc']}), flush=True)
            return
        except Exception as error:
            report.update(state='failed', failure=repr(error), traceback=traceback.format_exc(), completed_utc=datetime.now(timezone.utc).isoformat())
            save()
            raise
    if target.exists():
        raise FileExistsError('Final evidence already exists.')
    analysis_path = destination / 'status.json'
    analysis = json.loads(analysis_path.read_text())
    if analysis['state'] != 'complete' or analysis['passed'] != analysis['total'] or not (destination / 'COMPLETE').exists():
        raise RuntimeError('Analysis gate is incomplete.')
    inherit(inputs, analysis['inputs'])
    inherit(outputs, analysis['outputs'])
    for extra in [analysis_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(extra)
    note = root / 'DERIVATION-20260909-boundary-current-and-N64-spatial-control.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != target and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-boundary-current-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 15, 27, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected-file or cache check failed: ' + repr(touched))
    report = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'owners': owners, 'owner_check_count': sum(row['total'] for row in owners), 'analysis_check_count': analysis['total'], 'compiled_scripts': len(scripts), 'unique_input_hashes': len(inputs), 'output_hashes': len(outputs), 'inputs': inputs, 'outputs': outputs, 'boundary_time_samples': 33 * len(analysis['trajectories']), 'affine_ramp_samples': len(analysis['ramp_samples']), 'maximum_ramp_reconstruction_error': max(row['reconstruction_error'] for row in analysis['ramp_samples']), 'cited_local_paths_checked': cited, 'mutable_resume_pinned_as_snapshot_only': True, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T15:27:00Z, not a pre-turn full hash comparison; all tool writes scoped to post-checkpoint-work', 'no_bytecode_cache': True, 'boundary_current_and_energy_identity_derived': True, 'affine_positive_chart_link_bound_derived': True, 'both_endpoint_offsets_zero': False, 'full_coupled_DAE_solved': False, 'mesh_uniform_stability_proved': False, 'valid_for_physics_claim': False}
    with target.open('x') as handle:
        json.dump(report, handle, indent=2)
        handle.write('\n')
    print(json.dumps({key: report[key] for key in ['state', 'completed_utc', 'owner_check_count', 'analysis_check_count', 'affine_ramp_samples', 'boundary_time_samples', 'compiled_scripts', 'unique_input_hashes', 'output_hashes', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()

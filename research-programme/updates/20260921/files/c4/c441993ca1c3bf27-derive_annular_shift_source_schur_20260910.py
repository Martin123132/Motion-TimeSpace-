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
    import scipy
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_gram_joint_action_20260909 import gram_matrices
    from annular_parent_root_residence_20260910 import canonical_maps
    from annular_parent_coefficient_box_20260910 import Box
    from annular_shift_source_schur_20260910 import CHANNELS, matrix_solve, source_decomposition

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    parser.add_argument('--attempt', default='attempt01')
    parser.add_argument('--limit', type=int, default=0)
    arguments = parser.parse_args()
    if not re.fullmatch('[a-z0-9-]+', arguments.attempt) or arguments.limit < 0:
        raise ValueError('Invalid attempt/limit.')
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260910'
    destination = intake / ('annular-shift-source-schur-' + arguments.attempt)
    prior_path = intake / 'annular-implicit-parent-jets-final-integrity.json'
    root_path = intake / 'annular-parent-root-residence-attempt02/status.json'
    jets_path = intake / 'annular-implicit-parent-jets-attempt01/status.json'
    final_path = intake / 'annular-shift-source-schur-final-integrity.json'
    scripts = ['annular_shift_source_schur_20260910.py', 'derive_annular_shift_source_schur_20260910.py']
    inputs, outputs = {}, {}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path):
        inputs[str(path.relative_to(root))] = digest(path)

    def artifact(path):
        outputs[str(path.relative_to(root))] = digest(path)

    def inherit(table, inherited):
        for name, expected in inherited.items():
            actual = digest(root / name)
            if actual != expected or name in table and table[name] != actual:
                raise RuntimeError('Changed evidence: ' + name)
            table[name] = actual

    def loaded(path):
        own(path)
        with numerical.load(path) as handle:
            return {name: handle[name].copy() for name in handle.files}

    def size_bounds(value):
        return {'lower': float(numerical.maximum(0., numerical.maximum(value.lo, -value.hi)).max()), 'upper': float(value.magnitude.max())}

    def contains_zero(value):
        return numerical.all(value.lo <= 0) and numerical.all(value.hi >= 0)

    prior = json.loads(prior_path.read_text())
    if prior['state'] != 'complete':
        raise RuntimeError('Preceding exact-root shift-defect gate incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    for path in [prior_path, root_path, jets_path]:
        own(path)
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
        own(path)
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        for name in scripts:
            path = destination / ('executed-' + name)
            path.write_bytes((root / 'scripts' / name).read_bytes())
            artifact(path)
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'probe_limit': arguments.limit, 'channels': CHANNELS, 'runtime': {'python': sys.version, 'numpy': numerical.__version__, 'scipy': scipy.__version__}, 'original_states_unchanged': True, 'new_numerical_evolution': False, 'observed_tangent_used_to_build_sources': False, 'action_modified': False, 'all_shift_equations_verified': False, 'continuum_convergence_proved': False, 'valid_for_physics_claim': False, 'scope': 'Independent static-data variational source decomposition and verified Schur response at existing exact free-root enclosures. Channel partition is defined at the same background and full operator; not a unique causal attribution or corrected theory.'}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        save()
        try:
            reference = numerical.array([[1., -2., 3.], [4., 5., -6.]])
            control, diagnostic = matrix_solve(Box(numerical.array([[2., 1.], [1., 3.]])), Box(numerical.array([[2., 1.], [1., 3.]])) @ Box(reference))
            check('matrix_multiple_rhs_control', numerical.all(control.lo <= reference) and numerical.all(control.hi >= reference) and diagnostic['componentwise_majorant_verified'])
            try:
                matrix_solve(Box(numerical.array([[1., 1.], [1., 1.]])), Box(numerical.ones((2, 2))))
            except (ValueError, numerical.linalg.LinAlgError):
                rejected = True
            else:
                rejected = False
            check('singular_matrix_rejected', rejected)
            case_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
            own(case_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            samples = json.loads(root_path.read_text())['samples']
            if arguments.limit:
                samples = samples[:arguments.limit]
            for sample in samples:
                label, branch = sample['label'], sample['branch']
                report['active_sample'] = label
                save()
                print('Starting ' + label, flush=True)
                archived = loaded(root_path.parent / (label + '.npz'))
                basis = MixedActionBasis(archived['basis_radii'])
                links = MetricLinkQuadrature(basis)
                count = basis.radii.size
                configuration, momenta = archived['original_configuration'], archived['original_momenta']
                clock, clock_rate = archived['affine_clock']
                system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], clock, links)
                exact_maps = True
                for name, value in archived.items():
                    if name.startswith('basis_'):
                        exact_maps = exact_maps and numerical.array_equal(value, numerical.asarray(getattr(basis, name[6:])))
                    if name.startswith('links_'):
                        exact_maps = exact_maps and numerical.array_equal(value, getattr(links, name[6:]))
                value_map, gradient_map = canonical_maps(basis)
                factors, sampling = gram_matrices(count)
                exact_maps = exact_maps and all(numerical.array_equal(archived[name], value) for name, value in [('assembly_value_map', value_map), ('assembly_gradient_map', gradient_map), ('local_action_maps', numerical.stack(system.maps)), ('nodal_action_maps', numerical.stack(system.node_maps)), ('gram_factors', factors), ('gram_sampling', sampling)])
                check(label + '_all_archived_maps_reused_exactly', exact_maps)
                packed = Box(archived['initial_root_box_lower'], archived['initial_root_box_upper'])
                data = source_decomposition(system, packed, Box(configuration), Box(momenta), Box(clock), clock_rate, archived['endpoint_acceleration'], branch != 'GR')
                observed = loaded(jets_path.parent / (label + '.npz'))
                old_shift = Box(observed['initial_shift_defect_lower'], observed['initial_shift_defect_upper'])
                old_mismatch = Box(observed['initial_mass_velocity_mismatch_lower'], observed['initial_mass_velocity_mismatch_upper'])
                for name, diagnostic in data['diagnostics'].items():
                    check(label + '_' + name + '_verified_inverse', diagnostic['componentwise_majorant_verified'] and diagnostic['contraction'] < 1)
                check(label + '_positive_chart', data['minimum_F'] > 0 and data['minimum_N'] > 0)
                check(label + '_independent_source_sum_identity', contains_zero(data['assembly_difference']))
                check(label + '_old_shift_and_sourced_shift_overlap', numerical.all(data['source_shift_defect'].lo <= old_shift.hi) and numerical.all(old_shift.lo <= data['source_shift_defect'].hi))
                check(label + '_old_mass_and_sourced_mass_overlap', numerical.all(data['source_mass_mismatch'].lo <= old_mismatch.hi) and numerical.all(old_mismatch.lo <= data['source_mass_mismatch'].hi))
                shift_difference = float(abs(data['source_shift_defect'].midpoint - old_shift.midpoint).max())
                check(label + '_independent_shift_midpoint_agreement', shift_difference < 1e-11, shift_difference)
                check(label + '_inner_mass_mismatch_preserved_zero', data['source_mass_mismatch'].magnitude[0] == 0)
                check(label + '_direct_plus_projection_response_identity', contains_zero(data['shift_channels'] - data['direct_shift_channels'] - data['projection_shift_channels']))
                check(label + '_projection_Gram_symmetry', contains_zero(data['projection_gram'] - data['projection_gram'].T))
                check(label + '_necessary_boundary_rows_solved', contains_zero(data['boundary_repaired_obstruction'][[0, count - 1]]))
                if branch == 'GR':
                    check(label + '_Gram_input_channels_exactly_absent', numerical.all(data['sources'].magnitude[:, [1, 2]] == 0))
                    check(label + '_Gram_response_channels_exactly_absent', numerical.all(data['shift_channels'].magnitude[:, [1, 2]] == 0))
                ones = Box(numerical.ones(len(CHANNELS)))
                total_direct = data['direct_shift_channels'] @ ones
                total_projection = data['projection_shift_channels'] @ ones
                direct_obstruction = data['direct_obstruction_channels'] @ ones
                projection_obstruction = data['projection_obstruction_channels'] @ ones
                obstruction = data['obstruction_channels'] @ ones
                rows = []
                for column, name in enumerate(CHANNELS):
                    rows.append({'name': name, 'raw_source': size_bounds(data['sources'][:, column]), 'obstruction': size_bounds(data['obstruction_channels'][:, column]), 'shift_response': size_bounds(data['shift_channels'][:, column])})
                arrays = {}
                for name, value in data.items():
                    if isinstance(value, Box):
                        arrays[name + '_lower'], arrays[name + '_upper'] = value.lo, value.hi
                output = destination / (label + '.npz')
                numerical.savez_compressed(output, **arrays)
                with numerical.load(output) as saved:
                    check(label + '_archive_roundtrip_exact', set(saved.files) == set(arrays) and all(numerical.array_equal(saved[name], value) for name, value in arrays.items()))
                artifact(output)
                row = {'label': label, 'intervals': sample['intervals'], 'branch': branch, 'saved_time': sample['saved_time'], 'channels': rows, 'source_predicted_shift': size_bounds(data['source_shift_defect']), 'observed_shift': size_bounds(old_shift), 'independent_shift_midpoint_difference': shift_difference, 'direct_lapse_obstruction': size_bounds(direct_obstruction), 'projection_lapse_obstruction': size_bounds(projection_obstruction), 'total_lapse_obstruction': size_bounds(obstruction), 'direct_shift_response': size_bounds(total_direct), 'projection_shift_response': size_bounds(total_projection), 'diagnostics': data['diagnostics'], 'all_shift_equations_verified': False, 'continuum_convergence_proved': False}
                row.update(original_endpoint_acceleration=archived['endpoint_acceleration'].tolist(), required_endpoint_acceleration_lower=data['required_boundary_acceleration'].lo.tolist(), required_endpoint_acceleration_upper=data['required_boundary_acceleration'].hi.tolist(), boundary_repaired_interior_obstruction=size_bounds(data['boundary_repaired_obstruction'][1:-1]), boundary_repaired_shift=size_bounds(data['boundary_repaired_shift']), endpoint_acceleration_only_repair_rejected=size_bounds(data['boundary_repaired_obstruction'][1:-1])['lower'] > 0, boundary_trial_is_static_only=True)
                report['samples'].append(row)
                save()
                print(json.dumps({'label': label, 'predicted_shift': row['source_predicted_shift'], 'direct_obstruction': row['direct_lapse_obstruction'], 'projection_obstruction': row['projection_lapse_obstruction'], 'boundary_only_repair_rejected': row['endpoint_acceleration_only_repair_rejected'], 'boundary_trial_shift': row['boundary_repaired_shift'], 'channels': [{key: channel[key] for key in ['name', 'shift_response']} for channel in rows]}), flush=True)
            for module in tuple(sys.modules.values()):
                filename = getattr(module, '__file__', None)
                if filename:
                    path = Path(filename).resolve()
                    if path.parent == root / 'scripts' and path.suffix == '.py':
                        own(path)
            check('all_inputs_preserved', all(digest(root / name) == expected for name, expected in inputs.items()))
            check('all_outputs_preserved', all(digest(root / name) == expected for name, expected in outputs.items()))
            check('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
            report.update(state='complete', passed=sum(row['passed'] for row in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
            report.pop('active_sample', None)
            save()
            (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')
            print(json.dumps({name: report[name] for name in ['state', 'passed', 'total', 'completed_utc']}), flush=True)
            return
        except Exception as error:
            report.update(state='failed', failure=repr(error), traceback=traceback.format_exc())
            save()
            raise
    report_path = destination / 'status.json'
    report = json.loads(report_path.read_text())
    if report['state'] != 'complete' or report['passed'] != report['total'] or len(report['samples']) != 18 or report['probe_limit']:
        raise RuntimeError('Full source decomposition validation incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    own(report_path)
    own(destination / 'COMPLETE')
    note = root / 'DERIVATION-20260910-variational-shift-source-decomposition.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-shift-source-schur-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 10, 15, 0, 33, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache gate failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'saved_states': len(report['samples']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-10T15:00:33Z, not a full pre-turn hash baseline', 'no_bytecode_cache': True, 'static_variational_source_decomposition_verified': True, 'observed_tangent_used_to_build_sources': False, 'all_shift_equations_verified': False, 'continuum_convergence_proved': False, 'scope': report['scope'], 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()

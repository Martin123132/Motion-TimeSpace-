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
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_parent_coefficient_box_20260910 import Box
    from annular_joint_weak_action_20260910 import joint_prototype, weak_bulk_directional_control

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    parser.add_argument('--attempt', default='attempt01')
    parser.add_argument('--limit', type=int, default=0)
    arguments = parser.parse_args()
    if not re.fullmatch('[a-z0-9-]+', arguments.attempt) or arguments.limit < 0:
        raise ValueError('Invalid attempt/limit.')
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260910'
    destination = intake / ('annular-joint-weak-action-' + arguments.attempt)
    final_path = intake / 'annular-joint-weak-action-final-integrity.json'
    prior_path = intake / 'annular-weak-product-compatibility-final-integrity.json'
    roots_path = intake / 'annular-parent-root-residence-attempt02/status.json'
    scripts = ['annular_joint_weak_action_20260910.py', 'derive_annular_joint_weak_action_20260910.py']
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

    def contains_zero(value):
        return numerical.all(value.lo <= 0) and numerical.all(value.hi >= 0)

    def bounds(value):
        return {'lower': float(numerical.maximum(0., numerical.maximum(value.lo, -value.hi)).max()), 'upper': float(value.magnitude.max())}

    prior = json.loads(prior_path.read_text())
    if prior['state'] != 'complete':
        raise RuntimeError('Prior checkpoint incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    for path in [prior_path, roots_path]:
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
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'probe_limit': arguments.limit, 'original_fields_unchanged': True, 'production_action_modified': False, 'new_numerical_evolution': False, 'enrichment_built_from_observed_defect': False, 'full_parent_constraint_preservation': False, 'continuum_convergence_proved': False, 'valid_for_physics_claim': False, 'scope': 'Joint mass/shift weak-action kinematic prototype plus exact Gram virtual-work cancellation. Extra mass Euler rows checked, not assumed zero. No full nonlinear or nonsmooth-spacetime result.'}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        save()
        try:
            radius = symbolic.symbols('radius', positive=True)
            lapse = symbolic.Function('lapse')(radius)
            eta = symbolic.Function('eta')(radius)
            field_f = symbolic.Function('field_f')(radius)
            zeta = field_f * (lapse * symbolic.diff(eta, radius) - eta * symbolic.diff(lapse, radius))
            check('symbolic_exact_Gram_link_primitive', symbolic.simplify(zeta / (lapse**2 * field_f) - symbolic.diff(eta / lapse, radius)) == 0)
            case_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
            own(case_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            samples = json.loads(roots_path.read_text())['samples']
            if arguments.limit:
                samples = samples[:arguments.limit]
            for sample in samples:
                label, branch = sample['label'], sample['branch']
                report['active_sample'] = label
                save()
                print('Starting ' + label, flush=True)
                path = roots_path.parent / (label + '.npz')
                own(path)
                with numerical.load(path) as handle:
                    archived = {name: handle[name].copy() for name in handle.files}
                basis = MixedActionBasis(archived['basis_radii'])
                links = MetricLinkQuadrature(basis)
                count = basis.radii.size
                configuration, momenta = archived['original_configuration'], archived['original_momenta']
                clock = archived['affine_clock'][0]
                system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], clock, links)
                maps_equal = all(numerical.array_equal(value, numerical.asarray(getattr(basis, name[6:]))) for name, value in archived.items() if name.startswith('basis_'))
                maps_equal = maps_equal and all(numerical.array_equal(value, getattr(links, name[6:])) for name, value in archived.items() if name.startswith('links_'))
                check(label + '_original_maps_preserved', maps_equal)
                packed = Box(archived['initial_root_box_lower'], archived['initial_root_box_upper'])
                data = joint_prototype(system, packed, Box(configuration), branch != 'GR')
                for name, diagnostic in data['diagnostics'].items():
                    check(label + '_' + name + '_verified_inverse', diagnostic['componentwise_majorant_verified'] and diagnostic['contraction'] < 1)
                check(label + '_local_bubble_Gram_positive', numerical.all(data['local_bubble_determinant'].lo > 0))
                check(label + '_Gram_endpoint_virtual_work_cancels', contains_zero(data['Gram_joint_cancellation']))
                check(label + '_original_shift_equations_after_enrichment', contains_zero(data['original_shift_residual_after_enrichment']))
                check(label + '_enriched_shift_equations_after_enrichment', contains_zero(data['enriched_shift_residual_after_enrichment']))
                check(label + '_enriched_pairing_symmetric', contains_zero(data['enriched_pairing'] - data['enriched_pairing'].T))
                check(label + '_shift_projection_orthogonality', contains_zero(data['shift_projection_orthogonality']))
                check(label + '_enriched_pairing_identity', contains_zero(data['enriched_pairing_identity']))
                action_control = weak_bulk_directional_control(system, packed, configuration, momenta, clock, data)
                check(label + '_weak_bulk_zero_shift_embedding', action_control['zero_shift_bulk_embedding_error'] < 1e-10, action_control)
                check(label + '_weak_bulk_first_variation', action_control['first_variation_error'] < 1e-9, action_control)
                check(label + '_weak_bulk_second_variation', action_control['second_coefficient_error'] < 1e-4 * (1 + abs(action_control['second_coefficient'])), action_control)
                original_midpoint = float(abs(data['original_shift_residual_after_enrichment'].midpoint).max())
                enriched_midpoint = float(abs(data['enriched_shift_residual_after_enrichment'].midpoint).max())
                check(label + '_midpoint_shift_closure', max(original_midpoint, enriched_midpoint) < 1e-8, [original_midpoint, enriched_midpoint])
                if branch == 'GR':
                    check(label + '_Gram_channels_absent', numerical.all(data['Gram_joint_cancellation'].magnitude == 0) and numerical.all(data['Gram_endpoint_shift'].magnitude == 0))
                arrays = {}
                for name, value in data.items():
                    if isinstance(value, Box):
                        arrays[name + '_lower'], arrays[name + '_upper'] = value.lo, value.hi
                output = destination / (label + '.npz')
                numerical.savez_compressed(output, **arrays)
                with numerical.load(output) as saved:
                    check(label + '_archive_roundtrip_exact', set(saved.files) == set(arrays) and all(numerical.array_equal(saved[name], value) for name, value in arrays.items()))
                artifact(output)
                row = {'label': label, 'branch': branch, 'intervals': sample['intervals'], 'saved_time': sample['saved_time'], 'original_new_test_obstruction': bounds(data['original_enriched_shift_residual']), 'old_mass_space_insufficient': bounds(data['original_enriched_shift_residual'])['lower'] > 0, 'mass_speed_change': bounds(data['mass_speed_change']), 'Gram_cancellation': bounds(data['Gram_joint_cancellation']), 'Gram_link_quadrature_remainder': bounds(data['Gram_link_quadrature_remainder']), 'new_original_shift_residual': bounds(data['original_shift_residual_after_enrichment']), 'new_enriched_shift_residual': bounds(data['enriched_shift_residual_after_enrichment']), 'added_mass_equations': bounds(data['added_mass_equations']), 'zero_shift_and_shift_rate_embedding_rejected': bounds(data['added_mass_equations'])['lower'] > 0, 'original_midpoint_error': original_midpoint, 'enriched_midpoint_error': enriched_midpoint, 'diagnostics': data['diagnostics'], 'action_control': action_control, 'kinematic_shift_solve_verified': True, 'full_parent_constraint_preservation': False}
                report['samples'].append(row)
                save()
                print(json.dumps(row), flush=True)
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
        raise RuntimeError('Full joint-action validation incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    own(report_path)
    own(destination / 'COMPLETE')
    note = root / 'DERIVATION-20260910-joint-weak-action-and-compatible-mass-lift.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-joint-weak-action-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 10, 19, 39, 15, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache gate failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'saved_states': len(report['samples']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-10T19:39:15Z, not a full pre-turn hash baseline', 'no_bytecode_cache': True, 'kinematic_shift_solve_verified': True, 'full_parent_constraint_preservation': False, 'continuum_convergence_proved': False, 'valid_for_physics_claim': False, 'scope': report['scope']}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()

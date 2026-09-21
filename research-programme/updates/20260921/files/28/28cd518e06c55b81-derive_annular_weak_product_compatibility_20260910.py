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
    from annular_parent_coefficient_box_20260910 import Box
    from annular_weak_product_compatibility_20260910 import CHANNELS, weak_product_source

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    parser.add_argument('--attempt', default='attempt01')
    parser.add_argument('--limit', type=int, default=0)
    arguments = parser.parse_args()
    if not re.fullmatch('[a-z0-9-]+', arguments.attempt) or arguments.limit < 0:
        raise ValueError('Invalid attempt/limit.')
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260910'
    destination = intake / ('annular-weak-product-compatibility-' + arguments.attempt)
    final_path = intake / 'annular-weak-product-compatibility-final-integrity.json'
    prior_path = intake / 'annular-shift-source-schur-final-integrity.json'
    source_path = intake / 'annular-shift-source-schur-attempt01/status.json'
    roots_path = intake / 'annular-parent-root-residence-attempt02/status.json'
    scripts = ['annular_weak_product_compatibility_20260910.py', 'derive_annular_weak_product_compatibility_20260910.py']
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

    def box(arrays, name):
        return Box(arrays[name + '_lower'], arrays[name + '_upper'])

    def contains_zero(value):
        return numerical.all(value.lo <= 0) and numerical.all(value.hi >= 0)

    def bounds(value):
        return {'lower': float(numerical.maximum(0., numerical.maximum(value.lo, -value.hi)).max()), 'upper': float(value.magnitude.max())}

    prior = json.loads(prior_path.read_text())
    if prior['state'] != 'complete':
        raise RuntimeError('Previous source checkpoint incomplete.')
    inherit(inputs, prior['inputs'])
    inherit(outputs, prior['outputs'])
    for path in [prior_path, source_path, roots_path]:
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
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'probe_limit': arguments.limit, 'channels': CHANNELS, 'runtime': {'python': sys.version, 'numpy': numerical.__version__, 'scipy': scipy.__version__}, 'new_numerical_evolution': False, 'action_modified': False, 'observed_shift_used_as_source': False, 'full_shift_closure': False, 'continuum_convergence_proved': False, 'valid_for_physics_claim': False, 'scope': 'Canonical finite-quadrature weak product identity, using independent source-owned trial rates and existing exact free roots. No continuum integration or quadrature-error certificate.'}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        save()
        try:
            radius, lapse, field_f, mass_r, speed, speed_r, velocity, gradient, lapse_r, eta, eta_r, kappa = symbolic.symbols('radius lapse field_f mass_r speed speed_r velocity gradient lapse_r eta eta_r kappa', positive=True)
            mass_density = lapse * mass_r / (kappa * radius * field_f**symbolic.Rational(3, 2)) + radius * velocity**2 / (2 * lapse * field_f**symbolic.Rational(3, 2)) + radius * lapse * gradient**2 / (2 * symbolic.sqrt(field_f))
            mass_gradient_density = lapse / (kappa * symbolic.sqrt(field_f))
            mass_test = eta * speed / lapse
            mass_test_r = eta_r * speed / lapse + eta * speed_r / lapse - eta * speed * lapse_r / lapse**2
            scalar_flux = kappa * radius**2 * field_f * velocity * gradient
            geometry = speed_r / (kappa * symbolic.sqrt(field_f)) + mass_r * speed / (kappa * radius * field_f**symbolic.Rational(3, 2)) + radius * speed * (velocity**2 / (lapse**2 * field_f) + gradient**2) / (2 * symbolic.sqrt(field_f))
            first = eta * geometry + radius**2 * lapse * symbolic.sqrt(field_f) * gradient * velocity * (eta_r / lapse - eta * lapse_r / lapse**2)
            second = mass_density * mass_test + mass_gradient_density * mass_test_r + (scalar_flux - speed) * (eta_r - eta * lapse_r / lapse) / (kappa * symbolic.sqrt(field_f))
            check('symbolic_local_product_identity', symbolic.simplify(first - second) == 0)
            case_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
            own(case_path)
            case = json.loads(case_path.read_text())
            constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
            samples = json.loads(source_path.read_text())['samples']
            if arguments.limit:
                samples = samples[:arguments.limit]
            for sample in samples:
                label, branch = sample['label'], sample['branch']
                report['active_sample'] = label
                save()
                print('Starting ' + label, flush=True)
                archived = loaded(roots_path.parent / (label + '.npz'))
                sourced = loaded(source_path.parent / (label + '.npz'))
                basis = MixedActionBasis(archived['basis_radii'])
                links = MetricLinkQuadrature(basis)
                count = basis.radii.size
                configuration, momenta = archived['original_configuration'], archived['original_momenta']
                clock = archived['affine_clock'][0]
                system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], clock, links)
                maps_equal = all(numerical.array_equal(value, numerical.asarray(getattr(basis, name[6:]))) for name, value in archived.items() if name.startswith('basis_'))
                maps_equal = maps_equal and all(numerical.array_equal(value, getattr(links, name[6:])) for name, value in archived.items() if name.startswith('links_'))
                check(label + '_basis_and_links_preserved', maps_equal)
                packed = Box(archived['initial_root_box_lower'], archived['initial_root_box_upper'])
                lapse_rate = box(sourced, 'trial_lapse_channels') @ Box(numerical.ones(6))
                data = weak_product_source(system, packed, Box(configuration), Box(momenta), Box(clock), box(sourced, 'full_shift_rate'), lapse_rate, archived['endpoint_acceleration'], branch != 'GR')
                previous = box(sourced, 'obstruction_channels') @ Box(numerical.ones(6))
                for name, diagnostic in data['diagnostics'].items():
                    check(label + '_' + name + '_verified_inverse', diagnostic['componentwise_majorant_verified'] and diagnostic['contraction'] < 1)
                for name in ['full_algebra_difference', 'free_root_remainder', 'scalar_projection_orthogonality', 'shift_equation_check']:
                    check(label + '_' + name + '_contains_zero', contains_zero(data[name]))
                check(label + '_original_schur_obstruction_agreement', contains_zero(data['direct_lapse_derivative'] - previous))
                check(label + '_weak_identity_predicts_obstruction', contains_zero(data['reconstructed_obstruction'] - previous))
                midpoint_error = float(abs(data['reconstructed_obstruction'].midpoint - previous.midpoint).max())
                check(label + '_midpoint_agreement', midpoint_error < 1e-10, midpoint_error)
                check(label + '_every_interior_hat_has_positive_shift_jump', numerical.all(data['shift_hat_neighbor_jump'].lo > 0))
                if branch == 'GR':
                    check(label + '_Gram_channels_exactly_absent', numerical.all(data['channels'].magnitude[:, 6:] == 0))
                arrays = {}
                for name, value in data.items():
                    if isinstance(value, Box):
                        arrays[name + '_lower'], arrays[name + '_upper'] = value.lo, value.hi
                output = destination / (label + '.npz')
                numerical.savez_compressed(output, **arrays)
                with numerical.load(output) as saved:
                    check(label + '_archive_roundtrip_exact', set(saved.files) == set(arrays) and all(numerical.array_equal(saved[name], value) for name, value in arrays.items()))
                artifact(output)
                row = {'label': label, 'branch': branch, 'intervals': sample['intervals'], 'saved_time': sample['saved_time'], 'reconstructed_obstruction': bounds(data['reconstructed_obstruction']), 'previous_obstruction': bounds(previous), 'interior_obstruction': bounds(data['reconstructed_obstruction'][1:-1]), 'midpoint_difference': midpoint_error, 'free_root_remainder': bounds(data['free_root_remainder']), 'Gram_combined': bounds(data['Gram_combined']), 'Gram_combined_interior': bounds(data['Gram_combined'][1:-1]), 'boundary_pair': bounds(data['boundary_pair']), 'channels': [{'name': name, 'norm': bounds(data['channels'][:, column]), 'interior_norm': bounds(data['channels'][1:-1, column])} for column, name in enumerate(CHANNELS)], 'diagnostics': data['diagnostics']}
                row.update(scalar_only_enrichment_obstruction=bounds(data['scalar_enriched_necessary_interior_obstruction']), scalar_only_enrichment_rejected=bounds(data['scalar_enriched_necessary_interior_obstruction'])['lower'] > 0, minimum_positive_shift_jump=float(data['shift_hat_neighbor_jump'].lo.min()), scalar_enrichment_is_necessary_condition_test_only=True)
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
        raise RuntimeError('Full weak-product validation incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    own(report_path)
    own(destination / 'COMPLETE')
    note = root / 'DERIVATION-20260910-weak-product-compatibility-and-action-repair-condition.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-weak-product-compatibility-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 10, 17, 13, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache gate failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'checks': report['total'], 'saved_states': len(report['samples']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-10T17:13:00Z, conservative before first time reading; not a full pre-turn hash baseline', 'no_bytecode_cache': True, 'weak_product_identity_verified': True, 'action_modified': False, 'full_shift_closure': False, 'continuum_convergence_proved': False, 'valid_for_physics_claim': False, 'scope': report['scope']}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'checks', 'saved_states', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()

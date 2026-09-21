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
    from scipy.linalg import solve
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_first_derivative_energy_20260909 import affine_lift_matrix

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    old_intake = root / 'source-intake/navier-stokes/20260909'
    intake = root / 'source-intake/navier-stokes/20260910'
    parent_folder = intake / 'annular-paired-variational-energy-derived-attempt03'
    destination = intake / 'annular-boundary-trace-projection-derived'
    final_path = intake / 'annular-paired-variational-energy-final-integrity.json'
    parent_path = parent_folder / 'status.json'
    parent = json.loads(parent_path.read_text())
    if parent['state'] != 'complete' or parent['passed'] != parent['total']:
        raise RuntimeError('Paired identity gate incomplete.')
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

    inherit(inputs, parent['inputs'])
    inherit(outputs, parent['outputs'])
    for path in [Path(__file__).resolve(), parent_path, parent_folder / 'COMPLETE', parent_folder / 'executed-script.py']:
        own(path)
    compile(Path(__file__).read_bytes(), str(Path(__file__)), 'exec')
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'nonzero_trace_H1_projection_obstruction_derived': True, 'actual_source_trace_law_proved': False, 'endpoint_coefficients_are_diagnostic_projections_not_parent_parameters': True, 'valid_for_physics_claim': False}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        def close(name, first, second, tolerance=2e-8):
            error = float(numerical.max(abs(numerical.asarray(first) - second)))
            scale = 1 + float(numerical.max(abs(numerical.asarray(second))))
            check(name, error <= tolerance * scale, {'error': error, 'scale': scale})

        save()
        try:
            for sample in parent['samples']:
                label = sample['label']
                base = loaded(old_intake / 'annular-first-derivative-energy-derived' / (label + '.npz'))
                new = loaded(parent_folder / (label + '.npz'))
                source = loaded(old_intake / 'annular-released-Hermite-initial-derived' / (label.split('_sample')[0] + '.npz'))
                basis = MixedActionBasis(source['radius'])
                free = base['free']
                lift = affine_lift_matrix(basis)
                projected_lift = solve(base['M'], (base['full_M'] @ lift)[free], assume_a='sym')
                gram = projected_lift.T @ base['K'] @ projected_lift
                source_configuration = new['source_configuration']
                beta = solve(gram, projected_lift.T @ base['K'] @ source_configuration, assume_a='sym')
                boundary_part = projected_lift @ beta
                remainder = source_configuration - boundary_part
                total_squared = float(source_configuration @ base['K'] @ source_configuration)
                boundary_squared = float(boundary_part @ base['K'] @ boundary_part)
                remainder_squared = float(remainder @ base['K'] @ remainder)
                close(label + '_K_orthogonal_source_decomposition', projected_lift.T @ base['K'] @ remainder, numerical.zeros(2))
                close(label + '_source_norm_Pythagoras', total_squared, boundary_squared + remainder_squared)
                total_work = float(new['graph'] @ base['K'] @ source_configuration)
                boundary_work = float(new['graph'] @ base['K'] @ boundary_part)
                remainder_work = float(new['graph'] @ base['K'] @ remainder)
                close(label + '_source_work_not_discarded', total_work, boundary_work + remainder_work)
                row = {'label': label, 'intervals': sample['intervals'], 'branch': sample['branch'], 'time': sample['time'], 'diagnostic_endpoint_coefficients': beta.tolist(), 'source_configuration_Knorm': numerical.sqrt(max(total_squared, 0.)), 'endpoint_projection_Knorm': numerical.sqrt(max(boundary_squared, 0.)), 'remainder_Knorm': numerical.sqrt(max(remainder_squared, 0.)), 'fraction_source_squared_in_endpoint_subspace': boundary_squared / total_squared if total_squared > 0 else 0., 'boundary_work': boundary_work, 'remainder_work': remainder_work}
                if sample['time'] == max(item['time'] for item in parent['samples']):
                    value = numerical.concatenate([basis.scalar_value, basis.lift_value / basis.spacing], axis=1)[:, free]
                    radial = numerical.concatenate([basis.scalar_gradient, basis.lift_gradient / basis.spacing], axis=1)[:, free]
                    projected_one = projected_lift @ numerical.ones(2)
                    error = numerical.sqrt(numerical.dot(basis.quadrature_weights, (1 - value @ projected_one)**2))
                    gradient = numerical.sqrt(numerical.dot(basis.quadrature_weights, (radial @ projected_one)**2))
                    length = float(basis.radii[-1] - basis.radii[0])
                    lower = (1 - error**2 / length) / (2 * error)
                    check(label + '_nonzero_trace_projection_derivative_lower_bound', gradient + 1e-8 >= lower, {'actual': float(gradient), 'lower': float(lower), 'L2_error': float(error)})
                    nodes = basis.radii - basis.radii[0]
                    polynomial = nodes * (length - nodes)
                    polynomial_slope = basis.spacing * (length - 2 * nodes - basis.derivative @ polynomial)
                    full_polynomial = numerical.concatenate([polynomial, polynomial_slope])
                    projected_polynomial = solve(base['M'], (base['full_M'] @ full_polynomial)[free], assume_a='sym')
                    close(label + '_zero_trace_polynomial_projection_exact', projected_polynomial, full_polynomial[free])
                    polynomial_gradient = numerical.sqrt(numerical.dot(basis.quadrature_weights, (radial @ projected_polynomial)**2))
                    close(label + '_zero_trace_polynomial_uniform_derivative', polynomial_gradient, numerical.sqrt(length**3 / 3))
                    row['constant_projection_control'] = {'L2_error': float(error), 'derivative_L2': float(gradient), 'trace_lower_bound': float(lower), 'zero_trace_polynomial_derivative_L2': float(polynomial_gradient)}
                    print(json.dumps(row), flush=True)
                report['samples'].append(row)
                output = destination / (label + '.npz')
                numerical.savez_compressed(output, projected_endpoint_lifts=projected_lift, diagnostic_coefficients=beta, boundary_source=boundary_part, remainder_source=remainder)
                artifact(output)
                save()
            for module in tuple(sys.modules.values()):
                filename = getattr(module, '__file__', None)
                if filename:
                    path = Path(filename).resolve()
                    if path.parent == root / 'scripts' and path.suffix == '.py':
                        own(path)
            check('all_inherited_sources_preserved', all(digest(root / name) == expected for name, expected in inputs.items()))
            check('all_inherited_and_new_evidence_preserved', all(digest(root / name) == expected for name, expected in outputs.items()))
            check('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
            report.update(state='complete', passed=sum(row['passed'] for row in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
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
    if report['state'] != 'complete' or report['passed'] != report['total']:
        raise RuntimeError('Projection control incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260910-paired-variational-work-and-graph-energy-correction.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    for attempt_name in ['annular-paired-variational-energy-derived', 'annular-paired-variational-energy-derived-attempt02']:
        for filename in ['status.json', 'executed-script.py']:
            own(intake / attempt_name / filename)
    snapshot = intake / 'annular-paired-variational-energy-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 23, 45, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'paired_checks': parent['total'], 'projection_checks': report['total'], 'total_checks': parent['total'] + report['total'], 'saved_states': len(parent['samples']), 'frozen_controls': len(parent['frozen_controls']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T23:45:00Z, not a full pre-turn hash baseline', 'no_bytecode_cache': True, 'paired_identity_and_graph_correction_derived': True, 'nonzero_trace_projection_obstruction_derived': True, 'actual_source_boundary_correction_and_uniform_growth_open': True, 'full_evolution_closed': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'total_checks', 'saved_states', 'frozen_controls', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()

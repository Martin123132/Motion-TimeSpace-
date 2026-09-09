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
    from annular_adm_mixed_action_20260909 import MixedActionBasis, real_linear

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-affine-commutator-energy-control'
    final_path = intake / 'annular-mass-trace-final-integrity.json'
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

    gate_path = intake / 'annular-mass-trace-remainder-bound-derived/status.json'
    gate = json.loads(gate_path.read_text())
    if gate['state'] != 'complete' or gate['passed'] != gate['total'] or not (gate_path.parent / 'COMPLETE').is_file():
        raise RuntimeError('Mass-trace derivation gate is incomplete.')
    inherit(inputs, gate['inputs'])
    inherit(outputs, gate['outputs'])
    for path in [gate_path, gate_path.parent / 'COMPLETE', gate_path.parent / 'executed-script.py', Path(__file__)]:
        own(path)
    compile(Path(__file__).read_bytes(), str(Path(__file__)), 'exec')
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'scope': 'Exact cubic polynomial inverse estimates remove the unnecessary uniform third-derivative assumption from the affine scalar commutator. A uniform velocity H1 energy estimate is still not proved.'}

        def save():
            (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name + ' ' + repr(detail))

        save()
        try:
            coordinate = symbolic.symbols('coordinate', real=True)
            shape = coordinate**2 * (1 - coordinate)**2
            check('exact_Hermite_value_error_integral', symbolic.integrate(shape**2, (coordinate, 0, 1)) == symbolic.Rational(1, 630))
            check('exact_Hermite_derivative_error_integral', symbolic.integrate(symbolic.diff(shape, coordinate)**2, (coordinate, 0, 1)) == symbolic.Rational(2, 105))
            legendre = (3 * coordinate**2 - 1) / 2
            check('exact_quadratic_Legendre_norm', symbolic.integrate(legendre**2, (coordinate, -1, 1)) == symbolic.Rational(2, 5))
            check('exact_value_commutator_constant', symbolic.Rational(720, 36 * 630) == symbolic.Rational(2, 63))
            check('exact_derivative_commutator_constant', symbolic.Rational(720, 36) * symbolic.Rational(2, 105) == symbolic.Rational(8, 21))
            for sample in gate['samples']:
                tag = sample['case'] + '_N' + str(sample['intervals']) + '_' + sample['branch']
                steps = 64 if sample['intervals'] == 64 else 32
                index = int(round(sample['time'] / .01 * steps))
                trajectory = loaded(root / sample['source_trajectory'])
                arrays = loaded(gate_path.parent / (tag + '_sample' + str(index) + '.npz'))
                basis = MixedActionBasis(trajectory['radius'])
                count, face_count = basis.radii.size, basis.faces.size
                packed = trajectory['state'][index, 4 * count:]
                velocity = packed[face_count + count:face_count + 2 * count]
                slope_velocity = packed[face_count + 2 * count:face_count + 3 * count]
                velocity_gradient = real_linear(basis.scalar_gradient, velocity) + real_linear(basis.lift_gradient, slope_velocity / basis.spacing)
                velocity_value = real_linear(basis.scalar_value, velocity) + real_linear(basis.lift_value, slope_velocity / basis.spacing)
                width = numerical.diff(basis.radii)
                length = basis.radii[-1] - basis.radii[0]
                norm_gradient_squared = numerical.dot(basis.quadrature_weights, velocity_gradient**2)
                norm_velocity_squared = numerical.dot(basis.quadrature_weights, velocity_value**2)
                norm_error_squared = numerical.dot(basis.quadrature_weights, arrays['bulk_scalar_error']**2)
                norm_error_gradient_squared = numerical.dot(basis.quadrature_weights, arrays['bulk_scalar_radial_error']**2)
                third = arrays['bulk_velocity_third']
                exact_error_squared = numerical.sum(third**2 * width**9) / (36 * 630 * length**2)
                exact_gradient_error_squared = numerical.sum(third**2 * width**7) / (9 * 210 * length**2)
                value_bound_squared = (2 / 63) * numerical.max(width)**4 * norm_gradient_squared / length**2
                gradient_bound_squared = (8 / 21) * numerical.max(width)**2 * norm_gradient_squared / length**2
                label = tag + '_sample' + str(index)
                allowance = 1e-25 + 1e-9 * max(exact_error_squared, value_bound_squared)
                check(label + '_positive_Gauss_underestimate_for_degree8_square', norm_error_squared <= exact_error_squared + allowance)
                check(label + '_degree6_derivative_square_exact_quadrature', abs(norm_error_gradient_squared - exact_gradient_error_squared) <= 1e-24 + 1e-9 * exact_gradient_error_squared)
                check(label + '_velocity_H1_controls_value_commutator', exact_error_squared <= value_bound_squared + allowance)
                check(label + '_velocity_H1_controls_gradient_commutator', exact_gradient_error_squared <= gradient_bound_squared + 1e-24 + 1e-9 * gradient_bound_squared)
                force_norm = numerical.sqrt(numerical.dot(basis.quadrature_weights, arrays['bulk_scalar_Euler_density']**2))
                radial_force_norm = numerical.sqrt(numerical.dot(basis.quadrature_weights, arrays['bulk_scalar_radial_force']**2))
                scalar_bound = numerical.sqrt(value_bound_squared) * force_norm + numerical.sqrt(gradient_bound_squared) * radial_force_norm
                actual_scalar = float(arrays['bulk_signed_scalar_commutator'] + arrays['bulk_signed_scalar_radial_product'])
                check(label + '_scalar_bound_without_third_derivative_assumption', abs(actual_scalar) <= scalar_bound + 1e-13)
                per_cell_gradient = numerical.zeros(width.size)
                cell = numerical.clip(numerical.searchsorted(basis.radii, basis.quadrature, side='right') - 1, 0, width.size - 1)
                numerical.add.at(per_cell_gradient, cell, basis.quadrature_weights * velocity_gradient**2)
                third_bound_squared = 720 * per_cell_gradient / width**5
                check(label + '_cellwise_quadratic_inverse_estimate', numerical.all(third**2 <= third_bound_squared + 1e-14 + 1e-8 * third_bound_squared))
                path = destination / (label + '.npz')
                numerical.savez_compressed(path, velocity_gradient=velocity_gradient, velocity_value=velocity_value, cell_velocity_gradient_norm_squared=per_cell_gradient, third_derivative_bound_squared=third_bound_squared, error_norm_squared=norm_error_squared, exact_error_norm_squared=exact_error_squared, error_gradient_norm_squared=norm_error_gradient_squared, value_bound_squared=value_bound_squared, gradient_bound_squared=gradient_bound_squared, scalar_commutator_bound=scalar_bound)
                artifact(path)
                report['samples'].append({'case': sample['case'], 'intervals': sample['intervals'], 'branch': sample['branch'], 'time': sample['time'], 'velocity_L2_norm': float(numerical.sqrt(norm_velocity_squared)), 'velocity_radial_L2_norm': float(numerical.sqrt(norm_gradient_squared)), 'maximum_velocity_third': float(numerical.max(numerical.abs(third))), 'value_error_norm': float(numerical.sqrt(norm_error_squared)), 'value_error_H1_bound': float(numerical.sqrt(value_bound_squared)), 'gradient_error_norm': float(numerical.sqrt(norm_error_gradient_squared)), 'gradient_error_H1_bound': float(numerical.sqrt(gradient_bound_squared)), 'scalar_force_L2_norm': float(force_norm), 'scalar_radial_force_L2_norm': float(radial_force_norm), 'scalar_signed': actual_scalar, 'scalar_bound_using_H1_only': float(scalar_bound)})
            for module in tuple(sys.modules.values()):
                filename = getattr(module, '__file__', None)
                if filename:
                    path = Path(filename).resolve()
                    if path.parent == root / 'scripts' and path.suffix == '.py':
                        own(path)
            check('all_sources_preserved', all(digest(root / name) == expected for name, expected in inputs.items()))
            check('all_outputs_preserved', all(digest(root / name) == expected for name, expected in outputs.items()))
            check('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
            report.update(state='complete', passed=sum(row['passed'] for row in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
            save()
            (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')
            print(json.dumps({key: report[key] for key in ['state', 'passed', 'total', 'completed_utc']}), flush=True)
            print(json.dumps([sample for sample in report['samples'] if sample['time'] == .01], indent=2), flush=True)
            return
        except Exception as error:
            report.update(state='failed', failure=repr(error), traceback=traceback.format_exc(), completed_utc=datetime.now(timezone.utc).isoformat())
            save()
            raise
    if final_path.exists():
        raise FileExistsError('Final evidence already exists.')
    report_path = destination / 'status.json'
    report = json.loads(report_path.read_text())
    if report['state'] != 'complete' or report['passed'] != report['total'] or not (destination / 'COMPLETE').exists():
        raise RuntimeError('Energy-commutator gate incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    scripts = ['annular_mass_trace_remainder_bound_20260909.py', 'derive_annular_mass_trace_bound_20260909.py', 'derive_annular_commutator_energy_control_20260909.py']
    for name in scripts:
        path = root / 'scripts' / name
        compile(path.read_bytes(), str(path), 'exec')
    note = root / 'DERIVATION-20260909-mass-trace-control-and-bulk-commutator-bound.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.json', '.md', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-mass-trace-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    artifact(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 16, 1, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench or cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'mass_trace_checks': gate['total'], 'energy_commutator_checks': report['total'], 'state_samples': len(gate['samples']), 'energy_counterexamples': len(gate['energy_counterexamples']), 'compiled_scripts': scripts, 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T16:01:00Z, not full pre-turn hash comparison; all writes scoped to post-checkpoint-work', 'mutable_resume_pinned_as_snapshot': True, 'no_bytecode_cache': True, 'physical_mass_trace_estimate_derived': True, 'affine_bulk_commutators_derived': True, 'uniform_third_derivative_assumption_removed': True, 'uniform_velocity_H1_evolution_estimate_proved': False, 'full_coupled_DAE_solved': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({'state': final['state'], 'mass_trace_checks': gate['total'], 'energy_commutator_checks': report['total'], 'samples': len(gate['samples']), 'input_hashes': len(inputs), 'output_hashes': len(outputs), 'protected_workbench_files_written_since_turn_start': len(touched)}), flush=True)


if __name__ == '__main__':
    run()

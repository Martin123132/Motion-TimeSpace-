import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import sympy as symbolic
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    gate_path = intake / 'annular-metric-Schur-bound-derived/status.json'
    gate = json.loads(gate_path.read_text())
    destination = intake / 'annular-metric-Schur-box-certified'
    final_path = intake / 'annular-metric-Schur-box-final-integrity.json'
    inputs, outputs = {}, {}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path):
        inputs[str(path.relative_to(root))] = digest(path)

    def inherit(table, entries):
        for name, expected in entries.items():
            actual = digest(root / name)
            if actual != expected or name in table and table[name] != actual:
                raise RuntimeError('Changed evidence: ' + name)
            table[name] = actual

    if gate['state'] != 'complete' or gate['passed'] != gate['total']:
        raise RuntimeError('Schur derivation incomplete.')
    inherit(inputs, gate['inputs'])
    inherit(outputs, gate['outputs'])
    for path in [gate_path, gate_path.parent / 'COMPLETE', gate_path.parent / 'executed-script.py', Path(__file__).resolve()]:
        own(path)
    compile(Path(__file__).read_bytes(), __file__, 'exec')
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        rational = symbolic.Rational
        checks = []

        def check(name, condition):
            checks.append({'name': name, 'passed': bool(condition)})
            if not condition:
                raise RuntimeError('Failed certificate: ' + name)

        inner, outer, length = rational(47, 8), rational(49, 8), rational(1, 4)
        kappa = rational(1, 10)
        f_min, f_max = rational(13, 20), rational(17, 25)
        n_min, n_max = rational(4, 5), rational(21, 25)
        q_max, w_max, mass_r = rational(1, 50), rational(3, 100), rational(1, 500)
        sqrt_f_lower, sqrt_f_upper = rational(4, 5), rational(5, 6)
        sigma_lower, sigma_upper = rational(121, 100), rational(5, 4)
        check('sqrt_F_lower', sqrt_f_lower**2 <= f_min)
        check('sqrt_F_upper', sqrt_f_upper**2 >= f_max)
        check('inverse_sqrt_lower', sigma_lower**2 * f_max <= 1)
        check('inverse_sqrt_upper', sigma_upper**2 * f_min >= 1)
        beta_geometry = rational(3, 25)
        check('exact_geometry_lower_bound', beta_geometry**2 <= rational(gate['geometry_certificate']['beta_squared']))
        nodal_poincare = rational(21, 20) * length
        check('nodal_Poincare_majorant', (nodal_poincare / length)**2 >= rational(17, 16))
        mass_max = outer**2 / (n_min * sqrt_f_lower)
        p_max = outer**2 * n_max * sqrt_f_upper
        denominator = inner * f_min
        sigma_center, sigma_radius = (sigma_lower + sigma_upper) / 2, (sigma_upper - sigma_lower) / 2
        perturbation = sigma_radius / kappa + length * mass_r / (kappa * inner * f_min * sqrt_f_lower)
        perturbation += length * (mass_max * q_max**2 + p_max * w_max**2) / (2 * denominator * n_min)
        perturbation += 2 * nodal_poincare * p_max * w_max**2 / (denominator * n_min)
        beta = sigma_center / kappa * beta_geometry - perturbation
        a_bound = 3 * n_max * mass_r * length**2 / (kappa * inner**2 * f_min**2 * sqrt_f_lower)
        a_bound += 2 * n_max * length / (kappa * inner * f_min * sqrt_f_lower)
        a_bound += rational(3, 2) * mass_max * q_max**2 * length**2 / denominator**2 + p_max * w_max**2 * length**2 / (2 * denominator**2)
        a_bound += 2 * p_max * w_max**2 * nodal_poincare**2 / denominator**2
        d_bound = mass_max * q_max**2 / n_min**2
        check('beta_at_least_5_over_4', beta >= rational(5, 4))
        check('A_at_most_7_over_5', a_bound <= rational(7, 5))
        check('D_at_most_1_over_25', d_bound <= rational(1, 25))
        reference_inverse = rational(7, 5)
        spectral_majorant = symbolic.Matrix([[reference_inverse, -rational(4, 5)], [-rational(4, 5), reference_inverse - rational(7, 5) * rational(16, 25)]])
        check('two_by_two_inverse_majorant_positive', spectral_majorant[0, 0] > 0 and spectral_majorant.det() > 0)
        feedback = reference_inverse / 25
        full_inverse = reference_inverse / (1 - feedback)
        check('strict_Neumann_margin', feedback < 1)
        check('full_uniform_inverse_at_most_3_over_2', full_inverse <= rational(3, 2))
        for row in gate['samples']:
            bound = row['bounds']
            envelope = bound['envelope']
            check(row['label'] + '_inside_single_box', envelope['F_min'] >= float(f_min) and envelope['F_max'] <= float(f_max) and envelope['N_min'] >= float(n_min) and envelope['N_max'] <= float(n_max) and bound['q_max'] <= float(q_max) and bound['w_max'] <= float(w_max) and bound['mass_R_max'] <= float(mass_r) and row['intervals'] >= 16)
            check(row['label'] + '_common_inverse_bound', row['measured']['inverse_norm'] < float(full_inverse))
        box = {'annulus_inner': str(inner), 'annulus_outer': str(outer), 'length': str(length), 'kappa': str(kappa), 'F_min': str(f_min), 'F_max': str(f_max), 'N_min': str(n_min), 'N_max': str(n_max), 'q_max': str(q_max), 'w_max': str(w_max), 'mass_R_max': str(mass_r), 'minimum_scalar_nodes': 17}
        constants = {'beta_geometry_lower': str(beta_geometry), 'mass_density_upper': str(mass_max), 'stiffness_density_upper': str(p_max), 'beta_full_lower': str(beta), 'A_upper': str(a_bound), 'D_upper': str(d_bound), 'reference_inverse_upper': str(reference_inverse), 'spectral_majorant_determinant': str(spectral_majorant.det()), 'Neumann_feedback_upper': str(feedback), 'full_inverse_upper': str(full_inverse), 'simple_full_inverse_upper': '3/2'}
        report = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': checks, 'passed': sum(row['passed'] for row in checks), 'total': len(checks), 'box': box, 'exact_rational_constants': constants, 'scope': 'Every canonical GR or owned Gram configuration in this explicit box on any supported n>=17 grid. H1-mass/L2-lapse inverse norm, not a claim that solutions remain in the box.', 'rational_inequalities_exact': True, 'saved_state_box_membership_float_evaluation_not_interval_certificate': True, 'uniform_source_or_lapse_trace_bound_proved': False, 'valid_for_physics_claim': False}
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')
        (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')
        print(json.dumps({'state': report['state'], 'checks': report['total'], 'constants': constants}), flush=True)
        return
    report_path = destination / 'status.json'
    report = json.loads(report_path.read_text())
    if report['state'] != 'complete' or report['passed'] != report['total']:
        raise RuntimeError('Common-box certificate incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260909-metric-Schur-inverse-and-projection-remainder.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.json', '.md', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-metric-Schur-box-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    outputs[str(snapshot.relative_to(root))] = digest(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 17, 35, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench or cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'Schur_checks': gate['total'], 'box_checks': report['total'], 'saved_canonical_states': len(gate['samples']), 'manufactured_cases': len(gate['manufactured']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T17:35:00Z; not full pre-turn hash comparison', 'mutable_resume_pinned_as_snapshot': True, 'no_bytecode_cache': True, 'uniform_canonical_inverse_in_explicit_box_derived': True, 'uniform_source_or_pointwise_lapse_trace_bound_derived': False, 'solution_stays_in_box_proved': False, 'full_coupled_DAE_solved': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'Schur_checks', 'box_checks', 'saved_canonical_states', 'manufactured_cases', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()

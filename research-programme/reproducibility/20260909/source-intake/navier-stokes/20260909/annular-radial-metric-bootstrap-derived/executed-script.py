import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def radial_bounds(inner_radius, outer_radius, kappa, inner_f, outer_clock, scalar_square_integral, mass_defect_l1, lapse_defect_l1):
    if min(inner_radius, outer_radius - inner_radius, kappa, inner_f, outer_clock) <= 0 or min(scalar_square_integral, mass_defect_l1, lapse_defect_l1) < 0:
        raise ValueError('Positive annulus/chart data and nonnegative norm bounds required.')
    import math
    exponent = kappa * outer_radius * scalar_square_integral
    lower_f = inner_radius / outer_radius * math.exp(-exponent) * inner_f - 2 / inner_radius * mass_defect_l1
    upper_f = max(inner_f, 1.0) + 2 / inner_radius * mass_defect_l1
    lower_clock = outer_clock * math.exp(-exponent - lapse_defect_l1)
    upper_clock = outer_clock * math.exp(lapse_defect_l1)
    positive = lower_f > 0
    return {'F_lower': lower_f, 'F_upper': upper_f, 'E_lower': lower_clock, 'E_upper': upper_clock, 'positive_chart_gate': positive, 'N_lower': lower_clock * math.sqrt(lower_f) if positive else None, 'N_upper': upper_clock * math.sqrt(upper_f), 'c_lower': lower_clock * lower_f if positive else None, 'c_upper': upper_clock * upper_f, 'scalar_exponent': exponent}


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis, linear_value_gradient
    from annular_metric_flux_jets_20260909 import flux_profile
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-radial-metric-bootstrap-derived'
    gate_path = intake / 'annular-metric-flux-jets-derived/status.json'
    gate = json.loads(gate_path.read_text())
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

    def loaded(path):
        own(path)
        with numerical.load(path) as handle:
            return {name: handle[name].copy() for name in handle.files}

    if gate['state'] != 'complete' or gate['passed'] != gate['total']:
        raise RuntimeError('Metric flux gate incomplete.')
    inherit(inputs, gate['inputs'])
    inherit(outputs, gate['outputs'])
    for path in [gate_path, gate_path.parent / 'COMPLETE', gate_path.parent / 'executed-script.py', Path(__file__).resolve()]:
        own(path)
    compile(Path(__file__).read_bytes(), __file__, 'exec')
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': [], 'samples': [], 'radial_chart_bounds_derived_with_residuals': True, 'uniform_coupled_evolution_bootstrap_closed': False, 'valid_for_physics_claim': False, 'reference_search': {'url': 'https://laplace.physics.ubc.ca/2010-pi-nr/www/bgsoft.html', 'role': 'Primary-source course index identifies Choptuik Einstein-massless-Klein-Gordon lectures; general context only. Local equations derived from owned action.', 'checked_date': '2026-09-09', 'linked_pdf': 'https://laplace.physics.ubc.ca/2010-pi-nr/ref/387n-09-choptuik-emkg-collapse.pdf', 'pdf_status': 'web fetch timed out; no theorem or equation attributed to its unread contents'}}

        def check(name, passed, detail=None):
            report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                raise RuntimeError('Failed check: ' + name)

        radius, spatial_f, density, kappa_symbol, defect = symbolic.symbols('radius F density kappa defect', positive=True)
        mass = radius * (1 - spatial_f) / 2
        mass_gradient = kappa_symbol * radius**2 * spatial_f * density / 2 + defect
        expected = (1 - spatial_f) / radius - kappa_symbol * radius * spatial_f * density - 2 * defect / radius
        check('exact_radial_F_linear_ODE', symbolic.simplify(-2 * mass_gradient / radius + 2 * mass / radius**2 - expected) == 0)
        failure_control = radial_bounds(1, 2, .1, .5, 1, 0, 1, 0)
        check('large_residual_refuses_positive_chart_not_clipped', failure_control['F_lower'] < 0 and failure_control['positive_chart_gate'] is False and failure_control['N_lower'] is None)
        case_path = intake / 'annular-constraint-correction-initial/canonical.json'
        own(case_path)
        case = json.loads(case_path.read_text())
        constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
        kappa = float(symbolic.sympify(case['normalization_kappa']))
        for sample in gate['samples']:
            label, intervals, branch = sample['label'], sample['intervals'], sample['branch']
            tag = label.split('_sample')[0]
            steps = 64 if intervals == 64 else 32
            index = int(label.rsplit('sample', 1)[1])
            source = loaded(intake / 'annular-released-Hermite-initial-derived' / (tag + '.npz'))
            folder = 'annular-boundary-N64-evolution-smoke' if intervals == 64 else 'annular-released-Hermite-evolution-smoke'
            trajectory = loaded(intake / folder / (tag + '_steps' + str(steps) + '.npz'))
            old = loaded(intake / 'annular-uniform-energy-bounds-derived' / (label + '.npz'))
            basis = MixedActionBasis(source['radius'])
            count = basis.radii.size
            state = trajectory['state'][index]
            scalar, slope, momentum, slope_momentum = [state[part * count:(part + 1) * count] for part in range(4)]
            system = ReleasedHermiteRouthian(basis, scalar, slope, constants, kappa, momentum, slope_momentum, source['outer_clock'][0] + trajectory['time'][index] * source['outer_clock'][1], MetricLinkQuadrature(basis))
            packed, speed = old['packed'], old['packed_speed']
            quadrature = MixedActionBasis(source['radius'], order=12)
            profile = flux_profile(system, packed, speed, quadrature.quadrature)
            knots = numerical.unique(numerical.concatenate([basis.radii, basis.faces]))
            mass_map = linear_value_gradient(basis.faces, knots)[0]
            lapse_map = linear_value_gradient(basis.radii, knots)[0]
            mass_values = mass_map @ packed[system.slices[0]]
            lapse_values = lapse_map @ packed[system.slices[1]]
            f_values = 1 - 2 * mass_values / knots
            q_l2_squared = float(numerical.dot(quadrature.quadrature_weights, profile['scalar_q']**2))
            w_l2_squared = float(numerical.dot(quadrature.quadrature_weights, profile['scalar_r']**2))
            scalar_square_bound = q_l2_squared / (min(lapse_values)**2 * min(f_values)) + w_l2_squared
            mass_tv = float(numerical.sum(abs(numerical.diff(mass_values))))
            mass_defect_bound = mass_tv + kappa * knots[-1]**2 * max(f_values) * scalar_square_bound / 2
            clock_log_tv_bound = float(numerical.sum(abs(numerical.diff(numerical.log(lapse_values)))) + .5 * numerical.sum(abs(numerical.diff(numerical.log(f_values)))))
            lapse_defect_bound = clock_log_tv_bound + kappa * knots[-1] * scalar_square_bound
            outer_clock = lapse_values[-1] / numerical.sqrt(f_values[-1])
            bounds = radial_bounds(float(knots[0]), float(knots[-1]), kappa, float(f_values[0]), float(outer_clock), scalar_square_bound, mass_defect_bound, lapse_defect_bound)
            check(label + '_positive_radial_chart_gate', bounds['positive_chart_gate'], bounds)
            check(label + '_F_enclosed', min(f_values) >= bounds['F_lower'] - 1e-13 and max(f_values) <= bounds['F_upper'] + 1e-13)
            clock_values = lapse_values / numerical.sqrt(f_values)
            check(label + '_E_enclosed', min(clock_values) >= bounds['E_lower'] - 1e-13 and max(clock_values) <= bounds['E_upper'] + 1e-13)
            check(label + '_N_enclosed', min(lapse_values) >= bounds['N_lower'] - 1e-13 and max(lapse_values) <= bounds['N_upper'] + 1e-13)
            h_l1_sampled = float(numerical.dot(quadrature.quadrature_weights, abs(profile['hamiltonian_defect'])))
            e_l1_sampled = float(numerical.dot(quadrature.quadrature_weights, abs(profile['lapse_defect'])))
            check(label + '_norm_majorants_not_quadrature_cancellation', h_l1_sampled <= mass_defect_bound and e_l1_sampled <= lapse_defect_bound)
            lapse_integral = numerical.dot(quadrature.quadrature_weights, profile['clock_log_r'])
            check(label + '_radial_clock_integral_identity', abs(float(lapse_integral - numerical.log(clock_values[-1] / clock_values[0]))) < 1e-12)
            record = {'label': label, 'time': sample['time'], 'bounds': bounds, 'S_L1_majorant': scalar_square_bound, 'rH_L1_majorant': mass_defect_bound, 'rE_L1_majorant': lapse_defect_bound, 'rH_L1_sampled': h_l1_sampled, 'rE_L1_sampled': e_l1_sampled, 'F_min_actual': float(min(f_values)), 'N_min_actual': float(min(lapse_values)), 'outer_clock_trace': float(outer_clock), 'outer_clock_prescribed': float(system.outer_clock), 'outer_clock_trace_minus_prescribed': float(outer_clock - system.outer_clock), 'numeric_outward_interval_certificate': False, 'norm_majorants_use_actual_metric_variations_not_a_closed_bootstrap': True}
            report['samples'].append(record)
            if index == steps:
                print(json.dumps(record), flush=True)
        check('all_sources_and_outputs_preserved', all(digest(root / name) == expected for name, expected in inputs.items()) and all(digest(root / name) == expected for name, expected in outputs.items()))
        check('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
        report.update(state='complete', passed=sum(row['passed'] for row in report['checks']), total=len(report['checks']), completed_utc=datetime.now(timezone.utc).isoformat())
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')
        (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')
        print(json.dumps({name: report[name] for name in ['state', 'passed', 'total']}), flush=True)
        return
    report_path = destination / 'status.json'
    report = json.loads(report_path.read_text())
    if report['state'] != 'complete' or report['passed'] != report['total']:
        raise RuntimeError('Radial gate incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260909-metric-flux-cancellation-and-exact-constraint-jets.md'
    final_path = intake / 'annular-coupled-metric-bootstrap-final-integrity.json'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.json', '.md', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-coupled-metric-bootstrap-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    outputs[str(snapshot.relative_to(root))] = digest(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 17, 10, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench or cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'metric_flux_jet_checks': gate['total'], 'radial_bootstrap_checks': report['total'], 'canonical_saved_states': len(report['samples']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T17:10:00Z; not full pre-turn hash comparison', 'mutable_resume_pinned_as_snapshot': True, 'no_bytecode_cache': True, 'canonical_local_second_constraint_jets_derived': True, 'radial_metric_and_scalar_H2_conditional_bounds_derived': True, 'mesh_uniform_coupled_metric_bootstrap_closed': False, 'full_coupled_DAE_solved': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'metric_flux_jet_checks', 'radial_bootstrap_checks', 'canonical_saved_states', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()

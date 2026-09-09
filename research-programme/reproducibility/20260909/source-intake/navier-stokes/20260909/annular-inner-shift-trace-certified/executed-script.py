import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis, coefficient_jets
    from annular_clock_spatial_bound_20260909 import spatial_bounds
    from annular_gram_joint_action_20260909 import gram_matrices
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_metric_source_bound_20260909 import scalar_source_data
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian

    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['derive', 'seal'])
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260909'
    destination = intake / 'annular-inner-shift-trace-certified'
    final_path = intake / 'annular-clock-spatial-and-inner-shift-final-integrity.json'
    gate_path = intake / 'annular-clock-spatial-gradient-derived/status.json'
    gate = json.loads(gate_path.read_text())
    inputs, outputs = {}, {}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path):
        inputs[str(path.relative_to(root))] = digest(path)

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

    if gate['state'] != 'complete' or gate['passed'] != gate['total']:
        raise RuntimeError('Spatial gradient gate incomplete.')
    inherit(inputs, gate['inputs'])
    inherit(outputs, gate['outputs'])
    for path in [gate_path, gate_path.parent / 'COMPLETE', gate_path.parent / 'executed-script.py', Path(__file__)]:
        own(path)
    compile(Path(__file__).read_bytes(), str(__file__), 'exec')
    if arguments.phase == 'derive':
        destination.mkdir(exist_ok=False)
        (destination / 'executed-script.py').write_bytes(Path(__file__).read_bytes())
        checks, samples = [], []

        def check(name, passed, detail=None):
            checks.append({'name': name, 'passed': bool(passed), 'detail': detail})
            if not passed:
                failure = {'state': 'failed', 'checks': checks, 'inputs': inputs, 'outputs': outputs, 'samples': samples}
                (destination / 'status.json').write_text(json.dumps(failure, indent=2) + '\n')
                raise RuntimeError('Failed check: ' + name)

        rational = symbolic.Rational
        kappa, inner, outer = rational(1, 10), rational(47, 8), rational(49, 8)
        f_min, f_max, n_min, n_max = rational(13, 20), rational(17, 25), rational(4, 5), rational(21, 25)
        q_max, w_max = rational(1, 50), rational(3, 100)
        weight_lower = 1 / (kappa * n_max * f_max * rational(5, 6))
        weight_upper = 1 / (kappa * n_min * f_min * rational(4, 5))
        gap = 2 * weight_lower - weight_upper
        p_max = rational(16807, 640)
        inverse_clock = 1 / (n_min**2 * f_min)
        bulk_flux = kappa * outer**2 * f_max * q_max * w_max
        template_constant = 4 * 96 * rational(1, 8) + 5 * 384 * rational(1, 128) + 2 * 576 * rational(1, 256)
        check('exact_weight_gap_positive', gap > 0)
        check('exact_link_current_density_constant_below_68', template_constant < 68)
        check('exact_sqrt_bounds', rational(4, 5)**2 <= f_min and rational(5, 6)**2 >= f_max)
        gram_density = 68 * p_max * q_max * w_max * inverse_clock
        exact_bounds = {'GR': 3 * weight_upper * bulk_flux / gap, 'metric_Gram': 3 * (weight_upper * bulk_flux + gram_density) / gap}
        check('exact_both_shift_bounds_finite_positive', all(value > 0 for value in exact_bounds.values()))
        case_path = intake / 'annular-constraint-correction-initial/canonical.json'
        own(case_path)
        case = json.loads(case_path.read_text())
        constants = {name: float(symbolic.sympify(value)) for name, value in case['parameters'].items()}
        for intervals in [16, 32, 64]:
            steps = 64 if intervals == 64 else 32
            for branch in ['GR', 'metric_Gram']:
                tag = 'canonical_N' + str(intervals) + '_' + branch
                source = loaded(intake / 'annular-released-Hermite-initial-derived' / (tag + '.npz'))
                folder = 'annular-boundary-N64-evolution-smoke' if intervals == 64 else 'annular-released-Hermite-evolution-smoke'
                trajectory = loaded(intake / folder / (tag + '_steps' + str(steps) + '.npz'))
                basis = MixedActionBasis(source['radius'])
                links = MetricLinkQuadrature(basis)
                count = basis.radii.size
                factors, sampling = gram_matrices(count)
                norm_one = numerical.sum(abs(factors), axis=1)
                anchors = sampling @ numerical.arange(count)
                distances = numerical.sum(abs(factors) * abs(numerical.arange(count)[None, :] - anchors[:, None]), axis=1)
                count_margin, count_adjacent = count - 3, count - 4
                check(tag + '_owned_factor_family_count', factors.shape[0] == count_margin + count_adjacent + 2)
                products = 2 * distances * norm_one
                check(tag + '_factor_current_bounds', max(products[:count_margin]) <= 12 + 1e-12 and max(products[count_margin:count_margin + count_adjacent]) <= 3 + 1e-12 and max(products[-2:]) <= 9 / 4 + 1e-12)
                starts = numerical.array([numerical.flatnonzero(row)[0] for row in factors])
                ends = numerical.array([numerical.flatnonzero(row)[-1] for row in factors])
                check(tag + '_finite_factor_supports', bool(numerical.all(ends[:count_margin] - starts[:count_margin] <= 3)) and bool(numerical.all(ends[count_margin:count_margin + count_adjacent] - starts[count_margin:count_margin + count_adjacent] <= 4)) and bool(numerical.all(ends[-2:] - starts[-2:] <= 5)))
                occupancy = max(numerical.sum(products[(starts <= point) & (ends >= point)]) for point in numerical.arange(0, count - 1, .5))
                check(tag + '_overlapping_factor_current_constant', occupancy < 68)
                widths = numerical.diff(basis.faces)
                star_lengths = numerical.concatenate([widths, [0.]]) + numerical.concatenate([[0.], widths])
                for index in [0, steps // 2, steps]:
                    label = tag + '_sample' + str(index)
                    time, state = trajectory['time'][index], trajectory['state'][index]
                    scalar, slope, momentum, slope_momentum = [state[part * count:(part + 1) * count] for part in range(4)]
                    packed = state[4 * count:]
                    include_gram = branch != 'GR'
                    system = ReleasedHermiteRouthian(basis, scalar, slope, constants, float(kappa), momentum, slope_momentum, source['outer_clock'][0] + time * source['outer_clock'][1], links)
                    speed, pairing, matter, gram = system.shift_mass_velocity(packed, include_gram)
                    residual = pairing @ speed + matter - gram
                    defect = float(numerical.max(abs(residual) / star_lengths))
                    bound = float(exact_bounds[branch]) + 6 * defect / float(gap)
                    observed_gap = (2 * numerical.diag(pairing) - numerical.sum(abs(pairing), axis=1)) / star_lengths
                    check(label + '_actual_pairing_diagonal_gap', min(observed_gap) >= float(gap) / 6 - 1e-11)
                    check(label + '_bulk_shift_density_bound', float(numerical.max(abs(matter) / star_lengths)) <= float(weight_upper * bulk_flux / 2) + 1e-11)
                    check(label + '_Gram_shift_density_bound', float(numerical.max(abs(gram) / star_lengths)) <= (float(gram_density) / 2 if include_gram else 0) + 1e-11)
                    node_mass = basis.face_to_node @ packed[system.slices[0]]
                    coefficient, gradient, unused_hessian = coefficient_jets(packed[system.slices[2]], system.gradient_node, node_mass, packed[system.slices[1]], basis.radii, constants)
                    check(label + '_canonical_local_shift_coefficient_derivative_zero', bool(numerical.all(gradient[4] == 0)))
                    leading, leading_time = factors @ scalar, factors @ packed[system.slices[2]]
                    factor_coefficient = sampling @ coefficient
                    current = coefficient[links.node] * links.sweight * leading[links.factor] * leading_time[links.factor] / basis.spacing
                    current -= packed[system.slices[2]][links.node] * links.tweight * factor_coefficient[links.factor] * leading[links.factor] / basis.spacing
                    link_bound = float(p_max * q_max * w_max) * distances[links.factor] * (links.sweight * norm_one[links.factor] + abs(links.tweight))
                    check(label + '_individual_actual_link_current_bound', bool(numerical.all(abs(current) <= link_bound + 1e-12)))
                    check(label + '_entire_physical_shift_and_inner_trace_bound', max(abs(speed)) <= bound + 1e-11 and abs(speed[0]) <= bound + 1e-11)
                    previous = loaded(intake / 'annular-clock-spatial-gradient-derived' / (label + '.npz'))
                    tangent = system.constraint_tangent(packed, include_gram, source['endpoint_acceleration'], source['outer_clock'][1])
                    check(label + '_no_boundary_rate_was_replaced', tangent['packed_speed'][0] == speed[0] and numerical.array_equal(tangent['packed_speed'], previous['packed_speed']))
                    source_data = scalar_source_data(system, packed, include_gram, source['endpoint_acceleration'])
                    record = next(row for row in gate['samples'] if row['label'] == label)
                    closed = spatial_bounds(system, source_data, previous['mass_static_residual'], previous['mass_time_residual'], bound, source['outer_clock'][1], source['endpoint_acceleration'], include_gram, record['measured']['effective_constraint_rate_residual_dual'], record['measured']['scalar_constraint_rate_residual_m'])
                    check(label + '_substitution_is_an_upper_bound_not_new_data', closed['theta_radial_L2_bound'] >= record['bounds']['theta_radial_L2_bound'] - 1e-12)
                    samples.append({'label': label, 'branch': branch, 'intervals': intervals, 'time': float(time), 'actual_inner_shift_rate': float(speed[0]), 'actual_shift_max': float(max(abs(speed))), 'all_grid_shift_bound': bound, 'shift_equation_residual_per_star': defect, 'coefficient_and_inner_flux_derived_bounds': closed})
                    if index == steps:
                        print(json.dumps({'label': label, 'actual_inner': float(speed[0]), 'shift_bound': bound, 'theta_R_L2_bound_with_derived_inner': closed['theta_radial_L2_bound']}), flush=True)
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('source_hashes_unchanged', all(digest(root / name) == expected for name, expected in inputs.items()))
        check('evidence_hashes_unchanged', all(digest(root / name) == expected for name, expected in outputs.items()))
        check('no_bytecode_cache', not (root / 'scripts/__pycache__').exists())
        report = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs, 'outputs': outputs, 'checks': checks, 'passed': sum(row['passed'] for row in checks), 'total': len(checks), 'samples': samples, 'exact_constants': {'weight_lower': str(weight_lower), 'weight_upper': str(weight_upper), 'positive_diagonal_gap_factor': str(gap), 'factor_overlap_majorant': str(template_constant), 'rounded_factor_majorant': '68', 'GR_shift_bound': str(exact_bounds['GR']), 'Gram_shift_bound': str(exact_bounds['metric_Gram'])}, 'actual_shift_trace_bound_derived_not_prescribed': True, 'scope': 'Every canonical configuration in the existing box, including metric-link Gram shift. Actual shift equation residual retained in its star-volume norm.', 'scalar_graph_energy_still_time_dependent_input': True, 'clock_gradient_bound_is_L2_not_Linfinity': True, 'energy_transport_reclosed': False, 'valid_for_physics_claim': False}
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')
        (destination / 'COMPLETE').write_text(report['completed_utc'] + '\n')
        print(json.dumps({'state': report['state'], 'passed': report['passed'], 'total': report['total'], 'constants': report['exact_constants']}), flush=True)
        return
    report_path = destination / 'status.json'
    report = json.loads(report_path.read_text())
    if report['state'] != 'complete' or report['passed'] != report['total']:
        raise RuntimeError('Inner shift gate incomplete.')
    inherit(inputs, report['inputs'])
    inherit(outputs, report['outputs'])
    for path in [report_path, destination / 'COMPLETE', destination / 'executed-script.py']:
        own(path)
    note = root / 'DERIVATION-20260909-clock-spatial-gradient-and-derived-coefficient-input.md'
    cited = [value for value in re.findall(r'`([^`]+)`', note.read_text(encoding='utf-8')) if value.endswith(('.py', '.md', '.json', '.npz'))]
    missing = [value for value in cited if root / value != final_path and not (root / value).is_file()]
    if missing:
        raise FileNotFoundError(str(missing))
    own(note)
    snapshot = intake / 'annular-clock-spatial-and-inner-shift-resume-snapshot.md'
    with snapshot.open('xb') as handle:
        handle.write((root / 'CURRENT_LOCAL_RESUME.md').read_bytes())
    outputs[str(snapshot.relative_to(root))] = digest(snapshot)
    frozen = root.parent / 'formalization-workbench'
    since = datetime(2026, 9, 9, 21, 11, 0, tzinfo=timezone.utc).timestamp()
    touched = [str(path.relative_to(frozen)) for path in frozen.rglob('*') if path.is_file() and path.stat().st_mtime >= since]
    if touched or (root / 'scripts/__pycache__').exists():
        raise RuntimeError('Protected workbench/cache check failed: ' + repr(touched))
    final = {'state': 'complete', 'completed_utc': datetime.now(timezone.utc).isoformat(), 'spatial_checks': gate['total'], 'inner_shift_checks': report['total'], 'saved_states': len(report['samples']), 'manufactured_cases': len(gate['manufactured']), 'inputs': inputs, 'outputs': outputs, 'cited_local_paths_checked': cited, 'protected_workbench_files_written_since_turn_start': len(touched), 'protected_check_method': 'mtime scan since 2026-09-09T21:11:00Z, not full pre-turn hash baseline', 'mutable_resume_pinned_as_snapshot': True, 'no_bytecode_cache': True, 'spatial_coefficient_and_inner_shift_inputs_derived': True, 'clock_rate_gradient_and_paired_remainder_L2_bound_derived': True, 'energy_transport_reclosed': False, 'valid_for_physics_claim': False}
    with final_path.open('x') as handle:
        json.dump(final, handle, indent=2)
        handle.write('\n')
    print(json.dumps({name: final[name] for name in ['state', 'spatial_checks', 'inner_shift_checks', 'saved_states', 'manufactured_cases', 'protected_workbench_files_written_since_turn_start']}), flush=True)


if __name__ == '__main__':
    run()

import argparse
import hashlib
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def virtual_work_control(system, packed, configuration, sources):
    import numpy as numerical
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    links, basis = MetricLinkQuadrature(system.basis, sources['source_order']), system.basis
    count = system.node_count
    mass, lapse = packed[system.slices[0]], packed[system.slices[1]]
    coefficient = basis.radii**2 * lapse * numerical.sqrt(1 - 2 * (basis.face_to_node @ mass) / basis.radii)
    coefficient_time = .17 * coefficient * numerical.sin(basis.radii)
    velocity = packed[system.slices[2]]
    leading = links.collect(links.tweight * configuration[:count][links.node])
    endpoint, partial = sources['endpoint_jacobian'], sources['partial_jacobian']
    leading_time = links.collect(links.tweight * velocity[links.node] * endpoint)
    density = links.collect(links.sweight * coefficient[links.node] * endpoint)
    density_time = links.collect(links.sweight * coefficient_time[links.node] * endpoint**2)
    width = .02
    profile = numerical.cos(2 * links.points) + .3
    nodes, weights = numerical.polynomial.hermite.hermgauss(48)
    total_raw = total_anchor = total_physical = total_wrong = 0.
    for node, weight in zip(nodes, weights):
        time = width * node
        amplitude = leading + time * leading_time
        temporal_density = density + time * density_time
        local_coefficient = coefficient[links.node] + endpoint * time * coefficient_time[links.node]
        pulse = numerical.exp(-(partial * node)**2)
        displacement = endpoint * links.integrate(profile * pulse / partial)
        displacement_time = endpoint * links.integrate(profile * (-2 * partial * time / width**2) * pulse)
        amplitude_variation = links.collect(links.tweight * velocity[links.node] * displacement)
        density_variation = links.collect(links.sweight * (coefficient_time[links.node] * endpoint * displacement + local_coefficient * displacement_time))
        raw = -numerical.sum(2 * amplitude * amplitude_variation * temporal_density + amplitude**2 * density_variation) / (2 * basis.spacing)
        current = amplitude[links.factor] * (links.sweight * local_coefficient * leading_time[links.factor] - links.tweight * velocity[links.node] * temporal_density[links.factor]) / basis.spacing
        anchor = numerical.dot(current, displacement)
        inverse_times = time / partial
        pairs = links.pairs
        factors = links.factor[pairs]
        pulled_amplitude = leading[factors] + inverse_times * leading_time[factors]
        pulled_density = density[factors] + inverse_times * density_time[factors]
        pulled_coefficient = coefficient[links.node[pairs]] + endpoint[pairs] * inverse_times * coefficient_time[links.node[pairs]]
        pulled_current = pulled_amplitude * (links.sweight[pairs] * pulled_coefficient * leading_time[factors] - links.tweight[pairs] * velocity[links.node[pairs]] * pulled_density) / basis.spacing
        physical = numerical.dot(links.weights, pulled_current * endpoint[pairs] / partial**2 * profile)
        wrong = numerical.dot(links.weights, pulled_current * endpoint[pairs] * profile)
        total_raw += width * weight * numerical.exp(node**2) * raw
        total_anchor += width * weight * numerical.exp(node**2) * anchor
        total_physical += width * weight * physical
        total_wrong += width * weight * wrong
    scale = max(abs(total_raw), abs(total_physical), 1e-30)
    return {'raw_action_first_variation': float(total_raw), 'after_temporal_integration_by_parts': float(total_anchor), 'physical_time_adjoint': float(total_physical), 'raw_vs_adjoint_absolute_error': float(abs(total_raw - total_physical)), 'raw_vs_adjoint_relative_error': float(abs(total_raw - total_physical) / scale), 'temporal_IBP_error': float(abs(total_raw - total_anchor)), 'negative_control_missing_Jr_squared_error': float(abs(total_wrong - total_physical)), 'scope': 'Independent raw delta-J variation and physical-time pullback quadratures for the exactly soluble auxiliary connection f(t,R)=t*g(R), with linear time-dependent scalar and coefficient data and a Gaussian variation. Not a full nonlinear ADM history solve.'}


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_time_link_adjoint_20260911 import frozen_maps, coupled_slice_jet, slice_sources

    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', required=True)
    arguments = parser.parse_args()
    if not arguments.attempt.isalnum():
        raise ValueError('Attempt must be alphanumeric.')
    root = Path(__file__).resolve().parents[1]
    destination = root / 'source-intake/navier-stokes/20260911' / ('annular-time-link-adjoint-' + arguments.attempt)
    destination.mkdir(parents=True, exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'Gram_jet_interval_certified': False, 'new_evolution': False, 'boundary_condition_selected': False}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path):
        report['inputs'][str(path.relative_to(root))] = digest(path)

    def artifact(path):
        report['outputs'][str(path.relative_to(root))] = digest(path)

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    save()
    try:
        prior = root / 'source-intake/navier-stokes/20260911/annular-initial-shift-jet-probe02/status.json'
        own(prior)
        inherited = json.loads(prior.read_text())
        check('previous_GR_attempt_complete', inherited['state'] == 'complete')
        for table in ['inputs', 'outputs']:
            for name, expected in inherited[table].items():
                if digest(root / name) != expected:
                    raise RuntimeError('Inherited evidence changed: ' + name)
                report['inputs'][name] = expected
        for name in ['annular_time_link_adjoint_20260911.py', Path(__file__).name]:
            path = root / 'scripts' / name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            snapshot = destination / ('executed-' + name)
            snapshot.write_bytes(path.read_bytes())
            artifact(snapshot)
        case_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
        own(case_path)
        constants = {name: float(symbolic.sympify(value)) for name, value in json.loads(case_path.read_text())['parameters'].items()}
        roots = root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02'
        for branch in ['GR', 'metric_Gram']:
            label = 'canonical_N16_' + branch + '_sample0'
            report['active_sample'] = label
            save()
            print('Starting ' + label, flush=True)
            path = roots / (label + '.npz')
            own(path)
            with numerical.load(path) as archive:
                saved = {name: archive[name].copy() for name in archive.files}
            basis = MixedActionBasis(saved['basis_radii'])
            count = basis.radii.size
            configuration, momenta = saved['original_configuration'], saved['original_momenta']
            packed = (saved['initial_root_box_lower'] + saved['initial_root_box_upper']) / 2
            system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], saved['affine_clock'][0], MetricLinkQuadrature(basis))
            maps = frozen_maps(system, packed, configuration)
            cases = []
            for boundary_rate in [0., .001, -.001]:
                result = coupled_slice_jet(system, packed, configuration, saved['endpoint_acceleration'], maps, branch != 'GR', boundary_rate)
                check(label + '_coupled_midpoint_equations_' + str(boundary_rate), max(result['residuals'].values()) < 1e-9, result['residuals'])
                check(label + '_weighted_anchor_current_' + str(boundary_rate), abs(result['sources']['anchor_cancellation']).max() < 1e-12)
                cases.append({'boundary_rate': boundary_rate, 'maximum_lapse_rate': float(abs(basis.node_value @ result['lapse_rate']).max()), 'maximum_shift_rate': float(abs(result['shift_speed']).max()), 'maximum_scalar_acceleration': float(abs(result['acceleration']).max()), 'maximum_J_minus_one': float(abs(result['sources']['endpoint_jacobian'] - 1).max()), 'schur_condition': float(numerical.linalg.cond(result['schur'])), 'residuals': result['residuals']})
                if boundary_rate == 0:
                    primary = result
            refined = coupled_slice_jet(system, packed, configuration, saved['endpoint_acceleration'], maps, branch != 'GR', 0., 16)
            differences = {name: float(abs(primary[name] - refined[name]).max()) for name in ['mass_rate', 'shift_rate', 'lapse_rate', 'acceleration']}
            check(label + '_quadrature_refinement_control', max(differences.values()) < 1e-3, differences)
            zero = slice_sources(system, packed, configuration, maps, numerical.zeros_like(primary['shift_rate']))
            check(label + '_unit_time_Jacobian_limit', numerical.array_equal(zero['endpoint_jacobian'], numerical.ones_like(zero['endpoint_jacobian'])))
            boost = .2 / max(float(abs(primary['sources']['endpoint_log']).max()), 1e-12)
            stress_sources = slice_sources(system, packed, configuration, maps, boost * primary['shift_rate'])
            control = virtual_work_control(system, packed, configuration, stress_sources)
            check(label + '_independent_raw_action_adjoint', control['raw_vs_adjoint_relative_error'] < 1e-6, control)
            check(label + '_missing_Jacobian_negative_control_detected', control['negative_control_missing_Jr_squared_error'] > 100 * control['raw_vs_adjoint_absolute_error'], control)
            arrays = {name: value for name, value in primary.items() if isinstance(value, numerical.ndarray)}
            arrays.update({'map_' + name: value for name, value in maps.items()})
            arrays.update({'source_' + name: value for name, value in primary['sources'].items() if isinstance(value, numerical.ndarray)})
            output = destination / (label + '.npz')
            numerical.savez_compressed(output, **arrays)
            with numerical.load(output) as archive:
                check(label + '_archive_roundtrip', set(archive.files) == set(arrays) and all(numerical.array_equal(value, archive[name]) for name, value in arrays.items()))
            artifact(output)
            if branch == 'GR':
                reference = root / 'source-intake/navier-stokes/20260911/annular-initial-shift-jet-probe02' / (label + '.npz')
                own(reference)
                with numerical.load(reference) as archive:
                    for name in ['mass_rate', 'shift_rate', 'lapse_rate', 'acceleration']:
                        lower, upper = archive[name + '_lower'], archive[name + '_upper']
                        if lower.ndim == 2:
                            lower, upper = lower[:, 0], upper[:, 0]
                        check(label + '_' + name + '_inside_GR_certificate', numerical.all(primary[name] >= lower) and numerical.all(primary[name] <= upper))
            row = {'label': label, 'boundary_rate_cases': cases, 'order8_vs_order16_jet_differences': differences, 'virtual_work_control': control, 'Gram_interval_certificate': False, 'quadrature_error_certified': False, 'full_parent_evolution_proved': False}
            report['samples'].append(row)
            save()
            print(json.dumps(row), flush=True)
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        report['completed_utc'] = datetime.now(timezone.utc).isoformat()
        report.pop('active_sample', None)
        save()
        print('Complete: ' + str(len(report['checks'])) + ' checks', flush=True)
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        report['traceback'] = traceback.format_exc()
        save()
        raise


if __name__ == '__main__':
    run()

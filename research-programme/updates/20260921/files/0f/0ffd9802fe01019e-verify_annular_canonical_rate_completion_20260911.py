import hashlib
import json
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_adm_mixed_action_20260909 import MixedActionBasis, linear_value_gradient
    from annular_metric_link_quadratic_20260909 import MetricLinkQuadrature
    from annular_released_hermite_action_20260909 import ReleasedHermiteRouthian
    from annular_canonical_inverse_boundary_20260911 import InverseBoundaryInitialData
    from annular_canonical_reference_fields_20260911 import ConstructedGRFields, SavedCanonicalFields, local_rate_families
    from annular_canonical_rate_completion_20260911 import OriginalFrames, bubbles, complete_phase, evaluate_initial

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / 'annular-canonical-rate-completion-control-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False}

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def archive(path):
        own(path)
        with numerical.load(path, allow_pickle=False) as saved:
            return {name: saved[name].copy() for name in saved.files}

    save()
    try:
        own(Path(__file__))
        compile(Path(__file__).read_bytes(), __file__, 'exec')
        snapshot = destination / ('executed-' + Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        status_path = intake / 'annular-canonical-rate-completion-attempt01/status.json'
        own(status_path)
        status = json.loads(status_path.read_text())
        check('main_attempt_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
        parameter_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
        own(parameter_path)
        constants = {name: float(symbolic.sympify(value)) for name, value in json.loads(parameter_path.read_text())['parameters'].items()}
        for branch in ['GR', 'metric_Gram']:
            source = archive(root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02' / ('canonical_N16_' + branch + '_sample0.npz'))
            basis = MixedActionBasis(source['basis_radii'])
            count = basis.radii.size
            configuration, momenta = source['original_configuration'], source['original_momenta']
            packed = (source['initial_root_box_lower'] + source['initial_root_box_upper']) / 2
            links = MetricLinkQuadrature(basis)
            system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], source['affine_clock'][0], links)
            saved = archive(intake / 'annular-canonical-inverse-boundary-attempt01' / ('N16_' + branch + '_outer_clock.npz'))
            model = InverseBoundaryInitialData(system, packed, configuration, branch != 'GR', saved['boundary_velocity'].copy(), normalize_clock=True)
            model.pi_coeff_seed = saved['pi_coefficients'].copy()
            model.set_state(saved['state'])
            physical = ConstructedGRFields(basis, archive(intake / 'annular-canonical-gr-boundary-reference-attempt01/constructed_GR_first_jet.npz'), system.outer_clock) if branch == 'GR' else SavedCanonicalFields(model, saved)
            original = OriginalFrames(model)
            knots = numerical.unique(numerical.concatenate([original.knots, physical.knots]))
            gauss, gauss_weights = numerical.polynomial.legendre.leggauss(12)
            halfwidth = numerical.diff(knots) / 2
            points = ((knots[:-1] + knots[1:])[:, None] / 2 + halfwidth[:, None] * gauss).ravel()
            weights = (halfwidth[:, None] * gauss_weights).ravel()
            surfaces = {'quad': points, 'check': points.copy(), 'nodes': basis.radii, 'links': links.points}
            frames = {phase: {} for phase in ['mass', 'scalar']}
            rates = {phase: {} for phase in ['mass', 'scalar']}
            reservoir, data = {}, {}
            for surface, coordinates in surfaces.items():
                maps = original.evaluate(coordinates)
                value, gradient = linear_value_gradient(basis.radii, coordinates)
                data[surface] = physical.evaluate(coordinates)
                data[surface].update({'R': coordinates, 'eta': value, 'eta_r': gradient})
                families = local_rate_families(data[surface], coordinates, value, gradient)
                bubble, bubble_r = bubbles(knots, coordinates, 4)
                reservoir[surface] = {'q': bubble, 'qr': bubble_r}
                for phase in frames:
                    frames[phase][surface] = maps[phase]
                    rates[phase][surface] = {kind: families[phase + '_' + kind] for kind in ['q', 'qr', 'p']}
            completed, coordinate_only, dimensions = {}, {}, {}
            for phase in frames:
                completed[phase], diagnostic = complete_phase(frames[phase], rates[phase], reservoir, weights)
                retained = diagnostic['original_phase_dimension'] + diagnostic['position_rate_additions']
                coordinate_only[phase] = {surface: {kind: value[:, :retained] for kind, value in maps.items()} for surface, maps in completed[phase].items()}
                dimensions[phase] = retained
            results = {}
            for name, phase_frames in [('coordinate_only', coordinate_only), ('completed', completed)]:
                result = evaluate_initial(phase_frames['mass'], phase_frames['scalar'], data, basis, weights, links, branch != 'GR', system.outer_clock)
                nodes = data['nodes']
                bulk_flux = .1 * basis.radii**2 * nodes['F'] * result['q_nodes'] * nodes['w']
                delta_flux = result['mu_t_nodes'] - bulk_flux
                boundary_prediction = numerical.zeros(count)
                boundary_prediction[0] = -delta_flux[0] / (.1 * numerical.sqrt(nodes['F'][0])) + result['gram_scalar'][0] * result['q_nodes'][0] / nodes['N'][0]
                boundary_prediction[-1] = delta_flux[-1] / (.1 * numerical.sqrt(nodes['F'][-1])) + result['gram_scalar'][-1] * result['q_nodes'][-1] / nodes['N'][-1]
                trace_flux = bulk_flux[[0, -1]] + numerical.array([1., -1.]) * .1 * numerical.sqrt(nodes['F'][[0, -1]]) * result['q_nodes'][[0, -1]] * result['gram_scalar'][[0, -1]] / nodes['N'][[0, -1]]
                identity_error = float(abs(result['constraint_rate'] - boundary_prediction).max())
                record = {'constraint_rate_max': float(abs(result['constraint_rate']).max()), 'interior_constraint_rate_max': float(abs(result['constraint_rate'][1:-1]).max()), 'boundary_constraint_rates': result['constraint_rate'][[0, -1]].tolist(), 'boundary_prediction': boundary_prediction[[0, -1]].tolist(), 'full_boundary_identity_error': identity_error, 'weak_mass_flux_endpoints': result['mu_t_nodes'][[0, -1]].tolist(), 'parent_trace_flux_endpoints': trace_flux.tolist(), 'mass_flux_trace_gaps': (result['mu_t_nodes'][[0, -1]] - trace_flux).tolist()}
                if name == 'completed':
                    check(branch + '_entire_remaining_Cdot_is_boundary_trace_defect', identity_error < 1e-11, identity_error)
                    if branch != 'GR':
                        omitted = boundary_prediction.copy()
                        omitted[[0, -1]] -= result['gram_scalar'][[0, -1]] * result['q_nodes'][[0, -1]] / nodes['N'][[0, -1]]
                        check('omitting_Gram_endpoint_force_is_detected', abs(omitted - result['constraint_rate']).max() > 1e-7)
                if branch == 'GR':
                    check(name + '_GR_all_constraint_rate_rows_close', abs(result['constraint_rate']).max() < 1e-12)
                output = destination / (branch + '_' + name + '.npz')
                numerical.savez_compressed(output, constraint_rate=result['constraint_rate'], boundary_prediction=boundary_prediction, parent_trace_flux=trace_flux, weak_mass_flux=result['mu_t_nodes'], q_nodes=result['q_nodes'], gram_scalar=result['gram_scalar'])
                own(output, 'outputs')
                results[name] = record
            lapse_checks = []
            for amplitude, harmonic in [(0.001, 1), (-0.003, 2), (0.002, 3)]:
                phase = (basis.radii - basis.radii[0]) / (basis.radii[-1] - basis.radii[0])
                variation = amplitude * numerical.sin(harmonic * numerical.pi * phase)
                variation[[0, -1]] = 0
                changed = {surface: {key: value.copy() for key, value in current.items()} for surface, current in data.items()}
                for current in changed.values():
                    current['N'] += current['eta'] @ variation
                    current['N_r'] += current['eta_r'] @ variation
                result = evaluate_initial(completed['mass'], completed['scalar'], changed, basis, weights, links, branch != 'GR', system.outer_clock)
                metric = float(abs(result['constraint_rate'] if branch == 'GR' else result['constraint_rate'][1:-1]).max())
                check(branch + '_unfitted_lapse_profile_' + str(harmonic), metric < 1e-11, metric)
                lapse_checks.append({'amplitude': amplitude, 'harmonic': harmonic, 'all_rows_max': float(abs(result['constraint_rate']).max()), 'interior_max': float(abs(result['constraint_rate'][1:-1]).max())})
            if branch == 'GR':
                phase_frames = completed
                reference = evaluate_initial(completed['mass'], completed['scalar'], data, basis, weights, links, False, system.outer_clock)
                mass_frame, scalar_frame = completed['mass']['quad'], completed['scalar']['quad']
                mass_nodes, scalar_nodes = completed['mass']['nodes'], completed['scalar']['nodes']
                current, nodes = data['quad'], data['nodes']
                mass_count, scalar_count = mass_frame['q'].shape[1], scalar_frame['q'].shape[1]
                cuts = [0, mass_count, 2 * mass_count, 2 * mass_count + scalar_count, 2 * mass_count + 2 * scalar_count]

                def hamiltonian(coordinates):
                    mass_change, geometric, scalar_change, scalar_momentum = [coordinates[cuts[index]:cuts[index + 1]] for index in range(4)]
                    mass = current['mu'] + mass_frame['q'] @ mass_change
                    mass_r = current['mu_r'] + mass_frame['qr'] @ mass_change
                    momentum = mass_frame['p'] @ geometric
                    scalar_r = current['w'] + scalar_frame['qr'] @ scalar_change
                    pi = current['pi'] + scalar_frame['p'] @ scalar_momentum
                    geometry = 1 - 2 * mass / points
                    inverse_root_r = (mass_r / points - mass / points**2) / geometry**1.5
                    density = -current['N'] * mass_r / (.1 * numerical.sqrt(geometry)) + current['N'] * numerical.sqrt(geometry) * (pi**2 / (2 * points**2) + points**2 * scalar_r**2 / 2)
                    density += .1 * current['N'] * geometry**1.5 * momentum * pi * scalar_r + .05 * points * geometry**3 * (inverse_root_r * current['N'] + current['N_r'] / numerical.sqrt(geometry)) * momentum**2
                    node_mass = nodes['mu'] + mass_nodes['q'] @ mass_change
                    node_scalar = nodes['chi'] + scalar_nodes['q'] @ scalar_change
                    node_momentum = mass_nodes['p'] @ geometric
                    node_geometry = 1 - 2 * node_mass / basis.radii
                    boundary_quadratic = .05 * basis.radii * nodes['N'] * node_geometry**2.5 * node_momentum**2
                    boundary = boundary_quadratic[-1] - boundary_quadratic[0] + system.outer_clock * node_mass[-1] / .1
                    boundary -= reference['reactions'][0] * node_mass[0] + reference['reactions'][1] * node_scalar[0] + reference['reactions'][2] * node_scalar[-1]
                    return weights @ density + boundary

                gradient_expected = numerical.concatenate([-reference['mass_pair'].T @ reference['P_rate_coeff'], reference['mass_pair'] @ reference['mass_rate_coeff'], -reference['scalar_pair'].T @ reference['pi_rate_coeff'], reference['scalar_pair'] @ reference['q_coeff']])
                derivative_errors = []
                for index in range(4):
                    direction = numerical.zeros(cuts[-1])
                    direction[cuts[index]:cuts[index + 1]] = numerical.sin(numerical.arange(cuts[index + 1] - cuts[index]) + .4) * .001
                    observed = hamiltonian(1e-25j * direction).imag / 1e-25
                    expected = gradient_expected @ direction
                    error = float(abs(observed - expected))
                    check('enlarged_action_derivative_phase_' + str(index), error < 1e-10, error)
                    derivative_errors.append(error)
                results['bulk_action_directional_errors'] = derivative_errors
            report['samples'].append({'branch': branch, 'coordinate_only_dimensions': dimensions, 'results': results, 'unfitted_lapse_checks': lapse_checks, 'valid_for_physics_claim': False})
            save()
            print(json.dumps(report['samples'][-1]), flush=True)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        save()
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        save()
        raise


if __name__ == '__main__':
    run()

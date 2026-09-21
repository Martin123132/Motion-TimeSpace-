import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
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

    parser = argparse.ArgumentParser()
    parser.add_argument('--attempt', required=True)
    arguments = parser.parse_args()
    if not arguments.attempt.isalnum():
        raise ValueError('Use a fresh alphanumeric attempt.')
    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260911'
    destination = intake / ('annular-canonical-rate-completion-' + arguments.attempt)
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'started_utc': datetime.now(timezone.utc).isoformat(), 'inputs': {}, 'outputs': {}, 'checks': [], 'samples': [], 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'protocol': 'Frozen initial phase-space completion from all local canonical lapse-rate families, not observed defects or eigenmodes. All original phase directions retained; continuous coordinate enrichments and continuous bubble duals; full MTS time-link terms retained. GR formula reference uses an affine initial field offset, so this isolates rate-space error without interpolating its physical fields. No initial-data refit, no time evolution.'}

    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = digest(path)

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    def archive(path):
        own(path)
        with numerical.load(path, allow_pickle=False) as saved:
            return {name: saved[name].copy() for name in saved.files}

    save()
    try:
        seal_path = intake / 'annular-canonical-inverse-boundary-final-integrity.json'
        own(seal_path)
        prior = json.loads(seal_path.read_text())
        check('prior_seal_complete', prior['state'] == 'complete')
        for table in ['inputs', 'outputs']:
            for name, expected in prior[table].items():
                if digest(root / name) != expected:
                    raise RuntimeError('Previously sealed evidence changed: ' + name)
                report['inputs'][name] = expected
        for name in ['annular_canonical_reference_fields_20260911.py', 'annular_canonical_rate_completion_20260911.py', Path(__file__).name]:
            path = root / 'scripts' / name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
            snapshot = destination / ('executed-' + name)
            snapshot.write_bytes(path.read_bytes())
            own(snapshot, 'outputs')
        parameter_path = root / 'source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json'
        own(parameter_path)
        constants = {name: float(symbolic.sympify(value)) for name, value in json.loads(parameter_path.read_text())['parameters'].items()}
        for branch in ['GR', 'metric_Gram']:
            label = 'N16_' + branch
            print('Building ' + label, flush=True)
            source = archive(root / 'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02' / ('canonical_N16_' + branch + '_sample0.npz'))
            basis = MixedActionBasis(source['basis_radii'])
            count = basis.radii.size
            configuration, momenta = source['original_configuration'], source['original_momenta']
            packed = (source['initial_root_box_lower'] + source['initial_root_box_upper']) / 2
            links = MetricLinkQuadrature(basis)
            check_links = MetricLinkQuadrature(basis, order=12)
            system = ReleasedHermiteRouthian(basis, configuration[:count], configuration[count:], constants, .1, momenta[:count], momenta[count:], source['affine_clock'][0], links)
            saved = archive(intake / 'annular-canonical-inverse-boundary-attempt01' / ('N16_' + branch + '_outer_clock.npz'))
            model = InverseBoundaryInitialData(system, packed, configuration, branch != 'GR', saved['boundary_velocity'].copy(), normalize_clock=True)
            model.pi_coeff_seed = saved['pi_coefficients'].copy()
            model.set_state(saved['state'])
            if branch == 'GR':
                reference = archive(intake / 'annular-canonical-gr-boundary-reference-attempt01/constructed_GR_first_jet.npz')
                physical = ConstructedGRFields(basis, reference, system.outer_clock)
                check('GR_reference_reconstructed_independently', physical.original_agreement < 1e-12, physical.original_agreement)
            else:
                physical = SavedCanonicalFields(model, saved)
            original = OriginalFrames(model)
            knots = numerical.unique(numerical.concatenate([original.knots, physical.knots]))

            def quadrature(order):
                nodes, weights = numerical.polynomial.legendre.leggauss(order)
                halfwidth = numerical.diff(knots) / 2
                return ((knots[:-1] + knots[1:])[:, None] / 2 + halfwidth[:, None] * nodes).ravel(), (halfwidth[:, None] * weights).ravel()

            points, weights = quadrature(12)
            check_points, check_weights = quadrature(16)
            surfaces = {'quad': points, 'check': check_points, 'old_quad': basis.quadrature, 'nodes': basis.radii, 'links': links.points, 'links_check': check_links.points}
            frames = {phase: {} for phase in ['mass', 'scalar']}
            families = {phase: {} for phase in ['mass', 'scalar']}
            reservoir, data = {}, {}
            for surface, coordinates in surfaces.items():
                maps = original.evaluate(coordinates)
                value, gradient = linear_value_gradient(basis.radii, coordinates)
                data[surface] = physical.evaluate(coordinates)
                data[surface].update({'R': coordinates, 'eta': value, 'eta_r': gradient})
                rates = local_rate_families(data[surface], coordinates, value, gradient)
                bubble, bubble_r = bubbles(knots, coordinates, 4)
                reservoir[surface] = {'q': bubble, 'qr': bubble_r}
                for phase in frames:
                    frames[phase][surface] = maps[phase]
                    families[phase][surface] = {kind: rates[phase + '_' + kind] for kind in ['q', 'qr', 'p']}
            if branch != 'GR':
                old = model.evaluate(numerical.concatenate([model.fixed_lapse, saved['state'][-3:]]))
                replay = evaluate_initial(frames['mass'], frames['scalar'], data, basis, basis.quadrature_weights, links, True, system.outer_clock, saved['state'][-3:], surface='old_quad')
                replay_error = max(abs(replay['constraint_rate'] - old['constraint_rate']).max(), abs(replay['mu_t'] - model.maps['mass_map'] @ old['mass_rate']).max(), abs(replay['pi_t'] - model.pi_map @ old['pi_rate']).max(), abs(replay['P_t'] - model.momentum_map @ old['momentum_rate']).max())
                check('original_MTS_full_time_link_action_replay', replay_error < 1e-10, float(replay_error))
            baseline = evaluate_initial(frames['mass'], frames['scalar'], data, basis, weights, links, branch != 'GR', system.outer_clock)
            completed, frame_diagnostics = {}, {}
            for phase in frames:
                completed[phase], frame_diagnostics[phase] = complete_phase(frames[phase], families[phase], reservoir, weights)
                diagnostic = frame_diagnostics[phase]
                check(label + '_' + phase + '_original_modes_retained_and_square', diagnostic['original_modes_removed'] == 0 and completed[phase]['quad']['q'].shape[1] == completed[phase]['quad']['p'].shape[1])
                check(label + '_' + phase + '_derived_triangular_pairing', diagnostic['pairing_block_identity_error'] < 1e-8, diagnostic['pairing_block_identity_error'])
            repaired = evaluate_initial(completed['mass'], completed['scalar'], data, basis, weights, links, branch != 'GR', system.outer_clock)
            overintegrated = evaluate_initial(completed['mass'], completed['scalar'], data, basis, check_weights, check_links, branch != 'GR', system.outer_clock, surface='check', link_surface='links_check')
            snapshots = {'original': baseline, 'completed': repaired, 'overintegrated': overintegrated}
            outcomes = {}
            for name, result in snapshots.items():
                surface = 'check' if name == 'overintegrated' else 'quad'
                current_weights = check_weights if surface == 'check' else weights
                current = data[surface]
                coordinates = current['R']
                local = local_rate_families(current, coordinates, current['N'][:, None], current['N_r'][:, None])
                geometry = current['F']
                energy = current['pi']**2 / (2 * coordinates**2) + coordinates**2 * current['w']**2 / 2
                coefficient = current['mu_r'] / (.1 * coordinates * geometry**1.5) + energy / (coordinates * numerical.sqrt(geometry))
                differences = {'mass': (result['mu_tr'] - local['mass_qr'][:, 0]) / (.1 * numerical.sqrt(geometry)) + coefficient * (result['mu_t'] - local['mass_q'][:, 0]), 'scalar_velocity': -coordinates**2 * numerical.sqrt(geometry) * current['w'] * (result['q_r'] - local['scalar_qr'][:, 0]), 'scalar_momentum': -numerical.sqrt(geometry) * current['pi'] / coordinates**2 * (result['pi_t'] - local['scalar_p'][:, 0]), 'geometric_momentum': -.1 * geometry**1.5 * current['pi'] * current['w'] * (result['P_t'] - local['mass_p'][:, 0])}
                channels = {channel: current['eta'].T @ (current_weights * value) for channel, value in differences.items()}
                channels['explicit_Gram'] = result['gram_constraint_rate']
                reconstruction_error = float(abs(sum(channels.values()) - result['constraint_rate']).max())
                check(label + '_' + name + '_complete_projection_defect_identity', reconstruction_error < 1e-10, reconstruction_error)
                outcomes[name] = {'constraint_max': float(abs(result['constraint']).max()), 'constraint_rate_max': float(abs(result['constraint_rate']).max()), 'inner_mass_velocity': float(result['mu_t_nodes'][0]), 'mass_drive_gap': float(result['mu_t_nodes'][0] - physical.boundary_drive[0]), 'outer_scalar_drive_gap': float(result['q_nodes'][-1] - physical.boundary_drive[2]), 'q_local_error_sampled': float(abs(result['q'] - local['scalar_q'][:, 0]).max()), 'mass_rate_local_bulk_error_sampled': float(abs(result['mu_t'] - local['mass_q'][:, 0]).max()), 'pi_rate_local_bulk_error_sampled': float(abs(result['pi_t'] - local['scalar_p'][:, 0]).max()), 'P_rate_local_bulk_error_sampled': float(abs(result['P_t'] - local['mass_p'][:, 0]).max()), 'channel_maxima': {channel: float(abs(value).max()) for channel, value in channels.items()}, 'projection_identity_error': reconstruction_error, 'maximum_time_link_log': float(abs(result['endpoint_log']).max())}
                arrays = {key: value for key, value in result.items() if isinstance(value, numerical.ndarray)}
                arrays.update({'channel_' + key: value for key, value in channels.items()})
                arrays.update({'field_' + key: value for key, value in current.items()})
                selected_frames = frames if name == 'original' else completed
                arrays.update({phase + '_' + key: value for phase in ['mass', 'scalar'] for key, value in selected_frames[phase][surface].items()})
                arrays['weights'] = current_weights
                check(label + '_' + name + '_finite_arrays', all(numerical.all(numerical.isfinite(value)) for value in arrays.values()))
                output = destination / (label + '_' + name + '.npz')
                numerical.savez_compressed(output, **arrays)
                with numerical.load(output, allow_pickle=False) as reread:
                    check(label + '_' + name + '_archive_roundtrip', set(reread.files) == set(arrays) and all(numerical.array_equal(value, reread[key]) for key, value in arrays.items()))
                own(output, 'outputs')
            record = {'label': label, 'phase_completion': frame_diagnostics, 'outcomes': outcomes, 'valid_for_physics_claim': False, 'enlarged_initial_data_solved': False, 'caveat': 'Natural spatial reactions used, not the prior fitted finite reactions. MTS rate errors against local GR bulk expressions include genuine Gram forcing, not solely discretization error. All Gram contributions retained in total Cdot.'}
            report['samples'].append(record)
            save()
            print(json.dumps(record), flush=True)
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        report['completed_utc'] = datetime.now(timezone.utc).isoformat()
        save()
        print('Canonical rate-space completion finished.', flush=True)
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        save()
        raise


if __name__ == '__main__':
    run()

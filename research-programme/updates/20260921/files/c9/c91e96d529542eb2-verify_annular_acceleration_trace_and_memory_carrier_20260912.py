import hashlib
import json
import sys
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_canonical_trace_context_20260911 import load_archive
    from annular_canonical_trace_projection_stable_20260911 import GlobalPrimitive
    from annular_cubic_lapse_reference_gravity_20260912 import evaluate_cubic_initial
    from annular_frozen_second_jet_complex_20260912 import FrozenSecondJet

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    source = intake / 'annular-acceleration-trace-completion-attempt02'
    destination = intake / 'annular-acceleration-memory-control-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'checks': [], 'cases': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'full_second_jet_closed': False, 'memory_time_carrier_derived_not_yet_phase_completed': True}

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def save():
        (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')

    def check(name, passed, detail=None):
        report['checks'].append({'name': name, 'passed': bool(passed), 'detail': detail})
        save()
        if not passed:
            raise RuntimeError(name + ': ' + repr(detail))

    save()
    try:
        prior = json.loads((source / 'status.json').read_text())
        own(source / 'status.json')
        check('paired_joint_trace_extension_completed_without_second_jet_claim', prior['state'] == 'complete' and all(not row['finite_full_second_jet_gate'] for row in prior['cases']))
        hashes = {}
        for table in ['inputs', 'outputs']:
            for name, expected in prior[table].items():
                if name not in hashes:
                    hashes[name] = hashlib.sha256((root / name).read_bytes()).hexdigest()
                if hashes[name] != expected:
                    raise RuntimeError('Changed evidence: ' + name)
                report['inputs'][name] = expected
        own(Path(__file__))
        snapshot = destination / ('executed-' + Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        common = CommonProfile(root)
        for branch in ['GR', 'metric_Gram']:
            saved = load_archive(source / (branch + '_completed_second_jet.npz'))
            for higher in [False, True]:
                model = FrozenSecondJet(common, branch, higher=higher)
                variant = 'higher' if higher else 'primary'
                for phase in model.frames:
                    archive = load_archive(source / (branch + '_extended_' + phase + '_frames.npz'))
                    original = model.frames[phase]
                    model.frames[phase] = {surface: {kind: archive[surface + '__' + kind] for kind in ['q', 'qr', 'p']} for surface in model.data}
                    check(branch + '_' + variant + '_' + phase + '_every_old_map_exactly_retained', all(numerical.array_equal(model.frames[phase][surface][kind][:, :old.shape[1]], old) for surface, maps in original.items() for kind, old in maps.items()))
                model.first = evaluate_cubic_initial(model.frames['mass'], model.frames['scalar'], model.data, model.basis, model.weights, model.links, model.gram, model.context.system.outer_clock, surface=model.surface, link_surface=model.link_surface)
                for surface in model.rates:
                    mass, scalar = model.frames['mass'][surface], model.frames['scalar'][surface]
                    model.rates[surface] = {'mu': mass['q'] @ model.first['mass_rate_coeff'], 'mu_r': mass['qr'] @ model.first['mass_rate_coeff'], 'P': mass['p'] @ model.first['P_rate_coeff'], 'pi': scalar['p'] @ model.first['pi_rate_coeff'], 'chi': scalar['q'] @ model.first['q_coeff'], 'w': scalar['qr'] @ model.first['q_coeff']}
                model.prepare_links()
                result = model.evaluate(saved['lapse_rate_coefficients'])
                evidence = load_archive(source / (branch + ('_higher_second_jet.npz' if higher else '_completed_second_jet.npz')))
                check(branch + '_' + variant + '_full_second_jet_replay', max(float(abs(result[key] - evidence[key]).max()) for key in ['constraint_second', 'compatibility', 'gram_P_first', 'gram_scalar_first']) < 1e-12)
                first_gate = max(float(abs(model.first[key]).max()) for key in ['constraint', 'constraint_rate'])
                first_gate = max(first_gate, float(abs(model.first['P_t_nodes'][[0, -1]]).max()), abs(model.first['mu_t_nodes'][0] - model.saved['boundary_velocity'][0]), abs(model.first['q_nodes'][-1] - model.saved['boundary_velocity'][2]))
                check(branch + '_' + variant + '_full_first_jet_still_passes', first_gate < 1e-10, float(first_gate))
                if not higher:
                    check(branch + '_three_second_boundary_rows_pass_primary', abs(result['compatibility'][-3:]).max() < 1e-10)
                nodes, rates = model.data['nodes'], model.rates['nodes']
                local, local_rates = model.data[model.surface], model.rates[model.surface]
                lapse_rate = nodes['eta'] @ saved['lapse_rate_coefficients']
                geometry_first = -2 * rates['mu'] / nodes['R']
                q, q_second = rates['chi'], result['nodes']['chi']
                bulk_kinematic_acceleration = .1 * nodes['R']**2 * (geometry_first * q * nodes['w'] + nodes['F'] * q_second * nodes['w'] + nodes['F'] * q * rates['w'])
                bulk_kinematic_acceleration += (.1 * nodes['R'] * nodes['F']**1.5 * (nodes['F'] * nodes['N_r'] - nodes['N'] * nodes['F_r'] / 2) - .1**2 * nodes['N'] * nodes['R']**2 * nodes['F']**3 * nodes['w']**2) * rates['P']
                cP = .1 * numerical.sqrt(nodes['F']) / nodes['N']
                cP_first = cP * (-rates['mu'] / (nodes['R'] * nodes['F']) - lapse_rate / nodes['N'])
                signs = numerical.array([-1., 1.])
                trace_memory_first = signs * ((cP_first * q + cP * q_second) * model.first['gram_scalar'] + cP * q * result['gram_scalar_first'])[[0, -1]] if model.gram else numerical.zeros(2)
                parent_acceleration = bulk_kinematic_acceleration[[0, -1]] - trace_memory_first
                flux_defect = result['nodes']['mu'][[0, -1]] - parent_acceleration
                boundary_covector = nodes['eta'][[0, -1]].T @ (signs * flux_defect / (.1 * numerical.sqrt(nodes['F'][[0, -1]])))
                strong_C0 = local['mu_r'] / (.1 * numerical.sqrt(local['F'])) - numerical.sqrt(local['F']) * (local['pi']**2 / (2 * local['R']**2) + local['R']**2 * local['w']**2 / 2)
                bracket = (local['eta'] * local['N_r'][:, None] - local['eta_r'] * local['N'][:, None]).T @ (model.weights * .1 * local['F']**1.5 * local_rates['P'] * strong_C0)
                record = {'branch': branch, 'variant': variant, 'Cddot_max': float(abs(result['constraint_second']).max()), 'Pddot_endpoints': result['nodes']['P'][[0, -1]].tolist(), 'parent_mass_acceleration_endpoints': parent_acceleration.tolist(), 'mass_acceleration_trace_defect': flux_defect.tolist(), 'boundary_covector_max': float(abs(boundary_covector).max()), 'residual_after_boundary_covector_max': float(abs(result['constraint_second'] - boundary_covector).max()), 'GR_bracket_prediction_error': float(abs(result['constraint_second'] - boundary_covector - bracket).max()), 'GR_bracket_applies_to_GR_only': True}
                if not model.gram:
                    check(variant + '_GR_residual_explained_by_constraint_bracket_and_boundary', record['GR_bracket_prediction_error'] < 3e-8, record['GR_bracket_prediction_error'])
                else:
                    generator = .1 * numerical.sqrt(local['F']) * local_rates['P'] / local['N']
                    primitive = GlobalPrimitive(model.context.knots, generator, 16 if higher else 12)
                    P_second = model.frames['mass'][model.surface]['p'] @ result['second']['P']
                    alpha = -local_rates['mu'] / (local['R'] * local['F']) - (local['eta'] @ saved['lapse_rate_coefficients']) / local['N']
                    bvalue = .1 * numerical.sqrt(local['F']) / local['N'] * (P_second + 2 * alpha * local_rates['P'])
                    second_primitive = GlobalPrimitive(model.context.knots, bvalue * numerical.exp(primitive.evaluate(local['R'])), 16 if higher else 12)
                    links = model.links
                    target_g, anchor_g = primitive.evaluate(links.targets), primitive.evaluate(links.anchors)
                    target_B, anchor_B = second_primitive.evaluate(links.targets), second_primitive.evaluate(links.anchors)
                    coefficient_C = model.current * numerical.exp(target_g + anchor_g)
                    coefficient_D = result['current_first'] * numerical.exp(target_g + 2 * anchor_g) + coefficient_C * (target_B + anchor_B)
                    cell_points = model.basis.radii[:-1] + .371 * model.basis.spacing
                    oriented = ((cell_points[:, None] > numerical.minimum(links.anchors, links.targets)) & (cell_points[:, None] < numerical.maximum(links.anchors, links.targets))) * numerical.sign(links.targets - links.anchors)
                    cells_C, cells_D = oriented @ coefficient_C, oriented @ coefficient_D
                    cell = numerical.clip(numerical.searchsorted(model.basis.radii, local['R'], side='right') - 1, 0, model.basis.radii.size - 2)
                    local_g, local_B = primitive.evaluate(local['R']), second_primitive.evaluate(local['R'])
                    multiplier = .1 * numerical.sqrt(local['F']) / local['N']
                    memory_bulk_first = multiplier * numerical.exp(-3 * local_g) * cells_D[cell] + multiplier * (alpha * numerical.exp(-2 * local_g) - 2 * local_B * numerical.exp(-3 * local_g)) * cells_C[cell]
                    predicted = model.frames['mass'][model.surface]['p'].T @ (model.weights * memory_bulk_first)
                    predicted += model.frames['mass']['nodes']['p'].T @ (2 * .1**2 * nodes['R']**2 * nodes['N'] * nodes['F']**2.5 * model.nodal_density * rates['P'])
                    record['memory_time_carrier_weak_error'] = float(abs(predicted - result['gram_P_first']).max())
                    record['memory_time_anchor_jump_cancellation'] = float(max(abs(links.collect(coefficient_C)).max(), abs(links.collect(coefficient_D)).max()))
                    check(variant + '_derived_two_carrier_memory_force_time_family', record['memory_time_carrier_weak_error'] < 1e-8, record['memory_time_carrier_weak_error'])
                    check(variant + '_memory_time_anchor_jumps_cancel', record['memory_time_anchor_jump_cancellation'] < 1e-9, record['memory_time_anchor_jump_cancellation'])
                    path = destination / (variant + '_derived_memory_time_carriers.npz')
                    numerical.savez_compressed(path, radius=local['R'], global_g=local_g, global_B=local_B, alpha=alpha, cells_C=cells_C, cells_D=cells_D, bulk_memory_force_time=memory_bulk_first, boundary_covector=boundary_covector, residual_after_boundary=result['constraint_second'] - boundary_covector)
                    own(path, 'outputs')
                report['cases'].append(record)
                save()
        for module in tuple(sys.modules.values()):
            filename = getattr(module, '__file__', None)
            if filename:
                path = Path(filename).resolve()
                if path.parent == root / 'scripts' and path.suffix == '.py':
                    own(path)
        check('no_python_cache', not (root / 'scripts/__pycache__').exists())
        report['state'] = 'complete'
        save()
        print(json.dumps({'state': report['state'], 'checks': len(report['checks']), 'cases': report['cases']}), flush=True)
    except Exception as error:
        report.update({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()})
        save()
        raise


if __name__ == '__main__':
    run()

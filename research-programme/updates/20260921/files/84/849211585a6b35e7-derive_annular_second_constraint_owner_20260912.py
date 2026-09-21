import hashlib
import json
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from annular_canonical_common_profile_aligned_20260912 import CommonProfile
    from annular_canonical_trace_context_20260911 import load_archive
    from annular_cubic_lapse_reference_gravity_20260912 import evaluate_cubic_initial
    from annular_frozen_second_jet_complex_20260912 import FrozenSecondJet

    root = Path(__file__).resolve().parents[1]
    intake = root / 'source-intake/navier-stokes/20260912'
    source = intake / 'annular-acceleration-trace-completion-attempt02'
    destination = intake / 'annular-second-constraint-owner-attempt01'
    destination.mkdir(exist_ok=False)
    report = {'state': 'running', 'cases': [], 'inputs': {}, 'outputs': {}, 'valid_for_physics_claim': False, 'new_evolution': False, 'interval_certificate': False, 'MTS_full_bracket_identity_proven': False}
    previous_path = intake / 'annular-acceleration-memory-control-attempt01/status.json'
    previous = json.loads(previous_path.read_text())
    if previous['state'] != 'complete':
        raise RuntimeError('Previous control is not complete.')
    known = {}
    for table in ['inputs', 'outputs']:
        for name, expected in previous[table].items():
            if name not in known:
                known[name] = hashlib.sha256((root / name).read_bytes()).hexdigest()
            if known[name] != expected:
                raise RuntimeError('Changed evidence: ' + name)
            report['inputs'][name] = expected
    for path in [previous_path, Path(__file__)]:
        report['inputs'][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
    snapshot = destination / ('executed-' + Path(__file__).name)
    snapshot.write_bytes(Path(__file__).read_bytes())
    report['outputs'][str(snapshot.relative_to(root))] = hashlib.sha256(snapshot.read_bytes()).hexdigest()
    common = CommonProfile(root)
    for branch in ['GR', 'metric_Gram']:
        for higher in [False, True]:
            model = FrozenSecondJet(common, branch, higher=higher)
            for phase in model.frames:
                archive = load_archive(source / (branch + '_extended_' + phase + '_frames.npz'))
                model.frames[phase] = {surface: {kind: archive[surface + '__' + kind] for kind in ['q', 'qr', 'p']} for surface in model.data}
            model.first = evaluate_cubic_initial(model.frames['mass'], model.frames['scalar'], model.data, model.basis, model.weights, model.links, model.gram, model.context.system.outer_clock, surface=model.surface, link_surface=model.link_surface)
            for surface in model.rates:
                mass, scalar = model.frames['mass'][surface], model.frames['scalar'][surface]
                model.rates[surface] = {'mu': mass['q'] @ model.first['mass_rate_coeff'], 'mu_r': mass['qr'] @ model.first['mass_rate_coeff'], 'P': mass['p'] @ model.first['P_rate_coeff'], 'pi': scalar['p'] @ model.first['pi_rate_coeff'], 'chi': scalar['q'] @ model.first['q_coeff'], 'w': scalar['qr'] @ model.first['q_coeff']}
            model.prepare_links()
            values, nodes = model.data[model.surface], model.data['nodes']
            result = load_archive(source / (branch + ('_higher_second_jet.npz' if higher else '_completed_second_jet.npz')))
            energy = values['pi']**2 / (2 * values['R']**2) + values['R']**2 * values['w']**2 / 2
            strong = values['mu_r'] / (.1 * numerical.sqrt(values['F'])) - numerical.sqrt(values['F']) * energy
            tests = .1 * (values['F']**1.5 * model.rates[model.surface]['P'])[:, None] * (values['eta'] * values['N_r'][:, None] - values['eta_r'] * values['N'][:, None])
            bulk = tests.T @ (model.weights * strong)
            node_tests = .1 * (nodes['F']**1.5 * model.rates['nodes']['P'])[:, None] * (nodes['eta'] * nodes['N_r'][:, None] - nodes['eta_r'] * nodes['N'][:, None])
            nodal = -node_tests.T @ (nodes['R']**2 * numerical.sqrt(nodes['F']) * model.nodal_density) if model.gram else numerical.zeros(19)
            record = {'branch': branch, 'variant': 'higher' if higher else 'primary', 'bulk_weighted_constraint_max': float(abs(bulk).max()), 'candidate_nodal_weighted_constraint_max': float(abs(nodal).max()), 'full_nodal_candidate_error': float(abs(result['constraint_second'] - bulk - nodal).max()), 'bulk_only_error': float(abs(result['constraint_second'] - bulk).max()), 'full_nodal_candidate_matches_at_1e8_gate': bool(abs(result['constraint_second'] - bulk - nodal).max() < 1e-8), 'same_GR_algebra_with_nodal_constraint_is_hypothesis_not_proven': model.gram, 'one_sided_nodal_gradients_inherited': True}
            report['cases'].append(record)
            path = destination / (branch + '_' + record['variant'] + '_weighted_constraint_comparison.npz')
            numerical.savez_compressed(path, bulk=bulk, nodal=nodal, actual=result['constraint_second'], residual=result['constraint_second'] - bulk - nodal, generated_test_values=tests, generated_node_test_values=node_tests)
            report['outputs'][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
            print(json.dumps(record), flush=True)
    report['state'] = 'complete'
    (destination / 'status.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    run()

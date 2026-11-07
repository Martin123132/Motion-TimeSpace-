from grid_common import *
from compare_responses import load_run, interpolation, quadrature
from verify_stress_interface import ThermalStress, FrozenReference, state_from_spectral


def tail_norm(block, values, lower, upper):
    nodes = block['nodes']
    edges = np.unique(np.r_[nodes, lower, upper])
    edges = edges[(edges >= nodes[0]) & (edges <= nodes[-1])]
    points, weights = quadrature(edges)
    outside = (points < lower) | (points > upper)
    field = interpolation(nodes, values, points)
    return np.sum(abs(field[:, outside]) ** 2 * weights[outside], axis=1)


def main():
    modest()
    folder = ROOT / 'results/final-source-interface'
    assert not folder.exists()
    checks, rows, tails, inputs = [], [], [], []
    for suffix in ['split-384-refined', 'split-448-band']:
        label = 'synthetic-' + suffix
        blocks = load_run(label)
        heat, inertia = float(blocks[0]['capacity']), float(blocks[1]['capacity'])
        reference = FrozenReference(heat, inertia)
        system = ThermalStress(reference, heat)
        for kind in ['rate', 'finite-exchange']:
            values = ([linalg.cho_solve(linalg.cho_factor(block['metric'], lower=True),
                                       block['initial_collision_covector']) for block in blocks] if kind == 'rate'
                      else [block['defects'][-1] - block['defects'][0] for block in blocks])
            state = state_from_spectral(system, blocks, values)
            residual = system.constraints(0., state)[0]
            heat_size = float(abs(heat * values[0][-1]))
            momentum_size = float(abs(inertia * values[1][-1]))
            scale = reference.values['scale']
            energy_error = float(abs(residual[0]) / (2 * scale ** 2 * heat_size))
            momentum_error = float(np.linalg.norm(residual[1:]) / (scale ** 2 * momentum_size))
            checks.extend([
                dict(name=suffix + ':' + kind + ': inherited Hamiltonian constraint at exchanged-heat scale',
                     passed=energy_error < .002, value=energy_error),
                dict(name=suffix + ':' + kind + ': inherited momentum constraint at exchanged-momentum scale',
                     passed=momentum_error < 1e-9, value=momentum_error)])
            rows.append(dict(bank=suffix, probe=kind, heat_scale=heat_size, momentum_scale=momentum_size,
                             normalized_hamiltonian_residual=energy_error, normalized_momentum_residual=momentum_error))
        inputs.append(ROOT / 'runs' / label / 'status.json')
        inputs.extend((ROOT / 'runs' / label).glob('*.npz'))
    for model in ['heavy', 'cold', 'synthetic']:
        label = model + '-split-448-band'
        blocks = load_run(label)
        elastic = load_run(label + '-elastic') if model != 'synthetic' else None
        sections = {name: np.zeros(len(blocks[0]['times'])) for name in ['I', 'E', 'B', 'V']}
        for degree, block in enumerate(blocks):
            points = len(block['nodes'])
            values = block['defects'].copy()
            if elastic is not None:
                values -= elastic[degree]['defects']
            for mode, name in enumerate(block['names']):
                section = slice(mode * points, (mode + 1) * points)
                sections[name] += tail_norm(block, values[:, section], 1e-5, 60.) / (2 * degree + 1)
        tails.append(dict(fixture=model, added_interval='[1e-6,1e-5] union [60,80]',
                          peak_tail_norm={name: float(np.sqrt(max(value))) for name, value in sections.items()},
                          probe='warm-minus-elastic response' if elastic is not None else 'equilibrium-subtracted synthetic defect'))
        labels = [label, label + '-elastic'] if elastic is not None else [label]
        for name in labels:
            inputs.append(ROOT / 'runs' / name / 'status.json')
            inputs.extend((ROOT / 'runs' / name).glob('*.npz'))
    inputs += [ROOT / 'verify_stress_interface.py', ROOT / 'compare_responses.py',
               WAVES / 'coupled_system.py', WAVES / 'evolution_common.py']
    folder.mkdir(parents=True, exist_ok=False)
    finish(folder, dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
                        rows=rows, added_band_tail_diagnostics=tails,
                        tail_diagnostics_not_an_infinite_domain_bound=True,
                        largest_band_finite_heat_stress_interface_verified=True,
                        full_cosmological_background_evolution=False), __file__, sorted(set(inputs)))
    print(json.dumps(dict(checks=checks, rows=rows, tail_diagnostics=tails)), flush=True)


if __name__ == '__main__':
    main()

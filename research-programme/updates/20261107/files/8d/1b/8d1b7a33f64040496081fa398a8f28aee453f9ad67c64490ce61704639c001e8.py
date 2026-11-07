from common230 import *


def identity():
    names = ['bounds230.py', 'BRANCH-BOUND.md']
    for model in ('heavy', 'cold'):
        for count in (3200, 6400):
            names.extend([f'runs/{model}-{count}/history.npz', f'runs/{model}-{count}/status.json'])
    return {name: digest(ROOT / name) for name in names}


def histories(values, step):
    output = np.empty_like(values[1:])
    output[0] = values[0] / step
    output[1:] = (2 * values[1:-1] - .5 * values[:-2]) / step
    return output


def main():
    modest()
    protocol()
    assert read(ROOT / 'bound-configuration.json')['input_hashes'] == identity()
    inputs = read(ROOT / 'results/preflight-inputs.json')
    checks, reports = [], []
    for model in ('heavy', 'cold'):
        system = System(model, 6400, inputs)
        mass = (system.basis.mass + system.basis.mass.T) / 2
        factor = linalg.cho_factor(mass)
        energy = system.basis.energy
        defect = energy - system.basis.temperature @ mass
        epsilon = math.sqrt(max(float(defect @ linalg.cho_solve(factor, defect)), 0.))
        energy_dual = float(energy @ linalg.cho_solve(factor, energy))
        for count in (3200, 6400):
            folder = ROOT / f'runs/{model}-{count}'
            status = read(register(inputs, folder / 'status.json'))
            assert status['qualified']
            with np.load(register(inputs, folder / 'history.npz')) as archive:
                saved = dict(archive)
            rows = saved['rows']
            step = float(rows[-1, 0] / count)
            alpha = np.full(count, 1.5 / step)
            alpha[0] = 1 / step
            scales = system.background.start_scale * np.exp(rows[1:, 0])
            heat = system.heat
            photon = system.background.parent.photons / scales**4
            reference = system.background.parent.radiation / scales**4 + (system.background.parent.baryons + system.background.parent.cold) / scales**3
            for kind in ('NR', 'EOS'):
                column = 0 if kind == 'NR' else 1
                capacity = np.ones(count) if kind == 'NR' else saved['C0'][1:]
                A0 = np.ones(count) if kind == 'NR' else saved['A0'][1:]
                gamma = capacity * (alpha - 1) + 2
                profiles = saved['profiles'][:, :, 0] if kind == 'NR' else np.sum(saved['profiles'], axis=2)
                vector = histories(profiles, step)
                photon_rhs = vector @ system.basis.mass.T
                norm_photon = np.einsum('ij,ij->i', photon_rhs, linalg.cho_solve(factor, photon_rhs.T).T) / alpha
                gas_rhs = heat * histories(rows[:, 3], step) - 1
                if kind == 'EOS':
                    gas_rhs += histories(rows[:, 5], step) - (alpha - 1) * (A0 - 1)
                norm_rhs = np.sqrt(norm_photon + gas_rhs**2 / (heat * gamma))
                eta = np.sqrt(alpha / (heat * gamma)) * epsilon
                functional = np.sqrt(energy_dual / alpha + heat * capacity**2 / gamma)
                Q = heat * (A0 + functional * norm_rhs / (1 - eta))
                thermal_derivative = heat**2 * abs(capacity - 2) * norm_rhs / (4 * alpha * np.sqrt(heat * gamma) * (1 - eta)**2)
                floor = reference - photon * Q
                fields = np.sum(saved['fields'][:, :, :, :2 if kind == 'NR' else 3], axis=3)
                field_history = histories(fields, step)
                energy_history = np.stack([field_history[:, 0, :] * system.mass, field_history[:, 1, :] / scales[:, None]], axis=1)
                history_norm = np.sum(energy_history**2, axis=1)
                P = np.sum(history_norm, axis=1) / (2 * alpha**2)
                lower = scales * np.sqrt(floor / 3)
                upper = scales * np.sqrt((reference + photon * Q + P) / 3)
                D = np.sum(history_norm * (scales[:, None] * system.mass / lower[:, None]), axis=1) / alpha**3
                J_lower = 1 - (D + photon * thermal_derivative) / (2 * floor)
                hubble = rows[1:, 12] * (1 + rows[1:, 13])
                if kind == 'EOS':
                    hubble *= 1 + rows[1:, 14]
                check(checks, f'{model}:{count}:{kind}: energy-row perturbation condition', int(np.max(eta) >= 1), 0)
                check(checks, f'{model}:{count}:{kind}: positive source density floor', int(np.min(floor) <= 0), 0)
                check(checks, f'{model}:{count}:{kind}: sufficient physical-model root Jacobian', int(np.min(J_lower) <= 0), 0)
                check(checks, f'{model}:{count}:{kind}: root lies in physical sufficient bracket',
                    int(np.any(hubble < lower * (1 - 1e-12)) or np.any(hubble > upper * (1 + 1e-12))), 0)
                reports.append(dict(model=model, count=count, variant=kind, minimum_J_lower=float(np.min(J_lower)),
                    maximum_energy_row_eta=float(np.max(eta)), maximum_absolute_heat_bound=float(np.max(Q)),
                    maximum_thermal_jacobian_penalty=float(np.max(photon * thermal_derivative / (2 * floor))),
                    minimum_density_floor_fraction=float(np.min(floor / reference)), cells=count))
                save_npz(ROOT / f'results/{model}-{count}-{kind}-bounds.npz', expansion=rows[1:, 0], Q=Q,
                    H_lower=lower, H_upper=upper, J_lower=J_lower, thermal_derivative=thermal_derivative, eta=eta)
    add_modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    write(ROOT / 'results/bound-inputs.json', inputs)
    assert not (ROOT / 'results/branch-bounds.json').exists()
    report = dict(stage=230, state='complete', finished_at=now(), checks=checks, models=reports,
        qualified=all(row['passed'] for row in checks), failed=[row for row in checks if not row['passed']],
        scope='Sufficient theorem evaluated for retained physical passive weak form; not a binary interval certificate')
    write(ROOT / 'results/branch-bounds.json', report)
    print(json.dumps(dict(checks=len(checks), failed=report['failed'], minimum_J=min(row['minimum_J_lower'] for row in reports),
        thermal_penalty=max(row['maximum_thermal_jacobian_penalty'] for row in reports))), flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'freeze':
        assert not (ROOT / 'bound-configuration.json').exists()
        write(ROOT / 'bound-configuration.json', dict(frozen_at=now(), input_hashes=identity(),
            condition='rho_floor>0, eta<1, J_lower>0', physical_weak_model_only=True))
        print('Physical branch-bound evaluation frozen', flush=True)
    elif sys.argv[1] == 'evaluate':
        main()
    else:
        raise ValueError(sys.argv[1])

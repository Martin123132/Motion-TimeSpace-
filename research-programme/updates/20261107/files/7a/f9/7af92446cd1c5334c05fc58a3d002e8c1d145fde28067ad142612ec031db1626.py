from common235 import *
import radial234


def main():
    modest()
    config = protocol()
    assert not (ROOT / 'results/mass.json').exists()
    checks, records, values = [], [], {}
    owner = angular.inherited.source.dressed
    spin = angular.inherited.source.exact
    alpha = mp.mpf(str(angular.inherited.source.ALPHA))
    with mp.workdps(80):
        for row in config['events']:
            parameters, unused = source.physics.parameters_and_weight(row['theta'], row['node'])
            energy, cosine = [mp.mpf(str(value)) for value in (parameters['energy'], parameters['cosine'])]
            initial = mp.matrix([1, 0, 0, 0])
            incoming = spin.photon(energy, mp.matrix([0, 0, 1]))
            outgoing = spin.photon(energy / (1 + energy * (1 - cosine)), mp.matrix([mp.sqrt(1 - cosine**2), 0, cosine]))
            final = initial + incoming - outgoing
            for label, momentum in [('initial', initial), ('final', final), ('moving', owner.on_shell([mp.mpf('.2'), mp.mpf('-.13'), mp.mpf('.07')]))]:
                states = spin.spinors(momentum)
                left = states.transpose_conj() * spin.gamma_matrices()[0]
                for index, (direction, unused_weight) in enumerate(angular.inherited.source.angular_nodes(2)):
                    null = spin.photon(mp.mpf(1), spin.unit(direction))
                    actual = owner.self_energy(momentum, null)
                    predicted = 2 * spin.slash(null) / spin.dot(momentum, null)
                    check(checks, f'{row["label"]}:{label}:ray{index}:on-shell matrix', mp.norm(actual - predicted) / mp.norm(predicted))
                    check(checks, f'{row["label"]}:{label}:ray{index}:full spin projection', mp.norm(left * actual * states - 4 * mp.eye(2)) / 4)
                    shift, unused = owner.external_shift(momentum, null)
                    check(checks, f'{row["label"]}:{label}:ray{index}:pole energy', abs(shift * momentum[0] / 2 - 1))
            temperature = scalar(row['theta'])
            planck = 2 * mp.pi * alpha * temperature**2 / 3
            for join in config['joins']:
                local = {}
                for order in config['radial_orders']:
                    radial = packet(PARENT / 'radial' / f'join{join}-order{order}.npz')
                    factor = 4 * alpha * temperature**2 / mp.pi
                    moment = [factor * scalar(value) for value in radial['constant'][:98]]
                    thermal = factor * (scalar(radial['constant'][-1]) + radial234.thermal_exterior(*config['spectral_domain']))
                    check(checks, f'{row["label"]}:join{join}:order{order}:thermal derivative mass', abs(thermal / (2 * planck) - 1))
                    values[f'{row["label"]}:join{join}:order{order}:mass_coefficients'] = np.array(list(map(float, moment)))
                    local[order] = moment
                check(checks, f'{row["label"]}:join{join}:mass vector refinement', relative(list(map(float, local[4])), list(map(float, local[6]))), .002)
                for state in config['states']:
                    physical = [scalar(config['heat']) * mp.mpf(value) for value in state['coefficients'][:98]]
                    shifts = [mp.fsum(value * coefficient for value, coefficient in zip(local[order], physical)) for order in config['radial_orders']]
                    check(checks, f'{row["label"]}:join{join}:{state["model"]}:{state["history"]}:history mass refinement', abs(shifts[0] / shifts[1] - 1), .002)
                    records.append(dict(anchor=row['label'], join=join, model=state['model'], history=state['history'],
                        finite_domain_delta_mass_squared=float(shifts[-1]), planck_mass_squared=float(planck),
                        fraction_of_planck=float(shifts[-1] / planck)))
    save(ROOT / 'results/mass-coefficients.npz', **values)
    failed = [entry for entry in checks if not entry['passed']]
    report = dict(state='complete', qualified=not failed, checks=checks, failed=failed, records=records,
        coefficient_sha256=digest(ROOT / 'results/mass-coefficients.npz'), finished_at=now(),
        mass_multipoles=[0], full_spinor_response_scalar=False, actual_exterior_assumed=False)
    write(ROOT / 'results/mass.json', report)
    print(json.dumps(dict(checks=len(checks), failed=failed, fraction_range=[min(row['fraction_of_planck'] for row in records), max(row['fraction_of_planck'] for row in records)])), flush=True)
    assert not failed, failed


if __name__ == '__main__':
    main()

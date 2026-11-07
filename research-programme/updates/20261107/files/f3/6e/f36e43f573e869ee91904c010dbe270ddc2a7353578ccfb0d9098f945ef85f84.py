from run233 import *


def hilbert(location):
    return (mp.log(location / (2 * mp.pi)) - mp.re(mp.digamma(mp.j * location / (2 * mp.pi)))) / 2


def temperature_derivative(location):
    return -mp.mpf('.5') + mp.re(mp.j * location * mp.polygamma(1, mp.j * location / (2 * mp.pi)) / (4 * mp.pi))


def main():
    modest()
    config, frozen = run_protocol()
    target = ROOT / 'results/medium-derivative.json'
    assert not target.exists()
    write(ROOT / 'medium-configuration.json', dict(frozen_at=now(), script_sha256=digest(Path(__file__)),
        derivation_sha256=digest(ROOT / 'MEDIUM-DERIVATIVE.md'), angular_order=2,
        identity_tolerance=1e-10, new_loop_amplitudes=0, finite_difference_step='1e-15'))
    checks, records = [], []
    with mp.workdps(80):
        for row in config['events']:
            parameters, unused = source.physics.parameters_and_weight(row['theta'], row['node'])
            assert read(row['loop_path'])['identity'] == source.physics.event_owner.inherited.virtual_identity(parameters)
            energy, cosine, temperature = map(lambda value: mp.mpf(str(value)), (parameters['energy'], parameters['cosine'], row['theta']))
            hard = energy / (1 + energy * (1 - cosine))
            hard_direction = mp.matrix([mp.sqrt(1 - cosine**2), 0, cosine])
            for index, (direction, weight) in enumerate(angular.inherited.source.angular_nodes(2)):
                ray = mp.matrix(list(map(lambda value: mp.mpf(str(value)), direction)))
                ray /= mp.norm(ray)
                bath = list(map(lambda value: mp.mpf(str(value)), parameters['bath']))
                doppler = bath[0] - mp.fsum(value * component for value, component in zip(bath[1:], ray))
                poles = [energy / (1 + energy * (1 - ray[2])), hard / (1 - hard * (1 - (hard_direction.T * ray)[0]))]
                for branch, pole, sign in zip(('direct', 'crossed'), poles, (-1, 1)):
                    location = pole * doppler / temperature
                    occupation = 1 / mp.expm1(location)
                    analytic = temperature_derivative(location) - mp.j * mp.pi * sign * location * occupation * (1 + occupation) / 2
                    def kernel(shift):
                        scaled = location / (1 + shift)
                        return hilbert(scaled) - mp.j * mp.pi * sign / (2 * mp.expm1(scaled))
                    step = mp.mpf('1e-15')
                    measured = (kernel(step) - kernel(-step)) / (2 * step)
                    error = abs(measured - analytic) / max(abs(analytic), mp.mpf('1e-300'))
                    name = f'{row["label"]}:ray{index}:{branch}'
                    check(checks, name + ':retained complex pole thermal derivative', error)
                    incorrect = 2 * kernel(0)
                    shortcut = abs(incorrect - analytic) / max(abs(analytic), mp.mpf('1e-300'))
                    check(checks, name + ':blanket T squared scaling rejected', int(shortcut <= mp.mpf('1e-10')), 0)
                    records.append(dict(anchor=row['label'], ray=index, branch=branch, location_over_local_temperature=float(location),
                        derivative_real=float(mp.re(analytic)), derivative_imaginary=float(mp.im(analytic)),
                        derivative_relative_error=float(error), blanket_T2_relative_error=float(shortcut)))
            constant = lambda shift: mp.pi**2 * temperature**2 * (1 + shift)**2 / 6
            step = mp.mpf('1e-15')
            check(checks, row['label'] + ':constant thermal moment derivative', ((constant(step) - constant(-step)) / (2 * step)) / (2 * constant(0)) - 1)
    failed = [row for row in checks if not row['passed']]
    write(target, dict(state='complete', qualified=not failed, checks=checks, failed=failed, records=records, finished_at=now(),
        new_loop_amplitudes=0, new_pole_coefficients=0, actual_saved_spectral_radial_integrals_evaluated=False,
        scope='Source-owned analytic thermal derivative at48 actual event/ray poles; generic spectral functional derived in the accompanying document'))
    print(json.dumps(dict(medium_checks=len(checks), failed=failed, minimum_wrong_T2_error=min(row['blanket_T2_relative_error'] for row in records))), flush=True)
    assert not failed, failed


if __name__ == '__main__':
    main()

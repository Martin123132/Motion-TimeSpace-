import argparse
from matched_weak import *


def main():
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--moving', action='store_true')
    parser.add_argument('--angular', type=int, default=4)
    parser.add_argument('--radial', type=int, default=28)
    parser.add_argument('--profile', type=float)
    parser.add_argument('--separator', type=float, default=1.)
    parser.add_argument('--floor', type=float, default=0.)
    parser.add_argument('--chemical', action='store_true')
    arguments = parser.parse_args()
    folder = ROOT / 'results' / arguments.name
    folder.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    temperature = .00045962015785263325
    velocity = [.02, .005, -.01] if arguments.moving else [0., 0., 0.]
    source_file = (BRANCH / 'moving-polarized-thermal-20261008/results'
                   / ('moving-a6-r40-v8' if arguments.moving else 'rest-a6-r40') / 'source.npz')
    with np.load(source_file) as saved:
        virtual = saved['virtual'].copy()
    parameters = source.context(temperature, .1, velocity, temperature)
    result = matched(parameters, virtual[0, 0], arguments.angular, arguments.radial,
                     arguments.profile, arguments.separator, arguments.floor, arguments.chemical)
    output = result['total']
    null = np.zeros(len(output))
    null[1 if arguments.chemical else 0] = 1.
    null[-1] = 1.
    checks = [
        dict(name='Finite matched scalar weak matrix', passed=bool(np.all(np.isfinite(output)))),
        check('Weak matrix is symmetric', relative(output, output.T), 1e-12),
        check('Common energy null follows independent event kinematics',
              np.linalg.norm(output @ null) / np.linalg.norm(output), 2e-7),
        check('Real events conserve energy before integration',
              result['real']['maximum_event_energy_null_residual'], 1e-12)]
    np.savez(folder / 'matrix.npz', total=output, born=result['born'], virtual=result['virtual'],
             spontaneous=result['real']['spontaneous'], thermal=result['real']['thermal'],
             logarithm=result['real']['logarithm'], profile_conversion=result['real']['profile_conversion'],
             phase=result['state']['phase'], observable_shift=result['state']['observable_shift'],
             canonical=result['state']['canonical'], population=result['state']['population'])
    finish(folder, dict(arguments=vars(arguments), checks=checks, count=len(checks),
           all_checks_passed=all(row['passed'] for row in checks), elapsed_seconds=time.monotonic() - started,
           temperature=temperature, velocity=velocity, vacuum_ratio=result['vacuum_ratio'],
           thermal_virtual_ratio=result['thermal_virtual_ratio'],
           born_reference=parameters['born_differential_over_thomson'],
           matched_norm=float(np.linalg.norm(output)), matched_matrix=output.tolist(),
           correction_over_born_norm=float(np.linalg.norm(output) / np.linalg.norm(result['born'])),
           integrated_soft_pole=result['real']['integrated_pole'],
           scope='Fixed incoming electron/seed/observed direction; scalar IR-regular test functions unless chemical flag; not population-averaged.'),
           __file__, [source_file, source_file.parent / 'status.json'])
    print(json.dumps(dict(name=arguments.name, seconds=time.monotonic() - started,
                         failed=[row for row in checks if not row['passed']],
                         norm=float(np.linalg.norm(output)),
                         ratio=float(np.linalg.norm(output) / np.linalg.norm(result['born'])))), flush=True)


if __name__ == '__main__':
    main()
